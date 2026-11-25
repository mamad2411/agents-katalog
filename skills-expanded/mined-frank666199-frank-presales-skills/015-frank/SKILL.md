# Skill: Frank-项目需求访谈标准化工具

## Profile
- **Author**: Frank
- **Version**: 1.0.0
- **Language**: 中文
- **Category**: 维度2 - 售前全流程标准化
- **Description**: 规范售前访谈流程，精准挖掘隐性核心需求

---

## When to Use
与客户进行需求调研会议前/后使用

---

## Input Requirements
- 访谈对象信息
- 项目背景资料
- 已有需求清单（可选）

---

## Workflow
1. 根据访谈对象角色定制访谈提纲（领导/业务/技术不同侧重）
2. 按SPIN框架设计问题：Situation现状/Pain痛点/Implication影响/Need-payoff需求确认
3. 访谈中记录关键信息点，标注显性vs隐性需求
4. 访谈后24小时内整理结构化纪要
5. 提取待确认事项和下一步行动
6. 生成需求确认书发送客户确认

---

## Output Format
访谈提纲 + 访谈纪要 + 需求确认书

---

## Output Template
```
问题编号 | SPIN类型 | 问题内容 | 客户回答 | 需求提炼 | 确认状态
```

---

## Example
| 字段 | 内容 |
|------|------|
| Q005 | Pain | '目前系统最大的痛点是什么？' | '数据孤岛严重，跨部门无法共享' | 数据共享平台需求 | 待确认 |

---

## Constraints
- 访谈提纲提前发送客户
- 纪要中区分'客户明确说'和'我方推断'
- 需求确认书需客户签字

---

## Quality Criteria
- [ ] 问题覆盖SPIN四层
- [ ] 纪要结构化
- [ ] 需求确认闭环

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

> **Frank专属售前技能** | 维度2: 售前全流程标准化 | 编号: 015
> 基于"Frank售前解决方案Skills工具集 v1.0"与实操提示词融合优化生成
