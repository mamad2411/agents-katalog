---
name: worktree-standard
description: Create, resume, audit, and assess cleanup of Git worktrees under the shared cross-client standard. Use whenever creating a parallel checkout, choosing a worktree directory or branch name, coordinating jcode, pi, codex, claude, orca, pi-durable, or cursor, or inspecting orphan worktrees. Route creation through the bundled helper rather than inventing paths or deleting by age or branch prefix.
---

# Shared worktree standard

## Contract

Apply to new worktrees; preserve existing paths and branches unless the user explicitly authorizes removal of a managed worktree. Do not move, rename, prune, or change global Git hooks as part of adoption. Raw Git worktree mutations remain blocked; the helper's `remove` command is the sole managed-removal route, and its `--confirm` flag does not replace explicit user authorization.

```text
~/worktrees/<repo-key>/<client>/<task>--<unique-id>
<client>/<type>/<task>--<unique-id>   # new branch
```

Clients: `jcode`, `pi`, `codex`, `claude`, `orca`, `pi-durable`, `cursor`.
Task and type: lowercase kebab-case. Repo key derives from sanitized origin identity, with a stable local-only fallback. For `git@github.com:priceless/modern-visa.git`, use `github.com--priceless--modern-visa`, not just the repo basename or owner. Let the helper compute it. Never print remote credentials. Existing branches keep their names. Directory and branch naming identify intent, not authority to delete.

## Create

Run the installed helper, using the actual client and session ID. Do not claim another client's identity.

```bash
HELPER="$HOME/.agents/skills/worktree-standard/scripts/worktree.py"
python3 "$HELPER" plan --repo "$REPO" --client claude --task fix-onboarding --type fix
python3 "$HELPER" create --repo "$REPO" --client claude --task fix-onboarding --type fix --session "$SESSION_ID" --base HEAD
```

Use `--branch <existing-branch>` to preserve a branch rather than create one. Git retains its native branch checkout protections. No `--force`, `-B`, or automatic branch deletion. Use the returned path, never reconstruct it from the task name. Plan is a preview, not a reservation: create can generate another unique ID.

## Remove

Only remove a helper-managed worktree after explicit user authorization. `--confirm` is a required CLI acknowledgment, not authorization. The helper validates eligibility, removes the worktree directory, preserves its branch, and reports blockers/assessment; do not substitute raw `git worktree remove`, force, prune, or branch deletion. Omit `--root` for the default `~/worktrees`; set it only for a custom managed root.

```bash
python3 "$HELPER" remove --path "$WORKTREE_PATH" --confirm
```

Install dependencies and execute project commands in a subshell at the returned path. Keep the coordinator's working directory stable.

## Resume and ownership

Inspect `git worktree list --porcelain` before creating a duplicate. Reuse matching owned worktrees after inspecting their status. The helper stores creator client and session in the per-worktree Git metadata, outside tracked files. Metadata is provenance, not an authentication boundary.

An explicit cross-client handoff may authorize reuse. Preserve creator attribution; record the handoff separately. Do not rewrite ownership opportunistically. Missing metadata or a moved path means legacy/unknown, not disposable.

## Cleanup assessment

```bash
python3 "$HELPER" check --path "$WORKTREE"
```

`check` is read-only. It does not remove anything. Treat unknown ownership, mismatched paths, locked worktrees, dirty or untracked files, Git errors, and commits without another preserving branch/ref as blockers. Remote refs are local snapshots, not fresh evidence from the server. Even a clean result does not prove inactivity or authorize removal.

Before any destructive cleanup, obtain explicit authorization for the exact paths, establish session inactivity and commit preservation, and recheck immediately before using Git's native removal. Do not delete directories with `rm -rf`. Broken pointers may indicate relocation and contain unique files. Preserve them pending recovery.

## Integration

Read `references/integration.md` when configuring clients. Prefer a native worktree-root setting when documented. Route agent-driven creation through this helper via shared skill discovery or existing instruction files. Add hooks only where the client's documented event and rejection behavior can be verified. Do not pretend an advisory prompt enforces a built-in UI action.

Report coverage separately: policy discoverable, helper creation tested, native configuration verified, hook enforcement verified. The bundled `scripts/hook.py` blocks normal literal raw Git worktree mutation commands in supported native shell tool hooks; `plan`, `create`, `check`, and read-only Git remain available. Direct UI creation, aliases, obfuscated shell commands, and subprocesses outside hooked tools are not universally covered. This is a workflow guard, not a security sandbox. Do not work around a denial; legacy cleanup or relocation needs a reviewed exception. Unknown support stays unknown. Do not replace existing hook chains or intercept every `git` executable.
