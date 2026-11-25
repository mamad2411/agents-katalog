---
name: java-classpath-telemetry-integration
description: Add a synchronous, fire-and-forget HTTP telemetry / tool-usage-logging library to a plain Java CLI application packaged as a Jar-in-Jar runnable JAR — JAR-on-classpath delivery via `libs/`, classpath `<vendor>.properties` resolution with sysprop/env override layers, classpath-resource version SSOT, `rsrc:` → `user.dir` resource-path fallback, log4j-based lifecycle logging, and `*.spool` store-and-forward retry on the next run.
category: Build & Dependency Management
---

# Java Classpath Telemetry Integration Skill

> **Skill ID:** `java-classpath-telemetry-integration`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Sibling base**: [`eclipse-pde-telemetry-resilience`](../eclipse-pde-telemetry-resilience/SKILL.md) — the OSGi / PDE / Tycho counterpart

## Description

Integrate a non-critical telemetry / tool-usage-logging library into a
**plain Java CLI application** that is packaged as a runnable JAR
(typically via Eclipse's Jar-in-Jar Loader, the Maven Shade plugin, the
Gradle Shadow plugin, or an Ant `<jar>` task with `<zipfileset>`-bundled
deps).

This is the **classpath-JAR variant** of telemetry integration. It is
deliberately simpler than the
[OSGi / PDE variant](../eclipse-pde-telemetry-resilience/SKILL.md)
because a plain Java CLI tool has:

- A short-lived JVM (`main` returns → process exits) — no Equinox
  application thread, no IDE-hosted runs, no long-running container.
- A traditional classloader — Maven JARs can be dropped into `libs/`
  and listed on the classpath without ceremony.
- A user already prepared to wait for the tool to complete — the
  daemon-thread bulkhead with bounded wall-clock cap from the PDE
  variant is overkill here.

This base skill is consumed by organization-specific composer skills
that supply the vendor's payload model, server URL, and tool identity.
Those composers live in the organization's own private skills
repository.

***

## 1. Scope & Intent

**In scope**

- Adding the telemetry library and its native bindings (e.g., JNA) as
  JARs under `libs/`.
- Wiring them onto **both** compile paths used in a typical Eclipse
  workspace: the IDE's `.classpath` AND the Ant / Maven / Gradle build
  script.
- Bundling the JARs into the runnable JAR via Eclipse Jar-in-Jar
  Loader's `Rsrc-Class-Path` (or the moral equivalent for Shade /
  Shadow / `<zipfileset>`).
- A classpath `<vendor>.properties`-style configuration file plus
  sysprop / env override layers.
- A classpath-resource version SSOT read by both the build and the
  runtime.
- Resource-path resolution that survives the runnable JAR's `rsrc:`
  URI scheme.
- log4j-based lifecycle logging.
- `*.spool`-style store-and-forward retry that drains on the **next**
  process invocation (no in-process background worker required).
- Defensive `main(...)` integration: the telemetry singleton is
  initialized after argument validation, `setFeature` /
  `setStatus` / `setMisc` are called as the work progresses, and
  `sendLog()` is invoked from a `finally` block so the tool's exit
  code is the single source of truth for success.

**Out of scope**

- Vendor-specific payload format, server URL, tool identity (see
  composer skills).
- High-frequency telemetry, bounded queues, circuit breakers — use
  the [PDE variant](../eclipse-pde-telemetry-resilience/SKILL.md)
  or escalate to OpenTelemetry / Micrometer for those cases.
- Long-lived JVM processes — see "When to escalate" in §10.

***

## 2. Prerequisites

| Requirement | Minimum |
|---|---|
| JDK | Java 8+ |
| Build tool | Ant 1.7+, Maven 3.6+, or Gradle 6+ |
| Runnable-JAR mechanism | Eclipse Jar-in-Jar Loader, Maven Shade, Gradle Shadow, or Ant `<zipfileset>` |
| Eclipse (optional, if `.classpath` is committed) | 4.20+ |
| Maven Central reachability | To fetch the telemetry library's JAR and native bindings |

***

## 3. Environment & Dependencies

Before running, the agent MUST:

1. Confirm the project is a plain Java application (no `MANIFEST.MF`
   `Bundle-SymbolicName`, no `plugin.xml`, no Tycho `pom.xml`). If
   PDE/OSGi markers are present, switch to the
   [PDE variant](../eclipse-pde-telemetry-resilience/SKILL.md)
   instead.
2. Confirm the build script's classpath assembly idiom (Ant
   `<zipfileset>` + `Rsrc-Class-Path`, Maven Shade `<artifactSet>`,
   Gradle Shadow `mergeServiceFiles()`, etc.) — vendor JARs must end
   up inside the final runnable JAR.
3. Confirm a `version.properties` or equivalent SSOT pattern exists
   (or create one) so build and runtime never disagree on
   `TOOL_VERSION`.
4. Bootstrap shared PowerShell utilities (recursive form per the
   [Recursive Submodule Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md)):

    ```powershell
    git submodule update --init --recursive ai-agent-rules/powershell-scripts
    ```

***

## 4. Delivery Model — JARs in `libs/`, Bundled into the Runnable JAR

A plain Java CLI tool can use the conventional JAR delivery model. The
key is to wire **both** paths consistently:

| Path | Owner | Mechanism |
|---|---|---|
| IDE compile (`bin/`) | Eclipse `.classpath` | `<classpathentry kind="lib" path="libs/<jar>"/>` per JAR; OR a project-reference `<classpathentry kind="src" path="/<vendor-src-project>"/>` when the vendor is also imported as a workspace project |
| CLI compile (`javac`) | Build script | Glob `-cp "libs/*"` |
| Runtime as fat JAR | Build script | Vendor JAR copied **into** the runnable JAR root and listed in the manifest's `Rsrc-Class-Path` (Jar-in-Jar) / Shade `relocations` / Shadow `mergeServiceFiles` |

### 4.1 Eclipse `.classpath` template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<classpath>
    <classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER"/>
    <classpathentry kind="src" path="src"/>
    <classpathentry kind="lib" path="libs/<telemetry-lib>-<ver>.jar"/>
    <classpathentry kind="lib" path="libs/jna-<ver>.jar"/>
    <classpathentry kind="lib" path="libs/jna-platform-<ver>.jar"/>
    <!-- Optional: when the telemetry library is also imported as a workspace project for live debugging -->
    <classpathentry combineaccessrules="false" kind="src" path="/<telemetry-src-project>"/>
    <classpathentry kind="output" path="bin"/>
</classpath>
```

### 4.2 Eclipse Jar-in-Jar Loader manifest

```xml
<manifest>
    <attribute name="Main-Class" value="org.eclipse.jdt.internal.jarinjarloader.JarRsrcLoader"/>
    <attribute name="Rsrc-Main-Class" value="<your-package>.Application"/>
    <attribute name="Class-Path" value="."/>
    <attribute name="Rsrc-Class-Path" value="./
        <telemetry-lib>-<ver>.jar
        jna-<ver>.jar
        jna-platform-<ver>.jar"/>
</manifest>
<zipfileset src="${dir.buildfile}/jar-in-jar-loader.zip"/>
<fileset dir="${dir.project}/bin"/>
<zipfileset dir="${dir.project}/libs" includes="<telemetry-lib>-<ver>.jar"/>
<zipfileset dir="${dir.project}/libs" includes="jna-<ver>.jar"/>
<zipfileset dir="${dir.project}/libs" includes="jna-platform-<ver>.jar"/>
```

### 4.3 The compile-path duality rule

Eclipse and the build script MUST agree on the telemetry library
version. Two common patterns:

| Pattern | When | Risk |
|---|---|---|
| IDE references workspace source project `/<vendor-src>`; build script uses pre-built `libs/<vendor>-<ver>.jar` | When you actively develop the vendor library | Easy to forget to rebuild the JAR after editing source; the verification checklist must include "rebuild vendor JAR" |
| Both reference `libs/<vendor>-<ver>.jar` | When you only consume the vendor library | None |

***

## 5. Configuration Resolution Layers

Every configuration key MUST be resolvable through the following
chain, in order, first non-null wins:

1. **JVM system property** — `-D<vendor>.<key>=…`
2. **OS environment variable** — `<VENDOR>_<KEY>` (uppercase,
   underscores)
3. **Classpath `<vendor>.properties` file** — shipped at
   `src/<vendor>.properties`, copied to `bin/<vendor>.properties` by
   the IDE, and bundled at the root of the runnable JAR
4. **Hard-coded defaults** inside the vendor library

This precedence MUST be implemented inside the vendor library; the
adapter (`<ToolName>Constants` / `<ToolName>Logger`) does NOT
reimplement it.

### 5.1 What to ship in the properties file

Only the keys you want to **pin** for this tool. Leave timeouts and
other knobs at the library's default unless you have a documented
reason to deviate.

```properties
<vendor>.server.url=<production-server-url>
```

***

## 6. Version SSOT — One File, Read by Build and Runtime

```text
src/version.properties        # single source of truth
```

```properties
# Read by Java (classpath resource) and by the build (property file).
version=<MAJOR.MINOR.PATCH>
```

| Consumer | Mechanism |
|---|---|
| Ant build | `<property file="${dir.project}/src/version.properties"/>` then `${version}` everywhere it's needed |
| Maven build | `<resource><directory>src</directory><includes><include>version.properties</include></includes></resource>` + `${project.version}` filtering |
| Java runtime | `<ToolName>Constants.class.getResourceAsStream("/version.properties")` |

If the property file is missing or unreadable at runtime, the constant
MUST resolve to `"UNKNOWN"` (defense in depth — telemetry still sends,
the dashboard just shows the placeholder).

***

## 7. Resource-Path Resolution — Handling the `rsrc:` Scheme

Inside a Jar-in-Jar Loader runnable JAR,
`Class.getProtectionDomain().getCodeSource().getLocation().toURI()`
returns a `rsrc:` URI — NOT a real filesystem path. Calling
`Paths.get(uri)` on it throws `FileSystemNotFoundException`.

The skill mandates this resolver in `<ToolName>Constants`:

```java
private static String getResourcePath() {
    try {
        URI jarUri = <ToolName>Constants.class
            .getProtectionDomain()
            .getCodeSource()
            .getLocation()
            .toURI();
        // Skip non-file schemes (e.g. rsrc: from Jar-in-Jar Loader)
        if (!"file".equals(jarUri.getScheme())) {
            return System.getProperty("user.dir") + File.separator;
        }
        Path jarPath = Paths.get(jarUri).getParent();
        return jarPath.toString() + File.separator;
    }
    catch (URISyntaxException | RuntimeException e) {
        return System.getProperty("user.dir") + File.separator;
    }
}
```

| Runtime context | `getLocation()` scheme | Resolved path |
|---|---|---|
| IDE (`bin/`) | `file:` | Directory containing `bin/` |
| Plain CLI compile (`javac -d bin`) | `file:` | Directory containing `bin/` |
| Runnable JAR via Jar-in-Jar Loader | `rsrc:` | Falls back to `user.dir` |
| Maven Shade fat JAR | `file:` | Directory containing the fat JAR |
| Unexpected scheme / runtime error | (any) | Falls back to `user.dir` |

The trailing `File.separator` is part of the contract — callers
concatenate the filename directly.

***

## 8. log4j-Based Lifecycle Logging

A plain Java CLI app typically initializes log4j (or `java.util.logging`,
or SLF4J) at the very top of `main(...)`. Because no later code swaps
appenders, the telemetry singleton can simply use the standard logger
factory:

```java
private static final Logger LOGGER = Logger.getLogger(<ToolName>Logger.class);
```

Three lifecycle lines are sufficient for a one-shot CLI:

| Phase | Level | Example |
|---|---|---|
| Send success | `INFO` | `<vendor> log sent successfully for <TOOL>` |
| Send failure (HTTP) | `WARN` | `<vendor> log failed — saving for retry: <server message>` |
| Saved-log push failure | `WARN` | `Unable to push saved <vendor> log: <gmt-timestamp>.spool` |

The pre-init banner, dispatch line, retry-completion line, and
wall-clock-timeout line from the
[PDE variant](../eclipse-pde-telemetry-resilience/SKILL.md#6-flushed-timestamped-lifecycle-logging)
are NOT required here — there is no `System.out` swap to defend
against and no background worker to observe.

***

## 9. Defensive `main(...)` Integration

```java
public static void main(String[] args) {
    // 1. Argument validation, log4j init, output dir creation, ...
    if (!parseAndValidate(args)) { /* errorlevel set elsewhere */ return; }
    LoggerUtils.initlizeLogger(outputPath);

    // 2. Initialize the telemetry singleton AFTER the logger is ready.
    <ToolName>Logger logger = <ToolName>Logger.getInstance();

    // 3. Per-mode dispatch — each branch records its component/feature
    //    and ends with a single sendLog() in finally.
    try {
        runMode(mode, …, logger);
        logger.setStatus(STATUS_SUCCESS);
        logger.setMisc("mode=" + mode);
    }
    catch (Exception e) {
        logger.setStatus(STATUS_FAILURE);
        logger.setMisc("mode=" + mode + "; error=" + e.getMessage());
        LOG.error("Execution failed", e);
    }
    finally {
        logger.sendLog();   // synchronous — acceptable for a CLI tool
    }
}
```

### 9.1 Multi-step / "ALL"-mode pattern

When a single invocation runs N independent sub-operations:

```java
List<String> successes = new ArrayList<>();
List<String> failures  = new ArrayList<>();
for (Mode sub : subModes) {
    try { runConverter(sub, …, logger); successes.add(sub.name()); }
    catch (Exception e) { failures.add(sub.name()); }
}
if (failures.isEmpty())      logger.setStatus(STATUS_SUCCESS);
else if (successes.isEmpty()) logger.setStatus(STATUS_FAILURE);
else                          logger.setStatus(STATUS_PARTIAL);
logger.setMisc("mode=ALL; ok=" + join(successes) + "; fail=" + join(failures));
logger.sendLog();
```

### 9.2 `Event` mapping

The string `status` is mapped to the vendor `Event` enum inside the
adapter — typical mapping:

```java
event = status.startsWith(STATUS_FAILURE)
    ? Event.COMPLETE_WITH_ERRORS
    : Event.COMPLETE_WITHOUT_ERRORS;
```

`STATUS_PARTIAL` maps to `COMPLETE_WITHOUT_ERRORS` because the run
produced usable output; `misc` carries the detail for the dashboard.

***

## 10. When to Escalate to the PDE Variant

| Symptom | Action |
|---|---|
| The host is an Eclipse RCP / Equinox / Tycho application | Use [`eclipse-pde-telemetry-resilience`](../eclipse-pde-telemetry-resilience/SKILL.md) instead |
| The JVM is long-lived (server, daemon, IDE-hosted tests) | Daemon-thread bulkhead + wall-clock cap required — escalate |
| Telemetry is invoked many times per process | Bounded queue + circuit breaker — escalate |
| A later component swaps `System.out` (Log4j async appender, <host-logger>, custom `PrintStream`) | Flushed timestamped helpers required — escalate |
| First-call SSL handshakes consistently exceed the library's default HTTP timeout | Layered timeouts required — escalate |

***

## 11. Step-by-Step Protocol

The agent MUST execute these phases in order. Composer skills inject
their vendor-specific values at the points marked `<…>`.

### Phase 1 — Survey

1. Locate `main` class and the existing logger initialization.
2. Confirm the build script's runnable-JAR idiom.
3. Inspect `.classpath` to see whether vendor source is consumed as a
   workspace project or only as a `libs/` JAR.
4. Inspect existing `*.properties` files to choose a non-colliding
   namespace for the telemetry config keys.

### Phase 2 — Drop in the JARs

1. Copy `<vendor>-<ver>.jar`, `jna-<ver>.jar`, `jna-platform-<ver>.jar`
   (and any other transitive dep that doesn't ship inside the vendor
   JAR) into `libs/`.
2. Add `<classpathentry kind="lib" path="libs/<jar>"/>` for each in
   `.classpath`.
3. Add `<zipfileset dir="libs" includes="<jar>"/>` for each in the Ant
   build (or the equivalent Shade / Shadow / Maven inclusion).
4. List each JAR in the Jar-in-Jar manifest's `Rsrc-Class-Path` (or
   leave to Shade's flat-merge).

### Phase 3 — Create the adapter package

```text
src/<your-package>/<adapter-package>/
├── <ToolName>Constants.java     # tool identity + RESOURCE_PATH resolver (§7)
└── <ToolName>Logger.java        # singleton facade (§9)
```

`<ToolName>Logger` MUST:

- Be a singleton.
- Run `pushSavedLogToServer()` in the constructor (cheap, synchronous,
  acceptable for a one-shot CLI).
- Expose `setFeature(component, feature)`, `setStatus(status)`,
  `setMisc(s)`, `sendLog()`.
- Log success / failure / retry-failure through the project's logger
  factory (§8).

### Phase 4 — Configuration file

1. Create `src/<vendor>.properties` with the one or two keys the
   project wants to pin (typically just the server URL).
2. Confirm Eclipse copies it to `bin/` (default behaviour for files
   under a `src` folder).
3. Confirm the build script bundles `bin/` into the runnable JAR root.

### Phase 5 — Version SSOT

1. Create `src/version.properties` per §6 (if not already present).
2. Wire the build script to read it.
3. Wire the adapter to read it through the classpath at runtime.

### Phase 6 — Defensive `main(...)` integration

Implement the §9 template (single-mode and/or ALL-mode variant as
needed).

### Phase 7 — Verification

1. **Clean rebuild** so the IDE and build script both pick up the
   new JARs and properties.
2. **Healthy-network run** — confirm the log contains
   `<vendor> log sent successfully for <TOOL>` and no `.spool` file is
   left behind.
3. **Hosts-file smoke test** — block the telemetry host
   (`127.0.0.1 <server-host>` in the OS hosts file). Run the tool.
   Confirm:
    - the tool's `errorlevel` is unchanged,
    - the log contains `<vendor> log failed — saving for retry: …`,
    - a `<gmt-timestamp>.spool` file appears in `RESOURCE_PATH`.
4. **Restore the hosts file** — next run drains the `.spool` file
   silently (no extra log line is required for the success case).

***

## 12. Verification Checklist

- [ ] All telemetry JARs present in `libs/`.
- [ ] `.classpath` references every JAR (and the optional vendor
      source project, if applicable).
- [ ] Build script lists every JAR in its bundling step
      (`<zipfileset>` / Shade / Shadow).
- [ ] Runnable-JAR manifest's `Rsrc-Class-Path` (or equivalent) lists
      every JAR.
- [ ] `src/<vendor>.properties` present and bundled at the runnable
      JAR root.
- [ ] `src/version.properties` is the SSOT; build and runtime agree.
- [ ] `<ToolName>Constants.RESOURCE_PATH` falls back to `user.dir`
      when the URI scheme is not `file:`.
- [ ] `<ToolName>Logger.getInstance()` is called once, after logger
      init, before mode dispatch.
- [ ] Every dispatch path ends with `setStatus(...)` + `sendLog()` in
      a `finally` block.
- [ ] `ALL`-mode classifies as `SUCCESS` / `PARTIAL` / `FAILURE`
      using the success/failure lists.
- [ ] Disconnecting from the corporate network does NOT change the
      tool's `errorlevel`; a `*.spool` file appears in `RESOURCE_PATH`.
- [ ] Next on-network run drains the `*.spool` file.

***

## 13. Industry Standards Mapping

| What the skill mandates | Industry name | Reference |
|---|---|---|
| Synchronous fire-and-forget for short-lived CLI | "Best-effort logging" | OpenTelemetry SDK spec §Error Handling — telemetry MUST NOT throw to user code |
| Persist payload locally, retry next run | **Store-and-forward / outbox** | Sentry, Datadog Agent, AWS CloudWatch Agent; Chris Richardson, *Microservices Patterns* Ch. 3 |
| Classpath properties + sysprop + env layers | **12-Factor config** | Heroku 12-Factor App §III — Config; Spring Boot `PropertySource` precedence |
| Single version SSOT read by build and runtime | **Single source of truth** | SemVer FAQ; Maven `${project.version}` filter; Gradle `version.txt` pattern |
| Classpath resource for runtime metadata | Standard JVM practice | `Class.getResourceAsStream("/<name>.properties")` |
| Defensive `try / catch (Throwable)` around telemetry | **Observer isolation** | SLF4J, OpenTelemetry `SafeLogger`, GC logging |

***

## 14. Composition by Higher-Level Skills

No composers are registered in this public repository. Organization-specific
composers (which supply the vendor's payload model, server URL, JAR set,
and tool-identity constants) live in the organization's own private skills
repository and MUST link back to this base in their **Composition
Rationale** so the dependency graph remains bidirectionally discoverable
from the consuming side.

***

## 15. Related Skills

- [`eclipse-pde-telemetry-resilience`](../eclipse-pde-telemetry-resilience/SKILL.md)
  — the OSGi / PDE / Tycho counterpart for when the host is an
  Eclipse RCP / Equinox application; mandates the daemon-thread
  bulkhead with wall-clock cap that this skill deliberately omits.
- [`maven-pom-audit`](../maven-pom-audit/SKILL.md) — when the
  consumer project is Maven and `pom.xml` needs grooming alongside.
- [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
  — for arranging the integration as atomic commits.

***

## 16. Reference Implementation

The first production consumer was a plain-Java CLI tool packaged via
Eclipse's Jar-in-Jar Loader (Ant build), wiring this skill's pattern
through `.classpath` + Ant `Rsrc-Class-Path` + `src/<vendor>.properties`
+ `src/version.properties` + a `<Tool>TelemetryConstants` /
`<Tool>TelemetryLogger` adapter pair. Concrete file layouts and the
anonymized walkthrough live in the organization-specific composer
skill's private repository.
