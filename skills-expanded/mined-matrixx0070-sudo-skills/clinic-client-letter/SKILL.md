---
name: clinic-client-letter
version: 1.0.0
description: Draft plain-but-accurate correspondence to a clinic client — advice, status, or closing letters — for supervising-attorney review before anything is sent.
author: matrixx0070
tags: [legal-clinic, client-letter, correspondence, plain-language, supervision, scope]
capabilities: []
---

## When to use
Use this when you need to write directly to a client: an advice letter conveying an approved recommendation, a status update on their matter, or a closing letter ending the representation. Good client correspondence is accurate, plain, and stays inside the approved scope — it keeps the client informed (Rule 1.4) without overstating what the clinic can do.

**Not for:** internal contact records (use clinic-client-comms-log), the initial screening and relationship decision (use clinic-client-intake), or reusable process templates (use clinic-build-guide). A student draft is never final: nothing here goes to the client until the supervising attorney reviews and approves it, and no letter may state advice beyond what the attorney has approved (Rule 5.5 / UPL).

## Method
1. Confirm the letter's purpose (advice / status / closing) and the approved scope it must stay within.
2. State the client's situation and the letter's point in plain language, avoiding jargon and false certainty.
3. Convey only advice the supervising attorney has approved; where a question is open, say it is under review rather than guessing (Rule 5.5 / UPL).
   **Decision point:** if drafting tempts you to answer something not yet approved, stop and flag it for the attorney instead of writing it — students do not extend advice independently.
4. For closing letters, state that representation is ending, note deadlines the client must now handle, and how to retrieve their file.
5. Keep client-identifying content out of external or AI drafting tools; draft within secure clinic systems (Rule 1.6; ABA Op. 512).
6. Submit the draft for supervising-attorney review; send only after written sign-off.

## Example
> Draft status letter to client "A.G.": "Dear Ms. G — We filed your expungement petition on July 9. The court set a hearing for August 14; we will prepare you beforehand. You do not need to take any action now. We will update you if anything changes." [DRAFT — pending Prof. Nguyen review before sending.]

## Pitfalls
- Sending a draft before the supervising attorney signs off — student work is not final.
- Stating advice or predicting outcomes beyond the approved scope (Rule 5.5 / UPL).
- Overusing legal jargon so the client cannot actually understand the letter (Rule 1.4).
- Drafting in external or AI tools that expose the client's name and facts (Rule 1.6).

## Output format
```
[DRAFT — pending attorney review; do not send]
Date: <YYYY-MM-DD>   Type: <advice / status / closing>
Approved scope: <ref>   Drafted by: <student>   Reviewer: <attorney>

Dear <client>,

<plain-language body: situation, approved point, next steps>
<open items -> "under review", not guessed>

<for closing: representation ending, client's deadlines, file retrieval>

Sincerely,
<student>, under supervision of <attorney>, <Clinic Name>
```

## Reference
- Model Rules 1.4 (communication), 1.1 (competence), 1.6 (confidentiality), 5.5 (UPL — supervision required).
- ABA Formal Opinion 512 — competence and confidentiality when using GenAI to draft client correspondence.
- Clinic norm: every client-bound letter is attorney-reviewed and signed off before sending.
