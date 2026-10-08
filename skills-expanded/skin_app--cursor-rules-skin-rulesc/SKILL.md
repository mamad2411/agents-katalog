---
description: 
alwaysApply: true
---

# 售后系统项目规范 (Project Rules)

## 1. 架构与目录规范 (Feature-first)
- **目录结构**：严格按功能模块划分（如 `features/work_order`, `features/device_pairing`）。
- **分层要求**：每个 feature 下分为 `ui` (widgets/screens), `provider` (状态), `repository` (数据接口), `model` (数据模型)。
- **禁止跨层引用**：UI 层严禁直接调用 API，必须通过 Repository -> Provider -> UI 的路径。

## 2. 状态管理 (Riverpod 3.x)
- **代码生成**：强制使用 `riverpod_generator`。所有 Provider 必须通过 `@riverpod` 注解生成。
- **Widget 类型**：所有需要访问状态的 Widget 必须继承自 `ConsumerWidget` 或 `ConsumerStatefulWidget`。
- **异步处理**：网络请求必须使用 `AsyncValue` 进行处理，并在 UI 端通过 `.when()` 或 `.maybeWhen()` 显式处理加载中和错误状态。

## 3. 路由规范 (GoRouter)
- **声明式导航**：禁止使用 `Navigator.push`，统一使用 `context.go()` 或 `context.push()`。
- **路由定义**：所有路由路径常量化（如 `AppRoutes.orderDetail`），参数传递通过 `pathParameters` 或 `extra` 实现。
- **守卫机制**：权限校验（如登录态、售后人员身份）应在 GoRouter 的 `redirect` 逻辑中统一处理。

## 4. 蓝牙与权限流 (Bluetooth & Permissions)
- **权限先行**：在调用任何 `flutter_blue_plus` 接口前，必须通过 `permission_handler` 检查并申请蓝牙、定位（Android 12 以下）或周边设备权限（Android 12+）。
- **连接管理**：蓝牙连接状态必须通过 `StreamProvider` 暴露给全局，确保 UI 能实时反馈设备断开或连接。
- **异常处理**：针对蓝牙未开启、扫描超时、连接断开等场景，必须提供明确的 Toast 或弹窗提示用户。

## 5. 代码质量与 UI
- **常量化**：所有的 API Endpoint、颜色值、字体大小、固定间距必须引用 `core/theme` 或 `core/constants`。
- **国际化**：售后系统中所有的 UI 文字（工单状态、报错信息）必须通过 `l10n` 处理。
