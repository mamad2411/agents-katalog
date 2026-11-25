# cross-tool-shell-command-permission-sync (Composer Skill)

**Category:** `Tool-Configuration`
**Tier:** Tier-1 Python script (`json`, `tomllib`, `re`, `fnmatch`, `argparse`, `hashlib`,
`shutil`, `subprocess`, `os`, `sys`, `time`, `pathlib`); see
`ai-agent-rules/scripting-language-selection-rules.md` §3.

## Purpose

Synchronize the **read-only allow family** from opencode (`permission.bash` object, the SSOT)
into the other four shell-permission backends so that a read-only command auto-allowed by
opencode is also auto-allowed by Kilo, Claude, Copilot(VS Code), and Gemini — without
clobbering any unrelated existing rule. After every write, the base
`shell-command-permission-verifier` is invoked as a subprocess to confirm parity (the
composer never re-implements the verdict engines — see base SKILL.md §Rule Compliance).

## Why this exists

opencode's `permission.bash` is a hand-tuned 170-entry object where read-only families
(`docker ps*`, `git status*`, `git submodule status*`, `cat *`, `head *`, …) sit alongside
ask-guards (`*; *`, `git commit *`, `mkdir *`). Each tool encodes the same intent differently
(glob object, fnmatch globs, anchored regexes, TOSL priority tables), so the allow family
must be translated per target. This composer is that translation, with safety rails
(md5-stamped backups, ≥3s re-read stability, parse-check, dry-run).

## Translation table (SSOT pattern → target notation)

| Target | Format | Mapping | Identity / dedupe key |
| --- | --- | --- | --- |
| `kilo` | object glob | pattern verbatim → `{"pattern": "allow"}` | pattern string |
| `claude` | fnmatch glob | `Bash(<pattern>)` string | full string |
| `copilot` | anchored regex | opencode `*`→`.*` `?`→`.` specials escaped → `/^...$/` | regex string |
| `gemini` | TOSL `[[rule]]` | `commandRegex="^trans$"` `decision="allow"` `priority=100` | regex string |

opencode `*` (match-rest incl. spaces) → Copilot/Gemini `.*`; trailing opencode `*`
(optional args tail) → `( .*)?` to preserve optionality. The translator mirrors the base
engine's `wildcard_match` escaping exactly (`.+^${}()|[\]\\` escaped, space/`-`/`?` literal
except `?`→`.`).

## Safety guarantees

- **Read-only family only**: extracts entries whose action is `allow`; never touches ask/deny
  guards. The tool-specific destructive guards (opencode `*; *`, Gemini priority-300 chain
  guard, Gemini priority-200 `--outfile` guard) are NOT re-emitted — they are left intact
  and remain authoritative per tool.
- **Never clobber**: upsert by unique key; existing unrelated entries preserved.
- **Backup**: every config write is preceded by an md5-stamped backup copy
  (`<path>.syncbak.<ts>.<md5>`), never deleted.
- **Stability**: after write, the script sleeps ≥3s, re-reads, asserts the file's md5 is
  unchanged and re-parses successfully (catches opencode/VS Code runtime rewrites that drop
  edits — proven this session: opencode.json lost all custom rules; restored from kilo's copy).
- **`--dry-run`** prints proposed additions only; no writes.
- **`--verify-only`** runs the base parity check on current configs without writing.
- **No commits** — writes config files only; git staging/commit is out of scope.

## Invocation

```bash
# preview (no writes)
python3 scripts/sync-permission-rules.py --dry-run

# preview one target
python3 scripts/sync-permission-rules.py --dry-run --tools claude

# check current parity without writing
python3 scripts/sync-permission-rules.py --verify-only

# apply (writes + md5-stability + parse-check + base-verifier parity)
python3 scripts/sync-permission-rules.py
python3 scripts/sync-permission-rules.py --tools kilo,claude
```

## SSOT extraction

`patterns = [(pat, action) for pat, action in opencode["permission"]["bash"].items() if action == "allow"]`.
This yields 102 allow patterns at execution time (vs 68 ask/deny leaves + chain guards).
Only allow-family patterns are translated; the ask-leaves (`*; *`, `git commit *`, etc.)
are intentionally NOT propagated (each tool keeps its own defensive guards).

## Files

```text
cross-tool-shell-command-permission-sync/
├── SKILL.md            ← this file
├── AGENTS.md           ← companion bridge (§2.3 conventions)
└── scripts/
    ├── sync-permission-rules.py
    └── tool-registry.json   # <user-home>-placeholder path + format + shape map
```

## Rule Compliance Reference

- `ai-agent-rules/scripting-language-selection-rules.md` §3 (Python tier — file I/O + subprocess).
- `ai-agent-rules/scripting-language-selection-rules.md` §4 (no shell tier for orchestration).
- `ai-agent-rules/redaction-portability/SKILL.md` (`<user-home>` placeholders only in
  tool-registry.json; real paths used at runtime via env overrides).
- `ai-agent-rules/ide-renderer-freeze-prevention/SKILL.md` (output bounded; base verifier invoked with captured stdout).
- `ai-agent-rules/planning-artifact-lifecycle` & `versioned-artifact-superset-build` (plan amendments §11.1).
- Shell-execution: `bash` here is the opencode-permission bash rule family, which includes
  `bash`, `mkdir` (ask), `;`, `|`, `>`, `>>` (ask) — the composer's own `--verify-only`
  invokes `python3` (opencode `python3 *audit.py` allow; composer's path differs, but
  verify-only calls the base verifier which is read-only and already in the SSOT).
