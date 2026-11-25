---
name: amazon-lex-model-building-v2
description: "Amazon Lex Model Building V2 API skill. Use when working with Amazon Lex Model Building V2 for bots, exports, policy. Covers 102 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Lex Model Building V2
API version: 2020-08-07

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/customvocabulary/DEFAULT/metadata -- verify access
3. POST /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/customvocabulary/DEFAULT/batchdelete -- create first batchdelete

## Endpoints

102 endpoints across 11 groups. See references/api-spec.lap for full details.

### bots
| Method | Path | Description |
|--------|------|-------------|
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/customvocabulary/DEFAULT/batchcreate | Create a batch of custom vocabulary items for a given bot locale's custom vocabulary. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/customvocabulary/DEFAULT/batchdelete | Delete a batch of custom vocabulary items for a given bot locale's custom vocabulary. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/customvocabulary/DEFAULT/batchupdate | Update a batch of custom vocabulary items for a given bot locale's custom vocabulary. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/ | Builds a bot, its intents, and its slot types into a specific locale. A bot can be built into multiple locales. At runtime the locale is used to choose a specific build of the bot. |
| PUT | /bots/ | Creates an Amazon Lex conversational bot. |
| PUT | /bots/{botId}/botaliases/ | Creates an alias for the specified version of a bot. Use an alias to enable you to change the version of a bot without updating applications that use the bot. For example, you can create an alias called "PROD" that your applications use to call the Amazon Lex bot. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/ | Creates a locale in the bot. The locale contains the intents and slot types that the bot uses in conversations with users in the specified language and locale. You must add a locale to a bot before you can add intents and slot types to the bot. |
| PUT | /bots/{botId}/replicas/ | Action to create a replication of the source bot in the secondary region. |
| PUT | /bots/{botId}/botversions/ | Creates an immutable version of the bot. When you create the first version of a bot, Amazon Lex sets the version number to 1. Subsequent bot versions increase in an increment of 1. The version number will always represent the total number of versions created of the bot, not the current number of versions. If a bot version is deleted, that bot version number will not be reused. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/ | Creates an intent. To define the interaction between the user and your bot, you define one or more intents. For example, for a pizza ordering bot you would create an OrderPizza intent. When you create an intent, you must provide a name. You can optionally provide the following:   Sample utterances. For example, "I want to order a pizza" and "Can I order a pizza." You can't provide utterances for built-in intents.   Information to be gathered. You specify slots for the information that you bot requests from the user. You can specify standard slot types, such as date and time, or custom slot types for your application.   How the intent is fulfilled. You can provide a Lambda function or configure the intent to return the intent information to your client application. If you use a Lambda function, Amazon Lex invokes the function when all of the intent information is available.   A confirmation prompt to send to the user to confirm an intent. For example, "Shall I order your pizza?"   A conclusion statement to send to the user after the intent is fulfilled. For example, "I ordered your pizza."   A follow-up prompt that asks the user for additional activity. For example, "Do you want a drink with your pizza?" |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/slots/ | Creates a slot in an intent. A slot is a variable needed to fulfill an intent. For example, an OrderPizza intent might need slots for size, crust, and number of pizzas. For each slot, you define one or more utterances that Amazon Lex uses to elicit a response from the user. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/slottypes/ | Creates a custom slot type  To create a custom slot type, specify a name for the slot type and a set of enumeration values, the values that a slot of this type can assume. |
| DELETE | /bots/{botId}/ | Deletes all versions of a bot, including the Draft version. To delete a specific version, use the DeleteBotVersion operation. When you delete a bot, all of the resources contained in the bot are also deleted. Deleting a bot removes all locales, intents, slot, and slot types defined for the bot. If a bot has an alias, the DeleteBot operation returns a ResourceInUseException exception. If you want to delete the bot and the alias, set the skipResourceInUseCheck parameter to true. |
| DELETE | /bots/{botId}/botaliases/{botAliasId}/ | Deletes the specified bot alias. |
| DELETE | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/ | Removes a locale from a bot. When you delete a locale, all intents, slots, and slot types defined for the locale are also deleted. |
| DELETE | /bots/{botId}/replicas/{replicaRegion}/ | The action to delete the replicated bot in the secondary region. |
| DELETE | /bots/{botId}/botversions/{botVersion}/ | Deletes a specific version of a bot. To delete all versions of a bot, use the DeleteBot operation. |
| DELETE | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/customvocabulary | Removes a custom vocabulary from the specified locale in the specified bot. |
| DELETE | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/ | Removes the specified intent. Deleting an intent also deletes the slots associated with the intent. |
| DELETE | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/slots/{slotId}/ | Deletes the specified slot from an intent. |
| DELETE | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/slottypes/{slotTypeId}/ | Deletes a slot type from a bot locale. If a slot is using the slot type, Amazon Lex throws a ResourceInUseException exception. To avoid the exception, set the skipResourceInUseCheck parameter to true. |
| DELETE | /bots/{botId}/utterances/ | Deletes stored utterances. Amazon Lex stores the utterances that users send to your bot. Utterances are stored for 15 days for use with the ListAggregatedUtterances operation, and then stored indefinitely for use in improving the ability of your bot to respond to user input.. Use the DeleteUtterances operation to manually delete utterances for a specific session. When you use the DeleteUtterances operation, utterances stored for improving your bot's ability to respond to user input are deleted immediately. Utterances stored for use with the ListAggregatedUtterances operation are deleted after 15 days. |
| GET | /bots/{botId}/ | Provides metadata information about a bot. |
| GET | /bots/{botId}/botaliases/{botAliasId}/ | Get information about a specific bot alias. |
| GET | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/ | Describes the settings that a bot has for a specific locale. |
| GET | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/{botRecommendationId}/ | Provides metadata information about a bot recommendation. This information will enable you to get a description on the request inputs, to download associated transcripts after processing is complete, and to download intents and slot-types generated by the bot recommendation. |
| GET | /bots/{botId}/replicas/{replicaRegion}/ | Monitors the bot replication status through the UI console. |
| GET | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/generations/{generationId} | Returns information about a request to generate a bot through natural language description, made through the StartBotResource API. Use the generatedBotLocaleUrl to retrieve the Amazon S3 object containing the bot locale configuration. You can then modify and import this configuration. |
| GET | /bots/{botId}/botversions/{botVersion}/ | Provides metadata about a version of a bot. |
| GET | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/customvocabulary/DEFAULT/metadata | Provides metadata information about a custom vocabulary. |
| GET | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/ | Returns metadata about an intent. |
| GET | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/slots/{slotId}/ | Gets metadata information about a slot. |
| GET | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/slottypes/{slotTypeId}/ | Gets metadata information about a slot type. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/generate | Generates sample utterances for an intent. |
| POST | /bots/{botId}/aggregatedutterances/ | Provides a list of utterances that users have sent to the bot. Utterances are aggregated by the text of the utterance. For example, all instances where customers used the phrase "I want to order pizza" are aggregated into the same line in the response. You can see both detected utterances and missed utterances. A detected utterance is where the bot properly recognized the utterance and activated the associated intent. A missed utterance was not recognized by the bot and didn't activate an intent. Utterances can be aggregated for a bot alias or for a bot version, but not both at the same time. Utterances statistics are not generated under the following conditions:   The childDirected field was set to true when the bot was created.   You are using slot obfuscation with one or more slots.   You opted out of participating in improving Amazon Lex. |
| POST | /bots/{botId}/replicas/{replicaRegion}/botaliases/ | The action to list the replicated bots created from the source bot alias. |
| POST | /bots/{botId}/botaliases/ | Gets a list of aliases for the specified bot. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/ | Gets a list of locales for the specified bot. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/ | Get a list of bot recommendations that meet the specified criteria. |
| POST | /bots/{botId}/replicas/ | The action to list the replicated bots. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/generations | Lists the generation requests made for a bot locale. |
| POST | /bots/{botId}/replicas/{replicaRegion}/botversions/ | Contains information about all the versions replication statuses applicable for Global Resiliency. |
| POST | /bots/{botId}/botversions/ | Gets information about all of the versions of a bot. The ListBotVersions operation returns a summary of each version of a bot. For example, if a bot has three numbered versions, the ListBotVersions operation returns for summaries, one for each numbered version and one for the DRAFT version. The ListBotVersions operation always returns at least one version, the DRAFT version. |
| POST | /bots/ | Gets a list of available bots. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/customvocabulary/DEFAULT/list | Paginated list of custom vocabulary items for a given bot locale's custom vocabulary. |
| POST | /bots/{botId}/analytics/intentmetrics | Retrieves summary metrics for the intents in your bot. The following fields are required:    metrics – A list of AnalyticsIntentMetric objects. In each object, use the name field to specify the metric to calculate, the statistic field to specify whether to calculate the Sum, Average, or Max number, and the order field to specify whether to sort the results in Ascending or Descending order.    startDateTime and endDateTime – Define a time range for which you want to retrieve results.   Of the optional fields, you can organize the results in the following ways:   Use the filters field to filter the results, the groupBy field to specify categories by which to group the results, and the binBy field to specify time intervals by which to group the results.   Use the maxResults field to limit the number of results to return in a single response and the nextToken field to return the next batch of results if the response does not return the full set of results.   Note that an order field exists in both binBy and metrics. You can specify only one order in a given request. |
| POST | /bots/{botId}/analytics/intentpaths | Retrieves summary statistics for a path of intents that users take over sessions with your bot. The following fields are required:    startDateTime and endDateTime – Define a time range for which you want to retrieve results.    intentPath – Define an order of intents for which you want to retrieve metrics. Separate intents in the path with a forward slash. For example, populate the intentPath field with /BookCar/BookHotel to see details about how many times users invoked the BookCar and BookHotel intents in that order.   Use the optional filters field to filter the results. |
| POST | /bots/{botId}/analytics/intentstagemetrics | Retrieves summary metrics for the stages within intents in your bot. The following fields are required:    metrics – A list of AnalyticsIntentStageMetric objects. In each object, use the name field to specify the metric to calculate, the statistic field to specify whether to calculate the Sum, Average, or Max number, and the order field to specify whether to sort the results in Ascending or Descending order.    startDateTime and endDateTime – Define a time range for which you want to retrieve results.   Of the optional fields, you can organize the results in the following ways:   Use the filters field to filter the results, the groupBy field to specify categories by which to group the results, and the binBy field to specify time intervals by which to group the results.   Use the maxResults field to limit the number of results to return in a single response and the nextToken field to return the next batch of results if the response does not return the full set of results.   Note that an order field exists in both binBy and metrics. You can only specify one order in a given request. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/ | Get a list of intents that meet the specified criteria. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/{botRecommendationId}/intents | Gets a list of recommended intents provided by the bot recommendation that you can use in your bot. Intents in the response are ordered by relevance. |
| POST | /bots/{botId}/analytics/sessions | Retrieves a list of metadata for individual user sessions with your bot. The startDateTime and endDateTime fields are required. These fields define a time range for which you want to retrieve results. Of the optional fields, you can organize the results in the following ways:   Use the filters field to filter the results and the sortBy field to specify the values by which to sort the results.   Use the maxResults field to limit the number of results to return in a single response and the nextToken field to return the next batch of results if the response does not return the full set of results. |
| POST | /bots/{botId}/analytics/sessionmetrics | Retrieves summary metrics for the user sessions with your bot. The following fields are required:    metrics – A list of AnalyticsSessionMetric objects. In each object, use the name field to specify the metric to calculate, the statistic field to specify whether to calculate the Sum, Average, or Max number, and the order field to specify whether to sort the results in Ascending or Descending order.    startDateTime and endDateTime – Define a time range for which you want to retrieve results.   Of the optional fields, you can organize the results in the following ways:   Use the filters field to filter the results, the groupBy field to specify categories by which to group the results, and the binBy field to specify time intervals by which to group the results.   Use the maxResults field to limit the number of results to return in a single response and the nextToken field to return the next batch of results if the response does not return the full set of results.   Note that an order field exists in both binBy and metrics. Currently, you can specify it in either field, but not in both. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/slottypes/ | Gets a list of slot types that match the specified criteria. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/slots/ | Gets a list of slots that match the specified criteria. |
| POST | /bots/{botId}/analytics/utterances | To use this API operation, your IAM role must have permissions to perform the ListAggregatedUtterances operation, which provides access to utterance-related analytics. See Viewing utterance statistics for the IAM policy to apply to the IAM role.  Retrieves a list of metadata for individual user utterances to your bot. The following fields are required:    startDateTime and endDateTime – Define a time range for which you want to retrieve results.   Of the optional fields, you can organize the results in the following ways:   Use the filters field to filter the results and the sortBy field to specify the values by which to sort the results.   Use the maxResults field to limit the number of results to return in a single response and the nextToken field to return the next batch of results if the response does not return the full set of results. |
| POST | /bots/{botId}/analytics/utterancemetrics | To use this API operation, your IAM role must have permissions to perform the ListAggregatedUtterances operation, which provides access to utterance-related analytics. See Viewing utterance statistics for the IAM policy to apply to the IAM role.  Retrieves summary metrics for the utterances in your bot. The following fields are required:    metrics – A list of AnalyticsUtteranceMetric objects. In each object, use the name field to specify the metric to calculate, the statistic field to specify whether to calculate the Sum, Average, or Max number, and the order field to specify whether to sort the results in Ascending or Descending order.    startDateTime and endDateTime – Define a time range for which you want to retrieve results.   Of the optional fields, you can organize the results in the following ways:   Use the filters field to filter the results, the groupBy field to specify categories by which to group the results, and the binBy field to specify time intervals by which to group the results.   Use the maxResults field to limit the number of results to return in a single response and the nextToken field to return the next batch of results if the response does not return the full set of results.   Note that an order field exists in both binBy and metrics. Currently, you can specify it in either field, but not in both. |
| POST | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/{botRecommendationId}/associatedtranscripts | Search for associated transcripts that meet the specified criteria. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/ | Use this to provide your transcript data, and to start the bot recommendation process. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/startgeneration | Starts a request for the descriptive bot builder to generate a bot locale configuration based on the prompt you provide it. After you make this call, use the DescribeBotResourceGeneration operation to check on the status of the generation and for the generatedBotLocaleUrl when the generation is complete. Use that value to retrieve the Amazon S3 object containing the bot locale configuration. You can then modify and import this configuration. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/{botRecommendationId}/stopbotrecommendation | Stop an already running Bot Recommendation request. |
| PUT | /bots/{botId}/ | Updates the configuration of an existing bot. |
| PUT | /bots/{botId}/botaliases/{botAliasId}/ | Updates the configuration of an existing bot alias. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/ | Updates the settings that a bot has for a specific locale. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/{botRecommendationId}/ | Updates an existing bot recommendation request. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/ | Updates the settings for an intent. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/slots/{slotId}/ | Updates the settings for a slot. |
| PUT | /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/slottypes/{slotTypeId}/ | Updates the configuration of an existing slot type. |

### exports
| Method | Path | Description |
|--------|------|-------------|
| PUT | /exports/ | Creates a zip archive containing the contents of a bot or a bot locale. The archive contains a directory structure that contains JSON files that define the bot. You can create an archive that contains the complete definition of a bot, or you can specify that the archive contain only the definition of a single bot locale. For more information about exporting bots, and about the structure of the export archive, see  Importing and exporting bots |
| DELETE | /exports/{exportId}/ | Removes a previous export and the associated files stored in an S3 bucket. |
| GET | /exports/{exportId}/ | Gets information about a specific export. |
| POST | /exports/ | Lists the exports for a bot, bot locale, or custom vocabulary. Exports are kept in the list for 7 days. |
| PUT | /exports/{exportId}/ | Updates the password used to protect an export zip archive. The password is not required. If you don't supply a password, Amazon Lex generates a zip file that is not protected by a password. This is the archive that is available at the pre-signed S3 URL provided by the DescribeExport operation. |

### policy
| Method | Path | Description |
|--------|------|-------------|
| POST | /policy/{resourceArn}/ | Creates a new resource policy with the specified policy statements. |
| POST | /policy/{resourceArn}/statements/ | Adds a new resource policy statement to a bot or bot alias. If a resource policy exists, the statement is added to the current resource policy. If a policy doesn't exist, a new policy is created. You can't create a resource policy statement that allows cross-account access. You need to add the CreateResourcePolicy or UpdateResourcePolicy action to the bot role in order to call the API. |
| DELETE | /policy/{resourceArn}/ | Removes an existing policy from a bot or bot alias. If the resource doesn't have a policy attached, Amazon Lex returns an exception. |
| DELETE | /policy/{resourceArn}/statements/{statementId}/ | Deletes a policy statement from a resource policy. If you delete the last statement from a policy, the policy is deleted. If you specify a statement ID that doesn't exist in the policy, or if the bot or bot alias doesn't have a policy attached, Amazon Lex returns an exception. You need to add the DeleteResourcePolicy or UpdateResourcePolicy action to the bot role in order to call the API. |
| GET | /policy/{resourceArn}/ | Gets the resource policy and policy revision for a bot or bot alias. |
| PUT | /policy/{resourceArn}/ | Replaces the existing resource policy for a bot or bot alias with a new one. If the policy doesn't exist, Amazon Lex returns an exception. |

### testsets
| Method | Path | Description |
|--------|------|-------------|
| POST | /testsets/{testSetId}/testsetdiscrepancy | Create a report that describes the differences between the bot and the test set. |
| DELETE | /testsets/{testSetId} | The action to delete the selected test set. |
| GET | /testsets/{testSetId} | Gets metadata information about the test set. |
| POST | /testsets/{testSetId}/records | The list of test set records. |
| POST | /testsets | The list of the test sets |
| POST | /testsets/{testSetId}/testexecutions | The action to start test set execution. |
| PUT | /testsets/{testSetId} | The action to update the test set. |

### createuploadurl
| Method | Path | Description |
|--------|------|-------------|
| POST | /createuploadurl/ | Gets a pre-signed S3 write URL that you use to upload the zip archive when importing a bot or a bot locale. |

### imports
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /imports/{importId}/ | Removes a previous import and the associated file stored in an S3 bucket. |
| GET | /imports/{importId}/ | Gets information about a specific import. |
| POST | /imports/ | Lists the imports for a bot, bot locale, or custom vocabulary. Imports are kept in the list for 7 days. |
| PUT | /imports/ | Starts importing a bot, bot locale, or custom vocabulary from a zip archive that you uploaded to an S3 bucket. |

### testexecutions
| Method | Path | Description |
|--------|------|-------------|
| GET | /testexecutions/{testExecutionId} | Gets metadata information about the test execution. |
| GET | /testexecutions/{testExecutionId}/artifacturl | The pre-signed Amazon S3 URL to download the test execution result artifacts. |
| POST | /testexecutions/{testExecutionId}/results | Gets a list of test execution result items. |
| POST | /testexecutions | The list of test set executions. |

### testsetdiscrepancy
| Method | Path | Description |
|--------|------|-------------|
| GET | /testsetdiscrepancy/{testSetDiscrepancyReportId} | Gets metadata information about the test set discrepancy report. |

### testsetgenerations
| Method | Path | Description |
|--------|------|-------------|
| GET | /testsetgenerations/{testSetGenerationId} | Gets metadata information about the test set generation. |
| PUT | /testsetgenerations | The action to start the generation of test set. |

### builtins
| Method | Path | Description |
|--------|------|-------------|
| POST | /builtins/locales/{localeId}/intents/ | Gets a list of built-in intents provided by Amazon Lex that you can use in your bot.  To use a built-in intent as a the base for your own intent, include the built-in intent signature in the parentIntentSignature parameter when you call the CreateIntent operation. For more information, see CreateIntent. |
| POST | /builtins/locales/{localeId}/slottypes/ | Gets a list of built-in slot types that meet the specified criteria. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceARN} | Gets a list of tags associated with a resource. Only bots, bot aliases, and bot channels can have tags associated with them. |
| POST | /tags/{resourceARN} | Adds the specified tags to the specified resource. If a tag key already exists, the existing value is replaced with the new value. |
| DELETE | /tags/{resourceARN} | Removes tags from a bot, bot alias, or bot channel. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a batchdelete?" -> POST /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/customvocabulary/DEFAULT/batchdelete
- "Create a statement?" -> POST /policy/{resourceArn}/statements/
- "Create a testsetdiscrepancy?" -> POST /testsets/{testSetId}/testsetdiscrepancy
- "Create a createuploadurl?" -> POST /createuploadurl/
- "Delete a bot?" -> DELETE /bots/{botId}/
- "Delete a botaliase?" -> DELETE /bots/{botId}/botaliases/{botAliasId}/
- "Delete a botlocale?" -> DELETE /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/
- "Delete a replica?" -> DELETE /bots/{botId}/replicas/{replicaRegion}/
- "Delete a botversion?" -> DELETE /bots/{botId}/botversions/{botVersion}/
- "Delete a export?" -> DELETE /exports/{exportId}/
- "Delete a import?" -> DELETE /imports/{importId}/
- "Delete a intent?" -> DELETE /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/
- "Delete a policy?" -> DELETE /policy/{resourceArn}/
- "Delete a statement?" -> DELETE /policy/{resourceArn}/statements/{statementId}/
- "Delete a slot?" -> DELETE /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/slots/{slotId}/
- "Delete a slottype?" -> DELETE /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/slottypes/{slotTypeId}/
- "Delete a testset?" -> DELETE /testsets/{testSetId}
- "Get bot details?" -> GET /bots/{botId}/
- "Get botaliase details?" -> GET /bots/{botId}/botaliases/{botAliasId}/
- "Get botlocale details?" -> GET /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/
- "Get botrecommendation details?" -> GET /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/{botRecommendationId}/
- "Get replica details?" -> GET /bots/{botId}/replicas/{replicaRegion}/
- "Get generation details?" -> GET /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/generations/{generationId}
- "Get botversion details?" -> GET /bots/{botId}/botversions/{botVersion}/
- "List all metadata?" -> GET /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/customvocabulary/DEFAULT/metadata
- "Get export details?" -> GET /exports/{exportId}/
- "Get import details?" -> GET /imports/{importId}/
- "Get intent details?" -> GET /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/
- "Get policy details?" -> GET /policy/{resourceArn}/
- "Get slot details?" -> GET /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/slots/{slotId}/
- "Get slottype details?" -> GET /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/slottypes/{slotTypeId}/
- "Get testexecution details?" -> GET /testexecutions/{testExecutionId}
- "Get testset details?" -> GET /testsets/{testSetId}
- "Get testsetdiscrepancy details?" -> GET /testsetdiscrepancy/{testSetDiscrepancyReportId}
- "Get testsetgeneration details?" -> GET /testsetgenerations/{testSetGenerationId}
- "Create a generate?" -> POST /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/generate
- "List all artifacturl?" -> GET /testexecutions/{testExecutionId}/artifacturl
- "Create a aggregatedutterance?" -> POST /bots/{botId}/aggregatedutterances/
- "Create a botaliase?" -> POST /bots/{botId}/replicas/{replicaRegion}/botaliases/
- "Create a botaliase?" -> POST /bots/{botId}/botaliases/
- "Create a botlocale?" -> POST /bots/{botId}/botversions/{botVersion}/botlocales/
- "Create a botrecommendation?" -> POST /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/
- "Create a replica?" -> POST /bots/{botId}/replicas/
- "Create a generation?" -> POST /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/generations
- "Create a botversion?" -> POST /bots/{botId}/replicas/{replicaRegion}/botversions/
- "Create a botversion?" -> POST /bots/{botId}/botversions/
- "Create a bot?" -> POST /bots/
- "Create a intent?" -> POST /builtins/locales/{localeId}/intents/
- "Create a slottype?" -> POST /builtins/locales/{localeId}/slottypes/
- "Create a list?" -> POST /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/customvocabulary/DEFAULT/list
- "Create a export?" -> POST /exports/
- "Create a import?" -> POST /imports/
- "Create a intentmetric?" -> POST /bots/{botId}/analytics/intentmetrics
- "Create a intentpath?" -> POST /bots/{botId}/analytics/intentpaths
- "Create a intentstagemetric?" -> POST /bots/{botId}/analytics/intentstagemetrics
- "Create a intent?" -> POST /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/
- "Create a intent?" -> POST /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/{botRecommendationId}/intents
- "Create a session?" -> POST /bots/{botId}/analytics/sessions
- "Create a sessionmetric?" -> POST /bots/{botId}/analytics/sessionmetrics
- "Create a slottype?" -> POST /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/slottypes/
- "Create a slot?" -> POST /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/slots/
- "Get tag details?" -> GET /tags/{resourceARN}
- "Create a result?" -> POST /testexecutions/{testExecutionId}/results
- "Create a testexecution?" -> POST /testexecutions
- "Create a record?" -> POST /testsets/{testSetId}/records
- "Create a testset?" -> POST /testsets
- "Create a utterance?" -> POST /bots/{botId}/analytics/utterances
- "Create a utterancemetric?" -> POST /bots/{botId}/analytics/utterancemetrics
- "Create a associatedtranscript?" -> POST /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/{botRecommendationId}/associatedtranscripts
- "Create a testexecution?" -> POST /testsets/{testSetId}/testexecutions
- "Delete a tag?" -> DELETE /tags/{resourceARN}
- "Update a bot?" -> PUT /bots/{botId}/
- "Update a botaliase?" -> PUT /bots/{botId}/botaliases/{botAliasId}/
- "Update a botlocale?" -> PUT /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/
- "Update a botrecommendation?" -> PUT /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/botrecommendations/{botRecommendationId}/
- "Update a export?" -> PUT /exports/{exportId}/
- "Update a intent?" -> PUT /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/
- "Update a policy?" -> PUT /policy/{resourceArn}/
- "Update a slot?" -> PUT /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/intents/{intentId}/slots/{slotId}/
- "Update a slottype?" -> PUT /bots/{botId}/botversions/{botVersion}/botlocales/{localeId}/slottypes/{slotTypeId}/
- "Update a testset?" -> PUT /testsets/{testSetId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
