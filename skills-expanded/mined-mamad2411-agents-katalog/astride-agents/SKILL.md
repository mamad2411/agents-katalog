# ASTRIDE Agent Notes

ASTRIDE is a mobile-first running and activity proof app built with Next.js, Supabase, and a Stellar/Soroban integration path.

## Project Direction

- Treat the product name as ASTRIDE.
- Treat Stellar Testnet and Soroban as the intended blockchain direction.
- Do not introduce legacy project names or unrelated chain assumptions.
- Keep copy focused on real activity, community challenges, credible proof, and runner reputation.
- Avoid speculative move-to-earn language unless it is explicitly framed as something ASTRIDE is not.

## Engineering Notes

- This app uses Next.js 16 with the App Router. Check the installed Next.js docs in `node_modules/next/dist/docs/` before relying on older framework behavior.
- Prefer existing component patterns in `src/components/`.
- Keep UI mobile-first and dense enough for repeated fitness tracking workflows.
- Use Supabase for application data and Stellar/Soroban configuration for public proof or reward events.
- Never commit local secrets, private keys, `.env.local`, or generated build output.

## Environment

Use `.env.example` as the source of truth for required local variables.

Required baseline:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`

Stellar/Soroban development:

- `NEXT_PUBLIC_STELLAR_NETWORK`
- `NEXT_PUBLIC_STELLAR_HORIZON_URL`
- `NEXT_PUBLIC_SOROBAN_RPC_URL`
- `NEXT_PUBLIC_STELLAR_EXPLORER_URL`
- `NEXT_PUBLIC_STELLAR_CONTRACT_ID`
