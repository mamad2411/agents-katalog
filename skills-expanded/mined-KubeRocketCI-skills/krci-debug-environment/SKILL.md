---
name: krci-debug-environment
description: Why an environment is unhealthy, out of sync, or shows nothing deployed, and who owns the fix. Use when an environment or its Argo CD app is Degraded, Unknown, Missing, OutOfSync, or on version NaN, a sync failed, the environment failed to create, or pods crash-loop, stay Pending, or hit ImagePullBackOff. Not for a failed build or review run, or a pending quality gate, which krci-overview routes.
license: Apache-2.0
compatibility: Requires the krci CLI v0.20.0 or later with a portal session. kubectl under the user's own RBAC is optional and needed for container logs and for the pods of an environment on another cluster. Written against KubeRocketCI 3.15.
metadata:
  access: read-only
  roles: dev, qa, devops
  stage: operate
---

# Debug an environment

Settles why the projects of one environment are not running, or not running the version the platform reports, and whose job the fix is. For developers, QA engineers, and DevOps engineers who watch an environment.

Vocabulary, tool tiers, the safety contract, and the ownership verdict come from `krci-overview`. Load it before you answer, also when you run no command: it defines the verdict and the owners it allows. Run its preflight before the first krci or kubectl call.

## Verdict

Start the answer with the ownership verdict from `krci-overview`: the `Owner:` line first, then `Cause`, `Evidence`, and `Next step`. The analysis follows the block.

## Procedure

1. Read the environment with `krci env get <deployment> <environment> -o json`, normalized as `krci-overview` shows. Check the environment's own `status` first: `failed` stops here, classify its `detailedMessage` with the table below. Otherwise read each entry of `projects[]`.
2. Classify each project with "Reading Argo CD Application state" in `krci-overview`'s ownership reference, using `status`, `sync`, `conditions[]`, and `operation` together. A project that runs nothing has one of the shapes in its tooling reference, section "JSON contract". Read `operation` before `version` and `deployedAt`: a `Failed` or `Error` phase means the version did not finish rolling out, and the image of the running pods shows what runs.
3. When a version was deployed, read the last deploy run of the environment with `krci pipelinerun list --deployment <deployment> --env <environment> --type deploy --reason -o json`. Its `startTime` says when the last deploy ran. Its task `deploy-app` is the deploy: it fails when the applications do not come up, while `operation.phase` stays `Succeeded`. A run that is still running has no `tasks[]` yet. `krci-overview`'s tooling reference, section "Deploy history of one environment", explains the other tasks of the run and where its versions are.
4. For `degraded`, or `progressing` past the Deployment's progress deadline, run `krci env pods <deployment> <environment> -o json` and `krci env events <deployment> <environment> --warnings`, then use the table below. `--pod <pod>` narrows the events to one pod. For a restarted container, such as one in `CrashLoopBackOff`, `lastTermination` holds the `reason` and `exitCode` of its previous run. An empty event list does not clear a pod that `env pods` shows failing: events expire. For an environment whose `infrastructure.cluster` is not `in-cluster`, follow `krci-overview`'s rule for remote clusters. The previous container's log is not in krci: read it with `kubectl logs --previous` in `infrastructure.namespace`. Without kubectl, or on `Forbidden` or `permission denied`, put the commands you could not run into the escalation bundle as placeholders for someone with access to the namespace.
5. For `outofsync` on a healthy project, compare with Git before anyone syncs: the Application's page in Argo CD, at the path in `argocdUrl`, shows the diff. With `valuesOverride: true` the values come from `<deployment>/<environment>/<project>-values.yaml` on the `main` branch of the GitOps repository, with `false` that file is not read.
6. When the owner is not the user, build the escalation bundle from `krci-overview`'s ownership reference, naming the target cluster by `infrastructure.cluster`, not by an API server address. Take when it started from `conditions[].lastTransitionTime` and `operation.startedAt`, and the last version that worked from the deploy history in `krci-overview`'s tooling reference, section "Deploy history of one environment".

## Decision table

Rows cover the environment and pod evidence that the ownership reference hands off to this skill.

| Evidence | Cause | Owner and what settles it |
|---|---|---|
| Environment `failed`, `detailedMessage` with `failed to get cluster secret` | The environment's target cluster is not registered | platform team |
| Environment `failed`, `detailedMessage` with `failed to create namespace` or `failed to get regcred secret` | Namespace creation or the registry pull secret | platform team |
| `ErrImagePull` or `ImagePullBackOff` with `401`, `403`, or `unauthorized` | The pull secret `regcred` in the environment namespace is missing or stale. It is copied once when the environment is created, so an existing environment keeps old credentials after a rotation, unless the platform syncs it with External Secrets. | platform team. The same image pulling in another environment settles it. Check only that the secret exists and its age, with `kubectl get secret regcred` in the environment namespace and no output format. After the refresh the pods pull on their next retry, so no restart is needed. |
| `ErrImagePull` or `ImagePullBackOff` with `manifest unknown` or `not found` | The tag is not in the registry | `krci project versions <project>` settles it: a tag it does not list was never built (application team), a listed tag was removed from the registry (platform team) |
| Pull errors with `x509` or `i/o timeout` | The registry is unreachable or untrusted from the cluster | platform team |
| Last state `OOMKilled`, exit code `137` | The container exceeds its own memory limit | application team: limits in the chart or the values file |
| `CrashLoopBackOff` with any other exit code | The process exits | application team. The cause is in `kubectl logs --previous`. |
| `CreateContainerConfigError`, a Secret or ConfigMap not found | A referenced object is missing | whoever owns the reference: the chart or values (application team), an integration secret (platform team) |
| `Readiness probe failed` or `Liveness probe failed` | Probe or configuration | application team |
| `FailedScheduling` with `Insufficient cpu` or `Insufficient memory` | Cluster capacity | platform team, unless the chart requests more than a node has |
| `FailedScheduling` with node selector, affinity, or taint | Placement rules in the chart | application team |
| `FailedScheduling` with `unbound immediate PersistentVolumeClaims` | Storage class or volume provisioning | platform team |
| ReplicaSet `FailedCreate` with `exceeded quota` | Namespace quota | platform team, or application team when the requests are unrealistic |
| ReplicaSet `FailedCreate` with `admission webhook` and `denied` | Cluster policy | platform team for the policy, application team when the message names a chart setting the policy requires |

## Common mistakes

- Blaming a missing Git tag or a failed build for `version: "NaN"`. Nothing was deployed yet: deploy a version from the portal, or wait for the next build when the trigger type is `Auto`.
- Calling an environment empty because its project fields are `null`.
- Waiting for someone with kubectl to read the pods or events of an environment on the portal's cluster. `krci env pods` and `krci env events` read them with the user's portal session.
- Reporting `version` and `deployedAt` as a finished rollout, or `operation.phase` `Succeeded` as a successful deploy.
- Finding deploy runs with `krci pipelinerun list --project <project> --type deploy`. The result is always empty: deploy runs are selected with `--deployment` and `--env`.
- Asking for a hard refresh or a sync when a values override does not apply.
- Adding a pod restart or a rollback to the next step. Pods retry on their own once the cause is fixed, and the safety contract in `krci-overview` covers both.

## Further reading

- [Manage Deployments](https://docs.kuberocketci.io/docs/user-guide/manage-environments)
- [Application and pipeline statuses](https://docs.kuberocketci.io/docs/user-guide/application-and-pipeline-statuses)
- [Argo CD integration](https://docs.kuberocketci.io/docs/operator-guide/cd/argocd-integration)
- [Sync and health status Unknown](https://docs.kuberocketci.io/docs/operator-guide/troubleshooting/sync-health-status-unknown)
- [Container registry errors](https://docs.kuberocketci.io/docs/operator-guide/troubleshooting/container-registry-error)
