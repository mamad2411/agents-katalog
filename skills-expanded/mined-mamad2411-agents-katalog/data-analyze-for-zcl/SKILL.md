---
name: data-analyze-for-zcl
description: "Xiaohongshu/小红书/千帆 ceramics/tableware export analysis. DuckDB + evidence-scored tasks: weekly_business_review, sku_counterfactual_lift, comment_demand_mining, paid_traffic_efficiency, cover_style_effect, copy_angle_effect, note_funnel, product_opportunity_matrix. Triggers on 笔记数据_/订单数据_/SKU销售_ or columns 笔记ID/曝光量/note_sku_links. Not for generic data analysis or non-XHS platforms unless explicitly invoked."
---

# Xiaohongshu Ceramics Analytics

## When to use

Use this skill when the user provides Xiaohongshu (小红书 / 千帆) exported data files for a ceramics or tableware shop and wants analysis — weekly reviews, content performance, SKU lift, comment mining, paid traffic efficiency, or any task in the menu below. Also use when the user explicitly invokes `data-analyze-for-zcl`. Do not activate for generic data analysis or non-Xiaohongshu platforms.

## Workflow

1. **Resolve skill directory** — locate the bundled runtime under `assets/xhs-ca/`. Do not assume the user has a separate repo checkout.

2. **Authorize multi-agent final report — REQUIRED FIRST GATE** — this is the
   first user-facing action after the skill activates. Before bootstrap, requesting
   exports, building data, running coverage, or producing facts, ask one distinct
   yes/no question authorizing the multi-agent final-report workflow, because **asking is not spawning.**
   If the activating request already explicitly authorizes multiple agents,
   record that answer and do not ask twice. Otherwise, after asking, STOP and wait for
   the reply in a later turn. Silence is not a decline. Authorization permits the
   narrative agents when their briefs are ready; it does not permit changing source
   data or metric mappings. If the user declines, continue later with the deterministic
   final-report fallback rather than producing a separate fact report.
   Once authorized, that decision remains valid for the same report through later turns,
   interruptions, retries, and concurrency limits: do not ask again. Ask for multi-agent
   authorization again only for a separate report after this run finishes or when the
   user explicitly revokes it. A field-mapping decision is a separate semantic question,
   not a reason to repeat this authorization gate.

3. **Bootstrap** — after the authorization answer is recorded, run `scripts/bootstrap`.
   If it fails, read `assets/xhs-ca/references/troubleshooting.md`, surface the relevant
   fix to the user, and stop until the environment is repaired.

4. **Ask for exports** — request the user's Excel/CSV files (e.g. 笔记数据, 订单数据,
   SKU销售, 投放数据) and an optional cover-image folder. Clarify which date range and
   which shop account the files cover only when they cannot be inferred and are required
   to proceed. If file paths are already supplied, use them without asking again. Infer
   the date range from the exports when possible; if the shop name remains unavailable,
   use the neutral `店铺` fallback.

5. **Build** — first run the read-only preflight `scripts/xhs-ca inspect
   <files-or-directories...> --out <state-dir>/inspection.json`. Treat it as provisional:
   verify inferred workbook date range and shop name, file hashes/duplicate groups,
   per-table input/accepted/duplicate/conflict rows, mapping diagnostics, coverage and
   exact next-data-needed. Prefer workbook dates over parent-folder labels and never
   mutate source exports. Then run `scripts/xhs-ca build <files...>`; the formal
   `build_manifest.json` must agree with the inspected source set and inference. A
   mismatch is a blocker, not permission to hand-edit the manifest. If header-mapping fails, read
   `assets/xhs-ca/references/xhs_glossary.md` and
   `assets/xhs-ca/references/data_contract/_index.md`, then inspect the unmapped columns
   through the **字段映射自愈** risk gate below. Keep optional or safely degradable fields
   unmapped; request operator judgment only when that gate says it is genuinely required.
   Resolve the remaining `mapping_diagnostics` rows under that policy before analysis.

6. **Task selection and data quality — coverage-driven, not hand-picked
   (REQUIRED)** — run `scripts/xhs-ca coverage` after the build. Default to every
   **producible** task and record each blocked task's exact next-data-needed. Inspect
   data quality without creating a reader-facing report by running
   `scripts/xhs-ca facts data_quality_check` (plus `ad_data_quality_check` when paid
   traffic data exists) and reading the generated `results.json`. Resolve empty tables,
   missing columns, and mapping diagnostics before continuing by either applying an
   approved mapping or explicitly keeping the field unmapped with Not-judgable and
   next-data-needed. Ask the operator only under the risk gate below. The final report
   folds data quality into **附录：数据质量与口径说明**.

7. **Build internal fact sidecars — REQUIRED, not a deliverable** — run
   `scripts/xhs-ca facts auto`; it executes every producible task in one shot and writes
   `facts.json`, domain-sliced `results.json`, and `sidecar_status.json` without creating
   a fact-layer HTML report. To curate, pass every confirmed slug plus
   `data_quality_check` to one `facts` invocation. Do not run one slug at a time. These
   files are the deterministic evidence and audit layer for the final report, but they
   are internal intermediates. **Do not present or link the internal fact layer to the
   user.** Before narrative work, require both JSON files to share one directory and
   `sidecar_status.json` to be `ready` with the matching `facts_hash`; otherwise stop and
   rebuild. Read every selected task template and `references/cheatsheet.md` before
   interpreting the results.

### 7b. Required (auto-degrading): multi-agent narrative report (host with sub-agents)

Step 2 already recorded the user's authorization choice, and step 7 produced only
internal deterministic sidecars. The merchant-facing report is generated here by the
narrative workflow and is the only default delivery surface:

1. If step 2 was authorized, run `narrative prepare --multi-agent-authorized` with
   step 7's `results.json` and `facts.json`; never hand-build either input. Name the
   report `<店铺名><日期范围>经营诊断报告`. Never lead
   with `千帆`, `小红书`, `XHS`, or `Qianfan` unless it is literally part of the shop
   name. If the shop name is unavailable, use
   `店铺<日期范围>经营诊断报告` as the neutral fallback without asking.
2. Drive the quality-first workflow instead of composing directly. Follow
   `assets/xhs-ca/orchestration/runbook.md` exactly: two independent spine candidates →
   spine adjudication → per-domain writer/challenger/adjudicator → cross-domain synthesis →
   independent visual curation → deterministic gate → three independent review lenses →
   continuity → candidate HTML → merchant final review. Always dispatch the exact pending
   `task_id` values returned by `status --json`. Use each task's `result_path`, `schema_path`,
   enum hints, controller fields, current round, dynamic allowed values and contract version
   as its dispatch contract. Reserve only real capacity, persist dispatch/agent transitions,
   validate each result read-only, then ingest with `--task-id`; never advance over a
   missing sidecar. A cache hit may skip agent work,
   but authorization was still obtained first.
   If agent dispatch hits a concurrency limit, first inspect the already-dispatched
   agents, ingest their finished results to release controller capacity, and close or
   recycle completed host agents to release host capacity. Then retry pending tasks with a
   smaller batch or serially. `record-agent-state --status closed` is only a controller-ledger
   compatibility call after successful ingest; it does not close a host agent. Concurrency limits are
   transient scheduling pressure: they must not trigger `unsupported`, deterministic
   fallback, report degradation, or another user authorization prompt.
3. If step 2 was declined, prepare with `--multi-agent-declined`, then run
   `xhs-ca narrative finalize-deterministic --run-dir <dir> --reason denied`. If the
   host truly has no sub-agent facility, use `--multi-agent-unavailable` and reason
   `unsupported`. Gate exhaustion may route to the same deterministic fallback. An HTML
   render failure is `delivery_failed`: report the exact error and do not claim that a
   fallback file exists. A successful fallback is explicitly labeled `确定性骨架版`.

Both paths produce internal Markdown plus exactly one user-facing single-file HTML report.
The run directory, Markdown, facts, results, and status files are durable audit
state, not deliverables unless the user explicitly requests them.

The narrative report carries **agent-curated deterministic visuals**. There is no
per-domain quota and no per-domain cap: retain every view that materially proves a
decision-relevant claim, but do not add a table or chart merely because a source table
exists. The agent only curates
the *view* — which source table, which columns/rows, and the captions; a
deterministic engine fills every displayed number from the already-computed fact
layer, so the values stay reproducible and trustworthy while the agent decides only
what the visual looks like. The deterministic renderer may add a useful fallback chart
when a section has chartable data but no retained chart. If chartable data existed yet
no chart reached the HTML at all, `finalize` records
`degradation_reason=visuals_missing` — surface that in the step-10 summary rather
than presenting a silently prose-only narrative as complete.

Every decision-critical claim must have one structured `visual_coverage` record.
Retained records name real, matching and renderable `view_id` values; omissions use an
allowed reason code plus a specific reason. Gate/review removals become
`dropped_by_gate`/`dropped_by_review`, never a silent empty list. Every retained view
appears exactly once in final HTML as an escaped `data-view-id`.

The single HTML must also retain a deterministic **经营诊断明细** layer for available,
non-empty high-value search-term, content/note, SKU, channel, audience and refund tables.
Curated-view rejection must not erase those merchant-useful diagnostics. Long tables may
be capped/folded, and numeric columns may sort interactively using embedded deterministic
sort ranks; sorting must remain offline and must not expose unformatted source ratios.

The final report must replace a vague “暂时答不了的问题” section with deterministic
**缺哪些数据，补齐后能分析什么** derived from `blocked_modules`. Merge blocked tasks that require
the same data package, then state (1) what data to provide, (2) the minimum recommended
fields/content, and (3) which analyses become available afterward. Never expose internal
task slugs or raw table identifiers. Write for a non-specialist merchant: prefer everyday
Chinese and expand unavoidable abbreviations on first use, such as `成交额（GMV）` and
`规格编号（SKU）`. `cannot_say` remains an internal safety boundary and must not be rendered
as the merchant-facing data request.

Split that module into two reader-facing layers. **当前缺失数据** comes from blocked tasks.
**可选增强数据** may list only capabilities already implemented by the task registry when
deterministic result fields or the source-table inventory prove that the optional input is absent.
An existing field whose real value is zero is not missing. Capability wording must stay narrow:
`to_live_count` and `to_live_gmv` support笔记引流直播间访问/成交分析，但不代表系统已支持
独立的直播总览、直播间停留或直播商品漏斗；不得承诺后者。

8. **Custom integrated reports** — only when the data falls outside the built-in task
   registry: write the internal Markdown source, then render one final HTML with
   `scripts/xhs-ca render-html <report.md>`. For built-in tasks, use step 7's single
   `facts` invocation and step 7b rather than hand-authoring. Companion tables remain
   internal unless the user explicitly requests them.

9. **Delivery verification (REQUIRED, one HTML only)** — the user receives exactly one
   user-facing single-file HTML report from `finalize`, `render-frozen`, or the explicit
   deterministic skeleton fallback. Confirm it exists under
   `.xhs-ceramics-analytics/outputs/`, its filename starts with the shop/store name or
   neutral `店铺` fallback, and no platform name leads it. Do not present sidecars,
   Markdown, data-quality inspection output, or a fact-layer HTML as additional
   deliverables. Unless the run records `degradation_reason=visuals_missing`, verify the
   final HTML contains a useful chart when chartable evidence exists. Verify exact
   `<title>` and unique `<h1>`, zero unresolved `{tN}`, zero external resource dependency,
   and one `data-view-id` marker for every retained view. The merchant-reviewed candidate
   bundle/HTML hashes must match the final artifact, and the production directory must
   contain exactly one HTML. An unrelated fallback SVG does not clear a recorded
   critical-claim omission. A prose-only finalized report without the proper degradation
   reason is a defect. If rendering fails, report the exact error; do not silently
   substitute Markdown.

10. **Summarize** — present findings with evidence tier, key numbers, report caveats,
    next-data-needed, recommended action, narrative workflow status, and the one final
    HTML path. Do not mention the internal facts report unless the user asks for an audit
    artifact. If `degradation_reason=visuals_missing`, state it plainly. NEVER claim
    deterministic note-to-order attribution.

## 字段映射自愈 (Field-mapping self-heal)

The build never rejects a file for a drifted Chinese header — it degrades and records the gap. After every `xhs-ca build`, adjudicate the gaps before analysis:

1. **Read the audit and diagnostics.** Query `mapping_audit` first (`canonical_column,
   source_column, match_method, match_score, platform_metric_ids, semantic_status,
   applied, reason`), then `mapping_diagnostics`. Every attempted mapping is auditable;
   `mapping_diagnostics` contains only unresolved or quarantined fields.
2. **Judge each row, caliber-aware.** `verified` means an accepted platform binding;
   `reference_only` means the official definition agrees with the target but the binding
   is not approved; `operator_confirmed` came from `mapping_overrides.yaml`;
   `no_platform_reference` means the shipped exact alias has no catalog coverage.
   `review_required` means an automatic fuzzy match was quarantined and not projected;
   `conflict` means the platform definition contradicts the proposed target and is also
   not projected. **口径不可混淆:** `（支付时间）`/`_pay` and
   `（退款时间）`/`_refundtime` are different calibers. `missing` means genuinely absent;
   `ambiguous` means unmatched wording remains.
3. **Risk gate (hybrid).**
   - *Platform table fuzzy/conflict* — never auto-approve. Compare the official definition,
     unit, grain, PV/UV basis, and payment/refund time basis, then obtain operator
     confirmation before writing an override.
   - *Missing / caliber-uncertain / multiple candidates* — do not invent a mapping;
     leave the field unmapped and continue with Not-judgable plus exact next-data-needed
     whenever that is safe. Ask the operator only when a mapping decision is genuinely
     required to proceed or would materially change a metric or report conclusion.
     That question must provide a complete decision packet: source file and sheet,
     source header and representative sample values, candidate canonical fields and
     their official definitions, unit, grain, aggregation, PV/UV and payment/refund-time
     differences, mapping method/score/conflict reason, affected tasks and conclusions,
     and a recommended option with rationale. Always offer `leave unmapped` as an
     explicit choice. Never ask a bare “how should this field map?” question.
4. **`mapping_overrides.yaml` format** (lives in the state dir next to `analytics.duckdb`; overrides only ADD aliases, never remove a shipped one):
   ```yaml
   refund_overview:
     refund_users:
       - 退款人数合计
   business_overview_daily:
     net_gmv_pay:
       - 退款后金额
   ```
5. **Re-build.** Re-running `xhs-ca build` applies the learned alias deterministically; the column becomes canonical and marts see it. The judgment is frozen — identical `(export, overrides)` always produces the identical build.

### 平台字段目录的使用边界

When a diagnostic contains an unfamiliar Xiaohongshu metric name, a stable numeric
metric ID, or a definition/caliber ambiguity, load
`assets/xhs-ca/references/platform/xhs_metric_catalog.yaml`. Use it to understand the
platform definition, grain, time basis, unit, aggregation, formula, and known review
risks. `xhs_metric_promotion_review.csv` is a review queue: `proposed` means a candidate
only, never an approved mapping.

For `business_overview_daily`,
`assets/xhs-ca/references/platform/xhs_business_overview_binding_review.csv` is review
evidence only. It records evidence-backed suggestions and blockers from a completed
review pass, but `approve` is not an accepted binding and `runtime_action=none` means it
must not change import behavior.

Only an accepted row in
`assets/xhs-ca/references/source_bindings/xhs_platform_metrics.yaml` may act as an
approved platform-to-canonical reference. Runtime consumption declares
`runtime_mode: observe` and `runtime_scopes: [agent_context]`: accepted definitions and
exact-name, unapproved candidates are copied into `mapping_audit`, `facts.json`,
`results.json`, and narrative briefs. Runtime effect is
`automatic_header_mapping: validation_gate`: platform-table fuzzy matches and semantic
conflicts are quarantined before projection. Candidates remain `mapping_permission: none`;
they may explain or challenge a mapping but cannot approve one. The catalog does not
alter raw values, calculations, evidence, or task coverage.
Never add an override from display-name equality or tooltip proximity, or from a
proposed row alone. The payment/refund time basis, PV/UV grain, unit, and aggregation
must all match.

### 报表指标语义注册表

`assets/xhs-ca/references/metrics/registry.yaml` is the report-facing metric ontology.
It defines stable metric identity, display names, formulas, source/output grain,
daily-distinct scope, and permitted window aggregation. It is not an import mapping
and cannot approve a raw header or platform-to-canonical binding.

The registry runtime is validation-gated and limited to fact annotation. Unique facts
keep `task_id.key`; repeated keys receive a deterministic finding scope shared by the
FactBook, narrative results, and HTML. Only an exact, semantically compatible binding
whose `legacy_contracts` entry still pins unit/caliber/aggregation/grain may expose
registry name and formula. Repeated occurrences never inherit an unscoped legacy
binding; each needs an explicit scoped binding. Unmapped or rejected facts remain valid
and are listed in mapping diagnostics. Dynamic winners (for example, the dominant
carrier/refund stage or top audience member) stay unmapped until their selected
dimension is explicit. HTML may use validated names, rendered values, and units for
mapped key numbers, but keeps definitions in hover/focus tooltips and never prints the
HAR/platform field catalog into the report.

## Commands

```bash
# Check environment health
<skill-dir>/scripts/xhs-ca doctor

# Build database from multiple export files
<skill-dir>/scripts/xhs-ca build notes.xlsx orders.xlsx skus.xlsx

# Read-only provisional inspection before build
<skill-dir>/scripts/xhs-ca inspect <files-or-directories...> --out <state-dir>/inspection.json

# Build with comments only
<skill-dir>/scripts/xhs-ca build comments.xlsx

# See which tasks the built data can actually produce vs what's blocked (+ why)
<skill-dir>/scripts/xhs-ca coverage

# Internal fact sidecars only; no fact-layer HTML is generated.
<skill-dir>/scripts/xhs-ca facts auto

# Same internal fact build, explicitly curated in one invocation.
<skill-dir>/scripts/xhs-ca facts core_business_diagnosis demand_funnel_diagnosis search_efficiency_diagnosis channel_structure_diagnosis audience_structure_diagnosis refund_root_cause_diagnosis note_commercial_diagnosis sku_structure_diagnosis data_quality_check

# Inspect data quality internally during the 字段映射自愈 gate.
<skill-dir>/scripts/xhs-ca facts data_quality_check

# Prepare the authorized quality-first merchant report from the validated sidecar pair.
<skill-dir>/scripts/xhs-ca narrative prepare --run-dir <run-dir> --results <state-dir>/results.json --facts <state-dir>/facts.json --name 店铺名日期范围经营诊断报告 --multi-agent-authorized

# Durable dispatch loop: reserve -> record -> validate -> ingest
<skill-dir>/scripts/xhs-ca narrative reserve --run-dir <run-dir> --capacity <n> --json
<skill-dir>/scripts/xhs-ca narrative record-dispatch --run-dir <run-dir> --task-id <task_id> --agent-id <agent_id> --result-path <file>
<skill-dir>/scripts/xhs-ca narrative record-agent-state --run-dir <run-dir> --task-id <task_id> --status result_ready
<skill-dir>/scripts/xhs-ca narrative validate --run-dir <run-dir> --stage <stage> --task-id <task_id> --source <file> --json
<skill-dir>/scripts/xhs-ca narrative ingest --run-dir <run-dir> --stage <stage> --task-id <task_id> --source <file>

# Explicit-decline fallback: initialize deterministic-only state, then render one HTML.
<skill-dir>/scripts/xhs-ca narrative prepare --run-dir <run-dir> --results <state-dir>/results.json --facts <state-dir>/facts.json --name 店铺名日期范围经营诊断报告 --multi-agent-declined
<skill-dir>/scripts/xhs-ca narrative finalize-deterministic --run-dir <run-dir> --reason denied

# Convert a custom Markdown/integrated report into single-file HTML
<skill-dir>/scripts/xhs-ca render-html .xhs-ceramics-analytics/outputs/经营诊断报告.md
```

## Files this skill loads on demand

- **assets/xhs-ca/references/cheatsheet.md** — always loaded before summarizing (evidence tiers, metrics, report contract).
- **assets/xhs-ca/references/task_menu.md** — loaded at step 6 to explain producible and blocked tasks.
- **assets/xhs-ca/references/xhs_glossary.md** — loaded at step 5 only when header mapping fails.
- **assets/xhs-ca/references/data_contract/\<table\>.md** — loaded only when a schema question arises or build reports missing columns.
- **assets/xhs-ca/references/platform/xhs_metric_catalog.yaml** — loaded only for Xiaohongshu platform-definition, grain, time-basis, unit, formula, or stable metric-ID questions.
- **assets/xhs-ca/references/platform/xhs_metric_promotion_review.csv** — review queue only; `proposed` rows are not mappings.
- **assets/xhs-ca/references/platform/xhs_business_overview_binding_review.csv** — review evidence only for the first `business_overview_daily` candidate batch; suggestions are non-executable.
- **assets/xhs-ca/references/source_bindings/xhs_platform_metrics.yaml** — approved platform-to-canonical references consumed only as agent context.
- **assets/xhs-ca/references/metrics/registry.yaml** — validated report-facing metric ontology; observation-only runtime fact annotation.
- **assets/xhs-ca/task_templates/\<slug\>.md** — loaded before summarizing that specific task's output.
- **assets/xhs-ca/references/troubleshooting.md** — loaded only when bootstrap or doctor fails.

## Rules

1. **No deterministic attribution** — do not claim note-to-order causation unless explicit `note_sku_links` source data supports it. Inferred links produce at most Weak evidence.
2. **Every conclusion carries an evidence tier** — one of Strong, Medium, Weak, or Not-judgable with justification. Omitting the tier violates the report contract.
3. **Missing tables produce not-judgable + next-data-needed** — never fabricate numbers or force an analysis when required data is absent.
4. **Weak evidence = hypothesis, not recommendation** — Weak findings must not appear as "recommended action" without an explicit upgrade path stated.
5. **Prefer DuckDB and bundled tasks** — use `scripts/xhs-ca facts` plus the narrative workflow over ad-hoc Python/SQL scripts. The bundled tasks enforce evidence scoring, report structure, and metric definitions consistently.
6. **Never mention troubleshooting steps preemptively** — only surface repair commands from `assets/xhs-ca/references/troubleshooting.md` when bootstrap or doctor actually fails.
7. **Do not invent metrics** — all metrics in reports must trace back to `assets/xhs-ca/references/metric_definitions.md` (consolidated in cheatsheet). If a metric is needed but absent, flag it rather than fabricating a formula.
8. **HTML is the final deliverable surface** — deliver exactly one final HTML report.
   Fact sidecars, deterministic inspection output, and Markdown remain internal unless
   the user explicitly asks for audit/source artifacts. Markdown-only delivery is
   incomplete unless HTML rendering failed and the failure was explicitly reported.
