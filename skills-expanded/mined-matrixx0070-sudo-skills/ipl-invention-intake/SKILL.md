---
name: ipl-invention-intake
version: 1.0.0
description: Capture an invention disclosure and run a fast patentability screen to recommend filing, trade-secret protection, or defensive publication before any statutory bar closes.
author: matrixx0070
tags: [ip, patent, invention-disclosure, patentability, trade-secret, statutory-bar, intake]
capabilities: []
---

## When to use

Use this when an inventor or team has a new invention and needs it captured cleanly before deciding whether to patent it, keep it secret, or publish it. Speed matters: public acts can start a clock that permanently forecloses patenting.

**Not for:** checking whether shipping a product infringes someone else's patent (use `ipl-fto-triage`); reviewing IP clauses in a contract (use `ipl-ip-clause-review`); or building out a full matter file (use `ipl-matter-workspace`).

## Method

1. **Capture the people and dates.** Inventors, employer/assignment status, conception date, and any reduction-to-practice date.
2. **Capture the invention.** Problem solved, the novel elements, and how it differs from what exists. Record prior art the inventors know.
3. **Screen patentability** at a high level against the four bars (below). Flag weak spots; do not conclude.
4. **CRITICAL bar check:** Has the invention been publicly disclosed, offered for sale, or published anywhere? Any of these starts or blows the §102 clock. Record exact dates.
5. **Decision point:** patent versus trade secret — patenting requires public disclosure and expires (~20 yrs); a trade secret lasts while secret but dies on independent discovery or reverse-engineering. Match to how detectable the advantage is.
6. **Recommend:** file a provisional / commission a full patentability search through an attorney / keep as trade secret / defensive publication.

**ATTORNEY-ESCALATION GATE:** Filing decisions, patentability opinions, and any imminent statutory-bar deadline route immediately to a licensed patent attorney or agent. You capture and screen; you do not opine or file. This is not legal advice.

## Example

An engineer describes a novel battery-pack cooling channel, conceived three months ago, reduced to practice in a bench prototype. Bar check: shown at a public demo 40 days ago — the 1-year AIA grace clock is running. Recommendation: escalate to counsel now to file a provisional before the bar closes; capture the assignment; not a trade secret since the demo already disclosed it.

## Pitfalls

- **Missing the disclosure clock.** A demo, sale offer, or paper can bar patenting — date-check first.
- **Skipping ownership/assignment.** An uncaptured co-inventor or unassigned employee clouds title later.
- **Concluding patentability.** You screen and flag; the opinion belongs to counsel.
- **Defaulting to "just file."** A teardown-only process may be worth more as a trade secret.

## Output format

```
INVENTION INTAKE — <short title>
Inventors / assignment: <names, employer, assigned?>
Dates: conception <date> | reduction-to-practice <date>
Problem solved / novel elements: <summary>
Known prior art: <list>
Statutory-bar check: disclosed? sold? published? <dates or "none"> | clock status: <running/clear>
Patentability screen (§101/§102/§103/§112): <notes>
Decision: provisional | full search (attorney) | trade secret | defensive publication
Escalation: <bar deadline? filing decision? -> patent counsel>
```

## Reference

Patentability bars:
- **§101 — eligible subject matter.** No abstract ideas, laws of nature, natural phenomena.
- **§102 — novelty + statutory bars.** On-sale bar, public use, printed publication; AIA first-inventor-to-file with a 1-year grace period on the inventor's own disclosures.
- **§103 — non-obviousness.** Graham factors.
- **§112 — enablement, written description, definiteness.**

The disclosure clock is the urgent one — a public act can permanently foreclose patenting. Capture inventorship and assignment at intake. This is not legal advice.
