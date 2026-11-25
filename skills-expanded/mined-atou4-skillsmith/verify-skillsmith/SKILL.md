---
name: verify-skillsmith
description: Prove the skillsmith repo works end to end. Validates layout and manifests, installs every pack plugin into a throwaway Claude Code config from the working tree, checks what the npx skills CLI discovers, tests the skill-audit script on a known-bad fixture, and proves vendored skills match their pinned upstream. Use before pushing or tagging a release, after adding or editing any skill, or when a skill is missing from an install route.
metadata:
  internal: true
---

# Verify skillsmith

skillsmith is a library of agent skills with no server. Its "app" is the install paths users run: one Claude Code (and Codex) plugin per pack from `.claude-plugin/marketplace.json`, and the `npx skills` CLI, plus the repo's scripts. A change is verified when both install routes see exactly the skills the repo defines, vendored copies match their pins, and the checks are green.

This skill is agent-neutral. The one real copy lives in `.agents/skills/verify-skillsmith/` (read by Codex); `.claude/skills/verify-skillsmith` (Claude Code) and `.cursor/skills/verify-skillsmith` (Cursor) are symlinks to it. Edit the real copy only. Everything runs from the repo root. The helper does the work; the feature map in `features/` says what each check proves.

## Launch

There is no process to keep alive. "Launch" means create an isolated Claude Code config and install into it:

```bash
.agents/skills/verify-skillsmith/scripts/verify.sh install
```

It adds the local marketplace and installs every plugin it lists. Ready when it prints `PASS: install: plugins <names>; <n> skills registered from the working tree`. The helper sets `CLAUDE_CONFIG_DIR` to a throwaway directory for every subcommand and refuses to run against `~/.claude`. Never run `claude plugin install` for this repo without it: that would install into the user's real setup.

The plugin is copied into the isolated cache at install time. After editing a skill, run a fresh `install` (a new `RUN_ID` gives a new isolated config) rather than expecting the old install to update.

## Doctor

Read-only. Run it first, and again whenever a result looks wrong:

```bash
.agents/skills/verify-skillsmith/scripts/verify.sh doctor
```

It reports the repo path, `claude`, `python3`, `uv` and `npx` availability, each pack plugin with its version, the skill names found under `skills/`, and how many files are uncommitted. It fails if `claude` or `npx` is missing. If the git dirty count is not what you expect, stop and find out why before trusting a result: the install route reads the working tree, not the last commit.

## Drive

One command runs everything, and each step has its own subcommand:

| Step | Command | What it asserts |
|---|---|---|
| Static | `verify.sh static` | `scripts/validate-skills.py` prints `OK:` (with PyYAML, so invalid YAML frontmatter fails), and `claude plugin validate .` prints `Validation passed`. |
| Plugin install | `verify.sh install` | Every plugin in `marketplace.json` installs from the local path at its declared version, "Read from" is this repo, and the union of registered skills equals the folders under `skills/`. |
| CLI discovery | `verify.sh discover` | `npx skills add <repo> --list` lists exactly the repo's skills, and no skill folder or lock file changed. |
| Audit fixture | `verify.sh audit-fixture` | `skill-audit`'s script finds the broken symlink, name mismatch and missing SKILL.md in a fixture built for the purpose. |
| Vendored copies | `verify.sh vendor` | Every skill in `vendor.json` is byte-identical to upstream at its pinned commit (LICENSE is the only allowed extra), and reports whether upstream has moved since. Needs network; set `GITHUB_TOKEN` to avoid rate limits. |
| Everything | `verify.sh all` | All of the above, then cleanup. Prints `ALL PASSED. Evidence: <dir>`. |

Prefer `all`. Use single steps to localize a failure. Set `RUN_ID=<name>` to keep a run's files together across steps.

The two install routes can disagree, and that is the point of checking both: Claude's plugin loader tolerates frontmatter that the `skills` CLI rejects (an unquoted `: ` in a description is invalid YAML, and the CLI silently skips that skill).

## Evidence

Everything lands in `.agents/skills/verify-skillsmith/artifacts/<RUN_ID>/` (git-ignored):

- `summary.txt`: one `PASS:` line per step. A missing line means the step did not pass.
- `doctor.txt`, `validate-skills.txt`, `plugin-validate.txt`: static results.
- `install.txt`: the add, install, list and details output, including version and "Read from".
- `skills-list.txt`: the skill names the CLI discovered; `skills-list-raw.txt` is the raw output.
- `audit-fixture.txt`: the audit report for the fixture.
- `vendor.txt`: the vendored-copy comparison and upstream status.
- `failures.txt`: only exists if something failed.

Proof standards for this repo:

- Exercise the real routes (`claude plugin install`, `npx skills add --list`), not the validator alone. The validator passed while one skill was invisible to the CLI.
- Compare sets, not counts: installed names against folders under `skills/`.
- `npx skills add --list` is read-only. This was observed, not assumed: skill folder counts under `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills` and the lock file's modification time were identical before and after. The helper re-checks this each run. Never run `npx skills add` without `--list` as part of verification: it installs into the user's machine.
- Do not run `npx skills update` or `update --help`: it performs a real update.
- Report a skipped step with the command you ran and why it could not run. Do not count a step as verified through a different path.

## Cleanup

```bash
.agents/skills/verify-skillsmith/scripts/verify.sh clean   # with the same RUN_ID
```

It removes the isolated marketplace and config and deletes the throwaway directory. `all` runs it automatically on exit. It never deletes `artifacts/`. Do not kill processes by name; this verification starts none that outlive a command.

## Helpers

- `scripts/verify.sh <doctor|static|install|discover|audit-fixture|vendor|clean|all>`: described above. Executable; requires `claude`, `npx` and `python3`; uses `uv` for PyYAML when present. CI runs `discover`, `audit-fixture` and `vendor` (they do not need the `claude` CLI).

## Feature map

Read `features/README.md`, then the feature file that matches what changed. Each lists the entry points, the exact commands and the end state that proves it.
