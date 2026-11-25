---
name: tune-data
description: Build a training dataset for fine-tuning, distillation, or continued pretraining. Use when the user wants to turn logs/CSV/JSONL into fine-tuning data, label data with an LLM, distill a teacher model's outputs, generate synthetic training examples from nothing, chunk raw domain text for CPT, deduplicate a dataset, make train/valid/test splits, convert to MLX chat format, write a datacard, or asks "how much data do I need to fine-tune?".
---

# tune-data — build the dataset

Data quality determines fine-tuning quality more than any hyperparameter. The pipeline: **ingest → (distill) → dedupe → split → validate → datacard**. Every step has a bundled script; chain them, don't skip the gates.

`<skill-dir>` below = the directory containing this SKILL.md. Stdlib scripts run with `python3`; `distill_generate.py` is PEP 723 (`uv run`). Run everything from the user's project workdir.

## Before asking the user anything: read the project state

On invocation, check the workdir **first** — a fresh session (or one that just compacted) must resume mid-pipeline from disk alone:

1. **`EXPERIMENT-LOG.md`** — tune-decide writes the interview summary and level decision here precisely so you never re-ask. Look for: task shape, data inventory, the chosen level, any frozen labeling prompt or dedupe threshold from a prior session.
2. **`runs/*/state.json`** — if any run has `status: running|interrupted`, training is using `data_dir` right now (or will resume into it). Do not regenerate splits underneath it; ask before touching that directory.
3. **Partial pipeline artifacts** — resume where disk says you are: a raw teacher-output file smaller than the input means resume labeling (the script skips done ids; session-native, count ids and continue); `deduped.jsonl` present means go to split; `data/{train,valid,test}.jsonl` present means re-run validate and go to the datacard.

If there is **no level decision** in EXPERIMENT-LOG.md, route to **tune-decide** before building anything — whatever the task shape. Classification smell (N fixed categories, labels already logged) is the most urgent case: a Level 1 embeddings+classifier may need no fine-tuning dataset at all, and proving that in 10 minutes beats preparing data for a LoRA the user doesn't need.

After every completed stage, append to `EXPERIMENT-LOG.md` (append-only, `## <date> — <event>` with short Decision / Run (config) / Result / Predicted-vs-actual / Lesson lines as applicable). That log is what makes the dataset reproducible.

## Teaching protocol

Every step below is framed as four short lines before running it — **What** we're doing · **Why** it matters (the failure it prevents) · **Expect** what healthy output looks like · **Read** how to interpret what came out — and one line after connecting result → next decision. One-liners, not essays; jargon defined inline on first use, with depth in the bundled concepts files (`../../concepts/` relative to this file, e.g. concepts/epochs-and-overfitting.md). If the user says "skip the teaching" (or is clearly expert): drop Why/Expect/Read, keep What + the result reading.

**Stop-and-ask checkpoints.** tune-data stops for user judgment at exactly two points, nowhere else: **the prompt-freeze checkpoint** — freezing the labeling/teacher prompt after the 25-sample spot-check — and **the expensive-run checkpoint** — before a full API labeling job or anything that costs real money or hours. The level recommendation was tune-decide's checkpoint (read it from the log); the acceptance bar and metric set are registered by tune-decide at decision time and confirmed in tune-eval before any scoring.

**Research mode.** If EXPERIMENT-LOG.md marks the project research mode (or the goal is understanding, not shipping): build the smallest dataset that serves the experiment. Keep the train/valid split — val loss is the instrument. Skip the datacard and test ceremony. For the dedupe-ablation experiment, planted duplicates are the point: dedupe one arm only, never both.

## Target formats (MLX-LM, auto-detected)

Output is a directory (conventionally `data/`) with `train.jsonl` / `valid.jsonl` / `test.jsonl`, one JSON object per line, all in ONE of:

| Format | Line shape | Use for |
|---|---|---|
| **chat** | `{"messages": [{"role": "system"...}, {"role": "user"...}, {"role": "assistant"...}]}` | SFT — the default. System turn optional; keep it identical across records if used |
| **tools** | chat messages (assistant turns may carry `tool_calls`) + top-level `"tools": [...]` | tool-call SFT |
| **completions** | `{"prompt": "...", "completion": "..."}` | SFT without chat structure |
| **text** | `{"text": "..."}` | continued pretraining (CPT) on raw domain text |

These are standard JSONL — any trainer consumes them (TRL/Unsloth/axolotl on NVIDIA, cloud jobs). tune-data is backend-agnostic by construction; only the training step is MLX-first.

## Step 1 — pick the path by what exists

| Path | You have | Route |
|---|---|---|
| **A** | labeled/paired data (logged LLM calls, human-labeled CSV) | convert to MLX format → Step 2 |
| **B** | unlabeled inputs, teacher must label | teacher tier below → Step 2 |
| **C** | nothing | synthetic inputs + teacher labels → Step 2 |
| **D** | raw domain text (docs, filings, code) for CPT | chunk → Step 2 |

Sizing, when the user asks "is this enough?":

| Task | Minimum to try | Comfortable |
|---|---|---|
| Classification SFT | 50–100/class | 500+/class |
| Generation/extraction SFT | 500 pairs | 1k–10k |
| CPT | under ~10M tokens, question whether CPT is worth it at all | ~10M+ tokens |

Always: 1,000 clean, deduped, diverse examples beat 10,000 noisy ones.

### Path A — labeled data exists

Conversion is task-specific — write a small throwaway script. Keep the original input text and any **stable id** in each record (ids survive into resume logic and the datacard). Map: input → user turn, logged output/label → assistant turn, one shared system prompt describing the task.

### Path B — unlabeled inputs + teacher

**Pick the teacher tier by dataset size** (tunelab runs inside Claude Code — an authenticated Claude session):

| Tier | Size | How | Provenance note |
|---|---|---|---|
| **Session-native** (the DEFAULT, no API key) | up to ~500 — and always when no API key is at hand or the job is one-off | the session itself labels — fan out subagents for batches of ~25–50 | model **unpinned** — say so in the DATACARD |
| **API script** | above ~500 (to ~2k), or whenever a pinned model / resumability matters | `distill_generate.py`: pinned model, structured-output guarantees, resumable | provider + model pinned |
| **Batches API** | >2k | roadmap — mention it (halves cost); run overnight or accept sync cost | — |

**Session-native protocol** — label/generate directly, writing JSONL in the *exact* record shapes `distill_generate.py` produces, so every downstream step is tier-agnostic:

- raw output, classify: `{"id": ..., "text": "...", "label": "..."}` · generate: `{"id": ..., "text": "...", "generated": "..."}`
- training record: `{"messages": [{"role": "system", "content": <system prompt>}, {"role": "user", "content": <text>}, {"role": "assistant", "content": <target>}]}`

Resume by counting ids already in the raw file and processing the remainder. For batches, fan out subagents with the frozen prompt and 25–50 items each.

**Spot-check before scaling — ALWAYS, both tiers.**

> **What:** label the first 25 items only, then read every one with the user. **Why:** a bad labeling prompt poisons the entire dataset — 25 items is the cheapest point to find out. **Expect:** ~2–3 disagreements surfacing genuinely fuzzy label boundaries. **Read:** disagreements = prompt fixes, not item fixes — edit the prompt, not the labels.

Then **stop and ask** (the prompt-freeze checkpoint): show the corrected prompt, get explicit agreement, and **freeze it** — the same prompt verbatim for every remaining item, logged in EXPERIMENT-LOG.md and the DATACARD. Changing the prompt mid-run yields a dataset labeled by two different policies.

**API script** (needs `ANTHROPIC_API_KEY`; stop and ask before the full run — the expensive-run checkpoint):

```bash
# Spot-check first:  add --limit 25
# Classification (structured output guarantees a valid label):
uv run <skill-dir>/scripts/distill_generate.py --mode classify \
  --input inputs.jsonl --input-key text \
  --labels "billing,receipt,spam,support,newsletter,other" \
  --system "You label inbound emails for a small business." \
  --output data_labeled.jsonl --train-out train_chat.jsonl

# Generation (teacher produces the target output per input):
uv run <skill-dir>/scripts/distill_generate.py --mode generate \
  --input inputs.jsonl --input-key text \
  --system "Draft a reply in our support voice: concise, warm, no corporate filler." \
  --output data_labeled.jsonl --train-out train_chat.jsonl
```

Defaults: `--provider anthropic` with `--model claude-opus-4-8`, or `--provider openai` (needs `OPENAI_API_KEY`; only the selected provider's key and SDK are used) with `--model gpt-5.5`. Cheaper teachers trade quality for cost on easy jobs — ask first: `claude-sonnet-4-6` / `gpt-5.4-mini`, or `gpt-5.4-nano` for easy label sets (all ids verified 2026-06). `--max-tokens` 256 classify / 1024 generate. Resumable: ids already in `--output` are skipped on re-run; refusals/unparseable outputs are skipped and counted, re-run to retry. **Id-stability warning:** resume matches on the `"id"` field — if the input lacks ids, line numbers are used, so never reorder the input file between runs.

### Path C — nothing (synthetic from scratch)

Have the teacher generate the *inputs* too — but naive "generate 500 examples" prompts collapse into near-duplicates. Generate in batches with **explicit diversity instructions**: vary personas (novice/expert/angry/terse), lengths (one-liners to paragraphs), tones, phrasings, and edge cases (ambiguous asks, typos, adversarial inputs) — name the axes in the prompt and assign different slices to different batches. Generate **~130% of target**; dedupe eats the excess. **Spot-check the inputs too:** generate the first ~25 synthetic inputs and read them with the user for spread (distinct personas, lengths, edge cases — not 25 rephrasings); fix and freeze the generation prompt, then scale. Then label/generate targets exactly as Path B, including the 25-sample output spot-check and prompt freeze. Record `provenance: synthetic` in the DATACARD.

### Path D — raw domain text (CPT)

Gate first: under ~10M tokens, CPT likely isn't worth it for production — knowledge tasks are retrieval problems (RAG first; see ../../concepts/cpt-vs-rag.md). Small-corpus CPT is fine as a **research-mode experiment** with expectations reset to perplexity/fluency, not QA accuracy. Say this before chunking 200 markdown files.

> **What:** chunk documents into `{"text"}` records on natural boundaries. **Why:** CPT trains on raw text; mid-sentence cuts teach mangled language. **Expect:** chunks landing between `--target-tokens` and `--max-tokens` — commonly ~2× target, *not* near target. **Read:** the printed min/median/max chunk tokens, and the per-file chunk counts.

```bash
python3 <skill-dir>/scripts/chunk_text.py --input corpus/ extra_notes.md \
  --output chunks.jsonl --target-tokens 2000 --max-tokens 4000 --min-tokens 50
```

`--input` takes files and/or directories (dirs recurse for `.txt`/`.md`); tokens approximated as chars/4. Splits at markdown headings, then blank-line paragraphs; merges small pieces toward target; drops fragments under `--min-tokens`. Two consequences to act on: (1) at the defaults, routine chunks **exceed mlx_lm's `--max-seq-length` default of 2048** — tell tune-train to raise it, or chunk with `--target-tokens 1000`; (2) each record carries a `"source"` key (relative path — mlx-lm ignores unknown keys) — it feeds the DATACARD's provenance section. Dedupe afterwards is **mandatory** for CPT corpora.

## Step 2 — dedupe

> **What:** remove exact and near-duplicate records. **Why:** repetition is the dominant cause of memorization — a record appearing 50 times trains ~50 epochs on that one example and the model recites it verbatim (see ../../concepts/epochs-and-overfitting.md). **Expect:** a few percent dropped on organic data. **Read:** the sample kept/dropped pairs it prints — every time, before trusting the output.

```bash
python3 <skill-dir>/scripts/dedupe.py --input train_chat.jsonl --output deduped.jsonl
```

Exact dups via normalized hash; near-dups via deterministic MinHash (banded Jaccard over character 4-gram shingles — byte-identical output across runs, no hash-seed dependence) at `--threshold 0.80`. Chat records are compared on user/assistant content only — a shared system prompt is boilerplate, not duplication. First occurrence wins.

**The reading ritual:** the script prints up to 3 sample near-dup pairs. Read them with the user. If **>20% of records are flagged**, it warns about templated-data collapse — records differing only in names/numbers. Collapsing those is usually right (templates are exactly what gets memorized), but if templates are the legitimate shape of the task (receipts, form letters), re-run with `--threshold 0.95` *after* inspecting the samples, and log the choice + rationale in EXPERIMENT-LOG.md.

## Step 3 — split

> **What:** split into train/valid/test, 80/10/10, seeded. **Why:** without stratification a rare class can vanish from a split; without a held-out test set there is no honest scoreboard. **Expect:** three files with per-class proportions roughly preserved. **Read:** the per-split counts, and any empty-split warnings — an empty test set silently breaks the eval contract.

```bash
python3 <skill-dir>/scripts/split_data.py --input deduped.jsonl --outdir data/ \
  --ratios 0.8,0.1,0.1 --seed 42 --label-key label
```

Stratify whenever a label exists: `--label-key <field>` for a top-level field, or `--label-from-assistant` when the last assistant message *is* the label (the distillation chat shape) — they're mutually exclusive. No label field at all (open generation pairs)? Say so out loud — "splitting unstratified: no label to stratify on" — so the choice is visible, not accidental. The seed makes the split reproducible: same input + same seed = same split, which is what lets a future session regenerate it from the log.

Say the contract to the user explicitly: **valid.jsonl steers training (early stopping, hyperparameter picks); test.jsonl is looked at exactly once, at the end, by tune-eval.** A test set peeked at during development is just a second validation set wearing a costume (see ../../concepts/validation-vs-test.md).

## Step 4 — validate (the gate)

> **What:** machine-check every record before training. **Why:** mlx_lm's failure mode for malformed data is a cryptic error minutes into a run. **Expect:** `OK — safe to train`, exit 0. **Read:** errors block training; warnings are judgment calls — read each one.

```bash
python3 <skill-dir>/scripts/validate_dataset.py --data-dir data/
```

Checks: every line parses; format is one of the four mlx-lm 0.31.3 auto-detects (chat / **tools** / completions / text) and consistent within and across splits (chat+tools mixing is legal → warning only); chat roles sane, last turn assistant, no empty content; records under mlx_lm's `--max-seq-length` default of **2048 tokens** (≈chars/4 — longer records warn: raise `--max-seq-length` in tune-train or shorten); per-split counts + label distribution for classification-shaped data. Missing/empty `valid.jsonl` is a warning (mlx-lm trains without it, but tune-train's overfitting detection needs it).

**Non-zero exit = do not train.** Fix and re-run until it passes. No exceptions — this is the gate.

## Step 5 — datacard

Write `data/DATACARD.md` — short, factual, the first place future-you looks when an eval result is weird:

```markdown
# DATACARD — <dataset name>
- **Provenance:** <logs export | synthetic | corpus paths — Path D: source files from chunk records' "source" keys>
- **Teacher:** <tier: session-native (model unpinned — note date) | API script: provider + model> — or n/a (Path A/D)
- **Labeling prompt (frozen <date>):** <exact system prompt verbatim>
- **Dedupe:** <N in → N out; exact / near-dup counts; threshold + rationale if not 0.80>
- **Splits:** train/valid/test sizes; seed; stratification key
- **Known gaps:** <"no examples of X", class imbalance, length skew>
- **Intended use:** <narrow task> — distilling a closed provider's outputs may be ToS-restricted
  for training competing models; a narrow internal task model on your own traffic is a different
  posture, but the call is yours (see the distillation concepts note bundled with the tunelab plugin).
```

Eval reports downstream must also record which tier + model produced labels/verdicts — the datacard is where they look it up.

## Step 6 — log and hand off

Append to `EXPERIMENT-LOG.md`, e.g.:

```markdown
## 2026-06-12 — tune-data: dataset built (support-replies)
Decision: Path B, session-native teacher (~400 items); prompt frozen after 25-sample spot-check (2 fixes).
Run (config): dedupe --threshold 0.80 (412→389); split --seed 42 --label-from-assistant 0.8,0.1,0.1.
Result: train 311 / valid 39 / test 39; validate_dataset OK.
Lesson: refund-vs-billing boundary fuzzy — clarified in the frozen prompt.
```

Then hand off to **tune-train** with the `data/` path, the format, and any `--max-seq-length` note from chunking/validation. On NVIDIA/cloud setups: hand the same `data/` to TRL/Unsloth/axolotl or a cloud job instead — then return to **tune-eval**, which is backend-agnostic too.
