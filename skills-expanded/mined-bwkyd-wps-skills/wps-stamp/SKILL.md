---
name: wps-stamp
description: |
  电子印章制作。生成中国式圆形公章、合同章、财务章的PNG透明图片，
  用于设计稿和文档模板中标注盖章位置。仅供设计稿用途，不可替代真实印章。
  用于帮助用户生成印章效果图。当用户提到印章、公章、盖章时触发。
  Chinese-style electronic stamp image generator for design mockups.
license: MIT
user-invocable: true
argument-hint: '[单位名称] [印章类型]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 电子印章生成
  description_zh: 生成中国式圆形公章、合同章、财务章图片
  tags:
    - 印章
    - 签章
    - 图片
    - 设计
    - WPS
  version: 1.0.1
  license: MIT
---

# 电子印章生成器

输入单位名称 → 生成规范的中国式电子印章图片。

> **免责声明**：生成的印章仅供设计稿/样本/模板标注使用，不具有法律效力，
> 不可用于伪造公文或合同。如需正式电子签章请使用国家认可的CA认证服务。

## When to Use

- 文档模板/样本中需要印章占位
- 设计稿中需要印章效果图
- 内部演示文档标注用印位置
- 用户说"帮我生成个电子章""做个印章图片"

## When NOT to Use

- 正式法律文件盖章 → 使用CA认证电子签章服务
- 公文排版 → 使用 `wps-gongwen`（只标注位置）

## 印章类型

```text
[1] 圆形公章 → 单位全称环绕 + 中间五角星
[2] 椭圆合同章 → "XX合同专用章"
[3] 方形财务章 → "财务专用章"
[4] 方形法人章 → 法人姓名
[5] 圆形部门章 → 部门名称
```

## 工作流程

### Step 1: 确认印章信息

- **单位名称**
- **印章类型**（公章/合同章/财务章/法人章）
- **附加文字**（编码、日期等，可选）

### Step 2: 生成印章图片

```python
from PIL import Image, ImageDraw, ImageFont
import math
import os

def create_stamp(name, stamp_type='公章', output_path=None):
    """生成电子印章图片"""
    size = 400
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    center = size // 2
    color = (220, 30, 30, 230)  # 红色

    if stamp_type == '公章':
        # 外圆
        margin = 15
        draw.ellipse([margin, margin, size-margin, size-margin],
                     outline=color, width=6)

        # 五角星
        star_r = 45
        points = []
        for i in range(5):
            angle = math.radians(-90 + i * 72)
            points.append((center + star_r * math.cos(angle),
                          center + star_r * math.sin(angle)))
            angle2 = math.radians(-90 + i * 72 + 36)
            points.append((center + star_r * 0.38 * math.cos(angle2),
                          center + star_r * 0.38 * math.sin(angle2)))
        draw.polygon(points, fill=color)

        # 环绕文字
        try:
            font = ImageFont.truetype('/System/Library/Fonts/STHeiti Light.ttc', 28)
        except (OSError, IOError):
            font = ImageFont.load_default()

        radius = size // 2 - 40
        total_angle = len(name) * 22
        start_angle = 270 - total_angle // 2

        for i, char in enumerate(name):
            angle = math.radians(start_angle + i * 22)
            x = center + radius * math.cos(angle)
            y = center + radius * math.sin(angle)

            char_img = Image.new('RGBA', (40, 40), (0, 0, 0, 0))
            char_draw = ImageDraw.Draw(char_img)
            char_draw.text((5, 2), char, fill=color, font=font)
            rotated = char_img.rotate(-math.degrees(angle) - 90,
                                      expand=True, resample=Image.BICUBIC)
            paste_x = int(x - rotated.width // 2)
            paste_y = int(y - rotated.height // 2)
            img.paste(rotated, (paste_x, paste_y), rotated)

    elif stamp_type in ['财务章', '法人章']:
        # 方形章
        margin = 60
        draw.rectangle([margin, margin, size-margin, size-margin],
                       outline=color, width=5)
        try:
            font = ImageFont.truetype('/System/Library/Fonts/STHeiti Light.ttc', 42)
        except (OSError, IOError):
            font = ImageFont.load_default()

        text = name if stamp_type == '法人章' else f"{name}\n财务专用章"
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((center - tw//2, center - th//2), text,
                  fill=color, font=font)

    if not output_path:
        output_path = f'{name}_{stamp_type}.png'
    img.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 交付

1. 生成透明背景PNG图片
2. 建议尺寸和使用方式
3. 重申免责声明

## 在WPS文档中使用印章图片

```text
使用方法：
1. 插入 → 图片 → 选择生成的印章PNG
2. 图片格式 → 环绕方式 → 浮于文字上方
3. 调整大小（建议4cm × 4cm）
4. 拖动到落款位置（略偏右下盖住部分文字）
```

## 示例

```bash
# 公章
/wps-stamp XX科技有限公司 公章

# 合同章
/wps-stamp XX集团 合同章

# 法人章
/wps-stamp 张三 法人章
```
