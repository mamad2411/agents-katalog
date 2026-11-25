---
name: react-native-performance
description: Finds and fixes janky lists, wasted re-renders and chatty bridge calls in a React Native app, measuring before and after each change.
---

# React Native performance

Measure first. Never optimize on a debug build or in the simulator alone.

## Steps

1. Name the symptom and the screen. Build in release mode (`npx react-native run-android --mode release` or the Xcode Release scheme) and note the baseline: frame rate from the perf monitor, or a React Profiler recording of the interaction.
2. Lists first. For FlatList or SectionList check: a stable `keyExtractor` (never the array index for reorderable data), `getItemLayout` for fixed-height rows, `windowSize` and `maxToRenderPerBatch` tuned down, `removeClippedSubviews` on Android, and row components wrapped in `React.memo` with stable props. Consider FlashList when rows vary and the list is long.
3. Re-renders. Use the Profiler to find components that render without a prop change. Fix the cause: inline objects and arrow functions passed as props, a context whose value changes every render, state kept too high in the tree. Reach for `useMemo` and `useCallback` only where a memoized child receives the value.
4. Bridge and JS thread. Look for loops that call native modules per item, `JSON.parse` of large payloads on the JS thread, and animations that use `setState`. Batch native calls, move animations to Reanimated worklets or `useNativeDriver: true`, and defer heavy work with `InteractionManager.runAfterInteractions`.
5. Images. Require explicit width and height, resize on the server, and use a caching image component.
6. Startup. Check bundle size, Hermes enabled, and imports that run work at module load. Use inline requires for rarely used screens.
7. Re-measure after each single change and keep it only if the number improves.

## Rules

- One change per measurement.
- Do not add `useMemo` everywhere. Unmeasured memoization is noise.
- Never remove accessibility props to save render time.

## Report

Baseline and final numbers, each change kept with file and line, and changes reverted because they did not help.
