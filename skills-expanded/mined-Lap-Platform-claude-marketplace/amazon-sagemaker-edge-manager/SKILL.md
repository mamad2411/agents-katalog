---
name: amazon-sagemaker-edge-manager
description: "Amazon Sagemaker Edge Manager API skill. Use when working with Amazon Sagemaker Edge Manager for GetDeployments, GetDeviceRegistration, SendHeartbeat. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Sagemaker Edge Manager
API version: 2020-09-23

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /GetDeployments -- create first GetDeployments

## Endpoints

3 endpoints across 3 groups. See references/api-spec.lap for full details.

### GetDeployments
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetDeployments | Use to get the active deployments from a device. |

### GetDeviceRegistration
| Method | Path | Description |
|--------|------|-------------|
| POST | /GetDeviceRegistration | Use to check if a device is registered with SageMaker Edge Manager. |

### SendHeartbeat
| Method | Path | Description |
|--------|------|-------------|
| POST | /SendHeartbeat | Use to get the current status of devices registered on SageMaker Edge Manager. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a GetDeployment?" -> POST /GetDeployments
- "Create a GetDeviceRegistration?" -> POST /GetDeviceRegistration
- "Create a SendHeartbeat?" -> POST /SendHeartbeat
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
