---
name: setup-ai-build-kit
description: Start or resume project setup with /setup-ai-build-kit. Use /implement after founding, or /shape for features and repairs.
---

# Setup AI Build Kit

Prepare a project without writing feature code.

## Conversation contract

Speak when the person must answer, decide, approve, understand a blocker, or
see a result that changes what they can do next. Finishing an internal step is
not a user-facing result by itself. Routine reading, research, setup, and
checking happen quietly. Ask every question in the shape clarify's rules
describe. Name a service only when the person must choose, own its account,
grant access, pay, or understand a limit; say what it is in one plain sentence
at the same moment.

## 1. Orientation

Before technical work, explain the private setup and checkpoint, and that
nothing will be published without approval. For existing work, say you will
first understand it. Explain permissions just before a box. Do not announce
that a confirmation might appear later.

Founding ends with a saved project. Record open questions with your best guess
and check gaps as tasks. If they say to continue, state assumptions and carry
on.

## Route

1. Load `references/resume.md`.
2. Run `scripts/check-tooling.sh` and follow `references/capability-check.md`.
   Ask whether to adopt existing work; if yes, use `references/adopting.md`.
3. Follow `references/need-for-software.md`, then run the `clarify` skill. Settle terms,
   facts and visual questions with evidence or a prototype.
   Keep questions visible. Save answers in ignored `.agents/tmp/setup-notes.md`
   before the next question. Load `references/stand-up.md` before the closing
   reply and include its menu.
   Python document-worker and existing-database recipe parts are not offered
   yet; `Fits:` lists tool shapes.
4. Run `fit-check`: its three questions, then access, risk areas, cautions
   and recheck triggers. Consider redesigns first. Give the risk notice before
   flagged work and record acceptance. An ownership no becomes a task.
5. Follow `references/write-the-masterplan.md`. If a risk area is named, run
   `second-opinion` on the masterplan before flagged work. Record findings; apply a
   stopping finding only with approval. Otherwise record why review was
   skipped. Check ownership.
6. Cut one-sitting vertical slices in dependency order, not database, API and
   UI pieces. Follow `references/cut-the-plan.md` to save them as issues.
7. Follow `references/stand-up.md` to prepare, check and save; report with
   `references/completion-report.md`.

Do not push or open a pull request during founding. The first upload needs
approval as described in `merge`.

## Done

Finish with `scripts/check-tooling.sh --conditions` at exit 0, records and
review, visible pieces, a passing check and a saved local checkpoint.
Record private Free limits; founding continues. End with
`/implement` and `/shape` in a fresh chat.
