---
name: sustech-beamer-theme-fix
description: Fix for undefined \setsource/\setdomains/\setpresenter/\setvenue commands when compiling SUSTech Beamer slides from the standard template. Copy the extended beamerthemesustech.sty from the sustech-slides-template repository.
---

# SUSTech Beamer Theme \setsource Fix

## Problem

When filling `main.tex` from the standard `slides-template`, `latexmk -xelatex` fails with:
```
! Undefined control sequence.
l.23 \setsource{...}{...}
```
Also: `\setdomains`, `\setpresenter`, `\setvenue`. These are used by newer decks but NOT defined in the plain template version of `beamerthemesustech.sty`.

## Root cause

The base `beamerthemesustech.sty` is ~60 lines, ending with `\mode<all>`. The extended version (shipped in the sustech-slides-template repository) continues to ~100+ lines with:
- `\paperfrom{venue}{year}` — formats the source line
- `\setsource{venue}{year}` — calls `\paperfrom`
- `\setdomains{...}` — sets domain tags
- `\setpresenter{name}` — sets presenter name
- `\setvenue{location}` — sets venue location
- `\titlemetaline` — formats the title page bottom line

## Fix

The extended macros ship in the sustech-slides-template repository at `sustech-theme/beamerthemesustech.sty`. After copying the template into your deck, replace `beamerthemesustech.sty` with the extended version.

If you already have a checkout of the repository:

```bash
cp "<TEMPLATE_DIR>/sustech-theme/beamerthemesustech.sty" \
  "<TARGET>/slides-beamer/sustech-theme/beamerthemesustech.sty"
```

Otherwise clone it first, then copy:

```bash
git clone --depth 1 https://github.com/yhbcode000/sustech-slides-template.git <TEMPLATE_DIR>
cp "<TEMPLATE_DIR>/sustech-theme/beamerthemesustech.sty" \
  "<TARGET>/slides-beamer/sustech-theme/beamerthemesustech.sty"
```

Do this BEFORE first compile. The `beamerthemesustech-elements.sty` and `beamercolorthemesustech.sty` files are identical between the repository template and the reference deck — only `beamerthemesustech.sty` carries the extended macros; when in doubt, copy the whole `sustech-theme/` directory.
