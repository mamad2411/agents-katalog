# Skill: Frank-AI架构图绘制辅助工具

## Profile
- **Author**: Frank
- **Version**: 1.0.0
- **Language**: 中文
- **Category**: 维度1 - AI售前工具应用
- **Description**: 智能生成AI系统、数字化项目技术架构、业务架构图

---

## When to Use
方案编制中需要技术架构图、业务架构图、部署架构图时使用

---

## Input Requirements
- 系统组件清单
- 组件间关系描述
- 架构类型（业务/技术/部署/数据）

---

## Workflow
1. AI解析系统组件和关系，确定架构层次（接入层/应用层/服务层/数据层/基础设施层）
2. 按架构类型选择合适的图示模式（分层/总线/微服务/事件驱动）
3. 生成架构图的Mermaid/PlantUML代码
4. 标注每层的功能说明和技术选型
5. 生成图注和架构说明文字
6. 提供多种布局方案供选择

---

## Output Format
架构图代码（Mermaid/PlantUML）+ 架构说明文档 + 布局建议

---

## Output Template
```
层次 | 组件 | 技术选型 | 功能说明 | 与上层关系 | 与下层关系
```

---

## Example
| 字段 | 内容 |
|------|------|
| 应用层 | 政务服务门户 | Vue3+ElementPlus | 提供统一服务入口 | 接入层负载均衡 | 调用服务层API网关 |

---

## Constraints
- 组件关系逻辑正确
- 技术选型标注版本
- 图示层次清晰

---

## Quality Criteria
- [ ] 架构层次完整
- [ ] 组件关系准确
- [ ] 可直接渲染使用

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

> **Frank专属售前技能** | 维度1: AI售前工具应用 | 编号: 011
> 基于"Frank售前解决方案Skills工具集 v1.0"与实操提示词融合优化生成
