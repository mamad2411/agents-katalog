Fais un audit complet de l'outil dans le répertoire courant.

1. Lis le CLAUDE.md du répertoire courant pour comprendre l'architecture
2. Lis docs/gaps.md pour connaître les gaps existants
3. Lance `npm run build` (ou `pnpm build` pour Studio) et vérifie zéro erreur
4. Lance `npm run typecheck` et vérifie zéro erreur TypeScript
5. Ouvre l'URL déployée dans un navigateur et vérifie :
   - Console DevTools = zéro erreur rouge
   - Network = zéro 404
   - Toutes les features listées dans CLAUDE.md fonctionnent
6. Compare avec le concurrent direct :
   - Chat → Claude.ai / ChatGPT
   - IDE → Cursor / Windsurf
   - Agent → n8n / CrewAI
   - Text Editor → Notion
   - Studio → Webflow / Framer
7. Mets à jour docs/gaps.md avec les résultats
8. Retourne un tableau : score actuel / score concurrent / 3 priorités immédiates
