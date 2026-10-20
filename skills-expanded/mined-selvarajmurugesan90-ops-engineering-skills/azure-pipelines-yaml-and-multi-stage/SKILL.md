---
name: azure-pipelines-yaml-and-multi-stage
description: >
  Designs Azure Pipelines YAML (azure-pipelines.yml), multi-stage
  pipelines with environments/approvals, templates for reuse across
  repos, and self-hosted vs. Microsoft-hosted agent pools. Use when the
  user asks to "set up Azure Pipelines," "write an azure-pipelines.yml,"
  "add a multi-stage pipeline with approvals," "create a reusable
  pipeline template," "configure a self-hosted agent pool," or
  "troubleshoot a stuck/failed Azure DevOps pipeline run."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cicd-tooling
  maturity: stable
---

# Azure Pipelines YAML and Multi-Stage Design

## Purpose

Azure Pipelines (part of Azure DevOps) runs pipelines defined in
`azure-pipelines.yml` as a sequence of **stages**, each containing
**jobs**, each containing **steps** — with **environments** providing
approval gates and deployment history between stages, and **templates**
providing the reuse mechanism equivalent to GitHub Actions' reusable
workflows or GitLab's `include:`. This skill covers Azure Pipelines'
specific YAML schema, environment/approval mechanics, and template reuse
— not the generic pipeline-design concepts covered in
[ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md),
which apply here too but aren't repeated.

## When to use

- Standing up a new pipeline for a repo hosted in Azure Repos, GitHub, or
  Bitbucket that needs to build/test/deploy through Azure DevOps.
- Designing a multi-stage pipeline (e.g. Build → Dev → Staging →
  Production) with approval gates and deployment history tracked per
  **environment**.
- Extracting a shared pipeline template so multiple repos consume one
  canonical build/deploy definition instead of copy-pasting YAML.
- Choosing between Microsoft-hosted agents (fast to start, ephemeral, cost
  per minute) and self-hosted agent pools (persistent, custom tooling,
  network access to private resources).
- Diagnosing a pipeline run stuck at a specific stage/job, a template
  parameter not resolving as expected, or an approval gate that isn't
  notifying the right approvers.

## Prerequisites & environment

- An Azure DevOps organization and project, with a service connection
  configured for any external target (Azure subscription, Kubernetes
  cluster, container registry) the pipeline deploys to.
- Pipeline permissions: the pipeline's identity (or the service connection
  it uses) needs least-privilege access to only the resources it deploys
  to — not subscription-Owner-level access "to make it work."
- For self-hosted agents: a registered agent pool with agents that have
  network access to any private resources (internal artifact feeds,
  on-prem systems) the Microsoft-hosted pool can't reach.
- **Environments** (`Pipelines → Environments`) created ahead of time if
  you want approval gates and deployment history — a stage's
  `deployment` job references an environment by name, and the
  environment must exist (and have its approval checks configured) before
  the first run.

## Step-by-step guidance

1. **Structure the pipeline as stages of jobs**, mirroring how
   CodePipeline models stages of actions and GitHub Actions models a
   workflow's jobs:
   ```yaml
   # azure-pipelines.yml
   trigger:
     branches:
       include: [main]

   pool:
     vmImage: ubuntu-latest

   stages:
     - stage: Build
       jobs:
         - job: BuildAndTest
           steps:
             - script: npm ci && npm test
               displayName: "Install and test"
             - script: npm run build
               displayName: "Build"
             - publish: dist
               artifact: app-dist

     - stage: DeployStaging
       dependsOn: Build
       jobs:
         - deployment: DeployToStaging
           environment: "checkout-api-staging"
           strategy:
             runOnce:
               deploy:
                 steps:
                   - download: current
                     artifact: app-dist
                   - script: ./deploy.sh staging
                     displayName: "Deploy to staging"

     - stage: DeployProduction
       dependsOn: DeployStaging
       jobs:
         - deployment: DeployToProduction
           environment: "checkout-api-production"
           strategy:
             runOnce:
               deploy:
                 steps:
                   - download: current
                     artifact: app-dist
                   - script: ./deploy.sh production
                     displayName: "Deploy to production"
   ```
   The `deployment` job type (vs. a plain `job`) is what unlocks
   environment-linked approval gates and deployment history — a plain
   `job` deploying via script has neither.

2. **Configure the approval gate on the environment itself**, not in the
   YAML — in Azure DevOps, go to `Pipelines → Environments →
   checkout-api-production → Approvals and checks`, add the required
   approvers. This is Azure Pipelines' equivalent of a GitHub Actions
   protected `environment:` reviewer list or a GitLab `when: manual` job;
   the YAML only references the environment name, the gate configuration
   lives on the environment resource.

3. **Extract shared logic into a template** once two or more pipelines
   duplicate the same stage/job/steps:
   ```yaml
   # templates/build-and-test.yml
   parameters:
     - name: nodeVersion
       type: string
       default: "20.x"

   steps:
     - task: NodeTool@0
       inputs:
         versionSpec: ${{ parameters.nodeVersion }}
     - script: npm ci && npm test
   ```
   ```yaml
   # consuming pipeline
   steps:
     - template: templates/build-and-test.yml
       parameters:
         nodeVersion: "18.x"
   ```
   Templates can live in the same repo or a separate shared repo
   referenced via a `resources.repositories` block, mirroring
   [github-actions-centralized-reusable-workflows](../github-actions-centralized-reusable-workflows/SKILL.md)'s
   centralized-repo pattern.

4. **Pin template and task versions explicitly** in a shared/centralized
   setup — `resources.repositories` supports a `ref` (branch/tag), and
   marketplace tasks are versioned (`NodeTool@0`); an unpinned `ref: main`
   on a shared templates repo means every consumer's next run picks up
   whatever the templates repo's `main` branch currently contains,
   silently, with no PR to review.

5. **Choose Microsoft-hosted vs. self-hosted agents deliberately**:
   Microsoft-hosted (`pool: vmImage: ubuntu-latest`) requires no
   maintenance and starts fresh every run, but can't reach private
   network resources and has a per-minute cost past the free tier;
   self-hosted (`pool: name: my-agent-pool`) has persistent state (faster
   for large dependency caches) and network access to internal systems,
   but the org is responsible for patching and securing the agent host
   itself.

6. **Diagnose a stuck or failed run** by opening the specific stage/job's
   log, not just the pipeline summary — a `deployment` job's approval
   step shows as "Waiting" until approved/rejected (check the
   environment's pending approvals), and a failed step's raw log
   (`##[error]` lines) has the actual command/exit-code detail the
   pipeline-level red/green status doesn't surface.

## Best practices

- Use `deployment` jobs with named **environments** for anything that
  should have an approval gate and a deployment history — a plain `job`
  running a deploy script has neither, and there's no audit trail of
  who deployed what, when.
- Keep environment approval lists current as team membership changes; an
  approval gate whose only approver left the team blocks every future
  deployment until someone notices and fixes the check.
- Pin `resources.repositories` template refs to a tag or commit for
  production-facing pipelines, not a floating branch — see the pitfall
  below.
- Prefer parameterized templates over YAML anchors/copy-paste for shared
  logic — a template's `parameters` block is validated and documented,
  where copy-pasted YAML across pipelines silently drifts.
- Scope service connections narrowly (one per target environment/
  subscription, least-privilege role) rather than one broad connection
  reused across dev/staging/production — a compromised or misconfigured
  pipeline run should not be able to reach production through a
  connection meant for dev.

## Common pitfalls

- **Symptom:** A shared templates repo's `main` branch changes, and every
  consuming pipeline's next run silently behaves differently — no PR, no
  changelog, just a different result.
  **Fix:** Pin `resources.repositories.ref` to a specific tag or commit
  SHA for anything production-facing; treat the templates repo like any
  other versioned dependency, not a live-editable shared file.

- **Symptom:** A `deployment` job's approval step sits in "Waiting"
  indefinitely and nobody notices until someone asks why the release
  hasn't gone out.
  **Fix:** Configure the environment's approval notification (email/
  Teams/Slack via a service hook) so pending approvals are actively
  surfaced, not just visible if someone happens to check the
  Environments page.

- **Symptom:** A pipeline works fine on Microsoft-hosted agents in dev but
  fails to reach an internal artifact feed or database in staging/
  production.
  **Fix:** That target requires self-hosted agents with network access
  to the private resource — Microsoft-hosted agents run in Azure's shared
  pool with no route to on-prem or VPC-internal systems unless exposed
  publicly (which is its own security tradeoff to weigh deliberately).

- **Symptom:** A service connection was granted subscription-level
  Contributor/Owner "so the pipeline could deploy anything," and a bug in
  one pipeline's YAML deletes or modifies resources far outside what that
  pipeline should touch.
  **Fix:** Scope service connections to a specific resource group (or
  narrower) with only the roles the pipeline's actual deploy steps need —
  treat an overly broad service connection as a security finding.

## Worked example

**Scenario:** `checkout-api` builds once, then deploys through staging
and production with a required approval before production, using named
environments for the audit trail.

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include: [main]

pool:
  vmImage: ubuntu-latest

stages:
  - stage: Build
    jobs:
      - job: BuildAndTest
        steps:
          - template: templates/build-and-test.yml
            parameters:
              nodeVersion: "20.x"
          - publish: dist
            artifact: app-dist

  - stage: DeployStaging
    dependsOn: Build
    jobs:
      - deployment: ToStaging
        environment: "checkout-api-staging"
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: app-dist
                - script: ./deploy.sh staging

  - stage: DeployProduction
    dependsOn: DeployStaging
    jobs:
      - deployment: ToProduction
        environment: "checkout-api-production"   # approval check configured on this environment
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: app-dist
                - script: ./deploy.sh production
```

The `checkout-api-production` environment has an approval check
configured (release manager + on-call lead, either can approve) in
`Pipelines → Environments`, so `DeployProduction` pauses and notifies
both approvers via the configured Teams service hook; the environment's
deployment history then shows exactly which run deployed to production,
when, and who approved it.

## Cross-references

- [ci-cd-pipeline-design](../../../devops/skills/ci-cd-pipeline-design/SKILL.md) — vendor-neutral stage/gate/rollback concepts this pipeline implements in Azure-specific terms.
- [github-actions-centralized-reusable-workflows](../github-actions-centralized-reusable-workflows/SKILL.md) — the closest GitHub Actions equivalent to Azure Pipelines' template-repo reuse pattern.
- [aws-codepipeline-and-codedeploy](../aws-codepipeline-and-codedeploy/SKILL.md) — the closest AWS equivalent, for teams comparing or migrating between the two.
- [secure-cicd-gates](../../../devsecops/skills/secure-cicd-gates/SKILL.md) — where to place scan steps relative to the approval and deployment stages here.
