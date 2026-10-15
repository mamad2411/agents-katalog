---
name: install-civitai-videoflow-bundle
description: "Automatically installs and validates the Civitai Videoflow skill bundle from the civitai-agent-skills repository. Supports git clone or manual zip upload, runs npx skills add in dependency-safe order, and guides environment and tool prerequisite checks for CIVITAI_RECORDS_DATABASE_URL, DUOMI_API_TOKEN, IMAGEKIT_PRIVATE_KEY, and CIVITAI_ACCOUNT. Use when: user needs videoflow setup, install Civitai pipeline skills, configure image-to-video workflow, enable Civitai publish pipeline, or when civitai-videoflow and related worker skills are mentioned but unavailable. Triggers: install videoflow skills, setup civitai skills bundle, configure civitai-agent-skills, enable videoflow commands, install duomi/civitai pipeline skills."
---

# Install Civitai Videoflow Bundle

Automatically installs the Videoflow orchestrator and its worker skills, then verifies environment and runtime prerequisites.

## What This Skill Does

This skill helps install and validate the default Civitai Videoflow bundle:

1. **duomi-image-generator-skill** - image generation used by the pipeline
2. **duomi-video-generation-skill** - image-to-video generation
3. **civitai-upload-assets-skill** - upload assets for workflow steps
4. **civitai-post-skill** - optional Civitai publishing
5. **civitai-prompt-enhancer-skill** - creative prompt enhancement
6. **civitai-image-curator-skill** - candidate image selection support
7. **civitai-video-prompt-enhancer-skill** - motion/video prompt generation
8. **civitai-videoflow** - pipeline orchestrator skill

The bundle is installed in a deterministic order so dependency skills are available before the orchestrator is installed.

## Installation & Setup Workflow

When triggered by Videoflow installation requests, follow these steps.

### Step 1: Check If Skills Are Already Installed

Before installing, check if key bundle skills are already available:

1. Look for `civitai-videoflow` in available skills
2. Check whether previous videoflow-related runs succeeded

If the bundle appears installed, ask the user:

> I found that Civitai Videoflow skills appear to already be installed. Would you like me to:
> 1. Verify prerequisites and environment only (Recommended)
> 2. Reinstall the bundle to get the latest version
> 3. Skip setup and try using videoflow directly

If option 1, skip to Step 4.
If option 2, continue with installation.
If option 3, attempt use directly.

If the bundle is not available, ask for confirmation before installing:

> I will install the Civitai Videoflow bundle from `civitai-agent-skills`. This will:
> 1. Obtain the repository into `/tmp/civitai-agent-skills`
> 2. Install 8 skills in dependency-safe order
> 3. Verify required environment variables and runtime tools
> 4. Provide videoflow config and smoke-test guidance
>
> Installation usually takes 30-90 seconds. Proceed? (yes/no)

Wait for explicit confirmation before Step 2.

### Step 2: Obtain `civitai-agent-skills` Repository

Use git clone/pull by default, with HTTPS and zip fallback.

#### Option A: Git Clone (Default)

```bash
if [ -d "/tmp/civitai-agent-skills/.git" ]; then
    echo "Repository exists. Pulling latest changes..."
    cd /tmp/civitai-agent-skills && git pull
else
    echo "Cloning civitai-agent-skills repository..."
    rm -rf /tmp/civitai-agent-skills
    git clone git@github.com:feed-mob/civitai-agent-skills.git /tmp/civitai-agent-skills
fi
```

If SSH clone fails, use HTTPS:

```bash
rm -rf /tmp/civitai-agent-skills
git clone https://github.com/feed-mob/civitai-agent-skills.git /tmp/civitai-agent-skills
```

If both fail, continue with Option B.

#### Option B: Manual Zip Upload

Ask the user to provide a zip archive when git is unavailable.

> I could not fetch `civitai-agent-skills` using git. Please upload the repository zip, and I will extract it into `/tmp/civitai-agent-skills`.

Then run:

```bash
# Example uploaded file path (adjust if needed)
ZIP_PATH="/tmp/civitai-agent-skills.zip"

rm -rf /tmp/civitai-agent-skills
mkdir -p /tmp/civitai-agent-skills
unzip -q "$ZIP_PATH" -d /tmp/

if [ -d "/tmp/civitai-agent-skills-main" ]; then
  cp -R /tmp/civitai-agent-skills-main/. /tmp/civitai-agent-skills/
elif [ -d "/tmp/civitai-agent-skills" ]; then
  :
else
  echo "Could not find extracted civitai-agent-skills directory"
  exit 1
fi
```

Verify the expected skill directories exist:

```bash
ls /tmp/civitai-agent-skills/skills/civitai-videoflow
ls /tmp/civitai-agent-skills/skills/duomi-image-generator-skill
ls /tmp/civitai-agent-skills/skills/duomi-video-generation-skill
ls /tmp/civitai-agent-skills/skills/civitai-upload-assets-skill
ls /tmp/civitai-agent-skills/skills/civitai-post-skill
ls /tmp/civitai-agent-skills/skills/civitai-prompt-enhancer-skill
ls /tmp/civitai-agent-skills/skills/civitai-image-curator-skill
ls /tmp/civitai-agent-skills/skills/civitai-video-prompt-enhancer-skill
```

### Step 3: Install Skills Using `npx`

Install all 8 skills in this order:

1. `duomi-image-generator-skill`
2. `duomi-video-generation-skill`
3. `civitai-upload-assets-skill`
4. `civitai-post-skill`
5. `civitai-prompt-enhancer-skill`
6. `civitai-image-curator-skill`
7. `civitai-video-prompt-enhancer-skill`
8. `civitai-videoflow`

First set `AGENT_NAME`:

```bash
AGENT_NAME="opencode"  # or codex / claude-code / openclaw
```

Install commands:

```bash
npx skills add /tmp/civitai-agent-skills --skill duomi-image-generator-skill --agent "$AGENT_NAME" -y
npx skills add /tmp/civitai-agent-skills --skill duomi-video-generation-skill --agent "$AGENT_NAME" -y
npx skills add /tmp/civitai-agent-skills --skill civitai-upload-assets-skill --agent "$AGENT_NAME" -y
npx skills add /tmp/civitai-agent-skills --skill civitai-post-skill --agent "$AGENT_NAME" -y
npx skills add /tmp/civitai-agent-skills --skill civitai-prompt-enhancer-skill --agent "$AGENT_NAME" -y
npx skills add /tmp/civitai-agent-skills --skill civitai-image-curator-skill --agent "$AGENT_NAME" -y
npx skills add /tmp/civitai-agent-skills --skill civitai-video-prompt-enhancer-skill --agent "$AGENT_NAME" -y
npx skills add /tmp/civitai-agent-skills --skill civitai-videoflow --agent "$AGENT_NAME" -y
```

Progress messages to share while running:

- `[1/8] Installing duomi-image-generator-skill...`
- `[2/8] Installing duomi-video-generation-skill...`
- `[3/8] Installing civitai-upload-assets-skill...`
- `[4/8] Installing civitai-post-skill...`
- `[5/8] Installing civitai-prompt-enhancer-skill...`
- `[6/8] Installing civitai-image-curator-skill...`
- `[7/8] Installing civitai-video-prompt-enhancer-skill...`
- `[8/8] Installing civitai-videoflow...`

If installation fails, capture and report the command error. Common causes:

- wrong skill path under `/tmp/civitai-agent-skills/skills/`
- missing `npx` / broken Node installation
- permission issues in local skills directory

### Step 4: Verify Environment and Runtime Prerequisites

This installer performs verification and guidance only. It does not auto-run dependency bootstrap steps.

#### Verify Required Environment Variables

Required variables:

- `CIVITAI_RECORDS_DATABASE_URL`
- `DUOMI_API_TOKEN`
- `IMAGEKIT_PRIVATE_KEY`

Recommended variable:

- `CIVITAI_ACCOUNT`

Presence-only checks:

```bash
[ -n "$CIVITAI_RECORDS_DATABASE_URL" ] && echo "OK CIVITAI_RECORDS_DATABASE_URL is set" || echo "MISSING CIVITAI_RECORDS_DATABASE_URL"
[ -n "$DUOMI_API_TOKEN" ] && echo "OK DUOMI_API_TOKEN is set" || echo "MISSING DUOMI_API_TOKEN"
[ -n "$IMAGEKIT_PRIVATE_KEY" ] && echo "OK IMAGEKIT_PRIVATE_KEY is set" || echo "MISSING IMAGEKIT_PRIVATE_KEY"
[ -n "$CIVITAI_ACCOUNT" ] && echo "OK CIVITAI_ACCOUNT is set" || echo "WARN CIVITAI_ACCOUNT is not set"
```

Do not print token values.

#### Verify Required Tools

```bash
python --version
node --version
npm --version
npx --version
jq --version
agent-browser --version
```

If a tool is missing, report what is missing and provide next-step install guidance only.

### Step 5: Validate Videoflow Config Hints

Check whether the working project has `videoflow.yaml`.

If missing, suggest creating it from the template in the source repository:

```bash
cp /tmp/civitai-agent-skills/skills/civitai-videoflow/videoflow.example.yaml ./videoflow.yaml
```

Then ask the user to confirm/update at least:

- `image_generation_skill: duomi-image-generator-skill`
- `video_generation_skill: duomi-video-generation-skill`
- `upload_skill: civitai-upload-assets-skill`
- optional creative and publish skill keys
- `creator` and `civitai_account`

### Step 6: Final Verification and Smoke Test

After install and checks complete, guide the user:

1. Restart terminal/agent session if env vars were newly added.
2. In a project with `videoflow.yaml`, run a lightweight command:

```bash
# Status check for existing run
VF="./skills/civitai-videoflow/scripts/videoflow"
$VF list --pending

# Optional small test (no enhancement path)
$VF start test-run "simple cinematic scene" --no-enhance
```

If they use OpenCode commands, they can run `/videoflow-generate "prompt"` after setup.

### Step 7: Provide the Run Prompt Template

After successful installation and verification, share this exact prompt so the user can execute the full flow correctly:

```text
Use civitai-videoflow skill to run the full video generation pipeline and publish to Civitai.

Prompt: $ARGUMENTS
```

## Quick Reference

### Agent-Specific Install Commands

```bash
# OpenCode
npx skills add /tmp/civitai-agent-skills --skill duomi-image-generator-skill --agent opencode -y
npx skills add /tmp/civitai-agent-skills --skill duomi-video-generation-skill --agent opencode -y
npx skills add /tmp/civitai-agent-skills --skill civitai-upload-assets-skill --agent opencode -y
npx skills add /tmp/civitai-agent-skills --skill civitai-post-skill --agent opencode -y
npx skills add /tmp/civitai-agent-skills --skill civitai-prompt-enhancer-skill --agent opencode -y
npx skills add /tmp/civitai-agent-skills --skill civitai-image-curator-skill --agent opencode -y
npx skills add /tmp/civitai-agent-skills --skill civitai-video-prompt-enhancer-skill --agent opencode -y
npx skills add /tmp/civitai-agent-skills --skill civitai-videoflow --agent opencode -y

# Codex
npx skills add /tmp/civitai-agent-skills --skill duomi-image-generator-skill --agent codex -y
npx skills add /tmp/civitai-agent-skills --skill duomi-video-generation-skill --agent codex -y
npx skills add /tmp/civitai-agent-skills --skill civitai-upload-assets-skill --agent codex -y
npx skills add /tmp/civitai-agent-skills --skill civitai-post-skill --agent codex -y
npx skills add /tmp/civitai-agent-skills --skill civitai-prompt-enhancer-skill --agent codex -y
npx skills add /tmp/civitai-agent-skills --skill civitai-image-curator-skill --agent codex -y
npx skills add /tmp/civitai-agent-skills --skill civitai-video-prompt-enhancer-skill --agent codex -y
npx skills add /tmp/civitai-agent-skills --skill civitai-videoflow --agent codex -y

# Claude Code
npx skills add /tmp/civitai-agent-skills --skill duomi-image-generator-skill --agent claude-code -y
npx skills add /tmp/civitai-agent-skills --skill duomi-video-generation-skill --agent claude-code -y
npx skills add /tmp/civitai-agent-skills --skill civitai-upload-assets-skill --agent claude-code -y
npx skills add /tmp/civitai-agent-skills --skill civitai-post-skill --agent claude-code -y
npx skills add /tmp/civitai-agent-skills --skill civitai-prompt-enhancer-skill --agent claude-code -y
npx skills add /tmp/civitai-agent-skills --skill civitai-image-curator-skill --agent claude-code -y
npx skills add /tmp/civitai-agent-skills --skill civitai-video-prompt-enhancer-skill --agent claude-code -y
npx skills add /tmp/civitai-agent-skills --skill civitai-videoflow --agent claude-code -y

# OpenClaw
npx skills add /tmp/civitai-agent-skills --skill duomi-image-generator-skill --agent openclaw -y
npx skills add /tmp/civitai-agent-skills --skill duomi-video-generation-skill --agent openclaw -y
npx skills add /tmp/civitai-agent-skills --skill civitai-upload-assets-skill --agent openclaw -y
npx skills add /tmp/civitai-agent-skills --skill civitai-post-skill --agent openclaw -y
npx skills add /tmp/civitai-agent-skills --skill civitai-prompt-enhancer-skill --agent openclaw -y
npx skills add /tmp/civitai-agent-skills --skill civitai-image-curator-skill --agent openclaw -y
npx skills add /tmp/civitai-agent-skills --skill civitai-video-prompt-enhancer-skill --agent openclaw -y
npx skills add /tmp/civitai-agent-skills --skill civitai-videoflow --agent openclaw -y
```

### Environment Presence Checks

```bash
[ -n "$CIVITAI_RECORDS_DATABASE_URL" ] && echo "OK CIVITAI_RECORDS_DATABASE_URL" || echo "MISSING CIVITAI_RECORDS_DATABASE_URL"
[ -n "$DUOMI_API_TOKEN" ] && echo "OK DUOMI_API_TOKEN" || echo "MISSING DUOMI_API_TOKEN"
[ -n "$IMAGEKIT_PRIVATE_KEY" ] && echo "OK IMAGEKIT_PRIVATE_KEY" || echo "MISSING IMAGEKIT_PRIVATE_KEY"
[ -n "$CIVITAI_ACCOUNT" ] && echo "OK CIVITAI_ACCOUNT" || echo "WARN CIVITAI_ACCOUNT"
```

## Troubleshooting Checklist

```bash
# 1) unzip availability (for zip fallback)
unzip -v

# 2) source repository and skill paths
ls -la /tmp/civitai-agent-skills
ls -la /tmp/civitai-agent-skills/skills

# 3) npx availability
npx --version

# 4) check required skill directories
ls -la /tmp/civitai-agent-skills/skills/duomi-image-generator-skill
ls -la /tmp/civitai-agent-skills/skills/duomi-video-generation-skill
ls -la /tmp/civitai-agent-skills/skills/civitai-upload-assets-skill
ls -la /tmp/civitai-agent-skills/skills/civitai-post-skill
ls -la /tmp/civitai-agent-skills/skills/civitai-prompt-enhancer-skill
ls -la /tmp/civitai-agent-skills/skills/civitai-image-curator-skill
ls -la /tmp/civitai-agent-skills/skills/civitai-video-prompt-enhancer-skill
ls -la /tmp/civitai-agent-skills/skills/civitai-videoflow

# 5) if install fails, rerun with explicit agent
AGENT_NAME="opencode"
npx skills add /tmp/civitai-agent-skills --skill civitai-videoflow --agent "$AGENT_NAME" -y
```

If `agent-browser` is missing, instruct the user to install it before using publish workflows.

If `videoflow.example.yaml` is not found at repo root, use:

```bash
cp /tmp/civitai-agent-skills/skills/civitai-videoflow/videoflow.example.yaml ./videoflow.yaml
```

## Notes

- Skills install into the selected agent skills directory.
- Source repository is staged at `/tmp/civitai-agent-skills` during installation.
- This skill verifies environment/tool readiness but does not auto-install optional dependencies.
- Restart terminal/agent session after adding environment variables to shell config files.
- Keep tokens secure and never commit secrets to version control.
