---
name: writing-skills
description: 编写和优化 Claude Code 技能文件（SKILL.md）。使用 TDD 方法论确保技能质量。仅用户手动触发。
disable-model-invocation: true
argument-hint: [技能名称或描述]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# /writing-skills — 编写 Claude Code 技能

使用 TDD 方法论编写高质量的 SKILL.md 文件。

## SKILL.md 结构

每个技能文件必须包含：

### YAML Frontmatter

```yaml
---
name: skill-name
description: 一句话描述技能用途和触发条件。
disable-model-invocation: true/false
argument-hint: [可选参数说明]
allowed-tools: Tool1, Tool2, Tool3
---
```

字段说明：
- `name`：技能名称，小写字母加连字符
- `description`：Claude 用来判断是否匹配用户意图的关键字段。包含触发短语
- `disable-model-invocation`：true 表示只能手动触发，false 表示 AI 可自动匹配
- `allowed-tools`：技能执行时可使用的工具列表

### 正文结构

1. 标题（`# /name — 一句话描述`）
2. 核心原则或铁律（如有）
3. 流程步骤（编号清晰，每步有明确的输入和输出）
4. 约束和禁止行为（如有）

## 编写原则

### Claude 搜索优化（CSO）

description 字段是 AI 匹配技能的核心。好的 description：
- 包含用户可能使用的触发短语（中英文都要）
- 描述技能解决的问题，不仅仅是技能做什么
- 避免模糊的通用词汇

### Token 效率

- 避免冗长的解释，直接给指令
- 使用列表和代码块替代长段落
- 引用文件（references/）存放详细内容，SKILL.md 保持精简

### 流程设计

- 每个步骤应该是可验证的
- 步骤之间的转换条件要明确
- 有明确的完成标准

## TDD 流程

### 第一步：定义预期行为

列出技能应该响应的用户输入和预期的 AI 行为。

### 第二步：编写测试场景

为每个预期行为创建测试场景：

```
场景：用户说"[触发语句]"
预期：AI 执行 [具体行为]
验证：[如何确认行为正确]
```

### 第三步：编写 SKILL.md

根据测试场景编写技能文件。

### 第四步：使用子代理测试

使用 Agent 工具派遣子代理，模拟用户场景，验证技能行为。详见 `references/testing-skills-with-subagents.md`。

### 第五步：迭代优化

根据测试结果修改 SKILL.md，重复测试直到所有场景通过。

## 参考资料

- `references/anthropic-best-practices.md`：Anthropic 的技能编写最佳实践
- `references/testing-skills-with-subagents.md`：使用子代理测试技能的方法
