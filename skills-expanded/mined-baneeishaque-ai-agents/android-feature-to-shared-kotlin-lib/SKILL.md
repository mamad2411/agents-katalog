---
name: android-feature-to-shared-kotlin-lib
description: Industrial protocol for extracting a vertical feature slice from an Android (Java / Kotlin) application and porting it to a shared pure-Kotlin/JVM library that multiple JVM clients (Android, Kotlin CLI, desktop, server) can consume, with JitPack distribution, submodule-first commit discipline, and CRLF/LF working-tree hygiene.
category: Multi-Platform-Library-Engineering
---

# Android Feature → Shared Kotlin/JVM Library Porting Protocol

This skill captures the end-to-end workflow for taking a single feature
that lives only inside an Android application (Java or Kotlin, possibly
with Retrofit + a PHP/REST backend) and promoting it to a shared
**pure Kotlin/JVM library** so that:

- the Android app keeps the same behaviour by consuming the library;
- a Kotlin CLI (or any JVM client) can consume the same logic;
- distribution happens via **JitPack** (no Maven Central setup required).

Concretely the skill covers:

1. Locating the feature inside an Android codebase and identifying its
   vertical slice (API constants → Retrofit interface → DataSource →
   Operations layer → UI/Activity).
2. Porting each layer in dependency order into the shared library.
3. Wiring the new library function into the CLI (replacing a TODO stub).
4. Configuring `maven-publish` + `jitpack.yml` on the library.
5. Synchronising the library as a Git submodule of the CLI repo.
6. Committing in atomic, submodule-first order, with CRLF/LF discipline.

***

## 1. Reference Vertical Slice Anatomy

A typical "add resource" feature in an Android app using Retrofit has
exactly five layers. The shared library MUST own the bottom four; the
Android UI layer stays in the app (because it depends on `Activity` /
`Fragment` / Compose).

| Layer | Android-app location (typical) | Shared library location |
|---|---|---|
| 1. URL fragment / endpoint name | `ApiConstants` (often inline string in `ApiWrapper`) | `account.ledger.library.api.ApiConstants` |
| 2. Retrofit `@POST` / `@GET` interface | `Api` (often inline `OkHttp` call in `ApiWrapper`) | `account.ledger.library.api.Api` |
| 3. DataSource (suspend wrapper that calls the API) | absent in legacy Java; new in Kotlin | `account.ledger.library.retrofit.data.AccountsDataSource` |
| 4. Operations layer (business orchestration) | scattered across `Activity.onClick` | `account.ledger.library.operations.InsertOperations` |
| 5. UI layer | `Activity` + XML layout | stays in the Android app |

The skill's canonical exemplar is the `insertAccount` feature ported
from `Account-Ledger-Android-Client` to
`Account-Ledger-Library-Kotlin-Gradle`, consumed by both the Android
app (future migration) and the existing `Account-Ledger-Cli-Kotlin`.

## 2. Operational Logic

### 2.1 Phase 1 — Locate the Feature in the Android Source

Search the Android codebase for an entry point matching the feature
(e.g., an Activity named `Insert_Account.java`, an XML layout
`add_account.xml`, or a method `ApiWrapper.insertAccount()`). Capture:

- The exact endpoint URL fragment (e.g., `http_API/insert_Account.php`).
- The exact `@Field` / form-parameter set with their server-side names.
- The response type (often a `TransactionManipulationResponse` or
  similar JSON wrapper).
- Any default values applied by the UI (e.g., `accountType=GROUP`,
  `commodityType=CURRENCY`, `commodityValue=INR`).

### 2.2 Phase 2 — Map to Shared Library Layers

Decide, per layer, whether to **add a new symbol** or **extend an
existing one**.

- **ApiConstants**: usually add a single `const val` for the endpoint
  method name.
- **Api**: add an `@POST` interface method with `@Field` parameters
  that match the backend exactly (parameter names must match the
  backend's form-field names — this is the wire contract).
- **DataSource**: add a `suspend fun` that calls the API method.
    - Common pitfall: if the existing DataSource extends a generic
      base parametrised on a different response type
      (e.g., `AccountsDataSource : AppDataSource<AccountsResponse>`),
      and the new endpoint returns a different response type
      (`TransactionManipulationResponse`), you cannot reuse the parent
      class's helper. Drop down to the underlying generic primitive
      (e.g., `CommonDataSource<TransactionManipulationResponse>()`)
      directly inside the new method.
- **Operations layer**: add a public function that:
    - Constructs the DataSource.
    - Calls the suspend function.
    - Applies sensible defaults so callers do not have to pass every
      field.
    - **Reuses existing orchestration where possible** (e.g., the
      `manipulateTransaction()` helper already wraps the
      success / failure / retry flow for similar endpoints — reuse
      it instead of duplicating).

### 2.3 Phase 3 — Wire the CLI Consumer

The CLI typically has a stub like:

```kotlin
import common.utils.library.utils.ToDoUtilsInteractive

// in HandleInputs.kt option-3 branch:
ToDoUtilsInteractive.showTodo()
```

Replace with an interactive function that:

1. Reads each field via `readln()` with a sensible prompt.
2. Calls the new `Operations` function with the collected inputs.
3. Prints the success / failure result.

Update imports — remove the `ToDoUtilsInteractive` import, add the new
`account.ledger.library.operations.<Operations>` import.

### 2.4 Phase 4 — Configure JitPack Distribution

Two changes in the **library** repository:

#### 4a. `build.gradle.kts` of the publishable module

Add (or modify) the following:

```kotlin
plugins {
    `maven-publish`
    // existing plugins …
}

group = "com.github.<vcs-owner>"
version = "1.0.0"

java {
    withSourcesJar()
}

publishing {
    publications {
        create<MavenPublication>("mavenJava") {
            from(components["java"])
        }
    }
}
```

#### 4b. `jitpack.yml` at the library repo root

```yaml
jdk:
  - openjdk21
install:
  - ./gradlew :<lib-module>:publishToMavenLocal
```

Consumer (CLI / Android app) declares the dependency as:

```kotlin
implementation("com.github.<vcs-owner>:<lib-repo-name>:<tag>")
```

### 2.5 Phase 5 — Submodule-First Atomic Commits

The CLI consumes the library as a **git submodule**. Commit order MUST
be: library commits first → CLI commits second. Within each repo,
each commit MUST be atomic per the
[git-atomic-commit-construction](../git-atomic-commit-construction/SKILL.md)
protocol. The canonical decomposition for an Android→library port is:

| # | Repo | Commit type | Scope |
|---|---|---|---|
| L-1 | library | `feat(<feature>)` | The full vertical slice — ApiConstants + Api + DataSource + Operations as ONE atomic commit (they only compile together). |
| L-2 | library | `build(jitpack)` | `maven-publish` block in `build.gradle.kts` + `jitpack.yml` at root. |
| C-1 | cli | `fix(deps)` | Any dependency fixes the feature requires (e.g., Kotlin EAP version that exposes the new APIs). |
| C-2 | cli | `feat(<feature>)` | The new interactive consumer code **plus** the submodule pointer advance, in the SAME commit (the consumer code does not compile until the submodule points at L-2). |

The C-2 grouping (consumer code + submodule pointer) is a deliberate
Configuration Coupling per §5 of the atomic-commit rules.

### 2.6 Phase 6 — CRLF / LF Working-Tree Hygiene

When the library repo has `core.autocrlf = input` and stores `.kt`
files with CRLF in the HEAD blob, naive script-based edits (Python's
text-mode `open`, Node's default `fs.writeFile`, etc.) write LF and
trigger a full-file rewrite diff. Two cures:

1. **Preferred**: use the `edit` tool / `git apply` so existing line
   endings are preserved.
2. **Fallback**: after a text-mode write, re-encode the file to CRLF
   to match HEAD. Python recipe:

   ```python
   data = open(path, 'rb').read()
   crlf = data.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
   open(path, 'wb').write(crlf)
   ```

   After this, `git add` will normalise CRLF → LF on staging (per
   `core.autocrlf=input`) and the staged diff will show only the
   logical changes — no spurious line-ending churn.

### 2.7 Phase 7 — Verification

Before committing each side:

1. `./gradlew :<lib-module>:assemble` succeeds in the library.
2. `./gradlew :<cli-module>:compileKotlin` succeeds in the CLI with
   the submodule pointing at the new library HEAD.
3. JitPack dry-run (optional): `./gradlew :<lib-module>:publishToMavenLocal`
   produces a jar locally.

The CRLF cure above is verified by `git diff --cached <file>` showing
only the intended hunks — no full-file rewrite.

***

## 3. Reusable Scripts

| Script | Purpose |
|---|---|
| [scripts/feature-slice-inventory.py](scripts/feature-slice-inventory.py) | Given a feature name and an Android source root, list candidate files (Activity, layout, ApiWrapper method) that constitute the vertical slice. |
| [scripts/jitpack-config-bootstrap.py](scripts/jitpack-config-bootstrap.py) | Given a library module path and a VCS owner, append the `maven-publish` block to `build.gradle.kts` and create `jitpack.yml` at the repo root. Idempotent. |

***

## 4. Cross-References

- **Atomic commit discipline**: delegate to
  [git-atomic-commit-construction](../git-atomic-commit-construction/SKILL.md).
  The submodule-first commit order in §2.5 is a specialisation of that
  skill's Step 6 (Submodule Synchronization Protocol).
- **Submodule pointer advance metadata**: delegate to
  [git-submodule-commit-details](../git-submodule-commit-details/SKILL.md).
- **Dev-private config symlinks** (the runtime `.env` / JSON the CLI
  needs at execution time): delegate to
  [dev-env-private-config-symlink](../dev-env-private-config-symlink/SKILL.md).
- **Path / identity redaction** in this SKILL.md: delegate to
  [redaction-portability](../redaction-portability/SKILL.md).
- **Markdown lint**: project `markdownlint-cli2` invocation.

## 5. Prohibited Behaviors

The agent is **BLOCKED** from:

- Inlining `OkHttp` calls in the library — always use Retrofit
  interfaces so the library stays declarative.
- Duplicating orchestration logic (success / failure / retry flow)
  when an existing Operations helper can be reused.
- Committing the CLI consumer change before the library commits land
  and the submodule pointer is advanced (Step 6 violation —
  submodule-first discipline).
- Editing `.kt` files in the library without preserving the repo's
  HEAD line-ending convention (CRLF / LF). Either use the `edit` tool
  or apply the §2.6 cure.
- Auto-pushing after committing. Pushes require explicit user approval
  per the global push policy.

## 6. Composition Rationale

This skill is **atomic** at its own layer — the port itself is a
single coherent procedure. It **composes** several lower-level skills:

- `git-atomic-commit-construction` for the commit decomposition.
- `git-submodule-commit-details` for the parent-repo SHA-sync metadata.
- `redaction-portability` for SKILL.md hygiene.

Composer skills cite this skill back via their "Composition by
Higher-Level Skills" sections where applicable.

## 7. Traceability

This skill was extracted from the session that ported the
`insertAccount` feature from `Account-Ledger-Android-Client` (Java)
into the shared `Account-Ledger-Library-Kotlin-Gradle` (Kotlin/JVM),
wired it into the `Account-Ledger-Cli-Kotlin` CLI as
`HandleInputs.addAccountInteractive()`, configured JitPack distribution,
and landed the four commits L-1 / L-2 / C-1 / C-2 in that order.

The CRLF/LF discipline (§2.6) was discovered during that session when
Python text-mode writes caused full-file rewrite diffs that masked the
actual logical changes; the bytes-mode CRLF cure resolved it cleanly.
