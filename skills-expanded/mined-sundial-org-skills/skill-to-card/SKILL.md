---
name: skill-to-card
description: End-to-end workflow that creates a skill from a description and attached files, publishes it to Sundial as a private skill, generates a trading card (front + back with QR code), and sends it to a printer. Use when the user wants to create a skill and get a printed trading card, or says "skill to card", "create and print a skill card", "make me a skill with a card".
---

# Skill-to-Card Pipeline

Creates a skill, publishes it privately to Sundial, generates a trading card, and prints it.

## Step 1: Create the Skill

Gather from the user: what the skill should do, concrete usage examples, and any attached files/context.

Read [references/skill-creation-guide.md](references/skill-creation-guide.md) for the full skill creation spec — anatomy, frontmatter rules, body writing guidelines, and design patterns. Follow it exactly.

Use a YAML-safe frontmatter description format for long text:
```yaml
---
name: skill-name
description: >-
  What the skill does and when to use it. Trigger phrases include:
  "example one", "example two", "example three".
---
```

Validate frontmatter before push:
```bash
npx -y -p gray-matter node -e '
const fs = require("fs");
const matter = require("gray-matter");
const file = process.argv[1];
const src = fs.readFileSync(file, "utf8");
const { data } = matter(src);
if (!data.name || !data.description) {
  throw new Error("SKILL.md frontmatter must include name + description");
}
console.log("Frontmatter OK");
' /absolute/path/to/skill-dir/SKILL.md
```

## Step 2: Publish to Sundial (Private)

1. Authenticate via env var (preferred) or interactive login:
   ```bash
   # Option A: env var (no interactive login needed)
   export SUNDIAL_TOKEN="your-token-here"
   # Option B: interactive
   npx sundial-hub auth login
   ```

2. Push as private. Use an **absolute path** to the skill directory. Categories are **space-separated** (not comma-separated):
   ```bash
   npx sundial-hub push /absolute/path/to/skill-dir \
     --version 1.0.0 \
     --changelog "Initial release" \
     --visibility private \
     --categories creative writing
   ```

   Valid categories (pick 1-3): `product`, `research`, `outreach`, `marketing`, `admin`, `health`, `creative`, `financial`, `learning`, `community`, `coding`, `writing`, `other`.

   The push output looks like:
   ```
   ✔ Created skill-name v1 on the hub
   View on hub: https://www.sundialhub.com/AUTHOR/SKILL_NAME
   Push complete!
   Skill page: https://www.sundialhub.com/AUTHOR/SKILL_NAME
   ```
   Parse the author and skill name from this output.

   **Important**: There is no `info` or `show --json` command. Do NOT try `npx sundial-hub info` — it doesn't exist.

3. After push, fetch generated metadata (including `use_cases`) via the API:
   ```bash
   curl -s "https://www.sundialhub.com/api/hub/skills/by-author-name/AUTHOR/SKILL_NAME" \
     -H "Authorization: Bearer $SUNDIAL_TOKEN" | python3 -m json.tool
   ```
   The response JSON has this structure:
   ```json
   {
     "skill": {
       "name": "skill-name",
       "author": "author-name",
       "description": "...",
       "use_cases": [
         {"title": "Power Name", "desc": "What it does", "icon": "emoji"},
         ...
       ]
     }
   }
   ```
   `use_cases` are generated server-side from the skill content. Extract them for the card's Powers.
   For cards, do **not** pass all use cases:
   - Keep only **2 or 3** total powers
   - If 3+ exist, use the first 3
   - If only 2 exist, use both
   - Never pass more than 3 `--powers` arguments

## Step 3: Generate Trading Card

Use the bundled script to generate both front and back. You **MUST** pass `--reference-front` and `--reference-back` explicitly — do NOT rely on defaults, they won't resolve correctly.

First, locate the template files bundled with this skill:
- `templates/reference-front.jpg` — the canonical front card style (cartoon/anime, warm golden)
- `templates/reference-back.png` — the canonical back card with QR code area

Then run:

```bash
uv run SKILL_DIR/scripts/generate_single_card.py \
  --name "Skill Display Name" \
  --author "author-name" \
  --slug "author/skill-name" \
  --reference-front SKILL_DIR/templates/reference-front.jpg \
  --reference-back SKILL_DIR/templates/reference-back.png \
  --character "vivid character description matching the skill's theme — a person or creature with visual elements that represent what the skill does, wearing themed attire, dynamic pose" \
  --powers "emoji **Power Title** -- Power description" \
  --powers "emoji **Power Title** -- Power description" \
  --powers "emoji **Power Title** -- Power description" \
  --rarity Common \
  --qr-url "https://sundialhub.com/author/skill-name" \
  --side both \
  --output-dir /tmp/trading-cards/skill-name
```

Where `SKILL_DIR` is the absolute path to this skill-to-card directory. Use absolute paths for all file arguments.

### Card data mapping
- **name**: Skill display name (title case)
- **author**: From API response `skill.author`
- **slug**: `author/skill-name`
- **powers**: Map only the selected 2-3 card use cases to: `"{icon} **{title}** -- {desc}"`. Pass each as a separate `--powers` argument (2 or 3 total).
- **character**: Invent a vivid fantasy character matching the skill's theme. Include appearance, outfit with skill-themed elements, pose, and expression.
- **rarity**: New skills default to Common.
- **url**: `https://sundialhub.com/{slug}` — used for QR code on card back

### Requirements
- `GEMINI_API_KEY` env var must be set
- Templates are bundled at `templates/reference-front.jpg` and `templates/reference-back.png`

## Step 4: Print the Card

> **Printer connection TBD**

```bash
# Placeholder — replace with actual printer command when connected
# print-card --front /tmp/trading-cards/{name}-common.png \
#            --back /tmp/trading-cards/{name}-common-back.png \
#            --printer PRINTER_NAME
echo "Card images saved to /tmp/trading-cards/{skill-name}/"
```

Show the user the generated card images and inform them where the files are saved.
