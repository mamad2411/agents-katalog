---
name: members-api
description: "Members API skill. Use when working with Members for api. Covers 43 endpoints."
version: 1.0.0
generator: lapsh
---

# Members API
API version: v1

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /api/Location/Constituency/Search -- verify access

## Endpoints

43 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/Location/Browse/{locationType}/{locationName} | Returns a list of locations, both parent and child |
| GET | /api/Location/Constituency/Search | Returns a list of constituencies |
| GET | /api/Location/Constituency/{id} | Returns a constituency by ID |
| GET | /api/Location/Constituency/{id}/Synopsis | Returns a synopsis by constituency ID |
| GET | /api/Location/Constituency/{id}/Representations | Returns a list of representations by constituency ID |
| GET | /api/Location/Constituency/{id}/Geometry | Returns geometry by constituency ID |
| GET | /api/Location/Constituency/{id}/ElectionResults | Returns a list of election results by constituency ID |
| GET | /api/Location/Constituency/{id}/ElectionResult/{electionId} | Returns an election result by constituency and election id |
| GET | /api/Location/Constituency/{id}/ElectionResult/Latest | Returns latest election result by constituency id |
| GET | /api/LordsInterests/Register | Returns a list of registered interests |
| GET | /api/LordsInterests/Staff | Returns a list of staff |
| GET | /api/Members/Search | Returns a list of current members of the Commons or Lords |
| GET | /api/Members/SearchHistorical | Returns a list of members of the Commons or Lords |
| GET | /api/Members/{id} | Return member by ID |
| GET | /api/Members/{id}/Biography | Return biography of member by ID |
| GET | /api/Members/{id}/Contact | Return list of contact details of member by ID |
| GET | /api/Members/{id}/ContributionSummary | Return contribution summary of member by ID |
| GET | /api/Members/{id}/Edms | Return list of early day motions of member by ID |
| GET | /api/Members/{id}/Experience | Return experience of member by ID |
| GET | /api/Members/{id}/Focus | Return list of areas of focus of member by ID |
| GET | /api/Members/History | Return members by ID with list of their historical names, parties and memberships |
| GET | /api/Members/{id}/LatestElectionResult | Return latest election result of member by ID |
| GET | /api/Members/{id}/Portrait | Return portrait of member by ID |
| GET | /api/Members/{id}/PortraitUrl | Return portrait url of member by ID |
| GET | /api/Members/{id}/RegisteredInterests | Return list of registered interests of member by ID |
| GET | /api/Members/{id}/Staff | Return list of staff of member by ID |
| GET | /api/Members/{id}/Synopsis | Return synopsis of member by ID |
| GET | /api/Members/{id}/Thumbnail | Return thumbnail of member by ID |
| GET | /api/Members/{id}/ThumbnailUrl | Return thumbnail url of member by ID |
| GET | /api/Members/{id}/Voting | Return list of votes by member by ID |
| GET | /api/Members/{id}/WrittenQuestions | Return list of written questions by member by ID |
| GET | /api/Parties/StateOfTheParties/{house}/{forDate} | Returns current state of parties |
| GET | /api/Parties/LordsByType/{forDate} | Returns the composition of the House of Lords by peerage type. |
| GET | /api/Parties/GetActive/{house} | Returns a list of current parties with at least one active member. |
| GET | /api/Posts/GovernmentPosts | Returns a list of government posts. |
| GET | /api/Posts/OppositionPosts | Returns a list of opposition posts. |
| GET | /api/Posts/Spokespersons | Returns a list of spokespersons. |
| GET | /api/Posts/Departments/{type} | Returns a list of departments. |
| GET | /api/Posts/SpeakerAndDeputies/{forDate} | Returns a list containing the speaker and deputy speakers. |
| GET | /api/Reference/PolicyInterests | Returns a list of policy interest. |
| GET | /api/Reference/Departments | Returns a list of departments. |
| GET | /api/Reference/AnsweringBodies | Returns a list of answering bodies. |
| GET | /api/Reference/Departments/{id}/Logo | Returns department logo. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get Browse details?" -> GET /api/Location/Browse/{locationType}/{locationName}
- "List all Search?" -> GET /api/Location/Constituency/Search
- "Get Constituency details?" -> GET /api/Location/Constituency/{id}
- "List all Synopsis?" -> GET /api/Location/Constituency/{id}/Synopsis
- "List all Representations?" -> GET /api/Location/Constituency/{id}/Representations
- "List all Geometry?" -> GET /api/Location/Constituency/{id}/Geometry
- "List all ElectionResults?" -> GET /api/Location/Constituency/{id}/ElectionResults
- "Get ElectionResult details?" -> GET /api/Location/Constituency/{id}/ElectionResult/{electionId}
- "List all Latest?" -> GET /api/Location/Constituency/{id}/ElectionResult/Latest
- "List all Register?" -> GET /api/LordsInterests/Register
- "List all Staff?" -> GET /api/LordsInterests/Staff
- "List all Search?" -> GET /api/Members/Search
- "List all SearchHistorical?" -> GET /api/Members/SearchHistorical
- "Get Member details?" -> GET /api/Members/{id}
- "List all Biography?" -> GET /api/Members/{id}/Biography
- "List all Contact?" -> GET /api/Members/{id}/Contact
- "List all ContributionSummary?" -> GET /api/Members/{id}/ContributionSummary
- "List all Edms?" -> GET /api/Members/{id}/Edms
- "List all Experience?" -> GET /api/Members/{id}/Experience
- "List all Focus?" -> GET /api/Members/{id}/Focus
- "List all History?" -> GET /api/Members/History
- "List all LatestElectionResult?" -> GET /api/Members/{id}/LatestElectionResult
- "List all Portrait?" -> GET /api/Members/{id}/Portrait
- "List all PortraitUrl?" -> GET /api/Members/{id}/PortraitUrl
- "List all RegisteredInterests?" -> GET /api/Members/{id}/RegisteredInterests
- "List all Staff?" -> GET /api/Members/{id}/Staff
- "List all Synopsis?" -> GET /api/Members/{id}/Synopsis
- "List all Thumbnail?" -> GET /api/Members/{id}/Thumbnail
- "List all ThumbnailUrl?" -> GET /api/Members/{id}/ThumbnailUrl
- "List all Voting?" -> GET /api/Members/{id}/Voting
- "List all WrittenQuestions?" -> GET /api/Members/{id}/WrittenQuestions
- "Get StateOfTheParty details?" -> GET /api/Parties/StateOfTheParties/{house}/{forDate}
- "Get LordsByType details?" -> GET /api/Parties/LordsByType/{forDate}
- "Get GetActive details?" -> GET /api/Parties/GetActive/{house}
- "List all GovernmentPosts?" -> GET /api/Posts/GovernmentPosts
- "List all OppositionPosts?" -> GET /api/Posts/OppositionPosts
- "List all Spokespersons?" -> GET /api/Posts/Spokespersons
- "Get Department details?" -> GET /api/Posts/Departments/{type}
- "Get SpeakerAndDeputy details?" -> GET /api/Posts/SpeakerAndDeputies/{forDate}
- "List all PolicyInterests?" -> GET /api/Reference/PolicyInterests
- "List all Departments?" -> GET /api/Reference/Departments
- "List all AnsweringBodies?" -> GET /api/Reference/AnsweringBodies
- "List all Logo?" -> GET /api/Reference/Departments/{id}/Logo

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
