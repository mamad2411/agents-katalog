---
name: debugging-by-evidence
description: >-
  Find the cause of a failure and prove it before any fix. No hypothesis before a
  command that already reproduces the symptom. Covers building a signal that
  reproduces, ranking rival explanations with what would falsify each, probing
  without fixing, putting the regression test where the bug actually occurs, and
  reporting the causal chain at file:line. Use when the user says "this is
  broken", "why is this failing", "tests fail after my change", "it only breaks
  sometimes", or reports something throwing, hanging, or newly slow. Not for
  judging a change that already exists, or for an error whose message already
  names the file, line, and cause.
---

# Debugging by Evidence

**Core principle.** The loop is the skill. Everything after it is mechanical.

- **Without a loop the cause stays hidden.** No amount of reading the code will find it.
- **The weight sits in the loop and in the five states.** Every rule below either sharpens the loop or spends it.
- **You opened this in the middle of something.** This is how to do that work, not a replacement for it. Name what you were doing before you start, and return to it when this is done.

## No hypothesis before a command that reproduces it
- **The command MUST already have been run.** A command you wrote down and never ran is not a loop.
- **Its output MUST show the symptom the user reported.** A different red line is a different bug.
- **Reading code produces theories nothing can falsify.** A theory that cannot fail will survive every test you put it through.
- **The loop is that command plus the state it needs.** Record both.

## What you may write, and when
- **Until `EXPLAINED` the only write you MAY make is instrumentation.** Every inserted line carries a unique tag, so removal is one search. A fix written earlier destroys the red signal that was going to explain it.
- **Reverting your own change to re-observe the original failure is allowed here.** It is often the point. This skill runs experiments.
- **The licence stops at the workspace boundary.** No commit. No branch move. No remote or deployment action. Every tag comes out before you close.

## Establish before the first run
- **Never ask what the environment answers.** Three things settle the setup, and the environment already holds two of them.
  - The symptom in the user's own words, quoted.
  - The command the project already declares for running that surface.
  - Whether the failure is reported as constant or occasional, with a rate where it is occasional.
- **A symptom you restated in your own words is already a hypothesis.** Keep the original beside it.

## Which rules to read
**One rule per row.** Match the left column against the symptom or the state you are in.

- **The match sets where to start.** The loop state sets what you are allowed to do next. Enter at the matched row, then follow the loop states in order.
- **A rule belonging to a state you have not reached is read when you reach it.** Not now. Stopping applies from any state and outranks continuing.
- **Where two rows both look like the symptom, read both.** Under-reading costs a whole loop. Over-reading costs one file.

| If you see... | Read |
| --- | --- |
| **nothing you have run yet shows the symptom**, or the loop is slow, noisy, or fails only some of the time | `rules/runnable-signal.md` |
| a **red loop that drags in far more than the bug**: many files, a long sequence, a whole suite | `rules/minimising.md` |
| **one explanation already feels obvious**, or you are about to test the first thing that came to mind | `rules/rival-hypotheses.md` |
| you are about to **add a log line, a breakpoint, or a temporary edit** to see what happens | `rules/probing.md` |
| the failure **surfaces far from where it starts**: a bad value arriving from layers away, already wrong when it lands | `rules/fix-at-the-source.md` |
| **the cause is explained** and a test must now hold it down | `rules/regression-seam.md` |
| a **third fix attempt just exposed a fourth problem**, or the next step needs an observation you cannot make | `rules/stopping-and-escalating.md` |

**Discriminators.**

- **Signal against minimising.** Signal owns a loop that does not reproduce or cannot be trusted. Minimising owns a loop that reproduces but proves too much.
- **Hypotheses against probing.** Ranking comes before any run. A probe tests exactly one ranked prediction.
- **Source against seam.** Source decides where the fix belongs. Seam decides where its test belongs. Both wait for `EXPLAINED`.

**Default stance.**

- **Get a command to reproduce it before explaining anything.**
- **Name the state you are in**, and take only what that state licenses.
- **Never assert a cause no run has supported.** An untested explanation is labelled as one.

## Say which loop state you are in
**Report it every time.** Each state licenses only what it names.

| State | Means | Licenses |
| --- | --- | --- |
| `NO-SIGNAL` | nothing run yet reproduces it | more attempts at a loop, nothing else |
| `RED` | a command reproduces the symptom, deterministically or at a stated rate | hypotheses, probes |
| `MINIMISED` | removing any remaining element makes it pass | naming a cause |
| `EXPLAINED` | one surviving hypothesis, each link observed | a fix |
| `RESOLVED` | the original loop passes unmodified, and the nearest path the fix also touches was run | closing |

- **Skipping a state is the failure this skill exists to prevent.** You MAY spend as long as you need inside one state.
- **You SHOULD stop building a loop after five attempts** and report `NO-SIGNAL` instead. Keep going only where you can name what the sixth attempt does differently.
- **`NO-SIGNAL` for long enough is itself the report.** Say what you tried and what would produce a signal. Never proceed on theory.
- **Know what an empty result means before you trust it.** A zero is evidence of absence only from a path that records this event. A path that records nothing, or records only failures, produces the same zero and proves nothing.

## What makes a cause a cause
**All four hold, or it is a hypothesis and is labelled one.**

- **A run at `RED` or better produced it.** Not a reading of the code.
- **Each link from trigger to symptom cites an exact `file:line`.**
- **One prediction it made was tested and could have failed.**
- **It explains the whole symptom.** That includes the part that seems incidental.

**Three words carry their usual weight.**

- **Confirmed.** A probe result you observed.
- **Inference.** A hypothesis nothing has tested yet.
- **Gap.** An observation you could not reach. Name what would close it.
- **Say what the evidence does not establish.** A cause that explains the failure and nothing about its timing has one link missing, not zero.

## When to stop instead of trying again
- **Three attempted fixes that each reveal a new problem elsewhere are not a fourth attempt.** They are the finding.
- **The shape is wrong.** The report says so, and those three attempts are its evidence.
- **One thing you cannot observe stops the run the same way.** Name it. Name the observation that would settle it. Then stop, because debugging around an unknown produces a fix nobody can defend.

## Output contract

```
Symptom      as reported, in the user's words, and the loop that shows it
Loop state   one of the five, plus the reproduction rate where it is not 1
Ruled out    each rejected hypothesis with the observation that killed it
Cause        one line per causal link, each at file:line
Not shown    what this evidence leaves open
Fix          the change, and the seam the regression test sits in
Proof        the original loop re-run unmodified, the nearest adjacent path
             also run, and every probe tag removed
```

- **Report what you observed, not what you avoided.**
- **Never open with "fixed".** The reader needs the chain first. A fix stated before its cause reads as a guess that happened to work, and sometimes it is one.

## Do not skip this when
- **The cause seems obvious.** That is the anchor this skill exists to break.
- **Someone already told you what is broken.** That is a hypothesis, not a signal.
- **The fix is one line.** A one-line fix to the wrong line is still wrong.
- **You are in a hurry.** Guessing is what produces the second and third attempt.

## Routing
- **The table above selects the rule and its order.** Read a selected rule in full, interpret it yourself, and say which one you opened in one line.
- **Rival explanations MAY be tested in parallel.** Ranking them and judging what a result means is not delegated.
- **A direct instruction from the user outranks anything here.**
- **Once a fix exists it stops being a symptom and becomes a change.** Hand it to a review of the diff rather than judging it here.
