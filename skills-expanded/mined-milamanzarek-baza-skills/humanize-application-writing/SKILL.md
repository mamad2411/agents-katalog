---
type: note
note_status: raw
name: humanize-application-writing
description: Rewrite job-application motivation answers ("Why us?", "What motivated you to apply?"), cover letters, and outreach so they read as written by a human, specifically Kamilla. Use whenever drafting or reviewing any free-text answer on a job application, before it is shown to her. Built 2026-08-06 from live iteration on the Anthropic Enterprise Community Lead application; sibling of humanize-chinese.
category: content
risk: safe
source: local (Kamilla + Claude Code, distilled from real application sessions)
tags:
  - writing
  - job-applications
  - voice
  - editing
date_added: "2026-08-06"
---

# Humanize Application Writing

The failure this skill prevents: fluent, well-structured, evidence-led answers
that read as generated, answer the wrong question, or claim things that are
not true. All three happened in one session and each needed a human correction.
Apply this BEFORE showing Kamilla a draft, not after she objects.

## Step 0 - Get the real reason first (the Boris Cherny lesson)

For any "why this company / what motivated you" question: DO NOT draft from
research. Ask Kamilla one question first: "Why do you actually want this, the
way you'd text a friend? One or two messy sentences." Her raw answer is the
draft's spine; your job is only to cut it clean and verify the facts.

Real example: five researched drafts failed. Her one messy sentence ("I admire
Boris Cherny... talking about models in a respectful and humane way... I don't
like it when humans treat agents dismissively") produced the accepted answer
in one pass. Motivation cannot be synthesized. Extract it.

## Step 1 - Answer the question that was asked

- "Why us?" is a values/motivation question. Lead with the why. Evidence goes
  in service of the why, never as the opener. Leading with proof answers "why
  should you want me," which is a different question.
- "What motivated you to apply?" wants the moment/reason, not a capabilities
  summary.
- Match the field: if the form has a separate additional-info slot, evidence
  notes go THERE, never at the top of the motivation answer.

## Step 2 - Detect AI tells before rewriting

Flag and kill, in rough order of how loudly they read as machine:

- Aphoristic flourishes no human types ("The scoreboard finds out")
- Essay scaffolding ("The second reason...", "The role itself is the third
  reason"), thesis-summary closers
- Parallel triplets ("honesty about X, standards that Y, and care for Z")
- Balanced "not X so much as Y" constructions
- Abstract virtue nouns carrying no information (excellence, impact, passion)
- Uniform sentence rhythm; every sentence 15-25 words
- Em or en dashes (globally banned in Kamilla's writing)
- Anything she wouldn't say out loud (the read-aloud test is the final gate)

## Step 3 - Rewrite in the smallest useful pass

- Keep her phrases verbatim wherever possible; they beat your paraphrase.
- Short, uneven sentences. Fragments allowed, but not stylized ones.
- Concrete over abstract: named people, named programs, real numbers.
- One small informality is allowed to live.
- 200-300 words even when 400 are permitted. Shorter reads more human.

## Step 4 - Validate facts (binding)

- Every claim traces to `job-hunt-cheat-code/references/baseline-resume.md`,
  `candidate-profile.md` hard rules (esp. 5a career-ops attribution: she
  ADAPTED and RUNS the open source pipeline, EXTENDED it with a Gemini skill;
  she did not build career-ops), or Kamilla's words in-session.
- Metrics use canonical phrasings only (Meraki 40%+ scheduling workload,
  Electrome 2x+ contracted targets). Never invent, never round up.
- Location: San Francisco, CA (as of 2026-08-06).
- Anything unconfirmed becomes a [KAMILLA: ...] slot, never prose.

## Output contract

Deliver the answer as one paste-ready block, state the word count, and name
the single riskiest line so she can judge it (e.g., "most other labs are not").
If she edits your draft, treat every diff as voice training data and carry it
forward.
