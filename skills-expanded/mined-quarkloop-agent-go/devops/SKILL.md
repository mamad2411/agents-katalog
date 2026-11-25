# service-devops

The DevOps service provides selected typed operations for repositories, builds,
tests, containers, deployments, and policy checks. It is not a general command
execution layer.

## Agent Rules

1. Prefer read-only functions before proposing changes.
2. Use `policy_EvaluateChange` before write/admin work when the user request is
   ambiguous or risky.
3. Use the DevOps release functions for release automation:
   `build_DryRunRelease`, `build_InitReleaseConfig`, and `build_RunRelease`.
4. Do not mirror full Git, Docker, Kubernetes, Helm, or Terraform APIs through
   prompts. Select the narrow service function that matches the user request.
5. Treat write/admin functions as plans until approval has been granted and the
   execution result confirms completion.

## Service Functions

- `repo_Status`
- `repo_Diff`
- `repo_GetBranch`
- `repo_ListChangedFiles`
- `repo_ApplyPatch`
- `repo_Commit`
- `repo_GenerateReleaseNotes`
- `build_DetectProject`
- `build_ResolveTask`
- `build_RunTask`
- `build_CreateArtifact`
- `build_InitReleaseConfig`
- `build_DryRunRelease`
- `build_RunRelease`
- `test_DiscoverTests`
- `test_RunTests`
- `test_ExplainFailure`
- `container_BuildImage`
- `container_ListImages`
- `container_PlanRun`
- `deploy_Plan`
- `deploy_Apply`
- `policy_EvaluateChange`

## Approval

`repo_ApplyPatch`, `repo_Commit`, `build_RunTask`, `build_CreateArtifact`,
`build_InitReleaseConfig`, `build_RunRelease`, `test_RunTests`,
`container_BuildImage`, `container_PlanRun`, `deploy_Plan`, and `deploy_Apply`
require approval. Do not describe those actions as completed until the approved
execution result is available.

When an approved `test_RunTests` result fails, use its bounded
`tests[].evidence` lines when calling `test_ExplainFailure`. Do not invent
missing failure detail or substitute the aggregate status summary for evidence.
When selecting tests, pass only target IDs returned by `test_DiscoverTests`
such as `test`, or omit `targets` to run the default. Commands and glob
arguments such as `./...` are not target IDs.
