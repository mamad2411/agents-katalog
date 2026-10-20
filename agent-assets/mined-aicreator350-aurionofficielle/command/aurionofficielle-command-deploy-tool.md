# Deploy Tool

Déploie un outil spécifique ou tous les outils sur Vercel.

## Instructions

Paramètre : $ARGUMENTS (nom de l'outil ou "all")

1. **Si $ARGUMENTS = "all" ou vide**
   - Lance `node scripts/deploy-all-tools.cjs`
   - Ou `npm run deploy:everything` pour landing + tous les outils

2. **Si $ARGUMENTS = nom d'un outil**
   - `cd tools-deploy/$ARGUMENTS`
   - Vérifie quel type (Vite ou Next.js/Studio)

3. **Build**
   - Vite : `npm run build`
   - Studio (Next.js) : `pnpm build`

4. **Typecheck**
   - `npm run typecheck` (ou `pnpm check` pour Studio)
   - Zéro erreur obligatoire

5. **Deploy**
   - `npx vercel --prod --yes`
   - Attends l'URL de production
   - Vérifie que l'URL répond (curl ou fetch)

6. **URLs de production**
   | Outil | URL |
   |-------|-----|
   | chat | chat-aurion1.vercel.app |
   | ide | ide-aurion1.vercel.app |
   | agent-ai | agent-ai-cyan.vercel.app |
   | text-editor | text-editor-aurion1.vercel.app |
   | studio | studio-aurion1.vercel.app |
   | uiforge | uiforge-eight.vercel.app |
   | 1code | 1code-omega.vercel.app |
   | code-editor | code-editor-aurion1.vercel.app |
   | cowork | cowork-mauve.vercel.app |
   | ai-marketing | ai-marketing-xi.vercel.app |

7. **Post-deploy**
   - Met à jour PROGRESS.md avec le status du deploy
   - Note l'heure et la version déployée
