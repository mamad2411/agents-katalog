---
name: setup-cheety-skills
description: Installs the engineering harness into this repository — principles, workflow skills, the language-agnostic rule checker and one stack profile. Use this skill once per repository, right after adding the skills, or whenever somebody asks to set up the harness, add the rule checker, pick a stack profile, or wire up CI for it. It asks which stack the repository uses and installs only that one.
---

# Harness setup

Run this **once per repository**. It writes ordinary files that you own, commit
and edit. Nothing updates behind your back.

## What this installs

| Path | What it is |
|---|---|
| `AGENTS.md` | The eight principles, definition of done, language rule |
| `tools/arch-check/` | The rule checker plus the self-test for its rules |
| `tools/skill-eval/` | Issue rubric and the Test-first cycle check |
| `tools/arch-check/profiles/<stack>.json` | **Only the stack you choose** |
| `profiles/<stack>/PROFILE.md` | How the principles look in that stack |
| `.forgejo/`, `.github/` or `.gitlab/` + `.gitlab-ci.yml` | Workflows, issue templates, PR/MR template — for the forge you choose |
| `FORGES.md` | The differences between the three forges that fail silently |
| `.harness.json` | Records the chosen stack so CI and later runs agree |

## Steps

### 1. Ask which stack, unless it is obvious

Look at the repository first. `composer.json` with `laravel/framework` means
laravel; `package.json` with `typescript` means typescript; `pyproject.toml` or
`requirements.txt` means python. State what you found and ask for confirmation
rather than assuming — a wrong profile installs rules that never fire, which is
worse than none, because "0 findings" then looks like a clean codebase.

If nothing matches, list what is available:

```bash
node install.mjs --list
```

### 2. Ask which forge

`forgejo` (default), `github`, `gitlab` — or `none`. Look at the remote before
asking: a `git remote -v` pointing at github.com answers the question. Each forge
gets its own workflows, issue templates and PR/MR template; the differences that
fail silently are listed in `FORGES.md`.

### 3. Install

From the directory this skill lives in:

```bash
node install.mjs --stack laravel --forge github
```

Use `--dry-run` first if the repository already has an `AGENTS.md` or a `tools/`
directory. Existing files are never overwritten without `--force`, and the
installer prints what it skipped.

### 4. Verify — do not skip this

```bash
python3 tools/arch-check/eval.py --profile <stack>
python3 tools/arch-check/arch_check.py . --profile <stack> --coverage
```

The first command proves the rules still catch their planted violations and
raise no false positives. The second lists which of the eight principles the
profile covers.

**If `--coverage` reports a principle under "NO RULE AT ALL", say so.** A profile
that covers six of eight principles reports "0 findings" for the other two, and
that is indistinguishable from a clean codebase. Either add rules or declare the
principle `not_applicable` in the profile — silence by declaration, not by
omission.

### 5. Fill in the three project-specific gaps

`AGENTS.md` and `PROFILE.md` ship with placeholders. Without them the model
guesses:

1. **Reference files** — point them at real paths in this repository. The
   profile describes the house style; a real file *shows* it.
2. **`runs-on:`** in `.forgejo/workflows/*.yaml` — the label your runner uses.
   Forgejo only; the GitHub workflows use `ubuntu-latest` and GitLab has no
   equivalent line.
3. **Contact links** in the issue-template config — `.forgejo/issue_template/config.yaml`
   or `.github/ISSUE_TEMPLATE/config.yml`. GitLab has no such file; put the links
   into the templates themselves.

Then check the result mechanically:

```bash
python3 tools/forge_check.py .
```

## Updating later

```bash
npx skills update            # every installed skill — no name
node .claude/skills/setup-cheety-skills/install.mjs --stack <stack> --dry-run
```

**No name, and that is the point.** The harness is ten skills, not one: this one
carries the installer, the profiles, the tools and the slash commands, and the
nine workflow skills sit beside it as their own entries — `skills-lock.json`
lists each with its own path and hash. Naming this skill alone refreshes exactly
this one, which does not fail, it half-updates: the commands under
`assets/commands/` are new while the skills they point at are old.

`skills update` refreshes the skill directories. It does **not** touch the copies
already in your project — those are yours. The `--dry-run` shows what changed;
`--force` takes it.

## Adding a second stack

Run the installer again with the other stack. Profiles live side by side; the
checker takes `--profile` per run. `.harness.json` records the first one for CI —
edit it if the default should change.
