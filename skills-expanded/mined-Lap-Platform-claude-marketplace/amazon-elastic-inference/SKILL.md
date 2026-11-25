---
name: amazon-elastic-inference
description: "Amazon Elastic  Inference API skill. Use when working with Amazon Elastic  Inference for describe-accelerator-offerings, describe-accelerator-types, describe-accelerators. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Elastic  Inference
API version: 2017-07-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /describe-accelerator-types -- verify access
3. POST /describe-accelerator-offerings -- create first describe-accelerator-offerings

## Endpoints

6 endpoints across 4 groups. See references/api-spec.lap for full details.

### describe-accelerator-offerings
| Method | Path | Description |
|--------|------|-------------|
| POST | /describe-accelerator-offerings | Describes the locations in which a given accelerator type or set of types is present in a given region.   February 15, 2023: Starting April 15, 2023, AWS will not onboard new customers to Amazon Elastic Inference (EI), and will help current customers migrate their workloads to options that offer better price and performance. After April 15, 2023, new customers will not be able to launch instances with Amazon EI accelerators in Amazon SageMaker, Amazon ECS, or Amazon EC2. However, customers who have used Amazon EI at least once during the past 30-day period are considered current customers and will be able to continue using the service. |

### describe-accelerator-types
| Method | Path | Description |
|--------|------|-------------|
| GET | /describe-accelerator-types | Describes the accelerator types available in a given region, as well as their characteristics, such as memory and throughput.   February 15, 2023: Starting April 15, 2023, AWS will not onboard new customers to Amazon Elastic Inference (EI), and will help current customers migrate their workloads to options that offer better price and performance. After April 15, 2023, new customers will not be able to launch instances with Amazon EI accelerators in Amazon SageMaker, Amazon ECS, or Amazon EC2. However, customers who have used Amazon EI at least once during the past 30-day period are considered current customers and will be able to continue using the service. |

### describe-accelerators
| Method | Path | Description |
|--------|------|-------------|
| POST | /describe-accelerators | Describes information over a provided set of accelerators belonging to an account.   February 15, 2023: Starting April 15, 2023, AWS will not onboard new customers to Amazon Elastic Inference (EI), and will help current customers migrate their workloads to options that offer better price and performance. After April 15, 2023, new customers will not be able to launch instances with Amazon EI accelerators in Amazon SageMaker, Amazon ECS, or Amazon EC2. However, customers who have used Amazon EI at least once during the past 30-day period are considered current customers and will be able to continue using the service. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Returns all tags of an Elastic Inference Accelerator.   February 15, 2023: Starting April 15, 2023, AWS will not onboard new customers to Amazon Elastic Inference (EI), and will help current customers migrate their workloads to options that offer better price and performance. After April 15, 2023, new customers will not be able to launch instances with Amazon EI accelerators in Amazon SageMaker, Amazon ECS, or Amazon EC2. However, customers who have used Amazon EI at least once during the past 30-day period are considered current customers and will be able to continue using the service. |
| POST | /tags/{resourceArn} | Adds the specified tags to an Elastic Inference Accelerator.   February 15, 2023: Starting April 15, 2023, AWS will not onboard new customers to Amazon Elastic Inference (EI), and will help current customers migrate their workloads to options that offer better price and performance. After April 15, 2023, new customers will not be able to launch instances with Amazon EI accelerators in Amazon SageMaker, Amazon ECS, or Amazon EC2. However, customers who have used Amazon EI at least once during the past 30-day period are considered current customers and will be able to continue using the service. |
| DELETE | /tags/{resourceArn} | Removes the specified tags from an Elastic Inference Accelerator.   February 15, 2023: Starting April 15, 2023, AWS will not onboard new customers to Amazon Elastic Inference (EI), and will help current customers migrate their workloads to options that offer better price and performance. After April 15, 2023, new customers will not be able to launch instances with Amazon EI accelerators in Amazon SageMaker, Amazon ECS, or Amazon EC2. However, customers who have used Amazon EI at least once during the past 30-day period are considered current customers and will be able to continue using the service. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a describe-accelerator-offering?" -> POST /describe-accelerator-offerings
- "List all describe-accelerator-types?" -> GET /describe-accelerator-types
- "Create a describe-accelerator?" -> POST /describe-accelerators
- "Get tag details?" -> GET /tags/{resourceArn}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
