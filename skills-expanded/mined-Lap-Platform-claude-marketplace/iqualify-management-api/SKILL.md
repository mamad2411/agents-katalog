---
name: iqualify-management-api
description: "iQualify Management API skill. Use when working with iQualify Management for root, offerings, course-mappings. Covers 84 endpoints."
version: 1.0.0
generator: lapsh
---

# iQualify Management API
API version: v1

## Auth
ApiKey Authorization in header

## Base URL
https://api.iqualify.com/v1

## Setup
1. Set your API key in the appropriate header
2. GET / -- verify access
3. POST /offerings/{offeringId}/groups -- create first groups

## Endpoints

84 endpoints across 6 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | List supported endpoints URLs |

### offerings
| Method | Path | Description |
|--------|------|-------------|
| GET | /offerings/{offeringId}/analytics/pulses | Find all pulse IDs in the specified offering |
| GET | /offerings/{offeringId}/analytics/pulses/responses | Find pulses by offeringId |
| GET | /offerings/{offeringId}/analytics/pulses/{pulseId}/responses | Find pulses by offeringId and pulseId |
| GET | /offerings/{offeringId}/analytics/marks/assignments | Find assessment marks |
| GET | /offerings/{offeringId}/analytics/marks/quizzes | Find quiz marks |
| GET | /offerings/{offeringId}/analytics/learners-progress | Find learner progress in a specified offering |
| GET | /offerings/{offeringId}/analytics/unit-reactions | Find unit reactions |
| GET | /offerings/{offeringId}/analytics/submissions/assignments | Find submissions to assessments, including marks if any |
| GET | /offerings/{offeringId}/analytics/social-notes | Find shared social notes in an offering |
| GET | /offerings/{offeringId}/analytics/activities/responses | Find open response activity attempts |
| GET | /offerings/{offeringId}/analytics/submissions/open-response/{assessmentId} | Find submissions to a specified open response assessment, including marks if any |
| GET | /offerings/{offeringId}/analytics/submissions/{userEmail}/assignments/{assessmentId} | Find a learner's submission to a specified assessment, including marks if any |
| GET | /offerings/{offeringId}/groups | Find assessment groups |
| POST | /offerings/{offeringId}/groups | Add an assessment group |
| GET | /offerings/{offeringId}/groups/{groupId}/learners | Find learners in an assessment group |
| POST | /offerings/{offeringId}/groups/{groupId}/learners | Add a learner to an assessment group |
| DELETE | /offerings/{offeringId}/groups/{groupId}/learners/{userEmail} | Remove a learner from an assessment group |
| GET | /offerings/{offeringId}/analytics/channels/{channelId}/posts | Find posts |
| GET | /offerings/{offeringId}/analytics/channels/{channelId}/comments | Find comments |
| GET | /offerings/{offeringId}/analytics/channels/{channelId}/replies | Find replies |
| GET | /offerings/{offeringId}/channels | Find channels |
| POST | /offerings/{offeringId}/channels | Add channel |
| PATCH | /offerings/{offeringId}/channels/{channelId} | Update channel |
| POST | /offerings/{offeringId}/channels/{channelId}/learners | Add learners to a group channel |
| DELETE | /offerings/{offeringId}/channels/{channelId}/learners | Remove learners from a group channel |
| GET | /offerings/{offeringId}/channels/{channelId}/learners | Find learners in a group channel |
| GET | /offerings | Find current, past and future offerings |
| POST | /offerings | Create offering |
| GET | /offerings/summary | Offerings summary |
| GET | /offerings/current | Find active offerings |
| GET | /offerings/past | Find past offerings |
| GET | /offerings/future | Find scheduled offerings |
| GET | /offerings/info/{textPattern} | Find offerings where info field matches the specified textPattern |
| GET | /offerings/{offeringId} | Find offering by ID |
| PATCH | /offerings/{offeringId} | Update offering |
| GET | /offerings/{offeringId}/badges | Find offering badges |
| PUT | /offerings/{offeringId}/metadata/tags | Update offering tags metadata |
| PUT | /offerings/{offeringId}/metadata/category | Update offering category metadata |
| PUT | /offerings/{offeringId}/metadata/topic | Update offering topic metadata |
| PUT | /offerings/{offeringId}/metadata/level | Update offering level metadata |
| GET | /offerings/{offeringId}/assessments | Find offering's assessments |
| PATCH | /offerings/{offeringId}/assessments/{assessmentId} | Update assessment details |
| PATCH | /offerings/{offeringId}/assessments/{assessmentId}/{userEmail} | Update the due dates for a learner's quiz attempt |
| DELETE | /offerings/{offeringId}/assessments/{assessmentId}/documents/{documentId} | Remove assessment document |
| GET | /offerings/{offeringId}/learners/pending-submission | Find learners with assessments pending x days before due date within the specified offeringId |
| GET | /offerings/{offeringId}/activities/openresponse | Find offering's activities |
| GET | /offerings/{offeringId}/users | Find offering's users |
| POST | /offerings/{offeringId}/users | Adds user to the offering |
| DELETE | /offerings/{offeringId}/users/{userEmail} | Removes user from the offering |
| GET | /offerings/{offeringId}/users/{markerEmail}/marks | Find Learners marked by a coach |
| POST | /offerings/{offeringId}/users/{markerEmail}/marks | Add learners to be marked by a coach |
| DELETE | /offerings/{offeringId}/users/{markerEmail}/marks | Remove learners from coach's marking list |
| POST | /offerings/{offeringId}/users/{userEmail}/badges/award | Award badge |
| GET | /offerings/{offeringId}/users/{userEmail}/submissions/open-response | Find learner's open response assessment submissions |
| DELETE | /offerings/{offeringId}/users/{userEmail}/assessments/{assessmentId} | Reset user's assessment to draft state |

### course-mappings
| Method | Path | Description |
|--------|------|-------------|
| GET | /course-mappings | Find course mappings |
| GET | /course-mappings/externalcourse/{externalCourseId} | Find course mappings by externalCourseId |
| GET | /course-mappings/{offeringId} | Find course mappings by offeringId |
| PUT | /course-mappings/{offeringId}/{externalCourseId} | Add course mapping |
| DELETE | /course-mappings/{offeringId}/{externalCourseId} | Remove course mapping |

### courses
| Method | Path | Description |
|--------|------|-------------|
| GET | /courses | Find courses |
| GET | /courses/{contentId} | Find course by contentId |
| GET | /courses/{contentId}/activations | Find activations for a contentId |
| PUT | /courses/{contentId}/metadata/tags | Update course tags |
| PUT | /courses/{contentId}/metadata/category | Update course category |
| PUT | /courses/{contentId}/metadata/level | Update course level |
| PUT | /courses/{contentId}/metadata/topic | Update course topic |
| POST | /courses/{rootContentId}/permissions/{userEmail} | Update course access |
| GET | /courses/{contentId}/permissions | Find users who have access to the contentId provided |

### org
| Method | Path | Description |
|--------|------|-------------|
| GET | /org | Gets the current organisation |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/{userEmail} | Find user by email |
| PATCH | /users/{userEmail} | Update user |
| PUT | /users/{userEmail}/suspend | Suspend user |
| GET | /users/{userEmail}/offerings | Find user's offerings |
| POST | /users/{userEmail}/offerings | Adds the user to the specified offerings as a learner |
| GET | /users/{userEmail}/offerings/{offeringId}/progress | Find learner's progress in a specified offering |
| POST | /users/{userEmail}/permissions/{permissionName} | Add permission to user |
| GET | /users/all/progress | Find learner progress in all offerings |
| GET | /users/{userEmail}/progress | Find learner's progress in offerings |
| GET | /users/{userEmail}/badges | Find user's badges |
| PATCH | /users/{userEmail}/transfer | Transfer a user between offerings |
| POST | /users/{userEmail}/invite-email | Resend invitation email |
| POST | /users | Add new user |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all pulses?" -> GET /offerings/{offeringId}/analytics/pulses
- "List all responses?" -> GET /offerings/{offeringId}/analytics/pulses/responses
- "List all responses?" -> GET /offerings/{offeringId}/analytics/pulses/{pulseId}/responses
- "List all assignments?" -> GET /offerings/{offeringId}/analytics/marks/assignments
- "List all quizzes?" -> GET /offerings/{offeringId}/analytics/marks/quizzes
- "List all learners-progress?" -> GET /offerings/{offeringId}/analytics/learners-progress
- "List all unit-reactions?" -> GET /offerings/{offeringId}/analytics/unit-reactions
- "List all assignments?" -> GET /offerings/{offeringId}/analytics/submissions/assignments
- "List all social-notes?" -> GET /offerings/{offeringId}/analytics/social-notes
- "List all responses?" -> GET /offerings/{offeringId}/analytics/activities/responses
- "Get open-response details?" -> GET /offerings/{offeringId}/analytics/submissions/open-response/{assessmentId}
- "Get assignment details?" -> GET /offerings/{offeringId}/analytics/submissions/{userEmail}/assignments/{assessmentId}
- "List all groups?" -> GET /offerings/{offeringId}/groups
- "Create a group?" -> POST /offerings/{offeringId}/groups
- "List all learners?" -> GET /offerings/{offeringId}/groups/{groupId}/learners
- "Create a learner?" -> POST /offerings/{offeringId}/groups/{groupId}/learners
- "Delete a learner?" -> DELETE /offerings/{offeringId}/groups/{groupId}/learners/{userEmail}
- "List all posts?" -> GET /offerings/{offeringId}/analytics/channels/{channelId}/posts
- "List all comments?" -> GET /offerings/{offeringId}/analytics/channels/{channelId}/comments
- "List all replies?" -> GET /offerings/{offeringId}/analytics/channels/{channelId}/replies
- "List all channels?" -> GET /offerings/{offeringId}/channels
- "Create a channel?" -> POST /offerings/{offeringId}/channels
- "Partially update a channel?" -> PATCH /offerings/{offeringId}/channels/{channelId}
- "Create a learner?" -> POST /offerings/{offeringId}/channels/{channelId}/learners
- "List all learners?" -> GET /offerings/{offeringId}/channels/{channelId}/learners
- "List all course-mappings?" -> GET /course-mappings
- "Get externalcourse details?" -> GET /course-mappings/externalcourse/{externalCourseId}
- "Get course-mapping details?" -> GET /course-mappings/{offeringId}
- "Update a course-mapping?" -> PUT /course-mappings/{offeringId}/{externalCourseId}
- "Delete a course-mapping?" -> DELETE /course-mappings/{offeringId}/{externalCourseId}
- "List all courses?" -> GET /courses
- "Get course details?" -> GET /courses/{contentId}
- "List all activations?" -> GET /courses/{contentId}/activations
- "List all permissions?" -> GET /courses/{contentId}/permissions
- "List all offerings?" -> GET /offerings
- "Create a offering?" -> POST /offerings
- "List all summary?" -> GET /offerings/summary
- "List all current?" -> GET /offerings/current
- "List all past?" -> GET /offerings/past
- "List all future?" -> GET /offerings/future
- "Get info details?" -> GET /offerings/info/{textPattern}
- "Get offering details?" -> GET /offerings/{offeringId}
- "Partially update a offering?" -> PATCH /offerings/{offeringId}
- "List all badges?" -> GET /offerings/{offeringId}/badges
- "List all assessments?" -> GET /offerings/{offeringId}/assessments
- "Partially update a assessment?" -> PATCH /offerings/{offeringId}/assessments/{assessmentId}
- "Partially update a assessment?" -> PATCH /offerings/{offeringId}/assessments/{assessmentId}/{userEmail}
- "Delete a document?" -> DELETE /offerings/{offeringId}/assessments/{assessmentId}/documents/{documentId}
- "List all pending-submission?" -> GET /offerings/{offeringId}/learners/pending-submission
- "List all openresponse?" -> GET /offerings/{offeringId}/activities/openresponse
- "List all users?" -> GET /offerings/{offeringId}/users
- "Create a user?" -> POST /offerings/{offeringId}/users
- "Delete a user?" -> DELETE /offerings/{offeringId}/users/{userEmail}
- "List all marks?" -> GET /offerings/{offeringId}/users/{markerEmail}/marks
- "Create a mark?" -> POST /offerings/{offeringId}/users/{markerEmail}/marks
- "Create a award?" -> POST /offerings/{offeringId}/users/{userEmail}/badges/award
- "List all open-response?" -> GET /offerings/{offeringId}/users/{userEmail}/submissions/open-response
- "Delete a assessment?" -> DELETE /offerings/{offeringId}/users/{userEmail}/assessments/{assessmentId}
- "List all org?" -> GET /org
- "Get user details?" -> GET /users/{userEmail}
- "Partially update a user?" -> PATCH /users/{userEmail}
- "List all offerings?" -> GET /users/{userEmail}/offerings
- "Create a offering?" -> POST /users/{userEmail}/offerings
- "List all progress?" -> GET /users/{userEmail}/offerings/{offeringId}/progress
- "List all progress?" -> GET /users/all/progress
- "List all progress?" -> GET /users/{userEmail}/progress
- "List all badges?" -> GET /users/{userEmail}/badges
- "Create a invite-email?" -> POST /users/{userEmail}/invite-email
- "Create a user?" -> POST /users
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
