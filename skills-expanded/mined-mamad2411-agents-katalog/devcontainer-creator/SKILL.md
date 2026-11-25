---
name: devcontainer-creator
description: Create, edit, and update devcontainer environments (`.devcontainer/devcontainer.json`). Trigger this skill when asked to create a standardized Docker development environment, add development features (like Python, Go, Node.js), or initialize a VS Code/Codespaces compatible workspace.
---

# Devcontainer Creator

This skill acts as an implementation manual to assist you in creating, editing, and updating `.devcontainer/devcontainer.json` environments. It leverages the official Dev Container Specification, using images from `mcr.microsoft.com` and features from `ghcr.io/devcontainers/features/`.

## Core Principle

**Mandatory Planning:** Before creating or modifying any `.devcontainer` configuration files, you MUST draft a design plan and obtain user approval. The plan should outline the orchestration method (image, Dockerfile, or Compose), the base image, requested features, and any required lifecycle scripts or environment variables.

## Workflow

Follow these steps to construct or update the Devcontainer configuration:

### 1. Analyze the Workspace
Examine the project root to determine the primary languages and tools in use:
- Check for dependency files (e.g., `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`).
- Look for existing `Dockerfile` or `docker-compose.yml` (or `compose.yaml`) files. If the project already has custom container setups, prefer using the existing orchestration method (Dockerfile or Compose) over a pure image-based configuration.
- Check if a `.devcontainer` directory already exists. If it does, your goal is to *update* or *repair* it, not overwrite it blindly.

### 2. Draft Configuration Plan
Draft a plan proposing the orchestration method, base image, and any necessary features.

#### Select the Orchestration Method and Base Image
Based on the project's structure, choose the appropriate method:
- **Image-based**: If no Dockerfile/Compose exists. Refer to `references/images-catalog.md`.
  - If the project uses multiple languages or the user asks for a generic environment, prefer the `universal` image or a generic `base:ubuntu` / `base:debian` image. Always pin to a specific version or OS variant (e.g., `:8-bookworm`).
  - *Third-party Images*: You may also use other valid public images (e.g., NGC images like `nvcr.io/nvidia/cuda:13.2.0-cudnn-devel-ubuntu22.04` or `nvcr.io/nvidia/pytorch:26.02-py3`).
  - **Rule for non-devcontainer images:** When using images *not* specifically built for dev containers (like `ubuntu:latest` or `nvcr.io/...`), you MUST include the following baseline features to ensure a functional workspace:
    - `"ghcr.io/devcontainers/features/common-utils:2": {}`
    - `"ghcr.io/devcontainers/features/git:1": {}`
    - `"ghcr.io/devcontainers/features/git-lfs:1": {}`
- **Dockerfile-based**: If a `Dockerfile` exists. In `devcontainer.json`, replace `image` with a `build` object containing `dockerfile` (and optionally `context`). E.g., `"build": { "dockerfile": "Dockerfile", "context": "." }`.
- **Compose-based**: If a `docker-compose.yml` exists. In `devcontainer.json`, you must provide:
  - `"dockerComposeFile"`: Relative path to the compose file.
  - `"service"`: The name of the main dev container service defined in the compose file.
  - `"workspaceFolder"`: The path where the code is mounted (e.g., `"/workspaces/${localWorkspaceFolderBasename}"`).
  - *Note:* In the compose file itself, the dev container service often uses `command: sleep infinity` and a volume mount like `../..:/workspaces:cached`.

#### Select Features
Features are reusable units of installation code. Add them to the `"features"` object in `devcontainer.json`.
- Refer to `references/features-catalog.md` for available features and their configuration.
- Add features based on secondary tools detected (e.g., if a Python project needs AWS CLI, add the `aws-cli` feature).
- **Rule:** When using features, respect the JSON structure: `"ghcr.io/devcontainers/features/<feature-name>:<version>": { "optionName": "value" }`. Keep in mind that Features can define their own dependencies using the `dependsOn` property, but you typically just need to list the features you directly want.

### 3. Configure Editor & Environment Settings
Enhance the developer experience by configuring standard properties:
- **`customizations.vscode.extensions`**: Add relevant VS Code extensions based on the chosen languages (e.g., `ms-python.python`, `golang.go`).
- **`forwardPorts`**: If a web framework is detected (e.g., Express, Django), add the default development port to this array.
- **`remoteUser`**: To prevent running as root:
  - If using an official `mcr.microsoft.com/devcontainers/*` image, the user is usually already set up (e.g., `vscode` or `node`), so omit `remoteUser` unless explicitly overriding.
  - If using a generic/third-party image (like NGC or vanilla ubuntu) along with the `common-utils` feature, set `"remoteUser": "codespace"`.
- **`postCreateCommand`**: Provide a standard command to install dependencies (e.g., `npm install`, `pip install -r requirements.txt`). For multiple commands, use an array of strings or the parallel execution object syntax (refer to `references/schema/lifecycle-requirements.md`).
- **`hostRequirements.gpu`**: If the user needs GPU access (e.g., for AI/ML workloads), use the `hostRequirements.gpu` property. It can be set to `true` (required) or `"optional"` (used if available). (See `references/schema/lifecycle-requirements.md`).

### 4. Implementation
Once the user approves the plan, implement the changes.
- Use the templates in `assets/` as your starting point for new projects depending on the chosen orchestration method:
  - Image-based setups: [base-devcontainer.json](assets/base-devcontainer.json)
  - Dockerfile setups: [base-devcontainer-dockerfile.json](assets/base-devcontainer-dockerfile.json)
  - Compose setups: [base-devcontainer-compose.json](assets/base-devcontainer-compose.json)
- Write the final configuration to `.devcontainer/devcontainer.json`.

## Best Practices & Constraints
- **Idempotency:** Lifecycle scripts (`postCreateCommand`, etc.) should ideally be idempotent.
- **Declarative Secrets:** Do not hardcode secrets in `devcontainer.json`. If the project requires secrets (API keys), declare them using the `secrets` property (See `references/schema/general.md`).
- **Parallel Scripts:** Take advantage of parallel lifecycle script execution for independent setup tasks (e.g., starting a mock DB while npm installing) using the object syntax for commands.
- **Installation Order:** If you need to enforce a specific feature installation order, use the `overrideFeatureInstallOrder` array in the `devcontainer.json`.

## Reference Materials
- [images-catalog.md](references/images-catalog.md): Available base images.
- [features-catalog.md](references/features-catalog.md): Available features.
- [general.md](references/schema/general.md): General dev container properties.
- [scenario-specific.md](references/schema/scenario-specific.md): Specific properties for Image/Dockerfile/Compose.
- [lifecycle-requirements.md](references/schema/lifecycle-requirements.md): Details on lifecycle scripts and host hardware requirements.
- [variables-customizations.md](references/schema/variables-customizations.md): Details on spec variables.
- [supporting-tools.md](references/schema/supporting-tools.md): Tool-specific customizations (VS Code, Codespaces).
