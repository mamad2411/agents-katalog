---
name: wiki-links
description: Audit and repair wiki link integrity, argument chain links, and link-layer structural rules across the repository.
---

# Wiki Links

Use this as the standalone skill for wiki link maintenance.
It owns the repository's deterministic link audit and repair workflow.

## What It Covers

- `argument-notes` -> `permanent-notes` deterministic link sync
- `supports` / `next` audit and repair
- permanent-note `Links` block cleanup
- reference-note `Links` / `References` cleanup
- broken `[[wikilink]]` target detection across `wiki/`
- hidden-folder targets such as `archive/.cache/*` being treated as broken for Obsidian browsing
- structure / argument / permanent layer link-rule audit
- permanent-note reachability from `structure-notes`
- permanent-note and reference-note `References` format audit

## Modes

- `audit`
  - Report repository issues without changing notes.
  - Use this when you want to inspect link health, empty links, bad targets, or rule violations.
- `fix`
  - Apply deterministic repairs after the argument logic is already correct.
  - Use this when you want to sync `supports/next`, prune disallowed `Links` residue, or normalize known-safe link structures.

## Scope Boundary

- This skill is for link integrity and link-adjacent repository rules.
- It does not decide semantic merges, argument boundaries, or missing bridge-note content.
- For semantic open questions, fix the note logic first, then run this skill.

## Workflow

1. Decide whether the task is `audit` or `fix`.
2. If argument order changed, update the argument note manually first.
3. Run audit to see broken targets and rule violations.
4. If the issue is deterministic, run the fix command.
5. Re-run audit until the relevant issue class returns to zero.

## Commands

Audit the whole wiki:

```bash
python3 skills/wiki-links/scripts/audit_argument_links.py
```

Audit selected argument notes:

```bash
python3 skills/wiki-links/scripts/audit_argument_links.py \
  wiki/argument-notes/20260414-如何构建长期有效的学习系统.md
```

Sync argument-derived `supports/next`:

```bash
python3 skills/wiki-links/scripts/sync_argument_links.py --apply
```

Sync selected argument notes and prune disallowed residue:

```bash
python3 skills/wiki-links/scripts/sync_argument_links.py --apply --prune-disallowed \
  wiki/argument-notes/20260414-如何构建长期有效的学习系统.md
```

Clean all permanent-note `Links` blocks without changing chain order:

```bash
python3 skills/wiki-links/scripts/clean_permanent_links.py --apply
```

Normalize permanent-note and reference-note structural residue:

```bash
python3 skills/wiki-links/scripts/normalize_permanent_references.py --apply
```

## Hard Rules

- Treat `audit` and `fix` as two separate modes, even when they use the same rule set.
- Do not auto-fix semantic chain decisions.
- Broken `[[wikilink]]` targets in `wiki/` are repository issues and must not be ignored.
- Links that only resolve through hidden directories like `archive/.cache/` are considered broken for Obsidian use.
- Prefer filename-only wikilinks in permanent-note `References` when the source file is in the vault.
- `structure-notes` 只允许指向 `argument-notes`。
- `argument-notes` 只允许与 `structure-notes` 和 `permanent-notes` 建立结构性关联。
- `permanent-notes` 用 `supports` 指向 `argument-notes`，用 `next` 指向同链路中的下一条 `permanent-note`。
- `reference-notes` 不使用 `supports` / `next`，`Links` 只用于相关 `permanent-notes`，`References` 统一使用 `from` / `references` / `url`。
