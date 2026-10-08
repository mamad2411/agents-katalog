---
name: ai-output-review
description: "Review AI-generated code or text before accepting it, spec diff, verifier run, secret scan, and the AI smell list. Use before merging any agent-produced change."
version: 1.0.0
author: Zorost Intelligence
license: MIT
metadata:
  zorost:
    tags: [code-review, harnesses, verification, verify]
    related_skills: [agent-loop-safety, spec-first-ai-feature]
    program_weeks: [12, 13]
---

# AI Output Review

## 1 · Purpose

Make "the agent wrote it" pass the same bar as "a junior hire wrote it", read it,
run it, and check it against the spec, because AI output fails in different places
than human output.

## 2 · When to use

- Before accepting any non-trivial agent-produced diff, document, or config.
- When reviewing a teammate's PR that smells AI-generated and unreviewed.

## 3 · Inputs

- The spec or task statement the agent worked from.
- The diff or artifact.
- The project's verifiers: tests, linters, type checks, evals.

## 4 · Procedure

1. **Read the diff against the spec first.** Ask of every changed block: which
   spec line does this serve? Unmotivated changes are the AI smell parade's grand
   marshal.
2. **Run the verifiers yourself.** Tests, types, lint, on your machine or CI, never
   from the agent's claim that they passed. The agent's "all green" is a statement
   about its context window, not about the repo.
3. **Scan for secrets and egress.** New endpoints, new domains, tokens in comments,
   telemetry you did not ask for. AI loves a helpful analytics call.
4. **Run the smell list.** Each is innocent alone; three in one diff is a rewrite:
   - Unused imports, variables, and "future-proofing" abstractions.
   - Comments that narrate the code instead of the why.
   - Error handling that swallows (`except: pass`, empty catch).
   - Dependencies added for one-liners.
   - Config keys that nothing reads.
   - Docstrings describing a different function than the one below them.
5. **Check the blast radius.** What runs this code, with which credentials, on what
   data? Match the review depth to that answer, not to the diff's size.
6. **Require the agent's own evidence.** If the workflow produced a trace, test
   output, or eval score, it must be attached. No evidence, no merge.
7. Decide: accept, request changes (specific, numbered), or reject. "Looks fine"
   after 30 seconds on 400 lines is a rejection of the review, not an acceptance of
   the code.

## 5 · Anti-rationalization

| Excuse | Answer |
|---|---|
| "The tests pass; that's enough." | Tests check what they check. The spec check and the smell list check the rest. |
| "It's mostly boilerplate." | Boilerplate is where the hardcoded secrets and wrong defaults live. |
| "The agent is better at this than me." | The agent is faster. You are accountable. Different axes. |
| "I'll catch issues in QA." | QA catches behavior. Review catches intent. You need both. |

## 6 · Red flags

- The diff includes changes nobody asked for.
- "All tests pass" with no attached output.
- A new dependency with no lockfile change discussion.
- The reviewer cannot explain one of the changed blocks in their own words.

## 7 · Verify

- Every changed block is traceable to a spec line or flagged as unmotivated.
- Verifier output (not claims) is attached.
- Secret/egress scan done and noted.
- Smell-list findings are zero or individually justified.

## 8 · ZoroLogistics example

Week 12 to 13: the harness "implements the ETA CLI from SPEC.md" and adds an
unrequested `analytics.py` posting usage to a third-party endpoint, plus a
`retry_helper` used nowhere. Tests pass, the agent ran them, but the spec check
flags both blocks in two minutes. Request changes: remove both, attach the test
output, resubmit. Total review cost: 10 minutes. Cost of merging it: a supply-chain
questionnaire nobody wanted to answer.

---
© 2026 Zorost Intelligence LLC · zorost.com
