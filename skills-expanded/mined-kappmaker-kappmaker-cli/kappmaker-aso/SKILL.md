---
name: kappmaker-aso
description: Research App Store keywords for a KAppMaker app via the Astro MCP and produce the keyword report — primary keywords, sub-niche clusters, and what was discarded and why. Use when the user asks about ASO, app store keywords, search ranking or which keywords to target. For writing the actual title, subtitle and keyword fields use kappmaker-aso-metadata.
---

# KAppMaker — ASO Keyword Research

## Before starting

**Read `AiGuidelines/` first** — the PRD and positioning already answer most questions. This is a
skill-driven procedure: you (Claude) execute it with your own tools. No `kappmaker` binary is
involved and none needs to be installed.

### ASO Keyword Research — Find high-value keywords via Astro MCP

This is a **skill-driven procedure**, not an external CLI command. You (Claude) drive it using the [Astro MCP](https://tryastro.app/docs/mcp/) tools (real-time App Store search data, competitor keywords, popularity + difficulty scores) when they're available in the session, and write the curated keyword list to `AiGuidelines/keywords.md` for the user to review and feed into other ASO commands.

Output of this workflow is the natural input to the **Localize ASO Metadata** workflow below — research first, then expand the chosen keywords across the 9 US-indexed locales with `mode=keyword-expansion`.

**Trigger phrases**:
- `Using kappmaker, research keywords for <base keyword>`
- `Using kappmaker, find aso keywords [for/around/related to] <topic>`
- `Using kappmaker, keyword research <base>`
- "find keywords", "keyword research", "aso keyword discovery", "find sub-niche keywords"

**Argument parsing**:
- `base` / `base keyword` — required eventually, but can be derived if missing. Resolution order:
  1. Explicit value in the user message (`base="ai image generator"` or in-line: "research keywords for AI image generator")
  2. If a PRD / app idea / app description file exists in the project (e.g. `AiGuidelines/prd.md`, `AiGuidelines/app-idea.md`, or any `*.md` under `AiGuidelines/` that reads like a product description; fall back to the project `README.md`), read it and pick the strongest noun phrase that describes the app's core function. Confirm the choice with the user before proceeding.
  3. If `MobileApp/distribution/ios/appstore_metadata/texts/en-US/name.txt` + `subtitle.txt` exist, infer the base keyword from those (e.g. name=`Drift Tuner`, subtitle=`Real-Time Drift Coach` → base=`drift coaching`). Confirm with the user.
  4. As a last resort, ask the user directly.
- `competitors` — optional, comma-separated list of competitor app names or App Store IDs. If omitted, the workflow discovers top apps for the base keyword via `search_app_store`.
- `min_popularity` — optional, default **30**
- `max_difficulty` — optional, default **45**
- `target_count` — optional, default **30–50** unique keywords after filtering
- `output` — optional, default `AiGuidelines/keywords.md`

#### Preflight: check Astro MCP availability

Before proceeding, verify that at least these Astro MCP tools are visible in the current session: `search_app_store`, `extract_competitors_keywords`, `get_keyword_suggestions`. (Names may vary slightly between Astro MCP versions — `list_apps`, `add_app`, `get_app_keywords`, `track_app`, etc. are also useful when available.)

If none of those tools are present:
- Tell the user: `"Astro MCP is not connected in this session. The keyword-research workflow needs it for popularity/difficulty data. Either install/connect Astro MCP (see https://tryastro.app/docs/mcp/), or I can do a best-effort brainstorm without scores — say 'brainstorm without astro' to continue."`
- On `brainstorm without astro` (or equivalent), fall back to the **Manual brainstorm fallback** procedure below — generate ~30 sub-niche candidates via your own knowledge, mark scores as `?`, and tell the user to validate them on App Store Connect or a separate ASO dashboard.

#### Procedure (with Astro MCP)

1. **Discover competitor apps**
   - Call `search_app_store({ query: <base> })` to get the top live apps ranking for the base keyword.
   - Pick the top 5–10 most relevant ones (skip mega-apps with unrelated reach, e.g. don't include "Google" when researching "manga translator"). Note their `app_id` (App Store ID).
   - If the user passed `competitors=`, prefer those; supplement with discovery results up to 10 total.

2. **Track competitor apps in Astro** (so their keyword data is available)
   - If a `list_apps` tool exists, call it first to see which competitors are already tracked.
   - For each untracked competitor, call `add_app` / `track_app` with the App Store ID. Some tools require platform (`ios` / `android`) — default to `ios` unless the user is Android-only.
   - If `add_app` returns a quota error (free-tier limits), surface it to the user and proceed with whatever competitors got tracked. Don't abort.

3. **Extract competitor keywords**
   - For each tracked competitor, call `extract_competitors_keywords({ app_id: <id> })` (or `get_app_keywords`). Collect every returned keyword along with its `popularity` and `difficulty` scores. Tag each with the source competitor app name.

4. **Expand with AI suggestions**
   - Call `get_keyword_suggestions({ base_keyword: <base> })` (and/or per-competitor if the tool supports it). Add those to the candidate pool.

5. **Filter and dedupe**
   - Drop any keyword where `popularity < min_popularity` OR `difficulty > max_difficulty`.
   - Remove exact duplicates (case-insensitive). For near-duplicates (singular/plural pairs, e.g. `ai photo editor` / `ai photo editors`), keep the one with higher popularity unless both score well.
   - Drop keywords that are clearly off-topic (e.g. a "fitness" keyword surfaced from a competitor that also happens to sell supplements when researching "workout planner"). Use the base keyword as the relevance anchor — when in doubt, prefer keeping the keyword if it could plausibly match the app's value prop.
   - Aim for `target_count` (30–50) unique, relevant entries. If you have fewer after filtering, relax `max_difficulty` by +5 and retry the filter once — tell the user you did so.

6. **Cluster into sub-niches**
   - Group the filtered keywords by semantic cluster (e.g. for "AI image generator": `text-to-image`, `image editing`, `style transfer`, `avatar / portrait`, `interior design`, `try-on`, etc.).
   - Each cluster becomes a section heading in the output. This makes the file directly usable by `localize-metadata mode=keyword-expansion` (each cluster maps cleanly to one of the 9 indexed locales).

7. **Write `AiGuidelines/keywords.md`**
   - Use the **Output format** below.
   - Create the `AiGuidelines/` directory if it doesn't exist.
   - If a previous `AiGuidelines/keywords.md` exists, ask once before overwriting: `"AiGuidelines/keywords.md already exists. Overwrite? [y/N]"`. On `N`, write to `AiGuidelines/keywords-<ISO-date>.md` instead.

8. **Print a short console summary**: total candidates → filtered count → final clusters → file path. Then suggest the next step:
   ```
   Next: run `Using kappmaker, localize metadata mode=keyword-expansion keywords="..."` with these keywords to fan them across the 9 US-indexed locales.
   ```

#### Output format

Write `AiGuidelines/keywords.md` exactly as specified in `references/keywords-md-format.md` —
header with base/filters/sources, a top-5 "Recommended primary keywords" table, one table per
sub-niche cluster, and a "Discarded" table showing what the filters rejected and why. The
cluster-per-section structure is what `localize-metadata mode=keyword-expansion` consumes
downstream.

#### Manual brainstorm fallback (when Astro MCP is unavailable)

If the user chose to brainstorm without Astro MCP:

1. Use your own knowledge of the App Store category around the base keyword to generate 30–50 sub-niche candidates. Cluster them the same way (sub-niche groupings).
2. Mark `Popularity` and `Difficulty` columns as `?` (unknown) so the user understands these aren't measured numbers — they're hypothesis-only.
3. In the file header, add a prominent note: `> ⚠️ Popularity/difficulty scores are NOT included — Astro MCP was unavailable. Validate these candidates on App Store Connect, [Astro](https://tryastro.app/docs/mcp/), AppTweak, or Sensor Tower before using them in production listings.`
4. Skip the "Discarded" section (there's nothing to filter against).

The file structure (clusters + recommended primary keywords) stays the same so the user gets the same downstream value.

#### Tips and edge cases

- **Free-tier rate limits**: Astro free tier limits tracked-app count. If `add_app` fails with quota error, work with whatever competitors are already tracked + AI suggestions. Don't abort.
- **Very narrow niches**: if the base keyword is hyper-specific (e.g. "vintage manga panel translator"), `extract_competitors_keywords` may return only 5–10 keywords post-filter. That's fine — write them all and let the user know the niche is small.
- **Very broad keywords**: if the base is generic (e.g. "ai", "photo"), the candidate pool will be huge and the filter cutoffs may still leave 200+ entries. Cap output at `target_count × 1.5` and tell the user to narrow the base.
- **Multi-language base**: if the user's base keyword is non-English, the App Store search results are localized — Astro returns keywords in that language. The workflow still works; just note in the file header which storefront / language the data is for.
- **Chain to localize-metadata**: at the end of `AiGuidelines/keywords.md`, include a ready-to-paste command line suggestion using the top ~10 keywords:
  ```
  Using kappmaker, localize metadata mode=keyword-expansion keywords="<10 picks comma-separated>"
  ```

---

## Where this sits in the flow

- **Before this:** The app's positioning in `AiGuidelines/`.
- **After this:** **kappmaker-aso-metadata** — turn the chosen keywords into the actual title, subtitle and keyword fields.
