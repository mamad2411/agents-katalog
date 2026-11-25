"""Contoh scene Blender headless untuk media-forge.

Pakai:
    media-forge 3d ~/.agents/media/examples/blender-spin.py spin.mp4 --res 1080 --samples 64

Env yang disediakan media-forge:
    MF_FRAMES  folder output PNG (wajib dipakai)
    MF_RES     tinggi piksel (1080 default)
    MF_ENGINE  eevee | cycles
    MF_SAMPLES samples render
"""
import math
import os

import bpy

RES = int(os.environ.get("MF_RES", "1080"))
ENGINE = os.environ.get("MF_ENGINE", "eevee")
SAMPLES = int(os.environ.get("MF_SAMPLES", "64"))
FRAMES_DIR = os.environ.get("MF_FRAMES", "/tmp/blender-out")

# ── bersihkan scene ────────────────────────────────────────────────────────
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ── render ─────────────────────────────────────────────────────────────────
engines = {i.identifier for i in scene.render.bl_rna.properties["engine"].enum_items}
if ENGINE == "cycles":
    scene.render.engine = "CYCLES"
else:
    scene.render.engine = "BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in engines else "BLENDER_EEVEE"
if ENGINE == "cycles":
    scene.cycles.samples = SAMPLES
else:
    eevee = getattr(scene, "eevee", None)
    if eevee and hasattr(eevee, "taa_render_samples"):
        eevee.taa_render_samples = SAMPLES
scene.render.resolution_x = int(RES * 16 / 9) // 2 * 2
scene.render.resolution_y = RES
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = int(os.environ.get("MF_END", "90"))
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = os.path.join(FRAMES_DIR, "")
scene.render.film_transparent = False

# ── dunia ──────────────────────────────────────────────────────────────────
world = bpy.data.worlds.new("W")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.02, 0.03, 0.08, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.6

# ── objek utama: torus metalik ─────────────────────────────────────────────
bpy.ops.mesh.primitive_torus_add(major_radius=1.4, minor_radius=0.32,
                                 major_segments=128, minor_segments=32)
obj = bpy.context.active_object
mat = bpy.data.materials.new("metal")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.15, 0.55, 0.95, 1)
bsdf.inputs["Metallic"].default_value = 1.0
bsdf.inputs["Roughness"].default_value = 0.18
obj.data.materials.append(mat)
obj.rotation_euler = (math.radians(58), 0, 0)

# animasi putar
obj.rotation_euler.z = 0
obj.keyframe_insert("rotation_euler", frame=1)
obj.rotation_euler.z = math.tau
obj.keyframe_insert("rotation_euler", frame=scene.frame_end)
try:  # Blender <5
    for fc in obj.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
except Exception:
    pass  # Blender 5+ pakai action berlapis, interpolasi default sudah halus

# ── lantai gelap dengan pantulan ───────────────────────────────────────────
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -2))
floor = bpy.context.active_object
fmat = bpy.data.materials.new("floor")
fmat.use_nodes = True
fb = fmat.node_tree.nodes["Principled BSDF"]
fb.inputs["Base Color"].default_value = (0.01, 0.012, 0.02, 1)
fb.inputs["Roughness"].default_value = 0.12
fb.inputs["Metallic"].default_value = 0.6
floor.data.materials.append(fmat)

# ── kamera ─────────────────────────────────────────────────────────────────
cam_data = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cam_data)
scene.collection.objects.link(cam)
cam.location = (0, -6.5, 2.4)
cam.rotation_euler = (math.radians(72), 0, 0)
cam_data.lens = 55
scene.camera = cam

# ── lampu (3 titik, gaya studio) ───────────────────────────────────────────
for loc, energy, color, size in (
    ((4, -4, 5), 1200, (1.0, 0.95, 0.9), 4),
    ((-5, -2, 3), 700, (0.45, 0.7, 1.0), 5),
    ((0, 5, 4), 900, (1.0, 0.5, 0.7), 3),
):
    ld = bpy.data.lights.new("L", "AREA")
    ld.energy = energy
    ld.color = color
    ld.size = size
    lo = bpy.data.objects.new("L", ld)
    lo.location = loc
    lo.rotation_euler = (math.radians(60), 0, 0)
    scene.collection.objects.link(lo)

os.makedirs(FRAMES_DIR, exist_ok=True)
bpy.ops.render.render(animation=True)
print("selesai:", FRAMES_DIR)
