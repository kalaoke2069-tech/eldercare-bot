"""批次處理所有Companion圖片，加上名字浮水印"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

# 設定路徑
INPUT_DIR = r"C:\Users\Joshyoh\.openclaw\workspace\eldercare-project\code\static\images"
OUTPUT_DIR = r"C:\Users\Joshyoh\.openclaw\workspace\eldercare-project\code\static\images"

# Companion名字對應表
COMPANION_NAMES = {
    "scholar": "老陳",
    "grandma": "美雲阿姨",
    "comedian": "阿Ken",
    "chef": "阿美姐",
    "astrologer": "韻璇",
    "fengshui": "雲峰大師",
    "rockefeller": "洛克菲勒",
    "li_ka_shing": "李嘉誠",
    "james_simons": "西蒙斯",
    "scientist": "林博士",
    "dr_lin": "林博士",
    "music_teacher": "阿傑",
    "gardener": "阿土伯",
    "artist": "小敏",
}

def add_name_overlay(image_path, name, output_path):
    """在圖片底部加上半透明黑色橫幅和名字"""
    try:
        img = Image.open(image_path).convert('RGB')
        img_w, img_h = img.size
        
        draw = ImageDraw.Draw(img)
        
        # 字體大小根據圖片調整
        font_size = max(int(img_h * 0.1), 35)
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", font_size)
        except:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
        
        # 底部半透明黑色橫幅
        bar_height = int(img_h * 0.18)
        bar_y = img_h - bar_height
        
        # 建立半透明覆蓋層
        overlay = Image.new('RGBA', (img_w, bar_height), (0, 0, 0, 200))
        img.paste(overlay, (0, bar_y))
        
        draw = ImageDraw.Draw(img)
        
        # 計算文字位置（置中）
        bbox = draw.textbbox((0, 0), name, font=font)
        text_w = bbox[2] - bbox[0]
        text_x = (img_w - text_w) // 2
        text_y = bar_y + (bar_height - (bbox[3] - bbox[1])) // 2 - 5
        
        # 白色文字
        draw.text((text_x, text_y), name, font=font, fill=(255, 255, 255))
        
        img.save(output_path, quality=95)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    # 設定輸出編碼
    sys.stdout.reconfigure(encoding='utf-8')
    
    count = 0
    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith(('.jpeg', '.jpg', '.png')):
            continue
        
        # 從檔名取得companion key
        companion_key = filename.rsplit('.', 1)[0]
        
        if companion_key in COMPANION_NAMES:
            name = COMPANION_NAMES[companion_key]
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename)
            
            print(f"Processing: {filename} -> {name}")
            if add_name_overlay(input_path, name, output_path):
                count += 1
    
    print(f"\nDone! {count} images processed.")


if __name__ == "__main__":
    main()
