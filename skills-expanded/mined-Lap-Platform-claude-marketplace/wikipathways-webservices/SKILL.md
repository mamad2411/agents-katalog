---
name: wikipathways-webservices
description: "WikiPathways Webservices API skill. Use when working with WikiPathways Webservices for listOrganisms, listPathways, getPathway. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# WikiPathways Webservices
API version: 1.0

## Auth
ApiKey auth in query

## Base URL
https://webservice.wikipathways.org/

## Setup
1. Set your API key in the appropriate header
2. GET /listOrganisms -- verify access
3. POST /createPathway -- create first createPathway

## Endpoints

26 endpoints across 26 groups. See references/api-spec.lap for full details.

### listOrganisms
| Method | Path | Description |
|--------|------|-------------|
| GET | /listOrganisms | listOrganisms |

### listPathways
| Method | Path | Description |
|--------|------|-------------|
| GET | /listPathways | listPathways |

### getPathway
| Method | Path | Description |
|--------|------|-------------|
| GET | /getPathway | getPathway |

### getPathwayInfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /getPathwayInfo | getPathwayInfoGet some general info about the pathway, such as the name, species, without downloading the GPML. |

### getPathwayHistory
| Method | Path | Description |
|--------|------|-------------|
| GET | /getPathwayHistory | getPathwayHistoryGet the revision history of a pathway. |

### getRecentChanges
| Method | Path | Description |
|--------|------|-------------|
| GET | /getRecentChanges | getRecentChangesGet the recently changed pathways.<br>Note: the recent changes table only retains items for a limited time (2 months), so there is no guarantee that you will get all changes when the timestamp points to a date that is more than 2 months in the past. |

### login
| Method | Path | Description |
|--------|------|-------------|
| GET | /login | loginStart a logged in session, using an existing WikiPathways account. This function will return an authentication code that can be used to excecute methods that need authentication (e.g. updatePathway). |

### updatePathway
| Method | Path | Description |
|--------|------|-------------|
| GET | /updatePathway | updatePathwayUpdate a pathway on the wiki with the given GPML code.<br>Note: To create/modify pathways via the web service, you need to have an account with web service write permissions. Please contact us to request write access for the web service. |

### createPathway
| Method | Path | Description |
|--------|------|-------------|
| POST | /createPathway | createPathwayCreate a new pathway on the wiki with the given GPML code.<br>Note: To create/modify pathways via the web service, you need to have an account with web service write permissions. Please contact us to request write access for the web service. |

### findPathwaysByText
| Method | Path | Description |
|--------|------|-------------|
| GET | /findPathwaysByText | findPathwaysByText |

### findPathwaysByXref
| Method | Path | Description |
|--------|------|-------------|
| GET | /findPathwaysByXref | findPathwaysByXref |

### removeCurationTag
| Method | Path | Description |
|--------|------|-------------|
| GET | /removeCurationTag | removeCurationTagRemove a curation tag from a pathway. |

### saveCurationTag
| Method | Path | Description |
|--------|------|-------------|
| GET | /saveCurationTag | saveCurationTag |

### getCurationTags
| Method | Path | Description |
|--------|------|-------------|
| GET | /getCurationTags | getCurationTagsGet all curation tags for the given tag name. Use this method if you want to find all pathways that are tagged with a specific curation tag. |

### getCurationTagsByName
| Method | Path | Description |
|--------|------|-------------|
| GET | /getCurationTagsByName | getCurationTagsByNameGet all curation tags for the given tag name. Use this method if you want to find all pathways that are tagged with a specific curation tag. |

### getCurationTagHistory
| Method | Path | Description |
|--------|------|-------------|
| GET | /getCurationTagHistory | getCurationTagHistory |

### getColoredPathway
| Method | Path | Description |
|--------|------|-------------|
| GET | /getColoredPathway | getColoredPathwayGet a colored image version of the pathway. |

### findInteractions
| Method | Path | Description |
|--------|------|-------------|
| GET | /findInteractions | findInteractionsFind interactions defined in WikiPathways pathways. |

### getXrefList
| Method | Path | Description |
|--------|------|-------------|
| GET | /getXrefList | getXrefList |

### findPathwaysByLiterature
| Method | Path | Description |
|--------|------|-------------|
| GET | /findPathwaysByLiterature | findPathwaysByLiterature |

### saveOntologyTag
| Method | Path | Description |
|--------|------|-------------|
| GET | /saveOntologyTag | saveOntologyTag |

### removeOntologyTag
| Method | Path | Description |
|--------|------|-------------|
| GET | /removeOntologyTag | removeOntologyTag |

### getOntologyTermsByPathway
| Method | Path | Description |
|--------|------|-------------|
| GET | /getOntologyTermsByPathway | getOntologyTermsByPathway |

### getPathwaysByOntologyTerm
| Method | Path | Description |
|--------|------|-------------|
| GET | /getPathwaysByOntologyTerm | getPathwaysByOntologyTerm |

### getPathwaysByParentOntologyTerm
| Method | Path | Description |
|--------|------|-------------|
| GET | /getPathwaysByParentOntologyTerm | getPathwaysByParentOntologyTerm |

### getUserByOrcid
| Method | Path | Description |
|--------|------|-------------|
| GET | /getUserByOrcid | getUserByOrcid |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all listOrganisms?" -> GET /listOrganisms
- "List all listPathways?" -> GET /listPathways
- "List all getPathway?" -> GET /getPathway
- "List all getPathwayInfo?" -> GET /getPathwayInfo
- "List all getPathwayHistory?" -> GET /getPathwayHistory
- "List all getRecentChanges?" -> GET /getRecentChanges
- "List all login?" -> GET /login
- "List all updatePathway?" -> GET /updatePathway
- "Create a createPathway?" -> POST /createPathway
- "Search findPathwaysByText?" -> GET /findPathwaysByText
- "List all findPathwaysByXref?" -> GET /findPathwaysByXref
- "List all removeCurationTag?" -> GET /removeCurationTag
- "List all saveCurationTag?" -> GET /saveCurationTag
- "List all getCurationTags?" -> GET /getCurationTags
- "List all getCurationTagsByName?" -> GET /getCurationTagsByName
- "List all getCurationTagHistory?" -> GET /getCurationTagHistory
- "List all getColoredPathway?" -> GET /getColoredPathway
- "Search findInteractions?" -> GET /findInteractions
- "List all getXrefList?" -> GET /getXrefList
- "Search findPathwaysByLiterature?" -> GET /findPathwaysByLiterature
- "List all saveOntologyTag?" -> GET /saveOntologyTag
- "List all removeOntologyTag?" -> GET /removeOntologyTag
- "List all getOntologyTermsByPathway?" -> GET /getOntologyTermsByPathway
- "List all getPathwaysByOntologyTerm?" -> GET /getPathwaysByOntologyTerm
- "List all getPathwaysByParentOntologyTerm?" -> GET /getPathwaysByParentOntologyTerm
- "List all getUserByOrcid?" -> GET /getUserByOrcid
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
