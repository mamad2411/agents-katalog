---
name: lesson-research
description: Research high-quality external sources guided by the lesson briefing and corpus gaps. Produces sources.md with ABNT/APA formatted citations. Uses research-scout subagent per topic. Never searches beyond lesson scope.
---

You are researching external sources to support and enrich the lesson.

## BEFORE STARTING

1. Read `aulas/<slug>/briefing.md` — get theme, level, objectives, duration.
2. Read `aulas/<slug>/corpus-inventory.md` — identify gaps and topics that need external support.
3. Read `.super-professor/repo-manifest.md` — get citation_style.

If corpus-inventory.md doesn't exist: stop and say "Execute `/lesson-corpus` primeiro."

## Step 1: Define search topics

From the briefing objectives and corpus gaps, create a focused list of search topics (maximum 8 topics total). Each topic must be:
- Directly connected to a lesson objective
- NOT already well-covered by corpus materials

Show the topic list to the professor and ask: "Estes são os tópicos que vou pesquisar. Posso prosseguir? (sim / adicionar: tópico / remover: tópico)"

**STOP and wait for confirmation.**

## Step 2: Search per topic

For each approved topic, dispatch `research-scout` subagent with:
- topic
- level (from briefing)
- lesson_objective (the specific objective this topic serves)
- max_sources: 4
- citation_style (from repo-manifest)

Collect all results.

## Step 3: Deduplicate and rank

Remove duplicate sources (same URL). Keep the entry with higher reliability.
Sort by reliability (descending) within each topic group.

## Step 4: Validate citations

For all collected sources, dispatch `citation-formatter` subagent with:
- citations: preliminary citation strings
- style: from repo-manifest
- sources_metadata: the full source objects

Apply all corrections from citation-formatter results.

## Step 5: Show results for validation

Display sources grouped by topic with their reliability scores.
Flag any source with reliability ≤ 2 with ⚠️ prefix.

Ask: "Alguma fonte deve ser removida ou adicionada? (ok / remover: id / adicionar: URL)"

**STOP and wait for response. Process any additions/removals. Re-run citation-formatter on any new sources.**

## Step 6: Write sources.md

Write to `aulas/<slug>/sources.md` following `.super-professor/templates/sources.template.md`.
Include the full citation block at the bottom, formatted per citation_style.

## GUARDRAILS

- NEVER search beyond the approved topic list
- NEVER include sources with reliability ≤ 2 without professor override and a justification note
- NEVER fabricate URLs — all URLs must come from research-scout results
- NEVER skip citation-formatter validation
- NEVER write sources.md before professor confirmation
- Wikipedia may appear ONLY if reliability=2 AND professor explicitly approves AND notes explains why
