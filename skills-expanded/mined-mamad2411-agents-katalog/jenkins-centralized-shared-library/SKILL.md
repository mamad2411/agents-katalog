---
name: jenkins-centralized-shared-library
description: >
  Designs and maintains an organization-wide Jenkins Shared Library
  (vars/ and src/ layout) so many repos consume a thin Jenkinsfile that
  calls one shared pipeline function, instead of duplicating pipeline
  logic per repo. Use when the user asks to "set up a Jenkins shared
  library," "centralize our Jenkinsfiles," "add a global pipeline
  function," "version the shared library," or "reduce duplicated Jenkins
  pipeline logic across repos."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cicd-tooling
  maturity: stable
---

# Jenkins Centralized Shared Library

## Purpose

When ten, fifty, or a hundred repos each carry their own hand-written
Jenkinsfile ([jenkins-declarative-pipeline-per-repo](../jenkins-declarative-pipeline-per-repo/SKILL.md)),
a single change — a new required security scan, a registry migration, a
Groovy bugfix — has to be copy-pasted into every repo, drifts immediately,
and is untestable in isolation. A **Jenkins Shared Library** solves this by
hosting the real pipeline logic in one Git repository (`vars/` for
callable global steps, `src/` for supporting Groovy classes), registered
once with the Jenkins controller, so every consuming repo's Jenkinsfile
shrinks to a few lines that call one shared function with parameters. This
skill covers the shared library's structure, how a thin per-repo
Jenkinsfile consumes it, and how to version the library so a change
doesn't break every pipeline simultaneously.

## When to use

- More than a handful of repos have near-duplicate Jenkinsfiles and a
  change (new stage, new gate, new notification channel) requires editing
  each one individually.
- Standing up Jenkins pipeline standards for a new team/org and wanting
  every repo's Jenkinsfile to be a thin wrapper from day one.
- An existing shared library needs a new global step (`vars/*.groovy`) or
  a breaking change that must be versioned so consumers can opt in
  gradually.
- Deciding what belongs in the shared library (org-wide, stable logic)
  versus the per-repo Jenkinsfile (repo-specific parameters) — see
  [jenkins-declarative-pipeline-per-repo](../jenkins-declarative-pipeline-per-repo/SKILL.md)
  for the per-repo side of that boundary.
- Debugging why a pipeline behaves differently after a shared library
  update landed on `main`/`master` and consumers pinned to a floating ref.

## Prerequisites & environment

- A dedicated Git repository for the shared library (commonly named
  `jenkins-shared-library` or `pipeline-library`), separate from any
  consumer application repo.
- Jenkins **Pipeline: Shared Groovy Libraries** plugin, and the library
  registered in **Manage Jenkins → System → Global Pipeline Libraries**
  with a `Name` (e.g. `shared-lib`), a default version, and either
  "Load implicitly" off (recommended — require explicit `@Library`) or on.
- Git tags or branches in the library repo to serve as version references
  (e.g. `v1.4.0`, or a floating `main` for early adoption only).
- Repo admin/Jenkins admin coordination: consuming repos need to reference
  the library by name and version in their Jenkinsfile; the library itself
  needs its own CI (recommended — see Step 6) so changes are tested before
  every consumer picks them up.
- Groovy familiarity for anyone modifying `src/` classes — see
  [jenkins-groovy-scripting-best-practices](../jenkins-groovy-scripting-best-practices/SKILL.md)
  for sandboxing and testing guidance specific to this code.

## Step-by-step guidance

1. **Lay out the library repo in the required structure** — Jenkins
   expects exactly these top-level directories:
   ```
   (root)
   ├── vars/
   │   ├── standardPipeline.groovy      # callable as standardPipeline(...)
   │   └── standardPipeline.txt         # optional: help text shown in Jenkins UI
   ├── src/
   │   └── org/example/pipeline/
   │       ├── DeployTarget.groovy      # supporting classes
   │       └── Notifier.groovy
   └── resources/
       └── org/example/pipeline/
           └── deploy-template.yaml     # static files loaded via libraryResource()
   ```

2. **Write the global step in `vars/`.** A `vars/<name>.groovy` file's
   `call()` method is what a consuming Jenkinsfile invokes as `<name>(...)`:
   ```groovy
   // vars/standardPipeline.groovy
   def call(Map config = [:]) {
       pipeline {
           agent { label config.agentLabel ?: 'linux-x64' }
           options {
               timeout(time: config.timeoutMinutes ?: 30, unit: 'MINUTES')
           }
           stages {
               stage('Build') {
                   steps { sh config.buildCommand ?: 'make build' }
               }
               stage('Test') {
                   steps { sh config.testCommand ?: 'make test' }
               }
               stage('Deploy') {
                   when { branch config.deployBranch ?: 'main' }
                   steps {
                       script {
                           org.example.pipeline.Notifier.notifyStart(this, config.serviceName)
                       }
                       sh "make deploy TARGET=${config.deployTarget ?: 'staging'}"
                   }
               }
           }
           post {
               failure {
                   script {
                       org.example.pipeline.Notifier.notifyFailure(this, config.serviceName)
                   }
               }
           }
       }
   }
   ```

3. **Put reusable, testable logic in `src/` classes**, not scattered across
   multiple `vars/*.groovy` files — this is ordinary Groovy/Java-style code
   and can be unit tested independently of a running Jenkins instance:
   ```groovy
   // src/org/example/pipeline/Notifier.groovy
   package org.example.pipeline

   class Notifier implements Serializable {
       static void notifyFailure(script, String serviceName) {
           script.slackSend(channel: '#builds', color: 'danger',
               message: "FAILED: ${serviceName} — ${script.env.BUILD_URL}")
       }
       static void notifyStart(script, String serviceName) {
           script.echo "Deploying ${serviceName}..."
       }
   }
   ```
   Passing `this`/`script` explicitly (rather than relying on an implicit
   global `steps` binding) keeps `src/` classes usable and unit-testable
   outside the Jenkins CPS runtime — see
   [jenkins-groovy-scripting-best-practices](../jenkins-groovy-scripting-best-practices/SKILL.md).

4. **Consume the library from a thin per-repo Jenkinsfile** using
   `@Library` pinned to an explicit version — never an unpinned/floating
   default unless the team has explicitly decided every repo should always
   track `main`:
   ```groovy
   @Library('shared-lib@v1.4.0') _

   standardPipeline(
       agentLabel: 'linux-x64',
       serviceName: 'checkout-api',
       buildCommand: 'npm ci && npm run build',
       testCommand: 'npm test',
       deployBranch: 'main',
       deployTarget: 'staging'
   )
   ```
   This is the entire Jenkinsfile for a consuming repo — all pipeline logic
   lives in the library, and repo-specific values are passed as a config
   map.

5. **Version the library deliberately.** Tag releases (`git tag v1.5.0`)
   and document a changelog; treat `vars/` function signatures as a public
   API — adding an optional `Map` key is backward compatible, removing or
   renaming one is a breaking change that requires a major version bump and
   a migration note for consumers.

6. **Give the shared library its own CI** (ironically, often a
   Jenkinsfile in the library repo itself, or a separate lightweight
   Groovy test runner) using the **JenkinsPipelineUnit** test framework so
   `vars/` and `src/` logic is validated before a tag is cut — see
   [jenkins-groovy-scripting-best-practices](../jenkins-groovy-scripting-best-practices/SKILL.md)
   for the test setup.

7. **Roll out breaking changes gradually.** Cut a new major version tag,
   update one or two pilot consumer repos to `@Library('shared-lib@v2.0.0')`,
   validate, then bulk-update the rest (a small script that finds and
   updates the `@Library` line across consumer repos, submitted as
   individual PRs — never force-push or bulk-edit consumer repos' default
   branches without their own review).

## Best practices

- Treat the shared library repo like a published package: semantic
  versioning, a changelog, and tagged releases — not a repo where
  consumers point at a floating branch.
- Keep `vars/*.groovy` thin (orchestration: stages, calling into `src/`)
  and put real logic/business rules in `src/` classes, which are easier to
  unit test and reuse across multiple `vars/` entry points.
- Provide a `.txt` companion file next to each `vars/*.groovy` (e.g.
  `standardPipeline.txt`) documenting the config map's expected keys — this
  renders in the Jenkins "Global Variables Reference" and saves consumers
  from reading the Groovy source to know what parameters exist.
- Default every optional config key sensibly (`config.timeoutMinutes ?:
  30`) so a minimal consumer Jenkinsfile still works, and document required
  keys explicitly (fail fast with a clear error if a required key like
  `serviceName` is missing).
- Never let the library's own build/test pipeline depend on itself in a
  way that can't be tested standalone — the library needs to be verifiable
  without needing a full consumer repo to exercise it.
- Coordinate the migration from per-repo Jenkinsfiles to the shared library
  incrementally by repo, keeping the old per-repo pipeline working until
  the migrated version is verified, rather than a big-bang cutover across
  all repos at once.

## Common pitfalls

- **Symptom:** A shared library change breaks every consumer pipeline
  simultaneously the moment it's merged to `main`.
  **Fix:** Consumers should pin `@Library('shared-lib@v1.4.0')` to an
  explicit tag, not `@Library('shared-lib')` implicit-default or `@main` —
  a tagged version isolates consumers from in-progress library changes
  until they explicitly bump the pin.

- **Symptom:** Adding a new required parameter to `standardPipeline(...)`
  causes dozens of consumer Jenkinsfiles to fail with a null-pointer-style
  Groovy error on their next build.
  **Fix:** Make new parameters optional with a sensible default
  (`config.newThing ?: 'default'`) for a minor version; reserve breaking,
  required-parameter changes for a major version bump with an explicit
  migration announcement and grace period.

- **Symptom:** `NotSerializableException` thrown from a `src/` class used
  inside a pipeline step.
  **Fix:** Classes used inside Pipeline's CPS execution (anything invoked
  from `vars/` in the pipeline's execution context, e.g. objects held
  across a `stage`) must `implement Serializable`; keep such classes free
  of non-serializable fields (open file handles, threads) or mark them
  `transient`.

- **Symptom:** A `vars/*.groovy` function works when tested by one team but
  throws "Scripts not permitted to use ..." for another team's pipeline.
  **Fix:** This is the Groovy sandbox blocking a method/class not on the
  approved list — see
  [jenkins-groovy-scripting-best-practices](../jenkins-groovy-scripting-best-practices/SKILL.md)
  for the script-approval workflow; don't work around it by disabling the
  sandbox globally.

- **Symptom:** A repo owner wants to delete an old shared-library
  credential or an old library version, unaware three other teams'
  Jenkinsfiles still pin that exact version/credential ID.
  **Fix:** Before deleting a Jenkins credential or an old library tag,
  search consumer Jenkinsfiles (`grep -r "@Library('shared-lib@v1" .` across
  known consumer repos, or check the credential's "Used by" list if the
  Credentials plugin exposes it) for references — deleting a
  still-referenced credential or tag breaks every pipeline pinned to it
  with no warning until the next build.

## Worked example

**Scenario:** An organization has 30 Node.js service repos, each with a
near-identical Jenkinsfile. They centralize into a shared library so each
repo's Jenkinsfile becomes ~10 lines, and a future change (e.g. adding a
dependency-scan stage) needs only one PR in the library repo plus a
version bump per consumer.

Library repo layout (`jenkins-shared-library`):
```
vars/nodeServicePipeline.groovy
vars/nodeServicePipeline.txt
src/org/example/pipeline/Notifier.groovy
```

`vars/nodeServicePipeline.groovy`:
```groovy
def call(Map config = [:]) {
    if (!config.serviceName) {
        error "nodeServicePipeline: 'serviceName' is required"
    }
    pipeline {
        agent { docker { image config.nodeImage ?: 'node:20.11-bullseye' } }
        options { timeout(time: 20, unit: 'MINUTES') }
        stages {
            stage('Install & Test') {
                steps {
                    sh 'npm ci'
                    sh 'npm test'
                }
            }
            stage('Deploy') {
                when { branch 'main' }
                steps {
                    sh "make deploy SERVICE=${config.serviceName} TARGET=staging"
                }
            }
        }
        post {
            failure {
                script { org.example.pipeline.Notifier.notifyFailure(this, config.serviceName) }
            }
        }
    }
}
```

Consuming repo's Jenkinsfile (identical pattern across all 30 repos, only
`serviceName` differs):
```groovy
@Library('shared-lib@v1.2.0') _

nodeServicePipeline(serviceName: 'checkout-api')
```

Adding a dependency-scan stage later means one PR to
`vars/nodeServicePipeline.groovy`, tagging `v1.3.0`, and each consumer repo
bumping `@Library('shared-lib@v1.2.0')` → `@Library('shared-lib@v1.3.0')`
on its own schedule instead of 30 separate Jenkinsfile edits.

## Cross-references

- [jenkins-declarative-pipeline-per-repo](../jenkins-declarative-pipeline-per-repo/SKILL.md) — the thin consumer-side Jenkinsfile pattern this library is called from.
- [jenkins-groovy-scripting-best-practices](../jenkins-groovy-scripting-best-practices/SKILL.md) — sandbox approvals, `Serializable` requirements, and unit-testing `vars/`/`src/` code.
- [github-actions-centralized-reusable-workflows](../github-actions-centralized-reusable-workflows/SKILL.md) — the equivalent centralization pattern on GitHub Actions.
- [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md) — designing the security gates a shared library's stages should enforce consistently across all consumers.
