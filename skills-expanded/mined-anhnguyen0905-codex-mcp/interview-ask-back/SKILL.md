---
name: interview-ask-back
description: Ask-back techniques for the Interview phase — 5 Whys, example-driven probing, and hidden-assumption detection to extract information the user didn't think to volunteer.
---

# Ask-Back Techniques

The user's first description is never the full requirement. These techniques surface what they didn't say.

## 5 Whys (find the real goal)

When the request is a solution ("add a retry button"), ask why until you reach the underlying problem ("uploads fail on flaky Wi-Fi") — the best implementation may differ from the requested one. Two or three whys usually suffice; stop when the answer is a business/user outcome.

## Example-driven probing (make the abstract concrete)

Ask "walk me through one concrete case": *"A user uploads a 50 MB video on a slow connection — what should happen at each step?"* Concrete walkthroughs expose edge cases, states, and sequencing that abstract descriptions hide. Do this for at least: the happy path, one failure path, and one boundary value.

## Hidden-assumption detection

Probe the assumptions both sides are silently making:

- **Scale**: "How many users/items/requests should this handle?"
- **Actors**: "Who else touches this — admins, cron jobs, other services?"
- **Lifecycle**: "What happens to existing data when this changes?"
- **Reversibility**: "If this ships wrong, how do we roll back?"
- **Priority conflicts**: "If speed of delivery and completeness conflict, which wins?"

## Contradiction check

Before finishing, restate any pair of answers that could conflict ("You want zero new dependencies, but also PDF export — those conflict; which bends?"). Users resolve contradictions instantly when shown them; code review finds them weeks later.

## Anti-patterns

- Asking questions the codebase already answers — read it first, ask only what code can't tell you.
- Accepting "make it good" — convert to a measurable statement or record it as your judgment call.
- Interviewing forever — after two rounds, summarize and confirm; refine later if execution surfaces gaps.
