---
name: domain-generative
description: "Use for generative modeling of images and audio: text-to-image, image editing or image-to-image, unconditional image generation, inpainting, super-resolution, style transfer, and audio or music generation, including fine-tuning or personalizing a base model. Picks diffusion vs GAN, the right adaptation method, and generation-specific evaluation. For text generation use domain-nlp-llm instead. Triggers on 'generate images', 'text to image', 'diffusion', 'stable diffusion', 'GAN', 'image editing', 'inpainting', 'super resolution', 'synthesize', 'DreamBooth', 'LoRA image'."
---

# Generative Models - Method Selection

Prefer fine-tuning a strong pretrained base over training from scratch. Use classifier-free guidance for text alignment.

## Decision table
| Sub-task | Recommended | Notes |
|---|---|---|
| Text-to-image or general image generation | latent diffusion (Stable Diffusion family, SDXL) | diffusion now beats GANs on quality and diversity. |
| Personalize or customize on a few images | LoRA, DreamBooth, or textual inversion on a diffusion base | parameter-efficient, small data. |
| Fast or real-time, or paired image-to-image | GAN (pix2pix, StyleGAN) or a distilled diffusion model | GANs are faster at inference. |
| Inpainting or super-resolution | diffusion inpainting, Real-ESRGAN | |
| Audio or music generation | diffusion, or a transformer LM over audio tokens | |

## Cross-cutting practice
- Metrics: FID and KID (fidelity and diversity versus real data), CLIP score (text-image alignment), IS. For personalization, measure subject fidelity and prompt fidelity separately. Automatic metrics are weak proxies, so human evaluation remains essential. Do not judge on a single number.
- Caveats: generated data can carry artifacts, so training a downstream model on synthetic data can hurt. Watch for training-data memorization, plus licensing and safety.
- Explainability: cross-attention maps (which words drove which region) and guidance-scale sweeps.
- Recent bases (2024): SD3 and FLUX text-to-image, plus consistency and distilled models for fast few-step sampling.
- Improve results: use `accuracy-improvement-loop`; evaluate with `rigorous-evaluation` (generation metrics plus human review).
