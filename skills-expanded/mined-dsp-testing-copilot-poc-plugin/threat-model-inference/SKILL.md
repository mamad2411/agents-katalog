---
name: threat-model-inference
description: "Infer a deployment-aware, minimal-but-viable STRIDE threat model for the repository this runs in. Recon the checkout, then use org-wide GitHub code search to reconstruct how the service is deployed and what it talks to, derive trust boundaries, enumerate high-signal STRIDE threats mapped to CWE/OWASP, rank them by likelihood x impact, and propose mitigations. Read-only: writes THREAT-MODEL.md + threats.json + service-graph.json to a run directory for human review, then optionally surfaces them via artifact-placement. Triggers: threat model this repo, infer threat model, STRIDE analysis, attack surface, security risk model, what could an attacker exploit, deployment trust boundaries, dreaming threat model."
user-invocable: true
allowed-tools: bash, view, grep, glob, github-mcp-server-search_code, github-mcp-server-get_file_contents
---

# Threat Model Inference

Produce, fully unattended, a **viable but minimal** STRIDE threat model for the repo this
automation runs in — and infer the **deployment and service topology from the rest of the
org** so the model has real trust boundaries instead of a single-repo guess. The cross-repo
inference is the value-add: a single-repo read cannot see where a service sits relative to the
internet edge, its datastores, or its callers.

**This is a PoC: minimal but valid.** It distills the 8-phase interactive STRIDE workflow of
[`fr33d3m0n/threat-modeling`](https://github.com/fr33d3m0n/threat-modeling) (BSD-3-Clause) into
**5 unattended steps**. Borrowed *ideas only* (STRIDE structure, DFD elements, trust boundaries,
the likelihood x impact rubric, CWE/OWASP mapping) — no files copied. The source's per-phase FSM,
YAML data contracts, KB, and interactive checkpoints are intentionally dropped: a Dreaming run is
background and non-interactive.

**Honesty principle.** The output is an *inferred* model. Code search sees code, not running
config, secrets, or network policy. **Every cross-repo claim is flagged as an assumption** with
the exact search query that produced it, so a human can correct it.

## Prerequisites & constraints

- **GitHub-MCP-only.** Cross-repo discovery uses `github-mcp-server-search_code` /
  `get_file_contents`. Do **not** use `gh api`/`curl` — the Dreaming sandbox firewall blocks
  network egress; only the GitHub MCP server is reachable.
- **Read-only.** Read the checkout and the org via MCP; write artifacts only to `$RUN_DIR`
  (outside the checkout). Never commit, never open a PR.
- **Target repo is the checkout.** In a Dreaming automation the repo is checked out at the
  workspace root — use that as `--root`. The `OWNER` for org search is the repo's owner.

## Helper scripts

Invoke by absolute path as `"$SKILL_DIR/scripts/…"`, where `SKILL_DIR` is this skill's own
directory. All three are pure stdlib, deterministic, and firewall-safe (no network).

| Script | Purpose |
| --- | --- |
| `scripts/recon.py` | Deterministic security recon of the checkout; emits `recon.json` (entrypoints, auth, data stores, secrets, deploy artifacts, hostnames) + ranked **service identity**. |
| `scripts/plan_searches.py` | Turn `recon.json` into a bounded org **code-search battery** (`plan`), and fold the results the agent collects into `service-graph.json` (`--normalize`). |
| `scripts/score_risks.py` | Validate the agent-authored `threats.json`, compute **severity** from likelihood x impact (with cross-boundary amplification), sort, and render the Markdown risk table. |

## Procedure (5 steps)

Set up once:

```bash
SKILL_DIR="<this skill's directory>"
ROOT="<path to the checkout>"                 # the automation workspace root
OWNER="<org/owner of this repo>"              # for org-scoped code search
RUN_DIR="$(pwd)/threat-model-run-$(date +%Y%m%d-%H%M%S)"; mkdir -p "$RUN_DIR"
```

### Step 1 — Local recon (checkout only)

```bash
"$SKILL_DIR/scripts/recon.py" --root "$ROOT" --out "$RUN_DIR/recon.json"
```

`view` `recon.json`. Confirm the **top service-identity candidate** is right (it seeds the
search battery); if the guess looks wrong, note the correct name — Step 2 carries the top 3.

### Step 2 — Deployment & service-graph inference (cross-repo)

Generate the bounded query battery, then **execute each query with
`github-mcp-server-search_code`** (this is the only sanctioned cross-repo tool):

```bash
"$SKILL_DIR/scripts/plan_searches.py" --recon "$RUN_DIR/recon.json" --org "$OWNER" \
  --out "$RUN_DIR/searches.json"
```

For each query in `searches.json`, call `github-mcp-server-search_code`, and collect the hits
into a JSON array of `{purpose, query, repo, path, url, snippet}` at `$RUN_DIR/results.json`
(use `get_file_contents` to confirm a manifest actually deploys this service before trusting it).
Then normalize:

```bash
"$SKILL_DIR/scripts/plan_searches.py" --normalize --results "$RUN_DIR/results.json" \
  --out "$RUN_DIR/service-graph.json"
```

`service-graph.json` is the **inferred** deployment/dependency graph (deployer / upstream /
downstream / infra edges), every edge tagged `assumption: true`. If `search_code` is
rate-limited or returns nothing, proceed with an empty graph and say so in the report — do not
invent edges.

### Step 3 — DFD + trust boundaries

From `recon.json` (processes, data stores, surfaces) + `service-graph.json` (external entities,
deployment position), author a **minimal data-flow diagram** and mark **trust boundaries**
(internet edge, service-mesh / intra-cluster, datastore boundary, secret-store boundary,
third-party boundary). Trust boundaries come directly from the Step-2 topology and are the
most valuable output. Express the DFD as a **Mermaid** diagram + a short element list in the
report.

### Step 4 — STRIDE enumeration (high-signal only)

For each DFD element and each data flow that **crosses a trust boundary**, enumerate the
applicable STRIDE categories. **Cap the inventory at ~15–20 threats** — prioritise
cross-boundary flows and the surfaces/auth/data-store/secret signals from `recon.json`. Write
each threat to `$RUN_DIR/threats.json` (array) using the schema in `score_risks.py`'s header:
`id, element, stride, threat, cwe, owasp, likelihood, impact, crosses_trust_boundary,
mitigation`. Map each to a **CWE id** and an **OWASP category**.

### Step 5 — Risk rank + mitigations

```bash
"$SKILL_DIR/scripts/score_risks.py" --threats "$RUN_DIR/threats.json" \
  --out "$RUN_DIR/threats.json" --table "$RUN_DIR/risk-table.md"
```

This computes a consistent `severity` (likelihood x impact, +1 level if cross-boundary), sorts,
and validates. **Fix any hard validation errors** (exit 1) and re-run. Ensure **every High /
Critical threat has a concrete mitigation** (the script warns when one is missing).

## Output contract

Write to `$RUN_DIR` and report the absolute paths. Produce:

1. **`THREAT-MODEL.md`** — the deliverable. Sections, in order:
   - **Executive summary** (service, what it does, top risks at a glance).
   - **Inferred deployment & architecture** — narrative built from `service-graph.json`, with a
     clear **🚩 Assumptions** callout (this is inferred from code search, not verified).
   - **Data-flow diagram** (Mermaid) + **trust-boundary table**.
   - **Risk inventory** — paste `risk-table.md` (sorted by severity).
   - **Mitigations** — for every High/Critical, a concrete fix.
   - **🚩 Gaps & limitations** — wrong-service-identity risk, empty/uncertain graph areas, what a
     human must verify.
2. **`threats.json`** — the validated, scored, machine-readable inventory.
3. **`service-graph.json`** — the inferred topology + the exact `search_code` queries as provenance.

Do not commit and do not open a PR. Surfacing the artifacts as a `Dreaming`-labeled issue via
`/artifact-placement` is a separate downstream step (the standard automation prompt runs it after
this skill).

## Always do

- Use `github-mcp-server-search_code` for all cross-repo discovery; never `gh api`/`curl`.
- Flag every cross-repo inference as an assumption and record its query.
- Keep the threat inventory minimal (~15–20) and high-signal — cross-boundary first.
- Run `score_risks.py` and resolve hard failures before writing `THREAT-MODEL.md`.

## Never do

- Never invent deployment edges or threats not grounded in recon/search evidence.
- Never print secret *values* — `recon.py` reports only the fact + file location.
- Never write into the checkout or any repo; `$RUN_DIR` only.
- Never block on user confirmation — this runs unattended.

## Source

Concepts adapted from `fr33d3m0n/threat-modeling` (BSD-3-Clause): STRIDE categories, DFD
elements, trust boundaries, the likelihood x impact severity rubric, and CWE/OWASP mapping.
Distilled and re-implemented for unattended, GitHub-MCP-only Dreaming runs; no source files copied.
