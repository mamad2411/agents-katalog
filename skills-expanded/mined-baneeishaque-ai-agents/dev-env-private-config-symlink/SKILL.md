---
name: dev-env-private-config-symlink
description: Industrial protocol for symlinking developer-private configuration files (.env, JSON, HTTP-client envs) from a sibling <private-repo> repository into an application's working directory across multiple environments (Gitpod, Google Cloud Shell, NeverInstall, Ubuntu, macOS, Windows), with broken-target detection, case-mismatch diagnosis, and per-consumer audit.
category: Developer-Environment
---

# Dev-Environment Private Config Symlink Protocol

This skill captures the cross-environment pattern of holding developer-private
configuration (`.env`, runtime JSON, HTTP-client environments, etc.) in a
single private companion repository (`<private-repo>`) and projecting it into
an application's working tree via **symbolic links**.

The protocol covers:

1. **Bootstrap**: clone or pull the private companion repo to the correct
   absolute root for the current host environment.
2. **Link**: create symlinks from the app's working tree to the private
   files.
3. **Diagnose**: detect broken targets, case-mismatched filesystems
    (macOS case-mismatch), and stale links after host migration.
4. **Audit**: confirm every linked file is actually consumed by source code
   somewhere (Kotlin / Java / Dart / JS / TS / Python), and flag dead
   config so symlink overhead is justified.

***

## 1. Vocabulary & Canonical Paths

| Token | Meaning |
|---|---|
| `<app-repo>` | The application repository receiving the symlinks (e.g., a Kotlin CLI, Flutter desktop app, Android client). |
| `<private-repo>` | The git repository holding developer-private configs. |
| `<private-root>` | The absolute path to `<private-repo>` on the current host (varies by environment — see §2). |
| `<app-subdir>` | A subfolder inside `<private-repo>` scoping configs to one application (e.g., `AccountLedger`). |
| `<consumer>` | Any source file (Kotlin / Java / Dart / JS / Python / etc.) that reads one of the linked configs. |

## 2. Per-Environment `<private-root>` Resolution

Each host environment has its own canonical root. The matrix below is the
reference for new environments:

| Environment | `<private-root>` | Exemplar |
|---|---|---|
| Gitpod | `/workspace/<private-repo>` | [scripts/exemplars/symlink-gitpod.bash](scripts/exemplars/symlink-gitpod.bash) |
| Google Cloud Shell | `~/cloudshell_open/<private-repo>` | [scripts/exemplars/symlink-google-cloud-shell.bash](scripts/exemplars/symlink-google-cloud-shell.bash) |
| NeverInstall | `../<private-repo>` (sibling of `<app-repo>`) | [scripts/exemplars/symlink-neverinstall.bash](scripts/exemplars/symlink-neverinstall.bash) |
| Ubuntu (local) | `$HOME/<private-repo>` | [scripts/exemplars/symlink-ubuntu.bash](scripts/exemplars/symlink-ubuntu.bash) |
| macOS (local) | `~/<data-dir>/<private-repo>` (case-sensitive on the literal path) | (see §3 — case-mismatch caution) |
| Windows | `C:\<data-dir>\<private-repo>` | [scripts/exemplars/symlink-windows.ps1](scripts/exemplars/symlink-windows.ps1) |

New environments MUST add a row above and a matching exemplar script.

## 3. Case-Mismatch Diagnosis (macOS / Windows Pitfall)

On case-insensitive filesystems (default APFS, NTFS) a symlink whose target
spells the path with the wrong case (e.g., `~/<data-dir>/...` instead of `~/<Data-Dir>/...`) **resolves successfully at the shell** but
the resolved real path may differ from what later tooling expects. The
classic failure mode: a symlink created on a peer host with one case
convention is checked in or scripted, then breaks (or silently aliases the
wrong directory) when the project is moved to a peer with a different case
convention.

**Detection**: walk every link target, run `readlink -f` (or `Get-Item`
`.Target`), and compare the resolved path's case against the on-disk case
of every segment. Any mismatch is a defect even when the symlink resolves.

**Remediation**: delete the link and recreate with the on-disk-correct case.
Never rely on case-insensitive filesystem leniency — peers on case-sensitive
filesystems (Linux ext4, native git server) will fail outright.

## 4. Operational Logic

### 4.1 Phase 1 — Discover Configs

1. Inventory the application's working tree for symlinks pointing into a
   path containing `<private-repo>` (or whatever the project's
   private-repo convention is named).
2. For each, capture: link path, target path (raw + resolved), target
   exists?, target case matches on-disk?
3. Inventory bash / PowerShell setup scripts at the repo root for additional
   files declared but not currently linked (script-declared but
   working-tree-absent).

### 4.2 Phase 2 — Locate / Bootstrap `<private-root>`

1. Resolve `<private-root>` per the current host environment (§2 matrix).
2. If absent, clone from the canonical VCS URL.
3. If present, `git -C <private-root> pull` to get latest changes.

### 4.3 Phase 3 — Create / Repair Links

For each declared `(link, target)` pair:

1. If the link exists and resolves and the target case matches: leave alone.
2. If the link exists but the target is missing or case-mismatched:
   `rm` the link and recreate.
3. If the link is absent: create.
4. Always use the **absolute** target path resolved per §2.

### 4.4 Phase 4 — Verify Resolution

After all links are (re)created, walk each and confirm:

- `test -e <link>` succeeds.
- `readlink -f <link>` (or PowerShell equivalent) resolves to a real file.
- For text configs, the first line is readable and looks well-formed
  (e.g., `.env` has `KEY=VALUE` shape; `*.json` parses).

### 4.5 Phase 5 — Audit Consumer Coverage

For every linked file, search the application's source code (and any
sibling repos in the same workspace) for textual references to the
basename:

```bash
grep -rln --include="*.kt" --include="*.java" --include="*.dart" \
          --include="*.js" --include="*.ts" --include="*.py" \
  "<config-basename>" .
```

Cross-reference the consumer map against the link inventory. Three
outcomes:

- **Consumed locally**: at least one source file in the current app reads
  the config — link is justified.
- **Consumed elsewhere**: only sibling repos / other-language apps consume
  the config. Decide whether to keep the link for parity or drop it for
  the current app.
- **Orphan**: no consumer anywhere — flag as dead config, propose removal
  in coordination with the user.

Real example from the source session: `relationOfAccounts.json` was linked
in the Kotlin CLI but had **zero** Kotlin / Java consumers — it is in fact
read only by the Dart Flutter sibling apps. Without this audit the link
would silently rot.

### 4.6 Phase 6 — Round-Trip Upload (Optional)

When the developer edits a private config in place (via the link), the
private repo's working tree is mutated. A companion `upload` script
commits and pushes those changes back. See
[scripts/exemplars/upload-changes-gitpod.bash](scripts/exemplars/upload-changes-gitpod.bash).

***

## 5. Cross-Repo Reference Integrity

When a config file is consumed by **multiple** sibling repos (a common
multi-platform pattern: Kotlin CLI + Android client + Dart Flutter
desktop + Dart Flutter Windows), the symlink-setup scripts MUST be
mirrored in every repo, each pointing to the same `<private-root>`. A
change to the schema of any config requires a coordinated update across
every consumer.

The audit step (§4.5) is the canonical way to discover which sibling
repos consume which config — never rely on memory or naming conventions.

***

## 6. Exemplar Scripts (Shipped)

| Script | Environment | Style |
|---|---|---|
| [scripts/exemplars/symlink-gitpod.bash](scripts/exemplars/symlink-gitpod.bash) | Gitpod | clone-or-pull then `rm` + `ln -s` chain |
| [scripts/exemplars/symlink-google-cloud-shell.bash](scripts/exemplars/symlink-google-cloud-shell.bash) | Google Cloud Shell | one-shot `cd && clone && ln -s` |
| [scripts/exemplars/symlink-neverinstall.bash](scripts/exemplars/symlink-neverinstall.bash) | NeverInstall | sibling-relative `../` paths |
| [scripts/exemplars/symlink-ubuntu.bash](scripts/exemplars/symlink-ubuntu.bash) | Ubuntu (local) | `$HOME`-anchored |
| [scripts/exemplars/symlink-windows.ps1](scripts/exemplars/symlink-windows.ps1) | Windows | PowerShell with package-manager bootstrap (`scoop` / `choco` / `winget`) |
| [scripts/exemplars/upload-changes-gitpod.bash](scripts/exemplars/upload-changes-gitpod.bash) | Gitpod | round-trip commit + push of edited configs |

These scripts are preserved verbatim as **canonical references**. They
encode environment-specific knowledge (e.g., the exact Gitpod
`/workspace/` root, the Cloud Shell `~/cloudshell_open/` root, the
Windows `C:\<data-dir>\` root) that would be lost if reduced to a generic
template.

## 7. Automated Audit Script

[scripts/audit-symlinks.py](scripts/audit-symlinks.py) walks the current
working directory for symlinks pointing at any path containing
`<private-repo>` (configurable), and reports per link:

- target absolute path
- target exists?
- on-disk path case matches?
- consumer hit count across `*.kt`, `*.java`, `*.dart`, `*.js`, `*.ts`,
  `*.py`

Exit code 0 if every link resolves; exit code 1 if any link is broken
or any linked file has zero consumers.

## 8. SSOT Compliance & Cross-References

- Path / identity redaction policy: defer to
  [`redaction-portability`](../redaction-portability/SKILL.md).
- Markdown lint standard: defer to
  [`markdown-generation`](../markdown-generation/SKILL.md) + project rules.
- Atomic-commit discipline for symlink-related changes: delegate to
  [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
  — symlink additions and the consumer code that uses them should be in
  the same atomic commit (Configuration Coupling rule).

## 9. Prohibited Behaviors

The agent is **BLOCKED** from:

- Silently fixing a broken symlink without first confirming whether the
  target file is supposed to exist (§4.5 — orphan vs missing).
- Committing `.env` or any other private file to the public application
  repo. The link's target MUST live in the private companion repo only.
- Generating a symlink with a hard-coded path that does not match §2's
  per-environment matrix.
- Removing a config link without running the consumer audit (§4.5) to
  identify which repos break.

## 10. Composition Rationale

This skill is **atomic**: it does not split into base + composer because
the operational steps (clone / pull / symlink / verify) are tightly
sequenced. The `audit-symlinks.py` script is a self-contained utility
not used by other skills.

## 11. Related Skills

- [`tool-config-directory-symlink`](../tool-config-directory-symlink/SKILL.md) — Base skill for migrating entire tool configuration directories (XDG) into a companion repo with symlinks. This skill focuses on individual app-level config files (`.env`, JSON); the base skill generalises directory-level migration for tool configs.
- [`opencode-config-preserve`](../opencode-config-preserve/SKILL.md) — Analogous config preservation protocol
  for OpenCode CLI/IDE XDG directories, with selective gitignore tracking and recovery-value assessment.

## 12. Traceability

This skill was extracted from a session that:

- Detected broken `.env` and `frequencyOfAccounts.json` symlinks in a
  Kotlin CLI repo (targets with a case-mismatch).
- Repaired both with case-correct absolute targets.
- Audited `relationOfAccounts.json` and found zero Kotlin/Java consumers
  — discovered it is exclusively Dart-side, used by two Flutter desktop
  apps.
