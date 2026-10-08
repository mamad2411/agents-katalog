---
name: xhs-studio
description: Publishes image-text notes to Xiaohongshu (小红书) via a local MCP server. Supports text, images, tags, visibility settings, and scheduled publishing. Also supports searching trending content. Use when user asks to "post to XHS", "发小红书", "publish to Xiaohongshu", or "搜索小红书热点".
---

# Post to Xiaohongshu (小红书)

Publish image-text notes to Xiaohongshu via a local MCP server (`xiaohongshu-mcp`). Supports images, tags, visibility control, and scheduled posts.

## Prerequisites

1. Download `xiaohongshu-mcp` binary from [xiaohongshu-mcp releases](https://github.com/jobsimi/xiaohongshu-mcp)
2. Place the binary at a known path (e.g. `~/xiaohongshu-mcp/xiaohongshu-mcp-darwin-arm64`)
3. Configure the path in EXTEND.md (see **Preferences** below)
4. Run login once to save cookies: `python3 ${SKILL_DIR}/scripts/login.py`

## Preferences (EXTEND.md)

Check EXTEND.md (priority: project → user):

```bash
test -f .baoyu-skills/xhs-studio/EXTEND.md && echo "project"
test -f "$HOME/.baoyu-skills/xhs-studio/EXTEND.md" && echo "user"
```

| Path | Location |
|------|----------|
| `.baoyu-skills/xhs-studio/EXTEND.md` | Project directory |
| `$HOME/.baoyu-skills/xhs-studio/EXTEND.md` | User home |

**EXTEND.md schema:**

```yaml
mcp_bin: /path/to/xiaohongshu-mcp-darwin-arm64   # required
mcp_port: 18060                                    # optional, default 18060
```

If EXTEND.md not found → ask user for `mcp_bin` path, save EXTEND.md, then continue.

## Script Directory

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.py`

| Script | Purpose |
|--------|---------|
| `scripts/publish.py` | Publish image-text note |
| `scripts/search.py` | Search trending content |
| `scripts/login.py` | QR code login |

## Publishing a Note

```bash
python3 ${SKILL_DIR}/scripts/publish.py \
  --title "标题（≤20字）" \
  --content "正文内容" \
  --images /path/to/image1.png /path/to/image2.png \
  --tags "AI工具" "效率神器" \
  --visibility "公开可见"
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--title` | ✅ | 标题，最多 20 个中文字 |
| `--content` | ✅ | 正文内容（支持换行） |
| `--images` | ✅ | 图片路径列表（本地绝对路径 或 https:// 链接，最多 18 张） |
| `--tags` | optional | 话题标签，如 `"AI工具" "效率"` |
| `--visibility` | optional | `公开可见`（默认）/ `仅自己可见` / `仅互关好友可见` |
| `--schedule` | optional | 定时发布，ISO8601 格式：`2026-03-16T20:00:00+08:00` |

## Searching Trending Content

```bash
python3 ${SKILL_DIR}/scripts/search.py "关键词"
```

Returns top notes with title, author, and like count. Use this for topic research before writing.

## Login / Re-login

```bash
python3 ${SKILL_DIR}/scripts/login.py
```

Opens a QR code image. Scan with Xiaohongshu app. Session is saved automatically to `cookies.json` next to the MCP binary.

## Notes

- The MCP server starts automatically if not already running
- Requests to `localhost` must bypass any system proxy (`NO_PROXY=localhost` is set automatically)
- Title limit: 20 Chinese characters or equivalent
- Image limit: 18 images per post
- Scheduled posts: 1 hour to 14 days from now
