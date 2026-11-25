---
name: brand-voice-generator
description: |
  Generate tone-of-voice and brand-system files for use with the PPTX Generator and other brand-aware skills.

  TRIGGERS - Use this skill when user says:
  - "help me create a brand system" / "set up my brand"
  - "generate my tone of voice" / "create my voice guidelines"
  - "configure my brand for presentations" / "set up brand for slides"
  - "create brand files" / "initialize my brand"
  - Any request about defining brand identity, voice, or visual system for content creation

  Creates brand.json, config.json, brand-system.md, and tone-of-voice.md files.
---

# Brand & Voice Generator

Generate complete brand configuration files for content creation skills (PPTX Generator, Excalidraw diagrams, document generation, social media). This skill guides users through defining their brand identity and writing voice, then produces four standardized files that all brand-aware skills consume.

## What This Creates

| File | Purpose | Used By |
|------|---------|---------|
| `brand.json` | Colors, fonts, assets — machine-readable design tokens | PPTX Generator, Excalidraw, any skill reading brand colors/fonts |
| `config.json` | Output settings (directories, slide dimensions) | PPTX Generator |
| `brand-system.md` | Design philosophy, visual guidelines, signature elements | All content skills needing visual direction |
| `tone-of-voice.md` | Writing voice, vocabulary, banned words, tone calibration | Any skill generating text content |

## Output Location

Default location (project-local, works with PPTX Generator):
```
.claude/brands/{brand-name}/
```

Brand files are stored relative to the project root. The PPTX Generator and other brand-aware skills look for brands at `.claude/brands/` by default.

Always create an `assets/` subdirectory for logos and icons.

---

## How This Works

The process has three phases. The goal is to minimize back-and-forth — extract as much as possible from what the user already told you, use smart defaults for the rest, and only ask about things that genuinely need human input.

### Phase 1: Extract & Infer

Before asking any questions, analyze what the user already provided. Users often pack a lot of information into their initial message. Look for:

- **Brand name** — Any proper noun or quoted name
- **Industry/domain** — What they do (SaaS, education, consulting, etc.)
- **Colors** — Any hex codes, color names, or theme preferences (dark/light)
- **Personality** — Adjectives describing their brand or communication style
- **Voice influences** — Names of creators, brands, or people they admire
- **Anti-patterns** — Things they want to avoid ("I hate corporate speak")
- **Style preferences** — Sentence length, contractions, formality level
- **Quick mode signals** — "just the basics", "quick setup", "get started fast", "minimal"

Build a mental model of what you know vs. what you need. If the user gave you a name, a color, and said "dark theme" — that's enough for Quick Mode.

### Phase 2: Fill the Gaps

Ask only for what you couldn't infer. Batch your questions into a single message rather than asking one at a time. Here's what you need and how to prioritize:

**Always needed** (ask if not provided):
- Brand name (folder name: lowercase, hyphens, no spaces)
- At least one accent color (hex code)
- Dark or light theme preference

**Ask only if doing a full setup** (skip for Quick Mode):
- 3 personality words
- Voice influences (2-3 creators/brands they admire)
- What to avoid (tone, phrases, patterns)
- Sentence style preference

**Use defaults for** (don't ask unless user seems particular):
- Typography (default: Inter / Inter / JetBrains Mono)
- Full 10-color palette (generate from accent + theme)
- Assets (default: null, remind them to add later)
- Design principles (infer from personality + industry)

**Example batched question for full setup:**
> "I'll set up your brand files. I just need a few things:
> 1. Brand name for the folder (lowercase with hyphens, like 'my-brand')
> 2. Your signature color (hex code)
> 3. Dark or light theme?
> 4. Describe your brand personality in 3 words
> 5. Any creators or brands whose communication style you admire?"

### Phase 3: Generate

Once you have enough information, generate all four files. Don't ask for confirmation before generating — just produce the files and tell the user what you created. They can refine afterwards.

---

## Quick Mode

Trigger when the user says "just the basics", "quick setup", "minimal", or provides only a name and color. Quick Mode needs just three things:

1. Brand name
2. Signature color
3. Dark or light theme

Generate everything else from smart defaults based on industry context. Read `reference/color-presets.md` for pre-built color palettes — pick the closest match to their accent color and theme, then swap in their actual accent.

**Industry-aware voice defaults:**

| Industry | Personality | Voice Style | Influences |
|----------|-------------|-------------|------------|
| B2B SaaS | Clear, Confident, Practical | Professional but human | Stripe, Linear, Basecamp |
| Developer tools | Technical, Direct, Honest | Dev-to-dev, no fluff | Fireship, Vercel, Hashicorp |
| Education | Approachable, Clear, Patient | Mentor-to-student | 3Blue1Brown, Fireship |
| Creative/Design | Bold, Expressive, Authentic | Confident and opinionated | Apple, Figma |
| Consulting | Authoritative, Measured, Trustworthy | Expert-to-peer | McKinsey, HBR |

After generating Quick Mode files, tell the user:
> "Brand files created. Run this skill again anytime to refine your voice, colors, or design philosophy."

---

## Generating the Files

### brand.json

All color hex codes are stored WITHOUT the `#` prefix. This is important — downstream tools expect bare hex values.

```json
{
  "name": "{display_name}",
  "description": "{one_line_description}",

  "colors": {
    "background": "0B0F1A",
    "background_alt": "0E1225",
    "text": "F5F5F5",
    "text_secondary": "B0B8C9",
    "accent": "2563EB",
    "accent_secondary": "3B82F6",
    "accent_tertiary": "60A5FA",
    "code_bg": "080B14",
    "card_bg": "131829",
    "card_bg_alt": "1A2035"
  },

  "fonts": {
    "heading": "Inter",
    "body": "Inter",
    "code": "JetBrains Mono"
  },

  "assets": {
    "logo": null,
    "logo_dark": null,
    "icon": null
  }
}
```

**Building the 10-color palette from a single accent:**
1. `accent` — the user's provided color, stored without `#`
2. `accent_secondary` — lighter variant (shift toward white by ~15%)
3. `accent_tertiary` — even lighter (shift by ~30%) or a complementary hue
4. For dark themes: backgrounds in the `0a0a0a`–`1a1a2e` range, text in `f0f0f0`–`ffffff`
5. For light themes: backgrounds in `ffffff`–`f8f9fa` range, text in `111827`–`333333`
6. `code_bg` — slightly darker than background
7. `card_bg` / `card_bg_alt` — between background and text

Read `reference/color-presets.md` for complete palettes to use as starting points.

### config.json

```json
{
  "output": {
    "directory": "output/{brand_folder_name}",
    "naming": "{name}-{date}",
    "keep_parts": false
  },
  "generation": {
    "slides_per_batch": 5,
    "auto_combine": true,
    "open_after_generate": false
  },
  "defaults": {
    "slide_width_inches": 13.333,
    "slide_height_inches": 7.5
  }
}
```

### tone-of-voice.md

This is the highest-value file. A good tone-of-voice document makes every piece of generated content sound like the brand. Use `reference/tone-template.md` as the structure, but focus on making the content specific and actionable:

**What makes a great tone-of-voice file:**
- **Concrete vocabulary patterns** — actual words and phrases to use, not abstract descriptions
- **A banned-word replacement table** — mapping corporate/filler words to preferred alternatives (e.g., "leverage" → "use", "utilize" → "use", "synergize" → remove entirely). This is one of the most useful sections because it gives clear, unambiguous guidance.
- **Tone-by-context calibration** — how the voice shifts across different content types (presentations vs. social media vs. documentation)
- **Real example phrases** — headlines, CTAs, and descriptions written in the brand's actual voice
- **A pre-publish checklist** — 4-5 questions to ask before publishing anything

Read `reference/voice-templates.md` for example voice configurations.

### brand-system.md

Use `reference/brand-template.md` as the structure. Key sections:
- Brand philosophy with 3-4 core principles
- Color system documentation with usage guidance
- Typography rules
- Signature visual elements (suggest based on theme: glass effects for dark, clean shadows for light)
- Diagram color palette

---

## Updating an Existing Brand

When the user wants to modify an existing brand:

1. **Read ALL existing files first** — brand.json, config.json, brand-system.md, tone-of-voice.md
2. **Identify what's changing** — ask if unclear: "Do you want to update colors, voice, or everything?"
3. **Change only what was requested** — this is critical. If updating colors:
   - Update all 10 color values in brand.json
   - Update color references in brand-system.md
   - Preserve ALL accent colors if the user only asked for theme change (don't silently modify secondary/tertiary accents)
   - Leave tone-of-voice.md completely untouched
   - Leave config.json untouched
   - Update the theme-related design principles (e.g., "Dark Mode First" → "Light Mode First")
4. **Update the date** in any modified files

---

## Verification

After generating files:

1. List created files to confirm all four exist
2. If logo was mentioned, remind: "Copy your logo to the `assets/` folder in your brand directory"
3. Suggest a test: "Try: 'Create a 3-slide presentation for {brand-name} about [topic]'"
