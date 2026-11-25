---
name: git-lfs-selective-clone
description: Industrial protocol for cloning a Git LFS repository (and its
    submodules) without downloading any LFS blobs, then selectively pulling
    only the LFS objects the user actually needs via include/exclude globs.
category: Git & Repository Management
---

# Git LFS Selective Clone Skill

> **Skill ID:** `git-lfs-selective-clone`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Clone a Git LFS repository while skipping **all** LFS blob downloads, then
materialize only the LFS objects the user asks for. The skill covers:

1. **Bullet-proof skip** of LFS at clone time — defeating the silent
   `filter.lfs.process` long-running filter that bypasses
   `GIT_LFS_SKIP_SMUDGE` and `filter.lfs.smudge` alone.
2. **Verification** that LFS was *actually* skipped (pointer files are
   ~130 B; real blobs are MB–GB).
3. **Recursive submodule initialization** under the same skip regime —
   submodules that ship LFS objects must inherit the skip, otherwise the
   first `submodule update --init` silently pulls gigabytes.
4. **Selective post-clone pull** via `git lfs pull --include / --exclude`
   with brace-list globs, applied per-repo and per-submodule.

The clone history, tree contents, and pointer files are preserved
bit-for-bit; only the LFS object cache (`.git/lfs/objects/`) is left
empty until the user opts in to specific files.

## Source Conversations

| Date | Topic |
|---|---|
| 2026-05-12 | Selective LFS clone of a large LFS repo on Windows / PowerShell — diagnosed `GIT_LFS_SKIP_SMUDGE` failure on PowerShell `set`, identified the `filter.lfs.process` bypass, and built the three-filter override + per-path `git lfs pull` flow |

***

## 1. Environment & Dependencies

The agent MUST verify the following before executing this skill:

| Requirement | Minimum | Verification |
|---|---|---|
| Git | 2.20+ (long-running filter protocol stable) | `git --version` |
| Git LFS | 2.5+ (supports `filter.lfs.process`) | `git lfs version` |
| Shell | Windows PowerShell 5.1+ / PowerShell Core 7+ / Bash 4+ / Zsh | `$PSVersionTable.PSVersion` or `bash --version` |
| Network | Reachability to the host (e.g., `github.com`, internal `<internal-vcs>`) | `git ls-remote <url>` |

If `git lfs` is missing, install per the standard package manager:

```bash
# macOS
brew install git-lfs

# Debian / Ubuntu
sudo apt-get install -y git-lfs

# RHEL / Fedora
sudo yum install -y git-lfs

# Windows (winget / choco)
winget install Git.GitLFS
```

After install, run `git lfs install` **once per user** to register the
default filter hooks (does **not** force LFS on every repo — it is a
prerequisite for the filter overrides below to take effect).

***

## 2. When to Apply

Apply this skill when:

- The user asks to clone an LFS repository **without** the LFS blobs.
- The user complains the clone "hangs" or downloads many GB unexpectedly
  on a repo that has `.gitattributes` declaring `filter=lfs`.
- The user wants a subset of LFS files materialized (e.g., one `.zip`
  but not the 5 GB of `.mp4` companions).
- The repo contains submodules that themselves ship LFS objects and the
  user wants those submodules initialized **without** their LFS payload.

Do **NOT** apply when:

- The user wants the **full** LFS payload — use a plain
  `git clone --recurse-submodules <url>` instead.
- The user wants a shallow clone (`--depth=1`) primarily — that is a
  different size-control axis; the two can be combined but the shallow
  protocol is out of scope here.
- The repository has no `.gitattributes` `filter=lfs` entries — there
  are no LFS pointers to skip; a normal clone is sufficient.

***

## 3. Step-by-Step Procedure

### Step 0 — Pre-Flight Inspection

Confirm the target repo actually uses LFS before applying the overrides
(over-engineering a non-LFS clone is a "Greater-Than-Before" violation —
do not add ceremony where none is needed).

#### 0a — Probe `.gitattributes` Remotely (no clone yet)

```bash
git ls-remote --heads <repo-url>           # confirms reachability + auth
git archive --remote=<repo-url> HEAD .gitattributes 2>/dev/null | tar -xO
```

The agent MAY skip Step 0a if the user has already confirmed the repo
uses LFS. If `.gitattributes` shows `filter=lfs diff=lfs merge=lfs`
entries (typical pattern: `*.zip filter=lfs ...`), proceed.

#### 0b — Pick a Local Destination

Default per the
[Git Repository Management Rules §2](../../../ai-agent-rules/git-repo-management-rules.md#2-high-fidelity-cloning-protocol):
`~/sample/path/<repo-name>/` (or `~/<data-dir>/<repo-name>/` per
[Repo Discovery Rules](../../../ai-agent-rules/repo-discovery-rules.md)).
The agent MUST confirm the destination is empty.

***

### Step 1 — Clone Without LFS Blobs (Three-Filter Override)

This is the **only** clone form the agent MUST use for an LFS-skip
workflow. Single-flag attempts (env var alone, or
`filter.lfs.smudge=` alone) silently fail because modern Git LFS
installs a **long-running `process` filter** that bypasses the smudge
hook.

#### 1a — Canonical Command

POSIX (Bash / Zsh / Git Bash):

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone \
    -c filter.lfs.smudge= \
    -c filter.lfs.process= \
    -c filter.lfs.required=false \
    --recurse-submodules=no \
    --progress \
    <repo-url> <dest>
```

PowerShell (5.1+ / Core 7+):

```powershell
$env:GIT_LFS_SKIP_SMUDGE = "1"
git clone `
    -c filter.lfs.smudge= `
    -c filter.lfs.process= `
    -c filter.lfs.required=false `
    --recurse-submodules=no `
    --progress `
    <repo-url> <dest>
```

Windows CMD:

```cmd
set GIT_LFS_SKIP_SMUDGE=1
git clone -c filter.lfs.smudge= -c filter.lfs.process= -c filter.lfs.required=false --recurse-submodules=no --progress <repo-url> <dest>
```

> [!IMPORTANT]
> Submodules are handled **separately** in Step 3 under the same skip
> regime. Passing `--recurse-submodules` here would clone submodules
> with the **default** filter set and silently download their LFS
> blobs. The agent MUST use `--recurse-submodules=no` (or omit it; it
> is the default) and run Step 3 explicitly afterwards.

#### 1b — Deep Command Explanation (Pedagogical)

Per the Deep Command Explanation Mandate, every flag is justified
below:

- **`GIT_LFS_SKIP_SMUDGE=1`** — Tells the `git-lfs smudge` driver to
  emit the **pointer text** instead of fetching the blob when Git
  asks it to materialize a file during checkout. Necessary but
  **not sufficient** on its own — modern installs use the
  long-running `process` filter (added in Git LFS 2.2) which is a
  separate code path and ignores this env var on some builds /
  versions.
- **`-c filter.lfs.smudge=`** — Sets the smudge command to the
  empty string. When the smudge command is empty, Git skips the
  smudge step entirely and writes the pointer to the working tree
  as-is. This belt-and-suspenders the `GIT_LFS_SKIP_SMUDGE` env var.
  **Note:** `git clone -c` is **persisted** into the new repo's
  `.git/config` (it is NOT one-shot); the same applies to the two
  `-c` flags below. This is the desired state during clone but
  imposes a mandatory restoration step before any later
  `git lfs pull` — see §4d and §7.
- **`-c filter.lfs.process=`** — The critical override. Setting
  the `process` filter to empty disables the long-running filter
  protocol entirely for this clone. Without this, Git LFS streams
  every LFS blob during checkout regardless of the smudge override.
  **This is the single flag most "skip LFS" instructions on the
  internet omit, and it is the most common reason a "skipped" clone
  still downloads gigabytes.**
- **`-c filter.lfs.required=false`** — Tells Git not to fail the
  checkout if the LFS filters are absent / empty / non-functional.
  Without this, the empty filters above can cause `error: external
  filter '...' failed` at checkout time and abort the clone with a
  half-populated working tree.
- **`--recurse-submodules=no`** — Explicit opt-out of submodule
  recursion at clone time so the LFS-skip regime is not bypassed by
  the submodule clones. Step 3 reapplies the same overrides for
  submodules.
- **`--progress`** — Forces progress output to stderr even when the
  output is not a terminal (e.g., when redirected to a log file or
  piped through `Start-Process`). Critical for diagnosing hangs.

#### 1c — PowerShell Pitfall: `set` Is Not `$env:`

A frequent failure mode on Windows:

```powershell
# WRONG — `set` is an alias for `Set-Variable` in PowerShell.
# Creates a PowerShell variable that child `git.exe` cannot read.
set GIT_LFS_SKIP_SMUDGE=1

# CORRECT — exports a process-environment variable.
$env:GIT_LFS_SKIP_SMUDGE = "1"
```

The agent MUST detect the active shell (`$PSVersionTable.PSVersion`
present → PowerShell; otherwise CMD/POSIX) and emit the correct
syntax.

***

### Step 2 — Verify LFS Was Actually Skipped

The agent MUST run all three verifications before declaring success.
A "clone completed without errors" message is **not** evidence that
LFS was skipped — corrupted skips silently download everything.

```bash
cd <dest>

# (a) Total working-tree size (should be tiny relative to known LFS payload)
du -sh .   # POSIX
```

```powershell
# (a-pwsh) PowerShell equivalent
(Get-ChildItem -Recurse -Force | Measure-Object Length -Sum).Sum / 1MB
```

```bash
# (b) LFS object inventory — the marker column MUST be `-` (dash), NOT `*`
#     `-` = pointer only (blob NOT in local cache)
#     `*` = blob downloaded into .git/lfs/objects/
git lfs ls-files
```

```bash
# (c) Spot-check one known LFS file — MUST be ~130 B and start with
#     "version https://git-lfs.github.com/spec/v1"
head -3 <one-lfs-tracked-file>
```

```powershell
# (c-pwsh) PowerShell equivalent
Get-Content <one-lfs-tracked-file> -TotalCount 3
```

If any check fails (size matches the real blob, `*` markers in
`ls-files`, or binary content instead of `version https://...`), the
agent MUST:

1. Kill any running `git` / `git-lfs` processes.
2. Delete the destination directory.
3. Retry Step 1 — most commonly the `filter.lfs.process=` override
   was forgotten.

***

### Step 3 — Initialize Submodules Without LFS (Recursive)

Per the Recursive Submodule Mandate (defined in
[AI Rule Standardization Rules §4](../../../ai-agent-rules/ai-rule-standardization-rules.md#4-content-philosophy-ultra-lean-industrial))
all submodule operations MUST use the recursive form so nested LFS
submodules also inherit the skip.

```bash
cd <dest>
GIT_LFS_SKIP_SMUDGE=1 git \
    -c filter.lfs.smudge= \
    -c filter.lfs.process= \
    -c filter.lfs.required=false \
    submodule update --init --recursive --progress
```

```powershell
$env:GIT_LFS_SKIP_SMUDGE = "1"
git -c filter.lfs.smudge= -c filter.lfs.process= -c filter.lfs.required=false `
    submodule update --init --recursive --progress
```

**Pedagogical breakdown:**

- The same three `-c` overrides MUST be re-supplied here. Git
  configuration is **per-repo**, not inherited across the
  submodule boundary. A submodule clones into `.git/modules/<name>/`
  using its **own** default filter set, so without these overrides
  it would silently pull every LFS blob it ships.
- `--init` creates the working tree for each registered submodule.
- `--recursive` descends into nested submodules so any deeper LFS
  pointers also stay as pointers.
- `--progress` again surfaces progress to stderr — important for
  diagnosing hangs in the submodule phase.

After this step, re-run Step 2's verifications **inside each
submodule directory** (`git lfs ls-files` should show `-` markers).

#### 3a — Pre-Check: `submodule.active` Must Not Be `no`

A `submodule.active` value of `no` (or any pathspec that excludes the
registered submodule) causes `git submodule update --init --recursive`
to **silently no-op** — zero output, exit code 0, no clone, no error.
This setting can be inherited from `~/.gitconfig` or a system-wide
config and is also written by some VS Code / IDE workflows.

The agent MUST inspect the effective value **before** running Step 3:

```bash
git config --get submodule.active   # empty or matching pathspec → OK
```

If the value is `no`, or absent and the user's global config sets it
to `no`, override it locally before re-running Step 3:

```bash
git config --local submodule.active "."
```

The `.` pathspec means "all submodules are active" and is the safest
local override. It is written to `.git/config` and persists for
subsequent `submodule update` calls in this clone only.

#### 3b — Per-path Init Alternative (Subset Only)

When the caller wants only ONE or a few submodules initialized — not the
entire transitive set — do NOT use the `--recursive` command above. Defer
to the atomic skill:

- [`git-submodule-selective-init-no-lfs`](../git-submodule-selective-init-no-lfs/SKILL.md)
  — initializes exactly the named paths AND guarantees no LFS objects are
  fetched (`GIT_LFS_SKIP_SMUDGE=1` PLUS
  `-c filter.lfs.smudge= -c filter.lfs.process= -c filter.lfs.required=false`,
  since the env var alone is insufficient when the submodule's own
  `.gitattributes` declares LFS filters). Post-state asserts both: no `-`
  prefix in `git submodule status`, AND `.git/modules/<path>/lfs/objects`
  empty/absent.

This deferral is the canonical "narrow scope" branch out of Step 3 — the
full-recursive command above remains correct when ALL submodules are
wanted.

***

***

### Step 4 — Selective LFS Pull (Include / Exclude Globs)

Once the skeleton is in place, the agent materializes only the LFS
objects the user actually requested.

#### 4a — Locate the LFS Tracking Inventory

```bash
git lfs ls-files
```

This is the canonical surface of LFS-tracked paths. The agent MUST
use these literal paths (or globs over them) — guessing at extensions
is forbidden because a repo can track arbitrary patterns via
`.gitattributes`.

> [!NOTE]
> `git lfs ls-files -- <subdir>` is **NOT** a supported pathspec
> filter — it interprets the argument as a revision and fails with
> `fatal: bad revision`. To restrict by directory, post-filter with
> `grep` / `Select-String` instead.

#### 4b — Pull Selected Files (Split Fetch + Checkout)

The `--include` and `--exclude` flags accept comma-separated brace-
glob lists, evaluated against the paths emitted by `git lfs ls-files`.

> [!IMPORTANT]
> **Do NOT use `git lfs pull` as a single command for agent-driven
> execution.** Empirically, `git lfs pull` can terminate after the
> fetch phase but before the checkout phase — the blob lands in
> `.git/lfs/objects/` but the working-tree pointer is never
> smudged into the real file. The agent MUST split the operation
> into explicit `git lfs fetch` + `git lfs checkout`:

```bash
# 1) Fetch the blob(s) into .git/lfs/objects/ (network step)
git lfs fetch --include="ats/*.zip,sample_ats/*.zip" origin <branch>

# 2) Smudge the cached blob(s) into the working tree (local step)
git lfs checkout ats/*.zip sample_ats/*.zip
```

PowerShell with `-C` (no `cd` required):

```powershell
git -C <dest> lfs fetch --include="<pattern>" origin <branch>
git -C <dest> lfs checkout <path1> <path2>
```

**Why split:**

- `git lfs fetch` is the network-bound step; failures (timeouts,
  auth, server errors) are clearly attributable.
- `git lfs checkout` is local-only and idempotent — it scans the
  working tree for pointer files whose OID is present in the cache
  and smudges them. If the first run terminated before checkout,
  re-running `git lfs checkout` materializes the cached blobs
  without re-downloading.
- After a `git lfs fetch`, `Get-ChildItem .git/lfs/objects` confirms
  the blob is present (size matches the pointer's `size` field).
  This is the authoritative "download succeeded" check, independent
  of whether the working tree was smudged.

**Pedagogical breakdown:**

- `git lfs fetch --include="<glob1>,<glob2>" origin <branch>`
  downloads only LFS objects referenced by `<branch>` whose paths
  match the include globs. **The trailing `origin <branch>`
  arguments are recommended** — without them, `git lfs fetch` may
  scan all refs and behave inconsistently across LFS versions.
- `git lfs checkout <paths...>` smudges the listed pointer files
  using the cached blob. Accepts shell globs (expanded by the shell
  before reaching `git lfs`); on PowerShell, multi-glob expansion
  may differ — prefer listing exact paths or invoking once per
  file.
- `--include="<glob1>,<glob2>"` — comma-separated, **no spaces**.
  Spaces around commas break the parser silently and you will pull
  everything. Globs are matched against repo-relative paths from
  `git lfs ls-files`.
- `--exclude="<glob>"` — applied AFTER `--include`. The
  evaluation order is: (include == empty OR matches include) AND
  NOT matches exclude. To fetch *everything except one file*, use
  `--include="*"` with `--exclude="<file>"`.
- Both `fetch` and `checkout` operate on the **current submodule
  scope only** — they do NOT recurse. Run each pair once per
  repository / submodule that contains files of interest.

**Single-command fallback:** `git lfs pull --include="<glob>"` is
acceptable for interactive (human-typed) one-off pulls where the
user can rerun `git lfs checkout` manually if needed. The split
form above is REQUIRED for agent execution and any scripted /
batched workflow.

#### 4c — Brace-Glob Compatibility

Some `git lfs` versions on Windows do not expand `{a,b}` brace
syntax. Prefer the comma-separated `--include` list (which is the
LFS-native multi-pattern syntax) over brace expansion to stay
portable.

#### 4d — Restore LFS Filters Before Pulling (Mandatory)

The Step 1 clone writes empty `filter.lfs.smudge` / `process` /
`required` into `<dest>/.git/config`. With these in place,
`git lfs pull` will fetch the blob into `.git/lfs/objects/` but the
checkout step will **not** materialize the working-tree file — the
pointer stays put and the file appears not to have downloaded. The
agent MUST restore the filters before any selective pull:

```bash
cd <dest>
git config --local --unset filter.lfs.smudge
git config --local --unset filter.lfs.process
git config --local --unset filter.lfs.required
git lfs install --local
```

See §7 for the full rationale.

#### 4e — PowerShell: Run LFS Pull/Fetch Without Pipes

On Windows PowerShell, piping `git lfs pull` / `git lfs fetch` into
`Select-Object`, `Tee-Object`, or any other cmdlet buffers the entire
stream until the process exits and **swallows the live progress
line** (which `git-lfs` updates in place via `\r`). The download is
proceeding normally — the user just cannot see it.

Correct invocation:

```powershell
cd <dest>
git lfs pull --include="<pattern>"            # foreground, live progress
```

For agent-driven execution, run as a backgrounded shell command and
tail with `await_terminal` so the in-place progress line surfaces in
the output stream.

***

### Step 5 — Final Audit

```bash
git lfs ls-files                # `*` for downloaded, `-` for pointer
du -sh .                        # POSIX
```

```powershell
(Get-ChildItem -Recurse -Force | Measure-Object Length -Sum).Sum / 1MB
```

Present a before / after table to the user:

| Item | Before pull | After pull |
|---|---|---|
| Total working-tree size | `<X> MB` | `<Y> MB` |
| LFS files downloaded | 0 | `<N>` of `<M>` |
| LFS files still pointer-only | `<M>` | `<M-N>` |

The agent MUST flag any LFS file the user did **not** request that
nevertheless flipped from `-` to `*` — that indicates the
`--include` / `--exclude` glob matched too broadly and the cache
ate disk the user did not authorize.

***

## 4. Scope Coverage

| Concern | Convention |
|---|---|
| Clone-time blob skip | `GIT_LFS_SKIP_SMUDGE=1` **AND** `-c filter.lfs.smudge=` **AND** `-c filter.lfs.process=` **AND** `-c filter.lfs.required=false` |
| Submodule init | Same four overrides on `git submodule update --init --recursive` |
| Selective pull | Split: `git lfs fetch --include="<csv-globs>" origin <branch>` then `git lfs checkout <paths>` (single `git lfs pull` may exit after fetch without smudging) |
| Verification | `git lfs ls-files` marker column + per-file pointer header check |
| Shell portability | Detect PowerShell vs CMD vs POSIX and emit matching env-var syntax |
| Submodule recursion | `--recursive` mandatory (Recursive Submodule Mandate) |

***

## 5. Prohibited Behaviors

The agent is **BLOCKED** from:

- **Relying on `GIT_LFS_SKIP_SMUDGE` alone.** The `filter.lfs.process`
  override is mandatory; without it, LFS streams every blob through
  the long-running filter regardless of the env var.
- **Using PowerShell `set FOO=1` to export an env var.** That is an
  alias for `Set-Variable` and the child `git.exe` will not see it.
  Use `$env:FOO = "1"`.
- **Cloning with `--recurse-submodules`** in this workflow without
  re-supplying the four overrides on the recursive command path.
  Submodule defaults will silently fetch all LFS objects.
- **Declaring success based on "clone completed" alone.** Step 2
  verification (`ls-files` markers + pointer-file header check) is
  mandatory.
- **Spaces around commas in `--include` / `--exclude` lists.**
  `"a.zip, b.zip"` matches only `a.zip` and the literal pattern
  ` b.zip` (with leading space) — silently wrong.
- **Pulling LFS with `--include="*"` without a matching
  `--exclude`** when the user asked for "everything except X". The
  agent MUST surface the explicit exclude.
- **Using `git lfs ls-files -- <subdir>`** as a pathspec filter — it
  is interpreted as a revision and fails. Use `grep` / `Select-String`
  on the full listing instead.
- **Trusting a silent `git submodule update --init` exit-0** as
  evidence the submodule was cloned. If `submodule.active=no` is in
  effect (locally, globally, or system-wide), the command no-ops
  silently. Always verify with `git submodule status --recursive` —
  a leading `-` on every line means uninitialized.
- **Running `git lfs pull` / `git lfs fetch` through a PowerShell
  pipe** like `| Select-Object -Last N` or `| Tee-Object`. These
  buffer the entire stream until process exit and swallow the
  `\r`-overwritten progress line, making a perfectly healthy multi-
  gigabyte download look like a hang. Always run LFS pull/fetch in
  the foreground without pipes, or background with live progress
  via `await_terminal`.
- **Assuming `git clone -c filter.lfs.* =` is one-shot.** It is
  persisted into the cloned repo's `.git/config`. The agent MUST run
  the §7a restoration before any `git lfs pull` / `fetch` /
  `checkout`, or files will be fetched to cache but the pointer will
  remain in the working tree.
- **Using `git lfs pull` as a single command in agent-driven
  execution.** Empirically, `git lfs pull` can return success after
  the fetch phase without smudging the working-tree pointer, leaving
  the user with a cached blob and a 130-byte pointer file. Always
  split into explicit `git lfs fetch` (network) + `git lfs checkout`
  (local smudge); see §4b.

***

## 6. Common Pitfalls

| Pitfall | Solution |
|---|---|
| `set GIT_LFS_SKIP_SMUDGE=1` in PowerShell silently no-ops | Use `$env:GIT_LFS_SKIP_SMUDGE = "1"` |
| `-c filter.lfs.smudge=` alone still downloads blobs | Add `-c filter.lfs.process=` — the long-running filter is a separate code path |
| `error: external filter 'git-lfs filter-process' failed` at checkout | Add `-c filter.lfs.required=false` so empty filters are non-fatal |
| Submodule init pulls gigabytes despite parent skipping LFS | Re-supply the four overrides on `git submodule update --init --recursive` — submodules don't inherit parent's per-command `-c` config |
| `git submodule update --init --recursive` silently no-ops (exit 0, zero output, no clone) | Inherited `submodule.active = no` in global/system config. Run `git config --local submodule.active "."` then retry. Verify with `git submodule status --recursive` |
| Brace glob `{a,b}.zip` doesn't expand on Windows `git lfs` | Use comma-separated `--include="a.zip,b.zip"` (LFS-native syntax) |
| `git lfs ls-files -- ats` → `fatal: bad revision 'ats'` | `ls-files` doesn't accept pathspecs; post-filter with `grep ^.*\bats/` |
| Pointer files look like binary in `cat` output | They start with `version https://git-lfs.github.com/spec/v1` and are ~130 B; check with `head -3` not `file` |
| `git clone` "hangs" with no progress | `--progress` not passed; or LFS download is in progress (size grows). Inspect the destination tree size to disambiguate |
| Clone succeeded but later `git pull` re-pulls everything | The Step 1 `-c` overrides ARE persisted into `.git/config` (despite older docs claiming otherwise). See §7 for the explicit restoration sequence |
| `git lfs pull` reports success but working-tree file stays a 130-byte pointer | Empty `filter.lfs.smudge` in `.git/config` (left by Step 1). Run the §7a restoration (`--unset` the three filters + `git lfs install --local`) before pulling |
| PowerShell `git lfs fetch ... \| Select-Object -Last N` shows zero output then exits | PowerShell pipes buffer the entire stream and swallow `\r`-overwritten progress lines. Run `git lfs fetch / pull` **without any pipe** in the foreground, or background it via `run_in_terminal` with `isBackground=true` and tail via `await_terminal` — then progress streams live |
| `git lfs pull` returns success but file stays a 130-byte pointer (cache contains the blob) | `git lfs pull` exited after fetch without running checkout. Run `git lfs checkout <path>` to smudge the cached blob into the working tree. For future pulls, use the split fetch+checkout pattern from §4b |

***

## 7. Persistent vs One-Shot Skip

**Critical correction:** `git clone -c <key>=<value>` is **NOT**
one-shot. Every `-c` pair passed to `git clone` is **persisted** into
the new repo's `.git/config` exactly as if you had run
`git config --local <key> <value>` after the clone. The Step 1
command therefore writes the four overrides into the local config of
the cloned repo:

```ini
[filter "lfs"]
        smudge =
        process =
        required = false
```

This is the **desired** state during clone (skips LFS blob download)
but it has a consequential side effect: every subsequent `git lfs
pull` / `git lfs fetch` / `git checkout` in this repo **also** runs
with empty LFS filters. The fetch step still populates
`.git/lfs/objects/` (it does not use the smudge filter), but the
checkout step that should replace the pointer file with the real blob
invokes `filter.lfs.smudge` — and finding it empty, leaves the
pointer file in place. **The blob is downloaded into the cache but
never written to the working tree.** From the user's perspective it
looks like "the file did not download".

### 7a — Restoring LFS Filters After Selective Pull

Before any `git lfs pull` / `git lfs fetch` / `git lfs checkout` on a
repo cloned via Step 1, the agent MUST restore the LFS filters in the
local config so the smudge step can materialize blobs:

```bash
cd <dest>
git config --local --unset filter.lfs.smudge
git config --local --unset filter.lfs.process
git config --local --unset filter.lfs.required
git lfs install --local       # re-registers the standard filter set
```

The `--unset` commands remove the empty overrides so the global /
system defaults take effect; `git lfs install --local` then writes the
standard `git-lfs clean / smudge / filter-process` entries back into
the repo's `.git/config`. After this, `git lfs pull` works normally.

Repeat the same sequence inside every initialized submodule before
pulling LFS objects there.

### 7b — Keeping the Skip Permanent

If the user wants to keep the skip permanent on this clone (so future
`git pull` / `git checkout` operations never re-fetch LFS), do
**nothing** — the Step 1 clone already wrote the empty filters into
`.git/config`. The agent MUST then warn the user that any
`git lfs pull` will need the §7a restoration first to actually
materialize files.

The agent MUST ask the user which mode (post-clone restoration vs
permanent skip) they want **before** running any selective pull.

***

## 8. Related Skills

- [`git-repo-storage-minimization`](../git-repo-storage-minimization/SKILL.md) —
  complementary skill for shrinking `.git/` after LFS pointers are in
  place (deinit unused submodules, `gc --aggressive`).
- [`git-submodule-uninitialized-handler`](../git-submodule-uninitialized-handler/SKILL.md) —
  remediation for submodule pointers stuck in uninitialized state, can
  consume the output of this skill's Step 3 verification.
- [`git-github-auth-fallback`](../git-github-auth-fallback/SKILL.md) —
  if the clone in Step 1 fails with 401/403 before LFS even runs.
- [`git-submodule-selective-init-no-lfs`](../git-submodule-selective-init-no-lfs/SKILL.md)
  — atomic per-path, LFS-skipped peer to this skill's full-recursive
  Step 3. Reach for it when only a SUBSET of submodules is wanted while
  preserving the LFS-free property; see Step 3b above for the deferral
  point.

> **No higher-level composer skill currently consumes `git-lfs-selective-clone`
> directly.** If one is added later, declare it in a new
> `## Composition by Higher-Level Skills` section here.

## 9. Related Rules

- [Git Repository Management Rules §2 — High-Fidelity Cloning Protocol](../../../ai-agent-rules/git-repo-management-rules.md#2-high-fidelity-cloning-protocol)
- [Repo Discovery Rules — Cloning Workflow](../../../ai-agent-rules/repo-discovery-rules.md)
- [AI Rule Standardization Rules §4 — Recursive Submodule Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md#4-content-philosophy-ultra-lean-industrial)

***

## 10. Traceability

Source conversation logs MUST be sanitised via the
[Redaction & Portability Skill](../redaction-portability/SKILL.md)
before being committed under `ai-agent-rules/docs/conversations/`.
Specifically: internal LFS host names (e.g., `<internal-vcs>`), customer
product codenames embedded in LFS file names, and absolute Windows /
POSIX paths in shell transcripts MUST be replaced with the canonical
placeholder vocabulary before commit.
