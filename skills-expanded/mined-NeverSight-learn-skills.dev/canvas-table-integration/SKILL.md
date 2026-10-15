---
name: canvas-table-integration
description: Use when integrating `@qfei-design/canvas-table` into an existing app or page. Covers consumer-side local or virtual tables, public props/methods/events, row-head suffix actions, selection, drag, fixed columns, summary rows, empty states, lightweight `render + TextShape + shape click` interactions, host-side cell-edit architecture, schema-driven Make field editors, mandatory ExpensePoc-derived cell-edit standards, `customEdit`, `commit/cancel`, object `autoClose`, `relatedElements`, `overlayOptions`, `editApplyMode: controlled`, attachment editors, and Make field-display columns with value normalization, ExpensePoc-derived field renderers, and overflow-only tooltip behavior. Only supports `@qfei-design/canvas-table`, never UI-library tables. Read package AI docs first, choose Track A, B, or C, use documented public APIs, and do not modify the table library itself.
---

# canvas-table-integration

Use this skill only for **consumer-side integration** of `@qfei-design/canvas-table`. It does not support Ant Design Table, Arco Table, TDesign Table, native HTML tables, or any other table implementation as the product table.

This skill has three tracks:

- **Track A: first-version base integration**
  - basic local table
  - virtual remote table
  - common public props / methods / events
  - default row sequence numbers and hover-revealed open-detail row-head suffix action
  - optional row selection / drag / summary / empty state
  - row-head suffix actions such as an open-detail icon after the sequence number
  - lightweight `render + TextShape + shape click`
- **Track B: second-version cell-edit enhancement**
  - `editType` / `customEdit`
  - `commit` / `cancel`
  - object `autoClose`
  - `relatedElements` / `overlayOptions` / `destroy`
  - `editApplyMode: "controlled"`
  - host-side edit controller architecture
  - editor-container patterns
  - field-editor mappings
  - non-popup / 非弹窗 inline editor chrome: keep only the CanvasTable active edit border; inner input, textarea, number, select, and date triggers must be full-cell and borderless
  - ExpensePoc-derived editable-cell defaults: double-click enters edit, clipped cells scroll fully into view before editing, popup editors open immediately, inline editors fill the active cell, and unchanged values do not call save APIs
  - ExpensePoc-derived popup visibility, empty-value, no-double-border, and attachment-panel visual rules
  - schema field-type mappings for display value vs submit value
  - draft save layer vs immediate save layer
  - positioning / scroll / popup close handling
  - attachment editor integration
- **Track C: Make field-display integration**
  - schema-driven columns for supported Make field types
  - shared Make field type registry in `apps/ui/src/lib/make-field-types.ts` or the host equivalent
  - pure value normalization before canvas rendering
  - text / URL / number / date / tag / user / department / attachment / lookup renderers
  - default overflow-only tooltip behavior for text, tags, users, files, and lookup values
  - folder separation for `config`, `renderers`, `hooks`, `types`, and value adapters

Choose the track first. Do not mix a basic table integration request with a full cell-edit architecture refactor unless the user clearly wants the editing workflow.
If the user says display-only, field type display, or schema field rendering, choose Track C and leave cell editing out unless explicitly requested.
For new Make App projects or pages that display Make schema records, choose Track C by default even when the user only says "add a table" or "show a list". Use Track A only for `@qfei-design/canvas-table` pages whose columns are not Make schema-driven.
Hard Track B rule: every CanvasTable cell edit / 单元格编辑 implementation must follow Track B plus `references/make-cell-edit-defaults.md`. Missing borderless full-cell editors, host component-library field editors, immediate popup opening, post-scroll positioning, normalized values, or unchanged-value save skipping is a readiness and delivery blocker; do not report the table as complete.

## Quick start

1. Confirm this is a consumer-side table integration, not table-library maintenance.
2. Check package installation and read the package AI docs in the required order below.
3. Choose exactly one primary track: Track A display table, Track B editable cells, or Track C Make field display. If Make schema fields are in scope, Track C is the default.
4. For Make schema tables, load and normalize schema fields before initializing the table; build `IColumn[]` plus renderers from the normalized field types and the shared field type registry.
5. Read only the track references from the topic map.
6. Start from the package recipe/example when available, then adapt with the smallest project-local diff.
7. Enable table row defaults unless the user explicitly opts out: `showSN` sequence numbers plus a hover-revealed open-detail action through `bodyRowHeadSuffixOptions`.
8. For Make schema tables, apply the ExpensePoc-derived field renderer defaults. Text-bearing overflow must show ellipsis, and tooltip is enabled by default only for ellipsized overflow or hidden `+N` content; do not require the user to ask for it.
9. When the object/entity/schema key changes, reset table interaction state and scroll position. Do not carry the previous object's horizontal or vertical scroll into the next object.
10. If Track B is in scope, verify the mandatory cell-edit standard before finishing; a non-standard cell editor is not a shippable partial result.
11. Add only the capabilities the user explicitly needs now; pagination, selection, grouping, and editing are not defaults.
12. Before finishing, read the relevant pitfalls reference and verify one concrete table path.

## Typical requests

### Track A: base integration

- 在页面里接入 `canvas-table`
- 把现有列表替换成 canvas table
- 接一个本地数据表格
- 接后端分页 / 虚拟滚动表格（仅在用户明确要求分页或虚拟加载时）
- 只要接入表格，默认显示行序号，行 hover 时在行头显示进入详情图标；除非用户明确说不需要详情入口
- 按需做行选择、汇总、空状态、固定列
- 在序号列 / 行头后面添加进入详情、展开、快捷操作图标
- 把单元格渲染成可点击文本 / 链接
- 把 JSON meta 转成 `IColumn[]`

### Track B: cell-edit enhancement

- 给 canvas table 增加单元格编辑
- 设计或接入 `customEdit`
- 复用项目已有输入框 / 下拉 / 日期 / 人员 / 部门 / 附件组件
- 修复非弹窗单元格编辑出现二次边框、输入框内缩、数字字段不是数字输入框、日期/下拉没有立即打开等问题
- 让表格 cell editor 的 Make 字段映射与 Drawer 表单保持一致
- 按 ExpensePoc 默认方式处理双击进入编辑、编辑前滚动到可见、编辑器定位、弹窗左右/上下边界、关闭、保存、回显、回填、回滚
- 增加文本 / 数字 / 日期 / 选项 / 人员 / 部门 / 附件字段编辑
- 按后端字段类型补齐 18 种 Make 字段的展示和可编辑/只读边界
- 把现有项目字段编辑器接进 canvas table
- 修复双击进入编辑后弹窗没有立即打开、被遮挡单元格没有先滚动到可见、编辑器没有铺满单元格、回显缺失、未修改仍调用接口等单元格编辑问题

### Track C: Make field-display integration

- 根据 Make 字段类型生成 canvas table 展示列
- 新 Make 项目中只要是 schema 驱动的业务表格，默认按当前 ExpensePoc 表格展示基线生成；除非用户明确要求不同展示
- 新 Make POC 项目中在 `apps/ui/src/lib/make-field-types.ts` 或宿主等价文件维护统一字段类型 registry，表格列、详情展示、表单控件、筛选值编辑器和单元格编辑器都从这里取字段类型语义
- 把 18 种字段类型按展示族分类处理
- 默认处理列宽溢出：文本内容超出时显示省略号并展示 tooltip，未超出不展示 tooltip；多值被折叠为 `+N` 时，`+N` tooltip 展示完整列表
- 按 ExpensePoc 表格默认渲染附件、lookup、下拉标签、人员、部门、日期、金额等字段
- 把后端字段返回值规范化后展示在 canvas 表格中
- 拆分 `config` / `renderers` / `hooks` / `types` / value adapter
- 只处理展示，不做单元格编辑

## Do not use this skill for

- publishing `@qfei-design/canvas-table`
- editing the table library itself
- generating or keeping another product table implementation instead of `@qfei-design/canvas-table`
- maintaining `package.ai.json`, `recipes.json`, examples, or docs inside the table library repo
- configuring private npm registries
- treating grouped-table architecture as the default answer
- forcing a new UI component library into a project that already has an editor/component system

## Pre-flight check

Before editing code:

1. Confirm `@qfei-design/canvas-table` is installed in the current project.
2. If there is no `package.json`, stop and tell the user the current directory is not an npm package.
3. If the package is missing, detect the package manager from the lockfile and install it before continuing:
   - `pnpm-lock.yaml` -> `pnpm add @qfei-design/canvas-table`
   - `yarn.lock` -> `yarn add @qfei-design/canvas-table`
   - `package-lock.json` -> `npm install @qfei-design/canvas-table`
4. If no lockfile exists, default to `npm install @qfei-design/canvas-table`.
5. If install fails, stop and report the command and error.

Use `@qfei-design/canvas-table` consistently. If an existing codebase uses a different package name, stop and ask before changing the consumer app dependency.

If an existing Make record list uses another table component, the expected integration target is still `@qfei-design/canvas-table`. Do not preserve a UI-library table as the main record table unless the user explicitly says this page is out of scope for canvas-table.

## Required read order

Prefer reading from the installed package:

1. `node_modules/<pkg>/package.ai.json`
2. `node_modules/<pkg>/docs/agent-usage.md`
3. `node_modules/<pkg>/recipes.json`
4. `node_modules/<pkg>/capabilities.json`
5. `node_modules/<pkg>/PUBLIC_API.md`

If the project is working directly inside the table monorepo, use the source paths instead:

1. `packages/table/package.ai.json`
2. `packages/table/docs/agent-usage.md`
3. `packages/table/recipes.json`
4. `packages/table/capabilities.json`
5. `packages/table/PUBLIC_API.md`

Then choose the track-specific references.

## Topic reference map

| Task / topic | Read |
| --- | --- |
| Public props, methods, events, setup, cleanup | `references/core-props-methods-events.md` |
| Row-head sequence number or open-detail action | `references/row-head-action-patterns.md` |
| Virtual loading / paginated backend integration | `references/virtual-table-patterns.md` |
| Schema/meta to `IColumn[]` | `references/column-patterns.md` |
| Custom clickable cell shapes | `references/shape-render-patterns.md` |
| Track A pitfalls | `references/common-pitfalls.md` |
| Cell-edit contract | `references/edit-contract.md` |
| Host-side edit architecture | `references/edit-host-architecture.md` |
| Edit lifecycle, positioning, close/commit/rollback | `references/edit-interaction-lifecycle.md` |
| ExpensePoc-derived Make editable-cell defaults | `references/make-cell-edit-defaults.md` |
| Field editor mapping | `references/field-editor-patterns.md` |
| Host component choice | `references/editor-component-selection.md` |
| Attachment editor integration | `references/attachment-editor-patterns.md` |
| Track B pitfalls | `references/edit-common-pitfalls.md` |
| Make field display | `references/make-field-display-patterns.md` |
| Proven downstream usage and unvalidated areas | `references/validated-usage-notes.md` |
| Track workflows, capability checklists, output templates | `references/track-workflows.md` |

### For Track A: base integration

Read as needed:

- `references/core-props-methods-events.md`
- `references/row-head-action-patterns.md` when adding an icon or action to the body row head / sequence-number area
- `references/virtual-table-patterns.md` when using paginated virtual loading
- `references/column-patterns.md` when shaping columns
- `references/shape-render-patterns.md` when adding custom clickable cell content
- `references/common-pitfalls.md` before finalizing changes

### For Track B: cell-edit enhancement

Read in this order:

1. package-level cell-edit docs and source entry points
2. `references/edit-contract.md`
3. `references/edit-host-architecture.md`
4. `references/edit-interaction-lifecycle.md`
5. `references/make-cell-edit-defaults.md`
6. `references/field-editor-patterns.md`
7. `references/editor-component-selection.md`
8. `references/attachment-editor-patterns.md` when attachment fields are in scope
9. `references/edit-common-pitfalls.md` before finalizing changes

If any required package file is missing, stop and tell the user exactly which file is missing.

### For Track C: Make field-display integration

Read:

- `references/make-field-display-patterns.md`
- `references/shape-render-patterns.md` when adding canvas shapes
- `references/column-patterns.md` when deriving `IColumn[]` from field schemas
- `references/common-pitfalls.md` before finalizing changes

## Track A: first-version base integration scope

Use Track A for basic local tables, explicitly requested virtual/paginated tables, row-head defaults, optional public table capabilities, and lightweight clickable cell shapes. Do not turn a first-pass integration into grouped table or cell-edit work unless the user explicitly asks for that deeper path. For the detailed workflow and capability checklist, read `references/track-workflows.md`.

## Track B: second-version cell-edit enhancement scope

Use Track B when the user explicitly needs editable cells or a host-side field-editor system.

This track covers host-side edit controller design, editor containers, `editType` / `customEdit`, commit/cancel behavior, overlay positioning, value validation, rollback, and attachment-field editor integration. It does **not** require a fixed UI library; prefer the current project's existing editor components. For every CanvasTable editable table, the ExpensePoc-proven edit baseline in `references/track-workflows.md` and `references/make-cell-edit-defaults.md` is mandatory. Product-specific editors may vary only when they still satisfy the same lifecycle, value, popup, and no-double-border requirements.

## Track C: Make field-display integration scope

Use Track C when the task is to show Make platform fields correctly in canvas-table. In new Make App projects, this is the default for every Make schema-driven business table unless the user explicitly asks for a different table style. Keep it display-only: normalize backend values into a small display model, then route by display group to focused renderers. Before writing table-specific column or renderer branches in a new Make POC, create or reuse the shared field type registry described in `references/make-field-display-patterns.md`.

Default grouping:

- text: `Make.Field.ID`, `Make.Field.Text`, `Make.Field.TextArea`
- url: `Make.Field.URL`
- number: `Make.Field.Number`, `Make.Field.Currency`, `Make.Field.Percent`
- date: `Make.Field.Date`, `Make.Field.DateTime`, `Make.Field.DateRange`
- select: `Make.Field.SingleSelect`, `Make.Field.MultiSelect`
- user: `Make.Field.SingleUser`, `Make.Field.MultiUser`
- department: `Make.Field.SingleDepartment`, `Make.Field.MultiDepartment`
- file: `Make.Field.File`
- lookup: `Make.Field.Lookup`

Default Make schema table baseline:

- initialize the table only after runtime schema fields are available; missing schema is a blocking loading/error state, not a reason to infer columns from row keys
- derive columns from normalized runtime schema fields; do not pass raw remote schema objects or hand-maintain static columns for dynamic Make objects
- each generated column should retain `fieldType`, `fieldSchema`, and `renderKind` or equivalent metadata for renderer dispatch
- derive each generated column's `renderKind`, default width, alignment, and multiplicity from the shared field type registry before applying thin business overrides
- normalize field values once through a pure adapter before canvas rendering
- route display by field type group, not by business field names, except for explicit business roles such as a primary code link
- use the ExpensePoc-proven renderer families by default: text/link, tag list, compact user avatar/name list, attachment list, lookup reference text, and safe generic fallback
- number, currency, and percent renderers must only format finite parsed numbers; blank, invalid, `NaN`, `Infinity`, or unparseable values render the empty placeholder `-` and must never display `NaN`
- apply ellipsis plus overflow-only tooltip by default: visible text/tag/user/lookup labels must show ellipsis when truncated and get tooltip only when ellipsized; attachment/tag/user/lookup `+N` badges get a tooltip with the full hidden value list
- keep option, user, department, file, and lookup candidate loading outside cell renderers. Generated Make App table editors use the same default UI-Service candidate contract as forms: `GET /api/users?keyword=&page=&size=` and `GET /api/departments?keyword=&page=&size=`, or host equivalent routes, normalized to `userId/userName` and `departmentId/departmentName`
- treat object/entity/schema key as table identity. On identity change, rebuild or reset the table so scrollLeft/scrollTop, active edit state, selection, hover/suffix state, and header popups do not leak from the previous object
- preserve row defaults: `showSN` sequence numbers plus hover-revealed detail entry through `bodyRowHeadSuffixOptions`

## Safety rules and defaults

Treat these as safety rules:

- browser / client-only; never instantiate during SSR
- use a real DOM container with explicit width and height
- use only documented public APIs
- never import from `src` or `dist`
- use `@qfei-design/canvas-table` for product tables; do not substitute UI-library tables
- use `table.tableId` as the namespace key for `globalEventBus.onWithNamespace(...)`
- destroy the table instance on unmount / cleanup
- reset scroll and transient table state when switching object/entity/schema routes. Reusing the same React component for `/objects/:objectKey` is fine only if the table is keyed by that identity or the integration explicitly resets the canvas-table instance/state on identity change
- never pass raw meta directly into the table runtime
- convert meta into `IColumn[]` before creating the table
- for Make schema tables, do not create the table with generic placeholder columns or row-key-inferred columns while waiting for schema
- never render numeric parser failures as `NaN`, `Infinity`, or exception text; normalize them to an empty display value before canvas rendering
- do not put `aria-hidden` or `inert` on the visual canvas-table host, or on any ancestor that can contain the package-created focusable canvas
- if a screen-reader fallback table is needed, keep it as a separate visually-hidden structure and give the visual host its own non-hidden accessible label
- pagination is opt-in: do not add visible pagination controls, page-size selectors, page state, page query params, total-count handling, paginated fetch logic, `virtualOptions`, or `data:load` wiring unless the user explicitly asks for pagination, virtual loading, or paginated backend integration

## Detailed workflows and maintenance references

- For track workflows, capability checklists, avoid lists, deferred topics, and final response templates, read `references/track-workflows.md`.
- Before using a capability that is not obviously covered by the current project or package docs, read `references/validated-usage-notes.md` to distinguish validated downstream patterns from less-proven package capabilities.
