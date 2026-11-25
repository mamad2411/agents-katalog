---
name: playwright-ui-form-fill-zh
description: Web 表单识别与填写参考。触发词：新增表单、编辑表单、下拉、上传、必填、el-select、layui、cascader、填表。由 spec-gen / heal / orchestrator 引用，不单独执行浏览器。
disable-model-invocation: true
---

# Web 表单填写参考

本 Skill **不执行浏览器**，只提供生成与 heal 表单步骤时的共享规范。

## 何时阅读

| 场景 | 阅读 |
|------|------|
| 生成「新增/编辑」步骤 | [form-controls-zh.md](reference/form-controls-zh.md) |
| 提交前自检 | [form-fill-checklist.md](reference/form-fill-checklist.md) |
| 找范例脚本 | [script-index.md](reference/script-index.md) |

## 铁律

1. **弹窗表单**必须在 `.el-dialog` / layer / drawer 内按 label 定位，禁止用全页 placeholder 或列表筛选区。
2. **`.el-select` / layui 下拉 / `.el-cascader`** 不得用 `page.selectOption` 或原生 `<select>` 假设。
3. **提交前**在表单容器内审计必填项（`*` / `lay-verify` / 「请选择」占位）。

## 调用方

- **playwright-ui-spec-gen-zh** — 生成 `执行代码` 填表步骤
- **playwright-ui-heal-zh** — 表单未提交、字段未填、选错控件时分诊
- **playwright-ui-orchestrator-zh** — 复杂表单用例注明走本 reference
