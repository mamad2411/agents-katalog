---
name: re-tool-downloader
description: 逆向工具下载执行器——把 re-tool-registry 的任务清单变成磁盘上可用的工具：GitHub API 解析最新版下载链接、PowerShell 下载（带重试）、SHA256 记录、绿色解压到 C:\tools。当用户点名要下载或安装某工具（Ghidra、x64dbg、dnSpy、DIE 等）、或上层已产出清单待执行时使用。触发词：下载工具、安装工具、装上、下载执行、获取最新版本。不生成清单（属 re-tool-registry）、不维护 MANIFEST（属 re-tool-manifest）。
agent_created: true
x-alice-class: reverse
---# 逆向工具下载执行器（re-tool-downloader）

## 单一职责

只做一件事：**执行下载任务**——下载 → 校验 → 解压落地，产出"下载结果"。
清单来自 re-tool-registry，结果交 re-tool-manifest 登记。

## 触发条件

- 用户点名："下载 Ghidra / 把 x64dbg 装上"
- re-flow-orchestrator 在 ENV 阶段拿到清单后调用
- 上层传入现成任务清单

## 输入与输出

- **输入**：任务清单（`name` / `source` / `asset_pattern` / `type` / `dest`），或单个工具名（自动经 re-tool-registry 补全）
- **输出**：每项工具的下载结果——`status 成功/失败`、落地路径、SHA256、文件大小、版本标签；失败时给出原因与重试建议

## 执行步骤（一律 PowerShell，本机 bash coreutils 已损坏）

1. **准备环境**
   ```powershell
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   New-Item -ItemType Directory -Force -Path C:\tools\downloads
   ```
2. **GitHub 类解析最新版**（不硬编码版本号）
   ```powershell
   $rel = Invoke-RestMethod "https://api.github.com/repos/<org>/<repo>/releases/latest" -Headers @{ 'User-Agent'='workbuddy' }
   $asset = $rel.assets | Where-Object { $_.name -match '<asset_pattern>' } | Select-Object -First 1
   $url = $asset.browser_download_url; $ver = $rel.tag_name
   ```
3. **pip 类**：`pip install pefile capstone frida-tools`（托管环境装进 venv；frida 慢，后台跑）
4. **下载**：`Invoke-WebRequest -Uri $url -OutFile C:\tools\downloads\<name>-<ver>.zip`；失败重试 3 次，间隔 5 秒
5. **校验**：文件大小 > 1MB（防抓到错误页）+ `Get-FileHash -Algorithm SHA256` 记录哈希供审计
6. **解压**（green）：`Expand-Archive -LiteralPath <zip> -DestinationPath C:\tools\<name>\ -Force`；zip 内若多包一层目录，把内容上提
7. **installer 型**：下载到 downloads 后提示用户手动装（或给静默参数），不做强制静默
8. **输出结果清单**（stdout 表格），交 re-tool-manifest 登记

## 已知坑

- GitHub API 不带 User-Agent 会 403
- 本机 bash coreutils 损坏（`ls`/`head`/`dirname` 找不到）——所有操作走 PowerShell
- 下载"最新版"不要硬编码版本号，用 API 动态解析
- 哈希无法预置（版本滚动），正确做法是**下载后记录 SHA256 供审计**，而非预校验
- 大文件（Ghidra 数百 MB）下载可能中断，用后台任务 + 重试

## 边界与上下游

- **上游**：re-tool-registry（清单来源）
- **下游**：re-tool-manifest（结果登记）
- **调用方**：re-flow-orchestrator（ENV 阶段链式调用：registry → 本 skill → manifest）
