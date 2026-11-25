---
name: user-manual
description: Writes end-user manuals for a web app as PDF and DOCX, with real screenshots taken with Playwright and a clean Word template (cover, header, footer, table of contents). Use when asked for "/user-manual", a user manual, a user guide, how-to documentation or training material for the end users of a web app.
argument-hint: "[topic or walkthrough name]"
---

# User manual

Produces a manual from a **walkthrough** of the real app, with screenshots and
a neutral Word template (cover, header, footer and table of contents) that
`scripts/build_template.py` generates on first use. The result follows
`references/manual-style.md`.

In this guide `$H` is this skill's `scripts/` folder and `$V` is
`../visual-check/scripts`. `$V` holds the config loader and the walkthrough
runner shared by the three webapp-docs-kit skills.

## Before you start

1. If `$V/node_modules` does not exist, run `cd $V && npm install`. The browser
   is installed once with `node $V/node_modules/playwright-core/cli.js install chromium`.
2. Read the project's `README.md` and `CLAUDE.md`/`AGENTS.md`, its routes and
   navigation, to learn which screens and tasks exist and how the app is started.
3. **Ask the user** what you cannot work out from the code:
   - Which environment to capture: local, dev or staging. **Never use production.**
   - What the manual should cover and for whom. If the app is large, propose
     splitting it into several manuals (one walkthrough each, for example
     `getting-started`, `orders`, `admin`) and let the user decide.
   - The organization shown on the cover and the support contact.
   - The language of the manual, if it is not English (see "Other languages").

## Screens behind sign-in or other preconditions

This kit does not sign in, handle credentials or assume user roles. If the
screens to document are behind a login, a specific role, a feature flag or any
other precondition, **stop and ask the user how they want to handle it**. It is
their decision. Never ask for, type or store passwords, tokens or cookies
yourself, and never work around access controls.

## Steps

1. **Project config.** Create or update `docs/webapp-docs.json` following
   `../visual-check/references/configuration.md`. It is the same config
   `/visual-check` uses. If it already exists, use it.
2. **Walkthrough.** Write `docs/manuals/<name>/walkthrough.json`: scenes and
   steps covering what the manual explains. Add `"screenshot"` to the steps that
   get a figure. `/video-tutorial` uses the same file. The format is in
   `references/walkthrough-format.md`. To find selectors, run
   `node $V/check.js <path> --html` and look at the screenshot before writing
   long walkthroughs. Selector tips are in
   `../visual-check/references/capture-pitfalls.md`.
3. **Screenshots.**
   ```bash
   cd <project>
   node $H/capture.js docs/webapp-docs.json docs/manuals/<name>/walkthrough.json
   ```
   **Open every PNG.** Check that no screen came out blank, that personal data
   is blurred (`redact`), that no dev chrome shows, and that each crop shows
   what the text describes. If something is off, fix the walkthrough and rerun.
4. **Text.** Write `docs/manuals/<name>/manual.md` following
   `references/manual-style.md` and `references/markdown-format.md`. Describe
   only what the screenshots and the code confirm. Do not invent features.
5. **Build.**
   ```bash
   cd docs/manuals
   python3 $H/build_manual.py <name>/manual.md <name>/manual-<app>-<name>.docx
   python3 $H/to_pdf.py <name>/manual-<app>-<name>.docx \
       --title "User manual — <App>" --author "<Organization>"
   ```
   On Windows use `python` instead of `python3`. `to_pdf.py` recomputes the
   table of contents and writes the `.pdf` next to the `.docx`. It uses
   LibreOffice when installed (and relaunches itself with LibreOffice's Python
   if needed) or Microsoft Word on Windows.
6. **Mandatory visual review.** Render the PDF to images with
   `pdftoppm -r 50 -png manual.pdf <temp folder>/pg` and open them. Check that
   the table of contents has page numbers, that no figure is cut off and that no
   table overflows. Do not call the manual done without looking at it.
7. Repeat steps 2 to 6 for every manual requested.

## Rules

- **Screenshots never change data.** `capture.js` refuses to click Save,
  Delete, Submit, Send, Sign and similar buttons. Use `"simulate": true` on
  those steps: the button is highlighted but not clicked. Use
  `"allowChange": true` only with the user's explicit authorization for that
  step, and only in a test environment.
- Blur every element with personal data.
- If a screen looks different from what you expected, tell the user. It may be
  a bug in the app. Do not hide it in the manual.

## Other languages

Write `manual.md` in the target language and set `title`, `preface_title`,
`contents_title` and `figure_label` in its front matter (see
`references/markdown-format.md`). Add the language's destructive button labels
to `protectedLabels` in the config.

## Custom template

The default template is neutral (no logos). To brand it, either regenerate it
with other colors (`python3 $H/build_template.py out.docx --primary 0F766E --accent F59E0B [--letter]`)
or open it in Word/LibreOffice, add a logo, change fonts and colors, keep the
`{{...}}` markers, and pass it with `--template my-template.docx`.
`build_manual.py` stops and says what is missing if the template is unusable.

## Delivery

Leave in `docs/manuals/<name>/` the `walkthrough.json`, `manual.md`,
`screenshots/`, the `.docx` and the `.pdf`. At the end, report each PDF's path,
its page count, and any screen that could not be captured.
