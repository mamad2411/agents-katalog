---
name: brew-upgrade-workflow
description: Composer skill for Homebrew upgrade workflows — discovers outdated leaves, resolves formula vs cask types, applies default priority ordering, and delegates command assembly to the brew-upgrade-command-assembly base primitive.
category: Package-Management
---

# Brew Upgrade Workflow Skill (v4) — Composer

Domain-specific composition layer that drives the Homebrew sequential upgrade workflow defined in `brew-rules.md`. It handles:

- **Discovery**: Running `brew outdated --greedy` to identify pending updates
- **Leaf Filtering**: Cross-referencing against `brew leaves --installed-on-request` to exclude dependency formulae
- **Type Resolution**: Determining formula vs cask for each target package
- **Priority Ordering**: Applying the default priority
  (google-chrome, onedrive, visual-studio-code, gemini-cli) and
  respecting user-specified overrides
- **Assembly Delegation**: Invoking
  [`brew-upgrade-command-assembly`](../brew-upgrade-command-assembly/SKILL.md)
  to produce the final single-line command
- **Presentation**: Outputting the command for user review (the agent
  NEVER executes it directly)

This skill does NOT duplicate command-assembly logic — all mechanical chain construction is delegated to the base primitive.

***

## 1. Layering Decision

Per the Skill Factory §2.0 protocol, this capability is **layerable**:

| Layer | Skill | Responsibility |
| :--- | :--- | :--- |
| **Composer** (this skill) | `brew-upgrade-workflow` | Brew-specific discovery, filtering, type resolution, priority |
| **Base Primitive** | [`brew-upgrade-command-assembly`](../brew-upgrade-command-assembly/SKILL.md) | Generic command-chain assembly from typed package lists |

The primitive was extracted because:

1. The command-assembly logic (env prefix, `&&` chaining,
   `--prune=all` positioning, `fetch` ordering) is entirely
   brew-version-agnostic and reusable
2. Future skills (e.g., a selective cask-only upgrade flow, or a
   pre-fetch cache warmer) can invoke the same primitive without
   duplicating assembly logic
3. Keeping deterministic assembly in a script improves testability and
   reduces prose-driven drift

***

## 2. Workflow Protocol (Tier C — Agent Judgement)

The following steps require agent judgement and MUST NOT be fully automated:

### 2.1 Gather User Intent

Ask the user to clarify:

- **Scope**: Upgrade all outdated leaves, or only specific packages?
- **Exclusions**: Any packages to skip?
- **Fetch-only**: Any packages to download without installing?
- **Priority overrides**: Any package that should go first?

### 2.2 Invoke Discovery Script

Run the Tier-A script that performs the deterministic discovery and
assembly. The script accepts the user's preferences and outputs the
final command:

```bash
python3 .agents/skills/brew-upgrade-workflow/scripts/run-brew-upgrade.py \
  [--only "pkg1,pkg2"] \
  [--exclude "pkg1,pkg2"] \
  [--fetch-only "pkg1,pkg2"] \
  [--priority "pkg1,pkg2"] \
  [--first "pkg1,pkg2"]
```

**`--first` vs `--priority`**: `--priority` controls ordering within
the formula list and cask list separately (all formulae first, then all
casks). `--first` places the listed packages first in the ENTIRE chain
regardless of type — a first-priority cask will appear before any
formulae. If `--first` is not specified, it defaults to the first entry
of `--priority` (if any), so `--priority "claude-code@latest"` also
makes claude-code@latest appear first overall.

### 2.3 Present to User

Output the command inside a markdown code block. The agent MUST NOT execute the command.

> **Critical**: `brew fetch` entries in the command are placed AFTER
> `brew cleanup --prune=all` by the base primitive. If the user edits
> the command (e.g., to reorder), they must maintain this constraint.

### 2.4 Verify Against brew-rules.md

If the output seems inconsistent with `brew-rules.md`, the agent MUST
flag it and re-run with explicit debugging (`--debug` flag on the
script).

***

## 3. CLI Contract (Stable)

Located at [`scripts/run-brew-upgrade.py`](./scripts/run-brew-upgrade.py).

```bash
python3 run-brew-upgrade.py \
  [--only "pkg1,pkg2"] \
  [--exclude "pkg1,pkg2"] \
  [--fetch-only "pkg1,pkg2"] \
  [--priority "pkg1,pkg2"] \
  [--first "pkg1,pkg2"] \
  [--outfile PATH] \
  [--log PATH] \
  [--yes] \
  [--debug]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--only` | ❌ | Comma-separated — only upgrade these packages (others are excluded) |
| `--exclude` | ❌ | Comma-separated — skip these packages |
| `--fetch-only` | ❌ | Comma-separated — download these casks without installing (excluded from upgrade chain) |
| `--priority` | ❌ | Comma-separated — order these packages first (others follow default priority) |
| `--first` | ❌ | Comma-separated — place these packages first in the chain regardless of type (defaults to first entry of --priority) |
| `--outfile` | ❌ | Write the final command to a file instead of stdout |
| `--log` | ❌ | Wrap the command in `( ... ) 2>&1 | tee -a <path>` so every subcommand's stdout+stderr is captured even if the chain short-circuits on failure (appends to an existing log) |
| `--yes` | ❌ | Prefix every brew subcommand with `yes | ` to auto-confirm interactive prompts (symlink changes, keg-only conflicts) |
| `--debug` | ❌ | Print intermediate discovery state (outdated list, leaves, type resolution) |

### Output Semantics

- **stdout** (default): A single logical line — the full executable command, ready for user review
- **`--outfile PATH`**: Same command written to the specified file (stdout is silent)
- **`--log PATH`**: The command is wrapped in `( ... ) 2>&1 | tee -a <path>` so all output flows through `tee -a` and lands in the file regardless of exit code; appends to an existing log (created if absent)
- **`--debug`**: Additional diagnostic output on stderr, including the raw brew outputs and resolution decisions
- **`--yes` + `--log`**: Compatible — use both for unattended runs with full log capture

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Success (command assembled and output) |
| 1 | No outdated leaves found (nothing to upgrade) |
| 2 | One or more `brew` commands failed |

***

## 4. Error Handling & Edge Cases

| Scenario | Handling |
| :--- | :--- |
| `brew outdated --greedy` fails | Exit code 2; stderr contains brew's error |
| No outdated packages | Exit code 1; message "No outdated leaves found" |
| Package not installed | Skipped with a warning on stderr |
| Unknown package type | Treated as cask (default); warning on stderr |
| All packages excluded | Exit code 1; message "All packages excluded" |
| Fetch-only packages also outdated | Excluded from the upgrade chain; only `brew fetch` is emitted |

***

## 5. Script Dependencies

The Python script requires:

- `python3` (stdlib only — no pip dependencies)
- Homebrew (`brew`) installed and on `PATH`
- The base primitive script at
  `../../brew-upgrade-command-assembly/scripts/assemble-brew-command.py`
  (resolved via `os.path.dirname(os.path.abspath(__file__))` from the
  orchestrator's `scripts/` directory)

***

## 6. Language Choice (Python)

Same rationale as the base primitive (`brew-upgrade-command-assembly`
§4). Python is chosen because macOS is the target platform, stdlib is
sufficient (no external dependencies), and the toolchain is consistent
with the rest of this skill family.

***

## 7. Manual Usage Examples

Upgrade all outdated leaves with standard priority:

```bash
python3 .agents/skills/brew-upgrade-workflow/scripts/run-brew-upgrade.py
```

Upgrade only specific packages, with google-chrome first:

```bash
python3 .agents/skills/brew-upgrade-workflow/scripts/run-brew-upgrade.py \
  --only "google-chrome,onedrive,firefox" \
  --priority "google-chrome"
```

Upgrade all except some, fetch others:

```bash
python3 .agents/skills/brew-upgrade-workflow/scripts/run-brew-upgrade.py \
  --exclude "warp" \
  --fetch-only "antigravity,fork"
```

Upgrade all, with a specific package first overall (ahead of all
formulae and casks), and fetch-only for stable chrome + vscode:

```bash
python3 .agents/skills/brew-upgrade-workflow/scripts/run-brew-upgrade.py \
  --priority "claude-code@latest" \
  --fetch-only "google-chrome,visual-studio-code@insiders"
```

Use explicit `--first` to override the default (which takes the first
entry of `--priority`):

```bash
python3 .agents/skills/brew-upgrade-workflow/scripts/run-brew-upgrade.py \
  --priority "google-chrome,claude-code@latest" \
  --first "claude-code@latest"
```

Attended run with full log capture (all output preserved even if a
package fails mid-chain):

```bash
python3 .agents/skills/brew-upgrade-workflow/scripts/run-brew-upgrade.py \
  --log brew.log
```

Unattended / fully automated run (auto-confirm prompts + full log):

```bash
python3 .agents/skills/brew-upgrade-workflow/scripts/run-brew-upgrade.py \
  --yes \
  --log brew.log
```

Combine with `--only` / `--exclude` / `--priority` as needed; `--log`
and `--yes` compose freely with every other flag.

***

## 8. Execution Guidance (for the User Running the Command)

The agent presents the assembled command for the user to run (see §2.3).
The user may want to capture output during execution. Three patterns:

### 8.1 Interactive: `| tee brew.log`

Shows live progress and saves a permanent log:

```bash
<assembled-command> | tee brew.log
```

To capture both stdout and stderr:

```bash
<assembled-command> 2>&1 | tee brew.log
```

On macOS, `tee` is the BSD variant — `tee --version` fails, but `tee --help` works.

### 8.2 Silent: `repo-scratch-output-capture`

For background / CI-like runs where live terminal output is unnecessary,
use the [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md)
base skill to redirect to gitignored `scratch/` files.

### 8.3 macOS Shell Portability

The generated command uses `;` (not ` && `) after the `export`
statement. Writing `export ...; && brew upgrade ...` causes a shell
parse error. See
[`general/macos-shell-portability`](../general/macos-shell-portability/SKILL.md) §5.1.

***

## 9. Related Skills

| Skill | Relationship |
| :--- | :--- |
| [`brew-upgrade-command-assembly`](../brew-upgrade-command-assembly/SKILL.md) | Base primitive — assembles the command chain from typed package lists |
| [`general/macos-shell-portability`](../general/macos-shell-portability/SKILL.md) | Reference — macOS shell differences (zsh, BSD tools, `; &&` pitfalls) for brew command execution |
| [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) | Companion — silent output capture to `scratch/` for background brew runs |

***

## 10. Traceability

- **Source**: `ai-agent-rules/brew-rules.md` Sections 3–5 (Sequential Upgrade, Default Priority, Installation Reference)
- **Industrialized via**: `rule-to-skill-industrialization` protocol (§2.4 — Tier Decomposition applied)
- **Base Primitive**: [`brew-upgrade-command-assembly`](../brew-upgrade-command-assembly/SKILL.md)
- **Brew SSOT**: `ai-agent-rules/brew-rules.md` remains the
  authoritative reference for brew operations not covered by these
  skills

## 11. Changelog

### v4 (2026-07-31)

- **`--log` appends**: `--log PATH` now wraps the chain in `( ... ) 2>&1 | tee -a <path>` —
  output is appended to an existing log (created if absent) rather than truncating it.

### v3 (2026-06-23)

- **Execution Guidance**: New §8 documents three output capture patterns for
  the user when running the assembled command: interactive `tee`, silent
  `repo-scratch-output-capture`, and combined `2>&1 | tee`.
- **Portability cross-ref**: §8.3 links to `general/macos-shell-portability` §5.1 for the `;` vs `&&` pitfall explanation.
- **Related Skills**: New §9 table links `brew-upgrade-command-assembly`, `general/macos-shell-portability`, and `repo-scratch-output-capture`.
- **Section renumbering**: §§8-10 renumbered to accommodate new sections.

### v2 (2026-06-23) [formerly §9]

- **`--first` flag added**: Packages listed via `--first` are placed first in the entire
  command chain regardless of formula/cask type. Defaults to first entry of `--priority`
  when not specified.
- **Fetch-only exclusion fix**: Packages in `--fetch-only` are now correctly excluded from
  the upgrade chain (previously they appeared in both the upgrade section and the fetch
  section).
- **Path resolution bug fix**: Corrected the assembler script path from
  `SKILL_DIR/../brew-upgrade-command-assembly/...` to
  `SKILL_DIR/../../brew-upgrade-command-assembly/...` (missing `..` level).
- **Base primitive updated**: `assemble-brew-command.py` gained `--first` CLI flag and
  `_add_pkg()` helper. See
  [brew-upgrade-command-assembly Changelog](../brew-upgrade-command-assembly/SKILL.md).
