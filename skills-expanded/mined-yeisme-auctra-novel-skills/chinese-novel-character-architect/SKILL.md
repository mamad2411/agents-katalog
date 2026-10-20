---
name: chinese-novel-character-architect
description: Use when creating or revising Chinese novel character profiles, voice rules, flaws, wounds, relationships, antagonist pressure, knowledge boundaries, and growth arcs.
---

# 中文小说人物架构师

把人物写到足以指导场景、对白和情节选择，而不是只列外貌、身份和标签。

## 输入

- 小说 brief、大纲、题材、目标读者、已有角色设定和用户禁忌。
- 主角、反派、配角、关系线、人物参考、对白样例。

## 输出

- 人物档案：欲望、恐惧、缺陷、旧伤、面具、秘密、矛盾点。
- 关系网络：欲望、筹码、亏欠、怨恨、吸引、背叛风险。
- 对白声音规则、知识边界、人物弧线压力点。

普通人物卡保持轻量；只有用户明确要求证据式人物分析、开放人物智能本体、深入思维/动机/情绪/身份/声音/身体建模、跨场景压力测试，或需要关系、权力、文化阶层、群体组织、道德意识形态等社会机制时，才 handoff 到角色智能 suite。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 worker 交付格式、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章节模板、场景卡字段或拆章规格时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-diagram-templates.md`：需要人物关系、时间发展、分卷推进、人物弧线、知识边界或伏笔回收 Mermaid 图预设时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 review、导出前检查或多轮修订门禁时读取。

## 工作流

1. 判断是轻量人物卡还是深度角色智能任务。分析已有材料交给 `character-evidence-profiler`，创建/重构完整心理系统交给 `character-psychology-designer`，场景/关系/弧线验压交给 `character-dramatic-stress-tester`；需要深入某个内在机制或带来源的社会机制时先交给 `character-intelligence-router`，最多选择一个 facet specialist。
2. 轻量路径为主要人物定义显性目标和隐性恐惧。
3. 设计说话方式：句长、词汇、回避方式、情绪泄露点、禁用表达。
4. 绘制关系网，说明每对关键关系的筹码和风险。
5. 标记每个角色知道什么、误解什么、绝不能提前知道什么。
6. 把人物弧线绑定到大纲转折点，说明改变原因和代价。

## 质量门槛

- 每个重要角色都要有想要的和害怕面对的。
- 反派或阻力不能只是坏，必须有有效压力来源。
- 角色变化必须有铺垫，不能为了剧情突然转性。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。
- Auctra 中文项目中，人物 artifact 默认面向 `人物/` display path，并可作为 `素材/` 或 story-bible 输入；不要直接写 `.auctra/**` canon。
- 若人物设定要进入写章 gate，建议先运行 `auctra gate check --before chapter_write --json`，再把缺口交给 brief/outline/scene-card 技能补齐。
- 输出 handoff 时标明 phase=`character`、artifact=`character_profile`、gate=`chapter_write`、display_path 建议和仍待确认的知识边界。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。
- 不为了“完整”强制覆盖角色智能本体；轻量人物卡只保留会影响当前故事的承重信息。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
- 深度任务 handoff 必须说明推荐 worker、已有输入、缺失输入和预期交付物。
