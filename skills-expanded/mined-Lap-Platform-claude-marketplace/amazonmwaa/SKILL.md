---
name: amazonmwaa
description: "AmazonMWAA API skill. Use when working with AmazonMWAA for clitoken, environments, webtoken. Covers 11 endpoints."
version: 1.0.0
generator: lapsh
---

# AmazonMWAA
API version: 2020-07-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /environments -- verify access
3. POST /clitoken/{Name} -- create first clitoken

## Endpoints

11 endpoints across 5 groups. See references/api-spec.lap for full details.

### clitoken
| Method | Path | Description |
|--------|------|-------------|
| POST | /clitoken/{Name} | Creates a CLI token for the Airflow CLI. To learn more, see Creating an Apache Airflow CLI token. |

### environments
| Method | Path | Description |
|--------|------|-------------|
| PUT | /environments/{Name} | Creates an Amazon Managed Workflows for Apache Airflow (MWAA) environment. |
| DELETE | /environments/{Name} | Deletes an Amazon Managed Workflows for Apache Airflow (MWAA) environment. |
| GET | /environments/{Name} | Describes an Amazon Managed Workflows for Apache Airflow (MWAA) environment. |
| GET | /environments | Lists the Amazon Managed Workflows for Apache Airflow (MWAA) environments. |
| PATCH | /environments/{Name} | Updates an Amazon Managed Workflows for Apache Airflow (MWAA) environment. |

### webtoken
| Method | Path | Description |
|--------|------|-------------|
| POST | /webtoken/{Name} | Creates a web login token for the Airflow Web UI. To learn more, see Creating an Apache Airflow web login token. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{ResourceArn} | Lists the key-value tag pairs associated to the Amazon Managed Workflows for Apache Airflow (MWAA) environment. For example, "Environment": "Staging". |
| POST | /tags/{ResourceArn} | Associates key-value tag pairs to your Amazon Managed Workflows for Apache Airflow (MWAA) environment. |
| DELETE | /tags/{ResourceArn} | Removes key-value tag pairs associated to your Amazon Managed Workflows for Apache Airflow (MWAA) environment. For example, "Environment": "Staging". |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| POST | /metrics/environments/{EnvironmentName} | Internal only. Publishes environment health metrics to Amazon CloudWatch. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a environment?" -> PUT /environments/{Name}
- "Delete a environment?" -> DELETE /environments/{Name}
- "Get environment details?" -> GET /environments/{Name}
- "List all environments?" -> GET /environments
- "Get tag details?" -> GET /tags/{ResourceArn}
- "Delete a tag?" -> DELETE /tags/{ResourceArn}
- "Partially update a environment?" -> PATCH /environments/{Name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
