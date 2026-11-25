---
name: generate-image
description: Generate images with OpenAI image models (gpt-5.4-image-2, fallback gpt-5-image) through OpenRouter. Includes 10,000+ curated prompt templates for quick results, plus custom JSON prompting for precise control. Supports various resolutions, aspect ratios, and reference images. ALWAYS use this skill when building websites, landing pages, or web applications that require images.
user-invocable: true
---

# Generate Image Skill

Generate high-quality images with OpenAI image models through OpenRouter.

## ⚠️ MANDATORY: Provider and Models

**All generation goes through OpenRouter, using OpenAI image models only.**

- **PRIMARY**: `openai/gpt-5.4-image-2` (gpt-image-2 generation)
- **FALLBACK**: `openai/gpt-5-image` (the helper uses it on its own if the primary fails)
- Key: `OPENROUTER_API_KEY` from the environment (set in `~/.zshrc`). Never write the key into this file, a script, a command line or a repo.
- Override per run with `--model`, or set `OPENROUTER_IMAGE_MODEL` / `OPENROUTER_IMAGE_FALLBACK`.
- Do NOT call Gemini or Replicate directly. They are no longer configured.

If both models fail, report the error and ask the user how to proceed (retry, change prompt, or abandon).

## Usage

Always call the bundled helper. Do not hand-write API calls.

```bash
python3 ~/.agents/skills/generate-image/scripts/generate_image.py \
  --prompt "YOUR_PROMPT_HERE" \
  --aspect-ratio 3:2 \
  --out public/images/output.png
```

(Codex has the same script at `~/.codex/skills/generate-image/scripts/generate_image.py`.)

- `--reference path` (repeatable) sends reference images for style, subject or composition. Say in the prompt HOW to use each one.
- `--aspect-ratio` accepts `1:1`, `3:2`, `2:3`, `16:9`, `9:16`, `4:5` and so on.
- `--no-fallback` stops after the primary model.
- Output is PNG. Convert to webp/jpg with Pillow for the web.
- Renders take 30–120s. Run several in parallel with `&` and `wait`, or in the background.

## Automatic Triggers

This skill will automatically activate when:
- Building websites, landing pages, or web applications
- Creating placeholder images for web projects
- Generating hero images, banners, or headers
- Creating illustrations for blog posts or content
- Making icons, logos, or graphics for web projects
- Any explicit request to generate or create images

## What This Skill Does

1. Takes your image description (prompt) and optional parameters
2. Calls an OpenAI image model through OpenRouter (the helper falls back to a second OpenAI model if needed)
3. Downloads the generated image to your current directory (or specified web project directory)
4. Verifies image quality — checks for AI artifacts, fine detail accuracy, and physical realism
5. Auto-regenerates with improved prompts if quality check fails (up to 3 attempts)
6. Shows you the result
7. When building websites, automatically saves images in appropriate project directories (e.g., `public/images/`, `assets/`, etc.)

## 🆕 Prompt Library (6,000+ Curated Templates)

This skill includes a library of 6,000+ proven prompts sourced from viral AI artists, organized by category. Use these when you want quick results or inspiration.

### When to Use Library vs Custom

| Situation | Approach |
|-----------|----------|
| "I need a social media post image" | **Library** - search social-media-post category |
| "Generate a YouTube thumbnail" | **Library** - search youtube-thumbnail category |
| "I want something like [reference]" | **Library** - find similar templates |
| "Illustrate this article..." | **Library** - content illustration mode |
| Specific creative vision with details | **Custom** - JSON prompt engineering |
| Professional website photography | **Custom** - use photorealistic guidelines |
| Need precise control over every element | **Custom** - JSON prompt engineering |

### Available Categories

| Category | File | Best For |
|----------|------|----------|
| Profile/Avatar | `profile-avatar.json` | Profile pictures, headshots, avatars, 3D characters |
| Social Media | `social-media-post.json` | Instagram, Twitter/X, TikTok content (3,800+ prompts) |
| Product Marketing | `product-marketing.json` | Product shots, marketing visuals (1,900+ prompts) |
| YouTube Thumbnails | `youtube-thumbnail.json` | Click-worthy video thumbnails |
| E-commerce | `ecommerce-main-image.json` | Product listings, main images |
| Infographics | `infographic-edu-visual.json` | Data visualization, educational content |
| Posters/Flyers | `poster-flyer.json` | Event posters, promotional flyers |
| Comics | `comic-storyboard.json` | Comic panels, storyboards, sequential art |
| Game Assets | `game-asset.json` | Game graphics, sprites, characters |
| App/Web Design | `app-web-design.json` | UI mockups, web graphics, app screens |
| Others | `others.json` | Miscellaneous styles |

### Library Workflow

**Step 1: Detect Mode**
- If user mentions a category or wants inspiration → Library mode
- If user provides content to illustrate → Content illustration mode
- If user has specific creative vision → Custom JSON mode (skip to existing workflow)

**Step 2: Search the Library**
Use grep to search relevant category files. NEVER load entire files into context.

```bash
# Example: Search for "cyberpunk" in social media posts
grep -i "cyberpunk" /Users/georgelane/.codex/skills/generate-image/references/social-media-post.json | head -20
```

**Step 3: Present Recommendations**
- Show maximum 3 matching prompts
- Include: title, description, and sample image URL (sourceMedia)
- Use EXACT prompt text from library - do not modify
- Note if prompt requires reference images (needReferenceImages: true)

**Step 4: User Selection**
- User picks a prompt → Use it directly for generation
- User wants customization → Remix the selected prompt with their requirements
- User wants something different → Search again or switch to custom mode

### Content Illustration Mode

When user provides article/content to illustrate:

1. **Analyze the content** - Identify key themes, mood, subject matter
2. **Map to categories** - Which categories best match the content?
3. **Search for matching styles** - Find prompts that complement the content
4. **Present options** - Show 3 style templates with previews
5. **Remix if needed** - Customize selected template to match specific content elements

### Prompt Entry Structure

Each library prompt has these fields:
```json
{
  "content": "The actual prompt text (use this for generation)",
  "title": "Short descriptive title",
  "description": "What this prompt generates",
  "sourceMedia": ["URL to example image"],
  "needReferenceImages": false  // true if user must provide reference image
}
```

### Category Keywords for Routing

Map user requests to categories:

| User Says | Route To |
|-----------|----------|
| "avatar", "profile pic", "headshot", "pfp" | profile-avatar |
| "instagram", "twitter", "social", "post" | social-media-post |
| "product", "marketing", "ad", "advertisement" | product-marketing |
| "thumbnail", "youtube", "video cover" | youtube-thumbnail |
| "listing", "ecommerce", "shop", "store" | ecommerce-main-image |
| "infographic", "chart", "data", "educational" | infographic-edu-visual |
| "poster", "flyer", "event", "announcement" | poster-flyer |
| "comic", "manga", "storyboard", "panel" | comic-storyboard |
| "game", "sprite", "character", "asset" | game-asset |
| "app", "ui", "interface", "mockup", "web design" | app-web-design |

---

## ⚠️ CRITICAL: Avoiding AI-Looking Images

**When the user wants realistic/photographic images**, ALWAYS enhance their prompt with:

**Must Include:**
- "professional photography" or "shot on [camera]" (e.g., Canon EOS R5, Nikon Z9)
- "anatomically correct" + "natural proportions" (especially for people!)
- "natural lighting" + specific light direction (e.g., "window light from left")
- "authentic" + "realistic details" + "not AI generated"
- Camera specs: "50mm f/2.8", "natural grain", "shallow depth of field"
- **"no text", "no words", "no typography"** (text in AI images looks fake!)

**For People/Portraits (Critical!):**
- ALWAYS add: "anatomically correct, two hands visible, natural proportions"
- ALWAYS add: "natural skin texture with subtle pores and imperfections"
- NEVER use: "perfect", "flawless", "stunning" → Use "authentic", "natural" instead

**Never Include Text:**
- ALWAYS add: "no text, no words, no letters, no typography"
- AI-generated text looks unrealistic and screams "AI-made"
- If the user needs text, add it separately using design tools after generation
- Remove any mention of signs, labels, text, or written content from prompts

**Lighting Specifics (Makes it Real):**
- NOT: "good lighting" → USE: "soft window light from right creating gentle shadows"
- NOT: "studio lighting" → USE: "natural diffused daylight, overcast conditions"
- Add natural imperfections: "slight shadow under nose", "subtle rim light"

**Quick Formula for Realistic Images:**
```
[Subject] + professional photography + anatomically correct + natural proportions +
natural skin texture + authentic expression + shot on Canon EOS R5 with [lens] +
[specific lighting direction] + no text + no words + photojournalistic style +
realistic details + not AI generated
```

**Example:**
Instead of: "person in office"
Use: "professional photography of business person in modern office, anatomically correct proportions, two hands visible, natural skin texture with subtle pores, authentic expression, shot on Canon EOS R5 with 50mm f/2.8 lens, soft window lighting from right side, slight shadows, no text, no words, photojournalistic style, realistic details, not AI generated"

### For Scenes With Equipment, Tools, or Technical Objects

**IMPORTANT**: AI models frequently fail on fine physical details — pipes that don't connect, tools with wrong shapes, equipment with impossible geometry. Use these rules to prevent issues from the start:

- **ALWAYS** describe each object's material, condition, and how it connects to other objects
- **ALWAYS** specify realistic wear and imperfections: "slight scratches", "dust", "minor discoloration at joints"
- **ALWAYS** include real-world specifics: brand names, standard sizes, industry-standard configurations
- **NEVER** rely on the model to "know" what a boiler installation looks like — describe every pipe, valve, and fitting
- Add to constraints: `"every mechanical/technical detail must be physically accurate and functional"`

**Quick Formula for Detail-Heavy Scenes:**
```
[Subject] + [specific material/texture for each object] + [explicit connections between objects] +
[realistic wear/imperfections] + [correct scale references] + [industry-specific terminology] +
professional photography + natural lighting + no text
```

**Example:**
Instead of: "boiler installation in a kitchen"
Use: "professional photograph of a Worcester Bosch Greenstar 8000 combi boiler wall-mounted in a modern kitchen, 22mm copper pipes with compression fittings connecting to the boiler, pipes running neatly along the wall with chrome pipe clips at 300mm intervals, pressure gauge reading 1.5 bar, condensate pipe in 21.5mm white plastic waste pipe running to external wall, slight green patina on copper joints, realistic pipe bends with no impossible angles, shot on Canon EOS R5 with 35mm f/2.8, natural kitchen lighting from window, no text, no words, every detail physically accurate"

## Model Capabilities

OpenAI gpt-image models via OpenRouter: strong prompt following, reference images for style transfer and editing, landscape / portrait / square output. They tend toward smooth mid-tones, so if a brand needs flat inks, map the pixels to the palette in post-processing.

## How to Use

When invoked, you'll be asked for:

1. **Prompt** (required): Describe the image you want to generate
   - Be specific and detailed
   - Include style, mood, lighting, composition details
   - **Never include text/words in the image** - add text separately using design tools

2. **Resolution**: not a parameter. Describe the detail you need in the prompt.

3. **Aspect Ratio** (optional): Image dimensions
   - Common ratios: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`
   - Other options: `2:3`, `3:2`, `4:5`, `5:4`, `21:9`
   - Default: `match_input_image` (1:1 if no input image)

4. **Output Format** (optional): File type
   - `jpg` (default) - Smaller file size
   - `png` - Higher quality, transparency support


6. **Save Location** (when building websites): Specify where to save the image
   - Auto-detect project structure and suggest appropriate directory
   - Default to common patterns like `public/images/`, `assets/`, `static/`, etc.

## Implementation Steps

### 1. Determine Mode and Gather Parameters

**First, detect which mode to use:**

1. **Library Mode** - User wants templates/inspiration OR mentions a category
   - Search the appropriate reference file(s) using grep
   - Present up to 3 matching prompts with titles, descriptions, and sample images
   - Wait for user selection
   - If user picks a prompt, use it directly (or remix with their customizations)
   - Proceed to Step 2 with the selected/remixed prompt

2. **Content Illustration Mode** - User provides article/content to illustrate
   - Analyze the content for themes, mood, subject matter
   - Search relevant categories for matching styles
   - Present 3 style options with sample images
   - Remix selected template to match the specific content
   - Proceed to Step 2

3. **Custom Mode** - User has specific creative vision
   - Ask for prompt and optional parameters (resolution, aspect ratio, format)
   - Convert their description into a full JSON prompt (see "JSON Prompting" section below)
   - Proceed to Step 2

**For Library/Content modes:**
```bash
# Search example - find cyberpunk avatars
grep -i "cyberpunk" /Users/georgelane/.codex/skills/generate-image/references/profile-avatar.json

# Search multiple categories
grep -i "neon" /Users/georgelane/.codex/skills/generate-image/references/social-media-post.json /Users/georgelane/.codex/skills/generate-image/references/profile-avatar.json
```

**For Custom mode**, use sensible defaults if not specified:
- Resolution: 2K
- Format: jpg
- Aspect ratio: based on use case (16:9 for heroes, 1:1 for avatars, etc.)

For website projects, also determine the appropriate save location based on the project structure.

### 2. Generate

Run the helper (see Usage). It prints `saved <path> via <model>` on success, and the error for each model on failure.

### 3. Save Location

Use meaningful filenames (`hero-banner.png`, `plate-river.png`). For websites, save under the project's image directory (`public/images/…`), and convert to webp for production.

### 5. Quality Verification Loop

After saving the image, verify its quality before presenting to the user. This step is **automatic and mandatory** — do not ask the user whether to verify.

**Bypass:** If the user says "skip verification", "fast mode", "no QC", or similar, skip this step entirely.

#### How It Works

1. **Inspect the saved image** using Codex `view_image` when a visual quality check is needed
2. **Evaluate** against the quality rubric below, with special focus on fine physical details
3. **Decide**: ACCEPT / ACCEPT WITH CAVEAT / REJECT
4. If REJECT and attempts remain → modify the prompt, delete the failed image, regenerate
5. If REJECT and no attempts remain → present options to the user

**Retry limits:** MAX_ATTEMPTS = 3 (1 initial + 2 retries). Worst case cost: 3x base ($0.45-$0.90).

#### Quality Rubric

**Mode-aware:** For photorealistic images, apply the full rubric. For illustrations, abstract art, or comics, apply only CRITICAL checks plus physical accuracy checks (phantom objects, impossible connections). Skip skin/face/saturation/AI aesthetic checks for non-photorealistic styles.

##### CRITICAL Failures (auto-reject)

Any single CRITICAL failure means immediate rejection:

- Extra, missing, or deformed limbs or hands
- Grotesque facial distortion
- Visible garbled text artifacts
- Gross anatomical impossibility
- Image corruption or rendering artifacts
- Completely wrong subject (asked for a boiler, got a landscape)
- **Phantom objects** — limbs, pipes, wires, tools, or objects that appear from nowhere with no logical source or connection

##### MAJOR Warnings

**Fine Detail & Realism (THE KEY CHECKS — this is where AI falls down):**

- **Unrealistic object details** — pipes that don't connect properly, tools with wrong shapes/proportions, equipment that couldn't physically work, mechanical parts that make no sense
- **Impossible physical connections** — things joined at wrong angles, pipes going through walls illogically, wires connected to nothing, hoses with no source/destination
- **Wrong material textures** — copper that doesn't look like copper, plastic that looks like metal, wood grain that's too uniform, surfaces that are too smooth/perfect for the material
- **Scale inconsistencies** — objects that are wrong size relative to each other (e.g., a wrench bigger than a boiler, screws the size of fists)
- **Missing expected details** — a boiler with no pressure gauge, a toolbox with featureless tools, a kitchen with no handles on cabinets
- **Physically impossible arrangements** — objects floating, defying gravity, balanced impossibly, overlapping through each other

**General AI Tells:**

- Uncanny valley faces (waxy, dead eyes)
- Plastic/airbrushed skin with zero texture
- Oversaturated/HDR look
- Inconsistent lighting/shadows (light from contradictory directions)
- Background anomalies (morphing objects, impossible geometry)
- Generic AI aesthetic (too clean, too perfect, no authentic character)

##### MINOR Notes (don't reject, but note for improvement)

- Slightly unrealistic textures that aren't obviously wrong
- Minor composition issues
- Subtle color cast differences from intent

#### Decision Logic

```
Any CRITICAL failure           → REJECT
2+ MAJOR warnings              → REJECT
1 MAJOR warning + attempts remain → REJECT (worth improving)
1 MAJOR warning + final attempt   → ACCEPT WITH CAVEAT
0 CRITICAL + 0-1 MAJOR        → ACCEPT
```

#### Fine-Detail Verification Instructions

When evaluating an image, you MUST zoom in mentally on every distinct object/element and ask:

1. **"Does this look exactly like the real thing?"** — pipes, tools, equipment, furniture, etc.
2. **"Are all connections physically logical?"** — where do pipes go, what are wires attached to, do joints make sense?
3. **"Is everything the right scale relative to everything else?"**
4. **"Are there any phantom objects that shouldn't be there?"** — extra limbs, mystery pipes, floating elements
5. **"Would a professional in this field (plumber, electrician, builder) spot something wrong immediately?"**

This is the MOST IMPORTANT part of verification. General AI detection (smooth skin, weird lighting) matters less than getting the physical details right.

#### Prompt Modification Guide

When an image is rejected, modify the prompt to fix the specific issues found:

| Issue Found | How to Fix the Prompt |
|-------------|----------------------|
| Phantom objects/limbs | Add explicit count constraints: "exactly X pipes", "only the tools mentioned"; add to negative_prompt: "no extra objects, no phantom limbs" |
| Unrealistic object details | Add hyper-specific descriptions of each object: material, texture, wear, connection points. E.g., "copper pipes with green patina at joints, compression fittings" |
| Wrong physical connections | Describe the connections explicitly: "pipe connects from boiler outlet valve down to floor-mounted manifold" |
| Wrong material textures | Specify material AND its characteristics: "brushed stainless steel with visible grain direction and fingerprint marks" rather than just "metal" |
| Scale inconsistencies | Add explicit size references: "standard 15mm copper pipe", "adjustable wrench approximately 30cm long" |
| Missing expected details | List the details explicitly in the prompt rather than relying on the model to know what a boiler/kitchen/workshop should contain |
| Deformed hands/extra limbs | Add "exactly two arms, five fingers per hand"; or hide hands (pockets, cropped) |
| Plastic skin / uncanny faces | Add "natural skin texture with pores"; add film stock reference; remove "perfect"/"beautiful" |
| Oversaturation | Add "natural color grading, muted tones"; add "shot on Kodak Portra 400" |
| Lighting inconsistency | Specify single light source with explicit direction |
| Generic AI aesthetic | Add film stock imperfections; reference specific photography style |

#### Meta-Strategy Across Attempts

- **Attempt 1**: Original prompt (with enhanced detail guidance from the prompting rules above)
- **Attempt 2**: Original + specific fixes for issues found + more explicit object descriptions + strengthened anti-AI directives
- **Attempt 3**: Simplified composition (fewer objects, simpler scene) + all previous fixes + maximum detail on remaining elements

#### When All Attempts Fail

If all 3 attempts produce rejected images, present the user with three options:
1. **Try a fundamentally different approach** — different angle, composition, or style
2. **Accept the best attempt** — show all three and let the user pick
3. **Abandon** — move on without an image

### 6. Show Results

Display the saved file path to the user and show the image with `view_image` when a visual preview is useful.

## Example Prompts for Websites

**Hero Images (Photorealistic):**
- "professional photography of modern office space with diverse team collaborating, anatomically correct proportions, natural lighting from large windows, authentic expressions, shot on Canon EOS R5 with 24mm f/2.8 lens, slight natural grain, no text, no words, photojournalistic style, real workplace environment, not AI generated"
- "business meeting photograph, natural office setting, people with realistic proportions and natural skin texture, soft window lighting from left, authentic interaction, shot on full-frame DSLR, no text, no typography, documentary style, not AI generated"
- "cityscape photograph at blue hour, natural colors, taken from rooftop with 50mm lens, slight atmospheric haze, authentic urban environment, no text, no signs, film photography aesthetic"

**Hero Images (Abstract/Graphic - when you want stylized, not photorealistic):**
- "Modern abstract gradient background, blue to purple, smooth waves, minimal, professional website hero section"
- "Geometric pattern design, clean lines, modern aesthetic, suitable for web banner"

**Product/Service Images (Photorealistic):**
- "product photography of laptop on wooden desk, natural window light creating soft shadows, realistic wood grain texture, shot on Canon 5D Mark IV with 50mm f/2.8 lens, slight dust particles in light, authentic office environment, natural colors, no text, no words, no typography"
- "photograph of hand holding smartphone, anatomically correct hand with two visible fingers, natural skin texture, soft diffused lighting, shot on macro lens f/2.8, authentic product photography, realistic proportions, no text, no words"
- "professional workspace photograph, laptop and coffee cup on desk, natural morning light, subtle shadows, realistic textures, shot on DSLR camera, no text, no typography, photojournalistic style"

**Product Images (Illustration - when you want graphic style):**
- "Isometric illustration of a cloud server infrastructure, modern tech style, vibrant colors"
- "Flat design illustration of mobile app interface, modern minimal style"

**People/Team Photos (Critical - Always use photorealistic approach):**
- "professional headshot of business executive, anatomically correct facial features, natural skin texture with subtle pores, authentic smile, two hands visible in natural position, shot on Canon EOS R5 with 85mm f/1.8 lens, soft window light from right, slight shadows, no text, no words, no typography, photojournalistic style, real person not AI generated"
- "team photo in modern office, group of 4 people with anatomically correct proportions, natural expressions, authentic workplace interaction, shot on full-frame DSLR with 35mm lens, natural office lighting, no text, no words, photojournalistic documentary style, realistic details, not AI generated"
- "portrait of person working at desk, natural posture, anatomically correct, authentic concentration expression, natural skin texture, window light from left side, shot on 50mm f/2.0 lens, slight background blur, no text, no typography, professional photography"

**Blog/Content Images (Photorealistic):**
- "photograph of person working from home, natural home office setting, authentic workspace, soft natural lighting, shot on DSLR camera, no text, no words, documentary photography style, realistic environment and proportions, not AI generated"
- "close-up photograph of hands typing on laptop keyboard, anatomically correct hands, natural skin texture, shallow depth of field, shot on 85mm f/1.8 lens, natural lighting, no text, no typography"

**Blog/Content Images (Illustration - when you want graphic style):**
- "Flat illustration of people working remotely, modern style, pastel colors, friendly aesthetic"
- "Data visualization concept, charts and graphs, modern infographic style, blue and orange color scheme"

## Pricing Reference

Billed per image by OpenRouter at OpenAI rates. Check https://openrouter.ai/openai/gpt-5.4-image-2 for current prices.

## Error Handling

| Error | Action |
|---|---|
| `OPENROUTER_API_KEY is not set` | Ask the user to add it to `~/.zshrc`. Do not search for keys. |
| HTTP 401/402 | Bad key or no credit. Tell the user. |
| HTTP 429/5xx or timeout | The helper tries the fallback. If both fail, retry once, then report. |
| Content policy refusal | Change the prompt. A different model does not fix it. |
| Quality check fails | Change the prompt and regenerate (max 3 attempts), see step 5. |

## Tips for Best Results

### General Guidelines
1. Be specific about style, mood, and composition
2. Include lighting details (e.g., "golden hour", "studio lighting")
3. **NEVER include text/words in images** - AI-generated text looks fake; add text separately using design tools
4. Use higher resolutions (4K) for detailed images or large prints
5. Use PNG format if you need transparency or maximum quality
6. For website images, optimize aspect ratio for the use case (16:9 for heroes, 1:1 for avatars, etc.)
7. Consider web performance - use 1K or 2K for web, save 4K for special cases

### Creating Photorealistic, Non-AI-Looking Images

**IMPORTANT**: To avoid common AI artifacts (like extra fingers, unrealistic proportions, or overly smooth/plastic appearance):

**1. Photography Keywords** - Add these to make images look like real photos:
   - "professional photography", "DSLR camera", "shot on Canon EOS R5"
   - "natural lighting", "authentic", "realistic imperfections"
   - Specific camera settings: "f/2.8", "50mm lens", "ISO 400", "natural grain"
   - "documentary style", "candid shot", "photojournalism"

**2. Anti-AI Phrases** - Include these to reduce AI artifacts:
   - "anatomically correct", "realistic proportions", "natural human anatomy"
   - "real photograph", "not AI generated", "authentic photography"
   - "film photography", "shot on 35mm film", "analog photography"
   - "natural skin texture", "realistic details", "photorealistic"

**3. Avoid Generic AI Terms** - Don't use:
   - ❌ "highly detailed", "trending on artstation", "unreal engine"
   - ❌ "perfect", "flawless", "stunning", "breathtaking"
   - ❌ "digital art", "concept art" (unless you actually want digital art)
   - ❌ Overly generic descriptions without specific details

**4. Specify Realistic Details**:
   - Instead of: "beautiful person"
   - Use: "person with natural skin texture, slight blemishes, authentic expression, photographed in natural daylight"

   - Instead of: "amazing landscape"
   - Use: "landscape photograph taken during golden hour, natural colors, slight atmospheric haze, shot on full-frame DSLR"

**5. For People/Portraits** (to avoid extra limbs, wrong proportions):
   - ALWAYS specify: "anatomically correct", "two hands visible", "natural proportions"
   - Add: "professional portrait photography", "authentic human features"
   - Include: "natural skin texture with pores and subtle imperfections"
   - Example: "professional headshot of a business person, anatomically correct, natural proportions, two hands visible, authentic facial features, slight skin texture, shot on Canon 5D Mark IV with 85mm f/1.8 lens"

**6. Lighting Makes It Real**:
   - Be very specific: "soft window light from the left", "golden hour backlighting", "overcast natural light"
   - Avoid: "perfect lighting", "studio lighting" (unless you want studio look)
   - Add natural imperfections: "slight shadow under nose", "subtle rim light", "natural fall-off"

**7. Never Include Text/Typography**:
   - ALWAYS add to prompt: "no text, no words, no letters, no typography, no signs"
   - AI-generated text is an instant giveaway of AI generation
   - Remove any mention of: signs, labels, billboards, posters, text overlays, captions
   - If you need text on the image, add it after generation using Photoshop, Figma, or other design tools
   - Examples to avoid: ❌ "billboard with company name", ❌ "sign saying 'open'", ❌ "text overlay"

**Example Transformation**:

❌ **Bad (AI-looking)**: "beautiful woman in office"

✅ **Good (photorealistic)**: "professional photography of a business woman in modern office, anatomically correct proportions, natural skin texture with subtle pores, authentic expression, shot on Canon EOS R5 with 50mm f/2.8 lens, natural window lighting from right side, slight shadows, no text, no words, no typography, realistic details, photojournalistic style, not AI generated"

## JSON Prompting (Required for All Images)

**IMPORTANT: Always use JSON prompts for ALL image generations.** JSON prompts provide structured information that makes outputs more repeatable and gives you direct control over subject, style, composition, and lighting. They help avoid the model's default aesthetic and produce consistent, high-quality results.

### Why JSON for Everything

- **Consistency**: Every image follows the same structured approach
- **Control**: Direct control over every aspect of the image
- **No defaults**: Escape the model's default "beautiful, warm, rustic" look
- **Reproducibility**: Easy to tweak and iterate on prompts
- **Quality**: More detailed prompts = better results

### JSON Template Structure

Use this template as your starting point for ALL image generations. Adapt the fields to your subject:

```json
{
  "subject": {
    "main": "Description of the main subject",
    "details": {
      "appearance": "Specific visual details",
      "position": "Where/how positioned",
      "action": "What they're doing (if applicable)"
    }
  },
  "environment": {
    "setting": "Location/context",
    "background": {
      "type": "Studio/natural/urban/etc",
      "color": "Specific colors",
      "depth": "Shallow/deep/blurred"
    },
    "props": "Any additional elements in scene"
  },
  "photography": {
    "style": "Portrait/landscape/product/etc",
    "shot_scale": "Close-up/medium/wide",
    "lighting": {
      "type": "Natural/studio/dramatic/etc",
      "source": "Window/softbox/sun/etc",
      "direction": "From left/right/above/behind",
      "quality": "Soft/hard/diffused"
    },
    "camera_gear": {
      "lens": "50mm/85mm/24mm/etc",
      "aperture": "f/1.8/f/2.8/f/8/etc",
      "focus": "What's sharp vs blurred"
    },
    "post_processing": {
      "look": "Clean/moody/vintage/etc",
      "grading": "Color treatment"
    }
  },
  "aesthetic_fidelity": {
    "medium": "Digital Photography/Film/Illustration/etc",
    "vibe": "Overall mood and feeling",
    "visual_qualities": [
      "Quality 1",
      "Quality 2"
    ]
  },
  "constraints": {
    "must_keep": [
      "Essential element 1",
      "Essential element 2"
    ],
    "avoid": [
      "Unwanted element 1",
      "Unwanted element 2"
    ]
  },
  "negative_prompt": [
    "bad quality indicators",
    "unwanted elements",
    "AI artifacts to avoid"
  ]
}
```

### Adapting the Template

**For People/Portraits** - Add detailed face and body sections:
```json
{
  "subject": {
    "demographics": { "age": "30s", "gender": "Male" },
    "face": {
      "skin": { "tone": "Medium, warm undertones", "texture": "Natural with subtle pores" },
      "eyes": { "color": "Brown", "gaze_direction": "At camera" },
      "expression": "Confident, subtle smile"
    },
    "hair": { "style": "Short, neat", "color": "Dark brown" },
    "pose": { "position": "Seated", "hands": "Visible, natural position" }
  },
  "attire": {
    "clothing": "Navy blazer, white shirt",
    "fit": "Well-tailored, professional"
  }
}
```

**For Products** - Focus on object details:
```json
{
  "subject": {
    "product": "Wireless headphones",
    "brand_style": "Premium, minimalist",
    "material": { "body": "Matte black aluminum", "cushions": "Leather" },
    "details": "Visible texture, subtle branding"
  },
  "presentation": {
    "angle": "Three-quarter view",
    "surface": "White marble slab",
    "arrangement": "Slightly angled, hero position"
  }
}
```

**For Scenes/Landscapes** - Emphasize environment:
```json
{
  "environment": {
    "location": "Mountain lake at sunrise",
    "weather": "Clear, slight morning mist",
    "season": "Autumn, golden foliage",
    "time_of_day": "Golden hour, sun just above horizon"
  },
  "composition": {
    "foreground": "Rocky shoreline with scattered leaves",
    "midground": "Still lake with perfect reflections",
    "background": "Snow-capped peaks"
  }
}
```

**For Abstract/Graphic** - Focus on visual properties:
```json
{
  "design": {
    "type": "Abstract gradient",
    "shapes": "Flowing waves, organic curves",
    "colors": {
      "primary": "Deep purple (#6B21A8)",
      "secondary": "Electric blue (#3B82F6)",
      "accent": "Soft pink highlights"
    },
    "texture": "Smooth with subtle noise grain"
  },
  "composition": {
    "flow": "Diagonal, bottom-left to top-right",
    "balance": "Asymmetric, dynamic"
  }
}
```

### Complete Example: Website Hero Image

When user asks for "a hero image for a tech startup":

```json
{
  "subject": {
    "main": "Diverse team of 3 professionals collaborating",
    "details": {
      "people": [
        { "position": "Left", "action": "Pointing at screen", "attire": "Smart casual" },
        { "position": "Center", "action": "Typing on laptop", "attire": "Button-up shirt" },
        { "position": "Right", "action": "Taking notes", "attire": "Blazer" }
      ],
      "demographics": "Mixed ages 25-40, diverse ethnicities",
      "expressions": "Engaged, collaborative, natural smiles"
    }
  },
  "environment": {
    "setting": "Modern open-plan office",
    "background": {
      "elements": "Floor-to-ceiling windows, city view (blurred)",
      "depth": "Shallow, focus on people"
    },
    "props": "MacBook, notebooks, coffee cups, plant"
  },
  "photography": {
    "style": "Corporate lifestyle photography",
    "shot_scale": "Medium shot, waist up",
    "lighting": {
      "type": "Natural daylight",
      "source": "Large windows camera-left",
      "direction": "Side lighting with soft fill",
      "quality": "Soft, diffused, no harsh shadows"
    },
    "camera_gear": {
      "lens": "35mm",
      "aperture": "f/2.8",
      "focus": "Sharp on faces, soft background"
    },
    "post_processing": {
      "look": "Clean, modern, slightly lifted shadows",
      "grading": "Neutral with slight warmth"
    }
  },
  "aesthetic_fidelity": {
    "medium": "Digital Photography",
    "vibe": "Professional, approachable, innovative",
    "visual_qualities": [
      "High resolution",
      "Natural skin tones",
      "Realistic proportions",
      "Authentic interaction"
    ]
  },
  "constraints": {
    "must_keep": [
      "Natural, authentic expressions",
      "Anatomically correct hands and proportions",
      "Professional but approachable vibe",
      "Modern tech environment"
    ],
    "avoid": [
      "Stock photo poses",
      "Overly perfect/plastic skin",
      "Fake smiles",
      "Cluttered background",
      "Any text or signage"
    ]
  },
  "negative_prompt": [
    "text", "words", "typography", "signs", "logos",
    "extra limbs", "distorted hands", "blurry faces",
    "oversaturated", "HDR look", "artificial lighting",
    "stock photo", "generic", "clip art"
  ]
}
```

### Image to JSON Conversion

Use this system prompt with a capable vision model to convert a reference image into a JSON prompt:

```
You are an expert prompt engineer for OpenAI gpt-image models. Your task is to convert the user's description into a sophisticated, EXTREMELY DETAILED JSON prompt. You must output a single valid JSON object.

### JSON STRUCTURE GUIDELINES:
1. **Dynamic Fields**: Add new fields that capture specific details about the subject (e.g., "plating_style" for food, "architecture_era" for buildings).
2. **Remove Irrelevant Fields**: Do NOT include fields that don't apply. If the subject is a stove, do not include "hair", "skin", or "pose".
3. **Subject Specificity**:
   - **For People**: Keep subject, face, skin, hair, clothing structure.
   - **For Non-Humans**: Create a structure that fits the object.
4. **Standard Fields**: Always include "constraints" (with "must_keep" and "avoid" lists) and "negative_prompt".

### AESTHETIC GOALS:
- **Medium Specificity**: If the user asks for a specific style (e.g. "oil painting"), describe the brushwork, canvas texture, and drying cracks.
- **Lighting**: Be precise (soft, hard, volumetric, golden hour, studio, rim lighting).
- **Camera**: (focal length, depth of field) - ONLY if the style requires photorealism.

Return ONLY the raw JSON string.
```

### Creating Variations from JSON

Prefix your JSON prompt with instructions to generate variations while maintaining the same aesthetic:

**Basic variation:**
```
Generate a new image with SIGNIFICANTLY different nouns, objects, color palette and pose compared to the JSON below. CRITICAL: Strictly preserve the original 'vibe', 'aesthetic', and 'mood'. The result should look like a distinct image from the same artistic series.

[YOUR JSON PROMPT HERE]
```

**Steered variation:**
```
Additional Instruction: Make it night time

Generate a new image with SIGNIFICANTLY different nouns, objects, color palette and pose compared to the JSON below. CRITICAL: Strictly preserve the original 'vibe', 'aesthetic', and 'mood'. The result should look like a distinct image from the same artistic series.

[YOUR JSON PROMPT HERE]
```

### Quick Reference: Essential JSON Fields

For ANY image, always include these minimum fields:

```json
{
  "subject": { "main": "..." },
  "photography": {
    "lighting": { "type": "...", "source": "..." },
    "camera_gear": { "lens": "...", "aperture": "..." }
  },
  "aesthetic_fidelity": { "medium": "...", "vibe": "..." },
  "constraints": { "must_keep": [...], "avoid": [...] },
  "negative_prompt": [...]
}
```
