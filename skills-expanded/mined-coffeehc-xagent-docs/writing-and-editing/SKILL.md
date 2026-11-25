---
name: writing-and-editing
description: Use when creating, rewriting, editing, polishing, restructuring, shortening, expanding, adapting tone, translating style, or drafting human communication from user-provided facts. Includes emails, messages, replies, announcements, proposals, outlines, explanations, and general business writing. Prefer this Skill when the central work is prose quality, reader fit, clarity, tone, or meaning preservation. Do not use for formal official documents, research synthesis, solution briefs, meeting recaps, or unsupported factual invention.
meta:
  version: 1
  display_name: 写作与编辑
  source: jezweb/claude-skills writing commands; claude-office-skills internal-comms
  license: MIT
---

# Writing And Editing

## Purpose

Create or improve written content while preserving the user's intended meaning, facts, constraints, and audience needs. This Skill owns the writing process: intent capture, reader fit, structure, tone, revision discipline, and fact safety.

This Skill adapts writing and business-communication practices from reviewed open-source Skills. It does not bind to email, Slack, Office, publishing, or document-export tools.

## Use When

Use for:

- writing, rewriting, editing, polishing, simplifying, expanding, shortening, or restructuring text;
- drafting emails, chat messages, replies, announcements, requests, updates, feedback, or customer-facing notes;
- turning rough notes into clear prose;
- adapting tone, style, region, audience, formality, or length;
- reviewing writing for clarity, completeness, tone, reader fit, unsupported claims, or sensitive wording.

Prefer `official-document-drafting` for Chinese official/formal institutional material. Prefer `internal-comms` for structured internal announcements, newsletters, FAQs, or status communication. Prefer `solution-brief` when the prose is a decision-alignment brief with trade-offs, metrics, risks, and open questions.
Prefer `blog-writing-workflow` when the user is planning, drafting, editing, or packaging a blog post, article, technical blog, thought leadership post, or newsletter-style article.

## Do Not Use When

Do not use for:

- external research or source-backed evidence synthesis;
- document reading as the main task before writing; use `document-understanding` first;
- formal official documents, legal approvals, medical/financial advice, or binding commitments;
- data computation or chart/report generation;
- sending, publishing, scheduling, approving, or exporting the message;
- inventing facts, customer commitments, metrics, quotes, owners, dates, approvals, or policy positions.
- AI detector evasion, "humanizer" rewrites, or promises that text will beat AI detectors.

## Material Gate

Before writing, identify:

- writing mode: create, edit, rewrite, critique, shorten, expand, tone shift, or communication draft;
- audience, channel, purpose, desired outcome, and reader relationship;
- facts that must be preserved, claims that need support, and information that is missing;
- tone constraints: direct, polite, formal, plain, persuasive, apologetic, neutral, executive, technical, customer-facing, or internal;
- length, language, style, and sensitivity constraints.

If the task asks for factual content not present in the conversation, either ask for source material or mark it as missing. Do not research unless the user requests research.

## Workflow

1. Classify the writing task and audience.
2. Extract the factual payload from the user's material: names, dates, numbers, decisions, asks, constraints, commitments, and caveats.
3. Decide the edit depth using `references/writing-process.md`: light polish, structural edit, rewrite, critique, or communication draft.
4. Preserve user meaning unless the user explicitly asks to change it.
5. Choose a structure that serves the reader: context first, answer first, ask first, narrative, argument, checklist, or concise message.
6. Remove ambiguity, filler, duplication, unsupported certainty, and hidden assumptions.
7. Align tone with audience and channel without leaking internal reasoning or tool workflow.
8. For communication drafts, make the ask, decision, or next step explicit.
9. Check for unsupported commitments, sensitive information, and factual drift.
10. Deliver the requested text or edit notes in the user's preferred language and level of detail.

## Checks

- Meaning and required facts are preserved.
- The reader can tell what happened, what matters, and what is needed.
- Tone matches the audience and relationship.
- The text does not invent facts, metrics, approval, urgency, or authority.
- Sensitive or internal-only details are not exposed accidentally.
- The result is neither over-written nor under-specified for the channel.
- Rewrites improve clarity and voice without laundering unsupported claims into confident language.

## Outputs

Return the writing help the task needs: final text, rewrite, edit notes, critique, alternatives, short/long variants, tone options, or communication draft. Do not force a fixed writing template.

## Boundary

Skill owns writing workflow, editing depth, tone adaptation, reader fit, meaning preservation, communication clarity, and fact-safety checks.

It does not own XAgent tool schemas, file permissions, document export, message sending, publication, approvals, legal/compliance authority, external research, or final factual authority for unverified claims. It must not run shell, Python, Node, npm, curl, MCP, email, Slack, Teams, CMS, CRM, Office, publish, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/writing-process.md`: edit-depth selection, tone rules, communication workflow, and review checks.
- `LICENSE`: source and license notice.
