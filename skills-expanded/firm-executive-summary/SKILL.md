---
name: firm-executive-summary
description: Writes a one-page proposal executive summary for the signer who was not on the call, with the decision asked and the date first, their situation, the complication, the question, the recommended option with its reasons and every option in one line with what it leaves out. Use for "run firm-executive-summary", "write the executive summary", "one page for the person who signs", "summarise my proposal for their CEO", "the decision maker never met me", "exec summary of this proposal", "short version for the budget holder", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Proposal Executive Summary

## When To Use
Your contact is convinced. The signature belongs to someone two levels up who was in none of the conversations and will read one page between two meetings. Run this once the proposal is final, to write that page so it can be understood with no memory of the calls.

## When Not To Use
If your contact needs a neutral page that also covers doing nothing or doing it in house, use Client Decision Brief; this page recommends your option. To state your advice on their decision with no fees attached, use Recommendation Memo. With no proposal yet, write the Consulting Proposal first; this page draws only on it.

## Inputs
- The final proposal with its options and your prices
- The signer's role, and what that role cares about
- The date by which you are asking for a decision
If you have none of this beyond the proposal, I start from it alone and mark the page as a first draft. Claude Docs suits a page you will refine with your contact; any chat works.

## Approach
Situation, complication, question is Barbara Minto's opening structure (barbaraminto.com): begin with what the reader already accepts, say what has changed, name the question in front of them, answer it. Compressing a long document into this shape while staying faithful to it is something AI does quickly. Choosing what to recommend, and standing behind it, is yours. The failure it prevents is a summary of your practice, written for someone who was on the call, ending "as discussed".

## Workflow
1. Ask, in one go: who signs, and what does that role care about? Which option do you recommend, and why? By what date do you need the decision?
2. Decision first. The opening two lines state what is asked and by when, so a reader who stops there still knows what you need.
3. Situation: what the signer already holds to be true, in the client's words from the proposal. If they would dispute it, it is not yet the situation.
4. Complication: what changed or what is at stake, with figures only from the proposal. A missing figure stays [bracketed].
5. The question the signer has to answer, then your recommended option and the two or three reasons behind it, each traceable to a section of the proposal. Then every option in one line with what it leaves out, so the recommendation reads as a choice and not a push.
6. Cold-read pass. I remove each "as discussed", each unexplained abbreviation and each reference to a call, and confirm that nothing appears here that is not already in the proposal and that it fits one page.

## Output Format
```markdown
# One-Page Summary for the Signer
Written for: [signer's role] · By: [your name] · Date: [date]
**Decision asked of you:** [choose among the options / approve option] by [date].
## Situation
[Two or three sentences, in their words, that the reader would not dispute.]
## Complication
[What has changed, or what is at risk, in their figures or with a placeholder.]
## The question
[One sentence the signer must answer.]
## Recommended option
[Option] because [reason 1], [reason 2], [reason 3]. (Proposal sections: [refs])
## Every option
| Option | What it delivers | What it leaves out | Price |
|---|---|---|---|
| [option] | [one line] | [one line] | [as you set it] |
## Decision
[Signer's role] approves an option, or declines, by [date]; [you] send this page with the proposal yourself.
```

## Done When
- The decision asked and its date are in the first lines
- It can be read with no knowledge of the calls and fits one page
- Every figure and reason traces to the proposal

## Quality Bar
- Situation, complication, question, answer, in that order and in the client's words
- You appear in the recommendation, never in the opening
- Each option is summarised fairly, including what it leaves out
- Nothing new; a claim absent from the proposal is absent here
- The page draws on the proposal alone; I add no fact, figure or quote, and the signer decides.

## Next
Run firm-ai-objection-answer (AI Objection Answer) to prepare for the objection most likely to come back from that reader.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
