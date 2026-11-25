---
name: cynefin-frame
description: Classify a decision context — Clear / Complicated / Complex / Chaotic — and pick the response that fits the domain instead of forcing one shape on all problems.
---

# cynefin-frame

> Before reaching for a framework, classify what kind of problem this is. The wrong response shape (e.g. "best practice" for a complex domain) is how teams burn through trust.

## When to use

- The team is reaching for a heavy framework on what's actually a Clear problem (or vice versa).
- A decision keeps stalling because no one has named what kind of decision it is.
- A retrospective wants to understand why a past decision approach didn't work.

## The four domains (Dave Snowden)

| Domain | Cause/effect | Approach | Response shape |
| ------ | ------------ | -------- | -------------- |
| **Clear** | Obvious | Sense → Categorize → Respond | Best practice. Document, automate, move on. |
| **Complicated** | Knowable with expertise | Sense → Analyze → Respond | Good practice. Bring in expertise; small group decides. |
| **Complex** | Emerges; only visible in hindsight | Probe → Sense → Respond | Emergent practice. Cheap, parallel experiments; let signal guide you. |
| **Chaotic** | None | Act → Sense → Respond | Novel practice. Stabilize first; analyze later. |

A fifth domain — **Confusion / Disorder** — is for "we don't know which of the four we're in". The answer is to break the situation into pieces until each is recognizable.

## Procedure

1. **State the situation** in one sentence.
2. **Test for Clear**: is there a known, documented answer that always works? If yes → Clear; apply the best practice and move on.
3. **Test for Complicated**: is there a known answer that experts can identify with analysis? If yes → Complicated; engage 1–3 experts, decide in a small group.
4. **Test for Complex**: are cause and effect only visible in hindsight; do similar inputs produce different outputs over time? If yes → Complex; design 2–3 cheap, parallel probes with explicit stop conditions.
5. **Test for Chaotic**: is the system actively diverging (an outage, a security breach, a runaway deploy)? If yes → Chaotic; act to stabilize first, then move it to Complex or Complicated.
6. **Confusion**: if none of the above fit cleanly, the situation is a mix. Break it up into sub-situations and classify each.
7. **Name the implication**: write down what shape of response fits, and what shape would be wrong.

## Output

```text
Cynefin frame: <situation>

One-sentence statement: …

Domain: COMPLEX
  Evidence:
    - Past attempts produced different outcomes from similar inputs.
    - Stakeholders disagree on cause/effect, not just on which solution.
    - The "right answer" only becomes visible after we ship and observe.

Response shape: Probe → Sense → Respond.
  - 3 small parallel experiments with named stop conditions.
  - Decision-makers commit to letting signal decide, not opinion.

Wrong shape (avoid):
  - Big up-front "best-practice" doc. The domain doesn't have one.
  - Single one-shot pilot disguised as a probe.

Notes:
  - If the experiments converge, the domain may shift to Complicated. Re-classify.
```

## Quality bar

- Classification is justified with 2–3 pieces of evidence from the situation, not "vibes".
- Both the right and the wrong shape are named.
- Confusion is acknowledged when present; not forced into a domain.

## Anti-patterns to avoid

- Treating Complex problems with "best-practice" docs. They go stale immediately.
- Treating Clear problems with parallel experiments. Wastes weeks on a 10-minute answer.
- Skipping classification and going straight to a framework choice. Frameworks live inside domains.
