---
name: an-ui
description: pc端公共组件库，基于 Ant Design 封装的高级组件集合，包含表单、表格、抽屉、弹窗等
---

# an-ui Skill

pc端公共组件库，基于 Ant Design 二次封装，提供高级表单、高级表格、详情组件、抽屉弹窗等企业级组件。

## When to Use This Skill

Use this skill when you need to:
- 使用 an-ui 的组件（FormPro、TablePro、ModalForm、DrawerForm 等）
- 了解各组件的 props、API 和使用方式
- 查找代码示例和最佳实践
- 理解组件的配置模式和数据流

## Component Reference

### 高级表单 — FormPro

基于 Antd Form 封装，通过 `FormFieldConfig[]` 配置快速生成表单。

**支持的表单项类型：** input、select、cascader、tree-select、radio、checkbox、switch、date-picker、time-picker、auto-complete、input-number、upload（含 OSS）、color、read-only、custom

**核心特性：** hide/readOnly/disabled/required 支持布尔值和函数（表单联动）、templateOptions.request 支持远程加载选项、表单分组、动态表单

*详见 `references/an-ui.md` 高级表单章节*

### 高级表格 — TablePro

基于 Antd Table 封装，提供列设置、排序、扩展操作等功能。

**核心特性：** 完全继承 AntdTable API、列设置面板、拖拽排序、工具条扩展

*详见 `references/an-ui.md` 高级表格章节*

### 可编辑表格 — EditableTable

在 Antd Table 和 FormPro 基础上封装的可在表格内直接编辑的组件。

**核心特性：** columns 同时支持 FormItem 和 AntdTable 属性、dataIndex 作为表单项 name

*详见 `references/an-ui.md` 可编辑表格章节*

### 弹窗表单 — ModalForm

弹窗中的表单录入场景，提供 trigger 减少 state 使用。完全继承 FormPro 和 antd Modal API。

*详见 `references/an-ui.md` 弹窗表单章节*

### 抽屉 — DrawerPro

在 antd Drawer 基础上增加底部按钮功能，提供 trigger。完全继承 AntdDrawer API。

*详见 `references/an-ui.md` 抽屉章节*

### 抽屉表单 — DrawerForm

抽屉中的表单录入场景，提供 trigger。完全继承 FormPro 和 DrawerPro API。

*详见 `references/an-ui.md` 抽屉表单章节*

### 搜索列表 — FilterList

搜索表单+表格整合，适用于搜索和列表展示场景，支持批量操作。

*详见 `references/an-ui.md` 搜索列表章节*

### 搜索表单 — FilterForm

适用于搜索筛选场景，主要为 FilterList 内部使用。完全继承 FormPro API。

*详见 `references/an-ui.md` 搜索表单章节*

### 详情组件 — DescriptionsPro

基于 antd Descriptions 二次封装，用于展示只读信息。完全继承 Descriptions API。

*详见 `references/an-ui.md` 详情组件章节*

## Reference Files

- **`references/an-ui.md`** — 完整组件文档（9 个组件，含 API、示例代码）
- **`references/index.md`** — 文档索引

## Working with This Skill

### 查看组件文档
打开 `references/an-ui.md` 查看完整的组件说明和 API。

### 查找具体组件
在 Component Reference 中点击对应组件，按名称搜索即可快速定位。

### 开发调试
```bash
# 组件库调试
npm link @an/an-ui
npm run dev

# 业务项目调试
npm link @an/an-ui
```

## Quick Tips

- 表单配置使用 `FormFieldConfig[]`，每一项对应 Form.Item + 表单组件
- `type` 字段指定表单组件类型，不传 type 则渲染为普通展示列
- `templateOptions` 传递给表单组件的 props，支持 `request` 获取远程 options
- `hide`/`readOnly`/`disabled`/`required` 支持函数签名为 `(value, extra) => boolean` 实现联动
