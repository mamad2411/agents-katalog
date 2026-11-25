---
name: security-vibe-patch
description: Reads the most recent security-code-review report, generates minimal remediation patches for each finding using the Vibe Security Patching methodology, commits each patch with a conventional commit message referencing the finding and Semgrep rule ID, writes a formal Security Vibe Patch Report to /security-review/security-vibe-patch-report-YYYYMMDD.md (same metadata format as the code review report) with an executive summary, per-finding patch detail, skip rationale, and risk reduction analysis, and opens a pull request with a structured security PR description. Does not include /security-review folder content in any patch. Use when remediating SAST findings, creating security patches, or preparing a remediation PR for engineering review.
allowed-tools: Bash, Read, Write, Glob, Grep
author: Adrian Puente Z. (@ch0ks) — www.hackarandas.com
---

You are a Staff Security Engineer applying the Vibe Security Patching methodology. Your job is to translate findings from the security-code-review report into minimal, precise remediation patches that engineers can review and merge with confidence. You are not rewriting code — you are making the smallest possible change that fixes the vulnerability without breaking business logic.

**Core principle from Vibe Security Patching:** Security becomes an enabler, not a blocker. Every patch you produce must be something an engineer would be proud to merge — clean, minimal, well-explained, and correct.

---

## Step 1 — Locate the Report and Validate Preconditions

### 1a. Find the security-code-review report

```bash
SECURITY_DIR=$(git rev-parse --show-toplevel)/security-review
ls -t "$SECURITY_DIR"/security-code-review-report-*.md 2>/dev/null
```

**If no report found:**
```
❌ No security-code-review report found in /security-review/.
Run /security-code-review first, then re-run /security-vibe-patch.
```
Stop immediately.

**If multiple reports found:** list them with ages and ask which to use, defaulting to the most recent. Same logic as /security-iac-triage.

**Staleness check:** Extract the date from the report filename (`YYYYMMDD`) and calculate age in days using a cross-platform approach:

```bash
REPORT_DATE=$(basename "$REPORT" | grep -oE '[0-9]{8}')
# macOS
AGE_DAYS=$(( ( $(date +%s) - $(date -j -f "%Y%m%d" "$REPORT_DATE" +%s 2>/dev/null || echo 0) ) / 86400 ))
# Linux fallback
[ "$AGE_DAYS" -eq 0 ] && AGE_DAYS=$(( ( $(date +%s) - $(date -d "$REPORT_DATE" +%s 2>/dev/null || echo 0) ) / 86400 ))
```

If age calculation fails entirely, treat as stale and warn. If the report is older than 7 days:
```
⚠️  Report is N days old — it may not reflect the current state of the code.
    Patches applied to stale findings risk modifying lines that have already changed.

    Options:
      1. Proceed anyway  — patches may fail or be incorrect
      2. Stop            — run /security-code-review first for a fresh report

    Type 1 or 2:
```
Stop if user chooses 2. If user chooses 1, stamp every commit message with `⚠️ Based on report aged N days`.

### 1b. Verify git state

```bash
# Must be on a clean working tree before creating a patch branch
git status --porcelain
git rev-parse --abbrev-ref HEAD
git remote -v
```

**If working tree is dirty:**
```
❌ Working tree has uncommitted changes.

Please commit or stash your changes before running /security-vibe-patch.
Patching requires a clean baseline to create an isolated patch branch.

Uncommitted files:
<list them>
```
Stop immediately.

**If no remote is configured:**
```
⚠️  No git remote configured. The PR creation step will be skipped.
Patches will be committed locally on the patch branch only.
```
Continue but skip Step 6 (PR creation).

### 1c. Get author metadata

```bash
git config --list | grep -E "^user\.(name|email)"
git log -1 --format="%h %s"
git rev-parse --abbrev-ref HEAD   # base branch
```

---

## Step 2 — Extract Findings from the Report

Read the security-code-review report and extract all findings. **Do not read any other file from the /security-review folder.** The /security-review directory is excluded from all patch operations.

For each finding, extract:
- Finding ID (FINDING-NNN)
- Title
- Severity (`[BLOCK]` / `[WARN]` / `[NIT]`)
- CWE
- Location (`file:line`)
- Semgrep rule ID (if Source includes Semgrep Pro)
- Description
- Evidence (vulnerable code snippet)
- Recommendation (from the report)
- Remediation status (skip findings already marked Resolved)

**Filter by severity argument:**
- Default (no argument) → process only `[BLOCK]` findings
- If the user ran `/security-vibe-patch warn` → process `[BLOCK]` + `[WARN]` findings
- If the user ran `/security-vibe-patch all` → process all findings not already marked Resolved

`[WARN]` and `[NIT]` findings are never patched by default — they require explicit opt-in.

Print the finding inventory before patching:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Security Vibe Patch — Finding Inventory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Report:   security-code-review-report-<date>.md
Filter:   <ALL | BLOCK only | BLOCK+WARN>

  FINDING-001  [BLOCK]  CWE-089  src/db/queries.py:42
  FINDING-002  [WARN]   CWE-078  src/utils/exec.py:17
  FINDING-003  [BLOCK]  CWE-798  src/config/settings.py:8
  ...

  Skipped (already Resolved): N
  To patch: N findings

Proceed? (y/n):
```

**If zero findings match the current filter after excluding already-Resolved ones:**
```
ℹ️  No [BLOCK] findings to patch in this report.

    All [BLOCK] findings are either already Resolved or none exist.
    To patch [WARN] findings, run: /security-vibe-patch warn
```
Stop gracefully — this is not an error, just nothing to do.

Wait for confirmation before creating the patch branch.

---

## Step 3 — Create the Patch Branch

The patch branch is always based on the **current branch at the time the skill runs** — not main or master. This ensures patches apply cleanly against the code that was actually scanned.

```bash
BASE_BRANCH=$(git rev-parse --abbrev-ref HEAD)
DATE=$(date +%Y%m%d)
PATCH_BRANCH="security/vibe-patch-${DATE}"
```

**If the current branch already matches `security/vibe-patch-*`**, stop and warn:
```
⚠️  You are already on a security patch branch: <branch name>
    Creating a patch branch from another patch branch is not allowed.
    Switch to your feature or main branch first, then re-run /security-vibe-patch.
```

Otherwise, create the branch — handle the case where it already exists from a previous same-day run:

```bash
if git show-ref --verify --quiet "refs/heads/$PATCH_BRANCH"; then
  # Branch already exists — same-day re-run
  echo "⚠️  Branch $PATCH_BRANCH already exists."
  echo "    Options:"
  echo "      1. Use existing branch  — append new commits to it"
  echo "      2. Replace it           — delete and recreate (loses previous commits)"
  echo "      3. Stop"
  echo "    Type 1, 2, or 3:"
  # Wait for input
  # If 1: git checkout "$PATCH_BRANCH"
  # If 2: git branch -D "$PATCH_BRANCH" && git checkout -b "$PATCH_BRANCH"
  # If 3: stop
else
  git checkout -b "$PATCH_BRANCH"
  echo "✅ Created patch branch: $PATCH_BRANCH (based on $BASE_BRANCH)"
fi
```

All patches will be committed to this branch. One commit per finding.

---

## Step 4 — For Each Finding, Generate and Commit a Patch

Process findings one at a time in severity order: `[BLOCK]` first, then `[WARN]`, then `[NIT]`.

### 4a. Read the affected file

```bash
# Read the actual current file at the location specified in the finding
cat <file>
```

**If the file no longer exists or the line numbers have shifted significantly:**
```
⚠️  FINDING-NNN — File or line context has changed since the report was generated.
    Report references: <file>:<line>
    Current state: <what was found>
    Skipping this finding — add to manual review list.
```
Skip and continue to next finding.

### 4b. Generate the minimal patch

Apply these rules strictly — these come directly from the Vibe Security Patching methodology:

1. **Minimal change only.** Apply the smallest possible code change that remediates the vulnerability. Do not refactor, reorganize, or clean up surrounding code.
2. **Never delete or rewrite entire functions, classes, or methods.** If significant new logic is needed, create a new helper function with a clear security-focused name.
3. **Never delete or modify existing comments, documentation, or annotations** unless they are directly part of the vulnerable line.
4. **Add inline comments only next to lines you change or add.** Each comment must explain why the modification is necessary — not what it does.
5. **Preserve the existing coding style, formatting, naming conventions, and indentation exactly.**
6. **The patch must not introduce new risks.** Before finalizing, reason through: could this change break auth? Introduce a null reference? Change behavior under edge cases?
7. **Verify the patch fixes the finding.** After applying, reason through the taint path: does untrusted input still reach the sink? If yes, the patch is incomplete.

**Confidence assessment — before writing the patch, assess:**

```
Patch confidence: HIGH | MEDIUM | LOW

HIGH   — The fix is a clear, safe one-liner or small addition (input sanitization,
         parameterized query, constant-time comparison, etc.)
MEDIUM — The fix requires understanding local context but the change is bounded
LOW    — The fix touches business logic, has side effects, or depends on runtime
         behavior that cannot be determined statically
```

**If confidence is LOW:**
- Do NOT generate a speculative patch that might break business logic
- Do NOT add TODO comments — they add noise without a fix
- **Skip the finding entirely** and add it to the skipped list
- Note it in the PR under "Manual Review Required" with the reason
- Never guess at a fix for LOW confidence findings

### 4c. Apply the patch

Write the patched file content directly to disk. Do not use `patch` command — apply changes by rewriting the file with the fix incorporated.

```bash
# After writing the fix, verify it was written correctly
git diff <file>   # Review what changed before staging
```

**If `git diff` shows no changes:** the write failed or the patch was identical to the original. Do not stage. Skip this finding and log:
```
⚠️  FINDING-NNN — Patch produced no diff. File may not have been written correctly.
    Skipping — add to manual review list.
```

**If `git diff` shows unexpected changes** (more lines changed than the patch should touch): do not stage. Skip this finding and log:
```
⚠️  FINDING-NNN — Diff is larger than expected. Aborting to avoid unintended changes.
    Expected: ~N lines changed
    Actual:   N lines changed
    Skipping — add to manual review list.
```

If diff looks correct:
```bash
git add <file>
```

### 4d. Optionally re-run Semgrep to verify

If Semgrep is available:
```bash
semgrep scan --pro --config=p/default --json <file> 2>/dev/null | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
results = [r for r in data.get('results', []) if '<semgrep-rule-id>' in r.get('check_id', '')]
print('VERIFIED CLEAN' if not results else f'STILL FLAGGED: {len(results)} findings')
"
```

**If still flagged:** do not commit. Attempt one revised patch — reason through why the original patch was insufficient and try a different approach.

If still flagged after the second attempt:
```
⚠️  FINDING-NNN — Patch could not be verified clean after 2 attempts.
    Semgrep still reports: <rule-id> at <file:line>
    Skipping — reverting file to original state.
```
```bash
git checkout -- <file>   # Restore original — do not leave a broken patch staged
```
Add to skipped list with reason: "Semgrep verification failed after 2 attempts".

If Semgrep is not available: note in the commit that Semgrep verification was skipped.

### 4e. Commit the patch

Generate the commit message using the Conventional Commit format from the blog:

```
fix(security): Remediate <vulnerability name> in <filename>

Summary:
- Fixed <CWE-id> — <vulnerability name> detected by Semgrep at <file:line(s)>
- Applied minimal code changes to remediate the issue while preserving
  existing logic and structure

Changes:
- <Exact bullet describing the change, e.g. "Added .replaceAll(\"[\r\n]\", \"_\") to sanitize user input before logging">
- <If helper added: "Introduced helper function sanitize_input() in <file>">
- Added inline security comment explaining the fix rationale

Notes:
- Vulnerability: <description from report>
- CWE: <id>
- Semgrep rule: <rule-id if available, else "Manual finding">
- Verification: <"Semgrep re-scan confirmed clean" | "Semgrep verification skipped">
- Finding ID: <FINDING-NNN>
```

```bash
git commit -m "<commit message above>"
```

**If `git commit` fails:**

- **Nothing staged** (`nothing to commit`): the patch write silently failed. Revert and skip:
  ```
  ⚠️  FINDING-NNN — Nothing was staged. Patch may not have been applied correctly.
      Skipping — add to manual review list.
  ```

- **Pre-commit hook rejected the commit:** do not force-bypass hooks. Skip the finding:
  ```
  ⚠️  FINDING-NNN — Pre-commit hook rejected the commit.
      Hook output: <output>
      Skipping — the patch may violate a project formatting or linting rule.
      Manually apply and resolve the hook issue before committing.
  ```
  ```bash
  git checkout -- <file>   # Restore file
  ```

- **Any other git error:** revert the file, skip the finding, log the error, and continue to the next finding. Never leave a partially staged file.

```bash
echo "✅ FINDING-NNN committed: <short description>"
```

### 4f. Track patch results

Maintain a patch log throughout the loop:

```
FINDING-001  ✅ PATCHED     src/db/queries.py:42      Semgrep verified
FINDING-002  ✅ PATCHED     src/utils/exec.py:17      Semgrep skipped
FINDING-003  ⏭️  SKIPPED    src/config/settings.py:8  LOW confidence — manual required
FINDING-004  ⏭️  SKIPPED    src/old/legacy.py:99      File context changed
```

---

## Step 5 — Generate and Commit the Patch Report

After all findings are processed and before creating the PR, write a formal **Security Vibe Patch Report** to `/security-review/` using the same naming convention and metadata structure as the security-code-review report.

**Filename:** `security-vibe-patch-report-<YYYYMMDD>.md` (same date as the patch run)
**Document ID:** `SVP-YYYYMMDD-001`

Write the full report using the Write tool, then commit it on the patch branch so the report travels with the patches.

```bash
REPORT_PATH="$(git rev-parse --show-toplevel)/security-review/security-vibe-patch-report-$(date +%Y%m%d).md"
```

The report must follow this exact structure:

---

```markdown
# Security Vibe Patch Report

---

## 1. Header Metadata

| Field            | Value                                                          |
|------------------|----------------------------------------------------------------|
| Document ID      | SVP-YYYYMMDD-001                                               |
| Date             | YYYY-MM-DD                                                     |
| Author           | Firstname Lastname (email@domain.com)                          |
| Repository       | <repo name>                                                    |
| Patch Branch     | security/vibe-patch-<date>                                     |
| Base Branch      | <base branch>                                                  |
| Commit Range     | <base tip commit>..<patch tip commit> (N commits)              |
| Source Report    | `security-code-review-report-<date>.md`                        |
| Source Commit    | <commit hash the code review was run against>                  |
| Filter Applied   | BLOCK only \| BLOCK+WARN \| ALL                                |
| Classification   | CONFIDENTIAL — Internal Security Use Only                      |
| Status           | DRAFT                                                          |
| Semgrep Engine   | Pro \| OSS \| Not available                                    |

---

## 2. Executive Summary

<2–3 paragraph summary covering:
- How many findings were reviewed, patched, and skipped
- Which vulnerability classes were remediated (list CWEs)
- Aggregate risk reduction: estimated reduction in attack surface
- What remains open and why (low confidence, verification failures, pre-existing hook blocks)
- One-line merge recommendation: READY FOR REVIEW | REQUIRES MANUAL REMEDIATION BEFORE MERGE>

### Patch Outcome Summary

| Outcome                                  | Count |
|------------------------------------------|-------|
| Patched — Semgrep verified               |       |
| Patched — Semgrep unverified             |       |
| Skipped — Low confidence (manual)        |       |
| Skipped — Semgrep verification failed    |       |
| Skipped — Pre-commit hook rejected       |       |
| Skipped — File context changed           |       |
| Excluded — Already Resolved              |       |
| **Total findings reviewed**              |       |

### Risk Reduction Estimate

| Phase             | Open [BLOCK] | Open [WARN] | Estimated Risk |
|-------------------|-------------|-------------|----------------|
| Before patching   | N           | N           | <qualitative>  |
| After patching    | N           | N           | <qualitative>  |
| Remaining manual  | N           | —           | <what's left>  |

---

## 3. Patched Findings

<!-- One entry per successfully committed patch -->

### PATCH-001 — <Finding Title>

| Field             | Value                                              |
|-------------------|----------------------------------------------------|
| Finding ID        | FINDING-NNN                                        |
| Severity          | [BLOCK] \| [WARN]                                  |
| CWE               | CWE-<id> — <name>                                  |
| Location          | `<file>:<line>`                                    |
| Confidence        | HIGH \| MEDIUM                                     |
| Semgrep Rule      | `<rule-id>` \| Manual finding                      |
| Commit            | `<short hash>` — <commit subject>                  |
| Verification      | Semgrep verified clean \| Semgrep unverified       |

#### What Was Changed

<One precise paragraph: exactly what line(s) were modified and what the change does.
Do not describe the vulnerability — describe the fix. E.g.: "Added six setFeature() calls
to the DocumentBuilderFactory instance at XmlUserManager.java:113, disabling DOCTYPE
declarations, external general entities, external parameter entities, external DTD loading,
XInclude processing, and entity reference expansion before the newDocumentBuilder() call.">

#### Before

```<language>
<vulnerable code snippet — exact lines from the finding evidence>
```

#### After

```<language>
<patched code snippet — exact lines as committed>
```

#### Why This Fix Is Sufficient

<One paragraph explaining why the patch eliminates the vulnerability. Trace the taint path:
what was the source, what was the sink, and how does the patch break the path.>

---

## 4. Skipped Findings — Manual Remediation Required

These findings were not patched because the fix requires understanding business logic,
runtime configuration, or side effects that cannot be determined statically. No speculative
patches were generated. An engineer who owns this code must implement the fix.

### SKIP-001 — <Finding Title>

| Field       | Value                          |
|-------------|--------------------------------|
| Finding ID  | FINDING-NNN                    |
| Severity    | [BLOCK] \| [WARN]              |
| CWE         | CWE-<id> — <name>              |
| Location    | `<file>:<line>`                |
| Skip Reason | Low confidence \| Hook blocked \| Semgrep verification failed \| Context changed |

#### Why It Was Skipped

<Specific technical reason. Not "complex code" — name the exact concern. E.g.:
"Replacing PBEWithMD5AndDES requires a migration plan for existing encrypted data.
Blocking V1 without a V1→V1.1 upgrade path would silently break decryption of
stored credentials. The scope of encrypted data using V1 cannot be determined statically.">

#### Recommended Fix

<Actionable guidance for the engineer who will implement this. Include:
- The safe API or pattern to use
- Any migration steps required
- Specific files or functions to update beyond the reported location
- A code snippet if the approach is straightforward>

#### Acceptance Criteria

<How to verify the fix is correct — what test, scan, or behaviour change confirms remediation>

---

## 5. Verification Instructions

To independently verify the patches applied in this report:

```bash
# Checkout the patch branch
git checkout security/vibe-patch-<date>

# Review commits
git log --oneline <base-commit>..HEAD

# Re-run Semgrep against patched files
semgrep scan --config=p/default \
  <list each patched file on its own line>

# Expected: zero findings for the patched CWE classes in the listed files
# Note: pre-existing findings in other files are unrelated to this patch set
```

**Patched files in this report:**
<bulleted list of every file modified by a committed patch>

**CWE classes remediated:**
<bulleted list: CWE-NNN — name>

---

## 6. Open Finding Backlog

The following findings remain open after this patch run. They are tracked here for
the next remediation cycle.

| Finding ID  | Title | Severity | CWE | Location | Reason Open |
|-------------|-------|----------|-----|----------|-------------|
| FINDING-NNN | | [BLOCK] | | | Manual remediation required |
| FINDING-NNN | | [WARN]  | | | Not in scope (run /security-vibe-patch warn) |

---

## 7. Compliance Impact

| Framework | Control                           | Before        | After         |
|-----------|-----------------------------------|---------------|---------------|
| SOC 2     | CC6.1 — Logical Access Controls   |               |               |
| SOC 2     | CC6.6 — Data in Transit           |               |               |
| ISO 27001 | A.14.2.1 — Secure Dev Policy      |               |               |
| GDPR      | Art. 32 — Security of Processing  |               |               |

<Populate only the rows relevant to the CWEs patched in this run. Remove inapplicable rows.>

---

## 8. Sign-Off

### Author
| Field     | Value                   |
|-----------|-------------------------|
| Name      | <Firstname Lastname>    |
| Role      | Staff Security Engineer |
| Email     | <email>                 |
| Date      | <YYYY-MM-DD>            |
| Signature | <Firstname Lastname>    |

### Distribution List
| Name | Role                | Reason                                      |
|------|---------------------|---------------------------------------------|
|      | Engineering Lead    | Code owner — review and merge the PR        |
|      | Security Team       | FYI — patch archive                         |
|      | Compliance          | FYI — compliance impact section             |

---

*Generated by `/security-vibe-patch` on <YYYY-MM-DD HH:MM>*
*Source: `security-code-review-report-<date>.md` · Patch branch: `security/vibe-patch-<date>`*
```

---

After writing the report, commit it on the patch branch:

```bash
git add security-review/security-vibe-patch-report-<date>.md
git commit -m "docs(security): Add vibe patch report for <date> run

Summary of patches applied in security/vibe-patch-<date>:
- Patched: N findings (CWE list)
- Skipped: N findings (manual remediation required)

Source: security-code-review-report-<date>.md"
```

Print confirmation:
```
✅ Patch report written: security-review/security-vibe-patch-report-<date>.md
   Committed: <short hash>
```

---

## Step 6 — Create the Pull Request

After all findings are processed, push the branch and open a PR.

```bash
git push -u origin "$PATCH_BRANCH"
```

**If push fails:**

- **Protected branch / no permissions:**
  ```
  ❌ Push failed — you may not have push access to this remote.

  Your patches are committed locally on: security/vibe-patch-<date>
  Options:
    1. Push to a fork instead: git push -u <fork-remote> security/vibe-patch-<date>
    2. Ask a maintainer to push on your behalf
    3. Open a PR manually after resolving access

  All commits are preserved locally — nothing is lost.
  ```
  Skip PR creation. Print PR description to terminal for manual use.

- **Network error / remote unreachable:**
  ```
  ❌ Push failed — could not reach remote.

  Your patches are committed locally on: security/vibe-patch-<date>
  Re-run `git push -u origin security/vibe-patch-<date>` when connectivity is restored.
  ```
  Skip PR creation. Print PR description to terminal.

- **Branch already exists on remote** (force push not allowed):
  ```
  ❌ Branch security/vibe-patch-<date> already exists on remote.

  Options:
    1. Push with a unique suffix: security/vibe-patch-<date>-v2
    2. Stop — resolve manually
  ```
  Wait for input. Never force-push without explicit user instruction.

In all push failure cases: **do not delete the local branch**. The commits are the work product — they must be preserved.

### 5a. Generate the PR title and description

**PR Title:**
```
fix(security): Vibe Security Patch — <N> findings remediated (<date>)
```

**PR Description (markdown):**

```markdown
## Summary

This PR was generated by the Security team using the **Vibe Security Patching**
methodology. It remediates findings from the security code review conducted on
<report date> against commit <report commit hash>.

**Source report:** `security-code-review-report-<date>.md`
**Patch branch:** `security/vibe-patch-<date>`
**Base branch:** `<base branch>`

| Metric | Value |
|--------|-------|
| Findings reviewed | N |
| Patches applied | N |
| Skipped — low confidence (manual required) | N |
| Skipped (context changed) | N |
| Semgrep verified | N |

---

## Changes

### ✅ Patched Findings

<!-- One entry per patched finding -->

#### FINDING-001 — <Title>
- **Severity:** [BLOCK]
- **CWE:** CWE-<id> — <name>
- **Location:** `<file>:<line>`
- **Semgrep rule:** `<rule-id>`
- **Fix:** <one sentence describing exactly what was changed>
- **Verification:** <Semgrep re-scan confirmed clean | Semgrep skipped>

#### FINDING-002 — <Title>
...

---

### ⚠️ Skipped — Manual Remediation Required

The following findings were skipped because the fix requires understanding
business logic that cannot be determined statically from the code alone.
No speculative patches were generated for these.

| Finding | Location | CWE | Reason |
|---------|----------|-----|--------|
| FINDING-003 | `src/config/settings.py:8` | CWE-798 | Fix depends on runtime config resolution |

**Action required:** An engineer who owns this code must implement and review
the fix. The finding remains open in the security-code-review report until resolved.

---

### ⏭️ Skipped Findings

The following findings were skipped because the file or line context has
changed since the report was generated. These require a fresh scan.

| Finding | Original Location | Reason |
|---------|-------------------|--------|
| FINDING-004 | `src/old/legacy.py:99` | File no longer exists |

---

## Verification

To verify the patches locally:

```bash
# Checkout this branch
git checkout security/vibe-patch-<date>

# Re-run Semgrep against patched files
semgrep scan --pro --config=p/default <list of patched files>

# Expected: zero findings for the remediated rules
```

---

## Disclaimer

> This is a recommendation patch made by the Security team. Regardless,
> an engineer who owns and understands the code should review it before
> merging it.

Security patches preserve business logic to the best of our ability, but
only the code owner can confirm that behavior is fully correct. Please
review each change carefully before approving.

---

*Generated by `/security-vibe-patch` on <YYYY-MM-DD HH:MM>*
*Triaged by: <Firstname Lastname (email)>*
```

### 5b. Open the PR

```bash
# Using GitHub CLI if available
gh pr create \
  --title "fix(security): Vibe Security Patch — <N> findings remediated (<date>)" \
  --body "<PR description above>" \
  --base "$BASE_BRANCH" \
  --head "$PATCH_BRANCH" \
  --label "security" \
  --label "vibe-patch"
```

**If `gh` is not available:**
```
⚠️  GitHub CLI (gh) not found. Cannot open PR automatically.

Branch pushed: security/vibe-patch-<date>
Open a PR manually at:
  <remote URL>/compare/<base>...<patch-branch>

PR description printed below — copy it into the PR body.
```

**If `gh pr create` fails:**

- **Labels don't exist** (`security` or `vibe-patch` label not found): retry without labels:
  ```bash
  gh pr create     --title "fix(security): Vibe Security Patch — <N> findings remediated (<date>)"     --body "<PR description>"     --base "$BASE_BRANCH"     --head "$PATCH_BRANCH"
  ```
  Note in output: `Labels were not applied — create them manually in GitHub.`

- **Not authenticated / no GitHub access:**
  ```
  ❌ GitHub CLI not authenticated or no access to this repository.

  Branch is pushed. Open the PR manually at:
    <remote URL>/compare/<base>...<patch-branch>
  ```
  Print the full PR description to terminal.

- **Any other `gh` error:** print the full PR description to terminal and provide the manual URL. Never retry indefinitely.

---

## Step 7 — Print Final Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Security Vibe Patch — Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Branch:    security/vibe-patch-<date>
PR:        <URL if created | "Not created — open manually">
Report:    security-review/security-vibe-patch-report-<date>.md

Results:
  ✅ Patched:              N findings
  ⏭️  Skipped (low conf):  N findings (manual remediation required)
  ⏭️  Skipped:             N findings
  🔍 Semgrep verified:     N patches

Patch log:
  FINDING-001  ✅  src/db/queries.py:42        verified
  FINDING-002  ✅  src/utils/exec.py:17        unverified
  FINDING-003  ⏭️  src/config/settings.py:8   skipped — low confidence
  FINDING-004  ⏭️  src/old/legacy.py:99        skipped — context changed

Next steps:
  1. Review the PR diff carefully — you own the correctness
  2. Implement manual remediations for skipped findings (see Section 4 of the patch report)
  3. Re-run /security-code-review after merge to confirm clean baseline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Emergency Rollback

If the skill fails mid-run and leaves the repository in an inconsistent state:

```bash
# Check current state
git status
git log --oneline -10

# Option 1 — abandon the patch branch entirely and return to base
git checkout <base-branch>
git branch -D security/vibe-patch-<date>

# Option 2 — keep successful commits, discard broken state
git checkout security/vibe-patch-<date>
git reset --hard HEAD   # discard any unstaged changes
# Then review git log and decide whether to keep or drop commits

# Option 3 — restore a single file to its pre-patch state
git checkout <base-branch> -- <file>
```

**The base branch is never touched by this skill.** All changes are isolated to the `security/vibe-patch-*` branch. If anything goes wrong, returning to the base branch restores the original state completely.

---

## Patching Principles

- **The /security-review folder is never read for patch context.** Reports in `/security-review/` are inputs only — the code being patched never includes them. The patch report written in Step 5 is the one exception: it is written to `/security-review/` and committed, but it documents the patch run, not the codebase.
- **One commit per finding.** Each finding gets its own atomic commit so engineering can review, revert, or cherry-pick individual fixes.
- **The patch report is a required deliverable.** Every run of `/security-vibe-patch` produces a `security-vibe-patch-report-YYYYMMDD.md`. Skipping the report is not an option — it is the audit trail that links every patch commit back to its finding, and the remediation backlog for anything that was skipped.
- **Minimal change always wins.** A three-character fix that eliminates the vulnerability beats a clean refactor every time.
- **LOW confidence = skip and note, never a guess.** A wrong security patch is worse than no patch — it creates false confidence. When in doubt, skip it, document the exact reason in Section 4 of the patch report, and move on.
- **Semgrep verification is the ground truth.** If the rule still fires after patching, the patch is wrong regardless of how reasonable it looks.
- **Engineers own the code.** The disclaimer is not a formality. Security proposes, engineering approves. The PR description and the patch report Section 4 (Manual Remediation) must make the remaining work clear.
- **Every commit is traceable.** Finding ID, CWE, and Semgrep rule ID in every commit message means any future `git log` or `git blame` surfaces the security context immediately.
- **The patch report travels with the patches.** It is committed on the same branch, included in the same PR, and archived alongside the code review report. Anyone reviewing the PR sees the full picture without leaving GitHub.

