---
name: team-android-toolchain
description: 在 Windows DSH 环境中发现并验证 ADB、scrcpy、Frida、mitmproxy、jadx 与 apktool，连接真机或模拟器并检查版本与证据；需要 Android 工具链时加载。
user-invocable: true
disable-model-invocation: false
metadata:
  language: zh-CN
  version: '1.0'
---

# Android 工具链与设备接入

先读取当前任务的设备与应用范围，再从 DSH 实际运行环境发现工具。优先读取部署者提供的工具清单或项目配置；没有清单时，用 PowerShell 的 `Get-Command adb,scrcpy,frida,mitmdump,jadx,apktool -ErrorAction SilentlyContinue` 查看可执行入口，并核对安装目录、版本和来源。若存在多个 ADB，选择一条已验证的路径，并在本次任务中固定使用；不要假设系统目录中的同名程序较新。缺少工具时记录缺口和安装要求，不猜测绝对路径，也不改全局 PATH。

PowerShell 使用 `& '已核实的完整路径' 参数`，工作目录和输出目录由任务明确指定；不要把 Bash、cmd 语法拼进 PowerShell 字符串。版本清单作为当前任务证据保存，跨机器和跨会话重新核对。

## 接入顺序

1. 使用已核实的 ADB 完整路径执行 `devices -l`，记录实际序列号与状态；在看到在线设备前，不声称抓包、Hook 或真实设备测试已通过。
2. 真机先确认 USB 调试与设备屏幕授权；模拟器先确认实例在运行。多个设备出现时每条 ADB 命令都使用 `-s <实际序列号>`，避免误操作其他设备。`offline` 或 `unauthorized` 是连接状态问题，先诊断，不重复重启守护进程。
3. 读取 ABI、Android 版本、目标包名和进程状态，再选择与设备 ABI 和 Frida CLI 主版本兼容的设备端组件。记录设备端版本；未部署或未启动时标为“缺口”，不要猜测已可用。
4. 抓包先固定测试设备、应用版本、代理端口和基线请求。证书信任及网络设置的变更要记录、可恢复；失败时区分未走代理、证书校验、应用私有网络栈和服务端拒绝。
5. 静态分析用 jadx/apktool 对固定哈希的样本进行，产物写入本任务私有目录。运行时观测只选能区分当前假设的窄点，保存调用时间、线程和输入版本。

## 验收与恢复

工具检查通过、设备在线、应用流量可观察、目标观测点触发是四个不同状态；分别展示证据。设备拔出、模拟器重启、ADB 端口占用、Frida 版本不配、代理证书问题出现时保存检查点，释放设备占用，修复后续接同一任务。团队中同一设备和同一代理端口只交给一名当前负责人。
