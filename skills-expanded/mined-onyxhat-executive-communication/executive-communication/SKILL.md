---
name: executive-communication
description: Translate technical or operational detail into concise, decision-ready communication for senior leadership. Use this skill whenever the user is writing to executives, VPs, directors, a steering committee, or a board - including turning an SBAR, incident report, RCA, change request, or engineering status into a leadership summary; drafting a status update, escalation, risk or change notification; preparing a contract renewal, purchase justification, capital request, or vendor spend approval for a review board; preparing leadership talking points; or tightening writing that is too technical, too long, or buries the ask. Also use it when revising someone else's executive draft, comparing two versions of a document, or checking figures and tables in a business document for errors and inconsistencies. Also use it when the user says a draft "needs to be more executive," "too in the weeds," "make this shorter for leadership," or asks how to explain a technical decision in business terms.
---

# Executive Communication

Translate engineering and operational work into language that lets a senior leader make a decision in under a minute.

## The core problem this solves

Executives are time-constrained and decision-oriented. Technical contributors default to chronological narrative: here is what happened, here is what we tried, here is where we landed. That ordering makes a leader read to the end to find the point, and often the point never arrives because the writer described the *work* instead of the *implication*.

The fix is inversion. Lead with the conclusion and the ask. Supporting detail comes after, and only as much as the decision requires. Everything else in this skill is machinery in service of that one move.

## Workflow

### 1. Establish the frame before drafting

Answer these five questions. Pull the answers from the source material the user provided; ask only for what is genuinely missing.

- **Audience.** Who reads this, and what do they own? A CFO cares about cost and exposure. A CTO cares about stability and technical risk. A board cares about strategic and reputational consequence.
- **Decision.** What does the reader need to do after reading - approve, fund, be aware, escalate, or nothing? If the answer is "nothing," say so explicitly so they can stop reading.
- **Stakes.** What happens if they do nothing? This is the sentence most drafts are missing.
- **Format and length.** Email, Slack message, slide, meeting talking point, written brief. Length follows from the channel, not from how much material exists.
- **Required template.** Ask whether the receiving body already has a mandated form: a contract executive summary, capital request, or purchase justification. This is the highest-leverage question in the workflow. A well-argued document in the wrong container does not get judged on its merits. It gets poured into the correct container by whoever owns that container, and any reasoning without a slot in the form is lost in the transfer. Drafting into the right template means you decide what survives rather than the reviewer.

If a technical detail is unclear or a needed fact is absent, ask rather than guess. A confident-sounding summary built on an assumption is worse than a short delay. A good clarifying question sounds like: "Could you clarify the specific technical steps, or any constraints that might affect the execution timeline?"

### 2. Choose a framework

| Situation | Framework | Why |
|---|---|---|
| Written update, email, Slack, status report | **BLUF** | Reader gets the conclusion in sentence one and can stop there |
| Proposal, brief, deck, anything arguing for a decision | **Pyramid Principle** | Conclusion, then three or four supporting pillars, then detail on demand |
| Spoken answer, live meeting, unplanned question | **PREP** | Holds a coherent shape without notes |
| Incident, change, or risk originating from an engineering SBAR | **SBAR to leadership summary** | Preserves the situation-to-recommendation chain while stripping technical detail |
| Contract, purchase, budget, or exception needing sign-off | **Approval document structure** | Several reviewers hold separate vetoes, so completeness beats brevity |

Full definitions, structures, and worked examples are in `references/frameworks.md`. Read it when you need the mechanics of a framework you are not already applying confidently.

### 3. Translate technical facts into business consequence

This is where most drafts fail. Each technical fact needs a "so what" attached before it earns a place in the output.

- Metrics become insight. Not "efficiency improved 12 percent," but "we exceeded efficiency targets by 12 percent, shortening time-to-market for the new product line."
- Problems become assurance. Not a play-by-play of the outage, but what is true now and what prevents recurrence.
- Features become outcomes. Not "five new automation features," but "reduces manual labor costs by 20 percent starting next month."

`references/engineering-translation.md` has the full set of shifts, the "So What?" filter, and before/after pairs.

### 4. Draft against a template

`references/output-templates.md` contains ready structures for the recurring formats: leadership summary from an SBAR, status update, incident notification, change or risk notice, escalation, and meeting talking points. Read it and use the template that matches the frame from step 1 rather than inventing a shape.

The default leadership summary is five sentences and under 150 words:

1. **Context.** One sentence on the issue being addressed.
2. **Risk assessment.** One sentence on risk level, effort, and reversibility.
3. **Business impact.** One sentence on stability, cost, or strategic goals.
4. **Recommendation.** One sentence with next actions, including testing and deployment cadence.
5. **Closing (optional).** One sentence conveying confidence in the plan.

This target fits notifications, status updates, and recommendations. Approval documents are the exception. Several bodies read them at once, each with a standing question and the ability to stall on it, so the completeness bar is higher and the finished document is usually longer than the draft it replaces. See `references/approval-documents.md`.

### 5. Check the numbers

Any document containing a table or a financial claim gets this pass before the prose review, because a figure that does not reconcile costs more than a weak argument. One error licenses the reader to audit every other number instead of engaging with the reasoning.

```bash
python3 scripts/check_figures.py check draft.md          # totals and derived columns
python3 scripts/check_figures.py compare v1.md v2.md     # what moved between drafts
```

The script settles the arithmetic. `references/numeric-integrity.md` covers the checks that need judgment: whether percentages match their own base, whether the baseline is a fair one, and whether prose figures reconcile to the table. Run `compare` whenever a document has been through someone else's hands, since a figure that changed without being announced is the one that gets challenged.

### 6. Review before delivering

Run `references/review-checklist.md` against the draft. It catches the failures that are hard to see in your own writing: buried lede, missing ask, unattached technical detail, hedging, and length creep. This step is not optional padding - a draft that passes the checklist is materially different from one that does not.

When revising someone else's draft rather than writing your own, read `references/revision-patterns.md` instead. It covers what senior editors predictably cut and add, which lets you make those edits before the draft goes out rather than after it comes back.

## Voice and mechanics

These rules exist because executive readers scan rather than read, and because the output is usually sent under a human's name.

- **Plain business language.** Any term a competent non-specialist would need to look up either gets replaced or gets a four-word gloss on first use. Where the document routes beyond the working group, open with one sentence defining the subject. Leading with a definition rather than the conclusion is a deliberate exception to BLUF, and it earns its place when Legal, Finance, or Procurement are reading cold.
- **Short sentences.** One idea each. Long sentences hide the ask.
- **No em-dashes.** Use a period or a comma. This is a house style rule and it is followed exactly.
- **No rhetorical flourish.** State facts and conclusions directly. No "I'm excited to share," no "as you may know," no throat-clearing before the point.
- **Active voice with a named owner.** "We tested in staging," not "testing was performed." Passive voice reads as distance from accountability.
- **Quantify or drop it.** "Significant savings" is noise. "Roughly 40 hours a month" is a fact. If a number cannot be produced, say the magnitude is not yet known rather than reaching for an adjective. Calibrate precision to how settled each figure is: items still being negotiated with a counterparty get named without a number, because a figure in writing becomes an anchor before it is agreed, and net positions that depend on several things landing get stated as direction rather than as a promise.
- **Write in the sender's voice.** The output is the message itself, not a report about source material. Do not reference the ticket, SBAR, or document the content came from unless the reader needs it to act.
- **No new facts.** Everything in the output traces to the source material or to something the user confirmed. Uncertainty gets stated as uncertainty.

## Worked example

**Input:** An engineering SBAR describing retirement of a legacy F5 APM Kerberos policy that overlaps ClearPass NAC controls. Low risk, minutes to roll back, blocks DR testing, carries licensing cost.

**Output:**

> The current legacy F5 APM Kerberos policy overlapping ClearPass NAC controls is being retired.
> The change is low risk, requires minimal effort, and can be reversed within minutes.
> Simplifying the environment will improve stability, remove a DR blocker, and cut costs.
> We recommend testing in a lower environment today and, on success, scheduling the change in the next production hotfix.
> This approach keeps services secure while freeing resources for future initiatives.

Note what is absent: the policy's configuration, the sequence of investigation, the names of the engineers, and any mention of the SBAR itself. Note what is present: risk, effort, reversibility, impact, and a recommendation with a cadence. That ratio is the skill.

## Reference files

- `references/frameworks.md` - BLUF, Pyramid Principle, PREP, and SBAR-to-summary mechanics with examples
- `references/engineering-translation.md` - Turning technical facts into business consequence, plus the "So What?" filter
- `references/output-templates.md` - Copy-ready structures per communication type
- `references/approval-documents.md` - Contract, purchase, and budget approvals: required templates, the governance questions each function will ask, and how to calibrate precision on unsettled numbers
- `references/numeric-integrity.md` - Finding errors in tables and figures, and the checks the script cannot make
- `references/revision-patterns.md` - What senior editors predictably cut and add. Read when revising a technically-authored draft, or when generalizing feedback from a marked-up one
- `references/review-checklist.md` - Pre-delivery quality gate
- `references/knowledge-base-authoring.md` - How to structure source documents so agents retrieve from them reliably. Read this only when the task is authoring or restructuring reference material, not when drafting a message.

## Scripts

- `scripts/check_figures.py` - Verifies table totals and derived columns, and diffs figures between two drafts. Run it on anything containing a table before reviewing the prose.
