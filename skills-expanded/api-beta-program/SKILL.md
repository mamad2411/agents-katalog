---
name: api-beta-program
description: >-
  Runs an early-access, preview, beta or design-partner program for a new API feature: program
  shape, what each pre-GA label guarantees (SLA, support, breaking-change notice, pricing, data
  terms), stage on the wire, partner selection, per-account access, feedback cadence, exit to GA
  or kill, and rescuing betas that never ended. Use whenever the user mentions an API beta or
  preview program, design partners, beta labels or allowlists, production traffic on their own
  beta endpoint, or when to go GA - even if they only say "let a few customers try the new
  endpoint before it's final". Not for whole-app beta testing, a vendor's beta you consume, or
  canary rollouts of a GA change. Do NOT use for the stable version lifecycle - use
  samber/developer-platform-skills@api-versioning-policy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# API Beta Program

You are a developer-platform product lead. A beta label is a contract with fewer guarantees, and every integrator who builds on it holds you to whatever you never wrote down. This skill sets the program shape, writes what each pre-GA stage promises, wires the stage into the API, runs the cohort, and ends the program on a date with one of three outcomes: GA, extension or kill.

Boundaries:

- The stable lifecycle (version scheme, GA deprecation windows, sunset headers) belongs to `samber/developer-platform-skills@api-versioning-policy`. This skill owns everything before GA, including retiring one preview version for the next, and hands over at GA.
- Routine feedback intake and closing the loop with requesters belong to `samber/developer-relations-skills@developer-feedback-loop`. This skill owns only the cohort's feedback cadence.
- Whether a stage appears on the public roadmap belongs to `samber/developer-platform-skills@public-roadmap-strategy`, which reuses the stage contract written here.
- Percentage or canary rollouts of a change that is already GA, and launch marketing, are out of scope.

**Memory (advised):** store the stage contract, the cohort list and the exit date in `developer-platform-context.md` when memory lives in a file; otherwise use the harness memory. The next feature's beta then reuses the contract instead of re-deriving it.

## Interview

Ask one question per message, multiple-choice where offered, in this order. Skip any question the user's files already answer.

1. **What enters beta?** A new field or endpoint on an existing resource / a new resource family / a new protocol surface (webhooks, GraphQL, streaming) / a paid capability. Is the request and response shape decided, or still open? Is it billable?
2. **Existing labels:** does the company already use preview, beta, alpha or early-access labels anywhere (docs, console, SDKs, contracts, roadmap)? Where are they defined, and how long has the oldest been live?
3. **Why a beta:** specific customers waiting / a sales deal needs it / the team is unsure of the shape / load or cost unknowns / leadership wants a launch moment.
4. **Capacity:** engineer and product hours per week for partners, and who owns the program by name.
5. **Data and contracts:** will beta traffic carry personal or regulated data? Do enterprise contracts promise SLA, DPA or certification coverage on "all services"?
6. **Clock and horizon:** GA target date, effort ceiling, and whether this program is a one-off or the template for every future beta.
7. **Release machinery:** how versions surface today (path, header, date), whether SDKs have a pre-release channel, whether a changelog exists.

Question 6 exists because the shapes in step 1 diverge sharply on time to signal and effort. Question 5 exists because a missing DPA carve-out costs more than a missing SLA.

## Workflow

Present the recommended shape and one alternative before writing anything, then draft the program charter one section at a time, validating each with the user before the next. Steps 1-5 must be written and signed off before the first account enrolls.

1. Choose the program shape.
2. Write the stage contract.
3. Put the stage on the wire.
4. Set exit criteria.
5. Select the cohort and pass the enrollment gate.
6. Enable access per account.
7. Run the feedback cadence.
8. Apply change rules during the beta.
9. Decide and communicate the outcome.

When question 6 says "template for every beta", write step 2 as the company-wide contract before any feature-specific work.

Read [references/stage-contract-and-charter-template.md](references/stage-contract-and-charter-template.md) when drafting: contract and charter templates, enrollment record, backward timeline, launch checklist, sign-off block and the existing-beta inventory.

## Existing-beta rescue

Run this first when question 2 finds a stage already live with no exit date, often for years, with production callers:

1. Inventory each beta surface: first shipped, last shape change, callers over the last 90 days, accounts with production traffic, owner.
2. Publish a retroactive stage contract (step 2) and grandfather every production caller: nothing they call changes until their surface has a decision.
3. Decide per surface, each with an owner and date:
   - **GA as-is** when the shape has been stable for a long time, production callers exist, and `samber/developer-platform-skills@public-api-design-review` passes at GA level with zero Must-change findings: relabel, then hand to `api-versioning-policy`.
   - **Next version with migration** when the shape needs breaking fixes or the review finds any Must-change: run steps 1-9 for the new version.
   - **Kill** when usage is near zero: step 9 kill terms.
4. Tell production callers privately before any public relabel or notice.
5. Retire the old label publicly once every surface has a decision.

## 1. Choose the program shape

Pre-check first: an additive field or endpoint following an existing pattern skips the beta and ships GA under the versioning policy. A beta there adds a label nobody needs.

Otherwise, three shapes. Effort and value rise together; efficiency separates them. Say the ranking out loud:

- effort: `design partners > private preview > public preview`
- value (evidence about the shape before it freezes): `design partners > private preview > public preview`
- compliance cost: `design partners == private preview > public preview` - the tie holds because both need signed pre-GA terms per account; public preview runs on click-through terms.
- efficiency: `private preview > design partners > public preview`
- The hybrid below sits between private preview and design partners on effort and value, with the same compliance cost as both.

| Shape | What it is | Typical size |
|---|---|---|
| Private preview (default) | Built feature, invite-only cohort, allowlisted accounts, signed pre-GA terms | about 5-20 accounts |
| Design partners (highest value, highest effort) | Shape still open; partners co-design against prototypes on a fixed cadence | 3-5 for one API surface |
| Public preview | Self-serve opt-in, no SLA, notice rules published | anyone eligible |

- **Default: private preview.** It buys real-integration evidence from accounts you chose, at a support load you control.
- **Design partners lose every efficiency round** because value and effort are both highest. Promote them when question 1 says the shape is still open or the feature introduces a new resource model: a frozen wrong shape costs a version bump later.
- **Hybrid allowed:** a private preview whose first sessions run design-partner style on the one open question. Use it when the shape is mostly decided and the clock is short.
- **Public preview** follows a private preview, never replaces it, unless the change is low-risk and needs volume (load, pricing, long-tail use cases).
- **Ruled out: any shape with no owner** (question 4 empty). An ownerless beta becomes a perpetual one. Name the owner first.

Re-rank against the interview and say which answer moved which rung:

- A GA date closer than build time plus 8-12 weeks of partner sessions promotes private preview or the hybrid over design partners.
- "The team is unsure of the shape" promotes design partners to rung 1.
- "A sales deal needs it" changes nothing by itself: the deal account enters only if it passes step 5.

## 2. Write the stage contract

Use at most two pre-GA stages: private and public preview, the vocabulary most vendors converged on. A third, faster-breaking lane earns its place only for a domain that changes faster than your preview cadence.

Existing labels from question 2: map each defined label to a stage. Retire an undefined label (a docs badge nobody wrote terms for) and decide its endpoints in the existing-beta rescue; never adopt it as a stage, since its callers assume promises nobody made.

For every stage, fill each row. An empty row is a promise you will be held to anyway:

| Row | Decide |
|---|---|
| Access | Invite, waitlist, self-opt-in, plan gate |
| Availability | SLA or explicitly none; status-page coverage |
| Support | Channel and response expectation; who answers |
| Breaking changes | Allowed or not; notice before a change ships |
| Removal | Notice before the surface or the whole feature goes away |
| Production use | Unsupported, or permitted per account under a signed production exception |
| Pricing | Free, discounted or billed now; when GA pricing gets announced |
| Data and compliance | Which DPA, certification, residency and indemnity terms do not apply; whether beta data carries into GA |
| Limits | Published rate and volume limits for the stage |
| Marking | How docs, SDKs, payloads and the console show the stage |
| Discontinuation | What happens to data and integrations if the feature is killed |

- **Data carve-out:** the default line is "do not send personal data through this preview". When the payload is personal or regulated data by nature (question 5), that line makes the beta unusable; offer test-mode or synthetic data by default, and live data only under a per-account addendum legal signs that extends named DPA terms to the preview.
- **Precedence:** pre-GA terms must say they override an MSA or DPA that promises coverage on "all services"; counsel signs the wording.
- **SLA:** offer one on public preview only when the shape is frozen and enterprise buyers need production pilots before GA; the stage then differs from GA in pricing and completeness only, and the contract says so. Internal SLO targets used in step 4 are not contractual promises; share them only labelled as non-contractual goals, never in the terms or the contract table.

Vendor wording for each row is in [references/vendor-stage-precedents.md](references/vendor-stage-precedents.md); read it when the user cites a vendor ("like Stripe").

## 3. Put the stage on the wire

A stage that lives only in docs gets called by GA code paths and copied into production. Pick one mechanism, matching the versioning scheme from question 7:

- **Version with a stability suffix** (`v1beta`, dated `-preview` or `.preview` versions): best fit for path or date versioning.
- **Separate base path or endpoint** (`/beta`): simplest, and the easiest for callers to leave in production. Pair it with production-use detection (step 6).
- **Opt-in header per request:** fine for one field; becomes a maintenance trap once dozens accumulate, and graduating it breaks old self-hosted or pinned clients that still send it.

Non-REST surfaces:

- **Webhooks and events:** opt in per subscription (a preview version on the endpoint object, or preview event types); mark the stage in every delivery's payload or headers.
- **GraphQL:** a separate preview schema or preview-marked fields that GA clients cannot select without opting in.
- **Streams and channels:** a preview channel or topic name.

Then mark it everywhere the caller looks:

- Ship SDK support in a pre-release channel or a separate module, plus in-language markers (experimental annotations, a `beta` sub-package), so GA users cannot use beta methods by accident. When the beta adds SDK methods or types and no pre-release channel exists (question 7), that blocks enrollment; partners integrating over raw HTTP may enroll, with the channel ready before public preview. `samber/developer-platform-skills@sdk-package-publishing` sets it up.
- Keep beta operations out of the GA API description (separate spec artifact or tagged operations) so GA reference docs and generated clients never include them.
- Label each operation and field in the reference docs, not only the overview page.

## 4. Set exit criteria

Write all three before the first account enrolls. An exit decided at the end is decided by whoever is loudest.

- **Time box:** a dated exit review, derived backward from the GA target when one exists. Google Cloud publishes an average Preview of about six months; treat anything past twelve months as a perpetual beta.
- **GA criteria** (all): a minimum number of accounts activated; at least one running production traffic on the final shape under a signed production exception, or production-shaped traffic (live keys, real volume) from several accounts; no open blocker; design re-review passed if the surface changed since enrollment; support, docs and SDKs ready; GA pricing set; internal SLO met for a sustained window.
- **Kill criteria** (any): activation below the floor at the review date; the problem statement disproved; cost to serve above what GA pricing can carry; a better route found.
- **Extension rule:** one extension, no longer than half the original time box (a self-set default: long enough to fix one failed criterion, short enough not to become a second program), with a new date and the failed criterion written down. A second extension is a deferred decision and gets named as one.
- **Freeze:** set a contract-freeze date at least one partner release cycle before the exit review, so the review judges the frozen shape and partners migrate onto it before GA.

## 5. Select the cohort and pass the enrollment gate

Pick the accounts you want as customers at GA, not the first rows of the waitlist. Entry criteria, all required:

1. Evidence of the exact problem the feature solves: a ticket, an issue, a workaround in their code.
2. A real integration planned inside the program window, not an evaluation.
3. A named technical owner who attends the cadence.
4. Signed pre-GA terms: feedback licence, confidentiality, no SLA, the stage contract by reference, the outcome options.
5. Intent to pay at GA when the feature is billable.

Shape the cohort:

- **Cap it from capacity,** not demand. Count sessions, async support, integration help and fixes: budget several hours per active partner per week after program overhead (changelog, flags, legal loop). Take the lower of that cap and the shape's typical size.
- **Same persona, different workflows,** so a pattern seen across partners is real and one partner's quirk shows as a quirk.
- **Fewer qualified accounts than the minimum:** recruit from support tickets and issues describing the problem before opening any waitlist; below three, run as design partners, say the evidence will be anecdotal, and widen recruitment before the mid-point check. Persistent lack of qualified demand is a kill signal.
- **Concentration:** in a preview of four or more accounts, no partner above about a third of beta traffic. With design partners, watch backlog share instead: one partner's asks filling the backlog is custom development.
- **Platform partners** that resell or embed your API need enablement for their downstream accounts, and kill notice reaches those accounts through the partner. Multiply their support and notice budget.
- **Sales-requested access** is decided by product against the criteria above. An account that fails rows 1-3 gets a substitute that keeps the deal moving without access: a design review under NDA, a sandbox with synthetic data, the GA and freeze dates, first place in the next wave. An override still requires every entry criterion plus the data addendum.

Enrollment gate, signed before the first account enrolls:

- Program owner: steps 1-4 written.
- Design review passed at beta level: `samber/developer-platform-skills@public-api-design-review` treats beta as its blocking gate.
- Security review of the beta surface: auth scopes, authorization checks, abuse limits.
- Legal: pre-GA terms, data carve-out or addendum, precedence clause.
- Support: channel staffed at the contract's response time.

Selection rubric, terms checklist, free-rider signals and the sales substitute reply are in [references/cohort-and-communication-playbook.md](references/cohort-and-communication-playbook.md).

## 6. Enable access per account

- **Key enablement on the account or organization,** never the user or a request percentage: a percentage rollout gives one integration different behaviour on consecutive calls.
- **Keep an enrollment record per account:** approver, date, stage, technical owner, terms version, production exception, planned exit date.
- **Give every beta flag an expiry that alerts the owner on the exit date** and never disables access by itself, so an unresolved beta surfaces as an alert instead of a forgotten flag or a mass outage.
- **Detect production use server-side:** live keys, sustained volume, calls from or deliveries to production hosts. Without a production exception, detection triggers a conversation and longer notice; with one, it counts toward the GA criterion. Never stay silent.
- **Never remove access by deleting the flag.** Graduation or kill follows step 9; an enrolled account must never meet a silent 404.
- Test mode for the beta, when one exists, follows `samber/developer-platform-skills@api-test-mode-design`.

## 7. Run the feedback cadence

| Shape | Cadence | Channel |
|---|---|---|
| Design partners | Weekly or biweekly 30-60 min session, agenda sent ahead | Shared private channel plus the session |
| Private preview | Kickoff call, then biweekly office hours and async | One private channel or forum category per beta |
| Public preview | Async only | Public forum category or discussion thread |

- **Name one owner and a response time** for the channel. A beta channel nobody answers teaches partners to stop reporting.
- **Run structured sessions:** what they built since last time, what blocked them, what they worked around, what they would pay for.
- **Treat one partner's request as a data point, not an order.** Ship a change only when it recurs across partners or matches the problem statement.
- **Measure activation, not signups:** define one activation event per account (first successful production-shaped call, first event processed by their system) before enrollment opens.
- Route anything outside this feature to `samber/developer-relations-skills@developer-feedback-loop`.

## 8. Apply change rules during the beta

Breaking changes stay allowed in a beta; silent ones do not. Freezing the beta like GA removes the reason it exists. Use the company's breaking-change definition from `api-versioning-policy`; never invent a beta-only one.

- **Private preview:** breaking changes allowed with direct notice to every enrolled technical owner before they ship. Notice length scales with observed production use.
- **Public preview:** publish your own notice rule and batch breaks into a new preview version rather than mutating the current one. Vendor practice runs from zero notice (Google Cloud pre-GA terms, AWS, Microsoft Graph) through a 90-day availability floor after a newer preview ships (Azure) to a recommended 180-day deprecation (Google AIP-185 beta channel); details in [references/vendor-stage-precedents.md](references/vendor-stage-precedents.md) § 4.
- **Every change gets a changelog entry,** including in private preview (a private changelog is fine). Generating those entries from spec diffs, with beta operations kept out of the public feed by stability level, is `samber/developer-platform-skills@api-changelog-automation`.
- **No changes after the freeze date** from step 4.

## 9. Decide and communicate the outcome

Hold the exit review on the date. Three outcomes, each told to enrolled accounts privately first, then the waitlist, then the public changelog:

- **GA:** publish the migration from the beta surface to the GA shape, or a relabel notice when the shape did not change. Keep the beta surface working through an overlap window of at least one partner release cycle; with production use on it, use the GA deprecation window from `api-versioning-policy`. Then hand the surface over.
- **Extension:** new date, the criterion that failed, and what changes in the extension.
- **Kill:** close new enrollment at once; notice of months, not weeks, once anyone runs production on it (the documented beta kill, Honeycode, gave about six months; twelve-month GA shutdowns are the ceiling, not the floor; see [references/vendor-stage-precedents.md](references/vendor-stage-precedents.md) § 6); data export; a named alternative; a banner on every entry point; a per-account list of the operations each one calls. Stop billing from the announcement unless a signed order form says otherwise, then credit it.

Message templates and the rationalization table (shortcuts teams reach for and why each fails) are in [references/cohort-and-communication-playbook.md](references/cohort-and-communication-playbook.md).

## Measurement

- **Activation:** activated accounts over enrolled. Set the floor yourself at launch; for cohorts under ten, state it as an absolute count.
- **Accounts with production traffic on the final shape** at the exit review.
- **Time in stage against the time box.** Any beta past its date without an extension record is a defect.
- **Silent changes:** breaking changes shipped without notice. Target zero.
- **Migration completion at GA:** enrolled accounts off the beta surface by the end of the overlap window. Target 100%.
- **Partner conversion** to paid or committed GA use, when the feature is billable.

## Invocation examples

- "We're adding a bulk export endpoint and want five customers on it before GA. How do we run that?"
- "Our `/beta` endpoints have been beta for two years and customers run production on them. How do we get out?"
- "Sales wants to give a prospect early access to the new webhooks API to close the deal."

## References

- `samber/developer-platform-skills@api-status-communication` - incidents on a beta surface go on the status page when the stage contract promises coverage.
