# Skill: Frank-算力规划工具

## Profile
- **Author**: Frank
- **Version**: 1.0.0
- **Language**: 中文
- **Category**: 维度7 - AI项目专精
- **Description**: 针对训练/推理场景，进行GPU集群规模测算和算力经济性分析

---

## When to Use
AI项目需要规划算力资源时

---

## Input Requirements
- 模型规模
- 使用场景(训练/推理)
- 并发要求
- 预算约束

---

## Workflow
1. 评估训练算力需求：模型参数×训练数据×计算量→GPU小时
2. 评估推理算力需求：并发请求×响应时间→GPU数量
3. 选择GPU型号：A100/H100/RTX4090/国产昇腾
4. 规划集群架构：训练集群/推理集群/存储/网络
5. 测算算力成本：购买vs租赁vs云服务
6. 进行算力经济性分析：TCO/ROI
7. 输出算力规划方案

---

## Output Format
算力规划方案（含需求测算+选型+架构+成本分析+经济性分析）

---

## Output Template
```
算力项 | 需求 | 选型 | 数量 | 单价 | 成本 | 备注
```

---

## Example
| 字段 | 内容 |
|------|------|
| 训练算力 | 700亿参数微调 | A100 80G | 8卡 | 20万/卡 | 160万 | 含NVLink互联 |

---

## Constraints
- 算力测算有公式依据
- 成本含隐性成本
- 经济性分析客观

---

## Quality Criteria
- [ ] 测算准确
- [ ] 选型合理
- [ ] 成本分析全面

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

> **Frank专属售前技能** | 维度7: AI项目专精 | 编号: 078
> 基于"Frank售前解决方案Skills工具集 v1.0"与实操提示词融合优化生成
