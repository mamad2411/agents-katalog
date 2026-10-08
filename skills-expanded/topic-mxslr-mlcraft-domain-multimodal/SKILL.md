---
name: domain-multimodal
description: "Use for vision-language and multimodal tasks: image-text retrieval, zero-shot image classification, visual question answering (VQA), image captioning, document or chart understanding, and visual grounding. Picks a contrastive dual-encoder or an instruction-tuned VLM, and uses task-appropriate evaluation. Triggers on 'vision language', 'image and text', 'CLIP', 'VQA', 'visual question answering', 'image captioning', 'multimodal', 'describe an image', 'document understanding', 'zero-shot image'."
---

# Multimodal (Vision-Language) - Method Selection

Try zero-shot first. Pretrained models often work with no training.

## Decision table
| Task | Recommended | Notes |
|---|---|---|
| Zero-shot classification or image-text retrieval | CLIP or SigLIP (contrastive dual-encoder) | embeddings plus cosine similarity; build an approximate nearest neighbor index for retrieval. |
| VQA, captioning, visual chat | BLIP-2 (Q-Former plus a frozen LLM) or a LLaVA-family model | instruction-tuned; adapt parameter-efficiently. |
| Fine detail, documents, or charts | a high-resolution VLM or a document-specialized model | small text and layout need high input resolution. |
| Custom domain adaptation | LoRA on the VLM, or fine-tune CLIP with a contrastive loss | small data. |

## Cross-cutting practice
- Prompt design matters for VLMs. Start zero-shot and only fine-tune if it is insufficient.
- Metrics: retrieval uses Recall@K; zero-shot classification uses accuracy; VQA uses VQA accuracy (open-ended VQA needs an LLM judge plus human checks); captioning uses CIDEr, SPICE, or BLEU plus human review.
- Caveats: VLMs hallucinate, so evaluate faithfulness. Deduplicate to avoid train and test image overlap.
- Explainability: cross-attention or grounding maps (which region the answer used), and retrieved neighbors for retrieval.
- Improve results: use `accuracy-improvement-loop`; evaluate with `rigorous-evaluation`.
