---
name: "laya-training"
description: Fine-tune and evaluate Laya on labelled data, with before/after benchmarks. Use to train, fine-tune or retrain Laya, or learn the process through an optional guided Kaggle walkthrough with a bundled practice dataset.
license: Apache-2.0
compatibility: Needs Python 3 to run the bundled scripts. Fine-tuning runs on Kaggle (free account, GPU T4 x2 accelerator, internet access for package installation), so no local GPU is required.
metadata:
  author: SimpleCalm AI
  version: "1.0.11"
---

<!-- Copyright 2026 SimpleCalm Labs Ltd and contributors. SPDX-License-Identifier: Apache-2.0 -->

# Laya training

Laya is an open-weight encoder model developed by Convai Innovations. It answers typed questions (choice, score and yes/no) about a piece of text and returns probabilities. Training it on labelled examples can make it useful for one narrow decision, such as routing a support call or classifying an initiative. This skill takes a labelled dataset through to a trained model and a fair verdict on whether it works.

Use the official repository and notebook: <https://github.com/NandhaKishorM/laya>.

## Your training data

Show this notice to the user before they choose or prepare training data:

> Always make sure you are entitled to use your dataset to train or fine-tune AI models. A trained model keeps what it learned from its data. If you use data you have no right to, you may face legal claims and have to withdraw or retrain the model.
>
> You can use data when you definitely own it, or when you have correctly licensed it for this purpose.
>
> If you do not own the dataset, check its licence and make sure this use is not prohibited or restricted. If in doubt, do not use it.

The user decides whether they are entitled to use their data. Do not make that decision for them.

## Plain language

Many users are not technical. Explain each new term in one plain sentence the first time it appears (for example: "a GPU is a fast processor used for training"). Prefer everyday words to jargon, and say why each step matters before saying how to do it.

Speak as a friendly guide, not an instruction manual. Say what something is before asking the user to do anything with it, offer actions as gentle suggestions, and leave choices such as names to the user. Avoid bare commands such as "Download this" or "Run this". For example: "This is your training data. Please download it to your computer. Please save it in your project folder." Be direct about what is required: if something is needed, say so plainly, for example "You'll need a Kaggle account." Keep messages short.

## Licence of this guide

This training guide and its helper scripts are licensed under Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). Laya is separately developed and licensed by its upstream contributors. The guide does not bundle Laya's implementation, notebook or model weights. The bundled practice dataset is described in [assets/snips/SOURCE.md](assets/snips/SOURCE.md). When preparing a model or notebook for redistribution, check that exact upstream revision, include its licence, retain relevant attribution and NOTICE text, and mark changes to upstream files.

The beginner guide ends with downloading the model and a minimal local prediction script. Broader deployment, such as shadow mode or a production service, is outside this skill.

## Choose the path

When the user asks to learn, says they are new or unsure, or has no clear decision or dataset, read [the beginner guide](references/beginner-guide.md) before responding. It supplies the opening explanation of Laya and the parts of the process, the ordered teaching path and the bundled practice dataset. Give that orientation before practical instructions. After showing the data notice, ask whether the user has their own data they would like to use instead of the bundled SNIPS practice data in `assets/snips/`. Do not search for other datasets. Run the learning experiment on Kaggle, then guide saving the notebook, downloading the complete model and basic local inference. Do not stop at the benchmark result.

**Learning contract (beginner path).** The user does each step themselves and you guide them. Say this in your first reply, in words like these:

> You'll do the clicks and run the commands yourself, so you can repeat the process later on your own. I'll explain one step at a time, tell you what you should see, and help you read the result before we move on. I'll only do something on your computer if you ask me to do that step.

Then keep to it: do not run commands, create folders or write files on the user's computer unless they ask you to do a particular step. Ask for output only at meaningful checkpoints, not after every obvious click.

When the user has a clear task and dataset and wants execution, follow the workflow below without loading the beginner guide. Honour an explicit request for a walkthrough even when they have their own data. Both paths use the same technical procedures below.

## Files in this skill

| File | Purpose |
|---|---|
| `scripts/build_laya_dataset.py` | Turns a labelled CSV into `test.jsonl` (final test), `train.jsonl` (training), `heldout.jsonl` (a checking file) and `manifest.json`, and copies the `spec.json` used |
| `scripts/eval_laya.py` | Scores the untrained model (baseline) and, with `--trained`, the trained model on the same test file |
| `assets/snips/` | The bundled practice dataset: source CSVs, `spec.json`, the three built JSONL files and their `manifest.json` |

Run the scripts with Python 3. Where the user runs them elsewhere, such as Kaggle, give them the files to upload.

## Where files go

Treat the skill's own folder as read-only. Never write files into it, or into any agent or app folder such as `.codex`, `.claude` or `.agents`. Users cannot easily find files there, and an update to the skill may delete them.

Everything for the project lives in one folder the user creates, called the project folder below. Before any files are needed, ask in words like these:

> Please create a folder on your computer for this project and give it a name you'll recognise, such as "Laya Training". Then copy its path and paste it here. If you're not sure how to do this, tell me what type of computer you have (for example Windows, Mac or Chromebook) and I'll help.

If the user asks for help, give brief steps for their computer only. On a Chromebook, the folder must be created inside "Linux files" in the Files app (its path is `~/` followed by the folder name); otherwise the skill cannot see it. If you cannot reach the user's computer (for example, in the Claude web app), ask them only to create the folder, without the path, then offer each file for them to save into it. Use the path they paste. Do not choose a location for them.

Once they have shared the path, copy the starter files into the project folder: `scripts/build_laya_dataset.py` and `scripts/eval_laya.py`, and, for the SNIPS practice data, `assets/snips/spec.json`, `snips_train.csv`, `snips_test.csv` and `manifest.json` (rename that last copy `snips_reference_manifest.json`, so it is not confused with the one the user will create). Tell them what each file is. This setup copy is the one thing you do for the user in the beginner path; they run every command themselves. If they are using their own data, ask them to put a copy of their CSV file in the project folder too, so the original stays where it is, untouched.

All commands then run from inside the project folder, using short file names. The project folder ends up holding:

- the starter files above, and the user's own CSV and `spec.json` if they bring their own data;
- `kaggle-upload/`, made by the formatting script: `train.jsonl`, `heldout.jsonl`, `test.jsonl`, `manifest.json` and a copy of `spec.json`. Copy `eval_laya.py` into it too, so the four files to upload to Kaggle are together;
- the evaluation results;
- the model and results zips downloaded from Kaggle, and the unzipped model folder;
- the local prediction script.

## Workflow

1. **Frame the decision.** Write one question as Laya will see it. The build script handles one decision at a time. Prefer a choice question with short, distinct option descriptions. Keep it to 20 options or fewer; for more, split it into two decisions (for example, group and then item within group) or add a shortlist step before Laya. Write criteria as a dictionary of `option_id: description`; the notebook's metrics cell reads `criteria.keys()`.
2. **Get data that resembles the real input.** Match expected inputs in length, style and noise. Aim for at least 30 examples per option, and more for options that are easily confused. Show the data notice above first.
3. **Build the files, keeping the final test set back first.** Write a `spec.json` (see below) and run `python build_laya_dataset.py spec.json examples.csv kaggle-upload` from the project folder. The script removes repeated texts, keeps back `test_share` (default 20%) of each option as `test.jsonl`, then splits the rest into `train.jsonl` and `heldout.jsonl` with a fixed seed. If the user already has a separate set of real test cases, pass it as a fourth argument (`... kaggle-upload test.csv`); the whole file becomes `test.jsonl` and its texts are removed from training. The manifest records row counts, examples per option, removed rows and SHA-256 fingerprints. Read its warnings with the user. `test.jsonl` never goes into training.
4. **Measure the baseline and agree the pass mark before training.** Run `python eval_laya.py kaggle-upload/test.jsonl results_base` from the project folder (no `--trained`) to score the base model and save its predictions. Make **overall accuracy on the final test** the pass mark, with a clear margin over the base model rather than "any improvement" (for example, at least 10 percentage points higher, or removing at least half of the base model's errors if it already scores above 80%). Confidence results are secondary: if you use them, report both coverage (the share of answers above a cut-off) and accuracy among those answers, so a model cannot pass by answering only easy cases. If laya warns that temperatures were clamped, that model's confidence is uncalibrated: treat confidence results as advisory. Do not choose the pass mark after seeing the trained results.
5. **Run the Kaggle notebook** as described below.
6. **Download the model** as described below, into the project folder.
7. **Evaluate** both models on the same test file: `python eval_laya.py kaggle-upload/test.jsonl results --trained laya_finetuned_typed_decisions`. Use the same laya version, `--base` and `--revision` as the notebook. Evaluate on the final test once. Do not use its errors to change the training and rerun.
8. **Report** in plain English: overall correct counts for the untrained and trained models, the change in percentage points, coverage and accuracy at each cut-off (marked advisory if uncalibrated), whether two runs were identical, and the verdict against the pass mark from step 4. If the result is not usable, say so and identify the most likely causes.

## Running the Kaggle notebook

The official notebook is `notebooks/laya_finetune_typed_decisions_2xT4_kaggle.ipynb` in the Laya repository. The user imports it into their own Kaggle account; guide them cell by cell. The changes below were checked against the notebook at commit `fe9a6c35023a7d94102e7feaaeaae8857d9d1b07` with laya 0.4.15. If the headings differ, inspect the current notebook before giving instructions.

**Names.** Suggest names before the user meets the blank fields. For SNIPS: Kaggle dataset `laya-snips-training-data`, notebook `laya-snips-fine-tune`. For the user's own data: `laya-<task>-training-data` and `laya-<task>-fine-tune`, where `<task>` is a short word for their decision, such as `support-routing`. Explain that the dataset is a private input the notebook reads from.

**Settings.** Accelerator GPU T4 x2; internet on for package installation. Confirm that these settings are still available in the user's Kaggle environment.

**Which part of Kaggle.** Kaggle has several panels that look alike to a beginner. Before giving instructions, check which one the user is looking at:

- **Notebook editor:** code and text cells, each with a run button. All the steps below happen here.
- **Dependency Manager:** shows wording such as "Add pip commands here". Do not use it for this skill; guide the user back to the notebook editor.
- **Input panel:** lists attached datasets and files.
- **Output panel:** lists files the notebook has written to `/kaggle/working`.

Make sure `eval_laya.py` is in the `kaggle-upload` folder. Upload `train.jsonl`, `heldout.jsonl`, `test.jsonl` and `eval_laya.py` from `kaggle-upload` to a private Kaggle dataset, and add it to the notebook as an input. The commands below find these files wherever Kaggle places them, so the user does not need to know the folder name. Then make these changes. Give the user each changed line in full.

- **"2. Install Dependencies":** replace the whole cell with this install and check. It pins laya to 0.4.15, the version this skill was tested with, and avoids upgrading packages Kaggle already has. This is an interim install until a full tested package list is published.

  ```python
  # 2. Install and verify the environment
  !pip install -q "laya==0.4.15" "transformers>=4.48.0" "datasets>=3.0.0" safetensors huggingface_hub accelerate tabulate
  import laya, torch, transformers
  print("Laya:", laya.__version__, "| Transformers:", transformers.__version__,
        "| PyTorch:", torch.__version__, "| GPUs:", torch.cuda.device_count())
  assert laya.__version__ == "0.4.15", "Wrong laya version"
  assert torch.cuda.device_count() == 2, "Select the GPU T4 x2 accelerator before training"
  ```

  Pip may print dependency-conflict warnings about other Kaggle packages. They are not fatal if the check above passes. This cell must have passed before any other cell runs, and must be run again after any restart.
- **New cell after section 2, headed "2B. Baseline on the untouched final test set":**

  ```python
  import glob
  EVAL = glob.glob("/kaggle/input/**/eval_laya.py", recursive=True)[0]
  TEST = glob.glob("/kaggle/input/**/test.jsonl", recursive=True)[0]
  !python "{EVAL}" "{TEST}" /kaggle/working/results_base --device cuda
  ```

- **"3. Download & Preprocess Data":** pin the base model and read the uploaded files instead of the original benchmark. First, replace `model_dir = snapshot_download(MODEL_ID)` with:

  ```python
  import laya
  REVISION = laya.PINNED_REVISIONS[MODEL_ID]          # reviewed base revision for this laya version
  model_dir = snapshot_download(MODEL_ID, revision=REVISION)
  ```

  Then replace the `ds_train = load_dataset(...)` line with:

  ```python
  # SPDX-License-Identifier: Apache-2.0
  # Copyright 2026 SimpleCalm Labs Ltd and contributors.
  import glob, hashlib, json

  def read_jsonl(name, expect_sha):
      [path] = glob.glob(f"/kaggle/input/**/{name}", recursive=True)
      got = hashlib.sha256(open(path, "rb").read()).hexdigest()
      rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
      print(name, len(rows), got)
      assert got == expect_sha, f"{name} is not the file that was built"
      return rows

  ds_train = read_jsonl("train.jsonl", "<train sha256 from manifest.json>")
  ```

  Fill in the fingerprint from `manifest.json`. The fingerprint check stops the cell if the uploaded file differs from the one that was built. Also replace two leftover messages from the original benchmark, which would otherwise print "LocalLLaMA/typed-decisions" and "1,200 cases" even though the user's own data is loaded:
  - `print("Downloading LocalLLaMA/typed-decisions (train split)...")` becomes `print("Loading train.jsonl...")`;
  - the `print(f"Preprocessed ...across 1,200 cases.")` line becomes `print(f"Preprocessed {len(items)} training items (skipped {skipped or 'none'}) from {len(ds_train):,} examples.")`.

  The notebook's title cell still describes the original benchmark; the user can edit it or leave it.
- **"4. DDP Training Script":** before the user runs it, explain that this cell writes a helper file, `train_ddp.py`. It prints "Writing" the first time and "Overwriting" on later runs; both are normal. Optionally change `out_cfg["model_name"] = "laya-typed-decisions"` to a name for the user's model, such as `"laya-snips-intent"`. The output folder keeps the name `laya_finetuned_typed_decisions`; it is only a folder name.
- **"6. Run Benchmark Evaluation":** replace the `load_dataset(...)` line with `ds_test = read_jsonl("heldout.jsonl", "<heldout sha256 from manifest.json>")`. This scores the checking file, not the final test.
- **"7. Compute Official Metrics":** the accuracy it prints is valid for the checking file. Ignore the comparison rows for other systems; they describe the original benchmark.
- **"8. (Optional) Push to Hugging Face Hub":** delete this cell unless the user has asked to publish the model.
- **"9. Save Benchmark Report as JSON":** delete this cell. It labels the report as the original benchmark, miscounts the decisions and writes the file into the model folder.
- **New last cell, headed "10. Final test, model checks and downloadable archives":** this cell stands on its own, so it also works after a restart once section 2 has been run again. Fill in the test fingerprint from `manifest.json`.

  ```python
  # SPDX-License-Identifier: Apache-2.0
  # Copyright 2026 SimpleCalm Labs Ltd and contributors.
  import glob, hashlib
  from pathlib import Path
  import laya
  assert laya.__version__ == "0.4.15", "Run section 2 again first"
  found = [Path(p).parent for p in glob.glob("/kaggle/input/**/laya_finetuned_typed_decisions/rl_agent_config.json", recursive=True)]
  MODEL = next((m for m in [Path("/kaggle/working/laya_finetuned_typed_decisions"), *found]
                if (m / "rl_agent_config.json").exists()), None)
  assert MODEL, "No trained model found. See 'If the notebook restarted' before retraining."
  missing = [p for p in ("model.safetensors", "rl_agent_config.json", "encoder", "tokenizer") if not (MODEL / p).exists()]
  assert not missing, f"Model output is incomplete; missing: {missing}"
  EVAL = glob.glob("/kaggle/input/**/eval_laya.py", recursive=True)[0]
  TEST = glob.glob("/kaggle/input/**/test.jsonl", recursive=True)[0]
  assert hashlib.sha256(open(TEST, "rb").read()).hexdigest() == "<test sha256 from manifest.json>", "Wrong test file"
  print("Model:", MODEL)
  !python "{EVAL}" "{TEST}" /kaggle/working/results --device cuda --trained "{MODEL}"
  !cd "{MODEL.parent}" && zip -qr /kaggle/working/laya_model.zip "{MODEL.name}" -x "*/checkpoint_latest/*"
  !cd /kaggle/working && zip -qr laya_results.zip results && unzip -l laya_model.zip
  ```

### Warnings to explain before they appear

- **"You are sending unauthenticated requests to the HF Hub"** (or similar): harmless. The base model is public, so no Hugging Face login is needed.
- **"this checkpoint ships invalid temperatures… Treat confidence… as uncalibrated"**: Laya's confidence numbers for that model are not calibrated. Overall accuracy is still valid; treat confidence cut-offs as advisory. `eval_laya.py` records this in `eval_summary.json`.
- **Pip dependency-conflict warnings**: see section 2 above.
- **"Overwriting /kaggle/working/train_ddp.py"**: normal; see section 4 above.

### Training is finished only when

Run section 10 only after all of these are visible in the training output:

1. `=== Epoch 4/4 Completed ...`
2. `Fitted calibration temperatures ...`, or `Temperature fitting fallback: ...`. A fallback means the trained model's confidence is uncalibrated; accuracy is still valid.
3. `Model successfully saved to /kaggle/working/laya_finetuned_typed_decisions!`

Section 10 then checks that the model folder is complete. The loss figures are a progress signal, not the result: the "Avg Loss" line covers one GPU's share of the data, and a low loss does not show the model works on new examples. Overall accuracy on the final test decides that.

Training takes several minutes or more, depending on data size; the notebook prints the loss every 50 steps and a summary after each of its 4 epochs. The user should stay with an interactive run until it finishes. Do not rely on it continuing through laptop sleep or hibernation. An unattended "Save & Run All" route has not yet been tested for this skill.

### If the notebook restarted

Signs: `ModuleNotFoundError: No module named 'laya'`, `NameError` for a variable such as `EVAL`, or an empty Output panel. A restart loses installed packages and variables, and a new session also loses `/kaggle/working`. This says nothing about whether the model was saved. Before retraining:

1. Run section 2 again and check that it passes.
2. Run section 10. It looks for the model in `/kaggle/working` and in any attached inputs.
3. If the model is not found and the files in `/kaggle/working` are gone, check whether a saved version of the notebook has the model in its output. If so, add that notebook version as an input and run section 10 again.
4. Retrain only if no complete model can be found.

### Downloading the model

Section 10 creates `laya_model.zip` and `laya_results.zip` in `/kaggle/working`. The model zip leaves out `checkpoint_latest`, a rolling copy of the model saved after each epoch. The notebook does not resume exactly from it (it does not save the training state needed for that), so it is not needed once the final model has been checked. `laya_model.zip` must contain `model.safetensors`, `rl_agent_config.json`, and the `encoder/` and `tokenizer/` folders. `model.safetensors` alone cannot be loaded. Download both zips from the notebook's Output panel into the project folder, unzip them there, and point `--trained` or `laya.Agent(...)` at the unzipped `laya_finetuned_typed_decisions` folder. Remove the uploaded Kaggle dataset when it is no longer needed.

## spec.json and row format

Example `spec.json`:

```json
{"workflow": "support_routing", "seed": 13, "test_share": 0.2, "heldout_share": 0.25, "text_column": "text",
 "questions": {"team": {"type": "choice", "instructions": "Which team should take this call?",
   "criteria": {"billing": "Invoices, charges and refunds", "tech": "Faults and access"},
   "label_column": "team"}}}
```

You may also add `source`, `licence`, `licence_checked` and `generating_model` as text fields. When present, they are copied into `manifest.json`, so the record stays with the files. The build script does not require them.

Each output row is one JSON object per line. `state`, `questions` and `gold` are JSON strings, not nested objects:

```json
{"id": "train-00000", "workflow": "support_routing",
 "state": "\"Caller says the invoice was charged twice\"",
 "questions": "{\"team\": {\"type\": \"choice\", \"instructions\": \"Which team should take this call?\", \"criteria\": {\"billing\": \"Invoices, charges and refunds\", \"tech\": \"Faults and access\"}}}",
 "gold": "{\"team\": {\"probabilities\": {\"billing\": 1.0, \"tech\": 0.0}, \"label\": \"billing\"}}"}
```

`id` and `workflow` are needed by the notebook's evaluation cell. The build script produces choice questions only. For score or `noul` (yes/no) questions, use the row format in Laya's [docs/finetune.md](https://github.com/NandhaKishorM/laya/blob/fe9a6c35023a7d94102e7feaaeaae8857d9d1b07/docs/finetune.md).

## Limits to design around

- The build script warns at roughly 350 English words. This is a cautious warning, not a hard limit: the pinned notebook reads up to 1,024 tokens, and the question and option text use part of that. Much longer texts may be cut short.
- Keep choice questions to about 20 options or fewer.
- Graded scores are less reliable than choice questions, and the model is not intended for arithmetic.
- Confidence behaviour may vary with the number of choice options, and Laya may report uncalibrated confidence. Use overall accuracy as the main measure; keep any calibration work on data separate from the final test.
- CPU inference is suitable for evaluation; use a GPU environment for training.

## Housekeeping

- Do not commit model weights, archives or datasets to version control. Add ignore rules before downloading, then verify that version-control status shows only the intended small files.
- Keep the spec, manifest, scripts and results. They record what was done.
- If data or trained weights must later be withdrawn, identify every copy and service that holds them. Get the user's confirmation before deleting anything, especially when rewriting version-control history or removing cloud files.
