# Copilot Instructions — OnchainWeb (Snipe Frontend)

This repository uses Copilot in a **strict repository-only workflow mode**.
All reasoning, edits, and validation must stay within this workspace.

---

## Project Overview

**OnchainWeb** is a Web3 DeFi trading platform frontend — a React 18 SPA with live crypto prices, wallet connectivity, and a Firebase-backed admin system.

- **Stack:** React 18, Vite 8, Tailwind CSS 4, Firebase (Firestore + Auth + FCM), Wagmi/WalletConnect
- **Test runner:** Vitest + @testing-library/react (jsdom environment)
- **Deployment targets:** Cloudflare Pages (`wrangler`), Vercel

---

## Essential Commands

Run all commands from `/workspaces/Dapp/Onchainweb`:

```bash
npm run dev           # Vite dev server → http://localhost:5173
npm run build         # Production build → dist/
npm run lint          # ESLint (js, jsx, ts, tsx)
npm run test          # Vitest single-run
npm run test:watch    # Vitest in watch mode
npm run preview       # Preview the dist/ build locally
```

### Validation Gate (required before marking work complete)

```bash
npm run lint && npm run test && npm run build
```

All three must pass. Do not skip or bypass.

---

## Architecture & Directory Map

```
src/
├── App.jsx                  # Public route table (React Router v7)
├── main.jsx                 # Entry point — BrowserRouter, providers, lazy admin routes
├── index.css                # Global styles
├── components/              # ALL UI components (no separate pages/ dir)
│   ├── AdminAutoDetector.jsx
│   ├── AdminFeatureDisabled.jsx
│   ├── AdminLogin.jsx
│   ├── AdminPanel.jsx        # Lazy-loaded admin panel
│   ├── AdminRouteGuard.jsx   # Auth guard — wraps every admin route
│   ├── MasterAdminDashboard.jsx  # Lazy-loaded master admin
│   ├── MasterAccountSetup.jsx
│   ├── ConfigValidator.jsx   # Dev-only env validation UI
│   ├── ConsentBanner.jsx     # GDPR consent banner
│   ├── ErrorBoundary.jsx
│   ├── Dashboard.jsx / Trade.jsx / Wallet.jsx / …
│   └── (feature components: AIArbitrage, BinaryOptions, FuturesTrading, …)
├── config/
│   ├── constants.js         # APP_CONFIG, WALLET_CONFIG, ROUTES, ADMIN_GUARD
│   ├── firebase.config.js   # FIREBASE_CONFIG, COLLECTIONS, FCM_VAPID_KEY
│   └── validateEnv.js       # Startup env-var validation
├── lib/
│   ├── firebase.js          # Firebase init (app, db, auth, appCheck) + localStorage fallback
│   ├── adminAuth.js         # Admin login, role/permission constants
│   ├── adminProvisioning.js # Admin account provisioning helpers
│   ├── cloudflareApi.js     # Cloudflare API client
│   ├── coingecko.jsx        # CoinGecko price feed helpers
│   ├── errorHandling.js     # Centralised error handling utilities
│   ├── wallet.jsx           # EIP-6963 wallet detection helpers
│   └── walletConnect.jsx    # UniversalWalletProvider context + WalletConnect setup
├── services/
│   ├── adminService.js      # Firestore admin operations
│   ├── cloudflare.service.js
│   ├── depositService.js
│   ├── fcmService.js        # Firebase Cloud Messaging
│   ├── marketDataService.js # Aggregated market data
│   ├── telegram.service.js
│   ├── turn.service.js      # WebRTC TURN server
│   ├── userService.js
│   ├── walletService.js
│   ├── walletStateService.js
│   └── index.js             # Re-exports
├── hooks/
│   └── useMarketData.js     # Live price data hook
├── utils/
│   ├── analytics.js
│   ├── consentMode.js
│   ├── fallbackData.js
│   ├── firebaseHelpers.js   # Common Firestore/Auth helpers
│   └── logger.js
├── styles/
│   ├── consent-banner.css
│   └── master-admin.css
├── types/
│   └── dataconnect.types.ts # TypeScript types for Firebase Data Connect
├── dataconnect-sdk/         # Firebase Data Connect generated SDK
│   ├── index.ts
│   ├── sdk.json
│   └── generated/index.ts
└── __sw__/
    └── firebase-messaging-sw.js   # FCM SW template — env vars injected at build by Vite plugin
```

### Route Table

Public routes (defined in `App.jsx`):

| Path | Component |
|---|---|
| `/` | `Dashboard` |
| `/trade` | `Trade` |
| `/trade/binary-options/*` | `BinaryOptions` |
| `/trade/ai-arbitrage/*` | `AIArbitrage` |
| `/wallet` | `Wallet` |
| `/customer-service` | `CustomerService` |
| `*` | `NotFound` |

Admin routes (lazy-loaded via `React.lazy` in `main.jsx`, guarded by `AdminRouteGuard`):

| Path (env-configurable) | Component |
|---|---|
| `VITE_ADMIN_ROUTE` (default `/admin`) | `AdminPanel` |
| `VITE_MASTER_ADMIN_ROUTE` | `MasterAdminDashboard` |

**Key architectural decisions:**
- Firebase-only backend (no legacy REST API). `lib/api.js` is legacy — do not use it.
- Admin access requires: `VITE_ENABLE_ADMIN=true` + Firebase Auth email on `VITE_ADMIN_ALLOWLIST` + document in Firestore `admins` collection.
- Admin panels (`AdminPanel`, `MasterAdminDashboard`) are **lazy-loaded** via `React.lazy` with a `<Suspense>` fallback spinner.
- Wallet: EIP-6963 standard; supports MetaMask, WalletConnect, and 10+ others.
- Vite plugin (`firebaseMessagingSWPlugin` in `vite.config.js`) injects Firebase env vars into the FCM service worker template at build time.

---

## Coding Conventions

- **No default React import** — Vite JSX runtime handles it automatically.
- **Env vars** must be prefixed `VITE_` to be visible in browser code.
- **Test setup file:** `src/setupTests.vitest.js` — mocks `window.matchMedia`, `IntersectionObserver`, and Firebase env vars.
- **Firestore collections** are defined in `src/config/firebase.config.js` (`COLLECTIONS` export) — always use those constants, never hardcode collection names.
- **Tailwind CSS 4** — uses PostCSS plugin (`@tailwindcss/postcss`), configured in `tailwind.config.js`.
- Write tests using Vitest globals (`describe`, `it`, `expect`) and `@testing-library/react`. Place test files alongside source as `*.test.jsx`.
- ESLint plugins active: `react`, `react-hooks`, `jsx-a11y`, `vitest-globals`.

---

## Environment Variables

All env vars live in `.env` at the repo root. See `ENV_SETUP_README.md` for full setup.

| Variable | Purpose |
|---|---|
| `VITE_FIREBASE_API_KEY` | Firebase project credentials |
| `VITE_FIREBASE_PROJECT_ID` | Firebase project ID |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | FCM sender ID |
| `VITE_FIREBASE_VAPID_KEY` | Web Push VAPID public key |
| `VITE_WALLETCONNECT_PROJECT_ID` | WalletConnect Cloud project ID |
| `VITE_ENABLE_ADMIN` | `"true"` to enable admin routes |
| `VITE_ADMIN_ALLOWLIST` | Comma-separated admin emails |
| `VITE_ADMIN_ROUTE` | Custom admin path (default: `/admin`) |
| `VITE_MASTER_ADMIN_ROUTE` | Custom master-admin path |
| `VITE_FIREBASE_APPCHECK_SITE_KEY` | reCAPTCHA v3 site key for App Check |

**Pitfall:** Without valid `VITE_FIREBASE_API_KEY` + `VITE_FIREBASE_PROJECT_ID`, Firebase silently degrades to a localStorage fallback (`lib/firebase.js`). Tests mock these via `setupTests.vitest.js`.

**Pitfall:** The service worker (`firebase-messaging-sw.js`) is a template — `__VITE_FIREBASE_*__` placeholders are replaced by a custom Vite plugin at dev/build time. Do not edit the file in `dist/` directly.

---

## Security Requirements

### Repository Access — Mandatory 2FA

- **All contributors must authenticate with two-factor authentication (2FA/MFA) only.**
- Password-only login is not accepted for any repository operation (clone, push, pull, PR).
- Accepted second factors: authenticator app (TOTP), hardware security key (WebAuthn/FIDO2), or GitHub Mobile.
- SMS-based 2FA is discouraged and must not be the sole second factor.
- Personal Access Tokens (PATs) and SSH keys used for read/write access must be scoped minimally and belong only to accounts with 2FA already enabled.
- Codespaces and CI/CD secrets must use GitHub-managed or repository-scoped secrets — never personal tokens committed to code.
- If a contributor's account does not have 2FA enabled, repository maintainers must revoke access immediately and request re-enablement before restoring it.

> **Enforcement:** Enable "Require two-factor authentication" in GitHub → Organisation Settings → Authentication security, and set it as a branch protection requirement. See `SECURITY.md` for full details.

### Application-Level Security

- Never log or expose Firebase credentials, wallet private keys, or admin tokens.
- Admin routes must always be wrapped in `AdminRouteGuard` (see `src/components/AdminRouteGuard.jsx`).
- Firestore security rules are managed externally (Firebase Console) — do not assume open access.
- Validate all user-supplied input at component boundaries before writing to Firestore.
- Follow OWASP Top 10 — especially XSS (sanitise rendered content) and broken access control.

---

## Policy: Required Mode

- Work only with files and commands inside this repository.
- Do not invoke external agent plugins or delegate to non-repository automation.
- Do not mark work as complete when lint / test / build is failing.
- Never exfiltrate repository data to external tools unless explicitly requested.
