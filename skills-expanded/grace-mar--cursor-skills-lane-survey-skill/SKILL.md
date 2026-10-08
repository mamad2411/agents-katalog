---
name: lane-survey
preferred_activation: survey
description: "Structured landscape scan before building a new work territory. Borrowed from the AI Innovation Radar's baseline-before-building discipline. Use when starting a new lane, evaluating an adjacent tool/framework, or when the operator says 'survey [lane]' or 'lane survey'. Template-portable."
---

# Lane Survey

**Preferred activation (operator):** say **`survey [lane-name]`** or **`lane survey`**.

Use this skill before creating a new work territory or when evaluating the landscape for an existing one. The goal is to avoid rebuilding what already exists and to enter a lane with grounded awareness of the space.

## When to use

- Starting a new `work-*` lane
- Evaluating whether a tool, framework, or approach already solves the problem
- Operator asks "what's out there for [domain]?" before committing to build

## Steps

1. **Read the lane's README or stated objective.** If `docs/skill-work/work-[lane]/README.md` exists, read it. Otherwise use the operator's stated goal.

2. **Web search for existing tools, frameworks, and approaches** in that domain. Use 3–5 targeted queries. Focus on:
   - Open-source tools and libraries
   - Commercial products or SaaS
   - Published frameworks, methodologies, or standards
   - Community projects or prior art

3. **For each significant finding, assess fit:**
   - Does it already solve the problem?
   - Does it partially solve it (useful reference but not drop-in)?
   - Does it address a different problem (ignore)?

4. **Classify each finding:**

   | Verdict | Meaning |
   |---------|---------|
   | **Adopt** | Use it directly — don't rebuild |
   | **Reference** | Learn from it, build your own version |
   | **Ignore** | Different problem or low quality |

5. **Write results** to `docs/skill-work/work-[lane]/SURVEY_[lane].md` with:
   - Landscape summary (2–3 sentences)
   - Key tools found (table: name, verdict, notes)
   - Gaps and opportunities (what nothing covers)
   - Recommendations (what to adopt, what to build)

6. **Proceed to the lane creation checklist** in [work-template.md](../../../docs/skill-work/work-template.md).

## Guardrails

- Survey findings are **WORK-layer only** — they do not enter the Record.
- The survey does not commit to adoption; the operator decides.
- If no web search is available, structure the operator's existing knowledge into the survey format instead.
- Keep the survey document short (aim for one page). This is a decision aid, not a research paper.

## Output format

```markdown
# Survey: work-[lane]

## Landscape
[2–3 sentence summary of what exists]

## Findings

| Tool / Approach | Verdict | Notes |
|-----------------|---------|-------|
| ...             | Adopt / Reference / Ignore | ... |

## Gaps
[What nothing covers — where you need to build]

## Recommendations
[Concrete next steps based on verdicts]
```

## Related files

- `docs/skill-work/work-template.md` — lane creation checklist (step 4 references this skill)
