---
name: requirements-quality-check
description: Check an issue, requirement list, or linked document for consistency, ambiguity, contradiction, completeness, redundancy, validity, relevance, accuracy, clarity, correctness, entailment, and satisfiability, and report findings with evidence and severity. Use this skill whenever the Analyzer role gets an issue or document to analyze, review requirements, or validate a specification, even if the request only says "check this" or "is this OK".
---

# requirements-quality-check

Poor requirements cause the most expensive mistakes because everything else is built on them. The Analyzer finds problems while they are still cheap.

## Procedure

1. Read the issue, all comments, and the document it links. If the link cannot be opened, report that as the first finding and stop. Do not review from memory.
2. Run the lint script for a first pass on wording problems:

```bash
python3 $AGENT_INFRA_DIR/harness/library/skills/requirements-quality-check/scripts/check_requirements.py requirements.md
```

It finds vague words, TBD markers, missing `shall`, long sentences, passive voice, duplicates, and possible contradictions. It cannot judge meaning.
3. Read each requirement against the twelve criteria in `references/criteria.md`. Spend most time on the ones a script cannot see: consistency across requirements, entailment, satisfiability, accuracy, correctness.
4. Run `asd-ste100` on the wording and `principles-check` for the project principles (`PRINCIPLES.md`, `COMMON_MISTAKES.md`).
5. Write the findings to the wiki page `Requirements Review` (see `gitea-wiki`) using this table: `ID | criterion | severity | evidence | fix`.
6. Comment on the issue (see `issue-comment-protocol`): counts by severity, the wiki page, and the next step. Any `high` finding goes back to the Coordinator as `blocked` because the Human may need to decide.

## Judgement rules

- A finding needs evidence: a short quote and its location.
- Propose a concrete fix wording. Do not only say "unclear".
- Do not rewrite requirements yourself. Meaning belongs to the Human. Suggest and let the Coordinator escalate.
- Say what you could not check (for example, no access to a referenced standard).
