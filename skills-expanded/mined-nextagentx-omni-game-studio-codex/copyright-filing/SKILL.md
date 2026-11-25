---
name: copyright-filing
description: Orchestrate China software copyright (软件著作权 / 软著) registration for a game project — lock the software name, generate compliant source-code and manual documents, run risk audit and beginner guidance in parallel, and assemble a submission-ready package. Use when 用户要申请软著、准备申报材料、查名称能否用、第一次办需要照着做的指导，或游戏做完要确权、上架前补资质时。
---

# 软著申报 · 主理人编排

游戏做完只是「能上线」，确权之后才是「能保护、能上架、能维权」。这条能力线把中国版权保护中心的软著申报拆成四段：**锁名称 → 出材料 → 双线并行 → 汇编交付**。

当前会话的助手担任**主理人**（角色定义见 `subagents/copyright-filing-lead.toml`）。三位专业角色按需调用，配置随压缩包单独提供，未必已安装；未安装时由当前助手承担对应工作，不以缺少角色为由停工。

## 一句话事实（每次都要对用户说清）

软著登记是**形式审查**，中国版权保护中心不比对名称是否已被他人登记。所以查名称不是为了过审，是为了避免「证书拿到手，产品却不能叫这个名字」——真正的墙在商标和应用商店。别把软著说成专利那么难，也别承诺百分百过。

## 可用角色

| 角色 | 负责域 | 什么时候派 |
|---|---|---|
| `copyright-material-smith` | 源程序文档、说明书、申请表、材料清单、清第三方代码与密钥 | Phase 1 出材料 |
| `copyright-risk-auditor` | 名称查重、12 项风险、权属 / 开源 / 密钥 / AI 痕迹、提交前自评表 | Phase 0.5 与 Phase 2 A 线 |
| `copyright-guide-designer` | 网页版小白指导报告、常见问题 | Phase 2 B 线 |

配套技能：`skills/software-name-checker/SKILL.md`、`skills/copyright-material-kit/SKILL.md`、`skills/copyright-risk-audit/SKILL.md`、`skills/copyright-filing-guide/SKILL.md`。

配套脚本与模板：`scripts/copyright_name_check.py`、`scripts/copyright_source_doc.py`、`scripts/copyright_audit.py`、`templates/copyright/material-templates.md`、`templates/copyright/pre-submit-checklist.md`、`templates/copyright/guide-report.html`、`templates/copyright/faq.md`。

## 铁律（顺序不能反）

0. **名称没锁死，不做材料**。这是唯一「越晚发现越贵」的环节：页眉、说明书封面、申请表三处逐字一致，中途改名等于整套重做，已下证的要重新申请。
1. **先说结论，再说理由**。用户问「能交吗」，第一句就是「能」或「不能」。
2. **主理人不代写专业结论**。材料、风险结论、指导报告必须由对应角色输出后再采信；主理人只做编排、验收与汇编。
3. **跨线信息经主理人中转**。角色之间不直连；上一阶段的产出原文完整传给下一阶段，不摘要。
4. **写操作串行，只读分析才并行**。多个角色同时改同一份材料会写冲突。
5. **产物优先于叙述**。任何角色声称写了文件，就校验那个路径真的存在；不存在就是 PHASE FAILED，不推进、不总结为完成。
6. **风险说人话**。「权属瑕疵」→「这软件法律上可能不算你的」；「商标冲突」→「证书能拿到，但你上架可能被打下来」。
7. **不替用户做法律判断**。权属争议、侵权风险给判断依据和后果，结论让用户或律师定。
8. **不隐瞒 AI 辅助**。代码用了 AI 辅助就如实说，重点是独创性和过程证据，不是撒谎。
9. **不夸大也不含糊**。不说「名字被占用就办不下来软著」，也不说「名字随便取都行」。
10. **宿主差异要如实说**。Codex 没有 WorkBuddy 的团队运行时工具，本技能把协作写成流程契约而非工具调用：主理人由当前助手担任，成员产出以独立文件或独立段落回传，经主理人汇编。

## Phase 0：确认三件事（主理人自己做，不派单）

缺一项就停下来问，问完一次性锁死：

1. **软件目录在哪**：能读到源码的路径。没有代码就不做材料，只做指导。游戏项目通常就是当前工程根目录。
2. **软件全称与版本号**：例如「星海拾光 V1.0」。定下来之后全流程不许改一个字。
3. **著作权人是谁**：单位全称或个人信息，决定权属判断和身份证明材料。

顺带确认：是否首次登记、是否已发表、期望周期（正常 / 加急）。

## Phase 0.5：名称查重（不可跳过，派 `copyright-risk-auditor`）

走 `skills/software-name-checker/SKILL.md`，可先跑 `scripts/copyright_name_check.py` 做静态预检。

要求输出：13 项命名规则通过情况 + 独创性评分、六个渠道占用核查（软著登记公告、商标第 9/42 类、应用商店、备案、企业、官网）、三档结论（**可以直用 / 建议微调 / 必须改名**）、需改时 3–5 个备选名并推荐一个。

主理人必须守住：

- 「必须改名」→ 停下来把名字改掉再进 Phase 1，不许带高风险名称往下做。
- 「建议微调」且用户坚持不改 → 可以继续，但最终交付里保留这条风险，不许抹掉。
- 锁定后每次下发任务都使用同一个全称，一个字都不能差。

## Phase 1：材料生成（串行，派 `copyright-material-smith`）

把五项原样给它：软件目录路径、软件全称、版本号、著作权人、输出目录。走 `skills/copyright-material-kit/SKILL.md`。

产出：项目画像、源程序文档、软件说明书、申请表填写信息、材料清单。模板在 `templates/copyright/material-templates.md`，分页生成用 `scripts/copyright_source_doc.py`。

**主理人必须验收（不合格退回重做，不往下传）**：

- 源程序文档是否 60 页口径、每页 50 行、页眉规范（不足 60 页取全部，超过取前 30 + 后 30）
- 说明书里 `【待补充】` 有多少处，必须显式清点
- 三处「软件全称 + 版本号」是否逐字一致
- 画像报告里有没有密钥、第三方版权头这类硬风险

## Phase 2：双线并行

A 线 `copyright-risk-auditor` → `skills/copyright-risk-audit/SKILL.md` + `scripts/copyright_audit.py`：12 项风险红 / 黄 / 绿分级 + 每条规避动作 + `templates/copyright/pre-submit-checklist.md` 自评表。结论必须是「能交 / 不能交 / 补什么再交」。

B 线 `copyright-guide-designer` → `skills/copyright-filing-guide/SKILL.md` + `templates/copyright/guide-report.html` + `templates/copyright/faq.md`：网页版指导报告，外行照着能做完，材料状态如实标注「已生成 / 待补」。

两线输入相同（Phase 1 完整产出），产出互不重叠，可并行。红线由 A 线原文摘出，**一条不许省略**地交给主理人。

## Phase 3：汇编交付（主理人自己做）

```text
## 能交了吗
一句话结论。风控说「不能交」就如实说不能交，并列出必须先解决的问题。

## 交什么
文件清单 + 每个文件状态：可直接交 / 待补 X 处 / 需转 PDF

## 怎么交
指向指导报告路径，三句话说清提交顺序。

## 红线
A 线列出的高危项原文，逐条摘出，一条不许省略。
```

## 预设工作流（按问法路由）

| 触发 | 编排 |
|---|---|
| W1 全套申报（默认）：「我要申请软著」「帮我准备材料」且给了代码目录 | Phase 0 → 0.5 → 1 → 2 双线 → 3 |
| W2 只做风险体检：已有材料，问「有没有问题」「会不会被驳回」 | 直接派风控官，跳过 Phase 1，出问题清单与必改项 |
| W3 只做材料：「我只要源程序文档和说明书」 | Phase 0 简化确认 → 派材料工程师 → 主理人验收后交付 |
| W4 只要小白指导：「第一次办，不知道怎么弄」 | 派指导设计师；可先跑一次扫描拿真实数据 |
| W5 材料复核 + 修补：被补正了或想要第二意见 | 风控官先出问题清单 → 材料工程师按清单修 → 主理人复核 |
| W6 只查名称：「这个名字能不能用」 | 只跑 Phase 0.5，给结论 + 备选名；不自动改名、不顺手做材料 |
| W7 名称改了重做材料 | 对新名称重跑 0.5 → 无高危后重跑全部脚本；旧材料整份作废，页眉 / 封面 / 申请表三处都要重生成 |

## 单角色直调路由表

| 问法 | 直接调谁 |
|---|---|
| 源程序文档怎么生成、说明书怎么写、申请表怎么填 | `copyright-material-smith` |
| 这个名字能用吗、会不会重名、被谁注册了吗 | `copyright-risk-auditor` |
| 代码里的密钥要不要删、开源库能不能交、权属归谁 | `copyright-risk-auditor` |
| 第一次办流程是什么、给我一份能照着做的文档 | `copyright-guide-designer` |
| 全套帮我办了 | 走 W1 |

## 与游戏主线的衔接

`game-production-pipeline` 走到 G5 / 发布阶段时，把本能力线接在后面：发布方案里的资质清单若需要软著，就从 Phase 0 起走 W1。软著**不是**版号，也**不替代**应用商店的资质审核；它解决的是权属证明。游戏名称、包名、icon 与软件全称之间的对应关系要在 Phase 0.5 一并核对。

## 边界

- 材料是分页文本 / HTML / Markdown，需按提示转 PDF / DOCX 后再提交；脚本不假装已生成 PDF。
- 脚本只做静态检查，不替代六个渠道的人工核查，也不替代中国版权保护中心的形式审查。
- 不承诺过审、不承诺周期、不做法律判断、不替用户点提交。
- 权属争议、商标侵权风险给依据与后果，结论让用户或律师定。
