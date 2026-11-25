---
name: pour
description: Check web pages and UI code for WCAG 2.2 accessibility failures with the pour engine, and fix what it finds. Use when creating or changing HTML, components, templates or styles that render a page; when asked about accessibility, a11y, WCAG, screen readers, keyboard access, focus order, colour contrast or alt text; and before reporting UI work as finished.
license: MIT
compatibility: Needs the pour command (npm install -g pour-cli, or npx -y pour-cli) and an installed Chrome or Chromium for page audits. Uses the pour MCP server (pour mcp) when the client has it.
---

# Checking accessibility with pour

pour checks web pages against WCAG 2.2 Level A and AA with its own engine.
Its results come in two kinds, and they must be kept apart:

- **Violations** are failures the engine can demonstrate from the page. Fix them.
- **Needs review** means the engine abstained: the answer depends on
  something it cannot know, such as whether an image is decorative or
  whether captions match the audio. Do not count these as failures, and do
  not change code to make them go away by guessing. List them for the user
  as things a person needs to look at.

A clean result means pour found no failure it can detect. Automated checks
cover only part of WCAG, so never tell the user that a page is accessible,
compliant or conformant because a pour run came back clean.

## Tools

When the MCP tools from `pour mcp` are available, use them:

| Tool | Use |
| --- | --- |
| `pour_audit` | Audit a page. Takes `url` (a running dev server is fine) or `path` (a file on disk), plus `viewport`, `scroll`, `bestPractices`, `exclude`, `detail` and `maxNodes`. A template or component `path` is read as source. |
| `pour_focus_order` | The order the Tab key visits the page's controls, each with its accessible name, and the controls a `tabindex="-1"` has put out of reach. |
| `pour_screenshot` | A PNG of the page as it is, or through a simulation such as `deuteranopia`, `lowAcuity`, `focusOrder` or `landmarkMap`. |

Otherwise use the command line. If `pour` is not installed, `npx -y pour-cli`
runs the same command.

```sh
pour check src/components/Nav.tsx --format json   # source files, no browser
pour http://localhost:5173/ --format json          # the rendered page
pour dist/index.html --format json                 # a built page on disk
pour http://localhost:5173/ --viewport 390x844     # a phone-width layout
pour http://localhost:5173/ --filter deuteranopia --shot cb.png
pour --filter list                                 # every simulation name
```

Exit codes: 0 nothing found, 1 findings, 2 an error (an address that does not
load, a verification challenge, a sign-in page). Exit code 1 is the normal
result of finding something, not a broken command.

## Workflow

1. **Source first.** After editing markup, run `pour check` on the changed
   files (HTML, JSX, TSX, Vue, Svelte, Liquid, Nunjucks). Findings carry the
   file, line and column. Values that come from code are counted under
   `abstained`, not judged.
2. **Then the rendered page.** Colour contrast, focus order, computed names
   and anything built by script exist only in a browser. Start the project's
   dev server if it is not running, and audit each page the change touches.
3. **Note the state you audited.** Results depend on the viewport width,
   whether the page was scrolled (`scroll`, or `--scroll`, loads lazy
   content) and what was open. Audit at the default width, and at 390x844 as
   well when the change affects a responsive layout.
4. **Fix in the source**, guided by the Fix line the engine gives for each
   element. Make the smallest change that removes the failure.
5. **Audit again** in the same state and compare. Repeat until the
   violations in scope are gone, or explain why one remains.
6. **Check the keyboard path** with `pour_focus_order` after changing
   anything interactive: every control reachable, named, and visited in an
   order that follows the layout.

## Fixing without hiding

- Never make a finding disappear without fixing it. Do not use `exclude`,
  `aria-hidden="true"`, `role="presentation"`, `tabindex="-1"` or
  `display: none` on content or controls that people need.
- Prefer native HTML to ARIA: `<button>` over a `div` with `role="button"`,
  a `<label>` over `aria-label`. Add ARIA only when native HTML cannot
  express the thing.
- A control's accessible name must contain its visible text (WCAG 2.5.3).
  Do not give a button an `aria-label` that differs from the words on it.
- Alt text says what an image is for in its context. Use `alt=""` only for
  images that add nothing. When you cannot tell what an image shows, ask
  the user rather than invent a description.
- For contrast, change the colour where it is defined (a design token or a
  custom property), then audit again. Quote the ratio pour reports rather
  than estimating one.
- When a fix needs a decision only the user can make (wording, a brand
  colour, whether content is decorative), ask.

## Reading results

- `pour <page> --format json` gives the engine's full results. `violations`
  and `incomplete` (needs review) hold one entry per rule, with `id`,
  `impact`, `tags`, `help`, `helpUrl` and `nodes`. Each node has `target` (a
  CSS path), `html` and `failureSummary`, where the text after `Fix:` is
  the fix.
- `pour_audit` returns a compact form: `totals`, then `violations` and
  `needsReview`, each rule with its `wcag` criteria and up to `maxNodes`
  elements, each with `target`, `html`, `message` and `fix`. Pass
  `detail: "summary"` for the counts alone.
- `pour check --format json` gives `files[].findings[]`, each with `kind`
  (`violation` or `review`), `rule`, `impact`, `sc`, `message`, `fix`,
  `file`, `line` and `col`.

## Reporting to the user

Say what was audited (the address or the files), the viewport, and whether
the page was scrolled. Give the violations before and after, by rule, with
what changed. List the needs-review items separately, as things for a
person to check. Close with what pour cannot check, such as whether alt
text is accurate or whether the page makes sense read aloud, not with a
claim of compliance.

## When pour cannot run

- **No browser:** page audits need Chrome or Chromium; `--browser <path>`
  names one. `pour check` needs no browser.
- **A verification challenge or a sign-in page:** pour will not audit it and
  exits with 2. Tell the user. `--login` opens a window for them to sign in;
  it needs a person, so never use it unattended.
- **A dev server with a self-signed certificate:** `--insecure`.
- **A slow page:** `--wait <ms>` adds settle time after load.
