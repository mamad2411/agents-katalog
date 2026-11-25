---
name: eclipse-pde-jdk-migration
description: Eclipse PDE/Tycho workspace migration across JDK major versions — surveys JRE pins in `.classpath`/`MANIFEST.MF`/`*.launch`/`pom.xml`, drops obsolete PermGen flags, injects JDK 9+ `--add-opens` flags, and resolves IDE-only side issues (target-platform symbolic-name mismatches via PDE Maven `<location>` + bnd `<instructions>`, m2e proxy via `~/.m2/settings.xml`, empty source-folder paradox via `.gitkeep`) without touching CI/Tycho-consumed files.
category: Build & Dependency Management
---

# Eclipse PDE JDK Migration Skill

> **Skill ID:** `eclipse-pde-jdk-migration`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Migrate an Eclipse PDE/Tycho/OSGi workspace across a JDK major version
boundary (e.g., 8 → 11, 11 → 17, 17 → 21) without rewriting the source
code's Java language compliance.

The skill formalises the four-surface model that every PDE workspace
exposes — and that beginners conflate:

| Surface | What it controls | Migration verb |
|---|---|---|
| `.settings/org.eclipse.jdt.core.prefs` `compliance/source/target` | The Java language level the JDT compiler accepts | **KEEP** unless source bump is requested |
| `MANIFEST.MF` `Bundle-RequiredExecutionEnvironment` | The minimum JRE the OSGi runtime advertises | **KEEP**; a higher JDK satisfies a lower EE |
| `.classpath` `JRE_CONTAINER` (pinned vs. unpinned) | The JDK Eclipse uses to compile/run **this plug-in** | **UNPIN** so workspace default applies |
| `*.launch` `JRE_CONTAINER` + `VM_ARGUMENTS` | The JDK and JVM args used at run/debug time | **REPOINT** to new EE; **scrub** dead JVM args; **inject** `--add-opens` |

This separation is the SSOT — most failed migrations break because they
bump compliance unnecessarily, or pin the classpath to the new EE
(coupling future maintenance to a specific JDK), or forget JDK 9+
strong-encapsulation flags and only discover the JAXB / EMF / Sphinx /
Xtend `InaccessibleObjectException` at runtime.

## Prerequisites

| Requirement | Minimum |
|---|---|
| Eclipse | 4.20+ (any version that supports the target JDK as a JRE) |
| Tycho | 2.7+ for JDK 17, 4.0+ for JDK 21 |
| Target JDK | Installed and discoverable (path known) |
| PowerShell | 5.1+ on Windows or 7+ cross-platform |
| VCS | Git (skill assumes commits will be arranged via [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)) |

## Environment & Dependencies

Before running, the agent MUST:

1. Confirm the **target JDK is installed** and capture its path:

    ```powershell
    & '<jdk-install>\bin\java.exe' -version
    ```

2. Confirm Eclipse can register a new JRE (Window → Preferences → Java →
   Installed JREs is reachable on the user's IDE).
3. Confirm `git status` is clean in the workspace repo so migration
   edits can be staged atomically.
4. Bootstrap the shared PowerShell utilities submodule (recursive form
   per [Recursive Submodule Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md)):

    ```powershell
    git submodule update --init --recursive ai-agent-rules/powershell-scripts
    ```

## When to Apply

Apply this skill when:

- An Eclipse PDE / Tycho workspace must move to a new JDK major version
- The user reports `Unrecognized VM option 'MaxPermSize'` or
  `Unrecognized VM option 'PermSize'` after a JDK bump
- The user reports `java.lang.reflect.InaccessibleObjectException` or
  `module java.base does not "opens X" to unnamed module` from JAXB,
  EMF, Sphinx, Xpand, Xtend, or BeanShell after a JDK bump
- Launch configurations point to JDK installations that no longer exist
  on disk (`1.8.0_92_64`, `11.0.16.1`, etc.)
- A workspace boots on the IDE's bundled JDK but plug-ins fail to compile
  because their `.classpath` is pinned to a removed JRE

Do NOT apply when:

- The build system is plain Maven, Gradle, or sbt without Tycho/PDE
  (no `MANIFEST.MF` / `.classpath` / `.launch` surface to manage)
- The user explicitly asks for a **language-level** bump (Java 8 → 17
  source) — that requires source-code remediation (`var`, sealed types,
  removed `sun.*` API) which is out of scope here
- The JDK change is a minor/patch bump within the same major version
  (no surface change required)

---

## Phase 1 — Reference Survey (Read-Only)

Discover every place the workspace pins a JDK.

### Step 1.1 — Run the bundled survey script

```powershell
pwsh-preview -File .agents/skills/eclipse-pde-jdk-migration/scripts/Survey-JrePins.ps1 `
    -WorkspaceRoot '<workspace-root>'
```

Falls back to `pwsh` if `pwsh-preview` is unavailable. The script
produces a categorised report of:

- `.classpath` files where `JRE_CONTAINER` is pinned to a specific EE
  (`JavaSE-1.8`, `JavaSE-11`) versus unpinned (workspace default)
- `MANIFEST.MF` files and their `Bundle-RequiredExecutionEnvironment`
  value
- `*.launch` files with hard-coded VM ids (`1.8.0_92_64`,
  `11.0.16.1`, etc.) versus EE-based references (`JavaSE-17`)
- `pom.xml` files containing PermGen flags (`-XX:PermSize`,
  `-XX:MaxPermSize`) or an `<executionEnvironment>` property

The script is **read-only** — it never mutates files. It exits 0 on
success regardless of findings (a survey of zero issues is still a
successful survey).

### Step 1.2 — Manual cross-check (if script unavailable)

The four canonical regex queries the script encapsulates:

```powershell
# .classpath — pinned vs. unpinned JRE_CONTAINER
Select-String -Path '**\.classpath' -Pattern 'JRE_CONTAINER' -AllMatches

# MANIFEST.MF — Bundle-RequiredExecutionEnvironment
Select-String -Path '**\META-INF\MANIFEST.MF' -Pattern 'Bundle-RequiredExecutionEnvironment'

# *.launch — JRE_CONTAINER (EE or pinned VM id)
Select-String -Path '**\*.launch' -Pattern 'JRE_CONTAINER'

# pom.xml — PermGen flags
Select-String -Path '**\pom.xml' -Pattern 'PermSize'
```

---

## Phase 2 — Migration Decision Matrix

Apply the SSOT table below per surface. **Do NOT bump compliance unless
the user explicitly requested a source-language migration.**

| Finding | Default action | Rationale |
|---|---|---|
| `.classpath` JRE_CONTAINER pinned to old EE (e.g., `JavaSE-1.8`) | **Unpin** to plain `JRE_CONTAINER` | Lets workspace-default JRE apply; consistent with unpinned siblings |
| `.classpath` JRE_CONTAINER unpinned | **Leave** | Already correct; will pick up new workspace default JDK |
| `MANIFEST.MF` `Bundle-RequiredExecutionEnvironment: JavaSE-1.8` | **Leave** | A higher JDK satisfies a lower EE; bumping forces all consumers to upgrade |
| `MANIFEST.MF` already on a *newer* EE than `<OLD>` (e.g. `JavaSE-17` when migrating 17 → 21) | **Leave** | Forward-compatible with `<NEW>`; preserves any deliberate per-bundle hardening |
| `org.eclipse.jdt.core.prefs` `compliance/source/target = 1.8` | **Leave** | JDK 17 compiles `-source 1.8` cleanly; bumping is a language migration |
| `*.launch` JRE_CONTAINER pinned to specific VM id | **Repoint** to `JavaSE-<NEW>` EE | EE pin survives JRE renames; specific id pins break when JREs are uninstalled |
| `*.launch` `VM_ARGUMENTS` containing `-XX:MaxPermSize` / `-XX:PermSize` | **Strip** | PermGen removed in Java 8u; JDK 9+ aborts on `-XX:MaxPermSize` |
| `*.launch` `VM_ARGUMENTS` lacking `--add-opens` (target JDK ≥ 9) | **Inject** standard set | Required for JAXB/EMF/Sphinx/Xtend reflection (see Phase 4) |
| `pom.xml` `<argLine>` with PermGen | **Strip** | Same reason as `.launch` |
| Tycho `<executionEnvironment>` property | **Defer** to releng parent | This skill does not edit CI/CD-managed parent POMs |

---

## Phase 3 — Surgical Edits

The agent applies the matrix surface-by-surface. **Never bulk-replace VM
arguments** — every launch may carry user-customised properties (heap
size, system properties, JFR flags) that must be preserved.

### 3.1 Unpin classpath JRE containers

For each pinned `.classpath`:

```diff
- <classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8"/>
+ <classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER"/>
```

### 3.2 Drop PermGen from launches and Tycho POMs

```diff
- value="-Xms512m -Xmx3G -XX:MaxPermSize=512m -Xss1024k …"
+ value="-Xms512m -Xmx3G -Xss1024k …"
```

```diff
- <argLine>${tycho.testArgLine} -Xms512m -Xmx2048m -XX:PermSize=256m -XX:MaxPermSize=512m</argLine>
+ <argLine>${tycho.testArgLine} -Xms512m -Xmx2048m</argLine>
```

### 3.3 Re-EE launches

```diff
- <stringAttribute key="org.eclipse.jdt.launching.JRE_CONTAINER" value="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/11.0.16.1"/>
+ <stringAttribute key="org.eclipse.jdt.launching.JRE_CONTAINER" value="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-17"/>
```

### 3.4 Inject `--add-opens` (target JDK ≥ 9)

Prepend the standard set to every launch's `VM_ARGUMENTS`:

```text
--add-opens=java.base/java.lang=ALL-UNNAMED
--add-opens=java.base/java.lang.reflect=ALL-UNNAMED
--add-opens=java.base/java.io=ALL-UNNAMED
--add-opens=java.base/java.util=ALL-UNNAMED
--add-opens=java.base/java.net=ALL-UNNAMED
```

**Coupling note**: §3.2, §3.3, and §3.4 all touch the same launch file.
Per the buildable-state priority of
[`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md),
all three edits per launch MUST be coalesced into one commit per launch
group — splitting them leaves intermediate launches broken in two of
three states.

---

## Phase 4 — JDK 9+ Reflection Unblock Reference

When a launch crashes with
`module java.base does not "opens X" to unnamed module`, locate the
package in the table and append the matching `--add-opens` to that
launch's `VM_ARGUMENTS`.

| Symptom in stack trace | Required flag |
|---|---|
| `JAXBContext.newInstance` → `Injector.<clinit>` → `ClassLoader.defineClass` | `--add-opens=java.base/java.lang=ALL-UNNAMED` |
| EMF/Sphinx reflection on private fields | `--add-opens=java.base/java.lang.reflect=ALL-UNNAMED` |
| Eclipse log/file IO reflection | `--add-opens=java.base/java.io=ALL-UNNAMED` |
| Guava / collections reflection | `--add-opens=java.base/java.util=ALL-UNNAMED` |
| URL handler reflection | `--add-opens=java.base/java.net=ALL-UNNAMED` |
| `cannot access class sun.nio.ch.DirectBuffer` | `--add-opens=java.base/sun.nio.ch=ALL-UNNAMED` |
| `does not "opens java.nio"` | `--add-opens=java.base/java.nio=ALL-UNNAMED` |
| `does not "opens java.text"` (DateFormat) | `--add-opens=java.base/java.text=ALL-UNNAMED` |
| `does not "opens java.util.regex"` | `--add-opens=java.base/java.util.regex=ALL-UNNAMED` |
| BeanShell `AbstractStringBuilder.append()` — `does not "opens java.lang"` via BshInterpreter reflection on `StringBuilder` | `--add-opens=java.base/java.lang=ALL-UNNAMED` (JVM-side) **or preferably** replace `new StringBuilder().append(...)` with `+` in the `.bsh` source (eliminates reflection) |
| Xtend / Xtext on-the-fly compile via `com.sun.tools.javac` | `--add-opens=jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED` (also `.code`, `.tree`, `.util`, `.processing`, `.model`, `.parser`, `.comp`, `.main`, `.file`) |
| `does not "opens sun.security.x509"` | `--add-opens=java.base/sun.security.x509=ALL-UNNAMED` |
| `IllegalAccessError` on `jdk.internal.misc` | `--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED` |

---

## Phase 5 — Verification

1. **Eclipse Installed JREs**: Window → Preferences → Java → Installed
   JREs → Add Standard VM → point to `<jdk-install>` → tick as default.
2. **Execution Environments**: Java → Installed JREs → Execution
   Environments → tick the new JDK against `JavaSE-<NEW>` AND against
   the `MANIFEST.MF`-declared `JavaSE-1.8` (so the EE pin still
   resolves).
3. **Project → Clean… → All projects**.
4. **Spot-check** any plug-in: Build Path → Libraries → JRE System
   Library should now read `[<new-jdk-name>]`.
5. **Run** the most representative `*.launch` configuration. Watch for:
    - `Unrecognized VM option` — Phase 3.2 missed a flag
    - `InaccessibleObjectException` — Phase 4 needs another `--add-opens`
    - Successful boot — log header should print `java.version=<NEW>`
6. **Tycho command-line build** (if applicable):

    ```powershell
    $env:JAVA_HOME = '<jdk-install>'
    $env:PATH = "$env:JAVA_HOME\bin;$env:PATH"
    mvn -v   # confirm
    mvn clean verify
    ```

---

## Phase 6 — Target-Platform Symbolic-Name Aliasing (IDE-Only)

A new JDK / new Eclipse / new Orbit release frequently triggers
`Bundle '<X>' cannot be resolved` errors that have **nothing** to do with
the JDK itself — they are caused by Eclipse Orbit renaming a bundle to
Maven-style symbolic names (`<groupId>.<artifactId>`) while existing
`MANIFEST.MF` files still reference the legacy name (or vice-versa).

### 6.1 Detection pattern

| Legacy Orbit name | Maven-style name (Orbit ≥ R2024-09) |
|---|---|
| `org.apache.commons.io` | `org.apache.commons.commons-io` |
| `org.apache.commons.collections` | `org.apache.commons.commons-collections4` |
| `com.google.guava` | `com.google.guava.guava` |
| `org.slf4j.api` | `org.slf4j.slf4j-api` |

Symptom: `Bundle 'org.apache.commons.commons-io' cannot be resolved` while
`Get-ChildItem '<orbit-plugins>' -Filter '*commons*io*'` shows only
`org.apache.commons.io_2.x.y.jar`.

### 6.2 Hard constraint — never edit MANIFEST.MF for an IDE-only fix

If the workspace's CI/CD Tycho/Maven build resolves the bundle through a
*different* target platform (e.g., a remote p2 site that ships the
Maven-style name), then **rewriting `MANIFEST.MF` to the legacy name
breaks CI**. Any fix MUST be local to the IDE — i.e., scoped to a
`.target` file that is *not* consumed by the Tycho/Maven pipeline.

> **When the CI side is the one that breaks** (resolver fails on the
> Maven-Central-named bundle because the consumer's `MANIFEST.MF`
> still asks for the Orbit-style BSN), the dual problem applies:
> see [`osgi-require-bundle-to-import-package`](../osgi-require-bundle-to-import-package/SKILL.md),
> which migrates the consumer's `Require-Bundle: <bsn>` to
> `Import-Package: <pkg>` so the same source tree resolves on both
> sides of the rename without any target-platform alias. Pick this
> §6 path when you can change the target but not the manifests; pick
> the other skill when you can change the manifests but not the
> target.

### 6.3 Fix — PDE Maven location with bnd `<instructions>` override

Add a fourth `<location>` to the active `.target` that fetches the
artifact from Maven Central and **forces** the synthesized OSGi
symbolic name to whatever the workspace manifests demand:

```xml
<location includeDependencyScope="compile" includeSource="true"
    missingManifest="generate" type="Maven">
    <dependencies>
        <dependency>
            <groupId>commons-io</groupId>
            <artifactId>commons-io</artifactId>
            <version>2.22.0</version>
            <type>jar</type>
        </dependency>
    </dependencies>
    <instructions><![CDATA[
Bundle-Name:           Apache Commons IO (Maven-style alias for Orion)
Bundle-SymbolicName:   org.apache.commons.commons-io;singleton:=true
Bundle-Version:        ${version_cleanup;${mvnVersion}}
Import-Package:        *;resolution:=optional
Export-Package:        *;version="${version_cleanup;${mvnVersion}}";-noimport:=true
]]></instructions>
</location>
```

Key directives in the `<instructions>` block (bnd syntax):

- `Bundle-SymbolicName: <forced-name>` — overrides the default which
  would otherwise be `<groupId>.<artifactId>` (e.g.,
  `commons-io.commons-io`).
- `Export-Package: *;-noimport:=true` — re-exports every package without
  forcing the bundle to import its own packages.
- `Import-Package: *;resolution:=optional` — prevents the synthesized
  bundle from demanding optional transitive dependencies that the
  target platform may not ship.

### 6.4 Reload protocol

1. Open the active `.target` in the editor.
2. Click **Reload Target Platform** (top-right of the editor pane).
3. Wait for *Resolving Target Definition*; both the Maven location's
   *plug-in count* should turn into a positive integer.
4. Click **Set as Active Target Platform** if not already active.
5. Project → Clean… → All projects.

### 6.4.1 Worked example

For a complete reproducible walkthrough of this phase — including
discovery commands, the constraint matrix that ruled out every other
fix, the exact `.target` diff, the bnd `<instructions>` anatomy,
verification commands, and an adaptation table for other Orbit-renamed
bundles — see
[`docs/cases/apache-commons-io-symbolic-name-aliasing.md`](docs/cases/apache-commons-io-symbolic-name-aliasing.md).

### 6.5 m2e proxy gotcha (corporate environments)

`Could not transfer artifact … No such host is known
(repo.maven.apache.org)` while the OS clearly has internet via a
corporate proxy means **m2e is not reading OS proxy environment
variables** (`HTTP_PROXY` / `HTTPS_PROXY`). Maven only consults
`~/.m2/settings.xml`. Create it (per-user, not committed):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0">
  <proxies>
    <proxy>
      <id>corp-https</id>
      <active>true</active>
      <protocol>https</protocol>
      <host><corp-proxy-host></host>
      <port>8080</port>
      <nonProxyHosts>127.0.0.1|localhost|*.<corp-domain>|*.<corp-cloud-domain></nonProxyHosts>
    </proxy>
    <proxy>
      <id>corp-http</id>
      <active>true</active>
      <protocol>http</protocol>
      <host><corp-proxy-host></host>
      <port>8080</port>
      <nonProxyHosts>127.0.0.1|localhost|*.<corp-domain>|*.<corp-cloud-domain></nonProxyHosts>
    </proxy>
  </proxies>
</settings>
```

**Eclipse must be restarted** for m2e to re-read `settings.xml` — it is
loaded once at startup. Verify the proxy is reachable first:

```powershell
Test-NetConnection <corp-proxy-host> -Port <corp-proxy-port> -InformationLevel Quiet
# then sanity-check Maven Central is fetchable through it
Invoke-WebRequest -Proxy 'http://<corp-proxy-host>:<corp-proxy-port>' `
    -Uri 'https://repo.maven.apache.org/maven2/commons-io/commons-io/maven-metadata.xml' `
    -UseBasicParsing -TimeoutSec 15 | Select-Object StatusCode
```

**Worked example**: For a complete walkthrough — including why Eclipse
Network Connections preferences do *not* fix m2e, the full proxy
configuration matrix Maven actually consults, authenticated-proxy
variants, the 24-hour `.lastUpdated` retry suppression trap, and an
end-to-end 7-step verification sequence — see
[`docs/cases/m2e-enterprise-proxy-resolution.md`](docs/cases/m2e-enterprise-proxy-resolution.md).

### 6.6 Stale `.lastUpdated` failure markers

If m2e tried (and failed) before `settings.xml` existed, the local
repo will contain stale failure markers that suppress retries:

```powershell
Get-ChildItem "$env:USERPROFILE\.m2\repository" -Recurse -Filter '*.lastUpdated' |
    Remove-Item -Force
```

After deletion, re-trigger *Reload Target Platform*.

---

## Phase 7 — IDE State Hygiene (Eclipse Workspace Metadata)

New JDK + new Eclipse occasionally surfaces metadata desync errors that
are neither a code defect nor a missing dependency.

### 7.1 The empty source-folder paradox

Symptom: `Project '<X>' is missing required source folder: 'src'`,
but creating the folder via *New → Source Folder* yields *already
exists*. Cause: the folder physically exists on disk (often empty —
Git does not track empty directories) but Eclipse's JDT model has not
refreshed since import.

Fix:

1. Add a tracked placeholder so Git carries the folder across clones:

   ```powershell
   New-Item -ItemType File -Path '<project>\src\.gitkeep' -Force
   ```

2. In Eclipse: right-click the project → **Refresh** (F5) →
   Project → **Clean…** → select only that project → **Clean**.
3. If still red after clean: right-click → *Close Project* →
   right-click → *Open Project* (forces a full JDT model rebuild).

### 7.2 Forward-compatible per-bundle EE pins

When migrating `<OLD>` → `<NEW>` and a single `MANIFEST.MF` already
advertises an EE *between* `<OLD>` and `<NEW>` (e.g., `JavaSE-17` while
migrating 11 → 21), leave it untouched. JDK 21 satisfies `JavaSE-17`,
and bumping it to `JavaSE-21` would force every consumer of that
bundle onto JDK 21 as well — an unintended ripple.

### 7.3 Eclipse-bundled JRE for recent IDE versions

Eclipse 4.30+ ships a working JRE under `<eclipse>/plugins/
org.eclipse.justj.openjdk.hotspot.jre.full.<os>_<version>/jre`. If
the target JDK matches the bundled JRE major version, **no separate
JDK install is required** for IDE compile/run — only for command-line
Tycho builds. Phase 5's *Eclipse Installed JREs* step is skipped
entirely; the workspace default JRE auto-picks the bundled one.

---

## Phase 8 — Atomic Commit Arrangement

Defer commit construction to
[`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md).
The canonical three-commit split for a typical migration is:

| # | Type / scope / subject | Files | Rationale |
|---|---|---|---|
| 1 | `chore(jdt): unpin classpath JRE container from JavaSE-<OLD>` | every modified `.classpath` | Pure unpin; independently buildable |
| 2 | `build(tycho): drop obsolete PermGen JVM options for JDK <NEW>` | every modified Tycho `pom.xml` | CLI-build cleanup; independent |
| 3 | `chore(launch): migrate Eclipse launches to JDK <NEW> runtime` | every modified `*.launch` | Coupled three-way edit per launch (§3.2 + §3.3 + §3.4); coalesced per buildable-state priority |

`MANIFEST.MF` and `org.eclipse.jdt.core.prefs` MUST remain untouched
unless the user explicitly approves a language-level bump.

---

## Composition by Higher-Level Skills

*(none yet — this is a leaf skill; future composers may chain it with
target-platform refresh or product-config audits)*

---

## Prohibited Behaviors

- **DO NOT** bump `compliance/source/target` in
  `org.eclipse.jdt.core.prefs` unless the user explicitly requests a
  Java language-level migration. JDK 17 compiles `-source 1.8` cleanly.
- **DO NOT** edit `MANIFEST.MF` `Bundle-RequiredExecutionEnvironment`
  blindly. Every consumer of the bundle must support the new EE.
- **DO NOT** edit `MANIFEST.MF` `Require-Bundle` entries to work around
  IDE-only resolution errors. CI/Tycho may resolve the original name
  through a different target platform; manifest edits break the
  pipeline. Use Phase 6 (PDE Maven location + bnd `<instructions>`
  alias) instead.
- **DO NOT** blanket-replace `VM_ARGUMENTS` strings. Read each launch
  individually; preserve user-added system properties, heap settings,
  JFR flags, and module-path entries.
- **DO NOT** edit Tycho releng parent POMs from this skill. Parent
  `<executionEnvironment>` lives outside the workspace and is
  CI/CD-managed.
- **DO NOT** add `--add-opens` for packages the workspace does not
  actually exercise. Bloat hides which flags are load-bearing.
- **DO NOT** side-load missing artifacts into `~/.m2/repository`
  manually as a portable fix. Per-developer manual steps are not
  portable; either commit an in-repo `.target` `<location>` or rely
  on Maven Central via a properly configured `~/.m2/settings.xml`
  (Phase 6.5).
- **DO NOT** create empty source folders by hand inside Eclipse to
  satisfy a *missing required source folder* error. Add a tracked
  `.gitkeep` then refresh (Phase 7.1) — otherwise the folder vanishes
  on the next clone.
- **DO NOT** auto-commit. Commit arrangement is delegated to
  [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md)
  per the Sequential Objective Protocol.

---

## Related Skills

- [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) — three-commit split for the migration
- [`maven-pom-audit`](../maven-pom-audit/SKILL.md) — broader Maven POM auditing if Tycho parents come into scope
- [`system-wide-tool-management`](../system-wide-tool-management/SKILL.md) — installing the target JDK system-wide

---

## Related Conversations & Traceability

- [`docs/conversations/2026-05-10-jdk11-to-jdk17-migration.md`](docs/conversations/2026-05-10-jdk11-to-jdk17-migration.md)
  — full session log of the JDK 11 → 17 migration that birthed this
  skill, including the JAXB `Injector` stack trace that motivated the
  Phase 4 reference table.
- [`docs/conversations/2026-05-10-jdk17-to-jdk21-and-ide-fixes.md`](docs/conversations/2026-05-10-jdk17-to-jdk21-and-ide-fixes.md)
  — cross-version reapplication on a JDK 21 workspace plus three new
  IDE-only side issues (empty source-folder paradox, target-platform
  symbolic-name aliasing for `org.apache.commons.commons-io`, and the
  m2e proxy gotcha) that motivated Phases 6 and 7.

## Documented Cases

- [`docs/cases/apache-commons-io-symbolic-name-aliasing.md`](docs/cases/apache-commons-io-symbolic-name-aliasing.md)
  — reproducible Phase 6 walkthrough for the Eclipse Orbit
  `org.apache.commons.io` ↔ `org.apache.commons.commons-io` rename,
  with constraint matrix, bnd `<instructions>` anatomy, corporate
  proxy companion fix, and an adaptation table for other
  Orbit-renamed bundles (Guava, SLF4J, Commons Collections, Commons
  Lang3).
- [`docs/cases/m2e-enterprise-proxy-resolution.md`](docs/cases/m2e-enterprise-proxy-resolution.md)
  — reproducible Phase 6.5 / 6.6 walkthrough for `No such host is
  known: repo.maven.apache.org` in m2e despite OS-level proxy env
  vars being set; documents Maven's proxy-configuration hierarchy,
  why Eclipse Network Connections preferences are insufficient, the
  per-user `~/.m2/settings.xml` fix (with HTTP + HTTPS protocol
  duality and `<nonProxyHosts>` glob syntax), Eclipse-restart
  requirement, the 24-hour `.lastUpdated` retry-suppression trap,
  authenticated-proxy variants, and 7-step end-to-end verification.
