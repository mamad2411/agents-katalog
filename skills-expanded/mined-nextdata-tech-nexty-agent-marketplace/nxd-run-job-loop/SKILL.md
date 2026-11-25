---
name: nxd-run-job-loop
description: THE ENTRY POINT for local business-data work — whether the user asks a question or asks to BUILD. Use when a task references tabular business data (CSVs, spreadsheets, exports, a live database, a REST API) and the user wants an analytical answer they may revisit (breakdown, ranking, comparison, trend, anomaly, driver) OR asks to build or generate a data product over it. A direct build request starts HERE, not in nxd-generate-data-product: this skill gathers intent, sources, questions, models, transform logic, explicit inputs and outputs, inline terms, decisions, and open questions into the prose-first editable dp-blueprint.md, then invokes the generator. Going straight to the generator skips the co-authoring checkpoint. Answer only from the product's semantic query result; never substitute raw SQL, pandas, or shell aggregation. Not for one-off arithmetic. For a deployed platform product, use nxd-query-data-product.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Agent
  - Task
metadata:
  author: nextdata
  version: 0.76.0
---

# nxd-run-job-loop skill

These rules apply on every route before source gathering, whether references load or not:

- No local commands during first-plan discovery; never ask the user to run them or use a CLI construction fallback.
- Never ask for credential files, placeholders, YAML edits, environment variables, or secrets in chat. For a credentialed source, check the live `infra_profile_connections.native_entry` capability and use the native masked prompt through the connection tools when available; see [native infra-profile connections](reference/infra-profile-connections.md). For source-credential recovery, never ask for an env-variable name or give commands, OS setup, or restart instructions. Report only an evidenced blocker and supported next action; never invent a login requirement or claim waiting cannot help. Never offer or solicit a chat-connector fetch or file substitute for a requested live in-product source; only an independent user request to change source scope permits that different product. If the user volunteers a credential anyway, do not echo or copy it; tell them it now sits in chat history and should be rotated.
- Never guess spending protections, budgets, models or approval durations.
- Use runtime capability calls before claiming anything about the environment.
- Ask only for business meaning, source access and human consent.
- Read back result-changing plan choices before materialization; the agent owns authoring. Interpret approval by its explicitly authorized object and limits, never the word "approved" alone. Permission to inspect access, check connectivity or draft a plan is not complete prepared-plan consent; do not relay it as `session_decision` or use it to generate, build or publish.
- Require native spending acceptance and all admission gates; setup checks are not scoring.
- Keep diagnostics internal and answer only from published semantic query evidence; engineering tracker references never belong in setup/failure narration or explain the user's blocker, while verified business identifiers may cite the requested results.

## If a reference cannot be loaded

If a reference cannot be read at the announced base directory, locate this skill's own sibling paths through the host's plugin directory only after an exact skill
name + `metadata.version` match to this SKILL.md. Never substitute another version.
If still unavailable, say "Some guidance could not be loaded"; keep the rules above.

A missing document never implies the runtime is unavailable. Check the tools;
never tell the user to "open Claude Desktop" to recover a missing reference.
Use [user-facing-language.md](reference/user-facing-language.md) whenever readable.

## Overview

This skill is the analyst-facing entry point for local business-data questions; start from the user's outcome and available data, not internal product language. When a durable local product is useful, drive the **local job loop**: a natural language intent plus a local source become a running, queryable desktop product.

```
intent + sources + questions
   → author dp-blueprint.md, the IR    (user-editable; the policy read-back)
   → infer the semantic model          (nxd-build-semantic-data-product)
   → generate the runnable closure     (nxd-generate-data-product)
   → admit and publish on the supervisor (nxd-desktop MCP)
   → render the pinned static release  (nxd-render-static-artifact)
   → describe → translate NL → query → present → refine
```

This skill is the **orchestrator** and entry point for end-to-end builds. `nxd-generate-data-product` constructs the closure after the plan is settled; if you arrive there without Steps 1–1b, come back here first. It invokes the owning skills, then drives the supervisor MCP path — routing the user never sees.
> **You own the conversation and sequencing**, except for the policy read-back discharged by the approved `dp-blueprint.md` in Step 1b. Keep one data product in flight at a time while iterating.

## Route the request before doing work

Classify the request before provisioning, generation, or querying, and prefer the smallest path that gives an honest answer — the routing table, step order, caps, the one-DP-in-flight rule and the subagent fan-out are in [reference/scheduling.md](reference/scheduling.md). The two routes that decide the whole loop: **a source is in scope with no suitable local product** → run the loop end to end; **an existing local product but no live endpoint/token** (the typical new session, since the bearer never persists) → **reattach, don't rebuild**: `list_data_products` → `resume_data_product` → artifact. `list_data_products` is discovery only: it never supplies a static-artifact fallback and cannot show whether a run is in flight or finished. When the user returns or asks where things stand, read `inspect_run` (or `inspect_workflow`) before reporting status, never from memory ([reference/context-and-resume.md](reference/context-and-resume.md)). Treat ambiguity conservatively: when a request could mean either a one-off calculation or analysis of an unseen source, ask which should answer it, and prefer the reusable local-product path for recurring or multi-question work.

## Choose the execution surface

Choose this order before invoking any runtime command:

1. **MCP first.** Read the server's `tools/list` catalog when the client exposes
   it; this hand-maintained list is not exhaustive. New construction requires
   `get_workflow_capabilities`, `prepare_workflow`, `advance_workflow`,
   `inspect_workflow`, and `reset_workflow`. Published products use
   `list_data_products`, `resume_data_product`, `describe_models`, and
   `run_semantic_query`, plus read-only `export_data_product` for on-demand
   handoffs. On provider failure, use capability-advertised `provider_credential_status` for its read-only check; if the key is missing, call `begin_provider_credential_entry` (native masked prompt; never ask for the key in chat); see [workflow-v2](reference/workflow-v2.md#provider-credential-access).
   Use `inspect_workflow` once for an admitted failure rather than classifying it from prose. If `get_workflow_capabilities` or `list_data_products` returns `update.status: available` (and only then, unprompted), mention a newer Nexty Desktop once per conversation per [workflow-v2](reference/workflow-v2.md#gate-on-the-connected-capability): never name a version; link `download_url` verbatim only if it starts with `https://` (it opens the update download for their setup, whether an installer or the guide page); never fetch or run the installer or offer the update as a fix.
   This is the supported route for Claude Desktop and Claude Cowork. Read-only `nxd://`
   **resources** — with tool bridges where a client exposes none — expose what a
   release *declares*: [reference/catalog-resources.md](reference/catalog-resources.md).
2. **No construction fallback.** Direct CLI commands and local substitutes do
   not replace the v2 admission path.
3. **Otherwise stop.** Report that no usable v2 desktop runtime is connected
   and give the provisioning/connection recovery action.

In Claude Cowork, its workspace `Bash` is an isolated Linux environment — use it
only to read, stage, or materialize task files. **Never run `uname`, binary
probes, or supervisor commands there**, and never use its Linux paths as MCP
definition paths: the connected `nxd-desktop` MCP server runs on the host and is
the runtime authority. This plugin's validator restricts `allowed-tools` to
built-in names and cannot list MCP tools; the `mcp__nxd-desktop__…` calls above
are mandatory anyway whenever the session registry exposes them.

## The loop — step by step

### Step 1 — Gather intent, sources, questions, and output needs

Establish the following (ask the user for whatever is missing). Before asking for a path or claiming no source exists, inspect supplied attachments, declared workspace artifacts, source profiles, and reference files; use a discovered in-scope source and ask only for a genuine gap.

- **Intent** — what the data product is about, in the user's words.
- **Sources** — where the in-scope local data lives. Preserve each source
  exactly by default; for an in-scope file, use only the declared projection
  exception for unneeded personal data. Keep generated exports separate from
  the supplied source. **Shared folder:** job files need one the user has shared. If none, ask them to add one in the app (Desktop: "+" menu, "Add folder"; if unsure, "add a folder to this conversation"); never give them terminal or PowerShell commands, and create subfolders with your file tool ([details](reference/source-materialization.md#a-folder-to-work-in)). A REST API that serves only a recent window or revises past days, when the request implies repeated refreshes ("ready each morning"): settle the lookback and late-arrival handling with the user before the first build, and build it into the first transform ([incremental-transforms.md § Rolling-window sources](../nxd-generate-data-product/reference/incremental-transforms.md#rolling-window-sources-settle-the-lookback-before-the-first-build)).
- **Questions** — the natural-language questions the DP must answer. These
  drive the whole inference (right-to-left): the model is judged by whether it
  answers them.
- **Models, transform logic, and outputs** — what named relations should exist,
  which typed operations produce them, which questions each Output answers, and
  where each Output is delivered.
- **Any procedure the user already has** — capture it as a versioned procedure
  on a Transform step or reference Model. Decisions record provenance and
  rationale; they are never executable policy. If it is already written down,
  translate the document rather than asking the user to re-state it.

Warm the user up before long work: state you'll write the spec, generate the DP,
run it locally, then answer their questions — a multi-minute build is expected,
not a stall. **Determine every source the data product needs before
materializing.** A product may need one source or several — the same connector
type twice, or a mix (a database plus a REST API). For each, determine its
connector type: local file(s) (CSV/JSON/JSONL/Parquet), a live database
connection, or an off-mesh REST API. Ask if not already stated; never assume
database or API access exists because a question sounds analytical. If the
request already states a source's type and details, gather it all in one turn.

**The moment there is more than one source, give each a short, distinct label**
(lowercase, hyphenated, e.g. `orders`, `users`) and use it consistently for the
rest of the loop; a single-source data product needs none, so don't invent one.
The one-product-in-flight rule above limits how many products you build at once,
never how many sources one may have. Materialize each source faithfully before
inference — repeat the matching bullet once per source, tagging every artifact
with that source's label. **If the request supplied a procedure (rubric, gates,
thresholds, verdicts) with a gap that changes a result, the policy read-back in
Step 3's skill comes FIRST** — reading a source is always allowed, but copying it
into a closure is a materialization and waits for the user's reply. Per-kind
rules — attached file, pasted table, database, REST API and host-path handoff —
plus credential guidance are in [reference/source-materialization.md](reference/source-materialization.md).
It requires exact-copy landing by default, with one declared projection for
unneeded personal data; tell the user what was omitted and why without echoing it. When the user asks where to enter a key and the credentialed source's nonsecret service is settled, open native masked entry from a dedicated source-preparation sibling of the executable closure (never its parent or ancestor); this can precede complete-plan approval but never authorizes a fetch, build, or paid work.

### Step 1b — Author `dp-blueprint.md`, the prose-first user plan

Write what Step 1 gathered into **`dp-blueprint.md`** at
`…/nxd-jobs/<workflow>/dp-blueprint.md`, beside the closure (which lands at
`closure/`). The user-facing document uses the fixed, ordered sections Intent,
Questions, Scope, Terms, Inputs, Models, Transform, Outputs, Decisions, and
Open Questions. Keep the headings strict but allow ordinary prose, lists,
tables, examples, and code blocks within them. The user must never be asked to
write or inspect the terse typed proposal. Schema, Terms behavior, editing
rules, and the Claude Desktop form contract are in
[reference/dp-blueprint.md](reference/dp-blueprint.md). Every plan, the first included, writes its implicit conventions (row exclusion, matching, timezone, tie-break, null measures, aggregate span, fetched versus kept fields) as defaults, asking first when a choice changes the reported numbers and the source does not settle it ([§ Conventions every plan states](reference/dp-blueprint.md#conventions-every-plan-states)).

**If the user supplied a doc** — a build spec, a rubric page, or a prose
description — preserve its meaning in the Markdown and show what you filled in.
Do not force the user to translate it into labelled fields. Put expectations
under Inputs, promises under Outputs, and behavior-affecting decisions in
Transform. Terms are inline in this document; do not create or depend on an
external Glossary DP. Delivery is the platform-fixed local DuckDB semantic
query path, not a user-authored section. Executable contracts are compiled
internally from the Input expectations and Output promises. **A deviation the user asked for.** When the user explicitly asks for a workflow with a deliberate defect (for example a negative-credential fixture that omits `auth_type`), build it as asked and record it in that workflow's blueprint as an explicit Decision that quotes the user's request verbatim (any credential replaced as in the sanitized original request) and states the expected failure. A reviewer claim whose failure is exactly that expected failure, with no further affected output, may be adjudicated `out_of_scope` citing the Decision and the request text ([conditions](../nxd-generate-data-product/reference/adversarial-review.md#adjudicate-every-finding--this-is-the-point)). Every other `HIGH` or `MEDIUM` claim, disclosed or not, is adjudicated normally. Adjudicating normally includes `rejected` for a claim that objects to exactly the outcome an explicit instruction in the request requires and names no other affected output (never a deliberate defect, which stays `out_of_scope` as above, nor an approval, consent or credential claim); do not stop a workflow on a claim you have not verified as a defect, and when the user asks for a terminal step (validation, refusal on record), reach it.

Every Decision must come from something the user stated or explicitly named as
controlling policy. Never pre-fill an anticipated decision or reversal; mark an
unmade choice `[DECIDE]`. See [reference/workflow-v2.md](reference/workflow-v2.md).

After writing or editing the document, run the structural validator:

```bash
python3 "$JOB_HELPER_DIR/scripts/validate_dp_spec.py" <path>/dp-blueprint.md --json
python3 "$JOB_HELPER_DIR/scripts/dp_spec_authoring.py" validate <path>/dp-blueprint.md --json
```

The deterministic parser only checks headings, free prose, source spans, and lifecycle metadata. The typed `proposal` payload is a closed v3 object with exactly 12 keys; frontmatter-only `name` and `workflow` do not belong in it. Follow [reference/workflow-v2.md](reference/workflow-v2.md) for the exact nested shapes, statuses, fixed delivery object, and compiled contract rules. Then have the AI write the complete caller-authored typed proposal JSON beside it as `dp-blueprint.proposal.json`, omitting `source_hash` and carrying `explicit`, `inferred`, or `platform_fixed` provenance, source spans, compiled contracts, the fixed delivery profile, and a complete natural-language echo-back. Validate and bind its proposal content against the parsed blueprint before prepare. The supervisor owns the canonical `source_hash`: it inserts or replaces that value from the retained Markdown before validation and binding. Do not guess or hand-compute it when shell access is unavailable. Deterministic proposal validation must turn underspecification into an Open Question; it must never accept confidence as correctness.

**Approval is approval of the echo-back.** A validator pass is not approval,
and `status: approved` is the user's decision. A bare "yes"/"sure" that names nothing is neither approval nor a choice; re-ask once for the single item ([reference/workflow-v2.md](reference/workflow-v2.md)); never offer an accept-all-recommendations shortcut for disclosure, suppression or baseline questions, or for any other choice that changes the reported numbers and that the source does not settle; ask those before preparing, never as non-blocking defaults ([reference/dp-blueprint.md](reference/dp-blueprint.md)). Approval binds the Markdown and
supervisor-derived typed proposal hashes plus Terms, contract-inventory, compiler,
and delivery metadata. Lock each approved Decision by id and hash; extraction may not
overwrite it. A conflicting edit becomes an explicit change proposal and
revokes approval. The approved Markdown and typed proposal are byte-snapshotted
into the closure, never referenced through `../dp-blueprint.md`.

When a question needs a judgement read from each entity's evidence, model that
decision as a versioned `apply_procedure` Transform step or reference Model.
The result is a named Model exposed through an Output; the Decisions ledger
remains provenance only.

### Step 2 — Infer the semantic model

Invoke the **nxd-build-semantic-data-product** skill in its inference mode: profile
each source into `schema.json`, then derive the semantic model — grains,
dimensions, metrics, joins, PII, **and a description on every model, dimension
and metric** (Step 5 reads them to map questions) — from the profile(s), the
user's questions, and the spec's `models:` plan. With 2+ sources profile each
separately, carrying labels forward. That skill owns the role grammar. For this
local flow its complete output is `schema.json` plus
`semantic-model-plan.json`, both beside `dp-blueprint.md` and outside
`closure/`. This step must not create or edit `models.py`, `spec.py`,
`transform/`, `requirements.txt`, or any other generated closure surface, and
must not invoke the generator. Treat any executable closure write from the
inference step as a failed handoff: remove that unapproved generated output and
repeat inference within this boundary.

### Step 3 — Enroll, approve, then generate the runnable closure

Before the approval turn, the main thread must establish the connected supervisor's v2 execution capability and enroll this exact prose/proposal pair: write and validate `dp-blueprint.proposal.json` beside the host-visible `dp-blueprint.md`, parse that complete object, call `get_workflow_capabilities`, require structured `execution_enabled: true`, then call `prepare_workflow` with `kind: "generated-data-product"`, the blueprint path, and the inline `typed_proposal` object. For an unspecified mapper model, author the `opus` family and explain the choice and factual cost tradeoff in the complete prepared-plan echo-back. Preserve an explicit model choice, including an existing grant model; never infer provider access or observed quality from pricing. During mapper preflight, automatically save a returned `proposed_spec` for `mapper/model_missing` and re-run `prepare_mapper` before capture; see [mapper preflight](../nxd-generate-data-product/reference/mapper-preflight.md#desktop-preparation). Ask a separate model question only if material ambiguity blocks preparation. Omit `source_hash` from the caller-authored file and inline object; the supervisor inserts or replaces its canonical value. Proposal validation and binding happen before consent; the prepare request must carry the complete typed proposal object, not a path or placeholder. When the transform makes a call per row (mapper scoring, another provider call, a per-row API request), set `requested_transform_budget_secs` on this first prepare from an estimate of rows × calls per row × seconds per call, doubled; the 180 s default cannot be raised later without `remove_workflow` and a full new consent and spending cycle ([workflow-v2.md § Size the transform time budget at prepare](reference/workflow-v2.md#size-the-transform-time-budget-at-prepare)). Keep the blueprint at `status: proposed` during prepare. Never set `status: approved` or invent approval hashes; approval remains only through the returned `session_decision` consent action. Use
only its returned revision, invalidation epoch, requirement identities and
`next_actions`. Do not present an approval prompt or ask for approval until
`prepare_workflow` succeeds. Then present the prepared echo-back and relay the user's exact approval through the returned `session_decision` action only when it authorizes the complete prepared plan; access-check or drafting consent leaves plan consent pending. Genuine complete-plan approval may permit generation while paid scoring is separately withheld; native spending/budget verification and all admission gates still apply. A capability blocker or
failed prepare/consent action stops construction; it does not bypass supervisor
admission with a direct tool or local substitute.
If `check_data_product` or a build call times out at the client or bridge, do not dispatch a new build: call `inspect_run` / `inspect_workflow` first. When `check_data_product` returns a `check_id` (newer supervisors), poll `inspect_check` instead of re-running the check; retry `check_data_product` only against the unchanged closure.

Before paid mapper scoring, read `get_workflow_capabilities.mapper_budget`; use returned tools only when `availability: available` and inspect before proposing and again after each spending approval, immediately before each `start_run`. With `status: legacy` and no cap request, keep the existing per-approval/per-spec flow. Legacy/proposed `completeness: not_applicable` with null usage is normal absence of an active cap, not Unknown. With legacy/proposed status and all limits user-stated, call the returned proposal tool; native Establish re-verifies and adopts earlier recorded ledger history in the inspected active runtime data folder, not the authoring folder. A requested cap needs native acceptance and established, complete, open inspection before scoring; any established cap must be complete and open. Propose only stated limits; never ask for starting balance or historical usage, a remaining balance or provider dashboard; a proposal is not active. Never propose around an established unknown/integrity or exhausted budget. Unsupported requested caps or unknown, integrity-failed and exhausted states stop paid scoring. On exhaustion with `reset_supported: false`, say plainly that this folder's limit cannot be raised, reset or disabled in this version and that no more AI scoring is possible here; never suggest another data folder, a new budget or any other way around it. Unknown is not zero; never infer whole-test zero. Close other Nexty sessions before opting in; existing sessions are outside the cap until restarted. See `reference/workflow-v2.md` for details.

The successful returned `session_decision` action is the generation gate.
Invoke **nxd-generate-data-product** after that gate succeeds to assemble
the executable closure inputs — `spec.py`, `models.py`, `infra-profile.yaml`,
`transform/main.py`, `requirements.txt`, the approved-plan snapshot,
`build-record.json`, `README.md`, and the connector artifact — from the approved
`dp-blueprint.md`, inferred model, and connector config. Pass every source, its
label and provenance, plus the resolved absolute `job_helper_dir`. The generator
compiles the approved plan; it does not re-derive it, author supervisor YAML, or open a new policy turn. Follow its connector references and `reference/dlt.md` for the exact closure shape. Preserve any Step 1 connection's bound public service identity and opaque ref, then inspect compatibility at the final root; zero matches needs native entry, multiple need an explicit choice, and stored metadata never proves source access ([infra-profile-connections.md](reference/infra-profile-connections.md)).
The typed-v3 proposal sent to `prepare_workflow` is the consent candidate: every Decision is included in the exact echo-back and may remain `status: proposed` until the user approves. The supervisor's trusted materializer projects those Decisions to `locked` only after the subject-bound `session_decision`; `locked` is an approval-derived snapshot state, not authorization by itself. Do not change the proposal after prepare or consent. Any post-prepare or post-consent blueprint/proposal edit requires `reset_workflow` with the supervisor-returned graph-root requirement and a replacement blueprint, followed by complete regeneration, fresh prepare, and fresh consent. A repair that changes only how the view is built, while keeping the plan unchanged, never asks the user to re-approve the plan: reset the returned capture requirement, recapture, re-review, and explain the fix in plain words. For requested rules in the first plan, see [dp-blueprint.md](reference/dp-blueprint.md).
Full replacement reset sends both `replacement_blueprint_path` and the complete
matching inline `replacement_proposal`; never send the blueprint path alone.
The typed v3 contract inventory is executable handoff, not optional metadata: every
Input expectation and Output promise must become exactly one closure verifier and
one matching `custom(...)` wiring at its declared attachment and phase. Preserve
the contract id, attachment, model, phase, guarantee, rule, and fields exactly;
ordinary `.promise(model)` never satisfies a custom contract.
Classify prepare failures before proposal recovery: `v3.open_question.blocking_unresolved` means return to the user, ask the indicated Open Question, record their answer in the blueprint as a Decision, reparse, regenerate every proposal field and span, strictly validate, and prepare with a fresh `request_id`. Never set `blocking: false` yourself; any question-state change must faithfully reflect the user's answer. `workflow/proposal_validator_unavailable` means stop and report the runtime failure; do not regenerate. Only if `retryable: true`, a retry of the identical request is permitted later; do not automatically retry or enter a regeneration loop. For provenance recovery, copy exact parser coordinates for every source span (a `###` subsection `.text` range excludes its heading but may include separator blank lines). A `v3.provenance.span_mismatch` with a bounded `prepare_recovery_id` must call `inspect_prepare_recovery` and use its versioned same-blueprint semantic hash plus complete `source_spans` to regenerate the entire proposal. The inspection response contains only canonical parser paths and four integer coordinates, never source text or typed values. The legacy `validation_issue.expected_source_span` is a v1-compatible location hint, not a license to patch one path; even when present, regenerate and strictly validate the complete proposal. A `source_block_uncovered` after recovery means the complete-regeneration invariant was violated: follow **Recovering a rejected proposal** in `reference/workflow-v2.md`, replacing the whole proposal with coverage for every populated `.text` path, never patching another named path. If no recovery id is available, stop on stable `source_map_code` (`v3.provenance.source_map_unavailable` or `v3.provenance.source_map_oversized`) and obtain a fresh parser result. If the MCP host exposes only error text, read only the bounded `prepare_recovery_id` or `source_map_code` suffix; never reconstruct a map from prose. Never guess, split, trim, widen, or alter typed values.

Before `prepare_workflow` succeeds, any blueprint edit invalidates all parsed coordinates: reparse the final blueprint, regenerate every proposal field and span, replace the complete proposal file with the available file operation, strictly validate it, and send a new globally unique `request_id`. Do not claim generic filesystem atomicity for a file-tool replacement. Reuse a request id only for a byte-for-byte identical request.
Under the shellless v2 contract, the agent must not run lock write, hand-author reserved v3 metadata, or copy a checker into the closure before capture. The supervisor owns capture-time materialization and verification of those reserved surfaces. Before every capture, including after a repair, call the `check_data_product` MCP tool as described in the [preflight before capture](../nxd-generate-data-product/reference/pre-capture-audit.md#preflight-before-capture). After the review is clear, call it once more on the unchanged authoring closure before requesting validation (full for a closure without the mapper; `mode:"structural"` for a mapper closure), so the last successful check follows the last review. This holds for every capture, including each one after a reset or a validation-time edit (edit -> record the round -> reset -> check -> capture -> review -> check again -> validate -> start_run; any recapture restarts at capture, and nothing is edited after the last check); a check made before the capture never substitutes for it. The check after the review is **full** (no `mode`; `mode:"structural"` only for a mapper closure): a structural result never counts for a closure without the mapper, and a check made before an edit, a reset or the review is stale, so rerun it after the last edit or reset and before any validation retry ([reference/workflow-v2.md § Final check before validation](reference/workflow-v2.md#final-check-before-validation)). It needs no shell. Full mode gives detailed findings for its own checks; it does not cover every trusted validation check. It is diagnosis, never execution authority or a substitute for supervisor validation or admission. Shell helper self-check and lock checks stay optional evidence. Generation starts only after the supervisor records the approval. Steps 2–3
stay on the main thread for an activated workflow-v2 session. Do not delegate
semantic inference, closure generation, or any workflow MCP action to a child;
the only conversation child is the single retained-capture review in Step 3b.
Policy read-back, review relay, credential injection, and host-path verification
also remain on the main thread. The main thread must verify the host-visible
definition path before capture. A new result-changing gap returns
`gap_found` and triggers a fresh read-back and generation-only bounce. See [reference/scheduling.md](reference/scheduling.md). Resolve `job_helper_dir` from the exact staged skill pack for this run. Its skill metadata version must match the loaded `nxd-run-job-loop` version and it must contain the expected helper scripts. A missing or mismatched helper path stops the workflow; never fall back to another cached plugin release.

### Step 3b — Capture, review, and adjudicate

After generation authors the executable closure inputs and optional agent-side evidence, follow only the supervisor's returned `capture` action with its host-visible authoring root; never modify the captured tree afterward. Run **exactly one mandatory review per capture generation** by immediately dispatching one built-in `Agent` or `Task` conversation subagent, supplying the supervisor's matching `review_input` paths, sanitized request, and the canonical dispatch marker from [reference/workflow-v2.md](reference/workflow-v2.md).
Keep semantic inference, capture, workflow MCP actions, review adjudication, and the rich `review-record.json` ledger in the main thread; the main thread must not invoke `Skill(nxd-review-closure)`, inspect the retained capture inline, or launch the reviewer through MCP/supervisor. Write the required `NXD_EVAL_ATTESTATIONS_PATH` sidecar before `start_run` as specified in the reference. With shell access, before writing every ledger round (including later edits to the same round), put `$JOB_HELPER_DIR/scripts` on `sys.path`, `import dp_diagnostics`, and call `validate_review_round(round)` (it is not a CLI subcommand), and fix each reported problem; reading the rules is not a substitute. Without it, check the round inline against the reference and do not claim it was helper-validated. Its vocabularies are closed: copy round `status`, finding `classification` and `state`, and adjudication `disposition` verbatim from the ledger table in [reference/workflow-v2.md](reference/workflow-v2.md), never composing one (`open_needs_user`, `semantic_defect_reported_medium`). A round that fails validation invalidates the review it records.

Before dispatch, select only the current matching `RequirementView`. On a host without a runner-owned review guard, require a non-content read-only host path/accessibility check for both exact retained paths, including generation, allowed roots, types, and readability. On a host with the eval/live runner's review guard, do not issue a separate owning-thread check: the guard performs and repeats it immediately before dispatch. A host runtime without an equivalent metadata/stat mechanism must stop if it cannot establish availability. If either path is missing, stale, outside the allowed roots, or inaccessible, stop with an explicit incomplete blocker, leave the requirement pending, and never substitute another path. See [reference/workflow-v2.md](reference/workflow-v2.md).

Follow the returned `report_requirement` action only after the reviewer returns; a clear report permits the returned validation and admission actions only after one more `check_data_product` on the unchanged closure (the post-review check, on every cycle including the last), while findings, rejection, indeterminate, or an incomplete handoff leave the requirement unsatisfied. When every claim left is `LOW` or advisory, report `verdict: "clear"` with `findings: []`, never `findings`: clear means no blocking claim, not no claims, and the `LOW` claims stay in `review-record.json` and your report to the user. A `findings` entry is always `severity: "blocking"`; if the supervisor rejects an advisory-only report, resend it as clear, and never ask the user or an operator to accept it ([details](reference/workflow-v2.md)).

`workflow/review_findings` with any `behavior_affecting` finding stays
`needs_user`: ask about its IDs and proposed effects. Do not edit, reset, or
recapture in that turn; wait for explicit approval in a later turn. “I don't
know, you tell me” and “whatever you think” are deflections on a review finding,
including one about a mapped rename (a renamed-key drift decision outside review follows [failure-handling.md](reference/failure-handling.md)). Record and validate the decision before reset; see [reference/workflow-v2.md](reference/workflow-v2.md). Ask once per round: all of a round's blocking findings go in one list with one plan amendment and one re-approval request; cosmetic hardening is not a plan change; after two rounds whose findings concern only your own fix, stop and tell the user what is left and the consequence of shipping versus not, and keep that stop until publication. Recommend a fix only when a finding changes published results now, and prefer one that fits the approved plan so the decision on its IDs needs no plan re-approval ([reference/workflow-v2.md](reference/workflow-v2.md)).

After a review completes, ordinary Bash remediation remains available for
non-retained paths until reset; the runner guard rejects owner operations and
shell commands targeting retained captures or blueprints.

There is no skip under the activated v2 contract and no duplicate review against a mutable closure. A rejected,
indeterminate, or scope-refused report remains unsatisfied. A fix requires reset, local correction, optional evidence if available,
recapture, and one fresh review for the new generation. See
[reference/workflow-v2.md](reference/workflow-v2.md).

Auto-fix only an evidenced syntax/mechanical/procedural structural correction with approved spec, models, grain,
rows, values, aggregation, thresholds, verdicts and asserts unchanged. A timeout needs explicit user consent; no credential enters a reviewer.

**Land the closure at a durable, user-visible path — never a temp or scratch
directory.** Put it under a directory named by the workflow id, with the IR
beside it: `…/nxd-jobs/<workflow>/dp-blueprint.md` and
`…/nxd-jobs/<workflow>/closure/`. The supervisor captures that closure through
the returned v2 action. Use whichever base the host-visible-path rules in Step 1
make legal, and state the durable `…/nxd-jobs/<workflow>/` location in the
user-facing handoff when the user needs to open or back up the generated files.
Give the user the durable result and, when needed to resume, the documented
user-facing workflow handle. Never expose temporary, scratch, or
supervisor-owned staging paths. The bearer never
persists, so a later session reattaches to an admission-linked publication by
**workflow id** (`list_data_products` → `resume_data_product`); if no valid
  publication remains, start a fresh v2 construction rather than a direct rebuild
([reference/context-and-resume.md](reference/context-and-resume.md)). The durable
record a later session reads is **generated, never hand-written**: supervisor capture materializes and verifies `dp-blueprint.approved.md`, `dp-blueprint.proposal.approved.json`, `dp-blueprint.lock.json`, and the trusted `self_check.py`; it also records `build-record.json` carrying what happened —
stages, attempts, concessions, blockers, the read-back. Conversation review
rounds live in the adjacent `review-record.json` so reporting cannot mutate the
captured closure. Self-containment is
checked against the lock rather than trusted: a derived model's contract lives
inside the closure, never behind a `../` pointer the handoff would strand —
`../dp-blueprint.md` included, since the IR is upstream of the closure, not a
dependency of it. **Relay the distribution read-back before admission** in one or
two lines — the per-classification-column value counts (call out a uniform one),
and which assertions are internal-consistency only rather than checks against the
source; it is recorded in `build-record.readback`, relayed verbatim, non-gating.
A green self-check means the closure is structurally sound and the transform ran
— never evidence the numbers are right.

### Step 4 — Build and serve through MCP

Steps 3–3b already completed capability gating, preparation, consent, capture,
and the single retained-input review. Continue the same v2 workflow from its
latest response: do not start validation unless the last successful `check_data_product` came after the last review report for this capture (else check now, closure unchanged; every workflow and revision, a late new workflow included; a full check (structural only for a mapper closure), redone after any edit or reset and before a validation retry), then follow the returned `start_requirement`
action for supervisor validation, then the returned `start_run` action for
admission and publication. Use the exact envelopes in
[reference/workflow-v2.md](reference/workflow-v2.md) (the required `advance_workflow` parameters per action are in its "Follow returned actions through admission" and "Relay consent and capture" sections); never reuse stale action
parameters. Validation can return a queued or running operation before it finishes. Poll `inspect_workflow` until validation is satisfied, then use its current revision and returned admission action. Never end your turn while validation or a run you started is queued or running: a rate-limited source can keep it running for minutes, and a hand-back gives the user nothing to decide. Each poll returns at once, so dozens of identical `running` replies are normal and never mean it is stuck; only a terminal state, a failure code or a refusal ends the wait.
On the MCP workflow path, wait inside this same turn. When `get_workflow_capabilities` lists `inspect_wait`, call `inspect_workflow` with `wait_seconds: 25`: it blocks server-side while an operation is queued or running and returns early when it settles, so each call is your wait (pass `after_event` with the last event you saw to read only newer events). Without `inspect_wait`, `inspect_workflow` and `inspect_run` return immediately, so keep calling them back-to-back until the state is terminal. Never use `check_data_product` or any other call as a timer: a check running alongside validation competes with it. Never start a background timer or background command and end the turn to "come back later", and do not use `sleep`, `run_in_background`, Monitor or timers to wait: nothing wakes you, so the work is abandoned. End the turn only on a terminal state, when `inspect_run` reports it unknown, or when you need the user. A `start_run` or build call that times out at the bridge is not a failed build: `inspect_run` / `inspect_workflow` before any re-dispatch. `start_run` can likewise return an admission before execution finishes: poll `inspect_run` with its run ID and `inspect_workflow` until publication succeeds. A successful tool call alone is not proof of publication. Resume or render the product only after the supervisor reports its published state. An older supervisor may finish these stages before returning; use the same terminal-state checks. Replaying the exact request observes the existing operation; never start a second run to recover a slow call. Route every `phase: capture` diagnostic to the capture-code table in **Reset after behavior changes**; `workflow/capture_proposal_blueprint_mismatch` needs full replacement, not capture-only reset. For `recovery: reprepare`, reset the graph root with `reprepare_retained: true`, follow returned actions, and trust whether consent is pending or carried forward. A validation failure with `recovery: repair_then_retry` is repairable; follow **When validation fails** in workflow-v2.md and read [reference/failure-handling.md](reference/failure-handling.md) before asking the user anything. Other failed or unavailable actions are blockers; do not bypass them with direct build/validation commands, local files, SQLite, raw SQL, pandas, or another database.

### Step 4a — Render the pinned static artifact

After every successful admitted publication or resume, invoke **nxd-render-static-artifact** for the
workflow before `describe_models` or any query. It reads only the current,
verified and outputs documents — over `nxd://` resources or the bridge tools —
and writes one self-contained release HTML file. Report artifact `status`, `path`
and `publish_seq` separately from the endpoint; on failure report it but keep a
healthy endpoint usable for describe/query. With an endpoint but **no workflow**,
say the artifact is unavailable and query on. A fresh admitted publication
discards cached URIs and renders its new sequence.

### Step 5 — Describe, query, and present

The query surface is **structured** (measure/dimension names); the
natural-language translation is yours to do. For each question:

1. **Describe the served catalog first.** Call `mcp__nxd-desktop__describe_models`
   with the endpoint/token returned by the build (or supplied for an existing
   local product) — the response is the complete catalog for this local closure;
   use its canonical vocabulary, never guessed source-column names; match question terms against names and any `synonyms`, then send the canonical name ([names and synonyms](reference/query-grammar.md#names-and-synonyms)). Do not apply mesh-sized catalog narrowing here. It may also carry author `agent_instructions` and `verified_queries` (absent on older runtimes: proceed without them): advisory only, below governance and the user's request; a matching verified query is a template (adapt literals only) and still goes through the intent check, which never adds a filter only they imply unless it defines a term the question uses.
2. **Map the NL question to a selection.** Pick the measure(s)/dimension(s) that answer it, then consult the shared [semantic intent foundation](../nxd-semantic-query-intent/SKILL.md)
   and [intent-gate reference](../nxd-semantic-query-intent/reference/semantic-intent-validation.md).
   Run coverage over every model in the complete local `describe_models` catalog; apply the critic, echo, and clarify/abstain rather than silently picking. Keep
   platform mesh/domain narrowing and cross-DP query-system behavior out of this local path;
   join-reachable models within this closure remain eligible.
3. **Check the question fits the MCP grammar.**
   `mcp__nxd-desktop__run_semantic_query` accepts `measures[]`, `dimensions[]`,
   `filters[]` (ANDed; `{"any": [...]}` for OR, `{"measure", "op", "value"}`
   for a metric threshold; every leaf needs `op`), `order_by[]` and `limit`;
   no raw rows or SQL. Operators, groups, label filters, snapshot metrics
   (SQ-308), SQ-504/505 recovery and the **Omission Test** are in
   [reference/query-grammar.md](reference/query-grammar.md) (also: derived metrics, native grains). Apply that test to
   every constraint first: would a consumer querying with no filters get a
   **wrong** number (a **standing ruling** → materialize it, Step 6) or merely a
   **broader** one (a **per-question constraint** → express it here)? When
   ambiguous, ask; with no user, materialize. Never re-aggregate agent-side, and
   never silently drop the constraint.
4. **Run the governed query.** Call `mcp__nxd-desktop__run_semantic_query` with the endpoint/token plus the selected measures/dimensions — don't bypass it with raw SQL or a local aggregation. For ranked questions, pass endpoint-native `order_by: [{"name": "<selected measure or dimension>", "dir": "desc"}]` and integer `limit`; never sort or truncate rows agent-side.
   For row-level outputs, select numeric values as dimensions; never substitute a `total_<field>` aggregate for a promised record field.
5. **Quantify the review bucket before presenting a classified total.** If the
   selection's model carries a classification dimension with a review bucket
   (`needs_review`, `unmapped`, `other`), a single headline number hides how much
   is unclassified. Run the same measure grouped by that dimension and report the
   bucket's share alongside the total whenever nonzero — "€480k total; €190k
   (40%) is `needs_review`". An unquantified review bucket is a preview.
6. **Parse + present.** Render the returned rows as a compact table and state the
   semantic selection that produced them. Surface any ruling behind the answer:
   if a dimension grouped by or filtered on carries a `describe_models`
   description naming a ruling (a mapping, an exclusion, a reclassification),
   state it in the answer — the consumer trusts it whether or not they know it
   exists. If the result depends on proposed classifications rather than
   confirmed decisions, say so plainly and name the relevant rule version when
   it matters; report the unscored share alongside it. Label any partial or
   unverified result as a preview.

### Step 6 — Refine wrong answers back into the loop

If an answer is wrong, missing, or unsatisfying, decide where the fix belongs.
Once the published product answers the approved request, finish the handoff; do
not start another workflow, draft a new version, or expand the questions, models,
or outputs on your own: after publication, change the product only for a business change the user named or approved (in place, per Model / DP-level below). "Continue" or "use your judgment" with nothing pending is not one: report the current published release as current, say nothing is pending, and ask what they want changed; wording, disclosure or presentation tweaks never justify a new workflow and run unless the user asks for that change. If the user later asks for a change, confirm that
requested scope before resetting or starting another workflow, then follow it rather than declining it.
Every level is **bounded**, and the bounds are **counted** from
`build-record.json` `attempts[]`, never estimated — remap ≤~2/question,
regenerate ≤~3 total, environmental retry ≤~3. Each attempt ends in one typed
exit: `healed`, `healed_with_concessions`, `caps_exhausted`, `blocked`,
`retry_environmental`. Read [reference/failure-handling.md](reference/failure-handling.md) on any repair outcome (`repair_then_retry`, `validation/scratch_transform_failed`, any contract failure) before asking the user anything, and before preparing any revised or successor workflow after a source change (also on any refresh or new-version request, probe the live source first: [workflow-v2.md § Revised or successor plan](reference/workflow-v2.md#revised-or-successor-plan)). The repair levels, cheapest first:

- **Query-level** (cheapest) — the model is right but the selection was wrong or a
  dimension was missing. Re-describe, re-map, re-query through MCP.
- **Model / DP-level** — the inferred model is wrong (missing metric, wrong
  grain, missing join, wrong PII, an undistinguishing description), or the
  question needs a column or grain that doesn't exist (a filtered figure, a
  ratio, a monthly rollup, a classification) — a **derived model**, not a tweak.
  **Edit `dp-blueprint.md` first**, re-validate, and re-approve it when the change
  touches a ruling (a criteria change is a new `rubric_version`); then go back to
  Step 2/3 and use `reset_workflow` while the v2 construction is still pending.
  After publication, a refresh with unchanged logic (new rows under `data/`, or a live source refetched) is a
  recapture of the same workflow: capture, review, approval, validation, `start_run` ([reference/workflow-v2.md § Refresh in place](reference/workflow-v2.md#refresh-in-place)).
  The same applies once a failed admitted run is terminal. Never reset or remove a published workflow to refresh it. Validate against the live source first, running only the review `next_actions` require (no wider re-audit); propose no logic change until validation shows real drift or returns a code whose recovery is a logic change, and put new values or drift in front of the user first. If a refresh fails because the source changed, report what changed (values and counts) and ask; change no closure, diagnostics and hardening included, until the user decides. Before any edit outside `data/` to a published stateful product, and again before capturing, validating or running a closure that differs outside `data/` from the published release (a leftover correction included), run the coverage check: does the source still serve every row the release holds? A source you cannot probe but know serves only a limited window is assumed to serve just that window; one you cannot verify at all is coverage unknown, never full coverage, and a rebuild from empty is not published on a plan approval alone (refresh on the unchanged closure, or ask with that consequence; a total-count check afterward proves nothing, as late rows hide lost ones). If not, say what would be lost and offer only the options that fit why the change exists: a change the refresh can run without is refreshed without; one the user asked for is held and asked about, never dropped; one the refresh needs keeps the current release serving while you ask. Act only on a named choice: "ok", "go ahead", a review or spending approval or a request for fresh numbers never chooses to lose rows, and a plan approval authorizes the logic change but not the loss ([workflow-v2.md § Edits that lose rows](reference/workflow-v2.md#edits-that-lose-rows-on-a-refresh)).
  A behavior-changing revision of a published product also goes in place, on the same workflow ID ([reference/workflow-v2.md § Revise a published product in place](reference/workflow-v2.md#revise-a-published-product-in-place)): before the plan approval, say the next publication replaces the current results
  and rebuilds from empty, losing any rows the source no longer serves (a full re-score for a mapper, with its cost); revise the plan with `reset_workflow` and a replacement blueprint, whose plan starts with that source probe;
  the user's approval of the revised plan authorizes the change, not any row loss (that needs its own named choice). If the supervisor refuses, say in plain words the change can't be applied in place here and offer a separate product (asked first).
  Build a separate versioned product under a new workflow ID only when the user asks to keep the current release unchanged: ask and wait for the yes,
  never call `prepare_workflow` for the new ID in the same turn as the ask, and never fold that authorization into the plan approval.
  After fresh publication, discard cached artifacts/current file, render, re-describe. If caps expire, keep attempt history and report
  impact, state, next action ([user-facing-language.md](reference/user-facing-language.md)); never loop or quit silently.
- **Blocked** — the fix is a ruling only the user can make (a missing rate, an
  ambiguous scope, a measurement no source carries). That is an open question
  found late, not a heal: write it back into `dp-blueprint.md`'s `## Open Questions`
  with what it blocks, which **un-approves** the spec; ask the one smallest
  question and re-enter Step 1b. Never reach green by changing the plan.

## User-facing narration

Own the conversation and use the canonical [user-facing language](reference/user-facing-language.md)
reference for workflow and status wording. Decide technical matters yourself and ask the user only business questions, one at a time with a recommendation ([who decides what](reference/user-facing-language.md#decisions-the-user-owns-and-decisions-you-own)). The user may receive meaningful
progress, approval or clarification requests, blockers, retries, concessions,
and final outcomes. Automatically repaired diagnostics stay internal.

Do not expose internal labels, identifiers, hashes, internal paths, credentials,
or raw tool output. Verified user-facing handles and deliverable paths are
allowed when needed to use or retrieve the result. Preserve ordinary business
terms, including `schema` when it is needed to describe the user's data;
translate implementation framing instead.
If the user asks for technical detail, give only the necessary sanitized explanation.
Query-answer wording and failure classification remain in their current owners. When describing how the build works, build-step words (promise, annotation, recapture, capability, grant, pin, capture, generation) never reach the user, though the user's own business terms keep their names; use the plain replacements in the user-facing language reference. Name Claude Desktop, Nexty, macOS or the spending prompt as the source of a block only when the evidence shows it; never invent a cause, or a reason a run or check failed or did not flag, that the returned diagnostics or verified evidence do not show; see `reference/workflow-v2.md`, Reporting failures and check outcomes.

## Invariants — never violate these

- **Preserve supplied data.** Never modify the original or add raw identifiers. File exports are exact
  copies by default; only exception is a declared projection of unneeded personal data, preserving
  rows/retained values and recording drops, reasons, and both digests. Derive approved non-identifying
  continuity keys in memory before landing; omit the raw identifiers. Treat database and REST API sources
  as **read-only**: never write to them, fabricate a table/endpoint, or narrate a raw credential. A real
  credential is entered only in the native masked prompt when the runtime advertises it;
  the authored service holds explicitly public topology and an opaque local reference,
  never a credential value. `dp-blueprint.md` names field roles only. Derive machine
  slot names from the connector auth scheme; do not ask for values, env-variable names,
  or a credential file. A stored reference is unverified until admitted execution
  fetches the source ([reference/infra-profile-connections.md](reference/infra-profile-connections.md)).
  Legacy literal profiles remain sensitive; share through `export_data_product`
  because its fail-closed redaction is the credential boundary
  ([reference/handoff-export.md](reference/handoff-export.md)).
- **Label every source once there are 2+.** A single-source data product needs no label. With multiple
  sources each gets a short, distinct label used consistently across materialization, inference, and
  generation; two sources of the same connector type sharing an unlabeled or duplicate name is a collision
  nxd-generate-data-product can't resolve for you.
- **Correct data downstream, never upstream.** Cleaning, dedup, amortization, currency normalization,
  reclassification and regrain belong in **derived models computed from the approved landed source** —
  authored by nxd-generate-data-product, landed through the DuckDB output port, asserted in the transform.
  Never edit the user's original source to reach that outcome, never emulate it agent-side.
- **A judgement not in the data is confirmed and landed, not hardcoded.** FX rates, merchant→category and
  similar mappings are surfaced, confirmed, and landed as their own queryable model — never embedded as
  transform constants. **This covers agent-produced judgement too** — a per-entity
  score/verdict/classification read from evidence, landed as data (`status = proposed`, evidence-cited,
  rubric taught first); a baked-in judgement is hardcoded even when weighted. **Which lane judges depends
  on whether the product is packaged** — agent-side CSV while exploring, the field-mapper seam once it
  ships, so the logic travels with the closure and the credential never enters it
  ([reference/inference.md](reference/inference.md)).
- **A supplied procedure with a result-changing gap is read back BEFORE any materialization.** No closure
  directory, source copy, generated code, table, scoring, or build until the user has seen every proposed
  anchor, band and precedence rule and replied. A technical delivery question is not approval; "use your
  judgement" licenses authoring the proposal, not skipping the turn.
- **The plan is a file before it is code.** Every build is preceded by a `dp-blueprint.md` (Step 1b)
  written beside the closure, never inside it, and passed to the generator. A user-supplied value in it is
  encoded verbatim; a value you authored is marked `agent_authored` and named in the read-back; `status:
  approved` is the user's to set, never yours. Run `"$JOB_HELPER_DIR/scripts/validate_dp_spec.py"` after
  the scripts bootstrap before the read-back and again before generating — a validator pass only means
  compilable, never approved. What the user approves is what the generator byte-copies and hashes into the
  closure.
- **A heal changes generated code, never the plan.** The self-heal loop may rewrite `transform/main.py`,
  `models.py` or `spec.py`; it may never edit `dp-blueprint.md` to make a build pass. Narrowing the
  population to dodge a bad join, dropping a model whose grain won't resolve, relaxing a threshold — those
  are spec edits needing re-approval, and the build record catches one mechanically. Escalate instead of
  quietly re-planning.
- **Never claim green over an undisclosed concession, and say `materialized`, never `correct`.** A run
  that reached green by doing something the skills discourage is finished only once the user has heard
  what and why. Green means the approved plan compiled, ran and published — never that the numbers are
  right, and a ruling behind a number is always stated with the number.
- **Keep governed analysis on the supervisor path, and MCP is authoritative when connected.** Discover,
  admit, publish, resume, describe and query through the `nxd-desktop` tools whenever present. Never
  answer a governed local-data question with SQLite, raw SQL, pandas, or a shell pipeline as fallback, and
  never author raw SQL to bypass the semantic layer — a failed MCP build is a reported failure, not
  permission to route around it.
- **Reattach, don't rebuild, when live; keep one workflow ID per data product.** In a fresh session,
  `list_data_products` → `resume_data_product` → static artifact restores the published workflow with a
  fresh bearer; discovery isn't a fallback. Unavailable artifacts don't authorize reconstruction outside
  workflow-v2. A same-logic refresh is a recapture of the same workflow; so is a behavior-changing
  revision, under a freshly approved plan; a new ID only when the user asks to keep the old release ([reference/context-and-resume.md](reference/context-and-resume.md)).
- **Keep workflow-v2 authoring on the main thread.** Pass the returned `capture` action an absolute
  generated-definition path explicitly exposed by the file-writing surface; never infer one from an
  attachment ID or isolated Linux path. Semantic inference, generation, host-path verification, credential
  injection, and every workflow MCP action stay in the owning thread. The only conversation child is the
  mandatory retained-capture review, which receives no credential
  ([reference/scheduling.md](reference/scheduling.md)).
- **Query is by measure/dimension name, and a standing ruling materializes — a filter never enforces
  one.** Ground the NL→selection translation in `describe_models`; `filters[]`, `order_by[]` and `limit`
  are for **per-question scoping only**, never emulated by re-aggregating agent-side. Apply the **Omission
  Test** ([reference/query-grammar.md](reference/query-grammar.md)): if no-filter querying would get a
  *wrong* number the ruling belongs in the transform, and the ruling-bearing measure must be correct
  unfiltered. Landing an `is_transfer` dimension and expecting callers to filter on it is that same silent
  failure wearing a column.
- **The supervisor data dir is off-limits.** Everything under the supervisor's `--data-dir` (its `state/`
  tree) — pinned snapshots in `definitions/<id>/`, `state.sqlite*`, `staging/` — is immutable supervisor-owned state;
  never `chmod`, edit, or hand-write it, and a `.../staging/run-<id>/data.duckdb`
  path inside a pinned `manifest.yaml` is its own resolved runtime path, not a defect. Never list, glob, read, grep or shell into anything under it; the one exception is the exact `review_input` retained paths, where the parent runs only the metadata check [workflow-v2.md](reference/workflow-v2.md) allows. Diagnose a failed validation or run only through `inspect_workflow` then `inspect_run`; an empty `stderr_tail` with a data-dir `log_reference` is a supervisor limitation, not a pointer to follow, so never go looking for `diagnostic.json` ([reference/failure-handling.md](reference/failure-handling.md)). If a served closure
  is wrong, fix **your** source dir and run the workflow again — the supervisor re-pins. Approved rules/code stay pinned; each admitted live-source run refetches source data. When a mapper is part of the approved plan, that run invokes its bound mapper. Querying or reopening a publication alone is not a fresh run; claim freshness only from admitted-run evidence. Pinned state alone does not establish that a refresh requires a new version: use returned runtime capability/state evidence; a behavior-changing revision also stays in place under the rules above.
- **Never offer to skip, bypass or weaken a mandatory gate.** Once validation, review, consent or any other gate is mandatory, say what is needed to pass it or stop; "skip validation" is never an option to offer, even after calling the gate impossible.
- **Bearer only as a tool parameter** — keep it out of narration, never persist or print it. **Never
  present a preview or truncated result as verified data**, and never stall silently.
## Reference docs (this skill)
Use [dp-blueprint](reference/dp-blueprint.md), [build record](reference/build-record.md), [failure handling](reference/failure-handling.md), [user-facing language](reference/user-facing-language.md), [workflow-v2](reference/workflow-v2.md) for mapper budget status and codes, [source materialization](reference/source-materialization.md), [scripts bootstrap](reference/scripts-bootstrap.md), [scheduling](reference/scheduling.md), [context and resume](reference/context-and-resume.md), [inference](reference/inference.md), [handoff export](reference/handoff-export.md), [catalog resources](reference/catalog-resources.md), [query grammar](reference/query-grammar.md), and [dlt](reference/dlt.md) for named details.
