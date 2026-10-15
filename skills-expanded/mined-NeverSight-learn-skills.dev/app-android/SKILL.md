---
name: app-android
description: "Flutter Android 平台约束：JPush 推送、版本更新、权限配置、Platform Channel、多渠道包与发布构建。"
---

# app-android

Android-specific constraints for Flutter projects.

---

## Push Notifications (JPush 极光)

- 使用 `jpush_flutter` 插件直接集成
- `android/app/build.gradle` 配置 `manifestPlaceholders`：
  ```groovy
  manifestPlaceholders = [
    JPUSH_PKGNAME: applicationId,
    JPUSH_APPKEY : "your_appkey",
    JPUSH_CHANNEL: "developer-default"
  ]
  ```
- JPush 初始化在 `android/app/src/main/.../MainApplication.kt` 的 `onCreate()`
- Registration ID 每次启动上报后端
- 消息接收：通过 `jpush_flutter` 的 `addEventHandler` 在 Dart 层处理
- Android 8+ 需创建 `NotificationChannel` 才能显示通知

---

## Version Update

- 使用 `package_info_plus` 获取当前版本：
  ```dart
  final info = await PackageInfo.fromPlatform();
  // info.version → versionName，info.buildNumber → versionCode
  ```
- 多渠道包跳转对应应用市场 URL（通过 flavor 注入）
- 强制更新：阻断 UI（`PopScope` 拦截返回），无法关闭
- 软更新：可关闭 Dialog

---

## Widget 结构规范（Green Frame）

Flutter 文件内按以下顺序组织（与 CLAUDE.md 通用规范一致）：

1. import（`dart:` → `package:` → 相对路径，各组空一行）
2. 文件顶层常量
3. Widget 类
   - State 变量（`lowerCamelCase`）
   - `initState()` / `dispose()`
   - `handleXxx` 事件方法
   - `buildXxx` 辅助构建方法
   - `build()`

**Platform Channel（仅需调用原生功能时使用）：**
- Kotlin 桥接代码放 `android/app/src/main/kotlin/.../channels/`
- Channel 命名格式：`com.yourapp.module/feature`
- 每个 Channel 对应独立 Kotlin 文件，在 `MainActivity.kt` 中注册

---

## Module / Asset Organization

**Flutter 层（业务代码）：**

`lib/modules/` 按功能组织，见 CLAUDE.md 目录规范。

**Android 原生层（仅桥接 + 第三方 SDK 初始化）：**

```
android/app/src/main/kotlin/.../
├── MainActivity.kt        # MethodChannel 注册
├── MainApplication.kt     # JPush、第三方 SDK 初始化
└── channels/              # 自定义 Channel Kotlin 实现
```

共享 UI 组件 → 使用 Flutter 通用 Widget（无需 Android Library Module）

---

## Permissions

使用 `permission_handler` 包统一处理，封装在 `common/permissions/`（见 CLAUDE.md）：

```dart
final status = await Permission.camera.request();
// 处理三态：granted / denied / permanentlyDenied（引导去系统设置页）
```

`AndroidManifest.xml` 中必须声明（`permission_handler` 文档要求）：

```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.RECORD_AUDIO"/>
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
```

- 模块层禁止直接调用 `permission_handler`，必须经由 `common/permissions/` 封装

---

## Android 配置 (`android/app/build.gradle`)

```groovy
android {
    compileSdk 34
    defaultConfig {
        minSdk 21          // Flutter 最低要求
        targetSdk 34
    }
}
```

- 开发构建可在 `AndroidManifest.xml` 开启 `android:usesCleartextTraffic="true"`，Release 必须关闭
- 多渠道：使用 Flutter `--flavor` 参数，对应 Gradle `productFlavors`；每个 flavor 可注入不同 `manifestPlaceholders`（市场 URL、JPush AppKey 等）

---

## Build & Release

- 开发：`flutter run`
- APK（直接分发）：`flutter build apk --release --flavor <channel>`
- AAB（应用市场）：`flutter build appbundle --release --flavor <channel>`
- 版本管理统一在 `pubspec.yaml`：
  ```yaml
  version: 1.0.0+1   # versionName+versionCode，+后数字每次 Release 必须递增
  ```
- 签名：在 `android/key.properties` 配置（**不提交 git**），`build.gradle` 引用该文件
- 禁止提交 keystore 文件或密码到 git
