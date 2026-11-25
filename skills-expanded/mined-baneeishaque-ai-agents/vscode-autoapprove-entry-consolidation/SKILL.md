---
name: vscode-autoapprove-entry-consolidation
description: Composer — minimize the `chat.tools.terminal.autoApprove` entry list by extending existing anchored regex patterns (optional suffix, optional flag group, alternation collapse) before adding new ones; reuses the `vscode-terminal-autoapprove-audit` scripts.
category: VS Code Configuration
---

# VS Code Auto-Approve Entry Consolidation Skill (v1)

This skill governs the **"reuse before add"** discipline for `chat.tools.terminal.autoApprove` in
VS Code `settings.json`. Whenever a new command needs auto-approving (or a periodic cleanup is run),
the agent MUST first try to extend an existing entry; only when no existing entry covers the same
binary may a new entry be added.

This skill is the operational sibling to
[`vscode-terminal-autoapprove-audit`](../vscode-terminal-autoapprove-audit/SKILL.md) §11.1 — the
audit skill encodes the rule, and this skill encodes the **algorithm + extension catalogue**.

***

## 1. Layering Decision

Per [Skill Factory §2.0](../skill-factory/SKILL.md#20-layering-decision-base-vs-composer), this
skill is a **Composer** over `vscode-terminal-autoapprove-audit`:

- The base (`vscode-terminal-autoapprove-audit`) owns the scripts (`edit-entry.py`,
  `find-entry.py`, `fix-indents.py`), the indentation contract (§3.1), and the full audit
  lifecycle (initial review, dead-weight detection, secret scanning).
- This composer owns ONLY the **consolidation algorithm**: the extension-pattern catalogue, the
  reuse-check procedure, and the collapse heuristics.

It consumes (does not duplicate):

| Skill | Role |
| :--- | :--- |
| [`vscode-terminal-autoapprove-audit`](../vscode-terminal-autoapprove-audit/SKILL.md) | Owns scripts and full audit workflow |
| [`is-this-command-safe`](../is-this-command-safe/SKILL.md) | SSOT for four-tier safety verdicts |

***

## 2. Environment & Dependencies

| Requirement | Verification |
| :--- | :--- |
| Python 3.9+ | `python3 --version` |
| Valid `settings.json` | `python3 -c "import json; json.load(open('<path>'))"` |
| Base scripts present | `ls .agents/skills/vscode-terminal-autoapprove-audit/scripts/` |

No additional pip packages required. All scripts referenced are the base skill's stdlib-only Python
helpers, invoked through their absolute-from-workspace-root path.

***

## 3. Trigger Conditions

Invoke this skill when:

1. A new command needs auto-approving (i.e., before any `edit-entry.py --add`).
2. A periodic cleanup of the autoApprove list is requested.
3. The list grows past ~20 entries and looks like it contains near-duplicates.
4. The user notices two entries that differ only in a suffix, a flag, or a binary alternation.

***

## 4. Reuse-Before-Add Procedure (Primary Workflow)

Before any `--add`, the agent MUST execute the following procedure:

### Step 1 — Search for an existing entry covering the same binary or tool

```bash
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/find-entry.py \
  --settings <path/to/settings.json> --grep '<binary-or-tool-token>'
```

Examples of the `--grep` token:

- For a new `git stash list …` command → grep `stash`
- For a new `… | head -N` form → grep the upstream binary name
- For a new `npm view --json …` → grep `npm view`

### Step 2 — Classify the match

| Match result | Action |
| :--- | :--- |
| **0 matches** | No reuse possible. Proceed to §6 (Adding New Entries). |
| **1 match — same binary, different shape** | Try to extend via §5 extension patterns. |
| **2+ matches — near-duplicates** | Collapse via §5.3 alternation, then extend if needed. |

### Step 3 — Extend with `--replace`, NEVER duplicate with `--add`

```bash
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/edit-entry.py \
  --settings <path/to/settings.json> --replace \
  --old-key '<existing regex key>' \
  --new-key '<extended regex key>'
```

### Step 4 — Reapply indent overrides

```bash
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/fix-indents.py \
  --settings <path/to/settings.json>
```

### Step 5 — Verify

```bash
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/find-entry.py \
  --settings <path/to/settings.json> --grep '<binary-or-tool-token>'
```

The grep MUST now return **exactly one** entry covering both the original and new command forms.

***

## 5. Extension Pattern Catalogue

These are the canonical extension patterns for keeping the list minimal. All preserve the
anti-chaining character class `[^;&|<>$BTICK()]` (where `BTICK` denotes a literal backtick)
from [`vscode-terminal-autoapprove-audit` §7.2](../vscode-terminal-autoapprove-audit/SKILL.md#72-anti-chaining-character-class).

### 5.1 Optional Trailing-Pipe Suffix

For a command form that may or may not be piped into a fixed, safe sink (`head`, `grep`):

| Before (two entries) | After (one entry) |
| :--- | :--- |
| `/^cmd( ARGS)?$/` + `/^cmd( ARGS)? \| head( -N)?$/` | `/^cmd( ARGS)?( \| head( -[0-9]+)?)?$/` |
| `/^cmd( ARGS)?$/` + `/^cmd( ARGS)? \| grep …$/`     | `/^cmd( ARGS)?( \| grep( -[A-Za-z]+)*( ARG-CLASS+)+)?$/` |

> In the regex above, `ARG-CLASS` = the anti-chaining character class. See §7.2 of the base skill
> for the literal characters.

**Worked example** — collapsing standalone + `| head` for `find-entry.py`:

```bash
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/edit-entry.py \
  --settings <path> --replace \
  --old-key '/^python3 …/find-entry\.py( ARG-CLASS*)?$/' \
  --new-key '/^python3 …/find-entry\.py( ARG-CLASS*)?( \| head( -[0-9]+)?)?$/'
```

### 5.2 Optional Leading-Flag Group

For a command that may take an additional global flag without changing semantics
(e.g., `git --no-pager <subcommand>`):

| Before | After |
| :--- | :--- |
| `/^git <subcmd>( ARGS)?$/` + `/^git --no-pager <subcmd>( ARGS)?$/` | `/^git( --no-pager)? <subcmd>( ARGS)?$/` |

### 5.3 Alternation Collapse (Sibling Binaries)

For two binaries with identical argument grammars and identical SAFE verdicts:

| Before (two entries) | After (one entry) |
| :--- | :--- |
| `/^head( -[0-9]+)? PATH$/` + `/^tail( -[0-9]+)? PATH$/` | `/^(head\|tail)( -[0-9]+)? PATH$/` |
| `/^… --help( 2>&1)?$/` + `/^… --version( 2>&1)?$/`     | `/^… --(help\|version)( 2>&1)?$/` |

**Collapse-eligibility test (all MUST hold):**

1. Both binaries have identical SAFE classification in
   [`is-this-command-safe`](../is-this-command-safe/SKILL.md).
2. Argument grammar after the binary token is character-for-character identical.
3. The collapsed regex remains anchored (`^…$`) and keeps the anti-chaining class on every arg slot.
4. The combined entry does not become wider than its two parents (no new attack surface).

If ANY test fails, keep the entries separate.

### 5.3.1 Multi-Binary Safe-Chain Extension (Branch Append, Not Entry Add)

When a user wants to auto-approve `&&`-joined chains that mix SAFE binaries which a
single-binary safe-chain entry does not yet cover (e.g., a chain entry whose alternation
currently lists `git (status|log|diff)`, `echo`, `wc` — and the user pastes
`sed -n '208,214p' FILE && echo "---" && git diff FILE | grep -i PAT`), the **correct
extension** is to APPEND new branches to the existing safe-chain alternation, **NOT** to
add a separate per-binary chain entry.

| Anti-pattern (FORBIDDEN) | Canonical pattern |
| :--- | :--- |
| `--add` a new `/^sed -n 'N,Mp' FILE && echo … && git diff FILE \| grep PAT$/` entry per chain shape | `--replace` the existing `/^(?:GIT\|ECHO\|WC)( && (?:GIT\|ECHO\|WC))*$/` chain entry, appending `\|SED\|CAT\|HEAD\|LS\|WHICH\|GREP\|MDLINT` to BOTH the head alternation AND the `( && …)*` trailing alternation |

**Branch append protocol (per appended binary):**

1. The binary MUST already be classified SAFE (or SAFE-IF-PIPED with read-only sinks only) in
   [`is-this-command-safe`](../is-this-command-safe/SKILL.md).
2. The branch MUST carry its own arg slot using the anti-chaining class
   `[^;&\|<>$BTICK()]` (or the quoted-string equivalents), with no wildcards on destructive
   flags (e.g., `markdownlint-cli2` branch MUST retain `(?! .*--fix)`).
3. The branch MUST allow its OWN downstream sink slot (`( \| (head\|tail)( -N)?)?` etc.) so that
   per-segment pipes survive — without this, `git diff FILE \| grep PAT` cannot match inside
   an `&&` chain.
4. The branch MUST be appended to BOTH alternations (head AND `( && …)*`) symmetrically — an
   asymmetric append silently rejects chains starting with the new binary.
5. Every accept / reject assertion from the existing entry's
   [`specs/`](../command-autoapprove-onboarding/specs/) MUST still pass after the append.
   New accept assertions for each appended branch MUST be added in the same edit.

**Worked example — appending `sed -n`, `cat`, `head`, `ls`, `which`, `grep`, `markdownlint-cli2`
to the `(GIT\|ECHO\|WC)` chain entry**: the resulting alternation grew from ~915 chars to ~2235
chars (single entry; 40 entries total in `settings.json` unchanged), covering 10 newly-pasted
diagnostic command shapes with zero new attack surface (every rejection assertion — `git status
&& rm -rf ~`, `cat file > /etc/important`, `sed -i ...`, `markdownlint-cli2 --fix ...`,
`grep -r secret / \| xargs rm`, `git log; rm -rf .` — still rejects).

**When NOT to use branch-append (use a separate entry instead):**

- The new binary is `MUTATES` or `HAS-DESTRUCTIVE-FLAGS` (e.g., `cp`, `mv`, `rm`, `sed -i`).
- The new binary's safe grammar diverges so much from the alternation that the resulting
  regex doubles again (~4500+ chars). Past that complexity, readability collapses and a
  per-binary `&&`-chain entry with its own narrow alternation is clearer.
- The chain separator the user wants is `;` (not `&&` / `||`). `;` chains belong to a
  separate semicolon-safe-chain entry per §5.1 Safe-Chain Entries in the
  [command-autoapprove-onboarding skill](../command-autoapprove-onboarding/SKILL.md#step-51--safe-chain-entries-opt-in)
  — never silently widen an `&&` entry to accept `;`.

### 5.3.2 Pipeline Producer–Consumer Sink Extension (`xargs`-Whitelisted Downstream)

When a user wants to auto-approve a producer-consumer pipeline whose consumer is `xargs`
(e.g., `find … | xargs grep -<flags> <PAT>` for cross-file code search), the **correct
extension** is to widen the PRODUCER entry's sink slot to admit a new `\| xargs <safe-cmd> …`
branch with the downstream binary HARDCODED to a read-only command — never `xargs .*`.

`xargs` inherits the destructiveness of its downstream command, so `xargs rm`, `xargs sed -i`,
`xargs sh`, `xargs cp`, `xargs mv` are all destructive. The branch MUST whitelist exactly one
of `xargs (grep|head|tail|wc|cat)` per appended sink. See the `xargs` section in the
[`is-this-command-safe` cheatsheet](../is-this-command-safe/docs/cheatsheet.md#xargs).

**Sink extension protocol (per appended consumer):**

1. The downstream binary (e.g., `grep`) MUST be SAFE alone in `is-this-command-safe`
   (read-only — no in-place mutation flags).
2. The branch MUST be written as a literal binary name (`\| xargs grep`), NEVER as a
   metacharacter alternation (`\| xargs [a-z]+` is FORBIDDEN — it would admit `xargs rm`).
3. The downstream consumer's arg slot MUST carry the anti-chaining class
   `[^;&\|<>$BTICK()'" ]` (plus quoted-string forms), with destructive flags excluded.
4. Trailing read-only filters MAY be admitted (`\| grep -<flags> <PAT>`, `\| head -N`,
   `\| tail -N`, `\| wc`) so that the common `find … | xargs grep -li … | grep -v X | head -N`
   shape is covered in one entry.
5. The producer entry MUST add a new SSOT row for `xargs` (status: `SAFE-IF-PIPED`) the first
   time any `xargs <…>` branch lands in any entry. The SSOT row MUST list every blocked
   downstream binary AND every whitelisted downstream binary explicitly.

**Worked example — appending `\| xargs grep …` to the `find` entry [39]:**

| Aspect | Before | After |
| :--- | :--- | :--- |
| Sink alternation in `find` entry | `\| head` · `\| grep …` | + `\| xargs grep -<flags> <PAT> [-<flags>] [2>…] [\| grep …] [\| head]` |
| Regex length | 1206 chars | 1833 chars |
| `xargs` SSOT row | absent | `SAFE-IF-PIPED`, destructive list 5 binaries, safe list 5 binaries |
| Covered commands gained | 0 | 5 (`find … \| xargs grep …` variants) |
| Negative tests (`\| xargs rm`, `\| xargs sed -i`, `\| xargs sh`) | rejected | still rejected |

**When NOT to use sink extension:**

- The user's pipeline uses `xargs <mutating-cmd>` (`xargs rm`, `xargs sed -i`, `xargs sh -c`) — NEVER auto-approvable.
- The producer is a `MUTATES` binary — don't smuggle in a destructive form via permissive sink.
- The sink consumer is itself a chain (`\| xargs grep PAT && rm file`) — sinks must be terminal read-only filters.

### 5.4 Optional Sub-Sub-Command Group

For a tool family with a stable prefix (e.g., `npm <subcmd>`, `git <subcmd>`) where each
subcommand has a distinct grammar, do **NOT** alternation-collapse. Keep one entry per
subcommand. The shared prefix is too short to justify a wide regex.

**Anti-pattern — over-merging `git <subcmd>` entries.** A repo's `settings.json` may carry
many narrow git entries (e.g., `git remote -v`, `git rev-parse`, `git branch`,
`git check-ignore`, `git show`, `git stash list`, `git (status|log|diff|ls-files)`,
and a safe-chain entry for `&&`-chained reads). It is **tempting** to merge these into
one mega-regex on the shared `git` prefix. **Reject this temptation** — each subcommand
has its own legal flag set (`branch --show-current` vs `show --name-status` vs
`check-ignore -v` …) and its own legal sink set. The resulting mega-regex would either:

1. Lose specificity (e.g., would allow `git remote --show-current`, a nonsensical /
   ambiguous form that the per-subcommand entries correctly reject), OR
2. Grow to ~3× the sum of its parents to preserve per-subcommand constraints — defeating
   the readability benefit of the merge.

The **Collapse-eligibility test from §5.3** ("argument grammar after the binary token is
character-for-character identical") fails for any two distinct `git` subcommands, so the
merge violates the rule. Keep the per-subcommand entries separate.

### 5.5 Tight Token Whitelist (vs Generic Arg Slot)

A SAFE binary's argument grammar can be expressed two ways: a permissive
generic slot or an explicit token whitelist. The trade-off is acceptance
breadth vs. promotion-safety.

| Style | Regex shape | Accepts | Trade-off |
| :--- | :--- | :--- | :--- |
| Generic arg slot (default) | `<cmd>( [^;&\|<>$BTICK()]*)?` | Any single arg string free of chaining metacharacters (e.g., `HEAD~1`, `--cached`, `-- path/to/file`, `origin/main`) | Maximum reuse; arbitrary new flags pass without re-audit. Future MUTATES flags introduced upstream (`-i`, `--delete`, etc.) silently inherit auto-approval if the binary verdict ever shifts to `HAS-DESTRUCTIVE-FLAGS`. |
| Tight token whitelist | `<cmd>( --cached)?( -- [^;&\|<>$BTICK()]+)?` | Only the named tokens (in the named positions) | Highest promotion-safety; the entry is auditably narrow. Rejects previously-allowed forms (`HEAD~1`, `origin/main`, …) — requires explicit extension to add a new flag. |

(`BTICK` denotes a literal backtick.)

**Decision rule:**

1. Prefer the **tight token whitelist** when the binary is in the
   `HAS-DESTRUCTIVE-FLAGS` category in
   [`is-this-command-safe`](../is-this-command-safe/SKILL.md), or when the
   user explicitly asks for "specific flags only" / "predictable behaviour".
2. Prefer the **generic arg slot** for pure-`SAFE` binaries when the user
   uses many different arg shapes across sessions and explicitly accepts
   the broader surface.
3. When promoting an entry from generic to tight, the agent MUST present
   the **regression set** (the previously-accepted forms that the tight
   pattern will reject) and obtain explicit user confirmation per
   [`vscode-terminal-autoapprove-audit` §11.2](../vscode-terminal-autoapprove-audit/SKILL.md#112-adding-new-entries).

**Worked example** — `git (status|log|diff|ls-files)` for a settings-review
workflow that uses only `--cached` and `-- <path>` plus optional pipe to
`head`/`tail`/`sed -n 'N,Mp'`:

```text
/^git( -C [^;&|<>$BTICK()]+)?( --no-pager)? (status|log|diff|ls-files)( --cached)?( -- [^;&|<>$BTICK()]+)?( \| (head|tail)( -[0-9]+)?| \| sed -n '[0-9]+(,[0-9]+)?p')?$/
```

Validate via
[`scripts/test-regex-accept.py`](../command-autoapprove-onboarding/scripts/test-regex-accept.py)
with both the desired accept set AND the previously-accepted reject set
(`git diff HEAD~1`, `git log --oneline`, …) before committing.

***

## 6. Adding New Entries (Fallback)

Only when §4 Step 2 returns **0 matches** for the binary may the agent add a new entry. Follow
[`vscode-terminal-autoapprove-audit` §11.2](../vscode-terminal-autoapprove-audit/SKILL.md#112-adding-new-entries)
verbatim:

1. Classify with [`is-this-command-safe`](../is-this-command-safe/SKILL.md) §6.
2. If verdict is `MUTATES`: obtain explicit user confirmation.
3. Use anchored regex `/^…$/` + `matchCommandLine: true`. Bare-prefix `"token": true` is
   **FORBIDDEN**.
4. Apply the anti-chaining character class on every arg slot.
5. Scan for Tier A/B secrets per
   [`vscode-terminal-autoapprove-audit` §8](../vscode-terminal-autoapprove-audit/SKILL.md#8-secret-scanning).

For `;`-chained one-liners composed solely of already-SAFE binaries, prefer a
single **safe-chain entry** (per
[`command-autoapprove-onboarding` §5.1](../command-autoapprove-onboarding/SKILL.md#step-51--safe-chain-entries-opt-in))
over N separate atomic entries — the alternation-collapse pattern (§5.3 here)
applied at chain granularity. Always validate via
[`scripts/test-regex-accept.py`](../command-autoapprove-onboarding/scripts/test-regex-accept.py)
before committing.

***

## 7. Periodic Sweep Protocol

To detect missed consolidation opportunities, periodically run:

```bash
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/find-entry.py \
  --settings <path/to/settings.json> --list
```

Then scan the printed list for:

| Smell | Suggested fix |
| :--- | :--- |
| Two entries with the same binary prefix and different fixed suffixes | §5.1 optional-suffix merge |
| Two entries differing only by `--no-pager` or `--json` | §5.2 optional-flag-group merge |
| Two sibling binaries (`head`/`tail`, `--help`/`--version`) | §5.3 alternation collapse |
| An entry with a hardcoded one-shot path (specific CSV, session-backup dir) | Drop per audit §6 (dead-weight) |

Each fix MUST be applied via `--replace` + `--delete` (NEVER duplicate via `--add` then drop later
in two separate commits).

***

## 8. Prohibited Behaviors

The agent is **BLOCKED** from:

1. Calling `edit-entry.py --add` without first running the §4 Step 1 reuse-check grep.
2. Creating a new entry when an existing entry can be extended via §5.
3. Writing extension regex without the anti-chaining character class on every arg slot.
4. Collapsing two binaries via alternation when their SAFE classifications differ.
5. Duplicating the base skill's scripts into this skill's folder — this skill is a composer; the
   scripts live in `vscode-terminal-autoapprove-audit/scripts/`
   ([Skill Factory §2.2.1 #5 Portable Anchored Paths](../skill-factory/SKILL.md#221-script-authoring-mandates)).

***

## 9. Verification & Markdown Hygiene

- This `SKILL.md` and its companion `AGENTS.md` MUST pass
  [Markdown Generation Rules](../../../ai-agent-rules/markdown-generation-rules.md) lint.
- All inter-skill links use **relative paths** with correct depth (`../../../` to reach
  `ai-agent-rules/` from this 3-deep skill folder; `../<skill>/SKILL.md` for sibling skills).
- Per [Redaction & Portability Skill](../redaction-portability/SKILL.md), every file here is
  Tier C (public/universal technical content) — no Tier A/B identifiers are present or may be
  introduced. Concrete user-home paths in command examples use the `<path/to/settings.json>`
  placeholder.

***

## 10. Related Skills

| Skill | Role |
| :--- | :--- |
| [`vscode-terminal-autoapprove-audit`](../vscode-terminal-autoapprove-audit/SKILL.md) | Base — owns scripts, indentation contract, full audit lifecycle |
| [`is-this-command-safe`](../is-this-command-safe/SKILL.md) | SSOT for safety verdicts that justify entry additions |
| [`vscode-settings-promotion`](../vscode-settings-promotion/SKILL.md) | Promotes the consolidated setting to all profiles after cleanup |
| [`vscode-settings-indent-override`](../vscode-settings-indent-override/SKILL.md) | Re-indents `approve` / `matchCommandLine` sub-keys if `fix-indents.py` is unavailable |
| [`command-autoapprove-onboarding`](../command-autoapprove-onboarding/SKILL.md) | Orchestrator that calls this skill in Step 6 of its end-to-end pipeline |
| [`skill-factory`](../skill-factory/SKILL.md) | Authored this skill per Industrial Fidelity mandates |

***

## 11. Traceability

- Originating session: consolidating one user's autoApprove list from 25 → 22 entries by
  collapsing `git stash list` + `git stash list | grep`, `--help` + `--version`, and
  `head` + `tail` into single anchored regex entries. The session also produced
  [`vscode-terminal-autoapprove-audit` §11.1 (Reuse Before Add)](../vscode-terminal-autoapprove-audit/SKILL.md#111-reuse-before-add-primary-rule),
  which this skill expands into a full algorithm with extension catalogue.
