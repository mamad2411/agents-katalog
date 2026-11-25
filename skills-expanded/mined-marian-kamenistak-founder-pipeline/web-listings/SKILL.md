---
name: web-listings
description: "Use when deciding where to register a product, service or company, or to submit and track those listings: directories, registries, startup platforms (Product Hunt, BetaList), review sites, vertical and home-market catalogs; \"where should I list this\", \"get us on Product Hunt\", \"directory listings\", \"listings audit\". NOT for per-URL search-engine submission (`/founder-pipeline:web-indexation`) or earned editorial links and outreach (`/founder-pipeline:web-backlinks`)."
---

# Listings — register-once profile & directory presence

Turns the scattered "where should we be listed" question into one dated catalog (`config/targets.json`), a submission method (`references/method.md`), and a per-property ledger that tracks what's live so nothing gets re-submitted or forgotten. Deliberately separate from `/founder-pipeline:web-backlinks`: that skill owns *earned* placements that need a pitch, this one owns *register-once* identity listings. They were split because the two need different suppression rules, different laws, and different execution models — but the founder pipeline's P5.S2 requires BOTH to run, so treat them as a pair, not as alternatives.

## Commands

| Command | What happens |
|---|---|
| `/founder-pipeline:web-listings audit <domain>` | Phase 1: check current presence against priority-1 targets and the ledger |
| `/founder-pipeline:web-listings <domain>` | Phases 1-3: audit → select eligible targets → prepare submission packs |
| `/founder-pipeline:web-listings run <domain> [N]` | Phase 4: execute next N eligible targets, record outcomes |
| `/founder-pipeline:web-listings status` | One table across every property in the registry: listed/queued/blocked counts, staleness flags |
| `/founder-pipeline:web-listings nap-audit <entity>` | Diff every local-tier listing's NAP against `references/entity-pack.md`. Reports `exact` / `drift` / `missing`, plus rows with no `listing_url` recorded as **unmeasured, not clean**. `--list` shows which entity blocks carry NAP and which fields the canonical source does not define. CHK rows are candidates needing confirmation, never verdicts. |

## Property registry (configure once)

Domains map to properties through `config/properties.json`, which ships with example rows only —
fill it with your own before the first run. `/founder-pipeline:web-backlinks` reads the same file.
Each property declares a `brand_class`, which is what `config/targets.json` rows filter on.

**Active registration scope.** Decide once which properties are in the active push and which stay
in the catalog for later, and record that in `properties.json` (`active: true|false`). Registering
a property as a *product* on a launch-discovery platform is a deliberate choice, not a
brand_class-derived one — a community, a conference or a coaching practice can all be listed as
products on the general launch platforms if you want the discovery surface. The canonical login
email per property lives in `references/entity-pack.md`'s scope table.

## Ownership boundary

| Surface | Owner |
|---|---|
| Mode A — per-URL submission to search indexes (IndexNow, GSC, and any domestic search engine's webmaster tools) | `/founder-pipeline:web-indexation` |
| **Mode B — register-once identity/profile listings: catalog, submission, ledger** | **this skill** |
| Earned editorial links, outreach campaigns, guest posts, PR, your own link-magnet directory | `/founder-pipeline:web-backlinks` |
| Launch-day campaign (timing, hunter, comments) on a launch-discovery platform | Not this skill. This skill only stages the profile; run the launch itself as its own campaign |
| Post-launch orchestration and routing | Not this skill |
| Building/changing the site itself | `/founder-pipeline:web-site-creator` |

## The Laws (inherited from `/founder-pipeline:web-backlinks`, do not restate loosely)

1. **Never require, promise, or trade a followed link** (`web-backlinks` Law 4). Directory verification = identity confirmation only. Any swap link carries `rel="nofollow"`. A target whose terms demand a followed link is marked `rejected`, not submitted, and never re-proposed.
2. **Portfolio rule.** On any registry hosting multiple orgs/products, list every owned property that fits, each as its own entity pointing at its own domain — not just whichever one prompted the run.
3. **Entity accounting.** Wikidata / company-database / Google-Business-Profile / Knowledge-Panel profiles are citation surfaces, not backlinks — never report them as referring domains.
4. **Localize before you register.** No submission to a directory serving a language you don't publish in, until the pages that resolve there exist in that language, properly translated, correct `hreflang`, returning 200. Mark `blocked` with the reason if not met.
5. **The agent submits; the agent never authenticates.** The agent fills and submits genuine anonymous forms — a public form with no account or login behind it — after asking in chat and getting a clear yes for that specific submission. **Anything credential-bearing is OWNER-ONLY, and no in-chat authorization changes that:** the agent may not create an account, may not enter a password (typed or retrieved from a password manager), and may not complete an SSO login on the owner's behalf. This is a platform rule, not a skill preference — `/founder-pipeline:web-backlinks` Phase 4.4b records the full reasoning and the reversal that produced it. What the agent CAN do on an account-gated target: prepare the complete pack (copy at the right length, assets, canonical NAP, links) and stage it so the owner pastes it in during their own signup, and drive post-login non-secret form-fill in a session the owner authenticated themselves. **Hard stop, screenshot the state, queue OWNER-ONLY — do not attempt to push past these:** any account creation, any login or password field, any payment field, any CAPTCHA, any phone/SMS/ID verification step, any target whose terms are ambiguous about a followed link-back (Law 1 still applies unchanged). After a submission succeeds, verify the listing is actually live — spot-checked, never assumed — before marking a row `Done`.
6. **NAP consistency.** Name, address, phone, website identical across every listing (canonical values in `references/entity-pack.md`).

## Why this skill outranks its reputation — the AI-citation evidence

Listings read like hygiene. On the current evidence they are **the highest-leverage AI-visibility work available**, because every large measured citation effect is off-page and on-page formatting has *no published correlation coefficient at all*.

- [ ] **A third-party review profile is the single biggest measured swing in the dataset.** Brands with **no review profile on the major consumer-review platform: 1% median citation rate. Brands with just 1–13 reviews: 53.5%.** A 52-point swing from an off-site signal [Seer, 804,491 AI responses, 4 platforms, 1,926 brands, 15,783 prompts]. **Read the mechanism honestly before acting on it:** 1–13 reviews is far too few to be doing the work itself, so the profile is almost certainly a *proxy* for "this is a real, established, verifiable business" rather than a cause. It's correlational, it's the vendor's own client portfolio rather than a random sample, and the platform studied skews B2C/e-commerce. The actionable read is **"a credible third-party review profile exists at all"**, not "get on that specific platform" — pick the one that fits the brand class (below).
- [ ] **Being named beats being linked.** Citation rate 53.1% when the brand is mentioned in the answer vs 10.6% when not — 5× [Seer, 541,213 responses, 20 brands, 6 platforms]. Profile listings are how a brand becomes nameable to a model that has never seen the site.
- [ ] **Entity listings have a per-engine shape.** ChatGPT leans Wikipedia (47.9% of its top-10 sources), Perplexity leans Reddit (46.7%), AI Overviews lean Reddit + YouTube [Profound, 30M citations]. Caveat that matters: on a **total-volume** basis these are far smaller (Wikipedia = 7.8% of ChatGPT citations); the "share of top-10 sources" framing inflates apparent concentration ~6×. Wikidata/Wikipedia is disproportionately a **ChatGPT** play.
- [ ] **This does not change Law 3.** These are citation surfaces, still never reported as referring domains. What changes is priority: the review and entity categories move up, they don't move ledgers.

**Review-platform fit by brand class** — every class needs a credible review or verification surface; the platform differs:

| Brand class | Review/verification surface that fits |
|---|---|
| personal-brand | Google Business Profile, practitioner/coach directories, the accreditation body's public listing, recommendations syndicated to the site |
| services | Agency-rating platforms, a product-review site if a product ever ships, GBP, chamber verification in your home market |
| community / conference | Event-platform ratings, Google reviews on the event entity |
| marketplace-saas | The consumer-review platform plus the two big B2B software-review sites |
| app | App-store ratings, home-market catalog reviews |

Treat this as a **priority weighting, not a new mandate**: it does not override the localize gate (Law 4), the credential boundary (Law 5), or NAP consistency (Law 6). A review profile the owner can't service with real reviews is worse than none.

## Phase 1 — Audit

For the target property: read its site JSON-LD `sameAs`, check `references/entity-pack.md`'s sameAs table and any existing ledger rows for the property, then verify presence on priority-1 targets in `config/targets.json` (fetch, don't assume). Classify each as **listed** / **claimed-but-stale** (verified_on >90 days or copy doesn't match current NAP) / **absent**.

## Phase 2 — Select

Do not read `config/targets.json` whole: it is about 39,000 tokens. List the rows you need with `python3 "${CLAUDE_SKILL_DIR}/scripts/select_targets.py" --class <brand_class> [--territory <t> ...] [--priority <n>]`, and open one row with `--id <ID>` when you need its notes (`--unassigned` lists rows with `applies_to: []`). The filter is `applies_to` — a list of brand classes — matched against the property's `brand_class` from `config/properties.json`, then apply the localize gate to any row whose `territory` is a language you don't publish in. A row with `applies_to: []` is unassigned: judge fit from its `notes` and record the decision by editing `applies_to`. Brand-class weighting, mirroring `web-backlinks/references/platform-matrix.md`:

| Brand class | Go-deep categories |
|---|---|
| community | entity, event, institution, catalog, **review** |
| conference | event, media, entity, **review** |
| personal-brand | entity (person), vertical, institution (accreditation body), **speaker**, **review** |
| services | b2b-services, institution (chambers), catalog, **review** |
| marketplace-saas | startup-platform, review, vertical |
| app | catalog, institution, **review** |

`review` sits on every class — see the AI-citation evidence above for why, and for the platform that fits each class. It is a priority weighting, not a mandate: skip it where the owner can't service real reviews.

### Local tiers

A target that is a **local citation surface** — one that publishes NAP and corroborates a business's existence in a place — carries a `local_tier` (1–6). This is **additive**: it does not replace `category`, which still drives the brand-class weighting above. A row can be `catalog` and tier 2 at once.

| Tier | What it is |
|---|---|
| 1 | Core universal, every country: Google Business Profile, Bing Places, Apple Business Connect |
| 2 | Country-general business directory — your home market's two or three big ones |
| 3 | Industry / niche directory |
| 4 | City / chamber body with a public member directory |
| 5 | Trade / accreditation body with a public member directory |
| 6 | Data aggregator — a US construct that feeds downstream US directories. **Check whether your market has one at all before looking for it**; several European markets have no equivalent, and an empty tier 6 is a correct result, not a gap. |

**Selection rule.** A property takes local tiers only when it has a genuine place-based service. Tier 1 is gated on real eligibility, not on wanting the listing — a business with no location customers visit and no travel-to-customer service does not qualify for Google Business Profile, and submitting anyway risks suspension.

**Record `listing_url` on the row when a listing is created.** Without it `nap-audit` cannot check that listing and reports it as unmeasured. This skill owns the citation half of local SEO and the canonical NAP; the page-side half (local landing pages, service-area content) is separate work.

## Phase 3 — Prepare

For each selected target, build a submission pack from `references/entity-pack.md`: name, category, description at the required length, URL, logo, NAP. **Run `/founder-pipeline:brand-voice` on any generated copy first** — it is external-facing text. Numbers come from your single numbers source of truth (whatever registry, sheet or database holds them), never from site copy, which goes stale silently.

**Ask, don't skip or invent.** If a required field has no answer in `entity-pack.md` or in your numbers source, stop and ask the owner directly rather than leaving it blank, guessing, or quietly skipping the field. Missing info is a question, not a reason to submit a thinner listing.

**Cross-link every property the form allows.** Any target whose form has more than one URL/website/social-link field — not just the primary submission URL — should carry links to the other active properties too (see the cross-promotion table in `entity-pack.md`), so a visitor arriving via one listing can discover the others. Don't limit a submission to the single property that triggered it if the form has room for more.

## Phase 4 — Execute (`/founder-pipeline:web-listings run <domain> [N]`)

Full mechanics — browser tab lifecycle, form-fill pattern, hard-stop detection and screenshot procedure — live in `references/automation-execution.md`. This section is the sequence; that file is the how.

**Rollout is staged, not a big-bang.** Zero-risk warm-up (free, no-login targets) first, then a small pilot batch through the full flow for the owner to review, then paced full rollout — never fire the whole remaining catalog in one session (rapid-fire submissions from one session read as automated and trip anti-bot defenses on some targets).

1. **Check whether an account already exists** before proposing a signup — ask the owner, or check whatever record you keep of which platforms they're already on. Never create a second account under a different email for a platform they already use.
2. **No login required, one-shot form** → drive the browser, fill from `entity-pack.md`'s copy tiers plus the live-fetched favicon/og:image assets, **ask in chat for a clear yes on this specific submission**, then submit.
3. **Login or account required** → OWNER-ONLY (Law 5). Prepare the complete pack and stage it as paste-ready content; the owner authenticates. If they stay at the keyboard, the agent may drive the post-login non-secret form-fill in that same session.
4. **Hard stop, screenshot, queue `OWNER-ONLY`** on: any account-creation or password field, any payment field, any CAPTCHA, any phone/SMS/ID verification step, any ambiguous link-back term. Record the row with the full pack plus exactly where execution stopped and the screenshot path. If you use an external task board, this is where the row is created (Type `Listing`, Status `Ready`, `Source` = `listings <DIR-NNNN>`); otherwise the row goes in `queues/manual-queue.md`. `Ready` is an open state — it should be escalated by whatever staleness check your board runs, if any.
5. Any target whose terms require a followed link-back → status `Killed` with the reason, never re-propose.
6. Any target failing the localize gate → status `Blocked`, note what's missing.
7. **Log every attempt** to `<property>/listings/runs.jsonl` — target, property, timestamp, outcome (submitted / hard-stop / failed), live-check result, screenshot path if a hard-stop occurred. The board (or `queues/manual-queue.md`) is the human-facing status ledger, one row per property × target; the jsonl log is the machine-level execution history — the two aren't redundant, don't skip the log because the row exists.
8. On `live` (spot-checked by fetching the actual listing URL, never assumed), flip the row to `Done` with the listing URL, record `listing_url` on the `targets.json` row, and update the `sameAs` table in `references/entity-pack.md`.

## Staleness

Any `targets.json` row with `verified_on` older than 90 days gets re-verified before use in a new run. Any registry list this old is stale — don't submit against it blind.

## A different question: how STRONG is a listing that already exists?

"Where should we list" (this skill) and "is it live and NAP-correct" (`nap-audit`) both leave a third question unanswered: how good is the listing itself. There is no separate skill for that in this plugin — do it inline when you want it, read-only, scoring each live listing on completeness (every optional field the form offered, actually filled), freshness (copy matches current positioning and current numbers), cross-link coverage (did the submission use every URL field the form had), and review-profile signal (does the listing carry any third-party validation). Return a ranked fix list, highest-traffic listing first. It needs `listing_url` recorded on the rows before it can run at all.

## Red flags — stop and ask

- A target requires a followed link-back "to verify" → Law 1, reject
- A target serves a language you have no localized pages in → Law 4, block, don't submit an English-only URL
- A target already appears `Done`/live for this property → skip, don't resubmit
- Agent about to create an account, enter a password, complete an SSO login, enter payment info, hit a CAPTCHA, or complete a phone/SMS/ID verification step → stop, screenshot, queue OWNER-ONLY instead (Law 5)
- About to fire more than a handful of submissions in one session → pace it, see the staged-rollout note in Phase 4

## Common mistakes

| Mistake | Fix |
|---|---|
| Submitting one property, ignoring the others that fit the same registry | Portfolio rule — check `applies_to` fit across every active property before closing the target |
| Treating an auto-populated registry-ID catalog entry as unsubmitted | Check current listing accuracy first; correct, don't resubmit |
| Using site copy for member/attendee counts | Your numbers source of truth is the only source |
| Counting a Wikidata or company-database listing as a referring domain | Entity accounting rule — separate line, never backlinks |
| Re-verifying a target that's <90 days old | Trust `verified_on`, don't burn a fetch |
| Getting an in-chat "yes, create the account" and acting on it | Law 5 is a platform boundary; authorization does not lift it |

## Optional dependencies

- **A browser-automation MCP server** (e.g. `claude-in-chrome`), installed separately, for Phases 2-4 form-fill. Without one, every submission is a prepared pack for the owner.
- **An external task board.** Without one, `queues/manual-queue.md` is the ledger.
- **A rank/backlink data provider** for the presence-audit shortcuts in Phase 1. Without one, Phase 1 runs on plain fetches.

## References

- `config/targets.json` — the catalog, one row per target, dated
- `config/properties.json` — the property registry: brand class, territory, legal entity
- `references/method.md` — per-category submission mechanics
- `references/entity-pack.md` — canonical NAP, bio, logo pointers, sameAs tracking table (ships as a template — fill it before the first run)
- `references/automation-execution.md` — browser mechanics, hard stops, and platform-specific gotchas
- `references/CHANGELOG.md` — version history of the method
- `scripts/nap_audit.py` — the `nap-audit` implementation; `tests/test_targets.py` — catalog invariants
