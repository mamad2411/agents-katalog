---
name: eda-paper-fetch
description: Fetch primary-source paper metadata when evidence is missing or weak for EDA/model/flow claims. Use for requests like building reproducible paper candidate lists, generating user-download queues, and recording citation metadata for local validation.
---

# EDA Paper Fetch

## Overview

Use this skill to produce evidence-backed paper sets, not ad-hoc links. Always output a local manifest and evidence note.

## Workflow

1. Define scope and constraints.
- topic and claim to support/refute,
- date window and venue preference,
- target count (default: 5-15 papers).

2. Search primary sources first.
- Load `references/source-priority.md`.
- Prefer official sources (publisher/arXiv/OpenReview/DOI landing pages).
- Do not claim availability without opening source pages.

3. Triage and score.
- Keep only papers relevant to the exact claim.
- Record reason for inclusion/exclusion using `references/triage-template.md`.

4. Generate user-download queue instead of auto-download.
- Write `docs/papers/queues/<topic_slug>.download_queue.tsv`.
- Include columns: `paper_id`, `title`, `url`, `doi_or_arxiv`, `preferred_source`, `access_type(open/paywalled)`.
- User manually downloads PDFs to `docs/papers/pdf/` using filename:
  - `<year>_<first_author>_<short_title>.pdf`.

5. Produce manifest and summary.
- Write `docs/papers/manifests/<topic_slug>.paper_manifest.tsv`.
- Write `docs/papers/manifests/<topic_slug>.paper_manifest.md`.
- Include fields: `paper_id`, `title`, `authors`, `venue`, `year`, `url`, `doi_or_arxiv`, `local_pdf_path`, `relevance_note`, `status(todo/downloaded/summarized)`.

## Output Contract

Always return:
1. local manifest path,
2. local download queue path,
3. unresolved paywalled items,
4. one-paragraph evidence fitness assessment.

## References

Read only when needed:
1. `references/source-priority.md`
2. `references/triage-template.md`
