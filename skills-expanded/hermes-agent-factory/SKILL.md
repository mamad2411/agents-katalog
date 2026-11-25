---
name: hermes-agent-factory
description: "Use when creating or cloning a Hermes agent profile."
version: 1.1.0
author: coordinator role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, profile, agent-creation, cloning, method, anti-bloat, seed, template]
    related_skills: [hermes-agent]
---

# Hermes Agent Factory

A repeatable method for building a new Hermes agent that is **lean, single-purpose, and ready for the user to configure**.

Core belief: a new agent is not "whatever the default gives you." Every toolset, skill, and line of SOUL.md is paid for **on every single turn, forever**. Start from nothing and add only what the role needs.

## The Shape (read this first)

```
  1. ROLE      -> one sentence. what it does, what it must NOT do
  2. CLONE     -> clone the lean seed profile
  3. SOUL      -> identity + hard limits
  4. TOOLS     -> strip to the minimum set
  5. SKILLS    -> only what the role needs
  6. KEYS      -> STOP. hand to the user.
  7. VERIFY    -> measure, test, clean up
```

Never skip step 1. Never automate step 6.

---

## Step 1 — ROLE

Write one sentence before touching anything:

> "<name> is the agent that <does one thing> on <which machine>."

Then answer three questions:

- **Scope** — what jobs are in? what jobs are explicitly out?
- **Reach** — which machine, which folders, which network? Does it need internet at all?
- **Danger** — what must it never do? (delete media, push to git, spend money, touch secrets)

If the sentence needs an "and", you probably want **two** agents. Split it.

One agent = one job. This is the whole point.

## Step 2 — CLONE

Clone from the lean template rather than starting from the fat default.

```bash
hermes profile create <name> --clone-from seed --description "<one-line role>"
```

Flags that matter:

| flag | effect | when |
|---|---|---|
| `--clone-from seed` | copies config.yaml, .env, SOUL.md, skills from `seed` | **the normal path** |
| `--clone` | same, but from whatever profile is currently active | when you're already in the template |
| `--clone-all` | full copy incl. all state | almost never — carries junk |
| (nothing) | blank profile with bundled skills | when there is no seed yet |
| `--no-skills` | blank, no bundled skills | **has a cost — see warning** |
| `--no-alias` | skip the `<name>` wrapper command | rarely; the alias is convenient |

**Warning on `--no-skills`:** it also opts the profile out of `hermes update` skill sync permanently. Leanest start, but the profile never receives new bundled skills. Prefer cloning a seed that already has few skills.

**Warning on cloning and `.env`:** `--clone` and `--clone-from` copy `.env`, which holds API keys. The new agent inherits every key the source had. That is convenient but it widens blast radius — a narrow agent gets keys it has no business holding. Review and strip what the role does not need (the user does this, not the agent — see step 6).

`--description` is not cosmetic: the kanban decomposer routes tasks by it. Write what the agent is *good at*, not its name.

## Step 3 — SOUL

`$HERMES_HOME/profiles/<name>/SOUL.md` is slot #1 of the system prompt, loaded verbatim every turn. Keep it tight — this is per-turn rent.

A lean agent SOUL needs four blocks and nothing else:

```
  IDENTITY   who it is, who it serves, what it does
  VOICE      how it reports (short, bullets, plain words)
  LIMITS     what it must never do  <- the important one
  REPORTING  what a finished job looks like
```

Target under ~2 KB for a single-purpose agent. A specialist does not need a philosophy.

The LIMITS block is what keeps a narrow agent narrow. Write the dangers from step 1 as flat prohibitions.

Write the file directly (SOUL.md is a plain file, hand-editing is correct here — unlike config.yaml).

## Step 4 — TOOLS

This is the biggest bloat source by far. Tool schemas dominate the prompt — typically **~40 KB against ~9 KB** of identity and skills combined. Cutting toolsets is the single highest-leverage move.

See `references/toolset-costs.md` for measured sizes and role presets.

Set the toolset list for the platforms the agent actually uses:

```bash
hermes -p <name> config set platform_toolsets.cli '[terminal, file, web]'
```

Rules:

- Start from the role, not from the default list. Ask "which of these does the sentence in step 1 require?"
- A headless worker agent does not need `clarify`, `tts`, `vision`, `image_gen`, or `computer_use`.
- `browser` + `browser-use` together cost ~7.9 KB. Only for agents that truly drive a browser.
- `delegation` (~4 KB) is only for orchestrators. A leaf worker never delegates.
- Configure **only the platforms in use**. If the agent is CLI-only, do not populate `platform_toolsets.telegram`.

Never hand-edit config.yaml. Always `hermes -p <name> config set`. A stray indent corrupts the file and can break a live gateway.

## Step 5 — SKILLS

Skills are cheap in the prompt (~80 B each for the index line) but expensive in attention and disk. The body only loads when triggered.

- Give the agent the skills its role needs, nothing more.
- Skills live in `$HERMES_HOME/profiles/<name>/skills/`.
- A single-purpose agent often needs **one** skill: the procedure for its own job.
- Write that skill *after* the agent has done the job once and been corrected — not from imagination.

## Step 6 — KEYS (stop here)

**The agent never handles credentials.** Not reading, not copying, not echoing, not moving them between profiles.

When the new profile needs an API key, bot token, or password:

1. Stop.
2. Tell the user the exact file path: `$HERMES_HOME/profiles/<name>/.env`
3. Tell them the exact variable name and format.
4. Let them type it.

Anything an agent reads reaches a remote model provider. Moving a key "just between local profiles" still routes it through the context window. There is no safe version of this.

Secrets in `.env`. Settings in `config.yaml`. Never the reverse.

## Step 7 — VERIFY

Measure, do not assume.

```bash
hermes -p <name> prompt-size          # the bloat number, offline, no API call
hermes -p <name> prompt-size --json   # machine-readable
hermes profile show <name>            # what it actually is
hermes -p <name> doctor               # health check
```

`prompt-size` prints the per-turn cost broken into stable / context / volatile tiers, plus every toolset and skill by size. **This is the anti-bloat instrument.** Record the number.

Rough targets for a single-purpose worker:

- tool schemas — under 15 KB (default is ~40 KB)
- stable tier — under 8 KB
- total system prompt — under 25 KB

Then smoke-test with a real job:

```bash
hermes -p <name> chat -q "<a small real task from its role>"
```

Then **clean up**: remove scratch files, test artifacts, half-written configs, and any profile you created while experimenting.

```bash
hermes profile delete <throwaway> --yes
rm -f ~/.local/bin/<throwaway>.bat   # Windows: delete leaves the wrapper behind
```

**Verified bug:** `hermes profile delete` on Windows removes the profile directory but leaves the wrapper script in `~/.local/bin/`. Always delete it by hand and confirm:

```bash
ls ~/.local/bin/ | grep <throwaway>   # must return nothing
```

Report what you removed.

---

## Building the seed template

The seed is a profile that exists only to be cloned. It is never chatted with.

It should hold: sane model/provider defaults, a minimal toolset list, a skeleton SOUL.md with the four blocks and `<PLACEHOLDER>` markers, and no memories or sessions.

See `references/seed-profile.md` for the build procedure and the SOUL skeleton.

After cloning from seed, **always** overwrite SOUL.md. A clone that still says `<PLACEHOLDER>` is a bug.

**Once an agent owns a field, route the field's questions to it — even the quick ones.** When the owner asks "give me a list of visual styles", the coordinator does not answer from its own head; it sends the question to the designer and relays the answer. The fleet only pays off if the specialist is the one consulted.

**`--clone-from seed` does NOT copy the `.no-bundled-skills` marker.** The clone
starts lean, but the first `chat` (or `hermes update`) silently syncs ~55 bundled
skills into it (verified: designer/qa/product went 10 → 64 after one test chat).
Right after creating the clone, copy the marker before the first run:
`cp seed/.no-bundled-skills <name>/` — then confirm after the smoke test that
`find <name>/skills -name SKILL.md | wc -l` still matches what you installed.

**Hub scanner verdicts need a human read, not a reflex.** `hermes skills install`
blocks community skills on pattern hits; some are real (a skill that spawns
sub-agents with `bypassPermissions` or runs `npm install -g`), some are false
(a security checklist flagged for *mentioning* `../` doc links). Fetch the
flagged lines from the raw repo, decide, then `--force` only for the false ones
and write the reason into the fleet plan.

## Cloning an agent onto a second machine

When the same role is needed on another box (same person, different OS), the
agent is **not** one agent in two places. It is two agents with the same
identity and **separate memories**. Design for that from the start.

### What travels, and what must not

| carries over unchanged | must be rewritten per machine |
|---|---|
| `SOUL.md` — identity is machine-independent | host facts: OS, shell, paths, interpreter versions |
| `USER.md` — who the user is | the fleet map (the twin is now a sibling) |
| `skills/` | any skill section naming a machine-specific project home |
| `config.yaml`, `profile.yaml` | — |

A `MEMORY.md` copied verbatim is the failure mode: the Linux clone then
"knows" it runs MSYS with drive letters and burns turns acting on it. Rewrite
the host block before the first session, not after the first confusion.

**Add an explicit twin-awareness line to the clone's memory**, e.g. "a twin of
this agent runs on <other machine>; the two do NOT share memory or sessions;
anything that must survive a machine switch goes in the project's git remote."
Without it, each side assumes its own notes are the whole truth.

### `export` carries state you probably do not want

`hermes profile export` packs the entire profile: `state.db`, `lsp/`, caches,
`pastes/`, logs, so the archive is far larger than the agent itself.
Credentials are stripped; bulk is not.

For a clone, hand-build the archive instead — it is the same import format:

```bash
cd $HERMES_HOME/profiles
tar -czf <out-dir>/<name>.tar.gz \
    <name>/SOUL.md <name>/profile.yaml <name>/config.yaml \
    <name>/memories/MEMORY.md <name>/memories/USER.md <name>/skills
hermes profile import ./<name>.tar.gz --name <name>   # on the target
```

The archive's top-level directory name becomes the profile name hint; `--name`
overrides it. Import creates the `~/.local/bin/<name>` wrapper automatically.

**Never include `.env`.** The clone starts with no credentials by design — the
user writes the key on the target machine. Tell them the exact path
(`$HERMES_HOME/profiles/<name>/.env`) and variable name, and stop there.

### Verify on the target, not on the source

```bash
hermes -p <name> prompt-size | head -15   # compare with the source's number
hermes -p <name> doctor | tail -20        # "no .env" here is expected, not a fault
find $HERMES_HOME/profiles/<name>/skills -name SKILL.md | wc -l   # same count as source
```

### Tar on Git-Bash rejects `C:/` paths

GNU tar reads a leading `C:` as a **remote host** and dies with
`Cannot connect to C: resolve failed` — for `-f` outputs and `-t` listings
alike. Use the MSYS `/c/<path>` form for tar's own arguments, even though native
tools on the same host need `C:/`. The two rules coexist; pick per tool.

### When `scp` resets on every large file

Some links (observed over wifi) accept ssh command execution fine but reset
the moment a bulk transfer starts: `Connection reset by peer`, zero-byte file
on the far side, reproducible, unaffected by `-l` rate limiting or
`-o Compression=no`.

The workaround that works: base64 chunks through plain `ssh` with a final md5
comparison — `scripts/push_chunked.py` in this skill.

```bash
python scripts/push_chunked.py <local-file> <remote-path> user@host 32768
```

Always compare checksums after any transfer that has failed once. A zero-byte
or truncated archive imports as `tarfile.ReadError: empty file` far from the
real cause, and a *partially* transferred one may not error at all.

## Distributing an agent

Two paths, different purposes:

| | `export` / `import` | `install` (distribution) |
|---|---|---|
| form | one `.tar.gz` | a git repository |
| use | one-time handoff or machine move | an agent you keep shipping |
| updates | none — re-export | `hermes profile update <name>` |
| carries | skills, memory, persona, crons, plugins, settings | SOUL, config, skills, crons, MCP |
| credentials | **stripped** | stay per-machine |

```bash
hermes profile export <name>                      # keys stripped automatically
hermes profile import ./<name>.tar.gz --name <new>
hermes profile install github.com/you/<repo> --alias
hermes profile update <name>                      # keeps local memories + .env
```

Export strips credentials, but it does **not** strip memories. `MEMORY.md` and `USER.md` can contain private facts, paths, and infrastructure details. Read both before sharing a profile with anyone.

## Lessons from real builds

- **The seed's `.env` holds only comments** — a clone starts with NO API key. Expect "no API keys yet"; the owner writes the provider key (e.g. `ANTHROPIC_API_KEY=`) into `profiles/<name>/.env` themselves.
- `hermes config set agent.reasoning_effort medium` may print "not a recognized config key" — check that the value landed in `config.yaml` (`hermes -p <name> config get agent.reasoning_effort`) before assuming it failed; the validator can lag behind the keys the code reads.
- **Interview before configuring**: when the agent wraps a third-party skill, ask one question at a time (privacy, network, model, paths, browser, toolsets, budget, channel, test set, cleanup, usage rule), each with options + a recommendation. The owner decides; configure only after the last answer.
- Third-party skills run via `uv run` with unpinned deps pull the newest version. For Playwright that demanded a newer Chromium build than the one installed. Pin the dep to the release that matches the installed browser instead of downloading a browser; record every local patch in a `VERSION.md` inside the skill folder with the pinned upstream commit.
- Vendoring a skill from a repo: `git clone` + `git checkout <commit>` into scratch, copy only `skills/<name>/`, drop `tests/`, never `npx skills add` (writes to Claude Code/Codex dirs, not Hermes).
- Deleting a profile on Windows: also `rm` the wrapper, any data root you created (e.g. `D:\<Name>`), the scratch clone, and check `~/.cache/huggingface/hub` for model weights the skill may have pulled.

## Hard rules

- **One agent, one job.** If the role sentence needs an "and", split it.
- **Never hand-edit `config.yaml`** — `hermes -p <name> config set KEY VALUE`.
- **SOUL.md is hand-edited** — it is a plain file, that is the correct way.
- **Never move or read credentials.** Point the user at `.env` and stop.
- **Secrets in `.env`, settings in `config.yaml`.** Never reversed.
- **Measure with `prompt-size`** before declaring an agent lean.
- **Clone carries `.env`.** A narrow agent should not inherit every key.
- **Delete throwaway profiles** when done — `hermes profile delete <name> --yes`, then remove the orphaned `~/.local/bin/<name>.bat` wrapper by hand.
- **`--no-skills` is the real anti-bloat lever at creation time.** Measured: a default `profile create` syncs 58 bundled skills and costs 54.6 KB/turn; `--no-skills` plus a two-toolset list costs 18.6 KB/turn. Same agent, 66% less rent.
- **Restart to see changes.** SOUL.md, memory, and config are read at session start and frozen for the session. On a gateway agent (Telegram etc.) a service restart is NOT enough: the chat session keeps its frozen system prompt. Restart the service, then send `/new` in the chat, then test.

## Giving a new profile its own messaging gateway (Windows, standalone gateways)

Telegram is the example below; on another platform the `.env` key and the log line differ.
When the host runs per-profile gateways (not multiplexed), `hermes -p <name> gateway install`
refuses with "does not get a gateway of its own". Use `--force --start-now --start-on-login`.
Prefer this over `gateway migrate --multiplex` when another profile's gateway is live and
healthy: migrating touches every running bot for one new agent. Without admin rights the
installer falls back to a Startup-folder `.vbs` login item instead of a Scheduled Task — that
is expected. Verify with `grep 'telegram connected' profiles/<name>/logs/gateway.log`.
Check the `.env` shape without reading values:
`grep -cE '^TELEGRAM_BOT_TOKEN=[0-9]+:[A-Za-z0-9_-]+\s*$' .env` -> 1.

## Gotchas when verifying

- `--no-skills` can **still** seed bundled skills from a shared
  `$HERMES_HOME/skills` tree. Check `profiles/<name>/skills/` and delete by
  hand if the profile is meant to start empty.
- A toolset showing **0 B** in `prompt-size` is not necessarily missing.
  Deferred tools (e.g. `cronjob`) are reachable on demand via `tool_search` and
  cost nothing until called — confirm before "fixing" it.

## Path note

Profiles live at `$HERMES_HOME/profiles/<name>/`. Resolve from `$HERMES_HOME`; never hardcode `~/.hermes`, which is only correct for the default profile.

On Windows the Hermes home usually sits under `%LOCALAPPDATA%`; resolve it the same way, do not type it.
