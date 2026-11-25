---
name: skill-audit
description: Review the user's installed Claude Skills for overlap, dead weight, vague triggers, and gaps, then deliver a keep/merge/fix/delete action plan. Use whenever the user types /skill-audit, says their skills overlap or fire at the wrong times, asks which skills to keep or delete, wants their skill library cleaned up or organized, or asks "which of my skills are actually useful". Also use after a user has installed a batch of new skills and wants to know how they fit together.
---

# Skill Audit

A skill library degrades the same way a prompt library does: things pile up, two skills quietly do the same job, and descriptions get vague enough that nothing triggers reliably. This skill audits the collection and produces a ruthless, actionable cleanup plan.

## Step 1 — Get the inventory

Work from the best available source, in this order:
1. The skills visible in the current environment (if you can see an installed skills list, use it).
2. Otherwise, ask the user to paste their list from **Settings → Capabilities → Skills** — names are enough to start; descriptions make the audit much better.
3. If the user can share the actual SKILL.md files, audit those — that enables the deepest checks.

Never invent skills the user didn't confirm having.

## Step 2 — Map each skill to its job

For every skill, write one line: **the job it's hired for**, in the form "when [situation], produce [output]". If you cannot write that line from the skill's name and description, that is itself a finding — the skill has a triggering problem.

## Step 3 — Run the five checks

1. **Overlap.** Two or more skills hired for the same job (e.g. a /humanizer and an /anti-ai that both strip AI tells). Overlapping skills split triggering unpredictably — Claude may pick either one. Verdict: merge into one, or sharpen each description until the boundary is unambiguous (e.g. one runs on drafts, the other runs during prompt-writing).
2. **Vague triggers.** Descriptions like "helps with productivity" or "improves writing" — categories, not situations. These undertrigger (Claude skips them) or overtrigger (they fire on everything). Verdict: rewrite the description to name the exact user phrases and situations that should fire it.
3. **Dead weight.** Skills that duplicate what Claude does well with a one-line prompt (e.g. a skill that just says "summarize this"). A skill earns its slot by encoding a *procedure, format, or standard* Claude wouldn't apply by default. Verdict: delete, and note the one-line prompt that replaces it.
4. **Scope creep.** One skill doing three jobs ("writes posts, replies to comments, and plans content"). Multi-job skills trigger at the wrong times and dilute their instructions. Verdict: split, and name the resulting skills.
5. **Gaps.** Look at the user's actual recurring workflow (ask one question about it if unclear) and name at most 2-3 missing skills that would compound with the existing ones. Do not pad this list — a gap is only real if the user repeats that task weekly.

## Step 4 — Deliver the audit

ALWAYS use this exact structure:

```
## Inventory
[N] skills audited.

## Findings
| Skill | Job it's hired for | Verdict | Why |
|-------|--------------------|---------|-----|
| /name | when X, produce Y  | ✅ Keep / 🔀 Merge / 🔧 Fix description / 🗑️ Delete / ✂️ Split | one line |

## Action plan (do in this order)
1. [Highest-impact action first — usually the merge or the worst description fix]
2. ...

## Rewritten descriptions
[For every 🔧: the ready-to-paste replacement description,
naming concrete trigger situations and user phrases.]

## Gaps worth filling (max 3)
- /suggested-name — [the recurring job it would do]
```

## Judgment calls

- **Be conservative with 🗑️.** Deleting a skill the user loves destroys trust in the audit. If usage is unknown, mark it "🗑️ Delete (confirm: when did you last use this?)" instead of asserting.
- **A healthy library is a valid result.** If the collection is clean, say so, fix the one or two weakest descriptions, and stop. An audit that always finds problems is a horoscope.
- **Merges must be concrete.** Never just say "merge A and B" — state the merged skill's name, its one-line job, and which instructions survive from each parent.
- **Respect the library's purpose.** A content creator's library and a developer's library have different "dead weight" thresholds. Judge each skill against the user's actual work, not an abstract ideal.
