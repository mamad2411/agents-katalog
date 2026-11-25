---
name: forgeax-engine-audio
description: >-
  ForgeAX realm-neutral ECS audio with Host-owned playback. Use when playing BGM/SFX,
  wiring spatial listeners or buses, transporting Worker audio, or diagnosing decode and cleanup.
---

# forgeax-engine-audio

> **Gameplay owns `AudioSource`; the Host owns `AudioContext`.** `@forgeax/engine-audio` produces the same closed audio intents in every execution tier. `@forgeax/engine-audio-webaudio` consumes them in the Host realm.

## Takeoff

```ts
import { createApp } from '@forgeax/engine-app';
import { webAudioPlugin } from '@forgeax/engine-audio-webaudio';
import {
  AUDIO_ENGINE_RESOURCE_KEY,
  AudioListener,
  AudioSource,
  audioPlugin,
  type AudioBackend,
  type AudioClipAsset,
} from '@forgeax/engine-audio';

const created = await createApp(canvas, { plugins: [webAudioPlugin(), audioPlugin()] });
if (!created.ok) throw created.error;
const app = created.value;

const loaded = await app.renderer.assets.load(clipGuid, 'audio');
if (!loaded.ok) throw loaded.error;
const clip = loaded.value;

app.world.spawn({
  component: AudioSource,
  data: {
    clip,
    playing: true,
    loop: true,
    volume: 0.8,
    spatialBlend: 0,
    bus: 'music',
  },
}).unwrap();

const backend = app.world.getResource<AudioBackend>(AUDIO_ENGINE_RESOURCE_KEY);
backend.setBusVolume('music', 0.3);
app.start().unwrap();
```

Attach `Transform` to spatial `AudioSource` entities and `AudioListener` to the camera entity. Scene propagation supplies the emitter position and normalized local -Z direction; changed poses reach pending decode and paused panners through the same POD path. Configure `coneInnerAngle`, `coneOuterAngle` and `coneOuterGain` on the source for directional gain. Without a source transform, spatial playback uses the origin and -Z. The plugin runs listener sync after transform propagation and sends position, forward, and up as nine numeric scalars.

## Realm contract

| Owner | Data | Rule |
|:--|:--|:--|
| ECS World | `AudioSource`, `AudioListener`, playing edges, source and listener pose | Realm-neutral gameplay authority |
| Engine Worker | `createAudioIntentBackend()` and a per-frame intent batch | No Web Audio objects; first play carries bounded bytes or a stream index, later plays reuse the owner/handle/revision publication |
| Host | `createHostAudioConsumer()` and `WebAudioEngine` | Owns decode cache, `AudioBuffer`, nodes, buses, gesture resume, and `AudioContext` |
| Kernel Worker | Nothing | Audio is never a Shared Kernel concern |

`main-serial`, `engine-worker`, and `shared` use the same `audioPlugin()` and intent vocabulary. The App report projects Host state at `app.execution.report().audio`. Worker queries observe the last admitted Host snapshot; before feedback they report `unavailable` and a null active count. Do not diagnose autoplay from an unavailable observation. Host audio listens for the first gesture before lazy context creation; borrowed contexts retain caller ownership. Validate gesture ordering with trusted browser input, and qualify autoplay-policy behavior without a permissive autoplay launch override.

## Components and controls

| Surface | Purpose |
|:--|:--|
| `AudioSource.playing` | False-to-true plays; true-to-false stops. Toggle false before replaying a one-shot. |
| `AudioSource.paused` / `playbackRate` | Retain position while paused; positive speed multiplier also changes pitch |
| `AudioSource.fromPosition` / `AudioBackend.seek(entityId, seconds)` | Start at decoded clip seconds; edits seek once; explicit backend seek supports repeated identical requests and pending decode |
| `AudioSource.loop` / `volume` / `bus` | Source playback and accepted bus-ID routing |
| `AudioSource.coneInnerAngle` / `coneOuterAngle` / `coneOuterGain` | Full cone angles in degrees and outer gain; sampled on play, default omnidirectional |
| `AudioSource.spatialBlend` | `0` routes directly to the bus; values above `0` create a panner |
| `AudioListener` | Marker on the first listener entity whose world transform drives pose |
| `AcousticRegion` | Saved box/sphere: highest-priority normalized source routes and separate first-listener wet/send overlay; configure existing bus/effect references first. Read the Audio contract for local blend units, capacity and recovery. |
| `AudioBackend` | Source volume, bus volume/mute, state, active count, and destroy |

## Clip and async safety

`AudioClipAsset` is POD: buffered bytes or a validated PCM16 stream descriptor. Playback takes the asset owner and handle; the owner supplies its revision. The Host caches by owner/handle/revision, keeping `sourceKey` as provenance. Each play and music preparation uses fixed content; edits affect subsequent plays without invalidating existing voices. Stop, entity replacement and disposal fence pending decode. Preserve Host publication rejection feedback when implementing a custom transport so replay can republish rejected bytes.

Set Host cache budgets with `createHostAudioConsumer(engine, options)` when the defaults do not fit the project; units and rejection behavior are defined in `packages/audio-webaudio/README.md`. Bus settings apply even before the first context is created.

Inspect decode or context-resume failure through `backend.getState().lastError` or `app.execution.report().audio.lastError`. Consume `.code`, `.expected`, `.hint`, and `.detail`; do not parse the message.

For an inaudible sound, first prove that the intended actor actually triggers a playing edge and owns a valid clip. Then inspect Host context/error state, source lifetime, bus/mute/volume, emitter/listener poses and distance attenuation. Test an isolated source before overlapping gunfire, and compare listener orientations with the same source position. A loaded asset, active-source count or zero console errors does not prove audible output.

## Cleanup

`app.stop()` only stops frame scheduling. `app.dispose()` drains the Cordis realm and disposes the Host consumer exactly once: stop sources, disconnect nodes, clear source and pending-play maps, remove gesture listeners, and close the context. A poisoned World does not keep producing intents. Explicit Worker rebuild creates a fresh Host consumer so old async decode tasks cannot affect the new World identity.

## Sources of truth

| Contract | Owner |
|:--|:--|
| Components, plugin, intent union, tick, backend protocol | [`packages/audio/README.md`](../../packages/audio/README.md) |
| Host decode/cache/node implementation | [`packages/audio-webaudio/README.md`](../../packages/audio-webaudio/README.md) |
| App execution selection and report | [`forgeax-engine-app`](../forgeax-engine-app/SKILL.md) |
| Asset GUID loading | [`forgeax-engine-assets`](../forgeax-engine-assets/SKILL.md) |

## Simulation participant

Use the realm-neutral audio participant for portable intent/state evidence. ECS
owns `record`, `restore`, fixed-tick `trace`, semantic `report`, numeric
`tolerance`, and closed `error` values. The Host consumer still owns
`AudioContext`, `AudioBuffer`, source nodes, and cleanup.

Expose only the inspection summary through App, Preview, or Remote. Diagnose by
`code`/`expected`/`hint`/`detail`, then retry with a fresh target. This is not an
RHI tape or game replay surface.

## Host filter and spectrum controls

Use `webAudioPlugin(engine)` with one Host `WebAudioEngine` for native user filters and opt-in frequency analysis. After decode, `setFilters` owns an ordered chain; `createAnalyser` admits the FFT size and `readFrequencyData` writes dB into a reused caller buffer, including silence while paused. These native controls stay on the Host. Read [the package contract](../../packages/audio-webaudio/README.md#source-controls-and-spectrum) for ownership, bounds, failure and borrowed-context rules.

## Configure buses and long audio

Declare one acyclic parent/send graph with `AudioBackend.configureBuses`, then route source `bus` IDs through it. Install shared native chains on the Host with `WebAudioEngine.setBusEffects`; read its Result and the backend state before accepting the graph. Use source Meta `importSettings.playback: 'stream'` for supported PCM16 WAV and load the ordinary GUID. Verify Range hosting, `getStreamState` and `AudioState.streaming`; a play request or active-source count alone is not output evidence. Follow [the Host contract](../../packages/audio-webaudio/README.md#long-audio-through-source-meta-and-guid) for bounds, formats and recovery.

For execution bootstrap apps, install the shared Host graph through `execution.createHostAudio`; return a fresh consumer per rebuild. Keep `audioPlugin()` in the gameplay bootstrap and follow [the assembly contract](../../packages/audio-webaudio/README.md#app-host-effect-assembly).

## Quantized layered music

Save a bounded `MusicScore` with BPM, meter, loop beats and ordinary buffered clip
GUIDs. Resolve it with public `loadMusicScore`, then call
`consumer.prepareMusic(requestId, preparedScore)` in the Host audio factory. Each
rebuild prepares its fresh consumer. Gameplay sends complete stem gain vectors
through `AudioBackend.music` at a beat or bar boundary and consumes
`AudioState.music.receipts`; a scheduled receipt means native admission, while an
applied receipt observes the common Context target. Worker commands carry only
POD controls. They cannot prepare encoded bytes or native buffers.

Use the returned epoch for subsequent mix/cancel/pause/resume/tempo controls.
Late requests explicitly reject or move to the next boundary. Tempo changes
preserve beat phase and change pitch; streaming stems and time stretching are
unsupported. Read the [Audio music contract](../../packages/audio/README.md#quantized-layered-music)
and [Host transport contract](../../packages/audio-webaudio/README.md#native-musical-transport)
for bounds, target receipts, lifecycle and ordinary public examples. Do not create
a second Context, clock or per-stem game timer.
