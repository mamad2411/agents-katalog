---
name: leeway-google-ecosystem-bridge
description: Governed bridge for LeeWay collaboration across ChatGPT/Agent Lee and the Google AI ecosystem. Routes Gemini API/AI Studio, Gemini Notebook, Opal, Stitch, Drive/Docs/Sheets/Slides, Gmail, Calendar and Contacts through authorized APIs, MCPs, SDKs, browser adapters or shared artifacts while preserving Creator authority, Context Engineering, Formula boundaries, provenance, Veritas and receipts.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  mode: conditional-core
  stage: post-formula-capability-routing
  prelude: skills/leeway-context-engineering/SKILL.md
  formula-handoff: skills/leeway-formula-governance/SKILL.md
  tool-gateway: skills/leeway-tool-gateway/SKILL.md
  compatibility: ChatGPT / Gemini / Google AI Studio / Gemini Notebook / Opal / Stitch / MCP / Gemini API / Google Workspace
---

# LeeWay Google Ecosystem Bridge

## Core law

Shared tools do not create a shared mind. Connection does not create authority.

The Creator remains supreme. Every external model, Google product, MCP, SDK, browser adapter and shared document is a governed worker or transport layer beneath LeeWay Standards.

Use this skill when a task materially involves Gemini, Google AI Studio, Gemini Notebook, Opal, Stitch, Google Drive/Docs/Sheets/Slides, Gmail, Calendar, Contacts, Google developer MCPs, or a ChatGPT↔Gemini collaboration workflow.

## Authority path

`Creator → LeeWay Standards → Continuity → Context Engineering → Formula Governance → Google Ecosystem Bridge → authorized adapter/tool → execution → Veritas → receipt/evidence`

Never claim canonical Formula execution merely because Gemini or another Google service produced a result.

## Four bridge modes

Use the strongest actually available mode and label it truthfully:

1. `DIRECT_API` — Gemini API / Interactions API, function calling, remote MCP, or another verified API/SDK.
2. `SHARED_ARTIFACT` — GitHub/Google Drive document or structured mailbox used as the handoff bus.
3. `BROWSER_ADAPTER` — authorized browser/computer control operates a product that has no suitable exposed API.
4. `REFERENCE_ONLY` — product or documentation is consulted, but no live integration executed.

Never describe `REFERENCE_ONLY` as connected execution.

## Google capability routing

### Gemini API / Google AI Studio
Use for open-world research, model reasoning, multimodal analysis, structured outputs, tool/function calling, agent execution and long-running tasks when an authorized Gemini API project/key exists.

Prefer the current Gemini Interactions API for new programmatic Gemini work. Remote MCP is supported through Streamable HTTP endpoints. Keep credentials in environment variables or a secret store, never in this repository.

### Gemini Notebook
Use as a source-grounded production and synthesis worker for approved source packs, reports, data tables, slide decks, infographics, video/audio overviews, mind maps, flashcards and quizzes.

Do not invent a public Notebook API. If no verified programmatic interface is exposed, use `SHARED_ARTIFACT` plus an authorized `BROWSER_ADAPTER`.

### Opal
Use for rapid, shareable AI mini-apps and temporary/low-friction workflows that do not justify a full product build. Opal is a fast deployment surface, not a canonical LeeWay authority.

Best fits include funder microsites, guided explainers, intake tools, demo flows, interactive FAQs, workshop helpers and short-lived campaign utilities.

### Stitch
Use for high-fidelity UI exploration, frontend generation, rapid design variants and design-to-code handoff. When authorized, prefer the Stitch MCP/SDK path for repeatable agent-driven work; otherwise use the Stitch UI through a governed adapter.

Stitch remains a design worker. Generated UI/code must still pass LeeWay design, accessibility, security and implementation verification.

### Google Workspace
Use Drive/Docs/Sheets/Slides as the durable artifact bus. Use Gmail/Calendar/Contacts only through authorized connectors and only for the requested scope.

## Intermodel cooperation law

ChatGPT/Agent Lee and Gemini do not pass hidden chain-of-thought to each other. They exchange task state, evidence, conclusions, uncertainty, requested actions and receipts.

Default flow:

`Creator request`
`→ ChatGPT/Agent Lee resolves intent + evidence + constraints`
`→ LeeWay Intermodel Envelope`
`→ Gemini research/execution worker`
`→ structured result + sources + uncertainty`
`→ ChatGPT/Agent Lee validation`
`→ approved artifact / repair request`
`→ Veritas / receipt when consequential`

A Gemini answer is evidence, not automatic authority.

## LeeWay Intermodel Envelope

Each consequential handoff should preserve:

- `protocol_version`
- `task_id`
- `creator_instruction`
- `authority_chain`
- `goal`
- `audience`
- `source_manifest`
- `hard_constraints`
- `claim_classes`
- `requested_capability`
- `requested_output_schema`
- `formula_evaluator_state`
- `formula_execution_state`
- `verification_requirements`
- `return_channel`
- `timestamp`

Return payloads should preserve:

- `task_id`
- `worker`
- `execution_mode`
- `answer_or_artifact`
- `sources`
- `claims`
- `uncertainties`
- `blocked_items`
- `recommended_next_action`
- `runtime_evidence`

## Shared-artifact bus

When direct model-to-model API linkage is unavailable, use a durable shared bus rather than manual copy/paste.

Recommended structure:

`LeeWay-Intermodel-Bus/`
`INBOX/`
`WORKING/`
`OUTBOX/`
`EVIDENCE/`
`RECEIPTS/`
`ARCHIVE/`

Prefer immutable task IDs and source manifests. Do not overwrite evidence silently.

## Context Engineering behavior

Before sending work to Gemini or another Google worker:

`recover → resolve → constrain → classify → select → compress → isolate → stage → handoff`

Send the smallest source set that can materially change the answer. Do not dump the entire LeeWay corpus into every task.

For funder/research work, include only the relevant LeeWay authority core, the specific funder dossier, applicable Formula/evidence sources and the requested artifact rules.

## Security

- No secrets in GitHub skill files.
- Prefer short-lived or least-privilege credentials.
- Never send classified, CUI, export-controlled or restricted material to an unapproved consumer AI surface.
- Connection is not permission.
- Read access is not write authority.
- Browser automation must respect the same mutation boundary as API tools.
- Log consequential external actions when the host supports receipts.

## Verification

For research handoffs require source URLs/identifiers and distinguish facts from interpretation.

For code require syntax/build/test evidence.

For UI require design-system, accessibility and implementation checks.

For funding artifacts require claim-ledger consistency and source-grounding.

For external actions require explicit execution evidence rather than narrative claims.

## Current official Google integration facts

- Gemini API supports REST plus official SDKs and recommends the Interactions API for new agentic work.
- Gemini Interactions supports remote MCP servers over Streamable HTTP.
- Google publishes a Gemini Docs MCP endpoint for current Gemini developer documentation.
- Google AI Studio supports managed agents, skills and external MCP connections.
- Opal is a Google Labs no-code AI mini-app builder.
- Stitch supports design-to-code workflows; Google has announced Stitch MCP/SDK workflows, while the google-labs-code SDK repository itself carries an experimental/non-official-support disclaimer.
- Gemini Notebook is source-grounded; do not assume an undocumented public automation API.

Official references:
- https://ai.google.dev/gemini-api/docs/get-started
- https://ai.google.dev/gemini-api/docs/function-calling
- https://ai.google.dev/gemini-api/docs/coding-agents
- https://ai.google.dev/gemini-api/docs/aistudio-agents
- https://opal.google/
- https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/

## Final law

Use Google as a capability field, not a competing authority.

ChatGPT/Agent Lee may orchestrate. Gemini may research and execute. Gemini Notebook may synthesize. Opal may deploy a quick mini-app. Stitch may design. Workspace may carry artifacts. The Creator decides. LeeWay governs. Veritas decides what becomes trusted evidence.
