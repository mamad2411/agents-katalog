---
name: command-autoapprove-onboarding
description: Orchestrator — given any shell command (single / chained / multi-line / script), decompose it, classify every segment via `is-this-command-safe` (extending the cheatsheet & safety-table when a binary is missing), then onboard the verdict into VS Code `chat.tools.terminal.autoApprove` via the `vscode-autoapprove-entry-consolidation` reuse-before-add algorithm.
category: VS Code Configuration
---

# Command → Auto-Approve Onboarding Skill (v1)

This skill is the **end-to-end pipeline** for taking an arbitrary shell command the user wants
auto-approved and:

1. Decomposing it into atomic segments (single command, pipeline stages, `&&`/`||`/`;` chains,
   command substitutions, here-docs, script bodies).
2. Classifying each segment via [`is-this-command-safe`](../is-this-command-safe/SKILL.md) §6.
3. **Extending the cheatsheet & safety-table** when a referenced binary is missing — per the
   skill's §8 Append-Only Protocol.
4. Onboarding the command into `chat.tools.terminal.autoApprove` via the
   [`vscode-autoapprove-entry-consolidation`](../vscode-autoapprove-entry-consolidation/SKILL.md)
   reuse-before-add algorithm (extend existing entry first; only `--add` when no existing entry
   covers the same binary or shape).

This skill **orchestrates** the three lower-level skills — it owns NO scripts of its own. All
operational primitives live in the layer below.

***

## 1. Layering Decision

Per [Skill Factory §2.0](../skill-factory/SKILL.md#20-layering-decision-base-vs-composer), this
skill is a **Composer-of-Composers**:

| Layer | Skill | Role |
| :--- | :--- | :--- |
| Base | [`is-this-command-safe`](../is-this-command-safe/SKILL.md) | Four-tier safety verdict, cheatsheet & safety-table SSOT |
| Base | [`vscode-terminal-autoapprove-audit`](../vscode-terminal-autoapprove-audit/SKILL.md) | Owns `edit-entry.py`, `find-entry.py`, `fix-indents.py` and the indentation contract |
| Composer | [`vscode-autoapprove-entry-consolidation`](../vscode-autoapprove-entry-consolidation/SKILL.md) | Reuse-before-add algorithm, extension-pattern catalogue |
| **Orchestrator** | **This skill** | **Decompose → classify → extend SSOT → onboard** |

This skill is the only place where the full lifecycle (parse the user's command → write to
`settings.json`) is automated end-to-end. Every other skill in the chain is invoked by name; none
of their operational logic is duplicated here.

***

## 2. Environment & Dependencies

| Requirement | Verification |
| :--- | :--- |
| Python 3.9+ | `python3 --version` |
| `is-this-command-safe` skill present | `ls ../is-this-command-safe/docs/safety-table.csv` |
| `vscode-terminal-autoapprove-audit` scripts present | `ls ../vscode-terminal-autoapprove-audit/scripts/` |
| `vscode-autoapprove-entry-consolidation` SKILL present | `ls ../vscode-autoapprove-entry-consolidation/SKILL.md` |
| Target `settings.json` valid | `python3 -c "import json; json.load(open('<path>'))"` |
| Regex acceptance harness present | `ls scripts/test-regex-accept.py` |

No additional dependencies. All scripts referenced are stdlib-only Python.

### 2.1 Bundled Scripts

| Script | Role |
| :--- | :--- |
| [`scripts/extract-binaries.py`](scripts/extract-binaries.py) | Bootstrap §4b Batch Mode from an existing `settings.json` (Step B1-alt) |
| [`scripts/batch-coverage-check.py`](scripts/batch-coverage-check.py) | Coverage matrix: commands × SSOT × autoApprove (Step B2) |
| [`scripts/test-regex-accept.py`](scripts/test-regex-accept.py) | Regex acceptance harness — required for §5.1 safe-chain entries, recommended for all non-trivial §5 entries; consumes [`specs/*.spec.json`](specs/) |

***

## 3. Trigger Conditions

Invoke this skill when the user says any of:

- "Auto-approve `<cmd>`"
- "Add `<cmd>` to autoApprove"
- "I keep getting approval prompts for `<cmd>` — fix it"
- Pastes a multi-line script and asks for it (or its components) to be auto-approved
- "Make `<pipeline>` not ask for permission"

The skill ALSO triggers implicitly inside any other workflow when the agent is about to issue a
command that has been refused or is about to require manual approval — onboard it once, never
fight the gate twice.

***

## 4. End-to-End Pipeline

### Step 1 — Capture the command verbatim

Record the exact command string the user wants auto-approved. Preserve quoting, redirection,
heredoc bodies. Never paraphrase.

### Step 1b — Flatten backslash-newline continuations (if any)

If the captured command spans multiple physical lines via trailing `\<newline>` continuations, first flatten it via
[`bash-multiline-to-single-line`](../bash-multiline-to-single-line/SKILL.md). The runtime
autoApprove matcher receives the command as a single string, so regex coverage analysis
and pattern construction must operate on the flattened form.

```bash
python3 .agents/skills/bash-multiline-to-single-line/scripts/bash-multiline-to-single-line.py \
  --file commands-to-onboard.bash
```

### Step 2 — Decompose into atomic segments

| Construct | Decomposition |
| :--- | :--- |
| `A \| B \| C` | Three pipeline segments: `A`, `B`, `C`. Reclassify each via [`is-this-command-safe`](../is-this-command-safe/SKILL.md) §6. |
| `A && B` / `A \|\| B` / `A ; B` | Two (or more) chain segments. Each is an independent command to classify. |
| `A $(B)` / `` A `B` `` | Outer `A` plus inner `B`. Inner is a substitution; classify both. |
| `A > FILE` / `A >> FILE` / `A \| tee FILE` | Single command `A` plus redirection target. If `FILE` is an existing file and the redirection is truncating (`>`, `tee` without `-a`), `is-this-command-safe` §4 escalates the verdict to MUTATES. |
| Heredoc body (`<<EOF`) | Treat the heredoc body as input data, NOT as a command unless the heredoc is fed into `sh`/`bash`/`python -`. If fed to an interpreter, classify the body as a script (recurse into Step 2 for each line). |
| Multi-line script / `.sh` file | Walk the script line-by-line; classify each non-blank, non-comment, non-control-flow line. Control-flow (`if`, `for`, `while`) carries no destructive weight on its own — classify the bodies. |
| Variable assignment (`X=value`) | SAFE (no command executed). |
| `eval "$X"` / `bash -c "$X"` | UNKNOWN unless `$X` resolves to a literal at audit time — refuse-pending-user-confirmation. |

### Step 3 — Classify each segment

For each atomic segment produced by Step 2, follow
[`is-this-command-safe` §6 Lookup Procedure](../is-this-command-safe/SKILL.md#6-lookup-procedure)
and emit the §5 5-line verdict template. The overall command's verdict is the **strictest** of
all segment verdicts (worst-tier wins).

### Step 4 — Extend the cheatsheet & safety-table when a binary is missing

If any segment's binary is not present in
[`is-this-command-safe/docs/safety-table.csv`](../is-this-command-safe/docs/safety-table.csv):

1. Classify the binary via its man page or `--help` output.
2. Follow [`is-this-command-safe` §8 Append-Only Protocol](../is-this-command-safe/SKILL.md#8-extending-the-allowlist-append-only-protocol):
    - Add a row to `safety-table.csv` preserving column order.
    - Add a corresponding section to `cheatsheet.md` at the alphabetical position within its category.
    - Re-emit the verdict against the new entry to confirm correctness.
3. The cheatsheet & safety-table are the SSOT — **always update them before** updating
   `settings.json`. This ensures every autoApprove entry has a paper trail in the SSOT.

### Step 5 — Build the regex key

Choose the regex shape by the strictest verdict in Step 3:

| Worst-segment verdict | Allowed in autoApprove? | Regex shape |
| :--- | :--- | :--- |
| ✅ SAFE | Yes | Anchored `/^…$/` with anti-chaining char class `[^;&\|<>$BTICK()]` on every arg slot |
| 🟡 SAFE-IF-PIPED | Yes IFF the literal pipeline composed only of SAFE downstream sinks (`head`, `grep`, `wc`); escape the literal pipe `\|` between segments | Same shape, with `\|` literal between segment regexes |
| ⚠️ HAS-DESTRUCTIVE-FLAGS | Only the SAFE form (without the destructive flag) | Build the regex around the safe flag set; explicitly exclude the destructive flag |
| ❌ MUTATES | **Only with explicit user confirmation** per [`vscode-terminal-autoapprove-audit` §11.2](../vscode-terminal-autoapprove-audit/SKILL.md#112-adding-new-entries). For `>` truncating-redirect chains specifically, the chain MUST satisfy every clause of [`is-this-command-safe` Hardcoded Tmp-Write→Read Exception Pattern](../is-this-command-safe/docs/cheatsheet.md#hardcoded-tmp-writeread-exception-pattern); otherwise refuse. | Anchored, narrow, no wildcards on the destructive flag |

The anti-chaining char class is mandatory on every arg slot to prevent
`cmd; rm -rf ~` from being approved by a regex that allowed `cmd …`.

#### Step 5.1 — Safe-Chain Entries (opt-in)

The default §5 shape forbids `;` / `&&` / `||` / `|` between segments because
unconstrained chaining lets `cmd; rm -rf ~` slip through. There are **two paths**
for auto-approving a chained one-liner whose every segment is independently SAFE —
pick by the entries' `matchCommandLine` flag, governed by
[`vscode-terminal-autoapprove-audit` §11.3](../vscode-terminal-autoapprove-audit/SKILL.md#113-matchcommandline--per-verdict-policy):

**Path A — `matchCommandLine: false` (preferred for SAFE entries).**
VS Code splits the command line on `;`, `&&`, `||`, `|` and matches each
sub-command against the entry list independently. Three atomic SAFE entries
(one per binary) auto-approve any permutation of the chain — no safe-chain
entry needed. This is the canonical recommendation per §11.3 because it
keeps the entry list minimal and inherently composable.

**Path B — `matchCommandLine: true` + safe-chain entry (when split is unwanted).**
When the entries must be `matchCommandLine: true` (e.g., `SAFE-IF-PIPED` /
`HAS-DESTRUCTIVE-FLAGS` / `MUTATES` requirements per §11.3, or because the
agent's tool inserts wrapper characters that defeat the splitter), VS Code
matches the whole line as one regex. To allow chained SAFE one-liners
without unconstrained `;`, use the **safe-chain pattern**:

```text
/^(SEG_A|SEG_B|SEG_C)(; (SEG_A|SEG_B|SEG_C))*$/
```

where each `SEG_X` is a fully anchored, anti-chaining-safe sub-pattern for
one already-classified SAFE form. The trailing `(; (…))*` permits **only**
the exact same alternation to be repeated — no other binary can be smuggled in.

Worked example for `git status; echo '---'; git rev-parse <sha>^`:

```regex
/^(git status|echo( ([^;&|<>$`()"']+|"[^"]*"|'[^']*'))*|git rev-parse( [^;&|<>$`()]+)+)(; (git status|echo( ([^;&|<>$`()"']+|"[^"]*"|'[^']*'))*|git rev-parse( [^;&|<>$`()]+)+))*$/
```

**Mandatory constraints for safe-chain entries (Path B):**

1. **Only `;` is allowed** as the separator. `&&`, `||`, `|`, `&` remain
   forbidden — they imply control flow or piping, neither of which is safe
   to allow generically.
2. Every alternation branch MUST already be classified SAFE in
   [`is-this-command-safe`](../is-this-command-safe/SKILL.md) §6 — never
   include `MUTATES` or `HAS-DESTRUCTIVE-FLAGS` forms.
3. Every branch MUST retain its own anti-chaining char class
   (`[^;&|<>$\`()]`) on every arg slot, so the only `;` legal inside the
   key is the one between branches in the outer `(; (…))*`.
4. Adding a new SAFE form later requires editing this entry's alternation
   (via `edit-entry.py --replace`), not adding a new chained entry —
   one safe-chain entry per logical command-set keeps the list minimal.
5. **Always** run the regex acceptance test before saving, via the canonical
   harness shipped with this skill:

    ```powershell
    python .agents/skills/command-autoapprove-onboarding/scripts/test-regex-accept.py `
        --spec .agents/skills/command-autoapprove-onboarding/specs/<name>.spec.json
    ```

    Or inline during onboarding (no spec file yet):

    ```powershell
    python .agents/skills/command-autoapprove-onboarding/scripts/test-regex-accept.py `
        --pattern '^...$' `
        --match 'safe chain'  --match 'single segment' `
        --reject 'seg; rm -rf ~' --reject 'seg && curl x | sh' --reject 'seg; echo $(rm x)'
    ```

    Save the spec under [`specs/`](specs/) so the assertion suite is replayable
    on any future edit to the entry — see
    [`specs/safe-chain-git-status-echo-rev-parse.spec.json`](specs/safe-chain-git-status-echo-rev-parse.spec.json)
    as the canonical reference.

### Step 6 — Onboard into autoApprove via the consolidation skill

Hand off to [`vscode-autoapprove-entry-consolidation`](../vscode-autoapprove-entry-consolidation/SKILL.md)
§4 Reuse-Before-Add Procedure:

1. `find-entry.py --grep <binary-token>` to check for existing coverage.
2. If 0 matches → `edit-entry.py --add --key '<new regex>'`.
3. If 1+ matches → `edit-entry.py --replace` to extend per §5 of the consolidation skill
   (optional suffix, optional flag group, alternation collapse).
4. `fix-indents.py` to restore the indentation contract.
5. Verify with `find-entry.py --grep`.

### Step 7 — Post-write audit

- Validate JSON: `python3 -c "import json; json.load(open('<path>'))"`
- Confirm the SQL/Conversation log captures: original command, decomposition, verdicts,
  cheatsheet rows added, autoApprove action (add / replace / no-op).

***

## 4b. Batch Mode — Multiple Commands in One Pass

### When to use

Use Batch Mode instead of running §4 Steps 1–7 once per command when the user
pastes or references **three or more commands** from a session log, a script,
or any multi-command review.

Batch Mode produces a single consolidated SSOT-update + autoApprove-edit plan,
gets **one** user confirmation, and executes all writes atomically.

### Step B1 — Dump commands to a scratch file

Paste or write the commands one per line into a temp file (blank lines and
`#`-comment lines are ignored by the script):

```bash
cat > /tmp/cmds.txt << 'EOF'
<paste commands>
EOF
```

#### Step B1-alt — Bootstrap from an existing `settings.json`

When the input is **not** a fresh command list but an existing autoApprove block you
want to audit for coverage gaps, use `extract-binaries.py` to enumerate every distinct
binary referenced across all keys:

```bash
python3 .agents/skills/command-autoapprove-onboarding/scripts/extract-binaries.py \
  --settings <path/to/settings.json> --out /tmp/cmds.txt
```

Each line of `/tmp/cmds.txt` is one `<binary> <args>` placeholder ready for
`batch-coverage-check.py`. The script is best-effort: regex alternations like
`( -v| show)?` may surface phantom binaries (e.g., `show`) — inspect the output
before feeding the next step.

### Step B2 — Run batch-coverage-check.py

```bash
python3 .agents/skills/command-autoapprove-onboarding/scripts/batch-coverage-check.py \
    --commands /tmp/cmds.txt \
    --ssot .agents/skills/is-this-command-safe/docs/safety-table.csv \
    --settings "/Users/dk/Library/Application Support/Code - Insiders/User/settings.json"

# Gaps only (skip already-COVERED rows):
python3 ... --gaps-only
```

Output columns: `BINARY | VERDICT | SSOT | AUTOAPPROVE | STATUS`

| STATUS | Meaning | Action |
| :--- | :--- | :--- |
| COVERED | In SSOT + autoApprove | None needed |
| SSOT-ONLY | In SSOT, no autoApprove entry | Step B4 → onboard to autoApprove |
| AUTOAPPROVE-ONLY | Entry exists, missing from SSOT | Step B3 → add SSOT row |
| GAP | Neither SSOT nor autoApprove | Step B3 → classify + add SSOT row; Step B4 → onboard |

Known limitations of the script:
- Inline interpreter code (`python3 -c "..."`, `bash -c "..."`) may produce token
  artifacts in the binary column — ignore any row whose BINARY contains quotes,
  parentheses, or looks like a function call.
- Complex shell command substitutions `$(...)` with embedded quotes may produce
  false positive rows — inspect and discard by eye.
- Compound SSOT keys (e.g. `git branch -a`, `git branch -vv`) are not matched
  by the subcommand-only key `git branch` — add a general `git branch` row to
  the SSOT to resolve.

### Step B3 — Consolidated SSOT update (§4 Step 4, batched)

For every unique GAP or AUTOAPPROVE-ONLY binary (deduplicated):
1. Classify the binary via man page / `--help`.
2. Append a row to `safety-table.csv` + section to `cheatsheet.md`
   (§8 Append-Only Protocol — preserve alphabetical order).

Do **all** SSOT additions in one edit pass before touching `settings.json`.

### Step B4 — Consolidated autoApprove plan (§4 Steps 5–6, batched)

For every SSOT-ONLY or GAP binary (after Step B3):
1. Determine if any existing entry can be extended (consolidation §5 reuse-before-add).
2. Produce a numbered action table:

   | # | Action | Existing entry | Proposed regex | Mechanism |
   | :--- | :--- | :--- | :--- | :--- |
   | A | Add | — | `/^…$/` | `--add` |
   | B | Extend | `[N] …` | `/^…$/` | `--replace` |

3. **Present the full table** to the user for review.
4. Do NOT execute any `edit-entry.py` calls until the user confirms.

### Step B5 — Execute + audit

1. Run `edit-entry.py` for each action (adds first, then replaces).
2. Run `fix-indents.py`.
3. JSON-validate `settings.json`.
4. Re-run `batch-coverage-check.py --gaps-only` to confirm zero unresolved rows.

### Step B6 — Commit (delegate to git-atomic-commit-construction)

Two atomic commits per the standard protocol:
- **Commit 1** (SSOT repo): `docs(is-this-command-safe): add <binaries> to safety-table and cheatsheet`
- **Commit 2** (<private-config-repo>): `chore(autoapprove): <N new entries + M extensions> for <binaries>`

***

## 5. Worked Example

**User asks:** *"Auto-approve `git --no-pager stash list | grep before-nginx-on-agents-md`"*

| Step | Action | Result |
| :--- | :--- | :--- |
| 1 | Capture | `git --no-pager stash list \| grep before-nginx-on-agents-md` |
| 2 | Decompose | Two pipeline segments: `git --no-pager stash list`, `grep before-nginx-on-agents-md` |
| 3 | Classify | `git stash list` → SSOT MISS → classify SAFE; `grep` → SAFE-IF-PIPED |
| 4 | Extend SSOT | Add `git stash list` row to `safety-table.csv` and section to `cheatsheet.md` |
| 5 | Regex shape | `/^git( --no-pager)? stash list( ARG-CLASS*)?( \| grep( -[A-Za-z]+)*( ARG-CLASS+)+)?$/` |
| 6 | Onboard | `find-entry.py --grep stash` → 0 matches → `edit-entry.py --add`. (If a `git stash list` entry already existed without the `\| grep` suffix, hand off to consolidation §5.1 to `--replace` instead.) |
| 7 | Audit | JSON valid; new entry visible at correct position; indent overrides reapplied |

***

### 5.1 Worked Example — Hardcoded Tmp-Write→Read MUTATES Exception

**User asks:** *"Auto-approve `git -C <repo> diff -- <path> > /tmp/settings_diff.txt; wc -l /tmp/settings_diff.txt && head -100 /tmp/settings_diff.txt`"*

| Step | Action | Result |
| :--- | :--- | :--- |
| 1 | Capture | Full chain preserved verbatim. |
| 2 | Decompose | Three segments via `;` and `&&`: `git diff > FILE`, `wc -l FILE`, `head -100 FILE`. |
| 3 | Classify | `git diff` SAFE; **`> /tmp/settings_diff.txt` truncating redirect upgrades to MUTATES** per §4; `wc -l`, `head` both SAFE. Worst-tier = MUTATES. |
| 4 | Extend SSOT | Add `sed` (encountered while building the broader review-pipeline catalogue) to `safety-table.csv` + `cheatsheet.md`; cross-reference the new chain into the `git diff` section under the [Hardcoded Tmp-Write→Read Exception Pattern](../is-this-command-safe/docs/cheatsheet.md#hardcoded-tmp-writeread-exception-pattern). |
| 5 | Verify exception clauses | (1) hardcoded `/tmp/settings_diff.txt`; (2) under `/tmp`; (3) downstream consumers `wc`/`head` both SAFE; (4) only `;` + `&&` separators; (5) every arg slot retains anti-chaining class. All five hold → eligible. |
| 6 | Build regex | `/^git( -C [^;&\|<>$BTICK()]+)? diff( --cached)?( -- [^;&\|<>$BTICK()]+)? > /tmp/settings_diff\.txt; wc -l /tmp/settings_diff\.txt && head( -[0-9]+)? /tmp/settings_diff\.txt$/` with `matchCommandLine: true` (full-line match mandatory because the chain crosses SAFE→MUTATES→SAFE segments). |
| 7 | Spec | Author [`specs/hardcoded-chain-git-diff-tmp-settings-diff.spec.json`](specs/hardcoded-chain-git-diff-tmp-settings-diff.spec.json) with accept + reject assertions; run `test-regex-accept.py --spec …` before saving. |
| 8 | Onboard | `find-entry.py --grep settings_diff` → 0 matches → `edit-entry.py --add` with explicit user confirmation per §7.5. |
| 9 | Audit | JSON valid; entry rejects every form not pinned to `/tmp/settings_diff.txt`. |

***

## 6. Decision Tree (Quick Reference)

```text
User asks to auto-approve a command
         │
         ▼
[ Step 2: Decompose ]
         │
         ▼
[ Step 3: Classify each segment via is-this-command-safe §6 ]
         │
         ├── Any segment UNKNOWN (binary missing from cheatsheet)?
         │      └── YES → [ Step 4: Extend cheatsheet & safety-table ]
         │
         ├── Worst verdict == MUTATES?
         │      └── YES → ask user to confirm; if no → STOP, do not onboard
         │
         ▼
[ Step 5: Build regex key with anti-chaining class on every arg slot ]
         │
         ▼
[ Step 6: Hand off to vscode-autoapprove-entry-consolidation §4 ]
         │
         ├── Existing entry covers the binary?
         │      ├── YES → --replace (extend per consolidation §5)
         │      └── NO  → --add
         │
         ▼
[ fix-indents.py → verify → done ]
```

***

## 7. Prohibited Behaviors

The agent is **BLOCKED** from:

1. Skipping Step 2 (decomposition) for chained / piped / scripted commands — every segment must
   be classified independently.
2. Adding an autoApprove entry **before** updating the cheatsheet & safety-table when a binary
   is missing from the SSOT. The SSOT is updated first; the autoApprove change is downstream.
3. Calling `edit-entry.py --add` without running the consolidation skill's §4 Step 1 reuse-check
   grep first.
4. Emitting a regex without the anti-chaining character class on every arg slot
   (the §5.1 safe-chain pattern is the **only** exception, and only for `;` —
   never `&&` / `||` / `|` / `&`).
5. Auto-approving a `MUTATES` worst-verdict command without explicit user confirmation, even if
   the user originally asked for it.
6. Auto-approving `eval` / `bash -c "$VAR"` / any dynamic-construction form — these are
   UNKNOWN by `is-this-command-safe` §6 and MUST refuse pending user confirmation.
7. Building a §5.1 safe-chain entry that includes any branch whose worst verdict is
   not SAFE — `HAS-DESTRUCTIVE-FLAGS` and `MUTATES` forms MUST NOT appear in the
   alternation, even if the user asks.

***

## 8. Verification & Markdown Hygiene

- This `SKILL.md` and its companion `AGENTS.md` MUST pass
  [Markdown Generation Rules](../../../ai-agent-rules/markdown-generation-rules.md) lint.
- All inter-skill links use **relative paths** with correct depth (`../../../` to reach
  `ai-agent-rules/` from this 3-deep skill folder; `../<skill>/SKILL.md` for siblings).
- Per [Redaction & Portability Skill](../redaction-portability/SKILL.md), every file here is
  Tier C (public/universal technical content) — no Tier A/B identifiers are present or may be
  introduced.

***

## 9. Related Skills

| Skill | Role |
| :--- | :--- |
| [`is-this-command-safe`](../is-this-command-safe/SKILL.md) | Base — four-tier verdict, cheatsheet & safety-table SSOT |
| [`vscode-terminal-autoapprove-audit`](../vscode-terminal-autoapprove-audit/SKILL.md) | Base — owns the three Python scripts and the indentation contract |
| [`vscode-autoapprove-entry-consolidation`](../vscode-autoapprove-entry-consolidation/SKILL.md) | Composer — reuse-before-add algorithm consumed by Step 6 |
| [`vscode-settings-promotion`](../vscode-settings-promotion/SKILL.md) | Promotes the consolidated setting across profiles after onboarding |
| [`skill-factory`](../skill-factory/SKILL.md) | Authored this skill per Industrial Fidelity mandates |

***

## 10. Traceability

- Originating session: end-to-end onboarding of `git --no-pager stash list | grep …` —
  produced a missing `git stash list` row in
  [`is-this-command-safe`](../is-this-command-safe/SKILL.md) and a single consolidated regex
  entry in `chat.tools.terminal.autoApprove`, demonstrating the four-skill orchestration
  (this skill → is-this-command-safe → vscode-autoapprove-entry-consolidation →
  vscode-terminal-autoapprove-audit scripts).
