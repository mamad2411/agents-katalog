---
name: subagent-driven-development
description: "Execute plans via delegate_task subagents (2-stage review)."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegation, subagent, implementation, workflow, parallel]
    related_skills: [requesting-code-review, test-driven-development]
---

# 子代理驱动开发

## 概述

通过为每个任务分配全新的子代理，并结合系统化的两阶段审核机制来执行实施计划。

**核心原则：** 为每个任务配备全新子代理 + 两阶段审核（先审核需求规范，再审核质量）= 高质量成果与快速迭代。

## 适用场景

在以下情况下可使用此功能：
- 已有实施计划（来自 `plan` 功能或用户需求）
- 任务大多相互独立
- 对质量及需求合规性要求较高
- 希望在任务之间实现自动审核

**与手动执行的对比：**
- 每个任务拥有独立的上下文环境（避免因历史状态积累导致的混乱）
- 自动审核流程可及早发现问题
- 所有任务均能接受一致的质量检查
- 子代理可在开始工作前提出疑问

## 实施流程

### 1. 读取并解析计划

读取计划文件，一次性提取所有任务及其完整文本和上下文信息。随后生成待办清单：

```python
# Read the plan
read_file("docs/plans/feature-plan.md")

# Create todo list with all tasks
todo([
    {"id": "task-1", "content": "Create User model with email field", "status": "pending"},
    {"id": "task-2", "content": "Add password hashing utility", "status": "pending"},
    {"id": "task-3", "content": "Create login endpoint", "status": "pending"},
])
```

**关键点：** 仅需阅读计划内容一次，并提取所有相关信息。切勿让子智能体去读取计划文件——应直接在上下文中提供完整的任务文本。

### 2. 单项任务处理流程

针对计划中的每一项任务：

#### 第一步：派遣执行子智能体

使用 `delegate_task` 函数，并传入完整的上下文信息：

```python
delegate_task(
    goal="Implement Task 1: Create User model with email and password_hash fields",
    context="""
    TASK FROM PLAN:
    - Create: src/models/user.py
    - Add User class with email (str) and password_hash (str) fields
    - Use bcrypt for password hashing
    - Include __repr__ for debugging

    FOLLOW TDD:
    1. Write failing test in tests/models/test_user.py
    2. Run: pytest tests/models/test_user.py -v (verify FAIL)
    3. Write minimal implementation
    4. Run: pytest tests/models/test_user.py -v (verify PASS)
    5. Run: pytest tests/ -q (verify no regressions)
    6. Commit: git add -A && git commit -m "feat: add User model with password hashing"

    PROJECT CONTEXT:
    - Python 3.11, Flask app in src/app.py
    - Existing models in src/models/
    - Tests use pytest, run from project root
    - bcrypt already in requirements.txt
    """,
    toolsets=['terminal', 'file']
)
```

#### 第2步：派遣规范合规性审查员

在实施人员完成相关工作后，需根据原始规范进行核查：

```python
delegate_task(
    goal="Review if implementation matches the spec from the plan",
    context="""
    ORIGINAL TASK SPEC:
    - Create src/models/user.py with User class
    - Fields: email (str), password_hash (str)
    - Use bcrypt for password hashing
    - Include __repr__

    CHECK:
    - [ ] All requirements from spec implemented?
    - [ ] File paths match spec?
    - [ ] Function signatures match spec?
    - [ ] Behavior matches expected?
    - [ ] Nothing extra added (no scope creep)?

    OUTPUT: PASS or list of specific spec gaps to fix.
    """,
    toolsets=['file']
)
```

**如发现规范问题：** 填补缺失项，然后重新运行规范审查。只有在符合规范要求后才能继续。

#### 第3步：派发代码质量审查员

在通过规范审查后：

```python
delegate_task(
    goal="Review code quality for Task 1 implementation",
    context="""
    FILES TO REVIEW:
    - src/models/user.py
    - tests/models/test_user.py

    CHECK:
    - [ ] Follows project conventions and style?
    - [ ] Proper error handling?
    - [ ] Clear variable/function names?
    - [ ] Adequate test coverage?
    - [ ] No obvious bugs or missed edge cases?
    - [ ] No security issues?

    OUTPUT FORMAT:
    - Critical Issues: [must fix before proceeding]
    - Important Issues: [should fix]
    - Minor Issues: [optional]
    - Verdict: APPROVED or REQUEST_CHANGES
    """,
    toolsets=['file']
)
```

**如发现质量问题：** 需先修复问题并重新审核。只有获得批准后才能继续下一步。

#### 第4步：标记为已完成

```python
todo([{"id": "task-1", "content": "Create User model with email field", "status": "completed"}], merge=True)
```

### 3. 最终审核

在所有任务均完成之后，需指派一名最终集成审核员进行核查：

```python
delegate_task(
    goal="Review the entire implementation for consistency and integration issues",
    context="""
    All tasks from the plan are complete. Review the full implementation:
    - Do all components work together?
    - Any inconsistencies between tasks?
    - All tests passing?
    - Ready for merge?
    """,
    toolsets=['terminal', 'file']
)
```

### 4. 验证并提交

```bash
# Run full test suite
pytest tests/ -q

# Review all changes
git diff --stat

# Final commit if needed
git add -A && git commit -m "feat: complete [feature name] implementation"
```

## 任务粒度

**每个任务 = 2–5分钟的专注工作时间。**

**任务过大：**
- “实现用户认证系统”

**任务规模适中：**
- “创建包含邮箱和密码字段的用户模型”
- “添加密码哈希功能”
- “创建登录接口”
- “实现JWT令牌生成功能”
- “创建注册接口”

## 需避免的错误做法

- 未制定计划便开始开发
- 跳过审查环节（无论是规范合规性还是代码质量检查）
- 在关键/重要问题未解决的情况下继续推进
- 对涉及同一文件的多个任务分配多个子代理同时处理
- 要求子代理阅读计划文件（应在上下文中直接提供完整内容）
- 忽略任务背景说明（子代理需要了解该任务在整个项目中的定位）
- 不回应子代理的疑问（应在其继续工作前给予解答）
- 对规范合规性仅满足“勉强合格”便予以接受
- 跳过审查循环（审查者发现问题 → 开发者修复 → 再次审查）
- 用开发者自行审查替代正式审查（两者都是必要的）
- **在规范合规性尚未通过时就开始代码质量审查**（顺序错误）
- 在任何一项审查仍有未解决问题时便进入下一个任务

## 问题处理方式

### 当子代理提出疑问时

- 清晰完整地予以解答
- 如有需要，提供更多背景信息
- 不要催促其立即开始开发

### 当审查者发现问题时

- 由负责开发的子代理（或新的子代理）进行修复
- 审查者再次进行检查
- 重复此过程直至问题得到解决
- 绝对不能跳过重新审查环节

### 当子代理无法完成任务时

- 派遣一个新的修复子代理，并明确告知出现问题的具体原因  
- 不要在控制器会话中尝试手动修复（以避免上下文污染）  

## 效率优化建议

**为何每个任务需使用新的子代理：**  
- 避免因累积状态导致的上下文污染  
- 每个子代理都能拥有清晰、专注的上下文  
- 减少之前任务代码或推理逻辑带来的混淆  

**为何采用两阶段审查机制：**  
- 规范审查阶段可及早发现功能实现不足或过度设计的问题  
- 质量审查阶段能确保代码实现质量达标  
- 在问题在不同任务间扩散之前将其及时发现  

**成本与收益的权衡：**  
- 需调用更多子代理（每个任务需1名实现者 + 2名审查者）  
- 但能及早发现问题（比日后修复复杂问题更为经济）  

## 与其他技能的集成方式

### 与 `plan` 技能的集成  

该技能用于执行由 `plan` 技能生成的计划：  
1. 用户需求 → 计划方案 → 具体实现计划  
2. 实现计划 → 子代理驱动开发 → 可运行的代码  

### 与测试驱动开发（TDD）的集成  

实现者子代理应遵循TDD流程：  
1. 先编写无法通过的测试用例  
2. 编写最简化的代码实现  
3. 验证测试是否通过  
4. 提交代码  

需在每个实现者的上下文中包含TDD相关指导。  

### 与“请求代码审查”技能的集成  

两阶段审查机制本身即构成代码审查流程。对于最终集成阶段的审查，可使用“请求代码审查”技能所提供的审查维度。  

### 与系统化调试技能的集成  

若子代理在实现过程中遇到错误：  
1. 依照系统化调试流程处理  
2. 在修复前找出根本原因  
3. 编写回归测试用例  
4. 继续进行代码实现
## 示例工作流程

```
[Read plan: docs/plans/auth-feature.md]
[Create todo list with 5 tasks]

--- Task 1: Create User model ---
[Dispatch implementer subagent]
  Implementer: "Should email be unique?"
  You: "Yes, email must be unique"
  Implementer: Implemented, 3/3 tests passing, committed.

[Dispatch spec reviewer]
  Spec reviewer: ✅ PASS — all requirements met

[Dispatch quality reviewer]
  Quality reviewer: ✅ APPROVED — clean code, good tests

[Mark Task 1 complete]

--- Task 2: Password hashing ---
[Dispatch implementer subagent]
  Implementer: No questions, implemented, 5/5 tests passing.

[Dispatch spec reviewer]
  Spec reviewer: ❌ Missing: password strength validation (spec says "min 8 chars")

[Implementer fixes]
  Implementer: Added validation, 7/7 tests passing.

[Dispatch spec reviewer again]
  Spec reviewer: ✅ PASS

[Dispatch quality reviewer]
  Quality reviewer: Important: Magic number 8, extract to constant
  Implementer: Extracted MIN_PASSWORD_LENGTH constant
  Quality reviewer: ✅ APPROVED

[Mark Task 2 complete]

... (continue for all tasks)

[After all tasks: dispatch final integration reviewer]
[Run full test suite: all passing]
[Done!]
```

## 请记住

```
Fresh subagent per task
Two-stage review every time
Spec compliance FIRST
Code quality SECOND
Never skip reviews
Catch issues early
```

**卓越的品质绝非偶然，而是系统化流程的必然结果。**

## 进一步阅读（相关时加载）

当任务编排涉及大量上下文使用、漫长的审核循环或复杂的验证检查点时，请加载以下针对特定领域的参考文档：

- **`references/context-budget-discipline.md`** — 四级上下文质量衰退模型（PEAK / GOOD / DEGRADING / POOR）、随上下文窗口大小变化的阅读深度规则，以及上下文质量隐性下降的早期预警信号。当任务显然会消耗大量上下文时（如多阶段计划、多个子智能体、大型输出结果），请加载此文档。
- **`references/gates-taxonomy.md`** — 四种标准关卡类型（预检、修订、升级处理、中止），包括其运作机制、恢复策略及实际案例。在设计或审核任何包含验证检查点的工作流时，请加载此文档——明确使用相关术语，以便为每个关卡定义明确的触发条件、失败处理方式及恢复规则。

以上两篇参考文档改编自 gsd-build/get-shit-done（MIT © 2025 Lex Christopherson）。
