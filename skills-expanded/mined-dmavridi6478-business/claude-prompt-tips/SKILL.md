# Claude Prompt Tips

6-tip framework by @the.wealth.lab for getting the best possible results from Claude.

## The Formula

```
GOAL + CONTEXT + ROLE + QUESTIONS + FORMAT + REFINEMENT
```

---

## Tip 1 — Start With the Goal

Tell Claude exactly what you want, who it's for, and what success looks like.

**Example:**
```
Write a LinkedIn post for small business owners about AI automation. The goal is to educate and encourage engagement.
```

---

## Tip 2 — Give Claude Context

Provide background information, constraints, and relevant details before asking your question. The more Claude knows about your situation, the more tailored and useful the response.

---

## Tip 3 — Give Claude a Role

Assign Claude an expert persona to unlock domain-specific knowledge and tone.

**Example:**
```
Act as a senior sales consultant and write a persuasive follow-up email to a potential client.
```

---

## Tip 4 — Make Claude Interview You First

Ask Claude to gather what it needs before answering — prevents generic outputs.

**Example:**
```
Before answering, ask me the questions you need to give me the best possible result.
```

---

## Tip 5 — Define the Format

Specify exactly how you want the output structured.

**Example:**
```
Present the answer as a table with recommendations, benefits, and estimated costs.
```

Other format options: bullet list, numbered steps, executive summary, JSON, code block, email, script.

---

## Tip 6 — Refine With Follow-Ups

Claude's first response is a draft. Push it further:
- "Make it more concise"
- "Make the tone more casual"
- "Add a call to action"
- "Give me 3 alternative versions"
- "Expand the second point"

---

## Full Formula Prompt Template

```
[ROLE] Act as a [expert role].

[GOAL] I need you to [specific task] for [target audience]. The goal is to [desired outcome].

[CONTEXT] Here is the relevant context: [background details, constraints, examples].

[QUESTIONS] Before you start, ask me any questions you need to give me the best possible result.

[FORMAT] Present the output as [format: table / bullet list / numbered steps / email / etc.].
```
