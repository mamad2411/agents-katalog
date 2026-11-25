---
name: chinese-novel-style-polisher
description: Use when polishing Chinese novel prose for voice, sensory specificity, sentence rhythm, immersion, genre fit, and removal of AI-like or translation-like phrasing.
---

# 中文小说文风润色师

在不改变剧情核心的前提下，让中文小说更自然、具象、有节奏，并保留作者声音。

## 输入

- 小说段落、章节草稿、目标文风、人物视角、题材和禁用表达。
- 用户希望保留的原句、要强化的情绪、读者年龄和平台风格。

## 输出

- 润色后的文本。
- 改动说明：节奏、具象细节、视角贴近、去 AI 味、删改理由。
- 仍需结构或连续性编辑处理的问题。

## 参考资料

只在任务需要对应细节时读取参考资料，避免把所有模板一次性加载进上下文：
- `../chinese-novel-orchestrator/references/chinese-novel-worker-output-spec.md`：需要统一 worker 交付格式、handoff 和风险标记时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-chapter-scene-templates.md`：需要章节模板、场景卡字段或拆章规格时读取。
- `../chinese-novel-orchestrator/references/chinese-novel-revision-gates.md`：需要 review、导出前检查或多轮修订门禁时读取。

## 工作流

1. 先判断段落功能：动作、心理、环境、对白、过渡或高潮。
2. 保留情节事实和人物意图，只改表达密度、句式和细节。
3. 删除模板式总结、抽象形容词堆叠、翻译腔和过度整齐排比。
4. 用具体感官、动作和选择呈现情绪。
5. 保留作者可识别的语气，不把所有文本磨成同一种风格。

## 质量门槛

- 润色不能改变已确认事实、人物关系或线索。
- 不能用华丽辞藻掩盖场景没有冲突的问题。
- 如果结构问题严重，要先指出需要交给修订制片或节奏编辑。

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
