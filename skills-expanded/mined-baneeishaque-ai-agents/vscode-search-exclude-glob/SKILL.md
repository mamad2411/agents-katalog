---
name: vscode-search-exclude-glob
description: Generate a single brace-glob expression for the VS Code Search view's "files to exclude" field from any user-supplied list of paths, without modifying settings.json.
category: VSCode-Configuration
---

# VS Code Search Exclude Glob Skill (v1)

This is the **base** skill. It converts an arbitrary list of repository-relative paths
(directories and/or files) into a single brace-glob string suitable for the VS Code
Search view's **"files to exclude"** input field.

The skill is **session-only**. It MUST NOT write to `.vscode/settings.json`,
`*.code-workspace`, user/profile settings, or any persistent configuration tier.

This skill is intended to be **composed by higher-level skills** (e.g. submodule
exclusion, build-output exclusion, vendor-folder exclusion) that produce path lists from
a domain-specific source.

***

## 1. Scope & Intent

- **In scope**: Take an arbitrary list of paths (one per line, on stdin or in a file)
  and emit one brace-glob line:
    - `{path_a,path_b,path_c}/**` when all entries are directories.
    - A comma-joined list of literal globs when entries mix files and directories.
- **Out of scope**:
    - Discovering paths (delegated to consumer skills).
    - Writing the result anywhere — the Agent prints it; the user pastes it.
    - Any persistent VS Code settings mutation.

***

## 2. Environment & Dependencies

### 2.1 Required Tools

- **VS Code** 1.60+ — Search view "files to exclude" accepts brace-glob syntax.
- **PowerShell** — Windows PowerShell 5.1+ **or** PowerShell Core 7+. Execute via
  `pwsh-preview` (preferred) with `pwsh` as fallback, per the project's
  [Script Management Rules](../../../ai-agent-rules/script-management-rules.md).
- **`Common-Utils.ps1`** — Shared utility module dot-sourced from the
  [`powershell-scripts`](../../../ai-agent-rules/powershell-scripts/) submodule of
  `ai-agent-rules`. Provides the cross-platform `Write-Message` helper used for
  diagnostics. The submodule itself contains nested submodules, so initialization MUST
  always be recursive:

    ```bash
    git -C ai-agent-rules submodule update --init --recursive powershell-scripts
    ```

### 2.2 Verification

```powershell
# macOS / Linux / Windows: prefer pwsh-preview, fall back to pwsh.
if (Get-Command pwsh-preview -ErrorAction SilentlyContinue) {
    pwsh-preview -NoProfile -Command '$PSVersionTable.PSVersion'
} elseif (Get-Command pwsh -ErrorAction SilentlyContinue) {
    pwsh -NoProfile -Command '$PSVersionTable.PSVersion'
} else {
    Write-Error 'PowerShell not installed. See system-wide-tool-management skill.'
}

# Confirm the Common-Utils.ps1 dependency is materialized.
Test-Path ai-agent-rules/powershell-scripts/Common-Utils.ps1 -PathType Leaf
```

If neither executable is on `PATH`, follow the
[System-Wide Tool Management](../system-wide-tool-management/SKILL.md) skill to install
PowerShell Core. If `Common-Utils.ps1` is missing, initialize the submodule via the
command above.

***

## 3. Protocol

### 3.1 Step 1 — Acquire the Path List

The Agent MUST obtain a list of paths from one of:

1. **Pipeline input** — piped from another script or command (`'a','b' | ./script.ps1`).
2. **A file** — passed via the `-Path` parameter.
3. **An interactive prompt** — only when the user runs the skill manually with no input.

Paths MUST be **relative to the search root** (the workspace folder VS Code is searching
in). Absolute paths and paths beginning with `./` (or `.\` on Windows) MUST be
normalized (the script strips a leading `./` or `.\`).

### 3.2 Step 2 — Generate the Glob

Run:

```powershell
# From the pipeline
@('dir_a','dir_b','dir_c') |
    pwsh-preview -NoProfile -File .agents/skills/vscode-search-exclude-glob/scripts/generate_exclude_glob.ps1

# From a file
pwsh-preview -NoProfile -File .agents/skills/vscode-search-exclude-glob/scripts/generate_exclude_glob.ps1 -Path paths.txt
```

From inside an existing PowerShell session (no separate process):

```powershell
'dir_a','dir_b','dir_c' |
    & .agents/skills/vscode-search-exclude-glob/scripts/generate_exclude_glob.ps1
```

The script emits **one line** to stdout:

```text
{path_a,path_b,...,path_z}/**
```

A single-path input emits a literal glob (no braces), since brace expansion of one
element is wasteful:

```text
path_a/**
```

### 3.3 Step 3 — Apply the Filter in the Search View

1. Open the Search view (`Cmd+Shift+F` on macOS, `Ctrl+Shift+F` on Linux/Windows).
2. Expand the "…" toggle to reveal **"files to include"** / **"files to exclude"**.
3. Paste the generated glob into **"files to exclude"**.
4. Keep the **"Use Exclude Settings and Ignore Files"** toggle (open-book icon)
   **enabled** so this glob composes additively with `.gitignore` and `search.exclude`.

### 3.4 Step 4 — Verify

Run a query that is known to occur both inside and outside the excluded paths. The
result list MUST contain only matches from outside.

***

## 4. Brace-Glob Syntax (Pedagogical)

VS Code search uses `vscode-ripgrep` glob semantics:

| Token | Meaning |
| :--- | :--- |
| `{a,b,c}` | Brace expansion — matches `a`, `b`, or `c`. Equivalent to three OR'd globs. |
| `/**` | Recursive — every file inside the chosen directory at any depth. |
| `*.ext` | Single-segment file glob — matches `foo.ext` at the current depth only. |
| `**/*.ext` | Multi-segment file glob — matches `foo.ext` at any depth. |

**Why a single brace-glob instead of comma-separated entries?**

VS Code accepts either form, but a single brace expression keeps the Search input
compact, avoids per-glob parsing overhead, and survives copy-paste through clipboard or
chat tools that aggressively normalize whitespace.

**Why `/**` and not just the directory name?**

Without `/**`, VS Code may exclude the directory entry itself but still descend into its
contents in some edge cases (file-vs-directory glob ambiguity). The trailing `/**` makes
recursive intent explicit.

***

## 5. Script Reference

[`scripts/generate_exclude_glob.ps1`](./scripts/generate_exclude_glob.ps1) performs:

1. Dot-source `Common-Utils.ps1` from
   `../../../../ai-agent-rules/powershell-scripts/Common-Utils.ps1` (resolved against
   the script's own directory for portability).
2. Read paths from the pipeline (`-InputObject`) or `-Path` file.
3. Trim each line, strip an optional leading `./` or `.\`.
4. Drop blank lines and comment lines (`#…`).
5. Sort lexically with `Sort-Object -CaseSensitive -Unique` (deterministic, locale-safe).
6. Detect entries that already contain a glob metacharacter (`*`, `?`, `[`, `{`) and
   preserve them verbatim; append `/**` to the rest.
7. Emit `path/**` (single entry), `{p1,p2,…}/**` (multi entry, all directories), or
   `{p1,p2,…}` (mixed entries where some already carry a glob).

### 5.1 Cmdlet & Parameter Breakdown

- `[CmdletBinding()]` + `param(...)` — Standard PowerShell advanced-function pattern.
  Enables common parameters (`-Verbose`, `-ErrorAction`, etc.) and pipeline binding.
- `Set-StrictMode -Version Latest` — Refuses access to undeclared variables, catching
  typos at runtime. Mandatory for cross-version safety on Windows PowerShell 5.1.
- `$ErrorActionPreference = 'Stop'` — Promotes non-terminating errors (e.g., file I/O
  failures) to terminating ones, so `try/catch` and exit codes behave consistently.
- `[Parameter(ValueFromPipeline = $true)]` — Binds pipeline input to `$InputObject`.
  Combined with `begin`/`process`/`end` blocks, accumulates streamed input across
  invocations.
- `Get-Content -LiteralPath` — Reads file content without glob-interpreting the path.
  Critical when paths contain `[` or `]`.
- `Sort-Object -CaseSensitive -Unique` — Determinism guarantee. Without `-CaseSensitive`,
  `Sort-Object` uses culture-aware string comparison, which can reorder entries
  differently on systems with non-default `LC_COLLATE`.
- `Write-Message -Message ... -Color 'Red'` — Cross-platform diagnostic helper from the
  shared `Common-Utils.ps1` module. Routes through `Write-Host`, which writes to the
  Information stream and therefore does NOT pollute the success stream that callers
  pipe (verified end-to-end). Each call is guarded with the project-mandated
  `[string]::IsNullOrWhiteSpace` check from the
  [Script Management Rules](../../../ai-agent-rules/script-management-rules.md).
- `exit 1` — Sets the script's exit code so callers (including the composer script and
  shell pipelines) can detect failure via `$LASTEXITCODE` / `$?`.

***

## 6. Edge Cases & Constraints

- **Empty input**: The script exits with status 1 and prints
  `no paths provided` on stderr. Consumer skills MUST surface this verbatim instead of
  emitting a meaningless `{}/**`.
- **Paths with spaces**: Out of scope. Brace expansion in `vscode-ripgrep` does not
  reliably escape embedded spaces. The script does not quote them and will produce an
  incorrect glob — the Agent MUST refuse and ask the user for an alternative path list.
- **Mixed files + directories**: If an entry already contains a glob character
  (`*`, `?`, `[`, `{`), it is preserved verbatim instead of having `/**` appended. This
  lets consumers pass file globs like `**/*.snap` alongside directory names.
- **Single-entry input**: The output omits the braces (`path/**`) since one-element
  brace expansion is wasteful and visually noisy.

***

## 7. Prohibited Actions

- The Agent MUST NOT write the generated glob into `settings.json`, `*.code-workspace`,
  or any other persistent configuration.
- The Agent MUST NOT manually hand-author the glob — the script is the SSOT and MUST be
  used so consumers stay reproducible.
- The Agent MUST NOT silently drop entries with spaces or shell metacharacters; refuse
  and surface the offending lines.

***

## 8. Composition by Higher-Level Skills

This skill is the **base layer**. Composers feed their domain-specific path discovery
into the script's pipeline:

| Composer Skill | Path Source |
| :--- | :--- |
| [VS Code Search Exclude Submodules](../vscode-search-exclude-submodules/SKILL.md) | `path = …` lines from `.gitmodules` |

New composers (e.g. exclude `node_modules` trees, exclude all build outputs registered
in `.gitignore`) MUST reuse this base script rather than reinventing glob assembly.
Composer scripts MUST resolve this base script via a relative path anchored to their
own location (`Split-Path -Parent $MyInvocation.MyCommand.Path`) so the pipeline works
regardless of the caller's current working directory — see the
[Layered Composition Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md)
for the project-wide rule.
