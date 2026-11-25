---
name: appveyor-rest-api
description: "AppVeyor REST API skill. Use when working with AppVeyor REST for users, user, collaborators. Covers 53 endpoints."
version: 1.0.0
generator: lapsh
---

# AppVeyor REST API
API version: 1.0.0

## Auth
ApiKey Authorization in header

## Base URL
https://ci.appveyor.com/api

## Setup
1. Set your API key in the appropriate header
2. GET /users -- verify access
3. POST /users/invitations -- create first invitations

## Endpoints

53 endpoints across 10 groups. See references/api-spec.lap for full details.

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | Get users |
| PUT | /users | Update user |
| GET | /users/{userId} | Get user |
| DELETE | /users/{userId} | Delete user |
| GET | /users/invitations | Get user invitations |
| POST | /users/invitations | Invite user |
| DELETE | /users/invitations/{userInvitationId} | Cancel user invitation |

### user
| Method | Path | Description |
|--------|------|-------------|
| PUT | /user/join-account | Join Account |

### collaborators
| Method | Path | Description |
|--------|------|-------------|
| GET | /collaborators | Get collaborators |
| PUT | /collaborators | Update collaborator |
| GET | /collaborators/{userId} | Get collaborator |
| DELETE | /collaborators/{userId} | Delete collaborator |

### roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /roles | Get roles |
| POST | /roles | Add role |
| PUT | /roles | Update role |
| GET | /roles/{roleId} | Get role |
| DELETE | /roles/{roleId} | Delete role |

### account
| Method | Path | Description |
|--------|------|-------------|
| POST | /account/encrypt | Encrypt a value for use in StoredValue. |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects | Get projects |
| POST | /projects | Add project |
| PUT | /projects | Update project |
| GET | /projects/{accountName}/{projectSlug} | Get project last build |
| DELETE | /projects/{accountName}/{projectSlug} | Delete project |
| GET | /projects/{accountName}/{projectSlug}/branch/{buildBranch} | Get project last branch build |
| GET | /projects/{accountName}/{projectSlug}/build/{buildVersion} | Get project build by version |
| GET | /projects/{accountName}/{projectSlug}/history | Get project history |
| GET | /projects/{accountName}/{projectSlug}/artifacts/{artifactFileName} | Get last successful build artifact |
| GET | /projects/{accountName}/{projectSlug}/deployments | Get project deployments |
| GET | /projects/{accountName}/{projectSlug}/settings | Get project settings |
| GET | /projects/{accountName}/{projectSlug}/settings/yaml | Get project settings in YAML |
| PUT | /projects/{accountName}/{projectSlug}/settings/yaml | Update project settings in YAML |
| PUT | /projects/{accountName}/{projectSlug}/settings/build-number | Update project build number |
| GET | /projects/{accountName}/{projectSlug}/settings/environment-variables | Get project environment variables |
| PUT | /projects/{accountName}/{projectSlug}/settings/environment-variables | Update project environment variables |
| DELETE | /projects/{accountName}/{projectSlug}/buildcache | Delete project build cache |
| GET | /projects/status/{statusBadgeId} | Get project status badge image |
| GET | /projects/status/{statusBadgeId}/branch/{buildBranch} | Get project branch status badge image |
| GET | /projects/status/{badgeRepoProvider}/{repoAccountName}/{repoSlug} | Get status badge image for a project with a public repository |

### builds
| Method | Path | Description |
|--------|------|-------------|
| POST | /builds | Start build of branch most recent commit |
| PUT | /builds | Re-run build |
| DELETE | /builds/{accountName}/{projectSlug}/{buildVersion} | Cancel build |

### buildjobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /buildjobs/{jobId}/artifacts | Get build artifacts |
| GET | /buildjobs/{jobId}/artifacts/{artifactFileName} | Download build artifact |
| GET | /buildjobs/{jobId}/log | Download build log |

### environments
| Method | Path | Description |
|--------|------|-------------|
| GET | /environments | Get environments |
| POST | /environments | Add environment |
| PUT | /environments | Update environment |
| GET | /environments/{deploymentEnvironmentId}/settings | Get environment settings |
| GET | /environments/{deploymentEnvironmentId}/deployments | Get environment deployments |
| DELETE | /environments/{deploymentEnvironmentId} | Delete environment |

### deployments
| Method | Path | Description |
|--------|------|-------------|
| GET | /deployments/{deploymentId} | Get deployment |
| POST | /deployments | Start deployment |
| PUT | /deployments/stop | Cancel deployment |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all users?" -> GET /users
- "Get user details?" -> GET /users/{userId}
- "Delete a user?" -> DELETE /users/{userId}
- "List all invitations?" -> GET /users/invitations
- "Create a invitation?" -> POST /users/invitations
- "Delete a invitation?" -> DELETE /users/invitations/{userInvitationId}
- "List all collaborators?" -> GET /collaborators
- "Get collaborator details?" -> GET /collaborators/{userId}
- "Delete a collaborator?" -> DELETE /collaborators/{userId}
- "List all roles?" -> GET /roles
- "Create a role?" -> POST /roles
- "Get role details?" -> GET /roles/{roleId}
- "Delete a role?" -> DELETE /roles/{roleId}
- "Create a encrypt?" -> POST /account/encrypt
- "List all projects?" -> GET /projects
- "Create a project?" -> POST /projects
- "Get project details?" -> GET /projects/{accountName}/{projectSlug}
- "Delete a project?" -> DELETE /projects/{accountName}/{projectSlug}
- "Get branch details?" -> GET /projects/{accountName}/{projectSlug}/branch/{buildBranch}
- "Get build details?" -> GET /projects/{accountName}/{projectSlug}/build/{buildVersion}
- "List all history?" -> GET /projects/{accountName}/{projectSlug}/history
- "Get artifact details?" -> GET /projects/{accountName}/{projectSlug}/artifacts/{artifactFileName}
- "List all deployments?" -> GET /projects/{accountName}/{projectSlug}/deployments
- "List all settings?" -> GET /projects/{accountName}/{projectSlug}/settings
- "List all yaml?" -> GET /projects/{accountName}/{projectSlug}/settings/yaml
- "List all environment-variables?" -> GET /projects/{accountName}/{projectSlug}/settings/environment-variables
- "Get status details?" -> GET /projects/status/{statusBadgeId}
- "Get branch details?" -> GET /projects/status/{statusBadgeId}/branch/{buildBranch}
- "Get status details?" -> GET /projects/status/{badgeRepoProvider}/{repoAccountName}/{repoSlug}
- "Create a build?" -> POST /builds
- "Delete a build?" -> DELETE /builds/{accountName}/{projectSlug}/{buildVersion}
- "List all artifacts?" -> GET /buildjobs/{jobId}/artifacts
- "Get artifact details?" -> GET /buildjobs/{jobId}/artifacts/{artifactFileName}
- "List all log?" -> GET /buildjobs/{jobId}/log
- "List all environments?" -> GET /environments
- "Create a environment?" -> POST /environments
- "List all settings?" -> GET /environments/{deploymentEnvironmentId}/settings
- "List all deployments?" -> GET /environments/{deploymentEnvironmentId}/deployments
- "Delete a environment?" -> DELETE /environments/{deploymentEnvironmentId}
- "Get deployment details?" -> GET /deployments/{deploymentId}
- "Create a deployment?" -> POST /deployments
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
