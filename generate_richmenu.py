"""
ElderCare Rich Menu v8 - 更大字體 + 簡潔圖示
尺寸: 2500 x 1686 px
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

WIDTH = 1200
HEIGHT = 810

# 暖色調配色
WARM_WHITE = (255, 248, 240)
WARM_GOLD = (255, 200, 100)
WARM_ORANGE = (255, 160, 60)
CARD_BG = (40, 30, 25)
SHADOW = (20, 15, 10)

# 6個功能表
MENU = [
    {"en": "SERVICE", "zh": "服務簡介", "sub": "認識我們的服務"},
    {"en": "LTC DATABASE", "zh": "長照資料庫", "sub": "政府與NGO資源"},
    {"en": "EMERGENCY", "zh": "緊急電話", "sub": "各縣市聯絡"},
    {"en": "MEDICAL", "zh": "醫療照護", "sub": "醫院與診所"},
    {"en": "GUIDE", "zh": "使用說明", "sub": "Chatbot指南"},
    {"en": "MORE", "zh": "更多功能", "sub": "持續更新"},
]

colors = [WARM_GOLD, WARM_ORANGE, WARM_GOLD, WARM_ORANGE, WARM_GOLD, WARM_ORANGE]


def draw_icon_simple(draw, cx, cy, size, color):
    """繪製簡潔的線條圖示（使用線條而不是填充）"""
    r = size // 2
    
    # 外圈
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=4)
    
    # 中心十字（通用圖示）
    thick = 4
    draw.line([cx, cy-r+8, cx, cy+r-8], fill=color, width=thick)
    draw.line([cx-r+8, cy, cx+r-8, cy], fill=color, width=thick)


def draw_card(draw, x1, y1, x2, y2, color, item, font_en, font_zh, font_sub):
    """繪製卡片"""
    r = 25
    gap = 8
    
    # 陰影
    draw.rounded_rectangle([x1+gap, y1+gap, x2, y2], radius=r, fill=SHADOW)
    
    # 半透明深色背景
    draw.rounded_rectangle([x1, y1, x2-gap, y2-gap], radius=r, fill=CARD_BG)
    
    # 左側亮色邊條
    draw.rounded_rectangle([x1, y1, x1+16, y2-gap], radius=8, fill=color)
    
    # 英文（暖金色、加粗）
    en_y = y1 + 30
    draw.text((x1+60, en_y), item["en"], font=font_en, fill=color)
    
    # 中文（超大字體、超粗）
    zh_y = y1 + 85
    draw.text((x1+60, zh_y), item["zh"], font=font_zh, fill=WARM_WHITE)
    
    # 副標題（暖白）
    sub_y = y1 + 200
    draw.text((x1+60, sub_y), item["sub"], font=font_sub, fill=(200, 180, 160))


def create_rich_menu():
    # 載入背景圖
    bg_path = os.path.join(os.path.dirname(__file__), "dawn.png")
    try:
        bg = Image.open(bg_path).convert('RGB')
        bg = bg.resize((WIDTH, HEIGHT), Image.LANCZOS)
        bg = bg.point(lambda x: x * 0.4)
        enhancer = ImageEnhance.Color(bg)
        bg = enhancer.enhance(0.65)
        enhancer = ImageEnhance.Contrast(bg)
        bg = enhancer.enhance(1.3)
    except Exception as e:
        print(f"Background load error: {e}")
        bg = Image.new('RGB', (WIDTH, HEIGHT), (30, 20, 15))
    
    draw = ImageDraw.Draw(bg)
    
    # 字體（增大30%，按比例縮小）
    try:
        font_brand = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 32)
        font_en = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
        font_zh = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 62)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 24)
    except:
        font_brand = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 32)
        font_en = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
        font_zh = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 62)
        font_sub = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
    
    # 頂部品牌區
    draw.rectangle([0, 0, WIDTH, 120], fill=(20, 15, 10))
    draw.rectangle([0, 120, WIDTH, 128], fill=WARM_GOLD)
    
    # 品牌名稱
    draw.text((50, 35), "ElderCare 陪伴者", font=font_brand, fill=WARM_WHITE)
    draw.text((50, 90), "您的專屬長照 AI 助手", font=font_sub, fill=(200, 180, 150))
    
    # 底部標語
    draw.rectangle([0, HEIGHT-65, WIDTH, HEIGHT-55], fill=(20, 15, 10))
    draw.text((WIDTH - 420, HEIGHT - 52), "24/7 AI 陪伴 | 守護您每一天", font=font_sub, fill=WARM_GOLD)
    draw.rectangle([0, HEIGHT-55, WIDTH, HEIGHT-50], fill=WARM_GOLD)
    
    # 6宮格
    cols, rows = 3, 2
    cell_w = WIDTH // cols
    cell_h = (HEIGHT - 128) // rows
    gap = 42
    start_y = 128
    
    for i, item in enumerate(MENU):
        col = i % cols
        row = i // cols
        
        x1 = col * cell_w + gap
        y1 = start_y + row * cell_h + gap
        x2 = (col + 1) * cell_w - gap
        y2 = start_y + (row + 1) * cell_h - gap
        
        draw_card(draw, x1, y1, x2, y2, colors[i], item, font_en, font_zh, font_sub)
        
        # 右側簡潔圖示（十字圓圈）
        icon_x = x2 - 145
        icon_y = y1 + (y2 - y1) // 2
        draw_icon_simple(draw, icon_x, icon_y, 100, colors[i])
    
    return bg


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "richmenu_output.png")
    
    print("Generating Rich Menu v8 (30% Larger + Simple Icons)...")
    img = create_rich_menu()
    img.save(output_path)
    print("Rich Menu saved to: " + output_path)
    print("Size: " + str(WIDTH) + " x " + str(HEIGHT) + " px")