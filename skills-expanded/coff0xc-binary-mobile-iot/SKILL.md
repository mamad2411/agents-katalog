---
name: coff0xc-binary-mobile-iot
description: "Use when / 当用户请求 reverse engineering、PWN、kernel、APK/IPA、Frida、firmware、IoT/ICS/SCADA、PLC/Modbus、UART/JTAG/SPI、BLE/RF、CTF、crypto review、constant-time、设备包或可执行文件分析。手动触发：使用 coff0xc-binary-mobile-iot。"
---

# coff0xc-binary-mobile-iot

<!-- skill-id: cs-bmi-71e4a0cb -->

## 快速规则（日常任务先读这里）
> **[样本先行]** 先记录文件类型、hash、平台、架构、权限、入口点、字符串和运行边界。
> **[证据门禁]** 逆向结论绑定偏移、函数、符号、配置、网络端点、权限或硬件接口证据。
> **[安全执行]** 默认静态/本地隔离分析；动态调试要限定样本、环境和观测项。
> **[硬边界]** 未授权设备、持久化、绕过、真实利用、隐私数据读取和外部通信先确认。

普通二进制/移动/IoT 分析按本节先推进；只有动态 exploit、固件改写或硬件实验时再展开完整工作流。

## 能力定位
面向二进制、移动、IoT/ICS、固件和密码实现的逆向分析能力。它把样本、固件、APK、协议和调试线索转成结构化理解、风险点和验证路线。

## 能交付什么
- 样本/固件结构和入口点分析
- 字符串、配置、权限、通信和硬件接口线索
- 内存安全、加密实现、协议解析或移动风险发现
- 复现环境、工具命令、证据和修复建议

## 可以接收什么输入
- 可执行文件、APK/IPA、固件、pcap、日志、反编译结果
- Ghidra/IDA/Frida 输出、strings、符号、崩溃栈
- 硬件接口说明、UART/JTAG/SPI 线索、ICS 协议文档

## 放心使用的边界
- 可做本地样本、授权设备和实验环境分析
- 不提供未授权利用、持久化、规避检测或真实目标攻击步骤
- 对恶意样本和客户固件避免泄露敏感字符串或密钥
- 安全类能力默认只用于授权、防御、检测、加固、验证和报告；不提供未授权攻击、凭据窃取、持久化、规避检测、C2、钓鱼收集、数据外传或破坏性步骤。

## 为什么可以放心
- 先做静态结构，再决定动态验证
- 区分证据字符串、推断行为和已复现行为
- 输出工具版本、命令和可复现路径

## 典型使用方式
```text
使用 coff0xc-binary-mobile-iot 分析这个 APK 的权限、网络通信和 Frida hook 点。
使用 coff0xc-binary-mobile-iot 检查这个固件里的接口、密钥线索和协议风险。
Use coff0xc-binary-mobile-iot to triage this executable and summarize reverse engineering findings.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
