---
name: archive-skill
description: 对话归档技能。将当前对话流程提取并生成可重用的 skill 文件。
user-invocable: true
---

# /archive-skill - 对话归档

> **将成功对话转化为可复用技能**

分析当前对话，识别模式，生成可重用的 skill 文件。

---

## 核心分析流程

### 阶段 1：对话结构分析

#### 识别对话模式

| 特征维度 | 简单 | 流程 | 迭代 | 协作 |
|----------|------|------|------|------|
| **工具数量** | 1-2 | 3-5 | 3+ | 5+ |
| **执行顺序** | 线性 | 顺序 | 循环 | 并行/嵌套 |
| **重复模式** | 无 | 无 | 有 | 可能 |
| **Skill 调用** | 无 | 无 | 无 | 有 |
| **决策节点** | 0-1 | 2-3 | 1-2 | 3+ |

**判断逻辑**：
```
IF 调用其他 skills/agents THEN 协作模式
ELIF 包含重复循环 THEN 迭代模式
ELIF 工具调用 >= 3 THEN 流程模式
ELSE 简单模式
```

#### 提取关键信息

**决策节点关键词**：
- 条件判断：`if`, `是否`, `是否需要`
- 选项选择：`选择 A/B`, `方案 1/2`
- 验证检查：`检查`, `验证`, `确认`
- 错误处理：`失败`, `错误`, `异常`

**变量识别规则**：

| 变量来源 | 识别规则 | 参数化 |
|----------|----------|--------|
| 用户输入 | 用户明确提供的值 | `{{user_input}}` |
| 文件路径 | 文件操作中的路径 | `{{file_path}}` |
| 项目名 | 仓库名/项目名 | `{{project_name}}` |
| 函数/类名 | 代码标识符 | `{{function_name}}` |
| 数值 | 数字、计数 | `{{count}}` |
| 配置项 | 配置文件内容 | `{{config}}` |

### 阶段 2：抽象化处理

#### 通用化规则

| 保留 | 去除 | 示例 |
|------|------|------|
| 工具名称 | 具体参数值 | `Read()` → `Read({{file_path}})` |
| 步骤顺序 | 用户特定内容 | `编辑 src/auth.py` → `编辑 {{file_path}}` |
| 条件判断 | 项目路径 | `/home/user/project` → `{{project_path}}` |
| 输出格式 | 时间戳 | `2025-01-15` → (删除) |

#### 模板选择

| 模式 | 模板文件 | 提取重点 |
|------|----------|----------|
| 简单 | `templates/simple.md` | 核心步骤、主要工具 |
| 流程 | `templates/workflow.md` | 步骤序列、依赖关系、输出文件 |
| 迭代 | `templates/iterative.md` | 循环阶段、验证条件、退出条件 |
| 协作 | `templates/workflow.md` | 调用的 skills/agents、编排方式 |

### 阶段 3：生成输出

#### 信息推断

| 缺失项 | 推断规则 |
|--------|----------|
| skill 名称 | 从对话主题提取，如 "TDD 开发" → "tdd-workflow" |
| 描述 | 总结对话目的 |
| 使用场景 | 从对话初始问题提取 |
| 工具依赖 | 从实际调用的工具提取 |

#### 输出路径

```bash
# 默认
.claude/skills/{{skill_name}}/SKILL.md

# 用户指定
/archive-skill --output ./my-skills/
```

#### 质量检查

生成后验证：
- [ ] frontmatter 完整（name, description, user-invocable）
- [ ] 所有 `{{变量}}` 都有说明
- [ ] 工具依赖表与实际使用一致
- [ ] 步骤顺序与原对话一致
- [ ] 代码示例可运行（如果有）

---

## 使用方式

```bash
/archive-skill                          # 自动分析并生成
/archive-skill --name my-workflow       # 指定 skill 名称
/archive-skill --output ./skills/       # 指定输出目录
/archive-skill --template workflow      # 指定模板类型
/archive-skill --interactive            # 交互式确认
```

---

**一次成功对话，永久可用技能**
