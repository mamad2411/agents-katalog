---
name: project-work-log
description: 为长期项目建立并维护工作记录体系（过程记录 + 索引台账 + 经验手册，统一收在 work_log/ 容器里），不限编程——软件、研究、写作等跳会话或跨周持续投入的项目都适用。当用户要「开始新任务」「留下记录 / 建工作日志」「总结经验 / 复盘」「整理台账 / 待办」「归档旧记录」时使用。
---

# 项目长期工作记录（project-work-log）

> **来源与免责声明**：本技能的约定、文档与脚本整理自作者使用 **DeepSeek Flash 系列模型**处理内容时的常用操作，
> 并**完全由 DeepSeek Flash 系列模型整理生成**（未经人工逐条校验）。
> 使用时请自行甄别，**不保证效果、正确性与适用性**；建议先小范围试用，再按项目的实际情况调整。

## 这是什么

把"项目里发生过什么、怎么验证的、留下了什么可复用经验"沉淀成**三层、可检索、可校验**的文档体系。
三层同住**一个容器目录** `work_log/`（默认名，可配置），内部各有分工：

| 层 | 位置 | 职责 | 生命周期 |
|---|---|---|---|
| **过程层** | `work_log/NNN-*.md`（编号式）或 `work_log/YYYY-MM-DD-*.md`（日期式）；分卷后 `<YYYY>/…` | 一篇记录一次工作（一篇覆盖多少，见下「记录精细度」） | append-only，收口后不改写 |
| **索引层** | `work_log/README.md` | 分阶段索引 + 同主题簇 + 滚动待办 + 当前状态块（**可选**） | 每次收尾更新 |
| **经验层** | `work_log/lessons/*.md` | 提炼后的可复用知识：症状 → 根因 → 做法 → 来源 | 持续追加，每条必须有来源 |

记录正文的**小节自由**：不规定节次的数量、名称与顺序。唯一的硬要求是**一个验证类小节**。

一句话：**过程留证据，索引管导航，经验可复用**。三层不互相复制内容。

**这是一份工作记录，不是变更日志。** 它记的不只是代码变更——工作区整理、取证与复核、环境与资产变动都记，
所以 `变更集` 只是可选字段（实测 162 篇里有 146 篇写「无」）。

### 两种命名约定（都认）

| 约定 | 文件名 | H1 必须写成 | 用在哪儿 |
|---|---|---|---|
| **编号式** | `NNN-<slug>.md`（编号 1–3 位） | `# NNN · <标题>` | 原型 207 篇、`comfy` 30 篇 |
| **日期式** | `YYYY-MM-DD-<slug>.md` | `# YYYY-MM-DD <标题>`（日期后可接行内实验号，如 `R21：`） | `embeding try` 71 篇 |

- 两种都要求 **H1 与文件名一致**；**文件名两种都不匹配的文件不是记录**，工具会直接忽略，不会半解析。
- 「编号单调递增、永不复用、归档不改号」**只在编号式容器里生效**。
- 「编号式：回指写编号 `wl/209`；日期式：回指写文件名 `2026-09-06-门控两段式.md`」。
- 一个容器内**建议只用一种**（混用会让排序与索引变乱）；混用不报错，只提示一句。
- 引用地址不引入短锚点编号：文件名/编号已经唯一自明。

容器里的其他固定位置：归档记录在 `work_log/<stage>/…`（阶段目录直接建在容器下最省事；
多主题长项目可以用**归档层** `archive/` 把归档收在一处，写成 `work_log/archive/<主题>/<阶段>/`，
两种工具同等对待 —— 判据只有「相对容器路径的第一段不是 4 位年份 ⇒ 已归档」）、
旧状态块在 `work_log/STATE-HISTORY.md`、
旧记录声明（可选）在 `work_log/LEGACY.md`、日志与运行产物在 `work_log/logs/<来源>/`。
归档明细落**归档目录自己的索引** `work_log/archive/README.md`（一行一个阶段，
`archive --stage` 自动补/并那一行，正文由人写）；归档目录直接建在容器下的项目没有这一层，
明细就在台账的文件索引里（`index compact --stage X` 折成一行区间）。老容器可能还留着一份
`ARCHIVE.md`（曾经的归档索引，2026-10-16 起工具不再写它，`check` 只提示一句可删）。
完整布局与「日志归位要求」见 [references/conventions.md](references/conventions.md)。

> **领域无关**：这套结构不限于编程。三个标签各自认一组同义词：
>
> - **迭代**：`迭代 / 变更集 / 批次 / 阶段 / 版本 / 里程碑`（英文 `Iteration / Milestone`）
>   —— 全部**可选**，`变更集` 尤其只是其中一个别名，缺了不算错。
> - **验证小节**：`验证 / 复核 / 检查 / 评审 / 结果 / 证据 / 评估 / 确认 / 实测 / 审查 / 实验 / 判定 / 评测`
>   （英文 `Verification / Review / Results / Evidence / Tests`）；标题级别 h2–h4 都认
> - **可核对的内容**：数字、百分比、命令、引用输出、表格、对照都算
>
> 各领域的写法：研究项目 `批次：3` + `## 结果`（样本量、结论、反例）；写作项目 `版本：v2` +
> `## 评审`（编辑意见与处理）；软件项目 `变更集：154` + `## 验证`（测试命令与通过数）。
>
> ⚠ 一个标签一个值：写 `迭代：3`，**不要**写 `迭代 / 批次：3`（解析不出来）。

这套体系来自一个真实项目的 `work-log/` + `lessons/` 实践；基线分析（哪些沿用、哪些坑要避开）见
[references/analysis.md](references/analysis.md)。

## 何时用

- 用户说"开始一个新任务"——先确认/建立这套结构，再开工。
- 一项工作 / 一个迭代完成后要"收尾/留记录/更新台账"。
- 要"总结经验/整理踩坑/做复盘/归档旧东西"。
- 接手一个已有 `work_log/`、`journal/`、`work-log/`、`lessons/`、`docs/` 记录体系的项目，要按既有约定续写
  （旧名 `journal/`、`work-log/` 与顶层 `lessons/` 都能被识别，**只读取、不迁移**）。
- **长项目开工时由模型主动建议**——判据与问法见下「开工先问一句（要不要用这套）」。

## 开工先问一句（要不要用这套）

**这道闸是给模型的，不是给用户的**：新项目开工时先判一次，够格就**问一次**，别默认建、也别默认不建。
判据是**收益侧**的——"项目长不长"不作数（体系本来就可以中途补建）：

| 信号 | 说明 |
|---|---|
| 跨会话 / 跨周 | 会话清空后会丢结论的活 |
| 有会被回指的决策 | 后面必然要问"当初为什么这么定" |
| 结论要带证据 | 得给得出命令、数字、对照，而不是"我记得" |
| 已有踩过的坑 | 需要"症状 → 根因 → 做法"能复用 |

- **满足两条及以上就问**；一条不满足就**不提**（省一轮交互）。
- **负触发**（直接不提）：单次问答、一次性脚本、探索性原型（本来就要丢）、两小时内能收的活。
- **问法固定一次，用选项问**：① 建全套（过程 + 台账 + 经验）② 先不建，需要时中途再立
  ③ 只建经验层（`lessons/`，不要过程记录）。
- **时机**：只在"准备开工"那一刻问，得到答复再往下走；**不要干到一半才回头问**。

## 铁律（先看这 8 条）

1. **先记录、后动手**（方案类）：先写清"要解决什么 + 选项 + 建议默认值"，用户确认后再实施；有疑问先记录，不擅自改。
2. **一篇 = 一个可交付的子单元**（默认档 `full`；档位可调，见下「记录精细度」）。
   一次会话里做了几件可交付的事，就开几篇——实测同一天 8–34 篇是这个体系的**正常节奏**
   （原型 2026-09-13 一天 34 篇），粗档位会把它们并成一篇、埋掉可独立查阅的单元。
   纯调研/一次性记录把迭代字段写 `-`；日期式容器不分配编号。
3. **篇号与迭代号分开**：篇号是文件名/标题/回指用的地址（`wl/NNNN`，只有编号式才有）；迭代号只写在迭代字段
   （默认 `迭代：`，也认 `变更集/批次/阶段/版本/里程碑`）。**两个计数器独立发展，从不对应**——
   原型实测「变更集号 = 篇号」**0 例**（篇 207 → 变更集 182）。
4. **历史不改写**：收口后不抹旧结论；被推翻时**追加** `## 更正`（日期 / 原结论 / 新证据 / 现结论）。
5. **验证要有可核对的内容**（数字 / 百分比 / 命令 / 引用输出 / 表格 / 对照）与结果；
   没做的必须写明"未覆盖 + 原因"。光说"完成了""应该没问题"不算验证，**只写设置不写结果也不算**。
6. **经验必有来源**：lessons 每条带 `（wl/NNNN）`（日期式容器写文件名），来源不存在就不许写。
   **复发过或代价极大**的写成卡式条目（主行 + 缩进子条目 `触发 / 验证 / 别再来`）；
   触发词写任务里会出现的**现象词**，不写学科名。`check` 只认缩进子条目这一种形制，
   旧条目里的「触发条件」不会被命中（见 `conventions.md`「经验层」）。
7. **台账最多一个 `## 当前状态`**：有就校验新鲜度，**没有不算错**（状态也可以写在每篇开头）；
   换新块时旧块整段剪到 `work_log/STATE-HISTORY.md`。
8. **编号式容器：编号永不复用、归档不改号**；归档只 move + 改链接。日期式容器没有编号，这条不适用。

**小节结构是自由的。** 唯一硬要求是**一个验证类小节**。六段式（背景→事实→方案→执行→验证→遗留）
仍然可用，但它现在是**模板之一**，不是必填——实测 `embeding try` 71 篇里出现了 409 个不同的 `##` 标题，
最高频的也只出现 2 次：结构是长出来的，强行套模板只会让人绕开它。

完整约定见 [references/conventions.md](references/conventions.md)；模板见 [references/templates.md](references/templates.md)。

## 记录精细度（一篇 = 什么）

默认档是 `full`：**一段可交付的子单元就是一篇**，一次会话可能开出 2–3 篇。
档位存在台账 `## 当前状态` 的 `精细度` 字段里。字段随容器走、进版本控制。
新项目的初始档位写在项目配置文件 `<容器>/.config.json` 的 `mode` 里（可选）；台账一旦有 `精细度`，台账说了算。

| 档位 | 一篇 = | 一次会话的预期产出 |
|---|---|---|
| **`full`（默认）** | 一个可交付的子单元 | 2–3 篇；同一天多篇很正常 |
| `session` | 一次会话，或一个可交付成果 | 最多 1 篇；同一会话里的第二件事**追加到同一篇** |
| `digest` | 一个阶段 / 跨多次会话 | 多次会话并成一篇 |
| `milestone` | 一个阶段收口 | 只留决策与经验 |

> 为什么默认是 `full`：实测原型 111 篇带日期的记录分布在 **12 个日期**上（平均 9.2 篇/天，
> 最多一天 **34 篇**），`embeding try` 也有一天 8 篇。`session` 档会把 09-13 那 34 篇压成**一篇**——
> 那不是更简洁，那是把 34 个可独立查阅的单元埋进一个文件。`session` / `digest` / `milestone`
> 保留给确实低强度、以阶段为单位的项目（写作、调研、运维）。

档位只决定**要不要另起一篇**，以及可选叙述写多细。**验证要求不随档位放宽**：任何档位下，一篇记录都必须有可核对的验证小节（铁律 5）。

`digest` / `milestone` 还多一条义务：**写明这一轮刻意没有记录什么**，例如
`未记录：本轮的两处配置调整，见提交 abc1234`。粗粒度合并了多轮会话，不写这一句就等于静默丢信息。

怎么切档：

- **在会话里说一句**（临时）："这次记详细点" / "按阶段汇总就行" → 本轮按 `full` / `digest` 写。
  口头说的只管这一轮，工具不知道。
- **改台账**（持久）：`python scripts/journal.py mode --set digest --why "阶段收口"`。
  之后所有会话都按新档位走，`brief` 里直接看得到。

查看当前档位：`python scripts/journal.py mode`。台账里没有 `精细度` 字段的老项目取配置文件的 `mode`，配置也没有就按内置默认 `full`，都不会报错。

## 工作流 A · 初始化（项目第一次用）

0. **先判一次要不要用**：按「开工先问一句」的四条信号判断——满足两条及以上就问**一次**
   （建全套 / 先不建 / 只要经验层），得到答复再往下走；一条都不满足就别提，直接干正事。
   **用户已有明确要求（"建个工作日志"）就不用问**——那是他的决定，不是待议项。
1. 先查已有体系：`ls` 项目根，找 `work_log/` `journal/` `work-log/` `lessons/` `docs/` 以及根 `README.md` / `CLAUDE.md` / `AGENTS.md` 里的记录约定。
   **已有体系就沿用它的命名与编号，不新建平行目录。**
2. 没有则按 `references/templates.md` 落盘（容器名默认 `work_log/`，可用 `--work-log NAME` 改）：
   - `work_log/README.md`（台账模板）
   - `work_log/lessons/README.md` + `work_log/lessons/01-<topic>.md`（先建 3–5 个与本项目相关的分册）
   - `work_log/_inbox.md`（踩坑收件箱；模板见 `templates.md` §9）
   - `work_log/STATE-HISTORY.md`（`ARCHIVE.md` **不用建**：归档明细归
    `work_log/archive/README.md`，那个文件在第一次归档时由 `archive --stage` 自动建）
   - 有日志/运行产物的项目同时建 `work_log/logs/<来源>/`（见下「日志归位」）
   - 在项目根 `README.md` 加一行指向 `work_log/README.md`
   - **问一次**：要不要把「经验层」钩子写进本项目的 `AGENTS.md` / `CLAUDE.md`（模板见
    `templates.md` §10）。**不自动写** —— 不同宿主认的指令文件不同，得到答复再落盘。
   - **可选**：`work_log/.config.json` —— 项目配置文件，写默认档位与旧记录清单。
     不想写就不写：缺它等于全部用内置默认。要写就用 `config --write`，别手抄。
3. 跑一次 `journal.py check --strict` 确认骨架自洽（此时 0 篇记录也应通过）。
   台账模板里的**示例索引行**要先删掉或换成真实文件名，否则被判死链。

## 工作流 B · 一项工作（日常）

```
记录 → 确认 → 执行 → 验证 → 收尾
```

1. **记录**：先看档位——`python scripts/journal.py mode <项目根>`。
   默认档 `full` 下，**一个可交付单元一篇**；同一件事跨了多次会话就 `append` 续写原篇，
   还没交付完的小步合在一起。
   新开时用 `python scripts/journal.py new <项目根> --title "标题" [--iter N]`。
   入口字段**都可选**：`日期 / 迭代 / 触发 / 范围 / 结论` 按需要写；日期式容器把日期写在文件名与 H1 上即可。
2. **确认**：方案、口径、取舍写进记录；等用户拍板（涉及数据/破坏性操作必须确认）。
3. **执行**：小步做、每步可回退；做了什么记进正文（用小节，不强制名字）。
4. **验证**：用该项目能给出的核对方式（测试、数据、引用、样本、评审），把**依据 + 结果 + 未覆盖**写进验证小节。
5. **收尾**：见工作流 C。

## 工作流 C · 收尾清单（每篇记录都走一遍）

1. 记录补齐：入口字段按需要写 + **一个验证类小节（含结果，不只是设置）**。
   档位是 `digest` / `milestone` 时，再加一句「未记录：…」（见上「记录精细度」）。
2. 台账（有台账时）：索引表加一行；涉及跨篇主题就更新「同主题簇」；滚动待办增删。
   有 `work_log/目标.md`（**可选，多个长期目标并行推进时才建**，见 [references/conventions.md](references/conventions.md)「目标」）
   就顺带更新那一行的「状态」——状态人工维护，不从记录推导。
3. **状态**：台账里**有** `## 当前状态` 就更新它（8 个字段：`阶段 / 版本`、`迭代`、`产出`、
   `核对 / 验证`、`交付物与指纹`、`环境`、`阻塞 / 等待`、`精细度`），并让日期不早于最新一篇记录。
   台账里**没有**状态块不算错——状态也可以写在每篇开头的引用块里（`> 状态：… ｜ 工具：… ｜ 产物：…`）。
   字段名按台账写法原样保留 —— `--set "核对=…"` 会落到 `核对 / 验证` 上（短名可识别），不要手改成新字段。
   **别把台账当普通文件整读再手改**：先 `brief`（一屏），写用 `status --set` / `todo` / `index sync`
   —— 台账是热面，整读既贵又容易读到一半就改。`产出` 只留最近一段坐标，旧段落剪进 `STATE-HISTORY.md`。
4. **经验**：在说出「完成 / 搞定了 / 修好了」**之前**，先看 `work_log/_inbox.md` ——
   够格的（复发过的 / 代价大的）整理进 `work_log/lessons/` 对应分册并删掉那一行，小意外留着下次；
   卡式条目用 `lesson add --trigger … --verify … --avoid …` 生成。
   本轮若有可复用结论而 inbox 没记，直接写也照旧：写进分册并回填来源（编号式 `（wl/NNNN）`、
   日期式写文件名）。
5. **校验**：`python scripts/journal.py check --strict <项目根>`。
   旧记录不会因此变红——见下「渐进原则」。
6. **日志归位**：本轮产生的持久日志 / 运行产物放进 `work_log/logs/<来源>/`，别留在项目根（见下「日志归位」）。
7. 提交：代码与文档一起提交；提交信息引用篇号或文件名（如 `work_log: 0042 ...`）。

### 渐进原则：老记录只报不拦

新写的记录按新规格判错；**改动之前写下的记录只报 info**，免得第一次跑就是一片红、然后学会忽略这个工具。

判定依据是**显式清单**，不是日期启发式（日期不可靠：实测同一份语料里日期字段只覆盖一半）：

1. 容器里记着一份 `work_log/LEGACY.md`，逐条列出旧记录（`- 0007-*`、`- archive/**`）；
2. 或调用时给 `--legacy <glob,…>`；连空串也算显式（`--legacy ""` = 没有旧记录，全按新格式判）；
3. 两者都没有时按**容器规模**兜底：记录 **≥ 5 篇**的容器整批算旧记录（老项目零配置也是干净输出），
   **少于 5 篇**的容器算新项目（写坏的记录照报 error——新规格该红就红）。

这条兜底的代价是**双向的**，两个方向都要认：

- **体量小的老项目**会被当成新项目（多报几条）—— 用 `LEGACY.md` 一次收准。
- **成熟项目里新写的记录也会被当成旧记录**：缺验证小节、缺入口日期行只报 INFO，
  `check --strict` 照样绿 —— 也就是说**门禁在成熟容器里默认不再拦新记录**，而"长期项目"正是它的目标场景。
  `check` 每次都会把这件事**打印一行**（在门禁报告之外：不算发现、不计入 error/warn/info、不改退出码，
  `--quiet` 时不打）；要恢复对新记录的判定，就写 `LEGACY.md` 把老记录钉死，或用 `--legacy ""`。

只有「因旧格式而失败」的三类发现受它影响：**H1 形制**、**入口 `日期：` 行**、**验证小节**。
死链、漏索引、lessons 来源这些**从来就有**的客观规则永远照报。
降级的条目照样打印，级别是 `[INFO]`，末尾还会告诉你降了几条。

## 工作流 D · 归档、瘦身与复盘

- **归档判据 = 阶段收口**（某个阶段结束、索引表不再增长），不用"多少天没引用"这类经验值。
- 归档 → 瘦身 → 复盘，三步都是命令，不再手工搬文件：

```bash
python scripts/journal.py archive --stage 02-research --from 27 --to 45   # 搬 + 全仓链接重写 + 死链自检
python scripts/journal.py archive --stage 研究/01-采样 --from 46 --to 52   # 多级：可加一层主题
python scripts/journal.py archive --stage archive/工作记录/05-返工 --from 77 --to 84   # 收进归档层 archive/
python scripts/journal.py index compact --stage 02-research               # 已归档小节折叠成一行区间
python scripts/journal.py index compact --depth 2                         # 折多级小节：深度 = 路径段数 + 1
python scripts/journal.py retro --from 27 --to 45 --out /tmp/retro.md     # 阶段复盘骨架
```

- 很久以后，已归档、又没人引用的记录可以**冷存**（默认只报告，打包后才移出，**绝不直接删**）：
  `prune` → `prune --zip cold.zip` → `prune --zip cold.zip --apply`
- 记录成千上万时用 `split --by-year` 按年分卷（`wl/NNNN` 回指不受目录变化影响）。
- 复盘写进 `work_log/lessons/99-retrospectives.md`（阶段表 / 成果 / 可复用发现 / 遗留），**不要**另建 SUMMARY 文档到处写同一批数字。
- **证据不删**是硬规则：清理 = 移走 + 汇总 + 留清单，不是删除；搬动后必跑 `check` 确认 0 死链。

## 工作流 E · 把教训带出去（跨工作区）

一个工作区里确证过的教训，要让**别的工作区**也用得上，走全局记忆这一层
（默认落在 `<用户主目录>/dsh-lore-memory`，**不在工作区里**；`--memory`、设置文件里的
`memoryDir`、`$DSH_WORKLOG_MEMORY` 都能把它指到别处）。三步，每步都由人决定要不要走：

```bash
python scripts/journal.py memory publish --applies-to dsh-plugin --upload   # 1. 声明：哪些教训允许外流
#   ↑ 清单里那句话就是全局条目的正文，把它改成**能带走**的措辞
python scripts/journal.py memory collect                                    # 2. 收集（幂等，可重复跑）
python scripts/journal.py memory lint --strict && python scripts/journal.py memory index  # 3. 过门禁、重建索引
```

- **准入靠来源分档**，不靠"看起来重要吗"；`manual:inferred` 允许进，但**不进索引**。
- **`upload` 默认 `false`**：不显式打开，什么都不会外流。这是双向白名单。
- 想让它变成技能（而不是一条记忆）就 `promote suggest` 看够不够格 —— **只报候选，不自动打包**。
- 机制、条目格式、来源分档、生命周期见 [references/memory.md](references/memory.md)。

## 日志归位（任何产出都要归位）

- **持久日志 / 运行产物一律进容器并分类**：`work_log/logs/<来源>/`，一个来源一个子目录
  （例 `work_log/logs/build/`、`work_log/logs/bench/`）。**别散落在项目根，更别写到项目之外。**
- **测试夹具、一次性样本不是记录**，不进 `work_log/`。
- 日志里**不写绝对机器路径**，只写相对项目根的路径（脱敏后再落盘）。

完整表述见 [references/conventions.md](references/conventions.md) 的「日志归位要求」。

## 工具（`scripts/journal.py` / `scripts/journal.mjs`，纯标准库）

**核心用法：少读、少写、可校验。** 完整命令说明见 [references/commands.md](references/commands.md)。

> DSH 桌面版：把下文的 `python scripts/journal.py` 换成 `node scripts/journal.mjs`——
> 启动器会找 DSH 自带 Python 运行时，不必另装 Python。非 DSH 环境继续用 Python 即可。

```bash
ROOT  # 可省略，默认当前目录

# —— 少读：别整读 50 KB 索引 ——
python scripts/journal.py brief                 # 一屏：当前状态 + 待办 + 近期记录
python scripts/journal.py snapshot --entries 12 # 最近 12 篇的入口元信息汇总（只读，不改文件）
python scripts/journal.py show 42               # 单篇大纲（编号式按篇号）
python scripts/journal.py show 2026-09-06       # 日期式按日期，也可给文件名
python scripts/journal.py search "会话格式"      # 定向检索（记录+经验，只回命中行）
python scripts/journal.py outline               # 全部记录一行表

# —— 少写：外科式编辑，支持 --dry-run，保留 CRLF ——
python scripts/journal.py new --title "…" --iter 154 --insert --stage "A. 起步"
python scripts/journal.py status --set "迭代=154" --set "核对=抽样 30 条全部通过" --date   # 改状态块（--roll 归档旧块）
python scripts/journal.py mode                                                                  # 当前精细度（默认 full）
python scripts/journal.py mode --set digest --why "阶段收口"                                      # 切档位，附一行原因
python scripts/journal.py config                     # 项目配置文件：每个字段的生效值与来源（命令行/配置文件/内置默认）
python scripts/journal.py config --write             # 按当前生效值写出 <容器>/.config.json
python scripts/journal.py config --set mode=digest   # 改一项，保留其余字段与换行风格
python scripts/journal.py auto --list                # 自动操作 profile：内置 orient / verify / close
python scripts/journal.py auto --run orient          # 一次跑一组固定命令（开工：brief）
python scripts/journal.py auto --set-profile close \
        --command "index sync" --command "check --strict --lint"   # 把收尾动作写成 profile
python scripts/journal.py todo --add "…" | --done "子串" | --drop-done
python scripts/journal.py index sync --stage "B. 迭代"            # 补漏掉的索引行
python scripts/journal.py lesson add --volume 04-verification-and-safety.md --source 152 --text "…"
python scripts/journal.py lesson add --volume 01-host.md --source 152 --text "…" \
        --trigger "改完 lib/client.js，邻居界面丢样式" --verify "querySelectorAll('style:not([data-plugin])').length === 0" \
        --avoid "把标记写成 data-plugin-css（不在宿主判据里）"   # 卡式条目：触发 / 验证 / 别再来
python scripts/journal.py append 42 --section 更正 --text "…" --bullet

# —— 整理与清理：只搬不删，全部支持 --dry-run ——
python scripts/journal.py archive --stage 02-research --from 27 --to 45   # 归档 + 链接重写 + 死链自检
python scripts/journal.py archive --stage 研究/01-采样 --from 46 --to 52   # 多级归档（加一层主题）
python scripts/journal.py archive --stage archive/工作记录/05-返工 --from 77 --to 84   # 或者收进归档层 archive/
python scripts/journal.py index compact --stage 02-research               # 索引瘦身（已归档小节→一行）
python scripts/journal.py index compact --depth 2                         # 折多级小节（深度 = 路径段数 + 1）
python scripts/journal.py split --by-year --dry-run                       # 按年分卷（超长期，编号式）
python scripts/journal.py prune                                           # 冷存候选（只报告）

# —— 可校验：两道门禁（有 ERROR 退出码 1）——
python scripts/journal.py check --strict        # 结构：标题/日期/验证/死链/漏索引/状态/来源/目标表（可选文件）
python scripts/journal.py check --strict --lint  # 上面那道 + 下面那道，一次跑完（检查点/CI 用这条）
python scripts/journal.py lint --strict         # 内容：占位符/空小节/结论无可核对信息/含糊措辞
python scripts/journal.py check --legacy ""     # 全按新格式判（不给就是宽松起步：旧记录只报 info）

# —— 分析与生成 ——
python scripts/journal.py stats                 # 语料统计（节奏/合规率/引用覆盖/两种命名）
python scripts/journal.py topics --limit 15     # 同主题簇建议（中文用 --keywords）
python scripts/journal.py digest --out HANDOFF.md          # 交接摘要
python scripts/journal.py retro --from 100 --to 151 --out r.md  # 阶段复盘骨架
python scripts/journal.py export --csv --out work_log.csv   # 机器可读导出

# —— 跨工作区：全局记忆（默认在 <用户主目录>/dsh-lore-memory，不在工作区里）——
python scripts/journal.py memory publish --applies-to dsh-plugin --upload  # 写发布清单（双向白名单）
python scripts/journal.py memory collect                                    # 按清单收集（幂等）
python scripts/journal.py memory add "…" --source wl/0042 --id some-slug    # 新增一条（来源分档准入）
python scripts/journal.py memory lint --strict                              # 记忆门禁（判据见 memory.md §八）
python scripts/journal.py dream                                             # 记录 → 摘要骨架（模型填，再 --accept）
python scripts/journal.py inbox count                                       # 待收条数（stdout 一个整数）
python scripts/journal.py promote suggest                                   # 升格为技能的建议（只报候选）
```

> **全局记忆是经验层的上一层，不是另一套格式**：一条教训要离开本工作区，必须由
> 本工作区的 `发布.md` 点名（那是唯一获准被读的文件，也是双向白名单）。
> 机制、条目格式、来源分档与生命周期见 [references/memory.md](references/memory.md)。

自测：`python -B scripts/_selftest.py`（`-B` 别省：脚本住在包里，不加会在包内留下 `__pycache__`；临时工程跑通全部命令 + CRLF 保真 + 非编程场景 + 整理能力 + 英文标签 + 数据安全 + 新/旧布局 + 精细度档位 + 两种命名 + 渐进原则 + snapshot + 项目配置文件 + 目标表 + 全局记忆；**断言数以脚本实际输出为准**，全绿即通过）。

> 典型接手动作：`brief` → `snapshot` → `search` → `show` → 需要细节才读那一个文件（用当前可用的文件读取工具）。
> 典型收尾动作：`new --insert` → 补正文 → `status` → `lesson add` → `check --strict --lint`（两道门禁一起跑；为什么默认不合并见 [references/commands.md](references/commands.md)）。

## 在 DSH 里：让启动器找自带 Python

DSH 桌面版自带 Python 运行时。`node scripts/journal.mjs <命令>` 的参数与
`python scripts/journal.py <命令>` 完全相同；启动器按下面顺序找解释器：

1. `DSH_WORKLOG_PYTHON`（显式指定）
2. `DSH_PRIMARY_RUNTIME` / `DSH_BUNDLED_PRIMARY_RUNTIME`
3. `<DSH_HOME>/dsh-runtimes/*/dependencies/python/`
4. PATH 上的 `python` / `python3` / `py`

所以 DSH 装好就能跑，不必另装 Python。非 DSH 环境仍可直接用
`python scripts/journal.py`；两条路都要求 Python 3.9+。

## 没有 Python 怎么办（降级路径）

**本技能的核心是约定，脚本只是加速器。** 环境里没有 Python 也能完整使用，只是费手：

1. **建结构**：按 [references/templates.md](references/templates.md) 手工落这几个文件：`work_log/README.md`、`work_log/STATE-HISTORY.md`、`work_log/lessons/README.md`、`work_log/_inbox.md`。（已有旧体系就沿用旧名，见「目录布局」的回退顺序。`work_log/archive/README.md` 要等第一次归档才需要，见第 5 条。）
   项目配置文件 `work_log/.config.json` 也是手写一个 JSON 就行；**不写就等于全部内置默认**。
2. **写记录**：按记录模板写入口字段，加一个验证类小节；标题按容器选定的一种约定写
   （编号式 `# NNN · 标题` / 日期式 `# YYYY-MM-DD 标题`）。
3. **收尾**：把「工作流 C 收尾清单」当人工检查表逐条走；把 `check` / `lint` 的判据（见 [references/commands.md](references/commands.md)）当核对清单。
4. **检索导航**：用 `grep` / `rg` 代替 `search`，用 `snapshot` 的判据手工汇总最近几篇，用索引表代替 `brief` / `outline`。
5. **整理**：归档就是"移文件 + 改链接"（容器根 → `<stage>/`，可带主题层 `<主题>/<阶段>/`），手工做时**先全仓 grep 链接再改**——脚本的价值主要就在这里（自动重写 + 死链自检）。用了归档层 `archive/` 的项目，归档后还在 `archive/README.md` 的表里补/并一行（**篇号与篇数按磁盘重算**、日期区间取并集，同一个阶段只占一行；新容器就按 [references/templates.md](references/templates.md) §3 的骨架建）。

脚本全部只用 Python 标准库，**不需要 `pip install`**；只要 Python 3.9+ 在 PATH 里就能跑
（DSH 用户可走 `scripts/journal.mjs`，它会找 DSH 自带运行时，不要求 PATH 里有 Python；
更精确的实测范围见下方「环境边界」）。若连命令都不能执行（纯聊天环境），技能退化为一份
"怎么写记录"的规范——三层结构、收尾清单、归档判据仍然成立。

## 环境边界

- **纯标准库**，不需要 `pip install`。
- 实际下限是 **Python 3.9**：代码用了 PEP 585 泛型注解（`list[str]`）与海象运算符。
  实测过 **3.12**（CI / Ubuntu）与 **3.14**（Windows 本机）。
- Windows / macOS / Linux 均可（脚本无平台相关 API）。
- 记录文件用 **UTF-8**。控制台编码无关，脚本自己把 stdout 设为 UTF-8。
- 非 UTF-8 的老仓库**不会让工具崩**：脚本按 `errors="replace"` 读，坏字节变成 `�`。
  但中文标签会因此认不出来，`check` 会报一串 WARN。那是编码问题，不是记录坏了 ——
  先用编辑器把仓库转成 UTF-8。
- **解析中英双语**（写入默认中文）：`日期/Date`、`结论/Conclusion`、`触发/Trigger`、`范围/Scope`、
  `迭代/Iteration`（及 `变更集/批次/阶段/版本/里程碑/Milestone`）、
  `验证/Verification`（及 `复核/检查/审查/评审/结果/证据/评估/确认/实测/实验/判定/评测`）、
  `当前状态/Status`、`待办/TODO`、`文件索引/Index` 都能解析。
- **两种记录命名都认**：`NNN-slug.md` 与 `YYYY-MM-DD-slug.md`；两种都不匹配的文件不是记录，直接忽略。
- 无 Python 或不能执行命令时，按上一节降级为纯规范使用。

## 反模式（本工作区实测踩过的，别再来）

| 反模式 | 后果 | 正确做法 |
|---|---|---|
| 台账靠人肉同步、长期不更 | "当前状态"过期，看板不可信（基线项目实测） | 收口必更状态块，并用 `check` 判新鲜度（状态块日期 ≥ 最后一篇记录日期） |
| **把一天的密集实验并成一篇** | 34 个可独立查阅的单元挤进一个文件，导航价值归零（原型 09-13 实测 34 篇） | 默认档 `full`：一个可交付单元一篇；真要粗才 `mode --set session`/`digest`，别默默并 |
| 粗档位合并多轮会话，却不写漏了什么 | 粗粒度静默丢信息，事后无处查 | `digest` / `milestone` 下必写一句 `未记录：…` |
| 当前状态 + 一堆历史状态堆在索引 | 索引膨胀、改一处分多处 | 最多一块当前状态，旧块进 `STATE-HISTORY.md` |
| 拿日期式文件当编号记录解析 | 报出「编号 2026 重复」这类**假错误**（实测 11 个文件互相重号） | 文件名两种约定之一才解析；两种都不匹配的文件直接忽略 |
| 验证小节只写设置（`## 评测设置`） | 有标题没有结果，等于没验证，但看起来像验过了 | 补实测数字 / 百分比 / 命令输出 / 表格；`check` 会报出来 |
| 篇号当迭代号引用 | 引用歧义（`变更集` 与篇号**从不对应**，实测 0 例相等） | 迭代号只写迭代字段，回指一律 `wl/NNNN` |
| README 与 SUMMARY 各写一份数字 | 改一处漏一处 | 复盘并入 `work_log/lessons/99-retrospectives.md`，数字只留一份 |
| lessons 写结论不带来源 | 追不回证据、无法证伪 | 每条带 `（wl/NNNN）`（日期式写文件名），`check` 校验来源存在 |
| 把「收尾补写经验」当唯一采集点 | 实测两次都没自发；坑的细节已经忘了 | 踩坑**当场**往 `work_log/_inbox.md` 记一行，收尾整理；说「完成」之前先看 inbox |
| 卡式条目写成「触发 / 验证」只写一半 | 有触发没验证 = 下次照样不知道成了没有 | `check` 只认缩进子条目且要求成对；`--strict` 下直接判红 |
| 直接抹掉被推翻的旧结论 | 丢失演进与纠错价值 | 追加 `## 更正` 段 |
| 让新规格一上来就把老记录全判红 | 用户面对一片红，然后学会忽略这个工具 | 渐进原则：旧记录只报 info（`LEGACY.md` / `--legacy`）；新记录才判 error |
| 把软件术语当成通用要求（如"验证必须有命令"） | 研究/写作类项目无法满足，规则被架空 | 验证口径是"可核对的内容"：数字、百分比、命令、引用输出、表格都算 |
| 一次性调研随手建新目录 | 编号体系分裂 | 沿用既有 `work_log/`（或旧名 `journal/`），不编号就写 `迭代: -` |
| 日志、trace、导出文件散在项目根（或写到项目外） | 证据游离在版本控制与备份之外，接手时找不到 | 一律归位到 `work_log/logs/<来源>/`；夹具不进容器；日志只写相对路径 |

## 参考文件

- [references/analysis.md](references/analysis.md) · 基线实测分析与改进对照
- [references/conventions.md](references/conventions.md) · 容器目录布局（含旧布局回退）/编号/生命周期/台账/经验层/日志归位 的硬约定
- [references/commands.md](references/commands.md) · `journal.py` 全部命令与组合套路（含全局记忆 / 收敛 / 信箱 / 升格）
- [references/memory.md](references/memory.md) · 全局记忆（跨工作区）：分层 / 条目格式 / 来源分档 / 发布清单 / 生命周期 / 校验表 / 收敛 / 信箱 / 升格
- [references/templates.md](references/templates.md) · 记录、台账、归档、经验分册、复盘 全套模板
