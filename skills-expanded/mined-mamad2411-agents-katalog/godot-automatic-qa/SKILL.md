---
name: godot-automatic-qa
description: |
  Self-verify Godot 4 work instead of guessing or asking the user — two loops. (1) A fast VISUAL loop: inject a one-shot screenshot timer into the running project, launch it headfully from the CLI, and read the resulting PNG yourself. (2) A headless BEHAVIORAL loop: write a SceneTree test script (ASSERT PASS/FAIL console checks, simulated input, closed-loop steering) that loads a scene and verifies it behaves correctly across frames. Use the visual loop whenever the user says the UI "looks wrong / 一塌糊涂 / panels invisible / proportions off", or after you change a theme/layout/scene and need to see it before claiming done. Use the test script whenever you need automated verification that a scene or feature behaves correctly — positions, state, reaching a goal — either standalone or feeding `godot-capture` for a video. Works for C# (.NET) and GDScript. Strongly prefer this over asking the user to take a screenshot — close the verification loop yourself.
---

# Automatic QA — self-verification for Godot (visual + behavioral)

The structural smoke test ("scene instantiates, parser clean, 0 errors") doesn't see whether panels have backgrounds, whether splits give the right proportions, whether icons resolved, whether text overflowed — or whether the character actually reached the goal, the camera tracked it, and the state machine advanced. Don't ship work blind. Verify it yourself, two ways:

- **Loop A — visual:** inject a screenshot timer, launch headfully, `Read` the PNG. For "does it *look* right".
- **Loop B — behavioral:** a headless `SceneTree` test script with `ASSERT PASS/FAIL` lines and simulated input. For "does it *behave* right" across frames.

## Which loop

- *Looks wrong / layout / theme / icons / text overflow* → **Loop A** (visual screenshot).
- *Behavior across frames — position, velocity, state, "did it reach the goal"* → **Loop B** (SceneTree test).
- *A final video or screenshot deliverable* → `godot-capture` (Loop B's test scripts feed its movie-writer flow).

## When NOT to use this

- Producing final video/screenshot deliverables → use `godot-capture`.
- Cases where you genuinely can't get the rendered scene to a useful state without user input (login dialog, file picker, etc.) — say so, and ask the user.

---

# Loop A — Quick visual loop (headful screenshot)

A fast inner loop: inject a temporary screenshot timer into the project, launch it headfully, the project saves a PNG and quits, then you `Read` the PNG. Edit, repeat. No `.capture/` scaffolding, no `xvfb`, no `ffmpeg` — that's `godot-capture`'s job for final deliverables. This is for the inner debug loop, and a second iteration is cheap (you'll likely change something and look again).

## The minimal recipe

1. **Pick the injection site** — the main scene's `_ready()`, *after* anything load-bearing has run (theme apply, autoload wiring, bootstrap). A safe spot is right at the end of `_ready()`.

2. **Inject a one-shot timer** — one function fires a timer, then on tick saves the viewport image and quits. Mark the code clearly so you can rip it out later.

3. **Launch headfully** — `godot --path <project_dir>` (NO `-e`, NO bare `project.godot` path) so Godot runs the game, not the editor. Pin a known resolution with `--resolution WxH`.

4. **Read the PNG** — write to `/tmp/<name>.png` so the `Read` tool can open it as an image.

5. **Remove the injection** when the visual loop is done.

### GDScript injection template

```gdscript
# DEBUG SCREENSHOT — remove when visual QA pass is finished
func _schedule_screenshot_for_debug() -> void :
    var t: SceneTreeTimer = get_tree().create_timer(2.5)
    t.timeout.connect(func() -> void :
        var img: Image = get_viewport().get_texture().get_image()
        if img != null :
            img.save_png("/tmp/app_qa.png")
            print("[DEBUG] Screenshot saved to /tmp/app_qa.png size=%s" % img.get_size())
        var t2: SceneTreeTimer = get_tree().create_timer(0.3)
        t2.timeout.connect(func() -> void : get_tree().quit())
    )
```

Call `_schedule_screenshot_for_debug()` from `_ready()` after all important setup.

### C# variant

```csharp
// DEBUG SCREENSHOT — remove when visual QA pass is finished
private void ScheduleScreenshotForDebug()
{
    var t = GetTree().CreateTimer(2.5);
    t.Timeout += () =>
    {
        var img = GetViewport().GetTexture().GetImage();
        img?.SavePng("/tmp/app_qa.png");
        var t2 = GetTree().CreateTimer(0.3);
        t2.Timeout += () => GetTree().Quit();
    };
}
```

### Launch + read

```bash
# Linux / macOS — adjust the binary path for the host OS
rm -f /tmp/app_qa.png
godot --path /path/to/project --resolution 1600x900 2>&1 | tail -10
```

On macOS the binary typically lives at `/Applications/Godot.app/Contents/MacOS/Godot`; on Linux it's `godot` (or `godot4`) on PATH. Use whichever invocation works in the current shell.

Then use the `Read` tool on `/tmp/app_qa.png`. It renders inline as an image — you can see it directly.

## Choosing the delay

The timer wait controls when the screenshot fires relative to scene ready. Tune it:

- **1.0–1.5s** is enough for static UI that's fully laid out by `_ready()`
- **2.0–2.5s** is the safe default — covers async autoloads, theme application, project scan
- **Longer** when you need to wait on signals (project open, scene swap). In that case prefer **chained timers** — fire the action first, wait, then snapshot

```gdscript
func _schedule_screenshot_for_debug() -> void :
    var t_setup: SceneTreeTimer = get_tree().create_timer(1.2)
    t_setup.timeout.connect(func() -> void :
        # do the in-app navigation first (open project, switch screen, drill in, etc.)
        _drive_app_to_target_screen()
        var t_shot: SceneTreeTimer = get_tree().create_timer(2.0)
        t_shot.timeout.connect(func() -> void :
            get_viewport().get_texture().get_image().save_png("/tmp/app_qa.png")
            var t2: SceneTreeTimer = get_tree().create_timer(0.3)
            t2.timeout.connect(func() -> void : get_tree().quit())
        )
    )
```

This is how you avoid screenshotting a project picker / login / splash when the bug lives deeper inside.

### Capturing a long scrollable page

A single viewport snapshot only shows what's above the fold. If the page exceeds the window height, you'll miss whatever's at the bottom — often the broken section. Two cheap fixes:

1. **Two-shot top + bottom**: take a first PNG, walk the active scene subtree to find the first `ScrollContainer`, set `sc.scroll_vertical = 99999`, wait one timer tick, take a second PNG. Save as `/tmp/<task>_top.png` and `/tmp/<task>_bottom.png`. Read both.
2. **Resize the viewport taller**: `--resolution 1600x2400` makes the window tall enough that the page fits in one shot. Useful when there is no scroll container to drive.

Method 1 is what you usually want — it matches what the user actually sees at standard resolution and surfaces both above- and below-the-fold issues.

## In-app navigation before snapshot

Apps with a "pick a project" or "main menu" gate screenshot the gate, not the feature. Drive past it programmatically — but use the project's *real* API, don't invent names:

- Look up the autoload singletons in `project.godot` (under `[autoload]`) and grep for their public methods. Common shapes: a project manager exposing something like `open_project(...)` or `load_document(...)`; a router/state-machine exposing something like `set_screen(...)` / `goto(...)`.
- Call `has_method(...)` defensively if you're unsure — the same name across projects often has different signatures.
- Use `call_deferred(...)` for screen swaps so they happen after the current frame settles.
- If the target screen needs sample data (the bug is in how a list renders, but the list is empty), create a fixture programmatically or pick a fixture project that already has content. An empty screen proves layout but not data flow.

## Critical CLI invocation gotchas

- `godot project.godot` and `godot --path <dir>` both run the **game** if no `-e` flag is present. With `-e` (or `--editor`) you get the editor. Don't accidentally screenshot the editor.
- `godot --script foo.gd project.godot` runs in `--script` mode, which uses the editor's autoload context — autoload singletons may fail to load with `Identifier not found`. For real visual QA, run the project headfully, not via `--script`.
- `--headless` disables rendering. Headless screenshots return blank/uninitialized images. Don't pair `--headless` with Loop A.
- Pin a resolution with `--resolution WxH`. Otherwise the OS picks one based on screen and screenshots have inconsistent aspect ratio between iterations — comparisons become harder.
- Save under `/tmp/` (or another absolute path you can read back) — the `Read` tool can read any path it has access to and renders PNGs inline.

## Reading the screenshot

In Claude Code / Claude.ai, the `Read` tool natively renders PNG/JPG as inline images. After your bash launch completes:

1. `Read /tmp/<task>_qa.png` — you'll see the image directly.
2. Diagnose what's actually wrong (panel missing background, splits collapsed, icons not loaded, text overflow, etc.).
3. Edit the offending theme/scene/script.
4. Re-launch. Read. Repeat.

Typical loop time per iteration is 10–20 seconds total. Faster than asking the user.

## Finding nodes inside instanced sub-scenes

When the active scene embeds another `.tscn` and you need to manipulate a node inside the sub-scene at runtime, `%UniqueName` lookups don't reach across — unique names are scoped to their owning scene. Use:

```gdscript
var inner: Node = find_child("<NodeName>", true, false)
# recursive=true to walk descendants; owned=false to NOT filter by ownership
```

`owned=false` is the key — without it, `find_child` only returns nodes owned by the current scene's root, which excludes everything inside an instanced child scene.

When the embedded sub-scene's layout is wrong for your composition (e.g. an embedded library widget has its own HSplit with a useless detail pane in your enclosing layout), the cleanest fix is to surgically lift the useful child out and free the wrapping container:

```gdscript
var split: HSplitContainer = find_child("<HSplitName>", true, false) as HSplitContainer
var parent: Node = split.get_parent()
var keep: Node = split.get_node_or_null("<ChildToKeep>")
if keep != null and parent != null:
    var idx: int = split.get_index()
    split.remove_child(keep)
    parent.add_child(keep)
    parent.move_child(keep, idx)
    split.queue_free()
```

This is preferred over `split_offset = 99999` + `dragger_visibility = DRAGGER_HIDDEN`. Those hide the handle but the second pane still claims layout space, leaving a phantom empty column. Re-parenting is unambiguous.

**Note:** `queue_free()` on the container frees its remaining children too. If the sub-scene's script keeps `@onready` references to those children and tries to write to them later (visibility toggles, etc.), you'll get `Invalid assignment ... previously freed`. Either hide the children instead of freeing them, or guard the sub-scene's call sites with `is_instance_valid(...)`.

## Creating missing icons inline

If a button looks blank after a theme change, the icon file probably doesn't exist at the path the theme builder looks up. Grep for the file first. If the project uses a stroke-icon set (e.g. lucide-style SVGs under some `res://.../icons/<name>.svg`), you can write the missing SVG yourself — icon sets like lucide are MIT-licensed and the path data is public.

Template (24×24 viewBox, stroke 2, round caps — the lucide convention):

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="…"/></svg>
```

`stroke="#ffffff"` (white) is intentional — it lets the theme re-tint the icon via `add_theme_color_override("icon_normal_color", ...)` per button state. After writing the SVG, run import once so Godot generates the `.import` and `.ctex` files (without that step `load("res://...svg")` still returns `null`):

```bash
godot --headless --import /path/to/project.godot 2>&1 | tail -5
```

Then re-launch. Don't fall back to unicode glyphs unless you've confirmed the project's font actually renders them — many UI fonts ship without symbol coverage.

## Triage patterns

When the screenshot shows something unexpected:

- **Panels look transparent / invisible** — the theme's `PanelContainer` panel stylebox either has zero border width and a background color too close to the parent, or has no stylebox at all. Fix the theme's contrast, don't restructure the layout.
- **Splits collapsed (one child very small)** — `split_offset` semantics: positive HSplit makes the first (left) child wider; positive VSplit makes the first (top) child taller. If a child lacks `size_flags_*` set to `SIZE_EXPAND_FILL` (= 3) it won't grow. Set `custom_minimum_size` on both children to give the layout something to honor.
- **Buttons blank / icons missing** — the icon resource doesn't load. Check the path; if the project uses a known icon set, write the SVG and re-import. See "Creating missing icons inline" above.
- **Text overflows / wraps weirdly** — usually a Label missing `autowrap_mode`, or a fixed-width input forcing the row beyond its container. Don't add `custom_minimum_size` blindly — check parent constraints first.
- **Wrong screen captured** — your screenshot probably caught a gate (project picker, login, splash). Add in-app navigation before the snapshot.
- **One child of a card balloons into a giant blob covering everything** — the parent is a `Container` subclass (PanelContainer, VBoxContainer, etc.) and you added absolute-positioned children (anchor dots, badges, overlays) directly to it. Godot Containers auto-stretch every direct child to their content rect, so a small element with a high `corner_radius` becomes a huge ellipse. Fix: wrap the card root as a plain `Control` (non-Container), put the visual `PanelContainer` background as ONE child filling the rect via `PRESET_FULL_RECT`, and add absolute-position siblings (anchors, badges) directly to the outer Control. Container layout only applies to direct Container children.

## Cleanup

The injected code is debug instrumentation, not feature code. When the visual loop is done:

- Remove the screenshot scheduler function and the `_ready()` call into it.
- Remove any in-app-navigation helper you added solely for the snapshot.
- `/tmp/*.png` cleans itself.

Leaving the debug screenshot active will make every future windowed launch auto-quit after a few seconds, which is confusing for the next person (or future-you).

If you anticipate needing this loop again soon, leave the function body in place but un-wire the `_ready()` call. Then re-wiring is one line, not a rebuild.

## Validation standard

A visual QA pass is real if:

- The screenshot loaded and you actually read it (not just confirmed the file exists)
- You named at least one specific visual defect, or stated explicitly "I see no visual defects"
- If you changed anything based on what you saw, a follow-up screenshot showed the change

Don't claim "UI verified" off a structural smoke test or off a screenshot you didn't open.

## Worked example shape

Symptom: user says the UI looks wrong; you've never seen the rendered app.

1. Find the main scene's script (look at `application/run/main_scene` in `project.godot`). Append a one-line call to a new `_schedule_screenshot_for_debug()` at the end of `_ready()`.
2. Add the function body using the GDScript template above. Pick `/tmp/<task>_qa.png` as the output path.
3. If the app gates on a picker / login screen: add a helper that drives the app past the gate using its *real* autoload API (grep autoloads first), and chain a setup timer before the snapshot timer.
4. `rm -f /tmp/<task>_qa.png && godot --path /path/to/project --resolution 1600x900`
5. `Read /tmp/<task>_qa.png`. See actual problems (panel borders missing, contrast too low, icon miss, split collapsed, ballooning child).
6. Fix the root cause in the theme / scene / script.
7. Re-launch. Re-read. Confirm fix.
8. Strip the debug code.
9. Report what changed.

Total: a few minutes per iteration, no user round-trips needed.

---

# Loop B — Headless behavioral test (SceneTree script)

When the question is *behavior* — did the character reach the goal, did the camera track it, did the state machine advance, is the velocity right — write a `SceneTree` test script that loads the scene under test, advances frames, and verifies the goal. C#: `test/TestXxx.cs` (e.g. `test/TestT3.cs`); GDScript: `test/test_xxx.gd` (e.g. `test/test_t3.gd`).

## Language: C# (.NET) or GDScript?

Detect the project language before writing the test. A `.csproj`/`.sln` file, or a `[dotnet]` section in `project.godot`, means the project is **C# (.NET)**; otherwise it is **GDScript**. The test logic is identical across both languages — load the scene, advance frames, assert — only the syntax and the build prerequisite differ. Pick the path that matches the project and follow the language-labeled notes below.

## SceneTree script contract

Tests must extend `SceneTree` (not Node). Key details shared by both languages:
- Setup goes in the initialize hook, **not** a `_ready` — `_Initialize()` (C#) / `_initialize()` (GDScript)
- The per-frame process hook returns `false` to keep running
- Camera needs `current = true` to activate (`_cam.Current = true` in C#)
- The script must **not** call `Quit()` — exit is handled by `--quit-after N` (a built-in Godot flag) or by `godot-capture`'s movie writer

**[C# only]**
- `_Process(double delta)` returns `bool` — return `false` to keep running
- Must be `public partial class`
- Must run `dotnet build` before running the test

**(GDScript)**
- Use `func _initialize() -> void:` for setup
- Use `func _process(delta) -> bool:` returning `false` to keep running
- No `public partial class` — a plain script `extends SceneTree` is enough
- No `dotnet build` step — there is nothing to compile

## How to run Loop B

- **Standalone behavioral check (no video):**

  ```bash
  godot --headless --script test/test_xxx.gd --quit-after 120   # GDScript
  # C#: dotnet build first, then  godot --headless --script test/TestXxx.cs --quit-after 120
  ```

  Then grep stdout for `ASSERT FAIL` — any such line must be fixed before the task is complete. `--quit-after N` is the frame count after which Godot exits, so the script never needs to call `Quit()` itself.

- **With video:** run the same script through `godot-capture`'s movie-writer flow (`--write-movie … --fixed-fps … --quit-after … --script test/…`), which renders frames and lets you encode an `mp4`.

## Console assertions

The test harness stdout is captured alongside any screenshots. Print `ASSERT PASS/FAIL: ...` lines to verify behavioral properties that are hard to judge visually (exact positions, velocities, state changes). After running, check stdout for any `ASSERT FAIL` lines — these must be fixed before the task is complete.

**(C# / .NET)**

```csharp
GD.Print("ASSERT PASS/FAIL: ...");
```

**(GDScript)**

```gdscript
print("ASSERT PASS/FAIL: ...")
```

## Simulated input

For tests needing player input, use a `Timer` to trigger actions. This works in both languages.

**(C# / .NET)**

```csharp
var timer = new Timer();
timer.WaitTime = 1.0;
timer.OneShot = true;
timer.Timeout += () => Input.ActionPress("move_forward");
Root.AddChild(timer);
timer.Start();
```

**(GDScript)**

```gdscript
var timer := Timer.new()
timer.wait_time = 1.0
timer.one_shot = true
timer.timeout.connect(func(): Input.action_press("move_forward"))
root.add_child(timer)
timer.start()
```

### Sustained movement — use closed-loop steering (default)

Open-loop input (timed press/release sequences) causes visible drift, edge-sticking, and tightening spirals as per-frame errors compound. **Default to closed-loop waypoint steering:** read the actual position each frame and steer toward the next waypoint. This applies to all tests with sustained movement, not just presentation scripts.
