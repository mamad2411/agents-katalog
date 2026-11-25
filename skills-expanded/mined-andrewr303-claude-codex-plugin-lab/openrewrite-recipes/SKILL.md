---
name: openrewrite-recipes
description: Automated refactoring at scale with OpenRewrite — run prepackaged recipes for cleanup, security fixes, framework migrations, and static-analysis remediation via the Maven/Gradle plugins, and author declarative YAML recipes. Use for JVM tech-debt burndown, Java/dependency/framework upgrades, or fixing one pattern safely across an entire codebase.
---

# OpenRewrite Recipes

OpenRewrite is an automated refactoring engine. **Recipes** transform a
**Lossless Semantic Tree (LST)** — a type-attributed AST that preserves all
formatting and comments — so changes are semantically safe and produce minimal
diffs. Parsers and base recipes exist for Java, Kotlin, Groovy,
JavaScript/TypeScript, Python, and C#; the Maven/Gradle plugins run recipes
against JVM builds one repository at a time (multi-repo and non-JVM recipe runs
are the commercial Moderne platform's territory).

## When to Use This Skill

| Scenario | Use this skill | Alternative |
|----------|---------------|-------------|
| Java/Spring/JUnit framework or version migration | Yes | N/A |
| Codebase-wide static-analysis remediation with guaranteed-valid edits | Yes | `/avr-debug:code-antipatterns` to detect only |
| Formatting/import cleanup across a JVM repo | Yes | The project's formatter for single files |
| Structural find/replace in non-JVM code | No — use `ast-grep-search` | `semgrep-scan` `fix:` for semantic autofix |
| Detecting issues without changing code | No — dry-run only reports; use scanners | `/avr-debug:code-complexity`, `semgrep-scan` |

Rule of thumb: detection belongs to the scanners; **remediation at scale on JVM
code** belongs to OpenRewrite, because its edits are type-checked, not textual.

## Running Recipes (no build changes needed)

Maven — run one recipe module ad hoc:

```bash
mvn -U org.openrewrite.maven:rewrite-maven-plugin:run \
  -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-static-analysis:RELEASE \
  -Drewrite.activeRecipes=org.openrewrite.staticanalysis.CommonStaticAnalysis
```

Use `rewrite-maven-plugin:dryRun` to preview: it writes `target/rewrite/rewrite.patch`
instead of modifying sources.

Gradle — add the plugin, then dry-run/run:

```groovy
plugins { id("org.openrewrite.rewrite") version("latest.release") }
rewrite {
    activeRecipe("org.openrewrite.staticanalysis.CommonStaticAnalysis")
    setExportDatatables(true)
}
dependencies { rewrite("org.openrewrite.recipe:rewrite-static-analysis:latest.release") }
```

```bash
./gradlew rewriteDryRun   # report + patch file, no source changes
./gradlew rewriteRun      # apply changes to sources
```

## Recipes Worth Knowing for Code Health

| Recipe | Effect |
|--------|--------|
| `org.openrewrite.staticanalysis.CommonStaticAnalysis` | Bundle of dozens of static-analysis fixes |
| `org.openrewrite.java.RemoveUnusedImports` | Strip unused imports |
| `org.openrewrite.java.format.AutoFormat` | Reformat to project style |
| `org.openrewrite.staticanalysis.MissingOverrideAnnotation` | Add missing `@Override` |
| `org.openrewrite.java.migrate.UpgradeToJava21` | Java version migration (from `rewrite-migrate-java`) |
| `org.openrewrite.java.testing.junit5.JUnit4to5Migration` | JUnit 4 → 5 (from `rewrite-testing-frameworks`) |
| `org.openrewrite.maven.UpgradeDependencyVersion` / `org.openrewrite.gradle.UpgradeDependencyVersion` | Targeted dependency bumps |

Discover what's available: `mvn rewrite:discover` lists recipes on the plugin
classpath; the full catalog with per-recipe docs lives at docs.openrewrite.org.
Recipe modules are separate artifacts (`rewrite-static-analysis`,
`rewrite-migrate-java`, `rewrite-spring`, `rewrite-testing-frameworks`, …) —
add the one that contains your recipe to `recipeArtifactCoordinates` (Maven)
or the `rewrite(...)` dependency configuration (Gradle).

## Composing Your Own Recipe (declarative YAML)

Drop a `rewrite.yml` at the repo root; compose existing recipes with options —
no code required:

```yaml
---
type: specs.openrewrite.org/v1beta/recipe
name: com.yourorg.HealthSweep
displayName: Repo health sweep
description: Imports, formatting, and common static analysis in one pass.
recipeList:
  - org.openrewrite.java.RemoveUnusedImports
  - org.openrewrite.staticanalysis.CommonStaticAnalysis
  - org.openrewrite.java.format.AutoFormat
```

Then `activeRecipes=com.yourorg.HealthSweep`. Recipe naming conventions and
design rationale live in the project's ADRs (`doc/adr/` in the OpenRewrite repo).

## Workflow

1. **Dry-run first, always** — review `rewrite.patch` before touching sources.
2. **One recipe (or one composed sweep) per commit** — keeps diffs reviewable
   and bisectable; large migrations land as a series, not one mega-commit.
3. **Build + tests after each run** — LST edits are type-safe, but behavior
   changes from migrations (e.g. dependency upgrades) still need the suite.
4. **Data tables** — with `setExportDatatables(true)` (Gradle) the run emits
   CSV reports of what changed and why; cite them in the PR description.
5. Pair with `/avr-debug:code-review` on the resulting diff — automated does
   not mean unreviewed.

## Related Skills

- `ast-grep-search` — lightweight structural rewrites outside JVM builds
- `semgrep-scan` — semantic detection and small autofixes across 30+ languages
- `/avr-debug:code-antipatterns`, `/avr-debug:code-complexity` — find the debt this skill burns down
- `/avr-debug:code-dep-audit` — identify vulnerable dependencies before targeted `UpgradeDependencyVersion` runs
