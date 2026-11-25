---
name: perceiving-sorting-pairs
description: Discovers a labelled four-compartment destination from RGB-D and repeatedly perceives one remaining source object with its matching metric destination region, using an identity table the graph supplies for what each label looks like and what its graspable part is called. Use when a workflow must sort several visible objects into compartments identified by printed category labels.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: perception, tags: [sorting, labels, compartments, loop]}
gap:
  allowed_tools: [robot.get_observation, grounding-dino.detect, sam3.segment_box, geometry.mask_to_world_points, geometry.filter_and_compute_obb, vlm.query]
  required_inputs: {instruction: string, layout_description: string, source_description: string}
  produces_outputs:
    target_obb: OrientedBoundingBox
    target_mask: Mask
    target_cloud: PointCloud
    destination_obb: OrientedBoundingBox
    layout_json: string
  exit_conditions:
    found: An object and matching region were selected.
    ambiguous: Identity or association needs another view.
    finished: No unsorted object remains.
  canonical_scripts:
    - discover_regions: scripts/discover_regions.py
    - select_pair: scripts/select_pair.py
  streaming: false
---

# perceiving-sorting-pairs

A loop-head perception skill for sorting into a visible labelled 2x2 container.
`discover_regions` runs once: it reads the four printed labels and reconstructs
each compartment floor from calibrated depth. `select_pair` runs on every loop:
it observes only the described source region, selects one remaining object,
matches its type to one of the perceived labels, segments its graspable part,
and returns its OBB/mask/cloud together with the matching destination OBB. No
object-to-region table or simulator goal state is used.

## The identity table comes from the graph

The script knows no object. The graph supplies, as literals on the `select`
node:

- `identity_hints` -- the visual identities of the labels in play and the
  TARGET phrase to answer for each (for example "HAMMER is the cyan T-shaped
  tool and TARGET must be 'blue hammer handle'; ..."). When empty the prompt
  asks generically for the narrow graspable handle or body.
- `canonical_targets` -- a JSON object mapping a label to the exact TARGET
  phrase; a reply whose TARGET differs for a listed label is rejected.
  Labels absent from the table accept any TARGET.
- `allowed_labels` -- a comma-separated or JSON list restricting the layout
  to a subset of its labels, for instructions that sort only some categories.

Already-attempted labels are excluded through `exclude_label_1..3`;
`finished` is returned when none remain or the model replies DONE.

The reply parser accepts semicolon or newline separators, a missing PIXEL
(the box centre stands in), and coordinates given in crop pixels, 0-1000
normalised units, or full-frame pixels -- the first reading that fits the
crop wins. Masks under 100 px are rejected as fragments.

The two fixed-camera views are sufficient for layout and object perception.
An eye-in-hand camera may improve a downstream grasp skill, but is not required
by this skill and is never used to infer the sorting association.
