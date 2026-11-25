---
name: forgeax-engine-app
description: >-
  ForgeAX App assembly, worker policies, and browser frame ownership. Use when
  bootstrapping a game, selecting time or worker policy, wiring plugins/input/profiling,
  or diagnosing execution and rebuild reports.
---

# forgeax-engine-app

For mounted HUD layout and actions, use the [UI contract](../../packages/ui/README.md).
`mountUi` gives percentage-height content the host viewport height; keep scrolling
on the authored element. Its `onAction` delegation reads `data-ui-action`, not an
arbitrary `data-action` attribute. Verify real click acknowledgement and visible
geometry rather than the presence of HTML text.

## Render happy path

Supply optional host tools through the App host adapter. Keep environment and
HMR interpretation in DevKit or the bundler adapter; App, Renderer and animation
consume explicit capabilities and diagnostic subscriptions. Follow the
[runtime boundary contracts](../../scripts/ci/README.md#runtime-and-tool-boundary-contracts)
when adding an adapter or diagnosing a boundary gate failure.

The app host follows `RenderScene -> Standard Pipeline -> DeviceScope -> FrameReceipt`.
Use `createApp`, then let the host perform `attach -> draw`; use `inspect`, `observe`, and `recover`
with the returned receipt. Domain producers keep their own assets, input, audio, and plugin owners.

## Recovery route

Index renderer recovery as `renderer.state() -> renderer.inspect() ->
renderer.recover() -> FrameReceipt`. Renderer is the unique recovery owner;
App only admits a frame when the renderer is `alive`. `device-lost` and
`recovering` keep the Host/rAF heartbeat but freeze World update and submit
when logic and rendering are co-located. With a Render Worker, inspect `report.render`: App replaces
the GPU owner with a fresh epoch/baseline while retaining the source World identity.
World updates wait until the replacement is ready and has publication capacity.
For confirmed device loss with resident meshes, wait for the receiver's bounded
disposal acknowledgment before reusing the source World. Cleanup failure,
timeout or transport loss remains fatal with `meshReleaseUnconfirmed`; do not
infer GPU release from Worker termination.
Recheck both together after asynchronous waits: loss clears the old queue before
the replacement can admit a source frame.
Read `app.canvas` after replacement and rebind any caller-owned DOM listeners.
For picture acceptance, count `forgeax:frame-completed` events whose
`presentation` is `ready` on that canvas and current World. The report
`render.completedFrame` is a source publication identifier; subtracting
identifiers does not count completed pictures or exclude preparation.
`recover()` is single-flight, so concurrent calls share one Promise. A
`faulted` renderer must be disposed and recreated; `disposed` is terminal.

Branch on the closed `RenderError` code and read `expected`, `hint`, and typed
`detail`. Use its guidance to wait for the active flight, explicitly retry,
repair the named producer or capability, or rebuild the Renderer. After a
successful recovery, retry the same request and require its `FrameReceipt` and
device generation as submit evidence. Target/history identities survive, but
new-generation contents are uninitialized until that receipt; fallback output
is not real Browser/Dawn proof. Do not scan the factory for a hidden retry
loop, add a RecoveryManager, switch backend, destroy the old device, or create
a second submit path.

Browser display consumers can subscribe with
`subscribeBrowserFrameSubmitted(canvas, listener)`. The callback carries the
accepted frame/device/graph identity and the deeply frozen output mapping,
including identity distortion. Use it for display picking and world labels;
discard it on loss, retirement, or zero-size output and reacquire context only
after the existing Renderer recovery route succeeds. Worker execution carries
the same serializable facts through its frame-complete message.

> **`createApp` is a host adapter, not a second scheduler.** It measures one native host delta, calls `world.update(deltaSeconds)`, then draws. Game behavior belongs in ECS `Update` or `FixedUpdate` systems.

## One-screen takeoff

```ts
import { createApp } from '@forgeax/engine/app/browser';
import { Time, Update } from '@forgeax/engine/ecs';
import { forgeaxBundlerAdapter } from 'virtual:forgeax/bundler';

const result = await createApp(canvas, {}, forgeaxBundlerAdapter());
if (!result.ok) {
  console.error(result.error.code, result.error.hint);
  throw result.error;
}

const app = result.value;
app.world.addSystem(Update, {
  name: 'move-player',
  queries: [],
  fn: (world) => {
    const delta = world.getResource(Time).delta;
    void delta;
  },
}).unwrap();
app.start().unwrap();
```

Import browser construction from `@forgeax/engine/app/browser`; the root `app` entry requires an explicit borrowed `platform`, `renderer`, and `world`. The browser entry creates its World, renderer, default plugins, browser input backend, and frame loop. `app.start()` only arms the browser loop after the factory Result is successful.

CSS-sized drawing buffers use `canvasPixelRatio: 1` by default, matching
Three.js `setPixelRatio(1)`. Set `canvasPixelRatio: window.devicePixelRatio` to
request the browser's device scale explicitly. App does not follow device pixel
ratio or adjust resolution automatically for device performance. Render's
authored `DynamicResolution` remains a separate opt-in. Device texture limits
still clamp the resulting physical extent proportionally.

Choose `animation: { cadence: 'fixed' }` at App assembly when using skeletal
motion. Ordinary DevKit projects forward that same option through
`forgeax dev start --animation '{"cadence":"fixed"}'` and
`forgeax project build --animation '{"cadence":"fixed"}'`; public
`startLiveDev` and `buildCommand` accept `animation` unchanged. Main and Worker
use one App-installed animation owner. A Pack behavior must consume it rather
than installing a second playback plugin with a different cadence.

## Worker execution

```ts
const result = await createApp(canvas, {
  execution: {
    bootstrap: new URL('./game-bootstrap.mjs', import.meta.url),
    // Omitted policies are auto: enable every supported worker.
    workers: { engine: 'auto', render: 'auto', kernels: 'auto' },
  },
}, forgeaxBundlerAdapter());
if (!result.ok) throw result.error;
result.value.start().unwrap();
const report = result.value.execution.report();
```

| Need | Action |
|:--|:--|
| Default parallel execution | Omit `workers`; inspect each `report.workers` decision |
| Fixed skeletal animation | Set `animation: { cadence: 'fixed' }` and World fixed time; App forwards the Animation-owned POD to Host/Engine Worker, including rebuild. Add the motion plugin without duplicating default animation. |
| Require a worker | Set its policy to `true`; handle `app-execution-worker-unavailable` |
| Disable independent rendering | Set `render: false`; configure the co-located Renderer |
| WebGPU adapter cannot be acquired | Keep `auto`; usable Worker WebGL2 remains eligible. Inspect `report.capabilities.workerWebGpu` for admission and `report.render.capabilities.backendKind` for the actual backend |
| Shared numeric kernels | Leave `kernels: 'auto'`, serve COOP/COEP and inspect actual `kernelDispatch` |
| Host-only bootstrap | Set `engine: false`; leave dependent policies auto or false |
| Partial Kernel write | Call `app.execution.rebuild()` and use the new World identity |
| Fixed presentation rate (e.g. 30 FPS) | `app.execution.setFrameRateLimit(30)`; `null` removes it. Admission stays on display callbacks and World time is unchanged |

World and Assets stay in the Engine Worker. With `render` enabled, a child owns
Renderer/WebGPU; source plugins inject World/Assets and use bootstrap
`configureRenderer` for GPU setup. Declare Feature implementations through the
bootstrap. Logic N+1 overlaps render N; admission of N+2 waits for N's GPU receipt.
Kernel workers receive eligible shared numeric spans, independently of render
placement. Their initialization and module preflight inherit App `startupTimeoutMs`;
the first source frame uses that same startup policy. Later source admissions retain
their `frameTimeoutMs` bound, and running kernel dispatch retains its own deadline.
Missing isolation disables auto kernels only. Canvas/assemble calls
without a bootstrap explicitly construct local objects and remain local. DevKit generates that bootstrap for ordinary projects automatically; both templates therefore default to auto with browser UI (`roots.frontend`) and Engine gameplay (`roots.engine`) assets. `roots.host` remains the resident Node backend.
Use the [App contract](../../packages/app/README.md#worker-execution) for placement,
recovery and the report schema, and [ECS](../forgeax-engine-ecs/SKILL.md) for kernel eligibility.

When a host temporarily hands the presentation surface to another carrier
(for example, a disposable Play iframe or Tauri WebView), use
`await app.releaseSurfacePreserveWorld()` before mounting the new owner and
`await app.restoreSurface()` after it is destroyed. This preserves the exact
Edit World and Renderer identity; `app.stop()` and `renderer.dispose()` are
not relocation APIs. `app.stop()` only stops frame scheduling; `app.dispose()`
drains the plugin realm and releases the renderer.

## WebGPU stub for GPU-less CPU diagnostics

`createApp(canvas, { gpuStub: profile })` installs the `rhi-webgpu` stub in the main
realm before execution capability probing and forwards the profile to the Engine
and Render Workers, which install it before their Renderer exists. Worker WebGPU
counts as available, so the selected topology matches a GPU host. Generated hosts
map `?forgeax-gpu-stub=1` to `DEFAULT_WEBGPU_STUB_PROFILE`. CPU attribution only;
see the performance skill.

## Optional CPU profiling

Attach `@forgeax/engine-profiler` to the App or Renderer assembly when a bounded CPU artifact is
needed. The default is off: no profiler means no capture records or profiler-owned event objects.

```ts
import { createProfiler } from '@forgeax/engine/profiler';
import { createApp } from '@forgeax/engine/app';

const profiler = createProfiler();
const result = await createApp({ platform, renderer, world, profiler });
if (!result.ok) throw result.error;

const capture = profiler.startCapture({ frameLimit: 120, eventLimit: 1024 });
if (!capture.ok) throw capture.error;
// Drive the App, then call capture.value.finish() and validate the artifact.
```

Read `profiler.phaseCatalog` for the App/Render owner relation. Use
`validateProfileCapture` and `buildProfileModel` from the profiler package for offline analysis;
do not recreate phase lists or turn this capability into an ECS, GPU, UI, or RPC surface.

## Load timeline

Loading is recorded by default at negligible cost; nothing needs to be attached.
Mark game milestones with `markLoadTimeline('home-ready')` / `markLoadTimeline('map-ready')`
from `@forgeax/engine/app` in any realm, and read every realm with
`await collectLoadTimeline()` or `globalThis.__forgeaxLoadTimeline.collect()`.
Record kinds and limits: performance measurement.

## Render-owned evidence boundary

Render inspection and profiling are the evidence boundary. App exposes the
renderer `inspect` and `observe` projections and forwards the opt-in profiler;
it does not define a timing controller, timestamp vocabulary, or
membership-specific option.

`gpuPassTiming` is a transparent option projection to Runtime and Render. The
App does not admit the capability, own the `frameId`, create a timing session,
or own a `FrameReceipt`; it only keeps the existing realm and worker gate. The
Render route is `gpuPassTiming` opt-in -> `draw()` receipt ->
`observe(receipt, { include: ['timings'] })` -> status/code/hint. Membership
timing remains producer-specific and is not generic accepted evidence. Link to
the Render contract and validator before adding any new diagnostic surface.

## Renderer feature assembly

When a producer owns an optional render contribution, pass it through the
single renderer assembly seam. Game-author code uses the public umbrella
facades (`@forgeax/engine/<package-directory>`); the physical
`@forgeax/engine-*` names are repository ownership units for package source and
tests. `RenderFeature` and its `FrameData` type come from
`@forgeax/engine/render`; `createRenderer` comes from `@forgeax/engine/runtime`.

```ts
import { ok } from '@forgeax/engine/types';
import type { RenderFeature } from '@forgeax/engine/render';
import { createRenderer } from '@forgeax/engine/runtime';

type FrameData = { readonly visibleCount: number };
const feature = {
  identity: 'package.feature',
  extract: ({ owner }) => ok<FrameData>({ visibleCount: owner }),
  plan: (data, context) => {
    void data.visibleCount;
    void context;
    return ok({ resources: [], passes: [] });
  },
} satisfies RenderFeature<FrameData>;

const created = await createRenderer(canvas, { features: [feature] });
if (!created.ok) throw created.error;
const renderer = created.value;
```

`createApp(canvas, { outputColorSpace: 'display-p3' })` forwards the same option unchanged,
including under Worker execution. App owns no colour policy: read the negotiated result, or the
structured sRGB fallback, from `renderer.inspect().output.colorSpace` in the Renderer's realm.

### Declarative graphics and recovery

For a producer that needs graphics or compute, declare the work in its plan.
The public imports stay split by owner: `RenderFeature` and plan declarations
come from `@forgeax/engine/render`; `createRenderer` comes from
`@forgeax/engine/runtime`.

```ts
import { ok } from '@forgeax/engine/types';
import type { RenderFeature } from '@forgeax/engine/render';
import { createRenderer } from '@forgeax/engine/runtime';
interface PreparedFrame {
  readonly visibleCount: number;
}

const frame: PreparedFrame = { visibleCount: 0 };
const feature = {
  identity: 'package.prepared-feature',
  extract: () => ok(frame),
  plan: (_data, context) => {
    return ok({
      resources: [{
        kind: 'graphics-program',
        name: 'package.pipeline',
        program: {
          shader: 'package.shader',
          vertexLayout: 'package.vertices',
          colorFormats: [context.targets[0]?.format ?? 'rgba8unorm-srgb'],
          sampleCount: 1,
          topology: 'triangle-list',
        },
      }],
      passes: [],
    });
  },
} satisfies RenderFeature<PreparedFrame>;

const created = await createRenderer(canvas, { features: [feature] });
if (!created.ok) throw created.error;
const renderer = created.value;
```

The host derives opaque GPU resources and graph access from this declaration.
The producer owns extracted facts; it never receives a device, encoder, queue,
or submit callback.

Use `renderer.inspect()` and the single `renderer.subscribe()` stream as the
recovery surface. Branch on the closed `RenderError` code and read its
structured detail; do not parse console messages or import a private assembly
seam. Call `renderer.recover()` after device loss and treat `disposed` as
terminal. `renderer.dispose()` is idempotent.

For terminology and the public context boundary, use
[`@forgeax/engine/render`](../../packages/render/README.md) and its
[`declarative feature plan`](../../packages/render/src/features/plan.ts).
For the runtime host contract, use
[`packages/runtime/README.md`](../../packages/runtime/README.md). For code-first
GPU particles, use [`packages/vfx-render/README.md`](../../packages/vfx-render/README.md).

## Frame-loop contract

Each frame has one host-owned sequence:

```text
measured deltaSeconds -> world.update(deltaSeconds) -> renderer.draw({ leases, camera, environment })
```

`createApp` measures the delta once. A `World` owns time integration, fixed-step catch-up, and `Time` / `FixedTime` resources. Do not add a callback list, app-owned elapsed clock, app-side time clamp, or a second requestAnimationFrame loop.

The frame loop reports a failed world update or draw through `app.onError`. It does not swallow structured failures.

Native startup Hosts with screen UI return `null` from `drawSource` until the
existing root activation transaction commits. This submits UI-only pending frames
even after shader initialization. Return `undefined` to admit the primary scene,
and withdraw it on failure; do not infer readiness from Camera presence or opaque
UI pixels. The same App loop keeps World updates, UI, input, and Reload alive.

```ts
const stopListening = app.onError((error) => {
  console.error(error.code, error.hint);
});

const started = app.start();
if (!started.ok) console.error(started.error.code, started.error.hint);

// Later: stopListening(); app.stop();
```

## Time policy wiring

Canvas-form callers configure the new World at creation. The policy lives with the World, not with App.

```ts
const result = await createApp(canvas, {
  time: {
    fixedDeltaSeconds: 1 / 60,
    maxStepsPerUpdate: 4,
    maxDeltaSeconds: 0.1,
  },
});
```

`Time.delta` is the validated variable delta, `Time.elapsed` is its accumulated time, and `FixedTime` exposes the fixed delta, tick count, and truncation metrics. Read those resources in systems. `FixedTime.droppedSeconds` and `FixedTime.droppedUpdates` report a capped catch-up; they are not an invitation to restore an app-level clamp.

For the assemble form, the host creates the World first. Its existing policy is authoritative.

```ts
import { World } from '@forgeax/engine/ecs';
import { createApp } from '@forgeax/engine/app';

const world = new World({ time: { fixedDeltaSeconds: 1 / 120, maxStepsPerUpdate: 8 } });
const result = await createApp({ platform, renderer, world, plugins: [myPlugin] });
if (!result.ok) throw result.error;
result.value.start().unwrap();
```

## Callback deletion migration

The former `registerUpdate` callback surface is deleted. Convert each callback into a named `Update` system. The system reads time from the World and participates in schedule ordering.

```ts
import { Time, Update, defineSystem } from '@forgeax/engine/ecs';

const AnimateHud = defineSystem({
  name: 'animate-hud',
  queries: [],
  fn: (world) => {
    const elapsed = world.getResource(Time).elapsed;
    updateHud(Math.sin(elapsed));
  },
});

app.world.addSystem(Update, AnimateHud).unwrap();
```

For deterministic simulation, register the behavior on `FixedUpdate` instead. Use schedule edges or sets for ordering; never recreate an app callback queue.

```ts
import { FixedUpdate } from '@forgeax/engine/ecs';

app.world.addSystem(FixedUpdate, {
  name: 'step-combat',
  queries: [],
  fn: () => stepCombat(),
}).unwrap();
```

## Input and plugin wiring

For ordinary gamepad dual-rumble, read `feedbackTarget` and `dualRumble` from the
frozen gamepad reader, then use the optional `GamepadFeedback` World resource
under `GAMEPAD_FEEDBACK_KEY`. Poll its bounded results and branch on admission
capacity. Host input owns the actuator; App transports POD through existing
Worker frames. Read the [Input feedback contract](../../packages/input/README.md#gamepad-feedback)
for target fencing, replacement, cancellation and native timeout. API completion
does not establish physical vibration; acceptance needs a real controller.

The canvas form inserts the input backend and activates the input scan on `Update` before user systems. User systems read the frozen `InputSnapshot`; they do not install gameplay DOM listeners.

Pointer-lock FPS / mouse look (reference: `templates/game-3d/assets/camera/camera.pack.ts`):

- Gate from the Engine realm with `gameHost.setPointerLockAllowed(allowed)` (send it on
  change, e.g. `allowed = phase === 'playing'`). The Host requests the lock on the next
  trusted canvas click; gameplay never calls `requestPointerLock` or listens for DOM events.
- The gate defaults to allowed. A cursor game (top-down, RTS, tower defense, UI-driven)
  closes it once with `gameHost.setPointerLockAllowed(false)` in its plugin `apply`; the
  latest command is the effective state whenever the browser input backend is created,
  including during Worker startup and after canvas replacement.
- Consume `input.mouse.movementDelta` and fire buttons only while
  `input.mouse.pointerLocked`; the click that acquires the lock is not a shot. Clicks while
  locked keep the lock, so left-button fire is safe.
- Treat `pointerLocked` turning false (Esc, window blur, tab hide) as pause; resume
  needs a new click. Browsers refuse a relock shortly after a user Esc, so close the
  gate for about one second after a loss instead of relying on the refusal.
- A refusal is `app-pointer-lock-failed`, recoverable: the game keeps running unlocked
  and the next click retries. Never route it to a fatal handler.
- Desktop touch overlays (look pad, virtual stick) must not cover the canvas under the
  cursor, or they swallow the locking click; hide them unless the last pointer was touch.

```ts
import { INPUT_SNAPSHOT_RESOURCE_KEY, type InputSnapshot } from '@forgeax/engine/input';
import { Update, defineSystem } from '@forgeax/engine/ecs';

const ReadInput = defineSystem({
  name: 'read-input',
  queries: [],
  fn: (world) => {
    const input = world.getResource<InputSnapshot>(INPUT_SNAPSHOT_RESOURCE_KEY);
    if (input.keyboard.down('KeyW')) moveForward();
  },
});
app.world.addSystem(Update, ReadInput).unwrap();
```

Use `plugins` to compose optional capability packages such as physics and audio. These are native DeepSeek Cordis plugins: declare `inject`/`provide`, register every reversible side effect through `ctx.effect`, and let the App-owned `pluginContext` own their Fibers.

```ts
import type { Plugin } from '@forgeax/engine/plugin';

const gameplay: Plugin = {
  name: 'gameplay',
  inject: ['world'],
  apply(ctx) {
    ctx.effect(() => installGameplaySystems(ctx.world));
  },
};

const fiber = await app.pluginContext.plugin(gameplay);
await fiber.dispose();
await app.dispose();
```

`app.stop()` only stops frame scheduling. `app.dispose()` drains the Cordis realm and then releases simulation/Host/renderer ownership. An assemble-form host supplies its own World, renderer, input backend, and plugin set explicitly; the App still owns the Context it assembled around them.

## Boundaries

- `createApp` returns `Result`; handle `.ok`, `.error.code`, and `.error.hint` before starting.
- `createRenderer` is lower level. A host using it directly owns `world.update(deltaSeconds)` and `renderer.draw` itself.
- The app owns browser lifecycle and error fan-out; the World owns game scheduling and time.
- A demo that freezes after migration exposes an engine or schedule integration failure. Do not add a demo-side callback or manual loop workaround.

For exact option, Result, lifecycle, input, and renderer contracts, read `packages/app/README.md`, `packages/app/src/types.ts`, and `packages/app/src/internal/frame-loop.ts`.

## Simulation inspection

Pass already-created, ready simulation participants to `createApp`; App
registers them with the World and exposes one read-only inspection summary.
Use `app.simulationInspection()` for participant/readiness, baseline, trace,
report, tolerance, and structured error diagnostics. The schema is
`packages/app/schema/simulation-inspection.schema.json`.

App does not define record/schema/component state or restore policy. Preview and
Remote only consume the summary through existing read/eval paths. Do not add
restore/replay actions or transport raw World, Rapier, or Web Audio objects.

## Plugin asset authoring

Create functional Packs: export small native behaviors from the same file, and split
complex implementations into ordinary TypeScript modules. Follow the
[Plugin contract](../../packages/plugin/README.md): persistent definitions live in
Pack, and schema-v3 project `roots` select their GUIDs. Use `asset plugin inspect`
to check sourceKey and definitions, then inspect native Fiber state to confirm
activation. Verify a new session after code or configuration changes; engine and
frontend effects own scene and DOM cleanup respectively. For source reuse, read
`help asset source import` or `help asset source clone` and transfer the author closure.
