# Créer une PR

Crée une Pull Request complète avec description et contexte.

## Instructions

Paramètre : $ARGUMENTS (titre de la PR)

1. **Pré-PR checks**
   - `npm run typecheck` → zero erreurs
   - `npm run build` → succès
   - `git status` → tous les fichiers committés

2. **Branche**
   - Si pas sur une feature branch : `git checkout -b feat/[slug]`
   - Push la branche : `git push origin [branch]`

3. **Description de la PR**
   ```markdown
   ## Description
   [Résumé clair de ce que fait cette PR]

   ## Changements
   - [fichier] : [ce qui a changé et pourquoi]

   ## Type de changement
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation

   ## Tests
   - [ ] `npm run typecheck` passe
   - [ ] `npm run build` passe
   - [ ] Test manuel effectué

   ## Screenshots (si UI)
   [si applicable]
   ```

4. **Création**
   - `gh pr create --title "$ARGUMENTS" --body "[description]"`
   - Affiche le lien de la PR
