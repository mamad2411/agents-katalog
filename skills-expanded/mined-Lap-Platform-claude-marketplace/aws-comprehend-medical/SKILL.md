---
name: aws-comprehend-medical
description: "AWS Comprehend Medical API skill. Use when working with AWS Comprehend Medical for root. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Comprehend Medical
API version: 2018-10-30

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

26 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Gets the properties associated with a medical entities detection job. Use this operation to get the status of a detection job. |
| POST | / | Gets the properties associated with an InferICD10CM job. Use this operation to get the status of an inference job. |
| POST | / | Gets the properties associated with a protected health information (PHI) detection job. Use this operation to get the status of a detection job. |
| POST | / | Gets the properties associated with an InferRxNorm job. Use this operation to get the status of an inference job. |
| POST | / | Gets the properties associated with an InferSNOMEDCT job. Use this operation to get the status of an inference job. |
| POST | / | The DetectEntities operation is deprecated. You should use the DetectEntitiesV2 operation instead. Inspects the clinical text for a variety of medical entities and returns specific information about them such as entity category, location, and confidence score on that information. |
| POST | / | Inspects the clinical text for a variety of medical entities and returns specific information about them such as entity category, location, and confidence score on that information. Amazon Comprehend Medical only detects medical entities in English language texts. The DetectEntitiesV2 operation replaces the DetectEntities operation. This new action uses a different model for determining the entities in your medical text and changes the way that some entities are returned in the output. You should use the DetectEntitiesV2 operation in all new applications. The DetectEntitiesV2 operation returns the Acuity and Direction entities as attributes instead of types. |
| POST | / | Inspects the clinical text for protected health information (PHI) entities and returns the entity category, location, and confidence score for each entity. Amazon Comprehend Medical only detects entities in English language texts. |
| POST | / | InferICD10CM detects medical conditions as entities listed in a patient record and links those entities to normalized concept identifiers in the ICD-10-CM knowledge base from the Centers for Disease Control. Amazon Comprehend Medical only detects medical entities in English language texts. |
| POST | / | InferRxNorm detects medications as entities listed in a patient record and links to the normalized concept identifiers in the RxNorm database from the National Library of Medicine. Amazon Comprehend Medical only detects medical entities in English language texts. |
| POST | / | InferSNOMEDCT detects possible medical concepts as entities and links them to codes from the Systematized Nomenclature of Medicine, Clinical Terms (SNOMED-CT) ontology |
| POST | / | Gets a list of medical entity detection jobs that you have submitted. |
| POST | / | Gets a list of InferICD10CM jobs that you have submitted. |
| POST | / | Gets a list of protected health information (PHI) detection jobs you have submitted. |
| POST | / | Gets a list of InferRxNorm jobs that you have submitted. |
| POST | / | Gets a list of InferSNOMEDCT jobs a user has submitted. |
| POST | / | Starts an asynchronous medical entity detection job for a collection of documents. Use the DescribeEntitiesDetectionV2Job operation to track the status of a job. |
| POST | / | Starts an asynchronous job to detect medical conditions and link them to the ICD-10-CM ontology. Use the DescribeICD10CMInferenceJob operation to track the status of a job. |
| POST | / | Starts an asynchronous job to detect protected health information (PHI). Use the DescribePHIDetectionJob operation to track the status of a job. |
| POST | / | Starts an asynchronous job to detect medication entities and link them to the RxNorm ontology. Use the DescribeRxNormInferenceJob operation to track the status of a job. |
| POST | / | Starts an asynchronous job to detect medical concepts and link them to the SNOMED-CT ontology. Use the DescribeSNOMEDCTInferenceJob operation to track the status of a job. |
| POST | / | Stops a medical entities detection job in progress. |
| POST | / | Stops an InferICD10CM inference job in progress. |
| POST | / | Stops a protected health information (PHI) detection job in progress. |
| POST | / | Stops an InferRxNorm inference job in progress. |
| POST | / | Stops an InferSNOMEDCT inference job in progress. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
