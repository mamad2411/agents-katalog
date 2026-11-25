---
name: manage-my-skills
description: At the beginning of every session, inspect and safely maintain personal and source-installed Agent skills, detect reusable workflows for new or updated skills, reconcile independently connected machines, and keep this manager current. Use when organizing, installing, updating, backing up, synchronizing, restoring, joining, or diagnosing skills; managing a private skill library; or preserving a reusable workflow from the current task.
license: MIT
---

# Manage My Skills

Manage the public manager and the user's private skill library as two independent repositories. Never place private skills, credentials, local paths, connection details, or personal inventory in this public repository.

## Start Every Workflow

1. Locate this skill's `scripts/manage_my_skills.py`.
2. At the beginning of every session, run the read-only `maintain` check once. It combines manager update status, environment checks, the full local scan, private-library status, managed-link health, and public-source installation status. Do not replace it with a narrower check.
3. If the manager skill is not installed in the current Agent's skill root, run `install-manager` in preview mode and ask for approval before creating the link. The link must point to this public manager checkout; never copy a stale skill directory.
4. If `maintain` reports a fast-forward manager update, report it and offer to update the public manager before changing managed skills. After an update, re-read this `SKILL.md` and run `maintain` again.
5. Explain the result in plain language. Do not assume the user knows Git or GitHub.
6. Preview mutating commands first. Use `--apply` only after the user approves the stated files, repository, and effects.

If `maintain` reports local private skill changes or remote private-library updates, automatically run `sync` without `--apply` and include that detailed preview. If it reports missing, broken, wrong, or occupied managed links, automatically run `restore` without `--apply` and include that preview too.

For a capture-only suggestion, do not interrupt the current task with a network check. Run the manager check after the user accepts the suggestion and before changing skill files.
If the update check cannot reach the remote, report that the version is unverified and continue only with work that does not depend on a manager update. Never describe a failed check as current.

`manager-status` checks the public manager through Git; it does not require GitHub CLI login. Keep that result separate from `doctor`'s private-library authentication check. If local Git metadata cannot be refreshed, report the version as unverified and name the metadata or network issue only when it was directly observed. Never infer a read-only `FETCH_HEAD` or missing GitHub login from an unrelated fetch failure.
Remote version and GitHub authentication checks use a bounded timeout. A timeout is a network-unavailable result, not proof that the credentials or repository are invalid.
Before GitHub-dependent work, check GitHub network reachability. If it fails, report whether a proxy was detected, suggest configuring a proxy or requesting network access, and do not label the user as unauthenticated until connectivity is available.

GitHub operations use command-scoped HTTPS and existing `gh` authentication. For a required local proxy or a legacy Git error, follow [network-and-git.md](references/network-and-git.md): preview and save machine-local routing with `network-config`, then use the normal commands. Do not keep temporary Git wrappers or edit global Git/SSH configuration. Private-repository verification and all mutation guards still apply.

## Report Counts Without Mixing Scopes

Every inventory or maintenance report must keep these quantities separate:

- **Private-library managed skills**: the count and names from `status.skills`; these are the user-owned skills backed up in the private repository.
- **Source inventory records**: the count and names from `status.sources`; these are public, marketplace, plugin, or other skills tracked by portable source metadata.
- **Full local scan**: the count and classification from `scan.skills`; this includes skills outside the private library and must never be called the managed-skill count.

Report all three labels when both `status` and `scan` were run. Installation links are a separate health check, not another skill inventory. A scanner may not traverse directory symlinks, so a scan count must not be used to infer that a private skill is missing; use `restore` or an explicit link check for that.

## Choose The Workflow

- Inventory or classification: run `scan`; consult [classification.md](references/classification.md).
- First managed machine: follow [github-onboarding.md](references/github-onboarding.md), then preview and run `bootstrap`. It creates or verifies the private library and registers only the current machine.
- Another machine: preview and run `join`, then run `restore` separately. Each machine connects independently to GitHub; do not require machines to reach one another by SSH.
- Existing private backup without a machine registration: inspect it first. Use `connect` only to save an existing local connection without repository changes; otherwise preview `join` to add this machine to the private fleet inventory.
- Add a user-owned skill outside a managed target root: run `import` without `--apply`, show the destination, then apply. Run `sync` separately.
- Take over an existing personal skill in a managed target root: run `adopt` without `--apply`. It must preserve a local backup, verify the copied content, and create a link only after approval. Run `sync` separately.
- Track an open-source, marketplace, or plugin skill: confirm its canonical public source, then preview and run `track-source`. Never copy it into the private `skills/` directory.
- Reconcile source-managed skills: use the public-source status from `maintain`; compare the desired source, path, and ref with the current machine, then use the source's official installer or updater after preview and approval. The manager must report missing, duplicate, private-library-conflicting, source-mismatched, and locally unverifiable installations separately.
- Check backup and machine registration: use `maintain`, `status`, or `machine-status`; translate Git output into ordinary language.
- Publish private changes: after `status` finds local or remote pending changes, automatically run `sync` without `--apply`, review the file list and fast-forward plan, and apply only after explicit approval. After every approved `sync --apply`, run `restore` without `--apply` and show the managed-link preview before asking for separate approval.
- Install private skills: use `restore` to link skills from the private library into the registered target root. Never use a public skill installer for a skill already present in the private library. If a name appears in both the private library and source inventory, stop and report the ownership conflict before installing or restoring it.
- Restore a machine: run `restore` without `--apply`, verify every target, then apply. Reconcile every source-managed skill separately through its official source.
- Diagnose failure: run `doctor`; ask the user only for browser login, MFA, or permission approval that the Agent cannot complete.
- Update this manager: run `manager-status`, then preview and run `update-manager` only when the state is `update-available`. Do not invoke private-library synchronization as part of the update.

## Multi-Machine Model

GitHub is the shared hub, not a remote-control channel. The private library contains personal skills, the portable public-source inventory, and an optional `fleet.json` with only machine UUIDs, safe labels, roles, and enabled state. Each machine keeps its own checkout path, skill target, credentials, and local state.

On a new machine, the Agent must create a new random machine UUID and register it through `join`; never infer identity from a hostname, IP address, or path. When previewing a new UUID, carry that reviewed UUID into the approved apply command. If local identity is missing, incomplete, duplicated, or absent from `fleet.json`, stop before adoption or treating the machine as registered, then explain how to register or repair it.

Do not claim that a local check knows the live state of another machine. Without a direct connection or an explicitly configured reporting channel, a machine can only reconcile its own state when its Agent is invoked. `fleet.json` records desired machine identity; it is not a scheduler or remote-control channel.

## Suggest Reusable Skill Capture Or Update

When the current task produces a clearly reusable, user-owned workflow:

1. Compare it with existing personal skills.
2. If it adds durable value to an existing skill, offer once to update that skill. Otherwise, offer once to create a new skill.
3. Keep the prompt short: name the reusable value and ask whether to prepare a sanitized preview.
4. Do not create, update, import, or synchronize anything until the user agrees.
5. After agreement, use an appropriate skill-authoring workflow, remove machine-specific or sensitive details, and show the proposed content.
6. Import and synchronize only after separate approval.

Do not suggest capture for trivial one-off work, third-party instructions, or content whose main value depends on credentials, private identifiers, or confidential data.

## Non-Negotiable Safety Rules

Read [safety.md](references/safety.md) before any setup, bootstrap, join, adopt, import, sync, or restore operation.

- Keep preview mode as the default and require explicit `--apply` for mutation.
- Verify the backup repository is private through GitHub and its local checkout points to that exact repository before copying, registering, restoring, or pushing private-library content.
- Let `gh` or the operating system credential manager own authentication. Never store tokens in project files, `fleet.json`, or state JSON.
- Treat only user-authored skills as private-backup candidates. Track third-party, bundled, marketplace, and plugin skills by canonical source and reinstall or update them through their official mechanism.
- Never store executable installation commands, credentials, connection details, or machine-local paths in the portable source inventory or fleet inventory.
- Stop on secret-scan findings, existing restore targets, duplicate fleet identity, non-fast-forward history, conflicts, or staged paths outside `library.json`, `fleet.json`, and `skills/`.
- `adopt` must preserve a backup and must never delete or overwrite a skill.
- Never run `git add -A`, force-push, rewrite history, silently resolve conflicts, or delete/overwrite a skill.
- Update this public manager only by fast-forward. Stop on a dirty worktree, local-ahead history, divergence, or detached HEAD.
- After private-library synchronization, inspect managed links. Missing, broken, wrong, or occupied targets require a restore preview; never silently create, replace, or remove a target.
- Do not use ignored directories as private storage. Ignored files do not synchronize and can be removed by cleanup commands such as `git clean -xfd`.

## Session Integration

`maintain` is the portable session entry point. Codex can implicitly invoke this skill when it is installed in the active skill root. `install-manager` creates that managed link with preview and approval. Other Agents need a local session hook, startup instruction, or equivalent integration that invokes `maintain`; this repository cannot modify an unknown Agent's global configuration. A machine that is offline or has no Agent session cannot be actively reconciled without a separately configured scheduler or reporting channel.

For the integration contract and independent-machine boundary, read [session-integration.md](references/session-integration.md).

## Support Boundary

Automatic discovery is Codex-first and also checks common shared skill locations. `maintain` is read-only; it proposes manager update, private sync, restore, public-source reconciliation, and capture actions but never applies them. Manager update checks run when invoked, not as a background daemon. Personal skills synchronize as private content; open-source skills synchronize as a portable desired-source inventory and are reconciled on each machine through their official installer. Other Agents can use this repository with filesystem, Git, GitHub, and network access, but automatic invocation, source installation, and symlink support differ by platform.
