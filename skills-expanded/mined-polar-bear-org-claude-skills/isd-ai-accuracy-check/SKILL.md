---
name: isd-ai-accuracy-check
description: Traces every factual claim in a draft course to a source you approved, producing a claim trace with the supporting quote and its place, a flag list the expert decides line by line, and a real or fictional marking of every example and case. Use for "run isd-ai-accuracy-check", "where did these numbers come from", "check this AI-drafted storyboard against the sources", "flag what you cannot trace", "is this draft accurate", "the expert sent pages an AI wrote", "trace every claim to a source", "do not correct anything, just flag", part of the Claude for Instructional Designers Pack by 90n.
---

# AI Content Accuracy Check

## When To Use
The draft reads beautifully and nobody can say where its numbers came from. Use this once a storyboard, script, question set or job aid exists and before any reviewer sees it. It answers one question: is every fact in this draft traceable to a source we approved?

## When Not To Use
This check says nothing about whether the course teaches: an accurate draft with no practice passes it untouched, and Does It Teach Review owns that question. If you have no approved source list yet, run Source Content Triage first. The expert's wider comments on the draft belong to SME Review Round.

## Inputs
- The draft, with its version: storyboard, script, questions, job aid or the built course's text.
- The approved sources, each with its date and version. In a Project that holds your approved sources (the redesign is in beta on select plans) they are already loaded; otherwise attach them to the conversation.
- The name and role of the expert who decides the flags.
If you have none of this, I start from the draft alone, mark every claim untraced, and mark the output as a first draft.

## Approach
This is a claim-by-claim trace built on the quote-first technique in Anthropic's documentation "Reduce hallucinations": pull the word-for-word quote first, tie each claim to it, withdraw the claim if no quote exists, stay inside the supplied documents, and allow "not in the sources". Anthropic says this reduces invented claims and does not remove them, which is why the expert still reads. A college's public human-in-the-loop review guide puts accuracy first among the things a person must review in AI-made learning material. The failure it prevents: a procedure that gained a step in the draft, the extra one written in the same calm voice as the real ones, and a case study that reads like an incident report and never happened.

## Workflow
1. Ask up to three questions: which sources are approved (name, version, date), which draft version this is, and which expert decides the flags and by when. Anything outside that list, including what Claude knows in general, does not count as a source.
2. Extract every factual claim and number it: figures, limits, rules, steps and their order, names, dates, definitions, and every "always" or "never". Opinions and instructions to the learner are left out; when in doubt, list it.
3. Trace quote first. For each claim, find the supporting passage in an approved source, copy it word for word, and give its place. Show the quote, not the word "traced". A paraphrase that needs goodwill to match is not a match.
4. Give each claim one of four statuses: traced, untraced (no quote found), conflicts with source (the draft says one thing, the source another), or sources contradict (two approved sources disagree). Show both sides. Never reword the draft to fit and never pick a side.
5. Mark every example, case, name and figure as real (with its source) or fictional. A fictional case written as if it happened is a flag, however plausible it reads.
6. Hand the expert the flags only, as a short list. For each the expert chooses: confirm with a source, correct (in their words), or remove. You apply the decision and rerun the trace on every changed passage; Claude does not write the correction. Then list the high-stakes passages (safety, money, legal, anything costly to get wrong) for the expert to read in full, because a clean trace is not proof.

## Output Format
```markdown
# AI Content Accuracy Check
Draft: [name, version] | Trace run by: [role], [date] | Flags decided by: [expert name, role] | Approved sources, and nothing else counts: [source, version, date]
## Claim trace
| No. | Claim as written | Place in draft | Supporting quote, word for word | Source and place | Status |
|---|---|---|---|---|---|
| [C1] | [claim] | [screen or line] | [quote, or "no quote found"] | [source, section] | [traced / untraced / conflicts with source / sources contradict] |
## Conflicts, side by side
| Claim | The draft says | [Source A, place, date] says | [Source B, place, date] says |
|---|---|---|---|
| [C4] | [wording] | [quote] | [quote or n/a] |
## Examples, cases, names and figures
| Item | Place | Real or fictional | Source if real | Flag |
|---|---|---|---|---|
| [case or name] | [screen] | [real / fictional / unknown] | [source] | [none, or "fictional, written as real"] |
## Flags for the expert
High-stakes passages read in full by the expert: [passage, why it is high stakes, date read]
| Flag | Why it is flagged | Expert's decision (confirm with a source / correct / remove) | Expert's wording or source | Decided on |
|---|---|---|---|---|
| [C2] | [untraced] | [decision] | [text from the expert] | [date] |
## Decision
Trace run by [designer, role] on [date], version [x]. [Expert name, role] decides every open flag by [date]; the designer applies the decisions and reruns the trace on changed passages by [date].
```

## Done When
- Every claim has a number, a place and one of the four statuses.
- Every traced claim shows its quote and where the quote sits.
- Every example, case, name and figure is marked real or fictional, and every flag has the expert's decision or is listed as open with a date.

## Quality Bar
- A conflict shows both versions with their places; the trace never says which is right, and no claim is traced to "general knowledge", to the draft itself or to an undated page.
- Gaps are written `[to confirm with the expert]`, never filled with plausible detail.
- The check never states that the course is accurate; it states what was traced, on which version, and what the expert decided, recorded by role and date and nothing else about them.
- Claude flags and never fixes: the expert decides every flag, and nothing invented is passed off as real.

## Next
Run isd-does-it-teach-review (Does It Teach Review) to see whether the accurate draft gives anyone something to practise.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
