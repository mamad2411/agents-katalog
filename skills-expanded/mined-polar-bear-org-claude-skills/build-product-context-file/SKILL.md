---
name: build-product-context-file
description: Writes one short file that tells Claude what your product is and how it speaks, with users by need, a glossary, what exists today, hard constraints, tone, a never list and a review date. Use for "run build-product-context-file", "write a CLAUDE.md for my product", "stop re-explaining my product to Claude", "product context for Claude", "project instructions for my prototype", "Claude keeps using the wrong words", "glossary for Claude", part of the Claude for Product Builders Pack by 90n.
---

# Product Context File

## When To Use
You re-explain your product at the start of every chat, and the screens still come back with the wrong words. Use this before the first build session. It answers one question: what does Claude need to know about this product every time, in the fewest lines?

## When Not To Use
Not for how the product looks: use Design System Brief. Not for the rules of the build folder (sample data only, no keys, never touch production): use Claude Code Setup. If you need the context once, for one chat, paste it and skip the file.

## Inputs
- Any existing description of the product (a spec, an onboarding page, help text), and the terms that keep coming out wrong
- Two real strings from the live product that sound right to you (a button label, an error message)
If you have none of this, I start from a five-minute spoken description and mark the output as a first draft.

## Approach
The method is the project memory file described in the Claude Code docs (How Claude remembers your project, https://code.claude.com/docs/en/memory). Their rule of thumb is that specific, concise instructions are followed more consistently, with a target of under 200 lines. The judgment is what to leave out. The failure this prevents is the familiar one: a file that grew to hold everything, so Claude follows none of it, and one that quietly picked up a customer's name on the way.

## Workflow
1. I ask up to three questions. What is the product and who uses it, described by what they need to get done? Which terms keep coming out wrong? Will you work in a Project or in Claude Code?
2. I write users by need and task, one line each. No named people and no profile of a real customer: a need is enough for Claude to choose the right words.
3. I build the glossary as three columns: the term, its meaning, and the word never to use in its place. The third column does most of the work, because the wrong word is usually a reasonable synonym.
4. I add what exists today (so Claude does not invent features), then hard constraints, then tone with your two sample strings. A tone adjective without a sample changes nothing. Then I cut to fit: under 200 lines, and every line must change what Claude would otherwise write.
5. I write the never list and scan the draft against it: customer personal data, keys, passwords, tokens, unreleased figures. Then I name where the file lives: `CLAUDE.md` at the top of the prototype folder (or `.claude/CLAUDE.md`) for Claude Code, or project instructions in a Project. In Claude Code, `/context` shows whether it loaded.
6. I set a review date and an owner role, and give you a check to run: read the first three screens against the glossary. The file is context, not enforcement, and Claude can still get a term wrong.

## Output Format
```markdown
# Product Context File
Where it lives: [CLAUDE.md in the prototype folder / project instructions] · Lines: [n] · Owner: [role] · Review date: [date]
The product in two sentences: [plain words]
## Users by need
| User, by need | What they are trying to get done | What they already know |
|---|---|---|
| [need, not a name] | [task] | [assumed knowledge] |
## Glossary
| Term | Meaning | Never say instead |
|---|---|---|
| [term] | [meaning] | [wrong word] |
## What exists today and hard constraints
- Live today: [feature or screen] · does not do: [limit]
- Hard constraint: [what Claude must respect on every screen]
## Tone
Sounds like: "[real string you supplied]" and "[real string you supplied]" · Never sounds like: [description]
## Never in this file
Customer personal data, keys, passwords, tokens, unreleased figures. Scan result: [clean / removed: item] · First-screens check run on: [date]
## Decision
[Product owner, by role] agrees the glossary and the never list by [date]; [owner role] reviews the file on [review date].
```

## Done When
- The file is under 200 lines and every line would change an output
- Every glossary row has a "never say instead" entry
- Both tone samples are real strings you supplied; the never-list scan is recorded; the file has an owner role and a review date

## Quality Bar
- Users appear by need and task, never as named people or as profiles of real customers.
- "What exists today" says what is live, not what is planned.
- Whether a detail counts as personal data: check with a qualified adviser. Whether something counts as a secret: check with your engineering or security lead.
- No customer personal data and no key ever goes into the context file.

## Next
Run build-design-system-brief (Design System Brief) to give Claude the product's look as well as its words.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
