---
name: "dump-analyzer"
description: "Analyzes Java heap dump files (.hprof) using Eclipse MAT to identify memory leaks and OOM causes. Invoke when user uploads a .hprof file, provides a dump file path, or asks about memory leak analysis."
---

# Dump文件分析器 (MAT版)

## 功能

使用 Eclipse Memory Analyzer Tool (MAT) 深度分析 Java 堆转储文件（.hprof），识别内存泄漏、内存溢出等问题的根本原因，提供全面的内存分析报告。

## 触发条件

- 用户上传 `.hprof` 文件
- 用户提供 dump 文件路径
- 用户询问 "内存泄漏分析"
- 用户遇到 "OOM" 或 "OutOfMemoryError"
- 用户询问 "dump文件分析"
- 用户询问 "内存溢出原因"

## 依赖要求

- **必需**: Eclipse MAT 1.15+ 已安装
- **环境变量**: `MAT_HOME` 指向 MAT 安装目录

## 完整分析流程

### 步骤 1: 检测 MAT 环境

首先检查 `MAT_HOME` 环境变量是否已设置：

```powershell
$env:MAT_HOME
```

**如果未设置，按以下流程处理：**

#### 1.1 搜索常见安装位置

检查以下常见安装路径：

- `C:\Program Files\Eclipse\MAT`
- `C:\MAT`
- `D:\Develop\MAT\mat`
- `D:\MAT`

```powershell
$matPaths = @(
    "C:\Program Files\Eclipse\MAT",
    "C:\MAT",
    "D:\Develop\MAT\mat",
    "D:\MAT"
)

$foundMat = $null
foreach ($path in $matPaths) {
    if (Test-Path "$path\ParseHeapDump.bat") {
        $foundMat = $path
        break
    }
}

if ($foundMat) {
    Write-Host "找到 MAT 安装目录: $foundMat"
    $env:MAT_HOME = $foundMat
} else {
    Write-Host "未找到 MAT 安装"
}
```

#### 1.2 如果未找到，引导用户安装

如果搜索不到 MAT，向用户说明并提供安装指导：

***

**⚠️ 未检测到 Eclipse MAT**

分析 dump 文件需要 Eclipse Memory Analyzer Tool (MAT)。

**选项 1: 自动下载安装**

1. 下载地址: <https://www.eclipse.org/mat/downloads.php>
2. 选择 "Windows (x86\_64)" 版本
3. 解压到任意目录（建议 `D:\Develop\MAT\mat`）

**选项 2: 如果您已安装 MAT**
请提供 MAT 的安装路径，例如：

- `D:\Develop\MAT\mat`
- `C:\Program Files\Eclipse\MAT`

**设置环境变量后重新分析：**

```powershell
$env:MAT_HOME = "您的MAT安装路径"
```

***

### 步骤 2: 执行 MAT 分析

确认 MAT 环境后，执行分析：

```powershell
# 使用 MAT 命令行工具生成 Leak Suspects Report
& "$env:MAT_HOME\ParseHeapDump.bat" <dump-file> org.eclipse.mat.api:suspects

# 示例
& "$env:MAT_HOME\ParseHeapDump.bat" C:\temp\heapdump.hprof org.eclipse.mat.api:suspects
```

### 步骤 3: 读取分析结果

MAT 会生成以下文件：

- `<dump-file>_Leak_Suspects.zip` - 泄漏嫌疑点报告（含 HTML）
- `<dump-file>_Leak_Suspects.html` - 泄漏嫌疑点摘要
- `<dump-file>.index` - 索引文件（后续分析用）

### 步骤 4: 解压并解析报告

```powershell
# 解压报告
Expand-Archive -Path "<dump-file>_Leak_Suspects.zip" -DestinationPath "mat-report" -Force

# 读取 index.html 获取核心发现
Get-Content "mat-report\index.html" -Raw
```

## 完整报告分析维度

分析报告应包含以下所有维度，无论是否有问题：

### 1. 系统概览 (System Overview)

**必须读取文件**: `pages/System_Overview2.html`

展示内容：

- 堆内存总大小和已使用大小
- 对象总数
- 类总数
- 类加载器数量
- GC Roots 数量
- JVM 版本信息
- Dump 文件生成时间

### 2. 泄漏嫌疑点分析 (Leak Suspects)

**必须读取文件**: `index.html`, `pages/19.html`, `pages/23.html`

展示内容：

- 泄漏嫌疑点数量和严重程度
- 每个嫌疑点的详细信息：
  - 问题对象类型
  - 占用内存大小
  - 对象数量
  - 类加载器信息
  - 引用链分析

### 3. 类直方图 (Class Histogram)

**必须读取文件**: `pages/Class_Histogram7.html`

展示内容：

- Top N 内存占用类（按 Retained Heap 排序）
- 每个类的：
  - 对象数量
  - Shallow Heap
  - Retained Heap
- 识别异常大对象集合

### 4. 线程概览 (Thread Overview)

**必须读取文件**: `pages/Thread_Overview5.html`, `pages/30.html`, `pages/37.html`

展示内容：

- 所有线程列表
- 每个线程的：
  - 线程名称
  - 状态（alive, runnable, parked, waiting 等）
  - 是否为守护线程
  - 上下文类加载器
  - 堆栈信息
- 识别线程泄漏和死锁

### 5. 大对象分析 (Top Consumers)

**必须读取文件**: `pages/Top_Consumers6.html`

展示内容：

- 单个最大对象列表
- 每个对象的：
  - 对象类型
  - Shallow Size
  - Retained Size
  - 支配树信息

### 6. 支配树分析 (Dominator Tree)

**通过 MAT OQL 查询获取**

展示内容：

- 对象引用关系
- 内存占用路径
- GC Roots 到对象的引用链

### 7. GC Roots 分析

**通过 MAT 报告获取**

展示内容：

- 阻止对象被回收的根引用
- 引用类型（JNI Global、System Class、Thread 等）
- 引用链分析

### 8. 系统属性 (System Properties)

**必须读取文件**: `pages/System_Properties4.html`

展示内容：

- JVM 启动参数
- 系统环境变量
- 应用配置信息

## 分析报告模板

### 报告结构

```markdown
# Dump文件完整分析报告

## 1. 执行摘要
- 分析时间
- Dump文件信息
- 风险等级评估
- 主要发现概述

## 2. 系统概览
[展示 System Overview 所有指标]

## 3. 内存分布
- 堆内存使用详情
- 类加载器分布
- 对象数量统计

## 4. 类直方图分析
[展示 Top 20 类，包含正常和异常的]

## 5. 泄漏嫌疑点详细分析
[如果有泄漏嫌疑点]
- 问题描述
- 根因分析
- 修复建议

[如果没有泄漏嫌疑点]
- 说明未检测到明显泄漏
- 提供健康度评估

## 6. 线程分析
[展示所有线程状态]
- 线程总数
- 各状态线程数量
- 异常线程识别

## 7. 大对象分析
[展示 Top Consumers]
- 最大对象列表
- 内存占用分析

## 8. GC Roots 分析
[展示关键 GC Roots]
- 引用链分析
- 阻止回收的原因

## 9. 优化建议
[根据所有分析维度给出建议]
- 立即修复项
- 性能优化项
- 监控建议

## 10. 附录
- 系统属性详情
- 完整类直方图
- 线程堆栈详情
```

## 输出内容规范

### 必须包含的内容

1. **所有分析维度** - 不管是否有问题都要展示
2. **数据对比** - 与正常值的对比（如果有参考值）
3. **健康度评估** - 每个维度的健康状态
4. **风险评级** - 高/中/低/正常
5. **可操作建议** - 针对每个异常点给出具体修复方案

### 健康度标识

- 🔴 **高** - 严重问题，需要立即修复
- 🟡 **中** - 潜在问题，建议优化
- 🟢 **低** - 轻微问题，可以观察
- ⚪ **正常** - 无异常，状态良好

## 故障排除

### 问题: MAT\_HOME 未设置

**解决**: 设置环境变量指向 MAT 安装目录

```powershell
$env:MAT_HOME = "D:\Develop\MAT\mat"
[System.Environment]::SetEnvironmentVariable("MAT_HOME", "D:\Develop\MAT\mat", "User")
```

### 问题: ParseHeapDump.bat 找不到

**解决**: 确认 MAT 安装正确，或手动指定路径

```powershell
# 检查文件是否存在
Test-Path "$env:MAT_HOME\ParseHeapDump.bat"
```

### 问题: 分析大文件时内存不足

**解决**: 修改 MAT 内存配置
编辑 `MemoryAnalyzer.ini`，调整 `-Xmx` 参数：

```
-Xmx8g
```

## 相关资源

- [Eclipse MAT 下载](https://www.eclipse.org/mat/downloads.php)
- [MAT 文档](https://help.eclipse.org/latest/index.jsp)
- [Java Heap Dump Analysis Guide](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/)

