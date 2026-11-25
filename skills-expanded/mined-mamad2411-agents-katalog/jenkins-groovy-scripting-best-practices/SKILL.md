---
name: jenkins-groovy-scripting-best-practices
description: >
  Covers writing safe, testable Groovy inside Jenkins pipelines and shared
  libraries — the script security sandbox and approval workflow, unit
  testing with JenkinsPipelineUnit, CPS (Continuation-Passing Style)
  quirks, and common Groovy pitfalls specific to the pipeline execution
  context. Use when the user hits "script not permitted to use" sandbox
  errors, asks to "test Jenkins pipeline Groovy code," "approve a Jenkins
  script signature," or "fix a Groovy serialization/CPS error" in a
  Jenkinsfile or shared library.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cicd-tooling
  maturity: stable
---

# Jenkins Groovy Scripting Best Practices

## Purpose

Jenkins Pipeline (both per-repo Jenkinsfiles and shared libraries) is
written in Groovy, but it does not run like ordinary Groovy: it executes
under the **Groovy sandbox** (a security boundary that blocks arbitrary
Java/Groovy method calls unless explicitly approved) and under **CPS
(Continuation-Passing Style)** transformation (so pipelines can pause/
resume across Jenkins restarts), both of which produce failure modes that
look like bugs in your code but are actually artifacts of the execution
model. This skill covers the sandbox/script-approval workflow, how to unit
test shared library Groovy without a running Jenkins controller, and the
specific Groovy/CPS pitfalls (closures capturing `this`, non-serializable
state, `@NonCPS` usage) that recur in pipeline code.

## When to use

- A pipeline or shared library fails with `org.jenkinsci.plugins.scriptsecurity.
  sandbox.RejectedAccessException: Scripts not permitted to use ...`.
- Writing or reviewing Groovy code in a `Jenkinsfile`'s `script {}` block or
  in a shared library's `vars/`/`src/` files (see
  [jenkins-declarative-pipeline-per-repo](../jenkins-declarative-pipeline-per-repo/SKILL.md)
  and
  [jenkins-centralized-shared-library](../jenkins-centralized-shared-library/SKILL.md)
  for where this code lives).
- Setting up automated tests for shared library logic so changes are
  verified before a version tag is cut, rather than only discovered when a
  consumer's build breaks.
- Debugging `NotSerializableException`, unexpectedly re-executed code after
  a controller restart, or a closure that behaves differently than plain
  Groovy would suggest.
- Deciding whether a piece of logic should be `@NonCPS`-annotated.

## Prerequisites & environment

- A Jenkins controller with the **Script Security** plugin (bundled with
  modern Jenkins Pipeline installs) — this is what enforces the sandbox and
  stores approved signatures under **Manage Jenkins → In-process Script
  Approval**.
- Administrator access to approve pending script signatures (only Jenkins
  admins can approve; a pipeline author who hits a `RejectedAccessException`
  must request approval, not self-approve unless they hold that role).
- For unit testing: a JVM project (Maven or Gradle) alongside the shared
  library repo, with the **JenkinsPipelineUnit** library
  (`lesfurets:jenkins-pipeline-unit`) added as a test dependency, and a
  test framework (JUnit 5 or Spock) to drive it.
- Groovy 2.x/3.x knowledge (whichever your Jenkins version bundles — check
  **Manage Jenkins → System Information** for the exact Groovy version) —
  syntax mostly matches plain Groovy but some newer Groovy language
  features may not be supported inside the CPS-transformed subset.

## Step-by-step guidance

1. **Understand what the sandbox blocks.** By default, Pipeline scripts run
   in a sandbox that only allows a pre-approved allowlist of methods/
   constructors/static methods. Calling an unapproved method (e.g. a
   non-whitelisted Java standard library method, or certain Groovy
   metaprogramming) throws:
   ```
   org.jenkinsci.plugins.scriptsecurity.sandbox.RejectedAccessException:
   Scripts not permitted to use method java.lang.String.format java.lang.String java.lang.Object[]
   ```
   This is not a bug in your Groovy — it's the sandbox doing its job.

2. **Approve the specific signature, don't disable the sandbox.** As an
   admin, go to **Manage Jenkins → In-process Script Approval**, review the
   pending signature request, and approve only that specific method
   signature if it's legitimately needed and safe:
   ```
   method java.lang.String format java.lang.String java.lang.Object[]
   ```
   Never check "Process as though script requests are outside the sandbox"
   / mark the whole Jenkinsfile as unsandboxed as a workaround — this
   defeats the security control across every use of that
   Jenkinsfile/library going forward and is a real security regression, not
   a convenience.

3. **Prefer Pipeline-provided steps over raw Java/Groovy APIs** where an
   equivalent step exists (`readJSON`/`writeJSON` from the Pipeline
   Utility Steps plugin instead of `groovy.json.JsonSlurper` directly,
   `sh(script: ..., returnStdout: true)` instead of `ProcessBuilder`) —
   these are already sandbox-approved and portable across controllers,
   avoiding a per-controller approval request.

4. **Mark pure-computation helper methods `@NonCPS`** when they don't call
   pipeline steps and don't need to survive a controller restart mid-
   execution — this avoids CPS transformation overhead and sidesteps CPS
   limitations on certain Groovy constructs (e.g. some collection methods
   with closures):
   ```groovy
   @NonCPS
   def parseVersion(String tag) {
       def m = (tag =~ /^v(\d+)\.(\d+)\.(\d+)$/)
       return m ? [major: m[0][1] as int, minor: m[0][2] as int, patch: m[0][3] as int] : null
   }
   ```
   Never call a pipeline step (`sh`, `sleep`, `input`) from inside a
   `@NonCPS` method — it will fail or behave incorrectly, since `@NonCPS`
   methods run outside the CPS interpreter that pipeline steps depend on.

5. **Implement `Serializable` on any `src/` class whose instances are held
   across pipeline steps**, since Jenkins periodically serializes the
   pipeline's execution state to disk for durability across restarts:
   ```groovy
   class DeployTarget implements Serializable {
       String environment
       String region
   }
   ```
   A class held in a pipeline variable that isn't serializable throws
   `NotSerializableException` at the first checkpoint after it's used.

6. **Unit test shared library code with JenkinsPipelineUnit** instead of
   only validating by pushing to a real Jenkins and watching a build:
   ```groovy
   // test/groovy/NodeServicePipelineTest.groovy
   import com.lesfurets.jenkins.unit.BasePipelineTest
   import org.junit.Before
   import org.junit.Test
   import static org.junit.Assert.assertTrue

   class NodeServicePipelineTest extends BasePipelineTest {
       @Override
       @Before
       void setUp() throws Exception {
           super.setUp()
       }

       @Test
       void 'fails fast when serviceName is missing'() {
           def script = loadScript('vars/nodeServicePipeline.groovy')
           def threw = false
           try {
               script.call([:])
           } catch (Exception e) {
               threw = true
               assertTrue(e.message.contains("'serviceName' is required"))
           }
           assertTrue(threw)
       }
   }
   ```
   Run via `./gradlew test` (or Maven equivalent) in CI for the shared
   library repo itself — this is what makes the library's own CI (see step
   6 of
   [jenkins-centralized-shared-library](../jenkins-centralized-shared-library/SKILL.md))
   meaningful rather than just a syntax check.

7. **Avoid closures that implicitly capture non-serializable pipeline
   state** across step boundaries (e.g. capturing the `steps` context
   object itself in a long-lived closure stored in a class field) — pass
   the `script`/`this` reference explicitly into helper methods instead of
   relying on implicit closure capture, which is both clearer and avoids
   subtle serialization failures.

## Best practices

- Treat every sandbox rejection as a decision point: approve the narrow
  signature if it's genuinely needed, or rewrite using an already-approved
  Pipeline step — never blanket-disable the sandbox for a whole library or
  Jenkinsfile.
- Keep `@NonCPS` methods pure (no pipeline steps, no side effects on shared
  mutable state) — they exist for CPU-bound parsing/computation, not
  orchestration.
- Write unit tests for every `vars/*.groovy` entry point's parameter
  validation and branching logic using JenkinsPipelineUnit; this catches
  regressions before a library version tag goes out to dozens of
  consumers.
- Keep Groovy files small and single-purpose; a `vars/*.groovy` file that
  has grown to hundreds of lines of nested `if`/`switch` logic is a sign
  the branching belongs in tested `src/` classes instead.
- Log meaningful context on failure (`error "nodeServicePipeline: expected
  config.serviceName, got: ${config}"`) rather than letting a raw
  `NullPointerException` surface — pipeline consumers debugging a shared
  library failure have no access to the library's source by default.
- Review the **In-process Script Approval** queue periodically as an
  admin task — an unreviewed queue either blocks legitimate pipeline
  authors indefinitely or accumulates approval requests nobody looks at.

## Common pitfalls

- **Symptom:**
  `RejectedAccessException: Scripts not permitted to use staticMethod
  java.util.UUID randomUUID` (or similar) appears the first time a new
  helper method runs, even though the same Groovy runs fine in a plain
  `groovy` script outside Jenkins.
  **Fix:** This is expected — the sandbox allowlist is independent of
  whether the code is "valid Groovy." Request/approve the specific
  signature in **In-process Script Approval**, or replace the call with an
  already-approved Pipeline Utility Steps equivalent.

- **Symptom:** A shared library's helper method that calls `sh(...)`
  fails or hangs when marked `@NonCPS`.
  **Fix:** `@NonCPS` methods run outside the CPS interpreter and cannot
  call pipeline steps; remove the annotation from any method that invokes
  `sh`, `sleep`, `input`, or other steps — reserve `@NonCPS` strictly for
  pure computation.

- **Symptom:** `java.io.NotSerializableException` thrown partway through a
  long-running pipeline, often after several stages have already
  succeeded.
  **Fix:** A class instance held in a pipeline-scoped variable across
  steps must implement `Serializable`; audit `src/` classes referenced
  from `vars/*.groovy` and add `implements Serializable`, or mark
  genuinely non-serializable fields (e.g. a network client) `transient`
  and re-initialize them lazily.

- **Symptom:** After a Jenkins controller restart, a step appears to
  re-run from an earlier point, producing duplicate side effects (e.g. a
  notification sent twice).
  **Fix:** This is CPS checkpoint/resume behavior interacting with
  non-idempotent side effects; make steps with external side effects
  idempotent where possible, or restructure so the side effect happens
  once at a clearly-checkpointed boundary rather than inside a loop that
  could partially replay.

- **Symptom:** A library author "temporarily" enables running the
  Jenkinsfile without sandbox restrictions to unblock a demo, then it
  ships that way to production.
  **Fix:** This should be flagged as a security regression, not a
  convenience — running unsandboxed means the pipeline's Groovy has full
  access to the Jenkins controller's JVM (including credentials store
  internals); revert to sandboxed execution and go through proper script
  approval for the specific signatures actually needed.

## Worked example

**Scenario:** A shared library's `vars/nodeServicePipeline.groovy` (from
[jenkins-centralized-shared-library](../jenkins-centralized-shared-library/SKILL.md))
needs a helper to parse a semantic version tag and decide whether a build
is a pre-release, plus a unit test proving the parsing logic works before
it's used by 30 consumer repos.

`src/org/example/pipeline/VersionUtil.groovy`:
```groovy
package org.example.pipeline

class VersionUtil implements Serializable {
    @NonCPS
    static Map parse(String tag) {
        def m = (tag =~ /^v(\d+)\.(\d+)\.(\d+)(-rc\.\d+)?$/)
        if (!m) {
            return null
        }
        return [
            major: m[0][1] as int,
            minor: m[0][2] as int,
            patch: m[0][3] as int,
            isPrerelease: m[0][4] != null
        ]
    }
}
```

`vars/nodeServicePipeline.groovy` (excerpt):
```groovy
script {
    def v = org.example.pipeline.VersionUtil.parse(env.GIT_TAG_NAME ?: '')
    if (v?.isPrerelease) {
        echo "Skipping production deploy for pre-release tag ${env.GIT_TAG_NAME}"
        return
    }
}
```

`test/groovy/VersionUtilTest.groovy` (run in the library's own CI, no
Jenkins controller required):
```groovy
import org.example.pipeline.VersionUtil
import org.junit.Test
import static org.junit.Assert.assertEquals
import static org.junit.Assert.assertNull

class VersionUtilTest {
    @Test
    void 'parses a stable version tag'() {
        def v = VersionUtil.parse('v1.4.2')
        assertEquals(1, v.major)
        assertEquals(4, v.minor)
        assertEquals(2, v.patch)
        assertEquals(false, v.isPrerelease)
    }

    @Test
    void 'flags a release-candidate tag as prerelease'() {
        def v = VersionUtil.parse('v2.0.0-rc.1')
        assertEquals(true, v.isPrerelease)
    }

    @Test
    void 'returns null for a malformed tag'() {
        assertNull(VersionUtil.parse('not-a-version'))
    }
}
```
Because `VersionUtil.parse` is `@NonCPS` and does no pipeline I/O, it can
be unit tested as ordinary Groovy/JUnit with no Jenkins controller —
regressions in the tag-parsing regex are caught in the library's own CI
before any of the 30 consumer repos' pipelines run it.

## Cross-references

- [jenkins-declarative-pipeline-per-repo](../jenkins-declarative-pipeline-per-repo/SKILL.md) — where `script {}` blocks containing this Groovy typically live for a single repo.
- [jenkins-centralized-shared-library](../jenkins-centralized-shared-library/SKILL.md) — the `vars/`/`src/` structure this Groovy code is organized into at org scale.
- [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md) — general pipeline security-gate design, complementary to the script-sandbox security boundary covered here.
