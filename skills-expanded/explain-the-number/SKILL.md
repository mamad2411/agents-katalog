---
name: explain-the-number
description: Like-for-like before a measured number is reported or credited to a change. Use before saying a change moved a score, a count, a before/after delta, a benchmark time or speedup, a Lighthouse or Core Web Vitals result, an eval score, or an error, conversion or traffic rate. For whether the tests and gates passed, use `regression-proof`.
---

# Explain the number

A number credits a cause only when the comparison is **like-for-like** and nothing else that
changed between the runs explains it. Every number is held to this, the one that looks clean
included: a count taken over the same number of items carries the same suspects as the score
beside it. Credit and license: `LICENSE.md` in this folder.

1. **Diff the coverage before the result.** Set the two runs side by side on what they looked at:
   - the population: the actual set of pages, requests, users, test cases or files, not only
     the count, since two runs of 31 pages can be two different 31;
   - the measures: which checks, metrics or stages ran in each, and which were skipped;
   - the setup: tool and runtime versions, config, hardware or device profile, data or fixtures;
   - the world: deploys, content changes, traffic shifts and incidents in between.

   Each difference is a second explanation for the change.

2. **Rule out each explanation with evidence.** The usual suspects: a check or stage that did not
   run; items the newer run did not look at again (not looked at, so not fixed); items newly in
   scope (never seen before, so not new); a tool or dependency bump that moved a measure; cached,
   warmed-up or skipped work; one run of a noisy measure. A field that is missing from one run is
   unknown, not zero. Name the evidence that rules each suspect out, or keep it as a caveat.
3. **Name the limiter of a timing.** For a duration or speedup, say which stage bounds it (start-up,
   the network, I/O, one slow step). A total covers everything; a per-item time usually covers
   only part of the work. Credit a stage with a speedup only from that stage's own time.
4. **Match the measure's window and spread.** A rolling measure (Core Web Vitals field data is a
   28-day p75, weekly analytics a 7-day sum) has moved at most a fraction since last week's deploy.
   A benchmark or an eval needs several trials and their spread before a gap between two versions,
   prompts or models counts.
5. **Report coverage with the number.** Say what ran, what did not, and how many runs stand behind
   it. A measurement that did not run is reported as "did not run", never counted as clean. Full
   coverage is required to clear something, not to charge it: a problem that was reported has been
   looked at.

The step is done when every number you report has its coverage stated and each difference from
step 1 is either ruled out with evidence or written beside the number. When what is left is not
like-for-like, report what is, say what is not, and name the run that would settle it.
