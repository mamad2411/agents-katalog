---
name: bilibili-audio
description: 下载B站视频音频。支持单个视频下载和批量下载UP主所有视频。当用户提供B站视频链接（bilibili.com、b23.tv）、要求下载B站音频、下载B站视频、提取B站音频、或批量下载某个UP主的视频时使用。触发词：B站下载、bilibili下载、下载B站音频、B站音频、哔站下载。
user-invocable: true
---

# B站音频下载

下载B站视频音频，支持单个视频和批量UP主下载。

## 输入识别

根据用户输入自动判断模式：

| 输入类型 | 示例 | 模式 |
|---------|------|------|
| 视频URL | `https://www.bilibili.com/video/BVxxx` | 单个下载 |
| 短链接 | `https://b23.tv/xxx` | 单个下载 |
| 用户ID | `593926706` | 批量下载 |
| UP主链接 | `https://space.bilibili.com/593926706` | 批量下载 |

## 单个视频下载

当用户提供视频链接时：

```bash
mkdir -p ~/B站音频下载

BBDown --audio-only \
  --work-dir ~/B站音频下载 \
  -F '<publishDate>_<videoTitle>_<bvid>' "<视频URL>"

open ~/B站音频下载/
```

报告下载结果：标题、时长、文件大小、保存路径。

## 批量UP主下载

当用户提供用户ID或UP主空间链接时：

### 1. 提取用户ID

从 `https://space.bilibili.com/593926706` 提取 `593926706`。

### 2. 获取视频列表（推荐方法：使用 BBDown）

使用 BBDown 的 debug 模式获取视频列表，无需硬爬 API：

```bash
SCRIPT_DIR="$(dirname "$0")"
python3 ~/.claude/skills/bilibili-audio/scripts/bbdown_space_crawler.py <用户ID> ~/bilibili_<用户ID>_videos.csv
```

**原理说明：**
- BBDown 在解析 UP主空间投稿页面时会获取完整的视频列表
- 通过 `--debug` 参数可以输出原始 JSON 数据
- 脚本从 debug 输出中提取 bvid 和标题信息
- 此方法使用 BBDown 的内置能力，更加稳定可靠
- **支持获取隐藏空间的视频列表**（即使 UP主设置了隐私保护）
- 使用 `/upload/video` 页面绕过部分 412 限制

### 3. 提取视频URL

```bash
tail -n +2 ~/bilibili_<用户ID>_videos.csv | cut -d',' -f3 > ~/bilibili_<用户ID>_videos.txt
```

### 4. 创建下载目录

```bash
mkdir -p ~/B站音频下载/<用户ID>
```

### 5. 批量下载（随机间隔防封禁）

```bash
while read url; do
  echo "=== 下载: $url ==="
  BBDown --audio-only --save-archives-to-file \
    --work-dir ~/B站音频下载/<用户ID> \
    -F '<publishDate>_<videoTitle>_<bvid>' "$url"
  delay=$((RANDOM % 6 + 3))
  echo "等待 $delay 秒..."
  sleep $delay
done < ~/bilibili_<用户ID>_videos.txt
```

### 6. 完成

```bash
open ~/B站音频下载/<用户ID>/
```

报告下载数量和失败情况。

## 功能特性

- 最高音质（自动选择最高码率）
- 自动跳过已下载视频
- 字幕自动嵌入（如可用）
- 文件命名：日期_标题_BV号.m4a
- 随机间隔（3-8秒）防封禁，模拟人类行为
- 使用 BBDown 内置能力获取视频列表，稳定可靠

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 未安装 BBDown | brew install BBDown |
| Cookie 过期 | 重新登录B站更新 cookie |
| 视频不可用 | 可能被删除或会员专享 |
| 重新下载已跳过的 | rm -f ~/tools/BBDown.archives |
| 获取视频列表失败 | 检查 BBDown 是否已登录 |
