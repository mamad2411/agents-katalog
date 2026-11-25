---
name: codebase-audit
description: Run a principled whole-repository quality audit of a Python codebase, its tests and its OpenSpec specs — duplicated logic, test-only public API, error-type taxonomy, docstring/signature drift, module split points, near-duplicate and coverage-subset tests, private-detail tests, fragmented or near-duplicate capabilities — where deterministic scripts sweep every site and the model only judges candidates. Use when asked to audit a codebase for consolidation, plan a tidy/refactor pass, consolidate an OpenSpec spec tree or a test suite, or check an external audit's coverage.
argument-hint: [repo-path] [--dimensions a,b,...]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Skill: codebase-audit

Audit one repository. The repository is `$ARGUMENTS`, or the current directory.
`<scripts>` is `${CLAUDE_PLUGIN_ROOT}/skills/codebase-audit/scripts`.
`<refs>` is `${CLAUDE_PLUGIN_ROOT}/skills/codebase-audit/references`.

The rule that makes this audit principled: **a script counts, the model judges.** Never
sample a dimension and call it swept. A dimension is done when every candidate its script
emits has a verdict.

## Steps

1. **Scope.** Find the package (`src/<pkg>`), the tests, the specs (`openspec/specs/`),
   and the project rules (`CLAUDE.md`, `.claude/rules/`). Read the rules first: a finding
   that contradicts a recorded decision must name the rule and say why it is wrong.
   Note out-of-scope topics the project states, and keep them out.
2. **Interpreter.** Run every script with the project's own Python (`.venv/bin/python`),
   so `ast` parses the target syntax. The scripts use only the standard library and never
   import the code under audit.
3. **Baseline.** Run the test suite once with coverage contexts, so step 4 can use it:
   `pytest --cov=<pkg> --cov-branch --cov-context=test -q`. Record pass/skip counts.
   For anything over a few minutes, use a named tmux session.
4. **Sweep.** Run each dimension's script from `<refs>/dimensions.md`. Save each report
   under `<out>/` (default `/tmp/audit-<repo>/`). Each report states its method and its
   count: copy both into the final report verbatim.
5. **Recall check.** Before trusting a script on this repo, confirm it finds any known
   positives (earlier findings, a planted case). If it misses one, tune the script's
   threshold, rerun, and say so in the report.
6. **Judge.** For every candidate, read the code and decide `finding`, `rejected` (with a
   one-line reason) or `merged` (into another finding). Use the judgment rule for that
   dimension in `dimensions.md`. Delegate reading to subagents for large candidate sets,
   one dimension per subagent, giving them the rule and the candidate list.
7. **Verify.** Re-read the cited lines of every finding. Classify each as value-neutral
   (name the test that proves it) or value-changing (say what changes).
8. **Report.** Write the report with `<refs>/report-template.md`. A "checked and sound"
   line carries its method and its count, or it is not written.
9. **Triage.** Route each finding with `<refs>/triage.md` into the repo's own work units
   (OpenSpec changes, plans, issues). Ask the user before creating a new unit.

## Handing the audit to another tool

To get an independent read from another model, follow `<refs>/external-brief.md`. Give
it the script reports to judge, not dimensions to sweep: external tools sample.

## Constraints

- Propose; do not edit source, tests or specs during the audit.
- One row per pattern, with every site and the count. Never write "many".
- A coverage subset is a candidate, never a finding: equal coverage is not equal
  assertions.
- Do not propose a deprecation in a pre-release project; propose the removal.
