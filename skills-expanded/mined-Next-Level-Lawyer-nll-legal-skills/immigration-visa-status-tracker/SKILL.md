---
name: immigration-visa-status-tracker
description: Parse USCIS case status pages, receipt notices, and status-check emails to track where a case stands, flag priority date movement against the Visa Bulletin, and draft a client-facing status update. Use whenever the user pastes a USCIS case status, receipt number, processing time page, or Visa Bulletin data and wants to know what it means, whether something moved, or wants a client update drafted. Also use for bulk status checks across multiple clients/receipt numbers.
---

# Immigration Visa Status Tracker

Turns raw USCIS status text (or a batch of receipt numbers) into a plain-English case status and a client-ready update, without making the client guess what "Case Was Received" vs "Request for Additional Evidence Was Sent" actually means for their timeline.

## Workflow

1. **Parse the input.** Accept: pasted USCIS status text, a receipt number list, a Visa Bulletin excerpt, or a processing-times page. If the user gives only a receipt number with no status text, ask them to paste the status page content (no live USCIS access).
2. **Classify the status** into one of: Received, RFE Issued, RFE Response Received, Interview Scheduled, Approved, Denied, Transferred, Administrative Processing. Note the raw USCIS wording alongside the plain-English classification — don't discard it.
3. **Check for movement.** If prior status is known (from conversation history or provided), state explicitly what changed and how many days/weeks since the last update. If a priority date is involved, compare it against the relevant Visa Bulletin category/chargeability area and state whether it's current, and if not, the gap.
4. **Flag anything time-sensitive**: RFE response deadlines (typically 30/60/87 days depending on notice — use the date printed on the notice, never assume), biometrics appointments, interview dates.
5. **Draft the client update** (see format below) unless the user only wants the internal read.

## Output format

**Internal read:**
```
Receipt: [number] | Case type: [I-130/I-485/etc.]
Status: [plain-English] (USCIS text: "[verbatim status]")
Since last check: [what changed / no change, X days]
Deadline flag: [none / RFE due by DATE / interview on DATE]
```

**Client update draft** (only when requested — match AK's tone: warm, brief, no filler):
```
Hi [name],

Quick update on your case — [1-2 sentence plain-English status]. [If applicable: here's what we need from you / what happens next]. [If nothing needed: nothing needed on your end right now, we'll keep you posted].

[Sign-off]
```

## Notes

- Never guess at a receipt number's status without source text — pull from what's provided.
- Priority date current ≠ approval imminent; say so if the user seems to be conflating the two.
- Don't editorialize on processing time complaints; state the facts and the next concrete step.
