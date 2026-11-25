---
name: ai-usage
description: Frameworks and habits for using AI coding assistants effectively — the CRISP prompt framework (Context, Role, Instruction, Specifics, Proof), when to use vs. not use AI, avoiding over-reliance, and combining multiple AI tools. Use when the user asks "how do I prompt X", wants help writing a better prompt for an AI tool, or asks whether/when to use AI for a task. Not a general AI ethics or model-selection guide.
---

# Skill: AI Usage

> **Purpose**: Use AI tools effectively without becoming dependent. AI is a multiplier, not a replacement.

## When to Use
- Writing prompts for AI assistants
- Debugging with AI help
- Deciding when to use vs. not use AI
- Using multiple AI tools together

---

## Effective Prompt Writing

### The CRISP Framework

**C** — Context: What are you working on?
**R** — Role: What expertise should the AI use?
**I** — Instruction: What exactly do you want?
**S** — Specifics: Constraints, format, language, length
**P** — Proof: Ask for examples or verification

### Examples

```
❌ Bad prompt:
"Fix my code"

✅ Good prompt:
"I have a JavaScript async function that fetches user data.
It returns undefined instead of the user object.
Here's the code: [paste code]
Here's the error: [paste error]
What's causing this, and how do I fix it?
Show me the corrected code with an explanation."
```

```
❌ Bad prompt:
"Explain closures"

✅ Good prompt:
"Explain JavaScript closures in 3 sentences.
Then show one practical example where closures solve a real problem.
Then show one common mistake with closures and how to avoid it.
Keep it beginner-friendly."
```

### Prompt Templates

#### For Debugging
```
I'm getting this error in my [language] code:
Error: [paste full error message]

Here's the relevant code:
[paste code]

What I expected: [expected behavior]
What happened: [actual behavior]

What's the root cause, and how do I fix it?
```

#### For Learning
```
Explain [concept] as if I'm a junior developer.
- One-sentence definition
- One practical code example
- One common mistake to avoid
- When should I use this vs. [alternative]?
```

#### For Code Review
```
Review this [language] code for:
1. Bugs or potential errors
2. Readability improvements
3. Performance concerns

[paste code]

Prioritize issues from most to least critical.
```

---

## Debugging with AI

### Step-by-Step Process

1. **Try fixing it yourself first** (15 min rule)
2. **Gather context**: error message, stack trace, relevant code
3. **Ask AI with full context** using the debugging template
4. **Understand the fix before applying it** — ask "why does this work?"
5. **Verify the fix yourself** — don't blindly trust

### What to Share with AI
```
✅ Include:
- Full error message and stack trace
- The specific code that's failing
- What you expected vs. what happened
- What you already tried

❌ Don't include:
- Your entire codebase
- Unrelated files
- Vague descriptions like "it doesn't work"
```

### Red Flags in AI Responses
- Uses a library or API you didn't ask about → verify it exists
- Suggests deprecated syntax → check current docs
- Gives a complex solution for a simple problem → ask for simpler version
- Confidently wrong → always test the code

---

## Avoiding Over-Reliance

### The 3-Tier Rule

| Tier | When | Use AI? |
|------|------|---------|
| **Learn** | Studying a new concept | ✅ Yes — ask for explanations and examples |
| **Practice** | Solving problems, writing code | ⚠️ Minimal — try first, ask after 15 min |
| **Build** | Working on your project | ✅ Yes — for boilerplate, debugging, code review |

### Signs You're Over-Relying
- You paste every error without reading it first
- You can't explain code the AI wrote for you
- You feel anxious coding without AI
- You copy-paste without modifying for your use case

### How to Build Independence
1. **Read the error yourself** before asking AI
2. **Write the first version** yourself, then ask AI to review
3. **Explain AI's solution in your own words** — if you can't, you don't understand it
4. **Code without AI for 30 min daily** — build the muscle
5. **Use AI for validation, not creation** — "Is this approach correct?" vs. "Write this for me"

---

## Using Multiple AI Tools Efficiently

### Tool Strengths

| Tool | Best For |
|------|----------|
| **Claude** | Long-form code, detailed explanations, nuanced reasoning |
| **ChatGPT** | Quick answers, brainstorming, general knowledge |
| **GitHub Copilot** | In-editor autocomplete, boilerplate code |
| **Gemini** | Google ecosystem, search-integrated answers |
| **Perplexity** | Research with sources, fact-checking |

### Multi-Tool Workflow

```
1. Quick question → ChatGPT (fast response)
2. Deep debugging → Claude (detailed analysis, long context)
3. Writing code → Copilot (inline suggestions)
4. Research → Perplexity (sourced answers)
5. Verify facts → Cross-check between tools
```

### Cross-Verification Strategy
When an AI gives a non-trivial technical answer:
1. Ask a different AI the same question
2. Check official documentation
3. Test the code yourself
4. If two AIs disagree, the docs win

---

## Prompt Optimization Tips

### 1. Be Specific About Format
```
"Return the answer as:
1. One-line summary
2. Code example
3. Common pitfalls"
```

### 2. Give Examples of What You Want
```
"Format like this:
Input: [2, 3, 5]
Output: 10
Explanation: Sum of all elements"
```

### 3. Set Constraints
```
"Use only vanilla JavaScript. No libraries.
Keep the solution under 20 lines.
Explain each line with a comment."
```

### 4. Iterate
```
First prompt:  "Explain promises"
Follow-up:     "Now show a real-world example with error handling"
Follow-up:     "What happens if I don't catch the error?"
Follow-up:     "Rewrite this using async/await instead"
```

---

## Best Practices
1. **Understand before applying** — never paste code you don't understand
2. **Provide full context** — the better the input, the better the output
3. **Verify everything** — AI can be confidently wrong
4. **Use AI to learn, not to avoid learning**
5. **Build your own judgment** — over time, rely less on AI for decisions you can make

## Common Mistakes
| Mistake | Fix |
|---------|-----|
| "Fix my code" with no context | Include error, code, expected vs. actual |
| Blindly trusting AI output | Always test and verify |
| Using AI for trivial things you know | Only use when it genuinely saves time |
| Not learning from AI responses | Ask "why" and understand the reasoning |
| Using one AI for everything | Match the tool to the task |
