"""
ElderCare Companion — 資料庫管理
使用 Firebase Firestore 儲存所有用戶資料
"""

import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

# =====================================================
# 簡單的 In-Memory 資料庫（測試用）
# 生產環境請使用 Firebase Firestore
# =====================================================

# 結構：
# {
#   "users": {
#       "LINE_USER_ID": {
#           "companion_key": "scholar",
#           "family": ["LINE_ID_1", "LINE_ID_2"],
#           "created_at": "2026-04-14",
#           "subscription": "basic",  # free / basic / premium
#           "check_ins": {
#               "2026-04-14": "09:30",
#               ...
#           },
#           "blood_pressure": [
#               {"date": "2026-04-14", "time": "09:30", "systolic": 125, "diastolic": 80},
#               ...
#           ],
#           "medications": [
#               {"name": "高血壓藥", "times": ["08:00", "20:00"]},
#               ...
#           ]
#       }
#   }
# }

_db = defaultdict(lambda: defaultdict(dict))


def _get_user(user_id):
    """取得或建立用戶資料"""
    if user_id not in _db["users"]:
        _db["users"][user_id] = {
            "companion_key": None,
            "family": [],
            "created_at": datetime.now().isoformat(),
            "subscription": "free",
            "check_ins": {},
            "blood_pressure": [],
            "medications": [],
            "messages": []
        }
    return _db["users"][user_id]


# =====================================================
# Companion 設定
# =====================================================

def get_user_companion(user_id):
    """取得用戶的 Companion"""
    user = _get_user(user_id)
    return user.get("companion_key")


def set_user_companion(user_id, companion_key):
    """設定用戶的 Companion"""
    user = _get_user(user_id)
    user["companion_key"] = companion_key
    return True


# =====================================================
# 家人管理
# =====================================================

def get_family_members(user_id):
    """取得用戶的所有家人 LINE ID"""
    user = _get_user(user_id)
    return user.get("family", [])


def add_family_member(user_id, family_line_id):
    """加入家人"""
    user = _get_user(user_id)
    if "family" not in user:
        user["family"] = []
    if family_line_id not in user["family"]:
        user["family"].append(family_line_id)
    return True


def remove_family_member(user_id, family_line_id):
    """移除家人"""
    user = _get_user(user_id)
    if family_line_id in user.get("family", []):
        user["family"].remove(family_line_id)
    return True


def get_all_user_ids():
    """取得所有已註冊的用戶ID列表"""
    return list(_db["users"].keys())


# =====================================================
# 每日打卡
# =====================================================

def daily_check_in(user_id):
    """每日打卡"""
    user = _get_user(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")

    if "check_ins" not in user:
        user["check_ins"] = {}

    user["check_ins"][today] = now

    return {"date": today, "time": now}


def get_check_in_history(user_id, days=30):
    """取得打卡歷史"""
    user = _get_user(user_id)
    history = user.get("check_ins", {})

    # 過濾最近的天數
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    return {k: v for k, v in history.items() if k >= cutoff}


# =====================================================
# 血壓記錄
# =====================================================

def record_blood_pressure(user_id, systolic, diastolic):
    """記錄血壓"""
    user = _get_user(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")

    if "blood_pressure" not in user:
        user["blood_pressure"] = []

    record = {
        "date": today,
        "time": now,
        "systolic": systolic,
        "diastolic": diastolic
    }

    user["blood_pressure"].append(record)

    # 保持最近90筆記錄
    if len(user["blood_pressure"]) > 90:
        user["blood_pressure"] = user["blood_pressure"][-90:]

    return record


def get_blood_pressure_history(user_id, days=30):
    """取得血壓歷史"""
    user = _get_user(user_id)
    records = user.get("blood_pressure", [])

    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    return [r for r in records if r["date"] >= cutoff]


# =====================================================
# 用藥記錄
# =====================================================

def add_medication(user_id, name, times):
    """新增用藥"""
    user = _get_user(user_id)
    if "medications" not in user:
        user["medications"] = []

    medication = {
        "name": name,
        "times": times,
        "added_at": datetime.now().isoformat()
    }

    user["medications"].append(medication)
    return medication


def get_medications(user_id):
    """取得所有用藥"""
    user = _get_user(user_id)
    return user.get("medications", [])


# =====================================================
# 對話記錄
# =====================================================

def record_message(user_id, user_message, ai_response, companion_key):
    """記錄對話"""
    user = _get_user(user_id)
    if "messages" not in user:
        user["messages"] = []

    record = {
        "timestamp": datetime.now().isoformat(),
        "user": user_message,
        "ai": ai_response,
        "companion": companion_key
    }

    user["messages"].append(record)

    # 保持最近500筆
    if len(user["messages"]) > 500:
        user["messages"] = user["messages"][-500:]

    return record


def get_message_history(user_id, limit=50):
    """取得對話歷史"""
    user = _get_user(user_id)
    messages = user.get("messages", [])
    return messages[-limit:]


# =====================================================
# 訂閱管理
# =====================================================

def get_subscription(user_id):
    """取得訂閱狀態"""
    user = _get_user(user_id)
    return user.get("subscription", "free")


def set_subscription(user_id, plan):
    """設定訂閱方案 (free/basic/premium)"""
    user = _get_user(user_id)
    user["subscription"] = plan
    return True


# =====================================================
# 匯出（除錯用）
# =====================================================

def export_all_data():
    """匯出所有資料（JSON）"""
    return dict(_db)


def import_data(data):
    """匯入資料"""
    global _db
    _db = defaultdict(lambda: defaultdict(dict), data)