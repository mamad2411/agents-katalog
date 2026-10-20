# iOS Templates — Claude Code Instructions

> You are working on the **iOS App Templates** monorepo at `/Users/darisadam/Documents/Projects/Tools/swift-template`. This is **not** an iOS app — it is the scaffolding that *generates* iOS apps. Edit templates, not generated output.

## What this repo is

A curated set of iOS app templates with a CLI (`bin/ios-template`) that scaffolds new projects. Eight template variants live under `templates/{xcodegen,tuist}/{simple-mvvm,modular-mvvm,clean-mvvm-repository,modular-tca}/`. Shared assets (SwiftLint config, AI agent docs, gitignore, GitHub Actions) live under `shared/` and are layered into every generated project.

**Scope: SwiftUI only.** Every template uses SwiftUI views and `@Observable` view models. Do not introduce UIKit, Storyboards, or XIBs into any template — that's a hard architectural constraint, not a preference. If a user asks for UIKit support, point them at the FAQ in `README.md` (the answer is "fork and adapt; this isn't the right starting point").

## Where to make changes

| You want to… | Edit |
|--------------|------|
| Change a template's source code | `templates/<bs>/<arch>/...` |
| Change SwiftLint rules for all generated projects | `shared/linting/.swiftlint.yml` |
| Change `CLAUDE.md` / `AGENTS.md` / `.cursorrules` text for generated projects | `shared/ai/<name>.template` |
| Change the `setup.sh` shipped with generated projects | `shared/setup-xcodegen.sh.template` or `shared/setup-tuist.sh.template` |
| Change CLI behavior | `bin/ios-template` |
| Add a new architecture | New folder under each `templates/<bs>/` + entry in its `template.json` |
| Update top-level docs | `README.md` or `docs/` |

## Placeholders

Templates contain these tokens. The CLI substitutes them at scaffold time:

| Token | Example expansion |
|-------|-------------------|
| `__APP_NAME__` | `Aurora` |
| `__BUNDLE_ID__` | `com.example.aurora` |
| `__ORG_NAME__` | `Example Org` |
| `__SWIFT_VERSION__` | `6.0` |
| `__DEPLOYMENT_TARGET__` | `17.0` |
| `__ARCHITECTURE_NAME__` | `Clean Architecture + MVVM + Repository` |
| `__BUILD_SYSTEM__` | `tuist` |
| `__GENERATE_COMMAND__` | `tuist generate` *(read from template.json)* |
| `__TEST_COMMAND__` | The xcodebuild test command *(read from template.json)* |
| `__CONFIG_FILE__` | `Project.swift` or `project.yml` |
| `__PLATFORMS__` | `iPhone, iPad` |

If you add a new token: update `substitute_placeholders` in `bin/ios-template` and document it here.

## SourceKit diagnostics

When editing template files, your editor's SourceKit will scream about missing imports, unresolved symbols, etc. **Ignore them** — template files are not part of a real Swift module; they only compile after the CLI scaffolds a project. The CI workflow we ship with generated projects exercises the real build.

## When you finish editing a template

Always smoke-test by scaffolding into `/tmp`:

```bash
./bin/ios-template new \
  --build-system <bs> --architecture <key> \
  --name SmokeTest --bundle-id com.example.smoke --org "Test" \
  --output /tmp/smoke-$$ --no-git --no-setup -y
```

Then verify:
- File tree looks right
- No `__APP_NAME__` (or other unsubstituted placeholders) remain:
  ```bash
  grep -rIl '__APP_NAME__\|__BUNDLE_ID__\|__ORG_NAME__\|__SWIFT_VERSION__\|__DEPLOYMENT_TARGET__\|__GENERATE_COMMAND__\|__TEST_COMMAND__' /tmp/smoke-$$
  ```
- The setup.sh inside the generated project (if you have the tools available) successfully generates an Xcode project

## When you finish editing the CLI

```bash
./bin/ios-template list
./bin/ios-template doctor
./bin/ios-template new --help
# Then a real scaffold as above.
```

## Guardrails

- **Never edit a generated project directly** — edit the template, then regenerate. Otherwise your fix doesn't propagate.
- **Never commit absolute paths** that mention `/Users/darisadam` in template files. Tokenize or relative-path them.
- **Never run `rm -rf` on this repo** — there's a year of curation here. If you need to delete a template, move it to `.archive/` first.
- **Never use `// swiftlint:disable` in template Swift code** — the templates we ship enforce zero violations, so we cannot ship disable directives ourselves.

## Style

- Bash: 4-space indent, `set -euo pipefail`, every function logged via `log_*`
- Swift in templates: 2-space indent, explicit access control, no `print`, no force-unwrap
- Markdown: 2-space indent, sentence-case headers
- YAML/JSON: 2-space indent
