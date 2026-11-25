---
name: client-intake-form
description: "Creates client intake forms and questionnaires that gather essential project information efficiently."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Client Intake Form

## When to Use This Skill

Use this skill when you need to:
- Create an intake form that captures essential project information before kickoff
- Design questionnaires for onboarding new clients efficiently
- Reduce discovery call time by gathering key details in advance
- Standardize information collection across all new engagements

**DO NOT** use this skill for customer surveys, feedback forms, or lead generation forms. This is for service provider intake — gathering what you need to start working.

---

## Core Principle

A GREAT INTAKE FORM ASKS THE RIGHT QUESTIONS IN THE RIGHT ORDER — IT REPLACES A 60-MINUTE DISCOVERY CALL WITH A 10-MINUTE FORM THAT GIVES YOU BETTER INFORMATION.

---

## Phase 1: Form Requirements

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Service type** | "What service will you deliver after collecting this info?" | No default — must be provided |
| **Critical information** | "What must you know before starting work?" | No default — must be provided |
| **Client type** | "Who fills this out — business owners, marketing managers, individuals?" | Business owners |
| **Form length target** | "How long should this take to complete?" | 10-15 minutes |
| **Delivery method** | "Where will this form live — Google Forms, Typeform, PDF, email?" | Google Forms or Typeform |

**GATE: Confirm service type and critical info needs before designing the form.**

---

## Phase 2: Form Structure

### Section Framework

Organize questions into logical sections:

```
## Client Intake Form — [Service Name]

### Section 1: About You
- Business name
- Your name and role
- Website URL
- Industry/niche

### Section 2: Your Goals
- What is the primary goal for this project?
- What does success look like to you?
- Is there a deadline or launch date?

### Section 3: Current Situation
- What have you tried before?
- What is working well that we should keep?
- What is NOT working that prompted this project?

### Section 4: Project Specifics
- [Service-specific questions — see templates below]
- [Scope-defining questions]
- [Preference or style questions]

### Section 5: Logistics
- Budget range (provide tiers, not open-ended)
- Timeline preference
- Preferred communication method
- How did you hear about us?
```

### Question Design Rules

1. **Use closed-ended questions for facts** — multiple choice, dropdowns, yes/no
2. **Use open-ended questions for context** — limit to 3-5 per form
3. **Provide examples** — "Describe your target audience (e.g., women 25-40 who shop online for skincare)"
4. **Make critical fields required** — but keep optional fields for nice-to-have info
5. **Group related questions** — do not jump between topics randomly

---

## Phase 3: Service-Specific Templates

### Design/Branding Intake

- Do you have existing brand guidelines? (Upload option)
- Share 3 websites or brands whose design style you admire
- What colors, fonts, or imagery should we use or avoid?
- Who is your target audience?
- Where will this design be used — web, print, social?

### Copywriting/Content Intake

- What is the purpose of this content — sell, inform, educate, entertain?
- Describe your brand voice in 3 adjectives
- Who is reading this? What do they care about?
- Are there specific keywords or phrases to include?
- Share examples of content you like (URLs or uploads)

### Consulting/Strategy Intake

- What is the biggest challenge your business faces right now?
- What is your revenue and team size?
- What have you already tried to solve this problem?
- What resources (budget, team, time) are available for implementation?
- What would make this engagement a success in your eyes?

### Web Development Intake

- What platform does your site run on?
- What features or functionality do you need?
- Do you have content ready (copy, images, videos)?
- How many pages does the project include?
- Do you need e-commerce, booking, or membership functionality?

---

## Phase 4: Form Optimization

### Completion Rate Tips

- Keep forms under 15 questions for best completion rates
- Use progress bars to show how much is left
- Auto-save responses so clients can return later
- Send a reminder if the form is not completed within 48 hours
- Thank them immediately upon submission with a confirmation and next steps

### Post-Submission Workflow

1. Form submitted — trigger automatic confirmation email
2. Review responses within 24 hours
3. Flag any missing or unclear answers for follow-up
4. Schedule kickoff call only after form is reviewed
5. Reference form answers during kickoff to show you prepared

### Form Checklist

- [ ] Every question serves a specific purpose — no filler
- [ ] Required fields are limited to truly essential info
- [ ] Open-ended questions include example answers
- [ ] Budget question uses ranges, not open text
- [ ] File upload option is included for assets and references
- [ ] Confirmation message includes next steps and timeline
- [ ] Form is mobile-friendly

---

## Anti-Patterns

- **Too many open-ended questions** — 10 text boxes guarantee short, unhelpful answers. Use specific, guided prompts.
- **No budget question** — asking about budget early saves everyone time. Use ranges so clients feel comfortable.
- **Asking for info you will not use** — every question should connect to a decision you make during the project.
- **No confirmation or next steps** — submitting a form into a void makes clients anxious. Tell them what happens next.
- **Duplicating the discovery call** — if you still ask the same questions on the call, the form is not doing its job.

---

## Recovery

- **Client skips the form:** Make it a prerequisite — "I'll review your responses before our kickoff call." No form, no call.
- **Answers are vague or unhelpful:** Follow up with 2-3 targeted clarifying questions. Do not re-send the whole form.
- **Client pushes back on form length:** Shorten to the absolute essentials and gather the rest during the kickoff call.
- **Form tool limitations:** Use a simple Google Form or even a well-formatted email with numbered questions. The tool matters less than the questions.
- **Different clients need different forms:** Create 2-3 variations by service type rather than one catch-all form.
