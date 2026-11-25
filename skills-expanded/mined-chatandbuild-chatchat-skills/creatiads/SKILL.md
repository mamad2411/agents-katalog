---
id: creatiads
name: creatiads
description: "TikTok MCP-first advertising orchestrator with 8-step analysis workflow. Use when the user asks colloquially to list/查看广告账户或campaign (\"我有哪些广告账户\", \"列出campaign\", \"看看我的广告\", \"有哪些账户\"), find top/worst performers (\"哪个广告效果最好\", \"表现最好的campaign\", \"最差的广告\", \"浪费预算的广告\", \"best/worst performing ads\", \"top campaigns\"), or wants to inspect, plan, launch, diagnose, report, or optimize — including daily pulse/日报/weekly report/周报, vertical/user type classification/垂类诊断, creative fatigue analysis/创意素材分析, audience optimization/受众分析, landing page & W2A path/落地页分析, budget & bid/预算出价优化, measurement & SKAN attribution/归因分析, activity changelog/操作记录, cross-account rebuild/账户迁移, error & review handling/审核报错诊断, or generate HTML reports/出报告/生成报告. Also use for any of 13 verticals: ecommerce, short_drama/短剧, utility_or_w2a/工具, casual_game/休闲游戏, midcore_or_hardcore_game/中重度游戏, novel/小说, social/社交, entertainment/泛娱乐, financial_leads/金融借贷, search_arbitrage/搜索套利, earnings_or_offerwall, regulated_high_risk, agency_or_mixed/代理商. Covers TikTok, Smart+, TikTok One, GMV Max/Product GMV Max/TikTok Shop reports, Pangle, Spark Ads, carousel ads, catalog/shop ads, creative previews, product catalogs, pixels, audiences, and campaign performance. Uses L1 dispatcher for 80%+ tools; scripts are compute-only. Must initialize the remote MCP server before any platform API operation and use MCP tools as the default data plane."
category: TikTok
homepage: https://www.creatiads.com/
metadata:
  {
    "openclaw":
      {
        "emoji": "ads",
        "requires": {
          "mcp": ["tiktok-mcp"]
        }
      }
  }
---

# Creatiads

Creatiads is the MCP-first orchestration layer for TikTok advertising work. It owns strategy,
delivery planning, asset and catalog operations, reporting, review, and optimization while routing all
platform data access through the remote TikTok MCP server.

版权与温馨提示 / Copyright notice: see [copyright-notice](references/copyright-notice.md).

## Initialization Gate

Before any TikTok API operation, read [mcp-initialization](references/mcp-initialization.md) and
ensure the TikTok MCP is installed, enabled, and authorized.

Default servers:

| Platform | Server name | Remote URL |
| --- | --- | --- |
| TikTok | `tiktok-mcp` | `https://business-api.tiktok.com/open_mcp/tt-ads-mcp-layer` |

Rules:

- Match existing servers by URL first. Reuse a user-created server name if the URL already exists.
- Add a missing server with `codex mcp add <name> --url <remote-url>`.
- Start OAuth with `codex mcp login <name>` when authorization is required.
- Never print tokens, authorization headers, OAuth callback secrets, or MCP session metadata.
- If TikTok MCP is not callable after initialization, stop the task and return a structured unavailable result.

## Platform Routing

- TikTok, Smart+, TikTok One, GMV Max, identity, music, creative asset, and advertiser requests use the TikTok MCP adapter.
- If the platform is unclear and the request is not TikTok-related, explain that this skill is TikTok-only.
- For GMV Max / TikTok Shop / Product GMV Max reports, use the dedicated GMV Max workflow in
  [gmv-max-reporting](references/gmv-max-reporting.md). A GMV Max-first account may have empty regular
  auction campaign/adgroup/ad/activity sources; that is not a degradation when GMV Max sources are present.

## Analysis Workflow: User Type First

**This is the mandatory sequence for every report, diagnosis, or analysis task.**
Never skip user type classification or metric preset selection — they determine which
metrics to pull, which vertical sections to include, and how to interpret the numbers.

For repeatable work, generate an agent-native MCP task plan first. Use the
`creatiads/scripts/plan_*.py` entrypoints to write `pull_plan.json` and
`mcp_tasks.jsonl`; the agent executes those native MCP tasks and saves raw results.
Python scripts must not create their own MCP/OAuth clients or call Motata CLI.

### The 8-Step Sequence

```
1. MCP READY     → Ensure tiktok-mcp MCP is initialized and authorized
2. ACCOUNT INFO  → Pull advertiser details (timezone, currency, status)
3. CLASSIFY SEED → Pull only minimal current-window evidence for classification
4. USER TYPE     → Write user_type.json from advertiser, ad, app, landing, catalog/shop evidence
5. METRIC PRESET → Write metric_preset.json from user_type.json
6. REPORT DATA   → Pull current/previous formal reports with the selected metric set
7. ENRICHMENT    → Pull audience breakdowns, creative previews, landing paths, activities
8. HTML + AUDIT  → Produce analysis, HTML, and audit
```

**Step 3 is not the formal report data pull.** It may use a tiny current-window seed
(`classification_campaigns`, `classification_adgroups`, `classification_ads`,
`classification_ad_v2_insights`, app/catalog/shop/Smart+ evidence) only to classify the
advertiser. Formal `current_*`, `previous_*`, audience, creative, activity, and metric probe
sources must wait until `user_type.json` and `metric_preset.json` exist.

**Formal MCP report sources must be complete candidate pools.** Do not write top-row
samples as `current_campaigns`, `current_adgroups`, `current_ads`, `current_ad_v2_insights`,
or previous-period equivalents. Use MCP pagination/page sizes large enough to materialize
every row TikTok reports for that level, and merge all pages before report generation.
If `page_info.total_number > row_count` or `page_info.total_page > 1`, the audit must fail
until the missing pages are pulled. Also pull `current_advertiser_insights.json` and
`previous_advertiser_insights.json`; these one-row advertiser reports are the KPI totals,
while campaign/adgroup/ad/ad_v2 rows are driver pools.

**Step 4 must run before Step 5, and both must run before Step 6.** The user type determines
which metrics to pull, which HTML sections to include, what counts as "good" CPA, and what
caveats apply.

### Account Vertical Cache

Do not re-classify the same advertiser on every analysis run. When an account-level profile cache
exists and is still fresh, reuse its `user_type.json` and `metric_preset.json` instead of pulling
classification seed data again. The default cache TTL is 14 days.

After a fresh vertical classification, list the complete recommended metrics in both Chinese and
English and ask the user whether anything should be added or adjusted. If the user adds metrics,
run one metric probe/data-pull test for those additions first. Write the account profile cache only
after the added metrics are returned as active or supported-empty; otherwise keep the run uncached
and report the failed metric names.

For creative, ad, audience, activity, budget, bottleneck, landing/app, and performance diagnosis,
always include the account vertical context and metric preset. Creative/material and ad analysis must
rank and explain results through the cached or freshly classified vertical metric lens, not just generic
spend/click/conversion totals.

### Step 4: User Type Classification

Collect evidence from the current-period data:
- Campaign names, objective types, automation types
- Ad names, ad texts, CTAs
- Landing URLs, app IDs, store URLs
- Advertiser name, industry
- Catalog/shop presence

Classify into one of 13 types using keyword scoring (spend-weighted, domain hints,
app-store detection):

| Type | Key Signals | Metric Focus |
|---|---|---|
| `ecommerce` | shopify, amazon, product URLs, catalog, shop | shop metrics, ROAS, add-to-cart |
| `short_drama` | drama, 短剧, reelshort, 王妃, 重生 | value/ROAS, IAP, creative retention |
| `utility_or_w2a` | SaaS, 工具, 批量, 管理, ad management tools | conversion, app install, CTR |
| `casual_game` | puzzle, match, casual, hypercasual | app install, retention, CPI |
| `midcore_or_hardcore_game` | rpg, strategy, mmo, 传奇, 原神 | IAP value, ROAS, retention |
| `novel` | novel, 小说, reader, 阅读 | value, reading-time, install |
| `social` | dating, chat, social, live | messaging, engagement, install |
| `entertainment` | streaming, media, video, music | engagement, retention |
| `financial_leads` | loan, credit, finance, insurance | lead, form, conversion |
| `search_arbitrage` | multi-vertical, high-CTR, content farm | CTR, CPC, impression volume |
| `earnings_or_offerwall` | earn, reward, cash, offerwall | install, engagement |
| `regulated_high_risk` | casino, bet, gambling, 赌 | value, conversion (limited) |
| `agency_or_mixed` | 3+ types with meaningful scores | all groups — full probe |

Write `user_type.json` with `top_type`, `confidence` (high/medium/low),
`evidence` array, and `data_gaps`.

### Step 5: Metric Preset Selection

Map the top user type to metric groups:

```
ecommerce                → [core, conversion, value, shop, creative_video]
short_drama              → [core, conversion, value, creative_video, app]
utility_or_w2a           → [core, conversion, app, creative_video]
casual_game              → [core, conversion, value, app, creative_video]
midcore_or_hardcore_game → [core, conversion, value, app, creative_video]
novel                    → [core, conversion, value, creative_video, app]
social                   → [core, conversion, lead, app]
entertainment            → [core, conversion, creative_video, app]
financial_leads          → [core, conversion, lead]
search_arbitrage         → [core, conversion]
earnings_or_offerwall    → [core, conversion, lead]
regulated_high_risk      → [core, conversion, value]
agency_or_mixed          → [core, conversion, value, app, shop, lead, creative_video]
```

Each group expands to specific TikTok metric names (see `metric_probe.py` BASE_METRICS).
Write `metric_preset.json` with `{user_type, derived_user_type, groups[], metrics[],
source_user_type_hash}`. `source_user_type_hash` must match the current `user_type.json` so
the audit can prove the preset was selected after classification.

**At depth standard**, skip the formal metric probe — use the preset to guide which
additional metrics to pull in Step 6 enrichment. **At depth full/deep**, run the metric
probe to classify each recommended metric as active/supported_empty/unsupported.

### Step 6: Enrichment (depth-dependent)

`quick` is accepted as an alias for `fast`. Keep the source contract aligned with
Motata's quick/standard/full/deep behavior:

| Source | quick/fast | standard | full | deep |
|---|---|---|---|---|
| Current advertiser/campaign/ad reports | yes | yes | yes | yes |
| Current ad group reports | no | yes | yes | yes |
| Previous advertiser/campaign reports | yes | yes | yes | yes |
| Previous ad group/ad reports | no | yes | yes | yes |
| Current `ad_id_v2` report | yes | yes | yes | yes |
| Audience country | yes | yes | yes | yes |
| Audience age/gender | no | yes | yes | yes |
| Audience placement | no | yes | yes | yes |
| Audience device/platform | no | no | yes | yes |
| App summary | no | yes | yes | yes |
| Landing/app path analysis | yes | yes | yes | yes |
| Top campaign/adgroup/ad structure | no | top 30 | top 60 | all pages |
| Smart+ ad details (<=50/batch) | yes | yes | yes | yes |
| Creative previews (embed <img>) | no | yes | yes | yes |
| Creative retention (derived) | no | yes | yes | yes |
| Targeted activity changelog and factors | yes | yes | yes | yes |
| Advertiser-wide changelog | no | no | no | yes |
| Blocking errors / review | no | no | no | yes |
| Metric probe | no | no | yes | yes |

### Step 8: HTML Generation Rules

The report HTML must include these sections (at minimum):

1. **Status bar** — overall status (normal/watch/urgent) with reason
2. **KPI snapshot** — current vs previous period with deltas
3. **Campaign leaderboard** — ranked by spend, CPA highlighted
4. **Audience breakdown** — country, age×gender, placement, platform
5. **Creative preview** — embedded `<img>` tags and `<a>` links (NOT text labels)
6. **Activity changelog** — key operational events (budget/bid/targeting changes)
7. **Next actions** — P0/P1/P2 priority with specific entity IDs
8. **Data quality** — source status table with row counts and method notes

For the full HTML contract, see [report-contract](references/report-contract.md).

## Execution Path: L1 Dispatcher First

**80%+ of TikTok MCP tools are L1-only** — they require `tool_execute` to reach.
Do NOT assume a tool is unavailable just because it's not listed as a direct MCP function.

### Report KPI Exception

`report_integrated_get` is the canonical KPI and audience report path. For formal
`current_*`, `previous_*`, `ad_v2`, audience, metric probe, and activity-targeted insight
report rows:

- Call the direct MCP report tool only.
- Do not use `tool_execute`, `tool_get`, `tool_list`, direct HTTP, curl, or Motata data.
- Do not retry a formal KPI source with lean metrics unless the task retry ladder explicitly
  reaches that fallback. Record the fallback reason in `attempts`.
- If a direct report response is large, recover the full JSON from the subagent MCP event log
  (`mcp_tool_call_end`) instead of trusting truncated chat transcript text.

### Resolution order for every tool call:

1. **Try L0 direct** first (e.g. `mcp__tiktok-mcp__smart_plus_ad_get`)
2. **If "unknown tool" or `structured_unavailable`**, immediately fall back to L1 dispatcher:
   `mcp__tiktok-mcp__tool_execute(tool_name="ExactL1ToolName", params={{...}})`
3. **Only if both fail**, mark the source as `structured_unavailable`

### L0 tools (direct call — no dispatcher):

Smart+ CRUD: `smart_plus_campaign_get`, `smart_plus_adgroup_get`, `smart_plus_ad_get`
and their Create/Update/Status variants. Plus: `report_integrated_get`, `advertiser_info_get`,
`app_list_get`, `pixel_list_get`, `page_get`, `identity_get`, `file_image_ad_search`,
`smart_plus_material_report_overview_run`, `smart_plus_material_report_breakdown_run`,
`smart_plus_ad_preview`.

### Critical L1-only tools (require `tool_execute`):

| L1 Tool | Purpose |
|---|---|
| `ad_get`, `adgroup_get`, `campaign_get` | Regular (non-Smart+) entity detail |
| `file_image_ad_info_get`, `file_video_ad_info_get` | **Image/video preview URLs** |
| `tt_video_list_get`, `tt_video_info_get` | **Spark Ad posters and previews** |
| `changelog_task_create` → `changelog_task_check` → `changelog_task_download` | Activity changelog |
| `ad_review_info_get`, `adgroup_review_info_get` | Blocking errors |
| v2 no `new_name` for media upload | Media upload currently unavailable in v2 MCP |
| All audience, targeting, BC, GMV Max, creative portfolio tools | Discovery and management |

For activity changelog, first verify the exact L1 tool names with `tool_list`/`tool_get`.
If changelog/activity-log tools are not exposed in the current TikTok MCP server, write
`activity_changelog.json` as `structured_unavailable` with every attempted tool and error.
Then derive `activities`, `activity_targeted_insights`, `activity_daily_breakdown`, and
`activity_factors` from that unavailable source so the report can finish with explicit
degradation instead of hanging.

### Creative Preview HTML Rule

When preview URLs are resolved, they **MUST** be embedded in HTML as real `<img>` tags and
clickable `<a>` links. Never output bare text like "inline_image" in place of actual media.
The URL IS the preview. Before marking a report complete, verify at least one `<img>` tag
appears in the creative preview section.

## Task Routing Matrix

When the user asks for analysis, route to the correct workflow by intent:

| User Intent | Trigger Keywords | Follow |
|---|---|---|
| Daily pulse / snapshot | "日报", "daily pulse", "today", "昨天" | [tiktok-report-runner](references/tiktok-report-runner.md) + 8-step sequence above |
| Weekly report | "周报", "weekly report", "这周", "上周" | [tiktok-report-runner](references/tiktok-report-runner.md) + 8-step sequence above |
| User type / vertical diagnosis | "这是什么垂类", "what vertical", "账户类型" | [tiktok-analysis-playbooks](references/tiktok-analysis-playbooks.md) § Advertiser Type |
| Metric capability / preset | "有哪些指标", "metrics probe", "指标探测" | [vertical-metric-playbooks](references/vertical-metric-playbooks.md) |
| Audience diagnosis | "受众", "audience", "targeting" | [audience-optimization](references/audience-optimization.md) |
| Creative / video fatigue | "创意", "素材", "creative fatigue", "疲劳" | [creative-analysis](references/creative-analysis.md) |
| GMV Max / TikTok Shop report | "GMV Max", "Product GMV Max", "TikTok Shop", "商品周报", "店铺周报" | [gmv-max-reporting](references/gmv-max-reporting.md) |
| Landing page / funnel | "落地页", "landing page", "W2A", "app path" | [landing-page-and-funnel](references/landing-page-and-funnel.md) |
| Budget / bid optimization | "预算", "出价", "budget", "bid", "scale" | [budget-and-bid-optimization](references/budget-and-bid-optimization.md) |
| Measurement / attribution | "归因", "attribution", "SKAN", "measurement" | [measurement-and-attribution](references/measurement-and-attribution.md) |
| Cross-account rebuild | "迁移", "rebuild", "clone", "复制账户" | [tiktok-validation-and-rebuild](references/tiktok-validation-and-rebuild.md) |
| Error / degradation handling | "报错", "error", "permission denied", "degraded" | [error-cache-degradation](references/error-cache-degradation.md) |
| Formal HTML report | "出报告", "生成报告", "report", "HTML" | [report-contract](references/report-contract.md) + [report-validation](references/report-validation.md) |

## Reference Map

- MCP setup and auth: [mcp-initialization](references/mcp-initialization.md)
- Tool call rules and adapter contract: [mcp-data-plane](references/mcp-data-plane.md)
- TikTok tool mapping: [tiktok-mcp-tool-map](references/tiktok-mcp-tool-map.md)
- TikTok tool parameters and enum values: [tiktok-tool-parameters](references/tiktok-tool-parameters.md)
- TikTok interface parity: [tiktok-cli-sdk-mcp-parity](references/tiktok-cli-sdk-mcp-parity.md)
- TikTok operation parity map: [tiktok-operation-map](references/tiktok-operation-map.md)
- TikTok analysis playbooks: [tiktok-analysis-playbooks](references/tiktok-analysis-playbooks.md)
- Vertical metric playbooks: [vertical-metric-playbooks](references/vertical-metric-playbooks.md)
- Vertical report templates: [vertical-report-templates](references/vertical-report-templates.md)
- Audience optimization: [audience-optimization](references/audience-optimization.md)
- Creative analysis: [creative-analysis](references/creative-analysis.md)
- TikTok creative preview resolution: [tiktok-creative-preview-resolution](references/tiktok-creative-preview-resolution.md)
- GMV Max reporting: [gmv-max-reporting](references/gmv-max-reporting.md)
- Landing page and funnel: [landing-page-and-funnel](references/landing-page-and-funnel.md)
- Budget and bid optimization: [budget-and-bid-optimization](references/budget-and-bid-optimization.md)
- Measurement and attribution: [measurement-and-attribution](references/measurement-and-attribution.md)
- Error, cache, and degradation policy: [error-cache-degradation](references/error-cache-degradation.md)
- TikTok report runner: [tiktok-report-runner](references/tiktok-report-runner.md)
- TikTok validation and rebuild: [tiktok-validation-and-rebuild](references/tiktok-validation-and-rebuild.md)
- Reports and artifacts: [report-contract](references/report-contract.md)
- Report validation and audit: [report-validation](references/report-validation.md)

## Safety Rules

- Prefer read-first workflows.
- For create, update, activate, delete, share, budget, or status changes, read the target object first, summarize the intended payload and risk, and get explicit user approval before acting.
- Create new campaigns, ad groups, and ads in paused or disabled state by default.
- Activation is a separate approval step and must not be bundled with creation.
- Distinguish `unsupported`, `supported_empty`, `permission_denied`, `rate_limited`, `partial`, and `degraded` in results.
- Do not use non-MCP data sources unless the user explicitly asks for an external fallback.

## Reporting

For substantive analysis or client-facing output, materialize MCP data under:

```text
build/creatiads_runs/<platform>_<account_or_advertiser>_<period>_<depth>_<until>/
```

Read [report-contract](references/report-contract.md) before generating reports.

For TikTok reports, also read [tiktok-report-runner](references/tiktok-report-runner.md) and follow its
mandatory source order. A matching existing run directory is not evidence that the current task is done:
after skill, mapping, or MCP parity changes, run the MCP pulls again and overwrite or version the run
artifacts with a fresh `generated_at`. Reuse old artifacts only when the user explicitly asks for cached
inspection.

Before pulling formal report data, writing analysis, or writing HTML, the report run must first produce
`user_type.json` from current MCP classification evidence for the requested advertiser and date window.
Then write `metric_preset.json` from that exact user type. Use the preset to choose the formal metric set,
probe plan, vertical sections, caveats, and action logic.

### Scripts — Compute-Only (never make MCP calls)

All Python scripts have been refactored to accept MCP data as input and do pure computation.
**Scripts never call MCP tools.** The agent always makes MCP calls and passes results to scripts.

| Script | Input | Output | Use Case |
|---|---|---|---|
| `run_report.py` | MCP JSON data via `--data-dir` or stdin | `sources/*.json`, `manifest.json`, `report.html` | Full multi-source report assembly |
| `classify_user_type.py` | Advertiser info, campaign/ad names, URLs, apps | `user_type.json` | 13-class vertical classification |
| `metric_probe.py` | Report rows by metric group | `metric_preset.json`, `metric_probe.json` | Metric availability check |
| `creative_enrichment.py` | Ad rows + media info (image/video/Spark URLs) | `creative_previews.json`, `creative_retention.json` | Derived retention metrics, fatigue ranking |
| `audience_analysis.py` | Audience report rows (country/age/placement/device) | `audience_breakdowns.json` | Segment tagging (7 tags) |
| `landing_app_analyzer.py` | Ad URLs, app IDs, Smart+ landing paths | `landing_app_paths.json` | URL canonicalization, spend aggregation |
| `activity_analysis.py` | Changelog CSV from MCP download | `activities.json`, `activity_factors.json` | Activity normalization, ranking |
| `audit_creatiads_report.py` | Run directory path | `report_audit.json` | Report validation including user type/preset/phase order checks |
| `backend_router.py` | Tasks/phase from `pull_plan.json` | `backend_routing.json` | Route tasks between native_agent_mcp and mcp_subagent_executor backends |
| `plan_subagent_execution.py` | `mcp_tasks.jsonl` | `subagent_execution_plan.json`, `subagent_tasks/*.jsonl`, `subagent_prompts/*.md` | Split full/deep MCP tasks into subagent shards |
| `plan_gmv_max_report.py` | Advertiser ID, date range, optional BC ID | `pull_plan.json`, `mcp_tasks.jsonl`, `summary.json` | Product GMV Max / TikTok Shop report plan |
| `prepare_preview_mcp_calls.py` | Run directory with `current_ads` and ad detail sources | Concrete read-only MCP call specs | Expand final-row preview placeholders for image/video/Spark/catalog enrichment |
| `recover_subagent_mcp_payloads.py` | Run directory + Codex session JSONL files | Missing `raw/*.json` files | Fast recovery when subagents called MCP but large payloads were not written |
| `finalize_workflow_run.py` | Run directory + workflow args | `finalize_summary.json`, `timing_summary.json`, final workflow state | One-command post-MCP recovery, normalization, workflow advance, audit, and timing summary |
| `bridge_executor.py` | Legacy raw MCP responses via `raw/*.json` | Normalized `sources/*.json` | Deprecated bridge alias support; do not use for new plans |
| `normalize_mcp_source.py` | Raw MCP responses | Normalized source JSON | Unwrap L0/L1 dispatcher, text blocks, multi-page merge |
| `validate_pull_state.py` | Run directory with `pull_plan.json` | `validation_summary.json` | Phase gate, pagination, backend consistency, auth checks |
| `build_mcp_pull_plan.py` | Advertiser ID, depth, date range | `pull_plan.json`, `mcp_tasks.jsonl` | Generate agent-native MCP task plan with backend routing |

## Dual Backend Architecture

Creatiads uses a dual-backend execution model to separate light classification work from
heavy batch report pulls. The agent makes all MCP calls; backends define *how* tasks are
organized and validated.

### Backends

| Backend | Scope | Trigger |
|---|---|---|
| `native_agent_mcp` | Account inventory, user type, metric profile, fast/standard reports | Default for any light task |
| `mcp_subagent_executor` | Full/deep reports, batch enrichment, activity changelogs, multi-page merges | Depth `full` or `deep` with batch-eligible capability |
| `bridge_executor` | Deprecated alias | Legacy fixture/test compatibility only |

### Routing Rules

```
account_inventory, user_type, metric_profile → native_agent_mcp (always)
full_report, performance_diagnosis, audience_diagnosis,
  creative_diagnosis, landing_app_paths, activity_changelog,
  bottleneck_diagnosis                              → mcp_subagent_executor (full/deep), else native
Everything else                                     → native_agent_mcp
```

Subagent-to-native fallback is allowed for single tasks only. Every fallback must be
recorded in both `manifest.backend_fallbacks` and `source.attempts`.

### Source Contract Extensions

Every source file now carries:
- `backend`: `native_agent_mcp` or `mcp_subagent_executor`
- `auth_status`: empty for native/subagent sources; legacy bridge sources may carry auth state
- `attempts`: retry ladder records including backend fallback attempts

### MCP Subagent Executor Constraints

- **Agent-native only**: subagents call the existing TikTok MCP tools; Python never creates an MCP/OAuth client
- **Read-only for report flows**: no Create/Update/Status/Delete MCP tasks
- **Compact return contract**: subagents return only status, source paths, row counts, degraded sources, and errors
- **Output flow**: subagent fetches → `raw/*.json` → `normalize_mcp_source.py` → `sources/*.json`
- **Blocking first**: run only `blocking_before_report` shards for the first audited report. Shards marked
  `optional_after_first_report` (preview/activity enhancement) must not hold the main report unless the
  user explicitly asks for preview repair or enriched rerender.
- **Preview placeholders**: for `ad_details_for_enrichment` and `creative_preview_*`, run
  `prepare_preview_mcp_calls.py` after dependencies exist and execute the returned concrete MCP calls.
  Use `item_types`, `page`, and `page_size` for Spark posts; never use legacy `item_type` / `count`.
  If an image/video batch partially fails because of permissions, split and keep successful rows.
- **Legacy note**: `bridge_executor.py` remains only as deprecated compatibility glue and is not the new data plane

#### Subagent Recovery Rules

Real TikTok MCP runs showed that subagents may successfully call MCP but fail to write large
raw payloads to disk, or their final chat transcript may truncate/escape JSON. Treat the MCP
event stream as the source of truth:

- A subagent must write and verify each planned `raw/*.json` immediately after the MCP call.
  If a raw file cannot be written in that step, stop the shard and recover; do not keep calling
  more sources.
- Check `raw/*.json` first; never trust a "completed" subagent message without files or
  recoverable MCP events.
- If files are missing, inspect the subagent Codex session JSONL and extract the MCP result
  from `mcp_tool_call_end.payload.result.Ok.content[0].text`.
- Prefer the automated recovery command before manual JSONL inspection:
  `python3 creatiads/scripts/recover_subagent_mcp_payloads.py --run-dir <run_dir>`.
- Prefer `mcp_tool_call_end` over `function_call_output`; the latter can be truncated or
  JSON-escaped into an invalid fragment for large report responses.
- Use `subagent_prompts/*.md` from `plan_subagent_execution.py` when spawning workers; the
  prompts are pre-scoped to each shard and reduce setup chatter.
- Do not wait more than a short window for a shard that already made MCP calls. Run the
  recovery command, rerun `workflow_runner.py`, then relaunch only genuinely missing sources.
- The main session may write recovered MCP JSON into `raw/*.json`; this still preserves the
  subagent execution model because the platform call happened inside the subagent.
- For large sources, use small page sizes or page-range shards only when event recovery is
  unavailable. Otherwise one complete direct report call is acceptable if `mcp_tool_call_end`
  contains the full payload.
- Close subagents after their result has been recovered or recorded.

### Backend Consistency Checks

`validate_pull_state.py` enforces:
1. All tasks in the same phase must use the same backend
2. Executor auth failures (`auth_required`/`permission_denied`) must not be masked by `status: ok`
3. Manifest fallback entries must have corresponding source attempts
4. `audit_creatiads_report.py` checks for MCP session metadata leaks and missing backend fields
