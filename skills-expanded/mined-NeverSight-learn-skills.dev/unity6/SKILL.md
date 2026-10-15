---
name: unity6
description: Automate Unity 6 project initialization, environment pre-flight setup, package management, headless builds, automated testing, native pipeline C# commands ([CliCommand]), live REPL code evaluation (unity command eval), Model Context Protocol (MCP) server integration (unity mcp), editor status monitoring, and editor pipeline management with the Unity CLI. Use whenever the user mentions Unity, /unity6, /unity6:android, /unity6:android-optimize, /unity6:ios, /unity6:ios-optimize, /unity6:webgl, /unity6:webgl-optimize, /unity6:scene, /unity6:asset, /unity6:playmode, /unity6:package, /unity6:shader, setup, doctor, editor setup, project creation, pipeline, build automation, test runner, package installation, MCP, unity mcp, CliCommand, profiling, or agent workflows involving Unity Editor management.
---

# Unity 6 Automation & CLI Guide (Modern `unity` CLI & `com.unity.pipeline`)

## What This Skill Does

Automates end-to-end Unity 6 project initialization, environment pre-flight onboarding, dependency management, interactive 5-stage setup questionnaire (naming, OS pathing, LTS/Tech editor choices, template selection, Unity Cloud linking vs local-only), automated test execution, headless build automation, native `com.unity.pipeline` C# command execution (`[CliCommand]`), Model Context Protocol (`unity mcp`) integration for AI agents, live REPL C# code evaluation (`unity command eval`), status diagnostics (`unity status`), profiling analysis, and CI/CD workflow integration using 100% native `unity` CLI commands (v1.0.0-beta.3 or later) without requiring external scripts.

**Beta Notice**

The `unity` CLI and `com.unity.pipeline` package are currently in beta (v1.0.0-beta.3). Output formats, flag names, and exit codes may change between releases. If a command fails unexpectedly, update the CLI with `unity upgrade` and check the official Unity CLI documentation for the current API.

---

## 🛑 CRITICAL AI GUARDRAILS (READ FIRST)

If you are an AI agent, LLM, or automated script, you **MUST STRICTLY OBEY** the following process management rules:

1. **NEVER use OS-level process commands** (e.g., `ps aux`, `kill`, `killall`, `pkill`, `top`) to find or terminate the Unity Editor.
2. **NEVER try to launch the Editor in the background** using shell backgrounding (e.g., `&`, `nohup`).
3. **NEVER use macOS `open -a` or Windows `Start-Process`** to launch Unity.
4. **ALWAYS use `unity status`** to check if an Editor is running and connected.
5. **ALWAYS use `unity command eval "UnityEditor.EditorApplication.isPlaying = false;"`** to stop a running game.
6. **ALWAYS use `unity command eval "UnityEditor.EditorApplication.Exit(0);"`** if you absolutely must close the Editor gracefully.

Failure to follow these guardrails will corrupt the `com.unity.pipeline` socket connection and break the user's project state.

---

## Slash Commands & Sub-Skill Matrix (`unity command eval`)

Execute specialized sub-workflows via colon-delimited sub-commands or dashed sub-skills:

| Sub-Command / Skill | Target Workflow | Pure Native `unity command eval` Expression |
| :--- | :--- | :--- |
| **`/unity6`** | Environment Onboarding & Interactive Setup | `unity doctor && unity auth status && unity license status` |
| **`/unity6:scene`** | Scene & Object Control | `unity command eval "return UnityEngine.SceneManagement.SceneManager.GetActiveScene().name;"` |
| **`/unity6:asset`** | AssetDatabase Operations | `unity command eval "UnityEditor.AssetDatabase.Refresh(ImportAssetOptions.ForceUpdate);"` |
| **`/unity6:playmode`** | Live PlayMode Control | `unity command eval "UnityEditor.EditorApplication.isPlaying = true;"` |
| **`/unity6:package`** | PackageManager Control | `unity command eval "UnityEditor.PackageManager.Client.Add(\"com.unity.inputsystem\");"` |
| **`/unity6:shader`** | Shader Variant Stripping| `unity command eval "return UnityEditor.ShaderUtil.GetShaderGlobalKeywords();"` |
| **`/unity6:android-optimize`** (or `/unity6:android`) | Android Target Setup | `unity command eval "PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;"` |
| **`/unity6:ios-optimize`** (or `/unity6:ios`) | iOS Metal / IL2CPP Setup| `unity command eval "PlayerSettings.SetScriptingBackend(BuildTargetGroup.iOS, ScriptingImplementation.IL2CPP);"` |
| **`/unity6:webgl-optimize`** (or `/unity6:webgl`) | WebGL WASM / Brotli Setup| `unity command eval "PlayerSettings.SetManagedStrippingLevel(BuildTargetGroup.WebGL, ManagedStrippingLevel.High);"` |

---

## Interactive 5-Stage Project Setup Questionnaire

When `/unity6` or project initialization is triggered, the agent runs the following 5-stage setup questionnaire after pre-flight diagnostics pass:

### Stage 1: Naming & OS-Specific Path Resolution
- **Prompt**: Ask for Project Name (e.g. `MyGame`) and parent directory.
- **OS Path Resolution** (Auto-detected via `unity doctor --json`):
  - **macOS (`darwin`)**: Defaults to `~/Projects/MyGame`
  - **Windows (`win32`)**: Defaults to `C:\Users\<user>\Projects\MyGame`
  - **Linux (`linux`)**: Defaults to `/home/<user>/Projects/MyGame`

### Stage 2: Editor Version Decision Matrix (Installed vs. LTS vs. Tech)
- Query installed editors (`unity editors --installed --json`) and available releases (`unity releases --lts`).
- Present 3 options:
  - **Option A (Installed)**: Use detected Editor (e.g. `6000.7.0a3`).
  - **Option B (Recommended for Production)**: Install latest **LTS (Long Term Support)** release (`unity releases --lts`, `unity install 6000.0.30f1`).
  - **Option C (Tech Stream)**: Install latest **Tech / Beta** release for cutting-edge features (`unity releases --stream tech`).

### Stage 3: Render Pipeline & Template Selection
- Query templates available for editor (`unity templates list --editor <ver>`):
  - *(Recommended)* **Universal Render Pipeline (URP 3D)** (`com.unity.template.urp-blank`) — Best balance for Mobile, PC, & Consoles.
  - **Universal 2D (URP 2D)** (`com.unity.template.universal-2d`) — 2D games with URP lighting.
  - **High Definition Render Pipeline (HDRP)** (`com.unity.template.hdrp-blank`) — High-end PC & Console graphics.
  - **3D Core** (`com.unity.template.3d`) — Standard Built-in Render Pipeline.

### Stage 4: Unity Cloud Linking vs. Local-Only Mode
- **Local-Only Mode**: Offline, lightweight local project development.
- **Unity Cloud Linked**: Configures Unity Cloud Organization & Project ID (`unity cloud project`).

### Stage 5: Pipeline & Package Bootstrap
- Installs `com.unity.pipeline` package (`unity pipeline install --project-path <path> --non-interactive`).
- Installs optional package dependencies (`com.unity.inputsystem`, `com.unity.addressables`).

---

## Workflow Overview

The Unity 6 agent pipeline consists of 12 modular phases:

1. **Pre-Flight Environment & Onboarding (`/unity6`)** — Run native diagnostic pre-flight checks (`unity doctor`, `unity auth status`, `unity license status`)
2. **Interactive 5-Stage Setup Questionnaire** — Name, OS pathing, Editor version (Installed vs LTS), template, and Unity Cloud linking
3. **Enumerate Installed Editors** — Detect available Unity editors and architectures (`unity editors --installed --json`)
4. **Create Project & Templates** — Provision new projects from standard or custom templates (`unity projects new`)
5. **Manage Packages & Pipeline** — Install Unity Pipeline package (`com.unity.pipeline`) and manage `Packages/manifest.json` (`unity pipeline install`)
6. **Model Context Protocol (`unity mcp`)** — Configure MCP server and client integration for AI agents (`unity mcp configure antigravity`)
7. **Live Code & Command Execution (`unity command eval`)** — Trigger live C# code directly in connected Editor or Player runtime instances (`unity command eval`, `unity command --runtime <name>`)
8. **Native Pipeline Commands (`[CliCommand]`)** — Register custom C# Editor methods using `[CliCommand]` and trigger them via terminal (`unity command <command-name>`)
9. **Automated Testing** — Execute EditMode/PlayMode test suites and extract XML/JUnit reports (`unity test`)
10. **Headless Build Automation** — Build binaries across target platforms using Build Profiles (`unity build`)
11. **Native Platform & Feature Sub-Skills** — Execute pure native C# evaluation sub-skills (`/unity6:scene`, `/unity6:asset`, `/unity6:playmode`, `/unity6:package`, `/unity6:android-optimize`, `/unity6:android`)
12. **Status & Process Control** — Monitor live Editor PIDs, ports, and pipeline status (`unity status`, `unity pipeline list`)

---

## Prerequisites

- **`unity` CLI** v1.0.0-beta.3 or later
  - Install or upgrade: `unity upgrade`
  - Verify: `unity --version`
- **`com.unity.pipeline` Package**: Installed in project via `unity pipeline install`
- **Disk space**: 10–30 GB (only if installing a new editor version)
- **Non-interactive mode required for CI/CD**: Use `--non-interactive`, `--json`, and `--quiet` flags on all commands

---

## Step-by-Step Instructions

### Step 0: Environment Pre-Flight Checklist & Guided Setup (`/unity6`)

```bash
unity doctor
unity auth status
unity license status
unity editors --installed --json
```

---

### Step 1: Create Project via 5-Stage Setup Questionnaire

```bash
unity projects new MyGame \
  --editor-version 6000.7.0a3 \
  --template com.unity.template.urp-blank \
  --path ~/Projects \
  --non-interactive
```

---

### Step 2: Package & Pipeline Setup

```bash
unity pipeline install --project-path ~/Projects/MyGame --non-interactive
```

---

## Error Scenarios

### 1. Missing Unity CLI Binary
- **Diagnosis**: Command `unity` is not found in PATH.
- **Fix**: Run `npm install -g @unity/cli` or download binary from https://docs.unity.com/cli.

### 2. Not Authenticated / License Missing
- **Diagnosis**: `unity auth status` or `unity license status` returns false.
- **Fix**: Run `unity auth login` to authenticate, then `unity license activate`.

---

## Reference

- Official Unity CLI Docs: https://docs.unity.com/cli
- Unity Pipeline Package (`com.unity.pipeline`) Manual: https://docs.unity.com/6000/Manual/
- Sub-Skills: `unity6-android-optimize`, `unity6-ios-optimize`, `unity6-webgl-optimize`
