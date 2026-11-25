# Skill: Frank-行业大模型方案工具

## Profile
- **Author**: Frank
- **Version**: 1.0.0
- **Language**: 中文
- **Category**: 维度7 - AI项目专精
- **Description**: 生成垂直行业大模型预训练/微调/部署方案

---

## When to Use
行业大模型定制项目

---

## Input Requirements
- 目标行业
- 可用行业数据
- 性能要求
- 预算约束

---

## Workflow
1. 分析行业大模型需求：场景/数据/性能/合规
2. 选择基座模型：开源大模型(DeepSeek/Qwen/LLaMA)
3. 设计预训练方案（如需要）：行业语料+训练策略
4. 设计微调方案：SFT+RLHF+DPO
5. 规划数据方案：数据采集→清洗→标注→增强
6. 设计评估方案：行业Benchmark+人工评估
7. 规划部署方案：量化/蒸馏/推理优化
8. 输出行业大模型方案

---

## Output Format
行业大模型方案（含基座选型+训练方案+数据方案+评估方案+部署方案）

---

## Output Template
```
方案环节 | 技术方案 | 数据/资源需求 | 预期效果 | 风险/备注
```

---

## Example
| 字段 | 内容 |
|------|------|
| 微调 | LoRA微调+SFT | 10万条行业QA对 | 行业准确率提升15% | 需高质量标注数据 |

---

## Constraints
- 数据来源合法合规
- 训练方案有依据
- 评估方案可量化

---

## Quality Criteria
- [ ] 方案覆盖全流程
- [ ] 技术方案专业
- [ ] 成本估算合理

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

> **Frank专属售前技能** | 维度7: AI项目专精 | 编号: 080
> 基于"Frank售前解决方案Skills工具集 v1.0"与实操提示词融合优化生成
