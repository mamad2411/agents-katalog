---
name: ctf-writeup-screenshots
description: Capture and organize natural-looking screenshots for CTF re-solve write-ups,
  matching a human solver's workflow rather than generated diagrams. Use when preparing
  CTF write-ups that need step-by-step screenshots, terminal/browser evidence, or
  when the user asks for screenshots like another write-up.
version: 1.0.0
metadata:
  hermes_origin: import
license: MIT
tags:
- ctf
- writeup
- screenshots
- macos
- evidence
related_skills:
- ctf-writeup-discipline
---

# Natural CTF Write-up Screenshots

Use this skill when producing a CTF write-up that must include screenshots of the solve process. The goal is authentic, human-looking evidence: screenshots should be captured from real terminal/browser/editor windows during the actual re-solve, not recreated as diagrams or synthetic mockups.

## Core rules

1. Re-solve first, capture during the solve.
   - Do not only take final-result screenshots.
   - Capture intermediate evidence: file inspection, program behavior, debugging, exploit trials, successful flag extraction.

2. Screenshots must look natural.
   - Use real terminal/browser/app screenshots.
   - Do not use generated images, diagram renderings, fake terminal text, or composited UI unless explicitly labeled.
   - Prefer normal window chrome, realistic prompt history, and actual command outputs.

3. Cover the full narrative.
   - Each major write-up section should have at least one screenshot when possible.
   - Screenshots should correspond to commands or observations mentioned in the text.
   - Avoid huge unrelated screen areas; crop only enough to keep the evidence readable while preserving natural UI context.

4. Preserve raw evidence.
   - Keep original screenshots in an `assets/screenshots/` or similar folder.
   - Use ordered filenames such as `01-unzip-files.png`, `02-checksec.png`, `03-crash-repro.png`, `04-debug-root-cause.png`, `05-exploit-flag.png`.
   - Do not overwrite raw screenshots after editing/cropping; write cropped copies separately if needed.

## Recommended workflow

1. Create a workspace layout:

```text
writeup/
├── writeup.md
└── assets/
    └── screenshots/
        ├── raw/
        └── selected/
```

2. Start a real solve transcript:
   - Use a visible terminal with the challenge directory open.
   - Run commands naturally: unzip, list files, inspect binary/source, execute program, debug, test payloads.
   - Keep terminal width readable, usually 100-140 columns.

3. Capture screenshots at these points:
   - Challenge files extracted and identified.
   - Important static analysis result: `file`, `strings`, `checksec`, source snippets, decompiler/debugger view.
   - Vulnerability discovery: crash, sanitizer/error output, debugger register/stack view, suspicious code path.
   - Exploit construction: payload script, local proof, remote command if applicable.
   - Flag acquisition: final successful output with the flag visible, if challenge rules allow.

4. Use macOS screenshot capture naturally:
   - `Cmd+Shift+5` for screenshot UI when doing manual-style capture.
   - Window or selected-region screenshots are preferred over full desktop unless the write-up being matched uses full desktop screenshots.
   - If using tools, use actual app screenshots from `computer_use`/desktop capture, not diagram generation.

5. Name and index screenshots immediately after capture.
   - Keep screenshot order aligned with the write-up narrative.
   - Use descriptive filenames; never leave only `截圖 2026-...png` in the final artifact.

6. Write the Markdown with image references near the matching explanation:

```md
![確認題目檔案與保護機制](assets/screenshots/selected/02-checksec.png)
```

## Screenshot selection checklist

Before finalizing, verify:

- [ ] The write-up can be followed from screenshots alone at a high level.
- [ ] Every screenshot is from the real solve environment.
- [ ] The final flag/result screenshot exists.
- [ ] Screenshots are readable at normal Markdown/PDF viewing size.
- [ ] Filenames are ordered and descriptive.
- [ ] No secrets, unrelated private windows, or personal information are visible.
- [ ] If a screenshot contains a flag, publishing it is acceptable for the intended write-up.

## Matching another write-up's screenshot style

When the user provides an example write-up image or PDF:

1. Inspect the example for style features:
   - Terminal theme/light-dark mode.
   - Full screen vs selected window vs cropped region.
   - How much surrounding UI is visible.
   - Whether screenshots are mostly terminal, browser, debugger, or editor.
   - Image density: screenshot after every command vs only major milestones.

2. Emulate the style, not the pixels.
   - Keep natural UI context similar.
   - Match screenshot frequency and framing.
   - Do not copy or fabricate exact outputs.

3. If the example uses many screenshots, err on the side of capturing more during the solve, then select the best ones later.

## Common pitfalls

- Do not create polished diagrams when the user asked for natural screenshots.
- Do not take screenshots after cleaning up terminal history if that makes the process look artificial.
- Do not rely on only text logs; the user explicitly wants visual solve evidence.
- Do not include unrelated apps/tabs in screenshots.
- Do not crop out the command that produced an output; the command is often the evidence.

## Final delivery expectations

A completed CTF screenshot-backed write-up should include:

1. `writeup.md` with embedded images.
2. An `assets/screenshots/selected/` directory referenced by the Markdown.
3. Optional `assets/screenshots/raw/` with original uncropped captures.
4. A short note listing any screenshots omitted or any solve step that could not be visually captured.
