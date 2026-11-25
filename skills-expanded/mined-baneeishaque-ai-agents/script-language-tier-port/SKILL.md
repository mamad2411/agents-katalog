---
name: script-language-tier-port
description: Audit an existing script that picked the wrong language tier
    (per scripting-language-selection-rules.md) and port it to its canonical
    tier — covers detection, line-by-line tier accounting, idiomatic
    translation, byte-parity smoke test, doc updates, and a single atomic
    refactor commit.
category: Meta-Automation
---

# Script Language Tier Port Skill (v1)

This skill operationalizes the **remediation half** of
[`scripting-language-selection-rules.md`](../../../ai-agent-rules/scripting-language-selection-rules.md).
That rule file defines the four tiers and tells you what to pick for a
**new** script. This skill tells you what to do when you discover an
**existing** script picked the wrong tier — typically a bash wrapper around
a `python3 -c …` or `python3 - <<PY … PY` heredoc, or a `.sh` file that is
~70 % systems-language work in shell clothing.

The motivating session: `resolve-vscode-setting.bash` was a 200-line bash
file in which ~150 lines were a Python heredoc doing the actual work. It
was ported to `resolve-vscode-setting.py` (pure stdlib) with byte-identical
output. That session IS the reference implementation of this protocol.

## 1. When to Apply

Apply when ANY of the following is true of a script under review:

- The body contains `python3 -c "…"` or `python3 - <<PY … PY` (nested
  heredoc — a §2.3.3 silent-hang hazard one careless edit away from
  triggering).
- The bash / sh body is ≤ 30 % native shell orchestration; the rest is
  string manipulation, JSON parsing, regex extraction, file I/O, or
  numeric work — all Tier-1 (Python) territory per §2.1 of the selection
  rules.
- A `.sh` file exists at all — `.sh` is not in the selection-rules matrix;
  bash with `.bash` extension is allowed only under documented
  justification per skill-factory §2.2.1.
- A PowerShell script's body is essentially `Invoke-WebRequest` +
  `ConvertFrom-Json` + a loop — Tier-1 territory (Python `urllib` +
  `json`), no Windows-administrative API involvement to justify Tier-2.
- A script written in any tier requires per-OS conditional branches the
  chosen language can't express naturally (e.g., bash hard-coding
  `/Applications/` for macOS with no portable Windows path story).

Do NOT apply when:

- The script genuinely IS ≥ 80 % native binary orchestration (Tier-2
  PowerShell is correct — see selection rules §3.2).
- The script is measurably CPU/memory/latency bound (Tier-3 candidate —
  see selection rules §4).
- The script is brand new and unshipped — use the selection rules
  directly, not this remediation skill.
- The wrong-tier script is in a frozen vendored dependency you cannot
  modify.

## 2. Operational Logic

### 2.1 Phase 0 — Detection

Read the candidate script and tally each non-comment, non-blank line into
one of three buckets:

| Bucket | Examples |
| :--- | :--- |
| **Native shell** | `cp`, `mv`, `find`, `grep`, `chmod`, redirections, pipes between binaries, `set -euo pipefail`, trap handlers, env var export, here-strings into native tools |
| **Cross-tier-shaped** | Arg parsing, path normalization, conditional path discovery — could be either tier; counts toward whichever bucket is bigger |
| **Tier-1-class** | JSON / regex / numeric work, brace-balance parsing, string templating, NLS resolution, structured output formatting, dataclass-like records — Python territory regardless of which language wrote it |

Decision rule (mirrors selection rules §2.2):

- ≥ 50 % Tier-1-class lines → port to Python.
- ≥ 80 % Native-shell lines AND zero Tier-1-class → keep as PowerShell
  (Tier-2 confirmed). Re-extension `.sh` / `.bash` to `.ps1` unless a
  documented bash justification exists per skill-factory §2.2.1.
- Mixed but neither dominant → port to Python; Python can call native
  binaries via `subprocess` cleanly, the reverse is the failure pattern
  this skill exists to fix.

### 2.2 Phase 1 — Idiomatic translation table

| Shell idiom | Python equivalent |
| :--- | :--- |
| `set -euo pipefail` | `def main() -> None:` + explicit `sys.exit(…)` on error paths; uncaught exceptions are already the equivalent of `set -e` |
| `if [ -f "$x" ]` | `Path(x).is_file()` |
| `if [ -d "$x" ]` | `Path(x).is_dir()` |
| `mktemp` | `tempfile.NamedTemporaryFile(delete=False)` (and `os.unlink` in `finally`) |
| Heredoc into temp file | `Path(p).write_text(content, encoding="utf-8")` |
| `grep -E pattern file` | `re.search(pattern, Path(file).read_text())` |
| `jq '.foo.bar'` | `json.loads(...)["foo"]["bar"]` |
| `case "$1" in …` arg parsing | `argparse.ArgumentParser` with `choices=(…)` |
| Pipe to `head -n N` | slice in memory or break out of the loop |
| Exit code propagation from `python3 -c` | direct `sys.exit(code)` |
| `find … -printf '%T@ %p\n' \| sort` | `sorted(Path(root).rglob("*"), key=lambda p: p.stat().st_mtime)` |
| `[ -z "$VAR" ]` env-var check | `if not os.environ.get("VAR"):` |

### 2.3 Phase 2 — Python authoring requirements

Every ported script MUST satisfy
[`scripting-language-selection-rules.md` §2.3](../../../ai-agent-rules/scripting-language-selection-rules.md):

- Shebang `#!/usr/bin/env python3`.
- `from __future__ import annotations` when supporting Python 3.9 (macOS
  system Python at time of writing) — required for `X | None` union
  syntax in function signatures.
- Stdlib-first: `argparse`, `json`, `pathlib`, `re`, `sys`, `subprocess`,
  `tempfile`, `os`. Adding a third-party dep requires explicit
  justification.
- UTF-8 I/O explicit: `encoding="utf-8"` on every `open` / `read_text` /
  `write_text` call (do not rely on platform default — Windows defaults
  to cp1252).
- Type hints on public functions.
- `if __name__ == "__main__": main()` entry point.

### 2.4 Phase 3 — Byte-parity smoke test

Before deleting the old script, run BOTH against a canonical input and
diff stdout:

```bash
./scripts/resolve-vscode-setting.bash workbench.editor.useModal > /tmp/old.out 2>&1
python3 scripts/resolve-vscode-setting.py workbench.editor.useModal > /tmp/new.out 2>&1
diff /tmp/old.out /tmp/new.out
```

Acceptable diffs are limited to:

- The trailing path / banner line that names the script itself.
- Whitespace at end-of-file (one trailing newline is canonical).

Anything else MUST be reconciled before proceeding — most commonly a
regex that matched greedily in shell but non-greedily in Python (`.*?`),
or a JSON field that bash extracted by `grep -o` and Python extracted
structurally (Python's version is correct; trust Python's).

### 2.5 Phase 4 — Documentation cascade

For a script that lives inside a skill:

1. **`SKILL.md` script reference paragraph** — update filename, language
   line ("Python 3.9+ per scripting-language-selection-rules.md §2"),
   dependency list.
2. **`SKILL.md` invocation block** — `python3 path/to/script.py` (NOT
   `./script.py` — that requires execute bit + shebang resolution which
   varies on Windows).
3. **`SKILL.md` manual / script-less procedure section** — if it
   contained the same idioms in shell form, port them too.
4. **`AGENTS.md` one-line invocation** — same change.
5. **Drop any "Bash Extension Mandate" justification block** — it no
   longer applies.

### 2.6 Phase 5 — Atomic commit

Per [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md),
the port is a single coherent refactor. One commit:

- Renames / deletes the old `.bash` / `.sh` / `.ps1` script.
- Adds the new `.py` script.
- Updates the same skill's `SKILL.md` and `AGENTS.md`.

Subject template:

```text
refactor(<skill-name>): port <script> from <old-tier> to <new-tier> for <reason>
```

Body MUST cite the tier rule that justifies the port, the line-accounting
result from Phase 0, and the smoke-test outcome.

## 3. Failure Modes

| Symptom | Cause | Remedy |
| :--- | :--- | :--- |
| Smoke test diff shows extra fields in Python output | Python regex captured a structural field shell missed via greedy `.*` | Confirm Python output is correct against the source data; the diff is a bug fix, not a regression |
| Python script hangs on Windows where bash never did | Encoding mismatch on `open(... )` defaulting to cp1252 | Add `encoding="utf-8"` everywhere — selection rules §2.3 mandate |
| `str \| None` type hint raises `TypeError` on Python 3.9 | PEP 604 syntax not enabled | Add `from __future__ import annotations` at top of file |
| Ported script needs to invoke a native binary | Pure-Python rewrite over-corrected | `subprocess.run([...], check=True, capture_output=True, text=True)` is fine — the rule is "Python as the orchestrator", not "no subprocess" |
| PowerShell file passes Phase 0 with ≥ 80 % shell glue but uses §2.6 mojibake-hazard patterns | Wrong tier was Tier-2 5.1 specifically | Port to `pwsh` 7+ with `#requires -Version 7.0`, NOT to Python — see selection rules §3.4 |

## 4. Prohibited Behaviors

- **DO NOT** delete the old script before the byte-parity smoke test
  passes. Keep it on disk during the comparison; remove it in the same
  commit that adds the replacement.
- **DO NOT** port a §2.3.3 nested-heredoc bash script by "fixing the
  heredoc" — the script is the wrong tier; the heredoc is a symptom.
- **DO NOT** introduce third-party Python dependencies (`requests`, `pyyaml`,
  `click`) when stdlib (`urllib`, manual YAML if absolutely required,
  `argparse`) suffices. The selection rules §2.3 stdlib-first mandate
  applies to ports as much as to greenfield.
- **DO NOT** leave the bash-extension justification block in the SKILL.md
  after porting — it is now false documentation.
- **DO NOT** combine the port with unrelated changes (new features,
  refactors of other files) in the same commit. The port is the entire
  diff.

## 5. Composition with Other Skills

This skill is invoked BY (not from):

- [`skill-factory`](../skill-factory/SKILL.md) §2.2.1 — when a Factory
  audit on an existing skill finds a tier-violation script, the Factory
  delegates remediation here rather than inlining the port logic.
- Any skill maintenance session where a script-touching change reveals
  the script is the wrong tier — port FIRST as its own commit, then
  proceed with the originally intended change.

This skill itself delegates to:

- [`scripting-language-selection-rules.md`](../../../ai-agent-rules/scripting-language-selection-rules.md) —
  authoritative tier definitions.
- [`shell-execution-rules.md` §2.3.3](../../../ai-agent-rules/shell-execution-rules.md) —
  the nested-heredoc hazard that motivates many ports.
- [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) —
  commit shape and Interleaving Mandate.

## 6. Related Skills

- [`skill-cross-reference-audit`](../general/skill-cross-reference-audit/SKILL.md) —
  automated audit for skill graph issues (duplicates, missing bridges, missing frontmatter)
- [`script-template-extraction`](../script-template-extraction/SKILL.md) —
  companion base skill for template extraction; run cross-reference audit after extraction
- [`vscode-setting-schema-discovery`](../vscode-setting-schema-discovery/SKILL.md) —
  the reference port (`resolve-vscode-setting.bash` →
  `resolve-vscode-setting.py`) that motivated authoring this skill.
- [`skill-factory`](../skill-factory/SKILL.md) — sister skill for *new*
  skill authoring; this skill is the *remediation* counterpart.
