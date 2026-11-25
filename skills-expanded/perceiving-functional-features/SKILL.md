---
name: perceiving-functional-features
description: Locates a language-described functional part of a rigid object or fixture from calibrated RGB-D and fits a typed loop, shaft, tip, aperture, surface, or region feature with a metric centre, axis, and radius, either inside an already-segmented parent or end to end from a described object, protruding shaft, directed tip, or lidded aperture. Use when a manipulation step depends on where a specific part is rather than on the whole object, such as a tool loop to hang, a shaft to hang it on, an insertion tip, or an opening to insert into.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: perception, tags: [perception, affordance, geometry, rgb-d]}
gap:
  allowed_tools:
    - sam3.segment_text
    - sam3.segment_box
    - grounding-dino.detect
    - geometry.mask_to_world_points
    - geometry.filter_and_compute_obb
    - geometry.fit_planar_feature
    - geometry.fit_linear_feature
  exit_conditions:
    found: One geometrically valid feature was fitted and its centre, axis, and radius are bound.
    not_found: No described object or feature passed the segmentation and geometry gates (raised by every script, or returned as `route` by `perceive_protruding_shaft` when `required` is false).
  canonical_scripts:
    - perceive_feature: scripts/perceive_feature.py
    - perceive_object_feature: scripts/perceive_object_feature.py
    - perceive_protruding_shaft: scripts/perceive_protruding_shaft.py
    - perceive_directed_tip: scripts/perceive_directed_tip.py
    - perceive_aperture: scripts/perceive_aperture.py
    - perceive_fixture_feature: scripts/perceive_fixture_feature.py
  streaming: false
---

# perceiving-functional-features

Use when manipulation depends on a loop, shaft, tip, aperture, surface, or
region rather than on a whole object. Every script localizes geometry from a
calibrated RGB-D camera and returns a `FunctionalFeature` (`kind`, `pose`
whose local Z is the feature axis, `axis`, `confidence`, and the radius or
length the mating skill needs). None of them computes mating poses or moves
the robot.

Four of the scripts take an `Observation` and pick one camera by name
(`camera_name`, default `overhead`). `perceive_feature` instead takes
`cameras` -- the `Observation`'s `cameras` list -- because it searches
every view; the type registry names no bare list of frames, so the shape is
stated here rather than under `required_inputs`.

## Which script

- `perceive_feature` -- the part of an **already segmented** parent. Inputs
  `parent_cloud`, `parent_mask`, `feature_description`, `feature_type`
  (loop, aperture, surface, region, shaft, tip). Candidates outside the
  parent's 3D bounds are rejected. Outputs `feature`, `feature_mask`,
  `feature_cloud`.
- `perceive_object_feature` -- **object and its planar feature end to
  end**. `candidates` is a JSON list of rows `{kind, object_description,
  feature_description, feature_type, feature_score_min}`; each object
  description is segmented, the strongest wins, its cloud is optionally
  completed down to the support surface (`complete_to_support`), and the
  row's feature (when described) is segmented, centred, and fitted as a
  planar loop with the camera position fixing the normal sign. When
  `instruction` names one of the candidate kinds only those rows are tried.
  Outputs `target_kind`, `target_obb`, `target_mask`, `target_cloud`,
  `feature_center`, `feature_pose`, `functional_feature`. A row whose
  `feature_description` is empty yields the OBB centre as a point feature
  for a downstream landmark rule to refine; object-specific landmark rules
  belong to the graph, not to this script.
- `perceive_protruding_shaft` -- a **thin shaft protruding from a mounting
  plane** (a hook, peg, or pin). Detector boxes for `fixture_description`
  are gated by `label_keyword` and `aspect_min`, refined by SAM3, then the
  full protrusion is recovered from depth inside the box with the mounting
  plane as the far-X plane of the ROI (the shaft protrudes toward
  decreasing world X). `shaft_length_min/max` and `transverse_max` reject
  look-alikes. Outputs `fixture_obb/mask/cloud`, `shaft_tip`,
  `fixture_axis` (plane to tip), and `fixture_feature` with `radius_outer`,
  `usable_length`, and `seating_margin`. With `required: false` a miss
  returns `route: not_found` and empty outputs instead of raising.
- `perceive_directed_tip` -- an **elongated object's insertion tip**. The
  long axis is directed by a visible marker at one end
  (`direction_marker_description`, optional) or by the narrower end; the tip
  is the cloud's extreme along that axis. Outputs `target_obb/mask/cloud`,
  `insertion_pose` (local Z through the tip), `marker_center`, and a `tip`
  `functional_feature` with `radius_outer`.
- `perceive_aperture` -- an **opening in a lid**. The lid plane is fitted
  from the fixture cloud; the aperture centre and radius come from
  intersecting calibrated rays through the opening's 2D mask with that plane,
  since depth inside a hole is the interior, not the rim. Outputs
  `aperture_center`, `fixture_axis` (inward), `aperture_radius`, `rim_z`,
  the two masks and clouds, and an `aperture` `fixture_feature` with
  `radius_inner`.

## Boundaries

- Descriptions and score floors are inputs; no object class, CAD landmark,
  or world coordinate is assumed. Object-specific refinements (CAD offsets,
  a handle-to-tip axis, the mating relation) are graph glue downstream.
- A script raises on a failed gate; the graph routes that to `not_found`.
  Only `perceive_protruding_shaft(required=false)` returns the route.
- This skill localizes geometry. Registration, mating poses, and motion are
  other skills.
