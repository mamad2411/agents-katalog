---
name: orbyn-affectui
description: "Build agent UI in React from affectUI's free one-file components: tool-call cards, a decision inbox, a thinking loader, change summaries, message actions, comment threads, inputs and motion. Bundled and pinned; restyle to project tokens. Use when a React 19 app needs these pieces."
---

# affectUI components

Follow the consuming project's instructions and requested scope; use the
[portable defaults](../orbyn-workflow/references/project-policy.md) only where guidance is missing.

affectUI is an MIT library of React components, each one `.tsx` file with its styles
inside: no Tailwind, no CSS setup, no animation library. The free items are bundled
here, unmodified and pinned. [UI design](../orbyn-ui-design/SKILL.md) owns what the
interface should do; [agent-run views](../orbyn-ui-design/references/agent-run-views.md)
covers the agent screens; this skill covers using these files.

## What is bundled

Components and blocks come in two styles: `-clean` (white chips, hairline shadows) and
classic; pick one per product. Illustrations and motion have one file each.

| Folder | Items |
| --- | --- |
| [components](references/upstream/affectui/components/) | Agent work: tool-call card and group, decision inbox, thinking loader, change summary, smart recommendation, email draft for review, progress tracker, tips panel. Conversation: message actions, comment thread, reaction bar, notification stack. Inputs: button, checkbox, switch, select, segmented control, filter menu, tag input, text field, text area, OTP input, profile menu |
| [blocks](references/upstream/affectui/blocks/) | Logo marquee, testimonial wall |
| [illustrations](references/upstream/affectui/illustrations/) | Empty states and marketing scenes (agent team, integrations, layer stack, team invite and others) |
| [motion](references/upstream/affectui/motion/) | Grid background, number ticker, shimmer loader, text reveal |

Agent tree, trace waterfall, agent inbox, context map and agent handoff are paid Pro
items and are not here. Do not recreate them from the website or its screenshots;
design those views from [agent-run views](../orbyn-ui-design/references/agent-run-views.md)
with a design draft first.

## Use one

1. **Check fit.** React 19, a client component (`"use client"`), and nothing in the
   project already covering the job. Prefer the project's existing component when it
   has one.
2. **Copy the reviewed file.** Copy the item from the bundle into the project's
   components folder, keep its header comment, and add one line naming the source
   revision (`affectUI 3c5df43`). This is the version we reviewed. Use the shadcn
   registry (`npx shadcn@latest add https://www.affectui.com/r/<item>.json`) only when
   the user asks for the live version, and say it may differ from the bundle.
3. **Restyle through variables.** Components and blocks declare their colours, radius,
   shadows and easing as CSS custom properties: a shared `--aui-*` set and a per-item
   prefix (for example `--ui-tclc-*` on the tool-call card). Illustrations and motion
   use only their own prefix (for example `--ui-ti-*`, `--ui-nt-*`). Map those to the
   project's tokens, or to the [Orbyn house style](../orbyn-ui-design/references/house-style/README.md)
   when it has none, in one place; leave the rest of the file alone so a later refresh
   is a clean diff. Dark mode follows `.dark` or `data-theme="dark"` on an ancestor.
4. **Feed real state.** Drive status from real events: the thinking loader's `phase`
   from stream events, not its demo timer; a tool-call card's state from the actual
   call; decisions from the backend that will act on them. A component renders state
   and calls back; the app validates, authorizes and performs the effect.
5. **Verify.** Render it in the product in light and dark, with reduced motion on,
   long text, empty and error data, keyboard only and a screen reader announcement
   for live updates. The library's accessibility claims are a starting point, not
   evidence.

## Rules for every host

- **Never update by hand.** Do not re-run `shadcn add` or copy newer files from the
  website to "update" an item. `scripts/upstream_watch.py` opens an issue when
  affectUI changes; the bundle is refreshed through
  [upstream review](../orbyn-upstream-review/SKILL.md) in a reviewed PR, and projects
  take the new file from there.
- **No new MCP server without asking.** affectUI offers an MCP server and `llms.txt`
  for coding assistants. Adding that server to a host is a configuration change.
- **Brand marks are not ours.** Logo blocks and some illustrations draw third-party
  logos or name other products (for example model providers); the MIT licence covers
  the code, not those trademarks. Replace them with marks and names the product may use.
- **Keep the licence.** A copied file keeps its header; the project credits affectUI
  (MIT, Florian Höller) where it lists third-party code.

## Source and updates

Bundled from [flohoeller/affectui](https://github.com/flohoeller/affectui/tree/3c5df43893d870ee42d81fad4a4ba3ad72ba1b99)
at `3c5df43`, MIT, with the licence and a `snapshot.json` of file hashes. Showcase
images, the README and Pro items are not bundled.
