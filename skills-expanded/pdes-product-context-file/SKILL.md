---
name: pdes-product-context-file
description: Write the one file Claude reads before any design task, covering who the product is for, the jobs it does, voice and terms, principles, constraints, what the product never does and where each fact came from. Use for "run pdes-product-context-file", "product context file", "Claude does not know my product", "every chat starts from zero", "context file for design work", "brief Claude on our product", "the draft looks generic", "what should Claude know before designing", part of the Claude for Product Designers Pack by 90n.
---

# Product Context File

## When To Use
Every chat starts from zero and the first draft looks like a product for nobody in particular. You then open each session by retyping who the users are and what the product would never do. This skill answers one question: what does Claude have to know about this product before it designs anything for it?

## When Not To Use
Not for tokens, components or layout rules: those live in the Design System Rules File, and this file links to it instead of repeating it. Not for writing principles from scratch either. If the product has none written down, run Design Principles first and quote the result here.

## Inputs
- Research you can point to (study summaries, session notes, support themes), with dates
- Voice guidelines or a few lines of copy that sound right, the product's principles if written, and its platform and technical constraints with who set each one
- Two or three references you admire, and what exactly you admire in each
If you have none of this, I start from your own description of the product and mark the output as a first draft with every user line shown as a gap.

## Approach
The method is context before generation, as in Anthropic's published account of one designer's workflow in Claude Design (claude.com blog, 24 July 2026): plan before prompting, specify the look, connect real context. That page describes one person's practice, and this file treats it as a practice worth borrowing, not a rule. The judgement is in what you leave out: a context file that tries to say everything gets skimmed by people and diluted for the model. The failure it prevents is the invented user. Ask for a dashboard with no context and you get one designed for a confident, patient, desktop-bound person who exists in no study you ran.

## Workflow
1. I ask up to three questions: which product area the file covers, who owns the file and keeps it current, and how long it may be (about two pages unless you say otherwise).
2. I fill the sections in a fixed order: users, jobs, voice and terms, principles, constraints, never-does list, references, sources. The order matters, because everything after "users" should be readable in their light.
3. Every line gets its source: the study and date, the document, or the person by role. A line with no source reads `[gap]`. I write no typical-user filler to make a section look complete.
4. Terms: a short glossary of the words the product uses and the words it avoids, each used one way. Principles are quoted as they stand, with a link; I do not reword or add to them.
5. References: for each one, what exactly is admired (structure, density, tone), so a later draft borrows the idea and not the surface. Then I cut to your length limit, put the owner and a "last checked" date at the top, add the one-line link to the rules file, and list the gaps as research questions.

## Output Format
```markdown
# Product Context File
Product area: [area] · Owner: [role] · Last checked: [date] · Design system rules: [link]
## Users
| User group | What we know | Source and date |
|---|---|---|
| [group] | [fact, or gap] | [study and date, or gap] |
## Jobs the product does
- [Job in the user's terms] · Source: [source or gap]
## Voice and terms
| Voice rule or term | We say | We avoid | Source |
|---|---|---|---|
| [rule or term] | [real line or word] | [line or word] | [guideline or gap] |
## Principles
- [Principle, quoted as written] · [link]
## Constraints
- [Constraint] · Kind: [platform, technical, legal, business] · Set by: [role]
## What the product never does
- [Line] · Reason: [reason or gap]
## References
- [Reference] · Admired for: [structure, density or tone] · Do not copy: [surface detail]
## Sources and gaps
- [Source, date, owner by role] · Gaps to research: [gap], who could answer: [role]
## Decision
[The file owner] confirms the file is accurate enough to use by [date]. [The product manager] decides which gaps become research questions for the next round.
```

## Done When
- Every line about users has a source and date, or reads `[gap]`
- The file fits the length you set, and the glossary shows words used and words avoided
- No token, component or spacing rule appears anywhere in the file

## Quality Bar
- User groups only. No named individuals and no personal data from research.
- A constraint names the role that set it, so someone can be asked whether it still holds. Legal or regulatory constraints are recorded as stated to you, with the note "check with a qualified adviser".
- The never-does list is specific to this product ("never confuses the user" is cut). Works in a plain chat: paste the file at the start. A Project or memory keeps it between chats so you do not have to.
- Facts about users come from real research or show as gaps; Claude never fills the file with a plausible user.

## Next
Run pdes-user-flow (User Flow) to put the file to work on its first design task.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
