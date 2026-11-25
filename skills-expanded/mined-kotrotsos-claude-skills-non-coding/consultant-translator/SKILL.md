---
name: consultant-translator
description: Use this skill when reading a consulting deliverable (Deloitte, McKinsey, Bain, Accenture, BCG, EY, KPMG, PwC, or in-house consulting) and needing to extract the actual recommendation under the framework layer. Triggers on phrases like "translate this consultant deck", "what is this deck actually saying", "summarize this McKinsey report", or when the user shares a consulting document. Produces a one-page operator-friendly translation with assumptions flagged.
---

# Consultant-Speak Translator

## When to use this skill

A consulting deliverable lands in the user's inbox. It has frameworks, color-coded matrices, and confidence-inspiring language. The user needs to know in plain English: what are they actually recommending, what is recycled from prior engagements, and what assumptions have not been stated.

## Input the user provides

- The consulting document (deck, report, memo, slides, PDF)
- Optionally: the engagement context (what problem the firm was hired to solve, what stage the engagement is at)
- Optionally: the user's reaction to the document so far

## What this skill does

1. Reads the entire document and identifies the actual recommendation under the framework layer
2. Flags generic language that maps to nothing specific
3. Identifies assumptions the document treats as obvious but are actually contestable
4. Distinguishes engagement-specific analysis from boilerplate the firm uses across clients
5. Produces a one-page translation in the structure below.

## Output structure

```
# Translation: [Document title]
*Source: [firm name]. Page count: [n]. Read time saved: ~[estimate].*

## What they are actually recommending
2-3 sentences in plain language. Strip the frameworks, name the action.

## Their case (in 4 bullets)
- The evidence point that does the most work
- The assumption that holds it up
- The benchmark or comparison they lean on
- The risk they acknowledge

## What they are not saying
- Assumption [X] is treated as obvious. It is not.
- They use [framework term] to mean [specific thing]. The framework adds no insight beyond [thing].
- The cost projection assumes [Y], which may or may not hold for this organization.

## Recycled vs. specific
- Recycled: [specific phrases, slides, or claims that appear in their public materials or prior engagements]
- Specific to you: [the parts that demonstrate real engagement with your situation]

## Questions to push back on
- 2-4 sharp questions the user should ask before the next meeting with the firm.

## Honest read
2 sentences. Is this advice worth following, partially following, or pushing back on? Why?
```

## Calibration notes

- The "What they are not saying" section is the highest-value part. Most consulting documents are not wrong, they are incomplete in specific ways that the framework hides.
- Be specific about which assumptions are contestable. "Assumes 8% organic growth" is useful. "Has questionable assumptions" is not.
- Do not dismiss the work wholesale. Good consulting work exists. The job here is to extract the real recommendation from the packaging, not to undermine the engagement.
- If the document is genuinely strong, say so. Calibration is honest assessment, not contrarianism.

## Consulting clichés to watch for

These phrases tend to wrap one specific underlying claim, or nothing at all. When you encounter them, identify which:

- "Strategic enabler" / "key enabler"
- "Value chain transformation"
- "Next-generation operating model"
- "Holistic approach"
- "End-to-end solution"
- "Lever" (used as noun for "thing we could change")
- "Capability uplift"
- "Future-state architecture"
- "North star metric" (only meaningful if a specific one is named)
- "Center of excellence"

When you see these, dig for the actual claim. If there is no specific claim underneath, flag it.

## When NOT to use this skill

- Documents that are already written for operators (internal memos, peer-to-peer briefings)
- Academic papers (different filter)
- Vendor pitches (use a different evaluation lens)
