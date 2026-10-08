---
name: automotive-debug
description: Android Automotive OS 调试诊断指南
---

# Android Automotive 调试诊断指南

适用场景：AAOS 应用崩溃分析、Template 渲染问题、生命周期异常排查。

## 一、崩溃类型速查

### 1. Template 未正确构建

**症状：** 应用启动后黑屏或显示 "App unavailable"
**常见原因：**
- `onGetTemplate()` 抛出异常
- 返回 null
- 在 `onGetTemplate()` 中做阻塞操作

**排查步骤：**
```
1. 检查 logcat 过滤 "CarApp" 或 "Template"
2. 确认 onGetTemplate() 没有抛出未捕获异常
3. 确认返回的 Template 不为 null
4. 检查 Template Builder 是否调用了 build()
```

### 2. CarAppService 未声明或声明错误

**症状：** 应用无法启动，logcat 显示 "No CarAppService found"
**排查步骤：**
```xml
<!-- 检查 AndroidManifest.xml -->
<service
    android:name=".car.MyCarAppService"
    android:exported="true">
    <intent-filter>
        <action android:name="androidx.car.app.CarAppService" />
    </intent-filter>
</service>
```

### 3. minCarApiLevel 未声明

**症状：** 兼容性错误或应用在某些车机上不显示
**排查步骤：**
```xml
<!-- 检查 AndroidManifest.xml -->
<meta-data
    android:name="androidx.car.app.minCarApiLevel"
    android:value="3" />
```

### 4. 页面栈溢出

**症状：** screenManager.push() 抛出异常或内存持续增长
**排查步骤：**
```
1. 检查是否有循环跳转：A → B → A → B...
2. 检查 LiveData 是否触发了循环更新
3. 确认 pop() 在正确的时机调用
```

## 二、日志调试

### 推荐的 logcat 过滤标签

```bash
# Car App 相关日志
adb logcat -s CarApp:V CarService:V

# 全部 Automotive 相关
adb logcat | grep -i "car\|automotive\|template"

# 应用崩溃日志
adb logcat -s AndroidRuntime:E
```

### 在代码中添加调试日志

```kotlin
class MyScreen(carContext: CarContext) : Screen(carContext) {

    override fun onGetTemplate(): Template {
        Log.d("CarApp", "onGetTemplate called, state: ${viewModel.uiState.value}")
        val template = buildTemplate(viewModel.uiState.value ?: return buildErrorTemplate())
        Log.d("CarApp", "Template built: ${template.javaClass.simpleName}")
        return template
    }
}
```

## 三、车辆属性诊断

```bash
# 查看 Car Service 状态
adb shell dumpsys car_service

# 查看车辆属性列表
adb shell dumpsys car_service --vehicle-properties

# 查看指定属性的当前值
adb shell dumpsys car_service --vehicle-property <property_id>

# 查看 CarPropertyManager 连接状态
adb shell dumpsys car_service | grep -A 10 "CarPropertyService"

# 查看 UX 限制状态
adb shell dumpsys car_service | grep -A 5 "UxRestrictions"
```

## 四、模拟器调试

### 启动 Automotive 模拟器

```bash
# 创建 Automotive 虚拟设备
avdmanager create avd -n "Automotive_API35" \
  -k "system-images;android-35;automotive;x86_64" \
  -d "automotive_1024p_landscape"

# 启动模拟器
emulator -avd "Automotive_API35" -no-snapshot-load
```

### 验证应用是否正确加载

```bash
# 检查 Car App 服务是否注册
adb shell dumpsys activity services | grep CarApp

# 检查应用是否安装
adb shell pm list packages | grep "com.example.carapp"

# 强制启动应用（调试用）
adb shell am start-service -n com.example.carapp/.car.MyCarAppService
```

## 四、常见问题与解决方案

| 问题 | 可能原因 | 解决方案 |
|-----|---------|---------|
| Template 显示空白 | Row/Action 数量超限 | 检查 Section 最大行数限制 |
| 点击无响应 | 未调用 invalidate() | LiveData 更新后调用 invalidate() |
| 应用频繁重连 | Service 异常退出 | 检查 onCreateSession 是否抛异常 |
| 图片不显示 | CarIcon 格式错误 | 使用 CarIcon.create() 包装 |
| 文本截断 | 标题/文本过长 | 标题 < 30 字符，副标题 < 120 字符 |
| 内存持续增长 | 页面未正确销毁 | 检查 screenManager.pop() 调用 |
| 导航后返回状态丢失 | ViewModel 重建 | 使用 SavedStateHandle 保存状态 |

## 五、性能诊断

```bash
# 内存使用
adb shell dumpsys meminfo com.example.carapp

# CPU 使用
adb shell top -n 1 | grep com.example.carapp

# 检查 ANR
adb shell ls /data/anr/

# 检查线程数
adb shell ps -T | grep com.example.carapp
```

## 六、车辆属性常见问题诊断

| 问题 | 诊断命令 | 排查方向 |
|-----|---------|---------|
| 属性读取失败 | `dumpsys car_service --vehicle-properties` | 确认属性ID是否被车机支持 |
| 订阅无回调 | `dumpsys car_service \| grep CarPropertyService` | 检查注册状态和AreaId |
| 写入无效果 | `dumpsys car_service --vehicle-property <id>` | 确认属性是否 read-write |
| SecurityException | 检查 Manifest 权限 | CAR_CONTROL / CAR_SPEED 等 |
| 电量/油量不更新 | 检查车型是否支持 EV/FUEL 属性 | 部分车型不支持 |

## 七、崩溃日志分析模板

收到崩溃日志时，按以下顺序分析：
1. 找到 `FATAL EXCEPTION` 行，确定异常类型
2. 查看异常消息，判断是空指针、越界还是业务异常
3. 追踪堆栈到你自己的代码文件
4. 检查该行前后的变量状态
5. 如果是 Car App 框架内部崩溃，检查 Template 构建参数是否合法
