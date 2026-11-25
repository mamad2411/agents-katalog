---
name: foundrole-resume-check
description: Check how hiring software (an ATS parser) reads a resume with the FoundRole MCP app, and report what the parser extracted and what it lost. Use when a user asks whether their resume is ATS-friendly, why applications get no reply, whether a parser can read their PDF, what a recruiting system sees on their resume, or asks for a resume scan, resume score, or resume review. Also use when the user pastes resume text and wants it checked. Do not use it to rewrite or grade the content of a resume — this check reports machine readability, not writing quality.
---

# FoundRole resume check

`resume_check` reports which parts of a resume hiring software can read. Report exactly what it returns.

## When `resume_check` is not available

This skill can load while the FoundRole app itself is disabled or not connected, so `resume_check` is missing from the session. Tell the user the FoundRole app is not enabled in this client, and that turning it on in the client's app or plugin settings (or connecting `https://www.foundrole.com/mcp`) and starting a new session makes the check available. Do not simulate the parse, and do not present your own reading of the resume as a FoundRole result or band.

## Choose what to check

- When the resume text is already in the conversation — pasted by the user, or read from a file they shared — pass it as `resume_text`. If the text is too short, ask for the full text.
- Pass `resume_id` when the user has identified an owned upload or editable version by its FoundRole ID. An editable version is checked as plain text.
- With neither input, the check runs on the account's primary upload.
- Do not paraphrase, reformat, or clean up the resume before passing it. The check measures what a parser reads from the actual text, so an improved version measures the wrong document.
- Check one resume per call. To compare two versions, call the tool once per version and contrast the returned bands and findings.

## Read the result

The response carries `mode`, `band`, `findings`, nullable `parsedAs`, and optional actions in `studioContinuation`, `profileSetupUrl`, and `parserReportUrl` or `studioReportUrl`.

- `mode` says which document was read: `uploaded` (an upload), `version` (an editable version), `text` (the pasted text), `no_resume` (nothing to check), `processing` (the upload is still being read).
- `band` is `strong`, `good`, or `partial`. Report the band in plain words. It is a readability band, not a percentage and not a match score — do not convert it into one, and do not invent a number to accompany it.
- `findings` lists what the parse lost, each with its own `detail` and suggested `fix`. Report every returned finding with its detail and fix; do not summarize several findings into one line, and do not add a finding the tool did not return. A single `clean` finding means nothing significant was lost. The returned findings are the scope of this check; do not invent hidden findings or advertise a more complete report.
- `parsedAs`, when present, is what the parser extracted: detected job title, years of experience, recognized skills count, sections, and which contact channels were found. Present these as the parser's reading, not as facts about the person — "the parser found no phone number" rather than "you have no phone number". When it is null, report the band and returned findings without inventing parsed facts.

## Explain what the check covers

- Pasted or extracted text cannot establish whether the original PDF or DOCX layout parses correctly. State this limitation when the user asks about a file; never present the text check as a test against a named ATS.

- This is the mechanical read only. It does not judge wording, achievements, seniority, or fit for any role. If the user asks whether the resume is good, say what the parser reads and what it loses, and keep any writing advice clearly separate from the tool's output.
- Never state or estimate a score, percentage, or pass rate for a specific ATS product, and never claim the resume will or will not pass a named system. The check describes typical parser behavior.

## Handle each mode

- `no_resume`: the account has no uploaded resume and nothing was pasted. Ask the user to paste their resume text. When `profileSetupUrl` is present, also offer to finish their profile for personalized job matches.
- `processing`: the upload is still being read. Offer to retry shortly, or to check pasted text right away.
- `text`: The check does not create a saved Resume Studio report or add a resume to the account. Report the returned findings and fixes directly in the conversation. Do not claim that the input is never stored: operational request records and diagnostics may retain it.
- `uploaded` or `version`: report the returned findings and fixes. When `parserReportUrl` is present, it opens the checked upload in Studio. `studioReportUrl` may also be present.

## Point to the next step

- When `studioContinuation` is present, offer **Continue in Resume Studio** after the findings. The `kind` tells the user what the link opens: `upload` to bring their file, `import` to build from the checked upload, or `edit` to open their editable version.
- **Open your saved resume report** is a supporting action when `parserReportUrl` or `studioReportUrl` is present. If there is no Studio continuation or report, `profileSetupUrl` offers **Finish your profile** for personalized job matches.
- Use the returned URLs. The band, findings, and fixes remain available in chat whether the user opens a link or stays in the conversation.
