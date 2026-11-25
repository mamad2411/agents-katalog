---
name: isd-designer-run-through
description: Prepares the protocol for taking your own course start to finish as one kind of learner, then sorts your notes into a step-by-step issues log with the severity you set and your own verdict. Use for "run isd-designer-run-through", "I have never taken my own course", "prepare a run-through before reviewers see it", "I will take it as a new starter on a phone", "sort my run-through notes", "walk through the build step by step", "is it ready for reviewers", "what happens when one learner takes the whole thing", part of the Claude for Instructional Designers Pack by 90n.
---

# Designer Run-Through

## When To Use
You built it, you reviewed it screen by screen, and you have never once taken it. Use this on the built course, before any reviewer or learner opens it. It answers one question: what happens when one learner takes the whole thing, in order, on the device they really use?

## When Not To Use
A desk review against objectives, which also works on a storyboard, is Does It Teach Review. Keyboard and screen reader testing lives in Accessibility Check. This is you, alone: other people's comments are SME Review Round, and real learners are Learner Pilot Test. If you want Claude to take the course for you, no skill here does that.

## Inputs
- The learner kind you will be, from the Learner Analysis: role, what they already know, device, place, time they have.
- The built course, on the real device, and the time learners are told it takes. Afterwards: your rough notes, pasted as they are.
If you have none of this, I start from a one-line description of the learner and the course, prepare the protocol, and mark the output as a first draft.

## Approach
This is a cognitive walkthrough, from the Nielsen Norman Group article "Evaluate Interface Learnability with Cognitive Walkthroughs", adapted here from interfaces to a course. At each step it asks four things: will users try to achieve the right result, will they notice the correct action is available, will they associate that action with the result they want, and will they see progress after it. Any "no" fails the step. Claude prepares the protocol and sorts what you wrote. It does not take the course, does not imagine a learner's reactions and does not fill the log. The failure this prevents: the designer who has opened one screen from the editor again and again and never arrived at it tired, on a phone, after every screen before it.

## Workflow
1. Ask up to three questions: which learner kind this run is for, on which device and in what setting, and how many runs you plan (one per learner kind; you decide).
2. Write the learner kind at the top as a role description, never a named person. Set the conditions: the real device, the real setting as far as you can, one sitting, start to finish, sound as that learner would have it, no skipping, no fixing on the way. Notes only.
3. Take the course. At every step answer the four questions in course terms: would they know what they are trying to do here; would they see what to do next; would they connect that action to the goal; did what came back tell them whether they were right, and why? Log each "no" with the step and what happened, in a few words, and note your own start and end time.
4. Paste the rough notes. Claude sorts them into the log in step order, groups repeats, and adds nothing: no issue you did not write, no guessed cause.
5. Set a severity on each issue yourself: blocks the learner, slows or confuses, cosmetic. Record the time you took against the time learners have.
6. Write the verdict in your own words: ready for reviewers, or fix these first. State the limit: you know too much to stumble like a novice, which is why the pilot exists.

## Output Format
```markdown
# Designer Run-Through Log
Course: [name, version] | Run by: [designer name, role], [date] | Run [n] of [n planned]
## Learner kind and conditions
| Learner kind (role, what they already know) | Device | Setting | Sound | One sitting, no skipping, no fixing? |
|---|---|---|---|---|
| [role description, not a named person] | [device] | [place] | [on / off / captions] | [yes, or what was different] |
## Step log (every "no")
| Step or screen | Know what they are trying to do? | See what to do next? | Connect the action to the goal? | Told if right or wrong, and why? | What happened |
|---|---|---|---|---|---|
| [step] | [yes / no] | [yes / no] | [yes / no] | [yes / no] | [designer's note] |
## Issues
| Issue | Steps where it appears | Severity (blocks the learner / slows or confuses / cosmetic), set by the designer | Fix before reviewers? |
|---|---|---|---|
| [issue, in the designer's words] | [steps] | [severity] | [yes / no] |
## Time
Time I took: [measured by the designer] | Time learners are told: [as stated] | Time learners have: [from the Learner Analysis]
## Verdict, in the designer's words
[Ready for reviewers, or fix these first, and why.]
Limit: as the person who made this course, I know too much to stumble where a novice would. [What the pilot should watch.]
## Decision
Run-through done by [designer name] on [date], version [x], as [learner kind] on [device]. [Designer name] decides: ready for reviewers, or the listed issues are fixed by [date] and the affected steps are run again.
```

## Done When
- The log names one learner kind, the device and the conditions actually met.
- Every "no" has a step, a note in your words and a severity you set, and the time taken is your own measurement next to the time learners have.
- The verdict and the limit are written by you, with a date and the version.

## Quality Bar
- Every row comes from your notes. A row Claude could not find in them is deleted.
- No simulated learner, no predicted reaction, no "a typical learner would".
- The learner kind is a role description, never a real named person.
- You run through the course yourself before anyone else does; Claude prepares the protocol and sorts your notes, and does not take the course for you.

## Next
Run isd-sme-review-round (SME Review Round) now that you have taken it before anyone else.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
