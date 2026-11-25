---
name: legal-entity-management-api
description: "Legal Entity Management API skill. Use when working with Legal Entity Management for businessLines, documents, legalEntities. Covers 34 endpoints."
version: 1.0.0
generator: lapsh
---

# Legal Entity Management API
API version: 3

## Auth
ApiKey X-API-Key in header | Bearer basic

## Base URL
https://kyc-test.adyen.com/lem/v3

## Setup
1. Set Authorization header with your Bearer token
2. GET /themes -- verify access
3. POST /businessLines -- create first businessLines

## Endpoints

34 endpoints across 5 groups. See references/api-spec.lap for full details.

### businessLines
| Method | Path | Description |
|--------|------|-------------|
| POST | /businessLines | Create a business line |
| GET | /businessLines/{id} | Get a business line |
| DELETE | /businessLines/{id} | Delete a business line |
| PATCH | /businessLines/{id} | Update a business line |

### documents
| Method | Path | Description |
|--------|------|-------------|
| POST | /documents | Upload a document for verification checks |
| GET | /documents/{id} | Get a document |
| DELETE | /documents/{id} | Delete a document |
| PATCH | /documents/{id} | Update a document |

### legalEntities
| Method | Path | Description |
|--------|------|-------------|
| POST | /legalEntities | Create a legal entity |
| GET | /legalEntities/{id} | Get a legal entity |
| PATCH | /legalEntities/{id} | Update a legal entity |
| GET | /legalEntities/{id}/acceptedTermsOfServiceDocument/{termsofserviceacceptancereference} | Get accepted Terms of Service document |
| GET | /legalEntities/{id}/businessLines | Get all business lines under a legal entity |
| POST | /legalEntities/{id}/checkTaxElectronicDeliveryConsent | Check the status of consent for electronic delivery of tax forms |
| POST | /legalEntities/{id}/checkVerificationErrors | Check a legal entity's verification errors |
| POST | /legalEntities/{id}/confirmDataReview | Confirm data review |
| POST | /legalEntities/{id}/onboardingLinks | Get a link to an Adyen-hosted onboarding page |
| GET | /legalEntities/{id}/pciQuestionnaires | Get PCI questionnaire details |
| POST | /legalEntities/{id}/pciQuestionnaires/generatePciTemplates | Generate PCI questionnaire |
| POST | /legalEntities/{id}/pciQuestionnaires/signPciTemplates | Sign PCI questionnaire |
| POST | /legalEntities/{id}/pciQuestionnaires/signingRequired | Calculate PCI status of a legal entity |
| GET | /legalEntities/{id}/pciQuestionnaires/{pciid} | Get PCI questionnaire |
| POST | /legalEntities/{id}/setTaxElectronicDeliveryConsent | Set the consent status for electronic delivery of tax forms |
| POST | /legalEntities/{id}/termsOfService | Get Terms of Service document |
| PATCH | /legalEntities/{id}/termsOfService/{termsofservicedocumentid} | Accept Terms of Service |
| GET | /legalEntities/{id}/termsOfServiceAcceptanceInfos | Get Terms of Service information for a legal entity |
| GET | /legalEntities/{id}/termsOfServiceStatus | Get Terms of Service status |
| POST | /legalEntities/{id}/requestPeriodicReview | Request periodic data review. |

### themes
| Method | Path | Description |
|--------|------|-------------|
| GET | /themes | Get a list of hosted onboarding page themes |
| GET | /themes/{id} | Get an onboarding link theme |

### transferInstruments
| Method | Path | Description |
|--------|------|-------------|
| POST | /transferInstruments | Create a transfer instrument |
| GET | /transferInstruments/{id} | Get a transfer instrument |
| DELETE | /transferInstruments/{id} | Delete a transfer instrument |
| PATCH | /transferInstruments/{id} | Update a transfer instrument |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a businessLine?" -> POST /businessLines
- "Get businessLine details?" -> GET /businessLines/{id}
- "Delete a businessLine?" -> DELETE /businessLines/{id}
- "Partially update a businessLine?" -> PATCH /businessLines/{id}
- "Create a document?" -> POST /documents
- "Get document details?" -> GET /documents/{id}
- "Delete a document?" -> DELETE /documents/{id}
- "Partially update a document?" -> PATCH /documents/{id}
- "Create a legalEntity?" -> POST /legalEntities
- "Get legalEntity details?" -> GET /legalEntities/{id}
- "Partially update a legalEntity?" -> PATCH /legalEntities/{id}
- "Get acceptedTermsOfServiceDocument details?" -> GET /legalEntities/{id}/acceptedTermsOfServiceDocument/{termsofserviceacceptancereference}
- "List all businessLines?" -> GET /legalEntities/{id}/businessLines
- "Create a checkTaxElectronicDeliveryConsent?" -> POST /legalEntities/{id}/checkTaxElectronicDeliveryConsent
- "Create a checkVerificationError?" -> POST /legalEntities/{id}/checkVerificationErrors
- "Create a confirmDataReview?" -> POST /legalEntities/{id}/confirmDataReview
- "Create a onboardingLink?" -> POST /legalEntities/{id}/onboardingLinks
- "List all pciQuestionnaires?" -> GET /legalEntities/{id}/pciQuestionnaires
- "Create a generatePciTemplate?" -> POST /legalEntities/{id}/pciQuestionnaires/generatePciTemplates
- "Create a signPciTemplate?" -> POST /legalEntities/{id}/pciQuestionnaires/signPciTemplates
- "Create a signingRequired?" -> POST /legalEntities/{id}/pciQuestionnaires/signingRequired
- "Get pciQuestionnaire details?" -> GET /legalEntities/{id}/pciQuestionnaires/{pciid}
- "Create a setTaxElectronicDeliveryConsent?" -> POST /legalEntities/{id}/setTaxElectronicDeliveryConsent
- "Create a termsOfService?" -> POST /legalEntities/{id}/termsOfService
- "Partially update a termsOfService?" -> PATCH /legalEntities/{id}/termsOfService/{termsofservicedocumentid}
- "List all termsOfServiceAcceptanceInfos?" -> GET /legalEntities/{id}/termsOfServiceAcceptanceInfos
- "List all termsOfServiceStatus?" -> GET /legalEntities/{id}/termsOfServiceStatus
- "List all themes?" -> GET /themes
- "Get theme details?" -> GET /themes/{id}
- "Create a transferInstrument?" -> POST /transferInstruments
- "Get transferInstrument details?" -> GET /transferInstruments/{id}
- "Delete a transferInstrument?" -> DELETE /transferInstruments/{id}
- "Partially update a transferInstrument?" -> PATCH /transferInstruments/{id}
- "Create a requestPeriodicReview?" -> POST /legalEntities/{id}/requestPeriodicReview
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
