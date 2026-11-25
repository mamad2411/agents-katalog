---
name: bug-intake
description: Entry point for one bug report. Capture it, triage it without changing anything (severity, owning area, layers crossed with file and line, kind), find the expected behavior even when there is no spec, reproduce it with a failing automated test, trace the root cause across every caller, give it a traffic light and choose the route (fix against an existing contract, write the missing contract first, treat it as a feature, or stop because it does not reproduce), then run the short fix route of the feature-delivery-pipeline. yak-pilot starts it for a bug report (a regression, an error, a stack trace, a log line, "it does not work", "it returns a 500", "hotfix"). Use it directly when the user asks only to triage an issue, names it, or yak-pilot is not installed. It is not triage-findings-list, which merges review reports into a change list later in a pipeline.
---

# Bug intake

A bug report names a symptom. This skill turns it into a triage, a failing test, a root cause and a route. The pipeline's spec phase does not apply. There is no interview and no plan, and there may be no spec at all.

## 1. Capture

Write down, in the user's words where possible:

- What happened: the request, the screen or the command, and the answer or error.
- What the reporter expected.
- Where: branch or commit, environment, configuration that matters.

Ask only for what is missing and needed to reproduce. In an unattended run, record the assumption as a `Q-` entry (`unattended-run`).

## 2. Triage

Read the report and the code it needs. Change nothing yet: no file, no test, no branch. Give:

1. **Severity.** A light with `traffic-light-findings`, impact and likelihood together, and why in one sentence.
2. **Owner.** The area of the project that takes care of it, if the project has areas or teams (for example data, backend, frontend, product).
3. **Layers.** The layers of the architecture it crosses (for example source data, import, storage, API, interface), each with `file:line`.
4. **Kind.** For example a code bug, a data bug, a missing requirement, an interface problem, legacy code or performance.

A report can be partly wrong, whoever wrote it: a user, a teammate or an agent. Say which parts of it the code confirms, which parts it contradicts, and which parts you cannot check yet. Show the triage and ask before you go on. In an unattended run, log it as a `Q-` entry and go on.

## 3. Find the contract

The expected behavior must come from somewhere. Look in this order and write down which source you used:

1. The acceptance criteria of a feature spec (`docs/<slug>-spec.md`).
2. The decision records (`docs/decisions/`).
3. A published contract or the project docs: OpenAPI or JSON schema, CLI help, public docs, README, AGENTS.md.
4. Existing tests, and sibling code that already handles the same case (for example another route that already answers `400` to a bad id).
5. The reporter's expectation.

Sources often cover only part of the case. An OpenAPI parameter can say `minimum: 1` and still not say which status a bad value gets. Take what the sources say, and name the gap.

When no source decides the behavior, the expected behavior is a decision. Choose the option that matches the sibling code and the published contract. Write it in the bug report as **assumed contract**. Ask the user, or log a `Q-` entry in an unattended run. The regression test then becomes the contract. Record an ADR only when the choice is irreversible (for example, a status code of a public API) or a reviewer would really question it (`decision-record-log`).

## 4. Reproduce

Write the smallest automated test that fails for the reported reason. Put it at the layer where the user meets the bug (an HTTP test for an API answer, a unit test for a query), in the test file of that route or module. Run it and read the failure. It must fail for the reason in the report, not for a setup mistake.

A script is acceptable only while you explore. The fix starts from a test.

If it does not reproduce after two honest tries, stop and take route D.

## 5. Find the root cause

- Follow the code path from the entry point to the line that goes wrong.
- Grep every caller of the function you are going to change, and every sibling with the same pattern (the same parser, the same unchecked body, the same query).
- Fix at the shared point when the siblings share the cause: one guard in the shared function is a smaller change than one guard in each caller.
- Siblings with the same cause are in scope. Other bugs you find on the way are not. Write each one as a separate report line.

## 6. Route

Update the light of the triage with what the reproduction and the root cause showed. A 🔴 in production is a hotfix. The fix, the test and the pull request come first. Verification, review and retrospective come right after.

| Route | When | Next |
| --- | --- | --- |
| A | A contract exists and the code breaks it | Fix route |
| B | No contract, or it is wrong or silent on this case | Write the contract first (`write-acceptance-spec` if a spec exists; otherwise the assumed contract, the regression test and the PR text), then the fix route |
| C | The report asks for behavior that nobody promised | `feature-delivery-pipeline` from `on-the-spot` |
| D | It does not reproduce, or the cause is the environment or the configuration | Stop. Report what you tried and ask |

## 7. Write the bug report

Save `.scratchpad/<slug>/bug-report.md` in the conversation language:

```markdown
# Bug: <one line>

| | |
| --- | --- |
| Light | 🔴 / 🟠 / 🟡 and why |
| Owner, kind | area of the project, kind of bug |
| Route | A / B / C / D |
| Found at | branch or commit |

## Report          what happened, what was expected, where (quote the reporter)
## Triage          layers with file:line; what the code confirms or contradicts
## Contract        sources checked, what each says, the gap, the assumed contract if any
## Reproduction    test file and name, and the failure output
## Root cause      file:line, callers and siblings checked, which share the cause
## Scope           what this fix covers; other bugs found, one line each
```

## 8. The fix route

The fix route reuses the pipeline's skills in a shorter order:

1. Branch `fix/<slug>` (`git-commit-organizer`). If the project has a git host, check now that the branch can reach it; without one, the PR body stays local. Save `bug-report.md` (section 7) and start `progress.md` before you change any code.
2. `execute-plan-loop` in change-list mode. Item 1 is the failing test with the fix. Each sibling with the same cause is its own item: write its reproduction test when you start that item, so each commit keeps the suite green.
3. Check in proportion to the risk. The checks that are not deterministic (`red-team-review`, `browser-acceptance-testing`) cost the most; run them when the risk asks for them. Say which ones you skip and why.

   | Light of the bug | Checks |
   | --- | --- |
   | 🟡 For example a typo in a message | The regression test and the full test suite |
   | 🟠 Something does not work, or visible data is wrong | Also the affected criteria or contract (`verify-against-spec` when a spec exists) |
   | 🔴 Data lost, a service down, or security | Also `red-team-review` with one or two missions, and `browser-acceptance-testing` when the user meets the bug in an interface |
4. Never skip the regression test, even when you skip other checks.
5. `write-visual-pr`, with its short body for a bug fix.
6. `session-retrospective-rules`, always, with one question first: why did no test, verification or review catch this bug? The guard goes where it should have been caught.
