---
name: model-orchestrator
description: "Global model orchestrator that intelligently distributes tasks across different AI models (Claude/Gemini/GLM/MiniMax) based on task complexity, logical depth, code implementation requirements, or Chinese semantic understanding needs"
---

# Global Model Orchestrator (全球全明星模型分发器)

## 概述
当处理用户的研发需求时，本 Skill 会评估任务节点对“创造力”、“逻辑深度”、“代码实现”或“中文语义”的不同需求，在 Antigravity 默认模型（Claude/Gemini）与自定义外部模型（GLM/MiniMax）之间自动进行任务拆解与分发。

## 模型矩阵与擅长领域划分

### 1. 战略规划层 (Tier 0: Reasoning & Architecture)
*   **候选模型**: **Claude 4.5 Opus** / **Gemini 3 Pro**
*   **擅长领域**: 极其复杂的项目架构设计、长难代码逻辑推理、处理超长上下文依赖。
*   **分配场景**: “帮我重构整个项目的架构”、“分析这 20 个文件之间的调用漏洞”。

### 2. 核心逻辑与中文语义层 (Tier 1: Logic & Localization)
*   **候选模型**: **GLM-4.7** (via NVIDIA NIM)
*   **擅长领域**: 中文业务需求理解、逻辑推理、指令遵循（尤其是中文语境下的多步推理）。
*   **分配场景**: “根据这份中文 PRD 梳理业务流程”、“编写符合中国开发者习惯的文档”。

### 3. 工程实现与快速补全层 (Tier 2: implementation & Speed)
*   **候选模型**: **MiniMax M2.1** (via NVIDIA NIM) / **Gemini 3 Flash**
*   **擅长领域**: 极速代码片段生成、单元测试编写、常规 Bug 修复。
*   **分配场景**: “为这两个类写测试用例”、“把这个函数转换成异步版本”。

### 4. 工具执行与环境交互层 (Tier 3: Execution)
*   **候选模型**: **Antigravity (System)**
*   **擅长领域**: 操作本地文件、搜索实时文档、执行终端命令。

## 自动化分配工作流
1.  **需求解析**: Antigravity 首先作为一个“网关”解析用户意图。
2.  **节点拆解**: 将大任务拆解为“设计”、“实现”、“执行”等子任务。
3.  **模型分包**:
    - 如果涉及极其精妙的代码优化，请求由 UI 端的 **Claude 4.5** 引擎处理。
    - 如果涉及理解中文特定业务含义，通过 API 隧道交由 **GLM-4.7**。
    - 如果是大规模的搬砖工作（测试用例），交由 **MiniMax M2.1**。
4.  **汇总执行**: Antigravity 汇总各方结果，在用户本地环境中落地代码。
