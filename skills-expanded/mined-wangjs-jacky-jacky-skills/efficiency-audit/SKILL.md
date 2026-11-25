---
name: efficiency-audit
description: "分析当前会话的任务执行效率：定位耗时瓶颈、拆解步骤耗时、给出具体优化方案。触发词：效率分析、耗时分析、为什么这么慢、效率审计、efficiency-audit"
---

<role>
你是一个任务执行效率审计专家。通过回溯当前会话的完整上下文，定位效率瓶颈并提供可操作的优化方案。
</role>

<purpose>
当用户感觉某个任务执行时间过长，或想了解"为什么花了这么久"时，对会话进行效率复盘，给出量化分析和改进建议。
</purpose>

<philosophy>
**核心理念：数据驱动，根因定位，可操作改进。**

- 不做泛泛而谈的建议，每条优化必须对应具体事件
- 量化浪费：指出具体哪些操作是多余的，节省多少步
- 区分"必要耗时"和"可避免耗时"
- 输出结构化报告，便于用户下次改进
</philosophy>

<trigger>
```
效率分析
耗时分析
为什么这么慢
为什么花了这么久
效率审计
复盘下刚才的任务
分析下执行效率
efficiency-audit
```
</trigger>

<gsd:workflow>
  <gsd:meta>
    <name>efficiency-audit</name>
    <trigger>效率分析、耗时分析、为什么这么慢、效率审计、复盘</trigger>
    <requires>Read, Grep, Glob, Bash</requires>
    <checkpoints>
      <checkpoint order="1">完成上下文扫描</checkpoint>
      <checkpoint order="2">输出审计报告</checkpoint>
    </checkpoints>
    <constraints>
      <constraint>只分析当前会话内的操作，不跨会话推测</constraint>
      <constraint>每条建议必须对应具体的工具调用或决策点</constraint>
      <constraint>不输出模糊建议（如"提高效率"），只输出具体行动项</constraint>
    </constraints>
  </gsd:meta>

  <gsd:goal>为当前会话生成结构化效率审计报告，区分必要/可避免耗时，给出下次可复用的改进清单。</gsd:goal>

  <gsd:phase name="scan" order="1">
    <gsd:step>扫描当前会话上下文，提取所有工具调用序列</gsd:step>
    <gsd:step>按类别标记每个操作：必要 / 可优化 / 多余</gsd:step>
    <gsd:step>识别反模式（重复读文件、不必要验证、串行可并行等）</gsd:step>
    <gsd:checkpoint>完成上下文扫描</gsd:checkpoint>
  </gsd:phase>

  <gsd:phase name="report" order="2">
    <gsd:step>生成审计报告（含时间线、反模式、优化建议）</gsd:step>
    <gsd:step>输出下次执行同类任务的"标准 SOP"</gsd:step>
    <gsd:checkpoint>输出审计报告</gsd:checkpoint>
  </gsd:phase>
</gsd:workflow>

# efficiency-audit

## 执行流程

### Phase 1: 上下文扫描

**目标**：从当前会话提取完整操作序列并分类

**步骤**：
1. 回溯当前会话的所有工具调用
2. 按功能分组（文件读取、文件修改、命令执行、用户交互、任务管理）
3. 标记每个操作：
   - **必要**（`✓`）：推进任务核心目标
   - **可优化**（`~`）：目标正确但方式低效
   - **多余**（`✗`）：不推进目标或重复操作

#### 反模式检测清单

| 反模式 | 特征 | 检测方式 |
|--------|------|----------|
| **重复读文件** | 同一文件读取 ≥2 次 | 比对 Read 调用的 file_path |
| **不必要验证** | 已知结果的验证操作 | 检查上下文中是否有前置结论 |
| **过度管理** | 简单任务创建大量 TaskCreate/Update | 统计任务管理调用数 vs 实际步骤数 |
| **串行可并行** | 独立操作顺序执行 | 检查无依赖关系但未并行的调用 |
| **冗余 git 操作** | stash → 测试 → pop 验证已知结论 | 检查 git stash/pop 是否必要 |
| **过度确认** | 用户意图明确但仍询问 | 检查 AskUserQuestion 是否必要 |
| **无效构建** | 构建未修改的模块 | 比较修改文件范围 vs 构建范围 |
| **遗漏导致返工** | 首轮遗漏条目，需二次处理 | 检查是否有"补救性"操作 |

### Phase 2: 审计报告

**目标**：输出结构化报告

**输出格式**：

```
## 效率审计报告

### 概览
- 总操作数：X 次
- 必要操作：X 次（X%）
- 可优化操作：X 次（节省 ~X 步）
- 多余操作：X 次（浪费 X 步）

### 操作时间线

| # | 操作 | 类别 | 标记 | 说明 |
|---|------|------|------|------|
| 1 | Read link.ts | 文件读取 | ✓ | 首次读取，必要 |
| 2 | Read registry.ts | 文件读取 | ✓ | 了解依赖 |
| ... |

### 反模式摘要

1. **[反模式名称]** — 具体描述
   - 浪费：X 步
   - 建议：[具体行动]

### 优化建议（下次执行同类任务）

```
理想 SOP（X 步完成）：

1. [步骤 1]
2. [步骤 2]
...
```

### 关键教训

- [教训 1]
- [教训 2]
```

## 验证

- 每条反模式都对应具体的工具调用（可回溯定位）
- 优化建议可直接执行（不是泛泛而谈）
- 理想 SOP 步骤数 < 实际操作数

## Next Up

- [ ] 将关键教训写入项目 MEMORY.md
- [ ] 如果涉及通用模式，更新 CLAUDE.md 的注意事项
