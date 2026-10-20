---
name: observability-quality
description: Use when adding logging, metrics, distributed tracing, error monitoring, linting, architecture testing, or test infrastructure to a project. Covers OpenTelemetry, Sentry/Datadog/Grafana, Biome/ESLint, ArchUnit, commitlint, Knip, Playwright, and coverage strategy. Infrastructure and tooling quality only; writing feature tests goes to testing or e2e-testing.
triggers: [user, model]
allowed-tools: [read, grep, glob, edit, write, exec]
---

# Observability and Code Quality

Evidence-based guidance for three quality pillars. Synthesized from academic research (Microsoft Research, Google, ICSE, FSE, OOPSLA) and industry standards (CNCF, OpenTelemetry, Playwright).

## When to apply

These practices are NOT universal. Apply based on project context:

| Project type | Observability | Lint | Tests |
|---|---|---|---|
| Production service (multi-user) | Full (OTel + backend) | Full toolchain | Full pyramid |
| Internal tool | Sentry (errors only) | Lint + format | Unit + integration |
| Prototype / MVP | Console logging | Lint only | Smoke tests |
| Library / package | Minimal | Full toolchain | Full + mutation testing |
| Solo script | None | None | None |

**Observability overhead is real:** tracing adds 16-180% latency (Google: 16.3% avg, Facebook: 1.16 GB/s trace data). Don't add tracing to prototypes or low-traffic services.

## Pillar 1: Observability

### Foundation: OpenTelemetry (OTel)

OTel is the CNCF industry standard. 217% growth among Fortune 500 (2024). 90+ vendor backends. Vendor-neutral — no lock-in.

**Three signals (in order of priority):**

1. **Logs** — structured, with consistent fields (timestamp, level, traceId, service, message)
2. **Metrics** — counters (requests, errors), histograms (latency), gauges (queue depth)
3. **Traces** — end-to-end request flow across services (highest overhead, apply last)

### Backend selection

| Backend | Best for | Cost | Limitation |
|---|---|---|---|
| **Sentry** | Error tracking, stack traces, session replay | Free tier generous | No infra monitoring |
| **Grafana Cloud** | Metrics + logs + traces (self-host or cloud) | $0-300/mo | Requires config effort |
| **Datadog** | Full-stack, 700+ integrations, best UX | Expensive at scale | Per-host pricing punishes growth |
| **New Relic** | APM, 100GB/mo free tier | Free tier | UX loses to Datadog |

**Recommended combo for small teams:** Sentry (errors) + Grafana Cloud (metrics/logs) = $50-300/mo.

**Recommended for enterprises:** OTel collection layer + Datadog backend (if budget allows).

### What to instrument

| Priority | What | Signal |
|---|---|---|
| 1 | Unhandled errors, exceptions | Sentry / log ERROR |
|---|---|---|
| 2 | Request latency (p50, p95, p99) | Metric histogram |
| 3 | Error rate (4xx, 5xx) | Metric counter |
| 4 | Request flow across services | Trace (only if multi-service) |
| 5 | Business metrics (signups, conversions) | Metric counter |

### What NOT to instrument

- Prototypes and MVPs (overhead > value)
- Single-process scripts (no distributed tracing needed)
- Low-traffic internal tools (console.log is fine)
- Every function call (tracing overhead compounds)

## Pillar 2: Code quality and linting

### Toolchain (by category)

| Category | Recommended tool | Alternative | When to use alt |
|---|---|---|---|
| Linter + formatter | **Biome** | ESLint + Prettier | Need type-aware rules or 2400+ plugins |
| Architecture contracts | **ArchUnit** (Java/.NET) | dependency-cruiser (JS) | JS/TS projects |
| Commit linting | **commitlint** | — | If using conventional commits |
| Dead code | **Knip** (JS/TS) | ts-prune | JS/TS projects |
| Type checking | **tsc** / **biome check** | — | All TS projects |

### Biome vs ESLint

| Factor | Biome | ESLint |
|---|---|---|
| Speed | 10-56x faster | Baseline |
| Rules | 502 rules, ~94% of common ESLint | 2400+ plugins |
| Type-aware | Partial (~75-85%) | Full |
| Plugin ecosystem | None (all-in-one) | Massive |
| Config | Single file, simple | Complex, plugin conflicts |

**Choose Biome for:** new projects, speed-critical CI, simplicity.
**Choose ESLint for:** complex TypeScript, type-aware rules, existing plugin dependencies.

### Architecture testing

ArchUnit enforces architectural boundaries at test time. Prevents layer violations (e.g., controllers calling DB directly).

```
// ArchUnit (Java) example
noClasses().that().resideInAPackage("..controller..")
    .should().dependOnClassesThat().resideInAPackage("..repository..");
```

For JS/TS: `dependency-cruiser` provides similar capability.

**When to use:** projects with defined layers (controller/service/repository). Skip for prototypes or single-file modules.

### Commitlint

Enforces conventional commit format. Add to CI as a gate:

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
echo "export default { extends: ['@commitlint/config-conventional'] };" > commitlint.config.js
```

Husky hook: `commitlint --edit $1` on `commit-msg`.

## Pillar 3: Testing

### Test strategy

| Layer | Proportion | Tool | Speed |
|---|---|---|---|
| Static analysis | Base | Biome/tsc | Instant |
| Unit tests | Many | Vitest/Jest/pytest | <100ms each |
| Integration tests | Some | Vitest/pytest | <1s each |
| E2E tests | Few | Playwright | 5-30s each |

**Testing Trophy (Kent C. Dodds)** — integration-heavy — is preferred for web apps. **Test Pyramid** — unit-heavy — is preferred for libraries and complex domain logic.

### Playwright (E2E)

Industry standard (Microsoft-backed). Auto-waiting, web-first assertions, multi-browser, mobile emulation.

**Flakiness expectation:** Google reports ~16% of E2E tests are flaky. This is inherent, not a tooling failure. Mitigate with:
- `page.waitForURL()` / `page.waitForSelector()` (auto-wait)
- `expect(locator).toBeVisible()` (web-first assertions)
- Retry in CI (1-2 retries, not more)
- Quarantine flaky tests, don't delete

### Coverage: screen, not gate

**Research findings:**
- Microsoft Research: coverage has insignificant correlation with post-release bugs at project level
- UC Irvine: weak negative correlation with bug-fixes
- TU Delft: >80% of engineers ignore failing coverage checks

**Use coverage to:**
- Find untested code paths
- Identify critical paths lacking tests
- Track trends over time

**Do NOT use coverage to:**
- Enforce arbitrary percentage thresholds (80%, 90%)
- Gate PRs on coverage percentage
- Treat high coverage as quality proof

**Binary threshold that works:** covered vs not-covered. Code with tests has ~50% fewer bug-fixes than untested code. The binary matters; the percentage doesn't.

### Mutation testing (conditional)

Mutation testing is more reliable than coverage but expensive. Use `testing` skill for the full workflow.

**When to use:**
- Critical systems (security, financial, safety)
- When test suite quality matters more than CI speed
- Educational settings

**When to skip:**
- Rapid iteration / prototypes
- Limited CI resources
- Large existing test suites (cost compounds)

## Integration with existing skills

| This skill covers | Existing skill | Use both |
|---|---|---|
| Test strategy overview | `testing` | Yes — tdd for implementation, this for infrastructure |
| Mutation testing guidance | `testing` | Yes — this for when, that for how |
| Verification gates | `gates` | Yes — this for setup, that for per-task check |
| Code review | `code-review` | Independent |
| CI debugging | `debugging` | Independent |

## Setup checklist (new project)

- [ ] Biome configured (`biome init`)
- [ ] TypeScript strict mode
- [ ] commitlint + husky
- [ ] Knip in CI (`knip --production`)
- [ ] Vitest/Jest for unit + integration
- [ ] Playwright for E2E (if web app)
- [ ] Sentry for error tracking (if production)
- [ ] OTel SDK if multi-service (logs + metrics first, traces last)
- [ ] Coverage reporting (Codecov/Coveralls) as screen, not gate
- [ ] ArchUnit/dependency-cruiser if layered architecture

## Up-to-date docs

When the user names a specific library version or asks about current APIs, invoke the `context7` skill before proposing code. Good candidates: `OpenTelemetry`, `Sentry`, `Datadog`, `Grafana`, `Biome`, `ESLint`, `Prettier`, `Knip`, `Playwright`, `ArchUnit`.

If a tool's current documentation contradicts this skill, prefer the Context7 result and note the conflict.

## Sources

- Microsoft Research: Coverage and post-release defects — https://www.microsoft.com/en-us/research/publication/code-coverage-and-post-release-defects-a-large-scale-study-on-open-source-projects/
- Google: Code coverage at scale — https://research.google/pubs/code-coverage-at-google/
- TU Delft: Engineers ignore coverage checks (AST 2024) — https://dl.acm.org/doi/10.1145/3644032.3644444
- OOPSLA 2024: LLM-integrated static analysis — https://www.cs.ucr.edu/~zhiyunq/pub/oopsla24_llift.pdf
- FSE 2024: Defects in static analyzers — https://yuleisui.github.io/publications/fse24c.pdf
- ICSE 2018: Mutation scores and real faults — https://arxiv.org/abs/1804.04748
- ACM Computing Surveys 2021: Survey of flaky tests — https://dl.acm.org/doi/10.1145/3476105
- OpenTelemetry docs — https://opentelemetry.io/docs/
- Biome — https://biomejs.dev/
- ArchUnit — https://www.archunit.org/
- Knip — https://knip.dev/
- Playwright — https://playwright.dev/docs/
- Kent C. Dodds: Testing Trophy — https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
- Martin Fowler: Test Pyramid — https://martinfowler.com/bliki/TestPyramid.html
