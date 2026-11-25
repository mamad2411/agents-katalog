---
name: plan
description: Write a markdown plan to .hermes/plans/; no execution.
version: 2.0.0
author: Hermes Agent (writing-craft adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [planning, plan-mode, implementation, workflow, design, documentation]
    related_skills: [subagent-driven-development, test-driven-development, requesting-code-review]
---

# 计划模式

当用户需要制定计划而非直接执行任务时，可使用此技能。

## 核心行为

在本轮对话中，您仅负责制定计划。
- 不要编写代码。
- 除计划相关的 Markdown 文件外，不得修改项目文件。
- 不要运行会修改数据的终端命令、执行提交、推送操作或进行任何外部操作。
- 如有需要，可使用只读命令/工具查看代码库或其他相关内容。
- 您的输出应是一个保存在当前工作空间下的 `.hermes/plans/` 目录中的 Markdown 计划文件。

## 输出要求

需编写一份具体且可操作的 Markdown 计划。如适用，请包含以下内容：
- 目标
- 当前上下文/假设条件
- 建议的解决方案
- 分步执行计划
- 可能会被修改的文件
- 测试/验证方案
- 风险、权衡因素及未解决的问题

如果任务与代码相关，还需注明具体的文件路径、可能的测试目标以及验证步骤。

## 保存位置

使用 `write_file` 函数将计划保存至以下路径：
- `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md`

该路径是相对于当前工作目录/后端工作空间而言的。Hermes 的文件工具具备后端感知能力，因此使用此相对路径可确保计划在本地、Docker、SSH、Modal 以及 Daytona 等各类后端环境中都与工作空间保持同步。

如果运行环境指定了特定目标路径，则直接使用该路径；
若未指定，则需在 `.hermes/plans/` 目录下自行创建一个包含合理时间戳的文件名。

## 交互方式

- 若请求足够明确，可直接编写计划。
- 若仅输入 `/plan` 而无明确指令，可从当前对话上下文中推断任务内容。
- 若信息确实不足，应提出简短的澄清问题而非自行猜测。
- 计划保存完成后，简要回复说明所制定的计划内容及保存路径。

---

# 如何撰写优质的计划

本技能的后续内容将介绍如何编写一份*优质*的实施计划——即上述 Markdown 文件中所包含的内容。

## 概述

在编写实施计划时，应假设执行者对代码库一无所知且审美标准不高。需详细记录所有相关信息：需要修改的文件、完整代码、测试命令、需查阅的文档以及验证方法。同时要将任务拆分为小块，遵循 DRY、YAGNI、TDD 原则，并频繁提交代码。

假设执行者是技术娴熟的开发者，但对相关工具集或问题领域几乎不了解，且不擅长设计良好的测试用例。

**核心原则：** 一份好的计划能让实现过程一目了然。如果需要猜测，说明该计划还不够完善。

## 何时需要完整的实施计划

**以下情况务必提前制定计划：**
- 实现多步骤功能
- 拆分复杂需求
- 通过子代理驱动开发将任务分配给其他子代理

**以下情况不可省略计划：**
- 功能看似简单（但假设条件可能导致错误）
- 您打算亲自实现该功能（未来的自己需要指导）
- 独自工作时（文档至关重要）

## 任务的分块粒度

**每个任务应对应 2-5 分钟的专注工作时间。**

每一步都应是单一动作：
- “编写失败的测试用例” —— 一步
- “运行测试以确保其确实失败” —— 一步
- “编写最简代码使测试通过” —— 一步
- “运行测试并确认其全部通过” —— 一步
- “提交代码” —— 一步

**任务过大则不可行：**
```markdown
### Task 1: Build authentication system
[50 lines of code across 5 files]
```

**合适规模：**
```markdown
### Task 1: Create User model with email field
[10 lines, 1 file]

### Task 2: Add password hash field to User
[8 lines, 1 file]

### Task 3: Create password hashing utility
[15 lines, 1 file]
```

## 计划文档结构

### 标题（必填）

每个计划都必须以以下内容开头：

```markdown
# [Feature Name] Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

### 任务结构

每个任务均遵循以下格式：

````markdown
### Task N: [Descriptive Name]

**Objective:** What this task accomplishes (one sentence)

**Files:**
- Create: `exact/path/to/new_file.py`
- Modify: `exact/path/to/existing.py:45-67` (line numbers if known)
- Test: `tests/path/to/test_file.py`

**Step 1: Write failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify failure**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: FAIL — "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify pass**

Run: `pytest tests/path/test.py::test_specific_behavior -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## 开发流程

### 第一步：理解需求

仔细阅读并掌握以下内容：
- 功能需求
- 设计文档或用户需求描述
- 验收标准
- 各种限制条件

### 第二步：探索代码库

利用 Hermes 工具来深入了解项目结构：

```python
# Understand project structure
search_files("*.py", target="files", path="src/")

# Look at similar features
search_files("similar_pattern", path="src/", file_glob="*.py")

# Check existing tests
search_files("*.py", target="files", path="tests/")

# Read key files
read_file("src/app.py")
```

### 第3步：设计思路

需要确定以下内容：
- 架构模式
- 文件组织结构
- 所需依赖项
- 测试策略

### 第4步：编写任务

按顺序创建任务：
1. 基础设施搭建
2. 核心功能实现（每个功能均采用TDD测试驱动开发）
3. 边界情况处理
4. 系统集成
5. 代码清理与文档编写

### 第5步：补充完整细节

针对每一项任务，需包含以下内容：
- **精确的文件路径**（而非“配置文件”，而应是 `src/config/settings.py` 这样的具体路径）
- **完整的代码示例**（而非仅说明“添加验证逻辑”，而是提供实际代码）
- 带有预期输出结果的**确切命令**
- 能证明该任务已正常运行的**验证步骤**

### 第6步：审查计划

需检查以下要点：
- [ ] 任务顺序合理且逻辑清晰
- [ ] 每项任务的耗时控制在2-5分钟范围内
- [ ] 文件路径准确无误
- [ ] 代码示例完整，可直接复制使用
- [ ] 命令及预期输出均准确无误
- [ ] 未遗漏任何相关背景信息
- [ ] 已遵循DRY、YAGNI及TDD设计原则

## 设计原则

### DRY原则（避免重复代码）

**错误做法：** 在多个地方重复编写相同的验证逻辑  
**正确做法：** 将验证功能提取为独立函数，然后在各处统一调用

### YAGNI原则（不要过早实现）

**错误做法：** 为未来的需求预留“灵活性”接口  
**正确做法：** 仅实现当前真正需要的功能

```python
# Bad — YAGNI violation
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.preferences = {}  # Not needed yet!
        self.metadata = {}     # Not needed yet!

# Good — YAGNI
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

### TDD（测试驱动开发）

凡是生成代码的任务都应遵循完整的 TDD 开发流程：
1. 编写失败的测试用例
2. 运行测试以确认确实失败
3. 编写最简化的代码
4. 运行测试以确认测试通过

详情请参阅 `test-driven-development` 技能文档。

### 频繁提交代码

完成每个任务后都应进行代码提交：
```bash
git add [files]
git commit -m "type: description"
```

## 常见错误

### 任务描述模糊

**错误示例：** “添加认证功能”
**正确示例：** “创建包含 email 和 password_hash 字段的 User 模型”

### 代码不完整

**错误示例：** “第一步：添加验证函数”
**正确示例：** “第一步：添加验证函数”，随后需附上完整的函数代码

### 缺少验证步骤

**错误示例：** “第三步：测试功能是否正常”
**正确示例：** “第三步：运行 `pytest tests/test_auth.py -v`，预期结果为：3 个测试通过”

### 缺少文件路径说明

**错误示例：** “创建模型文件”
**正确示例：** “创建文件：`src/models/user.py`”

## 执行流程交接

保存计划后，需明确说明执行方案：

**“计划已完整保存。现在将采用子代理驱动开发模式进行执行——我会为每个任务分配一个全新的子代理，并进行两阶段审核（首先是规范合规性检查，其次是代码质量检查）。是否继续执行？”**

在执行过程中，请使用 `subagent-driven-development` 技能：
- 为每个任务分配包含完整上下文的独立 `delegate_task` 对象
- 每个任务完成后进行规范合规性检查
- 规范检查通过后再进行代码质量检查
- 仅当两阶段审核均通过后才继续执行

## 请记住

```
Bite-sized tasks (2-5 min each)
Exact file paths
Complete code (copy-pasteable)
Exact commands with expected output
Verification steps
DRY, YAGNI, TDD
Frequent commits
```

一个完善的规划能让实施过程变得清晰明了。
