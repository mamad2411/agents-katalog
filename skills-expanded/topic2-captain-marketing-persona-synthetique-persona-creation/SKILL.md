---
name: persona-creation
description: >
  Créer des personas synthétiques vivants et psychologiquement crédibles à partir de données réelles (transcriptions AI Notetaker, ICP, notes clients). Utiliser ce skill dès que l'utilisateur tape /Creation, demande de "créer un persona", "générer un profil client", "construire un persona synthétique", ou mentionne vouloir simuler un client cible. Ce skill est le point d'entrée obligatoire du plugin Persona Synthétique — il doit se déclencher avant toute commande /Validation, /Discussion ou /Panel. Déclencher aussi quand l'utilisateur dit "j'ai des calls à analyser" ou "je veux un persona basé sur mes clients".
---

# Skill : /Creation — Persona Synthétique

## Rôle de ce Skill

Transformer des données brutes (transcriptions, notes, ICP) en un persona synthétique vivant, psychologiquement crédible et exploitable en simulation conversationnelle.

Un persona réussi ici n'est pas une fiche marketing. C'est une entité capable de :
- Objecter, hésiter, douter
- Utiliser le vocabulaire spontané de vrais clients
- Simuler des biais cognitifs réalistes (aversion à la perte, inertie, etc.)
- Révéler ce qu'un client pense mais ne dit jamais à voix haute

---

## Étape 0 : Vérification des sources disponibles

Avant de commencer, demander à l'utilisateur quelles données il met à disposition :

```
Pour créer un persona solide, dis-moi ce que tu as :

1. Transcriptions AI Notetaker (calls, entretiens, réunions) → source prioritaire
2. ICP documenté (Ideal Customer Profile)
3. Notes d'entretiens clients existants
4. Données CRM ou feedback post-achat
5. Ton brief direct (si tu pars de zéro)

Tu peux combiner plusieurs sources. Colle ou uploade ce que tu as.
```

### ⚠️ Alerte volume insuffisant

Si l'utilisateur fournit des transcriptions AI Notetaker, **compter le nombre de conversations distinctes** avant de continuer.

**Règle critique** : En dessous de 15 transcriptions distinctes, déclencher cette alerte :

```
⚠️ Alerte qualité persona

Tu m'as fourni [N] transcription(s). Pour un persona statistiquement fiable, 
il en faut au minimum 15 — idéalement 20 à 25.

Avec moins, le risque est de sur-représenter un profil atypique 
ou de créer un persona biaisé par 1-2 personnalités marquantes.

Options :
→ Continuer avec [N] transcriptions (je signalerai les zones de fragilité dans le persona)
→ Ajouter d'autres sources (ICP, notes, brief) pour compenser
→ Attendre d'avoir plus de données

Que préfères-tu faire ?
```

Si l'utilisateur choisit de continuer avec moins de 15 sources, **marquer le persona généré avec** `[⚠️ Persona à consolider — données insuffisantes]` et lister les zones de fragilité en fin de fiche.

---

## Étape 1 : Analyse des sources

### 1a. Traitement des transcriptions AI Notetaker (source prioritaire)

Lire l'intégralité des transcriptions fournies et extraire systématiquement :

**Extraction verbatim**
- Repérer les citations directes les plus représentatives (viser 15 à 20)
- Identifier les formulations spontanées pour décrire le problème, les attentes, les peurs
- Relever le vocabulaire technique, les anglicismes, les tics de langage
- Noter le style de prise de parole : laconique / bavard, jargon / langage simple, direct / détours

**Patterns récurrents**
- Objections qui reviennent dans plusieurs conversations (noter la fréquence)
- Moments de bascule : quand le ton change (intérêt, méfiance, enthousiasme)
- Questions non posées explicitement mais sous-jacentes à plusieurs échanges
- Frustrations ou écarts mentionnés après un premier contact ou achat

**Signaux faibles**
- Ce qui est dit à demi-mot ou tourné en question rhétorique
- Les silences ou esquives sur certains sujets (inférés du contexte)
- Les comparaisons spontanées avec d'autres solutions

### 1b. Traitement du brief utilisateur (si pas de transcriptions)

Poser ces questions structurantes :

```
Pour construire le persona, j'ai besoin de comprendre :

1. Quel est le métier exact de ta cible ? (titre, taille d'entreprise, secteur)
2. Quel problème cherche-t-elle à résoudre quand elle te contacte ?
3. Qu'est-ce qui l'empêche de passer à l'action facilement ?
4. Quel est son rapport au budget pour ce type de solution ?
5. À quoi ressemble une bonne journée pour elle ? Et une mauvaise ?
6. Qu'est-ce qu'elle ne te dira jamais en face mais que tu devines ?
```

---

## Étape 2 : Construction du persona — Structure complète

Générer la fiche persona dans ce format exact.

---

### 🧑 IDENTITÉ

**Prénom** : [Prénom réaliste, pas générique]  
**Âge** : [Tranche précise, ex: 38-44 ans]  
**Titre / Fonction** : [Titre réel, pas idéalisé]  
**Secteur** : [Secteur d'activité]  
**Taille d'entreprise** : [Ex: PME 15-50 salariés, ETI, indépendant...]  
**Localisation type** : [Région / type de ville si pertinent]  
**Revenus estimés** : [Fourchette ou indice si pertinent]

---

### 🧠 PSYCHOGRAPHIE

**Valeurs profondes**  
[2-3 valeurs qui guident ses décisions — pas ses valeurs déclarées, ses valeurs réelles]

**Peurs inavouées**  
[Ce qui l'empêche de dormir mais qu'il/elle ne formulera jamais clairement]

**Ambitions non dites**  
[Ce qu'il/elle vise vraiment au-delà de l'objectif affiché]

**Biais cognitifs dominants**  
[Choisir parmi : aversion à la perte, biais de confirmation, effet de dotation, inertie du statu quo, preuve sociale, autorité, urgence artificielle... — justifier chaque biais par un signal issu des sources]

---

### 💼 JOB-TO-BE-DONE (JTBD)

> Formulation en première personne, style citation :
> *"Je ne suis pas juste [titre]. Je suis quelqu'un qui cherche à [objectif profond] 
> pour pouvoir [bénéfice de vie réel]."*

**Les 4 Forces de Progrès :**

| Force | Description |
|-------|-------------|
| 🔴 Push (ce qui ne va plus) | [Ce qui crée l'insatisfaction actuelle] |
| 🟢 Pull (ce qui attire) | [Ce qui rend ta solution désirable] |
| 😰 Anxiété (ce qui freine) | [Les peurs liées au changement] |
| 🧱 Inertie (les vieilles habitudes) | [Ce qui retient dans la situation actuelle] |

---

### 🗣️ LANGAGE AUTHENTIQUE

**Lexique spontané**  
[Liste des mots et expressions réels extraits des sources — pas de reformulation]

**Citations représentatives**  
Sélectionner 15 à 20 citations verbatim (ou proches du verbatim) classées par thème :

- *Problème* : [citation]
- *Attente* : [citation]
- *Objection* : [citation]
- *Déclencheur* : [citation]
- *Frustration* : [citation]
[...]

**Style de communication**  
[Direct/indirect — Jargon technique/langage courant — Laconique/bavard — Ton émotionnel/factuel]

---

### ❌ OBJECTIONS RÉCURRENTES

Pour chaque objection : fréquence observée, formulation exacte, nature (explicite = dite à voix haute / implicite = sous-entendue).

| Objection | Fréquence | Formulation exacte | Explicite/Implicite |
|-----------|-----------|-------------------|---------------------|
| Prix | [élevée/moyenne/rare] | [citation ou reformulation proche] | [E/I] |
| Temps | [...] | [...] | [...] |
| Confiance | [...] | [...] | [...] |
| [Autre] | [...] | [...] | [...] |

---

### ⚡ DÉCLENCHEURS DE DÉCISION

[Décrire les moments de bascule : qu'est-ce qui fait passer ce persona de "tiède" à "intéressé", de "intéressé" à "décidé" ?]

- **Déclencheur situationnel** : [Ex: fin de trimestre, recrutement raté, pression hiérarchique]
- **Déclencheur argumentaire** : [Formulation ou angle qui fait mouche]
- **Déclencheur relationnel** : [Recommandation d'un pair, preuve sociale spécifique]
- **Signal d'achat** : [Les phrases ou comportements qui indiquent qu'il est prêt]

---

### 🕳️ QUESTIONS NON POSÉES

[Les zones de flou que ce persona accepte sans chercher à les résoudre — incompréhensions persistantes, angles morts]

- [Question implicite 1]
- [Question implicite 2]
- [Question implicite 3]

---

### 😤 FRUSTRATIONS POST-ACHAT (si données disponibles)

[Si des conversations support ou feedback post-achat sont disponibles dans les sources]

- **Écart principal** : [Attente vs réalité d'usage]
- **Friction récurrente** : [Point de friction concret]
- **Formulation typique** : [Citation ou reformulation proche]

---

### 🎭 INSTRUCTIONS DE JEU DE RÔLE

*Ce bloc est réservé à Claude pour les modes /Discussion et /Panel — ne pas afficher à l'utilisateur dans la fiche finale.*

```
Tu incarnes [Prénom]. 

Personnalité : [2-3 traits dominants]
Ton : [Ex: direct et un peu impatient / chaleureux mais méfiant sur le budget]
Posture par défaut : [Ex: sceptique bienveillant / enthousiaste mais frileux à l'acte]

Biais à jouer : [Liste des biais cognitifs avec instruction comportementale]
Ex: "Tu as une forte aversion à la perte — tu reformules souvent les gains en pertes potentielles"

Objections à sortir en priorité : [Liste des 3 objections les plus fréquentes]

Ce que tu ne dis jamais spontanément mais qui ressort sous pression : [Peur inavouée + formulation approximative]

Vocabulaire imposé : [5-10 mots/expressions à utiliser naturellement dans tes réponses]

Tu ne sors jamais de ton personnage. Si une question te semble hors de ton expérience, 
tu réponds "Honnêtement, je me suis jamais vraiment posé la question" ou similaire — 
tu n'inventes pas de compétences que [Prénom] n'a pas.
```

---

## Étape 3 : Récapitulatif et passage à /Validation

Une fois la fiche générée, proposer :

```
Le persona [Prénom] est prêt.

Voici un résumé express :
→ [1 phrase sur son JTBD]
→ [1 phrase sur son objection principale]
→ [1 phrase sur son déclencheur de décision]

Prochaine étape : tape /Validation pour valider, challenger ou affiner ce persona.
Tu peux aussi demander directement "crée un autre persona" pour en générer un second.
```

---

## Notes pour l'itération

- Si l'utilisateur dit "il est trop lisse" ou "il ne sonnerait pas comme ça" → basculer en mode `/Optimisation` et demander un exemple de ce qui sonne faux
- Si des nouvelles transcriptions sont ajoutées après la création → signaler que `/Context` permet de mettre à jour le persona sans repartir de zéro
- Un persona créé depuis un brief seul (sans transcriptions) doit toujours être marqué `[Persona hypothétique — à valider sur le terrain]`
