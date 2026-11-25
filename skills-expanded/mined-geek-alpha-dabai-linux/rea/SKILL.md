# REA 逆向工程（rea）

REA（Reverse Engineer Anything，`morluto/rea`，MIT，npm 包 `rea-agents`）把「看懂别人已发布的应用」变成**可核验的 Evidence**：静态重建 Electron/JS 应用的模块图、扒 ASAR、反编译原生 PE/ELF、看 APK/固件/抓包/运行行为。走 MCP，207 个工具，按需连接。

## 0. 本机事实（2026-11-02 实测）

| 项 | 实测值 |
|---|---|
| 主机 | Windows 10 (26300) x64，`rea doctor` 判 `host ok = win32 x64` |
| Node | v24.21.0 / npm 11.19.0 |
| 包版本 | `rea-agents@6.7.0`（npm 最新，MIT） |
| MCP 入口 | `npx -y rea-agents@6.7.0 mcp`（stdio，协议 2024-11-05） |
| MCP 工具数 | 207（`mcp_connect(server="rea")` 实测连上） |
| 注册位置 | `skills/mcp/servers.json` 的 `rea` 条目（已写入） |
| 源码研究副本 | `D:\AI\_study\rea`（git clone，仅参考） |

**已验证能用（零外部依赖）**：
- `analyze_javascript_application` 对 `D:\AI\_study\jsfix`（1 个 js + package.json）秒回，产出 58KB Evidence：artifact sha256、`JavaScriptApplicationGraph` 节点图、`limitations` 声明。
- 静态 JS / Electron / ASAR / web bundle 静态重建，不需要 Ghidra、Java 或任何原生引擎。

**原生二进制已就绪（2026-11-02 装完并实测）**：Ghidra 12.1.4 + Temurin JDK 21.0.12.1，装在 `D:\tools\ghidra_12.1.4_PUBLIC` / `D:\tools\jdk-21`，env 写进 `skills/mcp/servers.json` 的 `rea.env`。
实测 `HOSTNAME.EXE`（40KB）：`analyze` 出 evidence `ev_101bd4…`，image_base `0x140000000`、9 段、86 函数、102 字符串；`decompile --procedure 0x140001300` 出伪代码 `void entry(void){ FUN_140001544(); FUN_140001140(); }`，evidence `ev_330edd…`，provider 明写 `ghidra 12.1.4`。
**还没装**：Hopper / IDA / JADX（→ APK 代码级）、Binwalk/Unblob（→ 固件，只有 Linux 侧）。

**五个实测坑**：
1. `package.json` 的 engines 写 `^22.23.4 || ^24.22.1 || >=26.12.1`，本机 24.21.0 差了 0.1，但 npm 只 warn、`rea doctor` 判 node `healthy`，实际跑得通——**不用先升 Node**。
2. 大目录会超时：对 `D:\AI\dabai\web`（20 个 js + vendor 资源）调 JS 分析，300s 没回来。**先从小目录/单模块起步**，确认通再放大；大目标要拆。
3. 参数名照 schema，不凭 CLI 习惯猜：`analyze_javascript_application` 入参是 `input_path`（不是 `path`），且只接受**目录或 `.asar`**，传单个 `.js` 报 `unsupported_target`；`open_binary` 恰好相反，只认 `path`。
4. `decompile` 传裸地址会被当成 **file offset**，报 `File offset 0x… has no loaded source mapping`；要传**函数入口地址**（先从 `inspect-native-load-image` 的 `entry_points` 或 `analyze` 拿），实测 `--procedure 0x140001300` 才通。`main`、`FUN_140001000` 都不认。
5. `--token-limit/--token-offset` 与结构化输出互斥（直接报 `UNSUPPORTED_OUTPUT_COMBINATION`）；`--filter-output` 过滤到不存在的 key 会吐出空 `{}`。想截断就 `--format md > file` 再读文件。
6. MCP 里原生工具的 `document` 参数不是文件名，是 **`target-<sha256 前 12 位>.EXE`**（Ghidra ephemeral 快照名）：先 `open_binary(path=...)` 拿 sha256，再 `inspect_native_instruction(address=..., document="target-f8b207720d86.EXE")`。传原文件名报 `Unknown Ghidra Program identity`；server 重启后要先重新 `open_binary`，否则 `target_unavailable: No app is open`。

## 1. 怎么用

```
mcp_connect(server="rea")                                  # 拿工具清单（207 个）
mcp_call(server="rea", tool="analyze_javascript_application",
         arguments={"input_path": "D:\\path\\to\\app"})
mcp_disconnect(server="rea")                                # 用完就断
```

失败时 `mcp_connect` 传显式命令（配置丢了也能起）：
`command="npx", args=["-y","rea-agents@6.7.0","mcp"]`

不走 MCP 的 CLI 兜底（同一套分析，直接出 Evidence JSON）：

```bat
npx -y rea-agents@6.7.0 analyze-javascript-application D:\path\to\app --json
npx -y rea-agents@6.7.0 doctor --json
```

## 2. 目标 → 工具路由（先定目标，再挑工具）

| 你要看的东西 | 起手工具 | 前置 |
|---|---|---|
| Electron / JS 应用（解包目录或 `.asar`） | `analyze_javascript_application` | 无 |
| 压缩包/安装包成员清单（ZIP/APK/IPA/MSIX/DMG/PyInstaller） | `open_binary` → `inspect_artifact`（大包先 `detail:"summary"`） | 无（原生前缀要引擎） |
| 原生 PE/ELF/Mach-O 反编译 | `open_binary` → `decompile` / `analyze_function` | **要引擎** |
| Android APK 代码/方法/引用 | `inspect_android_package` | JADX + JDK |
| APK 签名身份/完整性 | `inspect_apk_signature` | 无 |
| 托管 PE/CLI（.NET） | `inspect_managed_artifact` | 无 |
| 固件镜像分区/解包 | `inspect_firmware_regions` / `extract_firmware` | Binwalk/Unblob（Linux） |
| 已保存抓包（HAR/SAZ/qlog/pcap） | `inspect_web_network_capture` / `inspect_pcap_capture` | pcap 要 Wireshark tshark |
| 浏览器页面动作/截图 | `capture_browser_scenario`（Playwright） | 重资源，慎重 |
| Electron 运行时（已开着的 app） | `list_electron_targets` → `inspect_electron_fuses` | 无 |
| WebAssembly | `inspect_wasm_artifact` | WABT 1.0.42 |

完整清单看 `mcp_connect` 返回的工具表，别凭这份表猜参数。

## 3. 装原生分析引擎（只有反编译 exe/dll 才需要）

Windows 上属于 **experimental：只读 P0 边界**，只认 Windows 10+ x64 的本地 NTFS 目标 + 原生 PE（x86/x64/ARMNT/ARM64）。

```powershell
npx -y rea-agents@6.7.0 doctor --json     # 先看缺什么
# 需要：Ghidra 12.1.x（验证过 12.1.4）+ JDK 21+，REA 不会自己装
$env:GHIDRA_INSTALL_DIR = "C:\tools\ghidra_12.1.4_PUBLIC"
$env:JAVA_HOME = "C:\tools\jdk-21"
$env:REA_ANALYSIS_PROVIDER = "ghidra"
npx -y rea-agents@6.7.0 doctor --json     # 复检
```

装完要在 MCP 注册的 `env` 里带上这三个变量（`skills/mcp/servers.json` 的 `rea.env`），否则 server 进程看不到。

## 4. 别做的事

- **别跑 `npx rea-agents setup`**：它只认 claude_code / codex / cursor / vscode / copilot 这些客户端，会去改 `~/.claude.json`、`~/.codex/config.toml` 之类的别人的配置。大白走 `servers.json` 手写注册，不用它的 setup。
- **别把静态图说成运行事实**：Evidence 里的调用关系是静态推断时，`limitations` 会写明「未执行」。汇报结论必须带 `evidence_id` 和限制说明，不能拿「有这条边」当「运行时会调用」。
- 别在单次调用里堆大目录；超时先缩小范围再重试，别原样重发。

## 5. references（按需读，英文原版）

| 文件 | 什么时候读 |
|---|---|
| `references/connection-and-recovery.md` | 连不上/工具消失/超时，按它的阶梯修，别重复 setup |
| `references/evidence-workflows.md` | 怎么写 Evidence、怎么页取、怎么保留 digest |
| `references/javascript-applications.md` | Electron/JS 应用分析的细节与边界 |
| `references/native-and-artifacts.md` | 原生二进制、归档包、NativeAOT |
| `references/runtime-observation.md` | 运行时观测：进程/浏览器/流量/Fiddler |
| `references/android-applications.md` | Android APK、JADX、签名 |
| `references/environments.md` | AgentEnv bundle（把 Web 应用录成可复现环境） |

上游：https://github.com/morluto/rea · https://rea.tools/
