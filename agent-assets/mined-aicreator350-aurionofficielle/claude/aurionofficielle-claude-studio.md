# AURION STUDIO — CONTEXTE SPÉCIFIQUE

## URL
https://studio-aurion1.vercel.app

## ⚠️ STACK DIFFÉRENT
Studio est le SEUL outil en **Next.js + pnpm** (tout le reste = Vite + npm)
- Build : `next build --turbopack`
- ORM : Drizzle
- Style : biome.jsonc (pas ESLint)
- Workspace : pnpm-workspace.yaml

## ARCHITECTURE
- Entry : app/page.tsx → app/studio-page.tsx + app/layout.tsx
- 24 fichiers app/, 122 fichiers components/ (~622 KB)
- hooks/ (8 fichiers), lib/ (20+ fichiers), providers/
- Supabase intégration directe (pas via api/ centralisé)
- Email : React Email
- AI : AI SDK (Bedrock, OpenAI, XAI, Hume, LMNT, Luma)

## API (Next.js routes)
app/api/agents/, app/api/chat/, app/api/code/,
app/api/generate-image/, app/api/generate-video/,
app/api/media-status/, app/api/sync/, app/api/verify-domain/

## FEATURES FONCTIONNELLES
- Visual canvas editor (prompt-to-page)
- 13 built-in templates (newsletter, brand, product launch, YouTube, API docs, Instagram, design system...)
- CMS : getCMSCollectionsFromSupabase() + localStorage dual-write
- Custom domains : dns.resolveCname() + dns.resolveTxt() réels côté serveur
- Collaboration : Supabase Realtime channels (broadcast + presence)
- Preview WYSIWYG : iframe responsive avec breakpoints (7 breakpoints 320px→2560px)
- Gallery masonry, Lightbox, Animations configurables (keyframes)
- Media : image + vidéo generation (Replicate, Luma)

## SCRIPTS
```bash
pnpm dev      # Next.js + Supabase + Email + Stripe
pnpm build    # next build --turbopack
pnpm check    # biome check
pnpm fix      # biome fix
pnpm migrate  # Drizzle migrations
pnpm generate # Drizzle generate
```

## TESTER
1. Ouvrir https://studio-aurion1.vercel.app
2. Créer un projet → tester le canvas
3. Preview responsive → tester les breakpoints
4. Console DevTools = zéro erreur
