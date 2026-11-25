---
name: open-text-validation
description: Walks a researcher through testing whether a randomized treatment changed what respondents wrote in open-text answers (a construct or manipulation check), with the split-first protocol of the opencheck R package. A study card is written before any text is read, discovery and codebook work use a discovery fold only, the measurement is frozen into a hashed lock before the estimation fold is opened, and effects are estimated on the estimation fold with placebo constructs and split sensitivity. Covers yes/no presence, 0-9 rating, LLM-induced codebooks, pairwise Bradley-Terry scaling, local/ALICE/API runs, and reporting. Use when the user has open-ended responses from a survey experiment or conjoint and wants to know whether the treatment activated the intended consideration. General codebook and validation advice goes to text-classification; topic discovery to topic-modeling; logprob calibration to llm-calibration-logprobs.
argument-hint: '[describe the experiment, the open-ended item, and the treatment]'
---

# Open-Text Construct Checks with a Split-First Protocol

## Instructions

The question is narrow: did the randomized treatment change which considerations respondents articulate? The estimand is a text-as-outcome ITT, E[g(R(1))] − E[g(R(0))], where g is a measurement function fixed before the estimation data are seen. It is a regime contrast, not a mediation effect (Blackwell, Ma & Opacic 2024; Aklin et al. 2026). Say so to the user before anything else.

The one rule that cannot bend: **nothing that defines g may be tuned on the data used to estimate the effect.** That covers the codebook, prompts, few-shot examples, construct wording, the model roster and decoding settings. Topic models fit on all responses, codebooks revised on all responses, and few-shot examples drawn from estimation responses all break it. Reviewers call this double-dipping; under permuted labels it inflates false positives. The package enforces the rule; your job is to keep the user inside it.

Work through the steps in order. Use `opencheck` for every computation (`library(opencheck)`; source at `~/Documents/github/resources/opencheck`). Run R with `LANG=en_US.UTF-8`: in a C locale, R writes CJK text as `<U+XXXX>` escapes, and the package refuses such text.

### 0. Pick a hardware tier

Ask what the user has, then call `oc_profile()`.
- **Local:** a laptop with Ollama, Gemma 4 E4B.
- **Workstation:** one 24 GB GPU, Gemma 4 12B.
- **HPC:** SLURM with A40/A100, Qwen3.6-35B-A3B and Gemma 4 31B, plus API models.

The protocol does not change with the tier. In the validation corpus Gemma 4 E4B agreed with held-out human codes as well as models six to eight times its size, but it ran at full precision on a cluster GPU. A quantized Ollama copy on a laptop has not been validated: before relying on it, compare its labels with a full-precision run on about 100 discovery-fold items. Run two model families when you can.

### 1. Study card, before any text is read

Copy `system.file("templates", "study_card.yaml", package = "opencheck")` and fill it in with the user:

- **Treatment and contrast.** Use the randomized arm, or for a conjoint the attribute level in the **pair shown**. Never condition on the chosen profile: the choice is post-treatment.
- **Target construct(s).** One sentence each, in the authors' terms, with expected direction.
- **1–3 placebo constructs.** Considerations the treatment should not move, each a separate yes/no judgment. As categories of one label they fall when the target rises, and the check is void.
- **The context sentence shown to models.** Who answered, what they saw, what they were asked. No results.
- **Provenance.** Whether the text was read before writing the card, and any prior analysis of it.

Then `oc_study_validate()` and `oc_study_register(path, registry)`. Changes after registration need `amend = "reason"`; they are logged, never silent.

### 2. Split once

`oc_split(data, "id", strata = c("treatment", "country"), p_discovery = 0.3, seed = 42, n_splits = 11)` then `oc_split_write()`. Split 1 is primary; splits 2–11 feed the sensitivity analysis. Add `scheme = "twofold"` for a swap design. The manifest cannot be redrawn: a different split at the same path is an error.

### 3. Discovery and codebook work on D only

Read data only through `oc_discovery_data(data, split, log = ...)`.

- **Theory-only arm (A1):** `oc_prompt_presence()` and `oc_prompt_rating()` from the card. Needs no data.
- **Induced codebook (A2):** `oc_induce_request()` on D, run in generation mode, then `oc_induce_import()`. Repeat per split for the sensitivity distribution.
- **Researcher codebook (A3):** draft in Halterman–Keith YAML with the user (definition, clarification, negative clarification).
  - Few-shot examples need an `id` from D or `constructed: true`.
  - Iterate on D: pilot, read disagreements between models (and existing human codes on D if any), revise.
  - For general codebook advice, defer to `text-classification`.
- **Pairwise (B):** `oc_prompt_pairwise()` on the target. Bradley–Terry has no zero, so pair it with a presence measure.

Pilot every prompt on about 100 D items and check `valid` ≈ 1 and `p_valid` near 1 before freezing.

- With `max_tokens = 1`, multi-token code names arrive as prefixes. Use `oc_prompt(cb, answer = "number")` when code names share a first token.

### 4. Freeze

`oc_freeze(lock_path, split, components = c(codebook = ..., card = ...), prompts = list(...), models = ..., decoding = ...)`. The lock hashes every file and the exact prompt text. A changed codebook needs a new, separately named lock; report the change.

### 5. Measure on E

`oc_estimation_data(data, split, lock)` opens E only with a valid lock.

- **Locally or through an API:** `oc_classify(..., lock = lock)`. It is resumable and keyed by prompt and settings.
- **Batch:**
  - `oc_export_requests()` / `oc_export_pairs()` → the runner `inst/python/oc_vllm_runner.py`, launched with `oc_slurm_job()` (see the `alice` skill for Leiden's cluster), or `inst/python/oc_jev_client.py` for Jev;
  - then `oc_import_results()` / `oc_import_pairs()`, and `oc_bt()` / `oc_bt_validate()` for pairwise (report held-out accuracy and ICI).
- Use at least two model families; report agreement across models as reliability, not validity.
- Estimate API cost before each run.

### 6. Estimate and report

- `oc_effect(y, treat, strata, n_perm = 2000)` for every target **and** placebo under every contrast: a Neyman SE and a randomization p.
- `oc_aggregate_splits()` over the per-split A2 estimates (median estimate, median-adjusted SE, range).
- If human codes exist in E, report accuracy and κ there only (codes in D may be used for tuning), and correct the effect for measurement error with DSL or PPI.
- Report:
  - the card hash and lock hash;
  - N in D and E;
  - every arm and every placebo;
  - the split distribution;
  - models with exact revisions and access dates;
  - what was decided after which data were seen.
  Defer to `methods-reporting` for the checklist.

## Pitfalls to catch

- Looking at estimation-fold output (or full-sample topic models) before the lock exists.
- Conjoint contrasts defined on the chosen profile.
- Placebos measured as categories of the same label as the target.
- Few-shot examples quoted from E, or from text the card writer read.
- A single open-end after the last task, interpreted as a task-specific effect. It responds to the whole treatment history (R2's cumulative-exposure point).
- Text corrupted by the locale (`<U+…>`), text cut at token limits, and `NA` strings read as missing.
- Reading self-reported model confidence as accuracy: first-token probabilities track disagreement, not correctness (see `llm-calibration-logprobs`).
