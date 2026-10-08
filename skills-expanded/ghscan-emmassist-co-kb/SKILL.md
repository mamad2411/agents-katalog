---
name: kb-write
version: 2.1.0
description: "Safe trust-aware KB workflow for evidence reads, recall, proposals, remember, record, relate, annotate, validate, and cleanup without fragile inline JSON."
---

# KB Write

Use this when the task is to store, correct, structure, review, or clean up durable knowledge through the KB CLI.

## Fast Path

```bash
kb help
kb help runtime
kb help operator
kb help agent-improvement
kb schema search
kb schema query-relations
kb schema remember
kb schema record
kb schema relate
kb schema annotate
```

## Trust-Aware Read Before Write

Before mutating tenant/workspace knowledge, read the current state and its trust labels:

```bash
kb inspect
kb search --json '{"query":"billing owner","temporalFocus":"current"}'
kb query-relations --json '{"query":"owner of Stripe","mode":"graph-first-hybrid"}'
kb evidence --id vendor-stripe
kb recall --json '{"query":"billing owner","purpose":"pre-answer context"}'
kb debt
```

Use the `trust` envelopes, caveats, citations, supersession state, and evidence view to decide what is safe to write. `recall` is read-only; the agent/runtime decides if and when to inject it.

## Preferred Write Pattern

Prefer file-backed or stdin JSON:

```bash
printf '%s\n' '{"intent":"fact_update","summary":"..."}' | kb remember --json -
kb record --json @payload.json
kb relate --json @payload.json
kb annotate --json @payload.json
kb submit-proposal --json @proposal.json
```

Validate before mutating when the payload is non-trivial:

```bash
kb validate remember --json @payload.json
kb validate record --json @payload.json
kb validate relate --json @payload.json
kb validate annotate --json @payload.json
```

## Command Split

- Use `search` for factual retrieval; pass `temporalFocus` or `evidenceOnly` when currentness or raw evidence matters.
- Use `query-relations` for relation-shaped questions.
- Use `evidence --id` to inspect current-truth support, decisions, caveats, raw evidence, supersession, and open questions.
- Use `recall` only for caller-triggered read-only trust-aware context bundles.
- Use `remember` for facts, sources, corrections, and narrative/raw evidence capture.
- Use `record` for canonical structured entities.
- Use `relate` for explicit relation edges between existing entities.
- Use `annotate` for timeline or provenance updates on existing entities.
- Use `submit-proposal` when evidence suggests canonical truth should change but review is required.
- Use `delete --id ...` only to clean up bad test entities or accidental writes.

Treat `search`, `query-relations`, `evidence`, `recall`, `remember`, `submit-proposal`, `record`, `relate`, and `annotate` as the normal agent verbs. Do not use low-level event, draft, source-capture, relation-repair, review approval, proposal apply, or conflict commands unless you are explicitly doing KB repair or operator cleanup.

In a deployed runtime, `kb help runtime` is the compact contract for current workspace namespace, backend, canonicality, trust substrate version, and write discipline.

## Proposal Discipline

Raw notes and proposals are not canonical truth. When the agent lacks authority or evidence is ambiguous:

```bash
kb submit-proposal --json @proposal.json
kb proposals
kb get-proposal --id proposal_123
```

Only an explicit operator/review flow should approve and apply:

```bash
kb review-proposal --id proposal_123 --json '{"status":"approved","reviewer":"operator"}'
kb apply-proposal --id proposal_123 --applied-by operator
```

## Minimal Patterns

Reference or fact capture:

```bash
printf '%s\n' '{"intent":"source_capture","summary":"Captured a reference source for the vendor handbook.","source":{"title":"Vendor handbook","url":"https://example.com/vendor-handbook","kind":"research"}}' | kb remember --json -
```

Structured entity write:

```bash
kb record --json @payload.json
```

Timeline update:

```bash
printf '%s\n' '{"entity_ids":["company-acme"],"summary":"2026-05-09: Confirmed founder edge.","effective_at":"2026-05-09T00:00:00.000Z"}' | kb annotate --json -
```

Standalone explicit edge:

```bash
kb relate --json @relation.json
```

With a payload like:

```json
{
  "type": "founder_of",
  "fromId": "person-alex",
  "toId": "company-acme"
}
```

## Verification And Cleanup

- Run `schema <command>` if the shape is unclear.
- Run `validate <command>` before writes with nested arrays or batch files.
- Run `evidence --id ENTITY_ID` to verify source support and current-truth caveats.
- Run `links --id ENTITY_ID` or `traverse --id ENTITY_ID --explicit-only` to verify explicit edges.
- Run `debt` or `doctor` to inspect unsupported, stale, dangling, or review-needed state.
- Default to `relate` for explicit edges. Only use `record.relations[]` when you are already creating or rewriting the entity in the same payload.
- Do not use `annotate` to create relation edges.
- Use `record-batch` and `annotate-batch` for larger cleanups.
- If you truly need direct repair, review, or apply surfaces, discover them through `kb help operator` instead of treating them as part of the normal agent loop.

## Install

After installing `@emmassist-co/kb-cli`, prefer the package-local skill path:

```bash
npx skills add ./node_modules/@emmassist-co/kb-cli/skills/kb-write
```

If the package is not installed yet, the GitHub source path is available as a fallback:

```bash
npx skills add https://github.com/emmassist-co/kb/tree/main/packages/kb-cli/skills/kb-write
```
