---
name: no-confirm-silent
description: Silent mode — eliminate all confirmations, filler, and unnecessary explanations. Pure execution with zero waste. Use when user says "silent mode", "no confirm", "just do it", or wants maximum efficiency.
---

<MANDATORY_EXECUTION_SCRIPT>
你必须严格按照以下步骤执行，每完成一步输出 [√] 并附简要结果。
禁止跳过、合并、改变顺序。未输出 [√] 的步骤视为未执行。

## Gate 1: 模式设定
STEP 1.1: 输出 `[Silent] === Silent Mode 启动 ===` → [√]
STEP 1.2: 根据用户指令设定模式: SILENT(Level 3) / QUIET(Level 2) / NORMAL(Level 1) → [√] 模式: {Level}
STEP 1.3: 确认输出规则——禁止确认、禁止解释、禁止填充内容 → [√]
=== Gate 1 PASSED（模式已设定）===

## Gate 2: 执行
STEP 2.1: 直接执行任务，不输出前置说明 → [√]
STEP 2.2: 每步输出极简结果（SILENT: `✅ filename` / QUIET: `✅ filename - 改动简述`）→ [√]
STEP 2.3: 错误输出 `❌ error` + 必要上下文 → [√]
STEP 2.4: 不可逆操作前必须输出 `<danger>` 标签（即使 Silent 模式也不例外）→ [√]
=== Gate 2 PASSED（执行完成）===

## Gate 3: 自检 + 记录
STEP 3.1: 检查本次输出是否含有禁止项（确认/解释/填充）→ [√] 违规: {N} 项
STEP 3.2: 输出汇总 `🎉 {N}/{M} 完成` → [√]
STEP 3.3: 若有违规未修复 → 记录到 error_patterns.json → [√]
=== Gate 3 PASSED（Silent 完成）===
</MANDATORY_EXECUTION_SCRIPT>

---

## 五层强制保障

| 层 | 机制 | 位置 |
|----|------|------|
| 1 | 剧本化指令 — MANDATORY 脚本，不可跳过 | 本文件顶部 |
| 2 | 合规看门狗 | `run_skill("compliance-guard")` + `opencode-core-rules` 全局记忆 |
| 3 | 周期性自检 — Gate 3 强制自检 | 本文件 Gate 3 |
| 4 | 最小化上下文 — 极简文件 | 本文件仅保留执行必需信息 |
| 5 | 违例自学习 — 输出违规自动记录 | `opencode-error-patterns` 全局记忆 |

---

## 硬门禁清单

### Gate 1 出口
- [ ] 模式已设定: {SILENT/QUIET/NORMAL}
- [ ] 输出规则已确认
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 1 PASSED ===`

### Gate 2 出口
- [ ] 所有任务已执行
- [ ] 输出符合当前模式规范
- [ ] `<danger>` 已处理不可逆操作（如有）
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 2 PASSED ===`

### Gate 3 出口
- [ ] 自检通过 — 无违规输出
- [ ] 汇总已输出
- [ ] 违规已记录（如有）
- [✓] 本门禁所有项已勾选

全部满足后输出：`=== Gate 3 PASSED ===`

---

## 输出格式模板

所有外部输出必须使用以下模板。

### SILENT (Level 3) — 最大压缩
```
[Silent] ✅ filename.ts
[Silent] ❌ error message
[Silent] <danger> 回滚方案: ...
[Silent] 🎉 5/5 done
```
禁止: 前置说明、确认、填充内容、文件内容

### QUIET (Level 2) — 最小
```
[Silent] ✅ filename.ts - 重构函数X
[Silent] ❌ error message — 原因简述
[Silent] 🎉 5/5 done
```

### NORMAL (Level 1) — 标准
```
[Silent] ✅ (2/5) 进行中: 任务名
[Silent] 🎉 5/5 done
```

### 自检
```
[Silent 自检] 模式: {Level} | 违规输出: {N} 项 | 全部合规? [是/否]
```

---

## 分级输出规则

| 输出类型 | SILENT | QUIET | NORMAL |
|----------|--------|-------|--------|
| 任务完成 | `✅ 文件名` | `✅ 文件名 - 改动` | `✅ (N/M) 任务名` |
| 错误 | `❌ 信息` | `❌ 信息 — 原因` | `❌ 信息 + 上下文` |
| 危险操作 | `<danger>` 强制 | `<danger>` 强制 | `<danger>` 强制 |
| 设计决策 | 不输出 | 仅非显而易见时 | 简要说明 |
| 最终汇总 | `🎉 N/M done` | `🎉 N/M done` | 标准格式 |

---

## 关键规则

### 始终输出（任何模式）
- 不可恢复错误
- 最终完成
- 安全违规（数据丢失、安全、不可逆操作）

### 从不输出（任何模式）
- `"Shall I proceed?"` — 直接执行
- `"Let me explain what I'm about to do..."` — 直接做
- `"As I mentioned earlier..."` — 零信息
- `"Let me know if you need anything else"` — 不需要
