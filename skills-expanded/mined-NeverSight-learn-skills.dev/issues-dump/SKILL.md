---
name: issues-dump
description: "I will dump things I consider not quite right to you and YOUR ONLY JOB IS TO slightly improve it to normal language then put them into github issues of this repository using gh cli."
---

# Issues Dump

When invoked, take the user's informal dump of issues/complaints and turn each one into a GitHub issue.

## What you do

1. Read `$ARGUMENTS` — this contains the user's raw dump of things that aren't quite right.
2. Parse it into individual issues. Each distinct complaint or observation becomes one issue.
3. For each issue:
   - **Title**: Clean up the language into a concise, normal-sounding issue title. Keep it short.
   - **Body**: Slightly improve the user's original wording into clear, natural language. Do NOT over-formalize, add templates, add acceptance criteria, or pad it out. Just make it read like a normal person wrote it.
4. Create each issue using `gh issue create`.

## Rules

- **Minimal transformation only.** The user's voice and intent should be preserved. You are a copyeditor, not a project manager. Don't add labels, milestones, or assignees unless the user explicitly mentions them.
- **Don't ask questions.** Just create the issues. If something is ambiguous, create the issue with the ambiguity intact — the user can refine it later.
- **Don't summarize or confirm each issue before creating it.** Just do it.
- **One `gh issue create` per issue.** Run them in parallel when possible.
- **Report back** with a short list of the created issues (title + URL) when done.
- If `$ARGUMENTS` is empty, ask the user what's bugging them.
