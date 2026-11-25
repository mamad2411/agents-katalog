---
name: prospect-scorer
description: "Orchestre sirene + cnil + france-travail + bodacc + aides pour produire un score composite de prospect qualifié. Utiliser quand l'utilisateur demande d'analyser ou scorer un prospect, un SIRET, ou une entreprise cible."
metadata: { "openclaw": { "emoji": "🎯" } }
user-invocable: true
---

# Prospect Scorer

## Objectif

Produire un **scorecard JSON** avec score composite et recommandation d'approche commerciale pour un prospect identifié par SIRET ou nom d'entreprise.

## Déclencheurs

- `/score SIRET` (ex: `/score 44306184100047`)
- `/score Nom Entreprise` (ex: `/score Airbus`)
- "analyse ce prospect"
- "score cette entreprise"
- "est-ce un bon lead ?"

## Grille de scoring

| Signal | Points | Source |
|--------|--------|--------|
| Pas de DPO déclaré (CNIL) | +30 | data-pipe `cnil` |
| Recrute DevSecOps/RGPD/DPO | +25 | data-pipe `france-travail` |
| 50-250 salariés (cible NIS2) | +20 | data-pipe `sirene` |
| Région Occitanie | +15 | data-pipe `sirene` |
| Secteur cible (NAF IT/santé/industrie) | +15 | data-pipe `sirene` |
| Événement BODACC récent (levée, fusion, création) | +10 | data-pipe `bodacc` |
| Éligible à des aides/subventions | +10 | data-pipe `aides` |

**Seuil lead chaud : >= 50 points**

## Orchestration

Étapes à suivre dans l'ordre :

1. **Identification** : Résoudre le SIRET via `sirene` (recherche par nom si nécessaire). Extraire : raison sociale, NAF, effectif, adresse, région.
2. **Check CNIL** : Interroger le data-pipe `cnil` pour vérifier si un DPO est déclaré pour ce SIREN.
3. **Check France Travail** : Chercher les offres d'emploi récentes de cette entreprise contenant les mots-clés : `DPO`, `RGPD`, `RSSI`, `DevSecOps`, `cybersécurité`, `conformité`.
4. **Check BODACC** : Chercher les publications récentes (< 6 mois) : création, modification, radiation, vente de fonds, procédure collective.
5. **Check Aides** : Vérifier l'éligibilité aux dispositifs d'aide (France Num, BPI, subventions régionales cyber).
6. **Calcul du score** : Additionner les points selon la grille ci-dessus.
7. **Recommandation d'approche** :
   - Score >= 70 : **Appel direct** — lead très chaud, prioriser
   - Score 50-69 : **Email personnalisé** — lead chaud, déclencher séquence outreach
   - Score 30-49 : **Nurturing** — ajouter à la newsletter, surveiller les signaux
   - Score < 30 : **Veille** — pas prioritaire, réévaluer dans 3 mois

## Format de sortie

```json
{
  "siret": "44306184100047",
  "raison_sociale": "ACME SAS",
  "score_total": 65,
  "seuil_lead_chaud": 50,
  "est_lead_chaud": true,
  "signaux": [
    { "signal": "Pas de DPO déclaré", "points": 30, "detail": "Aucun DPO trouvé dans le registre CNIL" },
    { "signal": "Secteur cible", "points": 15, "detail": "NAF 6201Z - Programmation informatique" },
    { "signal": "Cible NIS2", "points": 20, "detail": "120 salariés, entité importante" }
  ],
  "approche_recommandee": "email_personnalise",
  "talking_points": [
    "Pas de DPO déclaré — obligation potentielle selon taille/activité",
    "NIS2 applicable — échéance mise en conformité",
    "Aide France Num potentiellement éligible pour reste à charge 0€"
  ],
  "donnees_entreprise": {
    "naf": "6201Z",
    "effectif": 120,
    "region": "Occitanie",
    "ville": "Toulouse",
    "date_creation": "2005-03-15"
  }
}
```

## Règles

- Toujours vérifier les 5 sources avant de scorer.
- Si une source est indisponible, noter `"source_indisponible": true` dans le signal correspondant et ne pas compter les points.
- Ne jamais inventer de données. Si l'information n'est pas trouvée, l'indiquer clairement.
- Le score est déterministe : mêmes données = même score.
