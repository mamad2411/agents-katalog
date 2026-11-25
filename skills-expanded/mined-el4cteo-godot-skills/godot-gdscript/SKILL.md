---
name: godot-gdscript
description: Write correct, statically typed GDScript for Godot 4.7 - script layout, typing (typed arrays and dictionaries), signals and await, setters, @export annotations, @abstract and variadic functions, lambdas, match, static members, error fixes, plus a real-engine compile check of all .gd files. Use when writing, reviewing or fixing any .gd file.
license: MIT
compatibility: Godot 4.7+. Python 3.9+ for scripts/gd_check.py.
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# GDScript (4.7)

**Check after every edit:** `python scripts/gd_check.py [paths]` compiles every `.gd` file with the real engine and returns `{file, line, msg}` errors. Autoloads and `class_name`s resolve like they do at runtime. Look up any engine API with `../godot-core/scripts/api_lookup.py` before you use it.

## Script layout (official style guide order)
```
@tool / @icon / @abstract  →  class_name  →  extends  →  ## doc comment
signals → enums → constants → static vars → @export vars → vars → @onready vars
_static_init → _init → _enter_tree → _ready → _process/_physics_process → other virtuals
public methods → _private methods → inner classes
```
Use snake_case for files, functions and variables, PascalCase for classes and nodes, CONSTANT_CASE for constants and enum values. Indent with tabs. Prefix private members with `_`.

## Typing rules (always typed: safer, and up to ~2x faster)
- `var speed := 5.0` infers the type. Use `var target: Node3D` when there's no initializer. Use `: Variant` only on purpose.
- Typed containers: `Array[Enemy]`, `Dictionary[StringName, int]` (4.4+). Typed arrays reject wrong element types at runtime.
- Give every function a return type, including `-> void`. In 4.7, an override of a typed-return method must return on every path.
- `node as Enemy` returns `null` when the cast fails, for objects. `is` tests the type. Use `is_instance_valid(x)` after any `await` that might outlive `x`.
- Enforce typing project-wide with `debug/gdscript/warnings/untyped_declaration = 2` (Error). Keep `inference_on_variant` at its default of Error.
- `int / int` is integer division. Write `float(a) / b` when you mean a fraction.

## Signals and await
- Declare typed signals: `signal health_changed(current: int, maximum: int)`. Emit with `health_changed.emit(hp, max_hp)`.
- Connect a Callable: `button.pressed.connect(_on_pressed)`. Add arguments with `.bind(id)` and one-shot behavior with `connect(f, CONNECT_ONE_SHOT)`. Avoid string forms like `connect("x", self, "y")`.
- Connections made in code don't need manual cleanup when either object is freed. Disconnect explicitly only when you'll reconnect, or when the source is a long-lived autoload and the target is a lambda capturing a freed node.
- `await sig` suspends the function. The caller gets control back immediately unless it also awaits. Any function containing `await` is a coroutine, so the caller must `await` it to get its return value.
- Prefer `await get_tree().create_timer(0.5).timeout` and `await get_tree().process_frame`/`physics_frame` to busy waits.
- "Call down, signal up": parents call methods on children, children emit signals. Cross-scene events go through an autoload event bus (see `godot-architecture`).

## Language features you should use
- Properties: `var hp: int = 10:` followed by an indented `set(value): hp = clampi(value, 0, max_hp)`, or `set = _set_hp`.
- `@export` variants (check them with `api_lookup.py @export_range`): `@export_range(0, 100, 1, "or_greater")`, `@export_enum`, `@export_flags_3d_physics`, `@export_file("*.json")`, `@export_group("Movement")`, `@export_subgroup`, `@export_category`, `@export_storage`, `@export_custom`, `@export_tool_button("Bake", "Bake")` (4.4+).
- `@onready var label: Label = %ScoreLabel` uses a scene-unique name (`%`). That's safer than long `$A/B/C` paths.
- `@abstract class_name Weapon` with `@abstract func fire() -> void` (4.5+). Variadic arguments: `func log_all(...parts: Array) -> void` (4.5+).
- Lambdas: `var double := func(x: int) -> int: return x * 2`. They capture locals **by value**. Mutate shared state through an Array or Dictionary, or through a member variable.
- `match` handles literals, `[a, b, ..]`, `{"k": v}`, `var x` bindings and `when` guards (4.3+).
- `static var`/`static func`, `const PRELOADED := preload("res://x.tscn")`, `&"string_name"`, `^"Node/Path"`.
- Doc comments: `##` above members (shown in the editor's help and by `--gdscript-docs`).

## Pitfalls (with fixes)
| Symptom | Cause, then fix |
|---|---|
| `Invalid access ... on a base object of type 'null instance'` | Wrong node path, or used before `_ready`. Use `@onready`/`%Unique`, and `get_node_or_null` when a node is optional. |
| `previously freed` | An await or deferred call outlived the node. Check `is_instance_valid()` or `is_inside_tree()`. |
| Physics or tree changes during a callback error out | Use `call_deferred("add_child", n)`, `set_deferred("disabled", true)` or `queue_free()`. |
| `Cyclic reference` / `Could not resolve class` | `class_name` cycles between preloads. Use type hints with `load()` at runtime, or split the shared type into its own script. |
| A signal callback never fires | Connected in `_ready` of a node that isn't in the tree yet, signature mismatch, or a typo in the signal name. Typed `sig.connect()` catches typos at parse time. |
| Exported var resets | Value set in `_init` gets overwritten by the scene file. Initialize in the declaration or in `_ready`. |
| Mixed tabs and spaces | Tabs only. Godot rejects mixed indentation. |

Deeper patterns, all compiled by the test suite: [references/patterns.md](references/patterns.md).
