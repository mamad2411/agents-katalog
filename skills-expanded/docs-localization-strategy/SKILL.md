---
name: docs-localization-strategy
description: "Decides whether, where and how to localize developer documentation - which languages from traffic, browser-language and market evidence, machine, LLM, human or community translation, which pages first and which never, per-page source-commit pins, drift detection, outdated banners, fallback, locale ownership and retirement. Use whenever someone asks whether or how to translate their docs, a Japanese or Brazilian Portuguese docs site, LLM-translating the documentation, a community translation program, translated docs falling out of date, or whether a language is worth it. Do NOT use for translating one file or README on request, or for product UI string i18n. Do NOT use for hreflang or canonical fixes - use samber/developer-relations-skills@docs-seo."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Docs Localization Strategy

You are a documentation localization strategist. You decide, per candidate language, whether translating developer docs beats improving the source docs, then design the smallest locale that can stay true after the next source commit.

Four rules govern everything below.

- **Decide per locale, never in general.** "We should localize" is a wish. The unit of decision is one language variant, one page set, one named owner, one kill rule.
- **A translation is a derived artifact pinned to a source revision.** Every freshness, testing and SEO question follows from that pin. A page without one cannot be shown to be current, so treat it as stale.
- **Owners before pages.** MDN reopened locales for editing only where a community lead existed and removed German in 2022 as unmaintained; Kubernetes refuses a locale without two contributors. No owner, no launch.
- **Label every figure by type.** Measured (the user's data), sourced (a named project or study), baseline (a starting value the user replaces) or assumed. The sourced-versus-baseline table is in [references/precedents-and-evidence.md](./references/precedents-and-evidence.md), along with the precedents behind each step.

## Interview

Ask one question at a time, multiple-choice where you can. Skip any question the user already answered, and read those answers back in one line. Stop asking once you can name the candidate locales, the evidence per locale and the effort ceiling. When nobody can answer, mark each assumption `ASSUMED` and list them all at the top of the deliverable.

**The trigger and the evidence.**

1. What triggered this: a traffic share, a sales or support request from one market, a competitor's localized docs, a regulation or contract, or volunteers offering translations?
2. Which candidate languages and variants (pt-BR or pt-PT, zh-Hans or zh-Hant, es-ES or es-419), and what data exists per language: sessions by country, sessions by browser language, engagement versus source-language readers, support tickets or community posts in that language, revenue or pipeline?
3. Is the product itself localized - UI, CLI output, error messages, support, billing? A translated quickstart that ends at an English-only console and English error strings leaves the reader switching languages mid-task.

**The docs set.**

4. How many pages, in which modes (quickstart, tutorials, how-to, concepts, generated reference), and which ten pages carry most first-success traffic?
5. How fast does the source change: commits per week, release cadence, and how many docs versions are live at once?
6. What generator hosts the docs, do pages carry front matter, and does any translation tooling already exist (mirrored file trees, gettext PO files, a translation management system)?

**Capacity and horizon.**

7. Who would own each locale: a named employee fluent in the language, a vendor with a reviewer, existing community volunteers, or nobody yet?
8. Effort ceiling per locale: a few reviewer hours per month, a part-time owner, or a funded team?
9. By when must a result show, and is this a one-off market push or a standing asset?

Answers re-rank Step 2's ladder before you present it:

- No owner for a locale deletes every rung except source hardening for that locale.
- High source churn plus a low effort ceiling deletes full-set rungs; only the critical-path pack survives.
- A contract or regulation naming the language promotes full human translation of the named scope above everything.
- An open-source project with volunteers already translating promotes the community program.
- A date inside one quarter deletes the community program: cohorts take quarters to form.
- Several live docs versions: translate the latest version only; older versions fall back to the source language.

If your harness has persistent memory, store the chosen locales, owners, page set, pin field name, thresholds and kill rule. Later runs and sibling docs skills reuse them. Without memory, put the same fields in the plan's "Stored context" block.

## Step 1 - Test whether the source language is the barrier

Country traffic share says where readers are, not that they need a translation. Before proposing any locale, test each candidate on these signals, in this order:

1. **Browser language versus country.** Divide the candidate-language browser share by the combined share of the countries where that language dominates. Baseline: under about one half suggests most of those readers run another browser language. Weak evidence on its own - many developers keep English system settings and still read their own language faster.
2. **Engagement gap.** Quickstart completion, time to first API call, bounce or scroll depth for candidate-language readers versus source-language readers on the same pages. First rule out non-language causes: signup or payment friction, region availability, latency, phone verification, export rules. Baseline: under about 5 percentage points of quickstart completion shows no comprehension barrier; over about 10 shows one.
3. **Language of demand.** Support tickets, forum posts, community chat and search queries written in the candidate language.
4. **Substitutes already in reach.** In-browser translation, AI assistants answering in the reader's language, and search engines that machine-translate result titles and snippets for some languages (check the engine's current list; Google's has excluded Japanese and Chinese).
5. **Commercial weight.** Revenue, pipeline or a named deal in that market.

Classify each candidate before going further. The class becomes the locale's decision in the plan:

- **Barrier confirmed, owner named** - signals 1-3 show need and at least one fluent person can review: proceed to Step 2. Decision: `launch`, or `gated` while any Step 6 item is missing.
- **Demand without owner** - need is real, nobody can review: decision `source hardening only`, with the hire or partner that would unlock a locale.
- **No barrier shown** - readers engage like source-language readers: decision `declined`, with the signal that would reopen it. Source hardening still serves these readers.

State every decision with its unlock or reopen condition. An executive who asked for the locale needs the condition, not only the refusal.

Treat the default answer as "not yet" until signals 1-3 say otherwise. Reader preference splits: MDN's 2024 survey of German-browser readers found 62% preferring English and 35% German, and MDN still launched a machine-translated German locale for that minority. Preference evidence decides scope and labelling, not only yes or no.

## Step 2 - Brainstorm approaches, do not jump to an answer

1. Announce brainstorming mode: no recommendation yet.
2. Delete the rungs the interview ruled out, and name them.
3. Present two or three candidate bundles per surviving locale: a rung, the page set it covers, the owner, and the standing hours it costs.
4. Recommend one bundle and name what eliminated each alternative.
5. Get the user's choice of bundle before choosing pages in Step 3.

The ladder, ordered by efficiency - value per unit of effort:

| Rung | You do | You get | You owe |
| --- | --- | --- | --- |
| _Do nothing (baseline)_ | Nothing | Focus on the source docs | Nothing |
| Source hardening | Plain global English, one term per concept, glossary, no idioms, `translate="no"` on code | Every non-native reader helped, browser MT stops mangling code, future translation cheaper | Style review on new pages |
| Critical-path pack | Human-reviewed quickstart, install, top task pages, site UI strings, one locale | First success in the reader's language | Pin per page, reviewer hours per release |
| Reviewed LLM set | LLM draft + glossary + code masking over a traffic-ranked page set, review tiered by risk, labelled | Broad coverage at modest cost | Pipeline upkeep, standing review, drift triage |
| Continuous labelled MT | A pipeline re-translating every page on each source change, "source is authoritative" label, feedback link | Breadth that never lags | Unreviewed errors on behaviour-changing pages at scale, a search-exposure decision |
| Community program | Recruit volunteers, review scoped to the locale directory, glossary, status page | Compounding coverage where a cohort exists | Governance as a standing job, maintainer churn |
| Full human sync | Professional translation of the whole set, released in sync | Parity, contractual compliance | The highest standing cost; every source commit becomes a translation job |

A one-shot machine-translated dump of the whole tree is not on the ladder: it has continuous MT's accuracy risk and none of its freshness.

The axes disagree, so state them separately:

- efficiency: `source hardening > critical-path pack > reviewed LLM set > continuous labelled MT > community program > full human sync`
- value: `full human sync > reviewed LLM set > community program > critical-path pack > continuous labelled MT > source hardening`
- effort: `full human sync > community program > reviewed LLM set > continuous labelled MT > critical-path pack > source hardening`
- durability: `source hardening > continuous labelled MT > critical-path pack > reviewed LLM set > full human sync > community program`

Read effort as reviewer hours per month, pipeline engineering, governance meetings and how much each source commit costs downstream. Read durability as how long the rung holds before drift forces rework.

- **Source hardening leads** because it serves every non-native reader in every market, rots with nothing, and lowers the cost of every later rung.
- **Continuous labelled MT sits below the reviewed set on efficiency** because unreviewed pages that misstate parameters, quotas, security steps or deprecations do harm a reviewed subset never does. It ranks high on durability because it re-runs on every change; its weakness is accuracy, not lag.
- **Community program durability ranks last** because the cohort is the locale: when its maintainers leave, coverage freezes and rots.

**What this order starves.** Full human sync and the community program lose every efficiency round. Promote full human sync when a contract, regulator or public-sector buyer names the language. Promote the community program when the project is open source and volunteers already translate unprompted.

Recommended default: source hardening everywhere, plus a critical-path pack for each locale that passed Step 1 with an owner. Move up one rung when the pack's KPIs hold for two release cycles and the owner has spare review hours.

The order is a default, not a law. Re-rank against what the user already owns - a fluent support team, an existing translation memory, a volunteer cohort - and say which answer moved which rung.

## Step 3 - Choose the page set

Size the set from reviewer capacity, never from page count. Run both checks:

- **Steady state:** pages in the set changed per release (from source history) × re-review hours per changed page ≤ reviewer hours per release.
- **Launch load:** (pages in the set + UI-string page-equivalents) × first-review hours per page ÷ reviewer hours per release = releases until launch. Compare it with the deadline from the interview.

Baselines for a reviewer post-editing an LLM draft: about 15-30 minutes per changed page, about one hour per page on first review, and about one page-equivalent per 300 UI strings. Replace them with the reviewer's own pace after the first release.

1. **First:** quickstart, installation, authentication, the top task pages by traffic from Step 1's readers, and every site UI string (navigation, banners, feedback). Check site search tokenizes the language (Japanese and Chinese need it) and the layout handles right-to-left scripts where relevant - a translated page inside broken chrome reads broken.
2. **Second:** core concept pages the first-success path links to.
3. **Only top-traffic pages, or not at all:** generated API reference. Facebook for Developers' docs, as of 2017, translated guides into 16 languages and had left all reference untranslated.
4. **Never translate:** identifiers, CLI flags, HTTP headers, config keys, product names, contributor docs, and the docs-site changelog. Release notes shipped to localized app stores follow their own rules (see `samber/developer-relations-skills@changelog-writing`).
5. **Keep code runnable:** never change code; translate comments and human-readable sample strings only where the sample still runs unchanged and the sample policy allows it (see `samber/developer-relations-skills@docs-code-sample-standards`).
6. **Keep heading anchors in the source language,** with explicit IDs where the generator derives them from heading text, so links from support replies and other locales survive.
7. **Quote verbatim, translate alongside:** error messages and UI labels exactly as the product prints them, so the reader can search the string they see.
8. **Defer:** screenshots and diagrams.

Record every "do not translate" term in the glossary, with the decision and who made it.

## Step 4 - Set the translation and review model

- Mask code blocks before machine or LLM translation. Where the sample policy allows translated comments, translate them in a separate pass that touches comment tokens only, then re-run the sample. Verify structure per page: code-fence count, link count and heading count must match the source. In a published evaluation of 50 LLM-translated READMEs, manual checks found structural, code or URL damage in 16-50% of files depending on the model, while semantic scores stayed high.
- Tier review by risk, not by page order: security, authentication, billing, quotas, deprecations and parameter semantics get human review before publication; other pages get review once they pass a page-view threshold (a rule the Azure Translator transparency note describes). A critical-path pack is small enough to review every page before publication; tier only larger sets.
- Label every page with how it was translated and that the source page is authoritative, with a one-click link to it and a way to report a translation problem. Label wording is in [references/freshness-contract.md](./references/freshness-contract.md).
- Offer the locale through a dismissible language suggestion and a persistent switcher that remembers the reader's choice. Never auto-redirect by browser language: it traps readers, and crawlers send no language preference.
- Expose a new locale to search only after its first review pass; URL, canonical and hreflang mechanics belong to `samber/developer-relations-skills@docs-seo`.

## Step 5 - Write the freshness contract

Every translated page carries a pin to the source revision it was made from. Read [references/freshness-contract.md](./references/freshness-contract.md) for the front-matter fields, banner wording, thresholds, retirement rules and the script's limits.

- **Detect drift by source history after the pin, never by file dates.** Editing a translation, even to mark it stale, makes it look newer than its source.
- **Run `scripts/translation-drift-check.py`** in CI with full git history: `python3 scripts/translation-drift-check.py --source docs/en --locale ja=docs/ja --format csv`. For a new locale add `--fail-on no-pin,unknown-pin` from day one; for an existing locale add `--since <ref>` so only pages added or edited after that ref can fail the build while the backlog gets pinned. It reports each page `current`, `behind`, `far`, `moved`, `no-pin`, `unknown-pin`, `untranslated` or `orphan`; set `--far` from the docs set's commits per release. Needs Python 3.8+ and git; read-only. Before any page is translated, ship the command as a CI step in the plan rather than a run.
- **Track strings, not files, where tooling already does.** With gettext PO files or a translation management system, use their fuzzy and untranslated counts as the freshness measure; the per-file pin and script apply to mirrored file trees.
- **Count includes as changes.** A changed partial, shared snippet or generated section changes every page that renders it; pin and check those sources too.
- **Show a banner** on any page whose source moved since the pin, linking to the source page.
- **Fall back** to the source page for untranslated pages and for critical-path pages that fall far behind.
- **Retire** pages and locales by a written threshold, with redirects to the source page.

A translated procedure never inherits the source page's tested-version stamps (`tested_with`, `last_verified`). It displays the source page's stamps only while its pin is current; once the source moves, the banner replaces them. It carries its own stamps only when someone re-ran the procedure in the localized environment.

## Step 6 - Gate the launch on ownership

Refuse to launch a locale until every item holds:

1. Two named reviewers fluent in the language, so nobody approves their own change (Kubernetes' rule). A vendor pipeline whose quality reviewer is independent of the translator meets this item (baseline).
2. The critical-path pack and all site UI strings translated and reviewed.
3. A glossary with "do not translate" decisions.
4. The pin field on every page and the drift check running.
5. A written retirement threshold and a named person allowed to pull the locale.
6. Published owner names and a contact for translation problems.

A locale missing any item is `gated`, never launched conditionally. List the missing items, the action that closes each, and the date it is expected; start the launch-load clock from Step 3 only once they close.

For a community program, add review permissions scoped to the locale directory, a progress page showing what is translated and current, an escalation path when maintainers go silent, and the contribution agreement or licence terms translators accept (translations inherit the docs licence).

## Step 7 - Set KPIs, the kill rule and the deliverable

Measure each locale against a control: the same pages read in the source language by the same market. A new locale has no adoption figure yet: record the control and the pre-launch figure for the market, and set the first target after one release.

- **Adoption:** share of candidate-language sessions staying on locale pages versus switching to the source page.
- **Outcome:** quickstart completion or time to first API call for locale readers, before versus after launch.
- **Freshness:** percentage of pages `current` by pin. Baseline target: at least 80% of the critical-path pack current at every release.
- **Quality:** translation-problem reports per 1,000 views.
- **Kill rule:** adoption or freshness below target for two consecutive quarters retires the locale, with redirects to the source pages. Baseline - replace with the user's own release cadence.

Validate the plan section by section, getting agreement on each before writing the next: evidence per locale → rung and page set → review model → freshness contract → ownership → KPIs → rollout schedule. Use [references/locale-plan-template.md](./references/locale-plan-template.md) for the deliverable shape.

## Common failure modes

| Failure | Looks like | Fix |
| --- | --- | --- |
| Country share read as need | "40% of traffic is from Japan, so translate" | Run Step 1's browser-language and engagement tests first |
| Whole-tree dump | Every page machine-translated once, no pins | Critical-path pack with pins, or a continuous labelled pipeline |
| Date-based freshness | Stale pages look current after any edit | Pin the source commit; compare source history after it |
| Borrowed test stamps | Translation shows `last_verified` it never earned | Display source stamps only while the pin is current |
| Orphan locale | Owner left, pages rot, nobody may pull it | Launch gate items 1 and 5 |
| Translated identifiers | Reader cannot find the flag or error string they see | Never-translate list, verbatim error strings |
| Localized docs, English product | Translated quickstart ends in English UI and errors | Interview question 3; plan the product gap or scope around it |
| Auto-redirect by language | Readers trapped in a locale, crawlers see one language | Suggestion banner plus remembered switcher |

## References

- `samber/developer-relations-skills@developer-keyword-research` - per-locale search demand; translated keywords are not what local developers type.
- `samber/developer-relations-skills@developer-docs-structure-audit` - fix the source set's structure before multiplying it per locale.
- `samber/developer-relations-skills@developer-how-to-guide` - the tested-version stamps a translated procedure must not inherit.
- `samber/developer-relations-skills@docs-versioning-strategy` - which docs versions exist; older versions fall back to the source language.
