# Backend Testing Across Languages

## Summary

**One-sentence:** Produces a test suite scaffold per backend language using the idiomatic runner (RSpec/Pest/xUnit/tokio::test/JUnit slices) with the right scope discipline (no @SpringBootTest by default; no WebApplicationFactory by default; #[tokio::test] for async Rust).

**One-paragraph:** Per-language test idioms: Ruby on Rails uses RSpec + factory_bot with let/let! discipline; Laravel uses Pest + RefreshDatabase + postJson/getJson; Spring Boot uses @ExtendWith(MockitoExtension.class) / @DataJpaTest / @WebMvcTest slices instead of @SpringBootTest by default; .NET uses xUnit + Moq + FluentAssertions, no WebApplicationFactory unless integration; Rust uses #[test] / #[tokio::test] in #[cfg(test)] mod tests {} blocks. Agent prompts include the runner name explicitly so LLMs don't default to the wrong API.

**Ефективно для:**

- Greenfield test setup in any of the five backend languages.
- Refactor passes replacing @SpringBootTest with proper slices.
- Adding async Rust tests under tokio::test instead of bare #[test].
- Cleaning up Minitest -> RSpec migrations.

## Applies If (ALL must hold)

- Backend language is one of: ruby_rails / laravel / spring / dotnet / rust.
- Project ships unit + integration tests as a quality gate.
- Tests run in CI and must complete in <10 minutes.
- Mocks/fakes are used for dependencies, not deep call graphs.

## Skip If (ANY kills it)

- Pure Python (use testing-django-pytest).
- Frontend tests (use testing-js-ts-frontend).
- End-to-end browser tests (use playwright-automation).
- Performance/load tests — separate methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Language | ruby_rails | laravel | spring | dotnet | rust | team decision |
| Test scope | unit | integration | slice | task brief |
| Dependencies the SUT uses | list of collaborators | service spec |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[practices-backend-languages]] | code-side patterns the tests verify |
| [[trunk-based-ci-gates]] | CI gate runs these tests on every push |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-runner` | haiku | lookup from language tag |
| `emit-test-scaffold` | sonnet | idiomatic test class with mocks + assertions |
| `scope-discipline-check` | sonnet | flag @SpringBootTest / WebApplicationFactory misuse |

## Templates

| File | Purpose |
|------|---------|
| `templates/OrderService.spec.rb` | RSpec test using factory_bot + let |
| `templates/OrderTest.php` | Pest test with RefreshDatabase + JSON assertion |
| `templates/OrderServiceTest.java` | Spring service unit test using MockitoExtension (no SpringBootTest) |
| `templates/OrderServiceTests.cs` | xUnit + Moq + FluentAssertions service test |
| `templates/order_test.rs` | Rust async unit test using tokio::test |
| `templates/artefact.json` | Sample artefact metadata for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-testing-backend-languages.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[testing-django-pytest]]
- [[testing-js-ts-frontend]]
- [[practices-backend-languages]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.
