---
name: build-claude-ai-employee
description: 7-step methodology from @SkillDropAI to build a reusable Claude AI employee — give it one job, define inputs, constrain outputs, and save it as a skill.
---

# Build Your First Claude AI Employee
*From @SkillDropAI — Master Claude With Expert Skills*

Turn Claude into a specialized, repeatable worker by following these 7 steps. Each step removes ambiguity so the output is consistent every time.

---

## Step 1 – Pick the Job
Start with one concrete task your business does repeatedly: write cold emails, summarize meetings, categorize support tickets, draft social posts.

---

## Step 2 – Give It One Job

> Don't give Claude a role. Give it a task.

Bad: "You are a marketing assistant."
Good: "Write a cold email for this prospect based on their LinkedIn bio and our offer."

One specific task → consistent output. Vague roles → unpredictable results.

---

## Step 3 – Add the Inputs

Tell Claude exactly what information it needs to do the job.

```
Inputs:
- [Prospect name]
- [Prospect LinkedIn bio]
- [Our offer in one sentence]
- [Desired tone: friendly / professional / bold]
```

If you don't define the inputs, Claude will hallucinate or ask. Define them upfront.

---

## Step 4 – Add the Context

Give Claude the background it needs to do the job well: your brand voice, your ICP, your constraints.

```
Context:
- We sell [product] to [audience]
- Our tone is [X]
- Avoid [Y]
- The email must be under [Z] words
```

---

## Step 5 – Force the Output

Specify exactly what format you want back. If the format is clear, the result is easier to use.

```
Output format:
1. Subject line (under 8 words)
2. Opening line (1 sentence, no "I hope this finds you well")
3. Body (3 sentences max)
4. CTA (one question or one link)
```

Claude returns clean, structured output that's easy to act on.
FORMAT → CLARITY → SPEED.

---

## Step 6 – Test and Iterate

Run it with 3–5 real inputs. Look for:
- Outputs that miss the mark → tighten the context
- Outputs that are too long → add length constraints
- Outputs that are off-tone → add tone examples

---

## Step 7 – Save It As a Skill

Once the prompt produces consistent results, save it as a Claude skill so you can invoke it anywhere.

Structure:
```
---
name: your-skill-name
description: One sentence describing exactly what it does.
---

[Your tested, final prompt here]
```

The skill becomes a reusable AI employee. One command → reliable output, every time.
