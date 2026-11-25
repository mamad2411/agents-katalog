---
name: pmjob-linkedin-profile
description: Checks and redrafts your LinkedIn profile from pasted text, giving a list of mismatches with your resume to fix first, a section check, three headline options, an About in your own voice and a claim map tying every claim to an evidence row. Use for "run pmjob-linkedin-profile", "fix my LinkedIn profile", "LinkedIn headline for a product manager", "write my About section", "my profile sounds like AI wrote it", "does my profile match my resume", "LinkedIn profile for a senior product designer", part of the Claude Guide for Product Interviews Pack by 90n.
---

# LinkedIn Profile Rewrite

## When To Use
Your profile undersells senior work, or a chatbot rewrote it and it now reads like everyone else's. Run this once the resume is settled, to answer: what on my profile does not match my record, what is missing, and how do I say what I do in my own voice?

## When Not To Use
If the role lines of your resume are not written yet, run Product Resume Bullets first; this skill takes those lines as they stand. If you cannot yet name the role you want next, run Target Role Brief, which owns the word list.

## Inputs
- Your profile as pasted text or as its PDF export, and your resume
- Your Career Evidence Inventory and the "shown" words from your Target Role Brief
- Three short samples of your own writing (an email, a document intro, a post)
If you have none of this, I start from the pasted profile and your resume alone, and mark the output as a first draft.

## Approach
The section list comes from LinkedIn Help, Create a good LinkedIn profile, which also notes that the profile strength meter measures completion only. The truth check against the resume is a practice rule and it runs first, because polish on a wrong date makes the date more visible. The failure this prevents: an interviewer with your resume in one tab and your profile in the other, finding two different titles before you say a word.

## Workflow
1. Ask up to three questions: which target role the profile should speak to, whether anything on the profile is newer than the resume, and which contact route, if any, you want public.
2. Truth pass first. Match every title, date, result and skill on the profile to the resume and to an evidence row. List each mismatch with what the record shows; a claim with no row is a mismatch. These are fixed before any new wording.
3. Section check against the LinkedIn Help list: photo, headline, About, experience and education, work samples, skills, recommendations, custom address. Each is present, missing or weak, with one reason. No score and no percentage.
4. Write three headline options that differ in what leads: role-led, proof-led (one evidence row), problem-led (the kind of problem you are hired for). Only "shown" words. You check the length on the site's own counter; I quote no limit.
5. Draft the About in one or two paragraphs and four moves: what you do now; what you are good at, with one concrete example from a row; what you want next; how to reach you, only if you chose a route. Take the voice from your three samples: sentence length, contractions, spelling. Every adjective about you is replaced by the example that shows it, or cut.
6. Build the claim map: claim, row ID, status (shown or gap). Give one version and one alternative opening line, so you edit a draft and do not pick between five.

## Output Format
```markdown
# LinkedIn Profile Rewrite
## Mismatches to fix first (target role [role], checked [date])
| Claim on the profile | Resume or evidence row says | Fix |
|---|---|---|
| [title, date, result or skill] | [what the record shows] | [correct the profile / correct the resume / remove] |
## Section check
| Section | Status | Reason |
|---|---|---|
| [Photo / Headline / About / Experience and education / Work samples / Skills / Recommendations / Custom address] | [present / missing / weak] | [one line] |
## Headline options
| # | Leads with | Headline | Rows behind it |
|---|---|---|---|
| 1 | Role | [headline] | [E_] |
| 2 | Proof | [headline] | [E_] |
| 3 | Problem | [headline] | [E_] |
## About draft and alternative opening line
[Paragraph 1: what you do now, and what you are good at, with one example] [Paragraph 2: what you want next, and how to reach you if you chose a route] [Alternative opening line: one line]
## Claim map
| Claim | Evidence row | Status |
|---|---|---|
| [claim] | [E_] | [shown / gap] |
## Decision
You decide which mismatches to correct, choose one headline, edit the About in your own words and paste it in yourself, by [date].
```

## Done When
- Every mismatch is listed with what the record shows, ahead of any new wording
- Every section has a status and one reason, and the three headlines differ in what leads, each with its rows
- Every claim in the About appears in the claim map, and no adjective about you survives without its example

## Quality Bar
- Works only from text you paste or export; I never open the live page and never act in your account.
- The check is of the profile, never of you, and never against anyone else's profile. No contact detail, location or personal data is added by default.
- Role lines come from the resume as they are; a gap in the claim map stays a gap.
- Every claim on the profile maps to an evidence row and matches the resume; you edit it in your words and paste it yourself.

## Next
Run pmjob-product-sense-case (Product Sense Case) to start preparing the rounds.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
