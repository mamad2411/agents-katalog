---
name: build-sample-data-plan
description: Plans the invented data a prototype runs on as a Sample Data Plan with every field it needs, an invented value for each one, the cases to cover (empty, long, odd characters, large volume), the places real data is tempting and why it stays out, and who approves any exception. Use for "run build-sample-data-plan", "can I paste a customer export into the prototype", "make the demo look real without real data", "what fake data do I need", "generate sample data for my prototype", "which edge cases should my data cover", "who has to approve using real data", part of the Claude for Product Builders Pack by 90n.
---

# Sample Data Plan

## When To Use
You are about to paste a customer export "just to make the demo look real". Stop and run this first, before any data goes into the prototype. It answers: what data does the prototype need, can all of it be invented, and who would have to say yes if not?

## When Not To Use
If the prototype is built and you are about to send a link, run Personal Data Check, which looks for real data that got in anyway. If you think the prototype needs live data from another tool, that question belongs to Connector Plan.

## Inputs
- The screens or the flow, and the fields each one shows
- The belief on your test card
- The places you are tempted to use real data, described, never pasted
If you have none of this, I start from a one-line description of the main screen and mark the output as a first draft.

## Approach
The method is data minimisation as the UK Information Commissioner's Office sets it out (ico.org.uk, data protection principles, data minimisation): data should be adequate, relevant and limited to what is necessary, and not held on the off-chance it might be useful. A prototype's purpose is to test a belief, and invented data is adequate for that. The GOV.UK Service Manual advises creating a character and matching documents when real data cannot be used (gov.uk/service-manual/user-research/using-moderated-usability-testing). The failure it prevents: a full customer export sitting in a folder, a chat and a shared link, to fill a table that needed a handful of invented rows. On any privacy question, check with a qualified adviser.

## Workflow
1. Ask up to three questions: which screens and fields does the prototype show, which belief is it testing, and where are you tempted to use real data?
2. Run the purpose test in the principle's three words. Adequate: is invented data enough to test the belief? Relevant: does each field have a rational link to that belief? Limited: drop every field the flow does not show.
3. Write one row per field: what it is, an invented value with a realistic shape (the right length, format and range), and the cases it must cover.
4. Cover four cases: empty, very long, odd characters, large volume. You set the volume. These feed the empty, error and loading states in your user flow; a table that only ever holds tidy rows hides the layout problems a tester would hit.
5. Keep invented meaning invented. A real record copied and lightly edited is still real data. Build a character with matching details instead, and make names and contact details plainly fictional, for example an address at example.com.
6. For each place real data is tempting, write why, and what invented data does instead. Any exception names the role who must approve it, before it happens, with the reason written down. Then Claude generates the data from the plan, and you read a sample of rows yourself for anything that could be taken for a real person.

## Output Format
```markdown
# Sample Data Plan
Prototype: [name] | Belief tested: [from the test card] | Written by: [role] | Date: [date]
## Purpose test
Invented data is adequate for this belief because [reason]. Fields dropped as not needed: [list].
## Fields
| Field | What it is | Invented example | Shape rule | Cases to cover |
|---|---|---|---|---|
| [field] | [meaning on screen] | [invented value] | [length, format, range] | [empty / long / odd characters] |
## Cases
| Case | Screen where it shows | Rows or values needed |
|---|---|---|
| Empty | [screen] | [what is left blank] |
| Very long | [screen] | [which field, how long] |
| Odd characters | [screen] | [accents, symbols, other scripts] |
| Large volume | [screen] | [number set by the builder] |
## Where real data is tempting
| Place | Why it is tempting | What invented data does instead | Exception asked? | Approved by (role), on (date, before use) |
|---|---|---|---|---|
| [screen or field] | [reason] | [invented substitute] | [no / yes, with the reason] | [none / role, date] |
## Decision
[Named approver, by role] approves or refuses each exception by [date]; with none approved, [builder, by role] uses invented data only.
```

## Done When
- Every field on every screen in the flow has a row
- All four cases have a place they show up, and no example value comes from a real record
- Each tempting place has an invented substitute or a named approver
- A person has read a sample of the generated rows

## Quality Bar
- No real export, screenshot or record is pasted to "show the shape". Describe the shape in words.
- No invented record is recognisable as a real person; names and contact details are plainly fictional.
- An exception approved after the data went in is not an approval. It is logged as a breach of the plan.
- No real customer data goes into the prototype; any exception is approved by a named person first. Privacy points: check with a qualified adviser.

## Next
Run build-connector-plan (Connector Plan) if the prototype still seems to need live data.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
