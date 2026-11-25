---
name: math-calculate
description: "Evaluate mathematical expressions using command-line tools."
metadata:
  openclaw:
    emoji: "🧮"
---

# Math Calculate

Evaluate mathematical expressions.

## Calculate

```bash
# Basic arithmetic
echo "scale=4; 355/113" | bc

# Complex expressions
echo "scale=10; sqrt(2)" | bc -l

# Percentage
echo "scale=2; 75 * 100 / 200" | bc
```

## Tips for AI Agents

- Use `bc -l` for the math library (trig functions, sqrt, etc.).
- Set `scale=N` for decimal precision.
- Use `awk` for quick inline math: `awk 'BEGIN{print 2^10}'`.
