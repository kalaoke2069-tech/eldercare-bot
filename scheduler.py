"""
ElderCare Companion — 每日排程服務
負責：
1. 每日主動問候（LINE 推播）
2. 用藥提醒
3. 血壓記錄提醒
4. 未打卡警示
"""

import os
import time
from datetime import datetime, timedelta
from threading import Thread
import random

from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage

from database import (
    get_check_in_history, get_blood_pressure_history,
    get_medications, get_user_companion, get_subscription
)
from companions import COMPANION_PRESETS, get_companion

line_bot_api = LineBotApi(os.getenv('LINE_ACCESS_TOKEN'))

# =====================================================
# 每日主動問候（Companion 風格）
# =====================================================

def daily_greeting(user_id):
    """發送每日問候"""

    companion_key = get_user_companion(user_id)
    subscription = get_subscription(user_id)

    if not companion_key:
        # 還沒選擇 Companion
        message = "早安！今天過得怎麼樣？記得每天打卡哦！"
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
        return

    companion = get_companion(companion_key)
    if not companion:
        return

    # 根據不同時間發不同問候
    now = datetime.now()
    hour = now.hour

    if hour < 10:
        greeting_type = "morning"
    elif hour < 14:
        greeting_type = "afternoon"
    elif hour < 18:
        greeting_type = "evening"
    else:
        greeting_type = "night"

    # Companion 風格的問候
    greetings = [
        f"早安！今天天氣不錯，起床了嗎？ [{companion['name']}]",
        f"哎，今天怎麼樣？有沒有吃早餐？ [{companion['name']}]",
        f"嘿！想你了，今天過得好不好？ [{companion['name']}]",
    ]

    # Free 用戶少一點推播
    if subscription == "free":
        # 只發早安
        if greeting_type == "morning":
            message = random.choice(greetings[:1])
        else:
            return

    else:
        message = random.choice(greetings)

    line_bot_api.push_message(user_id, TextSendMessage(text=message))


# =====================================================
# 用藥提醒
# =====================================================

def medication_reminder(user_id):
    """發送用藥提醒"""

    medications = get_medications(user_id)

    if not medications:
        return  # 沒有設定用藥

    now = datetime.now()
    current_time = now.strftime("%H:%M")

    for med in medications:
        times = med.get("times", [])
        if current_time in times:
            # 到了用藥時間
            message = f"""
💊 【用藥提醒】

該吃「{med['name']}」了！

時間：{current_time}
            """

            line_bot_api.push_message(user_id, TextSendMessage(text=message))


def medication_reminder_check():
    """檢查所有用戶的用藥提醒（每分鐘執行）"""

    from database import _db

    for user_id in _db["users"]:
        medication_reminder(user_id)


# =====================================================
# 未打卡警示
# =====================================================

def check_missing_checkin():
    """檢查今天還沒打卡的用戶"""

    from database import _db

    today = datetime.now().strftime("%Y-%m-%d")

    for user_id in _db["users"]:
        user = _db["users"][user_id]
        check_ins = user.get("check_ins", {})

        # 今天還沒打卡
        if today not in check_ins:
            companion_key = user.get("companion_key")
            companion = get_companion(companion_key) if companion_key else None

            if companion:
                companion_name = companion['name']
            else:
                companion_name = "小幫手"

            # 發送提醒
            message = f"""
[{companion_name}]

嗨！今天還沒看到你打卡哦！

身體還好嗎？記得回來讓我知道你沒事 🙏
            """

            try:
                line_bot_api.push_message(user_id, TextSendMessage(text=message))
            except Exception as e:
                print(f"無法發送打卡提醒給 {user_id}: {e}")


# =====================================================
# 每週健康報告
# =====================================================

def weekly_health_report(user_id):
    """發送每週健康報告"""

    # 取得這週的資料
    bp_history = get_blood_pressure_history(user_id, days=7)
    check_ins = get_check_in_history(user_id, days=7)

    if not bp_history and not check_ins:
        return  # 沒有資料

    # 計算血壓平均
    if bp_history:
        avg_sys = sum([r['systolic'] for r in bp_history]) / len(bp_history)
        avg_dia = sum([r['diastolic'] for r in bp_history]) / len(bp_history)
        bp_text = f"""
📊 血壓平均：
收縮壓 {avg_sys:.0f} mmHg
舒張壓 {avg_dia:.0f} mmHg
（{len(bp_history)}筆記錄）
"""
    else:
        bp_text = "本週還沒有血壓記錄 📝"

    # 打卡統計
    check_in_count = len(check_ins)
    check_in_text = f"""
✅ 打卡記錄：{check_in_count}/7 天
"""

    report = f"""
🌟 【每週健康報告】

{bp_text}
{check_in_text}

記得每天都要打卡哦！
    """

    line_bot_api.push_message(user_id, TextSendMessage(text=report))


# =====================================================
# 排程執行器（简易版）
# =====================================================

def run_scheduler():
    """
    啟動排程服務

    生產環境建議使用：
    - APScheduler (Python)
    - 或者 Linux crontab
    - 或者 LINE Bot 的预设消息功能
    """

    print("排程服務啟動中...")

    last_reminder_check = None
    last_missing_check = None
    last_greeting = None

    while True:
        now = datetime.now()

        # 每分鐘：檢查用藥提醒
        if now.minute != (last_reminder_check or -1):
            last_reminder_check = now.minute
            medication_reminder_check()

        # 每小時：檢查未打卡
        if now.hour != (last_missing_check or -1) and now.hour == 10:
            last_missing_check = now.hour
            check_missing_checkin()

        # 每天早上8點：發送問候
        if now.hour == 8 and now.minute == 0:
            if last_greeting != now.date():
                last_greeting = now.date()
                from database import _db
                for user_id in _db["users"]:
                    try:
                        daily_greeting(user_id)
                    except Exception as e:
                        print(f"無法發送問候給 {user_id}: {e}")

        # 等待1分鐘
        time.sleep(60)


# =====================================================
# 快速測試工具
# =====================================================

if __name__ == "__main__":
    print("測試排程功能...")

    # 測試發送
    test_user_id = "TEST_USER_ID"

    print("\n1. 測試每日問候")
    daily_greeting(test_user_id)

    print("\n2. 測試未打卡檢查")
    check_missing_checkin()

    print("\n3. 測試每週報告")
    weekly_health_report(test_user_id)

    print("\n完成！")