# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Research Goal

This subproject (`quant_protection/`) studies a single question: **when an in-memory vector index suffers bit flips (DRAM soft error / Rowhammer / storage corruption), is a *quantized* index more sensitive to recall loss than full precision?** Prior bit-flip / silent-data-corruption work in neural nets gives contradictory answers depending on fault model (floats collapse under EM injection; quantized nets resist targeted bit-flip attacks). No one has resolved this for vector retrieval. Existing vector-DB reliability work (e.g. P-HNSW) addresses crash consistency, not silent corruption's effect on recall.

`prompt.txt` is the authoritative research design (Traditional Chinese). Read it before doing experiment work — it defines the design matrix, controlled variables, and execution phases. Key principles encoded there:
- **Isolate the encoding variable**: hold the IVF structure fixed and swap only the encoding (IVF_FLAT vs SQ8 vs PQ) so algorithm differences aren't miscounted as quantization differences. FLAT↔HNSW isolates graph structure.
- **Normalize by physical error rate (faults/MB)** as the primary axis — not "how many bits flipped" — because hardware delivers a per-bit error rate, and a quantized index carries more weight per bit but has a smaller footprint. The net effect is the open question.
- **Single-bit sensitivity map first, then error-rate sweep**; report both traditional and tolerant/semantic recall so benign neighbor reshuffling isn't overcounted as recall loss.

This is the sibling of `../first-try/` (HNSW node-failure / cascade study); the `Q3` redundancy comparison connects back to that project's "graph damage only affects speed" finding. The parent `../CLAUDE.md` documents `first-try/`.

## Environment

```bash
bash setup.sh                 # idempotent: build .venv (system python3), install deps, verify
source .venv/bin/activate
```

`setup.sh` is the single entry point (`install.sh` is a deprecated redirect to it). It creates `.venv` from system `python3` (whatever the host ships), installs `requirements.txt`, checks the SIFT1M files exist, then runs `verify_env.py`. Re-running is safe — an existing `.venv` is reused.

`python verify_env.py` is the smoke test: prints library versions, reads the SIFT base header, runs FlatL2 + IVFFlat searches, exercises the **serialize → flip one bit → deserialize round-trip** (the foundation of the whole corruption-injection method), and a hnswlib query. Exits non-zero on any failure. Run it after changing dependencies.

## Tooling Decisions (already made — don't re-litigate)

- **FAISS (`faiss-cpu==1.14.2`) is the workhorse.** A single package covers the entire design matrix and exposes internal bytes for bit-flipping:
  - FLAT → `IndexFlatL2`; IVF_FLAT → `IndexIVFFlat`; IVF_SQ8 → `IndexIVFScalarQuantizer` (QT_8bit); IVF_PQ → `IndexIVFPQ` (M=8/16, nbits=8); HNSW → `IndexHNSWFlat`; HNSW_SQ8 → `IndexHNSWSQ`.
- **`hnswlib`** is kept only as a fp32-HNSW cross-check.
- **No C++ build / no git clone** — everything is a pip wheel (deliberate choice; unlike `first-try/` which builds hnswlib from source). FlatNav and RaBitQ/binary are optional/not installed.
- **System `python3`**, whatever the host ships — 3.13 originally, 3.12.3 on the current box after
  the interpreter was removed from it. Not pinned: `faiss-cpu==1.14.2` ships a `cp310-abi3` wheel and
  the rest are pure-Python or have wheels for both, so the venv rebuilds on either. A `.venv` built for
  a since-removed interpreter fails as `No module named numpy` — delete it and re-run `setup.sh`.

## Bit-Flip Injection Method

The core technique is **numpy on serialized index bytes**: `faiss.serialize_index(index)` → numpy `uint8` array → XOR a bit at a chosen byte/position → `faiss.deserialize_index(buf)`. `verify_env.py` proves this round-trip works. Targeting specific structures (codes vs codebook/centroid/SQ-scale vs graph edges vs entry-point/metadata) means flipping bits in the corresponding byte regions of that buffer. For fp32 indexes, also track sign/exponent/mantissa bit position.

## Dataset

SIFT1M lives in `sift/` (binary fvecs/ivecs; each vector prefixed by an int32 dim count, then `dim` float32/int32):
- `sift_base.fvecs` — 1M × 128-dim float32 (~492MB; `verify_env.py` reads only the first 10k rows to stay fast)
- `sift_query.fvecs` — 10K queries
- `sift_groundtruth.ivecs` — 10K × 100 true neighbors

`read_fvecs()` in `verify_env.py` is the reference loader (reads header dim, reshapes to `(N, dim+1)`, drops the leading dim column). Reuse it. GIST1M (960d) and a text embedding set (~768d) are in the design for generalization but **not yet downloaded** — only SIFT1M is present.

## Experiment Status & Conventions

Phases 0–3 (build indexes & align clean recall ≈0.95; single-bit sensitivity map; error-rate sweep r ∈ {1e-6…1e-3} normalized by faults/MB; failure-mode analysis) are **not yet written** — only the environment exists so far. When implementing, honor the controlled variables from `prompt.txt`:
- Fixed query set (10k), k=10, fixed ground truth.
- IVF family shares `nlist` (1024) and `nprobe`; graph indexes share `M` (16/32), `efConstruction`, `efSearch`.
- **Tune each index's *clean* recall to the same operating point (~0.95) before comparing** — the study measures *sensitivity*, not each index's own baseline.
- **refine / re-rank is OFF by default** — it re-ranks with original fp32 and would rewrite the corruption story; treat it as a separate condition if ever enabled.
- Each cell: 30–100 random fault placements, report mean ± 95% CI.
- Separately count three failure modes: **silent-wrong / nan-inf / crash**.
