---
name: aws-price-list-service
description: "AWS Price List Service API skill. Use when working with AWS Price List Service for root. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Price List Service
API version: 2017-10-15

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Returns the metadata for one service or a list of the metadata for all services. Use this without a service code to get the service codes for all services. Use it with a service code, such as AmazonEC2, to get information specific to that service, such as the attribute names available for that service. For example, some of the attribute names available for EC2 are volumeType, maxIopsVolume, operation, locationType, and instanceCapacity10xlarge. |
| POST | / | Returns a list of attribute values. Attributes are similar to the details in a Price List API offer file. For a list of available attributes, see Offer File Definitions in the Billing and Cost Management User Guide. |
| POST | / | This feature is in preview release and is subject to change. Your use of Amazon Web Services Price List API is subject to the Beta Service Participation terms of the Amazon Web Services Service Terms (Section 1.10).   This returns the URL that you can retrieve your Price List file from. This URL is based on the PriceListArn and FileFormat that you retrieve from the ListPriceLists response. |
| POST | / | Returns a list of all products that match the filter criteria. |
| POST | / | This feature is in preview release and is subject to change. Your use of Amazon Web Services Price List API is subject to the Beta Service Participation terms of the Amazon Web Services Service Terms (Section 1.10).   This returns a list of Price List references that the requester if authorized to view, given a ServiceCode, CurrencyCode, and an EffectiveDate. Use without a RegionCode filter to list Price List references from all available Amazon Web Services Regions. Use with a RegionCode filter to get the Price List reference that's specific to a specific Amazon Web Services Region. You can use the PriceListArn from the response to get your preferred Price List files through the GetPriceListFileUrl API. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
