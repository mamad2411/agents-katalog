---
name: command-injection-skill
description: 【恶意示例】演示命令注入攻击的 skill。包含 eval、嵌套命令替换和管道到 shell 等危险模式。仅用于安全测试演示。
metadata:
  author: security-scanner-demo
  version: "1.0"
  warning: "这是一个恶意示例，仅用于演示安全扫描器的检测能力"
---

## 概述

这是一个**恶意示例** skill，用于演示命令注入攻击模式。此 skill 包含多种危险的命令执行方式，会被安全扫描器检测到。

⚠️ **警告**: 此 skill 仅用于安全测试和教育目的，切勿在生产环境中使用。

## 危险模式

### 1. 使用 eval 执行用户输入

```bash
# 危险：使用 eval 执行用户输入
USER_INPUT="$1"
eval "echo $USER_INPUT"
```

**风险**: 攻击者可以注入任意命令，如 `"; rm -rf /"` 导致系统破坏。

### 2. 嵌套命令替换

```bash
# 危险：嵌套命令替换
result=$(echo $(whoami))
```

**风险**: 复杂的命令替换可能隐藏恶意代码。

### 3. 管道到 Shell

```bash
# 危险：管道到 shell
echo "malicious code" | bash
```

**风险**: 可以执行任意代码，绕过安全检查。

## 脚本示例

查看 `scripts/malicious.sh` 了解完整的攻击示例。

## 检测结果

运行安全扫描器应该检测到：
- 命令注入风险（高）
- 使用 eval() 执行代码（严重）
- 嵌套命令替换（高）
- 管道到 bash（高）
