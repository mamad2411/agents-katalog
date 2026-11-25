---
name: copilot-activity-history-split
description: Split a Microsoft / GitHub Copilot activity-history CSV export into one CSV per Conversation, sorted chronologically with the Human turn placed first on tied timestamps.
category: Data Processing
---

# Copilot Activity History Split Skill

## 1. Scope Statement

This skill defines the industrial protocol for autonomously partitioning a single
Copilot activity-history CSV export (`Conversation, Time, Author, Message`) into a
deterministic set of per-conversation CSV files. It targets users archiving their
Microsoft Copilot or GitHub Copilot chat history for offline analysis, retrieval,
or feeding into downstream LLM pipelines.

The produced files are:

- **Lossless**: every source row is preserved verbatim (multi-line quoted Message
  cells included).
- **Chronologically sorted**: rows are ordered by `Time` ascending; on identical
  timestamps the `Human` row is emitted before the `AI` row because the human always
  initiates a turn.
- **Portably named**: output filenames are slugified from the Conversation title
  (lowercase, ASCII alphanumerics only, hyphen-separated, capped at 120 chars).

***

## 2. Environment & Dependencies

Before execution, the agent MUST verify:

- **PowerShell Verification**: Ensure PowerShell is available
  (`pwsh-preview --version` preferred, `pwsh --version` fallback, Windows
  PowerShell 5.1+ acceptable). Run:

    ```bash
    pwsh-preview --version || pwsh --version
    ```

- **CSV Schema Verification**: Confirm the input file's first line is
  `Conversation,Time,Author,Message` (a UTF-8 BOM is tolerated). If the schema
  differs, the skill MUST NOT execute — coerce or remap upstream first.
- **No External Modules**: The script uses only built-in cmdlets
  (`Import-Csv`, `Group-Object`, `Sort-Object`, `Export-Csv`) — no external
  PowerShell modules or pip/npm dependencies are required.

***

## 3. Operational Logic

### 3.1 Inputs

| Parameter         | Required | Default | Purpose                                                             |
| :---------------- | :------- | :------ | :------------------------------------------------------------------ |
| `InputPath`       | Yes      | —       | Path to `copilot-activity-history.csv`.                             |
| `OutputDirectory` | Yes      | —       | Directory to receive per-conversation CSVs (created if missing).    |
| `HumanAuthor`     | No       | `Human` | Author label that wins the timestamp tiebreak (placed first).       |
| `AiAuthor`        | No       | `AI`    | Author label that loses the timestamp tiebreak (placed second).     |

### 3.2 Pipeline

1. Validate `InputPath` exists; create `OutputDirectory` if absent.
2. `Import-Csv` reads every row into typed `PSCustomObject`s, fully respecting
   RFC-4180 quoting so multi-line messages remain intact.
3. `Group-Object -Property Conversation` partitions the rows into one bucket per
   distinct Conversation value.
4. Each bucket is sorted via a two-key `Sort-Object`:
    1. Primary: `Time` ascending (ISO-8601 strings sort lexicographically and
       chronologically).
    2. Secondary: `Author` mapped to `0` (Human), `1` (AI), `2` (anything else)
       — Human always emitted first on a tie.
5. The Conversation title is slugified (`[^a-z0-9]+` collapsed to `-`, trimmed,
   lowercased, capped at 120 chars; empty results fall back to `untitled`).
6. `Export-Csv -NoTypeInformation -Encoding utf8` writes the per-conversation
   file. The header row is identical to the source schema.
7. A single summary line is printed (`Wrote N conversation CSVs to <path>`).

### 3.3 Execution

The canonical script lives next to this `SKILL.md` at
[`scripts/Split-CopilotActivityHistory.ps1`](./scripts/Split-CopilotActivityHistory.ps1).
The agent MUST resolve it through a path anchored on the script's own location
(or pass an absolute path supplied by the user) — never via `$PWD`-relative or
hard-coded absolute paths.

```bash
pwsh-preview -File <workspace-root>/.agents/skills/copilot-activity-history-split/scripts/Split-CopilotActivityHistory.ps1 \
    -InputPath <user-home>/Downloads/copilot-activity-history.csv \
    -OutputDirectory <user-home>/Downloads/copilot-conversations
```

If `pwsh-preview` is unavailable, fall back to `pwsh`:

```bash
pwsh -File ./Split-CopilotActivityHistory.ps1 -InputPath ./history.csv -OutputDirectory ./out
```

### 3.4 Deep Command Explanation Mandate

Flag-by-flag rationale for the canonical invocation above:

- `pwsh-preview` / `pwsh`: PowerShell Core entry points. `-preview` is preferred
  per the [Script Management Rules](../../../ai-agent-rules/script-management-rules.md)
  because it ships the latest fixes; `pwsh` is the documented fallback.
- `-File <path>`: Executes the named `.ps1` and exits — distinct from `-Command`,
  which would treat the argument as an inline expression and break parameter
  binding for the script's `[CmdletBinding()]` block.
- `-InputPath`: Bound by name (mandatory). Accepts absolute or relative paths;
  relative paths resolve against the caller's `cwd`, NOT the script's own
  location.
- `-OutputDirectory`: Bound by name (mandatory). The script creates the
  directory tree if missing via `New-Item -ItemType Directory -Force`.
- `-HumanAuthor` / `-AiAuthor` (optional): Override the author labels when the
  export uses non-default values (e.g., a user-renamed agent).

Inside the script:

- `Set-StrictMode -Version Latest` + `$ErrorActionPreference = 'Stop'`: Convert
  unhandled errors and uninitialized variables into terminating failures so the
  caller gets a non-zero exit code instead of a silently truncated split.
- `Import-Csv -LiteralPath`: `-LiteralPath` is critical because Conversation
  exports often live in cloud-storage paths containing `[`/`]` which PowerShell
  would otherwise treat as wildcard metacharacters.
- `Sort-Object -Property @{ Expression = 'Time'; Ascending = $true }, @{ ... }`:
  The hashtable form lets a single `Sort-Object` call apply two sort keys with
  per-key direction control, avoiding a brittle two-pass sort.
- `Export-Csv -NoTypeInformation -Encoding utf8`: `-NoTypeInformation` strips
  the legacy `#TYPE` header line so the output round-trips through `Import-Csv`
  cleanly; `-Encoding utf8` matches the source export.

***

## 4. Layered Composition Rationale

This skill is intentionally **atomic**, not layered. The "split a CSV by a column
value" primitive is generic, but the additional behaviour required here — the
Human-before-AI tiebreak on identical timestamps and the chat-conversation
slugification policy — is domain-specific to Copilot activity exports. A future
generic `csv-split-by-column` base skill could be extracted if a second composer
emerges; at that point this skill MUST be refactored to delegate via a relative
path per the [skill-factory section 2.0 Layering Decision](../skill-factory/SKILL.md)
mandate.

***

## 5. Prohibited Behaviors

- **DO NOT** mutate the source CSV in place — always write to a separate
  `OutputDirectory`.
- **DO NOT** emit non-UTF-8 output files; the activity export commonly contains
  multibyte characters (emoji, RTL scripts) that other encodings will mangle.
- **DO NOT** use `-Path` instead of `-LiteralPath` for any file argument — the
  cloud-storage paths typical for these exports contain wildcard metacharacters
  that `-Path` will misinterpret.
- **DO NOT** invent alternative slug rules — file consumers depend on the
  documented `[^a-z0-9]+` → `-` collapse for stable cross-run lookups.
- **DO NOT** inline this skill's logic into another skill; reference it via
  relative link instead, per the SSOT mandate.

***

## 6. Verification Checklist

After execution, the agent MUST confirm:

1. **Row Conservation**:
   `(Get-ChildItem $OutputDirectory -Filter *.csv | ForEach-Object { (Import-Csv $_.FullName).Count } | Measure-Object -Sum).Sum`
   equals `(Import-Csv $InputPath).Count`. Any drift indicates a parser failure
   on a multi-line quoted message and the run MUST be re-investigated.
2. **File Count**: Number of files in `OutputDirectory` equals the distinct
   Conversation count from
   `(Import-Csv $InputPath | Group-Object Conversation).Count`.
3. **Sort Invariant**: For at least one sampled file, the `Time` column is
   monotonically non-decreasing and any tie places `Human` before `AI`.

***

## 7. Related Skills

- **[skill-factory](../skill-factory/SKILL.md)** — the meta-skill that produced
  this one; it defines the layering and registration mandates referenced above.
- **[lower-case-hyphen-naming](../lower-case-hyphen-naming/SKILL.md)** — the
  general filename-hygiene SSOT this skill's slug rule conforms to.
