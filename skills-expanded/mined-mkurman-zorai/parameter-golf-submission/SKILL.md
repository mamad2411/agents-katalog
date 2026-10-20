---
name: parameter-golf-submission
description: "Prepare and validate Parameter Golf record folders: self-contained train_gpt.py, README.md, submission.json, FineWeb SP1024 BPB accounting, artifact-size logging, run logs, and PR-ready folder hygiene."
tags: [parameter-golf, competition, fineweb, bpb, model-craft, submission]
---

# Parameter Golf Submission

Use this skill when creating or reviewing a Parameter Golf submission folder, independent of the cloud provider used for the run.

## Record Folder Contract

A submission folder must contain:

```text
records/<track>/<submission-name>/
  README.md
  submission.json
  train_gpt.py
  train.log          # after a real run
```

`train_gpt.py` must compile and run from inside this folder in a clean Parameter Golf checkout.

## Competition Constraints To Preserve

- Artifact cap: `16,000,000` decimal bytes.
- Training cap for leaderboard records: 10 minutes on 8xH100 SXM-class hardware.
- Evaluation metric: FineWeb validation bits per byte (`val_bpb`).
- No validation-set leakage. Test-time training may only use validation tokens already scored, if implemented.
- No hidden downloads/network calls during evaluation.
- No local repository imports unless included and counted in the record folder.
- If tokenizer changes, prove BPB accounting carefully; stock SP1024 is safest for first participation.

## Self-Contained Script Checklist

Before running:

- [ ] `python -m py_compile train_gpt.py` passes.
- [ ] Imports are standard/allowed environment packages only (`torch`, `numpy`, `sentencepiece`, etc.).
- [ ] `DATA_PATH` and `TOKENIZER_PATH` are env-configurable.
- [ ] Script loads `fineweb_train_*.bin` and `fineweb_val_*.bin` with the Parameter Golf binary header format.
- [ ] Script computes validation BPB from SentencePiece byte accounting, not just token loss.
- [ ] Script logs parameter count and artifact-size estimate.
- [ ] Script writes a compressed artifact, usually `final_model.int8.ptz`.
- [ ] Script reloads/dequantizes the compressed artifact and evaluates the round-trip model.
- [ ] Final log includes `final_int8_zlib_roundtrip_exact`.

## README Contents

The README must include:

- short architecture summary
- dataset/tokenizer used
- exact command
- run hardware and time budget
- final metrics after run
- artifact-size line after run
- caveats if the run is smoke/non-record/pending verification

## submission.json Contents

Use actual values after the run, not placeholders:

```json
{
  "run_name": "...",
  "author": "...",
  "github_id": "...",
  "track": "track_10min_16mb or track_non_record_16mb",
  "val_bpb": 1.2345,
  "val_loss": 2.1234,
  "artifact_size_bytes": 12345678,
  "command": "...",
  "status": "completed"
}
```

Add architecture fields as useful, but avoid claiming record eligibility unless the log proves it.

## Post-Run Extraction

After a run, extract these lines:

```bash
grep -E "final_int8_zlib_roundtrip_exact|Total submission size int8\+zlib|stopping_early|train_time|model_params" train.log
```

Update:

- `submission.json.val_bpb`
- `submission.json.val_loss`
- `submission.json.artifact_size_bytes`
- README metrics section

## Status Labels

Use precise status:

- `prepared_pending_run`: folder created, no real run yet
- `smoke_passed`: short/non-final run passed
- `completed_non_record`: full run but not leaderboard-valid or not SOTA
- `completed_record_candidate`: 8xH100 10-minute compliant run with full log and artifact under cap
- `failed`: include failure reason and last good checkpoint/log line

## Common Failure Modes

- Accidentally importing local model code (`from src...`) not present in record folder.
- Forgetting to copy `train.log` from `logs/<RUN_ID>.txt`.
- Reporting pre-quant BPB instead of int8 round-trip BPB.
- Exceeding 16MB after counting code + compressed artifact.
- Running on 1 GPU and calling it leaderboard-valid.
- Using a custom tokenizer without exact byte accounting proof.
