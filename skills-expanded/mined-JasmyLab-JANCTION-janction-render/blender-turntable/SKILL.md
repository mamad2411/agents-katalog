---
name: blender-turntable
description: Builds a seamless 360-degree turntable animation in Blender - orbiting camera or rotating model, a loop with no duplicated frame, frame counts and FPS for MP4 and GIF, and lighting that stays consistent - for a .blend or an imported glTF, FBX, USD or OBJ model. Use when a user wants a spinning model, a 360 product video, a portfolio turnaround or a looping GIF.
license: MIT
metadata:
  author: JasmyLab Inc. (https://render.janction.jp)
  version: "0.1.1"
  related-skills: blender-product-shots, blender-lighting-recipes, blender-animation-delivery
---

# Blender Turntable

The two mistakes that show in every bad turntable: a stutter at the loop point (the first and last frames are the same
pose) and lighting that swims because the wrong thing rotates. Decide what rotates, then make the loop exact.

## Camera orbits or model rotates?

| Rotate | Light behaviour | Use for |
|---|---|---|
| The camera (around a pivot) | Lights stay fixed to the world: you see the lit side, then the shadow side | Showing a product in a real-looking room, HDRI reflections that move |
| The model | Every side passes through the same key light | Catalog turnarounds where every side should look equally good |

Either way: keep lights and world fixed, motion blur off, and the camera's look-at point at the model's center.

## Exact loop

With N frames, frame 1 is 0 degrees and the 360-degree key goes on frame N + 1, outside the range. Frame N is then
360 x (N - 1) / N degrees and the video loops without a repeated pose. Linear interpolation keeps the speed constant.

```python
import bpy, math
from mathutils import Vector

def turntable(target_objs, frames=120, fps=30, rotate="camera", elevation_deg=18, lens=70, fill=0.75):
    s = bpy.context.scene
    s.frame_start, s.frame_end = 1, frames
    s.render.fps, s.render.fps_base = fps, 1.0
    s.render.use_motion_blur = False

    pts = [o.matrix_world @ Vector(c) for o in target_objs for c in o.bound_box]
    center = sum(pts, Vector()) / len(pts)
    radius = max((p - center).length for p in pts)

    pivot = bpy.data.objects.new("TT_Pivot", None)
    s.collection.objects.link(pivot)
    pivot.location = center

    cam_data = bpy.data.cameras.new("CAM_Turntable")
    cam_data.lens = lens
    cam = bpy.data.objects.new("CAM_Turntable", cam_data)
    s.collection.objects.link(cam)
    r = s.render
    aspect = (r.resolution_x * r.pixel_aspect_x) / (r.resolution_y * r.pixel_aspect_y)
    t = math.tan(cam_data.angle / 2)
    tx, ty = (t, t / aspect) if aspect >= 1 else (t * aspect, t)   # sensor_fit AUTO: the angle spans the longer side
    e = math.radians(elevation_deg)
    fwd, right = Vector((0, math.cos(e), -math.sin(e))), Vector((1, 0, 0))
    up = right.cross(fwd)
    turn = []                                             # every corner at every 15 degrees of the turn
    for k in range(24):
        ca, sa = math.cos(math.tau * k / 24), math.sin(math.tau * k / 24)
        for p in pts:
            v = p - center
            v = Vector((v.x * ca - v.y * sa, v.x * sa + v.y * ca, v.z))
            turn.append((v.dot(right), v.dot(up), v.dot(fwd)))

    def fit(shift):                                       # closest distance that keeps every corner inside fill
        return max([radius * 1.05] + [max(abs(x) / (tx * fill), abs(y - shift) / (ty * fill)) - z for x, y, z in turn])

    shift = 0.0
    for _ in range(3):                                    # centre the band the object sweeps vertically
        dist = fit(shift)
        ys = [(y - shift) / ((dist + z) * ty) for x, y, z in turn]
        shift += (max(ys) + min(ys)) / 2 * dist * ty
    dist = fit(shift)
    aim = center + up * shift
    cam.location = aim - fwd * dist
    cam.rotation_euler = (aim - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam_data.clip_end = max(cam_data.clip_end, dist * 4)
    s.camera = cam
    bpy.context.view_layer.update()                       # matrix_world is current before parenting

    if rotate == "camera":
        cam.parent = pivot
        cam.matrix_parent_inverse = pivot.matrix_world.inverted()
        spinner = pivot
    else:
        for o in target_objs:
            if o.parent is None:
                o.parent = pivot
                o.matrix_parent_inverse = pivot.matrix_world.inverted()
        spinner = pivot

    spinner.rotation_euler = (0, 0, 0)
    spinner.keyframe_insert("rotation_euler", index=2, frame=1)
    spinner.rotation_euler = (0, 0, math.tau)
    spinner.keyframe_insert("rotation_euler", index=2, frame=frames + 1)
    for fc in fcurves_of(spinner):                        # new keys ease in and out; a turntable must not
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    return cam

def fcurves_of(obj):
    """F-curves of an object's action, before and after the layered actions of Blender 4.4 and later."""
    ad = obj.animation_data
    act = ad.action
    if getattr(act, "fcurves", None):                     # Blender 4.3 and earlier
        return list(act.fcurves)
    from bpy_extras import anim_utils
    bag = anim_utils.action_get_channelbag_for_slot(act, ad.action_slot)
    return list(bag.fcurves) if bag else []

model = [o for o in bpy.context.scene.objects if o.type == "MESH" and not o.name.startswith("Backdrop")]
turntable(model)
```

## Frame counts

| Output | Frames | FPS | Length | Notes |
|---|---|---|---|---|
| Web MP4 | 120 | 30 | 4 s | Smooth; 3 degrees per frame |
| Slow showcase | 240 | 30 | 8 s | Reads details; twice the render time |
| GIF | 36-72 | 12-24 | 3 s | 5-10 degrees per frame keeps the file small |
| Quick check | 24 | 24 | 1 s | Enough to see every side |

Render frames to PNG first, then encode (blender-animation-delivery). A GIF needs a palette pass to avoid banding:
`ffmpeg -framerate 24 -i frame_%04d.png -vf "scale=720:-1:flags=lanczos,palettegen" pal.png` then
`ffmpeg -framerate 24 -i frame_%04d.png -i pal.png -lavfi "scale=720:-1:flags=lanczos[x];[x][1:v]paletteuse" out.gif`.

## Check before the full render

Render frames 1, N/4, N/2 and N. Frame N must be one step before frame 1, not the same pose. For an exact check, render
frame N + 1 once (outside the delivery range): it must look identical to frame 1. Look for a floor or backdrop edge
entering the frame at some angle and for lights that pop into reflections.

## With JANCTION Render

`render_preview(scene_url=..., orbit=True)` shows four angles in one image (a cheap check). The final turn is
`render_final(..., preset="turntable")` (a full turn as an MP4 on a plain backdrop) or `orbit=True` with
`orbit_frames`. From a terminal: `uvx janction-render turntable model.glb`.
