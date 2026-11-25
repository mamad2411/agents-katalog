<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-agomezsittima
description: CTF writeups and security challenges by AGomezSittima.
---

# Writeups by AGomezSittima

Source repository: `/repos/AGomezSittima`

## Repository Index

- the-road-to-next-app/README.md

## Writeup Content


### File: the-road-to-next-app/README.md

# TicketBounty

A bug-bounty–style marketplace for reporting issues and rewarding fixes. Built with Next.js, React, TypeScript, Prisma, and Tailwind CSS.

> This project is based on the course [The Road to Next](https://www.road-to-next.com/) and is used to explore Next.js 15 and React 19 features, with additional modifications.

---

## How to start

- **Prerequisites:** Node.js (22+), `pnpm` recommended (or `npm`).
- Copy environment variables:

```bash
cp .env.example .env
```

- Install dependencies with `pnpm` (or `npm`):

```bash
pnpm install
# or
npm install
```

- Run development server:

```bash
pnpm dev
# or
npm run dev
```

- Open http://localhost:3000 in your browser.

---

## Tech Stack

- Next.js (App Router)
- React + TypeScript
- Tailwind CSS
- Prisma
- Inngest, Stripe, AWS, Resend

## Project structure

A high-level folder diagram of the repository:

```
.
├─ src/
│  ├─ actions/        # server actions, cookies
│  ├─ app/            # app pages (Next.js App Router)
│  ├─ components/     # shared UI components (form, ui, pagination, theme)
│  ├─ emails/         # email templates and components
│  ├─ features/       # feature-scoped modules (auth, tickets, organization, etc.)
│  ├─ hooks/          # custom React hooks
│  ├─ lib/            # third-party clients and helpers (Prisma, Stripe, AWS)
│  ├─ types/          # shared TypeScript types
│  └─ utils/          # helper utilities and path helpers
├─ prisma/
│  ├─ schema.prisma
│  └─ seed.ts
├─ public/            # static assets
└─ ...
```

## Commands

| Command       | Action                              |
| ------------- | ----------------------------------- |
| `dev`         | Run development server              |
| `build`       | Build production assets             |
| `start`       | Start production server             |
| `lint`        | Run ESLint on `src`                 |
| `lint-fix`    | Run ESLint with `--fix` on `src`    |
| `type`        | Type-check TypeScript               |
| `postinstall` | Run `prisma generate` after install |
| `prisma-seed` | Run prisma seeding script           |
| `stripe-seed` | Seed Stripe test data               |
| `seed`        | Run both seeds                      |
| `prettier`    | Format code with Prettier           |
| `email`       | Run email dev tool                  |

> If you use `pnpm`, scripts are available via `pnpm <script>`; use `npm run <script>` if you prefer npm.

---

## Demo

If you want to try the application without running it locally, visit the live demo: https://ticketbounty.agomezsittima.dev

> Attachments, email sending, and Stripe integration are not configured in the demo environment, so some features are disabled.

### Demo credentials

The demo database includes seeded accounts you can use to sign in:

| Role  | Email | Password |
|---|---:|:---|
| Admin | `admin@admin.com` | `secret123` |
| User  | `user@user.com`  | `secret123` |

These accounts are created by the seed script in `prisma/seed.ts`.

