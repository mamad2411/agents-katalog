---
name: fanout-review
description: "Multi-perspective code review with breaking-change detection, a deterministic merge gate, and questions for the dev. Spawns 6 parallel reviewers. Output optimized for PR-thread copy/paste, supporting GitHub, GitLab, or Azure DevOps (emoji semaphore, lists, backticked code)."
---

# Code review (multi-perspective)

Review the current branch by dispatching **6 parallel review tasks** (one mandate each), then synthesize findings into a categorical merge-gate decision (🚫 BLOCK / ⚠️ NEEDS DISCUSSION / ✅ CLEAR) backed by a risk profile and deterministic blocker checks. Output is designed to paste directly into a PR thread (GitHub, GitLab, or Azure DevOps).

## Mode detection

Read the user invocation prompt:

- Contains `quick`, `shallow`, or `fast` -> **single-pass mode** (skip fanout, lean output)
- Diff size below ~50 lines AND mode not explicitly stated -> ask the user once whether to do single-pass; default to single-pass if unanswered
- Otherwise -> **fanout mode** (default)

## Scope detection

Read the user invocation prompt:

- Mentions `committed`, `this branch`, `PR`, or `main..HEAD` -> scope to **committed changes only** (`git diff main..HEAD`)
- Mentions `staged` -> scope to `git diff --cached`
- Otherwise -> include **all changes** (committed + staged + unstaged)

Base branch resolution, in order:

1. If the user prompt names a branch (`vs feat/X`, `against develop`), use it.
2. Else `git symbolic-ref refs/remotes/origin/HEAD` if it resolves.
3. Else `main` if it exists locally, else `master`.
4. If neither exists, stop and ask the user which base to diff against. Do not silently fall back to `HEAD~1`.

---

## Fanout mode

### Step 1: Gather diff context

Run (substitute scope from detection above):

```bash
git diff <scope> --stat
git diff <scope> --name-status
git log <scope> --no-merges --pretty=format:"%h %s"
```

### Step 2: Dispatch 6 review tasks

Dispatch the review across 6 independent perspectives.

**Multi-runtime execution guidelines:**
- **Claude Code**: Use the `Agent` tool with `subagent_type: general-purpose`. Send all 6 tasks in a single turn with 6 tool calls for concurrent execution.
- **Antigravity / Gemini CLI**: Use `invoke_subagent` with 6 parallel entries in the `Subagents` array.
- **Single-agent runtimes (such as GitHub Copilot CLI)**: When parallel subagents are unavailable, evaluate each of the 6 review perspectives sequentially, accumulating JSON findings into context.

Each subagent or perspective receives the diff context, one task description below, and the JSON return contract.

**Task descriptions** (each subagent receives exactly one):

- **security**: Find OWASP Top 10 violations, secrets in code, input-validation gaps, authz/authn gaps, injection (SQL/cmd/path), unsafe deserialization, and weak crypto. Use `category: "security"` in the return.
- **performance**: Find hotspots, N+1 queries, unnecessary work in loops, allocation pressure, blocking I/O on hot paths, and missing memoization. Use `category: "performance"`.
- **breaking-change**: For each file in the diff, run `git show <base-branch>:<path>` and compare against the new version. Flag changed function signatures (added/removed/renamed params, changed return type), removed exports, schema/migration changes, env-var removals, feature-flag removals, behavior changes in public APIs, and removed config keys. Use `category: "breaking-change"`.
- **test-coverage**: Find missing tests for new code paths, untested edge cases (empty/null/boundary), redundant tests, and test-quality issues (AAA, FIRST, flakiness, mocks of external deps). Use `category: "test"`.
- **readability**: Find naming inconsistencies vs project conventions, unclear variable/function names, missing or excessive comments, magic numbers, and excessive function length/complexity. Use `category: "readability"`.
- **dry-solid**: Find DRY violations (3+ similar implementations), SOLID violations, dead code, antipatterns, and leaky abstractions. **DRY is project priority**; weight findings here higher than readability. Use `category: "dry-solid"`. When a DRY violation spans multiple files, set `location` to the **canonical** file (the natural home for the extracted abstraction, else first by path order) and list the remaining occurrences in `duplicate_locations`; do **not** concatenate multiple `file:lines` into one `location` string.

### Step 3: Return contract for each subagent

Each subagent MUST return its result as a **single JSON object**, no surrounding prose:

```json
{
  "findings": [
    {
      "category": "security|performance|breaking-change|test|readability|dry-solid",
      "severity": "critical|improvement|quick-win",
      "location": "path/to/file.ext:42-58",
      "duplicate_locations": ["path/b.ext:178-218", "path/c.ext:162-202"],
      "summary": "one-line description",
      "details": "what is wrong and why it matters: for breaking-change include what consumers/callers it affects and how they must adapt; for performance include the root cause and Big-O or concrete impact metric",
      "suggestion": "concrete fix recommendation (description only, no edits)",
      "question_for_dev": "what to ask the author: only if clarification is needed before deciding severity, else null"
    }
  ]
}
```

`duplicate_locations` is **optional**: populate it only when **one root cause repeats across files** (typical for `dry-solid`). When set, `location` is the **primary/canonical** occurrence: the natural home for the extracted abstraction (else first by path order), and `duplicate_locations` lists the other `file:lines` where the same code recurs. Omit it or use `[]` for single-location findings.

If a reviewer finds nothing, it returns `{"findings": []}`.

### Step 4: Synthesis (main agent)

The synthesis does NOT use consensus math. PR review is a per-decision call, not a sample-ranking problem; we use **deterministic blocker checks**, **categorical risk heuristics**, and **severity-driven aggregation**.

#### 4a: Deterministic blocker checks

Run against the **diff itself**, not against finding-counts. Each is a binary categorical check:

- **Tests missing**: `git diff <scope> --name-only` shows non-test files but no `*test*` / `*spec*` / `*.test.*` / `*.spec.*` files. _Treatment: BLOCKER candidate._
- **Secrets in diff**: path matches `*.env*` (excluding `.env.example`), `*secrets*`, `*credentials*`, `*.pem`, `*.key`. _Treatment: BLOCKER._
- **Deps without lockfile**: `package.json` is in the diff but `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` is not. _Treatment: BLOCKER candidate._
- **Migration files**: path matches `*/migrations/*`, `*migration_*`, `*/db/migrate/*`. _Treatment: RISK flag._
- **Critical-path files**: path matches `*/auth/*`, `*/security/*`, `*/config/*`, `.github/workflows/*`, `*/ci/*`, `*/infra/*`. _Treatment: RISK flag._
- **Large single-file delta**: `--stat` shows any file with >500 lines changed. _Treatment: RISK flag._
- **New external dependency**: `package.json` diff adds a `dependencies` / `devDependencies` entry, OR a new top-level `import` / `require` of an unfamiliar package. _Treatment: RISK flag._

#### 4b: Aggregate findings

**Dispatch checkpoint (run before grouping):**

Count how many of the 6 dispatched tasks returned a valid JSON object. State the count explicitly inside the output `## Risk profile` block on a `Dispatched:` line, e.g.:

`Dispatched: 6 of 6 returned (security ✓, performance ✓, breaking-change ✓, test ✓, readability ✓, dry-solid ✓).`

If any task returned invalid JSON, did not return at all, or returned an error:

- List the missing categories in the `Dispatched:` line with `(no response)`.
- In `## Findings`, render the missing categories headings with the literal text `_(not reviewed: re-run with subagent_type=general-purpose)_` instead of dropping them silently.
- Do **not** treat a missing category as "no findings found there." A category with `{"findings": []}` is reviewed-and-clean; a missing one is unreviewed.

**Then aggregate the returned findings:**

- Parse the JSON outputs from the tasks that responded.
- Group by **severity** (critical -> improvement -> quick-win).
- Within severity, group by **category** in this order: security -> breaking-change -> performance -> test -> dry-solid -> readability.
- **Annotate** any finding whose `location` targets a risk-flagged file: append ` ⚠️ _(critical path: <reason>)_` to the summary line.
- **Dedup**: if two tasks flagged the exact same line range with the same root cause, merge into one entry crediting both categories (e.g., `category: security + dry-solid`).

#### 4c: Compute merge gate

A single explicit decision goes at the top of the output. The gate is a **recommendation** to the human reviewer: surface which signals drove it so the user can override with context.

- 🚫 **BLOCK**: Any `critical` finding in `security` or `breaking-change` categories, OR any deterministic **BLOCKER** / **BLOCKER candidate**.
- ⚠️ **NEEDS DISCUSSION**: Any `critical` finding in any other category, OR any **RISK flag**, OR any non-null `question_for_dev`.
- ✅ **CLEAR**: No critical findings, no risk flags, no blockers.

---

## Output template (canonical, used by both modes)

This is the ONE shape that gets rendered. Single-pass mode uses the same template minus the post-findings blocks (see below).

### Rendering rules

- **Code identifiers in backticks**: every file path, function name, variable, env var, package name, and line range must be wrapped in backticks. This makes PR platforms (GitHub, GitLab, Azure DevOps) render them as inline code.
- **Semaphore emojis**: use exactly the emojis specified in the template; do not substitute.
- **No tables**: every list is a Markdown bullet list. Tables do not always render cleanly in ADO PR threads.
- **Omit empty sections**: if a category has no findings at that severity, drop the `#### Category` heading. If a severity has no findings at all, drop the `### 🔴/🟡/🟢 Severity` heading. If no questions exist for a topic, drop that topic from the Questions block.
- **Inline severity tag**: every finding header line begins with a severity tag matching its grouping: `🔴 _Critical_`, `🟡 _Improvement_`, or `🟢 _Quick win_`. This is intentional redundancy with the `### 🔴/🟡/🟢` grouping headers; it keeps the severity attached when a single finding is copied out of its section into a PR thread.
- **Finding separators**: insert a `---` horizontal rule between consecutive findings as a visual border for copy/paste. Do not place one immediately before a `####`/`###` heading (headings already separate groups).
- **Per-category render shape**: security / test / readability use the 2-sub-bullet shape (`Why it matters`, `Suggested fix`). **Breaking-change, performance, and dry-solid get expanded shapes** (below); the model derives the extra sub-fields from the subagent `details` text (and, for dry-solid, from `duplicate_locations`).

### Template

```markdown
## 🚫 Merge gate: BLOCK
> <1–2 sentence justification citing the specific blockers or risk signals that drove the decision>

## Risk profile

- **Dispatched**: <e.g., "6 of 6 returned" or "5 of 6 returned (test: no response)">
- **Diff size**: `X files`, `+Y / −Z LOC`
- **Tests touched**: yes | no | partial
- **Critical-path files**:
  - `path/one`
  - `path/two`
  - _(or "none")_
- **Deterministic blockers**:
  - 🚫 <description>
  - _(or "none")_
- **Risk flags**:
  - ⚠️ <description>
  - _(or "none")_

## Findings

### 🔴 Critical

#### Security
- 🔴 _Critical_: **`path/to/file.ext:42-58`**: <summary> ⚠️ _(critical path: <reason>, only if applicable)_
  - **Why it matters**: <details>
  - **Suggested fix**: <suggestion>

#### Breaking change
- 🔴 _Critical_: **`path/to/file.ext:42-58`**: <summary>
  - **What breaks**: <which consumers / callers / downstream services are affected: be concrete: name the function, the public API, the schema, the env var that disappeared>
  - **Migration path**: <how callers must adapt: code-level steps, not vague advice>
  - **Why it matters**: <impact details if not already covered above>
  - **Suggested fix**: <suggestion>

#### Performance
- 🔴 _Critical_: **`path/to/file.ext:42-58`**: <summary>
  - **Why it's slow**: <root cause: algorithmic complexity, blocking I/O, allocation pressure, redundant work, etc.>
  - **Estimated impact**: <Big-O on the relevant input dimension, OR a concrete metric: e.g., "blocks event loop ~200ms with N=10k", "adds one query per item in a hot loop">
  - **Suggested fix**: <suggestion>

#### Test
- 🔴 _Critical_: **`path/to/file.ext:42-58`**: <summary>
  - **Why it matters**: <details>
  - **Suggested fix**: <suggestion>

#### DRY/SOLID
- 🔴 _Critical_: **`path/to/file.ext:42-58`**: <summary>
  - **Why it matters**: <details>
  - **Suggested fix**: <suggestion>
  - **Same code also in** _(only when `duplicate_locations` is non-empty)_:
    - **`path/to/other-b.ext:178-218`**: same code as `path/to/file.ext:42-58`
    - **`path/to/other-c.ext:162-202`**: same code as `path/to/file.ext:42-58`

---

- 🔴 _Critical_: **`path/to/another.ext:10-30`**: <summary of a second, unrelated finding>
  - **Why it matters**: <details>
  - **Suggested fix**: <suggestion>

#### Readability
- 🔴 _Critical_: **`path/to/file.ext:42-58`**: <summary>
  - **Why it matters**: <details>
  - **Suggested fix**: <suggestion>

### 🟡 Improvement
<same shape, grouped by category; header tag is `🟡 _Improvement_`; only render if findings exist at this severity>

### 🟢 Quick win
<same shape, grouped by category; header tag is `🟢 _Quick win_`; only render if findings exist at this severity>

## Questions for the dev

### Breaking changes (please confirm before merging)
- In `` `path:line` ``, <question text>.

### Security
- In `` `path:line` ``, <question text>.

### Performance
- In `` `path:line` ``, <question text>.

### Test coverage
- In `` `path:line` ``, <question text>.
```

If no questions at all, replace the entire Questions block with a single line:

```markdown
## Questions for the dev
No clarifications needed; findings above are actionable as-is.
```

### Post-findings sections (fanout mode only)

After the Questions block, add these blocks **only when applicable**:

```markdown
## Mentoring
<short paragraph if any finding is a strong learning opportunity: explain the underlying principle. Skip the heading entirely if nothing teachable.>

## Next steps
> Run `/create-unit-tests` then `/check-tests` to close the gaps.
<only included when any test-coverage finding exists>
```

---

## Single-pass mode (`quick`)

Skip the 6-subagent fanout. Read the diff yourself. Run the deterministic blocker checks (4a). Then emit the **same canonical output template above**, with these omissions:

- **Skip** `## Questions for the dev`
- **Skip** `## Mentoring`
- **Skip** `## Next steps`

Everything else: merge gate, risk profile, findings with their per-category render shapes, emoji semaphore, backticked code: stays identical.

---

## Rules

- **DO NOT implement fixes. DO NOT edit any files. Report only.**
- Technical facts and data overrule opinions and personal preferences.
- Match the current codebase conventions (naming, file layout, error-handling style) when proposing fixes.
- Address the code, not the developer. Examples: positive: "This function allocates inside a tight loop." negative: "You should know better than to allocate here."
- In fanout mode, merge-gate + risk-profile + questions-for-dev sections are mandatory (questions can be the single-line "No clarifications needed" form).
- If the branch has zero diff vs base, say so in one line and stop.
