---
name: ldg-map-the-curriculum
description: Builds a curriculum map with modules by objective, practice, check and format (live, e-learning, on the job), the orphan modules and orphan objectives, a sequence from simpler to harder whole tasks, and the learning path. Use for "run ldg-map-the-curriculum", "curriculum map", "curriculum mapping", "learning path", "map the modules to objectives", "programme structure", "our modules do not connect", "sequence these modules", part of The Complete Claude Guide for L&D Pack by 90n.
---

# Map the Curriculum

## When To Use
A programme has grown module by module and nothing connects. Each piece arrived with its own request, and you need one page that shows which module serves which objective, with what practice and check, in which format and in what order.

## When Not To Use
The map holds the formal modules only. For the assignments, coaching and peer learning around them, run Build the 70-20-10 Plan; for one new hire's weeks, run Plan the Onboarding. For a single course, Write the Design Document is enough.

## Inputs
- The agreed objectives, and the design document if there is one
- The current module list: title, format, length, what each covers, any existing check
- The real cases the role handles, from routine to exception, and the formats and time people can get
If you have none of this, I start from a module list and one sentence on the role, and mark the output as a first draft.

## Approach
The method is backward design (a university teaching-centre guide) for the grid, and Merrill's First Principles of Instruction (2002 paper) for the sequence: whole tasks from simpler to harder, and inside each module activate, demonstrate, apply, integrate. The grid is written from the objective outward, so a module has to earn its row. The failure this prevents: a path where people sit through four modules of background before they meet a single real case, and the one module that practises the hard case is optional because it was added last.

## Workflow
1. Ask three questions: which objectives must the programme deliver, which modules exist or are planned, and which formats and how much time can people really get?
2. Build the grid, one row per module: objective, practice, check and format. Fill each cell from the objective, not from what the module contains today. A module with content and no practice is labelled a reading.
3. Find the orphans. A module with no objective gets a proposal (cut, merge or move to reference) and a reason its requester can accept. An objective with no practice or no check gets a proposal for where it goes. Nothing is removed silently.
4. Let the format follow the practice: live for practice with other people and feedback, e-learning for decisions someone can rehearse alone, on the job for the real task done with a person.
5. Sequence by whole task, simple to hard: a routine case, then one with a complication, then an exception. Topics that only matter in the hard case move later, even if the manual puts them in chapter one.
6. Check the four phases in every module: activate (a problem they have met), demonstrate (a worked example), apply (the practice), integrate (use at work before the next module). Mark what is missing in the phase-check column, and flag every module with no apply.
7. Lay out the path: order, format, duration and the gap before the next step. You set every duration and gap; they stay [placeholders] until you do. The grid can be a spreadsheet file, if file creation is on.

## Output Format
```markdown
# Curriculum Map
Programme: [name] | Role: [role] | Version: [v1] | Date: [date]
## Grid
| Module | Objective | Practice | Check | Format | Whole task (routine / complication / exception) | Phase check (missing) |
|---|---|---|---|---|---|---|
| [M1] | [objective 1] | [practice, or "reading"] | [check] | [live / e-learning / on the job] | [routine case] | [none / no apply / no integrate] |
## Orphan modules
| Module | Asked for by (role) | Proposal | Reason |
|---|---|---|---|
| [module] | [role] | [cut / merge into M2 / reference] | [no objective needs it] |
## Orphan objectives
| Objective | What is missing | Proposed place |
|---|---|---|
| [objective] | [practice / check] | [module] |
## Learning path
| Step | Module | Whole task | Format | Duration | Gap before next |
|---|---|---|---|---|---|
| 1 | [M1] | [routine case] | [format] | [duration] | [gap] |
## Decision
[L&D lead name] and [sponsor name] approve the map, with its cuts and merges, by [date]; [L&D lead name] tells each module's requester what was decided.
```

## Done When
- Every module traces to an objective, or sits on the orphan list with a proposal and a reason
- Every objective has at least one practice and one check
- The path runs from simpler to harder whole tasks, not by topic
- Every module has an apply phase, or is flagged; durations and gaps are your figures or placeholders

## Quality Bar
- Format follows the practice, never the other way round
- A module nobody can tie to an objective is named as an orphan, however senior its requester
- The hard case is on the main path, and informal learning is noted as out of scope, never squeezed into a module row
- Claude drafts the map; the L&D lead and the sponsor approve the cuts and merges, and checks in the grid measure the programme, never a person

## Next
Run ldg-write-the-scenarios (Write the Scenarios) to build the practice the map calls for.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
