---
name: hello-world-skill
description: 一个简单安全的 Hello World skill，演示基本的系统信息显示功能。用于对比安全和不安全的 skill 示例。
metadata:
  author: security-scanner-demo
  version: "1.0"
---

## 概述

这是一个**安全示例** skill，展示了正常、无害的操作。此 skill 只执行基本的信息显示命令，不涉及任何危险操作。

✅ **安全**: 此 skill 不包含任何恶意代码或危险操作。

## 功能

### 1. 显示问候信息

```bash
echo "Hello, World!"
```

### 2. 显示当前时间

```bash
echo "当前时间: $(date)"
```

### 3. 列出当前目录

```bash
ls -la
```

### 4. 显示系统信息

```bash
uname -a
```

## 使用说明

这个 skill 演示了安全的命令使用方式：
- 只读操作
- 不访问敏感信息
- 不修改系统文件
- 不执行网络请求
- 不使用危险的命令执行模式

## 检测结果

运行安全扫描器应该：
- ✓ 未发现安全问题
- 所有操作都是安全的
