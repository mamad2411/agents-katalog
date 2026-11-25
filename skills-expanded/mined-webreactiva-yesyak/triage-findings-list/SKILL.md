---
name: triage-findings-list
description: Merges findings from several reports (verification, browser testing, red team, production readiness, code review) into one numbered, deduplicated change list with traffic lights, grouped by when each change should happen and tagged with its source. Use it whenever the user asks to turn reports into a list of changes, prioritize findings, "what do we fix first", build a backlog from reviews, or decide what goes before merge and what goes later.
---

# Triage findings list

## Inputs

Read every report the user names, and by default every `*-report.md` in `.scratchpad/<slug>/`. Give each report a short source tag, for example V (verification against the spec), B (browser testing), RT (red team), P (production readiness).

## Build the list

1. **Deduplicate.** One change can fix findings from several reports. Merge them and keep all source tags and ids: `(RT2, B1)`.
2. **Write each change as an action**, not as a problem: "Wrap long words in the order list", not "Long words break the layout".
3. **Give it a light** with `traffic-light-findings`. Keep the highest light that the evidence supports.
4. **Group by timing:** 🔴 before merge (mandatory); 🟠 before merge (recommended, little code); 🟠 before production; 🟠 technical debt; 🟡 minor improvements; accepted (no change), with the reason.
5. **Number the changes 1..N** in that order. These numbers are what the user will use to approve work, so do not change them after you share the list.

For each change give: number, light, action, a short "why", the main files, and the source tags.

## Output

- Save `.scratchpad/<slug>/change-list.md`.
- In the chat, show a compact list: one line per change with number, light, action and source.
- Ask which changes to apply. Suggest a default: all 🔴 plus the cheap 🟠 before merge.
- Apply the approved changes with `execute-plan-loop` in change-list mode.
