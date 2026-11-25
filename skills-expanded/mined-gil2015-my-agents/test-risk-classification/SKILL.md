---
name: test-risk-classification
description: Use when deciding whether frontend requirements need new automated tests, manual verification, regression checks, or bug documentation
---

# Test Risk Classification

## 必须补自动化测试

- 核心业务计算/状态流。
- 表单校验/提交。
- 权限、登录、错误码。
- 数据转换和接口适配。
- 历史 bug 回归。
- 多步骤交互流程。

## 可手动验证

- 纯文案。
- 简单样式调整。
- 无分支只读展示。

## 输出

- `test-plan.md`
- `test-report.md`
- `bug.md`
