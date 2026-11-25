---
name: rn-skia
description: >
  React Native Skia (@shopify/react-native-skia) complete best practices, GPU-accelerated 2D graphics,
  60fps/120fps animation patterns, custom shaders, and production optimization for iOS and Android.
  Use when writing, reviewing, fixing, or optimizing React Native Skia code including Canvas rendering,
  shapes, paths, gradients, filters, text/fonts, images, video, Skottie/Lottie, particle systems,
  or custom SkSL shaders. Triggers on tasks involving @shopify/react-native-skia, Canvas, Circle,
  Rect, Path, Group, useImage, useFont, LinearGradient, RadialGradient, RuntimeShader, Blur,
  BlurMask, Shadow, Atlas, Picture, Skia.Paint, Skia.Path, useDerivedValue with Skia, interpolateColors,
  usePathInterpolation, useRSXformBuffer, BackdropBlur, ImageShader, FractalNoise, Turbulence,
  Paragraph, TextPath, TextBlob, Skottie, AnimatedImage, drawAsImage, immediate mode vs retained mode,
  or any Skia-based drawing/animation. Also triggers when the user asks to build charts, drawing
  canvases, progress rings, particle effects, frosted glass, neon glow, image filters, or other
  GPU-accelerated graphics with React Native Skia.
---

# React Native Skia — Best Practices & Performance Guide

> @shopify/react-native-skia 2.x / React Native >= 0.79 / React >= 19 / Reanimated v3+

## Critical Rules

1. **Never read `.value` in JSX render** — pass shared values directly as props: `<Circle cx={x} />` not `<Circle cx={x.value} />`.
2. **Never create Skia objects in render** — use `useMemo` for Paint, Path, PictureRecorder, RuntimeEffect.
3. **Always mark worklet functions** with `"worklet"` directive in `useDerivedValue` callbacks.
4. **Animate properties, not structure** — keep the component tree static; only animate numeric/color props.
5. **Use Atlas for 10+ similar elements** — single draw call beats N individual components.
6. **Reuse Paint and PictureRecorder objects** — creating per frame causes GC pressure and frame drops.
7. **Prefer retained mode** for UI animations (near-zero FFI cost); use immediate mode (Picture API) only for variable draw command counts (particles, generative art, games).
8. **Use BlurMask over Blur** for simple shapes — it's cheaper.
9. **Order filters cheapest-first** — MatrixColorFilter before Blur.
10. **Load fonts/images at component level** with `useFont`/`useImage` — handle null loading state before rendering.

## Version Compatibility

| React Native Skia | React Native | React | iOS    | Android      |
|-------------------|-------------|-------|--------|--------------|
| 2.x               | >= 0.79     | >= 19 | >= 14  | API >= 21    |
| 1.12.4            | <= 0.78     | <= 18 | >= 14  | API >= 21    |

Android API 26+ required for video support.

## Installation

```bash
npm install @shopify/react-native-skia
# Postinstall downloads prebuilt Skia binaries — must run
# Bun: bun add --trust @shopify/react-native-skia
# pnpm v10+: add to pnpm.onlyBuiltDependencies in package.json
```

iOS: `cd ios && pod install`. Android ProGuard: add `-keep class com.shopify.reactnative.skia.** { *; }`.

## Essential Imports

```tsx
import {
  Canvas, Circle, Rect, RoundedRect, Line, Path, Group, Fill,
  Text, Paragraph, Image, ImageSVG,
  LinearGradient, RadialGradient, SweepGradient,
  Blur, BlurMask, Shadow, BackdropBlur, MatrixColorFilter,
  RuntimeShader, FractalNoise, Turbulence, ImageShader,
  Atlas, Picture, Vertices, Patch, DiffRect, FitBox, Box,
  useFont, useImage, useSVG, useCanvasRef,
  Skia, vec, rect, rrect, drawAsImage,
  usePathInterpolation, useRSXformBuffer, useRectBuffer, useClock,
  interpolateColors,
} from "@shopify/react-native-skia";

import {
  useSharedValue, useDerivedValue, withTiming, withSpring,
  withRepeat, withSequence, withDelay, withDecay, cancelAnimation,
} from "react-native-reanimated";
```

## Core Pattern — Retained Mode Animation

```tsx
const x = useSharedValue(0);
const scale = useSharedValue(1);

useEffect(() => {
  x.value = withSpring(200);
  scale.value = withSpring(1.5);
}, []);

return (
  <Canvas style={{ flex: 1 }}>
    <Group transform={[{ translateX: x }, { scale }]}>
      <Circle cx={0} cy={100} r={50} color="cyan" />
    </Group>
  </Canvas>
);
```

## Rendering Mode Selection

| Scenario            | Mode      | Why                                  |
|---------------------|-----------|--------------------------------------|
| UI animations       | Retained  | Near-zero FFI, display list cached   |
| Charts & graphs     | Retained  | Static structure, animated props     |
| Particle systems    | Immediate | Variable draw command count          |
| Games               | Immediate | Full control per frame               |
| Generative art      | Immediate | Unpredictable scene changes          |
| Mixed               | Both      | Picture for particles + Group for UI |

## Performance Quick Reference

```
Fastest (use freely):      Circle, Rect, Line, Group transforms, MatrixColorFilter
Fast (use moderately):     Path (simple), BlurMask, LinearGradient
Slow (use sparingly):      BackdropBlur, RuntimeShader, DisplacementMap, Blur (large radius)
```

**Targets**: 60fps = 16.67ms budget, 120fps = 8.33ms budget. Memory < 100MB. JS thread < 50%.

## Anti-Patterns to Fix on Sight

| Anti-Pattern | Fix |
|---|---|
| `cx={x.value}` in JSX | `cx={x}` — pass shared value directly |
| `Skia.Paint()` in render body | Wrap in `useMemo(() => Skia.Paint(), [])` |
| `Skia.Path.Make()` in render body | Wrap in `useMemo` |
| `{items.map(i => <Circle .../>)}` for 10+ items | Use `Atlas` with `useRSXformBuffer` |
| `<Blur blur={0} />` | Remove — no-op filter wastes cycles |
| Dynamic component list changing every frame | Use immediate mode (Picture API) |
| `useState` driving Skia animations | Use `useSharedValue` |
| Missing `"worklet"` in `useDerivedValue` | Add directive as first statement |
| Font/image not null-checked | Guard with `if (!font) return null` |
| `<BackdropBlur>` wrapping large areas | Limit clip area or use `BlurMask` |

## Code Review Action

When asked to review/audit/check Skia code:

1. **Scan** all files importing `@shopify/react-native-skia`.
2. **Check** against Critical Rules and Anti-Patterns table.
3. **Report** in table: `| File | Line | Issue | Severity | Fix |`
4. **Severity**: CRITICAL (crash/broken render), HIGH (frame drops), MEDIUM (sub-optimal), LOW (style).
5. **Fix** all issues if confirmed, then re-scan to verify zero violations.

## Reference Files

Read these as needed for detailed API docs, examples, and patterns:

- **[Getting Started](references/getting-started.md)**: Installation (npm/yarn/Expo/Bun/pnpm), platform setup (iOS/Android/Web), postinstall scripts, Hello World, Canvas component, Skia object API, project structure, troubleshooting build errors, bundle size.
- **[Canvas & Rendering Modes](references/canvas-rendering.md)**: Retained mode (declarative components, display list, near-zero FFI), immediate mode (Picture API, PictureRecorder, direct draw commands), combining both modes, offscreen/headless rendering, canvas snapshots, custom renderers, platform considerations.
- **[Shapes & Drawing](references/shapes-drawing.md)**: All shape components (Circle, Rect, RoundedRect, Oval, Line, Points, Fill, Path with SVG notation, Atlas/RSXform sprite batching, Vertices, Patch, DiffRect), Group transforms/blend modes/clipping, Paint component, FitBox, Box with shadow, path trimming animation.
- **[Animations](references/animations.md)**: Reanimated v3 integration (shared values as direct props), animation types (timing/spring/decay/repeat/sequence), derived values, Skia hooks (usePathInterpolation, usePathValue, useClock, useRectBuffer, useRSXformBuffer), color animations (interpolateColors), gesture integration (pan/pinch/rotation/multi-touch), complete examples (pulsing button, spinner, bouncing ball).
- **[Shaders & Gradients](references/shaders-gradients.md)**: Linear/Radial/Sweep/TwoPointConical gradients, animated gradients, FractalNoise/Turbulence, custom SkSL runtime shaders (wave distortion, chromatic aberration, glow, aurora, water ripple), ShaderLib functions, ImageShader texturing, shader composition, performance (half precision, cache programs).
- **[Filters & Effects](references/filters-effects.md)**: Image filters (Blur, Offset, Morphology, DisplacementMap, Shadow, RuntimeShader), mask filters (BlurMask styles: normal/solid/outer/inner), color filters (MatrixColorFilter with grayscale/sepia/invert/brightness/contrast matrices, BlendColor, LumaColorFilter, Lerp), path effects (Discrete, Dash, Corner, Path1D, Path2D, Line2D, Sum), BackdropBlur/BackdropFilter, Mask (alpha/luminance), frosted glass/neon glow/vintage photo examples.
- **[Text & Fonts](references/text-fonts.md)**: Text component (baseline positioning), useFont hook, system fonts, matchFont, Paragraph builder (rich text, styles, alignment), TextPath (text along curves), TextBlob, Glyphs, font metrics/measurement, animated text (position, font size), marquee/typewriter/shadow examples.
- **[Images & Media](references/images-media.md)**: useImage hook (require/URL/bundle), Image component (fit modes, sampling), programmatic image creation (base64, raw pixels, drawAsImage), image manipulation (resize, encode, read pixels), AnimatedImage (GIF/WebP), SVG (useSVG, ImageSVG, from string), Video playback (useVideo, controls), Skottie/Lottie (animation, dynamic properties, slots), canvas snapshots, image effects.
- **[Performance Optimization](references/performance.md)**: Rendering pipeline (JS→UI→GPU), 60fps/120fps frame budgets, retained vs immediate mode characteristics, animation performance (shared values, derived values, batching, worklets), component structure optimization (flat trees, Groups, static Pictures), memory management (reuse objects, dispose images, resize), Atlas for high-perf rendering, filter cost hierarchy, platform-specific tips (iOS Metal, Android OpenGL/androidWarmup, Web CanvasKit), profiling (useFrameCallback FPS counter, React DevTools, native profilers), common pitfalls checklist.
- **[Advanced Patterns](references/advanced-patterns.md)**: Architecture (component composition, DrawingContext, atomic/molecular components, custom hooks, render props), real-world examples (interactive bar chart, particle system with Atlas, drawing canvas with gestures, progress ring, waveform visualizer), design system integration (theme provider with Skia colors), testing (unit tests, visual regression), debugging (visual grid overlay, performance monitor), common patterns (skeleton loading, ripple effect, confetti).
