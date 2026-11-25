---
name: isd-style-guide
description: Drafts a learning content style guide from your own best content, with voice and reading level, terms and banned terms, feedback wording, rules for examples, and a before and after pair for each rule. Use for "run isd-style-guide", "write a style guide for our courses", "our courses sound like three different organisations", "the AI drafts do not sound like us", "how should feedback be worded", "tone of voice for e-learning", "banned terms list", "make Claude write in our voice", part of the Claude for Instructional Designers Pack by 90n.
---

# Learning Content Style Guide

## When To Use
Three courses sound like three different organisations, and the AI drafts sound like none of them. Use this when more than one person, or one person plus Claude, writes for the same learners, and you need to answer: how do our courses speak, written down so that anyone can follow it and anyone can check it?

## When Not To Use
Not for applying the rules to a course: E-Learning Storyboard Template and Training Video Script do that. Not for testing a built course against access needs: that is Accessibility Check. If you write one course alone and nobody else will touch it, a short list of terms is enough.

## Inputs
- Two or three pieces of your own content you consider good, and one you consider bad
- Your term list, any house writing rules that already apply, who your learners are by role, and the reading level you aim for if you have set one
If you have none of this, I start from one screen you like and one you do not, and mark the output as a first draft.

## Approach
The base is plain language, from the US General Services Administration's plain language guide series (principles, writing for understanding, design for understanding, test for understanding), with W3C WAI's "Writing for Web Accessibility": informative titles, headings that carry structure, meaningful link text and text alternatives, clear instructions, concise content. The judgment is yours: the rules come out of content you already think is good, never out of my taste. The failure this prevents is the guide nobody can check, a page of "be friendly, be clear" that every writer agrees with and every writer reads differently.

## Workflow
1. Ask at most three questions: which samples are the good ones and which is the bad one, who speaks to whom in your courses, and what reading level you set and how you check it. I propose no level.
2. Read the samples side by side and list what the good ones do that the bad one does not, with the exact lines. Each difference is a candidate rule; you strike any that is an accident of one writer. Sort the rest into sections: voice, reading level, terms and banned terms, instructions, feedback wording, examples and names, screen text against narration, alt text and link text, numbers and dates.
3. Write each rule as one testable line with a before and after pair taken from your own content. Where your samples have no "after", I draft one and mark it `[drafted, to approve]`. A rule nobody could check on a screen is cut.
4. Set the feedback and example rules with care, because they touch people: feedback says why, never "Correct!" alone, and never blames the learner; examples are fictional, marked as such, varied, and free of real names and stereotyped roles.
5. Phrase every rule for two readers, a colleague and Claude: positive and specific ("address the learner as you"), then a short "do not" list. The guide can be loaded into a Project so drafts follow it, or kept in Claude Docs (beta) for colleagues to comment on.
6. Add the test for understanding and the upkeep: you try a sample screen written to the guide with a real reader from the audience, and never rely on a readability score alone. Name the guide's owner and review date.

## Output Format
```markdown
# Learning Content Style Guide
Version: [version] | Owner: [role] | Review date: [date] | Built from: [samples used]
## Voice and reading level
- Who speaks to whom: [rule], set by [role]
- Reading level: [target you set], checked by [how]
## Rules, with before and after
| # | Section | Rule (one line, testable) | Before | After | Source of the pair |
|---|---|---|---|---|---|
| [1] | [voice, instructions, feedback, examples, screen text, narration, alt text, link text, numbers and dates] | [rule] | [line from your content] | [rewritten line] | [sample, or drafted, to approve] |
## Terms
| Use | Do not use | Why |
|---|---|---|
| [term] | [banned term] | [reason] |
## Do not, and paste block for Claude
- Do not: [short list, one line each]
- Paste block: [the rules above as a numbered list, ready to load with the course sources]
## Test for understanding
| Sample screen | Reader (role) | What they did or misread | Rule to change |
|---|---|---|---|
| [screen] | [role] | [observation] | [rule number] |
## Decision
[Guide owner, by name] approves the rules by [date]. [Designer, by name] runs the reader test by [date] and decides which rules change.
```

## Done When
- Every rule has a before and after pair, and each drafted "after" is approved or removed
- No rule needs the word "appropriate" to work
- The feedback and example rules are present, and the paste block says the same thing as the table
- The guide has an owner and a review date

## Quality Bar
- Rules come from your content; where I add one from the plain language or accessibility guidance, it is marked as added
- One rule, one line, one pair, and examples never use a real person's name or a stereotyped role
- A readability score is a prompt to look, never proof a learner understood
- Claude drafts the rules from your own best content; you decide how your courses speak to learners.

## Next
Run isd-portfolio-case-study (Portfolio Case Study) to write up the work behind a finished course.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
