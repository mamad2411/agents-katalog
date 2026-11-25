---
name: strat-issue-tree
description: Splits the agreed strategic question into an Issue Tree with the root word for word, sub-questions split by one stated logic per level, overlap and coverage checks, and for each leaf the data that answers it and where it lives. Use for "run strat-issue-tree", "build an issue tree", "break this strategic question down", "which part do we look at first", "split the question into parts", "are we missing a branch", "what data answers each part", "check the tree for overlap", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Issue Tree

## When To Use
The question is big and the team argues about which part to look at first. Each person has a favourite corner, and the same cause keeps turning up under two headings. This skill answers: what are all the parts of this question, with no part counted twice, and what data would answer each one?

## When Not To Use
If the question itself is still vague or carries an option inside it, run Strategic Question Frame first; a tree on a bad root only tidies the confusion. This tree holds questions only: to put a first answer on each branch, run Hypothesis Board. To test whether roadmap items serve a goal, run Impact Map.

## Inputs
- The Strategic Question Frame, or the question in one line, word for word.
- The Product Health Read, or what you know about the product's current state.
- The data you can reach (reports, exports, interview notes), and the time box for the diagnosis.
If you have none of this, I start from the question alone and mark the output as a first draft.

## Approach
An issue tree is long-standing practice: the question at the root, split into sub-questions that do not overlap and that together cover it. The judgment is in the split. Each level uses one logic, written at the node, so that two people reading the tree would put any given cause in the same branch. The failure it prevents: branches called "pricing", "new segment" and "mobile", where a mobile pricing problem sits in two places and the team counts it twice while a whole cause has no home. It runs in any Claude chat.

## Workflow
1. Ask at most three questions: is the root exactly the agreed question, how deep should the tree go (two or three levels), and what is the time box?
2. Copy the root word for word from the Strategic Question Frame. If the wording has changed, stop and send it back to the decision owner; a drifted root is a different question.
3. Choose one split logic per level and write it at the node: a formula (for example customers times revenue per customer), the customer journey in order, or segments. Never mix logics on one level.
4. Run the overlap check on every level: can one cause sit in two branches? If yes, merge them or redraw the split.
5. Run the coverage check: is there a cause no branch holds? Add the branch, or an "other" branch with a note on what it holds, so nothing hides in it.
6. Give each leaf the data that would answer it and where it lives. Where no source exists, write "missing"; that is a finding, and it tells you which customers to go and ask.
7. Mark the leaves that cannot be answered inside the time box, so nobody starts them by accident, and propose which leaves to work first for the owner to confirm.

## Output Format
```markdown
# Issue Tree
**Root question:** [word for word from the Strategic Question Frame]
Depth: [two / three levels] | Time box: [dates]
## Tree
| Level 1 (split by [logic]) | Level 2 (split by [logic]) | Data that answers it | Where it lives | In time box? |
|---|---|---|---|---|
| [1. sub-question] | [1.1 sub-question] | [metric, report, interview theme] | [tool, export, notes, or "missing"] | [yes / no] |
| | [1.2 sub-question] | [data] | [source or "missing"] | [yes / no] |
| [2. sub-question] | [2.1 sub-question] | [data] | [source or "missing"] | [yes / no] |
**Overlap check:** [none found / what was merged or redrawn]
**Coverage check:** [none missing / branch added / "other" holds ...]
## Outside the time box
| Leaf | Why it cannot be answered in time | What would be needed |
|---|---|---|
| [leaf] | [reason] | [data, access, customer calls] |
## Work first
- [leaf]: [what it would settle for the decision]
## Decision
[Decision owner role] confirms the tree and which leaves the team works first, by [date].
```

## Done When
- The root matches the agreed question word for word.
- Every level states one split logic, and both checks are recorded with their result.
- Every leaf names its data and where it lives, or is marked "missing".
- Leaves outside the time box are listed apart.

## Quality Bar
- Questions only: no answers, guesses or fixes in the tree.
- No cause can sit in two branches; if it can, the split is wrong.
- A leaf is small enough that one data pull or one set of customer calls answers it.
- Branches about teams describe processes, never individuals.
- A missing data source is marked missing, never filled with a guess; the owner confirms which leaves to work first.

## Next
Run strat-hypothesis-board (Hypothesis Board) to put a first answer that could be false on each branch.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
