---
name: qwen-image
description: Generate new high-quality images locally with Qwen-Image-2.1 (20B DiT + Qwen3-VL 8B) on ROCm / AMD Strix Halo APU via ComfyUI. Use for /qwen-image and text-to-image requests, including game concept art, techwear, anime, characters, and complex scenes with native Chinese and English prompt understanding.
---

# Qwen Image Generation

Generate high-fidelity images locally using **Qwen-Image-2.1** (20B Diffusion Transformer + Qwen3-VL 8B Multimodal Text Encoder + 64-channel RGBA native transparency VAE) via local ComfyUI API on AMD ROCm / Strix Halo.

> [!NOTE]
> This skill is dedicated solely to **Qwen-Image-2.1** and does **NOT** require FLUX.2 or Anima.

---

## 🚀 Quick Run

Run the deployed CLI script:

```bash
python3 ~/.hermes/skills/qwen-image/scripts/qwen_image.py "YOUR PROMPT" [OPTIONS]
```

The script outputs clean JSON on stdout. In chat or Discord replies, attach the resulting image path using:

```text
[[image: /absolute/path/to/result.png]]
```

*(Or provide clickable Markdown links: `[filename](file:///absolute/path/to/result.png)`)*

---

## ⚙️ Options & Parameter Reference

| Flag | Short | Description | Default |
|---|---|---|---|
| `prompt` | | Text prompt (Traditional Chinese, Simplified Chinese, or English) | *Required* |
| `--aspect-ratio` | `-a` | Aspect ratio: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `3:2`, `2:3`, `21:9` | `16:9` |
| `--seed` | `-s` | Random seed for deterministic generation | Random |
| `--steps` | | Sampling steps (Flow Matching Euler Simple) | `25` (or `30` for native-1080p) |
| `--cfg` | | Classifier-Free Guidance scale | `1.0` |
| `--base-only` | `--fast` | Fast draft: output raw base latent without Lanczos upscaling | `False` |
| `--native-1080p` | | Direct unscaled 1080p latent (~350s runtime) | `False` |
| `--negative-prompt`| `-n` | Negative prompt for anatomical suppression | *(Built-in hand/anatomy filter)* |
| `--output-dir` | `-o` | Output directory | `/home/chihmin/models-work/flux2/output/qwen-image` |
| `--prefix` | `-p` | Filename prefix | `qwen21` |
| `--comfy-url` | | ComfyUI API endpoint | `http://127.0.0.1:8188` |
| `--timeout` | | Generation timeout in seconds | `600.0` |

---

## 📐 Aspect Ratios & Acceleration Architecture

Qwen-Image-2.1's Self-Attention computational complexity is $O(N^2)$ on latent tokens. Generating native 1080p latent directly takes ~354s on the APU.

To provide optimal speed and quality, this skill defaults to the **Two-Stage Super-Sampling Pipeline**:
1. **Base Latent Generation**: 25 steps at the model's optimal 1024-scale latent patch geometry.
2. **Lanczos-3 Upscaling**: High-fidelity upscaling to 1080p full HD deliverable in **~65 seconds** (5.3x acceleration).

| Aspect Ratio | Base Latent (Divisible by 32) | Final Output | Primary Use Case |
|---|---|---|---|
| `16:9` *(Default)* | 1280 × 704 | **1920 × 1080** | Landscape wallpaper, cinematic scenes, PC desktop |
| `9:16` | 704 × 1280 | **1080 × 1920** | Full-body character portrait, mobile wallpaper, vertical posters |
| `1:1` | 1024 × 1024 | **1440 × 1440** | Square avatar, social media posts, album art |
| `4:3` | 1152 × 864 | **1600 × 1200** | Classic photography, retro displays |
| `3:4` | 864 × 1152 | **1200 × 1600** | Portrait photography, publication covers |
| `3:2` | 1216 × 800 | **1800 × 1200** | Standard 35mm DSLR landscape |
| `2:3` | 800 × 1216 | **1200 × 1800** | Standard 35mm DSLR portrait |
| `21:9` | 1536 × 640 | **2560 × 1080** | Ultra-wide cinematic banners |

---

## 🎨 Prompt Engineering & Capabilities

### 1. Native Chinese & Multilingual Understanding
Because Qwen-Image-2.1 uses **Qwen3-VL 8B** as its text encoder, it natively understands complex nuances, Chinese idioms, poetry, and character interactions without translation:
```bash
python3 ~/.hermes/skills/qwen-image/scripts/qwen_image.py "雨夜霓虹街頭，一位銀髮雙馬尾賽博龐克兔耳少女，身穿半透明機能風外套與百褶裙，雙手叉腰自信微笑，全景全身立繪，腳踩潮濕積水地面" -a 9:16
```

### 2. Anatomical Hand & Pose Control
Qwen-Image-2.1 excels at intricate physical contact and hand poses. When specific gestures are required, include clear anatomical descriptions:

- **Peace Sign (剪刀手 / V字手勢)**:
  `making crisp peace sign V-gesture near cheek with one hand, other hand on hip, cheerful wink`
- **Combat Crouched / Ground Touch (低身戰鬥 / 單手觸地)**:
  `low crouched combat stance, one hand touching the wet pavement, other arm raised defensively, sharp serious focused eyes`
- **Hands on Hips (雙手叉腰自信挺立)**:
  `confident standing pose, both hands resting firmly on hips, chest puffed out, playful smirk, feet planted shoulder-width apart`
- **Relaxed Curb Sitting (街邊抱膝坐姿)**:
  `sitting relaxed on a glowing neon street curb, knees bent and pulled up, one hand gently resting on knee, looking up softly at the rainy night sky`

### 3. Built-in Hand & Defect Suppression
The script automatically applies this negative prompt by default (unless overridden with `-n`):
```text
malformed hands, extra fingers, missing fingers, fused fingers, duplicated fingers, branching fingers, webbed fingers, broken finger joints, misplaced thumbs, twisted wrists, bad anatomy, bad hands, mutated hands, poorly drawn hands, disfigured fingers, irregular finger count, cropped shoes, cropped head, cropped ears
```

---

## 🔧 Service & Environment Verification

Qwen-Image-2.1 connects to the local ComfyUI instance running as a systemd user service:

- **Check Service Status**:
  ```bash
  systemctl --user status comfyui
  ```
- **Restart Service**:
  ```bash
  systemctl --user restart comfyui
  ```
  *(Or trigger `/restart-service`)*
- **API Endpoint**: `http://127.0.0.1:8188`
- **Model Checkpoints**:
  - DiT: `/home/chihmin/src/ComfyUI/models/diffusion_models/qwen_image_2.1_int8_convrot.safetensors`
  - Text Encoder: `/home/chihmin/src/ComfyUI/models/text_encoders/qwen3vl_8b_int8_convrot.safetensors`
  - VAE: `/home/chihmin/src/ComfyUI/models/vae/qwen_image_2.1_vae_bf16.safetensors`
