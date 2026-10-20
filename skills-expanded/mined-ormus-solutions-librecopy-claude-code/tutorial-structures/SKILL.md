---
name: "tutorial-structures"
description: "Tutorial structure frameworks: the tutorial spectrum, Diátaxis, structure patterns (build, fix, compare, migrate), step design rules, checkpoint design, and time estimation. Use when designing a tutorial's overall shape."
---

# Tutorial Structures

> Pedagogical patterns and frameworks for creating effective technical tutorials.

## Knowledge Base

### The Tutorial Spectrum

Tutorials exist on a spectrum between two extremes:

| Recipe | Concept Guide |
|--------|--------------|
| "Do exactly this" | "Understand this idea" |
| Step-by-step | Explanation-heavy |
| Fast to complete | Deep understanding |
| Low retention | High retention |

The best tutorials blend both: steps for doing, explanations for understanding.

### Diataxis Framework

Technical documentation falls into four quadrants. Tutorials live in one:

| | Learning | Working |
|---|---------|---------|
| **Practical** | **Tutorial** (learning-oriented) | How-to Guide (task-oriented) |
| **Theoretical** | Explanation (understanding-oriented) | Reference (information-oriented) |

A tutorial is NOT a how-to guide. Tutorials teach; how-to guides assume knowledge and provide procedures.

### Tutorial Structure Patterns

**The Build Pattern** (most common):
1. Show the end result
2. Set up the environment
3. Build the thing step by step
4. Verify it works
5. Explain what to explore next

**The Fix Pattern** (debugging tutorials):
1. Present the broken state
2. Diagnose the problem
3. Apply the fix
4. Verify the fix
5. Explain why it was broken

**The Compare Pattern** (choosing between approaches):
1. Define the problem
2. Show approach A
3. Show approach B
4. Compare tradeoffs
5. Recommend based on criteria

**The Migrate Pattern** (upgrade tutorials):
1. Show the old way
2. Explain why it changed
3. Show the new way
4. Highlight differences
5. Provide automated migration steps

### Step Design Rules

1. **Atomic Steps**: One action per step. If a step has "and" in it, split it.
2. **Verifiable Steps**: Every step should have observable output. The learner must know it worked.
3. **Reversible Steps**: If a step can fail, explain how to undo it and try again.
4. **Numbered Steps**: Use numbers, not bullets. Order matters. Learners track progress by step number.
5. **Context Sentences**: Before each step, one sentence explaining why. After each step, one sentence confirming what happened.

### Checkpoint Design

Place checkpoints after every 3-5 steps or after each major section:

```markdown
#### Checkpoint

At this point, your project should have:
- [ ] A `package.json` with express and typescript as dependencies
- [ ] A `tsconfig.json` with strict mode enabled
- [ ] A `src/index.ts` that starts a server on port 3000

Test it: run `npm run dev` and visit http://localhost:3000.
You should see "Hello, World!" in your browser.

If something is not working, compare your code with the
[checkpoint-1 branch](link) in the tutorial repository.
```

### Time Estimation

| Activity | Time Per Unit |
|----------|--------------|
| Install a tool | 2-3 minutes |
| Create a file and write code | 3-5 minutes |
| Run a command and check output | 1-2 minutes |
| Read an explanation paragraph | 1 minute |
| Debug a common issue | 3-5 minutes |

Total tutorial time = sum of steps + 20% buffer for reading.

## Patterns

1. **Show the Destination**: Always show what the finished product looks like before starting. Motivation sustains effort.
2. **Working at Every Step**: The project should be runnable (even if incomplete) after each section. Never leave the learner in a broken state between sections.
3. **Minimal Viable Step**: Each step adds the minimum code/config to accomplish one thing. Do not add error handling, logging, or polish until a dedicated "polish" section.
4. **Escape Hatches**: Provide a reference repository with branches for each checkpoint. Learners who get lost can reset and continue.
5. **Celebrate Progress**: After each section, acknowledge what was accomplished. "You now have a working API with three endpoints."

## Anti-Patterns

1. **The Wall of Code**: Dropping a 50-line code block and saying "add this to your file." Break it into pieces, explain each piece.
2. **The Magic Step**: "Run this command" without explaining what it does. Every command needs at least one sentence of context.
3. **The Prerequisites Lie**: Saying "basic JavaScript knowledge" when the tutorial uses async generators, Proxy objects, and WeakMaps.
4. **The Abandoned Learner**: No troubleshooting notes. If the learner hits an error, they are on their own.
5. **The Scope Creep**: Starting with "Build a todo app" and ending with OAuth2, real-time sync, and Kubernetes deployment.
6. **The Stale Tutorial**: Code examples that use deprecated APIs or outdated package versions. Pin versions and note the date.

## References

- [Diataxis Framework](https://diataxis.fr/)
- [The Documentation System](https://documentation.divio.com/)
- [Write the Docs - Tutorials](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/)
- [Bloom's Taxonomy](https://en.wikipedia.org/wiki/Bloom%27s_taxonomy)
