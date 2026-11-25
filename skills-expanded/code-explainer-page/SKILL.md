---
name: code-explainer-page
description: Explain a piece of code or a fix to its owner in one throwaway HTML page opened in the browser, in eli5 style (big pictures, few words) - picture steps drawn in inline SVG, a read-only code editor (line numbers, syntax colors, green/red diff lines) pulled straight from git, numbered notes pinned to line ranges that light up the code when clicked, a double-check table with evidence, and a glossary. Use when the user says "show me the code", "explain the code/fix/diff to me", "walk me through this change", "open it in a browser so I can read it", or wants to review a commit or PR before approving it. The page is a review copy; delete it after review with --clean.
---

# Code explainer page

One local HTML file that lets a non-expert owner read real code with plain-English notes beside
it. Self-contained (inline CSS and JS, no CDN), opened in Chrome, deleted after review.

## When to use
- "Show me the code", "explain this fix", "walk me through the diff", "what does this change do".
- Before asking the owner to approve a commit or PR, so they can read what they approve.
- Not for architecture overviews (use a diagram skill) or for publishing docs (this page is temporary).

## Steps

1. **Double-check the code first.** Read the changed lines and every caller of what changed. Note
   real evidence: file:line, values, types, what overrides what. Anything you could not verify
   goes in the checks as `warn`, never as `pass`.
2. **Write a spec JSON** in the session scratchpad (format below). Prefer `git` blocks over pasted
   code: the script reads the exact file at a commit and marks added and removed lines against
   `base`, so line numbers cannot drift.
3. **Render and open:**
   ```bash
   node ~/.claude/skills/code-explainer-page/scripts/render.mjs <spec.json> --open
   ```
   It prints the output path (default `<os tmpdir>/code-explainer/code-explainer-<slug>.html`).
   `--out <file>` picks another path; the file name must start with `code-explainer-`.
4. **Verify before telling the owner it is ready**: load it in a headless browser or screenshot it,
   click one note, and check its badge sits on the right lines and that the page has no script errors.
5. **Reply in the terminal** with the path and two or three lines. Do not paste the page.
6. **After review**, delete it (the page footer shows the exact command):
   ```bash
   node ~/.claude/skills/code-explainer-page/scripts/render.mjs --clean <file>   # one page
   node ~/.claude/skills/code-explainer-page/scripts/render.mjs --clean          # every page in the default folder
   ```

## Spec format

```json
{
  "meta": { "title": "...", "subtitle": "...", "slug": "short-name",
            "repo": "...", "branch": "...", "commit": "...", "date": "YYYY-MM-DD" },
  "bigPicture": [ { "title": "What people saw", "text": "One or two plain sentences.",
                    "svg": "<svg viewBox='0 0 260 190' xmlns='http://www.w3.org/2000/svg'>...</svg>" } ],
  "files": [
    { "path": "src/x.js", "language": "javascript",
      "git": { "repo": "/path/to/repo", "rev": "HEAD", "base": "HEAD~1",
               "path": "src/x.js", "from": 10, "to": 80 } },
    { "path": "snippet.js", "language": "javascript", "startLine": 1,
      "code": "pasted code when there is no git", "added": [3, 4],
      "removed": [ { "after": 2, "text": "old line" } ] }
  ],
  "notes": [ { "file": 0, "lines": [12, 15], "kind": "fix",
               "title": "Short title", "body": "Plain words. `code` and **bold** work." } ],
  "checks": [ { "status": "pass", "label": "What was checked", "detail": "Evidence with file:line." } ],
  "glossary": [ { "term": "postCode", "meaning": "Plain meaning." } ]
}
```

- **Every changed file needs `base`** so its panel shows the green CHANGED banner. A panel with no
  diff lines is labeled "NOT CHANGED: shown only to explain the fix", and changed panels are listed
  first. Never show a context file in a way that looks edited; say in its notes that it is unchanged.
- `files[].git.base` is optional; without it no diff marks are drawn. `from`/`to` are line numbers
  in the `rev` version of the file. Several panels from the same file are fine.
- `notes[].file` is the index in `files` (or its `path`). `lines` are real line numbers.
- `kind`: `what` (what it does), `why`, `fix`, `risk` (watch out), `check`. Each gets a color.
- `checks[].status`: `pass`, `warn` or `fail`.

## Match the size of the change

A 3-line fix gets a small page. The owner must see at once how big the change really is.

- The main code section shows only what changed: each changed file opens on its changed lines plus
  3 lines around them (`files[].context` to change that). The rest sits behind a "Show the N lines
  around it" button.
- The banner counts what was added: lines of code, comment lines and blank lines, separately.
- Unchanged files (context) go into a closed "Background, not changed" section with their notes.
  Add one only when the owner needs it to understand why; never more than two.
- In the main section, pin notes on the changed lines only. One note per changed block is usually enough.
- Never present more code than the change itself as if it were the change.

## Proof: before and after

When the change has a visible result (UI fix, error message, output), the page must show proof,
**before and after**, in a "Proof it works" section placed right after the code.

- Add `proof` to the spec:
  ```json
  "proof": [
    { "label": "before", "path": "/tmp/proof/before-bug.webm", "caption": "Old code: what goes wrong." },
    { "label": "after",  "path": "/tmp/proof/after-fixed.webm", "caption": "New code: same steps, fixed." }
  ]
  ```
  `label` is `before` or `after` (red or green tag). Video `.webm`/`.mp4`/`.mov` or image
  `.png`/`.jpg`/`.gif`/`.webp`. Files up to 30 MB are embedded in the page (it stays self-contained
  and survives scratchpad cleanup); bigger ones are linked.
- **Before must be the real old code**, never a simulation: put the base version of the changed
  file back in the working tree without committing (`git show <base>:<path> > <path>`), rebuild,
  record, then `git checkout -- <path>`, rebuild again and record after. Check `git status` is
  clean at the end (revert any build churn).
- Record both with **the same steps** so they compare side by side. Use Playwright `recordVideo`
  in a fresh context; add a caption bar with what is measured at each step (for example the
  element positions and "overlap: YES/no"), so the video proves it with numbers, not only looks.
  Worked recorder: `examples/record-proof-video.mjs` (a generic template: optional sign-in from
  environment variables that are never printed; adapt the URL, steps and selectors).
- Wait for the element under test before measuring (`waitForSelector`), or the first caption
  measures an empty screen.
- No proof possible (backend-only change, no test environment)? Say so in a `checks` row with
  status `warn`; never leave the section looking complete.

## ELI5 style: big pictures, few words

Same style as the `eli5` skill: explain to someone who knows nothing about the code, with big
pictures and few words. The renderer prints a `warn:` line when a step has no picture or a text
runs long. Fix every warning before you open the page.

- `bigPicture`: 3 to 5 steps that tell the story without code: what the user saw, what was really
  happening, why, the fix. **Every step has an `svg`**: a simple inline SVG drawing
  (`viewBox='0 0 260 190'`, single quotes inside the JSON string, no external images, no emoji).
  Draw the screen or the idea: boxes, labels, one red mark for the problem, green for the fix.
  Text: one or two short sentences, under 30 words. A reader who looks only at the pictures should
  still get the story.
- `notes`: one idea each, under 45 words, everyday words. Put the fix note first. Notes on files
  that did not change start with "Not changed:".
- Explain a term the first time or put it in the glossary (keep meanings to a few words).
- Say what a line does for the user, not only what it does in code.
- Pin a note on every line range the owner must understand to approve the change; skip boilerplate.
- No emoji. No em dashes. Never invent behavior: every claim in a note or check comes from the code
  you read or a test you ran.

## Files
- `scripts/render.mjs`: renderer and cleaner (Node 18+, no dependencies; needs `git` for git blocks).
- `examples/example-spec.json`: a small worked spec (a shopping-cart total bug, 1 panel with pasted code, 4 notes, 3 checks). Render it with `node scripts/render.mjs examples/example-spec.json --open`.
- `examples/record-proof-video.mjs`: a generic Playwright recorder for before/after proof videos (needs `npm i -D playwright`).
