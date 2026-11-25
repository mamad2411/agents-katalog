---
name: persona-optimisation
description: >
  Affiner, corriger ou enrichir un persona synthétique existant sans repartir de zéro. Utiliser ce skill dès que l'utilisateur tape /Optimisation, dit "ce persona sonne faux", "affine [prénom]", "il est trop lisse", "ajoute ce biais", "corrige cette objection", "le persona ne correspond plus à ma réalité", ou signale un écart entre le persona et ce qu'il observe sur le terrain. Déclencher aussi automatiquement quand, pendant une session /Discussion ou /Panel, l'utilisateur corrige le persona en disant "non, il ne dirait jamais ça" ou "en vrai ce client réagirait plutôt comme ça".
---

# Skill : /Optimisation — Affinage et mise à jour d'un persona

## Rôle de ce Skill

Corriger ce qui sonne faux, enrichir ce qui manque de relief, mettre à jour ce qui est devenu obsolète — sans régénérer toute la fiche.

L'optimisation est chirurgicale : on touche uniquement ce qui pose problème. Un persona n'est jamais figé, il évolue avec le terrain.

---

## Étape 1 : Identification du déclencheur

Trois situations possibles déclenchent ce skill :

### Déclencheur A — Signal en cours de simulation

L'utilisateur corrige le persona pendant une session `/Discussion` ou `/Panel` :
- *"Non, il ne dirait jamais ça"*
- *"En vrai ce type de client réagirait plutôt comme ça"*
- *"Cette objection n'est pas la bonne"*

Claude sort brièvement du personnage, note la correction et propose :

```
Je note cette correction sur [Prénom].

Veux-tu :
→ Appliquer maintenant et reprendre la simulation immédiatement
→ Accumuler les corrections et les appliquer en fin de session (/Stop)
```

### Déclencheur B — Demande explicite post-session

L'utilisateur tape `/Optimisation` après une session ou depuis un bilan.

Afficher les personas disponibles si plusieurs existent :

```
Quel persona veux-tu optimiser ?

→ [Prénom 1] — [Titre / dernière mise à jour]
→ [Prénom 2] — [Titre / dernière mise à jour]
```

### Déclencheur C — Détection proactive par Claude

Si pendant une simulation Claude détecte lui-même que le persona produit des réponses incohérentes ou trop génériques, signaler en sortant brièvement du personnage :

```
[Hors personnage] Je remarque que mes réponses en tant que [Prénom] 
manquent de précision sur [sujet]. 

Veux-tu qu'on affine ce point avant de continuer ?
```

---

## Étape 2 : Diagnostic — Identifier ce qui doit changer

Avant toute modification, poser un diagnostic structuré.

### 2a. Si l'utilisateur a un problème précis

Demander de le formuler :

```
Qu'est-ce qui te semble faux ou insuffisant sur [Prénom] ?

Quelques exemples pour t'aider à cibler :
→ "Ses objections ne ressemblent pas à ce que j'entends vraiment"
→ "Son vocabulaire est trop soigné / trop générique"
→ "Il manque de résistance — il cède trop facilement"
→ "Son profil a changé, j'ai de nouvelles données"
→ "Il lui manque un biais important"
→ Autre chose ?
```

### 2b. Si l'utilisateur n'a pas de problème précis mais veut améliorer

Proposer un audit rapide des 5 axes d'optimisation :

```
Je passe [Prénom] en revue sur 5 axes. Dis-moi ce qui te semble prioritaire :

1. 🗣️ Authenticité du langage — les formulations sonnent-elles assez spontanées ?
2. 🧠 Profondeur psychologique — les biais et peurs sont-ils assez marqués ?
3. ❌ Résistance aux objections — le persona cède-t-il trop facilement ?
4. ⚡ Précision des déclencheurs — sait-on vraiment ce qui le fait basculer ?
5. 📊 Mise à jour terrain — y a-t-il de nouvelles données à intégrer ?

Sur quoi veux-tu qu'on travaille en priorité ?
```

---

## Étape 3 : Types d'optimisation et méthodes

### Type 1 — Correction de langage

**Signal** : les formulations sonnent trop "IA", trop propres, trop reformulées.

**Méthode** :
1. Identifier les citations ou expressions concernées
2. Demander à l'utilisateur un exemple de ce qu'il entend vraiment sur le terrain (ou extraire depuis de nouvelles sources)
3. Remplacer les formulations lisses par des tournures plus brutes, plus idiomatiques

**Avant / Après :**
```
Avant : "Je ne suis pas sûr que le retour sur investissement soit suffisant."
Après : "Ouais mais concrètement, ça me rapporte quoi ? Je vois pas le ROI."
```

### Type 2 — Renforcement des biais cognitifs

**Signal** : le persona répond de façon trop rationnelle, trop équilibrée, sans friction émotionnelle.

**Méthode** :
1. Identifier le ou les biais manquants ou sous-exploités
2. Formuler une instruction comportementale précise pour chaque biais

**Biais disponibles et leur instruction type :**

| Biais | Instruction comportementale |
|-------|----------------------------|
| Aversion à la perte | Reformule systématiquement les gains en pertes potentielles : "Ouais mais si ça marche pas..." |
| Inertie du statu quo | Reviens régulièrement à ce qui "tourne déjà bien" pour justifier l'inaction |
| Biais de confirmation | Cite spontanément des exemples qui confirment tes doutes existants |
| Preuve sociale | Demande systématiquement des références dans ton secteur avant de t'intéresser |
| Effet de dotation | Surestime la valeur de ta solution actuelle, même imparfaite |
| Surconfiance | Pense avoir déjà la réponse avant d'avoir entendu l'argument complet |
| Biais de disponibilité | Cite un exemple récent d'échec similaire pour nourrir ta méfiance |

### Type 3 — Ajout de tensions psychologiques

**Signal** : le persona est trop cohérent, trop prévisible, manque de contradictions internes.

**Méthode** : ajouter une tension entre deux dimensions du persona.

Exemples de tensions crédibles :
- Veut changer mais a peur de se tromper → *"J'aimerais bien essayer mais si ça foire, c'est moi qui prends."*
- Conscient du problème mais ne veut pas admettre qu'il ne l'a pas résolu seul → résistance passive
- Séduit par l'offre mais convaincu que "c'est pas le bon moment" → procrastination rationalisée
- Enthousiasmé en appel mais qui se refroidit entre deux échanges → effet d'inertie post-call

### Type 4 — Mise à jour avec nouvelles données

**Signal** : l'utilisateur a de nouvelles transcriptions, un nouveau feedback client, une évolution du marché.

**Méthode** :
1. Demander les nouvelles sources à uploader ou coller
2. Identifier les éléments nouveaux qui contredisent ou enrichissent le persona existant
3. Appliquer uniquement les modifications justifiées par les nouvelles données — ne pas tout réécrire

```
Tu m'as fourni [N] nouvelles transcriptions / [type de source].

Voici ce que je détecte de nouveau par rapport au persona actuel :
→ [Élément nouveau 1] — modifie [bloc concerné]
→ [Élément nouveau 2] — enrichit [bloc concerné]
→ [Élément nouveau 3] — contredit [point existant] — je te propose de le corriger

Veux-tu que j'applique ces modifications ?
```

### Type 5 — Recalibrage de la posture de résistance

**Signal** : le persona cède trop facilement aux arguments, la simulation manque de friction utile.

**Méthode** :
1. Renforcer la posture par défaut (sceptique → très sceptique, prudent → bloquant)
2. Augmenter le nombre d'échanges nécessaires avant qu'une objection soit levée
3. Ajouter une objection de rebond : quand une objection est levée, une nouvelle, plus profonde, émerge

```
Instruction ajoutée : quand une objection de [Prénom] est levée par un argument, 
ne pas valider immédiatement. Marquer une hésitation puis faire remonter 
une objection de niveau suivant (plus profonde, plus émotionnelle).
```

---

## Étape 4 : Application des modifications

Toujours montrer ce qui change avec un format Avant/Après par bloc modifié :

```
MODIFICATIONS APPLIQUÉES SUR [Prénom]

📝 Bloc : Langage authentique
Avant : [...]
Après : [...]

🧠 Bloc : Biais cognitifs
Ajout : [Biais + instruction comportementale]

❌ Bloc : Objections
Modification : [Objection reformulée]

Instructions de jeu de rôle mises à jour ✓
```

Ne jamais régénérer toute la fiche sauf si l'utilisateur le demande explicitement ou si plus de 50% des blocs sont modifiés.

---

## Étape 5 : Validation des modifications

Après chaque série de modifications, demander confirmation :

```
Voilà les changements sur [Prénom].

C'est bon pour toi ou tu veux encore ajuster quelque chose ?

Une fois validé, [Prénom] est prêt pour :
→ /Discussion — retester avec les nouvelles paramètres
→ /Panel — réintégrer le panel mis à jour
```

---

## Étape 6 : Versioning léger

Garder une trace des évolutions majeures du persona dans un bloc dédié en fin de fiche :

```
📌 HISTORIQUE DES VERSIONS

v1.0 — Création initiale | Source : [N transcriptions / brief]
v1.1 — [Date] : [Description courte de la modification]
v1.2 — [Date] : [Description courte]
```

Cela permet à l'utilisateur de savoir pourquoi le persona a évolué et de revenir en arrière si une modification s'avère moins bonne.

---

## Note sur la philosophie d'optimisation

Un persona ne doit jamais être "terminé". Il s'affine avec chaque simulation, chaque nouvelle donnée terrain, chaque correction de l'utilisateur. L'objectif n'est pas la perfection de la fiche — c'est la précision de la simulation.

La meilleure optimisation est celle déclenchée par une friction réelle : quand l'utilisateur dit "non, il ne dirait jamais ça", c'est exactement là que le persona progresse.
