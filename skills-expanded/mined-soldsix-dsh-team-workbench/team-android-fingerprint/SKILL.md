---
name: team-android-fingerprint
description: Android 设备指纹 SDK 逆向。用于 AAR/APK/DEX/SO 的 Java/Kotlin/JNI 采集链、系统标识、安装身份、缓存、权限、加密上报和设备注册分析。
user-invocable: true
disable-model-invocation: false
metadata:
  language: zh-CN
  version: '1.0'
---

# Android 设备指纹 SDK

先按本任务已确认的目标和范围确定 Android 成果；只有需要规划跨平台整体链路时才补读 [设备指纹总流程](../team-device-fingerprint/SKILL.md)。记录包名、签名、版本、目标 SDK、ABI、Android 版本、设备/模拟器类型与测试账号；保留 APK 分包、AAR、DEX 和 SO 的来源及摘要。

## 静态定位

用已安装的 JADX/反汇编器识别 SDK 初始化、组件注册、权限、远程配置、采集器和上传调用。混淆后的包名只是线索；结合资源、字符串、依赖、调用图与动态加载归属确认模块。反编译失败时查看 DEX 指令，不能把伪代码错误当作实际逻辑。

跨 Java/Kotlin、JNI、原生库逐段跟踪采集到序列化的参数。标注动态 JNI 注册、线程切换、回调、模块加载及地址偏移；原生逻辑成为独立分析问题时补读 [二进制分析](../team-native-reverse/SKILL.md)。加固导致目标代码不可读时，再按需使用 [移动端脱壳](../team-mobile-unpacking/SKILL.md) 建立可分析副本。

## 动态验证

使用受控应用和明确设备，先采基线，再观察关键 API 或函数的输入、输出、调用栈与触发条件。记录权限拒绝、API 不存在、异常、离线和超时的结果。探测是否调用某 API 与确认其值参与最终指纹是两项不同结论。

字段重点包括安装生成值、应用/开发者作用域标识、系统与硬件特征、传感器、网络环境、存储缓存、应用完整性相关输出；以实际观测为准。Android 平台对标识符和权限的限制随版本与应用身份变化，按 [官方标识符文档](https://developer.android.com/identity/user-data-ids) 核对，不承诺任意应用能读取永久硬件 ID。

设计清理应用数据、卸载重装、应用升级、签名变化、同型号设备、系统升级、不同用户/工作资料、权限撤回的对照。分别解释应用安装、账号与设备生命周期；完整性证明结果不自动等于稳定设备 ID。

## 成果与验收

提交 Java/JNI/SO 调用图、字段字典、缓存位置与生命周期、触发时序、序列化/加密边界及复现向量。至少验证一个正常和一个受限环境。测试中使用本地账号和数据；原始设备标识保存在项目受控证据中，通用专家记忆只保留方法。

复核者能用指定应用构建与设备重现关键字段来源，并说明哪些结论依赖 Android 版本、签名或服务端。注册接口分析衔接 [注册协议](../team-registration-protocol/SKILL.md)。
