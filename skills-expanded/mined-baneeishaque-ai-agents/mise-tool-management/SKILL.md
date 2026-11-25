---
name: mise-tool-management
description: Industrial protocols for mise configuration trust, tool version selection,
    and Python package setup. Use whenever a mise.toml is untrusted, a required tool
    is missing, or a Python package needs to be installed into a mise-managed environment.
category: Environment-Management
---

# Mise Tool Management Skill

This skill defines the **layered industrial protocol** for managing `mise`-based development
environments. Each layer is a strict prerequisite for the one above it.

```text
Layer 1: Mise Config Trust              (base — everything depends on this)
├── Layer 2: Mise Tool Selection        (works on top of Layer 1)
│   └── Layer 3: Mise Python Setup      (a specialisation of Layer 2 for Python)
│       └── Layer 4: Mise Python Package Setup  (works on top of Layer 3)
├── Layer 5: Bypass `mise exec` Cascade (alternative consumption path; sibling of Layer 2)
└── Layer 6: Deprecation Warning Handling & Backend Migration (cross-cuts Layers 1–5)
```

***

## 1. Layer 1 — Mise Configuration Trust Protocol

`mise` blocks any config file it does not explicitly trust. The agent MUST resolve this
before attempting any tool use.

### 1.1 Detection

Run the following command to detect whether any `mise` config in the working directory
is untrusted:

```bash
# Attempt to list tools — mise prints trust errors to stderr
mise ls 2>&1
```

- **Flag**: Output containing `Config files in ... are not trusted` signals an untrusted
  configuration.

### 1.2 Analysis & Presentation

When a trust error is detected, the agent MUST:

1. **Read** the untrusted `mise.toml` (or `.mise.toml`) file.
2. **Present** the full file content to the USER in a fenced code block.
3. **Analyse** each declared tool: what it is, what version is pinned, and why it exists.
4. **Recommend** explicitly (e.g. "This file only pins `python = "3.11"`. It does not
   run scripts and poses no security risk. I recommend trusting it.").

### 1.3 User Decision Gate

The agent MUST ask:

> "Do you want to trust this `mise.toml`? (yes / no)"

- **Yes** → run `mise trust` for the directory, then continue to Layer 2.
- **No** → halt. Document the decision. Do **not** attempt to use any `mise`-managed tool.

### 1.4 Trust Command

```bash
# Trust the config for the given directory
# Pass the config file path directly as the argument
mise trust /absolute/path/to/directory/mise.toml
```

- The config file path is passed as a positional argument, not via `--path`.
- Note: mise prints trust-error noise during parsing even as it processes the command—
  this is expected. Confirm success by checking for `mise trusted <path>` in the output.

***

## 2. Layer 2 — Mise Tool Selection Protocol

Applies when a tool required by `mise.toml` is missing or could be satisfied by an
already-installed version. This layer applies to **any** `mise`-managed tool (Python,
Node, Go, etc.).

### 2.1 Inventory

```bash
# List every installed version of a tool (replace `python` with the tool name)
mise ls python --json
```

Each JSON element has:

- `version` — installed version string
- `install_path` — filesystem path
- `source.path` — which `mise.toml` declared it
- `active` — whether it is the currently active version

### 2.2 Required Version Freshness Check (Multi-Source)

Before comparison, check whether the version pinned in `mise.toml` is itself
the latest release of the tool. A single source is **not enough**: mise's
remote index can lag the upstream by hours-to-days, and a `github:<owner>/<repo>`
repackaging backend can lag the upstream language project by an entire minor
version. The agent MUST query up to three independent sources and present a
comparison table to the USER.

#### 2.2.1 Tier 1 — Mise Remote Index (always)

```bash
# Newest versions known to mise's resolver:
mise ls-remote <tool>           | tail -5
mise ls-remote 'github:<owner>/<repo>' | tail -5
```

#### 2.2.2 Tier 2 — Backend-Native Truth (for `github:` backend)

The GitHub Releases API publishes a release the moment the upstream maintainer
cuts it — before mise's index resync. Query it with the
[`github-repo-commit-fetch`](../github-repo-commit-fetch/SKILL.md) base
primitive `latest-release.py` (the shipped script, not an inline one-liner):

```bash
python3 .agents/skills/github-repo-commit-fetch/scripts/latest-release.py \
    --repo <owner>/<repo>
# → {"tag_name": "0.69.0", "name": "0.69.0", "published_at": "..."}
```

`--repo` is `owner/name` WITHOUT the `github:` prefix. Raw-curl fallback if
`gh` is unavailable (per `github-rest-api-fallback`):

```bash
curl -s https://api.github.com/repos/<owner>/<repo>/releases/latest \
    | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tag_name"], "-", d["name"])'
```

For `ubi:`, `cargo:`, `npm:`, `pipx:`, and other backends, query the backend's
own registry (crates.io, npmjs.org, PyPI) for the same effect.

#### 2.2.3 Tier 3 — Upstream Language / Project Site (for repackaging backends)

When the backend is a community-maintained repackaging of an upstream language
or project (e.g., `github:adwinying/php` repackages PHP from php.net), the
upstream's own release feed is the meta-truth — it catches the case where the
repackager has not yet rebuilt the latest upstream release:

```bash
# Example: official PHP latest from php.net
curl -s 'https://www.php.net/releases/index.php?json&max=1' \
    | python3 -c 'import json,sys; d=json.load(sys.stdin); k=list(d)[0]; print(k, "->", d[k]["version"])'

# Comparable feeds:
#   Python  → https://www.python.org/api/v2/downloads/release/?is_published=true
#   Node.js → https://nodejs.org/dist/index.json
#   Ruby    → https://www.ruby-lang.org/en/downloads/releases/ (HTML)
```

If the repackager lags upstream by more than a patch release, surface that fact
in the presentation table — the user may want to wait, switch backends, or
proceed knowingly.

#### 2.2.4 Presentation Table

The agent MUST present all queried sources side-by-side:

```text
Pinned in mise.toml         : github:adwinying/php 8.4.11
Tier 1 — mise ls-remote     : 8.5.6  (latest mise-known)
Tier 2 — GitHub Releases    : v8.5.6 (latest repackager release)
Tier 3 — php.net upstream   : 8.5.6  (latest upstream PHP)

Verdict: OUTDATED — pinned is 1 minor + many patches behind on all sources.

Options:
  ① 8.5.6   — latest overall (newest features; possible BC concerns)
  ② 8.4.21  — patch-bump on the pinned 8.4 line (lowest-risk)
  ③ stay on 8.4.11

Recommendation: present, then ask. Do NOT pre-pick.
```

#### 2.2.5 Decision Branches

- **If user wants latest** → install latest AND update `mise.toml` pin.
- **If user wants required** → install required version; do NOT alter `mise.toml`.
- **If user is undecided about conf update** → install chosen version; do NOT alter
  `mise.toml` even if the user chose the latest.

### 2.3 Comparison Logic

Let `required` = version stated in the project `mise.toml`.
Let `installed` = all versions returned by `mise ls <tool> --json`.

| Scenario | Action |
| :--- | :--- |
| **No installed versions** | Run freshness check (§2.2); offer required or latest |
| **Installed version older than required** | Offer: install required OR use existing (with warning) |
| **Installed version exactly equals required** | Recommend using it as-is; no `mise.toml` change needed |
| **Installed version strictly greater than required** | Present analysis; ask user to use it AND offer to update `mise.toml` pin |
| **Multiple versions installed** | Present all with analysis; USER selects one |

> **Greater-version rule**: If the installed version is strictly greater than the pinned
> `required` version, the agent MUST ask the USER two questions:
>
> 1. "Use the installed `<tool>@<installed>` instead of `<tool>@<required>`?"
> 2. "Update `mise.toml` to pin `<tool> = "<installed>"`?" (only if user said yes to 1)
>
> The `mise.toml` MUST NOT be updated unless the USER explicitly approves question 2.

### 2.4 Presentation to User

The agent MUST present a full decision table, for example:

```text
Required by mise.toml : python 3.11
Latest available      : python 3.13.2
Installed under mise  :
  ① python 3.11.9  (active, from ~/.config/mise/config.toml)
                    GREATER than required (3.11.9 > 3.11) ← RECOMMENDED

Recommendation:
  Use python 3.11.9 — already installed, satisfies requirement.
  Offer to update mise.toml pin from "3.11" → "3.11.9"? Ask user.

mise.toml freshness : OUTDATED (3.11 vs latest 3.13.2)
  Separately: offer to bump to 3.13.2? Ask user.
```

### 2.5 User Decision Gate

1. **Which version to use?** User selects from presented options.
2. **Update `mise.toml` pin?** Only if user explicitly confirms.

```bash
# Use an existing installed version — scoped to the config file, not globally
mise use --path /absolute/path/to/project python@<chosen-version>

# Install and use a new version — scoped to config
# Wrap mise install with scratch capture (see Layer 6) so deprecation warnings on
# stderr are preserved for audit:
#   SCRATCH="$(python3 <path>/repo-scratch-output-capture/scripts/ensure-scratch-gitignored.py)"
#   mise install python@<chosen-version> > "$SCRATCH/mise-install.out" 2> "$SCRATCH/mise-install.err"
mise install python@<chosen-version>
mise use --path /absolute/path/to/project python@<chosen-version>
```

- `--path` — Ensures the `use` command writes to the **project-local** `mise.toml`,
  not the global `~/.config/mise/config.toml`. This prevents polluting the global env.

### 2.6 Post-Bump Cleanup of Older Version (Same-Backend Bump)

When a user-approved bump installs `<tool>@<new>` while `<tool>@<old>` still
exists under the **same backend** (e.g., `github:adwinying/php` bumped from
`8.4.11` → `8.5.6`), the old install MUST be cleaned up so it does not consume
disk and does not confuse `mise ls`. The cleanup recipe for this case is
**sharply different** from the cross-backend migration cleanup in §6.5 — read
both before acting.

#### 2.6.1 Why §2.6 ≠ §6.5

| Axis | Same-backend bump (§2.6) | Cross-backend migration (§6.5) |
| :--- | :--- | :--- |
| Backend identity | Identical (`github:` → `github:`) | Changes (`ubi:` → `github:`) |
| Plugin install root | `~/.local/share/mise/installs/<backend>-<owner>-<repo>/` is **LIVE** (hosts the new install) | The old plugin root is **DEAD** (no version references it) |
| Alias symlinks (`<major>`, `<major>.<minor>`, `latest`) | Auto-repointed by mise to `<new>` on install — must be kept | Point at nothing valid — removed with plugin root |
| `mise uninstall <pkg>@<old>` | ✅ Sufficient | ✅ Necessary but **not** sufficient |
| `rm -rf <plugin-root>` | ❌ **FORBIDDEN** — destroys the live `<new>` install | ✅ Required follow-up to remove dangling alias symlinks |

#### 2.6.2 Procedure

Always with scratch capture per
[`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md):

```bash
SCRATCH="$(python3 <path>/repo-scratch-output-capture/scripts/ensure-scratch-gitignored.py)"

# Step 1 — Uninstall the OLD version only (not the plugin root).
mise uninstall '<backend>:<owner>/<repo>@<old>' \
    > "$SCRATCH/mise-uninstall-<old>.out" 2> "$SCRATCH/mise-uninstall-<old>.err"

# Step 2 — Verify the plugin root remains LIVE with symlinks pointing at <new>.
ls -la "$HOME/.local/share/mise/installs/<backend>-<owner>-<repo>/"
# Expected: <new>/ directory present; <major>, <major>.<minor>, latest -> ./<new>

# Step 3 — Verify only <new> is active.
mise current 2>&1 | grep -E '<tool>|<owner>'
mise ls '<backend>:<owner>/<repo>'
# Expected: a single row, version <new>.

# Step 4 — Optional smoke test of the binary.
mise exec -- <binary> --version
```

If `ls -la` shows the symlinks STILL pointing at `<old>` (i.e., mise did not
re-link them on the new install — possible if the user never ran `mise install`
after editing the pin), re-run `mise install` from the project directory
**before** the `mise uninstall`. NEVER `rm -rf` the plugin root to "force" the
relink — that destroys `<new>`.

#### 2.6.3 Worked Example — `github:adwinying/php` 8.4.11 → 8.5.6

Real session against `Account-Ledger-Server-PHP/mise.toml` (2026-05-28):

```bash
# Edit pin in mise.toml: "github:adwinying/php" = "8.5.6"

# Install new version with scratch capture.
SCRATCH="$(python3 .agents/skills/repo-scratch-output-capture/scripts/ensure-scratch-gitignored.py)"
mise install > "$SCRATCH/mise-install-8.5.6.out" 2> "$SCRATCH/mise-install-8.5.6.err"
# → Exit: 0 ; stderr shows download+verify+extract+✓ installed

mise current | grep php
# → github:adwinying/php 8.5.6

# Uninstall the old 8.4.11.
mise uninstall 'github:adwinying/php@8.4.11' \
    > "$SCRATCH/mise-uninstall-8.4.11.out" 2> "$SCRATCH/mise-uninstall-8.4.11.err"
# → mise github:adwinying/php@8.4.11   ✓ uninstalled

# Verify plugin root is LIVE, symlinks repointed.
ls -la ~/.local/share/mise/installs/github-adwinying-php/
# →  8     -> ./8.5.6
# →  8.5   -> ./8.5.6
# →  8.5.6/   (directory)
# →  latest -> ./8.5.6
# (no 8.4.11/ directory — cleaned)

mise ls 'github:adwinying/php'
# → 8.5.6  ~/lab-data/Account-Ledger-Server-PHP/mise.toml  8.5.6
```

### 2.7 Global-Scope Standalone Tool Install (No Project `mise.toml`)

Layers 2.1–2.6 assume a project-scoped `mise.toml` (`mise use --path`).
Some tools — standalone CLI utilities like `difftastic`, `bat`, `fzf` — are
user-level tools (usable across every project), not project-bound languages.
When the workspace has NO `mise.toml` (checked via `ls mise.toml .mise.toml`),
the Layer's decision path diverges: the pin goes into the **global**
`~/.config/mise/config.toml`, and the install targets the **full backend
specification string** rather than a bare tool name.

#### 2.7.1 Scope Decision Gate (ask the user)

| # | Scope | Command | When |
| :--- | :--- | :--- | :--- |
| ① | **Global config** (Recommended for standalone CLI tools) | pin in `~/.config/mise/config.toml` + `mise install '<backend>:<owner>/<repo>@<ver>'` | Tool is a user-level CLI meant to work in every project |
| ② | Project `mise.toml` | `mise use --path /abs/path/to/project <tool>@<ver>` | Tool is only needed in this repo, and a `mise.toml` exists or will be created |
| ③ | Install only, no pin | `mise install '<backend>:<owner>/<repo>@<ver>'` | One-off smoke test / evaluation; do not persist |

#### 2.7.2 Freshness + install (global path) — worked recipe

Version selection still runs the §2.2 multi-source freshness check (Tier 1
`mise ls-remote 'github:<owner>/<repo>'`, Tier 2 `latest-release.py`). Only the
config-target and the install string differ:

```bash
# 1. Confirm NO project mise.toml anchors the tool.
ls mise.toml .mise.toml

# 2. Multi-source freshness (see §2.2):
mise ls-remote 'github:Wilfred/difftastic' | tail -5
python3 .agents/skills/github-repo-commit-fetch/scripts/latest-release.py --repo Wilfred/difftastic

# 3. Ask the user for scope (§2.7.1 ①/②/③). If ①:
#    Add to ~/.config/mise/config.toml under [tools]:
#      "github:Wilfred/difftastic" = "0.69.0"

# 4. Install the FULL backend spec with scratch capture (Layer 6).
SCRATCH="$(python3 .agents/skills/repo-scratch-output-capture/scripts/ensure-scratch-gitignored.py)"
mise install 'github:Wilfred/difftastic@0.69.0' \
    > "$SCRATCH/mise-install-difftastic.out" 2> "$SCRATCH/mise-install-difftastic.err"

# 5. Verify no deprecation warnings (Layer 6.1) and smoke-test the binary.
grep -E "deprecated|will be removed" "$SCRATCH/mise-install-difftastic.err" \
    || echo "no deprecation warnings"
mise exec -- difft --version
```

Key differences from §2.5 (project path):

- **Pin location**: global `[tools]` in `~/.config/mise/config.toml`, added by
  direct config edit after explicit user approval — §2.5's project-scoped
  `--path` guarantee only applies when a project toml is the target.
- **Install string**: the FULL backend form `'<backend>:<owner>/<repo>@<version>'`
  (e.g. `'github:Wilfred/difftastic@0.69.0'`) — a bare `difftastic@0.69.0` does
  NOT resolve for a `github:` backend.
- **Binary name**: often differs from repo name (difftastic ships `difft`).
  Discover the shipped binary in
  `~/.local/share/mise/installs/github-Wilfred-difftastic/<ver>/` before the
  smoke test.
- **Scope gate is mandatory**: get user approval before BOTH the global-config
  edit AND the install — matching §10's prohibition on unprompted global
  mutation.

***

## 3. Layer 3 — Mise Python Environment Setup

A specialisation of Layer 2 for the Python tool. Python requires extra steps to verify
the interpreter and `pip` are available through `mise exec`, preventing accidental use
of the system Python.

### 3.1 Verify Python via `mise exec`

Always use `mise exec` to invoke Python, scoped to the correct configuration file:

```bash
# Verify the exact Python version (not system Python)
mise exec --cd /absolute/path/to/project python@<version> -- python --version

# Verify pip is bundled with mise-managed Python
mise exec --cd /absolute/path/to/project python@<version> -- python -m pip --version
```

- `mise exec` — Runs the command inside the mise environment, bypassing system PATH.
- `python@<version>` — Pins the exact version, preventing accidental tool resolution.
- `--cd /absolute/path/to/project` — Ensures the correct local `mise.toml` is loaded,
  NOT the global config.
- `--` — Separator between `mise exec` arguments and the actual command to run.

### 3.2 Repair pip if Missing

```bash
mise exec --cd /absolute/path/to/project python@<version> -- python -m ensurepip --upgrade
```

Both verification commands MUST succeed before proceeding to Layer 4.

### 3.3 Runtime Tool Resolution

When a script needs to invoke a mise-managed tool at runtime, use the
decision tree below.  Applies to any tool: Python, Node, Ruby, PHP, etc.

```
Q: Does `<tool>` on PATH give an acceptable version?
├── YES → Use `<tool>` directly (fastest, no cascade risk)
└── NO  → Q: Is there a mise.toml that pins this tool?
         ├── YES → Q: Does `mise exec` trigger unwanted cascade?
         │   ├── NO  → `mise exec --cd /project -- <tool> <args>`
         │   └── YES → Direct installation path:
         │              `~/.local/share/mise/installs/<tool>/<version>/bin/<tool>`
         └── NO  → Install via `mise install <tool>@<version>`
```

**PATH resolution** — Works if the system or a mise shim puts a satisfactory
version on PATH.  Fastest approach, no risk of triggering cascade
installation of unrelated tools from `mise.toml`.

**`mise exec`** — Guarantees the correct tool version but can trigger
installation of *every* missing tool listed in `mise.toml` (the "cascade
risk").  Safe for single-tool configs; risky when `mise.toml` pins many
tools (e.g. Flutter + PHP + Java).

**Direct path** — Bypasses mise entirely by invoking the binary directly
from `~/.local/share/mise/installs/`.  Use when `mise exec` would trigger
cascade or when the mise environment is broken.  The version MUST be
pre-installed.

**`mise install`** — Last resort when no acceptable version exists anywhere.
Installs the specific version and makes it available for direct-path use.

Concrete examples:

```bash
# Python — direct PATH (preferred)
python3 script.py

# Node — mise exec (single-tool config safe)
mise exec --cd /project -- node script.js

# Ruby — direct path (bypass cascade risk)
~/.local/share/mise/installs/ruby/3.3.0/bin/ruby script.rb

# Install missing PHP
mise install php@8.3
```

For the companion **documentation convention** (skill docs MUST use simplified
forms like `python3`, never fragile path commands in examples), see
[skill-factory mandate #7](../skill-factory/SKILL.md#2211-universal-script-mandates).

***

## 4. Layer 4 — Mise Python Package Setup Protocol

Applies when a Python package (e.g. `pylint`, `black`, `ruff`) is required but not
installed. Requires Layer 3 to be complete. Uses `jq` for JSON parsing — ensure
`jq` is installed via the [System-Wide Tool Management Skill](../system-wide-tool-management/SKILL.md)
before running §4.3.

### 4.1 Requirements File Detection

Check whether a `requirements.txt` exists in the project scripts directory:

```bash
# Use absolute path to avoid any working-directory ambiguity
ls /absolute/path/to/project/requirements.txt 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

### 4.2 Package Entry Check

If `requirements.txt` exists, check whether the target package is listed:

```bash
# Replace `pylint` with the package name; use absolute path
grep -i "^pylint" /absolute/path/to/project/requirements.txt
```

### 4.3 Version Freshness Check via PyPI (using `jq`)

If the package is listed, compare the pinned version against the latest on PyPI:

```bash
# Get the latest published version from PyPI — requires jq (see system-wide-tool-management skill)
curl -s https://pypi.org/pypi/pylint/json | jq -r '.info.version'
```

- `curl -s` — Silent mode; suppresses progress output.
- `https://pypi.org/pypi/<package>/json` — PyPI JSON API endpoint for any package.
- `jq -r '.info.version'` — Extracts the `version` field from `info` as raw text.
  The `-r` flag removes surrounding quotes.

### 4.4 Decision Table

| State | Action |
| :--- | :--- |
| `requirements.txt` missing | Create it; add `<package>==<latest>` |
| Package not in `requirements.txt` | Add `<package>==<latest>` |
| Package pinned to outdated version | Present analysis; offer to update pin to latest |
| Package pinned to latest | Proceed directly to installation |

If pinned version is **not** the latest:

1. Present comparison to user (pinned vs latest).
2. Ask: "Update pin to latest and install?"
3. **User says yes to latest** → update pin, install.
4. **User says no to latest** → install the pinned version as-is. Do NOT alter
   `requirements.txt`.

### 4.5 Presentation to User

The agent MUST present its analysis, for example:

```text
requirements.txt  : /absolute/path/to/project/requirements.txt — EXISTS
pylint entry      : MISSING
Latest on PyPI    : 3.3.4

Recommendation:
  Add `pylint==3.3.4` to requirements.txt, then install via:
  mise exec python@3.11.9 -- python -m pip install -r /absolute/path/to/project/requirements.txt
```

### 4.6 User Decision Gate

> "Approve adding `pylint==<version>` to `requirements.txt` and installing? (yes / no)"

### 4.7 Installation

Upon approval, always use `mise exec` with an absolute path to `requirements.txt`:

```bash
# Install all packages declared in requirements.txt into the active mise python env
mise exec --cd /absolute/path/to/project python@<version> -- \
  python -m pip install -r /absolute/path/to/project/requirements.txt
```

- `mise exec --cd ... python@<version>` — Targets the exact mise-managed Python,
  not the system interpreter. This ensures packages land in the correct isolated environment.
- `python -m pip` — Uses the pip bundled with the `mise`-managed Python.
- `-r /absolute/path/to/project/requirements.txt` — Reads the pinned dependency file for reproducible installs.
  Absolute path eliminates any working-directory ambiguity.

### 4.8 Execution Verification

After installation, verify the tool works:

```bash
# Example: verify pylint is reachable and show its version
mise exec --cd /absolute/path/to/project python@<version> -- python -m pylint --version
```

***

## 5. Layer 5 — Bypass `mise exec` Cascade Protocol

`mise exec` walks UP the directory tree from the current working directory and, for every
trusted `mise.toml` it finds, ensures **every pinned tool** is installed before running your
command. From an unrelated repo, a one-shot `mise exec -- python script.py` can trigger
multi-GB downloads of Flutter, PHP, Composer, etc. — completely unrelated to the actual task.

This layer documents the **direct-binary invocation** alternative: invoke the mise-installed
binary by its concrete install path, which is still mise-managed (versioned, isolated from
system Python), but skips the trust-chain walk that triggers the cascade.

### 5.1 Detection — Are You at Risk of a Cascade?

Run from the CWD where you'd otherwise call `mise exec`:

```bash
mise current 2>&1
```

If the output lists tools you do NOT need for the current task (e.g., `flutter@3.22.3`,
`php@8.4.11`, `composer@...`, `ubi:adwinying/php`), `mise exec` will attempt to install all of
them before running your command. Cascade risk = HIGH.

### 5.2 Resolution — Direct-Binary Path

The mise install root is conventionally:

```text
$HOME/.local/share/mise/installs/<tool>/<version>/bin/<binary>
```

To find the version directory for a given tool:

```bash
ls "$HOME/.local/share/mise/installs/<tool>" | sort -V | tail -1
```

Then invoke directly — no shim, no trust walk, no cascade:

```bash
python3 --version
python3 -m pip install --user pymysql
```

**This is NOT the same as invoking from `$PATH`.** The prohibition in §10 against "Invoking
`python` or `pip` from PATH" targets unmanaged system binaries (`/usr/bin/python3` on macOS
is Apple Xcode 3.9, not your pinned version). The Layer 5 path is an explicit, version-pinned
mise install — fully consistent with the environment-management mandate.

### 5.3 When to Prefer Layer 5 over Layers 3/4

| Situation | Use Layer 3/4 (`mise exec`) | Use Layer 5 (direct path) |
| --- | --- | --- |
| CWD is the project that pins the tool | ✅ | — |
| CWD has NO `mise.toml` in ancestry | ✅ | acceptable |
| CWD's ancestor `mise.toml` pins UNRELATED tools (cascade risk) | ❌ | ✅ |
| Running a one-shot probe from an unrelated repo | ❌ | ✅ |
| CI / scripted invocation where install side-effects are forbidden | ❌ | ✅ |

### 5.4 Stream Convention Note (`mise trust` and Friends)

`mise trust`, `mise install`, and similar housekeeping commands write their confirmation
messages to **stderr**, not stdout, per Unix convention (stdout reserved for pipeable data
such as resolved paths; stderr for diagnostics). If you redirect only stdout to a log file
you will see an empty log and misinterpret the command as silently failing — always pair
`> stdout.log 2> stderr.log` or use `2>&1` when capturing.

This convention is shared with `git`, `cargo`, `rustup`, `npm` (for non-data output), and
most modern CLIs.

### 5.5 Cleanup After an Accidentally-Triggered Cascade

If `mise exec` was invoked from an unsafe CWD and partial installs leaked, clean up:

```bash
# 1. List recent mise installs (lots of dirs = cascade evidence).
ls -lt "$HOME/.local/share/mise/installs/" | head

# 2. Remove specific unwanted tool installs.
rm -rf "$HOME/.local/share/mise/installs/flutter/<version>"
rm -rf "$HOME/.local/share/mise/installs/ubi-adwinying-php"
rm -rf "$HOME/.local/share/mise/installs/ubi-composer-composer"
rm -rf "$HOME/.local/share/mise/installs/vfox-version-fox-vfox-php-<version>"

# 3. Remove partial download archives.
rm -f "$HOME/.cache/mise/<tool>/<version>.zip"
```

Verify nothing the user actually wanted got deleted:

```bash
mise ls
```

### 5.6 Consumers of Layer 5

- [`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md) — its
  `probe-runner.py` resolves python via Layer 5 to avoid the cascade when probing from any
  repo other than the python's home project.
- PHP `php -l` syntax linting outside the PHP-pinned project — resolve the binary directly
  at `~/.local/share/mise/installs/github-adwinying-php/<version>/php`. NOTE: the
  `adwinying/php` plugin (asdf-style) places the binary **directly** under the version
  directory with **no** `bin/` subdirectory, unlike the python plugin. Discover the exact
  path via `find ~/.local/share/mise/installs/github-adwinying-php/<version> -name php -type f`
  before scripting an invocation.
- Any future cross-repo probe / installer / one-shot script.

***

## 6. Layer 6 — Deprecation Warning Handling & Backend Migration Protocol

`mise` emits deprecation warnings on **stderr** (e.g.
`mise WARN  deprecated [ubi]: The ubi backend is deprecated. Use the github
backend instead …`) the first time an affected tool is resolved. Because the
warning is on stderr and `mise install` is otherwise terse on success, the
warning is **invisible** unless stderr is captured. This layer mandates the
capture, surfaces the warning to the user, and drives the `mise.toml` migration.

### 6.1 Capture-First Detection

Every `mise install` / `mise trust` / `mise ls` invocation in an unattended or
agent-driven flow MUST be wrapped in the scratch-capture pattern from the
[`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) base
skill. The scratch skill is the SSOT for the capture mechanics — this skill
only specifies *what* to capture and *how to react* to the captured content.

```bash
SCRATCH="$(python3 <path-to>/repo-scratch-output-capture/scripts/ensure-scratch-gitignored.py)"
mise install \
    > "$SCRATCH/mise-install.out" \
    2> "$SCRATCH/mise-install.err"
echo "Exit: $?"
```

After every invocation, grep stderr for deprecation signals:

```bash
grep -E "deprecated|will be removed" "$SCRATCH/mise-install.err" || \
    echo "(no deprecation warnings)"
```

### 6.2 Known Backend Deprecations

| Deprecated form in `mise.toml` | Replacement | Removal version | Notes |
| :--- | :--- | :--- | :--- |
| `"ubi:<owner>/<repo>" = "<ver>"` | `"github:<owner>/<repo>" = "<ver>"` | mise `2027.1.0` | The `ubi` backend is deprecated workspace-wide; the `github` backend is the direct successor and supports the same `<owner>/<repo>` slug. |

This table is the project's living deprecation registry. When `mise` introduces
a new deprecation, add a row here in the same change that documents the
migration — do NOT scatter migration notes across consumer projects.

### 6.3 Migration Decision Gate

When stderr contains a deprecation warning, the agent MUST:

1. **Present** the literal warning text to the user (quoted from the captured
   `.err` file).
2. **Identify** the affected entry in `mise.toml` (file path + line number +
   current value).
3. **Propose** the literal replacement form from §6.2.
4. **Cite** the removal version (so the user can decide urgency vs. risk).
5. **Ask**: "Migrate `<old>` → `<new>` in `mise.toml`? (yes / no)"

The `mise.toml` MUST NOT be edited without explicit user approval, in keeping
with the general prohibition in §10.

### 6.4 Migration Execution

Upon approval, perform the edit, re-install with scratch capture, and verify
no deprecation warning remains:

```bash
# 1. Edit mise.toml (literal replacement; preserve quoting and indentation).
#    Use whatever in-place editor is appropriate; verify with diff.
#    Example transformation:
#      "ubi:adwinying/php"    = "8.4.11"
#    →  "github:adwinying/php" = "8.4.11"

# 2. Re-run install with scratch capture.
SCRATCH="$(python3 <path-to>/repo-scratch-output-capture/scripts/ensure-scratch-gitignored.py)"
mise install \
    > "$SCRATCH/mise-install-postmigration.out" \
    2> "$SCRATCH/mise-install-postmigration.err"

# 3. Verify warning is gone.
grep -E "deprecated|will be removed" "$SCRATCH/mise-install-postmigration.err" \
    && echo "STILL DEPRECATED — investigate" \
    || echo "Migration verified clean."

# 4. (Optional) Validate the edited mise.toml per §9.2.
taplo check /absolute/path/to/project/mise.toml
taplo fmt --check /absolute/path/to/project/mise.toml
```

### 6.5 Stale-Install Cleanup

> **Contrast pointer**: §6.5 applies ONLY when the backend identifier itself
> changed (e.g., `ubi:` → `github:`), so the OLD plugin root is dead. For a
> same-backend version bump (e.g., `github:` 8.4.11 → 8.5.6) the plugin root
> is still LIVE and `rm -rf` of it would destroy the new install — use §2.6
> instead.

After a successful backend migration, the previous backend's install directory
under `~/.local/share/mise/installs/` is no longer referenced by `mise.toml`
but still consumes disk. The cleanup is **two-step** because `mise uninstall`
only removes the version directory — it does NOT remove the version-aliasing
symlinks (`8`, `8.4`, `latest`) that pointed to it, leaving them dangling.

Step 1 — Uninstall via mise (preferred over raw `rm -rf` so mise's internal
registry, caches, and `.mise.backend.toml` are all cleaned up):

```bash
SCRATCH="$(python3 <path>/repo-scratch-output-capture/scripts/ensure-scratch-gitignored.py)"
mise uninstall 'ubi:<owner>/<repo>@<version>' \
    > "$SCRATCH/mise-uninstall.out" 2> "$SCRATCH/mise-uninstall.err"
```

Step 2 — Remove the now-empty plugin root and its dangling symlinks:

```bash
ls -la "$HOME/.local/share/mise/installs/ubi-<owner>-<repo>/"   # confirm only dangling symlinks remain
rm -rf "$HOME/.local/share/mise/installs/ubi-<owner>-<repo>"
```

Step 3 — Verify the deprecated entry is gone and the replacement is active:

```bash
mise current 2>&1 | grep -E '<tool>|<owner>'
# → github:<owner>/<repo> <version>   (no ubi: line)
```

For wholesale removal after an accidentally-triggered cascade (multiple
unrelated tools to delete), §5.5 owns the bulk `rm -rf` recipe; this section
owns the targeted single-tool migration cleanup.

### 6.6 Worked Example — `ubi:adwinying/php` → `github:adwinying/php`

Real session against `Account-Ledger-Server-PHP/mise.toml` (2026-05-28):

```bash
# Initial capture
SCRATCH="$(python3 .agents/skills/repo-scratch-output-capture/scripts/ensure-scratch-gitignored.py)"
mise install > "$SCRATCH/mise-install.out" 2> "$SCRATCH/mise-install.err"
# → Exit: 0

tail -2 "$SCRATCH/mise-install.err"
# mise WARN  deprecated [ubi]: The ubi backend is deprecated. Use the github
#   backend instead (e.g., github:owner/repo). This will be removed in mise 2027.1.0.
# mise ubi:adwinying/php@8.4.11      ✓ installed
```

Migration:

```diff
 [tools]
-"ubi:adwinying/php" = "8.4.11"
+"github:adwinying/php" = "8.4.11"
```

Verification:

```bash
mise install > "$SCRATCH/mise-install-2.out" 2> "$SCRATCH/mise-install-2.err"
# → Exit: 0
grep -E "deprecated|will be removed" "$SCRATCH/mise-install-2.err" || echo "clean"
# → clean
tail -3 "$SCRATCH/mise-install-2.err"
# mise github:adwinying/php@8.4.11     [2/3] verify GitHub artifact attestations
# mise github:adwinying/php@8.4.11     [3/3] extract php-8.4.11-macos-aarch64.tar.gz
# mise github:adwinying/php@8.4.11   ✓ installed
```

***

## 7. Layer 7 — Plugin Installation & Backend Selection Protocol

Mise plugins frequently exist under multiple competing backends
(`asdf:`, `vfox:`, `github:`, `aqua:`, `ubi:`). The choice is **not
interchangeable** — different backends ship different binaries, manage
their own install roots, and have different SSH / HTTPS reachability
profiles on different networks. This Layer runs **before** Layers 1–6:
no version pin, no trust prompt, no `mise install` invocation can
succeed if the underlying plugin is missing or installed under a
backend that doesn't resolve in the current environment.

### 7.1 Detection

Apply this Layer whenever:

- The user issues `mise install <plugin>` (single-plugin install)
- The user issues `mise install` in a project folder and it fails with
  a plugin-resolution error (e.g., `plugin <name> not found`, SSH
  authentication failure resolving an `asdf:` or `vfox:` URL, or
  `mise registry` returning multiple candidates)
- A `mise.toml` references a tool whose plugin is not yet installed
  locally (`mise plugins --user` does not list it)

### 7.2 Backend Inventory

Query the mise registry for all available backends for the plugin:

```bash
# Show every registered backend for a given tool name
mise registry <plugin>
```

If the output lists more than one entry (e.g., `dart` may show
`asdf:asdf-community/asdf-dart` and `vfox:version-fox/vfox-dart`), the
plugin has **multiple backends** and the user MUST choose explicitly —
never auto-pick the first match.

### 7.3 Presentation to User

Present a numbered table of every backend candidate with its full
GitHub URL and a brief differentiator:

| # | Backend | Repo | Notes |
|---|---|---|---|
| 1 | `asdf:` | `asdf-community/asdf-dart` | Mature, large user base |
| 2 | `vfox:` | `version-fox/vfox-dart`    | Newer, cross-platform Lua plugin runtime |

Ask the user which to install. Do NOT proceed without an explicit
choice.

### 7.4 Installation — Full GitHub URL Form

Once the user has chosen a backend, install the plugin using the
**full HTTPS GitHub URL** of the chosen backend's repository:

```bash
mise plugins install <plugin> https://github.com/<org>/<repo>.git
```

**Forbidden form — `vfox:` / `asdf:` URL prefixes:**

```bash
# ❌ DO NOT USE — these prefixes cause SSH auth failures on networks
#    that lack a configured GitHub SSH key, even when the user is
#    fully authenticated for HTTPS clones.
mise plugins install <plugin> vfox:version-fox/vfox-<plugin>
mise plugins install <plugin> asdf:asdf-community/asdf-<plugin>
```

The HTTPS `.git` URL form sidesteps the SSH-key requirement and works
identically on Gitpod, Cloud Shell, NeverInstall, plain Ubuntu, macOS,
and Windows.

### 7.5 Triggering the Tool Install

**`mise.toml` precedence — Layer 7 never overrides it.** Layer 7
activates only when (a) the user issues a bare-plugin
`mise install <plugin>` outside of `mise.toml` control, or (b) a
project-folder `mise install` has already failed with a plugin-
resolution error. While `mise.toml` resolves cleanly, Layer 7 is a
no-op; the agent MUST NOT pre-emptively prompt for a backend choice
on plugins that `mise.toml` is silently happy with.

After the plugin lands, invoke the actual tool install. Two cases:

**Single-plugin install (user originally said `mise install <plugin>`):**

```bash
mise install <plugin>
```

This installs the latest version known to the freshly-installed
plugin's backend. From here, hand off to **Layer 2** (§2) for
version-freshness review and pinning.

**Project-folder install (user originally said `mise install`):**

```bash
mise install
```

This re-reads `mise.toml` and installs every pinned tool. If a
previous `mise install` attempt failed because the wrong-backend
plugin was installed, first **uninstall** the problematic backend
plugin before re-trying:

```bash
mise plugins uninstall <plugin>
mise plugins install <plugin> https://github.com/<org>/<repo>.git
mise install
```

### 7.6 Verification

After any plugin install, verify the registered backend URL:

```bash
mise plugins --urls --user
```

The output MUST show the plugin name mapped to the exact HTTPS URL
chosen in §7.3. If a `vfox:` or `asdf:` prefix appears instead, the
install bypassed this Layer — uninstall and re-run with the HTTPS
form before proceeding.

### 7.7 Decision Matrix (Quick Reference)

| User says | mise registry returns | Action |
|---|---|---|
| `mise install <plugin>` | 1 backend | Install with HTTPS URL (§7.4), then `mise install <plugin>` (§7.5) |
| `mise install <plugin>` | ≥ 2 backends | Present table (§7.3), get user choice, then §7.4 + §7.5 |
| `mise install` in project | succeeds | No-op — Layer 7 does not apply |
| `mise install` in project | fails with plugin error | Identify failed plugin, check `mise registry <plugin>` for alternatives, if ≥ 2: present table (§7.3) → uninstall (§7.5 second case) → reinstall via HTTPS → retry |

### 7.8 Worked Examples

#### 7.8.1 Scenario A — Bare-plugin install, multi-backend choice

User says: `mise install dart`

```bash
$ mise registry dart
asdf:asdf-community/asdf-dart
vfox:version-fox/vfox-dart
```

Two backends → Layer 7 applies. Agent prompts (literal phrasing from
the source rule):

> *"dart has asdf and vfox backends, which do you prefer?"*

User picks `asdf:`. Agent runs:

```bash
mise plugins install dart https://github.com/asdf-community/asdf-dart.git
mise install dart
mise plugins --urls --user | grep dart
# dart  https://github.com/asdf-community/asdf-dart.git
```

Layer 7 complete. Hand off to Layer 2 for version pin.

#### 7.8.2 Scenario B — Project-folder install fails, fallback to alternate backend

User runs `mise install` in a project folder pinning `dart`. The
currently-installed plugin backend (e.g., `asdf:asdf-community/asdf-dart`)
fails to resolve — network rejects the upstream tarball, the asdf
shim crashes, or the binary fails to launch post-install. Agent
checks `mise registry dart`, sees `vfox:` is also available, and
prompts (literal phrasing from the source rule):

> *"dart installation failed, try vfox backend instead?"*

User confirms. Agent runs:

```bash
mise plugins uninstall dart
mise plugins install dart https://github.com/version-fox/vfox-dart.git
mise install
mise plugins --urls --user | grep dart
# dart  https://github.com/version-fox/vfox-dart.git
```

`mise.toml` is unchanged (Layer 7 swaps the backend, never the
version pin). Hand off to Layer 2 only if the user now wants to bump
the version.

***

## 8. Full Worked Example — Pylint Setup for `sync-rules.py`

This section demonstrates all four layers against the real scenario.

### 8.1 Layer 1: Trust Check

```bash
mise ls 2>&1
# → mise ERROR: Config files in .../scripts/mise.toml are not trusted.
```

Present `mise.toml`:

```toml
[tools]
python = "3.11"
```

**Analysis**: Only pins `python = "3.11"`. No scripts or hooks. Safe to trust.

**Ask user**: "Trust this `mise.toml`? (yes/no)"

```bash
mise trust /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts/mise.toml
# → mise trusted /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts
```

### 8.2 Layer 2: Python Version Selection

```bash
mise ls python --json
mise ls-remote python | tail -5
```

```text
Required by mise.toml : python 3.11
Latest available      : python 3.13.2
Installed under mise  :
  ① python 3.11.9  (active, from ~/.config/mise/config.toml)
    — Satisfies requirement (3.11.9 >= 3.11). RECOMMENDED.

mise.toml is OUTDATED (3.11 vs 3.13.2).
Offer to update? Ask user.
```

**User decision**: Use `3.11.9`, do not update `mise.toml`.

```bash
mise use --path /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts python@3.11.9
```

### 8.3 Layer 3: Python Verification

```bash
mise exec --cd /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts python@3.11.9 -- python --version
# → Python 3.11.9
mise exec --cd /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts python@3.11.9 -- python -m pip --version
# → pip 24.x
```

### 8.4 Layer 4: Pylint Setup

```bash
grep -i "^pylint" /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts/requirements.txt
# → (no match)

curl -s https://pypi.org/pypi/pylint/json | jq -r '.info.version'
# → 3.3.4
```

**Analysis**: `pylint` absent from `requirements.txt`. Latest is `3.3.4`.

**Recommendation**: Add `pylint==3.3.4` to `requirements.txt` and install.

```bash
# After user approval:
echo "pylint==3.3.4" >> /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts/requirements.txt

mise exec --cd /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts python@3.11.9 -- \
  python -m pip install -r /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts/requirements.txt

mise exec --cd /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts python@3.11.9 -- \
  python -m pylint --version
```

***

## 9. Post-Edit File Validation Protocol

After **any** edit to a project file, the agent MUST validate the file using its
industrial-standard tool before proceeding. This catches formatting errors (e.g. stray
indentation) introduced by automated edits.

> The validation tools listed here are **system-wide tools**. Ensure they are installed
> using the [System-Wide Tool Management Skill](../system-wide-tool-management/SKILL.md)
> before running these commands.

### 9.1 Validation Commands by File Type

| File | Tool | Syntax Check | Format Check & Fix |
| :--- | :--- | :--- | :--- |
| `mise.toml` | `taplo` | `taplo check <absolute_path>` | `taplo fmt --check <absolute_path>` / `taplo fmt <absolute_path>` |
| `requirements.txt` | `pip` | `pip install --dry-run -r <absolute_path>` | N/A (no formatter) |
| `*.md` Markdown | `markdownlint-cli2` | `markdownlint-cli2 <absolute_path>` | `markdownlint-cli2 --fix <absolute_path>` |
| `*.py` Python | `pylint` via `mise exec` | `mise exec --cd <project_dir> python@<ver> -- python -m pylint <absolute_path>` | Manual fix per error |

> **Note on Python Errors & Formatting:**
>
> - `pylint` is a strict, comprehensive linter. It highlights semantic and structural
>   errors (e.g., missing docstrings, generic exceptions, complexity limits) which
>   **must be fixed manually** via code edits.
> - **DO NOT manually fix Pylint errors** before exhausting auto-fixers. You MUST use
>   specialized formatters and auto-fixers first to resolve stylistic and structural
>   complaints automatically.
> - **Primary Industrial Standard**: Use **`ruff check --fix`** and **`ruff format`** first.
>   It is drastically faster and can auto-fix many structural and code-style issues.
> - **Secondary Standard (Fallback)**: If `ruff` cannot be used, youMUST use **`black`**.
>   `black` is the definitive, uncompromising Python code formatter and was the
>   industry standard before `ruff`. (Only use `autopep8` as a last-resort legacy fallback).
> - Only after running these auto-fixers should you manually fix any remaining semantic
>   Pylint errors (e.g., missing docstrings, complex logic).
> - Because these are Python tools, they MUST follow Layer 4: add them to
>   `requirements.txt` and run them via `mise exec`.

### 9.2 `mise.toml` Validation & Formatting (`taplo`)

> **Important distinction:**
>
> - `taplo check` — validates TOML **syntax** (parse errors, duplicate keys). A file can
>   pass `check` but still be incorrectly formatted.
> - `taplo fmt --check` — verifies **formatting** (indentation, spacing, alignment).
> - `taplo fmt` — **auto-fixes** formatting in place; run after `check` passes.

Always run **both** steps in order:

```bash
# taplo must be installed — use system-wide-tool-management skill if missing
# Step 1 — Syntax check (exits 1 if invalid TOML)
taplo check /absolute/path/to/project/mise.toml

# Step 2 — Formatting check (exits 1 if not properly formatted)
taplo fmt --check /absolute/path/to/project/mise.toml

# Step 3 — Auto-format if Step 2 fails (modifies file in place)
taplo fmt /absolute/path/to/project/mise.toml

# Step 4 — Re-run formatting check to confirm clean
taplo fmt --check /absolute/path/to/project/mise.toml
```

- ✅ `taplo check`: exit 0, output `found files total=1` with no ERROR lines
- ✅ `taplo fmt --check`: exit 0 (no output on success)
- ❌ `taplo fmt --check` exit 1: `ERROR ... the file is not properly formatted` — run
  `taplo fmt` to auto-fix

Common TOML formatting mistakes:

- Leading indentation on key-value pairs under a table header.
    - ❌ Incorrect: `python = "3.11"` (4 spaces before `python`)
    - ✅ Correct: `python = "3.11"` (Starts securely at the beginning of the line)
- Missing blank line separating table sections
- Inconsistent quote style

### 9.3 `requirements.txt` Validation (`pip`)

```bash
pip install --dry-run -r /absolute/path/to/project/requirements.txt 2>&1 \
  | grep -E "^(Collecting|Requirement already|ERROR|WARNING)"
```

- ✅ Success: only `Collecting` and `Requirement already satisfied` lines; exit 0
- ❌ Failure: any `ERROR` line — fix the package specifier before proceeding
- No auto-formatter for `requirements.txt`; fix manually.

### 9.4 Worked Example — Validation After This Session's Edits

```bash
# Step 1 — Syntax check
taplo check /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts/mise.toml
# → INFO taplo: found files total=1 ... (no ERROR) ✅

# Step 2 — Formatting check (detected issue: 4-space indent on python key)
taplo fmt --check /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts/mise.toml
# → ERROR ... the file is not properly formatted ❌

# Step 3 — Auto-fix
taplo fmt /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts/mise.toml
# → (reformats in place)

# Step 4 — Confirm clean
taplo fmt --check /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts/mise.toml
# → (no output, exit 0) ✅

# Validate requirements.txt
pip install --dry-run -r /Users/dk/lab-data/ai-agents/ai-agent-rules/scripts/requirements.txt \
  2>&1 | grep -E "^(Collecting|Requirement already)"
# → Collecting google-generativeai==0.8.5 ... ✅
# → Collecting pylint==4.0.5 ...              ✅
```

***

## 10. Prohibited Actions

The agent is FORBIDDEN from:

- Running `mise use`, `mise install`, or `pip install` without explicit user approval.
- Modifying `requirements.txt` before presenting the full analysis to the USER.
- Modifying `mise.toml` (version pin) without explicit user approval, even if the user
  chose a newer tool version for installation.
- Trusting a `mise.toml` without first reading and presenting its full content.
- Invoking `python` or `pip` directly from PATH — always use `mise exec` with an
  explicit version and `--cd` to guarantee the correct environment.
- Running `mise use` without a project-scoped config target — always scope to the
  project directory, not globally. **Sole exception**: the §2.7 global-scope
  standalone-tool flow, which still requires explicit user approval.
- **Skipping post-edit file validation** — every edited file MUST be validated with its
  industrial-standard tool (§9) before proceeding to the next step.
- **Adding inline disable comments (e.g. `# pylint: disable=...`)** without asking the
  user first. The agent MUST present the error (e.g., `invalid-name` for a file name)
  and ask the user how they want to resolve it (e.g., rename the file vs disable the check).

***

## 11. Composition by Higher-Level Skills

| Composer | Domain | Pipes into this skill via |
| :--- | :--- | :--- |
| [mise-backend-vscode-tool-bridge](../mise-backend-vscode-tool-bridge/SKILL.md) | Non-default-backend installs (`github:`, `ubi:`, `asdf:`, `http:`) whose binary cannot be resolved by `mise which` and therefore cannot be auto-detected by the Mise VS Code extension. | Sibling Layer of §2 (Tool Selection) — uses [mise-non-standard-backend-bin-resolve](../mise-non-standard-backend-bin-resolve/SKILL.md) for resolution, then wires the result into VS Code via [vscode-multi-scope-setting-write](../vscode-multi-scope-setting-write/SKILL.md). |

When `mise which <tool>` fails for a non-default backend install, do NOT
loop back through Layers 1–7 — delegate directly to the bridge composer
above; it is the SSOT for that path.
