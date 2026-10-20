---
name: ruby-security
description: "When to activate: Rails security, strong parameters, CSRF protect_from_forgery, SQL injection ActiveRecord, XSS raw html_safe, Rails credentials, mass assignment, params.permit, Ruby security"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: ruby
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Ruby & Rails Security Patterns

## When to Use

Reviewing or writing Rails code that handles user input, renders untrusted content, executes raw SQL, or manages secrets/credentials.

## Core Patterns

### Strong Parameters Against Mass Assignment

```ruby
# BAD: permits everything the client sends, including admin/role fields
def user_params
  params.require(:user).permit!
end

# GOOD: explicit allow-list
def user_params
  params.require(:user).permit(:name, :email, :password)
end
```

Never allow `is_admin`, `role`, or similarly privileged attributes through `permit` unless the current user is authorized to set them, and even then, handle that assignment separately from the general update path.

### SQL Injection via ActiveRecord

```ruby
# BAD: string interpolation builds raw SQL
User.where("email = '#{params[:email]}'")

# GOOD: parameter binding, positional or named
User.where("email = ?", params[:email])
User.where(email: params[:email])
```

`where(column: value)` is always safe. The risk appears specifically when a raw SQL fragment string is built with interpolation — a common mistake with `order()`, `pluck()`, and raw `find_by_sql`.

```ruby
# BAD: interpolated column name in order() — injectable
Order.order("#{params[:sort_column]} #{params[:direction]}")

# GOOD: validate against an allow-list before interpolating
ALLOWED_SORT_COLUMNS = %w[created_at total_cents status].freeze
column = ALLOWED_SORT_COLUMNS.include?(params[:sort_column]) ? params[:sort_column] : "created_at"
Order.order(column => params[:direction] == "desc" ? :desc : :asc)
```

### CSRF Protection

```ruby
class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
end
```

API-only controllers authenticating via tokens (not cookies/sessions) can skip CSRF for those actions — but any controller that authenticates via session cookies must keep it enabled.

### XSS: raw / html_safe Are Escape Hatches, Not Defaults

```erb
<%# GOOD: auto-escaped by default %>
<p><%= comment.body %></p>

<%# DANGEROUS: bypasses escaping entirely %>
<div><%= raw comment.body %></div>
<div><%= comment.body.html_safe %></div>
```

Calling `.html_safe` on a string doesn't sanitize it — it's a promise to Rails that the string is *already* safe. Never call it on unsanitized user input. If you must render user-authored HTML, run it through a sanitizer first (`sanitize()` with an explicit allow-list, or a library like Loofah).

### Secrets Management

```ruby
# BAD: hardcoded secret committed to the repo
STRIPE_SECRET = "sk_live_abc123"

# GOOD: Rails encrypted credentials, decrypted at boot from a key not in git
Rails.application.credentials.stripe[:secret_key]

# GOOD: environment variable, for 12-factor deployments
ENV.fetch("STRIPE_SECRET_KEY")
```

`config/master.key` (or `RAILS_MASTER_KEY`) must never be committed — it decrypts `credentials.yml.enc`. Rotate immediately if it's ever exposed.

### Authorization, Not Just Authentication

```ruby
# BAD: only checks that *someone* is logged in, not that they own the resource
def show
  @order = Order.find(params[:id])
end

# GOOD: explicit ownership/policy check
def show
  @order = current_user.orders.find(params[:id])
  # or: authorize @order  (Pundit)
end
```

## Checklist

- [ ] No controller uses `params.permit!`
- [ ] All raw SQL fragments use `?`/named bindings, never string interpolation
- [ ] Dynamic `order()`/`pluck()` column names validated against an allow-list
- [ ] `protect_from_forgery` enabled on any session/cookie-authenticated controller
- [ ] `raw`/`html_safe` never applied to unsanitized user input
- [ ] Secrets loaded via `Rails.application.credentials` or `ENV`, never hardcoded
- [ ] Every action that loads a record scopes it to the current user/authorized resource, not `Model.find(params[:id])` unscoped

## Quick Reference

| Risk | Mitigation |
|---|---|
| Mass assignment | Strong Parameters (explicit `permit` list) |
| SQL injection | Parameter binding; allow-list dynamic column/order names |
| CSRF | `protect_from_forgery with: :exception` |
| XSS | Default ERB escaping; sanitize before `raw`/`html_safe` |
| Leaked secrets | `Rails.application.credentials` / `ENV`, never hardcoded |
| Insecure direct object reference | Scope queries to `current_user`, use Pundit/CanCanCan policies |

## See Also

- `skills/ruby-ecosystem/rails-patterns.md`
- `skills/ruby-ecosystem/ruby-database.md`
- `skills/security/owasp-checklist.md`
