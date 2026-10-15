---
name: avo-rest-api
description: Expose a JSON REST API over every Avo resource with the `avo-api` add-on — list/read/create/update/delete plus read-only association traversal, reusing each resource's fields, view visibility, and authorization, with no per-resource controllers. Bearer tokens are managed from the Avo UI (create, reveal-once, disable, revoke) and gated by an opt-in, per-token permission matrix; a code hook (`setup_authentication`) covers HTTP Basic / API-key / public schemes. Use when the user wants to expose a JSON API for a mobile app, let an external service or SPA read/write records over HTTP, add a REST API without writing controllers, issue API tokens for third-party or server-to-server access, give the frontend an API backed by the admin, ship a public read-only API for a resource, or build a webhook/integration that pulls records — whether they say it in Avo terms (`mount_avo_api`, `avo-api`, `avo_api_tokens`, `setup_authentication`, permission grants, token pepper) or plain terms ("programmatic access to my models", "server-to-server access to admin data", "an API for the mobile app").
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch
---

# Avo REST API

The `avo-api` add-on serves a JSON REST API for **every Avo resource** — the resources you already built for the admin panel are instantly available over HTTP (index, show, create, update, delete, plus read-only association traversal). It reuses each resource's field definitions, per-view visibility, and authorization, so there are **no per-resource controllers to write**: a single catch-all controller serves them all, keyed by the resource's `route_key`.

The API is **closed by default and security-forward**. Authentication is either a UI-managed **Bearer token** or a code hook you override; access is an **opt-in permission matrix** (a token with no grants can reach nothing). Get the mounting, the token pepper, and the grant model right and the rest follows.

- **Gem:** `avo-api`, from the private gem server (`packager.dev`). **Paid add-on** ([avohq.io/addons/json-api](https://avohq.io/addons/json-api)) — state this up front when scoping the work.
- **Migration tables:** `avo_api_tokens` and `avo_api_permission_grants`.
- **Config:** an `Avo::Api.configure` block in `config/initializers/avo.rb` (`manage_tokens_if`), plus the token pepper in credentials/ENV and `mount_avo_api` in `config/routes.rb`.

## Docs

Authoritative docs — fetch on demand (prefer the raw `.md`) rather than guessing, and verify every option/path name against the docs or the app's installed `avo-api` source before writing it:

- Docs map (discover any Avo page): https://docs.avohq.io/4.0/docs-map.md
- REST API (the whole feature — install, mount, auth, permissions, request/response, config reference): https://docs.avohq.io/4.0/rest-api.md
- Authorization (Pundit; interacts with the code-auth path): https://docs.avohq.io/4.0/authorization.md
- Authentication (Avo must know `current_user` for the code-auth path): https://docs.avohq.io/4.0/authentication.md

Read the REST API page before implementing anything beyond a stock install — the two auth paths behave differently and the permission model is easy to get wrong from memory.

## Install

Five steps, in order. Skipping the pepper or mis-mounting the engine are the two failures that break everything downstream.

### 1. Add the gem

```ruby
# Gemfile
gem "avo-api", source: "https://packager.dev/avo-hq/"
```

```bash
bundle install
```

The private gem server needs a Gem Server Token to bundle — that's the **avo-setup** skill (`BUNDLE_PACKAGER__DEV`, `bundle config`, host secrets). Hand off if `bundle install` 403s.

### 2. Run the install generator

```bash
rails generate avo_api:install
```

It copies one migration (creating `avo_api_tokens` + `avo_api_permission_grants`) and appends an `Avo::Api.configure` block to `config/initializers/avo.rb` with the `manage_tokens_if` gate and token-pepper instructions.

### 3. Migrate

```bash
rails db:migrate
```

### 4. Set the token pepper (REQUIRED)

Tokens are stored as HMAC-SHA256 digests keyed by a server-side **pepper**. Token creation **and** authentication **fail closed (raise)** until it's set. Generate a secret and store it in credentials (preferred) or the environment:

```bash
rails secret            # prints a long random value
rails credentials:edit
```

```yaml
# config/credentials.yml.enc
avo_api:
  token_pepper: <the value from `rails secret`>
```

Or set `AVO_API_TOKEN_PEPPER` in the environment. **Changing the pepper invalidates every existing token** — treat it like a signing key: set once, keep stable.

### 5. Mount the engine

```ruby
# config/routes.rb
Rails.application.routes.draw do
  mount_avo_api                       # mounts at /api by default

  authenticate :user do
    mount_avo
  end
end
```

`mount_avo_api` must sit **outside and before** any `authenticate :user do … end` block — see Gotchas. It forwards any option Rails' `mount` accepts:

```ruby
mount_avo_api at: "#{Avo.configuration.root_path}/api"     # e.g. /admin/api
mount_avo_api at: "/api", constraints: { subdomain: "api" } # api subdomain only
mount_avo_api do
  get "health", to: "health#check"                          # custom routes inside the engine
end
```

## When this applies

Reach for this skill when the request is "let something outside the admin **read or write** my records over HTTP" — a mobile app, an SPA, a partner service, a webhook, an internal integration:

| Request (Avo-shaped or plain) | What it maps to |
| --- | --- |
| "Expose a JSON API for the mobile app / SPA" | Install + `mount_avo_api` + a token with grants |
| "A REST API without writing controllers" | The catch-all controller — nothing to write |
| "API tokens for third-party access", "server-to-server access" | UI-managed Bearer tokens + per-token grant matrix |
| "Public read-only API for a resource" | `setup_authentication` left empty + default (read-only) grants |
| "Let an internal service read admin data with our existing auth" | `setup_authentication` code hook (HTTP Basic / API key) + Pundit |
| "Webhook/integration that pulls records" | Bearer token granted `index`/`show` on the resource(s) |
| "Give an external service write access to records" | Bearer token granted `create`/`update`/`destroy` (writes need a token) |
| "Shape which fields the API returns" | The resource's own view visibility (`only_on:`/`hide_on:`) |

Boundaries: **which fields exist and how they render** is the resource definition (**avo-fields** / **avo-resources**); **who `current_user` is** for the code-auth path is **avo-authentication**; **Pundit policies** that scope the code-auth path are **avo-authorization**; **bundling the paid gem + the mount** is **avo-setup**. This skill owns the API surface, tokens, and the grant matrix.

## Workflow

### Endpoints

For each resource, standard RESTful endpoints live under `resources/v1`, keyed by the resource's `route_key` (e.g. `teams`, `blog_posts`, `product_categories`). For a `teams` resource at the default `/api` mount:

```
GET    /api/resources/v1/teams          # index (paginated, sortable)
POST   /api/resources/v1/teams          # create
GET    /api/resources/v1/teams/:id      # show
PATCH  /api/resources/v1/teams/:id      # update (partial)
PUT    /api/resources/v1/teams/:id      # update (full)
DELETE /api/resources/v1/teams/:id      # destroy
GET    /api/resources/v1/teams/:id/members   # read-only association traversal
```

### Reading

**Index** returns records visible on the `:index` view plus a `pagination` block. Query params (index only): `page` (default `1`), `per_page` (default from your Avo config), `sort_by` (field), `sort_direction` (`asc`/`desc`).

```bash
curl "https://example.com/api/resources/v1/teams?page=2&per_page=10&sort_by=name&sort_direction=asc" \
  -H "Authorization: Bearer avo_xxxx"
```

**Show** returns one record with fields visible on the `:show` view. **Association traversal** (`/:id/members`) returns the association's records serialized with the **target** resource's `:index` fields — read-only, and the actor must be granted `index` (or `show`) on the **target** resource or the response is `403`.

Field values are serialized by type:

| Field type | Shape |
| --- | --- |
| Text, number, boolean, date/datetime | The raw value |
| `belongs_to` | `{ "id": 5, "label": "John Doe" }` |
| `has_many`, `has_one` | `{ "count": 12 }` (or `{ "id": 5 }` for a single loaded record) |
| `file`, `files` | `{ "filename": …, "content_type": …, "byte_size": …, "url": … }` |

Shape the response per view with the resource's own visibility — a field `hide_on: :index` is absent from the index response, `only_on: :show` appears only in show. An association key is **omitted entirely** when the actor may not read the target (no foreign-key or existence leak — see Gotchas). For **token** actors, file `url`s are **signed and expiring** (~5 min); code-auth actors get the standard attachment URL.

### Writing

Send field data under the resource's **singular** key, as JSON. `belongs_to` is written as the foreign key (`"admin_id": 5`).

```bash
curl -X POST https://example.com/api/resources/v1/teams \
  -H "Authorization: Bearer avo_xxxx" -H "Content-Type: application/json" \
  -d '{ "team": { "name": "Mobile Team", "url": "https://mobile.example.com", "admin_id": 5 } }'
```

- **Create** → `201 Created`, record serialized on `:show`.
- **Update** (`PATCH` partial / `PUT` full) → `200 OK`, updated record on `:show`.
- **Delete** → `200 OK` with a message.
- **Validation failure** → `422 Unprocessable Entity` with `{ "errors": { field: [...] }, "message": … }`.

Status codes: `200` ok · `201` created · `401` unauthenticated · `403` no grant · `404` not found · `422` validation errors.

### Custom controllers (only when overriding)

You need **no** controllers for the standard behavior. Generate one only to override a specific resource (custom `setup_authentication`, `setup_csrf_protection`, response shape, or serialization):

```bash
rails generate avo_api:controller User     # one resource
rails generate avo_api:controllers         # one per existing resource
```

Both create controllers under `app/controllers/avo/api/resources/v1/` that inherit `BaseResourcesController`. The override route is drawn **first**, so it wins over the catch-all. Naming follows Rails: `Avo::Resources::BlogPost` → `Avo::Api::Resources::V1::BlogPostsController`.

Overridable hooks on `BaseResourcesController`: the actions `index` / `show` / `create` / `update` / `destroy` / `related`; result callbacks `create_success_action` / `create_fail_action` / `update_*` / `destroy_*`; serialization `serialize_records(resources, view)` / `serialize_record(resource, view)` / `serialize_field_value(field)`; and auth `setup_authentication` / `self.setup_csrf_protection`. Call `super` and adjust, or replace outright.

```ruby
# app/controllers/avo/api/resources/v1/users_controller.rb
module Avo::Api::Resources::V1
  class UsersController < BaseResourcesController
    def create_success_action
      render json: { record: serialize_record(@resource, :show),
                     message: "Welcome! Your account has been created." },
             status: :created
    end
  end
end
```

**CSRF:** API controllers use Rails' `:null_session` strategy by default (correct for stateless token clients). Override per controller to change it:

```ruby
def self.setup_csrf_protection
  protect_from_forgery with: :exception   # or leave empty to disable entirely
end
```

## Auth & permissions

Two independent layers, both closed by default: **authentication** (who is calling) and **permissions** (what they may reach). A brand-new token authenticates but reaches **nothing** until it has grants.

### Authentication — two paths

Every request is checked in this order:

1. **Bearer token** — `Authorization: Bearer <token>`. The primary mechanism, for external and server-to-server clients. A valid token wins and the code hook is skipped. A **malformed or invalid** token is a uniform `401` with **no fall-through** — it never silently degrades to the code hook.
2. **Code hook** — when no Bearer token is present, the request calls `setup_authentication`. By default it **raises** (request rejected), so a stock resource is closed on this path until you override it.

With no valid token and no override, every request is `401` — the API is closed by default. Override `setup_authentication` in a generated controller to plug in your own scheme:

```ruby
# Public, unauthenticated reads for one resource:
def setup_authentication
  # leave empty to disable the code-auth check
end

# API key (server-to-server):
def setup_authentication
  expected = ENV.fetch("API_KEY")
  provided = request.headers["Authorization"]&.sub(/^ApiKey /, "")
  unless ActiveSupport::SecurityUtils.secure_compare(provided.to_s, expected)
    raise Avo::Api::AuthenticationError
  end
end
```

Raise `Avo::Api::AuthenticationError` to reject (renders `401`). HTTP Basic works the same way via `authenticate_with_http_basic`.

### Managing tokens (the UI)

Token management is gated by `manage_tokens_if`, which **defaults to deny**. Opt specific users in:

```ruby
# config/initializers/avo.rb
Avo::Api.configure do |config|
  config.manage_tokens_if = ->(user) { user.admin? }
end
```

Once enabled, an **API Tokens** entry appears in the Avo sidebar, where you can:

- **Create** a token with a name and optional expiry (blank = never expires).
- **Copy the secret** — the raw token is shown **exactly once**, on a one-time reveal screen. It's never stored or shown again; if lost, revoke and recreate.
- **Disable / enable** — reversible deactivation.
- **Revoke** — permanent (terminal; cannot be re-enabled).

Status is one of `Active` / `Disabled` / `Expired` / `Revoked`; only `Active` tokens authenticate. `last_used_at` is tracked so you can spot stale tokens.

### Permissions — opt-in from zero

Nothing is reachable until a **grant** exists. A grant is a `resource × verb` pair, where verbs map 1:1 to the REST actions: `index`, `show`, `create`, `update`, `destroy`. A request with no matching grant gets `403` — checked **before** record loading, so an ungranted client can't even probe whether a record exists.

Two grant sets:

- **Per-token grants** govern a specific Bearer token (edit them on that token's page). They may grant **any** verb, including writes.
- **The default permissions list** governs the **code-auth** path. Manage it at **API Settings** (`/<root_path>/avo_api/settings`). It is **read-only** — it may grant `index` and `show` only. **Writes always require a Bearer token.**

### How the two paths differ (critical)

| | Token request | Code-auth request |
| --- | --- | --- |
| Identified by | `Authorization: Bearer <token>` | `setup_authentication` succeeding |
| Governed by | The token's own grant matrix | The read-only default list |
| Writes | Allowed (if granted) | Never |
| Pundit policies | Row-scoping **OFF** — the grant matrix is authoritative | **On** — your `Scope`/policy methods still apply on top of the grant |
| File URLs | Signed & expiring | Standard attachment URL |

Pick **tokens** for external clients (governed purely by grants) and the **code hook** for trusted internal integrations (which keep your existing Pundit policies). Your Pundit setup is the **avo-authorization** skill; the code-auth path needs a working `current_user` (**avo-authentication**).

## Gotchas

Lead with the security-critical ones — they fail silently or fail open:

- **Mount `mount_avo_api` OUTSIDE / before any `authenticate :user do … end` block.** Inside it, the API inherits your web-session guard and token-based access breaks for external clients. Mount the API first, then the authenticated `mount_avo`. (This does not make the API unauthenticated — it authenticates itself via tokens / the code hook.)
- **The token pepper is REQUIRED and fails closed.** Until `avo_api.token_pepper` (credentials) or `AVO_API_TOKEN_PEPPER` (ENV) is set, token creation **and** authentication **raise**. And **changing it invalidates every existing token** — set it once and keep it stable, like a signing key.
- **Closed by default — grants are opt-in from zero.** No token / no override ⇒ `401`. A valid token with **no grants** ⇒ `403` on every resource. You must grant `resource × verb` per token (and enable `manage_tokens_if`, which defaults to deny). "My token 401s / 403s everywhere" is almost always the pepper, `manage_tokens_if`, or missing grants — not the client.
- **A malformed/invalid Bearer token is a hard `401` — it never falls through to the code hook.** Don't expect an expired token to silently degrade to your HTTP-Basic scheme; a present-but-bad `Bearer` is rejected outright.
- **The two auth paths authorize differently.** Token requests are governed **purely** by the grant matrix with Pundit row-scoping **off** and writes allowed; code-auth requests keep Pundit **and** draw only from the read-only default list (no writes). Don't assume your Pundit `Scope` filters a **token** response — it doesn't.
- **Association keys are omitted when the actor can't read the target.** The response never emits a foreign key or the existence of an ungranted related record — a `belongs_to`/`has_many` key simply disappears rather than returning `{id: …}`. Grant `index`/`show` on the **target** resource to make traversal and association keys appear.
- **A controller inheriting a plain `ActionController` is a full, unauthenticated, ungated bypass.** Custom API controllers must subclass `BaseResourcesController` to keep authentication and the permission gate. Inheriting a bare `ActionController` is a deliberate public escape hatch — use it only when you truly mean "public, unauthenticated, ungated," and never by accident.
- **Writes require a token, always.** The default (code-auth) list is read-only by design; even a granted `create`/`update`/`destroy` there is refused. If an integration must write, issue a Bearer token.
- **Verify before writing.** Option names, paths, and serialization shapes drift between versions — check the docs URLs above or the app's installed `avo-api` source rather than trusting memory.

## Report

When done, tell the user:

- **Files touched** (full paths): `Gemfile`, `config/routes.rb`, `config/initializers/avo.rb`, the copied migration, any credentials/ENV change, and any generated controller under `app/controllers/avo/api/resources/v1/` — plus the generator command(s) run.
- **The mount** shape and resulting base URL (`/api`, a custom path, or a subdomain), and an explicit confirmation it sits **outside** any `authenticate` block.
- **Prerequisites still owed by the user:** the `avohq.io/addons/json-api` license (paid add-on), the gem-server token to bundle (**avo-setup**), the **token pepper** (creation/auth fail closed until it's set), and enabling `manage_tokens_if` so someone can mint tokens.
- **Which auth path** you set up (Bearer tokens vs a `setup_authentication` code hook) and, for the code path, that it keeps Pundit (**avo-authorization**) and needs a working `current_user` (**avo-authentication**).
- **The permission model:** that it's opt-in from zero, which grants a client needs (`resource × verb`), that a token with no grants is `403` everywhere, and that writes require a token (the default list is read-only).
- Any **custom controller** overrides you added (auth, CSRF, serialization) and the fields/views that shape the response.
