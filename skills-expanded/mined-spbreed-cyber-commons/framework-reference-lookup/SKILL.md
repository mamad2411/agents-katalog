---
name: framework-reference-lookup
description: >-
  Look up which control vocabularies a lesson maps to, and which lessons address
  a given control, from the commons' own mapping file. Use when answering "where
  is this framework covered", when preparing an audit response, or when checking
  a framework's coverage for gaps.
allowed-tools: Read, Grep, Glob
---

# Two directions, and the second one is the one people actually ask for

Nobody asks what a lesson maps to. They ask **"show me where human oversight is
addressed"**, and the answer has to be a list of things that exist rather than a
paragraph asserting coverage.

This reads `curriculum/frameworks.json` — the same file every lesson page is
labelled from — so a reference table and a lesson's chips cannot disagree.

## The four vocabularies

| framework | what it is | when it is the right lens |
|---|---|---|
| [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) | LLM01–LLM10, application-level risks | reviewing a feature that calls a model |
| [OWASP Agentic AI Top 10](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) | T1–T15, threats specific to agents | the system plans and calls tools |
| [MITRE ATLAS](https://atlas.mitre.org/) | adversary tactics against AI systems | describing what an attacker did |
| [NIST AI RMF 1.0](https://airc.nist.gov/AI_RMF_Knowledge_Base/AI_RMF) | GOVERN, MAP, MEASURE, MANAGE | organising a programme, not a bug |
| [EU AI Act](https://artificialintelligenceact.eu/) | Regulation 2024/1689, by article | an obligation, with a deadline |

The first three describe *what can go wrong*. NIST describes *how you organise
to find out*. The EU AI Act describes *what you must be able to show*. A control
usually needs one of each, which is why lessons carry several.

## When to use this

Preparing an audit or assurance response, checking coverage before claiming it,
and picking the right vocabulary for a finding — an ATLAS tactic in a risk
register and a NIST function in an incident write-up are both category errors.

## Step-by-step

**1 — Decide which direction you need.** Lesson → controls for a reader;
control → lessons for an auditor.

**2 — Use the vocabulary the audience uses.** Do not translate a regulator's
article into a threat id for them.

**3 — Read the coverage counts as a gap finder.** A control with one lesson is
thin; one with none is a hole.

**4 — Follow the link before quoting the label.** The labels are indicative
mappings, not a certification.

## Example

**Output** — from a real run:

```
   Art. 14  Human oversight                                      17 lessons
   B1.2    OWASP LLM01 · OWASP T6 · ATLAS AML.T0051 · ATLAS Initial Access · NIST MAP · EUAI Art. 15
```

## Output contract

```json
{
  "frameworks": [{"name": "str", "url": "str", "size": "str"}],
  "euai_articles": [{"article": "str", "title": "str", "lessons": 0}],
  "coverage": {"nist": {"GOVERN": 0}, "owasp": {"LLM01": 0}},
  "lookup": {"by_lesson": {"B1.2": ["str"]}, "by_control": {"Art. 14": ["str"]}}
}
```

## Common edge cases

- **A lesson carries no labels.** A0 is setup and maps to no control on
  purpose; that is declared, not missing.
- **One article dominates.** Art. 15 covers accuracy, robustness *and*
  cybersecurity, so it is broad by construction.
- **A label with one lesson.** Thin coverage, not necessarily wrong — check
  whether the control deserves more.

## Failure modes

- **Quoting a mapping as compliance.** These are indicative. Studying a lesson
  discharges no obligation.
- **Maintaining a second copy of the tables.** They will diverge; read the one
  file.
- **Assuming a framework's ids are stable.** OWASP renumbered the LLM Top 10
  slugs between editions, which is why the links are fetched in CI.
