---
name: ai-content-policy
description: "Creates AI-generated content policies with disclosure requirements, quality standards, and review processes. Use when standardizing how your business produces AI-assisted content."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# AI Content Policy

## When to Use This Skill

Use this skill when you need to:
- Create a policy for how AI-generated content is produced and published
- Define disclosure requirements for AI-assisted content
- Establish quality review standards for AI outputs
- Build a content workflow that integrates AI with human oversight

**DO NOT** use this skill for company-wide AI ethics policies (use ai-ethics-policy), prompt engineering, or AI tool selection. This is specifically for content production policies involving AI.

---

## Core Principle

AI CONTENT POLICY EXISTS TO MAINTAIN QUALITY AND TRUST — EVERY AI-GENERATED PIECE MUST BE REVIEWED, EDITED, AND APPROVED BY A HUMAN BEFORE IT REACHES YOUR AUDIENCE.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Content types** | "What content does your business produce? Blog, social, email, reports?" | No default — list all types |
| **AI usage level** | "How much of your content involves AI? All, most, some, or experimenting?" | Some — growing |
| **Team size** | "Who creates and reviews content?" | Solo creator |
| **Brand sensitivity** | "How important is original voice and brand consistency?" | Very important |
| **Audience expectations** | "Do your readers care whether content is AI-assisted?" | Somewhat — transparency matters |
| **Industry norms** | "Does your industry have specific rules about AI content?" | None specific |

**GATE: Confirm the brief before drafting the policy.**

---

## Phase 2: Structure

### Policy Sections

1. **Purpose** — Why this policy exists
2. **Scope** — What content types it covers
3. **AI Usage Tiers** — Levels of AI involvement
4. **Quality Standards** — Review and editing requirements
5. **Disclosure Requirements** — When and how to disclose
6. **Prohibited Practices** — What is never acceptable
7. **Workflow** — Step-by-step content production process
8. **Review Schedule** — When to update the policy

**GATE: Confirm the structure before writing.**

---

## Phase 3: Write

### AI Usage Tiers

Define levels of AI involvement:

| Tier | AI Role | Human Role | Disclosure |
|------|---------|------------|-----------|
| **Tier 1: AI-Assisted** | Research, outline, brainstorming | Human writes the final content | Optional |
| **Tier 2: AI-Drafted** | AI produces first draft | Human edits substantially (30%+ rewrite) | Recommended |
| **Tier 3: AI-Generated** | AI produces near-final content | Human reviews and approves | Required |

### Quality Standards

```
## Content Quality Requirements

### Before Publishing Any AI-Assisted Content:

**Accuracy Check**
- [ ] All facts verified against primary sources
- [ ] Statistics include source citations
- [ ] No AI hallucinations (fabricated data, fake quotes, nonexistent sources)
- [ ] Technical claims reviewed by subject matter expert (if applicable)

**Voice and Brand**
- [ ] Content matches brand voice and tone guidelines
- [ ] Writing does not sound generic or template-like
- [ ] Personal perspective or experience is woven in where appropriate
- [ ] Industry jargon used correctly (not mimicked incorrectly by AI)

**Originality**
- [ ] Content is not a paraphrase of existing articles
- [ ] Unique insights, examples, or perspectives are included
- [ ] Checked for plagiarism (if high-stakes content)

**Technical**
- [ ] SEO elements are correct (if applicable)
- [ ] Formatting matches platform requirements
- [ ] Links are valid and go to intended destinations
- [ ] Images are original or properly licensed (not AI-generated without review)
```

### Disclosure Standards

```
## Disclosure Guidelines

**When to disclose:**
- Blog posts where AI generated the majority of the draft
- Marketing materials substantially produced by AI
- Client deliverables involving AI assistance
- Social media content generated entirely by AI

**When disclosure is optional:**
- Content where AI was used for research or brainstorming only
- Lightly edited grammar and style suggestions
- Internal communications

**Disclosure formats:**
- Blog post footer: "This article was written with AI assistance and reviewed by [Name]."
- About page: "We use AI tools to enhance our content creation process. All content is reviewed and approved by our team."
- Client communications: Disclose per client agreement

**What NOT to say:**
- Do not claim AI content is "written by [person]" if AI produced the majority
- Do not hide AI usage when directly asked
- Do not imply human expertise where AI provided the analysis
```

### Prohibited Practices

```
## Never Do These

- Publish AI content without human review
- Use AI to fabricate testimonials, reviews, or endorsements
- Present AI-generated research as original research
- Use AI to impersonate a specific person's writing style without disclosure
- Input confidential client data into AI tools without consent
- Publish AI-generated content containing unverified medical, legal, or financial advice
- Use AI to generate content that could mislead or deceive the audience
```

### Content Production Workflow

```
## AI Content Workflow

1. **Brief** — Define topic, audience, intent, and key messages (human)
2. **Research** — Gather sources and data (AI-assisted, human-verified)
3. **Draft** — Produce initial content (AI or human, per tier)
4. **Review** — Edit for accuracy, voice, and quality (human, mandatory)
5. **Approval** — Final sign-off before publishing (human, mandatory)
6. **Publish** — Post with appropriate disclosure (human)
7. **Monitor** — Check for reader feedback and accuracy issues (ongoing)
```

---

## Phase 4: Polish

### 1. Content Tier Decision Guide

Help decide the appropriate AI tier for each content type:

| Content Type | Recommended Tier | Rationale |
|-------------|-----------------|-----------|
| Thought leadership | Tier 1 (AI-Assisted) | Must reflect personal expertise |
| SEO blog posts | Tier 2 (AI-Drafted) | Benefit from AI efficiency with human editing |
| Social media captions | Tier 2 (AI-Drafted) | High volume, needs voice editing |
| Email newsletters | Tier 1-2 | Depends on personal nature of newsletter |
| Client reports | Tier 1 (AI-Assisted) | Client trust requires human authorship |
| Product descriptions | Tier 3 (AI-Generated) | Formulaic, volume-driven |
| Internal docs | Tier 3 (AI-Generated) | Lower stakes, efficiency priority |

### 2. Policy Communication

- Share the policy with anyone who creates content for the business
- Post the customer-facing disclosure on your website
- Include AI disclosure terms in client contracts where applicable
- Review and update the policy every 6 months

### 3. Quality Checklist

```
## AI Content Policy Checklist

- [ ] AI usage tiers defined (Assisted, Drafted, Generated)
- [ ] Quality standards require human review before all publishing
- [ ] Fact-checking and accuracy verification required for all tiers
- [ ] Disclosure requirements specified by content type
- [ ] Prohibited practices explicitly listed
- [ ] Content workflow includes mandatory human review step
- [ ] Each content type mapped to a recommended AI tier
- [ ] Customer-facing disclosure language is prepared
- [ ] Policy is accessible to all content creators
- [ ] Review schedule set (every 6 months minimum)
```

---

## Example

**Business:** Marketing agency producing blog content for clients

**Policy excerpt:**
"All blog posts produced for clients use Tier 2 (AI-Drafted): AI generates the first draft based on a human-created brief, and a senior writer edits at least 30% of the content for accuracy, voice, and originality. Each post is reviewed by the account manager before delivery. Client agreements include a clause disclosing our AI-assisted workflow."

**Disclosure:**
"[Agency] uses AI tools to enhance our content creation process. Every piece of content is briefed by a strategist, reviewed by a senior writer, and approved by your account manager before delivery."

---

## Anti-Patterns

- **No review step** — publishing AI content without human review guarantees quality problems. Always review.
- **Over-disclosing** — adding "Written by AI" to every social caption when AI was used for grammar is unnecessary. Match disclosure to involvement level.
- **Under-disclosing** — claiming full human authorship for AI-generated content erodes trust when discovered. Be honest.
- **One policy for all content** — thought leadership requires a different AI tier than product descriptions. Tier your policy.
- **Ignoring client expectations** — some clients expect human-written content. Disclose AI usage upfront and get consent.

---

## Recovery

- **Client objects to AI usage:** Offer a Tier 1 (AI-Assisted only) option at a premium rate for fully human-written content.
- **AI content quality drops:** Tighten the review process. Add a second reviewer or require more substantial editing before publishing.
- **Team member skips the review step:** Reinforce the workflow. Implement a publish approval step that requires sign-off.
- **Audience reacts negatively to AI disclosure:** Emphasize the human oversight. Audiences care about quality and honesty, not the tools used.
