# Skill: Frank-大模型选型工具

## Profile
- **Author**: Frank
- **Version**: 1.0.0
- **Language**: 中文
- **Category**: 维度7 - AI项目专精
- **Description**: 对比主流大模型在场景下的性能/成本/合规表现

---

## When to Use
AI项目技术选型阶段

---

## Input Requirements
- 应用场景描述
- 性能要求
- 预算约束
- 合规要求

---

## Workflow
1. 梳理候选模型：开源(DeepSeek/Qwen/LLaMA) vs 商业(GPT/Claude/文心/通义/豆包)
2. 按6维度评估：性能/成本/合规/部署/生态/定制化
3. 性能对比：理解能力/生成质量/推理速度/多模态能力
4. 成本对比：API调用成本/部署成本/微调成本
5. 合规评估：数据出境/算法备案/内容安全
6. 输出选型推荐和对比矩阵
7. 提供POC验证建议

---

## Output Format
大模型选型报告（含对比矩阵+推荐方案+POC建议）

---

## Output Template
```
评估维度 | DeepSeek | Qwen | GPT-4 | Claude | 文心 | 通义 | 推荐选择
```

---

## Example
| 字段 | 内容 |
|------|------|
| 推理速度 | 快(本地) | 中(本地) | 慢(API) | 慢(API) | 中(API) | 中(API) | DeepSeek(本地部署) |

---

## Constraints
- 性能数据来自公开评测或实测
- 成本计算含隐性成本
- 合规评估覆盖法规要求

---

## Quality Criteria
- [ ] 评估维度完整
- [ ] 对比客观公正
- [ ] 推荐有充分依据

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

> **Frank专属售前技能** | 维度7: AI项目专精 | 编号: 075
> 基于"Frank售前解决方案Skills工具集 v1.0"与实操提示词融合优化生成
