---
name: contribly
description: "Contribly API skill. Use when working with Contribly for artifact-formats, assignments, change-log. Covers 44 endpoints."
version: 1.0.0
generator: lapsh
---

# Contribly
API version: 1.0.0

## Auth
OAuth2

## Base URL
https://api.contribly.com/1

## Setup
1. Configure auth: OAuth2
2. GET /artifact-formats -- verify access
3. POST /assignments -- create first assignments

## Endpoints

44 endpoints across 22 groups. See references/api-spec.lap for full details.

### artifact-formats
| Method | Path | Description |
|--------|------|-------------|
| GET | /artifact-formats | Artifact formats |

### assignments
| Method | Path | Description |
|--------|------|-------------|
| GET | /assignments | List assignments |
| POST | /assignments | Create a new assignment |
| DELETE | /assignments/{id} | Delete this assignment and all of it's contributions |
| GET | /assignments/{id} | Get a single assigment by id |

### change-log
| Method | Path | Description |
|--------|------|-------------|
| GET | /change-log | Recent changes |

### contribution-refinements
| Method | Path | Description |
|--------|------|-------------|
| GET | /contribution-refinements | List contribution refinement options |

### contribution-refinement-types
| Method | Path | Description |
|--------|------|-------------|
| GET | /contribution-refinement-types | List valid contribution refinement types |

### export
| Method | Path | Description |
|--------|------|-------------|
| POST | /export | Export contributions. |

### export-summary
| Method | Path | Description |
|--------|------|-------------|
| POST | /export-summary | Export contributions preflight summary. |

### exports
| Method | Path | Description |
|--------|------|-------------|
| GET | /exports/{id} | Get a single export job; poll to follow export progress. |

### contributions
| Method | Path | Description |
|--------|------|-------------|
| GET | /contributions | List contributions |
| POST | /contributions | Create a new contribution |
| GET | /contributions/{id} | Get a single contribution by id |
| DELETE | /contributions/{id} | Delete this contribution |
| POST | /contributions/{id}/flag | Raise a flag against this contribution |
| POST | /contributions/{id}/like | Allows a user to mark a contribution as liked |
| GET | /contributions/{id}/likes | List users who have liked this contributions |
| POST | /contributions/{id}/moderate | Perform a moderation action on this contribution |

### credentials
| Method | Path | Description |
|--------|------|-------------|
| GET | /credentials | List the credentials associated with the authenticated user. |

### event-types
| Method | Path | Description |
|--------|------|-------------|
| GET | /event-types | Event types |

### forms
| Method | Path | Description |
|--------|------|-------------|
| GET | /forms | List forms |
| POST | /forms | Create a form |
| GET | /forms/{id} | Get a single form by id |
| DELETE | /forms/{id} | Delete this form and all of it's responses. |

### form-responses
| Method | Path | Description |
|--------|------|-------------|
| POST | /form-responses | Submit a response to a form |
| GET | /form-responses | List form responses |
| GET | /form-responses/{id} | Get a single form response by id |

### media
| Method | Path | Description |
|--------|------|-------------|
| POST | /media | Submit a new media file |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /notifications/contributions/{id}/preview |  |

### scopes
| Method | Path | Description |
|--------|------|-------------|
| GET | /scopes | Scopes |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions | List subscriptions for the authorised user. |
| DELETE | /subscriptions/{id} | Delete a subscription. |

### subscription-types
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscription-types | Subscription types |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | List tags |
| POST | /tags | Create a new tag |
| GET | /tags/{id} | Retrieve a single tag by id |

### tagsets
| Method | Path | Description |
|--------|------|-------------|
| GET | /tagsets | List tag sets |
| POST | /tagsets | Create a new tag set |
| GET | /tagsets/{id} | Retrieve a single tag set by id |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | List users |
| GET | /users/{id} | Retrieve a single user by id |
| GET | /users/{id}/linked/{type} | Retrieve a users linked profile by type |

### verify
| Method | Path | Description |
|--------|------|-------------|
| POST | /verify | Verify token and return details of the owning user |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all artifact-formats?" -> GET /artifact-formats
- "Search assignments?" -> GET /assignments
- "Create a assignment?" -> POST /assignments
- "Delete a assignment?" -> DELETE /assignments/{id}
- "Get assignment details?" -> GET /assignments/{id}
- "List all change-log?" -> GET /change-log
- "Search contribution-refinements?" -> GET /contribution-refinements
- "List all contribution-refinement-types?" -> GET /contribution-refinement-types
- "Create a export?" -> POST /export
- "Create a export-summary?" -> POST /export-summary
- "Get export details?" -> GET /exports/{id}
- "Search contributions?" -> GET /contributions
- "Create a contribution?" -> POST /contributions
- "Get contribution details?" -> GET /contributions/{id}
- "Delete a contribution?" -> DELETE /contributions/{id}
- "Create a flag?" -> POST /contributions/{id}/flag
- "Create a like?" -> POST /contributions/{id}/like
- "List all likes?" -> GET /contributions/{id}/likes
- "Create a moderate?" -> POST /contributions/{id}/moderate
- "List all credentials?" -> GET /credentials
- "List all event-types?" -> GET /event-types
- "List all forms?" -> GET /forms
- "Create a form?" -> POST /forms
- "Get form details?" -> GET /forms/{id}
- "Delete a form?" -> DELETE /forms/{id}
- "Create a form-respons?" -> POST /form-responses
- "List all form-responses?" -> GET /form-responses
- "Get form-respons details?" -> GET /form-responses/{id}
- "Create a media?" -> POST /media
- "List all preview?" -> GET /notifications/contributions/{id}/preview
- "List all scopes?" -> GET /scopes
- "List all subscriptions?" -> GET /subscriptions
- "Delete a subscription?" -> DELETE /subscriptions/{id}
- "List all subscription-types?" -> GET /subscription-types
- "List all tags?" -> GET /tags
- "Create a tag?" -> POST /tags
- "Get tag details?" -> GET /tags/{id}
- "List all tagsets?" -> GET /tagsets
- "Create a tagset?" -> POST /tagsets
- "Get tagset details?" -> GET /tagsets/{id}
- "List all users?" -> GET /users
- "Get user details?" -> GET /users/{id}
- "Get linked details?" -> GET /users/{id}/linked/{type}
- "Create a verify?" -> POST /verify
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
