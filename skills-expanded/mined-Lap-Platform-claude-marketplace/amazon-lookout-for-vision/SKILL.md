---
name: amazon-lookout-for-vision
description: "Amazon Lookout for Vision API skill. Use when working with Amazon Lookout for Vision for 2020-11-20. Covers 22 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Lookout for Vision
API version: 2020-11-20

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /2020-11-20/projects -- verify access
3. POST /2020-11-20/projects/{projectName}/datasets -- create first datasets

## Endpoints

22 endpoints across 1 groups. See references/api-spec.lap for full details.

### 2020-11-20
| Method | Path | Description |
|--------|------|-------------|
| POST | /2020-11-20/projects/{projectName}/datasets | Creates a new dataset in an Amazon Lookout for Vision project. CreateDataset can create a training or a test dataset from a valid dataset source (DatasetSource). If you want a single dataset project, specify train for the value of DatasetType. To have a project with separate training and test datasets, call CreateDataset twice. On the first call, specify train for the value of DatasetType. On the second call, specify test for the value of DatasetType.  This operation requires permissions to perform the lookoutvision:CreateDataset operation. |
| POST | /2020-11-20/projects/{projectName}/models | Creates a new version of a model within an an Amazon Lookout for Vision project. CreateModel is an asynchronous operation in which Amazon Lookout for Vision trains, tests, and evaluates a new version of a model.  To get the current status, check the Status field returned in the response from DescribeModel. If the project has a single dataset, Amazon Lookout for Vision internally splits the dataset to create a training and a test dataset. If the project has a training and a test dataset, Lookout for Vision uses the respective datasets to train and test the model.  After training completes, the evaluation metrics are stored at the location specified in OutputConfig.  This operation requires permissions to perform the lookoutvision:CreateModel operation. If you want to tag your model, you also require permission to the lookoutvision:TagResource operation. |
| POST | /2020-11-20/projects | Creates an empty Amazon Lookout for Vision project. After you create the project, add a dataset by calling CreateDataset. This operation requires permissions to perform the lookoutvision:CreateProject operation. |
| DELETE | /2020-11-20/projects/{projectName}/datasets/{datasetType} | Deletes an existing Amazon Lookout for Vision dataset.  If your the project has a single dataset, you must create a new dataset before you can create a model. If you project has a training dataset and a test dataset consider the following.    If you delete the test dataset, your project reverts to a single dataset project. If you then train the model, Amazon Lookout for Vision internally splits the remaining dataset into a training and test dataset.   If you delete the training dataset, you must create a training dataset before you can create a model.   This operation requires permissions to perform the lookoutvision:DeleteDataset operation. |
| DELETE | /2020-11-20/projects/{projectName}/models/{modelVersion} | Deletes an Amazon Lookout for Vision model. You can't delete a running model. To stop a running model, use the StopModel operation. It might take a few seconds to delete a model. To determine if a model has been deleted, call ListModels and check if the version of the model (ModelVersion) is in the Models array.   This operation requires permissions to perform the lookoutvision:DeleteModel operation. |
| DELETE | /2020-11-20/projects/{projectName} | Deletes an Amazon Lookout for Vision project. To delete a project, you must first delete each version of the model associated with the project. To delete a model use the DeleteModel operation. You also have to delete the dataset(s) associated with the model. For more information, see DeleteDataset. The images referenced by the training and test datasets aren't deleted.  This operation requires permissions to perform the lookoutvision:DeleteProject operation. |
| GET | /2020-11-20/projects/{projectName}/datasets/{datasetType} | Describe an Amazon Lookout for Vision dataset. This operation requires permissions to perform the lookoutvision:DescribeDataset operation. |
| GET | /2020-11-20/projects/{projectName}/models/{modelVersion} | Describes a version of an Amazon Lookout for Vision model. This operation requires permissions to perform the lookoutvision:DescribeModel operation. |
| GET | /2020-11-20/projects/{projectName}/modelpackagingjobs/{jobName} | Describes an Amazon Lookout for Vision model packaging job.  This operation requires permissions to perform the lookoutvision:DescribeModelPackagingJob operation. For more information, see Using your Amazon Lookout for Vision model on an edge device in the Amazon Lookout for Vision Developer Guide. |
| GET | /2020-11-20/projects/{projectName} | Describes an Amazon Lookout for Vision project. This operation requires permissions to perform the lookoutvision:DescribeProject operation. |
| POST | /2020-11-20/projects/{projectName}/models/{modelVersion}/detect | Detects anomalies in an image that you supply.  The response from DetectAnomalies includes a boolean prediction that the image contains one or more anomalies and a confidence value for the prediction. If the model is an image segmentation model, the response also includes segmentation information for each type of anomaly found in the image.  Before calling DetectAnomalies, you must first start your model with the StartModel operation. You are charged for the amount of time, in minutes, that a model runs and for the number of anomaly detection units that your model uses. If you are not using a model, use the StopModel operation to stop your model.   For more information, see Detecting anomalies in an image in the Amazon Lookout for Vision developer guide. This operation requires permissions to perform the lookoutvision:DetectAnomalies operation. |
| GET | /2020-11-20/projects/{projectName}/datasets/{datasetType}/entries | Lists the JSON Lines within a dataset. An Amazon Lookout for Vision JSON Line contains the anomaly information for a single image, including the image location and the assigned label. This operation requires permissions to perform the lookoutvision:ListDatasetEntries operation. |
| GET | /2020-11-20/projects/{projectName}/modelpackagingjobs | Lists the model packaging jobs created for an Amazon Lookout for Vision project.  This operation requires permissions to perform the lookoutvision:ListModelPackagingJobs operation.  For more information, see Using your Amazon Lookout for Vision model on an edge device in the Amazon Lookout for Vision Developer Guide. |
| GET | /2020-11-20/projects/{projectName}/models | Lists the versions of a model in an Amazon Lookout for Vision project. The ListModels operation is eventually consistent. Recent calls to CreateModel might take a while to appear in the response from ListProjects. This operation requires permissions to perform the lookoutvision:ListModels operation. |
| GET | /2020-11-20/projects | Lists the Amazon Lookout for Vision projects in your AWS account that are in the AWS Region in which you call ListProjects. The ListProjects operation is eventually consistent. Recent calls to CreateProject and DeleteProject might take a while to appear in the response from ListProjects. This operation requires permissions to perform the lookoutvision:ListProjects operation. |
| GET | /2020-11-20/tags/{resourceArn} | Returns a list of tags attached to the specified Amazon Lookout for Vision model. This operation requires permissions to perform the lookoutvision:ListTagsForResource operation. |
| POST | /2020-11-20/projects/{projectName}/models/{modelVersion}/start | Starts the running of the version of an Amazon Lookout for Vision model. Starting a model takes a while to complete. To check the current state of the model, use DescribeModel. A model is ready to use when its status is HOSTED. Once the model is running, you can detect custom labels in new images by calling DetectAnomalies.  You are charged for the amount of time that the model is running. To stop a running model, call StopModel.  This operation requires permissions to perform the lookoutvision:StartModel operation. |
| POST | /2020-11-20/projects/{projectName}/modelpackagingjobs | Starts an Amazon Lookout for Vision model packaging job. A model packaging job creates an AWS IoT Greengrass component for a Lookout for Vision model. You can use the component to deploy your model to an edge device managed by Greengrass.  Use the DescribeModelPackagingJob API to determine the current status of the job. The model packaging job is complete if the value of Status is SUCCEEDED. To deploy the component to the target device, use the component name and component version with the AWS IoT Greengrass CreateDeployment API. This operation requires the following permissions:    lookoutvision:StartModelPackagingJob     s3:PutObject     s3:GetBucketLocation     kms:GenerateDataKey     greengrass:CreateComponentVersion     greengrass:DescribeComponent    (Optional) greengrass:TagResource. Only required if you want to tag the component.   For more information, see Using your Amazon Lookout for Vision model on an edge device in the Amazon Lookout for Vision Developer Guide. |
| POST | /2020-11-20/projects/{projectName}/models/{modelVersion}/stop | Stops the hosting of a running model. The operation might take a while to complete. To check the current status, call DescribeModel.  After the model hosting stops, the Status of the model is TRAINED. This operation requires permissions to perform the lookoutvision:StopModel operation. |
| POST | /2020-11-20/tags/{resourceArn} | Adds one or more key-value tags to an Amazon Lookout for Vision model. For more information, see Tagging a model in the Amazon Lookout for Vision Developer Guide.  This operation requires permissions to perform the lookoutvision:TagResource operation. |
| DELETE | /2020-11-20/tags/{resourceArn} | Removes one or more tags from an Amazon Lookout for Vision model. For more information, see Tagging a model in the Amazon Lookout for Vision Developer Guide.  This operation requires permissions to perform the lookoutvision:UntagResource operation. |
| PATCH | /2020-11-20/projects/{projectName}/datasets/{datasetType}/entries | Adds or updates one or more JSON Line entries in a dataset. A JSON Line includes information about an image used for training or testing an Amazon Lookout for Vision model. To update an existing JSON Line, use the source-ref field to identify the JSON Line. The JSON line that you supply replaces the existing JSON line. Any existing annotations that are not in the new JSON line are removed from the dataset.  For more information, see Defining JSON lines for anomaly classification in the Amazon Lookout for Vision Developer Guide.   The images you reference in the source-ref field of a JSON line, must be in the same S3 bucket as the existing images in the dataset.   Updating a dataset might take a while to complete. To check the current status, call DescribeDataset and check the Status field in the response. This operation requires permissions to perform the lookoutvision:UpdateDatasetEntries operation. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a dataset?" -> POST /2020-11-20/projects/{projectName}/datasets
- "Create a model?" -> POST /2020-11-20/projects/{projectName}/models
- "Create a project?" -> POST /2020-11-20/projects
- "Delete a dataset?" -> DELETE /2020-11-20/projects/{projectName}/datasets/{datasetType}
- "Delete a model?" -> DELETE /2020-11-20/projects/{projectName}/models/{modelVersion}
- "Delete a project?" -> DELETE /2020-11-20/projects/{projectName}
- "Get dataset details?" -> GET /2020-11-20/projects/{projectName}/datasets/{datasetType}
- "Get model details?" -> GET /2020-11-20/projects/{projectName}/models/{modelVersion}
- "Get modelpackagingjob details?" -> GET /2020-11-20/projects/{projectName}/modelpackagingjobs/{jobName}
- "Get project details?" -> GET /2020-11-20/projects/{projectName}
- "Create a detect?" -> POST /2020-11-20/projects/{projectName}/models/{modelVersion}/detect
- "List all entries?" -> GET /2020-11-20/projects/{projectName}/datasets/{datasetType}/entries
- "List all modelpackagingjobs?" -> GET /2020-11-20/projects/{projectName}/modelpackagingjobs
- "List all models?" -> GET /2020-11-20/projects/{projectName}/models
- "List all projects?" -> GET /2020-11-20/projects
- "Get tag details?" -> GET /2020-11-20/tags/{resourceArn}
- "Create a start?" -> POST /2020-11-20/projects/{projectName}/models/{modelVersion}/start
- "Create a modelpackagingjob?" -> POST /2020-11-20/projects/{projectName}/modelpackagingjobs
- "Create a stop?" -> POST /2020-11-20/projects/{projectName}/models/{modelVersion}/stop
- "Delete a tag?" -> DELETE /2020-11-20/tags/{resourceArn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
