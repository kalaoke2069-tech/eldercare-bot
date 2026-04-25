"""
ElderCare Rich Menu 背景圖生成器 v4
尺寸: 2500 x 1686 px (LINE Rich Menu 標準尺寸)
"""

from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 2500
HEIGHT = 1686

# 顏色設定
WHITE = (255, 255, 255)
PRIMARY_GREEN = (46, 125, 50)
ACCENT_GREEN = (76, 175, 80)
LIGHT_GREEN = (200, 230, 201)
VERY_LIGHT = (245, 250, 245)
TEXT_DARK = (55, 71, 79)
TEXT_GRAY = (110, 120, 130)

# 6個功能表
MENU = [
    {"icon": "📋", "title": "服務簡介", "subtitle": "認識我們的服務", "color": PRIMARY_GREEN},
    {"icon": "🏥", "title": "長照資料庫", "subtitle": "政府與NGO資源", "color": ACCENT_GREEN},
    {"icon": "☎️", "title": "緊急電話", "subtitle": "各縣市聯絡", "color": PRIMARY_GREEN},
    {"icon": "🏩", "title": "醫療照護", "subtitle": "醫院與診所", "color": ACCENT_GREEN},
    {"icon": "📖", "title": "使用說明", "subtitle": "Chatbot指南", "color": PRIMARY_GREEN},
    {"icon": "➕", "title": "更多功能", "subtitle": "持續更新", "color": ACCENT_GREEN},
]


def draw_icon_circle(draw, x, y, radius, color, emoji, font_size=70):
    """在指定位置繪製帶 emoji 的圓形圖示"""
    # 外圈
    draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=LIGHT_GREEN)
    # 內圈
    draw.ellipse([(x - radius + 8, y - radius + 8), (x + radius - 8, y + radius - 8)], fill=color)
    # Emoji
    try:
        font_icon = ImageFont.truetype("C:/Windows/Fonts/seguisb.ttf", font_size)
        draw.text((x - font_size // 2 - 5, y - font_size // 2 - 5), emoji, font=font_icon, fill=WHITE)
    except:
        pass


def draw_card(draw, x1, y1, x2, y2, color, icon, title, subtitle):
    """繪製一個功能卡片"""
    # 陰影
    shadow_offset = 10
    draw.rounded_rectangle(
        [(x1 + shadow_offset, y1 + shadow_offset), (x2, y2)],
        radius=30,
        fill=(220, 220, 220)
    )
    
    # 白色卡片背景
    draw.rounded_rectangle(
        [(x1, y1), (x2 - shadow_offset, y2 - shadow_offset)],
        radius=30,
        fill=WHITE
    )
    
    # 左側彩色邊條
    draw.rounded_rectangle(
        [(x1, y1), (x1 + 18, y2 - shadow_offset)],
        radius=9,
        fill=color
    )
    
    # 圖示
    icon_x = x1 + 130
    icon_y = y1 + (y2 - y1) // 2
    draw_icon_circle(draw, icon_x, icon_y, 70, color, icon)
    
    # 標題
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 52)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 28)
    except:
        font_title = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 52)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28)
    
    title_x = x1 + 260
    title_y = y1 + 90
    draw.text((title_x, title_y), title, font=font_title, fill=TEXT_DARK)
    
    # 副標題
    sub_y = title_y + 70
    draw.text((title_x, sub_y), subtitle, font=font_sub, fill=TEXT_GRAY)
    
    # 右側箭頭
    try:
        font_arrow = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 60)
        arrow_x = x2 - 100
        arrow_y = y1 + (y2 - y1) // 2 - 30
        draw.text((arrow_x, arrow_y), ">", font=font_arrow, fill=(180, 180, 180))
    except:
        pass


def create_rich_menu():
    """生成 Rich Menu 背景圖"""
    img = Image.new('RGB', (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)
    
    # 頂部綠色條
    draw.rectangle([(0, 0), (WIDTH, 10)], fill=ACCENT_GREEN)
    
    # 頂部標題區（淺綠色背景）
    draw.rectangle([(0, 10), (WIDTH, 130)], fill=VERY_LIGHT)
    
    # 標題
    try:
        font_brand = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 52)
        font_tag = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 28)
    except:
        font_brand = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 52)
        font_tag = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28)
    
    draw.text((60, 40), "ElderCare 陪伴者", font=font_brand, fill=PRIMARY_GREEN)
    draw.text((60, 95), "您的專屬長照 AI 助手", font=font_tag, fill=TEXT_GRAY)
    
    # 底部標語
    draw.text((WIDTH - 300, HEIGHT - 55), "24/7 AI 陪伴", font=font_tag, fill=TEXT_GRAY)
    
    # 分隔線
    draw.rectangle([(0, 130), (WIDTH, 136)], fill=ACCENT_GREEN)
    
    # 6宮格（3列 x 2行）
    cols, rows = 3, 2
    cell_w = WIDTH // cols
    cell_h = (HEIGHT - 136) // rows
    gap = 40
    start_y = 136
    
    for i, item in enumerate(MENU):
        col = i % cols
        row = i // cols
        
        x1 = col * cell_w + gap
        y1 = start_y + row * cell_h + gap
        x2 = (col + 1) * cell_w - gap
        y2 = start_y + (row + 1) * cell_h - gap
        
        draw_card(draw, x1, y1, x2, y2, item["color"], item["icon"], item["title"], item["subtitle"])
    
    # 底部綠色條
    draw.rectangle([(0, HEIGHT - 10), (WIDTH, HEIGHT)], fill=ACCENT_GREEN)
    
    # 角落裝飾
    for i in range(5):
        y = HEIGHT - 80 - i * 20
        draw.ellipse([(30 - i*6, y), (50 - i*6, y + 25)], fill=LIGHT_GREEN)
        draw.ellipse([(WIDTH - 50 + i*6, y), (WIDTH - 30 + i*6, y + 25)], fill=LIGHT_GREEN)
    
    return img


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "richmenu_output.png")
    
    print("Generating Rich Menu image v4 (2500 x 1686)...")
    img = create_rich_menu()
    img.save(output_path)
    print("Rich Menu saved to: " + output_path)
    print("Size: " + str(WIDTH) + " x " + str(HEIGHT) + " px")