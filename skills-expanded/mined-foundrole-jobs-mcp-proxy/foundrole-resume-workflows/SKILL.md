---
name: foundrole-resume-workflows
description: Use FoundRole to review a saved profile or resume, preview tailoring for a job, check evidence of job fit, explain a resume parser result, or start a cover letter grounded in saved experience.
---

# FoundRole resume and application workflows

| Request | Tool |
|---|---|
| Read the career profile on the account | `profile_get` with no arguments |
| Read the actual saved resume text | `resume_get` with an optional `resume_id` |
| Preview a tailoring improvement for a specific job | `job_application_preview` with `workflow: "tailoring"` |
| See which saved evidence supports fit for a specific job | `job_application_preview` with `workflow: "fit"` |
| Get a cover-letter starting point for a specific job | `job_application_preview` with `workflow: "cover_letter"` |
| Explain what a resume parser read or missed | `resume_check` |

## Choose the resume and posting

Use the exact `id` returned by `jobs_search` as `job_id` in an application preview, and pass `resume_id` for a specific saved version. Without `resume_id` these tools use the account's primary or only resume, or return version choices. If `resume_get` returns `nextOffset`, continue with the same `resume.id` as `resume_id`, the returned `revision`, and `nextOffset` as `offset`. A `restart` status means the saved text or requested page changed. A processing state means the upload is still being read.

If a personal read or preview asks for consent, reconnect FoundRole in the host and approve sharing the saved profile and resume. If the resume or posting is unavailable, ask for the intended source. When no evidence or requirement is returned, say what is missing. A gap in the saved evidence is not proof the person lacks the skill.

## Explain the preview

An application preview can return `requirement`, `resumeEvidence`, `evidenceGap` and `guidance`. Use those returned fields. Tailoring offers a specific change or clarification, fit describes the evidence that supports the requirement, and a cover-letter starting point uses the evidence the tool returned. Fit does not establish eligibility or predict a hiring decision.

When the response has a `continueUrl`, present `continueLabel` with it. If `savesJobOnOpen` is true, the link saves the posting to the tracker when opened. The preview itself only reads. The user chooses whether to open the continuation.

For parsing, `resume_check` takes `resume_id` for an owned resume or `resume_text` for text supplied in the conversation. With neither argument it checks the primary upload. Explain its `band`, the returned `findings` and their fixes, and `parsedAs` when present. `parserReportUrl` or `studioReportUrl` can open the same saved upload. Keep the parsing result separate from job fit and writing quality.
