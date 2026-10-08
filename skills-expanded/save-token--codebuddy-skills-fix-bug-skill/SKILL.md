---
name: fix-bug
description: 'Bug 修复流水线。当用户报告 Bug 或想要修复已知问题时使用。调用时需附带 Bug 描述或复现步骤。自动串联：Bug 分析 → 代码修复 → UT（委托 ut-writer SKILL）→ Lint 检查（委托 lint-check-fix Agent）→ 全量验证 → 提交代码。'
argument-hint: '[Bug 描述 / 复现步骤]'
---

# Bug 修复流水线

从 Bug 描述出发，自动完成：Bug 分析与定位 → 代码修复 → 单元测试补充 → Lint 检查修复 → 全量验证 → 提交代码。

---

## 流程总览

```
用户输入 Bug 描述
        |
        v
[阶段 1] Bug 分析与定位
        |
        v
  确认修复方案
        |
        v
[阶段 2] 代码修复
        |
        v
[阶段 3] 补充单元测试（委托 ut-writer SKILL）
        |
        v
[阶段 4] Lint 检查修复（委托 lint-check-fix Agent）
        |
        v
[阶段 5] 全量验证（build / lint / test:coverage，并行）
        |  ← 失败则修复代码并重新验证
        v
[阶段 6] 提交代码
        |
        v
  完成 ✓
```

---

## 步骤

### 阶段 1：Bug 分析与定位

1. **获取 Bug 信息**

   - 如果用户直接提供了 Bug 描述，直接使用
   - 如果未提供任何信息，使用 **AskUserQuestion tool** 询问：
     > "请描述您遇到的 Bug，包括复现步骤、期望行为和实际行为。"

2. **阅读项目上下文**

   阅读以下文件获取项目背景：
   - `CODEBUDDY.md` — 项目架构和开发规范

3. **分析 Bug 根因**

   使用 **Agent tool**（subagent_type=Explore）深入分析 Bug：
   - 根据 Bug 描述定位相关代码文件
   - 追踪数据流和调用链
   - 分析可能的根因
   - 检查是否有相关的已有测试覆盖该场景

4. **提出修复方案并确认**

   使用 **AskUserQuestion tool** 向用户展示分析结果并确认修复方案：
   - Bug 根因分析
   - 受影响的文件和模块
   - 修复方案（如有多种方案，列出各方案的优缺点）
   - 可能的影响范围

   等待用户确认修复方案后再继续。

### 阶段 2：代码修复

5. **创建任务列表**

   使用 **TaskCreate tool** 根据确认的修复方案创建详细的任务列表，将修复工作拆分为可跟踪的小任务。

6. **实现代码修复**

   按照任务列表逐一修复代码：
   - 使用 **Read tool** 阅读需要修改的文件
   - 使用 **Edit tool** 进行精确修改
   - 遵循项目编码规范（CODEBUDDY.md）
   - 每完成一个任务，使用 **TaskUpdate tool** 标记为完成

   注意：
   - 保持修改范围最小化，仅修复 Bug 本身，不做无关的重构
   - 确保修改不引入新的问题

### 阶段 3：补充单元测试

7. **委托 ut-writer SKILL 补充单元测试**

   使用 **Skill tool** 调用 `ut-writer` SKILL：

   ```
   Skill tool, skill: "ut-writer"
   ```

   ut-writer 会自动：
   - 评估当前覆盖率基线
   - 分析覆盖率缺口
   - 为 Bug 修复涉及的模块补充或增强测试
   - 循环「写测试 → 跑测试 → 修复失败」直到覆盖率达 60% 且全部通过

   等待 ut-writer 完成后再继续。

### 阶段 4：Lint 检查修复

8. **委托 lint-check-fix Agent 检查并修复 lint 错误**

   使用 **Agent tool**（subagent_type="lint-check-fix"）进行 lint 检查与修复：

   ```
   Agent tool, subagent_type: "lint-check-fix"
   prompt: "请对项目进行 lint 检查并自动修复所有可修复的问题。"
   ```

   lint-check-fix 会自动：
   - 执行 lint 检查
   - 分类问题（可自动修复 / 需手动修复 / 需用户确认）
   - 自动修复可修复的问题
   - 输出修复报告

   等待 lint-check-fix 完成后再继续。

### 阶段 5：全量验证

9. **并行运行 build、lint、测试**

   以下验证任务相互独立，**必须并行执行**（使用多个 Bash tool 并行调用）：

   ```bash
   pnpm build              # 构建
   pnpm lint               # Lint 检查
   pnpm test:coverage      # 测试 + 覆盖率
   ```

   收集全部结果后统一分析。如果任何一项失败，分析错误并修复代码/测试。

10. **验证循环**

    如果步骤 9 中任何一项失败：
    - 分析错误日志
    - 修复代码或测试
    - 重新并行运行全部验证（build / lint / test:coverage）
    - 最多重试 3 轮。如果 3 轮后仍有失败，暂停并报告问题，等待用户指导。

### 阶段 6：提交代码

11. **提交代码**

    仅在阶段 5 的所有验证步骤全部通过后才执行此步骤。

    - 使用 `git status` 和 `git diff` 查看所有变更
    - 使用 `git add` 添加相关文件（不要添加无关文件）
    - 使用 `git commit` 提交，commit message 格式：
      ```
      fix: <Bug 简述>

      <详细描述修复内容和根因>
      ```

---

## 完成时的输出

```
## Bug 修复完成

**Bug：** <Bug 简述>
**根因：** <根因分析>
**修复方案：** <方案简述>

### 修改的文件
- <文件列表及修改说明>

### 验证结果
- ✓ 构建通过（pnpm build）
- ✓ Lint 通过（pnpm lint）
- ✓ 测试通过（pnpm test:coverage）

### Git 信息
- commit: <commit hash>
- message: <commit message>

Bug 修复全流程已完成！
```

---

## 护栏

- **严格按阶段顺序执行**：每个阶段必须完成后才能进入下一阶段
- **修复方案必须经用户确认**：不得跳过用户确认直接修改代码
- **修改范围最小化**：仅修复 Bug 本身，不做无关重构或功能增强
- **UT 必须委托 ut-writer**：单元测试统一通过 ut-writer SKILL 补充
- **Lint 必须委托 lint-check-fix**：Lint 检查与修复统一通过 lint-check-fix Agent 处理
- **验证必须全部通过**：build、lint、test:coverage 全部通过后才能提交代码
- **失败时修复而非跳过**：验证失败时必须修复代码并重新验证
- **重试有上限**：验证循环最多 3 轮，超过后暂停等待用户指导
- **使用 Task tool 跟踪进度**：创建任务跟踪每个阶段的进度
- **遵循项目编码规范**：遵循 CODEBUDDY.md 中的约定
