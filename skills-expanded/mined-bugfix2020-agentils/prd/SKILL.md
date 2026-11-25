---
name: prd
description: '为新功能生成 Product Requirements Document（PRD）。触发词：create a prd、write prd for、plan this feature、requirements for、spec out、创建 PRD、写需求文档。'
user-invocable: true
---

# PRD 生成器

为新功能生成清晰、可执行的产品需求文档。

---

## 工作步骤

1. 接收功能描述
2. 提出 3–5 个关键澄清问题（带字母选项）
3. 根据回答生成结构化 PRD
4. 保存到 `tasks/prd-[feature-name].md`

**重要：不要开始实现，只生成 PRD。**

---

## 澄清问题格式

```
1. 这个功能的主要目标是什么？
   A. 改善用户引导体验
   B. 提高用户留存
   C. 减少支持负担
   D. 其他：[请说明]

2. 目标用户是谁？
   A. 仅新用户
   B. 仅现有用户
   C. 所有用户
   D. 仅管理员
```

用户可以用 "1A, 2C" 快速回答。

---

## PRD 结构

```markdown
# PRD: [功能名]

## 简介

功能描述及其解决的问题。

## 目标

具体、可衡量的目标（列表）。

## User Stories

### US-001: [标题]

**描述：** As a [user], I want [feature] so that [benefit].

**验收标准：**

- [ ] 具体可验证的标准
- [ ] Typecheck passes
- [ ] [UI story 必须包含] Verify in browser

## 功能需求

- FR-1: 系统必须允许用户...
- FR-2: 当用户点击 X 时，系统必须...

## 非目标（范围外）

列出明确不做的事。

## 设计考量（可选）

UI/UX 要求，mockup 链接。

## 技术考量（可选）

已知约束、依赖项、集成点。

## 成功指标

如何衡量成功？

## 开放问题

待澄清的问题。
```

---

## Story 大小规则

**每个 story 必须能在一次 Ralph 迭代（一个 context window）内完成。**

正确大小的 story：

- 添加一个数据库列和迁移
- 在现有页面添加一个 UI 组件
- 更新一个 server action

太大（需要拆分）：

- "构建整个 dashboard" → 拆为：schema、queries、UI 组件、过滤器
- "添加认证" → 拆为：schema、middleware、登录 UI、session 处理

---

## 验收标准规则

必须可验证，不能模糊：

好的标准：

- "tasks 表添加 status 列，默认 'pending'"
- "过滤下拉框有选项：All、Active、Completed"

差的标准：

- "正常工作"
- "处理边缘情况"

**每个 story 必须包含：**

- `Typecheck passes`
- UI story 额外包含：`Verify in browser`

---

## 输出

- **格式：** Markdown
- **位置：** `tasks/`
- **文件名：** `prd-[feature-name].md`（kebab-case）
