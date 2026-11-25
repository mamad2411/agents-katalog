---
name: cross-verify
description: AI cross-verification skill that compares answers from Codex, Gemini, and Claude. Activated by requests like "cross verify", "cross check", "ask other AIs too", "multi AI comparison".
---

# AI Cross-Verification Skill

Collects and cross-verifies answers from Codex CLI, Gemini CLI, and Claude (Lead) on a given question, then synthesizes a comprehensive analysis.

## Prerequisites

At least one of the following CLI tools must be installed:
- **Codex CLI**: `npm install -g @openai/codex`
- **Gemini CLI**: `npm install -g @anthropic-ai/gemini` or via Google's official installation

## Workflow

### Phase 1: Prompt Preparation

1. Extract the question/task to verify from the user's request
2. If code-related, automatically gather context:
   - `git diff` (if there are changes)
   - Relevant file contents
   - Project structure
3. Compose the prompt for each agent:
   - Question body
   - Gathered context
   - Instruction to respond in the user's language

### Phase 2: CLI Availability Check

Before spawning agents, check which CLIs are available:

```bash
which codex 2>/dev/null && echo "CODEX_OK" || echo "CODEX_NOT_FOUND"
which gemini 2>/dev/null && echo "GEMINI_OK" || echo "GEMINI_NOT_FOUND"
```

- Both unavailable: inform the user that at least one CLI (codex or gemini) is required and stop
- One available: proceed with 2-model comparison (available CLI + Claude)
- Both available: proceed with 3-model comparison

### Phase 3: Agent Spawn

#### Preferred: Agent Teams (parallel execution)

Try creating a team first:

```
TeamCreate(team_name: "cross-verify", description: "AI cross-verification")
```

If TeamCreate fails (Agent Teams not enabled):
1. Display: "Agent Teams requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in your settings.json env. Would you like me to enable it?"
2. If user declines, fall back to sequential Agent spawn (see below)

On success, spawn agents in **a single message** (parallel):

Codex reviewer (only if codex is available):
```
Agent(
  description: "Run Codex CLI analysis",
  prompt: "<composed prompt with context>",
  name: "codex-reviewer",
  subagent_type: "codex-reviewer",
  team_name: "cross-verify",
  model: "haiku",
  mode: "dontAsk"
)
```

Gemini reviewer (only if gemini is available):
```
Agent(
  description: "Run Gemini CLI analysis",
  prompt: "<composed prompt with context>",
  name: "gemini-reviewer",
  subagent_type: "gemini-reviewer",
  team_name: "cross-verify",
  model: "haiku",
  mode: "dontAsk"
)
```

#### Fallback: Sequential Agent spawn

If Teams is not available, spawn agents sequentially with `run_in_background: true`:

```
Agent(
  description: "Run Codex CLI analysis",
  prompt: "<composed prompt>",
  name: "codex-reviewer",
  subagent_type: "codex-reviewer",
  model: "haiku",
  mode: "dontAsk",
  run_in_background: true
)
```

#### Lead (Claude) Analysis

While agents are working, the Lead performs its own analysis on the same question.

### Phase 4: Synthesis

After receiving all results, synthesize in this format:

```markdown
## Cross-Verification Results

### Consensus (all models agree)
- High-confidence conclusions

### Unique Insights
- **Codex (GPT)**: Findings unique to this model
- **Gemini**: Findings unique to this model
- **Claude**: Findings unique to this model

### Conflicts (disagreements)
- Per item: each model's position + Lead's judgment

### Final Conclusion
- Synthesized recommendation
```

### Phase 5: Cleanup

After output, send shutdown to teammates:
```
SendMessage(to: "codex-reviewer", message: {type: "shutdown_request"})
SendMessage(to: "gemini-reviewer", message: {type: "shutdown_request"})
```

## Error Handling

| Scenario | Action |
|----------|--------|
| CLI not installed | Skip that model, proceed with remaining |
| API error (ModelNotFoundError, etc.) | Skip that model, note in results |
| Timeout (agent doesn't respond) | Synthesize with available results |
| Both CLIs fail | Compare Lead analysis against error context |
| TeamCreate fails | Show activation guide, fallback to sequential Agent |

## Prompt Composition Rules

| Request Type | Context to Include |
|-------------|-------------------|
| Code review | git diff + relevant file contents |
| Architecture question | Project structure + key config files |
| Bug analysis | Error logs + related code |
| General technical question | Question only |
