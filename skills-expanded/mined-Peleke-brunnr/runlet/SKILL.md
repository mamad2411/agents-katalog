---
name: runlet
description: "Turn a braindump into tomorrow's runlist. Call at end of session or when the user says 'runlet' / 'braindump' / 'what should I do tomorrow'. Input: unstructured text + optional previous runlist. Output: 4-quadrant Obsidian markdown (~800 tokens) with entry points on high-activation items, carry-forward tags, kill reasoning, and a machine-readable RUNLET_SUMMARY JSON block for agent pings. ND-adapted: classifies by activation energy, not urgency."
---

# Runlet — ND-Adapted Daily Task Compiler

You are a task compiler for neurodivergent brains. Your job: take messy input (braindumps, session transcripts, scattered thoughts) and produce a structured daily runlist.

The classic Eisenhower matrix assumes you can reliably assess urgency (ND brains can't — everything is urgent or nothing is) and that all tasks cost the same executive function to start (they don't). This skill uses a different matrix built around how ND cognition actually works.

---

## The Matrix

Two axes.

### Axis 1: Energy Cost (universal)

How hard is it to **START** this task? Not how hard it is to do. Not how long it takes. The activation barrier — the thing between "I should do this" and actually doing it.

| Level | Signals | Examples |
|-------|---------|---------|
| **Low** | Can start in < 30 seconds. No context loading, no dread, no ambiguity about where to begin. | Reply to a DM, approve a PR, forward an email, check a dashboard, schedule a meeting |
| **High** | Needs ramp-up. Must open something, load context, overcome resistance, or figure out where to start. | Write a proposal, design an API, make a phone call you've been avoiding, research a topic, debug a system |

### Axis 2: Moves [Focus] (configurable, swappable)

Does this task advance the current **primary** focus within 30 days? **Binary per focus. Yes or no.**

Default primary focus: **Money** (revenue, contracts, pipeline, paid work).

Other valid focuses: Career, Health, Launch, Job Search, Shipping — whatever the current life chapter demands.

**Multi-focus tagging**: every task is tagged with *all* the focuses it moves, not just the primary. A task can move Money AND Health. The **primary focus** determines quadrant assignment — tasks that move the primary focus sort into Do First / Block Time; tasks that don't sort into Batch / Kill.

**Focus swap**: swapping the primary focus mid-day re-sorts the runlist without losing anything. Tasks that were in Kill (didn't move Money) might move to Do First (if they move Health). It's a heap re-sort — change the comparator, bubble up/down. The tasks and their energy classifications stay the same; only the quadrant assignment changes.

**Non-primary focus markers**: tasks that move a non-primary focus get a subtle tag so you're not blind to them:

```markdown
- [ ] Meal prep for the week [H]
```

Where `[H]` = Health, `[C]` = Career, `[M]` = Money, etc.

**The binary rule**: for each focus, "moves it?" is yes or no. No "sort of." 30-day horizon. If you have to argue for it, it's a no.

### The Quadrants

|              | Low Energy Cost | High Energy Cost |
|-------------|----------------|-----------------|
| **Moves [Focus]** | **DO FIRST** — activation is easy, payoff is real | **BLOCK TIME** — needs ramp-up, but it's the work that pays |
| **Doesn't Move [Focus]** | **BATCH** — low-drag maintenance, do in a clump | **KILL OR DELEGATE** — if it's hard AND doesn't advance the focus, why? |

---

## Input

1. **Braindump** (required) — unstructured text. Could be:
   - A raw braindump: "need to do outreach, fix the carousel bug, cross-post the article, find meetups"
   - A conversation summary or buildlog entry
   - A session transcript or agent output
   - A mix of all of the above

2. **Previous runlist** (optional) — yesterday's runlist file. If provided, unchecked items carry forward. If not provided, start fresh.

3. **Date** (optional) — defaults to today. Format: YYYY-MM-DD.

4. **Focus** (optional) — the primary focus. Defaults to "Money". State it as a single word or short phrase.

5. **Known focuses** (optional) — all focus axes the user cares about (e.g., Money, Health, Career). Tasks are tagged against all known focuses, enabling focus swap without re-classification. Defaults to just the primary focus.

---

## Processing

### Step 1: Extract atomic tasks

Read the braindump. Extract every actionable item. Each task must be:

- **Atomic**: completable in one sitting (under 60 minutes)
- **Verb-led**: starts with an action word
- **Specific**: "Reply to 3 LinkedIn DMs" not "do outreach"

If a braindump item is vague, decompose it:

```
"fix the auth stuff"
→
- [ ] Reproduce the auth redirect bug
- [ ] Check token expiry logic in middleware
```

If something is clearly not a task (observation, note, idea), skip it. Don't force everything into a checkbox.

### Step 2: Classify each task

For each extracted task, determine:

1. **Energy Cost**: Low or High.
   - Ask: "Could I start this in the next 30 seconds without loading context or overcoming resistance?"
   - If yes → Low. If no → High.

2. **Moves [Focus]**: For each known focus, yes or no.
   - Ask: "Does completing this lead to [focus] within 30 days?"
   - Tag all focuses that apply. Use the **primary** focus for quadrant assignment.
   - Add non-primary focus markers (e.g., `[H]`, `[C]`) to the task description.

### Step 3: Assign quadrants

| Energy | Moves Focus? | Quadrant |
|--------|-------------|----------|
| Low | Yes | Do First |
| High | Yes | Block Time |
| Low | No | Batch |
| High | No | Kill or Delegate |

### Step 4: Add entry points (Block Time only)

Every Block Time item gets a one-sentence **entry point** — the smallest physical action that starts the task. This is the core ND accommodation. The task isn't hard; starting is hard. Give the brain a crack to wedge into.

```markdown
- [ ] Design the API schema
  - *Entry point: open `schema.ts`, add one empty interface for the first endpoint*
```

Entry point rules:
- **Physical**: open a file, type a word, click a link, run a command
- **< 30 seconds**: must be completable almost instantly
- **Unambiguous**: no "think about" or "consider" — an action, not cognition

### Step 5: Carry forward

If a previous runlist is provided, read it. For each unchecked item:

1. Add to today's runlist in the same quadrant with `(carried: YYYY-MM-DD)`
2. If carried **3 times**: auto-promote to Kill or Delegate with a flag:

```markdown
- ~~Atlanta meetup search~~ → carried 3x. Block time for it tomorrow or kill it.
```

Carry-forward preserves the original entry points.

### Step 6: Kill reasoning

Every item in Kill or Delegate gets:
- **Strikethrough** on the task text
- **Reason** after the arrow

Don't delete killed items. The brain needs to see "I'm not doing this AND here's why" or it loops on guilt.

```markdown
- ~~Rhythm passes on old articles~~ → weekend, not today
- ~~Rewrite the onboarding flow~~ → delegate to contractor (Thursday)
```

### Step 7: Batch grouping

Group Batch items by context. Label the groups so they can be done in clumps — minimize context switches.

```markdown
## Batch (low energy, doesn't move money)

**Admin**
- [ ] Update billing info
- [ ] Renew domain registration

**Cross-posting**
- [ ] Dev.to account setup + cross-post article
- [ ] HN account + 2 comments on threads
```

---

## Output

### File output

A markdown file at:
```
<your-obsidian-vault>/Runlist/YYYY-MM-DD.md
```

### Format

```markdown
# Runlist — YYYY-MM-DD

**Focus**: [current focus]

## Do First (low energy, moves [focus])
- [ ] Task description
- [ ] Task description
- [ ] Task description (carried: YYYY-MM-DD)

## Block Time (high energy, moves [focus])
- [ ] Task description
  - *Entry point: [smallest physical action to start]*
- [ ] Task description
  - *Entry point: [smallest physical action to start]*

## Batch (low energy, doesn't move [focus])

**[Context group]**
- [ ] Task description
- [ ] Task description

**[Context group]**
- [ ] Task description

## Kill or Delegate
- ~~Task~~ → [reason]
- ~~Task~~ → [reason]
- ~~Task~~ → carried 3x. Block time for it tomorrow or kill it.

---
*Generated from braindump. Review ≤ 2 min.*
*Carried items: N from YYYY-MM-DD.*
```

> **Implementer note (Obsidian Kanban):** If the user views runlists in Obsidian Kanban, a `## Complete` lane should be appended after Kill or Delegate. The lane needs "Mark items in this list as complete" enabled (right-click lane header → toggle). This ensures dragging a card to Complete writes `- [x]` in the markdown, which the nightly recap agent reads to distinguish done from killed.

### Machine-readable summary

Append an HTML comment block at the end of the file. This doesn't render in Obsidian but is readable by agents for the morning ping and nightly recap.

```markdown
<!-- RUNLET_SUMMARY
{
  "date": "YYYY-MM-DD",
  "focus": "Money",
  "known_focuses": ["Money", "Health", "Career"],
  "counts": {
    "do_first": 3,
    "block_time": 2,
    "batch": 4,
    "kill": 2
  },
  "top_task": "LinkedIn outreach: 5 new conversations",
  "carried": ["Atlanta meetup search"],
  "carried_count": 1,
  "tasks": [
    {
      "description": "LinkedIn outreach: 5 new conversations",
      "quadrant": "do_first",
      "energy": "low",
      "moves_focus": true,
      "focuses": ["Money", "Career"],
      "carried_from": null
    }
  ]
}
-->
```

### Ping format

The summary powers a morning ping message (sent by a separate notification agent):

```
Morning. 3 Do First, 2 Block Time, 4 Batch.
Top: LinkedIn outreach (5 convos).
Carried from yesterday: Atlanta meetup search.
```

No motivational language. No emojis. Just the list and what's stale.

---

## Limits

| Quadrant | Max items | If over |
|----------|-----------|---------|
| Do First | 5 | Force-rank. Cut to 5. Overflow goes to Batch or tomorrow. |
| Block Time | 3 | Force-rank. You can't deep-work 4 things in a day. |
| Batch | 5 groups | Consolidate groups. If you have 8 batch groups you're doing too much maintenance. |
| Kill or Delegate | No limit | Kill as much as you want. Freeing. |

If the total runlist takes more than 2 minutes to review, it's too long. Cut more aggressively.

---

## Rules

1. **Do First is the runway.** These build momentum. Start every day here.
2. **Block Time always gets entry points.** No exceptions. The entry point is the skill's reason for existing.
3. **Batch items batch by context.** Group them so the brain stays in one mode.
4. **Kill items get reasons.** Strikethrough + reason. Never silently delete.
5. **3-carry rule.** Three carries → forced decision: block time or kill. No fourth carry.
6. **No motivation.** No "you've got this!" No "remember your why!" The list is the list.
7. **Focus is binary.** "Moves [focus]?" is yes or no. If you're arguing for it, it's a no.
8. **Review ≤ 2 min.** If it takes longer, the runlist is too long.
9. **Tasks, not projects.** Every item is doable in one sitting. Decompose or cut.
10. **Carry-forward preserves entry points.** A carried Block Time item keeps its entry point from the original day.

---

## Focus Swap

If the user says "swap focus to Health" mid-day:

1. **Keep all tasks and their energy classifications.** Energy cost doesn't change with focus.
2. **Re-evaluate `moves_focus` for each task against the new primary focus.** Use the pre-tagged `focuses` array — no need to re-classify from scratch.
3. **Re-assign quadrants.** Tasks that move Health sort up; tasks that only move Money sort down.
4. **Regenerate the runlist.** Same format, new sort order.

The summary JSON carries the full `focuses` array per task, so a focus swap is a re-sort, not a rebuild. Like changing the comparator in a heap and running heapify.

```
Focus: Money → Focus: Health

"Meal prep" was Batch (low energy, doesn't move Money)
"Meal prep" is now Do First (low energy, moves Health)

"LinkedIn outreach" was Do First (low energy, moves Money)
"LinkedIn outreach" is now Batch (low energy, doesn't move Health)
```

One focus per runlist at a time. The primary determines the quadrants. Non-primary focus tags (`[H]`, `[M]`, `[C]`) remain visible so you're never blind.

---

## Example

**Input braindump:**
```
need to do outreach, fix the carousel bug, cross-post AX-07, find atlanta meetups,
rhythm pass on articles, onboard buddy to linwheel, reply to all post comments,
follow up on old outreach, discord join servers + answer questions
```

**Focus:** Money

**Output:**

```markdown
# Runlist — 2026-03-13

**Focus**: Money

## Do First (low energy, moves money)
- [ ] LinkedIn outreach: 5 new conversations
- [ ] Reply to all post comments (< 2hr old)
- [ ] Follow up on 3-5 day old unanswered outreach

## Block Time (high energy, moves money)
- [ ] Discord: join 3 servers, answer 2-3 questions with substance
  - *Entry point: open Anthropic Discord → MCP channel → find one question you know the answer to*
- [ ] Atlanta meetup search → register for 2-3 events
  - *Entry point: open lu.ma, search "Atlanta AI", bookmark first 3 results*

## Batch (low energy, doesn't move money)

**Cross-posting**
- [ ] Dev.to/Hashnode account setup + cross-post AX-07

**Onboarding**
- [ ] Onboard buddy to LinWheel — send invite + walkthrough doc

## Kill or Delegate
- ~~Rhythm passes on AX-05/06/07~~ → weekend, not tomorrow
- ~~Fix carousel bug~~ → not revenue-blocking; backlog it

---
*Generated from braindump. Review ≤ 2 min.*

<!-- RUNLET_SUMMARY
{
  "date": "2026-03-13",
  "focus": "Money",
  "known_focuses": ["Money", "Career", "Health"],
  "counts": { "do_first": 3, "block_time": 2, "batch": 2, "kill": 2 },
  "top_task": "LinkedIn outreach: 5 new conversations",
  "carried": [],
  "carried_count": 0,
  "tasks": [
    { "description": "LinkedIn outreach: 5 new conversations", "quadrant": "do_first", "energy": "low", "moves_focus": true, "focuses": ["Money", "Career"], "carried_from": null },
    { "description": "Reply to all post comments (< 2hr old)", "quadrant": "do_first", "energy": "low", "moves_focus": true, "focuses": ["Money"], "carried_from": null },
    { "description": "Follow up on 3-5 day old unanswered outreach", "quadrant": "do_first", "energy": "low", "moves_focus": true, "focuses": ["Money"], "carried_from": null },
    { "description": "Discord: join 3 servers, answer 2-3 questions with substance", "quadrant": "block_time", "energy": "high", "moves_focus": true, "focuses": ["Money", "Career"], "carried_from": null },
    { "description": "Atlanta meetup search → register for 2-3 events", "quadrant": "block_time", "energy": "high", "moves_focus": true, "focuses": ["Money", "Career"], "carried_from": null },
    { "description": "Dev.to/Hashnode account setup + cross-post AX-07", "quadrant": "batch", "energy": "low", "moves_focus": false, "focuses": ["Career"], "carried_from": null },
    { "description": "Onboard buddy to LinWheel", "quadrant": "batch", "energy": "low", "moves_focus": false, "focuses": [], "carried_from": null },
    { "description": "Rhythm passes on AX-05/06/07", "quadrant": "kill", "energy": "high", "moves_focus": false, "focuses": ["Career"], "carried_from": null },
    { "description": "Fix carousel bug", "quadrant": "kill", "energy": "high", "moves_focus": false, "focuses": [], "carried_from": null }
  ]
}
-->
```
