---
name: persona-panel
description: >
  Réunir plusieurs personas synthétiques validés et les interroger simultanément. Utiliser ce skill dès que l'utilisateur tape /Panel, dit "réunis mes personas", "je veux que plusieurs personas répondent à la même question", "fais débattre mes personas", "salle de réunion virtuelle", ou veut comparer les réactions de profils différents sur un même sujet. Déclencher aussi quand l'utilisateur dit "comment réagiraient mes différents profils à..." ou "qu'est-ce que le sceptique et l'enthousiaste penseraient de...".
---

# Skill : /Panel — Simulation multi-personas

## Rôle de ce Skill

Faire fonctionner plusieurs personas en simultané — soit en mode débat (ils interagissent entre eux), soit en mode séquentiel (chacun répond indépendamment à la même question).

L'intérêt du panel est de révéler les divergences : deux profils différents face au même pitch ne bloquent pas aux mêmes endroits, n'utilisent pas le même vocabulaire, ne sont pas sensibles aux mêmes déclencheurs. Ces écarts sont des informations stratégiques.

---

## Étape 1 : Constitution du panel

### Sélection des personas

Afficher les personas disponibles et laisser l'utilisateur choisir sa composition :

```
Tu as [N] personas disponibles :

→ [Prénom 1] — [Titre / Profil en 1 ligne] | Posture : [ex: sceptique bienveillant]
→ [Prénom 2] — [Titre / Profil en 1 ligne] | Posture : [ex: enthousiaste mais frileux sur le budget]
→ [Prénom 3] — [Titre / Profil en 1 ligne] | Posture : [ex: pragmatique, cherche la preuve]

Quels personas veux-tu réunir ? (minimum 2, pas de maximum)
```

Si l'utilisateur n'a qu'un seul persona validé, l'avertir :

```
⚠️ Tu n'as qu'un seul persona validé pour l'instant.
Le mode /Panel nécessite au minimum 2 personas.

Options :
→ Créer un deuxième persona (/Creation)
→ Utiliser /Discussion pour travailler avec [Prénom] seul
```

### Recommandation de composition

Si l'utilisateur a plus de 3 personas et hésite, suggérer une composition équilibrée :

```
Pour un panel utile, je recommande de mixer les postures :
→ 1 persona sceptique (teste la résistance de tes arguments)
→ 1 persona enthousiaste (révèle ce qui attire vraiment)
→ 1 persona économe ou prudent (fait remonter les freins pratiques)

Veux-tu que je compose le panel selon ce principe, ou tu choisis toi-même ?
```

---

## Étape 2 : Choix du mode de fonctionnement

Une fois le panel constitué, poser la question du mode :

```
Ton panel est composé de :
→ [Prénom 1] — [Posture]
→ [Prénom 2] — [Posture]
→ [Prénom 3] — [Posture]

Comment veux-tu que ça fonctionne ?

🗣️ MODE DÉBAT
Les personas interagissent entre eux. Ils réagissent à tes questions 
mais aussi aux réponses des autres — ils peuvent se contredire, 
s'interpeller ou se rejoindre.
Idéal pour : explorer des tensions, tester la robustesse d'une idée, 
voir où les profils divergent vraiment.

📋 MODE SÉQUENTIEL
Chaque persona répond indépendamment à tes questions, dans l'ordre.
Pas d'interaction entre eux.
Idéal pour : comparer les réactions côte à côte, analyser les écarts,
préparer des messages différenciés par profil.
```

---

## Étape 3a : Mode Débat

### Règles d'animation

- Claude gère les prises de parole — chaque réponse est clairement attribuée avec `**[Prénom] :**`
- Les personas peuvent réagir aux propos des autres, pas seulement à la question
- Chaque persona conserve sa posture, son lexique et ses biais — ils ne convergent pas artificiellement
- Claude modère si nécessaire pour éviter que le débat ne tourne en monologues parallèles

### Structure d'un tour de débat

Pour chaque question ou pitch soumis par l'utilisateur :

1. Le persona le plus susceptible de réagir en premier prend la parole (selon sa posture)
2. Les autres réagissent — soit à la question, soit à ce que vient de dire le premier
3. Un troisième tour court est possible si une tension intéressante émerge
4. Claude ne clôt pas le débat prématurément — laisser les désaccords vivre

**Format d'affichage :**

```
**[Prénom 1] :** [Réaction — ton spontané, vocabulaire du persona, biais actifs]

**[Prénom 2] :** [Réaction ou réponse à [Prénom 1] — peut être en accord partiel, 
en désaccord, ou apporter un angle différent]

**[Prénom 3] :** [Réaction — peut clore, relancer ou laisser la tension ouverte]
```

### Gestion des convergences et divergences

- Si deux personas convergent sur un point → le signaler brièvement en sortant du débat : *"[Prénom 1] et [Prénom 2] s'accordent sur [X] — c'est un signal fort."*
- Si une tension forte émerge entre deux personas → laisser le débat se développer, ne pas arbitrer
- Si un persona reste silencieux sur un sujet (parce que ça ne le concerne pas) → le faire passer, ne pas forcer une réponse artificielle

---

## Étape 3b : Mode Séquentiel

### Structure de réponse

Pour chaque question soumise par l'utilisateur, chaque persona répond dans l'ordre défini.

**Format d'affichage :**

```
━━━━━━━━━━━━━━━━━━━━━━━━━
**[Prénom 1]** | [Titre / Posture]
━━━━━━━━━━━━━━━━━━━━━━━━━
[Réponse — ton spontané, vocabulaire du persona, biais actifs]

━━━━━━━━━━━━━━━━━━━━━━━━━
**[Prénom 2]** | [Titre / Posture]
━━━━━━━━━━━━━━━━━━━━━━━━━
[Réponse]

━━━━━━━━━━━━━━━━━━━━━━━━━
**[Prénom 3]** | [Titre / Posture]
━━━━━━━━━━━━━━━━━━━━━━━━━
[Réponse]
```

### Tableau de synthèse automatique

Après chaque série de réponses séquentielles, générer un tableau de synthèse :

```
📊 SYNTHÈSE DU PANEL

| | [Prénom 1] | [Prénom 2] | [Prénom 3] |
|---|---|---|---|
| Réaction initiale | [Positif/Neutre/Négatif] | [...] | [...] |
| Objection principale | [en 5 mots] | [...] | [...] |
| Déclencheur activé | [Oui/Non/Partiel] | [...] | [...] |
| Signal d'achat | [Présent/Absent] | [...] | [...] |

Points de convergence : [Ce sur quoi tous s'accordent]
Points de divergence : [Ce qui les sépare vraiment]
```

---

## Étape 4 : Changement de mode en cours de session

L'utilisateur peut switcher de mode à tout moment :

```
/Débat → passer en mode débat
/Séquentiel → passer en mode séquentiel
```

---

## Étape 5 : Sortie du panel et debriefing

L'utilisateur tape `/Stop` ou demande un bilan.

```
--- FIN DE SESSION PANEL ---

🎭 Personas actifs : [Prénom 1], [Prénom 2], [Prénom 3]
Mode utilisé : [Débat / Séquentiel / Les deux]
Durée : [N] échanges

BILAN PANEL

Ce qui fait consensus (tous les personas) :
→ [Point de convergence 1]
→ [Point de convergence 2]

Ce qui divise (selon les profils) :
→ [Divergence 1] : [Prénom X] vs [Prénom Y]
→ [Divergence 2] : [...]

L'objection la plus robuste (résiste à tous les profils) :
→ [Objection] — formulée par [Prénom(s)]

Le déclencheur le plus universel :
→ [Ce qui a eu un effet positif sur le plus grand nombre]

Recommandations :
→ [Message / argument à adapter selon le profil]
→ [Angle à creuser sur un profil spécifique]
→ [Objection prioritaire à traiter avant d'aller plus loin]
```

---

## Étape 6 : Export du panel

Proposer systématiquement l'export après le debriefing :

```
Veux-tu exporter le compte-rendu de cette session en .md ?
Il contiendra : composition du panel, échanges complets, tableau de synthèse et bilan.
```

Si oui → générer un fichier `.md` structuré avec :
- En-tête : date, personas, mode utilisé, sujet testé
- Transcription complète de la session
- Tableau de synthèse
- Bilan et recommandations

---

## Étape 7 : Options post-panel

```
Que veux-tu faire maintenant ?

→ Relancer une nouvelle session panel sur un angle différent
→ /Discussion — approfondir avec un persona spécifique
→ /Optimisation — affiner un persona sur la base de ce qu'on vient de voir
→ /Creation — créer un nouveau persona pour compléter le panel
```

---

## Note sur la cohérence des personas en panel

En mode panel, le risque principal est que les personas se ressemblent trop — surtout si leurs profils sont proches. Claude doit amplifier les différences réelles entre eux plutôt que de les lisser. Si deux personas ont des postures similaires, les différencier par le ton, le lexique et les priorités d'objection, pas seulement par le contenu.

Un panel utile crée des frictions. Des personas qui s'accordent sur tout ne testent rien.
