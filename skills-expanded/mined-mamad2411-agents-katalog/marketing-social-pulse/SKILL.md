---
name: marketing-social-pulse
description: Analyze mindshare, sentiment, and broader social metrics for a particular entity using Kaito MCP tools. Use this skill when the user asks about the social pulse of a particular entity, wants mindshare or sentiment trends, or wants a deeper anomaly-based explanation.
---

## Preamble (run first)

```bash
_KS_REPO=""
_KS_REAL_SKILL="$(cd "$HOME/.claude/skills/marketing-social-pulse" 2>/dev/null && pwd -P || true)"
for _candidate in \
  "${KAITO_SKILLS_DIR:-}" \
  "$( [ -n "$_KS_REAL_SKILL" ] && cd "$_KS_REAL_SKILL/../.." 2>/dev/null && pwd -P || true )" \
  "$HOME/kaito-skills" \
  "$HOME/.kaito-skills/repo"
do
  [ -n "$_candidate" ] || continue
  if [ -f "$_candidate/skills.json" ] && [ -x "$_candidate/bin/kaito-skills-update-check" ]; then
    _KS_REPO="$_candidate"
    break
  fi
done

if [ -n "$_KS_REPO" ]; then
  echo "KAITO_SKILLS_REPO $_KS_REPO"
  _UPD=$("$_KS_REPO/bin/kaito-skills-update-check" 2>/dev/null || true)
  [ -n "$_UPD" ] && echo "$_UPD" || true
fi
```

If output shows `KAITO_SKILLS_REPO <path>`, remember that path as `KAITO_SKILLS_REPO`.

If output shows `UPGRADE_AVAILABLE <old> <new>`, read `<KAITO_SKILLS_REPO>/docs/update-kaito-skills.md` and follow the "Inline upgrade flow" before continuing. If the user snoozes or disables update checks, continue with the current skill.

If output shows `JUST_UPGRADED <from> <to>`, tell the user `Running kaito-skills v{to} (just updated!)` and continue.

# Social Pulse

Use this skill when the user asks about mindshare, sentiment, or broader social metrics for a particular entity, especially when the answer should include time-window anomalies, 12-month context, and drill-down explanation.

## Inputs

- `token`: project name, ticker, or resolved Kaito token value; optional only when an upstream workflow already supplies `unresolved_string` plus a confirmed `official_handle`
- `official_handle`: optional upfront hint passed into `shared-entity-resolution` when the token does not resolve cleanly; required whenever unresolved mode is finalized
- `unresolved_string`: optional prebuilt keyword string from `shared-entity-resolution`; use it only when it already comes with a confirmed `official_handle`
- `affiliate_handles`: optional comma-separated handles that should be merged into the canonical exclusion set when already known
- `duration`: `7d`, `30d`, `90d`, or an explicit past window with `start` and `end` (default `30d`)

## Workflow

Organize the workflow into four stages: `Resolve Entity`, `Data Gathering`, `Analysis`, and `Output`.

### 1. Resolve Entity

Resolve the entity identity, exclusion set, and exact analysis window before pulling any metrics.

Use `shared-entity-resolution` first unless an upstream workflow already hands you a confirmed unresolved identity package.

- If `unresolved_string` is already supplied together with a confirmed `official_handle`, treat that pair as the unresolved identity package from `shared-entity-resolution` and do not rebuild it.
- Otherwise, follow `../shared-entity-resolution/SKILL.md` for token ambiguity handling, official-handle research, handle confirmation, and unresolved keyword-string construction.
- Carry forward the identity package returned by `shared-entity-resolution`:
  - resolved mode: `RESOLUTION_MODE = resolved`, `RESOLVED_TOKEN = <kaito token>`, plus `OFFICIAL_HANDLE` and `AFFILIATE_HANDLES` when available from `kaito_twitter_official_account`
  - unresolved mode: `RESOLUTION_MODE = unresolved`, `OFFICIAL_HANDLE = <confirmed official handle>`, and `UNRESOLVED_STRING = <keyword string>`
- Treat `OFFICIAL_HANDLE` as mandatory before continuing in unresolved mode.
- Build a reusable entity search filter:
  - resolved mode: `ENTITY_SEARCH_FILTER = tokens=<RESOLVED_TOKEN>`
  - unresolved mode: `ENTITY_SEARCH_FILTER = keyword=<UNRESOLVED_STRING>`
- In resolved mode, `mindshare`, `sentiment`, `mentions`, `engagement`, and `kaito_mindshare_entity_by_account` are available.
- In unresolved mode, continue with `mentions`, `engagement`, and search-based drill-down only. `mindshare`, `sentiment`, and `kaito_mindshare_entity_by_account` are unavailable and must be called out explicitly in the output.
- Identify `OFFICIAL_HANDLE` when available in resolved mode as well so exclusion logic can still work.
- In resolved mode, if the carried identity package is missing `OFFICIAL_HANDLE` or `AFFILIATE_HANDLES`, call `kaito_twitter_official_account` for `RESOLVED_TOKEN` before building exclusions.
- Build `EXCLUDED_HANDLES` from the canonical official handle, any affiliate handles returned by `kaito_twitter_official_account`, and any extra confirmed `affiliate_handles` supplied by the user.
- In unresolved mode, include only the confirmed official handle plus any extra `affiliate_handles` that are already confirmed. Do not guess affiliates.
- If affiliate handles are not available from the endpoint or user input, still exclude the official handle and state that affiliate exclusion may be incomplete.
- Convert the requested period into exact `window_start` and `window_end` timestamps.
- Also define `context_start` as the trailing 12-month start anchored to `window_end`.
- Use exact dates in the analysis and output, not only relative phrases such as `last month`.

### 2. Data Gathering

#### 2.1 Pull current-window and trailing-12-month metrics in parallel

Run the mode-appropriate bundle:

1. resolved mode:
   - `kaito_mindshare_entity` for the requested analysis window
   - `kaito_mindshare_entity` for the trailing 12 months ending at `window_end`
   - `kaito_sentiment_entity` for the requested analysis window
   - `kaito_sentiment_entity` for the trailing 12 months ending at `window_end`
   - `kaito_mentions` for the requested analysis window with `sources="Twitter"`
   - `kaito_mentions` for the trailing 12 months ending at `window_end` with `sources="Twitter"`
   - `kaito_engagement` for the requested analysis window
   - `kaito_engagement` for the trailing 12 months ending at `window_end`
2. unresolved mode:
   - `kaito_mentions` for the requested analysis window with `sources="Twitter"` using the unresolved entity expression
   - `kaito_mentions` for the trailing 12 months ending at `window_end` with `sources="Twitter"` using the unresolved entity expression
   - `kaito_engagement` for the requested analysis window using the unresolved entity expression
   - `kaito_engagement` for the trailing 12 months ending at `window_end` using the unresolved entity expression

In resolved mode, treat `mindshare` and `sentiment` as the primary analytical axes. Use `mentions` and `engagement` as secondary corroborating signals that help explain changes in perception rather than replace the main read.

Preserve the full returned time series for every metric that actually ran so you can compare:

- the anomaly pattern inside the requested window
- the window-level trend versus the entity's longer 12-month regime

For `kaito_mentions`, include only `Twitter`. Exclude every other source type from the mentions analysis because non-Twitter sources are not relevant for explaining changes in Twitter-driven social metrics.

### 3. Analysis

#### 3.1 Detect anomalies and place the window inside the 12-month trend

Analyze the current-window and 12-month series together using only the metrics available in the active resolution mode.

Find:

- unusual spikes or drops in every available metric inside the requested window
- divergence points where the available metrics move in different directions
- whether the requested window sits above, below, or near the entity's trailing 12-month baseline
- whether the window shows acceleration, deceleration, reversal, or normalization versus the longer trend

Mode-specific interpretation:

- resolved mode: focus first on mindshare and sentiment, then use mentions and engagement as secondary context and confirmation
- unresolved mode: analyze mentions and engagement together, and explicitly mark mindshare and sentiment as unavailable structured metrics

Anomaly-selection rules:

- Keep multiple anomaly windows when the data supports them.
- Treat immediately adjacent abnormal buckets as one investigation window.
- Rank anomalies by combined magnitude, persistence, and relevance across the metrics that actually ran.
- If no clear anomaly exists, say the period was trend-driven rather than event-driven and skip the anomaly drill-down step.

#### 3.2 Gather anomaly drill-down evidence

For each anomaly window, run these steps.

1. `kaito_advanced_search`
   - use the entity search filter from `Resolve Entity`:
     - resolved mode: `tokens=<RESOLVED_TOKEN>`
     - unresolved mode: `keyword=<UNRESOLVED_STRING>`
   - `sources="Twitter"`
   - `sort_by="smart_engagement"`
   - `size=100`
   - `min_created_at=<anomaly_start>`
   - `max_created_at=<anomaly_end>`
   - `exclude_handles=<EXCLUDED_HANDLES>` whenever `EXCLUDED_HANDLES` is available
   - goal: retrieve the top 100 external tweets for the entity during the anomaly window
2. contributor attribution
   - resolved mode:
     - run `kaito_mindshare_entity_by_account` for `RESOLVED_TOKEN` on the anomaly window whenever the endpoint supports window bounds
     - if the endpoint only supports a nearby preset range, use the closest available range and say so
     - use it to identify which accounts contributed the most mindshare quantitatively
   - unresolved mode:
     - skip `kaito_mindshare_entity_by_account`
     - identify the most relevant external voices directly from the anomaly-window Twitter corpus, using signal such as repeated presence, smart engagement, and prominence in the anomaly discussion
   - for the most relevant contributor handles from either mode, call `kaito_twitter_account_type` when available so you can characterize whether the anomaly was driven by KOLs, researchers or traders, builders, or community accounts
3. account follow-up search
   - run `kaito_advanced_search` for the most relevant contributor handles from the contributor-attribution step above
   - use the same entity search filter from `Resolve Entity`
   - add `usernames=<top contributor handles>`
   - use the same anomaly time bounds
   - paginate when practical so you capture all matching content from those accounts in the anomaly window
   - goal: inspect exactly what the main anomaly-driving accounts said

When choosing contributor handles for the account follow-up search, inspect the smallest set that explains the anomaly, usually the top 5 to 10 contributors or the set that clearly dominates the window.

#### 3.3 Resolve narratives for `Summary and Conclusions`

Before writing `Summary and Conclusions`, do one lightweight narrative check.

- Call `kaito_narratives` to get the canonical Kaito narrative set.
- Check whether `Summary and Conclusions` mentions any narrative from that set.
- If a mentioned narrative matches a canonical Kaito narrative, render it with the structured narrative token using the returned `narrative` value exactly as shown, but keep it embedded naturally inside the sentence that is already making the point.
- If a theme in `Summary and Conclusions` does not match the canonical narrative set, mention it in plain language only and do not invent a structured narrative token.

### 4. Output

Prefer the four-section structure below. If the user asks a specific question, answer it more directly within that structure, especially in `Summary and Conclusions`. If the user does not ask a specific question, use the same structure as the default summary or report.

Render exactly four sections in this order:

- `Summary and Conclusions`
  - lead with the most direct response to the user's request, then summarize the overall social pulse in the requested window and the main conclusion
- `Key Observations`
  - keep this section descriptive and data-first, but still tie the observations back to the user's request
  - focus on perception: in resolved mode, lead with the mindshare path and sentiment path, then use mentions and engagement as supporting context; in unresolved mode, focus on the metrics that are actually available
- `Key Insights`
  - explain why the anomalies happened in the context of the user's request
  - use the drill-down evidence from top tweets, the best available contributor attribution method for the active mode, and what those accounts actually said
- `Suggested Actions`
  - give concrete next actions that follow from the user's request and the observed perception shifts
  - focus on what the team should do because of the observed perception shifts and identified drivers

Do not add extra scorecard or benchmark sections unless the user explicitly asks for them.

`Summary and Conclusions` structured rendering rules:

- Keep this section high-level and compact. Do not restate full anomaly breakdowns, long tweet examples, or per-window metric detail there.
- If you mention an account handle in `Summary and Conclusions`, render it as `@handle`. The leading `@` is the parsing signal for frontend account rendering.
- If you mention a resolved narrative in `Summary and Conclusions`, render it as `[[narrative:<narrative>]]`, where `<narrative>` is the exact `narrative` field returned by `kaito_narratives`.
- Do not add standalone labels or trailing token lists such as `Matched narratives: [[narrative:AI]], [[narrative:L2]]`.
- Prefer natural phrasing such as `discussion concentrated around [[narrative:AI]]` instead of breaking the sentence just to surface the token.
- Keep the structured narrative token in `Summary and Conclusions` only unless the user explicitly asks for the same rendering elsewhere.

## Rules

- Always analyze the requested window together with trailing 12-month context.
- Always anchor the answer to the user's actual request. The four output sections are a response format, not a substitute for addressing the user's prompt directly.
- In resolved mode, prioritize `mindshare` and `sentiment` over `mentions` and `engagement` when framing the main story.
- Treat official and affiliate posts as owned-media noise for anomaly root-cause analysis and exclude them whenever practical.
- Keep `Key Observations` quantitative and descriptive. Do not mix in causal speculation there.
- Treat `mentions` and `engagement` as secondary evidence that helps explain or validate shifts in `mindshare` and `sentiment`, not as equal-priority headline metrics in resolved mode.
- Put causal interpretation in `Key Insights`, and tie it to tweet evidence plus the best available account-level attribution method for the active mode.
- When contributor classification is available, use it to explain the driver mix instead of only listing handles. Do not invent account roles or unsupported influence labels.
- If exclusion, pagination, or time-window support is incomplete for any endpoint, state the limitation clearly instead of hiding it.
- If the entity stayed unresolved, make the missing structured metrics explicit instead of filling the gaps with guesswork.
- If the entity stayed unresolved, say clearly that drill-down and trend analysis are keyword-based and entity precision may be weaker than in resolved-token mode.
- If no anomaly is found, say so explicitly and focus the report on long-cycle trend context.
- Say `smart accounts`, never `smart money`

## TODO

Add these planned metric extensions once the corresponding MCP endpoints exist:

1. rolling unique smart accounts
   - add a dedicated MCP endpoint for rolling unique smart-account participation over time
   - use it as an additional perception-quality signal alongside mindshare, sentiment, mentions, and engagement
2. sentiment mix
   - add a dedicated MCP endpoint for sentiment-mix breakdown over time
   - use it to enrich the sentiment read beyond a single aggregate sentiment series