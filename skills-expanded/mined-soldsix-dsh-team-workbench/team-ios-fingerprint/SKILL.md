---
name: team-ios-fingerprint
description: iOS 设备指纹 SDK 逆向。用于 framework/xcframework/IPA/Mach-O 的 Objective-C/Swift 采集链、标识与缓存生命周期、DeviceCheck/App Attest 接口及注册上报分析。
user-invocable: true
disable-model-invocation: false
metadata:
  language: zh-CN
  version: '1.0'
---

# iOS 设备指纹 SDK

先按本任务已确认的目标和范围确定 iOS 成果；只有需要规划跨平台整体链路时才补读 [设备指纹总流程](../team-device-fingerprint/SKILL.md)。盘点可获得的源码、调试构建、符号、framework/xcframework 或应用包，以及 macOS/Xcode、设备与调试权限。当前主机无法执行 iOS 动态实验时先做静态工作，明确依赖，不把模拟器结果写成真机结论。

## 定位与观测

1. 保存应用与各架构 slice 的摘要、Bundle ID、签名/entitlements、系统版本、SDK 构建与测试环境。对应用包加密和 SDK 自身混淆分别识别。
2. 找出模块加载、初始化、Objective-C selector、Swift 桥接、C/C++ 函数及异步回调。符号缺失时结合交叉引用与运行地址，保留模块相对偏移及 ASLR 基准。
3. 跟踪平台接口、生成的安装标识、Keychain/偏好/文件缓存、设备环境、编码和网络封装。记录值的可用前提及权限，而不是根据接口名推测实际上传内容。
4. 在允许调试的构建中用 LLDB 或现有观测工具验证关键参数和返回。观察前后分别保留基线；区分注入造成的差异、真机/模拟器差异与 SDK 自身判断。
5. 对首次启动、重启、升级、重装、权限拒绝、账号变化和网络失败做对照。不要假定 Keychain、应用目录或供应商作用域标识具有相同清除行为，按实际应用环境验证。

## 证明与服务端

若样本使用 DeviceCheck 或 App Attest，依据 [Apple DeviceCheck 文档](https://developer.apple.com/documentation/devicecheck) 分开记录客户端调用、挑战/返回处理和服务端校验。接口支持、证明验证与设备身份映射是不同问题；服务端不可见时不宣称已恢复服务端决策。

注册和挑战、Swift/原生逻辑或应用可读性成为独立缺口时，分别补读 [注册协议](../team-registration-protocol/SKILL.md)、[二进制分析](../team-native-reverse/SKILL.md) 或 [移动端脱壳](../team-mobile-unpacking/SKILL.md)；优先匹配版本的授权调试产物。

## 验收

交付模块归属、调用链、字段来源/作用范围/缓存表、关键输入输出及平台依赖。每个动态结论说明设备、构建与工具版本；静态推测单列。未获得真机或服务端条件时仍交付已完成的可复核部分，并列出精确补测项。
