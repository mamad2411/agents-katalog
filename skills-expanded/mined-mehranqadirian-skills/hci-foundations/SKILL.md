---
name: hci-foundations
description: Applies human-computer interaction principles to evaluate or design any interface. Use whenever the user asks for a usability review, UX critique, heuristic evaluation, design justification, or wants to know why a screen feels confusing, mentions Nielsen heuristics, Norman, Shneiderman, Fitts, Hick, cognitive load, affordances or feedback, or asks which HCI principle applies, even if they only say "does this UI make sense?". Produces evidence-based, severity-rated findings and a prioritized report, then points to the platform skill for fixes.
---

# hci-foundations

The base of the `hci` category. It turns principles into questions you can answer from the actual interface, rates problems by severity and produces a report that tells a team what to fix first.

```
hci-foundations/
├── SKILL.md
├── scripts/
│   └── heuristic_audit.py            findings CSV or JSON to a prioritized report (text, md, json)
├── references/
│   ├── principles.md                 Nielsen 10, Norman, Shneiderman 8, laws of UX, Gestalt, ethics, severity scale
│   └── evaluation-methods.md         which method to use, heuristic evaluation, cognitive walkthrough, small tests
└── templates/
    ├── findings.csv                  example findings with the right columns
    └── heuristic-evaluation-report.md   report skeleton
```

## When to use

- Reviewing a screen, flow, prototype or live product for usability
- Explaining why something is confusing, with a named principle and evidence
- Choosing between two design options and justifying the choice
- Planning an evaluation, or preparing findings for stakeholders
- Deciding which platform or concern skill to apply next

## Workflow

1. **Frame the review**: who are the users, what are the 3 to 5 key tasks, which screens or flows are in scope, what device and context. Ask only for what you cannot infer. If you only have a description or a screenshot, say what you could not check (motion, timing, real data).
2. **Walk each task step by step** and ask the heuristic questions in `references/principles.md` (visibility, match, control, consistency, error prevention, recognition, efficiency, minimalism, error recovery, help).
3. **Record each problem** with location, the issue as observed (not as opinion), the violated heuristic, evidence, a severity from 0 to 4 and a specific fix. Use `templates/findings.csv` as the format.
4. **Rate severity** by frequency, impact and persistence. Do not inflate: a cosmetic issue is a 1.
5. **Generate the report**: `python3 scripts/heuristic_audit.py findings.csv --format md --out report.md`. It prioritizes by severity, counts by heuristic and lists heuristics with no findings so you can confirm they were examined, not skipped. The exit code is 1 when a severity 4 finding exists, so it can gate a release.
6. **Recommend fixes** that are concrete and minimal, and say which platform skill covers the implementation (see Related skills).
7. **State the limits**: an expert review finds likely problems, real users show actual ones. Recommend a small usability test (`hci-usability-testing`) for the top findings.

## Rules

- Tie every finding to evidence from the interface; avoid "I do not like it"
- Describe the problem and its effect on the user, not the designer's intent
- One problem per finding; keep severity honest
- Include what works well, so good patterns are kept
- Do not invent user data or test results; label assumptions
- Do not recommend dark patterns even when they raise a metric
- Apply accessibility as part of every heuristic, not as a separate afterthought

## What to report back

| Field | Content |
|-------|---------|
| Scope | users, tasks, screens, what was not seen |
| Top problems | three at most, with evidence and fix |
| Full findings | table by severity, heuristic and location |
| Strengths | what to keep |
| Next steps | fixes in priority order, and the test that will verify them |

## Related skills

- `hci-react-native`, `hci-flutter`, `hci-android-native`, `hci-ios-swiftui`: mobile implementation
- `hci-web-accessibility`: web and WCAG
- `hci-desktop-apps`, `hci-cli-ux`: desktop and command line
- `hci-rtl-localization`: right-to-left and multilingual UI
- `hci-microcopy`: wording of messages and labels
- `hci-usability-testing`: verify with real users
