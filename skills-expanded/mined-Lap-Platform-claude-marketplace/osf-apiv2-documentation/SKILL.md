---
name: osf-apiv2-documentation
description: "OSF APIv2 Documentation API skill. Use when working with OSF APIv2 Documentation for addons, root, citations. Covers 343 endpoints."
version: 1.0.0
generator: lapsh
---

# OSF APIv2 Documentation
API version: 2.0

## Auth
No authentication required.

## Base URL
https://api.test.osf.io/v2

## Setup
1. No auth setup needed
2. GET /addons/ -- verify access
3. POST /institutions/{institution_id}/relationships/nodes/ -- create first nodes

## Endpoints

343 endpoints across 40 groups. See references/api-spec.lap for full details.

### addons
| Method | Path | Description |
|--------|------|-------------|
| GET | /addons/ | List all addons |

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Root |

### citations
| Method | Path | Description |
|--------|------|-------------|
| GET | /citations/styles/ | List all citation styles |
| GET | /citations/styles/{style_id}/ | Retrieve a citation style |

### comments
| Method | Path | Description |
|--------|------|-------------|
| GET | /comments/{comment_id}/ | Retrieve a comment |
| DELETE | /comments/{comment_id}/ | Delete a comment |

### files
| Method | Path | Description |
|--------|------|-------------|
| GET | /files/{file_id}/ | Retrieve a file |
| PATCH | /files/{file_id}/ | Update a file |
| GET | /files/{file_id}/versions/ | List all file versions |
| GET | /files/{file_id}/versions/{version_id}/ | Retrieve a file version |
| POST | /files/{file_id}/cedar_metadata_records/ | Create a CEDAR metadata record for a file |

### licenses
| Method | Path | Description |
|--------|------|-------------|
| GET | /licenses/ | List all licenses |

### license
| Method | Path | Description |
|--------|------|-------------|
| GET | /license/{license_id}/ | Retrieve a license |

### logs
| Method | Path | Description |
|--------|------|-------------|
| GET | /logs/{log_id}/ | Retrieve a log |

### actions
| Method | Path | Description |
|--------|------|-------------|
| GET | /actions/ | Actions |
| GET | /actions/reviews/ | List Review Actions |
| POST | /actions/requests/nodes/ | Create a Node Request Action |
| POST | /actions/requests/preprints/ | Create a Preprint Request Action |
| GET | /actions/{action_id}/ | Retrieve an Action by ID |

### institutions
| Method | Path | Description |
|--------|------|-------------|
| GET | /institutions/ | List all institutions |
| GET | /institutions/{institution_id}/ | Retrieve an institution |
| GET | /institutions/{institution_id}/users/ | List all affiliated users |
| GET | /institutions/{institution_id}/nodes/ | List all affiliated nodes |
| GET | /institutions/{institution_id}/registrations/ | List all affiliated registrations |
| GET | /institutions/{institution_id}/relationships/nodes/ | List nodes affiliated with an institution (relationship data) |
| POST | /institutions/{institution_id}/relationships/nodes/ | Add node relationships to an institution |
| DELETE | /institutions/{institution_id}/relationships/nodes/ | Remove node relationships from an institution |
| GET | /institutions/{institution_id}/relationships/registrations/ | List registrations affiliated with an institution (relationship data) |
| POST | /institutions/{institution_id}/relationships/registrations/ | Add registration relationships to an institution |
| DELETE | /institutions/{institution_id}/relationships/registrations/ | Remove registration relationships from an institution |

### schemas
| Method | Path | Description |
|--------|------|-------------|
| GET | /schemas/registrations/ | Retrieve a list of Registration Schemas |
| GET | /schemas/registrations/{registration_schema_id} | Retrieve a Registration Schema |

### schema_responses
| Method | Path | Description |
|--------|------|-------------|
| GET | /schema_responses/ | List all Schema Responses |
| POST | /schema_responses/ | Create a new Schema Response |
| GET | /schema_responses/{schema_response_id} | Retrieve a Schema Response |
| PATCH | /schema_responses/{schema_response_id} | Update a Registration's Schema Response |
| DELETE | /schema_responses/{schema_response_id} | Delete a Incomplete Schema Response |
| GET | /schema_responses/{schema_response_id}/actions/ | Retrieve a list of Schema Response Actions for a Schema Response |
| POST | /schema_responses/{schema_response_id}/actions/ | Create a new Schema Response Action |
| GET | /schema_responses/{schema_response_id}/actions/{schema_response_action_id} | A Schema Response Action from a Schema Response |
| GET | /schema_responses/{schema_response_id}/schema_blocks/ | Retrieve a list of Registration Schema Blocks for a Schema Response |
| GET | /schema_responses/{schema_response_id}/schema_blocks/{schema_response_block_id} | Retrieve a Registration Schema Block |

### nodes
| Method | Path | Description |
|--------|------|-------------|
| GET | /nodes/ | List all nodes |
| POST | /nodes/ | Create a node |
| GET | /nodes/{node_id}/ | Retrieve a node |
| PATCH | /nodes/{node_id}/ | Update a node |
| DELETE | /nodes/{node_id}/ | Delete a node |
| GET | /nodes/{node_id}/addons/ | List all addons |
| GET | /nodes/{node_id}/addons/{provider}/folders/ | List all addon folders |
| GET | /nodes/{node_id}/addons/{provider}/ | Retrieve an addon |
| PATCH | /nodes/{node_id}/addons/{provider}/ | Update an addon |
| GET | /nodes/{node_id}/children/ | List all child nodes |
| POST | /nodes/{node_id}/children/ | Create a child node |
| GET | /nodes/{node_id}/citation/ | Retrieve citation details |
| GET | /nodes/{node_id}/citation/{style_id}/ | Retrieve a styled citation |
| GET | /nodes/{node_id}/comments/ | List all comments |
| POST | /nodes/{node_id}/comments/ | Create a comment |
| GET | /nodes/{node_id}/contributors/ | List all contributors |
| POST | /nodes/{node_id}/contributors/ | Create a contributor |
| GET | /nodes/{node_id}/contributors/{user_id}/ | Retrieve a contributor |
| PATCH | /nodes/{node_id}/contributors/{user_id}/ | Update a contributor |
| DELETE | /nodes/{node_id}/contributors/{user_id}/ | Delete a contributor |
| GET | /nodes/{node_id}/draft_registrations/ | List all draft registrations |
| POST | /nodes/{node_id}/draft_registrations/ | Create a draft registration based on your current project Node. |
| GET | /nodes/{node_id}/draft_registrations/{draft_id}/ | Retrieve a Draft Registration |
| PATCH | /nodes/{node_id}/draft_registrations/{draft_id}/ | Update a draft registration |
| DELETE | /nodes/{node_id}/draft_registrations/{draft_id}/ | Delete a draft registration |
| GET | /nodes/{node_id}/files/ | List all storage providers |
| GET | /nodes/{node_id}/files/providers/{provider}/ | Retrieve a storage provider |
| GET | /nodes/{node_id}/files/{provider}/ | List all node files |
| GET | /nodes/{node_id}/files/{provider}/{path}/ | Retrieve a file |
| GET | /nodes/{node_id}/identifiers/ | Retrieve Identifiers for a Node |
| POST | /nodes/{node_id}/identifiers/ | Mint a New Identifier for a Node |
| GET | /nodes/{node_id}/institutions/ | List all institutions |
| POST | /nodes/{node_id}/forks/ | Create a fork of this node |
| GET | /nodes/{node_id}/forks/ | List all forks of this node |
| GET | /nodes/{node_id}/linked_nodes/ | List all linked nodes |
| GET | /nodes/{node_id}/logs/ | List all logs |
| GET | /nodes/{node_id}/preprints/ | List all preprints |
| GET | /nodes/{node_id}/registrations/ | List all registrations |
| GET | /nodes/{node_id}/view_only_links/ | List all view only links |
| GET | /nodes/{node_id}/view_only_links/{link_id}/ | Retrieve a view only link |
| GET | /nodes/{node_id}/wikis/ | List all wikis |
| GET | /nodes/{node_id}/linked_by_nodes/ | List Nodes Linking to a Node |
| GET | /nodes/{node_id}/linked_by_registrations/ | List Registrations Linking to a Node |
| GET | /nodes/{node_id}/relationships/institutions/ | Retrieve relationships between a Node and its affiliated Institutions |
| PATCH | /nodes/{node_id}/relationships/institutions/ | Replace relationships between a Node and its affiliated Institutions |
| POST | /nodes/{node_id}/relationships/institutions/ | Add relationships between a Node and Institutions |
| DELETE | /nodes/{node_id}/relationships/institutions/ | Remove relationships between a Node and Institutions |
| GET | /nodes/{node_id}/relationships/linked_nodes/ | Retrieve relationships between a Node and its linked Nodes |
| PATCH | /nodes/{node_id}/relationships/linked_nodes/ | Replace relationships between a Node and its linked Nodes |
| POST | /nodes/{node_id}/relationships/linked_nodes/ | Add relationships between a Node and linked Nodes |
| DELETE | /nodes/{node_id}/relationships/linked_nodes/ | Remove relationships between a Node and linked Nodes |
| GET | /nodes/{node_id}/relationships/linked_registrations/ | Retrieve relationships between a Node and its linked Registrations |
| PATCH | /nodes/{node_id}/relationships/linked_registrations/ | Replace relationships between a Node and linked Registrations |
| POST | /nodes/{node_id}/relationships/linked_registrations/ | Add relationships between a Node and linked Registrations |
| DELETE | /nodes/{node_id}/relationships/linked_registrations/ | Remove relationships between a Node and linked Registrations |
| GET | /nodes/{node_id}/relationships/subjects/ | Retrieve the relationships between a Node and its Subjects |
| PATCH | /nodes/{node_id}/relationships/subjects/ | Update the relationships between a Node and its Subjects |
| POST | /nodes/{node_id}/relationships/subjects/ | Add relationships between a Node and Subjects |
| DELETE | /nodes/{node_id}/relationships/subjects/ | Remove relationships between a Node and Subjects |
| GET | /nodes/{node_id}/requests/ | List Requests for a Node |
| GET | /nodes/{node_id}/settings/ | Retrieve Node Settings |
| PATCH | /nodes/{node_id}/settings/ | Update Node Settings |
| GET | /nodes/{node_id}/storage/ | List Storage Providers for a Node |
| GET | /nodes/{node_id}/subjects/ | List Subjects for a Node |
| POST | /nodes/{node_id}/cedar_metadata_records/ | Create a CEDAR metadata record for a node |

### preprints
| Method | Path | Description |
|--------|------|-------------|
| GET | /preprints/ | List all preprints |
| POST | /preprints/ | Create a preprint |
| GET | /preprints/{preprint_id}/versions/ | List preprint versions |
| POST | /preprints/{preprint_id}/versions/ | Create a preprint version |
| GET | /preprints/{preprint_id}/ | Retrieve a preprint |
| PATCH | /preprints/{preprint_id}/ | Update a preprint |
| GET | /preprints/{preprint_id}/citation/ | Retrieve citation details |
| GET | /preprints/{preprint_id}/citation/{style_id}/ | Retrieve a styled citation |
| GET | /preprints/{preprint_id}/contributors/ | List all Contributors for a Preprint |
| POST | /preprints/{preprint_id}/contributors/ | Create a Contributor |
| GET | /preprints/{preprint_id}/contributors/{user_id}/ | Retrieve a contributor |
| GET | /preprints/{preprint_id}/bibliographic_contributors/ | List all Bibliographic Contributors |
| GET | /preprints/{preprint_id}/institutions/ | List all Institutional Affilations for a Preprint |
| GET | /preprints/{preprint_id}/relationships/institutions/ | List all Institutions for a Preprint |
| PUT | /preprints/{preprint_id}/relationships/institutions/ | Update a Preprints Institutional Affilation |
| GET | /preprints/{preprint_id}/files/ | List storage providers for a preprint |
| GET | /preprints/{preprint_id}/files/osfstorage/ | List files for a preprint in osfstorage |
| GET | /preprints/{preprint_id}/identifiers/ | List identifiers for a preprint |
| GET | /preprints/{preprint_id}/relationships/node/ | Retrieve the relationship to the supplemental node of the preprint |
| PATCH | /preprints/{preprint_id}/relationships/node/ | Update the relationship to the supplemental node of the preprint |
| DELETE | /preprints/{preprint_id}/relationships/node/ | Remove the supplemental node relationship from the preprint |
| POST | /preprints/{preprint_id}/requests/ | Create a Preprint Request |
| GET | /preprints/{preprint_id}/review_actions/ | List Review Actions for a Preprint |
| GET | /preprints/{preprint_id}/subjects/ | List Preprint Subjects |

### preprint_providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /preprint_providers/ | List all preprint providers |
| GET | /preprint_providers/{provider_id}/ | Retrieve a preprint provider |
| GET | /preprint_providers/{provider_id}/preprints/ | List all preprints |
| GET | /preprint_providers/{provider_id}/taxonomies/ | List Taxonomies for a Preprint Provider |
| GET | /preprint_providers/{provider_id}/taxonomies/highlighted/ | List Highlighted Taxonomies for a Preprint Provider |
| GET | /preprint_providers/{provider_id}/licenses/ | List all licenses |
| GET | /preprint_providers/{provider_id}/moderators/ | List Moderators for a Preprint Provider |
| POST | /preprint_providers/{provider_id}/moderators/ | Add a Moderator to a Preprint Provider |
| GET | /preprint_providers/{provider_id}/moderators/{moderator_id}/ | Retrieve a Moderator for a Preprint Provider |
| PATCH | /preprint_providers/{provider_id}/moderators/{moderator_id}/ | Update a Moderator's Permission Group for a Preprint Provider |
| DELETE | /preprint_providers/{provider_id}/moderators/{moderator_id}/ | Remove a Moderator from a Preprint Provider |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/preprints/{provider_id}/citation_styles/ | List Citation Styles for a Preprint Provider |
| GET | /providers/preprints/{provider_id}/withdraw_requests/ | List Withdraw Requests for a Preprint Provider |
| GET | /providers/registrations/ | List all Registration Providers |
| GET | /providers/registrations/{provider_id}/ | Retrieve a Registration Provider |
| GET | /providers/registrations/{provider_id}/registrations/ | List Registration Requests |
| GET | /providers/registrations/{provider_id}/taxonomies/ | List Provider Taxonomies |
| GET | /providers/registrations/{provider_id}/taxonomies/highlighted/ | List Highlighted Taxonomies |
| GET | /providers/registrations/{provider_id}/licenses/ | Registration Providers Licenses List |
| GET | /providers/registrations/{provider_id}/actions/ | List Registration Actions |
| GET | /providers/registrations/{provider_id}/requests/ | List Registration Requests |
| GET | /providers/registrations/{provider_id}/schemas/ | List Registration Schemas for a Provider |
| GET | /providers/registrations/{provider_id}/subjects/ | List Subjects for a Registration |
| GET | /providers/registrations/{provider_id}/submissions/ | List Submissions for a Registration |
| GET | /providers/registrations/{provider_id}/subjects/highlighted/ | List Highlighted Subjects |
| GET | /providers/registrations/{provider_id}/moderators/ | List Moderators |
| POST | /providers/registrations/{provider_id}/moderators/ | Add Moderator |
| GET | /providers/registrations/{provider_id}/moderators/{moderator_id}/ | Retrieve Moderator Details |
| PATCH | /providers/registrations/{provider_id}/moderators/{moderator_id}/ | Update Moderator Permissions |
| DELETE | /providers/registrations/{provider_id}/moderators/{moderator_id}/ | Remove Moderator |
| GET | /providers/collections/ | List Collections Providers |
| GET | /providers/collections/{provider_id}/ | Collections Providers Detail |
| GET | /providers/collections/{provider_id}/licenses/ | Collections Providers Licenses List |
| GET | /providers/collections/{provider_id}/taxonomies/ | List Taxonomies for a Collection Provider (Deprecated) |
| GET | /providers/collections/{provider_id}/taxonomies/highlighted/ | List Highlighted Taxonomies for a Collection Provider (Deprecated) |
| GET | /providers/collections/{provider_id}/submissions/ | Collections Providers Submissions List |
| GET | /providers/collections/{provider_id}/subjects/highlighted/ | Collections Providers Highlighted Subject List |
| GET | /providers/collections/{provider_id}/moderators/ | Collections Providers Moderators List |
| GET | /providers/collections/{provider_id}/moderators/{moderator_id}/ | Collections Providers Moderators Detail |
| GET | /providers/collections/{provider_id}/subscriptions/ | List Notification Subscriptions for a Collection Provider |
| GET | /providers/collections/{provider_id}/subscriptions/{subscription_id}/ | Retrieve a Collection Provider Notification Subscription |
| PATCH | /providers/collections/{provider_id}/subscriptions/{subscription_id}/ | Update a Collection Provider Notification Subscription |
| GET | /providers/preprints/{provider_id}/subscriptions/ | List Preprint Provider Subscriptions |
| GET | /providers/preprints/{provider_id}/subscriptions/{subscription_id}/ | Retrieve a Preprint Provider Subscription |
| PATCH | /providers/preprints/{provider_id}/subscriptions/{subscription_id}/ | Update a Preprint Provider Subscription |
| GET | /providers/registrations/{provider_id}/subscriptions/ | List Registration Provider Subscriptions |
| GET | /providers/registrations/{provider_id}/subscriptions/{subscription_id}/ | Retrieve a Registration Provider Notification Subscription |
| PATCH | /providers/registrations/{provider_id}/subscriptions/{subscription_id}/ | Update a Registration Provider Notification Subscription |

### registrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /registrations/ | List all registrations |
| GET | /registrations/{registration_id}/ | Retrieve a registration |
| PATCH | /registrations/{registration_id}/ | Update a registration |
| GET | /registrations/{registration_id}/citations/ | List all citation styles |
| GET | /registrations/{registration_id}/citations/{citation_id}/ | Retrieve a citation |
| GET | /registrations/{registration_id}/children/ | List all child registrations |
| GET | /registrations/{registration_id}/comments/ | List all comments |
| GET | /registrations/{registration_id}/contributors/ | List all contributors |
| GET | /registrations/{registration_id}/contributors/{user_id}/ | Retrieve a contributor |
| GET | /registrations/{registration_id}/files/ | List all storage providers |
| GET | /registrations/{registration_id}/files/{provider}/ | List all files |
| GET | /registrations/{registration_id}/files/{provider}/{path}/ | Retrieve a file |
| GET | /registrations/{registration_id}/forks/ | List all forks |
| POST | /registrations/{registration_id}/forks/ | Create a fork |
| GET | /registrations/{registration_id}/identifiers/ | List all identifiers |
| GET | /registrations/{registration_id}/institutions/ | List all institutions |
| GET | /registrations/{registration_id}/linked_nodes/ | List all linked nodes |
| GET | /registrations/{registration_id}/logs/ | List all logs |
| GET | /registrations/{registration_id}/actions/ | List Registration Actions |
| GET | /registrations/{registration_id}/bibliographic_contributors/ | List Bibliographic Contributors for a Registration |
| GET | /registrations/{registration_id}/cedar_metadata_records/ | List CEDAR Metadata Records for a Registration |
| GET | /registrations/{registration_id}/citation/ | List all citation styles |
| GET | /registrations/{registration_id}/citation/{citation_id}/ | Retrieve a citation |
| GET | /registrations/{registration_id}/implicit_contributors/ | List Implicit Contributors for a Registration |
| GET | /registrations/{registration_id}/linked_by_nodes/ | List Linked By Nodes |
| GET | /registrations/{registration_id}/linked_by_registrations/ | List Linked By Registrations |
| GET | /registrations/{registration_id}/node_links/ | List Node Links for a Registration |
| GET | /registrations/{registration_id}/registrations/ | List Child Registrations of a Registration |
| GET | /registrations/{registration_id}/relationships/institutions/ | Retrieve Institution Relationships for a Registration |
| GET | /registrations/{registration_id}/relationships/linked_nodes/ | Retrieve Linked Nodes Relationship for a Registration or Node |
| GET | /registrations/{registration_id}/relationships/linked_registrations/ | Retrieve Linked Registrations Relationship for a Registration |
| GET | /registrations/{registration_id}/relationships/subjects/ | Retrieve Subjects Relationship for a Registration |
| GET | /registrations/{registration_id}/requests/ | List Requests for a Registration |
| GET | /registrations/{registration_id}/resources/ | List Related Resources for a Registration |
| GET | /registrations/{registration_id}/schema_responses/ | List Schema Responses for a Registration |
| GET | /registrations/{registration_id}/subjects/ | List Registration Subjects |
| GET | /registrations/{registration_id}/view_only_links/ | List all view only links |
| GET | /registrations/{registration_id}/view_only_links/{link_id}/ | Retrieve a view only link |
| GET | /registrations/{registration_id}/wikis/ | List all wikis |

### draft_registrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /draft_registrations/ | Retrieve a list of Draft Registrations |
| POST | /draft_registrations/ | Create a Draft Registration |
| GET | /draft_registrations/{draft_id}/ | Retrieve a Draft Registration |
| PATCH | /draft_registrations/{draft_id}/ | Update a Draft Registration |
| DELETE | /draft_registrations/{draft_id}/ | Delete a draft registration |
| GET | /draft_registrations/{draft_id}/contributors/ | Retreive a list Contributors from a Draft Registration |
| POST | /draft_registrations/{draft_id}/contributors/ | Add a contributor to a Draft Registration |
| GET | /draft_registrations/{draft_id}/contributors/{user_id}/ | Retreive a Contributor from a Draft Registration |
| GET | /draft_registrations/{draft_id}/institutions/ | Retrieve Institutions afilliated with a Draft Registration |
| GET | /draft_registrations/{draft_id}/subjects/ | Retrieve Subjects associated with a Draft Registration |
| GET | /draft_registrations/{draft_id}/bibliographic_contributors/ | List bibliographic contributors on a draft registration |
| GET | /draft_registrations/{draft_id}/relationships/institutions/ | Retrieve affiliated institutions for a draft registration |
| POST | /draft_registrations/{draft_id}/relationships/institutions/ | Add affiliated institutions to a draft registration |
| DELETE | /draft_registrations/{draft_id}/relationships/institutions/ | Remove affiliated institutions from a draft registration |
| GET | /draft_registrations/{draft_id}/relationships/subjects/ | Retrieve subjects relationship for a draft registration |
| POST | /draft_registrations/{draft_id}/relationships/subjects/ | Add subjects to a draft registration |
| DELETE | /draft_registrations/{draft_id}/relationships/subjects/ | Remove subjects from a draft registration |

### taxonomies
| Method | Path | Description |
|--------|------|-------------|
| GET | /taxonomies/ | List all taxonomies |
| GET | /taxonomies/{taxonomy_id}/ | Retrieve a taxonomy |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/ | List all users |
| GET | /users/{user_id}/ | Retrieve a user |
| PATCH | /users/{user_id}/ | Update a user |
| GET | /users/{user_id}/institutions/ | List all institutions |
| GET | /users/{user_id}/nodes/ | List all nodes |
| GET | /users/{user_id}/preprints/ | List all preprints |
| GET | /users/{user_id}/registrations/ | List all registrations |
| GET | /users/{user_id}/addons/ | List all user addons |
| GET | /users/{user_id}/addons/{provider}/ | Retrieve a user addon |
| GET | /users/{user_id}/addons/{provider}/accounts/ | List all addon accounts |
| GET | /users/{user_id}/addons/{provider}/accounts/{account_id}/ | Retrieve an addon account |
| POST | /users/{user_id}/claim/ | Claim a User Account |
| GET | /users/{user_id}/draft_preprints/ | List a User's Draft Preprints |
| GET | /users/{user_id}/draft_registrations/ | List a User's Draft Registrations |
| GET | /users/{user_id}/relationships/institutions/ | Retrieve a User's Institution Relationships |
| DELETE | /users/{user_id}/relationships/institutions/ | Remove Institutions from a User's Affiliations |
| GET | /users/{user_id}/settings/ | Retrieve a User's Settings |
| PATCH | /users/{user_id}/settings/ | Update a User's Settings |
| GET | /users/{user_id}/settings/emails/ | List User Email Addresses |
| POST | /users/{user_id}/settings/emails/ | Add a New Email Address |
| GET | /users/{user_id}/settings/emails/{email_id}/ | Retrieve a User's Email Address |
| PATCH | /users/{user_id}/settings/emails/{email_id}/ | Update a User's Email Address |
| DELETE | /users/{user_id}/settings/emails/{email_id}/ | Remove a User's Email Address |
| POST | /users/{user_id}/settings/export/ | Request User Account Export |
| GET | /users/{user_id}/settings/identities/ | List User External Identities |
| GET | /users/{user_id}/settings/identities/{identity_id} | Retrieve a User's External Identity |
| DELETE | /users/{user_id}/settings/identities/{identity_id} | Remove a User's External Identity |
| POST | /users/{user_id}/settings/password/ | Change a User's Password |

### view_only_links
| Method | Path | Description |
|--------|------|-------------|
| GET | /view_only_links/{link_id}/ | Retrieve a view only link |
| GET | /view_only_links/{link_id}/nodes/ | List all nodes |

### wikis
| Method | Path | Description |
|--------|------|-------------|
| GET | /wikis/{wiki_id}/ | Retrieve a Wiki |
| GET | /wikis/{wiki_id}/content/ | Retrieve the Content of a Wiki |
| POST | /wikis/{wiki_id}/versions/ | Create a new version of a wiki page |
| GET | /wikis/{wiki_id}/versions/{version_id}/ | Retrieve details for a specific wiki version |
| GET | /wikis/{wiki_id}/versions/{version_id}/content/ | Retrieve the raw content of a specific wiki version |

### collections
| Method | Path | Description |
|--------|------|-------------|
| GET | /collections/ | List all Collections |
| POST | /collections/ | Create a Collection |
| GET | /collections/{collection_id}/ | Retrieve a Collection |
| DELETE | /collections/{collection_id}/ | Delete a Collection |
| GET | /collections/{collection_id}/linked_nodes | List All Linked Nodes for a Collection |
| POST | /collections/{collection_id}/linked_nodes/relationships/ | Link Nodes to Collection |
| GET | /collections/{collection_id}/linked_nodes/relationships/ | Give a Sparse List of Node Ids |
| DELETE | /collections/{collection_id}/linked_nodes/relationships/ | Remove Nodes From Collection |
| GET | /collections/{collection_id}/linked_registrations/ | List All Linked Registrations for a Collection |
| POST | /collections/{collection_id}/linked_registrations/relationships/ | Link Registrations to Collection |
| GET | /collections/{collection_id}/linked_registrations/relationships/ | Give a Sparse List of Registrations Ids |
| DELETE | /collections/{collection_id}/linked_registrations/relationships/ | Remove Registrations From Collection |
| GET | /collections/{collection_id}/linked_preprints/ | List All Linked Preprints for a Collection |
| GET | /collections/{collection_id}/collected_metadata/ | Retrieve a list of collected metadata for a collection |
| POST | /collections/{collection_id}/collected_metadata/ | Add Metadata or Subjects to a Entity in a Collection |
| GET | /collections/{collection_id}/collected_metadata/{cgm_id} | Retrieve Specific Metadata for a Collection |
| POST | /collections/{collection_id}/collected_metadata/{cgm_id} | Add Metadata or Subjects to an Entity in a Collection |
| DELETE | /collections/{collection_id}/collected_metadata/{cgm_id} | Delete Collection Metadata from entitiy |
| GET | /collections/{collection_id}/collected_metadata/{cgm_id}/subjects/ | Retrieve subject data for a specific piece of metadata info for a collection |
| GET | /collections/{collection_id}/collected_metadata/{cgm_id}/relationships/subjects/ | Retrieve subject metadata for a specific piece of metadata in a collection |
| POST | /collections/{collection_id}/collected_metadata/{cgm_id}/relationships/subjects/ | Update subjects for a specific piece of metadata in a collection |

### collection_submissions
| Method | Path | Description |
|--------|------|-------------|
| GET | /collection_submissions/{collection_submission_id}/actions/ | Get a list of Collection Submission Actions for a Collection Submission |

### collection_submission_actions
| Method | Path | Description |
|--------|------|-------------|
| GET | /collection_submission_actions/{collection_submission_id}/ | Retrieve a Collection Submission Action |
| POST | /collection_submission_actions/ | Creates a Collection Submission Action |

### provider
| Method | Path | Description |
|--------|------|-------------|
| GET | /provider/collections/ | List Collections Providers |
| GET | /provider/collections/{provider_id}/ | Collections Providers Detail |
| GET | /provider/collections/{provider_id}/licenses/ | Collections Providers Licenses List |
| GET | /provider/collections/{provider_id}/submissions/ | Collections Providers Submissions List |
| GET | /provider/collections/{provider_id}/subjects/ | Collections Providers Subject List |
| GET | /provider/collections/{provider_id}/subjects/highlighted/ | Collections Providers Highlighted Subject List |
| GET | /provider/collections/{provider_id}/moderators/ | Collections Providers Moderators List |
| GET | /provider/collections/{provider_id}/moderators/{moderator_id}/ | Collections Providers Moderators Detail |

### requests
| Method | Path | Description |
|--------|------|-------------|
| GET | /requests/{request_id}/ | Retrieve details for a specific request |
| GET | /requests/{request_id}/actions/ | List actions associated with a request |

### resources
| Method | Path | Description |
|--------|------|-------------|
| GET | /resources/ | List resources |
| POST | /resources/ | Create a new resource |
| GET | /resources/{resource_id}/ | Retrieve a resource |
| PATCH | /resources/{resource_id}/ | Update a resource |
| DELETE | /resources/{resource_id}/ | Delete a resource |

### subjects
| Method | Path | Description |
|--------|------|-------------|
| GET | /subjects/ | List available taxonomy subjects |
| GET | /subjects/{subject_id}/ | Retrieve a single taxonomy subject |
| GET | /subjects/{subject_id}/children/ | List child subjects for a given subject |

### guids
| Method | Path | Description |
|--------|------|-------------|
| GET | /guids/{guid_id}/ | Retrieve a GUID resource or redirect to its referent resource |

### custom_file_metadata_records
| Method | Path | Description |
|--------|------|-------------|
| GET | /custom_file_metadata_records/{file_id}/ | Retrieve custom file metadata for a file |
| PATCH | /custom_file_metadata_records/{file_id}/ | Update custom file metadata for a file |

### custom_item_metadata_records
| Method | Path | Description |
|--------|------|-------------|
| GET | /custom_item_metadata_records/{guid_id}/ | Retrieve custom item metadata for a node or preprint |
| PATCH | /custom_item_metadata_records/{guid_id}/ | Update custom item metadata for a node or preprint |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/ | Retrieve a List of Notification Subscriptions |
| GET | /subscriptions/{subscription_id}/ | Retrieve a Notification Subscription |
| PATCH | /subscriptions/{subscription_id}/ | Update a Notification Subscription |

### registration_subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /registration_subscriptions/{subscription_id}/ | Retrieve a Registration Provider Subscription |
| PATCH | /registration_subscriptions/{subscription_id}/ | Update a Registration Provider Subscription |

### collection_subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /collection_subscriptions/{subscription_id}/ | Retrieve a Collection Subscription |
| PATCH | /collection_subscriptions/{subscription_id}/ | Update a Collection Subscription |

### regions
| Method | Path | Description |
|--------|------|-------------|
| GET | /regions/ | List Regions |
| GET | /regions/{region_id}/ | Region Detail |

### tokens
| Method | Path | Description |
|--------|------|-------------|
| GET | /tokens/ | List Personal Access Tokens |
| POST | /tokens/ | Create Personal Access Token |
| GET | /tokens/{_id}/ | Personal Access Token Detail |
| DELETE | /tokens/{_id}/ | Deactivate Personal Access Token |
| GET | /tokens/{_id}/scopes/ | List Scopes of a Personal Access Token |

### applications
| Method | Path | Description |
|--------|------|-------------|
| GET | /applications/ | List Registered Applications |
| POST | /applications/ | Create a New Application |
| GET | /applications/{client_id}/ | Retrieve Application Details |
| PATCH | /applications/{client_id}/ | Update Application |
| DELETE | /applications/{client_id}/ | Deactivate Application |
| POST | /applications/{client_id}/reset/ | Reset Application Client Secret |

### scopes
| Method | Path | Description |
|--------|------|-------------|
| GET | /scopes/ | List OAuth Scopes |
| GET | /scopes/{scope_id}/ | Retrieve OAuth Scope Detail |

### identifiers
| Method | Path | Description |
|--------|------|-------------|
| GET | /identifiers/{identifier_id}/ | Retrieve a Specific Identifier |
| GET | /identifiers/{node_id}/identifiers/ | List all identifiers |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all addons?" -> GET /addons/
- "List all styles?" -> GET /citations/styles/
- "Get style details?" -> GET /citations/styles/{style_id}/
- "Get comment details?" -> GET /comments/{comment_id}/
- "Delete a comment?" -> DELETE /comments/{comment_id}/
- "Get file details?" -> GET /files/{file_id}/
- "Partially update a file?" -> PATCH /files/{file_id}/
- "List all versions?" -> GET /files/{file_id}/versions/
- "Get version details?" -> GET /files/{file_id}/versions/{version_id}/
- "List all licenses?" -> GET /licenses/
- "Get license details?" -> GET /license/{license_id}/
- "Get log details?" -> GET /logs/{log_id}/
- "List all actions?" -> GET /actions/
- "List all institutions?" -> GET /institutions/
- "Get institution details?" -> GET /institutions/{institution_id}/
- "List all users?" -> GET /institutions/{institution_id}/users/
- "List all nodes?" -> GET /institutions/{institution_id}/nodes/
- "List all registrations?" -> GET /institutions/{institution_id}/registrations/
- "List all nodes?" -> GET /institutions/{institution_id}/relationships/nodes/
- "Create a node?" -> POST /institutions/{institution_id}/relationships/nodes/
- "List all registrations?" -> GET /institutions/{institution_id}/relationships/registrations/
- "Create a registration?" -> POST /institutions/{institution_id}/relationships/registrations/
- "List all registrations?" -> GET /schemas/registrations/
- "Get registration details?" -> GET /schemas/registrations/{registration_schema_id}
- "List all schema_responses?" -> GET /schema_responses/
- "Create a schema_respons?" -> POST /schema_responses/
- "Get schema_respons details?" -> GET /schema_responses/{schema_response_id}
- "Partially update a schema_respons?" -> PATCH /schema_responses/{schema_response_id}
- "Delete a schema_respons?" -> DELETE /schema_responses/{schema_response_id}
- "List all actions?" -> GET /schema_responses/{schema_response_id}/actions/
- "Create a action?" -> POST /schema_responses/{schema_response_id}/actions/
- "Get action details?" -> GET /schema_responses/{schema_response_id}/actions/{schema_response_action_id}
- "List all schema_blocks?" -> GET /schema_responses/{schema_response_id}/schema_blocks/
- "Get schema_block details?" -> GET /schema_responses/{schema_response_id}/schema_blocks/{schema_response_block_id}
- "List all nodes?" -> GET /nodes/
- "Create a node?" -> POST /nodes/
- "Get node details?" -> GET /nodes/{node_id}/
- "Partially update a node?" -> PATCH /nodes/{node_id}/
- "Delete a node?" -> DELETE /nodes/{node_id}/
- "List all addons?" -> GET /nodes/{node_id}/addons/
- "List all folders?" -> GET /nodes/{node_id}/addons/{provider}/folders/
- "Get addon details?" -> GET /nodes/{node_id}/addons/{provider}/
- "Partially update a addon?" -> PATCH /nodes/{node_id}/addons/{provider}/
- "List all children?" -> GET /nodes/{node_id}/children/
- "Create a children?" -> POST /nodes/{node_id}/children/
- "List all citation?" -> GET /nodes/{node_id}/citation/
- "Get citation details?" -> GET /nodes/{node_id}/citation/{style_id}/
- "List all comments?" -> GET /nodes/{node_id}/comments/
- "Create a comment?" -> POST /nodes/{node_id}/comments/
- "List all contributors?" -> GET /nodes/{node_id}/contributors/
- "Create a contributor?" -> POST /nodes/{node_id}/contributors/
- "Get contributor details?" -> GET /nodes/{node_id}/contributors/{user_id}/
- "Partially update a contributor?" -> PATCH /nodes/{node_id}/contributors/{user_id}/
- "Delete a contributor?" -> DELETE /nodes/{node_id}/contributors/{user_id}/
- "List all draft_registrations?" -> GET /nodes/{node_id}/draft_registrations/
- "Create a draft_registration?" -> POST /nodes/{node_id}/draft_registrations/
- "Get draft_registration details?" -> GET /nodes/{node_id}/draft_registrations/{draft_id}/
- "Partially update a draft_registration?" -> PATCH /nodes/{node_id}/draft_registrations/{draft_id}/
- "Delete a draft_registration?" -> DELETE /nodes/{node_id}/draft_registrations/{draft_id}/
- "List all files?" -> GET /nodes/{node_id}/files/
- "Get provider details?" -> GET /nodes/{node_id}/files/providers/{provider}/
- "Get file details?" -> GET /nodes/{node_id}/files/{provider}/
- "Get file details?" -> GET /nodes/{node_id}/files/{provider}/{path}/
- "List all identifiers?" -> GET /nodes/{node_id}/identifiers/
- "Create a identifier?" -> POST /nodes/{node_id}/identifiers/
- "List all institutions?" -> GET /nodes/{node_id}/institutions/
- "Create a fork?" -> POST /nodes/{node_id}/forks/
- "List all forks?" -> GET /nodes/{node_id}/forks/
- "List all linked_nodes?" -> GET /nodes/{node_id}/linked_nodes/
- "List all logs?" -> GET /nodes/{node_id}/logs/
- "List all preprints?" -> GET /nodes/{node_id}/preprints/
- "List all registrations?" -> GET /nodes/{node_id}/registrations/
- "List all view_only_links?" -> GET /nodes/{node_id}/view_only_links/
- "Get view_only_link details?" -> GET /nodes/{node_id}/view_only_links/{link_id}/
- "List all wikis?" -> GET /nodes/{node_id}/wikis/
- "List all linked_by_nodes?" -> GET /nodes/{node_id}/linked_by_nodes/
- "List all linked_by_registrations?" -> GET /nodes/{node_id}/linked_by_registrations/
- "List all institutions?" -> GET /nodes/{node_id}/relationships/institutions/
- "Create a institution?" -> POST /nodes/{node_id}/relationships/institutions/
- "List all linked_nodes?" -> GET /nodes/{node_id}/relationships/linked_nodes/
- "Create a linked_node?" -> POST /nodes/{node_id}/relationships/linked_nodes/
- "List all linked_registrations?" -> GET /nodes/{node_id}/relationships/linked_registrations/
- "Create a linked_registration?" -> POST /nodes/{node_id}/relationships/linked_registrations/
- "List all subjects?" -> GET /nodes/{node_id}/relationships/subjects/
- "Create a subject?" -> POST /nodes/{node_id}/relationships/subjects/
- "List all requests?" -> GET /nodes/{node_id}/requests/
- "List all settings?" -> GET /nodes/{node_id}/settings/
- "List all storage?" -> GET /nodes/{node_id}/storage/
- "List all subjects?" -> GET /nodes/{node_id}/subjects/
- "List all preprints?" -> GET /preprints/
- "Create a preprint?" -> POST /preprints/
- "List all versions?" -> GET /preprints/{preprint_id}/versions/
- "Create a version?" -> POST /preprints/{preprint_id}/versions/
- "Get preprint details?" -> GET /preprints/{preprint_id}/
- "Partially update a preprint?" -> PATCH /preprints/{preprint_id}/
- "List all citation?" -> GET /preprints/{preprint_id}/citation/
- "Get citation details?" -> GET /preprints/{preprint_id}/citation/{style_id}/
- "List all contributors?" -> GET /preprints/{preprint_id}/contributors/
- "Create a contributor?" -> POST /preprints/{preprint_id}/contributors/
- "Get contributor details?" -> GET /preprints/{preprint_id}/contributors/{user_id}/
- "List all bibliographic_contributors?" -> GET /preprints/{preprint_id}/bibliographic_contributors/
- "List all institutions?" -> GET /preprints/{preprint_id}/institutions/
- "List all institutions?" -> GET /preprints/{preprint_id}/relationships/institutions/
- "List all files?" -> GET /preprints/{preprint_id}/files/
- "List all osfstorage?" -> GET /preprints/{preprint_id}/files/osfstorage/
- "List all identifiers?" -> GET /preprints/{preprint_id}/identifiers/
- "List all node?" -> GET /preprints/{preprint_id}/relationships/node/
- "Create a request?" -> POST /preprints/{preprint_id}/requests/
- "List all review_actions?" -> GET /preprints/{preprint_id}/review_actions/
- "List all subjects?" -> GET /preprints/{preprint_id}/subjects/
- "List all preprint_providers?" -> GET /preprint_providers/
- "Get preprint_provider details?" -> GET /preprint_providers/{provider_id}/
- "List all preprints?" -> GET /preprint_providers/{provider_id}/preprints/
- "List all taxonomies?" -> GET /preprint_providers/{provider_id}/taxonomies/
- "List all highlighted?" -> GET /preprint_providers/{provider_id}/taxonomies/highlighted/
- "List all citation_styles?" -> GET /providers/preprints/{provider_id}/citation_styles/
- "List all licenses?" -> GET /preprint_providers/{provider_id}/licenses/
- "List all moderators?" -> GET /preprint_providers/{provider_id}/moderators/
- "Create a moderator?" -> POST /preprint_providers/{provider_id}/moderators/
- "Get moderator details?" -> GET /preprint_providers/{provider_id}/moderators/{moderator_id}/
- "Partially update a moderator?" -> PATCH /preprint_providers/{provider_id}/moderators/{moderator_id}/
- "Delete a moderator?" -> DELETE /preprint_providers/{provider_id}/moderators/{moderator_id}/
- "List all withdraw_requests?" -> GET /providers/preprints/{provider_id}/withdraw_requests/
- "List all registrations?" -> GET /registrations/
- "Get registration details?" -> GET /registrations/{registration_id}/
- "Partially update a registration?" -> PATCH /registrations/{registration_id}/
- "List all citations?" -> GET /registrations/{registration_id}/citations/
- "Get citation details?" -> GET /registrations/{registration_id}/citations/{citation_id}/
- "List all children?" -> GET /registrations/{registration_id}/children/
- "List all comments?" -> GET /registrations/{registration_id}/comments/
- "List all contributors?" -> GET /registrations/{registration_id}/contributors/
- "Get contributor details?" -> GET /registrations/{registration_id}/contributors/{user_id}/
- "List all files?" -> GET /registrations/{registration_id}/files/
- "Get file details?" -> GET /registrations/{registration_id}/files/{provider}/
- "Get file details?" -> GET /registrations/{registration_id}/files/{provider}/{path}/
- "List all forks?" -> GET /registrations/{registration_id}/forks/
- "Create a fork?" -> POST /registrations/{registration_id}/forks/
- "List all identifiers?" -> GET /registrations/{registration_id}/identifiers/
- "List all institutions?" -> GET /registrations/{registration_id}/institutions/
- "List all linked_nodes?" -> GET /registrations/{registration_id}/linked_nodes/
- "List all logs?" -> GET /registrations/{registration_id}/logs/
- "List all actions?" -> GET /registrations/{registration_id}/actions/
- "List all bibliographic_contributors?" -> GET /registrations/{registration_id}/bibliographic_contributors/
- "List all cedar_metadata_records?" -> GET /registrations/{registration_id}/cedar_metadata_records/
- "List all citation?" -> GET /registrations/{registration_id}/citation/
- "Get citation details?" -> GET /registrations/{registration_id}/citation/{citation_id}/
- "List all implicit_contributors?" -> GET /registrations/{registration_id}/implicit_contributors/
- "List all linked_by_nodes?" -> GET /registrations/{registration_id}/linked_by_nodes/
- "List all linked_by_registrations?" -> GET /registrations/{registration_id}/linked_by_registrations/
- "List all node_links?" -> GET /registrations/{registration_id}/node_links/
- "List all registrations?" -> GET /registrations/{registration_id}/registrations/
- "List all institutions?" -> GET /registrations/{registration_id}/relationships/institutions/
- "List all linked_nodes?" -> GET /registrations/{registration_id}/relationships/linked_nodes/
- "List all linked_registrations?" -> GET /registrations/{registration_id}/relationships/linked_registrations/
- "List all subjects?" -> GET /registrations/{registration_id}/relationships/subjects/
- "List all requests?" -> GET /registrations/{registration_id}/requests/
- "List all resources?" -> GET /registrations/{registration_id}/resources/
- "List all schema_responses?" -> GET /registrations/{registration_id}/schema_responses/
- "List all subjects?" -> GET /registrations/{registration_id}/subjects/
- "List all view_only_links?" -> GET /registrations/{registration_id}/view_only_links/
- "Get view_only_link details?" -> GET /registrations/{registration_id}/view_only_links/{link_id}/
- "List all wikis?" -> GET /registrations/{registration_id}/wikis/
- "List all registrations?" -> GET /providers/registrations/
- "Get registration details?" -> GET /providers/registrations/{provider_id}/
- "List all registrations?" -> GET /providers/registrations/{provider_id}/registrations/
- "List all taxonomies?" -> GET /providers/registrations/{provider_id}/taxonomies/
- "List all highlighted?" -> GET /providers/registrations/{provider_id}/taxonomies/highlighted/
- "List all licenses?" -> GET /providers/registrations/{provider_id}/licenses/
- "List all actions?" -> GET /providers/registrations/{provider_id}/actions/
- "List all requests?" -> GET /providers/registrations/{provider_id}/requests/
- "List all schemas?" -> GET /providers/registrations/{provider_id}/schemas/
- "List all subjects?" -> GET /providers/registrations/{provider_id}/subjects/
- "List all submissions?" -> GET /providers/registrations/{provider_id}/submissions/
- "List all highlighted?" -> GET /providers/registrations/{provider_id}/subjects/highlighted/
- "List all moderators?" -> GET /providers/registrations/{provider_id}/moderators/
- "Create a moderator?" -> POST /providers/registrations/{provider_id}/moderators/
- "Get moderator details?" -> GET /providers/registrations/{provider_id}/moderators/{moderator_id}/
- "Partially update a moderator?" -> PATCH /providers/registrations/{provider_id}/moderators/{moderator_id}/
- "Delete a moderator?" -> DELETE /providers/registrations/{provider_id}/moderators/{moderator_id}/
- "List all draft_registrations?" -> GET /draft_registrations/
- "Create a draft_registration?" -> POST /draft_registrations/
- "Get draft_registration details?" -> GET /draft_registrations/{draft_id}/
- "Partially update a draft_registration?" -> PATCH /draft_registrations/{draft_id}/
- "Delete a draft_registration?" -> DELETE /draft_registrations/{draft_id}/
- "List all contributors?" -> GET /draft_registrations/{draft_id}/contributors/
- "Create a contributor?" -> POST /draft_registrations/{draft_id}/contributors/
- "Get contributor details?" -> GET /draft_registrations/{draft_id}/contributors/{user_id}/
- "List all institutions?" -> GET /draft_registrations/{draft_id}/institutions/
- "List all subjects?" -> GET /draft_registrations/{draft_id}/subjects/
- "List all bibliographic_contributors?" -> GET /draft_registrations/{draft_id}/bibliographic_contributors/
- "List all institutions?" -> GET /draft_registrations/{draft_id}/relationships/institutions/
- "Create a institution?" -> POST /draft_registrations/{draft_id}/relationships/institutions/
- "List all subjects?" -> GET /draft_registrations/{draft_id}/relationships/subjects/
- "Create a subject?" -> POST /draft_registrations/{draft_id}/relationships/subjects/
- "List all taxonomies?" -> GET /taxonomies/
- "Get taxonomy details?" -> GET /taxonomies/{taxonomy_id}/
- "List all users?" -> GET /users/
- "Get user details?" -> GET /users/{user_id}/
- "Partially update a user?" -> PATCH /users/{user_id}/
- "List all institutions?" -> GET /users/{user_id}/institutions/
- "List all nodes?" -> GET /users/{user_id}/nodes/
- "List all preprints?" -> GET /users/{user_id}/preprints/
- "List all registrations?" -> GET /users/{user_id}/registrations/
- "List all addons?" -> GET /users/{user_id}/addons/
- "Get addon details?" -> GET /users/{user_id}/addons/{provider}/
- "List all accounts?" -> GET /users/{user_id}/addons/{provider}/accounts/
- "Get account details?" -> GET /users/{user_id}/addons/{provider}/accounts/{account_id}/
- "Create a claim?" -> POST /users/{user_id}/claim/
- "List all draft_preprints?" -> GET /users/{user_id}/draft_preprints/
- "List all draft_registrations?" -> GET /users/{user_id}/draft_registrations/
- "List all institutions?" -> GET /users/{user_id}/relationships/institutions/
- "List all settings?" -> GET /users/{user_id}/settings/
- "List all emails?" -> GET /users/{user_id}/settings/emails/
- "Create a email?" -> POST /users/{user_id}/settings/emails/
- "Get email details?" -> GET /users/{user_id}/settings/emails/{email_id}/
- "Partially update a email?" -> PATCH /users/{user_id}/settings/emails/{email_id}/
- "Delete a email?" -> DELETE /users/{user_id}/settings/emails/{email_id}/
- "Create a export?" -> POST /users/{user_id}/settings/export/
- "List all identities?" -> GET /users/{user_id}/settings/identities/
- "Get identity details?" -> GET /users/{user_id}/settings/identities/{identity_id}
- "Delete a identity?" -> DELETE /users/{user_id}/settings/identities/{identity_id}
- "Create a password?" -> POST /users/{user_id}/settings/password/
- "Get view_only_link details?" -> GET /view_only_links/{link_id}/
- "List all nodes?" -> GET /view_only_links/{link_id}/nodes/
- "Get wikis details?" -> GET /wikis/{wiki_id}/
- "List all content?" -> GET /wikis/{wiki_id}/content/
- "Create a version?" -> POST /wikis/{wiki_id}/versions/
- "Get version details?" -> GET /wikis/{wiki_id}/versions/{version_id}/
- "List all content?" -> GET /wikis/{wiki_id}/versions/{version_id}/content/
- "List all collections?" -> GET /collections/
- "Create a collection?" -> POST /collections/
- "Get collection details?" -> GET /collections/{collection_id}/
- "Delete a collection?" -> DELETE /collections/{collection_id}/
- "List all linked_nodes?" -> GET /collections/{collection_id}/linked_nodes
- "Create a relationship?" -> POST /collections/{collection_id}/linked_nodes/relationships/
- "List all relationships?" -> GET /collections/{collection_id}/linked_nodes/relationships/
- "List all linked_registrations?" -> GET /collections/{collection_id}/linked_registrations/
- "Create a relationship?" -> POST /collections/{collection_id}/linked_registrations/relationships/
- "List all relationships?" -> GET /collections/{collection_id}/linked_registrations/relationships/
- "List all linked_preprints?" -> GET /collections/{collection_id}/linked_preprints/
- "List all collected_metadata?" -> GET /collections/{collection_id}/collected_metadata/
- "Create a collected_metadata?" -> POST /collections/{collection_id}/collected_metadata/
- "Get collected_metadata details?" -> GET /collections/{collection_id}/collected_metadata/{cgm_id}
- "Delete a collected_metadata?" -> DELETE /collections/{collection_id}/collected_metadata/{cgm_id}
- "List all subjects?" -> GET /collections/{collection_id}/collected_metadata/{cgm_id}/subjects/
- "List all subjects?" -> GET /collections/{collection_id}/collected_metadata/{cgm_id}/relationships/subjects/
- "Create a subject?" -> POST /collections/{collection_id}/collected_metadata/{cgm_id}/relationships/subjects/
- "List all collections?" -> GET /providers/collections/
- "Get collection details?" -> GET /providers/collections/{provider_id}/
- "List all licenses?" -> GET /providers/collections/{provider_id}/licenses/
- "List all taxonomies?" -> GET /providers/collections/{provider_id}/taxonomies/
- "List all highlighted?" -> GET /providers/collections/{provider_id}/taxonomies/highlighted/
- "List all submissions?" -> GET /providers/collections/{provider_id}/submissions/
- "List all highlighted?" -> GET /providers/collections/{provider_id}/subjects/highlighted/
- "List all moderators?" -> GET /providers/collections/{provider_id}/moderators/
- "Get moderator details?" -> GET /providers/collections/{provider_id}/moderators/{moderator_id}/
- "List all actions?" -> GET /collection_submissions/{collection_submission_id}/actions/
- "Get collection_submission_action details?" -> GET /collection_submission_actions/{collection_submission_id}/
- "Create a collection_submission_action?" -> POST /collection_submission_actions/
- "List all collections?" -> GET /provider/collections/
- "Get collection details?" -> GET /provider/collections/{provider_id}/
- "List all licenses?" -> GET /provider/collections/{provider_id}/licenses/
- "List all submissions?" -> GET /provider/collections/{provider_id}/submissions/
- "List all subjects?" -> GET /provider/collections/{provider_id}/subjects/
- "List all highlighted?" -> GET /provider/collections/{provider_id}/subjects/highlighted/
- "List all moderators?" -> GET /provider/collections/{provider_id}/moderators/
- "Get moderator details?" -> GET /provider/collections/{provider_id}/moderators/{moderator_id}/
- "Get request details?" -> GET /requests/{request_id}/
- "List all actions?" -> GET /requests/{request_id}/actions/
- "List all resources?" -> GET /resources/
- "Create a resource?" -> POST /resources/
- "Get resource details?" -> GET /resources/{resource_id}/
- "Partially update a resource?" -> PATCH /resources/{resource_id}/
- "Delete a resource?" -> DELETE /resources/{resource_id}/
- "List all subjects?" -> GET /subjects/
- "Get subject details?" -> GET /subjects/{subject_id}/
- "List all children?" -> GET /subjects/{subject_id}/children/
- "Get guid details?" -> GET /guids/{guid_id}/
- "Create a cedar_metadata_record?" -> POST /files/{file_id}/cedar_metadata_records/
- "Create a cedar_metadata_record?" -> POST /nodes/{node_id}/cedar_metadata_records/
- "Get custom_file_metadata_record details?" -> GET /custom_file_metadata_records/{file_id}/
- "Partially update a custom_file_metadata_record?" -> PATCH /custom_file_metadata_records/{file_id}/
- "Get custom_item_metadata_record details?" -> GET /custom_item_metadata_records/{guid_id}/
- "Partially update a custom_item_metadata_record?" -> PATCH /custom_item_metadata_records/{guid_id}/
- "List all subscriptions?" -> GET /subscriptions/
- "Get subscription details?" -> GET /subscriptions/{subscription_id}/
- "Partially update a subscription?" -> PATCH /subscriptions/{subscription_id}/
- "List all subscriptions?" -> GET /providers/collections/{provider_id}/subscriptions/
- "Get subscription details?" -> GET /providers/collections/{provider_id}/subscriptions/{subscription_id}/
- "Partially update a subscription?" -> PATCH /providers/collections/{provider_id}/subscriptions/{subscription_id}/
- "List all subscriptions?" -> GET /providers/preprints/{provider_id}/subscriptions/
- "Get subscription details?" -> GET /providers/preprints/{provider_id}/subscriptions/{subscription_id}/
- "Partially update a subscription?" -> PATCH /providers/preprints/{provider_id}/subscriptions/{subscription_id}/
- "List all subscriptions?" -> GET /providers/registrations/{provider_id}/subscriptions/
- "Get subscription details?" -> GET /providers/registrations/{provider_id}/subscriptions/{subscription_id}/
- "Partially update a subscription?" -> PATCH /providers/registrations/{provider_id}/subscriptions/{subscription_id}/
- "Get registration_subscription details?" -> GET /registration_subscriptions/{subscription_id}/
- "Partially update a registration_subscription?" -> PATCH /registration_subscriptions/{subscription_id}/
- "Get collection_subscription details?" -> GET /collection_subscriptions/{subscription_id}/
- "Partially update a collection_subscription?" -> PATCH /collection_subscriptions/{subscription_id}/
- "List all regions?" -> GET /regions/
- "Get region details?" -> GET /regions/{region_id}/
- "List all tokens?" -> GET /tokens/
- "Create a token?" -> POST /tokens/
- "Get token details?" -> GET /tokens/{_id}/
- "Delete a token?" -> DELETE /tokens/{_id}/
- "List all scopes?" -> GET /tokens/{_id}/scopes/
- "List all applications?" -> GET /applications/
- "Create a application?" -> POST /applications/
- "Get application details?" -> GET /applications/{client_id}/
- "Partially update a application?" -> PATCH /applications/{client_id}/
- "Delete a application?" -> DELETE /applications/{client_id}/
- "Create a reset?" -> POST /applications/{client_id}/reset/
- "List all scopes?" -> GET /scopes/
- "Get scope details?" -> GET /scopes/{scope_id}/
- "List all reviews?" -> GET /actions/reviews/
- "Create a node?" -> POST /actions/requests/nodes/
- "Create a preprint?" -> POST /actions/requests/preprints/
- "Get action details?" -> GET /actions/{action_id}/
- "Get identifier details?" -> GET /identifiers/{identifier_id}/
- "List all identifiers?" -> GET /identifiers/{node_id}/identifiers/

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
