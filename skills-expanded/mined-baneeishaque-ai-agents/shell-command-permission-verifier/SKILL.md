# shell-command-permission-verifier (Base Skill)

**Category:** `Base-Utility`
**Tier:** Tier-1 Python script (stdlib `json`, `tomllib`, `re`, `fnmatch`, `argparse`,
`hashlib`, `os`, `sys`, `pathlib`); see `scripting-language-selection-rules.md` §3 (no shell
tier needed — this performs pure computation + file parse, no orchestration/shell-out).

## Purpose

Replay a shell command through each assistant's **native** shell-permission backend and return
its exact runtime verdict (`allow` / `ask` / `ask_user` / `deny`). This is the SSOT for
"what would X approve?" — the composer
[`cross-tool-shell-command-permission-sync`](../cross-tool-shell-command-permission-sync/SKILL.md)
shells out to this script rather than re-implementing the engines.

## Engines (ground truth, verified at execution)

Each engine parses its native config and simulates the **exact** match algorithm, not an
abstraction. Do not simplify the matchers (see `ide-renderer-freeze-prevention` §2.3): a single
regex-quantifier drift breaks last-match-wins parity.

| Engine | Config (default path, overridable by env) | Data shape | Match algorithm | Default |
| --- | --- | --- | --- | --- |
| `opencode-glob` | `$OPENCODE_CONFIG` → `$XDG_CONFIG_HOME/opencode/opencode.json` (defaults to `~/.config/opencode/opencode.json`, symlinked via dev-env-private-config-symlink into `~/lab-data/configurations-private/opencode/config/`) | `permission.bash` = **object** mapping pattern to action: allow, ask, or deny (170 entries) | last-match-wins (`findLast`) over wildcard matcher | `ask` |
| `kilo-glob` | `$KILO_CONFIG` → `~/.config/kilo/kilo.jsonc` | `permission.bash` = **object** (121 entries) | identical to opencode | `ask` |
| `claude-fnmatch` | `$CLAUDE_CONFIG` → `~/.claude/settings.json` | `permissions.allow` = **list** of strings (109) | any `fnmatch` match → allow | `ask` |
| `copilot-regex` | `$COPILOT_SETTINGS` → `~/Library/Application Support/Code - Insiders/User/settings.json` | `chat.tools.terminal.autoApprove` = **list** of `/regex/flags` strings (55) | any `re.search` (anchored `^…$`) → allow | `ask` |
| `gemini-regex-toml` | `$GEMINI_SAFE_COMMANDS` → `~/.gemini/policies/safe-commands.toml` | `[[rule]]` tables w/ `toolName`, `commandPrefix[]`, `commandRegex`, `decision`, `priority` (14) | highest-priority tier, first match in document order → decision | `ask_user` |

### Opencode/kilo wildcard matcher (ported verbatim from `@opencode-ai/core util/wildcard.ts`)

- Input backslash-normalized: `\` → `/`.
- Pattern specials **only** `. + ^ $ { } ( ) | [ ] \` are escaped (space and `-` stay literal).
- `*` → `.*`, `?` → `.`.
- Pattern ending in `.*` (literal space-star): the trailing `.*` becomes `( .*)?` — so
  `git status *` matches both `git status` and `git status -s`.
- Anchors: `^pattern$` (full match), single-line (`s`).

This means `commandPrefix=["date "]` in Gemini does **not** match bare `date` (the trailing
space is part of the prefix) — confirmed: `date` without a trailing space → `ask_user`,
`date` with a trailing space → `allow`.

## Files

```text
shell-command-permission-verifier/
├── SKILL.md            ← this file
├── AGENTS.md           ← per-skill AGENTS (§2.3 conventions)
├── scripts/
│   └── verify-verdicts.py
└── specs/
    ├── opencode-readonly.spec.json        # allow family (docker/git-submodule/audit)
    ├── opencode-dangerous.spec.json       # ask family (destructive git, chains, mkdir, --outfile)
    ├── cross-tool-align.spec.json         # per-engine verdict regression baseline (asserts real divergence)
    └── gemini-priority.spec.json          # priority-tiering + lookahead + prefix-spacing + default
```

## Invocation

```bash
# all engines + all bundled specs
python3 scripts/verify-verdicts.py --strict

# scope engines + pick specs
python3 scripts/verify-verdicts.py spec-x.json --tools opencode,claude

# one-off command verdicts to stdout
python3 scripts/verify-verdicts.py --cmd "git status" --tools opencode,kilo --json
python3 scripts/verify-verdicts.py --cmd "mkdir -p tmp" --json
```

## Output

- Human table (default): per-command verdict colored + `PASS/FAIL` + summary `N commands checked, M mismatch[es]`.
- `--json`: one JSON object per spec (`description`, `tools`, `results` with `pass` flag, `fails`).
- Exit code: `0` always except `--strict` returns `1` on any mismatch; `2` on usage/config errors.

## Spec format

```json
{
  "description": "human label — must cite the ground-truth source",
  "commands": [
    {"command": "<exact shell string>", "expect": {"gemini": "allow"}}
  ]
}
```

A command's `expect` asserts verdicts **only** for the engines it names (specs are scoped to
the engines that carry the command — e.g. the opencode specs name `opencode`/`kilo`, the
gemini spec names `gemini`, cross-tool-align names all five). Tools omitted from `expect` are
intentionally not checked.

## Stability / safety

- `md5`-stable: outputs are deterministic; re-running yields byte-identical results (the
  composer compares a golden hash before writing any config).
- No writes: this script is read-only. Mutating config writes live in the composer.
- Missing config → `MissingEngine` returns `none` (never a false allow).

## Rule Compliance Reference

- `ai-agent-rules/scripting-language-selection-rules.md` §3 (Python tier for I/O + computation).
- `ai-agent-rules/scripting-language-selection-rules.md` §4 (no shell tier).
- `ai-agent-rules/shell-execution-rules.md` §2.3 (atomize, no nested heredocs, bound
  output).
- `ai-agent-rules/ide-renderer-freeze-prevention/SKILL.md` (do not collapse matcher rules).
- `ai-agent-rules/redaction-portability/SKILL.md` (configs contain absolute
  `/Users/dk/...` paths — never log verbatim in committed fixtures).
- `ai-agent-rules/markdown-generation/SKILL.md` §3 (headings, code fences).
- `ai-agent-rules/planning-artifact-naming/SKILL.md` (artifact naming formula).
