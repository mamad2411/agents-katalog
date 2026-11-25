---
name: firm-statement-of-work
description: Writes a results-based statement of work, with objectives as results, deliverables each with an acceptance criterion and an accepting role, a dated timeline, client responsibilities, assumptions and the won't list word for word, and change control for any new request including ones the client's AI suggests, with contract terms left as placeholders. Use for "run firm-statement-of-work", "write the statement of work", "SOW for this engagement", "acceptance criteria for my deliverables", "stop scope creep before it starts", "change control wording", "scope document the client can sign", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Statement of Work

## When To Use
The client has said yes. In three weeks someone on their side will paste the scope into a model, ask "what else should a good consultant cover?" and forward you the list. Run this now, so both of you have one document that says what is delivered, how anyone will know it is finished, who does what by when, and how a new idea gets handled.

## When Not To Use
If the client has not picked an option, stay with the Consulting Proposal. If the scope is still disputed, settle it in MoSCoW Scope; this document records a scope, it does not decide one.

## Inputs
- The accepted option, your phases, and the scope with its won't list
- The dates you can commit to, and what the client must supply (access, people, decisions, data)
- Your AI use statement, and any contract template either side already uses
If you have none of this, I start from the accepted option, leave each date and standard as a [placeholder] and mark it as a first draft.

## Approach
The rule for the writing is taken from FAR 37.602 (acquisition.gov/far/37.602), which asks that work be set out as required results and measurable standards, not as hours or method. It is a public procurement rule borrowed here purely as a way of writing, with the usual practitioner sections around it. The failure it prevents is a deliverable such as "support the change programme", which can never be finished and can always be widened.

## Workflow
1. Ask, in one go: which option was accepted? Which dates are fixed on either side? Who at the client accepts deliverables?
2. Objectives as results: what will be true when the work ends, in the client's measures. An activity is not an objective; "hold three workshops" becomes whatever the workshops are for.
3. Deliverables, each with an acceptance criterion the client can check: form, content, rounds of review, the accepting role and the number of days they have. You set each standard; a deliverable with none is flagged.
4. Timeline with your dates, and client responsibilities with theirs. The document says plainly that a late input from the client moves the dates that depend on it.
5. Assumptions, then exclusions: the won't list is copied word for word from your scope, so nothing dropped earlier creeps back. Refer to your AI use statement for how AI is used.
6. Change control: any new request is written down, sized, priced and approved in writing before work starts. That includes requests the client's own AI tools suggest, treated like any other, no better and no worse. Liability, IP, confidentiality and payment stay as [placeholders] marked "check with a qualified adviser". Draft in Claude Docs or as an exported document; you send it.

## Output Format
```markdown
# Statement of Work
Client: [organisation] · Consultant: [you] · Version: [n], [date]
## Objectives (results)
- [What will be true at the end, in the client's measure]
## Deliverables and acceptance
| Deliverable | Acceptance criterion | Review rounds | Accepted by (role) | Within |
|---|---|---|---|---|
| [deliverable] | [standard you set] | [n] | [role] | [days] |
## Timeline and responsibilities
| Date | Consultant delivers | Client provides | Owner (role) |
|---|---|---|---|
| [date] | [item] | [access / data / decision] | [role] |
## Assumptions and exclusions
- Assumption: [ ]
- Not included (won't list, word for word): [ ]
## Change control
[How a request is raised, sized, priced and approved in writing before any work on it starts]
## Terms
[Liability, IP, confidentiality and payment stay as placeholders; check with a qualified adviser]
## Decision
[Client signer role] and [you] approve version [n] by [date]; a qualified adviser reviews the terms before anyone signs.
```

## Done When
- Every deliverable has an acceptance criterion and an accepting role
- The won't list appears word for word and the change route is written out
- Every date was supplied by you or the client, or is a [placeholder]

## Quality Bar
- Written as results and standards, never hours; every deliverable can be finished
- The client's responsibilities are as specific and as dated as yours
- No legal wording is offered as advice; terms stay placeholders for an adviser
- Standards, dates and terms are yours and the client's; I invent none, contract points go to a qualified adviser, and you send the document.

## Next
Run firm-proposal-red-team (Proposal Red Team Review) to have the whole draft read the way the buyer will read it.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
