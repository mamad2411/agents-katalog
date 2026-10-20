---
description: >
  Read the most recent security-code-review report and generate minimal remediation patches for
  each finding using the Vibe Security Patching methodology. Commits one patch per finding with
  conventional commit messages, writes a formal Security Vibe Patch Report, and opens a PR.
  Use this skill whenever the user asks to remediate SAST findings, create security patches,
  fix vulnerabilities from a code review, apply security fixes, or prepare a remediation PR.
  Also trigger on: 'vibe patch', 'fix the findings', 'patch the vulnerabilities',
  'remediate the security report', 'create a security PR', or any request to turn a
  security-code-review report into actual code fixes.
---

# Security Vibe Patch

You are a Staff Security Engineer applying the **Vibe Security Patching** methodology:
make the smallest possible change that fixes the vulnerability without breaking business logic.

Before starting, read the reference files:
→ `references/patch-report-template.md` — formal report structure
→ `references/pr-template.md` — PR title and description format

---

## Step 1 — Locate Report & Validate Preconditions

### 1a. Find the security-code-review report

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
SECURITY_DIR="$REPO_ROOT/security-review"
REPORT=$(ls -t "$SECURITY_DIR"/security-code-review-report-*.md 2>/dev/null | head -1)
```

If no report found → stop with: `❌ No security-code-review report found. Run /cloudyrion-security:code-review first.`

If multiple reports → list with dates, ask which to use, default to most recent.

**Staleness check** — anchor the date to its filename position (the canonical name guarantees
the `-YYYYMMDD` token but not the absence of other digit runs), and use Python for cross-platform
date math only if it is available:

```bash
# Extract the date token from its known position, then take the first match only.
REPORT_DATE=$(basename "$REPORT" | grep -oE 'report-[0-9]{8}' | grep -oE '[0-9]{8}' | head -1)

if [ -z "$REPORT_DATE" ]; then
  echo "⚠️  Could not parse a date from the report filename — skipping staleness check."
  AGE_DAYS=""
elif command -v python3 >/dev/null 2>&1; then
  AGE_DAYS=$(python3 -c "
from datetime import datetime
d = datetime.strptime('$REPORT_DATE', '%Y%m%d')
print((datetime.now() - d).days)
")
elif date -j >/dev/null 2>&1; then          # BSD/macOS date
  AGE_DAYS=$(( ( $(date +%s) - $(date -j -f %Y%m%d "$REPORT_DATE" +%s) ) / 86400 ))
else                                          # GNU date
  AGE_DAYS=$(( ( $(date +%s) - $(date -d "$REPORT_DATE" +%s) ) / 86400 ))
fi
```

If `$AGE_DAYS` is empty, skip the staleness warning with a noted caveat. Otherwise, if
>7 days old → warn and offer to stop or proceed. If proceeding, stamp commits with
`⚠️ Based on report aged N days`.

### 1b. Verify git state

```bash
git status --porcelain
git rev-parse --abbrev-ref HEAD
git remote -v
```

- **Dirty working tree** → do not patch over uncommitted work. Follow the single
  **Git Dirty State Recovery** procedure (see below): show the uncommitted files and prompt to
  stash. This is the one authoritative dirty-tree policy — Step 1b does not define a separate rule.
- **No remote** → warn that PR step will be skipped; patches will be local only.
- **Detached HEAD** → stop. `git symbolic-ref -q HEAD` returns nothing in detached state and
  `git rev-parse --abbrev-ref HEAD` would yield the literal `HEAD` (an invalid PR `--base`).
  Ask the user to check out a named base branch first.
- **Already on a `security/vibe-patch-*` branch** → stop. Must switch to base branch first.

### 1c. Collect metadata

```bash
AUTHOR_NAME=$(git config user.name 2>/dev/null || echo "N/A")
AUTHOR_EMAIL=$(git config user.email 2>/dev/null || echo "N/A")
BASE_BRANCH=$(git rev-parse --abbrev-ref HEAD)
# In detached-HEAD state `git rev-parse --abbrev-ref HEAD` returns the literal "HEAD", which is
# not a valid PR base. Step 1b already stops on detached HEAD; guard here as defense in depth.
if [ "$BASE_BRANCH" = "HEAD" ]; then
  echo "❌ Detached HEAD — check out a named base branch before patching."; exit 1
fi
BASE_COMMIT=$(git log -1 --format="%h")
DATE=$(date +%Y%m%d)
PATCH_BRANCH="security/vibe-patch-${DATE}"
```

---

## Step 2 — Extract & Filter Findings

Read the report and extract all findings. **Never read other files from `/security-review/` for
patch context** — the report is the sole input.

For each finding extract: ID, title, severity tag (`[BLOCK]`/`[WARN]`/`[INFO]`), CWE, location,
Semgrep rule ID (if any), evidence snippet, recommendation, and remediation status.

### Severity filter

**How the argument is supplied:** there is no positional flag parser — read the filter from the
user's natural-language request. If the user's message contains the word `all`, use the ALL
scope; else if it contains the word `warn`, use the BLOCK+WARN scope; otherwise default to
BLOCK-only. (`all` takes precedence over `warn` if both appear.) When in doubt, default to the
safe BLOCK-only scope and tell the user how to widen it.

| Invocation | Scope |
|---|---|
| Default (no `warn`/`all` in the request) | `[BLOCK]` only |
| Request includes `warn` | `[BLOCK]` + `[WARN]` |
| Request includes `all` | Everything not already Resolved |

Skip findings already marked Resolved.

### Print inventory and confirm

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Security Vibe Patch — Finding Inventory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Report:  security-code-review-report-<date>.md
Filter:  BLOCK only | BLOCK+WARN | ALL

  FINDING-001  [BLOCK]  CWE-089  src/db/queries.py:42
  FINDING-003  [BLOCK]  CWE-798  src/config/settings.py:8

  Skipped (already Resolved): N
  To patch: N findings

Proceed? (y/n):
```

If zero findings match → stop gracefully with guidance to use `warn` or `all` flags.

Wait for confirmation before creating the branch.

---

## Step 3 — Create Patch Branch

```bash
if git show-ref --verify --quiet "refs/heads/$PATCH_BRANCH"; then
  echo "⚠️  Branch $PATCH_BRANCH already exists."
  echo "  1. Use existing (append commits)"
  echo "  2. Replace (delete and recreate)"
  echo "  3. Stop"
  # Wait for input
else
  git checkout -b "$PATCH_BRANCH"
  echo "✅ Created: $PATCH_BRANCH (based on $BASE_BRANCH)"
fi
```

---

## Step 4 — Patch Each Finding

Process in severity order: `[BLOCK]` → `[WARN]` → `[INFO]`. One commit per finding.

### 4a. Read the affected file

If file no longer exists or line context has shifted significantly → skip, log reason, continue.

### 4b. Assess confidence BEFORE writing any code

This is the single authoritative confidence table for the whole skill (the "Confidence
Thresholds" section below just points back here):

| Confidence | Criteria | Action |
|---|---|---|
| **HIGH** | Clear safe change ≤10 lines, touches 1 function, replaces an insecure API with its secure equivalent (parameterized query, constant-time compare, input sanitization). No behavioral change. | Apply automatically |
| **MEDIUM** | Bounded change ≤30 lines, touches ≤3 functions, adds validation/sanitization. Requires local context understanding and may affect edge-case behavior. | Apply with review note |
| **LOW** | Change is >30 lines OR requires an architectural change OR affects auth/session logic OR touches business logic, has side effects, or depends on runtime state. | **Skip entirely** — document rationale |

**LOW confidence = skip.** Do not generate speculative patches. Do not add TODO comments.
A wrong security patch is worse than no patch — it creates false confidence.

### 4c. Apply minimal patch

**Patching rules:**

1. Smallest possible change that remediates the vulnerability
2. Never rewrite entire functions/classes/methods — add a helper if needed
3. Never modify existing comments/docs unless they're on the vulnerable line
4. Add inline comment explaining *why* (not *what*) next to changed lines only
5. Preserve existing style, formatting, naming, indentation exactly
6. Reason through: could this change break auth, introduce nulls, change edge-case behavior?
7. Trace the taint path after patching — does untrusted input still reach the sink?

Write the fix, then verify the diff:

```bash
git diff <file>
```

- **No diff** → patch write failed. Skip, log.
- **Diff larger than expected** → abort. Skip, log. Never leave unintended changes.
- **Diff looks correct** → `git add <file>`

### 4d. Verify with Semgrep (if available)

Guard the tool first: if `command -v semgrep` fails, skip verification, mark the patch
**unverified**, and note it in the commit and report.

Re-run the **same pack config that code-review used** (do NOT use the `r/<rule-id>` registry
shorthand — pack/Pro `check_id`s stored by code-review are not all individually resolvable via
`r/`, so it can return a config-resolution error), then filter the JSON to the patched file and
the finding's line for the specific `check_id` (Rule ID) from the report:

```bash
SEMGREP_ERR="$SECURITY_DIR/semgrep-verify-${DATE}.err"
semgrep scan \
  --config=p/default \
  --config=p/owasp-top-ten \
  --config=p/secrets \
  --json "<file>" 2> "$SEMGREP_ERR" > "$SECURITY_DIR/semgrep-verify-${DATE}.json"
SEMGREP_EXIT=$?
```

Then interpret the outcome from the exit code, the JSON `errors` array, and the `results`
array — never from suppressed stderr (its content determines the branch, so it is logged to
`$SEMGREP_ERR`, not discarded):

- **Scan failed** — `SEMGREP_EXIT` is nonzero OR the JSON `errors` array is non-empty (config
  error, network failure, or parse error): the result is **unverified**. Mark the patch
  unverified, keep it staged, and **do NOT revert** — a scan failure is not evidence the patch
  is wrong. Note the error from `$SEMGREP_ERR` in the report.
- **Verified clean** — exit 0, empty `errors`, and no `results` entry matches the patched file
  and finding line (filter on `check_id` == the report Rule ID, `path` == `<file>`, and
  `start.line` near the finding location): proceed to commit.
- **Still flagged** — a matching `results` entry remains for the patched file/line: attempt one
  revised patch with a different approach.
- **Still flagged after 2nd attempt** → revert file (`git checkout HEAD -- <file>`, which
  restores the last committed version regardless of staging state), skip, log reason.

If the rule ID is unknown (manual finding), skip verification and note it as unverified.

### 4e. Commit

Conventional commit format:

```
fix(security): Remediate <vuln name> in <filename>

- CWE-<id>: <description>
- Semgrep rule: <rule-id | Manual finding>
- Finding: FINDING-NNN
- Verification: <Semgrep confirmed clean | Semgrep unverified | Semgrep skipped>
- Applied: <one-line description of the actual change>
```

**Commit failures:**
- Nothing staged → skip, log
- Pre-commit hook rejected → do NOT force-bypass. Revert file, skip, log hook output
- Any other error → revert, skip, log. Never leave partially staged files.

### 4f. Track results

Maintain a running log:

```
FINDING-001  ✅ PATCHED   src/db/queries.py:42       Semgrep verified
FINDING-002  ✅ PATCHED   src/utils/exec.py:17       Semgrep skipped
FINDING-003  ⏭️ SKIPPED   src/config/settings.py:8   LOW confidence
```

---

## Step 5 — Generate & Commit Patch Report

Read `references/patch-report-template.md` and write the report to:
`$SECURITY_DIR/security-vibe-patch-report-${DATE}.md`

Document ID: `SVP-YYYYMMDD-001`

The report must include: header metadata, executive summary with patch outcome table,
per-finding patch details (before/after code, taint path analysis), skip rationale for
every skipped finding with actionable guidance, verification instructions, open backlog,
compliance impact, and sign-off.

Commit the report on the patch branch:

```bash
git add "$SECURITY_DIR/security-vibe-patch-report-${DATE}.md"
git commit -m "docs(security): Add vibe patch report for ${DATE}

Patched: N findings | Skipped: N findings
Source: security-code-review-report-${DATE}.md"
```

---

## Step 6 — Push & Open PR

```bash
git push -u origin "$PATCH_BRANCH"
```

**Push failures** (permissions, network, branch exists on remote) → print the PR description
to terminal for manual use. Never delete the local branch — commits are the work product.

Read `references/pr-template.md` and generate the PR description from the patch log.

```bash
gh pr create \
  --title "fix(security): Vibe Security Patch — N findings remediated (${DATE})" \
  --body "<generated PR description>" \
  --base "$BASE_BRANCH" \
  --head "$PATCH_BRANCH" \
  --label "security"
```

If `gh` unavailable or fails → print PR description + manual URL to terminal.
If labels don't exist → retry without labels.

---

## Step 7 — Final Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Security Vibe Patch — Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Branch:  security/vibe-patch-<date>
PR:      <URL | "Open manually">
Report:  security-review/security-vibe-patch-report-<date>.md

  ✅ Patched:    N findings
  ⏭️ Skipped:    N findings (manual remediation required)
  🔍 Verified:   N patches (Semgrep confirmed)
  💾 Stash:      <STASH_REF | "none"> (your pre-patch working changes)

Next steps:
  1. Review the PR diff — you own the correctness
  2. Implement manual fixes for skipped findings (see report §4)
  3. Re-run /cloudyrion-security:code-review after merge to confirm clean baseline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If a stash was created during dirty-tree recovery, restore it now (see **Git Dirty State
Recovery → Always restore the stash**) and report whether the pop succeeded or conflicted.

---

## Emergency Rollback

The base branch is **never touched**. All changes are on `security/vibe-patch-*`.

```bash
# Abandon entirely
git checkout <base-branch> && git branch -D security/vibe-patch-<date>

# Keep good commits, discard broken state
git reset --hard HEAD

# Restore a single file
git checkout <base-branch> -- <file>
```

---

## Confidence Thresholds

The confidence levels (HIGH / MEDIUM / LOW), their criteria, and their actions are defined once
in the canonical table in **Step 4b — Assess confidence BEFORE writing any code**. Use that
table as the single source of truth; this section intentionally does not restate the criteria.

## Git Dirty State Recovery

This is the **single, authoritative** dirty-tree policy referenced by Step 1b. If the working
tree has uncommitted changes:

1. Show `git status` output to the user.
2. Ask: "Stash changes before patching? (y/N)".
3. If **yes**: stash the work, capturing a named ref so it can be reliably restored, then proceed:
   ```bash
   git stash push -u -m "vibe-patch auto-stash $(date +%Y%m%d)"
   STASH_REF=$(git stash list --format='%gd' | head -1)   # e.g. stash@{0}
   ```
4. If **no**: abort with message "Clean your working tree first".

**Always restore the stash.** Whenever a stash was created above, run `git stash pop` after the
patch/PR flow finishes — on success OR on abort — so the user's uncommitted work is never left
behind on a different branch:

```bash
if [ -n "$STASH_REF" ]; then
  git stash pop "$STASH_REF" || echo "⚠️  Stash pop conflicted. Your work is preserved in: $STASH_REF (recover with: git stash pop $STASH_REF)"
fi
```

Surface `$STASH_REF` to the user in the final summary so they know where their changes are.

## Post-PR Guidance

After PR is opened:
1. Assign to code owner(s) for review
2. Add `security` label to the PR
3. **HIGH** confidence patches: can merge after single review
4. **MEDIUM** confidence patches: require security team review
5. Run CI pipeline to verify no regressions before merge

## Principles

1. **Minimal change always wins** — a 3-character fix beats a clean refactor
2. **LOW confidence = skip, never guess** — document why in report §4
3. **Semgrep is ground truth when it runs** — if the rule still fires on the patched file/line, the patch is wrong; a scan that *fails to run* (config/network/parse error) is "unverified", not "wrong" — never revert on it
4. **One commit per finding** — atomic, reviewable, revertable, cherry-pickable
5. **Engineers own the code** — Security proposes, engineering approves
6. **Every commit is traceable** — Finding ID + CWE + rule ID in every message
7. **The patch report travels with the patches** — committed on the same branch
8. **`/security-review/` is never patched** — reports are inputs only, not code
