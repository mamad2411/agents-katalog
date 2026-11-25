---
name: storybook-best-practice
description: 为给定的 React 组件生成符合规范的 Storybook stories 文件。当用户需要为组件创建 Storybook stories、展示组件用法或生成组件文档时使用。触发短语包括："为这个组件创建stories"、"生成storybook"、"写storybook"等。
---

# Storybook Stories 生成器

此技能为 React 组件生成标准化的 Storybook stories 文件（CSF3 格式）。

## 工作原理

1. 分析目标组件文件（`XxxCard.tsx`），提取 props 接口、默认值、子组件关系
2. 确定组件的主要功能和实际使用场景
3. 按照规范在同目录下生成 `XxxCard.stories.tsx`，包含所有必需 Cases
4. **仅为主组件创建 stories，不为子组件创建 stories 文件**

## 必需 Cases（按顺序）

### 1. Base

- **目的**：展示组件的完整基本用法
- **规则**：每个 props 都传入一个**典型值**，充分覆盖组件的主要功能

### 2. Default

- **目的**：展示组件的默认渲染样式（零配置状态）
- **规则**：`args` 为空对象 `{}`，**严格不传任何 props**，即 `<Component />`
- **禁止**：不得给 Default case 传入任何 args，哪怕组件有必填 props

### 3. BaseUsage

- **目的**：展示组件在真实业务场景中的使用方式
- **规则**：使用 `render` 函数，结合其他真实组件（布局容器、列表、页面片段等）来展示此组件在实际场景中的样子

### 4. 其他代表性 Cases

- 根据组件特性，额外设计 1～3 个有代表性的 Cases
- 典型场景：不同尺寸/变体、加载状态、空数据、禁用、错误状态、长文本截断等
- Case 命名使用 PascalCase 英文名称，含义清晰

## 代码规范

- **格式**：Storybook CSF3（Component Story Format v3）
- **语言**：TypeScript，使用 `Meta<typeof Component>` 和 `StoryObj<typeof Component>`
- **导入**：从 `@storybook/react` 导入 `Meta`、`StoryObj`
- **meta 对象**：`title` 使用 `"Components/XxxCard"` 格式，`component` 指向组件本身
- **参考代码**：严格参照 [代码示例](references/examples.md) 和 [最佳实践案例](best-practice-examples/) 中的写法
- **质量检查**：生成后对照 [检查清单](references/checklist.md) 逐项确认

## 执行步骤

1. 读取目标组件文件，分析 props 类型定义和组件结构
2. 读取 [代码示例](references/examples.md) 了解 CSF3 写法规范
3. 参考 [最佳实践案例](best-practice-examples/) 中的完整示例
4. 生成 stories 文件，确保包含 Base、Default、BaseUsage 和其他代表性 Cases
5. 对照 [检查清单](references/checklist.md) 逐项核查，确认无遗漏
