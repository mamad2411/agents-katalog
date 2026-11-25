---
name: reach-useful-material-match
description: Matches your own materials to one person's facts, with each item checked against what the research found, none, one or two that fit with the fact that makes them fit, and what you must not send. Use for "run reach-useful-material-match", "useful material match", "what can I share with them", "which article should I send", "something useful to share", "match my content to this prospect", "what do I send that is not a brochure", "resource to share", part of the Claude Guide for Outreach Pack by 90n.
---

# Useful Material Match

## When To Use
You want to share something useful, and everything you have feels like a brochure. This answers: of the things I have written, said or made, does any one fit what this person is working on, and if none does, can I accept that?

## When Not To Use
If you have no materials at all, skip this and go to Talking Points; a plain question is a fine substitute. If you have not researched the person, there is nothing to match against: run Person Research Brief first.

## Inputs
- Your own materials list: articles, a checklist, a talk, a case note you are allowed to share, each with one line on what it covers. Keep it in a Project (beta) if you want it available every time.
- This person's numbered facts and the reason you chose, or are leaning to.
- Anything you may not share: client work under confidentiality, drafts, material that is not yours.
If you have none of this, I start from three materials you describe in a line each and two facts about the person, and mark the match as a first draft.

## Approach
Match your material to the facts, and zero is a valid answer: a generic research discipline. An item fits only when you can point to the fact about this person or their organisation that makes it relevant. Everything else is sending your marketing to a stranger. I choose from your list only and never write, summarise or invent a material. The failure it prevents is the "thought you might find this interesting" link that has nothing to do with them.

## Workflow
1. Ask at most three questions: which materials are on your list, what you may not share, and which reason to write you are leaning to.
2. Write one line per material on what it helps a reader do. If I cannot say it from your description, I ask; I do not guess the content.
3. Check each material against the numbered facts. It fits only if a named fact makes it relevant, and the fit is written as "because [fact number]".
4. Run the brochure test on every fit: would this person want it if you sold nothing? Material whose main job is to describe your services fails, however good it is.
5. Keep none, one or two. Never more than two, and never two when one is clearly better. "None fits" is written plainly and is a normal result.
6. List what must not be sent: confidential work, anything that names a client without agreement, anything that failed the brochure test.
7. Stop before the message. The match says what could be shared and why; how you mention it is yours to write.

## Output Format
```markdown
# Useful Material Match
Person: [name] | Reason you are leaning to: [reason] | Materials checked: [number] | Date: [date]
## Materials checked
| Material (yours) | What it helps a reader do | Fits because (fact number) | Brochure test |
|---|---|---|---|
| [title] | [one line] | [F# / P#, or "no fact supports it"] | [pass / fail] |
## Fits
- [none / title]: because [fact number and one line]
## Do not send
- [title]: [confidential / names a client / reads as a brochure / no fact supports it]
## Decision
[Your name] decides by [date] whether to share one item, share nothing, or note what material is missing from the list.
```

## Done When
- Every material on the list has a fit line or "no fact supports it".
- No more than two items are kept, each with its fact number.
- The do-not-send list exists.
- If nothing fits, the output says so and stops.

## Quality Bar
- Only materials you listed are considered; none is written, extended or summarised for the occasion.
- A fit is a fact about them, never "they are in my target group".
- Client material is shared only with the client's agreement.
- Zero is a valid answer and is never rounded up to one.
- Claude matches your own material to sourced facts; you decide what, if anything, to share.

## Next
Run reach-talking-points (Talking Points) to line up what you could say for the reason you chose.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
