---
name: maven-pom-audit
description: Section-by-section audit of Maven pom.xml files — catching invalid URLs, wrong identities, missing metadata, and enforcing placeholder conventions.
category: Build & Dependency Management
---

# Maven POM Audit Skill

> **Skill ID:** `maven-pom-audit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Perform a systematic, section-by-section audit of Maven `pom.xml` files
to detect invalid URLs, stale developer identities, missing mandatory
metadata, hardcoded endpoints, unpinned dependency/plugin versions, and
non-standard properties. Fixes use the `YOUR_*` placeholder convention
with `<!-- TODO -->` comments so the POM remains valid XML while clearly
marking what needs real values later.

This skill preserves every existing section — it audits and fixes, never
removes. The philosophy is: **a perfect POM with placeholders is better
than a broken POM with fake URLs that silently fail.**

## Prerequisites

| Requirement | Minimum |
|---|---|
| Maven | 3.6+ |
| Java | 8+ (for `mvn` execution) |
| Shell | PowerShell 5.1+ or Bash 4+ |
| VCS | Git (for developer identity derivation) |

## When to Apply

Apply this skill when:
- A new Maven project is being initialized
- A user asks to "audit the pom" or "fix pom.xml"
- Invalid URLs, placeholder values, or `example.com` domains are detected
- Developer identity does not match the actual author
- Pre-commit or pre-release audit is requested
- A project is being migrated to a new repository host

Do NOT apply when:
- The build system is Gradle, sbt, or non-Maven (different audit needed)
- The POM is a BOM/parent POM (different structure — adapt checklist)
- The user explicitly says "leave the POM as-is"

---

## Step-by-Step Procedure

### Step 1 — Locate All POM Files

Find every `pom.xml` in the project. Multi-module projects have one per module.

```powershell
Get-ChildItem -Recurse -Filter "pom.xml" |
    Where-Object { $_.FullName -notmatch '\\(target|\.git|node_modules)\\' } |
    Select-Object FullName
```

```bash
find . -name "pom.xml" -not -path "*/target/*" -not -path "*/.git/*"
```

### Step 2 — Audit GAV & Project Metadata

Check the **identity block** — the first thing anyone reads:

| Element | Rule | Example |
|---|---|---|
| `<groupId>` | Must be a real, reversed-domain package | `com.acme.toolkit` |
| `<artifactId>` | Must match project naming convention (underscore if applicable) | `acme_logging` |
| `<version>` | Must follow SemVer; no `-SNAPSHOT` in release commits | `1.0.0` |
| `<packaging>` | Must be explicit (`jar`, `pom`, `war`) — never rely on default | `jar` |
| `<name>` | Human-readable project name — must exist | `Acme Logging` |
| `<description>` | One-sentence summary — must exist and be meaningful | Not just the artifact name |
| `<url>` | Must be valid OR a `<!-- TODO -->` placeholder | See Step 4 |
| `<licenses>` | Must contain at least one `<license>` with `<name>` and `<url>` | `Apache-2.0` |

**Red flags:**
- `<groupId>` is `com.example` or `org.example`
- `<description>` is empty or identical to `<name>`
- `<licenses>` section is missing entirely

### Step 3 — Audit Developer Identity

The `<developers>` section must reflect the actual project author(s).

**Derivation command:**
```powershell
git config user.name; git config user.email
```

```bash
git config user.name && git config user.email
```

| Element | Rule |
|---|---|
| `<name>` | Must match `git config user.name` or the real author |
| `<email>` | Must match `git config user.email` or the real contact |
| `<organization>` | Must be the actual organization, not a placeholder |

**Red flags:**
- Generic names: `Acme Team`, `Dev Team`, `John Doe`
- Generic emails: `team@example.com`, `dev@company.com`
- Missing `<developers>` section entirely

### Step 4 — Audit URLs

Every URL in the POM must be either **valid and reachable** or replaced
with a `YOUR_*` placeholder + `<!-- TODO -->` comment.

#### 4.1 Project URL

```xml
<!-- GOOD: placeholder with TODO -->
<url><!-- TODO: set project URL once VCS is configured --></url>

<!-- BAD: fake URL that returns 404 -->
<url>https://dev.azure.com/fake-org/fake-project</url>
```

#### 4.2 SCM Block

```xml
<scm>
    <!-- TODO: update once repository is hosted in VCS -->
    <connection>scm:git:https://YOUR_VCS_HOST/YOUR_ORG/project_name.git</connection>
    <developerConnection>scm:git:https://YOUR_VCS_HOST/YOUR_ORG/project_name.git</developerConnection>
    <url>https://YOUR_VCS_HOST/YOUR_ORG/project_name</url>
</scm>
```

#### 4.3 Distribution Management (per profile)

Each deployment profile's `<distributionManagement>` URLs must use the
`YOUR_*` convention if the target is not yet configured:

| Host Type | Placeholder |
|---|---|
| Azure Artifacts | `https://pkgs.dev.azure.com/YOUR_ORG/YOUR_PROJECT/_packaging/YOUR_FEED/maven/v1` |
| Reposilite | `https://YOUR_REPOSILITE_HOST/releases` |
| Sonatype Nexus | `https://YOUR_NEXUS_HOST/repository/maven-releases/` |
| Maven Central | No placeholder needed — uses standard `central-publishing-maven-plugin` |
| JitPack | No URL needed — JitPack infers from GitHub |

### Step 5 — Audit Properties & Encoding

| Property | Required | Standard Value |
|---|---|---|
| `<project.build.sourceEncoding>` | **MANDATORY** | `UTF-8` |
| `<maven.compiler.source>` | **MANDATORY** | `11` (or project minimum) |
| `<maven.compiler.target>` | **MANDATORY** | Must match `source` |
| `<project.build.outputTimestamp>` | Recommended (Maven 3.9+) | ISO-8601 date — enables reproducible builds |

**Red flags:**
- Missing encoding → platform-dependent builds (works on dev machine, fails in CI)
- `source` and `target` mismatch
- Dependency versions hardcoded inline instead of in `<properties>`

### Step 6 — Audit Dependencies

| Rule | Check |
|---|---|
| Version pinning | Every `<dependency>` must have an explicit `<version>` or inherit from a BOM |
| No SNAPSHOT in release | If `<version>` is not `-SNAPSHOT`, no dependency should be `-SNAPSHOT` |
| Version properties | Versions should be extracted to `<properties>` for multi-use dependencies |
| Scope correctness | `test` dependencies must have `<scope>test</scope>` |
| No duplicate GAVs | Same `groupId:artifactId` must not appear twice |

**Scan for SNAPSHOT dependencies:**
```powershell
Select-String -Path pom.xml -Pattern "SNAPSHOT" | Format-Table LineNumber, Line -AutoSize
```

### Step 7 — Audit Plugins

| Rule | Check |
|---|---|
| Pinned versions | Every `<plugin>` must have an explicit `<version>` — never rely on Maven super-POM defaults |
| Essential plugins present | `maven-compiler-plugin`, `maven-source-plugin`, `maven-javadoc-plugin` for library projects |
| JAR plugin config | `maven-jar-plugin` should include meaningful `<manifestEntries>` if applicable |
| GPG signing | Required for Maven Central profile — `maven-gpg-plugin` must exist in `central` profile |

**Red flags:**
- Plugin without `<version>` → builds are not reproducible across Maven versions
- `maven-compiler-plugin` missing → relies on super-POM defaults (Java 5)

### Step 8 — Audit Profiles

Each `<profile>` must be:

| Rule | Check |
|---|---|
| Has `<id>` | Descriptive, lowercase identifier |
| Activation is explicit | `<activeByDefault>`, property-based, or CLI (`-P`) — never ambiguous |
| URLs use placeholders | If the target is not configured, use `YOUR_*` pattern (Step 4) |
| No duplicate server IDs | `<id>` in `<repository>` must match `settings.xml` server IDs |

### Step 9 — Apply Fixes

When fixing issues found in Steps 2–8:

1. **Never remove sections** — replace invalid values with `YOUR_*` placeholders
2. **Always add `<!-- TODO -->` comments** — marks exactly what needs real values
3. **Derive developer identity from git config** — not from assumptions
4. **Keep industry-standard elements** — `<project.build.outputTimestamp>`, reproducible build config, etc.
5. **Update cascading files** — CI/CD configs, documentation, agent skills that reference POM values

#### Cascading File Checklist

After modifying `pom.xml`, check these files for stale references:

| File Type | What to Check |
|---|---|
| CI/CD configs (`*-pipelines.yml`, `.github/workflows/`) | Artifact IDs, feed names, deploy URLs |
| IDE configs (`.project`, `.classpath`) | Project name matching `<artifactId>` |
| Agent skills (`SKILL.md`, references) | Dependency coordinates, artifact IDs |
| Documentation (`README.md`, setup guides) | Maven coordinates, repository URLs |
| JitPack config (`jitpack.yml`) | Coordinate references |

### Step 10 — Verify

Run a final check to ensure no invalid URLs or stale values remain:

```powershell
# Check for common invalid URL patterns — add your own org's leak markers
# (e.g. `internal\.<corp>`, `<CORP>_ORG`, `<CORP>_PROJECT`) to the alternation below.
Get-ChildItem -Recurse -File |
    Where-Object { $_.FullName -notmatch '\\(target|\.git)\\' } |
    Select-String -Pattern "example\.com|fake-org|YOUR_ORG|YOUR_PROJECT|TODO" |
    Format-Table Filename, LineNumber, Line -AutoSize
```

```bash
grep -rn "example\.com\|fake-org\|YOUR_ORG\|YOUR_PROJECT\|TODO" \
    --include="*.xml" --include="*.yml" --include="*.md" \
    --exclude-dir='{target,.git}' .
```

**Also validate the POM parses correctly:**
```bash
mvn validate -q
```

---

## Audit Checklist (Quick Reference)

Single-glance table for rapid audits:

| # | Section | Check | Pass Criteria |
|---|---|---|---|
| 1 | GAV | `groupId`, `artifactId`, `version` | Real domain, correct convention, SemVer |
| 2 | Metadata | `name`, `description`, `url` | Present, meaningful, valid or TODO |
| 3 | License | `<licenses>` block | At least one with `name` + `url` |
| 4 | Developer | `<developers>` block | Matches `git config` identity |
| 5 | SCM | `<scm>` block | Valid URLs or `YOUR_*` placeholders |
| 6 | Encoding | `project.build.sourceEncoding` | `UTF-8` |
| 7 | Compiler | `maven.compiler.source/target` | Explicit, matching values |
| 8 | Reproducible | `project.build.outputTimestamp` | Present (Maven 3.9+) |
| 9 | Dependencies | Version pinning | All explicit, no inline hardcoding |
| 10 | Plugins | Version pinning | All explicit, essential set present |
| 11 | Profiles | Structure | Valid IDs, placeholder URLs, no dupes |
| 12 | Cascading | CI/CD, docs, skills | All references match POM values |

***

## Placeholder Convention (SSOT)

All placeholders follow this pattern:

| Pattern | Usage |
|---|---|
| `YOUR_VCS_HOST` | Git hosting domain (e.g., `github.com`, `dev.azure.com`) |
| `YOUR_ORG` | Organization or account name |
| `YOUR_PROJECT` | Azure DevOps project name (Azure only) |
| `YOUR_FEED` | Package feed name |
| `YOUR_REPOSILITE_HOST` | Reposilite instance domain |
| `YOUR_NEXUS_HOST` | Nexus CE instance domain |
| `YOUR_TUL_SERVER` | Application-specific server (example from tul_logging) |
| `YOUR_ENDPOINT` | Application-specific API endpoint |

**Rules:**
- Always `UPPER_SNAKE_CASE` prefixed with `YOUR_`
- Always accompanied by a `<!-- TODO: ... -->` comment in XML
- Always accompanied by a `# TODO: ...` comment in YAML/properties
- Placeholders must be greppable: `Select-String -Pattern "YOUR_"` finds all

***

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Removing POM sections** — Audit fixes replace values, never delete structure
- **Inventing URLs** — If the real URL is unknown, use a `YOUR_*` placeholder. Never guess
- **Inventing developer identity** — Derive from `git config` or ask the user. Never fabricate
- **Auto-upgrading dependency versions** — Flag stale versions but do not change them without explicit user approval
- **Removing `<project.build.outputTimestamp>`** — This is industry-standard for reproducible builds. Always keep
- **Leaving invalid URLs without placeholders** — Every URL must be valid OR use `YOUR_*`. No middle ground
- **Ignoring cascading files** — A POM change without updating CI/CD configs and docs is an incomplete fix
- **Running `mvn deploy`** — Audit only. Never trigger deployment during an audit

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Fixed POM but CI pipeline still references old artifact ID | Always run the cascading file checklist (Step 9) |
| Placeholder URL causes `mvn deploy` failure | Expected — placeholders are designed to fail loudly rather than silently POST to a wrong server |
| Removed `<project.build.outputTimestamp>` thinking it was stale | It is industry-standard since Maven 3.9+ — always keep it |
| Developer section has the original template author | Derive from `git config user.name` and `git config user.email` |
| Plugin version missing → works locally but fails in CI | Different Maven versions ship different super-POM defaults. Always pin |
| `<url>` points to a 404 page | Replace with `<!-- TODO: set project URL once VCS is configured -->` |
| Mixed placeholder styles (`TODO`, `FIXME`, `XXX`) | Standardize on `YOUR_*` + `<!-- TODO -->` exclusively |
| SNAPSHOT dependency in a release version POM | Flag and ask user — may be intentional during development |
