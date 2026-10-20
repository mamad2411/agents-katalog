# AI Incident Postmortem Template

## Summary

**One-sentence:** ML-specific postmortem template covering trigger / blast radius / root-cause class / fix / eval-guard added — fills the gap left by DevOps templates which assume deterministic failures.

**One-paragraph:** Generic DORA-style postmortems list "5 whys" and a fix; they have no place for the ML-specific axes that drive AI incidents — was it model drift, prompt regression, schema change, judge change, retrieval failure, tool fault, hallucination class. This methodology produces one filled postmortem per incident with required sections (trigger, blast radius, root-cause class, fix, eval-guard added, follow-up actions). Output is a versioned report committed to the team's incident archive that downstream agents can search by root-cause class to spot patterns.

**Ефективно для:** Команд, які пишуть AI postmortem за template для звичайних сервісів — і пропускають «модель сама змінилась, eval set не зловив, бо там цього випадку немає»; ML-specific template ловить такі гепи у структуру, а не в narrative.

## Applies If (ALL must hold)

- AI/ML system had a production incident with user-visible impact.
- Incident is closed (live triage is done; this is the writeup phase).
- A named incident commander or eval owner exists.
- Trace data from before / during / after the incident is available.
- A follow-up review meeting is scheduled within 7 days.

## Skip If (ANY kills it)

- Pre-prod incident with no user impact — log only, no full postmortem.
- Deterministic-only failure (DB down, deploy script error) — use DevOps template instead.
- Incident is ongoing — finish triage first.
- Single-author research postmortem with no organisational impact.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Incident ID | string | Incident tracker |
| Time window | start + end ISO timestamps | Observability stack |
| User impact | qualitative + count | Customer ops |
| Pre/during/post traces | jsonl logs | Observability |
| Eval results before/after fix | jsonl | QA |
| Named incident commander | handle | Incident tracker |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/ai-incident-response-playbook/AGENTS.md` | Response runbook precedes the postmortem. |
| `geek/ai/ai-agents/agent-trajectory-eval-method/AGENTS.md` | Eval-guard added section references trajectory eval. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: ML-specific axes filled, eval-guard added, blameless, blast-radius quantified, eval-set updated | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the postmortem report | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: gather → root-cause-class → fix → eval-guard → publish | ~900 |
| `content/05-examples.xml` | medium | Worked example: postmortem for hallucination incident | ~1000 |
| `content/06-decision-tree.xml` | essential | Tree: ML failure? → which root-cause class? → which eval-guard? | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract_facts_from_traces` | haiku | Structured extraction. |
| `classify_root_cause` | sonnet | Domain judgment over 8 root-cause classes. |
| `draft_postmortem` | sonnet | Composition. |
| `review_blameless_language` | opus | High-stakes voice review when teams are at odds. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the postmortem report. |
| `templates/output.example.json` | Filled example. |
| `templates/postmortem.md.j2` | Markdown skeleton with the required ML-specific sections. |
| `templates/postmortem.md` | Markdown skeleton with the required ML-specific sections. Generated from `templates/postmortem.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the postmortem report. | After draft, before publication to incident archive. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[ai-incident-response-playbook]] — runbook used during live triage.
- peer: [[agent-trajectory-eval-method]] — eval guard referenced from "guard added" section.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is this an ML failure (not pure infra)? (2) which root-cause class fits (drift / prompt regression / schema change / judge change / retrieval failure / tool fault / hallucination / data poisoning)? (3) is an eval-guard added that would have caught it? Leaves point to the postmortem section template.
