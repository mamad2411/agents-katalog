---
name: fr-open-data-explorer
description: Exploit French open data sources (SIRENE, INSEE, DVF, cadastre, DPE) for enrichment, analysis, and cross-referencing via data.gouv.fr APIs.
version: "1.0.0"
last-updated: "2026-04-17"
model_tested: "claude-sonnet-4-6"
category: data
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: fr
geo_relevance: [fr]
priority: medium
dependencies:
  mcp: [datagouv]
  skills: []
  apis: [data.gouv.fr, api.insee.fr, cadastre.data.gouv.fr]
  data: [fr-open-data-catalog.md]
update_sources:
  - url: "https://doc.data.gouv.fr/api/reference/"
    check_frequency: "quarterly"
    last_checked: "2026-04-17"
license: MIT
---

# French Open Data Explorer

## Quand Utiliser

- Enrichir des donnees entreprise avec SIRENE
- Analyser le marche immobilier avec DVF
- Obtenir des donnees demographiques INSEE
- Verifier des informations cadastrales
- Analyser la performance energetique (DPE)

## Sources Principales

| Source | Contenu | API | Licence |
|--------|---------|-----|---------|
| SIRENE (INSEE) | 12M+ entreprises, SIRET, NAF, dirigeants | api.insee.fr | Licence Ouverte 2.0 |
| DVF (Etalab) | Transactions immobilieres depuis 2014 | data.gouv.fr | Licence Ouverte 2.0 |
| Cadastre | Parcelles, batiments, adresses | cadastre.data.gouv.fr | Licence Ouverte 2.0 |
| DPE (ADEME) | Diagnostics energetiques batiments | data.ademe.fr | Licence Ouverte 2.0 |
| INSEE | Population, revenus, emploi par commune | api.insee.fr | Licence Ouverte 2.0 |
| BAN | Adresses normalisees (geocodage) | api-adresse.data.gouv.fr | Licence Ouverte 2.0 |
| RNCS | Registre du commerce | data.inpi.fr | Licence Ouverte 2.0 |

## Cas d'Usage

### 1. Enrichissement Entreprise
Objectif : a partir d'un SIRET, obtenir raison sociale, adresse, code NAF, effectif.
```
API: GET https://api.insee.fr/entreprises/sirene/V3.11/siret/{SIRET}
Auth: Bearer token (inscription gratuite api.insee.fr)
```

### 2. Analyse Immobiliere
Objectif : prix au m2 par commune, evolution, comparaison.
```
Dataset: "demandes-de-valeurs-foncieres" sur data.gouv.fr
Filtres: code_commune, type_local, date_mutation
Calcul: prix/surface = prix_m2
```

### 3. Diagnostic Energetique
Objectif : DPE d'un batiment, classe energetique, recommandations.
```
API: data.ademe.fr/datasets/dpe-v2
Filtres: code_postal, adresse, numero_dpe
```

### 4. Geocodage
Objectif : convertir adresse en coordonnees GPS.
```
API: GET https://api-adresse.data.gouv.fr/search/?q={adresse}
Retour: latitude, longitude, score de confiance
```

## Qualite des Donnees

| Source | Fraicheur | Completude | Fiabilite |
|--------|-----------|-----------|-----------|
| SIRENE | Quotidienne | Tres haute | Officielle |
| DVF | Semestrielle | Haute (hors Alsace-Moselle) | Officielle |
| Cadastre | Mensuelle | Haute | Officielle |
| DPE | Continue | Moyenne (pas tous les batiments) | Variable |
| BAN | Continue | Haute | Collaborative |

## Limitations

- DVF : Alsace-Moselle exclue (droit local)
- DPE : ne couvre pas tous les batiments (seulement ventes/locations recentes)
- SIRENE : dirigeants personnes physiques partiellement masques (RGPD)
- Rate limits : varie par API (INSEE = 30 req/min gratuit)

## Ce Que Ce Skill Ne Fait PAS

- Ne stocke pas les donnees (interroge les APIs en temps reel)
- Ne nettoie pas les datasets bruts (guide le processus)
- Ne garantit pas la fraicheur (depend de la source officielle)
- Ne croise pas automatiquement les sources (guide le croisement)
