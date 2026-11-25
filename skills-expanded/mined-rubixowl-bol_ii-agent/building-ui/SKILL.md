---
name: building-ui
description: Complete guide for building beautiful apps with Expo Router. Covers fundamentals, styling, components, navigation, animations, patterns, and native tabs.
version: 1.0.0
license: MIT
---

# Expo UI Guidelines

## References

Consult these resources as needed:

- ./references/route-structure.md -- Route file conventions, dynamic routes, query parameters, groups, and folder organization
- ./references/tabs.md -- Native tab bar with NativeTabs, migration from JS tabs, iOS 26 features
- ./references/icons.md -- SF Symbols with expo-symbols, common icon names, animations, and weights
- ./references/controls.md -- Native iOS controls: Switch, Slider, SegmentedControl, DateTimePicker, Picker
- ./references/visual-effects.md -- Blur effects with expo-blur and liquid glass with expo-glass-effect
- ./references/animations.md -- Reanimated animations: entering, exiting, layout, scroll-driven, and gestures
- ./references/search.md -- Search bar integration with headers, useSearch hook, and filtering patterns
- ./references/gradients.md -- CSS gradients using experimental_backgroundImage (New Architecture only)
- ./references/media.md -- Media handling for Expo Router including camera, audio, video, and file saving
- ./references/storage.md -- Data storage patterns including SQLite, AsyncStorage, and SecureStore
- ./references/webgpu-three.md -- 3D graphics, games, and GPU-powered visualizations with WebGPU and Three.js

## Running the App

**CRITICAL: Always try Expo Go first before creating custom builds.**

Most Expo apps work in Expo Go without any custom native code. Before running `npx expo run:ios` or `npx expo run:android`:

1. **Start with Expo Go**: Run `npx expo start` and scan the QR code with Expo Go
2. **Check if features work**: Test your app thoroughly in Expo Go
3. **Only create custom builds when required** - see below

### When Custom Builds Are Required

You need `npx expo run:ios/android` or `eas build` ONLY when using:

- **Local Expo modules** (custom native code in `modules/`)
- **Apple targets** (widgets, app clips, extensions via `@bacons/apple-targets`)
- **Third-party native modules** not included in Expo Go
- **Custom native configuration** that can't be expressed in `app.json`

### When Expo Go Works

Expo Go supports a huge range of features out of the box:

- All `expo-*` packages (camera, location, notifications, etc.)
- Expo Router navigation
- Most UI libraries (reanimated, gesture handler, etc.)
- Push notifications, deep links, and more

**If you're unsure, try Expo Go first.** Creating custom builds adds complexity, slower iteration, and requires Xcode/Android Studio setup.

## Code Style

- Be cautious of unterminated strings. Ensure nested backticks are escaped; never forget to escape quotes correctly.
- Always use import statements at the top of the file.
- Always use kebab-case for file names, e.g. `comment-card.tsx`
- Always remove old route files when moving or restructuring navigation
- Never use special characters in file names
- Configure tsconfig.json with path aliases, and prefer aliases over relative imports for refactors.

## Routes

See `./references/route-structure.md` for detailed route conventions.

- Routes belong in the `app` directory.
- Never co-locate components, types, or utilities in the app directory. This is an anti-pattern.
- Ensure the app always has a route that matches "/", it may be inside a group route.

## Library Preferences

- Never use modules removed from React Native such as Picker, WebView, SafeAreaView, or AsyncStorage
- Never use legacy expo-permissions
- `expo-audio` not `expo-av`
- `expo-video` not `expo-av`
- `expo-symbols` not `@expo/vector-icons`
- `react-native-safe-area-context` not react-native SafeAreaView
- `process.env.EXPO_OS` not `Platform.OS`
- `React.use` not `React.useContext`
- `expo-image` Image component instead of intrinsic element `img`
- `expo-glass-effect` for liquid glass backdrops

## Responsiveness

- Always wrap root component in a scroll view for responsiveness
- Use `<ScrollView contentInsetAdjustmentBehavior="automatic" />` instead of `<SafeAreaView>` for smarter safe area insets
- `contentInsetAdjustmentBehavior="automatic"` should be applied to FlatList and SectionList as well
- Use flexbox instead of Dimensions API
- ALWAYS prefer `useWindowDimensions` over `Dimensions.get()` to measure screen size

## Behavior

- Use expo-haptics conditionally on iOS to make more delightful experiences
- Use views with built-in haptics like `<Switch />` from React Native and `@react-native-community/datetimepicker`
- When a route belongs to a Stack, its first child should almost always be a ScrollView with `contentInsetAdjustmentBehavior="automatic"` set
- Prefer `headerSearchBarOptions` in Stack.Screen options to add a search bar
- Use the `<Text selectable />` prop on text containing data that could be copied
- Consider formatting large numbers like 1.4M or 38k
- Never use intrinsic elements like 'img' or 'div' unless in a webview or Expo DOM component

# Styling

Follow Apple Human Interface Guidelines.

## General Styling Rules

- Prefer flex gap over margin and padding styles
- Prefer padding over margin where possible
- Always account for safe area, either with stack headers, tabs, or ScrollView/FlatList `contentInsetAdjustmentBehavior="automatic"`
- Ensure both top and bottom safe area insets are accounted for
- Inline styles not StyleSheet.create unless reusing styles is faster
- Add entering and exiting animations for state changes
- Use `{ borderCurve: 'continuous' }` for rounded corners unless creating a capsule shape
- ALWAYS use a navigation stack title instead of a custom text element on the page
- When padding a ScrollView, use `contentContainerStyle` padding and gap instead of padding on the ScrollView itself (reduces clipping)
- CSS and Tailwind are not supported - use inline styles

## Text Styling

- Add the `selectable` prop to every `<Text/>` element displaying important data or error messages
- Counters should use `{ fontVariant: 'tabular-nums' }` for alignment

## Shadows

Use CSS `boxShadow` style prop. NEVER use legacy React Native shadow or elevation styles.

```tsx
<View style={{ boxShadow: "0 1px 2px rgba(0, 0, 0, 0.05)" }} />
```

'inset' shadows are supported.

# Navigation

## Link

Use `<Link href="/path" />` from 'expo-router' for navigation between routes.

```tsx
import { Link } from 'expo-router';

// Basic link
<Link href="/path" />

// Wrapping custom components
<Link href="/path" asChild>
  <Pressable>...</Pressable>
</Link>
```

Whenever possible, include a `<Link.Preview>` to follow iOS conventions. Add context menus and previews frequently to enhance navigation.

## Stack

- ALWAYS use `_layout.tsx` files to define stacks
- Use Stack from 'expo-router/stack' for native navigation stacks

### Page Title

Set the page title in Stack.Screen options:

```tsx
<Stack.Screen options={{ title: "Home" }} />
```

## Context Menus

Add long press context menus to Link components:

```tsx
import { Link } from "expo-router";

<Link href="/settings" asChild>
  <Link.Trigger>
    <Pressable>
      <Card />
    </Pressable>
  </Link.Trigger>
  <Link.Menu>
    <Link.MenuAction
      title="Share"
      icon="square.and.arrow.up"
      onPress={handleSharePress}
    />
    <Link.MenuAction
      title="Block"
      icon="nosign"
      destructive
      onPress={handleBlockPress}
    />
    <Link.Menu title="More" icon="ellipsis">
      <Link.MenuAction title="Copy" icon="doc.on.doc" onPress={() => {}} />
      <Link.MenuAction
        title="Delete"
        icon="trash"
        destructive
        onPress={() => {}}
      />
    </Link.Menu>
  </Link.Menu>
</Link>;
```

## Link Previews

Use link previews frequently to enhance navigation:

```tsx
<Link href="/settings">
  <Link.Trigger>
    <Pressable>
      <Card />
    </Pressable>
  </Link.Trigger>
  <Link.Preview />
</Link>
```

Link preview can be used with context menus.

## Modal

Present a screen as a modal:

```tsx
<Stack.Screen name="modal" options={{ presentation: "modal" }} />
```

Prefer this to building a custom modal component.

## Sheet

Present a screen as a dynamic form sheet:

```tsx
<Stack.Screen
  name="sheet"
  options={{
    presentation: "formSheet",
    sheetGrabberVisible: true,
    sheetAllowedDetents: [0.5, 1.0],
    contentStyle: { backgroundColor: "transparent" },
  }}
/>
```

- Using `contentStyle: { backgroundColor: "transparent" }` makes the background liquid glass on iOS 26+.

## Common route structure

A standard app layout with tabs and stacks inside each tab:

```
app/
  _layout.tsx — <NativeTabs />
  (index,search)/
    _layout.tsx — <Stack />
    index.tsx — Main list
    search.tsx — Search view
```

```tsx
// app/_layout.tsx
import { NativeTabs, Icon, Label } from "expo-router/unstable-native-tabs";
import { Theme } from "../components/theme";

export default function Layout() {
  return (
    <Theme>
      <NativeTabs>
        <NativeTabs.Trigger name="(index)">
          <Icon sf="list.dash" />
          <Label>Items</Label>
        </NativeTabs.Trigger>
        <NativeTabs.Trigger name="(search)" role="search" />
      </NativeTabs>
    </Theme>
  );
}
```

Create a shared group route so both tabs can push common screens:

```tsx
// app/(index,search)/_layout.tsx
import { Stack } from "expo-router/stack";
import { PlatformColor } from "react-native";

export default function Layout({ segment }) {
  const screen = segment.match(/\((.*)\)/)?.[1]!;
  const titles: Record<string, string> = { index: "Items", search: "Search" };

  return (
    <Stack
      screenOptions={{
        headerTransparent: true,
        headerShadowVisible: false,
        headerLargeTitleShadowVisible: false,
        headerLargeStyle: { backgroundColor: "transparent" },
        headerTitleStyle: { color: PlatformColor("label") },
        headerLargeTitle: true,
        headerBlurEffect: "none",
        headerBackButtonDisplayMode: "minimal",
      }}
    >
      <Stack.Screen name={screen} options={{ title: titles[screen] }} />
      <Stack.Screen name="i/[id]" options={{ headerLargeTitle: false }} />
    </Stack>
  );
}
```

## UI/UX DESIGN SYSTEM

### MANDATORY: Dark Mode and Light Mode Support

- Every mobile app MUST support both dark mode and light mode. Users expect apps to respect their system theme preference.
- **The default theme MUST be light mode.** The app should launch in light mode by default, and users can switch to dark mode via settings.

#### Implementation Guidelines:

- Use `expo-linear-gradient` or `react-native-linear-gradient` for gradient backgrounds
- Add subtle animations using `react-native-reanimated` to make backgrounds feel alive
- Gradient colors, positions, or opacity for dynamic effects
- Keep animations subtle and smooth (slow transitions, 3-5 second loops)
- Use `useSharedValue` and `withRepeat`/`withTiming` for performant animations

#### Best Practices:

- Use 2-3 colors maximum for gradients to keep it clean
- Ensure text remains readable over animated backgrounds
- Add blur overlays if content needs more contrast
- Test on lower-end devices to ensure smooth 60fps performance

### MANDATORY: Screens you must implement

- Intro: Each app might have a different set of screens. One onboarding flow might take 10 screens, and another might take 2. Understanding your app's UX and industry best practices is crucial for success. Here are the screens that every app must have.
- Login: Keep login screens simple and clear. Include username and assword fields plus a confirmation button. Always try to offer Google or Apple sign-in options. This takes extra setup time but greatly reduces user friction.
- Onboarding screens: Focus on communicating core value quickly and minimize required actions. Consider using progress indicators to show users how far they've come in the setup process. The best onboarding experiences feel helpful rather than obstructive, setting users up for success with the minimum necessary friction.
- Home screen: Home screen is the main hub for user interaction. It must address two critical states: the empty state (when users have no content yet) with a clear call-to-action guiding them to the app's primary function, and the content state for returning users that displays personalized information and quick access to main features.
- User Profiles: Profiles personalize the app experience and connect users to the community. Keep profile pages clean with limited, relevant information. Use intuitive flows to lead to secondary info without confusing the users.
- Settings screen: Organize options into logical categories, maintain a clean layout, and make actions visible. Group settings into sections to avoid overwhelm, and add a search function if your settings consist of a more complex flow.
- Subscription screen: For paid apps, clearly show available plans, pricing, and features. Highlight the most popular option, briefly describe benefits, and include a clear call to action. Keep the process simple. Implement biometric authentication (Face ID/Touch ID) and quick verification methods to streamline the payment process.

### Mandatory: Some design guidelines for mobile app

- Short and sweet onboarding: Your onboarding shouldn't feel like homework. Keep it to 3-4 screens max, clearly explain value, and quickly guide users to the app's core value. Every extra onboarding step risks losing users before they experience real value.
- Frictionless signup forms: Add Google and social sign-ins for easier, faster account creation. Don't make people fill out long forms right away. Let them sign up in seconds-then ask for the rest once they're in and already trust your product.
- Personalize immediately: Personalized experiences have higher retention. Collect basic preferences early, then customize the content users see right away. When users feel the app is built just for them, they stay engaged longer.
- Clear action buttons: Buttons drive actions. So, use clear, benefit-driven button labels ("Get Started", "Claim Your Free Trial") to boost taps. Generic labels like "Submit" or "Continue" are missed opportunities for higher conversions.
- Show progress early: Good UX guides users through every step. From entry to outcome, make sure each screen has a purpose: → Clear actions → Visual states (like timers, confirmations, outcomes) → A sense of movement and feedback
- Smart request permissions: Don't bombard users immediately with permission pop-ups. Ask for access (notifications, location, etc.) only when needed and clearly state the benefits. They're more likely to grant permissions if they understand why.
- Reducing cognitive load: Don't make users think too hard. Simplify choices, remove unnecessary steps, and break up complex flows into bite-sized chunks. The easier it is to use, the more likely users are to stick with it.
- Clear navigation hierarchy: If users can't navigate smoothly, they're gone. Use clear, simple navigation and limit tabs or menus to only what's necessary. A confused user rarely becomes a long-term user-keep it intuitive and straightforward.
- Keep it simple: If an element doesn't add value, remove it. Keep the UI clean and uncluttered. Every element should have a purpose.
- Utilize white space: White space isn't wasted space. It gives your design room to breathe and guides users' eyes to what's important.
- Use shadows for elevation: Shadows add depth and help users differentiate between layers. Keep them subtle to maintain a clean aesthetic.
- User blurs and gradients: Blurs and gradients, especially in iOS design, are a simple visual technique to add a modern, polished look to your UI.
- Blow up your images: Blown-up images as backgrounds add a dramatic, artsy vibe. Use blend layers for a unique look - AI images work great here

### MANDATORY: Design guidelines for mobile app settings screens

- Group settings: Group related settings together. Think about how users will look for things. Categories should make sense to users.
- Clear labels and descriptions: Use easy to understand labels and add short descriptions for more complex settings. Display & Brightness' tells users exactly what they'll find. Users shouldn't need to guess what something does.
- Highlight critical settings: Frequently used settings should be easy to find. Don't bury critical functions five levels deep just to keep things tidy.
- Personalize Defaults: Use onboarding flow to let users set their preferences early. This creates a more personalized experience from the start and reduces the need to dig through settings later.
- Use progressive settings: Start with basic settings, allow access to advanced ones. Not everyone needs every option visible at once.
- Use visual hierarchy: Use proper spacing and grouping. Make interactive elements obvious. Settings should be scannable at a glance.
- Consider edge cases: Account deletion, data export, privacy settings - these need extra attention. Make important actions clear but hard to trigger accidentally.

### Mandatory: Design guidelines for mobile app loading states

- Use a skeleton screen: Show a placeholder screen with the layout of the actual screen. This gives users an idea of what to expect and reduces the perceived load time.
- Progressive loading: Load content in chunks. Show the top part of the screen first, then load more content as the user scrolls. This reduces the perceived load time and makes the app feel faster.
- Branded animations: Use branded animations to show that the app is loading. This makes the app feel more responsive and polished.
- Progress indicators with context: Show a progress bar or spinner with context. This lets users know that the app is working and reduces the likelihood of them thinking the app has crashed.
- Avoid loading spinners: If the app is loading a large amount of data, show a progress bar or spinner. This lets users know that the app is working and reduces the likelihood of them thinking the app has crashed.

### Mandatory: Design guidelines for mobile app forms

- Show only what's necessary: Every extra field reduces completion rates by 20%. Ask only what you absolutely need right now. You can always collect more information later when users are more invested.
- Appropriate input types: Use the right keyboard for each field. Phone number? Show the numeric pad. Email? Show the email keyboard. Small detail that makes a huge difference in completion speed.
- Real-time validation: Don't wait until submission to show errors. Validate each field as users type or move to the next field. Show success states too - users like knowing they're doing things right.
- Use clear error states: When something goes wrong, make it obvious what needs fixing. "Password must be 8 characters" is better than "Invalid password." Help users recover quickly and seamlessly.
- Make CTAS stand out: Your submit button should be prominent and clear about what happens next. "Create Account" is better than "Submit." Size it properly for touch targets.
- Smart keyboard behavior: Enable auto-advance when sensible (like OTP fields). Add 'Next' and 'Done' buttons where appropriate. Small touches that make forms feel smoother.
- Break long-forms down: if you need lots of information, split it into logical steps. Show progress to keep users motivated. Each step should feel manageable.

### Mandatory: Design guidelines for mobile app welcome screen

- Show only what's necessary: Every extra field reduces completion rates by 20%. Ask only what you absolutely need right now. You can always collect more information later when users are more invested.
- Make the best of graphics: Use high quality images or canvas to make the app look professional. Use the right aspect ratio for the screen. Use the right file format. Use the right file size. Use the right compression. Use the right resolution. Use the right color depth. Use the right color profile. Use the right color space. Use the right color mode. Use the right color temperature. Use the right color balance. Use the right color correction. Use the right color grading

### Choose gradient colors for both light and dark mode that match your app's unique color theme. Do NOT copy example colors - create custom gradients that complement your app's design.

- Must choose color that contrast well with each other for both light and dark mode
- Select gradient colors based on the app category
- Beyond screen backgrounds, also apply gradients to: Hero sections and headers, Primary action buttons, Card backgrounds (subtle gradients), Empty states and onboarding screens, Premium/featured content highlights

### Icons: Use @expo/vector-icons Only

You MUST use `@expo/vector-icons` for all icons in your mobile apps. NEVER use FontAwesome icons.

Recommended icon sets from `@expo/vector-icons`:

- **Ionicons**: Modern, clean icons ideal for iOS-style apps
- **MaterialIcons**: Google's Material Design icons for Android-style apps
- **MaterialCommunityIcons**: Extended Material icons with more options
- **Feather**: Minimal, elegant line icons
- **AntDesign**: Clean icons with good variety

### MANDATORY: Animation Design Guidelines

Every mobile app MUST include smooth, delightful animations to create a polished user experience. Use `react-native-reanimated` for performant animations.

```bash
npx expo install react-native-reanimated
bun install react-native-worklets@0.5.1
```

Then update babel.config.js - add "react-native-worklets/plugin" as the LAST item in plugins array:

```js
module.exports = function (api) {
  api.cache(true);
  return {
    presets: ["babel-preset-expo"],
    plugins: [
      // ... other plugins
      "react-native-worklets/plugin", // MUST be last, do NOT use reanimated/plugin
    ],
  };
};
```

**IMPORTANT**: Only use "react-native-worklets/plugin". Do NOT use "react-native-reanimated/plugin" - that is the old version. Never add both plugins.
