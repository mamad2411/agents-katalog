---
name: resume-from-context
description: "Create a polished, debranded personal resume/CV as a PDF from existing context (an employer-branded CV, vault notes, a LinkedIn profile, or the conversation) using typst. Use when the user asks to build/make a resume or CV, turn an existing or consultancy-branded (e.g. Capgemini) CV into a personal one, create a beautiful shareable CV PDF with a photo, or 'lag en CV'."
---

# Resume from Context

Turn whatever source material exists (an existing CV PDF, vault person note, LinkedIn
profile, or the chat) into a beautiful, **personal**, shareable resume PDF. Output is
typst-based (no LaTeX needed). The bundled `assets/resume-template.typ` is the design;
fill it in and compile with `scripts/build-resume.sh`.

## Workflow

1. **Gather the source, preserving exact wording.** Read the existing resume (use the
   Read tool on the PDF), the person's vault note, and the conversation. Keep the
   subject's own phrasing for the summary and each role; you are reformatting, not
   rewriting.
2. **Confirm the decisions that actually change the output** (one at a time, recommend
   first; AskUserQuestion works well). Skip any the user already answered:
   - **Confidentiality / debranding** — always strip the source employer's branding,
     logo, footer, and "as a consultant from X" framing so it reads as the person's own
     CV. Then ask: keep real employer/client names (usually fine — public-sector or past
     employers), generalize them, or drop current-client work? Never include per-client
     secrets.
   - **Scope & wording fidelity** — comprehensive (keep all roles, her words) vs a tight
     1–2 page highlight reel. Don't force a page count; don't pad or gut content.
   - **Contact header** — which fields + values (name, title line, email, phone,
     LinkedIn, GitHub/portfolio, city). Pull from the source/vault before asking.
   - **Layout** — single-column + header band (default; paginates cleanly for long CVs)
     vs two-column sidebar (sharp on page 1, awkward across pages).
   - **Accent color** — e.g. deep navy `#1e3a5f` (default), petrol, monochrome, burgundy.
   - **Language** and any targeting line (e.g. "Open to relocation"). Default: match the
     source language, no targeting line (universally shareable).
3. **Author the typst** by copying `assets/resume-template.typ` and filling it in: header
   (photo top-right), Profile, Skills, Experience (one `entry(...)` per role, most recent
   first), Education, Certifications, Languages. Set `accent` at the top.
4. **Compile**: `bash scripts/build-resume.sh "<src>.typ" "<out>.pdf"`. It auto-handles the
   photo path (absolute path → `--root /`; relative path beside the `.typ` → no root).
5. **Review the actual PDF** with the Read tool, page by page. Check the photo renders,
   accents are right, nothing overflows, and all content survived. Fix and recompile.

## House rules

- **No em dashes** (—). Use commas, colons, parentheses, or `·`. Verify: `grep -c "—" <file>.typ`
  must be `0`. (En dashes `–` in date ranges are fine.)
- **Norwegian text**: keep correct æ/ø/å; never ASCII-fold.
- **Keep the subject's wording.** Merge the source's duplicated "Project" + "what she did"
  blocks into one tight paragraph per role, but in their voice.
- **Photo**: display via `image(..., height: 3.3cm)` inside a `box(clip: true, radius: 5pt)`
  for rounded corners, top-right of the header grid.

## Iterating later

For a regeneratable bundle (e.g. to store in an Obsidian vault `Attachments/` folder),
copy the photo next to the `.typ`, change the `#image(...)` path to **relative** (just the
filename), and keep `.typ` + `.pdf` + photo together. Then
`cd <folder> && typst compile "<name>.typ" "<name>.pdf"` regenerates it with no `--root`.

## Prerequisites

- `typst` (0.11+): `brew install typst`. Fonts resolve from the system (macOS has
  "Helvetica Neue"); override with `#set text(font: ...)` if missing.
