"""
ElderCare Flex Message Templates
6種 Rich Menu 按鈕的 Flex Message 內容
"""

from linebot.models import (
    FlexSendMessage, BubbleContainer, BoxComponent, 
    TextComponent, ButtonComponent, IconComponent,
    SeparatorComponent, URIAction, MessageAction,
    ButtonComponent, BoxComponent, TextComponent
)
from linebot.models.flex_message import FlexContainer


# =====================================================
# 1. 服務簡介
# =====================================================

def service_intro_flex():
    """服務簡介 Flex Message"""
    return FlexSendMessage(
        alt_text="服務簡介",
        contents=BubbleContainer(
            header=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text="📋 EldeCare 服務簡介", weight="bold", size="lg", color="#2E7D32"),
                    TextComponent(text="您的專屬長照 AI 助手", size="sm", color="#666666", margin="sm")
                ],
                paddingAll="15px"
            ),
            body=BoxComponent(
                layout="vertical",
                contents=[
                    BoxComponent(
                        layout="vertical",
                        spacing="md",
                        contents=[
                            TextComponent(text="🤖 AI Companion 陪伴", size="md", weight="bold"),
                            TextComponent(text="選擇你喜歡的人格（學者、奶奶、廚師等），AI 會像朋友一样陪你聊天、問候、給予建議", size="sm", color="#555555", wrap=True)
                        ]
                    ),
                    SeparatorComponent(color="#81C784"),
                    BoxComponent(
                        layout="vertical",
                        spacing="md",
                        contents=[
                            TextComponent(text="📊 健康記錄", size="md", weight="bold"),
                            TextComponent(text="記錄血壓、血糖等健康數據，長期追蹤走勢", size="sm", color="#555555", wrap=True)
                        ]
                    ),
                    SeparatorComponent(color="#81C784"),
                    BoxComponent(
                        layout="vertical",
                        spacing="md",
                        contents=[
                            TextComponent(text="🏥 長照資源查詢", size="md", weight="bold"),
                            TextComponent(text="输入「長照」快速查詢政府與 NGO 的長照服務資源", size="sm", color="#555555", wrap=True)
                        ]
                    ),
                    SeparatorComponent(color="#81C784"),
                    BoxComponent(
                        layout="vertical",
                        spacing="md",
                        contents=[
                            TextComponent(text="🚨 緊急通報", size="md", weight="bold"),
                            TextComponent(text="一鍵通知所有家人，緊急情況即時通報", size="sm", color="#555555", wrap=True)
                        ]
                    )
                ],
                paddingAll="15px"
            ),
            footer=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text="輸入 /help 查看所有指令", size="sm", color="#888888", align="center")
                ],
                paddingAll="10px"
            ),
            styles={"header": {"backgroundColor": "#F1F8E9"}}
        )
    )


# =====================================================
# 2. 長照資料庫
# =====================================================

def ltc_database_flex():
    """長照資料庫 Flex Message"""
    items = [
        {"title": "🌐 衛福部1966長照專線", "desc": "每週一至五 08:30-17:30", "action": "tel:1966"},
        {"title": "🏠 居家服務", "desc": "照顧服務員到宅協助日常生活", "action": "https://www.mohw.gov.tw/mp-2.html"},
        {"title": "😌 喘息服務", "desc": "照顧者短期休息，最長14-21天/年", "action": "https://www.mohw.gov.tw/mp-2.html"},
        {"title": "🏥 機構服務", "desc": "護理之家、康護之家、養老院", "action": "https://www.mohw.gov.tw/mp-2.html"},
        {"title": "💊 輔具補助", "desc": "每10年最高補助10萬元", "action": "https://www.mohw.gov.tw/mp-2.html"},
        {"title": "🙏 伊甸基金會", "desc": "身障、老人、弱勢家庭服務", "action": "https://www.eden.org.tw/"},
        {"title": "🌳 弘道老人福利基金會", "desc": "居家服務、日照中心", "action": "https://www.hondao.org.tw/"},
    ]
    
    contents = []
    for item in items:
        contents.append(
            BoxComponent(
                layout="vertical",
                spacing="sm",
                contents=[
                    TextComponent(text=item["title"], weight="bold", size="md"),
                    TextComponent(text=item["desc"], size="sm", color="#666666"),
                    ButtonComponent(
                        style="link",
                        height="sm",
                        action=URIAction(label="查看詳情", uri=item["action"])
                    )
                ],
                paddingAll="10px"
            )
        )
        contents.append(SeparatorComponent(color="#E0E0E0"))
    
    return FlexSendMessage(
        alt_text="長照資料庫",
        contents=BubbleContainer(
            header=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text="🏥 長照資源資料庫", weight="bold", size="lg", color="#2E7D32"),
                    TextComponent(text="政府與 NGO 長照服務資源", size="sm", color="#666666", margin="sm")
                ],
                paddingAll="15px"
            ),
            body=BoxComponent(
                layout="vertical",
                contents=contents,
                paddingAll="10px"
            ),
            styles={"header": {"backgroundColor": "#F1F8E9"}}
        )
    )


# =====================================================
# 3. 緊急電話
# =====================================================

def emergency_phone_flex():
    """緊急電話 Flex Message"""
    items = [
        {"region": "🌐 全國", "phone": "1966", "desc": "長照服務專線"},
        {"region": "🚨 緊急", "phone": "110", "desc": "報案"},
        {"region": "🏥 救護", "phone": "119", "desc": "叫救護車"},
        {"region": "📞 台北市", "phone": "02-2759-3000", "desc": "照顧管理中心"},
        {"region": "📞 新北市", "phone": "02-2968-3333", "desc": "照顧管理中心"},
        {"region": "📞 桃園市", "phone": "03-332-1321", "desc": "照顧管理中心"},
        {"region": "📞 台中市", "phone": "04-2515-5888", "desc": "照顧管理中心"},
        {"region": "📞 高雄市", "phone": "07-337-3370", "desc": "照顧管理中心"},
    ]
    
    contents = []
    for item in items:
        contents.append(
            BoxComponent(
                layout="horizontal",
                spacing="md",
                contents=[
                    BoxComponent(
                        layout="vertical",
                        flex=2,
                        contents=[
                            TextComponent(text=item["region"], weight="bold", size="md"),
                            TextComponent(text=item["desc"], size="sm", color="#888888")
                        ]
                    ),
                    BoxComponent(
                        layout="vertical",
                        flex=1,
                        contents=[
                            ButtonComponent(
                                style="primary",
                                color="#2E7D32",
                                height="sm",
                                action=URIAction(label=item["phone"], uri=f"tel:{item['phone'].replace('-','')}")
                            )
                        ]
                    )
                ],
                paddingAll="8px"
            )
        )
        contents.append(SeparatorComponent(color="#E0E0E0"))
    
    return FlexSendMessage(
        alt_text="緊急電話",
        contents=BubbleContainer(
            header=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text="☎️ 緊急聯絡電話", weight="bold", size="lg", color="#C62828"),
                    TextComponent(text="點擊可直接撥打電話", size="sm", color="#666666", margin="sm")
                ],
                paddingAll="15px"
            ),
            body=BoxComponent(
                layout="vertical",
                contents=contents,
                paddingAll="10px"
            ),
            styles={"header": {"backgroundColor": "#FFEBEE"}}
        )
    )


# =====================================================
# 4. 醫療照護
# =====================================================

def medical_care_flex():
    """醫療照護 Flex Message"""
    items = [
        {"title": "🏥 衛福部中央健康保險署", "desc": "健保卡、就醫、問題處理", "uri": "https://www.nhi.gov.tw/"},
        {"title": "🏨 醫療糾紛調處", "desc": "各縣市醫療調處窗口", "uri": "https://www.mohw.gov.tw/"},
        {"title": "💊 藥品查詢", "desc": "健保藥品項目查詢", "uri": "https://www.nhi.gov.tw/"},
        {"title": "🩺 全民健康保險", "desc": "健保相關資訊", "uri": "https://www.nhi.gov.tw/"},
        {"title": "🏠 居家醫療", "desc": "行動不便者居家醫療服務", "uri": "https://www.mohw.gov.tw/"},
    ]
    
    contents = []
    for item in items:
        contents.append(
            BoxComponent(
                layout="vertical",
                spacing="sm",
                contents=[
                    TextComponent(text=item["title"], weight="bold", size="md"),
                    TextComponent(text=item["desc"], size="sm", color="#666666"),
                    ButtonComponent(
                        style="link",
                        height="sm",
                        action=URIAction(label="查看詳情", uri=item["uri"])
                    )
                ],
                paddingAll="10px"
            )
        )
        contents.append(SeparatorComponent(color="#E0E0E0"))
    
    return FlexSendMessage(
        alt_text="醫療照護",
        contents=BubbleContainer(
            header=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text="🏩 醫療照護資源", weight="bold", size="lg", color="#1565C0"),
                    TextComponent(text="醫院、診所、健康相關服務", size="sm", color="#666666", margin="sm")
                ],
                paddingAll="15px"
            ),
            body=BoxComponent(
                layout="vertical",
                contents=contents,
                paddingAll="10px"
            ),
            styles={"header": {"backgroundColor": "#E3F2FD"}}
        )
    )


# =====================================================
# 5. 使用說明
# =====================================================

def user_guide_flex():
    """使用說明 Flex Message"""
    items = [
        {"emoji": "1️⃣", "title": "選擇朋友", "desc": "輸入「更換朋友」選擇你喜歡的 AI Companion 人格"},
        {"emoji": "2️⃣", "title": "日常聊天", "desc": "像跟朋友聊天一樣，直接輸入文字即可獲得 AI 回覆"},
        {"emoji": "3️⃣", "title": "記錄血壓", "desc": "輸入格式「130/80」，Bot 會幫你記錄並分析"},
        {"emoji": "4️⃣", "title": "查詢長照", "desc": "輸入「長照」或「長照+關鍵字」，查詢長照資源"},
        {"emoji": "5️⃣", "title": "緊急通報", "desc": "輸入「/緊急」通知所有家人"},
        {"emoji": "6️⃣", "title": "健康打卡", "desc": "輸入「/打卡」每日健康記錄"},
    ]
    
    contents = []
    for item in items:
        contents.append(
            BoxComponent(
                layout="horizontal",
                spacing="md",
                contents=[
                    TextComponent(text=item["emoji"], size="xl"),
                    BoxComponent(
                        layout="vertical",
                        contents=[
                            TextComponent(text=item["title"], weight="bold", size="md"),
                            TextComponent(text=item["desc"], size="sm", color="#666666", wrap=True)
                        ]
                    )
                ],
                paddingAll="8px"
            )
        )
        contents.append(SeparatorComponent(color="#E0E0E0"))
    
    return FlexSendMessage(
        alt_text="使用說明",
        contents=BubbleContainer(
            header=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text="📖 EldeCare 使用說明", weight="bold", size="lg", color="#2E7D32"),
                    TextComponent(text="快速上手指南", size="sm", color="#666666", margin="sm")
                ],
                paddingAll="15px"
            ),
            body=BoxComponent(
                layout="vertical",
                contents=contents,
                paddingAll="10px"
            ),
            styles={"header": {"backgroundColor": "#F1F8E9"}}
        )
    )


# =====================================================
# 6. 更多功能（預留）
# =====================================================

def more_features_flex():
    """更多功能（預留）Flex Message"""
    return FlexSendMessage(
        alt_text="更多功能",
        contents=BubbleContainer(
            header=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text="➕ 更多功能", weight="bold", size="lg", color="#2E7D32"),
                    TextComponent(text="持續更新中，敬請期待！", size="sm", color="#666666", margin="sm")
                ],
                paddingAll="15px"
            ),
            body=BoxComponent(
                layout="vertical",
                contents=[
                    BoxComponent(
                        layout="vertical",
                        spacing="md",
                        contents=[
                            TextComponent(text="🚧 功能開發中", weight="bold", size="md", color="#666666"),
                            TextComponent(text="以下是即將上線的功能：", size="sm", color="#888888", wrap=True),
                        ],
                        paddingAll="15px"
                    ),
                    SeparatorComponent(color="#E0E0E0"),
                    BoxComponent(
                        layout="vertical",
                        spacing="sm",
                        contents=[
                            TextComponent(text="⏰ 每日健康打卡提醒", size="md"),
                            TextComponent(text="定時問候，確認用戶安全", size="sm", color="#888888"),
                        ],
                        paddingAll="10px"
                    ),
                    SeparatorComponent(color="#E0E0E0"),
                    BoxComponent(
                        layout="vertical",
                        spacing="sm",
                        contents=[
                            TextComponent(text="💊 用藥提醒", size="md"),
                            TextComponent(text="設定服藥時間，準時提醒", size="sm", color="#888888"),
                        ],
                        paddingAll="10px"
                    ),
                    SeparatorComponent(color="#E0E0E0"),
                    BoxComponent(
                        layout="vertical",
                        spacing="sm",
                        contents=[
                            TextComponent(text="📊 健康報告", size="md"),
                            TextComponent(text="每週/每月健康趨勢分析", size="sm", color="#888888"),
                        ],
                        paddingAll="10px"
                    ),
                ],
                paddingAll="10px"
            ),
            footer=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text="即將上線，敬請期待！", size="sm", color="#888888", align="center")
                ],
                paddingAll="10px"
            ),
            styles={"header": {"backgroundColor": "#F1F8E9"}}
        )
    )


# =====================================================
# 快捷回覆地圖
# =====================================================

FLEX_MAP = {
    "menu_service_intro": service_intro_flex,
    "menu_ltc_database": ltc_database_flex,
    "menu_emergency_phone": emergency_phone_flex,
    "menu_medical_care": medical_care_flex,
    "menu_user_guide": user_guide_flex,
    "menu_more_features": more_features_flex,
}


def get_flex_message(action_key):
    """根據 action key 取得對應的 Flex Message"""
    return FLEX_MAP.get(action_key, lambda: None)()