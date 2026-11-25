---
name: shader-check
description: Look at an app's GPU work. Which shaders it ships, how it uses them, and whether a recording shows a clear slowdown to fix.
---

# Shader and GPU check

Goal: tell the user what the app does on the GPU and whether there is an obvious win.

1. Open each shader in the sidebar's GPU section. For every kernel, read its AIR and its "Loaded by" line, which names the CPU function that loads it by name.
2. For a kernel that runs often, look at what it reads: a blur or convolution that reads each pixel several times from a texture is a common cost, and reading once into threadgroup memory is the usual fix.
3. If there is a recording, open it and read the timeline, or call `gpu_profile` (eleven). Note the frame time, how busy the GPU is, and the gaps between frames.
   - GPU busy near 100%: the kernels are the cost. Point at the one doing the most memory traffic.
   - GPU idle between frames while the app waits on each one: the app serializes frames. Keeping two or three frames in flight is the fix.
   - A slow first frame: pipeline setup. Building pipelines at launch, or shipping a binary archive, fixes it.
4. If there is no recording yet, tell the user to press Record a GPU run in the sidebar.

Report in plain words: what the shaders do, which CPU code drives them, and the single most useful change, with the number from the recording that backs it up.
