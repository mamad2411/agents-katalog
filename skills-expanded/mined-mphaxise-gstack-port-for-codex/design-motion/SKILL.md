---
name: design-motion
description: Create and verify a looping motion study from an approved interface frame. Use for showcase loops, animated product stills and design-motion exports.
---

# Design motion

Start with the approved still, target dimensions, and one interaction to show.
Use the source design or running view to match type, imagery, layout, and
clipping. Check a render at the target size before adding motion.

1. Pick the elements that move and define the resting frame, transition, hold,
   and return. Keep the background fixed. Content must be readable with motion
   disabled and before scripts run.
2. Drive capture from a deterministic clock. Save the reference still and a
   contact sheet with the opening, peak, resting and loop-boundary frames.
3. Compare the first frame with the frame one cycle later. Check the empty
   interval for drift, the resting frame against the reference, and the pixels
   outside the moving region for overflow. Inspect the contact sheet for pops.
4. Export the requested format after those checks pass or the user accepts a
   named exception. Report actual dimensions, duration, frame rate, and files.
   If capture or encoding is unavailable, deliver the verified still or source
   and name the missing step.

[Upstream workflow and capture contract](https://github.com/garrytan/gstack/tree/76535826f5d50c721f95820f300037a3efe833a9/design-motion)
