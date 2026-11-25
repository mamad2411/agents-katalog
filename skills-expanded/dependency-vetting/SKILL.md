---
name: dependency-vetting
description: "Use when the owner brings a model or library to adopt. Vet it."
version: 1.1.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [evaluation, dependencies, models, research, caveats, roadmap, stress-test]
    related_skills: [build-method, project-memory]
---

# Dependency Vetting

Mid-project the owner finds a new model, library or service, has "got the
point" of it, and wants to know whether it belongs in the current build. The job
is not to share the enthusiasm. It is to say what the
thing IS in plain words, whether it fixes a weak point the project actually has,
what its known failure modes are, and where in the plan it goes — or why it
does not go anywhere.

Two requests arrive here, usually in this order. Answer both from primary
sources, never from memory — the thing is new by definition and memory is stale.

```
  1. "analyse it, pros and cons, does it help us?"   → VERDICT
  2. "check its caveats/gotchas so we set it right"  → CAVEAT SHEET, into the plan
```

## 1. Fetch the primary sources, in one batch

`web_extract` may not be available on every backend; `curl` through `terminal`
or `execute_code` always is. Fetch all of these together before saying a word:

```bash
# the thing itself
curl -sL https://raw.githubusercontent.com/<org>/<repo>/main/README.md
curl -sL https://raw.githubusercontent.com/<org>/<repo>/main/LICENSE
curl -sL https://raw.githubusercontent.com/<org>/<repo>/main/llms.txt   # many AI repos ship one; it is the API reference
# health and licence as GitHub sees them
curl -sL https://api.github.com/repos/<org>/<repo>          # license.spdx_id, stargazers_count, created_at, pushed_at
# what breaks, ranked by how many people hit it
curl -sL 'https://api.github.com/repos/<org>/<repo>/issues?state=all&per_page=100&sort=comments'
# the launch thread, where the author answers critics
curl -sL https://hn.algolia.com/api/v1/items/<hn-id>       # find the id with web_search "<name> hacker news"
                                                          # comments carry raw control chars: json.loads(s, strict=False)
```

Then the vendor's own guides on the two things that matter most (confidence /
thresholds, supported platforms), and one or two INDEPENDENT benchmarks — a
gist or blog that measured it on real hardware and says so.

If a source cannot be reached, say which one; never fill the gap with a
plausible guess.

## 2. Write the verdict — this shape, always

```
  WHAT IT IS        3-5 lines each, plain words, one analogy. Group by idea when
                    the owner brings several things at once (the closed original, the
                    open re-do, the tiny model).
  OUR WEAK POINTS   list the project's actual hard problems; say which one each
                    candidate touches. Usually: none of the core ones.
  VERDICT           per candidate: YES / NO / LATER, one reason each, and the
                    hard rule it hits (CPU-only, local-first, no cloud, licence).
  WHERE IN THE PLAN which roadmap step, and what must exist BEFORE it.
```

Rules that decide most verdicts before any benchmark:

- **A text model cannot fix a pixel problem.** Locate the exact seam where the
  candidate's input type meets the project — for an image app that is the
  chat/agent door, never the image pipeline. Say so explicitly, or the owner
  will read "promising model" as "more reliable tool".
- **A caption-then-classify chain is a double lossy translation.** "A VLM describes
  the image, then a text classifier scores the description" turns numbers into words
  and back into a guess. First check whether the project's own model already outputs
  the quantities wanted (pose, region size, detection score, embedding distance). If it
  does, the chain is a NO, and the VLM is at most a LATER for what numbers cannot see
  (context the numbers do not encode). Confirm a candidate's modality from its model card's
  `pipeline_tag`, not from its marketing.
- **Read the machine before recommending weight.** Get CPU cores, RAM and GPU
  (`Get-CimInstance Win32_Processor / Win32_ComputerSystem / Win32_VideoController` on
  Windows), then time the EXISTING model on a handful of the user's files and state
  hours per 10k. A GPU on the box does not override a project's CPU-only rule.
- **The project's hard rules are the filter.** Cloud, GPU, waitlist, closed
  weights: each is a one-line NO. Do not benchmark what a rule already rejects.
- **Read the licence of the WEIGHTS, not the repo's LICENSE file.** The
  LICENSE file and GitHub's `license.spdx_id` cover the code only; a model's
  terms live in the README "License" section or the Hugging Face model card,
  and they differ from the code licence in a large share of vision
  repos (MIT code over non-commercial weights is the common shape). A
  wrapper library that is itself MIT does not launder the models it
  downloads — its own licence section just links each model's terms. And
  permissive weights trained on research-only datasets are a third, legally
  unsettled case: name it as such, never resolve it. Licences change between
  releases, so read them now, not from a blog. Read the licence's own
  DEFINITION of non-commercial: "research or evaluation only" is stricter than
  "personal use" and excludes a published project's assets.
- **Compare an installed build to upstream before judging a new model.**
  Runtimes add model support at release and ship quality fixes (schedule,
  VAE) in the following days: GitHub `compare/<installed>...<latest>` lists
  them. A bad result on a stale build is not a verdict on the model.
- **A licence survey is a table with two licence columns** — repo licence
  and weights licence — plus ONNX/CPU availability, embedding size and a
  numbered primary-source link per row. State the switching costs beside the
  one clean row (embedding size → schema bump, new alignment path, every
  measured constant re-measured) so the decision is made against them, and
  end with the verdict as a decision for the owner, not a recommendation to switch:
  a personal-use tool pays nothing for a non-commercial licence.
- **"Beats models 10x its size" is a claim about the vendor's test set.** The
  repo's own open issues about its acceptance suite are the real number.

## 3. The caveat sheet

Rank the weaknesses by how much they bite THIS project, not by how loud they
were online. For each: the mechanism, the evidence, and the rule it sets.
Mark which version each finding came from — a flaw measured on v2 is a thing
to re-test on v3, not a fact about v3.

What to look for, every time, for a small task-specific model:

| Look for | Because |
|---|---|
| how literal the input must be | small models map surface words to tools; implication and "same as before" fail |
| is the confidence score usable as a threshold | often not out of the box, `None` when fine-tuned, collapses on non-English |
| acts-when-it-should-refuse | the repo's own acceptance suites failing on the shipped engine is the tell |
| determinism | sampling engines give opposite answers to one prompt; test same input ×20 |
| tool/option count ceiling | retrieval heads hide options past N; expose fewer than N |
| grammar/enum enforcement | constrained decoding still emits invalid values; validate in code anyway |
| fine-tuning path | quantisation and engine/training mismatch destroy tuned behaviour; base weights first |
| telemetry, pickle loaders, closed engine binaries, serve-mode hangs | privacy and hygiene; env vars to set and PROVE with a capture |
| what the author concedes in the launch thread | the honest scope statement is there, not in the README |
| repo age vs stars (`created_at` from the API) | tens of thousands of stars in a week is hype, not a track record |

Close the sheet with the design that survives the caveats, as a five-line
diagram: candidate = translator only → our code validates → confidence bands
(act / confirm / refuse) → the existing safe path. Destructive actions always
confirm, whatever the score.

## 4. Put it in the plan, not in the chat

The ask is always "write this new guest into the plan". The verdict and
the caveat sheet go into the roadmap beside the step that will use the thing,
so a future session does not rediscover them. Three parts, in this order:

1. **The step itself**, phrased as a measured head-to-head: candidate vs. the
   dumbest baseline that could work (a 40-line keyword/fuzzy matcher), scored
   on a frozen suite of ≥ 30 of OUR inputs kept in the private tree, the
   threshold written down with the numbers, re-run on every version bump.
   "If it does not beat the baseline it does not ship."
2. **The caveats as bullets under that step**, each ending in the rule it sets.
3. **A "Rejected, so not re-proposed" block** naming every alternative the owner
   brought and the one-line reason — including "no text model in the core
   pipeline". A rejection that is not written down is re-proposed next month.

Order of build stays: the contract/interface step first, the candidate spike
second. A model needs a fixed set of targets to aim at; define those before
measuring how well it hits them.

Then the project's own docs procedure (project-memory): log entry, gates,
sweep. No public file changes for a plan-only session — prove it with
`git add -A --dry-run` rather than assuming it.

## 5. Running the head-to-head (the spike itself)

One script under the private tree, one suite file, one venv in Temp (`uv venv`,
`uv pip install "<pkg>==<pinned>"`) — nothing enters the project venv or `src/`
until the number says so. Order:

1. **Freeze the suite in its own file before the first run, never edit it
   after.** A case added mid-run tunes the suite to the candidate being
   watched. A miss caused by a keyword the baseline lacked stays a miss on
   record; fix it in the next suite version. Cover, per tool: positives,
   typos, negations, off-topic, ambiguous-about-the-decision, an unknown
   name the validator must catch.
2. **Write the dumb baseline first** (stdlib `difflib` + keyword lists, ~40
   lines). It sets the bar; a model that ties it is a dependency for nothing.
3. **Both candidates behind the SAME validator** (does the named item exist, is
   the index in range). A win that comes from one side's post-processing is
   not the candidate's win.
4. **Sweep the threshold, do not pick one.** Score at every T and print the
   curve. A flat curve (same score from 0.1 to 0.95) means the confidence
   score is not a usable gate — that is a finding, write it down.
5. **Try the vendor's tool-design guide as variant 2** before calling the
   model bad — synonyms in descriptions, formats on arguments, enums in the
   grammar. If variant 3 adds regex triggers, note that the gain came from
   regexes, because those ARE the baseline.
6. **Determinism**: 3 sentences × 20 runs, count distinct outputs, in the
   same script.
7. **Print the misses side by side** (which candidate missed, expected vs.
   got, confidence). The hard-rule-breaking miss — a confident wrong action
   on a negation — outweighs the score. Name it in the verdict.

The verdict goes into the project's measurement page as a table plus the
worst miss, and the roadmap step is ticked with the numbers inline. Keep the
scripts and per-variant `results_*.json` in the private tree for the re-run
on a version bump; they are the suite's evidence, not litter.

**Proving "it sends nothing"** (telemetry, phone-home): a clean result is
suspect until the same detector is shown to fire with the behaviour ON. The
recipe and its traps: `references/absence-proofs.md`.

## Pitfalls

**Answering from what the model name sounds like.** The README of a thing
released this week is the only description that exists. Fetch it.

**Letting the analysis end in the chat.** A verdict the owner agreed with and nobody
wrote down is a verdict the next session re-litigates. The roadmap is the
deliverable.

**Benchmarking before filtering.** Check the hard rules (GPU, cloud, licence)
first — most candidates die there in one line and save the afternoon.

**Confusing "the vendor says it refuses" with "it refuses".** Refusal on
off-topic input is the safety story of every small tool-calling model and it
is the first thing independent runs find broken. It is a goal until measured
on our suite.

**Proposing fine-tuning as the fix.** For 2-bit / tiny models it is the
commonest way to lose the confidence signal and get engine≠training drift.
Base weights with a better tool list, or drop the candidate.

**Searching a log heading with `search_files`.** Headings like
`## [date] build | step` contain `[`, `|` and `.`, which the regex engine
reads as a class and alternation, and the call errors out. Use
`grep -n -F '<heading>' file` from the terminal, then read from that line.
