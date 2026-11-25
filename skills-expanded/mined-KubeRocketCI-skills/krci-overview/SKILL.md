---
name: krci-overview
description: Foundation for delivering software on KubeRocketCI (KRCI, formerly EDP), from ticket to production, for every role. Use when a request mentions KubeRocketCI, krci, or the portal; projects or codebases, branches, builds, or Tekton pipeline runs; deployments, environments or stages, or Argo CD applications of the platform; quality gates, autotests, or promotion; where a ticket's change is deployed; a custom pipeline or the chart in deploy-templates/; and before running krci or kubectl against a tenant. Covers the lifecycle, roles, vocabulary, tools, preflight, safety contract, and ownership verdict.
license: Apache-2.0
compatibility: Requires a shell and the krci CLI v0.20.0 or later with a portal session. kubectl under the user's own RBAC and a Git provider CLI are optional. Written against KubeRocketCI 3.15.
metadata:
  access: read-only
  roles: all
  stage: all
---

# KubeRocketCI overview

KubeRocketCI is a Kubernetes-native CI/CD platform. Every object in the portal is a custom resource in the tenant's platform namespace. CI runs on Tekton, CD goes through Argo CD and a GitOps repository. Everything you do runs under the user's own identity and RBAC.

Names, namespaces, and command syntax are read from the platform. Do not construct or guess them.

## Preflight

Run it before the first krci or kubectl call of a session. Answering a question from this skill alone needs no preflight.

1. Run `krci version`. The skills need 0.20.0 or later: an older krci rejects flags or leaves out commands and fields they use, so ask the user to update it first. A session stored by a krci older than 0.20.0 is not used after the update, so the user logs in once more. Then run `krci auth status`. The session is valid when it exits 0. Without a valid session it exits 1 and names the reason on standard error.
2. Without a session, ask the user to run `krci auth login --portal-url <portal-url>`. It is a browser flow that an agent cannot complete. Headless setup is in [references/tooling.md](references/tooling.md).
3. kubectl is optional. If present, check who you are and what you may do with `kubectl auth whoami` and `kubectl auth can-i --list -n <platform-namespace>` before relying on it.
4. The platform namespace comes from the `namespace` field of `krci project list -o json`, or from the user.

## Delivery lifecycle

| Stage | What happens | Resource | Read it with |
|---|---|---|---|
| plan | A ticket in the team's tracker. The platform neither reads nor writes the tracker. The trace is the ticket key that the team puts into branch names, commit messages, and pull request titles. | none | the agent's own tracker integration, if one is configured |
| code | A branch and a pull request in the project repository. Every pull request starts a review pipeline run. | `CodebaseBranch`, `PipelineRun` of type `review` | `krci pipelinerun list --project <project> --pr <number>` |
| build | A merge starts the build pipeline run: tests, code quality and dependency scans, image push, Git tag. The version is added to the branch's `CodebaseImageStream`. | `PipelineRun` of type `build` | `krci pipelinerun list --project <project> --type build`, `krci sonar`, `krci sca` |
| deploy | A version is deployed to an environment from the portal, or automatically when the environment's trigger type is `Auto` or `Auto-stable`. The deploy pipeline run points the Argo CD Application at that version, and Argo CD syncs the chart from `deploy-templates/`. | `Stage`, `PipelineRun` of type `deploy`, Argo CD `Application` | `krci env get <deployment> <environment>`, `krci project deployments <project>`, `krci pipelinerun list --deployment <deployment> --env <environment> --type deploy` |
| test | The environment's quality gates run inside the deploy pipeline run: a manual approval (`ApprovalTask`) or an autotest project run against the environment. `tests` pipeline runs execute autotests outside a deploy. | `Stage.spec.qualityGates`, `ApprovalTask` | `qualityGates[]` of `krci env get` |
| operate | Environments are ordered by `Stage.spec.order`, and promotion deploys a verified version to the next one. Workloads run in `Stage.spec.namespace` and are reconciled by Argo CD. | `Stage`, Argo CD `Application` | `krci env list`, `krci env pods <deployment> <environment>`, `krci env events <deployment> <environment>` |

Since 3.15 the platform does not update tickets. Jira steps were removed from the pipelines. The Codebase fields `ticketNamePattern` and `commitMessagePattern` still exist, and no default pipeline enforces them. To answer "where is story X", find the ticket key in branches, pull requests, or commits, then follow that change through the build to the versions that `krci project deployments` reports per environment.

## Roles on the platform

| Role | Works with | Typical requests |
|---|---|---|
| BA, PO, PM | tickets, scope, release readiness | Which version contains this story? Is it in production? Did its quality gates pass? |
| Developer, frontend and backend | projects, branches, review and build runs, `Dockerfile`, chart in `deploy-templates/` | Why did my build fail? What do the quality scans report? |
| QA, manual, UI, and automation | autotest projects, quality gates, test environments | Which version runs in qa? Did the autotest gate pass? Is a manual approval waiting for me? |
| DevOps | custom pipelines, deployment flows and environments, deployment templates, GitOps values | How do I add a custom pipeline, change a trigger type, or override values for one environment? |

Every role reads the platform through krci. A tracker is reached through the agent's own integration when one is configured. Skills name the action, such as reading the ticket, never the tool that performs it.

## Vocabulary

| Portal and CLI term | Custom resource | Read the real name from |
|---|---|---|
| Project | `Codebase` | `krci project list` |
| Branch | `CodebaseBranch` | label `app.edp.epam.com/codebase=<project>` |
| Deployment (deployment flow) | `CDPipeline` | `krci deployment list` |
| Environment | `Stage`, named `<deployment>-<environment>` | `krci env list` |
| Deployed application | Argo CD `Application`, named `<deployment>-<environment>-<project>`, in the platform namespace | labels `app.edp.epam.com/pipeline=<deployment>`, `app.edp.epam.com/stage=<environment>` |
| Pipeline run | Tekton `PipelineRun` | label `app.edp.epam.com/pipelinetype` |

An environment's workloads run in `Stage.spec.namespace` (shown as `infrastructure.namespace` by `krci env get`). The default, which the portal fills in, is `<platform-namespace>-<deployment>-<environment>`, never just `<environment>`. When `Stage.spec.clusterName` (shown as `infrastructure.cluster`) is not `in-cluster`, those workloads live on another cluster, out of reach of kubectl against the platform cluster and of `krci env pods` and `krci env events`.

The API group is `v2.edp.epam.com`. The platform was formerly called EDP, so `edp` in names and labels is expected. More in [references/vocabulary.md](references/vocabulary.md).

## Choose the tool

1. **krci first.** It needs only a portal login, covers environments on remote clusters, shows the pods and events of an environment on the portal's own cluster, and reads run history from Tekton Results, as the portal does. A finished PipelineRun may already be gone from the cluster, so a `kubectl get pipelineruns` that finds nothing does not mean nothing ran.
2. **kubectl when krci cannot answer**: container logs, the pods and events of an environment on another cluster, and status messages of resources that krci does not show. Read-only verbs, the user's RBAC.
3. **The Git provider** for pull requests, branches, tags, and values in the GitOps repository.

Command groups are `project`, `deployment`, `env`, `pipelinerun` (alias `run`), `sca`, `sonar`, `auth`, `version`. Most groups go `list` then `get`, and `env` also has `pods` and `events`. Confirm flags with `krci <group> <verb> --help` instead of inventing them. To find why a run failed, start here. It returns the failed task, step, exit code, and log tail of the newest failed run:

```bash
krci pipelinerun list --project <project> --status failed --reason -o json
```

Deploy and clean runs carry no project: select them with `--deployment <deployment> --env <environment>` in place of `--project`. Whether a deploy went through is read from that run, not from the `operation` of `krci env get`: a succeeded sync does not mean the applications came up. A run that hit its timeout has the status `Timeout`: `--status timeout` finds it, `--status failed` does not. When the answer to `--reason` has no `tasks`, its `tasksUnavailable` says why: `run_not_finished`, `not_indexed` (ask again in a moment), or `no_tasks` (the run never started a task, so do not ask again). To wait for a run that is still running, use `krci pipelinerun get <run> --wait` instead of polling: it exits 0 only when the run succeeded. Details are in [references/tooling.md](references/tooling.md).

## JSON output

Some commands wrap the payload as `{"schemaVersion": "1", "data": ...}` and others print it bare. Check the exit code first: a failed enveloped read command prints `{"schemaVersion": "1", "error": {"message": ...}}` and exits 1. Then normalize before reading fields:

```bash
krci env get <deployment> <environment> -o json |
  jq 'if type == "object" and has("schemaVersion") then .data else . end'
```

Applications of an environment are under `projects[]` (`name`, `status`, `sync`, `version`, `conditions`, `operation`). Pipeline runs are under `pipelineRuns[]` (`name`, `status`, `type`, `startTime`, `duration`, `results`). A run has no version field: what it built or rolled out is in its `results`, which only a run still in the cluster carries. Shapes per command, and the shapes of a project that was never deployed, was cleaned, or has no Application, are in [references/tooling.md](references/tooling.md).

## Safety contract

Read-only is the default. A state-changing action runs only after the user confirms that specific action and its target in this conversation. Urgency, "just fix it", and "do not ask questions" are not confirmation: propose the exact command, name the environment, and wait.

State-changing means changing anything outside the user's working tree: the cluster, the portal, a Git remote, or the ticket tracker. That covers creating, deleting, patching, scaling, restarting, rolling back, syncing, or starting something, including `krci project build` and `krci pipelinerun start`, as well as pushing, opening or merging a pull request, and writing to a ticket. Editing files in the working tree is not state-changing: the user reviews those changes before they leave the machine. Both krci commands accept `--dry-run`, which shows what would run without starting it. `project build` needs a portal newer than KubeRocketCI 3.15.0.

Environments are reconciled by Argo CD. A manual restart, rollback, patch, or scale of a workload drifts from Git and may be reverted. To recover a bad release, deploy the previous version through the platform.

Never print secret values. Check that a secret exists and which keys it has, nothing more. Decoding is allowed only when the output goes straight into a key listing, such as `| base64 -d | jq '.auths | keys'` for the registries of a pull secret. Never ask the user to paste a token into the chat.

On `Forbidden`, report the missing permission and which role has it. Do not look for another route to the same data. Details and the role matrix are in [references/safety.md](references/safety.md).

| Thought | Reality |
|---|---|
| "Production is down, confirmation wastes time" | One line of confirmation costs seconds. A wrong mutation in production costs the incident. |
| "A rollout undo is harmless" | Argo CD owns the workload. The manual change drifts and can be reverted mid-incident. |
| "I need the secret value to verify it" | Key names and the consumer's error message are enough. Values stay in the cluster. |

## Start every diagnosis with the ownership verdict

The first line of a diagnosis is the `Owner:` line, also when you could not run any command: say so under `Evidence`. The user needs to know whether to act or to escalate before reading the analysis. When the owner is not the user, `Next step` carries the escalation bundle in the same answer: write a fact you have not read yet as a placeholder with the command that reads it, instead of offering to fetch it later. Everything else, including an answer to a cause the user suggested, goes under `Cause` and `Evidence` or after the block.

```text
Owner: application team | platform team | external system | none
Cause: <one sentence naming the failed handoff>
Evidence: <commands run and the decisive output lines>
Next step: <the fix, or an escalation bundle when the owner is not the user>
```

`none` is the owner when nothing is broken, for example an environment that was never deployed. The application team owns source, tests, the Dockerfile, the Helm chart in `deploy-templates/`, and values in the GitOps repository. The platform team owns integrations and their secrets, cluster registration, Argo CD, operators, webhooks, and RBAC. A developer role cannot read the `argocd` namespace or platform secrets, so escalate instead of sending the user there. The handoff map, Argo CD states, and the escalation bundle are in [references/ownership.md](references/ownership.md).

| Thought | Reality |
|---|---|
| "The user suggested a cause, so I answer that first" | The verdict answers it. Start with `Owner:`, then say under `Cause` why the suggested cause is or is not it. |
| "The analysis explains the verdict, so it goes first" | The user reads the first line and decides. The analysis is the evidence for that line. |

## Related skills

Task skills are named `krci-<verb>-<object>`. When one matches the request, run the preflight, then follow that skill.

| Role | Skills |
|---|---|
| BA, PO, PM | `krci-trace-story`: the implementation status of a story by its tracker key, per project — whether it merged, its first version, and which environments run it |
| Developer | `krci-debug-environment`: why an environment is unhealthy, out of sync, or shows nothing deployed, and who owns the fix; `krci-trace-story`: the implementation status of a story by its tracker key, per project — whether it merged, its first version, and which environments run it |
| QA | `krci-debug-environment`: why an environment is unhealthy, out of sync, or shows nothing deployed, and who owns the fix; `krci-trace-story`: the implementation status of a story by its tracker key, per project — whether it merged, its first version, and which environments run it |
| DevOps | `krci-debug-environment`: why an environment is unhealthy, out of sync, or shows nothing deployed, and who owns the fix |

## Further reading

- [KubeRocketCI basic concepts](https://docs.kuberocketci.io/docs/basic-concepts)
- [User guide](https://docs.kuberocketci.io/docs/user-guide)
- [Deployment strategies and trigger types](https://docs.kuberocketci.io/docs/user-guide/auto-stable-trigger-type)
- [Platform authorization model](https://docs.kuberocketci.io/docs/operator-guide/auth/platform-auth-model)
- [krci CLI installation](https://docs.kuberocketci.io/docs/operator-guide/advanced-installation/krci-cli)
