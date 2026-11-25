---
name: apca-contrast
description: Calculate APCA Lc contrast scores (APCA-W3 v0.1.9) and look up exact pass/fail per font size and weight using the official fontLookupAPCA table. Audits Tailwind v4 globals.css automatically (extracts :root and .dark blocks side-by-side), supports every CSS color notation (hex, rgb/rgba, hsl/hsla, oklch, oklab, color() with display-p3 / rec2020 / srgb / srgb-linear, and 148 named colors incl. rebeccapurple), handles alpha compositing, and offers Reverse APCA (find a color that hits target Lc on a given background). Use this skill whenever the user asks to measure, audit, or check contrast — design system tokens, light/dark mode color audits, accessibility reviews, shadcn/Tailwind oklch tokens, "is this readable?" questions. Trigger even when the user only says "contrast", "Lc", "readability", "a11y review", "대비", "가독성", or pastes color values without explicitly naming APCA — APCA is the modern WCAG 2.x successor used in WCAG 3 draft and gives more accurate perceptual results.
---

# APCA Contrast Calculator

APCA-W3 v0.1.9 with the **official fontLookupAPCA matrix** for precise pass/fail per font size and weight. Algorithm constants frozen at `0.0.98G-4g` (Feb 2021), library version 0.1.9 (Jul 2022) — both verified current as of 2026.

The bundled Python script is deterministic and dependency-free. Use it instead of regenerating math at runtime.

## When to use

- Auditing design system color tokens — usually one shot via `--from-tailwind`
- Comparing light vs dark mode contrast for the same semantic role
- Validating shadcn/Tailwind oklch tokens directly (no manual hex conversion)
- Checking whether a token works at a specific font size + weight (e.g. "does muted-foreground pass for 14px medium?")
- Reverse-engineering a color: "what shade do I need for Lc 75 on white?"
- Any "is this readable / does this pass" question

If the user asks about WCAG 2.x ratio, mention APCA is the modern successor (WCAG 3 draft) and offer Lc instead.

## Color formats supported

| Format        | Examples                                              |
| ------------- | ----------------------------------------------------- |
| Hex           | `#fff`, `#ffffff`, `#fff8`, `#ffffff80`               |
| rgb / rgba    | `rgb(255 255 255)`, `rgba(0,0,0,0.5)`, `rgb(100% 0 0)`|
| hsl / hsla    | `hsl(0 0% 50%)`, `hsla(120, 100%, 25%, 0.5)`          |
| oklch         | `oklch(0.205 0 0)`, `oklch(50% 0.1 200deg)`           |
| oklab         | `oklab(0.5 0.05 -0.1)`                                |
| color() sRGB  | `color(srgb 1 0 0)`, `color(srgb-linear 0.5 0.5 0.5)` |
| color() P3    | `color(display-p3 1 0 0)` (auto-clamps to sRGB gamut) |
| color() 2020  | `color(rec2020 1 0 0)` (auto-clamps to sRGB gamut)    |
| Named         | `red`, `white`, `rebeccapurple`, `transparent`, ...   |

Wide-gamut inputs (Display-P3, Rec.2020) are converted via D65 matrices and clamped to sRGB — any out-of-gamut clipping is silent. APCA itself targets sRGB displays, so this is the correct behavior, but mention it in reports if the user is working in a P3-aware pipeline.

## Running the script

Path: `~/.claude/skills/apca-contrast/scripts/apca.py` (Python stdlib only).

### 1. Single pair

```bash
python3 ~/.claude/skills/apca-contrast/scripts/apca.py "<fg>" "<bg>"
```

Output includes the signed Lc, polarity (BoW/WoB), the verdict, and **minimum font size per weight** (400/500/600/700) from the official fontLookupAPCA table. Add `--matrix` for the full size×weight pass/fail grid.

### 2. Tailwind v4 audit (preferred for this project)

```bash
python3 ~/.claude/skills/apca-contrast/scripts/apca.py \
  --from-tailwind <path-to-globals.css>
```

Auto-extracts `:root` (light) and `.dark` blocks, pairs each common foreground token (`foreground`, `muted-foreground`, `primary`, `secondary-foreground`, `accent-foreground`, `destructive`, `card-foreground`, `popover-foreground`, `border`) against `--background`, and emits a side-by-side light/dark report. Use `--bg-token <name>` to audit against a different background (e.g. `--bg-token card` to check on-card contrast).

### 3. Batch mode

```bash
python3 ~/.claude/skills/apca-contrast/scripts/apca.py --batch pairs.json
```

Two batch shapes:

```json
[
  {"name": "foreground on bg",  "fg": "#0a0a0a",          "bg": "#ffffff"},
  {"name": "primary on card",   "fg": "oklch(0.205 0 0)", "bg": "oklch(0.985 0 0)"}
]
```

```json
{
  "background": "#ffffff",
  "tokens": {
    "foreground":       "#0a0a0a",
    "muted-foreground": "rgb(115, 115, 115)"
  }
}
```

### 4. Reverse APCA — find a passing color

```bash
python3 ~/.claude/skills/apca-contrast/scripts/apca.py --reverse <bg> <target_lc>
```

Returns the closest neutral grey foreground that hits the target |Lc|. Useful for: "what shade do I need for body text on this card?"

### 5. JSON output

Add `--json` to any command for structured output (use when feeding into a report).

## Interpreting Lc — the official ladder

The script attaches a verdict using the **fontLookupAPCA Ascend matrix** (apca-w3 0.1.9), keyed at weight 400. Always also report the per-weight breakdown — heavier weights pass at smaller sizes.

| Lc (abs) | Practical meaning at 400wt                              |
| -------- | ------------------------------------------------------- |
| ≥ 90     | Body text any size (≥14–16px @ 400)                     |
| 75 – 89  | Body text comfortable (≥16–17px @ 400)                  |
| 60 – 74  | Body minimum (≥18–24px @ 400)                           |
| 45 – 59  | Large text only (≥28–42px @ 400) — headlines            |
| 30 – 44  | Non-text UI / very large headlines only                 |
| 15 – 29  | Decorative / disabled UI — fails for text               |
| < 15     | Insufficient                                            |

For typical body copy targets: **Lc ≥ 75 is comfortable, Lc ≥ 60 is the practical floor at 16px+**. The script gives you the exact px threshold so you don't have to eyeball this ladder.

## Reporting back

After running the script:

1. Lead with the headline finding (which tokens fail, which are borderline).
2. Show a clean markdown table — extract Name, Lc, and Verdict columns; don't dump raw script output.
3. For light/dark audits, **flag asymmetries** explicitly. A token that's Lc 90+ in one mode and Lc 30–50 in the other is the most common design-system bug.
4. If the user pasted alpha colors or wide-gamut colors, mention the relevant caveat (alpha compositing is unofficial; wide-gamut clamps to sRGB).

## Limitations to flag honestly

These caveats matter — don't let the user walk away thinking an APCA-pass is the same as "fully accessible / legally safe / works for everyone."

### What APCA itself cannot tell you (mention these proactively)

- **APCA does NOT replace WCAG 2.x for legal compliance.** ADA, EN 301 549, KWCAG, Section 508 — every legal regime still mandates WCAG 2.x AA. APCA is a WCAG 3 *draft*, not law. **If the user mentions "audit," "compliance," "WCAG," "ADA," "법적," "공공기관," "장애인차별금지법," or anything similar, explicitly tell them this skill does NOT cover legal compliance** and recommend they run a WCAG 2.x ratio checker alongside (browser DevTools accessibility panel, axe DevTools, WAVE).
- **Single perceptual model.** APCA assumes one "average user." Color blindness, low vision, age-related changes aren't differentiated. For projects with known low-vision audiences, recommend additional vision-simulation tools.
- **Contrast ≠ readability.** Lc is necessary but not sufficient. Cramped line-height, tight tracking, and bad fonts can make Lc-90 text hard to read. If the user is reviewing real UI screens, mention typography is also a factor.
- **Lc 0–30 zone is noisy.** When findings land in this range, say "this fails" — don't quote the exact Lc as if it were precise to one decimal.
- **Font family and rendering are ignored.** The minimum px values from `fontMatrixAscend` are a starting point, not the final word. Pretendard 14px ≠ Times New Roman 14px in actual readability.
- **Algorithm frozen since Feb 2021.** New display tech (HDR, OLED light bleed, P3) isn't reflected. If the user's audience is on modern devices, mention real on-screen contrast may differ slightly from APCA's prediction.

### This implementation's specific limits

- **Alpha compositing is not part of the APCA spec.** The script pre-composites in sRGB (pragmatic default) and adds a warning. For arbitrary content behind translucent overlays (hero images with text), the approximation can be wrong by 5–10 Lc.
- **`fontLookupAPCA` Ascend variant only.** Body text. Other variants (headlines, non-text UI) aren't bundled.
- **Rounding:** lookup keys round abs(Lc) down to the nearest 5. Lc 73 and Lc 70 hit the same row. Surface this when results are right on a boundary.
- **No CSS variable resolution.** If a token's value is `var(--other)`, the user must resolve it or run the extractor against built CSS, not source.
- **Wide-gamut inputs clamp to sRGB.** `color(display-p3 ...)` is approximated, not true P3-display contrast.

## Common findings to watch for

- `destructive` and `primary` tokens often fail in dark mode while passing in light mode — the brand color was tuned on a light page and doesn't have enough luminance contrast against a dark background. Flag it; a separate `destructive-dark` / `primary-dark` shade is usually the fix.
- `muted-foreground` typically lands in the **Lc 50–70** range. Fine for 16px+ body, fails for 12–14px caption text. Recommend "use only for ≥16px" or darken.
- `border` tokens score **Lc 5–20**. Acceptable for non-text UI per APCA, but flag if the same color is reused for placeholder text.
- A token that scores below Lc 30 in either mode and is used for any text role is a hard failure — call this out explicitly.
