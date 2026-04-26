"""
ElderCare 隨機提醒排程器
每天 9:00 AM - 9:00 PM 隨機發送 2-3 次 AI 生成的關心訊息
"""

import os
import random
from datetime import datetime, time
from threading import Thread

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from linebot import LineBotApi
from linebot.models import TextSendMessage

from database import get_all_user_ids, get_user_companion, get_subscription
from companions import COMPANION_PRESETS, get_companion

# LINE Bot API
line_bot_api = LineBotApi(os.getenv('LINE_ACCESS_TOKEN'))

# =====================================================
# 隨機訊息庫（可擴展）
# =====================================================

RANDOM_MESSAGES = [
    # 健康關心
    "💊 提醒：今天吃了幾次藥？按時服藥很重要哦！",
    "🚶 天氣不錯，有機會出去走走動一動吧！",
    "💧 今天喝夠水了嗎？記得補充水分哦！",
    "😴 昨晚睡得好嗎？睡眠品質也很重要呢。",

    # Companion 提醒
    "🌟 你的 Companion 還記得你哦！想聊聊嗎？",
    "👋 今天還沒跟你的 Companion 打招呼呢，隨時歡迎回來聊聊！",
    "💬 有什麼心事想聊聊嗎？你的 Companion 在等你。",

    # 健康知識
    "📚 每日健康：多吃蔬菜水果，保持營養均衡！",
    "🧘 深呼吸幾次，讓自己放鬆一下身心。",
    "🏃 適度運動有助于保持健康，試著每天動一动哦！",

    # 簡單問候
    "☀️ 早安！今天過得怎麼樣？",
    "🌙 今天辛苦了，好好休息哦！",
    "🌸 希望你今天有愉快的事發生！",
    "😊 今天也要保持好心情哦！",

    # 用藥提醒
    "💊 吃藥時間到了嗎？記得按時服藥哦！",
    "🩺 如果有任何不舒服，請及時告訴家人或就醫。",
]

# 發送時段（9:00 - 21:00）
WINDOW_START = 9   # 早上 9 點
WINDOW_END = 21     # 晚上 9 點

# 每天發送次數
MESSAGES_PER_DAY = 3


def get_random_message(companion_key=None):
    """取得隨機訊息，可根據 Companion 調整语气"""
    msg = random.choice(RANDOM_MESSAGES)
    return msg


def should_send_now():
    """檢查現在是否在允許的發送時段內"""
    now_hour = datetime.now().hour
    return WINDOW_START <= now_hour < WINDOW_END


def pick_random_send_time():
    """在允許時段內隨機挑一個時間點"""
    # 從允許時段中隨機選一個小時
    hour = random.randint(WINDOW_START, WINDOW_END - 1)
    # 選一個分鐘
    minute = random.randint(0, 59)
    return hour, minute


def send_random_checkin():
    """發送隨機關心訊息給所有用戶"""
    if not should_send_now():
        print(f"[{datetime.now()}] Outside send window, skipping...")
        return

    try:
        user_ids = get_all_user_ids()
        if not user_ids:
            print(f"[{datetime.now()}] No users to send to")
            return

        for user_id in user_ids:
            try:
                companion_key = get_user_companion(user_id)
                companion = get_companion(companion_key) if companion_key else None

                if companion:
                    # 有 Companion → 發送一般關心訊息
                    msg = get_random_message(companion_key)
                    companion_name = companion.get('name', '')
                    full_msg = f"{companion_name}提醒你：{msg}"
                else:
                    # 還沒選 Companion → 發送選好友提醒
                    companion_options = [
                        "1️⃣ 老陳(學者) - 愛聊經濟股票",
                        "2️⃣ 美雲阿姨(長輩) - 溫暖關心人",
                        "3️⃣ 阿Ken(業務員) - 幽默風趣",
                        "4️⃣ 阿美姐(廚師) - 愛聊食譜",
                        "5️⃣ 韻璇(占星師) - 星座塔羅",
                        "6️⃣ 雲峰大師(命理師) - 易經八字",
                    ]
                    options_text = "\n".join(companion_options)
                    full_msg = f"""🌟 嗨！你還沒選擇你的 AI 陪伴好友哦！

在開始聊天之前，告訴我你喜歡什麼類型的朋友？

{options_text}

請輸入數字 1-6 選擇！

（也可以直接傳訊息跟機器人聊天，會引導你選擇）"""

                line_bot_api.push_message(user_id, TextSendMessage(text=full_msg))
                status = companion.get('name', 'No Companion') if companion else 'No Companion'
                print(f"[{datetime.now()}] Sent to {user_id} [{status}]: {msg[:30] if companion else 'companion selection'}")

            except Exception as e:
                print(f"Failed to send to {user_id}: {e}")

        print(f"[{datetime.now()}] Random check-in sent to {len(user_ids)} users")

    except Exception as e:
        print(f"Scheduler error: {e}")


def setup_scheduler(app):
    """設定 APScheduler 背景任務"""
    scheduler = BackgroundScheduler()

    # 每天設定 3 個隨機時間點發送
    for i in range(MESSAGES_PER_DAY):
        hour, minute = pick_random_send_time()
        # 每天執行
        scheduler.add_job(
            send_random_checkin,
            CronTrigger(hour=hour, minute=minute),
            id=f'random_checkin_{i}',
            replace_existing=True,
            misfire_grace_time=3600  # 錯過了1小時內還補發
        )
        print(f"Scheduled random check-in #{i+1} at {hour:02d}:{minute:02d}")

    # 另一種方式：每2-3小時發送一次（更簡單）
    # for i in range(MESSAGES_PER_DAY):
    #     interval_hours = (WINDOW_END - WINDOW_START) // MESSAGES_PER_DAY
    #     hour_offset = i * interval_hours + random.randint(0, interval_hours - 1)
    #     actual_hour = WINDOW_START + hour_offset
    #     scheduler.add_job(
    #         send_random_checkin,
    #         CronTrigger(hour=actual_hour, minute=random.randint(0, 59)),
    #         id=f'random_checkin_{i}',
    #         replace_existing=True
    #     )

    scheduler.start()
    print("✅ APScheduler started for random check-ins")
    return scheduler