---
name: is-this-command-safe
description: Pre-execution safety verdict protocol for shell commands — classify as SAFE, SAFE-IF-PIPED, HAS-DESTRUCTIVE-FLAGS, or MUTATES, with destructive-flag and dangerous-pipeline detection.
category: Core Agent Behavior
---

# Is This Command Safe Skill

This skill defines the protocol the agent (and the user) MUST use to vet any shell command **before**
execution. It exists to terminate the recurring "is `<command>` safe?" question with a deterministic,
auditable verdict instead of a fresh free-form essay each time.

The skill is the SSOT for:

1. The **four-tier safety classification** (SAFE / SAFE-IF-PIPED / HAS-DESTRUCTIVE-FLAGS / MUTATES).
2. The **destructive-flag inventory** for common read-only-by-default tools (`find`, `grep`, `git`, `sed`, …).
3. The **dangerous-pipeline catalogue** (`| xargs rm`, `| sh`, `>` over existing files, `tee` overwrite, …).
4. The **command allowlist cheatsheet** at [`docs/cheatsheet.md`](./docs/cheatsheet.md) and its
   machine-readable mirror [`docs/safety-table.csv`](./docs/safety-table.csv).
5. The **mandated verdict template** the agent emits (kept short and structured — no fresh prose per call).

Cross-reference: this skill is the operational complement to
[`ai-agent-rules/shell-execution-rules.md`](../../../ai-agent-rules/shell-execution-rules.md) §1
("Prioritize Safety and Non-Destructive Actions"). Where shell-execution-rules states the principle,
this skill provides the lookup table and verdict procedure.

***

## 1. Layering Decision (Atomic, with Future Composers)

Per [Skill Factory §2.0](../skill-factory/SKILL.md#20-layering-decision-base-vs-composer), the
verdict-lookup capability is currently **Atomic** — the cheatsheet, classification, and verdict
template form one indivisible workflow at v1.

Anticipated future composers (not yet built) MUST consume this skill rather than reinvent the lookup:

- **agent-execution-pre-flight-check** — intercepts every agent-issued shell command, pipes the
  command string into this skill, and refuses to execute on a `MUTATES` verdict without explicit
  user confirmation.
- **vscode-task-allowlist-generator** — filters this skill's safety table to `SAFE` rows and emits
  a VS Code `tasks.json` allowlist for autonomous agent execution.

When such composers are built, this skill MUST be promoted to **Base** status and gain a
`Composition by Higher-Level Skills` section per the Skill Factory mandate.

***

## 2. Environment & Dependencies

This is a doc-only protocol skill at v1 — **no runtime dependencies are required to consult the
cheatsheet**. The agent MUST be able to:

1. Read [`docs/cheatsheet.md`](./docs/cheatsheet.md) — plain Markdown, any Markdown viewer.
2. Parse [`docs/safety-table.csv`](./docs/safety-table.csv) — plain CSV, any CSV reader (e.g.,
   PowerShell `Import-Csv`, Python `csv` module, `awk`).

If a future composer ships a PowerShell lookup script (e.g., `Get-CommandSafety.ps1`), it MUST follow
the [Script Authoring Mandates](../skill-factory/SKILL.md#221-script-authoring-mandates) —
PowerShell-first, `Common-Utils.ps1` dot-source, anchored paths, `pwsh-preview` → `pwsh` fallback.

***

## 3. Safety Classification (Four Tiers)

Every command MUST receive **exactly one** classification. The classification is a property of the
**full command line as written**, not just the binary — `grep` is `SAFE` but
`grep -rl X . | xargs rm` is `MUTATES`.

| Tier | Symbol | Meaning | Default action |
| :--- | :--- | :--- | :--- |
| `SAFE` | ✅ | Read-only by itself; no flag combination of this binary alone can mutate the filesystem. Examples: `cat`, `head`, `tail`, `wc`, `less`, `lsof`, `mdls`, `git status`, `git log`, `git diff`. | Execute without confirmation. |
| `SAFE-IF-PIPED` | 🟡 | Read-only by itself, but commonly composed with a downstream destructive command via `\|`, `xargs`, `$()`, or backticks. Examples: `find` (without `-delete`/`-exec`), `grep`, `mdfind`, `git ls-tree`. | Execute the upstream command alone; refuse the full pipeline if downstream is `MUTATES` without explicit user confirmation. |
| `HAS-DESTRUCTIVE-FLAGS` | ⚠️ | The same binary is `SAFE` with one flag set and `MUTATES` with another. The verdict depends on the exact flags supplied. Examples: `find -delete`, `git push --force`, `git reset --hard`, `sed -i`, `rsync --delete`. | Inspect the flags actually present; confirm before executing the destructive form. |
| `MUTATES` | ❌ | Always changes filesystem, repository, or remote state. Examples: `rm`, `mv`, `mkdir`, `git commit`, `git push`, `git rebase`, `npm install`, `brew install`. | Require explicit user confirmation. Prefer a dry-run (`--dry-run`, `-n`, `echo` substitution) first. |

***

## 4. Destructive Flag Inventory (Non-Exhaustive, Authoritative)

The agent MUST treat the following flag/argument combinations as **automatic upgrade to MUTATES**
regardless of the binary's default classification:

| Binary | Destructive form | Effect |
| :--- | :--- | :--- |
| `find` | `-delete` | Deletes every match. |
| `find` | `-exec rm …` / `-exec mv …` / `-exec sed -i …` | Executes the destructive command per match. |
| `grep` (downstream) | `\| xargs rm` / `\| xargs sed -i` | Pipeline mutates files containing the pattern. |
| `sed` | `-i` (or `-i ''` on macOS) | In-place edit. |
| `git` | `push --force` / `push -f` / `push --force-with-lease` | Rewrites remote history. |
| `git` | `reset --hard` | Destroys uncommitted changes. |
| `git` | `clean -fd` / `clean -fdx` | Deletes untracked files (and ignored with `-x`). |
| `git` | `rebase` (any form) | Rewrites local history. |
| `git` | `branch -D` / `branch -d` | Deletes branches. |
| `git` | `checkout -- <path>` / `restore <path>` | Discards working-tree changes. |
| `rsync` | `--delete` / `--delete-after` / `--delete-during` | Deletes files on destination not present on source. |
| `tar` | `--delete` | Removes members from archive. |
| `xargs` | (any) when downstream is destructive | Inherits downstream destructiveness. |
| Redirection | `>` over existing file | Truncates the target file. |
| Redirection | `tee <existing-file>` (without `-a`) | Truncates the target file. |
| Process substitution | `$(rm …)`, `` `rm …` `` | Executes embedded mutation. |

When ANY of these patterns appears in the command line, the verdict is **MUTATES** even if the
host binary is `SAFE` or `SAFE-IF-PIPED`.

**Narrow documented exception**: the
[Hardcoded Tmp-Write→Read Exception Pattern](./docs/cheatsheet.md#hardcoded-tmp-writeread-exception-pattern)
defines the ONLY class of chains where a `>` truncating redirect may keep an
overall SAFE verdict. Every clause of that section MUST hold; otherwise the
verdict remains `MUTATES`. New occurrences MUST be added by extending the
pattern's catalogue table (with a corresponding per-binary `EXCEPTION` block
that links back), never by inventing a new exception class inline.

***

## 5. Verdict Template (Mandated Output Format)

The agent MUST emit verdicts in **exactly** this 5-line format. No prose preamble, no upsell question.

```text
Command   : <verbatim command>
Verdict   : <SAFE | SAFE-IF-PIPED | HAS-DESTRUCTIVE-FLAGS | MUTATES>
Reason    : <one-line justification — cite the cheatsheet row OR the destructive flag matched>
Safe form : <if HAS-DESTRUCTIVE-FLAGS or MUTATES: the dry-run / preview equivalent; else "n/a">
Action    : <Execute | Execute-with-care | Refuse-pending-user-confirmation>
```

The 4-section AI essay template (`✅ What it does / ⚠️ When destructive / 🛡️ Safety tips /
✅ Bottom line`) historically used in chat is **deprecated for this skill**. It is verbose,
repetitive across calls, and produces no reusable artifact. The 5-line verdict above is the SSOT.

If the user explicitly requests the long-form explanation (e.g., "explain why"), the agent MAY
expand into the legacy 4-section essay AFTER the 5-line verdict — never instead of it.

***

## 6. Lookup Procedure

For every command-safety query the agent MUST execute:

1. **Tokenize** the command line into `binary`, `flags[]`, `positional[]`, `pipeline_segments[]`,
   `redirections[]`, `substitutions[]`.
2. **Cheatsheet lookup**: locate the `binary` row in [`docs/safety-table.csv`](./docs/safety-table.csv).
   If absent, verdict is **UNKNOWN — refuse pending user confirmation**; propose adding the binary
   via §8.
3. **Flag scan**: walk `flags[]` against §4. Any match upgrades the verdict to `MUTATES`.
4. **Pipeline scan**: for each `pipeline_segments[i]` where `i > 0`, recursively classify and
   upgrade per §4 (downstream destructive ⇒ whole pipeline `MUTATES`).
5. **Redirection scan**: any `>` or `tee` without `-a` to an existing file ⇒ `MUTATES`.
6. **Substitution scan**: recursively classify any `$(…)` / backtick body.
7. **Emit verdict** using the §5 template.

***

## 7. Allowlist Cheatsheet

The complete, curated allowlist lives at [`docs/cheatsheet.md`](./docs/cheatsheet.md) (human-readable)
and [`docs/safety-table.csv`](./docs/safety-table.csv) (machine-readable). It covers the inspection
toolkit a cautious developer or AI-agent supervisor wants whitelisted, sourced from the originating
vetting thread (23 commands over 36 days — see §12):

- **File search & metadata**: `find`, `mdfind`, `mdls`
- **Text search**: `grep`
- **File viewing**: `cat`, `head`, `tail`, `less`, `wc`
- **Diffing**: `diff`, `git diff`
- **Git read-only inspection**: `git status`, `git log`, `git ls-tree`, `git branch -a`,
  `git branch -vv`, `git merge-base`, `git check-ignore`, `git show`
- **System/process inspection**: `lsof`, `command -v`
- **Media metadata**: `ffprobe`
- **Python verification**: `python3 -m py_compile`
- **NPM read-only**: `npm root`, `npm search`, `npm view`
- **DB read-only**: `pg_restore --list`
- **Line-oriented extraction**: `cut`, `sed -n`
- **Brew inventory**: `brew list`, `brew outdated`, `brew leaves`
- **Directory navigation**: `cd`, `readlink`, `du`
- **Linters**: `markdownlint-cli2`
- **Filesystem mutation (explicit, for contrast)**: `mkdir`
- **Non-CLI tokens**: `agy` — Google Antigravity IDE-embedded agent, not a shell binary;
  no applicable shell verdict.

***

## 8. Extending the Allowlist (Append-Only Protocol)

When a new binary is encountered, the agent MUST:

1. Add a row to [`docs/safety-table.csv`](./docs/safety-table.csv) preserving column order
   (`binary,verdict,destructive_flags,safe_alternative,notes`).
2. Add a corresponding section to [`docs/cheatsheet.md`](./docs/cheatsheet.md) at the correct
   alphabetical position within its category.
3. Re-emit the §5 verdict against the new entry to confirm the row is correct.
4. **Preservation Mandate**: existing entries MUST NOT be removed unless proven duplicate
   (per [AI Rule Standardization §4](../../../ai-agent-rules/ai-rule-standardization-rules.md)).

***

## 9. Prohibited Behaviors

The agent is **BLOCKED** from:

1. Executing a `MUTATES` command without explicit user confirmation in the same conversation turn.
2. Substituting the legacy 4-section essay template for the §5 5-line verdict.
3. Inventing a verdict for an `UNKNOWN` binary — the only correct action is to refuse and request
   the user confirm or add the binary via §8.
4. Stripping or summarizing the §4 destructive-flag inventory — it is the SSOT.
5. Trusting "safe by default" claims from a man page without applying the §6 procedure to the
   **exact command line** the user pasted.

***

## 10. Verification & Markdown Hygiene

- This `SKILL.md`, its companion `AGENTS.md`, the cheatsheet, and the conversation log MUST pass
  [Markdown Generation Rules](../../../ai-agent-rules/markdown-generation-rules.md) lint.
- The CSV MUST round-trip through `Import-Csv` / `csv.DictReader` without warnings.
- All links use **relative paths** with correct depth (`../../../` to reach `ai-agent-rules/`
  from this 3-deep skill folder).
- Per [Redaction & Portability Skill](../redaction-portability/SKILL.md), every file here is
  Tier C (public/universal technical content) — no Tier A/B identifiers are present or may be
  introduced.

***

## 11. Related Skills

- [Skill Factory](../skill-factory/SKILL.md) — produced this skill.
- [Redaction & Portability](../redaction-portability/SKILL.md) — sanitisation contract for
  `docs/conversations/`.
- Anticipated future composers: `agent-execution-pre-flight-check`,
  `vscode-task-allowlist-generator` (see §1).
- [`command-autoapprove-onboarding`](../command-autoapprove-onboarding/SKILL.md) —
  Orchestrator that consumes this skill's verdicts and SSOT files to onboard
  commands into VS Code autoApprove.

***

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| [`opencode-permission-config`](../opencode-permission-config/SKILL.md) | Reads `docs/safety-table.csv` (safety classifications) to derive `opencode.json` bash permission patterns. Consumes SAFE / SAFE-WITH-QUALIFICATION / MUTATES verdicts from §3 (Four-Tier system) and applies opencode-specific pattern-design logic (bare vs. wildcard, git safe-forms-only, git -C multi-repo, SAFE-IF-PIPED tradeoffs). Does NOT re-implement classification — delegates every verdict to this skill's safety table. See its §6 Pattern Design Decisions for the mapping rules. |
| [`command-autoapprove-onboarding`](../command-autoapprove-onboarding/SKILL.md) | Consumes `docs/safety-table.csv` and `docs/cheatsheet.md` to vet and onboard shell commands into VS Code `chat.tools.terminal.autoApprove`. Applies `is-this-command-safe`'s classification tiers (SAFE / SAFE-IF-PIPED / HAS-DESTRUCTIVE-FLAGS / MUTATES) for every binary and pipeline segment. Extends the safety-table with new entries when encountering unknown binaries during audit. |

***

## 12. Related Conversations & Traceability

- [`docs/conversations/2026-01-30-shell-command-safety-vetting.md`](./docs/conversations/2026-01-30-shell-command-safety-vetting.md)
  — originating multi-day vetting thread (23 commands, 36 days, Jan 30 – Mar 7 2026) that
  motivated this skill, sanitized per the Redaction & Portability protocol.
