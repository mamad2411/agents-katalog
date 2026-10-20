---
name: ralph-task-executor
slug: ralph-task-executor
version: 2.1.0
homepage: https://clawic.com/skills/ralph-task-executor
description: "无脑死磕执行，不弹窗、不询问、写完直接推进，专治中途摆烂停下。Relentless task execution engine with state machine, priority queues, and parallel support. Use when you need relentless task execution without interruptions. Triggers on 'execute tasks', 'run tasks', 'just do it', 'no stopping'."
---

> ⚠️ **此 skill 已标记为 OpenCode 遗产**。Reasonix 中请用 `full-autonomous` Phase 3 + `task-executor` 替代任务执行。

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 规划（PLANNING）
STEP 1.1: 输出 `[Executor] === Ralph Executor v2.1 启动 ===` → [√]
STEP 1.2: 接收任务列表 → 按优先级排序、检测依赖、分配并行组 → [√] 任务 N 个 | 并行组 M 组
STEP 1.3: 声明执行策略（P0 重试上限=8, P1=5, P2=3, P3=2）→ [√]
=== Gate 1 PASSED（规划完成）===

## Gate 2: 执行（EXECUTING）
STEP 2.1: 取最高优先级就绪任务 → [√] 当前: {任务名} (P{0-3})
STEP 2.2: 执行任务 — 写代码 / 跑命令 / 改文件 → [√]
STEP 2.3: 若任务独立且当前无依赖阻塞 → 并行派发 ≤3 个任务（task()）→ [√]
=== Gate 2 PASSED（执行完成）===

## Gate 3: 验证（VERIFYING）
STEP 3.1: 对已执行任务运行验证（测试/lint/类型检查）→ [√] {通过/失败}
STEP 3.2: 若通过 → 标记 DONE，回到 Gate 2 取下一任务
STEP 3.3: 若失败 → 修复并在该优先级重试预算内重试（P0=8, P1=5, P2=3, P3=2）
         → [√] 重试 {N}/{Max}
STEP 3.4: 若重试耗尽 → 标记 FAILED，继续下一任务 → [√]
=== Gate 3 PASSED（验证完成）===

## Gate 4: 收尾 + 自检
STEP 4.1: 所有任务处理完毕 → 输出执行报告 → [√]
          `[Executor] 🏁 DONE: N | FAILED: M | ⏱ Xm | 🔄 Y 次重试`
STEP 4.2: 失败任务记录到 error_patterns.json → [√]
STEP 4.3: 自检 — 检查是否有遗漏任务或挂起子代理 → [√]
=== Gate 4 PASSED（执行完毕）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本，不可跳过 | 本文件顶部 |
| 2 | 合规看门狗 | `run_skill("compliance-guard")` + `opencode-core-rules` 全局记忆 |
| 3 | 周期性自检 — Gate 4 强制自检 | 本文件 Gate 4 |
| 4 | 最小化上下文 — 本文件仅保留执行必须信息 | 详细设计移至 `details.md` |
| 5 | 违例自学习 — 失败任务自动记录 | `opencode-error-patterns` 全局记忆 |

---

## 硬门禁清单

### Gate 1 出口
- [ ] 任务列表已接收: {N} 个
- [ ] 优先级排序完成
- [ ] 并行组分配完成: {M} 组
- [ ] 重试上限已声明
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 当前任务已执行
- [ ] 并行任务已派发（如适用）
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 验证已运行
- [ ] 失败任务已重试 / 已标记 FAILED
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

### Gate 4 出口
- [ ] 执行报告已输出
- [ ] 失败已记录到 error_patterns.json
- [ ] 自检通过
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 4 PASSED ===`

---

## 输出格式模板

所有外部输出必须使用以下模板。

### 启动
```
[Executor] === Ralph Executor v2.1 启动 ===
[Executor] 📋 N 任务, M 并行组 | P0 上限=8, P1=5, P2=3, P3=2
```

### 进度
```
[Executor] ✅ (3/12) T-003 — DONE (P1) | 重试: 2 次
[Executor] 🔄 (5/12) T-005 — retry 3/5 (P2)
[Executor] ❌ (5/12) T-005 — FAILED (P2) | 重试耗尽
```

### 并行
```
[Parallel] T-001(P0), T-003(P1), T-004(P2) dispatched via sub-agents
[Parallel] Waiting for results...
[Parallel] ✅ T-001 | ✅ T-003 | ❌ T-004
```

### 自检
```
[Executor 自检] Gate 1 ✅ | Gate 2 ✅ | Gate 3 ✅ | Gate 4 进行中
[Executor 自检] 遗漏任务? [否] | 挂起子代理? [否]
```

### 汇总
```
[Executor] 🏁 DONE: 10 | FAILED: 2 | ⏱ 23m | 🔄 5 次重试
```

---

## 关键规则

### 重试预算
| 优先级 | 最大重试 | 适用场景 |
|--------|---------|---------|
| P0 | 8 | 核心功能、阻塞性任务 |
| P1 | 5 | 重要功能 |
| P2 | 3 | 一般功能 |
| P3 | 2 | 优化/样式/文档 |

### 并行规则
- 同一时间 ≤3 个并行子代理
- 有依赖关系的任务禁止并行
- 并行组中任一失败 → 不阻塞其他并行任务

### 执行纪律
- 不弹窗、不询问
- 卡住了换策略，不跳过
- 重试上限耗尽 → 标记 FAILED → 继续下一个（不阻塞队列）

---

See `details.md` for full reference: 状态机定义、协作模式、安全边界。