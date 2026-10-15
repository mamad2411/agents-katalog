---
name: element-ai-vue-helper
description: 帮助用户集成和使用 element-ai-vue 组件来构建 AI 聊天界面、Markdown 渲染、代码高亮、打字机效果等 AI 交互功能。当用户提到 AI 聊天、对话界面、Markdown 展示、代码高亮、思考链、消息气泡、聊天中的文件上传，或者提到 element-ai-vue 的任何具体组件名称（如 ElAMarkdown、ElABubble、ElASender、ElAThinking、ElATypewriter 等）时触发此技能。当用户在 element-ai-vue 项目本身中工作并想要添加或修改组件时也使用此技能。确保在用户提到任何与 AI 对话、聊天界面、打字机效果、Markdown 渲染、思考过程展示相关的需求时都主动使用此技能。
---

# Element AI Vue 助手

此技能帮助用户集成和使用 `element-ai-vue` 组件库，这是一个为 Vue 3 应用提供企业级 AI 交互组件的库。

## 何时使用此技能

当用户需要以下功能时使用此技能：

- 构建 AI 聊天或对话界面
- 实现带代码高亮和数学公式的 Markdown 渲染
- 添加流式文本的打字机效果
- 创建聊天应用的消息气泡
- 展示 AI 思考过程或推理链
- 在 AI 聊天场景中处理文件上传
- 使用 Shiki 实现代码语法高亮
- 渲染 Mermaid 图表
- 构建支持 @提及 功能的富文本输入

当用户提到以下具体组件名称时也使用此技能：
- `ElAMarkdown`、`ElABubble`、`ElABubbleList`、`ElASender`
- `ElAThinking`、`ElAThoughtChain`、`ElATypewriter`
- `ElACodeHighlight`、`ElACodeMermaid`
- `ElAFilesUpload`、`ElAFilesCard`、`ElADragUpload`
- `ElAOverflowToolbar`、`ElAPpt`

## 快速开始

### 安装

```bash
# 使用 pnpm（推荐）
pnpm install element-ai-vue

# 使用 npm
npm install element-ai-vue
```

### 导入样式（必需！）

在 `main.ts` 中：

```typescript
import 'element-ai-vue/dist/index.css'
```

### 基础示例

```vue
<template>
  <div class="chat">
    <ElABubble
      v-for="msg in messages"
      :key="msg.id"
      :placement="msg.role === 'user' ? 'end' : 'start'"
      :content="msg.content"
      :is-markdown="msg.role === 'assistant'"
    />

    <ElASender
      v-model="input"
      @send="handleSend"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElABubble, ElASender } from 'element-ai-vue'

const messages = ref([])
const input = ref('')

const handleSend = (content: string) => {
  messages.value.push({
    id: Date.now().toString(),
    role: 'user',
    content,
  })
  input.value = ''
}
</script>
```

## 核心组件

### 1. ElAMarkdown - Markdown 渲染器

支持代码高亮、数学公式、Mermaid 图表。

```vue
<ElAMarkdown :content="markdownText" />
```

**主要特性**：
- 代码高亮（100+ 语言）
- KaTeX 数学公式
- Mermaid 流程图
- 自定义插槽扩展

**详细文档**：查看 [references/markdown.md](./references/markdown.md)

### 2. ElABubble - 对话气泡

聊天消息气泡，支持打字机效果。

```vue
<ElABubble
  placement="start"
  :content="message"
  :typing="true"
  :is-markdown="true"
/>
```

**主要特性**：
- 左右位置（AI/用户）
- 打字机效果
- Markdown 渲染
- 加载动画
- 多种样式变体

**详细文档**：查看 [references/bubble.md](./references/bubble.md)

### 3. ElABubbleList - 消息列表容器

提供自动滚动功能的消息列表容器。

**详细文档**：查看 [references/bubble-list.md](./references/bubble-list.md)

### 4. ElASender - 富文本输入框

基于 Tiptap 的输入框，支持文件粘贴。

```vue
<ElASender
  v-model="content"
  @send="handleSend"
  @paste-file="handlePasteFile"
/>
```

**主要特性**：
- 富文本编辑
- 文件粘贴
- 自定义扩展
- 加载状态
- 水平/垂直布局

**详细文档**：查看 [references/sender.md](./references/sender.md)

### 5. ElAThinking - 思考过程展示

可折叠的思考过程展示组件。

**详细文档**：查看 [references/thinking.md](./references/thinking.md)

### 6. ElAThoughtChain - 思维链可视化

展示连续推理步骤的思维链组件。

**详细文档**：查看 [references/thought-chain.md](./references/thought-chain.md)

### 7. 打字机效果

`useTyperwriter` Hook 实现逐字显示。

```vue
<script setup>
import { useTyperwriter } from 'element-ai-vue'

const { start, setText, content } = useTyperwriter({
  interval: 50
})

setText('要显示的文本')
start()
</script>

<template>
  <div>{{ content }}</div>
</template>
```

**详细文档**：查看 [references/typewriter.md](./references/typewriter.md)

### 8. 文件上传组件

完整的文件上传解决方案。

```vue
<ElADragUpload
  v-model="fileList"
  :on-upload="handleUpload"
>
  <ElAFilesCard v-model="fileList" />

  <ElASender
    v-model="message"
    @paste-file="handlePasteFile"
  />
</ElADragUpload>
```

**包含组件**：
- `ElAFilesUpload` - 文件选择器
- `ElADragUpload` - 拖放区域
- `ElAFilesCard` - 文件预览
- `useFileOperation` - 文件操作 Hook

**详细文档**：
- [references/file-upload.md](./references/file-upload.md) - 文件上传组件概览
- [references/drag-upload.md](./references/drag-upload.md) - ElADragUpload 详细文档
- [references/files-card.md](./references/files-card.md) - ElAFilesCard 详细文档

### 9. ElACodeHighlight - 代码高亮

独立的代码高亮组件，使用 Shiki。

**详细文档**：查看 [references/code-highlight.md](./references/code-highlight.md)

### 10. ElACodeMermaid - Mermaid 图表

独立的 Mermaid 图表渲染器。

**详细文档**：查看 [references/code-mermaid.md](./references/code-mermaid.md)

### 11. ElAOverflowToolbar - 溢出工具栏

自动收起溢出项的工具栏组件。

**详细文档**：查看 [references/overflow-toolbar.md](./references/overflow-toolbar.md)

## 常见使用场景

### 场景 1：基础聊天界面

用户说："我想创建一个 AI 聊天界面"

**回复要点**：
1. 使用 `ElABubble` 显示消息
2. 使用 `ElASender` 作为输入框
3. 区分用户和 AI 消息（placement 属性）
4. AI 消息启用 Markdown

**参考示例**：查看 [examples.md](./examples.md) 中的"基础 AI 聊天界面"

### 场景 2：打字机效果

用户说："需要打字机效果" 或 "逐字显示"

**回复要点**：
1. 方式 1：在 `ElABubble` 中设置 `typing={true}` 并更新 content
2. 方式 2：使用 `useTyperwriter` Hook
3. 配合 `loading` 状态实现完整流程

**参考示例**：查看 [examples.md](./examples.md) 中的"带打字机效果的聊天"

### 场景 3：文件上传

用户说："支持文件上传" 或 "拖拽文件"

**回复要点**：
1. 使用 `ElADragUpload` 包裹输入区域
2. 使用 `ElAFilesCard` 显示文件预览
3. 使用 `useFileOperation` 处理粘贴
4. 在 `onUpload` 中更新进度

**参考示例**：查看 [examples.md](./examples.md) 中的"带文件上传的聊天"

### 场景 4：Markdown 展示

用户说："渲染 Markdown" 或 "代码高亮"

**回复要点**：
1. 使用 `ElAMarkdown` 组件
2. 支持代码高亮、数学公式、Mermaid
3. 可以与 `useTyperwriter` 结合实现流式输出

**参考示例**：查看 [examples.md](./examples.md) 中的"Markdown 文档展示"

## 提供帮助的原则

### 1. 始终提供完整代码

不要只给片段，提供可以直接运行的完整 Vue 组件代码，包括：
- `<template>`
- `<script setup lang="ts">`
- `<style scoped>`
- 必要的导入语句

### 2. 使用 TypeScript

展示正确的类型定义：

```typescript
import type { FilesUploadItem } from 'element-ai-vue'

const fileList = ref<FilesUploadItem[]>([])
```

### 3. 解释关键概念

- **placement**：`'start'`（左侧，AI）vs `'end'`（右侧，用户）
- **typing**：打字机效果开关
- **loading**：加载状态（三个跳动的点）
- **isMarkdown**：是否渲染为 Markdown

### 4. 提及相关组件

如果用户问聊天，提及：
- `ElABubble`（消息显示）
- `ElASender`（输入框）
- `ElAFilesCard`（文件预览）
- `useTyperwriter`（打字机效果）

### 5. 包含常见陷阱

提醒用户：
- ✅ 必须导入 CSS：`import 'element-ai-vue/dist/index.css'`
- ✅ 打字机需要 `typing={true}` 且持续更新 content
- ✅ 文件上传需要手动更新 progress 和 uploadingStatus
- ✅ AI 消息设置 `isMarkdown={true}`

## 文档结构

本 skill 包含以下详细文档：

- **[installation.md](./installation.md)** - 安装和配置指南
- **[examples.md](./examples.md)** - 快速开始示例
- **[references/markdown.md](./references/markdown.md)** - ElAMarkdown 完整文档
- **[references/bubble.md](./references/bubble.md)** - ElABubble 完整文档
- **[references/bubble-list.md](./references/bubble-list.md)** - ElABubbleList 完整文档
- **[references/sender.md](./references/sender.md)** - ElASender 完整文档
- **[references/thinking.md](./references/thinking.md)** - ElAThinking 完整文档
- **[references/thought-chain.md](./references/thought-chain.md)** - ElAThoughtChain 完整文档
- **[references/typewriter.md](./references/typewriter.md)** - 打字机效果文档
- **[references/file-upload.md](./references/file-upload.md)** - 文件上传组件概览
- **[references/drag-upload.md](./references/drag-upload.md)** - ElADragUpload 完整文档
- **[references/files-card.md](./references/files-card.md)** - ElAFilesCard 完整文档
- **[references/code-highlight.md](./references/code-highlight.md)** - ElACodeHighlight 完整文档
- **[references/code-mermaid.md](./references/code-mermaid.md)** - ElACodeMermaid 完整文档
- **[references/overflow-toolbar.md](./references/overflow-toolbar.md)** - ElAOverflowToolbar 完整文档

## 工作流程

当用户请求帮助时：

1. **识别需求**：判断用户需要哪些组件
2. **提供示例**：从 examples.md 中选择最接近的示例
3. **详细说明**：引用相关组件文档中的具体 API
4. **完整代码**：提供可直接运行的完整代码
5. **注意事项**：提醒常见陷阱和最佳实践

## 示例回复模板

### 用户问："如何创建 AI 聊天界面？"

**回复**：

我来帮你创建一个 AI 聊天界面。这需要使用 `ElABubble` 显示消息和 `ElASender` 作为输入框。

首先确保已安装并导入样式：

```bash
pnpm install element-ai-vue
```

```typescript
// main.ts
import 'element-ai-vue/dist/index.css'
```

这是完整的实现代码：

```vue
[提供完整的 Vue 组件代码]
```

**关键点说明**：
- 用户消息使用 `placement="end"`（右侧）
- AI 消息使用 `placement="start"`（左侧）
- AI 消息启用 `is-markdown="true"` 支持富文本
- 使用 `@send` 事件处理发送

如果需要添加打字机效果，查看 [打字机效果文档](./references/typewriter.md)。

如果需要文件上传功能，查看 [文件上传文档](./references/file-upload.md)。

## 外部资源

- **官方文档**：https://element-ai-vue.com
- **GitHub**：https://github.com/1365436742/element-ai-vue
- **在线演示**：https://element-ai-vue.com/base-demo/
- **NPM**：https://www.npmjs.com/package/element-ai-vue

## 总结

此技能通过详细的组件文档和完整的代码示例，帮助用户快速集成 element-ai-vue 构建 AI 交互界面。

**核心原则**：
1. 提供完整可运行的代码
2. 使用 TypeScript 类型
3. 解释关键概念
4. 提及相关组件
5. 提醒常见陷阱
6. 引用详细文档

**文档优先级**：
1. 先看 [examples.md](./examples.md) 找最接近的示例
2. 再查具体组件文档了解详细 API
3. 最后查 [installation.md](./installation.md) 解决配置问题
