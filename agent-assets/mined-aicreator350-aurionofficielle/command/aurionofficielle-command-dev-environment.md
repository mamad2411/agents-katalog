# Setup Development Environment

Configure l'environnement de développement complet.

## Instructions

1. **Prerequisites**
   - Node.js 20+ : `node -v`
   - npm 9+ : `npm -v`
   - Git : `git --version`
   - pnpm (pour Studio) : `npm i -g pnpm`

2. **Installation principale**
   ```bash
   git clone [repo] && cd aurionOFFICIELLE
   npm install
   cp .env.example .env
   ```

3. **Configuration .env**
   Variables requises :
   - VITE_SUPABASE_URL
   - VITE_SUPABASE_ANON_KEY
   - VITE_CLERK_PUBLISHABLE_KEY
   - VITE_STRIPE_PUBLISHABLE_KEY
   - OPENROUTER_API_KEY (pour les API routes)

4. **Dev servers**
   - Landing + Dashboard : `npm run dev` (port 5173)
   - Outil spécifique : `cd tools-deploy/[outil] && npm run dev`
   - Studio (Next.js) : `cd tools-deploy/studio && pnpm dev`

5. **Vercel CLI**
   - `npm i -g vercel`
   - `vercel login`
   - `vercel link` (dans chaque outil pour le premier deploy)

6. **Claude Code**
   - `npm i -g @anthropic-ai/claude-code`
   - `claude auth login`
   - Les skills sont dans .claude/skills/
   - Les commandes sont dans .claude/commands/

7. **Vérification**
   - `npm run build` → succès
   - `npm run typecheck` → zero erreurs
   - `npm run dev` → page visible sur localhost:5173
