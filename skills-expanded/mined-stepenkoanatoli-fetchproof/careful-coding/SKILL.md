---
name: "careful-coding"
description: Working discipline for writing code with fewer mistakes, catching the ones that slip through, reporting them honestly, and fixing the root cause. Use this skill on ANY coding task - writing, editing, refactoring, debugging, or reviewing code in any language or framework - even when the user does not ask for care or verification. Use it especially when the user says things like "be careful", "don't break anything", "make sure it works", "double check", "are you sure?", "did you test it?", "is it done?", when a previous attempt had a bug, or when a test or build fails. Covers understanding code before changing it, reproducing bugs before fixing them, verifying by actually running things instead of assuming, a mistake-report protocol (what, where, impact, cause, fix, how verified), and status summaries that separate verified from untested work.
---

# Careful Coding

Three rules carry the weight: **look before you change**, **prove it instead of assuming it**, and **when you are wrong, say so first, then fix the cause**.

Most assistant coding errors are not hard problems. They are skipped steps: editing a file unread, calling an API from memory, writing "should work" instead of running it, quietly loosening a failing test. Each costs seconds to prevent and hours to find later. A hidden or softened mistake costs more than the bug: it costs the user's ability to trust the rest of the work.

## 1. Before changing anything

**Read what you will touch, and what touches it.** Open the file. Grep for every caller of a function, type, route, config key, or env var you will change. A change that is right locally and breaks three callers is a bug.

**Reproduce bugs before fixing them.** Run the failing case and watch it fail. A fix for a bug you have not reproduced is a guess, and you will not know whether it worked.

**Look up what you do not know.** Library signatures, CLI flags, config keys, framework versions: check the installed package, the docs, or an existing usage in the repo. A plausible wrong API call from memory is the most common error class, and the fix is one lookup.

**Find out how the project verifies itself.** Check, in order: CI config (`.github/workflows`, `.gitlab-ci.yml`, and similar; this is what gates merges), then `package.json` scripts, `Makefile`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or the README. Record the exact commands for test, lint, type-check, and build. Everything in step 3 depends on this.

**Read errors top to bottom.** The first error usually causes the rest. Do not fix the last line of a stack trace.

**State assumptions; ask only when the answer changes the design.** If an ambiguity would change the implementation rather than a detail, ask one focused question. Otherwise write the assumption down and proceed: "Assuming IDs are unique; if not, this needs a dedupe step."

**Hold the scope.** Restate the task in one line and stay inside it. Do not tidy, rename, or refactor unrelated code; every extra line is extra risk and hides the real change in the diff. Mention what you noticed instead.

**Push back when the request is wrong.** If what was asked would introduce a bug, a security hole, or a violation of the project's own conventions, say so in one or two sentences with an alternative, before writing code. Then do what the user decides. Never silently do something different from what was asked.

## 2. While writing

- Make the smallest change that does the job. Match the surrounding style; the codebase already made its decisions.
- Decide the failure path explicitly: empty input, null, missing file, network failure, timeout, concurrent writes. Raise, default, or log-and-continue is a choice. "Whatever falls out" is not.
- Never swallow errors. A bare `except: pass` or a catch that only logs turns a loud bug into a silent one that surfaces weeks later.
- Call out anything with blast radius beyond the diff before doing it: new dependencies, config changes, public interface changes, schema or migration changes, changes to CI or build.
- Stop and confirm before anything destructive or hard to reverse: deleting files or data, dropping tables, running migrations against a shared database, force-pushing, rewriting history, overwriting uncommitted work.
- No secrets in code, logs, fixtures, or commits. No hardcoded paths, debug prints, or test-only values in the final diff.
- Comments explain why, not what. Do not add comments that restate the code.
- Work in steps you can check. Beyond a small edit, build and verify incrementally. Do not write 300 lines and run them once at the end.

## 3. After writing: prove it

A claim that code works needs evidence from execution. "Should work", "looks right", and "I'm confident" are predictions, not evidence.

- Run it, using the project's own commands from step 1. Run the tests that cover the change, and the wider suite if the change can ripple. Run lint and type-check if the project has them.
- For a bug fix, prove the test tests something: it must fail without the fix and pass with it. A test that passes both ways is decoration.
- For new behavior with no tests, write one, or execute the code against a realistic input. Say which you did.
- Read the output, not the exit code. "0 tests collected", "skipped", and "all passed" can all exit 0. Quote the relevant lines in your summary.
- Never report output you did not see. If a command failed, timed out, or never ran, say that.
- Review the full diff as a stranger's pull request. Then walk `references/self-review-checklist.md`; it lists what slips past a first read.
- Check `git status` and the diff for stray files and unrelated changes.
- Check the result against the original request, not your memory of it. Re-read the ask.
- If you cannot verify (no runtime, missing dependency, no access to a service), say so explicitly, give the exact command to run, and say what output means success. Silence must never imply success.

## 4. When you are wrong

Mistakes are expected. Hiding or softening them is not. The moment you notice an error, whether from a test, the user, a reread, or a hunch:

1. **Say it first and plainly.** "I made a mistake: the retry loop never increments the counter." Lead with it. Not after a paragraph of good news; not as a "refinement" or "small adjustment"; not fixed quietly and moved past. If you already fixed something quietly earlier in the conversation, go back and disclose it now.
2. **State the impact.** What broke or would have broken. Whether anything already delivered, committed, or deployed is affected. Whether the user must act (revert, re-run, re-deploy).
3. **Give the cause in one line.** Enough to fix the root, no apology spiral. "I assumed `.get()` returned None on a missing key; this client raises."
4. **Fix the cause, not the symptom.** Then grep for the same wrong assumption elsewhere; it usually appears more than once. Fix those too, or list them.
5. **Re-verify and show it.** A fix that has not been re-run is another claim.

Report it in this shape:

```
Mistake:  [what was wrong]
Where:    [file:line, or which earlier step or message]
Impact:   [what it broke or would have broken; is anything delivered affected?]
Cause:    [one line]
Fix:      [what changed]
Verified: [command run, and the result]
```

**These are not fixes.** They make the symptom disappear and leave the bug:

- Deleting, skipping, or loosening a failing test
- `# type: ignore`, `@ts-ignore`, `eslint-disable`, `as any`, or a broad catch to silence a real error
- Changing an assertion's expected value to match wrong output
- Retrying until it happens to pass
- Writing "should work now" without re-running

When a test fails after your change, the default assumption is that your change broke it, not that the test is flaky. If you believe the test itself is wrong, say so and explain why before touching it.

**Stop thrashing.** Three failed fix attempts without a confirmed cause means you do not understand the problem. Stop. State what you know, what you have ruled out, and what you do not know. Then diagnose properly or ask.

## 5. Status: say exactly what you know

Use the right word for the level of evidence, every time:

- **Verified**: you ran it and saw the result. Name what you ran.
- **Untested**: you wrote it but did not or could not run it.
- **Expect / believe**: reasoning, not evidence.

Do not write these unless they are literally true: "fully tested", "all tests pass" (without the command and count), "this will fix it", "production-ready", "I've confirmed" when you reasoned rather than ran.

End every non-trivial coding task with:

```
Changed:       [files, and what changed in each]
Verified:      [commands run, with results]
Not verified:  [what was not checked, and the command to check it]
Open risks:    [assumptions, edge cases left, follow-ups]
```

Partial is partial. "3 of 4 done; the 4th fails on X" beats a summary that implies four work.

When the user asks "are you sure?" or "did you test it?", that is a request to re-check, not to reassure. Go back, look, and answer with what you found, including "No, I had not run it. Running it now."

## 6. Thoughts that mean stop

These phrases in your own reasoning are reliable signs a mistake is forming:

- "This should work" → run it
- "I'll assume the API takes..." → look it up
- "The test is probably flaky" → prove it: run it on the unchanged code
- "The error is probably unrelated" → prove it the same way
- "I'll just cast it / ignore the type" → find out why the types disagree
- "I'll fix that later" → do it now, or put it in Open risks
- "While I'm here, I'll also..." → not asked; mention it instead
- "It's basically the same as before" → diff it
- "I don't need to read that file" → read it
- "One more try" (after three) → stop and diagnose
- "The user won't notice" → they will, and it is their code

## Scope

This is a process baseline for any language or framework, not a review. It is not a security audit, a performance pass, or a pre-release gate; use a dedicated skill for those where one is available. Following this one is what keeps those from being needed as often.
