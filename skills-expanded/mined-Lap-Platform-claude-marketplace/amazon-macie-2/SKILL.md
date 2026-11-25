---
name: amazon-macie-2
description: "Amazon Macie 2 API skill. Use when working with Amazon Macie 2 for invitations, custom-data-identifiers, automated-discovery. Covers 81 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Macie 2
API version: 2020-01-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /admin/configuration -- verify access
3. POST /invitations/accept -- create first accept

## Endpoints

81 endpoints across 22 groups. See references/api-spec.lap for full details.

### invitations
| Method | Path | Description |
|--------|------|-------------|
| POST | /invitations/accept | Accepts an Amazon Macie membership invitation that was received from a specific account. |
| POST | /invitations | Sends an Amazon Macie membership invitation to one or more accounts. |
| POST | /invitations/decline | Declines Amazon Macie membership invitations that were received from specific accounts. |
| POST | /invitations/delete | Deletes Amazon Macie membership invitations that were received from specific accounts. |
| GET | /invitations/count | Retrieves the count of Amazon Macie membership invitations that were received by an account. |
| GET | /invitations | Retrieves information about Amazon Macie membership invitations that were received by an account. |

### custom-data-identifiers
| Method | Path | Description |
|--------|------|-------------|
| POST | /custom-data-identifiers/get | Retrieves information about one or more custom data identifiers. |
| POST | /custom-data-identifiers | Creates and defines the criteria and other settings for a custom data identifier. |
| DELETE | /custom-data-identifiers/{id} | Soft deletes a custom data identifier. |
| GET | /custom-data-identifiers/{id} | Retrieves the criteria and other settings for a custom data identifier. |
| POST | /custom-data-identifiers/list | Retrieves a subset of information about all the custom data identifiers for an account. |
| POST | /custom-data-identifiers/test | Tests criteria for a custom data identifier. |

### automated-discovery
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /automated-discovery/accounts | Changes the status of automated sensitive data discovery for one or more accounts. |
| GET | /automated-discovery/configuration | Retrieves the configuration settings and status of automated sensitive data discovery for an organization or standalone account. |
| GET | /automated-discovery/accounts | Retrieves the status of automated sensitive data discovery for one or more accounts. |
| PUT | /automated-discovery/configuration | Changes the configuration settings and status of automated sensitive data discovery for an organization or standalone account. |

### allow-lists
| Method | Path | Description |
|--------|------|-------------|
| POST | /allow-lists | Creates and defines the settings for an allow list. |
| DELETE | /allow-lists/{id} | Deletes an allow list. |
| GET | /allow-lists/{id} | Retrieves the settings and status of an allow list. |
| GET | /allow-lists | Retrieves a subset of information about all the allow lists for an account. |
| PUT | /allow-lists/{id} | Updates the settings for an allow list. |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /jobs | Creates and defines the settings for a classification job. |
| GET | /jobs/{jobId} | Retrieves the status and settings for a classification job. |
| POST | /jobs/list | Retrieves a subset of information about one or more classification jobs. |
| PATCH | /jobs/{jobId} | Changes the status of a classification job. |

### findingsfilters
| Method | Path | Description |
|--------|------|-------------|
| POST | /findingsfilters | Creates and defines the criteria and other settings for a findings filter. |
| DELETE | /findingsfilters/{id} | Deletes a findings filter. |
| GET | /findingsfilters/{id} | Retrieves the criteria and other settings for a findings filter. |
| GET | /findingsfilters | Retrieves a subset of information about all the findings filters for an account. |
| PATCH | /findingsfilters/{id} | Updates the criteria and other settings for a findings filter. |

### members
| Method | Path | Description |
|--------|------|-------------|
| POST | /members | Associates an account with an Amazon Macie administrator account. |
| DELETE | /members/{id} | Deletes the association between an Amazon Macie administrator account and an account. |
| POST | /members/disassociate/{id} | Disassociates an Amazon Macie administrator account from a member account. |
| GET | /members/{id} | Retrieves information about an account that's associated with an Amazon Macie administrator account. |
| GET | /members | Retrieves information about the accounts that are associated with an Amazon Macie administrator account. |

### findings
| Method | Path | Description |
|--------|------|-------------|
| POST | /findings/sample | Creates sample findings. |
| POST | /findings/statistics | Retrieves (queries) aggregated statistical data about findings. |
| POST | /findings/describe | Retrieves the details of one or more findings. |
| GET | /findings/{findingId}/reveal | Retrieves occurrences of sensitive data reported by a finding. |
| GET | /findings/{findingId}/reveal/availability | Checks whether occurrences of sensitive data can be retrieved for a finding. |
| POST | /findings | Retrieves a subset of information about one or more findings. |

### datasources
| Method | Path | Description |
|--------|------|-------------|
| POST | /datasources/s3 | Retrieves (queries) statistical data and other information about one or more S3 buckets that Amazon Macie monitors and analyzes for an account. |
| POST | /datasources/s3/statistics | Retrieves (queries) aggregated statistical data about all the S3 buckets that Amazon Macie monitors and analyzes for an account. |
| POST | /datasources/search-resources | Retrieves (queries) statistical data and other information about Amazon Web Services resources that Amazon Macie monitors and analyzes. |

### admin
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin/configuration | Retrieves the Amazon Macie configuration settings for an organization in Organizations. |
| DELETE | /admin | Disables an account as the delegated Amazon Macie administrator account for an organization in Organizations. |
| POST | /admin | Designates an account as the delegated Amazon Macie administrator account for an organization in Organizations. |
| GET | /admin | Retrieves information about the delegated Amazon Macie administrator account for an organization in Organizations. |
| PATCH | /admin/configuration | Updates the Amazon Macie configuration settings for an organization in Organizations. |

### macie
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /macie | Disables Amazon Macie and deletes all settings and resources for a Macie account. |
| POST | /macie | Enables Amazon Macie and specifies the configuration settings for a Macie account. |
| GET | /macie | Retrieves the status and configuration settings for an Amazon Macie account. |
| PATCH | /macie | Suspends or re-enables Amazon Macie, or updates the configuration settings for a Macie account. |
| PATCH | /macie/members/{id} | Enables an Amazon Macie administrator to suspend or re-enable Macie for a member account. |

### administrator
| Method | Path | Description |
|--------|------|-------------|
| POST | /administrator/disassociate | Disassociates a member account from its Amazon Macie administrator account. |
| GET | /administrator | Retrieves information about the Amazon Macie administrator account for an account. |

### master
| Method | Path | Description |
|--------|------|-------------|
| POST | /master/disassociate | (Deprecated) Disassociates a member account from its Amazon Macie administrator account. This operation has been replaced by the DisassociateFromAdministratorAccount operation. |
| GET | /master | (Deprecated) Retrieves information about the Amazon Macie administrator account for an account. This operation has been replaced by the GetAdministratorAccount operation. |

### classification-export-configuration
| Method | Path | Description |
|--------|------|-------------|
| GET | /classification-export-configuration | Retrieves the configuration settings for storing data classification results. |
| PUT | /classification-export-configuration | Adds or updates the configuration settings for storing data classification results. |

### classification-scopes
| Method | Path | Description |
|--------|------|-------------|
| GET | /classification-scopes/{id} | Retrieves the classification scope settings for an account. |
| GET | /classification-scopes | Retrieves a subset of information about the classification scope for an account. |
| PATCH | /classification-scopes/{id} | Updates the classification scope settings for an account. |

### findings-publication-configuration
| Method | Path | Description |
|--------|------|-------------|
| GET | /findings-publication-configuration | Retrieves the configuration settings for publishing findings to Security Hub. |
| PUT | /findings-publication-configuration | Updates the configuration settings for publishing findings to Security Hub. |

### resource-profiles
| Method | Path | Description |
|--------|------|-------------|
| GET | /resource-profiles | Retrieves (queries) sensitive data discovery statistics and the sensitivity score for an S3 bucket. |
| GET | /resource-profiles/artifacts | Retrieves information about objects that Amazon Macie selected from an S3 bucket for automated sensitive data discovery. |
| GET | /resource-profiles/detections | Retrieves information about the types and amount of sensitive data that Amazon Macie found in an S3 bucket. |
| PATCH | /resource-profiles | Updates the sensitivity score for an S3 bucket. |
| PATCH | /resource-profiles/detections | Updates the sensitivity scoring settings for an S3 bucket. |

### reveal-configuration
| Method | Path | Description |
|--------|------|-------------|
| GET | /reveal-configuration | Retrieves the status and configuration settings for retrieving occurrences of sensitive data reported by findings. |
| PUT | /reveal-configuration | Updates the status and configuration settings for retrieving occurrences of sensitive data reported by findings. |

### templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /templates/sensitivity-inspections/{id} | Retrieves the settings for the sensitivity inspection template for an account. |
| GET | /templates/sensitivity-inspections | Retrieves a subset of information about the sensitivity inspection template for an account. |
| PUT | /templates/sensitivity-inspections/{id} | Updates the settings for the sensitivity inspection template for an account. |

### usage
| Method | Path | Description |
|--------|------|-------------|
| POST | /usage/statistics | Retrieves (queries) quotas and aggregated usage data for one or more accounts. |
| GET | /usage | Retrieves (queries) aggregated usage data for an account. |

### managed-data-identifiers
| Method | Path | Description |
|--------|------|-------------|
| POST | /managed-data-identifiers/list | Retrieves information about all the managed data identifiers that Amazon Macie currently provides. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Retrieves the tags (keys and values) that are associated with an Amazon Macie resource. |
| POST | /tags/{resourceArn} | Adds or updates one or more tags (keys and values) that are associated with an Amazon Macie resource. |
| DELETE | /tags/{resourceArn} | Removes one or more tags (keys and values) from an Amazon Macie resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a accept?" -> POST /invitations/accept
- "Create a get?" -> POST /custom-data-identifiers/get
- "Create a allow-list?" -> POST /allow-lists
- "Create a job?" -> POST /jobs
- "Create a custom-data-identifier?" -> POST /custom-data-identifiers
- "Create a findingsfilter?" -> POST /findingsfilters
- "Create a invitation?" -> POST /invitations
- "Create a member?" -> POST /members
- "Create a sample?" -> POST /findings/sample
- "Create a decline?" -> POST /invitations/decline
- "Delete a allow-list?" -> DELETE /allow-lists/{id}
- "Delete a custom-data-identifier?" -> DELETE /custom-data-identifiers/{id}
- "Delete a findingsfilter?" -> DELETE /findingsfilters/{id}
- "Create a delete?" -> POST /invitations/delete
- "Delete a member?" -> DELETE /members/{id}
- "Create a s3?" -> POST /datasources/s3
- "Get job details?" -> GET /jobs/{jobId}
- "List all configuration?" -> GET /admin/configuration
- "Create a disassociate?" -> POST /administrator/disassociate
- "Create a disassociate?" -> POST /master/disassociate
- "Create a macie?" -> POST /macie
- "Create a admin?" -> POST /admin
- "List all administrator?" -> GET /administrator
- "Get allow-list details?" -> GET /allow-lists/{id}
- "List all configuration?" -> GET /automated-discovery/configuration
- "Create a statistic?" -> POST /datasources/s3/statistics
- "List all classification-export-configuration?" -> GET /classification-export-configuration
- "Get classification-scope details?" -> GET /classification-scopes/{id}
- "Get custom-data-identifier details?" -> GET /custom-data-identifiers/{id}
- "Create a statistic?" -> POST /findings/statistics
- "Create a describe?" -> POST /findings/describe
- "Get findingsfilter details?" -> GET /findingsfilters/{id}
- "List all findings-publication-configuration?" -> GET /findings-publication-configuration
- "List all count?" -> GET /invitations/count
- "List all macie?" -> GET /macie
- "List all master?" -> GET /master
- "Get member details?" -> GET /members/{id}
- "List all resource-profiles?" -> GET /resource-profiles
- "List all reveal-configuration?" -> GET /reveal-configuration
- "List all reveal?" -> GET /findings/{findingId}/reveal
- "List all availability?" -> GET /findings/{findingId}/reveal/availability
- "Get sensitivity-inspection details?" -> GET /templates/sensitivity-inspections/{id}
- "Create a statistic?" -> POST /usage/statistics
- "List all usage?" -> GET /usage
- "List all allow-lists?" -> GET /allow-lists
- "List all accounts?" -> GET /automated-discovery/accounts
- "Create a list?" -> POST /jobs/list
- "List all classification-scopes?" -> GET /classification-scopes
- "Create a list?" -> POST /custom-data-identifiers/list
- "Create a finding?" -> POST /findings
- "List all findingsfilters?" -> GET /findingsfilters
- "List all invitations?" -> GET /invitations
- "Create a list?" -> POST /managed-data-identifiers/list
- "List all members?" -> GET /members
- "List all admin?" -> GET /admin
- "List all artifacts?" -> GET /resource-profiles/artifacts
- "List all detections?" -> GET /resource-profiles/detections
- "List all sensitivity-inspections?" -> GET /templates/sensitivity-inspections
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a search-resource?" -> POST /datasources/search-resources
- "Create a test?" -> POST /custom-data-identifiers/test
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Update a allow-list?" -> PUT /allow-lists/{id}
- "Partially update a job?" -> PATCH /jobs/{jobId}
- "Partially update a classification-scope?" -> PATCH /classification-scopes/{id}
- "Partially update a findingsfilter?" -> PATCH /findingsfilters/{id}
- "Partially update a member?" -> PATCH /macie/members/{id}
- "Update a sensitivity-inspection?" -> PUT /templates/sensitivity-inspections/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
