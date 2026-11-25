---
name: printnest-worksheets-lite
description: Free Claude Code Skill that generates educational worksheet PDFs for Etsy/TPT/KDP sellers. Includes 5 worksheet types — Kindergarten Math, Alphabet Tracing Pre-K, Sight Words 100, Phonics CVC, Cursive Handwriting. Pure Python (zero AI image cost). Pro version with 40+ types available separately. Triggers on "worksheets", "PrintNest", "worksheet PDF", "Math Workbook", "Alphabet Tracing".
---

# PrintNest Worksheets — LITE (Free)

A free Claude Code Skill for educational printable PDF sellers. Generates 5 worksheet types via pure Python + ReportLab — no AI image cost.

> 💎 **40+ worksheet types in the Pro version** → https://synishida.gumroad.com/l/printnest-worksheets-pro

## Setup (one time)

```bash
pip3 install reportlab Pillow
python3 ~/.claude/skills/printnest-worksheets-lite/setup.py
```

`setup.py` asks for your brand name + Etsy shop URL once, then injects them into every generated PDF.

## Generators (5 included)

```bash
python3 ~/.claude/skills/printnest-worksheets-lite/scripts/generate_math.py --book math_kg
python3 ~/.claude/skills/printnest-worksheets-lite/scripts/generate_alphabet.py --book alphabet_prek
python3 ~/.claude/skills/printnest-worksheets-lite/scripts/generate_sightwords.py --book sightwords
python3 ~/.claude/skills/printnest-worksheets-lite/scripts/generate_phonics_cvc.py --book phonics_cvc
python3 ~/.claude/skills/printnest-worksheets-lite/scripts/generate_cursive.py --book cursive_handwriting
```

Or just ask Claude:

> "Make me a Kindergarten Math Workbook"
> "Generate an Alphabet Tracing Pre-K workbook"

## Output

```
~/Desktop/PrintNest/{book_id}/
├── {book_id}_workbook.pdf       ← upload to Etsy/TPT/KDP
```

For Etsy thumbnails + listing copy, use:

```bash
python3 ~/.claude/skills/printnest-worksheets-lite/scripts/make_thumbnails_universal.py --book math_kg
python3 ~/.claude/skills/printnest-worksheets-lite/scripts/make_listing_universal.py --book math_kg
```

## Commercial use

All PDFs you generate with this skill can be **sold commercially anywhere** (Etsy / TPT / KDP / Gumroad / your own site). Free forever for personal and commercial use.

## Upgrade to Pro (40+ types)

The Pro version unlocks **40+ additional worksheet types** — Multiplication, Fractions, Money Math, Sudoku, Mazes, Word Search, Cryptogram, Sentence Building, Reading Comprehension, Recipes, and many more.

→ **https://synishida.gumroad.com/l/printnest-worksheets-pro**
