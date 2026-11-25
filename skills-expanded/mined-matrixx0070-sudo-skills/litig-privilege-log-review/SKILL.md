---
name: litig-privilege-log-review
version: 1.0.0
description: Build or review a privilege log with defensible entries, a stated privilege basis, adequate descriptions, and a waiver-risk assessment.
author: matrixx0070
tags: [litigation, discovery, privilege, work-product, waiver]
capabilities: []
---

## When to use
Use this when you are withholding or clawing back documents and must produce a privilege log, or when you are reviewing an opponent's log for gaps. It helps you assemble entry fields, articulate the privilege basis, test whether descriptions are adequate, and spot waiver exposure. Works for both attorney-client privilege and work-product claims.

**Not for:** deposition planning (see litig-deposition-prep) or subpoena responses (see litig-subpoena-triage).

## Method
1. Inventory each withheld document with metadata: date, author, recipients (including cc/bcc), type, and Bates or control number.
2. Classify the basis: attorney-client privilege, work-product, or both; note whether opinion or fact work-product.
3. **Decision point:** If a non-attorney or third party is on the communication, verify the common-interest or agency exception applies before asserting privilege; if not, the entry likely is not privileged.
4. Draft descriptions specific enough to justify the claim without disclosing privileged content ("email reflecting legal advice re: contract indemnity").
5. **Decision point:** If reviewing an opponent's log, flag conclusory entries ("legal advice") and missing recipients as grounds for a meet-and-confer or motion to compel.
6. Assess waiver: broad disclosure, subject-matter waiver, and inadvertent production (evaluate FRE 502 clawback).
7. ATTORNEY-ESCALATION gate: Route the log and all withholding calls to a supervising attorney for review before serving it.

## Example
> Reviewing your client's 40 withheld emails, you find six that cc an outside PR consultant. Because no common-interest agreement covers the consultant, you flag those as likely non-privileged, downgrade them for re-review, and route the full log to the supervising attorney before production.

## Pitfalls
- **Conclusory descriptions:** "Privileged communication" alone invites a motion to compel or in-camera review.
- **Third parties on the thread:** Copying a non-client third party can break privilege absent a recognized exception.
- **Subject-matter waiver:** Disclosing part of a privileged communication can waive the entire subject.
- **Forgetting FRE 502(d):** A court order can protect against waiver even for inadvertent production; not securing one raises risk.

## Output format
```
PRIVILEGE LOG
No. | Date | Author | Recipients (cc/bcc) | Type | Privilege basis | Description | Bates
Waiver-risk notes: [inadvertent / subject-matter / third-party]
502(d) order: [yes/no]
Attorney review: [name | date | status]
```

## Reference
Attorney-client privilege protects confidential communications made to obtain or give legal advice; work-product doctrine (FRCP 26(b)(3)) protects materials prepared in anticipation of litigation, with heightened protection for opinion work-product (attorney mental impressions). FRCP 26(b)(5)(A) requires a party withholding on privilege to expressly claim it and describe the nature of the documents in a manner that, without revealing privileged information, enables assessment of the claim. FRE 502(b) shields inadvertent disclosures where the holder took reasonable steps to prevent and promptly rectify; 502(d) lets a court order non-waiver. Privilege is generally waived by voluntary disclosure to third parties and can trigger subject-matter waiver when used offensively. Rules and log-format expectations vary by jurisdiction and standing order; confirm local practice. General information, not legal advice.
