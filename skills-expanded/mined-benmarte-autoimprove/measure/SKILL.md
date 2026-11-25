---
description: Run the full measurement suite defined in .claude/autoimprove/config.md and report the current codebase quality score (0-100). Use this to check your baseline before running the improve loop, or to spot-check at any time.
---

# Measure Skill

Run the project's quality measurement suite and report the composite score.

## Steps

1. Read `.claude/autoimprove/config.md`. If it doesn't exist, say: "Run /autoimprove:setup first."

2. Run each command defined in the config's measurement sections, in order:
   - Type check / compile
   - Build
   - Tests
   - Lint

3. Parse results using the error patterns and success patterns defined in the config.

4. Calculate composite score using the weights in the config.

5. Report:

```
📊 Codebase Quality Score: XX/100

  [Type check label]:  X errors  → XX/40 pts
  [Build label]:       ✅/❌      → XX/20 pts
  [Test label]:        X/X pass  → XX/30 pts
  [Lint label]:        X errors  → XX/10 pts

💡 Lowest area: [label] — [one specific actionable suggestion]
```

6. If any command fails unexpectedly (not just returns errors but actually crashes), report the raw output so the user can debug their tooling.
