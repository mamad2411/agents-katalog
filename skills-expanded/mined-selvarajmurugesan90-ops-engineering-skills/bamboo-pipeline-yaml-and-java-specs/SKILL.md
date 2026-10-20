---
name: bamboo-pipeline-yaml-and-java-specs
description: >
  Authors Atlassian Bamboo pipeline definitions using either Bamboo Specs
  (Java DSL, compiled and run to create/update a plan) or Bamboo's YAML
  specs format, covering plan/job/stage structure and how a Specs
  definition links to and updates a live Bamboo plan. Use when the user
  asks to "write a Bamboo Specs plan," "convert our Bamboo plan to code,"
  "add a stage/job to a Bamboo build," "use Bamboo YAML specs," or
  "troubleshoot a Bamboo Specs plan not updating the linked plan."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cicd-tooling
  maturity: stable
---

# Bamboo Pipeline YAML and Java Specs

## Purpose

Atlassian Bamboo predates most "pipeline as code" conventions and
historically configured plans through its web UI. **Bamboo Specs** bring
plans under version control two ways: a **Java DSL** (compiled and run as
a small program that calls the Bamboo REST API to create/update a plan) or
Bamboo's newer **YAML specs** format (a declarative file read directly
from the repo, closer to GitHub Actions/GitLab CI in spirit). This skill
covers both, plus Bamboo's plan → job → stage → task hierarchy (distinct
from GitHub Actions' workflow → job → step or GitLab's stage → job model)
and the mechanics of linking a Specs definition to a live Bamboo plan so
changes actually take effect.

## When to use

- A team currently configures Bamboo plans by hand through the UI and
  wants them version-controlled and code-reviewed instead.
- Writing or debugging a Bamboo Specs Java class that isn't correctly
  creating/updating the target plan.
- Choosing between the Java DSL and YAML specs format for a new Bamboo
  project.
- A plan/job/stage structure needs redesigning (e.g. splitting a
  monolithic job into parallel jobs within a stage).
- Migrating from a UI-configured Bamboo plan to a Specs-managed one
  without losing build history or breaking existing triggers.

## Prerequisites & environment

- A Bamboo Server or Data Center instance (Bamboo Specs and YAML specs
  both require Bamboo 6.x+; check the specific Bamboo version's
  documentation for exact Java Specs library compatibility, since
  Atlassian versions the `atlassian-bamboo-specs` artifact alongside
  Bamboo server releases and mismatches cause API-shape errors).
- For Java Specs: a JVM (Java 11+ typically) and Maven/Gradle to compile
  and run the Specs program; the `atlassian-bamboo-specs` dependency
  matching the target Bamboo server's version.
- For YAML specs: Bamboo Data Center with YAML specs enabled for the
  project, and a `bamboo-specs/` (or configured path) directory in the
  repo containing the `.yaml` files.
- A Bamboo user/service account with permission to create/edit plans in
  the target project, and its credentials configured wherever the Specs
  runner executes (CI job, or a "Bamboo Specs" repository trigger).
- An existing Bamboo project to house the plan (Specs create/update plans
  within a project; they don't create a project from scratch by default).

## Step-by-step guidance

1. **Decide Java DSL vs. YAML specs.** Java DSL gives full programmatic
   control (loops, shared builder functions across many plans, real unit
   testing of the Specs code itself) at the cost of a compile step and
   more boilerplate; YAML specs is declarative, easier to review in a PR
   diff, and closer to what teams coming from GitHub Actions/GitLab expect,
   but less expressive for highly dynamic plan generation. Use Java DSL
   when one team maintains dozens of structurally-similar plans
   programmatically; use YAML specs for a single project's plan that a
   broader team needs to read/edit without Java tooling.

2. **Model the plan/job/stage/task hierarchy explicitly.** Bamboo's
   structure, top to bottom: **Plan** (the overall pipeline) → **Stage**
   (sequential; stages run one after another) → **Job** (parallel within
   a stage; jobs in the same stage run concurrently on available agents)
   → **Task** (an individual step within a job, e.g. "Source Code
   Checkout", "Script", "JUnit Parser").

3. **Write a Java Specs plan.** A minimal plan with a build stage
   (parallel test jobs) and a deploy stage:
   ```java
   package com.example.bamboo;

   import com.atlassian.bamboo.specs.api.BambooSpec;
   import com.atlassian.bamboo.specs.api.builders.plan.Plan;
   import com.atlassian.bamboo.specs.api.builders.plan.Stage;
   import com.atlassian.bamboo.specs.api.builders.plan.Job;
   import com.atlassian.bamboo.specs.api.builders.project.Project;
   import com.atlassian.bamboo.specs.api.builders.task.ScriptTask;
   import com.atlassian.bamboo.specs.api.builders.task.CheckoutItem;
   import com.atlassian.bamboo.specs.api.builders.task.VcsCheckoutTask;
   import com.atlassian.bamboo.specs.util.BambooServer;

   @BambooSpec
   public class CheckoutApiPlanSpec {

       Plan plan() {
           return new Plan(
                   new Project().key("CHK").name("Checkout Services"),
                   "Checkout API", "CHKAPI")
               .stages(
                   new Stage("Build & Test")
                       .jobs(
                           new Job("Unit Tests", "UNIT")
                               .tasks(
                                   new VcsCheckoutTask()
                                       .checkoutItems(new CheckoutItem().defaultRepository()),
                                   new ScriptTask().inlineBody("npm ci && npm test")
                               ),
                           new Job("Lint", "LINT")
                               .tasks(
                                   new VcsCheckoutTask()
                                       .checkoutItems(new CheckoutItem().defaultRepository()),
                                   new ScriptTask().inlineBody("npm ci && npm run lint")
                               )
                       ),
                   new Stage("Deploy to Staging")
                       .jobs(
                           new Job("Deploy", "DEPLOY")
                               .tasks(
                                   new ScriptTask().inlineBody("./deploy.sh staging")
                               )
                       )
               );
       }

       public static void main(String[] args) {
           BambooServer bambooServer = new BambooServer("https://bamboo.example.com");
           bambooServer.publish(new CheckoutApiPlanSpec().plan());
       }
   }
   ```
   Running `main` (e.g. `mvn compile exec:java`) calls the Bamboo REST API
   to create or update the `CHK-CHKAPI` plan to match this definition —
   note that stages run **sequentially** ("Build & Test" completes before
   "Deploy to Staging" starts) while the two jobs within "Build & Test"
   run **in parallel**.

4. **Or write the equivalent as Bamboo YAML specs**, committed as
   `bamboo-specs/plan.yaml` in the repo (Bamboo Data Center reads this
   directly, no compile step):
   ```yaml
   version: 2
   plan:
     project-key: CHK
     key: CHKAPI
     name: Checkout API
   stages:
     - Build & Test:
         jobs:
           - Unit Tests
           - Lint
     - Deploy to Staging:
         jobs:
           - Deploy
   Unit Tests:
     tasks:
       - checkout:
           force-clean-build: false
       - script:
           - npm ci
           - npm test
   Lint:
     tasks:
       - checkout:
           force-clean-build: false
       - script:
           - npm ci
           - npm run lint
   Deploy:
     tasks:
       - script:
           - ./deploy.sh staging
   repositories:
     - checkout-api-repo
   ```

5. **Link the Specs definition to the live plan.** For Java DSL, this
   linkage happens the first time `bambooServer.publish(plan())` runs
   successfully against a plan key that doesn't yet exist (it creates the
   plan) or does exist (it updates it to match). For YAML specs, add a
   **"Bamboo Specs" repository trigger** on the project (or a dedicated
   "specs" plan) pointed at the repo/path containing `bamboo-specs/*.yaml`
   — Bamboo then re-syncs the target plan automatically on each push that
   changes the specs file.

6. **Verify the linkage, don't assume it worked.** After publishing/
   syncing, open the plan in the Bamboo UI and confirm the stage/job/task
   structure matches the Specs source — a Specs run that throws a
   permission or validation error partway through can leave the live plan
   in a partially-updated state.

7. **Keep secrets in Bamboo's own variable/credential store**
   (project- or plan-level variables marked as passwords), referenced by
   name in Specs/YAML (`${bamboo.deploy_token}`), never inlined in the
   Java or YAML source.

## Best practices

- Treat the Specs repo (or the specs directory within the app repo) as
  the source of truth; disable manual UI edits to a Specs-managed plan
  where possible (Bamboo shows a banner on Specs-managed plans) so
  drift between the UI and the Specs source doesn't silently occur.
- Use consistent, short project/plan keys (`CHK`/`CHKAPI`) chosen once —
  Bamboo keys are effectively permanent identifiers baked into build
  numbers, artifact URLs, and REST API paths.
- Prefer parallel **jobs within a stage** for independent work (lint,
  unit tests, security scan) and sequential **stages** only where a real
  dependency exists (build before deploy) — this is the direct Bamboo
  analog of the vendor-neutral parallelization guidance in
  [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md).
- For Java Specs maintaining many structurally similar plans, factor
  shared builder logic into a common Java method/class rather than
  copy-pasting the `Plan`/`Stage`/`Job` construction across each plan's
  Spec class.
- Run the Specs publish step itself from a CI job (a Bamboo plan, or even
  a GitHub Actions/Jenkins job) rather than a developer's laptop, so plan
  changes go through the same review/audit trail as code changes.
- Use manual stages (`.manual()` in Java Specs, or the equivalent
  approval configuration in YAML) for production deploy stages so a human
  gate exists before the "Deploy to Production" stage runs, mirroring the
  manual-approval-gate guidance in
  [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md).

## Common pitfalls

- **Symptom:** Running the Java Specs `main` method throws an
  authentication/permission error and the plan is left half-created (some
  stages present, others missing).
  **Fix:** Verify the service account used by `BambooServer` has "Create
  Plan"/"Edit Plan" permission on the target project *before* running
  publish, and re-run the full publish after fixing permissions — a
  partial publish is not automatically rolled back, so always open the
  plan in the UI afterward to confirm it matches the Specs source.

- **Symptom:** Two jobs in the same stage that are supposed to run one
  after another (e.g. "build" then "package" using the build's artifact)
  instead run concurrently and "package" fails because the artifact isn't
  ready.
  **Fix:** Jobs within one Bamboo stage always run in parallel by design;
  a genuine sequential dependency between two units of work needs to be
  two separate **stages**, not two jobs in the same stage.

- **Symptom:** YAML specs changes pushed to the repo don't appear to
  update the live plan at all.
  **Fix:** Confirm the project has a **Bamboo Specs repository trigger**
  configured and pointed at the correct path containing the YAML files —
  without that trigger (or a manually-run specs sync), pushing YAML
  changes to the repo does nothing on its own; YAML specs are not
  auto-discovered without this explicit linkage.

- **Symptom:** A plan's build number/history appears to reset or a new
  duplicate plan gets created instead of updating the existing one.
  **Fix:** This happens when the Specs project/plan key doesn't exactly
  match the existing plan's key — publishing with a new key creates a new
  plan rather than updating the old one; double check `project-key`/`key`
  (YAML) or `.key(...)` calls (Java) match the live plan exactly before
  publishing.

- **Symptom:** A teammate edits the plan directly in the Bamboo UI "just
  this once," and the next Specs publish silently reverts their change.
  **Fix:** Once a plan is Specs-managed, all changes should go through the
  Specs source and a normal publish/sync — treat a direct UI edit on a
  Specs-managed plan as a bug to fix in the Specs source, not a
  legitimate parallel path, and communicate this to the team explicitly.

## Worked example

**Scenario:** A team migrates a UI-configured Bamboo plan for a Java
service to YAML specs, adding a manual-gated production deploy stage
after the existing staging deploy.

`bamboo-specs/plan.yaml`:
```yaml
version: 2
plan:
  project-key: PAY
  key: PAYSVC
  name: Payment Service
stages:
  - Build & Test:
      jobs:
        - Build
        - Unit Tests
  - Deploy Staging:
      jobs:
        - Deploy Staging Job
  - Deploy Production:
      manual: true
      jobs:
        - Deploy Production Job
Build:
  tasks:
    - checkout:
        force-clean-build: false
    - script:
        - mvn -B compile
Unit Tests:
  tasks:
    - checkout:
        force-clean-build: false
    - script:
        - mvn -B test
    - test-parser:
        type: junit
        test-results: "**/target/surefire-reports/*.xml"
Deploy Staging Job:
  tasks:
    - script:
        - ./deploy.sh staging
Deploy Production Job:
  tasks:
    - script:
        - ./deploy.sh production
repositories:
  - payment-service-repo
```
With `manual: true` on "Deploy Production", the stage waits for a user
with plan permission to click "Run" in the Bamboo UI, giving the same
release gate as the manual-approval pattern in
[ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md),
expressed in Bamboo's own stage-level construct.

## Cross-references

- [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md) — vendor-neutral stage/gate design this Bamboo plan structure implements.
- [jenkins-centralized-shared-library](../jenkins-centralized-shared-library/SKILL.md) — a comparable "logic centralized, consumers thin" pattern on a different CI platform, useful when migrating between the two.
- [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md) — designing the severity/blocking policy for any scan tasks added into this plan.
