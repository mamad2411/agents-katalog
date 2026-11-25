---
name: tax-notice-response-drafter
description: Parse IRS or state tax notices (CP2000, audit letters, penalty notices, collection notices) and draft a structured response outline or template. Use whenever the user pastes IRS/state notice text, asks what a specific notice code means, or wants a response drafted or outlined for a tax notice.
---

# Tax Notice Response Drafter

Turns an IRS/state notice into a plain-English explanation and a structured response, so the client isn't left guessing what a CP2000 or audit letter actually requires.

## Workflow

1. **Identify the notice type** from the notice number/code if present (e.g., CP2000, CP504, Letter 566, audit notice) and state in plain English what it means and what triggered it.
2. **Extract the specifics**: proposed changes/amount, tax year(s), response deadline, and what documentation or action the notice requests.
3. **Assess the client's position**: does the user's information suggest the notice is correct, partially correct, or disputable? Note what documentation would support disputing it (don't assert it will succeed).
4. **Draft the response structure**:
   - Acknowledgment of the notice (reference notice number/date)
   - Position statement (agree / partially agree / disagree, with basis)
   - Supporting documentation list (attached or to be gathered)
   - Requested outcome (accept adjustment / propose correction / request additional time)
5. **Flag the deadline prominently** — many notices (especially CP2000) have real consequences for non-response (assessment becomes final).

## Output format

```
RESPONSE DEADLINE: [date from notice]
Notice type: [code] — [plain English meaning]
Proposed change: [amount/adjustment] for [tax year]

### Response outline
1. Acknowledgment: [reference notice details]
2. Position: [agree/disagree/partial, with basis]
3. Supporting documents: [list]
4. Requested outcome: [specific ask]
```

## Document Output Format

For the actual response letter, use the `docx` skill for a proper business letter:

- **Letterhead block:** firm/CPA firm name/address/phone placeholder, formatted per standard business correspondence convention.
- **Date, IRS/state agency address, notice reference line** (notice number, tax year, taxpayer ID reference — redacted/placeholder as appropriate).
- **Body:** professional serif font (Times New Roman or Garamond, 12pt), 1" margins, single-spaced with blank lines between paragraphs.
- **Supporting documents list:** clean numbered list, referenced consistently if attached as exhibits.
- **Signature block:** attorney/preparer name and firm placeholder.
- Surface the response deadline prominently at the top of the document itself (bold, or in the Re: line), not just in your chat summary.

## Notes

- Never assert a dispute will succeed — describe the documentation/argument that supports the client's position and flag that attorney/CPA judgment applies to strategy.
- Always surface the response deadline before anything else — missed deadlines on these notices often convert a disputable issue into a final assessment.
