---
name: app-ui-launch-zh
description: Maintain App launch configs (package, activity). Demo: Android Settings.
---

# App 启动配置

路径：`specs/app/launches/` 或 `examples/app/launches/`

## Demo

```json
{
  "名称": "Android Settings",
  "包名": "com.android.settings",
  "启动Activity": "com.android.settings/.Settings"
}
```

业务 spec 引用：

```json
"启动配置": "@examples/app/launches/android-settings.json"
```

注册表：`launches/registry.json`（可选）
