---
name: story-data-analyze
description: 分析番茄等网文平台的长篇小说与短故事后台数据，校验统计口径和刷新状态，拆解分发、点击、阅读、前三章/分段留存、回访与追更漏斗，识别真实异动并下钻到具体章节或段落，形成可验证的改文实验。用于 story-data-analyze、数据分析、后台数据、推荐数据、在读人数、跟读率、读完率、短故事点击率/15秒/30秒/60秒/触底率、修改后是否变好、为什么读者流失、该改哪一章或哪一段等请求。
metadata: {"openclaw":{"source":"https://github.com/qin1473692580-ux/oh-story-claudecode"}}
---

# story-data-analyze：指标体系驱动的小说数据诊断工作流

> Spawn 版本提示（不阻断 spawn）：先读取项目根 `.story-deployed` 的 `agents_version`。与本版 `agents_version: 39` 不一致时（标记缺失、字段缺失/非整数、小于或大于 39）**照常按文件存在性检查并 spawn**，同时报告 `Notice: agents bundle 版本不匹配（项目 {N}，本版 39）` 并提示重新运行 `/story-setup` 后新开会话；大于 39 时额外提示先更新 oh-story-claudecode，不要用本地旧版 setup 降级覆盖。只有 agent 文件缺失、或运行时不暴露 custom agent 时才降级 solo/direct，报告 `Fallback: ... -> solo`。本 Skill 的具体落点仍按 lane 降级矩阵映射为 `degraded` / `solo`；当前运行时定义 malformed 与 registry 缺失同样视为 agent 不可用。

## 目标

本 Skill 是多 Agent 工作流的唯一入口，不是一份逐项看数清单。它以机器可读指标目录、指标树和诊断路由为共同语义层，完成以下闭环，不要停在“数字总结”或“样本不足”：

`数据可信 → 漏斗定位 → 异动定级 → 阅读对应文本 → 提出因果闭合的修改 → 发布后验证`

指标体系固定分为五类，不得把它们平铺成互不相干的单点指标：

1. **结果指标**：作品是否持续产生有效阅读或有效触底；用于描述结果，不直接等同于可编辑抓手。
2. **驱动指标**：分发、包装承接、黄金前三章/分段漏斗、深读和回访如何共同驱动结果。
3. **诊断指标**：渠道结构、章节到达、条件跟读、损失人数、滚动窗进入/滚出等，用于寻找问题发生在哪里。
4. **护栏/反指标**：防止为了提高一个节点而破坏上游承诺、下游追读、逻辑一致性或流量质量。
5. **数据质量指标**：刷新、完整性、公式一致性、版本覆盖、范围可比性和污染；质量门不通过时关闭业务解释。

长篇的各层通常来自不同窗口或 cohort，不能把整棵树伪造成一个精确乘法公式；短故事同一快照的展示→阅读→15秒→30秒→60秒→触底在口径一致时可以严格分解。

每次至少回答六个问题：

1. 数据统计到哪一天，是否已完成刷新？
2. 最新数据相对修改前基线、前一快照分别怎样变化？
3. 变化发生在分发、包装、阅读承接、回访还是深章推进？
4. 异常对应哪一章、哪一段或哪个包装元素？
5. 为什么建议的修改在逻辑上有机会改善目标指标？
6. 发布后用什么指标、什么窗口验证，哪些指标不能变差？

把“方向”和“结论强度”分开。小样本也要如实报告绝对增量和上升/下降方向，但不得伪装成因果结论。

## 必读资源

处理番茄数据时按任务读取以下文件：

- 每次运行：读取 [references/workflow-contract.md](references/workflow-contract.md)，遵守 Agent 分工、artifact 状态机、八道门禁和回退协议。
- 每次运行：加载 `dictionary/metrics.v1.json`、`dictionary/metric-tree.v1.json` 与 `dictionary/diagnostic-routes.v1.json`；它们分别是指标语义、上下游关系和异动下钻的机器权威。
- 解释指标体系或排查指标联动：读取 [references/metric-system.md](references/metric-system.md) 与 [references/diagnostic-routing.md](references/diagnostic-routing.md)。
- 所有番茄任务：读取 [references/fanqie-metrics.md](references/fanqie-metrics.md)，只使用与长篇或短故事对应的章节。
- 比较前后快照、判断异动：读取 [references/anomaly-rules.md](references/anomaly-rules.md)。
- 给出改文建议或定位正文：读取 [references/text-drilldown.md](references/text-drilldown.md)。

需要复用方法或案例时，先读 `数据追踪/knowledge/index.json`，再读 `数据追踪/knowledge/methods/index.json` 或 `数据追踪/knowledge/cases/index.json`，最后只加载命中的条目。知识条目是辅助证据，不能覆盖当前官方口径或当前 run 的事实。

指标定义与后台当前 tooltip 不一致时，以后台当前官方定义为准，并把差异记录到报告和参考文件；不要凭指标名猜口径。

## 不可违反的规则

1. **先校验数据，再解释业务。** 把空值、未刷新、字段滞后、滚动窗口换日与真实变差分开。
2. **长篇和短故事使用不同漏斗。** 不得用长篇跟读率解释短故事触底率，也不得用短故事点击率替代长篇章节承接。
3. **先看上游，但不得因此跳过下游事实。** 上游没量会降低下游结论可信度，不代表可以不计算前三章或分段留存。
4. **百分比优先寻找权威分子/分母。** 平台提供权威人数或明确 cohort 基数时，同时报绝对人数、转化率、百分点变化和样本量；只有展示百分比时不得伪造人数。可以计算“最小兼容整数下界”检查曲线是否存在整数解释，但必须标 `minimum-compatible-lower-bound/display_only/non-authoritative/not-an-estimate`：真实 cohort 可为任意更大的兼容解，不得跨快照相减成新增人数，也不能复用滞后的 follow 字段作同一分母。
   - 该下界**不是人数估算**，不得进入样本门槛、显著性检验、置信区间、MDE、绝对损失或“可挽回人数”计算。
   - 找不到与本次问题同 cohort、同口径且权威的样本分母时，必须登记 `sample_size_qualified=false`、`sample_size=0`、`sample_size_authoritative=false`、`sample_aggregation=unavailable` 和非空 `sample_unavailability_reasons`；analysis 使用 `sample_metric_id=UNAVAILABLE`。这里的 `0` 是“合格样本不可得”的状态编码，不是“真实读者为 0”，禁止拿别的计数或兼容下界代替。
5. **渠道阅读人数不等于曝光。** 书城/分类为 0 只能说未观察到该渠道阅读 UV，不能说平台零曝光或推荐评估失败。
6. **继续阅读为 0 不等于绝对无人跨日回来。** 它只是该入口没有记录到阅读 UV。
7. **在读人数不是历史累计人数。** 番茄长篇在读人数是最近 14 天累计“听+读”用户，不能拿来计算章节跟读，也不能把单日 -1 直接称为流失 1 人。
8. **跟读低不只检查章末。** N→N+1 低说明读过 N 的人没有进入 N+1；检查第 N 章全章、章末、下一章标题和下一章开头。
9. **累计快照不是新读者队列。** 快照差值可能混有老读者继续推进；只能称“窗口增量到达”，除非平台提供同批 cohort。
10. **不得保证改文一定涨数据。** 必须证明修改与指标之间的因果链合理，再由发布后的数据验证。
11. **当前工作流不自动修改正文或发布。** 默认交付具体修改方案与数据诊断卡；当前只有 `UNATTESTED_PROCEDURAL` 记录、没有宿主签名，即使用户在会话中明确同意也只形成可审计交接，不能由本 run 自动落文或发布。
12. **搜索流量占主导时确认自访。** 未确认前保留方向事实，但把文本归因降级；不要擅自认定全部搜索都是作者或熟人。
13. **必须沿树联查，禁止孤立看点。** 任一异动都要执行诊断路由规定的上游、同层、下游和护栏检查；没有完成必查项，不得进入文本归因。
14. **Agent 不得越权替做。** 抓取 Agent 不解释业务，指标 Agent 不读正文，校验 Agent 不润色原结论，文本 Agent 不改正文，看守 Agent 不发明分析。
15. **运行产物不得冒充知识。** 日报、raw、单次推测和未验证修改都不能直接放入知识库；晋升必须经过监督门禁并保留来源 hash。

## 执行架构与总流程

### 运行模式

- `full`：五角色均可用，执行完整工作流。
- `degraded`：某一 lane 不可用，按 workflow contract 的降级矩阵执行并在报告中列出缺失能力。
- `solo`：runtime 无 custom agents 时由主 Agent 严格分阶段执行，但不得声称做过独立复算或监督；结论强度按缺失 gate 下调。

支持 custom agents 的运行时优先使用以下逻辑角色。先识别当前运行时，只检查对应目录：TRAE Code 为 `.trae/agents/{agent}.md`，Codex 为 `.codex/agents/{agent}.toml`；其他运行时只有部署了等价定义且暴露子 Agent 工具时才能进入 `full`。TRAE Code 的 `.md` 必须含合法 YAML frontmatter（`name`、`description` 必填，`tools` / `disallowedTools` 为逗号字符串），并通过内置 `Agent` 智能体选择同名 subagent；不要把 Claude 的 `subagent_type` 参数原样传给 TRAE。Codex 使用同名 `agent_type`。当前运行时对应目录或 registry 不完整时，按 [references/workflow-contract.md](references/workflow-contract.md) 的 lane 降级矩阵进入 `degraded` / `solo`，不得拿磁盘上其他端残留定义冒充已注册 Agent。项目中仅并存 `.zcode/` 不是当前运行时降级的依据。

WorkBuddy 使用有上限的物理 Agent 池，不再把五个逻辑角色全部注册为同名物理卡。WorkBuddy 物理注册只检查 `story-data-fetcher` 与 `story-data-readonly-runner`：前者保留 Bash 拉取能力，后者仅有 `Read, Glob, Grep`，承载其余四个只读逻辑角色。项目模式要求 `.codebuddy/agents/` registry 真实列出这两个原始名称；plugin-only 模式只在当前 registry 真实列出时使用 `oh-story:story-data-fetcher` 与 `oh-story:story-data-readonly-runner`，不从 manifest 或磁盘文件推测注册成功。

五个逻辑角色为：

1. `story-data-fetcher`
2. `story-data-metrics-analyst`
3. `story-data-method-validator`
4. `story-data-text-improvement-planner`
5. `story-data-supervisor`

主 Agent 是唯一编排器和最终报告写入者。所有子 Agent 的 prompt 必须自包含 `run_id`、作品身份、冻结输入及 hash、截止日、改动事件、允许输出和禁区；子 Agent 不得递归 spawn。TRAE Code 每次调用都在内置 `Agent` 中明确选择上表的精确名称，并把完整自包含合同作为任务正文；若 `Agent` 工具未列出该名称，立即按 lane 降级，不通过普通对话假装完成独立角色复算。

WorkBuddy 的 `story-data-fetcher` 仍把完整 `raw_capture` 合同直接放进物理 fetcher 的 `prompt`。调用其余四个逻辑角色时，主 Agent 必须调用物理 `story-data-readonly-runner`，且 prompt 只能用以下封装：

```json
{
  "logical_role": "<story-data-metrics-analyst|story-data-method-validator|story-data-text-improvement-planner|story-data-supervisor>",
  "logical_role_card_path": "<已解析的真实绝对路径>",
  "project_abs_path": "<当前作品项目真实绝对路径>",
  "task_contract": {"role": "<与 logical_role 相同>", "run_id": "<run_id>", "lane": "<该角色 lane>", "project_abs_path": "<与顶层字节一致>", "...": "<该逻辑角色的其余完整合同>"}
}
```

`logical_role_card_path` 项目模式只能解析到 `<项目根>/.codebuddy/skills/story-data-analyze/references/workbuddy-role-cards/<logical_role>.md`；plugin-only 模式只能解析到 CodeBuddy 已内联替换后的 `<CODEBUDDY_PLUGIN_ROOT>/skills/story-data-analyze/references/workbuddy-role-cards/<logical_role>.md`。传入 Runner 前必须取真实绝对路径，确认文件存在、直接父目录为该模式的固定 role-card 根、文件名与 `logical_role` 精确对应，且不含未解析占位符。Runner 或对应角色卡缺失、frontmatter 不合同、逻辑映射不唯一，均立即按该 lane 降级；不得改用旧的同名物理卡，不得把磁盘卡片存在冒充 registry 可用。

### 固定状态链

```text
INIT → RAW_CAPTURED → DATA_QUALIFIED → WINDOW_BOUND → METRICS_READY
→ ANALYZED → ANALYSIS_VERIFIED → TEXT_DIAGNOSED → SUPERVISED → REPORT_COMPLETE
```

每一步通过 `scripts/data_workflow.py` 记录不可变 artifact 和 hash；禁止手改 `analysis-runs` 的 manifest。validator 或 supervisor 退回时，从最早错误阶段新建 attempt，最多三轮，之后标 `BLOCKED`。

三次是**整个 run 共享的全局 RETURN 上限**，不是“每个 Agent 三次”或“每种根因三次”。validator 与 supervisor 合计最多接受 3 次 RETURN，第 4 次 RETURN 请求直接把 run 标为 `BLOCKED`；根因计数只用于诊断，不能扩大总额度。

固定顺序：抓取 → 确定性标准化与质量门 → 指标分析 → 独立方法校验 → 文本诊断 → 看守 → 主 Agent 渲染日报。文本 Agent 的输入合同要求 validator PASS，因此不得提前读取正文；最多只能并行预载不含正文的公开方法，不能记录为有效 text artifact。

validator 的“独立复算”不是复述 metrics artifact：必须对每条 fact 重新打开冻结 raw/normalized/window 源，按其 JSON Pointer 读取 observation，并按记录的 calculation expression 复算；事实选择器、source refs、observations、formula、calculation 和结果全部一致且无遗漏时才可 PASS。

各 Agent 返回统一 envelope，工作流 CLI 记录的是角色专属 lane payload。主 Agent 必须先做确定性 adapter：验证 envelope 的 `run_id/role/status/input_hashes`，再只提取 schema 规定的 `raw_capture/data_quality/analysis/validation/text_diagnosis/supervision` 对象；禁止把整个自然语言响应或整个 envelope 原样塞进 `record --payload`。

### Phase 0：确定作品类型和分析问题

先确定：

- 作品类型：长篇小说 / 短故事 / 两者都有。
- 用户问题：例行日报、修改效果、推荐/分发、前三章、某章断点、包装、完整诊断。
- 目标改动：改了什么、何时上线、预期影响哪个指标。
- 输入模式：拉取最新后台 / 分析用户给定快照或截图 / 只解释方法。
- 作品身份：锁定平台、作品名与作品 ID；账号有多部作品时禁止串数。

若同时分析长篇和短故事，分别建立漏斗和结论，不合并样本。

### Phase 1：取数并判定数据是否可用

用户要求最新数据或例行监控时，对本项目执行：

```bash
cd "<项目根>"
for PYBIN in python3 python py; do "$PYBIN" -c "" 2>/dev/null && break; done
"$PYBIN" "数据追踪/拉取番茄数据.py"
```

用户明确指定本地历史快照、上传数据或只询问分析方法时，不擅自拉取新数据；先核验给定数据的截止日和作品 ID。

随后完成五项检查：

1. **登录**：出现 `LOGIN_INVALID` 时停止，不使用旧数据冒充最新数据；通知用户重新登录。
2. **日期**：确认 raw 的 `date` 为运行日、`data_until` 为前一日；平台中午更新前抓到的占位数据标记“平台尚未更新”。
3. **完整性**：区分 `null`、空字符串、缺字段和真实 `0`；不得自动把前三者转成 0。
4. **内部一致性**：渠道合计、阅读人数、章节到达与跟读公式应在允许的四舍五入误差内一致；不一致时标出具体字段并选择可信度更高的原始人数或等待同步。
5. **口径**：记录累计/单日/7日/14日/自定义周期、是否跨日重复、是否滚动去重。

若当前问题所需样本分母不可从冻结源权威复算，不要拿日阅读人数、14 日在读、兼容整数下界或别的资格人群替代。按“样本不可用”编码继续生成事实与缺失节点，最终只能给 `样本不足/SAMPLE_INSUFFICIENT`，但仍可如实报告不依赖伪分母的原始观测。

若 raw 的 `short_query.scope_verified_against_ui=false`，短故事 `yesterday_sum_*`字段只能称“该快照接口原值”；打开后台核验当前周期后，才能称累计或单日口径。

输出数据质量标签：`可分析 / 部分字段滞后 / 平台未更新 / 登录失效 / 口径未知`。只有可用字段可以进入后续判断。

### Phase 2：建立修改与数据窗口的对应关系

读取 `数据追踪/番茄数据日志.md` 的改动登记，为每项改动建立实验卡：

| 字段 | 必填内容 |
|---|---|
| 改动 | 书名/封面/简介/具体章节与段落/更新恢复等 |
| 上线时间 | 精确到分钟，区分保存与实际发布 |
| 目标人群 | 上线后实际接触新版的读者 |
| 主指标 | 该改动最直接影响的一个指标 |
| 护栏指标 | 不应因改动而下降的上游或下游指标 |
| 修改前基线 | 优先取 3–7 个可比完整数据日，至少保留最后一个改前快照 |
| 最小有意义变化 | 预先写明数值及来源：本书历史、业务目标或可检测效应；不得看完结果后倒定 |
| 首个覆盖窗口 | 上线后真实读者开始看到新版的窗口 |
| 首个完整自然日 | 用于更稳定比较，不等同于“首次覆盖” |
| 干扰项 | 渠道、断更/复更、发新章、节假日、自访、同时改包装等 |

若用户确认某数据日的所有实际访问都发生在改动后，该日可视为已覆盖新版；完整自然日只提高可比性，不能机械地把前一窗口判成未覆盖。

工作流的机械日期绑定统一使用 `Asia/Shanghai`：先把带时区的 `published_at` 转为上海时间；`first_covered_data_date` 等于该本地日，只有恰好在本地 `00:00:00` 发布时 `first_full_data_date` 才等于同一天，否则为下一天。再用最新快照的 `data_until` 唯一推导三种覆盖状态：

```text
data_until < first_covered_data_date
  → NOT_COVERED
first_covered_data_date ≤ data_until < first_full_data_date
  → PARTIAL_DAY_COVERED
data_until ≥ first_full_data_date
  → FULL_DAY_COVERED
```

这三个状态描述“按统计日是否可能覆盖版本”，不证明当天每个访问者都看到新版；线上版本仍须单独给 `version_evidence`。不得手选更有利的覆盖状态，也不得把部分日覆盖写成完整日证据。

每次同时比较：

1. 修改前基线；
2. 前一日或前一快照；
3. 最新快照；
4. 有条件时再比较同星期、同渠道、同推荐阶段。

### Phase 3：按作品类型还原完整漏斗

#### 长篇小说漏斗

按以下顺序查看，但每层都保留事实表：

1. **资格与分发背景**：签约/推荐验证阶段、更新连续性、违规通知、书名封面简介或标签变更。
2. **阅读来源**：每日阅读人数，以及书城、分类、书架、继续阅读、搜索、其他的绝对 UV 与占比。
3. **包装承接**：只有拿到展示与阅读数据时才计算展示→阅读；没有曝光数据时不得用渠道阅读反推点击率。
4. **黄金前三章**：先取累计到达率 `R1/R2/R3/R4`；只有存在权威 cohort 基数或接口绝对人数时才还原 `A1/A2/A3/A4`。`R4/A4` 用于判断第3章是否把人带入第4章。
5. **深章推进**：检查最大绝对流失人数、最大条件跟读降幅和改动章附近的到达人数。
6. **回访与追读**：加书架、追更、催更、评论、评分与继续阅读入口；严格使用各自官方口径和合适的资格分母。
7. **近期活跃**：把在读人数按 14 天滚动窗口解释，拆分新进入日与滚出日。

有权威人数时固定计算：

```text
F1→2 = A2 / A1；L1→2 = A1 - A2
F2→3 = A3 / A2；L2→3 = A2 - A3
F3→4 = A4 / A3；L3→4 = A3 - A4
```

只有绝对人数来源权威、版本与口径可比时，才计算修改窗口增量 `ΔA1/ΔA2/ΔA3/ΔA4`。当 `ΔA1 > 0` 时可报告 `ΔA2/ΔA1`，但必须命名为“窗口增量到达比”，不得称为严格的新读者跟读率。若只有展示到达率，则直接计算 `R2/R1、R3/R2、R4/R3`；最小兼容下界只能做单快照一致性检查，禁止计算 `Δ下界`。

#### 短故事漏斗

按以下顺序查看：

```text
展示 → 阅读 → 15秒 → 30秒 → 60秒 → 触底 → 互动/转化
```

固定计算：

```text
点击率       = 阅读 / 展示
15秒留存     = 15秒人数 / 阅读人数
15→30承接率  = 30秒人数 / 15秒人数
30→60承接率  = 60秒人数 / 30秒人数
60秒后触底率 = 触底人数 / 60秒人数
整体触底率   = 触底人数 / 阅读人数
```

同时报告每段损失人数，例如 `阅读人数 - 15秒人数`。累计口径与按日求和口径分开；同一读者跨日可能在区间数据中重复，不能和全周期去重累计直接比较。

### Phase 4：识别异动并确定优先级

严格按 [references/anomaly-rules.md](references/anomaly-rules.md) 执行，先把变化分成：

1. **数据异动**：刷新滞后、空值、公式不一致、统计范围切换。
2. **流量异动**：阅读/展示量或渠道结构变化。
3. **转化异动**：在分母可比的情况下，某一漏斗转化发生变化。
4. **滚动窗异动**：在读人数等指标因新日进入、旧日滚出而变化。
5. **互动异动**：加书架、追更、催更、评论等资格人群行为变化。

异动识别后不得直接跳到正文。对每个命中节点执行 `dictionary/diagnostic-routes.v1.json` 中的固定路线：

1. 先检查数据质量门和指标自身分母；
2. 向上检查流量规模、渠道/包装和版本事件，判断是否只是上游传导；
3. 同层检查同义或互相校验的指标，排除字段滞后与统计范围变化；
4. 向下检查绝对到达、条件转化和护栏，判断是否存在额外流失；
5. 只有剩余解释仍指向可编辑内容时，才生成具体文本读取范围。

每条异动必须保存 `metric_id`、当前值、基线、绝对变化、相对变化/百分点、分子分母、历史噪声、MDE、样本状态、必查邻接节点结果、替代解释和证据等级。若目录未给出万能阈值，就使用本书同口径历史基线；不得临时创造“平台及格线”。

异动的基线和当前值不得手抄。`baseline_fact` 与 `current_fact` 必须分别用 `metric_id + 完整 dimensions` 唯一命中冻结事实表中的一行；`baseline/current` 必须等于所选事实值，`delta = current - baseline`，`effect_size` 使用同一带符号、保单位的差值，`direction` 由差值机械推导。selector 命中 0 行或多行、事实非数值、delta 无法复算时，该异动不能通过分析门。

给关键判断标注证据性质：原始观测 `OBSERVED`、可复算派生 `DERIVED`、相关 `ASSOCIATION`、待验证假设 `HYPOTHESIS`；只有随机实验或可信准实验才使用 `CAUSAL`。

优先级不要只看最大百分点，依次考虑：

- 是否为数据错误；
- 有权威分母时的受影响绝对人数；没有时用到达率/百分点并显式降级；
- 是否位于上游，影响后续多少读者；
- 与最近改动是否位置和时间对齐；
- 是否有足够样本和可比基线；
- 修复成本与副作用。

只有节点进入人数为权威绝对人数时，才可计算“可挽回人数”辅助排序：

```text
可挽回人数 ≈ 该节点进入人数 ×（合理目标转化率 - 当前转化率）
```

“合理目标”优先取作品自身稳定历史、同渠道改前基线或预先设定的最小有意义变化，不使用未经证实的平台万能及格线。

最终状态与方向分开写：

- `样本不足；方向上行/下行/持平`
- `改善/恶化（方向性，未达强结论）`
- `改善/恶化（较强证据）`
- `无明显变化`
- `数据未覆盖改动`
- `样本受自访污染`

结论必须逐项绑定改动，不得只给整本书一个状态。`analysis.change_assessments[]` 必须与 `window_bound.changes[]` 的 `change_id` 一一对应，同时保留覆盖状态、线上版本状态、实际评估的目标指标、证据和理由。改善/恶化不是简单的“数值向上/向下”：必须根据 `metrics.v1.json` 中该指标的 `preferred_direction_by_metric` 解读；例如流失人数下降才是改善。未覆盖的改动必须使用“数据未覆盖改动 + UNKNOWN”；样本不合格时不得用单个比例方向把改动升格为改善或恶化。

不要强行只选一个瓶颈。输出“首要约束、次要风险、暂不可判定项”；优先解决最上游且可挽回人数最多的有效异常。

### Phase 5：从指标断点下钻到具体文本

只有完成漏斗定位后才读正文，但一旦提出改文建议，必须真的读取数据指向的文本。不得只凭指标给“加强钩子、加快节奏”之类空话。

执行顺序：

1. 找到平台已发布版本对应的本地文件；确认本地稿与线上稿是否一致。
2. 读取断点前的承诺、断点章全文、下一章标题与开头；短故事按 300/1000/2000 字附近读取实际段落，并结合自然场景边界。
3. 标记读者在离开前已经知道什么、期待什么、付出了多少理解成本，以及下一步为何不值得继续。
4. 从短承诺兑现、信息增量、冲突升级、主角主动性、收益与代价、情绪强度、逻辑连续性、题材兑现、毒点与价值观排斥等维度找证据。
5. 引用具体章节、段落或行号，写清“文本现象 → 读者心理机制 → 指标表现”。
6. 多个候选原因并存时按证据强弱排序，先提出最小且可区分原因的修改，不把所有想法一次塞进正文。

具体映射和检查表见 [references/text-drilldown.md](references/text-drilldown.md)。

### Phase 6：把修改想法写成因果假设

每项建议必须使用以下结构：

```text
数据证据：哪个分子/分母在什么窗口异常
文本证据：具体章节/段落存在什么可观察问题
流失机制：该问题为什么会让这一节点的读者离开
修改动作：删/移/压缩/前置/补偿/升级/重写哪些内容
因果链：修改如何改变读者当下判断，从而影响哪个主指标
护栏：哪些上游承诺、人物逻辑、后续伏笔和指标不能受损
验证：何时、用什么基线和样本判断成功或失败
```

提交建议前做“逻辑闭环检查”：

- 修改位置是否在读者离开之前？
- 修改是否直击已识别机制，而非换一种写法重复原问题？
- 是否更早兑现书名/简介/导语承诺？
- 是否新增明确的信息、行动、代价或未决问题？
- 是否保留人物动机、世界规则、时间线和后续伏笔？
- 是否可能提高目标指标却伤害点击、前段留存或长期追读？
- 是否只动一个主变量，发布后能够归因？

若可用子 Agent，修改方案至少经过一次结构/读者体验审查；涉及设定或跨章因果时，再经过一致性检查。审查目标是验证因果链和副作用，不是追求辞藻。

若未来运行宿主提供 `HOST_ATTESTED` 授权并允许“本次数据分析 run”执行修改或发布，执行命令还必须携带并与授权 artifact 精确匹配：

```text
--analysis-run <run_id>
--analysis-proposal <proposal_id>
--analysis-action modify_text|modify_packaging|publish
--analysis-target <exact_target>
--analysis-target-sha256 <remote_payload_sha256，仅远端目标必需>
```

`text_diagnosis.proposals[]` 必须先登记相同的 `proposal_id/action/target/target_sha256_before`。hook 会核验 supervisor PASS、完整 hash 链、authorization 状态以及 proposal/action/target/hash 四方一致；这些只是未来受信执行器的附加条件，不是当前的执行许可。普通日更不携带这些参数，不受数据分析门禁影响。

当前运行时只能记录 `attestation_status=UNATTESTED_PROCEDURAL`：它把用户消息 hash、事件 ID、run、chain head、proposal、action、target 与改前 hash 绑定成可审计记录，但没有宿主提供的不可伪造用户事件签名。自动执行门要求 `HOST_ATTESTED`，而当前运行时不能生成该状态。因此即使写入了 `APPROVED` 程序性记录，也**禁止由本工作流自动改正文、改包装或发布**；只能把方案交给用户人工执行，或由将来能提供宿主签名的受信执行器重新授权。命令参数和 hook 命中都不能把 `UNATTESTED_PROCEDURAL` 升格成可执行授权。

### Phase 7：发布后验证

发布前记录：原文位置、修改摘要、发布时间、主指标、护栏指标、预期方向、最小有意义变化和干扰项。

发布后：

1. 先确认数据窗口确实覆盖新版；无新增合格样本时写“无新样本”，不要写“修改无效”。
2. 每日看早期方向，但把番茄官方建议的约一周观察期作为主要复盘窗口；首日受字数和刷新影响时单独标注。
3. 同时对比改前基线、前一快照、最新快照，并检查渠道构成是否变化。
4. 主指标上升但护栏明显下降时，不判成功；找出副作用并决定回滚或二次小改。
5. 多项改动重叠、流量阶段改变或自访污染时，降低归因强度。
6. 把核算后的数据、权威绝对人数（若有）、展示率、改动时间、判断依据和下一验证日追加到数据日志；最小兼容下界必须单列且不可跨日相减。不要篡改历史结论，需纠正时追加勘误。

## 样本与结论强度

以下为内部分析准则，不是番茄官方阈值：

- 有效样本 `< 30`：状态写“样本不足”；仍报告原始观测、展示率方向和已有的权威绝对变化，不把兼容下界当样本或人数，不做因果归因。
- 有效样本 `30–99`：只下方向性结论；要求绝对人数与比率同向、可比窗口至少两次同向或聚合窗口超出自身基线噪声。
- 有效样本 `≥ 100`：结合置信区间、预设最小有意义变化和护栏指标，才可给较强结论。

这里的“有效样本”仅指 `sample_size_qualified=true` 且全部样本证据权威、可从冻结源复算的分母。样本不可用时按 `sample_size=0 + sample_metric_id=UNAVAILABLE` 进入“样本不足”，不能把这个状态编码解释为实际零读者。

样本量不是唯一条件。即使人数足够，只要渠道、版本、统计口径或推荐阶段不可比，也要降级。

## 输出格式

先给一句不回避方向的结论，再给证据：

```markdown
# 一句话结论
数据截至 YYYY-MM-DD；[改动]当前状态为[状态]，方向[上行/下行/持平]；主要瓶颈在[漏斗节点]。

## 1. 数据质量与覆盖
- 更新时间/截止日：
- 可用与滞后字段：
- 改动覆盖窗口：
- 样本与污染风险：
- 指标目录/方法/运行 ID：

## 2. 漏斗对比
| 节点 | 修改前基线 | 前一快照 | 最新 | 绝对变化 | 转化变化 | 状态 |

## 3. 异动与问题定位
- 最大有效异动：
- 受影响绝对人数（仅权威来源；否则写不可得）：
- 首要约束 / 次要风险 / 暂不可判定项：
- 已完成的上游/同层/下游/护栏联查：
- 排除的替代解释：

## 4. 文本下钻证据
- 位置：第N章第X段 / 第X–Y字
- 原文现象：
- 读者心理与流失机制：

## 5. 修改实验卡
- 具体修改：
- 逻辑因果链：
- 主指标：
- 护栏指标：
- 最小有意义变化及来源：
- 风险与一致性检查：

## 6. 验证计划
- 首个覆盖窗口：
- 主要复盘窗口：
- 成功/失败判据：
- 下一步：

## 7. 工作流验收
- Requested / Effective Mode：
- Validator：PASS / REWORK / NOT_RUN
- Supervisor：PASS / RETURN / BLOCKED / NOT_RUN
- 证据强度上限与未过门禁：
```

日报可以压缩，但必须保留：数据截止日、数据是否正常、当前方向、绝对增量、前三章或短故事分段漏斗、瓶颈位置、具体修改/观察动作、下一验证时间。

## 知识维护

知识层只维护两类内容：

- `methods/`：指标口径、计算方法、异动检测、归因边界、文本映射、实验与复盘方法；更新时记录来源、适用范围、版本和反例。
- `cases/`：经完整门禁复核的分析案例；必须保存数据上下文、指标版本、异常与联查、文本证据、修改假设、替代解释、结果状态和适用边界。

案例分开标记“分析质量已验证”和“改动效果已验证”。没有发布后合格窗口的数据，只能是 `outcome_unverified`；无效果、回退和无法判断的高质量案例同样值得保留，不得只沉淀成功故事。任何晋升都通过 workflow CLI 的 `promote-case` 或 `promote-method`，并由 `REPORT_COMPLETE + validator PASS + supervisor PASS + 完整 hash 链` 背书；方法修订必须创建新版本并声明 `supersedes`，不得覆盖旧版本。

`verified_improvement / verified_regression / verified_no_effect` 还必须由至少两个**不同冻结最新快照窗口**的完整验证 run 支持；run ID 不同但 `latest_snapshot.source_sha256 + data_until` 相同仍算同一个窗口，禁止复制同一快照制造“复现”。每个验证 run 还须完整日覆盖、线上版本已验证、权威合格样本不少于 100、validator/supervisor 通过，并与同一 `change_id` 和结果方向一致。

晋升采用事务式写入：promotion artifact 内嵌待晋升知识文档并进入 hash 链，随后创建知识文件。崩溃留下的未提交 `*.attempt-*.json` 或已提交但缺失的知识文件，只能运行 `scripts/data_workflow.py recover --run-id <run_id>` 恢复；recover 会把孤儿 attempt 移入该 run 的 `recovery/<timestamp>/` 隔离目录（不删除），并且只从已提交、hash 匹配的内嵌文档重建缺失知识。recover 不推断业务事实、不推进状态，也不能修复无有效证据链的产物。

## 禁止输出

- “推荐为 0，所以正文一定没问题。”
- “继续阅读为 0，所以没有任何人跨日回来。”
- “加书架为 0，所以算法直接不给量。”
- “第 N 章读完率低，所以第 N 章差。”
- “跟读率低，只要把最后一句改成悬念。”
- “比例下降，所以作品恶化。”
- “样本不足，所以什么都看不出来。”
- “改完一定会涨。”

把这些句子改写成有口径、有绝对人数、有方向、有不确定性和可验证动作的结论。
