---
name: clerk-backend-api
description: "Clerk Backend API skill. Use when working with Clerk Backend for public, jwks, clients. Covers 195 endpoints."
version: 1.0.0
generator: lapsh
---

# Clerk Backend API
API version: 2025-11-10

## Auth
Bearer bearer

## Base URL
https://api.clerk.com/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /public/interstitial -- verify access
3. POST /clients/verify -- create first verify

## Endpoints

195 endpoints across 37 groups. See references/api-spec.lap for full details.

### public
| Method | Path | Description |
|--------|------|-------------|
| GET | /public/interstitial | Returns the markup for the interstitial page |

### jwks
| Method | Path | Description |
|--------|------|-------------|
| GET | /jwks | Retrieve the JSON Web Key Set of the instance |

### clients
| Method | Path | Description |
|--------|------|-------------|
| GET | /clients | List all clients |
| POST | /clients/verify | Verify a client |
| GET | /clients/{client_id} | Get a client |

### email_addresses
| Method | Path | Description |
|--------|------|-------------|
| POST | /email_addresses | Create an email address |
| GET | /email_addresses/{email_address_id} | Retrieve an email address |
| DELETE | /email_addresses/{email_address_id} | Delete an email address |
| PATCH | /email_addresses/{email_address_id} | Update an email address |

### phone_numbers
| Method | Path | Description |
|--------|------|-------------|
| POST | /phone_numbers | Create a phone number |
| GET | /phone_numbers/{phone_number_id} | Retrieve a phone number |
| DELETE | /phone_numbers/{phone_number_id} | Delete a phone number |
| PATCH | /phone_numbers/{phone_number_id} | Update a phone number |

### sessions
| Method | Path | Description |
|--------|------|-------------|
| GET | /sessions | List all sessions |
| POST | /sessions | Create a new active session |
| GET | /sessions/{session_id} | Retrieve a session |
| POST | /sessions/{session_id}/refresh | Refresh a session |
| POST | /sessions/{session_id}/revoke | Revoke a session |
| POST | /sessions/{session_id}/tokens | Create a session token |
| POST | /sessions/{session_id}/tokens/{template_name} | Create a session token from a JWT template |

### templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /templates/{template_type} | List all templates |
| GET | /templates/{template_type}/{slug} | Retrieve a template |
| PUT | /templates/{template_type}/{slug} | Update a template for a given type and slug |
| POST | /templates/{template_type}/{slug}/revert | Revert a template |
| POST | /templates/{template_type}/{slug}/preview | Preview changes to a template |
| POST | /templates/{template_type}/{slug}/toggle_delivery | Toggle the delivery by Clerk for a template of a given type and slug |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | List all users |
| POST | /users | Create a new user |
| GET | /users/count | Count users |
| GET | /users/{user_id} | Retrieve a user |
| PATCH | /users/{user_id} | Update a user |
| DELETE | /users/{user_id} | Delete a user |
| POST | /users/{user_id}/ban | Ban a user |
| POST | /users/{user_id}/unban | Unban a user |
| POST | /users/ban | Ban multiple users |
| POST | /users/unban | Unban multiple users |
| POST | /users/{user_id}/lock | Lock a user |
| POST | /users/{user_id}/unlock | Unlock a user |
| POST | /users/{user_id}/profile_image | Set user profile image |
| DELETE | /users/{user_id}/profile_image | Delete user profile image |
| PATCH | /users/{user_id}/metadata | Merge and update a user's metadata |
| GET | /users/{user_id}/billing/subscription | Retrieve a user's billing subscription |
| GET | /users/{user_id}/oauth_access_tokens/{provider} | Retrieve the OAuth access token of a user |
| GET | /users/{user_id}/organization_memberships | Retrieve all memberships for a user |
| GET | /users/{user_id}/organization_invitations | Retrieve all invitations for a user |
| POST | /users/{user_id}/verify_password | Verify the password of a user |
| POST | /users/{user_id}/verify_totp | Verify a TOTP or backup code for a user |
| DELETE | /users/{user_id}/mfa | Disable a user's MFA methods |
| DELETE | /users/{user_id}/backup_code | Disable all user's Backup codes |
| DELETE | /users/{user_id}/passkeys/{passkey_identification_id} | Delete a user passkey |
| DELETE | /users/{user_id}/web3_wallets/{web3_wallet_identification_id} | Delete a user web3 wallet |
| DELETE | /users/{user_id}/totp | Delete all the user's TOTPs |
| DELETE | /users/{user_id}/external_accounts/{external_account_id} | Delete External Account |
| POST | /users/{user_id}/password/set_compromised | Set a user's password as compromised |
| POST | /users/{user_id}/password/unset_compromised | Unset a user's password as compromised |

### invitations
| Method | Path | Description |
|--------|------|-------------|
| POST | /invitations | Create an invitation |
| GET | /invitations | List all invitations |
| POST | /invitations/bulk | Create multiple invitations |
| POST | /invitations/{invitation_id}/revoke | Revokes an invitation |

### organization_invitations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization_invitations | Get a list of organization invitations for the current instance |

### allowlist_identifiers
| Method | Path | Description |
|--------|------|-------------|
| GET | /allowlist_identifiers | List all identifiers on the allow-list |
| POST | /allowlist_identifiers | Add identifier to the allow-list |
| DELETE | /allowlist_identifiers/{identifier_id} | Delete identifier from allow-list |

### blocklist_identifiers
| Method | Path | Description |
|--------|------|-------------|
| GET | /blocklist_identifiers | List all identifiers on the block-list |
| POST | /blocklist_identifiers | Add identifier to the block-list |
| DELETE | /blocklist_identifiers/{identifier_id} | Delete identifier from block-list |

### beta_features
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /beta_features/instance_settings | Update instance settings |
| PUT | /beta_features/domain | Update production instance domain |

### actor_tokens
| Method | Path | Description |
|--------|------|-------------|
| POST | /actor_tokens | Create actor token |
| POST | /actor_tokens/{actor_token_id}/revoke | Revoke actor token |

### domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /domains | List all instance domains |
| POST | /domains | Add a domain |
| DELETE | /domains/{domain_id} | Delete a satellite domain |
| PATCH | /domains/{domain_id} | Update a domain |

### instance
| Method | Path | Description |
|--------|------|-------------|
| GET | /instance | Fetch the current instance |
| PATCH | /instance | Update instance settings |
| PATCH | /instance/restrictions | Update instance restrictions |
| GET | /instance/protect | Get instance protect settings |
| PATCH | /instance/protect | Update instance protect settings |
| POST | /instance/change_domain | Update production instance domain |
| PATCH | /instance/organization_settings | Update instance organization settings |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| POST | /webhooks/svix | Create a Svix app |
| DELETE | /webhooks/svix | Delete a Svix app |
| POST | /webhooks/svix_url | Create a Svix Dashboard URL |

### jwt_templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /jwt_templates | List all templates |
| POST | /jwt_templates | Create a JWT template |
| GET | /jwt_templates/{template_id} | Retrieve a template |
| PATCH | /jwt_templates/{template_id} | Update a JWT template |
| DELETE | /jwt_templates/{template_id} | Delete a Template |

### machines
| Method | Path | Description |
|--------|------|-------------|
| GET | /machines | Get a list of machines for an instance |
| POST | /machines | Create a machine |
| GET | /machines/{machine_id} | Retrieve a machine |
| PATCH | /machines/{machine_id} | Update a machine |
| DELETE | /machines/{machine_id} | Delete a machine |
| GET | /machines/{machine_id}/secret_key | Retrieve a machine secret key |
| POST | /machines/{machine_id}/secret_key/rotate | Rotate a machine's secret key |
| POST | /machines/{machine_id}/scopes | Create a machine scope |
| DELETE | /machines/{machine_id}/scopes/{other_machine_id} | Delete a machine scope |

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organizations | Get a list of organizations for an instance |
| POST | /organizations | Create an organization |
| GET | /organizations/{organization_id} | Retrieve an organization by ID or slug |
| PATCH | /organizations/{organization_id} | Update an organization |
| DELETE | /organizations/{organization_id} | Delete an organization |
| PATCH | /organizations/{organization_id}/metadata | Merge and update metadata for an organization |
| PUT | /organizations/{organization_id}/logo | Upload a logo for the organization |
| DELETE | /organizations/{organization_id}/logo | Delete the organization's logo. |
| GET | /organizations/{organization_id}/billing/subscription | Retrieve an organization's billing subscription |
| POST | /organizations/{organization_id}/invitations | Create and send an organization invitation |
| GET | /organizations/{organization_id}/invitations | Get a list of organization invitations |
| POST | /organizations/{organization_id}/invitations/bulk | Bulk create and send organization invitations |
| GET | /organizations/{organization_id}/invitations/pending | Get a list of pending organization invitations |
| GET | /organizations/{organization_id}/invitations/{invitation_id} | Retrieve an organization invitation by ID |
| POST | /organizations/{organization_id}/invitations/{invitation_id}/revoke | Revoke a pending organization invitation |
| POST | /organizations/{organization_id}/memberships | Create a new organization membership |
| GET | /organizations/{organization_id}/memberships | Get a list of all members of an organization |
| PATCH | /organizations/{organization_id}/memberships/{user_id} | Update an organization membership |
| DELETE | /organizations/{organization_id}/memberships/{user_id} | Remove a member from an organization |
| PATCH | /organizations/{organization_id}/memberships/{user_id}/metadata | Merge and update organization membership metadata |
| POST | /organizations/{organization_id}/domains | Create a new organization domain. |
| GET | /organizations/{organization_id}/domains | Get a list of all domains of an organization. |
| PATCH | /organizations/{organization_id}/domains/{domain_id} | Update an organization domain. |
| DELETE | /organizations/{organization_id}/domains/{domain_id} | Remove a domain from an organization. |

### organization_roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization_roles | Get a list of organization roles |
| POST | /organization_roles | Create an organization role |
| GET | /organization_roles/{organization_role_id} | Retrieve an organization role |
| PATCH | /organization_roles/{organization_role_id} | Update an organization role |
| DELETE | /organization_roles/{organization_role_id} | Delete an organization role |
| POST | /organization_roles/{organization_role_id}/permissions/{permission_id} | Assign a permission to an organization role |
| DELETE | /organization_roles/{organization_role_id}/permissions/{permission_id} | Remove a permission from an organization role |

### organization_domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization_domains | List all organization domains |

### proxy_checks
| Method | Path | Description |
|--------|------|-------------|
| POST | /proxy_checks | Verify the proxy configuration for your domain |

### redirect_urls
| Method | Path | Description |
|--------|------|-------------|
| GET | /redirect_urls | List all redirect URLs |
| POST | /redirect_urls | Create a redirect URL |
| GET | /redirect_urls/{id} | Retrieve a redirect URL |
| DELETE | /redirect_urls/{id} | Delete a redirect URL |

### sign_in_tokens
| Method | Path | Description |
|--------|------|-------------|
| POST | /sign_in_tokens | Create sign-in token |
| POST | /sign_in_tokens/{sign_in_token_id}/revoke | Revoke the given sign-in token |

### sign_ups
| Method | Path | Description |
|--------|------|-------------|
| GET | /sign_ups/{id} | Retrieve a sign-up by ID |
| PATCH | /sign_ups/{id} | Update a sign-up |

### oauth_applications
| Method | Path | Description |
|--------|------|-------------|
| GET | /oauth_applications | Get a list of OAuth applications for an instance |
| POST | /oauth_applications | Create an OAuth application |
| GET | /oauth_applications/{oauth_application_id} | Retrieve an OAuth application by ID |
| PATCH | /oauth_applications/{oauth_application_id} | Update an OAuth application |
| DELETE | /oauth_applications/{oauth_application_id} | Delete an OAuth application |
| POST | /oauth_applications/{oauth_application_id}/rotate_secret | Rotate the client secret of the given OAuth application |
| POST | /oauth_applications/access_tokens/verify | Verify an OAuth Access Token |

### saml_connections
| Method | Path | Description |
|--------|------|-------------|
| GET | /saml_connections | Get a list of SAML Connections for an instance |
| POST | /saml_connections | Create a SAML Connection |
| GET | /saml_connections/{saml_connection_id} | Retrieve a SAML Connection by ID |
| PATCH | /saml_connections/{saml_connection_id} | Update a SAML Connection |
| DELETE | /saml_connections/{saml_connection_id} | Delete a SAML Connection |

### testing_tokens
| Method | Path | Description |
|--------|------|-------------|
| POST | /testing_tokens | Retrieve a new testing token |

### agents
| Method | Path | Description |
|--------|------|-------------|
| POST | /agents/tasks | Create agent task |
| POST | /agents/tasks/{agent_task_id}/revoke | Revoke agent task |

### organization_memberships
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization_memberships | Get a list of all organization memberships within an instance. |

### waitlist_entries
| Method | Path | Description |
|--------|------|-------------|
| GET | /waitlist_entries | List all waitlist entries |
| POST | /waitlist_entries | Create a waitlist entry |
| POST | /waitlist_entries/bulk | Create multiple waitlist entries |
| DELETE | /waitlist_entries/{waitlist_entry_id} | Delete a pending waitlist entry |
| POST | /waitlist_entries/{waitlist_entry_id}/invite | Invite a waitlist entry |
| POST | /waitlist_entries/{waitlist_entry_id}/reject | Reject a waitlist entry |

### billing
| Method | Path | Description |
|--------|------|-------------|
| GET | /billing/plans | List all billing plans |
| GET | /billing/prices | List all billing prices |
| POST | /billing/prices | Create a custom billing price |
| GET | /billing/subscription_items | List all subscription items |
| DELETE | /billing/subscription_items/{subscription_item_id} | Cancel a subscription item |
| POST | /billing/subscription_items/{subscription_item_id}/extend_free_trial | Extend free trial for a subscription item |
| POST | /billing/subscription_items/{subscription_item_id}/price_transition | Create a price transition for a subscription item |
| GET | /billing/statements | List all billing statements |
| GET | /billing/statements/{statementID} | Retrieve a billing statement |
| GET | /billing/statements/{statementID}/payment_attempts | List payment attempts for a billing statement |

### organization_permissions
| Method | Path | Description |
|--------|------|-------------|
| GET | /organization_permissions | Get a list of all organization permissions |
| POST | /organization_permissions | Create a new organization permission |
| GET | /organization_permissions/{permission_id} | Get an organization permission |
| PATCH | /organization_permissions/{permission_id} | Update an organization permission |
| DELETE | /organization_permissions/{permission_id} | Delete an organization permission |

### role_sets
| Method | Path | Description |
|--------|------|-------------|
| GET | /role_sets | Get a list of role sets |
| POST | /role_sets | Create a role set |
| GET | /role_sets/{role_set_key_or_id} | Retrieve a role set |
| PATCH | /role_sets/{role_set_key_or_id} | Update a role set |
| POST | /role_sets/{role_set_key_or_id}/replace | Replace a role set |
| POST | /role_sets/{role_set_key_or_id}/roles | Add roles to a role set |
| POST | /role_sets/{role_set_key_or_id}/roles/replace | Replace a role in a role set |

### api_keys
| Method | Path | Description |
|--------|------|-------------|
| POST | /api_keys | Create an API Key |
| GET | /api_keys | Get API Keys |
| GET | /api_keys/{apiKeyID} | Get an API Key by ID |
| PATCH | /api_keys/{apiKeyID} | Update an API Key |
| DELETE | /api_keys/{apiKeyID} | Delete an API Key |
| GET | /api_keys/{apiKeyID}/secret | Get an API Key Secret |
| POST | /api_keys/{apiKeyID}/revoke | Revoke an API Key |
| POST | /api_keys/verify | Verify an API Key |

### m2m_tokens
| Method | Path | Description |
|--------|------|-------------|
| POST | /m2m_tokens | Create a M2M Token |
| GET | /m2m_tokens | Get M2M Tokens |
| POST | /m2m_tokens/{m2m_token_id}/revoke | Revoke a M2M Token |
| POST | /m2m_tokens/verify | Verify a M2M Token |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all interstitial?" -> GET /public/interstitial
- "List all jwks?" -> GET /jwks
- "List all clients?" -> GET /clients
- "Create a verify?" -> POST /clients/verify
- "Get client details?" -> GET /clients/{client_id}
- "Create a email_address?" -> POST /email_addresses
- "Get email_address details?" -> GET /email_addresses/{email_address_id}
- "Delete a email_address?" -> DELETE /email_addresses/{email_address_id}
- "Partially update a email_address?" -> PATCH /email_addresses/{email_address_id}
- "Create a phone_number?" -> POST /phone_numbers
- "Get phone_number details?" -> GET /phone_numbers/{phone_number_id}
- "Delete a phone_number?" -> DELETE /phone_numbers/{phone_number_id}
- "Partially update a phone_number?" -> PATCH /phone_numbers/{phone_number_id}
- "List all sessions?" -> GET /sessions
- "Create a session?" -> POST /sessions
- "Get session details?" -> GET /sessions/{session_id}
- "Create a refresh?" -> POST /sessions/{session_id}/refresh
- "Create a revoke?" -> POST /sessions/{session_id}/revoke
- "Create a token?" -> POST /sessions/{session_id}/tokens
- "Get template details?" -> GET /templates/{template_type}
- "Get template details?" -> GET /templates/{template_type}/{slug}
- "Update a template?" -> PUT /templates/{template_type}/{slug}
- "Create a revert?" -> POST /templates/{template_type}/{slug}/revert
- "Create a preview?" -> POST /templates/{template_type}/{slug}/preview
- "Create a toggle_delivery?" -> POST /templates/{template_type}/{slug}/toggle_delivery
- "Search users?" -> GET /users
- "Create a user?" -> POST /users
- "Search count?" -> GET /users/count
- "Get user details?" -> GET /users/{user_id}
- "Partially update a user?" -> PATCH /users/{user_id}
- "Delete a user?" -> DELETE /users/{user_id}
- "Create a ban?" -> POST /users/{user_id}/ban
- "Create a unban?" -> POST /users/{user_id}/unban
- "Create a ban?" -> POST /users/ban
- "Create a unban?" -> POST /users/unban
- "Create a lock?" -> POST /users/{user_id}/lock
- "Create a unlock?" -> POST /users/{user_id}/unlock
- "Create a profile_image?" -> POST /users/{user_id}/profile_image
- "List all subscription?" -> GET /users/{user_id}/billing/subscription
- "Get oauth_access_token details?" -> GET /users/{user_id}/oauth_access_tokens/{provider}
- "List all organization_memberships?" -> GET /users/{user_id}/organization_memberships
- "List all organization_invitations?" -> GET /users/{user_id}/organization_invitations
- "Create a verify_password?" -> POST /users/{user_id}/verify_password
- "Create a verify_totp?" -> POST /users/{user_id}/verify_totp
- "Delete a passkey?" -> DELETE /users/{user_id}/passkeys/{passkey_identification_id}
- "Delete a web3_wallet?" -> DELETE /users/{user_id}/web3_wallets/{web3_wallet_identification_id}
- "Delete a external_account?" -> DELETE /users/{user_id}/external_accounts/{external_account_id}
- "Create a set_compromised?" -> POST /users/{user_id}/password/set_compromised
- "Create a unset_compromised?" -> POST /users/{user_id}/password/unset_compromised
- "Create a invitation?" -> POST /invitations
- "Search invitations?" -> GET /invitations
- "Create a bulk?" -> POST /invitations/bulk
- "Create a revoke?" -> POST /invitations/{invitation_id}/revoke
- "Search organization_invitations?" -> GET /organization_invitations
- "List all allowlist_identifiers?" -> GET /allowlist_identifiers
- "Create a allowlist_identifier?" -> POST /allowlist_identifiers
- "Delete a allowlist_identifier?" -> DELETE /allowlist_identifiers/{identifier_id}
- "List all blocklist_identifiers?" -> GET /blocklist_identifiers
- "Create a blocklist_identifier?" -> POST /blocklist_identifiers
- "Delete a blocklist_identifier?" -> DELETE /blocklist_identifiers/{identifier_id}
- "Create a actor_token?" -> POST /actor_tokens
- "Create a revoke?" -> POST /actor_tokens/{actor_token_id}/revoke
- "List all domains?" -> GET /domains
- "Create a domain?" -> POST /domains
- "Delete a domain?" -> DELETE /domains/{domain_id}
- "Partially update a domain?" -> PATCH /domains/{domain_id}
- "List all instance?" -> GET /instance
- "List all protect?" -> GET /instance/protect
- "Create a change_domain?" -> POST /instance/change_domain
- "Create a svix?" -> POST /webhooks/svix
- "Create a svix_url?" -> POST /webhooks/svix_url
- "List all jwt_templates?" -> GET /jwt_templates
- "Create a jwt_template?" -> POST /jwt_templates
- "Get jwt_template details?" -> GET /jwt_templates/{template_id}
- "Partially update a jwt_template?" -> PATCH /jwt_templates/{template_id}
- "Delete a jwt_template?" -> DELETE /jwt_templates/{template_id}
- "Search machines?" -> GET /machines
- "Create a machine?" -> POST /machines
- "Get machine details?" -> GET /machines/{machine_id}
- "Partially update a machine?" -> PATCH /machines/{machine_id}
- "Delete a machine?" -> DELETE /machines/{machine_id}
- "List all secret_key?" -> GET /machines/{machine_id}/secret_key
- "Create a rotate?" -> POST /machines/{machine_id}/secret_key/rotate
- "Create a scope?" -> POST /machines/{machine_id}/scopes
- "Delete a scope?" -> DELETE /machines/{machine_id}/scopes/{other_machine_id}
- "Search organizations?" -> GET /organizations
- "Create a organization?" -> POST /organizations
- "Get organization details?" -> GET /organizations/{organization_id}
- "Partially update a organization?" -> PATCH /organizations/{organization_id}
- "Delete a organization?" -> DELETE /organizations/{organization_id}
- "List all subscription?" -> GET /organizations/{organization_id}/billing/subscription
- "Create a invitation?" -> POST /organizations/{organization_id}/invitations
- "List all invitations?" -> GET /organizations/{organization_id}/invitations
- "Create a bulk?" -> POST /organizations/{organization_id}/invitations/bulk
- "List all pending?" -> GET /organizations/{organization_id}/invitations/pending
- "Get invitation details?" -> GET /organizations/{organization_id}/invitations/{invitation_id}
- "Create a revoke?" -> POST /organizations/{organization_id}/invitations/{invitation_id}/revoke
- "Search organization_roles?" -> GET /organization_roles
- "Create a organization_role?" -> POST /organization_roles
- "Get organization_role details?" -> GET /organization_roles/{organization_role_id}
- "Partially update a organization_role?" -> PATCH /organization_roles/{organization_role_id}
- "Delete a organization_role?" -> DELETE /organization_roles/{organization_role_id}
- "Delete a permission?" -> DELETE /organization_roles/{organization_role_id}/permissions/{permission_id}
- "Create a membership?" -> POST /organizations/{organization_id}/memberships
- "Search memberships?" -> GET /organizations/{organization_id}/memberships
- "Partially update a membership?" -> PATCH /organizations/{organization_id}/memberships/{user_id}
- "Delete a membership?" -> DELETE /organizations/{organization_id}/memberships/{user_id}
- "Create a domain?" -> POST /organizations/{organization_id}/domains
- "List all domains?" -> GET /organizations/{organization_id}/domains
- "Partially update a domain?" -> PATCH /organizations/{organization_id}/domains/{domain_id}
- "Delete a domain?" -> DELETE /organizations/{organization_id}/domains/{domain_id}
- "Search organization_domains?" -> GET /organization_domains
- "Create a proxy_check?" -> POST /proxy_checks
- "List all redirect_urls?" -> GET /redirect_urls
- "Create a redirect_url?" -> POST /redirect_urls
- "Get redirect_url details?" -> GET /redirect_urls/{id}
- "Delete a redirect_url?" -> DELETE /redirect_urls/{id}
- "Create a sign_in_token?" -> POST /sign_in_tokens
- "Create a revoke?" -> POST /sign_in_tokens/{sign_in_token_id}/revoke
- "Get sign_up details?" -> GET /sign_ups/{id}
- "Partially update a sign_up?" -> PATCH /sign_ups/{id}
- "List all oauth_applications?" -> GET /oauth_applications
- "Create a oauth_application?" -> POST /oauth_applications
- "Get oauth_application details?" -> GET /oauth_applications/{oauth_application_id}
- "Partially update a oauth_application?" -> PATCH /oauth_applications/{oauth_application_id}
- "Delete a oauth_application?" -> DELETE /oauth_applications/{oauth_application_id}
- "Create a rotate_secret?" -> POST /oauth_applications/{oauth_application_id}/rotate_secret
- "Search saml_connections?" -> GET /saml_connections
- "Create a saml_connection?" -> POST /saml_connections
- "Get saml_connection details?" -> GET /saml_connections/{saml_connection_id}
- "Partially update a saml_connection?" -> PATCH /saml_connections/{saml_connection_id}
- "Delete a saml_connection?" -> DELETE /saml_connections/{saml_connection_id}
- "Create a testing_token?" -> POST /testing_tokens
- "Create a task?" -> POST /agents/tasks
- "Create a revoke?" -> POST /agents/tasks/{agent_task_id}/revoke
- "List all organization_memberships?" -> GET /organization_memberships
- "Search waitlist_entries?" -> GET /waitlist_entries
- "Create a waitlist_entry?" -> POST /waitlist_entries
- "Create a bulk?" -> POST /waitlist_entries/bulk
- "Delete a waitlist_entry?" -> DELETE /waitlist_entries/{waitlist_entry_id}
- "Create a invite?" -> POST /waitlist_entries/{waitlist_entry_id}/invite
- "Create a reject?" -> POST /waitlist_entries/{waitlist_entry_id}/reject
- "List all plans?" -> GET /billing/plans
- "List all prices?" -> GET /billing/prices
- "Create a price?" -> POST /billing/prices
- "Search subscription_items?" -> GET /billing/subscription_items
- "Delete a subscription_item?" -> DELETE /billing/subscription_items/{subscription_item_id}
- "Create a extend_free_trial?" -> POST /billing/subscription_items/{subscription_item_id}/extend_free_trial
- "Create a price_transition?" -> POST /billing/subscription_items/{subscription_item_id}/price_transition
- "List all statements?" -> GET /billing/statements
- "Get statement details?" -> GET /billing/statements/{statementID}
- "List all payment_attempts?" -> GET /billing/statements/{statementID}/payment_attempts
- "Search organization_permissions?" -> GET /organization_permissions
- "Create a organization_permission?" -> POST /organization_permissions
- "Get organization_permission details?" -> GET /organization_permissions/{permission_id}
- "Partially update a organization_permission?" -> PATCH /organization_permissions/{permission_id}
- "Delete a organization_permission?" -> DELETE /organization_permissions/{permission_id}
- "Search role_sets?" -> GET /role_sets
- "Create a role_set?" -> POST /role_sets
- "Get role_set details?" -> GET /role_sets/{role_set_key_or_id}
- "Partially update a role_set?" -> PATCH /role_sets/{role_set_key_or_id}
- "Create a replace?" -> POST /role_sets/{role_set_key_or_id}/replace
- "Create a role?" -> POST /role_sets/{role_set_key_or_id}/roles
- "Create a replace?" -> POST /role_sets/{role_set_key_or_id}/roles/replace
- "Create a api_key?" -> POST /api_keys
- "Search api_keys?" -> GET /api_keys
- "Get api_key details?" -> GET /api_keys/{apiKeyID}
- "Partially update a api_key?" -> PATCH /api_keys/{apiKeyID}
- "Delete a api_key?" -> DELETE /api_keys/{apiKeyID}
- "List all secret?" -> GET /api_keys/{apiKeyID}/secret
- "Create a revoke?" -> POST /api_keys/{apiKeyID}/revoke
- "Create a verify?" -> POST /api_keys/verify
- "Create a m2m_token?" -> POST /m2m_tokens
- "List all m2m_tokens?" -> GET /m2m_tokens
- "Create a revoke?" -> POST /m2m_tokens/{m2m_token_id}/revoke
- "Create a verify?" -> POST /m2m_tokens/verify
- "Create a verify?" -> POST /oauth_applications/access_tokens/verify
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
