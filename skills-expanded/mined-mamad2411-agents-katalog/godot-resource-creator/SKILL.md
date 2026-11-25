---
name: godot-resource-creator
description: Create Godot resource files (.tres) programmatically including themes, materials, environments, and custom resources. Essential for giving games their visual identity.
---

# Godot Resource Creator Skill

Creates `.tres` (text resource) files for Godot 4. These are used for themes, materials, environments, physics materials, and custom resources.

## Tool Usage

```bash
python3 .gemini/skills/godot-resource-creator/scripts/create_resource.py \
  --type "Theme" \
  --output "res://themes/main_theme.tres" \
  --properties "default_font_size=18"
```

For complex resources, write the `.tres` content directly.

## .tres File Format

```
[gd_resource type="<ResourceType>" load_steps=<N> format=3]

[ext_resource type="<Type>" path="<path>" id="<id>"]

[sub_resource type="<Type>" id="<id>"]
property = value

[resource]
property = value
```

## Common Resource Templates

### Theme
```
[gd_resource type="Theme" format=3]

[resource]
default_font_size = 18
```

### Environment (3D)
```
[gd_resource type="Environment" format=3]

[sub_resource type="ProceduralSkyMaterial" id="sky_mat"]
sky_top_color = Color(0.2, 0.4, 0.8, 1)
sky_horizon_color = Color(0.6, 0.7, 0.9, 1)
ground_bottom_color = Color(0.1, 0.07, 0.05, 1)
ground_horizon_color = Color(0.6, 0.7, 0.9, 1)

[sub_resource type="Sky" id="sky"]
sky_material = SubResource("sky_mat")

[resource]
background_mode = 2
sky = SubResource("sky")
ambient_light_source = 2
ambient_light_color = Color(0.5, 0.5, 0.6, 1)
tonemap_mode = 2
glow_enabled = true
fog_enabled = true
fog_light_color = Color(0.7, 0.75, 0.85, 1)
fog_density = 0.01
```

### StyleBoxFlat (for UI panels)
```
[gd_resource type="StyleBoxFlat" format=3]

[resource]
bg_color = Color(0.15, 0.15, 0.2, 0.9)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.4, 0.5, 0.8, 1)
corner_radius_top_left = 8
corner_radius_top_right = 8
corner_radius_bottom_right = 8
corner_radius_bottom_left = 8
shadow_color = Color(0, 0, 0, 0.3)
shadow_size = 4
```

### ShaderMaterial
```
[gd_resource type="ShaderMaterial" load_steps=2 format=3]

[sub_resource type="Shader" id="shader_1"]
code = "shader_type canvas_item;
uniform vec4 color : source_color = vec4(1.0);
void fragment() {
    COLOR = color;
}"

[resource]
shader = SubResource("shader_1")
shader_parameter/color = Color(1, 0.5, 0, 1)
```

### PhysicsMaterial
```
[gd_resource type="PhysicsMaterial" format=3]

[resource]
friction = 0.8
bounce = 0.2
```

### AudioBusLayout
```
[gd_resource type="AudioBusLayout" format=3]

[resource]
bus/1/name = &"SFX"
bus/1/solo = false
bus/1/mute = false
bus/1/bypass_fx = false
bus/1/volume_db = 0.0
bus/1/send = &"Master"
bus/2/name = &"Music"
bus/2/solo = false
bus/2/mute = false
bus/2/bypass_fx = false
bus/2/volume_db = -3.0
bus/2/send = &"Master"
```

## Tips

- `load_steps` = number of ext_resource + sub_resource + 1
- `[resource]` section is the main resource being defined
- For Theme resources, it's often better to create them via code or a dedicated theme editor — the .tres format for themes is very verbose
- AudioBusLayout should be saved as `res://default_bus_layout.tres` and set in project settings
