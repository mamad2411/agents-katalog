---
name: pr-drafter
description: >-
  Use this skill when the user wants a GitHub pull request body that follows
  the repository PR template, or a concise summary of branch changes for
  reviewers. Apply for informal asks like "write the PR" or "summarize this
  branch" even when they do not mention templates or GitHub explicitly.
---

# PR Drafter

Build PR description Markdown from **whatever PR template the repo actually uses** (headings, checklists, HTML comment instructions), then **write it to `.private/pr-drafts/`**, not only in chat. Follow the **workflow**, apply **Rules for the PR body**, skim **Common mistakes**.

## Workflow

### 1. Load `but` skill

GitButler’s CLI and its agent skill are both named **`but`**; resolve the skill by that name.

**MANDATORY**: When available, load and follow the **`but`** skill. If it is missing or you need syntax, use **`but --help`** and **`but <subcommand> --help`**.

```bash
but --help
```

Use **`but`** for workspace state and diffs. **Do not** mutate with `git`; use read-only `git` only to reconcile diff scope with the user’s intent when **`but`** is not enough.

### 2. Confirm PR head

Ask which **PR head** branch to draft against; do not guess. Cross-check with `but status -f` (branches, stacks). If it disagrees with the user, **prefer the user**.

### 3. Resolve template

Resolve explicitly (no fixed layout): **default** `.github/pull_request_template.md`; **else** `.github/PULL_REQUEST_TEMPLATE/*.md`, `docs/`, or a user path; **if none**, ask for path or expected sections. Read end-to-end. **HTML comments** are instructions; if they conflict with generic rules below, **the project wins**.

### 4. Gather facts

Collect commits and diffs for the PR head branch.

```bash
but branch show --files <branch-id>  # commits and changed files
but diff --no-tui <branch-id>        # full diff
```

### 5. Write the PR body

Using the template from step 3 and the facts from step 4, fill every placeholder. Map scope and type from file paths and commit messages. Apply **Rules for the PR body**. Only tick checklist items you actually verified.

Save to **`.private/pr-drafts/YYYY-MM-DD-HHMM-<stem>.md`** (mkdir if needed). `<stem>` = PR head slug (`/` → `-`). Collisions: append `-2`, `-3`, … before `.md`.

Tell the user the saved path and output a paste-ready PR body.

## Rules for the PR body

- **Heading fidelity**: Keep the template’s **`##` / `###` titles and their order** exactly as written. Do not translate, rename, or add sections the template does not define.
- **Checklists**: If the template includes `- [ ]` lines, **keep every row** unless the template explicitly tells you to drop rows or sections. Leave items **unchecked** when you did not run or verify them; do not tick boxes to “look done.”
- **Placeholders**: Replace issue/PR placeholders such as incomplete `Closes #` or empty `Fixes #` with a real reference when the user confirms one; otherwise **remove the broken line** so GitHub keywords stay valid.
- **Optional sections**: Some templates say to **delete whole sections** when not applicable, such as screenshots. Others want the heading left with “N/A.” **Follow the template comments**, not a global rule.
- **Deliverable cleanliness**: Strip HTML comments from the **pasted PR body** when they are only agent notes and would clutter the review; keep the structure those comments required.

## Common mistakes

<!-- prettier-ignore -->
| Mistake | Why it hurts |
|:---|:---|
| Inventing headings or reordering the template | Breaks team conventions and review bots. |
| Removing checklist lines to shorten the PR | Violates explicit template rules; reviewers lose signal. |
| Checking verification boxes without evidence | Misleading for CI/review; only check what you or the user confirmed. |
| Copying a summary from another repo's template shape | Wrong sections, wrong language, or missing required blocks. |
| Asserting a base (“vs `main`”, etc.) in the body that doesn’t match the PR’s actual diff scope | Reviewers see GitHub’s diff; the narrative drifts from what they review. |
| Leaving `Closes #` or similar with no number | Invalid or confusing GitHub linking. |
