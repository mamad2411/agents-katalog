<!-- owner: shared | audience: all-pms | last-updated: 2026-04 -->
<!-- purpose: Set up a new persistent agent — creates workspace, personalises definition, bootstraps context from live sources -->

# Set Up Persistent Agent

Set up a new persistent agent for a PM. This command creates the full workspace, personalises the agent definition, and bootstraps context from every available source — so the PM gets a working agent they can start testing immediately.

**Arguments:** `{initials}, {name}, {agent}` where agent is one of: cos, analyst, uxr, coach, manager, strategist, engineer

Example: `/setup-agent SJ, Steve, cos`

## Instructions

### Phase 1: Validate inputs and check tools

1. Parse the arguments. If any are missing, ask for them:
   - Initials (e.g. SJ)
   - Full first name (e.g. Steve)
   - Agent type — must be one of: `cos`, `analyst`, `uxr`, `coach`, `manager`, `strategist`, `engineer`

2. Check which MCP integrations are available by testing each one silently (don't show errors to the user, just note which work):
   - Calendar (e.g. Google Calendar) — try to list today's events
   - Meeting notes (e.g. Granola, Otter) — try to list recent meetings
   - Messaging (e.g. Slack) — try to read a channel
   - Data warehouse (e.g. BigQuery, Snowflake) — try a simple query (only if agent is `analyst`)

3. Tell the user which tools are connected and which aren't. Then decide what to do based on coverage:

   **If the critical MCPs for this agent are connected** (see table below), report the status briefly and continue to Phase 2:
   > **Tools connected:** Calendar, Meeting notes, Messaging
   > **Not available:** Data warehouse (not needed for COS)

   **If critical MCPs are missing**, pause and explain why they matter before continuing. Use this framing:

   > **Tools connected:** Messaging
   > **Not connected:** Calendar, Meeting notes
   >
   > I can set up your agent now, but I'd recommend connecting Calendar and Meeting notes first. Here's why:
   >
   > - **Calendar** — without it, I can't see who you meet, how often, or when. I'll have to create blank meeting context files that you fill in manually instead of pre-populated ones with real people and topics.
   > - **Meeting notes** — without it, I can't read your meeting transcripts to find action items, decisions, or standing topics. Your todo list and state file will be based on team priorities only, not your actual work.
   >
   > The difference is significant: with these tools, your first test output will reference your real meetings, real people, and real priorities. Without them, it'll be generic and you'll spend much longer correcting it.
   >
   > To connect them: open Claude Code settings (type `/mcp` in Claude Code) and enable the integrations you have available. Once they're connected, run `/setup-agent` again.
   >
   > Or if you'd rather continue now with what's available, just say "continue" and I'll do the best I can with local files.

   Wait for the user to respond before proceeding. If they say continue, proceed to Phase 2 with whatever's available.

   **Critical MCPs by agent type:**

   | Agent | Critical | Nice to have |
   |-------|----------|-------------|
   | COS | Calendar, Meeting notes | Messaging |
   | Analyst | Data warehouse | Messaging, Meeting notes |
   | UXR | Messaging | Meeting notes |
   | Coach | Meeting notes, Calendar | Messaging |
   | Manager | Meeting notes, Calendar | Messaging |
   | Strategist | Messaging, Meeting notes | Calendar |
   | Engineer | — | Messaging |

### Phase 2: Create workspace (or detect existing one)

First, check if `team/{INITIALS}/agents/state/` already exists and contains files. This tells you whether this is a first-time setup or an additional agent.

**If this is a new PM (no existing workspace):** create everything. Don't ask the user to do any of this manually.

1. **Directories:**
   - `team/{INITIALS}/agents/state`
   - `team/{INITIALS}/agents/memory`
   - `team/{INITIALS}/agents/archive`
   - `team/{INITIALS}/daily-prep`
   - `team/{INITIALS}/recurring-meeting-context`
   - `team/{INITIALS}/post-meeting-drafts`

2. **Gitignore:** `team/*` is already gitignored in this template (with `team/TEMPLATE` whitelisted). No edit needed unless `team/{INITIALS}/` is explicitly missing from the rules.

3. **Shared memory file:** Create `team/{INITIALS}/agents/memory/shared.md` by copying `team/TEMPLATE/agents/memory/shared.md` and replacing placeholders.

4. **Todo list:** Create `team/{INITIALS}/todo_list.md` by copying `team/TEMPLATE/todo_list.md` and replacing `{YOUR_NAME}` with the PM's name.

**If the PM already has a workspace** (existing state files from a previous agent): skip all of the above — directories, gitignore, shared memory and todo list already exist. Tell them briefly:

> You already have a workspace set up from your {existing agent} agent. I'll add the {new agent} agent to it.

### Phase 3: Create and personalise the agent definition

1. Read the starter at `.claude/agents/examples/starters/starter-{agent}.md`
2. Read the real (mature) agent at `.claude/agents/{agent}.md` — this shows what a battle-tested version looks like. Note the specificity of its responsibilities and proactive behaviours
3. Copy the starter to `.claude/agents/{INITIALS}-{agent}.md`
4. Personalise it:
   - Replace all `{YOUR_NAME}` with the PM's name
   - Replace all `{INITIALS}` with their initials
   - Update the "Tools you use" section to only list MCPs that are actually connected (from Phase 1). Remove any that aren't — Claude will try to use them and fail confusingly
   - Leave the state file format, pruning rules, and memory structure unchanged — these are battle-tested

### Phase 4: Bootstrap context from live sources

Use every available source to build the PM's initial context. For each file created, add a short confidence note at the top: what you're confident about, what you've inferred, and what needs confirmation.

1. **Always** read `context/current-priorities.md` for team priorities

2. **If Calendar is available:**
   - Find recurring meetings from the last 4 weeks
   - Identify who the PM meets regularly and how often
   - Create a recurring meeting context file for each person at `team/{INITIALS}/recurring-meeting-context/{person-name}.md` (skip any that already exist — don't overwrite previous context) with:
     - Name, role (if you can infer it), frequency, day/time
     - Standing topics (inferred from meeting titles and any available notes)
     - Confidence note on what's inferred vs confirmed

3. **If Meeting notes are available:**
   - Read the last 2 weeks of meeting transcripts
   - Extract action items, decisions, and open questions
   - Use transcript content to enrich the meeting context files (standing topics, carry-forward items, recent notes)

4. **If Messaging is available:**
   - Scan relevant channels for current priorities, open threads, and recent discussions
   - Use this to inform the todo list and state file

5. **Populate the todo list** at `team/{INITIALS}/todo_list.md`. Populate "Today's Focus" and "Actions" with real items from transcripts, messaging, and priorities. If sources are thin, add 2-3 items from `current-priorities.md` and mark them as inferred.

6. **Create the initial state file** at `team/{INITIALS}/agents/state/{agent}.md` following the format in the agent definition. Populate it with real data from the sources above.

7. **Create the initial memory file** at `team/{INITIALS}/agents/memory/{agent}.md` — start it mostly empty with just the standard section headers. Memory should be earned through use, not pre-filled.

### Phase 5: Summary and next steps

Once everything is created, give the PM a clear summary. **Tailor the output based on whether this is their first agent or an additional one.**

#### If this is their first agent:

---

**Setup complete.** Here's what I created:

- Agent definition: `.claude/agents/{INITIALS}-{agent}.md`
- {N} meeting context files in `team/{INITIALS}/recurring-meeting-context/`
- Todo list: `team/{INITIALS}/todo_list.md`
- State file: `team/{INITIALS}/agents/state/{agent}.md`
- Memory file: `team/{INITIALS}/agents/memory/{agent}.md`

Some of these files contain things I've inferred (marked with confidence notes). That's fine — you'll correct them as you go and the agent learns from every correction.

---

### What you need to do now

**1. Quick review (5 minutes)**

Scan these three files for anything obviously wrong — don't try to make them perfect, just catch the big errors:
- `team/{INITIALS}/todo_list.md` — are these actually your priorities right now?
- A couple of the meeting context files — are the people, frequencies, and topics roughly right?
- `team/{INITIALS}/agents/state/{agent}.md` — does the summary of your situation feel accurate?

**2. Test your agent (10 minutes)**

Open a new conversation with your agent:

```bash
claude -a {INITIALS}-{agent}
```

Then ask it: `"{agent-specific test prompt}"`

Use the appropriate test prompt:
- COS: "Give me today's brief. What should I focus on and what do I need to prepare for?"
- Analyst: "Give me this week's funnel summary. Flag anything unusual."
- UXR: "What are the strongest customer signals from the last 2 weeks?"
- Coach: "Review my week. What patterns do you see?"
- Manager: "Prep me for my 1:1s this week."
- Strategist: "Draft the key points for this week's exec update."
- Engineer: "Sweep the workspace. What's broken or needs attention?"

**3. Correct what's wrong (in the same conversation)**

When you see the output, tell the agent directly:
- What's **wrong**: "No, I meet Sarah fortnightly not weekly"
- What's **missing**: "You didn't mention my project review on Thursday"
- What's **noise**: "I don't need the calendar density summary, drop that"

Every correction goes to the agent's memory — it won't make the same mistake twice. **Run this test-and-correct loop 2-3 times** until the output references your real priorities, your real meetings, and your real people.

**4. Use it every day**

This is the most important part. Use your agent every working day. Here's what happens:

- **After 1 week** — it knows your stakeholders, your preferred framing, the topics that matter. Output feels personalised, not generic.
- **After 2 weeks** — it starts connecting things across sessions. "This is the second week the experiment tracker hasn't been updated." "You mentioned this concern in your 1:1 with Sarah last week."
- **After 1 month** — it has real institutional knowledge. Data gotchas, seasonal patterns, who to chase about what. It catches things you'd miss.
- **After 3 months** — it carries context that even you've forgotten.

Each session, spend 2 minutes refining: remove responsibilities that produce noise, add ones you wish it had covered. The agent compounds in two ways — its memory grows automatically, and its definition improves through your edits.

**5. When you're ready for more**

Read `.claude/agents/examples/README.md` for:
- How to connect your agent to messaging (two-way — it posts outputs and you can message it back)
- How to automate it on a schedule
- How to add a second agent (just run `/setup-agent` again with a different agent type)
- What makes the difference between a good agent and a great one

#### If this is an additional agent (workspace already exists):

Keep the summary short — they already know the system.

---

**{Agent} agent added.** Here's what I created:

- Agent definition: `.claude/agents/{INITIALS}-{agent}.md`
- State file: `team/{INITIALS}/agents/state/{agent}.md`
- Memory file: `team/{INITIALS}/agents/memory/{agent}.md`

Your existing todo list, meeting context files, and shared memory are unchanged — the new agent reads them too.

**Test it now:**

```bash
claude -a {INITIALS}-{agent}
```

Then ask: `"{agent-specific test prompt}"`

Same drill as before — correct what's wrong, what's missing, and what's noise. Use it daily for a couple of weeks before automating.

**Cross-agent wiring:** This agent can read your other agents' state files. Check the agent definition — it should reference `team/{INITIALS}/agents/state/{other-agent}.md` in its source files so it knows what your other agents are tracking.

---

---

## Important rules

- **Never ask the PM to create files or directories** — do it yourself
- **Never pre-fill memory with assumptions** — memory is earned through corrections and use
- **Always include confidence notes** — the PM needs to know what to verify
- **If an MCP fails during bootstrap, skip it silently** — don't error out, just work with what's available
- **Don't modify shared files** (anything outside `team/{INITIALS}/` and `.claude/agents/{INITIALS}-*.md`)
