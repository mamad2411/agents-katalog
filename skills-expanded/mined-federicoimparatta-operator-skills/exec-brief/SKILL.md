---
name: exec-brief
description: Use this skill when the user asks to write or structure a leadership brief, a board update, or a one-page summary for executives. Trigger phrases include "exec brief", "board update", "one-pager for leadership", "resumen para el board", "brief for the CEO", "summarize this for the board". Produces a single page that leads with the bet, the number, and the ask. Works in English and Rioplatense Spanish.
---

# exec-brief

> **Anchor:** One page. The bet, the number, the ask. Leading without title.

## When to use

Use this skill when the user needs to brief executives or a board on a decision, a bet, or a result. Works for:

- A leadership brief that asks for a decision, a resource, or air cover.
- A board update that reports state against a small set of numbers.
- A one-pager that compresses a long initiative into the part leadership reads.

Do not use when:

- The user is writing a recurring update to their own team. Use `status-update` instead.
- The user is writing outward to clients or external partners. Use `stakeholder-update`.

## Philosophy

An exec brief earns attention it cannot assume. Leadership reads the first line and decides whether to read the rest. So the first line is the decision or the ask, not the background.

Two concepts carry this skill. **Output vs outcomes:** report what changed in the business or the user, not what the team produced. A list of shipped work is not a brief. **Leading without title:** the brief makes a clear recommendation and owns it. Authority comes from the clarity of the call, not from the seniority of the sender. State the bet, state the ask, and stand behind both.

## Voice rules (apply to all outputs)

- No buzzwords: leverage, empower, synergy, resonate, tapestry, delve, elevate, captivate, explore, dynamic, testament.
- No em dashes.
- No filler openings.
- Decision-oriented over descriptive.
- High-context, no overexplaining.
- Standard sentence case for formal outputs.
- ES outputs match the register of the handbook: direct, self-aware, no reverence for process, comfortable naming failure.
- EN outputs use direct US business register. Do not soften bluntness into corporate-speak.
- Language switches based on audience, not author.

## Bilingual handling

- **ES.** Rioplatense register. Vos over tú. Keep technical terms in English where that is standard in industry use: board, update, KPI, runway, burn, milestone, stakeholder, rollout, AB test. Do not translate those to Spanish equivalents that no one uses in meetings.
- **EN.** Direct US business register. Short sentences. No British spelling unless the target audience is UK or AU.
- Choose the language of the audience that will read the brief, not the language the user types in. Ask once if ambiguous.

## Method

### Step 1. Lead with the decision or the ask

Open with the call, not the context. The first sentence names what you recommend or what you need. Background, if any, lives below the fold or in an appendix link. If the reader stops after the first line, they should still know what you want from them.

### Step 2. The single metric that matters and its trend

Pick one number. Not a dashboard. The number that tells leadership whether the bet is working. State its current value, its direction, and the window over which it moved. A number without a trend is a screenshot, not a signal.

### Step 3. The bet and its current state

Name the bet in one line: what we committed to, for whom, and why. Then state where it stands today: on track, at risk, or off track, in plain words. Do not narrate the journey.

### Step 4. Top risk and what you are doing about it

One risk, the one that would actually change the outcome. Then the action already in motion to handle it. A risk without an owned response reads as a warning, not a brief.

### Step 5. The specific ask

State exactly what you need from leadership: a decision, a resource, or air cover. Make it answerable in the meeting. "Approve the hire," not "discuss headcount." If there is no ask, say so and explain why the brief exists.

### Step 6. One-page limit, everything else is an appendix link

The brief fits on one page. Anything longer is detail the reader can pull when they want it. Move methodology, full metrics, and history to a linked appendix. The page is the part leadership reads; the appendix is the part they audit.

## Templates

- `templates/en/exec-brief.md`: one-page leadership brief.
- `templates/en/board-update.md`: board-meeting update.
- `templates/es/exec-brief.md`: brief de una página para liderazgo.
- `templates/es/board-update.md`: update para reunión de board.

## Related skills

- `status-update`: use it when the audience is your own team and the update recurs, not when briefing leadership.
- `stakeholder-update`: use it when the audience is outward, clients or external partners, not internal leadership.
- `roadmap-from-data`: cross-reference it when the bet and its state need to be grounded in roadmap data.
- `okr-drafting`: cross-reference it when the single metric should tie to a committed objective.

## Anti-patterns

This skill must never produce:

- A brief that opens with background instead of the decision or the ask.
- A brief that reports shipped work instead of outcomes.
- A brief with a dashboard of metrics instead of the one number that matters.
- A brief that states a metric with no trend or time window.
- A brief that names a risk with no owned response.
- A brief that ends without a specific, answerable ask.
- A brief that runs past one page instead of linking an appendix.
- A brief that hedges the recommendation to avoid owning it.
- A brief written in press-release voice for an internal board.
- A brief that mixes English and Spanish inconsistently within a single section.

## Checklist before delivery

- [ ] First line is the decision or the ask, not background.
- [ ] One metric, with current value, trend, and time window.
- [ ] The bet is stated in one line with its current state.
- [ ] Top risk has an owned response already in motion.
- [ ] The ask is specific and answerable in the meeting.
- [ ] The brief fits on one page, with detail moved to an appendix link.
- [ ] No buzzwords from the voice rules appear anywhere.
- [ ] No em dashes appear anywhere.
