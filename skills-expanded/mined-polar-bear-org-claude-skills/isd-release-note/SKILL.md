---
name: isd-release-note
description: Drafts a course release note with what the course is for and who should take it, a dated version entry saying what changed in the learner's terms, known limits, the content owner and review date, and an upload note for the person who runs your LMS. Use for "run isd-release-note", "course release note", "what changed in this version of the course", "announce the new course", "note for the LMS administrator", "course change log", "tell learners what is new", "who needs to retake the course", part of the Claude for Instructional Designers Pack by 90n.
---

# Course Release Note

## When To Use
The course goes live with a file name and nothing else. Learners do not know whether it is for them, managers do not know what changed, and the person who runs your LMS has to guess what it replaces. Use this when a version has been signed for release and you need to say, on one page, what is going live and what it means for each reader.

## When Not To Use
Not before the release decision exists: the internal record of checks and the signature is Release Sign-Off Record, and this note is drafted from it. A one-page aid people keep at work has its own upkeep line in Job Aid Template. Reading how the course did once it is live is Course Data Review.

## Inputs
- The change log for this version, the signed release record, and the previous release note if there was one.
- The course purpose, the audience by role, how long you say it takes, and the file or package name as produced by your authoring tool.
- The content owner by role, the review date, and their decision on who retakes.
If you have none of this, I start from the course title and the list of changes you can vouch for, and mark the output as a first draft.

## Approach
The method is the Keep a Changelog convention, adapted here from software to a course: notes written for people, not machines, an entry for every version, the latest first, the release date shown, and changes grouped by type. The adaptation is the wording. A developer's entry says a screen was edited; a learner needs "the refund limit section now reflects the new rule". The failure this prevents: version three replaces version two silently, half the audience completed the old one, and nobody can say whether they need to do anything. Claude Docs (beta) suits a note you export and file; a plain conversation works too.

## Workflow
1. Ask at most three questions: which version and release date, who the content owner is, and whether people who completed an earlier version must do anything. That last answer is the content owner's decision. If it is not made yet, I leave it open and say so at the top.
2. Read the change log and the release record, and list only changes that happened in this version. Anything I cannot find there is marked `[to confirm with the content owner]`, never filled in from memory or from the design document's intentions. Then write the part for learners and managers: what the course is for, who should take it and who need not, the duration you gave me, and the known limits. You judge which limits are worth stating; an honest "the scenario covers phone calls only" saves a complaint later.
3. Write the version entry, latest first, with the date. Group changes as Added, Changed, Removed and Fixed, each in the learner's terms. Deprecated and Security are used only if they apply, in plain words, for example a module that will be withdrawn at the next version.
4. Write the part for the person who runs your LMS: file or package name, version, what it replaces, the settings you ask for, who to contact. I write the note only. The package and the tracking happen in your authoring tool and your LMS.
5. Add upkeep: content owner by role, review date, and the triggers for an earlier update, such as a rule, product or process change. Then you read both parts as each reader would and cut what they do not need.

## Output Format
```markdown
# Course Release Note
**Course:** [title] | **Version:** [version] | **Release date:** [date] | **Content owner:** [role]
## For learners and managers
**What this course is for:** [one or two sentences, as the task people will do]
**Who should take it:** [roles] | **Who need not:** [roles] | **How long it takes:** [duration you provide]
**If you completed an earlier version:** [what to do, as decided by the content owner, or "decision pending"]
## What changed in version [version], released [date]
| Type | What changed, in the learner's terms | Where |
|---|---|---|
| Added | [change] | [lesson or screen] |
| Changed | [change] | [lesson or screen] |
| Removed | [change] | [lesson or screen] |
| Fixed | [change] | [lesson or screen] |

**Earlier versions, latest first:** [version, release date, summary of changes]
## Known limits and upkeep
- Known limits: [what the course does not cover, or a known issue and when it will be fixed]
- Upkeep: content owner [role], review date [date], earlier update if [rule, product or process change]
## Upload note for the person who runs your LMS
| File or package name | Replaces | Settings requested | Contact |
|---|---|---|---|
| [name as produced by your authoring tool] | [version or file name, or "new course"] | [audience, due date, completion rule, as you specify] | [role] |
## Decision
[Content owner, by role] confirms what changed and who retakes by [date]; [the person who runs your LMS] publishes version [version] on [date].
```

## Done When
- Every change in the note can be found in the change log or the release record.
- The version and date sit at the top, the latest version comes first, and the upload note says what this version replaces.
- A learner can tell in the first lines whether the course is for them and whether they must retake it, and the owner, review date and update triggers are filled in or marked open.

## Quality Bar
- Changes are written as what the learner will notice, not as screens edited, and known limits are stated plainly.
- No claim about results, effectiveness or time saved. The duration is yours, and empty change types are removed, not padded.
- Rule or policy changes are worded as the content owner approved them. Legal or regulatory wording: check with a qualified adviser.
- Claude drafts the note from your change log; the content owner confirms what changed, and nothing is announced that was not done.

## Next
Run isd-course-data-review (Course Data Review) once the course has been live long enough to have data worth reading.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
