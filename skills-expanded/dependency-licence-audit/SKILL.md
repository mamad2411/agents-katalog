---
name: dependency-licence-audit
description: "Use when a dependency licence may block publishing or selling, or a component swap needs pricing."
version: 1.1.0
author: coordinator role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [licence, open-source, dependencies, publishing, swap-cost, models]
---

# Dependency licence audit

For answering "can I publish this / sell this, and what is blocking me" — and
the question that always follows: "what does it cost to swap the offending
component out?" Also covers weighing a swap to a more permissive component.

The owner builds tools they intend to open-source. They are not a lawyer and
neither are you: the job is to establish **facts about which artifact carries
which licence** and **what a swap actually costs in code and data**, then give
them options.

## Always-on rules

- **Verify a licence by reading the licence file, never a search snippet or a
  vendor page.** Vendors who sell commercial licences write marketing copy that
  is ambiguous on purpose.
- **Never promise "the same quality" from a replacement.** Headline benchmarks
  are saturated and say nothing about the user's own data. Promise a
  measurement instead, against the project's own evaluation set.
- **Say plainly when an option is paid or cloud-hosted.** It is the last resort,
  not a peer option — local and FOSS is the default.
- **Separate what you ran and saw from what you believe.** "I read the LICENSE
  file" and "I expect this model is weaker" are different claims and must not be
  delivered in the same voice.

## Procedure

### 1. Name the artifacts separately

One project ships several things under several licences. Enumerate before
concluding anything:

| artifact | typical licence | who it binds |
|---|---|---|
| library / source code | permissive (MIT, Apache-2.0) | you, the redistributor |
| pretrained weights or models | often **non-commercial research only** | the end user's use |
| training data | usually not redistributable at all | whoever retrains |
| docs and assets | frequently unstated | you |
| the rendering engine / runtime a tool drives | sometimes **source-available**, free below a headcount | your organisation's size |

"Project X is MIT" is almost never the whole answer. Name which of these rows
your project actually touches.

**Source-available is not open source, and the trigger is usually headcount, not
usage.** Such licences publish the code, permit commercial use, and start
charging above a team-size threshold — so "is this free?" has no answer until
you know how many people are in the org. Quote the threshold and the per-seat
price, say explicitly that it is source-available rather than OSS, and only then
give the yes/no for this user. Calling it "free" or "paid" without the threshold
is wrong in both directions.

### 2. Read the real licence text

```bash
curl -sL --max-time 25 "https://raw.githubusercontent.com/<org>/<repo>/main/LICENSE" | head -20
```

The first 20 lines identify the licence family, which is what you need. Do the
same for each sub-component: in a model zoo, **two models in the same pipeline
can carry different licences** and must be checked as two separate files.

### 3. Decide whether it blocks what the user thinks it blocks

The highest-value step, and the one most often wrong in a project's own notes.

**Separate what the repository SHIPS from what the user downloads at runtime.**
If restrictive weights are fetched on first run by the end user, and no weight
file is committed, then publishing the permissively-licensed source is not
restricted at all — the restriction lands on the *user's commercial use*. A plan
that says "the model licence blocks publishing" is then wrong by exactly one
step, and correcting it can unblock a release for free.

Check the repo's ignore rules and tracked-file list to prove which side the
artifact sits on, rather than assuming from the dependency list.

### 4. Measure coupling before accepting "it's foundational"

Users describe a core component as the engine and assume swapping it rewrites
the architecture. Measure instead of agreeing:

```bash
rg -n "import <module>|from .<module>|<vendor_pkg>" src/ tests/
```

For each consumer ask whether it touches the component's **output shape** or
only passes it through. A well-isolated component is a swap of one module plus a
couple of constants; consumers that never see the raw output do not move at all.
Report the real file count. If the module genuinely is threaded through
everything, say that too — the point is to measure, not to reassure.

### 5. Price the persisted data, not just the code

**When the component produces data that was written to disk, the data is the
real cost of the swap.** Embeddings, indexes, caches and fingerprints from the
old component are meaningless to the new one: that is a storage-schema bump plus
a re-ingest the user must run and wait for. State it explicitly — it is the cost
nobody sees coming, and it is usually larger than the code change.

### 6. Check whether the replacement is already installed

Before proposing a replacement as an addition, test whether an existing
dependency already provides it:

```bash
.venv/Scripts/python.exe -c "import <pkg>; print(hasattr(<pkg>, '<Feature>'))"
```

A swap that **removes** dependencies is a far stronger recommendation than one
that adds them, and it flips the framing from "more machinery" to "less". Run
the check before writing the recommendation, not after.

### 7. Present options, then commit to one

When the owner asks for alternatives, they still want a recommendation, not a
menu. The shape that works:

- **Lead by correcting the premise** if the measurement contradicts it — one
  line, up front, before the options.
- **Three alternatives, labelled A/B/C**, each with what it is, what it costs,
  and the honest risk. A few lines each.
- **Push back on the option that only looks like a compromise.** "Ship both
  behind a flag" is usually the most expensive and least decisive choice: two
  configurations to measure, provenance to record per stored item, and the one
  module that must stay simple doubles in size.
- **Say which options are not actually competing.** Often the cheap one unblocks
  today and the thorough one lands later; sequence beats choice.
- **Close with the order of operations**, including anything unrelated but
  overdue that the audit surfaced.

## Pitfalls

- **A licence conclusion drawn from a search result is not a finding.** Search
  descriptions compress "code is MIT, weights are not" into "it's MIT" routinely.
  Fetch the file.
- **A permissive wrapper does not license the engine underneath it.** An MIT
  skill pack, plugin or template that drives a separately-licensed renderer
  carries the wrapper's licence only; audit the engine as its own artifact
  before telling the user the toolchain costs nothing.
- **Audit the project's own notes for a stale licence claim while you are there.**
  The claim was usually written once, early, by someone who had not separated the
  artifacts — and every later session inherits it as settled fact.
- **A component isolated behind one module was isolated on purpose.** Before
  proposing to restructure around a swap, check whether the seam already exists;
  proposing an architecture change where the seam is already cut wastes the
  user's time and misrepresents the work.
- **Two models with near-identical benchmark scores can differ sharply on a small
  real dataset.** Hard cases and few samples per class are where a lighter model
  loses, and none of that shows in a headline figure. Schedule the measurement;
  never substitute the benchmark for it.
