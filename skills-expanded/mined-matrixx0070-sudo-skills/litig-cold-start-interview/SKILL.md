---
name: litig-cold-start-interview
version: 1.0.0
description: Run an initial client interview from a cold start to elicit the story, issues, timeline, documents, and goals.
author: matrixx0070
tags: [litigation, client-interview, intake, fact-gathering, timeline]
capabilities: []
---

## When to use
Use this when you meet a new client with no prior context and must extract a coherent picture in one sitting. The aim is to get the full story, spot legal issues, build a timeline, inventory documents, and learn what the client actually wants — without prematurely narrowing.

**Not for:** demand-specific intake once a claim is chosen (see litig-demand-intake) or evaluating a received demand (see litig-demand-received).

## Method
1. Open with a narrative prompt: let the client tell the whole story uninterrupted first, then probe.
2. Run a conflicts check on every party and entity name before going deep.
3. Build a dated timeline of events, capturing who did what and when.
4. Identify legal issues emerging from the facts — flag, don't yet resolve.
5. Inventory documents, communications, and potential witnesses; ask what exists and where.
6. **Decision point:** if a limitations or notice deadline looks imminent, stop and escalate to the attorney before the meeting ends.
7. **Decision point:** if a conflict surfaces, pause substantive intake until it is cleared.
8. Elicit the client's goals and constraints (money, vindication, speed, relationship, budget).
9. Explain confidentiality and next steps; set expectations about scope and engagement.
10. Route your issue-spotting summary to a supervising attorney before giving the client any assessment of the claim's strength.

## Example
> Prospective client describes a partnership souring over misused funds. You take the narrative, run conflicts on both partners and the LLC, timeline the capital contributions and withdrawals, flag possible breach-of-fiduciary-duty and conversion issues, list bank records and the operating agreement to collect, and learn the client wants a buyout, not a public fight.

## Pitfalls
- **Leading the witness.** Feeding the client a theory shapes their memory; use open questions before closed ones.
- **Skipping conflicts.** Substantive discussion before a conflicts check can disqualify the firm and breach ethics rules.
- **Premature advice.** Assessing the claim's merits in the first meeting, before facts are verified, risks wrong and unauthorized advice.
- **No document plan.** Leaving without a concrete list of what to collect and preserve stalls the matter and risks spoliation.

## Output format
```
CLIENT: <name / entity>
CONFLICTS CHECK: <cleared / pending>
NARRATIVE SUMMARY: <the story, client's words>
TIMELINE: <dated events>
ISSUES SPOTTED: <flagged theories>
DOCUMENTS / WITNESSES: <inventory + location>
DEADLINES: <limitations / notice>
CLIENT GOALS: <outcome, budget, constraints>
NEXT STEPS: <collection / hold / engagement>
ATTORNEY REVIEW: <pending / cleared>
```

## Reference
Under ABA Model Rule 1.18, prospective clients receive duties of confidentiality even if no engagement follows — treat everything as privileged and screen carefully. Conflicts screening (Rules 1.7 and 1.9) must precede substantive discussion to avoid imputed disqualification. The attorney-client privilege attaches to communications for the purpose of obtaining legal advice, but the crime-fraud exception and waiver by third-party presence can defeat it. Begin preservation counseling early, since the duty to preserve arises when litigation is reasonably anticipated. Open-ended, non-leading questioning produces more reliable and admissible accounts. This is general information, not legal advice; ethics rules and privilege doctrine vary by jurisdiction and a licensed attorney must apply them to the specific matter.
