---
name: track-applications
description: Track the user's job applications and prepare for interviews with NeverApply. Use when the user asks about application status, what waits for them, follow-ups, quiet or stale applications, a resume tailored to a job, or interview preparation.
---

To track applications:

1. Call `list_applications`. Use `status` to narrow the list when the user asks for one group: `needs_answer` or `ready_to_send` for what waits for the user, `stale` for applications with no recent activity, or `interview` and `offer`.
2. Summarize `record` first in one or two lines: how many applications were sent, how many are not confirmed, how many wait for the user, and how many were not sent. Then list the rows that matter for the question.
3. For one application, call `get_application` with its `application_id` or `run_id`, and tell the user its `next_action`. For a held application, use the apply-to-jobs skill.

To prepare documents for a job:

- Tailored resume: call `tailor_resume` with the active `listing_id`. The copy is written in the background. While `status` is `generating`, call it again with the same `listing_id` in about a minute; a repeat call reads the same copy and does not pay for a second one. When it is ready, give the user the `studio_url` and the score change.
- Interview preparation: call `prepare_interview` with the `application_id`, or with the `listing_id` for a job without an application. The pack is written in the background. While `status` is `generating`, call it again with the same ID in about a minute. When it is ready, summarize the sections that are useful now.

Both tools need a paid NeverApply plan and use no application credits. If a tool reports `upgrade_required`, tell the user it is a paid feature. Do not retry. If the text says the last attempt failed, tell the user.

Call `send_feedback` only when the user asks to report a problem or send feedback, and use the user's own words.
