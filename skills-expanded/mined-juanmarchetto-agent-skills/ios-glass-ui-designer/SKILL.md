---
name: ios-glass-ui-designer
description: "Redesign mobile app UI to feel unmistakably iOS-native with modern Apple-like glass materials (translucency, blur, depth). Use when: iOS design, glass UI, translucent UI, Apple-style, iOS material system, glassmorphism, blur effects, iOS-native interface, mobile app redesign, SF Pro typography."
license: MIT
metadata:
  version: 1.0.0
  category: design
  tags: [ios, glass, ui, design, apple, translucency, blur, mobile, swift, swiftui]
---

# iOS Glass UI Designer

Redesign or audit mobile app UI screens to feel iOS-native with restrained glass materials.

## Workflow

### Step 1: Analyze Current Screen
Read the screen's code/design. Identify:
- Current material usage (solid, transparent, blur)
- Typography (is it SF Pro-like? semantic sizes?)
- Color palette (neutral base? single accent?)
- Layout (safe-area aware? touch targets 44pt+?)
- Navigation pattern (standard iOS or custom?)
- Component style (system-like or over-designed?)

### Step 2: Generate Redesign Spec
For each screen, produce:
1. **Design Intent** — what should feel more iOS-native and why
2. **Material Map** — where glass is used (ultra-thin/regular/thick) and why
3. **Typography Map** — text styles with hierarchy rationale
4. **Layout Changes** — spacing, grouping, safe areas
5. **Code Changes** — specific SwiftUI/React Native code to implement

### Step 3: Apply Changes
Implement the redesign with actual code modifications.

### Glass Material Decision Tree
- Is it a floating overlay/toolbar? -> ultra-thin material
- Is it a card needing separation? -> regular material
- Is it a bottom sheet/modal? -> thick material
- Is it primary content? -> solid surface (NO glass)
- When in doubt? -> no glass. Restraint over spectacle.

## Design Principles
- Native over custom
- Restraint over spectacle
- Material is functional, not decorative
- "Feels obvious" rather than "looks fancy"
- Glass is a tool for hierarchy, focus, and context — not a theme
- Fewer, larger glass surfaces over many small glass chips

## Typography Rules
- System-first typography (SF Pro style)
- Clear hierarchy using size and weight, not color
- Semantic text styles: Title / Headline / Body / Caption
- Consistent vertical rhythm

## Color Rules
- Neutral palette by default (white/off-white backgrounds, system gray scales)
- Accent colors used sparingly (1 primary accent max)
- Avoid neon, high saturation blocks, heavy gradients

## Component Guidelines

### Buttons
- System button semantics preferred
- Glass buttons only in floating contexts (toolbar, overlay)
- Press state: slight opacity down + subtle scale, never flashy

### Lists
- iOS list rhythm (consistent row height, predictable spacing)
- Use either separators OR spacing (not both)
- Glass behind lists only if within a sheet/overlay

### Navigation
- Standard navigation bars with large titles when appropriate
- Translucent nav bar when content scrolls under it
- Clear title hierarchy and scroll behavior

### Modals & Sheets
- Bottom sheets preferred over full-screen modals
- Respect drag-to-dismiss gestures
- Regular/Thick material based on background complexity

## Example Output

**Screen:** Settings

**Before:** Flat white background, custom toggle components, 6 different font sizes, no visual grouping, non-standard back button.

**After:**
```
Design Intent: Make settings feel like a first-party Apple app — grouped
inset list style, system toggles, standard navigation.

Material Map:
- Navigation bar: ultra-thin material (content scrolls beneath)
- Grouped sections: solid surface with system gray background
- No glass on content cards (clarity over decoration)

Typography Map:
- Screen title: Large Title (34pt, bold)
- Section headers: Footnote (13pt, uppercase, secondary color)
- Row labels: Body (17pt, regular)
- Row detail: Body (17pt, secondary color)

Layout Changes:
- Added 20pt section spacing
- Grouped related settings into inset sections
- Safe-area insets respected on all edges
- Touch targets: all rows 44pt minimum height

Code Changes:
- Replaced custom toggles with SwiftUI Toggle()
- Used List with .insetGrouped style
- NavigationStack with .navigationTitle("Settings")
- Removed 3 custom font sizes, replaced with .body and .footnote
```

## Error Handling
- If not an iOS app: adapt principles to platform (Material You for Android, Fluent for Windows)
- If using React Native: use @react-native-community/blur for glass effects
- If no screens specified: audit all screens in the navigation stack, prioritize the most-visited
- If design conflicts with brand guidelines: note the conflict and suggest compromise
