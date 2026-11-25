---
name: exec-ruby
description: Ruby execution idioms to embed into Codex prompts when the target project is Ruby — idiomatic style, error handling, and Rails conventions when present.
---

# Ruby Idioms (embed when project is Ruby)

```
Ruby standards:
- Follow the community style guide / the repo's RuboCop config: snake_case methods/vars, CamelCase
  classes, SCREAMING_SNAKE constants; two-space indent; guard clauses over nested conditionals.
- Errors: raise specific StandardError subclasses with messages; rescue the narrowest class you can
  handle; never rescue Exception broadly; use ensure for cleanup; avoid rescue => e that swallows.
- Prefer expressive enumerables (map/select/reduce/each_with_object) over manual loops; use safe
  navigation (&.) and fetch with defaults over silent nil; freeze constants and string literals
  where the project does (# frozen_string_literal: true).
- Keep methods short and single-purpose; extract private methods; avoid mutating shared state and
  method args unless the API intends it (bang methods signal mutation).
- Rails (if present): use its idioms — strong params, validations and scopes on models, avoid N+1
  with includes/eager_load, service objects for complex logic, migrations for schema. Never
  interpolate input into SQL — use the query interface or parameterized where.
- Add gems only via the Gemfile; respect the existing dependency and load-path conventions.
- Tests: RSpec or Minitest to match the repo; describe/context/it with behavior-focused names;
  arrange-act-assert; use factories/fixtures the project already uses.
```
