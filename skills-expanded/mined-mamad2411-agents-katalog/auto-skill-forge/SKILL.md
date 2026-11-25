---
name: auto-skill-forge
description: "Autonomous skill lifecycle engine. Creates new skills from user requirements or optimizes existing SKILL.md files. Dual evaluation: structural rubric (7 dimensions, 75pts) + checklist pass rate (25pts). Hill-climbing with adversarial review, same-judge scoring, ratchet mechanism. Use when user mentions \"优化skill\", \"创建skill\", \"新建skill\", \"做一个skill\", \"auto optimize\", \"skill quality\", \"skill review\", \"skill打分\", \"提升skill\", \"create skill\", \"skill优化\"."

---

# Auto-Skill-Forge

Create, evaluate, optimize, and package Agent Skills. Two-part scoring: structural rubric (75pts) + checklist pass rate (25pts). Autonomous hill-climbing: diagnose → edit → adversarial review + re-score → keep or revert. Creation is optimization from scratch — same evaluation, same loop, same ratchet.

## Prerequisites

- Git repo at project root
- `results.tsv` in auto-skill-forge directory (auto-created on first run if missing)

## Evaluation Rubric (100 points)

### Component A: Structural (75 points) — 静态分析

Score each dimension 1-10. Multiply by weight. Sum all, divide by 10.

| #    | Dimension               | Wt   | Check                                                        |
| ---- | ----------------------- | ---- | ------------------------------------------------------------ |
| 1    | Frontmatter quality     | 8    | `name` is lowercase-hyphenated. `description` says what it does, when to use, and lists trigger keywords. ≤1024 chars. |
| 2    | Workflow clarity        | 15   | Numbered, executable steps. Each step has explicit input and output. |
| 3    | Edge case coverage      | 10   | Covers failure scenarios. Has fallback paths.                |
| 4    | Checkpoint design       | 7    | User confirmation before critical/irreversible actions.      |
| 5    | Instruction specificity | 15   | No vague directives. Concrete parameters, formats, examples. |
| 6    | Resource integrity      | 5    | Referenced files, scripts, paths actually exist.             |
| 7    | Overall architecture    | 15   | Clear structure. No redundancy. No gaps.                     |

### Component B: Effectiveness (25 points) — 实测

Use a checklist: 3-6 yes/no questions + 8-12 test inputs. A judge agent runs the skill against each test input, answers every checklist question yes/no, and computes the pass rate.

```
pass_rate = total "yes" answers / (questions × inputs)
effectiveness_score = pass_rate × 25
```

Spawn an independent agent as the judge. If spawning is not possible, fall back to dry-run and note `eval_mode=dry_run` in results.

### Total Score

```
total = structural_score + effectiveness_score   (max 100)
```

Improvement requires strict `>` (not `≥`). Round to 1 decimal.

## Core Loop

```
Phase 0   Intent      → 判断模式（创建 / 优化），访谈或确定范围
Phase 1   Design      → [创建] 写草稿 + 边界扩展 / [优化] 加载已有 → 提炼能力 → 生成 checklist → 用户审批
Phase 2   Calibration → 验证 checklist 机械清晰度（TPR/TNR ≥ 80%）
Phase 3   Baseline    → [创建] with-skill vs bare-Claude 双锚点 / [优化] 单锚点摸底
Phase 4   Optimize    → 自主爬山：Diagnose → Edit → Review+Re-score → Keep/Revert（最多 3 轮）
Phase 5   Rewrite     → 触顶时从零重写（需用户同意）
Phase 6   Report      → 汇总报告 + 打包 .skill
```

---

### Phase 0: Intent & Initialize

First, determine the mode:

| User says                      | Mode                                              |
| ------------------------------ | ------------------------------------------------- |
| "创建/新建/做一个 skill for X" | **Create**                                        |
| "优化/改进/评估 skill Y"       | **Optimize**                                      |
| Ambiguous                      | Ask: "是要创建一个全新的 skill，还是优化已有的？" |

---

#### Mode A: Create New Skill

##### Step A1: Interview

Ask these 4 questions:

1. **What should this skill enable Claude to do?** — Core capability in one sentence.
2. **When should this skill trigger?** — What user phrases, contexts, or scenarios?
3. **What's the expected output format?** — File type, structure, key properties.
4. **What tools/dependencies does it need?** — Specific CLI tools, libraries, APIs.

If the current conversation already contains the user's workflow (sequence of steps, tools used, corrections made), extract answers from conversation history first. Only ask what's missing.

##### Step A2: Research

Check available tools, MCPs, and similar skills for reference. If useful sources exist, research in parallel via sub-agents.

##### Step A3: Write Draft

Write SKILL.md with:

- **name**: lowercase-hyphenated identifier
- **description**: what it does + when to trigger + trigger keywords. Slightly "pushy" — include phrases users might actually say, not just formal descriptions.
- **Workflow**: Numbered, executable steps. Each step has explicit input and output.
- **Examples**: At least one concrete input/output pair.
- **Edge cases & fallbacks**: What to do when things fail.

##### Step A4: Intent Expansion — 边界扩展（防自证陷阱）

**Critical step.** The agent wrote the draft — if it now generates a checklist based solely on that draft, it will test only what it already remembered to include. This creates a "self-grading" bias where the draft scores artificially high and Phase 4 has nothing to fix.

The agent must proactively challenge the draft's boundaries before generating the checklist:

> "为了确保这个 Skill 足够健壮，我假设它还需要处理以下边缘场景。请确认哪些需要纳入考核指标："
>
> 1. **非标准输入**：格式错误、编码异常、空输入、类型不匹配
> 2. **依赖缺失**：所需工具/库未安装或版本不兼容
> 3. **规模边界**：超大文件、超多字段、深层嵌套
> 4. **环境差异**：路径含空格/中文、权限不足、跨平台差异
> 5. **模糊指令**：用户没有明确说出操作名称，只描述了想达到的结果
>
> （Agent 根据具体 skill 类型补充领域特定的边界场景）

User confirms which boundaries to include. These become **additional claimed capabilities** that the draft must handle — forcing it to expose weaknesses during Phase 3 baseline, which then gives Phase 4 real optimization targets.

##### Step A5: Initialize

1. Create branch `auto-optimize/YYYYMMDD-HHMM`.
2. If `results.tsv` missing, create with header: `timestamp	commit	skill	old_score	new_score	status	dimension	note	eval_mode	pass_rate`.
3. Read existing `results.tsv`.

Proceed to Phase 1.

---

#### Mode B: Optimize Existing Skills

1. Determine scope: all skills (scan `.claude/skills/*/SKILL.md`, skip self) or user-specified list.
2. Create branch `auto-optimize/YYYYMMDD-HHMM`.
3. If `results.tsv` missing, create with header: `timestamp	commit	skill	old_score	new_score	status	dimension	note	eval_mode	pass_rate`.
4. Read existing `results.tsv`.

Proceed to Phase 1.

---

### Phase 1: Design

For each skill. Produces `{skill-dir}/test-checklist.json`.

**The agent does the heavy lifting. The user only reviews and approves.**

The first two steps differ by mode; from Step 3 onward, both modes follow the same flow.

#### Step 1: Load or Write Skill

- **Create mode**: The draft from Phase 0 Step A3 (already expanded with user-confirmed boundaries from Step A4) is the working version.
- **Optimize mode**: Read the existing SKILL.md.

#### Step 2: Extract Claims

Read SKILL.md carefully. Extract every concrete claim the skill makes:

> 这个 skill 声称自己能：
>
> 1. 把 JSON 转成 CSV，自动生成表头
> 2. 处理嵌套对象，展平成 "parent.child" 列名
> 3. 保持字段顺序和输入 JSON 一致
> 4. 处理空输入不崩溃
> 5. 输出带 UTF-8 BOM

**Create mode**: Claims must include both the original draft capabilities AND the user-confirmed expanded boundaries from Intent Expansion. If a boundary was confirmed ("需要处理编码异常"), the claim list must include it — even if the draft doesn't currently handle it yet. That's the point: expose the gap so Phase 4 can close it.

Show this list to the user: "我读完了，这个 skill 声称能做这些事。有没有漏的？有没有它其实没声称但你希望它能做的？"

#### Step 3: Propose Checklist Questions

For each claim, propose one yes/no question that mechanically verifies it. Rules:

- 3-6 questions total. Beyond 6, the skill starts gaming the checklist instead of genuinely improving.
- Every question must be answerable with a clear yes/no by looking at the output.
- No subjective language — "Is the output good?" is banned. "Does the output contain column headers?" is correct.

Show the user:

> 基于这些声称的能力，我建议用以下 checklist 来验证：
>
> 1. 所有 JSON key 都作为 CSV 列出现了吗？（是/否）
> 2. 嵌套对象被展平了吗，比如 a.b.c 这种列名？（是/否）
> 3. 列顺序和输入 JSON 的 key 顺序一致吗？（是/否）
> 4. 空输入能正常输出吗——有表头、零行数据、不报错？（是/否）
> 5. 输出文件带 UTF-8 BOM 吗？（是/否）

User can add, remove, or reword questions. Iterate until confirmed.

#### Step 4: Select Test Inputs

Select 8-12 real user requests. These are high-data-content task instructions — the agent will feed them to the skill and run the checklist against the output.

**The coverage rule:** the number of inputs is not arbitrary. Look back at the checklist questions — each one targets a boundary condition. Count the boundaries. Make sure every boundary is triggered by at least 2 test inputs. If there are 5 boundaries, that means at least ~10 inputs. 8 is the floor; 12 is "every boundary is solidly covered."

**How the agent picks them** — internally, the agent thinks about coverage dimensions to ensure the inputs are diverse, but this thinking stays invisible to the user:

- Complexity: simple / moderate / complex
- Input quality: clean / malformed / incomplete / missing
- Clarity: specific / ambiguous

The agent samples inputs that cover different combinations of these axes, checks whether every boundary from the checklist is triggered by at least 2 inputs, fills gaps, then presents the final list in plain language:

> 我用这几个场景来跑 checklist（确保每个检查项都至少有 2 个场景触发）：
>
> 1. "把这个 JSON 转成 CSV：[{\"name\":\"Alice\",\"age\":30}]"
>    → 正常场景，简单数据
> 2. "转成 CSV：{\"user\":{\"name\":\"A\",\"addr\":{\"city\":\"X\",\"zip\":\"10001\"}}}"
>    → 嵌套 2 层，考验展平逻辑
> 3. "把这个做成 CSV"（附件是一个只有 1 个字段的 JSON）
>    → 指令模糊 + 极简数据
> 4. 空的 JSON 数组：[]
>    → 边界情况，考验空输入处理
> 5. "整理下这些数据"（附件是一个字段名带特殊字符的 JSON）
>    → 模糊指令 + 脏数据
> 6. "转一下这个"（附件是 500 行 30 列的 JSON，但只有前 2 行有值）
>    → 大体积 + 稀疏数据
> 7. ……
>
> （实际数量取决于 checklist 覆盖的边界数，通常 8-12 个）

The words "dimension" or "tuple" never appear to the user. The agent carries the rigor of coverage thinking internally, but the user experience is just: "我建议用这几个场景来测试——你觉得够不够？"

User can add, remove, or modify inputs. Iterate until confirmed.

#### Step 5: Save

Write to `{skill-dir}/test-checklist.json`:

```json
{
  "checklist": [
    "所有 JSON key 都作为 CSV 列出现了吗？",
    "嵌套对象被展平了吗（parent.child 列名）？",
    "列顺序和输入 JSON 的 key 顺序一致吗？",
    "空输入能正常输出吗（有表头、零行、不报错）？",
    "输出文件带 UTF-8 BOM 吗？"
  ],
  "test_inputs": [
    "把这个 JSON 转成 CSV：[{\"name\":\"Alice\",\"age\":30}]",
    "转成 CSV：{\"user\":{\"name\":\"A\",\"addr\":{\"city\":\"X\",\"zip\":\"10001\"}}}",
    "把这个做成 CSV（附件：单字段极简 JSON）",
    "空数组：[]"
  ]
}
```

If the file already exists, ask: reuse / rewrite / append.

Pause. Display the full checklist and test inputs. Do not proceed until user confirms.

---

### Phase 2: Criteria Calibration

Purpose: verify that checklist questions are mechanically clear enough that different judges produce the same yes/no answers.

Pick 6 checklist-question × test-input pairs:

- 2 pairs that should clearly be "yes"
- 2 pairs that should clearly be "no"
- 2 borderline pairs

#### Step 1: User Labels

Present each pair to the user. User answers YES or NO. This takes ~3 minutes.

#### Step 2: Judge Scoring

Spawn an independent judge agent. Give it the SKILL.md and the 6 pairs (with checklist questions, WITHOUT user labels). Judge returns YES/NO per pair with a one-line justification.

#### Step 3: Check Criteria Clarity

Compare user vs judge:

```
             User: YES    User: NO
Judge: YES      TP           FP
Judge: NO       FN           TN

TPR = TP / (TP + FN)   — criteria clear enough for expected-YES items?
TNR = TN / (TN + FP)   — criteria clear enough for expected-NO items?
```

Low TPR or TNR means the checklist questions are ambiguous, NOT that the judge is bad. Fix the question wording, not the judge.

Checklist questions are typically mechanically clear by design — "Does the output contain column headers?" leaves little room for interpretation. Calibration usually passes first try. If it doesn't, the question wording needs tightening.

#### Step 4: Act on Results

| Condition                  | What it means                             | Action                                                       |
| -------------------------- | ----------------------------------------- | ------------------------------------------------------------ |
| TPR ≥ 80% AND TNR ≥ 80%    | Criteria are mechanically clear. Proceed. |                                                              |
| TPR < 80%                  | "Should be YES" criteria too vague        | Make questions more specific. Add concrete, observable markers. Re-test. |
| TNR < 80%                  | "Should be NO" criteria too vague         | Make questions more specific. Remove any room for interpretation. Re-test. |
| Both < 80% after 2 retries | These items are inherently subjective     | Accept best result. Annotate `criteria_partial: true`.       |

#### Step 5: Record

```
criteria_calibrated: true (or partial)
tpr: 0.XX
tnr: 0.XX
```

---

### Phase 3: Baseline Assessment

For each skill. The baseline logic differs by mode.

#### Common Step

1. Read SKILL.md. Score structural dimensions 1-7. One-line reason per dimension.

#### Optimize Mode

2. Spawn judge agent. For each test input, run the skill and answer every checklist question yes/no. `pass_rate = total "yes" / (questions × inputs)`.
3. `total = structural + pass_rate × 25`.
4. Append baseline row to `results.tsv`.

#### Create Mode — Dual Baseline

2. Spawn judge agent. Run **two passes** with the same checklist:

| Pass              | What                                                         | Purpose                             |
| ----------------- | ------------------------------------------------------------ | ----------------------------------- |
| **With-skill**    | Load the draft skill, run each test input                    | Baseline 0 for the ratchet          |
| **Without-skill** | Bare Claude — no skill loaded, same test inputs + same checklist | Reference: proves the skill's value |

3. Compute:

```
pass_rate_with    = total "yes" / (questions × inputs)  [with skill loaded]
pass_rate_without = total "yes" / (questions × inputs)  [bare Claude]

total_with    = structural + pass_rate_with × 25    → enters ratchet as baseline 0
total_without = structural + pass_rate_without × 25  → reference only
```

4. Append **one** baseline row to `results.tsv` using `total_with`. Record `total_without` in the note field for the final report (Phase 6).

**Why bare Claude?** It quantifies the skill's absolute value: "封装这个 skill 后，成功率从 X% 提升到了 Y%。" But it doesn't participate in the ratchet — the ratchet only compares with-skill versions (baseline 0 → Round 1 → Round 2 → Round 3).

Log the scorecard and proceed directly to Phase 4. No pause — the checklist and judge were already confirmed in Phases 1-2.

---

### Phase 4: Optimization

Process skills from lowest score to highest. Max 3 rounds per skill. **No human intervention — runs autonomously.**

Each round has 5 steps:

| Step            | What                                   | Who                          |
| --------------- | -------------------------------------- | ---------------------------- |
| 1. Diagnose     | Find the ONE weakest point             | Main agent                   |
| 2. Edit         | Fix it. git commit.                    | Main agent                   |
| 3. Review+Score | Critique the change + re-run all tests | **Independent review agent** |
| 4. Decide       | Keep if score improved, revert if not  | Main agent                   |
| 5. Log          | Write changelog entry                  | Main agent                   |

No pauses between rounds or between skills. Run until all skills hit their ceiling (no improvement after 1 round) or reach 3 rounds.

#### Step 1: Diagnose

Pick ONE target:

- Any structural dimension scored ≤ 5? → Target that dimension.
- ≥2 checklist questions consistently "no" across inputs? → Target that capability.
- Otherwise: target the capability with the lowest "yes" rate.

#### Step 2: Edit

- State: which lines, which target, expected impact.
- Edit SKILL.md.
- Git commit: `"optimize {skill}: {brief summary}"`.

#### Step 3: Adversarial Review + Same-Judge Re-score

**Spawn ONE independent agent.** Give it:

- The ORIGINAL SKILL.md (baseline, before any edits)
- The OPTIMIZED SKILL.md (after your edit)
- The git diff of your change
- The target problem you were trying to fix
- test-checklist.json

Do NOT give it your reasoning or diagnosis.

The review agent has a dual role — **critic** and **judge**:

**As critic:**

1. Did this change actually fix the target problem? (Yes / Partially / No)
2. Did it introduce new problems? (list specific issues, or "None")
3. Is there a simpler way to achieve the same fix? (suggest, or "No")
4. Overall quality of this change: /10
5. Semantic trigger blind-spot check: Imagine you are a user who needs this skill but expresses the request in vague, colloquial, or incomplete language. Write 3 user queries that SHOULD trigger this skill but might fail because the description doesn't cover them. If the current description would cover all 3, state "All covered". Otherwise, suggest which phrases to add to the description.

**As judge — scores BOTH versions in the same call:**

6. Baseline: yes/no per checklist question per input + baseline pass_rate
7. Optimized: yes/no per checklist question per input + new pass_rate
8. Delta: new pass_rate − baseline pass_rate

**Why both in one call?** Each sub-agent spawn is a fresh instance with its own judgment thresholds. Having the SAME judge score BOTH versions eliminates judge variance — the delta is real improvement, not "a different judge was more lenient."

If review score < 6/10 or answer to Q1 is "No": go back to Step 1 (re-diagnose).
If 6-7/10: address the specific issues raised, re-submit to review (no extra round counted).
If ≥ 8/10: proceed to Step 4.

Critical rule: **the agent that edited must not score.** Review agent has zero memory of the edit process and only sees diff + both skill versions + checklist.

#### Step 4: Decide

```
new_total > old_total → keep (update baseline)
new_total ≤ old_total → git revert HEAD --no-edit, log failure, break (ceiling reached)
```

Append row to `results.tsv` regardless.

#### Step 5: Write Changelog

After every round (keep or revert), append an entry to `{skill-dir}/changelog.md`. The changelog is a permanent knowledge base — future optimization sessions on the same skill can read it to avoid retrying approaches that already proved ineffective.

Each entry records the WHY, not just the WHAT:

```markdown
## Round 1 (YYYY-MM-DD HH:MM)

- **诊断**: Q4 整行 0/10 — skill 没有显式指令处理非 JSON 输入
- **改动**: Agent Prompt Step 1 新增一条分支："如果输入不是合法 JSON 也不是 CSV，停止并返回错误提示"
- **审稿评价**: 8/10 — 方向正确，建议同时在 Troubleshooting 加一条对应说明
- **结果**: 77.6 → 82.8 (+5.2)
- **通过率**: 83.3% → 100%
- **决定**: KEEP
- **为何有效**: 2 行指令补上了一个明确的逻辑缺口。之前 skill 的 Step 1 只说了"识别 JSON 还是 CSV"，没写"都不是怎么办"——agent 遇到非 JSON 直接掉进 jq 原始报错。加上之后就闭环了。
```

If the round was REVERTED:

```markdown
## Round 2 (YYYY-MM-DD HH:MM)

- **诊断**: 维度 4（检查点设计）得分 2.1，想加安装前确认步骤
- **改动**: 在 Step 5 加 "Ask user to confirm before running npx skills add"
- **审稿评价**: 5/10 — 增加了无意义摩擦，skill 的 Step 6 已经有 -y 跳过确认的场景
- **结果**: 82.8 → 80.5 (-2.3)
- **通过率**: 100% → 95%
- **决定**: REVERT
- **为何失败**: 加确认步骤反而让现有功能退化。用户在 Step 6 已经可以选择 -y 跳过，多问一次是多余摩擦。
```

Rules:

- One entry per round, always appended at the top (latest first)
- If `changelog.md` does not exist, create it with a `# Changelog — {skill-name}` header
- Be honest about why something failed — the failures are as valuable as successes for future reference
- Link to the git commit hash so the exact change can be inspected later

#### Fix Priority

| Priority | Trigger                                                | Action                                                       |
| -------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| P0       | ≥2 checklist questions consistently "no" across inputs | Fix that capability's instructions                           |
| P1       | Structural dimension ≤ 5                               | Fix that structural weakness                                 |
| P1       | Frontmatter missing trigger keywords                   | Add Chinese + English triggers. Do NOT just add synonyms — generate keywords by asking: "If a user only knew about this skill through its edge cases (e.g. a specific file format, a rare input type, a partial workflow), what would they type?" Keywords must cover the boundary conditions identified in Phase 0 Intent Expansion. |
| P2       | Step is vague                                          | Replace with specific parameters and format                  |
| P2       | Missing error handling                                 | Add "if X fails, then Y"                                     |
| P3       | Paragraph too long or repeated                         | Split / merge                                                |

---

### Phase 5: Exploratory Rewrite

Trigger: a skill hits its ceiling after 1-2 rounds with no improvement, AND structural score is still < 50.

Requires explicit user consent.

```
1. git stash current version.
2. Rewrite SKILL.md from scratch (restructure, not micro-edit).
3. Re-run Phase 3 (Baseline) with fresh judge.
4. If rewrite > stashed: adopt. Else: git stash pop.
```

---

### Phase 6: Report & Package

#### Report

Display overview table:

```
┌──────────────────────┬────────┬────────┬────────┬──────────────┐
│ Skill                │ Before │ After  │ Δ      │ Pass Rate Δ   │
├──────────────────────┼────────┼────────┼────────┼───────────────┤
│ {name}               │ 63.6   │ 78.2   │ +14.6  │ 55% → 85%     │
└──────────────────────┴────────┴────────┴────────┴───────────────┘
```

For **create mode**, also show the without-skill reference anchor:

```
裸 Claude (无 Skill): 52.3  →  封装后: 78.2  (+25.9)
```

#### Package

If the skill was created or significantly improved, offer to package as `.skill` file for distribution:

```bash
cd .claude/skills/auto-skill-forge && python -m scripts.package_skill <path/to/skill-folder>
```

---

## Data Files

### results.tsv

Location: `.claude/skills/auto-skill-forge/results.tsv`

```tsv
timestamp	commit	skill	old_score	new_score	status	dimension	note	eval_mode	pass_rate
2026-05-09T10:00	baseline	meeting-notes	-	62.5	baseline	-	Initial assessment	dry_run	0.55
2026-05-09T10:15	a1b2c3d	meeting-notes	62.5	78.2	keep	Edge cases	Q3,Q5 no→yes	sub_agent	0.85
```

For create mode baseline rows, include bare-Claude reference score in the note field: `note=bare_claude:52.3`.

### test-checklist.json

Location: `{skill-dir}/test-checklist.json`. Format defined in Phase 1 Step 5.

### changelog.md

Location: `{skill-dir}/changelog.md`. Format and rules defined in Phase 4 Step 5.

## Exception Handling

Always notify user before applying a fallback. Never silently skip.

| Condition                                     | Action                                                       |
| --------------------------------------------- | ------------------------------------------------------------ |
| Not a git repo                                | Ask user to `git init`. If declined: backup files as `.bak.YYYYMMDD-HHMM` instead of git revert. |
| results.tsv missing                           | Create with header row.                                      |
| Branch name collision                         | Append `-2`/`-3`. After 3 failures, switch to existing branch and ask. |
| git revert fails                              | `git stash`, retry. Still failing: extract file from previous commit manually. |
| 3 rounds reached (ceiling)                    | Show remaining gaps. Ask: add one more round / Phase 5 rewrite / stop. |
| File > 150% original size                     | Reject commit. Trim redundancy. Re-score.                    |
| test-checklist.json already exists            | Ask: reuse / rewrite / append.                               |
| SKILL.md not found                            | Terminate that skill. Write `status=error`. Continue to next. |
| No sub-agent for judge                        | Fall back to dry-run. Main agent evaluates directly. Note `eval_mode=dry_run`. |
| Creation mode: user declines Intent Expansion | Proceed without it, but warn: "没有扩展边界，checklist 可能测不出草稿的隐性缺陷。" |

## Anti-Patterns

- Changing the skill's core purpose. Only improve how it's written and executed.
- Adding new dependencies or scripts the skill didn't already have.
- Editing multiple unrelated dimensions in one round. One change at a time.
- Growing SKILL.md beyond 150% of original size.
- Using `git reset --hard` instead of `git revert`.
- Re-using the same agent context for editing and scoring.
- Writing checklist questions with subjective language ("Is the output good?"). Every question must be mechanically yes/no.
- Creating more than 6 checklist questions. More leads to checklist gaming, not genuine improvement.
- **Skipping Intent Expansion in create mode.** Without it, the agent grades its own homework and the draft scores artificially high — Phase 4 has nothing to fix and the skill ships with hidden gaps.