---
name: vscode-terminal-autoapprove-audit
description: Audit, tighten, and prune chat.tools.terminal.autoApprove entries in VS Code settings.json — one-by-one review with is-this-command-safe verdicts, dead-weight detection, loose prefix migration to anchored anti-chaining regex, secret scanning, and batch drop execution.
category: VSCode-Configuration
---

# VS Code Terminal Auto-Approve Audit Skill (v1)

This skill governs the lifecycle of `chat.tools.terminal.autoApprove` entries in VS Code
`settings.json`: initial audit, entry-by-entry safety review, migration of loose prefix rules
to anchored regex, secret scanning, and surgical bulk removal of dead-weight one-shots.

It composes the [`is-this-command-safe`](../is-this-command-safe/SKILL.md) skill as its
verdict engine. Classification tiers and destructive-flag inventory are NOT duplicated here —
they are the SSOT of that skill.

***

## 1. Layering Decision

Per [Skill Factory §2.0](../skill-factory/SKILL.md#20-layering-decision-base-vs-composer), this
skill is **Atomic** at v1. The entire workflow (list → classify → decide → apply) is specific to
`chat.tools.terminal.autoApprove` and has no reusable primitive that another domain would need.

It **consumes** (does not duplicate):

- [`is-this-command-safe`](../is-this-command-safe/SKILL.md) — four-tier safety verdict
- [`vscode-settings-promotion`](../vscode-settings-promotion/SKILL.md) — if the setting needs
  promoting across profiles after cleanup

***

## 2. Environment & Dependencies

| Requirement | Verification |
| :--- | :--- |
| Python 3.9+ | `python3 --version` |
| Valid `settings.json` | `python3 -c "import json; json.load(open('<path>'))"` |
| `is-this-command-safe` skill | Read `../is-this-command-safe/SKILL.md` |

No pip packages required — scripts use only the standard library (`json`, `re`, `sys`, `os`).

***

## 3. Trigger Conditions

Invoke this skill when:

1. `chat.tools.terminal.autoApprove` has accumulated many entries and needs pruning.
2. A bare-prefix entry (e.g. `"mkdir": true`) needs migrating to an anchored regex.
3. A suspected secret (password, token) is embedded in an entry key.
4. A new auto-approve rule is proposed and must pass safety classification before addition.

### 3.1 Formatting Contract — settings.json Indentation

The target file (`vscode-insiders-configuration/visual-studio-code-user-settings/settings.json`)
is written by VS Code itself and managed by the
[`vscode-user-settings-symlink`](../vscode-user-settings-symlink/SKILL.md) skill. The canonical
indentation convention for this file is **plain 4-space-per-level JSON throughout** — no
per-key overrides.

| Depth | Spaces | Content |
| :--- | :--- | :--- |
| 1 | 4  | Top-level keys (`"chat.tools.terminal.autoApprove": { ... }`) |
| 2 | 8  | Per-entry regex keys inside the `autoApprove` object; values inside `files.associations` |
| 3 | 12 | `approve` / `matchCommandLine` sub-keys |

This is exactly `json.dumps(data, indent=4, ensure_ascii=False)`.

> **History (May 2026 onward):** earlier revisions of this contract used a 2-space base with
> deliberate +2 / +4 overrides on `files.associations` values and `approve` /
> `matchCommandLine` sub-keys, applied via
> [`vscode-settings-indent-override`](../vscode-settings-indent-override/SKILL.md). That
> override layer is **retired**. The flat 4-space form supersedes it.

**After any edit that rewrites the file**, run the canonical one-shot fix:

```bash
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/fix-indents.py \
  --settings <path/to/settings.json>
```

This script loads the JSON and rewrites it with `indent=4` (validating along the way). It is
a no-op when the file is already canonical.

Use `--dry-run` to preview changes without writing.

> **Script indent behaviour:**
> - `edit-entry.py` writes `indent=2` → run `fix-indents.py` afterwards to renormalize.
> - `audit-autoapprove.py` uses raw regex surgery (no json.dump); its drop pattern was
>   calibrated to the legacy 4-space autoApprove-key form, which coincidentally matches the
>   new flat 4-space convention at depth 1 but NOT at depth 2 (now 8sp). Prefer
>   `edit-entry.py --delete` or `--delete-grep` for all single-entry drops.

***

## 4. Pre-Audit Setup

### 4.1 SQL Session Table

Create a tracking table at the start of the audit session — schema mirrors the actual
fields used during review:

```sql
DROP TABLE IF EXISTS autoapprove_review;
CREATE TABLE autoapprove_review (
    seq          INTEGER PRIMARY KEY,    -- 1-based entry position at time of review
    key_snippet  TEXT,                   -- first ~80 chars of decoded key
    verdict      TEXT,                   -- SAFE | SAFE-IF-PIPED | HAS-DESTRUCTIVE-FLAGS | MUTATES
    decision     TEXT,                   -- KEPT | DROPPED | MIGRATED | REPLACED
    notes        TEXT                    -- justification, related entries, follow-up
);
```

If the session is interrupted and the table schema is lost, recreate it. The SQL table is
a *side log* — the source of truth is `settings.json` itself plus the conversation.

### 4.2 Count and List Entries

Use the helper script (preferred — preserves indentation contract):

```bash
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/find-entry.py \
  --settings <path/to/settings.json> --list
```

### 4.3 Targeted Lookup

| Goal | Command |
| :--- | :--- |
| Print one entry by 0-based index | `find-entry.py --settings <p> --index 11` |
| Print one entry by 1-based index | `find-entry.py --settings <p> --index 12 --one-based` |
| Find entries containing substring | `find-entry.py --settings <p> --grep 'ssh-mcp'` |

> When grepping, keys are stored with `\\` escapes — search for `ast\\.parse`, not `ast.parse`.

***

## 5. One-by-One Review Protocol

For each entry the agent MUST:

1. **Decode the key** — unescape `\n`, `\\.`, `\\(`, `\\)` etc. to recover the effective command.
2. **Classify** using [`is-this-command-safe`](../is-this-command-safe/SKILL.md) §6 Lookup Procedure.
3. **Emit the §5 verdict template** from that skill (see §5.1 below).
4. **Apply dead-weight detection** (§6 below).
5. **Apply secret scanning** (§8 below).
6. **Present verdict + recommendation** and await user decision: `drop`, `keep`, or `next`.
7. **Log the decision** to the SQL table.

### 5.1 Verdict Output Format

Follow `is-this-command-safe` §5 exactly — no prose preamble, no essay:

```text
Command   : <verbatim effective command (first 120 chars)>
Verdict   : <SAFE | SAFE-IF-PIPED | HAS-DESTRUCTIVE-FLAGS | MUTATES>
Reason    : <one-line justification>
Safe form : <dry-run equivalent, or "n/a">
Action    : <Execute | Execute-with-care | Refuse-pending-user-confirmation>
```

Then append:

```text
Dead-weight: <Yes — one-shot, won't re-match | No — reusable>
Secrets    : <None | CREDENTIAL DETECTED — rotate before proceeding>
Recommend  : <Keep | Drop | Migrate prefix to anchored regex>
```

***

## 6. Dead-Weight Detection

An entry is **dead weight** when ALL of the following hold:

1. The key is a regex anchored with `^…$` and `matchCommandLine: true`.
2. The body contains hardcoded absolute paths (specific CSV files, session-specific backup
   directories) unlikely to recur verbatim.
3. The entry is a one-shot analysis or discovery command from a past session.

**Dead-weight recommendation: Drop.**

Entries that are **not** dead weight (keep/reuse candidates):

- Short general commands: `git remote -v`, `git status`, `git log --oneline`.
- Regex patterns covering a class of commands (e.g. anchored `git rev-parse` form).
- Lint/check tools invoked repeatedly: `markdownlint-cli2`, `npm list`.

***

## 7. Loose Prefix Migration Protocol

A **loose prefix** entry has the form `"<token>": true` (no `^…$` anchors, no
`matchCommandLine`). This matches any command line beginning with the token — including
injected mutations (e.g. `"command": true` approves `command rm -rf ~`).

### 7.1 Standard Migration Table

| Original loose form | Migrated anchored form | Class |
| :--- | :--- | :--- |
| `"git rev-parse": true` | `/^git rev-parse( [^;&\|<>\$` + '`' + `()]*)?$/` | SAFE |
| `"command": true` | `/^command -v [A-Za-z0-9_.+-]+$/` | SAFE |
| `"markdownlint-cli2": true` | `/^markdownlint-cli2( [^;&\|<>\$` + '`' + `()]*)?$/` | SAFE |
| `"mkdir": true` | `/^mkdir( -p)?( [^;&\|<>\$` + '`' + `()]+)+$/` | MUTATES (accepted) |
| `"pg_restore": true` | `/^pg_restore --list [^;&\|<>\$` + '`' + `()]+$/` | MUTATES→SAFE (list-only) |

### 7.2 Anti-Chaining Character Class

Every migrated regex MUST gate argument slots with `[^;&|<>$` + '`' + `()]` to block:

| Character | Attack blocked |
| :--- | :--- |
| `;` | Command sequencing (`cmd1; rm -rf ~`) |
| `&` | AND-chaining / backgrounding (`cmd && rm`) |
| `\|` | Pipe to destructive downstream |
| `<` `>` | Redirection (overwrite existing file) |
| `$` | Variable/command substitution `$()` |
| `` ` `` | Backtick command substitution |
| `(` `)` | Subshell |

### 7.3 Application Steps

1. Edit `settings.json`: replace `"<token>": true` with:
   ```jsonc
   "/^<anchored-regex>$/": {
       "approve": true,
       "matchCommandLine": true
   }
   ```
2. Validate: `python3 -c "import json; json.load(open('<settings.json>')); print('OK')"`
3. Log decision as `migrated` in the SQL table.

### 7.4 Script — `edit-entry.py`

Handles add, in-place key replacement (for migration), and delete without touching other
entries. Writes with `indent=4` (§3.1 contract).

```bash
# Migrate loose prefix to anchored form (position preserved)
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/edit-entry.py \
  --settings <path> --replace \
  --old-key '"mkdir": true' \
  --new-key '/^mkdir( -p)?( [^;&|<>$`()]+)+$/'

# Add a new anchored entry at the tail
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/edit-entry.py \
  --settings <path> --add \
  --key '/^echo( [^;&|<>$`()]*)?$/'

# Delete one entry by exact key
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/edit-entry.py \
  --settings <path> --delete \
  --key '/^<full regex key>$/'

# Delete by substring — use when key contains newlines (shell quoting breaks exact match)
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/edit-entry.py \
  --settings <path> --delete-grep \
  --key 'npm search --json ssh mcp'
```

> **`--delete-grep` safety**: fails if 0 or >1 keys match the substring — always unique-identify
> before running. After deletion, run `fix-indents.py` to restore overrides.

### 7.5 Script — `batch-edit.py`

When more than ~3 ops need to be applied in one session, or when keys contain backticks,
`$`, or inner quotes that PowerShell will mangle on the command line, use `batch-edit.py`
to drive every op from a JSONL file (no shell-quoting hazard, single Python startup):

```bash
# ops.jsonl — one operation per line; '#' and blank lines ignored
# {"op": "add",         "key": "/^…$/"}
# {"op": "replace",     "old": "loose-prefix", "new": "/^anchored$/"}
# {"op": "delete",      "key": "exact-key"}
# {"op": "delete-grep", "key": "unique-substring"}

python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/batch-edit.py \
  --settings <path> --ops ops.jsonl

# Validate the whole plan without writing
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/batch-edit.py \
  --settings <path> --ops ops.jsonl --dry-run
```

If any single op fails, the file is **NOT written** — all-or-nothing semantics.
Tolerates BOM-prefixed UTF-8 (PowerShell 5 `Out-File -Encoding utf8` default).
Run `fix-indents.py` afterwards (§3.1).

***

## 8. Secret Scanning

Before logging `keep` or `migrate`, scan the entry key for:

| Pattern | Risk tier | Action |
| :--- | :--- | :--- |
| `--password=`, `PASSWORD='…'` literal | Tier A credential | **Drop immediately + rotate + audit git history** |
| `CREATE ROLE … PASSWORD '…'` SQL DDL | Tier A credential | Same |
| Bearer / API token literal | Tier A credential | Same |
| IPv4 of non-public host | Tier B topology | Warn; recommend drop |
| Internal hostname / domain | Tier B topology | Warn; recommend drop |

> **Warning**: `settings.json` is often committed to version-controlled
> `<private-config-repo>` repositories and synced via
> `workbench.settings.applyToAllProfiles`. Credentials embedded in entry keys appear in git
> history. Rotate before removing the entry.

***

## 9. Batch Drop Execution

After collecting all `drop` decisions, apply in one atomic pass:

```bash
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/audit-autoapprove.py \
  --settings  <path/to/settings.json> \
  --drop-indices 0 1 2 3 6 7 8
```

The script ([`scripts/audit-autoapprove.py`](./scripts/audit-autoapprove.py)):

1. Loads `settings.json`, extracts `chat.tools.terminal.autoApprove`.
2. Removes keys at the specified 0-based indices (resolved before removal — indices stable).
3. Re-serialises JSON, fixes trailing-comma artifacts, validates with `json.loads`.
4. Writes file in-place.
5. Prints: `Removed N entries. autoApprove entries now: M`.

**Always confirm the drop index list against the SQL table before running.**

***

## 10. Post-Audit Checklist

- [ ] JSON validates: `python3 -c "import json; json.load(open('<settings.json>'))"`
- [ ] No loose-prefix entries remain: `grep -n '": true' settings.json`
  (only `workbench.settings.applyToAllProfiles` array values should show `true`)
- [ ] No secrets in retained entries (re-run §8 scan on remaining keys)
- [ ] SQL table has a row for every reviewed entry
- [ ] `workbench.settings.applyToAllProfiles` still lists `chat.tools.terminal.autoApprove`
- [ ] Git diff reviewed before committing

***

## 11. Forward Policy — Adding New Entries

### 11.1 Reuse Before Add (Primary Rule)

Before creating a new entry, the agent MUST check whether an existing entry can be extended
to cover the new command form. Prefer **extending** over **adding** to keep the list minimal.

> The full extension-pattern catalogue, reuse-check procedure, collapse-eligibility tests, and
> periodic sweep protocol live in
> [`vscode-autoapprove-entry-consolidation`](../vscode-autoapprove-entry-consolidation/SKILL.md)
> (composer over this skill). The summary table below is retained for inline reference only —
> the consolidation skill is the SSOT for the algorithm.

**Extension patterns:**

| Existing covers | New form | Action |
| :--- | :--- | :--- |
| `cmd( ARGS)?$` (standalone) | `cmd( ARGS)? \| head( -N)?` (with pipe) | Replace: make the `\| head` suffix optional with `( \| head( -[0-9]+)?)?` |
| `cmd( ARGS)?$` | `cmd --extra-flag( ARGS)?` | Replace: add `(--extra-flag )?` group to existing pattern |
| Two near-identical entries (same binary, different arg shapes) | — | Collapse into one regex with alternation `(form1\|form2)` |

**Reuse check procedure** (run before any `--add`):

```bash
# 1. Search for entries covering the same binary/tool
python3 .agents/skills/vscode-terminal-autoapprove-audit/scripts/find-entry.py   --settings <path> --grep '<binary-name>'

# 2. If a match exists, use --replace to extend the key; do NOT --add a new one.
# 3. Only --add when no existing entry covers the same binary/tool at all.
```

### 11.2 Adding New Entries

When no existing entry can be extended, the agent MUST:

1. Classify with `is-this-command-safe` §6.
2. If verdict is `MUTATES`: obtain explicit user confirmation.
3. Use anchored regex `/^…$/`. Bare-prefix `"token": true` is **FORBIDDEN** for any token
   that prefixes a destructive command.
4. Apply anti-chaining character class (§7.2) in all argument slots.
5. Set `matchCommandLine` per §11.3 below.
6. Scan for Tier A/B data (§8) before committing.

**Chained one-liners**: When the user explicitly wants a `;`-chained command
(e.g., `git status; echo '---'; git rev-parse <sha>^`) to auto-approve as a
single line, follow the **safe-chain pattern** documented in
[`command-autoapprove-onboarding` §5.1](../command-autoapprove-onboarding/SKILL.md#step-51--safe-chain-entries-opt-in),
including the mandatory regex-acceptance test via
[`scripts/test-regex-accept.py`](../command-autoapprove-onboarding/scripts/test-regex-accept.py).
Note that if all chained segments are SAFE and use `matchCommandLine: false`
(§11.3 default for SAFE), VS Code already splits the line on `;`/`&&`/`||`/`|`
and matches each sub-command independently — three atomic entries suffice and
the safe-chain pattern is unnecessary. The safe-chain pattern is for
`matchCommandLine: true` entries only.

### 11.3 `matchCommandLine` — Per-Verdict Policy

VS Code's `matchCommandLine` flag selects how the regex is evaluated against the user's
command line. Choose the value by safety verdict, not by personal preference:

| Verdict | `matchCommandLine` | Rationale |
| :--- | :--- | :--- |
| ✅ SAFE (read-only) | **`false`** | VS Code splits the line on `;`, `&&`, `\|\|`, `\|` and matches each sub-command independently. Chained read-only commands (e.g., `git status; git branch; git stash list`) auto-approve only when every segment matches a SAFE entry. The anti-chaining class still belongs in the regex — it costs nothing and defends against arg-embedded `$()`/backtick substitution that the line splitter does NOT split on. |
| 🟡 SAFE-IF-PIPED | **`true`** | Match the full pipeline literally so the SAFE downstream sink (head/grep/wc) is part of the contract. |
| ⚠️ HAS-DESTRUCTIVE-FLAGS | **`true`** | Full-line match needed to assert the destructive flag is absent in EVERY segment. |
| ❌ MUTATES (with user opt-in) | **`true`** | Narrow, full-line, no wildcards on the destructive flag. |

**Migration helper**: `batch-edit.py` supports an `update` op for flipping the flag in bulk:

```jsonl
{"op": "update", "key": "/^git status( …)*$/", "matchCommandLine": false}
```

> Note: `fix-indents.py` re-indents `approve`/`matchCommandLine` sub-keys regardless of value;
> no further indent adjustment is needed after a bulk flip.

***

## 12. Related Skills

| Skill | Role |
| :--- | :--- |
| [`is-this-command-safe`](../is-this-command-safe/SKILL.md) | SSOT for four-tier safety verdicts — consumed by §5 |
| [`vscode-settings-promotion`](../vscode-settings-promotion/SKILL.md) | Promotes setting to all profiles after cleanup |
| [`vscode-settings-indent-override`](../vscode-settings-indent-override/SKILL.md) | Re-indents `approve`/`matchCommandLine` sub-keys if needed |
| [`redaction-portability`](../redaction-portability/SKILL.md) | Sanitisation contract for `docs/conversations/` logs |
| [`vscode-autoapprove-entry-consolidation`](../vscode-autoapprove-entry-consolidation/SKILL.md) | Composer — reuse-before-add algorithm and extension-pattern catalogue for autoApprove entries |
| [`command-autoapprove-onboarding`](../command-autoapprove-onboarding/SKILL.md) | Orchestrator — end-to-end command → cheatsheet → autoApprove onboarding pipeline that consumes this skill's scripts |

***

## 13. Traceability

- [`docs/conversations/2026-05-19-autoapprove-audit.md`](./docs/conversations/2026-05-19-autoapprove-audit.md)
  — originating audit session: 47 entries reviewed, 10 dropped (first pass), 5 loose prefixes
  migrated to anchored anti-chaining regex; sanitised per Redaction & Portability protocol.
