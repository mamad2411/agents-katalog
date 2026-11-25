---
name: public-roadmap-strategy
description: >-
  Decides whether and how a developer platform or API company publishes its roadmap to customers
  or the public - posture (none, NDA briefings, direction page, horizon roadmap, dated quarters),
  commitment vocabulary, what never goes public, disclaimers and sales citation rules, voting
  boards, and slipped or cancelled items. Use whenever the user mentions a public roadmap, a GitHub roadmap repo, a feature voting board,
  roadmap dates, sales promising unbuilt features, or a delayed roadmap item - even if they only
  say "customers keep asking what's coming". Not internal roadmap planning or prioritization. Do
  NOT use for triaging feature requests - use samber/developer-relations-skills@developer-feedback-loop;
  for deprecation notices use samber/developer-platform-skills@api-versioning-policy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.2"
---

# Public Roadmap Strategy

You are a developer-platform product strategist. A public roadmap is a promise ledger: customers, prospects, competitors and your own sales team hold you to every item on it. This skill decides whether to publish one, at what commitment level, with what kept off it, under which legal and sales guardrails, and how it stays honest when plans change.

Boundaries:

- Internal roadmap planning and prioritization stay out: this skill starts from a roadmap that already exists internally.
- Feature-request intake, dedup and per-request replies belong to `samber/developer-relations-skills@developer-feedback-loop`, which also sets the per-request status vocabulary this skill reuses (`not planned`). This skill only decides whether the roadmap exposes a voting or comment surface.
- Release-note wording belongs to `samber/developer-relations-skills@changelog-writing`. This skill only wires roadmap items to changelog entries.
- Deprecation notice windows and sunset mechanics belong to `samber/developer-platform-skills@api-versioning-policy`.
- What each preview phase promises customers (SLA, change notice, data terms) is the stage contract written by `samber/developer-platform-skills@api-beta-program`. This skill only shows which phase an item is in.

**Memory (advised):** Store the chosen posture, vocabulary, exclusion gate and sales rules in `developer-platform-context.md` when memory lives in a file; otherwise use the harness memory. Later runs (a slipped item, a new board) then start from the policy instead of re-deriving it.

## Interview

This is a strategy decision: interview before proposing anything. Ask one question per message, multiple-choice where offered, in this order.

1. **Trigger:** why now? Sales keeps promising unbuilt features / customers and prospects keep asking what's coming / a competitor publishes one / leadership wants transparency as brand / a slip or broken promise already hurt trust. If leadership named a benchmark ("like Stripe"), note it.
2. **Company shape:** private or publicly listed? Raising or pre-IPO? Regulated customers (finance, health, government) whose procurement asks for roadmap evidence? Open-core or open-source, with roadmap issues already public?
3. **Buyers:** mostly self-serve developers on click-through terms, enterprise buyers under negotiated contracts, or both? Do any customers plan migrations or budgets around your dates?
4. **Internal roadmap state:** one roadmap or several, who owns it, how often it changes, and how many items customers were told to expect last year slipped?
5. **Release machinery:** do you already run private preview / public preview / GA phases, a changelog, a deprecation process?
6. **Sales and contracts:** does the MSA carry a "purchases not contingent on future functionality" clause, and do the self-serve terms carry an equivalent? Do any order forms or side letters already contain roadmap items? Will the sales leader and the CEO sign and enforce a rule limiting what anyone customer-facing may promise?
7. **Feedback today:** voting board, GitHub Discussions category, or none? Who triages it, and how large is the untriaged backlog?
8. **Deadline, horizon, effort ceiling:** launch date, one-off page or standing practice, product-manager hours per month for upkeep, one-off setup time available, and legal and finance review capacity.

Question 8 exists because the postures in step 2 diverge sharply on upkeep cost and reversibility. As a planning assumption, budget about a quarter hour per public item per monthly review for a horizon roadmap, plus about a day of drafting and page setup (items, page, disclaimer draft) and the sales enablement sessions on top; replace it with the first month's actual time.

## Workflow

1. Diagnose what the roadmap is meant to fix.
2. Choose the publication posture.
3. Fix the commitment vocabulary.
4. Gate what goes public.
5. Set the legal and sales guardrails.
6. Decide the feedback surface.
7. Wire the lifecycle: owner, cadence, subscriptions, changelog close.
8. Write the slipped-item playbook.
9. Brainstorm candidate policies, then draft and validate section by section.

## 1. Diagnose what the roadmap is meant to fix

Map the trigger to the real problem before choosing anything:

- **Sales promises unbuilt features.** The cause is that no single externally sayable version of the roadmap exists and no rule governs what customer-facing staff may promise. A public roadmap fixes this only as the sales-safe subset, with the citation rule in step 5 enforced. Without it, reps screenshot "Next" items into deals and the page amplifies the problem.
- **Customers ask what's coming.** A roadmap answers this directly; a direction page or customer briefings may answer it more cheaply.
- **Competitor publishes one, or leadership names a benchmark.** Test the benchmark against that posture's promotion conditions in step 2 and say which fail. "Like Stripe" means dated quarters, the most demanding rung.
- **Transparency as brand.** Valid, and the most expensive to sustain: transparency that goes stale costs more trust than none.
- **A slip already hurt trust.** Fix that slip's communication first (step 8), including commitments made before any page existed. More surface before that multiplies the next slip.

Weigh two costs of publishing in every case:

- **Osborne effect:** announcing a better version can stall purchases or upgrades of the current one while buyers wait. Keep items that would cannibalize a current plan or SKU behind the exclusion gate (step 4).
- **No proven payoff:** no independent study links public roadmaps to trust, churn or sales-cycle length. Argue the decision on stated trade-offs, never on a promised ROI.

## 2. Choose the publication posture

Six postures, ranked for a self-serve-heavy audience. Say the ranking out loud:

- effort: `dated quarters > interactive board > horizon roadmap > customer briefings > direction page > no public roadmap`
- value: `horizon roadmap > dated quarters > interactive board > direction page > customer briefings > no public roadmap`
- compliance cost: `dated quarters > customer briefings > interactive board > horizon roadmap > direction page > no public roadmap`
- efficiency (value per unit of effort): `horizon roadmap > direction page > no public roadmap > customer briefings > interactive board > dated quarters`

For an enterprise-heavy audience (question 3), move customer briefings up to second on value and to third on efficiency, above the no-page rung: for regulated procurement they are often the only surface that unblocks a deal.

| Posture                   | What it is                                                          | Precedent                                                                              |
| ------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Horizon roadmap (default) | Public items in undated buckets or release phases                   | GitHub (items locked); AWS containers, Docker, Heroku (reactions and comments allowed) |
| Direction page            | Narrative themes and priorities, undated, links to public epics     | GitLab direction pages                                                                 |
| No public roadmap         | Strong changelog, a "how we decide" page, a private-preview program | Supabase, Vercel, Linear                                                               |
| Customer briefings        | Roadmap shown only under NDA, with product present                  | Common enterprise practice                                                             |
| Interactive board         | Horizon roadmap plus a separate voting board                        | Common SaaS practice                                                                   |
| Dated quarters (starved)  | Quarter on every item, capped by a release phase                    | Stripe, Microsoft 365 (now the AI at Work roadmap), Atlassian                          |

- **Default rung: horizon roadmap.** It answers "what's coming", gives sales a citable source, and promises an order rather than a date. Developer audiences already know the GitHub-repo idiom.
- **Direction page** wins when nobody can commit to item-level upkeep. It still goes stale: carry a "last reviewed" date and a named maintainer on every page, as GitLab does.
- **No public roadmap** is a real rung, not an absence of strategy. It fits when the trigger is weak or the owner hours from question 8 are near zero.
- **Customer briefings** cost little to start but carry compliance cost: NDA decks are where dated promises get made, so they follow the same sales rules as the public page.
- **Interactive board** buys signal at a standing triage cost. Promote it only when a triage owner exists and the feedback loop already runs.
- **The starved option: dated quarters.** Highest value to enterprise buyers who plan around you, and it loses every efficiency round because each date is a standing liability. Promote it only when all four hold:
  - release phases already exist;
  - few items customers were told to expect slipped last year (question 4);
  - buyers plan budgets or migrations around your dates (question 3);
  - finance has reviewed revenue-recognition exposure, because a dated, named feature published to every customer is what ASC 606 (IFRS 15 outside US GAAP) reviews look for.
- **Deleted, not demoted: every public posture when the trigger is sales promises and leadership will not sign the citation rule** (question 6). Publishing without the rule hands reps a larger catalogue to promise from. Fix sales governance first with no public page; re-promote once the rule is signed.

Re-rank against the interview, and say which answer moved which rung:

- A hard deadline with few owner hours promotes the direction page.
- Regulated enterprise buyers promote customer briefings alongside the public page; bundling two rungs is allowed.
- An open-core company with public issues already promotes the horizon roadmap: the job becomes curating what exists, not deciding whether to publish.
- An existing preview program, a low slip rate and finance sign-off promote dated quarters.
- An existing, triaged community board promotes the interactive board.

## 3. Fix the commitment vocabulary

Pick one vocabulary and define, on the page, what a customer may rely on in each state. Three families, in rising commitment strength:

1. **Horizon buckets:** Researching / We're Working On It / Coming Soon / Just Shipped (AWS containers), or Now / Next / Later (Janna Bastow, ProdPad). Credit Now-Next-Later to Bastow, not to _Product Roadmaps Relaunched_. AWS glosses Coming Soon as "a couple of months out, give or take"; define your buckets by engineering state instead (for example "in build, named owner"), so no bucket smuggles in a date.
2. **Release phases:** exploring, in design, private preview (invite-only), public preview, GA (GitHub, Stripe, Microsoft 365). A phase says what customers may rely on, not when.
3. **Quarters or estimated dates:** only with a phase attached.

Rules (this skill's recommendations, not industry norms; GitHub, for one, dates in-design items by quarter column):

- **Cap every date with a phase.** "Q1 - private preview" promises an invite-only preview in Q1; a bare "Q1" reads as general availability to every buyer and every rep.
- **Date only what has entered private preview or later,** so the phase already caps the promise.
- **Publish a visible negative state:** `not planned` or `cancelled`, with a reason, kept visible for at least one review cycle. Most roadmaps silently drop items, which is the slip anti-pattern in step 8.
- **Separate community proposals from vendor plans** with their own label (AWS containers' `Proposed`, copied by Heroku), so a popular request never reads as a plan.
- **Write items problem-first:** "Rotate API keys without downtime", not "Key rotation v2". Teams can then change the solution without breaking the promise.
- **Map informal flags explicitly.** An undefined "beta" becomes private preview only once access rules are written; until then show it as a note on the item, not a phase.

## 4. Gate what goes public

The public roadmap is never the internal one minus a few rows. Run every candidate item through this gate, and mark only passing items as public in the internal tool:

- **Security fixes and hardening:** publication tells attackers where the gap is. AWS does not list every platform security update.
- **Deprecations and breaking changes not yet announced** through the versioning process. Once announced, link the notice from the item.
- **Pricing, packaging, company financials,** and items that would cannibalize a current plan (Osborne effect).
- **Partner integrations, third-party names and M&A before announcement.** Name the capability ("export usage data to your warehouse"), not the vendor, until the partner announces too.
- **Competitive bets and surprise launches:** AWS and Docker both reserve the right to ship unannounced work.
- **Customer-specific commitments:** these belong in that customer's order form, under legal review.
- **Internal plumbing:** refactors, infrastructure, bug backlog.

Record the gate in the policy, with who decides edge cases, so the next editor applies it without re-arguing each row. The same gate applies to NDA briefings.

## 5. Set the legal and sales guardrails

Route final wording to counsel: this skill sets the shape, not legal advice. Protection comes in layers, and each covers less than teams assume:

1. **Page disclaimer:** informational only, not a commitment, subject to change, not to be relied on for purchasing decisions (Atlassian's phrasing carries all four).
2. **Forward-looking statements:** listed companies add securities safe-harbor language (Salesforce). Private companies borrow only the customer sentence: purchase decisions should rest on features available today. Route investor-facing reuse of roadmap material (data rooms, fundraising decks) to counsel.
3. **Contract clause:** the MSA states purchases are not contingent on future functionality, including public statements (Salesforce's MSA; widely copied).
   - It reduces reliance claims from contracted customers.
   - It does not cover self-serve accounts unless the click-through terms carry an equivalent, and in many jurisdictions it cannot exclude misrepresentation or deceptive-advertising claims.
   - The page's own accuracy stays the residual exposure: never publish an item known to be off.

The override that defeats all three: a feature written into an order form, SOW or side letter is a binding deliverable whatever the disclaimer says. Before launch, inventory every existing contract that names a roadmap item; counsel and finance review each, and the account owner contacts the customer.

If the clause is missing, counsel decides whether to add it to new and renewing contracts and to the self-serve terms, and signs off in writing on the residual risk for existing contracts. Dated promises also carry revenue-recognition risk:

- Finance, then auditors, review roadmap communications, feature descriptions and release dates for a customer's "valid expectation of specified upgrades" (ASC 606; IFRS 15 equivalent).
- A specified upgrade can become a separate performance obligation and defer revenue.
- Undated, unspecified updates usually create no such obligation; dated, specified ones may. Bring finance in whenever a dated commitment reaches any customer.

Citation rules, signed by the sales leader and the CEO, covering anyone customer-facing (reps, solutions engineers, customer success, DevRel, executives on stage):

- Cite only the public roadmap, at the commitment level printed on it.
- Deeper previews go through a formal channel with product present: NDA briefing or private-preview enrollment.
- No dates in emails, proposals, decks or keynotes unless the public page shows that date. Listed companies run roadmap statements through the same disclosure review as other public statements.
- Legal and finance approve any roadmap item written into an order form.
- A deal that depends on an unbuilt feature goes to product for a decision, never to a rep's judgment.

For the disclaimer and clause shapes, the NDA-briefing rules and a sales one-pager outline, read [references/legal-and-sales-guardrails.md](references/legal-and-sales-guardrails.md).

## 6. Decide the feedback surface

Three launch options, ranked:

- effort: `separate board > reactions on items > locked items`
- value: `separate board > reactions on items > locked items`
- efficiency: `locked items > reactions on items > separate board`

- **Default: locked items, debate elsewhere** (GitHub). Roadmap items are read-only; each links to one feedback channel. Cheapest, and it keeps the roadmap a statement of plans.
- **Reactions and comments on items** (AWS containers): signal attached to plans, moderate triage cost.
- **Separate voting board (starved):** most signal, highest expectation debt. Promote it only when a named triage owner and the feedback loop exist.

When a board runs:

- Treat vote counts as one weighted signal, never the ranking. Canny concedes a hundred votes can all come from free users; weight by segment and account value.
- Give it a triage owner and a `not planned` state with reasons.
- Freeze a board nobody triages: read-only behind a dated notice pointing to the single feedback channel. It is the honest state between keeping and closing.
- Plan the exit before the launch. Microsoft moved off UserVoice product by product, and the Office 365 forum closed without notice, its requests no longer accessible: expectation debt written off. Closing needs a dated notice and a migration or read-only archive of open requests.

The untriaged backlog itself goes to the feedback loop; it does not gate the roadmap launch.

## 7. Wire the lifecycle: owner, cadence, subscriptions, changelog close

A stale public roadmap is worse than none: it publishes promises nobody keeps. PostHog's own staff called its roadmap page "a wishlist which, to my knowledge, nobody maintains".

- **Name one owner** and a backup, with the hours from question 8. Not "product" collectively.
- **Set a review cadence** (monthly is common) and touch every item at each review: confirm, move, or mark `not planned`. Publish only after at least two internal review cycles have produced decided statuses; a roadmap published before decisions exist is a list of hopes.
- **Give every item a stable ID** that survives from exploring to GA, and a subscription channel (watch, feed or email digest) so step 8 can notify anyone.
- **Pick a surface** that supports stable IDs, per-item subscriptions and comment locking: a repository project board, a portal page, or a roadmap tool. Placement in the portal belongs to `samber/developer-platform-skills@developer-portal-design`.
- **Close every shipped item with a changelog link.** GitHub applies a `shipped` label and closes the issue with a comment linking the changelog post.
- **Link deprecation notices both ways** once announced.
- **Snapshot the page at each review,** so anyone can audit what was promised and what shipped.

## 8. Write the slipped-item playbook

Every roadmap slips; the playbook decides whether the slip costs trust or builds it. "Committed" here means any item a customer was told to expect: written into a contract, shown in a deck, or carrying a date or GA phase on the page. Write the playbook into the policy before launch:

1. Change the status on the item itself: `delayed`, `descoped` or `not planned`. Never delete it.
2. Give a one-paragraph reason in plain language.
3. Offer a workaround or alternative.
4. Notify subscribers, reactors, and every account the briefing log shows saw the item.
5. Customers with a contractual commitment hear privately from the account owner, days before the public update. Legal checks the notice against the order-form terms first: a slip may trigger notice, credit or termination rights.
6. Keep cancelled items visible for at least one review cycle.

Apply the same steps to commitments that predate the page; they become a launch precondition.

Never delete, quietly demote or bulk-reset a slipped item, and never let contract-dependent customers learn of a slip in public.For a format change (new posture, new vocabulary), copy Microsoft's Dynamics 365 move to a continuous roadmap: a dated transition table plus an explicit "what's not changing" section.

Read [references/roadmap-policy-template.md](references/roadmap-policy-template.md) when drafting: item, slip-notice and format-change templates, plus the rationalization table of shortcuts teams reach for under pressure and why each fails.

## 9. Brainstorm candidates, then draft and validate

Do not jump from the interview to a finished policy.

1. Present 2-3 candidate policies as coherent bundles (posture + vocabulary + feedback surface + guardrails), each with trade-offs and one recommendation with its reason. List an ineligible candidate the user asked for (often "like Stripe") with the conditions that would make it eligible. Typical split, hybrids of two rungs allowed:
   - a GitHub-shaped read-only phase roadmap with debate in a forum;
   - a GitLab-shaped direction page plus NDA customer briefings;
   - a Stripe-shaped dated roadmap, only if step 2's four promotion conditions hold.
2. On the user's pick, draft the policy from the template, one section at a time. Validate every template section with the user before writing the next.
3. Gate publication on explicit approval by product, sales leadership, counsel and, where dates appear, finance.

Expected output: the candidate bundles with a recommendation, then the policy document from [references/roadmap-policy-template.md](references/roadmap-policy-template.md), plus a launch checklist of preconditions (signed citation rule, contract inventory, pre-page slips handled).

## Measurement

No outcome metric for a public roadmap has independent evidence, so measure the practice's integrity and the problem it was meant to fix:

- **Freshness:** share of items touched at each review. Target 100%; any item untouched for two cycles gets a decision.
- **Silent removals:** items that vanished without a `not planned` or `delayed` state. Target zero.
- **Slip rate:** committed items that moved, using step 8's definition. Track it before promoting to dated quarters.
- **Close rate:** shipped items closed with a changelog link. Target 100%.
- **Sales incidents** (trigger: sales promises): roadmap items in new order forms or side letters, and roadmap escalations. Baseline before launch, compare each quarter.
- **"When will X ship" volume** (trigger: customers asking): support tickets and sales questions about upcoming features, before and after launch.

## Invocation examples

- "Our sales team keeps promising features from the internal roadmap. The CEO wants a public roadmap. How should we do it?"
- "Should our API platform publish a roadmap on GitHub like AWS does, and should we let people vote?"
- "We said webhooks v2 would ship in Q3 on our public roadmap and it's slipping to Q1. How do we tell people?"

## References

- [references/roadmap-case-studies.md](references/roadmap-case-studies.md) - read when choosing a posture or vocabulary: GitHub, AWS containers, Docker, Heroku, Terraform AWS provider, Stripe, Microsoft 365, Atlassian, GitLab, PostHog, and the platforms that publish none.
- `samber/developer-platform-skills@api-status-communication` - incident and maintenance communication; a roadmap slip is not an incident and never goes on the status page.
- `samber/developer-platform-skills@integration-partnership-strategy` - joint roadmaps with a technology partner are governed there, not on the public page.
- `samber/developer-relations-skills@build-in-public` - a maintainer's devlog or open-startup updates that mention what's next; the Osborne-effect boundary there matches step 1 here.
