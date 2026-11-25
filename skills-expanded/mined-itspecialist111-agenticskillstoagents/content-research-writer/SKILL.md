# content/research-writer — skill payload

> Machine-readable contract: [`../content-research-writer.manifest.json`](../content-research-writer.manifest.json).

## What this skill does

Drafts a long-form research article (1500-3000 words) from a topic
brief. Workflow:

1. Gathers sources via web search.
2. Builds an outline from the strongest sources.
3. Drafts each section with inline citations.
4. Returns Markdown plus a structured bibliography of every cited URL.

Expects a human reviewer at publish time — the bibliography is the
audit trail.

## When to use it

- A content team needs a credible first-draft article on a topic where
  the source material exists publicly.
- A marketing team wants a thought-leadership piece anchored in real
  sources, not vibes.

## When **not** to use it

- The topic requires proprietary data or expert interview — use a human.
- The output must be SEO-optimised for a specific ranking goal — pair
  this skill with a separate SEO-pass step; this skill optimises for
  *credibility*, not rank.

## Determinism and risk

Determinism: **low** — narrative output varies. Risk: **medium** —
hallucination risk mitigated by the cited bibliography that lets a
reviewer verify every claim.

## How it composes

Often paired with `comms/meeting-insights` (turn meeting notes into a
blog post draft) or `content/research-writer` → `office/docx-toolkit`
(deliver as a Word doc).
