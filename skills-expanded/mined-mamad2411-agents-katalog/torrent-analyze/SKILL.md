---
name: torrent-analyze
description: "自动触发并直接执行种子验车能力。适用于用户在任意上下文给出 magnet 链接、32/40 位种子 hash，或提到验车、磁链、种子分析、种子信息、种子详情、whatslink、截图返回、图片拼图、高斯模糊、中文方框、font.ttf、MapleMono、缓存、torrent_info_cache、分析失败、频率限制等场景。模型应主动从最近对话、粘贴文本或 stdin 中抽取磁链/hash，使用本 skill 自带脚本查询 whatslink.info、格式化种子信息、缓存结果，并可选生成文本头 + 最多 3 张截图的拼图；不再要求用户使用旧的 /验车、/种子分析、/种子信息、/种子详情 指令。"
---
# 种子验车

自包含的磁链 / 种子 hash 分析工具。skill 内自带 `scripts/torrent_analyze.py`，可直接查询 whatslink.info，输出原插件同款文本结果，并可选渲染“文本头 + 截图”的拼图。

后文 `$SKILL_DIR` 指本 skill 安装目录，例如 `<项目>/.codex/skills/torrent-analyze`、`<项目>/.claude/skills/torrent-analyze`、`<项目>/.agents/skills/torrent-analyze`。

## 自动触发

用户给出以下内容时，直接使用本 skill，不要再要求用户发送机器人旧指令，也不要要求用户把磁链固定写在“验车”后面：

- `magnet:?xt=urn:btih:...`
- 32 位或 40 位种子 hash
- 一整段聊天记录、日志、网页文本或 Markdown，其中夹带磁链 / hash
- 一次贴多条磁链 / hash
- “验车这个磁链”“查一下种子信息”“分析这个 hash”“有截图吗”“生成验车图”
- “分析失败”“whatslink 频率限制”“中文方框”“font.ttf”“MapleMono”“缓存在哪”

AI 要先从最近用户消息和对话上下文中找磁链或 hash。找到后直接调用脚本；如果文本很长，优先通过 stdin 把整段上下文交给脚本自动抽取。上下文里有多条时脚本会按出现顺序批量处理，重复 hash 只处理一次，默认最多处理 20 条。

## 快速命令

文本验车：

```bash
python3 "$SKILL_DIR/scripts/torrent_analyze.py" "<磁链或hash>"
```

从整段上下文自动抽取并验车：

```bash
printf '%s' "<包含磁链或hash的上下文文本>" | python3 "$SKILL_DIR/scripts/torrent_analyze.py" --stdin
```

生成截图拼图：

```bash
python3 "$SKILL_DIR/scripts/torrent_analyze.py" "<磁链或hash>" --image
```

输出 JSON 供后续处理：

```bash
python3 "$SKILL_DIR/scripts/torrent_analyze.py" "<磁链或hash>" --json
```

指定缓存目录：

```bash
python3 "$SKILL_DIR/scripts/torrent_analyze.py" "<磁链或hash>" --cache-dir .torrent-analyze
```

## 默认配置

默认配置写在 `$SKILL_DIR/config/default.env`，安装后直接改这个文件即可调整 skill 默认行为。

优先级：

```text
命令行参数 > shell 环境变量 > $SKILL_DIR/config/default.env > 脚本内置默认值
```

如需临时指定另一份配置文件：

```bash
TORRENT_ANALYZE_ENV_FILE=/path/to/torrent-analyze.env python3 "$SKILL_DIR/scripts/torrent_analyze.py" "<上下文或磁链>"
```

| 环境变量 | 默认值 | 对应参数 | 说明 |
|----------|--------|----------|------|
| `TORRENT_ANALYZE_CACHE_DIR` | `.torrent-analyze` | `--cache-dir` | 缓存和渲染输出目录 |
| `TORRENT_ANALYZE_RETRY_TIMES` | `20` | `--retry-times` | whatslink 请求最大重试次数，脚本裁剪到 `1..60` |
| `TORRENT_ANALYZE_RETRY_INTERVAL` | `3.0` | `--retry-interval` | 重试间隔秒数，脚本裁剪到 `0.5..30.0` |
| `TORRENT_ANALYZE_MAX_ITEMS` | `20` | `--max-items` | 从上下文最多处理的磁链/hash数量，脚本裁剪到 `1..20` |
| `TORRENT_ANALYZE_IMAGE` | `false` | `--image` | 是否默认生成截图拼图 |
| `TORRENT_ANALYZE_BLUR` | `5` | `--blur` | 图片高斯模糊半径，脚本裁剪到 `0..10` |
| `TORRENT_ANALYZE_FONT_FILE` | 空 | `--font-file` | 字体文件绝对路径，优先级最高 |
| `TORRENT_ANALYZE_FONT_DIR` | `/AstrBot/data/fonts` | `--font-dir` | 字体查找目录 |
| `TORRENT_ANALYZE_FONT_FILENAME` | 空 | `--font-filename` | 指定字体文件名；为空时优先查找 `font.ttf` |
| `TORRENT_ANALYZE_AUTO_DOWNLOAD_FONT` | `true` | `--auto-download-font` / `--no-auto-download-font` | 找不到本地中文字体时是否自动下载 |
| `TORRENT_ANALYZE_FONT_URL` | Noto Sans CJK SC | `--font-url` | 自动下载字体 URL |
| `TORRENT_ANALYZE_FONT_CACHE_DIR` | 空 | `--font-cache-dir` | 自动下载字体缓存目录；空值表示 `<cache-dir>/fonts` |
| `TORRENT_ANALYZE_FONT_CACHE_FILENAME` | `NotoSansCJKsc-Regular.otf` | `--font-cache-filename` | 自动下载字体缓存文件名 |
| `TORRENT_ANALYZE_JSON` | `false` | `--json` | 是否默认输出 JSON |
| `TORRENT_ANALYZE_NO_CACHE` | `false` | `--no-cache` | 是否默认禁用缓存 |

示例：

```bash
# 持久默认值：编辑 skill 自带配置文件
$EDITOR "$SKILL_DIR/config/default.env"

# 单次覆盖：直接用 shell 环境变量或命令行参数
printf '%s' "<上下文文本>" | TORRENT_ANALYZE_IMAGE=1 TORRENT_ANALYZE_BLUR=6 \
  python3 "$SKILL_DIR/scripts/torrent_analyze.py" --stdin
```

## AI 行为约定

| 用户说 | AI 动作 |
|--------|---------|
| “验车 / 查一下 / 分析一下”，磁链在上下文里 | 从最近上下文提取，或 `printf '%s' "<上下文>" \| torrent_analyze.py --stdin` |
| “验这一堆 / 批量查 / 多个磁链” | 把整段上下文交给脚本，默认最多处理 20 条；需要更少时传 `--max-items <数量>` |
| “验车 <磁链/hash>” | 直接跑 `torrent_analyze.py "<磁链/hash>"`，把文本结果回给用户 |
| “带图 / 截图 / 拼图 / 高斯” | 跑 `torrent_analyze.py "<上下文或磁链>" --image`；除非用户临时指定模糊值，否则不要额外传 `--blur` |
| “JSON / 原始结果 / 调试接口” | 跑 `torrent_analyze.py "<上下文或磁链>" --json` |
| “频率限制 / quota_limited” | 调整 `--retry-times` 和 `--retry-interval` 后重试，说明 whatslink.info 可能限流 |
| “不要缓存 / 强制刷新” | 加 `--no-cache` |
| “中文方框 / 字体问题” | 默认会自动下载 Noto Sans CJK SC；如需固定字体，指定 `TORRENT_ANALYZE_FONT_FILE` 或 `--font-file` |

AI 不要做：

- 不要告诉用户再去发 `/验车`、`/种子分析`、`/种子信息`、`/种子详情`；这些只是原 AstrBot 插件命令，本 skill 的目标是替代该交互入口。
- 不要要求用户重复提供磁链；只要最近上下文里已有 magnet/hash，就主动抽取。
- 不要手写 curl 拼 whatslink URL；统一使用脚本，避免编码、重试、缓存、格式化逻辑分叉。
- 不要把图片渲染失败当成整个分析失败；脚本会保留文本结果。
- 不要把 `.torrent-analyze/` 缓存和渲染产物提交进 git。

## 能力说明

脚本内置原仓库核心能力：

- 支持 32/40 位 hash 与 `magnet:?xt=urn:btih:`。
- 支持从任意上下文文本或 stdin 中自动抽取多条 magnet/hash，按出现顺序处理并对重复 hash 去重。
- 批量处理默认最多 20 条，可用 `TORRENT_ANALYZE_MAX_ITEMS` 或 `--max-items` 调整；脚本会裁剪到 `1..20`。
- 请求 `https://whatslink.info/api/v1/link`，使用浏览器风格 headers。
- 对 `quota_limited` 和临时请求失败按参数重试。
- 格式化输出：种子哈希、文件类型、种子名称、总大小、文件总数。
- 只缓存 `error == ""` 且 `type != "UNKNOWN"` 的结果。
- 最多提取 3 张截图。
- 可选下载截图、应用高斯模糊、拼接文本头并输出 JPG。
- 字体优先级：`TORRENT_ANALYZE_FONT_FILE` / `--font-file` → `--font-filename` → `font.ttf` → MapleMono 候选 → 系统中文字体 → 自动下载 Noto Sans CJK SC → Pillow 默认字体。
- 自动下载的字体默认缓存到 `.torrent-analyze/fonts/NotoSansCJKsc-Regular.otf`；改 `TORRENT_ANALYZE_FONT_CACHE_DIR` 可调整位置，改 `TORRENT_ANALYZE_AUTO_DOWNLOAD_FONT=false` 可关闭。

## 依赖

- 必需：`httpx`
- 仅 `--image` 必需：`Pillow`

缺依赖时安装：

```bash
python3 -m pip install httpx Pillow
```

## 数据位置

默认在当前工作目录写运行数据：

```text
.torrent-analyze/
├── torrent_info_cache.json
├── fonts/
│   └── NotoSansCJKsc-Regular.otf
└── rendered/
    └── torrent_<hash>.jpg
```

可用 `--cache-dir <dir>` 改位置。

## 输出要求

给用户回复时优先精简：

```markdown
**验车结果**
<脚本文本输出的核心 5 行>

来源：<缓存 / whatslink.info>
截图：<无 / N 张 / 图片路径>
```

如果脚本返回失败：

- 输入无效：直接说明“这不是有效磁链或 32/40 位 hash”。
- `quota_limited`：说明 whatslink.info 当前限流，可稍后重试或调大重试间隔。
- 缺依赖：给出安装命令。
- 图片失败但文本成功：只返回文本，并说明截图渲染未成功。

## 反模式

- 把这个 skill 当成“维护说明文档”而不执行脚本。
- 继续要求用户使用原 AstrBot 斜杠命令。
- 忽略缓存导致同一个 hash 反复打 whatslink.info。
- 把 `UNKNOWN` 或错误响应长期写进缓存。
- 在没有字体时承诺中文图片一定能正确显示。
- 为了生成图片而丢掉文本验车结果。
