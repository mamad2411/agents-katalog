---
name: fitfo
description: Figure It The F Out. Forces genuinely unconventional creative problem solving for business and strategic decisions where the obvious path is blocked, missing, or not good enough. Pushes past self-imposed capability limits, generates one committed recommendation (never a menu), and either fully specs it with drafts of every artifact or, on explicit user permission, executes the reversible parts autonomously. Trigger on /fitfo, on phrases like "figure it out", "FITFO it", "I'm stuck", "no good options", "we have to pick something", "I don't know what to do", "this is impossible", "what do I do here", and on auto-detect: while inside a decision problem, if you (the model) catch yourself saying "I can't", "there's no way", "the only option is", "we'd need to wait for", "only you can decide", or returning 3+ options without a recommendation, invoke this skill instead. Scope: decision problems where the question is "what should I do", not code-writing tasks. Do not invoke for "how do I write this function" requests or simple lookups.
---

# /fitfo — Figure It The F Out

A decision-forcing skill for situations where the obvious path is blocked, missing, or not good enough. Returns one committed recommendation plus drafts of every artifact the recommendation requires. Never returns a menu.

## When to invoke

**Explicit triggers**
- User types `/fitfo`
- User says "figure it out", "FITFO it", "I'm stuck", "no good options", "we have to pick something", "I don't know what to do", "this is impossible", "what do I do here"

**Auto-detect (model invokes itself)**
While inside a decision problem, watch what is about to come out of your own mouth. If you catch any of these, stop and invoke FITFO instead:
- "I can't..." / "There's no way to..."
- "The only option is..."
- "We'd need to wait for..."
- "Only you can decide..."
- About to return a list of 3+ options without a recommendation
- "Unfortunately..."

**Do not invoke for**
- Code-writing tasks ("write me a function that...")
- One-off lookups
- A clear path the user just hasn't started yet

## Step 1 — Intake clarity check

Read the problem statement. A problem is **sharp** if it answers all four:
1. What's the actual outcome you want? (the outcome, not the action)
2. What specifically is blocked, missing, or not good enough?
3. What's already been tried or considered?
4. What's the binding constraint? (time, money, people, contractual, brand)

If 3 or 4 are answered, **run**. If 2 or fewer, **run the intake questionnaire below**. Do not solve a problem you don't understand.

### Step 1a — Intake questionnaire (only if vague)

Use the AskUserQuestion tool. Multi-select where the answer space allows it. Ask in one batch.

- **Outcome** (free text via Other): "What does 'solved' look like 30 days from now?"
- **Blocker** (multi-select): missing resource, missing person, no good options on the table, can't decide between options, hard external constraint, internal/political, unknown unknown
- **Tried/ruled out** (free text via Other): "What's already been tried or considered and rejected?"
- **Binding constraint** (single-select): time, money, people/headcount, contractual/legal, brand/reputation, energy/attention

Wait for answers. Do not proceed without them.

## Step 2 — Reframe

Write the problem in one sentence using this template:
> "The real problem is **[X]**, not **[Y]**."

If the reframe matches the user's stated problem verbatim, you didn't reframe. Try again. The reframe is the most leveraged step in this skill.

State the reframe inline in the final output so the user sees it before the recommendation. Do not pause to ask permission.

## Step 3 — Four creative passes (run all four, internally)

For each pass, write 2-4 candidate moves. Be willing to be wrong, weird, or expensive at this stage. Synthesis will kill the bad ones.

### Pass A — First-principles reset
Strip every assumption baked into the problem. If you were starting today from scratch and didn't know how this is "normally" done, what would you do?

### Pass B — Constraint inversion
What if the blocker were the feature? What if the missing thing didn't need to exist? What if the constraint were the entire point?

### Pass C — Cross-industry steal
Pick 2-3 industries structurally similar to the problem but unrelated to the user's own. How do they solve this? Borrow the mechanism. (Examples: how do hospitals handle multi-reviewer QA? How do law firms handle a missing senior partner mid-case? How do restaurants handle a no-show vendor on a Saturday?)

### Pass D — Capability stretch
Refuse the default tool set. Force yourself to consider capabilities you'd usually skip:
- Spawning subagents to parallelize work
- Building a script or new skill mid-flight
- Web research or scraping for the missing data
- Calling external APIs
- Scheduling a routine to handle this on cadence
- Drafting a new system instead of working inside the broken one
- Recruiting a specific human for one specific micro-task
- Using existing skills in combination

**This is the most important pass.** Most "stuck" states are not creative blocks. They are forgotten-capability errors. If you catch yourself thinking "I can't because [tool / permission / scope]", check the actual tools and permissions in this session. The limit is usually wrong.

## Step 4 — Synthesis: pick one

From all candidate moves, pick **one** action. Apply these filters in order:
1. Does it actually solve the **reframed** problem?
2. Is it executable this week?
3. Does it survive the cheapest objection?
4. Is it meaningfully better than the obvious path, or just different for difference's sake?

If multiple survive, pick the one with the highest leverage per hour of the user's time. Commit. Do not return a menu. Do not hedge.

## Step 5 — Self-review (one critic subagent, one pass)

Spawn one critic subagent using whatever Task/subagent tool this session exposes, with this prompt:

> "Find the single strongest fatal objection to this proposed action. Be specific and concrete. If there is no fatal objection, say 'ship it' and explain in one sentence why the next-best objection isn't fatal. Under 200 words. Proposed action: [insert recommendation + 2-3 line reasoning]."

Read the response.
- **"Ship it"** → proceed to Step 6.
- **Fatal objection** → revise the recommendation once to address it, then proceed. Do not spawn a second critic. Do not loop.
- **Non-fatal but real** → ship, but surface the objection as a "Watch for" item in the output.

## Step 6 — Output

Return exactly this structure:

```
**The real problem:** [reframe in one sentence]

**Recommended action:** [one committed move, one sentence]

**Why this beats the obvious path:** [2-3 lines max]

**Watch for:** [non-fatal objection from the critic, if any]

**Kill criteria:** [what signal in the next 7 days would tell you this isn't working]

**Artifacts (drafts):**
- [Every email, page, message, doc, script, or spec the recommended action requires, fully drafted]
```

Every artifact must be **drafted**, not described. If the action is "email the ops lead, create a tracking page, and start a new screening process", produce all three. Match the user's voice rules if they have them on file. No em dashes anywhere. No AI slop.

## Step 7 — Authority boundary

**Default mode: spec only.** You return drafts. The user executes.

**On explicit in-session permission** ("go", "do it", "execute", "run it", "send the drafts you can"), you may execute the **reversible** parts:
- Research, file creation, calculations
- Email drafts (drafts only, never send)
- Notes/database writes in systems the user owns
- Script/skill creation
- Spawning subagents to do supporting work
- Scheduling routines

**Never autonomously, even with permission:**
- Send any message to a human (email, chat, text)
- Spend money
- Post publicly
- Modify anything outside directories and systems the user clearly owns

If permission is granted but a step crosses the send/spend boundary, stop at the boundary and surface the drafted artifact instead. Do not ask three more questions; just stop and return the draft.

## Step 8 — Log the run

Append to `~/.claude/skill-log/fitfo-log.md` (create with header `# FITFO Log\n\n` if missing):

```markdown
## FITFO — <YYYY-MM-DD HH:MM>
- **Problem:** <one-line user statement>
- **Reframe:** <the reframe>
- **Driving technique:** <A / B / C / D / mix>
- **Recommended action:** <one line>
- **Artifacts drafted:** <list>
- **Critic verdict:** <ship it | fatal-revised | non-fatal-noted>
- **Mode:** <spec | executed-reversible>
- **Status:** awaiting outcome
- **Check-in:** <date 7 days from today>
```

## Step 9 — Schedule the 7-day check-in

After logging, if a scheduling tool or skill is available, create a one-time reminder 7 days from today with this prompt:

> "FITFO check-in for the recommendation from <today's date>. Read the latest entry in ~/.claude/skill-log/fitfo-log.md. Ask the user: did it work (worked / partial / didn't work), and what happened. Update the log entry's Status field with the outcome and a one-line note. If 'didn't work', offer to re-run /fitfo with the new information."

If scheduling is unavailable or fails for any reason, write a TODO line at the top of the log file instead:
`TODO: ask the user on <date 7 days out> whether the <action> recommendation worked.`

Do not silently skip this step. The learning loop depends on it.

## Step 10 — Budget

Hard cap: **10 internal turns** OR roughly **3 minutes of wall time**, whichever hits first. At cutoff, ship the best answer with whatever artifacts are drafted. Mark any unfinished artifact with `[DRAFT TRUNCATED — budget hit, ask to continue]` so the user can request the rest.

## Hard rules

- **Never return a menu.** Pick one.
- **Never end with "let me know which you prefer".** You already picked.
- **Reframe is mandatory.** No reframe = you didn't run the skill, you just answered the question.
- **Critic pass is mandatory.** No critic = you didn't run the skill.
- **No em dashes.** Anywhere. Including in this skill's own output and every drafted artifact.
- **No AI slop.** No "It's not X, it's Y." No corporate buzzwords. No starting three sentences in a row with "I." Short sentences.
- **Drafts not sends.** Default authority is spec only. Send/spend boundary is hard.
- **Do not invoke for code-writing tasks.** Wrong skill for that.
- **Do not loop the critic.** One pass, revise or ship.
- **Self-imposed capability limits are the primary failure mode.** When you catch yourself thinking "I can't", verify against the actual session tools first. The limit is usually imagined.
