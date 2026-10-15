---
name: fcode-ama
description: Factorial Code platform user journey and support — requesting access, development teams, creating an App (name, language, OAuth scopes, integrations framework), the Getting started checklist, OAuth app setup, local development, demo companies, the Dev Marketplace, installing apps, appRole forms, releases and promotion to production, marketplace publication (DatoCMS, private apps), and escalation paths. Use when answering "how do I…" questions about using the Factorial Code platform, guiding a user through any journey stage, or acting as a Factorial Code support agent.
license: MIT
metadata:
  category: factorial-code
---

# Factorial Code — platform guide (AMA)

Factorial Code (fcode) is Factorial's platform for building apps and
automations against the Factorial Public API. This skill covers **using the
platform** — the journey from requesting access to a published marketplace
app — and how to behave when supporting users through it. For *building* the
app itself (processes, modules, CLI, forms), route to the owning skills
(see the routing table below).

The full stage-by-stage walkthrough is in `references/journey.md`; common
problems and fixes are in `references/troubleshooting.md`.

## Who you're helping

Three user roles use the platform. Establish which one you're talking to
early — several flows diverge by role:

| Role | Who | Key differences |
|---|---|---|
| **Factorial internal** | Developers at Factorial | Create their own OAuth apps in the **Factorial Backoffice**; create demo companies directly (using the Demo generator); Slack `#factorial-code-users` available |
| **Partner** | External companies building apps/integrations with Factorial | OAuth app preconfigured by an administrator; demo companies by request |
| **Individual Contributor** | Someone building their own app or automation (may be a customer, but not always — never call this role "end customer") | Same as Partner |

All roles talk to Factorial through the **Public API**, and all belong to a
**development team**: every app a team creates is shared by all its members.
When someone requests access and an administrator sees their organization
already has a team on the platform, they are added to that existing team.

## Support-agent behavior rules

- **Answer only from documented flows** — this skill, its references, the
  other `fcode-*` skills, and the public docs. Never invent UI elements,
  URLs, commands, or policies. If it isn't covered, say so and escalate.
- **Identify the user's role first** when the answer differs by role.
- **Describe flows by page and section name** (e.g. "the Getting started
  checklist on the App detail page"), not by exact button pixels — labels
  change; flows are stable.
- **Admin actions: outcome only.** When a step is performed by an
  administrator (access approval, demo provisioning, OAuth preconfiguration,
  release review), tell the user what they will observe and what to do next.
  Never describe admin-side mechanics or how credentials are delivered.
- **Answer in the user's language.**
- **Fetch before deep-diving.** When you have web access, read the linked
  docs page before answering a detailed question; the live docs win over
  this skill on details. Without web access, answer from this skill and say
  which docs page has more.
- **Escalate when needed** — an admin action, a stuck request, or an
  uncovered question. Escalation paths are in the last section.

## Platform map

Everything lives under `https://code.factorialhr.com`, split across three
surfaces users often conflate:

- **Docs** (`/docs/...`) — public documentation, plus the landing page with
  the request-access form.
- **App console** (`/dashboard/...`) — apps, teams, demo companies,
  marketplaces, installations. Where the journey below happens.
- **Workspace console** (`/platform/...`) — inside a workspace: processes,
  executions, schedules, variables, versions, API credentials. The app
  console links into it (e.g. "open workspace" on an environment tab).

App console areas:

| Area | What it's for |
|---|---|
| **Apps** | The team's apps; where a new app is created |
| **App detail page** | Per-app home: the Getting started checklist and the **Development / Production / Publication** tabs; app settings |
| **Demo Companies** | Demo Factorial companies for testing installs |
| **Dev Marketplace** | Simulation of the production marketplace, run against demo companies |
| **Marketplace** | The production marketplace companies see |
| **Team** | Development team members and settings |
| **Installations** | The app installations across companies |

## The journey at a glance

| # | Stage | Where | What happens |
|---|---|---|---|
| 1 | Request access | Landing page → request-access form | An administrator reviews it; you're notified of the outcome and can then sign in. Joins an existing development team when one matches |
| 2 | Create an App | Apps → create | Name and purpose; language (**JavaScript** or **Python**); **OAuth scopes** (they bound what the app may do on the Factorial API); whether it uses the **integrations framework** — opt in only when you know what it provides (see `references/journey.md`) |
| 3 | Getting started | App detail page checklist | Ordered setup steps: build locally, link the Factorial integration (framework apps only), configure dev/prod OAuth (only when scopes were requested), publish a release, add marketplace metadata |
| 4 | Configure OAuth | Development / Production tabs | Client credentials for the OAuth flow against the Factorial API. Internal teams create the OAuth app themselves in the Factorial Backoffice; for Partners and Individual Contributors an administrator preconfigures it (automation planned) |
| 5 | Build locally | Your machine | Install the CLI, `fcode clone` the dev workspace, code with your own agent + the `fcode-*` skills, test locally, `fcode push` to the cloud dev workspace |
| 6 | Demo company | Demo Companies page | Internal: create directly (using the Demo generator). Partner/IC: request one; it's provisioned and you're notified by email |
| 7 | Test installs | Dev Marketplace | Run the real OAuth flow with the demo company's credentials and install the app; exercise its `appRole` forms |
| 8 | Release | App detail → Production tab | Request a release (semver + notes); the platform validates it; when deployed, the snapshot lands in the read-only prod workspace and the app becomes **published** |
| 9 | Publish listing | App detail → Publication tab | Metadata for the marketplace listing: link a DatoCMS record and/or fill the fallback (tagline, description, categories, screenshots); mark private if needed |
| 10 | Production | Marketplace | The app is visible and installable by companies; each install gets its own isolated workspace |

Per-stage detail, per-role callouts, and lifecycle states: `references/journey.md`.

## Workspaces behind the journey

Naming caution: a Factorial Code **workspace** is also called a "team" in the
workspace console and CLI (`team.json`, team variables, `fcode team:*`) —
that is unrelated to the **development team** of humans described above.

Each app maps to workspaces (slugs carry an encoded token, not the raw id):

- `dev-{appId}` — the development workspace you clone and push to.
- `prod-{appId}` — production copy; its code is read-only, updated only by
  deployed releases, but its variables are live — shared defaults and
  credentials for all installations are managed there.
- `deploy-{installationId}` — one per company installation, inheriting from
  the app workspace: it holds only that company's variables and executions,
  fully isolated from other companies. A change in the parent workspace is
  automatically available in every installation workspace.
- `base-app` / `base-integration-app` (language-matched variants, `-js`/`-py`)
  — shared bases every app inherits: API clients, webhook/schedule/email/form
  helpers, and (for framework apps) the integration templates.

Released versions are pinned tags; the **`stable` alias** points at the
current one, so forms, webhooks, and other external consumers pin to `stable`
and a rollout or rollback is a single alias move. For a marketplace app, ship
through the release flow (stage 8) — it wraps workspace version publishing;
don't publish versions or move `stable` by hand (those primitives, for
standalone workspaces, are in `fcode-core-concepts` / `fcode-cli`).

## Routing — where deep questions live

| Question is about | Route to |
|---|---|
| Platform model: processes, modules, variables & inheritance, datastore/storage, versioning & `stable` | `fcode-core-concepts` |
| CLI commands, `metadata.json` / `team.json` fields, `appRole` field reference, webhook auth, `FACTORIAL_TOKEN` | `fcode-cli` — docs: `/docs/cli/` |
| Writing process/module code | `fcode-javascript` / `fcode-python` — docs: `/docs/processes/` |
| Input-parameter schemas (forms definition) | `fcode-json-schema` |
| Embedding forms on webpages, themes, pre-fill | `fcode-forms` — docs: `/docs/forms/` |
| Recommended agent working method, MCP tools | `fcode-agent` — docs: `/docs/mcp-server/` |
| Worked examples (integration, install/uninstall lifecycle) | `fcode-examples` |
| Executions, schedules, webhooks at runtime | docs: `/docs/executions/` |
| Integrations framework | docs: `/docs/building-apps/integrations-framework/` |
| OAuth & API tokens | docs: `/docs/building-apps/oauth/` |
| Workspace hierarchy | docs: `/docs/building-apps/workspaces/` |
| The end-to-end journey (public version) | docs: `/docs/building-apps/developer-journey/` |

Doc paths are relative to `https://code.factorialhr.com`.

## Escalation & admin actions

| Need | What to do |
|---|---|
| Access request pending | It's under review; you'll be notified of the outcome |
| OAuth app for a Partner / Individual Contributor | Preconfigured by an administrator — visible on the app's environment tabs once done |
| Demo company (Partner / IC) | "Request a demo company" on the Demo Companies page; you're emailed when it's ready |
| Release review outcome | The release either deploys or you're notified of required changes; fix and request again with a higher version |
| Private app installed for a specific company | A production installation created from the App detail page — by an administrator **or by a developer** who provides the Factorial company ID (e.g. how Factorial's Forward Deployed Engineers roll out private apps) |
| Anything not covered | Internal Factorial users: Slack `#factorial-code-users`. Others: the in-platform request flows above |
