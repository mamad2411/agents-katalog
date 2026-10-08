---
name: persona-validation
description: >
  Valider, challenger et affiner un persona synthétique créé avec /Creation. Utiliser ce skill dès que l'utilisateur tape /Validation, dit "valide ce persona", "challenge le persona", "est-ce que ce persona est réaliste ?", ou veut vérifier la solidité d'un profil avant de l'utiliser en simulation. Ce skill est l'étape obligatoire entre /Creation et /Discussion — il garantit que le persona est crédible, non lissé et exploitable.
---

# Skill : /Validation — Vérification et consolidation du persona

## Rôle de ce Skill

Soumettre le persona créé à un protocole de validation structuré en deux temps :

1. **Auto-critique interne** : Claude évalue lui-même la solidité du persona selon 5 critères
2. **Challenge utilisateur** : L'utilisateur répond à 5 questions courtes pour confirmer, corriger ou enrichir

L'objectif n'est pas de valider pour valider — c'est de détecter ce qui sonne faux, ce qui est trop lisse, ce qui manque de relief avant d'entrer en simulation.

---

## Étape 1 : Présentation synthétique du persona

Avant tout challenge, présenter un résumé du persona sous cette forme :

```
📋 PERSONA EN COURS DE VALIDATION : [Prénom]

Profil : [Titre / Secteur / Taille d'entreprise]
JTBD : [Reformulation en 1 phrase]

Ses 3 objections principales :
→ [Objection 1 — formulation exacte]
→ [Objection 2]
→ [Objection 3]

Son déclencheur de décision : [1 phrase]
Sa peur inavouée : [1 phrase]
Son vocabulaire spontané : [5-6 mots/expressions clés]

Source : [Nb de transcriptions / brief / ICP — rappeler si ⚠️ données insuffisantes]
```

---

## Étape 2 : Auto-critique structurée (Claude évalue le persona)

Claude évalue le persona selon ces 5 critères et donne un score + commentaire pour chacun.

**Scoring** : ✅ Solide / ⚠️ Fragile / ❌ Insuffisant

---

### Critère 1 — Authenticité du langage

> Le vocabulaire et les citations sonnent-ils comme de vraies personnes ou comme du résumé IA ?

Vérifier :
- Les citations sont-elles en langage naturel ou reformulées de façon trop propre ?
- Le lexique spontané contient-il des termes vraiment spécifiques à ce profil ?
- Y a-t-il des tics de langage ou des tournures idiomatiques ?

**Si fragile** : signaler les citations qui semblent trop "lisses" et proposer de les reformuler de façon plus brute.

---

### Critère 2 — Profondeur psychologique

> Le persona a-t-il une vie intérieure ou est-ce une liste de caractéristiques plates ?

Vérifier :
- Les peurs inavouées sont-elles spécifiques ou génériques ("peur de l'échec") ?
- Les biais cognitifs sont-ils justifiés par des signaux concrets issus des sources ?
- Y a-t-il une tension interne crédible (ex: veut changer mais a peur de se tromper) ?

**Si fragile** : proposer 1-2 tensions psychologiques à ajouter.

---

### Critère 3 — Couverture des 5 dimensions

> Les 5 dimensions d'interrogation sont-elles toutes renseignées ?

| Dimension | Statut | Commentaire |
|-----------|--------|-------------|
| Objections récurrentes | ✅/⚠️/❌ | [...] |
| Langage authentique | ✅/⚠️/❌ | [...] |
| Déclencheurs de décision | ✅/⚠️/❌ | [...] |
| Questions non posées | ✅/⚠️/❌ | [...] |
| Frustrations post-achat | ✅/⚠️/❌ / N/A si pas de données | [...] |

---

### Critère 4 — Résistance à la confrontation

> Ce persona va-t-il objecter de façon crédible ou être trop accommodant ?

Vérifier :
- Les objections sont-elles formulées avec la bonne dose d'inconfort ?
- Y a-t-il une objection implicite (non dite) en plus des objections explicites ?
- Le persona a-t-il une posture par défaut claire (sceptique, curieux, méfiant, enthousiaste frileux...) ?

**Si fragile** : proposer une reformulation plus incisive de la posture de base.

---

### Critère 5 — Cohérence interne

> Les différents blocs du persona sont-ils cohérents entre eux ?

Vérifier :
- Le JTBD est-il aligné avec les déclencheurs de décision ?
- Les biais cognitifs renforcent-ils les objections (et pas le contraire) ?
- Le style de communication est-il cohérent avec le profil psychographique ?

**Si fragile** : signaler la contradiction et proposer une correction.

---

### Synthèse de l'auto-critique

```
BILAN VALIDATION INTERNE

✅ Points solides : [liste]
⚠️ Points à consolider : [liste]
❌ Points manquants : [liste]

Recommandation : [Prêt pour /Discussion / À affiner avant usage / Données insuffisantes]
```

---

## Étape 3 : Challenge utilisateur — 5 questions courtes

Après l'auto-critique, soumettre ces 5 questions à l'utilisateur. Les poser en une seule fois, pas une par une.

```
Maintenant, 5 questions rapides pour que tu valides de ton côté :

1. 🎯 Reconnaissance
   Est-ce que tu reconnais quelqu'un de réel dans ce profil ? 
   (Oui / Partiellement / Non — et si non, qu'est-ce qui cloche ?)

2. 🗣️ Langage
   Les formulations te semblent-elles proches de ce que tu entends vraiment 
   dans tes calls ? Y a-t-il des expressions qui sonnent faux ?

3. ❌ Objection manquante
   Y a-t-il une objection fréquente dans ta réalité qui n'apparaît pas dans ce persona ?

4. ⚡ Déclencheur
   Le déclencheur de décision décrit te semble-t-il juste ? 
   Qu'est-ce qui fait vraiment basculer ce type de client chez toi ?

5. 🔥 Ce qui manque
   Qu'est-ce que ce persona ne capture pas encore et qui serait important 
   pour simuler une vraie conversation avec lui ?
```

---

## Étape 4 : Intégration des retours et décision

Selon les réponses de l'utilisateur :

**Si tout est validé** :
```
✅ Persona [Prénom] validé.

Il est prêt pour :
→ /Discussion — dialoguer avec lui seul
→ /Panel — le réunir avec d'autres personas
→ /Creation — créer un deuxième persona pour compléter le panel

Que veux-tu faire ?
```

**Si des corrections sont nécessaires** :
- Intégrer immédiatement les ajustements dans la fiche persona
- Resoumettre uniquement les blocs modifiés pour confirmation
- Ne pas régénérer toute la fiche sauf si la correction est structurelle

```
J'ai mis à jour [liste des blocs modifiés].

Voici les changements :
→ [Bloc] : [Avant] → [Après]

C'est bon pour toi ou tu veux encore ajuster ?
```

**Si le persona est trop fragile pour être utilisé** :
```
⚠️ Ce persona a besoin d'être renforcé avant d'être utilisé en simulation.

Les points critiques : [liste]

Options :
→ Ajouter des sources (/Context)
→ Refaire le persona avec un brief plus précis (/Creation)
→ Utiliser quand même en mode "persona hypothétique" avec prudence
```

---

## Note sur la posture de Claude pendant la validation

Claude adopte ici une **posture de confrontation bienveillante** — pas de complaisance. Si le persona est trop lisse, trop générique ou trop accommodant, le dire clairement. Un persona flatteur est inutile en simulation : il ne préparera pas l'utilisateur aux vraies objections.
