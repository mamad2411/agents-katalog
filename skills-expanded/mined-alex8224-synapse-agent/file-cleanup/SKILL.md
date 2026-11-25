---
name: file-cleanup
description: 扫描并清理磁盘文件空间。第一阶段扫描定位大目录并识别可清理内容（包管理器缓存、浏览器缓存、IDE 索引、updater 安装包、容器镜像、构建产物、日志等）；第二阶段按「可立即清理」与「需用户确认」两类执行清理，并验证释放空间。面向 Windows 用户目录与 WSL 环境。
license: Apache-2.0
compatibility: Windows 10/11 + PowerShell 7；可选 dust（目录大小查看）、WSL2（若需清理 WSL/容器）。
allowed_tools: execute, read_file, write_file, search_files, find_files
---

# 文件清理（扫描 + 清理）

## 触发场景

- 用户询问磁盘 / 用户目录的空间占用，或"有什么可清理的"。
- 用户要求清理缓存、临时文件、安装包、构建产物、容器镜像、日志等。
- 用户目录过大、磁盘告急。

## 工作流总览

1. **扫描**：定位空间大头，识别内容类别（数据 vs 缓存 vs 工具链）。
2. **分类**：按"可立即清理（安全）"与"需用户确认"两档归类。
3. **清理**：安全项直接执行；需确认项列出清单、预估收益与风险，等用户拍板。
4. **验证**：清理前后对比 C 盘剩余与目标目录大小，报告累计释放。

## 第 1 步：扫描

### 1.1 磁盘与用户目录总览

```powershell
Get-Volume | Where-Object DriveLetter | Select-Object DriveLetter, @{n='SizeGB';e={[math]::Round($_.Size/1GB,1)}}, @{n='FreeGB';e={[math]::Round($_.SizeRemaining/1GB,1)}}
# 用户目录总大小（可能耗时，设长超时）
$t=(Get-ChildItem $HOME -Force -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum; "{0:N1} GB" -f ($t/1GB)
```

### 1.2 目录大小探测（一律优先 dust）

> **总则**：任何目录/文件大小探测一律优先使用 `dust`（并行扫描、速度快、输出干净）。
> 仅当 `dust` 不可用时，才退回 PowerShell `Measure-Object` 统计。
> 注意：dust 对稀疏文件（如 WSL `ext4.vhdx`）报的是逻辑大小，会高估；物理占用统计与压缩判定见"边界与安全"。

```powershell
dust -d 1 -z 100M -b -P -r -o gb "$HOME"          # 一层，>100MB，最大在上
dust -d 1 -z 100M -b -P -r -o gb "$HOME\AppData\Local"
dust -d 1 -z 100M -b -P -r -o gb "$HOME\AppData\Roaming"
dust -d 2 -z 300M -b -P -o gb "$HOME\AppData\Local\Microsoft"   # 细分大目录到两层
```

PowerShell 兜底（仅当 dust 不可用）：

```powershell
Get-ChildItem $HOME -Force -Directory | ForEach-Object {
  $s=(Get-ChildItem $_.FullName -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
  [PSCustomObject]@{Name=$_.Name; SizeGB=[math]::Round($s/1GB,2)}
} | Sort-Object SizeGB -Descending | Select-Object -First 25
```

### 1.3 专项检查清单

| 检查项 | 位置 | 命令/要点 |
| --- | --- | --- |
| 包管理器缓存 | `~\.cache`、`Local\uv\cache`（缓存）、`Roaming\uv`（python 工具链安装，勿清）、`Local\npm-cache`、`Local\Yarn`、`Local\pnpm-cache`、`~\.nuget\packages`、`.cargo`、`.rustup`、`scoop` | 见第 3 步命令 |
| 浏览器缓存 | `Local\Google\Chrome\User Data`、`Local\Microsoft\Edge\User Data` | 只清 `Default\Cache` 等 Cache 目录，勿动书签/登录态 |
| IDE 缓存 | `Roaming\Code\User\workspaceStorage`、`Local\JetBrains\*\caches\|index`、`Roaming\jdtls-*` | jdtls 多为多版本残留 |
| updater/安装包 | `Local\@*-updater`、`Local\Microsoft\WinGet\Packages`、应用内 `upgrade` 目录 | 安装包缓存，可删 |
| 容器/WSL | `Local\wsl\*\ext4.vhdx`；WSL 内 `docker` | `wsl --list --verbose`、`docker system df` |
| 虚拟机 (VMware) | `vm`、`Virtual Machines\*.vmem`、`*.vmsn`、`*.vmx` | `Get-Process -Name vmx` 判运行；vmem 判定与清理见「VMware 虚拟机清理」 |
| Java 构建产物深挖 | 项目内 `target/`、`build/`、`out/` | 按名枚举（见「构建产物」行），注意 `src\dist` 可能是源码打包资源，勿删 |
| 多版本残留 | `scoop\apps`、`Roaming\jdtls-*` | 检查同应用多版本目录 |

## 第 2 步：分类

### 可立即清理（安全：缓存/构建产物，自动重建，无用户数据）

| 类别 | 示例位置 | 说明 |
| --- | --- | --- |
| 临时文件 | `Local\Temp` | 直接清，占用文件自动跳过 |
| 包管理器缓存 | npm/yarn/pnpm/uv/cargo/scoop cache | `* cache clean` 或删目录 |
| NuGet 全局包缓存 | `~\.nuget\packages` | `nuget locals all -clear` 或删目录，还原时自动下载 |
| 工具链旧版本 | rustup 非默认 toolchain、nvm 旧版本 | 保留默认/在用版本 |
| IDE/编辑器缓存 | VS Code workspaceStorage、JetBrains caches/index、jdtls-*、Zed extensions | 重建索引即可 |
| 浏览器 Cache 目录 | Chrome/Edge `Default\Cache`、`Code Cache`、`GPUCache`、`Service Worker\CacheStorage` | 仅缓存，不动 User Data 其他部分 |
| updater/安装包缓存 | `@*-updater`、`WinGet\Packages`、应用 upgrade | 已安装后无用 |
| 运行时下载缓存 | `~\.cache`（puppeteer/uv/huggingface 等）、`Local\zig`、`.vpython-root` | 重新下载 |
| 构建产物 | 项目 `target/`（Maven/Rust）、`build/`、`out/` | `cargo clean`、`mvn clean` 或删目录；按语言分组（Java/Rust/C/C++）统计便于选择 |
| 日志 | WSL `/var/log`、应用 logs | 轮转日志删除、活动日志 truncate |
| 容器垃圾 | WSL 内停止容器、未引用镜像 | `docker rm` + `docker image prune -a -f` |
| scoop 旧版本 | `scoop\apps\*\旧版本目录` | `scoop cleanup <app>` |

### 需要用户确认（含用户数据或不可再得）

| 类别 | 示例位置 | 风险 |
| --- | --- | --- |
| 聊天记录/数据 | 微信/企业微信 `Data`、`Index`、`Backup`、`xwechat` | 删除即丢聊天记录 |
| 浏览器用户数据 | Chrome/Edge `User Data` 中 Cache 以外 | 书签、历史、密码、登录态 |
| 浏览器 on-device AI 模型 | Chrome `User Data\OptGuideOnDeviceModel` 等 | 可重新下载（数 GB），下次用 AI 功能自动重建，需确认 |
| IDE 配置/插件 | JetBrains plugins、Trae/Cursor/CodeBuddy 配置 | 删后需重装/重配 |
| 项目源码 | `project`、`workspace` 等 | 用户工作数据 |
| 备份目录 | `*.bak`、`*.backup` | 确认无用才删 |
| 系统/工具链本体 | WSL 虚拟磁盘（**禁止删除**，仅 sparse/compact 回收）、`.rustup`、`.nvm`、`.jdks` | 破坏环境 |
| ISO/系统镜像 | `Downloads\iso` | 需重新下载，先确认 |
| 运行中组件 | 企业微信 wwmapp 等被进程占用 | 删除后需重新初始化 |

## 第 3 步：清理执行

### 通用规则

1. **先查进程**：`Get-Process -Name "*chrome*","*code*","*WXWork*"`，运行中的应用其缓存删除可能失败或写回。
   - 构建产物删除前另查 `java*`、`mvn*`、`gradle*` 及应用本体（如 `wezterm-gui`、`quickpaste-gpui`）；exe 从 `target` 运行时仅该 exe 被锁定自动跳过，其余可删，运行中的程序不受影响。
2. 删除一律 `Remove-Item -Recurse -Force -ErrorAction SilentlyContinue`，被占用文件自动跳过，不中断。
3. 删除目录前记录大小，便于验证：先 `Measure-Object Length -Sum` 算 before，删完算 after。
4. WSL/Docker 清理：先 `wsl --shutdown` 再删，或用 WSL 内命令。

### 常用清理命令（已在本环境验证）

```powershell
# 临时文件
Get-ChildItem $env:TEMP -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# 包管理器缓存
uv cache clean                      # uv
nuget locals all -clear             # NuGet（或删 ~\.nuget\packages）
npm cache clean --force             # npm
yarn cache clean                    # yarn
pnpm store prune                    # pnpm（或删 Local\pnpm-cache）

# scoop 旧版本（保留 current）
scoop cleanup <app1> <app2>         # 或列出多版本应用后逐个清理

# rustup 卸载旧工具链（保留默认 stable）
rustup toolchain list
rustup toolchain uninstall <toolchain>

# 浏览器缓存（仅 Cache 类，路径以 Chrome 为例，Edge 同构）
$t=@("$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache","$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache","$env:LOCALAPPDATA\Google\Chrome\User Data\Default\GPUCache","$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Service Worker\CacheStorage")
foreach($p in $t){ Remove-Item $p -Recurse -Force -ErrorAction SilentlyContinue }

# WSL 内 Docker 垃圾
wsl -d <Distro> -u root -- bash -lc 'docker ps -aq | xargs -r docker rm -f; docker image prune -a -f'

# WSL 虚拟磁盘空间回收（sparse，无需管理员）
wsl --manage <Distro> --set-sparse true --allow-unsafe   # 先 wsl --shutdown
wsl --shutdown                                            # 让 sparse 回收物理空间
```

### WSL 内部扫描

```bash
wsl -d <Distro> -u root -- bash -lc 'df -h /; du -x --max-depth=1 / 2>/dev/null | sort -rh | head -15'
# 容器/镜像占用
wsl -d <Distro> -u root -- bash -lc 'docker system df'
```

注意：`du` 必须用 `-u root`，普通用户会漏算 root 目录（如 `/var/lib/containerd`），导致统计严重偏低。

### VMware 虚拟机清理（.vmem / .vmsn）

- `*.vmem` 是虚拟机内存（RAM）镜像，出现在三种场景：运行中（临时）、**挂起**（恢复必需）、**快照**（`SnapshotN.vmem` + `.vmsn`）。
- 判定能否删除：
  1. `Get-Process -Name vmx` —— 有 vmx 进程则 VM 在运行，勿动。
  2. 看对应 `vmware.log` 尾部：`OS_Suspend` → `SUSPEND: Completed suspend` → `Transitioned vmx/execState/val to suspended` = 上次会话以**挂起**结束，vmem 是挂起内存，**不能直接删**；
     `Setting cleanShutdown = "TRUE"` 且无挂起事件 = 干净关机，残留的 hex 后缀 vmem 属孤儿，可删。
  3. 命名规律：`VM-xxxxxxxx.vmem`（hex 后缀）= 运行/挂起内存；`VM-SnapshotN.vmem/.vmsn` = 快照内存。
- 正确清理方式：
  - 挂起内存：VMware 内 Power On 丢弃挂起状态 → guest 正常关机 → VMware 自动删除 vmem，勿手动删。
  - 快照内存：VMware 内 delete snapshot（合并增量盘），**勿直接删** `SnapshotN.vmem/.vmsn` 文件，否则快照损坏。

## 第 4 步：验证

```powershell
Get-Volume -DriveLetter C | Select-Object @{n='FreeGB';e={[math]::Round($_.SizeRemaining/1GB,1)}}
```

- 汇报每个清理项的释放量与累计值（C 盘剩余前后对比）。
- 提醒会"回涨"的项（浏览器缓存、IDE 索引、容器镜像下次使用会重建）。
- 数据类（聊天记录、项目、工具链）未删，明确告知保留。

## 边界与安全

- **绝不删除 WSL 虚拟磁盘**（`Local\wsl\*\ext4.vhdx` 或发行版 vhdx）：它是 WSL 发行版系统盘。
  只允许两种空间回收方式：`wsl --manage <Distro> --set-sparse true --allow-unsafe`（sparse 自动回收，无需管理员），
  或管理员权限的 diskpart compact（需提权，非必需）。删除 vhdx = 摧毁发行版。
- **稀疏 vhdx 的坑**：新版 WSL2 默认已 sparse 且关机自动 trim。dust 对 vhdx 报的是**逻辑文件大小**（会严重高估可回收量）；
  物理占用用 `fsutil file queryAllocRanges offset=0 length=<文件大小> <vhdx>` 统计。先查 `fsutil sparse queryflag <vhdx>`：
  已是 sparse 则无可回收空间，且 `Optimize-VHD -Mode Full` 与 `diskpart compact` 都会拒绝操作（要求非稀疏文件），勿重复尝试。
- 不主动删除含用户数据的内容；始终区分"缓存可重建"与"数据不可再得"。
- 破坏性操作先获得用户明确确认；同一目标只做一次确认，不重复询问。
- 磁盘空间紧张的 WSL 场景，优先用 sparse 自动回收，避免手动 compact（需要管理员权限）。
- 不泄露密钥/凭证；清理时跳过 `.ssh`、`.git-credentials`、`.env` 等敏感目录。


