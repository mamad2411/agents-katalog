---
id: tt4b-account-benchmark
name: tt4b-account-benchmark
description: "Platform-neutral TikTok account benchmark workflow. Use whenever the user asks whether a Campaign, Ad Group, Ad/Creative, or account result is good, strong, weak, worth scaling, better/worse than their account, above/below account baseline, or needs same-account relative performance context — even if they do not say \"benchmark\". Triggers: account baseline, relative performance, is this good, small sample noise, which one is stronger, 同账户对比, 账户基准, 表现好不好, 还行吗, 值不值得继续投, 哪个更靠谱, 是不是小样本假象, 高 CVR 是否可信. This read-only skill fetches TikTok reports through tt-ads MCP and computes deterministic same-advertiser, same-objective, same-grain benchmark statistics locally. Do NOT use for raw report pulls only (route to tt4b-get-performance-report), delivery/root-cause diagnosis such as no spend or rejection (route to tt4b-diagnose-campaign-health), or budget reallocation/execution (route to tt4b-optimize-budget)."
category: TikTok
metadata:
  version: 0.3.0
---

# TikTok Account Benchmark

This skill compares the performance currently being analyzed with a same-account benchmark
computed from the same advertiser's own reporting data.

This is a standard skill folder following the `SKILL.md` plus optional bundled resources pattern.
Keep host-specific setup outside the runtime skill instructions, and do not add local testbench
assumptions to this skill.

## Scope

Use this skill for:
- "Compare this account's last 7 days against its own benchmark."
- "How did my account perform over the last 7 days?"
- "Is this campaign's CPC better or worse than the account baseline?"
- "Show whether this campaign is better than most comparable campaigns in my account."
- "Find high-CVR / low-CPA / scalable ads and explain whether they are strong versus my account."
- "Which creative/ad is performing best?"
- "This Brand Awareness campaign has zero conversions; is it bad?"
- "Use cost-active ads as the benchmark pool."

Plain-language triggers / 非术语触发:
- Chinese: "这条 campaign 还行吗?", "这个广告值不值得继续投?", "哪个素材更靠谱?",
  "这个 high CVR 是不是样本太少?", "最近账户哪里拖后腿?", "比账户平均水平好吗?"
- English: "Is this campaign actually doing well?", "Is this ad worth scaling?",
  "Which creative is genuinely strong?", "Is this high-CVR result just small-sample noise?",
  "What is dragging down my account?", "Is it better than my account average?"
- Mixed: "这个 high CVR creative 靠谱吗?", "这个 ad worth scaling 吗?",
  "帮我找 truly strong 的素材."

If the user is asking whether a result is good, reliable, scalable, or strong versus their own
account, treat it as a benchmark request even when they never use the word "benchmark".

Object display rule:
- In every user-visible answer, render Campaign and AdGroup object names as Markdown links to
  TikTok Ads Manager whenever the required IDs are available. The linked text is the object name
  only, for example `[Summer Prospecting](https://ads.tiktok.com/...)`.
- Do not render Ad / Creative grain object names as Ads Manager links. This applies to ordinary
  Ads and Smart+ / virtual Creative rows. Ad-grain object names are plain text by design.
- Do not show a standalone object ID column by default, and do not use the legacy `{name} ({id})`
  style in tables, bullets, verdicts, or scope text. IDs belong in the URL or in explicit
  blocked/partial-link diagnostics for Campaign / AdGroup; for Ad grain, keep IDs out of the
  default display.
- Table headers must use the concrete single grain being analyzed: `Campaign`, `AdGroup`, or
  `Creative`, not generic `Object` / `对象`. If one answer needs multiple grains, split them into
  separate tables.
- Link mapping: Campaign uses `/manage/campaign` with `campaign_ids`; AdGroup uses
  `/manage/adgroup` with `ad_ids` but the filter value must come from the AdGroup identity
  (`adgroup_id`, falling back only when the MCP names that same value `ad_id`). Ad / Creative
  output does not build Ads Manager links, regardless of ordinary or Smart+ type. `creative_id`,
  `virtual_creative_id`, `smart_plus_ad_id`, and material IDs are asset/linkage context only; do
  not use them as the benchmark grain or user-visible link filter value.
- These IDs must be applied through the Ads Manager filter object, for example
  `filters[0][field]=campaign_ids` and `filters[0][in_field_values][0]=<campaign_id>`.
  Do not shorten links to top-level `campaign_ids=...`, `ad_ids=...`, or `creative_ids=...`;
  those links may open but will not filter the table correctly.
- If the MCP/API response does not include a name field, render `[Unknown name](url)` for linked
  Campaign / AdGroup rows when a link can be built. For Ad grain, render `Unknown name` as plain
  text and say the name field was unavailable.
- Candidate, contributor, and winner lists must include object name, grain, objective, spend,
  primary outcome, and the core efficiency metric used for the verdict.

Benchmark visibility and readability rule:
- If this skill is triggered, the final answer must contain a real benchmark result or an explicit
  benchmark-blocked/partial state. Do not answer with only an account summary, raw report, trend
  readout, or week-over-week comparison.
- For Chinese output, use Chinese-first section headings: `结论先说`, `核心对比`,
  `基准结论`, `下一步建议`, and `附录：基准范围`. For English
  output, use `Bottom line`, `Benchmark table`, `Benchmark verdict`, `Next steps`, and
  `Appendix: Benchmark scope`.
- Put the core judgment before benchmark metadata. `Benchmark scope` is useful, but for most
  readers it is metadata; move it to a compact appendix or one-line scope note near the end.
- The first sentence under `结论先说` should contain only one qualitative judgment plus one key
  number. Put other metrics in short bullets or tables instead of stacking them into one sentence.
- A response that says only "账号复盘", "账号诊断", "整体表现", "重点 Campaign", or "趋势" without a
  benchmark table and verdict is incomplete.
- Do not let week-over-week or trend analysis replace the benchmark. If the response includes WoW
  trend, separate it from `Account benchmark`.
- A benchmark answer must include benchmark scope, benchmark table, and benchmark verdict using
  median plus relative position. If no benchmark pool was computed, say "this is
  trend analysis, not benchmark" instead of implying a benchmark conclusion.
- Never finish by saying the benchmark will be added later. If the benchmark pool is unavailable,
  the final answer must be labeled `Benchmark blocked（Benchmark 受阻）` or
  `Partial benchmark（部分 Benchmark）` and explain the blocker.

Route elsewhere:
- Raw report only -> `tt4b-get-performance-report`
- Delivery/review/root-cause diagnosis -> `tt4b-diagnose-campaign-health`
- Budget shift recommendation or execution -> `tt4b-optimize-budget`
- Industry/platform-wide benchmark -> out of scope for MCP-only workflow

No-kit fallback:
- Prefer the sibling tt4b skill when it is installed and available. If the route target is not
  installed or cannot be invoked, do not fail just because routing is unavailable.
- For raw-report requests, this skill may pull the minimal read-only `tt-ads` report needed for a
  limited performance readout or benchmark, but state that full table export/report workflow is
  owned by the reporting skill when available.
- For diagnosis requests, this skill may reason from already retrieved read-only fields such as
  status, spend, impressions, clicks, and conversions. Do not claim a full delivery-health
  diagnosis when review, budget, pacing, bid, or status-history fields were not checked.
- For optimization or mutation requests, provide benchmark evidence and read-only decision support
  only. Do not pause, resume, edit budget, edit bids, or perform any spend-affecting action.
- Use this fallback wording when helpful: "我没有检测到对应的 kit skill，所以先在本 benchmark
  skill 的只读范围内推理；涉及写操作或完整诊断的部分需要对应 skill/tool。"

Language policy:
- Default to the user's primary language for the final conversational answer and any human-readable
  `summary.md` artifact.
- If the user writes in Chinese or mostly Chinese mixed with terms like `adg`, `benchmark`, `CVR`,
  or `creative`, answer in Chinese. If the user writes in English, answer in English.
- Keep object names, IDs, API metric keys, and standard ad terms unchanged when translation would
  reduce clarity. In Chinese output, keep headings Chinese-first and put English benchmark terms in
  parentheses only on first use when helpful.
- `result.json` and `manifest.json` remain structured machine-readable artifacts and do not need
  natural-language translation.

## Kit Collaboration

When installed inside a broader `tt4b-skill-kit`, this skill is the read-only relative-performance
judge. It should be easy to enter from report, diagnosis, or optimization conversations whenever
the user moves from "show me the numbers" to "are these numbers actually good versus my account?"

## What this skill does NOT own

| Out-of-scope intent | Route to |
|---|---|
| Raw performance table, export, dayparting, or multi-dimensional report without a relative account verdict | `tt4b-get-performance-report` |
| Delivery health, no spend, no impressions, review rejection, budget exhaustion, bid competitiveness, or creative fatigue root cause | `tt4b-diagnose-campaign-health` |
| Budget reallocation, pause/resume, budget edits, or executing recommendations that affect spend | `tt4b-optimize-budget` or `tt4b-manage-campaign` |
| Creating, duplicating, or editing campaigns, ad groups, ads, creatives, audiences, or catalogs | The matching `tt4b-launch-*`, `tt4b-duplicate-campaign`, or `tt4b-manage-*` skill |

If a neighboring skill already pulled report rows and the user asks a follow-up like "is that
good?", "which one is really strong?", "比账户其他 campaign 好吗?", or "高 CVR 可信吗?", switch into
benchmark logic using the existing advertiser, window, grain, and objective context when available.
Do not reframe that follow-up as another raw report.

## MCP Backend Compatibility

In kit environments that expose the `tt-ads-mcp` dispatcher, follow the kit dispatcher convention:
use direct L0 tools when available, otherwise call `tool_get` for schemas and then
`tool_execute(tool_name="<Tool>", params={...})`. The benchmark report logical call maps to the
host's reporting tool, commonly `Run_a_synchronous_report` in dispatcher kits or
`report_integrated_get` in direct `tt-ads` hosts. In environments that expose direct `tt-ads` MCP
tools, use the direct tool names in `references/mcp-report-contract.md`.

This compatibility note changes only how tools are invoked. It does not add a new MCP dependency,
does not permit direct network access from scripts, and does not allow synthetic or substituted
data.

## Default Configuration

If the user does not specify otherwise:
- `analysis_window`: last 7 complete account-local days
- `benchmark_window`: same length as `analysis_window`; default is last 7 complete account-local
  days ending on the same date as the analysis window
- `analysis_level`: Campaign
- `benchmark_level`: same as `analysis_level`
- `cost_active_rule`: `spend > 0`
- `metrics`: resolve from `objective_type`; if objective is unknown, default to CPC, CPA, CTR,
  CVR, CPM, conversions, and spend with a caveat
- `statistics`: median plus relative position; keep percentile fields internally,
  but translate them into advertiser-facing language such as "better than 75% of comparable
  Campaigns" or "higher than 75% of comparable Campaigns"
- `default_readout`: include both `Winners` and `Draggers` whenever the user asks for account
  performance, hot objects, best/worst objects, worth scaling, or whether performance is good.
  Do not wait for the user to ask separately for underperformers.
- `relative_waterline`: every Winner and Dragger shown to the user must carry a benchmark waterline
  statement for its own grain, such as "CPA better than 92% of comparable Campaigns" or
  "CPA worse than 88% of comparable Campaigns." Do not only say "better than account average" or
  "dragging CPA" when percentile/rank evidence is available.
- `single_grain_display`: show one entity grain per winner/dragger table. Campaign winners and
  AdGroup draggers must not share one table. If multiple grains are relevant, render separate
  Campaign / AdGroup / Creative sections.

Hard rule: benchmark comparisons must use one analysis target and a like-for-like benchmark pool.
The target is a single Campaign, Ad Group, or Ad. Do not merge a 7-day list of entities into one
aggregate and compare that aggregate to a 30-day pool.

Benchmark pools must match objective, grain, and window. A `REACH` Campaign should be compared
with other cost-active `REACH` Campaigns in the same window, not with `WEB_CONVERSIONS` Campaigns
or Ad-level rows. When an account contains multiple objectives, render account benchmark by
objective bucket instead of mixing CPA/CVR/CPM conclusions across objectives.

Account overview requests are mandatory benchmark requests. If the user asks how the account
performed without naming one object, first pull an account-level same-grain list for the analysis
window, summarize account totals and objective buckets, then run a benchmark in the same response.
Default to Campaign grain and split mixed objectives into objective buckets. If the user did not
choose a target object, auto-select the highest-spend cost-active Campaign within the dominant
objective bucket as the primary benchmark target and clearly state the selected linked Campaign name
before the benchmark blocks. Do not ask whether to benchmark before producing at least one
benchmark result. Only offer additional target choices after the mandatory benchmark is shown.
For prompts like "看看我账号表现如何最近" or "账号最近一周表现怎么样", do not output a standalone
account recap first and wait for the user to ask "你怎么没说 benchmark". The same response must
include the literal benchmark labels above.

Benchmark comparisons must also be like-for-like by entity grain.
Campaign analysis compares against cost-active Campaigns, Ad Group analysis compares against
cost-active Ad Groups, and Ad analysis compares against cost-active Ads. Do not compare Campaign
performance to an Ad-level benchmark.

Candidate discovery requests, such as "find high CVR creatives", are allowed only when they stay
connected to benchmark logic. Treat sorting as candidate generation, not the final conclusion.
After finding top candidates, run same-objective, same-grain account benchmark for each candidate
or for the shortlisted set. Creative/material requests use Ad grain for the main benchmark and use
`ad_id` as the benchmark and aggregation key. Do not aggregate by `ad_name`; names can repeat and
are not stable identifiers. If Smart+ material reporting is available, use it only as optional
enrichment to explain material-level contribution, not as a fourth user-facing benchmark grain.
Default candidate discovery should surface both
Winners and Draggers from the same benchmark pool: who looks meaningfully above account waterline,
and who is spending or receiving traffic while dragging the objective-specific efficiency below
account waterline.

Read `references/account-benchmark-design.md` when modifying definitions, explaining
methodology, or resolving ambiguity.
Read `references/mcp-report-contract.md` before changing report parameters, supported metrics,
pagination, or raw-response handling.
Read `references/interactive-intake.md` when the user request is vague, missing account/object
context, or phrased as a general "is my ad doing well?" question.
Read `references/metric-catalog.md` before translating user-facing metric names into API metrics.
Read `references/objective-metric-profiles.md` before selecting metrics, comparison pools, or
conclusion language.
Read `references/analysis-output.md` before writing narrative conclusions, insights, or
recommendations.
Read `references/candidate-discovery.md` before ranking or recommending high-CVR, low-CPA,
high-scale, or "good creative" candidates.
Read `references/smart-plus-material-benchmark.md` before using optional Smart+ material
enrichment.

## Workflow

0. Run execution preflight.
   - Confirm the `tt-ads` MCP server and required tools are available in the current host before
     promising a real data run. If they are not available, say the environment is blocked and do
     not fabricate report data.
   - If the MCP server reports authentication problems such as `invalid_token`, `unauthorized`, or
     `AuthRequired`, ask the user to reauthenticate (`codex mcp login tt-ads` in Codex) and stop
     before pulling reports.
   - If the API reports permission problems for the selected advertiser, surface the raw permission
     error and ask the user to switch identity or provide an accessible advertiser.
   - Validate dates before calling the report API: no future end date, no `start_date > end_date`,
     and avoid current-day data by default because it may be incomplete.
   - Translate requested metrics through `references/metric-catalog.md` and the selected objective
     profile. Do not request unsupported commerce or revenue metrics on the BASIC report path;
     explain the limitation and continue with supported metrics if that still answers the user's
     question.

1. Run interactive intake.
   - Do not assume the user knows the reporting schema, entity grain, or benchmark windows.
   - If the user gives a complete request, proceed without extra questions.
   - If critical fields are missing, ask focused questions using `references/interactive-intake.md`.
   - If the user asks for an account overview, resolve advertiser context and run mandatory account
     overview benchmark mode: summarize account-level performance, auto-select a primary
     cost-active Campaign when no object is specified, and produce benchmark scope/table/verdict in
     the same response.
   - Prefer defaults for non-critical choices: last 7 complete days for analysis, benchmark window
     equal to the analysis window length, and the default metric set. Offer a longer benchmark
     window only when the eligible sample is too small for a useful read.

2. Resolve advertiser context.
   - Prefer explicit `advertiser_id` if the user provides one.
   - Otherwise follow the standard BC -> advertiser selection flow from the installed tt4b skills.
     When installed with `tt4b-skill-kit`, prefer the shared semantics in
     `../shared/stage0-bc-advertiser.md` for listing BCs, listing advertiser assets, and reusing
     the selected `bc_id` / `advertiser_id`.
   - If `auth_advertiser_get` returns empty, do not fail immediately. Ask for or use a
     user-provided `advertiser_id` and continue to the report path.
   - If BC lookup times out but the user provided an `advertiser_id`, try that advertiser directly.
   - If multiple advertiser contexts are plausible, ask the user to choose. Do not infer the
     advertiser from an object ID unless a verified lookup resolves it.

3. Resolve objective and metric profile.
   - Resolve `objective_type` before choosing benchmark metrics and conclusion language.
   - For Campaign grain, request or look up Campaign `objective_type` directly when available.
   - For Ad Group or Ad grain, resolve the parent Campaign objective when row-level objective is not
     available.
   - If the user asks for a conversion verdict but the objective is awareness/reach, say this is a
     brand objective and use the awareness profile instead of CPA/CVR as the default verdict.
   - If the account has mixed objectives, split benchmark output into objective buckets. Do not
     mix `REACH` rows into conversion CPA/CVR benchmark or conversion rows into awareness CPM
     benchmark.
   - If objective lookup is unavailable, continue with neutral core metrics only when that still
     answers the request, and state that objective context was not verified.

4. Pull the analysis report.
   - Use `report_integrated_get`.
   - Follow the contract in `references/mcp-report-contract.md`.
   - The analysis output should resolve to one target entity.
     - If the user names or provides an ID, filter/select that entity.
     - If the user asks for a test, pick one cost-active entity from the requested level and state
       which one was selected.
     - If the user asks for account overview without a target, pick the highest-spend cost-active
      Campaign in the dominant objective bucket as the primary benchmark target after summarizing
      the account list. State the selected Campaign as a Markdown link when link fields are
       available before computing the benchmark.
  - If the user asks for a table/list, do not compute one benchmark verdict for the whole list;
      compute per-row verdicts for the displayed rows, including the relative waterline for each
      row, or produce at least one benchmark verdict for the auto-selected primary target before
      asking which additional row to inspect.
   - Common params:
     - `report_type=BASIC`
     - `service_type=AUCTION`
     - `data_level=AUCTION_CAMPAIGN` unless user asks for Ad Group or Ad.
     - `dimensions=["campaign_id"]` or `["campaign_id","stat_time_day"]` depending the user view.
     - Metrics: selected from `references/objective-metric-profiles.md` and translated through
       `references/metric-catalog.md`.
     - Do not request commerce or revenue metrics through this BASIC report path unless the MCP
       contract has been updated with a verified supporting endpoint.

5. Pull the benchmark report.
   - Use `report_integrated_get`.
   - Always pass an explicit `page` starting at `1`; some responses may include `total_number`
     and `total_metrics` while returning an empty `list` when pagination is omitted.
   - By default, use a benchmark window with the same number of complete days as the analysis
     window. If the user chooses a 7-day analysis window, use a 7-day benchmark window unless they
     explicitly ask for 30 days or the sample-size caveat suggests extending the window.
   - Match `objective_type`, `data_level`, dimensions, and window to the analysis report:
     - Campaign view: `data_level=AUCTION_CAMPAIGN`, `dimensions=["campaign_id"]`
     - Ad Group view: `data_level=AUCTION_ADGROUP`, `dimensions=["adgroup_id"]`
     - Ad view: `data_level=AUCTION_AD`, `dimensions=["ad_id"]`
     - same core metrics as analysis.
   - Page through all results. `page_size` is at most 1000.
   - If the account has more than 20,000 ads, batch by campaign/adgroup/ad filters.
   - The analysis report and benchmark report are independent read-only pulls and should be
     executed in parallel when the MCP/client supports it.
   - If the benchmark report cannot be pulled or the eligible pool is empty, the final answer must
     be labeled as benchmark blocked/partial with the reason, such as `E201_NO_BENCHMARK_SAMPLE`.
     Do not finish with only WoW trend or account summary.

6. If doing creative/ad candidate discovery, classify candidates before concluding.
   - Use Ad grain as the main user-facing benchmark, including when the user says "素材",
     "creative", "ad", or asks about Smart+ creative performance. Do not introduce Smart+
     Material as a fourth primary benchmark level.
   - If the relevant Campaign is `UPGRADED_SMART_PLUS` and
     `smart_plus_material_report_overview_run` is available, optionally use it as enrichment:
     aggregate by `main_material_id`, derive CPA/CVR/CTR locally from summed numerators, and use
     that only to explain material contribution behind the Ad-level result.
   - If Smart+ material enrichment is unavailable, unsupported, or missing material fields, keep
     the main Ad-level benchmark and add a short caveat only when the distinction affects the
     conclusion.
   - Generate candidates by the user's requested lens, such as high CVR, low CPA, or high
     conversion scale.
   - In the same pass, generate dragger candidates from the same benchmark pool. Do not ask the
     user whether to inspect underperformers. For single-object benchmark, classify the target as
     strong, neutral, or dragging; if the pool is already loaded, include 1-3 main draggers as
     context.
   - Use adaptive evidence tiers from the same benchmark pool instead of a single hard global
     threshold. Do not let 1-2 conversions or a handful of clicks enter the main recommendation
     bucket just because CVR is high.
   - Benchmark each main candidate at the same grain. A high-CVR Ad must be judged against
     cost-active Ads, not Campaigns or Ad Groups.
   - Separate recommendations into high CVR, low CPA, and high scale when the metrics tell
     different stories.
   - Separate negative findings into Draggers rather than hiding them as caveats. A dragger needs
     both meaningful scale and weak objective-specific efficiency, such as high spend with poor
     CPA/CVR for conversion objectives or high CPC with low CTR for traffic objectives. Low-spend
     or tiny-sample weak rows belong in directional observations, not the main dragger list.
   - Before labeling any candidate as "winner", "worth scaling", "热门", "可扩量", or "重点看",
     attempt a read-only status lookup for every surfaced candidate and its relevant parent
     objects. For Campaign candidates, check Campaign status. For Ad Group candidates, check Ad
     Group and parent Campaign status. For Ad candidates, check Ad, parent Ad Group, and parent
     Campaign status. If optional Smart+ material enrichment points to associated Smart+ objects,
     use those links only to support the Ad-level candidate status context.
   - Use read/list/status-get tools only. Never call `Update_*` tools or any status mutation tool
     from this benchmark skill.
   - Active/enabled candidates can stay in the main recommendation bucket. Disabled/stopped
     candidates must be downgraded or clearly marked: performance looked strong historically, but
     the object is not currently live, so it is not an immediate scaling candidate until stop
     reason/status is reviewed.
   - If status lookup is unavailable because the host lacks read tools, schemas, or permission,
     say "状态未能通过当前 MCP 工具查到" and keep the recommendation conditional. Do not write
     "扩量前最好再确认状态" without first attempting the lookup.

6a. Build Ads Manager object links when rendering user-visible object names.
   - For Campaign output, use the row's `campaign_id` as `campaign_ids` in `/i18n/manage/campaign`.
   - For AdGroup output, use the row's AdGroup identity as `ad_ids` in
     `/i18n/manage/adgroup`: prefer `adgroup_id`, and fall back to `ad_id` only when the MCP
     exposes the AdGroup identity under that field name. Do not substitute a child Ad ID from an
     Ad-level row.
   - For Ad / Creative output, do not build Ads Manager object links. This applies to ordinary Ad
     rows and Smart+ / virtual Creative rows. Query-time grain remains Ad; `creative_id`,
     `virtual_creative_id`, `smart_plus_ad_id`, `main_material_id`, and material IDs are context
     only, not user-visible link filter values.
   - If a required link field is missing, keep the object name as plain text and mark the answer as
     a partial link state with the missing field name. Do not substitute another ID. This partial
     link state applies only to Campaign / AdGroup links; Ad grain is intentionally plain text.

7. Persist raw responses.
   - Save or retain the raw `advertiser_info_get`, analysis `report_integrated_get`, and benchmark
     `report_integrated_get` responses as soon as they succeed when the host supports files or run
     artifacts.
   - If status lookup runs, save or retain the status/list raw response as part of the same run
     artifacts when the host supports files.
   - If the agent or runner fails after the MCP calls complete, report this as a host/runner
     failure separately from the API result. Do not discard successfully retrieved raw responses.
   - Never replace a failed or missing real response with sample, synthetic, or substituted data.

8. Compute locally.
   - Use `scripts/compute-account-benchmark.mjs` when report JSON is available and Node.js is
     available. If Node.js is unavailable, use `scripts/compute-account-benchmark.py` with the
     same raw analysis JSON, benchmark JSON, CLI flags, output language, object-link flags, and
     metric list. The two scripts are the same deterministic compute contract.
   - When generating markdown or `summary.md`, pass `--language zh` for Chinese or mostly Chinese
     prompts and `--language en` for English prompts. If the host writes `summary.md` without the
     script, follow the same language policy manually.
   - When Campaign / AdGroup object links are available, pass `--advertiser-id`, `--link-kind`,
     `--start-date`, and `--end-date`. Ads Manager links use the bundled script's stable
     `navigate_from=campaignList` template with `columns`, explicit `st`/`et`, and `filters[0]`
     parameters; do not hand-build a shortened URL with top-level `campaign_ids`, `ad_ids`, or
     `creative_ids`. Do not add `relative_time`, `sort_state`, or `sort_order`. For Creative / Ad
     output, the compute scripts must keep object names as plain text even when `--advertiser-id`
     and `--link-kind creative` / `smart_plus_creative` are passed.
   - Pass `--analysis-id` when the analysis report contains multiple rows.
   - Apply Cost Active, objective-bucket, and metric-specific eligibility rules locally.
   - Normalize additive volume metrics to average daily values when analysis and benchmark
     windows have different lengths. Additive metrics include `spend`, `impressions`, `clicks`,
     `conversion`, video view counts, and engagement counts.
   - Do not daily-normalize ratio or efficiency metrics. CPC, CPA, CPM, CTR, CVR, ROAS, and
     similar rates should be computed from the selected window's aggregated numerator and
     denominator.
   - Do not use `report_ad_benchmark_get` as the primary path; it is optional only.
   - If neither bundled runtime is available, reproduce the same deterministic rules from
     `references/account-benchmark-design.md`; do not ask an LLM to invent percentile math.
   - The preferred compute location is local deterministic code: the bundled script, or a local
     server that imports the same logic. MCP/agent calls fetch data only.

9. Render the result.
   - Before sending the final answer, run a mental output gate: if the response does not contain
     a bottom-line judgment, a benchmark table, a benchmark verdict, next steps, and a compact
     benchmark scope appendix or one-line scope note, it is not ready to send.
   - First write the conclusion directly in the conversation. Artifact links are supplemental and
     must not replace the user-facing summary.
   - Match the user's primary language in the conversational answer and any `summary.md` artifact.
   - If a human-readable `summary.md` is saved, verify its heading and main narrative language
     before final response. For Chinese or Chinese-dominant prompts, rewrite the file if it still
     uses English-only headings such as `Hot Ad Group Benchmark` or `Key Reads`.
   - Localize benchmark scope labels to the user's language. For Chinese output, write labels such
     as `广告主`, `窗口`, `粒度`, `目标`, `基准池`, `样本`, and `主基准对象`; do not use English labels
     such as `Advertiser`, `Window`, `Grain`, `Objective`, `Pool`, or `Primary benchmark target`.
   - For hot-object or ranked candidate outputs, keep the chat answer substantial enough to be
     useful without opening `summary.md`: include winners, draggers, scale leader, efficiency
     candidate, key risk/caveat, a compact benchmark table, and scope appendix.
   - Use a reader-first narrative: start with `结论先说`, then show same-grain Winners and Draggers
     as tables, then the metric table and next steps, then benchmark scope. The intro for Winners
     should state that these objects sit in a strong/high account tier; the intro for Draggers
     should state that these objects sit in a weak/low account tier or materially pull the
     objective bucket down.
   - Winners and Draggers must be rendered as tables. Preserve full object names, use the
     concrete grain as the first column header, include every computed metric as a visible column,
     and do not crop columns just to keep the table short.
   - Before sending, force-check the output: no standalone object `ID` column, no legacy
     `{name} ({id})` object labels, no generic `Object` / `对象` table header, Campaign / AdGroup
     object names are Markdown links when their link fields are available, and Ad / Creative grain
     object names are plain text. Campaign / AdGroup link URLs must include `columns=` and the
     encoded or raw `filters[0][field]` / `filters[0][in_field_values][0]` parameters; reject
     top-level `campaign_ids=...`, `ad_ids=...`, or `creative_ids=...`. AdGroup links must use the
     AdGroup identity even though the URL parameter is named `ad_ids`. Ad-grain output must not
     include `/manage/creative`, `creative_ids`, or `virtual_creative_id` links.
   - Show analysis window, benchmark window, entity grain, sample count, excluded count.
   - Show the resolved objective profile. If objective was unavailable, explicitly say it was not
     verified.
   - Translate distribution statistics into advertiser-facing language. Avoid making the user read
     P25/P50/P75 terminology unless they ask for diagnostic detail.
   - Format money with thousands separators, such as `$2,222.13`. Label median values
     with the statistic used, usually `中位数` / `Median`.
   - Compare current metrics to the median and relative position, for example:
     "CPC is better than 75% of comparable Campaigns" or "Spend is higher than 88% of comparable
     Campaigns."
   - For Winners, include "better than N% of comparable {grain}s" on the core objective metric.
     For Draggers, include "worse than N% / lower than N% / weaker than N% of comparable {grain}s"
     on the core objective metric, choosing wording that matches metric direction. For neutral
     scale metrics such as spend, say "higher than N%" or "lower than N%" rather than better/worse.
   - Interpret metric direction by objective and business meaning:
     - Conversion campaigns: CPA/CVR/conversions are primary.
     - Awareness/reach campaigns: CPM, impressions, reach, and frequency are primary; do not judge
       them by zero conversions by default.
     - Traffic campaigns: CPC, CTR, clicks, and landing page views are primary.
     - Video campaigns: CPV, 6s views, completion, and video volume are primary.
     - Spend, impressions, and clicks are scale signals unless the selected objective makes them
       outcome metrics.
   - For additive volume metrics across windows of different length, compare average daily values
     rather than raw period totals unless the user explicitly asks for period totals.
   - For ratio or efficiency metrics, compare the window-level rate rather than a daily average.
   - Do not present confidence as a standalone table column or numeric score. Instead, front-load
     a short sample-size caveat when eligible samples are below the threshold in
     `references/analysis-output.md`; repeat it in the narrative if it affects the conclusion.
   - Include a short narrative with observations, insights, and `下一步建议` / `Next steps`,
     following `references/analysis-output.md`. Under next steps, use positive decision-support
     wording such as "以下建议基于报表数据，执行前请结合实时投放状态确认。"
   - Keep the skill read-only.

## Failure Handling

- Missing MCP server/tooling: state that `tt-ads` is unavailable in the current host and list the
  expected tools: `advertiser_info_get` and `report_integrated_get`.
- Expired or missing OAuth: surface the auth error and ask the user to log in again; in Codex, use
  `codex mcp login tt-ads`.
- Empty advertiser discovery: ask for an `advertiser_id` and continue if the user provides one.
- BC lookup timeout: if an `advertiser_id` is known, try report pulls directly before declaring the
  workflow blocked.
- Advertiser permission denied: surface the raw API `code`, `message`, and request id, then ask for
  an accessible advertiser or account identity.
- Unsupported metric or field 400: remove the unsupported field/metric, retry once with the
  degraded metric set if the remaining metrics still answer the question, and explain the
  degradation.
- MCP network/timeout error: retry the same read-only TikTok call once. If retry fails, distinguish
  network/timeout from advertiser permission errors.
- No analysis rows: report that the selected object has no data in the analysis window; offer to
  extend the window or pick another cost-active object.
- No benchmark rows: report `E201_NO_BENCHMARK_SAMPLE` and offer a longer benchmark window or
  coarser entity grain.
- Objective unavailable: continue only with neutral or explicitly requested metrics and say the
  objective-aware benchmark could not be verified.
- Mixed objectives: split output by objective bucket; do not compute one cross-objective CPA/CVR
  verdict.
- Smart+ material enrichment unavailable: keep the Ad-level benchmark as the main result and avoid
  material-level claims.
- Too few eligible samples for a metric: front-load the sample-size caveat; do not fabricate.
- Candidate has tiny evidence: keep it out of the main recommendation bucket and label it as a
  directional observation.
- Candidate status disabled: downgrade it or clearly explain that performance looked strong but
  the object is currently stopped, so the next step is to inspect status history/reason.
- API 4xx/5xx: surface raw `code`, `message`, and request id.
- Official benchmark returns empty metrics: treat as unavailable and continue with local benchmark.
- Host-specific runner failure: report the host failure separately from MCP/API failure.

## Minimum Inputs

The skill can start from rough natural language, but it must resolve these before pulling reports:

| Field | Required? | How to get it |
|---|---|---|
| Advertiser/account | Required | Use explicit `advertiser_id`, resolved account context, or ask the user |
| Target grain | Required | Campaign, Ad Group, or Ad. Infer only when user explicitly says the type |
| Target object | Required | Object ID, object name/selection criteria, or user approval to pick one cost-active object |
| Analysis window | Optional | Default to last 7 complete account-local days |
| Benchmark window | Optional | Default to the same number of complete days as the analysis window |
| Metrics | Optional | Default to the resolved objective profile; use CPC, CPA, CTR, CVR, CPM, conversions, and spend only when objective is unknown |

If the user provides only an object ID without its type, ask whether it is Campaign, Ad Group, or Ad.
Do not infer type from numeric ID shape.

## Compute Location

The account benchmark calculation is local, not an MCP/API-side benchmark and not LLM reasoning.
The MCP server supplies raw report rows. The skill or host then runs deterministic local logic to:

- unwrap MCP/TikTok report responses
- filter the same-grain benchmark pool to cost-active entities
- filter or bucket the benchmark pool to the same objective when objective is available
- normalize additive metrics to daily averages when windows differ
- compute rate metrics from aggregated numerators and denominators
- compute P25/P50/P75, percentile rank, confidence, and verdicts

In the local web testbench, this happens in the Node server through
`scripts/compute-account-benchmark.mjs`. In a pure Claude/Codex skill invocation, use the bundled
Node script when Node.js is available, or `scripts/compute-account-benchmark.py` when Python is the
available local runtime. Both scripts must accept the same report JSON and produce the same
benchmark semantics. Only fall back to the reference rules manually if neither local runtime can run.

## Platform Boundary

The MCP server is the shared execution substrate. Claude, Codex, or another host may expose the
same MCP tool names differently, but the skill should continue to describe the desired `tt-ads`
tool contract rather than a host-specific function name.

Host adapters may handle:
- install path (`~/.claude/skills` vs `~/.codex/skills`)
- skill metadata limits
- MCP tool naming and invocation syntax
- subagent, eval, or runner capabilities

Host adapters must not change:
- account benchmark definitions
- same-grain comparison rule
- metric eligibility
- local deterministic compute rules
- read-only posture
