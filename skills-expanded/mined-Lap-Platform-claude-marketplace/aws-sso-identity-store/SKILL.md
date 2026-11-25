---
name: aws-sso-identity-store
description: "AWS SSO Identity Store API skill. Use when working with AWS SSO Identity Store for root. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS SSO Identity Store
API version: 2020-06-15

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

19 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates a group within the specified identity store. |
| POST | / | Creates a relationship between a member and a group. The following identifiers must be specified: GroupId, IdentityStoreId, and MemberId. |
| POST | / | Creates a user within the specified identity store. |
| POST | / | Delete a group within an identity store given GroupId. |
| POST | / | Delete a membership within a group given MembershipId. |
| POST | / | Deletes a user within an identity store given UserId. |
| POST | / | Retrieves the group metadata and attributes from GroupId in an identity store.  If you have administrator access to a member account, you can use this API from the member account. Read about member accounts in the Organizations User Guide. |
| POST | / | Retrieves membership metadata and attributes from MembershipId in an identity store.  If you have administrator access to a member account, you can use this API from the member account. Read about member accounts in the Organizations User Guide. |
| POST | / | Retrieves the user metadata and attributes from the UserId in an identity store.  If you have administrator access to a member account, you can use this API from the member account. Read about member accounts in the Organizations User Guide. |
| POST | / | Retrieves GroupId in an identity store.  If you have administrator access to a member account, you can use this API from the member account. Read about member accounts in the Organizations User Guide. |
| POST | / | Retrieves the MembershipId in an identity store.  If you have administrator access to a member account, you can use this API from the member account. Read about member accounts in the Organizations User Guide. |
| POST | / | Retrieves the UserId in an identity store.  If you have administrator access to a member account, you can use this API from the member account. Read about member accounts in the Organizations User Guide. |
| POST | / | Checks the user's membership in all requested groups and returns if the member exists in all queried groups.  If you have administrator access to a member account, you can use this API from the member account. Read about member accounts in the Organizations User Guide. |
| POST | / | For the specified group in the specified identity store, returns the list of all GroupMembership objects and returns results in paginated form.  If you have administrator access to a member account, you can use this API from the member account. Read about member accounts in the Organizations User Guide. |
| POST | / | For the specified member in the specified identity store, returns the list of all GroupMembership objects and returns results in paginated form.  If you have administrator access to a member account, you can use this API from the member account. Read about member accounts in the Organizations User Guide. |
| POST | / | Lists all groups in the identity store. Returns a paginated list of complete Group objects. Filtering for a Group by the DisplayName attribute is deprecated. Instead, use the GetGroupId API action.  If you have administrator access to a member account, you can use this API from the member account. Read about member accounts in the Organizations User Guide. |
| POST | / | Lists all users in the identity store. Returns a paginated list of complete User objects. Filtering for a User by the UserName attribute is deprecated. Instead, use the GetUserId API action.  If you have administrator access to a member account, you can use this API from the member account. Read about member accounts in the Organizations User Guide. |
| POST | / | For the specified group in the specified identity store, updates the group metadata and attributes. |
| POST | / | For the specified user in the specified identity store, updates the user metadata and attributes. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
