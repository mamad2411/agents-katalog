---
name: re-flow-recon
description: 逆向侦察流程——对目标程序做静态查壳（DIE/pefile 判壳与架构）、行为侦察（TCPView/Procmon 记录连接与文件写入）、按方法路线总览决策入口路线，产出侦察报告（含目标画像 8 项：版本、架构、语言运行时、壳类型、反调试、反虚拟机、完整性自检、授权模型）。当用户给出 exe 要求"分析、查壳、看它连什么、判断怎么破"，或 re-flow-orchestrator 进入 RECON 阶段时使用。触发词：查壳、侦察、分析程序、路线决策、壳类型、架构判断。
agent_created: true
x-alice-class: reverse
---# 侦察流程（re-flow-recon）

## 单一职责

只做一件事：**摸清目标"是什么、连哪里、存哪、走哪条路线"**，产出侦察报告与路线决策。
不做抓包（属 re-flow-capture）、不做脱壳（属 re-flow-unpack）。

## 触发条件

- 用户给出目标程序要求"分析 / 查壳 / 看它连什么 / 判断怎么破"
- re-flow-orchestrator 进入 RECON 阶段

## 输入与输出

- **输入**：目标 exe / 安装包路径（必填）；可选：可疑网络目标、授权码样本
- **输出**：侦察报告（任务目录 `report-recon.md`）——壳类型与版本、程序架构、网络行为、授权存储位置、推荐路线；并给出状态流转标记 `RECON → CAPTURE | UNPACK | ALGORITHM`

## 目标画像采集清单（必填 8 项）

侦察阶段必须逐项填；填不出的写"未确认"并注明原因——任一项缺失都会导致下游选错工具或走错路线。

| # | 采集项 | 采集方法 | 填不出时的默认假设与风险 |
|---|---|---|---|
| 1 | 程序版本与构建号 | 文件属性 Details / 资源 VERSIONINFO / 关于界面 | 补丁偏移与 hook 地址全部绑定版本，换版即失效 |
| 2 | CPU 架构 | DIE / pefile 读 Machine 字段（0x8664=x64、0x14c=x86、0xAA64=ARM64） | 默认 x64；选错位数 → 调试器挂不上、调用约定解析全错 |
| 3 | 编译语言与运行时 | BSJB / `.CLR_UEF` / coreclr.dll 特征、Go buildinfo、asar、PYZ | 见下表"多语言分支"；判错 = 在无效汇编上白耗 |
| 4 | 壳与混淆类型 | DIE 签名库 / pefile 节区名 / overlay 高熵 | 见下表"多壳分支"；漏判 Themida/WinLicense 会让 Scylla 直接失败 |
| 5 | 反调试手段 | 静态看导入表（IsDebuggerPresent / NtQueryInformationProcess）；动态挂一次看是否秒退 | 默认"有"，ScyllaHide 全选项开启 |
| 6 | 反虚拟机 / 反沙箱 | 在 VM 里跑一次，观察是否拒绝运行或行为异常 | 未确认 → 交 re-env-sandbox 处理，**否则 VM 里的结论不可信** |
| 7 | 完整性自检 | 改一个无关字节后看是否报错/自毁；查是否有 CRC 或签名校验 | 默认"有自检" → 优先 hook 而非 patch |
| 8 | 授权模型 | 离线本机码 / 在线激活 / 服务器验签 / 时间限制 / 硬件指纹 | 离线非对称验签 = 放弃伪造，转运行时绕过 |

## 多语言与多壳分支

**语言 / 运行时**

| 判据 | 语言 / 运行时 | 首选工具 | 备注 |
|---|---|---|---|
| 有 BSJB 元数据、依赖 mscorlib | .NET Framework | dnSpy / ILSpy | 混淆需先 de4dot / ConfuserEx 反混淆 |
| 单文件 bundle + 有 coreclr.dll | .NET 单文件 | 提取 bundle → 回 dnSpy | 可还原 IL |
| 单文件 bundle + 无 coreclr.dll | NativeAOT | IDA/Ghidra + 运行时分析 | **无 IL 可看，只能走运行时** |
| 无 BSJB、大量 VCL 类名、DFM 资源 | Delphi | IDR / DeDe | 事件表定位 OnClick |
| 函数名带包名、大字符串表 | Go | IDA + go_parser（符号恢复） | strip 后先恢复符号 |
| `resources/app.asar` | Electron | asar 解包 | 直接看 JS |
| PYZ / pyi 结构 | PyInstaller | pyi-archive_viewer + pyc 反编译 | 基本无保护 |
| 以上皆非 | 原生 C/C++ | IDA / Ghidra | 优先 API 断点缩小范围 |

**壳 / 混淆**

| 壳 / 混淆 | 判据 | 路线 | 关键工具 |
|---|---|---|---|
| 无壳 | 节区正常、字符串明文 | 直接静态分析 | — |
| UPX | 节区 UPX0/UPX1 | `upx -d` 一键脱 | upx |
| MPRESS | 节区 `.MPRESS1/2` | 运行时自解压，取 `%TEMP%\~*` 真身 | x64dbg / Procmon |
| VMP（VMProtect） | DIE 报 VMProtect、代码段高熵、虚拟化跳转表 | dump 非虚拟化主体 + 关键函数在 API 边界 hook（虚拟化不可还原） | Scylla + ScyllaHide，详见 windows-license-crack `references/vmprotect.md` |
| Themida / WinLicense | DIE 报对应签名 | 需内核级隐藏 + 大量手工 IAT 修复，成本极高 | TitanHide / HyperHide + Scylla；**建议直接转运行时路线** |
| Obsidium / Enigma / ASProtect | DIE 报对应签名 | 需专用脱壳脚本，否则转运行时 | Scylla 通常无效 |
| .NET 混淆（ConfuserEx / .NET Reactor） | 方法体异常、类名乱码 | 反混淆后回 dnSpy | de4dot 等；**Scylla 对 .NET 完全无效** |

## 执行步骤

1. **静态查壳**：DIE（图形）或 pefile（脚本读节区名、overlay、entrypoint）→ 判定 UPX / MPRESS / VMP / 无壳
2. **架构判定**：查 BSJB / `.CLR_UEF` 节 / coreclr.dll 特征 → 原生 C++、.NET Framework、.NET 单文件 bundle、NativeAOT
3. **行为侦察**：运行程序，TCPView 记录连接的域名/IP/端口，Procmon 记录文件与注册表写入（授权信息常存在此处）
4. **路线决策**：按 windows-license-crack「方法路线总览」四路线表选入口

| 侦察结果 | 推荐路线 |
|---|---|
| 无壳、字符串明文 | 路线一 静态逆向 |
| 压缩壳（UPX/MPRESS） | 路线二 脱壳后回静态 |
| 单文件 bundle / NativeAOT | 路线二或运行时 |
| VMP 虚拟化 / 字符串加密 | 运行时绕过（API 边界 hook） |
| 存在联网验证 | 叠加 re-flow-capture |

5. **归档**：报告写入任务目录，供后续阶段与 orchestrator 的 state.md 引用

## 边界与上下游

- **前置**：re-tool-manifest 环境自检（DIE、pefile、Procmon/TCPView 就位）；re-env-sandbox 提供隔离环境与快照
- **后继**：re-flow-capture（有网络验证）/ re-flow-unpack（有壳）/ re-flow-analyze（定位、追踪、补丁与验证）/ 直接进入 BYPASS（无壳简单场景）
- **决策依据**：windows-license-crack 的方法路线总览与「关键判断依据速查表」
- **产出契约**：`report-recon.md` 必须包含上述 8 项画像字段（键名固定），供 re-flow-analyze 与 orchestrator 的 `state.md` 直接消费
