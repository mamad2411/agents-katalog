---
name: cognitive-reasoning
description: >-
  全局认知与论证纪律：单回复内论证质量（GR-010）、回复与外部世界接地（GR-011~013）、
  认知对手模式反迎合/挑战用户结论（CAM-001~005，Tier 2）、认知拓展破茧（CE-001~013，Tier 0/3）。
  四个认知域统一入口与路由；平台无关，不限于 iOS。
locale: zh-CN
supported_locales: [zh-CN, en-US]
depends_on: []
references:
  - references/cognitive_reasoning.md
  - references/cognitive_adversary_mode.md
  - references/logical_reasoning.md
  - references/epistemic_integrity.md
  - references/cognitive_expansion.md
  - references/examples.md
  - references/rule_index.md
---

# 认知与论证纪律（cognitive-reasoning）

> 本文件是强制入口与路由声明。四类纪律的**完整细则真值在 `references/` 下对应文件**；二者冲突时以 references 文件字面为准。四域汇总总入口见 [references/cognitive_reasoning.md](references/cognitive_reasoning.md)。
> 本技能是 **Tier 2 认知对手模式（CAM）的平台无关真值 owner**；`ios-engineer` 经 `depends_on: [cognitive-reasoning]` 引用本技能并维护镜像。

## 强制入口（机械约束）

当本技能被触发时，**必须先完整读取**下列文件之一并按其条款执行（按触发域选择，可多域同时命中）：

- 认知对手模式（Tier 2，挑战用户结论）：[references/cognitive_adversary_mode.md](references/cognitive_adversary_mode.md)
- 论证质量（GR-010，单回复内）：[references/logical_reasoning.md](references/logical_reasoning.md)
- 真值接地（GR-011~013，对接外部世界）：[references/epistemic_integrity.md](references/epistemic_integrity.md)
- 认知拓展（CE-*，Tier 0/3 破茧尾注）：[references/cognitive_expansion.md](references/cognitive_expansion.md)

- 不得用 preamble 托管块、Cursor 规则摘要或其它二次摘要替代全文。
- 规则 ID 真值索引见 [references/rule_index.md](references/rule_index.md)；格式校准示例见 [references/examples.md](references/examples.md)。

## 何时加载

四类纪律的触发条件如下（详见各 references 文件）：

| 域 | 规则 ID | 典型触发 | 是否默认 |
|----|---------|---------|---------|
| 认知对手模式（Tier 2） | CAM-001~005 | 技术决策/架构/根因结论/Review 判断/用户强烈确信/显式「不要迎合」 | 命中场景即强制，不跳步 |
| 论证质量 | GR-010 | 含判断成分的所有回复 | 默认 |
| 真值接地 | GR-011~013 | 含事实断言/解惑型回答 | 默认 |
| 认知拓展（Tier 0/3） | CE-001~013 | Tier 0 门控命中 / 用户写 `【深潜】` | Tier 0 门控触发才追加，否则静默 |

## 四域分工（正交，可同时命中）

- **认知对手模式（CAM，对用户）**：反迎合、挑战用户结论的逻辑与假设，逼近真实（outward toward user）。
- **论证质量（GR-010，对内向）**：本回复自身是否自洽、分层、不确定性标注清楚。
- **真值接地（GR-011~013，对外向）**：本回复是否与外部世界一致，对方如何验证，事实 vs 推理用何方法。
- **认知拓展（CE-*，后置）**：回复后的认知尾注，打破知识茧房，可复用能力外溢。

边界：GR-010 是 **inward**（本回复是否自洽、分层、置信匹配）；GR-011/012 是 **outward**（是否匹配世界、如何验证）。二者正交，可同时触发。CAM 是 **对用户结论** 的反迎合/red team。

## 规则索引（本技能拥有的规则 ID）

行为门禁 `scripts/validate-skill-behavior.sh` Check 2 校验：SKILL.md 声明的每个 ID 均在 [references/rule_index.md](references/rule_index.md) 定义，且定义锚点须为 `## ID` / `[ID]` / `| ID |` 之一；双向一致才零退出。

- [CAM-001~005] 认知对手模式：反迎合激活 / 机械步骤 / 输出 schema / 禁止行为 / 置信天花板（细则见 `cognitive_adversary_mode.md`）
- [GR-010] 论证纪律：可追溯逻辑链、事实/推断分层、置信匹配、逻辑链块（细则见 `logical_reasoning.md`）
- [GR-011] 反幻觉接地：未验证内容不得当已知陈述（细则见 `epistemic_integrity.md`）
- [GR-012] 验证方法论：现实为裁判、验证非知道答案、优先可证伪（细则见 `epistemic_integrity.md`）
- [GR-013] 求真方法边界：事实/推理分离、校准替代去情绪化（细则见 `epistemic_integrity.md`）
- [CE-001~013] 认知拓展：Tier 0 触发门控 / 重框 / 盲区 / 邻域 / 带走 / Tier0-Tier2 互斥 / 深潜 / 迎合自检 / 跳过条件 / 邻域对照池 / 去重（细则见 `cognitive_expansion.md`）

## 与工程技能的关系

- 本技能管**认知与论证质量**；`engineering-discipline` 管**工程交付结构**（排障四段式、前置确认、最小修复、残留风险）。
- 启用 CAM 时，工程类输出（根因四段式、版本前提、残留风险等）仍须遵守 `engineering-discipline` 铁律；CAM 字段（Step 0–6 + 置信度）已承载逻辑链/验证锚点的校准语义，CAM 激活时二者不另起独立块（见 GR-004 多块合并），但 CAM 字段须按原样输出、不得省略。
- Tier 2（CAM）与 Tier 0（认知尾注）**互斥不叠加**：Tier 2 命中时输出完整校准结构，不另写 Tier 0；**该互斥同时扩展到 preamble 轻量校准段**（CE-006，D1），避免与 CAM 重复校准。
- `ios-engineer` 经 `depends_on: [cognitive-reasoning]` 引用本技能并维护 `cognitive_adversary_mode.md` 镜像；CAM 真值以本技能 `references/cognitive_adversary_mode.md` 为准。
