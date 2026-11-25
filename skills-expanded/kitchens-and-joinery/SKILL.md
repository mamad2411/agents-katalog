---
name: kitchens-and-joinery
description: Design kitchens, wardrobes and custom joinery in 3D New Era AI — cabinet runs sized to the wall, appliances embedded, slatted panels, countertops — and produce the cut list. Use for kitchens, closets, built-ins and anything a joiner will build.
---

# Kitchens and joinery

1. **Fill a wall.** `cabinet_run` with `wall=<id>` measures the free stretches between
   corners, doors, windows, fridge and stove and splits them into even modules
   (`dry=true` shows the plan without drawing). `p.sink` and `p.cooktop` place those
   cabinets and their cutouts.
2. **Appliances.** `embed` sets a sink bowl or cooktop into a countertop with an exact
   cutout, or an oven or microwave into a cabinet niche; the item then moves with it.
3. **One-off pieces.** `joinery` builds cabinets, slatted panels, countertops, plaster
   coves and sofas from parameters; workshop rules come back as notes and never refuse to
   draw. Change a build later with its `id` and only the new values.
4. **Check.** `layout` finds cabinets whose doors open against a wall and appliances
   a resized niche no longer holds; `ergonomics` checks counter heights and the work
   triangle.
5. **Cut list.** `cut_list` reads boards, edge banding and hardware; `export` with `what=cut_list`
   writes it as `.csv`, or `.dxf`/`.svg` sheets for the workshop.
