---
name: arabic-presentations
description: Create, edit, repair, and validate Arabic-first or Arabic-English PowerPoint decks with native editable PPTX text, paragraph-level RTL, correct mixed Arabic/Latin/number behavior, native bullets, Arabic language metadata, and PowerPoint-first QA. Use together with the Presentations skill whenever a deck contains Arabic, requires RTL or bilingual slides, must remain editable as .pptx, or renders Arabic differently in PowerPoint, Keynote, Google Slides, or Codex preview.
---

# Arabic Presentations

Build the deck with `Presentations:Presentations`; use this skill as the stricter Arabic text and compatibility layer. Follow all content, design, workspace, implementation, and visual-QA rules in the Presentations skill. Where Arabic text handling or renderer confidence differs, follow this skill.

This public release targets Codex. It requires Codex's bundled Presentations skill and Python 3.

## Reliability contract

Treat editable PPTX as the source artifact and PowerPoint desktop as its canonical viewer.

- Store text in normal logical Unicode order. Never reverse Arabic characters, words, or lines.
- Never wrap Arabic or Latin tokens with Unicode bidi controls such as RLE/PDF, RLI/PDI, LRI/PDI, LRM, or RLM.
- Set native DrawingML direction on every Arabic paragraph: `<a:pPr rtl="1">`.
- Set native text-body direction on every Arabic text body: `<a:bodyPr rtlCol="1">`.
- Right-align Arabic body text explicitly. Preserve intentional centered or justified alignment.
- Set Arabic run language metadata, normally `ar-SA`, and a complex-script font slot when a typeface is explicit.
- Use native PowerPoint bullets; do not ship a typed `•` at the start of a paragraph.
- Keep each paragraph to one base direction. Put long English passages, URLs, citations, and code in separate LTR text boxes.
- Do not promise identical fonts across computers. Use an Arabic-capable font, disclose substitution risk when relevant, and provide PDF when fixed appearance matters.

Read [references/authoring.md](references/authoring.md) before authoring Arabic or bilingual text. Read [references/qa.md](references/qa.md) before final QA or when diagnosing cross-application differences.

## Workflow

### 1. Author with the Presentations skill

Create or edit the deck using `Presentations:Presentations` and `@oai/artifact-tool`. Write plain strings without bidi wrappers. A newline may create several PowerPoint paragraphs; the normalization step must fix each paragraph independently.

Prefer separate text boxes when Arabic and English have different semantic roles. For short mixed phrases, keep the intended logical order, for example:

```text
بلغ النمو 25% في Q4 2026.
C4ISR يربط القيادة بالاستطلاع.
```

For lists, use the engine's native list API when available. If the engine only emits typed bullet characters, allow them in the raw draft and convert them during normalization.

### 2. Export a raw draft

Export to a scratch file such as `$TMP_DIR/deck.raw.pptx`. Reserve the requested final filename for the normalized file.

### 3. Normalize the PPTX

Run:

```bash
ARABIC_SKILL="${ARABIC_PRESENTATIONS_SKILL_DIR:-$HOME/.agents/skills/arabic-presentations}"

python3 "$ARABIC_SKILL/scripts/arabic_pptx.py" repair \
  "$TMP_DIR/deck.raw.pptx" \
  "$FINAL_PPTX" \
  --lang ar-SA \
  --convert-bullets
```

Add `--font "<Arabic-capable family>"` only when the user or deck specifies a font. This writes the complex-script font slot; it does not embed the font.

Add `--presentation-rtl` for an Arabic-first deck. Omit it for an English-primary or deliberately neutral bilingual deck; presentation reading order is a deck-level choice, separate from the mandatory RTL properties on Arabic paragraphs.

The repair command must preserve the raw draft, remove manual bidi controls, apply native paragraph/text-body direction, add language metadata, fill the complex-script font slot from the selected typeface when possible, and convert typed bullet glyphs to native bullets.

### 4. Run structural QA

Run the strict audit after every later edit or export:

```bash
python3 "$ARABIC_SKILL/scripts/arabic_pptx.py" audit "$FINAL_PPTX" --strict
```

For an Arabic-first deck, add `--expect-presentation-rtl` to the audit command.

Any error or strict warning is a delivery blocker. Reopen, repair, or regenerate the deck; do not explain away a failed audit.

The audit proves package structure and Arabic text metadata. It cannot prove visual order inside every application or whether a font is installed.

### 5. Run visual and application QA

Use the Presentations skill's render-and-inspect loop for layout, overflow, wrapping, contrast, and overlap. Do not use the Codex/LibreOffice renderer as the authority for Arabic character or word order; it may render valid PPTX bidi text incorrectly.

When invoking the Presentations skill's Python container tools in Codex Desktop, use the bundled Python returned by `load_workspace_dependencies`; the system Python may not include `pdf2image` and the other rendering dependencies.

When PowerPoint desktop is available, open the final normalized PPTX and inspect the mixed-text corpus in [references/qa.md](references/qa.md), plus every slide containing numbers, Latin acronyms, parentheses, percentages, URLs, or bullets. PowerPoint visual QA is required before claiming "PowerPoint verified."

Use Keynote and Google Slides only as secondary compatibility checks. If they differ from PowerPoint, preserve the structurally correct PPTX and report the application-specific difference. For Google Slides, expect unavailable local fonts to be substituted.

### 6. Deliver honestly

Report these separately:

- `Structural Arabic QA: PASS/FAIL`
- `Layout QA: PASS/FAIL`
- `PowerPoint visual QA: PASS/NOT RUN`
- `Keynote/Google Slides compatibility: PASS/NOT RUN/DIFFERS`
- `Font portability: installed-font dependent` or `PDF supplied`

Do not say "perfect everywhere" or "cross-app verified" unless those applications were actually opened and inspected.

## Special cases

- **Existing deck repair:** preserve the input and write a distinct normalized PPTX unless the user explicitly authorizes in-place replacement.
- **Arabic charts:** prefer numeric/Latin chart internals with Arabic titles and labels as separate RTL text boxes unless PowerPoint visual QA is available. Native chart bidi is not fully proven by the bundled audit.
- **Tables:** set RTL on cell paragraphs. Mirror column order only when the table's semantic reading order is Arabic; do not mirror decorative geometry automatically.
- **Speaker notes:** normalize Arabic notes too; the repair script scans DrawingML paragraphs throughout the PPTX package.
- **PDF:** use PDF for fixed distribution, not as a replacement for delivering the requested editable PPTX.
