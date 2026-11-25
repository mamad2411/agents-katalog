---
name: star-system
description: Ask the user to rate the code/output just produced on a 1-5 star scale, then ask rating-appropriate follow-up questions, log the rating, and iterate until the work reaches 4+ stars. Use when the user says "run the star system", "rate this", or invokes /star-system after a deliverable is complete — AND automatically after every deployment, without being asked.
---

# Star System — Code Rating & Feedback Loop

You have just delivered code or another work product, and the user wants to grade it. Run this process exactly.

This protocol is model-agnostic and harness-agnostic: it works for any AI model under any agent harness, IDE, or plain chat window. Where a step mentions a tool or file, treat it as an example — use your harness's equivalent, and fall back to plain chat when no equivalent exists. No step may fail just because a tool is unavailable.

## Step 1: Ask for the rating

Ask the user to rate the output you just produced, presenting this scale (if your harness has a structured choice/question tool, present the five options with it; otherwise ask in plain chat):

- ★ (1) — **Unacceptable.** Everything is wrong. The work must be redone from scratch.
- ★★ (2) — **Significant issues.** The code, UI, or another major element needs substantial rework.
- ★★★ (3) — **Acceptable.** A minimum viable product — works, but not exceptional.
- ★★★★ (4) — **Exceptional.** Very good; only minor tweaks needed in specific areas.
- ★★★★★ (5) — **Gold standard.** Exemplary. A model that all future output in this area should be measured against.

Wait for the user's answer. Do not guess or self-assign a rating.

## Step 2: Optional sub-scores (2-3 star ratings only)

If the rating is 2 or 3 stars, offer an optional breakdown so the follow-up questions target the weak dimension. Ask the user to score (1-5) any of these that apply, or skip:

- **Code quality** — structure, readability, idiom, error handling
- **UI / UX** — visual design, layout, interaction feel
- **Functionality** — does it actually do what was asked, correctly
- **Requirements fit** — was the request understood and scoped right

If the user provides sub-scores, focus Step 3's questions on the lowest-scoring dimensions and skip questions about dimensions scored 4+.

## Step 3: Ask follow-up questions scaled to the rating

The lower the rating, the more you must learn before touching the code again. Ask the questions for the given rating (one message; use a structured question tool where your harness has one, free-form chat otherwise). Adapt wording to the actual deliverable — these are topics, not scripts.

### 1 star — full diagnostic (6-8 questions)
The output is being discarded, so re-establish requirements from zero:
1. What was the single biggest failure — wrong functionality, wrong approach, wrong design, or wrong understanding of the request?
2. Was the core requirement misunderstood? Restate what you built it to do and ask the user to correct it.
3. Is there *anything* in the current output worth salvaging, or is it a true clean-slate restart?
4. What should the rebuilt version do differently at the architectural/structural level?
5. Are there examples, references, or existing code the redo should follow?
6. What constraints (stack, style, performance, scope) were violated or missed?
7. What would a 3-star (acceptable) version of this look like, at minimum?
8. Anything else that went wrong that the above didn't cover?

### 2 stars — deep rework interview (5-6 questions)
Major surgery, not a restart:
1. Which areas are the significant problems — code quality, UI/UX, functionality, performance, or something else? (multi-select; skip if sub-scores already answered this)
2. For each problem area named: what specifically is wrong, and what would "fixed" look like?
3. Which parts are working well enough to leave alone?
4. In what order should the problems be fixed (what's most painful)?
5. Are the issues fixable within the current approach, or does some part need a redesign?
6. What would move this to 4 stars?

### 3 stars — elevation interview (3-4 questions)
It works; find out what separates MVP from exceptional:
1. What's the biggest gap between this and what you'd call exceptional?
2. Which areas feel most "bare minimum" — polish, edge cases, UX, code structure? (skip if sub-scores already answered this)
3. Are there missing features or refinements that were expected but not delivered?
4. If only one thing could be improved, what should it be?

### 4 stars — tweak targeting (1-3 questions)
Close to perfect; identify the specific minor tweaks:
1. Which specific areas need the minor tweaks?
2. For each: what exactly should change?
3. Optionally: what small thing kept this from being 5 stars?

### 5 stars — no questions
Ask nothing. Instead run the Gold Standard procedure (Step 6).

## Step 4: Log the rating

Every rating round is recorded. In the project being reviewed, create or append to `ratings.md` at the project root (create it with the structure below if absent):

```markdown
# Star System Ratings

## Gold Standards
<!-- 5-star outputs live here permanently — see Step 6 -->

## Rating Log
```

Append each round under **Rating Log** as:

```markdown
### <YYYY-MM-DD> — <short deliverable name> — <stars as ★ characters> (round <N>)
- **Feedback:** <1-3 bullet summary of the user's answers>
- **Plan:** <1-2 line summary of the agreed action plan, or "n/a" for 5 stars>
```

Use the real current date. Round number increments each time the same deliverable is re-rated (Step 7). If the project has no writable root or the user declines the log, skip silently — never block the flow on logging.

## Step 5: Confirm the action plan, then execute

For ratings 1-4:
1. Play back what you heard as a concise, prioritized action plan (redo plan for 1 star; fix list for 2-4).
2. Ask the user to confirm or correct the plan.
3. Once confirmed, execute it.

## Step 6: Gold Standard procedure (5 stars)

1. Acknowledge the gold-standard rating.
2. Summarize (2-4 bullets) what made this output exemplary — the patterns, structure, and decisions worth repeating.
3. Record it permanently under the **Gold Standards** section of `ratings.md`:

```markdown
### <short deliverable name> — <YYYY-MM-DD>
- **Where:** <file paths or directory of the exemplary code>
- **Why:** <the 2-4 bullets from above>
```

4. If a memory system or agent notes file is available (e.g. AGENTS.md, .cursorrules, CLAUDE.md, or your harness's persistent memory), also add a one-line pointer there so future sessions measure new work in this area against this exemplar.

## Step 7: Re-rating loop — and after every deployment

After executing the action plan (Step 5), return to Step 1 and ask the user to re-rate the revised output.

**Ask again after every deployment, unprompted.** Any time fixed work reaches the user — shipped, released, installed on their device, pushed to the environment they will look at — that is a deployment, and it ends with the Step 1 question. Do not wait to be asked, do not batch several deployments into one rating, and do not decide on the user's behalf that a change was too small to be worth grading. The user should never have to remember to ask for the star system; the loop is what makes the rating a habit instead of an event.

Two things this is not. It is not a rating on work the user cannot see yet — if a change is committed but not deployed, finish deploying first. And it is not a prompt after every message: a turn that only investigates, answers a question, or reports findings has deployed nothing and ends normally.

- Repeat the full cycle — rate, question, log (incrementing the round number), plan, fix — until the user gives **4 or 5 stars**, or explicitly says to stop.
- On each round, only ask about what's still wrong; never re-ask settled questions.
- If a round's rating goes *down*, treat it as a signal the plan was wrong — ask what the fix broke or missed before planning again.
- When the loop ends at 4+ stars, note the final rating in the log and stop.

## Rules

- Never skip Step 1 or assume a rating from context.
- Every deployment ends with the Step 1 question, unprompted (Step 7).
- Never argue with or negotiate the rating. The rating is the user's verdict; your job is to extract actionable specifics.
- Scale strictly: 1 star = most questions, 4 stars = fewest, 5 stars = zero.
- Don't ask questions the user already answered — if they gave the rating alongside detailed feedback, only ask about the gaps.
- Keep the whole exchange efficient: batch questions rather than dribbling them one per message, unless an answer genuinely gates the next question.
