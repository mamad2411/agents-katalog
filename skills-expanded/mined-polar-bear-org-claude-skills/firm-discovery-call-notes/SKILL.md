---
name: firm-discovery-call-notes
description: Sorts your discovery call notes, or a transcript made with everyone's consent, into the client's words marked verbatim, facts, figures with unit and period, your inferences marked as yours, contradictions with the brief, open questions and the agreed next step. Use for "run firm-discovery-call-notes", "sort my call notes", "what did the client actually say", "pull their exact words from my notes", "clean up these discovery notes", "turn this consented transcript into a record", "I scribbled notes during the call", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Discovery Call Notes

## When To Use
You were listening, steering and typing at once, because there is nobody else to take notes. The page in front of you mixes things the client said with things you concluded. Run this the same day, while you can still tell a quote from your own shorthand. It answers: what did they say, and what did you only infer?

## When Not To Use
For a message to the client, use Discovery Recap Email; this record stays private. If the record is already clean and you want the problem in one statement, go to Problem Statement.

## Inputs
- Your notes as they stand, or a transcript only if everyone on the call agreed to it at the start
- Who attended, by role
- Optional: your brief reading, pre-call hypotheses and cost of waiting sheet, to check for contradictions
If you have none of this, I start from what you remember, told in your own words, and mark the record as a first draft from memory with no verbatim lines.

## Approach
This is verbatim capture as qualitative researchers practise it, described generically: a quote, a stated fact and your own inference go into separate bins because they carry different weight later. The judgment sits in the doubtful lines. A paraphrase that slips into quotation marks will reach the proposal as the client's words, and clients notice sentences they never said. In doubt, a line is a fact and not a quote.

## Workflow
1. Ask, in one go: was the call recorded or transcribed, and did everyone agree at the start? Who was there, by role? What next step was agreed before you hung up? With no consent I work from your notes and set any transcript aside.
2. Place every line in one of five bins. Verbatim: the exact words, inside quotation marks, with the role of whoever said them. Fact: stated, not word for word. Figure: a number with its unit, its period and who gave it. Inference: your conclusion, labelled as yours. Open question: what is still unknown.
3. Apply the quote test to each line in the first bin: can you say these were the exact words? If not, it moves to fact. Shorthand such as "budget frozen" is a fact. Inside quotation marks I leave the client's grammar as it was.
4. Check each figure for its unit and period. A bare number stays in the record flagged "[unit to confirm]" and adds a line to the open questions.
5. Compare with the brief and your hypotheses if you have them. Write each contradiction flatly (the brief said this, the call said that) and mark each hypothesis confirmed, weakened or untouched.
6. Write the agreed next step with an owner by role and a date, or write "none agreed". A call that ended without one is information to keep, not to hide.

## Output Format
```markdown
# Call Record
Call: [date] · Present: [roles] · Recorded: [no / yes, all agreed at the start]
## Their words (verbatim)
| Quote | Speaker (role) | Topic |
|---|---|---|
| "[exact words]" | [role] | [topic] |
## Facts and figures
| Item | Figure and unit | Period | Said by (role) |
|---|---|---|---|
| [fact] | [figure or none] | [period] | [role] |
## My inferences
- Inference: [conclusion, and the line it comes from]
## Contradictions and hypotheses
- [Brief or hypothesis] against [what was said]: [confirmed / weakened / untouched]
## Open questions
1. [question] · ask [role]
## Agreed step
[Step] · Owner: [role] · Date: [date] (or "none agreed")
## Decision
[You] decide by [date] whether the record is complete enough to play back to the client, and which open questions go into the recap.
```

## Done When
- Each line of your notes has landed in one bin and one only
- Each quotation mark holds words you can vouch for, with a speaker role
- Each figure has a unit, a period and a source, or a "[to confirm]" flag
- The agreed step has an owner and a date, or reads "none agreed"

## Quality Bar
- Speakers appear by role; no comment on anyone's mood, manner or attitude
- Inferences are labelled every time, including the obvious ones
- Nothing is added that was not in the notes; gaps become open questions
- Rules on recording differ from place to place; check with a qualified adviser
- Quotes are only words that were said, and a transcript is used only with everyone's consent; I invent no client quote and no figure.

## Next
Run firm-discovery-recap-email (Discovery Recap Email) to play the call back to the client in their own words.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
