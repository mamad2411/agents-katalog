# SovereignSolar.lv — Cursor Rules

## Projekts
Saules paneļu cenu salīdzināšanas un lead gen portāls Latvijai.
Lietotājs aizpilda formu → admin apstrādā → partneri saņem pieteikumu → 24h piedāvājums.

## Tech Stack
- React 18 + Vite 6
- Tailwind CSS v3 + shadcn/ui (komponenti no @/components/ui)
- React Router v6 (BrowserRouter)
- TanStack React Query v5
- framer-motion v11 (animācijām)
- lucide-react (ikonām)
- react-hook-form + zod (formām)

## Lietotāju lomas
- publisks → / (Home, RequestForm)
- admin → /admin (AdminDashboard)
- user → /user (UserDashboard)
- partner → /partner (PartnerDashboard)

## Projekta struktūra
```
src/
  api/           ← ⚠️ BASE44 ZONA — neskar bez norādījuma
  components/    ← droši rediģēt
    admin/       ← AdminOverview, ClientRequestsTab, OffersTab utt.
    ui/          ← shadcn/ui komponenti
  pages/         ← React Router lapas
    blog/        ← Blog raksti (Post*.jsx)
  lib/           ← AuthContext, utils, query-client
  hooks/         ← Custom hooks
  utils/         ← Palīgfunkcijas
```

## ⚠️ BASE44 BRĪDINĀJUMS
Src/api/ izmanto @base44/sdk — migrācija uz Supabase plānota.
NEKAD nepievieno jaunus base44 izsaukumus.
NEKAD neimportē no @base44/sdk vai @base44/vite-plugin.
Ja izmaiņa skar src/api/ — apstājies un jautā lietotājam.

## Koda noteikumi
- Funkcionālie komponenti ar arrow functions
- Props destrukturē tieši parametros
- cn() no @/lib/utils Tailwind klašu apvienošanai
- Komponenti zem 150 rindām — ja lielāks, sadalīt
- Guard clauses nevis nested if/else
- Async: vienmēr try/catch ar error state
- shadcn/ui no @/components/ui — neraksti custom button/input no jauna
- UI teksti latviešu valodā
- Absolūtie imports (@/components/..., @/lib/..., @/pages/...)

## Commit formāts
- Valoda: latviešu
- Prefiksi: feat:, fix:, refactor:, style:, docs:
- Piemērs: "feat: pievienots 24h countdown pieteikumu sarakstam"

## Aizliegumi
- NEKAD class components
- NEKAD inline styles (izmanto Tailwind)
- NEKAD jaunas npm pakotnes bez apstiprinājuma
- NEKAD vairāku failu izmaiņas vienā reizē
- NEKAD src/api/ izmaiņas bez skaidra norādījuma

## Pirms raksti kodu
1. Pārbaudi vai izmaiņa skar src/api/
2. Ja jā — apstājies un jautā
3. Ja nē — turpini ar VIENU failu
4. Raksti plānu pirms koda
