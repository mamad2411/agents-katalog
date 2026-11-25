---
name: vlm-multimodal
description: Vision-Language Models (Qwen2.5-VL, Gemma 3, Llama-3.2-Vision, Florence-2, mlx-vlm, llama.cpp mmproj, Ollama vision, Gemini multimodal) with visual token budgeting, video keyframe sampling, structured grounding, and multimodal RAG.
---

# VLM & Multimodal Intelligence (`/vlm-multimodal`)

> **Philosophy**: *Cap visual tokens before encoding, sample keyframes instead of raw video streams, enforce structured grounding schemas, and triage cheap CV/OCR ahead of VLM calls.*

---

## 1. Progressive Disclosure References

| Resource | Purpose |
| :--- | :--- |
| [references/vlm-runtimes-and-visual-tokens.md](references/vlm-runtimes-and-visual-tokens.md) | Local/cloud VLM matrix, `28x28` patch & tile math, `mlx-vlm` / `Ollama` / `Gemini` code, video keyframe sampling. |
| [references/visual-grounding-and-multimodal-rag.md](references/visual-grounding-and-multimodal-rag.md) | Normalized `[ymin, xmin, ymax, xmax]` schemas, ColPali page-image RAG, indirect prompt-injection defense. |
| [scripts/verify_vlm_hygiene.py](scripts/verify_vlm_hygiene.py) | Audits unresized image payloads, unthrottled video frame loops, unconstrained VLM outputs, and missing timeouts. |

---

## 2. Local & Cloud VLM Runtime Matrix

| Runtime / Model | Deployment | Strengths | Visual Token Control |
| :--- | :--- | :--- | :--- |
| **`Qwen2.5-VL` (3B/7B/32B)** | `vLLM` / `Ollama` / `mlx-vlm` / `llama.cpp` | OCR, UI/chart parsing, exact `[x,y]` grounding | Pin `min_pixels` / `max_pixels` (`256*28*28`..`1280*28*28`). |
| **`Gemma 3 Vision` / `Llama-3.2-Vision`** | `Ollama` / `llama-mtmd` (`--mmproj`) | Private local multimodal chat & captioning | Resize long edge `<= 896px` / `1120px` before base64. |
| **`Florence-2` (0.2B–0.7B)** | ONNX / PyTorch / Transformers.js | Ultra-fast `<50ms` captioning, OD, region OCR | Fixed low-res encoder (`768x768`); minimal VRAM. |
| **`Gemini 2.5 Flash / Pro`** | `google-genai` SDK | Long video, native PDF, high-accuracy reasoning | Use `Part.from_bytes` (`<= 1568px`) or File API for video/PDF. |

---

## 3. Visual Token Budgeting Invariants

1. **Resize Before Encode**: Downscale images so the longest edge is `<= 1280px–1568px` (`Image.thumbnail`) before base64/bytes serialization—sending raw 4K PNGs wastes `3–6x` visual tokens with zero accuracy gain on general reasoning.
2. **Keyframe Sampling for Video**: Never loop `VideoCapture.read()` directly into a VLM at 30fps. Sample `<= 1 fps` or gate on pixel/SSIM scene-delta thresholds (`delta > 0.12`), or upload directly via Gemini File API.
3. **Structured Grounding Contracts**: Require `response_schema` / Ollama `format` / GBNF JSON schemas with explicit `0–1000` normalized `[ymin, xmin, ymax, xmax]` coordinates.
4. **CV/OCR Triage First**: If a deterministic detector or OCR engine solves the task at `conf >= 0.85`, skip the VLM call completely (`/ai-integration`).

---

## 4. Automated VLM Hygiene Verification

```bash
python3 skills/vlm-multimodal/scripts/verify_vlm_hygiene.py --path . --strict
```
