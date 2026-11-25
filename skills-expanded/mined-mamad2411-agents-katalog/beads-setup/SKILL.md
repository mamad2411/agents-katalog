---
name: beads-setup
description: Onboard a darkmatter repo onto beads (`bd`) as the standard task tracker and persistent agent memory store, per ADR-0001. Triggers when a repo has no `.beads/` directory, when `bd` is not installed, when the user asks to "use beads here", "set up beads", "add beads to this repo", "enable beads linear sync", or when an agent needs `bd ready` / `bd remember` and finds the workspace unconfigured. Also triggers when wiring beads to Linear for a team that already uses Linear. Do NOT trigger for routine `bd create` / `bd close` work in an already-initialized repo, or for non-darkmatter projects that have opted out of this convention.
---

# Beads setup

Bring a darkmatter repo into compliance with [ADR-0001](../../docs/adr/0001-beads-as-task-tracker-and-agent-memory.md): beads is the standard task tracker and persistent agent memory store, with optional bidirectional Linear sync.

This skill assumes you are an agent operating inside a darkmatter repo. Do the smallest correct sequence of steps below — do not skip the verification at the end.

## When to use

- The current repo has no `.beads/` directory and you (or the user) need to track work, remember context across sessions, or query `bd ready`.
- `bd` is not on `PATH`.
- The user says "use beads here", "set up beads in this repo", "add bd", "wire up beads", "enable beads linear sync", "connect this repo to our Linear", or similar.
- You are about to reach for `TodoWrite` / `MEMORY.md` / `TODO.md` in a darkmatter repo — stop and run this skill first.
- A `bd doctor` run reports missing hooks, missing AGENTS.md guidance, or missing Linear configuration in a repo that should have it.

## When NOT to use

- The repo already has a healthy `.beads/` directory, `bd` is installed, and agent recipes are present (`bd setup <recipe> --check` passes). Just run `bd ready` and work.
- The project explicitly opts out of beads (rare; document the exception in that project's `AGENTS.md`).
- You only need ephemeral, intra-turn checklists for the current response. ADR-0001 governs cross-session state, not single-turn scratchpads.
- You are inside a non-darkmatter third-party repo where adding `.beads/` would surprise upstream maintainers.

## Preflight

Run these in parallel before doing anything else. They are read-only.

```bash
# Repo + agent surface
pwd
git rev-parse --show-toplevel 2>/dev/null
ls -la .beads 2>/dev/null
ls AGENTS.md CLAUDE.md .opencode/AGENTS.md .codex/AGENTS.md 2>/dev/null

# bd availability + version
command -v bd && bd --version

# Linear hints (do NOT print secret values; just existence)
test -f components.sops.json && echo "sops config present"
test -n "${LINEAR_API_KEY:-}" && echo "LINEAR_API_KEY in env"
test -n "${LINEAR_TEAM_ID:-}${LINEAR_TEAM_IDS:-}" && echo "Linear team id in env"
```

Interpret the output:

- `.beads/` already exists → skip to **Verify**. Run `bd doctor` and `bd setup <recipe> --check` for each relevant agent client; only re-run install steps for what's missing.
- `bd` missing → go to **Install bd**.
- `.beads/` missing → go to **Initialize the repo**.
- No Linear env or config but the project is a team project → go to **Wire Linear** after init.

## Install bd

Prefer the package manager that already governs the user's machine. Confirm with the user before running an installer that mutates global state on a machine you don't own.

```bash
# macOS, Homebrew
brew install steveyegge/beads/bd

# Nix (darkmatter-canonical path; check the local flake first)
nix profile install nixpkgs#beads        # if available in nixpkgs
# or wire it into the user's existing home-manager / nix-darwin flake

# Cargo (works anywhere with a Rust toolchain)
cargo install beads-cli

# Manual binary fallback
# See https://github.com/steveyegge/beads/releases and place the binary on PATH.
```

Verify:

```bash
bd --version
```

If `bd` is intentionally pinned to a project-local version (e.g. via a Nix devshell), do not override it with a global install.

## Initialize the repo

Run from the repo root. `bd` auto-detects a prefix from the directory name; override with `--prefix` only if the directory name is generic ("app", "repo") or already taken in Linear.

```bash
bd init --non-interactive --role maintainer
```

What `bd init` does (the parts that matter here):

- Creates `.beads/` with an embedded Dolt database. This directory is tracked in git so the issue graph travels with the repo.
- Writes / updates `AGENTS.md` with a minimal pointer to `bd prime`. If `AGENTS.md` does not exist yet, use the default. If it does, beads appends a section; review the diff before committing.
- Installs git hooks that auto-export `.beads/issues.jsonl` after writes, so the issue graph is readable from a diff.

Sanity-check:

```bash
bd context        # confirm prefix + backend
bd onboard        # show the agent-instructions snippet bd init wrote
bd doctor         # warns about missing hooks, conventions, or sync issues
```

Commit the new state:

```bash
git add .beads AGENTS.md
git commit -m "chore(beads): initialize bd for task tracking and agent memory (ADR-0001)"
```

## Wire agent recipes

Install the integration for every agent client that already operates in this repo. Skip clients the user does not use. Each recipe is idempotent and supports `--check` and `--remove`.

```bash
# Inspect first
bd setup --list

# Per-client install (run only those that apply)
bd setup opencode      # this repo's primary agent client
bd setup claude        # Claude Code SessionStart + PreCompact hooks
bd setup codex         # Codex CLI skill + AGENTS.md guidance
bd setup cursor        # Cursor IDE rules
bd setup gemini        # Gemini CLI hooks
bd setup aider         # Aider config + instructions
bd setup factory       # Factory Droid AGENTS.md section

# Verify
bd setup opencode --check
bd setup claude --check
```

Do not install recipes for clients the user does not use; each one adds files and noise to the repo.

If the user wants the long-form agent reference embedded directly in `AGENTS.md` instead of the `bd prime` pointer (e.g. for Codex or Factory hosts that don't support hooks), re-run init with `--agents-profile=full`:

```bash
bd init --agents-profile=full --skip-hooks
```

## Wire Linear (if the project uses Linear)

Skip this section if the project does not use Linear. Confirm with the user first — pushing local issues into a team's Linear without authorization is destructive.

### Credentials

For an individual developer:

```bash
# Prefer the encrypted config pattern (see the sops-secret-access skill)
# Otherwise, scoped env vars in the user's shell profile:
export LINEAR_API_KEY=<REDACTED>
export LINEAR_TEAM_ID="<team uuid>"
# or for multiple teams:
export LINEAR_TEAM_IDS="<uuid1>,<uuid2>"
```

For a CI worker, use OAuth client credentials instead — they authenticate as an application, not a user:

```bash
export LINEAR_OAUTH_CLIENT_ID="..."
export LINEAR_OAUTH_CLIENT_SECRET=<REDACTED>
```

If the repo already uses SOPS for secrets, load Linear credentials from the encrypted file rather than committing them or putting them in `bd config`. See the `sops-secret-access` skill.

### Configuration

Stable, non-secret Linear configuration goes in `bd config`. This is committed and shared:

```bash
# Team selection
bd config set linear.team_id "<team uuid>"
# or
bd config set linear.team_ids "<uuid1>,<uuid2>"

# Optional: restrict to one project inside the team
bd config set linear.project_id "<project uuid>"

# Optional: hash IDs in Linear so they match bd
bd config set linear.id_mode "hash"
bd config set linear.hash_length "6"
```

Confirm beads can see the team:

```bash
bd linear teams
```

### First sync

Always preview before mutating Linear:

```bash
bd linear sync --dry-run
```

Read the diff. If it looks right:

```bash
bd linear sync --pull   # import existing Linear issues into bd
bd linear sync --push   # mirror local-only bd issues into Linear
bd linear sync          # bidirectional (pull then push) once both sides are clean
bd linear status        # confirm
```

If `--pull` produces a large import, commit the resulting `.beads/issues.jsonl` before doing anything else, so the import is auditable.

## Verify

Before declaring the repo set up:

```bash
bd doctor                                  # no errors / warnings about missing hooks or AGENTS.md
bd ready                                   # responds (empty list is fine)
bd remember "beads-setup completed for $(basename "$PWD")"
bd memories beads-setup                    # confirm the memory persisted
bd linear status 2>/dev/null               # only if Linear was wired
git status --short                         # only expected diffs are .beads/ + AGENTS.md + any recipe files
```

Commit any remaining recipe files added by `bd setup` together, with a clear message referencing ADR-0001.

## Common mistakes

- Running `bd setup claude` and `bd setup codex` and `bd setup opencode` in a repo where only opencode is actually used. Each recipe adds files; only install for clients the user has.
- Storing `linear.api_key` via `bd config set` instead of an env var or SOPS-encrypted file. `bd config` is committed; secrets in there leak.
- Skipping `--dry-run` on the first `bd linear sync`. Always preview against an unfamiliar team first.
- Re-running `bd init` to "fix" a broken-looking workspace. Use `bd doctor` and `bd bootstrap` first; `bd init` has destructive variants (`--reinit-local`, `--discard-remote`) that throw away history.
- Replacing the per-turn ephemeral todo list with beads. ADR-0001 governs cross-session state; intra-turn checklists are still fine in the agent client.
- Quietly committing decrypted Linear credentials when wiring up a CI worker. Use OAuth client credentials via env vars in CI, not the API key.

## Reference

- [`ADR-0001`](../../docs/adr/0001-beads-as-task-tracker-and-agent-memory.md) — the standing decision this skill operationalizes.
- [`sops-secret-access`](../sops-secret-access/SKILL.md) — for storing Linear credentials in SOPS-encrypted config.
- `bd quickstart`, `bd prime`, `bd onboard`, `bd doctor`, `bd linear --help` — the upstream surface; treat upstream output as more current than this file if they disagree.
