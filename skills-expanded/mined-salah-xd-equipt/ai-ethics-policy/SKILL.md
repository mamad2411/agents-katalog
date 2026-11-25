---
name: ai-ethics-policy
description: "Creates AI usage policies for businesses with transparency commitments, bias mitigation, and disclosure guidelines. Use when establishing responsible AI practices."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# AI Ethics Policy

## When to Use This Skill

Use this skill when you need to:
- Create an AI usage policy for your business or team
- Define transparency and disclosure guidelines for AI-generated content
- Establish quality standards and review processes for AI outputs
- Build trust with customers through responsible AI practices

**DO NOT** use this skill for technical AI safety research, legal compliance audits, or data privacy policies (consult a lawyer). This is for practical business AI ethics policies.

---

## Core Principle

AN AI ETHICS POLICY IS A TRUST DOCUMENT — IT TELLS YOUR CUSTOMERS, TEAM, AND STAKEHOLDERS EXACTLY HOW YOU USE AI, WHAT YOU REVIEW, AND WHERE HUMANS REMAIN IN CONTROL.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What does your business do?" | No default — must be provided |
| **AI usage areas** | "Where do you use AI? Content, customer service, analysis, operations?" | No default — list all areas |
| **Customer sensitivity** | "How sensitive is your audience to AI usage? Very, moderate, low?" | Moderate |
| **Disclosure stance** | "Do you want to disclose AI usage publicly, internally only, or both?" | Both |
| **Industry regulations** | "Are there industry-specific AI guidelines you need to follow?" | None specific |

**GATE: Confirm the brief before drafting the policy.**

---

## Phase 2: Structure

### Policy Sections

1. **Purpose** — Why this policy exists
2. **Scope** — What it covers (tools, use cases, people)
3. **Approved Uses** — Where AI is used and how
4. **Prohibited Uses** — Where AI must not be used
5. **Human Oversight** — Review and approval requirements
6. **Disclosure Standards** — When and how to disclose AI usage
7. **Quality Standards** — Accuracy, bias, and output requirements
8. **Data Handling** — What data is shared with AI tools
9. **Review and Updates** — How the policy evolves

**GATE: Confirm the structure before writing.**

---

## Phase 3: Write

### Purpose Statement

"[Business Name] uses AI tools to enhance productivity, improve quality, and serve our customers better. This policy ensures we use AI responsibly, transparently, and with human oversight. AI assists our work — it does not replace our judgment, expertise, or accountability."

### Approved Uses

Document each approved use case:

```
## Approved AI Uses

| Use Case | AI Tool | Human Review Required | Disclosure Required |
|----------|---------|----------------------|---------------------|
| Content drafting | Claude/ChatGPT | Yes — before publishing | Yes — per disclosure standard |
| Email drafting | Claude/ChatGPT | Yes — before sending | No (internal communication) |
| Data analysis | AI analytics tools | Yes — verify conclusions | Depends on context |
| Image generation | DALL-E, Midjourney | Yes — before publishing | Yes — label as AI-generated |
| Customer support | AI chatbot | Escalation path to human | Yes — disclose bot usage |
| Research and summarization | Claude/ChatGPT | Yes — verify facts | No |
```

### Prohibited Uses

```
## AI Must NOT Be Used For

- Making final decisions on hiring, firing, or compensation
- Generating legal advice or contracts without attorney review
- Creating content that impersonates a specific real person
- Processing customer data through unapproved AI tools
- Replacing human judgment on safety-critical decisions
- Generating content on sensitive topics without expert review
- Fabricating testimonials, reviews, or social proof
```

### Disclosure Standards

```
## When to Disclose AI Usage

**Always disclose:**
- Blog posts, articles, or marketing content substantially written by AI
- AI-generated images used in marketing or products
- Customer-facing chatbots or automated responses
- AI-assisted analysis included in client deliverables

**Disclosure format:**
- Website footer or about page: "We use AI tools to assist with content creation. All AI-generated content is reviewed and approved by our team."
- Per-piece disclosure: "This [article/image/analysis] was created with AI assistance and reviewed by [Name]."
- Chatbot: "You are chatting with our AI assistant. A human team member is available if you need them."

**No disclosure required:**
- Internal notes and drafts
- Research and brainstorming
- Spell-checking and grammar tools
- Calendar scheduling and administrative automation
```

### Quality Standards

```
## AI Output Quality Requirements

1. **Accuracy:** All facts, statistics, and claims must be verified by a human before publishing
2. **Originality:** AI output must be reviewed for plagiarism and substantially edited for voice
3. **Bias check:** Review outputs for gender, racial, cultural, or other biases before use
4. **Brand voice:** AI drafts must be edited to match brand tone and style
5. **No hallucinations:** Any specific claims, quotes, or data points must be fact-checked against primary sources
```

---

## Phase 4: Polish

### 1. Data Handling Guidelines

```
## Data and AI Tools

**Do not input into AI tools:**
- Customer personal data (names, emails, financial info)
- Proprietary business data without approval
- Passwords, API keys, or security credentials
- Confidential client information

**Approved for AI input:**
- Publicly available information
- Your own original content and ideas
- Anonymized or aggregated data
- Internal process documentation
```

### 2. Policy Review Process

- Review the policy quarterly
- Update when new AI tools are adopted
- Solicit feedback from team members on practical challenges
- Monitor regulatory developments in your industry
- Document any incidents and update prohibited uses accordingly

### 3. Quality Checklist

```
## AI Ethics Policy Checklist

- [ ] Purpose statement explains why the policy exists
- [ ] All current AI use cases are documented with tools and review requirements
- [ ] Prohibited uses are explicitly listed
- [ ] Disclosure standards specify when, where, and how to disclose
- [ ] Quality standards require human review and fact-checking
- [ ] Data handling guidelines define what can and cannot be shared with AI tools
- [ ] Policy is accessible to all team members
- [ ] Review cadence is set (quarterly minimum)
- [ ] Customer-facing disclosure language is ready to publish
- [ ] Policy is practical and followable (not just aspirational)
```

---

## Example

**Business:** Marketing consultancy

**Customer-facing disclosure:**
"At [Agency], we use AI tools as part of our creative process. AI assists with research, drafting, and analysis — but every deliverable is strategized, reviewed, and refined by our human team. We believe in transparency: if you ever want to know how AI was involved in your project, just ask."

**Internal policy excerpt:**
"All client deliverables that include AI-generated content must be reviewed by a senior team member before delivery. The reviewer confirms: (1) facts are verified, (2) content matches the client's brand voice, (3) no AI hallucinations or fabricated data, and (4) disclosure requirements are met per the client agreement."

---

## Anti-Patterns

- **Policy nobody reads** — if the policy is 20 pages of legalese, nobody will follow it. Keep it practical and under 3 pages.
- **Blanket "we use AI" without specifics** — vague disclosure builds suspicion. Be specific about where and how AI is used.
- **No prohibited uses** — without clear lines, someone will use AI inappropriately. Define the boundaries.
- **Ignoring data privacy** — pasting customer data into AI tools without consent is a liability. Set clear data handling rules.
- **Set and forget** — AI capabilities change rapidly. A policy written 6 months ago may not cover new tools or use cases.

---

## Recovery

- **Team member violates the policy:** Treat it as a learning opportunity. Review the incident, update the policy if needed, and retrain.
- **Customer asks if content is AI-generated:** Answer honestly. Transparency builds more trust than deflection.
- **Industry issues new AI guidelines:** Update the policy immediately. Note the regulatory source and adjust approved/prohibited uses.
- **Policy feels too restrictive:** Review whether restrictions are based on real risks or theoretical concerns. Loosen where the risk is low.
