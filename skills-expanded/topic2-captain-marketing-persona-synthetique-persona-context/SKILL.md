---
name: persona-context
description: >
  Alimenter le plugin avec de nouvelles données pour mettre à jour les personas existants ou enrichir la base de connaissance avant une création. Utiliser ce skill dès que l'utilisateur tape /Context, dit "j'ai de nouveaux calls", "voici de nouvelles transcriptions", "j'ai un rapport d'étude à intégrer", "mon marché a évolué", "j'ai de nouveaux feedbacks clients", ou veut uploader des données fraîches sans repartir d'une création complète. Déclencher aussi quand l'utilisateur mentionne vouloir "mettre à jour" ou "nourrir" ses personas avec de nouvelles informations.
---

# Skill : /Context — Alimentation et mise à jour des données

## Rôle de ce Skill

Intégrer de nouvelles données dans le plugin sans repartir de zéro — ni en création, ni en optimisation manuelle. `/Context` est la commande de mise à jour continue : elle capte ce que le terrain apprend, l'analyse et propose des évolutions ciblées sur les personas concernés.

---

## Étape 1 : Réception et identification des nouvelles données

Demander à l'utilisateur ce qu'il apporte :

```
Quelles nouvelles données tu m'apportes ?

→ Transcriptions AI Notetaker (calls, entretiens, réunions)
→ Rapport d'étude de marché ou benchmark sectoriel
→ Feedbacks post-achat ou tickets support
→ Notes d'entretiens clients informels
→ Évolution de l'ICP ou du positionnement
→ Autre chose ?

Colle ou uploade tes données — je prends tout.
```

---

## Étape 2 : Vérification du volume

Comme en `/Creation`, vérifier le volume si des transcriptions sont fournies.

**Si les nouvelles transcriptions sont en dessous de 5** :

```
⚠️ Tu m'apportes [N] nouvelle(s) transcription(s).

C'est suffisant pour enrichir ponctuellement un persona existant, 
mais pas pour modifier en profondeur sa structure.

Je vais identifier ce qui change par rapport aux données actuelles 
et te proposer des ajustements ciblés — pas une refonte.

On continue ?
```

**Si les nouvelles transcriptions sont nombreuses (10+)** :

```
Tu m'apportes [N] nouvelles transcriptions.

C'est suffisant pour :
→ Mettre à jour les personas existants en profondeur
→ Détecter si un nouveau profil émerge qui justifierait un nouveau persona
→ Identifier des évolutions du marché (nouvelles objections, nouveaux déclencheurs)

Je lance l'analyse.
```

---

## Étape 3 : Analyse des nouvelles données

Appliquer la même grille d'extraction que dans `/Creation` — mais en mode différentiel : chercher ce qui est nouveau, ce qui confirme, ce qui contredit.

### Extraction différentielle

Pour chaque source analysée, identifier :

**Ce qui confirme les personas existants**
- Objections déjà présentes qui réapparaissent → noter la fréquence accrue
- Déclencheurs déjà identifiés qui se confirment
- Vocabulaire spontané déjà capturé

**Ce qui enrichit les personas existants**
- Nouvelles formulations, nouveaux tics de langage
- Nouvelles objections non encore répertoriées
- Nouveaux déclencheurs ou signaux d'achat
- Nouvelles tensions psychologiques

**Ce qui contredit les personas existants**
- Comportements ou formulations en rupture avec le profil actuel
- Évolutions du rapport au budget, au temps, au risque
- Changement de priorités (ex: post-crise, post-recrutement raté...)

**Ce qui suggère un nouveau persona**
- Profil récurrent qui ne ressemble à aucun persona existant
- Segment émergent avec des caractéristiques distinctes

---

## Étape 4 : Rapport d'analyse

Présenter les résultats avant toute modification :

```
📊 RAPPORT D'ANALYSE — NOUVELLES DONNÉES

Sources analysées : [N transcriptions / type de sources]
Période couverte : [si identifiable]

─────────────────────────────────
IMPACT SUR [Prénom 1]
─────────────────────────────────

✅ Confirmé (pas de modification nécessaire) :
→ [Élément confirmé 1]
→ [Élément confirmé 2]

➕ À enrichir :
→ [Bloc concerné] : [Description de l'enrichissement]
→ [Bloc concerné] : [...]

⚠️ À corriger :
→ [Bloc concerné] : [Ce qui a changé et pourquoi]

─────────────────────────────────
IMPACT SUR [Prénom 2]
─────────────────────────────────
[Même structure]

─────────────────────────────────
SIGNAL NOUVEAU PERSONA
─────────────────────────────────
[Si détecté] : J'ai repéré un profil récurrent qui ne correspond 
à aucun de tes personas actuels :
→ [Description succincte du profil émergent]
→ Fréquence : [N occurrences sur les nouvelles sources]

Veux-tu lancer une /Creation pour ce nouveau profil ?
[Si non détecté] : Aucun profil émergent identifié.
```

---

## Étape 5 : Application des modifications

Après validation du rapport par l'utilisateur, appliquer les modifications via le workflow `/Optimisation` — les deux skills sont liés.

```
Tu valides ce rapport ?

→ Oui, applique toutes les modifications
→ Applique uniquement sur [Prénom X]
→ Je veux revoir certains points d'abord
```

Si l'utilisateur valide → basculer sur `/Optimisation` pour chaque persona concerné, en mode silencieux (sans re-diagnostiquer ce que `/Context` vient déjà d'analyser).

---

## Étape 6 : Mise à jour du compteur de sources

Après chaque passage en `/Context`, mettre à jour le bloc historique de chaque persona modifié :

```
📌 HISTORIQUE DES VERSIONS [Prénom]

v1.0 — Création | 18 transcriptions
v1.1 — /Context | +7 transcriptions | Ajout : [description courte]
v1.2 — /Context | +1 rapport sectoriel | Correction : [description courte]
```

Et mettre à jour le compteur global de sources du plugin :

```
BASE DE CONNAISSANCE DU PLUGIN
Total transcriptions intégrées : [N]
Dernière mise à jour : [date]
Personas actifs : [N] | Dernière modification : [Prénom] — [date]
```

---

## Étape 7 : Cadence recommandée

Si l'utilisateur demande comment utiliser `/Context` de façon optimale :

```
Quelques repères pour alimenter tes personas régulièrement :

→ Après chaque série de 5 nouveaux calls → lancer /Context pour capter les évolutions fraîches
→ Après un changement d'offre ou de positionnement → /Context avant la prochaine simulation
→ Après un pic de churns ou d'objections inhabituelles → /Context pour détecter un signal faible
→ Tous les trimestres → bilan global pour vérifier si les personas tiennent toujours la route

Un persona qui n'est jamais mis à jour finit par simuler le marché d'il y a 6 mois.
```

---

## Note sur la relation /Context — /Optimisation

Ces deux skills sont complémentaires mais distincts :

- `/Context` analyse les données et détecte ce qui doit changer — c'est le diagnostic
- `/Optimisation` applique les changements et affine la simulation — c'est la chirurgie

Dans le workflow idéal : `/Context` → rapport → validation → `/Optimisation` automatique sur les blocs concernés.
