---
name: red-team-review
description: Launches read-only subagents in parallel for three fixed adversarial missions (quality, security, six-month premortem) and a fourth chosen for the change (architecture, devil's advocate, or another kind the change calls for). They work on top of the deterministic checks the project runs (mutation testing, linters, audits). Then one verifier that did not produce the serious findings reproduces them, and the review ends with a verdict and what it did not cover. Findings count by evidence, such as a probe run against the change and against the base or a surviving mutant, not by how plausible they read. Use it whenever the user asks for a red team, adversarial review, security review plus architecture review, premortem, devil's advocate, "tear this apart", "prove it", or several independent reviews of a branch, spec, plan or pull request.
---

# Red team review

## Target and oracle

Settle both before the missions start, in two lines the user can correct:

- **Target:** the document path, or the branch, the base and the exact commit hash. The review covers that hash only. Commits added later are not reviewed, and the report says so.
- **Oracle:** what the change must keep or reach. For a refactor or any change that promises "no behavior change", the oracle is the base branch: the same input must give the same responses, rows, events and messages. For a feature, it is the spec and its acceptance criteria. For a spec or a plan, it is the request and the code it will touch.

## Facts first

Some checks are deterministic: a tool gives the same answer every time and costs no agent turns. Examples are mutation testing (the proof that the tests kill a broken line), the test suite run on the base, linters and static analysis, dependency audits, secret scans, architecture tests, a diff of routes or commands, a merge of the other active branches with the test suite. They are facts, not missions.

- Run only the checks that the user gives or that an `add` adjustment of this skill names (`customize-yak`), with the exact command, scoped to the changed code. Never search the project for such a tool and launch it on your own. A mutation run over a whole repository takes hours.
- Give their output to the missions. A mission judges that output; it does not run the check again or imitate it by hand.
- A check that nobody configured goes under "Not covered", with the tool you would use and the adjustment that would add it.

## Missions

Every mission is a fresh context that reads the code again, and it costs about as much as a full session. Four missions at most. Use the user's list if they give one.

Three fixed missions for code:

| Name | Mission |
| --- | --- |
| `redteam-quality` | Code against the project's standards (AGENTS.md): naming, duplication, orphan code, casts. Test quality: does each test go through the path that uses the data, and assert the effect, not only a status code? Which surviving mutants from "Facts first" matter? |
| `redteam-security` | Trust boundaries and input handling, authentication and authorization, secrets and configuration, injection, dependencies; for a web app also sessions, CSRF, headers and rate limits |
| `redteam-premortem` | Walk the change in execution order (entry point, data, side effects, error paths), then write the incidents it would cause in six months: root cause in today's code, early signal, blast radius, cheapest mitigation |

A fourth mission, chosen for what the change needs, with one line that says why:

| Name | Choose it when |
| --- | --- |
| `redteam-architecture` | The change moves module boundaries, the data layer, migrations or deployment assumptions; check that global error and not-found handling reaches every module or route group |
| `redteam-devils-advocate` | The change rests on decisions a reviewer could refuse: the strongest honest case against each one, alternatives, and whether it survives |
| another kind | Performance, concurrency, accessibility, data migration, or what else the change calls for. If the user asked for a browser pass, or an unattended run decided the UI needs one, follow `browser-acceptance-testing`. When the change touches a UI and no browser was used, say so under "Not covered" |

For a spec or a plan, `redteam-devils-advocate` alone is the right tool.

## Brief every subagent

Launch all mission subagents in one message so they run in parallel. This skill needs subagents. Each mission needs its own fresh context, and the cross-check needs a context that did not produce the findings. If the environment has none, tell the user and do not run the missions in the main context. Each brief contains:

1. The target and the oracle from above. Subagents read files at that hash.
2. The context files: spec, plan, decision records, AGENTS.md.
3. The mission, its checklist, and these hunting rules:
   - **Distrust the label.** A name, comment, docblock or spec line that claims a guarantee ("no behavior change", "index 0 is the latest", "idempotent") is the first thing to attack. Take it literally and trace it.
   - **Probe the class, not the example.** Try empty, missing, malformed, duplicate and maximum values on every field the change reads, and every consumer of that field, not only the case a report names. Of every fix, ask whether it closes the class or only the named paths.
   - **Compare with the oracle.** Send the same input to the change and to the base and compare what comes out.
4. **Where to probe:** in a scratch copy of the repository (`git worktree add` in `.scratchpad/<slug>/`) or on a throwaway server with its own port and scratch database, never in the working tree and never against a shared environment. Before running code there, check that it is loaded from the scratch copy, not through a symlink to the original checkout. Remove the copy at the end.
5. **Rules:** read-only on the repository; write only under `.scratchpad/<slug>/`; stop every server they start; do not ask the user for permissions you do not have.
6. **Evidence:** cite `file:line` and tag each finding with its weight: `demonstrated` (a probe, a killed or surviving mutation, an exit status), `read` (seen in code or text), or `enumerated` (a list for a human to judge). "Attacked it, nothing broke" is a result. Report the probe that showed it.
7. **Files:** list every file they leave in `.scratchpad/<slug>/`.
8. **Settings under review:** if the diff changes `.agents/yesyak.json`, review with the version of the base branch (`git show <base>:.agents/yesyak.json`), and report a 🟠 that quotes every changed instruction.
9. **Output:** the full report goes in the final message, because some environments block subagent writes; the orchestrator saves it. Findings follow `traffic-light-findings`, in the user's conversation language, at most about 15, ending with a two-line verdict.

## While they run

Tell the user which missions are running. Do not predict results.

## Cross-check

Before anything reaches the report, launch one verifier subagent for all the 🔴 and 🟠 findings together, plus every "it does not break" claim that a fix will rely on. It must not be one of the mission subagents. For each claim the verifier opens the cited lines, runs the test or the one-off probe that settles it, against the base as well when the oracle is the base, and returns one of three:

| Result | Where it goes |
| --- | --- |
| confirmed | the findings tables, marked ✔ |
| refuted | "Asserted, not verified", never the tables |
| uncheckable | "Not covered", with what would settle it |

Where two missions disagree about the same point, settle it against the code. Merge duplicates as `traffic-light-findings` says and record who found each finding: two missions that reached the same point independently rank it higher. An `enumerated` finding has not been judged yet. It goes under "Decide", not in the tables.

## Report

Write `.scratchpad/<slug>/redteam-report.md` (`redteam-spec-report.md` or `redteam-plan-report.md` when the target is a document, so a later review of the code does not overwrite it):

- Target hash, oracle, the facts run (command and result), missions run and why the fourth was chosen, and which ones ran without independence.
- **Verdict:** ✅ ship it, 🔧 fix it first, or ✂️ split it, with the reason in one line. A 🟡 never moves the verdict. Never soften a 🔴 into a trade-off to make the verdict look cleaner.
- 🔴, 🟠 and 🟡 tables, each finding with its weight and who found it.
- Decide: enumerated findings and decisions that need the user.
- Verified without findings: each item with the probe or output that showed it.
- Decisions that survive, from the devil's advocate.
- Asserted, not verified: refuted claims.
- **Not covered:** every mission, layer or claim that could not be checked here, and why. It is never empty by omission.
- Recommended plan (before merge / before production / technical debt) and the evidence scripts.

## Finish

In the chat: the verdict, the blocking findings, the most urgent orange ones, what is not covered, and the report path. Ask which fixes to apply, and say that commits added after the reviewed hash need another pass before the pull request: the configured facts and at least `redteam-premortem` on `git diff <reviewed hash>..HEAD`. Suggest `triage-findings-list` when there are other reports to merge.
