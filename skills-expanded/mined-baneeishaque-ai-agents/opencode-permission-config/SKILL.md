---
name: opencode-permission-config
description: Configure opencode's permission system — pattern-based bash rules with last-match-wins semantics, edit workflow, restart requirement, and verification
category: Tool-Configuration
---

# opencode Permission Configuration Skill (v1)

This skill documents how to configure opencode's [`permission`](https://opencode.ai/docs/permissions)
system, specifically the pattern-based bash rules. It captures the critical **last-matching-rule-wins**
insertion-order semantics discovered during a real configuration session where a wrongly-ordered pattern
silently fell through to the catch-all.

***

## 1. Permission Config Format

The `permission` field in `opencode.json` controls which tools require user approval.

### 1.1 String Form (Simple)

A flat action applies to all invocations of that tool:

```json
"permission": {
  "bash": "ask",
  "edit": "ask",
  "read": "allow"
}
```

Actions: `"allow"`, `"ask"`, `"deny"`.

### 1.2 Object Form (Pattern-Based)

Most tools accept an object keyed by glob patterns. This enables per-command rules:

```json
"permission": {
  "bash": { "python3 -m py_compile *": "allow", "*": "ask" }
}
```

Each key is a glob pattern matched against the full command string. The corresponding
action applies when the pattern matches. Tools that accept pattern objects:
`read`, `edit`, `glob`, `grep`, `list`, `bash`, `task`, `external_directory`,
`lsp`, `skill`.

Tools that accept ONLY a flat action: `todowrite`, `question`, `webfetch`,
`websearch`, `doom_loop`.

***

## 2. Pattern Matching Semantics

### 2.1 Glob Pattern Matching

Patterns use standard glob (e.g., `fnmatch`) matching against the entire command
string as the agent would invoke it:

| Pattern | Matches | Does NOT match |
| :--- | :--- | :--- |
| `python3 *` | `python3 script.py`, `python3 -m http.server` | `python3.11 script.py` |
| `python3 -m py_compile *` | `python3 -m py_compile foo.py` | `python3 -m other_module` |
| `git *` | `git status`, `git log --oneline` | `hub status` |
| `*` | everything | — |

### 2.2 Last-Matching-Rule Wins (Critical Gotcha)

opencode evaluates patterns in **insertion order** and the **last matching pattern
wins**. This is the opposite of many firewall / ACL systems where first-match wins.

**Common mistake** — putting the broad catch-all (`"*": "ask"`) LAST:

```json
// WRONG — "*" is last and matches everything, overriding specific rules
"bash": { "python3 -m py_compile *": "allow", "*": "ask" }
```

With this order:

- `python3 -m py_compile --help` matches `python3 -m py_compile *` → `allow`
- …then ALSO matches `*` → **`ask`** (overrides the allow)

**Correct order** — broad / fallback FIRST, specific rules LAST:

```json
// CORRECT — specific rule is last and wins for matching commands
"bash": { "*": "ask", "python3 -m py_compile *": "allow" }
```

With this order:

- `python3 -m py_compile --help` matches `*` → `ask`
- …then ALSO matches `python3 -m py_compile *` → **`allow`** (final verdict)

### 2.3 Insertion Order Discipline

1. Place the catch-all pattern `"*"` FIRST.
2. Place specific allow/deny patterns AFTER, in order from least to most specific.
3. The last pattern in the object determines the final verdict for any command that
   matches it.

Reference: [opencode schema — `PermissionObjectConfig`](https://opencode.ai/config.json)

***

## 3. Editing Workflow

### 3.1 Locate opencode.json

| Scope | Path |
| :--- | :--- |
| Project | `./opencode.json`, `./opencode.jsonc`, or `.opencode/opencode.json` |
| Global | `~/.config/opencode/opencode.json` |

Configs are deep-merged — project overrides global.

### 3.2 Edit the Permission Block

Edit the `permission.bash` field. For example, to auto-allow `python3 -m py_compile`
for compile-check workflows:

```json
{
  "permission": {
    "bash": { "*": "ask", "python3 -m py_compile *": "allow" }
  }
}
```

### 3.3 Restart Requirement

opencode loads config once at startup and does **not** hot-reload. After editing
`opencode.json`, the user MUST quit and restart opencode for changes to take effect.
A running session continues using the previously-loaded config.

***

## 4. Testing & Verification

### 4.1 Manual Verification

After restarting opencode, run a command that should match the new rule:

```text
python3 -m py_compile --help
```

If configured correctly, the command executes without prompting.

### 4.2 Script-Based Pattern Verification

The bundled [`scripts/verify-permission-pattern.py`](scripts/verify-permission-pattern.py)
evaluates a permission object against test commands before editing `opencode.json`.

Supports three input modes:

**Mode 1 — Inline JSON config**:

```bash
python3 scripts/verify-permission-pattern.py \
  '{"*": "ask", "python3 -m py_compile *": "allow"}' \
  "python3 -m py_compile --help" "ls" "rm -rf /"
```

Output:

```text
  'python3 -m py_compile --help'  →  allow  (matched 'python3 -m py_compile *')
  'ls'  →  ask  (matched '*')
  'rm -rf /'  →  ask  (matched '*')
```

**Mode 2 — Direct opencode.json** (supports JSONC `//` comments, auto-extracts `permission.bash`):

```bash
python3 scripts/verify-permission-pattern.py \
  ~/.config/opencode/opencode.json \
  "git status" "git commit -m test" "rm -rf /"
```

Output:

```text
  'git status'  →  allow  (matched 'git status')
  'git commit -m test'  →  ask  (matched 'git commit *')
  'rm -rf /'  →  ask  (matched '*')
```

**Mode 3 — Pattern inventory** (no commands → prints all patterns):

```bash
python3 scripts/verify-permission-pattern.py \
  '{"*": "ask", "git status": "allow", "git status *": "allow"}'
```

Output:

```text
Pattern inventory:
  *: ask
  git status: allow
  git status *: allow
```

### 4.3 Spec-Based Regression Testing

Create a spec file (JSON array of `{command, expect}`) and run against a config:

```bash
OPENCODE_PERMISSION_CONFIG='{"*":"ask","python3 -m py_compile *":"allow"}' \
  python3 scripts/verify-permission-pattern.py \
  --spec specs/py-compile-allow.json
```

Run the comprehensive 92-test spec against the actual opencode.json:

```bash
OPENCODE_PERMISSION_CONFIG=~/.config/opencode/opencode.json \
  python3 scripts/verify-permission-pattern.py \
  --spec specs/full-config.json
```

All specs must PASS before deploying the config.

### 4.4 Wrong-Order Detection

Use the script to confirm the gotcha. The wrong order produces `ask` for a command
that should be `allow`:

```bash
python3 scripts/verify-permission-pattern.py \
  '{"python3 -m py_compile *": "allow", "*": "ask"}' \
  "python3 -m py_compile --help"
```

Output:

```text
  'python3 -m py_compile --help'  →  ask  (matched '*')
```

The specific rule matches but is overridden by the later `*` catch-all.

***

## 4.5 Real-Command Verification Protocol

This section describes the critical behavioral verification process that complements the spec-based pattern matching in §4.3.

The specification testing (`python3 verify-permission-pattern.py --spec ...`) validates that fnmatch patterns correctly match the intended command strings. However, true permission behavior must be verified by running the commands themselves within the opencode runtime environment.

We employ a two-phase verification workflow:

1. **Spec-Based Testing:** Use `verify-permission-pattern.py` with target specs to ensure pattern-string matching behavior
2. **Real-Command Testing:** Execute each candidate command in the operational environment to observe permission behavior

The merger finding revealed a critical process gap: spec testing verifies only the **pattern matching**, not the **runtime permission enforcement**. More importantly, running multiple bash calls simultaneously creates concurrent permission prompts that confuse verification.

The correct verification protocol requires **one command at a time**:

- Run a single command through the authorization system
- Observe whether it executes silently (✅ Allowed) or triggers a permission prompt (⚠️ Not Allowed)
- Repeat for each test case sequentially
- Never execute multi-command test batches that generate simultaneous prompts

This ensures:
- Each ask prompt traces to one specific command
- User feedback matches command execution
- Verification results are reproducible and auditable
- The system avoids confusing simultaneous prompt scenarios

**Verification Procedure:**

1. Start with an empty test set (no pending asks)
2. Execute one command at a time through the authorization interface
3. Observe the runtime response:
   - No prompt → command is ALLOWED (record as ✅)
   - Permission prompt → command is RESTRICTED (record as ⚠️)
4. Continue with next command in isolation
5. Document all outcomes in a test log

**Key Reminders:**
- Always test with `opencode.json` freshly restarted (quit opencode after config change; use `relaunch-opencode` tool)
- For patterns that use negation/negative lookahead concepts (like `!*`), verify they behave as expected in practice
- When validating cross-pattern interference, use a fresh start between test runs

The spec-based testing validates the **"what should happen"** logic; real-command testing validates the **"what does happen"** behavior.

SEE ALSO: `fnmatch-content-guard-pattern` §4.4 for spec-based testing details and §5 worked examples.

***

## 5. Troubleshooting

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| Pattern rule is ignored | Catch-all `"*"` appears AFTER the specific rule | Move `"*"` first (see §2.2) |
| Config change has no effect | opencode wasn't restarted | Quit and restart (see §3.3) |
| Pattern matches unexpected commands | Pattern is broader than intended | Narrow the glob (e.g., `python3 -m py_compile *` instead of `python3 *`) |
| `permission.bash` is still a string after edit | JSON syntax error | Validate with `python3 -m json.tool` |

***

## 6. Pattern Design Decisions

This section documents the design logic used to build a safe command allowlist from
the safety classifications in [`is-this-command-safe/docs/safety-table.csv`](../is-this-command-safe/docs/safety-table.csv).
It does NOT duplicate the safety table or the pattern list — those are the SSOTs. It
captures only the decision rules, gotchas, and tradeoffs that shaped the patterns.

### 6.1 Always-SAFE Commands

Commands classified `SAFE` in the safety table are never destructive regardless of
flags or pipeline context. These get bare + wildcard allow patterns (e.g., `echo *`,
`which *`, `pwd`, `true`, `false`, `head *`, `tail *`, `wc *`, `diff *`, `less *`,
`lsof *`, `du *`, `ffprobe *`, `readlink *`, `mdls *`).

### 6.2 SAFE-WITH-QUALIFICATION Commands

Commands classified `SAFE-WITH-QUALIFICATION` have both safe and destructive forms
depending on flags. Only the safe forms get allow patterns:

- **`cat`** — allow `cat *` (reading is safe); `cat > <file>` is MUTATES but falls
  through to `*: "ask"`. Accepted risk: the agent almost never uses `cat >` (it uses
  the `write`/`edit` tools instead).
- **`python3`** — only `python3 --version` and `python3 -m py_compile *` are allowed.
  Broad `python3 *` is intentionally omitted — the agent must ask before running
  arbitrary scripts.
- **`markdownlint-cli2`** — allowed as `markdownlint-cli2 *`. The `--fix` flag
  (in-place edit) matches the same wildcard, but the agent rarely invokes `--fix`
  without user knowledge. Accepted risk documented in §6.5.

### 6.3 Read-Only Git Subcommands

Only subcommands that NEVER mutate the repository are allowed. Design decisions:

- **`git remote *` is dangerous** — `git remote add`, `remote remove`, `remote set-url`,
  `remote rename` all match `git remote *`. Only bare `git remote` and `git remote -v`
  (both read-only) are allowed. `git remote -v` was added as a specific pattern to match
  the safety table's classification.
- **`git branch` safe-forms only** — bare `git branch` (list local branches), `-a`
  (list all branches), `-vv` (with tracking info), and `--show-current` are safe.
  `git branch *` is NOT added because it matches `git branch -D`, `-d`, `-m`,
  and `git branch <name>` (create). Each safe form is a separate narrow pattern.
- **`git stash` subcommands** — only `stash list` and `stash show` (read-only) are
  allowed. `stash drop/pop/apply` (MUTATES) have explicit ask patterns.
- **Bare vs wildcard** — fnmatch `*` does not match empty, so `git log *` does not
  match bare `git log`. Both bare and wildcard forms are needed (e.g., `git log`
  and `git log *`).

### 6.4 Git -C for Any Repo Path

Patterns use `git -C * <subcommand>` which matches any path after `-C`:
`.` `..` `~` `/absolute/path` `relative/path` etc. Safety is determined by the
subcommand, not the path — `git -C /nonexistent status` errors harmlessly.

```text
git -C /Users/dk/lab-data/ai-suite status    → MATCHES git -C * status
git -C /any/repo/path log -5                 → MATCHES git -C * log *
git -C . status                              → MATCHES git -C * status
```

The same fnmatch `*`-matches-chains risk applies here as to all wildcard
patterns (see §6.5). The specific path form `git -C /path/to/repos/*`
is safer (blocks `;` injection in the path position) but less general.
The general `*` form was chosen for wider applicability.

### 6.5 SAFE-IF-PIPED Tradeoffs

Commands classified `SAFE-IF-PIPED` are read-only alone but can be piped to destructive
downstream commands. fnmatch `*` matches pipe symbols (`|`), so `ls *` also matches
`ls | xargs rm`. The choice to allow or not depends on agent behavior:

| Pattern | Risk | Decision |
| :--- | :--- | :--- |
| `ls *` | Matches `ls \| xargs rm` | Allowed — agent rarely pipes to destructive commands; uses `write`/`edit` tools instead |
| `cat *` | Matches `cat > <file>` | Allowed — agent never uses `cat >` for writes |
| `grep *` | Matches `grep foo \| xargs rm` | Allowed — same reasoning as `ls` |
| `find *` | Matches `find . -delete` | NOT allowed — `-delete` is a flag, not a pipe; risk is higher |
| `sort *` | Matches `sort -o <file>` | NOT allowed — `-o <file>` flag clobbers files |

The general rule: allow SAFE-IF-PIPED commands where the destructive form requires an
unlikely agent behavior (piping to xargs rm vs. using the edit tool), but deny where
the destructive form is a single flag that the agent might plausibly use.

### 6.5.1 Broad-Allow + Narrow-Deny/Ask Content Guards

fnmatch cannot inspect argument content (no negative lookahead). For commands whose
dangerous forms have **distinctive substrings** (`system()`, `-f`, `-delete`,
`-exec`, `-o`), a middle ground exists: place a broad `C *` allow early, then
narrow `C *S*` ask/deny patterns **after** it. Last-match-wins means the narrow
pattern overrides the broad allow for dangerous forms.

```json
{
  "*": "ask",
  "C *": "allow",
  "C *S1*": "ask",
  "C *S2*": "ask"
}
```

This technique is the subject of the
[`fnmatch-content-guard-pattern`](../fnmatch-content-guard-pattern/SKILL.md)
base skill, which ships a pattern-generation script and worked examples for
`awk`, `find`, and `sort`. See §6.9 for the awk worked example that
originated this approach, and §4.5 for the real-command verification protocol that
complements this technique.

### 6.6 Explicit Ask Patterns for Unsafe Git Commands

Destructive git subcommands that could accidentally match a future allow pattern
are given explicit `"ask"` entries: `commit *`, `push *`, `rebase *`, `reset *`,
`clean *`, `checkout *`, `restore *`, `branch -d/-D/-m *`, `stash drop/pop/apply *`,
`merge *`, `remote add/remove/set-url/rename *`.

These are documentation — they don't change behavior since `*: "ask"` already
matches everything. They serve as a guardrail: if a future too-broad allow pattern
is added, these ask entries (which come after `*` but before allow patterns) prevent
the dangerous command from becoming auto-allowed.

### 6.7 VSCode autoApprove Cross-Reference

VSCode's `chat.tools.terminal.autoApprove` setting (regex-based) controls terminal
approval for Copilot Chat. This section documents which VSCode patterns were ported
to opencode's fnmatch system and why some cannot be ported.

#### Ported Patterns (opencode fnmatch equivalent)

| Pattern | VSCode coverage | Notes |
| :--- | :--- | :--- |
| `echo *` | VSCode: restricted (no metachars) | fnmatch is broader — accepts chain risk per §6.5 |
| `diff *` | VSCode: `-q` only | fnmatch allows all diff flags |
| `which *` | VSCode: requires arg(s) | fnmatch allows bare `which` too |
| `grep *` | VSCode: complex multi-pipe regex | Same §6.5 tradeoff |
| `ls *` | VSCode: restricted flags + pipes | Same §6.5 tradeoff |
| `cat *` | VSCode: single path, optional pipe | Broader — includes `cat >` risk (accepted) |
| `wc *` | VSCode: requires args, optional pipe | fnmatch allows bare `wc` |
| `head *` / `tail *` | VSCode: numeric flag only | fnmatch accepts any flags |
| `markdownlint-cli2 *` | VSCode: identical (no --fix) | Identical intent |
| `sed -n *` | VSCode: narrow print-only regex | `-n` required; `sed *` NOT added (matches `-i`) |
| `command -v *` | VSCode: requires args | Redundant with `which *`; parity |
| `brew list` / `brew outdated` / `brew leaves` | VSCode: same subcommands | Read-only only. `brew *` NOT added |
| `pg_restore --list *` | VSCode: same `--list` required | Lists dump contents; `pg_restore *` NOT added |
| `npm root` / `npm search *` / `npm view *` | VSCode: same subcommands | Read-only registry queries. `npm *` NOT added |
| `cut *` | VSCode: in sed+cut chain | Read-only field extractor |
| `cd *` | VSCode: `cd <path>` only | See §6.8 |
| `mkdir *` | VSCode: requires path arg(s) | MUTATES — user explicitly requested |
| `* --help` / `* --version` | VSCode: any `--help\|--version` | Safe — shows help text, doesn't execute. Overrides ask patterns for help/version variants (e.g., `git commit --help` allowed — shows man page, no commit) |

#### Ported via Content-Guard Technique

The following commands were previously excluded but are now ported using the
broad-allow + narrow-deny/ask technique (§6.5.1) from the
[`fnmatch-content-guard-pattern`](../fnmatch-content-guard-pattern/SKILL.md)
base skill:

| Command | Dangerous forms | Guard patterns added |
| :--- | :--- | :--- |
| `awk` | `system()`, `-f <script>` | `awk *system*`: ask, `awk *-f*`: ask |
| `find` | `-delete`, `-exec` | `find *-delete*`: ask, `find *-exec*`: ask |
| `sort` | `-o <file>` | `sort *-o*`: ask |

See §6.9 for the full awk worked example. The find and sort patterns follow
the same design.

#### Remaining Excluded (Regex-Only Protections)

| Command | Why fnmatch can't match VSCode | VSCode protection |
| :--- | :--- | :--- |
| `psql -c "SELECT..."` | VSCode blocks dangerous PG functions (`pg_read_file`, `lo_export`, etc.) via negative lookahead inside the SQL string. The dangerous substrings (`pg_read_file`, `lo_export`) are SQL-level, not shell-level; fnmatch sees the entire `-c "..."` string as one token | `(?!.*\b(pg_read_file\|...)\b)` inside the query string |

These remain excluded because the dangerous forms lack a shell-level distinctive
substring that fnmatch can target without false positives on legitimate uses.

### 6.8 cd Patterns

`cd` is classified **SAFE** (no filesystem mutation). opencode itself never runs
`cd` — it uses the `workdir` parameter on bash calls. `cd *` is added as a
safety-net so that if an agent ever constructs a `cd` command, it auto-runs
without prompting.

**Chain risk**: `cd *` matches chained destructive commands like
`cd /repo && git commit -m "x"` because `*` matches the entire suffix including
`&& <destructive>`. The agent's destructive git ask patterns (`git commit *`,
`git push *`, etc.) cannot protect chained cd+destructive forms because the
string starts with `cd /... && ...`, not `git ...`.

This risk is **accepted** because:

- The agent uses `workdir` instead of `cd` — it never constructs `cd`
  commands in practice.
- The existing `SAFE-IF-PIPED` tradeoff (§6.5) already accepts broader
  `*`-matches-chains risks for `ls *`, `cat *`, etc., where the chain could be
  `ls | xargs rm`.

If the agent's behavior changes and it starts using `cd && <destructive>`
frequently, `cd *` should be removed or narrowed.

### 6.9 awk — Content-Guard Worked Example

This subsection documents the conversation that originated the broad-allow +
narrow-deny/ask technique (§6.5.1) and the
[`fnmatch-content-guard-pattern`](../fnmatch-content-guard-pattern/SKILL.md)
base skill.

#### 6.9.1 Problem

The command `awk '/^\| Skill /,0' AGENTS.md | head -5` is a read-only pattern-match
invocation. Ideally it should be auto-allowed. But `awk` has two dangerous forms:
- `system()` — executes arbitrary shell commands
- `-f <script>` — runs a script file

fnmatch cannot express "allow awk UNLESS `system(` or `-f ` appears in the
argument list" (VSCode uses regex negative lookahead for this). The initial
design in §6.7 classified `awk` as excluded for this reason.

#### 6.9.2 Solution

Using last-match-wins ordering, add three patterns:

```json
{
  "awk *": "allow",
  "awk *-f*": "ask",
  "awk *system*": "ask"
}
```

Order within the config (after `"*": "ask"`):
1. `"awk *": "allow"` — broad allow for all awk invocations
2. `"awk *-f*": "ask"` — catches `-f <script>` (comes after allow, wins)
3. `"awk *system*": "ask"` — catches `system()` calls (comes after allow, wins)

#### 6.9.3 Verification

Using the [`verify-permission-pattern.py`](scripts/verify-permission-pattern.py) script:

```bash
python3 scripts/verify-permission-pattern.py \
  '{"*":"ask","awk *":"allow","awk *system*":"ask","awk *-f*":"ask"}' \
  "awk '/^Skill/,0' AGENTS.md" \
  "awk -f /tmp/test.awk" \
  "awk 'BEGIN {system(\"echo hello\")}'"
```

Results:

```text
  'awk '/^Skill/,0' AGENTS.md'            →  allow  (matched 'awk *')
  'awk -f /tmp/test.awk'                  →  ask  (matched 'awk *-f*')
  'awk 'BEGIN {system("echo hello")}''    →  ask  (matched 'awk *system*')
```

Three behaviors confirmed:
- **Safe read-only** → auto-allowed ✓
- **`-f <script>`** → prompts for approval ✓
- **`system()`** → prompts for approval ✓

The patterns were deployed to `opencode.json` (lines added after `"*": "ask"`),
and the deny patterns were later softened to ask so the user retains choice over
whether to run a potentially dangerous awk command.

#### 6.9.4 Generalization

The same technique applies to any command where dangerous forms have distinctive
shell-level substrings:
- **`find`**: `find *: allow` + `find *-delete*: ask` + `find *-exec*: ask`
- **`sort`**: `sort *: allow` + `sort *-o*: ask`

Each follows the same ordering discipline: broad allow first, narrow guard patterns
after, using last-match-wins semantics to let the guard override the allow.

***

## Composition Rationale

This skill is a composer: it does NOT re-implement command safety classification
or the fnmatch content-guard pattern technique. It consumes:
1. [`is-this-command-safe/docs/safety-table.csv`](../is-this-command-safe/docs/safety-table.csv)
   (the SSOT for command safety verdicts) to derive the allow/ask pattern set.
2. [`fnmatch-content-guard-pattern`](../fnmatch-content-guard-pattern/SKILL.md)
   (the base skill for the broad-allow + narrow-deny/ask technique) for commands
   whose dangerous forms need content-based filtering that fnmatch alone cannot
   express.

The pattern-design logic in §6 applies the safety table's classifications
(SAFE → allow, MUTATES → ask/deny) and the content-guard technique (§6.5.1)
while adding opencode-specific constraints (bare vs. wildcard, git -C,
SAFE-IF-PIPED tradeoffs) that neither base skill needs to know about.

Bidirectional discoverability: `is-this-command-safe` lists this skill in its
`## Composition by Higher-Level Skills` table; `fnmatch-content-guard-pattern`
lists this skill in its `## Composition by Higher-Level Skills` table.

## Related Skills

- [`opencode-jsonc-util`](../opencode-jsonc-util/SKILL.md) — Base JSONC utility for OpenCode config files (consumed by this skill's verification scripts)
- [`is-this-command-safe`](../is-this-command-safe/SKILL.md) — pre-execution
  command safety classification. This skill's SSOT data source.
- [`fnmatch-content-guard-pattern`](../fnmatch-content-guard-pattern/SKILL.md) —
  base skill for the broad-allow + narrow-deny/ask content-guard technique.
  Consumed by this skill for awk, find, and sort pattern additions.
- [`command-autoapprove-onboarding`](../command-autoapprove-onboarding/SKILL.md) —
  VS Code terminal auto-approve onboarding (complementary tool-approval domain,
  different tool).
- [`mcp-cross-tool-config-sync`](../mcp-cross-tool-config-sync/SKILL.md) —
  cross-tool config synchronization pattern.

## Source Rules

- [opencode JSON Schema — PermissionConfig](https://opencode.ai/config.json)
- [opencode Docs — Permissions](https://opencode.ai/docs/permissions)

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
| :--- | :--- |
| *(none yet)* | — |
