---
name: pmjob-resume-bullets
description: Writes your Product Resume Bullets, two to four lines per role as challenge, action, result, each with scope and the decision you made, your part kept apart from the team's and a number only with a source you could show. Use for "run pmjob-resume-bullets", "write my product manager resume bullets", "my resume reads like a job description", "resume lines for a senior product designer", "quantify impact without making numbers up", "turn launches into resume lines", "order my resume for this role", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Product Resume Bullets

## When To Use
Your resume is a list of launches and reads like the job description. "Shipped X, led Y, owned Z" says what existed, not what you decided or what it cost. Run this to answer: how do I write each role in a few lines that show scope, my call and the result, with nothing I could not defend in an interview?

## When Not To Use
If you have not yet recorded what you did in each role, run Career Evidence Inventory first. For the headline, the About text and the profile checks, run LinkedIn Profile Rewrite; this skill writes the role lines of the resume only.

## Inputs
- Your Career Evidence Inventory, with the rows and the do-not-claim list
- Your Target Role Brief, for the "shown" words and the order of lines
- Your current resume or your own draft lines, and three short samples of your own writing
If you have none of this, I start from each role's title, dates and one decision you made there, and mark the output as a first draft.

## Approach
Each line follows challenge, action, result, a common careers-service convention, with two additions for experienced people: scope and the decision. The rule on figures is a practice rule: no source, no number. One published candidate policy on AI use asks candidates to write their own first draft and refine it afterwards, and this skill works in that order. The failure it prevents: a team's result written as yours, with a rounded figure you can no longer source, and an interviewer who asks how it was measured.

## Workflow
1. Ask up to three questions: which roles go on and which target role sets the order, whether you have your own draft lines, and what records you hold behind any number.
2. Per role, set the header as held: title, employer as you state it, dates. Never a title you did not hold.
3. Start from your own draft where you have one. Write two to four lines per role, fewer for older roles. Each line: challenge (what needed deciding or fixing), action (what you did, "I"), result (what changed), with scope and the decision inside the line. A launch-list line is rebuilt around the decision behind the launch.
4. Apply the number rule: a figure appears only with its source noted under the entry. Without one, the result stays in words and the note reads `[no source: described in words]`. Never round up, never estimate.
5. Keep the team's part apart from yours: "the team cut [result]", "I led the [decision] that [result]". Check every line against the do-not-claim list.
6. Order the lines within each role by relevance to the target role, using only "shown" words from the Target Role Brief. A word marked "partly" needs wording that stays true.
7. Tighten in your voice, taken from your three samples: sentence length, plain verbs, your spelling. Claude Docs can hold the resume as a document you edit; a chat works too.

## Output Format
```markdown
# Product Resume Bullets
Target role: [role] · Updated: [date] · Status: [first draft / checked against records]
## [Title as held] · [employer as you state it] · [dates]
| Line | Scope | Decision | Row | Source for any number |
|---|---|---|---|---|
| [challenge, action, result in one sentence] | [team, users or surface] | [the call you made or shaped] | [E_] | [source / no source: described in words] |
## [Title as held] · [employer as you state it] · [dates]
| Line | Scope | Decision | Row | Source for any number |
|---|---|---|---|---|
| [challenge, action, result in one sentence] | [team, users or surface] | [the call you made or shaped] | [E_] | [source / no source: described in words] |
## Do-not-claim check
| Item on the list | Line it touches | What was done |
|---|---|---|
| [team result or someone else's decision] | [line] | [written as the team's / removed] |
## Target role words used
- [word] · shown, row [E_]
## Decision
You check every title, date and figure against your records, put the lines into your own words and decide which version goes out, by [date].
```

## Done When
- Every role has two to four lines, each with a scope, a decision and a row ID
- Every number has a named source, or no number appears
- Titles and dates match your records
- Every line has been checked against the do-not-claim list

## Quality Bar
- Lines read as plain sentences in your voice, not strings of keywords.
- The decision is visible in every line; "shipped" alone is not a line.
- No client name, internal figure or confidential detail; colleagues appear by role.
- Only "shown" words from the Target Role Brief; nothing is borrowed from an ad to fill a gap.
- No number without a source you could show, no title you did not hold, and the team's result is never written as yours.

## Next
Run pmjob-linkedin-profile (LinkedIn Profile Rewrite) to bring the profile in line with the resume.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
