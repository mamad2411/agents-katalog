---
name: comprehend
description: Walk through code line-by-line before using it. Prevents "copy-paste without comprehension" anti-pattern. Use when you receive AI-generated code or copy from Stack Overflow.
---

# Comprehend

If you can't explain it, you can't debug it.

**Copy-paste without comprehension is the most common anti-pattern** for AI-assisted coding. This skill ensures you understand code before using it.

## When to Use

Run `/comprehend` when:
- You receive AI-generated code (from Claude, ChatGPT, Copilot, etc.)
- You're about to copy-paste from Stack Overflow
- You're using code from a tutorial or blog post
- Code "works" but you don't know why
- You're modifying code you didn't write
- You feel uncertain about what code does

## The Comprehension Process

### Step 1: Read Through Once

Read the entire code block without stopping. Get a general sense of:
- What is the overall purpose?
- What are the main parts/sections?
- What looks familiar vs. unfamiliar?

### Step 2: Line-by-Line Analysis

Go through each section and explain what it does:

```markdown
| Lines | What It Does | Why |
|-------|--------------|-----|
| 1-3 | Import dependencies | Need X for Y functionality |
| 5-8 | Initialize state | Track Z during operation |
| 10-15 | Main logic | Does A then B then C |
| 17-20 | Error handling | Catches X, returns Y |
```

### Step 3: Identify Unknowns

Mark anything you don't fully understand:

```typescript
// Line 5: ??? What does this syntax do?
const result = data.reduce((acc, x) => acc ^ x, 0);

// Line 12: ??? Why this specific value?
const MAGIC_NUMBER = 0x5f3759df;

// Line 18: ??? What's the purpose of this check?
if (typeof window !== 'undefined') { ... }
```

**If you have more than 2-3 unknowns, stop and research before proceeding.**

### Step 4: Research Unknowns

For each unknown:

1. **Look up the API/method**
   - Check official documentation
   - Find the method signature and behavior
   - Note any gotchas or edge cases

2. **Find an example**
   - See it used in a simpler context
   - Understand the pattern

3. **Verify your understanding**
   - Can you explain it in your own words?
   - Could you write it differently?

### Step 5: Modification Test

Make a small, intentional change and predict the result:

```markdown
**Test:** If I change X to Y, what should happen?
**Prediction:** The output should change from A to B
**Actual:** [Run it and see]
**Conclusion:**
- If prediction was correct → I understand this part
- If prediction was wrong → I don't understand yet, investigate
```

### Step 6: Explain It Back

Write a brief explanation as if teaching someone else:

```markdown
## What This Code Does

This function [purpose] by:
1. First, it [step 1]
2. Then, it [step 2]
3. Finally, it [step 3]

The key insight is [why it works this way].

Edge cases handled:
- [Edge case 1]: [How it's handled]
- [Edge case 2]: [How it's handled]
```

**If you can't write this explanation, you don't understand the code well enough.**

## Output Format

```markdown
## Code Comprehension: [Brief description]

### Purpose
[One sentence: what this code accomplishes]

### Line-by-Line Understanding
| Lines | What | Why |
|-------|------|-----|
| 1-3 | [What it does] | [Why it's needed] |
| ... | ... | ... |

### Unknowns Resolved
| Unknown | Research | Understanding |
|---------|----------|---------------|
| `reduce((acc, x) => acc ^ x, 0)` | XOR reduction pattern | XORs all elements, returns unique value if one exists |
| ... | ... | ... |

### Modification Test
- **Changed:** [What you changed]
- **Predicted:** [What you expected]
- **Actual:** [What happened]
- **Conclusion:** [Confirmed/Need more investigation]

### Summary Explanation
[2-3 sentences explaining what this code does and why]

### Confidence Level
- [x] Can explain every line
- [x] Understand the design choices
- [x] Could modify it confidently
- [ ] Some gaps remain → List them, research before using
```

## Red Flags (Stop and Investigate)

If any of these are true, you don't understand the code well enough:

- [ ] "It works, I don't know why"
- [ ] "I'll figure it out later"
- [ ] "The AI said it's right, so it must be"
- [ ] "This is just boilerplate"
- [ ] Can't explain what would break if you removed a line
- [ ] Don't know what the edge cases are
- [ ] Couldn't write a test for it

**Don't use code you don't understand.** When it breaks, you'll be helpless.

## Common Patterns to Know

When you see these, make sure you understand them:

### JavaScript/TypeScript
```typescript
// Destructuring with defaults
const { a = 1, b = 2 } = obj;

// Spread operator
const newObj = { ...oldObj, newProp: value };

// Optional chaining
const name = user?.profile?.name;

// Nullish coalescing
const value = input ?? defaultValue;

// Array methods
arr.map(x => transform(x))
arr.filter(x => condition(x))
arr.reduce((acc, x) => combine(acc, x), initial)
```

### React
```typescript
// useEffect cleanup
useEffect(() => {
  const sub = subscribe();
  return () => sub.unsubscribe(); // Cleanup
}, [dep]);

// useMemo for expensive computation
const result = useMemo(() => expensiveCalc(data), [data]);

// useCallback for stable references
const handler = useCallback((e) => handle(e), [dep]);
```

### Async Patterns
```typescript
// Promise.all for parallel
const [a, b] = await Promise.all([fetchA(), fetchB()]);

// try/catch/finally
try { ... } catch (e) { ... } finally { ... }

// Async iteration
for await (const item of asyncIterable) { ... }
```

## Integration with Other Skills

```
Receive AI-generated code
    ↓
/comprehend (THIS SKILL)
    ↓
Understand it? → Yes → Use it
    ↓
No → Research unknowns → Re-run /comprehend
    ↓
Still unclear → Rewrite or ask for simpler version
```

## When to Skip

You can skip `/comprehend` for:
- Code you wrote yourself
- Code you've used many times before
- Trivial one-liners you immediately understand
- Code from trusted internal libraries you know well

When in doubt, take 5 minutes to verify understanding. The time saved debugging incomprehensible code far exceeds the time spent understanding it upfront.

## The Anti-Pattern This Prevents

**Copy-Paste Without Comprehension:**
- Copy code from AI/Stack Overflow
- It works!
- Ship it
- Bug appears
- Can't debug because you don't understand the code
- Spend hours trying to figure out what went wrong
- Eventually rewrite from scratch

**With `/comprehend`:**
- Receive code
- Verify understanding (this skill)
- Know exactly how it works
- Ship it
- Bug appears
- Debug quickly because you understand the code
- Fix in minutes, not hours
