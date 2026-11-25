---
name: brew-upgrade-command-assembly
description: Generic primitive for assembling Homebrew upgrade/cleanup command chains from package lists, respecting download concurrency, verbose logging, fetch-only handling, and the required brew cleanup --prune=all ordering.
category: Package-Management
---

# Brew Upgrade Command Assembly Skill (v4) — Base Primitive

Atomic, domain-agnostic primitive that assembles a Homebrew upgrade
command chain from provided package lists. The primitive handles the
mechanical assembly of:

- Sequential `upgrade && cleanup` pairs for each package (formula or cask)
- `HOMEBREW_DOWNLOAD_CONCURRENCY=1` environment export
- `--verbose` flag enforcement on every `brew` subcommand
- Fetch-only mode for specified packages (placed after final `--prune=all`)
- Final `brew cleanup --prune=all --verbose` step
- Correct omission of `--cask`/`--formula` on `brew cleanup` (positional only)
- `--first` flag: place specific packages first in the chain regardless of formula/cask type

The composer layer
([`brew-upgrade-workflow`](../brew-upgrade-workflow/SKILL.md))
owns the brew-specific discovery logic (identifying outdated leaves vs
dependencies, resolving formula vs cask types, applying priority
ordering) and invokes this primitive to produce the final command.

***

## 1. Composition Rationale

This skill is a **base primitive** — it owns ONLY the generic
command-assembly logic. It accepts package lists via CLI flags or stdin
and produces a deterministic, executable Homebrew command chain.

Composers that invoke this skill:

| Composer | Role |
| :--- | :--- |
| [`brew-upgrade-workflow`](../brew-upgrade-workflow/SKILL.md) | Discovers outdated leaves via `brew outdated --greedy` and `brew leaves --installed-on-request`, resolves formula vs cask types, applies default priority ordering, and pipes the sorted package lists into this base assembler. |

The primitive was extracted because multiple future workflows (e.g.,
selective cask upgrades, cache-pruning before fetch, dependency-aware
batching) could reuse the same command-assembly logic without
duplicating the brew-outdated-specific discovery code.

**Anti-Duplication**: If another skill needs a brew command chain, it
MUST invoke this primitive rather than re-implementing the assembly
pattern.

***

## 2. CLI Contract (Stable)

Located at [`scripts/assemble-brew-command.py`](./scripts/assemble-brew-command.py).

```bash
python3 assemble-brew-command.py \
  [--formula-names "pkg1,pkg2"] \
  [--cask-names "pkg1,pkg2"] \
  [--fetch-only "pkg1,pkg2"] \
  [--first "pkg1,pkg2"] \
  [--yes] \
  [--log PATH]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--formula-names` | ❌ | Comma-separated formula names to upgrade+cleanup |
| `--cask-names` | ❌ | Comma-separated cask names to upgrade+cleanup |
| `--fetch-only` | ❌ | Comma-separated cask names to fetch-only (appended after `--prune=all`) |
| `--first` | ❌ | Comma-separated packages to place first in the chain regardless of formula/cask type |
| `--yes` | ❌ | Prefix every `brew` subcommand with `yes | ` to auto-confirm interactive prompts |
| `--log` | ❌ | Wrap output in `( ... ) 2>&1 | tee -a <path>` so all output is captured even if the chain short-circuits on failure (appends to an existing log) |

At least one of `--formula-names`, `--cask-names`, or `--fetch-only` must be non-empty.

### Output Semantics

- Always starts with `export HOMEBREW_DOWNLOAD_CONCURRENCY=1;`
- `--first` packages are placed first in the chain (formulae first, then casks within that group)
- Each package gets a `brew upgrade --verbose --cask/--formula <pkg> && brew cleanup --verbose <pkg>` pair
- The chain is terminated by `brew cleanup --prune=all --verbose`
- `brew fetch --cask --verbose <pkg>` entries are appended AFTER the final cleanup
- Segments are joined with `;` then space after the export (standalone statement,
  exit code irrelevant), then ` && ` between all subsequent brew subcommands —
  producing a single logical line
- When `--log` is active: wraps the entire chain in `( ... ) 2>&1 | tee -a <path>`
  so every subcommand's output is captured regardless of `&&` short-circuit;
  `tee -a` appends to an existing log (created if absent)
- Trailing newline is always present

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Success (command written to stdout) |
| 1 | No packages specified (all lists empty) |

***

## 2a. Stdin Mode (Alternative Input)

If CLI flags are cumbersome (e.g., when the composer passes a long
list), the script also accepts newline-separated package entries via
stdin with type prefixes:

```bash
echo -e "formula:git\ncask:google-chrome\ncask:onedrive" | python3 assemble-brew-command.py --stdin
```

A `fetch:` prefix moves the entry into fetch-only position.
A `first:` prefix places the entry first in the chain regardless of type:

```bash
echo -e "formula:git\nfirst:google-chrome\nfetch:antigravity" | python3 assemble-brew-command.py --stdin
```

***

## 3. Generated Command Anatomy

The raw string this primitive produces follows this structure (one logical line):

```text
export HOMEBREW_DOWNLOAD_CONCURRENCY=1; brew upgrade --verbose --cask <first-cask> && brew cleanup --verbose <first-cask> && brew upgrade --verbose --formula <f1> && brew cleanup --verbose <f1> && brew upgrade --verbose --cask <c1> && brew cleanup --verbose <c1> && brew cleanup --prune=all --verbose && brew fetch --cask --verbose <fetch1>
```

**Join pattern:** The first join after `export ...` is `;` (NOT ` && `)
because the export is a standalone statement whose exit code is irrelevant.
All subsequent brew subcommands are joined with ` && `. A common mistake is
writing `export ...; && brew upgrade ...` — the `;` terminates the export,
leaving nothing for `&&` to chain to, which causes a shell parse error.
See [`general/macos-shell-portability`](../general/macos-shell-portability/SKILL.md)
§5.1 for details.

Key constraints enforced:

1. `brew cleanup` NEVER receives `--cask` or `--formula` flags (positional args only)
2. `brew fetch` always comes AFTER `brew cleanup --prune=all`
3. Every `brew` subcommand includes `--verbose`
4. `--first` packages are placed before all formulae and casks, in type groups (first-formulae then first-casks)

***

## 4. Language Choice (Python)

`ai-rule-standardization-rules.md §4` defaults to PowerShell. Python is chosen here because:

1. The skill operates on macOS (Homebrew's primary platform) where
   `python3` is universally available; PowerShell is not pre-installed.
2. Precedent: existing macOS-focused skills in this repository (e.g.,
   `bash-multiline-to-single-line`, `text-block-indent-override`) use
   Python — keeping the same toolchain reduces cognitive switching.
3. The transformation is a simple string join with no external dependencies.

***

## 5. Manual Usage Examples

Assemble a command for a single cask:

```bash
python3 .agents/skills/brew-upgrade-command-assembly/scripts/assemble-brew-command.py \
  --cask-names "google-chrome"
```

Assemble a mixed upgrade with fetch-only:

```bash
python3 .agents/skills/brew-upgrade-command-assembly/scripts/assemble-brew-command.py \
  --formula-names "git,curl" \
  --cask-names "google-chrome,onedrive" \
  --fetch-only "antigravity,fork"
```

Assemble with a first-priority package (placed before all others):

```bash
python3 .agents/skills/brew-upgrade-command-assembly/scripts/assemble-brew-command.py \
  --formula-names "gh,jq" \
  --cask-names "google-chrome,onedrive" \
  --first "claude-code@latest"
```

The output places `claude-code@latest` first in the chain, before `gh`, `jq`, and the rest.

***

## 6. Output Capture Patterns

The generated brew command chain can be long (dozens of `upgrade && cleanup`
pairs). The user typically needs to see live progress AND keep a log. Two
patterns suit this:

### 6.1 Interactive: `tee` (live progress + log file)

Pipe the entire chain through `tee` to watch output scroll while saving a permanent log:

```bash
python3 .agents/skills/brew-upgrade-command-assembly/scripts/assemble-brew-command.py \
  --formula-names "gh,jq" \
  --cask-names "google-chrome"
```

Then execute the output with `tee`:

```bash
<assembled-command> | tee brew.log
```

This shows every package's progress on the terminal AND writes a byte-for-byte
copy to `brew.log` in the working directory. On macOS, `tee` is the BSD variant
— `tee --version` fails, but `tee --help` works. See
[`general/macos-shell-portability`](../general/macos-shell-portability/SKILL.md)
§4.1.

### 6.2 Silent: `repo-scratch-output-capture` (background / unattended)

For probes, pre-flights, or CI-like runs where live output is not needed, use
the [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md)
base skill. It redirects stdout and stderr into separate files under a
gitignored `scratch/` folder co-located with the repo:

```bash
SCRATCH="$(python3 .agents/skills/repo-scratch-output-capture/scripts/ensure-scratch-gitignored.py)"
<assembled-command> > "$SCRATCH/brew-upgrade.out" 2> "$SCRATCH/brew-upgrade.err"
echo "Exit: $?  See $SCRATCH/brew-upgrade.{out,err}"
```

### 6.3 Combined (both stdout and stderr through tee)

The `tee` pattern above only captures stdout. To capture both stdout and stderr while still seeing both on the terminal:

```bash
<assembled-command> 2>&1 | tee brew.log
```

***

## 7. Related Skills

| Skill | Relationship |
| :--- | :--- |
| [`brew-upgrade-workflow`](../brew-upgrade-workflow/SKILL.md) | Composer — discovers outdated leaves and pipes sorted lists into this assembler |
| [`general/macos-shell-portability`](../general/macos-shell-portability/SKILL.md) | Reference — macOS shell differences (zsh, BSD tools, `;` vs `&&`) for brew commands |
| [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) | Companion — silent output capture to `scratch/` for background brew runs |

***

## 8. Traceability

- **Source**: `ai-agent-rules/brew-rules.md` Section 3 — Sequential Upgrade and Cleanup Workflow
- **Industrialized via**: `rule-to-skill-industrialization` protocol
- **Constraint source**: `brew-rules.md` §3.5 (fetch-after-cleanup
  ordering), §3.6 (export prefix), §1.3 (no --cask/--formula on cleanup)

## 9. Changelog

### v4 (2026-07-31)

- **`--log` appends**: The `--log` wrapper now uses `tee -a <path>` — output
  is appended to an existing log file (created if absent) instead of
  truncating it on every run.

### v3 (2026-06-23)

- **`;` vs `&&` clarification**: §3 Generated Command Anatomy now explicitly
  documents that the first join is `;` not ` && `, and warns about the common
  `export ...; &&` parse error.
- **Output capture patterns**: New §6 documents three capture patterns:
  interactive `tee`, silent `repo-scratch-output-capture`, and combined
  `2>&1 | tee`.
- **Related Skills**: New §7 table links `brew-upgrade-workflow`, `general/macos-shell-portability`, and `repo-scratch-output-capture`.
- **Portability cross-ref**: §3 links to `general/macos-shell-portability` §5.1 for the `; &&` pitfall explanation.
- **Section renumbering**: Traceability moved to §8, Changelog to §9.

### v2 (2026-06-23)

- **`--first` flag added**: Packages listed via `--first` are placed first in the command
  chain, before all formulae and casks. Internally refactored `_add_pkg()` helper extracted
  for DRY.
- **Stdin mode extended**: `first:<name>` prefix now supported alongside `formula:`, `cask:`,
  `fetch:`.
- **Consumed by**: [`brew-upgrade-workflow` v2](../brew-upgrade-workflow/SKILL.md) which
  passes `--first` from its own `--first` / `--priority` flags.
