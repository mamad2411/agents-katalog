---
name: avo-http-resource
description: Back an Avo resource with an external HTTP/REST API instead of an Active Record model — list, show, create, update, and delete records straight through the API with no database table, via `self.http_adapter`. Use when the user wants to build an admin panel for an external/third-party/SaaS REST API, show records that come from an API rather than the database, CRUD a remote service through Avo with no local table, map Avo's sort/filter UI to API query params, send auth headers on every request, parse a wrapped JSON response (results/meta/data), surface API failures with `Avo::HttpError`, customize create/update/destroy against a bespoke API, obfuscate record ids in URLs, or debug exactly what a resource sends and receives through the HTTP debug console. Paid add-on gem (`avo-http_resource`), Open Beta.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch
---

# Avo HTTP Resource

An **HTTP Resource** is an Avo resource whose records live behind an external HTTP endpoint instead of an Active Record model. Point it at an API and Avo lists, shows, creates, updates, and deletes records through that API — no database table, no model, no migration. The class inherits from `Avo::Core::Resources::Http` (not `Avo::BaseResource`), its paired controller inherits from `Avo::Core::Controllers::Http`, and a single `self.http_adapter` hash tells Avo where the endpoint is and how to read the JSON it returns.

Everything **inside** the resource — `def fields`, the field DSL, title/description/icon, filters, actions — works exactly as it does for a database-backed resource. Only the data source changes. So this skill covers the `http_adapter` and the API-specific plumbing; for the resource/field DSL itself, defer to the sibling **avo-resources** skill (and avo-fields / avo-associations) rather than re-deriving it here. Because it's a separate paid gem pulled from Avo's private gem server, the install/auth mechanics are shared with the **avo-setup** skill.

## Docs

Authoritative docs — fetch on demand rather than guessing, and verify every adapter key against the docs or the app's installed `avo-http_resource` source before writing it:

- Docs map (start here to discover pages): https://docs.avohq.io/4.0/docs-map.md
- HTTP Resource guide: https://docs.avohq.io/4.0/http-resource.md — API reference (`http_adapter` keys, types, defaults): https://docs.avohq.io/4.0/http-resource-api.md
- Resource/field DSL that HTTP resources reuse: https://docs.avohq.io/4.0/resources.md

## Install

The HTTP Resource ships as a **separate paid add-on gem** (`avo-http_resource`), currently in **Open Beta**. It is pulled from Avo's private gem server, so the app must already have gem-server auth configured — if `bundle` 403s on the gem, that's the **avo-setup** skill's territory (token / `BUNDLE_PACKAGER__DEV`).

```ruby
# Gemfile
gem "avo-http_resource", source: "https://packager.dev/avo-hq/"
```

Then `bundle install`. Once installed, the resource generator gains a `--http` flag and HTTP resources become a new resource type.

## When this applies

**Explicit (Avo / HTTP resource named):** "generate an HTTP resource", "back this resource with an API", "use `self.http_adapter`", "add an HTTP resource for the OpenAlex/Stripe/etc. API", "map Avo sorting to the API", "open the HTTP resource debug console".

**Implicit (no mention of Avo internals):** "build an admin panel for our external REST API", "show records that come from a third-party API, not our database", "manage data from a SaaS/third-party API inside the admin", "CRUD an external service through the admin — there's no table for it", "our data lives in another service's API, expose it in the admin", "let admins edit records that are stored in [external system]".

If the records **do** live in a local table, this is a normal resource — use **avo-resources**. If the data is a small static in-memory list, that's an array resource (also avo-resources). Reach for an HTTP resource specifically when each index/show/create/update/delete should become a live request to a remote API.

## Workflow

### 1. Confirm the gem and gem-server auth

HTTP resources need `avo-http_resource` in the Gemfile (see **Install**). Add it if it's missing; if `bundle` can't fetch it (403/`Forbidden`), fix the gem-server token first via **avo-setup** — don't work around it.

### 2. Generate the resource (and its controller)

```bash
bin/rails generate avo:resource Author --http
```

That writes `app/avo/resources/author.rb` (inheriting from `Avo::Core::Resources::Http`) plus its paired controller `app/controllers/avo/authors_controller.rb` (inheriting from `Avo::Core::Controllers::Http`). As with any resource, **a missing controller raises `ActionDispatch::MissingController`** on open — see avo-resources.

### 3. Configure the adapter (endpoint + response parsing)

With only `endpoint` set, Avo assumes the response body *is* the collection (index) or the record (show), and reads the total count from `response["total"]`. Most real APIs wrap their payload, so add the parse procs to point Avo at the right keys:

```ruby
# app/avo/resources/author.rb
class Avo::Resources::Author < Avo::Core::Resources::Http
  self.http_adapter = {
    endpoint: "https://api.openalex.org/authors",
    parse_collection: -> { response["results"] },   # index → Array of records
    parse_record: -> { response },                  # show  → one record
    parse_count: -> { response["meta"]["count"] }   # pagination total
  }

  def fields
    field :id, as: :id
    field :display_name
  end
end
```

Avo derives every HTTP verb from `endpoint`:

| Operation | Request |
| --- | --- |
| Index | `GET endpoint?page=…&per_page=…` |
| Show | `GET endpoint/:id` |
| Create | `POST endpoint` |
| Update | `PATCH endpoint/:id` |
| Destroy | `DELETE endpoint/:id` |

The three parse procs run in an `Avo::ExecutionContext`, so inside them you have `raw_response` (the `HTTParty::Response`), `response` (the parsed body, i.e. `raw_response.parsed_response`), and `headers` (the response headers). Use them to dig into nested payloads or inspect status codes.

### 4. Send authentication headers

`headers` is sent with every request. Pass a Hash, or a **proc** returning a Hash when the value must be computed per request (rotating tokens, per-user credentials):

```ruby
self.http_adapter = {
  endpoint: "https://api.openalex.org/authors",
  headers: {
    "Authorization" => "Bearer #{ENV.fetch("API_KEY")}"
  }
}
```

### 5. Map Avo's sort/filter UI to query params

`query_params` is a proc whose returned Hash is merged into the index request's query string, on top of the built-in `page`/`per_page`. It has access to controller `params`, so it's where you translate Avo's sorting/filtering into whatever the API expects:

```ruby
self.http_adapter = {
  endpoint: "https://api.openalex.org/authors",
  query_params: -> {
    if params[:sort_by].present? && params[:sort_direction].present?
      { sort: "#{params[:sort_by]}:#{params[:sort_direction]}" }
    else
      {}
    end
  }
}
```

(The legacy key `sort_params` is still honored as an alias — use `query_params` in new code.)

### 6. Surface API errors

When the API returns an error payload, raise `Avo::HttpError` from inside any parse proc. The controller rescues it and shows the message as a flash error instead of a broken page:

```ruby
parse_collection: -> {
  raise Avo::HttpError.new(response["message"]) if response["error"].present?
  response["results"]
}
```

### 7. Customize create / update / destroy (in the controller)

Out of the box the controller persists through the resource's client — `POST endpoint` on create, `PATCH endpoint/:id` on update, `DELETE endpoint/:id` on destroy. Override in the paired controller when the API needs different paths, extra params, or conditional logic. `save_record` must return a **boolean** (did it succeed?), and you tell create from update by inspecting `action_name`:

```ruby
# app/controllers/avo/authors_controller.rb
class Avo::AuthorsController < Avo::Core::Controllers::Http
  def save_record
    auth_headers = { "Authorization" => "Bearer #{ENV.fetch("API_KEY")}" }

    response = if action_name == "create"
      MyCustomApi.post("/authors", body: @record.as_json, headers: auth_headers)
    else # "update"
      MyCustomApi.patch("/authors/#{@record.id}", body: @record.as_json, headers: auth_headers)
    end

    response.success?
  end

  # def destroy_model
  #   @resource.client.delete(@record.id)
  # end
end
```

### 8. Customize the backing model (`model_class_eval`)

Avo builds a throwaway `ActiveModel` class behind each HTTP resource. `model_class_eval` is `instance_exec`'d **in that class body** to add behavior — most often obfuscating the id used in URLs:

```ruby
self.http_adapter = {
  endpoint: "https://api.openalex.org/authors",
  model_class_eval: -> {
    define_method :to_param do
      Base64.encode64(id)
    end
  }
}
```

It runs at class-definition time, so `response` / `raw_response` / `headers` are **not** available inside it.

### 9. Debug what the resource sends and receives

HTTP resources ship an interactive debug console at `<avo_root>/http-resource/debug` (e.g. `/avo/http-resource/debug`). Pick a resource and an action (`index`, `show`, `count`, `create`, `update`, `delete`) and fire it; it shows the sent URL, query params, masked request headers, raw vs. parsed response, request timing, and the output of each `parse_*` block, with per-stage errors so a broken adapter never crashes the page.

Same diagnostics as JSON for scripting or agent use: `POST <avo_root>/http-resource/debug/run.json` with `resource`, `probe_action`, `id`, `page`, `limit`, `query`, `body`, `confirm`. **Write actions (`create`/`update`/`delete`) hit the real API and require `confirm=1`.**

To surface the console in the sidebar's **Tools** section, add a partial at `app/views/avo/sidebar/items/_http_resource_debugger.html.erb`:

```erb
<%= render Avo::Sidebar::LinkComponent.new(
  label: "HTTP debugger",
  path: File.join(avo.root_path, "http-resource", "debug"),
  icon: "tabler/outline/api"
) %>
```

## `http_adapter` keys

| Key | Does | Type / default |
| --- | --- | --- |
| `endpoint` | Base URL; every verb is derived from it | String, verbatim. Default `nil` |
| `headers` | Sent on every request (auth, etc.) | Hash **or** proc → Hash. Default `{}` |
| `query_params` | Extra index query params (map sort/filter) | Proc → Hash. Default `-> { {} }` (alias: `sort_params`) |
| `parse_collection` | Array of records from the index response | Proc → Array. Default `-> { response }` |
| `parse_record` | One record from the show response | Proc → Hash. Default `-> { response }` |
| `parse_count` | Total record count for pagination | Proc → Integer. Default `-> { response["total"] }` |
| `model_class_eval` | Extend the generated ActiveModel class | Proc (`instance_exec`'d in the class). Default `-> {}` |

Controller override points: `save_record` (return a boolean; branch on `action_name` `"create"`/`"update"`) and `destroy_model`.

## Gotchas

- **Separate paid gem, Open Beta.** It's `avo-http_resource` from `https://packager.dev/avo-hq/`, not part of core Avo, and the feature is in Open Beta — expect rough edges and pin/verify against the installed source. If `bundle` 403s, that's gem-server auth (**avo-setup**).
- **Inherit from the right classes.** Resource → `Avo::Core::Resources::Http`; controller → `Avo::Core::Controllers::Http`. Generate with `--http` so both are wired; a hand-written resource still needs its controller or you'll hit `ActionDispatch::MissingController`.
- **`endpoint` is a plain String, used verbatim.** Unlike every other adapter key, it is **not** a proc and is **not** run through `Avo::ExecutionContext`. You can't compute it per-request; put per-request variation in `query_params`/`headers`, or override the controller methods.
- **The index always sends `page` and `per_page`.** The parameter names aren't configurable — add anything else via `query_params`. Requests **time out after 10 seconds** and raise.
- **Defaults assume an unwrapped body.** `parse_collection`/`parse_record` default to the *whole* response body; `parse_count` defaults to `response["total"]`. If the API wraps data (`results`, `data`, `meta.count`, …), you must set the parse procs or the index/count silently breaks.
- **`model_class_eval` has no response access.** It runs in the generated model's class body, not the request/response context — `response`, `raw_response`, `headers` are unavailable there. Read the response only inside the parse procs / controller.
- **`save_record` must return a boolean.** A truthy non-boolean or a raised error won't be treated as "saved". Check `response.success?` (or equivalent) and return that; use `action_name` to distinguish create from update.
- **The debug console's write actions hit the REAL API.** `create`/`update`/`delete` from the console (and the `.json` endpoint) actually POST/PATCH/DELETE to the live service — they require explicit confirmation (`confirm=1` for JSON). It's gated behind the license feature + Avo's developer/admin access, and it only lists/runs resources the current user's **authorization policy** allows (see the avo-authorization skill).
- **Don't re-invent the resource DSL here.** Fields, title/icon, filters, actions all behave as usual — that's the **avo-resources** / avo-fields / avo-associations skills. This skill is only the HTTP adapter and its controller.
- **Verify before writing.** Adapter key names and defaults can drift during Open Beta — check the API reference URL above or the app's installed `avo-http_resource` source rather than trusting memory.

## Report

When done, tell the user:

- The resource file and controller file you created or edited (full paths) and the generator command run (`bin/rails g avo:resource <Name> --http`).
- The API it targets: `endpoint`, and which `parse_collection` / `parse_record` / `parse_count` you set (and why, e.g. "the API wraps records under `results` and the count under `meta.count`").
- Any auth (`headers`), sort/filter mapping (`query_params`), error handling (`Avo::HttpError`), custom `save_record`/`destroy_model`, or `model_class_eval` you added.
- Anything still needed: add `avo-http_resource` to the Gemfile and `bundle` (fix gem-server auth via avo-setup if it 403s), define the `fields` (avo-resources/avo-fields), add an authorization policy if authorization is enabled, and set `API_KEY`/other ENV the adapter reads.
- Flag that this is a **paid, Open Beta** add-on, and remind them the debug console's create/update/delete hit the real external API.
