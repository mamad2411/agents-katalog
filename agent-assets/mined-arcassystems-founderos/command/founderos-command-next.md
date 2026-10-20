---
description: Recommend the next action. Say "what should I focus on next?" (or run /next). Reads priorities, clients, cadence, and brain, then recommends one thing with reasoning. Read-only.
---

# /next

Recommend ONE next action across everything the founder is currently doing. This is the orchestration command. It reads priorities, clients, cadence, and brain, then reasons about what to recommend.

## Procedure (in order)

### Step 0. Route by operator type

Before ranking, check who this is for. Read the `**Role:**` line under `## Basics` in `core/identity.md`, and whichever snapshot block the file carries (`## Founder Snapshot` or `## Role Snapshot`), if any. The role is the gate, not the profile variant - the variant field never holds `team_of_one`.

If the role is `founder` or `team_of_one` and a `## Founder Snapshot` block exists, OR the role is `operator` and a `## Role Snapshot` block exists, do NOT run the generic ranking below. Run the `founder-next-move` propose engine instead. It reads the same files, works out where they actually are, and names the single highest-leverage move - toward a paying customer on the founder path, toward the work they own on the operator path - with a three-option close. The engine handles a thin snapshot itself - it proposes a capture move when fields are missing - so route to it whenever the matching block exists, even half-filled. Never send someone who has a snapshot to the generic ranking.

For every other case (no identity file, a `student` / `career-mover` install with no snapshot block, or an older install carrying neither block), continue with the ranking in Steps 1 to 5 below.

### Step 1. Verify setup

Read `context/priorities.md`. If the file does not exist or only contains template placeholders, reply:

> Priorities not set up. Run `/founder-os:setup` and add at least one weekly priority, or edit `context/priorities.md` directly. I can't recommend a next action without knowing what matters this week.

Stop.

### Step 2. Read context

Read these files in this order. Use whatever is present, skip what is missing.

1. `context/priorities.md` - this week's must/should/could (REQUIRED)
2. `context/clients.md` - active deals and prospects (REQUIRED)
3. `brain/needs-input.md` - any open ask blocking a workflow (skip if file missing)
4. `brain/flags.md` - OPEN flags only (skip if file missing)
5. `context/decisions.md` - any item whose re-trigger condition has fired today (skip if file missing)
6. `cadence/daily-anchors.md` - today's anchors (skip if file missing or stale)
7. `cadence/weekly-commitments.md` - this week's commitments (skip if file missing or stale)
8. `brain/log.md` - last 3 entries only (skip if file missing)

If `cadence/daily-anchors.md` exists but the `## Today:` date is past, treat it as stale - flag it in the output.

### Step 3. Apply ranking logic

Walk this decision tree in order. Stop at the first match.

**Rule 1 - Blockers from needs-input win.**
If any open `brain/needs-input.md` ask blocks an active priority or deal, surface the ask as the recommendation. Do not recommend any other action - the founder has to provide the input first.

**Rule 2 - Re-triggered parked decisions are surfaced next.**
If a `context/decisions.md` parked item has a re-trigger condition that has fired today (date passed, or signal mentioned in recent log), surface that decision as the recommendation.

**Rule 3 - Stalled deals (no touch in 7+ days, no blocker) get high priority.**
If an active deal in `context/clients.md` has a `Last touched` date more than 7 days ago AND no blocker, recommend its next move. Revenue stalls cost the most.

**Rule 4 - Today's anchors matter.**
If `cadence/daily-anchors.md` is current and has unfinished anchors, recommend the first unfinished anchor.

**Rule 5 - This week's MUST DO commitments next.**
If a `weekly-commitments.md` MUST DO item has no recent log activity and no kill-criterion fire, recommend its next move via the matching priority.

**Rule 6 - Highest-impact SHOULD DO if MUSTs are clear.**
If all MUST DO items have recent activity, recommend the highest-impact SHOULD DO item.

**Rule 7 - No clear recommendation.**
If none of the above produce a recommendation, reply: "I don't have enough context to recommend. Set this week's MUST DO list in `cadence/weekly-commitments.md` or update an active deal in `context/clients.md`." Stop.

### Step 4. Render output

Use this exact format:

```
DO THIS NEXT
<action in one sentence>

WHY
<one or two sentences explaining the call - reference the rule that fired>

EXPECTED TIME
<rough estimate - 5min, 30min, 1h, 2h, 4h, half-day>

WHAT IT UNBLOCKS
<what downstream work, deal, or priority this clears - or "nothing immediate" if standalone progress>

SECOND-BEST (if you can't do the above)
<one alternative action with one-line trade-off>

CONTEXT
- Active priorities: <count>
- Active deals: <count>
- Open flags: <count>
- Open needs-input: <count>
- Today's anchors: <"current" | "stale - last refresh YYYY-MM-DD" | "not set">
```

If today's anchors are stale, surface that explicitly.

If the recommendation came from Rule 1 (needs-input blocker), the SECOND-BEST line should suggest unblocking a different priority or deal that doesn't depend on the same ask. If no such option exists, write "Address the blocker first - all active work depends on it."

### Step 4.5. Two rules on what you recommend

**It has to be their hands.** The recommendation is something the founder does: a call, a message, a decision, a piece of work. Never "review the queue", "triage your flags", or anything whose output is a tidier OS. If the highest-ranked item is really work the OS should be doing itself, say that plainly and recommend the next thing that genuinely needs a person. A recommendation that maintains the system instead of moving the business is the failure mode this rule exists to stop.

**Rank on what would move, not on what would close.** Rule 3 outranks Rule 6 for exactly this reason: a stalled deal is a thing that could move, and a tidy list is not. When two candidates score alike, prefer the one where something outside the OS changes - someone replies, a decision lands, money arrives. Prefer the one that only changes the OS last, and say so when that is all that is left.

### Step 5. Stop

Do not invoke other skills. Do not write to any file. /next is read-only - the founder's job is to act, your job is to recommend. The founder can run `/today` for the broader picture, or run a specific skill for execution.

## Rules

- Read-only. Do not modify any file.
- One recommendation. Not three. Not a menu. /next exists because the founder has too many options - your job is to compress them.
- Reasoning is required. Every recommendation must cite WHY (the rule that fired).
- No em dashes or en dashes. Hyphens with spaces.
- This command works only inside a FounderOS install. If BOTH `core/identity.md` and `CLAUDE.md` are missing from the working directory, reply: `Not a FounderOS install. Open your FounderOS folder and try again.` (Do not test for `.claude-plugin/` - it exists only on the plugin path, and setup builds the data folder without it.)
- If the brain layer doesn't exist (older version of FounderOS without brain/), fall back to recommending purely from priorities + clients + cadence. Do not require brain/.

<!-- private-tag: not applicable: updates structured deal-stage fields; not user-provided speech content -->
