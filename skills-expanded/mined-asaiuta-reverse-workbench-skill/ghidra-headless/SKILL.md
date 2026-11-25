---
name: ghidra-headless
description: 使用 Ghidra analyzeHeadless 对提供的 EXE、DLL、ELF、SO、固件和未知二进制执行可重复的无头初筛：导出反编译 C、函数、字符串、符号、调用关系和摘要。用户提到 Ghidra headless、批量反编译、函数/字符串/调用图导出或需要为后续 IDA、radare2、Frida 分析建立标准产物时使用。
---

# Ghidra 无头批量分析

该模块将项目内经过验证的 Ghidra Java 导出脚本纳入全局工具链。它用于可复现的**初筛和证据导出**，不替代对关键函数的手工反汇编、动态验证或跨反编译器交叉确认。

## 入口与依赖

1. 先运行 `archive-file-triage/` 对未知输入记录类型、大小和 SHA-256。
2. 读取 `../tool-index.md`，以其中的 `analyzeHeadless` 实际路径为准；不得猜测 Ghidra 安装路径。
3. 若工具缺失，按 `skills/scripts/bootstrap-reverse.ps1` 的 `ghidra-mcp`/Ghidra 能力流程安装或配置后再执行。

资源：

```text
scripts/ghidra-analyze.ps1                 Windows 原生包装器
scripts/ghidra-analyze.sh                  Linux/WSL 包装器
scripts/ghidra_scripts/ExportAll.java      聚合导出
scripts/ghidra_scripts/ExportDecompiled.java
scripts/ghidra_scripts/ExportFunctions.java
scripts/ghidra_scripts/ExportStrings.java
scripts/ghidra_scripts/ExportCalls.java
scripts/ghidra_scripts/ExportSymbols.java
```

## 标准工作流

初筛优先使用 `ExportAll.java`，把结果写入任务专属目录：

```powershell
$skill = ".\skills\ghidra-headless"   # 相对于技能根目录
& (Join-Path (Resolve-Path $skill) "scripts\ghidra-analyze.ps1") `
  -Script ExportAll.java `
  -OutputDirectory .\artifacts\sample `
  -Binary .\sample.exe
```

按需导出单项产物：

```powershell
& "$skill\scripts\ghidra-analyze.ps1" -Script ExportStrings.java -OutputDirectory .\artifacts\sample -Binary .\sample.exe
& "$skill\scripts\ghidra-analyze.ps1" -Script ExportFunctions.java -OutputDirectory .\artifacts\sample -Binary .\sample.exe
```

对架构判断错误或裸固件，可显式指定 processor，例如 `-Processor 'ARM:LE:32:v7'`；仅在已经确认格式且需要加速时使用 `-NoAnalysis`。

## 标准产物

`ExportAll.java` 会按输入基名产生下列可归档产物（具体扩展名以脚本输出为准）：

```text
<name>_summary.txt
<name>_decompiled.c
<name>_functions.json
<name>_strings.json 或 <name>_strings.txt
<name>_symbols.json
<name>_calls.json
<name>_interesting.txt
ghidra_analysis.log
ghidra_output.log
```

先读 `*_summary.txt` 和 `*_interesting.txt`，再根据字符串、导入、函数和调用关系锁定关键函数。重要结论应带文件路径、函数名/地址与原始证据；反编译结果只是近似 C，不应单独作为最终结论。

## 后续路由

- 需要 CLI 深挖、脚本化反汇编或快速交叉验证 → `radare2/`。
- 需要 IDA 数据库、反编译或 MCP → `ida-reverse/`。
- 需要调试、Hook、内存或行为验证 → `reverse-engineering/tools-dynamic.md`。
- 输入是固件 → 先进入 `firmware-pentest/`；输入是 APK 中的 `.so` → 回到 `apk-reverse/` 的 Native 分支。

## 输出要求

报告输入哈希、Ghidra 实际路径、包装器命令、processor/cspec、产物目录、关键函数/地址、结论与仍需动态验证的假设。
