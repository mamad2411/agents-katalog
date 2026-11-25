---
name: zapier-integration-playbook
description: >-
  Builds, publishes, grows and maintains a B2B SaaS vendor's own Zapier integration - Platform
  CLI code (triggers, actions, auth, invoke and push), Zapier's review and beta, Partner Program
  tiers, publishing Zap templates, Workflow Element embeds and versioning without breaking live
  Zaps. Use whenever the user mentions their Zapier integration, zapier-platform CLI or Platform
  UI, the Zapier app directory, or a Zapier trigger that misses
  or duplicates records. Do NOT use for building Zaps as an end user, for calling existing Zapier
  apps from code or agents (Zapier SDK, Zapier MCP), for choosing embedded iPaaS (use
  samber/developer-platform-skills@connector-marketplace-strategy), or for generic marketplace
  listing work (use samber/developer-platform-skills@integration-listing-optimization).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Zapier integration playbook

You own a SaaS product's integration on Zapier: a set of triggers, actions and searches that thousands of users wire into Zaps you never see. Every live Zap depends on today's keys and field shapes.

## Changes that break live Zaps

Zapier's change matrix and deduplication docs make each of these breaking in effect. Each stops existing Zaps, floods them, or forces users to rebuild them by hand:

- Renaming or removing a trigger, action, input-field or output-field key.
- Changing an output's response structure, or an input field's type.
- Switching a trigger between polling and REST hook.
- Changing the auth scheme, renaming an auth field, or adding a required auth field.
- Adding a required input field, unless it defaults.
- Changing what counts as "new" on a live polling trigger: sort order, page contents or id format. Each live Zap's dedupe memory holds the old ids, so the first poll after the change fires every unseen item as new.

Ship the replacement beside the original instead: copy the step under a new key (`new_invoice_v2`) with the same name and description, make the change there, hide the old step. Old Zaps keep running; new Zaps get the new step. Hiding a step invalidates every Zap template built on it: rebuild and resubmit those templates on the new key. Breaking changes that cannot ship this way need a new major version, and Zapier blocks user migration across majors: every user updates their Zaps manually.

Promotion blocks most schema-level breaking changes inside a major, but not renamed or removed output keys, changed response structure, or changed perform behavior. Diff those yourself before every promotion.

| Rationalization | Why it fails |
| --- | --- |
| "The key is ugly, let's rename it." | Users never see keys. Renaming breaks every Zap using it. |
| "It's a small user base, they'll rebuild their Zaps." | Zapier gives you no user email list; you reach them only through your own channels. |
| "Just fix the sort order in place, it's a bug." | Every live Zap floods with old records on the next poll. Twin it under a new key. |
| "We'll migrate everyone to 2.0." | Migrations stop at the major boundary, in the UI and CLI alike. |
| "Polling is slow; flip the trigger to instant." | Type changes are breaking. Add an instant twin under a new key, hide the polling one. |

## Interview

Ask one question at a time; skip what the request or repo already answers. When you cannot ask, state an assumption for each missing answer and flag it in the output:

1. Stage: no integration, private (how many users), submitted, beta, or public? Platform UI or CLI?
2. Current steps: which triggers, actions, searches; polling or hook; auth scheme?
3. Does the API expose a webhook subscription endpoint, newest-first sorting, unique ids, OAuth?
4. Which jobs do customers automate today: support tickets, CSV exports, "do you integrate with X" requests?
5. Date a result must land by, one-off launch or compounding channel, and engineering days available.

Re-rank every menu below against answers 3 and 5, and say which answer moved which option. Use answer 1 to choose UI or CLI (see Build).

## Route by stage

- **Any version with live users, or any planned change to one** → classify every change first (Maintain, step 4), then continue below.
- **No integration or private** → Design, Build, then Publish.
- **Submitted** → Publish steps 4-5; draft templates and help articles while review runs.
- **Beta or public** → Grow; go back to Design for any step whose 24-hour activation trails the others.
- **Deciding whether to be on Zapier at all** → samber/developer-platform-skills@connector-marketplace-strategy.

## Design

1. **Pick the steps from customer jobs**, not from the API reference. Read Zapier's recommended steps for the app's category on its recommended-triggers-and-actions page when you can browse; otherwise start from the examples in [references/platform-rules.md](references/platform-rules.md). Keep what support tickets and exports prove people do. Order: event triggers on core objects > creates on core objects > searches that feed dropdowns and search-or-create > updates > everything else. Ship four to eight good steps before twenty thin ones.
2. **Shape the steps Zapier's way**: create-or-update becomes a search-or-create plus an Update action; avoid deletes, and give any delete a copy field saying it is irreversible.
3. **Use the product's own nouns.** Step names title-cased (`New Invoice`, `Create Customer`, `Find Invoice`), field labels sentence-cased; descriptions "Triggers when…", "Creates a…", "Finds a…".
4. **Auth**: OAuth v2 when the product already issues OAuth tokens, else self-serve API key. Basic auth is acceptable but weakest. Users who must email support for a key block publication. Return HTTP 401 on expired tokens: Zapier refreshes on 401 only.
5. **Trigger type**: REST hook (shown as Instant) when the API can create and delete webhook subscriptions per Zap and keep several alive at once. Otherwise polling. Never a static webhook in a public integration. Every hook trigger also needs a perform list returning the exact payload schema; hook deliveries are not deduplicated, so send each event once.
6. **Polling contract**: newest-first, a unique primary key that never changes format, enough items per page to cover a burst (Zapier never reads page two). Zapier dedupes by id per Zap, so never filter "already sent" items server-side. An "updated" trigger needs a composite id such as `id-updated_at`; keep the original id in another field. Prefer a specific state trigger (`New Paid Invoice`) over a generic "Updated Invoice". A trigger that routinely exceeds 100 new items per poll belongs on a hook.
7. **Fields**: no input a user must type an id into; back each with a dynamic dropdown from a hidden trigger, plus a search for mapped values. Expose account custom fields as dynamic fields. Mirror the API's required fields exactly.
8. **Output and samples**: return id, human name, link to the record, ISO 8601 dates with offset, split names and addresses. Static sample data: one item, realistic values, only keys every account returns, so no custom fields.
9. **Errors**: never return 200 on a failure. User-fixable failures raise a normal error naming the field and the reason, under 250 characters (Zapier truncates the rest). Unmet preconditions (duplicate, already paid) raise a halted error, which never counts toward the auto-off rule. Let 429 surface with a `Retry-After` header: Zapier retries it. During a known outage, throw a throttled error with a delay; an uncaught 5xx errors the run toward the auto-off rule. Searches with no match return an empty array.
10. **Never move money.** Publishing rules ban facilitating payments or asset transfers. Recording a completed payment matches Zapier's own accounting recommendations; confirm anything that starts a charge, such as a payment link, with Zapier partner support before building it.

For an inherited integration, audit against this list first and classify each fix as additive (new key, hide old) or breaking (new major). Prefer additive fixes inside the current major. A version is editable only while private with fewer than 5 users: otherwise clone it to the next minor of the same major (`1.0.3` → `1.1.0`), fix the clone, promote, migrate. Hidden steps keep serving existing Zaps; confirm in validation that hiding a static-webhook step clears its publishing check.

## Build

Default to the CLI: the integration lives as code, so a private staging integration is one `register` away and stays identical to production. Keep the Platform UI only for a small integration that a non-engineer maintains and that needs no staging copy. Moving UI → CLI is a `convert`; CLI → UI is a manual rebuild users cannot migrate to. For the code-level API, read [references/cli-build.md](references/cli-build.md).

1. Scaffold with `zapier-platform init`, `register` the integration, pin `zapier-platform-core` exactly in `package.json`, keep secrets in per-version environment variables.
2. Write `authentication` with a cheap `test` call and a connection label; for OAuth2 set `refreshAccessToken` and `autoRefresh`.
3. Write each step from the Design list: triggers (polling `perform`, or hook `performSubscribe` / `performUnsubscribe` / `perform` / `performList`), creates, searches, `searchOrCreates`.
4. Add input fields (static, dynamic dropdowns, dynamic fields, line items), output fields and a static `sample` per step.
5. Centralize auth headers and error mapping in `beforeRequest` / `afterResponse`; throw only `z.errors.*`.
6. Test locally with `zapier-platform invoke` and unit tests with mocked HTTP, then `validate` and `push` a version.
7. Register a second, private integration (`<App> (Staging)`) from the same code. Keep the `.zapierapprc` that `register` or `link` writes for each integration as a per-environment file, and copy the right one in before `push`. Point the staging integration's environment variables at your staging API. Invite testers with `users:add` or `users:links`, and push and `invoke` there before you push to production. Never promote it: private integrations stay out of the app directory, and Zapier allows one public integration per app.

## Publish

1. Make every visible step pass a live run: at least 3 users with a live Zap, one live Zap and one successful run per visible step, in the admins' Zap history. Hide steps nobody can exercise.
2. Clear every validation Error and Publishing Task in the Developer Platform; Warnings don't block but read them.
3. Meet the eligibility rules: a publicly launched product, API ownership, production HTTPS endpoints, a non-expiring test account with paid features, an admin with a company-domain email, one public integration per app, not a Zapier competitor. See [references/platform-rules.md](references/platform-rules.md).
4. Submit from Integration Home; a reviewer replies with outstanding items, typically within a week. Each fix round adds about another week.
5. Approval lists you in the app directory as Beta. Beta ends after 90 days, or the next business day after Zapier detects one signup from any of your Zapier embeds.

Against a deadline, count backwards: recruiting the 3 live users comes before submission, templates exist only after approval, template review takes about two weeks. Four weeks between submission and the date is the happy-path minimum.

## Grow

Efficiency: Zap templates > a template embedded in the launch post and help articles > Workflow Element on the product's integrations page > Zapier surfaced in onboarding, support answers and empty integration search > Zapier spotlight benefits (Silver and up) > a custom marketplace on the Workflow API.

| Lever | Value | Low effort | Gate |
| --- | --- | --- | --- |
| 5-10 Zap templates for the top jobs | ++ | +++ | beta or public, ~2-week review |
| Template embed in launch post and help article per job | ++ | +++ (minutes) | one public template |
| Workflow Element in-product | +++ | ++ (an hour or two) | beta or public, a public template, domain allowlist |
| Onboarding, support macros, empty-search fallback | ++ | ++ | none |
| Newsletter spotlight, featured week, blog flyover | + | ++ | Silver+ (50 active users) |
| Custom marketplace on the Workflow API | +++ | - (a week) | engineering capacity |

- Submit templates on approval day: every other surface embeds them, and private integrations cannot have any. Anyone can publish templates for your app, and Zapier generates some from usage; yours are the ones you control.
- Any Zapier embed that produces one signup exits beta the next business day and, with a healthy score and the minimum active users, unlocks the next tier's benefits early. A deadline makes the first public template, embedded in the launch post, the fastest route; add the Workflow Element once templates are public.
- The order starves the Workflow API marketplace. Promote it when the product already runs an integrations directory with heavy search traffic. If Zapier must stay invisible in-product, that is an embedded-iPaaS decision for connector-marketplace-strategy.
- Zapier-led co-marketing campaigns are Platinum only, and Zapier pays partners no revenue share; the return is retained, activated users.
- Write template copy to Zapier's rules: see [references/templates.md](references/templates.md).

## Maintain

1. Read the Partner Program tier inputs: active users this quarter (tiers re-evaluated each January, April, July, October) and a health score built from open bug reports, feature requests and response to them, not from error rates. Work the Bugs & Feature Requests queue weekly, or sync it to your tracker with Zapier Issue Manager; keep users affected by open bugs under 10% of monthly actives.
2. Watch Zap activation within 24 hours by trigger and by action. A low step means a design defect: test it in the editor yourself.
3. Watch run errors: a Zap erroring on 95% of more than 20 runs over 7 days turns off. Zapier documents no integration-level error threshold for delisting; don't promise one.
4. For any change, classify it with [references/versioning.md](references/versioning.md), then clone, change, validate and diff by hand before promoting. Automatic migrations are on by default: promotion itself moves a first group of users, so test first. CLI: canary 5-10% for 30-60 minutes. UI: share the clone with test accounts. Then promote, watch Monitoring, migrate the rest. Breaking changes go additive (new key, hide old) or to a new major.
5. Public integrations sit in Zapier's Integration Maintenance Program by default: Zapier engineers may change your versions, and a CLI team must pull those changes before pushing or promoting. Only the Technical Contact can opt out.
6. Deprecate only a version that will stop working, such as on an endpoint sunset; otherwise mark it legacy. Set the date 3 weeks to 1 year ahead; Zapier emails affected users 14 days before; with automatic migrations on, users migrated before then get no email. Announce in-app and by email too.

## Measure

- Activation within 24 hours per step; target self-set, compare steps against each other.
- Quarterly active users against the next tier threshold; share of users on the promoted version.
- Open bugs and feature requests, and median days to first response.
- Templates live, embed click-to-activation funnel.

## Output

Return these sections, in order:

1. Assumptions, one line each, for every interview answer you lacked.
2. Stage and route.
3. Step table: key, label, type, change class (`keep` / `additive` / `hide` / `breaking` / `rejected`), reason.
4. Auth and trigger-type decisions, each with the API capability it rests on.
5. Publish checklist: item, owner role, week.
6. Growth actions ranked, with the interview answer that moved each.
7. Versioning plan: target version, canary, migration, what you diff by hand.
8. Metric baseline: current value, or "unknown" plus where to read it.

Mark every Zapier platform number, from this file or its references, with `†` and a footnote: verify against Zapier's live docs before quoting it.

## References

- samber/developer-platform-skills@webhook-platform-design - the subscription API a REST hook trigger needs.
- samber/developer-platform-skills@api-versioning-policy - deprecating the underlying API without stranding Zap users.
- samber/developer-platform-skills@oauth2-provider-design - the OAuth server Zapier connects through.
- samber/developer-platform-skills@integration-error-observability - your own per-integration logs beside Zapier's Monitoring.
- samber/developer-platform-skills@integration-partnership-strategy - whether Zapier beats a native integration for a given partner.
