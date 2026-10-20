---
name: screen-a-resume
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 15min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Evaluate one candidate resume against job-related criteria and record a fair, consistent screening decision.

## Preconditions

- The job description and screening rubric are available.
- You have access to the candidate record in the applicant tracking system.
- You know which criteria are required, preferred, or disqualifying.

## Steps

1. **Open the candidate record.** Review the resume, application answers, and source in the applicant tracking system. → *Expect:* the candidate materials are visible in one record.
2. **Check minimum qualifications.** Compare education, certifications, experience, location, and work authorization only where job-related and lawful. → *Expect:* each required criterion is marked met, not met, or unclear.
3. **Assess relevant experience.** Look for evidence of responsibilities, tools, scope, outcomes, and progression that match the role. → *Expect:* the resume has a concise job-related evidence summary.
4. **Ignore protected traits.** Do not use age, race, gender, disability, family status, national origin, religion, or other protected characteristics. → *Expect:* notes avoid protected-class assumptions.
5. **Apply the rubric.** Score or categorize the candidate using the same rubric used for comparable applicants. → *Expect:* the decision is tied to documented criteria.
6. **Choose the next status.** [BRANCH: advance | hold | reject] move qualified candidates forward, hold unclear cases for recruiter review, and reject clear nonmatches. → *Expect:* the candidate has the correct workflow status.
7. **Write neutral notes.** Record factual reasons such as "missing required certification" or "matches required payroll experience." → *Expect:* another reviewer can understand the decision.

## Decision points

- If a required qualification is unclear → mark for follow-up instead of assuming the answer.
- If the resume indicates a possible accommodation need → do not screen out; route through the accommodation process if needed.
- If the hiring manager requests inconsistent criteria → escalate to recruiting or HR before applying them.

## Failure modes & recovery

- **F1 Rubric drift:** detect notes based on "culture fit" or personal preference → rewrite against job-related criteria.
- **F2 Missing resume:** detect an empty or unreadable attachment → request a readable document before deciding.
- **F3 Duplicate candidate:** detect another active record for the same person → merge or flag according to ATS policy.

## Verification

The candidate record has a documented screen result, rubric-based notes, and no selection rationale based on protected traits or non-job-related assumptions.

## Variations

- US: keep EEO data separate and do not use protected-class information in screening.
- Other countries: follow local rules for work authorization, age, photo resumes, and data retention.
- High-volume roles: use structured knock-out questions only when validated as job-related.

## Safety & privacy

Medium risk because resumes contain PII and screening affects employment opportunity. Access candidate data only for recruiting work, document job-related reasons, and apply criteria consistently across candidates.
