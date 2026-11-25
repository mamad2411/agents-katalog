# Skill: Frank-售前线索甄别分级工具

## Profile
- **Author**: Frank
- **Version**: 1.0.0
- **Language**: 中文
- **Category**: 维度2 - 售前全流程标准化
- **Description**: 快速筛选G/B端有效线索，划分项目优先级

---

## When to Use
获取新项目线索后，第一时间评估跟进价值

---

## Input Requirements
- 线索来源信息
- 客户基本信息
- 项目概况描述

---

## Workflow
1. 按BANT框架评估：Budget预算/Authority决策权/Need需求/Timeline时间表
2. 结合MEDDPICC补充：Metrics量化指标/Economic Buyer经济买家/Decision Criteria决策标准/Decision Process决策流程/Identify Pain痛点/Champion内线/Competition竞争
3. 评估线索真实性：信息完整度、客户主动度、预算明确度
4. 划分优先级：A级(立即跟进)/B级(持续培育)/C级(暂缓)/D级(放弃)
5. 输出线索评估报告和跟进建议
6. 生成线索台账登记信息

---

## Output Format
线索评估报告（含BANT+MEDDPICC评分、优先级、跟进建议）

---

## Output Template
```
评估维度 | 信息/评分 | 依据 | 结论
```

---

## Example
| 字段 | 内容 |
|------|------|
| Budget | 预算约200万(客户口述) | 会议提及 | 有明确预算，BANT-B:高 |

---

## Constraints
- 评估基于事实信息，不主观臆断
- 缺失信息标注'待确认'
- 优先级评估有据可查

---

## Quality Criteria
- [ ] 评估维度完整
- [ ] 优先级判定合理
- [ ] 跟进建议具体可操作

---

## Applicable Scenarios
- **G端政府项目**: 适用
- **B端企业项目**: 适用
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

> **Frank专属售前技能** | 维度2: 售前全流程标准化 | 编号: 013
> 基于"Frank售前解决方案Skills工具集 v1.0"与实操提示词融合优化生成
