---
name: brain-github-deploy
description: Use when Brain invokes "/brain-github-deploy" for a GitHub repository branch, or when maintaining Brain's internal GitHub deployment workflow that produces Brain Crossplane YAML bundle artifacts. This is Brain-only and not a direct end-user command.
compatibility: git is required. Node.js 18+ is recommended for helper scripts. buildctl, kubectl, and a GitHub token with GHCR package write access are required when the pipeline must push a deployment image. The GHCR package owner is the GitHub login resolved from GITHUB_TOKEN, and successful images must be public. Build-time Kubernetes access must come from the sandbox-provided kubeconfig and current service account in the active namespace. This version does not require Sealos auth prompts, local Docker daemon access, or direct deploy access.
metadata:
  author: labring
---

# Brain GitHub Deploy

Prepare a GitHub repository branch for Brain without requiring direct Sealos login or local Docker builds.

This is a Brain-specific skill derived from the older Sealos deploy workflow. The real caller is Brain, not an end user typing a command. Brain supplies the repository, branch, and GitHub token, then consumes `.sealos/deployment-output.json` as a fixed API response containing one or more Brain/Crossplane templates. The rendered `.sealos/crossplane/resources.yaml` is a convenience multi-document YAML form of `templates[].manifest`.

## Input Contract

This skill expects Brain to provide these inputs:

```json
{
  "repository": "owner/repo or https://github.com/owner/repo",
  "branch": "branch-name",
  "github_token": "GitHub token with GHCR package write access"
}
```

The token may be supplied as the `GITHUB_TOKEN` environment variable instead of being printed in the prompt. Never echo, log, persist, or include the token in generated artifacts.

`repository` is required for source checkout and traceability. `branch` is required for source checkout and must be resolved to a concrete commit SHA before writing build artifacts. `github_token` is required when the skill must push a new GHCR image.

Resolve the GitHub login behind `github_token` with the GHCR preflight helper and use that login as the default GHCR package owner. For example, deploying source repository `labring/ShipRepo` with a token whose `/user.login` is `BrainDeployBot` must produce an image like `ghcr.io/braindeploybot/shiprepo:prepare-<sha>`, while artifacts still record `source.repo = "labring/ShipRepo"`. Do not default image ownership to the source repository owner unless `.sealos/config.json.target_image` explicitly asks for that and the token can publish there.

All successful GHCR deployment images must be public. If the pushed container package is not public after the build, the pipeline must fail before writing a succeeded deployment output.

## Output Contract

The final response must be exactly one JSON object with this fixed machine-readable shape:

```json
{
  "apiVersion": "brain.skills.sh/v1alpha1",
  "kind": "GitHubDeployResponse",
  "status": "succeeded",
  "mode": "deployable",
  "message": "Image built and Brain templates generated",
  "error": null,
  "source": {
    "repository": "https://github.com/owner/repo",
    "branch": "main",
    "commit": "0123456789abcdef0123456789abcdef01234567"
  },
  "image": {
    "ref": "ghcr.io/owner/repo:tag",
    "digest": null
  },
  "templates": [
    {
      "id": "ap:web",
      "role": "application",
      "apiVersion": "example.crossplane.io/v1",
      "kind": "AP",
      "name": "repo",
      "namespace": "default",
      "action": "apply",
      "dependsOn": [],
      "manifest": {
        "apiVersion": "example.crossplane.io/v1",
        "kind": "AP",
        "metadata": {
          "name": "repo",
          "namespace": "default"
        },
        "spec": {}
      }
    }
  ],
  "applyOrder": ["ap:web"],
  "bindings": [],
  "unresolvedInputs": [],
  "warnings": []
}
```

On failure, set `status` to `"failed"`, set `image.ref` to `null`, use a concise human-readable `message`, and put the actionable error string in `error`.

`mode` must be one of:

- `deployable` — image and all required templates are complete; `unresolvedInputs` must be empty
- `needs_input` — image and templates were generated but required user/runtime inputs remain unresolved
- `build_failed` — the image was not pushed successfully
- `unsupported` — the repository cannot be represented as a deployable Brain resource graph

`templates[].manifest` is the only Crossplane/Kubernetes resource body. It must be a valid Brain claim such as `apiVersion: example.crossplane.io/v1`, `kind: AP|DB|Project|DE|EntryPoint|Task|Notif`, or an explicitly supported platform resource such as `objectstorage.sealos.io/v1` `ObjectStorageBucket` plus safe Kubernetes `Secret`/`ConfigMap` support resources when required. Do not put `id`, `dependsOn`, `bindings`, or other API envelope fields inside `manifest`.

Detected managed databases (`postgres`, `mysql`, `mongodb`, `redis`) are generated as Brain `DB` claim templates before `ap:web`. Required database URL env vars that can be matched to those DB claims are generated in `ap:web.manifest.spec.input.env` from the DB connection secret instead of being listed in `unresolvedInputs`. Detected S3-compatible object storage is generated as an `ObjectStorageBucket` template before `ap:web`; object-storage service templates such as MinIO or RustFS can still be supplied explicitly through `brain.templates` as AP template claims when the project needs to deploy the storage service itself.

This version of `brain-github-deploy` is a sandbox-first workflow:

1. inspect and score the project
2. repair or generate a Dockerfile
3. confirm sandbox-local build inputs
4. write `.sealos/build-request.json`
5. run a sandbox BuildKit build through `k8s-buildkit-job`
6. push the deployment image to GHCR
7. write `.sealos/deployment-output.json` as the fixed `GitHubDeployResponse`
8. write `.sealos/crossplane/resources.yaml` from `templates[].manifest`

It does not:

- perform Sealos auth
- switch region, workspace, or namespace
- build or push images locally
- deploy directly to Sealos
- apply the Brain Crossplane bundle

## kubectl Safety Rules

If any future phase or downstream skill uses `kubectl`, it must use the sandbox-provided permissions, kubeconfig, namespace, and current service account. This version may create one-shot build Jobs, but it still must not mutate Sealos application resources directly.

## Brain Invocation

```text
/brain-github-deploy <repository> <branch>
```

This is the internal Brain invocation shape. Do not present it as a user-facing command. Brain may pass `repository` as `owner/repo`, `https://github.com/owner/repo`, or a git SSH URL. Checkout the requested `branch` into a sandbox-local working directory before pipeline execution. When the current workspace is already the target repository and branch, use that sandbox-local path instead of recloning.

The downstream BuildKit executor builds from the sandbox-local filesystem in `source.work_dir`. Repository, branch, and ref fields are recorded for traceability, while default image ownership comes from the resolved `GITHUB_TOKEN` login. The build does not pull Dockerfiles from GitHub at execution time.

## Quick Start

Execute the modules in order:

1. `modules/preflight.md` — environment checks and project resolution
2. `modules/pipeline.md` — build-and-prepare pipeline (Phase 1–6)

## Logging

Every run should write a log file at `~/.sealos/logs/deploy-<YYYYMMDD-HHmmss>.log`.

At the start of execution:

```bash
mkdir -p ~/.sealos/logs
LOG_FILE=~/.sealos/logs/deploy-$(date +%Y%m%d-%H%M%S).log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Prepare run started" > "$LOG_FILE"
```

Append phase boundaries and key decisions to the same file with `>>`.

## Scripts

Located in `scripts/` within this skill directory (`<SKILL_DIR>/scripts/`):

| Script | Usage | Purpose |
|--------|-------|---------|
| `score-model.mjs` | `node score-model.mjs <repo-dir>` | Deterministic readiness scoring (0-12) |
| `write-brain-deploy-response.mjs` | `node write-brain-deploy-response.mjs --analysis <file> --build-result <file> --out <file> --yaml-out <file> [--config <file>]` | Write the fixed API response and rendered Crossplane resources YAML |
| `write-deployment-output.mjs` | `node write-deployment-output.mjs --analysis <file> --build-result <file> --out <file> --yaml-out <file> [--config <file>]` | Compatibility entry point for `write-brain-deploy-response.mjs` |
| `write-brain-crossplane-ap.mjs` | `node write-brain-crossplane-ap.mjs --analysis <file> --build-result <file> --out <file> [--config <file>]` | Legacy single-AP helper retained for tests and migration reference |
| `validate-artifacts.mjs` | `node validate-artifacts.mjs --dir <work-dir>` | Validate `.sealos` JSON artifacts against enforced schemas |

Helper scripts output JSON except rendered YAML written through `--yaml-out`. Run scripts via Bash and parse or validate the expected artifact type.

## Internal Skill Dependencies

This skill references co-installed internal skills on demand:

```text
<SKILL_DIR>/../
├── brain-github-deploy/     ← this skill (Brain internal entry point)
├── dockerfile-skill/        ← Phase 2: Dockerfile generation knowledge
├── k8s-buildkit-job/        ← Phase 4: sandbox BuildKit execution
├── cloud-native-readiness/  ← Phase 1: assessment criteria
└── docker-to-sealos/        ← legacy Sealos template conversion references, not the API response contract
```

## Phase Overview

| Phase | Action | Skip When |
|-------|--------|-----------|
| 0 — Preflight | Capability scan, project resolution, sandbox assumptions | Entry blockers resolved |
| 1 — Assess | Analyze deployability and write `analysis.json` | Score too low → stop |
| 2 — Dockerfile | Reuse or generate Dockerfile | Existing valid Dockerfile can be reused |
| 3 — Build Context | Verify sandbox-local build inputs | — |
| 4 — Build And Push | Write `build-request.json`, run BuildKit, push GHCR image, resolve `build-result.json` | — |
| 5 — Brain Templates | Generate fixed response templates and `.sealos/crossplane/resources.yaml` from the resolved image and Brain resource plan | Existing valid response/resources can be reused |
| 6 — Finish | Write `delivery-manifest.json`, validate artifacts, return `GitHubDeployResponse` JSON | — |

## Decision Flow

```text
Input (Repository + branch + GitHub token)
  │
  ▼
[Phase 0] Preflight ── fail → explain blocker and STOP
  │ pass
  ▼
[Phase 1] Assess ── not suitable → STOP with reason
  │ suitable
  ▼
[Phase 2] Dockerfile
  │
  ▼
[Phase 3] Confirm build context
  │
  ▼
[Phase 4] Build and push GHCR image
  │
  ▼
[Phase 5] Generate Brain templates
  │
  ▼
[Phase 6] Finish with deployment output JSON
  │
  ▼
Done — deployment image pushed to GHCR and Brain templates generated
```

Execution rule: this version must never require Docker daemon access, Sealos auth, GitHub auth prompts, workspace switching, or direct deploy as entry prerequisites. It may require `buildctl`, `kubectl`, and `GITHUB_TOKEN` for the GHCR push path. When that happens, use only the active sandbox namespace and current service account instead of assuming `default` or switching to an admin kubeconfig. The final Brain-visible answer must follow the fixed `GitHubDeployResponse` contract and must not include token material.
