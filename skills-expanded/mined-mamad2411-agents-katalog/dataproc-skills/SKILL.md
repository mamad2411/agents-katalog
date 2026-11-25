---
description: Skills to interact with your Dataproc clusters and jobs. Follows current
  best practices for reliability, security, and maintainability.
metadata:
  evolved: true
  evolved_at: '2026-07-20T14:07:04.579867+00:00'
name: dataproc-skills
tags: []
version: 2
---

## Usage

All scripts can be executed using Node.js. Replace `<param_name>` and `<param_value>` with actual values.

**Bash:**
`node <skill_dir>/scripts/<script_name>.js '{"<param_name>": "<param_value>"}'`

**PowerShell:**
`node <skill_dir>/scripts/<script_name>.js '{\"<param_name>\": \"<param_value>\"}'`

Note: The scripts automatically load the environment variables from various .env files. Do not ask the user to set vars unless skill executions fails due to env var absence.

## Scripts

### get_cluster

Gets a Dataproc cluster

#### Parameters

| Name        | Type   | Description                                                                                                                                                                     | Required | Default |
| :---------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------- | :------ |
| clusterName | string | The short name of the cluster, e.g. for "projects/my-project/regions/us-central1/clusters/my-cluster", pass "my-cluster" (the project and region are inherited from the source) | No       |         |

---

### get_job

Gets a Dataproc job

#### Parameters

| Name  | Type   | Description                                                                                                                                      | Required | Default |
| :---- | :----- | :----------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------ |
| jobId | string | The job ID, e.g. for "projects/my-project/regions/us-central1/jobs/my-job", pass "my-job" (the project and region are inherited from the source) | No       |         |

---

### list_clusters

Lists and filters Dataproc clusters

#### Parameters

| Name      | Type    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Required | Default |
| :-------- | :------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------ |
| filter    | string  | A filter constraining the clusters to list. Filters are case-sensitive and have the following syntax: field = value [AND [field = value]] ... where field is one of status.state, clusterName, or labels.[KEY], and [KEY] is a label key. value can be \* to match all values. status.state can be one of the following: ACTIVE, INACTIVE, CREATING, RUNNING, ERROR, DELETING, UPDATING, STOPPING, or STOPPED. ACTIVE contains the CREATING, UPDATING, and RUNNING states. INACTIVE contains the DELETING, ERROR, STOPPING, and STOPPED states. clusterName is the name of the cluster provided at creation time. Only the logical AND operator is supported; space-separated items are treated as having an implicit AND operator. | No       |         |
| pageSize  | integer | The maximum number of clusters to return in a single page (default 20)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | No       | `20`    |
| pageToken | string  | A page token, received from a previous `ListClusters` call                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | No       |         |

---

### list_jobs

Lists and filters Dataproc jobs

#### Parameters

| Name            | Type    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Required | Default |
| :-------------- | :------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------ |
| filter          | string  | A filter constraining the jobs to list. Filters are case-sensitive and have the following syntax: field = value [AND [field = value]] ... where field is clusterName, status.state, or labels.[KEY], and [KEY] is a label key. value can be \* to match all values. status.state can be one of the following: PENDING, RUNNING, CANCEL_PENDING, JOB_STATE_CANCELLED, DONE, ERROR, or ATTEMPT_FAILURE. Only the logical AND operator is supported; space-separated items are treated as having an implicit AND operator. Filtering by clusterName is recommended to improve query performance. | No       |         |
| jobStateMatcher | string  | Specifies if the job state matcher should match ALL jobs, only ACTIVE jobs, or only NON_ACTIVE jobs. Defaults to ALL. Supported values: ALL, ACTIVE, NON_ACTIVE.                                                                                                                                                                                                                                                                                                                                                                                                                              | No       |         |
| pageSize        | integer | The maximum number of jobs to return in a single page (default 20)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | No       | `20`    |
| pageToken       | string  | A page token, received from a previous `ListJobs` call                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | No       |         |

---

## Prerequisites

- Ensure all required tools and dependencies are installed
- Verify you have the necessary permissions and access credentials
- Check that the target environment is in a known good state


## Error Handling

- Always check the exit code or response status of commands before proceeding
- On failure, log the error details and attempt recovery if a retry strategy exists
- If recovery fails, report the error with context: what was attempted, what went wrong, and suggested next steps
- Never silently ignore errors — treat unexpected output as potential failure


## Verification

- After each step, verify the expected outcome before continuing
- Use idempotent checks: running the same action twice produces the same result
- If verification fails, roll back the last change and report the issue
- Log verification results for audit trail


## Configuration

- Use environment variables with sensible defaults for configuration
- Validate configuration at the start of execution
- Document all configuration options and their effects
- Support loading config from files when appropriate
