---
description: "camofox-browser REST API endpoint reference — all endpoints on port 9377"
alwaysApply: false
---

# REST API Endpoints (Source-Verified)

Base URL: `http://localhost:9377`

## Core (`src/routes/core.ts`)

| Method | Endpoint |
|---|---|
| POST | `/sessions/:userId/cookies` |
| GET | `/tabs/:tabId/cookies` |
| GET | `/health` |
| GET | `/presets` |
| POST | `/tabs` |
| GET | `/tabs` |
| POST | `/tabs/:tabId/navigate` |
| GET | `/tabs/:tabId/snapshot` |
| POST | `/tabs/:tabId/wait` |
| POST | `/tabs/:tabId/click` |
| POST | `/tabs/:tabId/type` |
| POST | `/tabs/:tabId/press` |
| POST | `/tabs/:tabId/scroll` |
| POST | `/tabs/:tabId/scroll-element` |
| POST | `/tabs/:tabId/evaluate` |
| POST | `/tabs/:tabId/evaluate-extended` |
| POST | `/tabs/:tabId/back` |
| POST | `/tabs/:tabId/forward` |
| POST | `/tabs/:tabId/refresh` |
| GET | `/tabs/:tabId/links` |
| GET | `/tabs/:tabId/screenshot` |
| GET | `/tabs/:tabId/stats` |
| DELETE | `/tabs/:tabId` |
| DELETE | `/tabs/group/:listItemId` |
| DELETE | `/sessions/:userId` |
| POST | `/sessions/:userId/toggle-display` |
| GET | `/tabs/:tabId/downloads` |
| GET | `/users/:userId/downloads` |
| GET | `/downloads/:downloadId` |
| GET | `/downloads/:downloadId/content` |
| DELETE | `/downloads/:downloadId` |
| POST | `/tabs/:tabId/extract-resources` |
| POST | `/tabs/:tabId/batch-download` |
| POST | `/tabs/:tabId/resolve-blobs` |

## OpenClaw (`src/routes/openclaw.ts`)

| Method | Endpoint |
|---|---|
| GET | `/` |
| POST | `/tabs/open` |
| POST | `/start` |
| POST | `/stop` |
| POST | `/navigate` |
| GET | `/snapshot` |
| POST | `/act` |

## Common Request Patterns

- Tab-targeted routes require user-scoped lookup (`tabId` + `userId`).
- Snapshot/click/type/press/scroll are intended to run in a loop with fresh refs.
- `navigate` supports direct URL or macro expansion (`macro` + `query`).

## Auth Rules

- If `CAMOFOX_API_KEY` is set, cookie import/export and evaluate routes require `Authorization: Bearer <key>`.
- OpenClaw `POST /stop` always requires `x-admin-key` and compares it to configured admin key value.
- If keys are unset, routes are open except OpenClaw `POST /stop`, which still requires `x-admin-key`.
