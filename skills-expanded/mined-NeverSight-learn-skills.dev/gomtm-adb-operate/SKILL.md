---
name: gomtm-adb-operate
description: 自动化操作android设备, 使用 adb 正确高效地操作android设备.
---

## 基本原则

### 能直接通过命令完成的就不要通过屏幕点击完成

- 启动后台服务或者前台服务
  ❌ BAD: 点击SomeApp的屏幕或者SomeActivity找到"启动服务"按钮点击, 看到新的授权或者其他相关界面继续点击直到完成服务启动
  description: 由于设备和厂商不同,界面可能不一致; 设备当前屏幕可能不是你认为的相关屏幕; 实际打开的应用可能不是你预想的应用;
  ✅ GOOD: 使用`adb shell am start-foreground-service -n com.example.app/.MyService`

- 启动某应用的某Activity
  ❌ BAD: 通过点击动作按钮,点击屏幕,点击链接等方式打开
  ✅ GOOD: 使用`adb shell am start -n com.example.app/.MyActivity`

