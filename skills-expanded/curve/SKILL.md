---
name: curve
description: Ordered centrelines of deformable linear objects — skeletonises a
  cable, rope or hose mask, recovers one traversal order through occlusion
  breaks and self-crossings (TrackDLO's chain merge), back-projects the ordered
  pixels through depth onto the object's axis as an arc-length-parameterised
  polyline, and carries a known centreline onto the next frame with motion
  imputed for hidden stretches. Use when a workflow needs an ordered centreline
  of a cable, rope or hose from a mask and a depth frame, or must carry one
  through occlusion between frames.
license: Apache-2.0
compatibility: requires gap>=0.1
metadata: {category: perception, tags: [perception, deformable, cable, tracking, cpu]}
gap:
  requires: {}
  serving:
    command: ["python", "-m", "gap_core.rpc.server", "--bundle", "curve"]
    protocol: stdio-msgpack
  tools:
    - curve.fit_centerline: Fit an ordered, arc-length-parameterised 3D centreline to a deformable linear object from its mask and a depth frame.
    - curve.track_centerline: Advance a known centreline onto a new frame, imputing motion for occluded stretches from their visible neighbours.
---

# curve

A mask and a depth frame in, an ordered centreline out. Fully CPU — no model
weights, no GPU.

## What it computes

`geometry.fit_linear_feature` reduces a cloud to its principal axis, which is
right for a rod lying straight and wrong for one that has been bent or woven:
the principal axis of a curve through four posts is a chord that passes
through none of the places a hand needs to go. What replaces it is an
**ordered polyline parameterised by arc length** on `s in [0, 1]`, the same
coordinate an asset that declares features at `s = 0, 0.5, 1` (`end_a`,
`midpoint`, `end_b`) publishes — so per-node error is scorable against a
declared feature rather than only against task reward.

Both tools return a `Centerline` (`gap_core.types`): `points` as a plain
`[[x, y, z], ...]` list in world metres, in order along the object;
`arclength_m`; `radius_m` (mean radius, mask area over length); `nodes`;
`ordered`. The tracker adds `visibility` (per node, 0..1) and `tracked: true`.

- **`curve.fit_centerline(mask, depth, intrinsics, camera_pose, nodes=40,
  smooth=2.0)`** — the mask (any nonzero = object, `[H, W]`) is upscaled and
  skeletonised; TrackDLO's chain merge prunes the fragments and solves an
  endpoint-to-endpoint assignment with a Euclidean-plus-curvature cost, which
  is what recovers one traversal order through occlusion breaks and
  self-crossings. The ordered chain (not the whole mask — the medial axis
  samples the object's own surface, where silhouette pixels straddle the
  background and read metres away) is back-projected through `depth`
  (`[H, W]`, metres) and the 3x3 `intrinsics`, a smoothing spline is fitted
  in arc length and resampled to `nodes` points, and the curve is pushed from
  the object's surface onto its axis (below). `camera_pose` is camera-to-world
  as an `Se3Pose` or a 4x4 matrix.
- **`curve.track_centerline(prior, mask, depth, intrinsics, camera_pose)`** —
  `prior` is the `points` of an earlier fit or track (a whole `Centerline`
  dict is unwrapped). A cold fit sees only what is visible now, so a gripper
  covering half the rod produces half a rod. The tracker instead moves the
  known nodes: each takes a Gaussian-weighted correspondence to the new cloud,
  the displacement field is smoothed *along the rod* (arc-length kernel, not
  spatial — two points a fold has brought together are not neighbours) so a
  node with no observation moves with the stretch either side of it, a bending
  prior keeps unobserved nodes from folding, and after every iteration the
  nodes are re-spaced to the length they had, because a cable does not
  stretch. Faithful in structure to TrackDLO (Xiang et al., RA-L 2023), not in
  numerics: a fixed number of damped correspondence steps rather than the
  paper's CPD-style EM. Route on `visibility` when deciding whether the rod
  is still known.

## The constants, and why

- **`DEFAULT_NODES = 40`** — TrackDLO's own default region: a 500 mm rod is
  described every ~12 mm, few enough that the tracker stays real-time. Pass
  the rod's own segment count to get its discretisation.
- **`UPSCALE = 4`** — TrackDLO's preprocessing divides by 10 and mode-filters
  with a 15-pixel window, tuned for a rope ~40 px across in 1280x720. A
  640x480 frame with a rod ~6 px across is erased by that outright (measured:
  the chain came back empty, the principal-axis fallback silently returned all
  1651 mask pixels, and the width estimate read 0.6 px instead of 5.6).
  Upscaling four times with no further downscale puts the rod at ~24 px, the
  regime the mode filter expects; the chain is divided back down before use.
- **`SMOOTH = 2.0`** — `splprep` smoothing as a multiple of the point count.
  Zero would interpolate every skeleton pixel including its staircase; this
  trades a little fidelity for a usable tangent.
- **`TRACK_BETA = 0.18`** — motion-coherence width as a fraction of the rod's
  length: wide enough that an occluded stretch is carried by the visible rod
  either side of it, narrow enough that a real bend is not flattened.
- **`TRACK_ALPHA = 0.6`** — the step toward each node's observation per
  iteration. Below one because a single frame's correspondence is noisy, and a
  node that jumps onto its nearest pixel every frame chatters along the rod.
- **`TRACK_SIGMA = 0.020` m** — correspondence width; what stops the far
  strand of a doubled-back rod capturing nodes from the near one.
- **`TRACK_VIS_FLOOR = 0.05`** — visibility below which a node is treated as
  unobserved and moved only by its neighbours (TrackDLO's `k_vis`): a gripper
  covering the rod must not drag those nodes onto the gripper.
- **`TRACK_ITERS = 6`** damped steps per frame.
- **`TRACK_STIFFNESS = 0.25`** — the bending prior, applied where the rod is
  not observed. Without it the tracker coils: measured on `weave3` with the
  arm across the rod, the occluded nodes folded into a knot (tracked error
  14.3 mm against a cold fit's 6.0), because nothing in the
  correspondence-plus-coherence update penalises curvature. This is the term
  TrackDLO gets from its non-Gaussian kernel over displacement derivatives,
  which the compact version does not have.

## Surface-to-axis correction

Depth returns the range to the object's camera-facing *surface*, so a
centreline back-projected from it lies on the skin of the cylinder, displaced
one radius toward the camera — a systematic bias, invisible in a scatter and
fully present in every number derived from it. Measured on `weave3` from a
55-degree camera: +2.5 to +3.9 mm (median 3.1) toward +x at every station, in
every pose, exactly what a 5 mm rod predicts (`R cos 55 = 2.87` mm in x,
`R sin 55 = 4.10` mm in z — and a rod read 4 mm high is a grasp planned 4 mm
shallow). The fit pushes each point one measured radius along its own view
ray, away from the camera, per point rather than one direction for the whole
curve because a 500 mm rod spans enough of the frame that the ray turns
across it. The tracker applies the same correction to the observed cloud on
the way in, so the correspondence is axis-to-axis rather than pulling every
node one radius toward the camera each pass.

The radius itself is mask area over centreline length, both in metres. Three
other ways were measured and rejected: the cloud's spread along a world axis
(reads the curve, not the thickness), perpendicular distance to the
back-projected cloud (silhouette pixels carry the bench's depth and land
centimetres out), and area over the *skeleton chain's* pixel length (a thinned
chain zigzags: 376 px of chain across a 293 px span).

## Install

```bash
gap skills install curve   # numpy, scipy, scikit-image, opencv-python-headless, pillow
```

The bundle runs out of process in its own venv (`gap.serving`); `tools.py`
imports the maths lazily, so the bundle loads without its deps installed.

## Quirks

- An empty mask, or one too thin to skeletonise, returns `points: []`,
  `nodes: 0` and `ordered: false` — not an error. Route on `ordered` and on
  `len(points)`.
- TrackDLO's chain merge can legitimately fail on a degenerate mask (a single
  clean blob gives the assignment nothing to assign); the fit then orders the
  thinned skeleton along its principal axis instead and logs a warning
  **once per process**, not per frame. A merge that fails on *every* frame
  (an upstream API change once did) shows up only as that one line — read it.
- The skeleton's ends erode a few pixels, so `arclength_m` under-reads the
  true length slightly; the tracker preserves whatever length its prior had.
- `track_centerline` with a prior of fewer than three points falls back to a
  cold fit (no `visibility`/`tracked` keys in the result). With fewer than
  eight visible cloud points it returns the prior unchanged with all-zero
  `visibility`.

## Licence

The bundle is Apache-2.0. `_trackdlo.py` is vendored from TrackDLO
([RMDLO/trackdlo](https://github.com/RMDLO/trackdlo), `trackdlo/src/utils.py`)
under the MIT licence; the permission notice travels beside it as
`LICENSE.trackdlo`, and its header lists every edit to upstream. Cite:

> Xiang, Dinkel, Zhao, Gao, Coltin, Smith and Bretl, "TrackDLO: Tracking
> Deformable Linear Objects Under Occlusion with Motion Coherence",
> IEEE RA-L 2023. doi:10.1109/LRA.2023.3303710
