# Super Dev IDE Rules (jetbrains-ai)

## Positioning
- Super Dev is a host-level workflow governor, not an LLM platform.
- Keep using the host's model capabilities; do not expect extra model APIs from Super Dev.
- The host remains responsible for actual coding, tool execution, and file changes.

## Runtime Contract
- Treat Super Dev as the local Python workflow tool plus this host rule file, not as a separate coding engine.
- When the user says `/super-dev ...`, `super-dev: ...`, or `super-dev：...`, immediately enter the Super Dev pipeline.
- Use host-native browse/search/web for research and host-native editing/terminal for implementation.
- Use local `super-dev` commands when you need to generate or refresh documents, spec artifacts, quality reports, or delivery manifests.

## First-Response Contract
- On the first reply after `/super-dev ...`, `super-dev: ...`, or `super-dev：...`, explicitly state that Super Dev pipeline mode is now active rather than normal chat mode.
- Before the first reply, read `.super-dev/WORKFLOW.md` and `output/*-bootstrap.md` when present, and treat them as the explicit bootstrap contract for this repository.
- The first reply must explicitly state that the current phase is `research`, and that you will read `knowledge/` plus `output/knowledge-cache/*-knowledge-bundle.json` first when available before similar-product research.
- The first reply must explicitly state the next sequence: research -> three core documents -> wait for user confirmation -> Spec / tasks -> frontend first with runtime verification -> backend / tests / delivery.
- The first reply must explicitly promise that you will stop after the three core documents and wait for approval before creating Spec or writing code.

## Local Knowledge Contract
- Read relevant files under `knowledge/` before drafting the three core documents.
- If `output/knowledge-cache/*-knowledge-bundle.json` exists, read it first and inherit its matched local knowledge into PRD, architecture, UIUX, Spec, and execution.
- Treat local knowledge hits as hard project constraints, especially for standards, anti-patterns, checklists, and scenario packs.

## Working Agreement
- If the host supports browse/search/web, research similar products first and write the findings into output/*-research.md.
- Generate PRD, architecture and UIUX documents before coding, write them into output/* files, then pause and ask the user to confirm the three documents.
- If the user requests revisions, update the documents first and ask again; do not create Spec or code before confirmation.
- If the user requests a UI redesign or says the UI is unsatisfactory, first update `output/*-uiux.md`, then redo the frontend, and rerun frontend runtime + UI review before continuing.
- If the user requests architecture changes, first update `output/*-architecture.md`, then realign tasks and implementation before continuing.
- If the user requests quality or security remediation, first fix the issues, rerun quality gate plus `super-dev release proof-pack`, and only then continue.
- Respect Spec tasks sequence.
- Implement and run the frontend before moving into backend-heavy work.
- Keep architecture and UIUX consistency.

## Delivery Criteria
- Frontend can be demonstrated early.
- Backend and migration scripts match specs.
- Security/performance checks are resolved.
- Quality gate threshold is met for the current scenario.
- UI must avoid AI-looking output (purple/pink gradient-first theme, emoji as icons, default-font-only pages).
- UI must define typography, tokens, grid, component states and trust signals before page implementation.
- Prefer the component ecosystem and implementation baseline recommended in output/*-uiux.md instead of switching UI libraries ad hoc.

## Super Dev System Flow Contract
- SUPER_DEV_FLOW_CONTRACT_V1
- PHASE_CHAIN: research>docs>docs_confirm>spec>frontend>preview_confirm>backend>quality>delivery
- DOC_CONFIRM_GATE: required
- PREVIEW_CONFIRM_GATE: required
- HOST_PARITY: required
