---
name: rails-security
description: Rails security review — Brakeman integration, mass-assignment via strong_parameters, SQL injection in ActiveRecord, template injection via html_safe/raw, Devise hardening, credentials.yml.enc, force_ssl and CSP config, recent Rails/Rack CVE patterns.
---

# Rails Security

## When to use

This skill is the Rails-specific layer on top of `secure-coding`. Convention over configuration covers a lot, but anyone going against the grain (string interpolation in `.where`, `.html_safe` on user input, CSRF off because "it was hard") gets vulnerabilities back.

Triggers on:

- A question like "review this Rails app", "Brakeman triage", "Devise hardening", "mass-assignment check", "is our CSP OK", "force SSL".
- Presence of `Gemfile`, `config/application.rb`, `config/environments/production.rb`, `config/routes.rb`, Devise setup under `config/initializers/devise.rb`, Pundit/CanCanCan policies.
- A PR that touches `html_safe`, `raw`, `.where("... #{x} ...")`, `skip_before_action :verify_authenticity_token`, or `skip_forgery_protection`.
- A Brakeman report that needs triaging.
- A handoff from `security-review` where Rails is in the stack.

### When NOT (handoff)

- General Ruby secure-coding → `secure-coding`.
- API design (Rails API-only mode overlaps with `api-security`) → that skill for OWASP API Top 10, here for Rails-specific implementation.
- SAST tool orchestration → `sast-orchestrator`. Brakeman is Rails-specific and belongs here.
- Dep vulns in gems → `cve-triage` (via `bundle audit` or OSV-scanner).
- Container/K8s deploy → `container-hardening` / `k8s-security`.
- Secrets in `config/master.key` or `credentials.yml.enc` on disk → `secrets-scanner`. This skill only covers the Rails credentials model.

## Approach

Six phases. Brakeman does the heavy static-analysis lifting; this skill adds human context to what Brakeman outputs and catches what it misses.

### 1. Brakeman and dependency scanning

**Brakeman** (OSS, Rails-specific, since 2011). Static analysis that knows Rails idioms. Default tool for this skill.

```bash
bundle add brakeman --group=development
bundle exec brakeman --no-pager -o brakeman-report.json -f json
```

CI integration via the Brakeman action or plain `bundle exec brakeman --exit-on-warn`. Fail on new warnings via a baseline workflow (`--compare` against a previous run).

Triage Brakeman warnings with the same discipline as `sast-orchestrator` phase 5: baseline at introduction, suppress with rule ID plus reason (`ignore.json`), revisit periodically.

**bundler-audit** (OSS) for Gemfile.lock vulns; pass results on to `cve-triage`. Dependabot/Renovate for auto-updates.

### 2. Mass-assignment and strong_parameters

The classic Rails vulnerability. Pre-Rails-4 the whitelist was opt-in; since then it has been required via `strong_parameters`.

- **Controller idiom**: `params.require(:user).permit(:name, :email)`. Only those fields are accepted by `@user.update(user_params)`.
- **Foot-gun**: `params.require(:user).permit!` — the bang variant permits everything, effectively mass-assignment without a whitelist. Search for `.permit!` in every review.
- **Nested attributes**: `permit(addresses_attributes: [:street, :city])` — explicit per level.
- **Polymorphic / hash-type input**: `permit(preferences: {})` is an empty whitelist and accepts an entire hash without key checking. Limit to known keys.
- **Admin flags never in permit**: `is_admin`, `role`, `stripe_customer_id` — hardcode in the controller, do not allow via params.

### 3. SQL injection in ActiveRecord

ActiveRecord parameterizes via hash syntax and positional placeholders. Issues arise with string interpolation.

Safe (all parameterized):

```ruby
User.where(name: name)
User.where("name = ?", name)
User.where("name = :n AND age > :a", n: name, a: 18)
```

Unsafe:

```ruby
User.where("name = '#{name}'")          # string interpolation
User.where("name = '" + name + "'")     # concatenation
User.order(params[:sort])               # order-by user input = vulnerable
User.find_by_sql("SELECT ... #{query}") # raw SQL
```

Specific sub-patterns:

- **`order(params[:sort])`** — allowlist of permitted column names. `User.order(params[:sort].presence_in(%w[name created_at]) || :id)`.
- **`group(...)`, `having(...)`, `pluck(...)`** — accept string fragments; do not compose from user input.
- **`sanitize_sql_array`/`sanitize_sql_like`** for cases where you really do need raw SQL.
- **`find_by_sql`, `connection.execute`** — always parameterized; Brakeman catches this.

### 4. XSS and template escape

Rails escapes by default in ERB (`<%= %>`). XSS arises where you opt out.

- **`raw(user_input)`** — renders raw, no escaping.
- **`<%= user_input.html_safe %>`** — same effect, method on string.
- **`safe_concat`, `content_tag(..., user_input)`** with `escape: false` — variants.
- **`sanitize(user_html, tags: ..., attributes: ...)`** — Rails' built-in HTML sanitizer; acceptable for user-generated HTML provided the allowlist is tight. Refer to the Rails docs for the default allowlist.
- **`javascript_tag do ... end`** with user input in the body — JS-context XSS, not covered by HTML escape.
- **Custom helpers** that return `html_safe` are a common bug source. `def my_helper(input); "<b>#{input}</b>".html_safe; end` is broken if `input` is user input. Fix: `content_tag(:b, input)`.

### 5. Auth: Devise, CSRF, sessions, CSP

- **CSRF**: `protect_from_forgery with: :exception` (default since Rails 5.2). `skip_before_action :verify_authenticity_token` is a security-review trigger. API controllers extending `ActionController::API` do not need CSRF (stateless); mixed controllers (web + JSON) do.
- **Devise hardening**:
  - Modules: `:database_authenticatable`, `:registerable`, `:recoverable`, `:rememberable`, `:validatable`. Turn on `:confirmable` for email verification, `:lockable` for brute-force mitigation, `:timeoutable` for inactive sessions.
  - Password hashing: Devise uses bcrypt; stretches >= 12 for prod.
  - `devise-two-factor` for TOTP MFA.
  - Password reset flow: verify the token is time-bound (`reset_password_within` reasonably short) and enumeration-safe (same response for existing/non-existing email).
- **Session config**: `config.session_store :cookie_store, key: '_app_session', secure: Rails.env.production?, httponly: true, same_site: :lax`. `expire_after` reasonable (e.g. 2 hours of inactivity).
- **Content Security Policy**: since Rails 5.2 via `config/initializers/content_security_policy.rb`. Build the default policy without `'unsafe-inline'` or `'unsafe-eval'`; nonce-based if inline is needed.
- **`force_ssl`**: `config.force_ssl = true` in production.rb. Or at the reverse-proxy level, not both redundantly.

### 6. CVE patterns and verification-loop

Rails/Rack CVEs to know:

- **CVE-2019-5418 ActionView file disclosure** — Accept-header-based path traversal. Historical but canonical; every Rails version <5.2.2.1 / 4.2.11.1 is vulnerable. Reviewer reflex: is the Rails version recent enough?
- **CVE-2022-32224 ActiveRecord YAML deserialization RCE** — via `serialize :column`. Fixed in 5.2.8.1, 6.0.5.1, 6.1.6.1, 7.0.3.1. Search code for `serialize :col` without a type argument; that triggers the legacy YAML path.
- **CVE-2023-22795 ActionDispatch ReDoS** — header-parsing regex DoS.
- **Rack 3.x security stream (2024)** — multiple CVEs in Rack's request parser. `[verify against https://github.com/rack/rack/security/advisories]` for current status.
- **Other**: `[verify against https://rubyonrails.org/security/]` for Rails-specific, `[verify against https://github.com/rack/rack/security/advisories]` for Rack.

File uploads and Active Storage:

- `has_one_attached :avatar` — content type is stored via `content_type` on the blob, but the MIME check on upload is the controller's responsibility. Use `validates :avatar, content_type: [...]` via the `active_storage_validations` gem.
- **Variants** with the `ImageMagick` backend: a CVE-intensive library. Prefer `vips` as the backend.
- **Private storage** for non-public files (`ActiveStorage::Current.url_options`); do not share blob URLs directly without a signed URL plus expiry.

Verification-loop: Layer 1 scope (Gemfile versions, production.rb settings, routes + controller permits all walked through?), assumptions (`protect_from_forgery` active on all web controllers?). Layer 2 (CVE IDs verified against rubyonrails.org/security, Brakeman rule IDs are real, no invented Devise modules).

## Output

```
Rails security review — <app>
Rails: <x.y.z> | Ruby: <x.y.z> | Gems with vuln: <N via cve-triage>

Brakeman:
  Warnings total:       N (baseline: M, new: K)
  High-confidence:      <list>
  Grouped by class

Code patterns:
  skip_before_action :verify_authenticity_token: <list>
  .permit!, mass-assignment risks:                <list>
  String interpolation in .where/.order:          <list>
  html_safe/raw on user input:                    <list>

Devise:
  Modules present:      <confirmable, lockable, timeoutable?>
  MFA active:           <devise-two-factor | none>
  stretches:            <N>
  enumeration-safe:     <yes/no on reset flow>

Deploy settings:
  config.force_ssl:     <true | false>
  session-cookie flags: <secure, httponly, same_site>
  CSP:                  <default policy, no unsafe-inline?>

Active Storage (if applicable):
  MIME validation:      <present | missing>
  ImageMagick vs vips:  <backend>

Version check:
  Rails security releases:  <current | N months behind>
  Rack CVE scope:           <verified>

Findings (severity-sorted, follow security-review format)
Verification-loop: ...
```

## References

- Rails Security Guide — [https://guides.rubyonrails.org/security.html](https://guides.rubyonrails.org/security.html). Official security guide, maintained with core-team input.
- Rails Security Announcements — [https://rubyonrails.org/security/](https://rubyonrails.org/security/). CVE feed.
- Brakeman — [https://brakemanscanner.org/](https://brakemanscanner.org/). Rails-specific SAST.
- bundler-audit — [https://github.com/rubysec/bundler-audit](https://github.com/rubysec/bundler-audit). Gemfile.lock dep-CVE scan.
- Devise — [https://github.com/heartcombo/devise](https://github.com/heartcombo/devise) and [https://github.com/devise-security/devise-security](https://github.com/devise-security/devise-security) for extra modules.
- Active Storage Validations — [https://github.com/igorkasyanchuk/active_storage_validations](https://github.com/igorkasyanchuk/active_storage_validations). MIME/size checks that AS itself does not do.
- Rack Security Advisories — [https://github.com/rack/rack/security/advisories](https://github.com/rack/rack/security/advisories). Rack touches every Rails app directly.
- OWASP Ruby on Rails Cheat Sheet — [https://cheatsheetseries.owasp.org/cheatsheets/Ruby_on_Rails_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Ruby_on_Rails_Cheat_Sheet.html).

## Categories

- appsec
