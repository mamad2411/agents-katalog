---
name: huashu-douyin-script
description: |
  Short video viral script creation workflow. End-to-end process from competitor video breakdown to script generation: download Douyin videos → Gemini video analysis → viral formula extraction → script + storyboard generation → AI-tone proofreading.
  Use when the user mentions "short video script", "viral breakdown", "competitor analysis", "promotional script", "ad material", "seeding script", "video breakdown", or "short video analysis".
---

# Short Video Viral Script Creation

A complete workflow from competitor video breakdown to script generation. Transforms "copy viral videos by instinct" into "AI-powered systematic breakdown + structured replication".

## Environment Requirements

- `uv` (Python package manager)
- `yt-dlp` (video download — `pip install yt-dlp` or `brew install yt-dlp`)
- `GEMINI_API_KEY` environment variable (for Gemini video analysis — get from <https://aistudio.google.com/apikey>)
- Chrome browser signed into the relevant platform (to extract download cookies)

**Path convention**: `SKILL_DIR` in the instructions below refers to the absolute path of the directory containing this SKILL.md file. Before running scripts, use `dirname` or a Glob tool to determine the actual location of SKILL.md and replace `SKILL_DIR`.

## 6-Step Workflow

### Step 1: Collect Inputs

Gather the following from the user:

**Required**:

- Video links (1–5 benchmark / competitor videos)
- Product information (name, core selling points, target audience, price)
- Script type: Seeding video OR ad creative / paid traffic material

**Optional**:

- Product images (for visual reference in the script)
- Target duration (seeding default: 30 seconds; ad material default: 15 seconds)
- Brand tone requirements
- Campaign objective (live-stream traffic / product page / follow conversion)

If the user has only provided partial information, proactively ask for what's missing.

---

### Step 2: Download Videos

Run the download script:

```bash
uv run SKILL_DIR/scripts/download_video.py \
  --urls "URL1" "URL2" \
  --output-dir _temp/video-downloads
```

**Parameters**:

- `--urls`: Supports short links, page links, and share text (auto-extracts URL)
- `--output-dir`: Defaults to `_temp/video-downloads/` in the current working directory
- `--cookies-browser`: Default `chrome`; options include `edge` / `firefox`

**If download fails**:

1. Prompt the user to confirm Chrome is signed into the platform
2. Suggest manually downloading the video into `_temp/video-downloads/`
3. If a relevant MCP server is available, try downloading via MCP

---

### Step 3: Gemini Video Analysis (Can Be Parallelised)

For each successfully downloaded video, call Gemini video analysis:

```bash
uv run SKILL_DIR/scripts/analyze_video.py \
  --video "_temp/video-downloads/video-1-xxx.mp4" \
  --prompt "PROMPT_BELOW" \
  --model flash \
  --resolution medium \
  --output "_temp/video-downloads/analysis-1.md"
```

**Use the flash model + medium resolution** (sufficient for short videos; saves cost).

**Multiple videos can be analysed in parallel** (use `run_in_background=true`).

**Viral Analysis Prompt** (pass in via `--prompt`):

```text
As a senior short-form video e-commerce analyst, conduct a 7-dimension in-depth breakdown of this video.
Special focus: the first 3 seconds are the most critical part — break them down at a near-frame-by-frame level.

## 1. Hook Analysis (First 3 Seconds) ⭐ Most Critical
The first 3 seconds = copy hook + visual hook. Analyse both tracks in detail.

### 1a. Copy Hook
- Hook type (counterintuitive / pain point / data / scenario / suspense / benefit)
- Full verbatim transcript of the hook copy
- Relevance of copy to the product (strong / weak connection)

### 1b. Visual Hook (Frame-by-frame description)
- Frame 0: Describe the composition, tone, and main subject of the very first frame
- Visual hook type (visual spectacle / product stacking / sudden cut / action impact / text pop / first-person POV)
- Specific frame description: shot framing, tone, camera movement, effects, facial expression and actions
- Visual information density: how many information elements appear on screen simultaneously

### 1c. Copy × Visual Synergy
- Do the copy and visuals simultaneously reinforce the same message?
- Sound design: are there sound effects, BGM changes, or voice tone changes in the first 3 seconds?
- Combined hook intensity score (1–10) with reasoning

## 2. Shot Structure
Break down each shot in a table:
| Time | Shot Type | Frame Content | Voiceover / Subtitle | Transition |

## 3. Rhythm Design
- Timestamps of fast-cut segments
- Rhythm variation pattern (fast-slow-fast / gradually accelerating / pulsed)
- Alignment between BGM and visual content

## 4. Visual Elements
- Colour tone and filter style
- Subtitle style and appearance timing
- Product presentation method
- Composition characteristics

## 5. Conversion Design
- CTA type and timing
- Price anchoring strategy
- Urgency creation methods
- Conversion funnel (video → ? → ?)

## 6. Compliance Check
- Are there any absolute superlatives or prohibited expressions?
- Are efficacy claims compliant?
- Any potential review risks?

## 7. Replicable Elements
- Directly replicable: hook sentence patterns, shot structure, visual style, CTA scripts
- Not replicable: unique scenes, specific KOLs, brand authority

Please output in English, as detailed as possible.
```

---

### Step 4: Viral Formula Extraction ← User Confirmation Point

**When competitor videos are available** → Consolidate analysis results:

Read all `analysis-*.md` files and compare against the validated formulas in `references/proven-formulas.md`. Claude then synthesises:

1. **Category viral commonalities**: Success factors shared across multiple videos
2. **Hook formula**: Most effective hook types and sentence pattern templates
3. **Optimal shot structure**: Standard shot flow for the category
4. **Rhythm template**: Recommended rhythm design approach
5. **Conversion funnel**: Optimal CTA strategy
6. **Risk warnings**: Compliance issues to avoid

**When no competitor videos are available** → Use validated formulas directly:

Read `references/proven-formulas.md`, select the closest formula for the product category as a baseline. Remind the user: scripts without competitor analysis may lack category specificity — recommend sourcing competitor videos later.

**Save the consolidated summary** to `_temp/video-downloads/[product-name]-viral-analysis-summary.md`

**Present to the user for confirmation**:

- Confirm whether the analysis is accurate
- Confirm script type (seeding / ad material)
- Supplement product information (if Step 1 was incomplete)

**Formula accumulation**: After analysis is complete, append the new category's formula to `references/proven-formulas.md` for continuous knowledge building.

---

### Step 5: Script + Storyboard Generation

Generate the script based on the viral formula + product information + conversational style samples.

**Pre-generation preparation**:

1. Read `references/script-style-samples.md` for conversational style examples
2. Read the seeding vs ad material differences table in `references/analysis-dimensions.md`
3. Read the viral analysis summary from Step 4

**Script Generation Prompt Templates**:

#### Seeding Video Script

```text
You are a short-form video director specialising in seeding content.

## Task
Generate a [duration]-second seeding video script for the following product.

## Product Information
{product name, core selling points, target audience, price, brand information}

## Viral Formula (based on competitor analysis)
{Viral formula extracted in Step 4}

## Conversational Style Requirements
Reference the style characteristics of the following real scripts:
- Extremely conversational: write the way you speak; short sentences (15 words max)
- Specific data anchors: use concrete numbers, not "a lot" or "many"
- Sensory description: engage visual / tactile / taste / smell
- Emotional triggers: identity resonance, anxiety activation, scenario empathy
- Brand endorsement simplified: one sentence max
- Price anchoring + urgency

Real script examples:
{Select 1–2 examples from script-style-samples.md in the same category or similar style}

## Output Requirements

### Part A: Full Script
- First 3 seconds must have a strong hook (reference the most effective hook type from analysis)
- Middle section presents core selling points (max 3 — viewers won't remember more)
- Clear CTA at the end
- Fully conversational throughout — like a friend recommending something
- No absolute superlatives; compliant with platform ad review standards
- Annotate estimated duration for each segment

### Part B: Storyboard Table (first 3 seconds must describe the visual hook in detail)
| Shot # | Duration | Shot Type | Frame Content | Voiceover / Subtitle | Filming Notes |

⚠️ The storyboard for the first 3 seconds must include:
- Visual hook type (visual spectacle / product stacking / sudden cut / action impact / text pop / first-person POV)
- Specific frame description: composition, tone, camera movement, effects, expression and action
- First frame design: if paused at second 0, can this frame attract a click?
- Copy × visual synergy: do audio and visuals reinforce the same message simultaneously?
```

#### Paid Traffic Ad Creative Script

```text
You are an ad creative director specialising in high-conversion paid traffic material.

## Task
Write a [duration]-second paid traffic ad creative script for the following product.

## Product Information
{product name, core selling points, target audience, price, campaign objective}

## Viral Formula (based on competitor analysis)
{Viral formula extracted in Step 4}

## Conversational Style Requirements
{Same style requirements as the seeding script}

## Ad Creative Special Requirements
- First 3 seconds must have a strong hook (data-driven or pain-point based; do not open with a question)
- High information density; core selling points stated directly
- CTA must be hard: clearly guide to click / enter live stream / purchase
- No absolute superlatives; no unverified efficacy claims
- Compliant with platform ad review standards

## Output
### Part A: Full Script (with duration annotations)
### Part B: Storyboard Table
| Shot # | Duration | Frame Content | Voiceover / Subtitle | Production Notes |
```

**Save the script** to `_temp/video-downloads/[product-name]-seeding-script.md` or `[product-name]-ad-creative-script.md`

---

### Step 6: AI-Tone Proofreading ← User Confirmation Point

Conduct video-script-specific proofreading of the generated script — 5 checks:

#### Check 1: Conversational Level

Reference the video script colloquialisation rules:

- ❌ "Next, we will proceed with..." → ✅ "Let's..."
- ❌ "Perform the operation" → ✅ "Click"
- ❌ "In summary" → ✅ Just summarise directly
- Short sentences (no more than 15 words)
- Read it aloud; rewrite anywhere that makes you stumble

#### Check 2: Hook Strength

- Does the first 3 seconds have sufficient attraction?
- Is it tailored to the target audience?
- Does it create curiosity / urgency / emotional resonance?

#### Check 3: Pacing and Duration

- Are the per-segment duration annotations reasonable?
- Is the total duration within the target range?
- Is the information density appropriate? (neither overloaded nor sparse)

#### Check 4: Ad Compliance Review (Critical!)

This is the most common reason ad creative material gets rejected. Even if certain language appears in a brand's official marketing materials, the platform's review system may still reject it.

**4a. Absolute Superlatives** (must remove):

- ❌ Best / No. 1 / 100% / Absolute / Only / Top / Lowest price anywhere

**4b. Time + Efficacy Claims** (high risk — most commonly rejected):

- ❌ "Relieves sensitivity in 60 seconds" → ✅ "My mouth felt so much more comfortable right away"
- ❌ "Fades dark spots 83% in 28 days" → ✅ "Keep using it and you'll really see a difference"
- ❌ "Works in 7 days" → ✅ "After a while you can see the change"
- Rule: **Specific time + specific efficacy = must rewrite**. Remove the time reference OR remove the efficacy claim; replace with vague sensory descriptions
- Even if the data comes from official brand or clinical reports, it cannot be used directly in ad creative material

**4c. Efficacy Claim Wording**:

- ❌ Cures / Completely eliminates / Permanent fix → ✅ Alleviates / Helps improve / Feels much better
- ❌ Whitening / Acne-clearing / Anti-ageing → ✅ Brightening / Improves breakout-prone skin / Skin feels in better condition (especially for cosmetics)
- ❌ Anti-inflammatory / Antibacterial / Bacteriostatic → ✅ Feels clean and refreshing (non-medicines cannot use medical terminology)

**4d. Comparisons and Disparagement**:

- ❌ "Better than [Brand X]" or "Crushes all competitors"
- ❌ "Hospital would charge thousands" → ⚠️ Can be used cautiously, but must not imply it replaces medical treatment

**4e. Inducement and Misrepresentation**:

- ❌ "Not buying is a loss" / "Miss it and wait another year" (false urgency)
- ❌ Actors playing product users or experts without disclosure

**Rewrite principle**: Replace third-person data with first-person sensory descriptions. "After using it I felt..." is far safer than "Clinically proven to..."

#### Check 5: AI-Tone Check

Reference the 6 categories of AI-sounding language:

- ❌ Filler phrases: "In today's era", "It is worth noting"
- ❌ AI sentence patterns: "Not... but..." / "Not only... but also..." used repeatedly
- ❌ Formal vocabulary: "Significantly improve", "Fully leverage"
- ❌ Mechanical structure: Overuse of "Firstly, secondly, finally"
- ❌ Neutral stance: "It depends on the actual situation"
- ❌ Lacking detail: Too many big words, too few specific details

**After proofreading**, show the list of changes to the user for confirmation, then apply the changes.

---

## File Saving Conventions

All intermediate outputs and final deliverables are saved in `_temp/video-downloads/`:

```text
_temp/video-downloads/
├── video-1-[ID].mp4               # Downloaded video
├── video-2-[ID].mp4
├── analysis-1.md                   # Video analysis results
├── analysis-2.md
├── [product-name]-viral-analysis-summary.md  # Multi-video consolidated summary
├── [product-name]-seeding-script.md          # Final seeding script
└── [product-name]-ad-creative-script.md      # Final ad creative script
```

## Reference Resources

| Resource | Path | Purpose |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-douyin-script
description: |
  Short video viral script creation workflow. End-to-end process from competitor video breakdown to script generation: download Douyin videos → Gemini video analysis → viral formula extraction → script + storyboard generation → AI-tone proofreading.
  Use when the user mentions "short video script", "viral breakdown", "competitor analysis", "promotional script", "ad material", "seeding script", "video breakdown", or "short video analysis".
---

# Short Video Viral Script Creation

A complete workflow from competitor video breakdown to script generation. Transforms "copy viral videos by instinct" into "AI-powered systematic breakdown + structured replication".

## Environment Requirements

- `uv` (Python package manager)
- `yt-dlp` (video download — `pip install yt-dlp` or `brew install yt-dlp`)
- `GEMINI_API_KEY` environment variable (for Gemini video analysis — get from <https://aistudio.google.com/apikey>)
- Chrome browser signed into the relevant platform (to extract download cookies)

**Path convention**: `SKILL_DIR` in the instructions below refers to the absolute path of the directory containing this SKILL.md file. Before running scripts, use `dirname` or a Glob tool to determine the actual location of SKILL.md and replace `SKILL_DIR`.

## 6-Step Workflow

### Step 1: Collect Inputs

Gather the following from the user:

**Required**:

- Video links (1–5 benchmark / competitor videos)
- Product information (name, core selling points, target audience, price)
- Script type: Seeding video OR ad creative / paid traffic material

**Optional**:

- Product images (for visual reference in the script)
- Target duration (seeding default: 30 seconds; ad material default: 15 seconds)
- Brand tone requirements
- Campaign objective (live-stream traffic / product page / follow conversion)

If the user has only provided partial information, proactively ask for what's missing.

---

### Step 2: Download Videos

Run the download script:

```bash
uv run SKILL_DIR/scripts/download_video.py \
  --urls "URL1" "URL2" \
  --output-dir _temp/video-downloads
```

**Parameters**:

- `--urls`: Supports short links, page links, and share text (auto-extracts URL)
- `--output-dir`: Defaults to `_temp/video-downloads/` in the current working directory
- `--cookies-browser`: Default `chrome`; options include `edge` / `firefox`

**If download fails**:

1. Prompt the user to confirm Chrome is signed into the platform
2. Suggest manually downloading the video into `_temp/video-downloads/`
3. If a relevant MCP server is available, try downloading via MCP

---

### Step 3: Gemini Video Analysis (Can Be Parallelised)

For each successfully downloaded video, call Gemini video analysis:

```bash
uv run SKILL_DIR/scripts/analyze_video.py \
  --video "_temp/video-downloads/video-1-xxx.mp4" \
  --prompt "PROMPT_BELOW" \
  --model flash \
  --resolution medium \
  --output "_temp/video-downloads/analysis-1.md"
```

**Use the flash model + medium resolution** (sufficient for short videos; saves cost).

**Multiple videos can be analysed in parallel** (use `run_in_background=true`).

**Viral Analysis Prompt** (pass in via `--prompt`):

```text
As a senior short-form video e-commerce analyst, conduct a 7-dimension in-depth breakdown of this video.
Special focus: the first 3 seconds are the most critical part — break them down at a near-frame-by-frame level.

## 1. Hook Analysis (First 3 Seconds) ⭐ Most Critical
The first 3 seconds = copy hook + visual hook. Analyse both tracks in detail.

### 1a. Copy Hook
- Hook type (counterintuitive / pain point / data / scenario / suspense / benefit)
- Full verbatim transcript of the hook copy
- Relevance of copy to the product (strong / weak connection)

### 1b. Visual Hook (Frame-by-frame description)
- Frame 0: Describe the composition, tone, and main subject of the very first frame
- Visual hook type (visual spectacle / product stacking / sudden cut / action impact / text pop / first-person POV)
- Specific frame description: shot framing, tone, camera movement, effects, facial expression and actions
- Visual information density: how many information elements appear on screen simultaneously

### 1c. Copy × Visual Synergy
- Do the copy and visuals simultaneously reinforce the same message?
- Sound design: are there sound effects, BGM changes, or voice tone changes in the first 3 seconds?
- Combined hook intensity score (1–10) with reasoning

## 2. Shot Structure
Break down each shot in a table:
| Time | Shot Type | Frame Content | Voiceover / Subtitle | Transition |

## 3. Rhythm Design
- Timestamps of fast-cut segments
- Rhythm variation pattern (fast-slow-fast / gradually accelerating / pulsed)
- Alignment between BGM and visual content

## 4. Visual Elements
- Colour tone and filter style
- Subtitle style and appearance timing
- Product presentation method
- Composition characteristics

## 5. Conversion Design
- CTA type and timing
- Price anchoring strategy
- Urgency creation methods
- Conversion funnel (video → ? → ?)

## 6. Compliance Check
- Are there any absolute superlatives or prohibited expressions?
- Are efficacy claims compliant?
- Any potential review risks?

## 7. Replicable Elements
- Directly replicable: hook sentence patterns, shot structure, visual style, CTA scripts
- Not replicable: unique scenes, specific KOLs, brand authority

Please output in English, as detailed as possible.
```

---

### Step 4: Viral Formula Extraction ← User Confirmation Point

**When competitor videos are available** → Consolidate analysis results:

Read all `analysis-*.md` files and compare against the validated formulas in `references/proven-formulas.md`. Claude then synthesises:

1. **Category viral commonalities**: Success factors shared across multiple videos
2. **Hook formula**: Most effective hook types and sentence pattern templates
3. **Optimal shot structure**: Standard shot flow for the category
4. **Rhythm template**: Recommended rhythm design approach
5. **Conversion funnel**: Optimal CTA strategy
6. **Risk warnings**: Compliance issues to avoid

**When no competitor videos are available** → Use validated formulas directly:

Read `references/proven-formulas.md`, select the closest formula for the product category as a baseline. Remind the user: scripts without competitor analysis may lack category specificity — recommend sourcing competitor videos later.

**Save the consolidated summary** to `_temp/video-downloads/[product-name]-viral-analysis-summary.md`

**Present to the user for confirmation**:

- Confirm whether the analysis is accurate
- Confirm script type (seeding / ad material)
- Supplement product information (if Step 1 was incomplete)

**Formula accumulation**: After analysis is complete, append the new category's formula to `references/proven-formulas.md` for continuous knowledge building.

---

### Step 5: Script + Storyboard Generation

Generate the script based on the viral formula + product information + conversational style samples.

**Pre-generation preparation**:

1. Read `references/script-style-samples.md` for conversational style examples
2. Read the seeding vs ad material differences table in `references/analysis-dimensions.md`
3. Read the viral analysis summary from Step 4

**Script Generation Prompt Templates**:

#### Seeding Video Script

```text
You are a short-form video director specialising in seeding content.

## Task
Generate a [duration]-second seeding video script for the following product.

## Product Information
{product name, core selling points, target audience, price, brand information}

## Viral Formula (based on competitor analysis)
{Viral formula extracted in Step 4}

## Conversational Style Requirements
Reference the style characteristics of the following real scripts:
- Extremely conversational: write the way you speak; short sentences (15 words max)
- Specific data anchors: use concrete numbers, not "a lot" or "many"
- Sensory description: engage visual / tactile / taste / smell
- Emotional triggers: identity resonance, anxiety activation, scenario empathy
- Brand endorsement simplified: one sentence max
- Price anchoring + urgency

Real script examples:
{Select 1–2 examples from script-style-samples.md in the same category or similar style}

## Output Requirements

### Part A: Full Script
- First 3 seconds must have a strong hook (reference the most effective hook type from analysis)
- Middle section presents core selling points (max 3 — viewers won't remember more)
- Clear CTA at the end
- Fully conversational throughout — like a friend recommending something
- No absolute superlatives; compliant with platform ad review standards
- Annotate estimated duration for each segment

### Part B: Storyboard Table (first 3 seconds must describe the visual hook in detail)
| Shot # | Duration | Shot Type | Frame Content | Voiceover / Subtitle | Filming Notes |

⚠️ The storyboard for the first 3 seconds must include:
- Visual hook type (visual spectacle / product stacking / sudden cut / action impact / text pop / first-person POV)
- Specific frame description: composition, tone, camera movement, effects, expression and action
- First frame design: if paused at second 0, can this frame attract a click?
- Copy × visual synergy: do audio and visuals reinforce the same message simultaneously?
```

#### Paid Traffic Ad Creative Script

```text
You are an ad creative director specialising in high-conversion paid traffic material.

## Task
Write a [duration]-second paid traffic ad creative script for the following product.

## Product Information
{product name, core selling points, target audience, price, campaign objective}

## Viral Formula (based on competitor analysis)
{Viral formula extracted in Step 4}

## Conversational Style Requirements
{Same style requirements as the seeding script}

## Ad Creative Special Requirements
- First 3 seconds must have a strong hook (data-driven or pain-point based; do not open with a question)
- High information density; core selling points stated directly
- CTA must be hard: clearly guide to click / enter live stream / purchase
- No absolute superlatives; no unverified efficacy claims
- Compliant with platform ad review standards

## Output
### Part A: Full Script (with duration annotations)
### Part B: Storyboard Table
| Shot # | Duration | Frame Content | Voiceover / Subtitle | Production Notes |
```

**Save the script** to `_temp/video-downloads/[product-name]-seeding-script.md` or `[product-name]-ad-creative-script.md`

---

### Step 6: AI-Tone Proofreading ← User Confirmation Point

Conduct video-script-specific proofreading of the generated script — 5 checks:

#### Check 1: Conversational Level

Reference the video script colloquialisation rules:

- ❌ "Next, we will proceed with..." → ✅ "Let's..."
- ❌ "Perform the operation" → ✅ "Click"
- ❌ "In summary" → ✅ Just summarise directly
- Short sentences (no more than 15 words)
- Read it aloud; rewrite anywhere that makes you stumble

#### Check 2: Hook Strength

- Does the first 3 seconds have sufficient attraction?
- Is it tailored to the target audience?
- Does it create curiosity / urgency / emotional resonance?

#### Check 3: Pacing and Duration

- Are the per-segment duration annotations reasonable?
- Is the total duration within the target range?
- Is the information density appropriate? (neither overloaded nor sparse)

#### Check 4: Ad Compliance Review (Critical!)

This is the most common reason ad creative material gets rejected. Even if certain language appears in a brand's official marketing materials, the platform's review system may still reject it.

**4a. Absolute Superlatives** (must remove):

- ❌ Best / No. 1 / 100% / Absolute / Only / Top / Lowest price anywhere

**4b. Time + Efficacy Claims** (high risk — most commonly rejected):

- ❌ "Relieves sensitivity in 60 seconds" → ✅ "My mouth felt so much more comfortable right away"
- ❌ "Fades dark spots 83% in 28 days" → ✅ "Keep using it and you'll really see a difference"
- ❌ "Works in 7 days" → ✅ "After a while you can see the change"
- Rule: **Specific time + specific efficacy = must rewrite**. Remove the time reference OR remove the efficacy claim; replace with vague sensory descriptions
- Even if the data comes from official brand or clinical reports, it cannot be used directly in ad creative material

**4c. Efficacy Claim Wording**:

- ❌ Cures / Completely eliminates / Permanent fix → ✅ Alleviates / Helps improve / Feels much better
- ❌ Whitening / Acne-clearing / Anti-ageing → ✅ Brightening / Improves breakout-prone skin / Skin feels in better condition (especially for cosmetics)
- ❌ Anti-inflammatory / Antibacterial / Bacteriostatic → ✅ Feels clean and refreshing (non-medicines cannot use medical terminology)

**4d. Comparisons and Disparagement**:

- ❌ "Better than [Brand X]" or "Crushes all competitors"
- ❌ "Hospital would charge thousands" → ⚠️ Can be used cautiously, but must not imply it replaces medical treatment

**4e. Inducement and Misrepresentation**:

- ❌ "Not buying is a loss" / "Miss it and wait another year" (false urgency)
- ❌ Actors playing product users or experts without disclosure

**Rewrite principle**: Replace third-person data with first-person sensory descriptions. "After using it I felt..." is far safer than "Clinically proven to..."

#### Check 5: AI-Tone Check

Reference the 6 categories of AI-sounding language:

- ❌ Filler phrases: "In today's era", "It is worth noting"
- ❌ AI sentence patterns: "Not... but..." / "Not only... but also..." used repeatedly
- ❌ Formal vocabulary: "Significantly improve", "Fully leverage"
- ❌ Mechanical structure: Overuse of "Firstly, secondly, finally"
- ❌ Neutral stance: "It depends on the actual situation"
- ❌ Lacking detail: Too many big words, too few specific details

**After proofreading**, show the list of changes to the user for confirmation, then apply the changes.

---

## File Saving Conventions

All intermediate outputs and final deliverables are saved in `_temp/video-downloads/`:

```text
_temp/video-downloads/
├── video-1-[ID].mp4               # Downloaded video
├── video-2-[ID].mp4
├── analysis-1.md                   # Video analysis results
├── analysis-2.md
├── [product-name]-viral-analysis-summary.md  # Multi-video consolidated summary
├── [product-name]-seeding-script.md          # Final seeding script
└── [product-name]-ad-creative-script.md      # Final ad creative script
```

## Reference Resources

| Resource | Path | Purpose |
|----------|------|---------|
| Analysis dimension framework | `references/analysis-dimensions.md` | 7-dimension analysis + seeding vs ad material differences |
| Validated viral formulas | `references/proven-formulas.md` | Category formula library; baseline when no competitor videos are available |
| Conversational style samples | `references/script-style-samples.md` | Few-shot examples for script generation |
| Video download script | `scripts/download_video.py` | Video download (yt-dlp) |
| Gemini video analysis | `scripts/analyze_video.py` | Video comprehension and breakdown (built-in) |
| AI-tone proofreading rules | Embedded in Step 6 | 6 AI-tone identification categories |
| Script colloquialisation | Embedded in Step 6 | Conversational rewriting rules |

## Quick Guide

**When competitor videos are available** ("Help me break down these videos and write a script"):

1. Collect links and product information (Step 1)
2. Download + analysis can be parallelised (Steps 2–3)
3. Present analysis summary, confirm direction (Step 4)
4. Generate script, confirm then proofread (Steps 5–6)
5. Append the new category formula to `references/proven-formulas.md`

**When no competitor videos are available** ("Write me a seeding script for XX product"):

1. Collect product information (Step 1 — skip video links)
2. Skip Steps 2–3
3. Select category formula from `references/proven-formulas.md` (Step 4)
4. Generate script, confirm then proofread (Steps 5–6)

Total time: ~15–20 minutes with videos; ~5–10 minutes without.

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Analysis dimension framework | `references/analysis-dimensions.md` | 7-dimension analysis + seeding vs ad material differences |
| Validated viral formulas | `references/proven-formulas.md` | Category formula library; baseline when no competitor videos are available |
| Conversational style samples | `references/script-style-samples.md` | Few-shot examples for script generation |
| Video download script | `scripts/download_video.py` | Video download (yt-dlp) |
| Gemini video analysis | `scripts/analyze_video.py` | Video comprehension and breakdown (built-in) |
| AI-tone proofreading rules | Embedded in Step 6 | 6 AI-tone identification categories |
| Script colloquialisation | Embedded in Step 6 | Conversational rewriting rules |

## Quick Guide

**When competitor videos are available** ("Help me break down these videos and write a script"):

1. Collect links and product information (Step 1)
2. Download + analysis can be parallelised (Steps 2–3)
3. Present analysis summary, confirm direction (Step 4)
4. Generate script, confirm then proofread (Steps 5–6)
5. Append the new category formula to `references/proven-formulas.md`

**When no competitor videos are available** ("Write me a seeding script for XX product"):

1. Collect product information (Step 1 — skip video links)
2. Skip Steps 2–3
3. Select category formula from `references/proven-formulas.md` (Step 4)
4. Generate script, confirm then proofread (Steps 5–6)

Total time: ~15–20 minutes with videos; ~5–10 minutes without.

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Analysis dimension framework | `references/analysis-dimensions.md` | 7-dimension analysis + seeding vs ad material differences |
| Validated viral formulas | `references/proven-formulas.md` | Category formula library; baseline when no competitor videos are available |
| Conversational style samples | `references/script-style-samples.md` | Few-shot examples for script generation |
| Video download script | `scripts/download_video.py` | Video download (yt-dlp) |
| Gemini video analysis | `scripts/analyze_video.py` | Video comprehension and breakdown (built-in) |
| AI-tone proofreading rules | Embedded in Step 6 | 6 AI-tone identification categories |
| Script colloquialisation | Embedded in Step 6 | Conversational rewriting rules |

## Quick Guide

**When competitor videos are available** ("Help me break down these videos and write a script"):

1. Collect links and product information (Step 1)
2. Download + analysis can be parallelised (Steps 2–3)
3. Present analysis summary, confirm direction (Step 4)
4. Generate script, confirm then proofread (Steps 5–6)
5. Append the new category formula to `references/proven-formulas.md`

**When no competitor videos are available** ("Write me a seeding script for XX product"):

1. Collect product information (Step 1 — skip video links)
2. Skip Steps 2–3
3. Select category formula from `references/proven-formulas.md` (Step 4)
4. Generate script, confirm then proofread (Steps 5–6)

Total time: ~15–20 minutes with videos; ~5–10 minutes without.

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
