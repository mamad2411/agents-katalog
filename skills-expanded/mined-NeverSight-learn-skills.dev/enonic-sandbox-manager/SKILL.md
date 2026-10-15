---
name: enonic-sandbox-manager
description: Guides developers through Enonic CLI commands for sandbox management, project scaffolding, local development, app deployment, and CI/CD pipeline generation. Use when creating Enonic XP sandboxes, starting or stopping local instances, scaffolding projects from starters, running dev mode with hot-reload, deploying apps, or generating CI/CD workflows for Enonic apps. Don't use for writing XP application code (controllers, content types), querying via Guillotine or lib-content APIs, configuring non-Enonic environments, or Docker/Kubernetes deployment of XP.
license: MIT
metadata:
  author: webmaxru
  version: "1.1"
---

# Enonic CLI & Local Dev Environment Helper

## Procedures

**Step 1: Detect Workspace Context**
1. Execute `node scripts/find-enonic-targets.mjs` from the skill root to scan the current workspace for Enonic project markers (`.enonic`, `build.gradle` with `com.enonic.xp` plugin, `gradle.properties` with `xpVersion`).
2. If markers are found, note the project name, linked sandbox, and XP version from the output. Use these values as defaults for subsequent commands.
3. If no markers are found, treat the request as a greenfield setup and proceed to sandbox creation or project scaffolding as appropriate.

**Step 2: Ensure CLI is Available**
1. Verify the Enonic CLI is installed by running `enonic --version`.
2. If the command fails, read `references/cli-reference.md` for installation instructions and guide through the appropriate method for the detected OS:
   - **npm (any OS):** `npm install -g @enonic/cli`
   - **macOS:** `brew tap enonic/cli && brew install --no-quarantine enonic`
   - **Linux:** `wget -qO- https://repo.enonic.com/public/com/enonic/cli/installer/cli-linux/1.0.0/cli-linux-1.0.0.sh | sh`
   - **Windows:** `scoop bucket add enonic https://github.com/enonic/cli-scoop.git && scoop install enonic`
3. After installation, verify with `enonic --version`.

**Step 3: Sandbox Management**
1. Read `references/cli-reference.md` for the full sandbox command catalog.
2. Match the request to the correct operation:
   - **Create:** `enonic sandbox create <name> [-v <version>] [-t <template>] [--skip-template] [-f]`
   - **List:** `enonic sandbox ls`
   - **Start:** `enonic sandbox start <name> [--detach] [--prod] [--debug]`
   - **Stop:** `enonic sandbox stop`
   - **Upgrade:** `enonic sandbox upgrade <name> -v <version>`
   - **Delete:** `enonic sandbox delete <name> -f`
   - **Copy:** `enonic sandbox copy <source> <target>`
3. When creating a sandbox, prompt for the XP version if not specified. Use `-f` flag for non-interactive execution when the version and name are known.
4. If the request mentions templates, list available templates or use `-t <template>` flag. Use `--skip-template` to create a bare sandbox with no pre-installed apps.

**Step 4: Project Scaffolding**
1. For new project creation, use the simplified command: `enonic create <name> [-r <starter>] [-s <sandbox>] [-f]`
2. Common starters include `starter-vanilla`, `starter-headless`, and `starter-nextjs`. Read `references/cli-reference.md` for the full list of options.
3. To link an existing project to a different sandbox: `enonic project sandbox <name>`
4. Ensure the project folder contains `build.gradle` and `.enonic` configuration after creation.

**Step 5: Development Workflow**
1. Determine the appropriate development command:
   - **Dev mode (hot-reload):** `enonic dev` — starts the sandbox in detached mode and runs the app with file watching. Execute from the project root.
   - **Build only:** `enonic project build`
   - **Deploy to sandbox:** `enonic project deploy [sandbox-name] [-c]` — use `-c` for continuous deployment.
   - **Install to running XP:** `enonic project install`
   - **Run tests:** `enonic project test`
   - **Clean build artifacts:** `enonic project clean`
   - **Arbitrary Gradle task:** `enonic project gradle <tasks>`
2. If the sandbox is not running, start it first: `enonic sandbox start <name> -d`
3. To terminate dev mode, use `Ctrl-C`. The CLI will attempt to stop the detached sandbox automatically.

**Step 6: App Management on Running XP**
1. For managing applications on a running XP instance, read `references/cli-reference.md` for the XP app commands.
2. Match the operation:
   - **Install from URL:** `enonic app install --url <jar-url>`
   - **Install from file:** `enonic app install --file <path-to-jar>`
   - **Start app:** `enonic app start <app-key>`
   - **Stop app:** `enonic app stop <app-key>`
3. Authentication is required for XP commands. Use `--cred-file <path>` (XP 7.15+) or set `ENONIC_CLI_REMOTE_USER` and `ENONIC_CLI_REMOTE_PASS` environment variables.

**Step 7: CI/CD Pipeline Generation**
1. Read `assets/enonic-ci.template.yml` for the GitHub Actions workflow template.
2. Customize the template based on the project:
   - Set the correct XP version in the sandbox creation step.
   - Set the app name and Gradle build parameters.
   - Configure deployment targets (sandbox for staging, cloud for production).
3. Place the generated workflow file at `.github/workflows/enonic-ci.yml` in the project repository.

**Step 8: Troubleshooting**
1. If a sandbox fails to start or a deployment fails, read `references/troubleshooting.md` for common issues and resolutions.
2. Key diagnostic commands:
   - `enonic sandbox ls` — check sandbox status and XP version.
   - `enonic system info` — check running XP instance details.
   - Check port `8080` (HTTP) and `5005` (debug) availability.
3. Read `references/compatibility.md` for CLI-to-XP version compatibility if version mismatch errors occur.

## Error Handling
* If `scripts/find-enonic-targets.mjs` returns no results, proceed with greenfield setup instructions rather than failing.
* If `enonic --version` fails, guide through CLI installation per Step 2 before proceeding.
* If sandbox creation fails with a version error, read `references/compatibility.md` and suggest a compatible XP version.
* If port conflicts occur during sandbox start, read `references/troubleshooting.md` for resolution steps.
* If `enonic dev` fails, verify the project has a Gradle `dev` task (present in all official starters) and that the linked sandbox exists and is not already running in another terminal.
