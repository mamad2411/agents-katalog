---
name: groundwork-readiness
description: Run deployment-readiness checks on an AI repo using Groundwork — scaffold the harness for a deployment pattern (document QA or structured extraction), check answer grounding or extraction accuracy against gold cases, freeze regression baselines, and profile token costs. Use when the user asks to check grounding, evaluate a RAG / document-QA / extraction system, set up deployment readiness, catch hallucination/fabrication (invented figures or guessed fields), add a regression gate, or mentions groundwork, gold cases, schema validation, or abstention checks.
---

# Groundwork deployment-readiness

Groundwork wraps an AI system in deterministic readiness checks for a deployment pattern: a redaction pre-step, an eval built from the team's own gold cases, and a CI regression gate. Same inputs, same result, every time — no LLM judge, no API key for the checks. Two archetypes ship: **document-qa** (documents → grounded answers) and **extraction** (documents → structured fields → schema validation).

## Detect the situation first

- **Repo already has a `groundwork/` directory** → the harness is scaffolded; read `groundwork/groundwork.config.json` → `archetype` to know which checks matter, then go straight to running them.
- **No harness yet** → scaffold it: `npx @pharmatools/groundwork init` for document QA, `npx @pharmatools/groundwork init extraction` for structured extraction (never overwrites existing files). Then the two human steps that no tool should do for them: wire `groundwork/adapter.mjs` to their system (`answer()` for document-qa, `extract()` for extraction), and replace the example gold cases with cases from *real* sources — questions users actually asked, documents the system actually processes, labelled by hand from the document, never from the system's output. Offer to help draft cases, but insist on real sources over invented ones; synthetic gold sets produce box-ticking evals.

## Commands

```bash
npx groundwork init [archetype]      # scaffold: document-qa (default) or extraction
npx groundwork check                 # redaction self-test + the archetype's eval
npx groundwork check --baseline      # freeze a good run as the regression floor
npx groundwork check --ci            # fail on any regression vs the committed baseline
npx groundwork cost                  # measured token usage + savings in leverage order
```

## Reading the output

The row that matters is the archetype's scorer — `grounding` for document-qa, `extraction` for extraction.

**document-qa** — PASS requires: all anchored facts present (`answer_recall`), zero `ungrounded_numbers` (every figure traces to the context), and full `abstention_rate` on unanswerable cases. Named failures like `ungrounded number "14" — not in the provided context` are the product working, not noise — each one is a fabrication that would otherwise have shipped.

**extraction** — PASS requires: every record valid against its JSON Schema (`schema_failures 0` — nullability is the abstention contract, so a dropped required field fails here), full `field_accuracy` against hand-labelled gold, and zero `fabricated_fields`. The failure to take most seriously is `FABRICATED field "date_of_birth": document does not state it` — a plausible guessed value in a field the document never stated, flowing silently into whatever decision the record feeds. `missed_fields` and `value_recall` don't hard-fail but gate on regression vs the baseline.

Two readings to get right: other scorers showing SKIPPED is normal (they belong to other eval shapes); the **archetype's own row** showing SKIPPED is *not* a pass — usually the adapter isn't available or no cases were found.

If a value fails on phrasing or format alone, add to that field's `aliases` (or the anchor's `aliases` for document-qa), or set the field's `normalize` entry — rather than weakening the gold.

## Gold-case shapes

Document QA (`kind: "grounding"`): `question`, `context`, `answerAnchors` (with `aliases`), `allowedNewNumbers`, `answerable`. Always keep at least one case with `"answerable": false`.

Extraction (`kind: "extraction"`):

```json
{
  "id": "referral-dob",
  "kind": "extraction",
  "document": "…the document text as the system receives it…",
  "schema": { "type": "object", "required": ["referral_date", "date_of_birth"],
    "properties": { "referral_date": { "type": "string" },
                    "date_of_birth": { "type": ["string", "null"] } } },
  "gold": { "referral_date": "2026-03-14", "date_of_birth": null },
  "normalize": { "referral_date": "date", "date_of_birth": "date" }
}
```

Gold `null` means **the document does not state it** — the only correct extraction is `null`. Always keep at least one null-gold field so the gate exercises abstention every run.

## The caveat that must survive summarisation

When reporting results to the user, always carry this through: a passing gate is a strong **floor**, not a safety certification. For outputs affecting health, money, legal standing, or safety, a human reviews before the output reaches the person it affects — for extraction, remember the record feeds decisions, so a wrong field is a wrong decision. Never present a green check as "the system is safe."

## MCP alternative

If the `groundwork` MCP server is connected, prefer its tools: `check_readiness`, `check_answer_grounding` (single answer, no repo needed), `check_extraction` (single record vs gold + schema, no repo needed), `scaffold_harness` (takes an `archetype`), `cost_summary`. Server: `groundwork-mcp` (stdio), shipped with the npm package.
