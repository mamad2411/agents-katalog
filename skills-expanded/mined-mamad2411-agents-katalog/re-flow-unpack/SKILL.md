---
name: re-flow-unpack
description: 脱壳流程——编排加壳程序的 dump 落地：ScyllaHide 反调试对抗、API 断点法定位 OEP、Scylla dump 内存、IAT 搜索重建与 Fix Dump；VMP 虚拟化壳按"dump 非虚拟化主体 + 关键函数转 API 边界 hook"的务实路线执行。当用户要求"脱壳、dump、找 OEP、修复 IAT"，或 re-flow-orchestrator 进入 UNPACK 阶段时使用。触发词：脱壳、dump、OEP、IAT、Scylla、x64dbg、VMP、VMProtect、加壳。
agent_created: true
x-alice-class: reverse
---# 脱壳流程（re-flow-unpack）

## 单一职责

只做一件事：**把加壳程序变成可静态分析的主体**（dump + 修复），产出 dump PE 与修复报告。
不做抓包（属 re-flow-capture）、不做绕过（属 windows-license-crack 主流程）。

## 触发条件

- 用户："脱壳 / dump 出来 / 找 OEP / IAT 修复"
- re-flow-orchestrator 进入 UNPACK 阶段
- re-flow-recon 判定目标有壳

## 输入与输出

- **输入**：目标 exe 路径 + 壳类型（recon 结论）
- **输出**：dump 出的 PE 文件 + 修复报告（IAT 恢复率、PE 头状态、未恢复项清单）；状态流转标记 `UNPACK → BYPASS | 静态分析`

## 执行步骤

1. **反调试对抗先行**：x64dbg 附加前装好 ScyllaHide 并全选项开启（PEB BeingDebugged、NtGlobalFlag、DR 寄存器、rdtsc 时间差、CheckRemoteDebuggerPresent）
2. **定位 OEP**：
   - API 断点法：对 `GetModuleHandleW` / `GetCommandLineW` 下断（初始化必调），返回地址附近即真实入口
   - 区段执行法：程序运行后 RIP 首次落入原始代码节（.text）处
   - VMP 入口是 VM stub，初始大段是虚拟机初始化——不要单步硬跟
3. **Dump**：Scylla 附加目标进程 → Dump 保存内存镜像
4. **IAT 重建**：IAT Autosearch + Get Imports；VMP 新版部分调用走 VM 内部 stub，搜不全是常态，记录残留
5. **Fix Dump**：修复导出为可打开 PE；PE 头被抹（EraseHeader）时用 Scylla 重建
6. **归档**：dump 文件与修复报告写入任务目录 `dump/`

## 关键技术要点

- 压缩壳（UPX / MPRESS）：脱壳后回静态路线，IAT 通常可完整恢复
- VMP 虚拟化壳：**虚拟化函数无法还原**——dump 后只静态分析非虚拟化部分，关键验证逻辑转 API 边界 hook
- 改内存触发 CRC 自校验导致自杀时，不改代码段，改用返回值 hook

## 边界与上下游

- **前置**：re-flow-recon（壳类型）；re-tool-manifest（x64dbg / Scylla / ScyllaHide 就位，缺失走下载链）
- **后继**：BYPASS 阶段（windows-license-crack 第 4-7 步）；dump 结果反哺算法推导
- **深度参考**：windows-license-crack 的 `references/vmprotect.md`
