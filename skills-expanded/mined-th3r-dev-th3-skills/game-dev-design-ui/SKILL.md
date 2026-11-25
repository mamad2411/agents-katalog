---
name: game-dev-design-ui
description: >-
  Design a Roblox game's interface (HUD, shop, inventory, rewards, menus, onboarding prompts) as
  design-core applied to Roblox. Read the game's loop first; write a design brief per surface with
  every state and get it approved before building; then lay it out phone-first with Scale, AnchorPoint
  and constraints inside the core-UI safe insets; style it from StyleSheet tokens that match the
  game's look; keep value decisions on the server; and check it in a Studio playtest at phone, tablet
  and desktop. Works in any agent (Claude Code by default; Codex, Cursor, Gemini CLI). Use WHENEVER
  the work is "Roblox UI", "game UI", "HUD", "shop UI", "inventory UI", "reward popup", "menu",
  "ScreenGui", "BillboardGui", "mobile UI", "UI looks bad on phone", "buttons too small",
  "UI design", "UI/UX", "StyleSheet", "Style Editor", "design tokens in Roblox", "UI review",
  "first-time player experience", "onboarding", "ออกแบบ UI เกม Roblox", "หน้าร้านในเกม", "ทำ HUD",
  "UI มือถือ", or before building any ScreenGui.
---

# Design UI (Roblox)

This is [design-core](../../design/core/SKILL.md) applied to Roblox. design-core holds the
principles: the order of authority, composition, interface writing, the interface baseline, the
working order and the 0-10 review table. Read it first. This file adds only what Roblox changes.
Set the project up with [`../roblox/SKILL.md`](../roblox/SKILL.md); write Luau in its
[house style](../roblox/references/luau.md).

If the design skill isn't installed, keep its three rules that matter most here: one focal point
and spacing from tokens; labels that start with a verb and say what happens; every surface has its
default, empty, loading and error state.

Detail: [layout](references/layout.md), [visual language](references/visual.md),
[styling and tokens](references/styling.md), [the brief templates](references/design-brief.md),
[review and playtest](references/review.md).

## How design-core maps onto Roblox

| design-core | On Roblox |
|---|---|
| Order of authority: the request, then the product's system, then platform rules, then defaults | The product's system is the game's StyleSheet tokens and its existing screens. The platform rules are Roblox's: core-UI insets, the default touch controls, console and touch input |
| Workflow: understand → inventory → intent → build → review → hand off | Intent is the **design brief**, and nothing is built until it says `Status: approved`. Build is Luau with tokens. Review is on Studio captures at three devices |
| Composition, writing, interface baseline | The Roblox conventions below, and a shop's extra states: affordable, unaffordable, owned |
| Review table, 0-10, pass at 8+ | Three more rows: mobile fit, the first action, the trust boundary ([review.md](references/review.md)) |
| Reference first, off-default, taste | References are the game's own thumbnail and screens, then the catalogue in [visual.md](references/visual.md). Take grammar from a reference, never a paid pack's art |

## Rules

1. **Read the game first.** The loop and the goal decide what the HUD shows: the objective, the
   currency, progress, health or energy, the next reward. No brief yet: run
   [`../design-lens/SKILL.md`](../design-lens/SKILL.md). The player should act within 10-30 seconds;
   teach by doing, with a prompt and an objective marker, not a wall of instructions.
2. **The design gate.** Before building a surface, write `design/DESIGN.md` once (tokens, type,
   spacing, conventions) and `design/features/<surface>/design.md` for each surface: its job, the
   layout on phone, tablet and desktop, every state, the interactions and the copy. It ends with a
   `Status:` line. It stays `draft` until the person approves it; only `approved` gets built.
   Templates: [design-brief.md](references/design-brief.md).
3. **Layout phone-first** ([layout.md](references/layout.md)): Scale with every Offset at 0 (a needed
   Offset means a missing layout object), an AnchorPoint at the corner the element grows from,
   UIListLayout / UIGridLayout / UIPadding / UIAspectRatioConstraint instead of hand positions,
   `ScreenInsets = CoreUISafeInsets`, nothing that matters in the bottom-left and bottom-right
   corners (the default thumbstick and jump button), frequent buttons in the thumb zone. Design at
   1280×720 and check it larger.
4. **Visual language** ([visual.md](references/visual.md)): the most important thing first and
   biggest; colour, size, space and proximity spent on what matters, with restraint. Keep Roblox's
   conventions: a red square X at a dialog's top right, greyed buttons when unusable, a lock over
   what isn't unlocked, a red price when the player can't afford it, and one colour per stat
   everywhere it appears. Two fonts, display and body. White icons, recoloured with `ImageColor3`.
5. **Tokens, not literals** ([styling.md](references/styling.md)): colours, type, radius and
   spacing live in a StyleSheet, with themes that swap. They come from the game's look, so the
   UI matches the thumbnail that sold the game.
6. **States and feedback**: every button has default, hover, pressed, disabled and loading; every
   action answers with a tween and a sound; a reward shows the delta and the next goal, briefly.
   No popup interrupts the core action in the first five minutes.
7. **The client shows, the server decides.** A RemoteFunction asks to buy; the server checks the
   price, the currency and the lock, then answers. The client never grants value, and shows
   `loading` until the answer arrives.
8. **Run it.** Playtest in Studio, then capture each surface in the Device Emulator at a phone
   (about 844×390 landscape), a tablet (1024×768) and 1920×1080, in every state, with the Studio MCP
   server's screenshot tool, or by hand. Read the output log for errors. A check that could not run
   is NOT ASSESSED, never a pass.
9. **Review with fresh eyes**: score the captures with design-core's table plus the Roblox rows. In
   Claude Code a subagent does it; elsewhere a new session or a second model. The author's own score
   never decides. Then hand off per [review.md](references/review.md).

## Worked example

[examples/craghold-hud](examples/craghold-hud/README.md): the HUD and dungeon-key shop of Craghold,
the mock game whose thumbnails design's thumbnail-keyart makes. It includes the approved briefs,
StyleSheet tokens taken from the thumbnail, pure Luau modules tested under Lune, a server that
checks every purchase, and Studio captures at three devices.

## Sources

| Source | What it gives |
|---|---|
| [AshExplained/roblox-skills@a3a7b94](https://github.com/AshExplained/roblox-skills/tree/a3a7b94/roblox-game-ux) (MIT) | first action in 10-30 s, the HUD's contents, the onboarding order, the UX review output, the design gate with `Status:`; its `roblox-ui-implementation` (client renders, server decides) |
| [Roblox: UI](https://create.roblox.com/docs/ui), [position and size](https://create.roblox.com/docs/ui/position-and-size), [on-screen containers](https://create.roblox.com/docs/ui/on-screen-containers), [styling](https://create.roblox.com/docs/ui/styling) | containers, layouts, modifiers, ScreenInsets, reserved corners and thumb zones, universal styling with tokens and themes |
| [Roblox: UI/UX design](https://create.roblox.com/docs/production/game-design/ui-ux-design) | the hierarchy of information, attention, visual language, conventions, consistency, feedback, flows |
| [DevForum: The Ultimate UI Design Guide](https://devforum.roblox.com/t/the-ultimate-ui-design-guide/1236916) | sketch, then Figma, then rebuild in Studio from Properties; white recolourable icons |
| [DevForum: UI designing tips](https://devforum.roblox.com/t/ui-designing-tips/2423307) | Scale only, two fonts, a 1280×720 baseline, AnchorPoint at the growth corner, the Device Emulator, ten-foot UIs |

The AshExplained text is restated, not copied.

## Agents other than Claude

Plain Markdown and shell commands, like the rest of game-dev; loading per agent is in the umbrella's
[Agents other than Claude](../SKILL.md#agents-other-than-claude). Studio MCP for an agent:
`python ../roblox/scripts/roblox_setup.py mcp --client <claude|codex|cursor|gemini|vscode>`, with
`claude` the default. The example's tools (Rojo, Lune, Selene, StyLua) run from any shell.
