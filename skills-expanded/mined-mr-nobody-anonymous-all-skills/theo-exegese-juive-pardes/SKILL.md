---
name: theo-exegese-juive-pardes
description: "Orchestre une exégèse juive multicouche des textes bibliques en utilisant la méthode traditionnelle du PaRDeS (acronyme formalisé par Moïse de León). Se déclenche lors des demandes d'analyse d'un texte selon la tradition juive, le Midrash, la Kabbale, ou en demandant spécifiquement le cadre PaRDeS."
category: religious-studies
domain: religious-studies
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "ronanguilloux/skill-theo"
  commit: "02d02caf16"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


## When to Use
- Lorsqu'il est demandé d'analyser une section de la Torah (Parasha), un verset (Pasuk) ou un récit biblique en utilisant l'exégèse juive traditionnelle, y compris dans le Nouveau Testament lorsqu'il est interprété à travers une lentille juive.
- Lorsque l'utilisateur demande explicitement une analyse selon le PaRDeS, des perspectives midrashiques (*Nigleh*, la dimension révélée), des éclairages kabbalistiques (*Nistar*, la dimension cachée) ou des commentaires rabbiniques traditionnels.

## When NOT to Use
- Lorsque l'utilisateur demande une analyse académique historico-critique (Hypothèse documentaire) sans contexte juif traditionnel.
- Lors de l'analyse de textes non-biblique.
- Lorsqu'il est demandé d'effectuer une analyse grammaticale générique en dehors d'un contexte d'exégèse.

## Workflow / Core Loop

1. **Analyser le texte cible** : Identifiez le verset ou passage biblique spécifique que l'utilisateur souhaite analyser. Récupérez le texte hébreu original s'il n'est pas fourni, car le PaRDeS s'appuie fortement sur la formulation hébraïque originale.
2. **Exécuter le Peshat** : Lisez le fichier `references/peshat.md`. Appliquez ses instructions pour extraire le sens littéral, grammatical et contextuel du texte. Documentez vos résultats.
3. **Exécuter le Remez** : Lisez le fichier `references/remez.md`. Appliquez ses instructions pour trouver des significations allégoriques, des interprétations philosophiques ou des indices numériques/structurels (Guématria, Notarikon). Documentez vos résultats.
4. **Exécuter le Derash** : Lisez le fichier `references/derash.md`. Appliquez ses instructions pour mettre en évidence les interprétations homilétiques, éthiques et midrashiques (Talmud, Midrash Rabba). Documentez vos résultats.
5. **Exécuter le Sod** : Lisez le fichier `references/sod.md`. Appliquez ses instructions pour révéler les dimensions mystiques, kabbalistiques et ésotériques (Zohar, Sefirot). Documentez vos résultats.
6. **Synthétiser** : Compilez les quatre niveaux d'interprétation en un rapport d'exégèse structuré. Utilisez les structures et l'intériorité révélées par le niveau *Sod* pour unifier les enseignements des trois niveaux précédents (Peshat, Remez, Derash). **Garde-fou global (L'Exemple de Rabbi Akiva)** : Rappelez-vous l'histoire fondatrice du Talmud (*Haguiga 14b*) où quatre sages entrent dans le Pardes. Seul Rabbi Akiva est "entré en paix et ressorti en paix". Pour que votre exégèse soit réussie, l'interprétation métaphysique (Sod) ou allégorique (Derash) ne doit jamais détruire ou nier la Loi littérale (Peshat/Halakha). La synthèse doit maintenir un équilibre parfait, prouvant que l'agent a "rempli son ventre de pain et de viande" (la base littérale) avant de voler vers les cieux.

## Constraints
- Maintenez strictement les frontières entre les quatre niveaux (ne présentez pas un récit midrashique comme du Peshat).
- Fondez toujours l'analyse sur des sources juives traditionnelles reconnues (ex: Rachi pour le Peshat, Zohar pour le Sod).
- Utilisez la terminologie hébraïque originale (translittérée) en parallèle des traductions pour expliquer les nuances sémantiques.
- Conservez un ton respectueux, érudit et traditionnellement ancré dans les sources juives.

## Output Format

Générez la réponse finale en utilisant strictement la structure markdown suivante :

```markdown
# Exégèse PaRDeS : [Référence du texte, ex: Genèse 1:1]

**Texte Hébreu** : [Le texte en hébreu]
**Traduction** : [Traduction littérale]

### PESHAT (Sens Littéral)
[Sens littéral qui ne traite que du monde sensible. Résolution de l'aspérité, analyse grammaticale.]

### REMEZ (Allusion / Insinuation)
[Niveau plus élevé de l'étude. Rapprochements allusifs, typologie, concepts.]

### DERASH (Interprétation Figurée)
[Interprétation midrashique ou homilétique. Paraboles, légendes, proverbes éthiques.]

### SOD (Le Secret)
[Niveau ésotérique traitant de la métaphysique et de la révélation des réalités surnaturelles secrètes.]

### Synthèse Globale
[Brève conclusion sur la façon dont les 4 niveaux s'enrichissent mutuellement pour ce texte spécifique]
```
