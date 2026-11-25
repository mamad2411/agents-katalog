# Skill: Frank-智能体设计工具

## Profile
- **Author**: Frank
- **Version**: 1.0.0
- **Language**: 中文
- **Category**: 维度7 - AI项目专精
- **Description**: 设计AI Agent架构，生成智能体工作流

---

## When to Use
AI项目中需要设计Agent方案

---

## Input Requirements
- 业务场景
- 任务流程
- 可用工具/API

---

## Workflow
1. 设计Agent架构：感知模块→规划模块→记忆模块→工具模块→行动模块
2. 定义Agent角色和能力边界
3. 设计工作流：任务理解→计划制定→工具调用→结果整合→输出反馈
4. 规划记忆系统：短期记忆(对话上下文)+长期记忆(向量数据库)
5. 设计工具集成：API调用/数据库查询/文件操作/代码执行
6. 制定异常处理和回退策略
7. 输出Agent设计文档

---

## Output Format
Agent设计文档（含架构图+工作流+记忆设计+工具集成+异常处理）

---

## Output Template
```
Agent模块 | 功能 | 技术实现 | 工具/依赖 | 异常处理 | 性能指标
```

---

## Example
| 字段 | 内容 |
|------|------|
| 规划模块 | 任务分解和计划制定 | ReAct+CoT推理 | LLM+规划模板 | 规划失败→重试3次 | <5秒 |

---

## Constraints
- Agent能力边界明确
- 工具调用安全可控
- 异常处理完善

---

## Quality Criteria
- [ ] 架构设计合理
- [ ] 工作流覆盖完整
- [ ] 安全边界清晰

---

## Applicable Scenarios
- **G端政府项目**: 部分适用
- **B端企业项目**: 部分适用
- **AI智能项目**: 适用

---

## Usage
### 方式1：Claude Code / Cursor / Codex
将本SKILL.md内容复制到Agent技能配置区，通过技能名触发。

### 方式2：飞书妙搭 / 扣子
将SKILL.md内容粘贴到Agent提示词配置区，设置触发词为技能名。

### 方式3：独立使用
直接复制本文件内容到AI对话中，按Workflow步骤执行。

---

> **Frank专属售前技能** | 维度7: AI项目专精 | 编号: 076
> 基于"Frank售前解决方案Skills工具集 v1.0"与实操提示词融合优化生成
