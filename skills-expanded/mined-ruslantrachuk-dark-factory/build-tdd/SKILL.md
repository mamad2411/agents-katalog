---
name: build-tdd
description: >
  Use when the next step is to write the code of a planned piece of work — "build slice 1.1", "implement this
  task", "build 3.2 from tasks.md", a bd subtask with FILES and TESTS — and as the rules of the feature pipeline's
  implementers. Builds it by TDD (a failing test first, then the code, then the refactor), within the slice's files
  and the project's standards. Next: integrate.
---

# Skill `build-tdd` — one slice, test first

> Part of the dark-factory plugin. The method is the Superpowers `test-driven-development` skill (use it when it is
> installed); this skill adds what is specific to the factory.

## Steps

1. **Read the slice:** `bd show <id>` (without a bd queue, its entry in `tasks.md` or the task text) — its FILES,
   TESTS, ACCEPTANCE and any critic remarks — and the source it
   belongs to (the OpenSpec change, the spec).
2. **Read the standards in full:** the project's rules (`AGENTS.md`; a solo-kit project without one: `CLAUDE.md`) (with its list of known anti-patterns, if it has one) and
   `CODING_STANDARDS.md` (rule map by layer, general prohibitions, test pyramid, project language: layer
   responsibilities, where prompts, SQL, secrets and user-facing texts live, the language of logs, typed exceptions),
   and `naming.yaml` (the project map and glossary). Any user-facing text goes only through the project's message
   catalog.
3. **Read the actual code** around the slice: neighbouring modules, existing repositories, services, settings. Follow
   the neighbouring files; reuse what exists instead of writing a second one. Before a new component, style rule,
   helper or query, search for one with the same role (`grep` by class, function and key names) and extend it; a copy
   of an existing rule under a new name is the commonest review finding.
4. **RED → GREEN → REFACTOR.** A failing test first, then the code that makes it pass, then the refactor. Tests by the
   slice's TESTS, or, without one, the happy path and the rule's edge, error and negative cases — each at the rule's
   layer, not repeated at every layer. The layers, their directories and the project's profile are
   `CODING_STANDARDS.md` §Test pyramid — not this skill and not the neighbouring tests. Each
   test goes to the **lowest layer that can see what it checks**: a rule a pure function can decide — unit (extract
   the rule into a pure function if it sits inside a service or handler); a seam with a live dependency —
   integration; the HTTP contract — api, at most three per route (happy path, access, one error per rule call), while
   the branches of the rule stay in unit. Errors are asserted by code or key, not by message text; data is built by
   factories, not HTTP chains; no layout tests. Before writing a test, search for one on the same rule and extend it;
   a test this slice makes obsolete is deleted in the slice. Follow the neighbours in naming and fixtures, not in
   layer: twenty api tests next door are no reason to check a rule through HTTP. Tests of a lane this machine cannot
   run (e.g. a real database in Docker) are still written, following their neighbours; CI runs them.
5. **Run only the slice's tests** as you go (`pytest <abs path of the test file> -q`). The full suite is
   `integrate`'s job.
6. **Stay in the slice's files.** A new file only next to them (the same package or test folder). Migrations only
   when the spec allows them: a revision following its neighbours, up and down both written; otherwise the slice
   stops as failed with the reason.
7. **A screen built from a design checks itself before the report.** When the slice has design frames, serve the
   branch's frontend on a temporary stand (`stand.py start temp`, the `dev-stand` skill; `stop temp` after), take
   screenshots at each frame's width with
   the API stubbed in the browser (Playwright `page.route`), and put each frame next to its screenshot. Compare every
   pair and keep fixing until the only differences are ones you name; the named ones go into the report. Find the
   design's assets (images, icons) by listing the directory, not by typing their names (see the known traps on file
   names). A slice that changes a shared component also screenshots one other screen that uses it.
8. **Forks** not covered by the spec — KISS/YAGNI, and write each one down as an assumption: it goes into the PR
   description's `## Decisions`.
9. **Report:** files changed, test files, tests added, assumptions, the frame-to-screenshot differences left, and the
   status — done, partial (what is left),
   or failed (the missing precondition).

Comments and test descriptions are in the project language. Next: **`integrate`** — in a session right after each
slice; in a parallel wave the run's integrator does it for the whole wave.
