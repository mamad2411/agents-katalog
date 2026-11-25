---
name: executing-plans
description: 按 plan.md 逐任务执行实现。通过 Todo checkbox 追踪进度，每批改动后运行编译检查。触发短语："执行计划"、"按计划实现"、"开始实现"。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# /executing-plans — 执行实现计划

按照 plan.md 中的 Todo List 逐任务执行，确保每个改动可验证、可追踪。

## 前置条件

- 存在已批准的 plan.md（在 `docs/sdlc/` 下查找）
- 如果找不到 plan.md，建议用户先执行 /writing-plans
- 如果 plan.md 中没有 Todo List，先生成任务清单

## 流程

### 第一步：加载并审查计划

1. 读取 plan.md，理解整体方案和所有任务
2. 批判性审查：计划是否有遗漏、矛盾或过时的内容
3. 如果发现问题，向用户报告并等待确认后再继续

### 第二步：逐任务执行

按 Todo List 顺序执行每个任务：

1. 读取任务描述，理解预期改动
2. 读取相关源文件，理解现有实现
3. 执行改动
4. 在 plan.md 中将任务标记为 `[x]`

执行守卫：
- 不得中途停下求确认，直到所有任务完成
- 不得跳过任务或改变执行顺序（除非有技术依赖要求）
- 不得做计划之外的改动

### 第三步：编译检查

每完成一批相关改动后运行编译检查：

```bash
# 根据项目类型选择
tsc --noEmit                    # TypeScript
./gradlew compileJava           # Java/Gradle
cargo check                     # Rust
go build ./...                  # Go
python -m py_compile file.py    # Python
```

编译失败时立即修复，不继续下一个任务。

### 第四步：收尾验证

所有任务完成后：

1. 运行完整验证（格式化、编译、测试、构建）
2. 在 plan.md 末尾追加完成状态
3. 向用户报告完成情况

## 与子代理驱动开发的关系

本技能适用于：
- 小型改动（10 个以内的任务）
- 任务之间强依赖、无法并行的场景
- 不支持子代理的环境

大型改动建议使用 /subagent-driven-development，每个任务派遣独立子代理并行执行。
