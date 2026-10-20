---
name: image-steganography
version: 2.0.0
description: "识别与破解图片隐写（steganography）。当任务涉及图片中可能藏有隐藏文件 / flag / 附加数据、LSB 位平面隐写、EXIF/元数据线索、文件尾追加、PNG 高度/宽度被改、通道/位平面分析、二维码隐藏、GIF/APNG 多帧、JPEG steghide 口令隐写、盲水印/频域，或对可疑图片做取证、解 CTF Misc/Stego 题时使用。流程化：先判图片真实类型，再按隐写类型逐层穷举；以自带 Python(uv run) 脚本为主，zsteg/exiftool/steghide 等便携工具可用时优先调用。"
author: honglian
---

# 图片隐写识别与破解

帮助对一张可疑图片完成**隐写排查**：判断里面是否藏了文件、flag、附加数据或隐写信息，并给出提取办法。
适用于数字取证中的可疑图片分析，以及 CTF 的 Misc/Stego 题。

**方法论：先判类型，再按隐写类型逐层穷举。** 现成工具（zsteg/Stegsolve/binwalk）只是把常见思路打包；底层都是「遍历参数 → 抽数据 → 看是否可读」。本 skill 以**自带 Python 写脚本穷举**为主干，不被「工具装没装」卡住。

---

## 何时使用

- 怀疑图片里藏了另一个文件（压缩包、文本、第二张图、可执行文件）
- 找隐藏的 flag / 口令 / 坐标 / URL / 二维码
- 图片打开正常但「体积异常偏大」「显示不全」「来路不明」「题目暗示有隐藏内容」
- 需要分析 EXIF/元数据、LSB 位平面、颜色通道、文件尾追加、PNG 尺寸篡改、GIF 帧、盲水印

---

## 运行环境（重要）

本应用运行在 **Windows**，`exec` 工具用 **PowerShell 语法**。

- **跑 Python 脚本一律用 `uv run`**：`uv` 已随包提供并在 PATH 上，`uv run` 会自动按脚本头部声明装好依赖（pillow / numpy 等），离线即用，**无需你先 `pip install`**：
  ```powershell
  uv run "<skill 目录>\scripts\identify.py" .\suspect.png
  ```
  `<skill 目录>` 用本 skill 的真实绝对路径替换。脚本会把提取产物写到 `.\<图名>_steg\` 输出目录。
- **第三方便携工具按需调用**：zsteg / exiftool / binwalk / steghide / stegseek / pngcheck 若已放进应用 `tools\` 目录（在 PATH 上）或系统 PATH，可直接调用，效果更强；**没装也不影响**——核心能力都有 Python 脚本兜底。
- 工具的调用方式与平台无关（`zsteg -a a.png` 在哪都一样）；只有「循环、管道、重定向」才按 PowerShell 写。

> ⚠️ **取证完整性**：**先对原图算哈希（`Get-FileHash`），再在原图上只读分析**（脚本/工具都不写原图），不要改证据原件、也不必复制原图。所有提取/分离产物写到 workspace 里的独立输出目录。

---

## 排查流程

### 步骤 0 · 取证完整性
```powershell
Get-FileHash .\suspect.png -Algorithm SHA256    # 先留存原图哈希
```
先算哈希留证，然后**直接在原图上只读分析**——下面所有脚本/工具都只读原图，产物一律写到独立输出目录，**无需复制原图**。若某工具（如 `binwalk -e`）默认把提取物落在输入文件同级目录，就把 `exec` 的 `cwd` 设成你 workspace 的输出目录，别污染证据目录。

### 步骤 1 · 判断图片真实类型（先做这步）
扩展名会骗人，结构异常本身就是线索。
```powershell
uv run "<skill 目录>\scripts\identify.py" .\suspect.png
```
`identify.py` 报告：真实格式 vs 扩展名是否对不上、尺寸、颜色类型、**IEND/FFD9 后的追加数据**、多图拼接（多个文件签名）、文本块/调色板/APNG 等结构特征、以及 **PNG 高度疑似被改**——并据此建议优先试哪些技法。

### 步骤 2 · 按隐写类型逐层排查
按下表逐个试；一个没结果**不代表没隐写**，换一个继续，常见是「尾部追加 + LSB」等多手法叠加。

| # | 隐写类型 | 首选（Python，自带） | 适用格式 | 便携工具更强（若可用） |
|---|----------|----------------------|----------|------------------------|
| 1 | **LSB / 位平面** | `uv run "<skill 目录>\scripts\lsb_scan.py" .\suspect.png --show-best` | PNG/BMP/GIF | `zsteg -a .\suspect.png` |
| 2 | **EXIF / 元数据** | `uv run "<skill 目录>\scripts\exif_dump.py" .\suspect.jpg` | 全部 | `exiftool -a -G1 -u .\suspect.jpg` |
| 3 | **文件尾追加 / 内嵌** | `uv run "<skill 目录>\scripts\carve.py" .\suspect.png` | 全部 | `binwalk -e .\suspect.png` |
| 4 | **PNG 高度/宽度篡改** | `uv run "<skill 目录>\scripts\png_height_fix.py" .\suspect.png` | PNG | `pngcheck -v .\suspect.png`（先确认 CRC 错） |
| 5 | **通道 / 位平面分析** | `uv run "<skill 目录>\scripts\bit_planes.py" .\suspect.png` | PNG/BMP | （Stegsolve GUI，需人工查看时） |

**扩展技法**（按线索触发）：

| 隐写类型 | 脚本 | 何时用 |
|----------|------|--------|
| **二维码 / 条码** | `uv run "<skill 目录>\scripts\qr_decode.py" .\suspect.png` | 图里有二维码/条码，或位平面导出后发现码图 |
| **GIF / APNG 多帧** | `uv run "<skill 目录>\scripts\frames.py" .\suspect.gif` | 动图，疑似某帧藏信息 / 逐帧编码 |
| **盲水印 / 频域** | `uv run "<skill 目录>\scripts\freq.py" .\suspect.png` | 题面提示水印 / 像素域查不到 / 看 FFT 幅度谱找周期图案 |

**JPEG 专项**（LSB 对 JPEG 无效，有损压缩会破坏像素低位）：
- 口令隐写是 JPEG 主向量，**优先用便携工具**（无 Python 等价、但单 exe 易打包）：
  ```powershell
  steghide info .\suspect.jpg              # 是否含 steghide 数据
  steghide extract -sf .\suspect.jpg -p "" # 空口令试一发
  stegseek .\suspect.jpg .\rockyou.txt     # 字典爆破口令
  ```
- EXIF 缩略图与主图不一致（藏图经典手法）：`exif_dump.py` 会自动提取缩略图；或 `exiftool -b -ThumbnailImage .\suspect.jpg -o thumb.jpg`。
- 多个 `FFD8` 拼接：`identify.py` 会报，`carve.py` 负责分离。

### 步骤 3 · 通用兜底：有思路就 `uv run` 现写脚本
**隐写破解的本质是「有思路就能穷举」。** 可穷举的维度：**通道、位平面、像素遍历顺序、比特序、起始偏移、按行/列、是否异或/再解码**。一个组合没结果就换一个维度继续，必要时多维度一起爆破。
`references\python-recipes.md` 提供可直接改的片段：通道分离、双图异或、拼图、像素值转文本、palette 隐写、单字节异或爆破、最小 LSB 提取等。

---

## per-format 清单（逐项核对）

**PNG**：① 真实格式/尺寸（identify）② IEND 后追加数据（carve）③ LSB/位平面（lsb_scan / bit_planes）④ tEXt/zTXt/iTXt 文本块（carve）⑤ 高度/宽度被改（png_height_fix）⑥ 调色板隐写（palette，见 recipes）⑦ APNG 多帧（frames）⑧ IDAT 异常/非常规 filter。

**JPEG**：① EXIF/Comment（exif_dump）② 缩略图≠主图（exif_dump）③ steghide/stegseek 口令隐写 ④ FFD9 后追加数据（carve）⑤ 多个 FFD8 拼接（identify→carve）。**不要对 JPEG 做像素 LSB**。

**GIF**：① 多帧逐帧（frames）② Comment Extension（carve/exif）③ 调色板 ④ 帧延迟编码。

**BMP**：① 无压缩、LSB 容量大（lsb_scan / bit_planes）② 像素行 padding 可藏数据 ③ 尾部追加（carve）。

---

## 套路速查（特征 → 解法）

| 套路 | 特征 | 解法 |
|------|------|------|
| PNG 高度被改 | 图显示不全 / pngcheck 报 CRC 错 | `png_height_fix.py`（爆破高/宽 + 导正 CRC） |
| LSB 隐写 | 图看着正常但有隐藏信息 | `lsb_scan.py --show-best`；PNG 另可 `zsteg -a` |
| EXIF 隐藏 | 元数据藏 flag/提示 | `exif_dump.py`（重点 Comment/Description/Artist/GPS） |
| 文件拼接/图后藏包 | 体积偏大 / 尾部有数据 | `carve.py`（IEND·FFD9 后数据 + 签名雕复 + 解码链） |
| Steghide 加密 | JPG，info 提示需口令 | 空口令 → `stegseek` 字典爆破（口令常在题面/文件名） |
| 通道隐写 | 某颜色通道异常 | `bit_planes.py` 导各通道×位平面 PNG 看 |
| 二维码隐藏 | 图中有码 / 某位平面是码图 | `qr_decode.py`（pyzbar） |
| 图片拼图 | 多张需拼接 | recipes 的「拼接」片段 |
| 像素值编码 | 像素值对应 ASCII | `lsb_scan.py --mode pixel`，或 recipes 像素转文 |
| GIF 帧分析 | 动图某帧藏信息 | `frames.py` 逐帧导出再逐张排查 |

---

## 常见线索模式（搜字符串时重点看）
`flag{` / `FLAG{` / `ctf` / `PK\x03\x04`(zip) / `Rar!`(rar) / `http(s)://` / base64 串（`[A-Za-z0-9+/]{20,}={0,2}`）/ 十六进制串 / Morse / 坐标。

## 联网可用时（在线整合工具，作交叉验证）
- **aperisolve.com**：一键跑 zsteg/steghide/binwalk/Stegsolve 并汇总。
- **stegonline.net**：在线 LSB / 位平面分析。
- **29a.ch/photo-forensics**：ELA 等图片取证。

## 注意事项
1. **先哈希、在原图上只读分析**（产物写独立目录），保护证据原件，无需复制原图。
2. 一个工具/脚本没结果 ≠ 没隐写，**多种手法叠加排查**（尤其「尾部追加 + LSB」组合）。
3. 找到疑似数据再判编码：base64 / hex / 压缩包 / 进一步隐写（**套娃常见**）。
4. 所有提取产物集中放到独立输出目录，便于归档与复核。
