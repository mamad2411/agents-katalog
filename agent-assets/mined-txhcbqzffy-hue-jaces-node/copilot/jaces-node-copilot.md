# Copilot Instructions for JACES Fashion Store

Bienvenue ! Ce fichier guide Copilot et les agents IA pour contribuer efficacement à ce projet premium de mode.

## Principes généraux
- **Respecter le style éditorial** : Priorité à un design éditorial premium, typographie élégante, et une expérience immersive.
- **Conserver le français** : Toute l’UI, les prompts, et les textes doivent rester en français.
- **Préserver l’en-tête et le pied de page** : Ne jamais supprimer ou modifier radicalement la structure du header/footer JACES.
- **Favoriser les changements visuels rapides** : Préférer les itérations CSS/HTML rapides pour la présentation des pages mode.

## Conventions projet
- **Aucune dépendance JS externe** : Utiliser uniquement du JS natif, pas de frameworks ou librairies tierces.
- **Organisation** : Un fichier CSS principal (`style.css`), un JS pour les favoris (`favorites.js`), chaque page HTML dédiée à une section.
- **Composants** : Les cartes produits utilisent `.product-card`, les boutons favoris `.product-favorite`, et le badge `.fav-count`.
- **Accessibilité** : Toujours fournir des labels ARIA pour les boutons interactifs.

## Bonnes pratiques
- **Link, don’t embed** : Si une règle existe déjà dans ce fichier ou dans le code, faire référence plutôt que dupliquer.
- **Pas de duplication de styles** : Centraliser les styles dans `style.css`.
- **Favoris** : Utiliser le module `favorites.js` pour toute logique liée aux favoris, sans modifier son API publique.

## Pièges courants
- Ne pas ajouter de dépendances JS/CSS externes.
- Ne pas changer la structure du header/footer.
- Ne pas traduire l’UI en anglais ou autre langue par défaut.

## Exemples de prompts
- "Ajoute un badge favori sur chaque carte produit."
- "Modernise la grille produits en gardant le style JACES."
- "Améliore l’accessibilité des boutons favoris."
- "Ajoute une animation CSS premium à l’ouverture du panneau favoris."

---

Pour toute personnalisation avancée, créez un fichier instruction ou agent dédié (voir `/create-instruction ...`).
