---
name: repo-visual-assets
description: "Use when making repo art: logo, lockup, banner, workflow image, social preview, README screenshots."
version: 2.0.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, readme, logo, banner, diagram, image-generation, branding, open-source]
    related_skills: []
---

# Repo visual assets

The part of a public repo people SEE, not read: logo, banner, workflow image,
social preview. The agent owns the layout and placement conventions; the owner owns
the ideas and picks between drafts.

A workflow or architecture diagram is engineering: draw it from the code. A logo with
real brand character is design work: follow the logo process in section 5, never a
single prompt.

## 1. Isolate the work (parallel sessions)

Another session is often coding in the same repo. Never share its folder: a branch
switch rewrites the files under the other agent, and its `git add -A` sweeps up your drafts.

```
git -C <repo> worktree add ../<Repo>-art -b art     # SIBLING folder, not inside the repo
<Repo>-art/drafts/         tries and rejects, never committed
<Repo>-art/docs/assets/    finals only, committed on "art"
```

- Put the worktree NEXT to the repo, not under `.worktrees/` (the Hermes `/worktree new`
  and `hermes -w` default), unless the repo's .gitignore already ignores `.worktrees`:
  check with `git check-ignore -v .worktrees/x`. An unignored inner folder shows up as
  untracked files in the other session.
- Finals reach the official folder by `git merge art` (history, clean diff), never by
  copying files. Merge only after the other session has committed. Then
  `git worktree remove ../<Repo>-art` + `git branch -d art`.
- The official Hermes worktree doc: docs/user-guide/git-worktrees.

## 2. What to make, in this order

Read the repo README first so the art describes what the product actually does.

```
1 logo            README top, avatar, favicon      must
2 workflow image  under the tagline, replaces ASCII must
3 social preview  1280x640 link card, built from 1+2 must, cheap once 1+2 exist
4 terminal demo   real CLI run recorded (VHS/asciinema), NOT AI - last, needs stable code
5 app screenshots only if the owner asks: the real window, never a mockup
6 banner          only if the logo alone looks empty
```

- Default social preview = the hero banner, even once a GUI exists: the link card's
  job is to be remembered, and stylised hero art does that; the window belongs in
  README screenshots. Show a draft before committing any new social file.
- Workflow image: the product's SUBJECT at the centre and the workflow around it,
  learned once, then the daily loop. Stations come from the real commands, never
  invented steps. Settle the open specifics (subject, colours, station list) in ONE
  decision form before drawing.
- Assets in one repo are a FAMILY: every piece uses the same type and rendering
  recipe (fonts, sizes, grid, colours, glow). The REFERENCE is whichever piece the
  owner approved most recently, not necessarily the hero: when the new piece's look
  wins, re-render the older ones with the new piece's render code (copy the loop),
  not a re-tuned variant of the old recipe. "Close" twins get rejected: measure the
  visible differences (colour intensity, density) and report them before showing.
- Fine detail vs readability: when both matter, draw at 2x (e.g. a 2560x1280 canvas)
  and ship the 2x canvas as the ONLY file, not 1x + @2x duplicates. For the banner,
  which is also the social preview (GitHub limit: under 1 MB, 1280x640 or larger),
  save the 2x as a 256-colour PNG without dither (typically ~600 KB, no visible
  error). Offer a variant as a draft next to the hero, never replace the hero unasked.
- Diagram labels: plain English in the house reading font, sentence case, bright
  enough to read over any glow, numbered 1-N in plain digits. No decorative kickers,
  no Roman numerals, no italic grey captions: they read as unclear.
- A README image is a PRESENTATION for people who have never run the tool: no
  command names, flags, folder names or key bindings in any label, title or footer
  (`--apply`, `_review/`, `--json`, `<tool> run`). Translate each one into the
  user's action ("You say go", "Not sure? It asks"); the exact command belongs in
  the README text. Steps still come from the real commands, only the words change.
- Plain words must stay TRUE. Check every label against the code's actual
  behaviour before showing: never imply files move before the user's go-ahead, never
  claim a case goes to the user that the code leaves in place, never claim undo does
  more than it does. Honesty is the point of the diagram.
- After rewording, grep the WHOLE art src folder (shared helpers too, e.g. a
  `footer()` with default text) for the old technical strings, then read the
  rendered image with vision: a shared helper's default text ignores the list you
  edited in the main script.
- Taglines and captions must cover what the product actually handles: grep the
  code for supported inputs (e.g. a `*_EXTS` list) before writing "photos" - a tool
  that also handles videos must say "photos and videos", in the image and the
  README's first line together.
- Before asking the owner to choose between two images, say where each one appears
  (README top vs link card when shared vs README body). Placement is what gets judged.
- Promoting an approved draft: move its generator into `docs/assets/src/` with
  repo-relative inputs, re-run it, and prove the output is pixel-identical to the
  approved draft (`ImageChops.difference(...).getbbox() is None`) before commit.
  Give every generator an optional output-path argument so drafts render into
  `_private/art/<topic>/` with the exact committed code.
- When a new generator replaces an old one, delete the old script and its unused
  inputs, and prune the shared helper module to what the remaining generators
  reach (walk the `C.name` uses through the helpers with `ast`), keeping a backup in
  scratch. Then re-run every generator and re-prove pixel identity: dead helpers
  carrying old labels are what leaks technical text back into images.
- A new draft that would replace a committed asset goes in `_private/art/<topic>/`
  (numbered, with the owner's sketch saved as `00-`) and is shown first; the README
  keeps the old image until the owner says go.
- App screenshots: scripted from the running app over CDP, on a public/synthetic
  world, no username or local path in frame. Procedure and pitfalls:
  `references/app-screenshots.md`.
- One idea, two forms: HERO art (detailed, banner/social preview) and a LOGO MARK
  (simple, must read at 32 px). A detailed illustration is not a logo; say so early.
- Products that show people: never real people's photos, not even the owner's. Use
  fictional, statue or icon-style figures. The repo's own generated hero art is the
  best source: it is already public and licence-clean, and it keeps screenshots
  on-brand. Use invented names and say in the README that nobody real is shown.

## 3. Stress-test the art concept (before generating)

Same duty as for code ideas: verdict in a few lines, then build what the owner wants.

- **Cliche**: does the obvious rendering land in a dated trope (e.g. statue + glitch =
  vaporwave)? Name the trope and the fix (medium, palette, restraint).
- **Too close to the inspiration**: borrowing a mood is fine; copying another brand's
  look makes the project read as its side project. Pick a distinct medium/accent colour.
- **Message clash**: does the imagery contradict the product (scanning reticles vs a
  privacy tool)? Turn it: calm, precise, anonymous rather than threatening.
- Offer the naming hook when there is one (a Latin name -> a carved-capitals
  wordmark), for the wordmark only: never as decoration in labels or captions.

## 4. Layout and placement (GitHub conventions)

```
README top:  centred LOCKUP (light/dark via <picture>) -> one-line pitch -> short paragraph
then:        sections; workflow image ("how it works") is the ONLY other image
files:       docs/assets/{logo.svg, logo-dark.svg, logo-lockup.svg, logo-lockup-dark.svg,
             banner.png (social preview only), workflow.png}
```

- A clean README top: the lockup, then text. No `# Name` heading above it (the
  lockup says the name), no ASCII diagram, no banner. banner.png lives in
  docs/assets only as the social preview. Record the owner's own layout rule in the
  design system if it differs.
- A bare mark (e.g. 96 px logo.svg) looks too thin at the top: use a horizontal
  LOCKUP - mark left, name beside it, tagline under the name in small spaced
  capitals. Recipe: `references/lockup.md`.
- Keep README images to what the owner asked for (by default the workflow image).
  When an image leaves the README, grep the repo for its path; if nothing uses it,
  `git rm` it and its source inputs (no orphans). Inputs a private script still
  needs move to `_private/`, and that script's path is updated.
- Propose 2-3 tagline options of 2-4 words, each true to the code, with a
  recommendation and its reason (what it says vs what it leaves out).
- Follow the design system's name casing (e.g. "<Name>", never caps); if the owner
  writes it differently, point out the conflict and ask, and change the rule in the
  design system too if the owner overrides it.
- Show the README top before committing: GitHub cannot render a private or
  unpushed repo, so fill a small HTML page with GitHub's light (#fff/#1f2328) and
  dark (#0d1117/#e6edf3) panes, the real logo files and the README's first
  paragraphs, screenshot it with headless Chrome
  (`chrome --headless=new --hide-scrollbars --user-data-dir=<scratch>/prof
  --window-size=1520,560 --screenshot=<scratch>/top.png file:///<scratch>/top.html`),
  check it with vision, give the owner the PNG path and say it is a GitHub-styled
  local render, not GitHub itself. Whole-README render (markdown -> HTML -> tall
  screenshot): the coder role's `local-web-ui` skill, references/readme-for-window.md.
- Check the `<img>` alt text whenever labels change: it must use the same plain
  words as the image, never the old technical names.
- Center with `<p align="center"><img src="docs/assets/x.png" width="..." alt="..."></p>`.
- Dark/light: logo must read on white AND black, or ship two files and switch with
  `<picture><source media="(prefers-color-scheme: dark)" srcset=...>`.
- Social preview is uploaded by hand in repo Settings (not a file GitHub reads),
  under 1 MB, 1280x640 or larger. GitHub hides that setting on private repos: the
  owner uploads it once the repo is public, so record it as the owner's step in
  docs/assets/README.md, not an agent step.
- Detailed code-rendered art ships as ONE 2x file per image (can exceed 1 MB for
  the workflow; fine in a README); simple images stay under ~500 KB. Alt text on
  every image, in the same plain words as the labels.
- Diagrams: prefer SVG (sharp, text editable, no generator licence question).

## 5. Generate drafts

Order: a local model or cheap drafts for exploration, then the final from a source
whose terms give the owner the output (a vector redraw, or a model whose terms
assign output ownership). Read the generator's licence at the source every time
(model card + LICENSE file, not a catalogue page). A research-only or
non-commercial licence does not cover a project logo. A cloud image model is paid
per call and the prompt leaves the machine: check the vendor's current terms for
output ownership before using an output as a final asset.

- Ask the owner for the idea AND reference images BEFORE the first generation; test a
  model on the owner's real prompt, never a generic one. Rounds made from words alone
  tend to be rejected wholesale; references set the direction at once.
- A sketch with a photo in it: give an image model the photo (cropped, upscaled) as
  reference 1 (subject, pose) and the project's house art as reference 2 (material,
  light only), and tell the prompt what to take from and what to ignore in each.
- Compare side by side: same prompt through each candidate, the owner picks.
- Write drafts to `<Repo>-art/drafts/`, never into another project's output folder.
  Keep them out of git via `$(git rev-parse --git-common-dir)/info/exclude` (private to
  the machine) rather than .gitignore, which is tracked and touches the other session.
- Save the prompt next to each PNG (`NAME.prompt.txt`) so a liked draft can be
  reproduced or edited later.
- Each paid generation is a real cost: a few drafts, not dozens.
- A round = up to 3 distinct directions (medium/palette/form), numbered `NNX-name`,
  only while there is no reference. Once the owner picks a draft, switch to single
  edits of that draft (one change per round). Report each as: what works, what is
  weak, then one question with a recommended option.
- Use image gen for HERO art only. Small flat logo marks come out generic (a stock
  "user" icon), ignore colour instructions and get hazy alpha - draw the mark as SVG,
  derived from the chosen hero. This is also the licence-clean route.
- **A logo needs a disciplined process, not a prompt:** brief, concepts, SVG craft,
  then its own tests (16 px, one-colour, reversed, squint, mirror, contrast, next to
  similar products' marks) before showing anything. An AI raster is at most a concept
  sketch feeding that process.
- Hand over the finals with a style rule (colours, which asset where) written into
  the project's own docs/AGENTS.md, so later sessions follow it without asking.

## 6. Verify before showing

- Look at every image with vision_analyze. Reject misspelled wordmarks, wrong
  arrows, invented labels - image models still garble text.
- Transparent drafts: generated alpha is soft (many semi-transparent pixels, a faint
  cloudy fill a white preview hides). Measure and look on dark before judging:

  ```python
  from PIL import Image
  im = Image.open(p); h = im.getchannel("A").histogram(); n = im.width * im.height
  print("transparent %.1f%% opaque %.1f%% partial %.1f%%" % (h[0]/n*100, h[255]/n*100, (n-h[0]-h[255])/n*100))
  bg = Image.new("RGBA", im.size, (40, 40, 40, 255)); bg.alpha_composite(im); bg.convert("RGB").save(p_dark)
  ```

  Also composite on white and downscale to 256/32 px to judge logo readability;
  delete those `_preview` files after looking. A final logo needs cleanup or an
  SVG redraw.
- Before commit: strip metadata (PNG text chunks, SVG `<metadata>`, editor ids) and
  check for real names, local paths and other identities (the project's identity
  rules).

## Pitfalls

- **Ask where a reference image came from before building on its pixels, and never
  publish someone else's artwork even modified.** Regenerate an original in its style
  for the final. Third-party pixels in an MIT repo are a publication blocker.
- **Never touch another agent's project to make it serve yours.** A local generator
  owned by another agent (scripts, bin, config) is read-only unless the owner OKs a
  change: report bugs and upgrade opportunities, ask first. When approved, record the
  change in that project's PLAN.md. Call its binary directly with your own output
  path instead of editing its scripts.
- **Switching the image_gen provider changes every future call in the profile.**
  Prefer a direct CLI call for tests; if the config must change, note the
  one-line rollback.
- **Photo-enhance pipelines ruin flat art.** Detail passes with photographic prompt
  words add texture noise to logos and diagrams; use a plain upscaler (ESRGAN) only.
