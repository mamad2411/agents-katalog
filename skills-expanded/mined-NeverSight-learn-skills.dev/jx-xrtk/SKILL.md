---
name: jx-xrtk
description: |
  AI 接手工作 - 读取交接文档，理解上下文，继续开发。
  当用户要接手之前的工作、继续开发、或"新人填坑"时使用。
  触发词："/jx-xrtk"、"接手工作"、"新人填坑"、"继续开发"、"xrtk"
triggers:
  - jx-xrtk
  - 接手工作
  - 新人填坑
  - 继续开发
  - xrtk
allowed-tools:
  - Bash
  - Read
  - Glob
  - AskUserQuestion
---

# /jx-xrtk - 接手工作

读取交接文档，验证状态，生成理解规划。

## 工作流程

### Step 1: 扫描交接文档

```bash
HANDOVER_DIR="$(pwd)/.jx_skill/handover"

if [ -d "$HANDOVER_DIR" ]; then
  ls -t "$HANDOVER_DIR"/time_*.md 2>/dev/null | head -10
else
  echo "NO_HANDOVER"
fi
```

### Step 2: 列出文档让用户选择

使用 AskUserQuestion：

```
请选择要接手的交接文档：

1. time_3_基于login.ts的用户认证交接文档-20260502.md
   模块：用户认证 | 完成度：80%

2. time_2_基于payment.ts的支付模块交接文档-20260501.md
   模块：支付系统 | 完成度：60%
...
```

### Step 3: 读取并验证

- 读取选中的交接文档
- 验证关键文件是否存在
- 检查 git 状态

### Step 4: 生成理解规划文档

**命名**：`time_{x}_新人填坑_理解规划_{project}_{timestamp}.md`

**内容**：
- 对当前情况的理解
- 关键文件验证结果
- 下一步行动计划
- 当前卡点

### Step 5: 更新原交接文档双链

在原文档末尾追加引用记录。

### Step 6: 输出总结

```
✅ 已接手工作

📄 理解规划：time_{x}_新人填坑_理解规划_{project}_{timestamp}.md

我理解的情况是：
- 项目：{project} - {feature}
- 进度：{XX}%
- 已完成：{items}
- 当前卡点：{blocker}

下一步建议：{action}
```

---

## 理解规划文档模板

```markdown
# 新人填坑 - 理解与规划

**关联**：[[time_{x}_xxx交接文档]]
**接手时间**：{timestamp}

---

## 一、我理解的情况

**项目**：{project} - {feature}
**进度**：{XX}%

**已验证完成**：
- ✅ {item1}
- ✅ {item2}

**当前卡点**：
- {blocker}

---

## 二、文件验证

| 文件 | 状态 | 大小 |
|-----|------|------|
| src/auth/login.ts | ✅ 存在 | 2.3KB |
| src/auth/jwt.ts | ✅ 存在 | 1.1KB |

---

## 三、下一步计划

### 立即可做
1. {task1}（预计{time}）
2. {task2}（预计{time}）

### 需要确认
- {question}

---

## 四、工作记录

### {date} - 接手工作
- 验证了{item}
- 准备开始{task}
```

---

## 输出示例

```
✅ 已接手：用户认证模块

📄 已生成：time_3_新人填坑_理解规划_xxx_20260502001.md

──── 我理解的情况 ────
项目：用户认证
进度：70%（核心逻辑完成，待集成）
已验证：login.ts ✅, jwt.ts ✅
卡点：未集成到主路由
推荐：直接开始集成工作

────────

请确认理解无误后，我将开始下一步工作。
```
