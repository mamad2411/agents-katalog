---
name: flowy
description: Use when starting or planning ANY Webflow build, design, styling, layout, CMS, component, or edit task — before choosing tools — and the moment you are about to reach for a Webflow MCP write tool to do VISUAL or detail work. Owns which-hand routing (Webflow MCP vs the Chrome-driven Designer), the session lifecycle for both new builds and already-built sites, and the paste-first rule for third-party components. Invoke FIRST, before flowy-manual or flowy-verify.
---

# flowy — the door

Marks used throughout: ✅ verified on the date given · 🚫 banned or refuses · ⚠️ caution · 🔍 unchecked, not yet verified by either hand.

**Three hands, not two.** Verified against Webflow MCP **2.0.1** on 2026-07-25.

| Hand | What it is | Use it for |
|---|---|---|
| **Clipboard / Designer paste** | `Copy to Webflow` → `cmd+v` on a selected element | **Any third-party Webflow component.** Lossless — see [paste-first](two-hands.md#paste-first) |
| **Chrome extension** (`claude-in-chrome`) | Your hands in the real Designer | **Visual judgment** — spacing, colour, type, states, "match this look" |
| **Webflow MCP** (`mcp__<server>__*`, any server name containing "webflow") | REST data + Designer session tools | Structure, CMS, bindings, components, props, variables, settings, audits |

> 🚫 **Read [house-rules.md](house-rules.md) first: it holds the hard standing rules**, including
> **never publish and never offer to publish**, never resize the window, small MCP calls, fonts, and
> the banned custom-code preview. Those override anything below.

## Routing — which hand

| Task | Hand | Why |
|---|---|---|
| Reproduce a third-party Webflow component (Osmo, cloneable, library) | **Clipboard paste** | Verified lossless: 24 styles with full properties + every data attribute + semantic tags. MCP construction dropped a class in the same session |
| Visual design: spacing, sizing, colour, typography, layout, hover/states, "match this look / this Figma" | **Chrome → drive the Designer** | WYSIWYG, iterative; type exact values into the Style panel |
| Style on a **component variant** | **MCP** `data_component_variants_tool` | ✅ **Corrected 2026-07-29.** `update_style` still has no `variant_id` — but `set_variant_styles` / `get_variant_styles` do, plus `breakpoint_id`, `pseudo` and `variable_as_value`. Verified: wrote `#111111` to a variant, read it back, base kept `#eeeeee`. Overrides are **sparse** — the readback returns only overridden properties. [styles-and-classes.md](styles-and-classes.md) §4 |
| Class audit, unused-style purge, unifying a legacy class system | **Export census first, then MCP** | Local grep gives per-class usage the Designer never shows; map by value, not by name. [styles-and-classes.md](styles-and-classes.md) §5–§7 |
| Element tree: insert, move, remove, attributes, display names | **MCP** `data_element_tool` / `data_element_builder` | Fast and reliable; `data_element_builder` builds nested trees in one call |
| **CMS field bindings** (image src, text, href, alt, visibility, tag, domId) | **MCP** `data_element_settings_tool` | ✅ **New in 2.0** — `get_bindable_sources` + `set_settings` with `source_type:"cms"`. No longer a Designer-only click |
| **Collection List** source / filters / sort / pagination | **MCP** `data_element_settings_tool` on the `DynamoWrapper` | ✅ **New in 2.0** — fully configurable; `static_json` values |
| **Convert static repeats → CMS-driven** | **MCP**, per [static-to-cms.md](static-to-cms.md) | **One Collection List per parallel group**, same collection, same sort. Index alignment is what breaks silently |
| CMS collections, fields, items | **MCP** `data_cms_tool` | The API is the fast, repeatable path for data |
| Components: create, transform, props, variants, **inside definitions** | **MCP** `data_component_tool` / `_props_tool` / `_variants_tool` + `scope_component_id` | ✅ **New in 2.0** — no canvas navigation needed |
| **Work out how a project is already built** — naming, structure rule, style architecture | **MCP** reads + **Chrome** for computed truth | [conventions.md](conventions.md). **Adopt what exists; imposing on a project that has a system is a defect** |
| **Componentize a section that contains component instances** | **MCP** `create_blank_component` → `insert_component_instance` | 🚫 `transform_element_to_component` **refuses** any subtree containing instances. [componentize.md](componentize.md) |
| **Composite prop surface** — a component's prop driving a nested component's prop | **MCP** `set_component_instance_prop_values` `binding_source_type:"prop"` | ✅ Verified 2026-07-29, incl. cross-type binds (boolean → visibility) |
| Create a **`slot`** prop — a hole the client fills with any component | **MCP** `data_element_builder type:"ComponentSlot"` | The prop is **derived** from the element, not created. Same for `variant` ← `create_variant`. Full guide: [slots.md](slots.md) |
| **Fill** a slot | **MCP** `data_component_builder action_type:"insert_in_slot"` | ✅ **Corrected 2026-08-23.** The refusals logged on 2026-07-29 / 08-17 were all `data_element_tool > insert_component_instance`, which has no slot parameter. The component *builder* does. Reordering page-level instances is still the Designer hand. [slots.md](slots.md) |
| **Any grid, or any preset that ships children** (Slider, Tabs, Dropdown, Navbar, Form, Collection List) | **MCP + read the rendered result** | [presets.md](presets.md). The Style panel shows your class only — built-in `w-*` CSS and preset child structure are invisible to `query_styles` |
| **An interactive section** — accordion, tabs, slider, reveal | **Check for an existing IX first, then embed** | Ladder in [componentize.md](componentize.md) → *Interactive behaviour*. Reuse a template component that already animates — via a new **instance**, not `duplicate_component`, which strips IX (verified 2026-08-17); only then reach for an embed. **Never ship static because the canvas looks inert** — house rule #12 |
| **Reproducing a reference design** — "rebuild these sections from that template for this brand" | **Chrome FIRST, then MCP** | [from-template.md](from-template.md). Gate 0: *look at the rendered pages before creating a single style.* Reading tokens is not reading the design |
| **"Does this already animate?"** / learning a template's motion | 🚫 **NOT an MCP question — browser only** | [interactions.md](interactions.md). `data-w-id` is emitted at publish, so it does **not** exist in the Designer and an attribute query returns 0 on pages full of IX. Read the **Interactions panel**; watch it in **Preview ▷** (allowed — rule #4 bans only the *custom-code* preview) |
| **Need the reference's real runtime** — DOM, embed script, scroll behaviour | **Ask the user to publish the REFERENCE** | Reference sites only. Exhaust panel + Preview + MCP first. [interactions.md](interactions.md) §5. 🚫 Never the target site, never publish it yourself |
| **Replace an IX2 interaction with code** | **[ix2-to-code.md](ix2-to-code.md)** | A standing preference — get off IX2 wherever the effect is expressible in CSS/JS. Start at the **capability boundary table**: self-hover and other states are native and free; descendant/sibling hover, `::before`, `@keyframes`, custom properties and compound states are all **`<style>` embed**. Scroll-reveal → IntersectionObserver. Loop → CSS keyframes. Scrubbed multi-element timelines → price it first |
| **Just pasted something in from another project** | **Reconcile before anything else** | [two-hands.md](two-hands.md) → *After the paste*. The ` 2` rename toast is a collision report; variable bindings arrive **flattened to literals**; components arrive **unlinked** |
| Embed code — small or generated | **MCP** `data_element_settings_tool` key `code` | ✅ **New in 2.0**, byte-exact. See [embeds.md](embeds.md) |
| Embed code — large or externally authored | **Clipboard → CodeMirror** | Avoids hand-escaping into a JSON call. See [embeds.md](embeds.md) |
| Assets from a public URL | **MCP** `asset_tool > upload_image_by_url` | ✅ One call; replaces the MD5 + S3 multipart flow |
| Pages, SEO/meta, schema markup, sitemap, branches | **MCP** `data_pages_tool` / `data_sitemap_tool` | Structured page data |
| Reading ground truth | **Both** — Chrome for *live/rendered* truth, MCP `query_*` for *stored* truth | The canvas can lie (embed overrides) |
| **An MCP check that failed, errored or came back empty** | **Switch hands — Chrome, and go look** | House rule #13. A failed MCP check is not a finished check. `🔍 Unchecked` only after *both* hands fail |
| Publishing | 🚫 **Never without the user's explicit unprompted go** | [house-rules.md](house-rules.md) |

**Still Designer-only (verified 2026-07-25):** `clamp()`/`min()`/`max()` and `dvw`/`dvh` values,
descendant selectors, collection deletion, and re-picking a Collection List source after a
cut/paste into a component. See [flowy-manual](../flowy-manual/SKILL.md).

## Every session starts here

0. **Read `~/.claude/flowy.config.md`**: the user's browser, font policy, board and approval mode.
   Missing is normal and not a blocker: fall back to the defaults in [setup.md](setup.md) and carry
   on. Do not create the file unprompted; `/flowy:setup` does that.
1. **Load Chrome tools** in one `ToolSearch` call, batched:
   `select:mcp__claude-in-chrome__tabs_context_mcp,...navigate,...computer,...read_page,...tabs_create_mcp`
2. **`webflow_guide_tool` once**: it is the MCP's own current instructions. Do this before any other Webflow call.
3. **Pin the project**: `data_sites_tool > list_sites` → hold `site name` + `site_id` + `page_id`
   for the session. Never assume an id; never resolve by name alone. Working accounts carry
   hundreds of near-identically-named sites. More than one match → **ask which.** House rule #1a.
4. **Open the Designer in a NEW tab WITH the Bridge, in one navigation** (house rule #1b).
   `tabs_create_mcp` (never a previous session's tab id), fire any `designer_tool` call, take the
   `?app=<token>` link from the error text, `navigate` to it. Tokens are reusable within a session.
   Foreground with the `browser` value from the config (step 0), per house rule #6. It is frequently
   **not** Google Chrome, and the wrong app fails silently.
5. **`data_agent_instructions_tool > search_instructions`** for the site: Webflow now hosts
   site-specific rules and skills. Repeat on every site switch.
6. **Screenshot the area you'll touch**, then work.
7. **If a reference template is involved: Gate 0 before any write.** Open the reference Designer in
   its own tab (it need not be published), screenshot real pages at desktop *and* mobile, and build
   the motion inventory from the Interactions panel. Write the design language down in a
   paragraph and show the user before creating a single style.
   [from-template.md](from-template.md) · [interactions.md](interactions.md)

**The Bridge is only needed for `designer_tool`.** Verified 2026-07-25: with the Designer tab
backgrounded, `designer_tool` timed out while every `data_*` REST call kept succeeding. Keep the
Designer tab foregrounded whenever you use Designer-session tools.

## Two tracks

- **Track N — new build.** Connections → plan → execute → verify → present. No export, no mirror.
- **Track E — already-built site.** The unzipped export is the working folder; `_flowy/` is the
  resume anchor. Full phases, ledger, and mirror in [lifecycle.md](lifecycle.md).

## Red flags — STOP

- About to publish, or about to *offer* to publish → **STOP.** [house-rules.md](house-rules.md).
- About to rebuild a third-party component element-by-element → **paste it instead.**
- About to use an MCP style/element write to make a **visual judgment** → drive the Designer.
- About to resize the window to check mobile → use the device toggles.
- About to click ▷ Preview with custom code to verify an embed → **banned.** [embeds.md](embeds.md).
- About to **simplify or flatten a component because its behaviour doesn't show on the canvas** →
  **STOP.** Embed script never runs on canvas; that is normal. House rule #12.
- About to write **"couldn't verify" / "MCP is down" / `🔍 Unchecked`** on something a human could
  see on screen → **STOP. You are half-done.** Open the Designer with `claude-in-chrome` and look.
  House rule #13.
- About to hand-build an accordion / tabs / slider → **STOP. Check whether a template component
  already has the interaction** and instance it (duplication strips IX). [componentize.md](componentize.md).
- About to `duplicate_component` an animated component and trust the copy → **STOP.** ✅ Verified
  2026-08-17: the duplicate carries structure, styles and props, **not IX2 triggers**. The copy is
  static; read its Interactions panel before relying on it. [componentize.md](componentize.md).
- About to build from a reference template after reading only its **variables and classes** → **STOP.
  You have not seen the design.** Open the reference Designer and screenshot real pages first.
  [from-template.md](from-template.md) Gate 0. Generic-but-correct is the failure signature.
- About to copy a reference's **spacing values** into a project whose type system might **trim to
  cap height** → **STOP and check both sides first.** A gap is the author's spacer plus each line
  box's leading; trimming removes the leading, so verbatim spacing collapses and text collides.
  30-second check and the decision table: [from-template.md](from-template.md) Gate 0b. Lumos v2.1+
  trims by default.
- Concluded "no interactions" from an **MCP `data-w-id` query returning 0** → **that query cannot
  answer this.** Read the Interactions panel. Gate 1.
- Writing `Card 1 title … Card 6 title`, or a component with 20+ props → **STOP. That is a CMS
  collection wearing a costume.** [from-template.md](from-template.md) Gate 2.
- About to write **`grid-template-columns`** → **count the children in the same breath.** A track
  list that outlives the layout it was written for is the commonest silent misalignment: a 4-track
  template on a 2-child row crushes child 1 into the first track. If the count can vary, use
  `grid-auto-flow` + `grid-auto-columns`, not a fixed list. [presets.md](presets.md).
- Blaming a layout bug on **"Webflow's grid defaults"** → **check first.** `w-layout-grid` is only
  emitted when a Grid *preset* exists on the site; an MCP-made `display:grid` DivBlock never carries
  it. Grep the published CSS for `.w-layout-` before theorising. [presets.md](presets.md).
- About to build a marquee by **cloning the track in JavaScript** → **STOP.** Two groups in the DOM,
  animated in CSS. Gate: *Marquees* in [from-template.md](from-template.md).
- About to build **more than one or two components before showing the user** → **STOP.** The first
  component is the design review. [from-template.md](from-template.md) → *Batch size*.
- About to leave a **` 2` class** in the project after a paste → **STOP.** That numeral is Webflow
  telling you the target already owns the concept. Delete it or name it properly.
  [two-hands.md](two-hands.md) → *After the paste*.
- Pasted a section whose component the target **already has** → **STOP. Do not keep the unlinked
  copy.** Delete the loose markup and insert an instance of the existing component, or you now
  maintain two of everything.
- Treating pasted styles as tokenised → **they are not.** Cross-site paste **flattens variable
  bindings to literals**; the section will silently ignore every future token change. Rebind.
- About to reach for **IX2 for a hover** → **STOP.** Hover is CSS. If it only affects the hovered
  element, it is a **native State** (free). If it reaches a descendant or sibling, it is a **`<style>`
  embed**. Never an interaction. Capability boundary: [ix2-to-code.md](ix2-to-code.md).
- Setting the **same property** both natively and in an embed → **STOP.** Embed CSS out-ranks native
  classes on the published page while being invisible on canvas. That silently kills variant
  overrides. Pick one place per property.
- Reaching for MCP "because it's precise" → type the value into the Style panel and watch it land.
- About to edit a style with the canvas widened → **STOP.** The canvas width sets the active
  breakpoint; the edit lands on 1440/1920, not base. [styles-and-classes.md](styles-and-classes.md) §3.
- Just opened a component instance and started styling → **check which variant is selected.**
  `open_component_view` lands on **Base**, not the instance's variant. §4.
- About to click Webflow's "Clean up" / bulk-delete unused styles → **never unprompted.** It is one
  irreversible action across the whole site and it cannot see classes used by embeds, interactions
  or CMS rich text. §5.
- Trusting a write response → **re-read.** `set_settings` and `update_style` both report success on
  writes you must still verify. `set_variant_styles` returns a **thin echo with no properties**:
  `get_variant_styles` is the evidence.
- About to **impose a naming convention on a project that already has one** → **STOP.** That is a
  defect, not a service. [conventions.md](conventions.md) §1.
- About to call **`unregister_component`** → **STOP.** Schema-flagged DANGEROUS; it affects every
  instance site-wide. `unlink_component_instance` is the per-instance tool. Never unprompted,
  and a hook will make you ask. Same for `delete_asset`, `compress_assets` (replaces the
  original bytes in place) and `create_asset_folder` (folders cannot be deleted, ever).
- `transform_element_to_component` returned **"Target element is invalid."** → **check the subtree
  for component instances before debugging the element id.** The error string is identical for both.
- About to create a components/style-guide page → **check whether one already exists first.**
  Adopt-first applies to page structure, not just class names.
- About to **double-click a component in the Components panel to "open" it** → 🚫 **that INSERTS an
  instance onto the current page.** Verified 2026-07-30 (undone with `cmd+z`). Use `open_canvas`, or
  open an existing instance's component view.
- About to un-CMS a Collection List → **snapshot the bindings and item content first**
  (`all_raw_settings`). Removing the wrapper is not undoable.

## Reference map

| Open | For |
|---|---|
| [house-rules.md](house-rules.md) | **The hard standing rules.** Read first |
| [setup.md](setup.md) | **Where the user's config lives** (`~/.claude/flowy.config.md`), its four settings and their defaults. Read at session start; house rules #6, #7, #9 depend on it |
| [from-template.md](from-template.md) | **Reproducing a reference design as client components.** Gate 0 (look before you build), Gate 1 (the Interactions panel is the only IX authority), Gate 2 (CMS vs props vs slots), marquees, batch size, brand intake |
| [presets.md](presets.md) | **What a Webflow element brings with it.** The three style layers (`query_styles` sees only yours), which `w-*` base classes ship always vs. only-when-used, the Grid 2×2 default, presets that carry child elements, and the track-count-vs-child-count rule |
| [interactions.md](interactions.md) | **IX2 on a reference template.** How to read the Interactions panel, the motion inventory, the reuse ladder (duplicate → rebuild in IX2 → embed → static), when to ask the user to publish the reference, and how to make it award-level rather than merely faithful |
| [ix2-to-code.md](ix2-to-code.md) | **Translating IX2 into CSS/JS embeds.** The decision rule (what to translate, what to leave), a per-trigger translation table (hover, click, scroll-into-view, stagger, page load, mouse-move parallax, loops), and the non-negotiables — reduced motion, transform/opacity only, idempotency, scoping, specificity |
| [conventions.md](conventions.md) | **How this project is already built.** Adopt-vs-impose, the mess test, profile derivation, fingerprint scoring, cross-convention collisions. Profiles in [conventions/](conventions/) |
| [classify.md](classify.md) | Reading a site: section/atom/slot detection, the **three** Section›Container check modes, the candidate ledger, Gate 1 |
| [componentize.md](componentize.md) | Composite vs raw componentization, the transform rejection, prop derivation, the client-usability contract, derived prop types, the interactive-behaviour ladder |
| [slots.md](slots.md) | Slots — components inside components. When a slot beats a prop, deriving the slot prop, the instance-anchor ceiling, filling a slot |
| [cms-to-static.md](cms-to-static.md) | The inverse of `static-to-cms.md` — the ships-fixed decision rule, the snapshot guardrail, reverse index alignment |
| [rebrand.md](rebrand.md) | Token/asset swap, the required brand input, class-rename scope and the site-wide usage read |
| [styles-and-classes.md](styles-and-classes.md) | Style writes by hand, the canvas-width breakpoint trap, variant overrides, unused-class purge, unifying legacy class systems |
| [two-hands.md](two-hands.md) | Paste-first rule, the MCP-first anti-pattern, rationalization table |
| [static-to-cms.md](static-to-cms.md) | **One-list-per-parallel-group rule**, field/element/key mapping, verified conversion sequence |
| [embeds.md](embeds.md) | Which embed route, the CM6 procedure, verification |
| [lifecycle.md](lifecycle.md) | Track E phases, the write ledger, surfaces |
| [local-mirror.md](local-mirror.md) | Export anatomy, identity keys, hand-edit rules |
| [css-ladder.md](css-ladder.md) | JS embed placement tree, CSS fallback ladder |
| [flowy-manual](../flowy-manual/SKILL.md) | Verified behaviours, traps, MCP 2.0 changes |
| [flowy-verify](../flowy-verify/SKILL.md) | Post-write check routine |
