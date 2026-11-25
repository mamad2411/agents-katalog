---
name: rc-git
description: "Moves work onto a branch, pushes, opens a PR; also rebase and conflicts. Use to ship local work. Do not use to commit in place."
model: haiku
effort: medium
---

# Git Branch, Push & PR

Take the work currently in this repo from "changes on disk" to "PR opened", stopping for the user's confirmation at every outward-facing step. This skill is standalone — it does not read or require any `.rc/` workflow artifacts.

Ask every confirmation question in the user's language. An optional Linear issue (e.g. `PROJ-123`) may be supplied when the skill is invoked; if present, use it and skip the ticket question.

**Always write the PR title and description in Brazilian Portuguese (pt-BR)**, regardless of the conversation language. Keep the conventional-commit type prefix (`feat:`, `fix:`, etc.) in the title; everything else is in pt-BR.

Use a TodoWrite list to track the phases. Run them **in order**; commit, push, and opening the PR each need their own explicit yes — approval for one step never carries over to the next.

## Phase 0 — Gather git state

Before anything else, inspect the real repository state by running:

```bash
git rev-parse --is-inside-work-tree           # is this a git repo?
git branch --show-current                      # current branch (empty = detached HEAD)
git symbolic-ref --quiet refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'  # default branch
git status --short                             # working tree changes
git log --oneline @{u}..HEAD                   # local commits ahead of upstream
git remote -v                                  # remotes
command -v gh                                  # is the gh CLI available?
```

Base every later decision on this real state, not on assumptions.

## Phase 1 — Inspect & guard

- If this is **not** a git repo → stop and say so. Don't run anything else.
- If `HEAD` is **detached** → stop and ask the user to check out a branch first.
- Determine the **default branch** (the remote HEAD from Phase 0; if unknown, ask the user — commonly `main` or `master`).
- If the working tree is clean **and** there are no local commits ahead of the upstream/default → there's nothing to ship: tell the user and stop.

## Phase 2 — Summarize the changes

Build a concise, human-readable summary of what was done, from the actual diff — not guesswork:

- Working changes: `git status --short`, `git diff --stat`, `git diff --cached --stat`; read the diffs as needed.
- Any local commits ahead: `git log --oneline <base>..HEAD`.

Group by area/file and describe the intent (what changed and why), in a few bullets. If the diff is large, summarize honestly rather than omitting anything material. Reuse this summary for the branch name, commit message, and PR body.

## Phase 3 — Create the feature branch (only if on the default branch)

Skip this whole phase if the current branch is **not** the default branch — the work is already on a feature branch; go to Phase 4.

If on the default branch:

1. **Linear issue** — if a ticket was supplied at invocation, use it. Otherwise ask via **AskUserQuestion** whether a Linear issue should go in the branch name. **Default is no ticket** — only include one if the user provides it (they can type it via "Other").
2. **Propose branch names** — suggest 2–3 candidates via **AskUserQuestion** (recommended first, plus "Other" for a custom name). Build each as kebab-case from the summary:
   - Pick a type prefix that fits the change: `feat/`, `fix/`, `chore/`, `refactor/`, `docs/`, or `test/`.
   - No ticket (default): `<type>/<short-slug>` (e.g. `feat/git-branch-flow`).
   - With ticket: `<type>/<TICKET>-<short-slug>` (e.g. `feat/PROJ-123-git-branch-flow`).
   - Keep the slug short (3–5 words), lowercase, ASCII, hyphen-separated.
3. **Confirm creation** — show the chosen branch name **and** the commit message you'll use (subject from the summary; body with the bullets). Ask to proceed. On yes:
   - `git switch -c <branch>` (this carries the uncommitted working changes onto the new branch; the default branch stays untouched).
   - `git add -A && git commit` with the message. Do **not** add any co-author trailer or tool attribution to the commit message.
4. **Optional cleanup** — if the default branch had local commits ahead of its upstream (those commits are now also on the feature branch), offer to reset the local default branch back to its upstream so it stays clean (`git branch -f <default> <default>@{u}` — only while not checked out on it). Only offer this if it actually applies; let the user decline.

## Phase 4 — Push (confirm)

Confirm via **AskUserQuestion** before pushing. There must be a remote (`origin`); if none, say so and stop. On yes:

- `git push -u origin <current-branch>`.

Report the result (and the remote branch URL if the push output gives one).

## Phase 5 — Open the PR (confirm + confirm the target)

1. **Confirm the target base branch first** — detect the default branch as the suggested base, but **always ask** via **AskUserQuestion** which branch the PR targets, because some projects open PRs against a branch other than the default. Offer the detected default (recommended) and let the user pick another (list candidates from `git branch -r` or accept a custom one via "Other").
2. **Build the PR body in pt-BR** from the "PR description template" below, filling each section from the Phase 2 summary and the real diff. Omit sections that don't apply rather than writing filler. Use the supplied Linear issue (if any) in "Issue relacionada".
3. **Confirm opening the PR** — show the title (commit subject, in pt-BR) and the rendered body and the resolved `head → base`. On yes, open it with `gh`:
   - Write the rendered body to a temp file (e.g. `"$TMPDIR/rc-pr-body.md"`) and pass it with `--body-file` — markdown templates are multi-line and break with an inline `--body "..."`:
     `gh pr create --base <target> --head <current-branch> --title "<title>" --body-file <path>`.
   - Do **not** add any tool attribution or "generated with" footer to the PR body.
   - If `gh` is **not installed**, don't fail silently: print the GitHub "compare" URL (`<repo-url>/compare/<target>...<current-branch>?expand=1`) so the user can open it manually.

Report the PR URL.

## PR description template

Render the PR body in **Brazilian Portuguese (pt-BR)** using the structure below. Fill each section from the Phase 2 summary and the real diff; omit any section that doesn't apply rather than leaving placeholders. In "Tipo de mudança", check the single box matching the branch/commit type prefix.

```markdown
## Resumo
<o que mudou e por quê, em 1–3 frases>

## Tipo de mudança
- [ ] Feature
- [ ] Correção de bug
- [ ] Refatoração
- [ ] Documentação
- [ ] Chore / build / infra

## Mudanças
- <um bullet por área/arquivo, a partir do resumo da Phase 2>

## Como testar
<passos para o revisor validar localmente: comandos, testes ou fluxo a exercitar>

## Checklist
- [ ] Testado localmente
- [ ] Testes adicionados/atualizados quando aplicável
- [ ] Sem alterações não relacionadas ao objetivo da PR

## Issue relacionada
<ID da issue do Linear ou link; "N/A" se não houver>
```

## Guardrails

- Never touch unrelated branches.

## Rebase e resolução de conflitos

Handle git rebase operations and resolve merge conflicts intelligently while preserving features and maintaining code quality. Use this section when rebasing feature branches or resolving conflicts across commits. The full strategy decision matrix, conflict decision framework, diagnostic commands, troubleshooting, and automated/CI resolution live in `references/` — read the matching file **in full** when you reach that need in the workflow below, don't rely on memory of it.

### Quick start

For most rebases with 3+ commits, squash first to resolve conflicts once instead of per-commit:

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
git branch backup-rebase-$TIMESTAMP           # Step 1: safety backup
git rebase -i $(git merge-base HEAD origin/main)  # Step 2: squash commits
git rebase origin/main                        # Step 3: rebase onto target
# If conflicts: resolve, then git rebase --continue
git push origin $(git rev-parse --abbrev-ref HEAD) --force-with-lease
```

### Workflow

1. **Backup** — create the timestamped backup branch above (or note the current HEAD SHA via `git reflog`) before touching anything.
2. **Fetch & compare** — `git fetch origin`; `git log --oneline origin/main..HEAD` (your commits) vs `HEAD..origin/main` (new commits on main).
3. **Predict conflict scope** — `git diff --name-only origin/main...HEAD` vs `origin/main HEAD`; files changed on both sides will conflict.
4. **Choose a strategy** — read `references/strategies.md` **in full** for the decision matrix (squash-first, interactive, simple linear, rerere, or merge-instead) and each strategy's tradeoffs.
5. **Resolve conflicts** — read `references/resolution-patterns.md` **in full** for the conflict-marker anatomy and decision framework. Never delete a marker without understanding both sides; a feature must never silently disappear.
6. **Validate** — lint/type-check the resolved files, then run the test suite. Never continue a rebase (or force-push) on top of a failing validation.
7. **Force-push safely** — only `--force-with-lease` (never bare `--force`), and only after tests pass.

Diagnostic one-liners and the bundled helper scripts (`scripts/pre-rebase-backup.sh`, `scripts/analyze-conflicts.sh`, `scripts/validate-merge.sh`) are in `references/scripts-tools.md` (in full). Common failure modes — stuck rebase, lock errors, lost commits after a force-push — are in `references/troubleshooting.md` (in full). CI/automated conflict resolution (`-X theirs`/`ours`/`recursive`) is in `references/automation.md` (in full) — only for non-critical, well-tested changes, never as the default.

### When NOT to rebase

Shared branches, critical production code without comprehensive tests, or when multiple people push to the same branch — use `git merge origin/main` instead. Default to merge if uncertain.
