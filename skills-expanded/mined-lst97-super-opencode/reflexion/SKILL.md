---
name: reflexion
description: Post-action analysis to generate heuristics, update project memory, and prevent regression loops.
---

# Reflexion Skill

## Purpose

To transform **Failures** into **Heuristics**.
Reflexion is the cognitive step that occurs **after** a failed attempt and **before** the next attempt. It breaks the "Insanity Loop" (doing the same thing twice expecting different results).

**ROI Metric**: Prevents 5-10 wasted attempts in a loop by forcing a strategy shift after the first failure.

## When to Use

- **Automatic Trigger**: After a tool error (e.g., `bash` exit code != 0).
- **Automatic Trigger**: After a test failure during `execution` mode.
- **Manual Trigger**: When the user rejects an artifact ("This isn't what I asked for").
- **Periodic**: At the end of a major feature (Project Retro).

## The Reflexion Protocol (The Loop)

### 1. The Halt (Stop)

**Rule**: *Never retry immediately.*
If an error occurs, you must pause. Do not simply re-run the command hoping for a different outcome.

### 2. The Trace (Diagnosis)

**Action**: Analyze the mismatch between *Expected Output* and *Actual Output*.
- *Was it a Syntax Error?* (Context failure).
- *Was it a Logic Error?* (Reasoning failure).
- *Was it a Hallucination?* (Knowledge failure).

### 3. The Heuristic (Correction)

**Action**: Create a new rule for yourself.
- *Old Thought:* "I will use `rm -rf` to clean up."
- *New Heuristic:* "I must check if the directory exists before attempting delete."

### 4. The Store (Memory)

**Action**: Save this lesson.
- *Short-term:* Apply to current context window.
- *Long-term:* Write to `.opencode/memory/patterns.md`.

## Execution Template

*Use this scratchpad when entering a Reflexion State.*

```markdown
## 🧠 Reflexion: [Failure Context]

### 1. Analysis
- **Expectation**: Test passed.
- **Reality**: `ReferenceError: User is not defined`
- **Gap**: I assumed `User` was exported from `types.ts`, but it was a default export.

### 2. Critique
"I failed to check the import style of the existing module before writing the import statement."

### 3. New Strategy (The Pivot)
- ❌ **Stop**: Guessing import paths.
- ✅ **Start**: Using `grep` to see how other files import `User`.
- **Action**: Run `grep -r "import.*User" .` before fixing.

### 4. Memory Update
- [ ] Add to Local Context? (Yes)
- [ ] Add to Project Patterns? (No - simple syntax error)
```

## Memory Schema & Storage

Maintain a dedicated memory structure to allow the `researcher` and `pm-agent` to learn over time.

```text
.opencode/
└── memory/
    ├── active_context.md       # Scratchpad for current session
    ├── patterns.md             # Success patterns (What works here)
    └── anti_patterns.md        # Failure log (What breaks here)
```

### Example: `.opencode/memory/anti_patterns.md`

```markdown
## ⛔ Anti-Patterns

### 1. Database Connections
- **Context**: Next.js Server Components.
- **Failure**: "Too many connections" error.
- **Lesson**: Do not instantiate Prisma Client inside the component. Use the singleton pattern defined in `src/lib/db.ts`.

### 2. Styling
- **Context**: Button Components.
- **Failure**: Tailwinds classes not applying.
- **Lesson**: We are using `tailwind-merge`. Standard string concatenation will fail. Always use `cn()` utility.
```

## Integration with Agents

- **`execution` agent**: Must trigger `reflexion` after 2 failed build attempts.
  - *Logic:* "Attempt 1 Failed -> Retry -> Attempt 2 Failed -> **STOP & REFLECT** -> Attempt 3".
- **`pm-agent`**: Reads `.opencode/memory/patterns.md` at the start of a new task to load context.
- **`writer`**: Uses successful reflexions to update the project's `README.md` or `CONTRIBUTING.md`.

## Reflexion vs. Debugging

| Feature | `debug-protocol` | `reflexion` |
| :--- | :--- | :--- |
| **Focus** | The Code | The Agent's Process |
| **Goal** | Fix the Bug | Improve the Strategy |
| **Output** | Working Software | Better Internal Rules |
| **Question** | "Why is variable X null?" | "Why did I write code that made X null?" |
