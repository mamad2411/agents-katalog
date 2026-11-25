---
name: isd-course-project-setup
description: Drafts a setup sheet for one course in Claude, with the approved sources to load, standing instructions ready to paste, a list of what never goes in and a version naming rule. Use for "run isd-course-project-setup", "set up a Claude project for this course", "every chat starts from zero", "Claude keeps making things up", "draft from my sources only", "what can I upload to Claude", "standing instructions for a course", "stop Claude filling the gaps", part of the Claude for Instructional Designers Pack by 90n.
---

# Course Project Setup

## When To Use
Every chat starts from zero, so you paste the same manual again, and where the manual is silent Claude fills the gap with detail that sounds right. Use this once per course, before the first draft, to answer one question: what does Claude work from on this course, and what does it do when the sources run out?

## When Not To Use
Not for deciding which sources are approved: that is Source Content Triage, and this sheet only loads its result. Not for checking a finished draft (AI Content Accuracy Check) or for voice rules (Learning Content Style Guide). For a single question on a single file, attach the file and ask.

## Inputs
- The approved source list from your triage (each file with its date, owner and version) and the working documents you already have (brief, objectives, design document, style guide)
- Your organisation's rule on what may be loaded into an AI tool, or who owns that rule, and how you name versions today
If you have none of this, I start from the files you name and their dates, and mark the output as a first draft.

## Approach
The method is grounding in supplied sources, from Anthropic's documentation "Reduce hallucinations": allow "I don't know", ask for word-for-word quotes first, have each claim cite a supporting quote and withdraw it if none is found, and restrict answers to the documents provided. Anthropic says these reduce invented claims and do not remove them, so this sheet is a setup and never a check. The failure it prevents is quiet: a superseded procedure sits in the workspace next to the current one, and the draft blends the two into a step that exists in neither.

## Workflow
1. Ask at most three questions: which sources the expert approved and in which version, who owns the rule on what may be loaded, and whether you work in Projects (the redesign is in beta on select plans) or in a plain conversation with the files attached. Both work; the sheet is written for either.
2. Build the source list: one row per approved source with date, owner by role and version. Superseded, undated and ownerless files stay out and are listed as left out, with the reason. You decide borderline cases with the expert; I never promote a file.
3. Write the "never goes in" list before anything is loaded: learner names and results, pilot notes with names, personal data, confidential material your organisation has not cleared for this use. Whether a document may be loaded is your organisation's rule: ask whoever owns that policy, and on data protection check with a qualified adviser.
4. Draft the standing instructions, ready to paste, on the four techniques: use only the loaded sources for facts; quote the passage before using it; write `[to confirm with the expert]` where the sources are silent; say "not in the sources" instead of guessing; never invent a case, a name, a figure or a quote; mark every example fictional. You edit the wording so it fits how you brief a colleague.
5. Add the working documents the course produces as it goes (brief, objectives, design document, style guide), so a draft follows decisions already signed. Set one version naming rule for drafts and for sources, so every later check can say which version it ran on. Keep it short enough that you will follow it on a bad day.
6. Give the five-minute test for you to run: three questions whose answers are in the sources and one whose answer is not. The setup works if the fourth gets "not in the sources". You run it and record what came back; I do not mark my own test.

## Output Format
```markdown
# Course Project Setup Sheet
Course: [course name] | Workspace: [Project or conversation] | Set up by: [role] | Date: [date]
## Sources to load
| Source | Date | Owner (role) | Version | Approved by (role) |
|---|---|---|---|---|
| [file or section] | [date] | [role] | [version] | [role] |
## Left out, and never goes in
| File or kind of material | Reason (superseded, undated, no owner, learner data, personal data, not cleared) | Who rules on it (role) |
|---|---|---|
| [file or material] | [reason] | [role] |
## Standing instructions (paste as written)
1. [Use only the loaded sources for facts, and quote the passage and its place before using it.]
2. [Where the sources are silent, write "[to confirm with the expert]" or say "not in the sources".]
3. [Never invent a case, name, figure or quote. Mark every example fictional.]
## Working documents and version rule
| Document | Current version | Naming rule |
|---|---|---|
| [brief, objectives, design document, style guide] | [version] | [rule you set] |
## Five-minute test
| Question | Answer in the sources? | What came back | Result |
|---|---|---|---|
| [question] | [yes or no] | [reply] | [as expected or not] |
## Decision
[Designer, by name] decides by [date] whether the workspace is ready for drafting. [Policy owner, role] confirms by [date] what may be loaded.
```

## Done When
- Every loaded source has a date, an owner and a version, nothing undated is in the list, and the "never goes in" rows are written with the policy owner named
- The standing instructions can be pasted without editing, and you ran the test: the question with no answer got "not in the sources"

## Quality Bar
- No learner data in the workspace, ever: no names, no results, no pilot notes that identify anyone
- A file left out is listed with its reason, so nobody loads it later by habit
- Instructions are specific ("be accurate" is not one), and when a source changes the list changes the same day
- The setup lowers the risk of invented detail and does not remove it: the checks and the expert's sign-off still happen.

## Next
Run isd-style-guide (Learning Content Style Guide) to give the workspace one voice.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
