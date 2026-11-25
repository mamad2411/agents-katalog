---
name: java-vendored-snapshot-compile-check
description: Type-check a vendored Java source snapshot in isolation by enumerating its external symbol surface, generating minimal compile-only API stubs, and javac-ing against stubs plus real library JARs — proves a patch is syntactically valid without needing the original host workspace.
category: Build Validation
---

# Java Vendored Snapshot Compile-Check Skill (v1)

Generic protocol for **type-checking a vendored Java source snapshot** — a directory of `.java` files copied out of
a larger host project (Eclipse PDE bundle, internal SDK, closed-source product) for diff/patch review when the
original buildable workspace is unavailable.

This skill answers a narrow but high-value question: *"Does my patch to the snapshot still compile against the
host project's API contract?"* It does **not** verify runtime behaviour, bundle activation, or integration —
those require the host workspace.

***

## 1. When to use this skill

Use this skill when **all** of the following hold:

- You have a directory of Java source files that reference packages from a host project you do not have access
  to (no `pom.xml`, no `.classpath`, no `MANIFEST.MF`, no target platform).
- You have made source-level edits (e.g., a log-format upgrade, a bug fix) and need to prove the edits don't
  break the type contract with the host.
- Real library dependencies (e.g., JNA, log4j-api, Apache Commons) are available as JARs somewhere on disk.
- A full host-workspace build is gated on access, licensing, or workspace setup time you cannot pay right now.

Do **NOT** use this skill when:

- You have the buildable host workspace — run the host's real build instead.
- You need to validate runtime behaviour (use the host's integration-test harness).
- The snapshot is self-contained (no external imports beyond `java.*` and library JARs) — `javac` directly,
  no stubs needed.

***

## 2. Environment & Dependencies

- **JDK** — same major version as the host project's `Bundle-RequiredExecutionEnvironment` or source-level pin.
  Use `javac -source N -target N` if the host targets an older bytecode level than your JDK.
- **Library JARs** — the third-party runtime dependencies the snapshot imports (e.g., JNA, log4j, JSON).
  Locate them via:
    1. The host project's own `lib/` or `libs/` directory.
    2. A sibling project that vendors the same library at the same version (e.g., a co-located
       `<sibling-project>/libs/` that pins the same artifact at the same version).
    3. A local Maven repository (`~/.m2/repository/<group>/<artifact>/<version>/`).
- **Scratch directory** — `$env:TEMP\<snapshot-name>_compile_check\` on Windows; `/tmp/<snapshot-name>_compile_check/`
  on POSIX. The scratch directory is disposable; no need to commit anything from it.

***

## 3. Stage 1 — Symbol-Surface Discovery

Enumerate every external symbol the snapshot references, sorted and deduplicated.

### 3.1 Imports

```powershell
cd <snapshot-dir>
Select-String -Path *.java -Pattern '^import ' | ForEach-Object { $_.Line } | Sort-Object -Unique
```

Classify each unique import into one of four buckets:

| Bucket | Action |
|---|---|
| `java.*`, `javax.*` | None — JDK built-in. |
| Third-party library (`com.sun.jna.*`, `org.apache.logging.log4j.*`, etc.) | Provide the real JAR on the classpath. |
| **Internal self-imports** within the snapshot's own package | None — `javac` resolves these from the source set itself. |
| **Host-project packages** (everything else) | Stub required — proceed to §3.2. |

### 3.2 Qualified references (catches symbols pulled in via `*` imports or fully-qualified names)

```powershell
Select-String -Path *.java -Pattern '<HostClass>\.|<HostClass2>\.' |
    ForEach-Object { $_.Line.Trim() } | Sort-Object -Unique
```

For each host class identified in §3.1, grep for member accesses to enumerate the **minimum** API surface that
must be stubbed. A common rookie failure is stubbing only the class but forgetting one of its constants — the
compile then fails with `cannot find symbol: variable FOO`.

### 3.3 Result

A short text inventory of:

1. Library JARs needed on the classpath (each at a specific version).
2. Host classes needed as stubs, each with their used member list (methods + constants + nested types).

Commit this inventory to the scratch directory's `INVENTORY.md` for traceability if the validation is being
recorded.

***

## 4. Stage 2 — Stub Generation

Write **compile-only** stubs in the scratch directory. The stubs must:

1. Live under `<scratch>/stubs/<package-path>/<ClassName>.java`.
2. Declare the exact `package` of the host class.
3. Expose every member listed in §3.2 with the correct signature (parameter types + return type + modifiers).
4. Implement method bodies with the simplest no-op possible: `return null` / `return ""` / `return 0` / `return false`
   / empty `{}` for `void`.
5. Carry a `/** Compile-only stub of … */` Javadoc header so the file's purpose is obvious in a later audit.

**Forbidden in stubs**: functional logic, real dependencies, transitive imports. A stub that calls real code
introduces a second symbol-resolution problem and defeats the purpose.

### 4.1 Stubs for interfaces

If a stub class is an `interface`, only declare the abstract methods that are actually called. Default methods
and unused members can be omitted — `javac` only checks the call sites in the snapshot.

### 4.2 Stubs for enums / constants

If only constants are used, declare them as `public static final` on the stub class — no need to make it an
`enum` unless the snapshot uses `EnumName.values()` / `EnumName.valueOf(...)` / `switch (e) { case X: }`.

### 4.3 Compile the stubs first

```powershell
$work = '<scratch>'
$stubs = Get-ChildItem "$work\stubs" -Recurse -Filter *.java | ForEach-Object FullName
javac -d "$work\stubs-bin" $stubs
```

If the stubs themselves don't compile, fix them before moving on. A compile error in `stubs-bin` is **always**
cheaper to fix than the same error misattributed to the snapshot.

***

## 5. Stage 3 — Snapshot Compile

```powershell
$snapshot = Get-ChildItem '<snapshot-dir>' -Filter *.java -Recurse | ForEach-Object FullName
$cp = "$work\stubs-bin;<lib-jar-1>;<lib-jar-2>"
javac -d "$work\out" -cp $cp $snapshot
```

### 5.1 Pass criteria

1. `javac` exit code 0.
2. Every input `.java` produces at least one `.class` in `$work\out\`.
3. Patch-introduced inner classes (e.g., new `Level` enum from a log-format upgrade) appear as
   `<Class>$<Inner>.class`.

Verify:

```powershell
Get-ChildItem "$work\out" -Recurse -Filter *.class | ForEach-Object { $_.Name } | Sort-Object
```

### 5.2 Common failures and their root cause

| `javac` error | Root cause | Fix |
|---|---|---|
| `package <p> does not exist` | Missed a host package in §3 | Add stub for the missing class. |
| `cannot find symbol: variable FOO` | Stubbed the class but not the constant | Add `public static final … FOO = …;` to the stub. |
| `cannot find symbol: method bar(String)` | Wrong overload in stub | Add the overload to the stub. |
| `incompatible types: <X> cannot be converted to <Y>` | Stub return type doesn't match host | Adjust stub signature; do NOT change the snapshot. |
| `unreported exception <E>` | Stub method lacks `throws <E>` | Add the `throws` clause. |
| `class <C> is public, should be declared in a file named <C>.java` | Stub package layout wrong | Move stub `.java` to the correct directory. |

***

## 6. Stage 4 — Hand-Back Verdict Template

| Step | Result |
|---|---|
| Symbol-surface discovery | ✅/❌ N unique imports, M host classes identified |
| Stub generation | ✅/❌ N stub `.java` files under `<scratch>/stubs/` |
| Stub self-compile | ✅/❌ exit 0 |
| Snapshot compile (`javac` JDK \<ver\>) | ✅/❌ exit 0 |
| Output classes | ✅/❌ N `.class` files incl. \<new inner classes if any\> |
| Patch-introduced symbols present | ✅/❌ `<Class>$<NewInner>.class` confirmed |

The verdict MUST close with an explicit statement of what was **not** verified — at minimum runtime behaviour,
integration paths, and any host-side initialization (constructors, static blocks, OSGi activators).

***

## 7. SSOT Compliance

- Project structure and folder conventions: see the [Project Structure Skill](../project-structure/SKILL.md).
- Markdown formatting: see the [Markdown Generation Skill](../markdown-generation/SKILL.md).
- Redaction & portability before commit: see the [Redaction & Portability Skill](../redaction-portability/SKILL.md).
- PowerShell script craftsmanship (if you later wrap this skill in a script): see the
  [Script Management Rules](../../../ai-agent-rules/script-management-rules.md).

***

## 8. Composition by Higher-Level Skills

No composers are registered in this public repository. Organization-specific
composers (which supply the host project's toolbase JDK, the resolved
library-JAR paths, the concrete host stubs, and the expected output class
set) live in the organization's own private skills repository and MUST link
back to this base in their **Composition Rationale** section so the
dependency graph remains bidirectionally discoverable from the consuming
side.

***

## 9. Related Conversations & Traceability

- 2026-05-12 — First end-to-end exercise of this protocol against a vendored telemetry-adapter snapshot after a
  cross-consumer log-format helper patch (`Level` enum + ISO-8601 banner + runtime-threshold sysprop). All 6 verdict
  rows passed; a small number of stub classes were sufficient and the expected output `.class` set (including the
  patch-introduced inner `$Level.class`) was produced. Concrete project names, stub class lists, and exact counts
  live in the organization-specific composer skill's private repository per the
  [Redaction & Portability Skill](../redaction-portability/SKILL.md).
