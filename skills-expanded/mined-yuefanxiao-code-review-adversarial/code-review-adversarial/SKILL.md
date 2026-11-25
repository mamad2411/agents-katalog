---
name: code-review-adversarial
description: >
  Deep code review via a committee of specialized reviewers with PR-type-aware
  playbooks and convergence. Feature PRs → evaluate better alternatives; bugfix PRs →
  verify fix correctness + regression; design-heavy PRs (proto/contract only) →
  AIP/compatibility audit. Dispatches 2-4 reviewers from distinct stances, converges
  via collaborative arbiter, outputs structured verdict. Use for high-stakes PRs
  (concurrency, security, contract changes) or when the user asks for "深度评审",
  "对抗复核", "adversarial review", or "契约评审".
---

# code-review-adversarial

Deep code review engine that dispatches a committee of specialized reviewers, converges their findings, and outputs a structured verdict. PR-type-aware: feature PRs are evaluated for better alternatives; bugfix PRs are evaluated for fix correctness + regression introduction.

**Design doc**: `DESIGN.md` (in this skill's directory) — full design rationale, research references, and decision records.

**Reference files** (loaded on demand):
- `references/type-playbooks.md` — per-PR-type review checklists
- `references/reviewer-personas.md` — reviewer persona prompt templates
- `references/convergence-protocol.md` — convergence and arbitration rules

## When to use

- High-stakes PR: concurrency, security, API/contract changes
- User explicitly asks for adversarial / multi-agent / deep review
- Feature PR where solution quality matters (is there a better approach?)
- Bugfix PR where correctness and regression risk matter

## When NOT to use

- Routine PR quick pass (use a single reviewer)
- Pure merge/rebase with no logic changes
- User wants fast feedback, not deep analysis (this is expensive: 2-4 sub-agents)

## Arguments

Parse `$ARGUMENTS` loosely:

- **PR target (required)**: `PR #<N>`, `#<N>`, `<N>`, or full PR URL (GitHub/GitLab/Gitea).
- `reviewers:<comma-list>` — manually specify personas (overrides type-based auto-selection). Accepted tokens: `design`, `correctness`, `security`, `root-cause`, `regression`, `behavior`, `test-coverage`, `perf`, `devils-advocate`.
- `devils-advocate` or `--devils-advocate` — enable devil's advocate persona (high-stakes PRs).
- `max-rounds:<N>` — convergence round limit (default: 2).
- `format:<markdown|json|comment>` — output mode (default: `markdown`). `comment` asks user before posting.
- `pr-type:<type>` — manually specify PR type, overrides auto-classification. Accepted: `feature`, `bugfix`, `refactor`, `performance`, `chore`, `docs`, `test`.

If `$ARGUMENTS` is empty, stop and ask the user for a PR number or diff.

---

## Workflow

### Phase 0: Baseline（基线锁定）

确定 PR 真正改了哪些文件，防止 diff 污染。产出 `correct-diff.patch` 作为所有 reviewer 的评审基线。Phase 0 不限制 reviewer 能探索哪些文件——那是自由探索（Phase 2）。

基线必须 **unpolluted** — 如果连评审对象都搞错了，后面所有评审都是空中楼阁。

1. **Fetch PR metadata**. Use your platform's CLI or API (`gh pr`, `tea pr`, GitLab API, etc.) → base ref, head ref, title, labels, body, changed_files count.
2. **Lock merge-base** (critical — prevents diff pollution):
   ```bash
   git fetch origin "$BASE_REF" "$HEAD_REF"
   BASE=$(git merge-base origin/"$BASE_REF" origin/"$HEAD_REF")
   ```
3. **Generate correct diff** (two-dot, NOT three-dot):
   ```bash
   git diff "$BASE..origin/$HEAD_REF" > /tmp/<pr>/correct-diff.patch
   ```
4. **Verify file count** matches PR metadata:
   ```bash
   git diff --name-only "$BASE..origin/$HEAD_REF" | wc -l
   # Must match changed_files from the PR metadata. Mismatch → abort, report anomaly.
   ```

**Hard constraints**:
- NEVER use `origin/base...origin/head` (three-dot symmetric diff). Use merge-base two-dot only.
- File count mismatch → abort, report the discrepancy.

**Output**: `correct-diff.patch` — the clean review baseline, passed to all reviewers.

---

### Phase 1: PR Type Classification

**Goal**: Determine PR type → select reviewer personas + load checklist.

**Classification** (priority descending):

1. **PR labels**: contains `bug` → bugfix; contains `feature` → feature
2. **Conventional Commits prefix**: `feat`/`fix`/`refactor`/`perf`/`chore`/`docs`/`test`
3. **PR title keywords**: "fix"/"修复" → bugfix; "add"/"新增"/"feat" → feature
4. **Diff analysis**: if existing tests modified (not new test files) → reclassify as feature/bugfix (refactor must not change test behavior)

**Design-heavy detection**:
```bash
DESIGN_LINES=$(git diff "$BASE..origin/$HEAD_REF" -- '*.proto' '*.md' | grep -cE '^[+-]')
IMPL_LINES=$(git diff "$BASE..origin/$HEAD_REF" -- '*.go' '*.ts' '*.py' '*.java' '*.rs' | grep -cE '^[+-]')
# proto+md 占比 > 70% 且实现代码 < 30% → design-heavy: true
```

**Persona selection**: 按类型和 design-heavy 选角色。权威映射表（含 design-heavy override）在 `references/reviewer-personas.md` 的「角色与 PR 类型的映射速查」章节——读那里，不在这里重复。每个选中的 persona 读 `references/personas/<name>.md`。

**Fallback**: unrecognized types → use feature's personas (strictest).

**Output**: `pr_type` + `design-heavy: bool` + selected persona list + loaded checklist from `references/type-playbooks.md`.

---

### Phase 2: Reviewer Dispatch

**Goal**: Dispatch persona committee in parallel. Each persona covers one dimension.

**Prompt assembly** — 固定内容在前，变化内容在后（最大化 prompt cache 命中）:

```
[1. 通用约束]        ← 共享前缀（所有角色相同），from references/reviewer-personas.md
[2. correct-diff.patch]  ← 共享前缀
[3. PR 元数据]       ← 共享前缀（title / description / issue link）
[4. personas/<name>.md]  ← 变化部分，放最后。只读该角色文件
```

**Dispatch**: Use the Agent tool to launch all selected personas **in parallel** (multiple tool calls in one message). Each agent gets:
- The assembled prompt (通用约束 + diff + 元数据 + 角色专有)
- `correct-diff.patch` content as review baseline
- PR metadata (title, description, issue link if any)
- Repo path for free exploration

**Output schema** (each reviewer returns this — 8 fields, enforced):

```json
{
  "persona": "<role-name>",
  "verdict": "ready | ready-with-fixes | not-ready",
  "findings": [
    {
      "severity": "P0|P1|P2|P3",
      "type": "correctness|design|security|root-cause|regression",
      "file": "<path>",
      "line": <N>,
      "issue": "<one-line description>",
      "evidence": "<file:line + reasoning>",
      "confidence": <1-10>
    }
  ],
  "verified_correct": ["<confirmed-correct points>"]
}
```

`in_diff` / `finding_category` etc. are NOT filled by reviewers — Triage Filter (Phase 3) determines them automatically from file paths.

---

### Phase 3: Triage Filter

**Goal**: Discard invalid findings before convergence. Every surviving finding must be **diff-anchored** — it either points at a diff line, or proves the diff broke something outside it. Findings that float free of the diff are noise; drop them.

#### Step 1: Infer component scope

```bash
# Infer components from diff file paths
git diff --name-only "$BASE..origin/$HEAD_REF" | \
  sed 's|^\([^/]*\)/.*|\1|' | sort -u
# Example: api bss dashboard
#
# Further细分 (e.g. dashboard → backend / ui):
# api/                          → api
# bss/bss-invoice-service/      → bss-invoice-service
# dashboard/dashboard-backend/  → dashboard-backend
```

Output: `component-scope` set (e.g. `{api, bss-invoice-service, dashboard-backend}`).

#### Step 2: Apply discard rules

| Rule | Condition | Rationale |
|---|---|---|
| **component out-of-scope** | finding's file belongs to a component NOT in `component-scope` | PR semantic boundary — a backend PR doesn't review frontend, regardless of call-chain depth |
| **scope violation** | finding's file is outside diff AND finding is an "improvement" type (not "diffusion-impact") | Improvement suggestions not allowed on out-of-diff files; diffusion-impact (compile error, interface break) is allowed |
| **no citation** | finding has no `file:line` | Can't locate = invalid |
| **layer violation** | bugfix PR receives L3 finding ("consider alternatives"); refactor PR receives "add feature" | PR type determines allowed layers |
| **already fixed** | finding points to code already fixed in this PR | Stale |
| **implementation-speculation** (design-heavy only) | finding hypothesizes about implementation behavior that doesn't exist yet (e.g. "this function should handle nil" when there's no implementation) | Design-heavy PR has no implementation code; critiquing hypothetical implementation is premature — that's the next PR's job |

**Two scope rules — the distinction**:
- **component out-of-scope**: file belongs to a completely unrelated component (backend PR reviewing frontend) → discard regardless of finding type. This is the PR's semantic boundary.
- **scope violation**: file is outside diff but within a related component → only discard "improvement" type; keep "diffusion-impact" type. This allows reviewers to catch "the diff broke another file in the same component".

**Design-heavy 补充规则**: 当 `design-heavy: true` 时，「implementation-speculation」规则激活——丢弃所有对「尚未存在的实现行为」的推测性 finding。保留契约层 finding（兼容性、命名、字段编号、AIP 合规、错误码完备性）。判据：finding 引用的文件是 `.proto`/`.md`/接口定义 → 保留；引用的是 `.go`/`.ts` 等实现文件且该文件不在 diff 内（说明实现还没写）→ 丢弃。

**Output**: surviving findings + discarded findings (with discard reason, for transparency).

---

### Phase 4: Convergence

**Goal**: Converge multiple reviewers' surviving findings into a consistent verdict.

Every verdict and finding disposition must be **evidence-bound** — backed by a `file:line` citation the coordinator can verify. No evidence, no verdict. Load `references/convergence-protocol.md` for full rules. Summary:

#### Step 1: Build finding matrix

Group all surviving findings by "same issue" (same file:line + same defect).

#### Step 2: Converge by group type

| Group type | Definition | Action |
|---|---|---|
| **independent** | only one reviewer reported it | accept directly |
| **intersection** | 2+ reviewers reported same issue, severity agrees (±1) | high-confidence accept, take highest severity |
| **conflict** | 2+ reviewers reported same issue, severity disagrees (≥2 levels) or verdict contradicts | coordinator must arbitrate |

#### Step 3: Arbitrate conflicts

Coordinator reads code, independently judges. If code facts are insufficient → convergence round (Step 4).

#### Step 4: Convergence round (if needed)

1. **Prefer SendMessage** to wake surviving agents (saves tokens, preserves context).
2. If agent terminated → **re-dispatch** via Agent tool with coordinator's ruling + conflict summary + code locations as new prompt.
3. Send the convergence-round prompt template (from `references/convergence-protocol.md`).
4. **Guardrails**: max 2 rounds (default). Check stability after each round. Unresolved at limit → label "unresolved", list both sides, don't force-merge.

#### Step 5: Determine verdict

```
Count surviving findings (post-Triage + post-Convergence):

has P0              → not-ready
has P1, no P0       → ready-with-fixes
only P2/P3          → ready-with-fixes
no findings         → ready
```

**Convergence complete** when: all surviving findings have a disposition (fix-in-pr / followup / rejected) AND all conflicts are arbitrated AND unresolved disagreements (if any) are explicitly labeled.

---

## Output

Based on `format` argument:

### `format: markdown` (default)

产出评审报告的 markdown 文本，**返回给调用方**。不自动发 PR comment。
如果调用方想把报告发到 PR，由调用方决定，或用 AskUserQuestion 询问用户后再发。

### `format: json`

Return structured JSON to the caller (no PR comment posted):

```json
{
  "pr_type": "<type>",
  "verdict": "<ready|ready-with-fixes|not-ready>",
  "reviewers": [{"persona": "...", "verdict": "...", "findings_count": N}],
  "findings": [
    {
      "id": "F1",
      "severity": "P1",
      "type": "root-cause",
      "persona": "root-cause-auditor",
      "file": "...",
      "line": N,
      "issue": "...",
      "disposition": "fix-in-pr|followup|rejected",
      "consensus": "independent|intersection|arbiter-ruled|unresolved",
      "confidence": N
    }
  ],
  "triage": {"discarded": [{"reason": "...", "detail": "..."}]},
  "convergence": {"rounds": N, "conflicts_resolved": N, "unresolved": []}
}
```

### `format: comment`

产出精简 markdown 并**询问用户**确认后再发 PR comment。绝不自动发布。

**硬约束**: 必须先用 AskUserQuestion 询问用户「是否将评审报告发布到 PR？」，用户确认后才发。用户拒绝则只返回报告文本。

报告模板（精简版，只含决策必需信息）:

```markdown
## 对抗评审报告

**Verdict**: <ready/ready-with-fixes/not-ready>（PR 类型: <type>，置信度: <high/medium/low>）

### Finding 表
| # | 严重度 | 位置 | 问题 | 处理 |
|---|--------|------|------|------|

（如有 P0/P1 冲突仲裁）
- <finding> → <裁决>：<一句话理由>

（如仅 P2/P3）
> 残留 <N> 项 P2/P3（<类型>），建议 follow-up 跟踪，不阻塞合入。
```

---

## Safety rules

- **Never auto-comment to PR.** Default format is `markdown` (return text only). Even in `format: comment` mode, you MUST ask the user via AskUserQuestion before posting. The user says no → return text only.
- **Do not merge** unless the user explicitly asks AND verdict is ready/ready-with-fixes AND all blocking findings are addressed.
- **Do not push fixes** to someone else's PR.
- **Worktree cleanliness**: never switch branches on a dirty tree.
- **Diff baseline integrity**: Phase 0's merge-base lock is non-negotiable. If you can't verify the file count, stop and report.

---

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `reviewers` | auto by PR type | Manually specify personas (e.g. `reviewers:design,security`) |
| `devils-advocate` | off | Enable devil's advocate (high-stakes PRs) |
| `max-rounds` | 2 | Convergence round limit |
| `format` | markdown | Output: `markdown` (text only, default) / `json` (structured return) / `comment` (ask user before posting to PR) |
| `pr-type` | auto-classify | Manually specify PR type (overrides auto) |

---

## Design rationale

Full design decisions and research references: see `DESIGN.md` §2 (in this skill's directory).
