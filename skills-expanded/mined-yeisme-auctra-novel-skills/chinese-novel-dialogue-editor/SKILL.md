---
name: chinese-novel-dialogue-editor
description: Use when revising Chinese novel dialogue for character voice, subtext, power shifts, rhythm, conflict, exposition control, and removal of template-like lines.
---

# 中文小说对白编辑

让对白承担冲突、人物和推进，而不是只传递信息或解释设定。

## 输入

- 对白片段、人物档案、当前场景目标、角色关系和隐藏信息。
- 需要保留的事实、禁用语气、人物身份和场景压力。

## 输出

- 对白诊断：串味、解释腔、无目标发言、知识越界、节奏问题。
- 修订后的对白片段，含动作节拍和潜台词。
- 需要连续性编辑复核的知识边界问题。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 worker 交付格式、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章节模板、场景卡字段或拆章规格时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 review、导出前检查或多轮修订门禁时读取。

## 工作流

1. 判断每个说话者的目标、恐惧、筹码和隐瞒信息。
2. 删除直接说明设定的台词，除非这句话本身制造压力。
3. 加入潜台词、打断、回避、动作节拍和权力变化。
4. 调整词汇、句长、语气，让主要角色不互相串味。
5. 检查角色是否说出自己不该知道的信息。

## 质量门槛

- 对白必须改变场景状态。
- 重要角色不能听起来像同一个人。
- 动作节拍呈现情绪，不用旁白解释情绪。
- 中文对白自然、有身份差异，不写翻译腔。

## Auctra 轻集成

- 普通一次性写稿不强制进入 Auctra。
- 当用户在 Auctra 项目内工作、需要保存素材、审稿或导出时，优先建议 `auctra material`、`auctra text`、`auctra review`、`auctra export` 的真实命令。

## 边界

- 不伪造用户经历、数据、采访、截图、平台反馈或真实发布结果。
- 不执行登录、发布、私信、采集、刷量、规避平台风控或自动化互动。
- 不把完整思维链、原始提示词、供应商载荷、隐藏系统提示或私密工具参数写入稿件、证据、日志或结构化资产。
- 需要持久化 Auctra 项目状态时使用 Auctra CLI，不手写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 验证

- 交付前确认输出覆盖用户请求中的目标读者、素材依据、格式、限制和下一步。
- 检查是否存在空泛判断、虚假细节、结构缺口、语气错位和平台/题材不匹配。
- 无法确认的信息以待补问题列出，不用编造事实补齐。
