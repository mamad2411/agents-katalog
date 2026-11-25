---
name: canonical-source-vs-workflow-repo-audit
description: Audits a repository to classify it as canonical-source or workflow-backup before allowing source code edits.
category: Git-Operations
---

# Canonical-Source vs Workflow-Repo Pre-Edit Audit Skill

> **Skill ID:** `canonical-source-vs-workflow-repo-audit`<br>
> **Version:** 1.0.0<br>
> **Type:** Atomic + script

## Description

Before editing source code under any Git working tree, classify the
enclosing repository as **canonical-source**, **workflow-backup**, or
**mirror**. The audit blocks the "edited the wrong repo" mistake
common in ecosystems where a workflow / backup / CI repo coexists with
the canonical source repo and shares a similar name pattern.

### Real-world trigger (Account-Ledger ecosystem)

- `Account-Ledger-Server` — the **workflow / backup** repo. Hosts
  `.github/workflows/database-backup.yml` and a small `http_API/` snapshot
  of the live production server. Edits here NEVER reach the canonical PHP.
- `Account-Ledger-Server-PHP` — the **canonical source** PHP repo. Every
  HTTP-API edit MUST land here first; the workflow repo only consumes
  what production already serves.

In May 2026 an edit to `select_User.php` landed in the workflow repo,
was caught by review, soft-reset, and re-applied in the canonical repo.
This skill exists to **stop that mistake at pre-edit time**.

## When to Apply

- Before the first `cat > <file>` / `edit` call in any repository the
  session has not previously edited.
- Whenever two repository names share a common prefix or suffix that
  hints at related-but-distinct roles.
- Whenever a file's path matches paths already known to exist in another
  cloned-locally repo.

Do NOT apply when:
- Editing files under the audit-tool's own repo (the audit ROOT is itself).
- Editing config / dotfiles that are explicitly the repo's purpose
  (e.g. editing `.github/workflows/*` IN the workflow repo).

## Procedure

### Step 1 — Run the audit

```bash
python3 .agents/skills/canonical-source-vs-workflow-repo-audit/scripts/audit-repo-role.py /path/to/file/or/dir
```

Output:

```
REPO_ROOT: /Users/dk/lab-data/Account-Ledger-Server
VERDICT:   workflow
SIGNALS:   {'workflow': 5, 'canonical': 4, 'mirror': 0}
  - 1/1 workflow files match backup/mirror/sync pattern
  - 17/20 recent commits look like backup/snapshot/mirror
  - manifest(s) at root: composer.json
  - source dirs ['http_API'] contain 24 files

WARNING: editing source code in a workflow repo is almost always wrong.
         Locate the canonical source repo before proceeding.
```

### Step 2 — Decide

| Verdict | Action |
|---|---|
| `canonical` | Proceed with the edit. |
| `workflow` | **STOP.** Find the canonical source repo (often a sibling dir; ask user). |
| `mirror` | **STOP.** Never edit a read-only mirror. |
| `unknown` | Ask the user; the audit's heuristics are inconclusive. |

### Step 3 — Soft-Reset Recovery (when wrong repo already edited)

If the mistake was discovered AFTER an edit + commit in the wrong repo:

```bash
# Repo: wrong (workflow) repo
git -C /path/to/wrong/repo log --oneline -3   # confirm the mistaken commit is HEAD
git -C /path/to/wrong/repo reset --soft HEAD~1
git -C /path/to/wrong/repo restore --staged http_API/<file>.php  # unstage
git -C /path/to/wrong/repo checkout -- http_API/<file>.php       # discard

# Verify clean
git -C /path/to/wrong/repo status

# Re-apply the same change in the canonical repo
# ...then commit per git-atomic-commit-construction
```

CRITICAL: never `git reset --hard` — soft + restore + checkout
preserves any unrelated WIP. See
[`git-operation-rules.md`](../../../ai-agent-rules/git-operation-rules.md).

## Heuristic Signals (consulted by the script)

| Signal | Weight | What it indicates |
|---|---|---|
| `.github/workflows/*.yml` filenames match `backup\|snapshot\|mirror\|sync\|dispatch` for ≥50% of files | +3 workflow | Repo's primary job is CI orchestration / backup. |
| ≥10 of last 20 commit titles match same keywords | +2 workflow | Recent commit history dominated by automated backups. |
| Source manifest at root (`composer.json` / `package.json` / `pom.xml` / `mise.toml` / etc.) | +2 canonical | Repo declares itself as a buildable project. |
| ≥10 files inside `src/` / `lib/` / `http_API/` / `app/` / `kotlin/` / `java/` / `pkg/` / `cmd/` / `internal/` | +2 canonical | Real source tree present. |
| README declares "mirror of X" | +3 mirror | Explicit mirror declaration. |

A verdict requires the top-scoring category to have ≥2 signal weight;
otherwise the verdict is `unknown`.

### Tie-breaker note

A repo can score positive in BOTH `workflow` AND `canonical` (e.g. the
Account-Ledger-Server case: it has 1 backup workflow AND a small
`http_API/` source dir for production sync purposes). The script picks
the highest score; tied scores fall back to `unknown`. **Always present
the verdict + signals to the user — the human breaks ambiguous ties.**

## Composition with Other Skills

This audit is referenced as a **Step 0 / pre-edit** check by:

- [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) Step 0d — before authoring any new commit in a previously-unedited repo.
- [`php-mysqli-prepared-statement-modernization`](../php-mysqli-prepared-statement-modernization/SKILL.md) §Pitfalls — explicitly requires the audit before any PHP modernization edit.

## Pitfalls

| Pitfall | Mitigation |
|---|---|
| Two repos with `canonical` verdict for same artifact (forks) | Audit is single-repo; cross-repo provenance still requires human verification. |
| Repo recently rebranded from workflow to canonical (commit history misleads) | Manually inspect README + ask user. |
| Monorepo with both workflow and source subtrees | Audit returns one verdict per ROOT; not designed for monorepo subtree classification. |

## Related Skills

- [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) — Step 0d invokes this audit.
- [`git-personal-sandbox-remote`](../git-personal-sandbox-remote/SKILL.md) — distinct concern: routing personal-only commits.

## Scripts

| Script | Tier | Purpose |
|---|---|---|
| [`scripts/audit-repo-role.py`](scripts/audit-repo-role.py) | Deterministic | Classify enclosing repo via weighted-signal scoring. |
