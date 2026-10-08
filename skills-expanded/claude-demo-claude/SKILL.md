# Project conventions

The facts Claude can't infer from the code. Keep it short — replace the
placeholders below with your project's specifics.

## Stack
- <language / framework + versions>
- <datastore, key libraries, anything non-obvious>

## Canonical build & test commands
> These live HERE (not only in a skill) so the project builds for anyone —
> including contributors without the shared plugins.

- Build:     `<your build command>`
- Test:      `<your test command>`
- Lint:      `<your lint command>`
- Local dev: `<how to run the app locally>`

## Conventions
- <house rules Claude should always follow — error handling, API versioning, …>
- Never edit generated code or existing migrations — add a new one.

## Gotchas
- <non-obvious things that bite newcomers>

## Workflow
- Work on a feature branch and open a PR. `main` is protected: no direct
  pushes, no force-push, no deletion. CI must pass before merge.
