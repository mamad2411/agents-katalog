---
name: gif-splitter
description: GIF动图切分工具，将超过指定帧数的GIF文件自动拆分成多个小文件。适用于微信公众号等平台上传GIF时遇到"帧数超限"的问题。
---

# GIF 动图切分工具

## 概述

这个技能用于解决上传GIF到微信公众号等平台时遇到的"图片帧数超过300帧"限制问题。它会自动检测GIF帧数，并将超限的GIF智能切分成多个符合要求的小文件。

## 使用场景

当用户遇到以下情况时触发此技能：
- 上传GIF到微信公众号提示"帧数超过300帧"
- 需要将大GIF拆分成多个小GIF
- 需要检查GIF文件的帧数信息
- 需要将GIF拆分后确保每个文件不超过指定大小

## 快速开始

当用户需要切分GIF时，运行以下脚本：

```bash
# 切分单个GIF文件（默认最大280帧）
python3 ~/.claude/skills/jiamu-skills/gif-splitter/scripts/split_gif.py "GIF文件路径"

# 切分文件夹中所有GIF
python3 ~/.claude/skills/jiamu-skills/gif-splitter/scripts/split_gif.py "文件夹路径"
```

输出目录：原文件所在目录下的 `split_output/` 文件夹

## 依赖环境

### 安装 Pillow

```bash
pip3 install Pillow
```

### 验证安装

```bash
python3 -c "from PIL import Image; print('Pillow 安装成功')"
```

## 使用命令

### 基础用法

```bash
# 切分单个文件
python3 scripts/split_gif.py "动图.gif"

# 切分整个文件夹
python3 scripts/split_gif.py ~/Desktop/gif文件夹/
```

### 自定义参数

```bash
# 指定最大帧数（默认280帧，微信限制300帧）
python3 scripts/split_gif.py "动图.gif" --max-frames 200

# 指定输出目录
python3 scripts/split_gif.py "动图.gif" -o ~/Desktop/output

# 仅查看GIF信息，不切分
python3 scripts/split_gif.py "动图.gif" --info

# 组合使用
python3 scripts/split_gif.py ~/gifs/ --max-frames 250 -o ~/output --info
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `path` | GIF文件或文件夹路径 | 必填 |
| `--max-frames`, `-m` | 每个输出文件的最大帧数 | 280 |
| `-o`, `--output` | 输出目录 | 原目录下的 `split_output/` |
| `--info` | 仅显示GIF信息，不执行切分 | False |

## 工作原理

### 切分算法

1. **读取GIF**：使用Pillow库读取GIF的所有帧和每帧的持续时间
2. **计算分片**：根据总帧数和最大帧数限制，计算需要切分的文件数量
3. **均匀分配**：将帧数均匀分配到各个输出文件，避免最后一个文件帧数过少
4. **保存输出**：保留原始帧率和循环设置，生成优化后的GIF文件

### 示例

原文件：`演示动画.gif`（740帧，5.7MB）

切分结果：
```
演示动画_第1部分.gif  (247帧, 约2MB)
演示动画_第2部分.gif  (247帧, 约2MB)
演示动画_第3部分.gif  (246帧, 约2MB)
```

## 平台限制参考

| 平台 | 帧数限制 | 文件大小限制 | 建议 `--max-frames` |
|------|----------|--------------|---------------------|
| 微信公众号 | 300帧 | 10MB | 280（默认） |
| 微信聊天 | 无明确限制 | 25MB | 根据需要 |
| 微博 | 无明确限制 | 20MB | 根据需要 |

## 常见问题

### 切分后文件比原文件大？

这是正常现象。原因：
1. 原GIF可能使用了全局调色板优化
2. 切分后每个文件需要独立的调色板
3. 帧间压缩效果降低

解决方案：适当增加 `--max-frames` 减少切分数量

### 切分后动画速度变了？

脚本会保留原始帧率。如果发现速度异常，可能是原GIF的帧时间信息不完整。

### 如何只查看GIF信息不切分？

```bash
python3 scripts/split_gif.py "动图.gif" --info
```

输出示例：
```
文件: 演示动画.gif
帧数: 740 帧
大小: 5.70 MB
尺寸: 800x600
状态: 需要切分（超过 280 帧）
```

## 输出格式

输出文件命名规则：`{原文件名}_第{序号}部分.gif`

例如：
- `演示.gif` → `演示_第1部分.gif`, `演示_第2部分.gif`

## 技术细节

- **库依赖**：Pillow (PIL)
- **Python版本**：3.6+
- **支持格式**：GIF（动态/静态）
- **输出优化**：启用GIF优化压缩
