---
name: career-tools
description: Career workflow modes for verified accomplishments, truthful resume tailoring, opportunity review, and interview prep. Use when capturing co-op or project impact, revising resumes from approved facts, evaluating a job or program posting, or preparing for a known interview. Never invent metrics or write confidential facts into public artifacts.
---

# Career Tools

Select exactly one mode. Do not silently chain modes.

## Modes

| Mode | Body | Outcome |
|------|------|---------|
| `accomplishment` | See below | Verified ACC record draft |
| `resume-tailor` | [resume-tailor.md](resume-tailor.md) | Versioned resume draft + claim audit (≤2 LLM passes; résumé style profile only; never documenter) |
| `opportunity-review` | [opportunity-review.md](opportunity-review.md) | APPLY / INVESTIGATE / DEFER |
| `interview-prep` | [interview-prep.md](interview-prep.md) | Prep plan + story bank (practice labeled) |

## Mode: accomplishment

Prompt sequence:

1. What was the problem, goal, or responsibility?
2. What did you personally do?
3. Which tools, methods, or technical concepts did you use?
4. What changed as a result?
5. What evidence supports the result?
6. What may be disclosed publicly?

Output must match `schemas/personal/accomplishment.schema.json`.

Steal Glean productivity patterns: quality over volume; did ≠ viewed; cite sources; group by themes.

Never invent percentages, savings, scale, or team size. Persist only via `personal-store accomplishment append --confirm` after user review.

## Claim tags

`VERIFIED` | `USER_CONFIRMED` | `UNKNOWN` | `UNSUPPORTED`

Freshness: &lt;6 mo / 6–12 / 12+.

## Store

Private root: `%USERPROFILE%\.config\personal-career\` (or `PERSONAL_CAREER_ROOT`). Browser never writes.
