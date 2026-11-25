---
name: experience-manager
version: 2.0.0
description: "管理项目经验知识的沉淀与读取，实现知识闭环"

# 技能分类
category: "knowledge-management"

# 复杂度标识
complexity: "medium"

# 预计执行时长
typical_duration: "5-10min"

# 依赖关系
dependencies: []
benefits-from: []
conflicts-with: []

# 工件配置
output_artifact: "memory/artifacts/experience-manager/"

# 工具权限
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob

# 标签（用于技能推荐）
tags:
  - "经验管理"
  - "知识沉淀"
  - "错误预防"
  - "知识检索"
  - "复盘反思"
---

# Experience Manager - 经验管理技能

## 前置协议

### 环境检测

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "unknown")
mkdir -p memory/artifacts/experience-manager memory/retrospectives
```

### 调用方式

**方式1：工件传递**（推荐）
- 检测工件：`memory/artifacts/*/experience-*.json`

**方式2：用户直接调用**
- 使用 `/experience-manager` 命令

**详细说明**：参考 `detailed-guide.md`

---

## Overview

experience-manager 是独立的知识管理技能，负责项目经验知识的**沉淀、读取、复盘、反思**，实现知识闭环，帮助AI避免重复错误，持续改进。

**核心能力**：
1. **经验沉淀**：任务完成后，四层级同步沉淀
2. **经验读取**：任务开始前，智能检索历史经验
3. **经验复盘**：里程碑完成时，保留好的，改掉坏的
4. **经验反思**：验证有效性，提炼智慧
5. **错误预防**：检测风险，提供预防建议
6. **效果追踪**：记录应用效果，持续优化

**关键价值**：
- 避免重复错误，快速复用成功模式
- 持续积累知识资产，形成自我进化闭环

---

## 核心原则

### 四层级沉淀机制

| 层级 | 文件 | 维度 | 优先级 | 用途 |
|------|------|------|--------|------|
| **规则层** | CLAUDE.md | 做什么 | 最高 | 项目约定，强约束 |
| **策略层** | AGENT.md | 怎么做 | 高 | AI执行策略，决策规则 |
| **知识层** | MEMORY.md | 学到了什么 | 中 | 技术知识，经验总结 |
| **历史层** | MCP Memory | 过去发生了什么 | 低 | 完整历史，智能检索 |

**读取优先级**：规则层 > 策略层 > 知识层 > 历史层

**冲突处理**：以高优先级为准。

### 持续改进原则

- **好则加冕**：成功经验升级为规则/策略
- **错则改之**：失败教训更新知识库
- **动态更新**：过时经验及时标记和更新

---

## 核心能力

### 能力1：经验沉淀（Save）

**触发时机**：任务完成后，由 goal-oriented 调用

**执行步骤**：
1. 接收请求工件（`experience-save-request.json`）
2. 生成回顾报告（`memory/retrospectives/{task-id}.md`）
3. 四层级同步沉淀（CLAUDE.md、AGENT.md、MEMORY.md、MCP Memory）
4. 创建结果工件（`save-result-{timestamp}.json`）

**示例**：
```json
// 输入
{
  "action": "save",
  "task_id": "2026-03-24_task-keywords",
  "lessons_learned": ["经验1", "经验2"],
  "errors_fixed": [{"error": "...", "fix": "..."}]
}

// 输出：四层级同步更新 + 结果工件
```

---

### 能力2：经验读取（Retrieve）

**触发时机**：任务开始前，由 goal-oriented、pilot 调用

**执行步骤**：
1. 接收请求工件（`experience-request.json`）
2. 四层级并行检索（关键词匹配 + 语义检索）
3. 按优先级排序和去重
4. 生成预防清单和推荐模式
5. 创建结果工件（`experience-result-{timestamp}.json`）

**示例**：
```markdown
## 📚 历史经验参考

### ⚠️ 错误预防（来自 CLAUDE.md）
- 预防措施1
- 预防措施2

### 🎯 可复用模式（来自 AGENT.md）
- 代码模式/流程模式

### 📖 技术知识（来自 MEMORY.md）
- 知识点1、知识点2
```

---

### 能力3：经验复盘（Review）

**触发时机**：里程碑完成时，由 goal-oriented 调用

**目的**：保留好的，改掉坏的，持续优化

**执行步骤**：
1. 读取原始回顾文件
2. 分析应用效果（应用次数、成功率）
3. 评估得失（保留好的、改掉坏的）
4. 更新四层级知识库
5. 生成复盘报告

**示例**：
```markdown
## 复盘结果

### ✅ 保留好的（好则加冕）
1. **成功经验**
   - 应用效果：5次，成功率100%
   - 决策：写入 CLAUDE.md 强制规则

### ❌ 改掉坏的（错则改之）
1. **失败教训**
   - 问题：文档命名不直观
   - 改进：优化命名规范
```

---

### 能力4：经验反思（Reflect）

**触发时机**：经验可能过时、技术栈升级、定期反思

**目的**：验证有效性，提炼智慧

**执行步骤**：
1. 识别需要反思的经验（过期/低成功率）
2. 深度分析有效性（应用统计、失败案例）
3. 提炼智慧（表层经验 → 深层智慧）
4. 更新四层级知识库（标记旧经验、保存新经验）

**示例**：
```markdown
## 经验反思 - 目录检查

### 有效性分析
- 应用次数：8次，成功率：87.5%
- 问题：未考虑版本差异

### 智慧提炼
**表层经验**：测试前检查目录
**深层智慧**：防御性思维 + 版本意识 + 避免过度防御

**更新决策**：区分版本环境，优化检查流程
```

---

### 能力5：错误预防（Prevent）

**触发时机**：检测到潜在错误风险

**执行步骤**：
1. 检测风险（配置缺失、API错误使用等）
2. 检索相似历史错误
3. 生成预防建议和检查清单
4. 展示给用户确认

**示例**：
```markdown
## 💡 错误预防提醒

检测到风险：国际化配置缺失
预防措施：
- 检查 next.config.js 中的 i18n 配置
- 使用标准配置模板

历史错误：2026-03-20 类似错误
```

---

### 能力6：效果追踪（Track）

**触发时机**：经验被应用时

**执行步骤**：
1. 记录应用场景和上下文
2. 评估应用效果（是否预防错误、节省时间）
3. 更新经验统计数据
4. 持续优化知识库

**示例**：
```json
{
  "experience_id": "2026-03-24_i18n_config",
  "applied_count": 3,
  "error_prevented": 2,
  "time_saved": "50分钟"
}
```

---

## 复盘与反思的区别

| 维度 | 复盘（Review） | 反思（Reflect） |
|------|---------------|----------------|
| **对象** | 已完成任务/里程碑 | 已有经验 |
| **时机** | 完成后一段时间 | 经验可能过时时 |
| **目的** | 保留好的，改掉坏的 | 验证有效性，提炼智慧 |
| **深度** | 中等（关注得失） | 深度（关注本质） |

---

## 使用示例

### 场景1：任务完成后的完整流程

```bash
# 1. goal-oriented 创建目标
用户："优化文档结构"

# 2. 自动检索经验
experience-manager → 四层级检索 → 返回预防措施

# 3. 执行任务
应用经验或最佳实践

# 4. 里程碑复盘
experience-manager.review → 保留好的，改掉坏的

# 5. 整体完成
experience-manager.deep-review → 提炼智慧

# 6. 沉淀经验
四层级同步更新
```

### 场景2：检索历史经验

```bash
# 用户提出任务
用户："修复英文页面404错误"

# goal-oriented 调用
experience-manager.retrieve(
  keywords=["英文页面", "404", "路由"]
)

# 返回结果
- 错误预防：检查 i18n 配置
- 可复用模式：国际化路由配置模板
- 历史案例：2026-03-20 修复详情
```

---

## 常见误区

1. ❌ **只沉淀不读取** → 每次任务开始前必须检索经验
2. ❌ **只沉淀到单一位置** → 四层级同步沉淀，确保知识不丢失
3. ❌ **只沉淀不复盘** → 里程碑和整体完成时必须复盘
4. ❌ **经验过时未反思** → 定期反思，及时更新过时经验
5. ❌ **复盘流于形式** → 深度分析得失，制定可执行改进计划
6. ❌ **忽视智慧提炼** → 从经验中提炼方法论和可迁移模式

---

## 工件格式

**请求工件**：
```json
{
  "requesting_skill": "skill-name",
  "action": "save|retrieve|review|reflect",
  "task_keywords": ["关键词"],
  // 其他参数...
}
```

**结果工件**：
```json
{
  "status": "success",
  "timestamp": "2026-03-24T10:00:00Z",
  "layers_updated": ["CLAUDE.md", "AGENT.md", "MEMORY.md", "MCP Memory"],
  // 结果数据...
}
```

**详细格式**：参考 `templates/` 目录

---

## 模板文件

- `templates/retrospective-template.md` - 回顾报告模板
- `templates/experience-request-template.json` - 检索请求模板
- `templates/experience-retrieve-template.json` - 检索结果模板
- `templates/review-request-template.json` - 复盘请求模板
- `templates/reflection-request-template.json` - 反思请求模板

---

## 参考资料

**核心概念**：
- [Knowledge Management Systems](https://en.wikipedia.org/wiki/Knowledge_management_system)
- [Lessons Learned in Project Management](https://www.pmi.org/learning/library/lessons-learned-project-management-8096)
- [Agile Retrospectives](https://retrospectivewiki.org/)

**方法论**：
- [Double Loop Learning - Chris Argyris](https://en.wikipedia.org/wiki/Double-loop_learning)
- [Kaizen - Continuous Improvement](https://en.wikipedia.org/wiki/Kaizen)
- [The Five Whys - Root Cause Analysis](https://www.mindtools.com/a3mi00v/5-whys)

**详细指南**：参考 `detailed-guide.md` 获取完整的执行步骤、示例和最佳实践。

---

## 技能协作

**被调用入口**：
- ✅ `goal-oriented` - 创建目标时检索、里程碑/整体完成时复盘反思、完成后沉淀
- ✅ `pilot` - 调度前检索、检测风险时预防
- ✅ 其他技能 - 按需调用

**调用方式**：工件传递（推荐）或用户直接调用
