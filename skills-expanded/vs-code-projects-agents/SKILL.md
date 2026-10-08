# FAST Strength IT 195 Repository Guidance

## Purpose

This repository is the durable home for Peter's IT 195 e-commerce coursework and the FAST Strength Systems landing-page code. Keep IT 195 code, course requirements, UI feedback, decisions, tests, and handoff notes here.

IT 406 Capstone is a separate course with a separate context repository. Do not copy IT 406 assignments, research registers, participant data, decisions, or handoffs into this repository.

## Start of each session

1. Run `git status --short --branch`, `git remote -v`, and inspect the current upstream.
2. If the tree is clean and an upstream exists, run `git pull --ff-only`. Preserve uncommitted work or divergent history.
3. Read `README.md`, `docs/PROJECT_STATE.md`, `docs/HANDOFF.md`, and relevant entries in `docs/DECISIONS.md`.
4. Check `docs/COURSE_REQUIREMENTS.md` and `docs/ASSIGNMENT_TRACKER.md` before claiming that course requirements are complete.
5. State the current priority, blocker, and next action before substantive work.

## Working rules

- Keep the smallest functional e-commerce implementation that Peter can explain and demonstrate.
- Record Professor Menke's feedback accurately; distinguish direct feedback from interpretation.
- Define acceptance criteria before substantial features or UI revisions.
- Test desktop and narrow-screen layouts, keyboard access, local links, and failure states affected by a change.
- Do not invent prices, testimonials, customer results, credentials, or grading requirements.
- Do not commit credentials, private customer information, participant data, generated archives, or machine-specific state.
- Treat `backend/` as incomplete until authentication and data handling are deliberately designed and tested.
- Keep source code and course documentation together, but keep large generated deliverables and private data out of Git.

## End of substantive work

Update `docs/PROJECT_STATE.md`, `docs/HANDOFF.md`, and any relevant decision, requirement, test, or changelog entry. Record actual evidence and unresolved questions. When Peter asks to save, sync, wrap up, or prepare for class, review the diff, commit only intended files, push, and report whether the push succeeded.
