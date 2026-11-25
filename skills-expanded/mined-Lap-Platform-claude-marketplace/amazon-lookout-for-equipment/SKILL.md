---
name: amazon-lookout-for-equipment
description: "Amazon Lookout for Equipment API skill. Use when working with Amazon Lookout for Equipment for root. Covers 49 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Lookout for Equipment
API version: 2020-12-15

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

49 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates a container for a collection of data being ingested for analysis. The dataset contains the metadata describing where the data is and what the data actually looks like. For example, it contains the location of the data source, the data schema, and other information. A dataset also contains any tags associated with the ingested data. |
| POST | / | Creates a scheduled inference. Scheduling an inference is setting up a continuous real-time inference plan to analyze new measurement data. When setting up the schedule, you provide an S3 bucket location for the input data, assign it a delimiter between separate entries in the data, set an offset delay if desired, and set the frequency of inferencing. You must also provide an S3 bucket location for the output data. |
| POST | / | Creates a label for an event. |
| POST | / | Creates a group of labels. |
| POST | / | Creates a machine learning model for data inference.  A machine-learning (ML) model is a mathematical model that finds patterns in your data. In Amazon Lookout for Equipment, the model learns the patterns of normal behavior and detects abnormal behavior that could be potential equipment failure (or maintenance events). The models are made by analyzing normal data and abnormalities in machine behavior that have already occurred. Your model is trained using a portion of the data from your dataset and uses that data to learn patterns of normal behavior and abnormal patterns that lead to equipment failure. Another portion of the data is used to evaluate the model's accuracy. |
| POST | / | Creates a retraining scheduler on the specified model. |
| POST | / | Deletes a dataset and associated artifacts. The operation will check to see if any inference scheduler or data ingestion job is currently using the dataset, and if there isn't, the dataset, its metadata, and any associated data stored in S3 will be deleted. This does not affect any models that used this dataset for training and evaluation, but does prevent it from being used in the future. |
| POST | / | Deletes an inference scheduler that has been set up. Prior inference results will not be deleted. |
| POST | / | Deletes a label. |
| POST | / | Deletes a group of labels. |
| POST | / | Deletes a machine learning model currently available for Amazon Lookout for Equipment. This will prevent it from being used with an inference scheduler, even one that is already set up. |
| POST | / | Deletes the resource policy attached to the resource. |
| POST | / | Deletes a retraining scheduler from a model. The retraining scheduler must be in the STOPPED status. |
| POST | / | Provides information on a specific data ingestion job such as creation time, dataset ARN, and status. |
| POST | / | Provides a JSON description of the data in each time series dataset, including names, column names, and data types. |
| POST | / | Specifies information about the inference scheduler being used, including name, model, status, and associated metadata |
| POST | / | Returns the name of the label. |
| POST | / | Returns information about the label group. |
| POST | / | Provides a JSON containing the overall information about a specific machine learning model, including model name and ARN, dataset, training and evaluation information, status, and so on. |
| POST | / | Retrieves information about a specific machine learning model version. |
| POST | / | Provides the details of a resource policy attached to a resource. |
| POST | / | Provides a description of the retraining scheduler, including information such as the model name and retraining parameters. |
| POST | / | Imports a dataset. |
| POST | / | Imports a model that has been trained successfully. |
| POST | / | Provides a list of all data ingestion jobs, including dataset name and ARN, S3 location of the input data, status, and so on. |
| POST | / | Lists all datasets currently available in your account, filtering on the dataset name. |
| POST | / | Lists all inference events that have been found for the specified inference scheduler. |
| POST | / | Lists all inference executions that have been performed by the specified inference scheduler. |
| POST | / | Retrieves a list of all inference schedulers currently available for your account. |
| POST | / | Returns a list of the label groups. |
| POST | / | Provides a list of labels. |
| POST | / | Generates a list of all model versions for a given model, including the model version, model version ARN, and status. To list a subset of versions, use the MaxModelVersion and MinModelVersion fields. |
| POST | / | Generates a list of all models in the account, including model name and ARN, dataset, and status. |
| POST | / | Lists all retraining schedulers in your account, filtering by model name prefix and status. |
| POST | / | Lists statistics about the data collected for each of the sensors that have been successfully ingested in the particular dataset. Can also be used to retreive Sensor Statistics for a previous ingestion job. |
| POST | / | Lists all the tags for a specified resource, including key and value. |
| POST | / | Creates a resource control policy for a given resource. |
| POST | / | Starts a data ingestion job. Amazon Lookout for Equipment returns the job status. |
| POST | / | Starts an inference scheduler. |
| POST | / | Starts a retraining scheduler. |
| POST | / | Stops an inference scheduler. |
| POST | / | Stops a retraining scheduler. |
| POST | / | Associates a given tag to a resource in your account. A tag is a key-value pair which can be added to an Amazon Lookout for Equipment resource as metadata. Tags can be used for organizing your resources as well as helping you to search and filter by tag. Multiple tags can be added to a resource, either when you create it, or later. Up to 50 tags can be associated with each resource. |
| POST | / | Removes a specific tag from a given resource. The tag is specified by its key. |
| POST | / | Sets the active model version for a given machine learning model. |
| POST | / | Updates an inference scheduler. |
| POST | / | Updates the label group. |
| POST | / | Updates a model in the account. |
| POST | / | Updates a retraining scheduler. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
