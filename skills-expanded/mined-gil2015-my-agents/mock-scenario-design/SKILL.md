---
name: mock-scenario-design
description: Use when frontend UI, API integration, or tests need MSW mock data, parameterized mock behavior, or business scenario simulation
---

# Mock Scenario Design

## 场景

- 成功返回。
- 空数据。
- 错误码。
- 登录或权限失败。
- 参数差异返回。
- 业务状态切换。

## 阶段

- UI 阶段：服务页面可运行。
- 联调阶段：对齐真实接口契约。
- 测试阶段：覆盖边界和回归场景。

## 规则

接口文档存在后，mock 必须镜像接口字段、响应包装、可空性和错误码。
