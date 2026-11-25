---
name: daily-work-log
description: 生成本机今天（或指定日期）的「每日工作日报」——汇总 Claude Code / Codex / Gemini CLI / git 的工作记录，脱敏、按项目分组，产出文字版 + HTML 版（可截图成图片）。当用户说「整理今日工作 / 生成日报 / 我今天做了什么 / daily work log / standup」时使用。也可被定时任务（cron / Hermes）调用做无人值守日报。Powered by Debrief (the `debrief` CLI).
---

# 每日工作日报（Debrief）

基于 **Debrief**（`debrief` CLI）把本机 AI 编程活动整理成日报。CLI **只读本地日志、不联网、自动脱敏、零依赖**。

## 流程

### 1. 跑 CLI 生成日报（文字 + HTML + JSON）
```bash
# 已全局安装（npm i -g debriefly）/ npx debriefly：
debrief --lang zh --out ~/work-logs
# 或从源码：
node /path/to/debrief/bin/debrief.mjs --lang zh --out ~/work-logs
```
- 产出 `~/work-logs/debrief-<日期>.md`（文字版）、`.html`（图片版）、`.json`（结构化）。
- 常用参数：`--date YYYY-MM-DD` 指定日期、`--tz` 时区、`--lang en|zh`、`--sources claude,codex,gemini,git`。
- 想纳入 Hermes Agent / WorkBuddy / OpenClaw 的活动（默认不开）：加 `--sources claude,codex,gemini,git,hermes,workbuddy,openclaw`。三者内容都存在 SQLite，靠系统 `sqlite3` CLI 只读读取；没装 `sqlite3` 就自动跳过。WorkBuddy 本地只存会话标题（对话正文在云端/内存），OpenClaw 汇总的是 `task_runs` 里的任务文本。
- 想直接拿文本/JSON：`debrief --html` / `--json` 打到 stdout。

### 2. （可选）润色 / 总结
CLI 出的是「客观汇总」。如需更像周报/standup 的叙述，基于 `.json` 或 `.md` **再加一段简短总结**即可 —— 但**只能基于 CLI 输出**，不要臆造、不要引入采集之外的信息；任何拿不准的内容宁可不写。

### 3. （可选）发图 / 发消息
- 文字版：直接发文本。
- 图片版：把 `.html` 用浏览器/无头 Chrome **截成 PNG** 再发（飞书 / Slack / 企微都支持发图）。
- 两份一起发是最佳：文字便于检索，图片便于一眼看完。

## 定时（无人值守）场景
被 cron / Hermes 在每天固定时间（如 18:00–19:00）调用时：
- **Heartbeat 守卫**：若触发时刻早于约定时间，当天数据不完整 —— 不生成 / 不发送，只报告「调度异常：触发过早」。
- 已授权无人值守：不向用户请求确认 / 审批；可直接跑 CLI、写文件、发消息。
- 不自行登录任何网站、不处理或复述密码密钥、不修改任何代码仓库。

## 备注
- CLI 只认本机日志，**必须在本机运行**（云端读不到 `~/.claude`、`~/.codex`、`~/.gemini`）。
- 这是「汇总 / 归纳」类技能，不替代真实判断：拿不准的内容宁可留空。
- 安装/源码：`npm i -g debriefly` · https://github.com/<your>/debrief
