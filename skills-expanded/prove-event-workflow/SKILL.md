---
name: prove-event-workflow
description: >-
  Use when a PR adds or changes a GitHub Actions workflow that fires on anything
  but pull_request or push (issues, issue_comment, schedule, workflow_run), or
  when reviewing one.
metadata:
  author: Spool maintainers
---

# /prove-event-workflow — proving a workflow PR CI never fires

*Moved verbatim from `docs/CONVENTIONS.md` (#470), which keeps the one-line rule
and points here. The rule binds whether or not this skill is loaded.*

**Proving an event-driven workflow** (#209): a workflow that fires on
anything but `pull_request` or `push` — `issues`, `issue_comment`,
`schedule`, `workflow_run` — is never exercised by PR CI, so it can merge
broken and stay broken until someone reads the Actions tab. Three did in one
week (#203, #207). So: every such workflow also declares `workflow_dispatch`
with inputs standing in for the event payload, and a PR that adds or changes
one links **a green dispatched run from its own branch**, against fixture
data, in the template's Verification section. The reviewer checks that link
the way they check CI; a PR without it is not ready. After the merge the
author runs it once more on `main` via a real event and reports it on the
PR — the dispatched run proves the code, the real event proves the trigger.
`scripts/workflow-lint.sh` (a step of CI's `checks` job) enforces what a file can
show: the missing dispatch, a checkout without `contents: read` (#203), and
an event body interpolated anywhere in a workflow, `env:` included (#207).
**The exception is a brand-new workflow**, which cannot be dispatched at
all: GitHub dispatches only workflows already on the default branch, and
answers `404 … not found on the default branch` for one that lives on a
branch (measured on #210). So a PR *adding* a workflow says that in
Verification instead of linking a run, carries whatever evidence it can
reach — a harness that runs the real step, not a copy of it — and its
author dispatches it the moment it lands, reporting the run on the PR. The
reviewer holds the author to that last step; until it happens the workflow
is unproven, however green the PR was.
