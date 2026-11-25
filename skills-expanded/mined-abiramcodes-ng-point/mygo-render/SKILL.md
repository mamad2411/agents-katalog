---
name: mygo-render
description: Make videos and frame sequences with the mygo render plugin (github.com/egoist/mygo/plugins/render). A Go composition builds each frame from native UI widgets, the GPU draws it, and the system encoder writes MP4, MOV, WebM, ProRes or PNG frames, with optional sound and no browser. Use this skill whenever the user asks for a launch video, promo clip, product demo video, animated captions, a changelog clip, wants UI recorded as video in Go, mentions mygo or the mygo render plugin, or asks for a short crisp video for a product.
metadata:
  internal: true
---

# mygo render

The render plugin turns Go code into finished videos. Each frame is a view built from
`package ui`'s widgets (text, boxes, real controls), the plugin draws the frames like a
window's — Metal on macOS, Direct3D 11 on Windows, OpenGL otherwise, or the CPU renderer
where no GPU one starts — and the system's encoder writes the file (AVFoundation on macOS,
Media Foundation on Windows, GStreamer on Linux; ffmpeg only if asked). No browser runs, no
cgo, no JavaScript. A 1920x1080 frame costs a millisecond or two of CPU while the GPU draws.

Requires Go 1.27+. Validated on go1.27.4 darwin/arm64 with mygo v0.10.0: a 90-frame 1280x720
MP4 rendered in 620 ms.

## Setup

```bash
mkdir demo && cd demo
go mod init demo
go get github.com/egoist/mygo/plugins/render
```

Or run this skill's `scripts/setup.sh <dir> [module-name]`. The `go get` pulls mygo,
purego and go-text/typesetting — nothing else, no C toolchain. Imports you need:

```go
import (
	"context"

	"github.com/egoist/mygo/plugins/render"
	"github.com/egoist/mygo/ui"
)
```

(`github.com/egoist/mygo` itself is only needed for the preview window, below.)

## A complete, validated program

```go
package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/egoist/mygo/plugins/render"
	"github.com/egoist/mygo/ui"
)

func main() {
	ink := ui.Hex("#0e0e13")
	amber := ui.Hex("#ffc53d")
	comp := render.Composition{
		Width: 1280, Height: 720, FPS: 30, Frames: 90, Scale: 2,
		Dark: true, Background: ink,
		View: func(c *ui.Context, f render.Frame) {
			ui.Column(c).Fill().AlignItems(ui.Center).Justify(ui.Center).Gap(18).Children(func() {
				in := f.Interpolate([]float64{0, 20}, []float64{0, 1})
				ui.Text(c, "ng-point").FontSize(96).Bold().LetterSpacing(-2).
					Opacity(float32(in))
				sub, _ := f.Shift(10, 0)
				ui.Text(c, "render plugin proof").FontSize(28).TextColor(amber).
					Opacity(float32(sub.Interpolate([]float64{0, 12}, []float64{0, 1})))
			})
		},
	}
	start := time.Now()
	err := render.Video(context.Background(), comp, "out.mp4", render.Options{})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("rendered out.mp4 in %v\n", time.Since(start).Round(time.Millisecond))
}
```

Write it as `main.go`, then `go run .`. This exact program produced a 90-frame MP4 in 620 ms.

## The mental model

The video is a `render.Composition` and its `View` is called once per frame with that
frame's number. Everything on screen is positioned inside container views; all motion is a
function of the frame index. Nothing else runs: no event loop, no window, no app.

## Composition fields

| Field | Meaning |
| --- | --- |
| `Width`, `Height` | Output pixels |
| `FPS` | 30 by default; 29.97 is `30000/1001` to encoders |
| `Frames` | Length of the video |
| `Scale` | Pixels per DIP. A 1920x1080 video at `Scale: 2` lays its view out in 960x540 DIPs, so text and widgets sit at their usual window sizes |
| `Dark`, `Background` | `Dark` builds the view as the desktop's dark appearance would; `Background` fills behind the view (the theme's background by default) |
| `View` | `func(c *ui.Context, f render.Frame)` — the whole video |

## Driving motion (render.Frame)

- `f.Index` — the frame's number.
- `f.Interpolate([]float64{from, to}, []float64{fromVal, toVal})` — a linear ramp between
  two frames; pass `render.Interpolation{Easing: ui.EaseOut}` (or `ui.EaseInOut`) to shape it.
- `f.Spring(ui.Bouncy.Spring)` / `ui.Snappy.Spring` — a spring from 0 to 1 over the
  sequence's frames; multiply into scales and offsets.
- `g, _ := f.Shift(n, 0)` — a frame view shifted by n frames, for staggered entrances.
- `f.Sequence(c, from, to, func(f render.Frame) { ... })` — scenes. `to == 0` means "until
  the last frame". Overlapping sequences cross-fade nicely by ramping opacity out at each
  scene's end.
- `f.Audio(pluck)` / `f.Audio(pluck, render.AudioOptions{Volume: 0.8})` — schedule a sound
  at the sequence's start.

## UI building blocks

Containers: `ui.Column`, `ui.Row` with `.Fill()`, `.AlignItems(ui.Center)`,
`.Justify(ui.Center)`, `.Gap(n)`, `.Padding(n)`, `.Padding(x, y)`, `.Width(n)`,
`.Radius(n)`, `.Background(color)`, `.Border(1, color)`, `.Shadow(0, 24, 60, 0, rgba)`,
`.Opacity(x)`, `.Translate(x, y)`, `.Children(func())`, and `ui.Spacer`.
Content: `ui.Text(c, "…")` with `.FontSize`, `.Bold()`, `.LetterSpacing(-2)`,
`.TextColor(color)`, `.Padding`, `.Radius`, `.Background`, plus real widgets —
`ui.Switch(c, &on)`, `ui.Slider(c, &level, 0, 1)`, `ui.Progress(c, done)`,
`ui.Button(c, "Cancel")`, `ui.PrimaryButton(c, "Render")`, `ui.Badge(c, "frame 42")`.
Colors: `ui.Hex("#0e0e13")`, `ui.RGBA(0, 0, 0, 0.5)`.

## Sound

A known-good starter, a plucked A4 with its octave:

```go
func newPluck() *render.Sound {
	const rate = 48000
	pcm := make([]float32, rate*6/10)
	for i := range pcm {
		t := float64(i) / rate
		env := math.Exp(-7*t) * min(t/0.004, 1)
		pcm[i] = float32(0.3 * env * (math.Sin(2*math.Pi*440*t) + 0.4*math.Sin(2*math.Pi*880*t)))
	}
	return render.SoundOf(rate, 1, pcm)
}
```

Schedule it inside a `f.Sequence` with `f.Audio(pluck)`.

## Rendering

- `render.Video(ctx, comp, "out.mp4", render.Options{})` — `.mp4`, `.m4v`, `.mov`, `.webm`.
- `render.Images(ctx, comp, "frames/%04d.png", o)` — every frame to PNG or JPEG, encoded on
  all cores while the next frames draw.
- `render.Still(comp, frame, o)` — one frame as `*image.RGBA`.
- `render.Frames(ctx, comp, o, fn)` — hands each frame to your own encoder.
- `render.Options`: `Renderer` (`render.Auto`, `render.GPU`, `render.CPU`), `Codec`
  (`render.H264`, `render.HEVC`, `render.ProRes`, `render.ProRes4444`, `render.VP9`),
  `Workers`, `Progress func(render.Progress)` (fields: `Done`, `Frames`, `Elapsed`,
  `Renderer`), and `Encoder: render.FFmpeg` when the system encoder is not wanted.
- The output file appears when the video is whole; until then frames go into a temporary
  file beside it, which a cancel or error removes.
- `context.Background()` works fine; canceling the context stops the render.

## Preview window (optional, while authoring)

`render.NewPlayer(comp)` returns a `*ui.VideoPlayer` you can show with
`ui.Video(c, player)` inside a normal mygo app (`mygo.App.WhenReady`,
`mygo.NewWindow`, `mygo.App.Run`) — controls to pause and seek, no sound. The official
example's `previewWindow` function is the full pattern; copy it from
https://github.com/egoist/mygo/examples/render/blob/main/main.go.

## References

- Official example (sound, scenes, widgets, preview): https://github.com/egoist/mygo/examples/render
- Plugin docs: https://mygo.run/docs/plugins/render
- Repo docs (same text, versioned with the code): docs/plugins/render.md in egoist/mygo

## Gotchas

- `Scale` is DIPs, not a zoom: keep it 2 for Retina-like sizing so text lands at the sizes
  a window would show.
- Sequence bounds are frames, not seconds: `FPS: 30`, a scene from frame 0 to 75 is 2.5 s.
- **Inside `f.Sequence(c, from, count)`, `f.Index` is LOCAL (`f.Index - from`) and the third
  argument is a frame COUNT, not an end frame** (0 or less means "to the end"). Absolute
  timeline math silently never fires — re-anchor with `idx := f.Index + from`. Verified the
  hard way: a first render drew only background and music.
- Sequences stack as layers: later ones draw above earlier ones, and the layer keeps its
  layout (empty) while not showing.
- **`MotionBlur` only blurs clock-driven motion** (`f.Interpolate`, `f.Spring`, `f.Exact`,
  `Seconds`); plain `f.Index` math does not blur. Drive anything that should streak with
  `f.Interpolate(..., render.Interpolation{Easing: ui.EaseInOut})`. `Samples` 5-12,
  `Shutter` up to 360; each sample is a full draw, so 12 samples render ~12x slower.
- `f.Audio(sound)` streams the sound **per frame it is called in**, advancing through the
  sound's samples in sync with the composition clock — call it once per frame in the root
  view (or any full-span sequence) to play a baked track exactly once. With motion blur
  only the last sample pass's audio counts, so nothing overlaps.
- The View runs for every frame, so build everything inside it; nothing persists between
  calls except what you close over.
- No cgo: any machine compiles for any platform; macOS signing of the *output* is not a
  concern because the output is a video file, not an app.
