---
name: reactiive
description: React Native animation craft. Patterns for Reanimated, Gesture Handler, and Skia that make mobile interfaces feel alive. Use when building gestures, transitions, or any motion in React Native.
---

# React Native Animation Craft

## Initial Response

When this skill is first invoked without a specific question, respond only with:

> I'm ready to help you build animations that feel right.

Do not provide any other information until the user asks a question.

---

## The Recipe

Every animation needs three ingredients. Miss any and things will crash.

```tsx
// 1. A shared value that lives on the UI thread
const scale = useSharedValue(1);

// 2. An animated style that reads from it
const rStyle = useAnimatedStyle(() => ({
  transform: [{ scale: scale.get() }],
}));

// 3. An Animated.View that renders it
<Animated.View style={[styles.square, rStyle]} />
```

The shared value holds the data. The animated style transforms it into properties. The Animated.View renders it.

Once you get this, everything else is just variations.

**Note:** Use `.get()` and `.set()` instead of `.value` for React Compiler compatibility.

---

## The Four Hooks

| Hook | Purpose |
| --- | --- |
| **useSharedValue** | Create a value on the UI thread |
| **useAnimatedStyle** | Turn shared values into styles |
| **useDerivedValue** | Compute new values from existing ones |
| **useAnimatedReaction** | Trigger side effects when values change |

**useDerivedValue** is my favorite — it's going to be extremely important.

---

## useDerivedValue

Define a new shared value that **automatically recomputes** based on other shared values.

```tsx
const isDragging = useSharedValue(false);

const rotate = useDerivedValue(() => {
  return withSpring(isDragging.get() ? '45deg' : '0deg');
});

const scale = useDerivedValue(() => {
  return withSpring(isDragging.get() ? 0.9 : 1);
});
```

The magic: wrap the return value with animation functions. When isDragging changes, the derived values animate smoothly.

### Chaining Derived Values

```tsx
const color = useDerivedValue(() => {
  if (isDragging.get()) return '#0099ff';
  if (translateY.get() < 0) return 'black';
  if (translateY.get() > 0) return 'white';
  return '#0099ff';
});

const animatedColor = useDerivedValue(() => {
  return withTiming(color.get());
});
```

Chain them. The color derives from state. The animatedColor adds animation. Clean and declarative.

---

## useAnimatedReaction

Like useEffect for the UI thread. It watches a shared value and fires a callback when it changes.

```tsx
useAnimatedReaction(
  () => left.get(),
  (curr, prev) => {
    if (curr !== prev && curr !== 0) {
      cancelAnimation(scale);
      scale.set(0);
      scale.set(withSpring(1, { mass: 0.5 }));
    }
  },
);
```

The check for `curr !== 0` prevents firing on mount. Cancel any running animation before starting a new one.

---

## Common Mistakes

### Transform Order

The order of transforms matters. Scale before translate multiplies your translation.

```tsx
// ✗ Wrong: translateX of 50 becomes 50 * 1.5 = 75
transform: [
  { scale: 1.5 },
  { translateX: 50 },
]

// ✓ Correct: translate first, then scale
transform: [
  { translateX: translateX.get() },
  { translateY: translateY.get() },
  { scale: scale.get() },
  { rotate: rotate.get() },
]
```

### Array Index Keys

Using array indices as keys breaks layout animations.

```tsx
// ✗ Wrong: indices shift when items change
{items.map((item, index) => (
  <Animated.View key={index} layout={LinearTransition} />
))}

// ✓ Correct: stable unique IDs
{items.map((item) => (
  <Animated.View key={item.id} layout={LinearTransition} />
))}
```

### iOS Bounce

Scroll views bounce past their bounds on iOS. Without clamping, your interpolations break.

```tsx
import { clamp } from 'react-native-reanimated';

// Raw progress can go negative or exceed 1
const rawProgress = offset / maxOffset;

// Clamped progress stays valid
progress.set(clamp(rawProgress, 0, 1));
```

### Timing for Transforms

Timing animations on transforms feel robotic. Use springs.

```tsx
// ✗ Mechanical
scale.set(withTiming(1.2, { duration: 300 }));

// ✓ Natural
scale.set(withSpring(1.2));
```

### Missing Velocity

When ending gestures, pass the velocity. Without it, the animation feels disconnected.

```tsx
.onFinalize((event) => {
  translateX.set(withSpring(0, {
    velocity: event.velocityX,
  }));
});
```

---

## Springs

Springs feel natural because they simulate physics. Real objects don't move with fixed durations.

### The dampingRatio

**My range: 0.95 - 1.** Stay here for professional UI.

| dampingRatio | Behavior |
| --- | --- |
| **0.95 - 1** | Critically damped — no overshoot |
| **< 0.95** | Underdamped — intentionally bouncy |
| **> 1** | Overdamped — sluggish, avoid |

```tsx
// Default: clean, professional
scale.set(withSpring(1, { dampingRatio: 1 }));

// Slightly softer feel
translateY.set(withSpring(0, { dampingRatio: 0.95 }));
```

### When to Use What

| Animation Type | Use |
| --- | --- |
| Transforms (scale, translate, rotate) | `withSpring` |
| Static properties (opacity, colors) | `withTiming` + easing |

```tsx
// ✓ Transforms: springs
scale.set(withSpring(1.1));

// ✓ Opacity: timing
opacity.set(withTiming(1, { duration: 200 }));
```

---

## The Context Pattern

Pan gestures jump back to start on new touches. The solution: save position at gesture begin.

```tsx
const translateX = useSharedValue(0);
const context = useSharedValue({ x: 0 });

const panGesture = Gesture.Pan()
  .onBegin(() => {
    context.set({ x: translateX.get() });
  })
  .onUpdate((event) => {
    translateX.set(event.translationX + context.get().x);
  });
```

---

## Touch Feedback with pressto

Every tap needs feedback. pressto provides animated touchables that feel right.

```tsx
import { PressableScale } from 'pressto';

<PressableScale onPress={handlePress}>
  <View style={styles.button}>
    <Text>Tap me</Text>
  </View>
</PressableScale>
```

### Global Haptics

```tsx
import { PressablesConfig } from 'pressto';
import * as Haptics from 'expo-haptics';

<PressablesConfig
  globalHandlers={{
    onPress: () => Haptics.selectionAsync(),
  }}
>
  {children}
</PressablesConfig>
```

---

## Layout Animations

The easiest way to animate mount/unmount.

```tsx
import Animated, { FadeIn, FadeOut, LinearTransition } from 'react-native-reanimated';

{isVisible && (
  <Animated.View
    entering={FadeIn.duration(300)}
    exiting={FadeOut.duration(200)}
    layout={LinearTransition.springify()}
  />
)}
```

Exiting animations are hard to build manually. Reanimated handles the delay, animation, and unmount automatically.

### LinearTransition.springify()

```tsx
// Snappy
LinearTransition.springify().mass(0.3).damping(20).stiffness(250)

// Smooth
LinearTransition.springify().mass(1).damping(20).stiffness(120)
```

---

## Shared Transitions

Navigate between screens while an element morphs between them.

```tsx
import { Image } from 'expo-image';
import Animated from 'react-native-reanimated';

const AnimatedImage = Animated.createAnimatedComponent(Image);

// Home screen
<AnimatedImage
  source={{ uri: item.url }}
  sharedTransitionTag={`image-${item.id}`}
  style={{ width: 100, height: 100 }}
/>

// Detail screen - same tag
<AnimatedImage
  source={{ uri: item.url }}
  sharedTransitionTag={`image-${item.id}`}
  style={{ width: '100%', aspectRatio: 1 }}
/>
```

Use `containedTransparentModal` presentation for the detail screen.

---

## The Magic Button

This is what a memorable animation looks like. Scale, rotating gradient, blur — all on tap.

```tsx
const isTouched = useSharedValue(false);

const scale = useDerivedValue(() => {
  return withSpring(isTouched.get() ? 1.2 : 1);
});

const rotate = useDerivedValue(() => {
  return withTiming(isTouched.get() ? Math.PI * 2 : 0, { duration: 1000 });
});

<Canvas style={{ width: realWidth, height: realHeight }}>
  <Group origin={vec(centerX, centerY)} transform={[{ rotate: rotate.get() }]}>
    <RoundedRect x={realX} y={realY} width={width} height={height} r={width / 2}>
      <SweepGradient c={center} colors={['cyan', 'magenta', 'yellow', 'cyan']} />
      <BlurMask blur={20} style="solid" />
    </RoundedRect>
  </Group>
</Canvas>
```

**Functional animations** confirm touches. **Memorable animations** surprise. The magic button does both.

---

## Functional vs Memorable

Functional animations are what the user expects. Tap a button, get feedback. They're essential — without them, the app feels broken. But they don't make users remember your app.

Memorable animations are what the user doesn't expect. A gradient that glows and rotates. A 3D flip. These animations surprise.

Build the functional first. Then add the memorable.

---

## Philosophy

### Every Animation Needs a Job

| Job | Animation |
| --- | --- |
| Confirm touch | Scale down on press |
| Show connection | Morph card into detail |
| Direct attention | Fade in from trigger direction |
| Maintain orientation | Shared element between screens |
| Indicate progress | Pulse or shimmer |

If you can't name the job, delete the animation.

### Match Intensity to Frequency

The more often something happens, the more subtle it should be.

```tsx
// Happens constantly: clean, no bounce
const buttonScale = withSpring(pressed ? 0.97 : 1, {
  dampingRatio: 1,
});
```

### Pick Constraints Early

- Three spring configs for the whole app
- Scale and opacity only for touch feedback
- One easing curve for all timing animations

Decisions made once, applied everywhere. The app feels cohesive because it is.

---

## Reference Files

- [springs.md](springs.md) - Physics, dampingRatio, velocity
- [easings.md](easings.md) - Curves for opacity and colors
- [gestures.md](gestures.md) - Pan, tap, context pattern, pressto
- [scroll-animations.md](scroll-animations.md) - Parallax, progress, interpolate
- [skia-patterns.md](skia-patterns.md) - Canvas, shaders, paths, blur
- [sequences.md](sequences.md) - Layout animations, keyframes, stagger
- [text-animations.md](text-animations.md) - ReText, AnimateableText, Skia Text
- [worklets.md](worklets.md) - Threading, scheduleOnRN
- [design-engineering.md](design-engineering.md) - Philosophy, craft

---

#### Resources

- [Reanimated Docs](https://docs.swmansion.com/react-native-reanimated/)
- [React Native Skia](https://shopify.github.io/react-native-skia/)
- [pressto](https://github.com/nicksenger/pressto) - Animated touchables
- [Redash](https://wcandillon.gitbook.io/redash) - ReText, utilities
- [AnimateableText](https://github.com/axelra-ag/react-native-animateable-text) - Shared value text
