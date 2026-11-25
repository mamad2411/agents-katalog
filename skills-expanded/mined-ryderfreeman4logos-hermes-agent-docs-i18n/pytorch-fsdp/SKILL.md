---
name: pytorch-fsdp
description: Fully sharded data-parallel training for large models.
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [torch>=2.0, transformers]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Distributed Training, PyTorch, FSDP, Data Parallel, Sharding, Mixed Precision, CPU Offloading, FSDP2, Large-Scale Training]

---

# Pytorch-Fsdp 技能

基于官方文档生成的、用于辅助 pytorch-fsdp 开发的工具。

## 何时使用此技能

在以下情况下可触发此技能：
- 处理 pytorch-fsdp 相关任务
- 查询 pytorch-fsdp 的功能或 API 信息
- 实现 pytorch-fsdp 解决方案
- 调试 pytorch-fsdp 代码
- 学习 pytorch-fsdp 的最佳实践

## 快速参考

完整的常用模式目录（包含约 157,000 字节的可运行 FSDP 示例代码）位于 `references/common-patterns.md` 文件中。当需要了解封装、分片策略、检查点机制或混合精度相关示例时，可通过 `read_file` 函数加载该文件。建议直接参考此文件，而非凭记忆重新编写 FSDP 代码。

## 参考文件

此技能在 `references/` 目录下提供了详尽的文档资料：

- **other.md** - 其他文档

如需详细信息，可使用 `view` 函数查看特定的参考文件。

## 如何使用此技能

### 对于初学者
建议先阅读入门指南或教程类参考文件，掌握基础概念。

### 针对特定功能
可根据需求选择对应的分类参考文件（如 API 文档、使用指南等）以获取详细信息。

### 查看代码示例
上述快速参考部分汇总了从官方文档中提取的常用模式示例。

## 资源链接

### references/
该目录收录了从官方来源整理的文档资料，内容包括：
- 详细的说明文字
- 带有语言注释的代码示例
- 对应原始文档的链接
- 便于快速导航的目录结构
### scripts/
在此处添加用于常见自动化任务的辅助脚本。

### assets/
在此处存放模板、基础代码示例或项目范例。

## 备注

- 该技能是根据官方文档自动生成的。
- 参考文件保留了源文档的结构与示例内容。
- 代码示例会进行语言检测，以实现更出色的语法高亮显示。
- 快速参考模式是从文档中的常见使用案例中提取而来的。

## 更新说明

如需使用最新文档更新此技能：
1. 使用相同的配置重新运行抓取工具。
2. 该技能将基于最新信息重新生成。


