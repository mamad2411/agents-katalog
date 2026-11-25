---
name: authentication-and-identity-management
description: "Authentication and Identity Management API skill. Use when working with Authentication and Identity Management for resources. Covers 305 endpoints."
version: 1.0.0
generator: lapsh
---

# Authentication and Identity Management

## Auth
Bearer bearer

## Base URL
https://api.frontegg.com/identity

## Setup
1. Set Authorization header with your Bearer token
2. GET /resources/tenants/access-tokens/v1 -- verify access
3. POST /resources/auth/v2/api-token -- create first api-token

## Endpoints

305 endpoints across 1 groups. See references/api-spec.lap for full details.

### resources
| Method | Path | Description |
|--------|------|-------------|
| POST | /resources/auth/v2/api-token | Authenticate using API token |
| POST | /resources/auth/v2/api-token/token/refresh | Refresh API token |
| POST | /resources/tenants/access-tokens/v1 | Create account (tenant) access token |
| GET | /resources/tenants/access-tokens/v1 | Get account (tenant) access tokens |
| DELETE | /resources/tenants/access-tokens/v1/{id} | Delete account (tenant) access token |
| POST | /resources/tenants/api-tokens/v1 | Create client credentials token |
| GET | /resources/tenants/api-tokens/v1 | Get client credentials tokens |
| DELETE | /resources/tenants/api-tokens/v1/{id} | Delete client credentials token |
| PATCH | /resources/tenants/api-tokens/v1/{id} | Update client credentials token |
| POST | /resources/tenants/api-tokens/v2 | Create client credentials token |
| GET | /resources/tenants/invites/v1/user | Get account (tenant) invite of user |
| POST | /resources/tenants/invites/v1/user | Create account (tenant) invite for user |
| DELETE | /resources/tenants/invites/v1/user | Delete account (tenant) invite of user |
| PATCH | /resources/tenants/invites/v1/user | Update account (tenant) invite of user |
| POST | /resources/tenants/invites/v1/verify | Verify account (tenant) invite |
| GET | /resources/tenants/invites/v1/configuration | Get account (tenant) invite configuration |
| POST | /resources/tenants/invites/v2/user | Create tenant invite with roles for user |
| POST | /resources/tenants/invites/v1 | Create account (tenant) invite |
| GET | /resources/tenants/invites/v1/all | Get all account (tenant) invites |
| DELETE | /resources/tenants/invites/v1/token/{id} | Delete an account (tenant) invite |
| GET | /resources/configurations/v1/activation/strategies | Get activation strategies |
| POST | /resources/configurations/v1/activation/strategies | Create or update activation strategy |
| GET | /resources/configurations/v1/invitation/strategies | Get invitation strategies |
| POST | /resources/configurations/v1/invitation/strategies | Create or update invitation strategy |
| GET | /resources/roles/v2 | Get roles v2 |
| POST | /resources/roles/v2 | Create a new role |
| GET | /resources/roles/v2/distinct-levels | Get distinct levels of roles |
| GET | /resources/roles/v2/distinct-tenants | Get distinct assigned accounts (tenants) of roles |
| POST | /resources/approval-flows/v1 | Create approval flow |
| GET | /resources/approval-flows/v1 | Get approval flows |
| GET | /resources/approval-flows/v1/{id} | Get approval flow by ID |
| PATCH | /resources/approval-flows/v1/{id} | Update approval flow |
| DELETE | /resources/approval-flows/v1/{id} | Delete approval flow |
| POST | /resources/approval-flows/v1/approver-action | Approver action |
| GET | /resources/approval-flows/v1/execution-data | Get approval flow execution data |
| POST | /resources/approval-flows/v1/{id}/execute | Execute approval flow |
| POST | /resources/approval-flows/v1/step-up/execute | Execute step up approval flow |
| POST | /resources/configurations/v1 | Update identity management configuration |
| GET | /resources/configurations/v1 | Get identity management configuration |
| POST | /resources/configurations/v1/captcha-policy | Create captcha policy |
| PUT | /resources/configurations/v1/captcha-policy | Update captcha policy |
| GET | /resources/configurations/v1/captcha-policy | Get captcha policy |
| GET | /resources/configurations/v1/jwt-template-targeting | Get JWT template targeting configuration |
| POST | /resources/configurations/v1/jwt-template-targeting | Create JWT template targeting configuration |
| PUT | /resources/configurations/v1/jwt-template-targeting | Update or create JWT template targeting configuration |
| PATCH | /resources/configurations/v1/jwt-template-targeting/{id} | Update JWT template targeting configuration by ID |
| DELETE | /resources/configurations/v1/jwt-template-targeting/{id} | Delete JWT template targeting configuration by ID |
| POST | /resources/jwt-templates/v1 | Create JWT template |
| GET | /resources/jwt-templates/v1 | Get all JWT templates |
| GET | /resources/jwt-templates/v1/{id} | Get JWT template by ID |
| PUT | /resources/jwt-templates/v1/{id} | Update JWT template |
| DELETE | /resources/jwt-templates/v1/{id} | Delete JWT template |
| GET | /resources/configurations/v1/basic | Get identity management configuration |
| POST | /resources/sso/custom/v1 | Create custom oauth provider |
| GET | /resources/sso/custom/v1 | Get custom oauth provider |
| PATCH | /resources/sso/custom/v1/{id} | Update custom oauth provider |
| DELETE | /resources/sso/custom/v1/{id} | Delete custom oauth provider |
| POST | /resources/migrations/v1/auth0 | Migrate from Auth0 |
| POST | /resources/migrations/v1/local | Migrate a single user |
| POST | /resources/migrations/v1/local/bulk | Migrate users in bulk |
| GET | /resources/migrations/v1/local/bulk/status/{migrationId} | Check status of bulk migration |
| POST | /resources/migrations/v2/local/bulk | Migrate vendor users in bulk |
| GET | /resources/configurations/v1/delegation | Get delegation configuration |
| POST | /resources/configurations/v1/delegation | Create or update delegation configuration |
| POST | /resources/configurations/restrictions/v1/email-domain | Create domain restriction |
| GET | /resources/configurations/restrictions/v1/email-domain | Get domain restrictions |
| GET | /resources/configurations/restrictions/v1/email-domain/config | Get domain restrictions |
| POST | /resources/configurations/restrictions/v1/email-domain/config | Change domain restrictions config list type and toggle it off/on |
| DELETE | /resources/configurations/restrictions/v1/email-domain/{id} | Delete domain restriction |
| POST | /resources/configurations/restrictions/v1/email-domain/replace-bulk | Replace bulk domain restriction |
| POST | /resources/mail/v1/configurations | Create or update configuration |
| GET | /resources/mail/v1/configurations | Get configuration |
| DELETE | /resources/mail/v1/configurations | Delete configuration |
| POST | /resources/mail/v2/configurations | Create or update configuration v2 |
| POST | /resources/mail/v1/configs/templates | Add or update template |
| GET | /resources/mail/v1/configs/templates | Get template |
| DELETE | /resources/mail/v1/configs/templates/{templateId} | Delete template |
| GET | /resources/mail/v1/configs/{type}/default | Get default template by type |
| POST | /resources/auth/v1/user | Authenticate user with password |
| POST | /resources/auth/v1/user/token/refresh | Refresh user JWT token |
| POST | /resources/auth/v1/logout | Logout user |
| POST | /resources/users/v1/signUp | Signup user |
| POST | /resources/users/v1/signUp/username | Signup user with username |
| POST | /resources/configurations/v1/restrictions/ip/config | Create or update IP restriction configuration (ALLOW/BLOCK) |
| GET | /resources/configurations/v1/restrictions/ip/config | Get IP restriction configuration (ALLOW/BLOCK) |
| GET | /resources/configurations/v1/restrictions/ip | Get all IP restrictions |
| POST | /resources/configurations/v1/restrictions/ip | Create IP restriction |
| POST | /resources/configurations/v1/restrictions/ip/verify | Test Current IP |
| POST | /resources/configurations/v1/restrictions/ip/verify/allow | Test current IP is in allow list |
| DELETE | /resources/configurations/v1/restrictions/ip/{id} | Delete IP restriction by IP |
| POST | /resources/configurations/v1/lockout-policy | Create lockout policy |
| PATCH | /resources/configurations/v1/lockout-policy | Update lockout policy |
| GET | /resources/configurations/v1/lockout-policy | Get lockout policy |
| GET | /resources/vendor-only/users/access-tokens/v1/active | Get active access tokens list |
| GET | /resources/vendor-only/users/access-tokens/v1/{id} | Get user access token data |
| GET | /resources/vendor-only/tenants/access-tokens/v1/{id} | Get account (tenant) access token data |
| POST | /resources/auth/v1/user/mfa/recover | Recover MFA |
| POST | /resources/users/v1/mfa/disable | Disable authenticator app MFA |
| POST | /resources/users/v1/mfa/authenticator/{deviceId}/disable/verify | Disable authenticator app MFA |
| POST | /resources/users/v1/mfa/sms/{deviceId}/disable | Pre-disable SMS MFA |
| POST | /resources/users/v1/mfa/sms/{deviceId}/disable/verify | Disable SMS MFA |
| POST | /resources/auth/v1/user/mfa/verify | Verify MFA using code from authenticator app |
| POST | /resources/auth/v1/user/mfa/emailcode | Request verify MFA using email code |
| POST | /resources/auth/v1/user/mfa/emailcode/verify | Verify MFA using email code |
| POST | /resources/auth/v1/user/mfa/authenticator/enroll | Pre enroll MFA using Authenticator App |
| POST | /resources/auth/v1/user/mfa/authenticator/enroll/verify | Enroll MFA using Authenticator App |
| POST | /resources/auth/v1/user/mfa/authenticator/{deviceId}/verify | Verify MFA using authenticator app |
| POST | /resources/auth/v1/user/mfa/sms/enroll | Pre-enroll MFA using sms |
| POST | /resources/auth/v1/user/mfa/sms/enroll/verify | Enroll MFA using sms |
| POST | /resources/auth/v1/user/mfa/sms/{deviceId} | Request to verify MFA using sms |
| POST | /resources/auth/v1/user/mfa/sms/{deviceId}/verify | Verify MFA using sms |
| POST | /resources/auth/v1/user/mfa/webauthn/enroll | Pre enroll MFA using WebAuthN |
| POST | /resources/auth/v1/user/mfa/webauthn/enroll/verify | Enroll MFA using WebAuthN |
| POST | /resources/auth/v1/user/mfa/webauthn/{deviceId} | Request verify MFA using WebAuthN |
| POST | /resources/auth/v1/user/mfa/webauthn/{deviceId}/verify | Verify MFA using webauthn |
| GET | /resources/configurations/v1/mfa-policy/allow-remember-device | Check if remember device allowed |
| POST | /resources/users/v1/mfa/enroll | Enroll authenticator app MFA |
| POST | /resources/users/v1/mfa/authenticator/enroll | Enroll authenticator app MFA |
| POST | /resources/users/v1/mfa/enroll/verify | Verify authenticator app MFA enrollment |
| POST | /resources/users/v1/mfa/authenticator/enroll/verify | Verify authenticator app MFA enrollment |
| POST | /resources/users/v1/mfa/sms/enroll | Enroll SMS MFA |
| POST | /resources/users/v1/mfa/sms/enroll/verify | Verify MFA enrollment |
| POST | /resources/configurations/v1/mfa | Update MFA configuration |
| GET | /resources/configurations/v1/mfa | Get MFA configuration |
| POST | /resources/configurations/v1/mfa-policy | Create MFA policy |
| PATCH | /resources/configurations/v1/mfa-policy | Update security policy |
| PUT | /resources/configurations/v1/mfa-policy | Upsert security policy |
| GET | /resources/configurations/v1/mfa-policy | Get security policy |
| GET | /resources/configurations/v1/mfa/strategies | Get MFA strategies |
| POST | /resources/configurations/v1/mfa/strategies | Create or update MFA strategy |
| POST | /resources/configurations/v1/password | Create or update password configuration |
| GET | /resources/configurations/v1/password | Get password policy configuration |
| POST | /resources/configurations/v1/password-history-policy | Create password history policy |
| PATCH | /resources/configurations/v1/password-history-policy | Update password history policy |
| GET | /resources/configurations/v1/password-history-policy | Get password history policy |
| POST | /resources/users/v1/passwords/reset | Reset password |
| POST | /resources/users/v1/passwords/reset/verify | Verify password |
| POST | /resources/users/v1/passwords/change | Change password |
| GET | /resources/users/v1/passwords/config | Get strictest password configuration |
| POST | /resources/users/v2/passwords/reset/email | Reset password via email |
| POST | /resources/users/v2/passwords/reset/sms | Reset password via SMS |
| POST | /resources/users/v2/passwords/reset/sms/verify | Verify password reset code sent via SMS |
| GET | /resources/configurations/v1/password-rotation | Get password expiration period configuration |
| POST | /resources/configurations/v1/password-rotation | Manage password expiration |
| GET | /resources/configurations/v1/password-rotation/vendor | Get environment configuration for password expiration period. |
| POST | /resources/auth/v1/passwordless/smscode/prelogin | SMS code prelogin |
| POST | /resources/auth/v1/passwordless/smscode/postlogin | SMS code postlogin |
| POST | /resources/auth/v1/passwordless/magiclink/prelogin | Magic link prelogin |
| POST | /resources/auth/v1/passwordless/magiclink/postlogin | Magic link postlogin |
| POST | /resources/auth/v1/passwordless/code/prelogin | OTC (One-Time Code) prelogin |
| POST | /resources/auth/v1/passwordless/code/postlogin | OTC (One-Time Code) postlogin |
| GET | /resources/permissions/v1 | Get permissions |
| POST | /resources/permissions/v1 | Create permissions |
| DELETE | /resources/permissions/v1/{permissionId} | Delete permission |
| PATCH | /resources/permissions/v1/{permissionId} | Update permission |
| PUT | /resources/permissions/v1/{permissionId}/roles | Set a permission to multiple roles |
| PUT | /resources/permissions/v1/classification | Set permissions classification |
| GET | /resources/permissions/v1/categories | Get permissions categories |
| POST | /resources/permissions/v1/categories | Create category |
| PATCH | /resources/permissions/v1/categories/{categoryId} | Update category |
| DELETE | /resources/permissions/v1/categories/{categoryId} | Delete category |
| POST | /resources/users/access-tokens/v1 | Create user access token |
| GET | /resources/users/access-tokens/v1 | Get user access tokens |
| DELETE | /resources/users/access-tokens/v1/{id} | Delete user access token by token ID |
| POST | /resources/users/api-tokens/v1 | Create user client credentials token |
| GET | /resources/users/api-tokens/v1 | Get user client credentials tokens |
| DELETE | /resources/users/api-tokens/v1/{id} | Delete user client credentials token by token ID |
| GET | /resources/roles/v1 | Get roles |
| POST | /resources/roles/v1 | Create roles |
| DELETE | /resources/roles/v1/{roleId} | Delete role |
| PATCH | /resources/roles/v1/{roleId} | Update role |
| PUT | /resources/roles/v1/{roleId}/permissions | Assign permissions to a role |
| PUT | /resources/roles/v1/{roleId}/tenant | Update role tenant |
| GET | /resources/users/phone-numbers/v1 | Get all phone numbers |
| POST | /resources/users/phone-numbers/v1 | Set phone number for a user |
| POST | /resources/users/phone-numbers/v1/preverify | Pre-verify user's phone number |
| POST | /resources/users/phone-numbers/v1/verify | Verify creation of phone number for user |
| DELETE | /resources/users/phone-numbers/v1/{id} | Delete user's phone number |
| POST | /resources/users/phone-numbers/v1/{id}/delete/verify | Verify delete user's phone number |
| GET | /resources/users/phone-numbers/v1/me | Get current user's phone numbers |
| GET | /resources/users/phone-numbers/v2 | Get all phone numbers v2 |
| POST | /resources/configurations/v1/sms | Creates or updates a vendor SMS config |
| DELETE | /resources/configurations/v1/sms | Deletes a vendor SMS config |
| GET | /resources/configurations/v1/sms | Gets a vendor SMS config |
| GET | /resources/configurations/v1/sms/templates | Gets vendor SMS templates |
| GET | /resources/configurations/v1/sms/templates/{type} | Gets vendor SMS template by type |
| DELETE | /resources/configurations/v1/sms/templates/{type} | Deletes vendor SMS template by type |
| POST | /resources/configurations/v1/sms/templates/{type} | Create or update a vendor SMS template |
| GET | /resources/configurations/v1/sms/templates/{type}/default | Gets vendor default SMS template by type |
| GET | /resources/configurations/v1/sms/templates/default/all | Gets all vendor default SMS templates |
| GET | /resources/configurations/sessions/v1/vendor | Get environment session configuration |
| GET | /resources/configurations/sessions/v1 | Get account (tenant) or vendor default session configuration |
| POST | /resources/configurations/sessions/v1 | Create or update account (tenant) or vendor default session configuration |
| GET | /resources/configurations/v1/user-emails-policy | Get user emails policy |
| POST | /resources/configurations/v1/user-emails-policy | Create or update user emails policy |
| GET | /resources/groups/v1 | Get all groups |
| POST | /resources/groups/v1 | Create group |
| POST | /resources/groups/v1/bulkGet | Get groups by Ids |
| PATCH | /resources/groups/v1/{id} | Update group |
| DELETE | /resources/groups/v1/{id} | Delete group |
| GET | /resources/groups/v1/{id} | Get group by ID |
| GET | /resources/groups/v1/config | Get groups configuration |
| POST | /resources/groups/v1/config | Create or update groups configuration |
| POST | /resources/groups/v1/{groupId}/roles | Add roles to group |
| DELETE | /resources/groups/v1/{groupId}/roles | Remove roles from group |
| POST | /resources/groups/v1/{groupId}/users | Add users to group |
| DELETE | /resources/groups/v1/{groupId}/users | Remove users from group |
| GET | /resources/groups/v2 | Get all groups paginated |
| POST | /resources/tenants/users/v1/{userId}/disable | Disable user account (tenant) |
| POST | /resources/tenants/users/v1/{userId}/enable | Enable user account (tenant) |
| PUT | /resources/users/temporary/v1/{userId} | Sets a permanent user to temporary |
| DELETE | /resources/users/temporary/v1/{userId} | Sets a temporary user to permanent |
| GET | /resources/users/temporary/v1/configuration | Gets temporary users configuration |
| PUT | /resources/users/temporary/v1/configuration | Set temporary users configuration |
| GET | /resources/users/emails/v1 | Get all user emails |
| POST | /resources/users/emails/v1 | Create a user email |
| POST | /resources/users/emails/v1/verify | Verify user email |
| DELETE | /resources/users/emails/v1/{emailId} | Delete a user email |
| POST | /resources/users/emails/v1/vendor/{userId} | Create a user email for vendor |
| DELETE | /resources/users/emails/v1/vendor/{userId}/{emailId} | Delete a user email for vendor |
| POST | /resources/users/emails/v1/vendor/{userId}/primary | Mark email as primary for vendor |
| POST | /resources/users/emails/v1/me/primary | Mark email as primary |
| GET | /resources/users/emails/v1/me | Get current user`s emails |
| PUT | /resources/sub-tenants/users/v1/{userId}/access | Set sub-account access for a user |
| POST | /resources/users/v1/activate/reset | Reset user activation token |
| POST | /resources/users/v1/invitation/reset | Reset invitation |
| POST | /resources/users/v1/invitation/reset/all | Reset all invitation tokens |
| GET | /resources/users/v3 | Get users |
| GET | /resources/users/v3/roles | Get users roles |
| GET | /resources/users/v3/groups | Get users groups |
| POST | /resources/users/v3/me/unlock | Unlock user |
| POST | /resources/users/v2 | Invite user |
| PUT | /resources/users/v2/me | Update user profile |
| GET | /resources/users/v2/me | Get user profile |
| POST | /resources/users/v1 | Create user |
| PUT | /resources/users/v1 | Update user |
| DELETE | /resources/users/v1/{userId} | Remove user |
| PUT | /resources/users/v1/{userId} | Update user (global) |
| POST | /resources/users/v1/{userId}/roles | Assign roles to user |
| DELETE | /resources/users/v1/{userId}/roles | Unassign roles from user |
| PUT | /resources/users/v1/tenant | Update user's active account (tenant) |
| GET | /resources/users/v1/query/phrase | Get users with fuzzy search |
| GET | /resources/usernames/v1 | Get usernames for users |
| POST | /resources/usernames/v1 | Create a username for user |
| DELETE | /resources/usernames/v1/{username} | Delete a username for user |
| GET | /resources/usernames/v1/me | Get authenticated user's username |
| POST | /resources/users/v1/email/me | Update user email |
| POST | /resources/users/v1/email/me/verify | Verify user email |
| POST | /resources/users/v1/activate | Activate user |
| POST | /resources/users/v1/activate/code | Activate user with code |
| GET | /resources/users/v1/activate/strategy | Get user activation strategy |
| POST | /resources/users/v1/invitation/accept | Accept invitation |
| POST | /resources/users/v1/invitation/accept/code | Accept invitation with code |
| GET | /resources/users/v3/me | Get user profile |
| GET | /resources/users/v2/me/tenants | Get user accounts (tenants) |
| GET | /resources/users/v2/me/hierarchy | Get user accounts (tenants) hierarchy |
| GET | /resources/users/v1/me/authorization | Get user permissions and roles |
| GET | /resources/users/v1/me/tenants | Get user accounts (tenants) |
| GET | /resources/user-sources/v1 | Get vendor user sources |
| GET | /resources/user-sources/v1/{id} | Get vendor user source |
| DELETE | /resources/user-sources/v1/{id} | Delete user source |
| POST | /resources/user-sources/v1/external/auth0 | Create Auth0 external user source |
| POST | /resources/user-sources/v1/external/cognito | Create Cognito external user source |
| POST | /resources/user-sources/v1/external/firebase | Create Firebase external user source |
| POST | /resources/user-sources/v1/external/custom-code | Create Custom-Code external user source |
| POST | /resources/user-sources/v1/federation | Create Federation user source |
| PUT | /resources/user-sources/v1/external/auth0/{id} | Update Auth0 external user source |
| PUT | /resources/user-sources/v1/external/cognito/{id} | Update Cognito external user source |
| PUT | /resources/user-sources/v1/external/firebase/{id} | Update Firebase external user source |
| PUT | /resources/user-sources/v1/external/custom-code/{id} | Update Custom-Code external user source |
| PUT | /resources/user-sources/v1/federation/{id} | Update Federation user source |
| POST | /resources/user-sources/v1/assign | Assign applications to a user source |
| POST | /resources/user-sources/v1/unassign | Unassign applications from a user source |
| GET | /resources/user-sources/v1/{id}/users | Get user source users |
| GET | /resources/users/sessions/v1/me | Get user's active sessions |
| DELETE | /resources/users/sessions/v1/me/all | Delete all user sessions |
| DELETE | /resources/users/sessions/v1/me/{id} | Delete single user's session |
| GET | /resources/vendor-only/users/v1/{userId} | Get user |
| POST | /resources/vendor-only/users/v1/{userId}/mfa/unenroll | Unenroll user from MFA globally |
| POST | /resources/vendor-only/users/v1/passwords/verify | Verify user's password |
| POST | /resources/vendor-only/users/v1 | Create user |
| GET | /resources/tenants/users/v1/statuses | Get users account (tenant) statuses |
| POST | /resources/users/phone-numbers/v1/vendor/{userId} | Create user phone number verified by default |
| DELETE | /resources/users/phone-numbers/v1/vendor/{userId}/{phoneId} | Delete user phone number on an environment |
| POST | /resources/users/bulk/v1/invite | Invite users to an account (tenant) in bulk |
| GET | /resources/users/bulk/v1/status/{id} | Get status of bulk invite task |
| GET | /resources/users/v1/email | Get user by email |
| GET | /resources/users/v1/{id} | Get user by ID |
| POST | /resources/users/v1/{userId}/verify | Verify user |
| PUT | /resources/users/v1/{userId}/invisible | Make user invisible |
| PUT | /resources/users/v1/{userId}/superuser | Make user super-user |
| PUT | /resources/users/v1/{userId}/tenant | Set user's account (tenant) |
| POST | /resources/users/v1/{userId}/tenant | Add user to account (tenant) |
| PUT | /resources/users/v1/{userId}/email | Update user email |
| POST | /resources/users/v1/{userId}/links/generate-activation-token | Generate activation token |
| POST | /resources/users/v1/{userId}/links/generate-password-reset-token | Generate password reset token |
| POST | /resources/users/v1/{userId}/unlock | Unlock user |
| POST | /resources/users/v1/{userId}/lock | Lock user |
| PUT | /resources/users/v1/tenants/migrate | Move all users from one account (tenant) to another |
| GET | /resources/applications/v1/{appId}/users | Get users for application |
| GET | /resources/applications/v1/{userId}/apps | Get applications for user |
| POST | /resources/applications/v1 | Assign users to application |
| DELETE | /resources/applications/v1 | Unassign users from application |
| GET | /resources/applications/user-tenants/active/v1 | Get user active accounts (tenants) in applications |
| PUT | /resources/applications/user-tenants/active/v1 | Switch users active account (tenant) in applications |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a api-token?" -> POST /resources/auth/v2/api-token
- "Create a refresh?" -> POST /resources/auth/v2/api-token/token/refresh
- "Create a access-token?" -> POST /resources/tenants/access-tokens/v1
- "List all access-tokens?" -> GET /resources/tenants/access-tokens/v1
- "Delete a access-token?" -> DELETE /resources/tenants/access-tokens/v1/{id}
- "Create a api-token?" -> POST /resources/tenants/api-tokens/v1
- "List all api-tokens?" -> GET /resources/tenants/api-tokens/v1
- "Delete a api-token?" -> DELETE /resources/tenants/api-tokens/v1/{id}
- "Partially update a api-token?" -> PATCH /resources/tenants/api-tokens/v1/{id}
- "Create a api-token?" -> POST /resources/tenants/api-tokens/v2
- "List all user?" -> GET /resources/tenants/invites/v1/user
- "Create a user?" -> POST /resources/tenants/invites/v1/user
- "Create a verify?" -> POST /resources/tenants/invites/v1/verify
- "List all configuration?" -> GET /resources/tenants/invites/v1/configuration
- "Create a user?" -> POST /resources/tenants/invites/v2/user
- "Create a invite?" -> POST /resources/tenants/invites/v1
- "List all all?" -> GET /resources/tenants/invites/v1/all
- "Delete a token?" -> DELETE /resources/tenants/invites/v1/token/{id}
- "List all strategies?" -> GET /resources/configurations/v1/activation/strategies
- "Create a strategy?" -> POST /resources/configurations/v1/activation/strategies
- "List all strategies?" -> GET /resources/configurations/v1/invitation/strategies
- "Create a strategy?" -> POST /resources/configurations/v1/invitation/strategies
- "List all roles?" -> GET /resources/roles/v2
- "Create a role?" -> POST /resources/roles/v2
- "List all distinct-levels?" -> GET /resources/roles/v2/distinct-levels
- "List all distinct-tenants?" -> GET /resources/roles/v2/distinct-tenants
- "Create a approval-flow?" -> POST /resources/approval-flows/v1
- "List all approval-flows?" -> GET /resources/approval-flows/v1
- "Get approval-flow details?" -> GET /resources/approval-flows/v1/{id}
- "Partially update a approval-flow?" -> PATCH /resources/approval-flows/v1/{id}
- "Delete a approval-flow?" -> DELETE /resources/approval-flows/v1/{id}
- "Create a approver-action?" -> POST /resources/approval-flows/v1/approver-action
- "List all execution-data?" -> GET /resources/approval-flows/v1/execution-data
- "Create a execute?" -> POST /resources/approval-flows/v1/{id}/execute
- "Create a execute?" -> POST /resources/approval-flows/v1/step-up/execute
- "Create a configuration?" -> POST /resources/configurations/v1
- "List all configurations?" -> GET /resources/configurations/v1
- "Create a captcha-policy?" -> POST /resources/configurations/v1/captcha-policy
- "List all captcha-policy?" -> GET /resources/configurations/v1/captcha-policy
- "List all jwt-template-targeting?" -> GET /resources/configurations/v1/jwt-template-targeting
- "Create a jwt-template-targeting?" -> POST /resources/configurations/v1/jwt-template-targeting
- "Partially update a jwt-template-targeting?" -> PATCH /resources/configurations/v1/jwt-template-targeting/{id}
- "Delete a jwt-template-targeting?" -> DELETE /resources/configurations/v1/jwt-template-targeting/{id}
- "Create a jwt-template?" -> POST /resources/jwt-templates/v1
- "List all jwt-templates?" -> GET /resources/jwt-templates/v1
- "Get jwt-template details?" -> GET /resources/jwt-templates/v1/{id}
- "Update a jwt-template?" -> PUT /resources/jwt-templates/v1/{id}
- "Delete a jwt-template?" -> DELETE /resources/jwt-templates/v1/{id}
- "List all basic?" -> GET /resources/configurations/v1/basic
- "Create a custom?" -> POST /resources/sso/custom/v1
- "List all custom?" -> GET /resources/sso/custom/v1
- "Partially update a custom?" -> PATCH /resources/sso/custom/v1/{id}
- "Delete a custom?" -> DELETE /resources/sso/custom/v1/{id}
- "Create a auth0?" -> POST /resources/migrations/v1/auth0
- "Create a local?" -> POST /resources/migrations/v1/local
- "Create a bulk?" -> POST /resources/migrations/v1/local/bulk
- "Get status details?" -> GET /resources/migrations/v1/local/bulk/status/{migrationId}
- "Create a bulk?" -> POST /resources/migrations/v2/local/bulk
- "List all delegation?" -> GET /resources/configurations/v1/delegation
- "Create a delegation?" -> POST /resources/configurations/v1/delegation
- "Create a email-domain?" -> POST /resources/configurations/restrictions/v1/email-domain
- "List all email-domain?" -> GET /resources/configurations/restrictions/v1/email-domain
- "List all config?" -> GET /resources/configurations/restrictions/v1/email-domain/config
- "Create a config?" -> POST /resources/configurations/restrictions/v1/email-domain/config
- "Delete a email-domain?" -> DELETE /resources/configurations/restrictions/v1/email-domain/{id}
- "Create a replace-bulk?" -> POST /resources/configurations/restrictions/v1/email-domain/replace-bulk
- "Create a configuration?" -> POST /resources/mail/v1/configurations
- "List all configurations?" -> GET /resources/mail/v1/configurations
- "Create a configuration?" -> POST /resources/mail/v2/configurations
- "Create a template?" -> POST /resources/mail/v1/configs/templates
- "List all templates?" -> GET /resources/mail/v1/configs/templates
- "Delete a template?" -> DELETE /resources/mail/v1/configs/templates/{templateId}
- "List all default?" -> GET /resources/mail/v1/configs/{type}/default
- "Create a user?" -> POST /resources/auth/v1/user
- "Create a refresh?" -> POST /resources/auth/v1/user/token/refresh
- "Create a logout?" -> POST /resources/auth/v1/logout
- "Create a signUp?" -> POST /resources/users/v1/signUp
- "Create a username?" -> POST /resources/users/v1/signUp/username
- "Create a config?" -> POST /resources/configurations/v1/restrictions/ip/config
- "List all config?" -> GET /resources/configurations/v1/restrictions/ip/config
- "List all ip?" -> GET /resources/configurations/v1/restrictions/ip
- "Create a ip?" -> POST /resources/configurations/v1/restrictions/ip
- "Create a verify?" -> POST /resources/configurations/v1/restrictions/ip/verify
- "Create a allow?" -> POST /resources/configurations/v1/restrictions/ip/verify/allow
- "Delete a ip?" -> DELETE /resources/configurations/v1/restrictions/ip/{id}
- "Create a lockout-policy?" -> POST /resources/configurations/v1/lockout-policy
- "List all lockout-policy?" -> GET /resources/configurations/v1/lockout-policy
- "List all active?" -> GET /resources/vendor-only/users/access-tokens/v1/active
- "Get access-token details?" -> GET /resources/vendor-only/users/access-tokens/v1/{id}
- "Get access-token details?" -> GET /resources/vendor-only/tenants/access-tokens/v1/{id}
- "Create a recover?" -> POST /resources/auth/v1/user/mfa/recover
- "Create a disable?" -> POST /resources/users/v1/mfa/disable
- "Create a verify?" -> POST /resources/users/v1/mfa/authenticator/{deviceId}/disable/verify
- "Create a disable?" -> POST /resources/users/v1/mfa/sms/{deviceId}/disable
- "Create a verify?" -> POST /resources/users/v1/mfa/sms/{deviceId}/disable/verify
- "Create a verify?" -> POST /resources/auth/v1/user/mfa/verify
- "Create a emailcode?" -> POST /resources/auth/v1/user/mfa/emailcode
- "Create a verify?" -> POST /resources/auth/v1/user/mfa/emailcode/verify
- "Create a enroll?" -> POST /resources/auth/v1/user/mfa/authenticator/enroll
- "Create a verify?" -> POST /resources/auth/v1/user/mfa/authenticator/enroll/verify
- "Create a verify?" -> POST /resources/auth/v1/user/mfa/authenticator/{deviceId}/verify
- "Create a enroll?" -> POST /resources/auth/v1/user/mfa/sms/enroll
- "Create a verify?" -> POST /resources/auth/v1/user/mfa/sms/enroll/verify
- "Create a verify?" -> POST /resources/auth/v1/user/mfa/sms/{deviceId}/verify
- "Create a enroll?" -> POST /resources/auth/v1/user/mfa/webauthn/enroll
- "Create a verify?" -> POST /resources/auth/v1/user/mfa/webauthn/enroll/verify
- "Create a verify?" -> POST /resources/auth/v1/user/mfa/webauthn/{deviceId}/verify
- "List all allow-remember-device?" -> GET /resources/configurations/v1/mfa-policy/allow-remember-device
- "Create a enroll?" -> POST /resources/users/v1/mfa/enroll
- "Create a enroll?" -> POST /resources/users/v1/mfa/authenticator/enroll
- "Create a verify?" -> POST /resources/users/v1/mfa/enroll/verify
- "Create a verify?" -> POST /resources/users/v1/mfa/authenticator/enroll/verify
- "Create a enroll?" -> POST /resources/users/v1/mfa/sms/enroll
- "Create a verify?" -> POST /resources/users/v1/mfa/sms/enroll/verify
- "Create a mfa?" -> POST /resources/configurations/v1/mfa
- "List all mfa?" -> GET /resources/configurations/v1/mfa
- "Create a mfa-policy?" -> POST /resources/configurations/v1/mfa-policy
- "List all mfa-policy?" -> GET /resources/configurations/v1/mfa-policy
- "List all strategies?" -> GET /resources/configurations/v1/mfa/strategies
- "Create a strategy?" -> POST /resources/configurations/v1/mfa/strategies
- "Create a password?" -> POST /resources/configurations/v1/password
- "List all password?" -> GET /resources/configurations/v1/password
- "Create a password-history-policy?" -> POST /resources/configurations/v1/password-history-policy
- "List all password-history-policy?" -> GET /resources/configurations/v1/password-history-policy
- "Create a reset?" -> POST /resources/users/v1/passwords/reset
- "Create a verify?" -> POST /resources/users/v1/passwords/reset/verify
- "Create a change?" -> POST /resources/users/v1/passwords/change
- "List all config?" -> GET /resources/users/v1/passwords/config
- "Create a email?" -> POST /resources/users/v2/passwords/reset/email
- "Create a sm?" -> POST /resources/users/v2/passwords/reset/sms
- "Create a verify?" -> POST /resources/users/v2/passwords/reset/sms/verify
- "List all password-rotation?" -> GET /resources/configurations/v1/password-rotation
- "Create a password-rotation?" -> POST /resources/configurations/v1/password-rotation
- "List all vendor?" -> GET /resources/configurations/v1/password-rotation/vendor
- "Create a prelogin?" -> POST /resources/auth/v1/passwordless/smscode/prelogin
- "Create a postlogin?" -> POST /resources/auth/v1/passwordless/smscode/postlogin
- "Create a prelogin?" -> POST /resources/auth/v1/passwordless/magiclink/prelogin
- "Create a postlogin?" -> POST /resources/auth/v1/passwordless/magiclink/postlogin
- "Create a prelogin?" -> POST /resources/auth/v1/passwordless/code/prelogin
- "Create a postlogin?" -> POST /resources/auth/v1/passwordless/code/postlogin
- "List all permissions?" -> GET /resources/permissions/v1
- "Create a permission?" -> POST /resources/permissions/v1
- "Delete a permission?" -> DELETE /resources/permissions/v1/{permissionId}
- "Partially update a permission?" -> PATCH /resources/permissions/v1/{permissionId}
- "List all categories?" -> GET /resources/permissions/v1/categories
- "Create a category?" -> POST /resources/permissions/v1/categories
- "Partially update a category?" -> PATCH /resources/permissions/v1/categories/{categoryId}
- "Delete a category?" -> DELETE /resources/permissions/v1/categories/{categoryId}
- "Create a access-token?" -> POST /resources/users/access-tokens/v1
- "List all access-tokens?" -> GET /resources/users/access-tokens/v1
- "Delete a access-token?" -> DELETE /resources/users/access-tokens/v1/{id}
- "Create a api-token?" -> POST /resources/users/api-tokens/v1
- "List all api-tokens?" -> GET /resources/users/api-tokens/v1
- "Delete a api-token?" -> DELETE /resources/users/api-tokens/v1/{id}
- "List all roles?" -> GET /resources/roles/v1
- "Create a role?" -> POST /resources/roles/v1
- "Delete a role?" -> DELETE /resources/roles/v1/{roleId}
- "Partially update a role?" -> PATCH /resources/roles/v1/{roleId}
- "List all phone-numbers?" -> GET /resources/users/phone-numbers/v1
- "Create a phone-number?" -> POST /resources/users/phone-numbers/v1
- "Create a preverify?" -> POST /resources/users/phone-numbers/v1/preverify
- "Create a verify?" -> POST /resources/users/phone-numbers/v1/verify
- "Delete a phone-number?" -> DELETE /resources/users/phone-numbers/v1/{id}
- "Create a verify?" -> POST /resources/users/phone-numbers/v1/{id}/delete/verify
- "List all me?" -> GET /resources/users/phone-numbers/v1/me
- "List all phone-numbers?" -> GET /resources/users/phone-numbers/v2
- "Create a sm?" -> POST /resources/configurations/v1/sms
- "List all sms?" -> GET /resources/configurations/v1/sms
- "List all templates?" -> GET /resources/configurations/v1/sms/templates
- "Get template details?" -> GET /resources/configurations/v1/sms/templates/{type}
- "Delete a template?" -> DELETE /resources/configurations/v1/sms/templates/{type}
- "List all default?" -> GET /resources/configurations/v1/sms/templates/{type}/default
- "List all all?" -> GET /resources/configurations/v1/sms/templates/default/all
- "List all vendor?" -> GET /resources/configurations/sessions/v1/vendor
- "List all sessions?" -> GET /resources/configurations/sessions/v1
- "Create a session?" -> POST /resources/configurations/sessions/v1
- "List all user-emails-policy?" -> GET /resources/configurations/v1/user-emails-policy
- "Create a user-emails-policy?" -> POST /resources/configurations/v1/user-emails-policy
- "List all groups?" -> GET /resources/groups/v1
- "Create a group?" -> POST /resources/groups/v1
- "Create a bulkGet?" -> POST /resources/groups/v1/bulkGet
- "Partially update a group?" -> PATCH /resources/groups/v1/{id}
- "Delete a group?" -> DELETE /resources/groups/v1/{id}
- "Get group details?" -> GET /resources/groups/v1/{id}
- "List all config?" -> GET /resources/groups/v1/config
- "Create a config?" -> POST /resources/groups/v1/config
- "Create a role?" -> POST /resources/groups/v1/{groupId}/roles
- "Create a user?" -> POST /resources/groups/v1/{groupId}/users
- "List all groups?" -> GET /resources/groups/v2
- "Create a disable?" -> POST /resources/tenants/users/v1/{userId}/disable
- "Create a enable?" -> POST /resources/tenants/users/v1/{userId}/enable
- "Update a temporary?" -> PUT /resources/users/temporary/v1/{userId}
- "Delete a temporary?" -> DELETE /resources/users/temporary/v1/{userId}
- "List all configuration?" -> GET /resources/users/temporary/v1/configuration
- "List all emails?" -> GET /resources/users/emails/v1
- "Create a email?" -> POST /resources/users/emails/v1
- "Create a verify?" -> POST /resources/users/emails/v1/verify
- "Delete a email?" -> DELETE /resources/users/emails/v1/{emailId}
- "Delete a vendor?" -> DELETE /resources/users/emails/v1/vendor/{userId}/{emailId}
- "Create a primary?" -> POST /resources/users/emails/v1/vendor/{userId}/primary
- "Create a primary?" -> POST /resources/users/emails/v1/me/primary
- "List all me?" -> GET /resources/users/emails/v1/me
- "Create a reset?" -> POST /resources/users/v1/activate/reset
- "Create a reset?" -> POST /resources/users/v1/invitation/reset
- "Create a all?" -> POST /resources/users/v1/invitation/reset/all
- "List all users?" -> GET /resources/users/v3
- "List all roles?" -> GET /resources/users/v3/roles
- "List all groups?" -> GET /resources/users/v3/groups
- "Create a unlock?" -> POST /resources/users/v3/me/unlock
- "Create a user?" -> POST /resources/users/v2
- "List all me?" -> GET /resources/users/v2/me
- "Create a user?" -> POST /resources/users/v1
- "Delete a user?" -> DELETE /resources/users/v1/{userId}
- "Update a user?" -> PUT /resources/users/v1/{userId}
- "Create a role?" -> POST /resources/users/v1/{userId}/roles
- "List all phrase?" -> GET /resources/users/v1/query/phrase
- "List all usernames?" -> GET /resources/usernames/v1
- "Create a username?" -> POST /resources/usernames/v1
- "Delete a username?" -> DELETE /resources/usernames/v1/{username}
- "List all me?" -> GET /resources/usernames/v1/me
- "Create a me?" -> POST /resources/users/v1/email/me
- "Create a verify?" -> POST /resources/users/v1/email/me/verify
- "Create a activate?" -> POST /resources/users/v1/activate
- "Create a code?" -> POST /resources/users/v1/activate/code
- "List all strategy?" -> GET /resources/users/v1/activate/strategy
- "Create a accept?" -> POST /resources/users/v1/invitation/accept
- "Create a code?" -> POST /resources/users/v1/invitation/accept/code
- "List all me?" -> GET /resources/users/v3/me
- "List all tenants?" -> GET /resources/users/v2/me/tenants
- "List all hierarchy?" -> GET /resources/users/v2/me/hierarchy
- "List all authorization?" -> GET /resources/users/v1/me/authorization
- "List all tenants?" -> GET /resources/users/v1/me/tenants
- "List all user-sources?" -> GET /resources/user-sources/v1
- "Get user-source details?" -> GET /resources/user-sources/v1/{id}
- "Delete a user-source?" -> DELETE /resources/user-sources/v1/{id}
- "Create a auth0?" -> POST /resources/user-sources/v1/external/auth0
- "Create a cognito?" -> POST /resources/user-sources/v1/external/cognito
- "Create a firebase?" -> POST /resources/user-sources/v1/external/firebase
- "Create a custom-code?" -> POST /resources/user-sources/v1/external/custom-code
- "Create a federation?" -> POST /resources/user-sources/v1/federation
- "Update a auth0?" -> PUT /resources/user-sources/v1/external/auth0/{id}
- "Update a cognito?" -> PUT /resources/user-sources/v1/external/cognito/{id}
- "Update a firebase?" -> PUT /resources/user-sources/v1/external/firebase/{id}
- "Update a custom-code?" -> PUT /resources/user-sources/v1/external/custom-code/{id}
- "Update a federation?" -> PUT /resources/user-sources/v1/federation/{id}
- "Create a assign?" -> POST /resources/user-sources/v1/assign
- "Create a unassign?" -> POST /resources/user-sources/v1/unassign
- "List all users?" -> GET /resources/user-sources/v1/{id}/users
- "List all me?" -> GET /resources/users/sessions/v1/me
- "Delete a me?" -> DELETE /resources/users/sessions/v1/me/{id}
- "Get user details?" -> GET /resources/vendor-only/users/v1/{userId}
- "Create a unenroll?" -> POST /resources/vendor-only/users/v1/{userId}/mfa/unenroll
- "Create a verify?" -> POST /resources/vendor-only/users/v1/passwords/verify
- "Create a user?" -> POST /resources/vendor-only/users/v1
- "List all statuses?" -> GET /resources/tenants/users/v1/statuses
- "Delete a vendor?" -> DELETE /resources/users/phone-numbers/v1/vendor/{userId}/{phoneId}
- "Create a invite?" -> POST /resources/users/bulk/v1/invite
- "Get status details?" -> GET /resources/users/bulk/v1/status/{id}
- "List all email?" -> GET /resources/users/v1/email
- "Get user details?" -> GET /resources/users/v1/{id}
- "Create a verify?" -> POST /resources/users/v1/{userId}/verify
- "Create a tenant?" -> POST /resources/users/v1/{userId}/tenant
- "Create a generate-activation-token?" -> POST /resources/users/v1/{userId}/links/generate-activation-token
- "Create a generate-password-reset-token?" -> POST /resources/users/v1/{userId}/links/generate-password-reset-token
- "Create a unlock?" -> POST /resources/users/v1/{userId}/unlock
- "Create a lock?" -> POST /resources/users/v1/{userId}/lock
- "List all users?" -> GET /resources/applications/v1/{appId}/users
- "List all apps?" -> GET /resources/applications/v1/{userId}/apps
- "Create a application?" -> POST /resources/applications/v1
- "List all active?" -> GET /resources/applications/user-tenants/active/v1
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
