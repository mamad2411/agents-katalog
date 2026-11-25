---
name: luis-authoring-client
description: "LUIS Authoring Client API skill. Use when working with LUIS Authoring Client for apps, azureaccounts, package. Covers 168 endpoints."
version: 1.0.0
generator: lapsh
---

# LUIS Authoring Client
API version: 3.0-preview

## Auth
ApiKey Ocp-Apim-Subscription-Key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /apps/ -- verify access
3. POST /apps/{appId}/versions/{versionId}/phraselists -- create first phraselists

## Endpoints

168 endpoints across 3 groups. See references/api-spec.lap for full details.

### apps
| Method | Path | Description |
|--------|------|-------------|
| POST | /apps/{appId}/versions/{versionId}/phraselists | Creates a new phraselist feature in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/phraselists | Gets all the phraselist features in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/features | Gets all the extraction phraselist and pattern features in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/phraselists/{phraselistId} | Gets phraselist feature info in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/phraselists/{phraselistId} | Updates the phrases, the state and the name of the phraselist feature in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/phraselists/{phraselistId} | Deletes a phraselist feature from a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/example | Adds a labeled example utterance in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/examples | Adds a batch of labeled example utterances to a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/examples | Returns example utterances to be reviewed from a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/examples/{exampleId} | Deletes the labeled example utterances with the specified ID from a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/intents | Adds an intent to a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/intents | Gets information about the intent models in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/entities | Adds an entity extractor to a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/entities | Gets information about all the simple entity models in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/hierarchicalentities | Gets information about all the hierarchical entity models in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/compositeentities | Gets information about all the composite entity models in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/closedlists | Gets information about all the list entity models in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/closedlists | Adds a list entity model to a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/prebuilts | Adds a list of prebuilt entities to a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/prebuilts | Gets information about all the prebuilt entities in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/listprebuilts | Gets all the available prebuilt entities in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/models | Gets information about all the intent and entity models in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/models/{modelId}/examples | Gets the example utterances for the given intent or entity model in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/intents/{intentId} | Gets information about the intent model in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/intents/{intentId} | Updates the name of an intent in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/intents/{intentId} | Deletes an intent from a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/entities/{entityId} | Gets information about an entity model in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/entities/{entityId} | Deletes an entity or a child from a version of the application. |
| PATCH | /apps/{appId}/versions/{versionId}/entities/{entityId} | Updates the name of an entity extractor or the name and instanceOf model of a child entity extractor. |
| POST | /apps/{appId}/versions/{versionId}/intents/{intentId}/features | Adds a new feature relation to be used by the intent in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/intents/{intentId}/features | Gets the information of the features used by the intent in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/intents/{intentId}/features | Updates the information of the features used by the intent in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/intents/{intentId}/features | Deletes a relation from the feature relations used by the intent in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/entities/{entityId}/features | Adds a new feature relation to be used by the entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/entities/{entityId}/features | Gets the information of the features used by the entity in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/entities/{entityId}/features | Updates the information of the features used by the entity in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/entities/{entityId}/features | Deletes a relation from the feature relations used by the entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId} | Gets information about a hierarchical entity in a version of the application. |
| PATCH | /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId} | Updates the name of a hierarchical entity model in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId} | Deletes a hierarchical entity from a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId} | Gets information about a composite entity in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId} | Updates a composite entity in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId} | Deletes a composite entity from a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/closedlists/{clEntityId} | Gets information about a list entity in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/closedlists/{clEntityId} | Updates the list entity in a version of the application. |
| PATCH | /apps/{appId}/versions/{versionId}/closedlists/{clEntityId} | Adds a batch of sublists to an existing list entity in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/closedlists/{clEntityId} | Deletes a list entity model from a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/prebuilts/{prebuiltId} | Gets information about a prebuilt entity model in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/prebuilts/{prebuiltId} | Deletes a prebuilt entity extractor from a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/closedlists/{clEntityId}/sublists/{subListId} | Deletes a sublist of a specific list entity model from a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/closedlists/{clEntityId}/sublists/{subListId} | Updates one of the list entity's sublists in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/intents/{intentId}/suggest | Suggests example utterances that would improve the accuracy of the intent model in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/entities/{entityId}/suggest | Get suggested example utterances that would improve the accuracy of the entity model in a version of the application. |
| POST | /apps/ | Creates a new LUIS app. |
| GET | /apps/ | Lists all of the user's applications. |
| POST | /apps/import | Imports an application to LUIS, the application's structure is included in the request body. |
| GET | /apps/assistants | Gets the endpoint URLs for the prebuilt Cortana applications. |
| GET | /apps/domains | Gets the available application domains. |
| GET | /apps/usagescenarios | Gets the application available usage scenarios. |
| GET | /apps/cultures | Gets a list of supported cultures. Cultures are equivalent to the written language and locale. For example,"en-us" represents the U.S. variation of English. |
| GET | /apps/{appId}/querylogs | Gets the logs of the past month's endpoint queries for the application. |
| GET | /apps/{appId} | Gets the application info. |
| PUT | /apps/{appId} | Updates the name or description of the application. |
| DELETE | /apps/{appId} | Deletes an application. |
| POST | /apps/{appId}/versions/{versionId}/clone | Creates a new version from the selected version. |
| POST | /apps/{appId}/publish | Publishes a specific version of the application. |
| GET | /apps/{appId}/versions | Gets a list of versions for this application ID. |
| GET | /apps/{appId}/versions/{versionId}/ | Gets the version information such as date created, last modified date, endpoint URL, count of intents and entities, training and publishing status. |
| PUT | /apps/{appId}/versions/{versionId}/ | Updates the name or description of the application version. |
| DELETE | /apps/{appId}/versions/{versionId}/ | Deletes an application version. |
| GET | /apps/{appId}/versions/{versionId}/export | Exports a LUIS application to JSON format. |
| POST | /apps/{appId}/versions/{versionId}/train | Sends a training request for a version of a specified LUIS app. This POST request initiates a request asynchronously. To determine whether the training request is successful, submit a GET request to get training status. Note: The application version is not fully trained unless all the models (intents and entities) are trained successfully or are up to date. To verify training success, get the training status at least once after training is complete. |
| GET | /apps/{appId}/versions/{versionId}/train | Gets the training status of all models (intents and entities) for the specified LUIS app. You must call the train API to train the LUIS app before you call this API to get training status. "appID" specifies the LUIS app ID. "versionId" specifies the version number of the LUIS app. For example, "0.1". |
| POST | /apps/{appId}/versions/import | Imports a new version into a LUIS application. |
| GET | /apps/{appId}/settings | Get the application settings including 'UseAllTrainingData'. |
| PUT | /apps/{appId}/settings | Updates the application settings including 'UseAllTrainingData'. |
| GET | /apps/{appId}/publishsettings | Get the application publish settings including 'UseAllTrainingData'. |
| PUT | /apps/{appId}/publishsettings | Updates the application publish settings including 'UseAllTrainingData'. |
| DELETE | /apps/{appId}/versions/{versionId}/suggest | Deleted an unlabelled utterance in a version of the application. |
| GET | /apps/{appId}/endpoints | Returns the available endpoint deployment regions and URLs. |
| POST | /apps/{appId}/versions/{versionId}/closedlists/{clEntityId}/sublists | Adds a sublist to an existing list entity in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/customprebuiltdomains | Adds a customizable prebuilt domain along with all of its intent and entity models in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/customprebuiltintents | Adds a customizable prebuilt intent model to a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/customprebuiltintents | Gets information about customizable prebuilt intents added to a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/customprebuiltentities | Adds a prebuilt entity model to a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/customprebuiltentities | Gets all prebuilt entities used in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/customprebuiltmodels | Gets all prebuilt intent and entity model information used in a version of this application. |
| DELETE | /apps/{appId}/versions/{versionId}/customprebuiltdomains/{domainName} | Deletes a prebuilt domain's models in a version of the application. |
| GET | /apps/customprebuiltdomains | Gets all the available custom prebuilt domains for all cultures. |
| POST | /apps/customprebuiltdomains | Adds a prebuilt domain along with its intent and entity models as a new application. |
| GET | /apps/customprebuiltdomains/{culture} | Gets all the available prebuilt domains for a specific culture. |
| POST | /apps/{appId}/versions/{versionId}/entities/{entityId}/children | Creates a single child in an existing entity model hierarchy in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/children/{hChildId} | Gets information about the child's model contained in an hierarchical entity child model in a version of the application. |
| PATCH | /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/children/{hChildId} | Renames a single child in an existing hierarchical entity model in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/children/{hChildId} | Deletes a hierarchical entity extractor child in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/children | Creates a single child in an existing composite entity model in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/children/{cChildId} | Deletes a composite entity extractor child from a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/regexentities | Gets information about the regular expression entity models in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/regexentities | Adds a regular expression entity model to a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/patternanyentities | Get information about the Pattern.Any entity models in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/patternanyentities | Adds a pattern.any entity extractor to a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/entities/{entityId}/roles | Get all roles for an entity in a version of the application |
| POST | /apps/{appId}/versions/{versionId}/entities/{entityId}/roles | Create an entity role in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/prebuilts/{entityId}/roles | Get a prebuilt entity's roles in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/prebuilts/{entityId}/roles | Create a role for a prebuilt entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/closedlists/{entityId}/roles | Get all roles for a list entity in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/closedlists/{entityId}/roles | Create a role for a list entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/regexentities/{entityId}/roles | Get all roles for a regular expression entity in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/regexentities/{entityId}/roles | Create a role for an regular expression entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/roles | Get all roles for a composite entity in a version of the application |
| POST | /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/roles | Create a role for a composite entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/roles | Get all roles for a Pattern.any entity in a version of the application |
| POST | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/roles | Create a role for an Pattern.any entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/roles | Get all roles for a hierarchical entity in a version of the application |
| POST | /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/roles | Create a role for an hierarchical entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/customprebuiltentities/{entityId}/roles | Get all roles for a prebuilt entity in a version of the application |
| POST | /apps/{appId}/versions/{versionId}/customprebuiltentities/{entityId}/roles | Create a role for a prebuilt entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/explicitlist | Get the explicit (exception) list of the pattern.any entity in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/explicitlist | Add a new exception to the explicit list for the Pattern.Any entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/regexentities/{regexEntityId} | Gets information about a regular expression entity in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/regexentities/{regexEntityId} | Updates the regular expression entity in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/regexentities/{regexEntityId} | Deletes a regular expression entity from a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId} | Gets information about the Pattern.Any model in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId} | Updates the name and explicit (exception) list of a Pattern.Any entity model in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId} | Deletes a Pattern.Any entity extractor from a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/entities/{entityId}/roles/{roleId} | Get one role for a given entity in a version of the application |
| PUT | /apps/{appId}/versions/{versionId}/entities/{entityId}/roles/{roleId} | Update a role for a given entity in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/entities/{entityId}/roles/{roleId} | Delete an entity role in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/prebuilts/{entityId}/roles/{roleId} | Get one role for a given prebuilt entity in a version of the application |
| PUT | /apps/{appId}/versions/{versionId}/prebuilts/{entityId}/roles/{roleId} | Update a role for a given prebuilt entity in a version of the application |
| DELETE | /apps/{appId}/versions/{versionId}/prebuilts/{entityId}/roles/{roleId} | Delete a role in a prebuilt entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/closedlists/{entityId}/roles/{roleId} | Get one role for a given list entity in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/closedlists/{entityId}/roles/{roleId} | Update a role for a given list entity in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/closedlists/{entityId}/roles/{roleId} | Delete a role for a given list entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/regexentities/{entityId}/roles/{roleId} | Get one role for a given regular expression entity in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/regexentities/{entityId}/roles/{roleId} | Update a role for a given regular expression entity in a version of the application |
| DELETE | /apps/{appId}/versions/{versionId}/regexentities/{entityId}/roles/{roleId} | Delete a role for a given regular expression in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/roles/{roleId} | Get one role for a given composite entity in a version of the application |
| PUT | /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/roles/{roleId} | Update a role for a given composite entity in a version of the application |
| DELETE | /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/roles/{roleId} | Delete a role for a given composite entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/roles/{roleId} | Get one role for a given Pattern.any entity in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/roles/{roleId} | Update a role for a given Pattern.any entity in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/roles/{roleId} | Delete a role for a given Pattern.any entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/roles/{roleId} | Get one role for a given hierarchical entity in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/roles/{roleId} | Update a role for a given hierarchical entity in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/roles/{roleId} | Delete a role for a given hierarchical role in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/customprebuiltentities/{entityId}/roles/{roleId} | Get one role for a given prebuilt entity in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/customprebuiltentities/{entityId}/roles/{roleId} | Update a role for a given prebuilt entity in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/customprebuiltentities/{entityId}/roles/{roleId} | Delete a role for a given prebuilt entity in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/explicitlist/{itemId} | Get the explicit (exception) list of the pattern.any entity in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/explicitlist/{itemId} | Updates an explicit (exception) list item for a Pattern.Any entity in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/explicitlist/{itemId} | Delete an item from the explicit (exception) list for a Pattern.any entity in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/patternrule | Adds a pattern to a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/patternrules | Gets patterns in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/patternrules | Updates patterns in a version of the application. |
| POST | /apps/{appId}/versions/{versionId}/patternrules | Adds a batch of patterns in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/patternrules | Deletes a list of patterns in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/patternrules/{patternId} | Updates a pattern in a version of the application. |
| DELETE | /apps/{appId}/versions/{versionId}/patternrules/{patternId} | Deletes the pattern with the specified ID from a version of the application.. |
| GET | /apps/{appId}/versions/{versionId}/intents/{intentId}/patternrules | Returns patterns for the specific intent in a version of the application. |
| GET | /apps/{appId}/versions/{versionId}/settings | Gets the settings in a version of the application. |
| PUT | /apps/{appId}/versions/{versionId}/settings | Updates the settings in a version of the application. |
| POST | /apps/{appId}/azureaccounts | apps - Assign a LUIS Azure account to an application |
| GET | /apps/{appId}/azureaccounts | apps - Get LUIS Azure accounts assigned to the application |
| DELETE | /apps/{appId}/azureaccounts | apps - Removes an assigned LUIS Azure account from an application |

### azureaccounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /azureaccounts | user - Get LUIS Azure accounts |

### package
| Method | Path | Description |
|--------|------|-------------|
| GET | /package/{appId}/slot/{slotName}/gzip | package - Gets published LUIS application package in binary stream GZip format |
| GET | /package/{appId}/versions/{versionId}/gzip | package - Gets trained LUIS application package in binary stream GZip format |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a phraselist?" -> POST /apps/{appId}/versions/{versionId}/phraselists
- "List all phraselists?" -> GET /apps/{appId}/versions/{versionId}/phraselists
- "List all features?" -> GET /apps/{appId}/versions/{versionId}/features
- "Get phraselist details?" -> GET /apps/{appId}/versions/{versionId}/phraselists/{phraselistId}
- "Update a phraselist?" -> PUT /apps/{appId}/versions/{versionId}/phraselists/{phraselistId}
- "Delete a phraselist?" -> DELETE /apps/{appId}/versions/{versionId}/phraselists/{phraselistId}
- "Create a example?" -> POST /apps/{appId}/versions/{versionId}/example
- "Create a example?" -> POST /apps/{appId}/versions/{versionId}/examples
- "List all examples?" -> GET /apps/{appId}/versions/{versionId}/examples
- "Delete a example?" -> DELETE /apps/{appId}/versions/{versionId}/examples/{exampleId}
- "Create a intent?" -> POST /apps/{appId}/versions/{versionId}/intents
- "List all intents?" -> GET /apps/{appId}/versions/{versionId}/intents
- "Create a entity?" -> POST /apps/{appId}/versions/{versionId}/entities
- "List all entities?" -> GET /apps/{appId}/versions/{versionId}/entities
- "List all hierarchicalentities?" -> GET /apps/{appId}/versions/{versionId}/hierarchicalentities
- "List all compositeentities?" -> GET /apps/{appId}/versions/{versionId}/compositeentities
- "List all closedlists?" -> GET /apps/{appId}/versions/{versionId}/closedlists
- "Create a closedlist?" -> POST /apps/{appId}/versions/{versionId}/closedlists
- "Create a prebuilt?" -> POST /apps/{appId}/versions/{versionId}/prebuilts
- "List all prebuilts?" -> GET /apps/{appId}/versions/{versionId}/prebuilts
- "List all listprebuilts?" -> GET /apps/{appId}/versions/{versionId}/listprebuilts
- "List all models?" -> GET /apps/{appId}/versions/{versionId}/models
- "List all examples?" -> GET /apps/{appId}/versions/{versionId}/models/{modelId}/examples
- "Get intent details?" -> GET /apps/{appId}/versions/{versionId}/intents/{intentId}
- "Update a intent?" -> PUT /apps/{appId}/versions/{versionId}/intents/{intentId}
- "Delete a intent?" -> DELETE /apps/{appId}/versions/{versionId}/intents/{intentId}
- "Get entity details?" -> GET /apps/{appId}/versions/{versionId}/entities/{entityId}
- "Delete a entity?" -> DELETE /apps/{appId}/versions/{versionId}/entities/{entityId}
- "Partially update a entity?" -> PATCH /apps/{appId}/versions/{versionId}/entities/{entityId}
- "Create a feature?" -> POST /apps/{appId}/versions/{versionId}/intents/{intentId}/features
- "List all features?" -> GET /apps/{appId}/versions/{versionId}/intents/{intentId}/features
- "Create a feature?" -> POST /apps/{appId}/versions/{versionId}/entities/{entityId}/features
- "List all features?" -> GET /apps/{appId}/versions/{versionId}/entities/{entityId}/features
- "Get hierarchicalentity details?" -> GET /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}
- "Partially update a hierarchicalentity?" -> PATCH /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}
- "Delete a hierarchicalentity?" -> DELETE /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}
- "Get compositeentity details?" -> GET /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}
- "Update a compositeentity?" -> PUT /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}
- "Delete a compositeentity?" -> DELETE /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}
- "Get closedlist details?" -> GET /apps/{appId}/versions/{versionId}/closedlists/{clEntityId}
- "Update a closedlist?" -> PUT /apps/{appId}/versions/{versionId}/closedlists/{clEntityId}
- "Partially update a closedlist?" -> PATCH /apps/{appId}/versions/{versionId}/closedlists/{clEntityId}
- "Delete a closedlist?" -> DELETE /apps/{appId}/versions/{versionId}/closedlists/{clEntityId}
- "Get prebuilt details?" -> GET /apps/{appId}/versions/{versionId}/prebuilts/{prebuiltId}
- "Delete a prebuilt?" -> DELETE /apps/{appId}/versions/{versionId}/prebuilts/{prebuiltId}
- "Delete a sublist?" -> DELETE /apps/{appId}/versions/{versionId}/closedlists/{clEntityId}/sublists/{subListId}
- "Update a sublist?" -> PUT /apps/{appId}/versions/{versionId}/closedlists/{clEntityId}/sublists/{subListId}
- "List all suggest?" -> GET /apps/{appId}/versions/{versionId}/intents/{intentId}/suggest
- "List all suggest?" -> GET /apps/{appId}/versions/{versionId}/entities/{entityId}/suggest
- "Create a app?" -> POST /apps/
- "List all apps?" -> GET /apps/
- "Create a import?" -> POST /apps/import
- "List all assistants?" -> GET /apps/assistants
- "List all domains?" -> GET /apps/domains
- "List all usagescenarios?" -> GET /apps/usagescenarios
- "List all cultures?" -> GET /apps/cultures
- "List all querylogs?" -> GET /apps/{appId}/querylogs
- "Get app details?" -> GET /apps/{appId}
- "Update a app?" -> PUT /apps/{appId}
- "Delete a app?" -> DELETE /apps/{appId}
- "Create a clone?" -> POST /apps/{appId}/versions/{versionId}/clone
- "Create a publish?" -> POST /apps/{appId}/publish
- "List all versions?" -> GET /apps/{appId}/versions
- "Get version details?" -> GET /apps/{appId}/versions/{versionId}/
- "Update a version?" -> PUT /apps/{appId}/versions/{versionId}/
- "Delete a version?" -> DELETE /apps/{appId}/versions/{versionId}/
- "List all export?" -> GET /apps/{appId}/versions/{versionId}/export
- "Create a train?" -> POST /apps/{appId}/versions/{versionId}/train
- "List all train?" -> GET /apps/{appId}/versions/{versionId}/train
- "Create a import?" -> POST /apps/{appId}/versions/import
- "List all settings?" -> GET /apps/{appId}/settings
- "List all publishsettings?" -> GET /apps/{appId}/publishsettings
- "List all endpoints?" -> GET /apps/{appId}/endpoints
- "Create a sublist?" -> POST /apps/{appId}/versions/{versionId}/closedlists/{clEntityId}/sublists
- "Create a customprebuiltdomain?" -> POST /apps/{appId}/versions/{versionId}/customprebuiltdomains
- "Create a customprebuiltintent?" -> POST /apps/{appId}/versions/{versionId}/customprebuiltintents
- "List all customprebuiltintents?" -> GET /apps/{appId}/versions/{versionId}/customprebuiltintents
- "Create a customprebuiltentity?" -> POST /apps/{appId}/versions/{versionId}/customprebuiltentities
- "List all customprebuiltentities?" -> GET /apps/{appId}/versions/{versionId}/customprebuiltentities
- "List all customprebuiltmodels?" -> GET /apps/{appId}/versions/{versionId}/customprebuiltmodels
- "Delete a customprebuiltdomain?" -> DELETE /apps/{appId}/versions/{versionId}/customprebuiltdomains/{domainName}
- "List all customprebuiltdomains?" -> GET /apps/customprebuiltdomains
- "Create a customprebuiltdomain?" -> POST /apps/customprebuiltdomains
- "Get customprebuiltdomain details?" -> GET /apps/customprebuiltdomains/{culture}
- "Create a children?" -> POST /apps/{appId}/versions/{versionId}/entities/{entityId}/children
- "Get children details?" -> GET /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/children/{hChildId}
- "Partially update a children?" -> PATCH /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/children/{hChildId}
- "Delete a children?" -> DELETE /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/children/{hChildId}
- "Create a children?" -> POST /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/children
- "Delete a children?" -> DELETE /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/children/{cChildId}
- "List all regexentities?" -> GET /apps/{appId}/versions/{versionId}/regexentities
- "Create a regexentity?" -> POST /apps/{appId}/versions/{versionId}/regexentities
- "List all patternanyentities?" -> GET /apps/{appId}/versions/{versionId}/patternanyentities
- "Create a patternanyentity?" -> POST /apps/{appId}/versions/{versionId}/patternanyentities
- "List all roles?" -> GET /apps/{appId}/versions/{versionId}/entities/{entityId}/roles
- "Create a role?" -> POST /apps/{appId}/versions/{versionId}/entities/{entityId}/roles
- "List all roles?" -> GET /apps/{appId}/versions/{versionId}/prebuilts/{entityId}/roles
- "Create a role?" -> POST /apps/{appId}/versions/{versionId}/prebuilts/{entityId}/roles
- "List all roles?" -> GET /apps/{appId}/versions/{versionId}/closedlists/{entityId}/roles
- "Create a role?" -> POST /apps/{appId}/versions/{versionId}/closedlists/{entityId}/roles
- "List all roles?" -> GET /apps/{appId}/versions/{versionId}/regexentities/{entityId}/roles
- "Create a role?" -> POST /apps/{appId}/versions/{versionId}/regexentities/{entityId}/roles
- "List all roles?" -> GET /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/roles
- "Create a role?" -> POST /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/roles
- "List all roles?" -> GET /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/roles
- "Create a role?" -> POST /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/roles
- "List all roles?" -> GET /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/roles
- "Create a role?" -> POST /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/roles
- "List all roles?" -> GET /apps/{appId}/versions/{versionId}/customprebuiltentities/{entityId}/roles
- "Create a role?" -> POST /apps/{appId}/versions/{versionId}/customprebuiltentities/{entityId}/roles
- "List all explicitlist?" -> GET /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/explicitlist
- "Create a explicitlist?" -> POST /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/explicitlist
- "Get regexentity details?" -> GET /apps/{appId}/versions/{versionId}/regexentities/{regexEntityId}
- "Update a regexentity?" -> PUT /apps/{appId}/versions/{versionId}/regexentities/{regexEntityId}
- "Delete a regexentity?" -> DELETE /apps/{appId}/versions/{versionId}/regexentities/{regexEntityId}
- "Get patternanyentity details?" -> GET /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}
- "Update a patternanyentity?" -> PUT /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}
- "Delete a patternanyentity?" -> DELETE /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}
- "Get role details?" -> GET /apps/{appId}/versions/{versionId}/entities/{entityId}/roles/{roleId}
- "Update a role?" -> PUT /apps/{appId}/versions/{versionId}/entities/{entityId}/roles/{roleId}
- "Delete a role?" -> DELETE /apps/{appId}/versions/{versionId}/entities/{entityId}/roles/{roleId}
- "Get role details?" -> GET /apps/{appId}/versions/{versionId}/prebuilts/{entityId}/roles/{roleId}
- "Update a role?" -> PUT /apps/{appId}/versions/{versionId}/prebuilts/{entityId}/roles/{roleId}
- "Delete a role?" -> DELETE /apps/{appId}/versions/{versionId}/prebuilts/{entityId}/roles/{roleId}
- "Get role details?" -> GET /apps/{appId}/versions/{versionId}/closedlists/{entityId}/roles/{roleId}
- "Update a role?" -> PUT /apps/{appId}/versions/{versionId}/closedlists/{entityId}/roles/{roleId}
- "Delete a role?" -> DELETE /apps/{appId}/versions/{versionId}/closedlists/{entityId}/roles/{roleId}
- "Get role details?" -> GET /apps/{appId}/versions/{versionId}/regexentities/{entityId}/roles/{roleId}
- "Update a role?" -> PUT /apps/{appId}/versions/{versionId}/regexentities/{entityId}/roles/{roleId}
- "Delete a role?" -> DELETE /apps/{appId}/versions/{versionId}/regexentities/{entityId}/roles/{roleId}
- "Get role details?" -> GET /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/roles/{roleId}
- "Update a role?" -> PUT /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/roles/{roleId}
- "Delete a role?" -> DELETE /apps/{appId}/versions/{versionId}/compositeentities/{cEntityId}/roles/{roleId}
- "Get role details?" -> GET /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/roles/{roleId}
- "Update a role?" -> PUT /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/roles/{roleId}
- "Delete a role?" -> DELETE /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/roles/{roleId}
- "Get role details?" -> GET /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/roles/{roleId}
- "Update a role?" -> PUT /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/roles/{roleId}
- "Delete a role?" -> DELETE /apps/{appId}/versions/{versionId}/hierarchicalentities/{hEntityId}/roles/{roleId}
- "Get role details?" -> GET /apps/{appId}/versions/{versionId}/customprebuiltentities/{entityId}/roles/{roleId}
- "Update a role?" -> PUT /apps/{appId}/versions/{versionId}/customprebuiltentities/{entityId}/roles/{roleId}
- "Delete a role?" -> DELETE /apps/{appId}/versions/{versionId}/customprebuiltentities/{entityId}/roles/{roleId}
- "Get explicitlist details?" -> GET /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/explicitlist/{itemId}
- "Update a explicitlist?" -> PUT /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/explicitlist/{itemId}
- "Delete a explicitlist?" -> DELETE /apps/{appId}/versions/{versionId}/patternanyentities/{entityId}/explicitlist/{itemId}
- "Create a patternrule?" -> POST /apps/{appId}/versions/{versionId}/patternrule
- "List all patternrules?" -> GET /apps/{appId}/versions/{versionId}/patternrules
- "Create a patternrule?" -> POST /apps/{appId}/versions/{versionId}/patternrules
- "Update a patternrule?" -> PUT /apps/{appId}/versions/{versionId}/patternrules/{patternId}
- "Delete a patternrule?" -> DELETE /apps/{appId}/versions/{versionId}/patternrules/{patternId}
- "List all patternrules?" -> GET /apps/{appId}/versions/{versionId}/intents/{intentId}/patternrules
- "List all settings?" -> GET /apps/{appId}/versions/{versionId}/settings
- "Create a azureaccount?" -> POST /apps/{appId}/azureaccounts
- "List all azureaccounts?" -> GET /apps/{appId}/azureaccounts
- "List all azureaccounts?" -> GET /azureaccounts
- "List all gzip?" -> GET /package/{appId}/slot/{slotName}/gzip
- "List all gzip?" -> GET /package/{appId}/versions/{versionId}/gzip
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
