---
name: mcp-lsp-project-config
description: 配置、安装、检查、修复或迁移项目级 mcp-lsp stdio MCP，覆盖 Codex、Claude Code 和 Google Antigravity，以及 Windows 原生、WSL 原生和 Windows 宿主通过 wsl.exe 桥接 Linux sidecar 的自动选型。用户提到项目 MCP、LSP MCP、.codex/config.toml、.mcp.json、.agents/mcp_config.json、工具已显示但调用报 client is closing、EOF、Transport closed，或希望三个客户端共用仓库内 mcp-lsp 时使用。
description: 配置、安装、检查、修复或迁移项目级 mcp-lsp stdio MCP，覆盖 Codex、Claude Code 和 Google Antigravity，以及 Windows 原生、WSL 原生和 Windows 宿主通过 wsl.exe 桥接 Linux sidecar 的自动选型。用户提到项目 MCP、LSP MCP、.codex/config.toml、.mcp.json、.agents/mcp_config.json、Codex 中 LSP 工具有时直接暴露有时只在延迟工具目录、ALL_TOOLS 过滤为空、工具已显示但调用报 client is closing、EOF、Transport closed，或希望三个客户端共用仓库内 mcp-lsp 时使用。
---

# 项目级 mcp-lsp 配置

根据目标项目、当前主机和已安装客户端的真实状态，选择 bin/LSP 中正确的 mcp-lsp，并精确合并项目级配置。不要写用户级或全局配置。

本技能提供判断方法和配置契约，不提供固定生成脚本。Agent 必须自行检查和编辑；不得为了单次配置默认创建新的生成器、wrapper 或安装脚本，除非用户明确要求。

## 读取顺序

1. 完整读取本技能。
2. 读取 references/provider-configs.md，掌握三家项目级文件、字段差异和刷新方式。
3. 确认项目根、Git 状态、已有配置、将启动 MCP 的客户端运行环境、当前操作系统和 CPU；Windows 必须区分原生进程与 WSL 进程。
4. 解析项目根及其上一级目录，按“确认可信 cwd 与 workspace root”向用户提问并等待明确选择；未确认不得写配置。
5. 检查目标客户端当前版本、CLI help 或官方文档。已有参考与当前客户端冲突时，以当前官方格式和本机可验证行为为准，并同步修订参考。
6. 读取所有将被修改的配置，建立现有 server 和设置清单后再编辑。

## 同步客户端规范文件

配置 MCP 之前，必须让对应客户端加载 LSP 工作规范：

1. 完整读取 bin/LSP/AGENTS.md。
2. 配置 Codex 或 Antigravity 时，目标是项目根 AGENTS.md。
3. 配置 Claude Code 时，目标是项目根 CLAUDE.md。
4. 配置三家时，同时同步 AGENTS.md 和 CLAUDE.md；不要假设一个客户端会读取另一个客户端的规范文件。
5. 样板中的受管范围由 mcp-lsp-project-rules:start 和 mcp-lsp-project-rules:end 标记。目标已有同一标记时更新该范围，不得再次追加。
6. 目标没有标记但已经有等价规则时，做语义对照；只补缺失项，可为本次纳入的规则添加一组标记，禁止制造重复章节。
7. AGENTS.md 不存在时可以使用完整样板创建；CLAUDE.md 不存在时创建 CLAUDE.md，并只追加样板受管标记之间的规则，不要把 AGENTS.md 标题复制成 CLAUDE.md 标题。
8. 已有目标文件时保留原内容和更强规则，只追加缺失的 LSP 规范，不得整份覆盖。

同步后必须确认本次客户端对应的规范文件至少包含：

- file、inspect、xref、grep、structure、patch_edit、completion 七个短工具名。
- 定位、定义理解、引用或调用层级、精读、diagnostics 的证据链。
- file(action=diagnostics) 是诊断入口，patch_edit 是编辑入口。
- LSP 失败时先收窄重试，仍失败则记录 blocker，不得静默降级。
- diagnostics 的 Error、Warning、Information、Hint 都要处理。
- 修改后运行匹配的构建与测试，异常和缺配置 fail-fast。

对应规范文件同步未完成或无法确认作用域时，不得继续声称 MCP 已按规范配置。MCP 配置让客户端发现工具，AGENTS.md 或 CLAUDE.md 让对应 Agent 按项目规则使用工具，两者缺一不可。

## 选择并验证二进制

| 当前主机 | 使用文件 | 预期 Go 目标 |
|---|---|---|
| macOS Intel | bin/LSP/mcp-lsp-mac-x86 | darwin/amd64 |
| macOS Apple Silicon | bin/LSP/mcp-lsp-mac-arm | darwin/arm64 |
| Linux/WSL x86-64 | bin/LSP/mcp-lsp-linux-x86 | linux/amd64 |
| Linux/WSL ARM64 | bin/LSP/mcp-lsp-linux-arm | linux/arm64 |
| Windows x64 | bin/LSP/mcp-lsp-windows-x64.exe | windows/amd64 |
| Windows ARM64 | bin/LSP/mcp-lsp-windows-arm64.exe | windows/arm64 |
| Windows x86 | bin/LSP/mcp-lsp-windows-x86.exe | windows/386 |

上表中的 `mcp-lsp-windows-{x64,arm64,x86}.exe` 是发布包的 canonical 文件名及 `windows/{amd64,arm64,386}` 架构映射，供打包、分发和配置示例选择；它们不是运行时 basename 白名单。运行时接受受信交付布局内的其他 `.exe` 名称（例如重命名或版本化名称），但仍强制校验受信 `bin`/`bin/LSP` 安装根、包内 `lsp` bundle、`lsp-manifest.json` 位置与摘要及可执行文件身份；改名不能绕过这些校验。Windows 资产和依赖仍只由 `NativeArch` 选择，`ProcessArch` 不得替代。

不能只按文件名判断。优先用 go version -m 读取 Go 构建元数据并确认 GOOS/GOARCH；macOS/Linux 可用 file 交叉验证 Mach-O/ELF，Windows 可检查 PE Machine。若无法验证实际目标，记录 blocker，不要写配置。

Windows 必须分别记录系统版本/build、操作系统原生架构和当前进程架构。二进制按原生架构选择；仿真进程的架构只用于审计，不能覆盖原生架构。mcp-lsp 安装器会用 Windows API 再次检测这三项并按目录最低版本/build fail-fast；Agent 不得用 `PROCESSOR_ARCHITECTURE` 或当前 shell 位数替代该判断。

同时确认文件存在、非空；macOS/Linux 还要确认可执行权限。不得把 Intel、ARM 或其他操作系统的文件配置给当前主机。

### Windows 原生、WSL 原生与 Windows→WSL 桥接

不要求用户填写额外平台开关。Agent 必须分别确认 MCP host 和 sidecar 的目标运行环境，不能把两者压缩成一个“当前平台”判断：

1. **Windows 原生直连（Windows EXE 主线）**：Windows host 默认直接启动对应原生架构的 `windows/*` EXE；`command`、`cwd`、resources 和 roots 全部使用 Windows drive/UNC 路径。
2. **WSL 原生直连**：WSL 内的 CLI/IDE host 直接启动 `linux/*` 二进制；所有路径使用 `/mnt/...` 或其他 Linux 绝对路径。
3. **Windows host 通过 `wsl.exe` 桥接 WSL sidecar**：只有用户明确要求 sidecar 在 WSL 运行、且实际 MCP host 是 Windows Codex Desktop/IDE/PowerShell 时使用。`wsl.exe` 是 Windows EXE 的启动/桥接边界，不是替代 Windows EXE 的 Linux-only 旁路。Windows 不能直接 `CreateProcess` `/mnt/.../mcp-lsp-linux-*`；`command` 必须是绝对 Windows `wsl.exe`，host 的 `cwd` 是 Windows 项目根，而 `args` 必须通过 `--cd <WSL项目根> env KEY=VALUE... ./bin/LSP/mcp-lsp-linux-*` 在 WSL 内设置 Linux resources/roots 并启动 ELF。
4. 当前编辑 shell 不等于 MCP host，也不等于 sidecar。必须分别记录 host、bridge（如有）和 sidecar 三层证据。无法确认任一层时先报告 blocker。
5. 用 `go version -m` 和 `file` 复核 Linux ELF 的 GOOS/GOARCH；用实际 `wsl.exe` command+args 完成 MCP initialize 和至少一次 tools/call。`mcp-lsp` 本身不负责 Windows/WSL 路径转换。
6. Windows host 启动 `wsl.exe env ...` 时不得假设 WSL 用户的登录 PATH 已加载。先在目标发行版内分别用 `command -v` 定位 `go`、`gopls`、`node`、`typescript-language-server` 及项目需要的其他语言服务器，再把覆盖这些绝对目录的 Linux PATH 显式放进 args 的 `env` 段。缺少任一必需语言服务器时 fail-fast；不得用一个未经探测的通用 PATH 掩盖缺依赖。

桥接模式禁止以下错误配置：

- Windows host 的 `command` 直接写 `/mnt/c/.../mcp-lsp-linux-x86`。
- `command=wsl.exe`，却只在 `[mcp_servers.<name>.env]` 写 Linux 路径并假设 WSL 会可靠转换或继承这些值。
- 依赖 Windows Codex 继承的 PATH 或 WSL 非登录进程的偶然 PATH，导致用户级 `/home/<user>/.local/bin` 中的 `gopls`、`typescript-language-server` 等不可见。
- 把 Windows `cwd` 与 Linux `GO_AGENT_LSP_ROOT` 直接做字符串相等断言。
- 在桥接链中改用 Windows `.exe`，却继续传 `/mnt/...` roots。

Codex Windows→WSL 的规范模板位于 `bin/LSP/codex-windows-wsl-lsp-config.example.toml`。

当前 shell 就是目标客户端环境时，先记录自动探测证据：

~~~powershell
$isNativeWindows = ($PSVersionTable.PSEdition -eq "Desktop") -or ($IsWindows -eq $true)
$isWSL = ($IsLinux -eq $true) -and (($null -ne $env:WSL_INTEROP) -or ($null -ne $env:WSL_DISTRO_NAME))
[PSCustomObject]@{
  OSVersion = [Environment]::OSVersion.Version.ToString()
  OSArchitecture = [Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()
  ProcessArchitecture = [Runtime.InteropServices.RuntimeInformation]::ProcessArchitecture.ToString()
  ProcessorArchitectureEnv = $env:PROCESSOR_ARCHITECTURE
}
~~~

~~~bash
is_wsl=0
if [ -n "${WSL_INTEROP:-}${WSL_DISTRO_NAME:-}" ] || grep -qi microsoft /proc/sys/kernel/osrelease 2>/dev/null; then is_wsl=1; fi
printf 'is_wsl=%s arch=%s\n' "$is_wsl" "$(uname -m)"
~~~

`$isWSL=true` 或 `is_wsl=1` 且 MCP host 本身位于 WSL 时选择 Linux 直连。`$isNativeWindows=true` 时先确认 sidecar 目标：原生目标选择 Windows `.exe`；用户明确要求 WSL sidecar 时选择 `wsl.exe` 桥接 Linux ELF。Windows 的 `OSArchitecture` 为 Arm64、X64、X86 时分别选择 `mcp-lsp-windows-arm64.exe`、`mcp-lsp-windows-x64.exe`、`mcp-lsp-windows-x86.exe`；`ProcessArchitecture` 不一致表示当前进程处于仿真层，不得据此降级。若当前 shell 只是在编辑另一个环境的配置，不能用编辑 shell 的结果覆盖 host/sidecar 判定，仍以目标客户端进程为准。

### Windows NativeArch、ProcessArch 与官方依赖边界

配置、安装和审计时把 `OSArchitecture` 记为 `NativeArch`，把 `ProcessArchitecture` 记为 `ProcessArch`。`NativeArch` 是唯一的 Windows 交付物/依赖选择键；`ProcessArch` 仅是仿真诊断字段，不能让 ARM64 host 降级到 x64，也不能让 x64/x86 host 借用另一架构资产。Windows EXE、EmmyLua、Swift、Node 和 VCLibs 都必须对同一 `NativeArch` 做 fail-fast 选择和完整身份复验。

必须把下列官方锁定事实当作配置审查边界（完整 URL/SHA 清单见本目录的 `references/provider-configs.md`）：

- EmmyLua 固定为官方 `EmmyLuaLs/emmylua-analyzer-rust` `0.25.1` `emmylua_ls-win32-arm64.zip`；归档和其中 `emmylua_ls.exe` 的 SHA-256、PE ARM64 必须复验，且只允许 Windows `NativeArch=ARM64`。
- Swift/sourcekit-lsp 固定为 Swift `6.3.3` 官方 Windows ARM64 installer；`windows.msi`、`windows.cab` 和 `a22`–`a28`（ARM64/x64/x86 及 experimental sibling CAB）必须由同一 installer 提取并放在同一目录，不能删掉 sibling CAB 或跨版本混用；`sourcekit-lsp.exe` 必须为 ARM64。
- Node 固定官方 `22.22.0` 的 `win-arm64`、`win-x64`、`win-x86` ZIP；VCLibs 固定微软 `Microsoft.VCLibs.140.00.UWPDesktop` `14.0.33321.0` 的 `arm64`、`x64`、`x86` Appx。每个架构分别锁定 URL/SHA/版本/身份，不读 PATH、不跨架构回退。
- Windows 私有 Terraform CLI companion 固定 `1.15.6`：ARM64 `https://releases.hashicorp.com/terraform/1.15.6/terraform_1.15.6_windows_arm64.zip`（`02820bcae3725c9c4e91deb6656e9b96ca8af9f395fc5faccc0820dd3295d6e0`）、x64 `..._windows_amd64.zip`（`56b4d3a157e346f8fc1e94254d0a944e6fec81f58ddd43eb274b8e0ebb56e334`）、x86 `..._windows_386.zip`（`00d51ccf53664f68bd6fb7dfa7edbc7bbff4032ff048787c096d23ece2dcc092`）。
- Windows 私有 rustfmt companion 固定 Rust `1.96.0` `rustfmt-preview` MSVC 归档：ARM64 `https://static.rust-lang.org/dist/2026-05-28/rustfmt-1.96.0-aarch64-pc-windows-msvc.tar.xz`（`d9e403d778e0ad95d814275b1265057478d4cde463d8bf620846056a7f00a59d`）、x64 `...-x86_64-pc-windows-msvc.tar.xz`（`7ae6d141dfb844355c4756a41f39ed45b74ff9295fff86bd0bf9b559a83c5d5d`）、x86 `...-i686-pc-windows-msvc.tar.xz`（`75a69f518db96b5c46fa4b98d169688e7670c8bff29b7f1831f6dcfdfc6311ab`）。
- 两类 companion 均须验证归档/解包摘要、PE Machine、产品根 ACL 与 reparse；只向 product-owned `terraform-ls`/`rust-analyzer` 子进程注入同一 NativeArch 的 PATH。非 Windows 与外部配置不变，禁止 PATH、用户缓存和跨架构 fallback。下载/安装 proof 与 correctness E2E 分离：本地锁定包存在时 correctness 必须 `cache_only=true`、`HTTP=0`，setup/import receipt 不能冒充自动下载证明。此处中文说明是公共配置语义，实际平台选择仍只在 Windows 生产实现中执行。

8.3 short path 只允许作为 Swift/Node installer 或子进程的临时进程边界，用来规避 `MAX_PATH`；canonical long path 才是缓存、manifest、receipt、日志、roots 和安全身份，不能持久化短名或用短名作授权/身份比较。TOML、PowerShell 和本文中的注释只解释配置与安全边界，不能授予 ACL、改变架构选择或执行提权。Windows Win32 `5`/`1314` 必须保留为结构化 `authorization_required`；无宿主授权桥时报告 blocker，不改 ACL、不换目录、不吞错。以上规则仅作用于 Windows 原生；非 Windows 行为保持不变，macOS/Linux/WSL 原生行为和既有 Mach-O/ELF 依赖选择保持不变。

Kotlin/IntelliJ 的 Windows ARM64 进程边界必须使用产品私有、物理扁平且经过 ACL、reparse、架构和摘要校验的 short root；`subst`、8.3、junction 和系统公共目录都不是合规替代。canonical root 仍用于缓存、manifest、receipt 和授权身份。容量预检或受控解包遇到空间不足时必须 fail-fast，receipt 分类为 `disk_space_exhausted`/`runtime_failure`，不得伪装成合法空结果或能力不支持。

当前远程 6b7 工具协议只认 content 纯文本行（`OK`/`ERROR`/`ATTR`/`ROW`/`HINT`/`WARNING`）。`StructuredContent` 应为空且不可作为 fallback；验收只能依据 content 和动作合同分类 success、legal_empty、capability_unsupported 或 runtime_failure。

## 确认可信 cwd 与 workspace root

写入任何客户端配置前，必须先解析并向用户展示两个真实绝对路径，然后询问本次 LSP 的可信 cwd 选择：

1. **本仓库**：`<repo-root>`。只允许 LSP 工具访问本仓库及其子目录，适合单仓库开发，也是最小权限选项。
2. **仓库上一级**：`<parent-of-repo-root>`。允许 LSP 工具访问该上级目录及其全部子目录，适合顶层目录下多个相关 Git 微服务需要互相导航的场景。

必须等待用户明确选择“本仓库”或“仓库上一级”；不得根据当前 shell cwd、配置文件位置、聊天截图或多仓库布局自行扩大范围。用户未确认、回答含糊、项目根无法唯一解析或项目根已经是文件系统根时，立即阻断并说明原因。除非用户另行明确指定并授权其他绝对路径，否则只提供上述两个候选。

将用户选中的绝对路径记为 `<trusted-cwd>`，并保持以下绑定：

- 直连模式下，支持 `cwd` 字段的客户端 server 配置必须写 `cwd = <trusted-cwd>`；不支持该字段的客户端不得发明字段。
- `GO_AGENT_LSP_ROOT=<trusted-cwd>`。
- `GO_AGENT_LSP_ROOTS` 必须由 JSON encoder 生成，当前选择只写一个元素：`[<trusted-cwd>]`。
- 项目级配置文件以及 AGENTS.md/CLAUDE.md 仍写在原项目根；选择仓库上一级不等于把配置迁移到上一级。
- `SUPER_DOLPHIN_RUNTIME_RESOURCES_DIR` 仍指向已验证的分发包资源根或 source checkout 根，不跟随 `<trusted-cwd>` 扩大。

Windows→WSL 桥接是路径表示上的明确例外，不是扩大权限：host `cwd` 写 Windows 项目根；`wsl.exe --cd`、resources 和两个 roots 写同一目录的 WSL 绝对路径。必须分别解析两侧真实路径，并用 `wslpath` 或 `readlink -f` 证明它们映射到同一目录；不得用字符串相等代替映射验证。

这里控制的是 mcp-lsp 的 workspace containment。可信目录之外的路径会返回 `path_outside_workspace`；扩大 LSP workspace 不等于自动扩大客户端自身的文件系统沙箱或写权限。

## 必需 sidecar 启动契约

每一个本地 stdio server 的 `env` 必须显式包含：

~~~text
SUPER_DOLPHIN_RUNTIME_MODE=dev
SUPER_DOLPHIN_RUNTIME_RESOURCES_DIR=<分发包资源根；源码构建则为 checkout 根，必须是绝对路径>
SUPER_DOLPHIN_DEPENDENCY_PROFILE=production
GO_AGENT_LSP_ROOT=<用户确认的 trusted-cwd 绝对路径>
GO_AGENT_LSP_ROOTS=<由 JSON encoder 生成、仅含 trusted-cwd 的绝对路径数组>
~~~

前三项是 sidecar 启动所需契约，后两项绑定可信 LSP workspace。独立 `mcp-lsp` 使用 `production`；`desktop_host` 只用于桌面 owner 的开发启动器，不能复制到三家独立 MCP 配置。不得依赖 shell 中偶然继承的值，不得在二进制中添加隐式默认值。

原生 Windows 使用共享 gopls 时，当前 server 的 `env` 还必须显式包含：

~~~text
SUPER_DOLPHIN_LSP_BUNDLE_DIR=<bin/LSP/lsp 的绝对路径>
SUPER_DOLPHIN_LSP_MANIFEST=<bin/LSP/lsp/lsp-manifest.json 的绝对路径>
~~~

这两个字段只证明包内 gopls 的路径与摘要，不改变可信 workspace；不得把它们与 `GO_AGENT_LSP_ROOT(S)` 混用。bundle、manifest 或原生 `gopls.exe` 缺失时 fail-fast，不得退回 PATH gopls。把 bundle 仅视为命中 adapter 的受信二进制覆盖，禁止据此裁剪通用语言注册；manifest 未包含的其他已支持语言仍须进入自动发现或按需安装链路。

`SUPER_DOLPHIN_RUNTIME_RESOURCES_DIR` 在本 dev 分发布局中是随 `bin/LSP` 交付的资源根；从源码构建时是 source checkout 根。它不是目标源码文件目录，也不是凭二进制位置临时猜出的值。若用户采用其他资源布局，必须先核对真实资源根，再显式配置。

Windows 的 `GO_AGENT_LSP_ROOTS` 必须由 JSON encoder 生成；不要手工拼接 `C:\...`。直连模式的 command、cwd、runtime resources 与 roots 必须属于同一种路径体系。Windows→WSL 桥接模式则必须严格分层：Windows `command/cwd` 属于 host，`args` 中 `--cd`、resources、roots 和 Linux binary 属于 WSL sidecar；不得跨层混写。

桥接模式必须把五个必需变量和经目标 WSL 实机探测的 Linux `PATH` 作为 `wsl.exe` 参数中 `env KEY=VALUE...` 的一部分显式注入 Linux 进程。可以在 Codex server 的 `env` 表中同步保留 sidecar 字段用于配置审计，但不能依赖 Windows host 环境自动成为正确的 Linux sidecar 环境。PATH 中的 home 目录必须先解析为绝对 Linux 路径；不要把不会经 shell 展开的字面 `$HOME` 写入 TOML args。

正式构建的 LSP 空闲生命周期默认且最低为 15 分钟。不要在项目配置中写小于 `15m` 的 `MCP_LSP_IDLE_TIMEOUT` 或旧别名；正式二进制会 fail-fast。带 `mcp_lsp_short_idle_precheck` build tag 的短周期二进制只用于快速预检，不能交付，也不能替代“14 分钟仍存活、15 分钟后回收、精确进程身份零残留”的真实生命周期证据。

Windows Win32 `5` 或 `1314` 权限错误必须保留为结构化 `authorization_required`。桌面宿主必须通过 `ApprovalRequester` 发布真实授权提示；只有用户明确批准后，才允许对同一个已固定 peer 精确重试一次。拒绝、无决定、无审批 UI 或单次重试仍失败时都保持 blocker，禁止循环重试、改 ACL、换备用目录或吞错。独立 stdio sidecar 没有宿主授权桥，不能自行提权，也不能声称已经弹窗或取得权限。

原生 Windows 且 `SUPER_DOLPHIN_DEPENDENCY_PROFILE=production` 时，语义工具可见性还可由带 Windows build tag 的生产自动安装器提供：空 PATH、无额外 bundle 的 `tools/list` 也必须精确包含七个工具族，并在 sidecar 日志中标明 `source=windows_production_auto_installer`。这不是语言级 PASS；随后必须实际调用目标语言并验证安装、语义结果和生命周期。非 Windows/WSL 不读取这条 Windows 策略，仍按自己的 bundle/PATH 事实判断。

语言级验收必须逐一执行精确 36 键闭包，分布固定为 `file/inspect/xref/grep/structure/patch_edit/completion = 8/5/7/6/5/4/1`：`file` 为 `open_file`、五种 `read_file-*` 动作（`single/full/batch/lines/function`）及 `diagnostics`、`diagnostics-batch`；`inspect` 为 `hover/definition/implementation/type_definition/signature_help`；`xref` 为 `references`、`references-no-declaration`、三种 `call_hierarchy-*` 与两种 `type_hierarchy-*`；`grep` 为 `text_search`、`text_search-regex`、`text_search-paths`、`text_search-file_paths`、`text_search-glob`、`ast_search`；`structure` 为 `document_symbol`、两种 `workspace_symbol-*`、`folding_range`、`semantic_tokens`；`patch_edit` 为 `replace_range/rename/code_action/format`；`completion` 为 `completion`。精确键以 `bin/LSP/README.md` 的“36 个小动作的精确验收合同”为可读清单，以 E2E 的 `realMCPExpectedActionKeys` 为可执行守卫。结果必须区分 `success`、`legal_empty_success`、能力快照明确允许的 `capability_unsupported` 和 `runtime_failure/NON_PASS`；不得用工具可见性或合法空结果掩盖运行失败。

## 根据客户端配置

只处理用户要求的客户端；用户要求 all 或三家共用时才处理全部。

### Codex

- 项目文件：.codex/config.toml。
- 只在项目受信任时生效。
- stdio server 使用 mcp_servers.<name> 表、command、args、cwd 和 env。
- env 必须包含三个 sidecar 启动字段与两个 `GO_AGENT_LSP_ROOT(S)` workspace 字段；原生 Windows 还必须包含两个受信 LSP bundle 字段。
- Windows Desktop/IDE 桥接 WSL 时，使用 `wsl.exe` 模板，并在 args 的 `env` 段显式传入五个 Linux sidecar 字段与实机探测的 Linux PATH；不得让 Windows 直接执行 Linux ELF，也不得依赖登录 shell 才存在的 PATH 修改。
- 需要强制 LSP 时设置 `enabled = true` 和 `required = true`；初始化失败必须阻断，不能静默省略后继续任务。
- 保留其他 MCP server、features、hooks、model 和逐工具审批设置。

#### Codex 工具延迟暴露

Codex 可能已发现并启动 `lsp`，但首层工具列表不直接显示 `mcp__lsp__*`，只把它们放入 code mode 的延迟工具目录。先用 `codex features list` 检查 `tool_search_always_defer_mcp_tools`：若该项显示 `removed` 且有效值为 `true`，不要写 `features.tool_search_always_defer_mcp_tools = false`；该旧开关不会改变有效状态。

要让 LSP 命名空间作为直接工具暴露，逐字段合并以下项目级配置，不得覆盖已有 `[features]` 内容：

~~~toml
[features.code_mode]
enabled = true
direct_only_tool_namespaces = ["mcp__lsp"]
~~~

`mcp__lsp` 是命名空间，不是具体工具名。该设置控制工具 schema 的直接暴露方式，不承诺 sidecar 零耗时启动；同时保留 `[mcp_servers.lsp] required = true`，让初始化失败 fail-fast。修改后必须完整重启 Codex 宿主并新建任务；旧任务已经生成的工具 schema 不能作为新配置生效证据。

重启后同时验证三项，缺一不可：

1. 当前任务的顶层直接工具声明出现 `mcp__lsp`，并包含 `file`、`inspect`、`xref`、`grep`、`structure`、`patch_edit`、`completion`。
2. 不经过 `functions.exec`，直接调用至少一个 `mcp__lsp.<tool>` 成功。
3. 在 `functions.exec` 内执行 `ALL_TOOLS.filter(({ name }) => name.startsWith("mcp__lsp__"))`，结果应为 `[]`。`ALL_TOOLS` 是 code mode 的嵌套/延迟工具目录；direct-only 生效后 LSP 从这里移除，因此空数组是成功证据，不是未注册。只有“顶层直接工具不存在或直接调用失败”时，空数组才表示 LSP 两边都不可用。

最后确认 `codex features list` 中 `code_mode` 为 `true`，并用 `/mcp` 检查 `lsp` 已连接。不要把 `ALL_TOOLS` 非空、仅 `/mcp` enabled 或仅有 sidecar 进程当成直接暴露成功。

### Claude Code

- 项目文件：项目根 .mcp.json。
- 使用 mcpServers 对象中的项目 server；这是 project scope。
- 本地 stdio server 使用 command、args 和 env。
- env 必须包含三个 sidecar 启动字段与两个 `GO_AGENT_LSP_ROOT(S)` workspace 字段；原生 Windows 还必须包含两个受信 LSP bundle 字段。
- 首次加载项目 server 时需要 workspace trust 和用户批准。
- 不得误写默认 local scope 或用户级 ~/.claude.json。

### Google Antigravity

- 项目文件：.agents/mcp_config.json。
- 使用 mcpServers 对象中的 workspace-local server。
- 本地 stdio server 使用 command、args、cwd 和 env。
- env 必须包含三个 sidecar 启动字段与两个 `GO_AGENT_LSP_ROOT(S)` workspace 字段；原生 Windows 还必须包含两个受信 LSP bundle 字段。
- 不得写全局 ~/.gemini/config/mcp_config.json。
- 远程 MCP 才使用 serverUrl；本地 mcp-lsp 不使用 url、httpUrl 或 serverUrl。

#### Antigravity 同名配置冲突排查

工具已经显示但首次或后续 `tools/call` 报 `client is closing: EOF`、`Transport closed` 或 sidecar 很快退出时，不要只检查 `.agents/mcp_config.json`，也不要先归因于 Antigravity。先在当前 workspace 内完整盘点：

1. 规范入口 `<workspace>/.agents/mcp_config.json`。
2. 自动加载的 `<workspace>/.agents/plugins/*/mcp_config.json`。
3. 旧安装或误写的 `<workspace>/.gemini/config/mcp_config.json`。
4. 全局 `~/.gemini/config/mcp_config.json` 中是否还有同名 server；只读检查，未经用户明确授权不得修改全局配置。

同名 `lsp` 出现在规范入口和插件或旧副本中不是冗余备份：不同 `cwd`、roots、command 或 env 可能让客户端发现工具后启动另一份 server，造成调用时路径解析、进程 owner 和 stdio 生命周期不一致。以用户确认的正确配置为基准逐字段比较；确认插件只用于重复注册同一 server、没有其他能力后，获得删除授权再删除整个插件目录。不要保留空 `plugin.json`、wrapper 或 stale 配置。

必须从 `~/.super-dolphin/log/mcp-lsp/mcp-lsp-*.log` 核对实际生效值和时序：

- `tools/call begin/done` 之后才出现 `mcp stdio: read failed EOF`，说明二进制完成过调用，EOF 是 stdin 被关闭后的结果，不是二进制崩溃证据。
- `resolve parent path: lstat <trusted-cwd>/...` 说明请求相对路径按实际 trusted root 解析；用日志中的 root 和请求 path 重建最终路径。
- `sidecar requires SUPER_DOLPHIN_RUNTIME_MODE...` 只证明该次进程缺少启动 env。若它来自 Agent 用 shell 裸跑二进制的探测，不得据此断言正式 MCP server 配置漏传 env。
- `context canceled` 可能是上游 cascade 取消后的收敛结果；必须向前找到第一个工具错误或 stdin EOF，不能把最后一行当首因。

选择“仓库上一级”为 `<trusted-cwd>` 时，相对工具路径也以该上一级为基准。读取 `<trusted-cwd>/repo-a/cmd/main.go` 必须传 `repo-a/cmd/main.go`，不能传 `cmd/main.go`；否则会错误解析为 `<trusted-cwd>/cmd/main.go`。验证时必须覆盖这种带仓库目录前缀的真实调用。

删除重复配置或修改 server 后，必须完整退出并重启 Antigravity 宿主，再在 MCP Servers 页面 Refresh。仅 Refresh、新建 Agent 会话、重新加载窗口、覆盖配置或替换二进制都不能保证旧 stdio client 被销毁；已经 closing 的 client 不能原地复活。

## 修改配置后必须重启宿主

修改任何本地 stdio MCP 的 command、args、cwd、env、server 名、启用状态或配置来源后，必须完整停止并重新启动实际拥有 stdio 管道的宿主进程，然后再验证。该规则适用于 Codex、Claude Code、Antigravity 以及其他 MCP host：

- Codex Desktop/IDE：完整退出并重新打开宿主应用；Codex CLI：结束当前 CLI 进程并重新启动。
- Claude Code：结束当前 Claude Code/CLI 或承载其 MCP client 的 IDE host，再重新启动。
- Antigravity IDE/Desktop：完整退出并重新打开 Antigravity；Antigravity CLI：结束当前 CLI 进程并重新启动。

不得把 Refresh、Reload Window、重新打开项目、新建聊天或手工杀掉/重启 `mcp-lsp` 当作宿主重启。stdio 管道和 MCP client 由宿主拥有；宿主未重启时，旧进程、旧 env、旧配置快照或 closing client 都可能继续被复用。无法重启宿主时，把在线验证记为 `BLOCKED_HOST_RESTART_REQUIRED`，不得声称配置已经生效。

## Agent 自适配

Agent 可以根据事实调整 server 名、路径、环境变量、timeout、审批设置及客户端专属字段，也可以修改本技能和 references/provider-configs.md，使其匹配已验证的新版本行为。

自适配必须保留这些不变量：

1. 只写项目级配置。
2. 先按客户端同步项目根 AGENTS.md、CLAUDE.md 或两者，并保证重复执行不会重复追加。
3. 写入前严格读取并解析现有 JSON/TOML；未知结构立即阻断。
4. 逐字段合并，保留其他 server 和非 MCP 设置，不得整份覆盖。
5. 同名 server 内容不同时先展示差异并判断 owner；不得静默替换。
6. 直连模式的 command、cwd 和 roots 使用 sidecar 平台的一致路径。Windows→WSL 桥接模式的 command/cwd 使用 Windows 路径，args 内的 `--cd`、resources、roots 和 Linux ELF 使用经验证映射到同一可信目录的 WSL 路径；不得把桥接所需的分层路径误判为混用。
7. 不写密钥、令牌、账号、OAuth secret 或其他凭据。
8. 缺文件、错误架构、解析失败、schema 不明或客户端不受支持时 fail-fast。
9. 三个 sidecar 必需字段必须显式写在 server env 中；原生 Windows 的两个受信 LSP bundle 字段同样必须显式提供。不为一次性差异增加默认值、兼容分支或隐式 fallback。
10. 保留用户已有 `GOTOOLCHAIN` 策略。`auto` 或 `<name>+auto` 由 Go 在模块/go.work 目录中执行真实选择；不得为某个项目硬编码通用 Go 补丁版本。

如果目标项目的布局与 bin/LSP 不同，Agent 应直接按实际路径配置并更新说明，而不是强行搬运目录。移动项目或换机器后，要重新确认绝对路径和二进制架构。

## 编辑方法

1. 先输出拟修改文件、已有 server、目标 server 和字段差异。
2. 使用精确补丁或结构化编辑完成最小变更。
3. JSON 必须重新解析；TOML 必须通过当前客户端或可靠 TOML parser 重新解析。
4. 检查 diff，确认未删除或重排无关设置。
5. 配置含本机绝对路径时，明确说明是否适合提交；不得把本机配置冒充跨机器通用配置。

## 验证

1. 重新验证直连 command 或桥接链中的 `wsl.exe` 与 Linux binary 均存在、非空、架构正确；桥接模式必须确认 Linux binary 是 ELF 且 GOOS/GOARCH 匹配 WSL。
2. 直连模式确认 cwd、`GO_AGENT_LSP_ROOT` 和解码后的 `GO_AGENT_LSP_ROOTS` 与 `<trusted-cwd>` 完全一致。桥接模式分别验证 Windows cwd 和 WSL roots，并证明两者映射到同一用户确认的可信目录；不得做错误的跨平台字符串相等断言。
3. 重新读取本次客户端对应的 AGENTS.md、CLAUDE.md 或两者，确认受管规则存在一次且必需语义完整。
4. 重新解析所有修改后的 JSON/TOML。
5. Codex：完整退出并重启 Codex Desktop/IDE 宿主或 CLI 进程；信任项目后用 /mcp 或 codex mcp list 检查。
6. Claude Code：完整结束并重启 Claude Code/CLI 或承载 MCP client 的 IDE host；完成 workspace trust 和项目 MCP 批准后，用 /mcp、claude mcp list 或 claude mcp get 检查。
7. Antigravity：完整退出并重启 Antigravity IDE/Desktop 或 CLI 进程；宿主重启后再在 MCP Servers 页面 Refresh，或在 CLI 用 /mcp 检查。
8. 至少实际调用 file、structure、inspect、xref、diagnostics 中的一项；列表显示 enabled 不是运行证据。
9. 对含中文、空格或字面 `%` 的项目路径，至少用 `file(action=diagnostics)` 验证一次 file URI 能回到 workspace 内本机路径；`path_outside_workspace` 不能记为 PASS。
10. 对选择“仓库上一级”的配置，必须实际读取或导航一个位于上一级内、但不在本仓库内的已知文件；若没有可安全验证的相邻文件，明确记为未验证，不得扩大到其他目录取证。
11. 对 Go 项目保留并验证用户的 `GOTOOLCHAIN=auto`/`<name>+auto` 策略；版本探测应在已解析的 module 或 go.work 目录执行。
12. 若配置修改需要第二次复核，重复读取配置，确认没有重复规则、重复 server、stale 路径或旧字段。
13. Antigravity 必须再次扫描 `.agents/plugins/*/mcp_config.json` 和 workspace 内 `.gemini/config/mcp_config.json`，确认没有同名 `lsp` 副本；`initialize`、`tools/list` 和 UI enabled 不能替代至少一次真实 `tools/call`。
14. Windows→WSL 桥接必须使用配置中的完整 `command + args` 做启动验证；仅在 WSL shell 中裸跑 Linux binary 不能证明 Windows host 可以创建该 MCP 进程。
15. 桥接验证必须检查 `tools/list` 精确包含 `file`、`inspect`、`xref`、`grep`、`structure`、`patch_edit`、`completion` 七个工具。只出现 `file`、`grep` 时，优先用同一 command+args 执行 `command -v gopls` 和 `command -v typescript-language-server` 核对实际 PATH；不得把“server 已启动”写成 PASS。
16. 原生 Windows production 验证必须同时核对七族清单和可见性来源日志；PATH/bundle 为空时应命中 `windows_production_auto_installer`。只出现 `file`、`grep` 时先检查三个 `SUPER_DOLPHIN_*` 字段、实际 Windows EXE/NativeArch 和 installer 注册错误，不得照搬 WSL 的 PATH 修复或把两工具状态写成 PASS。

报告二进制目标、修改的项目级文件、保留的既有设置、解析结果、客户端发现状态和实际工具调用证据。未启动对应客户端时，把在线连接明确标为未验证。
