---
name: consulting-call-questions
description: Use when David is preparing for or running a consulting call (lawyer, accountant, tax advisor, etc.) and wants to manage a question list — adding, marking as asked, moving between Main/Potential, or tracking answers. Triggers on consulting call, advisor call, prep questions, mark as asked, add question to call.
---

# Consulting Call Questions

Manage David's question list for a consulting call. One file per call.

## File location

`work/legal/[org]/consulting-call-[advisor-firstname]-DD-MM-YYYY.md`

## File structure

```markdown
# Consulting Call — [Person] ([Org])

**Date:** DD-MM-YYYY
**Advisor:** [Name], [Org]

---

## Already-Made Decisions
- decision: [...]

## Main Questions

1. [question]
2. [question]

---

## Potential Questions

3. [question]
4. [question]

---

## Notes

_(fill in during/after the call)_

---

## Action Items

_(fill in after the call)_

---

## Already-Asked Questions

- [question]
  - _(answer:)_
```

## Hard rules

1. **Verbatim questions.** When David gives you a question, add it **exactly as he wrote it**. Do not rewrite, rephrase, fix grammar, or "improve" it. Same words, same order, same punctuation.

2. **Stage + commit + push after every change.** Immediately. No batching.
   ```bash
   git add [file] && git commit -m "[short msg]" && git push
   ```

3. **Be very concise.** Short sentences. No fluff.

## Numbering

- Main Questions + Potential Questions share **one continuous numbering sequence**.
- Main is 1..N, Potential continues N+1..M.
- **Never renumber when marking as asked or moving between sections.** Numbers stay as-is (gaps are fine).
- Only renumber when explicitly adding a new question that needs to fit into the sequence.

## Adding a question

Place it semantically:
- Framing/overview question → top of Main
- Follow-up to existing Q → directly after it
- Otherwise → end of Main (or end of Potential if low-priority)

## Marking a question as asked

1. Remove from Main/Potential.
2. Add to `## Already-Asked Questions` as:
   ```markdown
   - [question text]
     - _(answer:)_
   ```
3. **DO NOT renumber the remaining questions.** Leave the numbering as-is. Just remove the line and move it to the bottom.
4. Commit + push.

## Moving between sections

- Main ↔ Potential: cut from one, paste into the other, commit + push. Do NOT renumber.
