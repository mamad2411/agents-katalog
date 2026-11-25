---
name: optimizely
description: >
  Optimizely Feature Experimentation concepts, gotchas, and patterns for teams
  using OpenFeature with the Optimizely Java SDK (or a custom wrapper provider).
  TRIGGER when: working with Optimizely flags, debugging flag evaluation failures,
  setting up Optimizely provider configuration, wiring Optimizely with zio-openfeature,
  or writing service-level feature flag code that calls Optimizely decisions.
  Covers: flag key naming (case sensitivity), user ID semantics, targeting rules,
  variables, decision reasons, graceful degradation, environment management, and
  integration patterns derived from real production usage.
---

# Optimizely Feature Experimentation — Concepts and Patterns

## Core Concepts

Optimizely Feature Experimentation has a specific terminology model. Understanding it is essential for correctly wiring flags.

| Term | What it is |
|------|-----------|
| **Flag** | A named toggle in Optimizely's UI. Wraps one or more rules and a set of variables. |
| **Rule** | Targeting + traffic allocation logic within a flag (audience + percentage). Two kinds: *rollout* (delivery) and *experiment* (A/B test). |
| **Variation** | A named outcome of a rule: "on" / "off" or named variants ("control", "treatment_a"). |
| **Variable** | A typed value (boolean, string, integer, double, JSON) attached to a flag. Can differ per variation. |
| **Ruleset** | The ordered list of rules for a flag in a specific environment. Evaluated top-to-bottom; first match wins. |
| **Environment** | Dev / Staging / Production — each has its own SDK key and independent ruleset. |
| **Datafile** | JSON config fetched from CDN (`cdn.optimizely.com/datafiles/<sdkKey>.json`). The SDK polls this every 30 s (default). All decisions are made locally against the datafile — no per-evaluation network call. |
| **Decision** | The SDK's response to `decide(flagKey, userContext)`: enabled/disabled, variable values, variation key, decision reason. |
| **Event** | A conversion event dispatched to Optimizely's results backend (for experiments). Not the same as OpenFeature provider events. |

---

## Flag Keys — CRITICAL Gotchas

### Flag keys are case-sensitive

This is the most common cause of silent failures. A wrong case returns the "off" variation with no error — the SDK evaluates the flag as if no rule matched.

```
"my_feature_flag"   ← correct (matches what was created in Optimizely UI)
"My_Feature_Flag"   ← wrong — treated as "flag not found in datafile", returns off
"MY_FEATURE_FLAG"   ← wrong — same
```

**Defensive pattern:** define flag keys as constants, never inline strings.

```scala
object FeatureFlagKeys:
  // Exact match of the key in Optimizely UI — do not change case
  val DummyFeatureFlag   = "dummy_feature_flag"
  val NewCheckoutFlow    = "new_checkout_flow"
  val MaxItemsLimit      = "max_items_limit"
```

### Naming convention

Optimizely enforces `[a-zA-Z0-9_-]+`, max 64 characters, no spaces. The UI and all SDK examples use **snake_case** (`new_checkout_flow`, not `newCheckoutFlow` or `new-checkout-flow`). Stick to snake_case — mixing conventions with hyphens is valid but creates confusion.

### Flag must exist in the datafile

If the flag key doesn't exist in the current datafile for the current environment, Optimizely returns "off" silently. This happens when:
- The flag was just created in the UI but the SDK hasn't polled yet (wait up to 30 s)
- The wrong environment SDK key is in use (flag exists in Prod, SDK key is for Dev)
- The flag was archived

---

## User ID — Targeting and Service-Level Usage

### Why it matters

Optimizely's targeting rules and traffic allocation are deterministic *per user ID*. The same user ID always gets the same variation (absent a datafile change). Without a user ID, targeting rules that require audience matching cannot fire — every such evaluation returns the default "off".

```scala
// Correct: always pass a stable user ID
ff.boolean("new_checkout_flow", false, EvaluationContext("user-12345"))

// Silent failure: no targeting rules can fire
ff.boolean("new_checkout_flow", false)  // no userId — will return default
```

### Service-level (non-user) evaluations

Backend services often evaluate flags for business logic, not per-user. Use a stable **service account ID** — a string that identifies the service or deployment unit. All calls with the same service ID get consistent decisions.

```scala
// Good: consistent service ID — evaluations are stable and auditable
private val ServiceUserId = "pfc-ledger"

ff.boolean("enable_new_reconciliation", false, EvaluationContext(ServiceUserId))
```

Convention: use a descriptive string like `"<service-name>"` or `"<service-name>-<env>"`. Avoid UUIDs (hard to debug in Optimizely's logs). Avoid empty string (the SDK accepts it but targeting rules that filter on userId patterns will behave unexpectedly).

### Per-user evaluations

For user-facing decisions, always pass the stable user identifier (database user ID, hashed email, etc.):

```scala
def evaluateForUser(userId: String, ctx: Map[String, AttributeValue] = Map.empty): IO[FeatureFlagError, Boolean] =
  ff.boolean(
    "premium_feature",
    default = false,
    EvaluationContext(userId).withAttributes(ctx.toList*)
  )
```

### User attributes for targeting

Pass user attributes as `EvaluationContext` attributes. These must match the attribute keys defined in Optimizely's audience builder exactly (again: case-sensitive).

```scala
val ctx = EvaluationContext("user-123")
  .withAttribute("plan", "premium")        // must match attribute key in Optimizely UI
  .withAttribute("country", "US")
  .withAttribute("beta_tester", true)

ff.boolean("beta_feature", false, ctx)
```

---

## Flag Variables

Variables let you remotely configure typed values per variation, avoiding separate flag evaluations.

Optimizely variables are accessed via typed evaluation in zio-openfeature. The **default variable key is `"value"`** — that's the variable name you should define in Optimizely's UI for simple typed flags.

```scala
// In Optimizely UI: flag "discount_rate", variable key "value", type Double
val discount = ff.double("discount_rate", default = 0.0, userCtx)

// Override variable key if you named it differently
val ctx = userCtx.withAttribute("openfeature.variableKey", AttributeValue.StringValue("rate"))
val discount = ff.double("discount_rate", default = 0.0, ctx)
```

**Typed variable mapping in Optimizely:**

| OpenFeature call | Optimizely variable type | Notes |
|-----------------|------------------------|-------|
| `ff.boolean(...)` | (none — returns `decision.getEnabled`) | Not a variable; reflects flag on/off state |
| `ff.string(...)` | `string` | Variable key must be "value" or overridden |
| `ff.int(...)` | `integer` | |
| `ff.double(...)` | `double` | |
| `ff.long(...)` | `double` (via `getDoubleDetails`) | Exact up to 2⁵³ |
| `ff.obj(...)` | `json` | Returns `Map[String, Any]` |

**Boolean is special:** `ff.boolean("flag", false, ctx)` always calls `decision.getEnabled()` — it ignores any variable named "value". Boolean evaluation = "is this flag on for this user?", nothing more.

---

## Decision Reasons → ResolutionReason

Optimizely's SDK reports *why* a decision was made. In zio-openfeature these map to `FlagResolution.reason`:

| Optimizely reason | `ResolutionReason` | Meaning |
|------------------|-------------------|---------|
| `ROLLOUT` | `TargetingMatch` | User matched a targeted delivery rule |
| `FEATURE_TEST` | `TargetingMatch` | User matched an A/B experiment rule |
| `FORCED_DECISION` | `TargetingMatch` | Manual override via `setForcedDecision` |
| `OFF` | `Default` | Flag is globally off, or user fell through all rules |
| `FLAG_OFF` | `Default` | Flag disabled at environment level |
| `RULE_NOT_FOUND` | `Default` | Ruleset exists but no rule matched (unusual) |

Debugging tip: if `reason == Default` and you expected `TargetingMatch`, check:
1. Is the flag enabled in the current environment?
2. Does the user ID match audience conditions?
3. Is the user's traffic bucket within the rollout percentage?
4. Was the datafile fetched recently (within last 30 s of a change)?

---

## Provider Setup Patterns

### Standard `zio-openfeature-optimizely` provider

```scala
import zio.openfeature.optimizely.OptimizelyProvider

// Validates SDK key shape upfront
val provider = OptimizelyProvider.make(sys.env("OPTIMIZELY_SDK_KEY"))

// Use fromProviderAsync — init involves HTTP fetch
val layer = FeatureFlags.fromProviderAsync(provider.orDie, evaluationTimeout = 500.millis)
```

### Custom/internal provider (wrapping the Optimizely Java SDK)

If your org ships an internal provider (e.g., with custom polling, access tokens, or proxy support), the setup follows the same OpenFeature provider interface:

```scala
case class OptimizelyConfig(
  sdkKey: String,
  accessToken: String,
  pollIntervalSeconds: Int = 30,
  userId: String = "my-service"   // service-level default user ID
)
```

### Graceful Degradation with EnvVar Fallback

This is the recommended production pattern for services where Optimizely connectivity is not guaranteed at startup. The `FirstSuccessfulStrategy` means: try Optimizely first; if it fails or isn't configured, fall through to EnvVar.

```scala
import dev.openfeature.sdk.FeatureProvider
import dev.openfeature.sdk.multiprovider.FirstSuccessfulStrategy
import zio.openfeature.extras.EnvVarProvider

def optimizelyLayer: ZLayer[Scope & OptimizelyConfig, Throwable, FeatureFlags] =
  ZLayer.scoped:
    for
      config      <- ZIO.service[OptimizelyConfig]
      envProvider  = EnvVarProvider()
      optimizely  <- buildOptimizelyProvider(config)
      providers    = optimizely.toList :+ envProvider   // Optimizely first, EnvVar last
      ff          <- initFeatureFlags(providers)
    yield ff

private def buildOptimizelyProvider(
  config: OptimizelyConfig
): ZIO[Scope, Nothing, Option[FeatureProvider]] =
  ZIO
    .when(config.sdkKey.nonEmpty && config.accessToken.nonEmpty):
      ZIO.logInfo("Initializing Optimizely provider") *>
        ZIO.attempt(createOptimizelyProvider(config))
    .catchAll: err =>
      ZIO
        .logWarning(s"Failed to create Optimizely provider, using EnvVar only: ${err.getMessage}")
        .as(None)

private def initFeatureFlags(
  providers: List[FeatureProvider],
  hooks: List[FeatureHook] = Nil
): ZIO[Scope, Throwable, FeatureFlags] =
  for
    _   <- ZIO.logInfo(s"Initializing feature flags with ${providers.size} provider(s)")
    env <- FeatureFlags.fromMultiProviderAsync(providers, new FirstSuccessfulStrategy()).build
    ff   = env.get[FeatureFlags]
    _   <- ZIO.foreachDiscard(hooks)(ff.addHook)
    _   <- registerEventHandlers(ff)
  yield ff
```

**Why `FirstSuccessfulStrategy` and not `FirstMatchStrategy`:**
- `FirstMatchStrategy` aborts the chain on any error — a startup network failure reaching Optimizely would propagate as `ProviderError` instead of falling through to EnvVar
- `FirstSuccessfulStrategy` treats errors as "try the next provider" — EnvVar always succeeds

**EnvVar fallback semantics:** `EnvVarProvider` returns the default value for any flag it doesn't have configured. Set only the flags that absolutely must have a non-default value during an Optimizely outage.

---

## Evaluating Flags — Service and Per-User Patterns

### Service-level evaluation (stable userId)

```scala
object FeatureFlags:
  val ServiceUserId = "my-service"  // or from config

  def isEnabled(key: String, ff: FeatureFlags): UIO[Boolean] =
    ff.boolean(key, default = false, EvaluationContext(ServiceUserId))
      .catchAll: error =>
        ZIO.logWarning(s"Flag '$key' eval failed, using default: ${error.message}").as(false)

  def stringValue(key: String, default: String, ff: FeatureFlags): UIO[String] =
    ff.string(key, default, EvaluationContext(ServiceUserId))
      .catchAll: error =>
        ZIO.logWarning(s"Flag '$key' eval failed, using default: ${error.message}").as(default)
```

### Per-user evaluation (request-scoped userId)

```scala
def checkForUser(
  flagKey: String,
  userId: String,
  attributes: Map[String, Boolean | String | Int | Double] = Map.empty
): ZIO[FeatureFlags, Nothing, Boolean] =
  val ctx = attributes.foldLeft(EvaluationContext(userId)) { case (c, (k, v)) =>
    v match
      case b: Boolean => c.withAttribute(k, b)
      case s: String  => c.withAttribute(k, s)
      case i: Int     => c.withAttribute(k, i)
      case d: Double  => c.withAttribute(k, d)
  }
  FeatureFlags.boolean(flagKey, default = false, ctx)
    .catchAll(_ => ZIO.succeed(false))
```

### Always use `catchAll` at the call site for user-facing code

```scala
// Pattern from production: always return a safe default, log the failure
def dummyFeatureFlag(ff: FeatureFlags, userId: String = ServiceUserId): UIO[Boolean] =
  ff.boolean(FeatureFlagKeys.DummyFeatureFlag, default = false, EvaluationContext(Some(userId), Map.empty))
    .catchAll: error =>
      ZIO.logWarning(s"Flag eval failed, falling back to default: ${error.message}").as(false)
```

---

## Metrics Hook Pattern

Use `FeatureHook.metricsDetailed` to record evaluation latency and success/failure per flag:

```scala
def optimizelyMetricsHook(metrics: MetricsTracker): FeatureHook =
  FeatureHook.metricsDetailed(
    onSuccess = (ctx, _, duration) =>
      metrics.recordResponseTime(
        "featureflags.evaluation",
        duration,
        Map(
          "flag"     -> ctx.flagKey,
          "provider" -> ctx.providerMetadata.name,
          "success"  -> "true"
        )
      ) *>
        metrics.incrementCounter(
          "featureflags.evaluation.count",
          1,
          Map("flag" -> ctx.flagKey, "success" -> "true")
        ),
    onError = (ctx, error, duration) =>
      metrics.recordResponseTime(
        "featureflags.evaluation",
        duration,
        Map(
          "flag"    -> ctx.flagKey,
          "success" -> "false",
          "error"   -> FeatureFlagError.toErrorCode(error).toString
        )
      ) *>
        metrics.incrementCounter(
          "featureflags.evaluation.count",
          1,
          Map(
            "flag"    -> ctx.flagKey,
            "success" -> "false",
            "error"   -> FeatureFlagError.toErrorCode(error).toString
          )
        )
  )
```

Key metrics to track:
- `featureflags.evaluation` (histogram/timing) tagged by `flag`, `provider`, `success`
- `featureflags.evaluation.count` (counter) tagged by `flag`, `success`, `error` (on failure)
- Alert on: elevated error rate for a specific flag (likely a config issue), provider switch to "EnvVarProvider" (indicates Optimizely connectivity problem)

---

## Event Handler Registration

Always register lifecycle handlers so provider state is observable in logs:

```scala
private def registerEventHandlers(ff: FeatureFlags): UIO[Unit] =
  for
    _ <- ff.onProviderReady(meta =>
           ZIO.logInfo(s"Feature provider ready: ${meta.name}"))
    _ <- ff.onProviderError((error, meta) =>
           ZIO.logError(s"Feature provider error[${meta.name}]: ${error.getMessage}"))
    _ <- ff.onProviderStale((reason, meta) =>
           ZIO.logWarning(s"Feature provider stale[${meta.name}]: $reason"))
    _ <- ff.onConfigurationChanged((_, meta) =>
           ZIO.logInfo(s"Feature provider datafile updated: ${meta.name}"))
  yield ()
```

`onConfigurationChanged` fires every time Optimizely's datafile poller picks up a new revision. Log it — it's useful to confirm changes are propagating.

---

## Environment Management

Optimizely environments are completely isolated: separate SDK keys, separate rulesets, separate datafiles.

```scala
// Each env has its own SDK key — never share between environments
case class OptimizelyConfig(
  sdkKey: String,          // from OPTIMIZELY_SDK_KEY env var
  accessToken: String,     // from OPTIMIZELY_ACCESS_TOKEN env var
  pollIntervalSeconds: Int = 30
)

// Load from env at startup — fail fast if missing in non-local envs
val config: ZIO[Any, Throwable, OptimizelyConfig] =
  for
    sdkKey      <- ZIO.attempt(sys.env("OPTIMIZELY_SDK_KEY"))
    accessToken <- ZIO.attempt(sys.env("OPTIMIZELY_ACCESS_TOKEN"))
  yield OptimizelyConfig(sdkKey, accessToken)
```

**What "different environments" means in practice:**
- A flag enabled in Production may be disabled in Dev/Staging — the datafile for each env is independent
- A new flag created in the UI takes up to 30 s to appear in each environment's SDK after the datafile is re-fetched
- Traffic allocations are per-environment — a 10% rollout in Dev is independent of a 10% rollout in Prod

---

## Testing Flags

### Unit tests — use `TestFeatureProvider`, never touch Optimizely

```scala
import zio.openfeature.testkit.*

// Override flag values directly — no SDK key, no network
val testLayer = TestFeatureProvider.layer(Map(
  FeatureFlagKeys.NewCheckoutFlow -> true,
  FeatureFlagKeys.DiscountRate    -> 0.15
))

test("new checkout flow is shown when flag is on") {
  FeatureFlags.boolean(FeatureFlagKeys.NewCheckoutFlow, false)
    .map(assertTrue(_))
}.provide(Scope.default >>> testLayer)
```

### Testing graceful degradation (Optimizely down)

```scala
test("falls back to EnvVar when Optimizely is unavailable") {
  for
    provider <- ZIO.service[TestFeatureProvider]
    _        <- provider.setStatus(ProviderStatus.Error)
    result   <- FeatureFlags.boolean(FeatureFlagKeys.DummyFeatureFlag, false)
                  .catchAll(_ => ZIO.succeed(false))
  yield assertTrue(!result)  // returns default when provider is in error state
}.provide(Scope.default >>> TestFeatureProvider.layer(Map.empty))
```

### Testing with forced decisions (integration tests, Optimizely connected)

The Optimizely Java SDK supports forced decisions for testing specific variations without audience matching. Use via `OptimizelyUserContext.setForcedDecision` if you need to test specific variation paths in integration tests.

---

## Debugging Checklist

When a flag evaluation returns `false` / default and you expect otherwise:

1. **Check flag key case** — compare the string in code to the exact key in Optimizely UI character-by-character
2. **Check environment** — is the SDK key for the environment where the flag is enabled?
3. **Check flag status** — is the flag enabled for this environment in the UI?
4. **Check userId** — was a userId passed in the context? Without it, audience rules can't match
5. **Check attributes** — do the attribute keys match exactly what's defined in Optimizely audiences?
6. **Check traffic allocation** — is the user in the rollout percentage? (Use `ResolutionReason.Default` as a signal)
7. **Check datafile freshness** — was the flag change made within the last 30 s? The SDK polls on an interval
8. **Check provider status** — is the provider in `Ready` state? Log `ff.providerStatus` or use `onProviderReady`
9. **Check metrics** — is the error counter elevated? `FeatureFlagError.toErrorCode` in the hook reveals the specific error class
10. **Check `ResolutionReason`** — use `booleanDetails` instead of `boolean` to see `reason` and `errorCode`

```scala
// Diagnostic evaluation — use booleanDetails to see exactly why
ff.booleanDetails(FeatureFlagKeys.MyFlag, false, EvaluationContext("user-123"))
  .tap { r =>
    ZIO.logInfo(s"Flag ${r.flagKey}: value=${r.value}, reason=${r.reason}, variant=${r.variant}, errorCode=${r.errorCode}")
  }
```

---

## Anti-Patterns

1. **Inline flag key strings** — one typo or wrong case causes silent defaults. Always use constants.

2. **Evaluating without a userId for rules that need targeting** — Optimizely silently returns the default variation. Always pass a userId, even a service-level one.

3. **Using the same userId for all users** — if you're running an A/B test and pass the service ID for all users, every user gets the same variation (the one the service ID was bucketed into). Use per-user IDs for experiments.

4. **Expecting instant flag changes** — the SDK polls every 30 s by default. A flag change in the UI takes up to one polling interval to propagate. Don't test flag changes in code with immediate assertions; wait at least 30 s or reduce `pollIntervalSeconds` in tests.

5. **Hardcoding `accessToken` or `sdkKey`** — these are credentials. Load from env vars or a secrets manager; never commit to source control.

6. **`catchAll { _ => default }` without logging** — you'll never know when Optimizely is failing. Always log the error before returning the default.

7. **Using `boolean` to read a variable value** — `ff.boolean(...)` always returns `decision.getEnabled()`, not any variable. To read a boolean variable, use `ff.value[Boolean](...)` with a custom `FlagType`, or rethink the flag schema.

8. **Confusing Optimizely "events" with OpenFeature provider events** — Optimizely conversion events (sent to Optimizely's results backend for experiment analysis) are completely separate from `ProviderEvent.ConfigurationChanged` and other OpenFeature lifecycle events. `ff.track(...)` sends an Optimizely conversion event.

9. **Sharing a provider instance across multiple `FeatureFlags` layers** — the Java SDK's `OpenFeatureAPI` is a singleton; creating two `FeatureFlags` layers with the same provider and `fromProvider` will conflict. Use domains (`fromProviderWithDomain`) for multiple clients.

10. **Calling `OptimizelyProvider.make(sdkKey)` synchronously without async init** — the provider fetches the datafile over HTTP. With `fromProvider` (sync), the layer build blocks until the datafile arrives. On slow networks or cold starts, this can exceed `initTimeout`. Prefer `fromProviderAsync` and gate traffic on `providerStatus`.
