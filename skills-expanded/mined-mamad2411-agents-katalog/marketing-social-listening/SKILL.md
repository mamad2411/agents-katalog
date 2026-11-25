---
name: marketing-social-listening
description: Cluster the top 100 highest-signal tweets for a resolved or user-specified crypto project into hot topics using Kaito MCP tools. Use this skill when the user wants a past-window social listening report with topic tagging, author enrichment, urgency scoring, and concrete response guidance.
---

## Preamble (run first)

```bash
_KS_REPO=""
_KS_REAL_SKILL="$(cd "$HOME/.claude/skills/marketing-social-listening" 2>/dev/null && pwd -P || true)"
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

# Social Listening

Use this skill for the redesigned hot-topics social listening workflow.

## Inputs

- `token`: project name, ticker, or resolved Kaito token value; optional only when an upstream workflow already supplies `unresolved_string` plus a confirmed `official_handle`
- `official_handle`: optional upfront hint; required whenever unresolved mode is finalized
- `unresolved_string`: optional prebuilt keyword string from `shared-entity-resolution`; use it only when it already comes with a confirmed `official_handle`
- `duration`: `24h`, `48h`, `7d`, `30d`, `90d`, or an explicit past window with `start` and `end`
- `focus_mode`: `preset` or `custom` (default `preset`)
- `preset_topics`: optional multi-select. Default to all current preset topics:
  - `Engagement opportunities`
  - `Risk watch`
  - `Key voices`
  - `Emerging narratives`
  - `Product discussion`
  - `Market discussion`
  - `Bugs & issues`
  - `Competitor comparisons`
  - `Questions & evaluation`
  - `Feature requests`
- `custom_topic_focus`: optional free text used only when `focus_mode="custom"`
- `excluded_handles`: optional exclusion set that should be merged with canonical official and affiliate handles when already known. For unindexed fallback mode, this usually contains only the confirmed official handle.
- `max_tweets`: fixed at `100`

## Workflow

Organize the workflow into four stages: `Resolve Entity`, `Data Gathering`, `Analysis`, and `Output`.

### 1. Resolve Entity

Resolve the project identity, exclusion set, and exact analysis window before pulling any tweets.

Use `shared-entity-resolution` first unless an upstream workflow already hands you a confirmed unresolved identity package.

- If `unresolved_string` is already supplied together with a confirmed `official_handle`, treat that pair as the unresolved identity package from `shared-entity-resolution` and do not rebuild it.
- Otherwise, follow `../shared-entity-resolution/SKILL.md` for all token ambiguity handling, official-handle research, handle confirmation, and unresolved keyword-string construction.
- Carry forward the identity package returned by `shared-entity-resolution`:
  - resolved mode: `RESOLUTION_MODE = resolved`, `RESOLVED_TOKEN = <kaito token>`, plus `OFFICIAL_HANDLE` and `AFFILIATE_HANDLES` when available from `kaito_twitter_official_account`
  - unindexed mode: `RESOLUTION_MODE = unresolved`, `OFFICIAL_HANDLE = <confirmed official handle>`, and `UNRESOLVED_STRING = <keyword string>`
- Do not re-ask the user to restate the whole project if `shared-entity-resolution` has already narrowed the identity down to one handle candidate that only needs confirmation.
- Treat `OFFICIAL_HANDLE` as mandatory before continuing in unindexed mode.
- In resolved mode, identify the project display name and official X handle when available so the report header and exclusion filters use the correct account identity.
- In resolved mode, if the carried identity package is missing `OFFICIAL_HANDLE` or `AFFILIATE_HANDLES`, call `kaito_twitter_official_account` for `RESOLVED_TOKEN` before building exclusions.
- Build `DISPLAY_PROJECT_NAME` for output rendering:
  - prefer the resolved project display name when available
  - otherwise fall back to `@<OFFICIAL_HANDLE>`
- Build a reusable project search filter for downstream steps:
  - resolved mode: `PROJECT_SEARCH_FILTER = tokens=<RESOLVED_TOKEN>`
  - unindexed mode: `PROJECT_SEARCH_FILTER = keyword=<UNRESOLVED_STRING>`
- Build `EXCLUDED_HANDLES` as an optional exclusion set when the needed handles are known:
  - resolved mode: include the canonical official X handle plus any affiliate handles returned by `kaito_twitter_official_account`, then merge any extra confirmed `excluded_handles`
  - unindexed mode: include the confirmed official X handle plus only any extra `excluded_handles` that were already confirmed upstream
- In unindexed mode, do not invent affiliate handles. If only the official handle is confirmed, exclude only that handle.
- Convert any relative duration into exact `window_start` and `window_end` timestamps and use those exact bounds throughout the workflow.

### 2. Data Gathering

#### 2.1 Fetch the top 100 tweets first

Always pull the full broad corpus before topic filtering.

Run `kaito_advanced_search` five times in parallel with:

- `sources="Twitter"`
- the project search filter from `Resolve Entity`: `tokens=<RESOLVED_TOKEN>` in resolved mode or `keyword=<UNRESOLVED_STRING>` in unindexed mode
- `exclude_handles=<EXCLUDED_HANDLES>` whenever `EXCLUDED_HANDLES` is available
- `sort_by="smart_engagement"`
- `size=20`
- `from=0`, `20`, `40`, `60`, and `80`
- `min_created_at=<window_start>`
- `max_created_at=<window_end>`

Rules for the search stage:

- Do not prefilter by preset topics or custom focus. Fetch the same top 100 tweet corpus first, then apply focus during clustering and ranking.
- Exclude tweets authored by the official project handle and any known affiliate handles. This workflow is for external conversation, not owned-media output.
- In unindexed mode, exclude only the confirmed official handle. Do not guess or invent affiliate handles.
- In unindexed mode, run a quick query-quality check before trusting the full corpus:
  - inspect the first-page results and confirm they are materially about the intended project
  - if the query is noisy, tighten `UNRESOLVED_STRING` by removing ambiguous names and keeping only low-ambiguity aliases plus the handle
  - if the query is still noisy after refinement, pause and confirm the handle or alternate project names with the user before continuing
- Treat `EXCLUDED_HANDLES` as required retrieval logic whenever those handles are known:
  - pass `exclude_handles=<EXCLUDED_HANDLES>` directly in every Twitter corpus pull
  - if `EXCLUDED_HANDLES` is unavailable because the relevant handles are still unknown, continue with the smaller known exclusion set instead of inventing handles
- If the official handle has not been confirmed yet, stop and confirm it before proceeding with unindexed mode.
- Deduplicate by tweet ID after pagination.
- Keep replies and quote tweets if they rank in the top corpus, but still exclude them whenever the author is known to belong to `EXCLUDED_HANDLES`.
- If fewer than 100 tweets are returned, proceed with the available set and say so in the output.
- If the project is unindexed, say clearly that the corpus is keyword-based and entity precision may still be weaker than in resolved-token mode even with a confirmed handle.

#### 2.2 Enrich authors once and reuse the data

Build a unique author list from the fetched tweets and cache one author profile per handle.

For each unique author:

1. use `kaito_get_twitter_user` when `author_user_id` is available so you can retrieve:
   - display name
   - username
   - profile image / avatar
   - bio and classification when helpful for interpretation
2. use `kaito_smart_followers` in `count` mode for every unique author so you always have the latest normalized smart-follower count
3. use `kaito_twitter_account_type` for every unique author handle when available so you can retrieve:
   - account type classification
   - crypto role
4. determine whether the author is `new` or `existing` by checking for historical mentions of the same project before the current analysis window:
   - call `kaito_advanced_search` with:
     - `sources="Twitter"`
     - `usernames=<author_handle>`
     - the same project search filter from `Resolve Entity`:
       - `tokens=<RESOLVED_TOKEN>` when the token is resolved
       - `keyword=<UNRESOLVED_STRING>` for unindexed projects
     - `size=1`
     - `sort_by="relevance"`
     - `max_created_at=<window_start_minus_1s>`
   - use all available history before the current window, not the current window itself
   - search against the full project entity expression for the active mode, not only the resolved-token path
   - if at least one prior matching tweet is found, set `existing="existing"`
   - if no prior matching tweet is found, set `existing="new"` only when the project search filter includes at least one sufficiently unique project name or alias in addition to the handle
   - if no prior matching tweet is found and the unindexed filter is effectively handle-only, set `existing="unknown"` instead of `new` because recall is too weak
   - if the historical query cannot be completed or the handle is unavailable, set `existing="unknown"`

Author-enrichment rules:

- Do not rely on the search result's author smart-follower count as the primary source. Always refresh it with `kaito_smart_followers` because the search payload can be stale or return `0`.
- Use the search result's smart-follower count only as a last-resort fallback when the dedicated `kaito_smart_followers` call fails.
- Use `kaito_twitter_account_type` as the primary source for `role` when the call succeeds.
- Always derive `tier` from the refreshed smart-follower count using the thresholds below.
- Every tweet shown in the final output must display: avatar, display name, handle, smart followers, smart engagement, `existing`, `role`, and `tier`.
- If avatar or profile metadata is unavailable, leave it blank rather than inventing values.

Author-status fields:

- `existing`: `new | existing | unknown`
  - classify this by checking whether the author mentioned the same project before the current window
  - use `kaito_advanced_search` with `usernames=<author_handle>`, `max_created_at=<window_start_minus_1s>`, and the same project search filter from `Resolve Entity`
  - if there is at least one prior match, use `existing`
  - if there are no prior matches and the search filter includes at least one sufficiently unique project name or alias, use `new`
  - if there are no prior matches but the unindexed search filter is handle-only, use `unknown`
  - use `unknown` only when the lookup cannot be completed reliably
- `role`: `research/trader | builder | kol | community member | unknown`
  - this is a role classification field, not a boolean researcher flag
  - this should come from `kaito_twitter_account_type`
  - normalize the endpoint output into the allowed UI values above when needed
  - if the endpoint is unavailable or does not return a confident role, use `unknown`
  - keep the output lowercase and structured for UI rendering
- `tier`: `mega | large | medium | small | micro | unknown`
  - convenience UI size tier derived from smart-follower count for frontend rendering
  - definition:
    - `mega` when `smart_followers > 2000`
    - `large` when `1000 <= smart_followers <= 2000`
    - `medium` when `300 <= smart_followers < 1000`
    - `small` when `100 <= smart_followers < 300`
    - `micro` when `smart_followers < 100`
  - if smart-follower data is unavailable, use `unknown`
  - keep the output lowercase and structured for UI rendering
  - this is a simplified UI tier; still show the raw smart-follower count separately

### 3. Analysis

#### 3.1 Score each tweet for urgency and actionability

For every tweet, assign:

- `urgency`: `not urgent`, `low urgency`, `moderate urgency`, or `urgent`
- `urgency_reason`: one short sentence explaining why
- `suggested_action`: one concrete response line that combines the action and objective in a single field

#### Urgency definitions

- `urgent`: high-leverage content that should be handled in the current monitoring cycle. Usually combines at least two of:
  - high-author importance such as `mega` or `large` smart-follower tier, major media, major partner, major investor, or another clearly influential external voice
  - unusually high smart engagement for the corpus
  - time-sensitive content such as bugs, outages, misinformation, serious competitor framing, high-quality evaluation threads, or influential endorsements that are still open for engagement
- `moderate urgency`: meaningful signal worth replying to, amplifying, clarifying, or monitoring in the next response cycle, but it is not yet a current-cycle escalation
- `low urgency`: low-spread or weakly actionable content that is still worth logging and lightly monitoring
- `not urgent`: repetitive, stale, purely contextual, or non-actionable content that can be recorded without near-term follow-up

The `urgency_reason` must cite the actual drivers, such as author importance, smart engagement, content sensitivity, novelty, or timing.

#### Suggested actions

Use `suggested_action` as a single output field. Write it as:

- `<action> + <objective>`
- example: `Reply now to amplify product angle`

UI brevity rules for `suggested_action`:

- Keep it short enough for a compact UI chip or single-line field.
- Target 2 to 6 words and stay under roughly 60 characters.
- Do not include rationale, evidence, account names, metrics, lists, or multiple clauses.
- Do not write a paragraph after `Suggested Action:`. The explanation belongs in `urgency_reason` or the topic overview, not in the action field.

Use a concrete communications or product action, not trading advice. Good action verbs include:

- `Reply now`
- `Amplify from official account`
- `Clarify now`
- `Route to support`
- `Route to product`
- `DM / follow up privately`
- `Prepare internal brief`
- `Monitor only`

#### Objective guidance

Each `suggested_action` should still carry one clear objective. Common objectives include:

- `Amplify product angle`
- `Convert evaluator into advocate`
- `Correct misinformation`
- `Contain reputational risk`
- `Support affected users`
- `Reinforce competitive differentiation`
- `Collect product feedback`
- `Build relationship with key voice`
- `Track signal without overreacting`

Suggested actions should match the tweet:

- strong positive product commentary from a key voice -> `Reply now to amplify product angle` or `Amplify from official account to extend third-party validation`
- credible skeptical question -> `Reply now to convert evaluator into advocate`
- bug report or outage claim -> `Route to support to help affected users` or `Clarify now to contain reputational risk`
- competitor comparison -> `Reply now to reinforce competitive differentiation` or `Prepare internal brief to align the team on response`
- low-signal praise or stale commentary -> `Monitor only to track signal without overreacting`

#### 3.2 Cluster tweets into hot topics

Cluster the fetched tweets into coherent hot topics using tweet content, author context, smart engagement, and the selected focus.

Hot-topic rules:

- Build topic groups around a concrete discussion thread or narrative angle, not around generic sentiment buckets.
- Each hot topic should contain a short title, a concise thesis, and the ordered list of supporting tweets.
- Rank tweets inside each topic by smart engagement first, then by author importance, then by recency.
- Aim for selective topics rather than exhaustive fragmentation. Merge obviously overlapping clusters.

#### 3.3 Apply topic focus and tagging

The output tagging system uses the current preset topic taxonomy plus `Other`:

- `Engagement opportunities`
- `Risk watch`
- `Key voices`
- `Emerging narratives`
- `Product discussion`
- `Market discussion`
- `Bugs & issues`
- `Competitor comparisons`
- `Questions & evaluation`
- `Feature requests`
- `Other`

Tagging rules:

- Multi-tagging is allowed. Assign up to 3 labels per topic when justified.
- Use `Other` only when none of the current preset labels fit.
- If `focus_mode="preset"`, default to all current preset topics selected. If the user narrows the preset multi-select, prioritize and keep topics that match the selected preset labels.
- If `focus_mode="custom"`, use `custom_topic_focus` to change clustering and prioritization logic, but do not invent new output labels. Final topics must still be tagged with the current output taxonomy.

Use these label definitions:

- `Engagement opportunities`: clear chances to reply, quote, thank, or build a relationship
- `Risk watch`: negative claims, controversy, misinformation, or reputation-sensitive discussion
- `Key voices`: clusters dominated by important accounts or notable new entrants
- `Emerging narratives`: new or accelerating storylines
- `Product discussion`: features, launches, integrations, usage, demos, or UX
- `Market discussion`: price, valuation, flows, listings, or trading-related discussion
- `Bugs & issues`: reliability problems, exploits, outages, broken flows, or support pain
- `Competitor comparisons`: direct versus framing, category benchmarks, or substitution arguments
- `Questions & evaluation`: due-diligence threads, skeptical questions, or evaluative discussion
- `Feature requests`: explicit asks for missing or improved functionality
- `Other`: relevant discussion that does not fit the preset taxonomy

#### 3.4 Compute topic-level rollups

For each hot topic, compute:

- `tweet_count`: total number of tweets in the topic
- `total_smart_engagement`: sum of smart engagement across all tweets in the topic
- `urgency`: the highest urgency found in any tweet in the topic
- `key_accounts`: the most important or most repeated authors in the cluster

Topic-ranking rules:

- Order hot topics by highest topic urgency first using `urgent > moderate urgency > low urgency > not urgent`, then total smart engagement, then tweet count.
- A topic inherits the highest urgency found in its tweets using the same severity order: `urgent > moderate urgency > low urgency > not urgent`.
- Use the aggregate metrics in both the topic summary card and the detailed section.

#### 3.5 Resolve narratives for the summary

Before writing the `Summary`, do one lightweight narrative check.

- Call `kaito_narratives` to get the canonical Kaito narrative set.
- Check whether the `Summary` mentions any narrative from that set.
- If a mentioned narrative matches a canonical Kaito narrative, render it with the structured narrative token using the returned `narrative` value exactly as shown, but keep it embedded naturally inside the sentence that is already making the point.
- If a theme in the `Summary` does not match the canonical narrative set, mention it in plain language only and do not invent a structured narrative token.

### 4. Output

Prefer the output structure below. If the user asks a specific question, answer it more directly within that structure, especially in `Summary`. If the user does not ask a specific question, use the same structure as the default summary or report.

Start with a `Summary` section in exactly three short paragraphs:

1. the most direct response to the user's request, together with the overall conclusion for the selected project and time window
2. the most important hot topics, the most important accounts driving them, and any resolved narratives that matter most
3. the most important suggested actions and the objectives embedded in them

Summary-only structured rendering rules:

- Do not add a standalone report title before `Summary`. The UI can render the project name and time window separately.
- When the UI or surrounding workflow needs a project label, use `DISPLAY_PROJECT_NAME`.
- Keep each summary paragraph compact: no more than 2 sentences per paragraph.
- Keep `Summary` high-level. Do not restate full topic cards, long tweet examples, or per-topic metric breakdowns there.
- Mention only the most important 1 to 2 themes and the most important actions at a high level.
- If you mention an account handle in the `Summary`, render it as `@handle`. The leading `@` is the parsing signal for frontend account rendering.
- If you mention a resolved narrative in the `Summary`, render it as `[[narrative:<narrative>]]`, where `<narrative>` is the exact `narrative` field returned by `kaito_narratives` such as `AI` or `L2`. The `[[narrative:...]]` wrapper is the parsing signal for frontend narrative rendering, but it must appear inline in natural prose.
- Do not add standalone labels or trailing token lists such as `Matched narratives: [[narrative:AI]], [[narrative:L2]]`.
- Prefer wording like `discussion concentrated around [[narrative:AI]] and [[narrative:L2]]` instead of breaking the sentence to enumerate matches mechanically.
- Keep this structured narrative token in the `Summary` only. The `Hot Topics` section does not need this special rendering.

Then add `Hot Topics`.

For each hot topic, show:

- topic title
- topic labels from the current output taxonomy, with up to 3 labels when applicable
- overview explaining what the topic is about and why it matters in this time window
- `Tweets: N`
- `Smart Engagement: N`
- `Urgency: not urgent | low urgency | moderate urgency | urgent`
- key accounts

Hot-topic formatting rules:

- Topic cards are summary containers only. They should contain exactly the topic-level fields above plus the tweet list below, and nothing else.
- Use the exact tag labels from the taxonomy. Do not change capitalization or wording.
- `Urgency` must be one of the exact lowercase values: `not urgent`, `low urgency`, `moderate urgency`, or `urgent`.
- `Smart Engagement` must be a numeric aggregate, not qualitative text such as `High` or `Medium`.
- `key accounts` should be a short comma-separated list, preferably handles only.
- Do not add a topic-level `Suggested Action` paragraph or any extra block such as `Source Credibility`.
- The topic `overview` can be 2 to 3 short sentences. The first sentence is the most important and should work as the compact card summary; the full 2 to 3 sentences can be used in the detail view.
- Do not add separate topic-level prose sections such as `Why it matters`, `Recommended response`, `Takeaway`, or `Source notes` outside the single `overview` field.
- Keep the topic body compact for UI scanning. Show at most 5 tweets per topic, prioritized by smart engagement and author importance.

Then list the tweets in that topic. Every tweet entry must include:

- avatar
- display name
- handle
- smart followers
- smart engagement
- existing
- role
- tier
- tweet text or a concise factual summary
- tweet URL
- `Urgency: <level> - <reason>`
- `Suggested Action: <action + objective>`

Tweet-entry formatting rules:

- Tweet entries are the only place where `Suggested Action` appears.
- Do not render tweets as markdown tables. Use one compact entry per tweet so the UI can map fields cleanly.
- Use a real tweet URL, never a placeholder such as `link`.
- Keep the tweet text as the original text or a concise factual summary only.
- Do not add unsupported fields such as `Source Credibility`, free-form sentiment columns, or long prose after the tweet entry.
- `Suggested Action` must remain a short single line, not a mini recommendation paragraph.
- `existing`, `role`, and `tier` must stay structured and compact. Do not replace them with prose.

## Rules

- This workflow is content-first and topic-first, not KPI-first.
- Always anchor the answer to the user's actual request. The output structure is a response format, not a substitute for addressing the user's prompt directly.
- Always fetch the top 100 tweets for the resolved ticker or the confirmed keyword-based project query before applying focus logic.
- The top-tweets corpus should reflect external discussion only, excluding the project's own handle and any known affiliate handles when available.
- The summary and topic sections must use the exact selected time window, not a fuzzy rolling description.
- Do not invent author identity, avatar, or account role. Use factual profile data only.
- Keep `suggested_action` tied to the actual tweet, author context, and embedded objective.
- Keep actions practical for comms, community, support, or product teams.
- Do not output trading advice or market calls such as `buy signal`, `sell signal`, or price-target language.
- Do not include owned or affiliated project accounts in the external-conversation topic corpus or topic tweet lists. In unindexed mode, enforce this only for handles you actually know.
- If the project is unindexed or keyword-only, say so explicitly and note any limitations around entity precision, existing-voice recall, affiliate exclusion, and structured token-dependent coverage.
- If the dataset is sparse, say so directly rather than overstating confidence.
- Say `smart accounts`, never `smart money`.
