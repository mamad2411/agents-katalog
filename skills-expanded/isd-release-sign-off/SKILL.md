---
name: isd-release-sign-off
description: Assembles a release sign-off record for one course with the result of each check, its date and who ran it, the open issues with owners, a rights line, and the signer's written decision to release, fix first or stop. Use for "run isd-release-sign-off", "release sign-off record", "is this course ready to launch", "go or no-go for the course", "who signed off this course", "it was reviewed but there is no record", "final gate before release", "launch checklist for an e-learning course", part of the Claude for Instructional Designers Pack by 90n.
---

# Release Sign-Off Record

## When To Use
Launch is tomorrow and "it was reviewed" is the only evidence. You need one page that says which checks were run, on which version, by whom, what is still open, and who is putting their name to the release. It answers one question: can a named person sign this version, knowing exactly what was and was not checked?

## When Not To Use
This record collects results and reruns nothing. If a check has not been run, run it first: AI Content Accuracy Check, Does It Teach Review, Accessibility Check, Designer Run-Through, SME Review Round or Learner Pilot Test. To set the gates and the decider before the build, use Review and Sign-Off Plan. To tell learners what is going live, use Course Release Note.

## Inputs
- The version you intend to release, and the name and role of the person with the authority to release it.
- What you have from each check: date, who ran it by role, the version it ran on, the result in a line, open items.
- The open issues list, the sign-off table from your review plan if one exists, and who confirmed the rights to images, audio, video, fonts and quoted material.
If you have none of this, I start from the version name and the signer's name, write every check as "not reported", and mark the output as a first draft.

## Approach
This is a release gate with a named signer. The final gate asks the narrowest question of all, defects only: it is not the place to reopen objectives or structure. The closing question comes from a college's public human-in-the-loop review guide, which ends its review by asking whether you would attach your name to the content. The failure it prevents is the quiet one: six people each assume another one checked the captions, the course ships, and when a learner reports the problem nobody can say what was checked or on which version. In Claude Docs (beta) the record can be exported and filed; pasted into any conversation it works the same.

## Workflow
1. Ask at most three questions: which exact version is being released, who signs and by when, and which checks you can report on today. I take only what you report. I do not infer that a check happened because a file exists.
2. Fill one row per check in the check group: done or not done, date, who ran it by role, version checked, result in one line, open items. "Not done" is written as not done, with who accepted releasing without it. You decide whether a missing check is acceptable; I never soften the wording.
3. Compare each check's version with the release version. A check run on an older version is marked stale, and I list what changed since, from your change log. You judge whether the change touches what that check looked at.
4. List the open issues: each with an owner by role, a date, and whether it blocks release. Blocking is your call and the signer's. At this gate only defects are in scope; a request for new content goes back to the change rule in your plan.
5. Write the rights line: images, audio, video, fonts and quoted material, confirmed by whom and when. Where anyone is unsure about a licence or permission, check with a qualified adviser.
6. Put the question to the signer in writing: "Would you put your name on this version, with these checks and these open issues?" They answer in their own words and choose release, fix first (with the list) or stop. I leave the answer blank. I never sign and never propose the decision.

## Output Format
```markdown
# Release Sign-Off Record
**Course:** [title] | **Version to release:** [version] | **Planned release date:** [date] | **Record prepared by:** [role] on [date]
## Checks
| Check | Done or not done | Date | Run by (role) | Version checked | Stale? | Result in one line | Open items | If not done or stale: what changed, who accepted it, why |
|---|---|---|---|---|---|---|---|---|
| AI Content Accuracy Check | [done / not done] | [date] | [role] | [version] | [yes / no] | [result] | [items] | [change, role, reason] |
| Does It Teach Review | [done / not done] | [date] | [role] | [version] | [yes / no] | [result] | [items] | [change, role, reason] |
| Accessibility Check | [done / not done] | [date] | [role] | [version] | [yes / no] | [result] | [items] | [change, role, reason] |
| Designer Run-Through | [done / not done] | [date] | [role] | [version] | [yes / no] | [result] | [items] | [change, role, reason] |
| SME Review Round | [done / not done] | [date] | [role] | [version] | [yes / no] | [result] | [items] | [change, role, reason] |
| Learner Pilot Test | [done / not done] | [date] | [role] | [version] | [yes / no] | [result] | [items] | [change, role, reason] |
## Open issues
| Issue | Where | Owner (role) | Due | Blocks release? |
|---|---|---|---|---|
| [issue] | [screen or file] | [role] | [date] | [yes / no] |
## Rights and the signer's question
Images, audio, video, fonts and quoted material confirmed by [role] on [date]. Unsure about: [item, or "nothing"]; if anything, check with a qualified adviser.
"Would you put your name on this version, with these checks and these open issues?" Answer, in the signer's words: [written by the signer]
## Decision
[Signer's name and role] decides by [date]: [release / fix first / stop]. If fix first: [the list, each with an owner and a date]. Signed on [date] for version [version].
```

## Done When
- Every check in the check group has a row, and none says "done" without a date, a role and a version you reported.
- Each check on an older version than the release is marked stale, with what changed.
- Every open issue has an owner, a date and a yes or no on blocking, and the rights line names who confirmed it or says it is unconfirmed.
- The signer's answer and the decision are empty until the signer fills them.

## Quality Bar
- The record is internal, with one line per result in plain words. No score, grade or percentage for the course or for anyone.
- Names appear only as the signer and the check owners, by role and date. No tally of who was late or wrong.
- A stale check is never presented as current, "reviewed" is never accepted without a version, and new content requests go to the sponsor, not into the fix list.
- Claude assembles the record from what you report; a named person signs, and a check that was not run is written as not run.

## Next
Run isd-release-note (Course Release Note) to tell people what is going live.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
