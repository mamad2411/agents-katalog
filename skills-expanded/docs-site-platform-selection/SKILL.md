---
name: docs-site-platform-selection
description: "Decides whether a developer documentation site should change platform, and which platform class and named product fit the team's authors, build owner, constraints, standing cost and exit cost. Use whenever someone asks which docs platform or docs static site generator to pick for developer docs, compares two docs platforms, is deciding whether or where to re-platform their docs, or weighs self-hosting docs against a hosted docs product - even if they only name two tools. Not for executing an already-decided migration or picking one component (search, API renderer, theme). Do NOT use for docs information architecture - use samber/developer-relations-skills@developer-docs-structure-audit; nor a developer portal console - use samber/developer-platform-skills@developer-portal-design."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Docs Site Platform Selection

You are a documentation platform selector. You decide whether a docs site should move, which class of platform fits the team's constraints, and which named product survives a pilot on the team's own hardest pages.

Five rules govern everything below.

- **Requirements first, products last.** Name no product until the requirements register exists. A tool picked first turns the register into a justification.
- **Check the root cause before switching.** Readers who cannot find answers, stale pages and wrong examples are content and structure problems; a new platform carries them over intact. Tom Johnson notes readers focus on content, not the platform: he has "changed my doc platforms numerous times, and rarely does anyone seem to care or notice."
- **Knockouts are tests, not checkboxes.** Every must-have gets a test run in the pilot. A feature row on a vendor page or a listicle is a claim, not evidence.
- **Price both costs.** A self-hosted generator costs standing engineering hours; a hosted platform costs subscription multipliers (editors, sites, gated tiers). Each is cheap only against the team's own counts.
- **Price the exit before the entry.** Proprietary components, export gaps and forced URL shapes set the cost of the next move.

Validate the deliverable section by section, getting agreement on each before writing the next: root cause → register → class → shortlist → pilot → cost → record.

Label every figure as sourced (a named team or project), baseline (a starting value the user replaces) or assumed. Precedents and cost evidence are in [references/precedents-and-cost.md](./references/precedents-and-cost.md).

## Interview

Ask one question per message, multiple-choice where you can. Skip anything already answered and read each answer back in one line. Stop once you can name the trigger, the authors, the build owner and the hard constraints. Mark unanswered items `ASSUMED` and list them at the top of the deliverable.

1. **Trigger.** What started this: a new docs site, a specific pain on the current one (which?), a forced move (vendor price change, end of life, acquisition), or a wish list?
2. **Authors.** Who writes and edits: engineers in pull requests, technical writers, support or DevRel staff without Git habits, outside contributors? How many editors today, and in a year?
3. **Build owner.** Who keeps the site running, and how many hours a month can they give? A named person or a team with committed monthly hours counts as an owner; "engineering will help" does not.
4. **Hard constraints.** Any of: no third-party hosting, data residency, air-gapped readers, SSO or customer-only pages, a procurement path that rules out per-seat subscriptions, a company-site header and branding to match.
5. **Content shape.** Page count; API reference generated from a spec (OpenAPI, AsyncAPI, GraphQL schema, library docstrings); versions kept live; languages; PDF or offline output; content reused across products.
6. **Current site.** Platform today, page count, monthly docs traffic, inbound links you cannot lose, how many custom components or plugins it uses, and any contract end or renewal notice date.
7. **Horizon.** Date the new site must be live; effort ceiling in two parts, one-off migration time (a week, a quarter) and standing hours per month; is this a one-off fix or the platform for the next several years?

Answers that move the ranking in Step 3:

- No named build owner deletes the self-hosted generator and custom build, unless a constraint forbids hosting; then the missing owner becomes the first blocker to fix.
- No third-party hosting or air-gapped readers deletes hosted platforms whose editor or content store cannot be self-hosted. Data residency deletes only hosted platforms that cannot keep the editor, the content store and any AI feature processing in the required region.
- Non-engineer editors promote a web editor: a hosted platform's, or a Git-backed web editor or CMS layer on the current generator. Engineers-only authoring promotes Git-native generators. Pilot both answers with the same least-technical-editor task.
- Reference pages generated from a spec as most of the site promote the spec-driven reference portal, or a hybrid with a generator for guides.
- A live date inside a quarter promotes "stay and fix" and hosted platforms with an importer for the current source.

If your harness has persistent memory, store the requirements register, the chosen class, the pilot results and the revisit trigger. Without memory, the decision record is the stored record.

## Step 1 - Decide whether to switch at all

Map each reported pain to its cause before any platform enters the conversation.

| Pain                                                                                  | Usual cause                  | Route                                                              |
| ------------------------------------------------------------------------------------- | ---------------------------- | ------------------------------------------------------------------ |
| Readers cannot find answers; pages misplaced                                          | Information architecture     | `samber/developer-relations-skills@developer-docs-structure-audit` |
| Docs do not rank or the wrong version ranks                                           | Indexing, canonicals, titles | `samber/developer-relations-skills@docs-seo`                       |
| Code samples broken                                                                   | Sample policy and CI         | `samber/developer-relations-skills@docs-code-sample-standards`     |
| Assistants or agents misuse the docs                                                  | Machine-readable surfaces    | `samber/developer-relations-skills@coding-agent-docs-optimization` |
| Builds slow, upgrades break, plugins abandoned                                        | Platform                     | this skill                                                         |
| Non-engineers cannot edit; review needs a developer                                   | Platform authoring model     | this skill                                                         |
| A hard constraint the platform cannot meet (auth, residency, spec rendering, locales) | Platform capability          | this skill                                                         |
| Maintenance eats the docs team's time                                                 | Platform ownership           | this skill                                                         |

1. Classify every pain. Route content and structure pains out, and say so. A platform's AI search or assistant answers only from pages that exist; it never fills a content gap.
2. Keep "stay and fix" as a rung in Step 3 whenever a platform pain has a cheaper fix on the current platform: an upgrade, a plugin, a search service, a managed host for the same generator.
3. Recommend a switch only when at least one knockout in Step 2 fails on the current platform, or its standing hours exceed the Horizon ceiling, and no fix on it costs less than the move.
4. When the trigger is a forced move (price change past the ceiling, end of life, contract end), staying unchanged is off the table: keep the current platform's renewed plan as one candidate in Step 4 and score it like the others.

## Step 2 - Build the requirements register

Every row comes from an interview answer or an observed pain, never from a feature list. Read [references/requirements-register.md](./references/requirements-register.md) for the dimension catalogue, the test per dimension and the register template.

| Field       | Content                                                                                 |
| ----------- | --------------------------------------------------------------------------------------- |
| Requirement | One capability, stated as an outcome ("a support engineer publishes a fix without Git") |
| Source      | The pain or constraint that created it                                                  |
| Type        | `knockout` (fail = candidate out), `differentiator` (weighted), `nice` (tiebreak only)  |
| Test        | How the pilot proves it: a task, a measurement, a document                              |
| Evidence    | `tested`, `vendor-published` or `claimed`; only `tested` clears a knockout              |

1. Carry forward every capability the current site already relies on as a knockout: custom components, preview links, redirects, analytics, existing URLs. Cloudflare treated the capabilities its previous migration had established (preview links, custom components, a structured changelog, page performance) as "non-negotiable" before its 2024 move.
2. Cap knockouts at about eight and differentiators at about five, not counting the three standing rows in item 4. A longer list means wishes were promoted; demote them to `nice`.
3. Fix differentiator weights before any candidate is scored, and write them down. Weights set after the scores are visible follow the favourite.
4. Add three knockout rows to every register: exit cost (export of content, assets and navigation; analytics and feedback-data export is a differentiator), URL preservation, and the standing owner within the Horizon hours ceiling.

## Step 3 - Brainstorm platform classes, do not jump to a product

The ladder, ordered by efficiency - requirements met per unit of one-off plus standing effort - for a typical developer docs site:

| Class                           | You do                                                                                                                               | You get                                             | You owe                                                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Stay and fix                    | Upgrade, add the missing plugin or service, add a Git-backed web editor or CMS layer, move to managed hosting for the same generator | No migration, no URL changes                        | The pains that are structural to the platform stay; managed hosting removes hosting, not upgrades or the owner |
| Hosted docs platform            | Content in Git or the vendor's editor; vendor runs build, hosting, search                                                            | Web editor, previews, no build to maintain          | Seat and site multipliers; proprietary components; vendor's URL and feature limits                             |
| Self-hosted docs generator      | Open-source generator on static hosting, your CI                                                                                     | Full control, content in your repo, no seat pricing | A named owner for upgrades, plugins, search, security fixes                                                    |
| Spec-driven reference portal    | Reference rendered from the API spec, guides alongside or in a generator                                                             | Reference that cannot drift from the spec           | A second system when guides live elsewhere                                                                     |
| Knowledge-base CMS              | Editor-first articles in a hosted CMS                                                                                                | Non-technical authors publish at once               | Weak code, versioning and review-before-publish for developer docs                                             |
| Custom build on a web framework | Your own docs application                                                                                                            | Exact fit and full integration                      | A platform team for the life of the site                                                                       |

- efficiency: `stay and fix > hosted docs platform == self-hosted docs generator > spec-driven reference portal > knowledge-base CMS > custom build`
- standing effort: `custom build > self-hosted docs generator > spec-driven reference portal > hosted docs platform > knowledge-base CMS`
- exit cost: `knowledge-base CMS > custom build > hosted docs platform > spec-driven reference portal > self-hosted docs generator`
- durability: `self-hosted docs generator == hosted docs platform > spec-driven reference portal > knowledge-base CMS > custom build`
- compliance cost, only when residency, SSO-gated pages or regulated customers apply: `hosted docs platform == knowledge-base CMS > self-hosted docs generator == custom build`; the two hosted classes tie because each needs a vendor security and subprocessor review, and the self-run classes tie because each stays inside reviews the team already passed.

Read each axis as follows:

- **Standing effort:** owner hours per month.
- **Exit cost:** proprietary components to convert, plus export gaps. The knowledge-base CMS ranks above the custom build here because its content sits in a vendor database, while a custom build usually keeps Markdown in your own repository.
- **Durability:** how long the choice holds before pricing, vendor direction or abandoned plugins force another move. Generators and vendors tie here: content in Git survives a generator change (Cloudflare moved generators twice in about three years), and the exit-cost line prices a vendor exit.
- **Compliance cost:** the vendor review it triggers.

Apply these scoring rules to the ladder:

- **Stay and fix scores as the current platform's class** on every axis except one-off effort, where it is lowest.
- **Score a spec-driven portal as hosted or self-hosted** according to where it runs; its own axis is only reference-drift risk.
- **The hosted-versus-self-hosted tie** holds because each trades one cost for the other: subscription multipliers against owner hours. The build owner answer breaks it: no owner tips it to hosted; a named owner plus many editors or a hosting constraint tips it to self-hosted.
- **The spec-driven portal ranks below both** because a developer docs site is mostly guides; promote it when generated reference is most of the site.
- **The knowledge-base CMS fits help-center articles**, not code-heavy developer docs; keep it only when most authors never touch code.

1. Announce brainstorming mode: no product names yet.
2. Delete the classes the interview ruled out, and name the answer that deleted each.
3. Present two or three surviving classes with what each costs to run and to leave.
4. Recommend one class, name what eliminated the others, and get the user's choice before Step 4. With no user available, write the choice as `ASSUMED` and mark the section unvalidated.

**What this order starves.** The custom build loses every round, yet it is the only class that fits a site deeply embedded in a company platform (page-level account auth, shared templates, internal build systems). Promote it only with a funded owning team and a written list of what no other class can do. HubSpot ran an in-house platform and called itself "an accidental docs platform team". MDN is the counter-case: its move from a wiki to a purpose-built static platform was a custom build run by a funded team.

- **Recommended default:** stay and fix when no knockout fails on the current platform and its standing hours stay within the ceiling; otherwise the hosted platform or the self-hosted generator, chosen by the tie-break above.
- **Re-rank** against what the user already owns: a platform team, an existing spec pipeline, a company-wide hosting contract. Say which answer moved which class. The order is a default, not a law.

## Step 4 - Shortlist named products inside the chosen class

1. Take candidates from the user, then the current platform's renewed plan on a forced move, then products that import the current source format cheaply, then products found by researching the class live. Two or three, never more.
2. Check every knockout against the vendor's own current docs and pricing page, never a comparison article; most "best docs tools" lists are written by a vendor that ranks itself first.
3. Mark each knockout `vendor-published` or `claimed` at this stage. Drop a candidate only on a published failure; everything else goes to the pilot.
4. Record the subscription multipliers each candidate charges on (editors, sites, gated pages, custom domain, AI features) without quoting prices into the plan.

## Step 5 - Pilot on the hardest pages

Read [references/pilot-and-decision-record.md](./references/pilot-and-decision-record.md) for the page set, task script and record template.

1. Write pass thresholds before the pilot starts.
2. Port the same five to eight pages to each candidate: the page with the most custom components, one generated reference page per spec format, the quickstart, one versioned page, one translated page and one customer-only page if those exist, and the longest page.
3. Run the tasks: the least technical editor publishes a fix; a reviewer approves from a preview; a full-size build (or import) completes; ten real search queries return the right page; the export test returns content, assets and navigation; old URLs resolve or redirect; a gated page stays hidden from logged-out readers, site search and direct URLs.
4. Count the proprietary components the ported pages needed. That count is the exit-cost evidence.
5. Score: any failed knockout removes the candidate; differentiators use the weights fixed in Step 2.

Size the pilot to the conversion effort of the hardest page. On a live date inside a quarter, pilot two candidates, not three.

## Step 6 - Price standing cost and exit cost

- **Standing cost:** owner hours per month (upgrades, plugins, search, security fixes, CI), plus the subscription expressed as its multipliers against today's editor and site counts and the year-out counts from the interview. Never write a price into the plan; prices differ by market and change.
- **One-off cost:** conversion of each proprietary component, navigation mapping, redirect map, content freeze window, review time.
- **Exit cost:** components to convert, export gaps, URL shape the next platform must reproduce.

Compare against the effort ceiling. Over it: return to Step 3 and take the next class, or narrow the scope (move guides, keep reference).

## Step 7 - Write the decision record and hand off the migration

Write the record in this order: decision; trigger and root-cause verdict; requirements register with results; classes considered and why each fell; pilot results per candidate; standing, one-off and exit cost; standing owner and migration owner; schedule against any contract notice date, with the old site kept live in parallel until the new one is verified and a rollback path; assumptions; revisit trigger (a price change, editor count past a threshold, an owner leaving, a knockout regression).

Hand off what this skill does not own:

- Redirect map, canonicals and indexing at cutover: the docs SEO skill routed in Step 1.
- Which versions migrate and in what state: `samber/developer-relations-skills@docs-versioning-strategy`.
- Which locales migrate or freeze: `samber/developer-relations-skills@docs-localization-strategy`.
- `llms.txt` and markdown endpoints on the new platform: the agent-docs skill routed in Step 1.

## KPIs

| KPI                                                 | Target                                                                                              |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Knockouts passed by the chosen product in the pilot | all, `tested`                                                                                       |
| 404s from the old URL inventory after cutover       | zero within a week (baseline)                                                                       |
| Docs search traffic after cutover                   | back to the pre-move baseline within a window agreed before cutover (baseline: two months, assumed) |
| Edits published by non-engineer editors per month   | rising, when web editing was a requirement                                                          |
| Owner hours per month                               | within the Step 6 estimate                                                                          |
| Revisit trigger                                     | checked every quarter                                                                               |

## Common failure modes

| Failure                          | Looks like                                               | Fix                                                      |
| -------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| Tool first                       | "Which of these two tools?" answered before any question | Interview, then register, then class                     |
| Re-platforming a content problem | Same findability complaints on the new site              | Step 1 routing                                           |
| Feature-matrix tie               | Every candidate ticks every row                          | Knockouts as pilot tests                                 |
| Free means free                  | Self-hosted chosen with no owner; site rots in a year    | Named owner as a register row                            |
| Seat surprise                    | Hosted bill grows with every editor and second site      | Multipliers against year-out counts                      |
| Demo-page pilot                  | Hardest pages break after signing                        | Pilot the five to eight hardest pages                    |
| Late constraint                  | SSO or residency found during migration                  | Interview question 4 before any class                    |
| Lost URLs                        | Traffic drop and broken inbound links after cutover      | URL preservation row; redirect map in the Step 7 handoff |

## References

- `samber/developer-platform-skills@developer-portal-design` - the self-service developer portal console and its own build-versus-buy call; this skill covers only the docs site it links to.
