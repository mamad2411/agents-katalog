---
name: re-tool-registry
description: 逆向工程工具注册表——维护全部逆向/破解工具的下载元数据，负责下载任务的"发起"：按工具名、路线或最小启动集生成下载任务清单（官方源、GitHub repo、asset 匹配模式、安装类型、目标路径）。当用户要求安装或下载逆向工具、搭建逆向环境，或 re-flow-orchestrator 进入环境准备阶段、re-tool-downloader 需要源信息时使用。触发词：装工具、下载工具、工具目录、下载清单、搭逆向环境、工具源。只生成清单，不执行下载、不维护 MANIFEST。
agent_created: true
x-alice-class: reverse
---# 逆向工具注册表（re-tool-registry）

## 单一职责

只做一件事：**把"要装什么"翻译成"从哪下、怎么放"**——维护工具下载元数据目录并生成下载任务清单。
不执行下载（属 re-tool-downloader），不记录状态（属 re-tool-manifest）。

## 触发条件

- 用户："装上 Ghidra / 把逆向工具都装上 / 搭逆向环境 / 这个工具从哪下"
- re-flow-orchestrator 进入 ENV 阶段需要准备清单
- re-tool-downloader 接到单个工具任务，先查源信息

## 输入与输出

| 输入 | 说明 |
|---|---|
| 工具名 | 单个，如 `Ghidra` |
| 路线名 | 路线一~四对应的一组工具 |
| `最小启动集` | 覆盖 90% 场景的 7 件套（默认） |
| 空 | 返回全部目录 |

**输出**：下载任务清单（交 re-tool-downloader），每项字段：
`name` / `source` 官方源 / `asset_pattern` 下载包匹配正则 / `type` 安装类型 / `dest` 落地路径 / `note` 备注

## 工具目录（下载元数据的权威源）

### A. 环境底座（type=pip）

| name | 安装命令 | 备注 |
|---|---|---|
| pefile | `pip install pefile` | PE 头/节区/overlay 解析 |
| capstone | `pip install capstone` | 反汇编引擎 |
| frida-tools | `pip install frida-tools` | 动态插桩，下载慢，优先排队 |

### B. 绿色解压（type=green，dest=`C:\tools\<name>\`）

| name | source（GitHub repo） | asset_pattern | 备注 |
|---|---|---|---|
| ghidra | NationalSecurityAgency/ghidra | `^ghidra_.*_PUBLIC_.*\.zip$` | 反编译；依赖 JDK 21 |
| dnspy | dnSpyEx/dnSpy | `^dnSpy-net-win64\.zip$` | .NET 反编译，可改 IL |
| x64dbg | x64dbg/x64dbg | `^x64dbg_snapshot.*\.zip$` | 解压取 `release\x64\x64dbg.exe` |
| die | horsicq/DIE | `^die_win64_portable_.*\.zip$` | Detect It Easy 查壳 |
| upx | upx/upx | `^upx-.*-win64\.zip$` | 脱 UPX 壳 |
| scylla | NtQuery/Scylla | `Scylla.*x64\.zip` | dump + IAT 修复 |
| systeminformer | winsiderss/systeminformer | `^systeminformer-.*-bin\.zip$` | Process Hacker 继任者 |
| cyberchef | gchq/CyberChef | `^CyberChef_v.*\.zip$` | 网页版可免装 |
| jdk21 | adoptium/temurin21-binaries | `OpenJDK21U-jdk_x64_windows_hotspot_.*\.zip$` | Ghidra 前置依赖 |

### C. 安装向导类（type=installer）

| name | source | 静默参数参考 | 备注 |
|---|---|---|---|
| wireshark | wireshark.org/download | `/S /NoDesktopShortcut` | Npcap 已装时跳过其组件 |
| fiddler | telerik.com/fiddler/fiddler-classic | 常规向导 | HTTPS 解密代理 |
| proxifier | proxifier.com/download | `/S` | 强制直连程序走代理，试用版 |
| cheatengine | cheatengine.org/downloads | 常规向导 | 内存搜索 |
| apimonitor | rohitab.com/apimonitor | zip 直链（实为 green） | API 调用观测 |

### D. 最小启动集（默认返回）

pefile、capstone、frida-tools、ghidra、jdk21、dnspy、x64dbg、die —— Ghidra 无 JDK 跑不起来，二者绑定。

### E. 路线 → 工具分组

| 路线 | 工具 |
|---|---|
| 一 静态逆向 | ghidra、jdk21、dnspy、die |
| 二 脱壳解包 | upx、x64dbg、scylla（配 ScyllaHide 插件） |
| 三 算法推导 | cyberchef（哈希验证用 Python 标准库） |
| 四 运行时绕过 | frida-tools、systeminformer、apimonitor |

## 边界与上下游

- **上游**：re-flow-orchestrator（ENV 阶段）
- **下游**：re-tool-downloader（消费清单）
- **平行**：re-tool-manifest（登记结果）
- **相关**：windows-license-crack 的 `references/toolbox.md` 讲"每条路线用什么工具"，本表讲"每个工具从哪下"——**下载元数据以本 skill 为唯一权威源**，避免两处漂移
