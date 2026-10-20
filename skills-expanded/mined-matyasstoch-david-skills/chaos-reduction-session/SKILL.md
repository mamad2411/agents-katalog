---
name: chaos-reduction-session
description: Use when David is mid-day, feels scattered, and wants help collapsing chaos into focus. Triggers on "reduce chaos", "gain clarity", "help me focus on rest of day", "I'm pulled in too many directions", "what should I actually do now". NOT for fresh morning planning (use day-plan for that).
---

# Chaos Reduction Session

Mid-day or mid-task focus reset. David already has things in motion — calls scheduled, tasks half-done, swirl in head. Goal: collapse it into a ranked plan around the **actual remaining time window** and **locked calendar items**.

Distinct from `day-plan`: that's a structured morning 5-question flow starting from Todoist fetch. This is faster, lighter, conversational. Starts from what's swirling in his head right now.

## ABSOLUTE RULE — UPDATE THE DAILY FILE AFTER EVERY USER RESPONSE

David said it explicitly: "you are breaking the rule! i told you to update the file after EVERY one of my responses"

This is non-negotiable. After every single user message in a chaos-reduction session, patch `work/daily/DD-MM-YYYY.md` with the new info, decision, or reorder — BEFORE replying with analysis. The file is the source of truth, not the chat scrollback. If you reply without updating, you've broken the rule.

Reorder decisions especially must be logged with a one-line note in the file's `## Notes` section ("Reorder decision (TIME): X moved to #N because Y").

## Flow

### Step 0 — Create or find today's daily file

- `date` to confirm local time and date (David travels timezones).
- Check `work/daily/DD-MM-YYYY.md`. If exists, append. If not, create with the priority-list scaffold from `work/daily/AGENTS.md` rules.
- Initial file: empty priority list + Notes section with `Session goal: reduce chaos, get clarity on rest-of-day focus.`

### Step 1 — Brain dump (one question)

Ask: "What's swirling in your head right now? Dump everything that's pulling at your attention — tasks, decisions, worries, half-started things. Raw list, no order."

Wait. Save the raw dump into the daily file under `## Brain Dump (raw, unsorted)`.

### Step 2 — Get the time window + locked calendar

Two questions, ONE AT A TIME (never combined — see `about-david` rules):

1. "What time is it now and when's your hard stop tonight?"
2. "What's locked on your calendar today? Calls, meetings — who, when, how long?" (Accept screenshot of calendar.)

After answer: write `## Locked Calendar` block in the file. Compute and present the **free windows between locked items**. This is the most clarifying single move — David sees actual capacity instead of a vague "today".

### Step 3 — Rank against constraints

Build the priority list. Rules:
- Anything with a **hard external clock** (today's upload, time-locked deliverable) wins.
- Anything **psychologically heavy** that nags during deep work goes early — sending the heavy thing first clears the head. (See pitfall #2 below.)
- **Contiguous-context tasks should sit next to each other.** E.g., pre-production → recording back-to-back, because the context is warm.
- **Park anything that needs a real block but won't fit today.** Don't try to cram a 3-4h "total mess" task into 30-min scraps. Name it explicitly in `## Parked Today` with the reason and what it actually needs.
- **Engine call:** if a teammate/team isn't taking something seriously, that's a separate problem — don't bundle "fix the human" with "make tangible progress on the work itself".

Present the ranked list with WHY for each item. David pushes back, you adjust.

### Step 4 — Reorder discussions

David will often question the order ("should I do X first instead of Y?"). When he asks, give a concise opinion with reasoning. Don't hedge. Don't list pros and cons of both endlessly — pick one, defend it briefly. Then update the file immediately with the new order AND a one-line decision note.

### Step 5 — End the session by sending him to do #1

The session is not the goal. Execution is. End with: "Go do #1 right now. [Concrete first action]." Stop talking.

## Pitfalls

1. **Updating the file lazily.** David caught this. Update after EVERY response. Use `patch` to modify specific sections — never `write_file` to overwrite (you'll lose work). Read first if unsure.

2. **Defaulting "deep work first" without considering psychological load.** Example: David first ranked pre-production before an important voice note. But the unsent voice note would have nagged during deep work. Correct call was to send the emotional/relational thing first (15 min), then attack deep work with a clean head. Always ask: "Will this nag him during the deep work block?"

3. **Combining two questions into one.** David hates this. "What time is it AND what calls do you have?" → reject. Ask one, wait, ask the next.

4. **Building the ranked list without the time window.** Without `now → hard stop` and locked calendar, the ranking is fantasy. Free windows are the actual constraint.

5. **Pre-loading downstream decisions.** If a task triggers a follow-up (e.g., voice note → call later, sales email → response handling), do NOT pre-plan the downstream now. Park it. Decide when the trigger fires.

6. **Treating "fix the underperforming teammate" as part of the work task.** Separate problem. The work task: make one concrete tangible move on the work itself, not on the human. Bring the human issue to the relevant 1-on-1 / bottlenecks call.

7. **Suggesting Nietzsche / reading / introspection as primary slots.** They go in evening low-energy buffer, after main execution. Q2 goals matter but reading is not a deep-work slot.

8. **Sending him off without a concrete first action.** "Now go execute" = weak. "Go send the voice note. ~15 min. Then start pre-production." = correct.

9. **When drafting a sensitive message (voice note / hard convo opener), softening for the recipient's comfort.** External feedback (from friends/father) will often push for softer phrasing. David is usually optimizing for SIGNAL (her real response to a real question), not for keeping the conversation pleasant. When asked to compare a softened version vs. his version, default to defending his — unless the softer one is genuinely more direct or non-needy. Comfort optimization is a smell. See `references/voice-note-drafting.md`.

10. **Saving a drafted message to a standalone file too early.** When David is actively iterating on phrasing, keep edits in-place in the daily file or scratchpad. Only save to `/personal/<topic>/voice-note-DD-MM-YYYY.md` (or similar) once the script is locked. Otherwise you create a stale file you have to keep patching.

## File update pattern

For each update, use `patch` with surgical `old_string` / `new_string` replacement. Never rewrite the whole priority list section unless reordering — and even then, patch just the numbered list, not the whole file.

When reorder happens, also append to `## Notes`:
```
- **Reorder decision (HH:MMam/pm):** [X] moved to #[N], [Y] moved to #[M]. Reasoning: [one line].
```

## Output style during the session

- Ultra-concise. Single recommendations with one-line reasoning.
- No filler. No "great question". No "let's explore".
- When David asks "which is better?" — pick one, defend in 2-3 lines, move on.
- Bold key decisions. Plain prose for reasoning.
