# Agent Guide

## Project Goal

This is Miles's SXSW 2024 photo zine: a creative, minimal gallery for live-music photographs, band context, outbound links, and band photo downloads. The photographs are the product. Preserve their quality and make them feel large, sharp, and intentional.

## Non-Negotiables

- Main photographs must display at the largest size that still fully fits within the current viewport.
- Do not crop performance photos. Use `object-contain` unless the image is explicitly a thumbnail or decorative texture.
- Keep image quality high. Prefer better source assets and responsive sizing over compression that visibly degrades photos.
- Local development must be possible from a clean checkout using `.env.example`.
- Public route handlers must validate input and fail with clear status codes.
- Do not add hidden env vars. If code needs a new variable, add it to `.env.example` and README.

## Architecture

- Next.js App Router in `app/`
- Prisma/Postgres schema and seed data in `prisma/`
- Production photos served from S3 through CloudFront
- Local/mock photo mode served from checked-in images under `public/photos`
- Vercel hosts the production app

## Core Commands

```bash
npm ci
npx prisma generate
npx prisma migrate dev
npx prisma db seed
npm run dev
npm run check-types
npm run lint
npm run build
npm run test:e2e
```

## Local Environment

Start by copying `.env.example` to `.env.local`. For fast local UI work, keep `STORAGE_TYPE=local`; this maps seeded picture filenames to checked-in sample photos. For production-like testing, use `STORAGE_TYPE=s3` and fill every AWS/CloudFront variable.

Required for all local runs:

- `DATABASE_URL`
- `DIRECT_URL`
- `STORAGE_TYPE`
- `IP_HASH_SALT`

Required for S3 mode:

- `AWS_REGION`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `S3_BUCKET_NAME`
- `AWS_CLOUDFRONT_DOMAIN`
- `NEXT_PUBLIC_AWS_CLOUDFRONT_DOMAIN`

Required for blob mode:

- `BLOB_READ_WRITE_TOKEN`

## Implementation Preferences

- Prefer Server Components by default. Add `'use client'` only for browser APIs, state, effects, or event handlers.
- Keep Prisma and service SDK clients behind lazy helper functions.
- Validate public API request bodies before touching Prisma or external services.
- Make analytics non-blocking; link navigation should still work if tracking fails.
- Keep UI copy concise and zine-like. Avoid adding in-app explanations of implementation details.

## Testing Expectations

Before handing off a change, run the narrowest meaningful checks. For broad repo work, run:

```bash
npm run check-types
npm run lint
npm run build
```

For visual changes, also run the app locally and inspect mobile, tablet, desktop, and wide desktop. Confirm main photos are uncropped, sharp, and fully visible. Use `npm run test:e2e` after the database is running and seeded.
