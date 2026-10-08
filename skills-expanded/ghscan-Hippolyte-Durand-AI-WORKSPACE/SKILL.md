---
name: <agent-slug>
description: <une ligne — sert au routing L1 de GOUVERNANCE.md>
metadata:
  type: agent
  area: <Perso|Pro|Ecole|Business|Certifs>
  status: draft
---

# <Nom de l'agent>

> Contrat L2 (modèle ICM, voir `GOUVERNANCE.md#contrat-agent`). Ne charge QUE les fichiers de la table Inputs. Budget cible : 2–8K tokens.

## Mission
<1-3 lignes : ce que fait cet agent, pour qui, quand l'invoquer.>

## Inputs
| Fichier | Couche | Sections | Pourquoi |
|---|---|---|---|
| `DOCTRINE.md` | L3 | `#<section>` | contrainte à internaliser |
| `SCHEMA.md` | L3 | `#<type>` | champs/relations si l'agent écrit des notes |
| `<entité>/…` | L4 | tout | artefact du run à traiter |

<!-- L3 = référence stable, internaliser comme contrainte. L4 = artefact du run, traiter comme input. Nommer les sections, jamais le fichier entier. -->

## Process
1. <étape actionnable>
2. <…>

## Outputs
- <fichiers écrits/modifiés>
- Validation : `python3 _APP/check-vault-integrity.py` (doit passer).

## Escalade
Remonte à Hippo si : choix structurant non tranché, hors-scope routing, validation échoue 3× (→ `0-Inbox/` `#erreur-capture`). Sinon tranche seul. (→ `GOUVERNANCE.md#escalade`)

## Memory (L4 propre à l'agent, optionnel)
`Memory/{apprentissages,blocages}.md` — appris/pièges de cet agent, format `### YYYY-MM-DD — Titre`.
