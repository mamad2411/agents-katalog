Déploie l'outil dans le répertoire courant sur Vercel.

1. Vérifie quel outil (Vite ou Next.js/Studio)
2. Lance le build :
   - Vite : `npm run build`
   - Studio : `pnpm build`
3. Lance typecheck : `npm run typecheck` (ou `pnpm check` pour Studio)
4. Vérifie zéro erreur dans les deux étapes
5. Déploie : `npx vercel --prod --yes`
6. Attends l'URL de production
7. Affiche l'URL finale et le statut

Pour déployer TOUS les outils : `node scripts/deploy-all-tools.cjs`
Pour déployer TOUT (landing + outils) : `npm run deploy:everything`
