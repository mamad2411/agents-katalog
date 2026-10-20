---
name: bundler-patterns
description: "When to activate: Bundler, Gemfile, Gemfile.lock, pessimistic version operator, bundle groups, bundle audit, gemspec, private gem sources, Ruby dependency management"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: ruby
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Bundler Patterns

## When to Use

Managing a Ruby application's gem dependencies, authoring a gem's `.gemspec`, or auditing dependencies for known vulnerabilities.

## Core Patterns

### Gemfile Structure

```ruby
source "https://rubygems.org"
ruby "3.3.0"

gem "rails", "~> 7.1.0"
gem "pg", "~> 1.5"
gem "sidekiq", "~> 7.2"

group :development, :test do
  gem "rspec-rails", "~> 6.1"
  gem "factory_bot_rails"
  gem "rubocop", require: false
end

group :test do
  gem "vcr"
  gem "webmock"
end

group :production do
  gem "rack-timeout"
end
```

### Pessimistic Version Operator

```ruby
gem "rails", "~> 7.1.0"  # allows 7.1.x, blocks 7.2.0 — pins to patch updates only
gem "rails", "~> 7.1"    # allows 7.1.x AND 7.2.x, blocks 8.0 — pins to the major
gem "pg", ">= 1.5", "< 2" # explicit range, equivalent meaning, more readable to some teams
```

`~>` ("twiddle-wakka") is the idiomatic default — it allows safe updates while blocking breaking major/minor bumps depending on how many version segments you specify.

### Lockfile Discipline

```bash
bundle install              # resolves and writes Gemfile.lock
bundle install --deployment # (legacy) or `--frozen` — fail if Gemfile.lock is out of sync
BUNDLE_FROZEN=true bundle install  # CI: never silently re-resolve
```

Always commit `Gemfile.lock` for applications — it's what guarantees the same gem versions in dev, CI, and production. Never `.gitignore` it for an app (libraries/gems are the exception).

### Bundler Groups

```ruby
# Load only what's needed per environment
Bundler.require(*Rails.groups)

# Explicitly require a subset (e.g. a Rake task that shouldn't load web-only gems)
Bundler.require(:default, :development)
```

Keep `test`-only and `development`-only gems out of the `default` group so production installs (`bundle install --without development test`) stay lean.

### Vulnerability Scanning

```bash
bundle audit check --update
```

Run in CI on every PR; fail the build on any advisory. Pair with Dependabot/Renovate for automated update PRs against the lockfile.

### Authoring a Gem (.gemspec)

```ruby
# my_gem.gemspec
Gem::Specification.new do |spec|
  spec.name          = "my_gem"
  spec.version       = MyGem::VERSION
  spec.authors       = ["Acme Inc"]
  spec.summary       = "Shared billing utilities"
  spec.files         = Dir["lib/**/*.rb"]
  spec.require_paths = ["lib"]

  spec.add_dependency "activesupport", ">= 6.1"
  spec.add_development_dependency "rspec", "~> 3.13"

  spec.required_ruby_version = ">= 3.1"
end
```

Gems declare loose dependency ranges (`>=`) rather than pinning exact versions — the *application* consuming the gem is responsible for pinning via its own `Gemfile.lock`.

### Private Gem Sources

```ruby
source "https://gems.example.com" do
  gem "acme-internal-lib"
end
```

Store credentials for private sources via `bundle config` (writes to `~/.bundle/config`, not the repo) or environment variables like `BUNDLE_GEMS__EXAMPLE__COM`.

## Checklist

- [ ] `Gemfile.lock` committed for applications
- [ ] `~>` used for version constraints instead of unpinned `gem "x"` (any version) or exact pins for everything
- [ ] Dev/test-only gems scoped to their `group`, not loaded in production
- [ ] `bundle audit` runs in CI and fails the build on advisories
- [ ] No credentials committed in `Gemfile`/`Gemfile.lock` — use `bundle config` or ENV
- [ ] Gem's `.gemspec` uses loose (`>=`) dependency ranges, not exact pins

## Quick Reference

| Task | Command |
|---|---|
| Install matching the lockfile exactly | `bundle install` (with `BUNDLE_FROZEN=true` in CI) |
| Update a single gem | `bundle update gem_name` |
| Check for known vulnerabilities | `bundle audit check --update` |
| See why a gem is required | `bundle why gem_name` |
| Install without dev/test gems | `bundle install --without development test` |

## See Also

- `skills/ruby-ecosystem/ruby-patterns.md`
- `skills/ruby-ecosystem/ruby-performance.md`
