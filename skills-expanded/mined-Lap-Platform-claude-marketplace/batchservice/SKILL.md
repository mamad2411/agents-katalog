---
name: batchservice
description: "BatchService API skill. Use when working with BatchService for applications, poolusagemetrics, nodeagentskus. Covers 77 endpoints."
version: 1.0.0
generator: lapsh
---

# BatchService
API version: 2018-08-01.7.0

## Auth
No authentication required.

## Base URL
https://batch.core.windows.net

## Setup
1. No auth setup needed
2. GET /applications -- verify access
3. POST /certificates -- create first certificates

## Endpoints

77 endpoints across 11 groups. See references/api-spec.lap for full details.

### applications
| Method | Path | Description |
|--------|------|-------------|
| GET | /applications | Lists all of the applications available in the specified account. |
| GET | /applications/{applicationId} | Gets information about the specified application. |

### poolusagemetrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /poolusagemetrics | Lists the usage metrics, aggregated by pool across individual time intervals, for the specified account. |

### nodeagentskus
| Method | Path | Description |
|--------|------|-------------|
| GET | /nodeagentskus | Lists all node agent SKUs supported by the Azure Batch service. |

### nodecounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /nodecounts | Gets the number of nodes in each state, grouped by pool. |

### lifetimepoolstats
| Method | Path | Description |
|--------|------|-------------|
| GET | /lifetimepoolstats | Gets lifetime summary statistics for all of the pools in the specified account. |

### lifetimejobstats
| Method | Path | Description |
|--------|------|-------------|
| GET | /lifetimejobstats | Gets lifetime summary statistics for all of the jobs in the specified account. |

### certificates
| Method | Path | Description |
|--------|------|-------------|
| POST | /certificates | Adds a certificate to the specified account. |
| GET | /certificates | Lists all of the certificates that have been added to the specified account. |

### certificates(thumbprintAlgorithm={thumbprintAlgorithm},thumbprint={thumbprint})
| Method | Path | Description |
|--------|------|-------------|
| POST | /certificates(thumbprintAlgorithm={thumbprintAlgorithm},thumbprint={thumbprint})/canceldelete | Cancels a failed deletion of a certificate from the specified account. |
| DELETE | /certificates(thumbprintAlgorithm={thumbprintAlgorithm},thumbprint={thumbprint}) | Deletes a certificate from the specified account. |
| GET | /certificates(thumbprintAlgorithm={thumbprintAlgorithm},thumbprint={thumbprint}) | Gets information about the specified certificate. |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /jobs/{jobId}/tasks/{taskId}/files/{filePath} | Deletes the specified task file from the compute node where the task ran. |
| GET | /jobs/{jobId}/tasks/{taskId}/files/{filePath} | Returns the content of the specified task file. |
| HEAD | /jobs/{jobId}/tasks/{taskId}/files/{filePath} | Gets the properties of the specified task file. |
| GET | /jobs/{jobId}/tasks/{taskId}/files | Lists the files in a task's directory on its compute node. |
| DELETE | /jobs/{jobId} | Deletes a job. |
| GET | /jobs/{jobId} | Gets information about the specified job. |
| PATCH | /jobs/{jobId} | Updates the properties of the specified job. |
| PUT | /jobs/{jobId} | Updates the properties of the specified job. |
| POST | /jobs/{jobId}/disable | Disables the specified job, preventing new tasks from running. |
| POST | /jobs/{jobId}/enable | Enables the specified job, allowing new tasks to run. |
| POST | /jobs/{jobId}/terminate | Terminates the specified job, marking it as completed. |
| POST | /jobs | Adds a job to the specified account. |
| GET | /jobs | Lists all of the jobs in the specified account. |
| GET | /jobs/{jobId}/jobpreparationandreleasetaskstatus | Lists the execution status of the Job Preparation and Job Release task for the specified job across the compute nodes where the job has run. |
| GET | /jobs/{jobId}/taskcounts | Gets the task counts for the specified job. |
| POST | /jobs/{jobId}/tasks | Adds a task to the specified job. |
| GET | /jobs/{jobId}/tasks | Lists all of the tasks that are associated with the specified job. |
| POST | /jobs/{jobId}/addtaskcollection | Adds a collection of tasks to the specified job. |
| DELETE | /jobs/{jobId}/tasks/{taskId} | Deletes a task from the specified job. |
| GET | /jobs/{jobId}/tasks/{taskId} | Gets information about the specified task. |
| PUT | /jobs/{jobId}/tasks/{taskId} | Updates the properties of the specified task. |
| GET | /jobs/{jobId}/tasks/{taskId}/subtasksinfo | Lists all of the subtasks that are associated with the specified multi-instance task. |
| POST | /jobs/{jobId}/tasks/{taskId}/terminate | Terminates the specified task. |
| POST | /jobs/{jobId}/tasks/{taskId}/reactivate | Reactivates a task, allowing it to run again even if its retry count has been exhausted. |

### pools
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /pools/{poolId}/nodes/{nodeId}/files/{filePath} | Deletes the specified file from the compute node. |
| GET | /pools/{poolId}/nodes/{nodeId}/files/{filePath} | Returns the content of the specified compute node file. |
| HEAD | /pools/{poolId}/nodes/{nodeId}/files/{filePath} | Gets the properties of the specified compute node file. |
| GET | /pools/{poolId}/nodes/{nodeId}/files | Lists all of the files in task directories on the specified compute node. |
| POST | /pools | Adds a pool to the specified account. |
| GET | /pools | Lists all of the pools in the specified account. |
| DELETE | /pools/{poolId} | Deletes a pool from the specified account. |
| HEAD | /pools/{poolId} | Gets basic properties of a pool. |
| GET | /pools/{poolId} | Gets information about the specified pool. |
| PATCH | /pools/{poolId} | Updates the properties of the specified pool. |
| POST | /pools/{poolId}/disableautoscale | Disables automatic scaling for a pool. |
| POST | /pools/{poolId}/enableautoscale | Enables automatic scaling for a pool. |
| POST | /pools/{poolId}/evaluateautoscale | Gets the result of evaluating an automatic scaling formula on the pool. |
| POST | /pools/{poolId}/resize | Changes the number of compute nodes that are assigned to a pool. |
| POST | /pools/{poolId}/stopresize | Stops an ongoing resize operation on the pool. |
| POST | /pools/{poolId}/updateproperties | Updates the properties of the specified pool. |
| POST | /pools/{poolId}/upgradeos | Upgrades the operating system of the specified pool. |
| POST | /pools/{poolId}/removenodes | Removes compute nodes from the specified pool. |
| POST | /pools/{poolId}/nodes/{nodeId}/users | Adds a user account to the specified compute node. |
| DELETE | /pools/{poolId}/nodes/{nodeId}/users/{userName} | Deletes a user account from the specified compute node. |
| PUT | /pools/{poolId}/nodes/{nodeId}/users/{userName} | Updates the password and expiration time of a user account on the specified compute node. |
| GET | /pools/{poolId}/nodes/{nodeId} | Gets information about the specified compute node. |
| POST | /pools/{poolId}/nodes/{nodeId}/reboot | Restarts the specified compute node. |
| POST | /pools/{poolId}/nodes/{nodeId}/reimage | Reinstalls the operating system on the specified compute node. |
| POST | /pools/{poolId}/nodes/{nodeId}/disablescheduling | Disables task scheduling on the specified compute node. |
| POST | /pools/{poolId}/nodes/{nodeId}/enablescheduling | Enables task scheduling on the specified compute node. |
| GET | /pools/{poolId}/nodes/{nodeId}/remoteloginsettings | Gets the settings required for remote login to a compute node. |
| GET | /pools/{poolId}/nodes/{nodeId}/rdp | Gets the Remote Desktop Protocol file for the specified compute node. |
| POST | /pools/{poolId}/nodes/{nodeId}/uploadbatchservicelogs | Upload Azure Batch service log files from the specified compute node to Azure Blob Storage. |
| GET | /pools/{poolId}/nodes | Lists the compute nodes in the specified pool. |

### jobschedules
| Method | Path | Description |
|--------|------|-------------|
| HEAD | /jobschedules/{jobScheduleId} | Checks the specified job schedule exists. |
| DELETE | /jobschedules/{jobScheduleId} | Deletes a job schedule from the specified account. |
| GET | /jobschedules/{jobScheduleId} | Gets information about the specified job schedule. |
| PATCH | /jobschedules/{jobScheduleId} | Updates the properties of the specified job schedule. |
| PUT | /jobschedules/{jobScheduleId} | Updates the properties of the specified job schedule. |
| POST | /jobschedules/{jobScheduleId}/disable | Disables a job schedule. |
| POST | /jobschedules/{jobScheduleId}/enable | Enables a job schedule. |
| POST | /jobschedules/{jobScheduleId}/terminate | Terminates a job schedule. |
| POST | /jobschedules | Adds a job schedule to the specified account. |
| GET | /jobschedules | Lists all of the job schedules in the specified account. |
| GET | /jobschedules/{jobScheduleId}/jobs | Lists the jobs that have been created under the specified job schedule. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all applications?" -> GET /applications
- "Get application details?" -> GET /applications/{applicationId}
- "List all poolusagemetrics?" -> GET /poolusagemetrics
- "List all nodeagentskus?" -> GET /nodeagentskus
- "List all nodecounts?" -> GET /nodecounts
- "List all lifetimepoolstats?" -> GET /lifetimepoolstats
- "List all lifetimejobstats?" -> GET /lifetimejobstats
- "Create a certificate?" -> POST /certificates
- "List all certificates?" -> GET /certificates
- "Create a canceldelete?" -> POST /certificates(thumbprintAlgorithm={thumbprintAlgorithm},thumbprint={thumbprint})/canceldelete
- "Delete a certificates(thumbprintAlgorithm={thumbprintAlgorithm},thumbprint={thumbprint})?" -> DELETE /certificates(thumbprintAlgorithm={thumbprintAlgorithm},thumbprint={thumbprint})
- "Get certificates(thumbprintAlgorithm={thumbprintAlgorithm},thumbprint={thumbprint}) details?" -> GET /certificates(thumbprintAlgorithm={thumbprintAlgorithm},thumbprint={thumbprint})
- "Delete a file?" -> DELETE /jobs/{jobId}/tasks/{taskId}/files/{filePath}
- "Get file details?" -> GET /jobs/{jobId}/tasks/{taskId}/files/{filePath}
- "Delete a file?" -> DELETE /pools/{poolId}/nodes/{nodeId}/files/{filePath}
- "Get file details?" -> GET /pools/{poolId}/nodes/{nodeId}/files/{filePath}
- "List all files?" -> GET /jobs/{jobId}/tasks/{taskId}/files
- "List all files?" -> GET /pools/{poolId}/nodes/{nodeId}/files
- "Delete a jobschedule?" -> DELETE /jobschedules/{jobScheduleId}
- "Get jobschedule details?" -> GET /jobschedules/{jobScheduleId}
- "Partially update a jobschedule?" -> PATCH /jobschedules/{jobScheduleId}
- "Update a jobschedule?" -> PUT /jobschedules/{jobScheduleId}
- "Create a disable?" -> POST /jobschedules/{jobScheduleId}/disable
- "Create a enable?" -> POST /jobschedules/{jobScheduleId}/enable
- "Create a terminate?" -> POST /jobschedules/{jobScheduleId}/terminate
- "Create a jobschedule?" -> POST /jobschedules
- "List all jobschedules?" -> GET /jobschedules
- "Delete a job?" -> DELETE /jobs/{jobId}
- "Get job details?" -> GET /jobs/{jobId}
- "Partially update a job?" -> PATCH /jobs/{jobId}
- "Update a job?" -> PUT /jobs/{jobId}
- "Create a disable?" -> POST /jobs/{jobId}/disable
- "Create a enable?" -> POST /jobs/{jobId}/enable
- "Create a terminate?" -> POST /jobs/{jobId}/terminate
- "Create a job?" -> POST /jobs
- "List all jobs?" -> GET /jobs
- "List all jobs?" -> GET /jobschedules/{jobScheduleId}/jobs
- "List all jobpreparationandreleasetaskstatus?" -> GET /jobs/{jobId}/jobpreparationandreleasetaskstatus
- "List all taskcounts?" -> GET /jobs/{jobId}/taskcounts
- "Create a pool?" -> POST /pools
- "List all pools?" -> GET /pools
- "Delete a pool?" -> DELETE /pools/{poolId}
- "Get pool details?" -> GET /pools/{poolId}
- "Partially update a pool?" -> PATCH /pools/{poolId}
- "Create a disableautoscale?" -> POST /pools/{poolId}/disableautoscale
- "Create a enableautoscale?" -> POST /pools/{poolId}/enableautoscale
- "Create a evaluateautoscale?" -> POST /pools/{poolId}/evaluateautoscale
- "Create a resize?" -> POST /pools/{poolId}/resize
- "Create a stopresize?" -> POST /pools/{poolId}/stopresize
- "Create a updateproperty?" -> POST /pools/{poolId}/updateproperties
- "Create a upgradeo?" -> POST /pools/{poolId}/upgradeos
- "Create a removenode?" -> POST /pools/{poolId}/removenodes
- "Create a task?" -> POST /jobs/{jobId}/tasks
- "List all tasks?" -> GET /jobs/{jobId}/tasks
- "Create a addtaskcollection?" -> POST /jobs/{jobId}/addtaskcollection
- "Delete a task?" -> DELETE /jobs/{jobId}/tasks/{taskId}
- "Get task details?" -> GET /jobs/{jobId}/tasks/{taskId}
- "Update a task?" -> PUT /jobs/{jobId}/tasks/{taskId}
- "List all subtasksinfo?" -> GET /jobs/{jobId}/tasks/{taskId}/subtasksinfo
- "Create a terminate?" -> POST /jobs/{jobId}/tasks/{taskId}/terminate
- "Create a reactivate?" -> POST /jobs/{jobId}/tasks/{taskId}/reactivate
- "Create a user?" -> POST /pools/{poolId}/nodes/{nodeId}/users
- "Delete a user?" -> DELETE /pools/{poolId}/nodes/{nodeId}/users/{userName}
- "Update a user?" -> PUT /pools/{poolId}/nodes/{nodeId}/users/{userName}
- "Get node details?" -> GET /pools/{poolId}/nodes/{nodeId}
- "Create a reboot?" -> POST /pools/{poolId}/nodes/{nodeId}/reboot
- "Create a reimage?" -> POST /pools/{poolId}/nodes/{nodeId}/reimage
- "Create a disablescheduling?" -> POST /pools/{poolId}/nodes/{nodeId}/disablescheduling
- "Create a enablescheduling?" -> POST /pools/{poolId}/nodes/{nodeId}/enablescheduling
- "List all remoteloginsettings?" -> GET /pools/{poolId}/nodes/{nodeId}/remoteloginsettings
- "List all rdp?" -> GET /pools/{poolId}/nodes/{nodeId}/rdp
- "Create a uploadbatchservicelog?" -> POST /pools/{poolId}/nodes/{nodeId}/uploadbatchservicelogs
- "List all nodes?" -> GET /pools/{poolId}/nodes

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
