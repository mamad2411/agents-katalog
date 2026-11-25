---
name: amazon-comprehend
description: "Amazon Comprehend API skill. Use when working with Amazon Comprehend for root. Covers 85 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Comprehend
API version: 2017-11-27

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

85 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Determines the dominant language of the input text for a batch of documents. For a list of languages that Amazon Comprehend can detect, see Amazon Comprehend Supported Languages. |
| POST | / | Inspects the text of a batch of documents for named entities and returns information about them. For more information about named entities, see Entities in the Comprehend Developer Guide. |
| POST | / | Detects the key noun phrases found in a batch of documents. |
| POST | / | Inspects a batch of documents and returns an inference of the prevailing sentiment, POSITIVE, NEUTRAL, MIXED, or NEGATIVE, in each one. |
| POST | / | Inspects the text of a batch of documents for the syntax and part of speech of the words in the document and returns information about them. For more information, see Syntax in the Comprehend Developer Guide. |
| POST | / | Inspects a batch of documents and returns a sentiment analysis for each entity identified in the documents. For more information about targeted sentiment, see Targeted sentiment in the Amazon Comprehend Developer Guide. |
| POST | / | Creates a classification request to analyze a single document in real-time. ClassifyDocument supports the following model types:   Custom classifier - a custom model that you have created and trained. For input, you can provide plain text, a single-page document (PDF, Word, or image), or Amazon Textract API output. For more information, see Custom classification in the Amazon Comprehend Developer Guide.   Prompt safety classifier - Amazon Comprehend provides a pre-trained model for classifying input prompts for generative AI applications. For input, you provide English plain text input. For prompt safety classification, the response includes only the Classes field. For more information about prompt safety classifiers, see Prompt safety classification in the Amazon Comprehend Developer Guide.   If the system detects errors while processing a page in the input document, the API response includes an Errors field that describes the errors. If the system detects a document-level error in your input document, the API returns an InvalidRequestException error response. For details about this exception, see  Errors in semi-structured documents in the Comprehend Developer Guide. |
| POST | / | Analyzes input text for the presence of personally identifiable information (PII) and returns the labels of identified PII entity types such as name, address, bank account number, or phone number. |
| POST | / | Creates a dataset to upload training or test data for a model associated with a flywheel. For more information about datasets, see  Flywheel overview in the Amazon Comprehend Developer Guide. |
| POST | / | Creates a new document classifier that you can use to categorize documents. To create a classifier, you provide a set of training documents that are labeled with the categories that you want to use. For more information, see Training classifier models in the Comprehend Developer Guide. |
| POST | / | Creates a model-specific endpoint for synchronous inference for a previously trained custom model For information about endpoints, see Managing endpoints. |
| POST | / | Creates an entity recognizer using submitted files. After your CreateEntityRecognizer request is submitted, you can check job status using the DescribeEntityRecognizer API. |
| POST | / | A flywheel is an Amazon Web Services resource that orchestrates the ongoing training of a model for custom classification or custom entity recognition. You can create a flywheel to start with an existing trained model, or Comprehend can create and train a new model. When you create the flywheel, Comprehend creates a data lake in your account. The data lake holds the training data and test data for all versions of the model. To use a flywheel with an existing trained model, you specify the active model version. Comprehend copies the model's training data and test data into the flywheel's data lake. To use the flywheel with a new model, you need to provide a dataset for training data (and optional test data) when you create the flywheel. For more information about flywheels, see  Flywheel overview in the Amazon Comprehend Developer Guide. |
| POST | / | Deletes a previously created document classifier Only those classifiers that are in terminated states (IN_ERROR, TRAINED) will be deleted. If an active inference job is using the model, a ResourceInUseException will be returned. This is an asynchronous action that puts the classifier into a DELETING state, and it is then removed by a background job. Once removed, the classifier disappears from your account and is no longer available for use. |
| POST | / | Deletes a model-specific endpoint for a previously-trained custom model. All endpoints must be deleted in order for the model to be deleted. For information about endpoints, see Managing endpoints. |
| POST | / | Deletes an entity recognizer. Only those recognizers that are in terminated states (IN_ERROR, TRAINED) will be deleted. If an active inference job is using the model, a ResourceInUseException will be returned. This is an asynchronous action that puts the recognizer into a DELETING state, and it is then removed by a background job. Once removed, the recognizer disappears from your account and is no longer available for use. |
| POST | / | Deletes a flywheel. When you delete the flywheel, Amazon Comprehend does not delete the data lake or the model associated with the flywheel. For more information about flywheels, see  Flywheel overview in the Amazon Comprehend Developer Guide. |
| POST | / | Deletes a resource-based policy that is attached to a custom model. |
| POST | / | Returns information about the dataset that you specify. For more information about datasets, see  Flywheel overview in the Amazon Comprehend Developer Guide. |
| POST | / | Gets the properties associated with a document classification job. Use this operation to get the status of a classification job. |
| POST | / | Gets the properties associated with a document classifier. |
| POST | / | Gets the properties associated with a dominant language detection job. Use this operation to get the status of a detection job. |
| POST | / | Gets the properties associated with a specific endpoint. Use this operation to get the status of an endpoint. For information about endpoints, see Managing endpoints. |
| POST | / | Gets the properties associated with an entities detection job. Use this operation to get the status of a detection job. |
| POST | / | Provides details about an entity recognizer including status, S3 buckets containing training data, recognizer metadata, metrics, and so on. |
| POST | / | Gets the status and details of an events detection job. |
| POST | / | Provides configuration information about the flywheel. For more information about flywheels, see  Flywheel overview in the Amazon Comprehend Developer Guide. |
| POST | / | Retrieve the configuration properties of a flywheel iteration. For more information about flywheels, see  Flywheel overview in the Amazon Comprehend Developer Guide. |
| POST | / | Gets the properties associated with a key phrases detection job. Use this operation to get the status of a detection job. |
| POST | / | Gets the properties associated with a PII entities detection job. For example, you can use this operation to get the job status. |
| POST | / | Gets the details of a resource-based policy that is attached to a custom model, including the JSON body of the policy. |
| POST | / | Gets the properties associated with a sentiment detection job. Use this operation to get the status of a detection job. |
| POST | / | Gets the properties associated with a targeted sentiment detection job. Use this operation to get the status of the job. |
| POST | / | Gets the properties associated with a topic detection job. Use this operation to get the status of a detection job. |
| POST | / | Determines the dominant language of the input text. For a list of languages that Amazon Comprehend can detect, see Amazon Comprehend Supported Languages. |
| POST | / | Detects named entities in input text when you use the pre-trained model. Detects custom entities if you have a custom entity recognition model.   When detecting named entities using the pre-trained model, use plain text as the input. For more information about named entities, see Entities in the Comprehend Developer Guide. When you use a custom entity recognition model, you can input plain text or you can upload a single-page input document (text, PDF, Word, or image).  If the system detects errors while processing a page in the input document, the API response includes an entry in Errors for each error.  If the system detects a document-level error in your input document, the API returns an InvalidRequestException error response. For details about this exception, see  Errors in semi-structured documents in the Comprehend Developer Guide. |
| POST | / | Detects the key noun phrases found in the text. |
| POST | / | Inspects the input text for entities that contain personally identifiable information (PII) and returns information about them. |
| POST | / | Inspects text and returns an inference of the prevailing sentiment (POSITIVE, NEUTRAL, MIXED, or NEGATIVE). |
| POST | / | Inspects text for syntax and the part of speech of words in the document. For more information, see Syntax in the Comprehend Developer Guide. |
| POST | / | Inspects the input text and returns a sentiment analysis for each entity identified in the text. For more information about targeted sentiment, see Targeted sentiment in the Amazon Comprehend Developer Guide. |
| POST | / | Performs toxicity analysis on the list of text strings that you provide as input. The API response contains a results list that matches the size of the input list. For more information about toxicity detection, see Toxicity detection in the Amazon Comprehend Developer Guide. |
| POST | / | Creates a new custom model that replicates a source custom model that you import. The source model can be in your Amazon Web Services account or another one. If the source model is in another Amazon Web Services account, then it must have a resource-based policy that authorizes you to import it. The source model must be in the same Amazon Web Services Region that you're using when you import. You can't import a model that's in a different Region. |
| POST | / | List the datasets that you have configured in this Region. For more information about datasets, see  Flywheel overview in the Amazon Comprehend Developer Guide. |
| POST | / | Gets a list of the documentation classification jobs that you have submitted. |
| POST | / | Gets a list of summaries of the document classifiers that you have created |
| POST | / | Gets a list of the document classifiers that you have created. |
| POST | / | Gets a list of the dominant language detection jobs that you have submitted. |
| POST | / | Gets a list of all existing endpoints that you've created. For information about endpoints, see Managing endpoints. |
| POST | / | Gets a list of the entity detection jobs that you have submitted. |
| POST | / | Gets a list of summaries for the entity recognizers that you have created. |
| POST | / | Gets a list of the properties of all entity recognizers that you created, including recognizers currently in training. Allows you to filter the list of recognizers based on criteria such as status and submission time. This call returns up to 500 entity recognizers in the list, with a default number of 100 recognizers in the list. The results of this list are not in any particular order. Please get the list and sort locally if needed. |
| POST | / | Gets a list of the events detection jobs that you have submitted. |
| POST | / | Information about the history of a flywheel iteration. For more information about flywheels, see  Flywheel overview in the Amazon Comprehend Developer Guide. |
| POST | / | Gets a list of the flywheels that you have created. |
| POST | / | Get a list of key phrase detection jobs that you have submitted. |
| POST | / | Gets a list of the PII entity detection jobs that you have submitted. |
| POST | / | Gets a list of sentiment detection jobs that you have submitted. |
| POST | / | Lists all tags associated with a given Amazon Comprehend resource. |
| POST | / | Gets a list of targeted sentiment detection jobs that you have submitted. |
| POST | / | Gets a list of the topic detection jobs that you have submitted. |
| POST | / | Attaches a resource-based policy to a custom model. You can use this policy to authorize an entity in another Amazon Web Services account to import the custom model, which replicates it in Amazon Comprehend in their account. |
| POST | / | Starts an asynchronous document classification job using a custom classification model. Use the DescribeDocumentClassificationJob operation to track the progress of the job. |
| POST | / | Starts an asynchronous dominant language detection job for a collection of documents. Use the operation to track the status of a job. |
| POST | / | Starts an asynchronous entity detection job for a collection of documents. Use the operation to track the status of a job. This API can be used for either standard entity detection or custom entity recognition. In order to be used for custom entity recognition, the optional EntityRecognizerArn must be used in order to provide access to the recognizer being used to detect the custom entity. |
| POST | / | Starts an asynchronous event detection job for a collection of documents. |
| POST | / | Start the flywheel iteration.This operation uses any new datasets to train a new model version. For more information about flywheels, see  Flywheel overview in the Amazon Comprehend Developer Guide. |
| POST | / | Starts an asynchronous key phrase detection job for a collection of documents. Use the operation to track the status of a job. |
| POST | / | Starts an asynchronous PII entity detection job for a collection of documents. |
| POST | / | Starts an asynchronous sentiment detection job for a collection of documents. Use the operation to track the status of a job. |
| POST | / | Starts an asynchronous targeted sentiment detection job for a collection of documents. Use the DescribeTargetedSentimentDetectionJob operation to track the status of a job. |
| POST | / | Starts an asynchronous topic detection job. Use the DescribeTopicDetectionJob operation to track the status of a job. |
| POST | / | Stops a dominant language detection job in progress. If the job state is IN_PROGRESS the job is marked for termination and put into the STOP_REQUESTED state. If the job completes before it can be stopped, it is put into the COMPLETED state; otherwise the job is stopped and put into the STOPPED state. If the job is in the COMPLETED or FAILED state when you call the StopDominantLanguageDetectionJob operation, the operation returns a 400 Internal Request Exception.  When a job is stopped, any documents already processed are written to the output location. |
| POST | / | Stops an entities detection job in progress. If the job state is IN_PROGRESS the job is marked for termination and put into the STOP_REQUESTED state. If the job completes before it can be stopped, it is put into the COMPLETED state; otherwise the job is stopped and put into the STOPPED state. If the job is in the COMPLETED or FAILED state when you call the StopDominantLanguageDetectionJob operation, the operation returns a 400 Internal Request Exception.  When a job is stopped, any documents already processed are written to the output location. |
| POST | / | Stops an events detection job in progress. |
| POST | / | Stops a key phrases detection job in progress. If the job state is IN_PROGRESS the job is marked for termination and put into the STOP_REQUESTED state. If the job completes before it can be stopped, it is put into the COMPLETED state; otherwise the job is stopped and put into the STOPPED state. If the job is in the COMPLETED or FAILED state when you call the StopDominantLanguageDetectionJob operation, the operation returns a 400 Internal Request Exception.  When a job is stopped, any documents already processed are written to the output location. |
| POST | / | Stops a PII entities detection job in progress. |
| POST | / | Stops a sentiment detection job in progress. If the job state is IN_PROGRESS, the job is marked for termination and put into the STOP_REQUESTED state. If the job completes before it can be stopped, it is put into the COMPLETED state; otherwise the job is be stopped and put into the STOPPED state. If the job is in the COMPLETED or FAILED state when you call the StopDominantLanguageDetectionJob operation, the operation returns a 400 Internal Request Exception.  When a job is stopped, any documents already processed are written to the output location. |
| POST | / | Stops a targeted sentiment detection job in progress. If the job state is IN_PROGRESS, the job is marked for termination and put into the STOP_REQUESTED state. If the job completes before it can be stopped, it is put into the COMPLETED state; otherwise the job is be stopped and put into the STOPPED state. If the job is in the COMPLETED or FAILED state when you call the StopDominantLanguageDetectionJob operation, the operation returns a 400 Internal Request Exception.  When a job is stopped, any documents already processed are written to the output location. |
| POST | / | Stops a document classifier training job while in progress. If the training job state is TRAINING, the job is marked for termination and put into the STOP_REQUESTED state. If the training job completes before it can be stopped, it is put into the TRAINED; otherwise the training job is stopped and put into the STOPPED state and the service sends back an HTTP 200 response with an empty HTTP body. |
| POST | / | Stops an entity recognizer training job while in progress. If the training job state is TRAINING, the job is marked for termination and put into the STOP_REQUESTED state. If the training job completes before it can be stopped, it is put into the TRAINED; otherwise the training job is stopped and putted into the STOPPED state and the service sends back an HTTP 200 response with an empty HTTP body. |
| POST | / | Associates a specific tag with an Amazon Comprehend resource. A tag is a key-value pair that adds as a metadata to a resource used by Amazon Comprehend. For example, a tag with "Sales" as the key might be added to a resource to indicate its use by the sales department. |
| POST | / | Removes a specific tag associated with an Amazon Comprehend resource. |
| POST | / | Updates information about the specified endpoint. For information about endpoints, see Managing endpoints. |
| POST | / | Update the configuration information for an existing flywheel. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
