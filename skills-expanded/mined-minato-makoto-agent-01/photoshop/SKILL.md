---
name: photoshop
description: Control Adobe Photoshop via UXP plugin over adb-mcp Socket.IO bridge.
module: builtin_tools.photoshop_tools
tools:
  - ps_create_document
  - ps_open_document
  - ps_save_document
  - ps_close_document
  - ps_get_document_info
  - ps_create_layer
  - ps_delete_layer
  - ps_select_layer
  - ps_rename_layer
  - ps_set_layer_visibility
  - ps_set_layer_opacity
  - ps_move_layer
  - ps_resize_layer
  - ps_duplicate_layer
  - ps_merge_layers
  - ps_group_layers
  - ps_set_layer_blend_mode
  - ps_lock_layer
  - ps_rasterize_layer
  - ps_create_text_layer
  - ps_edit_text
  - ps_set_text_style
  - ps_fill_layer
  - ps_stroke_layer
  - ps_draw_rectangle
  - ps_draw_ellipse
  - ps_draw_line
  - ps_apply_gaussian_blur
  - ps_apply_sharpen
  - ps_apply_brightness_contrast
  - ps_apply_hue_saturation
  - ps_apply_levels
  - ps_apply_curves
  - ps_apply_color_balance
  - ps_apply_noise
  - ps_apply_drop_shadow
  - ps_crop
  - ps_resize_canvas
  - ps_resize_image
  - ps_rotate_canvas
  - ps_flip_canvas
  - ps_set_foreground_color
  - ps_set_background_color
  - ps_make_selection
  - ps_deselect
  - ps_invert_selection
  - ps_feather_selection
  - ps_export_png
  - ps_export_jpg
  - ps_export_layer
  - ps_get_active_layer
  - ps_undo
  - ps_redo
---

# Photoshop Skill

Provides 53 Photoshop-prefixed tools via adb-mcp proxy + UXP plugin.

## Prerequisites

1. Adobe Photoshop 26.0+ with UXP Developer Mode enabled
2. Proxy process running: `node adb-mcp/adb-proxy-socket/proxy.js`
3. UXP plugin loaded and connected

## Transport path

`Agent -> photoshop_tools.py -> Socket.IO -> adb-mcp proxy -> UXP plugin -> Photoshop`

## Usage notes

- All tools are prefixed with `ps_`.
- Most operations are mutating; apply in reversible steps where possible.
- If connectivity fails, verify proxy URL (`http://localhost:3000`) and plugin state.
