---
name: qt-qml-profiler
version: 1.0.0
description: Profile a Qt Quick app for jank, binding storms, and slow startup using the QML Profiler.
author: matrixx0070
tags: [qt6, qml, profiling, performance, scenegraph]
capabilities: []
---

## When to use

Use this when a running Qt Quick app stutters, drops frames, burns CPU on re-evaluated bindings, or takes too long to show its first frame, and you need a timeline attributing cost to JavaScript, bindings, component creation, and the scene graph. Works from Qt Creator or the standalone `qmlprofiler` CLI.

**Not for:** writing tests or asserting behavior — see `qt-qml-test`. For executing and triaging a test suite — see `qt-qml-test-run`.

## Method

1. Reproduce the symptom under a profile. **Decision point:** if you want an interactive flame/timeline view use the QML Profiler in Qt Creator; if you want a scriptable/headless capture use the standalone `qmlprofiler` CLI writing a trace file.
2. Enable the debug service on the app: launch it with `-qmljsdebugger=port:<n>,block,services:...` so the profiler can attach; `block` holds startup until the profiler connects (essential for startup profiling).
3. **Decision point:** if you are chasing startup cost, keep `block` and enable the `Creating` and `Compiling` categories; if you are chasing runtime jank, focus on `Binding`, `JavaScript`, `Painting`, and `SceneGraph`.
4. Capture a session covering the slow interaction, then stop; save the trace with `--output <trace>` (CLI) or via Creator's save.
5. Read against the frame budget: at 60fps each frame must finish in ~16.6ms. **Decision point:** if frames overrun, sort the timeline by duration and open the widest `Binding`/`JavaScript`/`SceneGraph` events first.
6. Diagnose binding storms: a single input change producing a cascade of `Binding` re-evaluations, or a `Binding loop detected` warning, points at a cyclic or over-broad dependency; narrow the binding or break the cycle.
7. **Decision point:** if the scene graph itself is the cost, inspect the render loop (`QSG_RENDER_LOOP=threaded|basic|windows`) and turn on `QSG_RENDERER_DEBUG` / `QSG_VISUALIZE` to see overdraw, batching, and changes.
8. Attack slow startup by finding the tallest `Creating` events (expensive component instantiation) and defer them with `Loader`, `asynchronous: true`, or lazy delegates.

## Example

```bash
# Launch the app with the debug service, blocking until the profiler attaches
./myapp -qmljsdebugger=port:5555,block,services:CanvasFrameRate,EngineControl,DebugMessages

# In another shell: attach the standalone profiler and write a trace
qmlprofiler --attach localhost --port 5555 --output run.qtd

# Inspect scene-graph behavior while reproducing jank
QSG_RENDER_LOOP=basic QSG_RENDERER_DEBUG=render,build QSG_VISUALIZE=overdraw ./myapp
```

```
Frame budget @60fps = 16.6 ms
  Frame 214: 41.2 ms  OVER
    Binding      27.9 ms   ListView delegate width (re-evaluated x480)
    JavaScript    9.1 ms   onCountChanged handler
    SceneGraph    3.8 ms   Render
Startup:
    Creating     612 ms    MainWindow.qml -> HeavyChart (synchronous)
```

## Pitfalls

- **Forgetting `block`.** Without `block` in `-qmljsdebugger`, the app runs before the profiler attaches and you miss all startup (`Creating`/`Compiling`) events.
- **Profiling a release with no debug service.** The QML debug service must be compiled in (default for normal builds); a fully stripped `QT_NO_QML_DEBUGGER` build cannot be attached.
- **Measuring the wrong frame.** Overhead from the profiler itself inflates numbers; compare relative costs and the frame-budget overruns, not absolute wall time.
- **Binding storms hidden in aggregates.** A cheap-looking binding re-evaluated hundreds of times per frame dominates; sort by total count, not just single-event duration.
- **Render-loop confusion.** `threaded` (default on most platforms) moves rendering off the GUI thread; forcing `basic` for debugging changes timings — note which loop produced the trace.
- **Overdraw invisible without tooling.** Excessive `Painting`/`SceneGraph` cost often needs `QSG_VISUALIZE=overdraw` to explain, not the timeline alone.

## Output format

```
App: <binary>  RenderLoop: <threaded|basic|windows>
Launch: -qmljsdebugger=port:<n>,block,services:<...>
Trace: <file>.qtd
Budget: 16.6 ms/frame @60fps
Hotspots:
  - <category>  <ms> (<count>x)  <symbol/QML loc>
Startup (Creating/Compiling):
  - <ms>  <component>  <sync|async>
Verdict: <jank | binding-storm | slow-startup>  Fix: <Loader/async/break-binding/render-loop>
```

## Reference

- QML Profiler is available inside Qt Creator (Analyze > QML Profiler) and as the standalone `qmlprofiler` CLI tool shipped in the Qt bin directory.
- Attach via the QML debug service: launch with `-qmljsdebugger=port:<n>,block,services:CanvasFrameRate,EngineControl,DebugMessages` (`host:` also accepted; `block` blocks startup until attach; `services:` selects profiler services).
- `qmlprofiler` CLI: `qmlprofiler --attach <host> --port <n>`, or `qmlprofiler -- <program args>` to launch, with `--output <trace>` to save a `.qtd` trace file for later loading.
- Timeline categories: `JavaScript`, `Binding`, `Creating` (component/object instantiation), `Painting`, `SceneGraph` (render loop stages), and `Compiling` (QML/JS compilation).
- Frame budget: 16.6 ms per frame at 60fps (8.3 ms at 120fps); frames exceeding it drop and cause visible jank.
- Scene graph render loop selectable via `QSG_RENDER_LOOP=threaded|basic|windows`; `threaded` is the default where supported. Threaded renders on a dedicated thread; `basic` is single-threaded (useful for deterministic profiling).
- Scene-graph diagnostics: `QSG_RENDERER_DEBUG=render,build,change,upload,roots` prints batching/geometry info; `QSG_VISUALIZE=overdraw|batches|clip|changes` overlays visual debugging.
- Binding-loop detection: the engine emits `Binding loop detected for property "<p>"` at runtime; the profiler's `Binding` category shows the re-evaluation cascade.
- `QT_QML_PROFILE`-style env and the CanvasFrameRate service drive frame-rate capture. Verified against Qt 6.2–6.8.
