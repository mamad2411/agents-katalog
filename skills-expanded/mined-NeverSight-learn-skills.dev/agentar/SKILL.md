---
name: agentar
description: This skill should be used to delegate tasks to Agentar platform agents from the command line. Use it when a task involves installing or verifying Agentar CLI, installing the Agentar Skill, running Agentar chat commands, configuring credentials, delegating office work such as PPTs, research documents, or tables, generating images, creating videos, testing attachments or sessions, or troubleshooting ordinary Agentar CLI usage.
---

# Agentar

## Overview

Use this skill to run Agentar from the command line, delegate specific tasks to Agentar platform agents, and validate Agentar workflows end to end. Ordinary `agentar "..."` chat does not require a backend `agentId`; select an explicit `--agent` only when the task should use one of the built-in scenario agents or when the caller supplies a backend `agentId`.

Agentar can delegate user tasks to built-in scenario agents: `office-agent` for PPTs, research documents, summaries, and tables; `image-agent` for image generation; and `video-agent` for video creation. This skill provides the safe CLI workflow for running ordinary chat or a selected scenario agent with explicit credentials and verifying results with repeatable commands.

The built-in scenario agents currently exposed by the CLI are:

- `office-agent`: delegate office productivity tasks such as creating PPTs, drafting research documents, summarizing materials, and producing tables.
- `image-agent`: delegate image generation tasks.
- `video-agent`: delegate video creation tasks.

The skill also covers installing and verifying the `agentar` command, configuring credentials safely, running chat/session/attachment flows, selecting built-in scenario agents when useful, and diagnosing ordinary CLI usage problems before changing source code.

The Agentar CLI distribution channel is an implementation detail of the install workflow below. Follow that workflow when installation or upgrade is required; otherwise start from the usage, safety, or troubleshooting sections that match the user's request.

## When To Use

Use this skill when the user asks to:

- Ask Agentar a general question or start an ordinary Agentar chat.
- Run a general Agentar task from the command line when no specialized scenario agent is needed.
- Create office outputs such as PPTs, research documents, summaries, or tables.
- Generate images.
- Create videos.
- Run or continue Agentar conversations from the command line without requiring an agent ID.
- Test attachments, output formats, sessions, or generated results.
- Configure Agentar credentials, authentication state, session state, or isolated test state.
- Install, upgrade, verify, or troubleshoot the Agentar CLI or Agentar Skill package.

Do not use this skill for unrelated Agentar platform source-code changes unless the CLI workflow has already reproduced a defect that requires code-level debugging.

## Install Workflow

Check Node.js and npm first. The installer uses npm internally; if npm is unavailable, fix npm instead of switching to pnpm or yarn for Agentar CLI installation:

```bash
node -v
npm -v
```

Confirm the install script is reachable:

```bash
curl -I 'https://dtaiagtavtr.antdigital.com/agentar-cli/install.sh'
```

Prefer the public production install script for user-facing installation:

```bash
curl -fsSL 'https://dtaiagtavtr.antdigital.com/agentar-cli/install.sh' | bash
```

The installer places the binary under `/tmp/agentar-cli/bin` by default. Verify with the absolute path first:

```bash
/tmp/agentar-cli/bin/agentar --version
/tmp/agentar-cli/bin/agentar --help
```

Add the binary to the current shell only when direct `agentar` invocation is needed:

```bash
export PATH="/tmp/agentar-cli/bin:$PATH"
agentar --version
```

For validation or CI-style checks, keep token and state files isolated under a temp directory.

The public production skill zip is available at:

```text
https://dtaiagtavtr.antdigital.com/agentar-cli/skill.zip
```

Install the marketplace Skill with the official Skills command:

```bash
npx skills add OpenAgentar/agentar-skills
```

## Usage Workflow

1. Verify the binary first:

   ```bash
   agentar --version
   agentar --help
   ```

2. Configure credentials. Prefer environment variables for one-off runs and `auth login` for persistent local use:

   ```bash
   AGENTAR_API_KEY=<YOUR_API_KEY> agentar "hello"
   agentar auth login --api-key <YOUR_API_KEY>
   agentar auth status
   ```

3. Run chat commands:

   ```bash
   agentar "hello"
   agentar chat "hello"
   agentar "hello" --output json
   ```

4. Use session commands only when multi-turn continuation is required:

   ```bash
   agentar "remember this" --name demo
   agentar -c "continue"
   agentar session list
   agentar session use demo
   ```

5. Do not require a backend `agentId` for ordinary chat. Use `--agent` only when the task clearly maps to a built-in scenario agent or when the caller explicitly supplies a backend `agentId`. Prefer built-in `--agent` presets over manual scene flags; use a raw backend `agentId` only when the caller explicitly supplies one:

   ```bash
   agentar "hello"
   agentar "summarize this" --attach ./file.pdf
   agentar -a office-agent "draft an office document outline"
   agentar -a image-agent "generate an image"
   agentar -a video-agent "generate a 5 second video of an orange cat resting by a sunny window" --duration 5
   agentar --agent openapi_default_agent "hello"
   ```

   `agentar agents` lists local presets only: `office-agent`, `image-agent`, and `video-agent`. Unknown `--agent` values are passed through as backend `agentId` values and are not listed by the CLI.

## Safety And Secrets

Do not print API keys, bearer tokens, saved token files, or raw request headers. Use placeholders such as `<YOUR_API_KEY>` or `sk-xxxxxxxxxxxX` in instructions and reports. For repeatable tests, isolate state with `AGENTAR_TOKEN_FILE` and `AGENTAR_PLAYGROUND_STATE_FILE` under a temp directory.

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| `agentar: command not found` | `/tmp/agentar-cli/bin` is not on `PATH` | Run `export PATH="/tmp/agentar-cli/bin:$PATH"` and retry |
| Install script download fails | Network cannot reach the download domain | Check network, proxy, or install script reachability |
| Auth fails or returns 401 | API key is missing or invalid | Run `agentar auth login --api-key <YOUR_API_KEY>` again |
| Skill does not trigger | Skill is not installed or the host CLI has not restarted | Run `npx skills add OpenAgentar/agentar-skills`, then restart the host CLI |

## Resources

- Public production install script: `https://dtaiagtavtr.antdigital.com/agentar-cli/install.sh`.
- Public production skill zip: `https://dtaiagtavtr.antdigital.com/agentar-cli/skill.zip`.
- `references/agentar-cli-quick-reference.md`: compact command, output, attachment, and scenario examples.
