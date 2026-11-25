---
name: zio-openfeature
description: >
  Complete usage guide for the zio-openfeature library — a ZIO 2 / Scala 3 wrapper around
  the OpenFeature Java SDK. TRIGGER when: code imports zio.openfeature.*, using FeatureFlags
  service, wiring OpenFeature providers via ZLayer, writing flag evaluations, setting up hooks,
  handling provider events, implementing lifecycle management, or writing feature-flag tests.
  Covers wiring and layering patterns, sync vs async init decision, provider-specific setup
  (Optimizely, flagd, LaunchDarkly, OFREP, HOCON, EnvVar), error handling, hooks pipeline,
  events and streaming, transactions, multi-provider fallback, and testing with TestFeatureProvider.
---

# zio-openfeature Usage Guide

## Installation

```scala
// Core (always required)
libraryDependencies += "io.github.etacassiopeia" %% "zio-openfeature-core" % "<version>"

// Built-in providers: HoconProvider, EnvVarProvider, CachingProvider, CircuitBreakerProvider
libraryDependencies += "io.github.etacassiopeia" %% "zio-openfeature-extras" % "<version>"

// Testing — scope Test
libraryDependencies += "io.github.etacassiopeia" %% "zio-openfeature-testkit" % "<version>" % Test

// OFREP HTTP provider (separate module — avoids Jackson/Guava transitive deps)
libraryDependencies += "io.github.etacassiopeia" %% "zio-openfeature-ofrep" % "<version>"

// Optimizely direct integration (first-party, not the OpenFeature contrib provider)
libraryDependencies += "io.github.etacassiopeia" %% "zio-openfeature-optimizely" % "<version>"
```

Third-party providers (add via OpenFeature ecosystem):

| Service | Dependency |
|---------|-----------|
| flagd | `"dev.openfeature.contrib.providers" % "flagd" % "0.8.9"` |
| LaunchDarkly | `"dev.openfeature.contrib.providers" % "launchdarkly" % "1.1.0"` |
| Flagsmith | `"dev.openfeature.contrib.providers" % "flagsmith" % "0.1.0"` |
| Flipt | `"dev.openfeature.contrib.providers" % "flipt" % "0.2.0"` |
| Unleash | `"dev.openfeature.contrib.providers" % "unleash" % "0.1.3"` |

---

## Core Service — FeatureFlags

The `FeatureFlags` trait is the single entry point for all flag operations.

### Flag Evaluation

```scala
import zio.*
import zio.openfeature.*

// Value only (most common)
val enabled: ZIO[FeatureFlags, FeatureFlagError, Boolean] =
  FeatureFlags.boolean("feature-toggle", default = false)

val variant:  ZIO[FeatureFlags, FeatureFlagError, String]  = FeatureFlags.string("button-color", "blue")
val limit:    ZIO[FeatureFlags, FeatureFlagError, Int]     = FeatureFlags.int("max-items", 100)
val rate:     ZIO[FeatureFlags, FeatureFlagError, Double]  = FeatureFlags.double("sample-rate", 0.1)
val count:    ZIO[FeatureFlags, FeatureFlagError, Long]    = FeatureFlags.long("max-bytes", 1000000L)
val config:   ZIO[FeatureFlags, FeatureFlagError, Map[String, Any]] =
  FeatureFlags.obj("feature-config", Map("timeout" -> 30))

// Detailed resolution — value + variant + reason + metadata
val details: ZIO[FeatureFlags, FeatureFlagError, FlagResolution[Boolean]] =
  FeatureFlags.booleanDetails("feature", default = false)

details.map { r =>
  println(r.value)                // the resolved value
  println(r.variant)              // Option[String] — experiment arm name
  println(r.reason)               // ResolutionReason (Static, TargetingMatch, Split, Cached, Default, ...)
  println(r.metadata.getString("source"))  // provider-specific metadata
  println(r.flagKey)
}
```

**ResolutionReason values:** `Static | Default | TargetingMatch | Split | Cached | Disabled | Unknown | Stale | Error`

### Custom Types via FlagType

```scala
given FlagType[MyConfig] = FlagType.from(
  "MyConfig",
  defaultValue = MyConfig.default,
  decoder = raw => Right(decodeJson(raw)),
  encoder = cfg => encodeJson(cfg)
)

val cfg: ZIO[FeatureFlags, FeatureFlagError, MyConfig] =
  FeatureFlags.value[MyConfig]("my-config-flag", MyConfig.default)
```

---

## ZLayer Wiring

### Factory Methods

| Factory | Blocks on init? | Use case |
|---------|----------------|----------|
| `fromProvider(p)` | Yes — 30 s default | Correctness-critical; layer build fails if provider doesn't reach Ready |
| `fromProvider(p, evalTimeout, initTimeout)` | Yes | Tuned timeouts |
| `fromProviderAsync(p)` | No | Fast boot; evaluations fail with ProviderNotReady until ready |
| `fromProviderAsync(p, evalTimeout, initTimeout)` | No | Async with tuned timeouts |
| `fromProviderWithDomain(p, domain)` | Yes | Isolated multi-domain client |
| `fromProviderWithDomainAsync(p, domain)` | No | Same, async |
| `fromProviderWithHooks(p, hooks)` | Yes | Pre-register hooks at layer creation |
| `fromProviderWithHooksAsync(p, hooks)` | No | Same, async |
| `fromMultiProvider(providers, strategy?)` | Yes | Fallback chain (sync) |
| `fromMultiProviderAsync(providers, strategy?)` | No | Fallback chain (async) |

### Basic Wire Pattern

```scala
object MyApp extends ZIOAppDefault:
  val program = for
    enabled <- FeatureFlags.boolean("my-feature", default = false)
    _       <- ZIO.when(enabled)(Console.printLine("Feature enabled!"))
  yield ()

  def run = program.provide(
    Scope.default >>> FeatureFlags.fromProvider(new FlagdProvider())
  )
```

### With Evaluation Timeout

```scala
// All evaluations on this instance are capped at 500ms
val layer = FeatureFlags.fromProvider(provider, evaluationTimeout = 500.millis)

// Per-call override — takes precedence over global
ff.booleanDetails("flag", false, options = EvaluationOptions.empty.withTimeout(100.millis))
```

---

## Sync vs Async — Critical Decision

Provider initialization has two dimensions: **blocking vs non-blocking** and **single vs multi-provider fallback**.

### Sync (`fromProvider`)
- **Blocks the layer build** until the provider reaches `Ready` (or timeout fires)
- After init returns, the library reads `provider.getState()` — anything other than `READY`/`STALE` fails the build
- Result: **no half-initialised state**. A wrong SDK key or unreachable endpoint surfaces at startup as `TimeoutException` or `IllegalStateException`
- Use for: financial logic, fraud checks, billing rules — any flag whose default value is unsafe

### Async (`fromProviderAsync`)
- **Returns immediately** — layer is available before provider is ready
- Evaluations fail with `ProviderNotReady` until provider signals `Ready`
- A watchdog fiber sleeps `initTimeout` (default 30 s), then atomically transitions `NotReady`/`Error` → `Fatal`
- **`Fatal` is not terminal** — if `PROVIDER_READY` fires later, status transitions `Fatal → Ready`
- Use for: UI variations, feature gates, experiments — flags where defaulting during init is acceptable

### Decision Matrix

| | Single remote provider | Remote + EnvVar fallback (multi-provider) |
|---|---|---|
| **Sync** | Refuses to boot if remote is sick. Best for correctness-critical workloads. | Rarely right — fails only if every provider fails; `EnvVarProvider` always succeeds so Optimizely failures become invisible |
| **Async** | Boots immediately. Gate traffic with `providerStatus` check. Flags default during init window. | Always boots and always `Ready`. Highest availability, but remote failures are masked — needs separate monitoring |

### Handling the "All Defaults" Gap (Async Mode)

**Option 1 — Gate traffic on readiness:**

```scala
val readinessCheck: URIO[FeatureFlags, Boolean] =
  ZIO.serviceWithZIO[FeatureFlags](_.providerStatus).map {
    case ProviderStatus.Ready | ProviderStatus.Stale => true
    case _                                            => false
  }
// Wire into your /health or /ready endpoint
```

**Option 2 — EnvVar fallback for correctness-critical flags only:**

```scala
import zio.openfeature.extras.EnvVarProvider

val critical = Map("FF_MAINTENANCE_MODE" -> "false", "FF_FRAUD_CHECK_ENABLED" -> "true")
val envProvider = EnvVarProvider.withLookup(critical.get)
val layer = FeatureFlags.fromMultiProviderAsync(
  List(optimizelyProvider, envProvider),
  MultiProviderStrategy.firstSuccessful
)
```

### Tuning `initTimeout`

```scala
// Tight — fail fast on misconfig
FeatureFlags.fromProvider(provider, evaluationTimeout = 500.millis, initTimeout = 15.seconds)

// Raise for slow cold-starts on constrained networks
FeatureFlags.fromProviderAsync(provider, evaluationTimeout = 500.millis, initTimeout = 90.seconds)
```

---

## Evaluation Context

Context carries user and environment attributes for targeting decisions.

```scala
// Targeting key = user ID (required for targeting rules to fire)
val ctx = EvaluationContext("user-123")
  .withAttribute("plan", "premium")
  .withAttribute("country", "US")
  .withAttribute("beta", true)
  .withAttribute("signup_date", Instant.now())

FeatureFlags.boolean("premium-feature", default = false, ctx)
```

### Context Hierarchy (5 Levels, Invocation Wins)

```
Global → Transaction → Client → Scoped → Invocation
```

```scala
// 1. Global — app-wide (e.g., version, environment)
FeatureFlags.setGlobalContext(
  EvaluationContext.empty.withAttribute("app_version", "2.0.0")
)

// 2. Client — per FeatureFlags instance
FeatureFlags.setClientContext(
  EvaluationContext.empty.withAttribute("service", "payments")
)

// 3. Scoped — fiber-local block (respects structured concurrency)
FeatureFlags.withContext(EvaluationContext("user-456").withAttribute("session_id", "xyz")) {
  for
    a <- FeatureFlags.boolean("feature-a", false)  // merged context
    b <- FeatureFlags.string("feature-b", "ctrl")
  yield (a, b)
}

// 4. Invocation — single evaluation call (highest priority)
FeatureFlags.boolean("feature", false, EvaluationContext("user-789"))
```

**AttributeValue types:** `BoolValue | StringValue | IntValue | LongValue | DoubleValue | InstantValue | ListValue | StructValue`

---

## Error Handling

`FeatureFlagError` is a sealed ADT. Handle errors at the appropriate level — not everything needs recovery.

```scala
FeatureFlags.boolean("flag", false)
  .catchSome {
    case _: FeatureFlagError.ProviderNotReady         => ZIO.succeed(false)
    case FeatureFlagError.ProviderError(cause)        => ZIO.logError(s"Provider: $cause") *> ZIO.succeed(false)
    case _: FeatureFlagError.Unreachable              => alertService.warn("network failure") *> ZIO.succeed(false)
    case FeatureFlagError.Unauthorized(reason)        => alertService.page(reason) *> ZIO.fail(...)
  }
```

### Full Error ADT

| Error | Meaning | When | Action |
|-------|---------|------|--------|
| `FlagNotFound(key)` | Flag key not in provider | Evaluation | Use default; check spelling |
| `TypeMismatch(key, expected, actual)` | Wrong type requested | Evaluation | Fix flag definition or eval call |
| `ParseError(key, underlying)` | Can't parse flag value | Evaluation | Fix flag config |
| `TargetingKeyMissing(key)` | Rule requires targeting key | Evaluation | Always pass a targeting key |
| `InvalidContext(reason)` | Malformed context | Evaluation | Validate context construction |
| `ProviderNotReady(status)` | Provider still initializing | Evaluation | Return default; check readiness |
| `ProviderInitializationFailed(cause)` | Init sequence failed | Layer build | Fix config; restart |
| `ProviderFatal` | Watchdog fired; no longer retrying | Evaluation | Alert; pod may recover later |
| `Unauthorized(reason)` | Bad/expired SDK key | Evaluation | Page on-call; rotate key |
| `Unreachable(cause)` | DNS / network failure | Evaluation | Check egress; consider self-hosted agent |
| `InvalidConfiguration(reason)` | Bad provider config | Layer build | Fix before deploy |
| `ProviderError(cause)` | Other provider error | Evaluation | Log + default |
| `NestedTransactionNotAllowed` | Transaction inside transaction | Runtime | Restructure code |

**`Unauthorized` and `Unreachable` are auto-classified** — the library inspects `Throwable` type and HTTP status codes to produce these typed cases. Match on them specifically in alerting hooks.

---

## Provider Lifecycle and Events

### Status Transitions

```
NotReady → Ready (normal init)
NotReady → Error (init error, recoverable)
NotReady → Fatal (watchdog fired; timeout elapsed)
Error    → Ready (provider recovered)
Fatal    → Ready (provider eventually became ready — recovery is real)
Ready    → Stale (provider has stale data but can still evaluate)
Ready    → ShuttingDown (scope closing)
```

`canEvaluate` returns `true` for `Ready` and `Stale`. `Fatal` stops evaluation — provider must recover or be replaced.

### Event Handlers

```scala
// Register handler — fires immediately if provider is already in matching state (spec 5.3.3)
val cancel: UIO[UIO[Unit]] = FeatureFlags.onProviderReady { meta =>
  ZIO.logInfo(s"Provider ${meta.name} ready")
}

FeatureFlags.onProviderError { (error, meta) =>
  ZIO.logError(s"Provider ${meta.name} error: ${error.getMessage}")
}

FeatureFlags.onProviderStale { (reason, meta) =>
  ZIO.logWarning(s"Provider ${meta.name} stale: $reason")
}

FeatureFlags.onConfigurationChanged { (changedFlags, meta) =>
  ZIO.logInfo(s"Flags updated: ${changedFlags.mkString(", ")}")
}

// Cancel when no longer needed
cancel.flatMap(cancel => cancel)
```

### Event Stream (Reactive)

```scala
FeatureFlags.events.foreach {
  case ProviderEvent.Ready(meta, _) =>
    ZIO.logInfo(s"Provider ${meta.name} ready")
  case ProviderEvent.ConfigurationChanged(flags, meta, eventMeta) =>
    ZIO.logInfo(s"Flags changed: ${flags.mkString(", ")}")
  case ProviderEvent.Stale(reason, meta, _) =>
    ZIO.logWarning(s"Provider data stale: $reason")
  case ProviderEvent.Error(error, meta, errorCode, errorMessage, _) =>
    ZIO.logError(s"Provider error: ${errorMessage.getOrElse(error.getMessage)}")
  case ProviderEvent.Reconnecting(meta, _) =>
    ZIO.logInfo(s"Provider ${meta.name} reconnecting...")
}.fork
```

### Hot-Swap Provider at Runtime

```scala
// Replaces provider; preserves hooks, context, event handlers
ff.setProvider(newProvider)

// On failure, old provider is gone — recover with a fallback
ff.setProvider(unreliableProvider).catchSome {
  case _: FeatureFlagError.ProviderInitializationFailed =>
    ff.setProvider(fallbackProvider)
}

// When using CircuitBreakerProvider — swap the whole stack, not just the inner
val newCb = CircuitBreakerProvider(newOptimizelyProvider, breakerConfig)
ff.setProvider(newCb)  // correct
// ff.setProvider(newOptimizelyProvider)  // wrong — CB state becomes stale
```

### Shutdown

```scala
// Automatic on scope exit (preferred)
ZIO.scoped {
  for ff <- ZIO.service[FeatureFlags]
  yield ()
}

// Explicit (rarely needed)
FeatureFlags.shutdown
```

---

## Hooks

Hooks add cross-cutting concerns to flag evaluation. All hook methods return ZIO effects.

### Lifecycle

```
before (in registration order)
    → flag resolution
        ↓ success             ↓ failure
      after (reverse order)  error (reverse order)
                    ↓
            finallyAfter (reverse order, always runs)
```

### Hook Levels (Execution Order)

**Before:** API-level → Client-level → Invocation-level → Provider-level

**After/Error/Finally:** Provider → Invocation → Client → API (reverse)

### Built-in Hooks

```scala
// Plain text logging
FeatureFlags.addHook(FeatureHook.logging(logBefore = false, logAfter = true, logError = true))

// Structured logging — adds typed ZIO log annotations (flag.key, flag.value, flag.reason, flag.duration_ms, etc.)
FeatureFlags.addHook(FeatureHook.structuredLogging(
  beforeLevel = Some(LogLevel.Debug),
  afterLevel  = Some(LogLevel.Debug),
  errorLevel  = Some(LogLevel.Warning),
  logContext  = false,             // include evaluation context in annotations
  redactKeys  = Set("email", "ip") // attribute keys to redact (value → "[REDACTED]")
))

// Simple metrics callback
FeatureFlags.addHook(FeatureHook.metrics { (flagKey, duration, success) =>
  metricsClient.record("flag.eval", duration, Map("key" -> flagKey, "success" -> success.toString))
})

// Detailed metrics — full HookContext + FlagResolution access
FeatureFlags.addHook(FeatureHook.metricsDetailed(
  onSuccess = (ctx, details, duration) =>
    metrics.timing("flag.eval", duration, tags = Map(
      "key"     -> ctx.flagKey,
      "reason"  -> details.reason.toString,
      "variant" -> details.variant.getOrElse("none"),
      "provider"-> ctx.providerMetadata.name
    )),
  onError = (ctx, err, duration) =>
    metrics.increment("flag.eval.error", tags = Map(
      "key"   -> ctx.flagKey,
      "error" -> err.getClass.getSimpleName
    ))
))

// Context validation
FeatureFlags.addHook(FeatureHook.contextValidator(
  requireTargetingKey = true,
  requiredAttributes  = List("userId", "sessionId")
))

// Register initial hooks at layer creation
val layer = FeatureFlags.fromProviderWithHooks(provider, List(loggingHook, metricsHook))
```

### Custom Hook

```scala
val auditHook = new FeatureHook:
  override def before(ctx: HookContext, hints: HookHints): UIO[Option[(EvaluationContext, HookHints)]] =
    ZIO.none   // None = no context modification

  override def after[A](ctx: HookContext, details: FlagResolution[A], hints: HookHints): UIO[Unit] =
    ZIO.logInfo(s"AUDIT: ${ctx.evaluationContext.targetingKey.getOrElse("anon")} → ${ctx.flagKey} = ${details.value}")

  override def error(ctx: HookContext, error: FeatureFlagError, hints: HookHints): UIO[Unit] =
    ZIO.logError(s"AUDIT: ${ctx.flagKey} failed: ${error.message}")

  override def finallyAfter(ctx: HookContext, details: Option[FlagResolution[_]], hints: HookHints): UIO[Unit] =
    ZIO.unit
```

### Context Modification in `before`

```scala
val enrichmentHook = new FeatureHook:
  override def before(ctx: HookContext, hints: HookHints): UIO[Option[(EvaluationContext, HookHints)]] =
    Clock.instant.map { now =>
      Some((ctx.evaluationContext.withAttribute("timestamp", now.toString), hints))
    }
  // ... other methods
```

### HookData — Per-Hook Mutable State

`HookData` persists across all stages of one evaluation for a single hook instance. Used for timing spans, correlation IDs, etc.

```scala
val spanHook = new FeatureHook:
  override def before(ctx: HookContext, hints: HookHints): UIO[Option[(EvaluationContext, HookHints)]] =
    ZIO.succeed { ctx.hookData.set("spanId", generateSpanId()); None }

  override def after[A](ctx: HookContext, details: FlagResolution[A], hints: HookHints): UIO[Unit] =
    ZIO.succeed { val id = ctx.hookData.get[String]("spanId").getOrElse("?"); closeSpan(id) }

  override def finallyAfter(ctx: HookContext, details: Option[FlagResolution[_]], hints: HookHints): UIO[Unit] =
    ZIO.succeed(ctx.hookData.clear())
```

### Invocation-Level Hooks (Per-Call)

```scala
val options = EvaluationOptions(
  hooks     = List(myAuditHook),
  hookHints = HookHints("audit-id" -> "req-123")
)
FeatureFlags.booleanDetails("flag", false, EvaluationContext.empty, options)
```

### Compose Multiple Hooks

```scala
val combined = FeatureHook.compose(List(loggingHook, metricsHook, auditHook))
FeatureFlags.addHook(combined)
```

---

## Specific Providers

### Optimizely

```scala
import zio.openfeature.optimizely.OptimizelyProvider

// Validates SDK key shape upfront (non-empty, [A-Za-z0-9_-]+, 6–128 chars, not a placeholder)
val provider = OptimizelyProvider.make(sys.env("OPTIMIZELY_SDK_KEY"))
  .mapError(e => new RuntimeException(e.message))

// Self-hosted Optimizely Agent
val provider = OptimizelyProvider.make(
  sdkKey      = sys.env("OPTIMIZELY_SDK_KEY"),
  datafileUrl = "https://flags.internal.example.com/datafile.json"
)
```

**Always use `fromProviderAsync` with Optimizely** — initialization involves an HTTP fetch from the CDN.

**User targeting** — `targetingKey` maps to Optimizely user ID:

```scala
val userCtx = EvaluationContext("user-12345")
  .withAttribute("plan", "premium")
  .withAttribute("country", "US")

val decision = ff.boolean("premium-feature", false, userCtx)
```

**Feature variables** — typed flags (String/Int/Double) look up variable named `"value"` by default. Override via context:

```scala
val ctx = userCtx.withAttribute("openfeature.variableKey", AttributeValue.StringValue("custom_var"))
val value = ff.string("feature-key", "default", ctx)
```

**Circuit breaker composition:**

```scala
import zio.openfeature.extras.{CircuitBreakerProvider, CircuitBreakerProviderConfig}

val breakerConfig = CircuitBreakerProviderConfig(failureThreshold = 5, resetTimeout = 30.seconds)
val inner   <- OptimizelyProvider.make(sdkKey)
val wrapped <- CircuitBreakerProvider.make(inner, breakerConfig)
val layer    = FeatureFlags.fromProviderAsync(wrapped, evaluationTimeout = 500.millis)
```

**3 Topology Patterns:**

**Pattern A — Async + readiness gate (default, experiments/UI flags):**
```scala
FeatureFlags.fromProviderAsync(provider, evaluationTimeout = 500.millis)
// Wire readinessCheck into /ready endpoint
```

**Pattern B — Sync fail-fast (correctness-critical, financial/billing):**
```scala
FeatureFlags.fromProvider(provider, evaluationTimeout = 500.millis, initTimeout = 15.seconds)
// App refuses to boot if Optimizely isn't ready — orchestrator restarts pod
```

**Pattern C — Optimizely + EnvVar hybrid (highest availability):**
```scala
val envProvider = EnvVarProvider.withLookup(Map("FF_MAINTENANCE_MODE" -> "false").get)
FeatureFlags.fromMultiProviderAsync(List(optimizely, envProvider), MultiProviderStrategy.firstSuccessful)
// Always ready; Optimizely failures masked — needs separate monitoring
```

**Optimizely operational alerts:**

| Signal | Likely cause | Action |
|--------|-------------|--------|
| `FeatureFlagError.Unauthorized` | Wrong/revoked SDK key | Page on-call; rotate key |
| `FeatureFlagError.Unreachable` | CDN DNS/network failure | Check egress; use Optimizely Agent |
| `providerStatus == Fatal` | Datafile never loaded | Restart with fixed config; alert if recurrent |
| `FlagResolution.errorCode` repeatedly populated | Misconfigured flag/rollout | Check Optimizely UI |

### flagd

```scala
import dev.openfeature.contrib.providers.flagd.{FlagdProvider, FlagdOptions}

val provider = new FlagdProvider(
  FlagdOptions.builder()
    .host("flagd.example.com")
    .port(8013)
    .tls(true)
    .build()
)

val layer = FeatureFlags.fromProvider(provider)
```

### LaunchDarkly

```scala
import dev.openfeature.contrib.providers.launchdarkly.{LaunchDarklyProvider, LaunchDarklyProviderOptions}

val provider = new LaunchDarklyProvider(
  LaunchDarklyProviderOptions.builder()
    .sdkKey(sys.env("LAUNCHDARKLY_SDK_KEY"))
    .build()
)
```

### HOCON Provider (Local Config)

```hocon
# application.conf
feature-flags {
  new-checkout = true
  max-items = 50
  rate-limit = 2.5
  welcome-message = "Hello!"
}
```

```scala
import zio.openfeature.extras.*

val layer = FeatureFlags.fromProvider(HoconProvider())              // reads "feature-flags" path
val layer = FeatureFlags.fromProvider(HoconProvider("my-flags"))    // custom path
val layer = FeatureFlags.fromProvider(HoconProvider.fromConfig(cfg)) // explicit Config object

// Reload without restart
provider.reload()
```

### EnvVar Provider

```bash
export FF_NEW_CHECKOUT=true
export FF_MAX_ITEMS=50
export FF_RATE_LIMIT=2.5
```

```scala
import zio.openfeature.extras.*

val layer = FeatureFlags.fromProvider(EnvVarProvider())  // default prefix: FF_
// Key transform: "new-checkout" → FF_NEW_CHECKOUT (uppercase, - and . → _)
```

### OFREP Provider

```scala
import zio.openfeature.ofrep.OFREPProvider

// Validates URL upfront (parseable, http/https, non-empty host)
val provider = OFREPProvider.make("http://localhost:8016")
  .mapError(e => new RuntimeException(e.message))
val layer = FeatureFlags.fromProviderAsync(provider, evaluationTimeout = 500.millis)
```

---

## Multi-Provider Strategy

```scala
import zio.openfeature.MultiProviderStrategy

// FirstMatch: first non-default result wins; any provider error aborts the chain
val layer = FeatureFlags.fromMultiProvider(List(primaryProvider, fallbackProvider))

// FirstSuccessful: first error-free result wins; errors fall through to next provider
val layer = FeatureFlags.fromMultiProvider(
  List(primaryProvider, fallbackProvider),
  MultiProviderStrategy.firstSuccessful
)
```

---

## Transactions

Transactions provide scoped flag overrides and evaluation tracking within a ZIO effect.

```scala
val txResult: ZIO[FeatureFlags, FeatureFlagError, TransactionResult[(Boolean, Int)]] =
  FeatureFlags.transaction(
    overrides      = Map("flag-a" -> true, "limit" -> 50),
    context        = EvaluationContext("user-123"),
    cacheEvaluations = true
  ) {
    for
      a <- FeatureFlags.boolean("flag-a", false)  // true (override)
      n <- FeatureFlags.int("limit", 10)          // 50 (override)
    yield (a, n)
  }

txResult.map { r =>
  r.result           // (true, 50)
  r.flagCount        // 2
  r.overrideCount    // 2
  r.allFlagKeys      // Set("flag-a", "limit")
  r.wasOverridden("flag-a")  // true
  r.wasEvaluated("flag-a")   // false (was overridden, not evaluated from provider)
  r.getEvaluation("flag-a")  // Option[FlagEvaluation[_]]
}
```

Use cases: per-request overrides, A/B test scaffolding, canary deployments, audit trails.

**Nested transactions are not allowed** — they throw `NestedTransactionNotAllowed`.

---

## Provider Registry (Multi-Domain)

For multi-service setups with domain-scoped providers.

```scala
val program = for
  billing  <- FeatureFlagRegistry.getClient("billing")
  auth     <- FeatureFlagRegistry.getClient("auth")
  // Domains without explicit provider fall back to default
  other    <- FeatureFlagRegistry.getClient("analytics")
  flag     <- billing.boolean("new-pricing", default = false)
yield flag

program.provide(Scope.default >>> FeatureFlagRegistry.fromProvider(defaultProvider))
```

```scala
// Hot-swap per domain
FeatureFlagRegistry.setProvider("billing", newOptimizelyProvider)
```

---

## Testing

### Choosing a TestFeatureProvider Layer

| Layer | Starts as | Use when |
|-------|-----------|----------|
| `TestFeatureProvider.layer(flags)` | `Ready` | Most tests — flags work immediately |
| `TestFeatureProvider.scopedLayer(flags)` | `Ready` | Same, explicit scope ownership |
| `TestFeatureProvider.asyncLayer(flags)` | `NotReady` | Test startup/init behavior — requires manual `setStatus` |
| `TestFeatureProvider.asyncReadyLayer(flags, delay)` | `NotReady → Ready` | Simulate async init without manual status |

### Basic Test

```scala
import zio.openfeature.testkit.*

object MySpec extends ZIOSpecDefault:
  def spec = suite("feature flags")(
    test("evaluates flag value") {
      for result <- FeatureFlags.boolean("feature-a", false)
      yield assertTrue(result == true)
    }
  ).provide(Scope.default >>> TestFeatureProvider.layer(Map("feature-a" -> true)))
```

### Service Layer Test Pattern

```scala
// Production layer: FeatureFlags → UserService
object UserService:
  val live: ZLayer[FeatureFlags, Nothing, UserService] = ZLayer.fromFunction(...)

// Test: TestFeatureProvider provides FeatureFlags + gives you control handle
object UserServiceSpec extends ZIOSpecDefault:
  private val testEnv =
    TestFeatureProvider.scopedLayer() >>>
      (ZLayer.environment[TestFeatureProvider with FeatureFlags] ++ UserService.live)

  def spec = suite("UserService")(
    test("new greeting when flag is ON") {
      for
        provider <- ZIO.service[TestFeatureProvider]
        _        <- provider.setFlag("new-greeting-copy", true)
        svc      <- ZIO.service[UserService]
        greeting <- svc.welcome("alice")
      yield assertTrue(greeting.contains("Hey alice"))
    },
    test("handles provider error") {
      for
        provider <- ZIO.service[TestFeatureProvider]
        _        <- provider.setStatus(ProviderStatus.Error)
        svc      <- ZIO.service[UserService]
        result   <- svc.welcome("carol").either
      yield assertTrue(result.isLeft)
    }
  ).provide(testEnv) @@ TestAspect.sequential
```

### TestFeatureProvider Controls

```scala
provider.setFlag("key", value)               // update single flag
provider.setFlags(Map("a" -> true, "b" -> 50)) // replace all flags
provider.removeFlag("key")
provider.clearFlags()

provider.setStatus(ProviderStatus.Ready)      // trigger status transition
provider.setStatus(ProviderStatus.Error)

provider.setDelay(100.millis)                 // simulate latency
provider.setFailing(true)                     // make all evaluations fail
provider.setErrorMode(ErrorMode.FlagNotFound) // specific error type
provider.setFailureProbability(0.3)           // 30% random failures

// Assertions
val evals: List[(String, EvaluationContext)] = provider.getEvaluations
val seen:  Boolean                           = provider.wasEvaluated("my-flag")
val count: Int                               = provider.evaluationCount("my-flag")
provider.clearEvaluations()
```

---

## Monitoring and Observability

```scala
// Structured log annotations (flag.key, flag.value, flag.reason, flag.duration_ms, flag.variant, flag.error, flag.error.type)
FeatureFlags.addHook(FeatureHook.structuredLogging(
  afterLevel = Some(LogLevel.Debug),
  errorLevel = Some(LogLevel.Warning),
  logContext = true,
  redactKeys = Set("email", "ssn", "ip")
))

// Custom metric tags via detailed hook
FeatureFlags.addHook(FeatureHook.metricsDetailed(
  onSuccess = (ctx, details, duration) =>
    metrics.timing("ff.eval", duration.toMillis,
      "key" -> ctx.flagKey, "reason" -> details.reason.toString, "provider" -> ctx.providerMetadata.name),
  onError = (ctx, err, duration) =>
    metrics.increment("ff.eval.error", "key" -> ctx.flagKey, "error" -> err.getClass.getSimpleName)
))

// Lifecycle events for dashboards
FeatureFlags.events.foreach {
  case ProviderEvent.Ready(meta, _)                 => metrics.gauge("provider.ready", 1)
  case ProviderEvent.Error(_, meta, _, _, _)        => metrics.gauge("provider.ready", 0) *> alertService.warn(...)
  case ProviderEvent.ConfigurationChanged(_, _, _)  => ZIO.logInfo("datafile updated")
  case _                                            => ZIO.unit
}.fork

// Readiness check
val isReady: URIO[FeatureFlags, Boolean] =
  ZIO.serviceWithZIO[FeatureFlags](_.providerStatus).map {
    case ProviderStatus.Ready | ProviderStatus.Stale => true
    case _                                            => false
  }
```

---

## Tracking Events

```scala
FeatureFlags.track("button-clicked")
FeatureFlags.track("purchase", EvaluationContext("user-123"))
FeatureFlags.track("checkout", TrackingEventDetails(value = Some(99.99), attributes = Map("currency" -> "USD")))
```

---

## Best Practices

1. **Always pass a `targetingKey`** — targeting rules won't fire without it; use the user's stable ID
2. **Gate traffic on `providerStatus` with async init** — don't route requests to pods that are still in `NotReady`
3. **Use `catchSome` not `catchAll`** — `Unauthorized` and `Unreachable` need different treatment from `ProviderNotReady`
4. **Register `structuredLogging` hook early** — zero-overhead when log level doesn't match; provides observability automatically
5. **Set `evaluationTimeout` on remote providers** — prevents slow CDN from blocking fibers indefinitely
6. **Use `TestFeatureProvider` for all unit tests** — no network, no SDK key, isolated per test
7. **Prefer `fromProviderAsync` for remote providers** — sync init blocks the layer build; use if and only if "all defaults = unsafe"
8. **Use `EnvVarProvider` as the last fallback** for critical kill switches — always ready, always correct
9. **Keep hooks fast** — hooks are synchronous with evaluation; fork slow side-effects with `.forkDaemon`
10. **Domain-scope with `fromProviderWithDomain`** — prevents cross-service contamination when multiple services share a JVM

---

## Anti-Patterns

1. **`catchAll { _ => ZIO.succeed(default) }`** — swallows `Unauthorized` (needs paging) and `Unreachable` (needs alerting). Match specific cases.

2. **Async init without a readiness check** — pods advertise healthy while every flag returns its OF default. Wire `providerStatus` into your `/ready` endpoint.

3. **Sync init with CDN-backed providers on constrained networks** — the 30 s `initTimeout` will fire on cold networks in CI/staging. Use async + readiness gate instead.

4. **Storing `FeatureFlags` outside the ZIO environment** — breaks resource management (shutdown won't run) and fiber-local context (`withContext` won't propagate).

5. **Busy-polling `providerStatus == Ready`** — use `onProviderReady(handler)` to react asynchronously instead of a spin loop.

6. **Slow I/O in hooks without forking** — `after` hooks block the evaluation pipeline. Fork anything that does network I/O or disk access.

7. **Hot-swapping only the inner provider of a `CircuitBreakerProvider`** — the CB's failure count and open/closed state become meaningless for the new delegate. Swap the entire CB+delegate stack.

8. **Reusing a Production SDK key in Development** — each Optimizely environment has its own key. Using the wrong key leaks production event data and may produce incorrect targeting results.

9. **Nested transactions** — the inner `transaction {}` throws `NestedTransactionNotAllowed` immediately. Flatten all overrides into a single outer transaction.

10. **Calling `shutdown()` manually in tests** — the scope cleanup calls it. Double-shutdown causes errors. Let `ZIO.scoped` or `TestFeatureProvider.scopedLayer` handle lifecycle.

11. **`fromMultiProvider` with `firstMatch` when a provider can return errors** — `firstMatch` aborts the chain on any error. Use `firstSuccessful` when you want errors to fall through to the next provider.

12. **Not providing `Scope.default` when wiring** — all `fromProvider*` factories require a `Scope` in the environment. The layer build will fail at compile time without it.

---

## Internals — How the Library Works

This section explains the internal mechanics. Understanding it helps diagnose subtle failures and reason about why certain patterns are required.

---

### Internal State (`FeatureFlagsState`)

Every `FeatureFlags` instance owns a single `FeatureFlagsState` that holds all mutable state. There are two kinds of ZIO state used deliberately:

```
Ref[T]      — shared across all fibers using this instance
FiberRef[T] — fiber-local; each fiber sees its own value, inherited from parent at fork
```

| Field | Type | What it holds |
|-------|------|--------------|
| `globalContextRef` | `Ref[EvaluationContext]` | App-wide context (set via `setGlobalContext`) |
| `clientContextRef` | `Ref[EvaluationContext]` | Per-instance context (set via `setClientContext`) |
| `fiberContextRef` | `FiberRef[EvaluationContext]` | Fiber-local context (set via `withContext {}`) |
| `transactionRef` | `FiberRef[Option[TransactionState]]` | Active transaction state — `None` outside a transaction |
| `hooksRef` | `Ref[List[FeatureHook]]` | Client-level hooks |
| `eventHub` | `Hub[ProviderEvent]` (dropping, 256) | Broadcast channel for all provider events |
| `statusRef` | `Ref[ProviderStatus]` | Current provider status |
| `trackRecorder` | `Ref[List[...]]` | Accumulated tracking events |

`FiberRef` for `fiberContextRef` means `withContext {}` is naturally fiber-scoped — child fibers inherit the context set by their parent, and the context reverts when the block exits, matching structured concurrency semantics. It does **not** cross `fork` boundaries unless you use `forkWithFiberRef` or similar.

`transactionRef` is also a `FiberRef` so transactions are naturally fiber-local. A transaction opened in one fiber is invisible to sibling fibers — which is why nested transactions (same fiber) throw immediately, but concurrent transactions in different fibers are safe.

---

### Flag Resolution Flow — Step by Step

Every `FeatureFlags.boolean(key, default, ctx)` call walks this exact path:

```
FeatureFlags.boolean(key, default, ctx)
  └─ ZIO.serviceWithZIO(_.boolean(key, default, ctx))      // service accessor
      └─ booleanDetails(key, default, ctx).map(_.value)
          └─ evaluateWithDetails(key, default, ctx, options)
              │
              ├─ 1. Resolve timeout: options.timeout orElse evaluationTimeout (global)
              │
              ├─ 2. effectiveContext(ctx)                   // merge all 5 context levels
              │      global.merge(txContext).merge(client).merge(fiberLocal).merge(invocation)
              │
              └─ 3. runWithHooks(key, default, mergedCtx, evaluate, extraHooks, hints)
                      │
                      ├─ read hooksRef (client hooks)
                      ├─ getProviderHooks (provider.getProviderHooks, wrapped as FeatureHook)
                      ├─ allHooks = clientHooks ++ invocationHooks ++ providerHooks
                      │
                      ├─ if allHooks.isEmpty → evaluate(context) directly
                      │
                      └─ else runHookPipeline(hookCtx, allHooks, context, hints, evaluate)
                              │
                              ├─ FeatureHook.compose(allHooks)   // creates one composed hook
                              ├─ composedHook.before(hookCtx, hints)
                              │     ← may return modified (context, hints) or None
                              │
                              ├─ evaluate(effectiveCtx)          // the core evaluation
                              │     └─ evaluateFlag(key, default, context, timeout)
                              │           ├─ checkProviderStatus  ← FAIL FAST if NotReady/Error/Fatal
                              │           └─ transactionRef.get match
                              │                 Some(txState) → evaluateWithTransaction(...)
                              │                 None          → evaluateFromClient(...)
                              │
                              ├─ on success: composedHook.after(hookCtx, resolution, hints)
                              ├─ on error:   composedHook.error(hookCtx, error, hints)
                              └─ always:     composedHook.finallyAfter(hookCtx, details, hints)
```

---

### Context Merge — Exact Code

```scala
// From FeatureFlagsLive.effectiveContext — right side wins in every merge
global.merge(txContext).merge(clientCtx).merge(fiberLocal).merge(invocation)
```

`merge` is right-biased at the attribute level: if both sides have the same key, the right (higher-priority) side wins. Nested `StructValue` fields are merged recursively, not replaced wholesale.

---

### Transaction Evaluation Logic

Inside `evaluateWithTransaction`, the resolution priority is:

```
1. Explicit override (Map passed to transaction {})
      ↓ found → decode to type A; OverrideTypeMismatch if type wrong
      ↓ not found
2. Cached evaluation from earlier in same transaction
      ↓ found and type-compatible → return FlagResolution.cached (reason = Cached)
      ↓ type mismatch → fall through to live evaluation
      ↓ not found
3. evaluateFromClient → store in transaction cache
```

The transaction state lives in a `FiberRef` — it's invisible to sibling fibers. Caching (`cacheEvaluations = true`, the default) means the second call to the same flag key within the same transaction returns the cached result without hitting the provider again.

---

### `evaluateFromClient` — Provider Dispatch

The actual provider call goes through `ClientEvaluator`, which dispatches to the correct Java SDK method per type:

| Scala type | Java SDK method | Notes |
|-----------|----------------|-------|
| `Boolean` | `getBooleanDetails` | Direct |
| `String` | `getStringDetails` | Direct |
| `Int` | `getIntegerDetails` | Boxes to `java.lang.Integer` |
| `Long` | `getDoubleDetails` | **Uses Double under the hood** — exact up to 2⁵³ |
| `Float` | `getDoubleDetails` | Converts result back to Float |
| `Double` | `getDoubleDetails` | Direct |
| `Map[String, Any]` | `getObjectDetails` | Converts to/from SDK `Value`/`Structure` |
| Custom `A` (FlagType) | `getObjectDetails` | Decodes via `FlagType.decode` |

All provider calls are wrapped in `ZIO.attemptBlocking` — they run on the blocking thread pool. The evaluation timeout is applied via `.disconnect.timeoutFail(...)` which returns the error to the caller immediately while letting the blocking thread complete naturally (avoiding provider internal-state corruption from interruption).

**TOCTOU race handling:** `checkProviderStatus` runs before the SDK call, but there is a window where the provider could transition to `NotReady` after the check but before the SDK call completes. The library handles this by inspecting `resolution.errorCode` after the SDK returns — if the provider returned `ProviderNotReady` or `ProviderFatal` error codes in the resolution, the library converts them to the appropriate `FeatureFlagError`.

---

### Error Classification — `FeatureFlagError.classify`

All `Throwable` values from the Java SDK are classified through `FeatureFlagError.classify`:

```
java.net.UnknownHostException   → Unreachable   (DNS failure)
java.net.ConnectException        → Unreachable   (TCP refused)
java.net.NoRouteToHostException  → Unreachable   (routing failure)
HTTP 401/403 in message or class → Unauthorized  (auth failure)
anything else                    → ProviderError  (original cause preserved)
```

`Unauthorized` matching is message-based — the classifier looks for "401", "403", "unauthorized", "forbidden" in the exception message or class name. This is intentionally permissive.

---

### Event Bridge — Java SDK → ZIO

The Java SDK fires events on its own thread pool. The bridge in `startEventBridge` translates them into ZIO:

```
Java SDK emitter thread
  └─ client.on(PROVIDER_READY, readyHandler)      ← registered during layer init
      └─ readyHandler fires on Java thread
          └─ Unsafe.unsafe { runtime.unsafe.run(zioEffect) }
              ├─ state.statusRef.update(...)        ← updates ProviderStatus
              └─ state.eventHub.publish(event)      ← drops if hub is full (capacity 256)
```

`eventHub` is a **dropping hub** — if all 256 slots are occupied, new events are silently dropped. Subscribers reconcile via the current `statusRef` value on the next evaluation, so missing intermediate events is safe.

ZIO subscribers consume events via `ZStream.fromHub(state.eventHub)`. Each subscriber gets a backpressured stream from the hub. Event handlers (`onProviderReady` etc.) fork daemon fibers that consume this stream and call user-provided handlers.

**Immediate handler execution (spec 5.3.3):** `onProviderReady` checks `providerStatus` at registration time. If the provider is already `Ready`, the handler is called immediately before subscribing to future events.

**Stale event guard:** When `setProvider` fails (new provider doesn't init), the library stamps `recentSwapFailureAt` with the current timestamp. The `readyHandler` checks this: if a `PROVIDER_READY` event arrives within 500 ms of a failed swap, it's treated as a stale queued event from the previous provider and ignored. Real recoveries take much longer than 500 ms.

---

### Sync Init (`build`) vs Async Init (`buildAsync`)

**Sync path (`fromProvider` → `build`):**

```
1. api.setProviderAndWait(provider)    ← blocking call; runs on blocking pool
   └─ .disconnect.timeoutFail(...)(initTimeout)  ← hard ceiling
2. verifyInitState(provider)           ← reads provider.getState()
   └─ NOT READY / ERROR / FATAL → ZIO.fail(IllegalStateException)
3. FeatureFlagsState.make             ← creates all refs
4. state.statusRef.set(verified)      ← seed with actual state (Ready or Stale)
5. ZIO.addFinalizer(api.shutdown())   ← shutdown when scope closes
6. ff.startEventBridge                ← register Java SDK listeners
```

After this, the layer is in a known-good state. If step 1 or 2 fails, the layer build throws and the ZLayer system propagates the error to the caller.

**Async path (`fromProviderAsync` → `buildAsync`):**

```
1. api.setProvider(provider)          ← non-blocking; returns immediately
2. FeatureFlagsState.make             ← statusRef starts as NotReady
3. ff.startEventBridge                ← MUST be before watchdog so Ready event isn't missed
4. (ZIO.sleep(initTimeout) *>         ← watchdog fiber, forked into layer Scope
     statusRef.update {
       NotReady | Error → Fatal
       other            → other       ← doesn't overwrite Ready/Stale/ShuttingDown
     }).forkScoped
```

The watchdog fiber lives in the layer's `Scope`. If the scope closes (normal shutdown) before the timeout fires, the fiber is interrupted automatically — no leaked fibers.

The critical ordering: event bridge is registered **before** the watchdog starts and **before** any readiness check. This closes the race where the provider becomes ready during `startEventBridge` setup — if `PROVIDER_READY` fires between `setProvider` and `startEventBridge`, the Java SDK would replay it when the handler is registered.

---

### Hot-Swap Mechanics (`setProvider`)

```
swapLock.withPermit {                      ← serializes concurrent swaps
  1. statusRef.set(NotReady)               ← evaluations fail fast immediately
  2. providerRef.set(newProvider)          ← update BEFORE setProviderAndWait
  3. providerNameRef.set(newName)          ← event bridge reads dynamically; must be consistent
  4. api.setProviderAndWait(newProvider)   ← Java SDK: shuts down old, inits new
     └─ on error:
          recentSwapFailureAt.set(now)     ← stamp BEFORE statusRef write
          providerRef.set(oldProvider)     ← rollback refs
          providerNameRef.set(oldName)
          statusRef.set(Error)             ← diagnosable state
  5. statusRef.set(Ready)                  ← explicit; event bridge also fires PROVIDER_READY
}
```

The refs are updated in step 2–3 before `setProviderAndWait` so the event bridge sees consistent metadata when `PROVIDER_READY` fires during initialization of the new provider. The Java SDK `client` object is **reused** — it delegates to whatever provider is currently registered with the API, not the one it was created with.

**In-flight evaluations during a swap:** The Java SDK does not interrupt running evaluations. An evaluation that started against the old provider before `statusRef.set(NotReady)` will complete against the old provider. New evaluations that arrive after `NotReady` is set fail fast with `ProviderNotReady`.

---

### Multi-Provider Wrapping

`fromMultiProvider` wraps the provider list in the Java SDK's `MultiProvider`:

```scala
fromProvider(new MultiProvider(providers.asJava, strategy))
```

From the ZIO layer's perspective, `MultiProvider` is a single provider. The strategy logic runs entirely inside the Java SDK:

- **`FirstMatchStrategy`** (default): iterates providers in order; returns the first resolution whose `reason` is not `DEFAULT`. If any provider throws an exception, the chain aborts immediately and the error propagates as `ProviderError`.
- **`FirstSuccessfulStrategy`**: iterates providers in order; returns the first resolution that has no error code. Provider exceptions and error-code responses both cause fall-through to the next provider.

The implication: with `firstMatch`, a network failure in provider 1 stops evaluation entirely — provider 2 is never tried. With `firstSuccessful`, provider 1's `Unreachable` is swallowed and provider 2 is tried.

---

### Shutdown Sequence

`FeatureFlags.shutdown` (called automatically by the scope finalizer):

```
1. statusRef.set(NotReady)       ← new evaluations fail immediately
2. hooksRef.set(Nil)
3. globalContextRef.set(empty)
4. clientContextRef.set(empty)
5. trackRecorder.set(Nil)
6. eventHub.shutdown             ← terminates all ZStream subscribers (they see stream end)
7. api.shutdown()                ← Java SDK shuts down the provider
```

Event stream subscribers see the stream complete gracefully on step 6. Any `foreach` / `collect` fiber running against `events` will terminate rather than hang.
