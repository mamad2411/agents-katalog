---
name: deslop
description: "Refactors a file or directory to remove AI slop — duplication, dead code, speculative abstraction, bloated functions — without changing observable behaviour. Takes a path argument. Invoke with /slop-guard:deslop <path>."
agent: deslop
context: fork
user-invocable: true
---

# Deslop — /slop-guard:deslop <path>

Invokes the `deslop` subagent to remove AI-generated code bloat from the given path.

## $ARGUMENTS contract

`$ARGUMENTS` is a file path or a directory path, optionally followed by:
- `--dry-run` — report the plan; change nothing.
- `--tests <cmd>` — shell command that proves behaviour is unchanged, run before and after edits.

If the path is missing or does not exist: print one line explaining why, change nothing.

Directory default: refactor one file at a time. Never rewrite an entire directory tree in a single edit.

## Refactor order

Apply in this priority; each category is a separate pass:

1. **Dead and unreachable code** — delete unused symbols, unused imports, unreachable branches, and unused parameters. This is the second-strongest AI-slop signal (34–43 % of all smells in LLM output per arXiv:2508.14727).

2. **Duplicated blocks** — extract any block that appears three or more times, or any duplicated block of five or more lines that appears twice. Count body lines only: a declaration or signature line does not count toward the five. Two occurrences of three or fewer lines: leave alone. Threshold reflects GitClear 2025/2026 data (8x rise in ≥5-line duplicate blocks; 73 duplicate blocks per million lines). jscpd reports *textual* clones; before extracting, confirm the copies are *behaviourally* the same — same inputs, same failure handling, same state touched. Two blocks that differ in a visibility rule, a payload field or an error path are not one helper, and sharing them leaves every caller configuring the exception. Apply the deletion test: the extraction must remove more lines than it adds, counting the new helper and its call sites; if it does not, leave both copies and say so in the report.

3. **Speculative abstraction** — delete interfaces with one implementor, factories that build one type, configuration knobs with one caller, wrappers that only forward. YAGNI applies. Tiebreaker against the public-API constraint below: when the abstraction *is* public API, keep the name and collapse what sits behind it. A factory imported by a test stays; the class hierarchy it hid does not.

4. **Functions that do more than one thing** — split only when responsibilities can be cleanly separated. Function length and cyclomatic complexity are supporting signals only; neither justifies a rewrite on its own.

5. **Standard library replacements** — replace hand-rolled code with the standard library or an existing project helper when the replacement is a direct equivalent.

6. **Comment noise** — delete comments that restate what the code says, and all commented-out code.

## Hard constraints

- Observable behaviour and public API stay identical unless the user explicitly asked otherwise. **Public API** here means: any symbol imported, required, or called from outside the file, including from tests; any symbol exported by the module's own export list; and, absent both, any symbol whose name does not start with the language's private marker (`_` in Python, lowercase initial in Go, `#`/`private` in TS). When in doubt, treat it as public and keep it.
- No test is skipped, deleted, or weakened — AP-AGENT-003.
- No suppression comment is added to silence a finding — AP-AGENT-001.
- No new dependency is added — AP-AGENT-004.
- No linter threshold or baseline is relaxed — AP-AGENT-002.
- Edits stay inside the requested path — AP-AGENT-007.
- Formatting is not slop. Preserve the file's existing blank-line separation, indentation, and quote style; a deletion pass must not close the gaps between surviving declarations. If the project has a formatter, run it at the end; if it does not, leave layout exactly as found.

## Procedure

1. Read the target file or directory listing.
2. Identify candidates against the refactor order above. That list is the definition of slop for this command. The per-language antipatterns skills — `python-antipatterns`, `go-antipatterns`, `php-antipatterns`, `ts-react-antipatterns`, `node-antipatterns`, and their `reference/<AP-ID>.md` pages — cover security and performance, not slop categories: read the one for the file's language so a refactor does not introduce an AP violation, and do not expect to find dead-code or duplication guidance there.
3. If `--tests <cmd>` was supplied, run it now and record the baseline result before touching any file.
4. Apply one category at a time, most-valuable first.
5. After each edit, read the slop-guard `PostToolUse` hook findings and resolve them; do not suppress. Outside a hook-enabled session no findings appear — then re-read the edited region yourself and move on; absence of hook output is not a pass.
6. Re-run the test command after all edits complete.
7. Report a diff summary: categories applied, lines removed vs added, and one verification line per file.

## Report format

For each file processed:

```
file: <path>
categories applied: <comma-separated list>
categories with no findings: <comma-separated list, or "none">
lines removed: N  lines added: M
behaviour: unchanged (verified by <cmd>)
  — OR —
behaviour: unverified (no test command given)
```

Only claim verification when the test command was supplied and passed.

## When to refuse

Refactoring a file with no test coverage and no `--tests` command is a risk, not a silent default. The agent proceeds only for pure deletions — dead code, unused symbols, commented-out code — because a deletion that compiles and leaves every call site intact cannot change behaviour. Extracting duplicated blocks is restructuring, not deletion: it waits for a test command. The agent stops before any behaviour-bearing change and reports: "No test command supplied. Proceeding with pure deletions only; skipping duplicate extraction and behaviour-bearing restructuring."
