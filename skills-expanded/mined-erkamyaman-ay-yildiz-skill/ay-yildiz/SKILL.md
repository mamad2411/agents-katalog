---
name: ay-yildiz
description: Draw the Turkish flag (Türk bayrağı) or its crescent and star (ay yıldız) from a vector computed from the Turkish Flag Law's table, instead of from memory. Trigger whenever an SVG, icon, logo, badge, favicon, illustration, CSS or canvas drawing, or animation contains the flag of Turkey or its crescent and star, or when asked to fix, check or animate one.
license: MIT
metadata:
  author: erkamyaman
  version: '1.1'
---

# Turkish flag

Models drawing the crescent and star from memory get it almost right: the inner circle is shifted, the star is too big or turned, the red changes every time. Almost right is wrong for a national flag. Never draw these shapes by hand. Copy the vector below and only scale or move it as one piece.

## The vector

Coordinates are in units where the flag's width (hoist height) G = 60000. The flag spans x 0 to 90000 and y -30000 to 30000, so its centre line is y = 0.

```svg
<!-- crescent -->
<path d="M42675 8021a15000 15000 0 1 1 0-16042 12000 12000 0 1 0 0 16042z"/>
<!-- star -->
<path d="M41750 0l13568-4408-8386 11541V-7133l8386 11541z"/>
```

Full flag: [assets/flag-of-turkey.svg](assets/flag-of-turkey.svg). It leaves out the white hem, for screen use. Crescent and star only, tightly cropped, white on transparent, so place it on red: [assets/crescent-and-star.svg](assets/crescent-and-star.svg).

Colours on screen: red `#DC0D15`, white `#FFFFFF`. This red is a convention, not the flag's legal colour. I found no government source that defines a screen colour for the flag. `#DC0D15` is the main red in the [Interior Ministry's current identity guide](https://www.icisleri.gov.tr/kurumsal-kimlik-kilavuz), and the ministry says its logo uses flag red. The legal red is a set of cloth coordinates in the regulation; see [references/construction.md](references/construction.md#colour).

These paths are computed from the official construction table attached to Law No. 2893 (Türk Bayrağı Kanunu, 1983), reproduced in [references/construction.md](references/construction.md). A Turkish and English diagram is in [references/construction-sheet.svg](references/construction-sheet.svg), and every value is in [references/construction.json](references/construction.json) for tools. Check any change against the table. The star's position follows E = G/3, which is a judgement: the official texts have a small conflict, explained in the construction notes.

## Putting it somewhere else

To place the crescent and star on a shield, badge, button or icon, wrap both paths in one group and use one transform:

```svg
<g fill="#fff" transform="translate(CX CY) scale(S) translate(-35159 0)">
  <path d="M42675 8021a15000 15000 0 1 1 0-16042 12000 12000 0 1 0 0 16042z"/>
  <path d="M41750 0l13568-4408-8386 11541V-7133l8386 11541z"/>
</g>
```

- `35159 0` is the centre of the emblem's bounding box (x 15000 to 55318, y -15000 to 15000), so `CX CY` is where its centre lands.
- `S = targetWidth / 40318`. Example: 300 px wide means `S = 0.00744`.
- Use the same scale on both axes. Never stretch.
- This template centres the emblem on a point. Don't use it to place the emblem on a whole flag; use the flag asset, where the emblem isn't centred.
- Keep it at least 24 px wide. At 12 px the star turns into a blob and the crescent's tips disappear.

## Rules

1. Copy the path data exactly. Don't round, simplify, re-type or redraw it, and don't rebuild it from `<circle>` elements and a star polygon unless you check every number against the construction sheet.
2. Move, scale and rotate the crescent and star together, never one alone. Their positions come from the law's table. An animation may move them, as long as it ends with both in place.
3. The star has one point aimed straight at the crescent (pointing to the hoist). Don't turn it.
4. The crescent opens toward the fly (away from the pole). If the design is mirrored for a right-to-left layout, still don't mirror the flag.
5. Fill only. No `stroke` on the white shapes: a stroke, especially with `stroke-linejoin="round"`, rounds the star's tips and fattens the crescent.
6. Keep the default `fill-rule` (nonzero). The star path crosses itself, and `fill-rule="evenodd"` punches a pentagon hole in its middle.
7. Use `#DC0D15` on screens. Not `red`, `#FF0000` or another brand's red. Use the regulation's coordinates for cloth.
8. A whole flag is 3:2 (length 1.5 G). Don't crop or stretch it to fit a square. Put it in a 3:2 box or use the crescent and star alone.

## Animating it

- The final frame has to be the exact static vector, with no leftover stroke, dash, scale or rotation.
- Reveal shapes with a mask (a sweep, a wipe, a growing circle) instead of drawing outlines with `stroke-dashoffset`. Outline drawing leaves a seam where the dash ends.
- To animate the star, scale or rotate it around its own centre `(49250, 0)` and end at scale 1, rotation 0.
- Leave room for any overshoot: the example's star grows about 15% mid-animation, so a tightly cropped viewBox clips it.
- Give each copy of the example its own mask `id`. Two copies with the same id can break the sweep.
- Respect `prefers-reduced-motion` by showing the static vector. SVG animation can't do this alone, so check it in code and pick which version to render.
- Renderers without SMIL support won't show this correctly, so use the static vector there too.

Example: crescent sweeps in, then the star spins into place, ending on the exact shape:

```svg
<defs>
  <mask id="sweep" maskUnits="userSpaceOnUse" x="14000" y="-16000" width="32000" height="32000">
    <circle cx="30000" cy="0" r="7600" fill="none" stroke="#fff" stroke-width="15200"
      pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">
      <animate attributeName="stroke-dashoffset" values="1;0" dur="0.9s" fill="freeze"/>
    </circle>
  </mask>
</defs>
<g fill="#fff" transform="translate(CX CY) scale(S) translate(-35159 0)">
  <path mask="url(#sweep)" d="M42675 8021a15000 15000 0 1 1 0-16042 12000 12000 0 1 0 0 16042z">
    <set attributeName="mask" to="none" begin="0.9s" fill="freeze"/>
  </path>
  <g transform="translate(49250 0)">
    <g transform="scale(0)">
      <animateTransform attributeName="transform" type="scale" values="0;1.15;1" keyTimes="0;0.7;1" begin="0.7s" dur="0.6s" fill="freeze"/>
      <g>
        <animateTransform attributeName="transform" type="rotate" values="-144;0" begin="0.7s" dur="0.6s" fill="freeze"/>
        <path transform="translate(-49250 0)" d="M41750 0l13568-4408-8386 11541V-7133l8386 11541z"/>
      </g>
    </g>
  </g>
</g>
```

The mask circle is stroked, but it is inside the mask, so no stroke shows on the crescent. The `<set>` removes the mask when the sweep ends, because a mask left in place softens the crescent's edges.

## Checking a drawing

Before you finish, compare against the vector:

- Both path `d` strings are byte-for-byte the ones above (or the shapes come from the asset files).
- At most one uniform `scale` on the shared group, no `skew`, no non-uniform scale.
- No `stroke` and no `fill-rule="evenodd"` on the white shapes.
- Red is `#DC0D15` (upper or lower case).
- Render it on red and look: the star's left tip points into the crescent's opening, and the tips are sharp.
