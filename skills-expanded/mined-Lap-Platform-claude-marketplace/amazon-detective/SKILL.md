---
name: amazon-detective
description: "Amazon Detective API skill. Use when working with Amazon Detective for invitation, graph, membership. Covers 29 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Detective
API version: 2018-10-26

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /tags/{ResourceArn} -- verify access
3. POST /graph/datasources/get -- create first get

## Endpoints

29 endpoints across 8 groups. See references/api-spec.lap for full details.

### invitation
| Method | Path | Description |
|--------|------|-------------|
| PUT | /invitation | Accepts an invitation for the member account to contribute data to a behavior graph. This operation can only be called by an invited member account.  The request provides the ARN of behavior graph. The member account status in the graph must be INVITED. |
| POST | /invitation/removal | Rejects an invitation to contribute the account data to a behavior graph. This operation must be called by an invited member account that has the INVITED status.  RejectInvitation cannot be called by an organization account in the organization behavior graph. In the organization behavior graph, organization accounts do not receive an invitation. |

### graph
| Method | Path | Description |
|--------|------|-------------|
| POST | /graph/datasources/get | Gets data source package information for the behavior graph. |
| POST | /graph | Creates a new behavior graph for the calling account, and sets that account as the administrator account. This operation is called by the account that is enabling Detective. The operation also enables Detective for the calling account in the currently selected Region. It returns the ARN of the new behavior graph.  CreateGraph triggers a process to create the corresponding data tables for the new behavior graph. An account can only be the administrator account for one behavior graph within a Region. If the same account calls CreateGraph with the same administrator account, it always returns the same behavior graph ARN. It does not create a new behavior graph. |
| POST | /graph/members | CreateMembers is used to send invitations to accounts. For the organization behavior graph, the Detective administrator account uses CreateMembers to enable organization accounts as member accounts. For invited accounts, CreateMembers sends a request to invite the specified Amazon Web Services accounts to be member accounts in the behavior graph. This operation can only be called by the administrator account for a behavior graph.   CreateMembers verifies the accounts and then invites the verified accounts. The administrator can optionally specify to not send invitation emails to the member accounts. This would be used when the administrator manages their member accounts centrally. For organization accounts in the organization behavior graph, CreateMembers attempts to enable the accounts. The organization accounts do not receive invitations. The request provides the behavior graph ARN and the list of accounts to invite or to enable. The response separates the requested accounts into two lists:   The accounts that CreateMembers was able to process. For invited accounts, includes member accounts that are being verified, that have passed verification and are to be invited, and that have failed verification. For organization accounts in the organization behavior graph, includes accounts that can be enabled and that cannot be enabled.   The accounts that CreateMembers was unable to process. This list includes accounts that were already invited to be member accounts in the behavior graph. |
| POST | /graph/removal | Disables the specified behavior graph and queues it to be deleted. This operation removes the behavior graph from each member account's list of behavior graphs.  DeleteGraph can only be called by the administrator account for a behavior graph. |
| POST | /graph/members/removal | Removes the specified member accounts from the behavior graph. The removed accounts no longer contribute data to the behavior graph. This operation can only be called by the administrator account for the behavior graph. For invited accounts, the removed accounts are deleted from the list of accounts in the behavior graph. To restore the account, the administrator account must send another invitation. For organization accounts in the organization behavior graph, the Detective administrator account can always enable the organization account again. Organization accounts that are not enabled as member accounts are not included in the ListMembers results for the organization behavior graph. An administrator account cannot use DeleteMembers to remove their own account from the behavior graph. To disable a behavior graph, the administrator account uses the DeleteGraph API method. |
| POST | /graph/members/get | Returns the membership details for specified member accounts for a behavior graph. |
| POST | /graph/datasources/list | Lists data source packages in the behavior graph. |
| POST | /graph/members/list | Retrieves the list of member accounts for a behavior graph. For invited accounts, the results do not include member accounts that were removed from the behavior graph. For the organization behavior graph, the results do not include organization accounts that the Detective administrator account has not enabled as member accounts. |
| POST | /graph/member/monitoringstate | Sends a request to enable data ingest for a member account that has a status of ACCEPTED_BUT_DISABLED. For valid member accounts, the status is updated as follows.   If Detective enabled the member account, then the new status is ENABLED.   If Detective cannot enable the member account, the status remains ACCEPTED_BUT_DISABLED. |
| POST | /graph/datasources/update | Starts a data source packages for the behavior graph. |

### membership
| Method | Path | Description |
|--------|------|-------------|
| POST | /membership/datasources/get | Gets information on the data source package history for an account. |
| POST | /membership/removal | Removes the member account from the specified behavior graph. This operation can only be called by an invited member account that has the ENABLED status.  DisassociateMembership cannot be called by an organization account in the organization behavior graph. For the organization behavior graph, the Detective administrator account determines which organization accounts to enable or disable as member accounts. |

### orgs
| Method | Path | Description |
|--------|------|-------------|
| POST | /orgs/describeOrganizationConfiguration | Returns information about the configuration for the organization behavior graph. Currently indicates whether to automatically enable new organization accounts as member accounts. Can only be called by the Detective administrator account for the organization. |
| POST | /orgs/disableAdminAccount | Removes the Detective administrator account in the current Region. Deletes the organization behavior graph. Can only be called by the organization management account. Removing the Detective administrator account does not affect the delegated administrator account for Detective in Organizations. To remove the delegated administrator account in Organizations, use the Organizations API. Removing the delegated administrator account also removes the Detective administrator account in all Regions, except for Regions where the Detective administrator account is the organization management account. |
| POST | /orgs/enableAdminAccount | Designates the Detective administrator account for the organization in the current Region. If the account does not have Detective enabled, then enables Detective for that account and creates a new behavior graph. Can only be called by the organization management account. If the organization has a delegated administrator account in Organizations, then the Detective administrator account must be either the delegated administrator account or the organization management account. If the organization does not have a delegated administrator account in Organizations, then you can choose any account in the organization. If you choose an account other than the organization management account, Detective calls Organizations to make that account the delegated administrator account for Detective. The organization management account cannot be the delegated administrator account. |
| POST | /orgs/adminAccountslist | Returns information about the Detective administrator account for an organization. Can only be called by the organization management account. |
| POST | /orgs/updateOrganizationConfiguration | Updates the configuration for the Organizations integration in the current Region. Can only be called by the Detective administrator account for the organization. |

### investigations
| Method | Path | Description |
|--------|------|-------------|
| POST | /investigations/getInvestigation | Detective investigations lets you investigate IAM users and IAM roles using indicators of compromise. An indicator of compromise (IOC) is an artifact observed in or on a network, system, or environment that can (with a high level of confidence) identify malicious activity or a security incident. GetInvestigation returns the investigation results of an investigation for a behavior graph. |
| POST | /investigations/listIndicators | Gets the indicators from an investigation. You can use the information from the indicators to determine if an IAM user and/or IAM role is involved in an unusual activity that could indicate malicious behavior and its impact. |
| POST | /investigations/listInvestigations | Detective investigations lets you investigate IAM users and IAM roles using indicators of compromise. An indicator of compromise (IOC) is an artifact observed in or on a network, system, or environment that can (with a high level of confidence) identify malicious activity or a security incident. ListInvestigations lists all active Detective investigations. |
| POST | /investigations/startInvestigation | Detective investigations lets you investigate IAM users and IAM roles using indicators of compromise. An indicator of compromise (IOC) is an artifact observed in or on a network, system, or environment that can (with a high level of confidence) identify malicious activity or a security incident. StartInvestigation initiates an investigation on an entity in a behavior graph. |
| POST | /investigations/updateInvestigationState | Updates the state of an investigation. |

### graphs
| Method | Path | Description |
|--------|------|-------------|
| POST | /graphs/list | Returns the list of behavior graphs that the calling account is an administrator account of. This operation can only be called by an administrator account. Because an account can currently only be the administrator of one behavior graph within a Region, the results always contain a single behavior graph. |

### invitations
| Method | Path | Description |
|--------|------|-------------|
| POST | /invitations/list | Retrieves the list of open and accepted behavior graph invitations for the member account. This operation can only be called by an invited member account. Open invitations are invitations that the member account has not responded to. The results do not include behavior graphs for which the member account declined the invitation. The results also do not include behavior graphs that the member account resigned from or was removed from. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{ResourceArn} | Returns the tag values that are assigned to a behavior graph. |
| POST | /tags/{ResourceArn} | Applies tag values to a behavior graph. |
| DELETE | /tags/{ResourceArn} | Removes tags from a behavior graph. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a get?" -> POST /graph/datasources/get
- "Create a get?" -> POST /membership/datasources/get
- "Create a graph?" -> POST /graph
- "Create a member?" -> POST /graph/members
- "Create a removal?" -> POST /graph/removal
- "Create a removal?" -> POST /graph/members/removal
- "Create a describeOrganizationConfiguration?" -> POST /orgs/describeOrganizationConfiguration
- "Create a disableAdminAccount?" -> POST /orgs/disableAdminAccount
- "Create a removal?" -> POST /membership/removal
- "Create a enableAdminAccount?" -> POST /orgs/enableAdminAccount
- "Create a getInvestigation?" -> POST /investigations/getInvestigation
- "Create a get?" -> POST /graph/members/get
- "Create a list?" -> POST /graph/datasources/list
- "Create a list?" -> POST /graphs/list
- "Create a listIndicator?" -> POST /investigations/listIndicators
- "Create a listInvestigation?" -> POST /investigations/listInvestigations
- "Create a list?" -> POST /invitations/list
- "Create a list?" -> POST /graph/members/list
- "Create a adminAccountslist?" -> POST /orgs/adminAccountslist
- "Get tag details?" -> GET /tags/{ResourceArn}
- "Create a removal?" -> POST /invitation/removal
- "Create a startInvestigation?" -> POST /investigations/startInvestigation
- "Create a monitoringstate?" -> POST /graph/member/monitoringstate
- "Delete a tag?" -> DELETE /tags/{ResourceArn}
- "Create a update?" -> POST /graph/datasources/update
- "Create a updateInvestigationState?" -> POST /investigations/updateInvestigationState
- "Create a updateOrganizationConfiguration?" -> POST /orgs/updateOrganizationConfiguration
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
