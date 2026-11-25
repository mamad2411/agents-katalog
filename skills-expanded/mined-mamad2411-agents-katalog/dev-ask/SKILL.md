---
name: dev-ask
description: Advisory router — query Claude, Codex, or Gemini for a quick second opinion. Experimental — only Claude is guaranteed available; other models require dev-mcp-setup configuration.
---

# Dev Ask

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

**EXPERIMENTAL.** Quick advisory query to a specific LLM (Claude, Codex, Gemini) for a second opinion. Different from `dev-ccg` which runs all three in parallel — `dev-ask` is single-shot.

## Use When
- You want a fast second opinion from a specific model
- Comparing how different models approach the same problem
- Validating Claude's answer against another model

## Do Not Use When
- Need consensus across models → use `dev-ccg`
- Just need an answer → ask the active session directly
- Codex/Gemini APIs not configured → only Claude available, fall back

## Workflow

1. **Pick the target model:** `claude` | `codex` | `gemini`
2. **Format the question** model-agnostically
3. **Send** via the appropriate API
4. **Return** the answer with the model's name attached
5. Optional: save to `workspace/development/research/[C]ask-{topic}-{date}.md`

## Configuration

| Model | Required setup |
|---|---|
| Claude | Native — always available |
| Codex | OpenAI API key configured via `dev-mcp-setup` |
| Gemini | Google API key configured via `dev-mcp-setup` |

If a target model isn't configured, the skill warns:
> "{model} is not configured. Only Claude is currently available. Configure via `dev-mcp-setup` or use `dev-ccg` to compare available models."

## Output Format

```markdown
## Ask — {target model}

### Question
{question}

### Answer (from {model})
{answer}

### Note
[Any caveats — model version, response time, confidence, etc.]
```

## Pairs With
- `dev-ccg` (multi-model parallel)
- `dev-mcp-setup` (configures non-Claude APIs)
- `@apex-architect` (often the consumer of multi-model perspectives)
