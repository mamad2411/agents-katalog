---
name: components-2
description: "Skill for the Components area of Securacy. 31 symbols across 9 files."
---

# Components

31 symbols | 9 files | Cohesion: 81%

## When to Use

- Working with code in `securacyfrontend/`
- Understanding how apiCallDelete, revokeApiKey, AppSidebar work
- Modifying components-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `securacyfrontend/components/LetterGlitch.tsx` | hexToRgb, interpolateColor, drawLetters, handleSmoothTransitions, animate (+8) |
| `securacyfrontend/components/app-sidebar.tsx` | AppSidebar, fetchThreats, handleSaved |
| `securacyfrontend/components/Plasma.tsx` | hexToRgb, Plasma, setSize |
| `securacyfrontend/components/Particles.tsx` | hexToRgb, Particles, resize |
| `securacyfrontend/components/LineWaves.tsx` | hexToVec3, LineWaves, resize |
| `securacyfrontend/components/DecryptedText.tsx` | DecryptedText, getNextIndex, shuffleText |
| `securacyfrontend/lib/api_call_config.ts` | apiCallDelete |
| `securacyfrontend/services/mcpService.ts` | revokeApiKey |
| `securacyfrontend/app/home/settings/_components/api-keys-section.tsx` | handleRevoke |

## Entry Points

Start here when exploring this area:

- **`apiCallDelete`** (Function) — `securacyfrontend/lib/api_call_config.ts:255`
- **`revokeApiKey`** (Function) — `securacyfrontend/services/mcpService.ts:65`
- **`AppSidebar`** (Function) — `securacyfrontend/components/app-sidebar.tsx:116`
- **`fetchThreats`** (Function) — `securacyfrontend/components/app-sidebar.tsx:160`
- **`handleSaved`** (Function) — `securacyfrontend/components/app-sidebar.tsx:184`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `apiCallDelete` | Function | `securacyfrontend/lib/api_call_config.ts` | 255 |
| `revokeApiKey` | Function | `securacyfrontend/services/mcpService.ts` | 65 |
| `AppSidebar` | Function | `securacyfrontend/components/app-sidebar.tsx` | 116 |
| `fetchThreats` | Function | `securacyfrontend/components/app-sidebar.tsx` | 160 |
| `handleSaved` | Function | `securacyfrontend/components/app-sidebar.tsx` | 184 |
| `handleRevoke` | Function | `securacyfrontend/app/home/settings/_components/api-keys-section.tsx` | 83 |
| `Plasma` | Function | `securacyfrontend/components/Plasma.tsx` | 92 |
| `setSize` | Function | `securacyfrontend/components/Plasma.tsx` | 159 |
| `LineWaves` | Function | `securacyfrontend/components/LineWaves.tsx` | 147 |
| `resize` | Function | `securacyfrontend/components/LineWaves.tsx` | 187 |
| `DecryptedText` | Function | `securacyfrontend/components/DecryptedText.tsx` | 20 |
| `getNextIndex` | Function | `securacyfrontend/components/DecryptedText.tsx` | 45 |
| `shuffleText` | Function | `securacyfrontend/components/DecryptedText.tsx` | 74 |
| `hexToRgb` | Function | `securacyfrontend/components/LetterGlitch.tsx` | 45 |
| `interpolateColor` | Function | `securacyfrontend/components/LetterGlitch.tsx` | 61 |
| `drawLetters` | Function | `securacyfrontend/components/LetterGlitch.tsx` | 115 |
| `handleSmoothTransitions` | Function | `securacyfrontend/components/LetterGlitch.tsx` | 152 |
| `animate` | Function | `securacyfrontend/components/LetterGlitch.tsx` | 173 |
| `LetterGlitch` | Function | `securacyfrontend/components/LetterGlitch.tsx` | 2 |
| `calculateGrid` | Function | `securacyfrontend/components/LetterGlitch.tsx` | 74 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `ApiKeysSection → DecodeJwt` | cross_community | 7 |
| `AppSidebar → DecodeJwt` | cross_community | 6 |
| `HandleSaved → DecodeJwt` | cross_community | 6 |
| `HandleResize → GetRandomChar` | cross_community | 4 |
| `HandleResize → GetRandomColor` | cross_community | 4 |
| `HandleResize → HexToRgb` | cross_community | 4 |
| `HandleResize → InterpolateColor` | cross_community | 4 |
| `HandleResize → DrawLetters` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| _components | 3 calls |
| Hooks | 1 calls |

## How to Explore

1. `gitnexus_context({name: "apiCallDelete"})` — see callers and callees
2. `gitnexus_query({query: "components"})` — find related execution flows
3. Read key files listed above for implementation details
