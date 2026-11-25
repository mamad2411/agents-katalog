---
name: ctf-writeup-discipline
description: Produce CTF write-ups with authentic solve evidence, scripts, screenshots,
  and clean separation from reference material. Use when writing, revising, or packaging
  CTF write-ups, especially when the user provides someone else's write-up as reference
  or requests screenshots.
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- ctf
- writeup
- screenshots
- evidence
- packaging
related_skills:
- digital-forensics
- ctf-reverse-engineering
- binary-exploitation
---

# CTF Write-up Artifact Discipline

## Trigger

Load this skill whenever producing a CTF write-up, especially if:
- the user provides another player's write-up as reference
- the user asks for screenshots of the solve process
- the write-up must include scripts / explanation / proof of solving
- files need to be organized for submission or later review

## Hard Rules

1. **Do not fabricate screenshots.**
   - Screenshots must come from an actual app/window/session via `screencapture`, browser screenshot, or other real capture mechanism.
   - Do not generate fake terminal/browser screenshots with PIL/HTML/image generation and present them as solve screenshots.
   - Diagrams are allowed only if explicitly labeled as diagrams, and only when the user asked for diagrams.

2. **Do not mix reference write-ups with your own write-up.**
   - Put reference/original material in `original_writeup/`.
   - Put the newly authored write-up, scripts, logs, screenshots, and flag in `my_writeup/`.
   - Add a top-level `README.md` that explains the separation.

3. **A write-up must include both思路 and解法.**
   - Challenge observation / artifact inventory
   - Vulnerability or mathematical insight
   - Step-by-step solve explanation
   - Commands run and key outputs
   - Full scripts or clearly linked script files
   - Final flag and verification

4. **Screenshots should support the story, not replace it.**
   - Capture normal-looking terminal/browser windows showing real commands and outputs.
   - Include screenshots for: artifact inventory, key intermediate recovery, exploit/solver run, final flag, and script view when requested.
   - Keep image links relative and verify all links resolve after moving folders.

## Preferred Folder Layout

```text
challenge_dir/
  README.md
  original_writeup/
    <reference write-up files>
    writeup_images/
  my_writeup/
    MY_WRITEUP.md
    scripts/
      solve.py / solve.sage / exploit.py
    logs/
      run.log
    screenshots/
      01_inventory.png
      02_key_step.png
      03_solver_run.png
      04_final_flag.png
    FLAG.txt
```

If the user wants a simpler layout, `my_writeup_images/` next to the markdown is acceptable, but keep it inside `my_writeup/`.

## Screenshot Workflow on macOS

For real terminal screenshots:

1. Run the real command and save logs:
   ```bash
   script -q logs/solver.typescript
   sage solve.sage | tee logs/solve.log
   ```
2. Open/show the evidence in Terminal.
3. Capture the real Terminal window:
   ```bash
   screencapture -x -l <WINDOW_ID> screenshots/03_solver_run.png
   ```
4. Verify dimensions and existence:
   ```bash
   sips -g pixelWidth -g pixelHeight screenshots/*.png
   ```

Using AppleScript to drive a temporary Terminal window is fine, but it must run/display real commands and outputs. Do not synthesize the pixels.

For browser screenshots:

1. Prefer real desktop/window captures when the user explicitly wants "直接在電腦上截圖" rather than tool-exported page images.
2. If using a real browser window, check for privacy leaks before keeping the screenshot: visible bookmarks, signed-in avatars, account names, extension popups, local file paths, and other personal UI chrome.
3. If a direct computer screenshot leaks personal information, replace it with a sanitized preexisting challenge screenshot or a browser-capture image that hides personal chrome, and explain the swap in the write-up if needed.
4. Do not keep a screenshot merely because it is more "real" if it exposes the user's personal account details.

## Naming / reference discipline

- If the challenge title in the user's folder or provided reference write-up differs from the hostname / deployed service name, preserve the user-visible challenge title in your write-up unless the user asks to rename it.
- Example: if the folder/reference says `easywab` but the live host is `easy-session`, write the challenge name as `easywab` and mention the target URL separately.

## Write-up Checklist

Before finalizing:

- [ ] Reference and own work are in separate folders.
- [ ] Markdown image links resolve from the markdown's location.
- [ ] No generated/fake screenshots are used as evidence.
- [ ] Any diagram is labeled as a diagram and not called a screenshot.
- [ ] Full solve scripts are embedded or placed under `scripts/` and linked.
- [ ] Commands and outputs shown in screenshots correspond to actual logs/files.
- [ ] Flag is verified from the solver output.
- [ ] Top-level README explains where to read the final write-up.

## macOS Screenshot Capture Workflow

For real terminal screenshots on macOS:

1. Start a real solve transcript:
   - Use a visible terminal with the challenge directory open.
   - Run commands naturally: unzip, list files, inspect binary/source, execute program, debug, test payloads.
   - Keep terminal width readable, usually 100-140 columns.

2. Capture screenshots at these points:
   - Challenge files extracted and identified.
   - Important static analysis result: `file`, `strings`, `checksec`, source snippets, decompiler/debugger view.
   - Vulnerability discovery: crash, sanitizer/error output, debugger register/stack view, suspicious code path.
   - Exploit construction: payload script, local proof, remote command if applicable.
   - Flag acquisition: final successful output with the flag visible, if challenge rules allow.

3. Use macOS screenshot capture naturally:
   - `Cmd+Shift+5` for screenshot UI when doing manual-style capture.
   - `screencapture -x -l <WINDOW_ID> screenshots/03_solver_run.png` for scripted capture.
   - Window or selected-region screenshots are preferred over full desktop unless the write-up being matched uses full desktop screenshots.

4. Name and index screenshots immediately after capture:
   - Use ordered filenames: `01-unzip-files.png`, `02-checksec.png`, `03-crash-repro.png`, `04-debug-root-cause.png`, `05-exploit-flag.png`.
   - Keep screenshot order aligned with the write-up narrative.
   - Never leave only `截圖 2026-...png` in the final artifact.

5. Verify screenshots:
   - `sips -g pixelWidth -g pixelHeight screenshots/*.png` — confirm dimensions.
   - No secrets, unrelated private windows, or personal information visible.
   - Every screenshot is from the real solve environment (not generated/synthetic).

## Matching Another Write-up's Screenshot Style

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

## Pitfalls Learned

- A polished image that looks like a terminal but was generated with code is misleading; users can spot it and may reject the write-up.
- If a reference write-up already has `writeup_images/`, do not reuse that folder name for your own screenshots in the same directory; it causes attribution confusion.
- When moving markdown into a subfolder, update image paths and verify them programmatically.
- Do not create polished diagrams when the user asked for natural screenshots.
- Do not take screenshots after cleaning up terminal history if that makes the process look artificial.
- Do not rely on only text logs; the user explicitly wants visual solve evidence.
- Do not include unrelated apps/tabs in screenshots.
- Do not crop out the command that produced an output; the command is often the evidence.
- Do not keep a screenshot merely because it is more "real" if it exposes the user's personal account details. Replace with a sanitized capture.
