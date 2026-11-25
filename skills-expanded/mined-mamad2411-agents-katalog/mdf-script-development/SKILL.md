---
name: mdf-script-development
description: Use when developing Yonyou MDF (Model-Driven Framework) frontend client scripts for bills, lists, and forms. Triggers include viewModel event handling, cb.rest API calls, grid/field operations, bill lifecycle hooks (customInit, afterLoadData, beforeValidate, beforePush), reference filtering, inventory/asset business flows, and 用友 diwork 平台客开脚本开发
---

# MDF 前端脚本开发

## Overview

用友 MDF（模型驱动框架）前端脚本是基于 `viewModel` 和 `cb` 命名空间的客户端脚本，运行在 diwork 平台的单据页和列表页中。脚本在页面加载时完整执行一次，通过注册事件监听器实现业务逻辑。

**核心原则**: 所有脚本操作围绕 `viewModel` 事件生命周期展开，通过空值守卫保证安全，通过代理模式处理远程调用。

## 当使用

**触发症状**:
- 需要编写或修改 MDF 客开前端脚本（`*.js` 文件）
- 需要处理单据页/列表页的生命周期事件（customInit, afterLoadData, beforeValidate, beforePush 等）
- 需要操作表格数据（GridModel）或字段值（FieldModel）
- 需要实现参照过滤、字段联动、按钮交互
- 需要调用后端 API（DynamicProxy, invokeFunction）
- 涉及资产业务流（盘点、清册、验收、变动、拆分、新线资产等）
- 需要处理 `_before` / `_after` 字段对比（盘点场景）
- 需要实现批改功能（batchModifySetFields）

**不适用**:
- 移动端独立应用开发（使用不同的 API 体系）
- 后端 Java 开发（服务端函数、数据模型）
- 纯样式修改（CSS 通过主题配置而非脚本）

## 脚本结构

每个脚本在页面加载时执行一次，按以下顺序组织：

```
1. customInit       → 特性启用、按钮显隐、CSS 注入
2. afterLoadData    → 数据驱动的状态配置（按钮、表格列）
3. modeChange       → 模式切换逻辑（browse/edit/add）
4. 字段/表格事件    → 值变更联动、参照过滤
5. beforeValidate   → 保存前校验
6. beforePush       → 推单前校验
7. batchModifySetFields → 批改字段过滤
8. 辅助函数         → 工具方法定义
```

## 快速参考

### 核心对象

| 对象 | 用途 | 详情 |
|------|------|------|
| `viewModel` | 页面根对象，获取字段/表格/按钮 | [API 参考](api-reference.md#viewmodel-方法) |
| `cb.rest` | 网络请求（DynamicProxy, invokeFunction） | [API 参考](api-reference.md#cbb-rest-api) |
| `cb.utils` | 工具函数（弹窗、确认、加载、参照） | [API 参考](api-reference.md#cbb-utils-api) |
| `cb.extend` | 扩展注册（环境配置、特性开关） | [API 参考](api-reference.md#cbb-extend-api) |

### 常用事件

| 事件 | 触发时机 | 返回值 | [详情](lifecycle-events.md) |
|------|---------|--------|------|
| `customInit` | 页面初始化 | 无 | 最早可执行钩子 |
| `afterLoadData` | 数据加载完成后 | 无 | 按钮/表格状态配置 |
| `modeChange` | 模式切换时 | 无 | browse/edit/add |
| `beforeValidate` | 保存前校验 | false 阻止保存 | 校验入口 |
| `beforePush` | 推单（生单）前 | false 阻止推单 | 下推校验 |
| `batchModifySetFields` | 打开批改弹窗 | 无 | 过滤可批改字段 |

### 表格事件

| 事件 | 触发时机 | [详情](lifecycle-events.md) |
|------|---------|------|
| `afterCellValueChange` | 单元格值变化后 | 联动处理 |
| `beforeCellValueChange` | 单元格值变化前 | 返回 false 阻止变更 |
| `beforeInsertRow` | 新行插入前 | 可修改 incoming row |
| `beforeBrowse` | 参照浏览弹窗前 | 设置过滤条件 |

### 常用操作速查

```javascript
// 获取字段/按钮
viewModel.get('fieldId')

// 获取表格（默认表格不传参）
viewModel.getGridModel('bodyvos')

// 字段值
field.getValue() / field.setValue(value)

// 字段状态
field.setState('disabled', true) / field.setVisible(false)

// 表格行
grid.getRows() / grid.getRow(index) / grid.updateRow(index, obj)

// 单元格
grid.setCellValue(index, key, value) / grid.setCellState(index, key, 'disabled', true)

// API 调用
const proxy = cb.rest.DynamicProxy.create({ action: { url: '/api/path?domainKey=' + domainKey, method: 'POST' } });
proxy.action(params, (err, result) => { ... });

// 弹窗
cb.utils.alert('消息', 'error' | 'success' | 'warning' | 'info')
cb.utils.confirm('确认消息', function() { /* 确认 */ })
```

## 完整指南

| 主题 | 文件 | 内容 |
|------|------|------|
| API 参考 | [api-reference.md](api-reference.md) | viewModel、cb.rest、cb.utils、字段模型、表格模型完整 API |
| 生命周期 | [lifecycle-events.md](lifecycle-events.md) | 详情页/列表页事件顺序、各事件详解、注册最佳实践 |
| 常见模式 | [common-patterns.md](common-patterns.md) | 单元格联动、字段联动、按钮处理、代理调用、参照过滤、校验模式 |
| 业务场景 | [business-patterns.md](business-patterns.md) | 盘点流、新线资产流、清册验收流、变动单、拆分单、列表页 |
| 脚本示例 | [examples.md](examples.md) | 从简单到复杂的 8 个完整示例 |

## 官方文档

MDF 官方文档位于内网: [https://bip-pre.yonyoucloud.com/iuap-yonbuilder-designer/ucf-wh/docs-mdf/mdf/index.html#/api/01-mvvm](https://bip-pre.yonyoucloud.com/iuap-yonbuilder-designer/ucf-wh/docs-mdf/mdf/index.html#/api/01-mvvm)

核心文档入口:
- [页面管理 Page](https://doc.yonisv.com/isv/mybook/professional-yonbuilder/mdf/general-js-api/page.html)
- [GridModel 模型](https://doc.yonisv.com/isv/mybook/professional-yonbuilder/mdf/patterns/Grid/GridModel.html)
- [网络请求 Proxy](https://doc.yonisv.com/isv/mybook/professional-yonbuilder/mdf/general-js-api/proxy.html)
- [常用工具 Utils](https://doc.yonisv.com/isv/mybook/professional-yonbuilder/mdf/general-js-api/utils.html)
- [详情页监听](https://doc.yonisv.com/isv/mybook/professional-yonbuilder/mdf/patterns/Listen/billListen.html)
- [列表页监听](https://doc.yonisv.com/isv/mybook/professional-yonbuilder/mdf/patterns/Listen/listListen.html)

## 命名约定

- **字段名**: snake_case，嵌套字段用 `__` 分隔（如 `pk_org__name`）
- **自定义字段**: `userDefines__xxx` 或使用 T-code（T0002, T0003）
- **表格名**: `module_table_bList`（主表），`_sList`（子表），`_gsList`（孙表），或 `bodyvos`（默认）
- **按钮 ID**: 自动生成（`button31if`）或语义化（`btnSave`, `btnEdit`）

## 代码规范

**禁止使用 `var`**: 统一使用 `const`（首选）和 `let`（仅当变量需要重新赋值时）。所有示例代码、生成代码必须遵守此规范。

**优先使用现代 JS 语法**:
- 箭头函数: `() => {}` 替代 `function() {}`
- 模板字符串: `` `text ${var}` `` 替代字符串拼接
- 对象方法简写: `{ foo() {} }` 替代 `{ foo: function() {} }`

## 注意事项

1. **始终使用空值守卫**注册事件: `viewModel.get('xxx') && viewModel.get('xxx').on(...)`
2. **不要保留 `debugger` 语句**在生产代码中
3. **同步调用**（`{async: false}`）会阻塞 UI，仅在必要时使用
4. **所有 API URL 必须携带 `domainKey` 参数**
5. **脚本无模块化**，所有代码在顶层执行，无 import/export
