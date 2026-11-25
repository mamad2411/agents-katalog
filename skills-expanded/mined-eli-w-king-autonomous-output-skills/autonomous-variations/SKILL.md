---
name: autonomous-variations
description: "Variations (AI-First edition): a few genuinely different takes on one part of your app, built at once. One session starts a parallel session per direction, each on its own branch, then opens a lab you flip through in the integrated browser with the repo's switch or ?v=, [ and ], and a switcher pill. Use for 'make N variations', 'explore options', 'four different toolbars', 'a lab for X'."
---

# Variations (AI-First edition)

Turn "show me a few ways to do X" into a lab the person flips through, then picks from. Four directions unless
they ask for another number. Shipping the pick follows [autonomous-prototypes](../autonomous-prototypes/SKILL.md).

## Rules

1. **Follow the repo.** Read `AGENTS.md` first. If it has a variations slot (a file per variation, a switch like
   `?toolbar=<slug>`, one default line), use exactly that; otherwise the generic lab below.
2. **Genuinely different:** each direction changes how the thing works or reads, not just a color or size. Each
   gets a slug, a name and a one-line idea. Only the decision changes; everything else still works.
3. **One session per direction, in parallel,** each in its own worktree and branch, adding only its own files.
4. **Cheap:** one size, a 13-inch laptop at 1280x800, unless asked; no console errors; one screenshot each. No push
   or PR until they pick.

## Steps

1. **List the directions** from the person's words or the brief they name (such as `workshop/pm-follow-up.md`),
   show it, and start.
2. **Set the base:** commit pending work in the main checkout and note `git rev-parse HEAD`, so every variation
   has the latest fixes. Get this chat's link with `get_current_session`.
3. **Start the sessions** all at once: `create_session` per direction, with `workspace` the repo folder,
   `worktree: true`, `model` "GPT-6.2 Sol" (or the person's model), a short `title` and the brief below. Without
   session tools, use parallel subagents, each in its own `git worktree add`.
4. **Tell the person, while they build:**
   - the sessions are listed under this one in the sessions list, on the left of the Agents window
   - to add a thought to one, type in its box and open the Send button's menu: **Add to Queue** runs after its
     current turn, **Steer with Message** reaches it right away
   - meanwhile, critique the directions or suggest another

   Then end your turn; the reports arrive as messages.
5. **Make the lab:** `git switch -c lab/<topic> <base>` in the main checkout, then `git merge --no-edit
   lab/<slug>` for each. Reuse the running dev server and open the lab in the integrated browser.
6. **Check each variation** at 1280x800: no console errors, nothing wraps, overflows or covers the canvas or the
   welcome screen, and the main task works (for a toolbar, draw a shape). Fix small breakages on the lab branch.
7. **Report** the lab link, a table (slug, name, idea), how to switch (`[` and `]`, the pill or the URL), the
   screenshots, and anything that didn't land. Ask which one they like.

## The brief for each session

```text
Build one variation of <what>, in parallel with other sessions. Read AGENTS.md first and follow it.
Direction: <name> (<slug>). Idea: <one line>. Intent: <their words or the PM team's>.
First: git switch -c lab/<slug> <base>
Add only your own files (<slot path, or labs/<slug>/>); don't edit shared files.
Get dependencies as AGENTS.md says (else npm ci --prefer-offline; npm.cmd on Windows), start the app, open
<link with the switch set to <slug>> in the integrated browser at 1280x800, use it once, and fix any console error
or anything that wraps, overflows or covers the canvas or the welcome screen.
Screenshot: node "<skills folder>/autonomous-demos/scripts/demo.mjs" shot --url <link> --out <review/shots/<slug>.png> --width 1280 --height 800
Commit on lab/<slug>; don't push. Then send_message to <this chat's link>: branch, commit, link, screenshot, one line.
```

`<skills folder>` is `~/.copilot/skills`, or `$COPILOT_HOME/skills`.

## Generic lab (no slot in the repo)

- Each variation renders when `?v=<slug>` is set; no `v` is today's version. Scope its CSS under its own class.
- Copy [`scripts/lab-pill.js`](scripts/lab-pill.js) into the project's static files and load it after setting
  `window.labVariations = [{ id, name, idea }]`, today first: the pill, `[` and `]`, hidden with `?embed=1`.
- Each worktree's server takes its own free port; the lab runs from the main checkout.

## After the pick

Make the pick the default in one clear line, keep the others reachable by URL, and ship it with
autonomous-prototypes. Offer to remove the variation worktrees (`git worktree remove <path>`) to free disk space.
