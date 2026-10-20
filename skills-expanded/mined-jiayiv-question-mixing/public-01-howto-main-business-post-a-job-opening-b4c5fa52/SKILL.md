---
name: post-a-job-opening
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 30min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Publish an approved job opening with accurate role details, fair hiring language, and a traceable posting record.

## Preconditions

- The role, budget, level, location, and hiring manager are approved.
- You have access to the applicant tracking system or job board.
- The job description has been reviewed for pay, requirements, and inclusive language.

## Steps

1. **Open the requisition.** Sign in to the recruiting system and select the approved requisition or create one from the approved template. → *Expect:* the role record is visible with the correct hiring manager.
2. **Enter core details.** Add title, department, employment type, location, work arrangement, compensation range if required, and application deadline. → *Expect:* the posting fields match the approved role.
3. **Paste the job description.** Add responsibilities, required qualifications, preferred qualifications, benefits, and EEO statement. → *Expect:* the preview reads clearly and avoids unnecessary exclusionary criteria.
4. **Set application questions.** Add only job-related screening questions and required documents. → *Expect:* applicants are asked for information needed to evaluate the role.
5. **Choose posting channels.** Select internal board, external careers page, and approved paid boards. → *Expect:* each intended channel is checked or scheduled.
6. **Review compliance fields.** Confirm equal opportunity language, pay transparency, location eligibility, and data retention notices. → *Expect:* required compliance fields show complete.
7. **Publish the opening.** Submit the posting for publication after final review. → *Expect:* the system shows a posted, pending, or scheduled status.
8. **Notify stakeholders.** Send the posting link to the hiring manager, recruiter, and approvers. → *Expect:* stakeholders can open the live or scheduled posting.

## Decision points

- If the compensation range is missing where required → pause and obtain the approved range before publishing.
- If a requirement may screen out protected groups unnecessarily → ask the hiring manager to justify or remove it.
- If the role is confidential → use the confidential requisition process and limit visibility.

## Failure modes & recovery

- **F1 Missing approval:** detect absent budget or headcount approval → keep the posting in draft and request approval.
- **F2 Posting rejected:** detect board validation errors → correct the flagged fields and resubmit.
- **F3 Biased wording:** detect gendered, age-coded, or nonessential language → replace with job-related neutral wording.

## Verification

The job has a live, pending, or scheduled posting status, the posting link opens correctly, and the requisition record contains approved role details and compliance text.

## Variations

- US: include required pay transparency, EEO, work authorization, and state-specific notices where applicable.
- Other countries: adapt salary disclosure, privacy notice, disability accommodations, and employment category language to local law.
- Internal-only opening: restrict the channel to the internal job board and confirm visibility rules.

## Safety & privacy

Medium risk because hiring decisions and candidate data are involved. Use job-related criteria, avoid discriminatory language, collect only necessary applicant data, and handle EEO or demographic information separately from selection decisions.
