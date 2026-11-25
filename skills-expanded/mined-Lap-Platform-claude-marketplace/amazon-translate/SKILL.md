---
name: amazon-translate
description: "Amazon Translate API skill. Use when working with Amazon Translate for root. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Translate
API version: 2017-07-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

19 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates a parallel data resource in Amazon Translate by importing an input file from Amazon S3. Parallel data files contain examples that show how you want segments of text to be translated. By adding parallel data, you can influence the style, tone, and word choice in your translation output. |
| POST | / | Deletes a parallel data resource in Amazon Translate. |
| POST | / | A synchronous action that deletes a custom terminology. |
| POST | / | Gets the properties associated with an asynchronous batch translation job including name, ID, status, source and target languages, input/output S3 buckets, and so on. |
| POST | / | Provides information about a parallel data resource. |
| POST | / | Retrieves a custom terminology. |
| POST | / | Creates or updates a custom terminology, depending on whether one already exists for the given terminology name. Importing a terminology with the same name as an existing one will merge the terminologies based on the chosen merge strategy. The only supported merge strategy is OVERWRITE, where the imported terminology overwrites the existing terminology of the same name. If you import a terminology that overwrites an existing one, the new terminology takes up to 10 minutes to fully propagate. After that, translations have access to the new terminology. |
| POST | / | Provides a list of languages (RFC-5646 codes and names) that Amazon Translate supports. |
| POST | / | Provides a list of your parallel data resources in Amazon Translate. |
| POST | / | Lists all tags associated with a given Amazon Translate resource. For more information, see  Tagging your resources. |
| POST | / | Provides a list of custom terminologies associated with your account. |
| POST | / | Gets a list of the batch translation jobs that you have submitted. |
| POST | / | Starts an asynchronous batch translation job. Use batch translation jobs to translate large volumes of text across multiple documents at once. For batch translation, you can input documents with different source languages (specify auto as the source language). You can specify one or more target languages. Batch translation translates each input document into each of the target languages. For more information, see Asynchronous batch processing. Batch translation jobs can be described with the DescribeTextTranslationJob operation, listed with the ListTextTranslationJobs operation, and stopped with the StopTextTranslationJob operation. |
| POST | / | Stops an asynchronous batch translation job that is in progress. If the job's state is IN_PROGRESS, the job will be marked for termination and put into the STOP_REQUESTED state. If the job completes before it can be stopped, it is put into the COMPLETED state. Otherwise, the job is put into the STOPPED state. Asynchronous batch translation jobs are started with the StartTextTranslationJob operation. You can use the DescribeTextTranslationJob or ListTextTranslationJobs operations to get a batch translation job's JobId. |
| POST | / | Associates a specific tag with a resource. A tag is a key-value pair that adds as a metadata to a resource. For more information, see  Tagging your resources. |
| POST | / | Translates the input document from the source language to the target language. This synchronous operation supports text, HTML, or Word documents as the input document. TranslateDocument supports translations from English to any supported language, and from any supported language to English. Therefore, specify either the source language code or the target language code as “en” (English).   If you set the Formality parameter, the request will fail if the target language does not support formality. For a list of target languages that support formality, see Setting formality. |
| POST | / | Translates input text from the source language to the target language. For a list of available languages and language codes, see Supported languages. |
| POST | / | Removes a specific tag associated with an Amazon Translate resource. For more information, see  Tagging your resources. |
| POST | / | Updates a previously created parallel data resource by importing a new input file from Amazon S3. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
