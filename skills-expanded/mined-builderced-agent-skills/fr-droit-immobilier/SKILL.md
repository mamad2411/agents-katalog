---
name: fr-droit-immobilier
description: Navigate French real estate law for individuals — leases, mandatory diagnostics, tenant rights, co-ownership, energy renovation aids (MaPrimeRenov), and rental taxation.
version: "1.0.0"
last-updated: "2026-04-20"
model_tested: "claude-sonnet-4-6"
category: metier-fr
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
  - url: "https://www.service-public.gouv.fr/particuliers/vosdroits/N19808"
    check_frequency: "yearly"
    last_checked: "2026-04-20"
license: MIT
---

# Droit Immobilier France (Particuliers)

> **AVERTISSEMENT** : Orientations generales. Consultez un notaire ou avocat pour toute decision juridique.

## Quand Utiliser

- Acheter ou vendre un bien immobilier
- Signer ou rompre un bail de location
- Comprendre les diagnostics obligatoires
- Calculer des frais de notaire
- Connaitre ses droits de locataire ou proprietaire
- Declarer des revenus fonciers

## Diagnostics Obligatoires (Vente)

Le DDT (Dossier de Diagnostics Techniques) doit contenir :

| Diagnostic | Validite | Obligatoire si |
|-----------|----------|---------------|
| DPE (Performance Energetique) | 10 ans | Toujours |
| Amiante | Illimite si negatif | Permis de construire avant 01/07/1997 |
| Plomb (CREP) | 1 an (vente), 6 ans (location) | Construction avant 01/01/1949 |
| Electricite | 3 ans | Installation > 15 ans |
| Gaz | 3 ans | Installation > 15 ans |
| Termites | 6 mois | Zones a risque (arrete prefectoral) |
| ERP (Risques naturels/techno) | 6 mois | Toujours |
| Assainissement | 3 ans | Non raccorde au tout-a-l'egout |
| Bruit | Illimite | Zone d'exposition au bruit des aerodromes |
| Audit energetique | 10 ans | Logements classes F ou G au DPE (depuis 2023) |

### Interdictions de Location par DPE

| Date | Interdiction |
|------|-------------|
| Depuis 2023 | Logements > 450 kWh/m2/an (G+) |
| Depuis 2025 | Logements classes G |
| 2028 | Logements classes F |
| 2034 | Logements classes E |

## Frais de Notaire (Estimation)

| Composante | Ancien | Neuf |
|-----------|--------|------|
| Droits de mutation | ~5.80% | ~0.71% |
| Emoluments notaire | ~0.80% | ~0.80% |
| Frais divers | ~0.40% | ~0.40% |
| **Total approximatif** | **~7-8%** | **~2-3%** |

## Bail d'Habitation (Loi du 6 juillet 1989)

### Location Vide
- Duree minimum : **3 ans** (proprietaire personne physique) ou **6 ans** (personne morale)
- Preavis locataire : **3 mois** (1 mois en zone tendue, mutation, perte emploi, RSA)
- Preavis proprietaire : **6 mois** avant echeance, motif obligatoire (reprise, vente, motif legitime)
- Depot de garantie : **1 mois** de loyer HC maximum
- Restitution : **1 mois** (si etat des lieux conforme) ou **2 mois** (si degradations)

### Location Meublee
- Duree minimum : **1 an** (9 mois si etudiant)
- Preavis locataire : **1 mois**
- Depot de garantie : **2 mois** maximum

### Encadrement des Loyers
Applicable dans les zones tendues (Paris, Lyon, Lille, Bordeaux, Montpellier, etc.) :
- Loyer de reference fixe par prefet
- Loyer ne peut depasser le **loyer de reference majore** (+20%)
- Complement de loyer possible si caracteristiques exceptionnelles

## Aides a la Renovation Energetique

| Aide | Montant | Conditions |
|------|---------|-----------|
| MaPrimeRenov' | Jusqu'a 90% des travaux | Proprietaires occupants/bailleurs, sous conditions de revenus |
| Eco-PTZ | Jusqu'a 50 000 EUR a taux 0% | Logement > 2 ans, bouquet de travaux |
| CEE (Certificats d'Economie d'Energie) | Variable | Via fournisseurs d'energie |
| TVA reduite | 5.5% au lieu de 20% | Travaux d'amelioration energetique |

## Copropriete (Essentiel)

- Charges generales : reparties selon tantiemes
- Charges speciales : selon utilite pour chaque lot
- AG annuelle obligatoire : convocation 21 jours avant
- Majorites : simple (Art. 24), absolue (Art. 25), double (Art. 26), unanimite
- Fonds travaux obligatoire : 5% du budget previsionnel minimum

## Ce Que Ce Skill Ne Fait PAS

- Ne remplace pas un notaire, avocat ou agent immobilier
- Ne calcule pas de pret immobilier (simulation bancaire)
- Ne genere pas de contrats de bail (templates uniquement)
- Ne couvre pas l'immobilier commercial
- Ne gere pas les litiges (procedure judiciaire)
