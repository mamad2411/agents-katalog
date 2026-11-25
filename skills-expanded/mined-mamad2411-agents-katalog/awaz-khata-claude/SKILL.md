# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**Awaz Khata (آواز کھاتہ)** — a voice-first personal finance assistant for Pakistani users (Uplift AI × Replit Voice AI Hackathon). Users speak in Urdu / Roman Urdu / English / mixed; the app records the money event or answers a finance question, and speaks back in Urdu.

pnpm monorepo (`artifacts/*`, `lib/*`, `scripts`). npm/yarn are blocked by the root `preinstall` hook.

## Commands

```bash
pnpm install

# Typecheck — ALWAYS use the root script, not the package one (see gotcha below)
pnpm run typecheck            # typecheck:libs (tsc --build) then all packages
pnpm run typecheck:libs       # builds lib/* dist output only

pnpm run build                # typecheck + recursive build

# Backend
pnpm --filter @workspace/api-server run dev     # build + start (needs PORT set)
pnpm --filter @workspace/api-server test        # vitest run
pnpm --filter @workspace/api-server run seed    # load demo ledger data

# Single test file / single test
pnpm --filter @workspace/api-server exec vitest run src/lib/finance.test.ts
pnpm --filter @workspace/api-server exec vitest run -t "confirmationFor"

# Mobile app (Expo)
pnpm --filter @workspace/awaz-khata run dev

# Regenerate the API client + zod schemas from the OpenAPI contract
pnpm --filter @workspace/api-spec run codegen
```

On Replit, the `API Server` and `expo` workflows start these automatically; `Project` runs the `test` + `typecheck` validation workflows.

## Secrets

Set as Replit Secrets, never `.env` files. `UPLIFTAI_API_KEY` (STT + TTS), `LLM_API_KEY` (Groq `gsk_...` or OpenAI — provider auto-detected). Optional: `UPLIFTAI_VOICE_ID` (default `v_meklc281`), `LLM_PROVIDER`, `LLM_MODEL`. The mobile app never talks to Uplift AI or the LLM directly — keys live only on the backend; the app reads `EXPO_PUBLIC_DOMAIN` and calls `https://<domain>/api/...`.

## Architecture

```
Expo records audio
  → POST /api/voice/transcribe   Uplift AI STT
  → POST /api/voice/extract      LLM → structured intent JSON (mode: transaction | query | unknown)
  → POST /api/transactions (save)  OR  POST /api/query (finance engine)
  → deterministic Urdu response template
  → POST /api/voice/speak        Uplift AI TTS → base64 MP3 → played aloud
```

**The single most important invariant: the LLM only extracts intent. It never calculates.** All arithmetic, period bucketing, and every spoken Urdu string are deterministic and live in `artifacts/api-server/src/lib/finance.ts`. `/api/chat` is the one LLM-worded endpoint (advisor answers over a `buildFinancialSnapshot`), and it still short-circuits to a fixed Urdu string on an empty ledger.

Key backend modules (`artifacts/api-server/src/`):
- `lib/finance.ts` — finance engine + Urdu response templates. Dates are bucketed in **Pakistan Standard Time (UTC+5, no DST)** via a fixed offset, not `Intl`. `summarize()` returns per-period totals; `overallSummary()` adds the available `balance` and is used only for the whole ledger — a "balance for today" would be meaningless.
- `lib/store.ts` — JSON-file ledger. Atomic temp-file + rename writes, mutations serialized through an in-process promise queue, a corrupt file **throws** rather than returning `[]` (returning empty would let the next write destroy the ledger). `AWAZ_DATA_DIR` overrides the data directory (tests point it at a temp dir).
- `lib/llm.ts` — intent extraction, zod-validated union of transaction/query/unknown.
- `lib/uplift.ts` — Uplift AI client. Routes under `src/routes/`, mounted at `/api` in `app.ts`.

Every error must reach the client as `{ error: "<Urdu message>" }` — the `app.ts` error handler exists so Express never emits its HTML error page.

Transaction types: `expense`, `income`, `given` (lent to a person), `received` (returned by a person). Person balance = given − received. Available balance = income − expenses − given + received.

`artifacts/mockup-sandbox/` is a separate Vite/React/shadcn design sandbox, not part of the shipping app. Its `typecheck` currently fails on a pre-existing duplicate-`@types/react` conflict (react-native pins ~19.1, the catalog is ^19.2), which is why root `pnpm run build` fails — build the packages individually instead.

## Mobile app structure

Four tabs (`app/(tabs)/`): `index` (dashboard), `awaz` (voice hero), `khata` (transactions + people), `settings`. Outside the tabs: `onboarding`, `entry/new` (manual add **and** edit), `person/[name]`, `chat` (the open-ended advisor, kept reachable but off the tab bar).

Three foundations that every screen depends on — do not bypass them:

- **`theme/`** — `useTheme()` gives `colors` (semantic tokens only, never hex), `spacing`/`radius`/`iconSize`, and `text(variant)` which resolves a semantic type variant for the active script and the user's text-size preference. `theme/palette.ts` holds light, dark and high-contrast values.
- **`i18n/`** — `useT()` for strings, `useDirection()` for RTL-aware layout. Five locales (`ur`, `pa`, `skr`, `hi`, `en`), all typed against `locales/en.ts`, so adding a key there is a compile error until every language provides it. **No user-facing string belongs in a component.**
- **`store/preferences.tsx`** — AsyncStorage-backed; language, theme, text size, contrast, haptics, hide-balances, name, onboarding flag. Never sent to the backend.

RTL is done **without** `I18nManager.forceRTL` (which needs an app restart and would break in-app language switching). Rows opt into `dir.row`; only directional affordances (back/forward chevrons) mirror — semantic icons like the mic never do.

Conventions worth keeping:
- All UI text goes through `components/ui/Text`, all taps through `components/ui/Pressable` (enforces 44pt targets, haptics, an accessibility label).
- Money renders via `useMoney()` / `components/ui/Amount`. English puts `Rs.` before the number; every other supported language puts «روپے» after it.
- Direction is never colour-only: income/expense also carry an arrow and a +/− sign.
- `lib/format.ts` is display-only and formats dates in PKT to match the backend's day boundaries. The UI must not derive financial figures.

## Contract-first API

`lib/api-spec/openapi.yaml` is the source of truth. `orval` generates:
- `lib/api-client-react/src/generated/` — typed react-query client used by the Expo app
- `lib/api-zod/src/generated/` — zod schemas used by the backend for request/response validation

After editing `openapi.yaml` and running codegen, **add any new type and enum names to the hand-written barrel `lib/api-zod/src/index.ts`**. That barrel uses explicit export lists (not `export *`) because generated zod consts collide with same-named types; codegen's `clean` only wipes `src/generated/`, so the barrel survives but goes stale. Codegen chains `typecheck:libs`, which catches misses.

## Gotchas

- **TS6305 on api-server typecheck** — the package uses TS project references to `lib/api-zod` / `lib/db`, which resolve against built `.d.ts`, and the libs have no per-package build script. Run root `pnpm run typecheck:libs` first (root `pnpm run typecheck` already orders this correctly).
- **AppleDouble sidecars** — on exFAT/network volumes macOS writes `._foo.tsx` next to every file. They are binary and break both Metro (expo-router treats `app/._layout.tsx` as a route) and vitest. Guards exist in `artifacts/awaz-khata/metro.config.js` and `artifacts/api-server/vitest.config.ts`; `find . -name '._*' -delete` clears existing ones.
- **Blank white Expo web screenshots** — usually `useFonts` still downloading ~2.5 MB of Nastaliq/Inter TTFs through the dev proxy, not a crash. Wait 20–30 s and retry; do not weaken the `useFonts` + SplashScreen gate. Native (Expo Go) bundles fonts locally and is unaffected.

## Product constraints (from the user's spec)

- **Storage stays a JSON file.** A database migration is explicitly vetoed. `lib/db` exists as workspace scaffolding; the ledger does not use it.
- Spoken save confirmations use the conversational «جی، میں نے سن لیا اور … کھاتے میں ڈال دیے ہیں» wording, built server-side **only after the save succeeds** — never wording implying success before the backend confirms.
- The assistant introduces itself on every app open/refresh (no persisted completed flag; onboarding state must never touch the backend). Web autoplay is blocked without a gesture, so the welcome intro offers a «تعارف سنیں» tap-to-play path on web; only native auto-plays TTS.
- If a client-side spoken ack («جی، میں نے سن لیا۔») is added right after recording stops, split that prefix out of the backend templates so the user does not hear it twice.

The authoritative spec lives in `attached_assets/Pasted--UPDATE-EXISTING-PROJECT-Awaz-Khata-*.txt`; read it before changing storage, voice-flow wording, or the mobile voice pipeline.
