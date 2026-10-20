---
description: Stress-test your venture the way an investor will, before they do. Say "what would an investor say" or "am I ready to raise" (or run /founder-os:self-diligence). Five scored dimensions, SWOT, and the questions you will be asked.
argument-hint: <optional - the business or venture, if you run more than one>
allowed-tools: ["Read", "Bash"]
---

# Founder OS self-diligence

Run the self-diligence skill at `skills/self-diligence/SKILL.md` end to end.

## Procedure

1. Read `skills/self-diligence/SKILL.md`.
2. Run `python scripts/check-identity-ready.py`. If it exits 1, surface the line verbatim and stop.
3. If `$ARGUMENTS` names a business, scope the read to it. If empty and `companies/` holds more than one, ask which. If empty and there is one, use it.
4. Read the file list in the skill. Do not ask the founder for anything already written down.
5. Produce the output block in the skill exactly: scores, per-dimension, SWOT, critical challenges, disclosed gaps, and the questions.
6. Read-only. Write nothing unless the founder asks for the read to be saved.

## Rules

- Never invent a fact or a number. Anything not grounded in the files becomes a question to the founder.
- No evidence is not a middling score. Report it as unscored with the question that would fix it.
- No em dashes or en dashes. No banned words.

<!-- private-tag: not applicable: read-only analysis over the founder's own files; writes nothing -->
