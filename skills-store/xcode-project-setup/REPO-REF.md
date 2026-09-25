# Repo Referensi: firebase/agent-skills

Repo: https://github.com/firebase/agent-skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/firebase_agent-skills
API: curl "localhost:27126/repos/readme?name=firebase_agent-skills"
Dibuat: 2026-09-16

## Cuplikan README
# firebase/agent-skills

Source: https://github.com/firebase/agent-skills
Fetched: 2026-09-16

## README
<h1 align="center">
  <img src="assets/firebase-agent-skills_logo.svg" width="48" alt="Logo" style="vertical-align: middle; margin-right: 10px;">
  Firebase Agent Skills
</h1>

A collection of skills for AI coding agents, to help them understand and work
with Firebase more effectively.

Skills are packaged instructions and scripts that extend agent capabilities,
following the [Agent Skills](https://agentskills.io/home) format.

## Installation

### Option 1: Agent Skills CLI

For most popular AI-assistive tools, you can use the `skills` CLI to install
Firebase agent skills:

```bash
npx skills add firebase/skills
```

### Option 2: Gemini CLI Extension

This repository is configured as a Gemini CLI extension. You can add it using
the Gemini CLI:

```bash
gemini extensions install https://github.com/firebase/skills
```

### Option 3: Claude Plugin

1. Add the Firebase marketplace for Claude plugins:

```bash
claude plugin marketplace add firebase/skills
```

Install the Claude plugin for Firebase:

```bash
claude plugin install firebase@firebase
```

Verify the installation:

```bash
claude plugin marketplace list
```

### Option 4: Codex Plugin

Add the Firebase marketplace for Codex plugins:

```bash
codex plugin marketplace add firebase/skills
```

Install the Firebase plugin:

```bash
codex plugin add firebase@firebase
```

### Option 5: Kimi Plugin

Install the Firebase plugin in Kimi Code CLI:

```bash
/plugins install https://github.com/firebase/skills
```

Verify the installation:

```bash
/plugins list
```

### Option 6: Manual Set Up

1. Clone this repository:

```bash
git clone https://github.com/firebase/skills.git
```

2. Copy the contents of the `skills` directory to the appropriate location for
   your AI tool. Common locations include:
   - **Cursor**: `.cursor/rules/`
   - **Windsurf**: `.windsurfrules/`
   - **GitHub Copilot**: `.github/copilot-instructions.md` (or project-specific
     instruction files)

### Option 7: Local Path via Agent Skills CLI

The `skills` CLI also supports installing skills from a local directory. If you
have cloned this repository, you can add skills by pointing the CLI to your
local folder:

```bash
npx skills add /path/to/your/local/firebase-skills/skills
```

If you make changes to the local skills repository and want to update your
project with the new changes, you can update them by running:

```bash
npx
