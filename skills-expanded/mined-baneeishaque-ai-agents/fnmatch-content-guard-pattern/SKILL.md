---
name: fnmatch-content-guard-pattern
description: Generic technique for using last-match-wins ordering to simulate content-based filtering in fnmatch-only permission systems — broad allow first, then narrow ask/deny patterns for dangerous argument substrings
category: Tool-Configuration
---

# fnmatch Content-Guard Pattern Skill (v1)

This skill documents a generic technique for working around fnmatch's inability to
inspect argument content (negative lookahead / content-based filtering). By exploiting
**last-match-wins** semantics, a broad allow pattern can be placed early, followed by
narrow deny/ask patterns that match only the dangerous argument forms — effectively
simulating content-based filtering in a glob-only pattern engine.

***

## 1. Problem

fnmatch globs match on **surface structure** — they see `*system*` but cannot answer
"does this command string contain the word `system` used as a function call?".

This matters for commands classified **SAFE-WITH-QUALIFICATION** or **SAFE-IF-PIPED**
where:
- Most invocations are safe (read-only, pattern matching, etc.)
- A small number of argument patterns are dangerous (`system()`, `-f <script>`,
  `-delete`, `-exec`, `-o <file>`)

VSCode's regex-based permission system can express:
```
/^awk(?!.*system\()(?!.*-f )/
```
(The command is allowed UNLESS `system(` or `-f ` appears.)

fnmatch has no equivalent. The naive approach — omitting the command entirely and
letting it fall through to `"*": "ask"` — works but forces the user to approve
every safe invocation too.

***

## 2. Solution: Broad-Allow + Narrow-Deny Content Guard

Using opencode's **last-match-wins** semantics (§2.2 of the
[opencode-permission-config](../opencode-permission-config/SKILL.md) skill),
patterns can be ordered so the dangerous forms are matched AFTER the broad allow
and thus override it.

### 2.1 Pattern Ordering

For a command `C` with dangerous substrings `S1..Sn`:

```json
{
  "*": "ask",           // 1. catch-all — matches everything first (lowest priority)
  "C *": "allow",       // 2. broad allow — matches all invocations of C
  "C *S1*": "ask",      // 3. narrow guards — match only dangerous forms, override allow
  "C *S2*": "ask",
  ...
}
```

Because opencode evaluates patterns in **insertion order** and the **last matching
pattern wins**:
- `C '/pat/'` → matches `*` (ask), then `C *` (allow) → **allow** ✓
- `C -f script.awk` → matches `*` (ask), then `C *` (allow), then `C *-f*` (ask) → **ask** ✓
- `C '{system("x")}'` → matches `*` (ask), then `C *` (allow), then `C *system*` (ask) → **ask** ✓

### 2.2 Selection Criteria

Apply this technique when:
1. The command's safe forms are used frequently enough that prompting on every
   invocation is disruptive.
2. The dangerous forms have **distinctive substrings** that appear in the command
   string — `system`, `-f`, `-delete`, `-exec`, `-o`, etc.
3. The dangerous substrings are unlikely to appear in safe invocations by accident
   (e.g., a file named `system.txt` would match `*system*`).

### 2.3 Limitations

- **False positives**: A safe command like `awk -v var="system"` would match
  `awk *system*` and be blocked. Accept the tradeoff or narrow the pattern further
  (e.g., `awk *system(*` — but fnmatch `*` matches `(` too).
- **Chain risk**: `C *` matches chained destructive commands like
  `awk '{system("x")}' && rm -rf /`. The narrow guard only catches the dangerous
  awk form itself, not the downstream chain. This risk is shared with all
  broad-allow patterns (see the `cd *` chain risk discussion in
  `opencode-permission-config` §6.8).
- **Substring collision**: A substring like `-f` appears in many benign contexts
  (`find . -name "*.txt"`, `du -sh .`). Only use this technique when the
  dangerous substring is specific enough to the command's dangerous form.

***

## 3. Environment & Dependencies

- Python 3.12+ for the generation script.
- `fnmatch` (stdlib) — no external dependencies.

***

## 4. Script: `generate-content-guard-patterns.py`

The [scripts/generate-content-guard-patterns.py](scripts/generate-content-guard-patterns.py)
script generates correctly-ordered JSON patterns for any command + dangerous substrings.

### 4.1 Quick Start

Generate awk patterns:

```bash
python3 scripts/generate-content-guard-patterns.py \
  awk \
  --dangerous=system --dangerous=-f \
  --action ask --display
```

Output:

```text
Content-guard patterns for 'awk':
  Insertion order (last-match-wins):
  1. "*": "ask"  →
  2. "awk *": "allow"  →
  3. "awk *system*": "ask"  →
  4. "awk *-f*": "ask"  ← LAST (wins)
```

### 4.2 Generate and Write to File

```bash
python3 scripts/generate-content-guard-patterns.py \
  find \
  --dangerous=-delete --dangerous=-exec \
  --action ask \
  --output /tmp/find-guard.json
```

### 4.3 CLI Reference

| Argument | Description |
|---|---|
| `command` | Command name (positional) |
| `--dangerous` / `-d` | Repeatable — dangerous substrings to guard. Use `=` form for dash-starting values: `--dangerous=-f` |
| `--action` | Action for dangerous patterns: `ask` (default) or `deny` |
| `--base-action` | Action for the broad allow: `allow` (default), `ask`, or `deny` |
| `--display` | Print human-readable ordering explanation alongside JSON |
| `--output <file>` | Write JSON to file instead of stdout |

### 4.4 Spec Files

Test specs for common commands are in the [`specs/`](specs/) directory. Run them
against the actual opencode config using the
[opencode-permission-config `verify-permission-pattern.py`](../opencode-permission-config/scripts/verify-permission-pattern.py):

```bash
OPENCODE_PERMISSION_CONFIG=~/.config/opencode/opencode.json \
  python3 ../opencode-permission-config/scripts/verify-permission-pattern.py \
  --spec specs/awk-guard.json
```

**Behavioral Verification Note:** While spec-based testing confirms fnmatch pattern
correctness, real-command verification (SEE [`opencode-permission-config` §4.5](../opencode-permission-config/SKILL.md#real-command-verification-protocol))
is required for runtime validation. Test ask/deny patterns one command at a time
to ensure accurate enforcement.

***

## 5. Worked Examples

### 5.1 awk — `system()` and `-f`

The conversation that originated this technique. awk's dangerous forms are
`system()` (executes arbitrary shell commands) and `-f <script>` (runs a script file).

Patterns generated:

```json
{
  "*": "ask",
  "awk *": "allow",
  "awk *system*": "ask",
  "awk *-f*": "ask"
}
```

Verification:

| Command | Expected | Matches | Verdict |
|---|---|---|---|
| `awk '/pat/,0' file.txt` | allow | `awk *` | allow ✓ |
| `awk -f /tmp/evil.awk` | ask | `awk *` then `awk *-f*` | ask ✓ |
| `awk '{system("ls")}'` | ask | `awk *` then `awk *system*` | ask ✓ |

### 5.2 find — `-delete` and `-exec`

`find` with `-delete` removes files found; `-exec` can run arbitrary commands.

Patterns:

```json
{
  "*": "ask",
  "find *": "allow",
  "find *-delete*": "ask",
  "find *-exec*": "ask"
}
```

Verification:

| Command | Expected | Verdict |
|---|---|---|
| `find . -name "*.py"` | allow | allow ✓ |
| `find . -delete` | ask | ask ✓ |
| `find . -exec rm {} +` | ask | ask ✓ |
| `find . -type f -name "*.tmp"` | allow | allow ✓ |

### 5.3 sort — `-o <file>`

`sort -o <file>` overwrites the input file in-place.

Patterns:

```json
{
  "*": "ask",
  "sort *": "allow",
  "sort *-o*": "ask"
}
```

Verification:

| Command | Expected | Verdict |
|---|---|---|
| `sort file.txt` | allow | allow ✓ |
| `sort -u file.txt` | allow | allow ✓ |
| `sort -o file.txt file.txt` | ask | ask ✓ |
| `sort -r -o /tmp/out.txt data.txt` | ask | ask ✓ |

***

## Composition Rationale

This skill is a **base skill**: it owns a generic pattern-design technique (broad-allow
+ narrow-deny/ask with last-match-wins ordering) that is domain-agnostic and applies to
any permission system using fnmatch-based glob matching. The companion script generates
correctly-ordered JSON patterns for any command + any set of dangerous substrings.

It is consumed by:

- **`opencode-permission-config`** — applies the technique to opencode's permission
  system, using the worked examples (awk, find, sort) as concrete additions to the
  config and documenting the design decisions in §6.

## Related Skills

- **`is-this-command-safe`** — command safety classification. Determines which
  commands are SAFE-WITH-QUALIFICATION and what their dangerous forms are.
- **`opencode-permission-config`** — opencode-specific permission configuration.
  Consumes this skill's pattern technique for real config updates.
- **`command-autoapprove-onboarding`** — complementary VS Code auto-approve
  configuration (regex-based, not fnmatch).

## Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| [`opencode-permission-config`](../opencode-permission-config/SKILL.md) | Applies the content-guard technique in §6.5.1 and §6.9 for concrete awk/find/sort pattern additions to opencode.json. Consumes the pattern-generation script to produce correctly-ordered JSON patterns; documents the design decisions in its Pattern Design Decisions section. |
