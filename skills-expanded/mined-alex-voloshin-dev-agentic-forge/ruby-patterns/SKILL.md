---
name: ruby-patterns
description: Ruby stack conventions agentic-forge applies when the detected stack is Ruby — the toolchain (bundler, RSpec/Minitest, RuboCop), idiomatic Ruby and error handling, testing discipline, layout, and the high-value Ruby pitfalls. Loaded on demand by develop / code-review and the software-engineer / qa-engineer roles after stack detection; kept off the always-on listing.
disable-model-invocation: true
---

# Ruby patterns

The Ruby stack pack: loaded by the `software-engineer` / `qa-engineer` roles (and the
`code-review` lint aspect) when `stacks.detect` reports Ruby. It carries only what is
**Ruby-specific** on top of [`engineering-standards`](../engineering-standards/SKILL.md).
(Mechanism: ADR 0015, by-stack detection + reference packs.)

## Toolchain

**Prefer the repo's own commands** — the `Rakefile`, `bin/` scripts, and CI; run everything
through **Bundler** (`bundle exec`). Defaults:

| Job | Conventional command | Gate |
| --- | --- | --- |
| test | `bundle exec rspec` (or `rake test` / Minitest) | green; new behaviour covered |
| lint/format | `bundle exec rubocop` | clean (no new `rubocop:disable`) |
| deps | `bundle install` / `bundle update` | `Gemfile.lock` consistent |

## Idioms

- **Blocks / `yield` / `Enumerable`** (`each`/`map`/`select`/`reduce`) over manual loops; duck
  typing; small methods with **guard clauses**.
- `attr_reader`/`attr_accessor`, **keyword arguments**, safe navigation **`&.`**, symbols for
  keys, `freeze`/`frozen_string_literal: true`.
- **Raise specific error classes** (subclass `StandardError`); follow the community style guide
  (RuboCop); keep side effects explicit.

## Testing

- **RSpec** (`describe`/`context`/`it`, `let`, `subject`) or Minitest. Cover the happy path plus
  a boundary and an **error** case. Prefer **FactoryBot** over fixtures; don't mock what you
  don't own. Deterministic — no real network/clock; never weaken or delete a test to go green.

## Pitfalls (Ruby-specific, high-value)

- **`rescue` without a class** (or `rescue Exception`) — catch the narrowest `StandardError`
  subclass; never swallow silently.
- **Monkey-patching core classes**; mutable **global/class state**; mutating a frozen string.
- **`nil` errors** (use `&.` / `fetch` with defaults); **N+1 queries** (Rails — eager-load);
  `==` vs `eql?`/`equal?`; thread-safety of shared mutable state.

## Definition of done (Ruby)

`bundle exec rubocop` is clean, `rspec`/Minitest is green with the new boundary/error cases, no
exception is swallowed, `frozen_string_literal` set, `Gemfile.lock` consistent — using the repo's
own commands where declared.
