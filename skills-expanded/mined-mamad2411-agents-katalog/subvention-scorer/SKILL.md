---
name: subvention-scorer
description: "Matcher subventions éligibles par prestation et scorer pertinence pour une association cible. Utiliser pour financement, aides, subventions."
metadata: { "openclaw": { "emoji": "💰" } }
user-invocable: true
---

# Skill: Subvention Scorer

## Quand utiliser cette skill

Utiliser cette skill dès que l'utilisateur demande :
- Quelles subventions sont disponibles pour financer une prestation numérique
- Calculer le reste à charge d'une association pour un projet digital
- Trouver des associations éligibles à des aides pour un type de prestation
- Vérifier si une association peut obtenir un financement 0€ sur une mission
- Toute question commençant par "quelles aides", "quel financement", "subventions pour"

Ne pas utiliser pour construire un pipeline commercial complet → utiliser `lead-pipeline` à la place.

---

## Types de prestations reconnus

| Code                    | Libellé complet                          |
|-------------------------|------------------------------------------|
| `audit_digital`         | Audit de maturité numérique              |
| `site_web`              | Création / refonte site web              |
| `formation_numerique`   | Formation et montée en compétences       |
| `cybersecurite`         | Audit et mise en conformité sécurité     |
| `rgpd`                  | Mise en conformité RGPD                  |
| `crm`                   | Déploiement outil CRM / GRC              |
| `communication_digitale`| Stratégie et outils communication web    |
| `automatisation`        | Automatisation processus métiers         |

Si l'utilisateur décrit une prestation en langage naturel → mapper vers le code le plus proche avant les appels.

---

## Workflow

```
find_leads_for_prestation → get_subvention_data → get_entity_details (si SIREN connu) → scoring pertinence → output structuré
```

### Étape 1 — Associations candidates par prestation
```
find_leads_for_prestation(
  type_prestation = <code_prestation>,
  department      = <code département si mentionné, sinon omis>
)
```
- Appeler avec le code prestation mappé
- Passer `department` uniquement si l'utilisateur a mentionné un périmètre géographique
- Conserver les SIRENs retournés pour les étapes suivantes

### Étape 2 — Subventions disponibles (LanceDB vector search)
```
get_subvention_data(
  siren           = <siren si association cible connue, sinon omis>,
  secteur         = <secteur d'activité de l'association si connu>,
  type_prestation = <code_prestation>
)
```
- Si un SIREN cible est fourni par l'utilisateur → toujours le passer pour un matching personnalisé
- Si pas de SIREN → appeler en mode "catalogue" (secteur + type_prestation uniquement)
- Les résultats exploitent la recherche vectorielle LanceDB → prioriser les subventions avec le meilleur score de similarité sémantique retourné

### Étape 3 — Enrichissement entité cible (optionnel, si SIREN connu)
```
get_entity_details(siren = <siren>)
```
- Appeler uniquement si un SIREN spécifique est fourni ou identifié à l'étape 1
- Extraire : secteur NAF, effectif, budget annuel, zone géographique, historique subventions reçues
- Ces données alimentent le scoring de pertinence à l'étape suivante

### Étape 4 — Scoring de pertinence (0–10)

Pour chaque subvention retournée, calculer un `score_pertinence` :

| Critère                                    | Points max |
|--------------------------------------------|-----------|
| Correspondance secteur association / subvention | 3      |
| Taille association dans la fourchette cible| 2         |
| Zone géographique couverte (national > régional > département) | 2 |
| Historique : association déjà bénéficiaire de subventions similaires | 2 |
| Subvention active (date limite non dépassée)| 1        |

```
score_pertinence = secteur_match(0-3)
                 + taille_match(0-2)
                 + zone_match(0-2)
                 + historique_match(0-2)
                 + active(0-1)
```

Arrondir au dixième. Conserver uniquement les subventions avec `score_pertinence >= 4`.

### Étape 5 — Calcul reste à charge

Pour chaque subvention retenue :
```
reste_a_charge = montant_prestation_HT × (1 - taux_financement)
```
- Indiquer si le cumul de plusieurs subventions peut couvrir 100 % du coût
- Signaler les cas où le reste à charge estimé est 0 € (objectif business prioritaire)
- Mentionner les plafonds de subvention si la prestation dépasse le montant max financé

### Étape 6 — Output structuré

```json
{
  "siren": "123456789",
  "nom_association": "Association XYZ",
  "type_prestation": "audit_digital",
  "subventions_matchees": [
    {
      "nom": "AMI Inclusion Numérique 2025",
      "porteur": "Agence Nationale de la Cohésion des Territoires",
      "perimetre": "national",
      "montant_max": 15000,
      "taux_financement": 0.80,
      "reste_a_charge_estime": 2000,
      "criteres_cles": ["association loi 1901", "moins de 50 salariés", "secteur inclusion"],
      "score_pertinence": 8.5,
      "date_limite": "2025-09-30",
      "url_dossier": "https://..."
    }
  ],
  "cumul_possible_0_euros": true,
  "note_strategique": "Combinaison AMI Inclusion + subvention régionale couvre 100% du coût."
}
```

---

## Instructions

### Résolution du type de prestation
- "site internet" → `site_web`
- "sécurité informatique" → `cybersecurite`
- "logiciel de gestion" → `crm` ou `automatisation` selon le contexte
- "protection des données" → `rgpd`
- Si ambiguïté → demander à l'utilisateur de choisir entre 2 options avant de lancer

### Priorité des subventions
1. Subventions avec `score_pertinence >= 8` → présenter en premier, annoter "Très bonne correspondance"
2. Score 5–7.9 → "Bonne piste à explorer"
3. Score < 5 → ne pas afficher (filtré à l'étape 4)

### Niveau géographique
- Toujours distinguer clairement :
  - **National** : ADEME, BPI, ANCT, ministères
  - **Régional** : Conseil Régional (fonds FEDER, aides régionales)
  - **Départemental** : Conseil Départemental, DDFIP locale
- Signaler si des subventions régionales nécessitent d'être complétées par la connaissance du territoire

### Règles métier (modèle 0€ reste à charge)
- Toujours calculer si le cumul des subventions disponibles peut atteindre 100 % du coût
- Si oui → mettre en avant "Financement 0€ possible" dans la réponse
- Si non → indiquer le gap et suggérer des pistes complémentaires (mécénat, appel à projets)

### Format de réponse à l'utilisateur
1. Phrase d'accroche : "Pour une prestation [type] en [zone], voici les aides disponibles :"
2. Tableau markdown : nom subvention | montant max | taux | reste à charge | score | deadline
3. Si financement 0€ possible → encadré mis en avant "Financement total possible"
4. Toujours conclure par : "Souhaitez-vous que je génère le dossier de candidature ?"

### Gestion des erreurs
- Si `get_subvention_data` retourne 0 résultat → relancer sans le filtre `siren`, en mode catalogue
- Si `find_leads_for_prestation` échoue → continuer avec `get_subvention_data` seul
- Si les données de subvention sont datées (> 6 mois) → avertir l'utilisateur de vérifier les dates officielles
