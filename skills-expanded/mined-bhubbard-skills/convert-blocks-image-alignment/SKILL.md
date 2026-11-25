---
name: convert-blocks-image-alignment
description: Guidance on preserving legacy image alignment during block conversion. Use when preventing broken captions and image layouts during Gutenberg migrations.
---

# Convert to Blocks: Preserving Image Alignment

One of the biggest issues with the native WordPress "Convert to Blocks" button (found inside the Classic Block wrapper) is how it handles legacy images. 

## The Native Core Problem
If you use the native WordPress conversion, it often strips out the surrounding `<figure class="alignleft">` or `alignright` HTML wrappers. This instantly destroys your legacy image alignment and can detach captions from the image entirely.

## The Convert to Blocks Solution
The Convert to Blocks plugin is specifically engineered to safely preserve these `<figure>` tags and alignment classes during the conversion process. If you have hundreds of old posts with carefully aligned text-wrapping images, this plugin ensures you won't have to manually re-align them after migrating to the Block Editor.
