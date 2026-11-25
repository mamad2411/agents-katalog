---
name: job-search-interview-prep
description: Builds a single-page interview cheat sheet (company snapshot, role details, talking points, questions to ask, watch-outs) for a specific interview. Triggers on "prep me for the interview at X", "make a cheat sheet for this posting", "interview prep for [company]", or when the user pastes a job posting/interview invite and asks to get ready for it.
---

# Interview cheatsheet

Read `${CLAUDE_PLUGIN_ROOT}/shared/conventions.md` and `profile.md` from
project memory for the person's background and target profile. If
`tracker-data.md` exists, read it and pull anything already known about this
company/role (status, source, notes, contact).

## Gather the specifics

From the user's message, a pasted job posting, a pasted email/calendar
invite, or by asking directly, get: company name, role title, interview
stage (recruiter screen / hiring manager / panel / onsite), date/time,
format (phone/video/onsite), and interviewer name + title if known. Don't
block on any of these — fill in what's available and leave the rest as
placeholders in the output, but ask the one or two most important missing
pieces (usually: which stage, and interviewer name if there is one) rather
than guessing.

## Research

Use web search / fetch to gather, for the company: what they do and how they
make money, funding/stage or public financials, employee count, key
customers, recent news (last 6-12 months — funding, layoffs, leadership
changes, product launches), and if findable, a read on interview culture or
common complaints (Glassdoor/Blind-style, cited generally — don't fabricate
specifics you can't find). For the role: pull responsibilities from the
posting/tracker if available.

Cross-reference the person's background (`profile.md` + resume summary)
against the role to build 4-5 genuine talking points — specific experience
that maps to what this role needs, not generic advice.

## Build the page

Fill in `references/cheatsheet-template.html` (read it, replace every
placeholder with real content, delete any section you truly have nothing
for rather than leaving placeholder text). Recolor `.header` background and
the accent colors (`.stat .num`, `.talking-point` border/strong color) to
loosely match the company's brand color if obvious (e.g. a well-known brand
color); otherwise leave the template's default blue-gray. Keep it to what
fits on one or two scrolls — dense but scannable, this gets read minutes
before a call.

Save the filled-in file and deliver it with `SendUserFile` (renders inline
so it's easy to pull up on a phone right before the call). Don't publish it
as a persisted Artifact — these are single-use per interview, not something
to keep a permanent link to; if the user asks for a link version, that's a
reasonable exception.

If a matching entry exists in `tracker-data.md`, update its `notes` with the
interview date/stage now scheduled, then run the sync procedure from
`shared/conventions.md` to refresh the webpage view.
