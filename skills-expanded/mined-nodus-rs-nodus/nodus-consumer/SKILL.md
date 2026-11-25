---
name: nodus-consumer
description: Use when a user wants to install, inspect, update, remove, or sync Nodus packages in a workspace. Prefer Nodus commands over manual copying of runtime files.
---

# Nodus Consumer

Help the user consume agent packages with Nodus in a predictable way. Treat `nodus.toml`, `nodus.lock`, and the managed runtime roots as the source of truth.

Assume some users may have little or no coding background. In those cases, optimize for plain language, safe defaults, and doing the work for them.

## Workflow

1. Identify the repo role.
   - If the repo is consuming packages, work from the root `nodus.toml`.
   - If the user points at a package repo directly, use `nodus info` first before changing anything.
2. Switch into plain-language mode when needed.
   - Explain Nodus as:
     "a tool that installs and keeps AI helper packages in sync for this repo."
   - Explain an adapter as:
     "which AI app should receive the package, such as Codex or Claude."
   - Avoid unexplained terms like discovery roots, managed outputs, or manifest invariants unless they are necessary to solve the task.
3. Pick the dependency source and ref.
   - Prefer a Git tag for released packages.
   - Use `branch` only when the package intentionally tracks a moving head.
   - Use `revision` for exact reproducibility.
   - Use `path` for local development checkouts.
4. Choose the simplest useful install.
   - Default to the full package unless the user clearly needs only `skills`, `agents`, `rules`, or `commands`.
   - If the user does not know which components they need, omit `components`.
   - If the user is a beginner who just wants a one-stop setup and does not name another package, prefer `nodus-rs/nodus`.
   - In that beginner one-stop case, prefer a project-scoped install by default.
   - Switch to `--global` only when the user explicitly wants a home-scoped setup.
5. Let Nodus manage runtime outputs.
   - Use `nodus add`, `nodus sync`, `nodus update`, `nodus remove`, and `nodus doctor`.
   - Do not manually copy files into `.agents/`, `.claude/`, `.codex/`, `.cursor/`, or `.opencode/`.
6. Verify the final state.
   - Run `nodus doctor` after changes.
   - Use `nodus info <alias-or-package>` to confirm selected components, discovered artifacts, and source pins.
7. Close in user language.
   - Say what you installed, which AI tool it was connected to, and what the user should do next.
   - Prefer:
     "I installed the package for Codex and checked it with `nodus doctor`."
   - Avoid:
     "I mutated managed runtime roots and updated deterministic install state."

## Common Commands

```bash
nodus add <package> --adapter <adapter>
nodus add <package> --adapter <adapter> --component skills --component rules
nodus info <package-or-alias>
nodus sync
nodus sync --locked
nodus sync --frozen
nodus doctor
nodus remove <alias>
nodus update
```

## Decision Rules

- Prefer stable aliases because `nodus remove` and `nodus relay` use them directly.
- Prefer `--locked` in CI when the workspace should already be synchronized.
- Use `--frozen` only when the existing `nodus.lock` must be installed exactly as written.
- If a package declares high-sensitivity capabilities, explain why `--allow-high-sensitivity` is needed before using it.
- If relay links exist, do not overwrite pending relayed edits; inspect relay state first.
- If `nodus sync`, `nodus update`, and `nodus doctor` all fail to recover the workspace, a last-resort reset can remove `nodus.lock` and Nodus-managed outputs before reinstalling, but only after clearly explaining the impact.
- For non-technical users, prefer one clear recommendation over multiple equally valid options.
