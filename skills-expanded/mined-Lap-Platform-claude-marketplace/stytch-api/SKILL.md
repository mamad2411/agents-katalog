---
name: stytch-api
description: "Stytch API skill. Use when working with Stytch for connected_apps, b2b, users. Covers 184 endpoints."
version: 1.0.0
generator: lapsh
---

# Stytch API
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://api.stytch.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/sessions -- verify access
3. POST /v1/connected_apps/clients/search -- create first search

## Endpoints

184 endpoints across 21 groups. See references/api-spec.lap for full details.

### connected_apps
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/connected_apps/clients/{client_id} | Get |
| PUT | /v1/connected_apps/clients/{client_id} | Update |
| DELETE | /v1/connected_apps/clients/{client_id} | Delete |
| POST | /v1/connected_apps/clients/search | Search |
| POST | /v1/connected_apps/clients | Create |
| POST | /v1/connected_apps/clients/{client_id}/secrets/rotate/start | Rotatestart |
| POST | /v1/connected_apps/clients/{client_id}/secrets/rotate/cancel | Rotatecancel |
| POST | /v1/connected_apps/clients/{client_id}/secrets/rotate | Rotate |

### b2b
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v1/b2b/scim/{organization_id}/connection/{connection_id} | Update |
| DELETE | /v1/b2b/scim/{organization_id}/connection/{connection_id} | Delete |
| GET | /v1/b2b/scim/{organization_id}/connection/{connection_id} | Getgroups |
| POST | /v1/b2b/scim/{organization_id}/connection/{connection_id}/rotate/start | Rotatestart |
| POST | /v1/b2b/scim/{organization_id}/connection/{connection_id}/rotate/complete | Rotatecomplete |
| POST | /v1/b2b/scim/{organization_id}/connection/{connection_id}/rotate/cancel | Rotatecancel |
| POST | /v1/b2b/scim/{organization_id}/connection | Create |
| GET | /v1/b2b/scim/{organization_id}/connection | Get |
| POST | /v1/b2b/organizations | Create |
| GET | /v1/b2b/organizations/{organization_id} | Get |
| PUT | /v1/b2b/organizations/{organization_id} | Update |
| DELETE | /v1/b2b/organizations/{organization_id} | Delete |
| POST | /v1/b2b/organizations/search | Search |
| GET | /v1/b2b/organizations/{organization_id}/metrics | Metrics |
| GET | /v1/b2b/organizations/{organization_id}/connected_apps | Connectedapps |
| GET | /v1/b2b/organizations/{organization_id}/connected_apps/{connected_app_id} | Getconnectedapp |
| DELETE | /v1/b2b/organizations/{organization_id}/external_id | Deleteexternalid |
| PUT | /v1/b2b/organizations/{organization_id}/members/{member_id} | Update |
| DELETE | /v1/b2b/organizations/{organization_id}/members/{member_id} | Delete |
| PUT | /v1/b2b/organizations/{organization_id}/members/{member_id}/reactivate | Reactivate |
| DELETE | /v1/b2b/organizations/{organization_id}/members/mfa_phone_numbers/{member_id} | Deletemfaphonenumber |
| DELETE | /v1/b2b/organizations/{organization_id}/members/{member_id}/totp | Deletetotp |
| POST | /v1/b2b/organizations/members/search | Search |
| DELETE | /v1/b2b/organizations/{organization_id}/members/passwords/{member_password_id} | Deletepassword |
| GET | /v1/b2b/organizations/members/dangerously_get/{member_id} | Dangerouslyget |
| GET | /v1/b2b/organizations/{organization_id}/members/{member_id}/oidc_providers | Oidcproviders |
| POST | /v1/b2b/organizations/{organization_id}/members/{member_id}/unlink_retired_email | Unlinkretiredemail |
| POST | /v1/b2b/organizations/{organization_id}/members/{member_id}/start_email_update | Startemailupdate |
| GET | /v1/b2b/organizations/{organization_id}/members/{member_id}/connected_apps | Getconnectedapps |
| DELETE | /v1/b2b/organizations/{organization_id}/members/{member_id}/external_id | Deleteexternalid |
| POST | /v1/b2b/organizations/{organization_id}/members | Create |
| GET | /v1/b2b/organizations/{organization_id}/member | Get |
| GET | /v1/b2b/organizations/{organization_id}/members/{member_id}/oauth_providers/google | Google |
| GET | /v1/b2b/organizations/{organization_id}/members/{member_id}/oauth_providers/microsoft | Microsoft |
| GET | /v1/b2b/organizations/{organization_id}/members/{member_id}/oauth_providers/slack | Slack |
| GET | /v1/b2b/organizations/{organization_id}/members/{member_id}/oauth_providers/hubspot | Hubspot |
| GET | /v1/b2b/organizations/{organization_id}/members/{member_id}/oauth_providers/github | Github |
| POST | /v1/b2b/organizations/{organization_id}/members/{member_id}/connected_apps/{connected_app_id}/revoke | Revoke |
| POST | /v1/b2b/idp/oauth/authorize/start | Authorizestart |
| POST | /v1/b2b/idp/oauth/authorize | Authorize |
| GET | /v1/b2b/sessions | Get |
| POST | /v1/b2b/sessions/authenticate | Authenticate |
| POST | /v1/b2b/sessions/revoke | Revoke |
| POST | /v1/b2b/sessions/exchange | Exchange |
| POST | /v1/b2b/sessions/exchange_access_token | Exchangeaccesstoken |
| POST | /v1/b2b/sessions/attest | Attest |
| POST | /v1/b2b/sessions/migrate | Migrate |
| GET | /v1/b2b/sessions/jwks/{project_id} | Getjwks |
| POST | /v1/b2b/impersonation/authenticate | Authenticate |
| GET | /v1/b2b/rbac/policy | Policy |
| GET | /v1/b2b/rbac/organizations/{organization_id} | Getorgpolicy |
| PUT | /v1/b2b/rbac/organizations/{organization_id} | Setorgpolicy |
| POST | /v1/b2b/recovery_codes/recover | Recover |
| GET | /v1/b2b/recovery_codes/{organization_id}/{member_id} | Get |
| POST | /v1/b2b/recovery_codes/rotate | Rotate |
| POST | /v1/b2b/totp | Create |
| POST | /v1/b2b/totp/authenticate | Authenticate |
| POST | /v1/b2b/totp/migrate | Migrate |
| POST | /v1/b2b/discovery/intermediate_sessions/exchange | Exchange |
| POST | /v1/b2b/discovery/organizations/create | Create |
| POST | /v1/b2b/discovery/organizations | List |
| POST | /v1/b2b/magic_links/authenticate | Authenticate |
| POST | /v1/b2b/magic_links/email/login_or_signup | Loginorsignup |
| POST | /v1/b2b/magic_links/email/invite | Invite |
| POST | /v1/b2b/magic_links/email/discovery/send | Send |
| POST | /v1/b2b/magic_links/discovery/authenticate | Authenticate |
| POST | /v1/b2b/oauth/authenticate | Authenticate |
| POST | /v1/b2b/oauth/discovery/authenticate | Authenticate |
| POST | /v1/b2b/otps/sms/send | Send |
| POST | /v1/b2b/otps/sms/authenticate | Authenticate |
| POST | /v1/b2b/otps/email/login_or_signup | Loginorsignup |
| POST | /v1/b2b/otps/email/authenticate | Authenticate |
| POST | /v1/b2b/otps/email/discovery/send | Send |
| POST | /v1/b2b/otps/email/discovery/authenticate | Authenticate |
| POST | /v1/b2b/passwords/strength_check | Strengthcheck |
| POST | /v1/b2b/passwords/migrate | Migrate |
| POST | /v1/b2b/passwords/authenticate | Authenticate |
| POST | /v1/b2b/passwords/email/reset/start | Resetstart |
| POST | /v1/b2b/passwords/email/reset | Reset |
| POST | /v1/b2b/passwords/email/require_reset | Requirereset |
| POST | /v1/b2b/passwords/session/reset | Reset |
| POST | /v1/b2b/passwords/existing_password/reset | Reset |
| POST | /v1/b2b/passwords/discovery/authenticate | Authenticate |
| POST | /v1/b2b/passwords/discovery/email/reset/start | Resetstart |
| POST | /v1/b2b/passwords/discovery/email/reset | Reset |
| GET | /v1/b2b/sso/{organization_id} | Getconnections |
| DELETE | /v1/b2b/sso/{organization_id}/connections/{connection_id} | Deleteconnection |
| POST | /v1/b2b/sso/authenticate | Authenticate |
| POST | /v1/b2b/sso/oidc/{organization_id} | Createconnection |
| PUT | /v1/b2b/sso/oidc/{organization_id}/connections/{connection_id} | Updateconnection |
| POST | /v1/b2b/sso/saml/{organization_id} | Createconnection |
| PUT | /v1/b2b/sso/saml/{organization_id}/connections/{connection_id} | Updateconnection |
| PUT | /v1/b2b/sso/saml/{organization_id}/connections/{connection_id}/url | Updatebyurl |
| DELETE | /v1/b2b/sso/saml/{organization_id}/connections/{connection_id}/verification_certificates/{certificate_id} | Deleteverificationcertificate |
| DELETE | /v1/b2b/sso/saml/{organization_id}/connections/{connection_id}/encryption_private_keys/{private_key_id} | Deleteencryptionprivatekey |
| POST | /v1/b2b/sso/external/{organization_id} | Createconnection |
| PUT | /v1/b2b/sso/external/{organization_id}/connections/{connection_id} | Updateconnection |

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/users | Create |
| GET | /v1/users/{user_id} | Get |
| PUT | /v1/users/{user_id} | Update |
| DELETE | /v1/users/{user_id} | Delete |
| POST | /v1/users/search | Search |
| PUT | /v1/users/{user_id}/exchange_primary_factor | Exchangeprimaryfactor |
| DELETE | /v1/users/emails/{email_id} | Deleteemail |
| DELETE | /v1/users/phone_numbers/{phone_id} | Deletephonenumber |
| DELETE | /v1/users/webauthn_registrations/{webauthn_registration_id} | Deletewebauthnregistration |
| DELETE | /v1/users/biometric_registrations/{biometric_registration_id} | Deletebiometricregistration |
| DELETE | /v1/users/totps/{totp_id} | Deletetotp |
| DELETE | /v1/users/crypto_wallets/{crypto_wallet_id} | Deletecryptowallet |
| DELETE | /v1/users/passwords/{password_id} | Deletepassword |
| DELETE | /v1/users/oauth/{oauth_user_registration_id} | Deleteoauthregistration |
| DELETE | /v1/users/{user_id}/external_id | Deleteexternalid |
| GET | /v1/users/{user_id}/connected_apps | Connectedapps |
| POST | /v1/users/{user_id}/connected_apps/{connected_app_id}/revoke | Revoke |

### sessions
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/sessions | Get |
| POST | /v1/sessions/authenticate | Authenticate |
| POST | /v1/sessions/revoke | Revoke |
| POST | /v1/sessions/migrate | Migrate |
| POST | /v1/sessions/exchange_access_token | Exchangeaccesstoken |
| GET | /v1/sessions/jwks/{project_id} | Getjwks |
| POST | /v1/sessions/attest | Attest |

### rbac
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/rbac/policy | Policy |

### crypto_wallets
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/crypto_wallets/authenticate/start | Authenticatestart |
| POST | /v1/crypto_wallets/authenticate | Authenticate |

### debug
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/debug/whoami | Whoami |

### fingerprint
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/fingerprint/lookup | Lookup |

### rules
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/rules/set | Set |
| POST | /v1/rules/list | List |

### verdict_reasons
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/verdict_reasons/override | Override |
| POST | /v1/verdict_reasons/list | List |

### email
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/email/risk | Risk |

### idp
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/idp/oauth/authorize/start | Authorizestart |
| POST | /v1/idp/oauth/authorize | Authorize |

### impersonation
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/impersonation/authenticate | Authenticate |

### m2m
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/m2m/clients/{client_id} | Get |
| PUT | /v1/m2m/clients/{client_id} | Update |
| DELETE | /v1/m2m/clients/{client_id} | Delete |
| POST | /v1/m2m/clients/search | Search |
| POST | /v1/m2m/clients | Create |
| POST | /v1/m2m/clients/{client_id}/secrets/rotate/start | Rotatestart |
| POST | /v1/m2m/clients/{client_id}/secrets/rotate/cancel | Rotatecancel |
| POST | /v1/m2m/clients/{client_id}/secrets/rotate | Rotate |

### magic_links
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/magic_links/authenticate | Authenticate |
| POST | /v1/magic_links | Create |
| POST | /v1/magic_links/email/send | Send |
| POST | /v1/magic_links/email/login_or_create | Loginorcreate |
| POST | /v1/magic_links/email/invite | Invite |
| POST | /v1/magic_links/email/revoke_invite | Revokeinvite |

### passwords
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/passwords | Create |
| POST | /v1/passwords/authenticate | Authenticate |
| POST | /v1/passwords/strength_check | Strengthcheck |
| POST | /v1/passwords/migrate | Migrate |
| POST | /v1/passwords/email/reset/start | Resetstart |
| POST | /v1/passwords/email/reset | Reset |
| POST | /v1/passwords/existing_password/reset | Reset |
| POST | /v1/passwords/session/reset | Reset |

### oauth
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/oauth/attach | Attach |
| POST | /v1/oauth/authenticate | Authenticate |

### otps
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/otps/authenticate | Authenticate |
| POST | /v1/otps/sms/send | Send |
| POST | /v1/otps/sms/login_or_create | Loginorcreate |
| POST | /v1/otps/whatsapp/send | Send |
| POST | /v1/otps/whatsapp/login_or_create | Loginorcreate |
| POST | /v1/otps/email/send | Send |
| POST | /v1/otps/email/login_or_create | Loginorcreate |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/projects/metrics | Metrics |

### totps
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/totps | Create |
| POST | /v1/totps/authenticate | Authenticate |
| POST | /v1/totps/recovery_codes | Recoverycodes |
| POST | /v1/totps/recover | Recover |

### webauthn
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/webauthn/register/start | Registerstart |
| POST | /v1/webauthn/register | Register |
| POST | /v1/webauthn/authenticate/start | Authenticatestart |
| POST | /v1/webauthn/authenticate | Authenticate |
| PUT | /v1/webauthn/{webauthn_registration_id} | Update |
| GET | /v1/webauthn/credentials/{user_id}/{domain} | Listcredentials |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get client details?" -> GET /v1/connected_apps/clients/{client_id}
- "Update a client?" -> PUT /v1/connected_apps/clients/{client_id}
- "Delete a client?" -> DELETE /v1/connected_apps/clients/{client_id}
- "Create a search?" -> POST /v1/connected_apps/clients/search
- "Create a client?" -> POST /v1/connected_apps/clients
- "Create a start?" -> POST /v1/connected_apps/clients/{client_id}/secrets/rotate/start
- "Create a cancel?" -> POST /v1/connected_apps/clients/{client_id}/secrets/rotate/cancel
- "Create a rotate?" -> POST /v1/connected_apps/clients/{client_id}/secrets/rotate
- "Update a connection?" -> PUT /v1/b2b/scim/{organization_id}/connection/{connection_id}
- "Delete a connection?" -> DELETE /v1/b2b/scim/{organization_id}/connection/{connection_id}
- "Get connection details?" -> GET /v1/b2b/scim/{organization_id}/connection/{connection_id}
- "Create a start?" -> POST /v1/b2b/scim/{organization_id}/connection/{connection_id}/rotate/start
- "Create a complete?" -> POST /v1/b2b/scim/{organization_id}/connection/{connection_id}/rotate/complete
- "Create a cancel?" -> POST /v1/b2b/scim/{organization_id}/connection/{connection_id}/rotate/cancel
- "Create a connection?" -> POST /v1/b2b/scim/{organization_id}/connection
- "List all connection?" -> GET /v1/b2b/scim/{organization_id}/connection
- "Create a organization?" -> POST /v1/b2b/organizations
- "Get organization details?" -> GET /v1/b2b/organizations/{organization_id}
- "Update a organization?" -> PUT /v1/b2b/organizations/{organization_id}
- "Delete a organization?" -> DELETE /v1/b2b/organizations/{organization_id}
- "Create a search?" -> POST /v1/b2b/organizations/search
- "List all metrics?" -> GET /v1/b2b/organizations/{organization_id}/metrics
- "List all connected_apps?" -> GET /v1/b2b/organizations/{organization_id}/connected_apps
- "Get connected_app details?" -> GET /v1/b2b/organizations/{organization_id}/connected_apps/{connected_app_id}
- "Update a member?" -> PUT /v1/b2b/organizations/{organization_id}/members/{member_id}
- "Delete a member?" -> DELETE /v1/b2b/organizations/{organization_id}/members/{member_id}
- "Delete a mfa_phone_number?" -> DELETE /v1/b2b/organizations/{organization_id}/members/mfa_phone_numbers/{member_id}
- "Create a search?" -> POST /v1/b2b/organizations/members/search
- "Delete a password?" -> DELETE /v1/b2b/organizations/{organization_id}/members/passwords/{member_password_id}
- "Get dangerously_get details?" -> GET /v1/b2b/organizations/members/dangerously_get/{member_id}
- "List all oidc_providers?" -> GET /v1/b2b/organizations/{organization_id}/members/{member_id}/oidc_providers
- "Create a unlink_retired_email?" -> POST /v1/b2b/organizations/{organization_id}/members/{member_id}/unlink_retired_email
- "Create a start_email_update?" -> POST /v1/b2b/organizations/{organization_id}/members/{member_id}/start_email_update
- "List all connected_apps?" -> GET /v1/b2b/organizations/{organization_id}/members/{member_id}/connected_apps
- "Create a member?" -> POST /v1/b2b/organizations/{organization_id}/members
- "List all member?" -> GET /v1/b2b/organizations/{organization_id}/member
- "List all google?" -> GET /v1/b2b/organizations/{organization_id}/members/{member_id}/oauth_providers/google
- "List all microsoft?" -> GET /v1/b2b/organizations/{organization_id}/members/{member_id}/oauth_providers/microsoft
- "List all slack?" -> GET /v1/b2b/organizations/{organization_id}/members/{member_id}/oauth_providers/slack
- "List all hubspot?" -> GET /v1/b2b/organizations/{organization_id}/members/{member_id}/oauth_providers/hubspot
- "List all github?" -> GET /v1/b2b/organizations/{organization_id}/members/{member_id}/oauth_providers/github
- "Create a revoke?" -> POST /v1/b2b/organizations/{organization_id}/members/{member_id}/connected_apps/{connected_app_id}/revoke
- "Create a start?" -> POST /v1/b2b/idp/oauth/authorize/start
- "Create a authorize?" -> POST /v1/b2b/idp/oauth/authorize
- "Create a user?" -> POST /v1/users
- "Get user details?" -> GET /v1/users/{user_id}
- "Update a user?" -> PUT /v1/users/{user_id}
- "Delete a user?" -> DELETE /v1/users/{user_id}
- "Create a search?" -> POST /v1/users/search
- "Delete a email?" -> DELETE /v1/users/emails/{email_id}
- "Delete a phone_number?" -> DELETE /v1/users/phone_numbers/{phone_id}
- "Delete a webauthn_registration?" -> DELETE /v1/users/webauthn_registrations/{webauthn_registration_id}
- "Delete a biometric_registration?" -> DELETE /v1/users/biometric_registrations/{biometric_registration_id}
- "Delete a totp?" -> DELETE /v1/users/totps/{totp_id}
- "Delete a crypto_wallet?" -> DELETE /v1/users/crypto_wallets/{crypto_wallet_id}
- "Delete a password?" -> DELETE /v1/users/passwords/{password_id}
- "Delete a oauth?" -> DELETE /v1/users/oauth/{oauth_user_registration_id}
- "List all connected_apps?" -> GET /v1/users/{user_id}/connected_apps
- "Create a revoke?" -> POST /v1/users/{user_id}/connected_apps/{connected_app_id}/revoke
- "List all sessions?" -> GET /v1/sessions
- "Create a authenticate?" -> POST /v1/sessions/authenticate
- "Create a revoke?" -> POST /v1/sessions/revoke
- "Create a migrate?" -> POST /v1/sessions/migrate
- "Create a exchange_access_token?" -> POST /v1/sessions/exchange_access_token
- "Get jwk details?" -> GET /v1/sessions/jwks/{project_id}
- "Create a attest?" -> POST /v1/sessions/attest
- "List all sessions?" -> GET /v1/b2b/sessions
- "Create a authenticate?" -> POST /v1/b2b/sessions/authenticate
- "Create a revoke?" -> POST /v1/b2b/sessions/revoke
- "Create a exchange?" -> POST /v1/b2b/sessions/exchange
- "Create a exchange_access_token?" -> POST /v1/b2b/sessions/exchange_access_token
- "Create a attest?" -> POST /v1/b2b/sessions/attest
- "Create a migrate?" -> POST /v1/b2b/sessions/migrate
- "Get jwk details?" -> GET /v1/b2b/sessions/jwks/{project_id}
- "Create a authenticate?" -> POST /v1/b2b/impersonation/authenticate
- "List all policy?" -> GET /v1/b2b/rbac/policy
- "Get organization details?" -> GET /v1/b2b/rbac/organizations/{organization_id}
- "Update a organization?" -> PUT /v1/b2b/rbac/organizations/{organization_id}
- "Create a recover?" -> POST /v1/b2b/recovery_codes/recover
- "Get recovery_code details?" -> GET /v1/b2b/recovery_codes/{organization_id}/{member_id}
- "Create a rotate?" -> POST /v1/b2b/recovery_codes/rotate
- "Create a totp?" -> POST /v1/b2b/totp
- "Create a authenticate?" -> POST /v1/b2b/totp/authenticate
- "Create a migrate?" -> POST /v1/b2b/totp/migrate
- "List all policy?" -> GET /v1/rbac/policy
- "Create a start?" -> POST /v1/crypto_wallets/authenticate/start
- "Create a authenticate?" -> POST /v1/crypto_wallets/authenticate
- "List all whoami?" -> GET /v1/debug/whoami
- "Create a exchange?" -> POST /v1/b2b/discovery/intermediate_sessions/exchange
- "Create a create?" -> POST /v1/b2b/discovery/organizations/create
- "Create a organization?" -> POST /v1/b2b/discovery/organizations
- "Create a lookup?" -> POST /v1/fingerprint/lookup
- "Create a set?" -> POST /v1/rules/set
- "Create a list?" -> POST /v1/rules/list
- "Create a override?" -> POST /v1/verdict_reasons/override
- "Create a list?" -> POST /v1/verdict_reasons/list
- "Create a risk?" -> POST /v1/email/risk
- "Create a start?" -> POST /v1/idp/oauth/authorize/start
- "Create a authorize?" -> POST /v1/idp/oauth/authorize
- "Create a authenticate?" -> POST /v1/impersonation/authenticate
- "Get client details?" -> GET /v1/m2m/clients/{client_id}
- "Update a client?" -> PUT /v1/m2m/clients/{client_id}
- "Delete a client?" -> DELETE /v1/m2m/clients/{client_id}
- "Create a search?" -> POST /v1/m2m/clients/search
- "Create a client?" -> POST /v1/m2m/clients
- "Create a start?" -> POST /v1/m2m/clients/{client_id}/secrets/rotate/start
- "Create a cancel?" -> POST /v1/m2m/clients/{client_id}/secrets/rotate/cancel
- "Create a rotate?" -> POST /v1/m2m/clients/{client_id}/secrets/rotate
- "Create a authenticate?" -> POST /v1/magic_links/authenticate
- "Create a magic_link?" -> POST /v1/magic_links
- "Create a send?" -> POST /v1/magic_links/email/send
- "Create a login_or_create?" -> POST /v1/magic_links/email/login_or_create
- "Create a invite?" -> POST /v1/magic_links/email/invite
- "Create a revoke_invite?" -> POST /v1/magic_links/email/revoke_invite
- "Create a authenticate?" -> POST /v1/b2b/magic_links/authenticate
- "Create a login_or_signup?" -> POST /v1/b2b/magic_links/email/login_or_signup
- "Create a invite?" -> POST /v1/b2b/magic_links/email/invite
- "Create a send?" -> POST /v1/b2b/magic_links/email/discovery/send
- "Create a authenticate?" -> POST /v1/b2b/magic_links/discovery/authenticate
- "Create a authenticate?" -> POST /v1/b2b/oauth/authenticate
- "Create a authenticate?" -> POST /v1/b2b/oauth/discovery/authenticate
- "Create a send?" -> POST /v1/b2b/otps/sms/send
- "Create a authenticate?" -> POST /v1/b2b/otps/sms/authenticate
- "Create a login_or_signup?" -> POST /v1/b2b/otps/email/login_or_signup
- "Create a authenticate?" -> POST /v1/b2b/otps/email/authenticate
- "Create a send?" -> POST /v1/b2b/otps/email/discovery/send
- "Create a authenticate?" -> POST /v1/b2b/otps/email/discovery/authenticate
- "Create a password?" -> POST /v1/passwords
- "Create a authenticate?" -> POST /v1/passwords/authenticate
- "Create a strength_check?" -> POST /v1/passwords/strength_check
- "Create a migrate?" -> POST /v1/passwords/migrate
- "Create a start?" -> POST /v1/passwords/email/reset/start
- "Create a reset?" -> POST /v1/passwords/email/reset
- "Create a reset?" -> POST /v1/passwords/existing_password/reset
- "Create a reset?" -> POST /v1/passwords/session/reset
- "Create a strength_check?" -> POST /v1/b2b/passwords/strength_check
- "Create a migrate?" -> POST /v1/b2b/passwords/migrate
- "Create a authenticate?" -> POST /v1/b2b/passwords/authenticate
- "Create a start?" -> POST /v1/b2b/passwords/email/reset/start
- "Create a reset?" -> POST /v1/b2b/passwords/email/reset
- "Create a require_reset?" -> POST /v1/b2b/passwords/email/require_reset
- "Create a reset?" -> POST /v1/b2b/passwords/session/reset
- "Create a reset?" -> POST /v1/b2b/passwords/existing_password/reset
- "Create a authenticate?" -> POST /v1/b2b/passwords/discovery/authenticate
- "Create a start?" -> POST /v1/b2b/passwords/discovery/email/reset/start
- "Create a reset?" -> POST /v1/b2b/passwords/discovery/email/reset
- "Create a attach?" -> POST /v1/oauth/attach
- "Create a authenticate?" -> POST /v1/oauth/authenticate
- "Create a authenticate?" -> POST /v1/otps/authenticate
- "Create a send?" -> POST /v1/otps/sms/send
- "Create a login_or_create?" -> POST /v1/otps/sms/login_or_create
- "Create a send?" -> POST /v1/otps/whatsapp/send
- "Create a login_or_create?" -> POST /v1/otps/whatsapp/login_or_create
- "Create a send?" -> POST /v1/otps/email/send
- "Create a login_or_create?" -> POST /v1/otps/email/login_or_create
- "List all metrics?" -> GET /v1/projects/metrics
- "Get sso details?" -> GET /v1/b2b/sso/{organization_id}
- "Delete a connection?" -> DELETE /v1/b2b/sso/{organization_id}/connections/{connection_id}
- "Create a authenticate?" -> POST /v1/b2b/sso/authenticate
- "Update a connection?" -> PUT /v1/b2b/sso/oidc/{organization_id}/connections/{connection_id}
- "Update a connection?" -> PUT /v1/b2b/sso/saml/{organization_id}/connections/{connection_id}
- "Delete a verification_certificate?" -> DELETE /v1/b2b/sso/saml/{organization_id}/connections/{connection_id}/verification_certificates/{certificate_id}
- "Delete a encryption_private_key?" -> DELETE /v1/b2b/sso/saml/{organization_id}/connections/{connection_id}/encryption_private_keys/{private_key_id}
- "Update a connection?" -> PUT /v1/b2b/sso/external/{organization_id}/connections/{connection_id}
- "Create a totp?" -> POST /v1/totps
- "Create a authenticate?" -> POST /v1/totps/authenticate
- "Create a recovery_code?" -> POST /v1/totps/recovery_codes
- "Create a recover?" -> POST /v1/totps/recover
- "Create a start?" -> POST /v1/webauthn/register/start
- "Create a register?" -> POST /v1/webauthn/register
- "Create a start?" -> POST /v1/webauthn/authenticate/start
- "Create a authenticate?" -> POST /v1/webauthn/authenticate
- "Update a webauthn?" -> PUT /v1/webauthn/{webauthn_registration_id}
- "Get credential details?" -> GET /v1/webauthn/credentials/{user_id}/{domain}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
