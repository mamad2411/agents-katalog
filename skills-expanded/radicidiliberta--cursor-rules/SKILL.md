# Cursor Rules per "Radici di Libertà"

## Informazioni Progetto

- **Nome:** Radici di Libertà
- **Framework:** Next.js 15 con App Router
- **Linguaggio:** TypeScript
- **Hosting:** Vercel
- **CSS:** Tailwind CSS
- **UI Library:** shadcn/ui
- **Testing:** Jest

## Struttura File

```
radici-di-liberta/
├── app/            # Struttura App Router di Next.js
│   ├── layout.tsx  # Layout principale dell'applicazione
│   ├── page.tsx    # Homepage
│   └── globals.css # Stili globali
├── components/     # Componenti riutilizzabili
│   ├── ui/         # Componenti UI generici da shadcn
│   └── sections/   # Sezioni specifiche della pagina
├── lib/           # Utility, hooks, e logica condivisa
├── public/        # Asset statici
└── tests/         # Test unitari e di integrazione
```

## Convenzioni di Codice

- **Componenti:** PascalCase (es. `Header.tsx`)
- **Hook/Utility:** camelCase (es. `useFormValidation.ts`)
- **File:** kebab-case (es. `contact-form.tsx`)
- **Server Components:** Tutti i componenti sono Server Components per default
- **Client Components:** Prefisso `'use client';` per componenti client-side
- **Server-only:** Aggiungere `import 'server-only';` ai file con logica server-side

## Stile e Design

### Colori
- **Primario:** #4CAF50
- **Secondario:** #2E7D32
- **Accento:** #AED581
- **Sfondo:** #F1F8E9
- **Testo:** #212121

### Componenti
- **Cards:**
  - Border radius: 2rem
  - Shadow: 0px 4px 6px rgba(0,0,0,0.1)
  - Padding: p-6
  
- **Buttons:**
  - Padding: px-6 py-3
  - Border radius: 1rem
  - Font weight: font-semibold

## Sezioni del Contenuto
1. **Hero** - "Rigenerare possibilità e benessere attraverso la natura"
2. **Il Problema** - Sovraffollamento carcerario, recidiva, ecc.
3. **Obiettivi** - Miglioramento dell'umore, aumento di agency, ecc.
4. **Attività Previste** - Cura delle piante, gestione orti, ecc.
5. **Strumenti di Misurazione** - PRS/IT, CNS, PANAS, ecc.
6. **Partner e Finanziamenti**
7. **Contatti** - Form di contatto

## Best Practices

### Accessibilità
- Usare sempre HTML semantico
- Alt text per tutte le immagini
- ARIA labels per elementi interattivi
- Contrasto adeguato per il testo

### TypeScript
- Definire tipi espliciti per tutti i componenti
- Utilizzare file `types.ts` separati per i tipi condivisi
- Validare form e input con Zod

### Next.js
- Utilizzare Server Components dove possibile
- Utilizzare Server Actions per mutazioni di dati
- Evitare API Route quando possibile, preferire Server Components/Actions
- Utilizzare `next/navigation` (non `next/router`)
- Implementare correttamente il caching e revalidazione dei dati

### Testing
- Test unitari per utility e hooks
- Test di integrazione per componenti complessi
- Snapshot tests per UI componenti base

## Commits e CI
- Seguire Conventional Commits
- Linting con ESLint e Prettier
- CI con GitHub Actions per lint e test 