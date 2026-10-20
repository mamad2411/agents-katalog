---
name: hiring-patterns
description: "When to activate: job description writing, structured interviews, hiring rubrics, interview panel design, offer calibration, candidate pipeline management, recruiting process"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: business-ops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Hiring Patterns

## Job Description Template

```
[Title] — [Team] at [Company]

About the role (3–4 sentences):
What will this person own? What does success look like in 12 months?
What makes this role uniquely interesting?

What you'll do (5–7 bullets — outcomes, not tasks):
- [Outcome-oriented bullet: "Own X to achieve Y"]
- [Outcome-oriented bullet]
- [Outcome-oriented bullet]

What we're looking for (split must-have from nice-to-have):
Must-have:
- [Specific skill / experience — be concrete, avoid vague adjectives]
- [Minimum years of relevant experience, if necessary]

Nice-to-have (do NOT gatekeep on these):
- [Domain knowledge]
- [Tooling familiarity]

What we offer:
- Salary range: $X–$Y (be transparent — it widens your funnel)
- Equity: [range or description]
- Benefits: [2–3 lines]
- Location: [remote / hybrid / onsite + timezone expectations]

Interview process (set expectations up front):
1. Application review (1 week SLA)
2. Recruiter screen — 30 min
3. Hiring manager interview — 45 min
4. Technical / skills assessment — [format]
5. Panel interviews — 3 × 45 min
6. Offer

[Company] is an equal opportunity employer.
```

### JD Anti-Patterns to Avoid
- "Rock star," "ninja," "wizard" — exclusionary
- 10+ years required for junior roles
- Long lists of technologies without context
- No salary range — reduces diverse applicant pool
- Culture-fit language without definition
- "Fast-paced" / "dynamic" with no substance

---

## Structured Interview Design

### Interview-to-Criteria Mapping
Map each interview to specific competencies. No competency assessed twice unless it's critical.

| Interview | Competencies assessed | Format |
|-----------|----------------------|--------|
| Recruiter screen | Communication, baseline fit, logistics | Phone/video, 30 min |
| Hiring manager | Role motivation, strategic thinking, leadership | Behavioral, 45 min |
| Technical | Domain skill, problem-solving, code quality | Skills assessment |
| Cross-functional | Collaboration, communication style | Behavioral, 45 min |
| Values / culture | Integrity, growth mindset, values alignment | Behavioral, 30 min |

### Behavioral Question Formula (STAR)
"Tell me about a time when you [situation requiring competency]."
- **S**ituation: what was the context?
- **T**ask: what were you responsible for?
- **A**ction: what specifically did you do?
- **R**esult: what was the measurable outcome?

### Sample Questions by Competency

**Execution / Ownership**
- Tell me about a project where you drove something to completion despite significant obstacles.
- Describe a time you took ownership of something outside your formal role.

**Strategic Thinking**
- Walk me through how you'd prioritize [relevant problem] if you had limited resources.
- Tell me about a decision you made that required thinking 12+ months ahead.

**Collaboration**
- Describe a time you had to influence someone without authority over them.
- Tell me about a disagreement with a peer or manager — how did you handle it?

**Growth Mindset**
- What is a significant professional mistake you've made? What did you learn?
- How do you stay current in [relevant domain]?

**Values-Based**
- Tell me about a time you had to choose between what was easy and what was right.
- Describe a situation where you had to deliver difficult feedback.

---

## Hiring Rubric

### Scoring Scale
| Score | Label | Definition |
|-------|-------|-----------|
| 4 | Strong Yes | Exceptional evidence; would advocate loudly |
| 3 | Yes | Clear evidence; comfortable hiring |
| 2 | No | Weak or missing evidence; significant concerns |
| 1 | Strong No | Disqualifying signals |

### Rubric Template per Competency
```
Competency: [Name]
Definition: [2-sentence description of what this looks like in practice]

4 — Strong Yes:
  [Concrete behavioral description of exceptional performance]

3 — Yes:
  [Concrete behavioral description of solid performance]

2 — No:
  [Concrete behavioral description of insufficient evidence]

1 — Strong No:
  [Concrete behavioral description of disqualifying behavior]
```

### Debrief Protocol
1. All interviewers submit scores before debrief (no anchoring)
2. Recruiter reads scores aloud — highest first, lowest last
3. Start with dissenters: ask "Strong No" to share reasoning first
4. Hiring manager gives final recommendation
5. Document decision rationale in ATS for every candidate
6. No hiring committee majority required if hiring manager has clear conviction + no Strong No from functional expert

---

## Panel Design

### Interview Panel Composition (5-person example)
| Panelist | Relationship to role | Focus |
|----------|---------------------|-------|
| Hiring manager | Direct supervisor | Role fit, strategy, leadership |
| Senior peer | Daily collaborator | Technical depth, collaboration style |
| Cross-functional stakeholder | Partner team lead | Cross-functional working style |
| Skip-level manager | Future growth manager | Long-term potential, values |
| HR / recruiter | Process owner | Values, culture, logistics |

### Panel Coordination Rules
- Brief every panelist before interviews (share role criteria, JD, candidate context)
- Each panelist covers different competencies — no duplicates
- Panel feedback submitted within 24h of interview
- Hiring manager is final decision authority, not consensus vote

---

## Offer Calibration

### Offer Components
| Component | Considerations |
|-----------|---------------|
| Base salary | Market data (Levels.fyi, Radford, Option Impact), internal equity, location |
| Equity | Stage-appropriate, strike price, vesting schedule (4yr / 1yr cliff standard) |
| Bonus | Target %, metrics, payout frequency |
| Signing bonus | Use to bridge unvested equity gap — make explicit in offer |
| Benefits | Health, dental, vision, 401k match, PTO policy |
| Start date | Negotiate — candidates need time for transitions |

### Compensation Bands
- Maintain salary bands per level per function
- Publish bands internally (reduces inequity)
- Offer within band — exceptions require VP+ approval
- Review bands annually vs. market data

### Offer Delivery Best Practices
1. Deliver verbally first — gives you ability to negotiate in real-time
2. Follow up in writing within 24h
3. Set a deadline (5–7 business days standard)
4. Assign a buddy to answer questions during decision period
5. Close the loop immediately if declined — ask for specific reason

---

## Pipeline Management

### ATS Stage Definitions
| Stage | Definition | SLA to advance or disposition |
|-------|-----------|------------------------------|
| Applied | Application received | 5 business days |
| Recruiter screen | Scheduled or completed | 3 business days post-screen |
| HM interview | Scheduled or completed | 3 business days post-interview |
| Assessment | Sent or in progress | 5 business days |
| Panel | Scheduling or in progress | 5 business days |
| Offer | Extended, negotiating, or closed | 7 business days |
| Closed | Hired / rejected / withdrew | — |

### Pipeline Health Metrics
| Metric | Formula | Target |
|--------|---------|--------|
| Time to fill | Req open date → accepted offer | < 45 days |
| Offer acceptance rate | Accepted / offers extended | ≥ 85% |
| Pipeline conversion | Hired / total applicants | Benchmark by role type |
| Diverse slate rate | % roles with diverse finalist | ≥ 50% |
| Interviewer calibration | % scorers whose ratings correlate with performance | Track quarterly |

### Candidate Experience Standards
- Acknowledge every application within 5 business days
- No interview ghost — disposition every candidate you interview
- Provide feedback when declined post-panel (if legal / policy allows)
- Send surveys after each stage — act on low scores
