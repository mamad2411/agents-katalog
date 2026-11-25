---
name: self-check
description: Mandatory post-code-change self-check checklist. Includes 29 universal programming discipline rules, code-type index matrix, configurable registration/truncation/dual-entry checks, V2.5 four-hop chain loop + breadcrumb auto-seeding, V2.6 integrity gate (prevents paper-only false completion), V2.7 failure recovery mode + graceful degradation, V2.9.0 adds rule 29 file-size auto-check. Triggers after every code change. Supports pipeline.json project configuration.
tags: [self-check, code-review, checklist, quality, pipeline, breadcrumb, integrity-gate, failure-recovery, file-size-check]
version: 2.9.0

---

# Post-Code-Change Self-Check V2.7 / 代码修改后自检 V2.7

## Overview / 概述

每次代码修改后的强制自检流程。逐项遍历 29 条规则，防止重复已知 Bug 模式。V2.5 新增面包屑自动播种，V2.6 新增完整性阻断点（防纸面自检伪完成），V2.7 新增失败恢复模式 + 优雅降级，V2.9 新增规则29 文件行数检查。

Mandatory self-check process after every code change. Iterates through 29 rules item by item to prevent repeating known bug patterns. V2.5 adds breadcrumb auto-seeding, V2.6 adds integrity gate (prevents paper-only false completion), V2.7 adds failure recovery + graceful degradation, V2.9 adds rule 29 file-size auto-check.

## Trigger Conditions (read from pipeline.json)

**Must execute** when any of the following occurs:

- {{#if hasToolDirectory}}Modifying files in `{{pipeline.architecture.toolDirectory}}`{{/if}}
- Modifying tool schema (name/description/parameters)
- {{#if hasThreeLayerRegistration}}Modifying `{{pipeline.architecture.fallbackToolsConstant}}` fallback list{{/if}}
- Modifying core task-link code
- {{#if hasDualEntry}}Modifying dual-entry HTML files{{/if}}
- Modifying Express routes
- Modifying database schema

## Self-Check Workflow / 自检流程

### Step -1: Pre-Modification Anchor Scan (V2.4+)

**Before writing any code**, scan target files for existing anchors (executed in coding-principles Principle 0):

1. **Scan @COUPLED tags**: record all coupled file paths → add them to self-check scope
2. **Scan 📖 references**: record all referenced docs → read their "Implementation Location" sections
3. **Scan 🍞 breadcrumb header**: if file has 🍞 block → parse @COUPLED/📖/@GOTCHA/@BUGFIX for navigation context
4. **If no 🍞 header**: mark "this file needs breadcrumb seeding after changes"

### Step 0: Locate Rules by Code Type Changed

Based on what you changed, use the index to locate relevant rules. See `references/self-check-full.md` Section 0. You don't need to iterate all 28 rules — only check rules triggered by your change type.

Quick index reference:

| What Changed | Required Rules | Extra Checks |
|-------------|----------------|-------------|
| New/modified tool | 5,6,7,14,28 | Schema completeness + truncation + breadcrumb |
| Tool registration/fallback list | 5,6,28 | Full diff + breadcrumb |
| Data transport pipeline | 5,6,7,28 | Truncation full scan + breadcrumb |
| Frontend core JS | 8,9,14,28 | Breadcrumb |
| Frontend workflow JS | 8,9,12,16,17,18,19,20,28 | All close paths + breadcrumb |
| Modal/popup/overlay | 12,28 | Exhaust close paths + breadcrumb |
| CSS/layout | 16,28 | Check adjacent components + breadcrumb |
| Express routes | 13,24,26,27,28 | Fixed-before-param + breadcrumb |
| Middleware | 28 | Manual: try/catch empty body + breadcrumb |
| Database schema/migration | 10,28 | Migration numbering + breadcrumb |
| Core library (LLM/payment/WS) | 23,28 | ESM/CJS compat + breadcrumb |
| Shared modules | 23,28 | ESM/CJS dual-format + breadcrumb |
| Desktop main process | 28 | Manual: IPC channels/window lifecycle + breadcrumb |

### Step 0.6: Breadcrumb Auto-Seeding 🍞 (V2.5 NEW — Mandatory for Every File Changed)

> Breadcrumbs are the AI's project map. This step ensures every code change automatically plants breadcrumbs, so any future AI opening the same file can navigate without extra context.

For **every modified file**:

**A. File has NO 🍞 header → Create one**:
Insert the standard 🍞 navigation block at the file header (after `'use strict'`, before first `import/require`):

```
/*
 * ─── 🍞 AI Breadcrumb Navigation ──────────────────
 * Tag meanings: @COUPLED=linked files @GOTCHA=gotcha @BUGFIX=bug fix @MAGIC=magic number
 *              @DEPENDS=external dependency @ASSUME=assumption @TODO=todo @WHY=design rationale
 *              @PERF=performance @CONTRACT=interface contract 📖=dev doc reference
 * 
 * Breadcrumbs (changing this affects):
 *   @COUPLED sync needed: fileA, fileB
 *   📖 see: docs/xxx/yyy.md
 * ──────────────────────────────────────────────────
 */
```

Auto-fill breadcrumbs detected during this change:
- a) **`@COUPLED`**: which other files were modified in this session? → mutual cross-reference
- b) **`📖`**: which dev docs were read during this change? → link them
- c) **`@BUGFIX`**: is this a bug fix? → add date + reason + solution
- d) **`@GOTCHA`**: any counter-intuitive patterns? → mark the trap
- e) **`@MAGIC`**: any hardcoded business numbers? → annotate meaning

**B. File already HAS 🍞 header → Update it**:
1. Verify existing `@COUPLED` file paths still exist
2. Verify existing `📖` doc paths still exist
3. Add new breadcrumbs from this change
4. Remove/stale-mark expired breadcrumbs

**C. Breadcrumb quality requirements** (block if violated):
- `@COUPLED` must specify file paths (or file+line), NOT vague "all frontend files"
- `📖` must point to real existing documents → block if missing
- `@BUGFIX` must include date + brief reason + fix approach

**D. Insertion position rules by language**:
- JavaScript/TypeScript: after `'use strict';`, before first `import/require`
- HTML: after `<!DOCTYPE html>`, before `<head>` (use `<!-- -->` comments)
- CSS: first line (use `/* */` comments)
- Python: after `#!` shebang, before first `import` (use `#` lines, replace 🍞 with `[breadcrumb]`)
- Markdown: after `#` title, before body text (use `<!-- -->` HTML comments)

**Why this format is AI-readable without any external docs**:
- `🍞` emoji = visual anchor, AI can `grep /🍞/` to locate instantly
- Tag meanings line = **inline cheat sheet**, no need to read ANCHOR_SPEC.md
- `@COUPLED` + file list = tells AI exactly which files to change together
- `📖` + doc path = entry point to detailed design docs
- `@BUGFIX` + date = prevents regressions

This step ensures: **every code change = one breadcrumb planted automatically**. No manual effort needed.

### Step 1: Architecture Registration Check (optional, per pipeline.json config)

{{#if hasThreeLayerRegistration}}
Check consistency between `{{pipeline.architecture.toolDirectory}}` and `{{pipeline.architecture.fallbackToolsConstant}}`.
Confirm count is `{{pipeline.architecture.toolCount}}`.
{{else}}
Skip (project `pipeline.json` has `architecture.hasThreeLayerRegistration` = false)
{{/if}}

### Step 2: Schema Field Completeness (if tools involved)

Confirm each tool entry has complete `name`/`description`/`parameters`.

### Step 3: Implementation Location Cross-Validation (V2.4+ — Four-Hop Chain)

If this change involves **dev docs** or **code referenced in docs' "Implementation Location"**:

1. **Changed docs** → verify "Implementation Location" sections are still accurate
2. **Changed code** → search which docs' "Implementation Location" references this file → check if they need updates
3. **📖 bi-directional verification**:
   - Code 📖 path → doc exists?
   - Doc "Implementation Location" → code path exists?
   - Either broken → fix or mark (block if path missing, warn if content mismatch)

### Step 4: Truncation Point Scan (if data transport involved)

{{#if hasTruncationPoints}}
Check all configured truncation points:
{{#each pipeline.architecture.truncationPoints}}
- `{{this}}`
{{/each}}
Confirm truncation limits can accommodate maximum data volume.
{{else}}
Skip (no truncation points configured)
{{/if}}

### Step 5: Iterate Through 29 Rules

Select relevant rules by change type. Core rule quick reference:

| Rule | Core | Trigger |
|------|------|---------|
| 8 | No `\|\|` for numeric falsy checks | Frontend JS changes |
| 9 | `<select>` must have placeholder option | Form/dropdown changes |
| 10 | POST upsert must not hardcode fields | Backend route changes |
| 11 | Rule self-growth | Fixed a new type of bug |
| 12 | Overlay must exhaust all close paths | Modal/drawer/overlay |
| 13 | Fixed routes before parameterized routes | Express routes |
| 14 | New tool → add to frontend display-name map | Tool addition |
| 16 | Layout migration: reset old artifacts | CSS/layout refactor |
| 18 | Re-initializable container: sync children | innerHTML rebuild |
| 20 | Async callback: verify context consistency | fetch/async |
| 23 | npm dep: check ESM/CJS compatibility | New dependency |
| 24 | GET/POST same-API data source symmetry | Route changes |
| 26 | Intent anchor comments (V2.3) | Any code change |
| 27 | Code-doc linkage consistency (V2.3) | Code references doc paths |
| 28 | 🍞 Breadcrumb auto-seeding (V2.5) | Any code change |
| 29 | 📏 File-size check (V2.9) | Any code change |

### Step 6: Historical Incident Pattern Match

Think: Could this change reproduce a known incident pattern? Reference `references/incident-history.md`.

### Step 6.5: Trust-Tiered Rule Check (V2.1+)

> This step handles self-growing system generated Trust-Tiered rules. Only executes when project `.ai-pipeline/` exists.

1. **Read observation pool**: `read_file("references/observations.md")`
   - Check if any Tier 0 observation entries relate to this change
   - If related, record "this pattern has been observed N times before"

2. **Read auto-grown rules**: Check `[SOFT]` and `[HARD]` marked rules at the end of `self-check-full.md` in the [Auto-Grown Rules Zone]
   - `[HARD]` rules → mandatory block, must fix
   - `[SOFT]` rules → warn, suggest fix but skippable

3. **User resistance demotion**: If user explicitly says "ignore this rule" or "skip this":
   - Record demotion event in `growth-log.md`
   - `[HARD]` → demote to `[SOFT]` (confidence -2)
   - `[SOFT]` → demote back to `observations.md` observation pool (confidence -2)
   - Confidence hits 0 → move to `retired.md`

4. **Retired rule check**: `read_file("references/retired.md")`
   - If current change pattern matches a retired rule, do NOT alert again

5. **Rule bloat sanity check (V2.2)**: Quick count of active rules
   - Count `[SOFT]` + `[HARD]` rules in `self-check-full.md`
   - If total > `antiBloat.maxTotalRules` (default 30): warn user
   - If `[HARD]` > `antiBloat.maxHardRules` (default 15): same warning

### Step 6.6: Self-Check Integrity Gate / 自检完整性阻断点 (V2.6 NEW)

> Steps 0-6.5 are all analytical operations (reading files, doing diffs, checking rules). These operations themselves create an illusion of "I've checked everything." Step 7 (Automated Testing) is an execution-type operation, fundamentally different in mode. Place a hard gate at the fracture point between analysis and execution.

> 步骤 0-6.5 全是分析型操作（读文件、做 diff、检查规则），这些操作本身会给人"已经查完了"的错觉。步骤 7 是执行型操作，模式完全不同。在分析模式和执行模式之间的断裂点设置硬性门禁。

After Step 6.5 completes, before Step 7, verify item-by-item / 逐项确认：
- □ Have Steps 0-6.5 all been completed? (No step may be skipped)
- □ Has Step 7 (Automated Testing) been queued for execution?
- □ If Step 7 has NOT been executed → **BLOCK here, prohibit proceeding to Step 8 (Changelog) or git commit**

**Block consequence / 阻断后果**: Skipping Step 7 to write changelog directly = paper-only false completion. Paper checks passed + not actually run tests = illusion of "everything is fine." Self-check = paper checks + actual verification, one step short = not done.

**Why this gate is necessary / 为什么需要这个门禁**: Without it, the AI's natural tendency to stop after analytical steps (all reads/diffs/logic checks feel like "completion") will cause the pipeline to silently truncate at Step 6.5. This gate forces the mode switch from analysis to execution.

### Step 6.7: Failure Recovery Mode / 失败恢复模式 (V2.7 NEW)

> When self-check finds too many violations, don't block delivery — group and prioritize. This prevents the pipeline from becoming a bottleneck on legacy codebases.
> 自检发现过多违规时，不要阻塞交付——分组优先级处理。防止流水线在遗留代码上变成瓶颈。

**Activation threshold / 激活阈值**: ≥ 5 violations found in a single self-check run.

When triggered:
```
┌── Failure Recovery Grouping / 失败分组 ──────────────────────
│
│ 🔴 HARD (must fix before merge / 合并前必须修):
│   [list violations that would cause runtime errors or data loss]
│   [列出会导致运行时错误或数据丢失的违规]
│
│ 🟡 SOFT (fix in next session / 下次修改时修):
│   [list violations that are quality issues but won't break]
│   [列出质量缺陷但不影响运行的问题]
│
│ ⚪ BASELINE (record as tech debt / 记录为技术债务):
│   [list violations that predate this change]
│   [列出本次改动之前就存在的违规]
│
│ Decision / 决策:
│ □ HARD = 0 → ✅ Proceed to Step 7 (testing) / 继续到步骤7
│ □ HARD > 0 → 🛑 Fix HARD items → re-check → then proceed
│ □ SOFT + BASELINE → Log to changelog, do NOT block delivery
│
└──────────────────────────────────────────────────────────────
```

**Key principle / 关键原则**:
- Only HARD violations block the pipeline. SOFT + BASELINE are recorded but don't halt.
- BASELINE items are auto-marked for re-check on next edit of the same file.
- If the same BASELINE item appears 3+ times across sessions → upgrade to SOFT.

### Step 6.8: Graceful Degradation / 优雅降级 (V2.7 NEW)

> The pipeline should never crash because optional infrastructure is missing. Degrade gracefully instead of blocking entirely.
> 流水线不应因为可选的基建缺失而崩溃。优雅降级而非完全阻断。

| Missing Component / 缺失组件 | Degradation Behavior / 降级行为 |
|:--|:--|
| `开发文档/` directory does not exist | Skip Step 3 (cross-validation), 🍞 breadcrumbs write to file headers only, print ⚠️ "Dev docs not found — breadcrumb 📖 links disabled" |
| `pipeline.json` not configured | Skip Steps 1, 4 (architecture/truncation), run Steps 2, 5-7 in generic mode |
| Test directory `{{pipeline.paths.tests}}` empty | Replace Step 7 with manual verification prompt, do NOT block |
| `.ai-pipeline/` does not exist (first run) | Skip Step 6.5 (trust-tier), run remaining steps in baseline mode |

**Degradation golden rule / 降级黄金守则**: Always print which steps were skipped and why. Never silently skip.

### Step 7: Automated Testing / 自动化测试 (mandatory when gate passes)

{{#if pipeline.skills.webTesting.enabled}}
After self-check integrity gate passes, execute automated tests:
- Check if project `{{pipeline.paths.tests}}` has test scripts
- Run tests and confirm all pass
{{else}}
**WARNING**: webTesting not enabled in pipeline.json — this does NOT exempt from Step 6.6 gate. If no automated test suite exists, perform manual verification before proceeding to Step 8.
{{/if}}

### Step 8: Changelog (mandatory)

After self-check + tests all pass, record this change:
- Format: change summary → file list → new deps → self-check digest
- Write to `{{pipeline.paths.changelogFormat}}`
- Must NOT skip or "do it later"

## Related Skill Orchestration

```
coding-principles (pre-code check + breadcrumb pre-scan 🍞 V2.5)
    ↓
safe-terminal-executor (if API verification needed)
    ↓
self-check (post-code check) ← This Skill
    ├── Step -1: pre-modification anchor scan
    ├── Step 0: locate rules by code type
    ├── Step 0.6: 🍞 breadcrumb auto-seeding (V2.5)
    ├── Step 1-2: architecture diff + schema
    ├── Step 3: implementation cross-validation (four-hop chain)
    ├── Step 4: truncation point scan
    ├── Step 5: iterate 29 rules
    ├── Step 6: incident pattern match
    ├── Step 6.5: trust-tier check
    ├── Step 6.6: 🛑 integrity gate (V2.6 — blocks if testing not queued)
    ├── Step 6.7: 🔄 failure recovery mode (V2.7 — HARD/SOFT/BASELINE grouping)
    ├── Step 6.8: ⚠️ graceful degradation (V2.7 — skip missing infra, never crash)
    ↓
web-testing (automated testing, mandatory when gate passes)
    ↓
changelog (change log)
    ↓
git commit
    ↓
Delivery closed loop
```

## Resources

- `references/self-check-full.md` — Complete self-check document (28 rules + auto-grown zone + V2.5 four-hop chain + 🍞 breadcrumbs)
- `references/incident-history.md` — Historical incident root cause + lesson quick reference
- `references/observations.md` — Tier 0 observation pool (V2.1+)
- `references/retired.md` — Retired rules archive (V2.1+)
- `references/growth-log.md` — Growth event log (V2.1+)
