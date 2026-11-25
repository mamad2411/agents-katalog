---
name: use-browser
description: >
  The agent's EYES — `npm run eyes`, a browser with no window that ships with every node: it opens a page of this node, clicks,
  takes a screenshot and tells what lies on top of what. Load it before you show any built surface to a person (a page, a drawer,
  a banner, a menu), when a proof needs the eye rather than the wire — console errors, a layout that is formally correct and looks
  wrong, an element covered by another — and before believing any measurement taken through automation. Needs no extension and
  no account of the person. Acting in SOMEONE ELSE's interface (a registrar, Google, Resend) is `help-in-browser`, not this.
---

# use-browser — the eyes

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

## 1. The rule that changes behaviour

**A built surface is SEEN before it is shown** (CLAUDE.md §6). «The class is in the build» proves the code arrived, not that the page
looks right. ✗ 2026-11-04, step 645-1: the drawer was proven by its CSS in the chunks and shown to the owner twice — with a hole on top
and a shift too big; one screenshot would have shown both.

## 2. The tool

```
npm run eyes -- <address> [--click "<text or css>"]… [--measure "<css>"]… [--top] [--width 390] [--dark] [--full] [--out <file.png>]
```

It prints the browser, the answer and the title, the screenshot path (`logs/eyes/<time>.png`), every console and page error, and for each
`--measure`: the box and what lies on top of its corner — «виден», «ПЕРЕКРЫТ: <who>» or «вне экрана». **Open the PNG and look at it**
(the Read tool shows images): a number does not see a broken rhythm, a hole or a fourth item that fell to a second row.

- Browser order, no questions: Playwright's own Chromium → the installed Chrome → Edge. `===EYES_NO_BROWSER===` — say it in one line
  with what to install (`npm run eyes:install` after); do not fall back to guessing.
- A clean browser every run: no person's session, no cookies. On `localhost` the core's panel opens without sign-in (the owner at the
  keyboard); on the temporary address it is read-only; on an own domain it is signed out — say which you measured.
- One check = one run, the browser closes after it; no resident process.

## 3. 🔒 Measurements that lied here

- **The panel scrolls itself to the content on load** — the bars above the header leave the screen, and an element out of view looked
  «covered». `eyes` now says «вне экрана»; `--top` scrolls to the start before the screenshot.
- **A tab opened before a rebuild shows the previous build** (the owner's Safari, 2026-11-04: old drawer items after the rebuild). A
  person's screenshot that contradicts `eyes` — ask them to reload with ⌘⇧R before you change code.
- **A registered service worker serves the PREVIOUS build.** `eyes` starts clean; the person's browser does not (`use-pwa`).
- **`scroll-smooth` makes a scroll position read back wrong** — measure after `behavior: "instant"`.
- **A screenshot times out, then works on the retry.** One timeout is not a broken page; retry once.

## 4. Reading a page like a person

- Both themes (`--dark`) and a narrow window (`--width 390`) for anything a visitor sees.
- Open what the person opens: `--click "Личный кабинет"` before measuring a drawer; measure the title AND the close button.
- Count elements rather than words: «privacy» also lives in structured data and class names.
- Scripts off for public pages is a wire check: `curl` the served markup (`use-aio`).

## 5. Before you call it seen

Name the state: address (localhost / temporary / own domain), width, theme, what was clicked. Then show the person the screenshot or
say where it is. `eyes` is not a proof of a foreign site — for those you act in the person's Chrome (`help-in-browser`).
