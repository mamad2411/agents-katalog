---
name: gcli
description: "Use this skill to operate the gcli Gmail CLI for practical email tasks: inbox triage, Gmail query search, message/thread retrieval, full content extraction, and machine-readable output handling. Trigger when users ask to查邮件、筛选邮件、读完整正文、按条件搜索、提取附件相关邮件、或直接执行 gcli 命令并解释结果."
---

# gcli - 邮件查询执行技能

用于指导使用 `gcli` 帮用户“查到邮件并给出可执行下一步”，而不是讲解底层实现。

## 触发条件（意图识别）

当用户出现以下意图时，立即使用本技能：

- “帮我查下最近邮件/未读邮件/某人来信”
- “按条件搜索邮件（发件人、主题、日期、是否附件）”
- “打开某封邮件全文/原始 MIME”
- “给我可直接执行的 gcli 命令”
- “把搜索结果整理成可机器消费的 JSON”

## 执行前检查

按顺序执行以下检查：

1. 先检查是否已安装 `gcli`（例如执行 `gcli version`）。
2. 如果命令找不到，先确认当前机器未安装 `gcli`，再执行安装：
```bash
curl -fsSL https://raw.githubusercontent.com/geekjourneyx/gcli/main/scripts/install.sh | bash
```
3. 安装后再次检查：`gcli version`；通过后继续后续流程。
4. 确认凭据已就绪：`GCLI_GMAIL_CLIENT_ID`、`GCLI_GMAIL_CLIENT_SECRET`、`GCLI_GMAIL_REFRESH_TOKEN`
5. 默认 JSON 输出；用户明确要人读表格时再用 `--output table`
6. 不输出完整密钥与令牌

## 标准工作流

### A. 收件箱快速分诊

```bash
gcli mail list --label INBOX --limit 20
```

说明：
- 默认低配额模式，适合先看“有哪些邮件”。
- 若用户要稳定的 `from/subject/date`，追加 `--hydrate`。

### B. 条件搜索（主路径）

```bash
gcli mail search "in:inbox is:unread from:boss@company.com" --max 50
gcli mail search --q "has:attachment filename:pdf after:2026/01/01" --limit 20
gcli mail search "subject:weekly report" --max 20 --page "<next_page_token>"
```

说明：
- `--max` 是 `--limit` 别名；`--page` 是 `--page-token` 别名。
- 位置参数查询和 `--q` 二选一，不能同时传。
- 搜索返回关键字段：`id`、`thread_id`、`date`、`from`、`subject`、`label_ids`。
- 用户要更完整字段时，加 `--hydrate`。

### C. 深读单封邮件

```bash
gcli mail get --id "<message_id>" --format metadata
gcli mail get --id "<message_id>" --format full
gcli mail get --id "<message_id>" --format raw
```

说明：
- `metadata`：元信息（轻量）
- `full`：正文文本/HTML（`body_text`/`body_html`）
- `raw`：完整 MIME（体积大，仅在需要时用）

## 查询语法速查（Gmail q）

- `in:inbox` / `in:sent` / `in:drafts` / `in:trash` / `in:spam`
- `is:unread` / `is:starred` / `is:important`
- `from:sender@example.com` / `to:recipient@example.com`
- `subject:keyword`
- `has:attachment` / `filename:pdf`
- `after:2024/01/01` / `before:2024/12/31`
- `label:Work` / `label:UNREAD`

## 响应模式（最佳实践）

1. 先给命令，再给结果解释，最后给下一步选项。
2. 先最小查询，再深挖；避免一上来 `--hydrate` 或 `--format raw`。
3. 用户给自然语言需求时，先转成 Gmail `q` 再执行。
4. 读取结果时优先引用 `message_id`/`thread_id`，避免模糊描述。

示例回复骨架：

```bash
# 1) 搜索
gcli mail search "from:alerts@example.com newer_than:7d" --max 20

# 2) 深读其中一封
gcli mail get --id "<message_id>" --format full
```

## 失败时最小处理

- `AUTH_MISSING_CREDENTIALS`：缺环境变量或 env 文件未加载
- `AUTH_SCOPE_INSUFFICIENT`：scope 非 `gmail.readonly`
- `MAIL_NOT_FOUND`：`message_id` 无效或已删除
- `TIMEOUT`：减小 `--limit` 或重试

鉴权失败时（`AUTH_*`）先引导执行 login 流程：

```bash
gcli auth login \
  --client-id "..." \
  --client-secret "..." \
  --redirect-uri "http://127.0.0.1:8787/callback" \
  --auth-timeout 10m \
  --print-env
```

成功后写入并加载环境变量，再重试原邮件命令。

## 输出契约

成功：
```json
{"version":"v1","data":{},"error":null}
```

失败：
```json
{"version":"v1","data":null,"error":{"code":"...","message":"...","retryable":false,"details":{"operation":"...","http_status":"...","google_reason":"..."}}}
```

## 安全规则

- 不输出完整密钥与令牌
- 邮件正文仅在用户明确要求时展示
- 默认最小权限：`gmail.readonly`

## 示例触发语句

- “帮我查最近 7 天老板发来的未读邮件。”
- “用 gcli 搜索有 PDF 附件的邮件，给我前 20 条。”
- “把这封邮件完整正文拉出来并总结要点。”
