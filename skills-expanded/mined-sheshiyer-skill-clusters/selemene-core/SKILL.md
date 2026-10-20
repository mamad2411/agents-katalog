---
name: selemene-core
description: "Shared reference for the Selemene cluster: the two report surfaces (deterministic Rust reports vs. narrative witness-pipeline readings), the @selemene/bridge CLI contract, the output manifest format, and non-prescriptive witnessing tone. USE WHEN deciding which Selemene surface to invoke or when routing between birth/compatibility/transit reports and solo/dyadic readings."
origin: project
cluster: selemene
version: 1.0.0
---

# Selemene Core

Cross-cutting rules for every Selemene skill.

## Two report surfaces

1. **Deterministic reports** — `crates/noesis-vedic-api/src/report_generator/`
   - `birth_report.rs`
   - `compatibility_report.rs`
   - `transit_report.rs`
   - Inputs: `BirthDetails`, `CompatibilityPair`, date ranges.
   - Output: `GeneratedReport` JSON with `sections` and `summary`.

2. **Narrative witness readings** — `packages/witness-pipeline/src/orchestrator/integrated.ts`
   - `IntegratedReadingOrchestrator`
   - Inputs: `ReportGenerationRequest` with `subjects`, `report_level`, `report_mode`.
   - Output: assembled markdown + source-pack (manifest + reading + reflection questions).

## Bridge CLI contract

The existing `@selemene/bridge` CLI at `bridges/cli/src/cli.ts` exposes:

- `init` — interactive wizard, writes `.selemenerc.json`
- `generate` — fetches Rust + TS OpenAPI specs and emits Claude/OpenAI/LangChain tool definitions
- `check` — health check
- `doctor` — diagnostics

The skill cluster reads `.selemenerc.json` for `rustUrl`, `tsUrl`, and `apiKey`. It does not regenerate tool definitions.

## Output manifest

Every report run must produce:

```json
{
  "report_type": "birth|compatibility|transit|witness",
  "created_at": "ISO-8601",
  "subject_count": 1,
  "engines_used": ["vedic"],
  "artifact_path": "/absolute/path/to/artifact",
  "witness_prompt": "..."
}
```

## Tone rule

All generated prompts and summaries are non-prescriptive mirrors. No medical, financial, or deterministic life advice. Questions only.
