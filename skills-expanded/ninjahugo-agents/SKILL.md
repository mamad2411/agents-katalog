# AI Agent Guidelines for Godot 4.x Development

## Pre-flight Checklist

Before modifying any `.gd` file:

1. **Run headless validation** after changes:

   ```bash
   flatpak run org.godotengine.Godot --headless --path /mnt/data/code/learn/hugo --quit 2>&1
   ```

2. **Run static analysis** for style issues:
   ```bash
   gdlint scripts/ scenes/ 2>&1 | grep -v "class-definitions-order"
   ```

## Critical Type Safety Rules

Godot 4.x is strict about type inference. These patterns cause runtime errors:

### Dictionary Access

```gdscript
# WRONG - Cannot infer type from Variant
var result := dict.some_key            # Error: Cannot infer type
var value := dict.nested.property      # Error: Cannot infer type
var cmp := dict.a == dict.b            # Error: Cannot infer comparison result

# CORRECT - Explicit types
var result: String = dict.get("some_key", "")
var nested: Dictionary = dict.get("nested", {})
var value: float = nested.get("property", 0.0)
var cmp: bool = dict.get("a", "") == dict.get("b", "")
```

### Common Dictionary Patterns to Fix

```gdscript
# Pattern 1: Iterating with Dictionary elements
# WRONG
for item in items:
    if item.node.position.x > threshold:  # Cannot infer
        process(item.node)

# CORRECT
for item in items:
    var node: Node2D = item.get("node")
    if is_instance_valid(node) and node.position.x > threshold:
        process(node)

# Pattern 2: Comparisons
# WRONG
var is_match := obj1.id == obj2.id

# CORRECT
var is_match: bool = obj1.get("id", "") == obj2.get("id", "")

# Pattern 3: Passing to functions
# WRONG
some_func(data.value)

# CORRECT
var value: String = data.get("value", "")
some_func(value)
```

## Tween API (Godot 4.x)

The tween API changed significantly from Godot 3.x:

```gdscript
# Parallel tweens - set on Tween, not PropertyTweener
var tween := create_tween().set_parallel(true)
tween.tween_property(a, "position", pos_a, 0.5)
tween.tween_property(b, "position", pos_b, 0.5)

# Sequential with parallel() helper
var tween := create_tween()
tween.tween_property(a, "position", pos1, 0.5)
tween.parallel().tween_property(b, "position", pos2, 0.5)  # Runs with previous

# Chain for sequential after parallel
var tween := create_tween().set_parallel(true)
tween.tween_property(a, "scale", Vector2(1.2, 1.2), 0.2)
tween.tween_property(b, "scale", Vector2(1.2, 1.2), 0.2)
tween.chain().tween_callback(func(): print("Both done"))
```

## Scene Structure for Modals/Popups

Modals must use CanvasLayer to appear above game UI:

```
ResultsScreen (CanvasLayer, layer=10)
└── Control (has the script)
    ├── Dimmer (ColorRect, covers screen)
    └── Panel (actual modal content)
```

When referencing from parent scenes:

```gdscript
# Script is on Control child, not CanvasLayer root
@onready var results_screen: Control = $ResultsScreen/Control
```

## Signal Connection Syntax

```gdscript
# Godot 4.x - Callable syntax
signal_name.connect(callable)
signal_name.connect(callable.bind(arg1, arg2))
signal_name.connect(func(): do_something())

# Lambda with arguments
button.pressed.connect(func(): handle_press(index))
# Or with bind
button.pressed.connect(_handle_press.bind(index))
```

## Validation Errors and Fixes

### "Cannot infer the type of X variable"

- Cause: Assigning from Dictionary with `:=`
- Fix: Use explicit type declaration with `.get()`

### "Identifier not found: X"

- Cause: Missing autoload, or testing scene in isolation
- Fix: Ensure autoload is in project.godot, or expected when testing with `-s`

### "Nonexistent function 'set_parallel' in base 'PropertyTweener'"

- Cause: Calling `.set_parallel()` on tween result instead of Tween
- Fix: Call `create_tween().set_parallel(true)` instead

### Line length exceeds 100 characters

- Fix: Break long lines or extract variables:

```gdscript
# Instead of
push_error("Failed: %s (line %d)" % [json.get_error_message(), json.get_error_line()])

# Do this
var err_msg := json.get_error_message()
var err_line := json.get_error_line()
push_error("Failed: %s (line %d)" % [err_msg, err_line])
```

### Unused function argument

- Fix: Prefix with underscore: `func callback(_unused: int) -> void:`

## Testing Workflow

1. Make changes to `.gd` files
2. Run headless validation - catches compile errors
3. Run gdlint - catches style issues
4. If validation passes, test in actual game

## File Organization

- Each scene (`.tscn`) has a matching script (`.gd`) in same directory
- Autoloads go in `scripts/autoload/`
- Base classes go in `scripts/` root or appropriate subdirectory
- Reusable UI components go in `scenes/ui/`

## When Modifying Scenes

1. Read the `.tscn` file to understand node structure
2. Read the `.gd` file to understand script references
3. If changing node hierarchy, update `@onready` paths in script
4. If using unique names (`%NodeName`), ensure `unique_name_in_owner = true` in `.tscn`
