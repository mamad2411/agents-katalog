---
name: coff0xc-network-protocol-security
description: "Use when / 当用户请求 network/protocol security：TLS、DNS、TCP/UDP、HTTP/2、HTTP/3、QUIC、WiFi、Bluetooth/BLE、RF、packet/pcap/Wireshark、抓包、握手、状态机、secure communication、ProVerif 或 Mermaid protocol。手动触发：使用 coff0xc-network-protocol-security。"
---

# coff0xc-network-protocol-security

<!-- skill-id: cs-nps-2e7f6b41 -->

## 快速规则（日常任务先读这里）
> **[证据先行]** 先定位 pcap、日志、RFC/规范、握手、状态机、字段和异常样本。
> **[协议门禁]** 结论要说明消息序列、字段语义、加密/认证边界、降级/重放/解析风险。
> **[验证闭环]** 给可复查过滤器、字段表、复现条件和防护/检测建议。
> **[硬边界]** 主动探测、无线/RF 操作、第三方网络、生产流量注入和模糊测试先确认。

普通协议/流量分析按本节先推进；只有形式化建模、主动测试或跨系统演练时再展开完整工作流。

## 能力定位
面向网络协议、TLS/DNS/QUIC/HTTP、无线通信、抓包和形式化建模的协议安全分析能力。它把通信证据转成流程图、风险点和验证建议。

## 能交付什么
- 协议流程、握手和状态机说明
- pcap/日志字段分析、异常字段和安全影响
- TLS/PKI/DNS/HTTP/QUIC/无线风险清单
- Mermaid/ProVerif/Tamarin 方向的建模建议

## 可以接收什么输入
- pcap、Wireshark 导出、协议日志、报文字段
- 协议规范、实现代码、握手说明、证书链
- 无线/BLE/RF 捕获摘要或设备通信流程

## 放心使用的边界
- 可做本地抓包和授权通信分析
- 不提供未授权监听、入侵、绕过或干扰第三方网络步骤
- 主动探测、无线发射、生产网络测试必须先确认范围
- 安全类能力默认只用于授权、防御、检测、加固、验证和报告；不提供未授权攻击、凭据窃取、持久化、规避检测、C2、钓鱼收集、数据外传或破坏性步骤。

## 为什么可以放心
- 把报文字段、代码和规范分开标注证据
- 优先说明状态机和信任边界
- 形式化建模只表达可验证协议性质，不夸大结论

## 典型使用方式
```text
使用 coff0xc-network-protocol-security 分析这个 pcap 里的 TLS 握手和异常字段。
使用 coff0xc-network-protocol-security 把这个协议流程画成 Mermaid 并指出安全边界。
Use coff0xc-network-protocol-security to review DNS/QUIC behavior and propose verification checks.
```

## 默认输出
- 收口只写完成、验证、还剩、下一步；有文件/代码/规则产物给路径或位置。
- 未真实运行的检查标为未验证，安全/架构结论标证据等级。

## 按需展开
- 日常任务只执行上面的快速规则、能力边界和典型用法，不默认读取完整门禁。
- 深度架构、复杂多阶段、质量评测、发版、正式交付或当前任务证据不足时，再读取 `references/full-workflow.md`。
- 读取 reference 后仍保持最小必要上下文；不要因为 reference 存在就输出长篇流程或额外自证材料。
