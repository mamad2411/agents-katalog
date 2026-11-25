---
name: yugioh-assistant-mcp
description: Yu-Gi-Oh! AI Judge, Meta Deck Builder, YDK/YDKE Parser, Lua Script Validator, Batch Art Slicer, and Multi-Market Pricing Assistant.
---

# Yu-Gi-Oh! Assistant

Skill for Claude Code and any AI agent working on Yu-Gi-Oh! Trading Card Game tasks (TCG, OCG, Asian-English AE, Genesys, Master Duel). The server runs over MCP stdio; without MCP, use the CLI `ygo call <tool>` with the same parameters.

## 0. Tool-first rule (hard requirement)

The tools are the source of truth. Training-data recall is not a source, even when it feels certain.

- **Never state a card fact, passcode, stat line, banlist status, price, tier list or ruling from memory — including inside a private reasoning/thinking block.** Thinking happens before the client schedules a tool call; drafts written there are still ungrounded and must not reach the answer.
- **Never output a decklist before calling a tool.** A decklist is valid only when it comes from `ygo_build_meta_deck` (or `ygo_parse_deck` / `ygo_optimize_deck` for an existing list) and has passed `ygo_check_legality`. Do not add, swap or "fix" cards by hand.
- **If a tool returns `available: false`, an empty result or an error**, report that fact with the tool's own `reason`. Never substitute another deck, card or archetype to fill the gap.
- **User-supplied lists** (`.ydk` path, raw `.ydk` text, `ydke://` link) go through `ygo_parse_deck` or `ygo_check_legality`; do not transcribe them by hand.
- **Quote the evidence** the tool returns: format, banlist limits, legality errors, freshness score, script provenance. An answer without that evidence is a guess.
- **AI answers are not guaranteed to be correct, and neither are tool answers.** Treat every result as a lead to verify, not a final authority. When a tool answer matters (a ruling, a banlist status, a price), say what it is based on and tell the user to check the cited source before acting. Never present a result as certain when the tool reports low confidence, `available: false`, stale data or a missing source.

If the user asks for something the tools cannot answer, say so explicitly instead of filling the gap with recall.

## 1. When to activate

Activate automatically when the user mentions:

- Deck analysis, reading/exporting `.ydk` files, `ydke://` links.
- Community decklists ("what are people building", "show me tournament decks for an archetype") and published combo lines.
- Legality checks and banlist compliance per format (TCG, OCG, AE, Genesys, Master Duel).
- Market questions: most expensive card, what is rising or falling, why a price moved, budget picks ("under $5").
- Rulings (Negate Activation vs Negate Effect, Miss Timing, Cost vs Effect, Damage Step, Fast Effect Timing, SEGOC).
- Looking up CardScript Lua code (`c<id>.lua`) from ProjectIgnis / ocgcore.
- Finding cards by stats and combo lines (searchers already in the deck, or bridging searchers).
- Building meta decks for 2025/2026 for the archetypes in the live tier list (use `ygo_get_monthly_meta` / `ygo_find_community_decks` to name them) with a 40–60 card Main Deck.
- Registering newly revealed cards (temp ID 990000000+, Lua compiled from the card text, migrate to the passcode later) and testing them on the engine with `ygo_test_custom_card`.
- Batch grid artworks (2x2, 3x3) to save tokens, then slicing each cell.
- Exporting a decklist PDF on the original Konami `KDE_DeckList.pdf` form; rendering a Konami Neuron-style deck PNG; printing real-size proxy sheets (59 x 86 mm on A4).
- Multi-market pricing: TCGPlayer (US), Yuyu-tei (JP), TCGCorner (AE).
- New card news from the YGOrganization RSS feed and Konami rulebook lookups.

## 2. Tool map (56 tools)

**Deck:** `ygo_parse_deck` · `ygo_check_legality` · `ygo_export_deck` · `ygo_build_meta_deck` · `ygo_optimize_deck` · `ygo_find_synergy_and_combos` · `ygo_find_community_decks` · `ygo_find_combos` · `ygo_find_counters` · `ygo_compare_decks` · `ygo_consistency_lab` · `ygo_matchup_planner` · `ygo_deck_cost`

**Card database:** `ygo_get_card` · `ygo_card_dossier` · `ygo_search_cards`

**Rulings & simulation:** `ygo_judge_card` · `ygo_analyze_lua` · `ygo_script_insights` · `ygo_judge_interaction` · `ygo_get_rulebook` · `ygo_get_policy` · `ygo_wiki` · `ygo_judge_scenario` · `ygo_verify_ruling` · `ygo_check_locks` · `ygo_golden_suite` · `ygo_ensure_script` · `ygo_simulate_duel_scenario` · `ygo_run_duel` · `ygo_ai_benchmark` · `ygo_export_selfplay`

**Meta & banlist:** `ygo_get_monthly_meta` · `ygo_compare_monthly_meta` · `ygo_get_daily_meta` · `ygo_sync_meta`

**Prices & news:** `ygo_market_query` · `ygo_check_prices` · `ygo_card_printing_prices` · `ygo_get_card_price_trends` · `ygo_get_trending_cards` · `ygo_get_news`

**Tournament paperwork:** `ygo_generate_tournament_decklist_pdf` · `ygo_render_deck_image` · `ygo_generate_proxy_pdf`

**Custom cards & archetype studio:** `ygo_create_custom_card` · `ygo_test_custom_card` · `ygo_migrate_temp_card` · `ygo_generate_batch_art_prompt` · `ygo_slice_batch_art` · `ygo_create_archetype_docx` · `ygo_read_and_validate_docx` · `ygo_export_database_and_scripts` · `ygo_generate_art_prompts` · `ygo_slice_art_grid` · `ygo_build_full_pipeline`

Full parameter lists: run `ygo call <tool> --help`, `ygo tools --verbose`, or read `docs/TOOLS.md`.

## 3. Standard workflows

### A. Deep search & combos

The user asks something like *"find a 1850 ATK Spellcaster for my deck and show me how to search it"*:

1. `ygo_find_synergy_and_combos` with `filter: { race: "Spellcaster", atk: 1850 }` and the user's deck.
2. The engine matches searchers already in the deck (for example a card that sends another card to the GY as material), emits the step-by-step combo and suggests a payoff already present in the pool.

### B. Rulings

0. **Start with the dossier**: `ygo_card_dossier` returns the database record, the wiki record (12 language names, Card Database ID, which tabs exist), the script provenance and — with `includeRulings: true` — the rulings summary. One call instead of three.
1. `ygo_judge_card` with `passcode` **or `cardName`** — reads the real Lua script: HOPT/SOPT, cost, targeting, miss timing, Damage Step, negate activation vs negate effect. It reports `script.provenance` and attaches rulebook + PSCT citations automatically; if no script exists it tells you to run `ygo_ensure_script`.
2. For two or more cards: `ygo_judge_interaction` with a `question` that states the exact board and chain.
3. For the general rules framework: `ygo_get_rulebook` with `topic: "official"` + `query` — returns **verbatim Konami PDF text** with printed page numbers (e.g. Damage Step → p.41). Use `topic: "section"` to read a whole section, `topic: "page"` for one page, `topic: "status"` for the loaded edition (version, fetch date, SHA-256). The `timing`/`damage_step`/`segoc`/`mechanics` topics are curated summaries — always prefer the verbatim quote when citing rules.

### B2. Tournament judging (policy, penalties, procedure)

Judge corpus: `ygo_get_policy`. Covers Tournament Policy (KDE-US), Infractions & Penalties, Speed Duel/Remote Duel addenda, Fast Effect Timing, Advanced Rules, the PSCT series, Judge Program and Judge FAQ.

1. `topic: "list"` to see the 19 documents and their versions.
2. `topic: "search"` + `query` for real questions ("penalty for intentionally drawing an extra card", "slow play", "appeal", "marked cards", "deck check"). Returns verbatim text plus `document`, `version` and `page`.
3. `topic: "section"` + `document` + `query` to read a whole section (e.g. `tournament-policy` + "Appeals").
4. `topic: "page"` + `document` + `page` to read one page in full.
5. `topic: "status"` (+ `refresh: true`) to check freshness and re-sync.

Ruling procedure: identify the infraction → look up `penalties` for the penalty range (Warning / Game Loss / Match Loss / Disqualification) → if it is procedure or authority, check `tournament-policy` → if it is timing, check `fast-effect-timing`. Always cite; when the documents contain no matching passage, say so instead of inferring.

### B3. Wiki (Yugipedia) — everything outside the official databases

`ygo_wiki` resolves by **name, passcode or Yu-Gi-Oh! Card Database ID** (e.g. `22132`).

1. `topic: "card"` + `input` → names in 12 languages, passcode, database ID, attribute/level/ATK/DEF, archetype, card text (including Japanese), and **which tabs exist**.
2. `topic: "tab"` + `input` + `tab` → `gallery` (image list), `rulings` (official OCG/TCG rulings), `errata`, `artworks`, `tips`, `trivia`, `appearances`, `names`, `lores`.
3. `topic: "page"` + `input` → sets, products (Structure Deck/booster), archetypes, any wiki page; add `section` to read one section in full ("Playing style", "Features", …).
4. `topic: "search"` + `query` → find a page.

Use the wiki for: errata/lore history, OCG rulings not in the rulebook, tips/trivia, set-specific art, a card's set list, or archetype background. Always include the source URL (CC BY-SA 3.0).

### B4. Run the scenario and let the engine conclude (`ygo_judge_scenario`)

This is the standard workflow when a conclusion must be **evidence-based**, not argued:

1. `ygo_judge_scenario` with `preset`:
   - `negate-protected` — Card A → Card B → Card C (result: the summon resolves).
   - `negate-unprotected` — no protection (result: no Summon).
   - `hopt-after-negate` — the hard once-per-turn is consumed even though the effect is negated.
   - `draw-blocked` — the draw is stopped.
2. For a custom scenario: pass `scenario` as JSON `{ handA, handB, deckA, extraA, decisions, expect }`.
   - `decisions`: `{ on: "idle"|"chain"|"card"|"effectyn", player: 0|1, action, card, cards }`
   - `expect`: `chainLink` / `chainSolved` / `negated` / `summoned` / `notSummoned` / `toGrave` / `banished` / `activated` / `size` / `lp`
3. Read the result: `verdict` = `CONFIRMED` (engine agrees), `REFUTED` (engine disagrees — the conclusion was wrong), `INCONCLUSIVE`; plus the real `chain`, `transcript`, `expectations[].evidence` (each one an engine message) and `citations` (rulebook/PSCT).

Rule: **the engine is the final arbiter**. If the verdict is REFUTED, correct the conclusion to match the engine; never defend the original opinion.

**Verifying a claim:** `ygo_verify_ruling` with a sentence ("Card A negates Card B") picks a matching scenario or runs the one you pass, and returns `SUPPORTED` / `CONTRADICTED` / `INCONCLUSIVE` with the observation that decided it. Use it before asserting a ruling you cannot point at engine evidence for.

**Regression:** `ygo_golden_suite` replays `data/golden/scenarios.json` and reports which case changed. Run it after a ProjectIgnis script update or an engine bump.

### B5. Deep script analysis (`ygo_script_insights`)

Use this when the question is about *how a script works*, not just the ruling:

- `mode: "card"` with `passcode`, `cardName`, `luaCode` or `luaPath` → per-effect breakdown: kind (ignition / trigger / quick / continuous / flip / summon / static / activate), trigger event, condition/cost/target/operation pipeline, cost kinds, whether it really targets, reset duration, hard/soft/duel once-per-turn, spell speed, and structural risks with severity.
- `mode: "corpus"` (+ optional `dir`) → aggregate a folder of `c<id>.lua`: effect-kind distribution, most common trigger events and categories, count-limit mix, recurring risks, top APIs and the worst offenders.
- `ygo_analyze_lua` with `deep: true` returns the same insight layer next to the raw AST.

### B5b. Cards without a script (`ygo_ensure_script`)

Mandatory workflow for a card with **no official script**. Two entry points:

**A. The card is not in any database yet (brand-new reveal).** `topic: "from-news"` + `url`:
- reads the article, extracts the **card name, artwork URLs, effect text and stats** (ATK/DEF/Level/Attribute/Type);
- assigns the next free temporary ID (990000000+);
- generates a script from that text and **verifies it in ocgcore using a card-data override**, so verification works even though the card is not in `cards.cdb`;
- returns the artwork candidates so they can be used for the card image.

**B. The card exists in `cards.cdb` but has no script.** `topic: "resolve"` + `passcode`:
- searches `manual/` → `custom_cards/` → official cache → downloads from ProjectIgnis;
- if still missing, generates a script from the `cards.cdb` text.

In both cases:

1. Read `provenance`: `manual` / `custom` / `official` / `generated`. If `generated`:
   - **never use it for tournament rulings**; use it only to test structure/mechanics.
   - trust `confidence` (high/medium/low) and `patterns` to know what it understood, and `verified` to know whether the engine accepted it.
2. When Konami/ProjectIgnis publishes the official script (and the temporary ID has been migrated to the real passcode):
   - `resolve` the same passcode again → the generated file (including a migrated copy in `custom_cards/`) is deleted and the official script written, returning `replacedGenerated: true`.
   - or sweep everything: `topic: "upgrade"`.
3. `topic: "inventory"` / `"list"` to see how many temporary scripts are in use.

Rule: generated scripts are **always labelled**, **always lose to an official script**, and **never override a hand-written custom script**; the sources are never mixed.

### C. Build & optimise a deck

0. **Measure before optimising**: `ygo_consistency_lab` with the deck (ydke/ydk/text) returns `anyActionRate` (a very low bar: at least one legal action) and `engineBoardRate` (reached the Extra Deck or kept a monster on the field), plus average board size and the most common openers. Quote both, and treat them as a goldfish lower bound, not a win-rate.
1. `ygo_build_meta_deck` with `archetype`, `format` (TCG/OCG/AE/Genesys/Master Duel), `targetCount` 40–60. If the archetype has no template the tool returns `available: false` plus `availableArchetypes` — it never substitutes another deck.
2. The format banlist is checked before anything is suggested, and the finished list is re-validated with `ygo_check_legality` before it is returned — never recommend a forbidden card, a banned copy count, or an Extra Deck monster in the Main Deck.
3. `ygo_check_legality` answers the basic question directly: sizes, banlist copy limits and zone placement for one format.
4. `ygo_optimize_deck` on an existing deck to grade the staple/hand-trap ratio and propose replacements. It accepts a file path, .ydk text, ydke:// link or object and refuses an empty parse.
5. `ygo_check_locks` before finalising: it reads every script and reports summon/activation/material locks plus contradictions (e.g. a Special Summon lock next to an Extra Deck lock). Real scripts using anonymous functions, `IsSynchroMonster()` and `aux.addContinuousLizardCheck` are understood.
6. `ygo_matchup_planner` turns the live tier list into an expected field (weighted by tops) plus a role-based side skeleton.
7. `ygo_deck_cost` prices the list across TCGPlayer / Yuyu-tei / TCGCorner and shows the cheapest market combination.

### D. Token-efficient custom cards

1. `ygo_create_custom_card` registers the card and returns a temporary ID plus its Lua script.
2. `ygo_generate_batch_art_prompt` merges every card into one grid prompt.
3. The user returns the grid image → `ygo_slice_batch_art` slices each cell and embeds it as Base64 into the finished SVG.
4. When Konami announces the passcode: `ygo_migrate_temp_card` updates the registry, the Lua file and every related `.ydk`.

### E. Tournament paperwork

1. `ygo_generate_tournament_decklist_pdf` with a YDK/YDKE/text list plus duelist details (`duelistName`, `cardGameId`, `eventName`, `eventDate`, `format`) — fills the 183 AcroForm fields of the original Konami template.
2. `ygo_render_deck_image` renders a PNG with 10 cards per row, auto-sorted Monsters → Spells → Traps, a banner and a Konami Neuron-style copyright footer; choose `lang: "jp"` or `"en"`. The PNG is attached to the tool result as an image block and the absolute `outputPath` is returned. Show the image to the user, and when the host has a file-preview/open-file capability (OpenCode: `browser.preview`; an editor: open the file) open that absolute path in a tab so the decklist stays visible. The PDF returned by `ygo_generate_tournament_decklist_pdf` follows the same rule.

### F. Meta tracking & freshness

1. `ygo_get_monthly_meta` with `month`, `year`, `format` — tier list, share %, the month's staples.
2. `ygo_compare_monthly_meta` diffs two months into Rising Stars and falling decks.
3. `ygo_get_daily_meta` for day-by-day movement and emergency banlist alerts.
4. Every online result carries `FreshnessEvidence` (timestamp, 0–100 freshness score, badge, SHA-256) — quote that evidence with the answer.

Format coverage: **TCG/OCG** come from YugiohMeta; **Master Duel** from Master Duel Meta's API (share of the latest topping decks); **Genesys** from the YGO Omega ladder table. **AE has no public live tier list** — the tool says so and suggests the OCG list only as a clearly labelled proxy.

### F2. Market questions ("most expensive", "what is rising", "why")

`ygo_market_query` ranks the whole priced pool. Use it for any price *question*, not for a single card's shop quotes.

| Question | Call |
|---|---|
| Which card is the most expensive? | `intent: "top_price"` (default `priceBasis: "market"`) |
| Most expensive *collector* printing? | `intent: "top_price", priceBasis: "top_printing"` |
| What is rising? | `intent: "movers", windowDays: 30` |
| What is hot / worth buying under $5? | `intent: "search", maxPrice: 5, minPrice: 1` |
| Why is this card priced like this? | `intent: "explain", card: "<name>"` |
| Which printing / rarity is cheaper? | `ygo_card_printing_prices` with `cardName` |

Rules that keep the answer honest:
1. **`movers` needs two daily snapshots.** The server records one snapshot per UTC day in `data/market/history/`. On day one it returns `available: false` plus `demandFallback` (weekly search interest) and `recentReleases`. Never describe `demandFallback` as "price is rising" — it is demand, not a measured delta.
2. **`priceBasis` decides the number.** `market` = YGOPRODeck aggregate TCGPlayer price (cheapest commonly listed copy); `top_printing` = most expensive printing; `floor` = cheapest priced printing. Say which one you quoted.
3. **A `notes` entry starting `Top printing … is Nx` is an asking price, not a traded market.** Quote the market figure and flag the outlier; never present a $115,000 listing as the card's value.
4. **`confidence`** is `high` (market + ≥2 priced printings), `medium` (market only) or `low` (printings only). Report it.
5. **Correlation is not proof.** `drivers` in `explain` are labelled `news` / `banlist` / `release` / `demand` / `meta` / `data`, each with a `confidence` and usually a `sourceUrl`. A `news` driver means the article matched the card name or archetype — say "matches", not "caused", unless it is a banlist or a reveal of that exact card.
6. Use `ygo_check_prices` only for one card's shop-by-shop quotes (TCGPlayer/Yuyu-tei/TCGCorner). It has no ranking and no pool.
7. **Never infer a price from rarity.** "Common is cheaper than Secret Rare" is false often enough to matter (promo/event/regional printings). For any "which printing is cheaper / how much is the Secret / KR version" question, call `ygo_card_printing_prices`: it returns one row per printing (set code, set name, rarity, language) and `price: null` when no source lists it. A null is "no data", never "cheap".
8. **Language coverage is explicit.** Priced: EN (TCGplayer per-product via TCGCSV), JP (Yuyu-tei), AE (TCGCorner). Unpriced: KR, DE/FR/IT/SP/PT, SC/TC — the tool says so and gives no number. Do not substitute a US price for a KR card and call it the KR price; say the feed does not exist.
9. **Ranking is US-only; secondary markets are per-card enrichment.** `includeMarkets` attaches live Yuyu-tei (JPY) and TCGCorner (HKD) quotes for the top 3 results (`explain` does it by default). Yuyu-tei is searched with the Japanese card name resolved from Yugipedia; if no listing matches, `status` is `unavailable` and there is **no price** — never fill that gap, and never treat a search-link fallback as a quote. FX is fixed reference rates (JPY 150, HKD 7.8 per USD), excluding shipping and duty. A `TCGCorner` quote in **EUR** is the Cardmarket benchmark fallback, not a shop listing — label it as such.
10. **"Most expensive" and "worth buying" are different questions.** Collector-only cards (high price, near-zero searches) dominate a raw price sort. Pass `minWeeklyViews` (e.g. 1000) to apply a liquidity floor and say you did; never present a 63-views/week card as a good buy.
11. **Read `confidenceRationale`, not just `confidence`.** `medium` usually means *the printings are listed but every `set_price` is 0* — that is not the same as "only one printing exists". `printingsListed` counts every set entry; `printingsPriced` counts the ones with a price; `listedPrintings` names rarity and set code (`hasPrice: false`). Use it to answer "which rarity is the cheapest entry" **without inventing a price for that rarity**.
12. **`sortBy: "liquidity_adjusted"` is the ranking for "expensive but actually sellable".** Score = `sqrt(logPriceNorm × logDemandNorm)`, 0–1, where price is `log10(1+price)/log10(1+10000)` and demand is `log10(1+weeklyViews)/log10(1+50000)`. It is a ranking heuristic, **not money and not expected sale value**. Do not substitute `price × log(views)` by hand (a $1,800 / 63-view card scores 13x a $58 / 17,481-view card), and do not substitute percentiles (rank compression still lets a $370 / 147-view card beat a $69 / 11,888-view one).

### F3. Community decks and published combos

Use `ygo_find_community_decks` when the user wants to see what other players actually built:

| Ask | Call |
|---|---|
| "Show me decks for an archetype" | `archetype: "<archetype>"` |
| An archetype category page | `category: "type/<archetype-slug>"` or the full `/category/type/<slug>` URL |
| "Tournament lists only" | `format: "tcg"`, `source: "ygoprodeck"` |
| "Top 8 from a tournament" | `tournament: "<event name>"` |
| "Decks under $100, 40 cards, using a specific card" | `maxPrice: 100`, `deckSize: 40`, `containsCard: "<card name>"` |
| "Master Duel builds" | `source: "masterduelmeta"` |
| "Official Konami recipe" | `source: "konami"`, `query: "<archetype>"` |
| "GOAT / Edison deck" | `source: "formatlibrary"`, `format: "goat"` |
| "What beats this deck" | `ygo_find_counters` with `archetype: "<deck type>"` |
| "Newest builds" | `sort: "recent"` |

Rules:
1. **Every deck carries `url` and `ydke`.** Quote the page URL. Feed the `ydke` into `ygo_check_legality`, `ygo_deck_cost`, `ygo_consistency_lab` or `ygo_optimize_deck` — never retype a community list by hand.
2. **A community list is not legal proof.** It is a player submission; run `ygo_check_legality` before recommending it, and report the errors it returns.
3. **Sources are labelled.** `ygoprodeck` = TCG/OCG community + curated tournament decks (`format: "tcg"` maps to their Tournament Meta category). `masterduelmeta` = Master Duel decks. `konami` = official card-database (Neuron) deck recipes: POST search with a session token, one extra request per deck, so keep `limit` ≤ 5 and always pass a query. `formatlibrary` = retro/community formats (GOAT, Edison, Fiber) with a direct `ydk` per deck. `source: "all"` = YGOPRODeck + Master Duel Meta only.
4. **Konami recipes are official but not legal proof.** They map card names to passcodes; `unresolvedCards` counts names that did not resolve, and a non-zero value means the ydke is incomplete — say so instead of patching it by hand.
5. **Only one public YGOPRODeck taxonomy exists: `/category/type/<slug>`.** `category` accepts that URL, `type/<slug>`, or a bare archetype; other `/category/...` paths return 404. It maps to the same `_sft_post_tag` filter.
6. **YGOPRODeck-only filters**: `tournament`, `deckSize`, `minPrice`/`maxPrice`, `from`/`to`, `containsCard`/`excludeCard`. The resolved values are echoed in `appliedFilters`, and the exact upstream URL in `sourceUrls`. They do not apply to Master Duel Meta results, so `source` defaults to `ygoprodeck` when one is used.
7. **Alternate passcodes are real.** YGOPRODeck maps more than one id to the same card (for example 94145021 *and* 94145022). Never call a returned deck wrong because one numeric id is missing — resolve the names.
8. `ygo_find_combos` returns **published** combos (starting cards + ordered steps) from Master Duel Meta's public combo API, by archetype or by card. The corpus is the 300 newest entries — an empty result is not proof that no combo exists; say so.
9. Combos attached to a deck may be `description` text, a `youtube` video, a `guide` link or `replay` availability. Do not present a video link as a written step-by-step line.
10. `ygo_find_counters` returns published counters (counter cards with an `impact` **label**, chokepoints, and the author's explanation) for an archetype or a counter card. `impact` is the author's opinion, not a measured win rate; verify the card's real behaviour with `ygo_judge_card`.
11. For a combo derived from a list you already hold, use `ygo_find_synergy_and_combos` (local engine), not this tool.

### G. Playing and training the AI

- `ygo_run_duel` with `ai: "greedy"` — both sides play the heuristic policy instead of the passive default responder.
- `ygo_ai_benchmark` — N seeded games, alternating the starting side, returns win rate vs baseline, average steps and LP. Treat it as a sanity check, not a strength claim.
- `ygo_export_selfplay` — policy-vs-policy games exported as JSONL (request type, legal option codes, chosen action, result) for behavioural cloning.

## 4. Operational notes

- This project is **beta (0.9.x)** and under active development: tools can change between versions. If behaviour looks wrong, run `ygo doctor`, check `ygo --version`, and consult the changelog before assuming a tool is broken.
- Run tools from the shell when MCP is unavailable: `ygo call ygo_get_card --name "<card name>"`. Flags map directly to parameters; values are parsed as JSON when possible.
- Offline mode: `ygo call <tool> --offline` (or `YGO_OFFLINE=1`) refuses every outbound request before it is made; tools then report `available: false` with the real reason instead of hanging.
- Cache control: `ygo cache` lists sizes/ages, `ygo cache --clear market --yes` frees an area. Clearing is a dry run without `--yes`.
- Environment: `ygo doctor --sources` pings each upstream API, `ygo doctor --fix` downloads missing data.
- For large results, read the key fields (`deck`, `adjudication`, `prices`) instead of quoting the whole JSON.
- Use absolute paths for user-supplied files; tool output usually goes to `data/` inside the project (or `~/.yugioh-assistant-mcp` for published npm installs).
- Reinstall the server into another client: `ygo install`; check the environment: `ygo doctor`.
