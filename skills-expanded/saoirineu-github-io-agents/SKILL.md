# AGENTS

## Purpose

This repository contains a Firebase-backed knowledge app with a Vite/React/TypeScript frontend in `frontend/` plus documentation and ontology/data assets at the repository root.

Agents working here should optimize for small, verified changes and preserve user work already in progress.

## Architecture

- The frontend is the primary runtime surface.
- Keep Firebase Auth and Firestore access in `frontend/src/lib/`.
- Keep route pages thin: query orchestration, mutations, and composition in the page; form mapping and large JSX sections in nearby modules.
- Reuse shared normalization helpers such as `frontend/src/lib/firestoreData.ts` instead of duplicating Firestore shaping logic.
- See `docs/arquitetura-frontend.md` for detailed frontend structure and examples.
- See `docs/firestore-schema.md` when changing collections or document fields.

## Build And Test

- `make serve` starts the frontend dev server.
- `cd frontend && npm run build` is the primary validation command.
- `cd frontend && npm run test` runs the Vitest helper suite.
- `cd frontend && npm run lint` must stay clean; it runs with `--max-warnings 0`.
- `make firestore-rules` deploys Firestore rules.
- `make storage-rules` deploys Firebase Storage rules.
- `make firebase-rules` deploys both Firestore and Storage rules.
- `make deploy-functions` builds and deploys Cloud Functions.
- `make deploy-backend` deploys Firestore rules, Storage rules, and Cloud Functions.
- `make mail-relay-secret` pushes the mail relay's shared secret (see Safety).

## Conventions

- Prefer strict typing over `any` casts.
- Keep Portuguese UI copy and the existing Tailwind-heavy styling approach.
- Show dates through `frontend/src/lib/dateFormat.ts` and edit them with `components/DateInput.tsx`: dd/MMM/yyyy in pt/es/it, MMM/dd/yyyy in en, following the site language rather than the browser's. Avoid `toLocaleString` and visible native `type="date"` inputs. Store dates as YYYY-MM-DD.
- Store pure form/payload helpers beside their page domain, using the `pages/<domain>/form.ts` pattern.
- Add tests around pure helpers before expanding refactors; current baseline lives beside the helper modules as `*.test.ts`.
- Link to existing docs instead of duplicating them in new instruction files.

## Safety

- Keep changes focused; do not reformat unrelated files.
- Check local changes before editing active feature files.
- Active work area: the generic events engine (`frontend/src/lib/events.ts`, `frontend/src/lib/eventRegistrations.ts`, `frontend/src/lib/leaderReview.ts`, `frontend/src/pages/events/`, `EventRegistrationPage.tsx`, `EventsAdminPage.tsx`, `LeaderReviewPage.tsx`). Check recent git history before editing these. (The bespoke European Gathering code was retired in June 2026 — EG is now the `events/encontro-europeu-2026` instance.)
- Work records (`trabalhos`, `WorksPage.tsx`, `pages/works/`, `lib/churchManagers.ts`, `lib/workTypes.ts`) book Daime through the `onWorkSacramentChange` Cloud Function, which owns `sacramentTransactions/work-{workId}`. Never write those movements from the client; the rules keep the ledger custodian-only. Read [docs/work-records.md](docs/work-records.md) for the access model and known limitations.
- Donations to ICEFLU Brazil (`icefluDonations`, `DonationsPage.tsx`, `pages/donations/`, `lib/donations.ts`) share that access model through `providers/useChurchRecordAccess.ts`. Their receipts live in Storage under `churches/{churchId}/donations/{donationId}/`, and the Storage rules refuse overwrites so a reviewed donation's proof cannot be swapped. See [docs/iceflu-donations.md](docs/iceflu-donations.md).
- Do not modify generated files unless they change as a result of a validated command.
- Email does not go over SMTP. Cloud Functions POST to a PHP relay hosted on the santodaime.it cPanel (`scripts/portal-mail/`), because Serverplan blocks Google's egress IPs. Deploying functions does **not** update that endpoint — it is uploaded by hand through cPanel — and its shared secret is mirrored in two places that must change together. Send mail only through `deliverOrQueue()` (the mail queue, with retries and guards), never `sendPortalMail()` directly. Read [docs/email-delivery.md](docs/email-delivery.md) before touching either or anything under `scripts/portal-mail/`. `make test-mail-queue` runs the queue against the Firestore emulator.
- Use route-level lazy loading and domain splits before accepting bundle growth.

## Key Paths

- `frontend/src/lib/`: Firebase and Firestore access helpers
- `frontend/src/pages/`: route-level screens and nearby helper modules
- `frontend/src/components/`: reusable UI shell components
- `frontend/src/providers/`: auth and shared context state
- `docs/`: architecture, schema, and agent-facing reference docs

## Docs

- Update this file when commands, architectural boundaries, or sensitive areas change.
- Prefer linking `docs/arquitetura-frontend.md`, `docs/firestore-schema.md`, and `docs/agentes-e-customizacoes.md` instead of copying their content here.
