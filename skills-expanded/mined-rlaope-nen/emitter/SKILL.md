---
name: emitter
description: Launch, positioning, and promotion — making finished work land with the audience that should care. Use when the user says "launch", "announce", "release notes", "changelog", "blog post", "tweet thread", "X thread", "Show HN", "Hacker News post", "how do I promote this", "who would care about this", or "positioning"; when a README needs a pitch instead of a manual; when something is built and working but nobody outside the repo knows it exists; or when launch copy already exists but reads like a feature list.
---

## Stance

放出系 Emission is the art of projecting aura beyond the body — power that never leaves your skin touches nothing. Code obeys the same physics. A tool that works flawlessly on your machine and is known to no one has, from the world's point of view, not been built. Projection is not the reward for finishing the work; it is a second discipline with its own craft, and engineers who treat it as an afterthought produce launches that read like commit logs.

Without this discipline, good work dies quietly. The announcement lists features instead of naming the reader's pain, the one person who would have loved it never sees it, and six months later someone else ships a worse version with a better sentence and takes the audience. The words are not decoration on the work. For everyone who wasn't in the room, the words are the work.

## Boundaries

If the ask has become "break this launch into workstreams, sequence the campaign, coordinate who does what by when" — stop. Decomposition and planning are manipulator's job. Emitter finds the impact point and writes the words that hit it; the moment the problem is orchestration rather than framing, hand it over and take back only the copy tasks that come out the other side.

If you catch yourself writing "just run this" about a demo path you have not verified under load — stop and check whether the thing is actually reliable enough to announce. A launch is a denial-of-service attack you schedule against yourself: cold starts, rate limits, the error page a thousand strangers will screenshot. Enumerating and hardening those failure modes is conjurer's territory. "Ready to announce" is your call; "won't fall over when the announcement works" is theirs, and theirs comes first.

## Method

1. **Name the audience and the single before→after they feel.** Not a demographic — a person mid-task. Write the sentence: "Before: they do X and it costs them Y. After: they run this and Z." If you cannot write it concretely, the problem is not the copy; you don't yet know what the work is for, and no amount of wordsmithing fixes that.

2. **Draft three competing angles, in full.** Typically: the pain angle, the mechanism angle, the result angle — but draft real opening lines, not labels. "Pain angle" is a category; a headline plus first sentence is a thing you can judge. Angles only become comparable once they exist as text, and the second-best angle usually reveals itself by being written.

3. **Pick one and cut the rest.** The whole piece carries one angle. The rejected two may survive as a single paragraph in a comment or a footnote in the README — never as coequal sections. A post that hedges across three angles has none; the reader you're aiming at bounces off the paragraph aimed at someone else.

4. **Format for the specific channel, from scratch.** Hacker News wants a plain declarative title and a first-person top comment with the backstory; a changelog wants what changed and what the reader must do about it; a thread wants one idea per post with the strongest first. These are different documents that happen to share facts. Rewrite for each; pasting is visible and readers punish it.

5. **Back every claim with a number or a demo, and delete what you can't back.** Every superlative gets a measurement in the same sentence or gets cut. This applies at draft time, not publish time: a number with no artifact behind it yet does not enter the draft with a verify-later note — produce the artifact as part of the writing, or cut the number. "Verify before publish" is deferred fabrication. And the piece must contain a try-it path that goes from reading to running in under a minute — no signup, no build step, no API key. If the fastest honest demo takes five minutes, ship a bundled sample that takes thirty seconds and say so.

6. **Rehearse the landing cold.** On a machine without your dev environment, copy-paste every command the copy instructs the reader to run — verbatim, not a variant — and time each one. The commands in the post are the commands a thousand people will run exactly as written; a typo there costs more than a typo anywhere else in the project.

7. **Publish, then hold the thread with the same evidence standard.** The first hour tells you which claim readers attack and which they repeat. Answer objections with the number or the demo, not with adjectives — the comments are part of the copy now.

Maintenance channels — release notes, changelogs, migration guides — are not launches, and they do not carry the full launch kit. What survives unchanged: name the reader and what they must do (step 1, where before→after becomes upgrade→outcome), channel-native formatting (step 4), the evidence rule (step 5), and a cold rehearsal of any command the copy tells the reader to run (step 6). What is waived: competing angles (steps 2–3) and objection thread-holding (step 7). Say which mode you are in — a changelog dressed as a launch post is as broken as the reverse.

## Worked trace

The work: `flakehunt`, a small CLI that reruns a test suite with shuffled ordering and varied RNG seeds, then ranks tests by conditional failure rate. Extracted from an internal tool, now on PyPI. Target channel: Show HN.

Step 1, the before→after: *Before: a developer clicks "re-run jobs" for the third time today and knows something is flaky, but finding which test costs an afternoon of bisecting. After: one command, ten minutes, a ranked list of suspects with a probable cause each.*

Step 2, three angles drafted as real headlines with openers:

```
A (pain):      Show HN: Flakehunt – find which test is flaky instead of rerunning CI
               "Every click of 're-run jobs' is a search you can't refine..."
B (mechanism): Show HN: Flakehunt – catches flaky tests by permuting order and seeds
               "Most flakes are order-dependent: a test passes alone and fails
                after some neighbor mutates shared state..."
C (result):    Show HN: Flakehunt – it pinned 11 flaky tests in our 4,100-test suite
               "Our suite failed roughly one run in six. Nine minutes of
                flakehunt later we had all eleven culprits..."
```

Step 3, pick A. HN rewards recognized pain; B leads with the how, which matters only after someone cares; C's number is strong but contextless as a headline. So C's number becomes the second sentence of A's body, and B's mechanism becomes one paragraph in the author comment. Two angles cut, both salvaged as support.

Steps 4 and 5, the channel-formatted copy with every claim backed:

```
Title: Show HN: Flakehunt – find which test is flaky instead of rerunning CI

Author comment:
I got tired of clicking "re-run jobs" and hoping. Flakehunt reruns your
suite N times with shuffled test order and fresh RNG seeds, then ranks
tests by conditional failure rate. Last month it pinned 11 flakes in our
4,100-test Django suite in 9 minutes — 9 order-dependent, 2 time-sensitive.

Try it in under a minute (no install, bundled demo suite):

    uvx flakehunt demo

Real usage: uvx flakehunt "pytest -q" -n 20
How it works: order permutation isolates state leaks between tests;
seed variation isolates randomness in the tests themselves. The ranking
is just failure count conditioned on what ran before.
```

Note what step 5 already killed: an early draft said "dramatically faster than bisecting by hand" — deleted, replaced by the 9-minute figure, which is a fact from a log instead of an adjective. Step 6, rehearsal on a clean laptop:

```
$ time uvx flakehunt demo
flakehunt: running bundled suite (14 tests) x 25 with order+seed variation
RANK  TEST                 FAILS   VERDICT
1     test_cache_expiry    9/25    order-dependent (fails after test_warm_cache)
2     test_retry_jitter    4/25    seed-sensitive
real    0m38.2s
```

38 seconds, no dev environment — the under-a-minute claim in the post is now a measurement, not a hope. At publish, the predictable first comment arrives ("how is this different from pytest-randomly?") and gets the discriminating answer — randomization finds flakes by accident, ranking attributes them on purpose — with the 11-in-9-minutes number attached, per step 7.

## Anti-patterns

- **Launch copy that is a feature list.** A bulleted enumeration of capabilities with no before→after anywhere in the draft — the reader is handed an inventory and asked to do the positioning themselves.
- **A superlative with no measurement beside it.** "Blazingly fast", "dramatically simpler", "massive improvement" — grep the draft for adjectives of scale; each one either has a number in the same sentence or is a defect.
- **Identical text pasted across channels.** The HN post, the tweet, and the changelog diff to zero. Each channel's readers can tell they got someone else's document, and each channel's norms are violated by the other two.
- **A launch post with no way to try the thing in under a minute.** The only path in is clone, install toolchain, configure, sign up for a key. Every added minute sheds the majority of remaining readers; the transcript of a cold-machine attempt tells you the real number.
- **Three angles in one post.** The headline promises pain relief, paragraph one pivots to architecture, paragraph two to benchmarks. Visible in the draft as topic sentences that don't share a subject.
- **A number in the copy that no artifact backs.** "9 minutes" appears in the post but in no log, benchmark, or transcript anywhere in the repo or session. Unbacked numbers are the first thing a hostile commenter checks and the fastest way to lose the thread.

## Done means

- The before→after sentence written down, naming a specific reader mid-task — the sentence the whole piece is a delivery vehicle for.
- Three drafted angles on record, one chosen with a stated reason, two visibly cut (and at most salvaged as a paragraph of support). *Launch pieces only — waived for maintenance channels, and the output says which mode it ran in.*
- Final copy per channel, each formatted to that channel's norms; no two channels share paragraphs.
- Every quantitative claim in the copy traceable to a command output, log, or benchmark artifact that exists.
- A demo path timed under 60 seconds on a machine without the dev environment, transcript kept.
- The piece published — or ready, with the top three predictable objections listed and an evidence-backed answer prepared for each, every answer cross-checked against the artifacts already in the piece so no reply contradicts the copy it defends. Copy that never ships is aura that never left the body.
