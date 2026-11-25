---
name: linkedin-apply-for-agents
description: >-
  Starts LinkedIn auto-apply after the user provides a resume, a target
  location, and a job scope. Use when installing this skill, or when the
  user mentions auto apply, mass apply, LinkedIn Easy Apply, job
  applications, 海投, 自动投简历, weekday checks for new postings, or the
  former name hk-auto-apply. Require the target location first. Always
  apply on LinkedIn with that location's geoId; if the location is Hong
  Kong, also apply on JobsDB automatically and never ask the user to
  choose platforms. Collect files, facts, and preferences first. Complete
  login later on the computer used for the run; the user may
  sign in themselves or give the agent the password or another
  login method. Do not add job sites beyond this
  location-based rule.
license: MIT
metadata:
  author: PoetCoderJun
---
# linkedin-apply-for-agents

把用户交来的简历和岗位范围，在由投递地区决定的平台上做成两件事：先把符合规则、能投的存量岗位投完，并写出带「平台」列的投递记录和分析报告；再按约定时间做增量检查。一开始必须确认投递地区。一律先投 LinkedIn，并用该地区的 geoId 搜岗。地区是香港时，自动同时投 JobsDB；不要询问要不要加 JobsDB，也不要让用户选择平台。

- **输入**：一份简历 + 投递地区 + 想找什么工作（打字或上传文件都行）。其他需要的信息，助手会再问你。投递地区未说明前，不要开始搜岗或投递。
- **输出**：带「平台」列的投递记录、分析报告和增量检查汇报。记录和报告可用本地 Excel、Google 表格、飞书、Notion 或用户指定的其他载体，不绑定 Notion。
- **动作**：收齐材料，在选定电脑上登录，按已确认的投递地区搜索近约 30 天岗位、阅读 JD、按规则筛选并去重，填写申请、核实结果并记录，再按约定时间检查和投递新岗。

候选人是谁、选哪些岗、申请表填什么，都以当前这位用户交来的材料为准。不要套用其他候选人的简历、薪资或筛选标准，不要编造牌照、语言、地址、身份证或额外年限。

把 `SKILL_DIR` 解析为包含本 `SKILL.md` 的目录。只读取当前步骤需要的 reference，脚本从 `SKILL_DIR/scripts` 运行。

## 按需阅读

- 安装后收集材料，或用户交来的不齐全：读 [references/intake.md](references/intake.md)
- 选择云电脑还是用户自己的电脑，以及登录：读 [references/runtime.md](references/runtime.md)
- 在某个平台上搜岗或投递：读 [references/platforms.md](references/platforms.md)
- 搜 JobsDB 的路径、翻页和卡片：读 [references/jobsdb-search.md](references/jobsdb-search.md)
- 搜 LinkedIn 的公开接口、分页和 429：读 [references/linkedin-search.md](references/linkedin-search.md)
- 域级节流、429 回退与证据日志：读 [references/rate-limit-and-pacing.md](references/rate-limit-and-pacing.md)
- 搜岗分区、游标与 complete/truncated/deferred：读 [references/search-coverage.md](references/search-coverage.md)
- 填写 Easy Apply / Quick Apply，或判断外部申请页：读 [references/applying.md](references/applying.md)
- 把发现结果落盘、中断后续跑：读 [references/queue.md](references/queue.md)
- 把岗位范围编成可执行规则，或阅读 JD：读 [references/selection.md](references/selection.md)
- 两个平台都投、需要去重：读 [references/dedup.md](references/dedup.md)
- 建跟踪表、写分析报告、设每日增量任务：读 [references/tracker-and-report.md](references/tracker-and-report.md)

## 流程

1. 若用户说「请安装这个 GitHub 链接」并指向本仓库（含旧地址或旧名 `hk-auto-apply`）：把整个 `skill/linkedin-apply-for-agents` 目录保存到技能库，包括 `SKILL.md`、`references/` 和 `scripts/`，不要只复制 `SKILL.md`。保存后立刻按 intake 把「文件 / 信息 / 偏好」清单发给用户。
2. 一开始必须确认投递地区；简历或岗位范围里已经写清的，就不要再问。不要询问要投哪些平台，平台由地区自动决定：
   - 一律投 LinkedIn，并用该地区对应的 geoId 搜岗。
   - 地区是香港时，LinkedIn 使用 `geoId=103291313`，并自动同时投 JobsDB、做跨平台去重。告诉用户会同时投这两个平台，不要再问要不要加 JobsDB。
   - 其他地区只投 LinkedIn，按地名解析 geoId；不要自行加入 JobsDB 或其他招聘网站。
3. 问清这次跑在云电脑还是用户自己的电脑，然后在那台电脑上完成登录。用户可以自行操作电脑登录，也可以把账号密码或登录方式交给你，由你在这台电脑上走登录流程。
4. 打开或创建带「平台」列的跟踪表。载体可以是本地 Excel、Google 表格、飞书、Notion 或用户指定的其他表；没指定就先做本地 Excel。双平台时，投之前先做去重。
5. **Backfill（首轮存量）**：用 `evidence/search_coverage_backfill.json` 记录计划内分区；遇 429 写 deferred/截断，不假装搜齐全站。把所有 **可投递**（JD 已可读、符合规则、非 deferred）岗处理到 `apply_log` 终态。首轮结束须：分区全 `complete`、`deferred.jsonl` 无未决 backfill JD/search 重试、可投递岗全终态；`apply_queue` 暂空不能单独证明完成。
6. 仅当 [references/search-coverage.md](references/search-coverage.md) 的 backfill 完成条件（覆盖 + 可投递队列）满足后，才写终版分析报告并称首轮结束；然后与用户确认增量时间、建立 **incremental** 定时任务（`search_coverage_incremental.json` 分开维护）。
7. 定时任务只做 incremental：上次之后新岗或表里还没有的岗；单次结束分别标记当次搜索/投递是否完成；补历史 truncated 分区走 backfill 文件续跑，不与增量混表。

## 硬性约束

- 必须项未齐之前，不要开始搜岗或投递。投递地区未说明算必须项缺失，必须先问清。不要询问要投哪些平台。
- 登录在实际使用的那台电脑上完成：用户可以自行操作电脑登录，也可以把账号密码或登录方式交给你，由你在这台电脑上走登录流程。如果他们发了密码，不要把密码写回聊天，也不要写进通用技能文本。
- 只有看到成功确认，才把该岗记成已投递。
- 没有站内快捷投递、要去公司自己申请页时：默认用海王模式，简单就填，复杂就跳过并记下原因；用户要求「一家都不能放过」时，再尽量跟完每一家外部页，并告知这会更慢、更容易出错。
- 可选封面信就跳过；必填时只根据简历写一小段事实。必填字段不知道就跳过该岗，不要填假。
- 不要删除跟踪表里的探测行或重复行，除非用户明确要求。
- 不要把整个待投队列预先写成「待投递」。中断后从已落盘的队列续跑，不要当新发现重新全网再扫一遍。
- **节流**：同一招聘域同时只有一个进行中的顶层搜岗/JD 请求；遵守 [references/rate-limit-and-pacing.md](references/rate-limit-and-pacing.md) 的运行默认值（10–20s 间隔、guest 10 分钟 ≤20 次、换词 ≥60s）；429 后只许放慢不许加快；记录 `evidence/request_log.jsonl`（无凭证/PII）。可用 `python3 SKILL_DIR/scripts/pacing_gate.py self-check` 做离线自检。
- **429 / 冷却**：尊重 `Retry-After`；无 Retry-After 响应头时不声称官方等待时长，采用运行级 backoff（30/60/120 秒加随机抖动）：第 1 次 429 后约 30s、第 2 次约 60s（均含抖动）；同一顶层请求**最多 2 次重试**（至多 3 次触及 429），之后该请求/分区 deferred 或域冷却 30 分钟；连续 3 次 429 立即域冷却。冷却期间不轮询，用定时任务在 `next_retry_at` 续跑（见 [references/runtime.md](references/runtime.md)）。不用换号/代理/无头绕过限制。
- **覆盖**：backfill 与 incremental 分文件；按 [references/search-coverage.md](references/search-coverage.md) 维护分区与游标；失败页从 `next_cursor` 续跑；队列空 ≠ 搜索完成；**首轮完成 = backfill 分区全 complete + `deferred.jsonl` 无未决 backfill JD/search 重试 + 可投递岗全终态**。
- **deferred**：JD 抓取 429/超时/疑似不完整 → `deferred.jsonl`，**不是** `apply_log` 的 `skipped`。仅硬不匹配、已核实关闭或用户接受遗漏才可 skipped。

## 交付

按平台拆开汇报：唯一卡片数、覆盖 summary（complete/truncated/deferred）、deferred 待重试数、标题匹配数、成功投出数、硬规则 skipped 数、跨平台重复数、限流导致的分区列表、跟踪表的文件或链接、调研文档的文件或链接，以及定时任务会在几点跑。说明范围是「计划内搜索」，不是全站已穷尽。不要假定跟踪表一定是 Notion。若跑在用户自己的电脑上，同时提醒他们到点需要开机。
