---
name: re-tool-manifest
description: 逆向环境登记簿——维护 C:\tools\MANIFEST.md（已装工具、版本、路径、SHA256 的权威记录），提供环境快照检查（pip 库 / C:\tools / Program Files 三级扫描）。当用户问"装了哪些工具、环境检查、还缺什么"，re-tool-downloader 完成需登记，或任何流程开工前自检时使用。触发词：环境检查、已装工具、MANIFEST、环境快照、还缺什么、工具状态。只做状态记录与查询，不执行下载。
agent_created: true
x-alice-class: reverse
---# 逆向环境登记簿（re-tool-manifest）

## 单一职责

只做一件事：**记录并回答"当前环境里有什么"**——下载结果登记 + 环境快照查询。

## 触发条件

- 用户："检查逆向环境 / 还缺什么工具 / 装了哪些"
- re-tool-downloader 完成时登记结果
- re-flow-orchestrator 开工前 ENV 自检

## 输入与输出

- **登记模式**输入：re-tool-downloader 的结果（name、type、version、path、sha256、时间）
- **查询模式**输入：无参数（全量快照）或工具名
- **输出**：
  - `C:\tools\MANIFEST.md`：登记表，列为 `name | type | version | installed | path | sha256 | source`
  - 环境快照：对照 re-tool-registry 最小启动集，输出 ✓已装 / ✗缺失 清单

## MANIFEST.md 格式

```
| name | type | version | installed | path | sha256 | source |
|---|---|---|---|---|---|---|
| ghidra | green | 11.2 | 2026-09-18 | C:\tools\ghidra\ | 3f9a… | NationalSecurityAgency/ghidra |
```
文件不存在则创建并写入表头；重复登记同一工具时按 `installed` 时间覆盖旧行。

## 环境检查逻辑（PowerShell，禁用 bash）

1. **pip 库**：`python -c "import pefile, capstone, frida"`，报 ModuleNotFoundError 即缺失
2. **绿色工具**：`Get-ChildItem C:\tools` 与 MANIFEST 比对（目录存在且有可执行文件）
3. **安装向导类**：扫 `C:\Program Files`、`C:\Program Files (x86)` 目录名匹配
4. 汇总成三级状态表输出，缺失项建议调用 re-tool-registry + re-tool-downloader 补齐

## 已知坑

- 本机 bash coreutils 损坏，列目录一律用 PowerShell
- 外部工具不在 PATH 属正常（绿色解压即用），不能只用 `where` 判断
- 托管 Python 与系统 Python 不同源，检查 pip 包时确认用的是跑脚本的那个解释器

## 边界与上下游

- **上游**：re-tool-downloader（结果登记）
- **服务对象**：re-flow-orchestrator（ENV 自检）、re-flow-recon / capture / unpack 的开工前置检查
- **参考数据源**：缺失判定对照 re-tool-registry 的最小启动集
