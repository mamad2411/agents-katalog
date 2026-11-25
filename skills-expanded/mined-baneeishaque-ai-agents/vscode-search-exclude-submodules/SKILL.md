---
name: vscode-search-exclude-submodules
description: Compose the base Search-Exclude-Glob skill with `.gitmodules` parsing to emit a brace-glob that excludes every registered Git submodule from a VS Code Search-view query, without editing settings.json.
category: VSCode-Configuration
---

# VS Code Search Exclude Submodules Skill (v1)

This is a **composer** skill. It extracts every submodule path from the parent
repository's `.gitmodules` and feeds the list into the base
[VS Code Search Exclude Glob](../vscode-search-exclude-glob/SKILL.md) skill, producing a
single brace-glob the user pastes into the Search view's **"files to exclude"** input.

The skill is **session-only**. It MUST NOT modify `.vscode/settings.json`,
`*.code-workspace`, user/profile settings, `.gitignore`, or `.git/info/exclude`.

***

## 1. Scope & Intent

- **In scope**: Parse `.gitmodules` at the parent repository root, extract every
  `path = …` entry, delegate brace-glob assembly to the base skill, print the result.
- **Out of scope**:
    - Glob assembly itself (delegated to
      [VS Code Search Exclude Glob](../vscode-search-exclude-glob/SKILL.md)).
    - Persistent `search.exclude` configuration.
    - Excluding nested submodules of submodules (only the parent's `.gitmodules` is
      consulted; nested entries already live inside an excluded directory, so the
      result remains correct).

***

## 2. Environment & Dependencies

### 2.1 Required Tools

- **PowerShell** — Windows PowerShell 5.1+ or PowerShell Core 7+. Prefer
  `pwsh-preview` with `pwsh` as fallback, per the
  [Script Management Rules](../../../ai-agent-rules/script-management-rules.md).
- **`Common-Utils.ps1`** — Same shared module dot-sourced by the base skill, supplied
  by the [`powershell-scripts`](../../../ai-agent-rules/powershell-scripts/) submodule
  of `ai-agent-rules`. The submodule has nested submodules of its own, so initialize
  recursively:
  `git -C ai-agent-rules submodule update --init --recursive powershell-scripts`.
- The base skill script MUST exist at
  `.agents/skills/vscode-search-exclude-glob/scripts/generate_exclude_glob.ps1`.

### 2.2 Verification

```powershell
# Confirm pwsh-preview (preferred) or pwsh (fallback) is installed.
Get-Command pwsh-preview, pwsh -ErrorAction SilentlyContinue |
    Select-Object -First 1

# Confirm .gitmodules exists in the current directory.
if (Test-Path .gitmodules -PathType Leaf) {
    'OK: .gitmodules found'
} else {
    "FAIL: no .gitmodules at $PWD"
}

# Confirm the base skill script exists.
$base = '.agents/skills/vscode-search-exclude-glob/scripts/generate_exclude_glob.ps1'
if (Test-Path $base -PathType Leaf) { 'OK: base script present' } else { "MISSING: $base" }

# Confirm the shared utility module is materialized.
Test-Path ai-agent-rules/powershell-scripts/Common-Utils.ps1 -PathType Leaf
```

If `.gitmodules` is missing the parent repository has no submodules — this skill is
**not applicable** and VS Code's default search already stays within the repo root.

***

## 3. Protocol

### 3.1 Step 1 — Locate `.gitmodules`

The Agent MUST run the script from the **parent repository root** (the directory
containing `.gitmodules`). Paths in `.gitmodules` are recorded relative to that root,
which is exactly the search root VS Code uses.

### 3.2 Step 2 — Generate the Glob

```powershell
pwsh-preview -NoProfile -File .agents/skills/vscode-search-exclude-submodules/scripts/generate_submodule_exclude_glob.ps1
```

From inside an existing PowerShell session:

```powershell
& .agents/skills/vscode-search-exclude-submodules/scripts/generate_submodule_exclude_glob.ps1
```

The composer script:

1. Validates that `.gitmodules` exists at the supplied (or default) path.
2. Resolves the base script via a path anchored to its own location
   (`Split-Path -Parent $MyInvocation.MyCommand.Path`), independent of `cwd`.
3. Extracts every `path = …` line via a regex match in PowerShell.
4. Pipes the resulting list into the base
   `generate_exclude_glob.ps1` script, which handles sorting, deduplication, and
   brace-glob assembly.
5. Prints one line of the form `{submodule_a,submodule_b,...}/**` to stdout, then
   propagates the base script's exit code.

### 3.3 Step 3 — Apply the Filter

Follow Section 3.3 of the
[base skill](../vscode-search-exclude-glob/SKILL.md#33-step-3--apply-the-filter-in-the-search-view).

### 3.4 Step 4 — Verify Scope

Run a known query (e.g. `README.md`) and confirm no result path begins with a submodule
directory. If results still leak in, ensure the
**"Use Exclude Settings and Ignore Files"** toggle is enabled and that the glob was
pasted into **"files to exclude"** (not **"files to include"**).

***

## 4. Composition Rationale

This skill deliberately **does not** assemble the brace-glob itself. Glob assembly,
deduplication, and edge-case handling are the concerns of the base
[VS Code Search Exclude Glob](../vscode-search-exclude-glob/SKILL.md) skill.

By composing rather than duplicating:

- A bug fix in the base skill (e.g. better handling of paths with metacharacters)
  benefits every composer automatically.
- New composers (exclude `node_modules` trees, exclude `target/` build outputs,
  exclude vendored archives) reuse the same base — keeping the brace-glob format and
  determinism guarantees identical across the fleet.

This mirrors the SSOT mandate from
[AI Agent Rule Standardization Rules §4](../../../ai-agent-rules/ai-rule-standardization-rules.md):
*"documentation MUST NOT duplicate content that exists in another definitive rule
file"* — applied here at the **executable** layer.

***

## 5. Script Reference

[`scripts/generate_submodule_exclude_glob.ps1`](./scripts/generate_submodule_exclude_glob.ps1)
performs:

1. Dot-source `Common-Utils.ps1` from
   `../../../../ai-agent-rules/powershell-scripts/Common-Utils.ps1` (resolved against
   the script's own directory for portability).
2. `Test-Path -LiteralPath $GitmodulesPath -PathType Leaf` — abort with status 1 if
   missing.
3. `Resolve-Path` against the base script computed from
   `Split-Path -Parent $MyInvocation.MyCommand.Path` — abort with status 1 if missing.
4. PowerShell regex `'^\s*path\s*=\s*(.+?)\s*$'` extracts every `path = …` value.
5. Pipe into the base `generate_exclude_glob.ps1` and propagate `$LASTEXITCODE`.

### 5.1 Cmdlet & Parameter Breakdown

- `Set-StrictMode -Version Latest` — Catches typos in undeclared variables. Critical
  for the `$LASTEXITCODE` access at the bottom of the script (guarded with
  `Test-Path Variable:LASTEXITCODE`).
- `$ErrorActionPreference = 'Stop'` — Promotes file-not-found and similar errors to
  terminating exceptions for predictable exit codes.
- `Split-Path -Parent $MyInvocation.MyCommand.Path` — Resolves the directory of the
  currently-executing script regardless of how it was invoked (via `&`, `-File`, or
  dot-sourced). Required for the Layered Composition Mandate's relative base lookup.
- `Resolve-Path -LiteralPath` — Normalizes the `..\..\<base>\scripts\...` join into a
  canonical absolute path; raises a terminating error (caught above) if missing.
- `& $BaseScript` — Invokes the base script in-process so the pipeline streams without
  spawning a separate `pwsh` process. The base script's `exit N` sets `$LASTEXITCODE`.
- `Test-Path Variable:LASTEXITCODE` — Guard the read because PowerShell only sets
  `$LASTEXITCODE` after a native command (or script that called `exit`); under
  `Set-StrictMode -Version Latest`, an unguarded read of an unset variable throws.
- The base script handles sort, dedup, and brace-glob assembly — see
  [base skill §5.1](../vscode-search-exclude-glob/SKILL.md#51-cmdlet--parameter-breakdown).

***

## 6. Edge Cases & Constraints

- **Submodule paths with spaces**: `.gitmodules` allows quoted paths containing spaces.
  This composer assumes paths use `[A-Za-z0-9._\-/]` only (the conventional case).
  Quoted paths with spaces are out of scope — the base skill will refuse them.
- **Nested submodules**: Only the parent `.gitmodules` is read. Nested submodules sit
  inside a directory that is already excluded, so the result is still correct.
- **Hyphen-vs-underscore directory names**: Paths are preserved exactly as written;
  this skill MUST NOT normalize naming conventions (that is the responsibility of the
  [Lower Case Hyphen Naming](../lower-case-hyphen-naming/SKILL.md) and
  [Lower Case Underscore Naming](../lower-case-underscore-naming/SKILL.md) skills).
- **Empty `.gitmodules`**: The base script exits 1 with `no paths provided`. The
  composer surfaces this verbatim — the Agent MUST NOT emit a meaningless `{}/**`.

***

## 7. Prohibited Actions

- The Agent MUST NOT write the generated glob into `settings.json`,
  `*.code-workspace`, or any persistent configuration.
- The Agent MUST NOT modify `.gitignore` or `.git/info/exclude` as a substitute for the
  Search-view filter.
- The Agent MUST NOT maintain a hand-typed list of submodule directories — the
  composer pipeline is the SSOT and MUST be regenerated whenever `.gitmodules` changes
  (typical triggers: [Git Submodule Addition](../git-submodule-addition/SKILL.md) and
  [Git Submodule Removal](../git-submodule-removal/SKILL.md)).
- The Agent MUST NOT inline the base script's logic into this composer — composition
  through the shared base is mandatory.

***

## 8. Related Skills

- [VS Code Search Exclude Glob](../vscode-search-exclude-glob/SKILL.md) — the base
  primitive this skill composes.
- [Git Submodule Addition](../git-submodule-addition/SKILL.md) /
  [Git Submodule Removal](../git-submodule-removal/SKILL.md) — triggers for
  regeneration.
- [VS Code Settings Promotion](../vscode-settings-promotion/SKILL.md) — for the
  inverse case where the user wants a **persistent** `search.exclude` instead of an
  ad-hoc filter.
