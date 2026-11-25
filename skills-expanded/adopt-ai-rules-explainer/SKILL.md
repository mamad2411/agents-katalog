---
name: adopt-ai-rules-explainer
description: Rewrites your organisation's own AI rules as a can, cannot and ask first table with real task examples, a who-to-ask list for grey areas and a list of what is still undecided. Use for "run adopt-ai-rules-explainer", "explain our AI policy", "AI policy in plain language", "can I paste a customer email into AI", "what are we allowed to put into AI", "AI rules one pager", "simplify the AI use policy", "AI dos and don'ts for staff", part of the Claude Guide for AI Adoption Pack by 90n.
---

# AI Rules Explainer

## When To Use
The policy exists, is eleven pages long, and people still do not know whether they can paste a customer email. Use this when the rules are written down and nobody can act on them in the middle of a task. It answers one question for the reader: what can I do, what can I not do, and who do I ask when I am not sure?

## When Not To Use
Do not use it when there is no policy, or to fill a hole in one: this skill explains rules that exist and writes none. For one team's own practice inside the rules, run Team AI Agreement. For the single rule that belongs to a single task, run AI Job Aid.

## Inputs
- The organisation's AI policy or rules, pasted or uploaded, with section or page numbers where it has them.
- The roles who will read the explainer, two or three real tasks for each, and the questions they keep asking, in their words and without names.
- Who owns the policy, and who answers data, security and legal questions.
If you have none of this, I start from the policy text alone and mark the output as a first draft.

## Approach
The method is the set of plain language principles in the US General Services Administration's plain language guides: write for your audience, start with the point, use the active voice, organise and summarise up front, use tables and lists, test with readers. The judgment sits in what the explainer refuses to do. Plain wording cannot repair an unclear rule, so where the policy is silent the entry reads "undecided" and names who to ask. The failure this prevents is the friendly summary that quietly invents a permission, which someone then follows with real customer data. Some organisations place this work under the EU AI Act, Article 4, on AI literacy: treat that as context only, and check with a qualified adviser.

## Workflow
1. Ask up to three questions: which roles will read this, which real tasks they keep asking about, and who owns the policy and will approve the explainer.
2. Read the policy clause by clause and list every rule with its section or page. Flag what cannot be read as a rule: a principle with no instruction, two clauses that disagree, a term nobody defined. I list these for the owner and resolve none of them.
3. Sort each rule into can, cannot or ask first. "Ask first" is for rules that depend on a condition. It is not a place to park rules that were hard to read.
4. Give each rule one example from a real task of the reader's roles, marked as an example. If the policy does not settle the example, it moves to the grey areas, each with the role to ask and how to reach them. Where the policy says nothing, write "undecided, ask [role]". No rule is invented to fill a gap.
5. Run the plain language pass: the reader's own words, the answer first, the active voice, one rule per line. Mark every legal or data point "check with a qualified adviser".
6. Prepare the reader test: two or three readers each decide a real case using only the explainer. A person runs it. Where readers hesitate or decide differently, the line is rewritten or goes back to the policy owner, who approves the final text. Share it in Claude Docs (beta) or any shared document.

## Output Format
```markdown
# AI Rules Explainer
Source policy: [title, version, date] | Policy owner: [role] | Status: [draft, or approved on date]
If this explainer and the policy differ, the policy wins. Tell [role] so the explainer is corrected.
## The short version
[Three or four lines, the answer first, in the reader's words.]
## Can, cannot, ask first
| Rule in plain words | Can, cannot or ask first | Example from a real task (example) | Policy clause |
|---|---|---|---|
| [rule] | [one of the three] | [task example] | [section or page] |

## Grey areas and who to ask
| Situation | Who to ask | How to reach them | Legal or data point |
|---|---|---|---|
| [situation] | [role] | [channel] | [no, or yes: check with a qualified adviser] |

## Still undecided
| Question the policy does not answer | Who will decide | What to do until then |
|---|---|---|
| [question] | [role] | [ask [role] before going ahead] |

## Reader test
[For each real case given to two or three readers: what they decided with the explainer alone, and the line changed as a result, or none.]
## Decision
[Policy owner, by role] approves, corrects or returns this explainer by [date]. [Role] publishes it at [place] and confirms the line that asking a question is never held against anyone.
```

## Done When
- Every line in the table traces to a section or page of the source policy and has one example from a real task of a named role.
- Every grey area has a role to ask, and every gap reads "undecided", not a guess.
- The reader test is planned with real cases, and its result has a place in the document.

## Quality Bar
- One rule per line, in the active voice, with the answer before the reason.
- The explainer says where to ask, and that asking is never held against anyone.
- No rule is added, softened or tightened. If the wording changes the meaning, the policy wording stays.
- It explains rules the organisation already has; the policy owner approves it, and every legal or data point goes to a qualified adviser.

## Next
Run adopt-ai-jobs-answer (AI and Jobs Answer) to prepare the other question that is in every room.

## About the makers
This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
