---
name: test-case-manager
description: >
  Use this skill to manage natural-language test case libraries. Handles three scenarios:
  (1) ingesting a new PRD and generating test cases for the first time,
  (2) supplementing an existing module with more test cases (edge cases, error flows),
  (3) analyzing the impact of a PRD update and performing CRUD on affected test cases.
  Works with a hierarchical file-system test case library. Never loads all test cases at once —
  uses on-demand tree navigation to stay within token limits.
  Trigger phrases: "管理测试用例", "新增测试用例", "补充测试用例", "测试用例影响分析",
  "PRD变更", "更新测试用例", "test case manager", "新PRD", "初次接入测试用例"
---

# Test Case Manager

## Purpose

Manage a hierarchical, natural-language test case library that evolves alongside PRDs.
The library lives on the local file system as Markdown files.
This skill never loads the entire library — it navigates the tree on demand.

## Before You Start

Read these reference files to understand the rules you must follow:
- `references/tc-format.md` — file formats, TC ID rules, naming conventions
- `references/tree-navigation.md` — how to navigate the library tree without loading everything
- `references/semantic-dedup.md` — how to detect and handle duplicate test cases
- `references/crud-rules.md` — how to classify test cases as UPDATE/DELETE/CREATE (sub-flow 3 only)

## Step 1: Identify Required Inputs

Ask the user for any missing inputs before proceeding:
- **PRD content**: the PRD text (paste inline) or a file path to a `.md` file
- **test-cases root**: the path to the `test-cases/` directory (default: `./test-cases/`)

Store the confirmed path as `{test_cases_root}` — this variable is used in all subsequent steps.

## Step 2: Intent Routing

Analyze the user's request and determine which sub-flow to execute:

```
- Contains "新PRD / 首次 / 新需求 / 初次接入 / new PRD / first time" → Sub-flow 1
- Contains "补充 / 继续 / 增量 / 边界 / 异常 / 深挖 / supplement / edge case" → Sub-flow 2
- Contains "更新 / 变更 / V2 / 影响分析 / 迭代 / update / impact / changed" → Sub-flow 3
- Signal unclear → show disambiguation menu (see below)
```

**Disambiguation menu** (show when signal is unclear):
```
我需要确认操作类型，请选择：
1. 全新接入 — 这是该PRD第一次生成测试用例
2. 增量补充 — 该模块已有用例，需要补充更多场景（异常流、边界值等）
3. 变更影响 — PRD有更新，需要分析影响并更新现有用例
```

---

## Sub-flow 1: New PRD Ingestion

**Goal**: Extract test intentions from a new PRD and mount them into the correct location in the library.

### 1.1 Parse PRD
Extract a list of test intentions from the PRD. Each intention should describe **what to test** (business scenario), not **how to test** (steps). Format as a numbered list.

### 1.2 Navigate to target module
Follow the algorithm in `references/tree-navigation.md` to locate the correct module.
If depth 3 is insufficient, stop and ask the user to specify the exact path.

### 1.3 Semantic deduplication
For each extracted test intention, compare against existing test cases in the target module.
Follow the scoring rules in `references/semantic-dedup.md`.
- Score > 85: skip (already exists)
- Score 40–85: flag for user confirmation
- Score < 40: include in new cases

### 1.4 Preview and confirm
Show the user:
- Target module path
- List of new test cases to be written (after dedup)
- Any flagged possible duplicates requiring confirmation

Wait for user confirmation before writing.

### 1.5 Write files
Following `references/tc-format.md`:
1. Write new test cases to `{module}/{feature}.md` (create file if it doesn't exist)
2. Update `_index.md` files along the path (append new entries, do not overwrite)
3. If any directories are missing, show the full path to be created and wait for confirmation

---

## Sub-flow 2: Incremental Supplement

**Goal**: Add missing test cases (error flows, boundary values, edge cases) to an existing module.

### 2.1 Parse PRD
Understand the business scope of the PRD.

### 2.2 Locate target module
- If the user specified a module path explicitly → use it directly
- Otherwise → follow the algorithm in `references/tree-navigation.md` to locate the module

### 2.3 Load baseline
Read all direct `.md` files in the target module directory (not recursive).
This is the "baseline" — the set of already-covered scenarios.

### 2.4 Identify coverage gaps
Analyze the baseline against the PRD. Look for uncovered dimensions:
- 异常流程: invalid inputs, network errors, permission denied, timeout
- 边界值: empty fields, max length, zero values, negative numbers
- 并发: simultaneous operations, race conditions
- 权限: different user roles, unauthorized access attempts

Generate supplemental test cases only for uncovered scenarios.

### 2.5 Semantic deduplication
Apply dedup from `references/semantic-dedup.md` against the baseline.

### 2.6 Preview and confirm
Show the supplemental cases to the user. Wait for confirmation.

### 2.7 Append to files
Append new cases to the appropriate section of the existing `.md` files.
Do NOT overwrite or reorder existing content.
Follow TC ID rules from `references/tc-format.md`.

---

## Sub-flow 3: Change Impact Analysis

**Goal**: Given a PRD update, identify affected test cases and produce a CRUD change set.

**Required inputs for this sub-flow:**
- PRD_V2 content (the updated PRD, or a description of what changed)
- `{test_cases_root}` (already collected in Step 1)

### 3.1 Extract change signals
From PRD_V2 (or the change description), extract:
- Business keywords describing what changed
- Module/feature names mentioned

### 3.2 Identify affected modules
Read `{test_cases_root}/_index.md` and each domain's `_index.md`.
Use LLM semantic judgment (not exact string matching) to identify which modules are semantically related to the change signals.
Output: list of affected module paths.

**Guard**: if more than 5 modules are identified, show the list to the user and ask for confirmation before loading their content.

### 3.3 Load affected test cases
Read only the test case files in the identified modules.

### 3.4 Classify changes
Compare PRD_V2 against each loaded test case. Follow `references/crud-rules.md` to classify:
- UPDATE: scenario still exists but intent changed
- DELETE: scenario no longer applies (mark with strikethrough, do not delete line)
- CREATE: new scenario in PRD_V2 with no existing coverage

### 3.5 Present diff preview
Format the change set using the output template in `references/crud-rules.md`.
Wait for user confirmation. Support partial confirmation.

### 3.6 Execute changes
Apply only the confirmed changes to the files.

---

## Error Handling

| Situation | Action |
|-----------|--------|
| PRD exceeds 200 lines | Ask user to split by feature module; process one module at a time |
| No domain matches PRD | Show domain list, ask user to select or name a new domain |
| Target path does not exist | Show full path to be created, wait for confirmation |
| `_index.md` is malformed | Show expected format, ask user to fix before retrying |
| `.lock` file exists at `{test_cases_root}/.tc-manager.lock` | Warn user another operation may be in progress; if lock is older than 10 minutes, suggest manual deletion |

## Lock File

Before any write operation, create `{test_cases_root}/.tc-manager.lock` with content:
```json
{"pid": "skill-session", "operation": "{sub-flow name}", "started": "{ISO timestamp}"}
```
Note: `pid` is set to the string `"skill-session"` since LLM-based skills do not have OS process IDs.
Delete the lock file after all writes complete.
