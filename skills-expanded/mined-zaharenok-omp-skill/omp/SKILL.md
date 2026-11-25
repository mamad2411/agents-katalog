---
name: omp
description: "Delegate coding to the omp terminal coding agent."
version: 1.0.0
author: Oleg Zakharchenko
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, omp, Oh-My-Pi, Code-Review, Refactoring, Subagents]
    related_skills: [codex, claude-code, opencode]
---

# omp — terminal coding agent

Delegate coding work to [omp](https://omp.sh) (Oh My Pi) from your agent's
shell/terminal tool (examples use Hermes `terminal(...)` syntax; the same
commands run through any Bash/shell tool).
omp is a terminal-first coding agent combining repo search, file edits, shell,
LSP code intelligence (semantic renames, references, diagnostics), live DAP
debugging, headless browser, GitHub integration, plan mode, and parallel
subagents — with resumable local sessions.

Full docs: https://omp.sh/docs (sidebar indexes every page).
Local deep-dives: [references/cli-reference.md](references/cli-reference.md),
[references/capabilities.md](references/capabilities.md).

## When to choose omp

- **Multi-file refactors needing semantics** — omp drives the language server:
  safe cross-file renames, find-references, apply LSP fixes.
- **Runtime bugs** — omp can attach a real debugger (DAP): breakpoints, step,
  read locals from a live process.
- **Large/risky changes** — plan first (`--plan-yolo` headless, or two-step
  plan→implement), then execute.
- **Parallelizable audits** — omp fans out its own subagents (scout, reviewer,
  security-reviewer…): one omp call replaces several of your own subagents.
- **One-shot build/fix/test loops** in any repo (no git repo required, unlike
  codex).

Prefer a plain shell + find/replace for single-file trivial edits (no model
round-trip). Prefer codex/claude-code when the user names them explicitly.

## Core patterns (verified on omp 18.1.18, macOS)

### One-shot — the default

```
terminal(command="omp -p --no-session --max-time 600 'Fix the failing test in src/parser.test.ts, run it, explain the root cause in 3 lines.'", workdir="<repo>")
```

Rules:
1. **Always `-p`** (print mode) — no TUI, streams to stdout, exits.
   Note: `-p` does NOT disable sessions — it only skips the TUI; the session
   is still saved unless `--no-session` is passed.
2. `--no-session` ONLY for throwaway scratch tasks. On real projects omit it:
   omp sessions accumulate project knowledge (investigations, decisions, file
   context), and continuing with `-c` reuses that context instead of
   re-explaining the codebase from scratch.
3. **Always `--max-time <s>`** (600, 10m, 1h) so a stuck run can't hang the call.
4. **Always `workdir=<project root>`** — launch dir = project root; LSP needs
   the marker (package.json, Cargo.toml, go.mod, pyproject.toml) directly in
   that dir; discovery never walks parents.
5. From `$HOME` add `--allow-home`.

### Long tasks → background

```
terminal(command="omp -p --max-time 3600 'Migrate the job queue to Postgres; keep public API; run full test suite after.'", workdir="~/proj", background=true, notify=true)
# then poll the background process / read its log
```

### Multi-turn with memory — keep the session (PREFERRED on real projects)

omp sessions store accumulated project knowledge: past investigations,
decisions, file context. If the project already has omp sessions, CONTINUE
them rather than starting cold:

```
terminal(command="omp -p --max-time 600 'Investigate src/auth: map every entry point, report, do NOT edit.'", workdir="~/proj")   # session SAVED
# …next turn / next day:
terminal(command="omp -c -p --max-time 900 'Good. Now implement fix #2 from your report and verify.'", workdir="~/proj")
```

- Before a new task on a known project, check for prior sessions:
  `ls ~/.omp/agent/sessions/` (stored per project path). If a relevant thread
  exists → `omp -c -p` (latest for that dir) or `omp -r <id-prefix> -p`
  (specific one). Fresh session only for genuinely unrelated work.
- `--no-session` is for one-off scratch/cleanups where residue is unwanted.
- Sessions are plaintext JSONL under `~/.omp/agent/sessions/` — they may
  contain secrets printed by commands (see Pitfalls).

### Structured output — json mode

`--mode json` emits newline-delimited events (`session`, `agent_start`,
`turn_start`, `message_start/update/end`, `turn_end`, …). Parse in Python and
take the LAST `turn_end` with `role=assistant` (a `-p` run may contain several
— agent self-continuations):

```python
import json, subprocess
out = subprocess.run(["omp","-p","--mode","json","--no-session","--max-time","300","PROMPT"],
                    capture_output=True, text=True, cwd=repo).stdout
answer = ""
for line in out.splitlines():
    try: ev = json.loads(line)
    except: continue
    if ev.get("type") == "turn_end" and ev.get("message",{}).get("role") == "assistant":
        answer = "".join(c.get("text","") for c in ev["message"].get("content",[]) if c.get("type")=="text")
```

json mode also exposes per-turn `usage`/`cost`. For embedding omp long-term in
a host program there is also `--mode rpc` (JSON-RPC over stdio), ACP, and a
TypeScript SDK — see references/capabilities.md.

### Plan-then-execute (risky changes)

- Headless: `--plan-yolo` forces read-only planning, auto-approves, then
  implements via `--plan-yolo-into <model>` (default smol role).
- Agent-driven review (safer):

```
omp -p --no-session "Draft a plan for X. Investigate, do NOT edit anything. Output the full plan as markdown."
# you review/edit the plan, then:
omp -p --no-session "Implement exactly this plan: <plan text>"
```

### Model selection

- `omp models` — list configured providers/models (doubles as auth probe);
  `omp models <provider>` filters; `omp models refresh` refreshes catalogs.
- `--model` fuzzy-matches (`opus`, `gpt-5.2`, `provider/model-id`).
- Roles: `--smol` fast/cheap, `--slow` deep reasoning, `--plan` planner;
  `--thinking off|minimal|low|medium|high|xhigh|max|auto`.
- Custom OpenAI-compatible endpoints: `~/.omp/agent/models.yml`
  (providers.<name>.baseUrl/api/apiKey/models; apiKey = env-var NAME first,
  literal second).

### Subagents inside one omp call

Phrase it in the prompt: "Parallelize: three file-disjoint workers, integrate
in the main session" or "Use the security-reviewer (read-only) to audit
src/auth, do not edit". Bundled specialists (case-sensitive): `scout` (read-only
recon), `designer` (UI/UX), `reviewer` (evidence-backed review),
`security-reviewer` (read-only security), `librarian` (external API research),
`task` (general), `sonic` (mechanical edits). Workers are separate model
sessions — cost multiplies; keep fan-out minimal, ownership file-disjoint.

## Safety / approvals

- omp default approval mode is **yolo** — everything runs unprompted (that is
  what makes headless `-p` work; a `prompt` policy would hang with no UI).
  Treat every omp run as delegated authority: explicit workdir, narrow prompt,
  `git diff` review after, never point it at production creds.
- If a config/profile sets `tools.approvalMode: prompt|always-ask`, a headless
  `-p` run will hang silently at the first non-read tool call — no TTY to show
  the prompt. For headless runs pass `--auto-approve` (or
  `--approval-mode yolo`) explicitly, and treat that as delegated authority.
- Read-only hard limit: `omp -p --tools read,grep,glob --no-session "…"`
  (also `--no-tools`, or per-tool deny via `--config` overlay:
  `tools.approval.<tool>: deny`).
- `--approval-mode write|always-ask` is interactive-only — do not rely on it
  in `-p` runs.

## Useful subcommands

| Command | Purpose |
|---|---|
| `omp models [provider]` | list models / probe auth |
| `omp config list/get/set <key> <val>` | settings (~/.omp/agent/config.yml) |
| `omp agents unpack [--project]` | export bundled subagent defs for editing |
| `omp commit` | generate commit message + changelog |
| `omp cleanse` | fix project diagnostics with parallel subagents |
| `omp usage` / `omp stats` | provider limits / usage stats |
| `omp plugin install/list` | marketplace plugins |
| `omp update` | self-update |

## Configuring omp itself (when the user asks)

- **MCP servers**: `.omp/mcp.json` (project) / `~/.omp/agent/mcp.json` (user);
  stdio (`command/args/env/cwd`) or `http`/`sse` (`url/headers`, explicit
  `type` required); `${VAR}` expansion in values; managed OAuth via
  `/mcp reauth <name>`. omp auto-imports Claude Code/Codex/Cursor/VS Code
  MCP configs — check `/mcp list` before duplicating.
- **Skills**: `~/.omp/agent/skills/<name>/SKILL.md` (user) or
  `.omp/skills/<name>/SKILL.md` (project); frontmatter `description` is the
  trigger; explicit call `/skill:<name>`. Also discovered from ~/.claude/skills,
  ~/.codex/skills, ~/.agent/skills, ~/.agents/skills, opencode dirs.
- **Config**: `~/.omp/agent/config.yml` global; `.omp/config.yml` project
  (exact launch dir only, no parent walk); profiles `omp --profile <name>`.
- **Project rules**: omp reads AGENTS.md in repo root automatically, plus its
  own rules/context files.
- More (hooks, custom tools, subagent authoring, TTSR, prompt templates,
  marketplaces): references/capabilities.md.

## Pitfalls

1. `-p` without `--max-time` can hang a shell call forever.
2. Quoting: the prompt is one shell arg — single-quote it; for long prompts
   write a file and use `omp -p "$(cat /tmp/task.md)"`.
3. LSP/DAP need the right server/adapter installed (typescript-language-server,
   debugpy, dlv…) and launch at the repo/package root.
4. Sessions store prompts/results/command output (incl. printed secrets) in
   plaintext JSONL — use `--no-session` for sensitive scratch work.
5. Bare `omp` opens an interactive TUI — always `-p` from an agent (or
   pty + background if the TUI is genuinely needed).
6. Subagent workspace isolation needs a git repo; isolated workers are not
   revivable after completion.
7. Env fallbacks: `PI_SMOL_MODEL`, `PI_SLOW_MODEL`, `PI_PLAN_MODEL`,
   `OMP_PROFILE`; `.env` chain: `./.env` → `~/.omp/agent/.env` → `~/.omp/.env`
   → `~/.env`.
8. `--list-models` is NOT a flag (some docs show it for older versions) — the
   subcommand is `omp models`.
9. Long prompts with quotes/interpolation: don't inline them in the shell
   command — write to a file and run `omp -p "$(cat /tmp/task.md)"` (also
   listed in Pitfall 2; this is the form that survives any shell quoting).
