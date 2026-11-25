---
name: archify-gcp
description: Create polished Google Cloud architecture diagrams (standalone HTML + SVG/PNG/draw.io) from a typed JSON spec using the official Google Cloud icons, with an optional monthly cost estimate from the Cloud Billing Catalog API and an advisory Google Cloud Well-Architected Framework review. Use when the user asks to diagram, visualize, document, cost or review a Google Cloud architecture, VPC/network topology, GKE or serverless design, data pipeline, or a Vertex AI / RAG / agent workload.
license: MIT
metadata:
  version: "0.1"
  companion_to: tt-a1i/archify
---

# archify-gcp

Turns a description of a Google Cloud workload into a checked, explorable diagram. Same philosophy as Archify: write typed JSON,
let the tool lay out, route and validate, and report only what was actually verified.

## Setup
Installed with `npx skills add akashtalole/archify-gcp`; run every command below from the skill directory (`node bin/archify-gcp.mjs ...`).
The official Google Cloud icons are downloaded automatically on the first `render`/`finalize` (network needed once). To fetch them yourself or check the install:
```bash
node bin/archify-gcp.mjs fetch-icons
node bin/archify-gcp.mjs doctor
```
No npm dependencies. PNG export additionally needs Chrome/Chromium (`CHROME_PATH`, or Playwright's browser).
Cost estimates need a price book: `GOOGLE_API_KEY=… npm run prices:fetch` (your own Cloud Billing API key). Without one the Cost tab is simply omitted.

## Diagram types
| Type | Use for | Start from |
|---|---|---|
| `architecture` (default) | Topology: organization, projects, VPCs, zones, products, data stores | `init three-tier` / `serverless-api` / `genai-rag` |
| `sequence` | API call chains, request lifecycles, agent tool calls, retries, async handoffs | `init sequence` |
| `dataflow` | Pipelines, ETL/ELT, ingestion → store → serve, lineage | `init dataflow` |

Unsure? `node bin/archify-gcp.mjs guide "<scenario>" --json`. Existing assets: a Mermaid flowchart/sequence (`import mermaid`) or a Terraform repo using the
`google` provider (`import iac`) — see [references/importers.md](references/importers.md); review the icon mappings it lists and the relationships it inferred before delivering.

## Workflow
1. **Understand the workload.** Identify entry point, main request path, data stores, async paths, identity, and observability. For AI workloads also: model access,
   safety controls (Model Armor, safety filters), retrieval/grounding data, logging, agent tools. If the user pastes an architecture description, a Terraform repo or a
   Mermaid flowchart, read it for topology and re-author as a spec (do not mechanically convert styling).
2. **Pick icons.** `node bin/archify-gcp.mjs icons search "<term>" --json`. Use product ids/aliases (`gke`, `bq`, `cloud-run`); never invent ids. Use exact official names in
   `label` (full name first, short form after). Google has no separate icons for some newer products: use the closest official icon (`vertexai` for Gemini and models; the **Agents** category icon `category-agents` for Agent Engine, Agent Builder and Gemini Enterprise) and name the product in the label.
3. **Read** [references/spec.md](references/spec.md) once, and the closest example in `examples/`. Start from `node bin/archify-gcp.mjs init <template>`.
4. **Author the spec** (see *Authoring rules*). Put it in `.archify-gcp/<slug>-<timestamp>/spec.json`, with `meta.output` beside it.
5. **Finalize** (the one command): `node bin/archify-gcp.mjs finalize <spec.json> --json`. It validates, renders, runs strict artifact checks and a real-browser check, exports the PNG
   and writes `<out>.receipt.json`. A non-zero exit is never success: exit 1 = a gate failed — read `stages[].detail.errors`, fix every listed item (unknown icons come with
   suggestions); layout warnings mean reorder `children`, change `layout`, widen `gap`, or move a node next to its main neighbour. Rerun the whole command after each edit; max ~4 repair rounds, then report what remains.
6. **Look at the PNG** (open it) — the receipt says `visualReview: "not-performed"` because mechanics are checked, aesthetics are not. Fix collisions, tangled routes, unclear labels.
7. **Cost and review.** `finalize` also writes a **Well-Architected review** tab (and a **Cost** tab when a price book exists) into the same HTML; read `cost` and `review` in the receipt.
   Do not paper over gaps by adding decorative icons: either the architecture really has the control (add it, with its connection) or say it's out of scope.
8. **Report:** absolute paths to `.html` (and `.svg`/`.png`/`.drawio`), node/edge counts, warnings, the monthly cost with its confidence and key assumptions (or that no price book was loaded),
   the findings by risk, how many recommendations were actually evidenced, and explicitly: "cost is an indicative list-price estimate and the review is advisory — inferred from the drawing, not from deployed configuration".

## Cost estimation rules (adapted from the AWS billing-and-cost-management skill)
* Check today's date before quoting prices; the price book records its retrieval date.
* Never do cost arithmetic by reasoning: run `archify-gcp cost` (deterministic code) and quote its numbers. 730 hours/month.
* Only public on-demand list prices from the Cloud Billing Catalog API. Never invent a price; unpriced components stay "not-itemized" / "not-estimated" (Vertex AI model tokens are not modelled: use `usage.monthlyUsd` and say where the number came from).
* Put real usage in each node's `usage`; defaulted assumptions make the estimate "indicative". Point to the Google Cloud Pricing Calculator for a quote.

## Well-Architected review rules (structure adapted from the AWS well-architected-review skill)
* The corpus is the frozen Google Cloud Well-Architected Framework snapshot (`archify-gcp wa corpus`); use canonical ids only (`REL-3.1`, `SEC-1.4`…), never fabricate one.
* Five statuses: Implemented, Partially Implemented, Not Implemented, Not Applicable, Cannot Determine. Say "Cannot Determine" rather than guess.
* Risk = impact × likelihood; do not manufacture Criticals, and acknowledge strengths. Scores are provisional when few recommendations are evidenced.
* The report is CONFIDENTIAL: do not post it to broadly visible channels without approval.

## Authoring rules (Google Cloud Architecture Center + Well-Architected)
* Structure first: `gcp-cloud › organization › folder › project › region › vpc › zone`. Show ≥ 2 zones (or regional/multi-regional tiers) when the design claims high availability.
  Global and regional managed products (Cloud Storage, BigQuery, Pub/Sub, Cloud KMS, Cloud Logging, Identity Platform) sit beside the VPC; draw a `perimeter` group for VPC Service Controls.
* One main flow, left → right, in a single `row` so icons share a centre line; branches above/below via `column` or `stack`. 6–15 nodes is the readable range; split bigger systems into several diagrams.
* Number only the primary request path (`step`); dashed edges for async, replication, control and telemetry.
* Label every non-obvious edge with protocol/action. Don't label edges that a label would not clarify.
* Use `custom` groups for product-scoped boundaries (for example a "Vertex AI" group), `stack` only for alignment.
* Never alter icons; never invent products or icons; do not draw controls the user didn't ask for just to please the review.
* AI workloads: draw clients → authenticated API layer (Apigee / API Gateway) → orchestrator → (Model Armor or safety filters, retrieval, model) → request-response logging.
  Name the safety node "Model Armor" (or "… safety filters") so the review recognises it; show the vector store / knowledge source and where logs go. See [references/well-architected.md](references/well-architected.md).
* Readers get Reach, Route, Finder, Passport, presentation and export for free; point users at them and at deep links (`#focus=…&reach=downstream`, `#route=a~b`) — see [references/viewer-runtime.md](references/viewer-runtime.md). Reach/Route are authored reachability, not impact analysis: say so.
* Diagram conventions are summarised in [references/gcp-diagram-guidelines.md](references/gcp-diagram-guidelines.md).

## Commands
`finalize`, `render`, `export --format drawio`, `validate`, `cost`, `wa review|corpus`, `review`, `import mermaid|iac`, `icons search|info|categories|groups`, `guide`, `schema`, `init`, `fetch-icons`, `doctor` — run
`node bin/archify-gcp.mjs --help`. Always pass `--json` when parsing results.

## Don't
* Don't claim visual quality you didn't inspect, or that the review certifies compliance.
* Don't commit the downloaded icon package; don't install this skill into a live agent setup unless asked.
