---
name: figshare-api
description: "Figshare API skill. Use when working with Figshare for token, articles, account. Covers 151 endpoints."
version: 1.0.0
generator: lapsh
---

# Figshare API
API version: 2.0.0

## Auth
OAuth2

## Base URL
https://api.figshare.com/v2

## Setup
1. Configure auth: OAuth2
2. GET /token -- verify access
3. POST /token -- create first token

## Endpoints

151 endpoints across 11 groups. See references/api-spec.lap for full details.

### token
| Method | Path | Description |
|--------|------|-------------|
| GET | /token | Get OAuth token information |
| POST | /token | Create OAuth token |

### articles
| Method | Path | Description |
|--------|------|-------------|
| GET | /articles | Public Articles |
| POST | /articles/search | Public Articles Search |
| GET | /articles/{article_id} | View article details |
| GET | /articles/{article_id}/versions | List article versions |
| GET | /articles/{article_id}/versions/{version_id} | Article details for version |
| GET | /articles/{article_id}/versions/{version_id}/files | Article version file details |
| GET | /articles/{article_id}/download | Public Article Download |
| GET | /articles/{article_id}/versions/{version_id}/download | Public Article Version Download |
| GET | /articles/{article_id}/versions/{version_id}/embargo | Public Article Embargo for article version |
| GET | /articles/{article_id}/versions/{version_id}/confidentiality | Public Article Confidentiality for article version |
| GET | /articles/{article_id}/files | List article files |
| GET | /articles/{article_id}/files/{file_id} | Article file details |

### account
| Method | Path | Description |
|--------|------|-------------|
| POST | /account/articles/search | Private Articles search |
| GET | /account/articles | Private Articles |
| POST | /account/articles | Create new Article |
| GET | /account/articles/{article_id} | Article details |
| PUT | /account/articles/{article_id} | Update article |
| PATCH | /account/articles/{article_id} | Partially update article |
| DELETE | /account/articles/{article_id} | Delete article |
| GET | /account/articles/{article_id}/embargo | Article Embargo Details |
| PUT | /account/articles/{article_id}/embargo | Update Article Embargo |
| DELETE | /account/articles/{article_id}/embargo | Delete Article Embargo |
| POST | /account/articles/{article_id}/resource | Private Article Resource |
| POST | /account/articles/{article_id}/publish | Private Article Publish |
| POST | /account/articles/{article_id}/unpublish | Public Article Unpublish |
| POST | /account/articles/{article_id}/reserve_doi | Private Article Reserve DOI |
| POST | /account/articles/{article_id}/reserve_handle | Private Article Reserve Handle |
| GET | /account/articles/{article_id}/download | Private Article Download |
| PUT | /account/articles/{article_id}/versions/{version_id} | Update article version |
| PATCH | /account/articles/{article_id}/versions/{version_id} | Partially update article version |
| PUT | /account/articles/{article_id}/versions/{version_id}/update_thumb | Update article version thumbnail |
| GET | /account/articles/{article_id}/authors | List article authors |
| POST | /account/articles/{article_id}/authors | Add article authors |
| PUT | /account/articles/{article_id}/authors | Replace article authors |
| DELETE | /account/articles/{article_id}/authors/{author_id} | Delete article author |
| GET | /account/articles/{article_id}/categories | List article categories |
| POST | /account/articles/{article_id}/categories | Add article categories |
| PUT | /account/articles/{article_id}/categories | Replace article categories |
| DELETE | /account/articles/{article_id}/categories/{category_id} | Delete article category |
| GET | /account/articles/{article_id}/confidentiality | Article confidentiality details |
| PUT | /account/articles/{article_id}/confidentiality | Update article confidentiality |
| DELETE | /account/articles/{article_id}/confidentiality | Delete article confidentiality |
| GET | /account/articles/{article_id}/private_links | List private links |
| POST | /account/articles/{article_id}/private_links | Create private link |
| PUT | /account/articles/{article_id}/private_links/{link_id} | Update private link |
| DELETE | /account/articles/{article_id}/private_links/{link_id} | Disable private link |
| GET | /account/articles/{article_id}/files | List article files |
| POST | /account/articles/{article_id}/files | Initiate Upload |
| GET | /account/articles/{article_id}/files/{file_id} | Single File |
| POST | /account/articles/{article_id}/files/{file_id} | Complete Upload |
| DELETE | /account/articles/{article_id}/files/{file_id} | File Delete |
| GET | /account/articles/export | Account Article Report |
| POST | /account/articles/export | Initiate a new Report |
| GET | /account/collections | Private Collections List |
| POST | /account/collections | Create collection |
| GET | /account/collections/{collection_id} | Collection details |
| PUT | /account/collections/{collection_id} | Update collection |
| PATCH | /account/collections/{collection_id} | Partially update collection |
| DELETE | /account/collections/{collection_id} | Delete collection |
| POST | /account/collections/search | Private Collections Search |
| POST | /account/collections/{collection_id}/reserve_doi | Private Collection Reserve DOI |
| POST | /account/collections/{collection_id}/reserve_handle | Private Collection Reserve Handle |
| POST | /account/collections/{collection_id}/resource | Private Collection Resource |
| POST | /account/collections/{collection_id}/publish | Private Collection Publish |
| GET | /account/collections/{collection_id}/authors | List collection authors |
| POST | /account/collections/{collection_id}/authors | Add collection authors |
| PUT | /account/collections/{collection_id}/authors | Replace collection authors |
| DELETE | /account/collections/{collection_id}/authors/{author_id} | Delete collection author |
| GET | /account/collections/{collection_id}/categories | List collection categories |
| POST | /account/collections/{collection_id}/categories | Add collection categories |
| PUT | /account/collections/{collection_id}/categories | Replace collection categories |
| DELETE | /account/collections/{collection_id}/categories/{category_id} | Delete collection category |
| GET | /account/collections/{collection_id}/articles | List collection articles |
| POST | /account/collections/{collection_id}/articles | Add collection articles |
| PUT | /account/collections/{collection_id}/articles | Replace collection articles |
| DELETE | /account/collections/{collection_id}/articles/{article_id} | Delete collection article |
| GET | /account/collections/{collection_id}/private_links | List collection private links |
| POST | /account/collections/{collection_id}/private_links | Create collection private link |
| GET | /account/collections/{collection_id}/private_links/{link_id} | View collection private link |
| PUT | /account/collections/{collection_id}/private_links/{link_id} | Update collection private link |
| DELETE | /account/collections/{collection_id}/private_links/{link_id} | Disable private link |
| POST | /account/projects/search | Private Projects search |
| GET | /account/projects | Private Projects |
| POST | /account/projects | Create project |
| GET | /account/projects/{project_id} | View project details |
| PUT | /account/projects/{project_id} | Update project |
| PATCH | /account/projects/{project_id} | Partially update project |
| DELETE | /account/projects/{project_id} | Delete project |
| POST | /account/projects/{project_id}/publish | Private Project Publish |
| GET | /account/projects/{project_id}/notes | List project notes |
| POST | /account/projects/{project_id}/notes | Create project note |
| GET | /account/projects/{project_id}/notes/{note_id} | Project note details |
| PUT | /account/projects/{project_id}/notes/{note_id} | Update project note |
| DELETE | /account/projects/{project_id}/notes/{note_id} | Delete project note |
| POST | /account/projects/{project_id}/leave | Private Project Leave |
| GET | /account/projects/{project_id}/collaborators | List project collaborators |
| POST | /account/projects/{project_id}/collaborators | Invite project collaborators |
| DELETE | /account/projects/{project_id}/collaborators/{user_id} | Remove project collaborator |
| GET | /account/projects/{project_id}/articles | List project articles |
| POST | /account/projects/{project_id}/articles | Create project article |
| GET | /account/projects/{project_id}/articles/{article_id} | Project article details |
| DELETE | /account/projects/{project_id}/articles/{article_id} | Delete project article |
| GET | /account/projects/{project_id}/articles/{article_id}/files | Project article list files |
| GET | /account/projects/{project_id}/articles/{article_id}/files/{file_id} | Project article file details |
| POST | /account/authors/search | Search Authors |
| GET | /account/authors/{author_id} | Author details |
| POST | /account/funding/search | Search Funding |
| GET | /account | Private Account information |
| GET | /account/licenses | Private Account Licenses |
| GET | /account/institution | Private Account Institutions |
| GET | /account/institution/embargo_options | Private Account Institution embargo options |
| GET | /account/institution/articles | Private Institution Articles |
| GET | /account/institution/custom_fields | Private account institution group custom fields |
| POST | /account/institution/custom_fields/{custom_field_id}/items/upload | Custom fields values files upload |
| GET | /account/categories | Private Account Categories |
| GET | /account/institution/groups | Private Account Institution Groups |
| GET | /account/institution/groups/{group_id}/embargo_options | Private Account Institution Group Embargo Options |
| GET | /account/institution/roles | Private Account Institution Roles |
| GET | /account/institution/accounts | Private Account Institution Accounts |
| POST | /account/institution/accounts | Create new Institution Account |
| GET | /account/institution/accounts/{account_id} | Private Institution Account information |
| PUT | /account/institution/accounts/{account_id} | Update Institution Account |
| GET | /account/institution/roles/{account_id} | List Institution Account Group Roles |
| POST | /account/institution/roles/{account_id} | Add Institution Account Group Roles |
| DELETE | /account/institution/roles/{account_id}/{group_id}/{role_id} | Delete Institution Account Group Role |
| POST | /account/institution/accounts/search | Private Account Institution Accounts Search |
| GET | /account/institution/users/{account_id} | Private Account Institution User |
| GET | /account/institution/reviews | Institution Curation Reviews |
| GET | /account/institution/review/{curation_id} | Institution Curation Review |
| GET | /account/institution/review/{curation_id}/comments | Institution Curation Review Comments |
| POST | /account/institution/review/{curation_id}/comments | POST Institution Curation Review Comment |
| PUT | /account/profile | Update public profile |
| POST | /account/profile/{user_id}/picture | Update public profile picture |

### collections
| Method | Path | Description |
|--------|------|-------------|
| GET | /collections | Public Collections |
| POST | /collections/search | Public Collections Search |
| GET | /collections/{collection_id} | Collection details |
| GET | /collections/{collection_id}/versions | Collection Versions list |
| GET | /collections/{collection_id}/versions/{version_id} | Collection Version details |
| GET | /collections/{collection_id}/articles | Public Collection Articles |

### item_types
| Method | Path | Description |
|--------|------|-------------|
| GET | /item_types | Item Types |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects | Public Projects |
| POST | /projects/search | Public Projects Search |
| GET | /projects/{project_id} | Public Project |
| GET | /projects/{project_id}/articles | Public Project Articles |

### institutions
| Method | Path | Description |
|--------|------|-------------|
| GET | /institutions/{institution_string_id}/articles/filter-by | Public Institution Articles |

### categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /categories | Public Categories |

### licenses
| Method | Path | Description |
|--------|------|-------------|
| GET | /licenses | Public Licenses |

### institution
| Method | Path | Description |
|--------|------|-------------|
| POST | /institution/hrfeed/upload | Private Institution HRfeed Upload |

### file
| Method | Path | Description |
|--------|------|-------------|
| GET | /file/download/{file_id} | Public File Download |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all token?" -> GET /token
- "Create a token?" -> POST /token
- "List all articles?" -> GET /articles
- "Create a search?" -> POST /articles/search
- "Get article details?" -> GET /articles/{article_id}
- "List all versions?" -> GET /articles/{article_id}/versions
- "Get version details?" -> GET /articles/{article_id}/versions/{version_id}
- "List all files?" -> GET /articles/{article_id}/versions/{version_id}/files
- "List all download?" -> GET /articles/{article_id}/download
- "List all download?" -> GET /articles/{article_id}/versions/{version_id}/download
- "List all embargo?" -> GET /articles/{article_id}/versions/{version_id}/embargo
- "List all confidentiality?" -> GET /articles/{article_id}/versions/{version_id}/confidentiality
- "List all files?" -> GET /articles/{article_id}/files
- "Get file details?" -> GET /articles/{article_id}/files/{file_id}
- "Create a search?" -> POST /account/articles/search
- "List all articles?" -> GET /account/articles
- "Create a article?" -> POST /account/articles
- "Get article details?" -> GET /account/articles/{article_id}
- "Update a article?" -> PUT /account/articles/{article_id}
- "Partially update a article?" -> PATCH /account/articles/{article_id}
- "Delete a article?" -> DELETE /account/articles/{article_id}
- "List all embargo?" -> GET /account/articles/{article_id}/embargo
- "Create a resource?" -> POST /account/articles/{article_id}/resource
- "Create a publish?" -> POST /account/articles/{article_id}/publish
- "Create a unpublish?" -> POST /account/articles/{article_id}/unpublish
- "Create a reserve_doi?" -> POST /account/articles/{article_id}/reserve_doi
- "Create a reserve_handle?" -> POST /account/articles/{article_id}/reserve_handle
- "List all download?" -> GET /account/articles/{article_id}/download
- "Update a version?" -> PUT /account/articles/{article_id}/versions/{version_id}
- "Partially update a version?" -> PATCH /account/articles/{article_id}/versions/{version_id}
- "List all authors?" -> GET /account/articles/{article_id}/authors
- "Create a author?" -> POST /account/articles/{article_id}/authors
- "Delete a author?" -> DELETE /account/articles/{article_id}/authors/{author_id}
- "List all categories?" -> GET /account/articles/{article_id}/categories
- "Create a category?" -> POST /account/articles/{article_id}/categories
- "Delete a category?" -> DELETE /account/articles/{article_id}/categories/{category_id}
- "List all confidentiality?" -> GET /account/articles/{article_id}/confidentiality
- "List all private_links?" -> GET /account/articles/{article_id}/private_links
- "Create a private_link?" -> POST /account/articles/{article_id}/private_links
- "Update a private_link?" -> PUT /account/articles/{article_id}/private_links/{link_id}
- "Delete a private_link?" -> DELETE /account/articles/{article_id}/private_links/{link_id}
- "List all files?" -> GET /account/articles/{article_id}/files
- "Create a file?" -> POST /account/articles/{article_id}/files
- "Get file details?" -> GET /account/articles/{article_id}/files/{file_id}
- "Delete a file?" -> DELETE /account/articles/{article_id}/files/{file_id}
- "List all export?" -> GET /account/articles/export
- "Create a export?" -> POST /account/articles/export
- "List all collections?" -> GET /collections
- "Create a search?" -> POST /collections/search
- "Get collection details?" -> GET /collections/{collection_id}
- "List all versions?" -> GET /collections/{collection_id}/versions
- "Get version details?" -> GET /collections/{collection_id}/versions/{version_id}
- "List all articles?" -> GET /collections/{collection_id}/articles
- "List all collections?" -> GET /account/collections
- "Create a collection?" -> POST /account/collections
- "Get collection details?" -> GET /account/collections/{collection_id}
- "Update a collection?" -> PUT /account/collections/{collection_id}
- "Partially update a collection?" -> PATCH /account/collections/{collection_id}
- "Delete a collection?" -> DELETE /account/collections/{collection_id}
- "Create a search?" -> POST /account/collections/search
- "Create a reserve_doi?" -> POST /account/collections/{collection_id}/reserve_doi
- "Create a reserve_handle?" -> POST /account/collections/{collection_id}/reserve_handle
- "Create a resource?" -> POST /account/collections/{collection_id}/resource
- "Create a publish?" -> POST /account/collections/{collection_id}/publish
- "List all authors?" -> GET /account/collections/{collection_id}/authors
- "Create a author?" -> POST /account/collections/{collection_id}/authors
- "Delete a author?" -> DELETE /account/collections/{collection_id}/authors/{author_id}
- "List all categories?" -> GET /account/collections/{collection_id}/categories
- "Create a category?" -> POST /account/collections/{collection_id}/categories
- "Delete a category?" -> DELETE /account/collections/{collection_id}/categories/{category_id}
- "List all articles?" -> GET /account/collections/{collection_id}/articles
- "Create a article?" -> POST /account/collections/{collection_id}/articles
- "Delete a article?" -> DELETE /account/collections/{collection_id}/articles/{article_id}
- "List all private_links?" -> GET /account/collections/{collection_id}/private_links
- "Create a private_link?" -> POST /account/collections/{collection_id}/private_links
- "Get private_link details?" -> GET /account/collections/{collection_id}/private_links/{link_id}
- "Update a private_link?" -> PUT /account/collections/{collection_id}/private_links/{link_id}
- "Delete a private_link?" -> DELETE /account/collections/{collection_id}/private_links/{link_id}
- "List all item_types?" -> GET /item_types
- "List all projects?" -> GET /projects
- "Create a search?" -> POST /projects/search
- "Get project details?" -> GET /projects/{project_id}
- "List all articles?" -> GET /projects/{project_id}/articles
- "Create a search?" -> POST /account/projects/search
- "List all projects?" -> GET /account/projects
- "Create a project?" -> POST /account/projects
- "Get project details?" -> GET /account/projects/{project_id}
- "Update a project?" -> PUT /account/projects/{project_id}
- "Partially update a project?" -> PATCH /account/projects/{project_id}
- "Delete a project?" -> DELETE /account/projects/{project_id}
- "Create a publish?" -> POST /account/projects/{project_id}/publish
- "List all notes?" -> GET /account/projects/{project_id}/notes
- "Create a note?" -> POST /account/projects/{project_id}/notes
- "Get note details?" -> GET /account/projects/{project_id}/notes/{note_id}
- "Update a note?" -> PUT /account/projects/{project_id}/notes/{note_id}
- "Delete a note?" -> DELETE /account/projects/{project_id}/notes/{note_id}
- "Create a leave?" -> POST /account/projects/{project_id}/leave
- "List all collaborators?" -> GET /account/projects/{project_id}/collaborators
- "Create a collaborator?" -> POST /account/projects/{project_id}/collaborators
- "Delete a collaborator?" -> DELETE /account/projects/{project_id}/collaborators/{user_id}
- "List all articles?" -> GET /account/projects/{project_id}/articles
- "Create a article?" -> POST /account/projects/{project_id}/articles
- "Get article details?" -> GET /account/projects/{project_id}/articles/{article_id}
- "Delete a article?" -> DELETE /account/projects/{project_id}/articles/{article_id}
- "List all files?" -> GET /account/projects/{project_id}/articles/{article_id}/files
- "Get file details?" -> GET /account/projects/{project_id}/articles/{article_id}/files/{file_id}
- "List all filter-by?" -> GET /institutions/{institution_string_id}/articles/filter-by
- "Create a search?" -> POST /account/authors/search
- "Get author details?" -> GET /account/authors/{author_id}
- "Create a search?" -> POST /account/funding/search
- "List all account?" -> GET /account
- "List all categories?" -> GET /categories
- "List all licenses?" -> GET /licenses
- "List all licenses?" -> GET /account/licenses
- "List all institution?" -> GET /account/institution
- "List all embargo_options?" -> GET /account/institution/embargo_options
- "List all articles?" -> GET /account/institution/articles
- "List all custom_fields?" -> GET /account/institution/custom_fields
- "Create a upload?" -> POST /account/institution/custom_fields/{custom_field_id}/items/upload
- "List all categories?" -> GET /account/categories
- "List all groups?" -> GET /account/institution/groups
- "List all embargo_options?" -> GET /account/institution/groups/{group_id}/embargo_options
- "List all roles?" -> GET /account/institution/roles
- "List all accounts?" -> GET /account/institution/accounts
- "Create a account?" -> POST /account/institution/accounts
- "Get account details?" -> GET /account/institution/accounts/{account_id}
- "Update a account?" -> PUT /account/institution/accounts/{account_id}
- "Get role details?" -> GET /account/institution/roles/{account_id}
- "Delete a role?" -> DELETE /account/institution/roles/{account_id}/{group_id}/{role_id}
- "Create a search?" -> POST /account/institution/accounts/search
- "Get user details?" -> GET /account/institution/users/{account_id}
- "List all reviews?" -> GET /account/institution/reviews
- "Get review details?" -> GET /account/institution/review/{curation_id}
- "List all comments?" -> GET /account/institution/review/{curation_id}/comments
- "Create a comment?" -> POST /account/institution/review/{curation_id}/comments
- "Create a upload?" -> POST /institution/hrfeed/upload
- "Get download details?" -> GET /file/download/{file_id}
- "Create a picture?" -> POST /account/profile/{user_id}/picture
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
