---
name: pr-review
description: >
  Deep code-centric review of pull requests for the moving-frontend monorepo. Use when the user
  mentions reviewing a PR, triaging GitHub Copilot or CodeRabbit comments, doing a code review,
  or wants feedback on a team member's code. Also trigger for "리뷰", "PR 리뷰", "코드 리뷰",
  "review PR", "review this PR", "Copilot review", "GitHub Copilot review", or when a PR doc
  path or GitHub PR URL is provided. Performs independent deep code analysis with git-truth
  validation, provider-aware AI review triage, and educational Korean-language feedback.
  AI review triage is secondary — the review stands alone even with 0 Copilot/CodeRabbit comments.
---

# PR Review Skill

Help Eddie (team leader) efficiently review PRs through independent deep code analysis. Produce structured review documents with git-truth validation, scope-aware findings, educational feedback, and developer growth tracking.

## Settings

On startup, check for a settings file at `.claude/pr-review.local.md` (relative to the project root). If it exists, read the YAML frontmatter to configure behavior:

- `output_language` — review feedback language (default: `ko`)
- `default_review_source` — default `--review-source` value (default: `all`)
- `default_repo_path` — default `--repo-path` for auto mode (avoids passing it every time)
- `full_review_dimensions` / `quick_review_dimensions` — which of the 9 dimensions to check per mode
- `fix_forward_exclusions` — file patterns that fix-forward should never auto-modify
- `track_developer_profiles` — whether to create/update developer profiles

If the settings file doesn't exist, use the defaults defined in this skill. Settings from the file override the defaults. CLI flags (e.g., `--review-source copilot`) override settings.

**Output language**: Determined by `output_language` setting. Default: Korean with English technical terms (component names, TypeScript types, React concepts).

## Modes

1. **Full Review** (default) — Complete PR review: git-truth validation, deep code review, AI review triage (GitHub Copilot and/or CodeRabbit), developer tracking
2. **Quick Review** (`--quick`) — Skip AI review triage + developer history. Focused git-truth validation and streamlined code review. Use for fast turnaround when provider output is unavailable or irrelevant. The output document must **completely omit** the AI review triage section (not include it with a "skipped" note — omit it entirely). Quick mode also reduces review depth: focus on the top 5 dimensions (Bugs & Correctness, Architecture/FSD, React & TypeScript, Error Handling, Performance) and skip Sibling Consistency, DRY/Duplication, UI/Design System, and Accessibility unless an obvious issue is spotted. This produces a meaningfully shorter and faster review, not just the same review minus the triage section.
3. **Triage Only** (`--triage-only`) — Only process GitHub Copilot and/or CodeRabbit comments without deep code review
4. **Developer History** (`--history <github-id>`) — Show a developer's accumulated review patterns
5. **Auto Review** (`--auto <PR#>`) — Worktree-aware end-to-end pipeline: fetch PR data, run the full review, prepare a managed Round N record, generate provider-neutral artifacts, preview mutations safely, and only perform live commit/push/reply/resolve when `--live` is explicitly present. Auto mode executes the workflow; it does **not** invent autonomous review judgment. See Step 11.

## Parameters

When invoked, extract these from the user's message:

- **PR doc path** (required): Path to the PR document, typically `docs/pr-for-review/[TICKET-ID] ...md`
- **Branch name** (required): The feature branch to review, e.g. `ACME-595/split-place-card`
- **GitHub ID** (required): PR creator's GitHub username — extract from the PR doc title (`# [TICKET] Title by <github-id>`) or ask the user
- **Ticket ID** (auto-extracted): Extracted from PR title or branch name (e.g., `ACME-595`). Used for scope determination.
- **Review source** (optional): `--review-source <all|coderabbit|copilot|none>`. Default is `all` for Full Review / Triage Only / Auto Review and `none` for Quick Review.
- **Repo path** (auto mode): `--repo-path <abs-path>`. Explicit target product repo path for auto mode. If omitted, check `default_repo_path` from `.claude/pr-review.local.md` settings. If neither is set, resolve from the current working directory only; never guess across repos.
- **Review doc override** (auto mode): `--review-doc <path>`. Optional explicit Round N review record path. Resolution precedence is: explicit `--review-doc`, then `docs/reviews/<TICKET>-review.md` derived from the PR head branch basename, else fail fast.
- **Worktree policy** (auto mode): `--worktree auto|<abs-path>`. `auto` creates or reuses a deterministic clean worktree for the current PR round. An explicit path reuses or creates that worktree path. If the target repo has staged changes and no worktree option is supplied, auto mode must stop safely. Unstaged modifications are not considered dirty.
- **Dry run** (optional): `--dry-run`. Preview GitHub reply / thread-resolution mutations without posting them.
- **Live confirmation** (auto mode): `--live`. Required before commit, push, reply, or resolve actions happen. Without `--live`, `/pr-review --auto` stops after artifacts and previews are generated.
- **Flags** (optional): `--quick`, `--triage-only`, `--history <github-id>`, `--auto <PR#>`, `--review-source <...>`, `--repo-path <abs-path>`, `--review-doc <path>`, `--worktree auto|<abs-path>`, `--dry-run`, `--live`

If the user provides a GitHub PR URL instead of a local path, use `gh pr view <number> --json body` to fetch the content. Fall back to asking for a local doc path if `gh` is unavailable.

When `--auto` is used, the PR number replaces the need for a PR doc path — the skill fetches it automatically via `scripts/fetch-pr.sh`. Branch name, GitHub ID, provider latest-round metadata, and head-repo metadata are extracted from the fetched PR data.

When AI review triage is requested, prefer a PR URL/number or a fetched PR doc that has a sibling `*.review-data.json` file generated by `scripts/fetch-pr.sh`. Local markdown alone may include CodeRabbit text but usually will not include GitHub Copilot inline comments unless that sidecar JSON exists.

Auto mode hard rules:

- Resolve the target repo from `--repo-path` or the current working directory only. If neither resolves the correct repo, fail fast.
- If `--repo-path` is absent and the current working directory is not the PR target repo, stop immediately. Do **not** scan sibling directories, prior worktrees, or unrelated clones as a fallback.
- Validate the resolved local repo against the PR head repo and head branch before any fix-forward or GitHub mutation.
- Extract the ticket id from the PR head branch basename using exactly one `[A-Z][A-Z0-9]+-\d+` match. If zero or multiple matches exist, require `--review-doc`.
- Use `.pr-review/pr-<PR_NUMBER>/round-<N>/` inside the target repo as the canonical artifact directory for that round.
- Treat `.pr-review/` as local operational state only. Add it to the active worktree exclude file instead of editing the tracked product `.gitignore`.
- Review-doc contract: the authoritative source review doc must live inside the resolved target repo. When worktree mode is used, the workflow mirrors that review doc into the prepared worktree at the same repo-relative path before any managed Round N edits. All round updates happen in the worktree copy.
- Stop after dry-run previews unless `--live` is present. `--live` must fail if any selected latest-round decision remains `pending`.

---

## Execution Workflow

### Step 1: Parse PR Document + Extract Claims

Read the PR doc and extract structured data:

1. **Header**: ticket ID (e.g. `ACME-595`), title, author GitHub ID
2. **Features section** (`## ✨ Features`): what the PR claims to do → build a **claim list**
3. **Changes section** (`## 🔄 Changes`): component table, file tree → build a **claimed file list**
4. **Note available AI review providers** (do NOT read their content yet):
   - Check if a sibling `*.review-data.json` sidecar file exists (structured provider data)
   - Check if CodeRabbit sections exist in the PR doc (e.g., `<!-- auto-generated comment: release notes -->`)
   - Check if GitHub Copilot sections exist (e.g., `## Summary by GitHub Copilot`)
   - Record which providers have data available — actual comment extraction happens in Step 5
   - Note: inline summaries (CodeRabbit walkthrough, Copilot summary) may be visible when reading the PR doc. Do not let them influence your independent analysis in Step 4.

The claim list is used in Step 2 for git-truth validation. Provider guides are loaded in Step 5:

- `references/coderabbit-triage-guide.md`
- `references/copilot-triage-guide.md`

### Step 2: Git-Truth Validation

Verify PR document claims against the actual git diff. Load `references/review-criteria.md` Section J.

**Repo access requirement**: Steps 2-4 require access to the actual git repository. Resolution order:
1. `--repo-path` if provided
2. `default_repo_path` from `.claude/pr-review.local.md` settings
3. Current working directory if it matches the PR's target repo
4. If the PR is from a GitHub URL and no local repo is available, use `gh pr diff <PR#> --repo <owner/repo>` to fetch the diff via GitHub API — this provides file-level changes without a full clone
5. If none of the above work, degrade gracefully and clearly disclose the limitation in the review output:
   - Skip git-truth validation (note: "Git-truth validation skipped — repo not available locally")
   - In Step 3, rely on PR doc file listings and the `gh pr diff` output if available — but clearly label all findings as "based on PR doc / GitHub API diff, not verified against full source code"
   - Never silently pretend you read actual source code when you didn't

1. Run `git diff dev..HEAD --name-only` to get the authoritative list of changed files
2. Cross-reference with the PR doc's file tree:
   - Flag **undocumented changes** (in diff, not in doc)
   - Flag **phantom files** (in doc, not in diff)
   - Flag **inaccurate descriptions** (file listed but change doesn't match)
3. Build **scope map** from commit messages:
   - Run `git log dev..HEAD --oneline`
   - Commits with `[TICKET-ID]` prefix → changed files are **IN_SCOPE**
   - Commits with different ticket prefix → changed files are **OUT_OF_SCOPE**
   - Commits with no prefix → **IN_SCOPE** (assumed)
4. Produce a verification table (see Section J format)
5. If OUT_OF_SCOPE files exist, note this for the scope section in the output

### Step 3: Read Actual Code (Deep)

The actual source code is the primary review source — the PR doc provides context only.

1. For each **IN_SCOPE** changed file:
   - Read the full file to understand context
   - Read the specific diff with `git diff dev..HEAD -- <filepath>`
   - Note architecture, patterns, and potential issues
2. For each **OUT_OF_SCOPE** changed file:
   - **Skim only**: read the diff, check for obvious bugs
   - Do NOT deep-review these files
3. Cross-compare sibling components:
   - If the PR adds/modifies a component, read its sibling components in the same directory
   - Check for consistency in prop interfaces, naming, patterns
4. Check barrel exports (e.g. `index.ts`) for proper re-export organization
5. Check import statements for FSD layer compliance

Prioritize: new files first, then modified files, then renamed/deleted files.

### Step 4: Independent Deep Code Review (PRIMARY SPINE)

This is the core of the review and runs **unconditionally** — regardless of whether GitHub Copilot or CodeRabbit produced comments or not. Load `references/review-criteria.md` and perform a thorough, adversarial review of every IN_SCOPE file.

**CRITICAL execution order**: Complete this entire step BEFORE reading any AI provider comments (Step 5). Do not read the `*.review-data.json` sidecar, CodeRabbit sections, or Copilot summaries until Step 4 is fully complete. This ensures findings are genuinely independent. If you read provider comments first, your "independent" findings will be contaminated by confirmation bias.

**Review Dimensions** (9 categories):

| Dimension           | Criteria Section | Focus                                            |
| ------------------- | ---------------- | ------------------------------------------------ |
| Bugs & Correctness  | —                | Runtime errors, logic bugs, null dereferences    |
| Architecture / FSD  | A                | Layer compliance, import direction, API location |
| React & TypeScript  | B                | useWatch, useEffect deps, type safety            |
| Sibling Consistency | I, K             | Parallel patterns across related components      |
| DRY / Duplication   | I                | Repeated logic, extractable utilities            |
| UI / Design System  | C                | Semantic tokens, layout patterns, hover states   |
| Error Handling      | D                | safeResponseJson, mutation error UX              |
| Accessibility       | F                | aria-labels, semantic HTML, keyboard             |
| Performance         | H                | useCallback, useMemo, N+1 patterns               |

**Adversarial Review Process** (go beyond checklist-walking):

1. **Per-file dimension walk**: For each IN_SCOPE file, check all 9 dimensions. Don't just skim — read the logic line by line.
2. **Try to break it mentally**: For each piece of logic, ask "what input or state would cause this to fail?" Check:
   - What happens with empty arrays, null, undefined, 0, empty strings?
   - What if the API returns an unexpected shape or error?
   - What if the user navigates away mid-operation?
   - What if this component renders before its data is loaded?
3. **Trace data flow end-to-end**: Follow props from parent → child, follow state from hook → render, follow API data from fetch → display. Flag any point where types narrow unsafely or data is assumed present.
4. **Check what's MISSING, not just what's wrong**: Missing error boundaries, missing loading states, missing barrel exports, missing type guards at boundaries, missing accessibility attributes.
5. **Cross-compare siblings**: Read sibling components in the same directory. Flag inconsistencies in prop interfaces, naming patterns, error handling approaches, or conditional rendering strategies.
6. **Validate feature claims (AC Validation)**: For each feature/change claimed in the PR doc (from Step 1's claim list), search the implementation for evidence and classify:
   - **VERIFIED**: Feature is fully implemented as described
   - **PARTIAL**: Feature exists but is incomplete or doesn't match the description
   - **NOT_VERIFIED**: No evidence found in the actual code
   - PARTIAL and NOT_VERIFIED are HIGH severity findings — feed into the verification table in Step 2's output.
7. **Audit test quality**: If the PR includes test files, verify they contain real assertions — not placeholder `expect(true).toBe(true)` or empty test bodies. Check that tests actually exercise the changed logic, not just import the module. Missing tests for new utility functions or complex logic = a finding.
8. **Classify findings** on both axes: Fix-Self or Pass-to-Creator (who fixes it) AND 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW (severity). See the Classification Framework below.
9. **Record evidence**: Every finding must include file:line references and either a code snippet or a concrete description of the issue. No vague "could be improved" statements.

**Severity count validation**: After classifying all findings, count the severity labels in each individual finding's detail block and verify they match the summary line (`총 X건: 🔴 HIGH A건 / 🟡 MEDIUM B건 / 🟢 LOW C건`). If a finding is labeled MEDIUM in the summary but LOW in its detail, fix the inconsistency before finalizing. The detail block's severity is the source of truth.

**This step should produce the bulk of the review findings**. If it produces fewer than 3 findings for a non-trivial PR, proceed to Step 6 for re-examination.

### Step 5: Triage AI Review Comments (Demoted)

This step is provider-aware and secondary to the independent code review.

1. Resolve the effective review source:
   - `--review-source all` → triage every available provider
   - `--review-source coderabbit` → only CodeRabbit
   - `--review-source copilot` → only GitHub Copilot
   - `--review-source none` or `--quick` → skip this step entirely
2. Load only the provider guide(s) needed:
   - `references/coderabbit-triage-guide.md`
   - `references/copilot-triage-guide.md`
3. Prefer structured sidecar data from `*.review-data.json` when available. Fall back to markdown parsing only if sidecar data is absent.
4. For each provider, focus on the **latest review round** unless the user explicitly asks for historical rounds:
   - CodeRabbit: latest `# Comment | by CodeRabbit bot | <timestamp>` section
   - GitHub Copilot: latest review summary plus comments whose `pull_request_review_id` belongs to that latest Copilot review
5. For each comment **individually**:
   - Read the actual code at the referenced file and line range
   - Determine if the issue **still exists** in current code
   - Apply **scope-aware triage**: if the comment targets an OUT_OF_SCOPE file, dismiss with "스코프 외" reason
   - Classify using the decision tree below

**Important**: Every comment must appear as an individual row in the triage tables (Fix-Self, Pass-to-Creator, or Dismissed). Do NOT bulk-dismiss comments without per-comment entries. The consolidated footer (for 5+ scope dismissals) is an _additional_ summary footnote — it does not replace individual rows in the Dismissed table.

```
Is this comment from the latest review round for its provider?
├── No → DISMISSED: "이전 리뷰 라운드 기준이라 현재 검토 대상 아님"
└── Yes
    ├── Is the issue still present in current code?
    │   ├── No → DISMISSED: "이후 커밋에서 이미 수정됨"
    │   └── Yes
    │       ├── Is the file OUT_OF_SCOPE?
    │       │   └── Yes → DISMISSED: "스코프 외 ([TICKET] 커밋 소속)"
    │       │       Exception: obvious bugs still flagged
    │       ├── Does this contradict a project convention in CLAUDE.md or provider instructions?
    │       │   └── Yes → DISMISSED: "프로젝트 컨벤션과 상충"
    │       └── Is the fix mechanical?
    │           ├── Yes → FIX-SELF + severity (HIGH/MEDIUM/LOW)
    │           └── No → Would the developer learn something?
    │               ├── Yes → PASS-TO-CREATOR + severity (HIGH/MEDIUM/LOW)
    │               └── No → FIX-SELF + severity (HIGH/MEDIUM/LOW)
```

**If a selected provider has 0 comments**:

- CodeRabbit → Follow the Zero CodeRabbit Comments Protocol in `references/coderabbit-triage-guide.md`
- GitHub Copilot → Follow the Zero Copilot Comments Protocol in `references/copilot-triage-guide.md`

State this clearly in the review and move on — the review's substance comes from Step 4.

### Step 6: Minimum Issue Check (NEW)

If the PR is non-trivial (3+ IN_SCOPE files with meaningful logic) and Steps 4-5 combined produced fewer than 3 HIGH+MEDIUM findings:

1. Load `references/review-criteria.md` Section K
2. Re-examine using the checklist: edge cases, sibling consistency, integration points, test coverage, missing error states
3. If new findings emerge, add them to the review
4. If re-examination finds nothing: state "코드 품질이 양호합니다" with confidence (don't invent fake issues)
5. For trivial PRs (< 3 files, simple logic): skip this step entirely

### Step 7: Check Developer History

1. Read `docs/reviews/developers/<github-id>.md` if it exists
2. Look for **recurring patterns** that match current findings
3. If a category has 3+ entries: adjust feedback tone — still kind, but more direct:
   - "이 패턴이 이전 PR들에서도 나타났습니다. 이번에 확실히 익혀봅시다."
4. Note recurring strengths for the praise section

### Step 8: Generate Review Document

Load `references/output-template.md` for the review structure and `references/feedback-templates.md` for Korean phrasing. Save to:

```
docs/reviews/[TICKET-ID]-review.md
```

When using `--quick` mode, add `-quick` suffix to avoid overwriting a full review: `docs/reviews/[TICKET-ID]-review-quick.md`.

Present a summary to Eddie in the conversation after saving.

### Step 9: Update Developer Profile

Create or update `docs/reviews/developers/<github-id>.md`:

1. Increment review count, update last review date
2. For each Pass-to-Creator finding: add a categorized entry with date, ticket, description, file:line
3. For notable Fix-Self findings (not pure formatting): add entry too
4. Update "주요 강점" and "주의 영역" summary based on accumulated data

### Step 10: Reviewer Fix-Forward (Conditional)

This step activates when the reviewer decides to fix issues directly instead of waiting for the PR creator. Common triggers include: "직접 수정", "내가 고칠게", "시간이 없어서 내가 수정", "fix it myself", "fix-forward".

1. Apply fixes to the codebase based on the review findings (both Fix-Self and Pass-to-Creator items)
   - **Fix-forward exclusions**: Never auto-modify files matching the patterns in `fix_forward_exclusions` from `.claude/pr-review.local.md` settings (defaults below). Instead, output "Manual fix recommended" with an explanation:
     - `**/migrations/**`, `**/*.sql` in migration directories (immutable after application in Supabase, Prisma, etc.)
     - `Dockerfile`, `docker-compose*.yml`
     - `.github/workflows/**` (CI/CD pipelines)
     - `*.lock` (lockfiles)
     - `.env*` (environment files)
   - For any fix touching files outside the immediate feature code, show the proposed change and ask for confirmation before applying
   - **Track every file you modify** in a list — you will need this for step 2b
2. Run `pnpm typecheck` to verify all fixes pass
   a. **Commit convention**: Before creating any commit, run `git log --oneline -10` in the target repo to detect the existing commit message convention (e.g., conventional commits, gitmoji, ticket prefixes). Match that convention exactly.
   b. **Specific git add only**: Only `git add` the specific files you modified during fix-forward. Never use `git add .`, `git add -A`, or any broad staging command. This prevents accidentally staging the user's unrelated changes.
   c. **No attribution metadata**: Never include `Co-Authored-By`, `Signed-off-by`, or any similar attribution trailer in generated commits.
3. Load `references/fix-forward-template.md` for the appendable section format
4. Append the fix log to the **existing** review document (`docs/reviews/[TICKET-ID]-review.md`)
5. Use `Round 1` for the first fix pass; increment to `Round 2`, `Round 3` etc. if new issues arise after pushing fixes (e.g., new GitHub Copilot or CodeRabbit comments)
6. The `{reviewer_github_id}'s Comment` section is **mandatory** — it serves as the copy-pasteable PR comment for the author. The `피드백` subsection within it is also mandatory to preserve educational value even when the reviewer fixes things directly
7. Present a summary to Eddie in the conversation after appending

### Step 11: Auto Review Pipeline (`--auto` mode only)

When invoked with `--auto <PR#>`, execute the managed pipeline below. Use the canonical scripts under `skills/pr-review/scripts/`.

#### Phase A: Fetch and Resolve

1. Run `scripts/fetch-pr.sh <PR#> --review-source <source> [--repo-path <abs-path>]` to fetch PR metadata, provider latest-round metadata, and the sibling `*.review-data.json` sidecar.
2. Resolve the target product repo from `--repo-path` or the current working directory. If neither resolves the correct repo, fail fast instead of guessing.
3. Resolve the review doc path using this precedence:
   - explicit `--review-doc <path>`
   - `docs/reviews/<TICKET>-review.md` derived from the PR head branch basename
   - otherwise fail fast
4. If the ticket id cannot be derived from the branch basename via exactly one `[A-Z][A-Z0-9]+-\d+` match, require `--review-doc`.
5. Run `scripts/prepare-pr-worktree.sh <review-data.json> [--repo-path <abs-path>] [--review-doc <path>] [--worktree auto|<abs-path>]`.
   - This step is mandatory. Do **not** improvise around it.
   - If the script returns `status: needs-repo-path`, stop immediately and tell Eddie to rerun with `--repo-path <abs-path>`.
   - If the target repo has **staged changes** (`git diff --cached` is non-empty) and no worktree override is supplied, stop safely and tell Eddie to rerun with `--worktree auto` or `--worktree <abs-path>`. Unstaged modifications (e.g. local `.gitignore` changes) are not considered dirty — they won't leak into commits as long as fix-forward only `git add`s specific files.
   - If `--worktree auto` is used, create or reuse the deterministic clean worktree for the current PR round.
   - If worktree mode is used and the review doc exists only in the source repo clone, the script mirrors that review doc into the prepared worktree at the same repo-relative path.
   - If the review doc does not exist yet, the script must still return the resolved canonical `review_doc_path` plus a Round 1 context so the first review document can be created during Phase B.
   - Record the worktree JSON output for the next phases and use the returned `review_doc_path` from that output for subsequent round updates.

#### Phase B: Full Review and Fix-Forward

1. Run **Steps 1-9** (Full Review mode) using the fetched PR doc, branch, and GitHub ID from the review data.
   - On a first-run auto review where the returned `review_doc_path` does not exist yet, create the initial review document at that exact returned path inside the prepared worktree or resolved repo before Phase C begins.
   - If `--review-doc <path>` points to a non-standard location inside the repo, honor that exact path for the first save instead of drifting back to the default `docs/reviews/[TICKET]-review.md`.
2. Proceed to **Step 10** (Fix-Forward) inside the prepared worktree when the review requires reviewer-applied changes.
3. Run `pnpm typecheck` (and any focused tests) inside the prepared worktree before continuing.

#### Phase C: Managed Round N Record

1. Run `scripts/update-review-round-doc.sh init <review-data.json> --repo-path <repo> [--review-doc <path>] [--review-source <source>] [--worktree-json <path>]`.
2. The script appends or resumes the current managed round in the existing review document and writes two canonical fenced JSON blocks:
   - `round_meta`
   - `round_decisions`
3. `round_meta` is the source of truth for:
   - PR number, ticket id, branch, head SHA
   - latest provider review ids
   - artifact directory
   - round status
   - worktree metadata
4. `round_decisions` is the canonical machine-readable source for verdicts and reasons. A new managed round starts with one `pending` row for every latest selected provider comment.
5. Update each `round_decisions` row to `accepted` or `declined` during triage. Do **not** rely on free-form prose for verdicts.

#### Phase D: Artifact Generation and Dry-Run Verification

1. Generate the normalized decisions artifact:
   ```bash
   scripts/generate-decisions-json.sh <review-doc> <review-data.json> --repo-path <repo>
   ```
2. Persist artifacts in the deterministic round directory:
   - `.pr-review/pr-<PR_NUMBER>/round-<N>/decisions.json`
   - optional reply/resolve preview outputs for the same round
3. Preview replies and thread resolution before any live mutation:
   ```bash
   scripts/post-ai-review-comments.sh <PR#> <decisions.json> --repo <owner/repo> --dry-run --output <reply-output.json>
   scripts/resolve-ai-review-threads.sh <PR#> <decisions.json> --repo <owner/repo> --dry-run --output <resolve-output.json>
   ```
4. After preview succeeds, update the round state:
   ```bash
   scripts/update-review-round-doc.sh status <review-doc> --round <N> --status dry-run-verified \
     --artifact decisions_json=<path> \
     --artifact reply_output=<path> \
     --artifact resolve_output=<path>
   ```
5. Stop here unless `--live` is present. `/pr-review --auto` without `--live` is a supervised artifact-and-preview flow, not autonomous mutation.

#### Phase E: Live Mutation (`--live` required)

1. Before any commit or reply/resolve step:
   - rerun the decisions generator as a mandatory live preflight:
     ```bash
     scripts/generate-decisions-json.sh <review-doc> <review-data.json> --repo-path <repo> --require-live-ready --output <decisions.json>
     ```
   - this preflight must fail before commit or push if any selected latest-round decision remains `pending`
   - re-fetch the PR branch and abort if the remote branch advanced or the push would be non-fast-forward
2. If fix-forward produced repo or review-doc changes, commit them in the prepared worktree and push with the recorded remote target.
3. Run the live mutation steps with the generated artifact:
   ```bash
   scripts/post-ai-review-comments.sh <PR#> <decisions.json> --repo <owner/repo> --output <reply-output.json>
   scripts/resolve-ai-review-threads.sh <PR#> <decisions.json> --repo <owner/repo> --output <resolve-output.json>
   ```
4. Update the round state explicitly:
   - `live-posted` on full success
   - `mutation-partial` if code changes committed/pushed but GitHub mutation was incomplete
   - `blocked` if the flow cannot continue safely
5. Only `mutation-partial -> live-posted` is resumable automatically. Any other rerun scenario requires explicit operator judgment.

#### Acceptance Procedure

1. Dry-run proof:
   - Run `/pr-review --auto <PR#> --review-source <source> [--repo-path ...] [--review-doc ...] [--worktree ...]`
   - Verify the review doc contains the new managed round and that the round artifact directory contains the generated decisions file plus preview outputs.
2. Live proof:
   - Update every `pending` row in `round_decisions`
   - Re-run the same command with `--live`
   - Confirm commit/push success, replies posted, threads resolved, and round status transitioned to `live-posted`

#### Error Handling

- If `fetch-pr.sh` fails (e.g. PR not found): abort with a clear error.
- If the repo path, repo identity, branch, or review-doc path cannot be resolved safely: abort before fix-forward.
- If `pnpm typecheck` fails after fixes: do **not** commit or push.
- If provider metadata drifts between round creation and decisions generation or live mutation: fail rather than replying to stale rounds.
- If reply/resolve succeeds only partially, persist `mutation-partial` or `blocked` instead of pretending the round finished cleanly.

---

## Classification Framework

Every finding is classified on **two orthogonal axes**:

### Axis 1: Who Fixes It?

The guiding principle: **"Would fixing this myself teach the developer nothing, or would explaining it teach them something valuable?"**

**Fix-Self** (reviewer fixes directly) — mechanical, no learning opportunity lost:

- Missing semicolons, extra blank lines, formatting issues
- Adding `aria-label` to icon-only buttons
- Conditional rendering guard (`{memo && <p>...</p>}`)
- Reformatting a cramped function signature onto multiple lines
- Removing dead constants (e.g. `IS_EDIT_MODE = false` that's never truly toggled)
- Fixing a one-line null check or fallback

**Pass-to-Creator** (developer should fix to learn) — the developer gains something:

- `useEffect` with incorrect dependency array — understanding React's reactivity model
- Modal close-before-mutation pattern — understanding async UX flow
- Ambient type declaration vs explicit module export — understanding TypeScript module system
- Silent fallback for unknown enum values — understanding defensive error handling strategy
- Pure utility function inline in a component file — understanding FSD code organization
- Type inconsistency across sibling components — understanding prop contract design

### Axis 2: Severity

| Severity  | Criteria                                                                                           | Merge Impact                                       |
| --------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| 🔴 HIGH   | Runtime crash, data loss, security vulnerability, broken feature, wrong behavior                   | **Blocks merge** — must fix before approval        |
| 🟡 MEDIUM | Missing error handling, incorrect types, FSD violation, silent failures, incomplete implementation | **Should fix** — strongly recommended before merge |
| 🟢 LOW    | Style improvement, minor accessibility gap, extractable utility, naming inconsistency              | **Nice to fix** — can merge with follow-up         |

### Combined Examples

| Finding                                     | Who             | Severity  | Why                                                 |
| ------------------------------------------- | --------------- | --------- | --------------------------------------------------- |
| Null dereference when API returns empty     | Fix-Self        | 🔴 HIGH   | Crash risk, mechanical one-line fix                 |
| `useEffect` missing `placeData` in deps     | Pass-to-Creator | 🔴 HIGH   | Stale data bug, developer needs to learn reactivity |
| `safeResponseJson` not used in catch block  | Fix-Self        | 🟡 MEDIUM | Silent failure on empty body, easy to fix           |
| Silent `?? 'bus'` fallback for unknown enum | Pass-to-Creator | 🟡 MEDIUM | Hides backend changes, teaches defensive strategy   |
| Missing `aria-label` on icon button         | Fix-Self        | 🟢 LOW    | Accessibility gap, mechanical addition              |
| Utility function could move to `lib/`       | Pass-to-Creator | 🟢 LOW    | FSD organization, learning opportunity              |

---

## Output Template

Load `references/output-template.md` for the exact review document structure. Follow it precisely — the template defines all section headings, table formats, and conditional rendering rules (e.g., omit AI triage section in quick mode).

---

## Korean Feedback Tone Guide

Two modes, mixed as appropriate:

**교육적 (Educational)** — for architecture, patterns, and "why" explanations:

- 선배 개발자가 후배에게 설명하는 느낌
- "이 패턴을 사용하면 ~ 때문에 향후 유지보수가 어려워질 수 있어요."
- "React에서 useEffect의 dependency array는 ~ 역할을 하는데..."
- Always explain the "why", not just the "what"

**간결 (Concise)** — for small, obvious fixes:

- "세미콜론 누락"
- "`aria-label` 추가 권장"
- "빈 태그 렌더링 방지 필요"

**Tone rules:**

- Always lead with something positive in the 잘한 점 section
- Never use harsh language ("잘못했다", "이해를 못한 것 같다")
- Frame mistakes as growth: "이 부분을 알게 되면 다음부터 훨씬 수월해질 거예요"
- If recurring issue (3+ times): be direct but still kind: "이 패턴이 계속 나오고 있어요. 이번에 확실히 정리해봅시다."

For detailed phrase templates, read `references/feedback-templates.md`.

---

## Developer Tracking

### File Location

```
docs/reviews/developers/<github-id>.md
```

### File Format

```markdown
# Developer Profile: @github-id

## 통계 (Statistics)

- 총 리뷰 횟수: N
- 마지막 리뷰: YYYY/MM/DD
- 주요 강점: [comma-separated areas]
- 주의 영역: [comma-separated areas]

## 리뷰 이력 (Review History)

### YYYY/MM/DD - [TICKET-ID] Title

**전체 평가**: [1-2 sentence summary]
**발견 건수**: Fix-Self N건, Pass-to-Creator N건, Dismissed N건

## 카테고리별 이력 (History by Category)

### Code Style & Formatting

- [YYYY/MM/DD] [TICKET] description (file:line) [Fix-Self/Pass-to-Creator]

### Type Safety & TypeScript

### React Patterns

### Accessibility

### Architecture / FSD Compliance

### Error Handling

### Performance

### DRY / Code Duplication
```

### Update Rules

- **New developer**: Create file from template, populate all sections
- **Existing developer**: Append to Review History and Category sections, update Statistics. Before appending, check if an entry for the same ticket+date already exists — if so, update it instead of creating a duplicate.
- **Category with 0 entries**: Keep the heading but leave empty (don't delete categories)
- **Strengths/Watch areas**: Re-derive from the full category history each time

---

## Reference Files

Load these on demand during the workflow:

| Reference                               | When to Load     | Purpose                                                                   |
| --------------------------------------- | ---------------- | ------------------------------------------------------------------------- |
| `references/review-criteria.md`         | Steps 2, 4, 6    | Git-truth validation (J), code review checklist (A-I), re-examination (K) |
| `references/output-template.md`         | Step 8           | Exact review document structure with all section headings and table formats |
| `references/feedback-templates.md`      | Step 8           | Korean phrase templates for writing feedback                              |
| `references/coderabbit-triage-guide.md` | Step 5           | How to parse, classify, and scope-triage CodeRabbit comments              |
| `references/copilot-triage-guide.md`    | Step 5           | How to parse, classify, and scope-triage GitHub Copilot comments          |
| `references/fix-forward-template.md`    | Step 10          | Appendable fix log template with 수정/미수정 tables and PR comment format |
| `scripts/fetch-pr.sh`                   | Step 11, Phase A | Fetches PR data from GitHub API and creates `*.review-data.json` sidecars |
| `scripts/prepare-pr-worktree.sh`        | Step 11, Phase A | Validates repo identity, handles dirty repos safely, and prepares deterministic worktrees |
| `scripts/update-review-round-doc.sh`    | Step 11, Phase C | Appends or resumes managed Round N sections and owns round status / artifact metadata |
| `scripts/generate-decisions-json.sh`    | Step 11, Phase D | Reads `round_meta` + `round_decisions` and emits the normalized decisions artifact |
| `scripts/post-ai-review-comments.sh`    | Step 11, Phases D-E | Previews or posts accept/decline replies to GitHub Copilot or CodeRabbit comments |
| `scripts/resolve-ai-review-threads.sh`  | Step 11, Phases D-E | Previews or resolves accepted GitHub Copilot or CodeRabbit threads via GraphQL |

These files contain detailed content that should not be loaded upfront. Read them only at the step indicated.

Also always reference:

- `CLAUDE.md` (already in context) — the authoritative source for project coding conventions
- `.coderabbit.yaml` — CodeRabbit configuration for understanding its review profile and path-specific rules
- `.github/copilot-instructions.md` and `.github/instructions/**/*.instructions.md` — GitHub Copilot review guidance and path-specific review instructions
