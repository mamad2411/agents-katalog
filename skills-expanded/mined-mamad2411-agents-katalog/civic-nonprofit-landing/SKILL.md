---
name: civic-nonprofit-landing
description: Construire une page d'accueil pour une association, une ONG, un service public ou un organisme d'intérêt général. À utiliser quand on demande un site vitrine associatif, une landing page pour une asso, un site pour une organisation à but non lucratif, ou une page de présentation pour une structure d'intérêt général. Fournit la structure en six sections, les règles d'écriture et le design system.
---

# Page d'accueil pour une organisation d'intérêt général

Ce skill produit une page d'accueil complète en HTML/CSS/JS pur, sans framework
ni étape de build, dans un registre sobre et institutionnel.

## Avant de commencer

1. **Lis le design system** : `design-systems/warm-civic.md`, à la racine de ce
   plugin. Il contient la palette, l'échelle typographique, les règles de
   texture et de mouvement. Ne réinvente pas ces valeurs.
2. **Demande les informations manquantes** si l'utilisateur ne les a pas
   fournies : nom de l'organisation, forme juridique, ce qu'elle fait en une
   phrase, qui elle accompagne, et l'affirmation centrale qu'elle mettrait sur
   une affiche.
3. Si l'utilisateur préfère travailler en français, la version française de ce
   prompt est dans `prompts/civic-nonprofit-landing/prompt.fr.md`.

## Livrable

Un `index.html` autonome, plus `assets/css/style.css` et `assets/js/main.js`.
Aucun framework, aucune bibliothèque CSS. La page doit fonctionner en l'ouvrant
directement depuis le système de fichiers.

## Structure — six sections, dans cet ordre

1. **En-tête collant.** Logotype avec un glyphe SVG géométrique, cinq liens,
   un bouton de thème, un appel à l'action. Flou d'arrière-plan ; bordure et
   ombre uniquement une fois la page défilée. Sous 900px, menu burger avec
   panneau coulissant.

2. **Hero, deux colonnes asymétriques.** À gauche : intitulé de rubrique, h1 de
   huit à douze mots avec exactement un mot surligné au marqueur, chapô de deux
   phrases, deux boutons, rangée de trois chiffres clés séparée par un filet.
   À droite : illustration SVG inline originale. Deux taches floutées derrière.

   Le h1 énonce la position de l'organisation, jamais son nom.

3. **Le constat, bande teintée.** Introduction centrée, puis trois cartes
   numérotées — grands chiffres en accent, sans icône — qui exposent
   l'enchaînement causal du problème traité.

4. **Les programmes, grille deux par deux.** Quatre cartes : icône dans une
   tuile arrondie teintée, titre, description de trois lignes, lien fléché qui
   glisse au survol. Faire varier la couleur des tuiles.

5. **L'impact, bande sombre pleine largeur.** Quatre chiffres avec comptage
   animé au défilement, plus une ligne indiquant la source ou la date d'arrêté.

6. **Appel final.** Panneau arrondi avec lueur floutée dans un angle, titre,
   deux phrases, deux boutons. Puis pied de page en quatre colonnes.

## Règles d'écriture

C'est là que la plupart des pages générées échouent.

- **Prose concrète, jamais de registre publicitaire.** Écris comme la personne
  qui fait le travail le décrirait, pas comme une agence de communication.
- **Vocabulaire interdit :** innovant, à la pointe, fluide, accompagner vers
  l'excellence, révolutionner, holistique, synergie, parcours, solution,
  libérer le potentiel, écosystème. En anglais : innovative, cutting-edge,
  seamless, empower, journey, unlock, transform, holistic.
- **Toujours le détail précis plutôt que l'abstraction.** « Mardi 9h-12h, sans
  rendez-vous » vaut mieux que « des modalités d'accompagnement souples ».
  « Apportez vos papiers, même en désordre » vaut mieux que « nous accueillons
  toutes les situations ».
- **L'appel final nomme un besoin réel, petit et concret** — un manque précis
  que le lecteur pourrait combler cette semaine, pas un appel général.
- **Chaque titre est une pensée complète.** « Nos actions » n'est pas un titre ;
  « Quatre programmes, un même fil conducteur » en est un.
- Aucun point d'exclamation, aucune question rhétorique, aucun emoji.

## Exigences techniques

- Couleur, typographie et espacement pilotés par des variables CSS déclarées une
  seule fois dans `:root`. Changer l'identité ne doit demander que ce bloc.
- Échelle typographique fluide en `clamp()`, aucune media query sur les tailles.
- Thème sombre via `data-theme="dark"` sur `<html>`, bouton dans l'en-tête,
  préférence en `localStorage`, et un script inline dans le `<head>` qui applique
  le thème avant le premier rendu pour éviter le flash blanc.
- CSS Grid avec `repeat(auto-fit, minmax(min(Npx, 100%), 1fr))`. **Vérifie le
  nombre de colonnes obtenu par rapport au nombre réel de cartes** — une grille
  de quatre cartes qui tombe sur trois colonnes laisse un orphelin.
- Révélation au défilement via `IntersectionObserver`, avec repli qui affiche
  tout si l'API est absente.
- Les compteurs portent la **valeur finale dans le HTML**, le JS animant depuis
  zéro. Jamais un `0` écrit en dur dans le balisage.
- Illustrations en SVG inline écrit à la main. Aucune image externe, aucune photo
  de banque d'images, aucun visage généré.
- Accessibilité : lien d'évitement, focus visible, `aria-current` sur le lien
  actif, champs étiquetés, menu au clavier avec fermeture par Échap, et un bloc
  `prefers-reduced-motion` qui désactive toutes les transitions.
- Responsive jusqu'à 390px, sans défilement horizontal.

## Honnêteté du contenu

Si tu inventes des noms, chiffres, adresses ou dates comme gabarit, place un
commentaire HTML en haut du fichier pour le dire clairement. Ne présente jamais
des statistiques ou des témoignages fabriqués comme réels.

Si la page comporte une section de don, ne construis pas de formulaire de
paiement. Renvoie vers un prestataire agréé et indique sur la page qu'aucun
paiement n'y est traité. Ne collecte jamais de coordonnées bancaires.

## Avant de rendre

Relis les textes et supprime chaque phrase qui pourrait figurer sur le site de
n'importe quelle autre organisation. Ce qui reste est la page.

Les captures de référence sont dans `prompts/civic-nonprofit-landing/preview/`.
