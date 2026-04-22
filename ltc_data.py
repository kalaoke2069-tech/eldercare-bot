"""
ElderCare Companion — 長照資源資料
台灣長期照顧服務資訊（政府與NGO）
"""

# =====================================================
# 政府長照資源
# =====================================================

GOVERNMENT_LTC = {
    "衛福部長照專區": {
        "type": "政府",
        "phone": "1966",
        "website": "https://www.mohw.gov.tw/mp-2.html",
        "description": "衛福部長期照顧服務專區，提供最新長照政策、補助資訊、服務項目說明",
        "services": ["長照2.0服務項目", "補助申請", "照顧管理", "喘息服務", "居家服務", "機構服務"],
        "regions": "全國"
    },
    "1966長照專線": {
        "type": "政府",
        "phone": "1966",
        "website": "https://www.nhi.gov.tw/Content/List.aspx?nodeid=1137",
        "description": "週一至週五 08:30-12:00 / 13:30-17:30，另有行動電話另付通話費用",
        "services": ["長照服務申請", "資源查詢", "補助資格諮詢"],
        "regions": "全國"
    },
    "各縣市照顧管理中心": {
        "type": "政府",
        "description": "各縣市均設有照顧管理中心，負責個案管理、服務連結",
        "regions": "全國",
        "data": {
            "台北市": {"phone": "02-2759-3000", "website": "https://carewalker.gov.taipei/"},
            "新北市": {"phone": "02-2968-3333", "website": "https://www.ntpc.gov.tw/"},
            "桃園市": {"phone": "03-332-1321", "website": "https://www.tycg.gov.tw/"},
            "台中市": {"phone": "04-2515-5888", "website": "https://www.taichung.gov.tw/"},
            "台南市": {"phone": "06-293-1111", "website": "https://www.tainan.gov.tw/"},
            "高雄市": {"phone": "07-337-3370", "website": "https://www.kcg.gov.tw/"},
            "新竹縣": {"phone": "03-551-8101", "website": "https://www.hsinchu.gov.tw/"},
            "彰化縣": {"phone": "04-726-1111", "website": "https://www.chcg.gov.tw/"},
            "屏東縣": {"phone": "08-732-0415", "website": "https://www.pthg.gov.tw/"},
            "花蓮縣": {"phone": "03-822-5171", "website": "https://www.hl.gov.tw/"},
            "台東縣": {"phone": "089-326-141", "website": "https://www.taitung.gov.tw/"},
        }
    },
    "喘息服務": {
        "type": "政府",
        "description": "提供家庭照顧者暫時休息的服務，減輕照顧壓力",
        "services": ["居家喘息", "機構喘息", "日照中心喘息", "小規模多機能喘息"],
        "eligible": "長期照顧給付對象，經照管中心評估失能等级達2-8級者",
        "subsidy": "依失能等级補助每年最高14-21天"
    },
    "居家服務": {
        "type": "政府",
        "description": "照顧服務員到宅協助日常生活活動",
        "services": ["身體照顧", "日常生活照顧", "家務協助", "餐食照顧"],
        "eligible": "65歲以上老人、55歲以上山地原住民、50歲以上身心障礙者",
        "regions": "全國"
    },
    "長照2.0社區整合照顧服務": {
        "type": "政府",
        "description": "整合醫療與長照資源，在社區提供連續性照護",
        "services": ["社區整體照顧服務中心（A、B、C級）", "巷弄長照站", "失智症社區服務"],
        "regions": "全國"
    },
    "出院準備服務": {
        "type": "政府",
        "description": "醫院協助病患及家屬規劃出院後的長照需求，無縫接軌長照服務",
        "services": ["銜接長照資源", "照顧計畫建議", "返家準備"],
        "eligible": "住院病患經評估有長照需求者",
        "regions": "全國"
    },
    "輔具及居家無障礙改善": {
        "type": "政府",
        "description": "補助購買輔具及居家環境改善",
        "services": ["輔具補助", "居家無障礙環境改善", "喘息服務"],
        "eligible": "65歲以上老人、身心障礙者",
        "subsidy": "每10年最高補助10萬元"
    },
}

# =====================================================
# NGO 長照服務單位
# =====================================================

NGO_LTC = {
    "伊甸基金會": {
        "type": "NGO",
        "phone": "02-2577-5689",
        "website": "https://www.eden.org.tw/",
        "description": "基督教伊甸社會福利基金會，提供身障、老人、弱勢家庭服務",
        "services": ["居家照顧", "日照中心", "失智症照顧", "社區照顧", "身障就業服務", "長照2.0服務"],
        "regions": "全國（20縣市服務）",
        "features": ["30年長照經驗", "專業照服員培訓", "個案管理服務"]
    },
    "弘道老人福利基金會": {
        "type": "NGO",
        "phone": "04-2418-0122",
        "website": "https://www.hondao.org.tw/",
        "description": "弘道老人福利基金會，專注老人照顧與活躍老化",
        "services": ["居家服務", "日照中心", "社區關懷", "老人福利倡導", "不老青春服務"],
        "regions": "全國",
        "features": ["不老服務理念", "社區志工網絡", "預防延緩失能"]
    },
    "華山基金會": {
        "type": "NGO",
        "phone": "03-335-3399",
        "website": "https://www.elder.org.tw/",
        "description": "創世社會福利基金會附設華山基金會，專注獨居老人服務",
        "services": ["免費到宅服務", "關懷訪視", "物資協助", "年節關懷"],
        "regions": "全國",
        "features": ["免費服務弱勢長者", "愛心物資配送", "志工到宅陪伴"]
    },
    "仁寶基金會": {
        "type": "NGO",
        "phone": "02-2707-0789",
        "website": "https://www.rbcharity.org.tw/",
        "description": "仁寶電腦旗下基金會，專注科技助老與社會公益",
        "services": ["科技老化服務", "數位落差培訓", "長者科技教育", "銀髮族關懷"],
        "regions": "全台服務",
        "features": ["科技結合長照", "數位學習課程", "智慧照顧解決方案"]
    },
    "聖母基金會": {
        "type": "NGO",
        "phone": "02-2771-5770",
        "website": "https://www.maryknoll.org.tw/",
        "description": "瑪利諾會附設基金會，專注老人與弱勢服務",
        "services": ["安養照護", "日間照顧", "居家服務", "社區關懷"],
        "regions": "全台服務",
        "features": ["天主教服務精神", "專業護理團隊", "靈性關懷"]
    },
    "陽光基金會": {
        "type": "NGO",
        "phone": "02-2507-8006",
        "website": "https://www.sunshine.org.tw/",
        "description": "陽光社會福利基金會，專注顏損及口腔癌照顧服務",
        "services": ["顏損者服務", "口腔癌照顧", "心理重建", "就業支持"],
        "regions": "全國",
        "features": ["30年服務經驗", "專業復健團隊", "家庭支持服務"]
    },
    "肢體障礙協會": {
        "type": "NGO",
        "phone": "02-2559-3210",
        "website": "https://www.mda.org.tw/",
        "description": "中華民國肌肉萎縮症病友協會",
        "services": ["病友照護", "醫療資訊", "輔具補助", "心理支持"],
        "regions": "全國",
        "features": ["罕見疾病服務", "全人關懷", "家屬支持團體"]
    },
    "智障者家長協會": {
        "type": "NGO",
        "phone": "02-2702-6233",
        "website": "https://www.ppct.org.tw/",
        "description": "中華民國智障者家長協會，專注心智障礙者照顧與權益",
        "services": ["照護諮詢", "家屬支持", "機構服務", "權益倡導"],
        "regions": "全國",
        "features": ["家長網絡", "專業培訓", "政策倡議"]
    },
    "失智症協會": {
        "type": "NGO",
        "phone": "02-2599-2809",
        "website": "https://www.tada2002.org.tw/",
        "description": "台灣失智症協會，專注失智症防治與照顧",
        "services": ["失智症諮詢", "家屬支持", "認識課程", "照顧訓練", "記憶篩檢"],
        "regions": "全國",
        "features": ["專業衛教", "家屬工作坊", "早期介入服務"]
    },
    "老化議題協會": {
        "type": "NGO",
        "phone": "02-2511-0528",
        "website": "https://www.taga.org.tw/",
        "description": "台灣銀髮族協會，專注老人福利與活躍老化",
        "services": ["老人福利倡導", "教育培訓", "休閒活動", "國際交流"],
        "regions": "全國",
        "features": ["銀髮族發聲平台", "預防延緩失能", "社會參與促進"]
    },
}

# =====================================================
# 實用查詢關鍵字對照
# =====================================================

SEARCH_KEYWORDS = {
    "關鍵字": {
        "政府": ["政府", "公家", "長照中心", "照管中心", "1966", "補助", "申請"],
        "ngo": ["基金會", "協會", "伊甸", "弘道", "華山", "仁寶", "陽光", "失智症", "老人"],
        "服務類型": ["居家", "日照", "喘息", "機構", "接送", "輔具", "無障礙", "復健"],
        "特殊需求": ["失智", "身障", "癌癥", "中風", "糖尿病", "洗腎", "精神"],
        "地區": ["台北", "新北", "桃園", "台中", "台南", "高雄", "花蓮", "台東", "基隆", "新竹", "嘉義", "彰化", "屏東"]
    }
}

# =====================================================
# 查詢函數
# =====================================================

def search_ltc(query, region=None, service_type=None):
    """
    搜尋長照資源
    
    Args:
        query: 搜尋關鍵字（字串）
        region: 地區（可選，繁體中文）
        service_type: 服務類型（可選）
    
    Returns:
        list: 符合條件的長照資源列表
    """
    results = []
    query_lower = query.lower()
    
    # 合併搜尋所有資源
    all_resources = {}
    for name, data in GOVERNMENT_LTC.items():
        all_resources[name] = data
    for name, data in NGO_LTC.items():
        all_resources[name] = data
    
    for name, data in all_resources.items():
        # 檢查名稱
        if query_lower in name.lower():
            results.append({"name": name, "data": data, "match": "名稱"})
            continue
        
        # 檢查描述
        desc = data.get("description", "").lower()
        if query_lower in desc:
            results.append({"name": name, "data": data, "match": "描述"})
            continue
        
        # 檢查服務
        services = data.get("services", [])
        for service in services:
            if query_lower in service.lower():
                results.append({"name": name, "data": data, "match": f"服務：{service}"})
                break
    
    # 如果指定了地區，過濾結果
    if region:
        filtered = []
        for r in results:
            regions = r["data"].get("regions", "")
            if region in regions or "全國" in regions:
                filtered.append(r)
        results = filtered if filtered else results
    
    return results


def format_ltc_result(result):
    """格式化單一查詢結果為LINE訊息"""
    name = result["name"]
    data = result["data"]
    org_type = data.get("type", "")
    phone = data.get("phone", "無")
    website = data.get("website", "無")
    desc = data.get("description", "")
    services = data.get("services", [])
    regions = data.get("regions", "")
    
    msg = f"【{name}】\n"
    msg += f"類型：{org_type}\n"
    if phone != "無":
        msg += f"電話：{phone}\n"
    msg += f"地區：{regions}\n"
    msg += f"\n{desc}\n"
    
    if services:
        msg += f"\n服務項目：\n"
        for s in services[:5]:
            msg += f"• {s}\n"
    
    if website != "無":
        msg += f"\n網站：{website}"
    
    return msg


def get_all_resources_summary():
    """取得所有資源的摘要"""
    msg = "🏥 台灣長照資源總覽\n\n"
    msg += "【政府資源】\n"
    for name, data in GOVERNMENT_LTC.items():
        phone = data.get("phone", "")
        msg += f"• {name}"
        if phone:
            msg += f" ({phone})"
        msg += "\n"
    
    msg += "\n【NGO組織】\n"
    for name, data in NGO_LTC.items():
        phone = data.get("phone", "")
        msg += f"• {name}"
        if phone:
            msg += f" ({phone})"
        msg += "\n"
    
    msg += "\n💡 輸入「長照+關鍵字」查詢，例如：\n"
    msg += "「長照 居家服務」\n"
    msg += "「長照 伊甸」\n"
    msg += "「長照 台北」\n"
    msg += "「長照 失智」"
    
    return msg
