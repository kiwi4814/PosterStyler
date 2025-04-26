# PosterStyler
为电影海报增加统一化风格

# Adaptive Poster Styler - 演员/人物风格化海报生成器

这是一个 Python 脚本，旨在使用 ImageMagick 自动为人物照片（例如演员海报）应用统一的风格化效果。其灵感来源于常见的影库人物海报样式。

该脚本能够处理不同分辨率的输入图片，并尝试生成视觉效果一致的输出图片。

## 主要功能

* **灰度转换:** 将输入的彩色图片转换为黑白（灰度）图片。
* **叠加蒙层:** 在图片底部添加一个预先设计好的、横跨整个宽度的半透明倾斜蒙层。
* **动态文本:** 在蒙层上添加两行文字：
    * 第一行：用户指定的人物名称，使用艺术字体，颜色从预设列表中随机选择。
    * 第二行：固定的 "Collection" 字样，使用指定的常规字体和颜色（默认为白色）。
* **自适应布局:**
    * 蒙层宽度会自动缩放以匹配输入图片的宽度。
    * 两行文字的大小会根据输入图片的高度按比例自动调整。
    * 两行文字的位置会根据图片尺寸按百分比自动定位在蒙层区域内（通常在底部中心偏右的位置）。
* **跨平台:** 依赖 Python 和 ImageMagick，理论上可在 Windows, macOS, Linux 上运行。
* **可配置:** 大部分样式（字体、颜色、大小比例、位置百分比）都可以通过修改脚本顶部的配置项进行调整。

## 效果示例

(这里你可以放一张最终生成的效果图链接，或者直接描述效果)

脚本处理后的图片大致效果如下：
原始图片变为黑白，底部覆盖一层半透明的黑色倾斜蒙层，蒙层上方偏右位置有两行文字，第一行是彩色的艺术字人名，第二行是稍小的白色 "Collection" 字样。字体大小和位置会根据原图分辨率自适应调整。

## 依赖需求

1.  **Python 3.x:** 脚本是用 Python 3 编写的。需要先安装 Python 环境。([下载 Python](https://www.python.org/downloads/))
2.  **ImageMagick 7.x:** 这是核心的图像处理库。
    * 需要下载并安装 ImageMagick。([下载 ImageMagick](https://imagemagick.org/script/download.php))
    * **重要:** 在安装 ImageMagick 时，请务必勾选 **"Add application directory to your system path"** (或类似选项)，以便脚本能直接调用 `magick` 命令。安装后可以在命令行输入 `magick -version` 检查是否安装成功并加入了 PATH。

## 所需文件

要运行此脚本，你需要准备好以下文件，并将它们放在**同一个文件夹**下（或者在脚本中指定完整路径）：

1.  **`process_script.py`:** 本脚本文件（就是你提供的代码）。
2.  **`overlay_shape_fullwidth.png`:** **蒙层模板图片**。这是一个**关键**文件，需要你自己预先制作（推荐使用 Photoshop, GIMP 等工具）：
    * 它必须是一个 **PNG** 文件。
    * 背景必须是**完全透明**的。
    * 内容是**横跨整个画布宽度**的、底部对齐的、顶边向上倾斜的**半透明黑色**形状。
    * 推荐宽度设置为主流海报宽度（如 2000 像素），高度根据需要的蒙层范围设置（如 400-500 像素）。
    * **导出时不要裁切画布**，要保留完整的宽度和透明区域。
3.  **字体文件:** 脚本中指定的字体文件：
    * **艺术字体:** 默认为 `GreatVibes-Regular.ttf` (你需要下载这个字体或替换为你选择的其他艺术字体文件)。
    * **"Collection" 字体:** 默认为 `JosefinSans-LightItalic.ttf` (你需要下载这个字体或替换为你选择的其他合适的、最好是窄体的常规字体文件)。

## 安装与设置

1.  确保你的系统已经安装了 Python 3 和 ImageMagick 7 (并且 `magick` 命令在系统 PATH 中)。
2.  下载 (或复制) `process_script.py` 脚本文件。
3.  制作 `overlay_shape_fullwidth.png` 蒙层模板文件，并将其与脚本放在同一目录。
4.  下载所需的 `.ttf` 或 `.otf` 字体文件 (`GreatVibes-Regular.ttf` 和 `JosefinSans-LightItalic.ttf` 或你选择的替代字体)，并将它们也放在脚本所在的目录。
5.  **配置脚本:** 打开 `process_script.py` 文件，找到顶部的 `# --- 配置项 ---` 部分，根据你的实际情况修改：
    * `OVERLAY_TEMPLATE_PATH`: 确认蒙层文件名正确。
    * `COLOR_PALETTE`: 你可以修改这个列表，添加或删除你喜欢的颜色代码。
    * `FONT_PATH`: **必须**修改为你实际使用的艺术字体文件的**路径或文件名** (如果在同一目录)。
    * `FONT_PATH_COLLECTION`: **必须**修改为你实际使用的 "Collection" 字体的**路径或文件名**。
    * **【重要调优参数】** 以下参数**强烈建议**你通过**反复试验**来调整，以达到最佳视觉效果：
        * `FONT_SIZE_RATIO_LINE1`, `FONT_SIZE_RATIO_LINE2`: 控制两行文字相对于图片高度的大小比例。数值越大，字越大。
        * `TEXT_OFFSET_X_PERCENT_LINE1`, `TEXT_OFFSET_Y_PERCENT_LINE1`: 控制第一行文字的位置（相对于底部中心，X% 向右，Y% 向上）。
        * `TEXT_OFFSET_X_PERCENT_LINE2`, `TEXT_OFFSET_Y_PERCENT_LINE2`: 控制第二行文字的位置。通常 X% 与第一行保持一致，Y% 比第一行小很多。
    * `MAGICK_CMD`: 确认 ImageMagick 的命令是 `magick` (通常 Windows/Linux/macOS 较新版本都是这个) 还是 `convert` (旧版本)。

## 使用方法

在配置好脚本并准备好所有必需文件后，打开你的**命令行终端** (Terminal, CMD, PowerShell 等)，切换到脚本所在的目录，然后使用以下命令格式运行：

```bash
python process_script.py <图片路径> "<人物名称>"
```

**参数说明:**

- `<图片路径>`: 你要处理的原始图片文件的完整路径或相对路径。
- `"<人物名称>"`: 你想要显示在图片上的名字或文本。**如果名称包含空格，请务必用英文双引号 `""` 将其括起来！**

**示例:**

Bash

```
# 处理当前目录下的 a.jpg，名字是 "Jackie Chan"
python process_script.py a.jpg "Jackie Chan"

# 处理 D 盘某个文件夹下的 b.png，名字是 "Tony Leung Chiu-wai"
python process_script.py "D:/Movies/Posters/b.png" "Tony Leung Chiu-wai"

# 在 PowerShell 中处理带空格路径的图片
python .\process_script.py ".\image with space.jpg" "Some Name"
```

脚本执行成功后，会在**原始图片所在的目录下**生成一个新的图片文件，文件名是在原文件名的基础上加上了配置的 `OUTPUT_SUFFIX` (默认为 `_styled_final`)，并且强制保存为 **PNG** 格式（以保证质量和透明度效果）。例如，处理 `a.jpg` 会生成 `a_styled_final.png`。

## 注意事项

- **参数调优:** 获得理想视觉效果的关键在于耐心调整脚本配置区的字体大小比例和文字偏移百分比。这是一个需要反复运行脚本、查看效果、再调整参数的过程。
- **文件路径:** 确保脚本中配置的所有文件路径（蒙层、字体）都是正确的，并且脚本有读取这些文件的权限。如果字体或蒙层文件与脚本不在同一目录，请使用绝对路径或正确的相对路径。
- **ImageMagick 版本:** 脚本基于 ImageMagick 7 的 `magick` 命令编写。如果你使用的是非常旧的 ImageMagick 6，可能需要将 `MAGICK_CMD` 改为 `"convert"`，并且某些命令参数可能需要微调。
- **输入图片:** 脚本目前假设输入的是单帧图片。对于 GIF 动图或多页 TIFF 等，它只处理第一帧 (`[0]`)。
- **临时文件:** 脚本在运行时会生成一个临时的缩放后蒙层文件 (`_temp_overlay.png`)，处理完成后会自动尝试删除。如果脚本意外中断，可能需要手动删除这个临时文件。
- **错误处理:** 脚本包含基本的错误检查（文件是否存在、命令是否找到、ImageMagick 是否报错），请留意命令行的输出信息。
