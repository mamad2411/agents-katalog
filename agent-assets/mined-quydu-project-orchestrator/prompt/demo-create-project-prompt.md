---
mode: agent
description: Demo step 1 - provision the Skills Orchestrator Demo project and prepare it for automated follow-up prompts.
---

Skip clarification. Do not ask clarifying questions and do not wait for plan confirmation. Execute this request end to end and report the result when finished.

## Parameters

Use the prompt with no parameters for the normal demo project:

```text
/demo-create-project
```

Use `--Test` to create a separate preserved test project. Test mode keeps the same demo setup and
validation, but appends `-test` to the project name and destination folder so it cannot be
confused with the normal demo project:

```text
/demo-create-project --Test
```

Use `--demo-date YYYY-MM-DD` to record the scheduled demo date in the project brief and report.
This is optional and supports any future invitation; for example:

```text
/demo-create-project --demo-date 2026-09-17
/demo-create-project --Test --demo-date 2026-09-17
```

If `--demo-date` is omitted, do not invent a date. Record that the demo date was not supplied.
The date is metadata only and does not authorize deployment, cleanup, publication, commit, or push.

When `--Test` is present, use these values:

- Project name: `Skills Orchestrator Demo Test`
- Project path: `C:\repos\skills-orchestrator-demo-test`
- Intent: include `test run` and the supplied demo date when present

When `--Test` is absent, use the normal values in the steps below. Never delete an existing normal
or test project; stop and report if its destination already exists.

## Objective

Use Project Orchestrator only as the immutable source framework to provision a new governed project named **Project Orchestrator Demo**. After creation, perform all application development, validation, and any future deployment only inside the newly created project. Do not modify this source repository.

## Steps

1. Create the project by running, from the repository root. Use the normal command unless `--Test`
   was supplied; in test mode use the test name, destination folder, and intent shown above. Add
   the optional demo date to the intent only when the user supplied it:

   ```powershell
   node .\pso.mjs create-project --name "Skills Orchestrator Demo" --destination "C:\repos" --stack typescript,tests --intent "Build the session countdown web app for the GitHub Copilot Skills Orchestrator demo." --accept-risk
   ```

   The normal project is created at `C:\repos\skills-orchestrator-demo`; test mode is created at
   `C:\repos\skills-orchestrator-demo-test`. Stop and report if the selected path already exists;
   do not delete it.

2. Confirm and report these facts from the created project:
   - `conformanceProfile` in `project-orchestrator.json` is `durable`
   - `reports/installation-verification.json` has status `passed`
   - `.github/skills/audit-azure-environment/SKILL.md` exists
   - `infra/discover.ps1` and `infra/main.bicep` exist
   - the number of installed skills
   - `docs/PROJECT-BLUEPRINT.json` exists and records the selected project name and demo intent
   - the supplied demo date is present when `--demo-date` was used, otherwise report it as not supplied

3. Copy `.github/prompts/demo-web-app.prompt.md` from this source repository into the created project at the same relative path, so the presenter can run `/demo-web-app` there without pasting prompt text. This is the final action performed from the source repository. The copied prompt already bypasses clarification for its bounded build workflow while preserving the generated project's default governance and approval policy. In test mode, preserve the test project for inspection after the run; do not delete it automatically.

4. Open the new project in its own Visual Studio Code window using a unique temporary workspace
   identity. Reusing the generated `.code-workspace` path can restore editor tabs from an earlier
   rehearsal, including a localhost preview before the app server exists. Load the generated
   workspace as structured JSON, point its folder at the selected project, and write the session
   copy outside the project so no demo artifact is added:

   ```powershell
   $projectPath = "C:\repos\skills-orchestrator-demo"
   $generatedWorkspace = Join-Path $projectPath "skills-orchestrator-demo.code-workspace"
   $sessionWorkspace = Join-Path $env:TEMP "skills-orchestrator-demo-$([guid]::NewGuid().ToString('N')).code-workspace"
   $workspace = Get-Content $generatedWorkspace -Raw | ConvertFrom-Json
   $workspace.folders[0].path = $projectPath
   $workspace.settings.'window.title' = "🚀 Skills Orchestrator Demo • skills-orchestrator-demo (Workspace)"
   $workspace | ConvertTo-Json -Depth 20 | Set-Content $sessionWorkspace -Encoding utf8
   code --new-window $sessionWorkspace
   ```

   In test mode, substitute the test project path, generated workspace filename, and title. Require the
   session workspace path to be under `$env:TEMP`, require its filename to contain a fresh GUID,
   and confirm its only folder resolves to the selected project before opening it. Never open the
   stable generated workspace directly during this workflow. Do not delete prior VS Code
   workspace storage or chat history.

   `--new-window` is required. Without it the command can return exit code 0 and open nothing at all. Confirm a window titled `skills-orchestrator-demo (Workspace)` appears before reporting success.

   Do not pass `--open` to `create-project`. Combined with `--intent`, that path launches `code chat --mode ask`, which cannot edit files, and it seeds a kickoff prompt that instructs the agent to ask three clarifying questions first. Both would stall the demo.

5. Report the absolute project path and tell the presenter to accept the workspace trust prompt, switch Chat to **Agent** mode, and run `/demo-web-app` in the new window. From this point forward, all work belongs to the new project; do not return to or modify the Project Orchestrator source repository.

   For a fully unattended handoff instead, run this from the created project directory rather than step 5:

   ```powershell
   code chat --mode agent --add-file .github/prompts/demo-web-app.prompt.md "Follow .github/prompts/demo-web-app.prompt.md exactly. Skip clarification and build it end to end."
   ```

## Constraints

- The Project Orchestrator source repository is immutable during the demo. It creates and hands off the new project but is never changed by application build, validation, or deployment work.
- Modify only the newly created project after the initial handoff.
- Do not commit, push, or deploy.
- `--Test` changes only the project name and destination convention; it does not grant permission to mutate external systems.
- `--demo-date` is optional scheduling metadata and must use `YYYY-MM-DD`; do not infer it from conversational context.
