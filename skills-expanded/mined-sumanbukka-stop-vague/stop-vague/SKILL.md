---
name: stop-vague
description: Rewrites vague workplace feedback (performance reviews, 1:1 notes, peer feedback, promotion write-ups) into specific, behavioral, actionable feedback. Use when the user pastes feedback that sounds like "great job", "needs more ownership", "be more strategic", or asks to sharpen, fix, or score feedback before delivering it ("use stop-vague", "sharpen this feedback", "score this feedback").
---

# Stop Vague

Most feedback fails because the writer knows what they mean and the reader does not. "Needs more ownership" tells the reader something is wrong and nothing about what to do on Monday. This skill finds the vague parts, asks for or infers the missing facts, and rewrites the feedback so a person could act on it or repeat it back.

## Workflow

1. Check "When to step back" first. Then read the draft. Note who it is for (the person, their manager, a calibration committee) and whether it is praise, correction, or both.
2. Score it on the five dimensions below, 1 to 10 each.
3. List every violation of the rules, quoting the exact phrase.
4. If key facts are missing (no example, no outcome), ask up to three short questions. If the user cannot answer, rewrite with clearly marked placeholders like [date] or [outcome] instead of inventing facts.
5. Rewrite with all violations fixed. Keep the writer's voice and level of warmth. Write in the language the feedback was written in, and keep names, dates, and quotes exactly as given.
6. Re-score, counting only what the writer provided. A dimension whose content is a [placeholder] cannot score above 6. If any dimension is below 7 and the missing facts can be supplied, ask for them or rewrite again; if they cannot, say what is still missing instead of raising the score.

Never invent events, quotes, numbers, or outcomes. A sharp but fabricated example is worse than a vague true one.

## Sensitive content

If the input attaches a real name to sensitive content (a PIP, compensation, termination, a health or legal matter), remind the user once in the conversation that they may want to swap the name for a placeholder like [Name] before sharing the result further, then proceed with the rewrite as normal. Do not refuse, do not repeat the reminder, and do not change the rewrite because of it. The exception is a report of someone's conduct toward another person (see "When to step back"): never suggest placeholders there, because the report needs the real names.

## When to step back

Already specific: if the draft names a moment, a behavior, an impact, and a next step, and scores 35 or above, say so, name what works, and leave it unchanged. Offer at most one small edit. Do not rewrite good feedback to look busy.

Reports of conduct toward a person, such as harassment, discrimination, or unsafe or unlawful treatment: say once that this kind of feedback may need HR or legal review, and sharpen only the facts as the writer states them. Do not score it, soften it, reframe it, or characterize the conduct, do not suggest replacing names with placeholders, and do not give legal advice. Leave the impact and the ask as placeholders for the writer to fill, since they are the writer's to state.

## The five dimensions

Specificity: Does it point to a real moment, artifact, or pattern?
Behavior: Does it describe what the person did or said, not what they are?
Impact: Does it say what changed because of it (for the team, the customer, the schedule)?
Actionability: Does the reader know the next concrete step or what to repeat?
Tone fit: Is it honest without being harsh or padded?

Below 35 out of 50 means rewrite.

## The 8 rules

1. Replace labels with behaviors. "Not a team player" becomes what they did in which meeting.
2. Attach one real example to every claim. Two if the claim is a pattern. Include when and where.
3. State the impact. What happened because of the behavior, to whom.
4. End with a next step the reader can do. Name the behavior to start, stop, or keep, and by when if it matters.
5. Cut vague intensifiers and softeners. "Very", "quite", "somewhat", "a bit", "kind of" hide the size of the issue. Use a number or a comparison.
6. Separate observation from interpretation. Say what you saw, then, if needed, say what you read into it and mark it as your read.
7. Do not bury the point. Lead with the main message, then support it. No compliment sandwiches that hide the correction.
8. Make praise as specific as criticism. Praise without a behavior cannot be repeated, so it does not reinforce anything.

## Formats

Pick one structure for the rewrite. Use it as a skeleton, not a form. Short feedback can fold it into two or three sentences.

SBI (default): Situation (when and where), Behavior (what they did), Impact (what resulted). Close with one line for the next step: what to start, stop, or keep doing.

STAR: Situation (the context), Task (what was expected or needed), Action (what they did), Result (what came of it). Close with one line for the next step. Suits promotion write-ups and self-reviews, where the story matters.

Four part: Situation, Behavior, Impact, Next step, with the next step as its own part rather than a closing line.

Choosing the format:

- Use SBI unless told otherwise.
- If the user states a preference ("use STAR", "four part"), use it and keep using it for the rest of the conversation. Do not ask again.
- In Claude Code, also look in CLAUDE.md for a line like `feedback format: STAR`. A preference stated in the conversation overrides it.
- Never ask which format to use.

The format changes the shape of the rewrite only. The rules, the scoring, and the placeholder behavior stay the same in every format.

## Output format

Unless a "When to step back" case applies, return in this order: the score table, the violations with exact quotes, the rewrite, the re-score. If the user only asks for the rewrite, give the rewrite and one line on what changed.

## Before you send

1. Every number, date, name, quote, event, and behavior in the rewrite appears in the draft or in the user's answers. Do not propose example incidents or behaviors, even as illustrations or after "e.g.", and not in your questions either: ask what happened without offering sample answers. If the draft does not say what happened, the whole behavior is a [placeholder], not just its date or number.
2. Any duration or count you state matches the dates or figures given. Recompute it. If the numbers disagree, ask the writer which is right instead of silently correcting. In rewrite-only mode, keep the writer's figure and flag the mismatch in the one-line note.
3. Each placeholder is in square brackets and names what is missing, such as [what they did] or [the impact]. It never suggests an answer, so the words "e.g." and "for example" never appear inside a rewrite or a placeholder. Wrong: [what they did, e.g., missed a deadline]. Right: [what they did].
4. The next step is something the reader can do, with a date or a [date] placeholder when timing matters.
5. No fact the writer stated was dropped, and the correction is no softer than the draft.

## References

Load on demand: references/phrases.md for phrases to catch, references/structures.md for structural patterns, references/examples.md for before and after pairs.
