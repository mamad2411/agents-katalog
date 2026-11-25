---
name: reproducing-bug
description: Use when a reported bug needs to be proven before anyone fixes it — a symptom seen in a customer or cloud environment, a report with no confirmed cause, an issue closed once as "not reproducible", a fix whose acceptance criteria were ticked without tests, or any bug that must end in a failing test rather than a write-up
argument-hint: "[issue-id-or-description]"
---

# Reproducing a Bug

## Overview

A bug report is one person's observation. It is not yet something anyone can fix.

This skill turns that observation into two things: a run that fails on demand, and a
**test that fails while the bug is alive and turns green when it is fixed**.

**The job ends at the test, not at the report.** Reproducing proves the bug is real.
Only the test stops it coming back.

Two rules carry most of the weight:

- **Drive the product, do not read the source.** Reading gives you a guess. A run that fails in front of you gives you a fact.
- **Prove the test both ways.** A test you never saw pass is not a test.

## When to use

- A report names a symptom but no confirmed cause.
- The bug was seen somewhere you cannot debug directly — a customer cloud, a managed cluster, someone else's machine.
- An earlier attempt closed it as "not reproducible".
- A fix has landed and you want to know whether it holds when things are real.
- Acceptance criteria were ticked with no test behind them.

**Do not use** when the issue already has a confirmed cause and a failing test, or when a plain unit test can express the whole thing.

## What this skill is not

- **Not a root-cause analysis.** You name the mechanism you saw. The fix decision belongs to whoever owns the issue.
- **Not the fix.** Do not write one, even when it looks obvious.
- **Not finished at the report.** That is the halfway point.

## Input

Any of: an issue id, an issue link, or a pasted symptom with no ticket at all.

From the issue, take — do not guess:

- **The symptom and the steps**, if given.
- **The environment and version** it was seen in, and whether you can reach it.
- **The docs it names.** Read those sections, not whole files.
- **The comments.** An earlier attempt may say why it was closed.
- **The acceptance criteria.** Any criterion ticked with no test is a gap you must probe,
  whether or not anyone asked you to.

## Stage 1 — prove the bug is real

### Preflight, then stop

Work out what state the product must be in for the scenario to be reachable. Check every precondition **by using the real path**, not by reading config — something that looks healthy can still fail when used.

- Check them **all** before reporting. One complete list, not one blocker at a time.
- Fix whatever you can yourself. Only truly human things go on the list: a sign-in, a consent screen, a credential only they can grant, a paid quota.
- Then **stop and wait**. Do not start, do not write the script, and do not offer a read-from-source cause as a consolation prize.

**Preconditions rot.** Something that passed at preflight can be false minutes later — the product may undo it, a token may expire, a job may reset it. Re-check anything fragile right before the step that needs it, and retry when it has decayed. Something that keeps flipping back is itself a finding.

### Drive it like a person

- **Everything through the interface, setup included.** Real clicks, real typing, real waiting for the screen to settle. Creating the records, sending the messages, retrying a failed step — all of it clicked.
- **Never call the API to get somewhere.** No request helpers, no console fetch, no database write, no seeding script. The path you skip may be where the bug lives, and a state reached by API is not the state a user would be in. Read-only calls for watching are fine.
- **Find the control.** If a button is hard to locate, read its component for the label or test id. "I could not find it so I called the endpoint" is not acceptable.
- **Use a browser that is already signed in.** A fresh profile lands on a login screen. If you reach one, the connection was wrong — fix that, do not log in.

### Watch everything at once

Line these up by time:

1. **Browser console** — every level, with source location and full stacks.
2. **Network** — request, response, status, timing, and bodies for the calls that matter.
3. **Application logs**.
4. **Container logs**, for anything the scenario starts.
5. **Central logs** — query the API directly.

**Check the log shape before you trust a query.** Ask the log store what fields a stream really carries. A documented field name is a guess: an id that is a label will not match a text search, and `camelCase` and `snake_case` versions of the same field often both exist.
Trusting a documented query is how people wrongly conclude there are no logs at all.

**Central logs should be enough on their own.** Write down anything you needed that was not there. Those gaps matter as much as the bug.

### Look at what already happened

You are replacing the engineer who checks everything before saying anything. That person starts with the past.

- **Query the original incident window** — its date, time, environment. The symptom was already caught once, and those logs often say more than a clean local run.
- **Read what the ticket carries** — captures, log bundles, recordings, comments.
- **Look for earlier times it happened.** Widen the range. Does it track a release, a version, one customer? "Every time" and "once" are different bugs.
- **Compare that environment with yours.** A mismatch is a finding — often the reason an earlier attempt failed to reproduce.

### Any environment

Local, containers, a shared cluster, a customer cloud — only the log endpoint and the sign-in change, never the method. Prefer the cheapest place that still shows the symptom.
Never say a bug is absent from an environment you could not watch properly, and always say where each observation came from.

### Evidence

- **A trace is better than a video.** It gives a frame-by-frame filmstrip with the network and console lined up against each frame, so a reader can stop on the exact moment.
- **Do not run a screen recorder.** It asks for a system permission and the trace already covers it.
- **Use a large window and set the viewport.** Frames are captured at viewport size; a small window makes the filmstrip useless.

### The Stage 1 report

Print it in the session. Saving a file and giving the path is not delivering it.

**Start with a verdict box. Five lines, no more.** A reader must get the whole answer without scrolling:

```
Verdict:  <one line — is it broken, and how badly>
Impact:   <who feels it and when>
Cause:    <the one thing that is wrong>
Next:     <the single next action>
Proof:    <one command or link>
```

Say the size of the problem honestly. "Broken" and "partly broken" are different verdicts — a fix that works in one case and fails in another is **partly** fixed, and calling it broken is as wrong as calling it fixed.

Then the detail, in this order:

1. **What was driven** — the steps, as a user would say them.
2. **What was seen** — the symptom, and the moment it showed.
3. **Mechanism** — the chain at file:line. Mark each link **confirmed** (you saw it) or **guessed** (read from source). Never present a guessed chain as the cause.
4. **Evidence** — every item a command to run or a link to click.
5. **Log gaps** — what was missing, or logged so that two different causes look the same.

**Keep it readable or it will not be read.**

- **Plain, everyday words.** Write "covers the chat", not "fronts the live conversation".
  Write "second reason", not "an additive cause". If a word would slow a tired reader down,
  use the common one.
- **Short sentences. One idea each.**
- **Aim for one screen per section.** Long tables, full logs, and raw output go in files and get linked. A report nobody finishes has failed, however correct it is.
- **Say how many runs you did and why, in one line.** Do not make the reader count them.
- **No hedging and no padding.** If something is unknown, say "unknown". If a result is weak, say which part is weak.

Then keep going. Do not ask whether to continue.

## Stage 2 — turn it into a test

### Find the smallest scenario

Strip the run down. What was load-bearing, what was decoration? A bug that needed two records and two live sessions may need only one selection repeated. This decides how cheap the lasting test can be.

### Map it to existing coverage

Find the acceptance-criteria and test-case ids the scenario touches. Then say which it is:

- **uncovered** behaviour under a criterion that exists,
- a criterion **covered but asserting the wrong thing**,
- or behaviour with **no criterion at all**.

Never invent an id. If none fits, say so — creating one belongs to whoever owns the spec.

### Pick the lane that can run the trigger

Work out **where the trigger lives**, then pick the cheapest lane that can execute it. Read the project's own lane rules; do not guess from this table.

| Trigger lives in | Lane |
| --- | --- |
| Logic in one server function or service | Unit (backend) |
| Client code — a handler, effect, hook, render decision | Unit (frontend) |
| A multi-step outcome across real backend calls | Flow (API level, fakes outside) |
| The same, but only with a real agent runtime | Flow, real-agent variant |
| The assembled screen — timing, focus, several panes | Journey, mocked |
| A whole screen driving a real agent end to end | Journey, real runtime |
| Image start-up, routing, sign-on, log wiring | Container |
| A fake's own behaviour | Fake/twin unit |
| A shape or invariant guard, no app start | Structural |

An API-level test cannot run a click that decides to call an endpoint. If the API cannot reach the trigger, **say so plainly** and say what an API test would and would not catch.

**Check whether the server is actually wrong** before choosing an API-level lane. If it behaves as designed, a test there asserts intended behaviour and proves nothing.

**If the bug is user-visible, cover it in a browser too.** A call-count unit test asserts the shape of a call, not what a person sees. Do not turn down the browser test because it costs more — turn it down only if you can say why the outcome is already covered.

**Prefer mocked lanes.** Move up to a real runtime only when the bug needs something a mock cannot make: real timing, a real container lifecycle, a real status change, a real credential. Say which. "More realistic" is not a reason — real lanes are slow and flaky, so they must earn their place.

**Do not invent a lane.** If nothing fits, say so.

### Check the fake can carry it

Ask whether the existing fake or twin can produce the root cause as it stands. Often it cannot — a missing error code, an absent status, a state it never models. Extending it is part of the work, not a blocker. Say exactly what you extended and why.

### Write the test

- Use the project's test-writing skill.
- **Assert what the user sees**, not internals, so a refactor that keeps the behaviour keeps the test.
- **Assert the CORRECT behaviour**, so it fails now and passes once fixed. Never write a test that locks in the broken behaviour.
- **Tie every assertion to something you saw** — a request in your timeline, a log line, a screenshot, a trace frame. An assertion you cannot tie to evidence is invented, and inventing one is the exact failure this whole cycle exists to prevent.
- **Mock at the outermost edge, not the thing you are testing.** Mock the network call.
  Never mock the hook, service, or function whose behaviour is the subject — its real success and error paths then never run, so the test cannot see what it claims to check.
- **Choose and say why.** State the pick in one line with the reason and keep going. The user can redirect you; a paused session helps nobody.

### Prove the test both ways

A test marked "expected to fail" passes on **any** error — a broken mock, a missing field,
a render loop. So it can sit green forever on a lie.

1. **Show the real failure with the marker removed.** It must be an assertion failure, not a crash.
2. **Add a canary** in the same file that is not marked expected-to-fail and passes both before and after the fix. A broken harness then turns the canary red instead of hiding.
3. **Simulate the fix and watch it flip.** Force the fixed condition on, or stub it, and check the test passes — then undo it. Without this you never learn whether the test can pass at all.
4. **Read it like an enemy.** Would it still fail if the bug were fixed a different way?
   Would it pass if the bug got worse?

### Existing tests

If a test already asserts the broken behaviour, name it — path and line — and say it **may need updating**. Stop there. Do not say the fix must change it: fixes often work further upstream and never reach that code.

### Decide by confidence

- **High** — draft the issue: symptom, mechanism, and the failing test named, so fixing it turns the test green. That is what "done" means for the fix.
- **Low** — draft a spike instead: which paths need digging into, what would raise confidence. Do not force a test you cannot defend.

Present it. **Do not file it** — that is the user's call.

### The Stage 2 report

Add these to the same report and print them too. This part is the real output. Same rules:
plain words, short sections, long output in linked files. Update the verdict box at the top if Stage 2 changed the answer.

6. **Root cause and smallest scenario**
7. **Coverage mapping** — ids touched, and which of the three cases
8. **Lane** — chosen, why, and what a cheaper lane would miss
9. **Fake** — can it carry the cause, and what you extended
10. **The test** — path, what it asserts, the real failure output, the canary, the flip
11. **Assertion-to-evidence map**
12. **Existing tests asserting the broken behaviour** — "may need updating"
13. **Confidence**, and why
14. **The drafted issue or spike** — ready to paste, not filed

### Close the loop

When the real fix lands, run the test again. An expected-to-fail test that starts passing turns red — that is the signal to remove the marker. Check the canary still passes so the red is real.

Then compare: which links of your mechanism were right, which were wrong, and does the lane they tested in match the one you picked. Report what you got wrong. Being wrong in the open is the point.

### What you may and may not land

- **May write:** the failing test, any fake extension it needs, throwaway scripts.
- **May not:** commit, push, or open a pull request. Leave it in the tree, show the diff,
  stop.
- **One pull request per concern.** The failing test is one. A fix for something you tripped over on the way is another, with its own issue. Never combine them.
- **Keep throwaway scripts out of the repository** — they live with the trace in a scratch directory, never at the repo root, or they end up in someone's commit.
- **Never change product code here.** If the fix looks obvious, say so in the draft issue.

## A blocker that is itself a bug

If the thing stopping you looks like a bug and not missing setup — a control that does nothing, a state the product cannot recover from, an error that names the wrong cause — say so: what you were doing, what happened, and why it is separate from the bug you came for.

Tell the user, take the manual unblock, and put it in the report under its own heading. Do not quietly work around it, do not let it become the main finding, and do not file a ticket for it.

**Stay on the reported bug.** Side findings get named and handed over. They do not get investigated, fixed, or turned into their own job here. If one blocks you, make the smallest change that unblocks the run, say exactly what you changed, and carry on.

## Environment traps

Each of these looked like a product bug and was not:

- **A browser may refuse remote control on its default profile.** It needs its own profile directory. A copied profile also loses the session on restart, so keep one dedicated signed-in browser instead of copying each run.
- **Never close a browser you connected to.** It kills the user's window and their session.
  Close only pages you opened.
- **A connected browser keeps the script alive forever.** The connection is an open handle,
  so the process never ends by itself. Exit on purpose.
- **Opening a new page can hang in headless over a remote connection.** Reuse the open page.
- **A deep link to a record may be overridden** by whatever the app remembers as selected.
  If a URL does not take you where you expect, drive the picker — and note it, because it will mislead anyone sharing links.
- **Piping a command into `tail` hides its exit code.** You read a passing tail and think it passed. Capture the exit code separately.
- **A script outside the repository cannot resolve plain imports** — module lookup starts at the script's own folder. Run it with the repo's toolchain.
- **A non-default system locale can fail local checks** that pass on the main branch.
  Suspect the environment before the code.
- **A command run in a restricted shell can print nothing at all** and look like it never started. Run those without the restriction.

## Red flags — stop and go drive the product

- Writing a cause chain before a single click has landed
- "Root cause found, no reproduction needed"
- "I could not find the button, so I called the endpoint"
- Asking the user to click something you never tried to script
- Reporting one blocker and stopping instead of checking the rest
- Presenting a source-read chain without marking it a guess
- Handing over a file path instead of the report
- A report with no verdict at the top, or a verdict you must scroll to find
- Calling a partly working fix "broken", or a partly broken one "fixed"
- Naming a browser test as needed, then not writing it
- Stopping at the report, as if reproducing were the job
- Marking a test expected-to-fail without showing the real failure
- Mocking the very thing the test is meant to check
- Saying "the fix must change this existing test"
- Turning down a browser test only because it costs more

## Rationalizations

| Excuse | Reality |
|--------|---------|
| "The code clearly shows the cause, a run adds nothing" | It shows a likely cause. Products fail for reasons the source does not predict. Not reproduced means not confirmed. |
| "Seeding through the API is the same and faster" | The skipped path is a place the bug could live. Not the same. |
| "I could not find the control" | Read its component for the label or test id. |
| "This step needs a person" | Only if the product cannot be driven to it. Slow and fiddly is your job. |
| "They are blocked anyway, so a source-read write-up beats nothing" | It is worse than nothing if wrong, because it will be treated as the answer. Report the blocker and wait. |
| "There are no logs for this" | Check the query shape against the real field names first. Usually the filter was wrong. |
| "I will mention the log gaps informally" | They are a required section, and half the value. |
| "Reproduced, so I am done" | Reproducing prevents nothing. The job ends at a test. |
| "It fails, so the test works" | Expected-to-fail passes on any error. Show the assertion, add a canary, prove the flip. |
| "Mocking the hook is simpler" | Then its real paths never run and the test cannot see what it claims to check. |
| "A call-count unit test is enough" | That checks the shape of a call, not what the user sees. |
| "This old test obviously has to change" | Fixes often work upstream and never reach it. Say it may need updating. |
| "The criteria are all ticked, so it is covered" | Ticked is not tested. Probe every criterion with no test behind it. |
| "It is all in the report" | If it takes 500 lines to find, it is not delivered. Verdict at the top, detail in files. |
| "The precise wording is more accurate" | A reader who gives up learns nothing. Common words, short sentences. |
| "I noted that a browser test is needed" | Naming a gap is not covering it. If you named it, write it. |

## Done when

- [ ] Reproduced on demand, with evidence
- [ ] Mechanism named, each link marked confirmed or guessed
- [ ] Smallest scenario that still shows it
- [ ] Coverage ids mapped, none invented
- [ ] Lane chosen and defended
- [ ] Fake checked, extended if needed
- [ ] Test written, expected-to-fail, real failure output shown
- [ ] Canary added, passing both ways
- [ ] Flip proved against a simulated fix
- [ ] Mocks at the network edge, not on the subject
- [ ] Every assertion tied to evidence
- [ ] Tests asserting the broken behaviour named as "may need updating"
- [ ] Log gaps listed
- [ ] Confidence stated; issue or spike drafted, not filed
- [ ] Tree clean apart from the test and fake changes

Say which of these are missing rather than implying it is all done.
