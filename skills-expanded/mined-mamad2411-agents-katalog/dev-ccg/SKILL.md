---
name: dev-ccg
description: Tri-model orchestration — run the same task through Claude + Codex + Gemini in parallel and synthesize the best answer. Use for high-stakes decisions where multi-model consensus reduces single-model bias.
---

# Dev CCG (Claude + Codex + Gemini)

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

**EXPERIMENTAL.** Tri-model orchestration: run the same prompt through Claude, Codex (OpenAI Codex / GPT-Code), and Gemini in parallel, then synthesize the best answer.

> **Note:** This skill assumes external API access to Codex and Gemini, which may or may not be configured in EvoNexus. If only Claude is available, the skill degrades to single-model mode and warns the user.

## Use When
- High-stakes decision where single-model bias is a real concern
- Architectural choice where you want multiple LLMs' perspectives
- Code review where you want adversarial multi-model agreement

## Do Not Use When
- Routine work — single model is fine
- API access to Codex/Gemini is not configured
- The task requires real-time iteration (CCG is slow)

## Workflow

1. **Format the prompt** — make it model-agnostic (no Claude-specific syntax)
2. **Spawn in parallel:**
   - Claude (current session, native)
   - Codex (via OpenAI API, if configured)
   - Gemini (via Google API, if configured)
3. **Collect responses**
4. **Synthesize:**
   - Where do they agree? → high confidence
   - Where do they disagree? → flag for human review
   - Combine the strongest reasoning from each
5. Save to `workspace/development/research/[C]ccg-{topic}-{date}.md`

## Output

```markdown
## CCG Synthesis — {topic}

### Models Consulted
- ✅ Claude (Opus 4.6)
- ✅ Codex (gpt-code-X)
- ✅ Gemini (gemini-Y)

### Agreement Zones
- All three agree on: {points}

### Disagreement Zones
- Claude says X
- Codex says Y
- Gemini says Z
- → Flagged for human review

### Synthesized Answer
[Combined reasoning, marking uncertainty zones]
```

## Pairs With
- `@apex-architect` (for high-stakes architectural decisions)
- `@raven-critic` (for adversarial cross-validation)

## Configuration

If Codex/Gemini APIs are not configured, this skill warns:
> "CCG requires Codex and Gemini API access. Currently only Claude is available — falling back to single-model mode. Configure via `dev-mcp-setup` if needed."
