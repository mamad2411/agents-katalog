---
name: akamai-application-security-api
description: "Akamai: Application Security API skill. Use when working with Akamai: Application Security for activations, api-discovery, configs. Covers 213 endpoints."
version: 1.0.0
generator: lapsh
---

# Akamai: Application Security API
API version: v1

## Auth
No authentication required.

## Base URL
https://{hostname}/appsec/v1

## Setup
1. No auth setup needed
2. GET /api-discovery -- verify access
3. POST /activations -- create first activations

## Endpoints

213 endpoints across 10 groups. See references/api-spec.lap for full details.

### activations
| Method | Path | Description |
|--------|------|-------------|
| POST | /activations | Activate a configuration version |
| GET | /activations/status/{statusId} | Get an activation request status |
| GET | /activations/{activationId} | Get activation status |

### api-discovery
| Method | Path | Description |
|--------|------|-------------|
| GET | /api-discovery | List discovered APIs |
| GET | /api-discovery/host/{hostname}/basepath/{basePath} | Get a discovered API |
| PUT | /api-discovery/host/{hostname}/basepath/{basePath} | Modify an API's visibility |
| POST | /api-discovery/host/{hostname}/basepath/{basePath}/endpoints | Create an endpoint or resource |
| GET | /api-discovery/host/{hostname}/basepath/{basePath}/endpoints | List discovered API endpoints |

### configs
| Method | Path | Description |
|--------|------|-------------|
| POST | /configs | Create a configuration |
| GET | /configs | List configurations |
| GET | /configs/{configId} | Get a security configuration |
| PUT | /configs/{configId} | Rename a security configuration |
| DELETE | /configs/{configId} | Delete a configuration |
| GET | /configs/{configId}/activations | List activation history |
| POST | /configs/{configId}/custom-rules | Create a custom rule |
| GET | /configs/{configId}/custom-rules | List custom rules |
| GET | /configs/{configId}/custom-rules/{ruleId} | Get a custom rule |
| PUT | /configs/{configId}/custom-rules/{ruleId} | Modify a custom rule |
| DELETE | /configs/{configId}/custom-rules/{ruleId} | Remove a custom rule |
| GET | /configs/{configId}/failover-hostnames | List failover hostnames |
| POST | /configs/{configId}/notification/subscription/{feature} | Subscribe or unsubscribe to recommendation emails |
| GET | /configs/{configId}/notification/subscription/{feature} | List subscribers |
| POST | /configs/{configId}/versions | Clone a configuration version |
| GET | /configs/{configId}/versions | List configuration versions |
| POST | /configs/{configId}/versions/diff | Compare two versions |
| GET | /configs/{configId}/versions/{versionNumber} | Get configuration version details |
| DELETE | /configs/{configId}/versions/{versionNumber} | Delete a configuration version |
| GET | /configs/{configId}/versions/{versionNumber}/advanced-settings/cookie-settings | Get cookie settings |
| PUT | /configs/{configId}/versions/{versionNumber}/advanced-settings/cookie-settings | Modify cookie settings |
| GET | /configs/{configId}/versions/{versionNumber}/advanced-settings/evasive-path-match | Get evasive path match settings for a configuration |
| PUT | /configs/{configId}/versions/{versionNumber}/advanced-settings/evasive-path-match | Modify evasive path match settings for a configuration |
| GET | /configs/{configId}/versions/{versionNumber}/advanced-settings/logging | Get the HTTP header log settings for a configuration |
| PUT | /configs/{configId}/versions/{versionNumber}/advanced-settings/logging | Modify HTTP header log settings for a configuration |
| GET | /configs/{configId}/versions/{versionNumber}/advanced-settings/logging/attack-payload | Get the attack payload log settings for a configuration |
| PUT | /configs/{configId}/versions/{versionNumber}/advanced-settings/logging/attack-payload | Modify attack payload log settings for a configuration |
| GET | /configs/{configId}/versions/{versionNumber}/advanced-settings/pii-learning | Get PII learning settings for a configuration |
| PUT | /configs/{configId}/versions/{versionNumber}/advanced-settings/pii-learning | Enable PII learning settings for a configuration |
| GET | /configs/{configId}/versions/{versionNumber}/advanced-settings/pragma-header | Get Pragma settings for a configuration |
| PUT | /configs/{configId}/versions/{versionNumber}/advanced-settings/pragma-header | Modify Pragma settings for a configuration |
| GET | /configs/{configId}/versions/{versionNumber}/advanced-settings/prefetch | Get prefetch requests |
| PUT | /configs/{configId}/versions/{versionNumber}/advanced-settings/prefetch | Modify prefetch requests |
| GET | /configs/{configId}/versions/{versionNumber}/advanced-settings/request-body | Get request body size settings for a configuration |
| PUT | /configs/{configId}/versions/{versionNumber}/advanced-settings/request-body | Modify request body inspection limit settings for a configuration |
| GET | /configs/{configId}/versions/{versionNumber}/bypass-network-lists | Get bypass network lists settings |
| PUT | /configs/{configId}/versions/{versionNumber}/bypass-network-lists | Modify the bypass network lists settings |
| POST | /configs/{configId}/versions/{versionNumber}/custom-deny | Create a custom deny action |
| GET | /configs/{configId}/versions/{versionNumber}/custom-deny | List custom deny actions |
| GET | /configs/{configId}/versions/{versionNumber}/custom-deny/{customDenyId} | Get a custom deny action |
| PUT | /configs/{configId}/versions/{versionNumber}/custom-deny/{customDenyId} | Modify a custom deny action |
| DELETE | /configs/{configId}/versions/{versionNumber}/custom-deny/{customDenyId} | Remove a custom deny action |
| GET | /configs/{configId}/versions/{versionNumber}/hostname-coverage/match-targets | Get the hostname coverage match targets |
| GET | /configs/{configId}/versions/{versionNumber}/hostname-coverage/overlapping | List hostname overlaps |
| POST | /configs/{configId}/versions/{versionNumber}/malware-policies | Create a malware policy |
| GET | /configs/{configId}/versions/{versionNumber}/malware-policies | List malware policies |
| GET | /configs/{configId}/versions/{versionNumber}/malware-policies/content-types | List supported malware policy content types |
| GET | /configs/{configId}/versions/{versionNumber}/malware-policies/{malwarePolicyId} | Get a malware policy |
| PUT | /configs/{configId}/versions/{versionNumber}/malware-policies/{malwarePolicyId} | Modify a malware policy |
| DELETE | /configs/{configId}/versions/{versionNumber}/malware-policies/{malwarePolicyId} | Remove a malware policy |
| POST | /configs/{configId}/versions/{versionNumber}/match-targets | Create a match target |
| GET | /configs/{configId}/versions/{versionNumber}/match-targets | List match targets |
| PUT | /configs/{configId}/versions/{versionNumber}/match-targets/sequence | Modify match target order |
| GET | /configs/{configId}/versions/{versionNumber}/match-targets/{targetId} | Get a match target |
| PUT | /configs/{configId}/versions/{versionNumber}/match-targets/{targetId} | Modify a match target |
| DELETE | /configs/{configId}/versions/{versionNumber}/match-targets/{targetId} | Remove a match target |
| PUT | /configs/{configId}/versions/{versionNumber}/protect-eval-hostnames | Protect evaluation hostnames |
| POST | /configs/{configId}/versions/{versionNumber}/rate-policies | Create a rate policy |
| GET | /configs/{configId}/versions/{versionNumber}/rate-policies | List rate policies |
| GET | /configs/{configId}/versions/{versionNumber}/rate-policies/{ratePolicyId} | Get a rate policy |
| PUT | /configs/{configId}/versions/{versionNumber}/rate-policies/{ratePolicyId} | Modify a rate policy |
| DELETE | /configs/{configId}/versions/{versionNumber}/rate-policies/{ratePolicyId} | Remove a rate policy |
| PUT | /configs/{configId}/versions/{versionNumber}/rate-policies/{ratePolicyId}/evaluation | Modify a rate policy evaluation |
| POST | /configs/{configId}/versions/{versionNumber}/reputation-profiles | Create a reputation profile |
| GET | /configs/{configId}/versions/{versionNumber}/reputation-profiles | List reputation profiles |
| GET | /configs/{configId}/versions/{versionNumber}/reputation-profiles/{reputationProfileId} | Get a reputation profile |
| PUT | /configs/{configId}/versions/{versionNumber}/reputation-profiles/{reputationProfileId} | Modify a reputation profile |
| DELETE | /configs/{configId}/versions/{versionNumber}/reputation-profiles/{reputationProfileId} | Remove a reputation profile |
| POST | /configs/{configId}/versions/{versionNumber}/security-policies | Clone or create a security policy |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies | List security policies |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId} | Get a security policy |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId} | Modify a security policy |
| DELETE | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId} | Remove a security policy |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/evasive-path-match | Get evasive path match settings |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/evasive-path-match | Modify evasive path match settings |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/logging | Get HTTP header log settings |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/logging | Modify HTTP header log settings |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/logging/attack-payload | Get attack payload logging settings for a policy |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/logging/attack-payload | Modify attack payload logging settings for a policy |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/pragma-header | Get Pragma settings for a security policy |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/pragma-header | Modify Pragma settings for a security policy |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/request-body | Get request body inspection limit settings for a security policy |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/request-body | Modify request body size settings for a security policy |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/api-endpoints | List API endpoints |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/api-request-constraints | List API request constraints and actions |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/api-request-constraints | Modify the request constraint action for all APIs |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/api-request-constraints/{apiId} | Modify an API request constraint's action |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/attack-groups | List attack groups |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/attack-groups/{attackGroupId} | Get the action for an attack group |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/attack-groups/{attackGroupId} | Modify the action for an attack group |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/attack-groups/{attackGroupId}/condition-exception | Get the exceptions of an attack group |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/attack-groups/{attackGroupId}/condition-exception | Modify the exceptions of an attack group |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/bypass-network-lists | Get the bypass network lists settings for a security policy |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/bypass-network-lists | Modify the bypass network lists settings for a security policy |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/cpc | Get Client-Side Protection & Compliance settings |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/cpc | Modify Client-Side Protections & Compliance settings |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/custom-rules | List custom rule actions |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/custom-rules/{ruleId} | Modify a custom rule action |
| POST | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval | Set evaluation mode |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-groups | List evaluation attack groups |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-groups/{attackGroupId} | Get the action for an evaluation attack group |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-groups/{attackGroupId} | Modify the action for an evaluation attack group |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-groups/{attackGroupId}/condition-exception | Get the exceptions of an evaluation attack group |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-groups/{attackGroupId}/condition-exception | Modify the exceptions of an evaluation attack group |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-hostnames | List evaluation hostnames for a security policy |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-hostnames | Modify evaluation hostnames for a security policy |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-penalty-box | Get the penalty box for a policy in evaluation mode |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-penalty-box | Modify the evaluation penalty box |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-penalty-box/conditions | Get penalty box conditions in evaluation mode |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-penalty-box/conditions | Modify the penalty box conditions in evaluation mode |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-rules | List evaluation rules |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-rules/{ruleId} | Get the action of an evaluation rule |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-rules/{ruleId} | Modify the action of an evaluation rule |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-rules/{ruleId}/condition-exception | Get the conditions and exceptions for an evaluation rule |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-rules/{ruleId}/condition-exception | Modify the conditions and exceptions for an evaluation rule |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/ip-geo-firewall | Get IP/Geo Firewall settings |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/ip-geo-firewall | Modify IP/Geo Firewall settings |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/malware-policies | List malware policy actions |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/malware-policies/{malwarePolicyId} | Modify a malware policy action |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/mode | Get the current mode |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/mode | Modify the mode |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/penalty-box | Get the penalty box |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/penalty-box | Modify the penalty box |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/penalty-box/conditions | Get penalty box condition |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/penalty-box/conditions | Modify the penalty box conditions |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/protect-eval-hostnames | Protect evaluation hostnames for a security policy |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/protections | Get protections |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/protections | Modify protections |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules | List rapid rules |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/action | Get rapid rules' default action |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/action | Update rapid rules' default action |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/status | Get rapid rules' status |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/status | Update rapid rules' status |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/{ruleId}/condition-exception | List a rapid rule's conditions and exceptions |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/{ruleId}/condition-exception | Update a rapid rule's conditions and exceptions |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/{ruleId}/lock | Get a rapid rule's lock status |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/{ruleId}/lock | Update a rapid rule's lock status |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/{ruleId}/versions/{ruleVersion}/action | Get a rapid rule's action |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/{ruleId}/versions/{ruleVersion}/action | Update a rapid rule's action |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rate-policies | List rate policy actions |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rate-policies/{ratePolicyId} | Modify a rate policy action |
| POST | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/recommendations | Respond to exception recommendations |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/recommendations | Get tuning recommendations for a policy |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/recommendations/attack-groups/{attackGroupId} | List tuning recommendations for an attack group |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/recommendations/rules/{ruleId} | List tuning recommendations for a rule |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/reputation-analysis | Get reputation analysis settings |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/reputation-analysis | Modify reputation analysis settings |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/reputation-profiles | List reputation profile actions |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/reputation-profiles/{reputationProfileId} | Get the action for a reputation profile |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/reputation-profiles/{reputationProfileId} | Modify the action for a reputation profile |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules | List rules |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules | Upgrade KRS ruleset |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/threat-intel | Get adaptive intelligence settings |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/threat-intel | Modify adaptive intelligence settings |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/upgrade-details | Get upgrade details |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/{ruleId} | Get the action for a rule |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/{ruleId} | Modify the action for a rule |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/{ruleId}/condition-exception | Get the conditions and exceptions of a rule |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/{ruleId}/condition-exception | Modify the conditions and exceptions of a rule |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/selected-hostnames | List selected hostnames for a security policy |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/selected-hostnames | Modify selected hostnames for a security policy |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/slow-post | Get slow POST protection settings |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/slow-post | Modify slow POST protection settings |
| GET | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/url-protections | List URL protection policy actions |
| PUT | /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/url-protections/{urlProtectionPolicyId} | Modify a URL protection policy action |
| GET | /configs/{configId}/versions/{versionNumber}/selectable-hostnames | List selectable hostnames |
| GET | /configs/{configId}/versions/{versionNumber}/selected-hostnames | List selected hostnames |
| PUT | /configs/{configId}/versions/{versionNumber}/selected-hostnames | Modify selected hostnames |
| GET | /configs/{configId}/versions/{versionNumber}/selected-hostnames/eval-hostnames | List evaluation hostnames |
| PUT | /configs/{configId}/versions/{versionNumber}/selected-hostnames/eval-hostnames | Modify evaluation hostnames |
| GET | /configs/{configId}/versions/{versionNumber}/siem | Get SIEM settings |
| PUT | /configs/{configId}/versions/{versionNumber}/siem | Modify SIEM settings |
| POST | /configs/{configId}/versions/{versionNumber}/url-protections | Create a URL protection policy |
| GET | /configs/{configId}/versions/{versionNumber}/url-protections | List URL protection policies |
| GET | /configs/{configId}/versions/{versionNumber}/url-protections/{urlProtectionPolicyId} | Get a URL protection policy |
| PUT | /configs/{configId}/versions/{versionNumber}/url-protections/{urlProtectionPolicyId} | Modify a URL protection policy |
| DELETE | /configs/{configId}/versions/{versionNumber}/url-protections/{urlProtectionPolicyId} | Remove a URL protection policy |
| GET | /configs/{configId}/versions/{versionNumber}/version-notes | Get the version notes |
| PUT | /configs/{configId}/versions/{versionNumber}/version-notes | Modify version notes |

### contracts-groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /contracts-groups | List contracts and groups |

### contracts
| Method | Path | Description |
|--------|------|-------------|
| GET | /contracts/{contractId}/groups/{groupId}/selectable-hostnames | List available hostnames for a new configuration |

### cves
| Method | Path | Description |
|--------|------|-------------|
| GET | /cves | List CVEs |
| POST | /cves/subscribe | Subscribe to CVEs |
| GET | /cves/subscribed | List subscribed CVEs |
| POST | /cves/unsubscribe | Unsubscribe from CVEs |
| GET | /cves/{cveId} | Get a CVE |
| GET | /cves/{cveId}/security-coverage | Get CVE coverage |

### export
| Method | Path | Description |
|--------|------|-------------|
| GET | /export/configs/{configId}/versions/{versionNumber} | Export a configuration version |

### hostname-coverage
| Method | Path | Description |
|--------|------|-------------|
| GET | /hostname-coverage | Get hostname coverage |

### onboardings
| Method | Path | Description |
|--------|------|-------------|
| POST | /onboardings | Create an onboarding |
| GET | /onboardings | List onboardings |
| GET | /onboardings/{onboardingId} | Get an onboarding |
| DELETE | /onboardings/{onboardingId} | Delete an onboarding |
| POST | /onboardings/{onboardingId}/activations | Activate an onboarding |
| GET | /onboardings/{onboardingId}/activations/{activationId} | Get an onboarding activation |
| GET | /onboardings/{onboardingId}/certificate-validation | List onboarding certificate challenges |
| POST | /onboardings/{onboardingId}/certificate-validation/validate | Validate onboarding certificate |
| GET | /onboardings/{onboardingId}/cname-to-akamai | List hostname CNAME DNS records |
| POST | /onboardings/{onboardingId}/cname-to-akamai/validate | Validate hostname CNAME DNS records |
| GET | /onboardings/{onboardingId}/origin-validation | List origin hostname DNS records |
| POST | /onboardings/{onboardingId}/origin-validation/skip | Skip origin hostnames DNS record validation |
| POST | /onboardings/{onboardingId}/origin-validation/validate | Validate origin hostnames DNS records |
| GET | /onboardings/{onboardingId}/settings | Get onboarding settings |
| PUT | /onboardings/{onboardingId}/settings | Modify onboarding settings |

### siem-definitions
| Method | Path | Description |
|--------|------|-------------|
| GET | /siem-definitions | Get SIEM versions |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a activation?" -> POST /activations
- "Get status details?" -> GET /activations/status/{statusId}
- "Get activation details?" -> GET /activations/{activationId}
- "Search api-discovery?" -> GET /api-discovery
- "Search basepath?" -> GET /api-discovery/host/{hostname}/basepath/{basePath}
- "Update a basepath?" -> PUT /api-discovery/host/{hostname}/basepath/{basePath}
- "Create a endpoint?" -> POST /api-discovery/host/{hostname}/basepath/{basePath}/endpoints
- "List all endpoints?" -> GET /api-discovery/host/{hostname}/basepath/{basePath}/endpoints
- "Create a config?" -> POST /configs
- "List all configs?" -> GET /configs
- "Get config details?" -> GET /configs/{configId}
- "Update a config?" -> PUT /configs/{configId}
- "Delete a config?" -> DELETE /configs/{configId}
- "List all activations?" -> GET /configs/{configId}/activations
- "Create a custom-rule?" -> POST /configs/{configId}/custom-rules
- "List all custom-rules?" -> GET /configs/{configId}/custom-rules
- "Get custom-rule details?" -> GET /configs/{configId}/custom-rules/{ruleId}
- "Update a custom-rule?" -> PUT /configs/{configId}/custom-rules/{ruleId}
- "Delete a custom-rule?" -> DELETE /configs/{configId}/custom-rules/{ruleId}
- "List all failover-hostnames?" -> GET /configs/{configId}/failover-hostnames
- "Get subscription details?" -> GET /configs/{configId}/notification/subscription/{feature}
- "Create a version?" -> POST /configs/{configId}/versions
- "List all versions?" -> GET /configs/{configId}/versions
- "Create a diff?" -> POST /configs/{configId}/versions/diff
- "Get version details?" -> GET /configs/{configId}/versions/{versionNumber}
- "Delete a version?" -> DELETE /configs/{configId}/versions/{versionNumber}
- "List all cookie-settings?" -> GET /configs/{configId}/versions/{versionNumber}/advanced-settings/cookie-settings
- "List all evasive-path-match?" -> GET /configs/{configId}/versions/{versionNumber}/advanced-settings/evasive-path-match
- "List all logging?" -> GET /configs/{configId}/versions/{versionNumber}/advanced-settings/logging
- "List all attack-payload?" -> GET /configs/{configId}/versions/{versionNumber}/advanced-settings/logging/attack-payload
- "List all pii-learning?" -> GET /configs/{configId}/versions/{versionNumber}/advanced-settings/pii-learning
- "List all pragma-header?" -> GET /configs/{configId}/versions/{versionNumber}/advanced-settings/pragma-header
- "List all prefetch?" -> GET /configs/{configId}/versions/{versionNumber}/advanced-settings/prefetch
- "List all request-body?" -> GET /configs/{configId}/versions/{versionNumber}/advanced-settings/request-body
- "List all bypass-network-lists?" -> GET /configs/{configId}/versions/{versionNumber}/bypass-network-lists
- "Create a custom-deny?" -> POST /configs/{configId}/versions/{versionNumber}/custom-deny
- "Search custom-deny?" -> GET /configs/{configId}/versions/{versionNumber}/custom-deny
- "Get custom-deny details?" -> GET /configs/{configId}/versions/{versionNumber}/custom-deny/{customDenyId}
- "Update a custom-deny?" -> PUT /configs/{configId}/versions/{versionNumber}/custom-deny/{customDenyId}
- "Delete a custom-deny?" -> DELETE /configs/{configId}/versions/{versionNumber}/custom-deny/{customDenyId}
- "List all match-targets?" -> GET /configs/{configId}/versions/{versionNumber}/hostname-coverage/match-targets
- "List all overlapping?" -> GET /configs/{configId}/versions/{versionNumber}/hostname-coverage/overlapping
- "Create a malware-policy?" -> POST /configs/{configId}/versions/{versionNumber}/malware-policies
- "List all malware-policies?" -> GET /configs/{configId}/versions/{versionNumber}/malware-policies
- "List all content-types?" -> GET /configs/{configId}/versions/{versionNumber}/malware-policies/content-types
- "Get malware-policy details?" -> GET /configs/{configId}/versions/{versionNumber}/malware-policies/{malwarePolicyId}
- "Update a malware-policy?" -> PUT /configs/{configId}/versions/{versionNumber}/malware-policies/{malwarePolicyId}
- "Delete a malware-policy?" -> DELETE /configs/{configId}/versions/{versionNumber}/malware-policies/{malwarePolicyId}
- "Create a match-target?" -> POST /configs/{configId}/versions/{versionNumber}/match-targets
- "List all match-targets?" -> GET /configs/{configId}/versions/{versionNumber}/match-targets
- "Get match-target details?" -> GET /configs/{configId}/versions/{versionNumber}/match-targets/{targetId}
- "Update a match-target?" -> PUT /configs/{configId}/versions/{versionNumber}/match-targets/{targetId}
- "Delete a match-target?" -> DELETE /configs/{configId}/versions/{versionNumber}/match-targets/{targetId}
- "Create a rate-policy?" -> POST /configs/{configId}/versions/{versionNumber}/rate-policies
- "List all rate-policies?" -> GET /configs/{configId}/versions/{versionNumber}/rate-policies
- "Get rate-policy details?" -> GET /configs/{configId}/versions/{versionNumber}/rate-policies/{ratePolicyId}
- "Update a rate-policy?" -> PUT /configs/{configId}/versions/{versionNumber}/rate-policies/{ratePolicyId}
- "Delete a rate-policy?" -> DELETE /configs/{configId}/versions/{versionNumber}/rate-policies/{ratePolicyId}
- "Create a reputation-profile?" -> POST /configs/{configId}/versions/{versionNumber}/reputation-profiles
- "List all reputation-profiles?" -> GET /configs/{configId}/versions/{versionNumber}/reputation-profiles
- "Get reputation-profile details?" -> GET /configs/{configId}/versions/{versionNumber}/reputation-profiles/{reputationProfileId}
- "Update a reputation-profile?" -> PUT /configs/{configId}/versions/{versionNumber}/reputation-profiles/{reputationProfileId}
- "Delete a reputation-profile?" -> DELETE /configs/{configId}/versions/{versionNumber}/reputation-profiles/{reputationProfileId}
- "Create a security-policy?" -> POST /configs/{configId}/versions/{versionNumber}/security-policies
- "List all security-policies?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies
- "Get security-policy details?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}
- "Update a security-policy?" -> PUT /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}
- "Delete a security-policy?" -> DELETE /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}
- "List all evasive-path-match?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/evasive-path-match
- "List all logging?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/logging
- "List all attack-payload?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/logging/attack-payload
- "List all pragma-header?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/pragma-header
- "List all request-body?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/advanced-settings/request-body
- "List all api-endpoints?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/api-endpoints
- "List all api-request-constraints?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/api-request-constraints
- "Update a api-request-constraint?" -> PUT /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/api-request-constraints/{apiId}
- "List all attack-groups?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/attack-groups
- "Get attack-group details?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/attack-groups/{attackGroupId}
- "Update a attack-group?" -> PUT /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/attack-groups/{attackGroupId}
- "List all condition-exception?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/attack-groups/{attackGroupId}/condition-exception
- "List all bypass-network-lists?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/bypass-network-lists
- "List all cpc?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/cpc
- "List all custom-rules?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/custom-rules
- "Update a custom-rule?" -> PUT /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/custom-rules/{ruleId}
- "Create a eval?" -> POST /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval
- "List all eval-groups?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-groups
- "Get eval-group details?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-groups/{attackGroupId}
- "Update a eval-group?" -> PUT /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-groups/{attackGroupId}
- "List all condition-exception?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-groups/{attackGroupId}/condition-exception
- "List all eval-hostnames?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-hostnames
- "List all eval-penalty-box?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-penalty-box
- "List all conditions?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-penalty-box/conditions
- "List all eval-rules?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-rules
- "Get eval-rule details?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-rules/{ruleId}
- "Update a eval-rule?" -> PUT /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-rules/{ruleId}
- "List all condition-exception?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/eval-rules/{ruleId}/condition-exception
- "List all ip-geo-firewall?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/ip-geo-firewall
- "List all malware-policies?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/malware-policies
- "Update a malware-policy?" -> PUT /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/malware-policies/{malwarePolicyId}
- "List all mode?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/mode
- "List all penalty-box?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/penalty-box
- "List all conditions?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/penalty-box/conditions
- "List all protections?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/protections
- "List all rapid-rules?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules
- "List all action?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/action
- "List all status?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/status
- "List all condition-exception?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/{ruleId}/condition-exception
- "List all lock?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/{ruleId}/lock
- "List all action?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rapid-rules/{ruleId}/versions/{ruleVersion}/action
- "List all rate-policies?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rate-policies
- "Update a rate-policy?" -> PUT /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rate-policies/{ratePolicyId}
- "Create a recommendation?" -> POST /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/recommendations
- "List all recommendations?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/recommendations
- "Get attack-group details?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/recommendations/attack-groups/{attackGroupId}
- "Get rule details?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/recommendations/rules/{ruleId}
- "List all reputation-analysis?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/reputation-analysis
- "List all reputation-profiles?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/reputation-profiles
- "Get reputation-profile details?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/reputation-profiles/{reputationProfileId}
- "Update a reputation-profile?" -> PUT /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/reputation-profiles/{reputationProfileId}
- "List all rules?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules
- "List all threat-intel?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/threat-intel
- "List all upgrade-details?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/upgrade-details
- "Get rule details?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/{ruleId}
- "Update a rule?" -> PUT /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/{ruleId}
- "List all condition-exception?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/rules/{ruleId}/condition-exception
- "List all selected-hostnames?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/selected-hostnames
- "List all slow-post?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/slow-post
- "List all url-protections?" -> GET /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/url-protections
- "Update a url-protection?" -> PUT /configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/url-protections/{urlProtectionPolicyId}
- "List all selectable-hostnames?" -> GET /configs/{configId}/versions/{versionNumber}/selectable-hostnames
- "List all selected-hostnames?" -> GET /configs/{configId}/versions/{versionNumber}/selected-hostnames
- "List all eval-hostnames?" -> GET /configs/{configId}/versions/{versionNumber}/selected-hostnames/eval-hostnames
- "List all siem?" -> GET /configs/{configId}/versions/{versionNumber}/siem
- "Create a url-protection?" -> POST /configs/{configId}/versions/{versionNumber}/url-protections
- "List all url-protections?" -> GET /configs/{configId}/versions/{versionNumber}/url-protections
- "Get url-protection details?" -> GET /configs/{configId}/versions/{versionNumber}/url-protections/{urlProtectionPolicyId}
- "Update a url-protection?" -> PUT /configs/{configId}/versions/{versionNumber}/url-protections/{urlProtectionPolicyId}
- "Delete a url-protection?" -> DELETE /configs/{configId}/versions/{versionNumber}/url-protections/{urlProtectionPolicyId}
- "List all version-notes?" -> GET /configs/{configId}/versions/{versionNumber}/version-notes
- "List all contracts-groups?" -> GET /contracts-groups
- "List all selectable-hostnames?" -> GET /contracts/{contractId}/groups/{groupId}/selectable-hostnames
- "List all cves?" -> GET /cves
- "Create a subscribe?" -> POST /cves/subscribe
- "List all subscribed?" -> GET /cves/subscribed
- "Create a unsubscribe?" -> POST /cves/unsubscribe
- "Get cve details?" -> GET /cves/{cveId}
- "List all security-coverage?" -> GET /cves/{cveId}/security-coverage
- "Get version details?" -> GET /export/configs/{configId}/versions/{versionNumber}
- "List all hostname-coverage?" -> GET /hostname-coverage
- "Create a onboarding?" -> POST /onboardings
- "List all onboardings?" -> GET /onboardings
- "Get onboarding details?" -> GET /onboardings/{onboardingId}
- "Delete a onboarding?" -> DELETE /onboardings/{onboardingId}
- "Create a activation?" -> POST /onboardings/{onboardingId}/activations
- "Get activation details?" -> GET /onboardings/{onboardingId}/activations/{activationId}
- "List all certificate-validation?" -> GET /onboardings/{onboardingId}/certificate-validation
- "Create a validate?" -> POST /onboardings/{onboardingId}/certificate-validation/validate
- "List all cname-to-akamai?" -> GET /onboardings/{onboardingId}/cname-to-akamai
- "Create a validate?" -> POST /onboardings/{onboardingId}/cname-to-akamai/validate
- "List all origin-validation?" -> GET /onboardings/{onboardingId}/origin-validation
- "Create a skip?" -> POST /onboardings/{onboardingId}/origin-validation/skip
- "Create a validate?" -> POST /onboardings/{onboardingId}/origin-validation/validate
- "List all settings?" -> GET /onboardings/{onboardingId}/settings
- "List all siem-definitions?" -> GET /siem-definitions

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object
- Error responses use types: [Conflict](https, [Forbidden](https, [Invalid](https, [Unauthorized](https

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
