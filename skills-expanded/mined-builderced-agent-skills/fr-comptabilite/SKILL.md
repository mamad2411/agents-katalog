---
name: fr-comptabilite
description: Guide French accounting with Plan Comptable General (PCG), journal entries, TVA declarations, and liasse fiscale preparation.
version: "1.0.0"
last-updated: "2026-04-17"
model_tested: "claude-sonnet-4-6"
category: metier-fr
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: fr
geo_relevance: [fr]
priority: high
dependencies:
  mcp: []
  skills: [fr-fec-generator]
  apis: []
  data: [pcg-classes.md]
update_sources:
  - url: "https://www.anc.gouv.fr"
    check_frequency: "yearly"
    last_checked: "2026-04-17"
license: MIT
---

# Comptabilite Francaise (PCG)

> **AVERTISSEMENT** : Ce skill fournit des orientations. Il ne remplace pas un expert-comptable. Verifiez toujours avec un professionnel qualifie.

## Quand Utiliser

- Structurer des ecritures comptables selon le PCG
- Choisir le bon compte pour une operation
- Preparer une declaration de TVA
- Comprendre la liasse fiscale
- Valider la coherence d'un journal comptable

## Plan Comptable General (PCG) — Structure

Le PCG organise les comptes en 8 classes :

| Classe | Intitule | Type |
|--------|----------|------|
| 1 | Comptes de capitaux | Bilan |
| 2 | Comptes d'immobilisations | Bilan |
| 3 | Comptes de stocks | Bilan |
| 4 | Comptes de tiers | Bilan |
| 5 | Comptes financiers | Bilan |
| 6 | Comptes de charges | Resultat |
| 7 | Comptes de produits | Resultat |
| 8 | Comptes speciaux | Hors bilan |

### Comptes les Plus Utilises (PME)

| Compte | Intitule | Usage Courant |
|--------|----------|---------------|
| 101 | Capital social | Apport initial |
| 164 | Emprunts | Pret bancaire |
| 401 | Fournisseurs | Factures a payer |
| 411 | Clients | Factures a encaisser |
| 512 | Banque | Mouvements bancaires |
| 530 | Caisse | Especes |
| 606 | Achats non stockes | Fournitures, services |
| 607 | Achats de marchandises | Revente |
| 613 | Locations | Loyer bureau |
| 616 | Primes d'assurance | Assurances |
| 622 | Remunerations intermediaires | Honoraires, sous-traitance |
| 625 | Deplacements | Frais de deplacement |
| 626 | Frais postaux et telecoms | Telephone, internet |
| 641 | Remunerations du personnel | Salaires |
| 645 | Charges sociales | Cotisations |
| 706 | Prestations de services | Chiffre d'affaires services |
| 707 | Ventes de marchandises | Chiffre d'affaires ventes |

## Ecriture Comptable — Regles

Toute ecriture respecte le principe de la partie double :
- Total des **debits** = Total des **credits**
- Chaque ecriture a : date, numero de piece, libelle, compte, montant

### Exemple : Achat de fournitures TTC

```
Date: 15/04/2026
Piece: FA-2026-042

  606100  Fournitures bureau     Debit    83.33
  445660  TVA deductible         Debit    16.67
  401000  Fournisseur X         Credit   100.00
```

### Exemple : Encaissement client

```
Date: 20/04/2026
Piece: RE-2026-015

  512000  Banque                 Debit   1200.00
  411000  Client Y              Credit  1200.00
```

## TVA — Taux Applicables (2026)

| Taux | Application |
|------|------------|
| 20% | Taux normal (biens et services standard) |
| 10% | Taux intermediaire (restauration, transport, travaux renovation) |
| 5.5% | Taux reduit (alimentation, livres, energie) |
| 2.1% | Taux super-reduit (medicaments rembourses, presse) |

### Comptes TVA

| Compte | Usage |
|--------|-------|
| 44566 | TVA deductible sur ABS (achats biens et services) |
| 44562 | TVA deductible sur immobilisations |
| 44571 | TVA collectee |
| 44551 | TVA a decaisser |

## Liasse Fiscale — Documents Principaux

| Formulaire | Contenu |
|-----------|---------|
| 2050 | Bilan actif |
| 2051 | Bilan passif |
| 2052-2053 | Compte de resultat |
| 2054 | Immobilisations |
| 2055 | Amortissements |
| 2056 | Provisions |
| 2057 | Etat des echeances |
| 2058-A | Determination du resultat fiscal |
| 2059-A | Affectation du resultat |

## Ce Que Ce Skill Ne Fait PAS

- Ne remplace pas un expert-comptable
- Ne genere pas de declarations fiscales officielles
- Ne calcule pas les cotisations sociales (complexite URSSAF)
- Ne gere pas la paie (domaine specialise)

## References

Source officielle : anc.gouv.fr (Autorite des Normes Comptables)
Voir `references/pcg-classes.md` pour la liste detaillee.
