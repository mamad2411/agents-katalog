---
name: osgi-require-bundle-to-import-package
description: Decouple an Eclipse PDE / Tycho plugin from an upstream OSGi Bundle-SymbolicName rename (e.g., Eclipse Orbit `org.apache.commons.io` → Maven-Central `org.apache.commons.commons-io`) by migrating its `Require-Bundle` entry to a `Import-Package` entry against the still-stable exported package name. Heals "Missing requirement: ... requires 'osgi.bundle; <bsn> 0.0.0' but it could not be found" failures in CI/Tycho without editing the releng-controlled p2 target platform, and without breaking IDE builds across multiple Eclipse vintages that ship the legacy Orbit-named IU.
category: Build & Dependency Management
---

# OSGi `Require-Bundle` → `Import-Package` Migration Skill

> **Skill ID:** `osgi-require-bundle-to-import-package`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Convert one or more `MANIFEST.MF` `Require-Bundle: <bsn>` clauses to
`Import-Package: <pkg>;version="[floor,major+1)"` clauses, so that the
plugin resolves against **any** OSGi bundle that exports the package —
regardless of which `Bundle-SymbolicName` the upstream packager chose
for that bundle.

This skill exists because the Eclipse / OSGi ecosystem is currently
mid-migration from the legacy **Eclipse Orbit** packaging convention
(`Bundle-SymbolicName: <java.package>`, e.g.,
`org.apache.commons.io`) to the **Maven-Central OSGi** packaging
convention (`Bundle-SymbolicName: <maven-groupId>.<artifactId>`, e.g.,
`org.apache.commons.commons-io`). Releng teams that swap the underlying
p2 contribution will silently break every downstream
`Require-Bundle: <old-bsn>` clause — but the **package** the consumer
actually imports is unchanged on both sides, because Apache (the
upstream project) owns the package name.

The fix is local to the consuming plugin's `MANIFEST.MF`, requires zero
changes to the build pipeline or target platform, and survives both
sides of the rename in the same source tree.

## Prerequisites

| Requirement | Minimum |
|---|---|
| Eclipse PDE / Tycho plugin | A bundle whose `Require-Bundle` lists the renamed/missing BSN |
| Source access | The consuming plugin's `src/` directory (to enumerate actual package imports) |
| Network / repo access | Read access to ONE provider of the package (resolved p2 site, target-platform JAR, or local IDE plugins dir) for exporter verification |
| PowerShell or Bash | For grep + ZIP/MANIFEST.MF inspection |
| `jar` / `unzip` / `[System.IO.Compression.ZipFile]` | To inspect provider bundle `META-INF/MANIFEST.MF` |

## Environment & Dependencies

Verify before starting:

```powershell
# Confirm PowerShell can open ZIP entries (no install needed on Windows PowerShell 5.1+ / pwsh 7+)
Add-Type -AssemblyName System.IO.Compression.FileSystem; 'ok'
```

```bash
# POSIX equivalent: any unzip + grep
which unzip && which grep
```

## When to Apply

Apply this skill when **all** of the following are true:

1. A Tycho / PDE build fails with a resolver error of the shape
   `Missing requirement: <consumer> ... requires 'osgi.bundle; <bsn> [<range>]' but it could not be found`.
2. The plugin's own source code uses `import <pkg>.<Type>` for one or
   more packages exported by `<bsn>` — i.e., the dependency is **real**,
   not dead.
3. **Some** bundle on the resolved target platform still exports
   `<pkg>` (verified per §3 below), even though no bundle uses
   `<bsn>` as its `Bundle-SymbolicName` anymore.

Do **not** apply when:

- The Require-Bundle entry is dead (no source code actually uses any
  package from it) — just delete it instead.
- The consumer relies on OSGi semantics that `Import-Package` can't
  express: bundle-private internals, `Bundle-ClassPath` propagation,
  `DynamicImport-Package` resolution behaviour, or split-package
  participation.
- No bundle anywhere on the resolved target platform exports the
  package. That is a real missing-dependency situation; ask releng to
  re-publish the provider bundle, or stage a stop-gap via
  [`eclipse-pde-jdk-migration` §6 IDE-only alias](../eclipse-pde-jdk-migration/SKILL.md#62-hard-constraint--never-edit-manifestmf-for-an-ide-only-fix).

---

## 1. Why `Import-Package` Decouples the Consumer

OSGi resolves `Require-Bundle` against `Bundle-SymbolicName` and
resolves `Import-Package` against the `Export-Package` clause of any
bundle on the resolved platform. The two coordinates have different
ownership boundaries:

| Coordinate | Owned by | Stability across re-packagings |
|---|---|---|
| `Bundle-SymbolicName` | The **OSGi packager** (Eclipse Orbit, Maven-Central OSGi, internal repackager) | **Unstable** — changes when the packager changes |
| `Export-Package` (package name) | The **upstream Java project** (Apache, Eclipse, JBoss, etc.) | **Stable** — guaranteed by upstream backward compatibility within a major version |

Therefore, coupling to the package name immunises the consumer against
BSN churn that the consumer's team does not control.

### 1.1 The dual-export trick (why ranges work across versions)

Modern Maven-Central OSGi bundles often dual-publish the package at
two semantic versions: the real version, plus a synthetic
back-compat anchor (e.g., `1.4.9999`) for callers whose old
`Import-Package` was pinned to a pre-OSGi-cleanup range. Example
(from `org.apache.commons.commons-io_2.17.0.jar`):

```
Export-Package: ...,
 org.apache.commons.io;version="1.4.9999",
 org.apache.commons.io;version="2.17.0",
 ...
```

A consumer importing the package with range `[2.2.0, 3.0.0)` binds
to the `2.17.0` export and ignores the `1.4.9999` anchor; a legacy
consumer importing with range `[1.4, 2)` still resolves to the
anchor. Both populations stay green from the same provider bundle.

---

## 2. Procedure

### Step 1 — Capture the failing requirement from the build log

```
[ERROR] Cannot resolve dependencies of project <gid>:<aid>:eclipse-plugin:<version>
[ERROR]   Missing requirement: <consumer-bsn> <version> requires
              'osgi.bundle; <missing-bsn> <range>' but it could not be found
```

Record:

- The **consumer plugin** (which `MANIFEST.MF` to edit).
- The **missing BSN** (the dead `Require-Bundle` entry).
- The **range** (often `0.0.0` for unrestricted; otherwise the floor
  the consumer used to ask for).

### Step 2 — Identify the actual package usage in the consumer's source

```powershell
# In the consumer plugin directory:
Select-String -Path 'src\**\*.java' -Pattern '^import\s+<top-level-package>\.'
```

```bash
grep -RhE '^import +<top-level-package>\.' src/ | sort -u
```

Bucket the matches by package:

| Sub-package referenced | Used in N files |
|---|---|
| `<top-level-package>` | … |
| `<top-level-package>.<sub1>` | … |
| `<top-level-package>.<sub2>` | … |

The set of distinct packages is the `Import-Package` payload.
**If the set is empty → the `Require-Bundle` entry is dead; skip to
Step 6.**

### Step 3 — Verify a provider bundle on the resolved platform exports the package

You MUST confirm this with first-hand evidence, not by trusting the
build log alone. Pick whichever provider source applies to your
environment and extract its `META-INF/MANIFEST.MF`:

**A. p2 site via HTTPS (Tycho / CI such as Jenkins, after seeing the URL in the build log)**

```powershell
$url = '<p2-base>/<component>/<version>/plugins/<provider-bsn>_<provider-version>.jar'
$dst = Join-Path $env:TEMP 'provider.jar'
# Re-use Maven settings credentials when the repo requires Basic auth:
[xml]$x = Get-Content "$env:USERPROFILE\.m2\settings.xml"
$srv = $x.settings.servers.server | Where-Object { $_.id -eq '<your-server-id>' }
$pair = "$($srv.username):$($srv.password)"
$hdr  = @{ Authorization = 'Basic ' + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair)) }
Invoke-WebRequest -Uri $url -OutFile $dst -UseBasicParsing -Headers $hdr
'Bytes: ' + (Get-Item $dst).Length
```

**B. Local plugin directory (Eclipse / Equinox runtime)**

```powershell
Get-ChildItem '<eclipse-install>\plugins' -Filter '<provider-bsn>*.jar' |
  Select-Object Name
```

**C. Read the provider manifest**

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
$z = [System.IO.Compression.ZipFile]::OpenRead('<path-to-provider.jar>')
$e = $z.Entries | Where-Object { $_.FullName -eq 'META-INF/MANIFEST.MF' }
$sr = New-Object System.IO.StreamReader($e.Open())
$raw = $sr.ReadToEnd(); $sr.Close(); $z.Dispose()
# Unfold OSGi manifest continuation lines (folded at column 72):
$unfolded = ($raw -replace "`r`n ","") -replace "`n ",""
($unfolded -split "`n") | Where-Object { $_ -match '^(Bundle-SymbolicName|Bundle-Version|Export-Package):' }
```

Confirm the output shows `Export-Package: <pkg>;version="<v>"` for
each package from Step 2. Record the **lowest** observed `<v>` across
**all** environments the consumer must build in (IDE vintages + CI).

### Step 4 — Compute the version range

| Bound | Value | Rationale |
|---|---|---|
| Floor | The **oldest** export version observed across all required environments | Resolves on every supported IDE / CI / runtime |
| Ceiling | Next major version (exclusive) | OSGi convention: a major bump may break API |

Example: if an older Eclipse vintage ships package at `2.2.0` and a
newer Eclipse vintage / Jenkins CI target at `2.17.0`, range = `[2.2.0, 3.0.0)`.

### Step 5 — Edit the MANIFEST.MF

Apply two coordinated edits to the consumer's `META-INF/MANIFEST.MF`:

1. **Remove** the dead `Require-Bundle: <missing-bsn>,` line (preserve
   surrounding entries and folding/indentation).
2. **Add** `Import-Package: <pkg>;version="[<floor>,<major+1>.0.0)"`,
   either as a new header (if none exists) or as new entries appended
   to the existing `Import-Package` header.

#### Worked diff — single-package consumer (no prior `Import-Package`)

```diff
 Require-Bundle: org.eclipse.core.runtime,
  ...,
- <missing-bsn>,
  ...
 Export-Package: <consumer.exports>
+Import-Package: <pkg>;version="[<floor>,<major+1>.0.0)"
```

#### Worked diff — multi-package consumer with prior `Import-Package`

```diff
- <missing-bsn>,
 Import-Package: <other.pkg>;version="<existing-range>",
+ <pkg>;version="[<floor>,<major+1>.0.0)",
  <yet.another.pkg>;version="<existing-range>"
```

OSGi manifest folding rules: continuation lines are indented one space
exactly. Do **not** introduce tabs or trailing whitespace; the manifest
parser is strict.

### Step 6 — Repository-wide sweep

The same upstream BSN rename usually breaks more than one consumer.
Sweep the whole repo:

```powershell
Select-String -Path '<root>\*\META-INF\MANIFEST.MF' `
  -Pattern '^\s*<missing-bsn>\s*,?\s*$' |
  ForEach-Object { "{0}:{1}: {2}" -f $_.Path, $_.LineNumber, $_.Line.Trim() }
```

For each additional hit, repeat Step 2 (source-usage grep) for that
consumer plugin:

- **Live usage** → repeat Steps 4 + 5.
- **No usage** → delete the dead `Require-Bundle` line (do not migrate
  to `Import-Package`; that would just move a dead reference to a
  different header).

### Step 7 — Verify zero `Require-Bundle: <missing-bsn>` remain

```powershell
Select-String -Path '<root>\*\META-INF\MANIFEST.MF' `
  -Pattern '<missing-bsn>[^.a-zA-Z0-9_-]'
```

Output MUST show **only** `Import-Package:` lines (not `Require-Bundle`
continuation lines). The pattern's negative-character-class tail
prevents a false positive on a longer BSN that happens to share a
prefix (e.g., `<missing-bsn>.extras`).

### Step 8 — Resume the build

For Tycho / Maven:

```
mvn <args> -rf :<first-fixed-consumer>
```

The resolver should now bind every fixed consumer to the package
provider that previously failed the `Require-Bundle` check.

---

## 3. Failure-mode catalogue

| Symptom after the edit | Cause | Remedy |
|---|---|---|
| `Missing requirement: <consumer> requires 'osgi.wiring.package; <pkg> <range>'` | No provider on the target exports the package in your range. Floor too high, or the package was retired upstream. | Re-check Step 3 against EVERY environment; widen floor; or escalate to releng. |
| Compiles in IDE, fails in CI (or vice versa) | One target ships only the `1.4.9999` synthetic anchor (legacy), the other only the real version. | Choose a range that intersects both — typically pick the lowest **real** version, not the anchor. |
| Manifest parser error: "invalid manifest format" | Folding broken — a continuation line lost its leading space, or a tab was introduced. | Re-fold by hand; ensure every continuation line begins with **exactly one** ASCII space. |
| `Bundle-ClassPath`-style internal resource is now `ClassNotFoundException` at runtime | The dead bundle was carrying a transitive resource the consumer used via `Bundle.getResource`. `Import-Package` doesn't carry resources. | Restore the bundle relationship some other way (Maven `<location>` alias per [eclipse-pde-jdk-migration §6.3](../eclipse-pde-jdk-migration/SKILL.md#63-fix--pde-maven-location-with-bnd-instructions-override)), or vendor the resource. |
| Pre-existing `Bundle-RequiredExecutionEnvironment` is too low for the new provider's `Require-Capability` | New provider needs newer JavaSE EE. | Raise `Bundle-RequiredExecutionEnvironment`, or pin to an older provider. |

---

## 4. Relationship to neighbouring skills

| Skill | Relationship |
|---|---|
| [eclipse-pde-jdk-migration §6](../eclipse-pde-jdk-migration/SKILL.md#6-orion-13-orbit-symbolic-name-mismatch-fixable-without-touching-manifestmf) | **Complementary, opposite direction.** That skill solves the same Orbit-vs-Maven-Central BSN mismatch via a **target-platform alias** (`<location>` + bnd `<instructions>`) — IDE-only fix that MUST NOT touch `MANIFEST.MF` because CI uses a different target. This skill is the inverse: edit the consumer `MANIFEST.MF` once so the same source works in IDE **and** CI without target-platform tricks. Use this when you control consumer manifests but not the target; use that one when you control the IDE target but not consumer manifests. |
| [eclipse-pde-telemetry-resilience](../eclipse-pde-telemetry-resilience/SKILL.md) | When integrating a third-party library that itself imports from a renamed bundle, prefer specifying the library's transitive deps via `Import-Package` for the same decoupling reason. |
| [maven-pom-audit](../maven-pom-audit/SKILL.md) | Adjacent build-config hygiene — POM-side audits often surface the same kind of upstream rename via dependency-management drift. |

---

## 5. Worked Example (sanitised)

A consuming plugin declared:

```
Require-Bundle: ...,
 org.apache.commons.io,
 ...
```

CI Tycho build failed:

```
[ERROR] Missing requirement: <consumer> requires
   'osgi.bundle; org.apache.commons.io 0.0.0' but it could not be found
```

Source-grep showed exactly one usage:

```
src/.../FCListGeneration.java:import org.apache.commons.io.FileUtils;
```

Provider audit across all required environments:

| Environment | Provider bundle | BSN | Exports `org.apache.commons.io` at |
|---|---|---|---|
| Eclipse 4.8 vintage | `org.apache.commons.io_2.2.0…jar` | `org.apache.commons.io` | `2.2.0` |
| Eclipse 4.14 vintage | `org.apache.commons.io_2.6.0…jar` | `org.apache.commons.io` | `2.6.0` |
| Eclipse 4.27 vintage | `org.apache.commons.io_2.8.0…jar` | `org.apache.commons.io` | `2.8.0` |
| Eclipse 4.36 vintage (IDE) | both Orbit + Maven-Central | both `…io` and `…commons-io` | `2.8.0` and `2.16.1` |
| Eclipse 4.36 vintage (CI p2) | `org.apache.commons.commons-io_2.17.0.jar` shipped inside an unrelated component p2 zip | `org.apache.commons.commons-io` | `2.17.0` (plus synthetic `1.4.9999`) |

Floor = `2.2.0` (oldest required). Ceiling = `3.0.0` (next major).
Edit applied:

```diff
- org.apache.commons.io,
 ...
 Export-Package: <consumer.exports>
+Import-Package: org.apache.commons.io;version="[2.2.0,3.0.0)"
```

Repo sweep found two sibling test plugins with the same dead
`Require-Bundle`: one had a live `FileUtils` usage (migrated the same
way), the other had no source usage (deleted as dead).

Result: single source tree resolves cleanly against the Orbit-named
provider on every IDE vintage AND against the Maven-Central-named
provider on CI, with no target-platform edits required.

---

## 6. Related Conversations & Traceability

The protocol distilled here was first proved out during a Tycho build
investigation where the same source tree had to keep resolving across
five Eclipse vintages plus a Jenkins CI target that had swapped from
Orbit to Maven-Central commons-io packaging. The fix was the manifest
migration above; verification was a live HTTP fetch of the provider
JAR from the CI p2 site followed by `META-INF/MANIFEST.MF` extraction
proving the package export at the expected version — not log
inspection alone.
