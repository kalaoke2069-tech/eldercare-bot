"""
ElderCare Rich Menu 背景圖生成器 v3
尺寸: 2500 x 843 px (LINE Rich Menu 標準尺寸)
清新自然風格 + 彩色 emoji 圖示
"""

from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 2500
HEIGHT = 843

# 顏色設定
WHITE = (255, 255, 255)
PRIMARY_GREEN = (46, 125, 50)
ACCENT_GREEN = (76, 175, 80)
LIGHT_GREEN = (200, 230, 201)
VERY_LIGHT = (245, 250, 245)
TEXT_DARK = (55, 71, 79)
TEXT_GRAY = (110, 120, 130)
CARD_BG = (250, 250, 250)
SHADOW = (220, 220, 220)

# 6個功能表
MENU = [
    {"icon": "📋", "title": "服務簡介", "subtitle": "認識我們的服務", "color": PRIMARY_GREEN},
    {"icon": "🏥", "title": "長照資料庫", "subtitle": "政府與NGO資源", "color": ACCENT_GREEN},
    {"icon": "☎️", "title": "緊急電話", "subtitle": "各縣市聯絡", "color": PRIMARY_GREEN},
    {"icon": "🏩", "title": "醫療照護", "subtitle": "醫院與診所", "color": ACCENT_GREEN},
    {"icon": "📖", "title": "使用說明", "subtitle": "Chatbot指南", "color": PRIMARY_GREEN},
    {"icon": "➕", "title": "更多功能", "subtitle": "持續更新", "color": ACCENT_GREEN},
]


def draw_card(draw, x1, y1, x2, y2, color, icon_emoji, title, subtitle):
    """繪製一個功能卡片"""
    # 陰影
    shadow_offset = 8
    draw.rounded_rectangle(
        [(x1 + shadow_offset, y1 + shadow_offset), (x2, y2)],
        radius=25,
        fill=SHADOW
    )
    
    # 白色卡片背景
    draw.rounded_rectangle(
        [(x1, y1), (x2 - shadow_offset, y2 - shadow_offset)],
        radius=25,
        fill=WHITE
    )
    
    # 左側彩色邊條
    draw.rounded_rectangle(
        [(x1, y1), (x1 + 16, y2 - shadow_offset)],
        radius=8,
        fill=color
    )
    
    # 圖示背景（淺綠色圓形）
    icon_x = x1 + 110
    icon_y = y1 + (y2 - y1) // 2
    draw.ellipse(
        [(icon_x - 60, icon_y - 60), (icon_x + 60, icon_y + 60)],
        fill=LIGHT_GREEN
    )
    draw.ellipse(
        [(icon_x - 52, icon_y - 52), (icon_x + 52, icon_y + 52)],
        fill=color
    )
    
    # 嘗試載入字體
    try:
        font_icon = ImageFont.truetype("C:/Windows/Fonts/seguisb.ttf", 70)
        font_title = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 48)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 28)
    except:
        font_icon = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 70)
        font_title = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 48)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28)
    
    # 圖示 emoji（使用 emoji font fallback）
    try:
        draw.text((icon_x - 28, icon_y - 38), icon_emoji, font=font_icon, fill=WHITE)
    except:
        # 如果 emoji 不支援，用文字替代
        pass
    
    # 標題
    title_x = x1 + 220
    title_y = y1 + 90
    draw.text((title_x, title_y), title, font=font_title, fill=TEXT_DARK)
    
    # 副標題
    sub_y = title_y + 65
    draw.text((title_x, sub_y), subtitle, font=font_sub, fill=TEXT_GRAY)
    
    # 右側箭頭
    arrow_x = x2 - 80
    arrow_y = y1 + (y2 - y1) // 2 - 25
    try:
        draw.text((arrow_x, arrow_y), ">", font=font_icon, fill=(180, 180, 180))
    except:
        pass


def create_rich_menu():
    """生成 Rich Menu 背景圖"""
    img = Image.new('RGB', (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)
    
    # 頂部綠色條
    draw.rectangle([(0, 0), (WIDTH, 8)], fill=ACCENT_GREEN)
    
    # 頂部標題區（淺綠色背景）
    draw.rectangle([(0, 8), (WIDTH, 100)], fill=VERY_LIGHT)
    
    # 標題
    try:
        font_brand = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 44)
    except:
        font_brand = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 44)
    
    draw.text((50, 28), "ElderCare 陪伴者", font=font_brand, fill=PRIMARY_GREEN)
    
    try:
        font_tag = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 24)
    except:
        font_tag = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
    
    draw.text((50, 65), "您的專屬長照 AI 助手", font=font_tag, fill=TEXT_GRAY)
    
    # 底部標語
    draw.text((WIDTH - 250, HEIGHT - 45), "24/7 AI 陪伴", font=font_tag, fill=TEXT_GRAY)
    
    # 分隔線
    draw.rectangle([(0, 100), (WIDTH, 104)], fill=ACCENT_GREEN)
    
    # 6宮格
    cols, rows = 3, 2
    cell_w = WIDTH // cols
    cell_h = (HEIGHT - 104) // rows
    gap = 35
    start_y = 104
    
    for i, item in enumerate(MENU):
        col = i % cols
        row = i // cols
        
        x1 = col * cell_w + gap
        y1 = start_y + row * cell_h + gap
        x2 = (col + 1) * cell_w - gap
        y2 = start_y + (row + 1) * cell_h - gap
        
        draw_card(draw, x1, y1, x2, y2, item["color"], item["icon"], item["title"], item["subtitle"])
    
    # 底部綠色條
    draw.rectangle([(0, HEIGHT - 8), (WIDTH, HEIGHT)], fill=ACCENT_GREEN)
    
    # 角落裝飾（葉子效果）
    for i in range(4):
        y = HEIGHT - 60 - i * 15
        draw.ellipse([(25 - i*5, y), (45 - i*5, y + 20)], fill=LIGHT_GREEN)
        draw.ellipse([(WIDTH - 45 + i*5, y), (WIDTH - 25 + i*5, y + 20)], fill=LIGHT_GREEN)
    
    return img


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "richmenu_output.png")
    
    print("Generating Rich Menu image v3...")
    img = create_rich_menu()
    img.save(output_path)
    print("Rich Menu saved to: " + output_path)
    print("Size: " + str(WIDTH) + " x " + str(HEIGHT) + " px")