#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys
import os
import shlex
import math
import random

OVERLAY_TEMPLATE_PATH = "../assets/overlay_shape_fullwidth.png"

COLOR_PALETTE = [
    # --- 白色和灰色系 ---
    "#FFFFFF",  # 纯白色 (Classic White)
    "#F5F5F5",  # 白烟色 (WhiteSmoke - 极浅灰)
    "#E5E4E2",  # 铂金色 (Platinum - 近乎白色的银灰)
    "#D3D3D3",  # 浅灰色 (LightGray)
    "#C0C0C0",  # 银色 (Silver)
    # --- 金色和黄色系 ---
    "#F5E5A0",  # 淡金色 (PaleGoldenrod - 柔和)
    "#FAFAD2",  # 亮金黄色 (LightGoldenrodYellow - 极浅黄)
    "#EEE8AA",  # 苍麒麟色 (PaleGoldenrod - 略深)
    "#FFD700",  # 金色 (Gold - 标准亮金)
    "#DAA520",  # 金麒麟色 (Goldenrod - 偏暗金)
    "#B8860B",  # 暗金麒麟色 (DarkGoldenrod - 深金)
    "#FAF0E6",  # 亚麻色 (Linen - 浅米白)
    "#D2B48C",  # 褐色 (Tan - 浅棕褐，有时也像暗金)
    # --- 其他色系
    "#FFA07A",  # 亮鲑鱼色 (LightSalmon)
    "#FF7F50",  # 珊瑚色 (Coral)
    "#FFB6C1",  # 浅粉色 (LightPink)
    "#90EE90",  # 淡绿色 (LightGreen)
    "#98FB98",  # 苍绿色 (PaleGreen)
    "#AFEEEE",  # 苍白绿松石色 (PaleTurquoise)
    "#ADD8E6",  # 淡蓝色 (LightBlue)
    "#87CEFA",  # 亮天蓝色 (LightSkyBlue)
    "#D8BFD8",  # 蓟色 (Thistle - 淡紫)
    "#EE82EE",  # 紫罗兰色 (Violet)
]

# --- 第一行 (人名) 的配置 ---
FONT_PATH = "../fonts/GreatVibes-Regular.ttf"
FONT_SIZE_RATIO_LINE1 = 0.075
TEXT_OFFSET_X_PERCENT_LINE1 = 20
TEXT_OFFSET_Y_PERCENT_LINE1 = 10

# --- 第二行 ("Collection") 的配置 ---
FONT_PATH_COLLECTION = "JosefinSans-LightItalic.ttf"
FONT_SIZE_RATIO_LINE2 = 0.05  # 示例值: 1.5%
TEXT_COLOR_COLLECTION = "#FFFFFF"
TEXT_OFFSET_X_PERCENT_LINE2 = 20 
TEXT_OFFSET_Y_PERCENT_LINE2 = 3

# --- 其他设置 ---
OUTPUT_SUFFIX = "_styled_final"
TEMP_OVERLAY_NAME = "_temp_overlay.png"
MAGICK_CMD = "magick"
# ---------------------------------

def get_image_dimensions(image_path):
    """使用 magick identify 获取图片宽高"""
    try:
        command = [MAGICK_CMD, "identify", "-format", "%w %h", image_path]
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        first_line = result.stdout.splitlines()[0]
        width, height = map(int, first_line.split())
        return width, height
    except FileNotFoundError:
        print(f"错误：找不到 '{MAGICK_CMD}' 命令。请确保 ImageMagick 已安装并添加到系统 PATH。")
        return None, None
    except Exception as e:
        print(f"错误：无法获取图片尺寸 '{image_path}': {e}")
        identify_stdout = result.stdout if 'result' in locals() else 'N/A'
        identify_stderr = result.stderr if 'result' in locals() else 'N/A'
        print(f"Identify 命令输出: {identify_stdout}")
        print(f"Identify 错误输出: {identify_stderr}")
        return None, None

def process_image(input_image_path, person_name):
    """
    自适应处理图片：转黑白，动态缩放并添加蒙层，动态计算大小和位置添加文字。
    """
    # 检查输入和蒙层文件
    if not os.path.exists(input_image_path):
        print(f"错误：找不到输入图片文件 '{input_image_path}'")
        return
    if not os.path.exists(OVERLAY_TEMPLATE_PATH):
        print(f"错误：找不到蒙层模板文件 '{OVERLAY_TEMPLATE_PATH}'")
        return

    # 1. 获取原图尺寸 (确保处理单帧)
    input_frame_spec = input_image_path + "[0]"
    img_w, img_h = get_image_dimensions(input_frame_spec)
    if not img_w or not img_h:
        return

    print(f"图片尺寸: {img_w}x{img_h}")

    # 构建输出和临时文件名
    base, input_ext = os.path.splitext(input_image_path)
    output_ext = ".png" # 强制输出 PNG 以获得最佳质量和透明度
    output_image_path = f"{base}{OUTPUT_SUFFIX}{output_ext}"
    script_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else "."
    temp_overlay_path = os.path.join(script_dir, f"{os.path.basename(base)}{TEMP_OVERLAY_NAME}")

    # 2. 动态调整蒙层大小
    try:
        resize_command = [
            MAGICK_CMD, OVERLAY_TEMPLATE_PATH,
            "-resize", f"{img_w}x", # 宽度匹配，高度等比
            f"png:{temp_overlay_path}" # 确保临时文件是 PNG
        ]
        print(f"正在缩放蒙层: {' '.join(shlex.quote(str(arg)) for arg in resize_command)}")
        subprocess.run(resize_command, check=True, capture_output=True)
    except Exception as e:
        print(f"错误：缩放蒙层失败: {e}")
        if isinstance(e, subprocess.CalledProcessError):
             print(f"错误输出: {e.stderr.decode('utf-8', errors='ignore')}")
        if os.path.exists(temp_overlay_path):
             try: os.remove(temp_overlay_path)
             except OSError: pass
        return

    # 3. 动态计算字体大小
    font_size1 = max(10, int(img_h * FONT_SIZE_RATIO_LINE1))
    font_size2 = max(8, int(img_h * FONT_SIZE_RATIO_LINE2)) # <- 使用 FONT_SIZE_RATIO_LINE2
    print(f"动态字号: {font_size1}pt, {font_size2}pt")

    # 4. 动态计算文字偏移量 (像素值)
    offset_x1_px = int(img_w * (TEXT_OFFSET_X_PERCENT_LINE1 / 100.0))
    offset_y1_px = int(img_h * (TEXT_OFFSET_Y_PERCENT_LINE1 / 100.0))
    text_offset1 = f"+{offset_x1_px}+{offset_y1_px}"

    offset_x2_px = int(img_w * (TEXT_OFFSET_X_PERCENT_LINE2 / 100.0))
    offset_y2_px = int(img_h * (TEXT_OFFSET_Y_PERCENT_LINE2 / 100.0))
    text_offset2 = f"+{offset_x2_px}+{offset_y2_px}"
    print(f"动态偏移1: {text_offset1}, 动态偏移2: {text_offset2}")

    # 随机选择人名颜色
    selected_color_line1 = random.choice(COLOR_PALETTE)
    print(f"随机选择颜色: {selected_color_line1}")

    # 5. 构建最终的 ImageMagick 命令
    command = [
        MAGICK_CMD,
        input_frame_spec,           # 使用带帧说明符的输入
        "-colorspace", "Gray",      # 转灰度

        # --- 合成蒙层 ---
        "(", temp_overlay_path, ")",
        "-gravity", "South",
        "-composite",

        # --- 添加文字 ---
        "-gravity", "South",        # 定位基准

        # 第一行 (人名)
        "-font", FONT_PATH,
        "-pointsize", str(font_size1),
        "-fill", selected_color_line1, # 使用随机颜色
        "-annotate", text_offset1,
        person_name,

        # 第二行 (Collection)
        "-font", FONT_PATH_COLLECTION,
        "-pointsize", str(font_size2), # <- *** 修正：使用 font_size2 ***
        "-fill", TEXT_COLOR_COLLECTION,
        "-annotate", text_offset2,
        "COLLECTION",                 # <- 写死 "Collection"
        # "Collection",                 # <- 写死 "Collection"

        f"png:{output_image_path}"    # 输出为 PNG
    ]

    print(f"正在执行最终命令: {' '.join(shlex.quote(str(arg)) for arg in command)}")

    try:
        # 执行命令
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        print(f"成功生成图片: {output_image_path}")
    except FileNotFoundError:
        print(f"错误：找不到 '{MAGICK_CMD}' 命令。请确保 ImageMagick 已安装并添加到系统 PATH。")
    except subprocess.CalledProcessError as e:
        print(f"错误：ImageMagick 命令执行失败。")
        print(f"返回码: {e.returncode}")
        # 尝试更友好地打印错误输出
        try:
            stderr_decoded = e.stderr.decode('utf-8', errors='ignore')
            print(f"错误输出:\n{stderr_decoded}")
        except:
             print(f"错误输出 (原始): {e.stderr}")
        print(f"请检查 ImageMagick 命令参数是否正确，特别是文件路径和字体名称。")
    except Exception as e:
        print(f"发生未知错误: {e}")
    finally:
        # 清理临时蒙层文件
        if os.path.exists(temp_overlay_path):
            try:
                os.remove(temp_overlay_path)
                print(f"已删除临时文件: {temp_overlay_path}")
            except OSError as e:
                print(f"警告：无法删除临时文件 '{temp_overlay_path}': {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python process_script.py <图片路径> \"<人物名称>\"")
        print("例如: python process_script.py \"C:/path to/my_photo.jpg\" \"Jackie Chan\"")
        sys.exit(1)

    image_path = sys.argv[1]
    name_text = sys.argv[2]

    if not os.path.exists(image_path):
         print(f"错误：输入图片路径不存在 '{image_path}'")
         sys.exit(1)

    process_image(image_path, name_text)