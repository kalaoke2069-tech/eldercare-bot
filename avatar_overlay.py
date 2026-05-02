"""
Companion Avatar Generator - 把名字加在圖片上
"""

from PIL import Image, ImageDraw, ImageFont
import os

def add_name_overlay(image_path, name, output_path):
    """在圖片上加上名字浮水印"""
    try:
        img = Image.open(image_path).convert('RGB')
        img_w, img_h = img.size
        
        # 字體大小根據圖片調整
        font_size = max(int(img_h * 0.08), 30)
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", font_size)
        except:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
        
        draw = ImageDraw.Draw(img)
        
        # 半透明黑色背景
        overlay_h = int(img_h * 0.15)
        overlay = Image.new('RGBA', (img_w, overlay_h), (0, 0, 0, 180))
        img.paste(overlay, (0, img_h - overlay_h), overlay)
        
        draw = ImageDraw.Draw(img)
        
        # 白字
        name_short = name  # 可以根據需要截斷
        text_y = img_h - int(overlay_h * 0.65)
        
        # 左右留白
        margin = int(img_w * 0.05)
        
        draw.text((margin, text_y), name_short, font=font, fill=(255, 255, 255))
        
        img.save(output_path, quality=95)
        return True
    except Exception as e:
        print(f"Error adding overlay: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python avatar_overlay.py <input_image> <name> <output_image>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    name = sys.argv[2]
    output_path = sys.argv[3]
    
    success = add_name_overlay(input_path, name, output_path)
    print(f"Success: {success}" if success else f"Failed")
