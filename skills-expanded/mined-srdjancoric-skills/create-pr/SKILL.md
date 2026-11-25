---
name: create-pr
description: Prepare a pull request for the current branch in this repository's house format. By default the repository is read-only: the body is written to /tmp/pr-body.md and the commands are reported for the user to run. With --auto, stage, commit, push, and open the PR, then stop. Never merges.
---

# Create Pull Request

Inspect the current branch, write the pull request title and body, and report the remaining commands
in chat.

By default the user owns every action that leaves their machine. With `--auto`, this skill performs
those actions itself and stops once the PR is open.

## Boundaries

Without `--auto`, treat the repository as read-only. Never run `git add`, `git commit`, `git push`,
`git switch`, `gh pr create`, `gh pr edit`, or `gh pr merge`. Emit those as commands for the user
instead.

With `--auto`, staging, committing, pushing, and opening the PR are authorized. Everything else
stays forbidden.

In either mode: never merge the PR, never write a managed task pointer, and never modify task
markers. Never mention an AI assistant, and never add a co-author trailer or session link, in the
PR title or body.

## Inputs

Accept an optional `--auto` flag, an optional feature name, an optional managed task path, and
optional evidence from `finish-task`:

- task-review and review-fix-worker outcome (fixed findings, skipped minors with reasons);
- automated and manual verification proof;
- accepted security risks and the user's reasons.

Without a supplied task path, treat a unique active task whose `**Branch**` matches the current
branch as managed. Do not guess when more than one task matches.

## Process

### 1. Gather current state

Run:

```sh
git branch --show-current
git status --short
git diff --cached --stat
git diff --stat
git log main..HEAD --oneline || git log origin/main..HEAD --oneline
git diff --name-status main...HEAD || git diff --name-status origin/main...HEAD
git diff --stat main...HEAD || git diff --stat origin/main...HEAD
git diff --check
```

Confirm the current branch is not `main`. Read the changed files rather than inferring from paths.
Identify the observable result, dependencies, and material risks in the diff. Inspect the base,
current head, staged state, and working tree, then classify the complete change as `plan-only`,
`documentation-only`, `dependencies`, `configuration`, `code`, or `mixed`. Derive the matching
validation tier and retain both decisions in working context. Fail closed to `mixed` and `canonical`
when the classification is ambiguous.

One PR carries one logical change. Report unstaged or untracked changes that do not belong to this
PR and say so explicitly in the handoff rather than folding them in.

Do not run application lint, typecheck, builds, or tests for plan-only or documentation-only diffs.
Require `git diff --check` and any repository-provided document, link, or plan consistency check.
Dependency and configuration diffs use only their affected checks unless mixed with code.

When the caller supplies managed review evidence, confirm there is no unresolved supported finding,
security decision, or current-task proof gap. Return to the caller when supplied evidence is
incomplete. Standalone PR creation does not invent missing managed evidence.

### 2. Write the title

Invoke `write-well` before writing the title or body.

Titles state the outcome, in the present tense, in sentence case: "Stops the friction eval accusing
guests of repeating themselves", "Greets returning travelers correctly on the empty trips list",
"Adds the Stripe subscription webhook". Name what the repository now does, not the work performed.
Do not use a `type(scope):` prefix. Append a ticket id in parentheses only when the repository's
recent history does.

### 3. Write the body

Start from this template. It is the house format; when the repository ships its own
`.github/PULL_REQUEST_TEMPLATE.md` and it differs, the repository's file wins, headings and
checklist wording verbatim. Fill every section that applies, and prune the rest as described after
the template.

````markdown
# [Brief description of changes]

## Problem

<!-- Describe what was broken, unclear, or missing. Include:
- User-facing symptoms
- Root cause (if known)
- Why this matters
-->

## Solution

### Core changes

<!-- Describe the main technical changes. Use code snippets for clarity:

**[Component/module changed]**
```typescript
// Before
const problematic = oldApproach();

// After
const fixed = newApproach();
```

Focus on:
- What changed and why
- Key architectural decisions
- Performance/correctness improvements
-->

### Additional improvements

<!-- Optional: List secondary improvements, refactorings, or preparatory work -->

## Testing

<!-- Describe how changes were validated:
- [ ] Unit tests (specify which)
- [ ] Integration tests
- [ ] Manual testing scenarios
- [ ] Edge cases covered
-->

## Migration notes

<!-- Required: Explicitly state one of:
- "No breaking changes" (explain what's backward compatible)
- "Breaking changes" (list what breaks and migration steps)
- "Internal only" (no public API impact)
-->

## Files changed

<!-- Optional but recommended: Group changes by category for reviewers

**Core logic:**
- `path/to/file.ts` - Brief description

**UI:**
- `path/to/component.tsx` - Brief description

**Schema/Types:**
- `path/to/schema.ts` - Brief description
-->

## Screenshots/Video

<!-- Optional: For UI changes, add before/after screenshots or a demo video -->

## Checklist

- [ ] Tests pass locally (`pnpm test`)
- [ ] Types check (`pnpm typecheck`)
- [ ] Linter passes (`pnpm lint`)
- [ ] Updated CLAUDE.log (if architectural change)
- [ ] Updated relevant documentation

## Reviewers

<!-- Tag specific reviewers or areas to focus on:
@username - Please review [specific aspect]
-->
````

**Drop the sections the diff does not touch.** Omit `### Additional improvements` when there are
none, and add `## Screenshots/Video`, `## Checklist`, or `## Reviewers` only when they carry real
content. A section of `N/A` lines is noise a reviewer has to read past to reach the part that
matters, and an unticked box invites a reviewer to wonder whether the author forgot rather than
whether it applied. Delete the whole section; do not annotate it item by item. Then state in the
chat handoff which sections were dropped and why, so the omission is a visible decision rather than
a silent gap.

**Length.** Target under 400 words for the whole body. Past 600, cut rather than write more. A
small diff does not earn a long body: scale the body to what the reviewer must understand, never to
the effort spent producing it.

Section by section:

- **Problem** — the observable symptom in one or two sentences, and why it needed fixing; for a
  defect, name the symptom a user saw. Then the root cause in one short paragraph. Evidence is the
  shortest decisive artifact: one error id, one log line, one `file:line`. Never paste a full log,
  stack trace, or command transcript.
- **Core changes** — one to three bullets stating the material mechanism, plus one before/after
  snippet for the single change that carries the idea. Not one snippet per file, and not a snippet
  for a change the sentence already explains. Cite only the `path:line` references that help the
  reviewer understand the mechanism, not every location the diff touched.
- **Additional improvements** — bullets, one line each.
- **Testing** — two to four lines with concrete results ("`pnpm typecheck` clean", "559 passed, 1
  skipped"). State what the tests cover as concrete cases a reviewer can check against the change:
  give the inputs and expected results, not the mechanics. No test names, line numbers, fixtures, or
  framework details.
- **Migration notes** — one line stating exactly one of: "No breaking changes", "Breaking changes"
  (with the migration steps), or "Internal only".
- **Files changed** — grouped by category (`**State:**`, `**UI:**`, `**Tests:**`, `**Docs:**`), one
  line per file naming its purpose. No prose.
- **Checklist**, when present — tick an item only when it is verifiably true from the diff or from
  evidence the user supplied. Unticked is the default: never tick an item because it is probably
  true, because the work "should" have been done, or to make the checklist look complete. Never
  claim evidence under a heading it does not belong to — a server test run does not satisfy a client
  test claim. Items that need human eyes, such as browser checks or visual review, are never ticked
  on the user's behalf; collect them in the handoff's confirmation list instead.
- **Screenshots/Video** — for a non-visual change write `N/A — <reason>` or drop the section. For a
  visual change, leave it for the user and list it in the handoff as required.

Add a `### Why not the alternatives` block under `## Solution` only when a reviewer would plausibly
challenge the approach, as bullets, each naming the evidence that ruled the alternative out.

Throughout:

- Lead every section with its conclusion. The reviewer should get the point from the first sentence.
- Cut the investigation narrative. How long the cause took to find, what it looked like at first,
  and which theory was wrong belong in the changelog, not the PR, unless they change what the
  reviewer should check.
- Do not restate the diff in prose; `Files changed` already lists it.
- Never record the same evidence under two headings. If `Testing` already names a command and its
  result, the checklist does not repeat it.
- Replace or remove every placeholder the template carries, including its HTML comments. A merged
  PR still showing template scaffolding is a defect.
- Do not narrate self-evident edits — renames, formatting, import changes, code movement — unless
  they affect behavior or risk.
- Use a table only for a genuine comparison, never to format a list.
- Include every accepted security risk and the user's reason, in `Problem` or `Migration notes`.

### 4. Deliver

**Default (no `--auto`).** Write the filled body to `/tmp/pr-body.md`, then open it:

```sh
open /tmp/pr-body.md
```

Write only the body to that file. The title, commands, and notes belong in the chat reply, because
the file's whole contents get pasted into the forge.

Never write the body inside the repository. An untracked `pr-body.md` under the repository root
pollutes `git status` and can reach a commit. Always overwrite the file rather than appending, so a
previous PR's body cannot silently become the next PR's starting content.

**With `--auto`.** Stage only changes that belong to the PR, including related README and CHANGELOG
changes. Leave unrelated changes unstaged. Never stage secrets, credentials, local environment
files, or unrelated plan files. Commit using repository conventions. Push to `origin`, creating
upstream tracking when needed. Open the PR with `gh pr create` or the repository's documented
equivalent, using `main` as the base unless the user explicitly chose another branch. If the branch
already has an open PR, update and reuse it. Add configured labels and reviewers.

### 5. Confirm the managed task marker

Never commit a plan-pointer change onto the PR head. Doing so creates a new head that invalidates a
green run, and suppressing that rerun with `[skip ci]` leaves the merged head with no required
status at all. The pointer stays at `[~]` for the whole life of the PR; it moves to `[x]` after the
verified merge.

Find the master plan through the most specific `AGENTS.md` `Active plan` entry, falling back to
`CLAUDE.md`. Resolve the managed task from the supplied task path or a unique active task whose
`**Branch**` matches the current branch. Read the pointer without writing it:

- If no task matches and no task path was supplied, treat the PR as standalone and continue.
- If the pointer is `[~]`, that is the expected state. Continue.
- If the pointer is `[>]`, it was set by an older workflow. Leave it; it is closed after the merge.
- If the pointer is `[ ]` or `[x]`, stop and report the lifecycle mismatch. Also stop when the task
  path does not match or more than one task matches.

Do not move the task file and do not change the pointer; every managed-task write happens after the
merge, outside this skill.

### 6. Report

**Default.** Give these parts in order, each one line or compact bullets, with no restatement of the
body:

1. **Title** — ready to paste.
2. **File** — `/tmp/pr-body.md` is written and open; the reply does not repeat its contents.
3. **Commands** — in the order the user runs them: validation first, then push. Use
   `git push -u origin HEAD` for a branch with no upstream and bare `git push` once it has one.
4. **Needs your confirmation** — every checklist item left unticked that only the user can settle,
   and every screenshot or visual check left open, each with what would make it true.
5. **Dropped sections** — template sections deleted because the diff does not touch them, and why.
6. **Left out** — unstaged or untracked changes deliberately excluded from this PR, and why.

**With `--auto`.** Give the PR URL and number, base branch, head branch, head SHA, the managed task
path and its observed marker state when applicable, verification evidence, and accepted security
risks included in the PR. Report the same **Needs your confirmation**, **Dropped sections**, and
**Left out** lists; opening the PR does not settle them.

Stop without merging, and do not wait for CI. The user owns the merge.

### 7. Clean up on "done"

Default mode only. While `/tmp/pr-body.md` is open, revise it in place on request and report each
revision. When the user says `done`, delete it and confirm:

```sh
rm /tmp/pr-body.md
```

Delete it only on that explicit signal.
