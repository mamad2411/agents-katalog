---
name: marcom-best-practices
description: This skill should be used when the user wants to find and apply best practices for a MARCOM (marketing communications) project, idea, channel, or campaign — e.g. "find me the best practices for [X]", "before we go a new direction on [X], what should we be doing", "/marcom-best-practices [target]", "audit how we do [email/SEO/launch/social/…]", "are we doing [X] wrong". It sweeps three tiers — our installed plugins/skills, the Workforce Automation tool catalog (every known Claude skill/plugin/MCP, so it can recommend capabilities we don't have yet), and heavy external web research — then benchmarks MoxyWolf's current practice against what it finds, and returns a prioritized best-practices brief plus a "run these next" plan. Assumes the premise that we are probably doing it wrong and should consult the full toolbox before committing to a new direction.
---

# MARCOM Best Practices

Point this at a MARCOM target — a project, an idea, a channel, a campaign, a funnel stage — and it answers one question: **what are the best practices we should be following, and where are we falling short of them?** It does that by scouring our own toolbox first, then the wider Claude-tool ecosystem for capabilities we don't have, then the outside world, and finally benchmarking our current practice against all three.

The operating premise (the user's words): *we are probably doing things wrong, and before we move a new direction we want the full toolbox consulted.* So this skill is deliberately critical — it surfaces gaps, not reassurance.

## When to use

- "find me the best practices in MARCOM for [target]"
- "before we change direction on [X], what should we be doing?"
- "audit how we do [email / SEO / launches / social / lifecycle / pricing pages / …]"
- "are we doing [X] wrong?"
- `/marcom-best-practices [target]`

If the target is vague, ask (see *Inputs*). Otherwise start the sweep immediately.

## Inputs

Resolve these before the sweep. If the user gave the target in the invocation, use it; only ask for what's missing (one `AskUserQuestion`, ≤3 questions):

- **Target** — the MARCOM project/idea/channel in focus (e.g. "our onboarding email sequence for STIGViewer", "OpenControls launch", "LinkedIn thought-leadership", "the SAMS pricing page"). Required.
- **Goal / metric** — what success looks like (activations, MQLs, reply rate, signups, pipeline, rankings). Shapes which best practices matter.
- **Product line / audience** — which MoxyWolf product and which reader (SAMS, STIGViewer, RegGenome, OpenControls, Frontier Founder, …). Scopes the benchmark and the voice.

Unattended (scheduled) run with no target: stop and write a one-line note that a target is required; don't guess one.

## MARCOM domain taxonomy

Classify the target into one or more domains. This is the spine of the whole sweep — Tier 1's map, Tier 2's search regexes, and the benchmark all key off it.

1. **Positioning, messaging & brand/voice**
2. **Audience & customer research** (ICP, JTBD, customer interviews)
3. **SEO & AI-visibility** (technical, on-page, programmatic, schema, GEO/answer-engine)
4. **Content & editorial** (blog, thought leadership, content strategy, repurposing)
5. **Social & community** (LinkedIn, community marketing, scheduling)
6. **Lifecycle email & outreach** — treat the full funnel as first-class, not one "email" bucket: **onboarding/activation → nurturing/education → upgrade/expansion → retention/win-back**, plus **cold outbound/prospecting**. This is the domain we most often under-cover; always expand it into its stages.
7. **Paid acquisition & creative** (search/social ads, ad creative, ASO)
8. **Conversion optimization** (landing/page CRO, signup, forms, popups, paywalls, onboarding UX)
9. **Pricing, packaging & offers**
10. **Campaigns, launches & GTM**
11. **Partnerships, PR & earned media** (co-marketing, PR/journalist outreach, podcasts, directories, referrals)
12. **RevOps, analytics & measurement** (attribution, tracking, A/B testing, dashboards, lead lifecycle)
13. **Competitive & market intelligence**

## The sweep — three tiers

Run the tiers in order; each feeds the benchmark. Fan out with parallel reads/searches where you can.

### Tier 1 — our installed toolbox (what we already have)

For each in-scope domain, pull the best practices our installed skills already encode, and note which skill owns each. This is the curated map; skills live across several installed marketplaces, so reference them by their `plugin:skill` invocation name.

| Domain | Our installed skills (by invocation name) | Live data / MCP |
|---|---|---|
| Positioning / brand / voice | `marketing:brand-review`, `moxywolf-skills:brand-guidelines`, `moxywolf-skills:voice-injection`, `growth-engineer-skills:product-marketing-context`, `growth-engineer-skills:marketing-psychology`, `product-orchestrator:product-gtm` + vault `_Shared Knowledge/Brand and Voice/dorian-cougias.md` | — |
| Audience & customer research | `growth-engineer-skills:product-marketing-context`, `research-pipeline:*`, `council:deliberate` | Clarify CRM, `moxywolf-crm` (Supabase `easplopgieskgqaifajp`) |
| SEO & AI-visibility | `searchfit-seo:*` (seo-audit, technical-seo, on-page-seo, programmatic-seo, schema-markup, ai-visibility, keyword-clustering, internal-linking), `growth-engineer-skills:seo-audit`/`ai-seo`/`programmatic-seo`/`schema-markup`/`site-architecture`, `marketing:seo-audit` | **Ahrefs MCP**, GSC via Ahrefs |
| Content & editorial | `4d-blog-engine:*`, `editorial-forge:*`, `moxywolf-skills:blog-content-ecosystem`/`sorkin-dob-weekly-blog`/`stigviewer-content-ecosystem`, `research-pipeline:write-article`, `growth-engineer-skills:content-strategy`/`copywriting`/`copy-editing`/`social-content` | — |
| Social & community | `linkedin-growth:*`, `moxywolf-skills:linkedin-thought-leadership`/`linkedin-analytics`, `synergy-engine:*`, `growth-engineer-skills:social-content` | **Postiz MCP**, Apify (LinkedIn) |
| Lifecycle email & outreach | `growth-engineer-skills:email-sequence`/`onboarding-cro`/`signup-flow-cro`/`churn-prevention`/`paywall-upgrade-cro`/`cold-email`, `marketing:email-sequence`, `sales:draft-outreach`, `apollo:sequence-load`, `moxywolf-skills:birds-of-a-feather-outreach` | Mailtrap MCP, Apollo MCP, `moxywolf-crm` |
| Paid & creative | `growth-engineer-skills:paid-ads`/`ad-creative` | — |
| Conversion optimization | `growth-engineer-skills:cro-audit`/`page-cro`/`form-cro`/`onboarding-cro`/`signup-flow-cro`/`popup-cro`/`paywall-upgrade-cro`, `saas-frontend-designer:*` | **PostHog** (431506), GA4 |
| Pricing & offers | `saas-pricing-engine:*` (competitor-scan, price-check, tier-builder), `growth-engineer-skills:pricing-strategy` | — |
| Campaigns / launch / GTM | `growth-engineer-skills:marketing-ideas`/`marketing-brief`/`launch-plan`/`launch-strategy`, `marketing:campaign-plan`, `product-orchestrator:product-gtm`, `frontier-founder-smb:campaign-creator`/`run-campaign` | — |
| Partnerships / PR / earned | `moxywolf-skills:podcast-booking-ladder`/`birds-of-a-feather-outreach`, `growth-engineer-skills:referral-program`/`free-tool-strategy` | Apify |
| RevOps / analytics | `growth-engineer-skills:revops`/`analytics-tracking`/`ab-test-setup`, `marketing:performance-report`, `analytics:google-analytics`, `linkedin-growth:analytics` | **PostHog**, **GA4**, **Ahrefs**, Monarch (spend) |
| Competitive & market intel | `marketing:competitive-brief`, `searchfit-seo:competitor-analyzer`, `saas-pricing-engine:competitor-scan`, `moxywolf-skills:market-awareness-analyzer`, `sales:competitive-intelligence` | Ahrefs, Firecrawl, Perplexity |

To read what a skill actually recommends, read its `SKILL.md` (in the installed plugin) or invoke it read-only. Don't assume — the point is to surface the *real* encoded best practice.

### Tier 2 — the Workforce Automation catalog (capabilities we DON'T have)

The `workforce-automation` Supabase project (`lmhfgsaznbwnnfldpxgc`) catalogs ~580K Claude tools (skills, plugins, MCPs, commands) harvested from the ecosystem, with an `installed` source that mirrors our own set. Query it via the **Supabase MCP** (`execute_sql`) to surface adoption candidates — high-signal tools that fit the target's domain and that we don't already have.

Schema that matters: `tools` (`current_name`, `current_description`, `current_long_description`, `current_category_declared/observed`, `kind`, `status`, `is_canonical`, `dup_count`, `source_id`), `sources` (`name`), and — where seeded — `capabilities` / `tool_capability_map` (`automation_level` ∈ replaces/augments/supports/informs). Note: the structured capability bridge is currently seeded only for 3 pilot security/engineering occupations, so **for MARCOM, discover by text/category search on `tools`, not through the capability map.**

Ranking signal: prefer curated sources (`coreyhaines31/marketingskills` is a 47-skill marketing pack), then `dup_count` desc (prevalence across the ecosystem ≈ consensus). Always exclude what's already in the `installed` source.

Adoption-candidate query (substitute the domain regex from the target's domains):

```sql
with installed as (
  select lower(t.current_name) nm
  from public.tools t join public.sources s on s.id = t.source_id
  where s.name = 'installed'
)
select t.current_name, left(coalesce(t.current_description,''),160) as descr,
       sr.name as source, t.kind::text, t.dup_count
from public.tools t
join public.sources sr on sr.id = t.source_id
where t.status = 'active' and coalesce(t.is_canonical,true) = true
  and sr.name <> 'installed'
  and (coalesce(t.current_name,'') || ' ' || coalesce(t.current_description,'') || ' ' ||
       coalesce(t.current_category_declared,'') || ' ' || coalesce(t.current_category_observed,''))
      ~* :DOMAIN_REGEX
  and lower(t.current_name) not in (select nm from installed)
order by (sr.name = 'coreyhaines31/marketingskills') desc, t.dup_count desc nulls last
limit 40;
```

Domain regex starters (extend per target):

- Lifecycle email & outreach: `(email sequenc|drip|nurtur|lifecycle|onboarding|activation|win-?back|re-?engage|retention|cold email|newsletter|autoresponder|sms)`
- SEO & AI-visibility: `(seo|search engine|schema|structured data|programmatic seo|generative engine|answer engine|geo\M|llm.?visib)`
- CRO: `(conversion|cro\M|landing page|signup|onboarding|paywall|popup|form optimi)`
- Launch/GTM: `(launch|go-to-market|gtm\M|product hunt|announcement|positioning)`
- PR/partnerships: `(public relations|pr\M|journalist|earned media|podcast|co-marketing|directory|referral|affiliate)`

Also pull the curated marketing pack directly for the domain (`where sr.name='coreyhaines31/marketingskills'`) — it's dense, well-written, and a good "what does a complete skill set for this look like" reference even where we won't install it.

Present Tier-2 results as **adoption candidates**: name, what it does, source, and a one-line "worth installing because…". Flag anything that would fill a gap the benchmark (below) exposes.

### Tier 3 — external best-practice research (the outside world)

Treat the target as a real research question. Use `research-pipeline:discover-literature`, Perplexity (`perplexity_research`/`perplexity_reason`), Firecrawl (`firecrawl_search`/`firecrawl_scrape`), and Ahrefs (SERP/competitor data) to gather: current best practices for the domain, benchmarks/metrics to aim for, and 2-4 competitor or category-leader examples. Adversarially check claims — prefer primary sources and recent (≤18-month) material; note where "best practice" is contested. `council:deliberate` is available when the target warrants multiple expert lenses.

## Benchmark — what we do now vs. what best practice says

Read our current practice for the target and score it honestly against Tiers 1-3:

- **Artifacts** — the relevant Taskade `12 – MARCOM` folder (mind the dash: Team Plugins uses `12 – MARCOM` en-dash; other projects vary — `ls` first), the product's own project folder, and vault brand/voice.
- **Live signal** — pull the metric that matters via GA4 (`analytics:google-analytics`), PostHog (431506), Ahrefs, Postiz, or `moxywolf-crm`/Clarify, scoped to the target. Don't assert performance without a number.
- For each best practice, mark: **doing it**, **doing it partially**, **not doing it**, or **doing the opposite**. The "probably doing it wrong" premise means: don't grade on a curve.

## Output — the best-practices brief

Write a markdown brief to the target project's `12 – MARCOM/` (or `08 – Go-to-Market/` if that fits better), named `marcom-best-practices-<target-slug>-YYYY-MM-DD.md`, with:

1. **Target & goal** — one line each.
2. **Domains in scope** — from the taxonomy.
3. **Best practices that matter here** — the synthesized set from all three tiers, each with its source (our skill / catalog tool / external), ranked by impact on the stated goal.
4. **Where we stand** — the benchmark table (practice → status → the number, if any).
5. **Gaps, most costly first** — where we're partial / not doing it / doing the opposite.
6. **Recommendations** — prioritized, concrete, no wall-clock estimates (complexity/dependencies only, per project rules).
7. **Adoption candidates** — Tier-2 tools worth installing to close a gap, with why.
8. **Run these next** — the ordered list of installed skills to invoke for this target (feeds the auto-run step).

Deliver the file with `SendUserFile`. If the target is a recurring surface the user will revisit (a channel scorecard, a lifecycle map), also offer an HTML scorecard persisted via `create_artifact`.

## Auto-run the top applicable sub-skills

After the brief, invoke the highest-value **installed** skills from the "Run these next" list to produce starter deliverables in the same pass — e.g. for a lifecycle-email target, run `growth-engineer-skills:email-sequence` (or the onboarding/nurture/win-back variants) against the benchmarked gaps; for SEO, run `searchfit-seo:seo-audit`.

Guardrails: confirm before running more than ~2 heavy skills or anything that writes outside Taskade/sends anything; run read-only/generative skills freely; never let auto-run send outreach, post socially, or push code without the human gate those skills already enforce. Collect each sub-skill's output into the target folder and reference it from the brief.

## Edge cases

- **Supabase MCP not pointed at `workforce-automation` / no access.** Tier 2 degrades to the curated-pack knowledge embedded here plus Tier-3 web research; note the degradation in the brief rather than silently skipping "capabilities we don't have".
- **Catalog returns tens of thousands of matches.** Expected (~40K for broad MARCOM). Always apply the canonical filter, the `installed` exclusion, and the curated-source-then-`dup_count` ranking, and cap at 40; log that the list is ranked-and-capped, not exhaustive.
- **A named skill isn't installed in this session.** It may live in a marketplace the user hasn't added. Note it as an adoption candidate rather than trying to invoke it.
- **No live metric available for the target.** Say so; benchmark on artifacts alone and flag "instrument this" as a recommendation.
- **Target spans many domains** (e.g. a full GTM). Scope to the 2-3 highest-leverage domains for the stated goal rather than sweeping all 13 shallowly; say which you dropped.

## Notes

- Reference skills by `plugin:skill` invocation name so the brief is actionable regardless of which marketplace they came from.
- The Workforce Automation catalog is a living index (daily walker + nightly discovery); re-querying later surfaces newly-published tools. Don't cache its results into this skill — query live.
- Respect voice rules for any prose that will be read outside the team (read `dorian-cougias.md`); internal brief prose can be lighter.
- No wall-clock time estimates; MoxyWolf is a small team, never "solo founder"; never fabricate names or numbers.
