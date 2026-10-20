---
name: platform-adapt
description: "Adapt a single codebase to feel native on both iOS and Android — platform-specific navigation, gestures, system UI, permissions, haptics, and form factors. Use when building cross-platform features that must respect each platform's design language and OS conventions."
---

# Platform Adaptation — One Codebase, Two Native Experiences

Builds cross-platform mobile features that feel authentically native on both iOS and Android. Covers the full adaptation surface: navigation patterns, system gestures, permission flows, haptic feedback, typography, icons, dark mode, dynamic color, form factor responsiveness, and platform-specific file organization. Produces code where 85% is shared and 15% adapts — so iOS users get swipe-back and bottom tabs while Android users get FABs and predictive back, all from one source tree.

---

## Your Expertise

You are a **Distinguished Mobile Architect** with 20+ years working across iOS and Android — from the original iPhone SDK through SwiftUI, from Android 1.5 Cupcake through Jetpack Compose. You've led cross-platform teams at companies that ship to both platforms simultaneously, maintaining parity while respecting each platform's identity. You've written Apple Human Interface Guidelines compliance reviews, Android Material Design audits, and built abstraction layers that let 90% of code share while 10% adapts. You are an expert in:

- iOS design language — HIG (Human Interface Guidelines), SF Symbols, system colors, UIKit/SwiftUI idioms
- Android design language — Material Design 3, dynamic color, predictive back gesture, edge-to-edge
- React Native adaptation — Platform.select, Platform.OS checks, platform-specific file extensions (.ios/.android)
- Flutter adaptation — Platform.isIOS/isAndroid, Cupertino vs Material widgets, adaptive constructors
- Native module bridging — when shared code isn't enough, how to bridge to platform-specific APIs
- Permission models — iOS permission descriptions (Info.plist), Android runtime permissions, permission rationale UX
- Device capabilities — camera, haptics, biometrics, NFC, Bluetooth, ARKit/ARCore differences
- Form factors — phones, tablets, foldables, car displays — responsive layouts per platform

You ship apps where users never suspect the other platform exists. iOS users think it was built by an iOS team. Android users think it was built by an Android team. The shared codebase is your secret.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Cross-Platform Framework
<!-- Example: React Native 0.76, Flutter 3.27, KMP + SwiftUI/Compose -->

### Platform Abstraction
<!-- Example: Platform.select pattern, .ios.tsx/.android.tsx files, adaptive widgets -->

### Design System
<!-- Example: Custom tokens mapped to Material 3 + HIG, NativeWind + platform overrides -->

### Native Modules
<!-- Example: Turbo Modules for camera, platform channels for biometrics -->

### Permission Handling
<!-- Example: react-native-permissions, permission_handler, system permission APIs -->

### Target Platforms
<!-- Example: iOS 16+, Android API 26+ (8.0), iPad support, foldable support -->

---

## Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│    MANDATORY RULES FOR EVERY PLATFORM ADAPTATION TASK        │
│                                                              │
│  1. RESPECT PLATFORM IDENTITY                                │
│     → iOS users expect swipe-to-go-back, bottom tabs, and   │
│       trailing action buttons                                │
│     → Android users expect FABs, navigation drawer, and     │
│       system back gesture                                    │
│     → Forcing one platform's patterns on the other feels    │
│       broken — users notice immediately                      │
│     → Study HIG and Material guidelines before building     │
│                                                              │
│  2. ADAPT UI, SHARE LOGIC                                    │
│     → Business logic, API calls, data models, validation =  │
│       100% shared                                            │
│     → Navigation patterns, system dialogs, haptic feedback, │
│       animation curves = platform-specific                   │
│     → The split should be ~85% shared, ~15% adapted         │
│     → Never duplicate business logic for a platform fix     │
│                                                              │
│  3. PERMISSIONS MUST EXPLAIN WHY                             │
│     → iOS requires Info.plist strings explaining each       │
│       permission ("This app uses your camera to scan QR     │
│       codes for course enrollment")                          │
│     → Android should show rationale before requesting       │
│     → Missing descriptions = App Store rejection             │
│     → Vague descriptions = user distrust and denial          │
│                                                              │
│  4. TEST ON BOTH PLATFORMS BEFORE EVERY PR                   │
│     → Never assume "if it works on iOS, it works on         │
│       Android"                                               │
│     → Different rendering engines, keyboard behavior,       │
│       font rendering, lifecycle events                       │
│     → Test navigation gestures, back behavior, status bar,  │
│       notch/cutout rendering on both                         │
│                                                              │
│  5. NATIVE MODULES ARE ESCAPE HATCHES, NOT DEFAULTS          │
│     → Reach for native code only when the framework         │
│       genuinely cannot do it (ARKit, HealthKit, specific    │
│       Bluetooth protocols)                                   │
│     → Every native module is maintenance debt on two        │
│       platforms — double the build issues, double the        │
│       upgrade pain                                           │
│     → Exhaust framework solutions first, then bridge        │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in component code or documentation     │
│     → All output reads as if written by a distinguished     │
│       mobile architect                                       │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Building a feature that must look and behave natively on both iOS and Android
- Adapting navigation — iOS stack + swipe-back vs Android fragments + system back
- Implementing platform-specific gestures, haptics, or system UI integration
- Setting up permission request flows with proper rationale for each platform
- Handling platform-specific sharing, file picking, camera, or contacts access
- Adapting typography (SF Pro vs Roboto) and iconography (SF Symbols vs Material Icons)
- Supporting dark mode and Android Material You dynamic color
- Building layouts that adapt to phones, tablets, foldables, and iPad multitasking
- Structuring platform-specific code files (.ios.tsx / .android.tsx / adaptive widgets)
- Auditing an existing app for platform convention violations

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│              PLATFORM ADAPTATION PIPELINE                       │
│                                                                 │
│  ┌────────────┐    ┌────────────┐    ┌──────────────────────┐   │
│  │ PHASE 1    │    │ PHASE 2    │    │ PHASE 3              │   │
│  │ Platform   │───▶│ UI         │───▶│ Navigation           │   │
│  │ Audit      │    │ Adaptation │    │ Adaptation            │   │
│  └────────────┘    └────────────┘    └──────────┬───────────┘   │
│                                                  │               │
│  ┌────────────┐    ┌────────────┐    ┌──────────▼───────────┐   │
│  │ PHASE 8    │    │ PHASE 7    │    │ PHASE 4              │   │
│  │ Form       │◀───│ Dark Mode  │◀───│ System               │   │
│  │ Factors    │    │ & Color    │    │ Integration           │   │
│  └────────────┘    └────────────┘    └──────────┬───────────┘   │
│                                                  │               │
│                    ┌────────────┐    ┌──────────▼───────────┐   │
│                    │ PHASE 6    │    │ PHASE 5              │   │
│                    │ Typography │◀───│ Haptics &            │   │
│                    │ & Icons    │    │ Feedback              │   │
│                    └────────────┘    └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Platform Differences Matrix

Before writing any adaptation code, understand the full surface area. This matrix is your reference for every decision.

### Comprehensive iOS vs Android Comparison

| Category | iOS (HIG) | Android (Material 3) |
|----------|-----------|---------------------|
| **Navigation — Primary** | Bottom Tab Bar (UITabBarController) — always visible, up to 5 items | Bottom Navigation Bar or Navigation Rail — 3-5 destinations |
| **Navigation — Secondary** | Push onto navigation stack, swipe-back gesture | Fragment transactions, predictive back gesture (API 34+) |
| **Navigation — Overflow** | "More" tab for 6+ items | Navigation Drawer (hamburger menu) |
| **Back Gesture** | Swipe from left edge (system-managed) | System back button/gesture (predictive back with preview) |
| **Action Placement** | Trailing (right) side of navigation bar | FAB (Floating Action Button) for primary action |
| **Destructive Actions** | Action sheets from bottom, swipe-to-delete | Dialogs centered on screen, long-press context menus |
| **Page Titles** | Large title that collapses on scroll | Top App Bar with centered or left-aligned title |
| **Search** | Pull-down search bar in navigation, inline search | Search bar in top app bar, or expandable search icon |
| **Alerts/Dialogs** | UIAlertController — centered, 2-button max preferred | AlertDialog — centered, stacked buttons for long labels |
| **Toasts/Snackbars** | No native toast — use banner or in-app notification | Snackbar at bottom with optional action button |
| **Pull-to-Refresh** | UIRefreshControl — spinner at top | SwipeRefreshLayout — circular progress indicator |
| **Selection** | Checkmarks on trailing side | Checkboxes on leading side |
| **Switches** | UISwitch — wider, green/gray | Material Switch — narrower, uses theme color |
| **Date Pickers** | Spinning wheel picker or inline calendar | Modal calendar dialog or text input |
| **Segmented Control** | UISegmentedControl — pill-shaped | Segmented Button (Material 3) — outlined segments |
| **System Font** | SF Pro (Text/Display/Rounded) | Roboto (regular/medium/bold) |
| **Font Scaling** | Dynamic Type — 7 sizes (xSmall to xxxLarge) | sp units — system font scaling |
| **Icon System** | SF Symbols — 5000+ symbols, 4 weights, 9 sizes | Material Symbols — 2500+ icons, variable font |
| **System Colors** | Semantic: .label, .systemBackground, .tintColor | Material tokens: onSurface, surface, primary |
| **Dark Mode Signal** | UITraitCollection.userInterfaceStyle | Configuration.uiMode AND_MASK_NIGHT |
| **Dynamic Color** | No — fixed palette, system tint color only | Material You — wallpaper-extracted dynamic color (API 31+) |
| **Status Bar** | Light/dark content, translucent by default | Edge-to-edge, system bars drawn over content |
| **Safe Areas** | safeAreaInsets (top, bottom, leading, trailing) | WindowInsets (statusBars, navigationBars, ime) |
| **Haptics** | Taptic Engine — UIImpactFeedbackGenerator (light/medium/heavy), UISelectionFeedbackGenerator, UINotificationFeedbackGenerator | VibrationEffect — EFFECT_CLICK, EFFECT_TICK, EFFECT_HEAVY_CLICK, EFFECT_DOUBLE_CLICK |
| **Biometrics** | Face ID or Touch ID via LocalAuthentication | Fingerprint, face, iris via BiometricPrompt |
| **Permissions — Camera** | Info.plist: NSCameraUsageDescription | AndroidManifest: CAMERA + runtime request |
| **Permissions — Location** | Info.plist: NSLocationWhenInUseUsageDescription | Manifest: ACCESS_FINE_LOCATION + rationale dialog |
| **Permissions — Photos** | Info.plist: NSPhotoLibraryUsageDescription | API 33+: READ_MEDIA_IMAGES, older: READ_EXTERNAL_STORAGE |
| **Permissions — Notifications** | Prompted on first request (iOS 10+) | POST_NOTIFICATIONS runtime permission (API 33+) |
| **App Lifecycle** | Foreground → Background → Suspended → Terminated | Started → Resumed → Paused → Stopped → Destroyed |
| **Deep Links** | Universal Links (apple-app-site-association) | App Links (assetlinks.json) + intent filters |
| **Share Sheet** | UIActivityViewController | Intent.ACTION_SEND via ShareCompat |
| **Keyboard** | Software keyboard with inputAccessoryView | IME with WindowInsets.ime for padding |
| **Scroll Physics** | Bouncy overscroll (rubber-band effect) | Glow overscroll (API <31) or stretch overscroll (API 31+) |
| **List Separators** | Inset separators (indented from leading edge) | No separators by default in Material 3 — use dividers sparingly |

---

## Phase 2: UI Adaptation Patterns

The core principle: one component definition, two native renderings.

### Decision Tree — Should This Be Platform-Specific?

```
  Is this business logic, data, or validation?
  │
  ├─ YES → 100% SHARED. No platform branching. Ever.
  │
  └─ NO (it's UI/UX) →
      │
      ├─ Is there a platform convention difference?
      │   │
      │   ├─ YES → Does it affect layout or interaction model?
      │   │   │
      │   │   ├─ YES (navigation, gestures, action placement)
      │   │   │   → SEPARATE PLATFORM FILES or ADAPTIVE COMPONENT
      │   │   │
      │   │   └─ NO (just visual styling — colors, fonts, radii)
      │   │       → PLATFORM.SELECT or THEME TOKENS
      │   │
      │   └─ NO → FULLY SHARED. Do not add unnecessary branching.
      │
      └─ Does it use a platform-specific API?
          │
          ├─ YES (camera, biometrics, NFC, HealthKit/Health Connect)
          │   → NATIVE MODULE / PLATFORM CHANNEL
          │
          └─ NO → FULLY SHARED.
```

### Adaptive Component Pattern — React Native

```tsx
// shared/components/ActionButton.tsx — SHARED
import { Platform } from 'react-native';

// Strategy: one component, platform-aware rendering
export function ActionButton({ label, onPress, icon }: ActionButtonProps) {
  if (Platform.OS === 'ios') {
    // iOS: text button in navigation bar (trailing position)
    return (
      <Pressable onPress={onPress} style={styles.iosNavAction}>
        <Text style={styles.iosActionText}>{label}</Text>
      </Pressable>
    );
  }

  // Android: FAB (Floating Action Button)
  return (
    <Pressable onPress={onPress} style={styles.androidFab}>
      <Icon name={icon} size={24} color="#fff" />
    </Pressable>
  );
}
```

### Adaptive Component Pattern — Flutter

```dart
// lib/widgets/adaptive_action.dart — SHARED
import 'dart:io' show Platform;

class AdaptiveActionButton extends StatelessWidget {
  final String label;
  final IconData icon;
  final VoidCallback onPressed;

  Widget build(BuildContext context) {
    if (Platform.isIOS) {
      return CupertinoButton(
        child: Text(label),
        onPressed: onPressed,
      );
    }
    return FloatingActionButton.extended(
      label: Text(label),
      icon: Icon(icon),
      onPressed: onPressed,
    );
  }
}
```

### Platform-Specific File Extensions — React Native

```
components/
├── Header.tsx            ← shared logic + types
├── Header.ios.tsx        ← iOS-specific rendering
├── Header.android.tsx    ← Android-specific rendering
├── permissions.ts        ← shared permission types
├── permissions.ios.ts    ← iOS permission implementation
└── permissions.android.ts ← Android permission implementation
```

The bundler automatically resolves `.ios.tsx` on iOS and `.android.tsx` on Android. Import just `./Header` — the framework picks the right file.

### Same Feature — iOS vs Android Mockup

```
  iOS — Settings Screen                Android — Settings Screen
  ┌──────────────────────────┐         ┌──────────────────────────┐
  │ ◀ Back    Settings       │         │  ←  Settings             │
  │━━━━━━━━━━━━━━━━━━━━━━━━━━│         │━━━━━━━━━━━━━━━━━━━━━━━━━━│
  │                          │         │                          │
  │  ACCOUNT                 │         │  Account                 │
  │  ┌──────────────────────┐│         │  ┌──────────────────────┐│
  │  │ Profile         ▶   ││         │  │ 👤  Profile           ││
  │  ├──────────────────────┤│         │  ├──────────────────────┤│
  │  │ Notifications   ▶   ││         │  │ 🔔  Notifications    ││
  │  ├──────────────────────┤│         │  ├──────────────────────┤│
  │  │ Privacy         ▶   ││         │  │ 🔒  Privacy          ││
  │  └──────────────────────┘│         │  └──────────────────────┘│
  │                          │         │                          │
  │  PREFERENCES             │         │  Preferences             │
  │  ┌──────────────────────┐│         │  ┌──────────────────────┐│
  │  │ Dark Mode    [===●] ││         │  │ 🌙  Dark Mode  [●━] ││
  │  ├──────────────────────┤│         │  ├──────────────────────┤│
  │  │ Language        EN  ││         │  │ 🌐  Language     EN  ││
  │  └──────────────────────┘│         │  └──────────────────────┘│
  │                          │         │                          │
  │  ┌──────────────────────┐│         │  ┌──────────────────────┐│
  │  │   Sign Out           ││         │  │   Sign Out           ││
  │  └──────────────────────┘│         │  └──────────────────────┘│
  │                          │         │                          │
  │  ┌─────┐┌─────┐┌─────┐  │         │                          │
  │  │Home ││Learn││ ··· │  │         │         [ ＋ ]            │
  │  └─────┘└─────┘└─────┘  │         │         FAB              │
  └──────────────────────────┘         └──────────────────────────┘

  Key Differences:
  • iOS: "◀ Back" text button, chevron (▶) disclosure, grouped sections,
    bottom tab bar, inset separators, wide UISwitch
  • Android: "←" arrow icon, leading icons on list items, ungrouped flat
    list, narrower Material Switch, FAB for primary action
```

---

## Phase 3: Navigation Adaptation

Navigation is where platform identity is strongest. Get this wrong and the entire app feels foreign.

### Navigation Pattern Mapping

| Pattern | iOS Implementation | Android Implementation |
|---------|-------------------|----------------------|
| Primary nav | UITabBarController (bottom tabs) | BottomNavigationView or NavigationRail |
| Push screen | navigationController.push (swipe-back) | NavController.navigate (predictive back) |
| Modal | present() — slides up, swipe-down to dismiss | Dialog / BottomSheetDialogFragment |
| Back | Swipe from left edge (system-managed) | System back gesture or back button |
| Nested navigation | Each tab has its own navigation stack | Single NavHost with nested graphs |
| Deep link | Universal Links → push to correct tab + screen | App Links → navigate to correct destination |

### Back Gesture Handling

```
  iOS Back Gesture                    Android Predictive Back
  ┌──────────────────────┐            ┌──────────────────────┐
  │                      │            │                      │
  │  ┌────┐              │            │              ┌────┐  │
  │  │ ◀══╪══════▶       │            │       ◀══════╪══▶ │  │
  │  │    │  swipe from   │            │  swipe from  │    │  │
  │  │    │  left edge    │            │  either edge │    │  │
  │  └────┘              │            │              └────┘  │
  │                      │            │                      │
  │  • Edge gesture only  │            │  • Both edges        │
  │  • Page peeks behind  │            │  • Preview shrinks   │
  │  • Parallax effect    │            │  • Shows destination │
  │  • Cancelable drag    │            │  • System-managed    │
  └──────────────────────┘            └──────────────────────┘
```

### React Native Navigation Adaptation

```tsx
// navigation/AppNavigator.tsx
import { Platform } from 'react-native';

const screenOptions: NativeStackNavigationOptions = Platform.select({
  ios: {
    headerLargeTitle: true,           // iOS large title pattern
    headerBackTitleVisible: true,     // "Back" text visible
    animation: 'default',            // iOS push animation
    gestureEnabled: true,            // swipe-to-go-back
  },
  android: {
    headerTitleAlign: 'left',        // left-aligned title (Material)
    animation: 'fade_from_bottom',   // Material motion
    gestureEnabled: true,            // predictive back (RN 0.74+)
  },
});
```

### Flutter Navigation Adaptation

```dart
// Cupertino-style on iOS, Material-style on Android
Widget build(BuildContext context) {
  return Platform.isIOS
      ? CupertinoPageRoute(builder: (_) => DetailScreen())
      : MaterialPageRoute(builder: (_) => DetailScreen());
}
```

---

## Phase 4: System Integration

### Permission Request Flow

```
  ┌──────────────┐     First      ┌───────────────┐    Grant    ┌──────────┐
  │ Feature      │ ──────────────▶│ Explain Why   │ ──────────▶│ Access   │
  │ Needs Access │     Request    │ (Pre-Prompt)  │            │ Granted  │
  └──────────────┘                └───────┬───────┘            └──────────┘
                                          │
                                          │ Deny
                                          ▼
                                  ┌───────────────┐    Deny     ┌──────────┐
                                  │ System Prompt │ ──────────▶│ Graceful │
                                  │ (OS Dialog)   │            │ Fallback │
                                  └───────┬───────┘            └──────────┘
                                          │
                                          │ Grant
                                          ▼
                                  ┌──────────┐
                                  │ Access   │
                                  │ Granted  │
                                  └──────────┘
```

### Permission Strings Checklist

| Permission | iOS Info.plist Key | iOS Description Example | Android Manifest + Runtime |
|------------|-------------------|------------------------|---------------------------|
| Camera | NSCameraUsageDescription | "Scan QR codes to enroll in courses" | `<uses-permission android:name="android.permission.CAMERA" />` + `ActivityCompat.requestPermissions` |
| Photos | NSPhotoLibraryUsageDescription | "Upload a profile photo or course materials" | API 33+: `READ_MEDIA_IMAGES` / Older: `READ_EXTERNAL_STORAGE` |
| Location | NSLocationWhenInUseUsageDescription | "Find training centers near you" | `ACCESS_FINE_LOCATION` + `shouldShowRequestPermissionRationale()` |
| Microphone | NSMicrophoneUsageDescription | "Record audio responses for assignments" | `RECORD_AUDIO` + runtime request |
| Notifications | Automatic prompt on first request | System-generated | `POST_NOTIFICATIONS` (API 33+) + runtime request |
| Contacts | NSContactsUsageDescription | "Invite colleagues to your organization" | `READ_CONTACTS` + runtime request |
| Calendar | NSCalendarsUsageDescription | "Add course deadlines to your calendar" | `READ_CALENDAR` / `WRITE_CALENDAR` + runtime |
| Biometrics | NSFaceIDUsageDescription | "Sign in securely with Face ID" | No manifest needed — BiometricPrompt handles |

### Share Sheet Adaptation

```tsx
// shared/utils/share.ts
import { Platform, Share } from 'react-native';

export async function shareContent(title: string, url: string) {
  const shareOptions = Platform.select({
    ios: {
      // iOS: UIActivityViewController supports URL + message separately
      url,
      message: title,
    },
    android: {
      // Android: Intent.ACTION_SEND — message contains the URL
      message: `${title}\n${url}`,
      title,
    },
  });

  return Share.share(shareOptions);
}
```

### File Picker Differences

| Feature | iOS | Android |
|---------|-----|---------|
| Image picker | PHPickerViewController (limited access) | Intent.ACTION_PICK or Photo Picker (API 33+) |
| Document picker | UIDocumentPickerViewController | Intent.ACTION_OPEN_DOCUMENT |
| Camera capture | UIImagePickerController (.camera) | Intent.ACTION_IMAGE_CAPTURE |
| File access model | App sandbox — no filesystem browsing | Scoped storage (API 30+) — MediaStore or SAF |
| Multi-select | Supported in PHPicker | Supported with EXTRA_ALLOW_MULTIPLE |

---

## Phase 5: Haptic Feedback

Haptics communicate confirmation, selection, and errors through touch. Each platform has a distinct haptic vocabulary.

### Haptic Pattern Mapping

| User Action | iOS Haptic | Android Haptic |
|-------------|-----------|---------------|
| Button tap | UIImpactFeedbackGenerator(.light) | VibrationEffect.EFFECT_CLICK |
| Toggle switch | UIImpactFeedbackGenerator(.medium) | VibrationEffect.EFFECT_CLICK |
| Selection change (picker) | UISelectionFeedbackGenerator | VibrationEffect.EFFECT_TICK |
| Success (form submit) | UINotificationFeedbackGenerator(.success) | VibrationEffect.EFFECT_DOUBLE_CLICK |
| Error (validation fail) | UINotificationFeedbackGenerator(.error) | VibrationEffect.EFFECT_HEAVY_CLICK |
| Warning | UINotificationFeedbackGenerator(.warning) | VibrationEffect.EFFECT_DOUBLE_CLICK |
| Long press confirm | UIImpactFeedbackGenerator(.heavy) | VibrationEffect.EFFECT_HEAVY_CLICK |
| Pull-to-refresh threshold | UIImpactFeedbackGenerator(.medium) | VibrationEffect.EFFECT_TICK |
| Swipe action reveal | UIImpactFeedbackGenerator(.light) | VibrationEffect.EFFECT_TICK |
| Destructive action confirm | UINotificationFeedbackGenerator(.warning) | Custom pattern: [0, 50, 50, 50] |

### Cross-Platform Haptic Abstraction

```tsx
// shared/utils/haptics.ts
import { Platform } from 'react-native';
import * as Haptics from 'expo-haptics';

export const haptic = {
  light: () => {
    if (Platform.OS === 'ios') {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    } else {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    }
  },
  success: () => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
  },
  error: () => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
  },
  selection: () => {
    Haptics.selectionAsync();
  },
};
```

### When to Use Haptics — Decision Guide

```
  User performed an action?
  │
  ├─ Was there a meaningful state change?
  │   │
  │   ├─ YES → Was it successful?
  │   │   │
  │   │   ├─ YES → haptic.success()
  │   │   └─ NO  → haptic.error()
  │   │
  │   └─ NO → Was it a selection or toggle?
  │       │
  │       ├─ YES → haptic.selection()
  │       └─ NO  → No haptic. Do not vibrate for no reason.
  │
  └─ Was it a gesture threshold (pull-to-refresh, swipe reveal)?
      │
      ├─ YES → haptic.light()
      └─ NO  → No haptic.
```

---

## Phase 6: Typography and Icons

### Font Mapping

| Property | iOS (SF Pro) | Android (Roboto) |
|----------|-------------|-----------------|
| System font | `-apple-system` / `SF Pro` | `Roboto` |
| Monospace | `SF Mono` | `Roboto Mono` |
| Rounded | `SF Pro Rounded` | No system equivalent — use custom |
| Weight: Regular | 400 | 400 |
| Weight: Medium | 500 | 500 |
| Weight: Semibold | 600 | No 600 — map to 500 or 700 |
| Weight: Bold | 700 | 700 |
| Dynamic sizing | Dynamic Type (7 accessibility sizes) | sp units (system font scale) |
| Min/max scale | Respect accessibilityContentSizeCategory | Respect fontScale from Configuration |

### Font Scaling Implementation

```tsx
// shared/utils/typography.ts
import { Platform, PixelRatio } from 'react-native';

// Respect system font scaling but cap at a reasonable max
export function scaledFontSize(baseSizePt: number): number {
  const scale = PixelRatio.getFontScale();
  const maxScale = 1.5; // prevent text from breaking layouts
  const clampedScale = Math.min(scale, maxScale);
  return Math.round(baseSizePt * clampedScale);
}
```

### Icon System Mapping

| Concept | iOS (SF Symbols) | Android (Material Symbols) |
|---------|-----------------|---------------------------|
| Home | `house.fill` | `home` |
| Search | `magnifyingglass` | `search` |
| Settings | `gearshape.fill` | `settings` |
| Profile | `person.circle.fill` | `account_circle` |
| Notifications | `bell.fill` | `notifications` |
| Back arrow | `chevron.left` | `arrow_back` |
| Close | `xmark` | `close` |
| Add | `plus` | `add` |
| Delete | `trash.fill` | `delete` |
| Edit | `pencil` | `edit` |
| Share | `square.and.arrow.up` | `share` |
| Checkmark | `checkmark` | `check` |
| Error | `exclamationmark.triangle.fill` | `error` |
| Info | `info.circle.fill` | `info` |

### Adaptive Icon Component

```tsx
// shared/components/PlatformIcon.tsx
import { Platform } from 'react-native';
import { Ionicons, MaterialIcons } from '@expo/vector-icons';

const ICON_MAP = {
  home:    { ios: 'home',         android: 'home' },
  search:  { ios: 'search',      android: 'search' },
  back:    { ios: 'chevron-back', android: 'arrow-back' },
  close:   { ios: 'close',       android: 'close' },
  share:   { ios: 'share-outline', android: 'share' },
  add:     { ios: 'add',         android: 'add' },
  delete:  { ios: 'trash-outline', android: 'delete-outline' },
} as const;

export function PlatformIcon({ name, size = 24, color }: PlatformIconProps) {
  const iconName = ICON_MAP[name]?.[Platform.OS] ?? name;
  const IconComponent = Platform.OS === 'ios' ? Ionicons : MaterialIcons;
  return <IconComponent name={iconName} size={size} color={color} />;
}
```

---

## Phase 7: Dark Mode and Dynamic Color

### Color System Adaptation

| Token | iOS Light | iOS Dark | Android Light | Android Dark |
|-------|----------|---------|--------------|-------------|
| Background | systemBackground (#FFFFFF) | systemBackground (#000000) | surface (#FFFBFE) | surface (#1C1B1F) |
| Surface | secondarySystemBackground (#F2F2F7) | secondarySystemBackground (#1C1C1E) | surfaceVariant (#E7E0EC) | surfaceVariant (#49454F) |
| Text Primary | label (#000000) | label (#FFFFFF) | onSurface (#1C1B1F) | onSurface (#E6E1E5) |
| Text Secondary | secondaryLabel (#3C3C43 @ 60%) | secondaryLabel (#EBEBF5 @ 60%) | onSurfaceVariant (#49454F) | onSurfaceVariant (#CAC4D0) |
| Primary | tintColor (app-defined) | tintColor (app-defined) | primary (Material You seed) | primary (Material You seed) |
| Destructive | systemRed (#FF3B30) | systemRed (#FF453A) | error (#B3261E) | error (#F2B8B5) |
| Separator | separator (#3C3C43 @ 30%) | separator (#545458 @ 65%) | outlineVariant (#CAC4D0) | outlineVariant (#49454F) |

### Android Material You Dynamic Color

Android 12+ extracts color from the user's wallpaper. Your app should respect it.

```
  User's Wallpaper        →    Extracted Palette    →    App Theme
  ┌──────────────┐            ┌─────────────────┐      ┌─────────────────┐
  │ ~~~~~~~~~~   │            │ Primary: #6750A4│      │ Buttons: #6750A4│
  │ ~~ 🌄 ~~~~   │  ────────▶ │ Secondary:#625B71│ ──▶ │ Cards:  #FFFBFE│
  │ ~~~~~~~~~~   │   extract  │ Tertiary: #7D5260│      │ FAB:    #6750A4│
  │ ~~~~~~~~~~   │            │ Neutral: #605D62│      │ Text:   #1C1B1F│
  └──────────────┘            └─────────────────┘      └─────────────────┘
```

### Cross-Platform Color Abstraction

```tsx
// shared/theme/colors.ts
import { Platform } from 'react-native';
import { DynamicColorIOS, PlatformColor } from 'react-native';

export const colors = {
  background: Platform.select({
    ios: PlatformColor('systemBackground'),
    android: PlatformColor('@android:color/background_light'),
    default: '#FFFFFF',
  }),
  text: Platform.select({
    ios: PlatformColor('label'),
    android: PlatformColor('@android:color/primary_text_light'),
    default: '#000000',
  }),
  separator: Platform.select({
    ios: PlatformColor('separator'),
    android: PlatformColor('@android:color/darker_gray'),
    default: '#C6C6C8',
  }),
};
```

---

## Phase 8: Form Factor Adaptation

### Device Matrix

| Form Factor | iOS Devices | Android Devices | Layout Considerations |
|-------------|------------|-----------------|----------------------|
| Phone (small) | iPhone SE (375pt) | 360dp width devices | Single column, full-width cards |
| Phone (large) | iPhone 15 Pro Max (430pt) | 412dp+ devices | Single column, slightly wider margins |
| Tablet | iPad (768pt+) | 600dp+ tablets | Two-column master-detail, sidebar nav |
| Foldable (folded) | N/A | Galaxy Fold outer (280dp) | Compact single column |
| Foldable (unfolded) | N/A | Galaxy Fold inner (585dp) | Two-pane layout, avoid hinge |
| iPad Multitasking | Split View (50/50, 33/66) | N/A | Respond to size class changes |

### Responsive Layout Decision Tree

```
  Screen width in density-independent units?
  │
  ├─ < 380dp → COMPACT
  │   → Single column, stacked layout
  │   → Bottom sheet instead of side panel
  │   → Cards fill width with 16dp margins
  │
  ├─ 380-599dp → STANDARD PHONE
  │   → Single column, standard margins (16-20dp)
  │   → Bottom tabs (iOS) / bottom nav (Android)
  │   → Full-width content with card containers
  │
  ├─ 600-839dp → MEDIUM (small tablet / unfolded phone)
  │   → Two-column where appropriate
  │   → Navigation Rail (Android) / sidebar (iOS)
  │   → Master-detail split for list→detail flows
  │
  └─ 840dp+ → EXPANDED (tablet / desktop)
      → Multi-column layout
      → Permanent sidebar navigation
      → Master-detail is default pattern
      → Content max-width to prevent ultra-wide lines
```

### Foldable Device Handling (Android)

```
  Folded State                         Unfolded State
  ┌─────────────┐                     ┌─────────────┬─────────────┐
  │             │                     │    Left     ││    Right    │
  │  Compact    │    ── unfold ──▶    │    Pane     ││    Pane     │
  │  Layout     │                     │  (list)    ││  (detail)   │
  │             │                     │             ││             │
  └─────────────┘                     └─────────────┴─────────────┘
                                                   ↑
                                                 hinge
                                            (avoid placing
                                            content here)
```

---

## Platform-Specific File Organization

### React Native — Recommended Structure

```
src/
├── components/
│   ├── Button.tsx                   ← shared component (no platform code)
│   ├── Header.tsx                   ← shared types + logic
│   ├── Header.ios.tsx               ← iOS-specific rendering
│   ├── Header.android.tsx           ← Android-specific rendering
│   └── PlatformIcon.tsx             ← platform-adaptive icon mapper
├── hooks/
│   ├── usePermissions.ts            ← shared permission interface
│   ├── usePermissions.ios.ts        ← iOS permission implementation
│   └── usePermissions.android.ts    ← Android permission implementation
├── utils/
│   ├── haptics.ts                   ← cross-platform haptic abstraction
│   ├── share.ts                     ← cross-platform share sheet
│   └── platform.ts                  ← Platform.select utilities
├── theme/
│   ├── tokens.ts                    ← shared design tokens
│   ├── colors.ios.ts                ← iOS system colors (PlatformColor)
│   └── colors.android.ts            ← Android system colors + dynamic
└── navigation/
    ├── AppNavigator.tsx             ← shared navigator structure
    ├── screenOptions.ios.ts         ← iOS nav options (large titles, swipe)
    └── screenOptions.android.ts     ← Android nav options (Material motion)
```

### Flutter — Recommended Structure

```
lib/
├── widgets/
│   ├── adaptive_button.dart         ← CupertinoButton vs ElevatedButton
│   ├── adaptive_dialog.dart         ← CupertinoAlertDialog vs AlertDialog
│   ├── adaptive_scaffold.dart       ← CupertinoPageScaffold vs Scaffold
│   └── adaptive_switch.dart         ← CupertinoSwitch vs Switch
├── platform/
│   ├── permissions.dart             ← unified permission API
│   ├── haptics.dart                 ← HapticFeedback abstraction
│   └── share.dart                   ← share sheet abstraction
└── theme/
    ├── app_theme.dart               ← ThemeData + CupertinoThemeData
    ├── typography.dart              ← platform-aware text styles
    └── colors.dart                  ← adaptive color tokens
```

---

## Common Adaptation Anti-Patterns

| Anti-Pattern | Why It's Wrong | What to Do Instead |
|-------------|---------------|-------------------|
| iOS-style bottom tabs on Android | Android uses Bottom Navigation (different height, shape, ripple) | Use platform-native navigation component |
| Android-style FAB on iOS | iOS has no FAB convention — users don't expect it | Use trailing nav bar button on iOS |
| Same alert dialog on both | iOS alerts look different from Material dialogs | Use CupertinoAlertDialog on iOS, AlertDialog on Android |
| Ignoring back gesture differences | iOS: swipe from left edge. Android: swipe from either edge | Configure platform-specific gesture handlers |
| Same switch component | UISwitch is wider and green. Material Switch is narrower and uses theme color | Use platform-native switch or adaptive wrapper |
| Hardcoded colors instead of system | Breaks dark mode, ignores dynamic color, ignores accessibility | Use PlatformColor, semantic tokens, or Material You |
| Same date picker on both | iOS uses wheel picker. Android uses calendar dialog | Use DateTimePicker with platform mode |
| Forcing custom fonts everywhere | Ignores system font benefits (Dynamic Type, font scaling) | Use system font as primary, custom for brand moments |
| Same scroll physics | iOS has rubber-band bounce. Android has stretch/glow overscroll | Let the platform provide default scroll physics |
| Ignoring Android edge-to-edge | Content hidden behind system bars | Apply WindowInsets correctly, draw behind system bars |
| Same keyboard avoidance | iOS: KeyboardAvoidingView. Android: windowSoftInputMode | Use platform-specific keyboard handling |
| Building custom permission dialogs | OS-mandated dialogs cannot be replaced | Show rationale BEFORE the system prompt, not instead of it |

---

## Tips for Best Results

1. **Start with the differences matrix** — before writing any code, identify which platform conventions apply to your feature. The matrix in Phase 1 is your checklist
2. **Prototype on the harder platform first** — if your feature involves gestures, start on Android (more gesture edge cases). If it involves system integration, start on iOS (stricter sandbox)
3. **Use platform-specific files for complex differences** — a 5-line Platform.select is fine. A 50-line branching block should be two separate files
4. **Test on the cheapest Android device you can find** — if it runs smooth on a budget phone, it runs smooth everywhere. Simulators lie about performance
5. **Record your app and watch at 0.5x speed** — you will catch every animation hitch, every layout jump, every incorrect gesture response
6. **Read the actual platform guidelines every quarter** — Apple and Google update HIG and Material Design regularly. What was correct last year might be deprecated now
7. **Ship the same features to both platforms on the same day** — platform parity prevents "why does Android get this but iOS doesn't?" support tickets
8. **Keep your native module surface area as small as possible** — every native module is a potential build failure on every framework upgrade
9. **Respect system settings** — dark mode, font scale, reduced motion, bold text. Users chose these settings for a reason. Override them and you lose their trust
10. **Measure adaptation ROI** — track which platform-specific adaptations actually improve retention or reduce support tickets. Cut the ones that don't matter

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
