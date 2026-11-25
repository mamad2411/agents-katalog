---
name: fr-fec-generator
description: Generate and validate FEC (Fichier des Ecritures Comptables) files compliant with French DGFIP specifications. 18 mandatory fields, tab-delimited, UTF-8.
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
  skills: [fr-comptabilite]
  apis: []
  data: [fec-field-spec.md]
update_sources:
  - url: "https://bofip.impots.gouv.fr"
    check_frequency: "yearly"
    last_checked: "2026-04-17"
license: MIT
---

# FEC Generator (Fichier des Ecritures Comptables)

> **AVERTISSEMENT** : Ce skill aide a la preparation. La validation finale doit etre faite par un expert-comptable. Amende de 5 000 EUR en cas de non-conformite.

## Quand Utiliser

- Generer un fichier FEC a partir de donnees comptables
- Valider un FEC existant avant transmission a la DGFIP
- Comprendre les 18 champs obligatoires
- Corriger les erreurs courantes de format

## Specification du Format

- **Extension** : `.txt`
- **Encodage** : UTF-8
- **Delimiteur** : Tabulation `\t` ou pipe `|` (coherent dans tout le fichier)
- **Nom de fichier** : `{SIREN}FEC{AAAAMMJJ}.txt` (ex: 123456789FEC20251231.txt)
- **Separateur decimal** : Point `.` ou virgule `,` (coherent dans tout le fichier)
- **Couverture** : Toutes les ecritures d'un exercice fiscal complet

## Les 18 Champs Obligatoires

| # | Champ | Description | Format |
|---|-------|-------------|--------|
| 1 | JournalCode | Code du journal | Texte (ex: "VE", "AC", "BQ") |
| 2 | JournalLib | Libelle du journal | Texte (ex: "Ventes", "Achats") |
| 3 | EcritureNum | Numero de l'ecriture | Texte, unique et croissant |
| 4 | EcritureDate | Date de l'ecriture | AAAAMMJJ |
| 5 | CompteNum | Numero de compte PCG | Texte (3 a 12 chiffres) |
| 6 | CompteLib | Libelle du compte | Texte |
| 7 | CompAuxNum | Compte auxiliaire | Texte (ou vide) |
| 8 | CompAuxLib | Libelle auxiliaire | Texte (ou vide) |
| 9 | PieceRef | Reference de la piece | Texte |
| 10 | PieceDate | Date de la piece | AAAAMMJJ |
| 11 | EcritureLib | Libelle de l'ecriture | Texte |
| 12 | Debit | Montant au debit | Numerique (0.00 si vide) |
| 13 | Credit | Montant au credit | Numerique (0.00 si vide) |
| 14 | EcrtureLettrage | Lettrage | Texte (ou vide) |
| 15 | DateLettrage | Date de lettrage | AAAAMMJJ (ou vide) |
| 16 | ValidDate | Date de validation | AAAAMMJJ |
| 17 | Montantdevise | Montant en devise | Numerique (ou vide) |
| 18 | Idevise | Identifiant devise | Texte ISO 4217 (ou vide) |

## Regles de Validation

1. **En-tete obligatoire** : premiere ligne = noms exacts des 18 champs
2. **EcritureNum** : croissant dans le temps, sans trous
3. **Debit + Credit** : jamais les deux non-zero sur la meme ligne
4. **Equilibre** : pour chaque EcritureNum, somme debits = somme credits
5. **CompteNum** : doit correspondre au PCG (classes 1-8)
6. **Dates** : format AAAAMMJJ strict, dans l'exercice fiscal
7. **Delimiteur** : un seul type dans tout le fichier
8. **Decimal** : un seul separateur dans tout le fichier

## Erreurs Courantes

| Erreur | Cause | Correction |
|--------|-------|------------|
| Encodage corrompu | Accents mal encodes | Forcer UTF-8 a l'export |
| Delimiteur mixte | Tab + pipe melanges | Uniformiser |
| EcritureNum non croissant | Ecritures ajoutees hors ordre | Retrier par date |
| SIREN dans nom fichier | SIREN incorrect ou absent | Verifier au registre |
| Debit ET credit non-zero | Ligne avec les deux montants | Splitter en 2 lignes |

## Exemple de FEC Valide

```
JournalCode\tJournalLib\tEcritureNum\tEcritureDate\tCompteNum\tCompteLib\tCompAuxNum\tCompAuxLib\tPieceRef\tPieceDate\tEcritureLib\tDebit\tCredit\tEcrtureLettrage\tDateLettrage\tValidDate\tMontantdevise\tIdevise
VE\tVentes\t001\t20260101\t411000\tClients\tC001\tClient A\tFA-001\t20260101\tFacture janvier\t1200.00\t0.00\t\t\t20260131\t\t
VE\tVentes\t001\t20260101\t706000\tPrestations\t\t\tFA-001\t20260101\tFacture janvier\t0.00\t1000.00\t\t\t20260131\t\t
VE\tVentes\t001\t20260101\t445710\tTVA collectee\t\t\tFA-001\t20260101\tFacture janvier\t0.00\t200.00\t\t\t20260131\t\t
```

## Ce Que Ce Skill Ne Fait PAS

- Ne transmet pas le FEC a la DGFIP (envoi manuel ou via logiciel comptable)
- Ne corrige pas les erreurs comptables de fond (seulement le format)
- Ne genere pas les A-nouveaux (ecriture d'ouverture)

## References

Base legale : Article L47 A-1 du Livre des procedures fiscales
Amende : 5 000 EUR par exercice non conforme (Article 1729 D du CGI)
