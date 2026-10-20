## Architecture rules

- All data access goes through `src/lib/api.ts`; screens never import `src/mocks` directly. `api.ts` talks to the FastAPI backend when `VITE_API_URL` is set (see `src/lib/http.ts`) and falls back to the mocks (demo mode) otherwise.
- Money comes from the API as decimal strings; `api.ts` converts with `num()` only for display. Do not do money math in the app.
- Split rules mirror the backend: transfers never have split; the split happens when a charge (cobrança) with an invoice (NF-e) is paid, retaining the CBS/IBS stated on the invoice. `src/lib/split.ts` holds the transition table (2026–2033) and is used only for estimates (simulator, loja/viagens demo).
- Login is per person; the current account (PF or a company the person is linked to) goes in the `X-Conta` header. Switching accounts clears the React Query cache.
- Authenticated screens live under the pathless `_app` layout (TanStack Router, not React Router).
- The project no longer depends on Lovable: `vite.config.ts` declares the standard plugins directly.
