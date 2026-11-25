---
name: refactor
description: 在用户指定文件或目录需要结构化重构时使用——支持文件模式和模块模式
---

# Refactor (重构)

对指定代码进行结构化重构，支持**文件模式**和**模块模式**。

**目标**：`$ARGUMENTS`

> 如果 `$ARGUMENTS` 为空，请提示用户提供目标文件或目录路径。

## 流程

```
检测类型 → ANALYZE → PLAN → [用户确认] → EXECUTE → VERIFY
```

## Step 0：检测目标类型

- **文件模式**：路径指向单个文件
- **模块模式**：路径指向目录

---

## 文件模式

### ANALYZE 阶段

1. 调用 `coding-standards` skill（重点：`references/api.md`、`references/react.md`、`references/typescript.md`）
2. 读取目标文件，统计行数
3. 代码异味检测（大组件 >200行、useState >5个、useEffect >3个、深嵌套 >4层）
4. 标准符合性检查（组件职责分离、提取 Hook 信号、API 规范）
5. 输出分析报告

### PLAN 阶段

- 分解为小步骤（每步 <50 行）
- **必须等待用户确认**

### EXECUTE 阶段

- 逐步执行，每步后验证变更文件 eslint
- 保持代码可编译

---

## 模块模式

### ANALYZE 阶段

1. 加载编码规范（同文件模式）
2. 目录结构扫描（文件列表、入口文件、总行数）
3. 依赖关系分析（内部依赖、外部依赖、循环依赖）
4. 逐文件异味检测，按严重度排序
5. 模块级问题识别（职责不清、缺少分层、导出混乱）
6. 输出模块分析报告

### PLAN 阶段

分阶段制定计划（基础设施 → 逐文件重构 → 清理），**必须等待用户确认**。

### EXECUTE 阶段

- 按 Phase 逐步执行
- 每个文件重构后验证 eslint
- 保持模块可用

---

## VERIFY 阶段（通用）

**只检查变更文件**：

```bash
CHANGED_FILES=$(git diff --name-only --diff-filter=AM | grep -E '\.(ts|tsx)$' | tr '\n' ' ')
npx eslint $CHANGED_FILES --fix
pnpm build
```

> 不要直接运行 `pnpm lint`，会格式化整个代码库。

## 关键规则

- 规划阶段**必须等待用户确认**后才能执行
- 文件模式：每步 <50 行
- 模块模式：每步 1 文件
- 不改变外部行为（纯重构）
- **不自动提交**——等待用户确认

## 下一步

VERIFY 通过后，建议运行：`/refactor-check`

详细指导参见 `refactor-workflow` skill。
