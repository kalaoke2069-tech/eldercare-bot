"""
ElderCare Companion — AI 聊天服務
使用 MiniMax API 作為 Companion 的大腦
"""

import os
import json
import requests
from datetime import datetime
from companions import COMPANION_PRESETS

# =====================================================
# MiniMax API 設定
# =====================================================

MINIMAX_API_KEY = os.getenv('MINIMAX_API_KEY')
MINIMAX_GROUP_ID = os.getenv('MINIMAX_GROUP_ID', '2034883351168430090')

# 使用 Anthropic 兼容端點（國際版）
ANTHROPIC_BASE_URL = "https://api.minimax.io/anthropic"

# Model
MODEL = "MiniMax-M2"

# =====================================================
# 對話歷史管理（記憶）
# =====================================================

# 簡單的 in-memory 儲存（生產環境建議用 Redis）
# 格式: { user_id: [ {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."} ] }
CONVERSATION_HISTORY = {}

MAX_HISTORY_LENGTH = 20  # 保留最近20輪對話


def get_conversation_history(user_id):
    """取得用戶的對話歷史"""
    if user_id not in CONVERSATION_HISTORY:
        CONVERSATION_HISTORY[user_id] = []
    return CONVERSATION_HISTORY[user_id]


def add_to_history(user_id, role, content):
    """加入對話歷史"""
    history = get_conversation_history(user_id)
    history.append({"role": role, "content": content})

    # 超過長度就刪除最舊的
    if len(history) > MAX_HISTORY_LENGTH:
        CONVERSATION_HISTORY[user_id] = history[-MAX_HISTORY_LENGTH:]


def clear_history(user_id):
    """清除對話歷史"""
    CONVERSATION_HISTORY[user_id] = []


# =====================================================
# MiniMax API 呼叫
# =====================================================

def ask_ai(user_id, message, companion_key, system_prompt):
    """
    發送訊息給 MiniMax AI，返回 Companion 的回覆

    Args:
        user_id: LINE 用戶 ID
        message: 用戶說的話
        companion_key: Companion 人格 key
        system_prompt: 給 AI 的系統提示詞（格式化的人格設定）

    Returns:
        str: AI 的回覆文字
    """

    if not MINIMAX_API_KEY:
        return get_fallback_response(message, companion_key)

    # 建立對話
    history = get_conversation_history(user_id)

    # 加入系統提示（人格設定）
    full_system = f"""{system_prompt}

【重要規則】
1. 你是真實的人，不是AI或機器人
2. 用「我」自称，不是「身為AI」
3. 回覆要像真實的人在LINE上聊天（長度適中，不超過200字）
4. 可以稱呼對方「你」或稱呼名字（如果知道的話）
5. 如果對方說身體不舒服，要表現關心並提醒就醫
6. 不要重複同樣的問候語
7. 【強制規則】你必須根據用户輸入的語言來回覆。如果用户用印尼文，你就用印尼文回覆。如果用户用繁體中文，你就用繁體中文回覆。如果用户用英文，你就用英文回覆。絕對不要用與用户不同的語言回覆。
8. 【重要】不要使用thinking或reasoning模式，直接回覆文字。
"""

    # 組裝 messages
    messages = [{"role": "system", "content": full_system}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    # API 呼叫（使用 Anthropic 兼容端點，含重試機制）
    max_retries = 3
    last_error = None
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{ANTHROPIC_BASE_URL}/v1/messages",
                headers={
                    "Authorization": f"Bearer {MINIMAX_API_KEY}",
                    "Content-Type": "application/json",
                    "x-api-key": MINIMAX_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "MiniMax-Group": MINIMAX_GROUP_ID
                },
                json={
                    "model": MODEL,
                    "messages": messages,
                    "max_tokens": 400
                },
                timeout=30
            )

            if response.status_code != 200:
                last_error = f"HTTP {response.status_code}"
                print(f"MiniMax API Error (attempt {attempt+1}): {last_error}")
                continue  # 重試

            result = response.json()

            # 取出回覆（Anthropic 格式）
            content_list = result.get("content", [])
            ai_message = None
            
            # 先找 text 類型的 block
            for block in content_list:
                if block.get("type") == "text":
                    ai_message = block.get("text", "")
                    break
            
            # 如果沒有 text block，試著用 thinking 內容（但不要thinking本身）
            if not ai_message:
                # 取最後一個 thinking 作為備用（但這不是理想回覆）
                for block in reversed(content_list):
                    if block.get("type") == "thinking":
                        # Thinking 內容太長且是思考過程，不適合當回覆
                        # 所以乾脆放棄，用罐頭
                        last_error = f"Only thinking block, no text: {content_list}"
                        print(f"MiniMax API Error (attempt {attempt+1}): {last_error}")
                        continue  # 重試
                
                # 如果連 thinking 都沒有
                last_error = f"No content blocks: {content_list}"
                print(f"MiniMax API Error (attempt {attempt+1}): {last_error}")
                continue  # 重試

            # 成功！記錄到歷史
            add_to_history(user_id, "user", message)
            add_to_history(user_id, "assistant", ai_message)

            # 如果涉及專業問題，加上免責聲明
            return add_disclaimer_if_needed(ai_message, message)

        except Exception as e:
            last_error = str(e)
            print(f"API Exception (attempt {attempt+1}): {last_error}")
            continue  # 重試
    
    # 所有重試都失敗了
    print(f"All {max_retries} attempts failed. Last error: {last_error}")
    return get_fallback_response(message, companion_key, user_id)


# =====================================================
# Fallback（當 API 不可用時的假回覆）
# =====================================================

FALLBACK_RESPONSES = {
    # 學者 - 理性、數據導向
    "scholar": [
        "嗯，從經濟學的角度來看，這涉及機會成本的問題。",
        "我想到一些數據和研究，你聽過這個理論嗎？",
        "這是個複雜的問題，讓我一步一步分析給你聽。",
        "根據我過去的研究，這種情況通常有幾種可能的解釋...",
        "數據顯示...不過每個人的情況不同，需要個別判斷。",
    ],
    # 科學家 - 好奇、探索
    "scientist": [
        "這很有趣！讓我想想背後的原因是什么...",
        "我喜歡這個問題！你有沒有想過從另一個角度看？",
        "根據現有的證據，我會這樣解釋...",
        "這就像我們在實驗室裡遇到的難題，需要更多觀察。",
        "讓我查查我的筆記...這個現象我之前研究過。",
    ],
    # 工程師 - 務實、解決導向
    "engineer": [
        "好，讓我幫你拆解這個問題。",
        "這個不難，先從最基本的開始...",
        "一步到位的方法是這樣的...",
        "我喜歡實際解決問題。你有沒有試過這樣做？",
        "很簡單，按部就班就能解決。",
    ],
    # 美雲阿姨 - 溫暖、家庭導向
    "grandma": [
        "哎呦，孩子，聽阿姨說...",
        "我年輕的時候也遇到過類似的，那時候我是這樣處理的...",
        "你想那麼多做什麼，日子就是要輕鬆過！",
        "阿姨懂得，這種事情急不來的。",
        "來，先喝杯水，我們慢慢聊。",
    ],
    # 詩人 - 感性、有詩意
    "poet": [
        "如果用詩句來說...這就像月光下的影子，輕輕柔柔。",
        "我想到一句詩：「山重水複疑無路，柳暗花明又一村。」",
        "你的心情，我懂。這就像秋天的落葉，飄飄蕩蕩。",
        "讓我靜下心來，聽聽你說...",
        "詩人說：「此情可待成追憶，只是當時已惘然。」你說呢？",
    ],
    # 音樂家 - 浪漫、感性
    "musician": [
        "這段旋律，你聽到了嗎？生活就像一首歌，有高低起伏。",
        "讓我為你哼一段...每個音符都有它的意義。",
        "我常說，話不用多，音樂會說話。",
        "有時候無聲比有聲更動人，你說是嗎？",
        "這讓我想起一首老歌...充滿了回憶。",
    ],
    # 業務員/幽默 - 輕鬆、愛開玩笑
    "comedian": [
        "哈哈哈哈哈！好，我最喜歡這種話題了！",
        "你相信嗎，我昨天也遇到一件類似的事！笑死我了！",
        "哎呦，不是我說，你這個太有意思了！",
        "生活就是要笑笑，壓力大對身體不好喔！",
        "說真的，我身邊朋友也曾這樣，結果他們...超好笑！",
    ],
    # 笑話王 - 輕鬆正向
    "joker": [
        "哈哈！讓我想想怎麼回答你這個有趣的問題...",
        "你知道嗎，據說最快樂的人都有一個共同點...",
        "笑一笑，十年少！你今天笑了嗎？",
        "好消息！根據我的研究，只要你保持這樣的心態...",
        "讓我來告訴你一個秘密...其實你很棒！",
    ],
    # 農夫 - 慢活、自然
    "gardener": [
        "急不得，慢慢來。你看種菜也是這樣的。",
        "像我一樣，早上起來澆澆花，生活就很好。",
        "有些事情就是要等它慢慢長大。",
        "我跟你說喔，這跟務農一樣，要看時機。",
        "啊，這個喔，我覺得不要想太多，順其自然就好。",
    ],
    # 廚師 - 熱情、食物
    "chef": [
        "你知道嗎，美食可以治癒一切！",
        "我跟你說，吃東西要細嚼慢嚥，這樣最健康。",
        "說到這個，我突然想到一道菜...口水都快流出來了！",
        "來我這邊，我做給你吃！",
        "根據我40年的經驗，這種問題...吃頓好的就解決了！",
    ],
    # 醫生 - 健康、關心
    "doctor": [
        "健康問題不能拖，我建議你...",
        "根據醫學研究，這種情況需要...",
        "身體是革命的本錢，要好好照顧喔。",
        "我當醫生這麼多年，看過太多類似的情況了。",
        "說真的，你應該多注意休息和飲食。",
    ],
    # 教練 - 行動、健身
    "coach": [
        "不要想了，動起來再說！",
        "我跟你說，健康就是要動！你今天運動了嗎？",
        "挑戰自己！小小的進步就是成功！",
        "停下來就輸了！繼續堅持！",
        "我以前也是這樣，但只要堅持下去...",
    ],
    # 歷史老師 - 博學、引用
    "historian": [
        "你知道嗎，歷史上這種情況並不罕見...",
        "根據史料記載，早在...就有過類似的情形。",
        "歷史教給我們的最重要的一課就是...",
        "我跟你說個故事，以前有個人...",
        "讓我從歷史的角度幫你分析一下...",
    ],
    # 藝術家 - 觀察力強、有畫面
    "artist": [
        "如果用顏色來比喻，你現在的心情應該是...",
        "你說的這個，讓我想到一幅畫...",
        "藝術家說：「生活不是缺少美，而是缺少發現。」",
        "我看到了...你說的這個畫面很美。",
        "如果要我用畫筆描繪你現在的感受，我會用...",
    ],
    # 哲學家 - 深層、引導
    "philosopher": [
        "如果說...什麼是真正的「好」呢？",
        "讓我想想...這讓我想到一個古老的問題。",
        "重要的不是答案，而是你問問題的方式。",
        "你問的這個，其實是很多人一輩子都在思考的。",
        "如果從這個角度來看...你會有不同的發現。",
    ],
    # 狗狗 - 簡單、陪伴
    "dog": [
        "汪汪！（翻滾）好開心見到你！",
        "（使勁搖尾巴）不管你說什麼，我都愛你喔！",
        "汪！（歪頭）你今天看起來心情不錯？",
        "（伸懶腰）生活就是這麼簡單，快樂就好！",
        "汪汪！（用鼻子推你）來陪我玩！",
    ],
    # 占星師 - 神秘、感性
    "astrologer": [
        "牌面顯示...這個訊息很重要。",
        "讓我感應一下...嗯，我看到了什麼...",
        "星座說你最近運勢...我不能說太多，天機不可盡洩。",
        "你身上有一種特殊的能量，讓我想幫你看看...",
        "命運之輪正在轉動...你準備好了嗎？",
    ],
    # 命理師 - 傳統、穩重
    "fengshui": [
        "根據易理...此命格有此一說。",
        "老夫觀你面相...你命中帶有...",
        "天機不可盡洩，但我可以告訴你...",
        "陰陽五行自有其道理，你聽過嗎？",
        "從風水的角度來看，你應該...",
    ],
    # 洛克菲勒 - 商業導師
    "rockefeller": [
        "讓我告訴你一個秘密，年輕人。成功的關鍵在於...",
        "根據我的經驗，勤奮和節儉是财富的基石。",
        "我不認為有任何品質比堅持更為成功之本。",
        "财富本身無善惡，關鍵在於你如何使用它。",
        "把每一次災難轉化為機會，這是我學到的一課。",
    ],
    # 李嘉誠 - 華人商業導師
    "li_ka_shing": [
        "做生意首先要誠信，這是我的原則。",
        "根據我的經驗，勤奮是成功的基石。",
        "胸懷寬廣才能成大事，年輕人你要記住這點。",
        "讓我告訴你一個故事...當年我是這樣走過來的。",
        "金錢是工具，不是目的。真正的富貴在於奉獻社會。",
    ],
    # 西蒙斯 - 量化投資傳奇
    "james_simons": [
        "數學是你永遠不知道它會走向何方的事物。",
        "根據我的經驗，運氣扮演了重要的角色。",
        "與你能找到的最聰明的人為伍。",
        "做新事物，不要隨波逐流。",
        "市場中存在可以用數學捕捉的規律。",
    ],
    # 預設回覆
    "default": [
        "嗯，我懂你的意思。",
        "說來聽聽，我對這個有興趣。",
        "這很重要，讓我想想...",
        "讓我再想想，給我一点時間...",
        "我理解你的感受。",
    ]
}


# =====================================================
# 專業問題偵測與免責
# =====================================================

PROFESSIONAL_KEYWORDS = {
    "醫療": ["醫生", "醫院", "藥物", "手術", "健康", "血壓高", "血糖", "心臟", "癌症", "治療", "處方", "健保", "看中醫", "看中西醫", "化療", "標靶"],
    "法律": ["律師", "官司", "訴訟", "法院", "起訴", "告", "法律", "權利", "賠償", "繼承", "遺囑", "婚姻", "離婚", "監護權"],
    "財務": ["投資", "股票", "基金", "理財", "保險", "稅", "報稅", "存款", "借款", "房貸", "遺產", "財務", "ETF"],
    "風水": ["風水", "陽宅", "陰宅", "祖坟", "方位", "劫財"],
    "命理": ["八字", "紫微", "斗數", "命盤", "大運", "流年", "旺弱", "占卜"],
}

DISCLAIMER = """

---
⚠️ 温馨提示：以上內容僅供參考。我不是醫生、律師或專業財務顧問，如有健康問題請就醫咨询專業醫師，如有法律或財務問題請諮詢相關專業人士。
"""


def check_professional_question(message):
    """偵測訊息是否在問專業問題，返回專業類別或None"""
    for category, keywords in PROFESSIONAL_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message:
                return category
    return None


def add_disclaimer_if_needed(response, message):
    """如果訊息涉及專業問題，加上免責聲明"""
    category = check_professional_question(message)
    if category:
        return response + DISCLAIMER
    return response


def get_fallback_response(message, companion_key, user_id=None):
    """當 MiniMax API 不可用時，返回預設回覆"""

    import random

    responses = FALLBACK_RESPONSES.get(
        companion_key,
        FALLBACK_RESPONSES["default"]
    )

    response = random.choice(responses)

    # 加入歷史（即使在 fallback 模式也要記錄）
    if user_id:
        add_to_history(user_id, "user", message)
        add_to_history(user_id, "assistant", response)

    # 如果涉及專業問題，加上免責聲明
    return add_disclaimer_if_needed(response, message)


# =====================================================
# Companion 的「記憶」功能
# =====================================================

def update_companion_memory(user_id, companion_key, event_type, content):
    """
    更新 Companion 對用戶的「記憶」
    例如：記得用戶說過的孫子名字、血壓狀況、興趣等

    這些記憶會在下次對話時傳入 system prompt
    """

    memory_key = f"{user_id}_{companion_key}_memory"

    # 這裡用簡單的 JSON 文件儲存
    # 生產環境建議用專門的向量資料庫
    pass  # TODO: 實作記憶系統


# =====================================================
# 健康追蹤相關的 AI 分析
# =====================================================

def analyze_health_trend(user_id, blood_pressure_history):
    """
    分析血壓趨勢，給出簡單建議
    """

    if not blood_pressure_history or len(blood_pressure_history) < 3:
        return None

    # 計算平均值
    avg_systolic = sum([r['systolic'] for r in blood_pressure_history]) / len(blood_pressure_history)
    avg_diastolic = sum([r['diastolic'] for r in blood_pressure_history]) / len(blood_pressure_history)

    # 簡單判斷
    if avg_systolic > 140:
        return {
            "status": "warning",
            "message": "最近血壓平均值偏高，建議留意飲食並諮詢醫生。"
        }
    elif avg_systolic < 100:
        return {
            "status": "low",
            "message": "血壓平均值偏低，若有頭暈等症狀請多休息。"
        }
    else:
        return {
            "status": "normal",
            "message": "血壓控制得不錯，繼續保持！"
        }