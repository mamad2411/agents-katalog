# Platform Adapter Implementation

## Purpose
Implements platform-specific native capabilities using Metro bundler's file extension resolution.

## Role
Mobile Developer

## Phase
Development

## Triggered By
Story requires native device capability (camera, biometrics, etc.).

## Inputs
- Native capability requirement from the story

## Process

### Folder Structure Per Adapter
```
platform/
├── {adapter-name}/
│   ├── index.ts              ← interface definition + barrel export (ALWAYS)
│   ├── {name}.ts              ← web stub (for dev in Expo web mode)
│   ├── {name}.native.ts       ← iOS + Android (most cases)
│   ├── {name}.ios.ts          ← iOS only (rare — genuine OS difference)
│   └── {name}.android.ts      ← Android only (rare)
└── index.ts                   ← root barrel, re-exports all adapters
```

### Decision Rule
- Simple (<10 lines difference): `Platform.select` inline, single file in index.ts
- Standard: `{name}.ts` (web stub) + `{name}.native.ts` + index.ts
- Genuine OS difference: `{name}.ts` + `{name}.ios.ts` + `{name}.android.ts` + index.ts

### Metro Resolution Order
- On iOS: `.ios.ts` > `.native.ts` > `.ts`
- On Android: `.android.ts` > `.native.ts` > `.ts`
- On Web: `.ts` (stub)

### Import Rule
ALWAYS import from folder barrel (`platform/{adapter}`). NEVER import from platform file directly (`platform/{adapter}/{name}.native.ts`).

### Interface Required in index.ts
```typescript
// platform/camera/index.ts
export interface CameraAdapter {
  takePicture(): Promise<string>
  requestPermission(): Promise<boolean>
}

export { camera } from './{name}'  // Metro resolves to correct platform
```

PRs containing native code in `ios/` or `android/` files → add label `needs: device-testing` to PR automatically. Edward validates on physical device before merging.

Agent develops entirely in Expo web mode (~90%+ of app testable this way).

## Outputs
Platform adapter with web stub, native implementation, and barrel export.

## Quality Gates
- [ ] index.ts exists in every adapter folder with TypeScript interface
- [ ] Barrel export used (never direct platform file import)
- [ ] Web stub returns sensible mock data (enables web mode dev)
- [ ] needs: device-testing label added for native-specific PRs

## References
- `.claude/skills/mobile-developer/mobile-app-scaffolding/SKILL.md`
