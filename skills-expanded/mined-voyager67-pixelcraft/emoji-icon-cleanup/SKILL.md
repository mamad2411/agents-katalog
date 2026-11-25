---
name: emoji-icon-cleanup
description: "Identifies emoji-as-icon, mixed icon families, inconsistent sizes, and decorative glyphs; replaces them with a consistent semantic icon system."
license: CC-BY-NC-4.0
---

# Emoji Icon Cleanup

## Workflow

1. Inventory every emoji, unicode symbol, icon package, SVG, and icon font used as UI chrome.
2. Distinguish expressive content emoji from functional icons; do not remove legitimate user content.
3. Choose the existing icon family if coherent; otherwise recommend one library already compatible with the project.
4. Map each icon to a semantic action or state; delete icons that have no meaning.
5. Normalize size, stroke, alignment box, label gap, and color inheritance.
6. Check accessible names, decorative hiding, and touch-target size.

## Output

Icon inventory, replacement mapping, removed decoration, and consistency checks.

## Non-negotiable rules

- Judge the interface that exists, not assumptions about who or what produced it. AI authorship cannot be reliably inferred from generic visual patterns alone.
- Treat “AI slop” as a shorthand for observable quality problems: generic patterns, weak hierarchy, arbitrary decoration, vague copy, fabricated-looking content, inconsistent systems, or incomplete states.
- A pattern is a signal, not proof. Record evidence, confidence, and plausible benign explanations. Do not label a screen “AI-generated” as a factual finding.
- Preserve user goals, factual content, product behavior, existing brand assets, and working accessibility unless the evidence supports a change.
- Never invent metrics, reviews, customer logos, endorsements, product claims, features, integrations, or data to make a screen look more convincing.
- Inspect rendered output when tools allow it. If you only inspect source code or a screenshot, state that limitation.
- Make the smallest effective change first. Do not replace an existing coherent visual language just to make the result look different.
- Never expose secrets or private information found in a repository. If a secret is detected, do not repeat its value; report only the file and line, stop short of publishing it, and recommend revocation/rotation.

## Completion report

State the signals found, evidence and confidence, fixes made, files changed, checks actually run, and unresolved issues. Distinguish visual review, code review, and runtime testing.
