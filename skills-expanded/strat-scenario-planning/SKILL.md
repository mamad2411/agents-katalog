---
name: strat-scenario-planning
description: Builds a scenario model with base, upside and downside for each option on the two or three drivers that separate them, the one assumption that flips the choice and early signals with thresholds the owner sets, as an editable spreadsheet. Use for "run strat-scenario-planning", "scenario planning for our product strategy", "model base, upside and downside for the leading option", "which assumption flips the choice?", "replace the single forecast line", "what early signal tells us we are in the downside?", "stress-test the chosen option against the others", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Scenario Planning Model

## When To Use
One forecast line is in the plan and everyone knows it is wrong, but nobody can say how wrong or in which direction. A leading option has come out of the comparison and you want to know whether it still leads when the few things you do not control go well or badly. It answers one question: which single assumption would flip the choice, and how would we see it coming?

## When Not To Use
If the question is how big the space is, use Market Sizing (TAM, SAM, SOM). If the option is settled and the person who funds it wants costs, use Business Case. If the argument is about how much each criterion should count, that is the weight check inside Decision Matrix, not a driver model.

## Inputs
- The Strategic Option Set, do nothing included, and which option currently leads
- The outcome measure the decision cares about and the horizon
- Baseline figures you hold (usage, conversion, retention, price, cost), each with its source and date
If you have none of this, I start from the options and the outcome measure, label every value "assumption" and mark the output as a first draft.

## Approach
Scenarios as plausible futures, with a one-at-a-time sensitivity check. Both are common practice with no single originator. A scenario is a setting of the few drivers that matter. It is not a forecast and it carries no probability. The judgment is in picking the drivers that pull the options apart and holding everything else still. The failure this prevents: three columns where every cell moves by the same percentage, which is one forecast drawn three times.

## Workflow
1. Ask at most three questions: the outcome measure and horizon, which baseline figures are confirmed and where each comes from, and which option leads today.
2. Pick the two or three drivers that most separate the options (for example adoption, price realised, retention, time to deliver). Write why each one matters. Every other input stays at base, and a driver that moves all options alike is dropped.
3. Set base, upside and downside per driver, per option, do nothing included. Each value carries a source and date or the label "assumption". Figures from what your customers did beat a borrowed figure; say which is which.
4. Build the spreadsheet with file creation (switch on "Code execution and file creation"): one input tab with every driver value and its label, one tab per option, one summary tab. Formulas visible, no hard-coded results. In a plain chat the same model comes out as tables.
5. Sensitivity: move one assumption at a time across its range and record the single assumption that flips the preferred option, and the value where it flips. That is the finding. If nothing flips it, say so.
6. Early signals: for each scenario an observable sign, the threshold the owner sets, where it is read and how often. A signal nobody is named to watch is not a signal.

## Output Format
```markdown
# Scenario Model
**Options:** [list, do nothing included] | **Leading option:** [option] | **Outcome measure:** [measure] | **Horizon:** [period]
## Drivers
| Driver | Why it separates the options | Base | Upside | Downside | Source and date, or assumption |
|---|---|---|---|---|---|
| [driver] | [reason] | [value] | [value] | [value] | [source, date / assumption] |
## Outcomes by option
| Option | Base | Upside | Downside |
|---|---|---|---|
| 0 Do nothing | [result] | [result] | [result] |
## The assumption that flips the choice
[Assumption] moves the preferred option from [A] to [B] past [value]. Evidence today: [source / assumption].
## Early signals
| Scenario | Signal | Threshold (owner sets) | Where read | How often | Watched by (role) |
|---|---|---|---|---|---|
| Downside | [sign] | [threshold] | [source] | [cadence] | [role] |
## Decision
[Decision owner role] confirms by [date] whether the leading option stands, which assumption is tested first and which role watches each signal.
```

## Done When
- Every driver value has a source and date, or the label "assumption"
- The spreadsheet opens, the formulas are visible and the inputs can be changed
- The assumption that flips the preferred option is named with its value, or "none found" is stated
- Each scenario has a signal, a threshold the owner set and a role that watches it

## Quality Bar
- Two or three drivers only; a model with ten hides which one matters
- Do nothing is modelled with the same care as every other option
- No probabilities and no single "expected" line anywhere in the model
- Drivers are about the product and the market, never figures for a named person
- An unsourced value is an assumption in plain sight; scenarios are never presented as forecasts, and the owner sets every threshold.

## Next
Run strat-red-team-review (Red Team Review) to have the leading option argued against before anyone commits to it.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
