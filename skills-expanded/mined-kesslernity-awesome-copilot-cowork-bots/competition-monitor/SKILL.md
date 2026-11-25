---
name: competition-monitor
description: Watches a named list of competitors and reports only when something materially changed, staying silent when nothing did. Use when the user asks what competitors have changed, to monitor competitor pricing or positioning, or to set up a competitive watch.
---

# Competition Monitor

Reports a material change and nothing else. **The suppression is the product.**

**How this differs from a news digest.** A digest finds five to eight items because five to eight
is the target. This finds zero items most weeks, and that is the correct output. A monitor that
always reports something is a monitor its reader stops opening within a month.

## Inputs
- **Deep Research** over the competitor list
- `references/config.md` for competitors, the watch list and what counts as material
- The prior run's output, read from the output folder, which is how "changed" is possible at all

## Procedure
1. **Read the prior snapshot** from `/Documents/Cowork/output/competition-<date>.md`. Without it,
   this run is a baseline, not a monitor: say so explicitly and report the current state only.
2. **For each competitor, check only the watched attributes** from config. Typically published
   pricing, packaging and tiers, a positioning statement, a named new product, a public leadership
   change. Not blog posts. Not social activity. Not hiring.
3. **Compare against the prior snapshot, attribute by attribute.**
4. **Apply the materiality test** before reporting anything:
   - Did a **number** change, or a **tier boundary** move?
   - Did a **claim** change, not its wording?
   - Is the change **visible to a customer**?

   A rewritten sentence that means the same thing is not material. A price moving from 40 to 45 is.
5. **Report only what passed the test**, each with: competitor, attribute, before, after, the date
   observed, and the source URL.
6. **Write the new snapshot** for next time, whether or not anything changed.

## Output
When something changed:

| Competitor | Attribute | Before | After | Observed | Source |

Then one line each on why it is material.

When nothing changed: **one line.** "No material change across N competitors since <date>." Then
stop. Do not list what you checked, do not summarize the market, do not add context.

## Definition of done
The snapshot is written, and either the material changes are listed with before-and-after, or a
single line says nothing changed.

**Silence is the success state and the most common one.** Resist every instinct to add value by
reporting a near-miss. If it did not pass the materiality test, it does not appear.

## When there is no data
- No prior snapshot: baseline run, said plainly.
- A competitor's page unreachable: say which and that it was not checked. **Never carry forward
  the old value as if it were confirmed today.**
- A page changed so much it cannot be compared attribute by attribute: say so rather than
  reporting a diff of the whole page.

## Boundaries
- **Never access anything behind a login, a paywall or a trial.** Public pages only.
- Never report a competitor's non-public information even if a source offers it.
- Never characterize a competitor's intent or finances. Report the observed attribute.
- **Draft only.** Circulating this is the user's action.

## Self-check
- Did everything reported pass the materiality test, or did I soften it to have something to say?
- Is an unreachable source reported as unchecked rather than unchanged?
- If nothing changed, is the output exactly one line?
