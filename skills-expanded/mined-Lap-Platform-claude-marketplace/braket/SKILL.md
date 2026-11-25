---
name: braket
description: "Braket API skill. Use when working with Braket for job, quantum-task, device. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# Braket
API version: 2019-09-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /device/{deviceArn} -- verify access
3. POST /job -- create first job

## Endpoints

13 endpoints across 7 groups. See references/api-spec.lap for full details.

### job
| Method | Path | Description |
|--------|------|-------------|
| PUT | /job/{jobArn}/cancel | Cancels an Amazon Braket job. |
| POST | /job | Creates an Amazon Braket job. |
| GET | /job/{jobArn} | Retrieves the specified Amazon Braket job. |

### quantum-task
| Method | Path | Description |
|--------|------|-------------|
| PUT | /quantum-task/{quantumTaskArn}/cancel | Cancels the specified task. |
| POST | /quantum-task | Creates a quantum task. |
| GET | /quantum-task/{quantumTaskArn} | Retrieves the specified quantum task. |

### device
| Method | Path | Description |
|--------|------|-------------|
| GET | /device/{deviceArn} | Retrieves the devices available in Amazon Braket.  For backwards compatibility with older versions of BraketSchemas, OpenQASM information is omitted from GetDevice API calls. To get this information the user-agent needs to present a recent version of the BraketSchemas (1.8.0 or later). The Braket SDK automatically reports this for you. If you do not see OpenQASM results in the GetDevice response when using a Braket SDK, you may need to set AWS_EXECUTION_ENV environment variable to configure user-agent. See the code examples provided below for how to do this for the AWS CLI, Boto3, and the Go, Java, and JavaScript/TypeScript SDKs. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Shows the tags associated with this resource. |
| POST | /tags/{resourceArn} | Add a tag to the specified resource. |
| DELETE | /tags/{resourceArn} | Remove tags from a resource. |

### devices
| Method | Path | Description |
|--------|------|-------------|
| POST | /devices | Searches for devices using the specified filters. |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /jobs | Searches for Amazon Braket jobs that match the specified filter values. |

### quantum-tasks
| Method | Path | Description |
|--------|------|-------------|
| POST | /quantum-tasks | Searches for tasks that match the specified filter values. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a job?" -> POST /job
- "Create a quantum-task?" -> POST /quantum-task
- "Get device details?" -> GET /device/{deviceArn}
- "Get job details?" -> GET /job/{jobArn}
- "Get quantum-task details?" -> GET /quantum-task/{quantumTaskArn}
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a device?" -> POST /devices
- "Create a job?" -> POST /jobs
- "Create a quantum-task?" -> POST /quantum-tasks
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
