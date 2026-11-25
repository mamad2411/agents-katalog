---
name: firm-proposal-red-team
description: Reads your proposal draft from the chair of the signer who was not on the call and returns an edit list by severity, covering the first-page read, every number, result, reference and quote traced or flagged "source or remove", their words against yours, lines any firm could have written and where you talk about yourself too early, never a rewrite. Use for "run firm-proposal-red-team", "read my proposal like the client would", "review the proposal before I send it", "red team this draft", "check for unsourced claims", "does this sound generic", "is this ready to go out", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Proposal Red Team Review

## When To Use
It is late, the proposal is finished, and you are the only person who has read it. You were on the call, so every sentence makes sense to you. The signer was not. Run this before anything goes out, to learn what a stranger with ten minutes understands, believes and doubts.

## When Not To Use
If the proposal is not written, use Consulting Proposal; a review of an outline only finds what is missing. For a fresh single page for the signer, use Proposal Executive Summary. This review never rewrites.

## Inputs
- The draft proposal, and the statement of work if it travels with it
- Your call record, playback or problem statement, so claims and client words can be traced
- Who will read it at the client, and which of them missed the call
If you have none of this beyond the draft, I flag every claim "source unknown" and mark the list as a first draft.

## Approach
Reviewing a proposal as its evaluator would, by someone who did not write it, is a long-standing convention among professional proposal teams, often run as colour-coded reviews; it is described generically here. An author cannot read their own draft cold, so I sit in the chair of the signer who missed the call. This is work AI does well: equal attention on every line, each claim checked against your files. What to change, and the voice, stay with you. The failure it prevents is a remembered result you cannot source, sent to a reader who has never met you.

## Workflow
1. Ask, in one go: who signs, and were they on the call? Is anything already agreed that must not change (a price, a scope line, a named reference)? When does it go out?
2. First-page read. I read page one only, as the absent signer, and write three lines: what they now think the problem is, what you propose, what they must decide. Each gap between that and what you meant becomes an item.
3. Claim check. I trace each number, result, reference, date and client quote back to your notes or files. What traces, stays. What does not is flagged "source or remove", never completed or softened.
4. Their words against yours. I mark where the problem is told in the client's language and where it slid into your jargon. A problem section with none of their words is a top-severity item.
5. Generic lines and self-talk. Any sentence that would fit any adviser or any client is flagged with the reason, and I point to the fact in your notes that would make it specific; I do not make one up. I also find where you first talk about yourself; if it comes before their problem, it heads the list.
6. The edit list, in three severities (would lose the decision, would cost credibility, would improve), closing with whether I would send it as it stands and which three items would change that.

## Output Format
```markdown
# Cold Read Edit List
Proposal: [title] · Read as: [signer's role] · Read on: [date]
## First-page read
- The problem, as the signer now sees it: [one line]
- What they believe you are proposing: [one line]
- What they think they must decide, and by when: [one line]
## Edits
| # | Severity | Where | Issue | Suggested fix |
|---|---|---|---|---|
| 1 | [would lose the decision / would cost credibility / would improve] | [page, section, sentence] | [unsourced / generic / your words, not theirs / you before them] | [source or remove / use their phrase from the notes / move below the problem] |
## Claims without a source
| Claim | Where | Status |
|---|---|---|
| [figure, result, reference or quote] | [location] | [source or remove] |
## Decision
[You] choose the edits and send the proposal yourself by [date]. Ready as it stands: [yes / no, fix items 1 to 3 first].
```

## Done When
- Every number, result, reference and quote is traced or listed as lacking a source
- The first-page read is written from the absent signer's chair
- Each edit has a place, an issue and a suggested fix, and nothing in the draft was rewritten

## Quality Bar
- An edit list, never a rewrite; the voice and the accountability stay yours
- A fix points to a fact in your notes; where there is none, the fix is a question for the client
- Comments concern sentences and claims, never the author or anyone at the client
- No rival is mentioned or run down in a suggested fix
- An unsourced number, result, reference or quote is flagged and never filled in; you decide the edits and you send it.

## Next
Run firm-proposal-walkthrough-deck (Proposal Walk-Through Deck) to present the proposal live so it is not left to be read cold.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
