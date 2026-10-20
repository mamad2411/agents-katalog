# Margin Notes

Margin Notes is a full-stack Rails reading-notebook application. Signed-in readers
keep private notebooks of rich-text notes with a searchable list. Develop only the
requested feature. Guide examples illustrate conventions, not a feature backlog.

## Read for the work at hand

- Read [ARCHITECTURE.md](ARCHITECTURE.md) before choosing where behavior belongs.
- Use [CONTRIBUTING.md](CONTRIBUTING.md) for setup, the development loop, and delivery.
- Read [TESTING.md](TESTING.md) when adding or changing behavior or tests.
- Read the relevant [controller](docs/guides/controllers.md),
  [model](docs/guides/models.md), and [view](docs/guides/views.md) guides for those
  layers. Read [fixtures](docs/guides/fixtures.md) when changing shared test data.
- Examples come from public Fizzy source. The [source notes](docs/references/fizzy.md)
  identify their versions, adaptations, and limits. Local code and locked
  dependencies determine what works here.

## Development rules

- Extend the closest existing Rails pattern before introducing a new abstraction.
  Put domain decisions in models. Controllers handle HTTP, and views present results.
- Implement ordinary user behavior end to end. Keep domain decisions testable
  without a browser, and verify request and browser behavior at their own boundaries.
- Keep the dependency versions and framework defaults in place unless the task
  authorizes changing them. Do not add libraries simply because an example uses them.
- Update guidance when a decision changes. Distinguish existing behavior from a
  proposed design and do not document unimplemented features as available.

## Commands

Run commands from the repository root with its Ruby version active. Database
preparation writes to the configured databases. See [TESTING.md](TESTING.md) for
test requirements and focused commands.

```sh
bundle check
bin/rails db:prepare
bin/rails server
bin/rails zeitwerk:check
bin/rails test
bin/rails test:system
```

The browser suite runs separately from `bin/rails test`. There is currently no
`bin/ci` or configured linter.

## Task skills

- Load [writing-rails-controllers](.claude/skills/writing-rails-controllers/SKILL.md)
  for routes, controllers, HTTP behavior, and request tests.
- Load [writing-rails-models](.claude/skills/writing-rails-models/SKILL.md)
  for persistence, domain objects, concerns, queries, and model tests.
- Load [writing-rails-views](.claude/skills/writing-rails-views/SKILL.md)
  for ERB, forms, Turbo, Stimulus, Jbuilder, and rendered-output tests.

Use more than one skill when a feature crosses layers. Skills point to the same
guides as this file, not a separate set of conventions.
