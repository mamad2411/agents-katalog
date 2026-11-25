---
name: hermes-multi-agent-telegram
description: Generic how-to for spinning up multi-agent Telegram setups using Hermes profiles. NOT applicable to Charles. Charles's sub-agents (Mark, Eric, Bob, Michael, Tammie) are SKILLS Hermes loads in-process — they have never had separate Telegram bots on the Hermes side. Do not propose @BotFather workflows for Charles.
version: 1.0.0
author: Hermes Agent
tags: [telegram, multi-agent, profiles, bots, team, group-chat]
---

# Hermes Multi-Agent Telegram Team Setup

> ## ⛔ STOP — Reality Check for Charles's Setup
>
> **Charles's sub-agents on the Hermes side are SKILLS, not separate Telegram bots.** When he says "tell Bob to skip-trace this" or "have Mark make a thumbnail", load the matching skill (`bob`, `yt-thumbnail-creator`, etc.) and do the work in-process. **They have never had their own Telegram bots on the Hermes side, and they don't need any.**
>
> If you are reading this skill thinking "Phase 1 says Charles needs to create bots via @BotFather" — **you are wrong**. The skill below is generic documentation for hypothetical future setups, not a TODO for Charles. Suggesting BotFather to Charles is a hallucination — see SOUL.md "Sub-Agents Are Skills, Not Bots".
>
> (Separately: Charles also has an **OpenCLAW** system on the same VPS where Mark/Eric/Bob/Michael/Tammie exist as full standalone agents with their own Telegram bots. He uses OpenCLAW directly when he wants. James does not relay to OpenCLAW.)

The rest of this skill is generic guidance for setups that aren't Charles's. It is not a TODO list.

---

Use when a user wants multiple AI agents as separate Telegram bots, each with its own personality, memory, and skills — all capable of working together in a shared Telegram group.

## What This Skill Does

This skill Generic how-to for spinning up multi-agent Telegram setups using Hermes profiles. NOT applicable to Charles. Charles's sub-agents (Mark, Eric, Bob, Michael, Tammie) are SKILLS Hermes loads in-process — they have never had separate Telegram bots on the Hermes side. Do not propose @BotFather workflows for Charles.

## How It Works

Hermes supports **profiles** — fully independent HERMES_HOME directories. Each profile has:
- Its own `config.yaml` (including a unique Telegram bot token)
- Its own `SOUL.md` (personality)
- Its own memory, sessions, skills, and cron jobs
- Its own gateway process

One profile = one Telegram bot = one agent.

## Key Paths

- Profiles live at: `~/.hermes/profiles/<name>/`
- Profile commands: `hermes profile create|list|delete|use`
- Run a profile's gateway: `hermes -p <name> gateway run`
- Or set sticky default: `hermes profile use <name>`

## Phase 1 — Create Telegram Bots (User does this)

For each agent, the user must create a new bot via @BotFather on Telegram:

1. Open Telegram, message @BotFather
2. Send `/newbot`
3. Give it a display name (e.g. "Bob - Property Intel")
4. Give it a username (e.g. `@CharlesREIBobBot`) — must end in `bot`
5. Copy the token BotFather gives you
6. Repeat for each agent

Agents in Charles's case: Bob, Mark, Eric, Michael, Tammie (+ main Hermes)

## Phase 2 — Create Profiles (Agent does this)

For each agent, create a profile, set the SOUL.md, and configure the bot token:

```bash
# Create profile (clones config, .env, and SOUL.md from default)
hermes profile create bob --clone
# This also creates a wrapper alias: /root/.local/bin/bob
# So you can use `bob gateway start` instead of `hermes -p bob gateway start`
```

**Set the bot token** — edit the profile's .env directly (no `hermes config set` command for this):
```bash
# ~/.hermes/profiles/bob/.env
# Find the TELEGRAM_BOT_TOKEN= line and replace it, or append if missing
TELEGRAM_BOT_TOKEN=8687664413:AAGTfo43FFhvWr8fWvhdgCJh8jV8LNWcpCw
```

**Set the SOUL.md** — copy from OpenClaw or write fresh:
```bash
cp /root/.openclaw/workspace/agents/bob/SOUL.md ~/.hermes/profiles/bob/SOUL.md
```

**Set the personality** in `~/.hermes/profiles/bob/config.yaml`:
```yaml
# Find this line (it's there by default):
personalities: {}

# Replace with:
personalities:
  bob: 'You are Bob, Charles's property intelligence engine. ...'
```
Also set `personality: bob` in the `display:` section.

**Disable require_mention** so the bot responds in groups when @mentioned:
```yaml
# In config.yaml under discord: section
require_mention: false
```

Repeat for each agent (mark, eric, michael, tammie).

## Phase 3 — Start Each Bot's Gateway

**CRITICAL: You must run `install` before `start`.** Running `start` without `install` fails with "Unit not found".

```bash
# Step 1: Install the systemd service (only needed once per profile)
bob gateway install
mark gateway install
michael gateway install
tammie gateway install

# Step 2: Start the services
bob gateway start
mark gateway start
michael gateway start
tammie gateway start

# Check status
bob gateway status
```

The profile wrapper aliases (`bob`, `mark`, etc.) are created automatically at
`/root/.local/bin/<name>` when you run `hermes profile create <name> --clone`.
Use them instead of `hermes -p <name>` for brevity.

Services survive reboots automatically (systemd linger is enabled by default).

**Verify connection** by checking the gateway log:
```bash
tail -20 ~/.hermes/profiles/bob/logs/gateway.log
# Should show: "✓ telegram connected" and "Gateway running with 1 platform(s)"
```

## Phase 4 — Telegram Group Setup (User does this)

1. Create a new Telegram group
2. Add yourself + all 5 bots to the group
3. Each bot must be given admin rights or at minimum messaging permission
4. In each bot's BotFather settings, enable group privacy OFF (so bots can read all messages, not just @mentions):
   - Message @BotFather → `/mybots` → select bot → Bot Settings → Group Privacy → Turn Off

## Phase 5 — Configure Group Response Behavior

By default, bots in groups only respond when mentioned. To configure:

In `~/.hermes/profiles/<name>/config.yaml`:
```yaml
# Require @mention before responding (recommended for group chats)
# Leave this at default — Hermes respects @mentions automatically
```

In the group, users address agents like:
- `@CharlesREIBobBot pull everything on 123 Main St Baltimore`
- `@CharlesREIMarkBot create a thumbnail for my new video`

## Agent SOUL.md Sources (Charles's Team)

Pre-existing SOUL.md files from OpenClaw migration are at:

| Agent | SOUL.md Path |
|-------|-------------|
| Bob | `/root/.openclaw/workspace/agents/bob/SOUL.md` |
| Mark | `/root/.openclaw/workspace/agents/mark/SOUL.md` |
| Eric | `/root/.openclaw/workspace/agents/eric/SOUL.md` |
| Michael | `/root/.openclaw/workspace/agents/michael/SOUL.md` |
| Tammie | `/root/.openclaw/agents/tammie/SOUL.md` (or reconstruct from config) |

## Migrating an Agent from OpenClaw → Hermes Profile

When an agent has an existing OpenClaw workspace, pull these files into the Hermes SOUL.md:

1. `hermes profile create <name> --clone` — creates profile + wrapper alias
2. Copy `SOUL.md` from `/root/.openclaw/workspace/agents/<name>/SOUL.md`
3. Pull key content from `IDENTITY.md`, `TOOLS.md`, `AGENTS.md` into SOUL.md:
   - All API keys and credentials (Blotato, Zapier MCP, Fish Audio, etc.)
   - Platform account IDs
   - Default workflow settings
   - File paths for scripts and outputs
   - Charles's social handles and preferences
4. Copy any important scripts to `~/.hermes/profiles/<name>/workspace/`
5. Bot token still goes in `.env` — `TELEGRAM_BOT_TOKEN=<token>`

The goal: agent should be fully self-contained from SOUL.md alone — no need to re-read OpenClaw files on every session.

## Agent Reply Protocol

When Charles addresses a specific agent by name in conversation, invoke them in their own voice and prefix every reply:
- `Mark: [reply]`
- `Bob: [reply]`
- `Eric: [reply]`
- `Michael: [reply]`
- `Tammie: [reply]`
- `James: [reply]` (main agent)

Each agent speaks with their own personality from their SOUL.md — not filtered through James.

## Phase 6 — Disable Tool Progress Noise on Telegram

After starting all gateways, set `tool_progress: none` so raw execution code doesn't stream to Telegram. Default is `all` which spams every tool call live.

```bash
# Fix main profile
sed -i 's/tool_progress: all/tool_progress: none/g' ~/.hermes/config.yaml

# Fix all agent profiles
for profile in bob mark michael tammie eric; do
  sed -i 's/tool_progress: all/tool_progress: none/g' ~/.hermes/profiles/$profile/config.yaml
done

# Restart all gateways to pick up the change
for profile in bob mark michael tammie eric; do
  $profile gateway restart
done
```

## Pitfalls

- **Install before start** — `bob gateway install` must run before `bob gateway start`, or you get "Unit hermes-gateway-bob.service not found"
- **Each bot needs a unique token** — never reuse the same token across profiles
- **Token goes in .env, not config.yaml** — edit `~/.hermes/profiles/<name>/.env`, set `TELEGRAM_BOT_TOKEN=<token>`. There is no `hermes config set` shortcut for this.
- **BotFather rate limits** — you can only create ~2 bots before hitting a cooldown (can be up to 22 hours). Plan ahead and spread creation across sessions if building a large team.
- **Profile wrapper aliases** — created at `/root/.local/bin/<name>` automatically. Use `bob gateway start` not `hermes -p bob gateway start`.
- **personalities: {} placeholder** — in config.yaml, this is the line to find/replace when adding a custom persona prompt. Also update `display.personality: <name>` to match.
- **require_mention: false** — set this in config.yaml to allow bots to respond to @mentions in groups without needing full group admin
- **Session isolation** — each profile has its own sessions DB; agents don't share memory unless you set shared skill dirs in config
- **Logs** — gateway logs are at `~/.hermes/profiles/<name>/logs/gateway.log`, not in journalctl

## Verification

After setup, test each bot:
1. DM each bot directly — it should respond
2. Add to group — mention it by @username — it should respond
3. Ask it something role-specific (Bob: property address, Mark: thumbnail request)

## Notes on Team Coordination

In the current Hermes architecture, agents don't natively "talk to each other" in real-time. Coordination happens through:
- Charles directing each bot by @mention in the group
- Agents sharing files via a common workspace directory
- Main Hermes orchestrating tasks and delegating to subagents via `delegate_task`
