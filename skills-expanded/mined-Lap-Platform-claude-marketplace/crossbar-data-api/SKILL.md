---
name: crossbar-data-api
description: "CROssBAR Data API skill. Use when working with CROssBAR Data for activities, assays, drugs. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# CROssBAR Data API
API version: 1.0

## Auth
No authentication required.

## Base URL
https://www.ebi.ac.uk/Tools/crossbar

## Setup
1. No auth setup needed
2. GET /activities -- verify access

## Endpoints

13 endpoints across 10 groups. See references/api-spec.lap for full details.

### activities
| Method | Path | Description |
|--------|------|-------------|
| GET | /activities | Get ChEMBL activities |

### assays
| Method | Path | Description |
|--------|------|-------------|
| GET | /assays | Get ChEMBL assays |

### drugs
| Method | Path | Description |
|--------|------|-------------|
| GET | /drugs | drugs collected from Drugbank |

### efo
| Method | Path | Description |
|--------|------|-------------|
| GET | /efo | Get EFO diseases data |

### hpo
| Method | Path | Description |
|--------|------|-------------|
| GET | /hpo | Get HPO phenotypes data |

### intact
| Method | Path | Description |
|--------|------|-------------|
| GET | /intact | Molecular Interactions collected from IntAct |

### molecules
| Method | Path | Description |
|--------|------|-------------|
| GET | /molecules | Get ChEMBL molecules |

### proteins
| Method | Path | Description |
|--------|------|-------------|
| GET | /proteins | Proteins collected from Uniprot for selective tax ids  HUMAN(9606), MOUSE(10090), RAT(10116), BOVINE(9913), ESCHERICHIA_COLI(83333), SUS_SCROFA(9823), MYCOBACTERIUM_TUBERCULOSIS(83332), ORYCTOLAGUS_CUNICULUS(9986), SACCHAROMYCES_CEREVISIAE(559292), CVHSA(694009) & SARS2(2697049) |

### pubchem
| Method | Path | Description |
|--------|------|-------------|
| GET | /pubchem/bioassays | Get pubchem bioassays |
| GET | /pubchem/bioassays/sids | Get pubchem bioassays associated to particular substance ids (sid) & outcome |
| GET | /pubchem/compounds | Get pubchem compounds |
| GET | /pubchem/substances | Get pubchem substances |

### targets
| Method | Path | Description |
|--------|------|-------------|
| GET | /targets | Get ChEMBL targets |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all activities?" -> GET /activities
- "List all assays?" -> GET /assays
- "List all drugs?" -> GET /drugs
- "List all efo?" -> GET /efo
- "List all hpo?" -> GET /hpo
- "List all intact?" -> GET /intact
- "List all molecules?" -> GET /molecules
- "List all proteins?" -> GET /proteins
- "List all bioassays?" -> GET /pubchem/bioassays
- "List all sids?" -> GET /pubchem/bioassays/sids
- "List all compounds?" -> GET /pubchem/compounds
- "List all substances?" -> GET /pubchem/substances
- "List all targets?" -> GET /targets

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
