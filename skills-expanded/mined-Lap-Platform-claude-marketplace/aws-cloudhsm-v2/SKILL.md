---
name: aws-cloudhsm-v2
description: "AWS CloudHSM V2 API skill. Use when working with AWS CloudHSM V2 for root. Covers 18 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS CloudHSM V2
API version: 2017-04-28

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

18 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Copy an CloudHSM cluster backup to a different region.  Cross-account use: No. You cannot perform this operation on an CloudHSM backup in a different Amazon Web Services account. |
| POST | / | Creates a new CloudHSM cluster.  Cross-account use: Yes. To perform this operation with an CloudHSM backup in a different AWS account, specify the full backup ARN in the value of the SourceBackupId parameter. |
| POST | / | Creates a new hardware security module (HSM) in the specified CloudHSM cluster.  Cross-account use: No. You cannot perform this operation on an CloudHSM cluster in a different Amazon Web Service account. |
| POST | / | Deletes a specified CloudHSM backup. A backup can be restored up to 7 days after the DeleteBackup request is made. For more information on restoring a backup, see RestoreBackup.  Cross-account use: No. You cannot perform this operation on an CloudHSM backup in a different Amazon Web Services account. |
| POST | / | Deletes the specified CloudHSM cluster. Before you can delete a cluster, you must delete all HSMs in the cluster. To see if the cluster contains any HSMs, use DescribeClusters. To delete an HSM, use DeleteHsm.  Cross-account use: No. You cannot perform this operation on an CloudHSM cluster in a different Amazon Web Services account. |
| POST | / | Deletes the specified HSM. To specify an HSM, you can use its identifier (ID), the IP address of the HSM's elastic network interface (ENI), or the ID of the HSM's ENI. You need to specify only one of these values. To find these values, use DescribeClusters.  Cross-account use: No. You cannot perform this operation on an CloudHSM hsm in a different Amazon Web Services account. |
| POST | / | Deletes an CloudHSM resource policy. Deleting a resource policy will result in the resource being unshared and removed from any RAM resource shares. Deleting the resource policy attached to a backup will not impact any clusters created from that backup.  Cross-account use: No. You cannot perform this operation on an CloudHSM resource in a different Amazon Web Services account. |
| POST | / | Gets information about backups of CloudHSM clusters. Lists either the backups you own or the backups shared with you when the Shared parameter is true. This is a paginated operation, which means that each response might contain only a subset of all the backups. When the response contains only a subset of backups, it includes a NextToken value. Use this value in a subsequent DescribeBackups request to get more backups. When you receive a response with no NextToken (or an empty or null value), that means there are no more backups to get.  Cross-account use: Yes. Customers can describe backups in other Amazon Web Services accounts that are shared with them. |
| POST | / | Gets information about CloudHSM clusters. This is a paginated operation, which means that each response might contain only a subset of all the clusters. When the response contains only a subset of clusters, it includes a NextToken value. Use this value in a subsequent DescribeClusters request to get more clusters. When you receive a response with no NextToken (or an empty or null value), that means there are no more clusters to get.  Cross-account use: No. You cannot perform this operation on CloudHSM clusters in a different Amazon Web Services account. |
| POST | / | Retrieves the resource policy document attached to a given resource.   Cross-account use: No. You cannot perform this operation on an CloudHSM resource in a different Amazon Web Services account. |
| POST | / | Claims an CloudHSM cluster by submitting the cluster certificate issued by your issuing certificate authority (CA) and the CA's root certificate. Before you can claim a cluster, you must sign the cluster's certificate signing request (CSR) with your issuing CA. To get the cluster's CSR, use DescribeClusters.  Cross-account use: No. You cannot perform this operation on an CloudHSM cluster in a different Amazon Web Services account. |
| POST | / | Gets a list of tags for the specified CloudHSM cluster. This is a paginated operation, which means that each response might contain only a subset of all the tags. When the response contains only a subset of tags, it includes a NextToken value. Use this value in a subsequent ListTags request to get more tags. When you receive a response with no NextToken (or an empty or null value), that means there are no more tags to get.  Cross-account use: No. You cannot perform this operation on an CloudHSM resource in a different Amazon Web Services account. |
| POST | / | Modifies attributes for CloudHSM backup.  Cross-account use: No. You cannot perform this operation on an CloudHSM backup in a different Amazon Web Services account. |
| POST | / | Modifies CloudHSM cluster.  Cross-account use: No. You cannot perform this operation on an CloudHSM cluster in a different Amazon Web Services account. |
| POST | / | Creates or updates an CloudHSM resource policy. A resource policy helps you to define the IAM entity (for example, an Amazon Web Services account) that can manage your CloudHSM resources. The following resources support CloudHSM resource policies:     Backup - The resource policy allows you to describe the backup and restore a cluster from the backup in another Amazon Web Services account.   In order to share a backup, it must be in a 'READY' state and you must own it.  While you can share a backup using the CloudHSM PutResourcePolicy operation, we recommend using Resource Access Manager (RAM) instead. Using RAM provides multiple benefits as it creates the policy for you, allows multiple resources to be shared at one time, and increases the discoverability of shared resources. If you use PutResourcePolicy and want consumers to be able to describe the backups you share with them, you must promote the backup to a standard RAM Resource Share using the RAM PromoteResourceShareCreatedFromPolicy API operation. For more information, see  Working with shared backups in the CloudHSM User Guide   Cross-account use: No. You cannot perform this operation on an CloudHSM resource in a different Amazon Web Services account. |
| POST | / | Restores a specified CloudHSM backup that is in the PENDING_DELETION state. For more information on deleting a backup, see DeleteBackup.  Cross-account use: No. You cannot perform this operation on an CloudHSM backup in a different Amazon Web Services account. |
| POST | / | Adds or overwrites one or more tags for the specified CloudHSM cluster.  Cross-account use: No. You cannot perform this operation on an CloudHSM resource in a different Amazon Web Services account. |
| POST | / | Removes the specified tag or tags from the specified CloudHSM cluster.  Cross-account use: No. You cannot perform this operation on an CloudHSM resource in a different Amazon Web Services account. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
