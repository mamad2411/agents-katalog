---
name: markdown-proxy
description: |
  Fetch any URL as clean Markdown via proxy services (r.jina.ai / defuddle.md) or built-in scripts.
  Works with login-required pages like X/Twitter, WeChat 公众号, Feishu/Lark docs, Instagram, etc.
  Use this BEFORE agent-fetch, defuddle CLI, or WebFetch when the URL might need authentication or when you want the cleanest markdown output.
  Triggers on any URL the user shares, "fetch this", "read this link", "get content from".
  Supports X/Twitter posts, WeChat 公众号 articles, Feishu/Lark documents, and login-walled pages.
---

# Markdown Proxy - URL to Markdown

将任意 URL 转为干净的 Markdown。支持需要登录的页面和专有平台。

## URL 路由规则（先判断再执行）

收到 URL 后，先判断类型，不同类型走不同通道：

| URL 特征 | 路由到 | 原因 |
|----------|--------|------|
| `mp.weixin.qq.com` | 内置 `scripts/fetch_weixin.py` | 公众号有反爬，需 Playwright 抓取 |
| `feishu.cn` / `larksuite.com`（文档/知识库） | 内置 `scripts/fetch_feishu.py` | 需要飞书 API 认证 |
| `youtube.com` / `youtu.be` | `yt-search-download` skill | YouTube 有专用工具链 |
| 其他所有 URL | 代理服务级联（见下方） |  |

## 代理服务优先级

| 优先级 | 服务 | URL 模式 | 优势 |
|--------|------|----------|------|
| 1 | **r.jina.ai** | `https://r.jina.ai/{url}` | 内容更完整，保留图片链接，覆盖面广 |
| 2 | **defuddle.md** | `https://defuddle.md/{url}` | 输出更干净，带 YAML frontmatter |
| 3 | `agent-fetch` | npx agent-fetch | 本地工具，无需网络代理 |
| 4 | `defuddle` CLI | defuddle parse | 本地 CLI，适合普通网页 |

## Workflow

### Step 0: URL 类型判断

```
if URL contains "mp.weixin.qq.com":
    → Step A: 公众号抓取
    → 结束

if URL contains "feishu.cn/docx/" or "feishu.cn/wiki/" or "feishu.cn/docs/" or "larksuite.com/docx/":
    → Step B: 飞书文档抓取
    → 结束

if URL contains "youtube.com" or "youtu.be":
    → 调用 yt-search-download skill
    → 结束

else:
    → 继续 Step 1
```

### Step A: 公众号文章抓取（内置）

```bash
python3 ~/.claude/skills/markdown-proxy/scripts/fetch_weixin.py "WEIXIN_URL"
```

依赖：`playwright`、`beautifulsoup4`、`lxml`
输出：YAML frontmatter（title, author, date, url）+ Markdown 正文
失败时回退到 Step 1-2 代理服务。

### Step B: 飞书文档抓取（内置）

```bash
python3 ~/.claude/skills/markdown-proxy/scripts/fetch_feishu.py "FEISHU_URL"
```

依赖：`requests`（标准库级别），环境变量 `FEISHU_APP_ID` + `FEISHU_APP_SECRET`
支持：docx 文档、doc 文档、wiki 知识库页面（自动解析实际文档 ID）
输出：YAML frontmatter（title, document_id, url）+ Markdown 正文
支持 `--json` 参数输出 JSON 格式。

### Step 1: 优先用 r.jina.ai

```bash
curl -sL "https://r.jina.ai/{original_url}" 2>/dev/null
```

如果返回非空且包含实际内容，使用此结果。

### Step 2: 如果 Jina 失败，用 defuddle.md

```bash
curl -sL "https://defuddle.md/{original_url}" 2>/dev/null
```

### Step 3: 如果两个代理都失败，回退本地工具

```bash
# agent-fetch: https://github.com/teng-lin/agent-fetch
npx agent-fetch "{original_url}" --json
# 或
defuddle parse "{original_url}" -m -j
```

### Step 4: 展示内容（必做）

抓取成功后，**必须**按以下格式向用户展示：

```
**标题**: {title}
**作者**: {author}（如有）
**来源**: {source_type}（公众号 / 飞书文档 / 网页等）
**URL**: {original_url}

### 内容摘要
{前 3-5 句话的摘要}

### 正文
{完整 Markdown 内容，超长时截取前 200 行并注明"内容已截取，完整版已保存到 xxx"}
```

### Step 5: 保存文件（默认执行）

将抓取的 Markdown 内容保存到本地：

```
默认保存路径：~/Downloads/{title}.md
文件格式：YAML frontmatter（title, author, date, url, source）+ Markdown 正文
```

- 文件名用文章标题，去掉特殊字符
- 如果用户指定了其他保存路径，按用户要求
- 保存后告知用户文件路径
- 如果用户明确说"不用保存"或只是快速预览，可以跳过

## Examples

### X/Twitter 帖子
```bash
curl -sL "https://r.jina.ai/https://x.com/username/status/1234567890"
```

### 普通网页
```bash
curl -sL "https://r.jina.ai/https://example.com/article"
```

### 公众号文章
```bash
python3 ~/.claude/skills/markdown-proxy/scripts/fetch_weixin.py "https://mp.weixin.qq.com/s/abc123"
```

### 飞书文档
```bash
python3 ~/.claude/skills/markdown-proxy/scripts/fetch_feishu.py "https://xxx.feishu.cn/docx/xxxxxxxx"
```

### 飞书知识库
```bash
python3 ~/.claude/skills/markdown-proxy/scripts/fetch_feishu.py "https://xxx.feishu.cn/wiki/xxxxxxxx"
```

## Notes

- r.jina.ai 和 defuddle.md 均免费、无需 API key
- 公众号文章使用内置 Playwright 脚本（需 `playwright install chromium`）
- 飞书文档使用内置 API 脚本（需环境变量 `FEISHU_APP_ID` + `FEISHU_APP_SECRET`）
- 飞书脚本自动将 blocks 转为 Markdown（标题、列表、代码块、引用、待办等）
- 对于超长内容，可用 `| head -n 200` 先预览
