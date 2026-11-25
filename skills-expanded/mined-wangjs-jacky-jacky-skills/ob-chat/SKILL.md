---
name: ob-chat
description: "Obsidian 知识库问答。当用户想要查询知识库、基于笔记回答问题、在知识库中搜索信息时触发此 skill。也支持通过文章 ID（OBA-{8位随机ID}）直接定位文章。"
---

<role>Obsidian 知识库问答助手，通过索引优先的方式从知识库中检索并综合回答用户问题。</role>
<purpose>基于 wiki/index.md 导航知识库，选择最相关的文章综合回答。</purpose>
<trigger>

```text
触发词：
- 问一下知识库
- 查询笔记
- ob-chat
- 知识库问答
- 在我的笔记中查找
- 根据我的知识库回答

文章 ID 触发（自动识别）：
- 用户消息中包含 OBA-{8位随机ID} 格式的 ID（如 OBA-k7jm2p9q, OBA-xn8btf3w）
- 自动理解为"基于该 ID 对应的 Obsidian 文章回答问题"
- 无需显式调用 ob-chat

示例：
- "ob-chat RLHF 和 chain-of-thought 有什么关系？"
- "在我的知识库中查找关于 Transformer 的内容"
- "问一下：注意力机制和 RLHF 有什么共同点？"
- "OBA-k7jm2p9q 里提到的终端跳转方案，能详细解释下吗？"
- "看看 OBA-xn8btf3w 这篇文章"
```

</trigger>
<gsd:workflow xmlns:gsd="urn:gsd:workflow">
  <gsd:meta>requires=OBSIDIAN_REPO; focus=query,answer</gsd:meta>
  <gsd:goal>通过索引优先检索从知识库中找到最相关文章，综合回答用户问题，并将答案归档回 wiki 实现知识复利。</gsd:goal>
  <gsd:phase>**委托 ob-router skill** 解析当前激活仓库路径，读取 wiki/index.md 作为导航入口。</gsd:phase>
  <gsd:phase>从索引中定位 1-2 个最相关子分类，选择 3-5 篇具体文章。</gsd:phase>
  <gsd:phase>读取选中的完整文章，综合回答用户问题，带 [[wikilinks]] 引用。</gsd:phase>

</gsd:workflow>

# Obsidian 知识库问答 (ob-chat)

基于索引的知识库问答，答案归档实现知识复利。

## 配置检查

**【硬约束】仓库路径一律委托 ob-router skill 解析，本 skill 不自行读取路径文件。**

调用 ob-router skill 获取 `$OBSIDIAN_REPO`：
- ob-router 内部处理优先级（ob-router.json → CLAUDE.md → 询问）
- 若 ob-router.json 不存在，ob-router 会**主动提示** `ob-router init` 持久化
- 若存在多个仓库，ob-router 会**主动询问**切换目标，不静默使用默认值

将 ob-router 返回的路径保存为 `$OBSIDIAN_REPO`，后续全程使用此变量。
4. 检查 `$OBSIDIAN_REPO/wiki/index.md` 是否存在
5. 如果不存在，提示用户先运行 ob-index 初始化知识库

## 执行流程

### 第零步：文章 ID 识别（优先级最高）

检查用户消息是否包含文章 ID（格式 `OBA-[a-z0-9]{8}`）：

1. 如果包含 ID → 在所有项目的 `index.md` 中查找匹配行，获取文件路径
2. 直接读取该文章全文，基于文章内容回答用户问题
3. 跳过第一步和第二步（不需要索引检索）
4. 回答中标注 `[OBA-{id}]` 引用来源

**查找路径**：遍历 `$OBSIDIAN_REPO/wiki/projects/*/index.md`，匹配表格中 ID 列。

**用户提到多个 ID 时**：读取所有匹配文章，综合回答。

### 第一步：读取索引

读取 `$OBSIDIAN_REPO/wiki/index.md`，获取知识库全局导航。

**如果索引文件过长**（超过 200 行）：
1. 先读取主索引中的分类标题
2. 根据问题定位到最相关的 1-2 个子分类
3. 读取对应的子索引文件

**如果知识库为空**：
```
知识库索引为空。请先使用 ob-collect 采集内容或使用 ob-index 初始化知识库。
```

### 第二步：定位相关文章

从索引的一行摘要中，选择 3-5 篇最相关的文章。

**选择标准**：
1. 标题或摘要直接包含问题关键词
2. 概念文章优先于来源文章（更凝练）
3. 综合文章优先（已经过二次提炼）

**展示检索过程**：
```
索引检索：
→ 分类：概念 → 选中 3 篇
  - [[concepts/rlhf]] — "用人类反馈强化学习对齐语言模型"
  - [[concepts/chain-of-thought]] — "引导模型逐步推理的提示技术"
  - [[concepts/attention]] — "让模型动态权衡 token 相关性"
→ 分类：来源 → 选中 2 篇
  - [[sources/instructgpt]] — "OpenAI 的 RLHF 实践"
  - [[sources/cot-paper]] — "Chain-of-Thought 原始论文"
```

### 第三步：读取并综合回答

1. 读取选中的 3-5 篇文章全文
2. 综合回答用户问题
3. 回答中所有知识库概念使用 `[[wikilinks]]` 引用
4. **识别 code-ref callout**：文章中包含 `> [!code-ref]` 的内容，作为"相关代码"部分展示
5. 底部列出参考文章和相关代码

**回答格式**：

```markdown
## {回答标题}

{综合回答内容，使用 [[wikilinks]] 引用相关概念}

### 相关代码

> [!code-ref] {从文章中提取的 code-ref，直接展示}
> ...

---

### 参考
- [[sources/{来源 1}]]
- [[concepts/{概念 1}]]
- [[synthesis/{综合文章}]]
- [OBA-{id}] {文章标题}（如涉及项目知识文章）
```

**code-ref 展示规则**：
- 文章中的 code-ref callout 直接带入回答的"相关代码"部分
- 如果用户问的是"怎么实现某功能"，优先展示与该功能相关的 code-ref
- code-ref 中的 GitHub 链接直接呈现，用户可点击直达代码

**文章 ID 展示规则**：
- 引用项目知识文章时，在参考中标注 `[OBA-{id}]` + 文章标题
- 方便用户后续直接用 ID 引用该文章





### 无法回答时

如果知识库中没有足够信息回答问题：

```
知识库中未找到足够信息回答此问题。

已有相关内容：
- [[concepts/{相关概念}]] — 部分相关

建议采集以下内容以补充知识库：
1. {建议的来源/文章}
2. {建议的来源/文章}
```

将"无法回答"本身也记录为知识缺口，追加到 log.md。
