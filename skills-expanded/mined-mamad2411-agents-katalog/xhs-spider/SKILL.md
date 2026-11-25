---
name: xhs-spider
description: 小红书（XHS）数据采集 CLI 工具，支持笔记抓取、用户数据采集、内容搜索
---

# xhs-spider

小红书（XHS）数据采集 CLI 工具

---

## Skill Metadata

**Name:** xhs-spider
**Type:** CLI Tool
**Language:** TypeScript/Node.js
**Repository:** https://github.com/DivXPro/xhs-spider

---

## Triggers

Invoke this skill when:
- 用户请求获取小红书笔记数据
- 用户请求搜索小红书内容
- 用户请求采集小红书用户笔记
- 用户提到 xhs、小红书、数据采集、笔记爬虫

---

## Related Skills

**评论商业价值分析** - 位于 `reference/SKILL-comment-analysis.md`
- 分析小红书评论数据
- 生成量化汇总报告
- 包含情感分析、话题分类、购买意向等维度

---

## Installation

```bash
# 从 npm 安装（推荐）
npm install -g xhs-spider

# 安装后即可使用全局命令
xhs --help
```

---

## Environment Setup

执行 CLI 前需要从配置文件读取 `XHS_COOKIES` 并注入环境变量。

### 配置文件格式

`.claude/settings.env` 文件内容：
```
XHS_COOKIES="你的小红书cookies字符串"
```

### 自动注入环境变量

**Linux / macOS:**
```bash
# 先导入环境变量，再执行命令
export "$(grep '^XHS_COOKIES=' .claude/settings.env)" && XHS_COOKIES="${XHS_COOKIES//\"/}" && xhs note "url"
```

**Windows (CMD):**
```cmd
for /f "tokens=1,2 delims==" %i in ('findstr XHS_COOKIES .claude\settings.env') do @set %i=%~j && xhs note "url"
```

**Windows (PowerShell):**
```powershell
$c = Get-Content .claude/settings.env | Where-Object { $_ -match '^XHS_COOKIES=' }; $p = $c -split '=', 2; $v = $p[1].Trim([char]34); [Environment]::SetEnvironmentVariable($p[0], $v, 'Process'); xhs note "url"
```

---

## Quick Start

```bash
# 1. 设置 cookies（方式一：环境变量）
export XHS_COOKIES="你的小红书cookies"

# 2. 获取笔记详情
xhs note "https://www.xiaohongshu.com/explore/xxx"

# 3. 搜索笔记
xhs search "美食" -n 20 -f table
```

---

## Commands

| 命令 | 说明 |
|------|------|
| `xhs note <url>` | 获取单个笔记详情 |
| `xhs user <url>` | 获取用户的所有笔记 |
| `xhs search <query>` | 搜索笔记 |
| `xhs creator` | 获取创作者发布的笔记 |
| `xhs comment <url>` | 获取笔记的评论 |

---

## Command Options

### 全局参数（所有命令可用）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-c, --cookies <cookies>` | XHS cookies | - |
| `-f, --format <format>` | 输出格式：json/table/csv/md | json |
| `--download` | 下载笔记媒体文件 | false |

### note 命令

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--download` | 下载笔记的图片/视频 | false |
| `--refresh` | 强制从网络重新获取最新数据 | false |

### user 命令

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-n, --num <数量>` | 获取笔记数量 | 100 |
| `--download` | 下载笔记的图片/视频 | false |

### search 命令

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-n, --num <数量>` | 搜索数量 | 10 |
| `--sort <0-4>` | 排序方式 | 0 |
| `--type <0-2>` | 笔记类型 | 0 |
| `--time <0-3>` | 笔记时间 | 0 |
| `--download` | 下载笔记的图片/视频 | false |

**sort 参数值：**
- `0` - 综合排序
- `1` - 最新
- `2` - 最多点赞
- `3` - 最多评论
- `4` - 最多收藏

**type 参数值：**
- `0` - 不限
- `1` - 视频笔记
- `2` - 普通笔记

**time 参数值：**
- `0` - 不限
- `1` - 一天内
- `2` - 一周内
- `3` - 半年内

### comment 命令

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--download` | 保存评论到本地 YAML 文件 | false |

---

## Output Formats

| 格式 | 说明 | 适用场景 |
|------|------|----------|
| `json` | JSON 美化输出 | 程序处理 |
| `table` | 制表符分隔 | 控制台查看 |
| `csv` | CSV 格式 | Excel 导入 |
| `md` | Markdown 表格 | 文档使用 |

---

## Configuration

### Cookies 配置（必填）

Cookies 优先级（从高到低）：

1. **命令行参数**
   ```bash
   xhs note "url" -c "cookies字符串"
   ```

2. **环境变量**
   ```bash
   export XHS_COOKIES="cookies字符串"
   xhs note "url"
   ```

3. **.env 文件**
   ```
   XHS_COOKIES=cookies字符串
   ```

### 获取 Cookies

1. 打开浏览器，登录小红书
2. 按 F12 打开开发者工具
3. 切换到 Network 标签
4. 刷新页面，任意请求中找到 Cookie 请求头
5. 复制完整 cookie 字符串

---

## Examples

```bash
# 获取笔记详情（JSON 输出）
xhs note "https://www.xiaohongshu.com/explore/xxx"

# 表格形式显示
xhs note "https://www.xiaohongshu.com/explore/xxx" -f table

# 获取笔记详情（强制刷新）
xhs note "https://www.xiaohongshu.com/explore/xxx" --refresh

# 下载笔记媒体
xhs note "https://www.xiaohongshu.com/explore/xxx" --download

# 搜索最新笔记
xhs search "榴莲" -n 20 --sort 1

# 搜索视频笔记
xhs search "美食" --type 1 --sort 2 -f csv

# 获取用户笔记
xhs user "https://www.xiaohongshu.com/user/profile/xxx" -n 50

# 获取笔记评论
xhs comment "https://www.xiaohongshu.com/explore/xxx"

# 获取评论并保存到本地
xhs comment "https://www.xiaohongshu.com/explore/xxx" --download

# Markdown 格式导出
xhs search "旅游攻略" -n 30 -f md > results.md
```

---

## Data Output

下载的媒体文件保存在 **项目根目录** 下的 `datas/media_datas/{笔记ID}/` 目录，包含：
- `note.yaml` - 笔记完整信息（YAML 格式，程序处理用）
- `NOTE.md` - 笔记 Markdown 详情
- `comments.yaml` - 评论数据（使用 `--download` 参数时生成）
- `image_0.jpg`, `image_1.jpg` - 图片
- `video.mp4` - 视频（如果有）

**注意**：Agent 执行命令时需确保运行在项目根目录（`package.json` 所在目录），而非 `.claude/` 目录，否则数据会保存到错误位置。

---

## Data Fetching Strategy

**获取笔记数据时，优先从本地数据文件夹读取，除非明确要求获取最新数据。**

### 读取优先级

1. **优先读取本地数据** - 当笔记已下载过时，优先从 `datas/media_datas/{笔记ID}/note.yaml` 读取
2. **按需抓取最新数据** - 仅当用户明确要求（添加 `--refresh`、`--force` 或 `--latest` 等参数）时，才重新从网络抓取

### 适用场景

- 查看历史下载的笔记数据
- 避免重复请求，提高响应速度
- 减少对小红书服务器的压力

### 强制刷新

如需获取最新数据，请使用 `--refresh` 参数：

```bash
xhs note "https://www.xiaohongshu.com/explore/xxx" --refresh
```
