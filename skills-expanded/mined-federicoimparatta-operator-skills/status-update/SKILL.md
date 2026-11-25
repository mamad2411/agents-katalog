---
name: status-update
description: Use this skill when the user asks to write or revise a recurring status update for a team or stakeholders. Trigger phrases include "weekly update", "status update", "cycle update", "armemos el update", "update de producto". Reports outcomes, not activity. Scales to a single period or an end-of-cycle wrap. Works in English and Rioplatense Spanish.
---

# status-update

> **Anchor:** Output is what you did; outcomes are what changed. A status update reports outcomes.

## When to use

Use this skill when the user needs to write or restructure a recurring update about work in progress for a team, a manager, or a cross-functional group. Works for:

- A weekly update reporting what moved this period.
- An end-of-cycle wrap closing out a sprint, milestone, or planning cycle.
- A standing update that has drifted into a task log and needs to refocus on outcomes.

Do not use when:

- The audience is an executive who needs a decision framed in one page. Use `exec-brief` instead.
- The audience is external partners, investors, or customers. Use `stakeholder-update`.
- The work is a retrospective on a failure or incident. Use `post-mortem` for that kind of analysis.

## Philosophy

A status update is a ritual, and rituals are cheap to start and expensive to keep honest. The default failure mode is a list of activity that nobody reads twice. The fix is to report consequence.

Two concepts from the handbook apply directly. **Output vs outcomes:** write what changed in user behavior, system state, or the bet you are running, not the list of tasks the team touched. A closed ticket is output. A funnel that moved is an outcome. **Rituals serve results:** the update exists to keep a team or a stakeholder oriented toward the goal, not to prove the team was busy. If a section does not change a reader's understanding or a decision, cut it.

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

- **ES.** Rioplatense register. Vos over tú. Keep technical terms in English where that is standard in industry use: sprint, backlog, KPI, rollout, stakeholder, feature flag, AB test. Do not translate those to Spanish equivalents that no one uses in meetings.
- **EN.** Direct US business register. Short sentences. No British spelling unless the target audience is UK or AU.
- Choose the language of the audience that will read the update, not the language the user types in. Ask once if ambiguous.

## Method

1. **State the one outcome that moved this period.** Open with the single change that mattered most. Not a list. One sentence about what is different now that was not different before.
2. **Show progress against the bet or goal, not a task list.** Frame work as motion toward the goal you committed to. A reader should learn whether the bet is on track, not what the team did Monday through Friday.
3. **Name what is blocked and the decision needed, with an owner.** Every blocker gets a named decision and a named person who can unblock it. A blocker without an owner is a complaint.
4. **Report what changed in the plan and why.** If scope, sequence, or timeline moved, say so and give the reason. Silent plan drift is how trust erodes.
5. **Name next period's single most important bet.** One thing. The work that, if it slips, the period failed. Not a backlog dump.
6. **Cut anything that is activity without consequence.** Read the draft and delete every line that reports motion but no change. If a sentence would not alter a reader's decision or understanding, it does not belong.

## Templates

- `templates/en/weekly-update.md`: a single period update.
- `templates/en/cycle-update.md`: an end-of-cycle wrap.
- `templates/es/weekly-update.md`: un update de un solo periodo.
- `templates/es/cycle-update.md`: el cierre de un ciclo.

## Related skills

- `exec-brief`: use it when the audience is an executive who needs a decision in one page, not a recurring team update.
- `stakeholder-update`: use it when the audience is external partners, investors, or customers rather than the internal team.
- `roadmap-from-data`: cross-reference it when the update needs to tie progress back to a data-driven roadmap.
- `post-mortem`: use it when the work is a retrospective on a failure or incident rather than a forward-looking update.

## Anti-patterns

This skill must never produce:

- An update that opens with a list of completed tasks instead of the outcome that moved.
- An update that reports activity with no statement of what changed.
- A blocker with no named owner and no decision attached.
- A plan change buried or omitted instead of stated with its reason.
- A next-period section that dumps the whole backlog instead of naming one bet.
- An update padded with status colors or percentages that carry no meaning.
- An update written to prove the team was busy rather than to orient the reader.
- An update that mixes English and Spanish inconsistently within a single section.
- An update that cites "good progress" without naming the outcome that proves it.

## Checklist before delivery

- [ ] The update opens with the one outcome that moved this period.
- [ ] Progress is framed against the bet or goal, not as a task list.
- [ ] Every blocker has a named decision and a named owner.
- [ ] Plan changes are stated with their reason.
- [ ] Next period names a single most important bet, not a backlog.
- [ ] Every remaining line reports a change, not just activity.
- [ ] No buzzwords from the voice rules appear anywhere.
- [ ] The update reads cleanly to someone who missed the prior period.
