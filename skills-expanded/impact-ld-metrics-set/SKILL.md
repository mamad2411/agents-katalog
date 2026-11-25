---
name: impact-ld-metrics-set
description: Builds a short fixed set of measures for the L&D function in three kinds (efficiency, effectiveness, outcome), producing a reader and decision map, a metrics table with definition, source, owner and reader per measure, and a stop reporting list. Use for "run impact-ld-metrics-set", "L&D metrics", "learning and development metrics", "training KPIs", "what should L&D report", "L&D dashboard measures", "training metrics executives read", "stop reporting completions", part of the Claude Guide for Training Impact Pack by 90n.
---

# L&D Metrics Set

## When To Use
Your report is hours, completions and a satisfaction score, and nobody upstairs reads it. Use this when you want to fix, once, what the function reports: which few measures, for which reader, feeding which decision. It answers one question: what would our readers miss if we stopped sending it?

## When Not To Use
Not for filling the measures in: the set holds definitions and no results, and Quarterly L&D Report is the page that reports them. Not for one programme: use Kirkpatrick Data Collection Plan for a programme's collection schedule, or Success Measures Agreement for the measures one sponsor signs.

## Inputs
- The report or dashboard export you send today, pasted, or uploaded as a CSV file: the measure names are enough, group figures only.
- Who reads the function's figures (roles), what each decides with them, your plan for the period if it carries targets, and the measures already agreed with sponsors for your main programmes.
If you have none of this, I start from the list of what you report today and mark the output as a first draft.

## Approach
Three kinds of measure, a common way to sort a function's figures: efficiency (how much, at what cost), effectiveness (how good) and outcome (the business result the programmes were meant to move). One principle comes from the catalogue abstract of ISO/TS 30437:2023, "Learning and development metrics" (the abstract only; the full text was not read): the choice of metrics depends on who uses them and why, and a balanced set avoids unintended consequences. The failure this prevents is the report built from whatever your LMS exports: twelve efficiency counts, no reader, and a function that looks like a cost because cost is all it shows.

## Workflow
1. I ask three questions at once: who reads the function's figures and which decision each reader makes with them; what you report today (paste it); and the maximum number of measures you will allow, with where your plan's targets live.
2. Build the reader map first: reader, decision, how often they decide. Every measure you report today is then tested against it. A measure with no reader and no decision goes on the stop list, however long it has been reported.
3. Sort what survives into the three kinds. Efficiency: volume, cost, time. Effectiveness: reaction, learning, application on the job. Outcome: the business result. Show the count per kind plainly; a set that is all efficiency is the usual finding, and it explains why nobody reads it.
4. Fill the empty kinds from what already exists, never from a wish list. Outcome measures are the business's own measures, taken from the agreements your sponsors signed and read from their reports. If no programme has an agreed outcome measure yet, the row says "none agreed yet" and names the programme that should get one first.
5. Cut to your maximum, keeping at least one of each kind. For each measure kept, write the definition, how it is calculated in words, the source, the owner, how often it is read, the reader and the decision it informs. Targets come only from your plan; where there is none the cell says "no plan set". Ask for the set as a spreadsheet file if file creation is turned on; the table below is the default.
6. Run the balance check: for each measure, what could people do to make it look good without the work getting better, and which other measure in the set would show it. Volume with nothing on application rewards filling seats.
7. Write the stop list with a reason per line and who is told. Then the people check: anything that counts hours per person, or would rank named learners, trainers or managers, is rewritten for the group or removed.

## Output Format
```markdown
# L&D Metrics Set
Function: [name] · Fixed for: [period] · Maximum measures: [you set] · Owner of the set: [name, role] · Status: [first draft / agreed] · Cannot show yet: [what, and what it would take]
## Readers and decisions
| Reader (role) | Decision they make with L&D figures | How often they decide |
|---|---|---|
| [role] | [decision] | [frequency] |
## The set
| # | Kind | Measure | Definition | Calculated as (in words) | Source | Owner | Read how often | Reader | Decision it informs | Target from your plan |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [efficiency / effectiveness / outcome] | [measure] | [definition] | [calculation] | [system or report] | [name, role] | [frequency] | [role] | [decision] | [your figure / no plan set] |
## Balance check
| Kind | Measures in the set | What chasing them alone could cause | Balanced by |
|---|---|---|---|
| [kind] | [count] | [unintended consequence] | [measure #] |
## Stop reporting
| Measure | Reason to stop | Who is told, and by whom |
|---|---|---|
| [measure] | [no reader / no decision / counts people, not programmes] | [role] |
## Decision
[Name, role] agrees the set and the stop list by [date]; [name, role] tells each reader what changes from [period].
```

## Done When
- Every measure has a reader, a decision, a source and a named owner, or it is on the stop list.
- The set holds at least one measure of each kind and no more than the maximum you set.
- The target column holds only figures from your plan or the words "no plan set".
- The stop list has a reason per line, and no measure in the set counts or ranks a person.

## Quality Bar
- Short and fixed: the set does not change mid-year, so quarters compare. A change is dated and explained.
- Definitions are written so two people would calculate the same figure from the same export.
- The set contains no results. Figures belong in the report, with their voucher.
- Group level only: no per-person hours and nothing that tracks one manager's team by name. Privacy points: check with a qualified adviser.
- No target or benchmark is supplied by Claude; the set measures programmes and the function, never a person, and each measure has a named owner.

## Next
Run impact-quarterly-ld-report (Quarterly L&D Report) to report the set for the quarter.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
