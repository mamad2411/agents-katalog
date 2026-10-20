---
description: Grade a rendered ad's visual design against the rubric and fix what's weak
argument-hint: [ad slug, optionally "review only" to skip the fixes]
---

Run a design pass. Target: **$ARGUMENTS** — if empty, use the ad this
conversation has been working on, or the only folder in `ads/`.

Invoke the **`critique-ad`** skill and follow it. It owns the rubric, the
thumbnail test, and where each class of fix belongs; don't restate any of that
here.

Two things this command settles before the skill starts:

**The input is pixels, never source.** Render first, or grab frames for motion.
If you haven't looked at the image, you haven't reviewed the ad.

**Scope.** This grades and fixes *design* — layout, hierarchy, type, colour,
space, thumbnail legibility. It does not rewrite the offer, the angle, or the
CTA target; flag those and let the user decide. Copy is fair game only where
length is a layout problem, and cutting words always beats shrinking type.

If the argument says "review only", score and report without editing.

Distinct from `/verify`, which asks whether the ad rendered *correctly*. This one
asks whether it's any *good*. An ad can pass `/verify` completely and still fail
here at thumbnail size.
