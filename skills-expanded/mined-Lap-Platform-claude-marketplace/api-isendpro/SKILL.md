---
name: api-isendpro
description: "API iSendPro API skill. Use when working with API iSendPro for campagne, comptage, credit. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# API iSendPro
API version: 1.1.1

## Auth
No authentication required.

## Base URL
https://apirest.isendpro.com/cgi-bin

## Setup
1. No auth setup needed
3. POST /campagne -- create first campagne

## Endpoints

14 endpoints across 12 groups. See references/api-spec.lap for full details.

### campagne
| Method | Path | Description |
|--------|------|-------------|
| POST | /campagne | Retourne les SMS envoyés sur une période donnée |

### comptage
| Method | Path | Description |
|--------|------|-------------|
| POST | /comptage | Compter le nombre de caractère |

### credit
| Method | Path | Description |
|--------|------|-------------|
| POST | /credit | Interrogation credit |

### hlr
| Method | Path | Description |
|--------|------|-------------|
| POST | /hlr | Vérifier la validité d'un numéro |

### repertoire
| Method | Path | Description |
|--------|------|-------------|
| POST | /repertoire | Gestion repertoire (creation) |
| PUT | /repertoire | Gestion repertoire (modification) |

### getlistenoire
| Method | Path | Description |
|--------|------|-------------|
| POST | /getlistenoire | Retourne le liste noire |

### setlistenoire
| Method | Path | Description |
|--------|------|-------------|
| POST | /setlistenoire | Ajoute un numero en liste noire |

### dellistenoire
| Method | Path | Description |
|--------|------|-------------|
| POST | /dellistenoire | Ajoute un numero en liste noire |

### shortlink
| Method | Path | Description |
|--------|------|-------------|
| POST | /shortlink | add a shortlink |

### subaccount
| Method | Path | Description |
|--------|------|-------------|
| POST | /subaccount | Ajoute un sous compte |
| PUT | /subaccount | Edit a subaccount |

### sms
| Method | Path | Description |
|--------|------|-------------|
| POST | /sms | Envoyer un sms |

### smsmulti
| Method | Path | Description |
|--------|------|-------------|
| POST | /smsmulti | Envoyer des SMS |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a campagne?" -> POST /campagne
- "Create a comptage?" -> POST /comptage
- "Create a credit?" -> POST /credit
- "Create a hlr?" -> POST /hlr
- "Create a repertoire?" -> POST /repertoire
- "Create a getlistenoire?" -> POST /getlistenoire
- "Create a setlistenoire?" -> POST /setlistenoire
- "Create a dellistenoire?" -> POST /dellistenoire
- "Create a shortlink?" -> POST /shortlink
- "Create a subaccount?" -> POST /subaccount
- "Create a sm?" -> POST /sms
- "Create a smsmulti?" -> POST /smsmulti

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
