# AGENTS.md

Guidance for agents and humans working in this repository. This file is self-contained. Check the repository's source, Mise configuration, Lefthook configuration, and workflows for facts that can vary instead of copying versions or commands from another project.

## Working here

- Read the relevant code, configuration, tests, and nearby examples before editing. Existing code and reference implementations are evidence; understand the invariant and ownership boundary before choosing a solution.
- Target current supported behaviour. Prefer the simplest design that reduces state and machinery, and bring the affected path into conformance when existing code disagrees with this baseline.
- Preserve unrelated work. Keep changes focused, remove artifacts orphaned by the change, and keep generated outputs with their source change.
- Verify dependency APIs, flags, and defaults from the pinned source or primary documentation.
- Keep secrets, credentials, real identities, production data, and local environment files out of source, fixtures, logs, and commits.

## Baseline

- Write idiomatic, modern code for the versions pinned by this repository.
- Keep operations idempotent. Re-running a command, generator, reconciler, or migration with identical input shouldn't accumulate side effects.
- Stay DRY and minimal without premature abstraction. Three similar call sites are fine; add a helper, interface, options type, or generic abstraction when real callers need the variance it provides.
- Comments explain non-obvious constraints, invariants, and external requirements. Names and structure carry the ordinary narrative.
- Do not add file banners, author or date headers, or comment-based change logs. Git owns provenance and history.
- Write prose from the repository's point of view. Use `we` and `our` for the organisation, and `the app`, `the service`, `the command`, or direct wording for this repository. Omit organisation and product names when context already identifies them; keep names that are identifiers or distinguish an external system.
- Keep tracked documentation durable and present-tense. READMEs use a terse introduction and the relevant established emoji-led sections; omit migration history, temporary setup state, and inventories of absent features.
- Keep one-time local and external-service setup notes out of tracked files. If asked to preserve them locally, leave them untracked without adding ignore or exclude rules.
- Tests protect behaviour and contracts at the lowest useful boundary. Use realistic synthetic inputs and add regression coverage for plausible failures rather than implementation shape.

## Repository tooling

- Mise owns tools and commands. Run `mise tasks` and read `.mise/config.toml` before choosing task names or invoking bare tools.
- Lefthook extends the shared organisation configuration. Read `.lefthook.toml` and use `lefthook dump` when merged hook behaviour matters; local hooks contain only repository-specific additions.
- Run focused checks while working, then the relevant repository format, lint, test, build, generation, workflow, packaging, and security tasks before calling the work complete.
- Treat generated files, schemas, lockfiles, release metadata, and package assets as part of the contract that produces them.

## Go

- Follow [Effective Go](https://go.dev/doc/effective_go) and [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments). Let `gofmt -s` own formatting.
- `go.mod` declares the language floor; Mise pins the toolchain used by local tasks and CI. Use modern standard-library constructs supported by the declared version.
- Put executable composition in `cmd/<app>/main.go` and owned behaviour under `internal`. Keep `main` to configuration, logging, dependency construction, lifecycle, and exit status.
- Use `github.com/caarlos0/env/v11` for application-owned environment configuration. Parse into one config type, derive and validate in one load boundary, and fail at startup. Document config fields with their purpose and meaningful defaults.
- Use `github.com/spf13/pflag` for application-owned flags and Cobra when the CLI has commands or more than a small flag surface. Structured files suit user-authored domain configuration; all sources converge on one validation path.
- Use `log/slog` and structured stdout logging. Configure logging once at composition; use package-level logging or inject `*slog.Logger` at a genuine reusable boundary.
- Wrap errors with `fmt.Errorf("<component>: %w", err)`. Use sentinel errors for conditions callers branch on and classify errors once at the HTTP, CLI, job, or protocol boundary.
- Functions that perform I/O take `context.Context` first and propagate cancellation. Long-running processes use signal-aware root contexts and bounded shutdown; use `errgroup` for related goroutines that can fail.
- Prefer standard-library tests and table-driven subtests when a table makes cases clearer. Keep the package's established test framework, use local servers or fakes at real boundaries, and run race-enabled tests for concurrent code.
- Containerized Go services default to static, trimmed binaries and a non-root minimal runtime. Run the repository's vulnerability task for dependency and release work.

## Git and completion

- Use focused Conventional Commits; Release Please derives versions from them where configured.
- Commit, push, publish, deploy, contact live systems, or perform destructive operations only when explicitly requested.
- Report the checks run, behaviour changed, generated outputs refreshed, and any verification that couldn't be completed.

## Repository contract

- Prometheus exporter-toolkit, Kingpin, and `promslog` own the conventional exporter CLI, web listener, and logging surface.
- Keep Epson transport and parsing separate from metric collection. Metric names, labels, and meanings are public scrape contracts.
- Tests use captured responses and local servers. Configuration modules carry scrape policy and HTTP client behaviour through one validation path.
