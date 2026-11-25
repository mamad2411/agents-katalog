---
name: company-researcher
description: Research a company using public sources and summarize strategy plus product signals. Use when the user says "research company X", "company research", "LinkedIn and strategy for X", or when onboarding needs company context.
---

# Company Researcher

Research a company end-to-end and return a merged summary that combines strategy with product signals.

## Inputs

- Company name, exactly as given by the user
- Optional role or product focus to emphasize

## Workflow

1. Research company strategy:
   - Use the latest 10-K or annual report, earnings materials, investor relations pages, LinkedIn company overview, and recent press.
   - Focus on company overview, strategy, priorities, and named products or tiers.
2. Research product signals:
   - Look at job postings, LinkedIn Jobs, Reddit, and app-store signals when relevant.
   - Infer product areas and goals from job descriptions, and label those as inferred from job postings.
3. Merge the result:
   - Overview and strategy first.
   - Product features and goals second.
   - Source hints last.
4. Keep the summary factual and neutral.

## Output format

- 1-2 sentences on what the company does and where it sits in the market.
- 1-2 short paragraphs on strategy, current initiatives, and priorities.
- `Product features and goals:` bullet list.
- `Source hints:` short list of the sources used, including the fiscal year for any 10-K.

## Rules

- Prefer primary or near-primary sources.
- Treat job-posting inference as signal, not ground truth.
- If the company name is missing, ask for it before researching.
