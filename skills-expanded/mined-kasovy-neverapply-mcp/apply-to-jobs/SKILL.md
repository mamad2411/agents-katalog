---
name: apply-to-jobs
description: Apply to jobs through NeverApply, answer screening questions on a held application, and approve or dismiss a held application. Use when the user wants to apply to a job, send an application, or asks about an application that waits for their approval or answers.
---

NeverApply never sends an application without the user's approval of that exact job. Follow these steps in order.

1. Confirm the job with the user by its title and company, and confirm which resume to send: the default resume, a tailored variant from `tailor_resume`, or the uploaded resume. Do not continue until the user clearly says yes to this named job in this conversation.
2. Call `apply_to_job` with the `listing_id`, `job_approved: true` and an `idempotency_key` such as `apply-<listing_id>`. If you call it again for the same job, use the same key.
3. Read `status` and `next_action` in the result and tell the user what happened:
   - The application is queued: the user gave this assistant permission to send. Say that it is queued, not that it is delivered.
   - The application is held for approval: nothing went to the employer and nothing was charged. Offer to approve it now, or give the `application_url`.
   - `status` is `waiting_for_answers` and `next_action` is `answer_screening_question`: call `get_application` with the `run_id`. Show each open question with its offered choices and let the user pick. Then call `answer_screening_question` with every choice and the current `review_version`.
   - `next_action` is `open_review`: give the user the `review_url`. These questions need the NeverApply website.
4. To send or dismiss a held application, ask the user first. Then call `approve_application` with the `run_id`, the current `review_version`, `decision` (`send` or `dismiss`) and `job_approved: true`.

Never pick an answer for the user. Never guess identity, residence, work authorization, salary or demographic answers. If a tool reports `upgrade_required` or too few credits, say so plainly and stop.
