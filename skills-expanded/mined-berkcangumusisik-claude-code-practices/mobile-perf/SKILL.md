---
name: mobile-perf
description: Audits React Native app for performance issues - FlatList, re-renders, bridge calls
argument-hint: [file-or-directory]
user-invocable: true
allowed-tools: Read Grep Glob
effort: medium
---

## React Native Performance Audit

Target: **$1** (or `src/` if not specified)

### 1. List Rendering
```bash
grep -rn "map.*return\|\.map(" ${1:-src/} --include="*.tsx" | grep -v "test\|spec" | head -20
```
- Plain `map()` in JSX for lists > 10 items → should use `FlatList`
- `FlatList` without `keyExtractor`
- `FlatList` without `getItemLayout` for fixed-height items (prevents scroll optimization)
- Missing `removeClippedSubviews` for long lists

### 2. Re-render Detection
```bash
grep -rn "useState\|useSelector\|useContext" ${1:-src/} --include="*.tsx" | head -20
```
- Context consumers re-rendering when unrelated state changes
- Inline object/array props (`style={{ margin: 10 }}` recreated every render)
- Missing `React.memo` on list items
- Missing `useCallback` on functions passed as props

### 3. Native Bridge Calls
- Animated values: using JS-driven vs native-driven (`useNativeDriver: true`)
- Missing `InteractionManager.runAfterInteractions` for post-navigation heavy work
- Synchronous native modules called in render

### 4. Images
- Missing `resizeMode` and explicit dimensions
- Not using `FastImage` for remote images
- Missing progressive loading for large images

Report with severity and code fix for each finding.
