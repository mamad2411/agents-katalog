---
name: heuristic-evaluation
description: Run a systematic expert review of an interface against Nielsen's 10 usability heuristics, documenting each issue with heuristic, location, evidence and a 0-4 severity rating, then prioritising findings. Use when you need findings without recruiting participants.
license: MIT license
category: docs
metadata: {"version": "1.0", "skill-author": "MC Dean (designer-skills)"}
---

# Heuristic Evaluation

Find usability problems before user testing, with findings that are documented and ranked rather than
opinionated. 中文触发：启发式评估、专家走查、可用性问题清单、严重度分级。

## Nielsen's 10 heuristics
1. **Visibility of system status** — users know what is happening
2. **Match between system and real world** — speak the users' language
3. **User control and freedom** — easy undo and exit
4. **Consistency and standards** — follow platform and product conventions
5. **Error prevention** — stop problems before they occur
6. **Recognition over recall** — make options visible
7. **Flexibility and efficiency of use** — shortcuts for experts
8. **Aesthetic and minimalist design** — no irrelevant information
9. **Help users recognise, diagnose and recover from errors**
10. **Help and documentation** — provide assistance where needed

## Process
1. Define scope: which screens and flows are evaluated
2. Walk through as a **new** user
3. Walk through as an **experienced** user
4. Walk through each task flow end to end
5. Document every issue found
6. Rate severity
7. Compile, de-duplicate and prioritise

## Issue record format

| Field | Content |
|---|---|
| Heuristic | which of the 10 is violated (1–10) |
| Description | what is wrong, in one sentence |
| Location | screen, component, step |
| Evidence | screenshot or concrete reproduction steps |
| Severity | 0–4 (below) |
| Recommendation | the specific fix |

## Severity scale
- **0** — not a usability problem
- **1** — cosmetic only
- **2** — minor problem
- **3** — major problem, important to fix
- **4** — catastrophe, must fix before release

Sort findings by severity, then by how often the flow is used.

## Working rules
- 3–5 evaluators find substantially more issues than one; evaluate independently before comparing
- Judge against real user tasks, not edge cases
- Do not stop at problems — every entry carries a recommendation
- Combine with real user testing for the full picture
