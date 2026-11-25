---
name: fr-fiscalite-investissement
description: French investment taxation for individuals — PEA, CTO, assurance-vie, PER, crypto, dividends, interest, capital gains optimization.
version: "1.0.0"
last-updated: "2026-04-20"
model_tested: "claude-sonnet-4-6"
category: finance
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: fr
geo_relevance: [fr]
priority: medium
dependencies:
  mcp: []
  skills: [fr-fiscalite-particulier]
  apis: []
  data: []
update_sources:
  - url: "https://bofip.impots.gouv.fr"
    check_frequency: "yearly"
    last_checked: "2026-04-20"
license: MIT
---

# Fiscalite des Investissements (Particuliers France)

> **AVERTISSEMENT** : Ne constitue pas un conseil en investissement ou fiscal. Consultez un CGP ou expert-comptable.

## Quand Utiliser

- Choisir entre PEA, CTO, assurance-vie, PER
- Optimiser la fiscalite de ses investissements
- Declarer des plus-values, dividendes, interets
- Comprendre le PFU vs bareme progressif
- Declarer des revenus crypto

## Comparatif des Enveloppes

| Enveloppe | Fiscalite apres delai | Plafond | Sortie | Ideal pour |
|-----------|-----------------------|---------|--------|-----------|
| **PEA** | 17.2% PS apres 5 ans | 150 000 EUR | Libre apres 5 ans | Actions EU long terme |
| **CTO** | 30% PFU (ou bareme) | Illimite | Libre | Actions monde, options |
| **Assurance-vie** | 24.7% apres 8 ans (< 150K) | Illimite | Libre (rachat) | Diversification, succession |
| **PER** | Deductible a l'entree, impose a la sortie | 10% revenus | Retraite (sauf exceptions) | TMI elevee, defiscalisation |
| **Livret A** | Exonere | 22 950 EUR | Libre | Epargne securite |
| **LDDS** | Exonere | 12 000 EUR | Libre | Complement Livret A |

## PFU (Flat Tax) vs Bareme Progressif

| TMI | PFU (30%) | Bareme + PS (17.2%) | Choix optimal |
|-----|-----------|---------------------|---------------|
| 0% | 30% | 17.2% | **Bareme** |
| 11% | 30% | 28.2% | **Bareme** |
| 30% | 30% | 47.2% | **PFU** |
| 41% | 30% | 58.2% | **PFU** |
| 45% | 30% | 62.2% | **PFU** |

**Attention** : le choix bareme est **global** (s'applique a tous les revenus du capital de l'annee).

## Plus-Values Mobilieres (CTO)

- PFU : 12.8% IR + 17.2% PS = **30%**
- Ou bareme progressif + 17.2% PS
- Compensation : les moins-values se compensent avec les plus-values
- Report des moins-values : **10 ans**
- Seuil de cession : pas de seuil minimum (contrairement a avant 2018)

## Dividendes

- PFU : **30%** (12.8% IR + 17.2% PS)
- Ou bareme progressif apres **abattement de 40%** + 17.2% PS
- Acompte de 12.8% preleve a la source (imputable sur IR)

## Crypto-Monnaies (Particuliers)

| Element | Regle |
|---------|-------|
| Taux | PFU 30% ou bareme progressif (option globale) |
| Seuil declaration | Cessions > 305 EUR/an |
| Calcul plus-value | Prix cession - (Prix total acquisition x Prix cession / Valeur totale portefeuille) |
| Methode | Prix moyen pondere d'acquisition (PMP) |
| Obligation declarative | Comptes sur plateformes etrangeres : formulaire 3916-bis |
| Staking/airdrops | Imposes comme BNC si habituels, sinon a la cession |

### Exemple Calcul Crypto
```
Portefeuille : 10 000 EUR investis, valeur actuelle 25 000 EUR
Cession de 5 000 EUR

Plus-value = 5 000 - (10 000 x 5 000 / 25 000)
Plus-value = 5 000 - 2 000 = 3 000 EUR
Impot PFU = 3 000 x 30% = 900 EUR
```

## Assurance-Vie (Detail)

| Duree | Versements < 150K EUR | Versements > 150K EUR |
|-------|----------------------|----------------------|
| < 4 ans | 30% PFU | 30% PFU |
| 4-8 ans | 30% PFU | 30% PFU |
| > 8 ans | 7.5% IR + 17.2% PS = **24.7%** | 12.8% IR + 17.2% PS = 30% |

Abattement annuel (apres 8 ans) : 4 600 EUR (celibataire) / 9 200 EUR (couple).

Succession : abattement de 152 500 EUR par beneficiaire (versements avant 70 ans).

## PER (Plan Epargne Retraite)

- Versements deductibles du revenu imposable (plafond : 10% des revenus N-1, min 4 399 EUR)
- A la sortie (retraite) : capital impose a l'IR, plus-values au PFU
- Deblocage anticipe : achat residence principale, accidents de la vie
- Interessant si TMI >= 30% a l'entree et TMI plus faible a la retraite

## Ce Que Ce Skill Ne Fait PAS

- Ne constitue pas un conseil en investissement
- Ne recommande pas de produits financiers specifiques
- Ne gere pas la fiscalite des non-residents
- Ne couvre pas l'IS (entreprises)
- Ne remplace pas un CGP ou expert-comptable
