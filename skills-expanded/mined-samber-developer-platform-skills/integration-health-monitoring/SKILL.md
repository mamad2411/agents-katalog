---
name: integration-health-monitoring
description: "Find third-party integrations on your platform that will break on a known date - version drift, deprecated-endpoint usage, SDK end of life, expiring or dormant credentials - reach their owners, and decide when a deprecated surface is safe to turn off. Use whenever the user mentions version drift, who still calls a deprecated endpoint, partners on old API versions, chasing integrations before a sunset, brownouts, or retiring an API surface third parties call, even without saying \"integration health\". Not for migrating off another vendor's API. Do NOT use for live error dashboards (samber/developer-platform-skills@integration-error-observability), deprecation policy (samber/developer-platform-skills@api-versioning-policy) or key expiry design (samber/developer-platform-skills@api-auth-key-management)."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Integration Health Monitoring

You are finding the integrations that work today and will break on a date you already know - a sunset, an SDK end of life, a credential expiry, a payload-version retirement - and getting each one's owner to move first. The deliverable is a census that names every integration at risk and the person who can fix it, a notification loop that reaches that person, and a gate that says when it is safe to turn the old surface off.

Integrations failing right now belong to `samber/developer-platform-skills@integration-error-observability`. The deprecation policy itself - notice windows, headers, fall-forward or hard cutoff - belongs to `samber/developer-platform-skills@api-versioning-policy`. This skill executes that policy one integration at a time.

The recurring failure is counting calls instead of owners. A sunset at "99% of traffic migrated" still breaks every integration in the remaining 1%, and the providers who broke them could not say who they were or how to reach them.

## Interview

Ask before building anything. Batch them: this is an operational task, not a strategy interview.

1. What breaks, and when? List every dated change on the horizon: version sunsets, removed endpoints or fields, SDK end of life, auth-method removal, certificate or TLS changes, webhook payload-version retirement.
2. Is every request tagged with an integration identity - API key, OAuth client ID, app ID - at the gateway? What share of traffic carries none?
3. Who builds against you: customers' own engineers, partner apps installed across many customer accounts, or plugins and agencies whose end users never talk to you? (see "Who sits behind an integration")
4. What contact do you hold per integration, when was it last confirmed, and do you track bounces?
5. What is the longest business cycle an integration runs on? Monthly invoicing, quarterly reporting, year-end close and annual renewals all call once and go quiet.
6. Is the replacement surface stable and feature-complete for the migrating use cases? Escalation past a reminder is unfair while it is not.
7. Deadline, payoff and effort: is the date fixed by contract, security or cost, is this one sunset or a standing practice you will run for every future change, and what can you spend - engineering weeks, a partner team's hours, an account manager per top integration?

Question 7 moves every ranking below. A fixed date promotes whatever you can measure and send this month. A standing mandate promotes the attribution and contact work that every later sunset reuses.

Question 6 can block the ladder outright: brownouts and cutoffs against a replacement that cannot carry the workload break partners for your own defect.

If your harness has persistent memory, or the project keeps a `developer-platform-context.md`, store the break-date catalog, the attribution coverage figure, the lookback window, the readiness gate and the exception register there, so the next sunset starts from them.

## Who sits behind an integration

The contact chain decides who your notice must reach:

- **Single-account integrators** - a customer's engineers calling your API for their own use. One credential, one owner, often reachable. Risk: the engineer who built it left, and the email on file goes to an empty mailbox.
- **Fleet partner apps** - one partner's app installed across many customer accounts. One fix repairs every install. Rank them first, and reach them through a named person, not a no-reply list.
- **Plugins, self-hosted connectors and agency builds** - one package or credential used by many end sites whose owners never signed up with you. The developer shipping a fix is not the end: each site upgrades on its own schedule, so track installs on the fixed release, and plan a customer-admin notice too.

Name every shape question 3 returns. A loop designed for the first shape reaches nobody in the third.

## Workflow

1. Build the break-date catalog.
2. Attribute traffic to an integration and an owner.
3. Build the drift census.
4. Rank by days to break and blast radius.
5. Close the door, then send and verify.
6. Run the notification ladder.
7. Burn down and gate the sunset.

## 1. Build the break-date catalog

List each forward risk as one row: the surface, the date it breaks, the replacement, and the signal that identifies who still depends on it. A risk with no date is not yet a health signal; send it to `api-versioning-policy` to get one.

- Include risks no deprecation notice announces: expiring client certificates, a CA or TLS change, OAuth client secrets with an expiry, a webhook payload version the platform will stop rendering.
- Include changes that ignore version pins. A removal applied to every version at once breaks pinned integrations that a per-version census calls safe.

The catalog scopes every later step: instrument only signals that map to a row in it.

## 2. Attribute traffic to an integration and an owner

Key attribution on the credential the platform issued - API key ID, OAuth client ID, app ID - logged at the gateway on every request. Add the client fingerprint beside it: SDK name and version header, User-Agent, and the API version actually served. Treat the fingerprint as a hint. User-Agents are spoofable, stripped by proxies, and shared by every tool built on the same HTTP library.

- Measure the **unattributed share**: calls to any catalogued surface that carry no integration identity. On an authenticated surface every accepted call carries a credential, so a share above zero there is a logging gap - fix the logging first. True unattributed traffic exists only on public or unauthenticated surfaces, and it is the floor of what you will break blind.
- Expect shared credentials. An agency or reseller reusing a partner's token makes the partner's report show calls the partner never made. Add a "dispute this attribution" path to every report you send.
- Link each identity to an owner record: the developer or partner account, plus the installing customer accounts for a fleet app.

## 3. Build the drift census

One row per integration per catalogued risk. The fields, a starter query and a good/bad row pair are in [references/signal-catalog.md](references/signal-catalog.md).

**Record the version actually served, not the account default.** One integration can pin a version in several places at once: account default, client configuration, a per-request header, the SDK release in typed languages, and each webhook endpoint separately. A census built from the account default alone reports a migrated account that still receives old-shape webhooks.

**Set the lookback to the longest business cycle from question 5, never a fixed 7 or 30 days.** An integration that runs a year-end close calls once a year. A 30-day window counts it as migrated, and it breaks on its next run, after the cutoff.

**Mark an integration migrated only when one of these holds:**

- No call on the old surface for one full lookback after its first call on the replacement.
- The owner confirms in writing that every job and operation has moved. Any old-surface call after that date reopens the row as unacknowledged.

One replacement call proves nothing on its own: an integration's daily sync can move in March while its year-end job still calls the same old route in December. Under an annual lookback the first rule rarely passes before the break date, so expect top-tier rows to close on written confirmation or an exception; the first rule then serves as the post-cutoff audit. When log retention is shorter than the lookback, mark the row unknown, never migrated, and start retaining for the full cycle now.

**Census dormant integrations too.** A credential with no recent calls is not a migrated integration. It is either seasonal and about to resume on the old surface, or abandoned. Record its last-seen date and resolve which. Hand confirmed-abandoned credentials to `api-auth-key-management`'s revocation flow; never expire them inside the sunset program, where the seasonal ones break.

Signals ranked by efficiency, value returned per unit of effort:

- value (break-dated integrations identified): `deprecated-surface calls > served version > push-destination versions > SDK version > credential expiry > dormant credentials`
- effort: `SDK version > served version > dormant credentials > deprecated-surface calls > push-destination versions == credential expiry` - the tie holds because both read configuration the platform already stores, with no new request-path code.
- efficiency: `deprecated-surface calls > push-destination versions > credential expiry > served version > dormant credentials > SDK version`

Deprecated-surface calls include removed auth methods (password, key in the query string) and deprecated GraphQL fields. On GraphQL every call hits one route, so record field usage per operation and client identity.

**Default rung: count calls to each deprecated route, field and auth method per credential at the gateway.** The gateway already sees every call, so on REST this is a tag plus a grouped count. On GraphQL, field-usage reporting per operation costs more and can push the rung down.

**The starved rung is served version** - second on value, second on effort, so it loses the efficiency round to cheaper signals. It is the only signal that catches per-request header pins, and the most complete one for SDK pins the account default never shows. Promote it whenever a version, not a route, is what retires.

This ranking is a default, not a law. Re-rank it against what you already have:

- A gateway already logging the resolved version per request makes served version as cheap as the default rung.
- Mobile apps and typed SDKs that pin the API version to their release promote SDK version: an end user's device decides when the old version stops calling you.
- Push-only integrations make push-destination versions the default rung.
- A catalog with no dated credential change deletes credential expiry from the menu.

## 4. Rank by days to break and blast radius

Bucket rows by days to break first - breaking before the next escalation step, or later - then sort each bucket by end customers affected. A credential expiring next week outranks a version sunset next year, whatever their install counts. Never sort by call volume: a partner app making ten calls a day across 3,000 installs outranks one account making a million calls, because one conversation fixes 3,000 breakages.

- Add a commercial-weight column - contract terms, penalties, strategic account - and let it promote a row into the top tier. One enterprise contract can outweigh a free plugin's installs.
- Split each bucket into **top tier**, which gets named outreach in step 6, and **long tail**, which gets the automated ladder.
- Size the top tier by outreach capacity, not by a share: take rows from the top of the ranking until the hours from question 7 run out.
- Keep unattributed public-surface traffic in its own row group. It cannot be notified, so only in-response warnings and brownouts reach it.

## 5. Close the door, then send and verify

**On notice day, stop new integrations starting on the old surface.** Scope the door to new integration identities, never to credentials:

- New accounts, new app registrations and new webhook destinations default to, or are pinned to, the replacement.
- Rotated keys, new tokens and new installs of an existing app inherit that app's current surface until its break date or exception. Blocking them breaks integrations inside the notice window you promised.
- Flag marketplace listings that still use the surface during the window. Block new installs only once the surface is past its date.

Without the door, the integrations curve in step 7 can rise while you drain it. Microsoft blocked new application registrations from Azure AD Graph by default after a cutoff date, and Shopify blocks new installs of apps calling resources already unsupported.

**Send the first notice on notice day to every contact on file, and verify in the same message.** The notice window belongs to the policy. Holding the notice for a verification round-trip eats into it. Providers keep an emergency or technical contact field but rarely describe verifying it, and the documented sunset failures share that gap: the notice reached the credential's email, and the person who had to act was two hops away.

- Hold three contact roles per integration: technical owner, commercial owner, and for fleet apps or plugins, the installing customer's admin.
- Ask each notice's recipient to confirm ownership or name the owner. Track bounces and silence. An unverified contact counts as no contact in the readiness gate.
- Route unverified rows to the commercial owner, then the customer admin. The customer admin can uninstall, pressure the vendor or fix it themselves, and they lose data on cutoff day.
- For a standing practice, verify contacts continuously between sunsets, so the next notice starts verified.

Contact procedure and templates are in [references/notification-templates.md](references/notification-templates.md).

## 6. Run the notification ladder

Escalate per integration, not per announcement. Each row climbs one rung when its owner has not acknowledged within the interval you set, and stops climbing once it meets the migrated rule in step 3.

Every notice carries the same payload: the surface, the integration identity, the call count and last-seen time, one sample request ID, the replacement, the migration guide, and the break date. "You are using deprecated APIs" with no specifics produces a support ticket, not a migration.

Rungs, ranked by affected owners who act per unit of effort:

- value: `named outreach > brownout > targeted email > customer-admin notice > in-response warning > dashboard drift report`
- effort: `named outreach > brownout > customer-admin notice > dashboard drift report > in-response warning > targeted email` - the admin notice sits above the dashboard report because it needs partner-contract review and admin resolution across every install.
- efficiency: `targeted email > in-response warning > customer-admin notice > brownout > dashboard drift report > named outreach`
- compliance cost: `customer-admin notice > brownout > targeted email == in-response warning == dashboard drift report == named outreach` - a partner agreement may restrict contacting the partner's customers, and a brownout is a deliberate outage that must fit your SLA terms. The four others tie because each tells the credential holder about its own traffic.

**Default rungs: targeted email to every contact plus an in-response warning, both from notice day.** The email reaches people. The warning reaches whatever still calls, including traffic you could not attribute.

**The starved rung is named outreach** - a partner or account manager calling the owner. It costs hours per row and loses every efficiency round. Promote it for every top-tier row from step 4: those rows hold most of the end customers.

**Brownouts come last, announced and short.**

- Return the final-state status during each window, so integrations fail on the same code path they will hit at cutoff. Put the schedule in the error body, so the engineer who finds the failure finds the date, and send `Cache-Control: no-store` so no cache keeps the failure after the window.
- Escalate the window: hours first, then longer. GitHub ran 12-, 24- and 48-hour brownouts before one removal.
- Run them only once gate line 4 in step 7 holds.

Changelog and policy-page publication sit outside this ladder: `api-versioning-policy` owns them, and they reach no specific owner.

This ranking is a default, not a law. Re-rank it against the user:

- A fixed contractual or security date promotes brownouts earlier, since the date cannot slip.
- A plugin-shaped integration base promotes the customer-admin notice to default; in-admin warnings on installed apps are common practice.
- An outbound partner team already staffed makes named outreach cheaper, so extend it past the top tier.

## 7. Burn down and gate the sunset

Track two curves to the break date: calls on the deprecated surface, and integrations still on it. The calls curve falls first and flatters progress; the integrations curve is the one the gate reads. Track new integrations starting on the old surface too; target zero.

The readiness gate - iterate the ladder until every line holds:

1. Every top-tier integration migrated under the step 3 rule, or covered by an exception in the register.
2. Every remaining long-tail integration notified at a verified contact, or routed to its customer admin.
3. Unattributed public-surface calls below a floor you set and defend; zero on authenticated surfaces.
4. The replacement met its service objective for the migrated traffic over the last several weeks - at least one brownout interval - with no open incident, and has headroom for the residual old-surface load.
5. Every exception in the register carries an owner, a reason and an expiry date.

The same line 4 test gates the first brownout and the cutoff.

**Grant exceptions per integration, never a global slip.** A global extension teaches every integrator that dates move. One high-blast-radius row gets an exception on an allowlist keyed to its credential. Slip the date for everyone only when line 4 fails.

**A date pulled earlier is a policy change, not a burn-down result.** Shortening a published notice breaks the promise every integrator planned against. Hand the decision to `api-versioning-policy`, and require the gate to pass at the new date with the notice owners actually received. A "nearly nobody left" call-share figure never justifies it on its own.

**When the remaining window is shorter than three notice intervals**, compress rather than skip: send at once, at the midpoint and one week before each brownout, and move named outreach for the top tier to this week.

Report the verdict to the decision-maker as a go/no-go against the gate, line by line, never as a date with a percentage. The memo template, burn-down layout, exception register, brownout scheduling and extension precedents are in [references/burn-down-and-readiness.md](references/burn-down-and-readiness.md).

**After cutoff, keep the old code path deployable behind the exception allowlist for one lookback.** A top-tier integration the census missed gets an emergency exception with a two-week expiry, never a global rollback. Every new caller is a census miss: hand its errors to `integration-error-observability` and its attribution gap to the next sunset's catalog.

## Failure modes

- Readiness read from the share of calls migrated, while dozens of integrations remain.
- Census keyed on the account default version, missing per-request overrides and webhook endpoints.
- Lookback shorter than a quarterly or annual job, so a seasonal integration reads as migrated.
- One replacement call taken as proof of migration while another job still calls the old surface.
- Dormant credentials excluded from the census, or expired inside the sunset program, breaking seasonal jobs.
- Rows ranked by call volume, so the plugin with thousands of installs sits below one busy account.
- New integrations still allowed to start on the deprecated surface after notice day.
- Notices held until contacts verify, or sent to the email on file with no bounce check.
- A blast to every developer, training the affected few to ignore the next one.
- Notices with no endpoint, count or sample request ID.
- User-Agent treated as identity, so a shared HTTP library merges unrelated integrations.
- Brownouts unannounced, with no schedule in the error, or run against an unstable replacement.
- A global extension granted for a handful of laggards instead of per-integration exceptions.
- A sunset date pulled in because the call share looks small.

## Measurement

- **Unattributed share** of calls to catalogued surfaces - gate: zero on authenticated surfaces, below your floor on public ones, before the first brownout.
- **Verified-contact coverage** of integrations still on the old surface - gate: 100% verified or routed to a customer admin.
- **Integrations remaining** on each surface, weekly against the break date - the burn-down the gate reads.
- **New integrations starting on the old surface** after notice day - target zero.
- **Time from first notice to acknowledgment**, per rung - the number that justifies promoting a rung.
- **Post-cutoff new callers** - target zero. Each one is a census miss, and its cause goes into the next catalog.

The first two are gates. The rest are trends with no defensible industry figure behind them, so baseline them from your own previous sunset.

## Invocation examples

- "We kill API v2 on March 31 and still see 4% of traffic on it - who is it and how do we reach them?"
- "Build a report showing each partner app which deprecated endpoints it still calls."
- "Our webhook payload v1 retires next quarter; how do we find every endpoint still on it?"
- "Half our deprecation emails bounce. Fix how we reach integration owners before the sunset."
- "Is it safe to turn off password auth next month? Usage dropped to almost nothing."

## References

- [references/signal-catalog.md](references/signal-catalog.md) - forward-risk signal definitions, served-version resolution across pin sites, the first census query, census row fields, a good/bad census row, partner-visible versus internal fields.
- [references/notification-templates.md](references/notification-templates.md) - contact resolution procedure, notice payload, cadence rules, templates for every rung including the confirmation request, outreach brief and drift report.
- [references/burn-down-and-readiness.md](references/burn-down-and-readiness.md) - two-curve burn-down, readiness worksheet, go/no-go memo, exception register, brownout scheduling, vendor notice and extension precedents.

See also, same collection:

- `samber/developer-platform-skills@sdk-portfolio-strategy` - decides when an SDK reaches end of life; this skill finds who still runs it.
- `samber/developer-platform-skills@webhook-platform-design` - the payload-versioning model behind push-destination drift.
- `samber/developer-platform-skills@app-marketplace-listing-standards` - listing staleness and flags on marketplace apps still on a deprecated surface.
- `samber/developer-platform-skills@connector-certification-program` - renewal and decertification of certified connectors, which can consume this census.
