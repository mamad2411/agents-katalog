---
name: interview-synthesis
description: Turn raw user-interview notes or a transcript into a filed synthesis, kept separate from interpretation, and route durable findings to the context files. Use after the user runs one or several user interviews.
---

# Interview synthesis

Turn what a user said into something the team can act on, and file it where future sessions will find it.

## Steps

1. **Take the raw material.** A transcript, rough notes, or a voice-note dump. Ask for the interview goal and who the participant was (role, segment) if not stated.
2. **Separate observation from interpretation.** First pass: what the participant actually said and did, with short verbatim quotes. Second pass: what you and the user think it means. Never blend the two; a quote is evidence, a reading is a hypothesis.
3. **Structure the synthesis:**
   - Participant: role, segment, context, date.
   - Goal of the session.
   - What they said and did: the strongest verbatim moments, each with a one-line setup.
   - Readings: the hypotheses these moments support or weaken, stated as hypotheses.
   - Contradictions: where what they said conflicts with what they do, or with previous interviews.
   - Follow-ups: what to probe in the next session.
4. **File it.** Save to `operations/` with the date and participant slug in the filename, for example `2026-08-14-interview-nadia-churn.md`.
5. **Promote what's durable.** If a finding holds across several interviews, offer to update `context/users.md` (What we know) with a one-line digest pointing at the filed syntheses. Single-interview findings stay in `operations/`; patterns get promoted.

## Rules

- Quotes stay verbatim, including hesitations that carry meaning. Cleaning up a quote destroys the evidence.
- Flag leading questions you notice in the transcript; the next interview gets better.
- Never present one participant's view as "users want". One voice is a data point.
