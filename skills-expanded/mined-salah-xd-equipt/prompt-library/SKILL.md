---
name: prompt-library
description: "Organizes and documents reusable prompt libraries with categories, variables, and quality scoring. Use when building a structured collection of AI prompts for your business."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Prompt Library

## When to Use This Skill

Use this skill when you need to:
- Build an organized library of reusable AI prompts for business tasks
- Document prompts with variables, examples, and usage instructions
- Create a quality scoring system for prompt effectiveness
- Standardize prompt usage across a team or workflow

**DO NOT** use this skill for writing individual prompts, prompt engineering tutorials, or AI tool comparisons. This is for organizing and documenting a collection of prompts.

---

## Core Principle

A PROMPT LIBRARY IS A BUSINESS ASSET — EVERY PROMPT SHOULD BE DOCUMENTED, TESTED, AND VERSIONED SO ANYONE CAN USE IT AND GET CONSISTENT RESULTS.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What does your business do?" | No default — must be provided |
| **AI tools used** | "Which AI tools do you use? Claude, ChatGPT, Gemini, other?" | Claude |
| **Key use cases** | "What do you use AI for most? Content, email, research, analysis?" | No default — list at least 5 |
| **Team usage** | "Will this library be used by just you or shared with a team?" | Solo use |
| **Current prompts** | "Do you have any prompts you already reuse regularly?" | A few informal ones |
| **Storage preference** | "Where should the library live? Notion, Google Docs, markdown files?" | Markdown files |

**GATE: Confirm the brief before designing the library structure.**

---

## Phase 2: Design the Library

### Category Structure

Organize prompts by business function:

```
prompt-library/
├── content/
│   ├── blog-post-draft.md
│   ├── social-media-caption.md
│   └── email-newsletter.md
├── marketing/
│   ├── ad-copy.md
│   ├── landing-page-copy.md
│   └── lead-magnet-outline.md
├── operations/
│   ├── meeting-summary.md
│   ├── process-documentation.md
│   └── project-brief.md
├── finance/
│   ├── invoice-reminder.md
│   └── expense-report.md
├── customer/
│   ├── support-response.md
│   ├── review-reply.md
│   └── onboarding-email.md
└── research/
    ├── competitor-analysis.md
    └── market-research.md
```

### Prompt Card Template

Every prompt in the library uses this format:

```
# [Prompt Name]

**Category:** [Business function]
**AI Tool:** [Claude / ChatGPT / Any]
**Version:** [1.0]
**Last tested:** [Date]
**Quality score:** [1-5]

## Purpose
[One sentence: what this prompt produces]

## Variables
- {{VARIABLE_1}}: [Description, example]
- {{VARIABLE_2}}: [Description, example]

## Prompt
[The full prompt text with {{VARIABLES}} marked]

## Example Output
[A sample of what good output looks like]

## Tips
- [Usage tip 1]
- [Usage tip 2]

## Changelog
- v1.0 — Initial version
```

**GATE: Confirm the structure and template before populating the library.**

---

## Phase 3: Populate

### Prompt Writing Rules

- **One prompt, one purpose** — do not combine tasks. A prompt that writes AND edits AND formats is three prompts.
- **Variables are explicit** — use `{{DOUBLE_BRACES}}` for every input the user must provide. Never leave implicit assumptions.
- **Include constraints** — word count, tone, format, what to avoid. Constraints improve output quality.
- **Show the ideal output** — include one example of what a good response looks like. This sets the quality bar.
- **Version everything** — when you improve a prompt, increment the version and note what changed.

### Quality Scoring Rubric

| Score | Label | Criteria |
|-------|-------|----------|
| 5 | Production-ready | Consistent high-quality output with minimal editing needed |
| 4 | Reliable | Good output 80%+ of the time, occasional light editing |
| 3 | Usable | Produces a solid starting point but requires human refinement |
| 2 | Needs work | Inconsistent results, prompt needs improvement |
| 1 | Experimental | Untested or unreliable, keep for iteration |

### Prompt Iteration Process

1. Write the initial prompt (v1.0)
2. Test with 3 different inputs
3. Score the outputs
4. Identify weaknesses (too long, wrong tone, missing elements)
5. Revise the prompt (v1.1)
6. Retest and rescore
7. Repeat until score reaches 4+

---

## Phase 4: Polish

### 1. Library Maintenance

- **Monthly review:** Test top 10 most-used prompts with current AI model versions
- **Quarterly audit:** Archive prompts not used in 90 days, add new ones for emerging needs
- **Version control:** Never overwrite — always create a new version and note changes
- **Usage tracking:** Note which prompts get used most and which produce the best results

### 2. Team Sharing Guide (if applicable)

- Store in a shared location (Notion, shared folder, repo)
- Create a quick-start guide: how to find prompts, how to use variables, how to submit new prompts
- Designate a prompt librarian (or rotate the role)
- Set up a feedback mechanism: "This prompt worked / didn't work because..."

### 3. Quality Checklist

```
## Prompt Library Checklist

- [ ] Categories cover all major business functions
- [ ] Every prompt uses the standard card template
- [ ] All variables are marked with {{DOUBLE_BRACES}} and described
- [ ] Each prompt includes at least one example output
- [ ] Quality scores are assigned and up to date
- [ ] Prompts are versioned with changelogs
- [ ] Library is organized in a searchable structure
- [ ] Monthly review cadence is scheduled
- [ ] Top prompts are tested with current AI model versions
- [ ] Archive process exists for unused prompts
```

---

## Example

**Prompt card:**
```
# Social Media Caption

**Category:** Content
**AI Tool:** Claude
**Version:** 1.2
**Last tested:** 2026-02-15
**Quality score:** 4

## Purpose
Writes a social media caption for Instagram or LinkedIn from a topic and key message.

## Variables
- {{PLATFORM}}: Instagram or LinkedIn
- {{TOPIC}}: The subject of the post
- {{KEY_MESSAGE}}: The one point you want to make
- {{TONE}}: casual, professional, motivational, witty
- {{CTA}}: What you want the reader to do

## Prompt
Write a {{PLATFORM}} caption about {{TOPIC}}.

Key message: {{KEY_MESSAGE}}
Tone: {{TONE}}
Include a call to action: {{CTA}}

Requirements:
- Under 150 words for Instagram, under 200 for LinkedIn
- Open with a hook (question, bold statement, or surprising fact)
- Use line breaks for readability
- End with the CTA
- No hashtags in the body (I will add them separately)

## Example Output
"Most solopreneurs spend 6 hours a week on invoicing.

Six. Hours.

That is an entire workday every month spent on paperwork instead of revenue.

I cut that to 45 minutes by automating three things:
→ Invoice generation from project completion
→ Automatic payment reminders
→ Expense categorization

The tools cost $30/month total. The time savings are worth $1,200.

Drop a 🔥 if you want the exact setup."

## Changelog
- v1.2 — Added "no hashtags" constraint, improved hook instruction
- v1.1 — Added platform-specific word count limits
- v1.0 — Initial version
```

---

## Anti-Patterns

- **Hoarding untested prompts** — a library of 50 untested prompts is a junk drawer. Test and score before adding.
- **No variables** — hardcoded details make prompts single-use. Extract every changeable element into a variable.
- **No examples** — without a sample output, quality is subjective. Always show what good looks like.
- **Never updating** — AI models change. A prompt that worked 6 months ago may not work as well today. Review regularly.
- **Overcomplicating** — a prompt that requires 15 variables is too complex. Break it into multiple simpler prompts.

---

## Recovery

- **Too many prompts to organize:** Start by categorizing the 10 you use most. Archive everything else and add as needed.
- **Prompts produce inconsistent results:** Add more constraints (word count, format, tone, examples). Constraints reduce variance.
- **Team members not using the library:** The library is too hard to access or search. Simplify structure and create a quick-start guide.
- **Quality scores are all low:** The prompts may be too broad. Narrow the purpose of each prompt to one specific output.
