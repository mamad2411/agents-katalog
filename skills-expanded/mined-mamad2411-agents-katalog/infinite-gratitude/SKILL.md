---
name: infinite-gratitude
description: Multi-agent research that keeps bringing gifts back — like cats! Dispatch multiple agents to research a topic in parallel, compile findings, and iterate on new discoveries.
argument-hint: "<topic>" [--depth quick|normal|deep] [--agents 1-10]
---

# Infinite Gratitude 🐾

> 無限貓報恩 | 無限の恩返し
> Multi-agent research that keeps bringing gifts back — like cats! 🐱

## Quick Reference

| Option | Values | Default |
|--------|--------|---------|
| `topic` | Required | - |
| `--depth` | quick / normal / deep | normal |
| `--agents` | 1-10 | 5 |

## Usage

```bash
/infinite-gratitude "pet AI recognition"
/infinite-gratitude "RAG best practices" --depth deep
/infinite-gratitude "React state management" --agents 3
```

## Behavior

### Step 1: Split Directions
Split `{topic}` into 5 parallel research directions:
1. GitHub projects
2. HuggingFace models
3. Papers / articles
4. Competitors
5. Best practices

### Step 2: Dispatch Agents
```
Task(
    prompt="Research {direction} for {topic}...",
    subagent_type="research-scout",
    model="haiku",
    run_in_background=True
)
```

### Step 3: Collect Gifts
Compile all findings into structured report.

### Step 4: Loop
If follow-up questions exist → Ask user → Continue? → Back to Step 2

### Step 5: Final Report

## Example Output

```
🐾 Infinite Gratitude!

📋 Topic: "pet AI recognition"
🐱 Dispatching 5 agents...

━━━━━━━━━━━━━━━━━━━━━━
🎁 Wave 1
━━━━━━━━━━━━━━━━━━━━━━

🐱 GitHub: MegaDescriptor, wildlife-datasets...
🐱 HuggingFace: DINOv2, CLIP...
🐱 Papers: Petnow uses Siamese Network...
🐱 Competitors: Petnow 99%...
🐱 Tutorials: ArcFace > Triplet Loss...

💡 Key: Data volume is everything!

🔍 New questions:
   - How to implement ArcFace?
   - How to use MegaDescriptor?

Continue? (y/n)

🐾 by washinmura.jp
```

## Notes

- Uses `haiku` model to save cost
- Max 5 agents per wave
- Deep mode loops until satisfied

## Additional Resources

- For agent configuration, see [references/agent-config.md](references/agent-config.md)

## Related Skills

- **ai-dojo** — Foundation for AI coding agents
- **research-scout** — Single-agent research

---

*Part of 🥋 AI Dojo Series by [Washin Village](https://washinmura.jp) 🐾*
