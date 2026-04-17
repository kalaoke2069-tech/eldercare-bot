"""
ElderCare Companion - 訊息處理 Logic
"""

import os
import re
from dotenv import load_dotenv

# 延遲載入,避免環境變數還沒設定就初始化
def _get_line_bot_api():
    """延遲初始化 LineBotApi,確保環境變數已載入"""
    load_dotenv()
    from linebot import LineBotApi
    _api = LineBotApi(os.getenv('LINE_ACCESS_TOKEN'))
    return _api

# 使用時才初始化
line_bot_api = None

def _get_api():
    global line_bot_api
    if line_bot_api is None:
        line_bot_api = _get_line_bot_api()
    return line_bot_api

from linebot.models import TextSendMessage, FlexSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction
from datetime import datetime
import random

from companions import COMPANION_PRESETS, get_companion, format_companion_for_ai
from ai_service import ask_ai
from database import record_message, get_user_companion, set_user_companion, daily_check_in, record_blood_pressure


# =====================================================
# Companion 選項設定(放在模組層級)
# =====================================================

COMPANION_OPTIONS = [
    ("scholar", "老陳(學者)", "愛聊經濟、股票、國際大事"),
    ("grandma", "美雲阿姨(長輩)", "溫暖會關心人,愛聊家庭"),
    ("comedian", "阿Ken(業務員)", "幽默風趣,愛開玩笑"),
    ("chef", "阿美姐(廚師)", "愛聊食譜、吃的話題"),
    ("astrologer", "韻璇(占星師)", "星座塔羅、靈性指引"),
    ("fengshui", "雲峰大師(命理師)", "易經八字、風水命理"),
    ("rockefeller", "洛克菲勒(商業導師)", "商業智慧、财富責任、人生導師"),
    ("li_ka_shing", "李嘉誠(華人超人)", "經商之道、逆境自強、慈善奉獻"),
    ("james_simons", "西蒙斯(量化傳奇)", "量化投資、數學之美、算法交易"),
]


# =====================================================
# 文字訊息處理
# =====================================================

def handle_text(reply_token, user_id, text):
    """處理一般文字訊息,交給 AI Companion 回覆"""

    # 1. 檢查數字選擇 (1-9)
    if text.strip() in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        idx = int(text.strip()) - 1
        companion_key = COMPANION_OPTIONS[idx][0]
        select_companion(reply_token, user_id, companion_key)
        return

    # 2. 檢查是否有選擇Companion的指令
    if text.startswith("選擇朋友:"):
        companion_key = text.replace("選擇朋友:", "").strip()
        select_companion(reply_token, user_id, companion_key)
        return

    # 3. 指令處理
    if text.startswith("/"):
        handle_command(reply_token, user_id, text)
        return

    # 3.5 檢查是否為血壓輸入(格式:120/80 或 120,80 或 120 80)
    bp_match = re.match(r'^(\d{2,3})[\/\s,]+(\d{2,3})$', text.strip())
    if bp_match:
        systolic = int(bp_match.group(1))
        diastolic = int(bp_match.group(2))

        # 簡單驗證
        if 60 <= systolic <= 250 and 40 <= diastolic <= 150:
            record_blood_pressure(user_id, systolic, diastolic)
            status = '✅ 血壓正常,繼續保持!' if systolic < 130 else '⚠️ 血壓偏高,建議注意飲食並持續觀察'
            response = f"""
📊 血壓記錄完成!

收縮壓:{systolic} mmHg
舒張壓:{diastolic} mmHg
時間:{datetime.now().strftime('%H:%M')}

{status}
            """
            _get_api().reply_message(reply_token, TextSendMessage(text=response))
            return
        else:
            _get_api().reply_message(reply_token, TextSendMessage(text="這個數值不太對喔,請確認血壓計顯示後再告訴我,例如:130/80"))
            return

    # 4. 日常聊天 → AI Companion 回覆
    companion_key = get_user_companion(user_id)
    if not companion_key:
        # 還沒選Companion → 引導選擇
        guide_companion_selection(reply_token, user_id)
        return

    companion = get_companion(companion_key)
    if not companion:
        guide_companion_selection(reply_token, user_id)
        return

    # 5. AI 回覆
    ai_response = ask_ai(
        user_id=user_id,
        message=text,
        companion_key=companion_key,
        system_prompt=format_companion_for_ai(companion)
    )

    # 6. 回覆LINE
    _get_api().reply_message(
        reply_token,
        TextSendMessage(text=ai_response)
    )

    # 7. 記錄對話
    record_message(user_id, text, ai_response, companion_key)


# =====================================================
# 圖片處理(血壓/血糖拍照)
# =====================================================

def handle_image(reply_token, user_id, image_path):
    """處理圖片:血壓計、血糖機拍照"""

    # 請用戶手動輸入血壓值
    response = """
📸 照片收到了!

請告訴我你的血壓數值,例如:
「130/80」或「130、80」

我會幫你記錄下來!
"""
    _get_api().reply_message(reply_token, TextSendMessage(text=response))


# =====================================================
# Postback(按鈕回調)
# =====================================================

def handle_postback(reply_token, user_id, data):
    """處理 Quick Reply / Button 的回調"""

    if data == "check_in":
        # 每日打卡
        daily_check_in(user_id)
        companion_key = get_user_companion(user_id)
        companion = get_companion(companion_key) if companion_key else None

        msg = "✅ 今天打卡完成!"
        if companion:
            companion_name = companion.get('name', '你的朋友')
            msg += f"\n{companion_name}說:{companion['greeting']}"

        _get_api().reply_message(reply_token, TextSendMessage(text=msg))

    elif data == "bp_record":
        # 血壓記錄
        _get_api().reply_message(
            reply_token,
            TextSendMessage(text="📸 請拍攝血壓計的數值畫面上傳,我會幫你記錄!")
        )

    elif data == "medicine_remind":
        # 用藥提醒
        _get_api().reply_message(
            reply_token,
            TextSendMessage(text="💊 用藥記錄功能即將上線,請期待!")
        )

    elif data == "emergency":
        # 緊急通報
        send_emergency(reply_token, user_id)

    elif data == "change_companion":
        # 換朋友
        guide_companion_selection(reply_token, user_id)


# =====================================================
# Companion 選擇
# =====================================================

def select_companion(reply_token, user_id, companion_key):
    """用戶選擇了某個Companion"""

    if companion_key not in COMPANION_PRESETS:
        _get_api().reply_message(
            reply_token,
            TextSendMessage(text="這個朋友不在名單上哦!")
        )
        return

    # 設定用戶的Companion
    set_user_companion(user_id, companion_key)
    companion = COMPANION_PRESETS[companion_key]

    response = f"""
🤝 設定成功!

從現在起,你的陪伴者是:
「{companion['name']}」

{companion['intro']}

明天開始每天都會跟你打招呼哦!🌞
    """

    _get_api().reply_message(reply_token, TextSendMessage(text=response))


def guide_companion_selection(reply_token, user_id):
    """引導用戶選擇Companion"""

    # 顯示9種人格選項
    options_text = "\n".join([f"{i+1}️⃣ {name} — {desc}" for i, (_, name, desc) in enumerate(COMPANION_OPTIONS)])
    
    text = f"""👋 嗨！我是你的AI陪伴者！

在開始聊天之前，告訴我你喜歡什麼類型的朋友？

{options_text}

請輸入數字 1-9 選擇！

輸入「更換朋友」可以看更多人格哦！"""

    _get_api().reply_message(reply_token, TextSendMessage(text=text))


# =====================================================
# 緊急通報
# =====================================================

def send_emergency(reply_token, user_id):
    """發送緊急通報給所有家人"""

    from database import get_family_members

    family = get_family_members(user_id)  # 取得所有家人LINE ID

    alert_message = f"""
🚨【緊急通報】

您的家人需要協助!
時間:{datetime.now().strftime('%Y/%m/%d %H:%M')}

請立即回覆或致電確認狀況。
"""

    # 發送給所有家人
    for member_id in family:
        try:
            _get_api().push_message(member_id, TextSendMessage(text=alert_message))
        except Exception as e:
            print(f"無法發送緊急通知給 {member_id}: {e}")

    # 回覆用戶
    _get_api().reply_message(reply_token, TextSendMessage(text=f"🚨 已通知所有家人(共{len(family)}位)!"))


# =====================================================
# 指令處理
# =====================================================

def handle_command(reply_token, user_id, command):
    """處理 /指令"""

    if command == "/help":
        help_text = """
🤖 EldeCare 指令:

/打卡 - 今日健康打卡
/bp - 記錄血壓(直接輸入數值如130/80)
/用藥 - 用藥提醒設定
/健康報告 - 本月健康趨勢
/更換朋友 - 選擇不同陪伴者
/緊急 - 立即通知家人
/hello - 和你的陪伴者打招呼
        """
        _get_api().reply_message(reply_token, TextSendMessage(text=help_text))

    elif command == "/打卡":
        daily_check_in(user_id)
        companion_key = get_user_companion(user_id)
        companion = get_companion(companion_key) if companion_key else None
        msg = "✅ 今日打卡完成!"
        if companion:
            msg += f"\n\n{companion['name']}說:{companion['greeting']}"
        _get_api().reply_message(reply_token, TextSendMessage(text=msg))

    elif command == "/hello":
        companion_key = get_user_companion(user_id)
        if not companion_key:
            guide_companion_selection(reply_token, user_id)
            return
        companion = get_companion(companion_key)
        _get_api().reply_message(
            reply_token,
            TextSendMessage(text=f"{companion['greeting']}\n\n[{companion['name']}]")
        )

    elif command == "/緊急":
        send_emergency(reply_token, user_id)

    else:
        _get_api().reply_message(
            reply_token,
            TextSendMessage(text=f"不確定的指令。輸入 /help 看所有指令。")
        )
