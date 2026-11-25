---
name: aws-license-manager
description: "AWS License Manager API skill. Use when working with AWS License Manager for root. Covers 50 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS License Manager
API version: 2018-08-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

50 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Accepts the specified grant. |
| POST | / | Checks in the specified license. Check in a license when it is no longer in use. |
| POST | / | Checks out the specified license for offline use. |
| POST | / | Checks out the specified license.  If the account that created the license is the same that is performing the check out, you must specify the account as the beneficiary. |
| POST | / | Creates a grant for the specified license. A grant shares the use of license entitlements with a specific Amazon Web Services account, an organization, or an organizational unit (OU). For more information, see Granted licenses in License Manager in the License Manager User Guide. |
| POST | / | Creates a new version of the specified grant. For more information, see Granted licenses in License Manager in the License Manager User Guide. |
| POST | / | Creates a license. |
| POST | / | Creates a license configuration. A license configuration is an abstraction of a customer license agreement that can be consumed and enforced by License Manager. Components include specifications for the license type (licensing by instance, socket, CPU, or vCPU), allowed tenancy (shared tenancy, Dedicated Instance, Dedicated Host, or all of these), license affinity to host (how long a license must be associated with a host), and the number of licenses purchased and used. |
| POST | / | Creates a new license conversion task. |
| POST | / | Creates a report generator. |
| POST | / | Creates a new version of the specified license. |
| POST | / | Creates a long-lived token. A refresh token is a JWT token used to get an access token. With an access token, you can call AssumeRoleWithWebIdentity to get role credentials that you can use to call License Manager to manage the specified license. |
| POST | / | Deletes the specified grant. |
| POST | / | Deletes the specified license. |
| POST | / | Deletes the specified license configuration. You cannot delete a license configuration that is in use. |
| POST | / | Deletes the specified report generator. This action deletes the report generator, which stops it from generating future reports. The action cannot be reversed. It has no effect on the previous reports from this generator. |
| POST | / | Deletes the specified token. Must be called in the license home Region. |
| POST | / | Extends the expiration date for license consumption. |
| POST | / | Gets a temporary access token to use with AssumeRoleWithWebIdentity. Access tokens are valid for one hour. |
| POST | / | Gets detailed information about the specified grant. |
| POST | / | Gets detailed information about the specified license. |
| POST | / | Gets detailed information about the specified license configuration. |
| POST | / | Gets information about the specified license type conversion task. |
| POST | / | Gets information about the specified report generator. |
| POST | / | Gets detailed information about the usage of the specified license. |
| POST | / | Gets the License Manager settings for the current Region. |
| POST | / | Lists the resource associations for the specified license configuration. Resource associations need not consume licenses from a license configuration. For example, an AMI or a stopped instance might not consume a license (depending on the license rules). |
| POST | / | Lists the grants distributed for the specified license. |
| POST | / | Lists the license configuration operations that failed. |
| POST | / | Lists the license configurations for your account. |
| POST | / | Lists the license type conversion tasks for your account. |
| POST | / | Lists the report generators for your account. |
| POST | / | Describes the license configurations for the specified resource. |
| POST | / | Lists all versions of the specified license. |
| POST | / | Lists the licenses for your account. |
| POST | / | Lists grants that are received. Received grants are grants created while specifying the recipient as this Amazon Web Services account, your organization, or an organizational unit (OU) to which this member account belongs. |
| POST | / | Lists the grants received for all accounts in the organization. |
| POST | / | Lists received licenses. |
| POST | / | Lists the licenses received for all accounts in the organization. |
| POST | / | Lists resources managed using Systems Manager inventory. |
| POST | / | Lists the tags for the specified license configuration. |
| POST | / | Lists your tokens. |
| POST | / | Lists all license usage records for a license configuration, displaying license consumption details by resource at a selected point in time. Use this action to audit the current license consumption for any license inventory and configuration. |
| POST | / | Rejects the specified grant. |
| POST | / | Adds the specified tags to the specified license configuration. |
| POST | / | Removes the specified tags from the specified license configuration. |
| POST | / | Modifies the attributes of an existing license configuration. |
| POST | / | Updates a report generator. After you make changes to a report generator, it starts generating new reports within 60 minutes of being updated. |
| POST | / | Adds or removes the specified license configurations for the specified Amazon Web Services resource. You can update the license specifications of AMIs, instances, and hosts. You cannot update the license specifications for launch templates and CloudFormation templates, as they send license configurations to the operation that creates the resource. |
| POST | / | Updates License Manager settings for the current Region. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
