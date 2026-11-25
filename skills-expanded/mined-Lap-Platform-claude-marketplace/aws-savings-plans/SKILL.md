---
name: aws-savings-plans
description: "AWS Savings Plans API skill. Use when working with AWS Savings Plans for CreateSavingsPlan, DeleteQueuedSavingsPlan, DescribeSavingsPlanRates. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Savings Plans
API version: 2019-06-28

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /CreateSavingsPlan -- create first CreateSavingsPlan

## Endpoints

10 endpoints across 10 groups. See references/api-spec.lap for full details.

### CreateSavingsPlan
| Method | Path | Description |
|--------|------|-------------|
| POST | /CreateSavingsPlan | Creates a Savings Plan. |

### DeleteQueuedSavingsPlan
| Method | Path | Description |
|--------|------|-------------|
| POST | /DeleteQueuedSavingsPlan | Deletes the queued purchase for the specified Savings Plan. |

### DescribeSavingsPlanRates
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeSavingsPlanRates | Describes the rates for the specified Savings Plan. |

### DescribeSavingsPlans
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeSavingsPlans | Describes the specified Savings Plans. |

### DescribeSavingsPlansOfferingRates
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeSavingsPlansOfferingRates | Describes the offering rates for the specified Savings Plans. |

### DescribeSavingsPlansOfferings
| Method | Path | Description |
|--------|------|-------------|
| POST | /DescribeSavingsPlansOfferings | Describes the offerings for the specified Savings Plans. |

### ListTagsForResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /ListTagsForResource | Lists the tags for the specified resource. |

### ReturnSavingsPlan
| Method | Path | Description |
|--------|------|-------------|
| POST | /ReturnSavingsPlan | Returns the specified Savings Plan. |

### TagResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /TagResource | Adds the specified tags to the specified resource. |

### UntagResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /UntagResource | Removes the specified tags from the specified resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a CreateSavingsPlan?" -> POST /CreateSavingsPlan
- "Create a DeleteQueuedSavingsPlan?" -> POST /DeleteQueuedSavingsPlan
- "Create a DescribeSavingsPlanRate?" -> POST /DescribeSavingsPlanRates
- "Create a DescribeSavingsPlan?" -> POST /DescribeSavingsPlans
- "Create a DescribeSavingsPlansOfferingRate?" -> POST /DescribeSavingsPlansOfferingRates
- "Create a DescribeSavingsPlansOffering?" -> POST /DescribeSavingsPlansOfferings
- "Create a ListTagsForResource?" -> POST /ListTagsForResource
- "Create a ReturnSavingsPlan?" -> POST /ReturnSavingsPlan
- "Create a TagResource?" -> POST /TagResource
- "Create a UntagResource?" -> POST /UntagResource
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
