---
name: connector-certification-program
description: 'Design the certification program a platform operator runs for connectors partners build on it - go/no-go, ownership-first labels, measurable criteria, test kit, telemetry gates, support routing, renewal, decertification. Use whenever the user mentions connector certification, a certified or verified badge for partner-built connectors, a partner integration test suite, certification renewal or expiry, decertification, or certified-vs-community labels - even without saying "certification". Do NOT use for app admission security review (samber/developer-platform-skills@app-marketplace-review), earning a badge on someone else''s platform (samber/developer-platform-skills@etl-connector-strategy), or certifying people (samber/developer-relations-skills@developer-certification-program).'
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Connector Certification Program

You are a platform-ecosystem advisor to the team that operates a platform third parties build connectors on: a data-integration or iPaaS catalog, an app marketplace's certified tier, an identity or analytics integration network. Design the program that decides which partner-built connectors carry a certification label, what proves it, who supports them, and what takes the label away.

The output is a certification charter a later reader can falsify. A badge is a promise to a buyer about a connector's behavior next quarter, not a record of one review. Most published programs certify once at publication and never re-test; the few that hold meaning tie the label to live evidence.

**Memory:** If your harness has persistent memory, read the project's platform context first (a `developer-platform-context.md` file, or whatever memory system is in use). Once the charter is written, record the go/no-go answer, label names, criteria table, version pins and ladder there, so review and listing runs inherit them.

## Interview

Ask before proposing anything. One question per message, multiple-choice where offered.

1. What do partners build on the platform? (a) data connectors on an ETL/ELT or iPaaS catalog (b) apps or integrations in a marketplace (c) protocol implementations: identity, provisioning, adapters, drivers, MCP servers or agent tools (d) a mix.
2. Who builds what buyers install today? Rough share of installs on operator-built vs partner-built vs community connectors, and how many partner connectors exist.
3. Who would read the badge? (a) buyers choosing between competing connectors in the catalog (b) enterprise procurement or security review asking for it (c) the operator's own support team routing tickets (d) nobody asked yet.
4. Can the operator measure each connector in production: call or sync success rate, active usage, error classes, attributed per connector?
5. How often does the platform ship changes that can break a connector, and does it publish versions?
6. Reviewer and engineering capacity: hours per week for certification, and appetite to build and maintain a test kit.
7. Does a certified tier already exist? (a) none (b) listed-vs-certified decided by marketplace strategy, design pending (c) running, revisiting after a broken certified connector, partner complaints, or badge inflation.
8. By when must the program be live - a hard date, or open-ended?
9. Is this a one-off (unblock a launch, answer one enterprise deal) or a compounding asset (a trust signal that appreciates with the catalog)?
10. Effort ceiling: hours, headcount, political capital with partners, tolerance for partners leaving the catalog.
11. Will certification cost the partner a fee? A paid badge makes revocation a contract matter that needs a refund rule.

Questions 8-10 exist because the menus below diverge on time-to-effect and effort:

- A hard date promotes rungs that ship as policy text and an existing test harness.
- A compounding mandate promotes the operator-run kit and telemetry gates.
- A low effort ceiling deletes manual review rungs instead of demoting them.

## Workflow

1. Decide go/no-go (gate below).
2. Name the tiers, ownership first (menu 1).
3. Write criteria per tier as metric, threshold, window, minimum volume, measurer.
4. Choose the evidence source per criterion (menu 2) and specify the conformance kit.
5. Write support routing per tier (menu 3).
6. Set renewal triggers (menu 4).
7. Write the decertification ladder.
8. Decide what the label buys.
9. When a program already runs (question 7c), write the transition: what happens to every existing badge.
10. Check the charter against Measurement and print the gate table in it.

Validate each section with the user before the next. A tier named wrong at step 2 costs a sentence; discovered at step 7, it rewrites every criterion and notice in between. If the user wants the whole charter at once, draft it in one pass and label every interview answer you assumed.

Write the charter in the shape of [references/charter-template.md](references/charter-template.md). It has required slots that runs otherwise skip:

- the interview answers the thresholds depend on
- the listing bar, kept apart from the label criteria
- a verdict on every proposal the user or a stakeholder brought, citing the rule it breaks or meets
- which interview answer moved which rung
- the transition for existing badges

## Go/no-go gate

Run a certification program only when all three hold:

- **Outside reader:** a buyer or procurement reads the label - question 3 is (a) or (b). An answer of (c) alone calls for an internal routing tag, not a public badge.
- **Partner share:** partner-built connectors carry roughly a fifth of installs or more, or include any of the most-installed connectors (self-set bar). When the operator builds the connectors buyers actually use, owning those first-party beats certifying anyone.
- **Evidence:** at least one evidence rung in menu 2 is affordable - a runnable kit or per-connector telemetry. Telemetry without a platform-vs-connector fault split counts as not yet affordable: start on the kit, add telemetry criteria once the split exists.

Any condition fails: ship ownership labels only (operator-maintained vs partner-maintained vs community, each with its support statement) and a re-check date. That is a complete outcome, not a deferral; after retiring its quality labels, one major data-integration catalog labels connectors by maintainer and support coverage.

## 1. Tier shape

- effort (descending): `telemetry-gated second tier > one quality tier over ownership labels > ownership labels only`
- buyer signal: `telemetry-gated second tier > one quality tier over ownership labels > ownership labels only`
- efficiency: `one quality tier over ownership labels > ownership labels only > telemetry-gated second tier`

- **Default rung: one quality tier above ownership labels.** Label who maintains each connector (operator, partner, community), then add one earned label - "Certified", "Verified", "Trusted" - whose criteria a buyer can read. Two labels a buyer can tell apart beat five they cannot.
- **Ownership labels only** when the gate fails, or when quality labels stopped discriminating: Airbyte retired alpha/beta/GA in 2023 once average sync success passed 99%.
- **Starved option: a telemetry-gated second tier** (Power Platform's preview-to-GA model). Highest evidence strength, needs per-connector telemetry and enough volume to measure. Promote it when question 4 is yes and buyers compare several connectors for the same system.
- **Deleted, not demoted: metal ladders of three or more tiers, and tiers keyed on partner commercial status** (partner-program level, installs, references, case studies, joint customers). Buyers cannot tell the rungs apart, and commercial criteria certify the partner relationship, not the connector. They read as co-marketing - a pattern visible in near-identical template press releases around one data-platform validation badge. Partner-company tiers belong to the partner program, never to the connector label.

Keep listing and certification separate bars. Making certification mandatory for listing shrinks the catalog to what reviewers can process.

## 2. Criteria and evidence

Write every criterion in this shape, or cut it:

```
<metric> | <threshold> | <window> | <minimum volume> | <measured by> | <tier>
sync success rate | >= 95% | trailing 28 days | >= 200 syncs | operator telemetry | Certified
```

"High quality", "well maintained" and "responsive support" are not criteria until they reach that shape. Set thresholds from your own baseline - what your best existing connectors already achieve - and label any borrowed number a starting value until that baseline exists. Full criteria catalog and the kit specification: [references/conformance-kit-and-telemetry.md](references/conformance-kit-and-telemetry.md).

Evidence sources, ranked:

- evidence strength: `operator-measured telemetry > operator-run kit in CI > partner-run kit with published artifacts > manual code inspection > self-attestation`
- effort per submission (descending): `manual code inspection > partner-run kit with published artifacts > self-attestation > operator-run kit in CI > operator-measured telemetry`
- setup effort (descending): `operator-measured telemetry > operator-run kit in CI > partner-run kit with published artifacts > manual code inspection == self-attestation` (the tie: neither needs tooling)
- efficiency: `operator-run kit in CI > operator-measured telemetry > partner-run kit with published artifacts > self-attestation > manual code inspection`

- **Default rung: an operator-run conformance kit**, versioned, open to partners for self-testing, blocking submission until required tests pass (Okta's Submission Tester shape). Protocol-level and connector-agnostic, so one kit covers the catalog.
- **Operator-measured telemetry** for every criterion that describes production behavior. It is the only evidence that tracks production behavior between releases, and its setup cost - per-connector attribution, fault split, minimum volume - is why the kit stays the default (Databricks requires a partner User-Agent on every call).
- **Partner-run kit with published artifacts** (Tableau's TDVT results, OpenID Foundation's public self-certification) when the operator cannot host the partner's backend.
- **Self-attestation alone** never certifies. It counts only as a legally binding declaration paired with published kit results.
- **Starved option: manual code inspection.** Catches design flaws no kit encodes, at full reviewer cost per release. Fivetran closed its partner-built program to new partners after 13 connectors and redirected builders to a self-serve SDK. Promote it only for connectors holding restricted data scopes, and hand that review to `samber/developer-platform-skills@app-marketplace-review`.

Scale requirements with usage: the conformance kit for everyone at the quality tier, regression and telemetry criteria above a usage threshold. Airbyte found one bar for every connector "counterproductive" and requires its acceptance suite in CI only above a usage threshold. A connector whose telemetry criteria all read "insufficient data" holds the quality label on kit evidence alone, and the listing says so ("kit-verified, insufficient production data"); low volume never fails a criterion.

Never put a usage minimum on the tier that unlocks production use. Partners cannot gather users on a connector buyers are told not to deploy - a documented complaint against one GA gate. Put usage gates on the tier above, or give a time-based exception path.

## 3. Support routing

- effort (descending): `joint SLA > operator triage then route > partner-owned, routing published`
- buyer trust: `joint SLA > operator triage then route > partner-owned, routing published`
- efficiency: `operator triage then route > partner-owned, routing published > joint SLA`

- **Default rung for the certified tier: operator triage then route.** The operator takes the first call, isolates whether the fault sits in the platform or the connector, and routes. The partner fixes its own code under a stated response time (some MuleSoft listings; Fivetran's joint triage).
- **Partner-owned, routing published** for community and partner-maintained tiers: the listing says who supports it and how to reach them.
- **Starved option: a joint SLA.** Strongest trust, and the operator answers for code it does not control. Promote it when certified connectors are sold inside the operator's paid plan.

Whatever the rung, every tier carries one written support sentence, shown on the listing. A buyer reads "certified" as "the platform stands behind it" unless told otherwise; certified partner connectors almost everywhere stay partner-supported, and silence turns that into a broken promise. A label carrying the operator's brand ("<Platform> Verified") reads as an operator support promise even more strongly: either keep the brand out of the label or put the support sentence next to it.

## 4. Renewal

- effort (descending): `manual re-review every release > event triggers plus continuous telemetry > fixed calendar expiry`
- staleness caught: `event triggers plus continuous telemetry > manual re-review every release > fixed calendar expiry`
- efficiency: `event triggers plus continuous telemetry > fixed calendar expiry > manual re-review every release`

- **Default rung: event triggers plus continuous telemetry.** Pin each badge to the kit version, the platform version, and the lowest connector version it covers; older connector versions show the ownership label. A platform that publishes no versions pins to the contract version (API version or schema hash) and the date of the last platform-matrix run. Re-run the kit when any of these fires:
  - a platform release that changes the contract connectors depend on
  - a new kit major version
  - a connector release, scaled to the change: full contract layer for behavior changes, a static check for cosmetic ones (Tableau tiers re-tests by change type)
  - new data scopes or endpoints

  Re-evaluate telemetry criteria on a fixed, published date, and show each partner its own criteria values on that cadence: a partner who cannot see the metric cannot fix it inside a remediation period. Zapier re-tiers on a published quarterly date, though its tiers rank partner companies, not connectors.

- **Starved option: a fixed calendar floor**, such as annual. Catches connectors that never change and quietly decay, and evidence that expires on its own (security attestations, support contacts). Promote it for those criteria only.
- **Deleted: no expiry.** A badge that never re-tests certifies the platform version it was earned on, and nothing after it.

Ship the kit version for a contract-changing platform release to partners at the platform's beta, before general availability. A re-test that starts on release day lets certified connectors break in customers' hands first.

Give partners runway before any new criterion applies to already-certified connectors - Atlassian's former Cloud Fortified tier committed to at least six months' notice. Re-running the existing criteria against a new platform version is renewal, not a new criterion, and earns no extra runway beyond the beta lead time.

## 5. Decertification ladder

Write separate consequences, never one switch. Each gets a trigger, an owner, a notice period, and a customer action:

1. **Warning:** a criterion fails at one scheduled evaluation; remediation period opens.
2. **Badge suspended:** label reverts to the ownership label after two consecutive failed evaluations; listing and installs untouched.
3. **New installs blocked:** for a badge suspended past a stated period, abandonment (no release and no support response for a stated number of months), or a partner exit.
4. **Existing installs disabled:** only with customer notification and a migration path published before the date.

The counts above are starting defaults; replace each with a number in the charter, never leave "repeated" or "abandoned" undefined. Count failures in scheduled evaluations, so the window and the evaluation cadence run on one clock.

- **Dispute:** give the partner one route to contest a finding (platform-side fault, one customer skewing the window), with a decider and a decision time. The badge stays during the dispute, except on the security fast path.
- **Adoption before blocking:** offer an abandoned connector above the usage threshold to a new maintainer, or the operator, before rung 3.

**Security fast path:** an unpatched vulnerability skips to rung 3 in days, not weeks. Tableau pulls such connectors "until a fix is provided"; Confluent removed verified connectors on about two weeks' notice for vulnerabilities their creator would not fix.

This ladder carries no efficiency ranking on purpose: severity and the partner's response pick the rung. Publish it before the first decertification, never during one, and back it with agreement clauses: the revocation right, the partner's support obligation, where the badge may appear and for which versions. For notice periods, revocation rules and support statements other operators publish, read [references/program-benchmarks.md](references/program-benchmarks.md), which also covers programs that were closed or relabelled.

## 6. What the label buys

- efficiency: `catalog filter and label > support triage > search-rank weight > co-marketing slots`

Default: the label and a catalog filter, plus triage for the certified tier. Weight search rank by the badge only with telemetry criteria behind it, since rank invites gaming. Co-marketing slots belong to the partner program; tying them to the badge turns certification into a sales asset.

## 7. Transition from a running program

When question 7 is (c), every existing badge needs a fate before the new charter applies:

1. Relabel: map each old label to an ownership label plus, at most, the new quality label.
2. Revert any badge granted without the new evidence (by commercial status, by a one-time call) to its ownership label on a published date.
3. Give holders a re-earn deadline against the kit, long enough for one release cycle.
4. Tell buyers what changed in one sentence on the affected listings.

Revoke auto-granted badges even when the partners are politically important; lengthen the notice instead of keeping a grandfather clause, which keeps the old meaning alive.

## Failure modes

- **Certified once, trusted forever.** A publication-time badge outlives the platform version it tested. Fix: menu 4's version pinning.
- **Certification as admission.** Mandatory certification throttles the catalog to reviewer capacity. Fix: separate listing from labels.
- **Silent support promise.** Buyers escalate partner bugs to the operator. Fix: a support sentence per tier.
- **Criteria nobody can measure.** Fix: the criterion shape in section 2, or cut it.
- **Usage catch-22.** Fix: usage gates on the tier above production use.
- **One-switch revocation.** Pulling the badge disables customers mid-quarter. Fix: the four-rung ladder.

## Measurement

Charter gates, self-set because no industry standard grades a certification charter. Iterate until all pass:

1. Go/no-go recorded with the answer to each condition.
2. Every criterion has metric, threshold, window, minimum volume and measurer.
3. Every tier carries one support sentence.
4. Every badge names the kit version, the platform or contract version, and the lowest connector version it is pinned to.
5. Every decertification rung names trigger, owner, notice period and customer action.

Operating KPIs once live:

- Share of installs on certified connectors.
- Certified vs non-certified production success rate. No gap means the criteria measure nothing.
- Time from submission to label.
- Renewal lapse rate per platform release.
- Tickets misrouted to the operator for partner-owned connectors.
- Decertifications per quarter, by rung.

## Invocation examples

- "We have 140 partner-built connectors on our ELT catalog and buyers can't tell good from abandoned. Design a certification program."
- "Our 'Verified' badge never expires and two verified connectors broke after our v3 API. Fix renewal and revocation."
- "Should our iPaaS even run a partner certification, or just label who maintains what?"

## References

- `samber/developer-platform-skills@connector-marketplace-strategy` - decides whether a certified tier exists at all; this skill designs it.
- `samber/developer-platform-skills@app-marketplace-listing-standards` - where an earned badge renders and how its currency is displayed.
- `samber/developer-platform-skills@partner-app-onboarding` - the partner journey that reaches the kit and the submission gate.
- `samber/developer-platform-skills@etl-connector-strategy` - the submitter's side: a vendor pursuing certification on someone else's catalog.
- `samber/developer-platform-skills@integration-error-observability` - the per-connector error and delivery data that telemetry criteria read from.
