---
name: Articulate
description: Structure raw ideas into articulate outlines using Dan Koe's frameworks. USE WHEN articulate, structure ideas, outline talk, outline article, think through piece, brainstorm structure, how should I say this, organize my thoughts, structure this post, help me outline.
---

# Articulate

Upstream thinking layer that takes messy ideas and gives them structure. Does NOT produce final prose — outputs structured outlines with framework labels and section suggestions. Hands off to format-specific skills (XPoster, WriteStory, etc.) for final output.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/PAI/USER/SKILLCUSTOMIZATIONS/Articulate/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there.

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the Articulate skill"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **Articulate** skill...
   ```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Structure** | "articulate this", "structure this", "outline this", "help me think through", "organize my thoughts", raw brain dump input | `Workflows/Structure.md` |
| **GreatestHits** | "update my hits", "add to greatest hits", "what are my big ideas", "manage hits" | `Workflows/GreatestHits.md` |
| **Sharpen** | "sharpen this", "is this articulate", "pressure test this piece", "review structure" | `Workflows/Sharpen.md` |

## Quick Reference

- **3 Frameworks:** Micro Story (short-form), Pyramid Principle (talks/slides), Cross-Domain Synthesis (long-form articles)
- **8 Idea Legos:** Pain point, Example, Personal story, Statistic, Metaphor, Quote, Reframe, What/How/Why
- **Greatest Hits:** Your 8-10 signature ideas stored in `GreatestHits.json`

**Full Documentation:**
- Frameworks: Read `Frameworks.md` for the three articulation methods
- Building blocks: Read `IdeaLegos.md` for section expansion tools
- Your big ideas: Read `GreatestHits.json` for connections to current topic
