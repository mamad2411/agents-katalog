---
name: prompt-engineering
description: Use this skill when writing, improving, or debugging prompts for any AI model — Claude, GPT, Gemini, or Copilot. Also use when designing plan-before-execute workflows, verification patterns, self-improvement loops, or structuring AI instructions for maximum clarity and output quality. Trigger on keywords: prompt, prompt engineering, instruct AI, system prompt, few-shot, chain-of-thought, AI instruction, prompt template, prompt pattern.
---

# Prompt Engineering

## Core Philosophy

A great prompt is not a magic spell — it's a specification. The more precisely you define the goal, context, constraints, and output format, the more reliably the AI performs. Think of prompting like writing a function signature: the model is the implementation, you are the interface designer.

**The Golden Rule:** If the output isn't what you wanted, the problem is almost always in the prompt — not the model.

---

## Prompt Anatomy (4-Part Structure)

Every effective prompt has four components:

```
ROLE:    Who the AI should be (expertise, perspective, voice)
GOAL:    What you want done (specific, unambiguous task)
CONTEXT: Relevant background, data, constraints, examples
OUTPUT:  Exact format, length, structure of the response
```

### Example
```
ROLE: You are a senior TypeScript developer with expertise in React and Next.js.
GOAL: Review this component for performance issues and suggest specific improvements.
CONTEXT: This is a client component in Next.js 15 App Router. 
         Performance is critical — this renders on every keystroke.
         [paste code here]
OUTPUT: List issues as BLOCKER / WARNING / SUGGESTION with specific fix for each.
```

---

## Core Techniques

### Zero-Shot
Ask directly with no examples. Works for well-understood tasks.
```
Write a conventional commit message for this diff: [diff]
```

### Few-Shot
Provide 2–3 examples before the real task. Best for format-sensitive or pattern-matching tasks.
```
Examples:
Input: Added login form → Output: feat(auth): add login form with email/password
Input: Fixed null crash → Output: fix(api): handle null response from user endpoint

Now write a commit message for: [diff]
```

### Chain-of-Thought (CoT)
Force step-by-step reasoning. Add "Think step by step" or "Reason through this before answering."
```
Is this API design RESTful? Think step by step before answering.
```

### Role / Persona Assignment
Set expertise level and perspective upfront.
```
You are a security engineer specializing in OWASP Top 10.
Review this authentication code for vulnerabilities.
```

### Delimiters
Use clear separators to prevent the model from confusing instructions with content.
```
Refactor the following code:
"""
[code here]
"""
Rules: No external dependencies. TypeScript only. Preserve existing tests.
```

---

## Advanced Techniques

### Self-Consistency
For critical decisions, run the same prompt 3 times and take the majority answer. Reduces variance on high-stakes reasoning.

### Tree of Thought (ToT)
Force the model to explore multiple approaches before committing.
```
Propose three different approaches to solve this problem.
For each approach, list pros, cons, and implementation complexity.
Then recommend the best one with justification.
```

### ReAct (Reason + Act)
Interleave reasoning with action steps. Best for agentic or multi-step tasks.
```
Thought: What do I need to understand before solving this?
Action: [tool or analysis]
Observation: [result]
Thought: Based on this, the next step is...
```

### Metacognitive Prompting
Ask the model to critique its own output before finalizing.
```
After generating your answer, critically evaluate it:
- Are all steps logically valid?
- Are there unsupported assumptions?
- What could go wrong with this approach?
Correct any issues before presenting the final answer.
```

### COSTAR Framework
Structured template for complex prompts:
- **C**ontext — background information
- **O**bjective — what you want done
- **S**tyle — tone and voice
- **T**one — formal, casual, direct
- **A**udience — who will read this
- **R**esponse format — structure of output

---

## Plan-Before-Execute Pattern

**Never let AI jump straight to implementation for non-trivial tasks.**

```
Step 1 — Plan: Outline your approach step by step. 
         Do NOT write any code yet.
Step 2 — Review: I will confirm the plan before you proceed.
Step 3 — Execute: Implement each step from the approved plan.
```

### When to Use Plan Mode
- Task spans multiple files or components
- Architectural decisions are involved
- Uncertainty exists about requirements
- Task has 3+ steps

### When to Skip It
- Single-file, well-defined change
- Bug fix with obvious cause and solution
- Formatting or style-only change

---

## Verification Patterns

Always instruct the AI to verify its own work before presenting it.

```
Before finalizing your answer:
1. Check that all steps are logically sound
2. Verify no assumptions were made that weren't stated
3. Confirm the output matches the requested format
4. Correct any issues you find
Then present the final answer.
```

For code specifically:
```
After writing the code:
1. Trace through it mentally with a simple test case
2. Check all edge cases (null, empty, boundary values)
3. Verify error handling is present
4. Confirm it matches the requirements exactly
```

---

## Self-Improvement Loop

When the AI makes a mistake, don't just fix it — extract the lesson:

```
I noticed an error in your previous response: [describe error]
1. Explain why this error occurred
2. State the general rule that would prevent it
3. Apply that rule to the corrected answer
```

For long sessions, maintain a lessons log:
```
Update your working notes with this lesson:
[lesson from the correction]
Apply this to all remaining tasks in this session.
```

---

## Model-Specific Tips

| Model | Strengths | Best Practices |
|---|---|---|
| **Claude** | Long context, nuanced reasoning, following complex instructions | Use XML-style tags for structure, provide CLAUDE.md for project context, explicit role assignment |
| **GPT-4/4o** | Strict format adherence, JSON output, code generation | Put instructions at top, use delimiters, hint at language with imports |
| **Gemini** | Research, citations, massive context windows, multi-modal | Request citations explicitly, define scope and time range, specify how to handle uncertainty |
| **Copilot** | In-editor context awareness, code completion | Use `.github/copilot-instructions.md` for project context, be explicit about stack |

---

## Anti-Patterns (What to Avoid)

| Anti-Pattern | Problem | Fix |
|---|---|---|
| "Write code for X" | Too vague | Add role, constraints, output format |
| Treating first answer as final | Misses errors | Always include verification step |
| No examples for format-sensitive tasks | Wrong format | Add 2–3 few-shot examples |
| Skipping role assignment | Generic tone/depth | Always assign a specific expertise persona |
| Concatenating user input into system prompt | Prompt injection risk | Use delimiters, validate input, separate concerns |
| Over-prompting simple tasks | Wastes tokens | Match prompt complexity to task complexity |

---

## Prompt Security

- **Prompt Injection:** User input that hijacks the model's behavior. Never concatenate raw user input into system prompts.
- **Delimiter Protection:** Use `"""` or XML tags to clearly separate instructions from user content.
- **Principle of Least Privilege:** Don't give the AI more context or permissions than it needs for the task.
- **Input Validation:** Sanitize user inputs before they reach the model in production systems.

---

## See Also
- `references/prompt-templates.md` — Ready-to-use prompt templates for common dev tasks
- `ai-prompting-patterns` skill — Agent communication and intent clarification patterns
- `ai-agent-design` skill — Building full agentic systems
