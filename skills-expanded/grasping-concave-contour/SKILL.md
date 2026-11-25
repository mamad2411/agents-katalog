---
name: grasping-concave-contour
description: >-
  Grasp an awkward rigid part by the waists in its own silhouette — take the
  alpha shape of its point cloud from above, find where that boundary turns
  inward, and close the jaws across a pair of those inward runs. Use when a part
  has no graspable long axis and no pair of parallel walls an OBB would find —
  pliers and scissors gripped at the joint, a spool at its neck, a gear between
  two teeth, a bulb socket at its skirt. Use grasping-linear-feature instead for
  handles, rods and shafts, and grasping-short-axis when an upright box is
  enough.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: grasping, tags: [grasping, manipulation, point-cloud, alpha-shape, concavity, top-down, cpu]}
gap:
  requires: {connector: [robot.describe_gripper]}
  allowed_tools:
    - geometry.fit_linear_feature
    - robot.describe_gripper
    - robot.go_home
    - robot.go_to_pose
    - robot.get_observation
    - robot.open_gripper
  required_inputs:
    target_obb: OrientedBoundingBox
    target_cloud: PointCloud
  produces_outputs:
    grasp_pose: Se3Pose
    pregrasp_pose: Se3Pose
    grip_width: float
    confidence: float
  exit_conditions:
    posed: The wrist reached the computed pose with the jaws open, ready for the close a verifying skill will make.
    failed: No pair of concave runs fits the jaw span, or the pose could not be reached.
  hard_rules:
    - >
      The silhouette is the alpha shape, not the convex hull. A hull has no
      concavities by construction, so every waist this skill grasps by is
      exactly what a hull erases; measuring deviation FROM a hull is an
      indirect proxy for the thing the alpha shape states directly. Pass the
      segmented cloud and let `alpha_radius` (default 15 mm) set how fine a
      notch survives.
    - >
      Pair the runs, do not grasp one. A single inward run says where a pad can
      sit; a parallel jaw needs two, and the secant between their centroids is
      both the closing direction and the width to command. Candidates whose
      secant does not fit `robot.describe_gripper`'s span are not candidates,
      which is why this skill reads the gripper rather than assuming one.
    - >
      Descend to a floor, not to the cloud. A top-down view of a part lying in
      a bin sees its upper surface, so the cloud's own z is the top of the
      object and closing there grips air above a short part or drives through a
      tall one. Pass `bin_floor_z` and the grasp is placed `grasp_z_offset`
      above the floor the part rests on; without it the script falls back to the
      cloud's centre and says so.
    - >
      Approach straight down and turn only in plane. The pose this skill builds
      commands a wrist roll, so the arm must be on an IK backend that solves the
      roll rather than leaving it free — a free wrist discards the direction the
      jaws were told to close along and closes across whatever heading it chose.
  canonical_scripts:
    - compute_concave_grasp: scripts/contour_concave_grasp.py
  streaming: false
---

# Grasping by the concavities in a silhouette

A parallel jaw wants two opposing surfaces. For a handle or a rod, the pair is
implied by the long axis and `grasping-linear-feature` finds it. For a part with
no long axis — a pair of pliers, a spur gear, a wire spool, a bulb socket — the
opposing surfaces are the *waists*: the places where the outline turns inward.
This skill finds them directly.

## What the script does

1. Projects the segmented cloud to the (x, y) plane the part is seen from.
2. Builds the **alpha shape** of that projection — a Delaunay triangulation
   filtered to triangles whose circumradius is under `alpha_radius`, whose
   boundary is the part's real outline rather than its hull.
3. Walks that boundary and keeps the **reflex vertices**, where it turns inward.
   Consecutive reflex vertices are one run; each run's centroid is one candidate
   pad site.
4. Pairs the candidates, keeps the pairs whose secant fits the gripper's span,
   and builds a straight-down pose centred on each pair's midpoint with the jaws
   closing along the secant.
5. Ranks by confidence and returns the best, with the rest in `candidates` so a
   caller that fails one can try the next without recomputing.

## Where it fits

It is a *proposer that also poses*: it returns `grasp_pose` and `pregrasp_pose`
directly rather than handing a list to a selector. Put `verifying-grasps` after
it — this skill exits `posed` with the hand open and does not close it — and
route `failed` to whatever recovery the graph has, because a part whose
silhouette has no fitting pair of waists is one this skill genuinely cannot take.

A sensible arrangement is to try `grasping-linear-feature` first and fall through
to this on `failed`: most parts have an axis, and the ones that do not are
exactly the ones this skill is for.
