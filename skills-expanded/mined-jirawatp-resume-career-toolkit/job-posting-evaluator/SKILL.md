---
name: Job Posting Evaluator
description: Analyze a job posting against a resume to score fit, surface gaps, flag red flags, and recommend whether to apply. Use this skill when someone pastes a job description and asks if they should apply, wants a match score, needs gap analysis, wants to understand job requirements, or asks about red flags in a posting. Also trigger for "am I qualified", "is this worth applying to", or any resume-to-JD comparison request.
---

# Job Posting Evaluator

Score how well a resume matches a job posting and decide whether the application is worth the effort.

## Evaluation Process

### 1. Decompose the Job Posting

Break every requirement into one of three buckets:

**Hard Requirements** -- non-negotiable qualifications
- Specific degrees or licenses ("must have CPA")
- Minimum years of experience ("5+ years required")
- Named technical skills repeated 3+ times
- Legal requirements (clearance, work authorization, certifications)

**Soft Requirements** -- strong preferences
- "Preferred" or "nice to have" qualifications
- Industry-specific experience
- Tool proficiency mentioned 1-2 times
- Advanced degrees listed as preferred

**Cultural Signals** -- clues about work environment
- Language about pace, autonomy, collaboration style
- Mentions of travel, on-call, or hours
- Benefit and perk descriptions
- Company values and mission statements

### 2. Score the Match

For each hard and soft requirement, check whether the resume provides evidence:

```
MATCH SCORING

Hard Requirements: X of Y matched
  [requirement]: [MATCH / PARTIAL / MISSING]
  ...

Soft Requirements: X of Y matched
  [requirement]: [MATCH / PARTIAL / MISSING]
  ...

Hard Match Rate: X%
Weighted Score: (Hard Rate x 0.7) + (Soft Rate x 0.3) = Z%
```

**Score interpretation:**
- 85%+: Strong fit, apply immediately
- 70-84%: Good fit, worth a tailored application
- 55-69%: Stretch, apply only if the role is compelling and gaps are addressable
- Below 55%: Poor fit, spend time on better-matched roles

### 3. Gap Analysis

For each missing requirement, classify:

**Dealbreaker:** Cannot be fixed (missing license, missing clearance, 10+ year experience gap). Recommendation: do not apply.

**Addressable:** Can be mitigated in cover letter or interview (missing one tool that is similar to ones you know, 1-2 years short on experience, missing a "preferred" qualification). Recommendation: apply with a plan to address.

**Irrelevant:** Listed but unlikely to be enforced (degree requirement when the role clearly values experience, "preferred" items in a list of 15). Recommendation: ignore.

### 4. Red Flag Scan

Scan the posting for warning signs:

**Scope creep signals:**
- Role combines two distinct jobs ("engineer who also does sales")
- Unrealistic skill breadth ("expert in 8+ languages")
- Vague responsibilities covering everything

**Culture warning signs:**
- "We are a family" (boundary issues)
- "Must thrive in chaos" (poor management)
- "Rockstar/ninja/guru" (immature culture)
- Posting has been open 90+ days (something is wrong)
- "Competitive salary" with no range (likely below market)
- "Unlimited PTO" (often means less PTO taken)

**Compensation red flags:**
- No salary range posted when law requires it
- "DOE" with zero guidance
- Heavy emphasis on equity with no mention of base
- Commission-only for non-sales roles

### 5. Application Strategy

If the score supports applying, provide:

**Resume adjustments:** Which bullets to lead with, which keywords to add, which skills to reorder.

**Cover letter angles:** 2-3 specific points connecting the candidate's experience to the employer's stated needs.

**Gaps to address proactively:** Which missing requirements to acknowledge and how to frame them positively.

**Timeline:** How quickly to apply based on posting age and competition level.

## Output Template

```
JOB FIT REPORT

Position: [title]
Company: [name]
Match Score: X%
Recommendation: [APPLY / APPLY WITH CAVEATS / SKIP]

REQUIREMENT BREAKDOWN
Hard Requirements (X/Y matched):
  [requirement] -- [MATCH/PARTIAL/MISSING] -- [note]
  ...

Soft Requirements (X/Y matched):
  [requirement] -- [MATCH/PARTIAL/MISSING] -- [note]
  ...

GAPS
Dealbreakers: [list or "none"]
Addressable: [list with mitigation strategy]

RED FLAGS: [list or "none detected"]

APPLICATION PLAN
Resume changes: [specific adjustments]
Cover letter hooks: [2-3 angles]
Gap framing: [how to address missing items]
Priority: [HIGH/MEDIUM/LOW based on fit and role quality]
```
