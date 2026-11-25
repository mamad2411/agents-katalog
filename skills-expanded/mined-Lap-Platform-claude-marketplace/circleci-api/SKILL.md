---
name: circleci-api
description: "CircleCI API skill. Use when working with CircleCI for insights, jobs, me. Covers 111 endpoints."
version: 1.0.0
generator: lapsh
---

# CircleCI API
API version: v2

## Auth
ApiKey Circle-Token in header | Basic | ApiKey circle-token in query

## Base URL
https://circleci.com/api/v2

## Setup
1. Set your API key in the appropriate header
2. GET /me -- verify access
3. POST /jobs/{job-id}/cancel -- create first cancel

## Endpoints

111 endpoints across 16 groups. See references/api-spec.lap for full details.

### insights
| Method | Path | Description |
|--------|------|-------------|
| GET | /insights/pages/{project-slug}/summary | Get summary metrics and trends for a project across it's workflows and branches |
| GET | /insights/time-series/{project-slug}/workflows/{workflow-name}/jobs | Job timeseries data |
| GET | /insights/{org-slug}/summary | Get summary metrics with trends for the entire org, and for each project. |
| GET | /insights/{project-slug}/branches | Get all branches for a project |
| GET | /insights/{project-slug}/flaky-tests | Get flaky tests for a project |
| GET | /insights/{project-slug}/workflows | Get summary metrics for a project's workflows |
| GET | /insights/{project-slug}/workflows/{workflow-name} | Get recent runs of a workflow |
| GET | /insights/{project-slug}/workflows/{workflow-name}/jobs | Get summary metrics for a project workflow's jobs. |
| GET | /insights/{project-slug}/workflows/{workflow-name}/summary | Get metrics and trends for workflows |
| GET | /insights/{project-slug}/workflows/{workflow-name}/test-metrics | Get test metrics for a project's workflows |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /jobs/{job-id}/cancel | Cancel job by job ID |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /me | User Information |
| GET | /me/collaborations | Collaborations |

### organization
| Method | Path | Description |
|--------|------|-------------|
| POST | /organization | Create a new organization |
| DELETE | /organization/{org-slug-or-id} | Delete an organization |
| GET | /organization/{org-slug-or-id} | Get an organization |
| POST | /organization/{org-slug-or-id}/project | Create a new project |
| POST | /organization/{org-slug-or-id}/url-orb-allow-list | Create a new URL Orb allow-list entry |
| GET | /organization/{org-slug-or-id}/url-orb-allow-list | List the entries in the org's URL Orb allow-list |
| DELETE | /organization/{org-slug-or-id}/url-orb-allow-list/{allow-list-entry-id} | Remove an entry from the org's URL orb allow-list |

### pipeline
| Method | Path | Description |
|--------|------|-------------|
| GET | /pipeline | Get a list of pipelines |
| POST | /pipeline/continue | Continue a pipeline |
| GET | /pipeline/{pipeline-id} | Get a pipeline by ID |
| GET | /pipeline/{pipeline-id}/config | Get a pipeline's configuration |
| GET | /pipeline/{pipeline-id}/values | Get pipeline values for a pipeline |
| GET | /pipeline/{pipeline-id}/workflow | Get a pipeline's workflows |

### project
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /project/{project-slug} | Delete a project |
| GET | /project/{project-slug} | Get a project |
| POST | /project/{project-slug}/checkout-key | Create a new checkout key |
| GET | /project/{project-slug}/checkout-key | Get all checkout keys |
| DELETE | /project/{project-slug}/checkout-key/{fingerprint} | Delete a checkout key |
| GET | /project/{project-slug}/checkout-key/{fingerprint} | Get a checkout key |
| POST | /project/{project-slug}/envvar | Create an environment variable |
| GET | /project/{project-slug}/envvar | List all environment variables |
| DELETE | /project/{project-slug}/envvar/{name} | Delete an environment variable |
| GET | /project/{project-slug}/envvar/{name} | Get a masked environment variable |
| GET | /project/{project-slug}/job/{job-number} | Get job details |
| POST | /project/{project-slug}/job/{job-number}/cancel | Cancel job by job number |
| GET | /project/{project-slug}/pipeline | Get all pipelines |
| POST | /project/{project-slug}/pipeline | Trigger a new pipeline |
| GET | /project/{project-slug}/pipeline/mine | Get your pipelines |
| GET | /project/{project-slug}/pipeline/{pipeline-number} | Get a pipeline by pipeline number |
| POST | /project/{project-slug}/schedule | Create a schedule |
| GET | /project/{project-slug}/schedule | List schedule triggers |
| GET | /project/{project-slug}/{job-number}/artifacts | Get a job's artifacts |
| GET | /project/{project-slug}/{job-number}/tests | Get test metadata |
| POST | /project/{provider}/{organization}/{project} | ⚠️ Create a project |
| GET | /project/{provider}/{organization}/{project}/settings | Get project settings |
| PATCH | /project/{provider}/{organization}/{project}/settings | Update project settings |
| POST | /project/{provider}/{organization}/{project}/pipeline/run | [Recommended] Trigger a new pipeline |

### schedule
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /schedule/{schedule-id} | Update a schedule |
| GET | /schedule/{schedule-id} | Get a schedule by ID. Available only on schedules associated with GitHub OAuth or Bitbucket Cloud pipeline definitions. |
| DELETE | /schedule/{schedule-id} | Delete a schedule |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user/{id} | User Information |

### webhook
| Method | Path | Description |
|--------|------|-------------|
| POST | /webhook | Create an outbound webhook |
| GET | /webhook | List webhooks |
| PUT | /webhook/{webhook-id} | Update an outbound webhook |
| GET | /webhook/{webhook-id} | Get a webhook |
| DELETE | /webhook/{webhook-id} | Delete an outbound webhook |

### workflow
| Method | Path | Description |
|--------|------|-------------|
| GET | /workflow/{id} | Get a workflow |
| POST | /workflow/{id}/approve/{approval_request_id} | Approve a job |
| POST | /workflow/{id}/cancel | Cancel a workflow |
| GET | /workflow/{id}/job | Get a workflow's jobs |
| POST | /workflow/{id}/rerun | Rerun a workflow |

### org
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /org/{orgID}/oidc-custom-claims | Delete org-level claims |
| GET | /org/{orgID}/oidc-custom-claims | Get org-level claims |
| PATCH | /org/{orgID}/oidc-custom-claims | Patch org-level claims |
| DELETE | /org/{orgID}/project/{projectID}/oidc-custom-claims | Delete project-level claims |
| GET | /org/{orgID}/project/{projectID}/oidc-custom-claims | Get project-level claims |
| PATCH | /org/{orgID}/project/{projectID}/oidc-custom-claims | Patch project-level claims |

### owner
| Method | Path | Description |
|--------|------|-------------|
| GET | /owner/{ownerID}/context/{context}/decision | Retrieves the owner's decision audit logs. |
| POST | /owner/{ownerID}/context/{context}/decision | Makes a decision |
| GET | /owner/{ownerID}/context/{context}/decision/settings | Get the decision settings |
| PATCH | /owner/{ownerID}/context/{context}/decision/settings | Set the decision settings |
| GET | /owner/{ownerID}/context/{context}/decision/{decisionID} | Retrieves the owner's decision audit log by given decisionID |
| GET | /owner/{ownerID}/context/{context}/decision/{decisionID}/policy-bundle | Retrieves Policy Bundle for a given decision log ID |
| GET | /owner/{ownerID}/context/{context}/policy-bundle | Retrieves Policy Bundle |
| POST | /owner/{ownerID}/context/{context}/policy-bundle | Creates policy bundle for the context |
| GET | /owner/{ownerID}/context/{context}/policy-bundle/{policyName} | Retrieves a policy document |

### context
| Method | Path | Description |
|--------|------|-------------|
| POST | /context | Create a new context |
| GET | /context | List contexts |
| GET | /context/{context_id} | Get a context |
| DELETE | /context/{context_id} | Delete a context |
| GET | /context/{context_id}/environment-variable | List environment variables |
| PUT | /context/{context_id}/environment-variable/{env_var_name} | Add or update an environment variable |
| DELETE | /context/{context_id}/environment-variable/{env_var_name} | Remove an environment variable |
| GET | /context/{context_id}/restrictions | Get context restrictions |
| POST | /context/{context_id}/restrictions | Create context restriction |
| DELETE | /context/{context_id}/restrictions/{restriction_id} | Delete context restriction |

### organizations
| Method | Path | Description |
|--------|------|-------------|
| GET | /organizations/{org_id}/groups | Groups in an organization |
| POST | /organizations/{org_id}/groups | Create Groups |
| GET | /organizations/{org_id}/groups/{group_id} | A group in an organization |
| DELETE | /organizations/{org_id}/groups/{group_id} | Delete a group |
| POST | /organizations/{org_id}/usage_export_job | Create a usage export |
| GET | /organizations/{org_id}/usage_export_job/{usage_export_job_id} | Get a usage export |

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/{project_id}/pipeline-definitions | List pipeline definitions |
| POST | /projects/{project_id}/pipeline-definitions | Create pipeline definition |
| GET | /projects/{project_id}/pipeline-definitions/{pipeline_definition_id} | Get pipeline definition |
| PATCH | /projects/{project_id}/pipeline-definitions/{pipeline_definition_id} | Update pipeline definition |
| DELETE | /projects/{project_id}/pipeline-definitions/{pipeline_definition_id} | Delete pipeline definition |
| GET | /projects/{project_id}/pipeline-definitions/{pipeline_definition_id}/triggers | List pipeline definition triggers |
| POST | /projects/{project_id}/pipeline-definitions/{pipeline_definition_id}/triggers | Create trigger |
| GET | /projects/{project_id}/triggers/{trigger_id} | Get trigger |
| PATCH | /projects/{project_id}/triggers/{trigger_id} | Update trigger |
| DELETE | /projects/{project_id}/triggers/{trigger_id} | Delete trigger |
| POST | /projects/{project_id}/rollback | Rollback a project |

### deploy
| Method | Path | Description |
|--------|------|-------------|
| GET | /deploy/environments | List Environments |
| GET | /deploy/environments/{environment_id} | Get Environment |
| GET | /deploy/components | List Components |
| GET | /deploy/components/{component_id} | Get Component |
| GET | /deploy/components/{component_id}/versions | List Component Versions |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all summary?" -> GET /insights/pages/{project-slug}/summary
- "List all jobs?" -> GET /insights/time-series/{project-slug}/workflows/{workflow-name}/jobs
- "List all summary?" -> GET /insights/{org-slug}/summary
- "List all branches?" -> GET /insights/{project-slug}/branches
- "List all flaky-tests?" -> GET /insights/{project-slug}/flaky-tests
- "List all workflows?" -> GET /insights/{project-slug}/workflows
- "Get workflow details?" -> GET /insights/{project-slug}/workflows/{workflow-name}
- "List all jobs?" -> GET /insights/{project-slug}/workflows/{workflow-name}/jobs
- "List all summary?" -> GET /insights/{project-slug}/workflows/{workflow-name}/summary
- "List all test-metrics?" -> GET /insights/{project-slug}/workflows/{workflow-name}/test-metrics
- "Create a cancel?" -> POST /jobs/{job-id}/cancel
- "List all me?" -> GET /me
- "List all collaborations?" -> GET /me/collaborations
- "Create a organization?" -> POST /organization
- "Delete a organization?" -> DELETE /organization/{org-slug-or-id}
- "Get organization details?" -> GET /organization/{org-slug-or-id}
- "Create a project?" -> POST /organization/{org-slug-or-id}/project
- "Create a url-orb-allow-list?" -> POST /organization/{org-slug-or-id}/url-orb-allow-list
- "List all url-orb-allow-list?" -> GET /organization/{org-slug-or-id}/url-orb-allow-list
- "Delete a url-orb-allow-list?" -> DELETE /organization/{org-slug-or-id}/url-orb-allow-list/{allow-list-entry-id}
- "List all pipeline?" -> GET /pipeline
- "Create a continue?" -> POST /pipeline/continue
- "Get pipeline details?" -> GET /pipeline/{pipeline-id}
- "List all config?" -> GET /pipeline/{pipeline-id}/config
- "List all values?" -> GET /pipeline/{pipeline-id}/values
- "List all workflow?" -> GET /pipeline/{pipeline-id}/workflow
- "Delete a project?" -> DELETE /project/{project-slug}
- "Get project details?" -> GET /project/{project-slug}
- "Create a checkout-key?" -> POST /project/{project-slug}/checkout-key
- "List all checkout-key?" -> GET /project/{project-slug}/checkout-key
- "Delete a checkout-key?" -> DELETE /project/{project-slug}/checkout-key/{fingerprint}
- "Get checkout-key details?" -> GET /project/{project-slug}/checkout-key/{fingerprint}
- "Create a envvar?" -> POST /project/{project-slug}/envvar
- "List all envvar?" -> GET /project/{project-slug}/envvar
- "Delete a envvar?" -> DELETE /project/{project-slug}/envvar/{name}
- "Get envvar details?" -> GET /project/{project-slug}/envvar/{name}
- "Get job details?" -> GET /project/{project-slug}/job/{job-number}
- "Create a cancel?" -> POST /project/{project-slug}/job/{job-number}/cancel
- "List all pipeline?" -> GET /project/{project-slug}/pipeline
- "Create a pipeline?" -> POST /project/{project-slug}/pipeline
- "List all mine?" -> GET /project/{project-slug}/pipeline/mine
- "Get pipeline details?" -> GET /project/{project-slug}/pipeline/{pipeline-number}
- "Create a schedule?" -> POST /project/{project-slug}/schedule
- "List all schedule?" -> GET /project/{project-slug}/schedule
- "List all artifacts?" -> GET /project/{project-slug}/{job-number}/artifacts
- "List all tests?" -> GET /project/{project-slug}/{job-number}/tests
- "Partially update a schedule?" -> PATCH /schedule/{schedule-id}
- "Get schedule details?" -> GET /schedule/{schedule-id}
- "Delete a schedule?" -> DELETE /schedule/{schedule-id}
- "Get user details?" -> GET /user/{id}
- "Create a webhook?" -> POST /webhook
- "List all webhook?" -> GET /webhook
- "Update a webhook?" -> PUT /webhook/{webhook-id}
- "Get webhook details?" -> GET /webhook/{webhook-id}
- "Delete a webhook?" -> DELETE /webhook/{webhook-id}
- "Get workflow details?" -> GET /workflow/{id}
- "Create a cancel?" -> POST /workflow/{id}/cancel
- "List all job?" -> GET /workflow/{id}/job
- "Create a rerun?" -> POST /workflow/{id}/rerun
- "List all oidc-custom-claims?" -> GET /org/{orgID}/oidc-custom-claims
- "List all oidc-custom-claims?" -> GET /org/{orgID}/project/{projectID}/oidc-custom-claims
- "List all decision?" -> GET /owner/{ownerID}/context/{context}/decision
- "Create a decision?" -> POST /owner/{ownerID}/context/{context}/decision
- "List all settings?" -> GET /owner/{ownerID}/context/{context}/decision/settings
- "Get decision details?" -> GET /owner/{ownerID}/context/{context}/decision/{decisionID}
- "List all policy-bundle?" -> GET /owner/{ownerID}/context/{context}/decision/{decisionID}/policy-bundle
- "List all policy-bundle?" -> GET /owner/{ownerID}/context/{context}/policy-bundle
- "Create a policy-bundle?" -> POST /owner/{ownerID}/context/{context}/policy-bundle
- "Get policy-bundle details?" -> GET /owner/{ownerID}/context/{context}/policy-bundle/{policyName}
- "Create a context?" -> POST /context
- "List all context?" -> GET /context
- "Get context details?" -> GET /context/{context_id}
- "Delete a context?" -> DELETE /context/{context_id}
- "List all environment-variable?" -> GET /context/{context_id}/environment-variable
- "Update a environment-variable?" -> PUT /context/{context_id}/environment-variable/{env_var_name}
- "Delete a environment-variable?" -> DELETE /context/{context_id}/environment-variable/{env_var_name}
- "List all restrictions?" -> GET /context/{context_id}/restrictions
- "Create a restriction?" -> POST /context/{context_id}/restrictions
- "Delete a restriction?" -> DELETE /context/{context_id}/restrictions/{restriction_id}
- "List all settings?" -> GET /project/{provider}/{organization}/{project}/settings
- "List all groups?" -> GET /organizations/{org_id}/groups
- "Create a group?" -> POST /organizations/{org_id}/groups
- "Get group details?" -> GET /organizations/{org_id}/groups/{group_id}
- "Delete a group?" -> DELETE /organizations/{org_id}/groups/{group_id}
- "Create a usage_export_job?" -> POST /organizations/{org_id}/usage_export_job
- "Get usage_export_job details?" -> GET /organizations/{org_id}/usage_export_job/{usage_export_job_id}
- "Create a run?" -> POST /project/{provider}/{organization}/{project}/pipeline/run
- "List all pipeline-definitions?" -> GET /projects/{project_id}/pipeline-definitions
- "Create a pipeline-definition?" -> POST /projects/{project_id}/pipeline-definitions
- "Get pipeline-definition details?" -> GET /projects/{project_id}/pipeline-definitions/{pipeline_definition_id}
- "Partially update a pipeline-definition?" -> PATCH /projects/{project_id}/pipeline-definitions/{pipeline_definition_id}
- "Delete a pipeline-definition?" -> DELETE /projects/{project_id}/pipeline-definitions/{pipeline_definition_id}
- "List all triggers?" -> GET /projects/{project_id}/pipeline-definitions/{pipeline_definition_id}/triggers
- "Create a trigger?" -> POST /projects/{project_id}/pipeline-definitions/{pipeline_definition_id}/triggers
- "Get trigger details?" -> GET /projects/{project_id}/triggers/{trigger_id}
- "Partially update a trigger?" -> PATCH /projects/{project_id}/triggers/{trigger_id}
- "Delete a trigger?" -> DELETE /projects/{project_id}/triggers/{trigger_id}
- "Create a rollback?" -> POST /projects/{project_id}/rollback
- "List all environments?" -> GET /deploy/environments
- "Get environment details?" -> GET /deploy/environments/{environment_id}
- "List all components?" -> GET /deploy/components
- "Get component details?" -> GET /deploy/components/{component_id}
- "List all versions?" -> GET /deploy/components/{component_id}/versions
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
