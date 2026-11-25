---
name: eclipse-pde-telemetry-resilience
description: Add a fire-and-forget HTTP telemetry exporter to an Eclipse PDE / Tycho / OSGi plugin without coupling tool exit code to telemetry availability — vendored library source, native dependencies via target-platform Maven location, daemon-thread bulkhead, layered timeouts, store-and-forward retry files, flushed timestamped lifecycle logging, and defensive IApplication.start integration.
category: Build & Dependency Management
---

# Eclipse PDE Telemetry Resilience Skill

> **Skill ID:** `eclipse-pde-telemetry-resilience`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Integrate a non-critical telemetry / tool-usage-logging library into an
Eclipse PDE / Tycho headless application (`IApplication`) such that:

1. The library compiles and resolves under PDE's bundle-resolution
   model — Maven JARs cannot be dropped into `libs/` and listed under
   `Bundle-ClassPath` the way a plain Java application can.
2. A slow, hung, or unreachable telemetry server **never** stalls the
   tool, blocks JVM shutdown, or alters the tool's exit code.
3. Every lifecycle event is observable in the console even when the
   host application later replaces `System.out` with its own logging
   appender (Log4j, JUL, <host-logger>, etc.).

This skill is the **base** for any organization-specific telemetry
composer. Composer skills supply the vendor-specific payload model,
server URL, and tool-identity constants; this base skill owns the
**resilience scaffolding** and the **PDE delivery model**.

***

## 1. Scope & Intent

**In scope**

- Vendoring a telemetry library's source files into a PDE plugin (the
  PDE-correct alternative to `libs/*.jar` + `Bundle-ClassPath`).
- Delivering native-binding dependencies (e.g., JNA) as proper OSGi
  bundles via a workspace `.target` Maven `<location>`.
- Daemon-thread bulkhead (`ExecutorService` of one daemon worker).
- Layered timeouts: HTTP connect/read inside a wall-clock cap.
- Store-and-forward retry files persisted on timeout / failure.
- Flushed, timestamped, single-line lifecycle logging that survives
  late `System.out` redirection by the host's logging framework.
- Defensive `IApplication.start(...)` integration: nullable telemetry
  reference, `try/catch (Throwable)` at every call site, send invoked
  from `finally` so the codegen / build / generation result is the
  single source of truth for the tool's exit code.

**Out of scope**

- Vendor-specific payload format, server URL, tool identity (see
  composer skills).
- High-frequency telemetry (this design assumes one send per JVM run;
  see [§7 — When to harden further](#7-when-to-harden-further)).
- Submitting telemetry to the OpenTelemetry collector or any standard
  observability backend — composer skills decide the wire format.

***

## 2. Prerequisites

| Requirement | Minimum |
|---|---|
| Eclipse | 4.20+ (any version supporting the workspace's target JDK) |
| Tycho | 2.7+ for JDK 17, 4.0+ for JDK 21 |
| PDE target file | A workspace `.target` writable by the integrator |
| Maven Central reachability | For target-platform Maven `<location>` (or an internal mirror) |
| JDK | Java 8+ (uses only `java.util.concurrent`, `java.net.HttpURLConnection`) |
| PowerShell | 5.1+ on Windows or 7+ cross-platform (for verification scripts only) |

## 3. Environment & Dependencies

Before running, the agent MUST:

1. Confirm the PDE plugin's `MANIFEST.MF`, `build.properties`,
   `.classpath`, and the workspace `.target` file are writable.
2. Confirm the workspace target file's location by inspecting
   `*.target` files under the standalone-pdebuild plugin (or
   equivalent target host bundle).
3. Confirm Maven Central (or the configured internal mirror) is
   reachable — `m2e` must be able to resolve `<dependency>` entries
   added to the `.target` file's Maven `<location>`.
4. Confirm the host's `IApplication` implementation lives in a known
   plugin (`<plugin>.app/src/.../Application.java`) and is the
   integration point.
5. Bootstrap shared PowerShell utilities (recursive form per the
   [Recursive Submodule Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md)):

    ```powershell
    git submodule update --init --recursive ai-agent-rules/powershell-scripts
    ```

***

## 4. The PDE Delivery Model — Why `libs/` Doesn't Work

A plain Java application can declare a runtime dependency by dropping a
JAR into `libs/` and listing it under `Bundle-ClassPath`. **Eclipse PDE
plugins cannot reuse Maven JARs that way** because:

- There is no host classloader to add to — every class must be visible
  through OSGi bundle resolution.
- Any JAR not exposed as a proper OSGi bundle (with valid
  `MANIFEST.MF`, `Bundle-SymbolicName`, exported packages) is invisible
  to dependency resolution and to the IDE's compile path.
- Tycho consumes the workspace `.target` file, not `libs/`.

The skill mandates two PDE-correct mechanisms instead:

| Asset class | Mechanism | Why |
|---|---|---|
| Telemetry library source | **Vendor source files** into the consuming plugin under `src/<vendor>/<package>/` | Compiles and exports through the host plugin's existing OSGi metadata; no extra `Bundle-ClassPath` entry needed |
| Native-binding library (e.g., JNA) | **Maven `<location>` in the workspace `.target` file** | The Maven Central JAR already ships a valid OSGi `MANIFEST.MF`; PDE registers it as a real bundle the consuming plugin requires via `Require-Bundle` |

### 4.1 Vendoring telemetry source into the plugin

```text
<plugin>.app/
├── META-INF/MANIFEST.MF        # Bundle-ClassPath: .   (no libs/ entries)
├── build.properties            # bin.includes does NOT list libs/
├── src/
│   ├── <vendor>/<package>/     # vendored telemetry library source
│   │   ├── <Writer>.java
│   │   ├── <Config>.java
│   │   └── …
│   └── <consuming-package>/
│       ├── Application.java
│       └── <telemetry-adapter>/         # app-specific adapter (composer-defined name)
│           ├── <ToolName>Constants.java
│           └── <ToolName>Logger.java
└── (no libs/ folder)
```

What the plugin's `MANIFEST.MF` **must NOT** contain:

```manifest
# WRONG for PDE — would only work for a plain Java app:
# Bundle-ClassPath: .,
#  libs/<vendor>-logging-1.0.0.jar,
#  libs/jna-5.14.0.jar
```

What it **must** contain:

```manifest
Bundle-ClassPath: .
Require-Bundle: …,
 com.sun.jna;bundle-version="5.14.0",
 com.sun.jna.platform;bundle-version="5.14.0"
```

`build.properties` likewise drops any `libs/` entry:

```properties
source.. = src/
output.. = bin/
bin.includes = plugin.xml,\
               META-INF/,\
               .,\
               <telemetry-config>.properties
```

### 4.2 Native-binding library via the workspace `.target` file

In the workspace target file (e.g.,
`<plugin>.standalone.pdebuild/<release>.target`), add **separate**
Maven `<location>` blocks per logical package family:

```xml
<location includeDependencyScope="compile" includeSource="true"
    missingManifest="generate" type="Maven">
    <dependencies>
        <dependency>
            <groupId>net.java.dev.jna</groupId>
            <artifactId>jna</artifactId>
            <version>5.14.0</version>
            <type>jar</type>
        </dependency>
        <dependency>
            <groupId>net.java.dev.jna</groupId>
            <artifactId>jna-platform</artifactId>
            <version>5.14.0</version>
            <type>jar</type>
        </dependency>
    </dependencies>
    <!-- NO <instructions> here — JNA jars already ship correct OSGi metadata -->
</location>
```

**Critical anti-pattern** — never put a `<instructions>` block on a
Maven `<location>` containing dependencies whose original symbolic
names you want to keep. Bnd `<instructions>` apply to **every**
dependency in that location, so a `Bundle-SymbolicName` template
silently renames every JAR. Each symbolic-name override must live in
its own `<location>` block. See
[apache-commons-io-symbolic-name-aliasing.md](../eclipse-pde-jdk-migration/docs/cases/apache-commons-io-symbolic-name-aliasing.md)
for the canonical case study.

***

## 5. The Resilience Scaffolding

The integration MUST follow this five-layer defensive model. Composer
skills do NOT override these layers; they only fill in the
vendor-specific names (`<ToolName>Logger`, `<ToolName>Constants`,
server URL, payload format).

### 5.1 Threading model — daemon-thread bulkhead

All telemetry network I/O runs on a single dedicated daemon worker:

```java
private static final ExecutorService TELEMETRY_EXEC =
    Executors.newSingleThreadExecutor(new ThreadFactory() {
        @Override
        public Thread newThread(Runnable r) {
            Thread t = new Thread(r, "<ToolName>-Telemetry-Worker");
            t.setDaemon(true);   // critical: JVM exit is never held up
            return t;
        }
    });
```

| Property | Value | Why |
|---|---|---|
| Thread name | `<ToolName>-Telemetry-Worker` | Spottable in thread dumps |
| Daemon | `true` | JVM exit is **never** blocked by a hung socket |
| Pool size | 1 | Saved-log retry and current-payload send are serialized; one send-per-run is enough |
| Submission | `EXEC.submit(...).get(timeoutSec, SECONDS)` | Caller waits **at most** `timeoutSec`; on `TimeoutException` it cancels the future and proceeds |

### 5.2 Layered timeouts

| Layer | Mechanism | Default |
|---|---|---|
| **L1 — Construction** | `getInstance()` wrapped in `try/catch (Throwable)` at the call site | n/a |
| **L2 — No blocking I/O in constructor** | Saved-log retry runs lazily inside the safe wrapper, never in the singleton ctor | n/a |
| **L3 — HTTP connect/read** | `HttpURLConnection.setConnectTimeout / setReadTimeout` | **10 s** (matches OpenTelemetry OTLP, Datadog, Micrometer Prometheus) |
| **L4 — Wall-clock cap** | `Future.get(timeoutSec, SECONDS)` + `cancel(true)` on the daemon worker | **30 s** (matches OTLP exporter, Datadog flush, AWS SDK API call) |
| **L5 — Catch-all at every call site** | `try/catch (Throwable)` around every telemetry call in `IApplication.start` | n/a |

Why L3 < L4: HTTP timeout handles the common case (slow/unresponsive
server); the wall-clock cap is the belt-and-braces backstop in case a
JVM bug, JNI hang, DNS resolver, or SSL handshake somehow ignores L3.

### 5.3 Store-and-forward retry

On L3 failure or L4 timeout, persist the payload to a `.spool`-style
retry file under a writable resource directory (`user.dir` or the
plugin's resolved bundle resource path). On the next run, the safe
wrapper drains the directory **before** sending the new payload — also
under the same wall-clock bound.

### 5.4 The safe wrapper — `sendLogSafely(int)`

```java
public void sendLogSafely(final int timeoutSeconds) {
    log("sendLogSafely(timeout=" + timeoutSeconds + "s) — dispatching on daemon worker");

    // Bounded retry of saved logs.
    Future<?> retry = EXEC.submit(() -> { try { pushSavedLogToServer(); }
        catch (Exception e) { logErr("Retry of saved logs failed: " + e.getMessage()); } });
    try { retry.get(timeoutSeconds, TimeUnit.SECONDS); }
    catch (TimeoutException te) { logErr("Retry timed out after " + timeoutSeconds + "s"); retry.cancel(true); }
    catch (Exception e) { logErr("Retry aborted: " + e.getMessage()); }

    // Bounded send of current payload.
    Future<?> send = EXEC.submit(() -> { try { sendLog(); }
        catch (Throwable t) { logErr("sendLog failed: " + t); persistForRetry(); } });
    try { send.get(timeoutSeconds, TimeUnit.SECONDS); }
    catch (TimeoutException te) { logErr("sendLog timed out after " + timeoutSeconds + "s"); send.cancel(true); persistForRetry(); }
    catch (Exception e) { logErr("sendLog aborted: " + e.getMessage()); }
}
```

The synchronous `sendLog()` remains the underlying primitive.
**Production code paths must call `sendLogSafely(...)`**; never call
`sendLog()` directly from `IApplication.start`.

### 5.5 SSL trust note (optional)

Some internal corporate CAs expire and the truststore lags behind. A
**non-sensitive telemetry endpoint** MAY install a trust-all
`X509TrustManager` to avoid blocking tool workflows on certificate
validation failures. The trust-all manager MUST be scoped to the
telemetry exporter only — never to the host application's general
HTTPS client.

***

## 6. Flushed Timestamped Lifecycle Logging

The host application (Equinox + <host-logger> / Log4j / JUL) typically
**replaces `System.out`** with its own appender shortly after
`IApplication.start(...)` begins. Anything written without an explicit
`flush()` to the original `PrintStream` will be discarded when the
appender swap happens.

### 6.0 Line format (standardized)

```
[<TAG> <ISO-8601 ts with TZ offset> <LEVEL>] <message>
```

Example:

```
[telemetry 2026-05-11T18:48:11.415+02:00 INFO ] Application.start — initializing telemetry
```

| Field | Choice | Rationale |
|---|---|---|
| Channel tag `[<TAG>]` | Fixed short string per tool (e.g. `[telemetry]`, `[OTEL]`) | Grep-friendly demux from co-mingled Eclipse / <host> / Equinox stdout |
| Timestamp | `yyyy-MM-dd'T'HH:mm:ss.SSSXXX` via `OffsetDateTime.now()` | RFC 3339 / ISO 8601 with offset — sortable across timezones; native parse by Elasticsearch, CloudWatch, OpenTelemetry |
| Level | 5-char fixed-width (`TRACE` / `DEBUG` / `INFO ` / `WARN ` / `ERROR`) | Enables runtime severity gating; aligned columns for human scanning |
| Message | Free-text prose for now; structured payload (JSON / ECS) deferred until SIEM ingestion is required | Bootstrap-safe (no logging-framework dependency); migration is formatter-local |

The skill mandates the helper shape below and uses it for **every**
line. Public API is `log` / `debug` / `trace` / `warn` / `logErr` — all
back-compatible no-arg-list aliases over an internal `emit(Level, msg)`
gated by a runtime threshold:

```java
public enum Level { TRACE, DEBUG, INFO, WARN, ERROR }

private static final DateTimeFormatter TS_FMT =
    DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSSXXX");

private static volatile Level threshold = parseLevel(
    System.getProperty("<tag>.log.level"), Level.INFO);

private static void emit(Level lvl, String msg, boolean toStdErr) {
    if (lvl.ordinal() < threshold.ordinal()) { return; }
    String line = String.format("[<TAG> %s %-5s] %s",
        OffsetDateTime.now().format(TS_FMT), lvl.name(), msg);
    PrintStream out = toStdErr ? System.err : System.out;
    out.println(line);
    out.flush();
}

public static void log   (String m) { emit(Level.INFO , m, false); }
public static void debug (String m) { emit(Level.DEBUG, m, false); }
public static void trace (String m) { emit(Level.TRACE, m, false); }
public static void warn  (String m) { emit(Level.WARN , m, false); }
public static void logErr(String m) { emit(Level.ERROR, m, true ); }
```

Threshold override: `-D<tag>.log.level=DEBUG` (default `INFO`). DEBUG /
TRACE call-sites cost a single ordinal compare when disabled, so
per-byte HTTP traces or JNA call traces can be left in production code.

#### 6.0.1 Industry-standard alignment & deliberate deviations

The format above follows the *spirit* of every relevant logging
standard while deliberately dropping bureaucratic ornaments that don't
serve a bootstrap-safe, console-grep workflow. Each row below is one
conscious trade-off:

| Aspect | Industry-standard prescription | This skill | Why this deviation is acceptable |
|---|---|---|---|
| **Lifecycle banner** | OTel SDK "SDK starting"; SLF4J/Logback startup banners; systemd `Started …` | Pre-init `Application.start — initializing telemetry` line before any fallible call | ✅ **Follows the standard** — emit before the subsystem that can fail, so init crashes leave evidence |
| **Timestamp** | RFC 3339 / ISO 8601 with offset (`2026-05-11T18:48:11.415+02:00`); default in Log4j2, Logback, JUL, OTel logs spec | Same — `yyyy-MM-dd'T'HH:mm:ss.SSSXXX` via `OffsetDateTime.now()` | ✅ **Follows the standard** — enables cross-timezone aggregation (India + Germany + USA build farms into one Elastic/CloudWatch index) |
| **Channel tag** | Common in CLI tools (`[INFO]`, `[gradle]`, `[npm WARN]`); OTel uses `instrumentation.scope.name` | `[<TAG>]` short fixed string in square brackets | ✅ **Follows the standard pattern** — grep-friendly demux of co-mingled stdout |
| **Severity field** | RFC 5424 / OTel / SLF4J: include level (`INFO`, `DEBUG`, …) on every line | 5-char fixed-width (`TRACE` / `DEBUG` / `INFO ` / `WARN ` / `ERROR`); runtime threshold via `-D<tag>.log.level` | ✅ **Follows the standard** — lets users hide future DEBUG/TRACE diagnostics (per-byte HTTP, JNA call traces) at runtime |
| **Defensive logging before instantiation** | "Telemetry must never break the request" — Netflix Hystrix, Google SRE workbook | Pre-init banner emitted *before* `getInstance()`; all helpers swallow exceptions | ✅ **Follows the standard** |
| **Stream-swap survival** | Specific to PDE / OSGi hosts that hijack `System.out` | Saved `PrintStream` reference (when applicable) + explicit `flush()` on every line | ✅ **Standard for this host class** — Eclipse PDE / Equinox swap stdout shortly after `IApplication.start` |
| **Structured payload** | OTel Logs Data Model / Elastic Common Schema (ECS) / GELF: key-value or JSON body | Free-text prose body (`status=SUCCESS, misc='…'`) | ⚠ **Deferred** — bootstrap-safe (no logging-framework dependency); not yet needed because logs are read by support engineers, not piped to a SIEM dashboard. See §6.0.2 |
| **Logger name** | SLF4J convention: fully-qualified class name (`<vendor>.…<Tool>Logger`) | Short channel tag (`[telemetry]`) | ⚠ **Deferred** — every line in this subsystem is from the same emitter; FQNs are noise until ≥ 3 internal classes exist. See §6.0.2 |

> **Bottom line.** Six of eight dimensions match named standards
> (ISO 8601, RFC 5424, RFC 3339, OTel Logs, SLF4J banner pattern,
> SRE defensive-telemetry). Two dimensions — structured payload and
> FQN logger name — are intentionally simplified for now, with a
> clearly-scoped upgrade path documented below.

#### 6.0.2 Deferred-upgrade path

When the consuming tool needs to ship telemetry into an enterprise log
aggregator (SIEM / Elastic / Splunk / Datadog), the migration is
**formatter-local** — all `emit(...)` call-sites are already correct.
Apply the upgrades in the order below; each step is independent:

| Step | Trigger | Change | Public-API impact |
|---|---|---|---|
| **U1 — Structured JSON body** | First time someone asks for a Grafana / Kibana panel ("p95 send duration", "failure rate by component") | Swap the `emit()` body to ECS-JSON or OTel Logs Data Model encoding; gate via `-D<tag>.log.format=json` (default `text`) | None — call-sites unchanged |
| **U2 — FQN logger name** | When the wrapper grows ≥ 3 internal classes that should be distinguishable (e.g. `<Tool>Logger`, `<Tool>Sender`, `<Tool>RetryDaemon`) | Replace `[<TAG>]` with `[<short-fqn>]` (e.g. `[<o.p.q.r.s.t.u>.<Tool>Logger]`) — derive once per emitter via `MethodHandles.lookup().lookupClass()` | None — channel tag becomes class-bound but format is identical |
| **U3 — Native OTel SDK** | When the host application adopts OpenTelemetry as its full observability backbone | Replace the hand-rolled formatter with the OTel Java SDK `LoggerProvider`; keep the `[<TAG>]` scope name as `instrumentation.scope.name` | None for callers; build adds `io.opentelemetry:opentelemetry-api` + exporter |

Each upgrade is reversible by toggling the corresponding sysprop, so
they can be rolled out per-environment (e.g. JSON in production,
text in developer Eclipse launches).

### 6.1 Lifecycle event catalogue

Every phase MUST emit at least one line so the run is fully traceable.
Examples below use `[telemetry]` as the channel tag and the standardized
ISO-8601-with-offset timestamp format from §6.0:

| Phase | Level | Example line |
|---|---|---|
| Pre-init banner (Application) | INFO | `[telemetry 2026-05-11T18:48:11.415+02:00 INFO ] Application.start — initializing telemetry` |
| Constructor | INFO | `[telemetry …+02:00 INFO ] Initialized for <TOOL> <VER> (resource=…, test=false, server=…, httpTimeout=10000ms)` |
| Init failure (rare) | ERROR | `[telemetry …+02:00 ERROR] Initialization failed; continuing without telemetry: <ExceptionType> — <message>` |
| `sendLogSafely` dispatch | INFO | `[telemetry …+02:00 INFO ] sendLogSafely(timeout=30s) — dispatching on daemon worker '<TAG>-Worker'` |
| Saved-log retry done | INFO | `[telemetry …+02:00 INFO ] Saved-log retry completed in <N>ms` |
| Saved-log retry timeout | ERROR | `[telemetry …+02:00 ERROR] Retry of saved logs timed out after 30s — server unreachable; tool will continue.` |
| Pre-send summary | INFO | `[telemetry …+02:00 INFO ] Sending <N> LogDetail(s) for <TOOL> — components=[…], features=[…], status=…, misc='…'` |
| Send success | INFO | `[telemetry …+02:00 INFO ] Log sent successfully for <TOOL> in <N>ms` |
| Send failure (HTTP) | INFO | `[telemetry …+02:00 INFO ] Log failed in <N>ms — saving for retry: <server message>` |
| Send skipped | INFO | `[telemetry …+02:00 INFO ] Log skipped after <N>ms: <reason>` |
| Wall-clock timeout | ERROR | `[telemetry …+02:00 ERROR] sendLog timed out after 30s — server unreachable; saving for retry on next run.` |
| Persistence | INFO | `[telemetry …+02:00 INFO ] Payload persisted to <resource-path>/<gmt-time>.spool` |
| `sendLogSafely` finished | INFO | `[telemetry …+02:00 INFO ] sendLogSafely completed in <N>ms` |

If a run shows **zero** `[<TAG>]` lines, the new bytecode wasn't picked
up (PDE `bin/` cache stale) — instruct the user to do a clean rebuild
of the consuming plugin.

***

## 7. Defensive `IApplication.start` Integration

```java
@Override
public Object start(final IApplicationContext context) throws Exception {
    final String[] args = (String[]) context.getArguments().get("application.args");
    int errorlevel = 1;

    // L1 — Construction is defensive; logger may be null.
    <ToolName>Logger.log("Application.start — initializing telemetry");
    <ToolName>Logger logger = null;
    try { logger = <ToolName>Logger.getInstance(); }
    catch (Throwable t) {
        <ToolName>Logger.logErr("Initialization failed; continuing without telemetry: "
            + t.getClass().getSimpleName() + " — " + t.getMessage());
    }

    try {
        errorlevel = doRealWork(args);
        if (logger != null) {
            logger.setFeature("<component>", "<feature>");
            logger.setStatus(errorlevel == 0 ? "SUCCESS" : "FAILURE");
            logger.setMisc("…");
        }
    }
    catch (Exception e) {
        errorlevel = 1;
        if (logger != null) {
            try {
                logger.setFeature("<component>", "<feature>");
                logger.setStatus("FAILURE");
                logger.setMisc("error=" + e.getMessage());
            }
            catch (Throwable ignored) { /* must never mask the real error */ }
        }
        throw e;
    }
    finally {
        // L4/L5 — bounded send; never throws; never blocks JVM exit.
        if (logger != null) {
            logger.sendLogSafely(<ToolName>Logger.DEFAULT_SAFE_TIMEOUT_SECONDS);
        }
    }

    return errorlevel;
}
```

***

## 8. When to Harden Further

For a once-per-run, fire-and-forget tool-usage ping the design above is
the right size. If usage shifts to high-frequency or multi-call
patterns, the conventional next steps are:

1. **Bounded queue + drop policy** — replace the unbounded executor
   submission with `LinkedBlockingQueue(capacity)` so a sustained
   outage cannot grow memory.
2. **Circuit breaker** — Resilience4j `CircuitBreaker`: after N
   consecutive failures, short-circuit for a cooldown window.
3. **Exponential backoff on the spool retry** — instead of
   unconditionally draining `*.spool` files on every startup.
4. **Self-metrics** — count `<tag>.send.success` / `.failure` /
   `.timeout` to dashboard the dashboarder.

***

## 9. Step-by-Step Protocol

The agent MUST execute these phases in order. Composer skills inject
their vendor-specific values at the points marked `<…>`.

### Phase 1 — Survey

1. Locate the consuming plugin (the one whose `IApplication` is the
   integration point).
2. Locate the workspace target file (typically
   `<plugin>.standalone.pdebuild/<release>.target`).
3. Inspect `MANIFEST.MF`, `build.properties`, `.classpath` for any
   pre-existing `libs/` references that must be removed.

### Phase 2 — Vendor library source

1. Create `src/<vendor>/<package>/` inside the consuming plugin and
   add the telemetry library's source files (the composer skill
   specifies which files).
2. Create `src/<consuming-package>/<adapter-package>/` and add:
    - `<ToolName>Constants.java` — tool identity constants
      (`TOOL_NAME`, `TOOL_VERSION`, `RESOURCE_PATH` resolution that
      handles OSGi `bundleresource:` URI scheme by falling back to
      `user.dir`).
    - `<ToolName>Logger.java` — singleton facade implementing
      everything in §5–§6.

### Phase 3 — Wire native dependencies via the target file

1. Add a Maven `<location>` block per logical package family (see
   §4.2).
2. NEVER share `<instructions>` across families.
3. Add the corresponding `Require-Bundle` entries to the consuming
   plugin's `MANIFEST.MF`.
4. Reload the target platform from inside the IDE
   (Window → Preferences → Plug-in Development → Target Platform →
   select active → Reload).

### Phase 4 — Configuration file

1. Add `<telemetry-config>.properties` at the consuming plugin's root
   with at least:

    ```properties
    <vendor>.server.url=<server-url>
    <vendor>.timeout=10
    ```

2. Register it in `build.properties`'s `bin.includes`.

### Phase 5 — Defensive `IApplication.start` integration

Implement the §7 template, making sure to:

- Use the flushed `log()` / `logErr()` helpers from `<ToolName>Logger`
  for the pre-init banner.
- Wrap `getInstance()` in `try/catch (Throwable)`.
- Null-guard every subsequent telemetry call.
- Call `sendLogSafely(...)` from `finally` only.

### Phase 6 — Verification

1. **Clean rebuild** the consuming plugin (PDE `bin/` cache must be
   purged).
2. **Healthy-network run** — confirm the first console line is the
   pre-init banner and that the run logs `Log sent successfully … in
   <N>ms`.
3. **Hosts-file smoke test** — add `127.0.0.1 <server-host>` to the
   host's `hosts` file, run the tool, confirm:
    - codegen / build `errorlevel` is unchanged,
    - log includes `sendLog timed out after 30s`,
    - a new `*.spool` file exists under `RESOURCE_PATH`.
4. **Restore `hosts`** — next run logs
   `Saved-log retry completed in <N>ms` and removes the `*.spool` file.

***

## 10. Verification Checklist (composer-agnostic)

- [ ] No `libs/` directory remains in the consuming plugin.
- [ ] `Bundle-ClassPath: .` (no JAR entries).
- [ ] `.classpath` contains no `<classpathentry kind="lib" …>` JAR
      entries for the telemetry stack.
- [ ] `build.properties` `bin.includes` does not list `libs/`.
- [ ] Workspace `.target` has separate Maven `<location>` blocks per
      logical package family — none share `<instructions>`.
- [ ] First console line of every run is the timestamped pre-init
      banner.
- [ ] Constructor line shows resolved `server=`, `httpTimeout=`,
      `resource=`, `test=`.
- [ ] Disconnecting from the corporate network (or blocking the
      telemetry host) does not change the tool's exit code.
- [ ] Lifecycle lines appear at every phase (dispatch / retry /
      pre-send / send-result / persistence / completion).
- [ ] Send-success line includes elapsed `… in <N>ms`.
- [ ] Off-network: a `<gmt-time>.spool` file appears in `RESOURCE_PATH`;
      next on-network run drains it.
- [ ] Daemon worker thread name appears in any thread dump as
      `<ToolName>-Telemetry-Worker`.

***

## 11. Industry Standards Mapping

| What the skill mandates | Industry name | Authoritative reference |
|---|---|---|
| Telemetry on a separate daemon thread pool | **Bulkhead isolation** | Michael Nygard, *Release It!* (2nd ed., Ch. 5); Netflix Hystrix; Resilience4j `Bulkhead` |
| Daemon thread so JVM exit is never blocked | Standard JVM guidance | `java.lang.Thread` Javadoc; OpenTelemetry, Micrometer, Log4j Async appender, `java.util.logging` handlers |
| `Future.get(timeout, …)` + `cancel(true)` on timeout | **Timeout pattern** | Brian Goetz, *Java Concurrency in Practice* §6.3.7 ("Timed tasks") |
| `try/catch (Throwable)` boundary at every call site | **Defensive boundary / observer isolation** | SLF4J, OpenTelemetry SDK `SafeLogger` / `ThrowableHandler`, GC logging |
| Persist payload locally and retry next run | **Store-and-forward / outbox pattern** | Sentry, Datadog Agent, AWS CloudWatch Agent, Application Insights, Azure Monitor; Chris Richardson, *Microservices Patterns* Ch. 3 |
| Short HTTP timeout inside a longer wall-clock cap | **Layered timeouts** | Google SRE Book Ch. 22 ("Addressing Cascading Failures"); AWS Builders' Library — *Timeouts, retries, and backoff* |
| Telemetry must never affect business outcome | **"Observability is best-effort"** | OpenTelemetry spec §SDK Error Handling: *"The SDK MUST NOT throw exceptions to the user code."* |

### 11.1 Default-timeout precedent

| Library | Default network timeout |
|---|---|
| OpenTelemetry OTLP exporter | 10 s |
| Datadog Java tracer | 10 s request, 30 s shutdown flush |
| Micrometer Prometheus push | 10 s |
| AWS SDK default API call | 30 s |
| New Relic Java agent harvest | 60 s |
| Sentry Java SDK shutdown flush | 2 s (worker keeps running afterwards) |

The skill's defaults of **10 s HTTP** + **30 s wall-clock** lie in the
center of this distribution — generous enough to survive a first-call
SSL handshake over VPN, tight enough to bound the user-visible wait.

***

## 12. Composition by Higher-Level Skills

No composers are registered in this public repository. Organization-specific
composers (which supply the vendor's payload model, server URL, JAR / source
set, and tool-identity constants) live in the organization's own private
skills repository and MUST link back to this base in their **Composition
Rationale** section so the dependency graph remains bidirectionally
discoverable from the consuming side.

***

## 13. Related Skills

- [eclipse-launch-stdout-capture](../eclipse-launch-stdout-capture/SKILL.md)
  — capture the lifecycle lines emitted by this skill into a persistent
  artifact by patching the host's Eclipse `.launch` file with
  `org.eclipse.debug.ui.ATTR_CAPTURE_IN_FILE`. Without this complement,
  the lines exist only in the in-memory Eclipse Console view and
  vanish when the run ends.
- [eclipse-pde-jdk-migration](../eclipse-pde-jdk-migration/SKILL.md) —
  the broader PDE migration playbook; contains the canonical
  apache-commons-io case study showing the same target-file Maven
  `<location>` mechanism with **deliberate** symbolic-name aliasing.
- [git-atomic-commit-construction](../git-atomic-commit-construction/SKILL.md)
  — for arranging the integration as two atomic commits (resilience
  code + properties; documentation).
- [maven-pom-audit](../maven-pom-audit/SKILL.md) — when the consuming
  plugin's `pom.xml` also needs grooming.

***

## 14. Reference Implementation

The first production consumer was an Eclipse PDE workspace whose
original telemetry implementation did blocking I/O in the singleton
constructor and used 5 s / 8 s timeouts that false-tripped on
first-call SSL handshakes; the daemon-worker bulkhead with the
10 s HTTP / 30 s wall-clock defaults specified by this skill
eliminated both failure modes. Concrete file layouts, anonymized
post-mortems, and additional case studies live in the
organization-specific composer skill's private repository.

***

## 15. Related Conversations & Traceability

- Initial implementation conversation — to be archived under
  `docs/conversations/` after redaction per the
  [Redaction & Portability Skill](../redaction-portability/SKILL.md).
