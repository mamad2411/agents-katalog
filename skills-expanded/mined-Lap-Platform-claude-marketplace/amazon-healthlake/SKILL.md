---
name: amazon-healthlake
description: "Amazon HealthLake API skill. Use when working with Amazon HealthLake for root. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon HealthLake
API version: 2017-07-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

13 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates a data store that can ingest and export FHIR formatted data. |
| POST | / | Deletes a data store. |
| POST | / | Gets the properties associated with the FHIR data store, including the data store ID, data store ARN, data store name, data store status, when the data store was created, data store type version, and the data store's endpoint. |
| POST | / | Displays the properties of a FHIR export job, including the ID, ARN, name, and the status of the job. |
| POST | / | Displays the properties of a FHIR import job, including the ID, ARN, name, and the status of the job. |
| POST | / | Lists all FHIR data stores that are in the user’s account, regardless of data store status. |
| POST | / | Lists all FHIR export jobs associated with an account and their statuses. |
| POST | / | Lists all FHIR import jobs associated with an account and their statuses. |
| POST | / | Returns a list of all existing tags associated with a data store. |
| POST | / | Begins a FHIR export job. |
| POST | / | Begins a FHIR Import job. |
| POST | / | Adds a user specified key and value tag to a data store. |
| POST | / | Removes tags from a data store. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
