---
name: mobile-ui
description: Native mobile UI/UX craftsmanship, responsive adaptive layouts (iOS horizontalSizeClass, Android WindowSizeClass, foldables), kinetic spring motion, and tactile engineering for SwiftUI, Jetpack Compose, React Native, and Flutter.
---

# Mobile UI/UX, Responsive Layouts & Native Motion (`/mobile-ui`)

> **Philosophy**: *Adapt every screen from active window bounds (`Compact`/`Medium`/`Expanded`), replace linear curves with harmonic springs, respect safe areas and 200% text scaling, and keep touch targets ergonomic.*

---

## 1. Progressive Disclosure References & Playbook

| Resource | Purpose |
| :--- | :--- |
| [references/responsive-adaptive-layouts.md](references/responsive-adaptive-layouts.md) | Unified iOS & Android breakpoints, `AnyLayout`/`ViewThatFits`/`NavigationSplitView`, `WindowSizeClass`/`NavigationSuiteScaffold`/`ListDetailPaneScaffold`, foldable hinges, RN/Flutter parity. |
| [references/apple-hig-and-material3.md](references/apple-hig-and-material3.md) | `44pt`/`48dp` touch bounds, safe areas & `imePadding()`, `200%` Dynamic Type scaling, dark/light surface tokens. |
| [references/native-motion-and-gestures.md](references/native-motion-and-gestures.md) | Harmonic springs, `matchedGeometryEffect`, `SharedTransitionLayout`, `PredictiveBackHandler`, Reanimated 3, Impeller, haptics. |
| [scripts/verify_mobile_ui_hygiene.py](scripts/verify_mobile_ui_hygiene.py) | Audits hardcoded widths, linear easing, missing safe areas, `UIScreen.main.bounds`/`Dimensions.get` traps, fixed text heights, and portrait locks. |

> **Agent Execution Playbook**: Follow [`skills/darknecrostack/playbooks/mobile-responsive.md`](../darknecrostack/playbooks/mobile-responsive.md) when building or reviewing responsive iOS/Android layouts.

---

## 2. iOS & Android Responsive Breakpoint Matrix

| Class | Width | iOS (SwiftUI) | Android (Compose M3 Adaptive) | Cross-Platform (RN / Flutter) |
| :--- | :--- | :--- | :--- | :--- |
| **Compact** | `< 600 dp/pt` | `.compact` + bottom `TabView` | `WindowWidthSizeClass.COMPACT` + `NavigationBar` | `useWindowDimensions()` / `LayoutBuilder` 1-col |
| **Medium** | `600–839 dp/pt` | `AnyLayout` 2-col + `ViewThatFits` | `MEDIUM` + `NavigationRail` + `FoldingFeature` | 2-col adaptive grid (`min 160–200`) |
| **Expanded** | `>= 840 dp/pt` | `NavigationSplitView` + `maxWidth: 700` | `EXPANDED` + `ListDetailPaneScaffold` + `widthIn(680.dp)` | Permanent drawer + multi-pane split |

---

## 3. Core Native Craftsmanship Invariants

1. **Active Window Bounds Only**: Size from `horizontalSizeClass` / `WindowSizeClass` / `useWindowDimensions()` / `MediaQuery.sizeOf(context)`—ban `UIScreen.main.bounds`, module-scope `Dimensions.get`, fixed phone widths (`375`–`430`), and portrait locks.
2. **Safe Areas & 200% Font Scaling**: Wrap root content in `.safeAreaInset` / `WindowInsets.systemBars` + `Modifier.imePadding()`, and use `minHeight`/`heightIn(min=)` so `200%` Dynamic Type never clips text.
3. **Ergonomic Touch & Spring Motion**: Enforce `>= 44x44 pt` (iOS) / `>= 48x48 dp` (Android) hit bounds in the bottom `60%` thumb arc; ban `.linear` animations in favor of calibrated springs (`response: 0.32s, dampingFraction: 0.72`) and detent haptics.

---

## 4. Automated Mobile Hygiene Verification

```bash
python3 skills/mobile-ui/scripts/verify_mobile_ui_hygiene.py --path .
```
