---
name: skill-repo-readme
description: Generate or refresh the README.md for a skill repository — one that vendors agentskills.io skills under `.agents/skills/<name>/SKILL.md`. Scans every skill's frontmatter, builds a skills table, and writes install instructions (`npx skills add` per skill plus a `curl | bash` one-shot) and a layout section. Use when the user asks to create, update, generate, or refresh the README for a skill repo, when a repo's README is a bare stub, or after adding/removing skills under `.agents/skills/`.
tier: org
---

# Skill-Repo README Author

Generate or refresh the `README.md` for a **skill repository** — a repo whose payload is a
set of agentskills.io skills under `.agents/skills/<name>/SKILL.md`, each mirrored into
`.claude/skills/<name>` as a relative symlink (see the companion
[`claude-symlink-agent-individual-skills`](../claude-symlink-agent-individual-skills/SKILL.md)
skill). The README's job is to tell a reader **what skills the repo ships and how to install them**.

This skill produces that README deterministically with a bundled script, then has you polish
the prose the script cannot infer.

## When to use

- The repo's `README.md` is a bare stub (just a title) or missing.
- Skills were added to / removed from `.agents/skills/` and the README is now stale.
- The user asks to "create / update / generate / refresh the README for a skill repo".

## What a good skill-repo README contains

1. **Title + one-paragraph intro** — what the repo is and the `.agents → .claude` symlink convention.
2. **Skills table** — one row per skill: linked name + a one-line "what it does" (the first
   sentence of the skill's `description:` frontmatter).
3. **Install** — two paths:
   - **Per skill** via `npx skills add <owner/repo> --skill <name> -a claude-code`.
   - **One-shot** via `curl -fsSL .../install.sh | bash` (plus a `--dry-run` preview), when
     the repo ships a root `install.sh`.
4. **Layout** — the `.agents/skills/<name>/SKILL.md` source and `.claude/skills/<name>` symlink.

## How to run

The bundled generator is zero-dependency Node (stdlib only). It finds the repo root via
`git rev-parse --show-toplevel` (falling back to `$PWD`), reads each skill's frontmatter, and
derives the `owner/repo` slug from the `origin` remote.

**It skips git-ignored skills by default.** A skill repo typically *vendors* third-party
skills (re-fetched from upstream, listed in `skills-lock.json`, and `.gitignore`d so they
aren't committed) alongside the skills it actually authors. The README should document what
the repo *owns*, so any `.agents/skills/<name>/` directory that `git check-ignore` matches is
left out. Pass `--include-ignored` to list every skill regardless.

```bash
# 1. Preview the generated README — writes nothing
node .agents/skills/skill-repo-readme/bin/gen-readme.mjs --dry-run

# 2. Write it (see the clobber guard below)
node .agents/skills/skill-repo-readme/bin/gen-readme.mjs

# Operate on a different repo root
node .agents/skills/skill-repo-readme/bin/gen-readme.mjs /path/to/other-repo --dry-run
```

### Recommended workflow

1. **Generate the baseline** with `--dry-run` and read it.
2. **Refine the prose** the script left as placeholders — it marks them with
   `<!-- TODO(agent): ... -->`:
   - Rewrite the intro paragraph to say what *this* repo actually is.
   - If the repo has **no** root `install.sh`, replace the curl TODO with a working
     bootstrap command (e.g. point `curl` at the
     `claude-symlink-agent-individual-skills` installer) or add an `install.sh`.
   - Tighten any table cell whose first sentence reads awkwardly.
3. **Write** the file (drop `--dry-run`, add `--force` only when intentionally replacing a
   hand-written README — see below).
4. After editing prose by hand, keep the `<!-- gen-readme:auto -->` marker at the top **only
   if** you still want the file treated as regenerable; remove it once the README is
   hand-owned so future `--force`-less runs refuse to clobber it.

### Flags

| Flag | Effect |
|------|--------|
| `[root]` | Operate on a specific repo root instead of the detected one |
| `--dry-run` | Print the README to stdout; write nothing |
| `--check` | Exit `1` if `README.md` differs from freshly generated output (for CI) |
| `--force` | Overwrite an existing README even without the auto-marker |
| `--include-ignored` | List git-ignored skills too (default: skip them) |
| _(none)_ | Write `README.md`, but refuse to clobber a marker-less (hand-written) file |

## Safety guarantees

- **Never clobbers a hand-written README.** A plain write refuses to overwrite a `README.md`
  that lacks the `<!-- gen-readme:auto -->` marker; use `--force` to override deliberately.
- **Deterministic** — the same tree yields byte-identical output, so `--check` works as a CI gate.
- **Read-only against skills** — only ever reads `SKILL.md` frontmatter; never edits a skill.

## Relationship to other skills

- Pairs with [`claude-symlink-agent-individual-skills`](../claude-symlink-agent-individual-skills/SKILL.md),
  which creates the `.claude/skills` symlinks the README documents.
- Complements the `agent-skill-kit-*` toolkit (creator, validator, linter, …): those author
  and vet individual skills; this one documents the **repo** that ships them.

## GitHub operations

When this skill's output needs to be committed, branched, or turned into a PR/issue, use the
**`gh` CLI** (`gh pr create`, `gh issue create`) rather than any MCP GitHub tool.
