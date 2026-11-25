---
name: aws-glue-databrew
description: "AWS Glue DataBrew API skill. Use when working with AWS Glue DataBrew for recipes, datasets, profileJobs. Covers 44 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Glue DataBrew
API version: 2017-07-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /datasets -- verify access
3. POST /recipes/{name}/batchDeleteRecipeVersion -- create first batchDeleteRecipeVersion

## Endpoints

44 endpoints across 10 groups. See references/api-spec.lap for full details.

### recipes
| Method | Path | Description |
|--------|------|-------------|
| POST | /recipes/{name}/batchDeleteRecipeVersion | Deletes one or more versions of a recipe at a time. The entire request will be rejected if:   The recipe does not exist.   There is an invalid version identifier in the list of versions.   The version list is empty.   The version list size exceeds 50.   The version list contains duplicate entries.   The request will complete successfully, but with partial failures, if:   A version does not exist.   A version is being used by a job.   You specify LATEST_WORKING, but it's being used by a project.   The version fails to be deleted.   The LATEST_WORKING version will only be deleted if the recipe has no other versions. If you try to delete LATEST_WORKING while other versions exist (or if they can't be deleted), then LATEST_WORKING will be listed as partial failure in the response. |
| POST | /recipes | Creates a new DataBrew recipe. |
| DELETE | /recipes/{name}/recipeVersion/{recipeVersion} | Deletes a single version of a DataBrew recipe. |
| GET | /recipes/{name} | Returns the definition of a specific DataBrew recipe corresponding to a particular version. |
| GET | /recipes | Lists all of the DataBrew recipes that are defined. |
| POST | /recipes/{name}/publishRecipe | Publishes a new version of a DataBrew recipe. |
| PUT | /recipes/{name} | Modifies the definition of the LATEST_WORKING version of a DataBrew recipe. |

### datasets
| Method | Path | Description |
|--------|------|-------------|
| POST | /datasets | Creates a new DataBrew dataset. |
| DELETE | /datasets/{name} | Deletes a dataset from DataBrew. |
| GET | /datasets/{name} | Returns the definition of a specific DataBrew dataset. |
| GET | /datasets | Lists all of the DataBrew datasets. |
| PUT | /datasets/{name} | Modifies the definition of an existing DataBrew dataset. |

### profileJobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /profileJobs | Creates a new job to analyze a dataset and create its data profile. |
| PUT | /profileJobs/{name} | Modifies the definition of an existing profile job. |

### projects
| Method | Path | Description |
|--------|------|-------------|
| POST | /projects | Creates a new DataBrew project. |
| DELETE | /projects/{name} | Deletes an existing DataBrew project. |
| GET | /projects/{name} | Returns the definition of a specific DataBrew project. |
| GET | /projects | Lists all of the DataBrew projects that are defined. |
| PUT | /projects/{name}/sendProjectSessionAction | Performs a recipe step within an interactive DataBrew session that's currently open. |
| PUT | /projects/{name}/startProjectSession | Creates an interactive session, enabling you to manipulate data in a DataBrew project. |
| PUT | /projects/{name} | Modifies the definition of an existing DataBrew project. |

### recipeJobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /recipeJobs | Creates a new job to transform input data, using steps defined in an existing Glue DataBrew recipe |
| PUT | /recipeJobs/{name} | Modifies the definition of an existing DataBrew recipe job. |

### rulesets
| Method | Path | Description |
|--------|------|-------------|
| POST | /rulesets | Creates a new ruleset that can be used in a profile job to validate the data quality of a dataset. |
| DELETE | /rulesets/{name} | Deletes a ruleset. |
| GET | /rulesets/{name} | Retrieves detailed information about the ruleset. |
| GET | /rulesets | List all rulesets available in the current account or rulesets associated with a specific resource (dataset). |
| PUT | /rulesets/{name} | Updates specified ruleset. |

### schedules
| Method | Path | Description |
|--------|------|-------------|
| POST | /schedules | Creates a new schedule for one or more DataBrew jobs. Jobs can be run at a specific date and time, or at regular intervals. |
| DELETE | /schedules/{name} | Deletes the specified DataBrew schedule. |
| GET | /schedules/{name} | Returns the definition of a specific DataBrew schedule. |
| GET | /schedules | Lists the DataBrew schedules that are defined. |
| PUT | /schedules/{name} | Modifies the definition of an existing DataBrew schedule. |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /jobs/{name} | Deletes the specified DataBrew job. |
| GET | /jobs/{name} | Returns the definition of a specific DataBrew job. |
| GET | /jobs/{name}/jobRun/{runId} | Represents one run of a DataBrew job. |
| GET | /jobs/{name}/jobRuns | Lists all of the previous runs of a particular DataBrew job. |
| GET | /jobs | Lists all of the DataBrew jobs that are defined. |
| POST | /jobs/{name}/startJobRun | Runs a DataBrew job. |
| POST | /jobs/{name}/jobRun/{runId}/stopJobRun | Stops a particular run of a job. |

### recipeVersions
| Method | Path | Description |
|--------|------|-------------|
| GET | /recipeVersions | Lists the versions of a particular DataBrew recipe, except for LATEST_WORKING. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{ResourceArn} | Lists all the tags for a DataBrew resource. |
| POST | /tags/{ResourceArn} | Adds metadata tags to a DataBrew resource, such as a dataset, project, recipe, job, or schedule. |
| DELETE | /tags/{ResourceArn} | Removes metadata tags from a DataBrew resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a batchDeleteRecipeVersion?" -> POST /recipes/{name}/batchDeleteRecipeVersion
- "Create a dataset?" -> POST /datasets
- "Create a profileJob?" -> POST /profileJobs
- "Create a project?" -> POST /projects
- "Create a recipe?" -> POST /recipes
- "Create a recipeJob?" -> POST /recipeJobs
- "Create a ruleset?" -> POST /rulesets
- "Create a schedule?" -> POST /schedules
- "Delete a dataset?" -> DELETE /datasets/{name}
- "Delete a job?" -> DELETE /jobs/{name}
- "Delete a project?" -> DELETE /projects/{name}
- "Delete a recipeVersion?" -> DELETE /recipes/{name}/recipeVersion/{recipeVersion}
- "Delete a ruleset?" -> DELETE /rulesets/{name}
- "Delete a schedule?" -> DELETE /schedules/{name}
- "Get dataset details?" -> GET /datasets/{name}
- "Get job details?" -> GET /jobs/{name}
- "Get jobRun details?" -> GET /jobs/{name}/jobRun/{runId}
- "Get project details?" -> GET /projects/{name}
- "Get recipe details?" -> GET /recipes/{name}
- "Get ruleset details?" -> GET /rulesets/{name}
- "Get schedule details?" -> GET /schedules/{name}
- "List all datasets?" -> GET /datasets
- "List all jobRuns?" -> GET /jobs/{name}/jobRuns
- "List all jobs?" -> GET /jobs
- "List all projects?" -> GET /projects
- "List all recipeVersions?" -> GET /recipeVersions
- "List all recipes?" -> GET /recipes
- "List all rulesets?" -> GET /rulesets
- "List all schedules?" -> GET /schedules
- "Get tag details?" -> GET /tags/{ResourceArn}
- "Create a publishRecipe?" -> POST /recipes/{name}/publishRecipe
- "Create a startJobRun?" -> POST /jobs/{name}/startJobRun
- "Create a stopJobRun?" -> POST /jobs/{name}/jobRun/{runId}/stopJobRun
- "Delete a tag?" -> DELETE /tags/{ResourceArn}
- "Update a dataset?" -> PUT /datasets/{name}
- "Update a profileJob?" -> PUT /profileJobs/{name}
- "Update a project?" -> PUT /projects/{name}
- "Update a recipe?" -> PUT /recipes/{name}
- "Update a recipeJob?" -> PUT /recipeJobs/{name}
- "Update a ruleset?" -> PUT /rulesets/{name}
- "Update a schedule?" -> PUT /schedules/{name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
