"""
ElderCare 資料庫模組 - Firebase Firestore 持久化
"""

import base64
import json
import os
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

# =====================================================
# Firebase 初始化
# =====================================================

def _init_firebase():
    """初始化 Firebase Admin SDK"""
    # 先嘗試從 Railway 環境變數讀取（base64 encoded JSON）
    cred_b64 = os.environ.get('FIREBASE_CREDENTIALS')
    if cred_b64:
        try:
            cred_content = base64.b64decode(cred_b64).decode('utf-8')
            cred_dict = json.loads(cred_content)
            cred = credentials.Certificate(cred_dict)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            return
        except Exception as e:
            print(f"Failed to parse FIREBASE_CREDENTIALS env var: {e}")
    
    # 否則從本地檔案讀取
    cred_path = os.path.join(os.path.dirname(__file__), "firebase-admin.json")
    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Firebase credentials not found: {cred_path}")
    
    cred = credentials.Certificate(cred_path)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

_db_client = None

def get_db():
    """取得 Firestore 客戶端（單例）"""
    global _db_client
    if _db_client is None:
        _init_firebase()
        _db_client = firestore.client()
    return _db_client

# =====================================================
# 用戶資料操作
# =====================================================

def _get_user_ref(user_id):
    """取得用戶文檔引用"""
    db = get_db()
    return db.collection("users").document(str(user_id))


def _get_user(user_id):
    """取得用戶資料"""
    doc = _get_user_ref(user_id).get()
    if doc.exists:
        return doc.to_dict()
    return None


def _get_or_create_user(user_id):
    """取得或建立用戶資料"""
    user = _get_user(user_id)
    if user is None:
        user = {
            "companion_key": None,
            "family": [],
            "created_at": datetime.now().isoformat(),
            "subscription": "free",
            "check_ins": {},
            "blood_pressure": [],
            "medications": [],
            "messages": []
        }
        _get_user_ref(user_id).set(user)
    return user


# =====================================================
# Companion 設定
# =====================================================

def get_user_companion(user_id):
    """取得用戶的 Companion"""
    user = _get_or_create_user(user_id)
    return user.get("companion_key")


def set_user_companion(user_id, companion_key):
    """設定用戶的 Companion"""
    _get_user_ref(user_id).update({"companion_key": companion_key})
    return True


# =====================================================
# 家人管理
# =====================================================

def get_family_members(user_id):
    """取得用戶的所有家人 LINE ID"""
    user = _get_or_create_user(user_id)
    return user.get("family", [])


def add_family_member(user_id, family_line_id):
    """加入家人"""
    user = _get_or_create_user(user_id)
    family = user.get("family", [])
    if family_line_id not in family:
        family.append(family_line_id)
        _get_user_ref(user_id).update({"family": family})
    return True


def remove_family_member(user_id, family_line_id):
    """移除家人"""
    user = _get_or_create_user(user_id)
    family = user.get("family", [])
    if family_line_id in family:
        family.remove(family_line_id)
        _get_user_ref(user_id).update({"family": family})
    return True


# =====================================================
# 所有用戶
# =====================================================

def get_all_user_ids():
    """取得所有已註冊的用戶ID列表"""
    db = get_db()
    users = db.collection("users").get()
    return [doc.id for doc in users]


# =====================================================
# 健康資料
# =====================================================

def daily_check_in(user_id):
    """每日打卡"""
    date_key = datetime.now().strftime('%Y-%m-%d')
    add_check_in(user_id, date_key, "completed")


def record_message(user_id, user_message, ai_response, companion_key=None):
    """記錄對話（舊接口，向下相容）"""
    add_message(user_id, "user", user_message)
    add_message(user_id, "assistant", ai_response)


def record_blood_pressure(user_id, systolic, diastolic):
    """記錄血壓（舊接口，向下相容）"""
    add_blood_pressure(user_id, systolic, diastolic)


def add_check_in(user_id, date_key, response):
    """新增每日打卡"""
    user = _get_or_create_user(user_id)
    check_ins = user.get("check_ins", {})
    check_ins[date_key] = {
        "response": response,
        "timestamp": datetime.now().isoformat()
    }
    _get_user_ref(user_id).update({"check_ins": check_ins})


def get_check_in(user_id, date_key):
    """取得打卡記錄"""
    user = _get_or_create_user(user_id)
    check_ins = user.get("check_ins", {})
    return check_ins.get(date_key)


def add_blood_pressure(user_id, systolic, diastolic):
    """新增血壓記錄"""
    user = _get_or_create_user(user_id)
    bp = user.get("blood_pressure", [])
    bp.append({
        "systolic": systolic,
        "diastolic": diastolic,
        "timestamp": datetime.now().isoformat()
    })
    _get_user_ref(user_id).update({"blood_pressure": bp})


def get_blood_pressure_history(user_id, limit=10):
    """取得血壓歷史"""
    user = _get_or_create_user(user_id)
    bp = user.get("blood_pressure", [])
    return bp[-limit:]


# =====================================================
# 用藥提醒
# =====================================================

def set_medications(user_id, medications):
    """設定用藥清單"""
    _get_user_ref(user_id).update({"medications": medications})


def get_medications(user_id):
    """取得用藥清單"""
    user = _get_or_create_user(user_id)
    return user.get("medications", [])


# =====================================================
# 訊息歷史
# =====================================================

def add_message(user_id, role, content):
    """新增訊息到歷史"""
    user = _get_or_create_user(user_id)
    messages = user.get("messages", [])
    messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    # 保留最近 50 條訊息
    if len(messages) > 50:
        messages = messages[-50:]
    _get_user_ref(user_id).update({"messages": messages})


def get_messages(user_id, limit=20):
    """取得最近訊息"""
    user = _get_or_create_user(user_id)
    messages = user.get("messages", [])
    return messages[-limit:]


def clear_messages(user_id):
    """清除訊息歷史"""
    _get_user_ref(user_id).update({"messages": []})


# =====================================================
# 訂閱狀態
# =====================================================

def get_subscription(user_id):
    """取得訂閱狀態"""
    user = _get_or_create_user(user_id)
    return user.get("subscription", "free")


def set_subscription(user_id, plan):
    """設定訂閱狀態"""
    _get_user_ref(user_id).update({"subscription": plan})