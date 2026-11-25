---
name: theo-rethorique-synchronique
description: >-
  Analyse socio-rhétorique des textes bibliques (méthode de Vernon Robbins). Utilisez ce skill lorsque l'utilisateur demande une analyse "synchronique", une "analyse socio-rhétorique", l'étude des "textures" du texte (interne, socio-culturelle, idéologique), ou cherche à comprendre comment la forme littéraire d'un récit biblique subvertit les normes sociales, religieuses et de pouvoir (honneur/honte, pureté).
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
# Analyse Socio-Rhétorique (Socio-Rhetorical Criticism)

## Quand l'utiliser
- Lorsque l'utilisateur demande une analyse "synchronique".
- Lorsque l'utilisateur demande une analyse "socio-rhétorique" (Vernon Robbins).
- Lorsque l'utilisateur souhaite étudier les "textures" d'un texte (interne, socio-culturelle, idéologique).
- Lorsque l'utilisateur veut comprendre comment la forme littéraire d'un récit biblique subvertit les normes sociales, religieuses et de pouvoir (honneur/honte, pureté).

## Quand NE PAS l'utiliser
- Lorsque l'utilisateur demande une analyse diachronique (méthode historico-critique, histoire de la rédaction pure).
- Lorsque l'utilisateur demande spécifiquement la Rhétorique Sémitique (Roland Meynet) ou l'analyse littéraire de Robert Alter. Dans ces cas, utilisez leurs skills respectifs.

## Workflow / Processus d'Analyse

Exécutez ce processus séquentiel pour analyser le texte soumis par l'utilisateur. Appuyez-vous impérativement sur les documents de référence fournis.

### 1. Cadrage et Clôture du Texte
- Déclarez l'approche synchronique de l'analyse.
- Délimitez la péricope (le début et la fin de l'unité narrative) pour confirmer que vous analysez un tout cohérent.

### 2. Analyser la Texture Interne et la Stratégie Narrative
- Lisez le fichier `references/01-texture-interne.md` pour le cadre technique.
- Analysez la "mise en intrigue" (Plot) : comment le narrateur guide-t-il le lecteur à travers des choix structurels (enchâssements, chiasmes) ou l'ironie dramatique ?
- Identifiez les schémas d'architecture formelle : technique de l'enchâssement (le "sandwich" marcien), chiasmes, ou répétitions lexicales majeures.
- Accordez une attention particulière aux "Dyades Symétriques" (ex: paires lucaniennes) : comment la juxtaposition de personnages diamétralement opposés révèle-t-elle l'intentionnalité rédactionnelle de l'auteur ? Cherchez la "différence dans la répétition" (l'asymétrie socio-culturelle cachée derrière le parallèle).
- Traquez les **micro-échos** (chiffres partagés, mots-crochets ou fils de liaison, *hapax*, actions physiques symétriques, **détournement des termes de parenté**) qui servent de "colle textuelle" pour lier intimement les éléments d'une dyade ou d'un enchâssement.
- Expliquez comment cette structure formelle (notamment l'**antiparallélisme**) crée une tension dramatique, manipule les attentes du lecteur, ou lie irrémédiablement deux événements en apparence distincts.

### 3. Analyser l'Intertexture (Dialogues culturels et intra-livre)
- Lisez le fichier `references/04-intertexture.md` pour le cadre technique.
- Cherchez les citations ou allusions à l'Ancien Testament : comment servent-elles à légitimer l'action anticonformiste du Christ ?
- Identifiez les **scènes-types** (ex: la rencontre au puits) : comment le texte utilise-t-il un schéma narratif classique de l'Ancien Testament pour créer une attente chez le lecteur, puis le subvertir à des fins théologiques ?
- Cherchez les "Échos Intra-livre" : le geste du personnage (ex: l'outsider) préfigure-t-il ou imite-t-il une action majeure du Christ à l'échelle du livre entier ?

### 4. Analyser la Texture Socio-Culturelle (Dynamiques Sociales)
- Lisez le fichier `references/02-texture-socioculturelle.md` pour le cadre technique.
- Cartographiez les personnages selon les codes méditerranéens antiques de l'**honneur/honte** et de la **pureté/impureté**.
- Déterminez qui détient le pouvoir (statut social, autorité religieuse, sexe dominant) et qui est marginalisé (maladie, impureté, statut subalterne).
- Analysez la **Topographie morale (Dedans/Dehors)** : le personnage est-il "perdu dehors" ou "perdu dedans" (aliéné au cœur même de la communauté/maison) ?
- Repérez si les activités décrites (agricoles, domestiques) agissent comme des **marqueurs sociaux genrés** (ex: semer vs pétrir) renforçant une dyade symétrique.
- Évaluez le "choc culturel" (Culture shock) : à quel point les actions racontées étaient-elles scandaleuses pour un auditoire méditerranéen du premier siècle, et comment cela sert-il à légitimer une nouvelle communauté inclusive ?

### 5. Analyser la Texture Idéologique (La Subversion Théologique)
- Lisez le fichier `references/03-texture-ideologique.md` pour le cadre technique.
- Analysez le point de bascule : comment le récit, et spécifiquement l'action de Jésus (ou de Dieu), transgresse-t-il les normes établies à l'Étape 4 ? Recherchez les exemples d'anticonformisme, de débat théologique aboutissant à un "retournement christique", ou de "pureté contagieuse".
- Démontrez le renversement d'alliance ou de pouvoir : comment les "Bien-pensants" échouent-ils face aux "Anticonformistes" ?
- Identifiez l'enjeu dogmatique : le récit met-il en scène le passage vers **l'universalité du salut** (la surabondance de la miséricorde) ?
- Expliquez comment le texte déconstruit les rôles sociaux assignés et **subvertit les figures d'autorité ou les liens de parenté** (ex: attitude patriarcale "indigne" reflétant la grâce divine).
- Observez comment l'auteur opère une "restauration identitaire" (ex: "Fille d'Abraham") pour promouvoir une "communauté d'égaux" (Discipleship of equals) et une option préférentielle pour les marginaux (Horizon de Galates 3:28).

### 6. Créer la Synthèse Socio-Rhétorique Totale
- Rédigez une synthèse démontrant que la mécanique du récit (Texture Interne et Intertexture) est le dispositif parfait pour faire passer le bouleversement théologique (Texture Socio-culturelle et Idéologique). La forme est le fond.

## Contraintes

- **RÈGLE ANTI-DIACHRONIQUE :** Ne mentionnez JAMAIS l'histoire de la compilation des sources (Source Q, documents J, E, D, P) ni l'évolution des manuscrits. Cependant, vous DEVEZ reconnaître l'**"intentionnalité rédactionnelle" (Redaktionsgeschichte appliquée au texte final)** : traitez l'auteur/évangéliste final comme un théologien qui édite et structure délibérément son récit (ex: en créant des paires lucaniennes ou des intercalations) pour délivrer un message spécifique.
- **PAS DE SOCIOLOGIE SANS THÉOLOGIE :** L'analyse des rapports de pouvoir (honneur, pureté, genre) ne doit pas se limiter à un constat sociologique ou politique moderne. Elle doit mettre en lumière l'intention théologique (le message du Christ ou de l'évangéliste).
- **UTILISEZ LE LEXIQUE EXACT :** Vous DEVEZ impérativement employer les termes de la méthode : *Texture interne*, *Texture socio-culturelle*, *Topographie morale (Dedans/Dehors)*, *Texture idéologique*, *Structures de parité / Dyades symétriques / Macro-dyades*, *Différence dans la répétition*, *Antiparallélisme*, *Micro-échos / Mot-crochet*, *Écho intra-livre / Préfiguration*, *Scène-type*, *Intertextualité*, *Activités genrées*, *Enchâssement / Intercalation / Sandwich*, *Intentionnalité rédactionnelle*, *Choc des paradigmes*, *Débat théologique / Retournement christique*, *Universalité du salut*, *Pureté contagieuse*, *Anticonformisme vs Bien-pensants*, *Subversion de l'autorité et des liens de parenté*, *Détournement lexical*, *Restauration identitaire / Usurpation prophétique*, *Option préférentielle*, *Communauté d'égaux / Galates 3:28*.

## Format de Sortie Attendu

Votre réponse finale doit obligatoirement utiliser ces niveaux de titre (Markdown `###`) :

### 1. Clôture de l'Unité Narrative
*(Bref rappel des limites du texte analysé)*

### 2. Texture Interne et Stratégie Narrative
*(L'analyse formelle : intrigue, guidage du lecteur, enchâssements, chiasmes)*

### 3. Intertexture
*(L'analyse des scènes-types, citations de l'AT et échos intra-livre)*

### 4. Texture Socio-Culturelle : Codes et Pouvoirs
*(L'analyse du système antique : honneur/honte, pur/impur, dominants/marginaux)*

### 5. Texture Idéologique : La Subversion Théologique
*(Le renversement des codes par l'action divine ou christique)*

### 6. Synthèse Rhétorique Synchronique
*(Comment l'architecture littéraire et réthorique, et les différentes textures du texte tour à tour analysées, servent de véhicule au message théologique)*
