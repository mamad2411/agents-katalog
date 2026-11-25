---
name: pmjob-company-research
description: Writes a Company Research Brief with what the product does and for whom from the company's own pages, your notes from using it, dated news with sources, how it makes money as far as public pages say, product and design team signals and three questions a website cannot answer. Use for "run pmjob-company-research", "research this company before my interview", "what does this company actually do", "how do they make money", "recent news about this employer", "what should I know before the hiring manager call", "help me structure my notes on their product", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Company Research Brief

## When To Use
The interview is in three days and you could only describe the logo. Run this to answer: what does the product do and for whom, what has changed lately, how does the company earn money as far as it says in public, and what is worth asking a person because no page answers it?

## When Not To Use
For the people you will meet, use Interviewer Research Notes; this brief covers the organisation and its product. For one line each across many companies, use Target Company List; this goes deep on one.

## Inputs
- The company name, the role, and the ad or your Job Ad Breakdown
- Pages you have open or pasted: product site, pricing page, changelog, engineering or design blog, annual report or filings
- Your own notes from using the product, however rough
If you have none of this, I start from the company name and its own website and mark the output as a first draft.

## Approach
Dated, sourced employer research, joined to a product walkthrough that you do yourself. One public employer interview guide tells candidates to use the product as a customer before the interview, and an experienced interviewer can hear within a minute whether you did. Every claim carries a source and the date it was read, because a confident line about last year's pricing, said to the person who changed it, undoes the conversation. With web search in chat turned on, I can find and open public pages; without it, I work from what you paste.

## Workflow
1. Ask up to three questions: which role and which round is this for; how many news items you want and how old is too old; whether you have used the product yet.
2. Write what they do and for whom in two lines, from their own site, with the page named and the date read.
3. Set up your walkthrough: sign up or take the free path, do one core task, and note three things: what was easy, where you hesitated, what you would ask the team. I structure what you write and add nothing from imagination. If the product cannot be tried, the brief says so and uses public demos or documentation.
4. List the news, as many items as you set, each with date and source. Anything older than your cut-off is marked "old". Dates are checked on the page, not taken from search snippets.
5. Record how they make money only from public pages: pricing page, annual report, filings. Otherwise "not published". No guessed revenue, headcount or funding.
6. Collect product and design team signals from public material only: engineering or design blog, job ads, public talks, changelog. Each with its source and date.
7. Write three questions a website cannot answer, each built from one sourced fact above, the kind a peer who has shipped products would ask.

## Output Format
```markdown
# Company Research Brief
Company: [name] · Role: [role] · Read on: [date] · Status: [full / first draft]
## What they do, and for whom
[Two lines] (source: [their page], read [date])
## My notes from using the product (tried [date], path: [free plan / trial / public demo / could not be tried], core task: [task])
| What was easy | Where I hesitated | What I would ask the team |
|---|---|---|
| [your note] | [your note] | [your note] |
## News
| Date | Item | Source | Old? |
|---|---|---|---|
| [date] | [one line] | [publisher, page] | [yes / no] |
## How they make money, and team signals (public pages only)
| Kind | What is stated | Source | Date |
|---|---|---|---|
| [money] | [pricing model, segment, or "not published"] | [pricing page, annual report or filing] | [date] |
| [product team / design team] | [what the blog, changelog, talk or job ad shows] | [source] | [date] |
## Three questions a website cannot answer
1. [Question] (from: [sourced fact])
2. [Question] (from: [sourced fact])
3. [Question] (from: [sourced fact])
## Decision
You decide which two findings and which question you will bring into the round, by [date].
```

## Done When
- Every claim has a named source and a date; old news is marked "old" and anything not found says "not published"
- The walkthrough notes are in your words, or the brief says the product could not be tried
- None of the three questions can be answered from their site

## Quality Bar
- Their own pages first; third-party summaries only where named and dated.
- Staff appear only if named in the company's own public material, with their public role only.
- An opinion about their product is marked as your view and tied to a walkthrough note.
- Every claim about the company has a dated source; the notes on using the product are yours, not generated.

## Next
Run pmjob-interviewer-research (Interviewer Research Notes) to prepare for the people on the loop.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).