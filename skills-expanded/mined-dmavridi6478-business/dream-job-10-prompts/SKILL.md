---
name: dream-job-10-prompts
description: Ten application prompts - decode the job description, tailor the CV, rewrite bullets (action + task + result), write the cover letter, build a role-fit matrix, fix ATS alignment, predict interview questions, build 8 STAR answers, get a recruiter-style review (shortlist/maybe/reject), and generate a full application pack. Use when the user is applying for a specific role and has the job description and their own background. Source Cyberman AI "10 Prompts to Land Your Dream Job" (Batch 102). Overlaps `job-application-5-prompts`; this set is wider (matrix, ATS, STAR x8, recruiter verdict, pack).
---

# 10 prompts to land your dream job

Replace the [paste] fields. Prompts are quoted from the slide. Run with `/dream-job <1-10>`. Truthfulness rule for every prompt: use only the user's real experience; mark anything missing as [ADD METRIC] or ask, never invent.

1. **Decode the job description.** "Act as a recruiter. Analyze this JD and extract key skills, responsibilities, ATS keywords, and standout traits in a table. Then tailor the resume to match the role." JD: [paste]
2. **Tailor the CV.** "Rewrite my CV for this role without adding false information. Improve the summary, bullets, and skills section using ATS keywords from the JD." CV: [paste] | JD: [paste]
3. **Rewrite the bullets.** "Rewrite these CV bullets using action + task + result format. Keep them concise and aligned with the JD. If metrics are missing, insert [ADD METRIC]." Role: [title] | JD: [paste] | Bullets: [paste]
4. **Write the cover letter.** "Write a tailored cover letter from my background. Highlight key achievements and match them to the company's needs." Background: [paste] | JD: [paste]
5. **Build a role-fit matrix.** "Create a role-fit matrix comparing my background to this JD - strengths, gaps, CV focus, cover letter points, and interview stories." Background: [paste] | JD: [paste]
6. **Fix ATS alignment.** "Compare my CV with this JD. Find missing keywords, weak areas, ATS issues, and rewrite my summary for better alignment." CV: [paste] | JD: [paste]
7. **Predict interview questions.** "Act as the hiring manager. Generate 15 likely interview questions grouped by technical, behavioral, and culture fit - with what a strong answer includes." Background: [paste] | JD: [paste]
8. **Build STAR answers.** "Create 8 STAR interview answers from my experience covering leadership, problem-solving, conflict, failure, and achievement." Background: [paste] | JD: [paste]
9. **Get a recruiter-style review.** "Review my CV and cover letter for this role. Give a verdict - shortlist, maybe, or reject - plus strengths, weaknesses, and quick fixes." CV: [paste] | Cover Letter: [paste] | JD: [paste]
10. **Generate a full application pack.** "Create a complete pack: CV summary, cover letter, interview questions, questions for the interviewer, a recruiter DM, and a follow-up email - using only my real experience." Background: [paste] | JD: [paste]

## Guidance
- Order that works: 1, 5, 6, 2, 3, 4, 9 (fix what the verdict says), then 7 and 8 before an interview; use 10 only once the CV is settled.
- Prompt 3 matches the formula in `job-application-5-prompts` and `cv-linkedin-prompts`; do not run both sets on the same CV.
- The slide says "this is how you compete in 2025"; the claim that one resume per job is "the old way" is the author's view, not data.
- The recruiter DM in #10 should follow `linkedin-job-search-5-hacks` (#4): reference something real, no ask for a job.
