---
name: togaf
version: 1.0.0
description: TOGAF (The Open Group Architecture Framework) enterprise architecture methodology and best practices. Provides ADM (Architecture Development Method) guidance, architecture content framework, building blocks, viewpoints, and governance. Use this skill for enterprise architecture planning, architecture development, transition planning, or any TOGAF-based architecture work.
author: DeepArchi
license: MIT
keywords:
  - togaf
  - enterprise-architecture
  - adm
  - architecture-development-method
  - building-blocks
  - architecture-governance
  - deeparchi
---

# TOGAF Skill - 企业架构框架

## 概述

TOGAF (The Open Group Architecture Framework) 是业界最广泛使用的企业架构框架。本技能提供 TOGAF 方法论、ADM 流程、架构内容框架和最佳实践指南。

## 何时使用

当用户需要：
- 了解或应用 TOGAF 企业架构框架
- 执行 ADM（架构开发方法）流程
- 创建 TOGAF 架构制品和交付物
- 设计架构视图和视角
- 建立架构治理机制
- 制定架构原则和标准
- 规划架构转型路径

## 快速开始

1. 参考 `README.md` 了解 TOGAF 核心概念
2. 查看 `references/adm-deliverables-guide.md` 了解各阶段交付物
3. 使用 `assets/adm-phases.drawio` 作为 ADM 流程参考
4. 参考 `references/principles-template.md` 编写架构原则

## 核心功能

- **ADM 完整指南**：Preliminary 到 Phase H 的全流程指导
- **架构内容框架**：Content Metamodel 和实体定义
- **构建块体系**：ABB 和 SBB 的定义与管理
- **视图和视角**：标准视角和视图设计
- **架构治理**：治理框架和合规审查
- **集成指南**：与 ArchiMate、BIAN 等框架集成

## ADM 阶段速查

```
Preliminary    → 准备组织实施 EA
Phase A       → 架构愿景、利益相关者
Phase B       → 业务架构（能力、流程、服务）
Phase C       → 信息系统架构（数据、应用）
Phase D       → 技术架构（基础设施）
Phase E       → 机会与解决方案（工作包）
Phase F       → 迁移规划（过渡架构）
Phase G       → 实施治理（合规审查）
Phase H       → 架构变更管理
Requirements  → 贯穿全程的需求管理
```

## 关键概念速查

### Building Blocks（构建块）

- **ABB (Architecture Building Block)**: 逻辑定义，独立于实现
- **SBB (Solution Building Block)**: ABB 的具体产品/技术实现

### 架构层次

| 层次 | 内容 | ADM 阶段 |
|------|------|---------|
| Business | 能力、流程、服务 | Phase B |
| Data | 数据实体、数据流 | Phase C1 |
| Application | 应用组件、接口 | Phase C2 |
| Technology | 平台、基础设施 | Phase D |

## 资源文件

- `README.md` - 完整技能文档
- `EXAMPLES.md` - 使用示例
- `assets/adm-phases.drawio` - ADM 阶段流程图
- `assets/building-blocks-template.xlsx` - 构建块模板
- `references/adm-deliverables-guide.md` - ADM 交付物指南
- `references/viewpoints-catalog.md` - 视角目录
- `references/principles-template.md` - 原则模板
- `scripts/validate-artifacts.js` - 验证脚本

## 相关链接

- [TOGAF Official Website](https://www.opengroup.org/togaf)
- [ArchiMate Standard](https://www.opengroup.org/archimate)
- [DeepArchi 架构管理平台](https://www.deeparchi.com.cn)
