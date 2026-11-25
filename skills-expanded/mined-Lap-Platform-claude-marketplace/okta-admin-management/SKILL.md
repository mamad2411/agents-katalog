---
name: okta-admin-management
description: "Okta Admin Management API skill. Use when working with Okta Admin Management for .well-known, api, attack-protection. Covers 705 endpoints."
version: 1.0.0
generator: lapsh
---

# Okta Admin Management
API version: 5.1.0

## Auth
ApiKey Authorization in header | OAuth2

## Base URL
https://subdomain.okta.com

## Setup
1. Set your API key in the appropriate header
2. GET /.well-known/app-authenticator-configuration -- verify access
3. POST /api/v1/agentPools/{poolId}/updates -- create first updates

## Endpoints

705 endpoints across 10 groups. See references/api-spec.lap for full details.

### .well-known
| Method | Path | Description |
|--------|------|-------------|
| GET | /.well-known/app-authenticator-configuration | Retrieve the well-known app authenticator configuration |
| GET | /.well-known/apple-app-site-association | Retrieve the customized apple-app-site-association URI content |
| GET | /.well-known/assetlinks.json | Retrieve the customized assetlinks.json URI content |
| GET | /.well-known/okta-organization | Retrieve the Org metadata |
| GET | /.well-known/ssf-configuration | Retrieve the SSF transmitter metadata |
| GET | /.well-known/webauthn | Retrieve the customized webauthn URI content |

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v1/agentPools | List all agent pools |
| GET | /api/v1/agentPools/{poolId}/updates | List all agent pool updates |
| POST | /api/v1/agentPools/{poolId}/updates | Create an agent pool update |
| GET | /api/v1/agentPools/{poolId}/updates/settings | Retrieve an agent pool update's settings |
| POST | /api/v1/agentPools/{poolId}/updates/settings | Update an agent pool update settings |
| GET | /api/v1/agentPools/{poolId}/updates/{updateId} | Retrieve an agent pool update by ID |
| POST | /api/v1/agentPools/{poolId}/updates/{updateId} | Update an agent pool update by ID |
| DELETE | /api/v1/agentPools/{poolId}/updates/{updateId} | Delete an agent pool update |
| POST | /api/v1/agentPools/{poolId}/updates/{updateId}/activate | Activate an agent pool update |
| POST | /api/v1/agentPools/{poolId}/updates/{updateId}/deactivate | Deactivate an agent pool update |
| POST | /api/v1/agentPools/{poolId}/updates/{updateId}/pause | Pause an agent pool update |
| POST | /api/v1/agentPools/{poolId}/updates/{updateId}/resume | Resume an agent pool update |
| POST | /api/v1/agentPools/{poolId}/updates/{updateId}/retry | Retry an agent pool update |
| POST | /api/v1/agentPools/{poolId}/updates/{updateId}/stop | Stop an agent pool update |
| GET | /api/v1/api-tokens | List all API token metadata |
| DELETE | /api/v1/api-tokens/current | Revoke the current API token |
| GET | /api/v1/api-tokens/{apiTokenId} | Retrieve an API token's metadata |
| PUT | /api/v1/api-tokens/{apiTokenId} | Upsert an API token network condition |
| DELETE | /api/v1/api-tokens/{apiTokenId} | Revoke an API token |
| GET | /api/v1/apps | List all applications |
| POST | /api/v1/apps | Create an application |
| GET | /api/v1/apps/{appId} | Retrieve an application |
| PUT | /api/v1/apps/{appId} | Replace an application |
| DELETE | /api/v1/apps/{appId} | Delete an application |
| GET | /api/v1/apps/{appId}/connections/default | Retrieve the default provisioning connection |
| POST | /api/v1/apps/{appId}/connections/default | Update the default provisioning connection |
| GET | /api/v1/apps/{appId}/connections/default/jwks | Retrieve a JSON Web Key Set (JWKS) for the default provisioning connection |
| POST | /api/v1/apps/{appId}/connections/default/lifecycle/activate | Activate the default provisioning connection |
| POST | /api/v1/apps/{appId}/connections/default/lifecycle/deactivate | Deactivate the default provisioning connection |
| GET | /api/v1/apps/{appId}/credentials/csrs | List all certificate signing requests |
| POST | /api/v1/apps/{appId}/credentials/csrs | Generate a certificate signing request |
| GET | /api/v1/apps/{appId}/credentials/csrs/{csrId} | Retrieve a certificate signing request |
| DELETE | /api/v1/apps/{appId}/credentials/csrs/{csrId} | Revoke a certificate signing request |
| POST | /api/v1/apps/{appId}/credentials/csrs/{csrId}/lifecycle/publish | Publish a certificate signing request |
| GET | /api/v1/apps/{appId}/credentials/jwks | List all the OAuth 2.0 client JSON Web Keys |
| POST | /api/v1/apps/{appId}/credentials/jwks | Add a JSON Web Key |
| GET | /api/v1/apps/{appId}/credentials/jwks/{keyId} | Retrieve an OAuth 2.0 client JSON Web Key |
| DELETE | /api/v1/apps/{appId}/credentials/jwks/{keyId} | Delete an OAuth 2.0 client JSON Web Key |
| POST | /api/v1/apps/{appId}/credentials/jwks/{keyId}/lifecycle/activate | Activate an OAuth 2.0 client JSON Web Key |
| POST | /api/v1/apps/{appId}/credentials/jwks/{keyId}/lifecycle/deactivate | Deactivate an OAuth 2.0 client JSON Web Key |
| GET | /api/v1/apps/{appId}/credentials/keys | List all key credentials |
| POST | /api/v1/apps/{appId}/credentials/keys/generate | Generate a key credential |
| GET | /api/v1/apps/{appId}/credentials/keys/{keyId} | Retrieve a key credential |
| POST | /api/v1/apps/{appId}/credentials/keys/{keyId}/clone | Clone a key credential |
| GET | /api/v1/apps/{appId}/credentials/secrets | List all OAuth 2.0 client secrets |
| POST | /api/v1/apps/{appId}/credentials/secrets | Create an OAuth 2.0 client secret |
| GET | /api/v1/apps/{appId}/credentials/secrets/{secretId} | Retrieve an OAuth 2.0 client secret |
| DELETE | /api/v1/apps/{appId}/credentials/secrets/{secretId} | Delete an OAuth 2.0 client secret |
| POST | /api/v1/apps/{appId}/credentials/secrets/{secretId}/lifecycle/activate | Activate an OAuth 2.0 client secret |
| POST | /api/v1/apps/{appId}/credentials/secrets/{secretId}/lifecycle/deactivate | Deactivate an OAuth 2.0 client secret |
| GET | /api/v1/apps/{appId}/cwo/connections | Retrieve all Cross App Access connections |
| POST | /api/v1/apps/{appId}/cwo/connections | Create a Cross App Access connection |
| GET | /api/v1/apps/{appId}/cwo/connections/{connectionId} | Retrieve a Cross App Access connection |
| PATCH | /api/v1/apps/{appId}/cwo/connections/{connectionId} | Update a Cross App Access connection |
| DELETE | /api/v1/apps/{appId}/cwo/connections/{connectionId} | Delete a Cross App Access connection |
| GET | /api/v1/apps/{appId}/features | List all features |
| GET | /api/v1/apps/{appId}/features/{featureName} | Retrieve a feature |
| PUT | /api/v1/apps/{appId}/features/{featureName} | Update a feature |
| GET | /api/v1/apps/{appId}/federated-claims | List all configured federated claims |
| POST | /api/v1/apps/{appId}/federated-claims | Create a federated claim |
| GET | /api/v1/apps/{appId}/federated-claims/{claimId} | Retrieve a federated claim |
| PUT | /api/v1/apps/{appId}/federated-claims/{claimId} | Replace a federated claim |
| DELETE | /api/v1/apps/{appId}/federated-claims/{claimId} | Delete a federated claim |
| GET | /api/v1/apps/{appId}/grants | List all app grants |
| POST | /api/v1/apps/{appId}/grants | Grant consent to scope |
| GET | /api/v1/apps/{appId}/grants/{grantId} | Retrieve an app grant |
| DELETE | /api/v1/apps/{appId}/grants/{grantId} | Revoke an app grant |
| GET | /api/v1/apps/{appId}/group-push/mappings | List all group push mappings |
| POST | /api/v1/apps/{appId}/group-push/mappings | Create a group push mapping |
| GET | /api/v1/apps/{appId}/group-push/mappings/{mappingId} | Retrieve a group push mapping |
| PATCH | /api/v1/apps/{appId}/group-push/mappings/{mappingId} | Update a group push mapping |
| DELETE | /api/v1/apps/{appId}/group-push/mappings/{mappingId} | Delete a group push mapping |
| GET | /api/v1/apps/{appId}/groups | List all application groups |
| GET | /api/v1/apps/{appId}/groups/{groupId} | Retrieve an application group |
| PUT | /api/v1/apps/{appId}/groups/{groupId} | Assign an application group |
| PATCH | /api/v1/apps/{appId}/groups/{groupId} | Update an application group |
| DELETE | /api/v1/apps/{appId}/groups/{groupId} | Unassign an application group |
| POST | /api/v1/apps/{appId}/lifecycle/activate | Activate an application |
| POST | /api/v1/apps/{appId}/lifecycle/deactivate | Deactivate an application |
| POST | /api/v1/apps/{appId}/logo | Upload an application logo |
| PUT | /api/v1/apps/{appId}/policies/{policyId} | Assign an authentication policy |
| GET | /api/v1/apps/{appId}/sso/saml/metadata | Preview the application SAML metadata |
| GET | /api/v1/apps/{appId}/tokens | List all application refresh tokens |
| DELETE | /api/v1/apps/{appId}/tokens | Revoke all application tokens |
| GET | /api/v1/apps/{appId}/tokens/{tokenId} | Retrieve an application token |
| DELETE | /api/v1/apps/{appId}/tokens/{tokenId} | Revoke an application token |
| GET | /api/v1/apps/{appId}/users | List all application users |
| POST | /api/v1/apps/{appId}/users | Assign an application user |
| GET | /api/v1/apps/{appId}/users/{userId} | Retrieve an application user |
| POST | /api/v1/apps/{appId}/users/{userId} | Update an application user |
| DELETE | /api/v1/apps/{appId}/users/{userId} | Unassign an application user |
| POST | /api/v1/apps/{appName}/{appId}/oauth2/callback | Verify the provisioning connection |
| GET | /api/v1/authenticators | List all authenticators |
| POST | /api/v1/authenticators | Create an authenticator |
| GET | /api/v1/authenticators/{authenticatorId} | Retrieve an authenticator |
| PUT | /api/v1/authenticators/{authenticatorId} | Replace an authenticator |
| GET | /api/v1/authenticators/{authenticatorId}/aaguids | List all custom AAGUIDs |
| POST | /api/v1/authenticators/{authenticatorId}/aaguids | Create a custom AAGUID |
| GET | /api/v1/authenticators/{authenticatorId}/aaguids/{aaguid} | Retrieve a custom AAGUID |
| PUT | /api/v1/authenticators/{authenticatorId}/aaguids/{aaguid} | Replace a custom AAGUID |
| PATCH | /api/v1/authenticators/{authenticatorId}/aaguids/{aaguid} | Update a custom AAGUID |
| DELETE | /api/v1/authenticators/{authenticatorId}/aaguids/{aaguid} | Delete a custom AAGUID |
| POST | /api/v1/authenticators/{authenticatorId}/lifecycle/activate | Activate an authenticator |
| POST | /api/v1/authenticators/{authenticatorId}/lifecycle/deactivate | Deactivate an authenticator |
| GET | /api/v1/authenticators/{authenticatorId}/methods | List all methods of an authenticator |
| GET | /api/v1/authenticators/{authenticatorId}/methods/{methodType} | Retrieve an authenticator method |
| PUT | /api/v1/authenticators/{authenticatorId}/methods/{methodType} | Replace an authenticator method |
| POST | /api/v1/authenticators/{authenticatorId}/methods/{methodType}/lifecycle/activate | Activate an authenticator method |
| POST | /api/v1/authenticators/{authenticatorId}/methods/{methodType}/lifecycle/deactivate | Deactivate an authenticator method |
| GET | /api/v1/authorizationServers | List all authorization servers |
| POST | /api/v1/authorizationServers | Create an authorization server |
| GET | /api/v1/authorizationServers/{authServerId} | Retrieve an authorization server |
| PUT | /api/v1/authorizationServers/{authServerId} | Replace an authorization server |
| DELETE | /api/v1/authorizationServers/{authServerId} | Delete an authorization server |
| GET | /api/v1/authorizationServers/{authServerId}/associatedServers | List all associated authorization servers |
| POST | /api/v1/authorizationServers/{authServerId}/associatedServers | Create an associated authorization server |
| DELETE | /api/v1/authorizationServers/{authServerId}/associatedServers/{associatedServerId} | Delete an associated authorization server |
| GET | /api/v1/authorizationServers/{authServerId}/claims | List all custom token claims |
| POST | /api/v1/authorizationServers/{authServerId}/claims | Create a custom token claim |
| GET | /api/v1/authorizationServers/{authServerId}/claims/{claimId} | Retrieve a custom token claim |
| PUT | /api/v1/authorizationServers/{authServerId}/claims/{claimId} | Replace a custom token claim |
| DELETE | /api/v1/authorizationServers/{authServerId}/claims/{claimId} | Delete a custom token claim |
| GET | /api/v1/authorizationServers/{authServerId}/clients | List all client resources for an authorization server |
| GET | /api/v1/authorizationServers/{authServerId}/clients/{clientId}/tokens | List all refresh tokens for a client |
| DELETE | /api/v1/authorizationServers/{authServerId}/clients/{clientId}/tokens | Revoke all refresh tokens for a client |
| GET | /api/v1/authorizationServers/{authServerId}/clients/{clientId}/tokens/{tokenId} | Retrieve a refresh token for a client |
| DELETE | /api/v1/authorizationServers/{authServerId}/clients/{clientId}/tokens/{tokenId} | Revoke a refresh token for a client |
| GET | /api/v1/authorizationServers/{authServerId}/credentials/keys | List all credential keys |
| GET | /api/v1/authorizationServers/{authServerId}/credentials/keys/{keyId} | Retrieve an authorization server key |
| POST | /api/v1/authorizationServers/{authServerId}/credentials/lifecycle/keyRotate | Rotate all credential keys |
| POST | /api/v1/authorizationServers/{authServerId}/lifecycle/activate | Activate an authorization server |
| POST | /api/v1/authorizationServers/{authServerId}/lifecycle/deactivate | Deactivate an authorization server |
| GET | /api/v1/authorizationServers/{authServerId}/policies | List all policies |
| POST | /api/v1/authorizationServers/{authServerId}/policies | Create a policy |
| GET | /api/v1/authorizationServers/{authServerId}/policies/{policyId} | Retrieve a policy |
| PUT | /api/v1/authorizationServers/{authServerId}/policies/{policyId} | Replace a policy |
| DELETE | /api/v1/authorizationServers/{authServerId}/policies/{policyId} | Delete a policy |
| POST | /api/v1/authorizationServers/{authServerId}/policies/{policyId}/lifecycle/activate | Activate a policy |
| POST | /api/v1/authorizationServers/{authServerId}/policies/{policyId}/lifecycle/deactivate | Deactivate a policy |
| GET | /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules | List all policy rules |
| POST | /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules | Create a policy rule |
| GET | /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules/{ruleId} | Retrieve a policy rule |
| PUT | /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules/{ruleId} | Replace a policy rule |
| DELETE | /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules/{ruleId} | Delete a policy rule |
| POST | /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules/{ruleId}/lifecycle/activate | Activate a policy rule |
| POST | /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules/{ruleId}/lifecycle/deactivate | Deactivate a policy rule |
| GET | /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys | List all Custom Authorization Server Public JSON Web Keys |
| POST | /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys | Add a JSON Web Key |
| GET | /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys/{keyId} | Retrieve a Custom Authorization Server Public JSON Web Key |
| DELETE | /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys/{keyId} | Delete a Custom Authorization Server Public JSON Web Key |
| POST | /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys/{keyId}/lifecycle/activate | Activate a Custom Authorization Server Public JSON Web Key |
| POST | /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys/{keyId}/lifecycle/deactivate | Deactivate a Custom Authorization Server Public JSON Web Key |
| GET | /api/v1/authorizationServers/{authServerId}/scopes | List all custom token scopes |
| POST | /api/v1/authorizationServers/{authServerId}/scopes | Create a custom token scope |
| GET | /api/v1/authorizationServers/{authServerId}/scopes/{scopeId} | Retrieve a custom token scope |
| PUT | /api/v1/authorizationServers/{authServerId}/scopes/{scopeId} | Replace a custom token scope |
| DELETE | /api/v1/authorizationServers/{authServerId}/scopes/{scopeId} | Delete a custom token scope |
| GET | /api/v1/behaviors | List all behavior detection rules |
| POST | /api/v1/behaviors | Create a behavior detection rule |
| GET | /api/v1/behaviors/{behaviorId} | Retrieve a behavior detection rule |
| PUT | /api/v1/behaviors/{behaviorId} | Replace a behavior detection rule |
| DELETE | /api/v1/behaviors/{behaviorId} | Delete a behavior detection rule |
| POST | /api/v1/behaviors/{behaviorId}/lifecycle/activate | Activate a behavior detection rule |
| POST | /api/v1/behaviors/{behaviorId}/lifecycle/deactivate | Deactivate a behavior detection rule |
| GET | /api/v1/brands | List all brands |
| POST | /api/v1/brands | Create a brand |
| GET | /api/v1/brands/{brandId} | Retrieve a brand |
| PUT | /api/v1/brands/{brandId} | Replace a brand |
| DELETE | /api/v1/brands/{brandId} | Delete a brand |
| GET | /api/v1/brands/{brandId}/domains | List all domains associated with a brand |
| GET | /api/v1/brands/{brandId}/pages/error | Retrieve the error page sub-resources |
| GET | /api/v1/brands/{brandId}/pages/error/customized | Retrieve the customized error page |
| PUT | /api/v1/brands/{brandId}/pages/error/customized | Replace the customized error page |
| DELETE | /api/v1/brands/{brandId}/pages/error/customized | Delete the customized error page |
| GET | /api/v1/brands/{brandId}/pages/error/default | Retrieve the default error page |
| GET | /api/v1/brands/{brandId}/pages/error/preview | Retrieve the preview error page preview |
| PUT | /api/v1/brands/{brandId}/pages/error/preview | Replace the preview error page |
| DELETE | /api/v1/brands/{brandId}/pages/error/preview | Delete the preview error page |
| GET | /api/v1/brands/{brandId}/pages/sign-in | Retrieve the sign-in page sub-resources |
| GET | /api/v1/brands/{brandId}/pages/sign-in/customized | Retrieve the customized sign-in page |
| PUT | /api/v1/brands/{brandId}/pages/sign-in/customized | Replace the customized sign-in page |
| DELETE | /api/v1/brands/{brandId}/pages/sign-in/customized | Delete the customized sign-in page |
| GET | /api/v1/brands/{brandId}/pages/sign-in/default | Retrieve the default sign-in page |
| GET | /api/v1/brands/{brandId}/pages/sign-in/preview | Retrieve the preview sign-in page preview |
| PUT | /api/v1/brands/{brandId}/pages/sign-in/preview | Replace the preview sign-in page |
| DELETE | /api/v1/brands/{brandId}/pages/sign-in/preview | Delete the preview sign-in page |
| GET | /api/v1/brands/{brandId}/pages/sign-in/widget-versions | List all Sign-In Widget versions |
| GET | /api/v1/brands/{brandId}/pages/sign-out/customized | Retrieve the sign-out page settings |
| PUT | /api/v1/brands/{brandId}/pages/sign-out/customized | Replace the sign-out page settings |
| GET | /api/v1/brands/{brandId}/templates/email | List all email templates |
| GET | /api/v1/brands/{brandId}/templates/email/{templateName} | Retrieve an email template |
| GET | /api/v1/brands/{brandId}/templates/email/{templateName}/customizations | List all email customizations |
| POST | /api/v1/brands/{brandId}/templates/email/{templateName}/customizations | Create an email customization |
| DELETE | /api/v1/brands/{brandId}/templates/email/{templateName}/customizations | Delete all email customizations |
| GET | /api/v1/brands/{brandId}/templates/email/{templateName}/customizations/{customizationId} | Retrieve an email customization |
| PUT | /api/v1/brands/{brandId}/templates/email/{templateName}/customizations/{customizationId} | Replace an email customization |
| DELETE | /api/v1/brands/{brandId}/templates/email/{templateName}/customizations/{customizationId} | Delete an email customization |
| GET | /api/v1/brands/{brandId}/templates/email/{templateName}/customizations/{customizationId}/preview | Retrieve a preview of an email customization |
| GET | /api/v1/brands/{brandId}/templates/email/{templateName}/default-content | Retrieve an email template default content |
| GET | /api/v1/brands/{brandId}/templates/email/{templateName}/default-content/preview | Retrieve a preview of the email template default content |
| GET | /api/v1/brands/{brandId}/templates/email/{templateName}/settings | Retrieve the email template settings |
| PUT | /api/v1/brands/{brandId}/templates/email/{templateName}/settings | Replace the email template settings |
| POST | /api/v1/brands/{brandId}/templates/email/{templateName}/test | Send a test email |
| GET | /api/v1/brands/{brandId}/themes | List all themes |
| GET | /api/v1/brands/{brandId}/themes/{themeId} | Retrieve a theme |
| PUT | /api/v1/brands/{brandId}/themes/{themeId} | Replace a theme |
| POST | /api/v1/brands/{brandId}/themes/{themeId}/background-image | Upload the background image |
| DELETE | /api/v1/brands/{brandId}/themes/{themeId}/background-image | Delete the background image |
| POST | /api/v1/brands/{brandId}/themes/{themeId}/favicon | Upload the favicon |
| DELETE | /api/v1/brands/{brandId}/themes/{themeId}/favicon | Delete the favicon |
| POST | /api/v1/brands/{brandId}/themes/{themeId}/logo | Upload the logo |
| DELETE | /api/v1/brands/{brandId}/themes/{themeId}/logo | Delete the logo |
| GET | /api/v1/brands/{brandId}/well-known-uris | Retrieve all the well-known URIs |
| GET | /api/v1/brands/{brandId}/well-known-uris/{path} | Retrieve the well-known URI of a specific brand |
| GET | /api/v1/brands/{brandId}/well-known-uris/{path}/customized | Retrieve the customized content of the specified well-known URI |
| PUT | /api/v1/brands/{brandId}/well-known-uris/{path}/customized | Replace the customized well-known URI of the specific path |
| GET | /api/v1/captchas | List all CAPTCHA instances |
| POST | /api/v1/captchas | Create a CAPTCHA instance |
| GET | /api/v1/captchas/{captchaId} | Retrieve a CAPTCHA instance |
| POST | /api/v1/captchas/{captchaId} | Update a CAPTCHA instance |
| PUT | /api/v1/captchas/{captchaId} | Replace a CAPTCHA instance |
| DELETE | /api/v1/captchas/{captchaId} | Delete a CAPTCHA instance |
| GET | /api/v1/device-assurances | List all device assurance policies |
| POST | /api/v1/device-assurances | Create a device assurance policy |
| GET | /api/v1/device-assurances/{deviceAssuranceId} | Retrieve a device assurance policy |
| PUT | /api/v1/device-assurances/{deviceAssuranceId} | Replace a device assurance policy |
| DELETE | /api/v1/device-assurances/{deviceAssuranceId} | Delete a device assurance policy |
| GET | /api/v1/device-integrations | List all device integrations |
| GET | /api/v1/device-integrations/{deviceIntegrationId} | Retrieve a device integration |
| POST | /api/v1/device-integrations/{deviceIntegrationId}/lifecycle/activate | Activate a device integration |
| POST | /api/v1/device-integrations/{deviceIntegrationId}/lifecycle/deactivate | Deactivate a device integration |
| GET | /api/v1/device-posture-checks | List all device posture checks |
| POST | /api/v1/device-posture-checks | Create a device posture check |
| GET | /api/v1/device-posture-checks/default | List all default device posture checks |
| GET | /api/v1/device-posture-checks/{postureCheckId} | Retrieve a device posture check |
| PUT | /api/v1/device-posture-checks/{postureCheckId} | Replace a device posture check |
| DELETE | /api/v1/device-posture-checks/{postureCheckId} | Delete a device posture check |
| GET | /api/v1/devices | List all devices |
| GET | /api/v1/devices/{deviceId} | Retrieve a device |
| DELETE | /api/v1/devices/{deviceId} | Delete a device |
| POST | /api/v1/devices/{deviceId}/lifecycle/activate | Activate a device |
| POST | /api/v1/devices/{deviceId}/lifecycle/deactivate | Deactivate a device |
| POST | /api/v1/devices/{deviceId}/lifecycle/suspend | Suspend a Device |
| POST | /api/v1/devices/{deviceId}/lifecycle/unsuspend | Unsuspend a Device |
| GET | /api/v1/devices/{deviceId}/users | List all users for a device |
| POST | /api/v1/directories/{appInstanceId}/groups/modify | Update an Active Directory group membership |
| GET | /api/v1/domains | List all Custom Domains |
| POST | /api/v1/domains | Create a Custom Domain |
| GET | /api/v1/domains/{domainId} | Retrieve a custom domain |
| PUT | /api/v1/domains/{domainId} | Replace a custom domain's brand |
| DELETE | /api/v1/domains/{domainId} | Delete a custom domain |
| PUT | /api/v1/domains/{domainId}/certificate | Upsert the custom domain's certificate |
| POST | /api/v1/domains/{domainId}/verify | Verify a custom domain |
| GET | /api/v1/email-domains | List all email domains |
| POST | /api/v1/email-domains | Create an email domain |
| GET | /api/v1/email-domains/{emailDomainId} | Retrieve an email domain |
| PUT | /api/v1/email-domains/{emailDomainId} | Replace an email domain |
| DELETE | /api/v1/email-domains/{emailDomainId} | Delete an email domain |
| POST | /api/v1/email-domains/{emailDomainId}/verify | Verify an email domain |
| GET | /api/v1/email-servers | List all enrolled SMTP servers |
| POST | /api/v1/email-servers | Create a custom SMTP server |
| GET | /api/v1/email-servers/{emailServerId} | Retrieve an SMTP server configuration |
| PATCH | /api/v1/email-servers/{emailServerId} | Update an SMTP server configuration |
| DELETE | /api/v1/email-servers/{emailServerId} | Delete an SMTP server configuration |
| POST | /api/v1/email-servers/{emailServerId}/test | Test an SMTP server configuration |
| GET | /api/v1/eventHooks | List all event hooks |
| POST | /api/v1/eventHooks | Create an event hook |
| GET | /api/v1/eventHooks/{eventHookId} | Retrieve an event hook |
| PUT | /api/v1/eventHooks/{eventHookId} | Replace an event hook |
| DELETE | /api/v1/eventHooks/{eventHookId} | Delete an event hook |
| POST | /api/v1/eventHooks/{eventHookId}/lifecycle/activate | Activate an event hook |
| POST | /api/v1/eventHooks/{eventHookId}/lifecycle/deactivate | Deactivate an event hook |
| POST | /api/v1/eventHooks/{eventHookId}/lifecycle/verify | Verify an event hook |
| GET | /api/v1/features | List all features |
| GET | /api/v1/features/{featureId} | Retrieve a feature |
| GET | /api/v1/features/{featureId}/dependencies | List all dependencies |
| GET | /api/v1/features/{featureId}/dependents | List all dependents |
| POST | /api/v1/features/{featureId}/{lifecycle} | Update a feature lifecycle |
| GET | /api/v1/first-party-app-settings/{appName} | Retrieve the Okta application settings |
| PUT | /api/v1/first-party-app-settings/{appName} | Replace the Okta application settings |
| GET | /api/v1/groups | List all groups |
| POST | /api/v1/groups | Add a group |
| GET | /api/v1/groups/rules | List all group rules |
| POST | /api/v1/groups/rules | Create a group rule |
| GET | /api/v1/groups/rules/{groupRuleId} | Retrieve a group rule |
| PUT | /api/v1/groups/rules/{groupRuleId} | Replace a group rule |
| DELETE | /api/v1/groups/rules/{groupRuleId} | Delete a group rule |
| POST | /api/v1/groups/rules/{groupRuleId}/lifecycle/activate | Activate a group rule |
| POST | /api/v1/groups/rules/{groupRuleId}/lifecycle/deactivate | Deactivate a group rule |
| GET | /api/v1/groups/{groupId} | Retrieve a group |
| PUT | /api/v1/groups/{groupId} | Replace a group |
| DELETE | /api/v1/groups/{groupId} | Delete a group |
| GET | /api/v1/groups/{groupId}/apps | List all assigned apps |
| GET | /api/v1/groups/{groupId}/owners | List all group owners |
| POST | /api/v1/groups/{groupId}/owners | Assign a group owner |
| DELETE | /api/v1/groups/{groupId}/owners/{ownerId} | Delete a group owner |
| GET | /api/v1/groups/{groupId}/roles | List all group role assignments |
| POST | /api/v1/groups/{groupId}/roles | Assign a role to a group |
| GET | /api/v1/groups/{groupId}/roles/{roleAssignmentId} | Retrieve a group role assignment |
| DELETE | /api/v1/groups/{groupId}/roles/{roleAssignmentId} | Unassign a group role |
| GET | /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/catalog/apps | List all group role app targets |
| PUT | /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName} | Assign a group role app target |
| DELETE | /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName} | Unassign a group role app target |
| PUT | /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId} | Assign a group role app instance target |
| DELETE | /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId} | Unassign a group role app instance target |
| GET | /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/groups | List all group role group targets |
| PUT | /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/groups/{targetGroupId} | Assign a group role group target |
| DELETE | /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/groups/{targetGroupId} | Unassign a group role group target |
| GET | /api/v1/groups/{groupId}/users | List all member users |
| PUT | /api/v1/groups/{groupId}/users/{userId} | Assign a user to a group |
| DELETE | /api/v1/groups/{groupId}/users/{userId} | Unassign a user from a group |
| GET | /api/v1/hook-keys | List all keys |
| POST | /api/v1/hook-keys | Create a key |
| GET | /api/v1/hook-keys/public/{keyId} | Retrieve a public key |
| GET | /api/v1/hook-keys/{id} | Retrieve a key by ID |
| PUT | /api/v1/hook-keys/{id} | Replace a key |
| DELETE | /api/v1/hook-keys/{id} | Delete a key |
| GET | /api/v1/iam/assignees/users | List all users with role assignments |
| GET | /api/v1/iam/governance/bundles | List all governance bundles for the Admin Console |
| POST | /api/v1/iam/governance/bundles | Create a governance bundle for the Admin Console in RAMP |
| GET | /api/v1/iam/governance/bundles/{bundleId} | Retrieve a governance bundle from RAMP |
| PUT | /api/v1/iam/governance/bundles/{bundleId} | Replace a governance bundle in RAMP |
| DELETE | /api/v1/iam/governance/bundles/{bundleId} | Delete a governance bundle from RAMP |
| GET | /api/v1/iam/governance/bundles/{bundleId}/entitlements | List all entitlements for a governance bundle |
| GET | /api/v1/iam/governance/bundles/{bundleId}/entitlements/{entitlementId}/values | List all entitlement values for a bundle entitlement |
| GET | /api/v1/iam/governance/optIn | Retrieve the opt-in status from RAMP |
| POST | /api/v1/iam/governance/optIn | Opt in the Admin Console to RAMP |
| POST | /api/v1/iam/governance/optOut | Opt out the Admin Console from RAMP |
| GET | /api/v1/iam/resource-sets | List all resource sets |
| POST | /api/v1/iam/resource-sets | Create a resource set |
| GET | /api/v1/iam/resource-sets/{resourceSetIdOrLabel} | Retrieve a resource set |
| PUT | /api/v1/iam/resource-sets/{resourceSetIdOrLabel} | Replace a resource set |
| DELETE | /api/v1/iam/resource-sets/{resourceSetIdOrLabel} | Delete a resource set |
| GET | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings | List all role resource set bindings |
| POST | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings | Create a role resource set binding |
| GET | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings/{roleIdOrLabel} | Retrieve a role resource set binding |
| DELETE | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings/{roleIdOrLabel} | Delete a role resource set binding |
| GET | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings/{roleIdOrLabel}/members | List all role resource set binding members |
| PATCH | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings/{roleIdOrLabel}/members | Add more role resource set binding members |
| GET | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings/{roleIdOrLabel}/members/{memberId} | Retrieve a role resource set binding member |
| DELETE | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings/{roleIdOrLabel}/members/{memberId} | Unassign a role resource set binding member |
| GET | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/resources | List all resource set resources |
| POST | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/resources | Add a resource set resource with conditions |
| PATCH | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/resources | Add more resources to a resource set |
| GET | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/resources/{resourceId} | Retrieve a resource set resource |
| PUT | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/resources/{resourceId} | Replace the resource set resource conditions |
| DELETE | /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/resources/{resourceId} | Delete a resource set resource |
| GET | /api/v1/iam/roles | List all custom roles |
| POST | /api/v1/iam/roles | Create a custom role |
| GET | /api/v1/iam/roles/{roleIdOrLabel} | Retrieve a role |
| PUT | /api/v1/iam/roles/{roleIdOrLabel} | Replace a custom role |
| DELETE | /api/v1/iam/roles/{roleIdOrLabel} | Delete a custom role |
| GET | /api/v1/iam/roles/{roleIdOrLabel}/permissions | List all custom role permissions |
| GET | /api/v1/iam/roles/{roleIdOrLabel}/permissions/{permissionType} | Retrieve a custom role permission |
| POST | /api/v1/iam/roles/{roleIdOrLabel}/permissions/{permissionType} | Create a custom role permission |
| PUT | /api/v1/iam/roles/{roleIdOrLabel}/permissions/{permissionType} | Replace a custom role permission |
| DELETE | /api/v1/iam/roles/{roleIdOrLabel}/permissions/{permissionType} | Delete a custom role permission |
| GET | /api/v1/identity-sources/{identitySourceId}/sessions | List all identity source sessions |
| POST | /api/v1/identity-sources/{identitySourceId}/sessions | Create an identity source session |
| GET | /api/v1/identity-sources/{identitySourceId}/sessions/{sessionId} | Retrieve an identity source session |
| DELETE | /api/v1/identity-sources/{identitySourceId}/sessions/{sessionId} | Delete an identity source session |
| POST | /api/v1/identity-sources/{identitySourceId}/sessions/{sessionId}/bulk-delete | Upload the data to be deleted in Okta |
| POST | /api/v1/identity-sources/{identitySourceId}/sessions/{sessionId}/bulk-upsert | Upload the data to be upserted in Okta |
| POST | /api/v1/identity-sources/{identitySourceId}/sessions/{sessionId}/start-import | Start the import from the identity source |
| GET | /api/v1/idps | List all IdPs |
| POST | /api/v1/idps | Create an IdP |
| GET | /api/v1/idps/credentials/keys | List all IdP key credentials |
| POST | /api/v1/idps/credentials/keys | Create an IdP key credential |
| GET | /api/v1/idps/credentials/keys/{kid} | Retrieve an IdP key credential |
| PUT | /api/v1/idps/credentials/keys/{kid} | Replace an IdP key credential |
| DELETE | /api/v1/idps/credentials/keys/{kid} | Delete an IdP key credential |
| GET | /api/v1/idps/{idpId} | Retrieve an IdP |
| PUT | /api/v1/idps/{idpId} | Replace an IdP |
| DELETE | /api/v1/idps/{idpId} | Delete an IdP |
| GET | /api/v1/idps/{idpId}/credentials/csrs | List all certificate signing requests |
| POST | /api/v1/idps/{idpId}/credentials/csrs | Generate a certificate signing request |
| GET | /api/v1/idps/{idpId}/credentials/csrs/{idpCsrId} | Retrieve a certificate signing request |
| DELETE | /api/v1/idps/{idpId}/credentials/csrs/{idpCsrId} | Revoke a certificate signing request |
| POST | /api/v1/idps/{idpId}/credentials/csrs/{idpCsrId}/lifecycle/publish | Publish a certificate signing request |
| GET | /api/v1/idps/{idpId}/credentials/keys | List all signing key credentials for IdP |
| GET | /api/v1/idps/{idpId}/credentials/keys/active | List the active signing key credential for IdP |
| POST | /api/v1/idps/{idpId}/credentials/keys/generate | Generate a new signing key credential for IdP |
| GET | /api/v1/idps/{idpId}/credentials/keys/{kid} | Retrieve a signing key credential for IdP |
| POST | /api/v1/idps/{idpId}/credentials/keys/{kid}/clone | Clone a signing key credential for IdP |
| POST | /api/v1/idps/{idpId}/lifecycle/activate | Activate an IdP |
| POST | /api/v1/idps/{idpId}/lifecycle/deactivate | Deactivate an IdP |
| GET | /api/v1/idps/{idpId}/users | List all users for IdP |
| GET | /api/v1/idps/{idpId}/users/{userId} | Retrieve a user for IdP |
| POST | /api/v1/idps/{idpId}/users/{userId} | Link a user to IdP |
| DELETE | /api/v1/idps/{idpId}/users/{userId} | Unlink a user from IdP |
| GET | /api/v1/idps/{idpId}/users/{userId}/credentials/tokens | List all tokens from OIDC IdP |
| GET | /api/v1/inlineHooks | List all inline hooks |
| POST | /api/v1/inlineHooks | Create an inline hook |
| GET | /api/v1/inlineHooks/{inlineHookId} | Retrieve an inline hook |
| POST | /api/v1/inlineHooks/{inlineHookId} | Update an inline hook |
| PUT | /api/v1/inlineHooks/{inlineHookId} | Replace an inline hook |
| DELETE | /api/v1/inlineHooks/{inlineHookId} | Delete an inline hook |
| POST | /api/v1/inlineHooks/{inlineHookId}/execute | Execute an inline hook |
| POST | /api/v1/inlineHooks/{inlineHookId}/lifecycle/activate | Activate an inline hook |
| POST | /api/v1/inlineHooks/{inlineHookId}/lifecycle/deactivate | Deactivate an inline hook |
| GET | /api/v1/logStreams | List all log streams |
| POST | /api/v1/logStreams | Create a log stream |
| GET | /api/v1/logStreams/{logStreamId} | Retrieve a log stream |
| PUT | /api/v1/logStreams/{logStreamId} | Replace a log stream |
| DELETE | /api/v1/logStreams/{logStreamId} | Delete a log stream |
| POST | /api/v1/logStreams/{logStreamId}/lifecycle/activate | Activate a log stream |
| POST | /api/v1/logStreams/{logStreamId}/lifecycle/deactivate | Deactivate a log stream |
| GET | /api/v1/logs | List all System Log events |
| GET | /api/v1/mappings | List all profile mappings |
| GET | /api/v1/mappings/{mappingId} | Retrieve a profile mapping |
| POST | /api/v1/mappings/{mappingId} | Update a profile mapping |
| GET | /api/v1/meta/schemas/apps/{appId}/default | Retrieve the default app user schema for an app |
| POST | /api/v1/meta/schemas/apps/{appId}/default | Update the app user profile schema for an app |
| GET | /api/v1/meta/schemas/group/default | Retrieve the default group schema |
| POST | /api/v1/meta/schemas/group/default | Update the group profile schema |
| GET | /api/v1/meta/schemas/logStream | List the log stream schemas |
| GET | /api/v1/meta/schemas/logStream/{logStreamType} | Retrieve the log stream schema for the schema type |
| GET | /api/v1/meta/schemas/user/linkedObjects | List all linked object definitions |
| POST | /api/v1/meta/schemas/user/linkedObjects | Create a linked object definition |
| GET | /api/v1/meta/schemas/user/linkedObjects/{linkedObjectName} | Retrieve a linked object definition |
| DELETE | /api/v1/meta/schemas/user/linkedObjects/{linkedObjectName} | Delete a linked object definition |
| GET | /api/v1/meta/schemas/user/{schemaId} | Retrieve a user schema |
| POST | /api/v1/meta/schemas/user/{schemaId} | Update a user schema |
| GET | /api/v1/meta/types/user | List all user types |
| POST | /api/v1/meta/types/user | Create a user type |
| GET | /api/v1/meta/types/user/{typeId} | Retrieve a user type |
| POST | /api/v1/meta/types/user/{typeId} | Update a user type |
| PUT | /api/v1/meta/types/user/{typeId} | Replace a user type |
| DELETE | /api/v1/meta/types/user/{typeId} | Delete a user type |
| GET | /api/v1/meta/uischemas | List all UI schemas |
| POST | /api/v1/meta/uischemas | Create a UI schema |
| GET | /api/v1/meta/uischemas/{id} | Retrieve a UI schema |
| PUT | /api/v1/meta/uischemas/{id} | Replace a UI schema |
| DELETE | /api/v1/meta/uischemas/{id} | Delete a UI schema |
| GET | /api/v1/org | Retrieve the Org general settings |
| POST | /api/v1/org | Update the Org general settings |
| PUT | /api/v1/org | Replace the Org general settings |
| GET | /api/v1/org/captcha | Retrieve the org-wide CAPTCHA settings |
| PUT | /api/v1/org/captcha | Replace the org-wide CAPTCHA settings |
| DELETE | /api/v1/org/captcha | Delete the org-wide CAPTCHA settings |
| GET | /api/v1/org/contacts | List all org contact types |
| GET | /api/v1/org/contacts/{contactType} | Retrieve the contact type user |
| PUT | /api/v1/org/contacts/{contactType} | Replace the contact type user |
| POST | /api/v1/org/email/bounces/remove-list | Remove bounced emails |
| GET | /api/v1/org/factors/yubikey_token/tokens | List all YubiKey OTP tokens |
| POST | /api/v1/org/factors/yubikey_token/tokens | Upload a YubiKey OTP seed |
| GET | /api/v1/org/factors/yubikey_token/tokens/{tokenId} | Retrieve a YubiKey OTP token |
| POST | /api/v1/org/logo | Upload the org logo |
| GET | /api/v1/org/orgSettings/thirdPartyAdminSetting | Retrieve the org third-party admin setting |
| POST | /api/v1/org/orgSettings/thirdPartyAdminSetting | Update the org third-party admin setting |
| GET | /api/v1/org/preferences | Retrieve the org preferences |
| POST | /api/v1/org/preferences/hideEndUserFooter | Set the hide dashboard footer preference |
| POST | /api/v1/org/preferences/showEndUserFooter | Set the show dashboard footer preference |
| GET | /api/v1/org/privacy/aerial | Retrieve Okta Aerial consent for your org |
| POST | /api/v1/org/privacy/aerial/grant | Grant Okta Aerial access to your org |
| POST | /api/v1/org/privacy/aerial/revoke | Revoke Okta Aerial access to your org |
| GET | /api/v1/org/privacy/oktaCommunication | Retrieve the Okta communication settings |
| POST | /api/v1/org/privacy/oktaCommunication/optIn | Opt in to Okta user communication emails |
| POST | /api/v1/org/privacy/oktaCommunication/optOut | Opt out of Okta user communication emails |
| GET | /api/v1/org/privacy/oktaSupport | Retrieve the Okta Support settings |
| GET | /api/v1/org/privacy/oktaSupport/cases | List all Okta Support cases |
| PATCH | /api/v1/org/privacy/oktaSupport/cases/{caseNumber} | Update an Okta Support case |
| POST | /api/v1/org/privacy/oktaSupport/extend | Extend Okta Support access |
| POST | /api/v1/org/privacy/oktaSupport/grant | Grant Okta Support access |
| POST | /api/v1/org/privacy/oktaSupport/revoke | Revoke Okta Support access |
| GET | /api/v1/org/settings/autoAssignAdminAppSetting | Retrieve the Okta Admin Console assignment setting |
| POST | /api/v1/org/settings/autoAssignAdminAppSetting | Update the Okta Admin Console assignment setting |
| GET | /api/v1/org/settings/clientPrivilegesSetting | Retrieve the default public client app role setting |
| PUT | /api/v1/org/settings/clientPrivilegesSetting | Assign the default public client app role setting |
| POST | /api/v1/orgs | Create an org |
| GET | /api/v1/policies | List all policies |
| POST | /api/v1/policies | Create a policy |
| POST | /api/v1/policies/simulate | Create a policy simulation |
| GET | /api/v1/policies/{policyId} | Retrieve a policy |
| PUT | /api/v1/policies/{policyId} | Replace a policy |
| DELETE | /api/v1/policies/{policyId} | Delete a policy |
| GET | /api/v1/policies/{policyId}/app | List all apps mapped to a policy |
| POST | /api/v1/policies/{policyId}/clone | Clone an existing policy |
| POST | /api/v1/policies/{policyId}/lifecycle/activate | Activate a policy |
| POST | /api/v1/policies/{policyId}/lifecycle/deactivate | Deactivate a policy |
| GET | /api/v1/policies/{policyId}/mappings | List all resources mapped to a policy |
| POST | /api/v1/policies/{policyId}/mappings | Map a resource to a policy |
| GET | /api/v1/policies/{policyId}/mappings/{mappingId} | Retrieve a policy resource mapping |
| DELETE | /api/v1/policies/{policyId}/mappings/{mappingId} | Delete a policy resource mapping |
| GET | /api/v1/policies/{policyId}/rules | List all policy rules |
| POST | /api/v1/policies/{policyId}/rules | Create a policy rule |
| GET | /api/v1/policies/{policyId}/rules/{ruleId} | Retrieve a policy rule |
| PUT | /api/v1/policies/{policyId}/rules/{ruleId} | Replace a policy rule |
| DELETE | /api/v1/policies/{policyId}/rules/{ruleId} | Delete a policy rule |
| POST | /api/v1/policies/{policyId}/rules/{ruleId}/lifecycle/activate | Activate a policy rule |
| POST | /api/v1/policies/{policyId}/rules/{ruleId}/lifecycle/deactivate | Deactivate a policy rule |
| GET | /api/v1/principal-rate-limits | List all principal rate limits |
| POST | /api/v1/principal-rate-limits | Create a principal rate limit |
| GET | /api/v1/principal-rate-limits/{principalRateLimitId} | Retrieve a principal rate limit |
| PUT | /api/v1/principal-rate-limits/{principalRateLimitId} | Replace a principal rate limit |
| GET | /api/v1/push-providers | List all push providers |
| POST | /api/v1/push-providers | Create a push provider |
| GET | /api/v1/push-providers/{pushProviderId} | Retrieve a push provider |
| PUT | /api/v1/push-providers/{pushProviderId} | Replace a push provider |
| DELETE | /api/v1/push-providers/{pushProviderId} | Delete a push provider |
| GET | /api/v1/rate-limit-settings/admin-notifications | Retrieve the rate limit admin notification settings |
| PUT | /api/v1/rate-limit-settings/admin-notifications | Replace the rate limit admin notification settings |
| GET | /api/v1/rate-limit-settings/per-client | Retrieve the per-client rate limit settings |
| PUT | /api/v1/rate-limit-settings/per-client | Replace the per-client rate limit settings |
| GET | /api/v1/rate-limit-settings/warning-threshold | Retrieve the rate limit warning threshold percentage |
| PUT | /api/v1/rate-limit-settings/warning-threshold | Replace the rate limit warning threshold percentage |
| GET | /api/v1/realm-assignments | List all realm assignments |
| POST | /api/v1/realm-assignments | Create a realm assignment |
| GET | /api/v1/realm-assignments/operations | List all realm assignment operations |
| POST | /api/v1/realm-assignments/operations | Execute a realm assignment |
| GET | /api/v1/realm-assignments/{assignmentId} | Retrieve a realm assignment |
| PUT | /api/v1/realm-assignments/{assignmentId} | Replace a realm assignment |
| DELETE | /api/v1/realm-assignments/{assignmentId} | Delete a realm assignment |
| POST | /api/v1/realm-assignments/{assignmentId}/lifecycle/activate | Activate a realm assignment |
| POST | /api/v1/realm-assignments/{assignmentId}/lifecycle/deactivate | Deactivate a realm assignment |
| GET | /api/v1/realms | List all realms |
| POST | /api/v1/realms | Create a realm |
| GET | /api/v1/realms/{realmId} | Retrieve a realm |
| PUT | /api/v1/realms/{realmId} | Replace the realm profile |
| DELETE | /api/v1/realms/{realmId} | Delete a realm |
| POST | /api/v1/risk/events/ip | Send multiple risk events |
| GET | /api/v1/risk/providers | List all risk providers |
| POST | /api/v1/risk/providers | Create a risk provider |
| GET | /api/v1/risk/providers/{riskProviderId} | Retrieve a risk provider |
| PUT | /api/v1/risk/providers/{riskProviderId} | Replace a risk provider |
| DELETE | /api/v1/risk/providers/{riskProviderId} | Delete a risk provider |
| GET | /api/v1/roles/{roleRef}/subscriptions | List all subscriptions for a role |
| GET | /api/v1/roles/{roleRef}/subscriptions/{notificationType} | Retrieve a subscription for a role |
| POST | /api/v1/roles/{roleRef}/subscriptions/{notificationType}/subscribe | Subscribe a role to a specific notification type |
| POST | /api/v1/roles/{roleRef}/subscriptions/{notificationType}/unsubscribe | Unsubscribe a role from a specific notification type |
| GET | /api/v1/security-events-providers | List all security events providers |
| POST | /api/v1/security-events-providers | Create a security events provider |
| GET | /api/v1/security-events-providers/{securityEventProviderId} | Retrieve the security events provider |
| PUT | /api/v1/security-events-providers/{securityEventProviderId} | Replace a security events provider |
| DELETE | /api/v1/security-events-providers/{securityEventProviderId} | Delete a security events provider |
| POST | /api/v1/security-events-providers/{securityEventProviderId}/lifecycle/activate | Activate a security events provider |
| POST | /api/v1/security-events-providers/{securityEventProviderId}/lifecycle/deactivate | Deactivate a security events provider |
| POST | /api/v1/sessions | Create a session with session token |
| GET | /api/v1/sessions/me | Retrieve the current session |
| DELETE | /api/v1/sessions/me | Close the current session |
| POST | /api/v1/sessions/me/lifecycle/refresh | Refresh the current session |
| GET | /api/v1/sessions/{sessionId} | Retrieve a session |
| DELETE | /api/v1/sessions/{sessionId} | Revoke a session |
| POST | /api/v1/sessions/{sessionId}/lifecycle/refresh | Refresh a session |
| GET | /api/v1/ssf/stream | Retrieve the SSF stream configuration(s) |
| POST | /api/v1/ssf/stream | Create an SSF stream |
| PUT | /api/v1/ssf/stream | Replace an SSF stream |
| PATCH | /api/v1/ssf/stream | Update an SSF stream |
| DELETE | /api/v1/ssf/stream | Delete an SSF stream |
| GET | /api/v1/ssf/stream/status | Retrieve the SSF Stream status |
| POST | /api/v1/ssf/stream/verification | Verify an SSF stream |
| GET | /api/v1/templates/sms | List all SMS templates |
| POST | /api/v1/templates/sms | Create an SMS template |
| GET | /api/v1/templates/sms/{templateId} | Retrieve an SMS template |
| POST | /api/v1/templates/sms/{templateId} | Update an SMS template |
| PUT | /api/v1/templates/sms/{templateId} | Replace an SMS template |
| DELETE | /api/v1/templates/sms/{templateId} | Delete an SMS template |
| GET | /api/v1/threats/configuration | Retrieve the ThreatInsight configuration |
| POST | /api/v1/threats/configuration | Update the ThreatInsight configuration |
| GET | /api/v1/trustedOrigins | List all trusted origins |
| POST | /api/v1/trustedOrigins | Create a trusted origin |
| GET | /api/v1/trustedOrigins/{trustedOriginId} | Retrieve a trusted origin |
| PUT | /api/v1/trustedOrigins/{trustedOriginId} | Replace a trusted origin |
| DELETE | /api/v1/trustedOrigins/{trustedOriginId} | Delete a trusted origin |
| POST | /api/v1/trustedOrigins/{trustedOriginId}/lifecycle/activate | Activate a trusted origin |
| POST | /api/v1/trustedOrigins/{trustedOriginId}/lifecycle/deactivate | Deactivate a trusted origin |
| GET | /api/v1/users | List all users |
| POST | /api/v1/users | Create a user |
| POST | /api/v1/users/me/lifecycle/delete_sessions | End a current user session |
| GET | /api/v1/users/{id} | Retrieve a user |
| POST | /api/v1/users/{id} | Update a user |
| PUT | /api/v1/users/{id} | Replace a user |
| DELETE | /api/v1/users/{id} | Delete a user |
| GET | /api/v1/users/{id}/appLinks | List all assigned app links |
| GET | /api/v1/users/{id}/blocks | List all user blocks |
| GET | /api/v1/users/{id}/groups | List all groups |
| GET | /api/v1/users/{id}/idps | List all IdPs for user |
| POST | /api/v1/users/{id}/lifecycle/activate | Activate a user |
| POST | /api/v1/users/{id}/lifecycle/deactivate | Deactivate a user |
| POST | /api/v1/users/{id}/lifecycle/expire_password | Expire the password |
| POST | /api/v1/users/{id}/lifecycle/expire_password_with_temp_password | Expire the password with a temporary password |
| POST | /api/v1/users/{id}/lifecycle/reactivate | Reactivate a user |
| POST | /api/v1/users/{id}/lifecycle/reset_factors | Reset the factors |
| POST | /api/v1/users/{id}/lifecycle/reset_password | Reset a password |
| POST | /api/v1/users/{id}/lifecycle/suspend | Suspend a user |
| POST | /api/v1/users/{id}/lifecycle/unlock | Unlock a user |
| POST | /api/v1/users/{id}/lifecycle/unsuspend | Unsuspend a user |
| PUT | /api/v1/users/{userIdOrLogin}/linkedObjects/{primaryRelationshipName}/{primaryUserId} | Assign a linked object value for primary |
| GET | /api/v1/users/{userIdOrLogin}/linkedObjects/{relationshipName} | List the primary or all of the associated linked object values |
| DELETE | /api/v1/users/{userIdOrLogin}/linkedObjects/{relationshipName} | Delete a linked object value |
| GET | /api/v1/users/{userId}/authenticator-enrollments | List all authenticator enrollments |
| POST | /api/v1/users/{userId}/authenticator-enrollments/phone | Create an auto-activated Phone authenticator enrollment |
| POST | /api/v1/users/{userId}/authenticator-enrollments/tac | Create an auto-activated TAC authenticator enrollment |
| GET | /api/v1/users/{userId}/authenticator-enrollments/{enrollmentId} | Retrieve an authenticator enrollment |
| DELETE | /api/v1/users/{userId}/authenticator-enrollments/{enrollmentId} | Delete an authenticator enrollment |
| GET | /api/v1/users/{userId}/classification | Retrieve a user's classification |
| PUT | /api/v1/users/{userId}/classification | Replace the user's classification |
| GET | /api/v1/users/{userId}/clients | List all clients |
| GET | /api/v1/users/{userId}/clients/{clientId}/grants | List all grants for a client |
| DELETE | /api/v1/users/{userId}/clients/{clientId}/grants | Revoke all grants for a client |
| GET | /api/v1/users/{userId}/clients/{clientId}/tokens | List all refresh tokens for a client |
| DELETE | /api/v1/users/{userId}/clients/{clientId}/tokens | Revoke all refresh tokens for a client |
| GET | /api/v1/users/{userId}/clients/{clientId}/tokens/{tokenId} | Retrieve a refresh token for a client |
| DELETE | /api/v1/users/{userId}/clients/{clientId}/tokens/{tokenId} | Revoke a token for a client |
| POST | /api/v1/users/{userId}/credentials/change_password | Update password |
| POST | /api/v1/users/{userId}/credentials/change_recovery_question | Update recovery question |
| POST | /api/v1/users/{userId}/credentials/forgot_password | Start forgot password flow |
| POST | /api/v1/users/{userId}/credentials/forgot_password_recovery_question | Reset password with recovery question |
| GET | /api/v1/users/{userId}/devices | List all devices |
| GET | /api/v1/users/{userId}/factors | List all enrolled factors |
| POST | /api/v1/users/{userId}/factors | Enroll a factor |
| GET | /api/v1/users/{userId}/factors/catalog | List all supported factors |
| GET | /api/v1/users/{userId}/factors/questions | List all supported security questions |
| GET | /api/v1/users/{userId}/factors/{factorId} | Retrieve a factor |
| DELETE | /api/v1/users/{userId}/factors/{factorId} | Unenroll a factor |
| POST | /api/v1/users/{userId}/factors/{factorId}/lifecycle/activate | Activate a factor |
| POST | /api/v1/users/{userId}/factors/{factorId}/resend | Resend a factor enrollment |
| GET | /api/v1/users/{userId}/factors/{factorId}/transactions/{transactionId} | Retrieve a factor transaction status |
| POST | /api/v1/users/{userId}/factors/{factorId}/verify | Verify a factor |
| GET | /api/v1/users/{userId}/grants | List all user grants |
| DELETE | /api/v1/users/{userId}/grants | Revoke all user grants |
| GET | /api/v1/users/{userId}/grants/{grantId} | Retrieve a user grant |
| DELETE | /api/v1/users/{userId}/grants/{grantId} | Revoke a user grant |
| GET | /api/v1/users/{userId}/risk | Retrieve the user's risk |
| PUT | /api/v1/users/{userId}/risk | Upsert the user's risk |
| GET | /api/v1/users/{userId}/roles | List all user role assignments |
| POST | /api/v1/users/{userId}/roles | Assign a user role |
| GET | /api/v1/users/{userId}/roles/{roleAssignmentId} | Retrieve a user role assignment |
| DELETE | /api/v1/users/{userId}/roles/{roleAssignmentId} | Unassign a user role |
| GET | /api/v1/users/{userId}/roles/{roleAssignmentId}/governance | Retrieve all user role governance sources |
| GET | /api/v1/users/{userId}/roles/{roleAssignmentId}/governance/{grantId} | Retrieve a user role governance source |
| GET | /api/v1/users/{userId}/roles/{roleAssignmentId}/governance/{grantId}/resources | Retrieve the user role governance source resources |
| GET | /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/catalog/apps | List all admin role app targets |
| PUT | /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/catalog/apps | Assign all apps as target to admin role |
| PUT | /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName} | Assign an admin role app target |
| DELETE | /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName} | Unassign an admin role app target |
| PUT | /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId} | Assign an admin role app instance target |
| DELETE | /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId} | Unassign an admin role app instance target |
| GET | /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/groups | List all admin role group targets |
| PUT | /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/groups/{groupId} | Assign an admin role group target |
| DELETE | /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/groups/{groupId} | Unassign an admin role group target |
| GET | /api/v1/users/{userId}/roles/{roleIdOrEncodedRoleId}/targets | Retrieve a role target by assignment type |
| DELETE | /api/v1/users/{userId}/sessions | Revoke all user sessions |
| GET | /api/v1/users/{userId}/subscriptions | List all subscriptions for a user |
| GET | /api/v1/users/{userId}/subscriptions/{notificationType} | Retrieve a subscription for a user |
| POST | /api/v1/users/{userId}/subscriptions/{notificationType}/subscribe | Subscribe a user to a specific notification type |
| POST | /api/v1/users/{userId}/subscriptions/{notificationType}/unsubscribe | Unsubscribe a user from a specific notification type |
| GET | /api/v1/zones | List all network zones |
| POST | /api/v1/zones | Create a network zone |
| GET | /api/v1/zones/{zoneId} | Retrieve a network zone |
| PUT | /api/v1/zones/{zoneId} | Replace a network zone |
| DELETE | /api/v1/zones/{zoneId} | Delete a network zone |
| POST | /api/v1/zones/{zoneId}/lifecycle/activate | Activate a network zone |
| POST | /api/v1/zones/{zoneId}/lifecycle/deactivate | Deactivate a network zone |

### attack-protection
| Method | Path | Description |
|--------|------|-------------|
| GET | /attack-protection/api/v1/authenticator-settings | Retrieve the authenticator settings |
| PUT | /attack-protection/api/v1/authenticator-settings | Replace the authenticator settings |
| GET | /attack-protection/api/v1/user-lockout-settings | Retrieve the user lockout settings |
| PUT | /attack-protection/api/v1/user-lockout-settings | Replace the user lockout settings |

### device-access
| Method | Path | Description |
|--------|------|-------------|
| GET | /device-access/api/v1/desktop-mfa/enforce-number-matching-challenge-settings | Retrieve the Desktop MFA Enforce Number Matching Challenge org setting |
| PUT | /device-access/api/v1/desktop-mfa/enforce-number-matching-challenge-settings | Replace the Desktop MFA Enforce Number Matching Challenge org setting |
| GET | /device-access/api/v1/desktop-mfa/recovery-pin-settings | Retrieve the Desktop MFA Recovery PIN org setting |
| PUT | /device-access/api/v1/desktop-mfa/recovery-pin-settings | Replace the Desktop MFA Recovery PIN org setting |

### integrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /integrations/api/v1/api-services | List all API service integration instances |
| POST | /integrations/api/v1/api-services | Create an API service integration instance |
| GET | /integrations/api/v1/api-services/{apiServiceId} | Retrieve an API service integration instance |
| DELETE | /integrations/api/v1/api-services/{apiServiceId} | Delete an API service integration instance |
| GET | /integrations/api/v1/api-services/{apiServiceId}/credentials/secrets | List all API service integration instance secrets |
| POST | /integrations/api/v1/api-services/{apiServiceId}/credentials/secrets | Create an API service integration instance secret |
| DELETE | /integrations/api/v1/api-services/{apiServiceId}/credentials/secrets/{secretId} | Delete an API service integration instance secret |
| POST | /integrations/api/v1/api-services/{apiServiceId}/credentials/secrets/{secretId}/lifecycle/activate | Activate an API service integration instance secret |
| POST | /integrations/api/v1/api-services/{apiServiceId}/credentials/secrets/{secretId}/lifecycle/deactivate | Deactivate an API service integration instance secret |

### oauth2
| Method | Path | Description |
|--------|------|-------------|
| GET | /oauth2/v1/clients/{clientId}/roles | List all client role assignments |
| POST | /oauth2/v1/clients/{clientId}/roles | Assign a client role |
| GET | /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId} | Retrieve a client role |
| DELETE | /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId} | Unassign a client role |
| GET | /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/catalog/apps | List all client role app targets |
| PUT | /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName} | Assign a client role app target |
| DELETE | /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName} | Unassign a client role app target |
| PUT | /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId} | Assign a client role app instance target |
| DELETE | /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId} | Unassign a client role app instance target |
| GET | /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/groups | List all client role group targets |
| PUT | /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/groups/{groupId} | Assign a client role group target |
| DELETE | /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/groups/{groupId} | Unassign a client role group target |

### okta-personal-settings
| Method | Path | Description |
|--------|------|-------------|
| PUT | /okta-personal-settings/api/v1/edit-feature | Replace the Okta Personal admin settings |
| GET | /okta-personal-settings/api/v1/export-blocklists | List all blocked email domains |
| PUT | /okta-personal-settings/api/v1/export-blocklists | Replace the blocked email domains |

### privileged-access
| Method | Path | Description |
|--------|------|-------------|
| GET | /privileged-access/api/v1/service-accounts | List all app service accounts |
| POST | /privileged-access/api/v1/service-accounts | Create an app service account |
| GET | /privileged-access/api/v1/service-accounts/{id} | Retrieve an app service account |
| PATCH | /privileged-access/api/v1/service-accounts/{id} | Update an existing app service account |
| DELETE | /privileged-access/api/v1/service-accounts/{id} | Delete an app service account |

### security
| Method | Path | Description |
|--------|------|-------------|
| POST | /security/api/v1/security-events | Publish a security event token |

### webauthn-registration
| Method | Path | Description |
|--------|------|-------------|
| POST | /webauthn-registration/api/v1/activate | Activate a preregistered WebAuthn factor |
| POST | /webauthn-registration/api/v1/enroll | Enroll a preregistered WebAuthn factor |
| POST | /webauthn-registration/api/v1/initiate-fulfillment-request | Generate a fulfillment request |
| POST | /webauthn-registration/api/v1/send-pin | Send a PIN to user |
| GET | /webauthn-registration/api/v1/users/{userId}/enrollments | List all WebAuthn preregistration factors |
| DELETE | /webauthn-registration/api/v1/users/{userId}/enrollments/{authenticatorEnrollmentId} | Delete a WebAuthn preregistration factor |
| POST | /webauthn-registration/api/v1/users/{userId}/enrollments/{authenticatorEnrollmentId}/mark-error | Assign the fulfillment error status to a WebAuthn preregistration factor |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all app-authenticator-configuration?" -> GET /.well-known/app-authenticator-configuration
- "List all apple-app-site-association?" -> GET /.well-known/apple-app-site-association
- "List all assetlinks.json?" -> GET /.well-known/assetlinks.json
- "List all okta-organization?" -> GET /.well-known/okta-organization
- "List all ssf-configuration?" -> GET /.well-known/ssf-configuration
- "List all webauthn?" -> GET /.well-known/webauthn
- "List all agentPools?" -> GET /api/v1/agentPools
- "List all updates?" -> GET /api/v1/agentPools/{poolId}/updates
- "Create a update?" -> POST /api/v1/agentPools/{poolId}/updates
- "List all settings?" -> GET /api/v1/agentPools/{poolId}/updates/settings
- "Create a setting?" -> POST /api/v1/agentPools/{poolId}/updates/settings
- "Get update details?" -> GET /api/v1/agentPools/{poolId}/updates/{updateId}
- "Delete a update?" -> DELETE /api/v1/agentPools/{poolId}/updates/{updateId}
- "Create a activate?" -> POST /api/v1/agentPools/{poolId}/updates/{updateId}/activate
- "Create a deactivate?" -> POST /api/v1/agentPools/{poolId}/updates/{updateId}/deactivate
- "Create a pause?" -> POST /api/v1/agentPools/{poolId}/updates/{updateId}/pause
- "Create a resume?" -> POST /api/v1/agentPools/{poolId}/updates/{updateId}/resume
- "Create a retry?" -> POST /api/v1/agentPools/{poolId}/updates/{updateId}/retry
- "Create a stop?" -> POST /api/v1/agentPools/{poolId}/updates/{updateId}/stop
- "List all api-tokens?" -> GET /api/v1/api-tokens
- "Get api-token details?" -> GET /api/v1/api-tokens/{apiTokenId}
- "Update a api-token?" -> PUT /api/v1/api-tokens/{apiTokenId}
- "Delete a api-token?" -> DELETE /api/v1/api-tokens/{apiTokenId}
- "Search apps?" -> GET /api/v1/apps
- "Create a app?" -> POST /api/v1/apps
- "Get app details?" -> GET /api/v1/apps/{appId}
- "Update a app?" -> PUT /api/v1/apps/{appId}
- "Delete a app?" -> DELETE /api/v1/apps/{appId}
- "List all default?" -> GET /api/v1/apps/{appId}/connections/default
- "Create a default?" -> POST /api/v1/apps/{appId}/connections/default
- "List all jwks?" -> GET /api/v1/apps/{appId}/connections/default/jwks
- "Create a activate?" -> POST /api/v1/apps/{appId}/connections/default/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/apps/{appId}/connections/default/lifecycle/deactivate
- "List all csrs?" -> GET /api/v1/apps/{appId}/credentials/csrs
- "Create a csr?" -> POST /api/v1/apps/{appId}/credentials/csrs
- "Get csr details?" -> GET /api/v1/apps/{appId}/credentials/csrs/{csrId}
- "Delete a csr?" -> DELETE /api/v1/apps/{appId}/credentials/csrs/{csrId}
- "Create a publish?" -> POST /api/v1/apps/{appId}/credentials/csrs/{csrId}/lifecycle/publish
- "List all jwks?" -> GET /api/v1/apps/{appId}/credentials/jwks
- "Create a jwk?" -> POST /api/v1/apps/{appId}/credentials/jwks
- "Get jwk details?" -> GET /api/v1/apps/{appId}/credentials/jwks/{keyId}
- "Delete a jwk?" -> DELETE /api/v1/apps/{appId}/credentials/jwks/{keyId}
- "Create a activate?" -> POST /api/v1/apps/{appId}/credentials/jwks/{keyId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/apps/{appId}/credentials/jwks/{keyId}/lifecycle/deactivate
- "List all keys?" -> GET /api/v1/apps/{appId}/credentials/keys
- "Create a generate?" -> POST /api/v1/apps/{appId}/credentials/keys/generate
- "Get key details?" -> GET /api/v1/apps/{appId}/credentials/keys/{keyId}
- "Create a clone?" -> POST /api/v1/apps/{appId}/credentials/keys/{keyId}/clone
- "List all secrets?" -> GET /api/v1/apps/{appId}/credentials/secrets
- "Create a secret?" -> POST /api/v1/apps/{appId}/credentials/secrets
- "Get secret details?" -> GET /api/v1/apps/{appId}/credentials/secrets/{secretId}
- "Delete a secret?" -> DELETE /api/v1/apps/{appId}/credentials/secrets/{secretId}
- "Create a activate?" -> POST /api/v1/apps/{appId}/credentials/secrets/{secretId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/apps/{appId}/credentials/secrets/{secretId}/lifecycle/deactivate
- "List all connections?" -> GET /api/v1/apps/{appId}/cwo/connections
- "Create a connection?" -> POST /api/v1/apps/{appId}/cwo/connections
- "Get connection details?" -> GET /api/v1/apps/{appId}/cwo/connections/{connectionId}
- "Partially update a connection?" -> PATCH /api/v1/apps/{appId}/cwo/connections/{connectionId}
- "Delete a connection?" -> DELETE /api/v1/apps/{appId}/cwo/connections/{connectionId}
- "List all features?" -> GET /api/v1/apps/{appId}/features
- "Get feature details?" -> GET /api/v1/apps/{appId}/features/{featureName}
- "Update a feature?" -> PUT /api/v1/apps/{appId}/features/{featureName}
- "List all federated-claims?" -> GET /api/v1/apps/{appId}/federated-claims
- "Create a federated-claim?" -> POST /api/v1/apps/{appId}/federated-claims
- "Get federated-claim details?" -> GET /api/v1/apps/{appId}/federated-claims/{claimId}
- "Update a federated-claim?" -> PUT /api/v1/apps/{appId}/federated-claims/{claimId}
- "Delete a federated-claim?" -> DELETE /api/v1/apps/{appId}/federated-claims/{claimId}
- "List all grants?" -> GET /api/v1/apps/{appId}/grants
- "Create a grant?" -> POST /api/v1/apps/{appId}/grants
- "Get grant details?" -> GET /api/v1/apps/{appId}/grants/{grantId}
- "Delete a grant?" -> DELETE /api/v1/apps/{appId}/grants/{grantId}
- "List all mappings?" -> GET /api/v1/apps/{appId}/group-push/mappings
- "Create a mapping?" -> POST /api/v1/apps/{appId}/group-push/mappings
- "Get mapping details?" -> GET /api/v1/apps/{appId}/group-push/mappings/{mappingId}
- "Partially update a mapping?" -> PATCH /api/v1/apps/{appId}/group-push/mappings/{mappingId}
- "Delete a mapping?" -> DELETE /api/v1/apps/{appId}/group-push/mappings/{mappingId}
- "Search groups?" -> GET /api/v1/apps/{appId}/groups
- "Get group details?" -> GET /api/v1/apps/{appId}/groups/{groupId}
- "Update a group?" -> PUT /api/v1/apps/{appId}/groups/{groupId}
- "Partially update a group?" -> PATCH /api/v1/apps/{appId}/groups/{groupId}
- "Delete a group?" -> DELETE /api/v1/apps/{appId}/groups/{groupId}
- "Create a activate?" -> POST /api/v1/apps/{appId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/apps/{appId}/lifecycle/deactivate
- "Create a logo?" -> POST /api/v1/apps/{appId}/logo
- "Update a policy?" -> PUT /api/v1/apps/{appId}/policies/{policyId}
- "List all metadata?" -> GET /api/v1/apps/{appId}/sso/saml/metadata
- "List all tokens?" -> GET /api/v1/apps/{appId}/tokens
- "Get token details?" -> GET /api/v1/apps/{appId}/tokens/{tokenId}
- "Delete a token?" -> DELETE /api/v1/apps/{appId}/tokens/{tokenId}
- "Search users?" -> GET /api/v1/apps/{appId}/users
- "Create a user?" -> POST /api/v1/apps/{appId}/users
- "Get user details?" -> GET /api/v1/apps/{appId}/users/{userId}
- "Delete a user?" -> DELETE /api/v1/apps/{appId}/users/{userId}
- "Create a callback?" -> POST /api/v1/apps/{appName}/{appId}/oauth2/callback
- "List all authenticators?" -> GET /api/v1/authenticators
- "Create a authenticator?" -> POST /api/v1/authenticators
- "Get authenticator details?" -> GET /api/v1/authenticators/{authenticatorId}
- "Update a authenticator?" -> PUT /api/v1/authenticators/{authenticatorId}
- "List all aaguids?" -> GET /api/v1/authenticators/{authenticatorId}/aaguids
- "Create a aaguid?" -> POST /api/v1/authenticators/{authenticatorId}/aaguids
- "Get aaguid details?" -> GET /api/v1/authenticators/{authenticatorId}/aaguids/{aaguid}
- "Update a aaguid?" -> PUT /api/v1/authenticators/{authenticatorId}/aaguids/{aaguid}
- "Partially update a aaguid?" -> PATCH /api/v1/authenticators/{authenticatorId}/aaguids/{aaguid}
- "Delete a aaguid?" -> DELETE /api/v1/authenticators/{authenticatorId}/aaguids/{aaguid}
- "Create a activate?" -> POST /api/v1/authenticators/{authenticatorId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/authenticators/{authenticatorId}/lifecycle/deactivate
- "List all methods?" -> GET /api/v1/authenticators/{authenticatorId}/methods
- "Get method details?" -> GET /api/v1/authenticators/{authenticatorId}/methods/{methodType}
- "Update a method?" -> PUT /api/v1/authenticators/{authenticatorId}/methods/{methodType}
- "Create a activate?" -> POST /api/v1/authenticators/{authenticatorId}/methods/{methodType}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/authenticators/{authenticatorId}/methods/{methodType}/lifecycle/deactivate
- "Search authorizationServers?" -> GET /api/v1/authorizationServers
- "Create a authorizationServer?" -> POST /api/v1/authorizationServers
- "Get authorizationServer details?" -> GET /api/v1/authorizationServers/{authServerId}
- "Update a authorizationServer?" -> PUT /api/v1/authorizationServers/{authServerId}
- "Delete a authorizationServer?" -> DELETE /api/v1/authorizationServers/{authServerId}
- "Search associatedServers?" -> GET /api/v1/authorizationServers/{authServerId}/associatedServers
- "Create a associatedServer?" -> POST /api/v1/authorizationServers/{authServerId}/associatedServers
- "Delete a associatedServer?" -> DELETE /api/v1/authorizationServers/{authServerId}/associatedServers/{associatedServerId}
- "List all claims?" -> GET /api/v1/authorizationServers/{authServerId}/claims
- "Create a claim?" -> POST /api/v1/authorizationServers/{authServerId}/claims
- "Get claim details?" -> GET /api/v1/authorizationServers/{authServerId}/claims/{claimId}
- "Update a claim?" -> PUT /api/v1/authorizationServers/{authServerId}/claims/{claimId}
- "Delete a claim?" -> DELETE /api/v1/authorizationServers/{authServerId}/claims/{claimId}
- "List all clients?" -> GET /api/v1/authorizationServers/{authServerId}/clients
- "List all tokens?" -> GET /api/v1/authorizationServers/{authServerId}/clients/{clientId}/tokens
- "Get token details?" -> GET /api/v1/authorizationServers/{authServerId}/clients/{clientId}/tokens/{tokenId}
- "Delete a token?" -> DELETE /api/v1/authorizationServers/{authServerId}/clients/{clientId}/tokens/{tokenId}
- "List all keys?" -> GET /api/v1/authorizationServers/{authServerId}/credentials/keys
- "Get key details?" -> GET /api/v1/authorizationServers/{authServerId}/credentials/keys/{keyId}
- "Create a keyRotate?" -> POST /api/v1/authorizationServers/{authServerId}/credentials/lifecycle/keyRotate
- "Create a activate?" -> POST /api/v1/authorizationServers/{authServerId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/authorizationServers/{authServerId}/lifecycle/deactivate
- "List all policies?" -> GET /api/v1/authorizationServers/{authServerId}/policies
- "Create a policy?" -> POST /api/v1/authorizationServers/{authServerId}/policies
- "Get policy details?" -> GET /api/v1/authorizationServers/{authServerId}/policies/{policyId}
- "Update a policy?" -> PUT /api/v1/authorizationServers/{authServerId}/policies/{policyId}
- "Delete a policy?" -> DELETE /api/v1/authorizationServers/{authServerId}/policies/{policyId}
- "Create a activate?" -> POST /api/v1/authorizationServers/{authServerId}/policies/{policyId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/authorizationServers/{authServerId}/policies/{policyId}/lifecycle/deactivate
- "List all rules?" -> GET /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules
- "Create a rule?" -> POST /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules
- "Get rule details?" -> GET /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules/{ruleId}
- "Update a rule?" -> PUT /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules/{ruleId}
- "Delete a rule?" -> DELETE /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules/{ruleId}
- "Create a activate?" -> POST /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules/{ruleId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/authorizationServers/{authServerId}/policies/{policyId}/rules/{ruleId}/lifecycle/deactivate
- "List all keys?" -> GET /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys
- "Create a key?" -> POST /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys
- "Get key details?" -> GET /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys/{keyId}
- "Delete a key?" -> DELETE /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys/{keyId}
- "Create a activate?" -> POST /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys/{keyId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/authorizationServers/{authServerId}/resourceservercredentials/keys/{keyId}/lifecycle/deactivate
- "Search scopes?" -> GET /api/v1/authorizationServers/{authServerId}/scopes
- "Create a scope?" -> POST /api/v1/authorizationServers/{authServerId}/scopes
- "Get scope details?" -> GET /api/v1/authorizationServers/{authServerId}/scopes/{scopeId}
- "Update a scope?" -> PUT /api/v1/authorizationServers/{authServerId}/scopes/{scopeId}
- "Delete a scope?" -> DELETE /api/v1/authorizationServers/{authServerId}/scopes/{scopeId}
- "List all behaviors?" -> GET /api/v1/behaviors
- "Create a behavior?" -> POST /api/v1/behaviors
- "Get behavior details?" -> GET /api/v1/behaviors/{behaviorId}
- "Update a behavior?" -> PUT /api/v1/behaviors/{behaviorId}
- "Delete a behavior?" -> DELETE /api/v1/behaviors/{behaviorId}
- "Create a activate?" -> POST /api/v1/behaviors/{behaviorId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/behaviors/{behaviorId}/lifecycle/deactivate
- "Search brands?" -> GET /api/v1/brands
- "Create a brand?" -> POST /api/v1/brands
- "Get brand details?" -> GET /api/v1/brands/{brandId}
- "Update a brand?" -> PUT /api/v1/brands/{brandId}
- "Delete a brand?" -> DELETE /api/v1/brands/{brandId}
- "List all domains?" -> GET /api/v1/brands/{brandId}/domains
- "List all error?" -> GET /api/v1/brands/{brandId}/pages/error
- "List all customized?" -> GET /api/v1/brands/{brandId}/pages/error/customized
- "List all default?" -> GET /api/v1/brands/{brandId}/pages/error/default
- "List all preview?" -> GET /api/v1/brands/{brandId}/pages/error/preview
- "List all sign-in?" -> GET /api/v1/brands/{brandId}/pages/sign-in
- "List all customized?" -> GET /api/v1/brands/{brandId}/pages/sign-in/customized
- "List all default?" -> GET /api/v1/brands/{brandId}/pages/sign-in/default
- "List all preview?" -> GET /api/v1/brands/{brandId}/pages/sign-in/preview
- "List all widget-versions?" -> GET /api/v1/brands/{brandId}/pages/sign-in/widget-versions
- "List all customized?" -> GET /api/v1/brands/{brandId}/pages/sign-out/customized
- "List all email?" -> GET /api/v1/brands/{brandId}/templates/email
- "Get email details?" -> GET /api/v1/brands/{brandId}/templates/email/{templateName}
- "List all customizations?" -> GET /api/v1/brands/{brandId}/templates/email/{templateName}/customizations
- "Create a customization?" -> POST /api/v1/brands/{brandId}/templates/email/{templateName}/customizations
- "Get customization details?" -> GET /api/v1/brands/{brandId}/templates/email/{templateName}/customizations/{customizationId}
- "Update a customization?" -> PUT /api/v1/brands/{brandId}/templates/email/{templateName}/customizations/{customizationId}
- "Delete a customization?" -> DELETE /api/v1/brands/{brandId}/templates/email/{templateName}/customizations/{customizationId}
- "List all preview?" -> GET /api/v1/brands/{brandId}/templates/email/{templateName}/customizations/{customizationId}/preview
- "List all default-content?" -> GET /api/v1/brands/{brandId}/templates/email/{templateName}/default-content
- "List all preview?" -> GET /api/v1/brands/{brandId}/templates/email/{templateName}/default-content/preview
- "List all settings?" -> GET /api/v1/brands/{brandId}/templates/email/{templateName}/settings
- "Create a test?" -> POST /api/v1/brands/{brandId}/templates/email/{templateName}/test
- "List all themes?" -> GET /api/v1/brands/{brandId}/themes
- "Get theme details?" -> GET /api/v1/brands/{brandId}/themes/{themeId}
- "Update a theme?" -> PUT /api/v1/brands/{brandId}/themes/{themeId}
- "Create a background-image?" -> POST /api/v1/brands/{brandId}/themes/{themeId}/background-image
- "Create a favicon?" -> POST /api/v1/brands/{brandId}/themes/{themeId}/favicon
- "Create a logo?" -> POST /api/v1/brands/{brandId}/themes/{themeId}/logo
- "List all well-known-uris?" -> GET /api/v1/brands/{brandId}/well-known-uris
- "Get well-known-uris details?" -> GET /api/v1/brands/{brandId}/well-known-uris/{path}
- "List all customized?" -> GET /api/v1/brands/{brandId}/well-known-uris/{path}/customized
- "List all captchas?" -> GET /api/v1/captchas
- "Create a captcha?" -> POST /api/v1/captchas
- "Get captcha details?" -> GET /api/v1/captchas/{captchaId}
- "Update a captcha?" -> PUT /api/v1/captchas/{captchaId}
- "Delete a captcha?" -> DELETE /api/v1/captchas/{captchaId}
- "List all device-assurances?" -> GET /api/v1/device-assurances
- "Create a device-assurance?" -> POST /api/v1/device-assurances
- "Get device-assurance details?" -> GET /api/v1/device-assurances/{deviceAssuranceId}
- "Update a device-assurance?" -> PUT /api/v1/device-assurances/{deviceAssuranceId}
- "Delete a device-assurance?" -> DELETE /api/v1/device-assurances/{deviceAssuranceId}
- "List all device-integrations?" -> GET /api/v1/device-integrations
- "Get device-integration details?" -> GET /api/v1/device-integrations/{deviceIntegrationId}
- "Create a activate?" -> POST /api/v1/device-integrations/{deviceIntegrationId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/device-integrations/{deviceIntegrationId}/lifecycle/deactivate
- "List all device-posture-checks?" -> GET /api/v1/device-posture-checks
- "Create a device-posture-check?" -> POST /api/v1/device-posture-checks
- "List all default?" -> GET /api/v1/device-posture-checks/default
- "Get device-posture-check details?" -> GET /api/v1/device-posture-checks/{postureCheckId}
- "Update a device-posture-check?" -> PUT /api/v1/device-posture-checks/{postureCheckId}
- "Delete a device-posture-check?" -> DELETE /api/v1/device-posture-checks/{postureCheckId}
- "Search devices?" -> GET /api/v1/devices
- "Get device details?" -> GET /api/v1/devices/{deviceId}
- "Delete a device?" -> DELETE /api/v1/devices/{deviceId}
- "Create a activate?" -> POST /api/v1/devices/{deviceId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/devices/{deviceId}/lifecycle/deactivate
- "Create a suspend?" -> POST /api/v1/devices/{deviceId}/lifecycle/suspend
- "Create a unsuspend?" -> POST /api/v1/devices/{deviceId}/lifecycle/unsuspend
- "List all users?" -> GET /api/v1/devices/{deviceId}/users
- "Create a modify?" -> POST /api/v1/directories/{appInstanceId}/groups/modify
- "List all domains?" -> GET /api/v1/domains
- "Create a domain?" -> POST /api/v1/domains
- "Get domain details?" -> GET /api/v1/domains/{domainId}
- "Update a domain?" -> PUT /api/v1/domains/{domainId}
- "Delete a domain?" -> DELETE /api/v1/domains/{domainId}
- "Create a verify?" -> POST /api/v1/domains/{domainId}/verify
- "List all email-domains?" -> GET /api/v1/email-domains
- "Create a email-domain?" -> POST /api/v1/email-domains
- "Get email-domain details?" -> GET /api/v1/email-domains/{emailDomainId}
- "Update a email-domain?" -> PUT /api/v1/email-domains/{emailDomainId}
- "Delete a email-domain?" -> DELETE /api/v1/email-domains/{emailDomainId}
- "Create a verify?" -> POST /api/v1/email-domains/{emailDomainId}/verify
- "List all email-servers?" -> GET /api/v1/email-servers
- "Create a email-server?" -> POST /api/v1/email-servers
- "Get email-server details?" -> GET /api/v1/email-servers/{emailServerId}
- "Partially update a email-server?" -> PATCH /api/v1/email-servers/{emailServerId}
- "Delete a email-server?" -> DELETE /api/v1/email-servers/{emailServerId}
- "Create a test?" -> POST /api/v1/email-servers/{emailServerId}/test
- "List all eventHooks?" -> GET /api/v1/eventHooks
- "Create a eventHook?" -> POST /api/v1/eventHooks
- "Get eventHook details?" -> GET /api/v1/eventHooks/{eventHookId}
- "Update a eventHook?" -> PUT /api/v1/eventHooks/{eventHookId}
- "Delete a eventHook?" -> DELETE /api/v1/eventHooks/{eventHookId}
- "Create a activate?" -> POST /api/v1/eventHooks/{eventHookId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/eventHooks/{eventHookId}/lifecycle/deactivate
- "Create a verify?" -> POST /api/v1/eventHooks/{eventHookId}/lifecycle/verify
- "List all features?" -> GET /api/v1/features
- "Get feature details?" -> GET /api/v1/features/{featureId}
- "List all dependencies?" -> GET /api/v1/features/{featureId}/dependencies
- "List all dependents?" -> GET /api/v1/features/{featureId}/dependents
- "Get first-party-app-setting details?" -> GET /api/v1/first-party-app-settings/{appName}
- "Update a first-party-app-setting?" -> PUT /api/v1/first-party-app-settings/{appName}
- "Search groups?" -> GET /api/v1/groups
- "Create a group?" -> POST /api/v1/groups
- "Search rules?" -> GET /api/v1/groups/rules
- "Create a rule?" -> POST /api/v1/groups/rules
- "Get rule details?" -> GET /api/v1/groups/rules/{groupRuleId}
- "Update a rule?" -> PUT /api/v1/groups/rules/{groupRuleId}
- "Delete a rule?" -> DELETE /api/v1/groups/rules/{groupRuleId}
- "Create a activate?" -> POST /api/v1/groups/rules/{groupRuleId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/groups/rules/{groupRuleId}/lifecycle/deactivate
- "Get group details?" -> GET /api/v1/groups/{groupId}
- "Update a group?" -> PUT /api/v1/groups/{groupId}
- "Delete a group?" -> DELETE /api/v1/groups/{groupId}
- "List all apps?" -> GET /api/v1/groups/{groupId}/apps
- "Search owners?" -> GET /api/v1/groups/{groupId}/owners
- "Create a owner?" -> POST /api/v1/groups/{groupId}/owners
- "Delete a owner?" -> DELETE /api/v1/groups/{groupId}/owners/{ownerId}
- "List all roles?" -> GET /api/v1/groups/{groupId}/roles
- "Create a role?" -> POST /api/v1/groups/{groupId}/roles
- "Get role details?" -> GET /api/v1/groups/{groupId}/roles/{roleAssignmentId}
- "Delete a role?" -> DELETE /api/v1/groups/{groupId}/roles/{roleAssignmentId}
- "List all apps?" -> GET /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/catalog/apps
- "Update a app?" -> PUT /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}
- "Delete a app?" -> DELETE /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}
- "Update a app?" -> PUT /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId}
- "Delete a app?" -> DELETE /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId}
- "List all groups?" -> GET /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/groups
- "Update a group?" -> PUT /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/groups/{targetGroupId}
- "Delete a group?" -> DELETE /api/v1/groups/{groupId}/roles/{roleAssignmentId}/targets/groups/{targetGroupId}
- "List all users?" -> GET /api/v1/groups/{groupId}/users
- "Update a user?" -> PUT /api/v1/groups/{groupId}/users/{userId}
- "Delete a user?" -> DELETE /api/v1/groups/{groupId}/users/{userId}
- "List all hook-keys?" -> GET /api/v1/hook-keys
- "Create a hook-key?" -> POST /api/v1/hook-keys
- "Get public details?" -> GET /api/v1/hook-keys/public/{keyId}
- "Get hook-key details?" -> GET /api/v1/hook-keys/{id}
- "Update a hook-key?" -> PUT /api/v1/hook-keys/{id}
- "Delete a hook-key?" -> DELETE /api/v1/hook-keys/{id}
- "List all users?" -> GET /api/v1/iam/assignees/users
- "List all bundles?" -> GET /api/v1/iam/governance/bundles
- "Create a bundle?" -> POST /api/v1/iam/governance/bundles
- "Get bundle details?" -> GET /api/v1/iam/governance/bundles/{bundleId}
- "Update a bundle?" -> PUT /api/v1/iam/governance/bundles/{bundleId}
- "Delete a bundle?" -> DELETE /api/v1/iam/governance/bundles/{bundleId}
- "List all entitlements?" -> GET /api/v1/iam/governance/bundles/{bundleId}/entitlements
- "List all values?" -> GET /api/v1/iam/governance/bundles/{bundleId}/entitlements/{entitlementId}/values
- "List all optIn?" -> GET /api/v1/iam/governance/optIn
- "Create a optIn?" -> POST /api/v1/iam/governance/optIn
- "Create a optOut?" -> POST /api/v1/iam/governance/optOut
- "List all resource-sets?" -> GET /api/v1/iam/resource-sets
- "Create a resource-set?" -> POST /api/v1/iam/resource-sets
- "Get resource-set details?" -> GET /api/v1/iam/resource-sets/{resourceSetIdOrLabel}
- "Update a resource-set?" -> PUT /api/v1/iam/resource-sets/{resourceSetIdOrLabel}
- "Delete a resource-set?" -> DELETE /api/v1/iam/resource-sets/{resourceSetIdOrLabel}
- "List all bindings?" -> GET /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings
- "Create a binding?" -> POST /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings
- "Get binding details?" -> GET /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings/{roleIdOrLabel}
- "Delete a binding?" -> DELETE /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings/{roleIdOrLabel}
- "List all members?" -> GET /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings/{roleIdOrLabel}/members
- "Get member details?" -> GET /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings/{roleIdOrLabel}/members/{memberId}
- "Delete a member?" -> DELETE /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/bindings/{roleIdOrLabel}/members/{memberId}
- "List all resources?" -> GET /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/resources
- "Create a resource?" -> POST /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/resources
- "Get resource details?" -> GET /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/resources/{resourceId}
- "Update a resource?" -> PUT /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/resources/{resourceId}
- "Delete a resource?" -> DELETE /api/v1/iam/resource-sets/{resourceSetIdOrLabel}/resources/{resourceId}
- "List all roles?" -> GET /api/v1/iam/roles
- "Create a role?" -> POST /api/v1/iam/roles
- "Get role details?" -> GET /api/v1/iam/roles/{roleIdOrLabel}
- "Update a role?" -> PUT /api/v1/iam/roles/{roleIdOrLabel}
- "Delete a role?" -> DELETE /api/v1/iam/roles/{roleIdOrLabel}
- "List all permissions?" -> GET /api/v1/iam/roles/{roleIdOrLabel}/permissions
- "Get permission details?" -> GET /api/v1/iam/roles/{roleIdOrLabel}/permissions/{permissionType}
- "Update a permission?" -> PUT /api/v1/iam/roles/{roleIdOrLabel}/permissions/{permissionType}
- "Delete a permission?" -> DELETE /api/v1/iam/roles/{roleIdOrLabel}/permissions/{permissionType}
- "List all sessions?" -> GET /api/v1/identity-sources/{identitySourceId}/sessions
- "Create a session?" -> POST /api/v1/identity-sources/{identitySourceId}/sessions
- "Get session details?" -> GET /api/v1/identity-sources/{identitySourceId}/sessions/{sessionId}
- "Delete a session?" -> DELETE /api/v1/identity-sources/{identitySourceId}/sessions/{sessionId}
- "Create a bulk-delete?" -> POST /api/v1/identity-sources/{identitySourceId}/sessions/{sessionId}/bulk-delete
- "Create a bulk-upsert?" -> POST /api/v1/identity-sources/{identitySourceId}/sessions/{sessionId}/bulk-upsert
- "Create a start-import?" -> POST /api/v1/identity-sources/{identitySourceId}/sessions/{sessionId}/start-import
- "Search idps?" -> GET /api/v1/idps
- "Create a idp?" -> POST /api/v1/idps
- "List all keys?" -> GET /api/v1/idps/credentials/keys
- "Create a key?" -> POST /api/v1/idps/credentials/keys
- "Get key details?" -> GET /api/v1/idps/credentials/keys/{kid}
- "Update a key?" -> PUT /api/v1/idps/credentials/keys/{kid}
- "Delete a key?" -> DELETE /api/v1/idps/credentials/keys/{kid}
- "Get idp details?" -> GET /api/v1/idps/{idpId}
- "Update a idp?" -> PUT /api/v1/idps/{idpId}
- "Delete a idp?" -> DELETE /api/v1/idps/{idpId}
- "List all csrs?" -> GET /api/v1/idps/{idpId}/credentials/csrs
- "Create a csr?" -> POST /api/v1/idps/{idpId}/credentials/csrs
- "Get csr details?" -> GET /api/v1/idps/{idpId}/credentials/csrs/{idpCsrId}
- "Delete a csr?" -> DELETE /api/v1/idps/{idpId}/credentials/csrs/{idpCsrId}
- "Create a publish?" -> POST /api/v1/idps/{idpId}/credentials/csrs/{idpCsrId}/lifecycle/publish
- "List all keys?" -> GET /api/v1/idps/{idpId}/credentials/keys
- "List all active?" -> GET /api/v1/idps/{idpId}/credentials/keys/active
- "Create a generate?" -> POST /api/v1/idps/{idpId}/credentials/keys/generate
- "Get key details?" -> GET /api/v1/idps/{idpId}/credentials/keys/{kid}
- "Create a clone?" -> POST /api/v1/idps/{idpId}/credentials/keys/{kid}/clone
- "Create a activate?" -> POST /api/v1/idps/{idpId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/idps/{idpId}/lifecycle/deactivate
- "Search users?" -> GET /api/v1/idps/{idpId}/users
- "Get user details?" -> GET /api/v1/idps/{idpId}/users/{userId}
- "Delete a user?" -> DELETE /api/v1/idps/{idpId}/users/{userId}
- "List all tokens?" -> GET /api/v1/idps/{idpId}/users/{userId}/credentials/tokens
- "List all inlineHooks?" -> GET /api/v1/inlineHooks
- "Create a inlineHook?" -> POST /api/v1/inlineHooks
- "Get inlineHook details?" -> GET /api/v1/inlineHooks/{inlineHookId}
- "Update a inlineHook?" -> PUT /api/v1/inlineHooks/{inlineHookId}
- "Delete a inlineHook?" -> DELETE /api/v1/inlineHooks/{inlineHookId}
- "Create a execute?" -> POST /api/v1/inlineHooks/{inlineHookId}/execute
- "Create a activate?" -> POST /api/v1/inlineHooks/{inlineHookId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/inlineHooks/{inlineHookId}/lifecycle/deactivate
- "List all logStreams?" -> GET /api/v1/logStreams
- "Create a logStream?" -> POST /api/v1/logStreams
- "Get logStream details?" -> GET /api/v1/logStreams/{logStreamId}
- "Update a logStream?" -> PUT /api/v1/logStreams/{logStreamId}
- "Delete a logStream?" -> DELETE /api/v1/logStreams/{logStreamId}
- "Create a activate?" -> POST /api/v1/logStreams/{logStreamId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/logStreams/{logStreamId}/lifecycle/deactivate
- "Search logs?" -> GET /api/v1/logs
- "List all mappings?" -> GET /api/v1/mappings
- "Get mapping details?" -> GET /api/v1/mappings/{mappingId}
- "List all default?" -> GET /api/v1/meta/schemas/apps/{appId}/default
- "Create a default?" -> POST /api/v1/meta/schemas/apps/{appId}/default
- "List all default?" -> GET /api/v1/meta/schemas/group/default
- "Create a default?" -> POST /api/v1/meta/schemas/group/default
- "List all logStream?" -> GET /api/v1/meta/schemas/logStream
- "Get logStream details?" -> GET /api/v1/meta/schemas/logStream/{logStreamType}
- "List all linkedObjects?" -> GET /api/v1/meta/schemas/user/linkedObjects
- "Create a linkedObject?" -> POST /api/v1/meta/schemas/user/linkedObjects
- "Get linkedObject details?" -> GET /api/v1/meta/schemas/user/linkedObjects/{linkedObjectName}
- "Delete a linkedObject?" -> DELETE /api/v1/meta/schemas/user/linkedObjects/{linkedObjectName}
- "Get user details?" -> GET /api/v1/meta/schemas/user/{schemaId}
- "List all user?" -> GET /api/v1/meta/types/user
- "Create a user?" -> POST /api/v1/meta/types/user
- "Get user details?" -> GET /api/v1/meta/types/user/{typeId}
- "Update a user?" -> PUT /api/v1/meta/types/user/{typeId}
- "Delete a user?" -> DELETE /api/v1/meta/types/user/{typeId}
- "List all uischemas?" -> GET /api/v1/meta/uischemas
- "Create a uischema?" -> POST /api/v1/meta/uischemas
- "Get uischema details?" -> GET /api/v1/meta/uischemas/{id}
- "Update a uischema?" -> PUT /api/v1/meta/uischemas/{id}
- "Delete a uischema?" -> DELETE /api/v1/meta/uischemas/{id}
- "List all org?" -> GET /api/v1/org
- "Create a org?" -> POST /api/v1/org
- "List all captcha?" -> GET /api/v1/org/captcha
- "List all contacts?" -> GET /api/v1/org/contacts
- "Get contact details?" -> GET /api/v1/org/contacts/{contactType}
- "Update a contact?" -> PUT /api/v1/org/contacts/{contactType}
- "Create a remove-list?" -> POST /api/v1/org/email/bounces/remove-list
- "List all tokens?" -> GET /api/v1/org/factors/yubikey_token/tokens
- "Create a token?" -> POST /api/v1/org/factors/yubikey_token/tokens
- "Get token details?" -> GET /api/v1/org/factors/yubikey_token/tokens/{tokenId}
- "Create a logo?" -> POST /api/v1/org/logo
- "List all thirdPartyAdminSetting?" -> GET /api/v1/org/orgSettings/thirdPartyAdminSetting
- "Create a thirdPartyAdminSetting?" -> POST /api/v1/org/orgSettings/thirdPartyAdminSetting
- "List all preferences?" -> GET /api/v1/org/preferences
- "Create a hideEndUserFooter?" -> POST /api/v1/org/preferences/hideEndUserFooter
- "Create a showEndUserFooter?" -> POST /api/v1/org/preferences/showEndUserFooter
- "List all aerial?" -> GET /api/v1/org/privacy/aerial
- "Create a grant?" -> POST /api/v1/org/privacy/aerial/grant
- "Create a revoke?" -> POST /api/v1/org/privacy/aerial/revoke
- "List all oktaCommunication?" -> GET /api/v1/org/privacy/oktaCommunication
- "Create a optIn?" -> POST /api/v1/org/privacy/oktaCommunication/optIn
- "Create a optOut?" -> POST /api/v1/org/privacy/oktaCommunication/optOut
- "List all oktaSupport?" -> GET /api/v1/org/privacy/oktaSupport
- "List all cases?" -> GET /api/v1/org/privacy/oktaSupport/cases
- "Partially update a case?" -> PATCH /api/v1/org/privacy/oktaSupport/cases/{caseNumber}
- "Create a extend?" -> POST /api/v1/org/privacy/oktaSupport/extend
- "Create a grant?" -> POST /api/v1/org/privacy/oktaSupport/grant
- "Create a revoke?" -> POST /api/v1/org/privacy/oktaSupport/revoke
- "List all autoAssignAdminAppSetting?" -> GET /api/v1/org/settings/autoAssignAdminAppSetting
- "Create a autoAssignAdminAppSetting?" -> POST /api/v1/org/settings/autoAssignAdminAppSetting
- "List all clientPrivilegesSetting?" -> GET /api/v1/org/settings/clientPrivilegesSetting
- "Create a org?" -> POST /api/v1/orgs
- "Search policies?" -> GET /api/v1/policies
- "Create a policy?" -> POST /api/v1/policies
- "Create a simulate?" -> POST /api/v1/policies/simulate
- "Get policy details?" -> GET /api/v1/policies/{policyId}
- "Update a policy?" -> PUT /api/v1/policies/{policyId}
- "Delete a policy?" -> DELETE /api/v1/policies/{policyId}
- "List all app?" -> GET /api/v1/policies/{policyId}/app
- "Create a clone?" -> POST /api/v1/policies/{policyId}/clone
- "Create a activate?" -> POST /api/v1/policies/{policyId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/policies/{policyId}/lifecycle/deactivate
- "List all mappings?" -> GET /api/v1/policies/{policyId}/mappings
- "Create a mapping?" -> POST /api/v1/policies/{policyId}/mappings
- "Get mapping details?" -> GET /api/v1/policies/{policyId}/mappings/{mappingId}
- "Delete a mapping?" -> DELETE /api/v1/policies/{policyId}/mappings/{mappingId}
- "List all rules?" -> GET /api/v1/policies/{policyId}/rules
- "Create a rule?" -> POST /api/v1/policies/{policyId}/rules
- "Get rule details?" -> GET /api/v1/policies/{policyId}/rules/{ruleId}
- "Update a rule?" -> PUT /api/v1/policies/{policyId}/rules/{ruleId}
- "Delete a rule?" -> DELETE /api/v1/policies/{policyId}/rules/{ruleId}
- "Create a activate?" -> POST /api/v1/policies/{policyId}/rules/{ruleId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/policies/{policyId}/rules/{ruleId}/lifecycle/deactivate
- "List all principal-rate-limits?" -> GET /api/v1/principal-rate-limits
- "Create a principal-rate-limit?" -> POST /api/v1/principal-rate-limits
- "Get principal-rate-limit details?" -> GET /api/v1/principal-rate-limits/{principalRateLimitId}
- "Update a principal-rate-limit?" -> PUT /api/v1/principal-rate-limits/{principalRateLimitId}
- "List all push-providers?" -> GET /api/v1/push-providers
- "Create a push-provider?" -> POST /api/v1/push-providers
- "Get push-provider details?" -> GET /api/v1/push-providers/{pushProviderId}
- "Update a push-provider?" -> PUT /api/v1/push-providers/{pushProviderId}
- "Delete a push-provider?" -> DELETE /api/v1/push-providers/{pushProviderId}
- "List all admin-notifications?" -> GET /api/v1/rate-limit-settings/admin-notifications
- "List all per-client?" -> GET /api/v1/rate-limit-settings/per-client
- "List all warning-threshold?" -> GET /api/v1/rate-limit-settings/warning-threshold
- "List all realm-assignments?" -> GET /api/v1/realm-assignments
- "Create a realm-assignment?" -> POST /api/v1/realm-assignments
- "List all operations?" -> GET /api/v1/realm-assignments/operations
- "Create a operation?" -> POST /api/v1/realm-assignments/operations
- "Get realm-assignment details?" -> GET /api/v1/realm-assignments/{assignmentId}
- "Update a realm-assignment?" -> PUT /api/v1/realm-assignments/{assignmentId}
- "Delete a realm-assignment?" -> DELETE /api/v1/realm-assignments/{assignmentId}
- "Create a activate?" -> POST /api/v1/realm-assignments/{assignmentId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/realm-assignments/{assignmentId}/lifecycle/deactivate
- "Search realms?" -> GET /api/v1/realms
- "Create a realm?" -> POST /api/v1/realms
- "Get realm details?" -> GET /api/v1/realms/{realmId}
- "Update a realm?" -> PUT /api/v1/realms/{realmId}
- "Delete a realm?" -> DELETE /api/v1/realms/{realmId}
- "Create a ip?" -> POST /api/v1/risk/events/ip
- "List all providers?" -> GET /api/v1/risk/providers
- "Create a provider?" -> POST /api/v1/risk/providers
- "Get provider details?" -> GET /api/v1/risk/providers/{riskProviderId}
- "Update a provider?" -> PUT /api/v1/risk/providers/{riskProviderId}
- "Delete a provider?" -> DELETE /api/v1/risk/providers/{riskProviderId}
- "List all subscriptions?" -> GET /api/v1/roles/{roleRef}/subscriptions
- "Get subscription details?" -> GET /api/v1/roles/{roleRef}/subscriptions/{notificationType}
- "Create a subscribe?" -> POST /api/v1/roles/{roleRef}/subscriptions/{notificationType}/subscribe
- "Create a unsubscribe?" -> POST /api/v1/roles/{roleRef}/subscriptions/{notificationType}/unsubscribe
- "List all security-events-providers?" -> GET /api/v1/security-events-providers
- "Create a security-events-provider?" -> POST /api/v1/security-events-providers
- "Get security-events-provider details?" -> GET /api/v1/security-events-providers/{securityEventProviderId}
- "Update a security-events-provider?" -> PUT /api/v1/security-events-providers/{securityEventProviderId}
- "Delete a security-events-provider?" -> DELETE /api/v1/security-events-providers/{securityEventProviderId}
- "Create a activate?" -> POST /api/v1/security-events-providers/{securityEventProviderId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/security-events-providers/{securityEventProviderId}/lifecycle/deactivate
- "Create a session?" -> POST /api/v1/sessions
- "List all me?" -> GET /api/v1/sessions/me
- "Create a refresh?" -> POST /api/v1/sessions/me/lifecycle/refresh
- "Get session details?" -> GET /api/v1/sessions/{sessionId}
- "Delete a session?" -> DELETE /api/v1/sessions/{sessionId}
- "Create a refresh?" -> POST /api/v1/sessions/{sessionId}/lifecycle/refresh
- "List all stream?" -> GET /api/v1/ssf/stream
- "Create a stream?" -> POST /api/v1/ssf/stream
- "List all status?" -> GET /api/v1/ssf/stream/status
- "Create a verification?" -> POST /api/v1/ssf/stream/verification
- "List all sms?" -> GET /api/v1/templates/sms
- "Create a sm?" -> POST /api/v1/templates/sms
- "Get sm details?" -> GET /api/v1/templates/sms/{templateId}
- "Update a sm?" -> PUT /api/v1/templates/sms/{templateId}
- "Delete a sm?" -> DELETE /api/v1/templates/sms/{templateId}
- "List all configuration?" -> GET /api/v1/threats/configuration
- "Create a configuration?" -> POST /api/v1/threats/configuration
- "Search trustedOrigins?" -> GET /api/v1/trustedOrigins
- "Create a trustedOrigin?" -> POST /api/v1/trustedOrigins
- "Get trustedOrigin details?" -> GET /api/v1/trustedOrigins/{trustedOriginId}
- "Update a trustedOrigin?" -> PUT /api/v1/trustedOrigins/{trustedOriginId}
- "Delete a trustedOrigin?" -> DELETE /api/v1/trustedOrigins/{trustedOriginId}
- "Create a activate?" -> POST /api/v1/trustedOrigins/{trustedOriginId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/trustedOrigins/{trustedOriginId}/lifecycle/deactivate
- "Search users?" -> GET /api/v1/users
- "Create a user?" -> POST /api/v1/users
- "Create a delete_session?" -> POST /api/v1/users/me/lifecycle/delete_sessions
- "Get user details?" -> GET /api/v1/users/{id}
- "Update a user?" -> PUT /api/v1/users/{id}
- "Delete a user?" -> DELETE /api/v1/users/{id}
- "List all appLinks?" -> GET /api/v1/users/{id}/appLinks
- "List all blocks?" -> GET /api/v1/users/{id}/blocks
- "List all groups?" -> GET /api/v1/users/{id}/groups
- "List all idps?" -> GET /api/v1/users/{id}/idps
- "Create a activate?" -> POST /api/v1/users/{id}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/users/{id}/lifecycle/deactivate
- "Create a expire_password?" -> POST /api/v1/users/{id}/lifecycle/expire_password
- "Create a expire_password_with_temp_password?" -> POST /api/v1/users/{id}/lifecycle/expire_password_with_temp_password
- "Create a reactivate?" -> POST /api/v1/users/{id}/lifecycle/reactivate
- "Create a reset_factor?" -> POST /api/v1/users/{id}/lifecycle/reset_factors
- "Create a reset_password?" -> POST /api/v1/users/{id}/lifecycle/reset_password
- "Create a suspend?" -> POST /api/v1/users/{id}/lifecycle/suspend
- "Create a unlock?" -> POST /api/v1/users/{id}/lifecycle/unlock
- "Create a unsuspend?" -> POST /api/v1/users/{id}/lifecycle/unsuspend
- "Update a linkedObject?" -> PUT /api/v1/users/{userIdOrLogin}/linkedObjects/{primaryRelationshipName}/{primaryUserId}
- "Get linkedObject details?" -> GET /api/v1/users/{userIdOrLogin}/linkedObjects/{relationshipName}
- "Delete a linkedObject?" -> DELETE /api/v1/users/{userIdOrLogin}/linkedObjects/{relationshipName}
- "List all authenticator-enrollments?" -> GET /api/v1/users/{userId}/authenticator-enrollments
- "Create a phone?" -> POST /api/v1/users/{userId}/authenticator-enrollments/phone
- "Create a tac?" -> POST /api/v1/users/{userId}/authenticator-enrollments/tac
- "Get authenticator-enrollment details?" -> GET /api/v1/users/{userId}/authenticator-enrollments/{enrollmentId}
- "Delete a authenticator-enrollment?" -> DELETE /api/v1/users/{userId}/authenticator-enrollments/{enrollmentId}
- "List all classification?" -> GET /api/v1/users/{userId}/classification
- "List all clients?" -> GET /api/v1/users/{userId}/clients
- "List all grants?" -> GET /api/v1/users/{userId}/clients/{clientId}/grants
- "List all tokens?" -> GET /api/v1/users/{userId}/clients/{clientId}/tokens
- "Get token details?" -> GET /api/v1/users/{userId}/clients/{clientId}/tokens/{tokenId}
- "Delete a token?" -> DELETE /api/v1/users/{userId}/clients/{clientId}/tokens/{tokenId}
- "Create a change_password?" -> POST /api/v1/users/{userId}/credentials/change_password
- "Create a change_recovery_question?" -> POST /api/v1/users/{userId}/credentials/change_recovery_question
- "Create a forgot_password?" -> POST /api/v1/users/{userId}/credentials/forgot_password
- "Create a forgot_password_recovery_question?" -> POST /api/v1/users/{userId}/credentials/forgot_password_recovery_question
- "List all devices?" -> GET /api/v1/users/{userId}/devices
- "List all factors?" -> GET /api/v1/users/{userId}/factors
- "Create a factor?" -> POST /api/v1/users/{userId}/factors
- "List all catalog?" -> GET /api/v1/users/{userId}/factors/catalog
- "List all questions?" -> GET /api/v1/users/{userId}/factors/questions
- "Get factor details?" -> GET /api/v1/users/{userId}/factors/{factorId}
- "Delete a factor?" -> DELETE /api/v1/users/{userId}/factors/{factorId}
- "Create a activate?" -> POST /api/v1/users/{userId}/factors/{factorId}/lifecycle/activate
- "Create a resend?" -> POST /api/v1/users/{userId}/factors/{factorId}/resend
- "Get transaction details?" -> GET /api/v1/users/{userId}/factors/{factorId}/transactions/{transactionId}
- "Create a verify?" -> POST /api/v1/users/{userId}/factors/{factorId}/verify
- "List all grants?" -> GET /api/v1/users/{userId}/grants
- "Get grant details?" -> GET /api/v1/users/{userId}/grants/{grantId}
- "Delete a grant?" -> DELETE /api/v1/users/{userId}/grants/{grantId}
- "List all risk?" -> GET /api/v1/users/{userId}/risk
- "List all roles?" -> GET /api/v1/users/{userId}/roles
- "Create a role?" -> POST /api/v1/users/{userId}/roles
- "Get role details?" -> GET /api/v1/users/{userId}/roles/{roleAssignmentId}
- "Delete a role?" -> DELETE /api/v1/users/{userId}/roles/{roleAssignmentId}
- "List all governance?" -> GET /api/v1/users/{userId}/roles/{roleAssignmentId}/governance
- "Get governance details?" -> GET /api/v1/users/{userId}/roles/{roleAssignmentId}/governance/{grantId}
- "List all resources?" -> GET /api/v1/users/{userId}/roles/{roleAssignmentId}/governance/{grantId}/resources
- "List all apps?" -> GET /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/catalog/apps
- "Update a app?" -> PUT /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}
- "Delete a app?" -> DELETE /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}
- "Update a app?" -> PUT /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId}
- "Delete a app?" -> DELETE /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId}
- "List all groups?" -> GET /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/groups
- "Update a group?" -> PUT /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/groups/{groupId}
- "Delete a group?" -> DELETE /api/v1/users/{userId}/roles/{roleAssignmentId}/targets/groups/{groupId}
- "List all targets?" -> GET /api/v1/users/{userId}/roles/{roleIdOrEncodedRoleId}/targets
- "List all subscriptions?" -> GET /api/v1/users/{userId}/subscriptions
- "Get subscription details?" -> GET /api/v1/users/{userId}/subscriptions/{notificationType}
- "Create a subscribe?" -> POST /api/v1/users/{userId}/subscriptions/{notificationType}/subscribe
- "Create a unsubscribe?" -> POST /api/v1/users/{userId}/subscriptions/{notificationType}/unsubscribe
- "List all zones?" -> GET /api/v1/zones
- "Create a zone?" -> POST /api/v1/zones
- "Get zone details?" -> GET /api/v1/zones/{zoneId}
- "Update a zone?" -> PUT /api/v1/zones/{zoneId}
- "Delete a zone?" -> DELETE /api/v1/zones/{zoneId}
- "Create a activate?" -> POST /api/v1/zones/{zoneId}/lifecycle/activate
- "Create a deactivate?" -> POST /api/v1/zones/{zoneId}/lifecycle/deactivate
- "List all authenticator-settings?" -> GET /attack-protection/api/v1/authenticator-settings
- "List all user-lockout-settings?" -> GET /attack-protection/api/v1/user-lockout-settings
- "List all enforce-number-matching-challenge-settings?" -> GET /device-access/api/v1/desktop-mfa/enforce-number-matching-challenge-settings
- "List all recovery-pin-settings?" -> GET /device-access/api/v1/desktop-mfa/recovery-pin-settings
- "List all api-services?" -> GET /integrations/api/v1/api-services
- "Create a api-service?" -> POST /integrations/api/v1/api-services
- "Get api-service details?" -> GET /integrations/api/v1/api-services/{apiServiceId}
- "Delete a api-service?" -> DELETE /integrations/api/v1/api-services/{apiServiceId}
- "List all secrets?" -> GET /integrations/api/v1/api-services/{apiServiceId}/credentials/secrets
- "Create a secret?" -> POST /integrations/api/v1/api-services/{apiServiceId}/credentials/secrets
- "Delete a secret?" -> DELETE /integrations/api/v1/api-services/{apiServiceId}/credentials/secrets/{secretId}
- "Create a activate?" -> POST /integrations/api/v1/api-services/{apiServiceId}/credentials/secrets/{secretId}/lifecycle/activate
- "Create a deactivate?" -> POST /integrations/api/v1/api-services/{apiServiceId}/credentials/secrets/{secretId}/lifecycle/deactivate
- "List all roles?" -> GET /oauth2/v1/clients/{clientId}/roles
- "Create a role?" -> POST /oauth2/v1/clients/{clientId}/roles
- "Get role details?" -> GET /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}
- "Delete a role?" -> DELETE /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}
- "List all apps?" -> GET /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/catalog/apps
- "Update a app?" -> PUT /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}
- "Delete a app?" -> DELETE /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}
- "Update a app?" -> PUT /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId}
- "Delete a app?" -> DELETE /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/catalog/apps/{appName}/{appId}
- "List all groups?" -> GET /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/groups
- "Update a group?" -> PUT /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/groups/{groupId}
- "Delete a group?" -> DELETE /oauth2/v1/clients/{clientId}/roles/{roleAssignmentId}/targets/groups/{groupId}
- "List all export-blocklists?" -> GET /okta-personal-settings/api/v1/export-blocklists
- "List all service-accounts?" -> GET /privileged-access/api/v1/service-accounts
- "Create a service-account?" -> POST /privileged-access/api/v1/service-accounts
- "Get service-account details?" -> GET /privileged-access/api/v1/service-accounts/{id}
- "Partially update a service-account?" -> PATCH /privileged-access/api/v1/service-accounts/{id}
- "Delete a service-account?" -> DELETE /privileged-access/api/v1/service-accounts/{id}
- "Create a security-event?" -> POST /security/api/v1/security-events
- "Create a activate?" -> POST /webauthn-registration/api/v1/activate
- "Create a enroll?" -> POST /webauthn-registration/api/v1/enroll
- "Create a initiate-fulfillment-request?" -> POST /webauthn-registration/api/v1/initiate-fulfillment-request
- "Create a send-pin?" -> POST /webauthn-registration/api/v1/send-pin
- "List all enrollments?" -> GET /webauthn-registration/api/v1/users/{userId}/enrollments
- "Delete a enrollment?" -> DELETE /webauthn-registration/api/v1/users/{userId}/enrollments/{authenticatorEnrollmentId}
- "Create a mark-error?" -> POST /webauthn-registration/api/v1/users/{userId}/enrollments/{authenticatorEnrollmentId}/mark-error
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
