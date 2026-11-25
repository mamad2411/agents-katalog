---
name: strategic-compact
description: Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction.
---

# Strategic Compact Skill

Suggests manual context compaction at strategic points in your workflow.

## Why Strategic Compaction?

Auto-compaction triggers at arbitrary points:
- Often mid-task, losing important context
- No awareness of logical task boundaries
- Can interrupt complex multi-step operations

Strategic compaction at logical boundaries:
- **After exploration, before execution** - Compact research context, keep implementation plan
- **After completing a milestone** - Fresh start for next phase
- **Before major context shifts** - Clear exploration context before different task

## Logical Compaction Points

### Good Times to Compact

1. **After planning, before implementation**
   - Plan is finalized and clear
   - Exploration context no longer needed
   - Implementation requires fresh space

2. **After completing a feature**
   - Tests passing, code reviewed
   - Ready to move to next task
   - Previous context no longer relevant

3. **After debugging session**
   - Bug fixed and verified
   - Error-resolution context can be discarded
   - Ready for new work

4. **Before major context shift**
   - Switching from frontend to backend
   - Moving to different feature area
   - Changing task type entirely

### Bad Times to Compact

1. **Mid-implementation**
   - Losing track of what's done vs. pending
   - Missing important context about approach

2. **During debugging**
   - Need full error context
   - Previous attempts inform next steps

3. **While iterating on feedback**
   - User corrections still relevant
   - Context about requirements needed

## Threshold Guidelines

Track tool calls and consider compaction:
- **50+ tool calls**: Consider if at logical boundary
- **75+ tool calls**: Strongly consider compaction
- **100+ tool calls**: Find next logical point to compact

## Best Practices

1. **Compact after planning** - Once plan is finalized, compact to start fresh
2. **Compact after debugging** - Clear error-resolution context before continuing
3. **Don't compact mid-implementation** - Preserve context for related changes
4. **Create checkpoints first** - Save important state before compaction
