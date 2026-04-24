"""
ElderCare Companion — LINE Bot 主程式
LINE Webhook 接收 + 派發到各 handler
"""

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,
    FlexSendMessage, BubbleContainer, ImageComponent,
    BoxComponent, TextComponent, ButtonComponent,
    URIAction, MessageAction, QuickReply, QuickReplyButton,
    PostbackEvent, TemplateSendMessage, ButtonsTemplate, MessageAction
)
from dotenv import load_dotenv
import os

from handlers import handle_text, handle_image, handle_postback
from companions import COMPANION_PRESETS
from database import get_all_user_ids, get_user_companion
from ltc_data import get_all_resources_summary

load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('LINE_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

# =====================================================
# cron-job.org 每日打卡 endpoint
# =====================================================

@app.route("/cron/daily", methods=['GET', 'POST'])
def cron_daily_check():
    """
    cron-job.org 每天早上呼叫這個 endpoint
    對所有註冊用戶發送「還好嗎？」打卡問候
    
    使用方式：
    cron-job.org 設為 GET https://eldercare-bot-production.up.railway.app/cron/daily?token=YOUR_SECRET_TOKEN
    """
    
    # 驗證 token（防止別人乱call）
    expected_token = os.getenv('CRON_SECRET_TOKEN', 'eldercare_cron_secret_2026')
    received_token = request.args.get('token', '')
    
    if received_token != expected_token:
        return 'Unauthorized', 401
    
    # 取得所有用戶
    user_ids = get_all_user_ids()
    
    results = []
    for user_id in user_ids:
        companion_key = get_user_companion(user_id)
        companion = COMPANION_PRESETS.get(companion_key) if companion_key else None
        
        greeting = companion['greeting'] if companion else "早安！今天過得怎麼樣？"
        
        try:
            line_bot_api.push_message(user_id, TextSendMessage(text=greeting))
            results.append(f"OK: {user_id}")
        except Exception as e:
            results.append(f"FAIL: {user_id} - {e}")
    
    return f"Daily check sent to {len(results)} users"

# =====================================================
# 測試模式：懶人開關（True時直接用假的companion回覆）
TEST_MODE = False  # 生產環境設為False

# =====================================================
# LINE Webhook 接收
# =====================================================

@app.route("/callback", methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        # LINE Webhook 驗證
        # LINE 發送 GET 到此 URL，帶上 hub.verify_token 和 hub.challenge
        # 只要 verify_token 符合就回傳 hub.challenge
        verify_token = os.getenv('LINE_VERIFY_TOKEN', 'eldercare_verify_token')
        received_token = request.args.get('hub.verify_token', '')
        challenge = request.args.get('hub.challenge', '')
        
        if received_token == verify_token:
            return challenge
        else:
            abort(400)
    
    # POST: 處理訊息
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# =====================================================
# 訊息事件處理
# =====================================================

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_text = event.message.text.strip()

    # --- 選Companion模式 ---
    if user_text.startswith("選擇陪伴者") or user_text == "更換朋友":
        show_companion_selection(event.reply_token, user_id)
        return

    # --- 一般聊天 → AI Companion 回覆 ---
    handle_text(event.reply_token, user_id, user_text)

# =====================================================
# 圖片處理（血壓/血糖拍照上傳）
# =====================================================

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    user_id = event.source.user_id
    image_id = event.message.id

    # 下載圖片
    message_content = line_bot_api.get_message_content(image_id)
    temp_path = f"/tmp/{image_id}.jpg"
    with open(temp_path, 'wb') as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

    # 交给 image handler 處理
    handle_image(event.reply_token, user_id, temp_path)

# =====================================================
# Postback（按鈕回調）
# =====================================================

@handler.add(PostbackEvent)
def handle_postback(event):
    handle_postback(event.reply_token, event.source.user_id, event.postback.data)

# =====================================================
# Companion 選擇選單
# =====================================================

def show_companion_selection(reply_token, user_id):
    """顯示人格選擇選單"""

    bubbles = []

    # 每3個companion一組
    items = list(COMPANION_PRESETS.items())

    for i in range(0, len(items), 3):
        chunk = items[i:i+3]

        bubble = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "選擇你的朋友",
                        "size": "lg",
                        "bold": True,
                        "align": "center"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": []
            }
        }

        for key, companion in chunk:
            # 名稱
            name_text = f"🤖 {companion['name']}"
            # 描述
            desc_text = companion['intro'][:30] + "..."

            # 按鈕
            btn = {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "message",
                    "label": companion['name'],
                    "text": f"選擇朋友:{key}"
                }
            }

            item = {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {"type": "text", "text": name_text, "weight": "bold", "size": "md"},
                    {"type": "text", "text": desc_text, "size": "sm", "color": "#666666"}
                ]
            }

            bubble["body"]["contents"].append(item)
            bubble["body"]["contents"].append(btn)

        bubbles.append(bubble)

    # 發送 flex message
    flex = FlexSendMessage(
        alt_text="選擇你的陪伴者",
        contents={"type": "carousel", "contents": bubbles}
    )

    line_bot_api.reply_message(reply_token, flex)


def handle_command(reply_token, user_id, command):
    """處理指令"""
    if command == "/help":
        help_text = """
🤖 ElderCare 指令列表：

/打卡 — 今日打卡
/血壓 — 記錄血壓
/用藥 — 記服用藥
/健康報告 — 本月總結
/更換朋友 — 選擇不同陪伴者
/緊急 — 立即通知家人

輸入任何文字與我聊天！
        """
        line_bot_api.reply_message(reply_token, TextSendMessage(text=help_text))

    elif command == "/緊急":
        send_emergency_alert(user_id)
        line_bot_api.reply_message(reply_token, TextSendMessage(text="🚨 已通知所有家人！"))

    else:
        line_bot_api.reply_message(reply_token, TextSendMessage(text="不確定這個指令，輸入 /help 看所有指令"))


def send_emergency_alert(user_id):
    """發送緊急通報給所有家人"""
    # TODO: 從資料庫讀取此用戶的所有家人LINE ID
    # 然後逐一發送緊急訊息
    pass


# =====================================================
# 啟動
# =====================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("=" * 50)
    print("ElderCare Companion — LINE Bot")
    print("=" * 50)
    print(f"TEST_MODE: {TEST_MODE}")
    print(f"Companions loaded: {len(COMPANION_PRESETS)}")
    print(f"Starting on port {port}")
    print("=" * 50)

    # 生產模式
    app.run(host='0.0.0.0', port=port, debug=False)