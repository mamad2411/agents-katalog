---
name: visual-verify
description: Visual verification of Flutter output against Figma reference screenshots using Claude Vision
triggers:
  - verify visual
  - compare screenshots
  - figma diff
  - visual comparison
  - golden test failure
---

# Visual Verification Skill

Compare Figma reference screenshots with Flutter golden test outputs to ensure pixel-level design fidelity.

## When to Use

- After running golden tests and encountering failures
- When you want to verify that generated Flutter code matches the Figma design
- To analyze specific visual differences between design and implementation
- During code review to validate design accuracy

## Workflow

### 1. Identify the widget to verify

Find the corresponding files:
- Figma reference: `test/goldens/figma_ref/{widget_name}_figma_ref.png`
- Flutter golden: `test/goldens/ci/{widget_name}.png` or run golden tests to generate
- IR JSON: `output/ir/{widget_name}.ir.json` or `test/fixtures/{widget_name}.ir.json`

### 2. Run verification

```bash
# Basic comparison
node dist/verify-visual.js test/goldens/figma_ref/card_figma_ref.png test/goldens/ci/card.png

# With IR context for better analysis
node dist/verify-visual.js ref.png golden.png --ir design.ir.json

# JSON output for CI integration
node dist/verify-visual.js ref.png golden.png --json
```

### 3. Analyze results

The verification produces:
- **Fidelity score** (1-10): 8+ is passing
- **Categorized differences**: color, spacing, font, layout, border-radius
- **Severity levels**: low (cosmetic), medium (noticeable), high (breaking)
- **Fix suggestions**: Specific guidance on what to change

### 4. Fix differences

Common fixes by category:
- **Color**: Check token mappings in `figma2flutter.config.json` and `src/compiler/emitters/container-emitter.ts`
- **Spacing**: Check padding/margin emission in `src/compiler/emitters/flex-emitter.ts`
- **Font**: Check typography token resolution in `src/compiler/emitters/text-emitter.ts`
- **Layout**: Check layout mode handling in `src/compiler/flutter-compiler.ts`
- **Border radius**: Check border radius emission in container/image emitters

## Environment Setup

Requires `ANTHROPIC_API_KEY` environment variable.

```bash
export ANTHROPIC_API_KEY=your-key-here
```
