# Protein Language Model Function Analysis Starter

Use this skill to validate protein FASTA inputs, extract deterministic smoke-safe embeddings, and run a reusable sequence-to-function triage flow that can later be swapped onto real ESM-2 or ProtT5 backends.

## What This Skill Does

- reads protein sequences from FASTA and rejects unsupported residue symbols
- emits per-sequence embeddings to a TSV contract
- runs centroid-based function analysis when labels are supplied
- reports nearest-neighbor structure in embedding space
- preserves a stable CLI for real `transformers` backends such as ESM-2 and ProtT5

## When To Use It

- when you need a concrete local skill for `protein-embeddings` and `sequence-to-function-modeling`
- when you want a deterministic smoke path before moving to GPU-backed protein language model inference
- when you need a compact handoff artifact for downstream DeepFRI, annotation, or benchmarking work

## Run

```bash
python3 skills/proteomics/protein-language-model-function-analysis-starter/scripts/run_protein_language_model_function_analysis.py \
  --input skills/proteomics/protein-language-model-function-analysis-starter/examples/toy_sequences.fasta \
  --labels skills/proteomics/protein-language-model-function-analysis-starter/examples/toy_labels.tsv \
  --config skills/proteomics/protein-language-model-function-analysis-starter/examples/analysis_config.json \
  --embeddings-out scratch/protein-lm/toy_embeddings.tsv \
  --summary-out scratch/protein-lm/toy_summary.json
```

## Notes

- The default `mock` backend is intentionally deterministic and test-friendly. It preserves the same file contract as a real protein language model run.
- For live model inference, switch the backend to `transformers` and point `model_id` at an ESM-2 or ProtT5 checkpoint. See [`refs.md`](refs.md) for canonical sources and formatting notes.
- The bundled toy labels are illustrative and suitable only for smoke testing or pipeline scaffolding, not biological claims.
