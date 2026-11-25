---
name: data-api
description: "Data API skill. Use when working with Data for contacts, district_admins, districts. Covers 44 endpoints."
version: 1.0.0
generator: lapsh
---

# Data API
API version: 1.2.0

## Auth
OAuth2

## Base URL
https://api.clever.com/v1.2

## Setup
1. Configure auth: OAuth2
2. GET /contacts -- verify access

## Endpoints

44 endpoints across 8 groups. See references/api-spec.lap for full details.

### contacts
| Method | Path | Description |
|--------|------|-------------|
| GET | /contacts | Returns a list of student contacts |
| GET | /contacts/{id} | Returns a specific student contact |
| GET | /contacts/{id}/district | Returns the district for a student contact |
| GET | /contacts/{id}/student | Returns the student for a student contact |

### district_admins
| Method | Path | Description |
|--------|------|-------------|
| GET | /district_admins | Returns a list of district admins |
| GET | /district_admins/{id} | Returns a specific district admin |

### districts
| Method | Path | Description |
|--------|------|-------------|
| GET | /districts | Returns a list of districts. In practice this will only return the one district associated with the bearer token |
| GET | /districts/{id} | Returns a specific district |
| GET | /districts/{id}/admins | Returns the admins for a district |
| GET | /districts/{id}/schools | Returns the schools for a district |
| GET | /districts/{id}/sections | Returns the sections for a district |
| GET | /districts/{id}/status | Returns the status of the district |
| GET | /districts/{id}/students | Returns the students for a district |
| GET | /districts/{id}/teachers | Returns the teachers for a district |

### school_admins
| Method | Path | Description |
|--------|------|-------------|
| GET | /school_admins | Returns a list of school admins |
| GET | /school_admins/{id} | Returns a specific school admin |
| GET | /school_admins/{id}/schools | Returns the schools for a school admin |

### schools
| Method | Path | Description |
|--------|------|-------------|
| GET | /schools | Returns a list of schools |
| GET | /schools/{id} | Returns a specific school |
| GET | /schools/{id}/district | Returns the district for a school |
| GET | /schools/{id}/sections | Returns the sections for a school |
| GET | /schools/{id}/students | Returns the students for a school |
| GET | /schools/{id}/teachers | Returns the teachers for a school |

### sections
| Method | Path | Description |
|--------|------|-------------|
| GET | /sections | Returns a list of sections |
| GET | /sections/{id} | Returns a specific section |
| GET | /sections/{id}/district | Returns the district for a section |
| GET | /sections/{id}/school | Returns the school for a section |
| GET | /sections/{id}/students | Returns the students for a section |
| GET | /sections/{id}/teacher | Returns the primary teacher for a section |
| GET | /sections/{id}/teachers | Returns the teachers for a section |

### students
| Method | Path | Description |
|--------|------|-------------|
| GET | /students | Returns a list of students |
| GET | /students/{id} | Returns a specific student |
| GET | /students/{id}/contacts | Returns the contacts for a student |
| GET | /students/{id}/district | Returns the district for a student |
| GET | /students/{id}/school | Returns the primary school for a student |
| GET | /students/{id}/sections | Returns the sections for a student |
| GET | /students/{id}/teachers | Returns the teachers for a student |

### teachers
| Method | Path | Description |
|--------|------|-------------|
| GET | /teachers | Returns a list of teachers |
| GET | /teachers/{id} | Returns a specific teacher |
| GET | /teachers/{id}/district | Returns the district for a teacher |
| GET | /teachers/{id}/grade_levels | Returns the grade levels for sections a teacher teaches |
| GET | /teachers/{id}/school | Retrieves school info for a teacher. |
| GET | /teachers/{id}/sections | Returns the sections for a teacher |
| GET | /teachers/{id}/students | Returns the students for a teacher |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all contacts?" -> GET /contacts
- "Get contact details?" -> GET /contacts/{id}
- "List all district?" -> GET /contacts/{id}/district
- "List all student?" -> GET /contacts/{id}/student
- "List all district_admins?" -> GET /district_admins
- "Get district_admin details?" -> GET /district_admins/{id}
- "List all districts?" -> GET /districts
- "Get district details?" -> GET /districts/{id}
- "List all admins?" -> GET /districts/{id}/admins
- "List all schools?" -> GET /districts/{id}/schools
- "List all sections?" -> GET /districts/{id}/sections
- "List all status?" -> GET /districts/{id}/status
- "List all students?" -> GET /districts/{id}/students
- "List all teachers?" -> GET /districts/{id}/teachers
- "List all school_admins?" -> GET /school_admins
- "Get school_admin details?" -> GET /school_admins/{id}
- "List all schools?" -> GET /school_admins/{id}/schools
- "List all schools?" -> GET /schools
- "Get school details?" -> GET /schools/{id}
- "List all district?" -> GET /schools/{id}/district
- "List all sections?" -> GET /schools/{id}/sections
- "List all students?" -> GET /schools/{id}/students
- "List all teachers?" -> GET /schools/{id}/teachers
- "List all sections?" -> GET /sections
- "Get section details?" -> GET /sections/{id}
- "List all district?" -> GET /sections/{id}/district
- "List all school?" -> GET /sections/{id}/school
- "List all students?" -> GET /sections/{id}/students
- "List all teacher?" -> GET /sections/{id}/teacher
- "List all teachers?" -> GET /sections/{id}/teachers
- "List all students?" -> GET /students
- "Get student details?" -> GET /students/{id}
- "List all contacts?" -> GET /students/{id}/contacts
- "List all district?" -> GET /students/{id}/district
- "List all school?" -> GET /students/{id}/school
- "List all sections?" -> GET /students/{id}/sections
- "List all teachers?" -> GET /students/{id}/teachers
- "List all teachers?" -> GET /teachers
- "Get teacher details?" -> GET /teachers/{id}
- "List all district?" -> GET /teachers/{id}/district
- "List all grade_levels?" -> GET /teachers/{id}/grade_levels
- "List all school?" -> GET /teachers/{id}/school
- "List all sections?" -> GET /teachers/{id}/sections
- "List all students?" -> GET /teachers/{id}/students
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
