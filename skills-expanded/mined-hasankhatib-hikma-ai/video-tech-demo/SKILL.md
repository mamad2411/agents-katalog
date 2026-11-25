---
name: video-tech-demo
description: "Makes short, silent, loopable tech demo videos and GIFs for a CLI or developer tool, with real terminal output and the project's own brand, built with Hyperframes. Use when the user asks for a demo video, product video, GIF, launch clip, or a post for X about Hikma or another CLI."
---

# Tech demo videos

For a game-style animated scene on a web page, use `video-pixel-scene` instead.

A short silent clip that shows a CLI doing something a person recognizes from their own work. The terminal output is real, the look is the brand's, and the clip works muted and on a loop.

## Rules

- Do not render until the user says go. Propose the scenarios and length first. "Don't do a video yet" means research and copy only.
- Build in the scratchpad, not in the repo. Add files to the repo only when the user names a place.
- Never invent CLI output silently. Run the real command, and list what was approximated when you report back.
- Do not run commands that write outside a temp directory or to GitHub. Take the push confirmation text from `docs/site/commands/` instead of pushing.
- Do not install Hyperframes skills or plugins globally. Use `npx hyperframes` and author from `npx hyperframes docs <topic>`.
- Keep brand elements the user removed removed. Ask before adding any back.
- No org-specific names, private registry URLs, or credentials in a video. Use `myghaccount/myrepo` for the registry.

## Workflow

1. **Brief.** Get the audience, the one feeling to hit, and the length. Default to a loop of 15 to 20 seconds with no voice-over.
2. **Scenarios.** Pick three to six moments a person recognizes, each phrased in the user's voice ("New laptop? Same skills."). Prefer personal first-person beats over feature lists. See `references/lessons.md`.
3. **Capture real output.** Build the binary into the scratchpad, then run each command in a temp directory with `HOME`, `XDG_CONFIG_HOME` set to temp paths, `NO_COLOR=1`, and local git fixtures as sources. Copy the real strings. Commands that need `gh` or the network come from the docs.
4. **Brand.** Sample the logo's background and gradient with `ffmpeg` (one pixel to rawvideo) and read colors from code such as `internal/ui/brand.go`. Put them in `:root` tokens.
5. **Build.** Scaffold with `HYPERFRAMES_SKIP_SKILLS=1 npx -y hyperframes init <name> --example blank --non-interactive --resolution 1080p`, then start from `assets/loop-template.html` and edit the `scenes` array.
6. **Check and look.** Run `npm run check` and fix every error. Run `npx hyperframes snapshot --at <times> -o <dir>` at the start, middle and end of each scenario and read the contact sheet. Fix clipping, overlaps and the loop seam.
7. **Render.** Only after go: `npx hyperframes render -o clip.mp4`, then a GIF with ffmpeg (`fps=15`, `scale=960`, palettegen and paletteuse).
8. **Report.** Give the absolute paths, what is real and what is approximated, and what the viewer can't tell from the frames. Do not claim you watched the clip.

## What the layout is

One persistent view, no intro frame. A moving index of scenarios on the left, the terminal on the right, and a small pixel-art character at a computer bottom right as the only brand mark. The highlight bar slides to the active scenario, and the sub-line fades in under it. See `references/lessons.md` for sizes that fit.

## The post

Write the X post in the first person with no hype, and put the link in a reply. The video needs no captions: every command and result is on screen as text, so it reads muted. Upload the MP4 natively.

## Files

- `references/lessons.md` is what worked, what broke, and how to size text.
- `assets/loop-template.html` is a working 18-second composition with no external images. Copy it over the scaffolded `index.html` and edit the `scenes` array.
