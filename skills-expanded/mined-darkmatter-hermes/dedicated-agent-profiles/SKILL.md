---
name: dedicated-agent-profiles
description: >-
  Carve a restricted, single-purpose Hermes agent out of a named profile —
  pinned model, minimal toolsets, 2-3 skills, curated MCP — for a recurring
  automation class (browser driving, payments, watchdogs) when the
  general-purpose agent is too slow, too noisy, or keeps derailing. Use when
  the user says "set up an agent for this", "limit the tools so this doesn't
  keep happening", or a task class repeatedly fails from tool/context bloat.
version: 1.0.0
metadata:
  hermes:
    tags: [hermes, profiles, agents, toolsets, isolation]
    category: devops
    related_skills: [hermes-agent]
---

# Dedicated agent profiles (restricted single-purpose Hermes agents)

When one class of work keeps failing under the general-purpose agent (slow
per-step probing, wrong skill loading, context bloat, model too big for the
loop), the fix is a **named Hermes profile configured as a purpose-built
agent**: one pinned model, a handful of toolsets, only the skills that govern
that work, and only the MCP servers it needs. Validated 2026-08-03 building
the `studio` browser-drive agent.

## Signals this is the right fix

- User: "this keeps happening", "set up an agent responsible for this",
  "with limited tools and skills".
- The same task class repeatedly burns time on wrong approaches (e.g.
  one-element-at-a-time form probing instead of one vision sweep).
- A workflow needs a cheap/fast model (gemini-3.6-flash) while the main
  session runs a big model.

## Playbook (exact commands)

1. **Pick or create the profile.** `hermes profile list` — reuse an existing
   named profile if one matches; else `hermes profile create <name>`.
   Profile home: `~/.hermes/profiles/<name>/` (config.yaml, skills/, .env,
   SOUL.md, cron/, memories/).
2. **Pin the model.** Verify it's live first (catalog + 1-line completion),
   then:
   ```bash
   hermes -p NAME config set model.default google/gemini-3.6-flash
   hermes -p NAME config set model.provider openrouter
   ```
3. **Lock down toolsets** to the minimum the task needs:
   ```bash
   for t in web browser code_execution image_gen x_search tts session_search delegation cronjob computer_use; do
     hermes -p NAME tools disable "$t"
   done
   hermes -p NAME tools list   # verify what stays enabled
   ```
   Typical browser-drive agent keeps: terminal, file, vision, skills, todo,
   memory, clarify (+ its MCP server's tools).
4. **Prune skills to the 2-3 that govern the work.** Profile creation clones
   the skill library — wipe the clone:
   ```bash
   cd ~/.hermes/profiles/NAME/skills
   chmod -R u+w .                 # clones are read-only (nix-style, epoch-1 mtimes)
   rm -rf */ .archive             # see pitfall: protect keepers FIRST
   mkdir -p ops devops            # recreate category dirs
   cp -R ~/.hermes/skills/<cat>/<keeper> <cat>/
   ```
   Then **stop re-injection**:
   ```bash
   touch ~/.hermes/profiles/NAME/.no-bundled-skills
   ```
   Without this marker, the next hermes launch re-syncs bundled skills and
   silently undoes the prune (marker makes `sync_skills()` a no-op; delete the
   file to opt back in). Verify: `hermes -p NAME skills list` shows ONLY keepers.
5. **Curate MCP servers.** Remove unrelated ones, test the keeper:
   ```bash
   hermes -p NAME mcp remove <unrelated>
   hermes -p NAME mcp test <keeper>   # must discover its tools
   ```
6. **Optional:** `hermes -p NAME config set curator.enabled false` so the
   curator never reshuffles the deliberately-pruned library.
7. **Write `~/.hermes/profiles/NAME/SOUL.md`** — the agent's mission: what it
   owns, its one loop (name the skill), its stop conditions, and style
   ("report state changes with evidence, no narration"). This is injected
   every session; keep it < ~30 lines.
8. **Alias for direct invocation:** `hermes profile alias NAME` →
   `~/.local/bin/NAME`.
9. **Smoke test** before handing real work:
   ```bash
   hermes -p NAME chat -q "Answer one line each, no tools: (1) what exact
   model are you? (2) list the skill names you can see. (3) is
   mcp__<server>__<tool> available?"
   ```
   Pass = correct model name, exactly the keeper skills, MCP tool visible.
10. **Hand off work as one self-contained prompt** (the profile has NO memory
    of your session — pass every path, URL, and boundary in the task text):
    ```bash
    hermes -p NAME chat -q "$(cat /tmp/task.txt)" > /tmp/NAME-run.log 2>&1
    ```
    Run it in the background with notify-on-complete for anything > 1 min.
    Resume a half-finished run: `hermes --resume <session> -p NAME`.

## Pitfalls

- `-Q chat` is not a flag — it's `hermes chat -q "..."` under a profile.
- **Marker before first run.** Prune skills, THEN touch `.no-bundled-skills`,
  THEN launch; otherwise the launch re-injects bundled skills over your prune.
- **Read-only clones:** profile skill copies are `r--r--r--` with Dec 31 1969
  mtimes; plain `rm -rf` fails per-file. `chmod -R u+w` first.
- **Protect keepers when wiping:** a `for d in */` delete loop matches keeper
  dirs too (lost `ops/`+`devops/` once to a trailing-slash glob). Move keepers
  out or case-exclude them explicitly; restore from `~/.hermes/skills/` if hit.
- **Smoke-test models directly:** some models return reasoning text with an
  empty final answer on vague prompts — ask direct one-line questions and
  verify the catalog + a completion before pinning.
- Profile memory/memories are separate stores — the dedicated agent does not
  see the default profile's memory. Everything it needs goes in the task text
  or its own skills/SOUL.
- Toolset disables are per-profile; the default profile is unaffected (this
  is the point — the main session keeps full tools).
- **Profile skill copies are snapshots.** With `.no-bundled-skills` set, a
  patch to `~/.hermes/skills/.../SKILL.md` does NOT propagate to the
  profile's copy — the dedicated agent keeps running the stale rule. After
  patching a skill the profile uses (e.g. financial-operations §6 pre-approval
  rule, 2026-08-03), `cp` the file to
  `~/.hermes/profiles/NAME/skills/<cat>/<skill>/SKILL.md` in the same step.

## Verification checklist

- `hermes -p NAME skills list` → exactly the keepers, no bundled names.
- `hermes -p NAME tools list` → only intended toolsets enabled; only intended
  MCP servers listed.
- Smoke test answers match (model, skills, MCP tool).
- One real end-to-end run completes or stops at a declared boundary with
  evidence — never "it should work".
