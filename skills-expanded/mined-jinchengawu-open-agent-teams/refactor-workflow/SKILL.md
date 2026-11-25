---
name: refactor-workflow
description: 代码重构工作流程和模式。在进行组件拆分、hooks 提取、模块重组等重构任务时激活。提供标准流程（分析→规划→执行→验证）和常用重构模式。
---

# 重构工作流

## 标准流程

```
检测类型 → ANALYZE → PLAN → [用户确认] → EXECUTE → VERIFY → [/refactor-check]
```

| 阶段    | 输出     | 关键动作                  |
| ------- | -------- | ------------------------- |
| ANALYZE | 分析报告 | 代码异味 + 标准符合性检查 |
| PLAN    | 重构计划 | 分解步骤、**等待确认**    |
| EXECUTE | 代码变更 | 小步修改、每步验证        |
| VERIFY  | 验证报告 | eslint/build/test         |

## 两种模式

| 维度     | 文件模式         | 模块模式                     |
| -------- | ---------------- | ---------------------------- |
| 输入     | 单个文件路径     | 目录路径                     |
| 分析     | 单文件代码异味   | 目录结构 + 依赖 + 逐文件异味 |
| 步骤粒度 | 行级（<50行/步） | 文件级（1文件/步）           |
| 输出     | 单文件优化       | 可能涉及文件拆分/移动/新建   |

## 核心原则

| 原则           | 说明                             |
| -------------- | -------------------------------- |
| **等待确认**   | 规划阶段必须等用户确认后才执行   |
| **小步修改**   | 文件模式 <50 行，模块模式 1 文件 |
| **保持可用**   | 每步后代码必须可编译             |
| **不改行为**   | 纯重构不改变外部行为             |
| **不自动提交** | 重构完成后等待用户确认再提交     |

## ANALYZE 阶段

**首先必须加载编码规范**：

- 调用 `coding-standards` skill，或读取 `.cursor/skills/coding-standards/` 下所有规范文件
- 重点：`references/api.md`、`references/react.md`、`references/typescript.md`

然后根据模式执行分析：

- **文件模式**：[references/analysis.md](references/analysis.md)
- **模块模式**：[references/module-analysis.md](references/module-analysis.md)

## 详细参考

- **文件分析**: [references/analysis.md](references/analysis.md) - 单文件代码异味检查
- **模块分析**: [references/module-analysis.md](references/module-analysis.md) - 目录结构 + 依赖分析
- **重构模式**: [references/patterns.md](references/patterns.md) - 组件拆分、提取 hooks 等
- **技术验证**: [references/validation.md](references/validation.md) - eslint/build/test 检查项

## 下一步

重构完成后（代码未提交），运行：

```bash
/refactor-check
```

校验业务逻辑是否保持不变，参见 `refactor-check` skill。

## 快速参考

### 重构信号

**文件级（需要拆分/提取）**：

- 超过 200 行
- 超过 5 个 useState
- 多个 useEffect 处理相关逻辑

**模块级（需要重组）**：

- 单文件超过 500 行
- 缺少 hooks/types 分层
- 循环依赖

### 验证命令

**重要：只检查变更文件，避免格式化整个代码库**

```bash
# 获取变更文件
CHANGED_FILES=$(git diff --name-only --diff-filter=AM | grep -E '\.(ts|tsx)$' | tr '\n' ' ')

# 只对变更文件运行 eslint（不要直接运行 pnpm lint）
npx eslint $CHANGED_FILES --fix

# 完成后运行 build/test
pnpm build
pnpm test      # 如有测试
```

> 不要直接运行 `pnpm lint`，它会格式化整个代码库，产生大量无关变更。
