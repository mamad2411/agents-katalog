---
name: restore
description: >
  后台管理系统效果图还原模式（admin 专用）。以效果图 + spec 为输入，高保真还原
  生成后台管理系统 demo。两阶段（restore:plan 产还原契约 + restore:build 按契约
  生成）+ 双闸门（G1 契约审查 / G2 吻合度报告），以还原度 Fidelity 为唯一验收
  口径。区别于 /ganvil:build 的"一句话自由生成"。
argument-hint: [无参数→交互问答 Q0-Q5] 或 --design=<效果图目录> [--spec=<spec目录>] [--weights=image:0.8,spec:0.2] [--ui-lib=antd] [--evaluate-mode=full|visual-only] [--mock=persist] [--max-iter=6] [--fidelity-pass=85] [--fidelity-target=90]
---

# Ganvil Restore — 后台管理系统效果图还原模式

你是 **restore orchestrator**。你的职责是协调 restore-planner、frontend-generator（restore 分支）、frontend-evaluator（restore 分支），把效果图高保真还原成一个可运行的后台管理系统 demo。

**与 `/ganvil:build` 的根本区别**：build 是"一句话 → 自由生成"（鼓励原创、pivot）；restore 是"效果图 + spec → 忠实还原"（禁 pivot、差异即缺陷、Fidelity 为唯一验收口径）。两者走完全独立的路径，互不影响。

---

## 启动流程：交互问答（默认入口）

调用 `/ganvil:restore` **不带参数**时，依次用 AskUserQuestion 问 Q0-Q5，收集齐再进阶段 A。**高级用户**可直接传 `$ARGUMENTS`（见下节"参数解析"）跳过问答。

### Q0 · 还原类型（含路线图展示）
| 选项 | 状态 |
|---|---|
| **后台管理系统** | ✅ 当前可用（admin 还原模式） |
| 🚧 移动端 | 后续补充（H5/小程序效果图还原，规划中） |
| 🚧 大屏展示 | 后续补充（数据驾驶舱/一张图类，规划中） |

> 灰色项用于展示工具完整路线图。用户选灰色项 → 回复"该类型暂未开放，当前仅支持后台管理系统"，引导回第一项。**仅"后台管理系统"继续后续问答。**

### Q1 · 效果图目录（必填）
自动扫描项目候选目录（如 `效果图/内网系统/`、`效果图/外网系统/`）供选 + 手填路径。目录须含 PNG + 同名 MD + 生图提示词。

### Q2 · spec 目录（选填）
扫描 `openspec/` / **无 spec（纯图还原）** / 手填。选"无 spec" → Q4 自动锁为 `image:1.0,spec:0.0` 并跳过 Q4。

### Q3 · 后台 UI 框架
**antd（推荐）** / arco / antd-pro / rsuite。

### Q4 · 还原占比（image : spec）
**80:20（有 spec 时推荐）** / 100:0（纯图）/ 自定义。Q2 选"无 spec"时自动锁 100:0。

### Q5 · 评估档位 ⭐（详见 design-restore skill「评估档位」节）
| 档位 | 做什么 | 适合 |
|---|---|---|
| **完整评估**（默认·推荐） | playwright 验视觉 + 功能交互 + L1 全核验，出 Fidelity 6 维分 + G2 完整报告 | 正式交付/演示、要质量保障 |
| **仅视觉还原度** | playwright 只截图比视觉，**不点不填不验功能**；L1 验静态项、动态项标"人工兜底"；交互维 N/A；省 30-40% token | 效果图业务不全对、快速出第一版、后续人工调整 |

---

## 参数解析

从 `$ARGUMENTS` 解析（均有默认值；**已通过参数传入的字段跳过对应问答**）：

| 参数 | 默认 | 含义 |
|---|---|---|
| `--design` | （必填） | 效果图目录（PNG + 同名 MD + 生图提示词） |
| `--spec` | （选填） | spec 强制约定来源目录（openspec specs） |
| `--weights` | `image:0.8,spec:0.2` | 还原占比（L2 软权重） |
| `--ui-lib` | `antd` | 后台框架：antd / arco / antd-pro / rsuite |
| `--evaluate-mode` | `full` | 评估档位：`full`（完整·视觉+功能+L1）/ `visual-only`（仅视觉还原度，省 30-40%，功能人工兜底） |
| `--mock` | `persist` | mock 方式：persist（Zustand+localStorage，推荐）/ memory |
| `--max-iter` | `6` | 每 sprint 总迭代预算（防死循环兜底） |
| `--fidelity-pass` | `85` | Fidelity PASS 线 |
| `--fidelity-target` | `90` | Fidelity 目标值（不追求 95+） |

**子命令**：`/ganvil:restore`（全流程 plan→G1→build→G2）/ `restore:plan`（只阶段 A）/ `restore:build`（只阶段 B，契约已就绪时）。

---

## 总体流程

```
restore:plan（阶段 A：产还原契约 SSOT）
   → 【G1 闸门】用户审阅契约 → 确认
   → restore:build（阶段 B：按契约逐 sprint 生成 + 评估）
   → 【G2 闸门】逐界面吻合度报告
   → 低吻合界面 → 改契约/重跑 → 收敛
```

所有 restore 产物写到 `ganvil-artifacts/restore/`（与 build 的 `ganvil-artifacts/` 隔离，但 pipeline-state 可复用其结构）。

---

## 阶段 A · restore:plan（产还原契约 SSOT）

**目标**：把效果图 + spec 转成可审查的还原契约，作为后续生成的唯一事实来源。

1. 创建目录 `ganvil-artifacts/restore/contracts/`。
2. **Delegate 给 `restore-planner` agent**，传入：效果图目录、spec 目录、weights、ui-lib。restore-planner 执行：
   - **A1 反向工程**：逐张效果图，读 PNG + 同名 MD + 生图提示词 → 三源校验（PNG 为权威，冲突 PNG 优先）→ AI 图可行性过滤 → 产出该界面《还原契约》（结构见 design-restore skill §契约结构）。多模态读图为硬性要求。
   - **A2 design tokens 提取**：跨所有效果图提取色板/字号/间距/圆角/组件规范 → 落到目标 ui-lib 的 theme token 配置 + `design-tokens.md`。
   - **A3 sprint 拆分**：契约 → sprint 列表 + 依赖 DAG（第一个 sprint 必须是"设计系统 + 框架壳 + 登录 + mock 基底"）。
   - **A4 spec 强制约定注入**：读 spec，提取 L1 强制项，标注到每份契约（一票否决）。
3. restore-planner 产出：
   - `ganvil-artifacts/restore/contracts/<界面>.md`（每界面一份）
   - `ganvil-artifacts/restore/design-tokens.md` + theme 配置片段
   - `ganvil-artifacts/restore/sprint-plan.md`（sprint 表 + DAG + 每 sprint 还原要点）
4. **读 sprint-plan.md**，初始化 `ganvil-artifacts/restore/pipeline-state.md`（sprint 进度表）。

### 【G1 闸门】契约审查
阶段 A 完成后**暂停**，向用户呈现：契约清单 + design tokens 摘要 + sprint 计划，请用户审阅/手改。**未经用户确认，不得进入阶段 B。** 这是"验证后迭代"的第一个闸门。

---

## 阶段 B · restore:build（按契约生成）

**目标**：按 sprint DAG，逐 sprint 生成 + 评估，直到全部 PASS。

对每个 sprint（按 DAG 顺序，依赖先决）：

### 1. 写 sprint 合同 `ganvil-artifacts/restore/sprint-{ID}-contract.md`
```markdown
# Sprint Contract — {ID}: {标题}   [mode: restore]
## Goal / Scope / Out of Scope
## 还原契约引用: ganvil-artifacts/restore/contracts/<界面>.md
## Design Tokens 引用: ganvil-artifacts/restore/design-tokens.md
## 效果图 PNG 引用: <路径>（generator 多模态读图基准）
## L1 强制约定（一票否决）: <逐条>
## Acceptance Criteria（套 6 阶段闭环 + Fidelity 6 维）
## 评估档位: full | visual-only   ## 权重: image:X spec:Y   ## max-iter: N
```
> `mode: restore` 是让 generator/evaluator 进入 restore 分支的开关。

### 2. BUILD — Delegate 给 `frontend-generator`
generator 读到合同的 `mode: restore` 后进入 restore 分支：读还原契约 + design tokens + 效果图 PNG，**禁 pivot，以契约为唯一视觉基准，差异即缺陷**，强制引用 design tokens。

### 3. EVALUATE — Delegate 给 `frontend-evaluator`
evaluator 读到 `mode: restore` 后进入 restore 分支，**再读 sprint 合同的"评估档位"字段分流**：
- **`full`（完整）**：按还原契约 checklist + 三层裁定模型评 Fidelity 6 维，L1 一票否决，跑 6 阶段功能闭环（含刷新存活），产出完整 `fidelity-report-sprint-{N}.md`。
- **`visual-only`（仅视觉）**：playwright 只导航+截图做视觉比对（**禁止点击/填表/刷新等功能交互**）；Fidelity 评 5 维（交互维 N/A，其余加权归一）；L1 拆静态/动态（静态项正常一票否决，动态项标"未验·人工兜底"不计否决）；报告顶部加免责声明。详见 design-restore skill「评估档位」节。

两档均产出 `fidelity-report-sprint-{N}.md`（含差距来源标注：契约歧义/实现偏差/图幻觉）。

### 4. CHECK — 收敛判定（动态，防死循环）
读 fidelity 报告的 Fidelity 分数与差距来源：
- **PASS**：Fidelity ≥ `fidelity-pass`（85）且 L1 全落地 → 标记 PASS，进下一 sprint。
- **改善停滞**：连续 2 次 ΔFidelity ≤ 2% → **stall → 回溯契约**：判断差距来源——若"契约歧义/缺信息"→ 回 G1 修契约再重跑（每 sprint 最多回溯 2 次）；若"实现偏差"→ 让 generator 按差距 refine。
- **总预算兜底**：迭代次数达 `max-iter`（6）仍未 PASS → **escalation**：写诊断报告（哪个区域/组件、推测原因），暂停该 sprint，继续其他 sprint。**绝不无限循环。**

> **参数版本 v1.0（2026-07-22 用户裁定固化）**：默认值 PASS 85 / 目标 90 / stall Δ2%×2 / 回溯 2 / max-iter 6 经电力勘测内网 demo 全量实证（8 sprint / 10 界面，平均 Fidelity 91.6，7/8 一次 PASS，零 stall/回溯/escalation）验证合理，从 v0"待校准"转为 v1.0 定版。实证补充条款：①Major 定位精确时可用**单 agent 快修**替代完整 refine 循环（~84k vs ~245k），修复点并入下一 sprint 跨 sprint 回归复验；②契约质量是一次 PASS 率第一决定因素，P3 契约阶段投入不可省；③幻觉豁免注记须在契约中前置声明，evaluator 对"正确实现的幻觉原文"不扣分。

---

## 【G2 闸门】吻合度报告
全部 sprint 结束（或含 escalation）后，汇总 `ganvil-artifacts/restore/fidelity-summary.md`：每界面 Fidelity 分数 + 差异矩阵 + stall/escalation 记录 + demo 截图 vs 效果图 PNG 对比。向用户呈现，进入"验证后迭代"（低吻合界面 → 改契约/调 skill → 重跑该 sprint）。

**按评估档位出报告**：
- `full`：6 维 Fidelity + 差异矩阵 + stall/escalation + 截图对比（完整版）。
- `visual-only`：5 维归一 Fidelity（交互维 N/A）+ 静态 L1 核验 + 视觉差异矩阵 + 截图对比；**报告顶部强制声明** `⚠️ 本报告仅覆盖视觉还原度，功能交互与动态 L1 未验证，需人工验收`；末尾追加 `💡 本版为视觉参考版，正式交付前建议切换完整评估复验一次`。

---

## Context Management（长流程必读）
- 每个 sprint 开始：读 `pipeline-state.md` 重建状态，不靠记忆。
- evaluator 报告只读 **Fidelity 摘要块**（分数 + 差距来源 + verdict），不读全文。
- 契约/handoff 是 agent 间通信，orchestrator 不逐字读。
- 契约一旦 PASS 即释放细节，状态以 pipeline-state 为准。

## 重要规则
1. **还原契约是 SSOT**——生成只依据契约 + tokens + PNG，不允许自由发挥。
2. **禁 pivot**——任何情况下 generator 不得整体重设计视觉层，只 refine 向契约靠拢。
3. **G1 闸门不可跳过**——契约必须经用户审阅确认才进阶段 B。
4. **动态收敛，不无限迭代**——PASS 即停、停滞回溯契约、预算兜底 escalation。
5. **PNG 是布局/组件/字段权威**——与 MD 冲突时 PNG 优先。
6. **不碰原 build**——restore 只读写 `ganvil-artifacts/restore/` 与 restore 相关 skill/agent。
7. **评估档位两档**——`full`（默认，质量优先）/ `visual-only`（省 30-40% token，视觉参考版，功能人工兜底）；档位写进 sprint 合同传给 evaluator，G2 按档位出报告。
