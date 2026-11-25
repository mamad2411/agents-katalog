---
name: explain
description: Explain any file in the suite in plain language, teaching the pattern behind the code. Use when the user runs /explain or asks what a file does or why it is structured a certain way.
---

# /explain — Explain a File in Plain Language

**Type:** Learning
**Description:** Explains any generated file in plain language, teaching the pattern behind the code rather than just describing the output. Built primarily for Persona 1 (manual QA learning automation).

---

## Input Format

- A file path (Page Object, spec, fixture, factory, config, or k6 script), or
- A pasted snippet the user wants explained

## Output Format

A plain-language walkthrough:
1. **What this file is** — its role in the suite
2. **Why it's structured this way** — the Autoframe convention behind it
3. **Line-by-line / block-by-block** — what each part does, no jargon
4. **The pattern to remember** — the reusable lesson
5. **Try it yourself** — a small suggested exercise

## Step-by-Step Instructions

1. Default to Persona 1 tone: warm, encouraging, jargon-free; define every term the first time it appears.
2. Read the target file fully.
3. Identify which Autoframe convention it follows (POM, spec, fixture, factory, k6) and reference CLAUDE.md.
4. Walk through it block by block, always pairing *what* with *why*.
5. Surface the transferable pattern so the user can apply it to the next file.
6. End with a small, concrete exercise (e.g. "add an `expectErrorVisible()` assertion method").
7. Offer to explain a related file next.

## Rules

- Teach the pattern, not just the syntax.
- No unexplained jargon.
- Never modify the file — this skill only explains.
