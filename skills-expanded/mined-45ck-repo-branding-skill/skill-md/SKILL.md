# Repo Branding Skill

Generate a complete brand kit for a GitHub repository: light/dark PNG banners, logos, icons, a social preview, and a theme-aware README banner using `<picture>`. All images are generated via Gemini image generation for high-quality output.

## Trigger

This skill is invoked via `/repo-branding`.

## Instructions

Follow these steps exactly:

### Step 1: Gather Repo Context

Read the current repository's context to inform branding decisions:

1. **README**: Read the first 100 lines of `README.md` (if it exists)
2. **Project manifest**: Check for and read whichever exists first:
   - `package.json` (extract `name` and `description`)
   - `pyproject.toml` (extract `[project].name` and `[project].description`)
   - `Cargo.toml` (extract `[package].name` and `[package].description`)
   - `go.mod` (extract module name)
3. **Repo name**: Get from `git remote get-url origin` (extract repo name from URL), or fall back to the current directory name via `basename $(pwd)`
4. **Primary language**: Determine by checking which file extensions are most common:
   ```bash
   find . -type f \( -name '*.ts' -o -name '*.js' -o -name '*.py' -o -name '*.rs' -o -name '*.go' -o -name '*.java' -o -name '*.rb' -o -name '*.cpp' -o -name '*.c' \) | head -50 | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -1
   ```
5. **Existing brand assets**: Scan `assets/`, `.github/`, and the project root for existing logos, banners, or brand images
6. **Additional docs**: Read `CONTRIBUTING.md` headers or `docs/` index if present for extra context
7. **License**: Detect license type from `LICENSE` or `LICENSE.md`

Store these values:
- `PROJECT_NAME`: human-readable project name
- `PROJECT_DESCRIPTION`: one-line description (or synthesize one from README)
- `PRIMARY_LANGUAGE`: dominant language
- `DOMAIN`: the project's domain/category (e.g., "CLI tool", "web framework", "data pipeline")
- `LICENSE_TYPE`: detected license (e.g., "MIT", "Apache-2.0")

### Step 2: Check for API Key

Check the environment for a Gemini API key:

```bash
echo "${GEMINI_API_KEY:-${GOOGLE_API_KEY:-__MISSING__}}"
```

If the result is `__MISSING__`, tell the user:

> **Gemini API key not found.** Set one of these environment variables and try again:
>
> ```bash
> export GEMINI_API_KEY="your-key-here"
> ```
>
> Get a free key at https://aistudio.google.com/apikey

Then **stop** -- do not continue.

### Step 3: Generate Design Brief

Using all the context gathered in Step 1, produce a design brief and save it to `assets/DESIGN_BRIEF.json`.

Create the `assets/` directory if it doesn't exist:
```bash
mkdir -p assets
```

You (Claude Code) generate this brief -- do NOT call Gemini for this step. Be specific and opinionated. Ground every choice in the actual repo content. The brief must follow this structure:

```json
{
  "repo_name": "",
  "tagline": "",
  "one_sentence_purpose": "",
  "target_users": "",
  "keywords": ["", "", "", ""],
  "visual_metaphors": ["", "", ""],
  "avoid": ["no mascots", "no photorealism", "..."],
  "style_adjectives": ["minimal", "technical", "credible", "..."],
  "palette_hint": {
    "bg_light": "#ffffff",
    "bg_dark": "#0d1117",
    "primary": "",
    "accent": "",
    "ink": ""
  },
  "assets_needed": [
    {"path": "assets/banner.light.png", "type": "readme_banner", "desc": "Wide banner on white background"},
    {"path": "assets/banner.dark.png", "type": "readme_banner", "desc": "Wide banner on dark background (#0d1117)"},
    {"path": "assets/logo.light.png", "type": "square_logo", "desc": "Square logo on white background"},
    {"path": "assets/logo.dark.png", "type": "square_logo", "desc": "Square logo on dark background (#0d1117)"},
    {"path": "assets/social-preview.png", "type": "github_social_preview", "desc": "GitHub social preview card (landscape)"}
  ]
}
```

Guidelines for the brief:
- `tagline`: Short, memorable phrase -- not just the description restated
- `visual_metaphors`: Concrete imagery ideas grounded in what the project does
- `style_adjectives`: At least 3-5 adjectives that describe the desired visual feel
- `palette_hint.primary` and `accent`: Pick colors that reflect the project's personality (e.g., blue for trust/stability, green for growth/data, orange for energy/speed)
- `avoid`: List things that would look bad or be inappropriate for this project

Write the JSON to `assets/DESIGN_BRIEF.json`.

### Step 4: Generate All Images via Gemini Image Generation

Write and execute a single Python script that generates all brand assets using Gemini's image generation models. Each asset is generated with a tailored prompt derived from the design brief.

Install the SDK first if needed:
```bash
pip install -q google-genai
```

**Python script** (write to a temp file and run it):

```python
import json
import os
import sys

from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

with open("assets/DESIGN_BRIEF.json") as f:
    brief = json.load(f)

repo = brief["repo_name"]
tagline = brief.get("tagline", "")
purpose = brief.get("one_sentence_purpose", "")
style = ", ".join(brief.get("style_adjectives", ["clean", "modern"]))
metaphors = ", ".join(brief.get("visual_metaphors", []))
avoid = ", ".join(brief.get("avoid", []))
primary = brief.get("palette_hint", {}).get("primary", "#3b82f6")
accent = brief.get("palette_hint", {}).get("accent", "#8b5cf6")

shared_style = f"""Style: {style}.
Visual inspiration: {metaphors}.
Primary color: {primary}. Accent color: {accent}.
Do NOT include: {avoid}.
No photorealism. No stock photo aesthetics. Clean vector/flat illustration style.
All text must be crisp, readable, and correctly spelled."""

assets = [
    {
        "path": "assets/banner.light.png",
        "prompt": f"""Create a wide GitHub README banner image (ultra-wide, roughly 4:1 aspect ratio).

White/light background (#ffffff or very light).
Display "{repo}" as large, bold, prominent title text -- perfectly spelled and readable.
Below it, smaller text: "{tagline}"
Include subtle abstract decorative elements inspired by: {metaphors}.
{shared_style}
The text must be the focal point. Keep decorative elements subtle and secondary.
Professional open-source project banner aesthetic."""
    },
    {
        "path": "assets/banner.dark.png",
        "prompt": f"""Create a wide GitHub README banner image (ultra-wide, roughly 4:1 aspect ratio).

Dark background (#0d1117 or very dark).
Display "{repo}" as large, bold, prominent title text in light/white color -- perfectly spelled and readable.
Below it, smaller text: "{tagline}"
Include subtle abstract decorative elements inspired by: {metaphors}.
{shared_style}
The text must be the focal point. Keep decorative elements subtle and secondary.
Professional open-source project banner aesthetic. Dark theme."""
    },
    {
        "path": "assets/logo.light.png",
        "prompt": f"""Create a square logo/icon for a software project called "{repo}".

White/light background.
Simple, memorable, iconic symbol that represents: {purpose}.
Do NOT include any text in the logo -- symbol/icon only.
{shared_style}
Square format. Clean edges. Would work as a favicon or app icon at small sizes."""
    },
    {
        "path": "assets/logo.dark.png",
        "prompt": f"""Create a square logo/icon for a software project called "{repo}".

Dark background (#0d1117).
Simple, memorable, iconic symbol that represents: {purpose}.
Do NOT include any text in the logo -- symbol/icon only.
{shared_style}
Square format. Clean edges. Would work as a favicon or app icon at small sizes. Dark theme."""
    },
    {
        "path": "assets/social-preview.png",
        "prompt": f"""Create a GitHub social preview image (landscape, roughly 2:1 aspect ratio, 1280x640).

Dark background preferred.
Display "{repo}" prominently in large, bold text -- perfectly spelled.
Below it: "{tagline}"
Include abstract decorative background inspired by: {metaphors}.
{shared_style}
No small text, no fine details -- this will be shown as a thumbnail.
Professional open-source project social card."""
    },
]

models_to_try = ["gemini-2.0-flash-exp-image-generation", "gemini-2.0-flash-preview-image-generation"]

os.makedirs("assets", exist_ok=True)
created = []
failed = []

for asset in assets:
    path = asset["path"]
    prompt = asset["prompt"]
    print(f"\nGenerating {path}...")

    success = False
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                ),
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image_data = part.inline_data.data
                    with open(path, "wb") as f:
                        f.write(image_data)
                    size_kb = len(image_data) / 1024
                    print(f"  Saved {path} ({size_kb:.1f} KB) via {model_name}")
                    created.append(path)
                    success = True
                    break

            if success:
                break
            print(f"  No image from {model_name}, trying next...")
        except Exception as e:
            print(f"  {model_name} failed: {e}")

    if not success:
        print(f"  FAILED to generate {path}")
        failed.append(path)

print(f"\n{'='*50}")
print(f"Generated {len(created)}/{len(assets)} images.")
if failed:
    print(f"Failed: {', '.join(failed)}")
if not created:
    sys.exit(1)
```

Run the script. Verify the PNG files were created in `assets/`.

**Note on models**: The script tries `gemini-2.0-flash-exp-image-generation` first (best availability), then falls back. If those models don't work, try substituting with `gemini-3-pro-image-preview` or `gemini-3.1-flash-image-preview` as the primary model.

### Step 5: Update README

Update `README.md` to include the theme-aware banner using a `<picture>` element:

1. **If a `<picture>` tag** already exists for the banner, replace the entire `<p align="center">...<picture>...</picture>...</p>` block with the new one below.
2. **If an `<img` tag or `![` markdown image** referencing a banner exists within the first 10 lines, replace that line (and surrounding `<p>` tag if present) with the new block below.
3. **Otherwise**, insert the following block after the first `# Title` heading line:

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner.dark.png" />
  <source media="(prefers-color-scheme: light)" srcset="assets/banner.light.png" />
  <img src="assets/banner.light.png" alt="PROJECT_NAME banner" width="100%" />
</picture>
```

Replace `PROJECT_NAME` with the actual project name.

### Step 6: Output Summary

After completing all steps, output:

```
Repo branding complete!

  assets/
    DESIGN_BRIEF.json     : Design brief (editable -- rerun to regenerate)
    banner.light.png      : README banner (light theme)
    banner.dark.png       : README banner (dark theme)
    logo.light.png        : Logo (light background)
    logo.dark.png         : Logo (dark background)
    social-preview.png    : GitHub social preview (1280x640)
  README.md               : Updated with <picture> banner

To set the social preview on GitHub:
  Settings > General > Social preview > Upload assets/social-preview.png

To commit:
  git add assets/ README.md && git commit -m "Add repo branding kit"
```
