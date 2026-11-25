---
name: training-manual
description: "Writes training manuals with step-by-step instructions, visual aids, knowledge checks, and reference sections."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Training Manual

## When to Use This Skill

Use this skill when you need to:
- Write a training manual for employees, clients, or program participants
- Create step-by-step instructions for processes and procedures
- Include knowledge checks that verify comprehension
- Build reference sections for ongoing use after training

**DO NOT** use this skill for SOPs (use property-management-sop or similar), user documentation, or API documentation. This is for training materials designed to teach someone how to do something.

---

## Core Principle

A TRAINING MANUAL IS NOT A REFERENCE BOOK — IT IS A GUIDED LEARNING EXPERIENCE THAT TAKES SOMEONE FROM "I DO NOT KNOW HOW" TO "I CAN DO THIS ON MY OWN" THROUGH STRUCTURED, SEQUENTIAL INSTRUCTION.

---

## Phase 1: Manual Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Subject** | "What skill or process does this manual teach?" | No default — must be provided |
| **Audience** | "Who is the learner — new employee, client, general public?" | New team member |
| **Prior knowledge** | "What should the reader already know before starting?" | No prior knowledge assumed |
| **Format** | "Digital PDF, printed manual, or online wiki?" | Digital PDF |
| **Estimated length** | "How many sections or chapters?" | 5-8 sections |

**GATE: Confirm subject, audience, and scope before outlining the manual.**

---

## Phase 2: Manual Structure

### Outline Template

```
## [Manual Title] — Training Manual

### Front Matter
- Title page
- Table of contents
- How to use this manual
- Prerequisites (if any)

### Section 1: [Foundation / Overview]
- What is [subject] and why it matters
- Key concepts and terminology
- How this fits into the bigger picture

### Section 2: [Core Process / Skill — Part 1]
- Step-by-step instructions
- Visual aids and screenshots
- Common mistakes to avoid
- Knowledge check

### Section 3: [Core Process / Skill — Part 2]
- Step-by-step instructions
- Tips and best practices
- Troubleshooting guide
- Knowledge check

### Section 4: [Advanced Topics]
- Building on the basics
- Edge cases and exceptions
- When to escalate or ask for help

### Section 5: [Practice Exercises]
- Hands-on scenarios with guided steps
- Independent practice with answer keys
- Real-world application exercises

### Reference Section
- Quick reference card (1-page summary)
- Glossary of terms
- FAQ
- Resource links and contacts
```

---

## Phase 3: Writing Guidelines

### Step-by-Step Instruction Format

```
## [Task Name]

**Purpose:** [Why this task matters — 1 sentence]
**Time required:** [Estimate]
**Tools needed:** [List]

### Steps:

1. **[Action verb] + [specific action]**
   - [Additional detail or explanation]
   - [Screenshot or visual placeholder: describe what the reader should see]

2. **[Action verb] + [specific action]**
   - [Additional detail]
   - ⚠️ **Note:** [Important warning or tip]

3. **[Action verb] + [specific action]**
   - [Additional detail]
   - ✓ **Result:** [What the reader should see when done correctly]
```

### Writing Rules

1. **One action per step** — do not combine "click Save and then navigate to Settings" into one step
2. **Use imperative voice** — "Click the button" not "The button should be clicked"
3. **Include visual checkpoints** — tell the reader what they should see after each major step
4. **Warn before errors** — place caution notes BEFORE the step that could cause issues
5. **Define terms on first use** — bold and briefly explain any jargon
6. **Keep paragraphs to 2-3 sentences** — training content must be scannable
7. **Number all steps** — so learners can reference specific steps in questions

### Knowledge Check Format

After each section, include 3-5 questions:

```
## Knowledge Check — Section [X]

1. [Question — multiple choice, true/false, or short answer]
   a) [Option A]
   b) [Option B]
   c) [Option C]
   **Answer: [Correct answer with brief explanation]**

2. [Scenario-based question]
   "You encounter [situation]. What should you do?"
   **Answer: [Correct action and why]**
```

---

## Phase 4: Supplementary Materials

### Quick Reference Card (One-Pager)

```
## [Subject] — Quick Reference

### Key Steps
1. [Step 1 — condensed]
2. [Step 2 — condensed]
3. [Step 3 — condensed]

### Common Shortcuts
- [Shortcut 1]: [What it does]
- [Shortcut 2]: [What it does]

### Troubleshooting
- [Problem]: [Quick fix]
- [Problem]: [Quick fix]

### Need Help?
Contact: [Name/Team] at [email/phone]
```

### Glossary Template

```
## Glossary

**[Term 1]** — [Definition in plain language]
**[Term 2]** — [Definition in plain language]
**[Term 3]** — [Definition in plain language]
```

### Manual Quality Checklist

- [ ] Table of contents matches actual section headers
- [ ] Every section has a clear learning objective
- [ ] Step-by-step instructions use numbered lists with one action per step
- [ ] Visual aids or screenshot placeholders are included for complex steps
- [ ] Knowledge checks appear after each major section
- [ ] Answers are provided for all knowledge check questions
- [ ] Quick reference card summarizes the key process on one page
- [ ] Glossary defines all technical terms used
- [ ] Manual has been tested by someone unfamiliar with the process
- [ ] Version number and last-updated date are included

---

## Anti-Patterns

- **Assuming knowledge** — if the reader knew how, they would not need the manual. Explain everything from the beginning.
- **Walls of text** — training content must be visual and scannable. Use lists, tables, headers, and white space.
- **No practice opportunities** — reading instructions without doing them results in poor retention. Include exercises.
- **Outdated screenshots** — nothing erodes trust faster than visuals that do not match what the reader sees. Update regularly.
- **No troubleshooting section** — learners will encounter problems. Anticipate the common ones and provide solutions.
- **Writing for experts** — a training manual is for beginners. Use plain language, not industry shorthand.

---

## Recovery

- **Manual is too long:** Split into a quick-start guide (essentials only) and a comprehensive manual (everything). Most people need the quick-start.
- **Learners still confused after reading:** Add more examples, simplify language, and test with a fresh reader. Watch where they get stuck.
- **Process changes frequently:** Version the manual and maintain a changelog. Designate an owner responsible for updates.
- **No visuals available:** Use descriptive text placeholders and add screenshots later. The manual is still useful without images.
- **Multiple audiences with different needs:** Create role-specific sections or separate manuals rather than one document that tries to serve everyone.
