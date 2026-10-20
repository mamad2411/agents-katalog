---
name: yeisme-auctra-cli-runtime
description: Use when changing, testing, reviewing, documenting, or designing the Auctra CLI-first text creation product runtime under cli/auctra, including product workflows, CLI behavior, approved Service API projections, app-service boundaries, screenplay corpus intelligence, material/brief/review/export contracts, runtime providers, run evidence, and independent-client or Scaena handoffs.
---

# Yeisme Auctra CLI Runtime

Use this skill for `cli/auctra`, the local-first text creation product engine whose owned interactive surface is CLI and whose stable projections may support approved independent clients.

## Product Identity Lock

Auctra is a specialized text creation product engine, not a generic agent and not a provider router. CLI remains its owned direct user interface; product PRDs, workflow design, and client contract gaps are still in scope even when frontend implementation belongs to a separate approved client.

```text
External agent / script -> Auctra CLI or approved typed API -> shared app service -> evidence -> review -> version/export
```

Auctra owns materials, briefs, text runs, review items, versions, export manifests, and redaction. Codex, Claude, Cohors, and Yeisme subagents are callers of `auctra`; they are not embedded providers inside Auctra.

## Boundary

- CLI entrypoint: `cli/auctra/cmd/auctra`.
- Command parsing and mode wiring: `internal/cli` and `internal/cli/command`.
- Shared output projections/renderers: `internal/presenter`; CLI output changes must follow `ai-native-cli-output-contract`.
- App workflows: `internal/app`.
- Project identity and `.auctra/project.yaml`: `internal/project`.
- Text units, briefs, generators, templates, versions, and exports: `internal/content` and `internal/manuscript`.
- Materials and links: `internal/material`.
- Corpus import, segmentation, evidence, recipe, project link, and screenplay overlays: `internal/corpus`.
- Review queue, decisions, and adoption: `internal/review`.
- Approved operation catalog and client-safe projections: `internal/operation`; do not create network-only business logic.
- Runtime provider contract and runtime selection: `internal/runtime`.
- Cohors fixture/subprocess integration only: `internal/cohors`; do not modify `cli/cohors`.
- Persistent index: `internal/store` with SQLite/GORM.

## Non-Negotiable Invariants

- **Human review first:** generation creates pending review items. Only `review accept` or `review partial` may create accepted versions. No `--auto-accept`, unattended overwrite, or publish bypass.
- **Shared text engine:** novel chapters, Xiaohongshu notes, WeChat articles, short-video scripts, and screenplay scenes use one text unit / brief / run evidence / review / export core. Do not create independent per-kind generator stacks.
- **Local-first evidence:** project state, materials, drafts, versions, run receipts, review decisions, and export manifests stay under `.auctra/` by default.
- **Direct UI ownership:** CLI remains Auctra's direct interface. A versioned Service API is allowed only when an approved OpenSpec projects the same application operations to an independent client; Auctra still owns no Web UI, business BFF, scraper, platform login, provider SDK, or auto-publisher.
- **Structured asset boundary:** agents may write user prose files, but must mutate `.auctra/project.yaml`, `.auctra/profile/**`, `.auctra/runs/**`, `.auctra/review/**`, `.auctra/exports/**`, and SQLite rows only through Auctra commands or app services.
- **Accepted-only production handoff:** Auctra exports canonical accepted screenplay semantics and source provenance. It never manufactures Scaena `ShotIntent`, `ShotGenerationSpec`, generation bundles, provider jobs, or downstream acceptance.

## Runtime Provider Contract

Provider IDs are closed for current work: `pi`, `omp`, `cohors`, and `fixture`. Adding a provider or changing provider semantics requires an Auctra OpenSpec change.

Runtime providers are projection adapters, not model SDK integrations:

- `pi` is the default real runtime priority.
- `omp` is explicit through `--runtime omp` or `AUCTRA_RUNTIME=omp`.
- `fixture` is the only deterministic offline test/demo path.
- `cohors` remains planned/unavailable until a separate Auctra change makes it real.

Provider implementations must consume a versioned text projection such as `auctra.provider.text_projection.v1`. Do not import provider SDKs, save provider secrets, parse human-readable provider output, or silently fall back to fixture while claiming a requested provider succeeded.

Run evidence must keep redaction enabled. Secrets, auth headers, raw prompts, hidden prompts, provider payloads, private tool arguments, and chain-of-thought must not appear in CLI output, receipts, fixtures, golden files, or docs.

## Screenplay Corpus Intelligence

For multi-sample Chinese screenplay, short-drama, DOCX/Markdown conversion, symbol restoration, Pattern Lens, recipe, or blind-eval work, load `$auctra-screenplay-pattern-research`.

Preserve these invariants:

- Source Markdown stays immutable; parsing, repair, symbol display, and review live in additive overlays.
- `△/▲` and other source markers are preserved. Studio icons are presentation only and always have text/accessibility labels.
- Calibration, holdout, and exploratory access is enforced by the application policy, not by a hidden UI button. Holdout cannot enter parser, runtime, recipe, cache, embedding, or generation tuning.
- `short_drama_screenplay`, `screenplay-zh-short-drama-v1`, and `dramatic-pattern-v1` are additive contracts. Do not repurpose `novel`, `chapter`, `satisfaction-v1`, or stable Fountain enum values.
- Pattern claims require accepted source spans, positive/negative evidence, permission, split provenance, and review. Recipe constraints must be abstract and cannot carry sample dialogue, names, or unique plot expressions.
- Corpus, pattern, or recipe refs cannot become Scaena inputs. Only a human-accepted Auctra screenplay can produce the production handoff.

If the installed CLI/help lacks the approved screenplay audit/profile/review/eval operation, return `capability_missing` and use `openspec/changes/auctra-screenplay-corpus-intelligence-v1/` as the implementation owner. Do not substitute legacy chapter or satisfaction analysis.

## Agent-Facing CLI Contract

Agent workflows must use real commands with `--json` or `--agent`:

```bash
auctra material add --kind note --title "咖啡店观察" --from ./notes/cafe.md --json
auctra content new xhs_note --title "这家咖啡店为什么适合一个人待一下午" --platform xiaohongshu --json
auctra content generate note_001 --runtime pi --agent
auctra review --status pending --json
auctra content export note_001 --format markdown --to ./dist --json
```

`--json` must emit one envelope. `--agent` must emit stable `key=value` facts. Diagnostics go to stderr. Tests must parse machine output directly, never default human summaries.

## Scaena Production Handoff Contract

Use the production handoff commands only after canonical screenplay review is complete:

```bash
auctra production handoff inspect --project <path> --target scaena --json
auctra production handoff export --project <path> --target scaena --to <file> --json
auctra production handoff diff --project <path> --from <handoff-id> --json
auctra production handoff apply-receipt --project <path> --from <receipt-file> --json
```

`auctra.production_handoff.v1` is the additive producer contract. Preserve:

- `schema`, `handoff_id`, stable `source_project_ref`, `source_revision`, and canonical `canon_digest`;
- accepted units and scenes only; draft/candidate/rejected text must not enter the package;
- deterministic scene order and stable scene/action/dialogue span refs;
- scene heading semantics (`int_ext`, location, `time_of_day`), action spans, dialogue spans, continuity facts, constraints, accepted visual refs, review summary, and evidence refs;
- digest stability across timestamps and filesystem locations when accepted creative state is unchanged.

Readiness is fail closed. Pending review, blocking findings, unresolved refs, missing accepted versions, or stale source revision block export. `apply-receipt` validates the handoff id and digest and must not persist partial mappings on mismatch.

Scaena is the consumer and execution owner. Auctra must not call Scaena, mutate `.scaena`, choose a video model, or infer shot-generation parameters. A downstream import receipt may map Auctra refs to Scaena refs, but it does not retroactively change Auctra acceptance.

## Language Rule

Local project docs and OpenSpec artifacts default to Chinese. CLI help, errors, command run summaries, logs, and `--explain` reports default to English. Chinese remains valid product content for Xiaohongshu, WeChat, Douyin, manuscripts, source notes, fixtures, and quoted material.

## OpenSpec And Docs Ownership

Auctra implementation plans live under `cli/auctra/openspec/changes/auctra-<slug>/` or an existing active change such as `agent-cli-redesign`. Product, operator, runtime, command, and module docs live under `cli/auctra/docs/**`. Do not create root doc mirrors for Auctra implementation state.

## Validation

For output/review/runtime contract changes:

```bash
cd cli/auctra
go test -tags=nomsgpack ./internal/cli ./internal/cli/command ./internal/app ./internal/runtime
openspec validate agent-cli-redesign --strict
```

For the Scaena production handoff contract:

```bash
cd cli/auctra
go test -tags=nomsgpack ./internal/content ./internal/productionhandoff ./internal/app -count=1
openspec validate auctra-shot-production-handoff-v1 --strict
```

For screenplay corpus intelligence design or implementation:

```bash
cd cli/auctra
go test ./internal/corpus ./internal/content ./internal/review ./internal/operation -count=1
openspec validate auctra-screenplay-corpus-intelligence-v1 --strict
```

For broader code or command behavior changes:

```bash
cd cli/auctra
go test -tags=nomsgpack ./...
task build
```

If runtime, evidence, fixture demo, or main creation flows change, also run:

```bash
cd cli/auctra
task fixture-demo
task test:integration
```
