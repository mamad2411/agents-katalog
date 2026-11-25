---
name: pmjob-target-role-brief
description: Builds your Target Role Brief with two or three target roles and their level, your own weighted criteria and deal-breakers written before any offer exists, and the words real job ads use matched to your evidence rows. Use for "run pmjob-target-role-brief", "what do I want next", "I am applying to everything", "which product roles should I aim at", "read these job ads for keywords", "set my criteria for the next role", "senior or lead or principal", "match my experience to these ads", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Target Role Brief

## When To Use
You are applying to everything and cannot say in one line what you want next. Run this before the next application to answer three things: which two or three roles, at what level, am I aiming at; what must the next role give me; and which of the words those ads use can I already show from shipped work?

## When Not To Use
For one ad you are about to apply to, use Job Ad Breakdown, which reads a single ad line by line; this brief reads several ads for vocabulary and holds no must-have list and no rounds. With no evidence rows yet, run Career Evidence Inventory first, or every word ends up "not yet".

## Inputs
- Two or three target roles in your words, each with the level you would apply at
- Five real job ads per role, pasted as text (not links)
- Your Career Evidence Inventory, or a rough list of roles, products and launches
If you have none of this, I start from one role and the ads you can find, and mark the output as a first draft.

## Approach
Job ad keyword reading with evidence matching. The Prospects guide, How to improve your LinkedIn profile, says to start by reviewing the skills listed in postings for the roles you want; this brief adds a check against your evidence and a list of your own criteria. The judgment is in the matching, not the extracting: a word earns a place only when a row shows it. The criteria are written now for a reason. A list drafted with an offer already on the table tends to describe that offer.

## Workflow
1. Ask up to three questions: the roles in your order and the level for each; what the next role must give you and what would make you say no; the date by which you want a focused list.
2. Write each role with its level in the employer's words (senior, lead, principal, head of) and what that level would mean in scope: the size of the problem, the team, who you report to. The order is yours. I never say which role suits you.
3. Set your own criteria: five to eight in your words (the work, scope, the manager, pay, location and flexibility, the product, growth), each with a weight you set, and a separate deal-breaker list. Date it. Offer Comparison reads this list later, so it is fixed before any offer arrives.
4. Check the ads: five per role is the aim, fewer than three marks the brief "thin", and reposts of one advert count once.
5. Extract repeated words per role, sorted into skills, tasks, tools and qualities, each with "in x of 5 ads". The counts describe these ads and nothing more.
6. Match each word to your inventory: shown (row ID), partly (row ID plus what is missing), not yet. Only "shown" words go on your resume and profile; "partly" needs wording that stays true ("contributed to the pricing decision", not "owned pricing").
7. For each "not yet" word, name one real step inside your current work, or write "leave for now". You choose; I do not invent a step.

## Output Format
```markdown
# Target Role Brief
Updated: [date] · Ads read: [n per role] · Status: [full / thin]
## Roles, in your order
| Role | Level, in the employer's words | What that level means in scope |
|---|---|---|
| [role] | [senior / lead / principal / head of] | [problem size, team, reports to] |
## Own criteria (written [date], before any offer)
| Criterion, in your words | Weight you set | What "met" looks like |
|---|---|---|
| [criterion] | [weight] | [what you would need to see] |
Deal-breakers: [item], [item]
## Employer words, role 1: [role]
| Word or phrase | Type | In how many ads | Match | Evidence row | If not yet: one real step in current work, or "leave for now" |
|---|---|---|---|---|---|
| [word] | [skill / task / tool / quality] | [x of 5] | [shown / partly / not yet] | [E3, or what is missing] | [step, by when] |
## Words you may use now
- [shown words only, with row IDs]
## Decision
You decide the role order, the weights and the deal-breakers, and confirm the "shown" word list, by [date].
```

## Done When
- Every role has a level, a scope line, an ad count and a full or thin status
- Five to eight criteria carry your weights, the deal-breakers sit apart, and the list is dated
- Every extracted word has a match status, and every "shown" word cites a row ID
- Every "not yet" word has one real step or "leave for now"

## Quality Bar
- Counts are copied from the ads you pasted, never estimated or presented as a market view.
- Pay appears as a criterion in your words; any figure comes from you or from an employer's stated range, with source and date.
- I never infer which role fits you from personality, age or background.
- Ads are read as text you paste; I do not browse job sites for you. A Project can keep the brief where later skills read it.
- Ad words go on your resume or profile only where an evidence row shows them; no role, result or number is invented to fill a gap.

## Next
Run pmjob-job-ad-breakdown (Job Ad Breakdown) to read one real ad against the brief.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).