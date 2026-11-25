---
name: Nano Banana 2 Image Generation Master
description: A formalized skill for generating hyper-realistic, highly-controlled images using the Nano Banana 2 (Gemini 3.1 Flash) model through parameterized JSON prompting via the Kie.ai API.
---

# Nano Banana 2 Image Generation Master

## Goal
Provide a standardized, highly controlled method for generating images using Nano Banana 2 (Gemini 3.1 Flash via Kie.ai). Strictly enforcing a structured JSON parameter schema neutralizes native model biases (over-smoothing, dataset-averaging, "plastic" AI styling) and ensures raw, unretouched, hyper-realistic outputs.

## Prerequisites
- `KIE_AI_API_KEY` set in `.env` at project root
- Python installed
- Scripts at `scripts/generate_kie.py` and `scripts/get_kie_image.py`

## Workflow

### Step 1 — Clarify the request
Ask the user for:
- **Subject**: Who or what (if a person, get physical description, outfit, pose)
- **Environment**: Location, background, lighting
- **Output**: Single image or collage, aspect ratio (e.g. 4:5, 16:9, 3:4)
- **Style**: Candid/realistic, product shot, documentary, etc.

### Step 2 — Build the Dense Narrative Prompt (Paradigm 2)
Construct a JSON file saved to `/prompts/` using the Dense Narrative Format:

```json
{
  "prompt": "Ultra-descriptive narrative. Include: exact camera specs (85mm lens, f/2.0, ISO 200), explicit imperfections (visible pores, mild redness, subtle freckles), lighting behavior (direct on-camera flash creating sharp highlights on skin), direct negative commands inside the prompt (Do not beautify or alter facial features. No makeup styling.).",
  "negative_prompt": "no plastic skin, no CGI, no skin smoothing, no anatomy normalization, no body proportion averaging, no beautification filters, no studio lighting, no airbrushed texture, no stylized realism, no editorial fashion proportions, no high-end retouching",
  "image_input": [],
  "api_parameters": {
    "google_search": false,
    "resolution": "2K",
    "output_format": "png",
    "aspect_ratio": "4:5"
  },
  "settings": {
    "resolution": "2K",
    "style": "documentary realism",
    "lighting": "natural ambient",
    "camera_angle": "eye level",
    "depth_of_field": "shallow, subject sharp",
    "quality": "high detail, unretouched"
  }
}
```

### Step 3 — Execute via Python
```powershell
python scripts/generate_kie.py prompts/your_prompt.json images/output.png "4:5"
```

### Step 4 — Deliver result
Tell the user where the image was saved and offer to iterate.

---

## Core Schema (Paradigm 1 — Structured JSON for complex builds)

Use this when you need maximum control over multi-panel collages or product shots:

```json
{
  "task": "string - e.g., 'single_macro_portrait'",
  "output": {
    "type": "single_image or 4-panel_collage",
    "layout": "1x1 or 2x2_grid",
    "aspect_ratio": "4:5",
    "resolution": "ultra_high",
    "camera_style": "smartphone_front_camera or professional_dslr"
  },
  "image_quality_simulation": {
    "sharpness": "tack_sharp",
    "noise": "unfiltered_sensor_grain",
    "compression_artifacts": false,
    "dynamic_range": "hdr_capable",
    "white_balance": "slightly_warm",
    "lens_imperfections": ["subtle chromatic aberration", "minor lens distortion"]
  },
  "subject": {
    "type": "human_portrait",
    "human_details": {
      "identity": "string",
      "appearance": "extremely specific — visible pores, mild redness, asymmetrical features",
      "outfit": "string"
    }
  },
  "environment": {
    "location": "string",
    "background": "string",
    "lighting": {
      "type": "natural or overhead",
      "quality": "uneven, realistic, non-studio"
    }
  },
  "explicit_restrictions": {
    "no_professional_retouching": true,
    "no_studio_lighting": true,
    "no_ai_beauty_filters": true,
    "no_high_end_camera_look": false
  },
  "negative_prompt": {
    "forbidden_elements": [
      "anatomy normalization", "body proportion averaging", "dataset-average anatomy",
      "beautification filters", "skin smoothing", "plastic skin", "airbrushed texture",
      "stylized realism", "editorial fashion proportions", "depth flattening",
      "mirror selfies", "reflections"
    ]
  }
}
```

## Best Practices

1. **Camera Mathematics** — Always specify focal length, aperture, ISO: `85mm, f/2.0, ISO 200`
2. **Explicit Imperfections** — Name the flaws: `mild redness`, `subtle freckles`, `peach fuzz`
3. **Direct Commands** — Embed negatives in the positive prompt: `Do not beautify. No makeup styling.`
4. **Lighting Behavior** — Describe what the light *does*, not just its type
5. **Noise Trap** — Keep ISO below 800; use physical imperfections for realism, not heavy grain
6. **Negative Stack** — Always include the full forbidden_elements list

## Cost
~$0.04–$0.09 per image via Kie.ai API
