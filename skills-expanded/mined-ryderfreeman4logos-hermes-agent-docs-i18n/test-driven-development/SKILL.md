---
name: test-driven-development
description: "TDD: enforce RED-GREEN-REFACTOR, tests before code."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [testing, tdd, development, quality, red-green-refactor]
    related_skills: [systematic-debugging, subagent-driven-development]
---

# 测试驱动开发（TDD）

## 概述

首先编写测试用例，然后观察其失败。接着编写最简短的代码来让测试通过。

**核心原则：** 如果你没有亲眼看到测试失败，你就无法确定它是否在检测正确的内容。

**违背规则的字面要求，就等同于违背了规则的精神。**

## 适用场景

**始终适用的情况：**
- 新功能开发
- 错误修复
- 代码重构
- 行为变更

**例外情况（需先征得用户同意）：**
- 临时性原型设计
- 自动生成的代码
- 配置文件

有没有想过“就这一次跳过TDD”？请停下，那只是借口罢了。

## 不变法则

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

在编写测试之前先写代码？那就删掉它，重新开始。

**无一例外：**
- 不得将其保留作为“参考”
- 编写测试时不得对其进行“修改”
- 甚至不得查看它
- “删除”即意味着彻底清除

必须完全基于测试来实现功能，没有商量余地。

## 红绿重构循环

### RED — 编写失败的测试

编写一个最简的测试用例，用以描述预期会发生的情况。

**优秀的测试用例应满足：**
```python
def test_retries_failed_operations_3_times():
    attempts = 0
    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception('fail')
        return 'success'

    result = retry_operation(operation)

    assert result == 'success'
    assert attempts == 3
```
名称需清晰，且能真实测试行为，仅此而已。

**糟糕的测试示例：**
```python
def test_retry_works():
    mock = MagicMock()
    mock.side_effect = [Exception(), Exception(), 'success']
    result = retry_operation(mock)
    assert result == 'success'  # What about retry count? Timing?
```
名称模糊，测试使用的是模拟代码而非真实代码。

**要求：**
- 每个测试仅验证一种行为
- 名称需清晰具描述性（名称中包含“和”字时请拆分）
- 必须使用真实代码，不得使用模拟代码（确实无法避免的情况除外）
- 名称应描述行为本身，而非实现方式

### 验证 RED — 观察其失败过程

**此项为强制要求，绝不可跳过。**

```bash
# Use terminal tool to run the specific test
pytest tests/test_feature.py::test_specific_behavior -v
```

确认以下情况：
- 测试失败（并非因拼写错误导致的错误）
- 出现了预期的失败信息
- 失败原因是相关功能缺失

**测试立即通过？** 说明你正在测试现有行为。请修正该测试。

**测试出现错误？** 请先修复错误，然后重新运行，直到测试真正失败为止。

### 绿色状态 — 最小化代码量

只需编写最简的代码即可让测试通过，无需更多内容。

**良好：**
```python
def add(a, b):
    return a + b  # Nothing extra
```

**错误：**
```python
def add(a, b):
    result = a + b
    logging.info(f"Adding {a} + {b} = {result}")  # Extra!
    return result
```

不得添加新功能，也不得重构其他代码或进行超出测试范围的“改进”。

在 **GREEN** 模式下，以下行为属于作弊行为，是被允许的：
- 硬编码返回值
- 直接复制粘贴
- 重复代码
- 跳过边界情况处理

我们会在 **REFACTOR** 模式中修复这些问题。

### 验证 **GREEN** 状态——观察其通过测试

**此项为强制要求。**

```bash
# Run the specific test
pytest tests/test_feature.py::test_specific_behavior -v

# Then run ALL tests to check for regressions
pytest tests/ -q
```

确认以下内容：
- 测试通过
- 其他测试仍通过
- 输出结果完好（无错误、无警告）

**测试失败了？** 修正代码，而非测试本身。

**其他测试失败了？** 立即修复回归问题。

### 重构 —— 清理优化

仅在所有测试通过后执行：
- 删除重复代码
- 优化变量命名
- 提取辅助函数
- 简化表达式

始终确保测试保持通过状态，切勿新增功能逻辑。

**如果在重构过程中测试失败：** 立即回退，采取更小的改进步骤。

### 重复迭代

针对下一个功能点处理下一个失败的测试，一次完成一个循环。

## 避免横向切割

切勿先编写所有测试再实现全部功能。这就是所谓的横向切割：红色状态变成了“编写一堆假设性的测试”，绿色状态则变成了“让这些测试全部通过”。由于在实现代码之前就设计了测试，而代码本身尚未揭示哪些功能行为和接口真正重要，因此这种方式会导致测试变得脆弱。

建议改用纵向逐步实现的方式：

```text
WRONG:
  RED:   test1, test2, test3, test4
  GREEN: impl1, impl2, impl3, impl4

RIGHT:
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

追踪弹是一种端到端的行为切片。它能够验证路径是否正常，帮助你了解接口功能，同时让后续的每一项测试都建立在刚刚学到的知识基础上。

## 顺序为何重要

**“我稍后会写测试来验证功能是否正常”**

在代码通过后才编写的测试往往能立即通过。但这种立即通过的情况并不能证明什么：
- 可能测试的内容有误
- 可能测试的是实现细节而非实际行为
- 可能遗漏了某些边缘情况
- 你根本看不到它是否能捕获错误

采用测试优先的方法，能迫使你面对测试失败的情况，从而确认测试确实针对了某个具体内容。

**“我已经手动测试过所有边缘情况了”**

手动测试具有随意性。你可能以为已经测试了一切，但实际上：
- 没有记录测试的内容
- 代码变更时无法重新运行测试
- 在压力之下容易忘记某些测试用例
- “我当时试的时候它能正常工作”并不等同于测试全面

自动化测试则具有系统性，每次都会以相同的方式运行。

**“删除数小时的工作成果太浪费了”**

这是沉没成本谬误。那些时间已经耗尽。你现在可以选择：
- 删除这些代码，并通过测试驱动开发重新编写（可靠性高）
- 保留现有代码，之后再补充测试（可靠性低，很可能会出现错误）

真正的“浪费”在于保留那些不可靠的代码。

**“测试驱动开发过于死板，务实意味着要灵活调整”**

测试驱动开发恰恰是最务实的做法：
- 在提交代码前就发现错误（比事后调试更快）
- 防止功能退化（测试能立即捕捉到异常）
- 记录代码行为（测试展示了如何使用代码）
- 支持代码重构（可自由修改代码，测试会及时发现问题）

所谓的“务实”捷径，其实只会带来生产环境中的调试工作，反而效率更低。

**“事后测试只是实现目标的一种手段——它是精神而非仪式。”**

事后测试回答的是“它实现了什么？”而先测法则追问“它应该实现什么？”

事后测试容易受到实际实现方式的制约。你测试的只是自己编写的代码，而非真正需要验证的功能。而先测法则要求在实现之前就发现各种边界情况。

## 常见的借口

| 借口 | 实际情况 |
|------|----------|
| “太简单了，没必要测试” | 简单的代码也可能会出错。测试只需30秒而已。 |
| “我之后再测试” | 即使测试立即通过，也无法证明什么。 |
| “事后测试也能达到相同目的” | 事后测试 = “它实现了什么？”；先测法 = “它应该实现什么？” |
| “已经手动测试过了” | 临时测试 ≠ 系统化测试。没有记录，就无法重复执行。 |
| “删除代码会浪费时间” | 这是沉没成本谬误。保留未经验证的代码其实就是在积累技术债务。 |
| “先保留作为参考，再写测试” | 你最终还是会修改代码。那不还是事后测试吗？该删就删。 |
| “需要先探索一下” | 没问题。那就放弃探索，直接从TDD开始吧。 |
| “测试困难意味着设计不清晰” | 要倾听测试的反馈。难以测试的代码，其使用体验也会很差。 |
| “TDD会降低效率” | TDD实际上比调试更快。务实的做法就是先测法。 |
| “手动测试更快” | 手动测试无法覆盖边界情况。每次修改后都得重新测试。 |
| “现有代码没有测试用例” | 你正在改进它。只需为你修改的代码添加测试即可。 |

## 危险信号——立即停止，重新开始

如果你发现自己有以上任何行为，那就删除相关代码，重新从TDD开始吧：

- 先写代码，再测试  
- 实现功能后再进行测试  
- 第一次运行测试就直接通过  
- 无法解释测试失败的原因  
- “稍后再添加测试”  
- 以“就这一次”为借口  
- “我已经手动测试过了”  
- “实现功能后的测试也能达到相同目的”  
- “留作参考”或“直接修改现有代码”  
- “已经花了X小时，删除太浪费了”  
- “TDD太死板，我要务实一点”  
- “这个情况不同，因为……”  

**以上所有情况都意味着：删除代码，重新从TDD开始。**  

## 验证检查清单  

在标记任务完成之前，请确认：  
- [ ] 每个新函数/方法都有对应的测试  
- [ ] 在实现功能前已观察过每个测试的失败情况  
- [ ] 每个测试失败的原因都是预期的（如功能缺失，而非拼写错误）  
- [ ] 为通过每个测试而编写了最简化的代码  
- [ ] 所有测试均通过  
- [ ] 输出结果完整无缺（无错误、无警告）  
- [ ] 测试使用的是真实代码（仅在不可避免时才使用模拟对象）  
- [ ] 已覆盖所有边界情况和异常情况  

如果无法勾选所有选项，说明你跳过了TDD流程，需要重新开始。  

## 遇到难题时  

| 问题 | 解决方案 |
|---------|----------|
| 不知道如何编写测试 | 先设计所需的API，先写出断言逻辑，或向用户咨询。 |
| 测试过于复杂 | 接口设计过于复杂，需简化接口。 |
| 必须对所有内容进行模拟 | 代码耦合度过高，应使用依赖注入技术。 |
| 测试环境配置过于繁琐 | 提取辅助函数，如果仍然复杂，则需简化设计。 |

## Hermes Agent集成  

### 运行测试  

可在每个步骤中使用`terminal`工具来运行测试：

```python
# RED — verify failure
terminal("pytest tests/test_feature.py::test_name -v")

# GREEN — verify pass
terminal("pytest tests/test_feature.py::test_name -v")

# Full suite — verify no regressions
terminal("pytest tests/ -q")
```

### 使用 delegate_task 功能时

在派发子智能体执行任务时，需在目标设定中强制执行测试驱动开发原则：

```python
delegate_task(
    goal="Implement [feature] using strict TDD",
    context="""
    Follow test-driven-development skill:
    1. Write failing test FIRST
    2. Run test to verify it fails
    3. Write minimal code to pass
    4. Run test to verify it passes
    5. Refactor if needed
    6. Commit

    Project test command: pytest tests/ -q
    Project structure: [describe relevant files]
    """,
    toolsets=['terminal', 'file']
)
```

### 系统化调试方法

发现了错误？请编写能够复现该问题的失败测试，然后遵循测试驱动开发（TDD）流程。测试不仅可用于验证修复方案的有效性，还能防止问题再次出现。

绝不要在没有测试的情况下直接修复错误。

## 常见的测试反模式

- **仅测试模拟行为而非真实行为**——模拟对象的作用应是验证系统间的交互，而非替代被测系统本身
- **过度关注实现细节**——应测试系统的行为或输出结果，而非内部方法调用
- **仅覆盖正常流程**——务必同时测试边界情况、异常场景以及极端条件
- **脆弱性过高的测试**——测试应用于验证功能行为，而非代码结构；重构不应导致这些测试失效

## 最终准则

```
Production code → test exists and failed first
Otherwise → not TDD
```

未经用户明确许可，不得抛出任何异常。
