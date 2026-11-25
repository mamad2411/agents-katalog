---
name: post-completion
description: "Post-completion polish steps for Developer. Use when all PRD stories pass but before declaring COMPLETE. Triggers on: post-completion, polish, aesthetic review, post-change actions, final checks."
---

# Post-Completion Polish

> Load this skill when: All PRD stories pass but BEFORE declaring COMPLETE.

## Overview

After ALL stories pass, run these polish steps before marking the PRD complete.

---

## Step A: Full Aesthetic Review

If ANY stories modified UI files (`.tsx`, `.jsx`, `.css`, `.scss`):

1. **Gather all UI files changed across the feature:**
   - Get base branch from `docs/project.json` → `git.defaultBranch` (defaults to `main`)
   ```bash
   git diff <baseBranch>...HEAD --name-only | grep -E '\.(tsx|jsx|css|scss)$'
   ```

2. **Invoke @aesthetic-critic with the full list:**
   ```
   @aesthetic-critic: Full feature review before release.
   
   Changed UI files:
   [list all changed UI files]
   
   Mode: full (include Warnings)
   ```

3. **Read `docs/aesthetic-review.md`**

4. **Handle results:**
   - Critical issues → Fix them and re-commit before proceeding
   - Only Warnings → Note them in progress.txt but proceed

---

## Step B: Run Post-Change Actions

> **Support articles, AI tools, marketing pages, and other downstream propagation are now handled by `postChangeActions` in `project.json`.**
> These fire automatically after each story commit (see `test-flow` → Section 5.5).
> By the time post-completion runs, per-story postChangeActions have already executed.

At this point, check if any **PRD-level** post-change actions remain:

1. **Review `postChangeActions` with `trigger: "feature-change"`** — these may need a final holistic pass now that the full feature is implemented
2. **If any pending-update actions target a related project**, verify the update files were created during story commits
3. **If any agent actions were configured**, verify the agents completed successfully

If all post-change actions already ran per-story, no additional action needed here.

---

## Step C: Final Screenshot Check

1. **Read `docs/marketing/screenshot-registry.json`** (if exists)

2. **Get all files changed in the feature:**
   - Use base branch from `docs/project.json` → `git.defaultBranch`
   ```bash
   git diff <baseBranch>...HEAD --name-only
   ```

3. **Compare against `sourceComponents` in registry**

4. **If any screenshots need updating**, invoke @screenshot-maintainer:
   ```
   @screenshot-maintainer: Final screenshot check for feature.
   
   All changed files:
   [list of all changed files across feature]
   ```

5. **Also check if new support articles were created** that need screenshots

6. **Commit any screenshot updates:** `docs: update product screenshots`

---

## Step D: Verify Post-Change Action Results

Review all post-change actions that fired during the PRD:

1. **Check for any failed actions** — look for warnings in commit logs or session state
2. **If any pending-update files were created in related projects**, verify they exist:
   ```bash
   ls <related-project>/docs/pending-updates/*.md 2>/dev/null
   ```
3. **If any agent actions produced artifacts** (support articles, tool definitions, marketing pages), verify they are committed

If all actions succeeded, proceed to completion.

---

## Completion

After all polish steps complete, proceed to Phase 4 completion steps in the main developer flow.
