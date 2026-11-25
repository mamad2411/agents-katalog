---
name: initial-setup
description: "Welcome and onboard new EvoNexus users — introduce agents, skills, routines, and the dashboard. Triggers when the user says 'get started', 'how do I use this', 'what can you do', 'help me get started', 'onboarding', 'show me around', 'what agents do I have', 'how does this work', 'first time here', or seems unfamiliar with the workspace. Also trigger when the user opens Claude Code in an EvoNexus workspace for the first time."
---

# EvoNexus — Welcome & Onboarding

The user already has EvoNexus installed and running. Your job is to welcome them, show what's available, and help them start using agents, skills, and routines right away.

## Step 0: Bootstrap Workspace Structure (dynamic)

Before welcoming, ensure the `workspace/` folder tree exists. The workspace is gitignored (personal data) so new installations start empty — you need to discover which agents are installed and create folders based on **what each agent declares in its own system prompt**, not a hardcoded list. This keeps the skill self-updating: when new agents are added (business, engineering, or custom), their folders are created automatically the next time this runs.

### Discovery phase

1. **Read `config/workspace.yaml`** to get `workspace.owner`, `workspace.company`, `workspace.language`, `workspace.timezone`, `workspace.name`. These values drive language and personalization.

2. **List all installed agents** with `Glob .claude/agents/*.md`. This captures:
   - Business layer agents (`clawdia-assistant.md`, `flux-finance.md`, etc.)
   - Engineering layer agents (`apex-architect.md`, `bolt-executor.md`, etc.) as they get imported
   - Custom agents (`custom-*.md`) the user created

3. **For each agent file**, Read it and extract:
   - **Name** from the frontmatter (`name: ...`)
   - **Color** from the frontmatter (`color: ...`) — used for future dashboard integration
   - **Domain / role** from the `description:` frontmatter field or the first prose paragraph
   - **Working folder** — look for the `## Working Folder` section and parse the first sentence for `workspace/{folder}/`. If the agent has no `## Working Folder` section (e.g., pure orchestrators like Clawdia, knowledge agents like Oracle), record it as "no dedicated folder" and skip folder creation for that agent.
   - **Subfolders** — if the Working Folder description or the agent's prose mentions specific subfolders (e.g., `strategy/analyses/`, `project/github-reviews/`), extract them too.
   - **Anti-patterns / approval rules** — scan sections like `## Anti-patterns`, `## Absolute Rules`, `## Your Level`, `### REQUIRES user approval` to extract the 1-2 most important conventions.

4. **Build an in-memory table** of `{agent, folder, subfolders, domain, conventions}`. This is the source of truth for Step 1.

### Creation phase

5. **Check if the structure already exists.** Run a quick check: if **every** folder in the discovered table already exists on disk, structure is already bootstrapped — skip creation and proceed to the "Customizations" summary below. Otherwise, continue.

6. **Create folders.** For each entry in the table that declares a Working Folder:
   - Create `workspace/{folder}/` if missing
   - Create any declared subfolders
   - Create `.gitkeep` in the top-level folder (subfolders don't need it — the wildcard in `.gitignore` handles them)
   - **Never overwrite** existing folders or files

7. **Create the shared read-only folder** `workspace/projects/` (plural) if missing — this is where the user uploads git repositories that every agent can read. Also add a `.gitkeep`.

8. **Create operational folders** that are not owned by any single agent but are referenced by routines:
   - `workspace/daily-logs/` — written by clawdia and by the morning/eod routines
   - `workspace/meetings/` — managed by `int-sync-meetings` routine (Fathom)

   Only create these if they're referenced by at least one installed routine or agent; skip if the underlying agent/routine is not installed.

### Overview files phase

9. **Read `workspace.language`** from `config/workspace.yaml`. All overview files respect this value:
   - Filename and content are translated to `workspace.language` (e.g., `pt-BR` → `[C] Visão Geral — Financeiro.md`; `en` → `[C] Overview — Finance.md`; `es` → `[C] Visión General — Finanzas.md`)
   - If `workspace.language` is not set, default to `en`
   - This is the only place where the codebase writes localized filenames, because these files land in `workspace/` (gitignored, personal)

10. **For each folder** you created in Step 6, write an overview file using this canonical template (translate title, headings, and bullets to the target language before writing):

    ```markdown
    # Overview — {Sector}

    Working folder for agent **@{agent-name}** ({agent domain extracted from the agent file}).

    ## What goes here

    {Extract 3-6 bullets from the agent's Working Folder description and Responsibilities section}

    ## Conventions

    - Files created by the agent are prefixed with `[C]`
    - {1-2 agent-specific rules extracted from Anti-patterns / Absolute Rules / Your Level}
    ```

    **Never overwrite** an existing overview — if one already exists in any language, skip it (the user may have customized it).

### Customizations summary phase

11. **Scan agent improvement notes.** For each agent, check if `.claude/agent-memory/{agent-name}/_improvements.md` exists. If yes, read the first few lines and remember them for the summary.

12. **Scan agent memory folders** for customizations the user has saved (e.g., feedback memories, project memories). Count how many entries each agent has in its `MEMORY.md` index.

13. **Report customizations to the user.** After the welcome, include a "Your workspace customizations" section that surfaces:
    - Which agents have pending `_improvements.md` notes (and the first line of each)
    - Which agents have non-empty `MEMORY.md` indexes (count of entries) — this tells the user where they've already built up context
    - Any `custom-*` agents the user has created
    - Any new folders the user added to `workspace/` that don't match an installed agent

    This makes onboarding dynamic: instead of a generic tour, the user sees **their** workspace state and what's already been tailored.

### Important rules

- **Never overwrite** existing files or folders — the user may already have content
- **Discovery drives creation** — never hardcode folder names; always parse from the agent files. If a new agent is added, it will be picked up automatically.
- **`projects/` (plural)** is shared read-access for all agents; the user uploads git repos there
- **Engineering agents** (dev layer from oh-my-claudecode) typically don't declare a `## Working Folder` because they work across the codebase itself — skip folder creation for them
- **`personal/`** may contain a health dashboard setup (`docker-compose.yml`, `health-data.js`) — don't touch if it exists
- **`meetings/`** is managed by the sync-meetings routine — no overview file (has its own `README.md`)
- **Speed:** the discovery phase reads ~30 small markdown files; keep it fast by only reading the top ~40 lines of each agent unless you need deeper inspection

After bootstrap is done (or confirmed already existing), proceed to Welcome.

## Welcome

Start with a warm, **dynamic** welcome that uses the counts you discovered in Step 0. Do not hardcode agent or skill numbers — read them from the filesystem so the message stays accurate as the workspace grows.

Counts to compute at runtime:
- **Agents:** `Glob .claude/agents/*.md` and count entries (exclude `custom-*.md` or report them separately)
- **Skills:** `Glob .claude/skills/*/SKILL.md` and count entries
- **Routines:** count entries in `config/routines.yaml` (or `ROUTINES.md` if yaml doesn't exist)
- **Custom extensions:** count `.claude/agents/custom-*.md`, `.claude/skills/custom-*/SKILL.md`, `.claude/commands/custom-*.md`

Welcome text (template, translate to `workspace.language`):

> Welcome to **{workspace.name}** — your AI-powered operating system, {workspace.owner}. You have **{N} agents**, **{N} skills**, and **{N} automated routines** ready to go. Let me show you what you can do.

## Your Agents

Present the agents in a **dynamic table** built from Step 0's discovery table. Group them by layer:

1. **Business layer** — agents whose file name matches the canonical business names (clawdia, flux, atlas, pulse, pixel, sage, nex, mentor, kai, oracle, mako, aria, zara, lex, nova, dex) or whose description mentions a business domain
2. **Engineering layer** — agents whose file name starts with a known dev role (apex, bolt, compass, echo, flow, grid, hawk, lens, oath, prism, probe, quill, raven, scout, scroll, trail, vault, zen, canvas) — these come from oh-my-claudecode
3. **Custom layer** — any agent whose filename starts with `custom-`

For each layer, build a table dynamically by reading each agent file and extracting command, name, and one-line role:

| Command | Agent | Role | Try saying... |
|---------|-------|------|---------------|
| `/{command}` | **{Name}** | {role from description frontmatter} | {first example from description} |

**Do not hardcode the table.** Build it from the files on disk so new agents (including engineering imports and custom ones) appear automatically.

After the agents table, add:

> You don't have to use slash commands — just describe what you need and I'll route to the right agent automatically.

## Quick Wins to Try Right Now

Suggest 3 things the user can try immediately based on what's most useful:

### 1. Morning Briefing
"Say **'good morning'** and the Ops agent will check your calendar, emails, tasks, and give you a prioritized plan for the day."

### 2. Dashboard Overview
"Open **http://localhost:8080** to see the web dashboard — overview metrics, reports, services, and even a Claude Code terminal in the browser."

### 3. Run a Routine
"Try running a routine manually:
- `make morning` — morning briefing
- `make community` — community pulse report
- `make fin-pulse` — financial snapshot

Each routine generates an HTML report you can view in the dashboard under Reports."

## Skills by Domain

Compute skill categories **dynamically** from the filesystem:

1. `Glob .claude/skills/*/SKILL.md` → list of installed skills
2. Group by prefix (the part before the first `-`): `fin-`, `social-`, `dev-`, `int-`, `mkt-`, etc.
3. Count entries per prefix
4. For each prefix, pull 2-3 representative examples by reading the `name:` frontmatter of the first few skills in that group

Present as a table:

> You have **{total}** skills organized by prefix. Here are the categories installed in your workspace:

| Prefix | Count | Examples |
|--------|-------|----------|
| `{prefix}-` | {N} | {skill1, skill2, skill3} |
| ... | ... | ... |

**Do not hardcode the prefix list.** Different installations may have different layers enabled — the business layer (`fin-`, `social-`, `mkt-`, `hr-`, `legal-`, etc.), the engineering layer (`dev-`), and any custom prefixes the user introduced. Build the table from what's actually installed.

After the table:

> Browse all skills in the dashboard under **Skills**, or just ask me to do something and I'll use the right skill.

## Automated Routines

Read `config/routines.yaml` at runtime to list the actual routines installed in this workspace. Group them by frequency (daily / weekly / monthly) based on the cron schedule or `frequency:` field, and list the first handful per group.

Present as:

> EvoNexus can run routines automatically on a schedule. You have **{N} routines** installed:
>
> **Daily:** {list top 5-6 by name}
> **Weekly:** {list}
> **Monthly:** {list}
>
> Start the scheduler with `make scheduler` and routines run at their configured times. See the full list with `make help`.

If `config/routines.yaml` is missing or empty, say so and point the user to `create-routine` skill to set up their first one.

## The Web Dashboard

"Your dashboard at **http://localhost:8080** has:

- **Overview** — all metrics at a glance
- **Chat** — Claude Code terminal in the browser
- **Reports** — HTML reports from routines
- **Systems** — register and manage your apps
- **Services** — start/stop scheduler, see live logs
- **Routines** — metrics per routine + manual run button
- **Integrations** — connect YouTube, Instagram, LinkedIn via OAuth
- **Users & Roles** — manage access with custom permissions"

## Your Workspace Customizations

After the welcome tour, surface what's already been tailored in this specific workspace — this turns a generic onboarding into a personalized status check. Gather:

1. **Agent improvement notes** — for each agent folder in `.claude/agent-memory/`, check if `_improvements.md` exists. If yes, read the first line and list it. Example output:
   > - **@flux** has 2 pending improvement ideas: "Add cash flow forecast chart…"
   > - **@sage** has 1 pending improvement idea: "Link OKR review to Linear cycles…"

2. **Agent memory depth** — for each `.claude/agent-memory/{agent}/MEMORY.md`, count the index entries. Report agents with accumulated context:
   > - **@clawdia** has built up 14 memories (feedback, project context, references)
   > - **@aria** has 3 memories

3. **Shared knowledge base** — check `memory/index.md`. Report how many people profiles, projects, glossary entries, and trends are populated:
   > - **Shared memory:** 6 people profiles, 2 project histories, 42 glossary terms, 15 weekly trend snapshots

4. **Custom agents, skills, and commands** — list anything under `.claude/agents/custom-*`, `.claude/skills/custom-*`, `.claude/commands/custom-*`. These are workspace-specific extensions the user created.

5. **Orphaned folders** — list any directories in `workspace/` that do **not** match a declared agent working folder. These may be legacy or manual organization and deserve a heads-up:
   > - `workspace/meetings/` — managed by the sync-meetings routine (not owned by any agent, this is expected)
   > - `workspace/{unknown}/` — not matched to any agent, you may want to review

6. **Config status** — check `config/workspace.yaml` values. If `owner`, `company`, `language`, or `timezone` are missing/default, flag them as "needs configuration".

Present all of this as a concise summary under a heading like:

> ## Your workspace so far
>
> Here's what's already been customized in **{workspace.name}**:
> - {bulleted list from items 1-6 above}
>
> This tells you where you've invested setup time. Agents with pending `_improvements.md` notes are great targets for your next session — open the file with your agent and clear the backlog.

## What to Do Next

Based on what you discovered in the customizations phase, suggest **personalized** next steps — don't hardcode suggestions:

- If the user has populated `memory/people/` but not `memory/projects/` → suggest updating project context
- If any agent has `_improvements.md` → suggest tackling it
- If no routines are scheduled → suggest running a morning briefing manually
- If the user has `custom-*` agents → suggest trying one of them
- Default: suggest "good morning" to `@clawdia` (if installed) for the daily briefing

End with:

> Just tell me what you're working on and I'll route you to the right agent.

## Tone

- Enthusiastic but not overwhelming — show value quickly
- Let the user explore at their own pace
- Suggest concrete actions, not abstract descriptions
- If they seem experienced, be concise; if new, be more detailed
- Always end with an invitation to try something: "Want to try one of these now?"
