---
name: aws-robomaker
description: "AWS RoboMaker API skill. Use when working with AWS RoboMaker for batchDeleteWorlds, batchDescribeSimulationJob, cancelDeploymentJob. Covers 57 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS RoboMaker
API version: 2018-06-29

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /tags/{resourceArn} -- verify access
3. POST /batchDeleteWorlds -- create first batchDeleteWorlds

## Endpoints

57 endpoints across 55 groups. See references/api-spec.lap for full details.

### batchDeleteWorlds
| Method | Path | Description |
|--------|------|-------------|
| POST | /batchDeleteWorlds | Deletes one or more worlds in a batch operation. |

### batchDescribeSimulationJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /batchDescribeSimulationJob | Describes one or more simulation jobs. |

### cancelDeploymentJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /cancelDeploymentJob | Cancels the specified deployment job.  This API will no longer be supported as of May 2, 2022. Use it to remove resources that were created for Deployment Service. |

### cancelSimulationJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /cancelSimulationJob | Cancels the specified simulation job. |

### cancelSimulationJobBatch
| Method | Path | Description |
|--------|------|-------------|
| POST | /cancelSimulationJobBatch | Cancels a simulation job batch. When you cancel a simulation job batch, you are also cancelling all of the active simulation jobs created as part of the batch. |

### cancelWorldExportJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /cancelWorldExportJob | Cancels the specified export job. |

### cancelWorldGenerationJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /cancelWorldGenerationJob | Cancels the specified world generator job. |

### createDeploymentJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /createDeploymentJob | Deploys a specific version of a robot application to robots in a fleet.  This API is no longer supported and will throw an error if used.  The robot application must have a numbered applicationVersion for consistency reasons. To create a new version, use CreateRobotApplicationVersion or see Creating a Robot Application Version.   After 90 days, deployment jobs expire and will be deleted. They will no longer be accessible. |

### createFleet
| Method | Path | Description |
|--------|------|-------------|
| POST | /createFleet | Creates a fleet, a logical group of robots running the same robot application.  This API is no longer supported and will throw an error if used. |

### createRobot
| Method | Path | Description |
|--------|------|-------------|
| POST | /createRobot | Creates a robot.  This API is no longer supported and will throw an error if used. |

### createRobotApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /createRobotApplication | Creates a robot application. |

### createRobotApplicationVersion
| Method | Path | Description |
|--------|------|-------------|
| POST | /createRobotApplicationVersion | Creates a version of a robot application. |

### createSimulationApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /createSimulationApplication | Creates a simulation application. |

### createSimulationApplicationVersion
| Method | Path | Description |
|--------|------|-------------|
| POST | /createSimulationApplicationVersion | Creates a simulation application with a specific revision id. |

### createSimulationJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /createSimulationJob | Creates a simulation job.  After 90 days, simulation jobs expire and will be deleted. They will no longer be accessible. |

### createWorldExportJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /createWorldExportJob | Creates a world export job. |

### createWorldGenerationJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /createWorldGenerationJob | Creates worlds using the specified template. |

### createWorldTemplate
| Method | Path | Description |
|--------|------|-------------|
| POST | /createWorldTemplate | Creates a world template. |

### deleteFleet
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteFleet | Deletes a fleet.  This API will no longer be supported as of May 2, 2022. Use it to remove resources that were created for Deployment Service. |

### deleteRobot
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteRobot | Deletes a robot.  This API will no longer be supported as of May 2, 2022. Use it to remove resources that were created for Deployment Service. |

### deleteRobotApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteRobotApplication | Deletes a robot application. |

### deleteSimulationApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteSimulationApplication | Deletes a simulation application. |

### deleteWorldTemplate
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteWorldTemplate | Deletes a world template. |

### deregisterRobot
| Method | Path | Description |
|--------|------|-------------|
| POST | /deregisterRobot | Deregisters a robot.  This API will no longer be supported as of May 2, 2022. Use it to remove resources that were created for Deployment Service. |

### describeDeploymentJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeDeploymentJob | Describes a deployment job.  This API will no longer be supported as of May 2, 2022. Use it to remove resources that were created for Deployment Service. |

### describeFleet
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeFleet | Describes a fleet.  This API will no longer be supported as of May 2, 2022. Use it to remove resources that were created for Deployment Service. |

### describeRobot
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeRobot | Describes a robot.  This API will no longer be supported as of May 2, 2022. Use it to remove resources that were created for Deployment Service. |

### describeRobotApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeRobotApplication | Describes a robot application. |

### describeSimulationApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeSimulationApplication | Describes a simulation application. |

### describeSimulationJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeSimulationJob | Describes a simulation job. |

### describeSimulationJobBatch
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeSimulationJobBatch | Describes a simulation job batch. |

### describeWorld
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeWorld | Describes a world. |

### describeWorldExportJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeWorldExportJob | Describes a world export job. |

### describeWorldGenerationJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeWorldGenerationJob | Describes a world generation job. |

### describeWorldTemplate
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeWorldTemplate | Describes a world template. |

### getWorldTemplateBody
| Method | Path | Description |
|--------|------|-------------|
| POST | /getWorldTemplateBody | Gets the world template body. |

### listDeploymentJobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /listDeploymentJobs | Returns a list of deployment jobs for a fleet. You can optionally provide filters to retrieve specific deployment jobs.  This API will no longer be supported as of May 2, 2022. Use it to remove resources that were created for Deployment Service. |

### listFleets
| Method | Path | Description |
|--------|------|-------------|
| POST | /listFleets | Returns a list of fleets. You can optionally provide filters to retrieve specific fleets.  This API will no longer be supported as of May 2, 2022. Use it to remove resources that were created for Deployment Service. |

### listRobotApplications
| Method | Path | Description |
|--------|------|-------------|
| POST | /listRobotApplications | Returns a list of robot application. You can optionally provide filters to retrieve specific robot applications. |

### listRobots
| Method | Path | Description |
|--------|------|-------------|
| POST | /listRobots | Returns a list of robots. You can optionally provide filters to retrieve specific robots.  This API will no longer be supported as of May 2, 2022. Use it to remove resources that were created for Deployment Service. |

### listSimulationApplications
| Method | Path | Description |
|--------|------|-------------|
| POST | /listSimulationApplications | Returns a list of simulation applications. You can optionally provide filters to retrieve specific simulation applications. |

### listSimulationJobBatches
| Method | Path | Description |
|--------|------|-------------|
| POST | /listSimulationJobBatches | Returns a list simulation job batches. You can optionally provide filters to retrieve specific simulation batch jobs. |

### listSimulationJobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /listSimulationJobs | Returns a list of simulation jobs. You can optionally provide filters to retrieve specific simulation jobs. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists all tags on a AWS RoboMaker resource. |
| POST | /tags/{resourceArn} | Adds or edits tags for a AWS RoboMaker resource. Each tag consists of a tag key and a tag value. Tag keys and tag values are both required, but tag values can be empty strings.  For information about the rules that apply to tag keys and tag values, see User-Defined Tag Restrictions in the AWS Billing and Cost Management User Guide. |
| DELETE | /tags/{resourceArn} | Removes the specified tags from the specified AWS RoboMaker resource. To remove a tag, specify the tag key. To change the tag value of an existing tag key, use  TagResource . |

### listWorldExportJobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /listWorldExportJobs | Lists world export jobs. |

### listWorldGenerationJobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /listWorldGenerationJobs | Lists world generator jobs. |

### listWorldTemplates
| Method | Path | Description |
|--------|------|-------------|
| POST | /listWorldTemplates | Lists world templates. |

### listWorlds
| Method | Path | Description |
|--------|------|-------------|
| POST | /listWorlds | Lists worlds. |

### registerRobot
| Method | Path | Description |
|--------|------|-------------|
| POST | /registerRobot | Registers a robot with a fleet.  This API is no longer supported and will throw an error if used. |

### restartSimulationJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /restartSimulationJob | Restarts a running simulation job. |

### startSimulationJobBatch
| Method | Path | Description |
|--------|------|-------------|
| POST | /startSimulationJobBatch | Starts a new simulation job batch. The batch is defined using one or more SimulationJobRequest objects. |

### syncDeploymentJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /syncDeploymentJob | Syncrhonizes robots in a fleet to the latest deployment. This is helpful if robots were added after a deployment.  This API will no longer be supported as of May 2, 2022. Use it to remove resources that were created for Deployment Service. |

### updateRobotApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateRobotApplication | Updates a robot application. |

### updateSimulationApplication
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateSimulationApplication | Updates a simulation application. |

### updateWorldTemplate
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateWorldTemplate | Updates a world template. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a batchDeleteWorld?" -> POST /batchDeleteWorlds
- "Create a batchDescribeSimulationJob?" -> POST /batchDescribeSimulationJob
- "Create a cancelDeploymentJob?" -> POST /cancelDeploymentJob
- "Create a cancelSimulationJob?" -> POST /cancelSimulationJob
- "Create a cancelSimulationJobBatch?" -> POST /cancelSimulationJobBatch
- "Create a cancelWorldExportJob?" -> POST /cancelWorldExportJob
- "Create a cancelWorldGenerationJob?" -> POST /cancelWorldGenerationJob
- "Create a createDeploymentJob?" -> POST /createDeploymentJob
- "Create a createFleet?" -> POST /createFleet
- "Create a createRobot?" -> POST /createRobot
- "Create a createRobotApplication?" -> POST /createRobotApplication
- "Create a createRobotApplicationVersion?" -> POST /createRobotApplicationVersion
- "Create a createSimulationApplication?" -> POST /createSimulationApplication
- "Create a createSimulationApplicationVersion?" -> POST /createSimulationApplicationVersion
- "Create a createSimulationJob?" -> POST /createSimulationJob
- "Create a createWorldExportJob?" -> POST /createWorldExportJob
- "Create a createWorldGenerationJob?" -> POST /createWorldGenerationJob
- "Create a createWorldTemplate?" -> POST /createWorldTemplate
- "Create a deleteFleet?" -> POST /deleteFleet
- "Create a deleteRobot?" -> POST /deleteRobot
- "Create a deleteRobotApplication?" -> POST /deleteRobotApplication
- "Create a deleteSimulationApplication?" -> POST /deleteSimulationApplication
- "Create a deleteWorldTemplate?" -> POST /deleteWorldTemplate
- "Create a deregisterRobot?" -> POST /deregisterRobot
- "Create a describeDeploymentJob?" -> POST /describeDeploymentJob
- "Create a describeFleet?" -> POST /describeFleet
- "Create a describeRobot?" -> POST /describeRobot
- "Create a describeRobotApplication?" -> POST /describeRobotApplication
- "Create a describeSimulationApplication?" -> POST /describeSimulationApplication
- "Create a describeSimulationJob?" -> POST /describeSimulationJob
- "Create a describeSimulationJobBatch?" -> POST /describeSimulationJobBatch
- "Create a describeWorld?" -> POST /describeWorld
- "Create a describeWorldExportJob?" -> POST /describeWorldExportJob
- "Create a describeWorldGenerationJob?" -> POST /describeWorldGenerationJob
- "Create a describeWorldTemplate?" -> POST /describeWorldTemplate
- "Create a getWorldTemplateBody?" -> POST /getWorldTemplateBody
- "Create a listDeploymentJob?" -> POST /listDeploymentJobs
- "Create a listFleet?" -> POST /listFleets
- "Create a listRobotApplication?" -> POST /listRobotApplications
- "Create a listRobot?" -> POST /listRobots
- "Create a listSimulationApplication?" -> POST /listSimulationApplications
- "Create a listSimulationJobBatche?" -> POST /listSimulationJobBatches
- "Create a listSimulationJob?" -> POST /listSimulationJobs
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a listWorldExportJob?" -> POST /listWorldExportJobs
- "Create a listWorldGenerationJob?" -> POST /listWorldGenerationJobs
- "Create a listWorldTemplate?" -> POST /listWorldTemplates
- "Create a listWorld?" -> POST /listWorlds
- "Create a registerRobot?" -> POST /registerRobot
- "Create a restartSimulationJob?" -> POST /restartSimulationJob
- "Create a startSimulationJobBatch?" -> POST /startSimulationJobBatch
- "Create a syncDeploymentJob?" -> POST /syncDeploymentJob
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Create a updateRobotApplication?" -> POST /updateRobotApplication
- "Create a updateSimulationApplication?" -> POST /updateSimulationApplication
- "Create a updateWorldTemplate?" -> POST /updateWorldTemplate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
