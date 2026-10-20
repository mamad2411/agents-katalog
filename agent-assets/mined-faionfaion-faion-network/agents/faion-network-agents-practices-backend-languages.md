# Backend Languages Practices

## Summary

**One-sentence:** Produces a backend service scaffold in Go/Rails/Laravel/Spring Boot/.NET/Rust enforcing the canonical layout, error model, DI shape, and async discipline for the chosen language.

**One-paragraph:** Reference patterns for six backend languages. Go: cmd/internal/pkg layout, wrapped errors via fmt.Errorf with %w, consumer-side interfaces, worker-pool concurrency. Ruby on Rails: thin controllers + service/form/query objects. PHP Laravel: controller -> Form Request -> Service. Java Spring Boot: constructor injection (no @Autowired on fields), @Service @RequiredArgsConstructor, builder DTOs. C# .NET: IService interfaces + DI, async Task<T> throughout. Rust: thiserror Result types, tokio for async, no blocking I/O inside async fns. The artefact is the language tag + scaffold metadata; the validator checks the canonical fields per language are present.

**Ефективно для:**

- Greenfield service scaffolding in any of the six languages.
- Cross-language onboarding: produce equivalent service shape in two stacks.
- Code-review gate — check Go interfaces are consumer-side, Spring uses constructor injection, Rust async has no blocking calls.
- Refactor passes aligning an existing module to the known-good shape.

## Applies If (ALL must hold)

- Greenfield service scaffolding in one of Go, Rails, Laravel, Spring Boot, .NET, Rust.
- Cross-language onboarding where shape parity matters.
- Refactor passes aligning existing modules to canonical layout.
- Code-review gates checking idiomatic patterns per language.

## Skip If (ANY kills it)

- Architecture decisions (microservices vs monolith) — out of scope.
- Performance profiling or observability — out of scope.
- Frontend code — see practices-frontend-components / practices-js-ts-stack.
- Project already has a documented house style that diverges — agent will overwrite.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target language | one of: go | rails | laravel | spring | dotnet | rust | team decision |
| Service name + intended public surface | free text + endpoint list | task brief |
| DI framework (when applicable) | Spring / Symfony container / built-in | language defaults |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[testing-backend-languages]] | shared test runner conventions per language |
| [[trunk-based-ci-gates]] | scaffolded service must pass the CI gate |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-language-template` | haiku | lookup based on input field |
| `emit-canonical-scaffold` | sonnet | render layout + key files with idiomatic patterns |
| `review-against-rules` | sonnet | rule-by-rule check on generated tree |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-layout.txt` | Canonical Go project layout tree |
| `templates/go-service.go` | Go service skeleton with consumer-side interface + worker pool |
| `templates/spring-service.java` | Spring Boot service using constructor injection |
| `templates/rust-error.rs` | Rust error type via thiserror + async fn |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-practices-backend-languages.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[practices-python-ecosystem]]
- [[practices-django-coding]]
- [[testing-backend-languages]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
