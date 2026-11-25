---
name: gpt-import
description: Import and distill leaked GPT prompts from linexjlin/GPTs into agent knowledge files. Fetches directly from GitHub, distills domain knowledge via agent-refine-knowledge, logs source to claude-secrets catalog.
invocation: /gpt-import
argument-hint: "<agent-id> [--gpt=<gpt-name>] [--search=<query>]"
---

# /gpt-import — GPT Knowledge Importer

## Usage
/gpt-import <agent-id>
/gpt-import <agent-id> --gpt=logo-creator
/gpt-import <agent-id> --search=seo

## What this skill does

Fetches leaked custom GPT instructions from `linexjlin/GPTs` GitHub repo and distills
the domain knowledge into the agent's knowledge/ directory.

## Execution steps

1. **Resolve agent** — Find agent by ID or name in `~/Projects/claude-config/config/agent-registry.json`.
   Get agent's category and capabilities.

2. **Browse available GPTs** — Fetch file list from GitHub API:
   ```bash
   gh api repos/linexjlin/GPTs/contents/prompts --jq '.[].name' 2>/dev/null
   ```
   If `--gpt=<name>` specified: fetch that specific file directly.
   If `--search=<query>`: filter list by query, show top 10 matches to user.
   Otherwise: show list filtered by agent's category keywords, ask user to pick.

3. **Fetch selected GPT content**:
   ```bash
   gh api repos/linexjlin/GPTs/contents/prompts/<filename> --jq '.content' | base64 -d
   ```

4. **Distill** — Call `/agent-refine-knowledge` skill with:
   - Agent ID
   - The fetched GPT content as additional source material
   - Instruction: "Extract only domain knowledge and methodology. Remove all OpenAI/GPT-specific instructions, tool calls, DALL-E references, tone/personality, and proprietary integrations. Output as model-agnostic knowledge topic."

5. **Write to knowledge/** — The refine skill writes to agent's knowledge/ dir.

6. **Log to sources catalog** — Append entry to `~/Projects/claude-secrets/sources-catalog.md`
   (or wherever it was created):
   ```
   | <date> | <agent-id> | <gpt-name> | https://github.com/linexjlin/GPTs/blob/main/prompts/<filename> | distilled |
   ```

7. **Report** — Show user: agent updated, which GPT was source, what topic was added to knowledge/.

## Rules
- Never store raw GPT content in knowledge files
- Never add OpenAI/GPT-specific instructions to agent files
- Always log source to catalog (even if distill quality is low)
- If GPT content is mostly roleplay/personality with no domain knowledge → report "low value, skipped"
