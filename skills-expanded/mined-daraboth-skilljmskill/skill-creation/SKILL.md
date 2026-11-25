---
name: skill-creation
description: Teach Claude a new permanent skill based on user-provided resources, articles, or documentation. Trigger this skill when the user asks you to "learn a new skill" or provides a resource and says "learn this".
---

# Skill: Skill Creation

> **Purpose**: Teach Claude a new permanent skill based on user-provided resources, articles, or documentation.

## When to Use
- You find a great tutorial or guide and want Claude to remember its patterns
- You want to standardize a new team workflow or coding practice
- You want to expand Claude's knowledge base in the `skills/` directory

---

## How to Teach Claude a New Skill

### Step 1: Provide the Resource
Give Claude the raw material. This can be:
- Pasting the text of an article
- Providing a link or asking Claude to search the web
- Providing a local file path to documentation

### Step 2: Prompt Claude to Learn
Use this exact prompt format to trigger the skill creation:
```
Learn a new skill from this resource: [link/text/file]
Name the skill: [Skill Name]
Category: [coding | personal | language-learning]
```

---

## Claude's Processing Workflow

When the user asks you to learn a new skill, you MUST follow this exact sequence:

### 1. Analyze and Extract
- Read the provided resource thoroughly.
- Extract the core principles, workflows, and best practices.
- Strip out fluff, marketing speak, and long historical context.

### 2. Format
Structure the extracted knowledge using the **Standard Skill Format** (see below). Ensure it strictly adheres to the ADHD-friendly design principles (scannable, short paragraphs, example-driven).

### 3. Save
Create a new `.md` file in the appropriate `skills/[category]/` directory. (e.g., `skills/coding/react-hooks.md`).

### 4. Register
Update `CLAUDE.md` to add the new skill name alphabetically to the "Available skills" list.

### 5. Confirm
Reply to the user with a short summary of what was learned and confirm that the skill is now active.

---

## Standard Skill Format

Every new skill MUST follow this structure to remain consistent:

```markdown
# Skill: [Name]

> **Purpose**: [One sentence explaining why this skill exists]

## When to Use
- [Scenario 1]
- [Scenario 2]

---

## Core Concepts
### [Concept 1]
- Bullet points only
- Keep it punchy

## Examples
### ✅ Good Example
\`\`\`language
// Clean, readable code or clear text
\`\`\`

### ❌ Bad Example
\`\`\`language
// What to avoid
\`\`\`

## Best Practices
1. **Rule 1** — Explanation
2. **Rule 2** — Explanation

## Common Mistakes
| Mistake | Fix |
|---------|-----|
| [Mistake] | [Fix] |
```

---

## Rules for Skill Creation

### 1. ADHD-Friendly Formatting
- **No walls of text**: Use short paragraphs (max 2-3 sentences).
- **Highly scannable**: Use headers, bullet points, and bold text for keywords.
- **Action-oriented**: Focus on *how to do it*, not just *what it is*.

### 2. Practicality Over Theory
- Include code snippets or concrete examples for everything.
- If the source material lacks examples, generate practical ones yourself.

### 3. Modularity
- One concept per file. If a skill gets too large, split it into sub-skills.
- Stay objective. Focus on facts and tested workflows, not unverified opinions.
