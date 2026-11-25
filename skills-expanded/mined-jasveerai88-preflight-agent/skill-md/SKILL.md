# preflight-agent — agent skill

Scan an AI-agent setup before it runs. Use it
whenever a task involves opening, installing, or
trusting a folder that carries agent configuration —
a cloned repo with `.claude/`, an MCP config someone
handed you, a settings file whose hooks you rely on
for safety, a folder of agent definitions, a skills
tree — when the question is "what is already wrong
with this setup, before anything executes?"

It is the merged suite of five static auditors
(clone-guard, secret-guard, hook-doctor, fleet-audit,
skill-sprawl), each also runnable on its own. All
read-only, local, stdlib-only; no scan executes,
imports, or installs anything in the target.

## The commands

```bash
preflight-agent scan DIR [--home DIR] [--json]
preflight-agent clone-guard DIR [--json]
preflight-agent secret-guard scan FILE... [--json]
preflight-agent secret-guard fix FILE... [--apply] [--json]
preflight-agent hook-doctor audit SETTINGS [--home DIR] [--json]
preflight-agent fleet-audit audit FOLDER [--json]
preflight-agent skill-sprawl audit FOLDER [--json]
```

(Install with `pipx install preflight-agent`; from a
source checkout, prefix with
`python3 src/preflight_agent.py`. Suite version
1.0.2 — each module still reports its own source-tool
version, v0.1.0, inside its sections and JSON.)

- `scan` is the one-shot preflight: all five modules
  over one setup folder, one combined receipt. Target
  discovery per module is documented in README.md —
  most importantly, a module with nothing to audit
  reports **skipped with a reason**, never clean.
- Exit codes everywhere: **0** clean, **1** findings,
  **2** usage/input error. In `--json` mode every
  error — including argument errors — is one JSON
  object with an `error` key. Never a traceback.
- **Read-only scanning.** The single exception is
  `secret-guard fix --apply`: it writes only the
  files it is handed, after a dry run by default,
  keeping a timestamped backup of each changed file.
  `scan` never invokes it.

## What each module decides

| Module | Verdict vocabulary | Clean means |
|---|---|---|
| clone-guard | AUTO-RUN / INSTALL-TIME / PRESENT / UNPARSEABLE per surface | none of the checked auto-execution surfaces (Claude/VS Code/devcontainer configs, npm install scripts, direnv, git/husky hooks) were found |
| secret-guard | INLINE-SECRET / ENV-LITERAL / UNPARSEABLE per file | no secret-named key holds a literal and no env block holds a secret-shaped literal, in the files checked |
| hook-doctor | ERROR / WARNING / INFO per hook | no hook is dead as configured: matchers can fire, guards can block, command paths exist |
| fleet-audit | ERROR / WARNING / INFO per agent | no name duplicates, no description collisions at the stated thresholds, grants match the promised job shape |
| skill-sprawl | ERROR / WARNING / INFO per skill | no cross-scope duplicates or collisions, no oversized bodies, the discovery listing fits the stated budget |

## JSON contract

One object per command. Module commands emit exactly
the object their standalone tool emits
(`tool`, `version`, `command`, the module's own
sections, `clean`). `scan` emits one object:
`tool: "preflight-agent"`, `command: "scan"`, `dir`,
`home`, `modules` (a per-module section — the
module's own object plus its `exit_code`; skipped
modules carry `status: "skipped"`, a `reason`, and
`clean: null`), `summary` (modules run / skipped /
clean / with findings), and the combined `clean`.

## Limits (the honest list)

- Static evidence only. clone-guard reports surfaces
  that *would* execute, not what the code does once
  running; a CLEAN scan is never a safety guarantee.
- secret-guard checks JSON configs it can parse;
  values under ordinary key names outside env blocks,
  and TOML/YAML configs, are out of its scope — and a
  secret that was ever committed stays leaked after
  moving it: rotate it.
- hook-doctor judges hooks against a static rule
  table; it never runs a hook, so runtime behaviour
  (a script that exists but misbehaves) is invisible
  to it.
- fleet-audit / skill-sprawl similarity is a token-set
  Jaccard heuristic at stated thresholds (collision
  0.50, near-identical 0.90, short-description floor
  40 chars, discovery budget 16,000 listing chars) —
  a reported figure, not a platform guarantee.
- `scan`'s discovery is a convention, stated in the
  README: it audits the settings/config/agents/skills
  locations it looks for. A setup that keeps those
  elsewhere needs the module commands pointed at the
  real paths directly.
- Pinning a module means accepting its limits: each
  module's own report prints the full list for its
  checks, and those texts govern over this summary.
