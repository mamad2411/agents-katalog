---
name: interview-prep
description: "Trigger: interview prep, mock interview, preparar entrevista, simulacro, cultural fit, behavioral. Mood-aware personality strategy, per-JD playbook, interactive mock interview with scoring."
license: Apache-2.0
metadata:
  author: "giannipasquinelli"
  version: "1.1"
---

## Activation Contract

Use when the user prepares for an interview and wants: a mood-aware personality strategy, a per-JD playbook (behavioral/cultural-fit/soft-skill), or an interactive mock interview with live scoring. One mode or all three in sequence. Always read `assets/methodology.md` first.

## Hard Rules

- **Behavioral/cultural-fit/soft-skill focus only.** No leetcode, algorithms, or system design. Trait-keyed probes (Avature) and seniority-graded rubrics are a complementary lens, not a replacement.
- **Interviewology Four Styles only** (Charmer / Challenger / Examiner / Harmonizer). No DISC, MBTI, Big Five, or Enneagram.
- **Output language is absolute.** JD in English → ALL output in English. JD in Spanish → ALL output in Spanish. No JD → match the user's last message language (English fallback). Scores, feedback, questions, scorecards, everything follows this rule. Technical concept terms (STAR, Nugget First, Harmonizer, Charmer, etc.) stay in English regardless.
- **Interactive always.** Ask before producing. Use the `question` tool for explicit choices. Never dump a wall of text.
- **No fabrication, no salary content, no body-language coaching.** Cross-reference `job-application` for salary. Flag corpus gaps honestly.
- **Nugget First + STAR default** for every behavioral answer: nugget line → Situation → Task → Action ("I", not "we") → Result (quantified). Reuse `job-application` artifacts when available.

## Decision Gates

| Need | Mode |
|---|---|
| Strategy for today's interview | `personality-strategy` — mood-aware |
| Per-JD prep doc | `playbook` |
| Live rehearsal with scoring | `mock-interview` |
| Full sequence | Run strategy → playbook → mock in order |
| `job-application` ran this session | Reuse `company-research` + `adapt-resume` as playbook inputs |
| User is LATAM/Argentine | Optionally apply `interview-ready.md` cultural overlay in strategy coaching |

## Execution Steps

1. Read `assets/methodology.md`.
2. Identify the mode. If ambiguous, ask. Multiple modes per session OK.
3. Execute the mode following `assets/mode-procedures.md` exactly.
4. Present outputs inline. Report saved file paths.
5. Ask whether to run the next mode or stop.

## Output Contract

- Personality-aware, evidence-backed, structured. No cliches ("passionate", "apasionado").
- `personality-strategy`: inline only, no file.
- `playbook`: save `output/playbook_<company-slug>.md` + inline.
- `mock-interview`: inline by default; `output/mock-scorecard_<date>.md` only on request.
- Flag any gap you could not cover.

## References

- `assets/methodology.md` — canonical synthesis (read first)
- `assets/mode-procedures.md` — per-mode execution steps
- `assets/personality-cheatsheet.md` — Four Styles + mood overlay
- `assets/question-bank.md` — question taxonomy (families A–G)
- `assets/mock-rubric.md` — scoring grid + session flow
- `assets/external-links.md` — Notion/test links status
- `assets/pdfs/` — source corpus