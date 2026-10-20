# Getting Started with Persistent Agents

A practical guide for PMs setting up their own agent team in Claude Code.

**The single most important thing:** Build one really good agent before you build a second one. A great agent you use every day is worth more than six mediocre ones you ignore. This guide walks you through building that first agent properly, understanding how it works, and then expanding when you're ready.

**Why this compounds:** Every correction you make teaches the agent something permanent. Every week of use adds institutional knowledge — data gotchas, stakeholder preferences, seasonal patterns, meeting rhythms — that survives between sessions. After a month, your agent knows things that would take a new human team member weeks to discover. After a quarter, it's carrying context that even you've forgotten. The investment you put in during the first two weeks pays off every single day after that, and the gap between a week-old agent and a 3-month-old agent is enormous.

---

## What are persistent agents?

Persistent agents are team members. Each one has a clear **outcome** it's accountable for, a **job description** that defines how it works, **tools** it uses to get things done, and **memory** — both short-term (what's happening right now) and long-term (what it's learned over time). They can post to your messaging tool so you see their work without opening the terminal, and you can message them back to ask questions or give instructions — it's a two-way channel. They also behave like a team: each agent knows the others' priorities by reading their state files.

The difference from a normal Claude conversation is persistence. A regular conversation starts fresh each time. A persistent agent remembers what matters, builds institutional knowledge over weeks, and gets better the longer it runs.

Each agent is defined by five things:

- **Outcome** — the single thing this agent exists to deliver (e.g. "nothing falls through the cracks", "decisions grounded in accurate data"). This is the most important part. Everything else serves the outcome
- **Job description** — specific responsibilities, proactive behaviours, and how it communicates
- **Tools** — slash commands, MCP integrations (messaging, calendar, meeting notes, data warehouse), and file access
- **Short-term memory (state)** — a compact (80-line max) working document tracking what matters right now, refreshed daily or weekly
- **Long-term memory** — permanent institutional knowledge that survives state pruning and compounds over time

### The 3-layer system

Every persistent agent has three files:

```
┌─────────────────────────────────────────────┐
│  Agent definition (.claude/agents/cos.md)    │  ← The outcome + job description
│  Written once, refined over time             │     (what this team member delivers)
├─────────────────────────────────────────────┤
│  State file (team/YOU/agents/state/cos.md)       │  ← Short-term memory
│  Refreshed daily/weekly, max 80 lines        │     (what's happening right now)
├─────────────────────────────────────────────┤
│  Memory file (team/YOU/agents/memory/cos.md)     │  ← Long-term memory
│  Grows over time, max 150 lines              │     (institutional knowledge)
└─────────────────────────────────────────────┘
```

**The outcome comes first.** When you read a good agent definition, the very first thing you see is the outcome — what this team member is accountable for delivering. Every responsibility, every proactive behaviour, every tool choice flows from that outcome. If you can't articulate the outcome in one sentence, the agent won't be focused enough to be useful.

**Agent definitions** live in `.claude/agents/` and are shared in git (they're reusable).
**State and memory files** live in `team/{initials}/agents/` and are gitignored (they're personal).

The definition tells Claude *what to deliver and how*. The state file tells it *what's happening right now*. The memory file tells it *what it's learned permanently*. Without state and memory, it's just a prompt. With them, it's a team member that gets better over time.

---

## Pick your first agent

Choose the one that solves your biggest daily pain point. Don't overthink it — you can always switch.

| If your biggest pain point is... | Start with | Why |
|----------------------------------|-----------|-----|
| Forgetting actions, being unprepared for meetings, things slipping | **Chief of Staff (COS)** | You'll feel the difference on day one. It reads your todo list, calendar, and meeting notes — then tells you what to focus on |
| Not having data to hand, missing funnel changes, slow experiment reads | **Analyst** | It watches the numbers so you don't have to refresh dashboards manually |
| Missing user signals, not connecting research across sources | **UX Researcher (UXR)** | It reads reviews, support calls, research studies, and competitor moves — then connects the dots |
| Losing track of direct reports' development, unprepared 1:1s | **Manager** | It preps your 1:1s and tracks each report's growth across impact, process, and culture |
| Wanting structured self-reflection and growth tracking | **Coach** | Weekly operating reviews with pattern detection — spots what you can't see from inside |
| Struggling to frame work for execs, inconsistent strategic narrative | **Strategist** | Tracks what each exec cares about and helps you frame the same work differently for each |

**For most PMs, COS is the best first agent.** It has the most frequent feedback loop (daily), so you'll learn how agents work faster.

---

## Build your first agent

Run this in Claude Code:

```
/setup-agent SJ, Steve, cos
```

Replace with your initials, first name, and chosen agent type (`cos`, `analyst`, `uxr`, `coach`, `manager`, `strategist`, `engineer`). Or just run `/setup-agent` with no arguments and it will ask you for each one.

The command checks your MCP connections (and helps you set them up if the important ones are missing), creates your workspace, personalises the agent definition, and bootstraps context from your calendar, meeting transcripts, messaging, and local files. It takes about 5 minutes. When it's done, it tells you exactly what to review, how to test the agent, and how to correct what it gets wrong.

**That's it for setup.** When you're ready for a second agent, run `/setup-agent` again with a different agent type — it detects your existing workspace and just adds the new agent.

The rest of this guide explains how the system works and how to get the most out of it over time.

### Use it daily and let it compound

This is where most people go wrong. They build the agent, test it a few times, think "that's neat", and move on to building more agents. Don't.

**Use your first agent every single working day.** Here's what compounds over time:

| Timeframe | What changes |
|-----------|-------------|
| **Day 1** | Output is useful but generic in places. Agent knows your meetings and priorities but misses nuance |
| **Week 1** | Agent has absorbed your corrections. It knows your stakeholders, your preferred framing, the topics that matter to you. Output starts feeling personalised |
| **Week 2** | Memory is building. Agent starts connecting information across sessions — "this is the second week the experiment tracker hasn't been updated" or "you mentioned this concern in your 1:1 with Sarah last week" |
| **Month 1** | Agent has real institutional knowledge. It knows data gotchas, seasonal patterns, which metrics are unreliable, who to chase about what. It catches things you'd miss |
| **Month 3+** | Agent carries context that even you've forgotten. New team members could learn more from reading its memory file than from a week of onboarding |

**Each session, the agent gets a little better** because its memory grows and your corrections compound. Keep refining the definition too — spend 2 minutes after each session:
- If a responsibility produced noise today, remove it
- If you wished it had told you something, add that as a responsibility
- If it surfaced something genuinely useful, note what made it work and lean into that

The agent evolves in two ways: its memory compounds automatically, and its definition improves through your edits. Both matter. Memory without a good definition produces unfocused output. A good definition without memory produces generic output. Together, they compound.

**Use these checkpoints to gauge progress:**

- **After 1 week:** Output should reference your real people, meetings, and priorities. If it's still generic, your context files need more detail or your MCPs aren't connected.
- **After 2 weeks:** The agent should be surfacing things you'd have missed — an overdue action, a connection between two meetings, a metric trend. If it's not, check the proactive behaviours in your definition.
- **After 1 month:** You should feel like you'd genuinely miss this agent if it stopped running. If you wouldn't, the agent isn't solving a real pain point — reconsider which agent you started with.

### Connect your agent to a messaging tool

Once the agent is producing output worth reading daily, connect it to your messaging tool (e.g. Slack, Teams). There are two levels — start with posting, add two-way conversation when you're ready.

#### Level 1: Agent posts to messaging (one-way)

This lets automated scripts post agent outputs (daily briefs, weekly digests, alerts) to a channel you control.

**1. Create a messaging app and bot:**

In your messaging tool, create a new app/integration and give it a name like `{Name} Agent Bot`.

**2. Add bot permissions:**

Grant scopes that let the bot:
- Read channel messages
- Read channel metadata
- Read private channel messages (if you'll use private channels)
- Post messages

Install the app to the workspace. Copy the **Bot Token** — you'll need this.

**3. Create your agent channel:**

Create a private channel: `#{initials}-{agent}` (e.g. `#sj-cos`). Add your bot to the channel and copy the **Channel ID**.

**4. Configure the bot token:**

Create your env file at `scripts/slack-agent-bot/.env`:

```bash
# Your bot token from step 2
SLACK_BOT_TOKEN=xoxb-your-token-here

# Your user ID — so the bot doesn't respond to your manual messages in the channel
SKIP_USER_IDS=U12345ABC
```

(The example uses Slack environment variable names — adjust if you're using a different messaging tool.)

**5. Update your agent definition:**

In the messaging section of your agent definition, replace the placeholders:

```markdown
## Messaging channel

`#sj-cos` — your Chief of Staff channel (ID: `C0ABC123DEF`).
```

Now automated scripts can post to your channel using the bot token. The messaging MCP handles posting when the agent is invoked interactively.

#### Level 2: Two-way conversation via polling bot (interactive)

This is what makes messaging agents feel like real team members — you message the agent in its channel, and it responds in-thread. The polling bot watches your channels, routes messages to the correct agent via Claude CLI, and posts the response back.

A reference implementation lives at `scripts/slack-agent-bot/` (if included in this template). The general shape:

**1. Map your channel to your agent:**

Create an `agents.json` mapping channel IDs to agent definitions:

```json
{
    "C0ABC123DEF": {
        "name": "Chief of Staff",
        "agent_file": "{initials}-cos.md",
        "tools": "Read,Glob,Grep",
        "model": "sonnet"
    }
}
```

The fields:
- `name` — display name (for logging)
- `agent_file` — filename in `.claude/agents/` (your personalised definition)
- `tools` — which Claude Code tools the agent can use. `Read,Glob,Grep` is the safe default (read-only). Add `Bash` only if you want the agent to run commands
- `model` — Claude model to use. `sonnet` is fast and cheap for messaging responses; `opus` for deeper analysis

**2. Install dependencies and run:**

Install the messaging SDK and supporting libraries for your stack, then run the bot from the repo root. The bot will log which channels it's watching and confirm authentication.

**3. Deploy as a persistent daemon:**

Once it's working, set it up to run automatically via launchd (macOS), systemd (Linux), or your preferred process manager so it survives restarts.

**How it works under the hood:**
- The bot polls each configured channel every 60 seconds for new messages
- When it finds one, it loads the agent definition, builds a prompt with thread context, and runs `claude --print` as a subprocess
- The response is posted back in-thread (never to the channel feed)
- Thread conversations are tracked for 24 hours — the bot includes full thread history so multi-turn conversations work naturally
- Messages from your own user ID are ignored, so you can post in the channel without triggering the bot
- Long responses are split into multiple messages

**Adding more agents later:** Add entries to `agents.json` — one channel ID per agent. Create the channel, invite the bot, add the mapping, then restart the bot to pick up the new config.

### Automate (when you trust it)

Automation is the final step, not the first. Only automate when:
- You've been running it manually for 2+ weeks
- You trust its output enough to act on it without checking
- You know what it should say on a typical day

Start with one automation. The script depends on which agent you're automating:

| Agent | Suggested script | Frequency |
|-------|------------------|-----------|
| COS | `{initials}-daily-meeting-prep.sh` | Daily (morning) |
| Analyst | `{initials}-weekly-analyst-refresh.sh` | Weekly (Monday) |
| UXR | `{initials}-weekly-uxr-refresh.sh` | Weekly (Monday) |
| Coach | `{initials}-friday-weekly-review.sh` | Weekly (Friday) |
| Manager | `{initials}-weekly-manager-refresh.sh` | Weekly (Monday) |
| Strategist | `{initials}-weekly-exec-email.sh` | Weekly (Friday) |
| Engineer | `{initials}-weekly-repo-sweep.sh` | Weekly (Friday) |

**Naming convention:** always prefix personal scripts with your initials (`sj-`, `jk-`, `as-`, etc.). Scripts following the `{initials}-*.sh` pattern are gitignored automatically — they stay on your machine and never land in the shared repo.

```bash
# Test it manually first
bash scripts/sj-daily-meeting-prep.sh   # replace sj- with your initials

# If it works, deploy via your platform's scheduler
bash scripts/deploy.sh
```

See `scripts/README.md` for the full automation setup, deployment process, and `.env` configuration.

### Set up monitoring and alerting

Automations will break. Scripts fail, MCPs go down, state files go stale. Without monitoring, you won't notice until the agent's output degrades — or stops entirely. Two things protect you:

#### The alert wrapper

Every automation script should run through `run-with-alert.sh` (provided in `scripts/`), which wraps the script with failure detection and notifications. In your scheduler config, instead of calling the script directly, call it via the wrapper:

```bash
# Instead of:
bash scripts/daily-meeting-prep.sh

# Use:
bash scripts/run-with-alert.sh scripts/daily-meeting-prep.sh
```

What the wrapper does:
- Logs every run to `scripts/logs/run-history.log` (format: `date|script|OK/FAIL|exit_code`)
- Posts to your alert channel on failure
- Tracks consecutive failure streaks — escalates at 3+ and 5+ failures
- Optionally sends Telegram alerts for critical failures (configure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`)

#### The Engineer agent

The Engineer agent (`starters/starter-engineer.md`) is specifically designed to monitor your automation system. Set it up once you have 3+ automations running — it runs weekly and checks:

- **Script failures** — which scripts failed since last sweep, how often, and why
- **Silent failures** — scripts that exit 0 but produce no output (the dangerous ones)
- **Stale state files** — any agent state past its `Next due` date, meaning its automation is broken
- **Consecutive failures** — same script failing 3+ times in a row gets escalated
- **Cost trends** — whether your automation costs are increasing

Create an alerting channel (`#{initials}-engineer`) and point it there. This is the channel you check when something feels off — it's your system health dashboard.

#### What a healthy setup looks like

```
scripts/logs/
├── run-history.log          ← all runs, one line per execution
├── daily-meeting-prep.log   ← stdout for each script
├── daily-meeting-prep-error.log  ← stderr
├── .streak-daily-meeting-prep    ← consecutive failure count (0 = healthy)
└── ...
```

Check health any time: `grep FAIL scripts/logs/run-history.log | tail -10`

Or just ask the Engineer agent: `claude -a engineer "What's broken?"`

---

## What Claude needs to know (and what it doesn't)

When you write an agent definition, you're writing instructions for Claude. Here's what it can and can't do in this workspace.

### What's available to Claude

This workspace can integrate with several tools via MCP. Your agent can use any of these once you've configured them in `.mcp.json`:

| Capability | How |
|-----------|-----|
| Read any file in the repo | `Read`, `Glob`, `Grep` tools |
| Read your personal files | `team/{INITIALS}/` (gitignored) |
| Run slash commands | `/daily-prep`, `/investigate`, etc. (full list in `CLAUDE.md`) |
| Query your data warehouse | BigQuery / Snowflake / similar MCP |
| Read your calendar | Calendar MCP (e.g. Google Calendar) |
| Read meeting transcripts | Meeting notes MCP (e.g. Granola, Otter) |
| Post to and read messaging | Messaging MCP (e.g. Slack) |
| Read wiki pages | Wiki MCP (e.g. Notion, Confluence) |
| Send email | Email MCP |
| Search analytics dashboards | Analytics MCP (e.g. Hex, Mode) |
| Explore data models | Data modelling MCP (e.g. dbt) |
| Read/write state files | `Write` tool to `team/{INITIALS}/agents/state/` |
| Read/write memory files | `Write` tool to `team/{INITIALS}/agents/memory/` |

### What's NOT available

- **Other people's team directories** — `team/` is gitignored per person, your agent can't read other team members' state files
- **Automations you haven't deployed** — the scripts exist in `scripts/` but don't run until you schedule them
- **Channels that don't exist** — create the channel before telling the agent to post there
- **Write access to shared files** — agents can read `insights/`, `data/`, `context/`, but should only write to `team/{INITIALS}/`

### Tell your agent what it has

In your agent definition, list the tools it should use for its responsibilities. Be specific about *what* each tool is for — this helps Claude choose the right tool at the right time.

**Good:**
```markdown
## Tools you use
- `/daily-prep` — generates the full daily brief
- Calendar (via MCP) — for reading today's events, finding free slots, checking attendees
- Meeting notes (via MCP) — for retrieving meeting notes and transcripts to extract actions
- Messaging (via MCP) — for scanning recent conversations with attendees before 1:1s
```

**Too vague:**
```markdown
## Tools you use
- Slash commands
- All MCP integrations
```

---

## Understanding what makes an agent great

After two weeks of daily use, you'll start to see what separates a good agent from a great one. The mature agents in this repo (`.claude/agents/cos.md`, `uxr.md`, `analyst.md`, etc.) are the best examples — read them and notice what they do differently from a basic prompt.

### Good agent: follows instructions
- Reads the right files
- Produces structured output
- Updates state correctly

### Great agent: saves you time and catches things you miss
- Surfaces the thing you forgot about
- Connects information from different sources you wouldn't have combined
- Notices patterns over time ("this is the 3rd week you've had no focus time")
- Knows your context well enough to prioritise what matters to you specifically
- Gets better each week because memory accumulates

### What makes the difference (with real examples)

1. **Rich context files** — the agent can only work with what it can read. Compare: a well-loved COS reads 30+ meeting context files, a live todo list, and current priorities. That's why its briefs are specific, not generic. Your agent will mirror the quality of its sources

2. **Specific responsibilities** — "monitor the funnel" is too vague. Look at how the analyst agent does it: "Flag when any funnel step moves ±2 standard deviations from its 4-week average." That's actionable. Compare the responsibilities in the mature agents to your starter — you'll see the difference in specificity

3. **Proactive behaviours** — the best agents don't just answer questions, they spot things unprompted. Look at COS's proactive behaviours: information cascade (flagging when a decision in one meeting affects someone in a different meeting), meeting effectiveness tracking (flagging meetings that produce nothing for 4+ weeks), stakeholder contact gaps. These are the things that make you say "I didn't even think of that"

4. **Memory that compounds** — each week the agent learns something permanent. See `example-memory.md` for what this looks like after a few months: data gotchas, seasonal patterns, stakeholder preferences, dead ends. After 3 months, your agents know things that would take a new person weeks to discover

5. **Pruning discipline** — state files that grow unchecked become useless. The 80-line budget and pruning rules keep the signal high. This feels aggressive at first, but it forces the agent to keep only what matters right now — permanent learnings go to memory, everything else gets removed

---

## When you're ready: expand to a second agent

Once your first agent is running well (you use it daily, you've refined it through multiple iterations, and it's genuinely saving you time), you're ready to add a second one.

**Don't start from scratch.** Just run `/setup-agent` again with a different agent type. It detects your existing workspace and only adds the new agent's files (definition, state, memory) — your existing todo list, meeting context, and shared memory carry over.

Then bootstrap, test, iterate for 2 weeks before automating.

### The full agent roster

| Agent | Short name | Outcome | Best for |
|-------|-----------|---------|----------|
| Chief of Staff | `cos` | Nothing falls through the cracks | Everyone — operational backbone |
| Analyst | `analyst` | Decisions grounded in accurate data | PMs who need data regularly |
| UX Researcher | `uxr` | User signals spotted early | PMs who own user-facing features |
| Coach | `coach` | Continuous self-improvement | Anyone who wants structured reflection |
| Manager | `manager` | Reports levelling up | People managers with 3+ reports |
| Strategist | `strategist` | Leadership backing | PMs presenting to execs regularly |
| Engineer | `engineer` | Workspace runs reliably | When you have 5+ automations |

### Using Engineer and Coach to improve your setup

Two agents are specifically designed to help you improve the system itself:

**Engineer** audits your setup and finds problems:
```
claude -a engineer "Review my agent setup. Check state file freshness, automation health, and repo structure. What needs fixing?"
```

**Coach** spots patterns in how you work:
```
claude -a coach "Review my week. Am I spending time on the right things? What patterns do you see across the last 4 weeks?"
```

Use Engineer monthly to check your system is healthy. Use Coach weekly to check you're effective.

---

## Starter agent definitions

The **mature agents** (`.claude/agents/cos.md`, `uxr.md`, `analyst.md`, etc.) are the best reference for what a fully evolved agent looks like. Read them first.

The **starters** below are for copying and personalising. They have the full set of responsibilities — that's what teaches you what the agent *can* do. What's different from the mature versions is the infrastructure: starters don't assume cross-agent wiring, complex automations, or specific MCPs. Instead, they use HTML comments (`<!-- -->`) to show you what to unlock next and why.

| File | Agent | What it can do from day one |
|------|-------|-----------------------------|
| `starters/starter-cos.md` | COS | Daily briefing, meeting prep, action tracking, follow-up chasing, priority alignment, information cascade |
| `starters/starter-analyst.md` | Analyst | Funnel monitoring, anomaly detection, experiment tracking, evidence verification, data gotchas |
| `starters/starter-uxr.md` | UXR | Signal synthesis across all sources, theme tracking, persona grounding, hypothesis validation, competitor monitoring |
| `starters/starter-coach.md` | Coach | Weekly review, development tracking across 5 skill areas, goal progress, pattern spotting, review compliance |
| `starters/starter-manager.md` | Manager | 1:1 prep, three-pillar PM tracking, goal tracking, feedback gap detection, team health |
| `starters/starter-strategist.md` | Strategist | Exec comms, audience framing, feedback tracking, narrative consistency, evidence validation, goal quality |
| `starters/starter-engineer.md` | Engineer | Automation health, state file freshness, script failures, cost trends, repo quality, technical opportunities |

**How the starters teach you:** Each starter contains `<!-- AS YOUR AGENT MATURES -->` and `<!-- PROACTIVE BEHAVIOURS YOU CAN ADD LATER -->` comments throughout. These are invisible to Claude but visible to you when editing the file. They explain what each upgrade does and when to add it. This way you grow the agent deliberately rather than starting with everything and not understanding what's working.

---

## Example files

| File | What it shows |
|------|--------------|
| `example-state.md` | A filled-in UXR state file with illustrative data |
| `example-memory.md` | A filled-in memory file across all categories |
| `persistent-agent-template.md` | Blank template with all standard sections — for building from scratch |

---

## What's in this repo

| What | Where | Notes |
|------|-------|-------|
| Agent definitions | `.claude/agents/` | Shared perspective agents + examples |
| Slash commands | `.claude/commands/` | Shared commands (full list in `CLAUDE.md`) |
| PM playbook | `pm-playbook/` | Process docs, templates, training |
| Insights | `insights/` | Research, reviews, competitor intel |
| Data context | `data/funnel-context.md`, `data/queries/` | Metric definitions, saved queries |
| Automation scripts | `scripts/` | Deployment tools, scheduler configs |
| Context files | `context/` | Priorities, product, personas |
| Your personal files | `team/{INITIALS}/` | Created by `/setup-agent`, gitignored |
| Your messaging channels | `#{initials}-cos`, etc. | Created when connecting to messaging |
| Your `.env` and scheduler jobs | See Messaging + Automate sections | Created when automating |

---

## Troubleshooting

**"My agent gives generic, unhelpful output"**
→ This is almost always a context problem, not an agent problem. Check: does your todo list have real items? Do your meeting context files have actual notes? Are your priorities up to date? The agent mirrors the quality of its sources.

**"My agent doesn't know about recent meetings"**
→ Check that your meeting notes MCP is configured. Without it, use `/export-transcripts` to pull transcripts manually, or add notes to your meeting context files after each 1:1.

**"State file is getting too long"**
→ Ask the agent: `"Prune your state file. Remove resolved items, enforce the 80-line budget, and write any permanent learnings to memory before removing."` The pruning rules exist for a reason — trust them.

**"Automation isn't running"**
→ Check your scheduler (e.g. `launchctl list` on macOS) to see if jobs are loaded. Check `scripts/logs/` for error logs. Run `bash scripts/deploy.sh` to redeploy.

**"Too much noise in messaging"**
→ Remove proactive behaviours from the agent definition until only the ones you act on remain. You can always add them back.

**"I want to change something but I'm not sure if I should"**
→ Change it. Agent definitions are meant to be iterated on. If it doesn't work, change it back. The worst thing you can do is leave a bad agent running unchanged.

---

## Quick reference

| Thing | Where it lives |
|-------|---------------|
| Agent definitions | `.claude/agents/{name}.md` |
| State files | `team/{INITIALS}/agents/state/{name}.md` |
| Memory files | `team/{INITIALS}/agents/memory/{name}.md` |
| Starter agents | `.claude/agents/examples/starters/` |
| Example files | `.claude/agents/examples/` |
| Template | `.claude/agents/examples/persistent-agent-template.md` |
| Automation scripts | `scripts/` |
| Automation logs | `scripts/logs/` |
| Run history | `scripts/logs/run-history.log` |
| Messaging bot config | `scripts/slack-agent-bot/agents.json` (reference implementation) |
| Slash commands | `.claude/commands/` |
| PM playbook | `pm-playbook/` |

---

## Getting help

- **Ask the Engineer agent** — `claude -a engineer "Help me debug my setup"`
- **Read the PM playbook** — `pm-playbook/README.md`
- **Open an issue on the repo** — if something looks broken or unclear
