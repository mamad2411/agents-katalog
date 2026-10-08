---
name: mineru-local
description: 把 PDF/DOC/PPT/Image 转成 Markdown。默认走本地 MinerU 3.1.4（M5 mbp 127.0.0.1:8010，1-3s/PDF），云端 fallback 走 mineru.net /api/v4（URL/extra_formats/local 离线）。一行命令 `pdf2md`，自动按输入路由。Trigger 词：pdf转md / pdf to markdown / 解析 pdf / mineru / pdf2md / 把这个 PDF 转成笔记 / 提取 PDF 内容 / arxiv 论文转 md。
allowed-tools: Bash, Read, Write
---

# MinerU 双通道：本地 + mineru.net 云端

> **配置（bundled into grimoire-skill）**：本地服务地址由环境变量
> `MINERU_LOCAL_URL` 指定，默认 `http://127.0.0.1:8010`。原作者用的是内网
> tailnet 主机，移植进本仓库时已脱敏为 localhost 默认值 + 可配置变量。
> 自己机器上：`export MINERU_LOCAL_URL=http://<你的-mineru-host>:8010`；
> 无本地服务时自动回落 mineru.net 云端（需 `~/.config/mineru/token`）。

## 服务架构

```
客户端
  ├── 默认/auto + 文件输入 + local 在线
  │     → curl POST ${MINERU_LOCAL_URL:-http://127.0.0.1:8010}/file_parse
  │     → M5 mbp mineru-api 3.1.4 (launchd KeepAlive)
  │     → pipeline / vlm-transformers 后端（Apple Silicon MPS）
  │
  └── URL 输入 / --cloud / --format / auto+local 挂
        → ~/.claude/skills/mineru/scripts/mineru-parse.sh
        → POST https://mineru.net/api/v4/extract/task (Bearer JWT)
        → 异步轮询 → ZIP 下载 → 解压拿 .md + images + JSON
```

**helper**：`~/bin/pdf2md`（已 chmod +x）— 自动路由 local / cloud

**Token**：`~/.config/mineru/token`（exp 2026-05-28，到期前提示重新申请）

## 触发场景

用户提到下面任意一条 → 立即用本 skill：

- "把这个 PDF 转成 Markdown"
- "解析这个 PDF"
- "PDF to Markdown"
- "pdf2md"
- "用 mineru 本地解析"
- "提取 PDF 文字 / 表格 / 公式"
- "OCR 这个扫描件"

**不要走 cloud API**（旧 `mineru` skill 是 cloud 的，已不推荐 — token 收费、600 页限制、数据出机）。

## 通道速览

| 通道 | 配额 | 单文件上限 | 速度（暖态）| 鉴权 | 状态 |
|---|---|---|---|---|---|
| **local M5** | 无 | 无 | 1-3s | 无 | ✅ |
| **cloud `/api/v4`** | 1k 高优页/天 | **200 页** / 200MB | 10-30s | Bearer JWT | ✅ |
| ~~web (Playwright)~~ | 5k 页/天 独立池 | 600 页 | 30-90s | session cookie | ⚠️ EXPERIMENTAL（runtime 调试中，见 mineru-web skill）|

## 决策表（自动路由）

| 用户给的输入 / 需求 | 路由到 | 命令 |
|---|---|---|
| 一个本地 PDF 文件路径 | **local** M5 | `pdf2md <path>` |
| URL（http/https）输入 | **cloud** mineru.net | `pdf2md https://...pdf`（自动识别）|
| 想要 docx / latex / html 输出 | **cloud**（local 不支持 extra_formats） | `pdf2md x.pdf --format docx` |
| 本地 PDF 200-600 页 | **web**（cloud 不行） | `pdf2md x.pdf --web` |
| 想省 JWT 高优配额 | **web**（独立池）| `pdf2md x.pdf --web` |
| local 在线，想自动 fallback | **auto** | `pdf2md x.pdf --auto`（local 优先，挂了走 cloud） |
| 显式云端 | **cloud** | `pdf2md x.pdf --cloud --model vlm` |
| 大型扫描件 / 复杂公式 / 表格 | local vlm-transformers | `pdf2md x.pdf -b vlm-transformers` |
| 多个 PDF | for 循环 local | `for f in *.pdf; do pdf2md "$f"; done` |
| 部分页（节选章节）| cloud | `pdf2md x.pdf --cloud --pages "1-5,8"` |
| 敏感文档（合同 / 内部材料） | **强制 local** | `pdf2md x.pdf`（不要 --cloud / --web） |
| Word / PPT / Excel | 任意通道 | `pdf2md x.docx` |

### Web 通道首次设置（一次性）

```bash
python3 ~/Tools/mineru-web/login.py    # 弹浏览器，扫码/登录 mineru.net，按 Enter 关
```

cookie 落到 `~/Tools/mineru-web/profile/`，约 30 天有效。失效后再跑一次。
失效检测：`pdf2md x.pdf --web` 报 "not logged in"，或 `health-check.sh` 第 7 段提示。

## 一键用法

```bash
# 最常见：一个 PDF → 同名 .md（同目录）
pdf2md ~/Downloads/某论文.pdf
# → ~/Downloads/某论文.md

# 指定输出文件
pdf2md input.pdf /tmp/out.md

# 指定后端（vlm 更准但 slow）
pdf2md input.pdf -b vlm-transformers
```

helper 内部就是：
```bash
curl --max-time 600 -X POST ${MINERU_LOCAL_URL:-http://127.0.0.1:8010}/file_parse \
  -F "files=@input.pdf" -F "backend=pipeline" -F "return_md=true"
```

## 高级：直接 curl

mineru-api `/file_parse` 完整 form 字段（OpenAPI spec 实测）：

| 字段 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `files` | file[] | (必填) | multipart 文件，支持多个 |
| `backend` | str | pipeline | `pipeline` / `vlm-transformers` / `vlm-vllm-engine` |
| `parse_method` | str | auto | OCR 还是文本提取自动判断 |
| `lang_list` | str[] | auto | OCR 语言（109 语支持），如 `["ch","en"]` |
| `formula_enable` | bool | true | 公式 → LaTeX |
| `table_enable` | bool | true | 表格 → HTML |
| `start_page_id` | int | 0 | **0-based 起始页**（包含） |
| `end_page_id` | int | -1 | **0-based 结束页**（包含），-1 = 最后一页 |
| `return_md` | bool | false | 返回 markdown |
| `return_middle_json` | bool | false | 返回中间结构化 JSON |
| `return_content_list` | bool | false | 返回 element 列表 |
| `return_images` | bool | false | 返回 base64 图片 |
| `response_format_zip` | bool | false | 全部打 ZIP 返回 |

例：解析 100-199 页 + 返回 images：

```bash
curl --max-time 600 -X POST ${MINERU_LOCAL_URL:-http://127.0.0.1:8010}/file_parse \
  -F "files=@big.pdf" \
  -F "backend=pipeline" \
  -F "start_page_id=100" \
  -F "end_page_id=199" \
  -F "return_md=true" \
  -F "return_images=true" \
  -o /tmp/result.json
```

## 异步任务（超长 PDF / 后台批处理）

```bash
# 提交
TASK=$(curl -s -X POST ${MINERU_LOCAL_URL:-http://127.0.0.1:8010}/tasks \
  -F "files=@huge.pdf" -F "backend=pipeline" -F "return_md=true" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['task_id'])")

# 轮询状态
curl -s ${MINERU_LOCAL_URL:-http://127.0.0.1:8010}/tasks/$TASK | python3 -m json.tool

# 拿结果
curl -s ${MINERU_LOCAL_URL:-http://127.0.0.1:8010}/tasks/$TASK/result -o /tmp/huge.json
```

## 限制（重要！与旧 cloud skill 区别）

| 项 | Cloud (mineru.net) | **本地 M5 (本 skill)** |
|---|---|---|
| 单 PDF 页数 | **600 页** | **无硬上限**（README: tens of thousands of pages） |
| 单文件大小 | 200 MB | 无硬上限 |
| 并发 | 多并发 | concurrency=1（多 PDF 排队） |
| 隐私 | 上传到 mineru.net | 不出 tailnet |
| 成本 | token | 0（M5 算力本来就在） |
| 联网 | 必需 | 不必（首次启动除外，要拉子模型） |

实际限制因素：
- M5 内存 128GB unified — 万页都撑得住
- 首次冷启动 ~4 min（fetch HF 子模型）；KeepAlive 后秒级
- pipeline 后端 ~1-3s/PDF（暖态）；vlm 后端慢但更准

## 故障排查

### 服务不响应

```bash
# 1. 验证 M5 mineru-api 还在跑
ssh mbp 'launchctl list | grep mineru-api'
# 期望: <PID>  0  com.leo.mineru-api

# 2. 端口监听
ssh mbp 'lsof -i :8010 | head'
# 期望: python3 ... TCP *:8010 (LISTEN)

# 3. 端到端 docs 健康
curl --max-time 5 ${MINERU_LOCAL_URL:-http://127.0.0.1:8010}/docs -o /dev/null -w "HTTP %{http_code}\n"
# 期望: HTTP 200
```

### 卡住没响应（首次）

```bash
# 看 M5 mineru 是不是在拉 HF 子模型
ssh mbp 'tail -f /tmp/mineru-api.err'
# 看到 "Fetching N files: X%" 就是在拉，4 min 完成
```

### 422 Validation Error

字段名错。注意 `files=@...`（**复数**）不是 `file=`。

### 重启 mineru-api

```bash
ssh mbp 'launchctl unload ~/Library/LaunchAgents/com.leo.mineru-api.plist && \
         launchctl load ~/Library/LaunchAgents/com.leo.mineru-api.plist'
```

### 直接走 M5 CLI（绕过 HTTP）

```bash
ssh mbp 'source ~/Tools/mineru-m5/.venv/bin/activate && \
         mineru -p /path/to/input.pdf -o /path/to/output_dir'
# 输出 output_dir/<basename>.md + 图片
```

## 工作流模板

### 模板 A：单 PDF → 同目录 .md

```bash
pdf2md "$1"
```

### 模板 B：批量 → 同目录

```bash
for f in ~/Downloads/*.pdf; do
  out="${f%.pdf}.md"
  if [ ! -f "$out" ]; then
    pdf2md "$f"
  else
    echo "skip $out (exists)"
  fi
done
```

### 模板 C：PDF → vault Books/

如果是要进 Knowledge-Hub vault 的读书笔记：

1. `pdf2md ~/Downloads/Book.pdf /tmp/book-raw.md`
2. 看一遍 `/tmp/book-raw.md` 确认 OCR 没大问题
3. 用 vault 的 Books/ frontmatter 模板加头（参考 `~/Documents/Obsidian-Vaults/Knowledge-Hub/CLAUDE.md` 读书笔记规范）
4. 移到 `~/Documents/Obsidian-Vaults/Knowledge-Hub/Books/<book-slug>/INDEX.md`
5. 让 git auto-sync 5 min 内同步到 mac-mini / mbp / GitHub

### 模板 D：超大 PDF 分块

```bash
# 先看总页数
PAGES=$(python3 -c "import sys; from pypdf import PdfReader; print(len(PdfReader(sys.argv[1]).pages))" big.pdf)
echo "$PAGES pages, will split into 100-page chunks"

# 分块跑
for i in $(seq 0 100 $((PAGES-1))); do
  end=$((i+99))
  [ $end -ge $PAGES ] && end=$((PAGES-1))
  curl --max-time 600 -s -X POST ${MINERU_LOCAL_URL:-http://127.0.0.1:8010}/file_parse \
    -F "files=@big.pdf" -F "backend=pipeline" \
    -F "start_page_id=$i" -F "end_page_id=$end" -F "return_md=true" \
    -o /tmp/big_${i}_${end}.json
  python3 -c "import json; d=json.load(open('/tmp/big_${i}_${end}.json')); print(d['results']['big'].get('md_content',''))" \
    > /tmp/big_${i}_${end}.md
  echo "wrote /tmp/big_${i}_${end}.md"
done
cat /tmp/big_*.md > /tmp/big_full.md
```

## 脚本

- `scripts/pdf2md-batch.sh` — 批量目录处理（参考模板 B）
- `scripts/pdf-pages.sh` — 拆超大 PDF 分块跑（参考模板 D）

## 配套文档

- 完整架构文档：`Knowledge-Hub/Claude-Memory/Projects/mineru-local-mac-mini-m5-2026-04-26.md`
- memory 索引：`reference_mineru_local.md`
- helper 源码：`~/bin/pdf2md`
- M5 launchd：`mbp:~/Library/LaunchAgents/com.leo.mineru-api.plist`

## 不要做的事

- ❌ 不要走 cloud API（旧 `mineru` skill 还在但只作 fallback）
- ❌ 不要一次提交 100+ 个 PDF（concurrency=1 排死）
- ❌ 不要在没有 tailnet 的网络上用（M5 在 tailnet 127.0.0.1）
- ❌ 不要假设 mac-mini:8010 能用（反代未通；用 M5 直连）
