---
name: snyk-api-webs-api-reference-documentation
description: "Snyk API & Web's API Reference Documentation API skill. Use when working with Snyk API & Web's API Reference Documentation for account, api-user-roles, api-users. Covers 371 endpoints."
version: 1.0.0
generator: lapsh
---

# Snyk API & Web's API Reference Documentation
API version: 1.2.0

## Auth
ApiKey Authorization in header

## Base URL
https://api.probely.com/

## Setup
1. Set your API key in the appropriate header
2. GET /account/available-slots/ -- verify access
3. POST /account/credits/top-up/ -- create first top-up

## Endpoints

371 endpoints across 30 groups. See references/api-spec.lap for full details.

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account/available-slots/ | Retrieve the Number of Free Slots for Targets with Unlimited Scans |
| GET | /account/billing/ | Retrieve Billing Information |
| PUT | /account/billing/ | Update Billing Information |
| PATCH | /account/billing/ | Partial Update Billing Information |
| GET | /account/credits/ | Retrieve Credits Details |
| POST | /account/credits/top-up/ | Purchase Credits |
| GET | /account/credits/top-up/settings/ | Retrieve Credits Auto Top-up Settings |
| PUT | /account/credits/top-up/settings/ | Update Credits Auto Top-up Settings |
| PATCH | /account/credits/top-up/settings/ | Partial Update Credits Auto Top-up Settings |
| GET | /account/credits/usage/ | List Credits Usage |
| GET | /account/credits/usage/report/ | Download a CSV file with Credits Usage entries. |
| GET | /account/entitlements/ | Retrieve Entitlements |
| GET | /account/invoices/ | List Invoices |
| GET | /account/invoices/{id}/pdf/ | Retrieve Invoice |
| GET | /account/settings/ | Retrieve Account Settings |
| PUT | /account/settings/ | Update Account Settings |
| PATCH | /account/settings/ | Partial Update Account Settings |
| GET | /account/subscription/ | Retrieve Subscription Information |
| GET | /account/unlimited/ | List Targets with Unlimited Scans |
| PUT | /account/unlimited/ | Bulk Update Targets with Unlimited Scans |
| PATCH | /account/unlimited/ | Bulk Partial Update Targets with Unlimited Scans |
| DELETE | /account/unlimited/ | Bulk Disable Targets with Unlimited Scans |

### api-user-roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /api-user-roles/ | List API User Roles |
| POST | /api-user-roles/ | Create API User Role |
| GET | /api-user-roles/{id}/ | Retrieve API User Role |
| PUT | /api-user-roles/{id}/ | Update API User Role |
| PATCH | /api-user-roles/{id}/ | Partial Update API User Role |
| DELETE | /api-user-roles/{id}/ | Delete API User Role |
| POST | /api-user-roles/bulk/create/ | Bulk Create API User Roles |
| POST | /api-user-roles/bulk/delete/ | Bulk Delete API User Roles |
| POST | /api-user-roles/bulk/operations/ | Bulk Operations on API User Roles |
| POST | /api-user-roles/bulk/update/ | Bulk Update API User Roles |

### api-users
| Method | Path | Description |
|--------|------|-------------|
| GET | /api-users/ | List API Users |
| POST | /api-users/ | Create API User |
| GET | /api-users/{id}/ | Retrieve API User |
| PUT | /api-users/{id}/ | Update API User |
| PATCH | /api-users/{id}/ | Partial Update API User |
| DELETE | /api-users/{id}/ | Disable API User |
| GET | /api-users/{user_id}/targets/ | List API User Targets |
| POST | /api-users/bulk/update/ | Bulk Update API Users |
| GET | /api-users/policy/ | Retrieve API Key Policy |
| PUT | /api-users/policy/ | Update API Key Policy |

### audit-log
| Method | Path | Description |
|--------|------|-------------|
| GET | /audit-log/ | List Audit Log entries. |
| GET | /audit-log/download/ | Download a CSV file with Audit Log entries. |

### credits-packs
| Method | Path | Description |
|--------|------|-------------|
| GET | /credits-packs/ | List Credits Packs |
| GET | /credits-packs/{id}/ | Retrieve Credits Pack |

### dashboard
| Method | Path | Description |
|--------|------|-------------|
| GET | /dashboard/aggregated-risk-trend/ | List Aggregated Risk Trends |
| GET | /dashboard/average-fix-time/ | List Average Fix Times |
| GET | /dashboard/fixed-vulnerabilities-trend/ | Get Fixed Vulnerabilities Trend |
| GET | /dashboard/needs-attention-pie/ | Retrieve Attention Pie |
| GET | /dashboard/needs-attention-top/ | List Top Items needing attention |
| GET | /dashboard/risk-trend/ | List Risk Trends |
| GET | /dashboard/severity-trend/ | List Severity Trends |
| GET | /dashboard/top-vulnerabilities/ | List Top Vulnerabilities |

### definitions
| Method | Path | Description |
|--------|------|-------------|
| GET | /definitions/ | List Vulnerability Definitions |
| GET | /definitions/{id}/ | Retrieve Vulnerability Definition |

### discovery
| Method | Path | Description |
|--------|------|-------------|
| GET | /discovery/assets/ | List Discovered Assets |
| GET | /discovery/assets/{discovery_asset_id}/logs/ | List Discovered Asset's Logs |
| GET | /discovery/assets/{id}/ | Retrieve Discovered Asset |
| PUT | /discovery/assets/{id}/ | Update Discovered Asset |
| PATCH | /discovery/assets/{id}/ | Partial Update Discovered Asset |
| POST | /discovery/assets/{id}/create_target/ | Create Target for Discovered Asset |
| GET | /discovery/assets/{id}/download_api_schema_file/ | Download API Schema File |
| GET | /discovery/assets/stats/ | Get Asset Discovery Statistics |
| GET | /discovery/settings/ | Retrieve Discovery settings |
| PUT | /discovery/settings/ | Update Asset Discovery Settings |
| PATCH | /discovery/settings/ | Partially Update Asset Discovery Settings |
| GET | /discovery/sources/ | List Asset Discovery Sources |
| GET | /discovery/status/ | Get Asset Discovery Status |

### domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /domains/ | List Domains |
| POST | /domains/ | Create Domain |
| GET | /domains/{id}/ | Retrieve Domain |
| PUT | /domains/{id}/ | Update Domain |
| PATCH | /domains/{id}/ | Partial Update to Domain |
| DELETE | /domains/{id}/ | Delete Domain |
| POST | /domains/{id}/verify/ | Verify Domain Ownership |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events/ | List Account's Events |
| GET | /events/{id}/ | Retrieve Account's Event |

### findings
| Method | Path | Description |
|--------|------|-------------|
| GET | /findings/ | List Account's Findings |
| GET | /findings/{id}/ | Retrieve Account's Finding |
| PUT | /findings/{id}/ | Update Account's Finding |
| PATCH | /findings/{id}/ | Partial Update Account's Finding |
| POST | /findings/bulk/report/ | Select Findings for Report |
| POST | /findings/bulk/retest/ | Bulk Retest Account's Findings |
| POST | /findings/bulk/update/ | Bulk Update Account's Findings |
| GET | /findings/report/ | Retrieve Selected Findings Report |

### frameworks
| Method | Path | Description |
|--------|------|-------------|
| GET | /frameworks/ | List Frameworks |
| GET | /frameworks/{id}/ | Retrieve Framework |

### integrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /integrations/akamai/ | Retrieve Akamai Configuration |
| PUT | /integrations/akamai/ | Update Akamai Configuration |
| PATCH | /integrations/akamai/ | Partial Update Akamai Configuration |
| DELETE | /integrations/akamai/ | Delete Akamai Configuration |
| POST | /integrations/akamai/refresh/ | Refresh Akamai Records |
| GET | /integrations/aws/ | Retrieve AWS Configuration |
| PUT | /integrations/aws/ | Update AWS Configuration |
| PATCH | /integrations/aws/ | Partial Update AWS Configuration |
| DELETE | /integrations/aws/ | Delete AWS Configuration |
| POST | /integrations/aws/refresh/ | Refresh AWS Records |
| GET | /integrations/azure-devops/ | Retrieve Azure DevOps Account Config |
| PUT | /integrations/azure-devops/ | Update Azure DevOps Account Config |
| PATCH | /integrations/azure-devops/ | Patch Azure DevOps Account Config |
| DELETE | /integrations/azure-devops/ | Delete Azure DevOps Account Config |
| GET | /integrations/cloudflare/ | Get Cloudflare Account instance data |
| PUT | /integrations/cloudflare/ | Update a Cloudflare Account instance |
| PATCH | /integrations/cloudflare/ | Partial Update a Cloudflare Account instance |
| DELETE | /integrations/cloudflare/ | Delete a Cloudflare Account instance |
| POST | /integrations/cloudflare/refresh/ | Refresh Cloudflare Records |
| GET | /integrations/jira-server/ | Get Jira Server Account instance data |
| PUT | /integrations/jira-server/ | Update a Jira Server Account instance |
| PATCH | /integrations/jira-server/ | Partial Update a Jira Server Account instance |
| DELETE | /integrations/jira-server/ | Delete a Jira Server Account instance |
| GET | /integrations/postman/ | Retrieve Account's Postman Integration Settings |
| POST | /integrations/postman/ | Add Account's Postman Settings |
| PUT | /integrations/postman/ | Update Account's Postman Settings |
| PATCH | /integrations/postman/ | Partial Update Account's Postman Settings |
| DELETE | /integrations/postman/ | Delete Account's Postman Setting |

### labels
| Method | Path | Description |
|--------|------|-------------|
| GET | /labels/findings/ | List Finding Labels |
| POST | /labels/findings/ | Create Finding Label |
| GET | /labels/findings/{id}/ | Retrieve Finding Label |
| PUT | /labels/findings/{id}/ | Update Finding Label |
| PATCH | /labels/findings/{id}/ | Partial Update Finding Label |
| DELETE | /labels/findings/{id}/ | Delete Finding Label |
| GET | /labels/targets/ | List Target Labels |
| POST | /labels/targets/ | Create Target Label |
| GET | /labels/targets/{id}/ | Retrieve Target Label |
| PUT | /labels/targets/{id}/ | Update Target Label |
| PATCH | /labels/targets/{id}/ | Partial Update Target Label |
| DELETE | /labels/targets/{id}/ | Delete Target Label |
| GET | /labels/users/ | List User Labels |
| POST | /labels/users/ | Create User Label |
| GET | /labels/users/{id}/ | Retrieve User Label |
| PUT | /labels/users/{id}/ | Update User Label |
| PATCH | /labels/users/{id}/ | Partial Update User Label |
| DELETE | /labels/users/{id}/ | Delete User Label |

### permissions
| Method | Path | Description |
|--------|------|-------------|
| GET | /permissions/ | List Permissions |

### plans
| Method | Path | Description |
|--------|------|-------------|
| GET | /plans/ | List Plans |

### profile
| Method | Path | Description |
|--------|------|-------------|
| GET | /profile/ | Retrieve Profile |
| POST | /profile/accept_tos/ | Accept User Terms of Service |
| POST | /profile/change_password/ | Change Password |
| GET | /profile/notifications/ | Retrieve Notifications Configuration |
| PUT | /profile/notifications/ | Update Notifications Configuration |
| PATCH | /profile/notifications/ | Partial Update Notifications Configuration |
| GET | /profile/permissions/ | List Permissions |
| GET | /profile/roles/ | List Roles |
| GET | /profile/targets/ | List Targets |

### report
| Method | Path | Description |
|--------|------|-------------|
| GET | /report/ | List Report Requests |
| POST | /report/ | Generate Report |
| GET | /report/{id}/ | Retrieve Report Request |
| PUT | /report/{id}/ | Update Report Request |
| PATCH | /report/{id}/ | Partial Update to Report Request |
| GET | /report/{id}/download/ | Download Report |
| GET | /report/{id}/status/ | Report Generation Status |
| GET | /report/types/ | Get all stored report types |

### roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /roles/ | List Roles |
| POST | /roles/ | Create Role |
| GET | /roles/{id}/ | Retrieve Role |
| PUT | /roles/{id}/ | Update Role |
| PATCH | /roles/{id}/ | Partial Update Role |
| DELETE | /roles/{id}/ | Delete Role |

### scan-profiles
| Method | Path | Description |
|--------|------|-------------|
| GET | /scan-profiles/ | List Scan Profiles |
| POST | /scan-profiles/ | Create Custom Scan Profile |
| GET | /scan-profiles/{id}/ | Retrieve Scan Profile |
| PUT | /scan-profiles/{id}/ | Update Custom Scan Profile |
| PATCH | /scan-profiles/{id}/ | Parcial Update Custom Scan Profile |

### scanning-agents
| Method | Path | Description |
|--------|------|-------------|
| GET | /scanning-agents/ | List Scanning Agents |
| POST | /scanning-agents/ | Create Scanning Agent |
| GET | /scanning-agents/{hek}/config-files/ | Get Configuration File |
| GET | /scanning-agents/{id}/ | Retrieve Scanning Agent |
| PUT | /scanning-agents/{id}/ | Update Scanning Agent |
| PATCH | /scanning-agents/{id}/ | Partial Update Scanning Agent |
| DELETE | /scanning-agents/{id}/ | Delete Scanning Agent |
| POST | /scanning-agents/{id}/generate/ | Create Token |

### scans
| Method | Path | Description |
|--------|------|-------------|
| GET | /scans/ | List Account's Scans |
| GET | /scans/{id}/ | Retrieve Account's Scans |
| POST | /scans/bulk/cancel/ | Bulk Cancel Scans |
| POST | /scans/bulk/pause/ | Bulk Pause Scans |
| POST | /scans/bulk/resume/ | Bulk Resume Scans |
| POST | /scans/bulk/start/ | Bulk Start Scans |
| GET | /scans/warnings/ | List Scan Warnings |
| GET | /scans/warnings/{id}/ | Retrive Scan Warning |

### scheduledscans
| Method | Path | Description |
|--------|------|-------------|
| GET | /scheduledscans/ | List Account's Scheduled Scans |
| POST | /scheduledscans/bulk/ | Bulk Create Scheduled Scans |
| PUT | /scheduledscans/bulk/ | Bulk Update Scheduled Scans |
| PATCH | /scheduledscans/bulk/ | Bulk Update Scheduled Scans |
| DELETE | /scheduledscans/bulk/ | Bulk Delete Scheduled Scans |

### stored-reports
| Method | Path | Description |
|--------|------|-------------|
| GET | /stored-reports/ | List Findings Scheduled Reports |
| POST | /stored-reports/ | Create Findings Scheduled Report |
| GET | /stored-reports/{id}/ | Retrieve Findings Scheduled Report |
| PUT | /stored-reports/{id}/ | Update Findings Scheduled Report |
| PATCH | /stored-reports/{id}/ | Partial Update Findings Scheduled Report |
| DELETE | /stored-reports/{id}/ | Delete Findings Scheduled Report |
| POST | /stored-reports/{id}/generate/ | Get report download URL |
| POST | /stored-reports/preview/ | Download Findings Scheduled Report Preview |

### targets
| Method | Path | Description |
|--------|------|-------------|
| GET | /targets/ | List Targets |
| POST | /targets/ | Create Target |
| GET | /targets/{id}/ | Retrieve Target |
| PUT | /targets/{id}/ | Update Target |
| PATCH | /targets/{id}/ | Partial Update Target |
| DELETE | /targets/{id}/ | Delete Target |
| DELETE | /targets/{id}/api-auth/ | Clear API Authentication Configuration |
| GET | /targets/{id}/average_fix_time/ | Average Fix Time Graph |
| DELETE | /targets/{id}/basic-auth/ | Clear Basic Authentication Configuration |
| POST | /targets/{id}/check_api_login/ | Test Log In to API |
| GET | /targets/{id}/download_api_schema_file/ | Download API Schema File |
| DELETE | /targets/{id}/form-login/ | Clear Login Form Configuration. |
| GET | /targets/{id}/get_postman_collection_folders/ | List Postman Collection Folders |
| GET | /targets/{id}/integrations/azure-devops/ | Retrieve Azure DevOps Target Config |
| PUT | /targets/{id}/integrations/azure-devops/ | Update Azure DevOps Target Config |
| PATCH | /targets/{id}/integrations/azure-devops/ | Patch Azure DevOps Target Config |
| DELETE | /targets/{id}/integrations/azure-devops/ | Delete Azure DevOps Target Config |
| GET | /targets/{id}/integrations/jira-cloud/ | Retrieve Jira Cloud Target Config |
| PUT | /targets/{id}/integrations/jira-cloud/ | Update Jira Cloud Target Config |
| PATCH | /targets/{id}/integrations/jira-cloud/ | Partial Update of Jira Cloud Target Config |
| DELETE | /targets/{id}/integrations/jira-cloud/ | Delete Jira Cloud Target Config |
| GET | /targets/{id}/integrations/jira-server/ | Retrieve Jira Server Target instance data |
| PUT | /targets/{id}/integrations/jira-server/ | Update a Jira Server Target instance |
| PATCH | /targets/{id}/integrations/jira-server/ | Partial Update a Jira Server Target instance |
| DELETE | /targets/{id}/integrations/jira-server/ | Delete a Jira Server Target instance |
| GET | /targets/{id}/integrations/slack/ | Retrieve Slack Configuration |
| PUT | /targets/{id}/integrations/slack/ | Update Slack Configuration |
| PATCH | /targets/{id}/integrations/slack/ | Partial Update Slack Configuration |
| DELETE | /targets/{id}/integrations/slack/ | Delete Slack Configuration |
| GET | /targets/{id}/login-video/ | Retrieve Login Video |
| DELETE | /targets/{id}/logout-detection/ | Clear Logout Detection Configuration |
| GET | /targets/{id}/mle/ | Retrieve MLE Configuration for Target |
| PUT | /targets/{id}/mle/ | Create or Update MLE Configuration for Target |
| PATCH | /targets/{id}/mle/ | Update MLE Configuration for Target |
| DELETE | /targets/{id}/mle/ | Delete MLE Configuration for Target |
| POST | /targets/{id}/move-team/ | Move Target to Another Team |
| GET | /targets/{id}/mtls/ | Retrieve mTLS Configuration for Target |
| PUT | /targets/{id}/mtls/ | Create or Update mTLS Configuration for Target |
| PATCH | /targets/{id}/mtls/ | Update mTLS Configuration for Target |
| DELETE | /targets/{id}/mtls/ | Delete mTLS Configuration for Target |
| DELETE | /targets/{id}/otp/ | Clear 2FA Configuration |
| POST | /targets/{id}/otp/{otp_url_token}/ | Send OTP |
| POST | /targets/{id}/otp/reset/ | Reset OTP URL |
| GET | /targets/{id}/postman-authentication/ | Retrieve Postman Authentication Settings |
| PUT | /targets/{id}/postman-authentication/ | Update Postman Authentication Settings |
| PATCH | /targets/{id}/postman-authentication/ | Partial Update Postman Authentication Settings |
| DELETE | /targets/{id}/postman-authentication/ | Delete Postman Authentication Settings |
| GET | /targets/{id}/risk_trend/ | Risk Trend Graph |
| POST | /targets/{id}/scan_now/ | Start a scan |
| DELETE | /targets/{id}/sequence-login/ | Clear Login Sequence Configuration |
| GET | /targets/{id}/severity_trend/ | Severity Trend Graph |
| GET | /targets/{id}/signature/ | Retrieve Message Signature Configuration Status |
| PUT | /targets/{id}/signature/ | Configure or Replace Message Signature |
| PATCH | /targets/{id}/signature/ | Update Message Signature Configuration |
| DELETE | /targets/{id}/signature/ | Delete Message Signature Configuration |
| GET | /targets/{id}/top_vulns/ | Top Vulnerabilities Graph |
| POST | /targets/{id}/upload_api_schema_file/ | Upload API Schema File |
| GET | /targets/{scope}/findings/{id}/integrations/azure-devops/ | Retrieve Azure DevOps Finding Config |
| PUT | /targets/{scope}/findings/{id}/integrations/azure-devops/ | Update Azure DevOps Finding Config |
| PATCH | /targets/{scope}/findings/{id}/integrations/azure-devops/ | Patch Azure DevOps Finding Config |
| GET | /targets/{scope}/findings/{id}/integrations/jira-cloud/ | Retrieve Jira Cloud Finding Config |
| PUT | /targets/{scope}/findings/{id}/integrations/jira-cloud/ | Update Jira Cloud Finding Config |
| PATCH | /targets/{scope}/findings/{id}/integrations/jira-cloud/ | Partial Update of Jira Cloud Finding Config |
| GET | /targets/{scope}/findings/{id}/integrations/jira-server/ | Retrieve Jira Server Finding instance |
| PUT | /targets/{scope}/findings/{id}/integrations/jira-server/ | Update a Jira Server Finding instance |
| PATCH | /targets/{scope}/findings/{id}/integrations/jira-server/ | Partial Update of Jira Server Finding instance |
| GET | /targets/{target_id}/assets/ | List Extra Hosts |
| POST | /targets/{target_id}/assets/ | Create Extra Host |
| GET | /targets/{target_id}/assets/{id}/ | Retrieve Extra Host |
| PUT | /targets/{target_id}/assets/{id}/ | Update Extra Host |
| PATCH | /targets/{target_id}/assets/{id}/ | Partial Update Extra Host |
| DELETE | /targets/{target_id}/assets/{id}/ | Delete Extra Host |
| GET | /targets/{target_id}/events/ | List Target's Events |
| GET | /targets/{target_id}/events/{id}/ | Retrieve Target's Event |
| GET | /targets/{target_id}/findings/ | List Target's Findings |
| GET | /targets/{target_id}/findings/{finding_id}/logs/ | List Findings Activity |
| GET | /targets/{target_id}/findings/{id}/ | Retrieve Target's Finding |
| PUT | /targets/{target_id}/findings/{id}/ | Update Target's Finding |
| PATCH | /targets/{target_id}/findings/{id}/ | Partial Update Target's Finding |
| POST | /targets/{target_id}/findings/{id}/retest/ | Retest Target's Finding |
| POST | /targets/{target_id}/findings/bulk/report/ | Create Target's Findings Report |
| POST | /targets/{target_id}/findings/bulk/retest/ | Bulk Retest Target's Findings |
| POST | /targets/{target_id}/findings/bulk/update/ | Bulk Update Target's Findings |
| GET | /targets/{target_id}/findings/report/ | Retrieve Target's Findings Report |
| GET | /targets/{target_id}/logout/ | List Logout Detectors |
| POST | /targets/{target_id}/logout/ | Create Logout Detector |
| GET | /targets/{target_id}/logout/{id}/ | Retrieve Logout Detector |
| PUT | /targets/{target_id}/logout/{id}/ | Update Logout Detector |
| PATCH | /targets/{target_id}/logout/{id}/ | Partial Update Logout Detector |
| DELETE | /targets/{target_id}/logout/{id}/ | Delete Logout Detector |
| GET | /targets/{target_id}/reduced-scopes/ | List Reduced Scopes |
| POST | /targets/{target_id}/reduced-scopes/ | Create Reduced Scope |
| GET | /targets/{target_id}/reduced-scopes/{id}/ | Retrieve Reduced Scope |
| PUT | /targets/{target_id}/reduced-scopes/{id}/ | Update Reduced Scope |
| PATCH | /targets/{target_id}/reduced-scopes/{id}/ | Partial Update Reduced Scope |
| DELETE | /targets/{target_id}/reduced-scopes/{id}/ | Delete Reduced Scope |
| GET | /targets/{target_id}/scan/ | Retrieve Target's Current Scan |
| POST | /targets/{target_id}/scan/cancel/ | Cancel Target's Current Scan |
| POST | /targets/{target_id}/scan/pause/ | Pause Target's Current Scan |
| POST | /targets/{target_id}/scan/resume/ | Resume Target's Current Scan |
| GET | /targets/{target_id}/scans/ | List Target's Scans |
| GET | /targets/{target_id}/scans/{id}/ | Retrieve Scan |
| PUT | /targets/{target_id}/scans/{id}/ | Update Scan |
| PATCH | /targets/{target_id}/scans/{id}/ | Partial Update Scan |
| POST | /targets/{target_id}/scans/{id}/cancel/ | Cancel Scan |
| GET | /targets/{target_id}/scans/{id}/endpoints/ | Export Coverage Report |
| POST | /targets/{target_id}/scans/{id}/pause/ | Pause Scan |
| GET | /targets/{target_id}/scans/{id}/report/ | Download Scan Report |
| POST | /targets/{target_id}/scans/{id}/resume/ | Resume Scan |
| GET | /targets/{target_id}/scans/dates/ | List Scan Dates |
| GET | /targets/{target_id}/scans/retrieve_page/ | Retrieve Page Number for Scan Date |
| GET | /targets/{target_id}/scheduledscans/ | List Target's Scheduled Scans |
| POST | /targets/{target_id}/scheduledscans/ | Create Target's Scheduled Scan |
| GET | /targets/{target_id}/scheduledscans/{id}/ | Retrieve Target's Scheduled Scan |
| PUT | /targets/{target_id}/scheduledscans/{id}/ | Update Target's Scheduled Scan |
| PATCH | /targets/{target_id}/scheduledscans/{id}/ | Partial Update Target's Scheduled Scan |
| DELETE | /targets/{target_id}/scheduledscans/{id}/ | Delete Target's Scheduled Scan |
| GET | /targets/{target_id}/scheduledscans/expanded/ | List Target's Scheduled Scans (Expanded) |
| GET | /targets/{target_id}/sequences/ | List Sequences |
| POST | /targets/{target_id}/sequences/ | Create Sequence |
| GET | /targets/{target_id}/sequences/{id}/ | Retrieve Sequence |
| PUT | /targets/{target_id}/sequences/{id}/ | Update Sequence |
| PATCH | /targets/{target_id}/sequences/{id}/ | Partial Update Sequence |
| DELETE | /targets/{target_id}/sequences/{id}/ | Delete Sequence |
| POST | /targets/{target_id}/sequences/{id}/order/ | Re-order Sequences |
| GET | /targets/{target_id}/webhooks/ | List Target's Webhooks |
| POST | /targets/{target_id}/webhooks/ | Create Target's Webhook |
| GET | /targets/{target_id}/webhooks/{id}/ | Retrieve Target's Webhook |
| PUT | /targets/{target_id}/webhooks/{id}/ | Update Target's Webhook |
| PATCH | /targets/{target_id}/webhooks/{id}/ | Partial Update Target's Webhook |
| DELETE | /targets/{target_id}/webhooks/{id}/ | Delete Target's Webhook |
| GET | /targets/all/average_fix_time/ | Average Fix Time Graph |
| GET | /targets/all/needs_attention_pie/ | Targets with open vulnerabilities pie chart data |
| GET | /targets/all/needs_attention_top/ | Targets with top number of open vulnerabilities |
| GET | /targets/all/risk_trend/ | Risk Trend Graph |
| GET | /targets/all/scans/ | List all Scans of Target |
| GET | /targets/all/scheduledscans/expanded/ | Account Scheduled Scans |
| GET | /targets/all/severity_trend/ | Severity Trend Graph |
| GET | /targets/all/top_vulns/ | Top Vulnerabilities Graph |
| GET | /targets/assets/ | List Account's Extra Hosts |
| POST | /targets/bulk/delete/ | Bulk Delete Targets |
| POST | /targets/bulk/move-team/ | Move Targets to Another Team |
| POST | /targets/bulk/update/ | Bulk Update Targets |
| GET | /targets/download/ | Export Targets |
| GET | /targets/sequences/ | List Account's Sequences |
| POST | /targets/upload/ | Import Targets |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /teams/ | List Teams |
| POST | /teams/ | Create Team |
| GET | /teams/{id}/ | Retrieve Team |
| PUT | /teams/{id}/ | Update Team |
| PATCH | /teams/{id}/ | Partial Update Team |
| DELETE | /teams/{id}/ | Delete Team |
| GET | /teams/available-slots/ | Retrieve the Number of Free Slots for Targets in the Team |

### user-roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /user-roles/ | List User Roles |
| POST | /user-roles/ | Create User Role |
| GET | /user-roles/{id}/ | Retrieve User Role |
| PUT | /user-roles/{id}/ | Update User Role |
| PATCH | /user-roles/{id}/ | Partial Update User Role |
| DELETE | /user-roles/{id}/ | Delete User Role |
| POST | /user-roles/bulk/create/ | Bulk Create User Roles |
| POST | /user-roles/bulk/delete/ | Bulk Delete User Roles |
| POST | /user-roles/bulk/operations/ | Bulk Operations User Roles |
| POST | /user-roles/bulk/update/ | Bulk Update User Roles |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/ | List Users |
| POST | /users/ | Create User |
| GET | /users/{id}/ | Retrieve User |
| PUT | /users/{id}/ | Update User |
| PATCH | /users/{id}/ | Partial Update User |
| DELETE | /users/{id}/ | Disable User |
| GET | /users/{user_id}/targets/ | List Targets |
| POST | /users/bulk/update/ | Bulk Update Users |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks/ | List Account's Webhooks |
| POST | /webhooks/ | Create Account's Webhook |
| GET | /webhooks/{id}/ | Retrieve Account's Webhook |
| PUT | /webhooks/{id}/ | Update Account's Webhook |
| PATCH | /webhooks/{id}/ | Partial Update Account's Webhook |
| DELETE | /webhooks/{id}/ | Delete Account's Webhook |

### wizard
| Method | Path | Description |
|--------|------|-------------|
| GET | /wizard/targets | List Wizard Targets |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all available-slots?" -> GET /account/available-slots/
- "List all billing?" -> GET /account/billing/
- "List all credits?" -> GET /account/credits/
- "Create a top-up?" -> POST /account/credits/top-up/
- "List all settings?" -> GET /account/credits/top-up/settings/
- "Search usage?" -> GET /account/credits/usage/
- "List all report?" -> GET /account/credits/usage/report/
- "List all entitlements?" -> GET /account/entitlements/
- "Search invoices?" -> GET /account/invoices/
- "List all pdf?" -> GET /account/invoices/{id}/pdf/
- "List all settings?" -> GET /account/settings/
- "List all subscription?" -> GET /account/subscription/
- "Search unlimited?" -> GET /account/unlimited/
- "List all api-user-roles?" -> GET /api-user-roles/
- "Create a api-user-role?" -> POST /api-user-roles/
- "Get api-user-role details?" -> GET /api-user-roles/{id}/
- "Update a api-user-role?" -> PUT /api-user-roles/{id}/
- "Partially update a api-user-role?" -> PATCH /api-user-roles/{id}/
- "Delete a api-user-role?" -> DELETE /api-user-roles/{id}/
- "Create a create?" -> POST /api-user-roles/bulk/create/
- "Create a delete?" -> POST /api-user-roles/bulk/delete/
- "Create a operation?" -> POST /api-user-roles/bulk/operations/
- "Create a update?" -> POST /api-user-roles/bulk/update/
- "Search api-users?" -> GET /api-users/
- "Create a api-user?" -> POST /api-users/
- "Get api-user details?" -> GET /api-users/{id}/
- "Update a api-user?" -> PUT /api-users/{id}/
- "Partially update a api-user?" -> PATCH /api-users/{id}/
- "Delete a api-user?" -> DELETE /api-users/{id}/
- "Search targets?" -> GET /api-users/{user_id}/targets/
- "Create a update?" -> POST /api-users/bulk/update/
- "List all policy?" -> GET /api-users/policy/
- "Search audit-log?" -> GET /audit-log/
- "List all download?" -> GET /audit-log/download/
- "List all credits-packs?" -> GET /credits-packs/
- "Get credits-pack details?" -> GET /credits-packs/{id}/
- "Search aggregated-risk-trend?" -> GET /dashboard/aggregated-risk-trend/
- "Search average-fix-time?" -> GET /dashboard/average-fix-time/
- "Search fixed-vulnerabilities-trend?" -> GET /dashboard/fixed-vulnerabilities-trend/
- "Search needs-attention-pie?" -> GET /dashboard/needs-attention-pie/
- "Search needs-attention-top?" -> GET /dashboard/needs-attention-top/
- "Search risk-trend?" -> GET /dashboard/risk-trend/
- "Search severity-trend?" -> GET /dashboard/severity-trend/
- "Search top-vulnerabilities?" -> GET /dashboard/top-vulnerabilities/
- "Search definitions?" -> GET /definitions/
- "Get definition details?" -> GET /definitions/{id}/
- "Search assets?" -> GET /discovery/assets/
- "Search logs?" -> GET /discovery/assets/{discovery_asset_id}/logs/
- "Get asset details?" -> GET /discovery/assets/{id}/
- "Update a asset?" -> PUT /discovery/assets/{id}/
- "Partially update a asset?" -> PATCH /discovery/assets/{id}/
- "Create a create_target?" -> POST /discovery/assets/{id}/create_target/
- "List all download_api_schema_file?" -> GET /discovery/assets/{id}/download_api_schema_file/
- "List all stats?" -> GET /discovery/assets/stats/
- "List all settings?" -> GET /discovery/settings/
- "List all sources?" -> GET /discovery/sources/
- "List all status?" -> GET /discovery/status/
- "Search domains?" -> GET /domains/
- "Create a domain?" -> POST /domains/
- "Get domain details?" -> GET /domains/{id}/
- "Update a domain?" -> PUT /domains/{id}/
- "Partially update a domain?" -> PATCH /domains/{id}/
- "Delete a domain?" -> DELETE /domains/{id}/
- "Create a verify?" -> POST /domains/{id}/verify/
- "Search events?" -> GET /events/
- "Get event details?" -> GET /events/{id}/
- "Search findings?" -> GET /findings/
- "Get finding details?" -> GET /findings/{id}/
- "Update a finding?" -> PUT /findings/{id}/
- "Partially update a finding?" -> PATCH /findings/{id}/
- "Create a report?" -> POST /findings/bulk/report/
- "Create a retest?" -> POST /findings/bulk/retest/
- "Create a update?" -> POST /findings/bulk/update/
- "List all report?" -> GET /findings/report/
- "Search frameworks?" -> GET /frameworks/
- "Get framework details?" -> GET /frameworks/{id}/
- "List all akamai?" -> GET /integrations/akamai/
- "Create a refresh?" -> POST /integrations/akamai/refresh/
- "List all aws?" -> GET /integrations/aws/
- "Create a refresh?" -> POST /integrations/aws/refresh/
- "List all azure-devops?" -> GET /integrations/azure-devops/
- "List all cloudflare?" -> GET /integrations/cloudflare/
- "Create a refresh?" -> POST /integrations/cloudflare/refresh/
- "List all jira-server?" -> GET /integrations/jira-server/
- "List all postman?" -> GET /integrations/postman/
- "Create a postman?" -> POST /integrations/postman/
- "Search findings?" -> GET /labels/findings/
- "Create a finding?" -> POST /labels/findings/
- "Get finding details?" -> GET /labels/findings/{id}/
- "Update a finding?" -> PUT /labels/findings/{id}/
- "Partially update a finding?" -> PATCH /labels/findings/{id}/
- "Delete a finding?" -> DELETE /labels/findings/{id}/
- "Search targets?" -> GET /labels/targets/
- "Create a target?" -> POST /labels/targets/
- "Get target details?" -> GET /labels/targets/{id}/
- "Update a target?" -> PUT /labels/targets/{id}/
- "Partially update a target?" -> PATCH /labels/targets/{id}/
- "Delete a target?" -> DELETE /labels/targets/{id}/
- "Search users?" -> GET /labels/users/
- "Create a user?" -> POST /labels/users/
- "Get user details?" -> GET /labels/users/{id}/
- "Update a user?" -> PUT /labels/users/{id}/
- "Partially update a user?" -> PATCH /labels/users/{id}/
- "Delete a user?" -> DELETE /labels/users/{id}/
- "Search permissions?" -> GET /permissions/
- "List all plans?" -> GET /plans/
- "Search profile?" -> GET /profile/
- "Create a accept_to?" -> POST /profile/accept_tos/
- "Create a change_password?" -> POST /profile/change_password/
- "List all notifications?" -> GET /profile/notifications/
- "List all permissions?" -> GET /profile/permissions/
- "Search roles?" -> GET /profile/roles/
- "Search targets?" -> GET /profile/targets/
- "Search report?" -> GET /report/
- "Create a report?" -> POST /report/
- "Get report details?" -> GET /report/{id}/
- "Update a report?" -> PUT /report/{id}/
- "Partially update a report?" -> PATCH /report/{id}/
- "List all download?" -> GET /report/{id}/download/
- "List all status?" -> GET /report/{id}/status/
- "List all types?" -> GET /report/types/
- "Search roles?" -> GET /roles/
- "Create a role?" -> POST /roles/
- "Get role details?" -> GET /roles/{id}/
- "Update a role?" -> PUT /roles/{id}/
- "Partially update a role?" -> PATCH /roles/{id}/
- "Delete a role?" -> DELETE /roles/{id}/
- "Search scan-profiles?" -> GET /scan-profiles/
- "Create a scan-profile?" -> POST /scan-profiles/
- "Get scan-profile details?" -> GET /scan-profiles/{id}/
- "Update a scan-profile?" -> PUT /scan-profiles/{id}/
- "Partially update a scan-profile?" -> PATCH /scan-profiles/{id}/
- "Search scanning-agents?" -> GET /scanning-agents/
- "Create a scanning-agent?" -> POST /scanning-agents/
- "List all config-files?" -> GET /scanning-agents/{hek}/config-files/
- "Get scanning-agent details?" -> GET /scanning-agents/{id}/
- "Update a scanning-agent?" -> PUT /scanning-agents/{id}/
- "Partially update a scanning-agent?" -> PATCH /scanning-agents/{id}/
- "Delete a scanning-agent?" -> DELETE /scanning-agents/{id}/
- "Create a generate?" -> POST /scanning-agents/{id}/generate/
- "Search scans?" -> GET /scans/
- "Get scan details?" -> GET /scans/{id}/
- "Create a cancel?" -> POST /scans/bulk/cancel/
- "Create a pause?" -> POST /scans/bulk/pause/
- "Create a resume?" -> POST /scans/bulk/resume/
- "Create a start?" -> POST /scans/bulk/start/
- "List all warnings?" -> GET /scans/warnings/
- "Get warning details?" -> GET /scans/warnings/{id}/
- "Search scheduledscans?" -> GET /scheduledscans/
- "Create a bulk?" -> POST /scheduledscans/bulk/
- "Search stored-reports?" -> GET /stored-reports/
- "Create a stored-report?" -> POST /stored-reports/
- "Get stored-report details?" -> GET /stored-reports/{id}/
- "Update a stored-report?" -> PUT /stored-reports/{id}/
- "Partially update a stored-report?" -> PATCH /stored-reports/{id}/
- "Delete a stored-report?" -> DELETE /stored-reports/{id}/
- "Create a generate?" -> POST /stored-reports/{id}/generate/
- "Create a preview?" -> POST /stored-reports/preview/
- "Search targets?" -> GET /targets/
- "Create a target?" -> POST /targets/
- "Get target details?" -> GET /targets/{id}/
- "Update a target?" -> PUT /targets/{id}/
- "Partially update a target?" -> PATCH /targets/{id}/
- "Delete a target?" -> DELETE /targets/{id}/
- "List all average_fix_time?" -> GET /targets/{id}/average_fix_time/
- "Create a check_api_login?" -> POST /targets/{id}/check_api_login/
- "List all download_api_schema_file?" -> GET /targets/{id}/download_api_schema_file/
- "List all get_postman_collection_folders?" -> GET /targets/{id}/get_postman_collection_folders/
- "List all azure-devops?" -> GET /targets/{id}/integrations/azure-devops/
- "List all jira-cloud?" -> GET /targets/{id}/integrations/jira-cloud/
- "List all jira-server?" -> GET /targets/{id}/integrations/jira-server/
- "List all slack?" -> GET /targets/{id}/integrations/slack/
- "List all login-video?" -> GET /targets/{id}/login-video/
- "List all mle?" -> GET /targets/{id}/mle/
- "Create a move-team?" -> POST /targets/{id}/move-team/
- "List all mtls?" -> GET /targets/{id}/mtls/
- "Create a reset?" -> POST /targets/{id}/otp/reset/
- "List all postman-authentication?" -> GET /targets/{id}/postman-authentication/
- "List all risk_trend?" -> GET /targets/{id}/risk_trend/
- "Create a scan_now?" -> POST /targets/{id}/scan_now/
- "List all severity_trend?" -> GET /targets/{id}/severity_trend/
- "List all signature?" -> GET /targets/{id}/signature/
- "List all top_vulns?" -> GET /targets/{id}/top_vulns/
- "Create a upload_api_schema_file?" -> POST /targets/{id}/upload_api_schema_file/
- "List all azure-devops?" -> GET /targets/{scope}/findings/{id}/integrations/azure-devops/
- "List all jira-cloud?" -> GET /targets/{scope}/findings/{id}/integrations/jira-cloud/
- "List all jira-server?" -> GET /targets/{scope}/findings/{id}/integrations/jira-server/
- "Search assets?" -> GET /targets/{target_id}/assets/
- "Create a asset?" -> POST /targets/{target_id}/assets/
- "Get asset details?" -> GET /targets/{target_id}/assets/{id}/
- "Update a asset?" -> PUT /targets/{target_id}/assets/{id}/
- "Partially update a asset?" -> PATCH /targets/{target_id}/assets/{id}/
- "Delete a asset?" -> DELETE /targets/{target_id}/assets/{id}/
- "Search events?" -> GET /targets/{target_id}/events/
- "Get event details?" -> GET /targets/{target_id}/events/{id}/
- "Search findings?" -> GET /targets/{target_id}/findings/
- "Search logs?" -> GET /targets/{target_id}/findings/{finding_id}/logs/
- "Get finding details?" -> GET /targets/{target_id}/findings/{id}/
- "Update a finding?" -> PUT /targets/{target_id}/findings/{id}/
- "Partially update a finding?" -> PATCH /targets/{target_id}/findings/{id}/
- "Create a retest?" -> POST /targets/{target_id}/findings/{id}/retest/
- "Create a report?" -> POST /targets/{target_id}/findings/bulk/report/
- "Create a retest?" -> POST /targets/{target_id}/findings/bulk/retest/
- "Create a update?" -> POST /targets/{target_id}/findings/bulk/update/
- "List all report?" -> GET /targets/{target_id}/findings/report/
- "Search logout?" -> GET /targets/{target_id}/logout/
- "Create a logout?" -> POST /targets/{target_id}/logout/
- "Get logout details?" -> GET /targets/{target_id}/logout/{id}/
- "Update a logout?" -> PUT /targets/{target_id}/logout/{id}/
- "Partially update a logout?" -> PATCH /targets/{target_id}/logout/{id}/
- "Delete a logout?" -> DELETE /targets/{target_id}/logout/{id}/
- "Search reduced-scopes?" -> GET /targets/{target_id}/reduced-scopes/
- "Create a reduced-scope?" -> POST /targets/{target_id}/reduced-scopes/
- "Get reduced-scope details?" -> GET /targets/{target_id}/reduced-scopes/{id}/
- "Update a reduced-scope?" -> PUT /targets/{target_id}/reduced-scopes/{id}/
- "Partially update a reduced-scope?" -> PATCH /targets/{target_id}/reduced-scopes/{id}/
- "Delete a reduced-scope?" -> DELETE /targets/{target_id}/reduced-scopes/{id}/
- "List all scan?" -> GET /targets/{target_id}/scan/
- "Create a cancel?" -> POST /targets/{target_id}/scan/cancel/
- "Create a pause?" -> POST /targets/{target_id}/scan/pause/
- "Create a resume?" -> POST /targets/{target_id}/scan/resume/
- "Search scans?" -> GET /targets/{target_id}/scans/
- "Get scan details?" -> GET /targets/{target_id}/scans/{id}/
- "Update a scan?" -> PUT /targets/{target_id}/scans/{id}/
- "Partially update a scan?" -> PATCH /targets/{target_id}/scans/{id}/
- "Create a cancel?" -> POST /targets/{target_id}/scans/{id}/cancel/
- "List all endpoints?" -> GET /targets/{target_id}/scans/{id}/endpoints/
- "Create a pause?" -> POST /targets/{target_id}/scans/{id}/pause/
- "List all report?" -> GET /targets/{target_id}/scans/{id}/report/
- "Create a resume?" -> POST /targets/{target_id}/scans/{id}/resume/
- "List all dates?" -> GET /targets/{target_id}/scans/dates/
- "List all retrieve_page?" -> GET /targets/{target_id}/scans/retrieve_page/
- "Search scheduledscans?" -> GET /targets/{target_id}/scheduledscans/
- "Create a scheduledscan?" -> POST /targets/{target_id}/scheduledscans/
- "Get scheduledscan details?" -> GET /targets/{target_id}/scheduledscans/{id}/
- "Update a scheduledscan?" -> PUT /targets/{target_id}/scheduledscans/{id}/
- "Partially update a scheduledscan?" -> PATCH /targets/{target_id}/scheduledscans/{id}/
- "Delete a scheduledscan?" -> DELETE /targets/{target_id}/scheduledscans/{id}/
- "List all expanded?" -> GET /targets/{target_id}/scheduledscans/expanded/
- "Search sequences?" -> GET /targets/{target_id}/sequences/
- "Create a sequence?" -> POST /targets/{target_id}/sequences/
- "Get sequence details?" -> GET /targets/{target_id}/sequences/{id}/
- "Update a sequence?" -> PUT /targets/{target_id}/sequences/{id}/
- "Partially update a sequence?" -> PATCH /targets/{target_id}/sequences/{id}/
- "Delete a sequence?" -> DELETE /targets/{target_id}/sequences/{id}/
- "Create a order?" -> POST /targets/{target_id}/sequences/{id}/order/
- "Search webhooks?" -> GET /targets/{target_id}/webhooks/
- "Create a webhook?" -> POST /targets/{target_id}/webhooks/
- "Get webhook details?" -> GET /targets/{target_id}/webhooks/{id}/
- "Update a webhook?" -> PUT /targets/{target_id}/webhooks/{id}/
- "Partially update a webhook?" -> PATCH /targets/{target_id}/webhooks/{id}/
- "Delete a webhook?" -> DELETE /targets/{target_id}/webhooks/{id}/
- "List all average_fix_time?" -> GET /targets/all/average_fix_time/
- "List all needs_attention_pie?" -> GET /targets/all/needs_attention_pie/
- "List all needs_attention_top?" -> GET /targets/all/needs_attention_top/
- "List all risk_trend?" -> GET /targets/all/risk_trend/
- "List all scans?" -> GET /targets/all/scans/
- "List all expanded?" -> GET /targets/all/scheduledscans/expanded/
- "List all severity_trend?" -> GET /targets/all/severity_trend/
- "List all top_vulns?" -> GET /targets/all/top_vulns/
- "Search assets?" -> GET /targets/assets/
- "Create a delete?" -> POST /targets/bulk/delete/
- "Create a move-team?" -> POST /targets/bulk/move-team/
- "Create a update?" -> POST /targets/bulk/update/
- "List all download?" -> GET /targets/download/
- "Search sequences?" -> GET /targets/sequences/
- "Create a upload?" -> POST /targets/upload/
- "Search teams?" -> GET /teams/
- "Create a team?" -> POST /teams/
- "Get team details?" -> GET /teams/{id}/
- "Update a team?" -> PUT /teams/{id}/
- "Partially update a team?" -> PATCH /teams/{id}/
- "Delete a team?" -> DELETE /teams/{id}/
- "List all available-slots?" -> GET /teams/available-slots/
- "List all user-roles?" -> GET /user-roles/
- "Create a user-role?" -> POST /user-roles/
- "Get user-role details?" -> GET /user-roles/{id}/
- "Update a user-role?" -> PUT /user-roles/{id}/
- "Partially update a user-role?" -> PATCH /user-roles/{id}/
- "Delete a user-role?" -> DELETE /user-roles/{id}/
- "Create a create?" -> POST /user-roles/bulk/create/
- "Create a delete?" -> POST /user-roles/bulk/delete/
- "Create a operation?" -> POST /user-roles/bulk/operations/
- "Create a update?" -> POST /user-roles/bulk/update/
- "Search users?" -> GET /users/
- "Create a user?" -> POST /users/
- "Get user details?" -> GET /users/{id}/
- "Update a user?" -> PUT /users/{id}/
- "Partially update a user?" -> PATCH /users/{id}/
- "Delete a user?" -> DELETE /users/{id}/
- "Search targets?" -> GET /users/{user_id}/targets/
- "Create a update?" -> POST /users/bulk/update/
- "Search webhooks?" -> GET /webhooks/
- "Create a webhook?" -> POST /webhooks/
- "Get webhook details?" -> GET /webhooks/{id}/
- "Update a webhook?" -> PUT /webhooks/{id}/
- "Partially update a webhook?" -> PATCH /webhooks/{id}/
- "Delete a webhook?" -> DELETE /webhooks/{id}/
- "Search targets?" -> GET /wizard/targets
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
