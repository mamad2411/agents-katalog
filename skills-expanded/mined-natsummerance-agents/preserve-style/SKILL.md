---
name: preserve-style
description: |
  当用户询问"去痕后是否还会像自己写的"、"如何保持个人写作特色"或"技术文档如何处理"时调用此 skill。不适用于：不需要风格保持的场景、用户希望完全重写风格的场景。关键 trigger 信号：保持风格、作者风格、personal writing、technical prose、neutral and plain、style preservation。
source_book: Humanizer Blader
source_project: blader/humanizer
source_chapter: Introduction / style preservation section
tags: [style-preservation, personal-writing, technical-prose, neutral-style]
related_skills: ["voice-matching", "no-fabrication"]
---

# SKILL.md - Preserve Style（保持作者风格）

## R (Reading) - 原文引用

> "For personal writing, Humanizer keeps the writer's style. Technical and reference prose stays neutral and plain."
> 
> "If you provide a writing sample, Humanizer follows that sample instead of its default style rules."

## I (Interpretation) - 方法论骨架

**核心思想**：对于个人写作，Humanizer 保持作者的风格；技术参考文本保持中立和平淡。如果提供写作样本，遵循该样本而不是默认样式规则。这种"风格保留"原则确保去痕后的文本既移除了 AI 痕迹，又保持了适当的风格。

**关键要素**：
1. **Personal Writing**: 个人写作保持作者的风格
2. **Technical Prose**: 技术参考文本保持中立和平淡
3. **Writing Sample Override**: 如果提供写作样本，遵循样本而不是默认规则

## A1 (Past Application) - 书中作者用过的案例

README 中明确区分了个人写作和技术文本的不同处理方式：
- **个人写作**：如里斯本旅行文本，保持作者的个人风格（如"my calves had opinions"、"I would go back, but in spring and with better shoes"）
- **技术文本**：保持中立和平淡，不添加个人色彩

这种差异化处理确保了去痕后的文本既移除了 AI 痕迹，又保持了适当的风格。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户担心去痕后会失去个人风格
- 用户想了解技术文档如何处理
- 用户想保持自己的写作特色
- 用户想知道 Humanizer 如何处理不同类型的文本

**与相邻 skill 的区分**：
- 与 `voice-matching` 的区别：preserve-style 是**被动保持作者风格**（根据文本类型自动判断），而 voice-matching 是**主动提供写作样本来匹配风格**。前者更被动，后者更主动。
- 与 `no-fabrication` 的区别：preserve-style 关注**风格保持**，而 no-fabrication 关注**事实不编造**。前者是个性化保障，后者是真实性保障。

## E (Execution) - 可执行步骤

1. **识别文本类型**
   - 判断文本是个人写作还是技术参考文本
   - 个人写作：博客、游记、个人随笔等
   - 技术文本：API 文档、技术教程、参考手册等
   - 完成标准: 已给出"个人写作/技术文本"二选一判定及依据；混合类型需说明主从关系

2. **应用相应的风格策略**
   - **个人写作**：保持作者的风格，包括用词偏好、句式结构、标点习惯等
   - **技术文本**：保持中立和平淡，避免个人色彩
   - 完成标准: 重写稿实际采用的风格策略与第 1 步的类型判定一致

3. **提供写作样本（可选）**
   - 如果希望更精确的风格匹配，提供 2-3 段自己的写作作为样本
   - Humanizer 会遵循样本而不是默认规则
   - 完成标准: 若提供样本则不少于 2 段且被采用；若不提供则明确记录沿用默认规则

4. **验证风格保持效果**
   - 检查去痕后的文本是否保持了期望的风格
   - 如果不满意，提供更详细的样本或反馈
   - 确认最终版本符合自己的期望
   - 完成标准: 最终版与原作在用词偏好、句式结构、标点习惯上逐项比对通过

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 用户希望完全重写风格（如从正式变为非正式）
- 不需要风格保持的场景（如匿名写作）
- 用户没有明确的风格偏好
- 快速原型验证（不需要精细风格调整）

**作者的盲点**：
- Blader 假设文本可以清晰分为"个人写作"和"技术文本"两类，但实际上可能存在混合类型
- humanizer 缺少对风格保持程度的配置（如轻度保持 vs 重度保持）
- 没有提到如何处理风格冲突（如个人风格与技术文档规范冲突）