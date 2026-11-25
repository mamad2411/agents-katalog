---
name: tokenizer-trainer
description: Train and evaluate BPE tokenizers for from-scratch LLM pretraining with HF-compatible outputs.
---

# Tokenizer Trainer (BPE)

Use this skill to train a tokenizer for **new model pretraining**.
Tokenizer quality is treated as a first-class performance lever, not an afterthought.

## Defaults

- Preferred algorithms: BPE via Hugging Face `tokenizers` or SentencePiece BPE.
- Vocabulary size must be user-configurable in the **32K to 50K** range.
- Train on cleaned corpus samples representative of final pretraining distribution.

## Required Special Tokens

Always include these special tokens:

- `<BOS>`
- `<EOS>`
- `<PAD>`
- `<UNK>`

Keep ids stable once training starts to avoid checkpoint/tokenizer mismatch.

## Training Procedure

1. Sample training text from balanced cleaned corpus.
2. Normalize text consistently with downstream data loader assumptions.
3. Train candidate tokenizer(s) with multiple vocab sizes when needed.
4. Compare compression efficiency, OOV behavior, and domain fragmentation.
5. Select final tokenizer and freeze artifacts for training.

## Evaluation Checklist

- Token-per-byte ratio and sequence length distribution.
- Domain-specific tokenization quality (e.g., code, math, biomedical terms).
- Unknown token pressure and fragmentation hotspots.
- Compatibility with model context window and training throughput goals.

## Output Format (HF-Compatible)

Export artifacts in Hugging Face-compatible layout:

- `tokenizer.json`
- `tokenizer_config.json`
- `special_tokens_map.json`
- `vocab.json` + `merges.txt` (for BPE where applicable)

Optionally include a small validation report (`tokenizer_report.md`) with metrics and chosen settings.

## Handoff Protocol

After training is complete, produce a handoff summary for the **model-architect** skill:

- `vocab_size` (exact integer)
- special token IDs (`bos_token_id`, `eos_token_id`, `pad_token_id`, `unk_token_id`)
- `special_tokens_map.json` path
- recommended `max_position_embeddings` based on tokenizer sequence length analysis

The model-architect must import these values into `config.json` to ensure tokenizer-model compatibility.

## Tools/Libraries

- Hugging Face `tokenizers`
- `sentencepiece` (BPE mode)
- `transformers` (for compatibility checks)
