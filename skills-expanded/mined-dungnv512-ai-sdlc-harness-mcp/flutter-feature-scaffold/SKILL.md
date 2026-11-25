---
name: flutter-feature-scaffold
description: Generate Clean Architecture folders and stub files for a new Flutter feature. MANDATORY TRIGGERS - "scaffold feature", "new feature", "create feature folder", "feature skeleton", "bootstrap feature".
allowed-tools: Read, Glob, Write, Edit, Bash
---

# Skill: flutter-feature-scaffold

> Invoked by `/scaffold-feature <slug>`
> (`.claude/commands/scaffold-feature.md`). The command is the contract
> surface; this skill is the implementation.

## When to use

User asks to create a new feature folder, scaffold a feature, or
bootstrap presentation/domain/data layers. Always invoked by
`/scaffold-feature`.

## Inputs

- `feature_slug`: `lower_snake_case` single word(s), e.g. `feed`,
  `post_composer`.

## Repo shape

This repo uses a Flutter local-package layout under `modules/`. Each
module is its own Dart package with its own `pubspec.yaml`, its own
`lib/`, and its own `test/`. See [`CLAUDE.md`](../../../CLAUDE.md)
"The Flutter app" for the current shape.

A "feature" is a coherent slice of user-visible behaviour. Small
features live inside an existing module (e.g. a new page inside
`modules/auth/lib/src/presentation/`). A large feature that will own
its own DI barrel + route table + release cadence graduates to a
new module (e.g. `modules/newsfeed/`). Ask which of the two the
user means before scaffolding.

## Steps — small feature inside an existing module

1. Confirm the target module (`modules/<module_name>/`) and the
   slug (`lower_snake_case`).
2. Refuse if `modules/<module_name>/lib/src/<slug>/` exists.
3. Create under `modules/<module_name>/lib/src/`:
   - `<slug>/data/{datasource,dto,repository}/…` (as needed)
   - `<slug>/domain/{entity,repository,usecase}/…`
   - `<slug>/presentation/{bloc,pages,widgets}/…`
4. Mirror tests at `modules/<module_name>/test/src/<slug>/…`.
5. Register any new DI in the module's `src/di/<module>_injection.dart`
   (raw `get_it` — no `injectable` annotations unless the module
   already uses them).
6. Add a route entry in `src/routes/<module>_routes.dart` if the
   feature is user-navigable.
7. If Freezed / JsonSerializable was added, run
   `dart run build_runner build --delete-conflicting-outputs` in
   the module directory.
8. Run `flutter analyze modules/<module_name>/`; block if not clean.

## Steps — new module

1. Confirm the module name (`lower_snake_case`).
2. Refuse if `modules/<module_name>/` exists.
3. Create the standard package skeleton:
   ```
   modules/<module_name>/
     pubspec.yaml               # name: <module_name>; dev dep bloc_test / mocktail
     analysis_options.yaml      # include: ../core/analysis_options.yaml (or shared)
     README.md, AGENTS.md       # follow modules/auth/ as the template
     docs/CONTEXT.md            # module-specific decisions
     lib/
       <module_name>.dart       # barrel — exports src/di, src/routes, public APIs
       src/
         data/{datasources,models,repositories}/.gitkeep
         domain/{entities,repositories,usecases}/.gitkeep
         presentation/…/.gitkeep
         di/<module_name>_injection.dart   # configure<Module>Dependencies(sl)
         routes/<module_name>_routes.dart  # list of GoRoute
     test/
       .gitkeep
   ```
4. Add `<module_name>: {path: modules/<module_name>}` to the
   root `pubspec.yaml` under `dependencies:`.
5. Wire the module into the shell:
   `configure<Module>Dependencies(sl)` in
   `lib/core/di/injection_container.dart`, and spread
   `<module_name>Routes` in `lib/config/routes/app_router.dart`.
6. Run `flutter pub get` at repo root.
7. Run `flutter analyze`; block if not clean.

## Output template

After scaffolding, emit:

```
Scaffolded modules/<module>/lib/src/<slug>/
  data/      ...
  domain/    ...
  presentation/ ...
Tests mirrored at modules/<module>/test/src/<slug>/
Codegen: OK (or SKIPPED — no @freezed / @JsonSerializable in scope)
flutter analyze: OK
Next: /implement <slug> (starts with test-first sub-step for usecase Get<Slug>)
```

## Examples

- Small feature: `feed-vote` inside `modules/newsfeed/` →
  `modules/newsfeed/lib/src/feed_vote/{data,domain,presentation}/`.
- New module: `newsfeed` → `modules/newsfeed/` scaffold + shell
  wiring.

## Anti-patterns to refuse

- Scaffolding at `lib/features/<slug>/` (the pre-modular layout —
  no longer used; see `docs/architecture/01-frontend-flutter.md`
  masthead).
- Adding an `@RoutePage` (`auto_route`) or `@module` (`injectable`)
  annotation when neither package is in the module's
  `pubspec.yaml`. The default is raw `get_it` + `go_router`.
- Creating a module without an `AGENTS.md` / `README.md` /
  `docs/CONTEXT.md` — future contributors need the module-local
  context to touch it safely.

## See also

- `clean-architecture` skill (boundaries)
- `bloc-pattern` skill (Bloc template)
