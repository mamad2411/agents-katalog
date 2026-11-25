---
name: jobs-to-be-done
description: "Use when applying the Jobs to Be Done framework. Transforms user needs into AI-ready JTBD blueprints with guided discovery flows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [jtbd, jobs-to-be-done, user-research, product-design, needs-analysis, innovation]
    related_skills: [buyer-persona-architect, value-proposition-architect, use-case-architect, business-model-canvas-builder]
---

# Jobs to Be Done (JTBD) Architect

## Overview

Applies the Jobs to Be Done framework to transform customer needs, user stories, or product ideas into structured JTBD statements with full context: functional, emotional, and social job dimensions, current alternatives, desired outcomes, and the forces that drive or block switching. Outputs are formatted for direct use in product roadmaps, UX research, and AI/automation opportunity mapping.

## When to Use

- A product team says "users want X" but you need deeper understanding of why they want it.
- Defining new features or products — JTBD uncovers demand beyond surface-level feature requests.
- Prioritizing a backlog: JTBD helps distinguish real jobs from nice-to-haves.
- Building AI or automation solutions — JTBD blueprints make the underlying need explicit so AI can be designed to address it.
- Competitive analysis: understanding what job customers hire a competitor's product to do.
- Don't use for: technical implementation, UI/UX design (JTBD informs it but doesn't replace it), or persona work (use `buyer-persona-architect` for that).

## How It Works

1. **Discovery flow** — Guides the user through a structured interview (or processes submitted documents) to uncover the real job behind surface-level requests.
2. **JTBD statement generation** — Produces properly formatted job statements using the standard syntax: "When [situation], I want to [motivation], so I can [expected outcome]."
3. **Job dimension mapping** — For each job, identifies the functional, emotional, and social dimensions, plus the forces of progress and inertia.
4. **Blueprint output** — Produces an AI-ready blueprint that maps each job to solution approaches, success criteria, and implementation priority.

## Steps

1. **Discovery interview (if no documents provided):** Walk through:
   - What triggered the search for a solution? (the "push" moment)
   - What were you doing before? (the current alternative / workaround)
   - What does success look like? (the desired outcome)
   - What almost stopped you? (anxieties, habits, switching costs)
2. **Generate JTBD statements:** For each discovered job, produce:
   - **Job Statement:** When [situation/context], I want to [functional job], so I can [emotional/social outcome].
   - **Current Alternative:** What they do today (manual process, competing product, nothing).
   - **Forces of Progress:** Push (pain of current state), Pull (attraction of new solution), Anxiety (fear of switching), Inertia (habit of current behavior).
3. **Map job dimensions:**
   - **Functional:** The practical task being accomplished.
   - **Emotional:** How the user wants to feel (confident, in control, relieved).
   - **Social:** How the user wants to be perceived by others (competent, efficient, innovative).
4. **Prioritize jobs:** Score each job on:
   - Frequency (how often is this job hired?)
   - Importance (how critical is getting it done?)
   - Dissatisfaction (how bad is the current alternative?)
   - Opportunity Score = Importance + max(Importance - Satisfaction, 0)
5. **Produce AI blueprint:** For each high-priority job, map to:
   - What AI/automation capability could address this job?
   - What data/inputs does the AI need?
   - What's the success criterion for the AI solution?
   - Tie to `use-case-architect` for full implementation scoping.

## Common Pitfalls

1. **Confusing jobs with features:** "Users want a dashboard" is a feature request. The job is "I want to quickly assess my team's performance so I can report to my board with confidence."
2. **Skipping emotional/social dimensions:** The functional job is only one-third of the picture. A tool that does the job but makes users feel stupid or look amateurish will fail.
3. **Assuming the job instead of discovering it:** Don't guess. Use the discovery flow. If the user can't provide real customer input, flag it as a hypothesis, not a confirmed job.
4. **Job-bloat:** Not every user action is a job. Jobs are stable over time (people have wanted to "share information quickly" for centuries — the feature changes from mail to email to Slack, but the job persists).
5. **Ignoring non-consumption:** The biggest competitor is often "doing nothing" or "using a workaround." Map this explicitly.

## Verification Checklist

- [ ] Each job has a properly formatted statement with situation, motivation, and outcome
- [ ] Functional, emotional, and social dimensions are mapped for each job
- [ ] Forces of Progress (push, pull, anxiety, inertia) are documented
- [ ] Current alternatives (including non-consumption) are listed
- [ ] Jobs are prioritized by opportunity score
- [ ] AI blueprint ties high-priority jobs to concrete capabilities
- [ ] Hypotheses are flagged separately from validated jobs

## Source

Originally a custom GPT: [Jobs to be Done](https://chatgpt.com/g/g-6802c7da3c688191875f67a5468d82e2-jobs-to-be-done)
