---
name: ai-science-vision-rag
description: "ColPali-style Vision RAG: embed rendered PDF pages, retrieve via ColBERT MaxSim, feed top-k pages to Qwen2-VL, no OCR. Use for PDF/document QA over figures and tables, multimodal retrieval, or Recall@k/MRR eval."
tool_type: python
primary_tool: transformers
---

# Vision RAG for Document Understanding (ColPali-Style)

**Attribution:** Patterns inspired by Unsloth AI and Manuel Faysse (ColPali) Vision RAG tutorials.

## When to Use

- Building RAG over PDFs, scientific papers, or clinical reports where figures, tables, and layout carry information that text extraction/OCR would destroy
- Need to retrieve relevant document *pages as images* and hand them to a VLM instead of chunking extracted text
- Implementing or debugging ColPali/ColBERT-style late-interaction (MaxSim) retrieval scoring
- Evaluating retrieval quality (Recall@k, MRR, NDCG) for a document-page retriever
- Deciding between single-vector (CLIP-style) page embeddings and multi-vector late interaction

## Version Compatibility

`transformers` >=4.45, `qwen-vl-utils` >=0.0.8, `torch` >=2.1, Python >=3.10, `Qwen/Qwen2-VL-7B-Instruct` checkpoint. For production ColPali retrieval use `colpali-engine` >=0.3 (PaliGemma-2 backbone). Code below simulates embeddings with NumPy to teach the scoring math without requiring a GPU.

## Prerequisites

```bash
pip install transformers accelerate qwen-vl-utils torch numpy pillow matplotlib
```

GPU with >=16GB VRAM is required only for actual Qwen2-VL/ColPali inference — the retrieval-math and simulation code below runs on CPU. Familiarity with embeddings/cosine similarity and standard text RAG (chunk → embed → vector store → top-k) is assumed.

## VLM Architecture

A VLM combines:
1. **Visual encoder** — ViT processes image patches
2. **Projection layer** — maps visual tokens into the LLM embedding space
3. **LLM decoder** — generates text conditioned on visual + text tokens

**Key VLMs (2024–2025):**
| Model | Size | Strengths |
|---|---|---|
| Qwen2-VL | 2B, 7B, 72B | Multi-image, long context, document understanding |
| LLaVA-1.6 | 7B, 13B, 34B | Strong OCR, open weights |
| InternVL2 | 2B–76B | High benchmark scores |
| PaliGemma | 3B | Compact, versatile |

## Vision RAG vs Text RAG

**Standard text RAG:** chunk → embed → vector store → retrieve top-k → LLM

**Vision RAG (ColPali-style):**
1. Render each PDF page as an image
2. Embed pages with a multimodal model → page embedding matrix (one row per patch)
3. At query time: embed query text → compute MaxSim against every page matrix
4. Retrieve top-k pages → feed as images to a VLM
5. VLM generates the answer directly from visual context

**Advantage:** no OCR step — layout, tables, and figures are preserved natively. ColPali reports ~81 NDCG@5 on the ViDoRe benchmark vs ~66 for the best OCR+text-embedding baseline (arXiv:2407.01449, Table 2).

**Goal:** turn a folder of "PDF pages" into retrievable images for the pipeline below.
**Approach:** render synthetic pages with PIL (stand-in for `pdf2image`/`fitz` page rendering) so the retrieval math can be demoed without a real PDF corpus.

```python
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import warnings
warnings.filterwarnings("ignore")

plt.rcParams.update({"figure.dpi": 110})

def create_synthetic_page(text_content, page_num, width=595, height=842):
    """Render a synthetic PDF page as a PIL Image (stand-in for pdf2image.convert_from_path)."""
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([40, 40, width - 40, 90], fill="#f0f0f0")
    draw.text((50, 55), f"Document Page {page_num}", fill="black")

    # Body text
    y = 110
    for line in text_content.split("\n")[:20]:
        draw.text((50, y), line[:80], fill="black")
        y += 25
        if y > height - 60:
            break

    # Simulated figure box
    draw.rectangle([50, height // 2, width - 50, height // 2 + 200], outline="#888", width=2)
    draw.text((width // 2 - 60, height // 2 + 90), f"[Figure {page_num}]", fill="#888")

    return img

pages_content = [
    "Introduction to RNA-seq\n\nRNA sequencing quantifies gene expression\ngenome-wide.\nPipeline: library prep -> Illumina sequencing ->\nQC (FastQC) -> alignment (STAR) -> counting\n(featureCounts) -> DE testing (DESeq2).",
    "Methods: Differential Expression\n\nWe used DESeq2 for differential expression.\nNormalization: median of ratios method.\nModel: negative binomial GLM.\nFDR threshold: 0.05 (Benjamini-Hochberg).\nLog2FC threshold: 1.0. Genes tested: 25,000.\nDE genes identified: 1,247.",
    "Results: Top DE Genes\n\nUpregulated (n=743): MYC log2FC=3.2 padj=1e-45;\nVEGFA log2FC=2.8 padj=2e-38; HIF1A log2FC=2.1.\nDownregulated (n=504): TP53 log2FC=-2.4;\nRB1 log2FC=-1.9.",
    "Discussion\n\nHypoxic response pathway activation is consistent\nwith HIF1A/VEGFA upregulation and TP53/RB1 loss\nin this cancer subtype. Future work: single-cell\nvalidation.",
    "Methods: GWAS Analysis\n\nGenotypes from 10,000 samples. QC: MAF > 0.01,\nHWE p > 1e-6. Population stratification corrected\nwith top 10 PCs. Test: logistic regression.\nGenome-wide significance: p < 5e-8.",
]

pages = [create_synthetic_page(content, i + 1) for i, content in enumerate(pages_content)]
print(f"Created {len(pages)} synthetic document pages")
```

## ColPali: Late-Interaction Retrieval (MaxSim)

**Single-vector (CLIP-style):** compresses a whole page into one vector → loses spatial/layout detail.

**Late interaction (ColPali/ColBERT-style):**
```text
query → Q matrix (n_tokens x dim)
page  → P matrix (n_patches x dim)
score = sum_i max_j( Q[i] . P[j] )    <- MaxSim
```
Each query token independently finds its best-matching page patch, so spatial detail in the page is preserved instead of averaged away.

- **196 patches**: a 224x224 image / 16x16 px patches = 196 patches. Qwen2-VL instead uses dynamic resolution (patch count scales with image size).
- **MaxSim is directional**: it is query→page (max over patches per query token), not a symmetric similarity — don't swap the `.max(axis=...)` axis.
- **ColPali training**: a PaliGemma-2 backbone fine-tuned contrastively on (query, relevant page) pairs from the ViDoRe benchmark.

**Goal:** score each page's relevance to a text query using ColBERT-style MaxSim.
**Approach:** represent the query as (n_tokens, dim) and each page as (n_patches, dim); MaxSim is a matmul + row-wise max + sum — no external retrieval library needed.

```python
DIM = 128
N_Q_TOKENS = 32
N_PATCHES = 196  # 14x14 patches for a 224x224 image

def simulate_page_embedding(page_idx, n_patches=N_PATCHES, dim=DIM, seed=None):
    """Simulate L2-normalized page-patch embeddings (stand-in for a real ColPali forward pass)."""
    r = np.random.default_rng(seed or page_idx)
    emb = r.normal(0, 1, (n_patches, dim))
    emb /= np.linalg.norm(emb, axis=1, keepdims=True)
    return emb

def simulate_query_embedding(query_text, n_tokens=N_Q_TOKENS, dim=DIM):
    """Simulate L2-normalized query-token embeddings, deterministic per query string."""
    seed = sum(ord(c) for c in query_text) % 10000
    r = np.random.default_rng(seed)
    emb = r.normal(0, 1, (n_tokens, dim))
    emb /= np.linalg.norm(emb, axis=1, keepdims=True)
    return emb

def maxsim_score(query_emb, page_emb):
    """ColBERT MaxSim: for each query token, take the max similarity to any page patch, then sum."""
    scores = query_emb @ page_emb.T   # (n_q, n_p)
    return scores.max(axis=1).sum()   # sum of per-token maxima

# Simulate relevance: page 2 (index 1) is relevant to the differential-expression query
page_embeddings = [simulate_page_embedding(i) for i in range(5)]

relevant_features = simulate_query_embedding("differential expression DESeq2").mean(0)
page_embeddings[1][:10] += relevant_features[:DIM] * 3
page_embeddings[1][:10] /= np.linalg.norm(page_embeddings[1][:10], axis=1, keepdims=True)

query = "What normalization method was used for differential expression?"
query_emb = simulate_query_embedding(query)
scores = [maxsim_score(query_emb, pe) for pe in page_embeddings]
ranked = sorted(range(5), key=lambda i: -scores[i])

print(f"Query: '{query}'")
for rank, page_idx in enumerate(ranked):
    print(f"  Rank {rank + 1}: Page {page_idx + 1} (score = {scores[page_idx]:.3f})")
print(f"Recall@1: {int(ranked[0] == 1)}")
```

## Full RAG Pipeline

**Goal:** go from a raw query string to the page images that would be fed to a VLM.
**Approach:** embed the query, rank pages by MaxSim, keep top-k, and pass those page images (not text) downstream.

```python
def simple_rag_pipeline(query, pages, page_embeddings, top_k=2, verbose=True):
    """
    1. Embed query
    2. Retrieve top-k pages by MaxSim
    3. (In production) feed pages[top_idx] as images to a VLM alongside the query
    """
    query_emb = simulate_query_embedding(query)
    scores = [maxsim_score(query_emb, pe) for pe in page_embeddings]
    top_idx = sorted(range(len(scores)), key=lambda i: -scores[i])[:top_k]

    if verbose:
        print(f"Query: '{query}'")
        print(f"Retrieved pages: {[i + 1 for i in top_idx]}")
        print(f"Scores: {[f'{scores[i]:.2f}' for i in top_idx]}")

    context_summary = " | ".join(pages_content[i][:80] for i in top_idx)
    return {
        "retrieved_pages": [i + 1 for i in top_idx],
        "scores": [scores[i] for i in top_idx],
        "simulated_context": context_summary,
    }

for q in ["What normalization method was used?", "Which genes were upregulated?", "What was the GWAS sample size?"]:
    result = simple_rag_pipeline(q, pages, page_embeddings, top_k=2)
    print()
```

## Evaluating Retrieval Quality

**Goal:** quantify whether the retriever surfaces the right page(s), not just eyeball rankings.
**Approach:** Recall@k (is the relevant page in the top-k?) and MRR (how high does the *first* relevant page rank?) over a labeled query set.

```python
def recall_at_k(ranked_page_indices, relevant_page_idx, k):
    """Fraction check: is relevant_page_idx within the top-k ranked pages for one query?"""
    return int(relevant_page_idx in ranked_page_indices[:k])

def mean_reciprocal_rank(ranked_page_indices, relevant_page_idx):
    """1 / rank of the first relevant page (0 if not found)."""
    if relevant_page_idx in ranked_page_indices:
        rank = ranked_page_indices.index(relevant_page_idx) + 1
        return 1.0 / rank
    return 0.0

queries_and_relevant = [
    ("What normalization method was used?", 1),   # page 2, 0-indexed
    ("Which genes were upregulated?", 2),          # page 3
    ("What was the GWAS sample size?", 4),         # page 5
]

for k in (1, 3, 5):
    recalls = []
    for q, relevant_idx in queries_and_relevant:
        q_emb = simulate_query_embedding(q)
        s = [maxsim_score(q_emb, pe) for pe in page_embeddings]
        ranked = sorted(range(5), key=lambda i: -s[i])
        recalls.append(recall_at_k(ranked, relevant_idx, k))
    print(f"Recall@{k}: {np.mean(recalls):.2f}")
```

## Qwen2-VL Inference Pattern (GPU required)

**Goal:** answer a question using the retrieved page *images* directly, with no OCR.
**Approach:** pass a list of PIL images plus the question through Qwen2-VL's chat template; `qwen_vl_utils.process_vision_info` handles per-image dynamic resolution.

```python
# Install (Colab): pip install -q transformers accelerate qwen-vl-utils

from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
import torch

model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto",
    attn_implementation="flash_attention_2",  # requires flash-attn on Ampere+ GPUs
)
processor = AutoProcessor.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct",
    min_pixels=256 * 28 * 28,
    max_pixels=1280 * 28 * 28,
)

def answer_from_pages(pages, question):
    """Answer a question by feeding retrieved document-page images (no OCR) to Qwen2-VL."""
    content = [{"type": "image", "image": page} for page in pages]
    content.append({"type": "text", "text": question})

    messages = [{"role": "user", "content": content}]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(text=[text], images=image_inputs, padding=True,
                        return_tensors="pt").to(model.device)

    with torch.no_grad():
        ids = model.generate(**inputs, max_new_tokens=512, temperature=0.1, do_sample=False)

    # Decode only the newly generated tokens
    answer = processor.decode(ids[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    return answer
```

## Pitfalls

- **Simulation vs production**: `simulate_page_embedding`/`simulate_query_embedding` are random-vector stand-ins for teaching MaxSim math — swap in a real `colpali-engine` or Qwen2-VL forward pass before trusting retrieval scores on real documents.
- **MaxSim is directional**: it maxes over the *page* axis for each *query* token (`scores.max(axis=1)`); flipping the axis silently computes the wrong (page→query) score.
- **Don't force-resize pages to a fixed square**: distorting aspect ratio to fit a fixed patch grid corrupts tables/figures — let the processor's dynamic-resolution logic (`min_pixels`/`max_pixels`) handle varying page sizes.
- **Context blowup**: each page can cost ~1000+ visual tokens; feeding many high-res pages to a VLM in one prompt exhausts context fast — keep `top_k` small (2–4) and only escalate if recall is poor.
- **`flash_attention_2` requires the `flash-attn` package and an Ampere+ GPU**; drop `attn_implementation` (or set `"sdpa"`) on older/CPU hardware.
- **Multiple testing / batch effects** mentioned in retrieval eval metadata (e.g. DE gene counts in the synthetic pages) are illustrative content only — don't treat the synthetic document text as real biological findings.

## See Also

- `document-rag` — text-based RAG pipeline for non-visual documents
- `vision-language-models` — general VLM usage beyond retrieval
- `generative-imaging` — image generation/diffusion counterpart
- `ai-science-llm-finetuning` — fine-tuning the VLM/LLM components used here
