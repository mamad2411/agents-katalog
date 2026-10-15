---
name: document-update
description: Post-ship documentation update. Reads all project docs, cross-references the diff, updates README, ARCHITECTURE, and other markdown files to match what shipped. Polishes CHANGELOG voice and cleans up TODOS. Use when asked to "update the docs", "sync documentation", or "post-ship docs".
---

# Document Update: Post-Ship Documentation Sync

You are running the `document-update` workflow. This runs when the user wants to ensure every documentation file in the project is accurate, up to date, and written in a friendly, user-forward voice. It is typically run after a feature is completed but before a PR is merged.

You are mostly automated. Make obvious factual updates directly. Stop and ask only for risky or subjective decisions.

**Only stop for:**
- Risky/questionable doc changes (narrative, philosophy, security, removals, large rewrites)
- New TODOS items to add
- Cross-doc contradictions that are narrative (not factual)

**Never stop for:**
- Factual corrections clearly supported by the diff
- Adding items to tables/lists
- Updating paths, counts, version numbers
- Fixing stale cross-references
- CHANGELOG voice polish (minor wording adjustments)
- Marking TODOS complete
- Cross-doc factual inconsistencies (e.g., version number mismatch)

**NEVER do:**
- Overwrite, replace, or regenerate CHANGELOG entries — polish wording only, preserve all content.
- Use `Write` tool on CHANGELOG.md — always use `Edit` or `Replace` with exact `old_string` matches.

---

## Step 1: Pre-flight & Diff Analysis

1. Gather context about what changed:
   ```bash
   # Find the base branch
   BASE_BRANCH=$(gh pr view --json baseRefName -q .baseRefName 2>/dev/null || gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || echo "main")
   
   git diff $BASE_BRANCH...HEAD --stat
   git log $BASE_BRANCH..HEAD --oneline
   git diff $BASE_BRANCH...HEAD --name-only
   ```

2. Discover all documentation files in the repo:
   ```bash
   find . -maxdepth 2 -name "*.md" -not -path "*/.git/*" -not -path "*/node_modules/*" | sort
   ```

3. Output a brief summary: "Analyzing N files changed across M commits. Found K documentation files to review."

---

## Step 2: Per-File Documentation Audit

Read each documentation file and cross-reference it against the diff. Use these heuristics:

**README.md:**
- Does it describe all features and capabilities visible in the diff?
- Are install/setup instructions consistent with the changes?
- Are examples, demos, and usage descriptions still valid?

**ARCHITECTURE.md:**
- Do component descriptions match the current code?
- Be conservative — only update things clearly contradicted by the diff. Architecture docs describe things unlikely to change frequently.

**CONTRIBUTING.md — New contributor smoke test:**
- Walk through the setup instructions as if you are a brand new contributor.
- Are the listed commands accurate? Would each step succeed?
- Flag anything that would fail or confuse a first-time contributor.

**Any other .md files:**
- Read the file, determine its purpose and audience.
- Cross-reference against the diff to check if it contradicts anything the file says.

For each file, classify needed updates as:
- **Auto-update** — Factual corrections clearly warranted by the diff.
- **Ask user** — Narrative changes, security model changes, large rewrites, ambiguous relevance.

---

## Step 3: Apply Auto-Updates

Make all clear, factual updates directly using your file editing tools.
For each file modified, output a one-line summary describing **what specifically changed** (e.g., "README.md: added new feature X to capabilities list").

---

## Step 4: Ask About Risky/Questionable Changes

For each risky or questionable update identified in Step 2, use the `ask_user` tool (or standard prompt) to present options to the user with your recommendation. Apply approved changes immediately after the answer.

---

## Step 5: CHANGELOG Voice Polish

**CRITICAL — NEVER CLOBBER CHANGELOG ENTRIES.**

1. Read the entire CHANGELOG.md first. Understand what is already there.
2. Only modify wording within existing entries. Never delete, reorder, or replace entries.
3. If CHANGELOG was modified in this branch, review the entry for voice:
   - Lead with what the user can now **do** — not implementation details.
   - "You can now..." not "Refactored the..."
   - Flag and rewrite any entry that reads like a commit message.
   - Auto-fix minor voice adjustments. Use `ask_user` if a rewrite would alter meaning.

---

## Step 6: Cross-Doc Consistency & Discoverability Check

1. Does the README's feature list match what other docs describe?
2. Does ARCHITECTURE's component list match CONTRIBUTING's project structure description?
3. **Discoverability:** Is every documentation file reachable from README.md? Every doc should be discoverable from the main entry point.
4. Auto-fix clear factual inconsistencies (e.g., a version mismatch). Use `ask_user` for narrative contradictions.

---

## Step 7: TODOS Cleanup

1. **Completed items not yet marked:** Cross-reference the diff against open TODO items. Move clearly completed items to a "Completed" section.
2. **Items needing updates:** If a TODO references significantly changed files, ask the user to confirm whether it should be updated, completed, or left as-is.
3. **New deferred work:** Check the diff for `TODO`, `FIXME`, and `HACK` comments. Use `ask_user` to ask whether they should be captured in a centralized TODOS.md file.

---

## Step 8: Commit & Output

1. **Empty check:** Run `git status`. If no documentation files were modified by any previous step, output "All documentation is up to date." and exit.
2. **Commit:** Stage modified documentation files by name and create a single commit:
   ```bash
   git commit -m "docs: sync documentation for recent changes"
   ```
3. **Push:** Push to the current branch (`git push`).

**PR body update:**
1. Read the existing PR body into a tempfile:
   ```bash
   gh pr view --json body -q .body > /tmp/pr-body-$$.md
   ```
2. Update or append a `## Documentation` section with a doc diff preview detailing what was changed.
3. Write the updated body back:
   ```bash
   gh pr edit --body-file /tmp/pr-body-$$.md
   ```
4. Output a scannable structured summary showing every documentation file's status:
   ```
   Documentation health:
     README.md       [Updated] (added feature X)
     CHANGELOG.md    [Voice polished] (adjusted wording)
     ARCHITECTURE.md [Current] (no changes needed)
     ...
   ```
