---
name: porting-gotchas
description: Read before writing markup for a section ported from WordPress. Covers the layout failures that pass a height check, silent CSS failures, per-builder quirks, and the rules for measuring correctly. Use when porting a WordPress or page-builder site to any stack, when a diff shows a delta you cannot explain, or when a ported section looks right but measures wrong.
---

# Porting gotchas

Every item here cost real hours on a real port. Read them before writing markup, not after discovering one.

## The rule everything else serves

**Never claim a page is done without a numeric comparison, and always compare position as well as height.**

Most of the bugs below pass a height check.

---

## Layout failures that pass a height check

### Margin collapse moves whole sections

A negative top margin on an inner div collapses out of its section and takes the **section's background** with it. The section's own height is unchanged, so height comparison sees nothing. Only position catches it.

Symptom: `Δtop` on one section and every section after it, with no `Δh` anywhere.

Fix: `flow-root` on the containing element. That establishes a block formatting context and stops the margin escaping.

### Padding on a fixed-width box shrinks the content

`w-[287px] pl-[15px]` gives a 272px content box. Text rewraps, height changes, and nothing in the class list says so.

Fix: put the gap on the sibling. `mr-[15px]` on the icon, not `pl-[15px]` on the container.

### Inline-block descenders

A `<textarea>` or `<img>` without `display: block` sits on the text baseline and adds roughly 7px of descender space below it. Enough to fail a comparison, invisible by eye.

Fix: `block` on the element.

### Negative margins differ per page

The same component can wrap in a 558px row on one page and a 570px row on another, because the builder applied different negative margins per instance.

Do not chase this with a magic clip value. Make the row height a prop and write down why it differs.

---

## Silent CSS failures

### A missing type token emits nothing

`text-28` used in three places, `--text-28` never defined. Tailwind emits no rule. The element inherits its parent's size, and if it is absolutely positioned the section height stays correct.

On the port this came from, every team member's name on four pages rendered at half size for hours, through a full geometry pass.

Run `/wp-audit` before trusting any measurement.

### Interpolated class names produce no CSS

Tailwind's scanner reads source text. `pl-[{{ $x }}px]` and `` className={`pl-[${x}px]`} `` are not class names at build time, they are strings the scanner cannot resolve.

Fix: for genuinely dynamic values, use an inline `style`. For a fixed set, write the full class strings out.

### `leading-normal` is about 1.5em and the design usually wants less

A 20px title with `leading-normal` renders at 30px. The builder's is 24px. On one port this was 17px wrong on one section and 30px on another.

**Always take line-height from the measurement.** A `lineHeight: "normal"` in a dump is a value you have not resolved yet, not a value you can keep.

---

## Measuring correctly

These are handled by the plugin's browser layer. They matter when you measure by hand or wonder why two runs disagree.

- **Entrance animations shift rects.** Builders start elements at `opacity: 0` with a transform, and `getBoundingClientRect()` reads the post-transform box. Kill all animation and force the holding classes visible before reading anything.
- **Fonts landing late shift every text height.** `await document.fonts.ready` first. The symptoms look exactly like a missing type token, so rule this out before hunting for one.
- **`content-visibility: auto` and lazy sections report height 0** until they have been near the viewport. Scroll the whole page, return to the top, then measure.
- **`img.decode()` never settles for an image whose source never resolves.** Await on a budget, and treat unsettled images as a warning that the page may still reflow.
- **Scrollbars change the effective viewport.** A 1440 viewport is a 1425 layout where scrollbars take space. Two dumps at different `clientWidth` are not comparable, full stop.
- **Background video is not a styling bug.** Two frames of the same 38-second loop look like different designs. Pin `currentTime` on both sides before comparing anything visual.

---

## Builder-specific

### Elementor

- Paragraphs carry a hidden ~14.4px bottom margin **on top of** the widget's own margin. A text block measuring 62px around a 48px paragraph is not missing padding, it already has it.
- CSS is scoped per post ID: `.elementor-42 .elementor-element-a1b2c3`. Renaming or restructuring a wrapper stops the rules matching. This is why keeping the original CSS and componentising are close to mutually exclusive.
- The page root is `.elementor-<postid>`, and a page has several: header, footer and content each get their own. Find the content one with `grep -oE 'elementor-[0-9]+'` on the mirrored page and check which has the most sections.
- Boxed container width comes from `--container-max-width` in the site's global CSS, not from anything on the section.
- Breakpoints default to 767/768 and 1024/1025 but are editable. Read the real values from the source CSS.

### Divi

- Sections are `.et_pb_section` inside `#et-boc .et_builder_inner_content`.
- Per-post CSS lives in `et-core-unified-*.css` under uploads.
- Divi's own row gutters are percentage-based and change with container width. Measure at every breakpoint.

### Gutenberg and block themes

The easy case. `theme.json` is already a design token file: palette, type scale and spacing scale are all in it. Read it directly instead of sampling computed styles.

### Bricks, Beaver Builder, Oxygen, WPBakery

Section roots are `.brxe-section`, `.fl-row`, `.ct-section` and `.vc_row`. WPBakery is the awkward one: it emits inline `<style>` blocks per shortcode with generated IDs, so a token census picks up a lot of noise.

---

## Writing the markup

- **Use measured numbers as arbitrary values.** `mb-[11px]`, `h-[56px]`. Do not round to the framework's spacing scale. You will spend longer chasing the 2px than you saved.
- **Props are flat and string-keyed.** That is the shape a CMS repeater hands back, so wiring the CMS later is passing data through rather than reshaping it.
- **Variation between pages is a prop, not a copy.** Padding, container width, row height. Pass literal class strings, never interpolate.
- **Extract a component when a block appears on a second page**, not before. On the source project, reuse ran: services 1 new section of 5, events 1 of 7, about-us 2 of 8, team 0 of 4.

## Working order per section

1. `/wp-measure <page> --mode sections` to see the shape of the page.
2. `/wp-measure <page> --mode tree` for the one section you are about to write, then query the file rather than reading it whole.
3. Write the section using the measured values.
4. `/wp-diff <page>`.
5. Repeat. Two to four rounds per page is normal.
