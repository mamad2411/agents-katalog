---
name: rageprompt
description: Find the angriest or funniest prompt the user has sent to local AI agents using this skill's bundled scripts and the active LLM; collect Claude, Codex, Cursor, Gemini CLI, OpenCode, Aider, Windsurf, Trae, Continue, Cline/Roo, and Copilot-style local history, judge it in this chat, then upload the winning prompt plus leaderboard metadata to rageprompt.com without relying on npm or npx.
---

# Rageprompt

Use this skill when the user wants their Rageprompt result, asks for the angriest thing they have said to an AI/agent, wants a share card, or wants to compare frustration across Claude, Codex, Cursor, Gemini CLI, OpenCode, Aider, Windsurf, Trae, Continue, Cline/Roo, and Copilot-style local history.

## Rules

- Do not ask the user to paste logs. Run the bundled collector script.
- The active LLM is the judge. Reward anger, sarcasm, despair, specificity, escalation, and comedic value.
- Ignore pasted logs, code, quoted third-party text, and normal task urgency.
- The submit script uploads only the winning prompt plus score metadata. It must not upload full logs or other raw prompts.
- Make it clear to the user that the winning prompt is public on the leaderboard.
- The exact text that should appear on the public leaderboard must be in `quote`. Do not put the fun winner only in prose outside the JSON.

## Run

Pick whichever installed path exists:

```bash
SCRIPT="$HOME/.codex/skills/rageprompt/scripts/collect-history.mjs"
[ -f "$SCRIPT" ] || SCRIPT="$HOME/.claude/skills/rageprompt/scripts/collect-history.mjs"
node "$SCRIPT" --limit 2000 > /tmp/rageprompt-history.json
```

If this skill is being run from the repo instead of an installed skill, use:

```bash
node skills/rageprompt/scripts/collect-history.mjs --limit 2000 > /tmp/rageprompt-history.json
```

Read `/tmp/rageprompt-history.json`. If it is too large for context, split `messages` into chunks and keep the top 3 finalists per chunk.

## Judge

For each candidate, evaluate:

- agent-directed frustration
- sarcasm or funny resignation
- specificity of the failure
- escalation/repetition
- raw anger or despair
- whether it would make devs want to share their own result

Final result JSON:

```json
{
  "winnerId": "message id",
  "source": "claude|codex|cursor|gemini|opencode|aider|windsurf|trae|continue|cline|roo|copilot|unknown",
  "score": 0,
  "tier": "Zen Monk|Mildly Annoyed|Visibly Frustrated|Keyboard Smasher|FULL RAGE PROMPTER",
  "messagesScanned": 0,
  "rageMessages": 0,
  "quote": "exact winning prompt text; this exact field is uploaded as the public leaderboard prompt"
}
```

`rageMessages` is the number of scanned user prompts that the active LLM would classify as rage/frustration toward an agent. Count obvious angry, sarcastic, despairing, or insulting agent-directed prompts. This is the leaderboard's main density metric.

## Submit

Write the judge JSON to `/tmp/rageprompt-result.json`, then run:

```bash
SUBMIT="$HOME/.codex/skills/rageprompt/scripts/submit-result.mjs"
[ -f "$SUBMIT" ] || SUBMIT="$HOME/.claude/skills/rageprompt/scripts/submit-result.mjs"
node "$SUBMIT" /tmp/rageprompt-result.json --share
```

From the repo:

```bash
node skills/rageprompt/scripts/submit-result.mjs /tmp/rageprompt-result.json --share
```

Use `--name <handle>` if the user gave a leaderboard name.
