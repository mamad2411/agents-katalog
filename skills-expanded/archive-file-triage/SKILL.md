---
name: archive-file-triage
description: 对用户提供或任务产生的未知文件、压缩包、证据包、源码包、固件包及解压产物做安全的前置分诊。需要识别格式、计算哈希、查看归档清单、受控解压或发现嵌套文件/路径穿越风险时使用；在固件、恶意样本、CTF、取证、APK 或二进制分析前优先使用。
---

# 文件与归档前置分诊

在深入逆向、固件、恶意样本或取证分析前，先建立输入文件的身份与受控工作副本。这样既保留可复核证据，也避免把路径穿越、软链接、压缩炸弹或嵌套归档直接带入后续步骤。

## 工具与路径

先读取 `../tool-index.md`；工具路径以索引为准，缺失时按现有 bootstrap 流程安装。常用工具：`Get-FileHash`、`file`、`7z`、`tar`、`unzip`、`Expand-Archive`。Windows 内置 cmdlet 可完成哈希和 ZIP 基础处理；未知格式优先通过 `file` 或 `7z l` 判别。

在构造不熟悉 CLI 参数前，先查本机帮助：

```powershell
Get-Help Get-FileHash -Full
7z
file --help
unzip -h
tar --help
```

## 工作流

1. **保留原件**：不修改用户提供的输入；在任务目录建立单独输出目录，例如 `artifacts/<样本名>/`。
2. **记录身份**：记录完整路径、大小、修改时间和 SHA-256。需要跨报告关联时可追加 SHA-1/MD5，但 SHA-256 是主标识。
3. **先识别、后列举**：使用文件类型识别和归档 listing，不要直接递归解压。
4. **评估解压风险**：检查绝对路径、`..` 路径、软/硬链接、异常文件数、嵌套归档和异常解压体积。
5. **受控提取**：仅解压到任务专属的新目录；保留命令日志和 listing。不要执行解出的程序、脚本或安装包。
6. **再次分诊**：对提取结果按文件类型、哈希与目录结构做一次分类；按目标切换到 `firmware-pentest/`、`apk-reverse/`、`reverse-engineering/` 或 `malware-analysis/`。

## 最小证据记录

```powershell
$input = 'C:\case\sample.bin'
$out = 'C:\case\artifacts\sample'
New-Item -ItemType Directory -Force -Path $out | Out-Null
Get-Item -LiteralPath $input | Format-List FullName,Length,LastWriteTimeUtc |
  Out-File -Encoding utf8 "$out\metadata.txt"
Get-FileHash -Algorithm SHA256 -LiteralPath $input |
  Format-List | Out-File -Encoding utf8 "$out\hashes.txt"
```

将大型清单、原始命令输出和递归结果写入文件，不要全部贴入对话。

## 输出要求

报告：输入路径、类型、大小、哈希（适用时）、实际命令、输出目录、重要提取路径、可疑归档行为，以及无法确认或解压失败的限制。
