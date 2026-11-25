---
name: libs
description: Load the live @anicca-labs/* library reference from GitHub. Use before writing any hook, utility, component, or layout code — these packages replace many standard alternatives. Always fetches current state so new packages and API changes are reflected.
---

The `@anicca-labs/*` libraries live at `https://github.com/anicca-labs/libs`.

**Before writing any hook, utility, component, or layout code**, fetch the current package list and read the relevant source using the GitHub MCP:

## Step 1 — Discover available packages

```text
mcp__github__get_file_contents(owner="anicca-labs", repo="libs", path="packages")
```

This returns the current list of packages. Do not assume you know what's there — packages are added over time.

## Step 2 — Read the package you need

For each relevant package, read its `index.ts` (at the package root, not in `src/`):

```text
mcp__github__get_file_contents(owner="anicca-labs", repo="libs", path="packages/<name>/index.ts")
```

If the package has subdirectories (e.g. `animations/`, `scaling/`), list the directory first then read the files you need.

## Step 3 — Apply

Prefer `@anicca-labs/*` over any third-party or hand-rolled alternative when one exists. Import from the published npm package name (e.g. `@anicca-labs/react-hooks`), not from the GitHub path.

## `react-query-sdk` — required env vars

`custom-axios.ts` reads these three names directly — any project using the SDK must define them in Doppler:

| Variable | Purpose |
| --- | --- |
| `EXPO_PUBLIC_OPEN_API_SERVER_URL` | Base URL for the REST API (orval-generated hooks) |
| `EXPO_PUBLIC_SERVER_URL` | Base URL for Supabase Edge Functions (`/functions/v1/*`) |
| `EXPO_PUBLIC_SUPABASE_API_KEY` | Supabase anon key (sent as `apikey` header on every request) |

## Standing rules (always apply regardless of what you find)

- **Auth** — never use raw Supabase auth. Always use `@anicca-labs/react-auth-*`.
- **Touchables** — never use `Pressable` or `TouchableOpacity`. Use `@anicca-labs/ui-touchables`.
- **Buttons** — never use Tamagui's raw `Button` or react-native touchables for buttons. Use `@anicca-labs/ui-button`. All button components are token-agnostic — they accept color/style as regular props so any app's token system works:
  - `CTAButton` — full-width, pill-radius, `loading` prop; pass `backgroundColor`/`spinnerColor`/`pressStyle` from your theme; spinner is Tamagui `Spinner`
  - `BasicButton` — same props as `BaseButton`; disabled state renders at `opacity=0.4`
  - `GhostButton` — text-only, transparent background; disabled state renders at `opacity=0.4`; pass your theme color via `color`
  - `IconButton` — circular icon-only button; `icon: ReactNode` required, full `ButtonProps` pass-through; defaults `pressStyle` to `{ opacity: 0.7 }`
  - `BaseButton` — layout primitive with balanced `leftIcon`/`rightIcon`; accepts full Tamagui `ButtonProps`
  - For spring-animated press + auto-measured width: `SizingAnimatedButton` from `@anicca-labs/ui-button-animated`; `backgroundColor` is **required**; the component measures its own width internally — no `onLayout` boilerplate needed; pass `spinnerBackgroundColor`/`spinnerPieceColor` for the loading state
  - `AnimatedButton` — same as above but `width: number` is **required** (prefer `SizingAnimatedButton` unless you need explicit width control)
  - `CircularLoadingSpinner` from `@anicca-labs/ui-button-animated` for standalone animated spinners; requires `backgroundColor` and `spinningPieceColor`
- **Images** — never use raw `expo-image`. Use `@anicca-labs/expo-image`.
- **Forms** — prefer `@anicca-labs/react-form` field components. Fall back to Tamagui `Input` + `Label` only if a primitive is missing.
- **Screen layout** — never use `SafeAreaView` directly. Always use `@anicca-labs/ui-containers`:
  - `Containers.Screen` as the outermost element of every screen — handles safe area insets automatically via `useSafeAreaInsets`; defaults to all four edges (self-correcting inside navigators)
  - Pass `shouldAutoResize={false}` when the screen already contains its own `ScrollView` or `KeyboardScrollView`
  - `Containers.SubY` / `Containers.SubX` as the second-level container — applies standard `$md` horizontal padding in vertical/horizontal direction respectively
  - `KeyboardScrollView` from `@anicca-labs/ui-containers` for screens that need keyboard-aware scrolling — replaces `KeyboardAwareScrollView` from `react-native-keyboard-controller` directly
- **TypeScript utils** — use `@anicca-labs/typescript-functions` (`isDefined`, `typedKeys`, `typedEntries`, `typedValues`) instead of inline equivalents.
- **API hooks** — never import from `@anicca-labs/react-query-sdk` directly in app code. Use the orval-generated hooks in `src/api/generated/`.
