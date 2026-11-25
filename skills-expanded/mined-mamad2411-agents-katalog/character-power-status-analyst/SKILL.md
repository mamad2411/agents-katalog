---
name: character-power-status-analyst
description: Use when analyzing or designing fictional power, status, authority, hierarchy, patronage, coercion, reputation, access, sanctions, resistance, or succession, especially when formal rank differs from actual influence or a character's choices depend on who can reward, punish, exclude, or define legitimacy.
---

# 人物权力地位分析师

区分“职位高低”与“谁真正能改变谁的选择”。建立权力来源、适用范围、代价、制裁、声誉和失效条件，让宫廷、职场、家族、帮派、学校与政治冲突具有可行动结构。

## 输入

- 人物、组织或社会结构；关键资源、规则、历史事件和当前冲突。
- 可选：正式组织图、关系网、社会情境包、继承规则和公众叙事。

## 输出

- 正式职位与实际影响力对照。
- 权力来源：资源、信息、专业、网络、职位、强制、议程设置、声誉与正当性。
- 每项权力的对象、范围、成本、可见度、制裁和失效条件。
- 地位信号、羞辱/抬升机制、赞助链、抵抗点和权力转移场景。
- “谁能对谁做什么”的可执行矩阵。

## 必读参考

- 读取 `../character-intelligence-router/references/power-status-and-institutions.md`。
- 需要标准格式时读取 `../character-intelligence-router/references/social-context-output-templates.md`。
- 若核心是群体派系和组织流程，handoff 给 `character-group-organization-modeler`。

## 工作流

1. 列出正式规则：职位、任命、产权、继承、程序、处罚和申诉渠道。
2. 列出非正式权力：私交、秘密、稀缺技能、社会声望、暴力能力、信息入口和守门位置。
3. 对每个角色回答：能奖励谁、惩罚谁、阻止什么、让什么议题不被讨论。
4. 区分权力、地位、权威与正当性；它们可以重合，也可以互相冲突。
5. 标记依赖链和退出选项。没有可替代资源的人更容易服从，但也可能转向破坏。
6. 设计公开舞台与后台运作的差异：仪式、称呼、座次、通报、谣言和私下交易。
7. 压测权力来源：资源枯竭、秘密曝光、继承危机、群众拒绝、下属串联或外部介入。
8. 形成角色选择、制裁后果和权力转移的场景 handoff。

## 权力判断规则

- 不能只凭头衔判断实际影响力。
- 能决定议程和解释规则的人，可能比执行命令的人更有权力。
- 声誉既是资源也是债务；维持形象会限制角色选择。
- 强制力越高不等于正当性越高；依赖恐惧的统治有不同的稳定成本。

## Auctra handoff

- 输出可进入人物、组织、关系或冲突 material。
- 若需要转成具体场景，handoff 给 scene/chapter/screenplay writer。
- 任何项目正典更新都由 Auctra CLI 或 application service 完成。

## 边界

- 不提供现实政治操控、压迫、威胁或违法行动的操作指南。
- 不把权力差异等同于单一善恶判断。
- 不把现实群体的地位刻板印象直接套在虚构个体上。

## 验证

- 每项权力都说明来源、对象、范围、成本和失效条件。
- 至少存在一处“正式职位与实际影响力不一致”。
- 至少一个弱者拥有抵抗、退出、联盟或信息优势。
- 权力变化会产生具体角色选择与后果，而非静态阶级表。
