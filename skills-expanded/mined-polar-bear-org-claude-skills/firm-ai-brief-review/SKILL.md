---
name: firm-ai-brief-review
description: Sorts every line of a client's brief into a decision the client made, generic text, an assumption or a contradiction, runs six missing-constraint checks and lists the questions only the client can answer, in priority order. Use for "run firm-ai-brief-review", "read this client brief", "the brief was written with AI", "I cannot scope from this document", "what is this RFP not telling me", "which lines did they actually decide", "what do I ask before I quote", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# AI-Written Brief Review

## When To Use
A brief lands in your inbox with every heading filled in: goals, phases, success factors, a timeline. It was probably drafted with AI, and after two readings you still could not say what the client would fund first. Run this before you reply or quote. It answers one question: which of these lines did somebody at the client actually decide?

## When Not To Use
After the call, when the job is trimming a long wish list to what the fee covers, use MoSCoW Scope. If you are not yet sure you should answer at all, Bid/No-Bid Decision comes first.

## Inputs
- The brief exactly as received (pasted, PDF or document) and the covering message
- Anything you heard outside the document, with where you heard it
- Your practice brief, if you keep one (the work you want and the work you decline)
If you have none of this beyond the document, I start from the brief alone and mark the output as a first draft.

## Approach
This is claim, assumption and gap reading, a habit from requirements-quality work, described generically with no standard named. A generated brief fails in one particular way: it fills every section with sentences that sound decided and are not, and each one becomes your risk the day you price from it. The review never asks who or what wrote the document. Drafting a brief with AI is a sensible thing for a client to do; the only question is what can be scoped from it.

## Workflow
1. Ask, in one go: has anyone at the client spoken to you yet, and in what role? Did you hear a budget range or a date outside the document? Which part of this work do you most want?
2. Number every sentence and bullet, then give each exactly one label. Decision: specific to this client and owned by them (a date, a system, a named constraint, a figure). Generic: would sit unchanged in any client's brief. Assumption: asserted as fact with no basis shown. Contradiction: cannot hold together with another line, both numbers quoted.
3. Be mean with the decision label. "Strengthen cross-team collaboration" is generic even when true; "the board reviews this on [their stated date]" is a decision. In doubt, label it generic: a generic line costs one question, a false decision costs the engagement.
4. Run the six constraint checks whatever the brief claims to cover. Budget or range, the decision owner, the deadline and the reason for it, what was tried before, success in their own measures, what is out of scope. Each is found (with the line number) or missing.
5. Write one question per generic block and per missing constraint, as a forced choice where possible: "if only one of these four goals were funded this year, which?" gets further than "tell me about your priorities".
6. Order the questions: first those that change scope or price, then those that change whom you need to meet. Star the three worth asking even on a short call. Then read the list as the client would and cut anything that sounds like marking their homework.

## Output Format
```markdown
# Brief Reading Sheet
Brief: [title or date received] · Read on: [date] · Contact so far: [none / role, date]
## Line by line
| # | Line (shortened) | Label | Why |
|---|---|---|---|
| [n] | [text] | [decision / generic / assumption / contradiction] | [what makes it so] |
## Six constraint checks
| Constraint | Found or missing | Line | Question if missing |
|---|---|---|---|
| Budget or range | [found / missing] | [n] | [question] |
| Decision owner · Deadline and why · Tried before · Success measures · Out of scope | [found / missing] | [n] | [question] |
## Questions for the client alone
1. [Question] · changes [scope / price / who to meet] · ask on a short call [yes / no]
## Decision
[You] choose which questions go into the call or a reply by [date]. Nothing is quoted until [the constraints you named] are answered by the client.
```

## Done When
- Every line carries one label and its number
- All six constraints read found or missing
- Each generic block and missing constraint has a question, and no line comments on how the brief was written

## Quality Bar
- The decision label needs something the client owns; a sensible-sounding goal does not qualify
- A contradiction quotes both line numbers, never a summary of them
- No gap is filled with a likely answer, a typical budget or a guess at intent
- The client is never judged for using AI, in the sheet or in the questions
- Gaps become questions for the client, never numbers or facts I supply; you decide what to ask and you send the reply.

## Next
Run firm-meddic-qualification (MEDDIC Qualification) to check whether the opportunity behind the brief fits the work you want.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
