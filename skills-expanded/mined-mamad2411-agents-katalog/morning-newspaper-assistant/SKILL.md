---
name: morning-newspaper-assistant-skill
description: 当用户希望生成 AI 早报、运行晨报链路、查看今日资讯摘要，或消息中包含”早报””晨报””今日资讯””新闻摘要”等关键词时触发。
---

# Morning Newspaper Assistant Skill

当用户希望运行中文 AI 晨报助手链路、生成 `top10_publishable.json`、输出静态页面、启动 8510 固定链接，或者排查邮箱提醒与成稿稳定性时，使用本 Skill。

## 项目依赖

这个 Skill 依赖完整项目仓库，不能只拷贝 `SKILL.md` 单独使用。

按以下顺序定位项目根目录：
1. 环境变量 `MORNING_NEWSPAPER_ROOT`
2. `~/projects/agentic-ai/morning-newspaper`
3. `~/.openclaw/workspace/morning-newspaper`

若这些路径都不存在，应明确告诉用户：当前环境尚未部署完整项目仓库，请先完成部署。

主要入口：
- `<repo_root>/scripts/run_daily_pipeline.py`
- `<repo_root>/config/sources.yaml`

## 稳定目标

1. `runtime/top10_publishable.json` 稳定为 **10 条**
2. `runtime/dashboard.html` 稳定可生成
3. 8510 固定链接稳定可用
4. 右侧”今日待办提醒”优先读取真实邮箱结果，而不是占位 JSON
5. 如果 IMAP 连通但收不到新邮件，自动继续走 **POP3 fallback**

## 稳定工作流

### A. 每日稳定主流程

**重要：不要直接执行 `run_daily_pipeline.py`。** 该脚本是批处理入口，不会生成 LLM 结果文件。必须按以下步骤逐步执行，在每个"LLM 关口"处读取 prompt 文件、生成结果、再继续。

#### 第一阶段：采集与准备

```bash
python3 scripts/collect_mailbox.py
python3 scripts/collect_raw.py
python3 scripts/enrich_content.py
python3 scripts/prepare_title_shortlist.py
```

产出：
- `runtime/collected_raw.json`
- `runtime/content_enriched.json`
- `runtime/title_candidates.json`
- `runtime/title_shortlist_prompt.txt`

#### LLM 关口 1：标题粗筛

读取 `runtime/title_shortlist_prompt.txt`，按 prompt 要求生成结果，写入 `runtime/title_shortlist_result.json`。

**必须基于本轮 `title_candidates.json` 生成，不能复用旧文件。**

然后继续：

```bash
python3 scripts/apply_title_shortlist.py
python3 scripts/prepare_draft_input.py
```

产出：`runtime/shortlist.json`、`runtime/draft_input.json`、`runtime/draft_prompt.txt`

#### LLM 关口 2：中文成稿

读取 `runtime/draft_prompt.txt`，按 prompt 要求生成结果，写入 `runtime/draft_result.json`。

**必须基于本轮 `draft_input.json` 生成，不能复用旧文件。**

然后继续：

```bash
python3 scripts/apply_draft_results.py
python3 scripts/prepare_top10_ranking.py
```

产出：`runtime/drafted_items.json`、`runtime/top10_ranking_input.json`、`runtime/top10_ranking_prompt.txt`

#### LLM 关口 3：Top10 精排

读取 `runtime/top10_ranking_prompt.txt`，按 prompt 要求生成结果，写入 `runtime/top10_ranking_result.json`。

**必须基于本轮 `top10_ranking_input.json` 生成，不能复用旧文件。**

然后继续：

```bash
python3 scripts/apply_top10_ranking.py
python3 scripts/build_dashboard.py
python3 scripts/check_runtime_status.py
```

产出：`runtime/top10_publishable.json`、`runtime/dashboard.html`

#### 防串轮次机制

每个 apply 脚本会检查结果文件的修改时间是否晚于输入文件。如果结果文件更旧，说明是上一轮遗留的，脚本会报错要求重新生成。遇到此错误时，必须删掉旧文件、重新读取当前 prompt 生成新结果。

### B. 只重建页面

```bash
python3 scripts/run_daily_pipeline.py --rebuild-dashboard-only
```

### C. 8510 固定链接服务

```bash
./scripts/serve_dashboard_8510.sh
```

这个脚本会：
- 停掉已有的 8510 服务实例
- 在 `runtime/` 目录下启动 `python3 -m http.server 8510 --bind 0.0.0.0`

## 人工或模型回填点

以下 3 个结果文件当前仍可由模型或人工回填：

- `runtime/title_shortlist_result.json`
- `runtime/draft_result.json`
- `runtime/top10_ranking_result.json`

如果缺少这些文件，Skill 不应假装完成，而应明确指出缺的是哪一步。

## 页面与数据规则

- `Top10` 必须完整展示 **10 条**
- `summary`/`summary_main` 不允许是 `[TEST] 标题` 这类占位文本
- Tavily 条目没有发布时间时，页面可以显示 `-`，**不要额外加“待确认”文案**
- Tavily 图标不应退回默认 `•`
  - HN → `📰`
  - GitHub → `🧰`
  - 官方模型/研究页 → `🧠`
  - 商业/融资新闻 → `💼`
  - 其他 Tavily → `🔎`
- 邮箱提醒区如果没有真实提醒，应显示空态；不要保留“邮箱模块已切换为独立区域”这种占位卡片

## 邮箱规则

- 真实邮箱提醒写入：`runtime/executive_mailbox.json`
- 事件队列写入：`runtime/mail_event_queue.json`
- 采集报告写入：`runtime/mailbox_collect_report.json`
- 若 IMAP 成功但 `alerts/events` 都为空，且已开启 `pop3_fallback_enabled`，则必须继续尝试 POP3

## 邮箱配置

支持任何提供 IMAP/POP3 服务的邮箱（163、QQ、Gmail、Outlook 等），服务器地址在 `config/sources.yaml` 的 `assistant_mailbox` 段配置。

项目根目录 `.env` 至少需要：

```text
IMAP_USER=your_email@example.com
IMAP_PASS=your_imap_authorization_code
```

注意：`IMAP_PASS` 填邮箱后台生成的客户端授权码 / 应用专用密码，不是网页登录密码。

## 页面输出

- 静态页面：`runtime/dashboard.html`
- 固定分享链接：`http://<服务器IP>:8510/dashboard.html`
- Streamlit 看板入口：`scripts/dashboard_app.py`

## 回复要求

执行完后，至少汇报：

- 当前链路完成到了哪一步
- `runtime/dashboard.html` 是否已更新
- 8510 页面服务是否正常
- 采集总数、候选池数量、成稿数量、Top10 数量、邮箱提醒数量、异常来源数量
- 如果缺少模型回填文件，明确指出缺的是哪一个
