---
name: traffic-light-findings
description: Convention for reporting findings with a traffic-light severity (🔴 blocking, 🟠 worth discussing, 🟡 minor) and stable IDs. Use it whenever you review, audit, challenge or verify anything and report what you found. This includes code reviews, security reviews, devil's advocate passes, premortems, verification reports, browser test reports and triage lists. Use it too whenever the user asks for a "semaphore", "traffic light", severity levels or a ranked list of issues. Also use it when you consolidate findings from several reviewers or subagents.
---

# Traffic-light findings

If AGENTS.md sets a different convention for this topic, follow AGENTS.md.

## Severity

| Light | Meaning | What happens next |
| --- | --- | --- |
| 🔴 | Blocking. The work does not move on (merge, release, next phase) until it is fixed. | Fix it or get an explicit decision from the user. |
| 🟠 | Worth discussing. It is a real problem or a strong counter-argument, but it does not block. | Discuss, then fix or record the decision. |
| 🟡 | Minor. A warning without real risk, or a cosmetic issue. | Fix when convenient, or accept. |

Choose the light by impact and likelihood together. If a finding is blocking only in some contexts (for example, only behind a proxy), say so and give the light for each context.

## Finding format

Give every finding a stable ID. Use a prefix that shows its source and a number: `RT1` (red team), `B2` (browser test), `V3` (verification), `P4` (production readiness), `AC-17` (acceptance criterion). Do not renumber IDs after you share them. If you must renumber, show the old and new IDs.

Each finding has an ID and a one-line title, where (`file:line`, route, document section or command), evidence (a short quote, a reproduction or test output), impact (what goes wrong, for whom) and a concrete recommendation.

## Evidence rules

- Verify before you claim. Read the code or reproduce the behavior.
- Mark findings that you reproduced yourself with ✔.
- Separate evidence from speculation. Write "not verified" when you infer something.
- Do not report a finding that you cannot connect to the code, the docs or a reproduction.

## Consolidating several reports

When you merge reports from several reviewers or subagents:

1. Merge duplicates into one finding. List who found it ("Found by: security, architecture").
2. Keep the highest severity that the evidence supports. Say when you changed a reviewer's light and why.
3. Reproduce the 🔴 and the most important 🟠 findings yourself before you report them.
4. Add a section "Verified without findings" for checks that passed. It shows what the review covered.

## Summary block

Start every report with the counts:

| | Count |
| --- | --- |
| 🔴 Blocking | n |
| 🟠 Worth discussing | n |
| 🟡 Minor | n |

## Asking the user to choose

When you ask the user which findings to act on, quote each one by ID **and** title. Check the IDs against the list before you send the question. A wrong number makes the user's answer ambiguous.
