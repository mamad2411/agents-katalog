---
name: writing-plans
description: 当你有规格文档或需求，准备开始多步骤任务时使用。写出详细的逐任务实现计划。触发词：写计划、实现计划、开始实现、how to implement、implementation plan。
agent_created: true
---

# 编写实现计划

写出完整的实现计划，假设执行者对代码库一无所知。文档化他们需要知道的一切：每个任务涉及哪些文件、代码、测试、参考文档、验证方法。

**开始时声明：** "我将用 writing-plans 技能创建实现计划。"

## 计划文件位置

`docs/plans/YYYY-MM-DD-<功能名>.md`

## 任务粒度

**每个步骤一个动作（2-5 分钟）：**

```markdown
### 任务 N: [组件名]

**文件:**
- 创建: `exact/path/to/file.py`
- 修改: `exact/path/to/existing.py:123-145`
- 测试: `tests/exact/path/to/test.py`

- [ ] **步骤 1: 写失败测试**
```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **步骤 2: 运行测试确认失败**
命令: `pytest tests/path/test.py::test_name -v`
预期: FAIL — "function not defined"

- [ ] **步骤 3: 写最小实现**
```python
def function(input):
    return expected
```

- [ ] **步骤 4: 运行测试确认通过**
命令: `pytest tests/path/test.py::test_name -v`
预期: PASS

- [ ] **步骤 5: 提交**
```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## 红线（绝对禁止的占位符）

- "TBD"、"TODO"、"稍后实现"、"自行填充"
- "添加适当的错误处理"、"添加验证"、"处理边界情况"（不写具体代码）
- "为以上写测试"（不写具体测试代码）
- "类似任务 N"（重复代码——执行者可能乱序阅读）
- 引用了任务中未定义的类型、函数或方法

## 计划文档头部模板

```markdown
# [功能名称] 实现计划

> **对执行者:** 全程使用 TDD。先写失败测试，看它失败，再实现。

**目标:** [一句话描述要构建什么]
**架构:** [2-3 句方案说明]
**技术栈:** [关键技术/库]
```

## 计划审查

写完计划后自检：

1. **规格覆盖** — 规格中的每个需求都有对应任务吗？列出遗漏项
2. **占位符扫描** — 搜索红线中的禁用模式，修复
3. **类型一致性** — 后续任务中的类型、方法签名、属性名和前面定义的一致吗？

发现问题就地修复。

## 执行移交

计划保存后，提供两个选项：

> "计划已完成，保存到 `docs/plans/<文件名>.md`。两种执行方式："
>
> **1. 子代理驱动（推荐）** — 每个任务派一个全新子代理，任务间做审查
> **2. 内联执行** — 在当前会话中用 executing-plans 逐任务执行
>
> "选哪个？"

- 选子代理驱动 → 调 `subagent-driven-development`
- 选内联执行 → 调 `executing-plans`

## 关键规则

- 始终使用精确的文件路径
- 每个步骤包含完整代码——不是"在此添加验证"
- 精确命令+预期输出
- DRY、YAGNI、TDD、每个绿色测试后提交
