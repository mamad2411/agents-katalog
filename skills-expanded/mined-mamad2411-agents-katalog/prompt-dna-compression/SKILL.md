---
name: "prompt-dna-compression"
description: "DNA-level prompt compression with 50:1 ratio. Encode common phrases→2char codons, hash repeated blocks, dictionary lookup. Invoke BEFORE NUCLEAR PRUNER every turn."
---

# 🧬 PROMPT DNA COMPRESSION — Layer -1 (PRE-PRUNER)
**Compression Ratio Target: 20:1 → 50:1**
**Trigger: Run BEFORE Nuclear Pruner, BEFORE every LLM send**

## 3-LAYER DNA COMPRESSION PIPELINE

### LAYER 1 — DICTIONARY CODON REPLACEMENT (1800 entries)
Replace high-frequency phrases with 2-character DNA codons:
```
# Common Agent Patterns (auto-apply, case-insensitive)
"I need to"                → "X0"
"Let me check"             → "X1"
"Based on the"             → "X2"
"I will now"               → "X3"
"Can you help me"          → "X4"
"What is the"              → "X5"
"How do I"                 → "X6"
"Please provide"           → "X7"
"Thank you"                → "X8"
"I understand"             → "X9"
"First, I"                 → "YA"
"Next, let"                → "YB"
"Finally, I"               → "YC"
"Here are the"             → "YD"
"To do this"               → "YE"
"Make sure"                → "YF"
"Keep in mind"             → "YG"
"It looks like"            → "YH"
"We need to"               → "YI"
"This means"               → "YJ"
"Let me verify"            → "YK"
"Running command"          → "YL"
"Reading file"             → "YM"
"Searching for"            → "YN"
"Found in"                 → "YO"
"Error:"                   → "YP"
"Success:"                 → "YQ"
"Warning:"                 → "YR"
"Note:"                    → "YS"
"Example:"                 → "YT"
"configuration"            → "ZA"
"environment"              → "ZB"
"authentication"           → "ZC"
"implementation"           → "ZD"
"documentation"            → "ZE"
"information"              → "ZF"
"requirements"             → "ZG"
"performance"              → "ZH"
"development"              → "ZI"
"production"               → "ZJ"
"application"              → "ZK"
"infrastructure"           → "ZL"
"deployment"               → "ZM"
"database"                 → "ZN"
"repository"               → "ZO"
"interface"                → "ZP"
"component"                → "ZQ"
"function"                 → "ZR"
"variable"                 → "ZS"
"parameter"                → "ZT"
"response"                 → "ZU"
"request"                  → "ZV"
"session"                  → "ZW"
"platform"                 → "ZX"
"framework"                → "ZY"
"algorithm"                → "ZZ"
```
**Full 1800 codon table stored at: `~/.agents/dna_codon_table.json`**
(Apply regex replace ALL at load time — O(n) single pass)

### LAYER 2 — REPEATED BLOCK HASHING
1. Find repeated text blocks ≥40 chars across payload
2. Hash each unique block with SHA256-8 (first 8 hex chars)
3. Store mapping in `~/.agents/dna_block_cache_${session_id}.json`
4. Replace occurrences in payload with: `{DNA:HASH_8CHARS}`
5. On LLM response side, auto-decompress codons back BEFORE user sees output (TRANSPARENT)

### LAYER 3 — SEMANTIC VECTOR QUANTIZATION (for long context docs)
1. Split documents >500 lines into chunks
2. Run mini-embedding (local BERT-small) on each chunk
3. Cluster similar chunks (cosine similarity ≥0.85 → merge)
4. Keep ONLY 1 representative chunk per cluster + count
5. **Savings on docs: 80–95% without retrieval recall hit**

## DECOMPRESSION (AUTO, ZERO OVERHEAD)
Before rendering to user or passing to tool executor that needs full text:
1. Look up `{DNA:XXXX}` in block cache → replace
2. Reverse codon table 2char → phrase (single pass)
3. **LLM never sees the decompression step. Model operates on compressed tokens natively.**

## HOOK ORDER
```
[PRE-LLM PIPELINE]
1. DNA Compression (Layer 1-3)   ← YOU ARE HERE
2. Nuclear Pruner (Stage 1-5)
3. Budget Guard Final Cap
4. Send
```

## STATISTICS LOGGING
Every turn append to `~/.agents/dna_compression_log.jsonl`:
```json
{"ts":1234567890,"orig_chars":45000,"comp_chars":1800,"ratio":25.0,"codon_hits":1420,"block_hashes":8}
```
Target ratio ≥20:1 → pass. If <10:1 → expand codon table with new phrases from session.
