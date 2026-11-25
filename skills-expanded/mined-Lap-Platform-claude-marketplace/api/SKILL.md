---
name: api
description: "API skill. Use when working with this API for api. Covers 286 endpoints."
version: 1.0.0
generator: lapsh
---

# API
API version: v1

## Auth
ApiKey code in query

## Base URL
https://secure.agco-ats.com

## Setup
1. Set your API key in the appropriate header
2. GET /api/v2/activities -- verify access
3. POST /api/v2/activities -- create first activities

## Endpoints

286 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v2/activities | Get Activities |
| POST | /api/v2/activities | Create an Activity |
| GET | /api/v2/activities/{activityID} | Get an Activity by ID |
| PUT | /api/v2/activities/{activityID} | Update an Activity |
| DELETE | /api/v2/activities/{activityID} | Mark the delete flag for the Activity |
| GET | /api/v2/activityRuns | Get ActivityRuns |
| GET | /api/v2/activityRuns/{activityRunID} | Get an ActivityRun by ID |
| PUT | /api/v2/activityRuns/{activityRunID} | Update an ActivityRun |
| GET | /api/v2/activityRuns/{activityRunID}/status | Get the ActivityRunStatus of an ActivityRun |
| PUT | /api/v2/activityRuns/{activityRunID}/status | Update the ActivityRunStatus of an ActivityRun |
| GET | /api/v2/AftermarketServices/Certificates | No Documentation Found. |
| PUT | /api/v2/AftermarketServices/ECUs/{serialNumber} | Activate or Deactivate an ECU, or Report an ECU as Damaged. |
| GET | /api/v2/AftermarketServices/Engines/{serialNumber}/ProductionData | Get production calibration data for given engine. |
| GET | /api/v2/AftermarketServices/Engines/{serialNumber}/IQACodes | Get injector codes given engine. |
| PUT | /api/v2/AftermarketServices/Engines/{serialNumber}/IQACodes | Report the IQA codes used by an engine |
| GET | /api/v2/AftermarketServices/UserStatuses | Retrieve the status of an EDT Kit Registration with AGCO Power Web Services |
| PUT | /api/v2/AftermarketServices/UserStatuses | Update the status of an EDT Kit Registration with AGCO Power Web Services |
| GET | /api/v2/AftermarketServices/Hello | Check whether there is connectivity to AGCO Power Web Services |
| GET | /api/v2/agents | Get Agents |
| POST | /api/v2/agents | Create an Agent |
| GET | /api/v2/agents/{agentID} | Get Agent |
| PUT | /api/v2/agents/{agentID} | Update an Agent |
| DELETE | /api/v2/agents/{agentID} | Delete an Agent |
| GET | /api/v2/agents/Current | Get Agent associated with the current user |
| GET | /api/v2/agents/{agentID}/ActivityRun | Get an Agent's ActivityRun |
| PUT | /api/v2/agents/{agentID}/ActivityRun | Update the ActivityRun assigned to the Agent. |
| GET | /api/v2/agents/Current/ActivityRun | Get the ActivityRun of Agent associated with the current user |
| PUT | /api/v2/agents/{agentID}/Status | Update an Agent |
| PUT | /api/v2/AuthenticatedUsers/{UserID}/Tokens | Manage API tokens. |
| POST | /api/v2/Authentication | Authenticate a user. |
| GET | /api/v2/Authentication/IsAlive | Acknowledges the connection to the API |
| POST | /api/v2/Authentication/RequestPasswordReset | Request a password reset. |
| POST | /api/v2/Authentication/ResetPasword | Reset a password |
| GET | /api/v2/Authentication/OAuthRedirect | Redirect to OIDC provider with configured and provided query parameters. |
| GET | /api/v2/Authentication/OAuthCallback | Provided as "redirectUri" query parameter when redirecting to OIDC provider. |
| POST | /api/v2/Authentication/OAuthUser | Login using OpenID. |
| GET | /api/v2/Authentication/OAuthCertificate | Retrieve the certificate used for OAuth Client Authentication. |
| GET | /api/v2/AuthorizationCategories | Get authorization categories. |
| POST | /api/v2/AuthorizationCategories | Add an authorization category. |
| PUT | /api/v2/AuthorizationCategories/{id} | Update an authorization category. |
| DELETE | /api/v2/AuthorizationCategories/{id} | Remove an authorization category. |
| POST | /api/v2/AuthorizationCategories/{id}/Users/{userID} | Add a category that a user can see. |
| DELETE | /api/v2/AuthorizationCategories/{id}/Users/{userID} | Deletes a category a user could see. |
| GET | /api/v2/AuthorizationCategories/Users | Returns a report of access that users have to Authorization Categories. |
| GET | /api/v2/AuthorizationCodeDefinitions | Get authorization code definitions. |
| POST | /api/v2/AuthorizationCodeDefinitions | Add an authorization code definition. |
| GET | /api/v2/AuthorizationCodeDefinitions/{id} | Get an authorization code definition by its ID |
| PUT | /api/v2/AuthorizationCodeDefinitions/{id} | Update an authorization code definition |
| DELETE | /api/v2/AuthorizationCodeDefinitions/{id} | Disable an authorization code definition |
| POST | /api/v2/AuthorizationCodeDefinitions/{ID}/Categories/{categoryID} | Add a category to an authorizationCodeDefintion. |
| DELETE | /api/v2/AuthorizationCodeDefinitions/{ID}/Categories/{categoryID} | Deletes the category from the authorization code definition. |
| GET | /api/v2/AuthorizationCodes | Get authorization codes. |
| POST | /api/v2/AuthorizationCodes | Generates an authorization code using the provided definition and parameters. |
| GET | /api/v2/AuthorizationCodes/{id} | Get an authorization code by its ID. |
| PUT | /api/v2/AuthorizationCodes/{id} | Update an authorization code. |
| DELETE | /api/v2/AuthorizationCodes/{id} | Hide an authorization code. |
| GET | /api/v2/AuthorizationCodes/{id}/Validate | No Documentation Found. |
| GET | /api/v2/AuthorizationCodes/{id}/ContactInformation | Get contact information for an authorization code. |
| GET | /api/v2/AuthorizationContactInformation | Get contact information for authorization codes. |
| POST | /api/v2/AuthorizationContactInformation | Add contact information for authorization code. |
| GET | /api/v2/Brands | Gets a list of Brands. |
| GET | /api/v2/Bundles | Get the list of bundles. |
| POST | /api/v2/Bundles | Add a Bundle to the Update System. |
| GET | /api/v2/Bundles/{ID} | Get a specific Bundle by ID. |
| PUT | /api/v2/Bundles/{ID} | Modify a Bundle in the Update System. |
| DELETE | /api/v2/Bundles/{ID} | Delete a Bundle. |
| GET | /api/v2/Clients | Get a List of Clients in the Update System. |
| GET | /api/v2/Clients/{ID} | Get a Client in the Update System. |
| PUT | /api/v2/Clients/{ID} | Update a Client. |
| GET | /api/v2/Clients/{ID}/UpdateGroupSubscriptions | Get a Client's Current Update Group Subscriptions |
| GET | /api/v2/Clients/{ID}/AvailableUpdateGroupSubscriptions | Get a Client's Available Update Group Subscriptions |
| GET | /api/v2/ContentDefinitions | Get ContentDefinitions |
| POST | /api/v2/ContentDefinitions | Create a ContentDefinition |
| GET | /api/v2/ContentDefinitions/{contentDefinitionID} | Get a ContentDefinition by ID |
| PUT | /api/v2/ContentDefinitions/{contentDefinitionID} | Update a ContentDefinition |
| DELETE | /api/v2/ContentDefinitions/{contentDefinitionID} | Delete a ContentDefinition |
| GET | /api/v2/ContentDefinitions/{contentDefinitionID}/Attributes | Get Attributes for a ContentDefinition |
| POST | /api/v2/ContentDefinitions/{contentDefinitionID}/Attributes | Add an Attribute to a ContentDefinition |
| POST | /api/v2/ContentDefinitions/{contentDefinitionID}/Attributes/Batch | No Documentation Found. |
| PUT | /api/v2/ContentDefinitionAttributes/{contentDefinitionAttributeID} | Update an Attribute for a ContentDefinition |
| DELETE | /api/v2/ContentDefinitionAttributes/{contentDefinitionAttributeID} | Remove an Attribute from a ContentDefinition |
| PUT | /api/v2/ContentDefinitionAttributes/Batch | No Documentation Found. |
| GET | /api/v2/ContentReleases | Get ContentReleaseVersion |
| POST | /api/v2/ContentReleases | Create a ContentReleaseVersion |
| GET | /api/v2/ContentReleases/{ContentReleaseId} | Get a Content Release Version by ID |
| PUT | /api/v2/ContentReleases/{ContentReleaseId} | Update a ContentReleaseVersion |
| DELETE | /api/v2/ContentReleases/{ContentReleaseId} | Delete a ContentReleaseVersion |
| GET | /api/v2/ContentSubmissions | Get ContentSubmissions |
| POST | /api/v2/ContentSubmissions | Create a ContentSubmission |
| GET | /api/v2/ContentSubmissions/{contentSubmissionID} | Get a ContentSubmission by ID |
| PUT | /api/v2/ContentSubmissions/{contentSubmissionID} | Update a ContentSubmission |
| DELETE | /api/v2/ContentSubmissions/{contentSubmissionID} | Delete a ContentSubmission |
| GET | /api/v2/ContentSubmissions/{contentSubmissionID}/Status | Get the status of a ContentSubmission |
| GET | /api/v2/ContentSubmissions/{contentSubmissionID}/Attributes | Get Attributes for a ContentSubmission |
| POST | /api/v2/ContentSubmissions/{contentSubmissionID}/Attributes | Add an Attribute to a ContentSubmission |
| POST | /api/v2/ContentSubmissions/{contentSubmissionID}/Attributes/Batch | No Documentation Found. |
| PUT | /api/v2/ContentSubmissionAttributes/{contentSubmissionAttributeID} | Update an Attribute for a ContentSubmission |
| DELETE | /api/v2/ContentSubmissionAttributes/{contentSubmissionAttributeID} | Remove an Attribute from a ContentSubmission |
| PUT | /api/v2/ContentSubmissionAttributes/Batch | No Documentation Found. |
| GET | /api/v2/ContentSubmissionTypes | Returns available Content Submission Types. |
| POST | /api/v2/ContentSubmissionTypes | Add a Content Submission Type |
| GET | /api/v2/ContentSubmissionTypes/{id} | Retrieves a Content Submission Type by its ID. |
| PUT | /api/v2/ContentSubmissionTypes/{id} | Update a Content Submission Type |
| DELETE | /api/v2/ContentSubmissionTypes/{id} | Remove a Content Submission Type |
| GET | /api/v2/DealerByCountry | Get a total count of dealers per country |
| GET | /api/v2/Dealers/{DealerCode} | Lookup a dealer using a dealer code. |
| GET | /api/v2/Dealers | Get a list of dealers. |
| GET | /api/v2/Files | Get a paged response of file metadata. |
| POST | /api/v2/Files | Create the metadata for a file before uploading. The State of the File should be 'Created'. |
| GET | /api/v2/Files/{ID} | Gets a file's metadata. |
| PUT | /api/v2/Files/{ID} | Update the metadata for a file. Size may not be modified by the client. |
| DELETE | /api/v2/Files/{ID} | Mark a file as 'Removed'. Disables download of the file and hides metadata from GET all method |
| GET | /api/v2/Files/{ID}/FileContents | Download the contents of a file. The current State of the File should be 'Available'. |
| PUT | /api/v2/Files/{ID}/FileContents | Upload the contents of a file. The current State of the File should be 'Created'. |
| GET | /api/v2/FileUploadIndexFields | Get File Upload Index Fields |
| POST | /api/v2/FileUploads/Report | Build a report from file uploads |
| GET | /api/v2/FileUploadTypes | Get File Upload Types |
| GET | /api/v2/GlobalImageCategories | Get a paged response of file metadata. |
| POST | /api/v2/GlobalImageCategories | Create the metadata for a file before uploading. The State should be 'Created'. |
| GET | /api/v2/GlobalImageCategories/{ID} | Gets a file's metadata. |
| GET | /api/v2/GlobalImages | Get a paged response of GlobalImage. |
| POST | /api/v2/GlobalImages | Create the metadata for a GlobalImage before uploading. The State should be 'Created'. |
| GET | /api/v2/GlobalImages/{ID} | Gets a GlobalImage's metadata. |
| PUT | /api/v2/GlobalImages/{ID} | Update the metadata for an image. |
| DELETE | /api/v2/GlobalImages/{ID} | Mark a file as 'Removed'. Disables download of the image and hides metadata from GET all method |
| GET | /api/v2/GlobalImages/{ID}/ImageContents | Download the contents of a GlobalImage. The current State of the GlobalImage should be 'Available'. |
| PUT | /api/v2/GlobalImages/{ID}/ImageContents | Upload the contents of a GlobalImage. The current State of the File for the GlobalImage should be 'Created'. |
| GET | /api/v2/jobRuns | Get JobRuns |
| POST | /api/v2/jobRuns | Create a JobRun |
| GET | /api/v2/jobRuns/{jobRunID} | Get a JobRun by ID |
| PUT | /api/v2/jobRuns/{jobRunID} | Update a JobRun |
| DELETE | /api/v2/jobRuns/{jobRunID} | Delete a JobRun |
| GET | /api/v2/jobs | Get Jobs |
| POST | /api/v2/jobs | Create a Job |
| GET | /api/v2/jobs/{jobID} | Get a Job by ID |
| PUT | /api/v2/jobs/{jobID} | Update a Job |
| DELETE | /api/v2/jobs/{jobID} | Mark the delete flag for the Job |
| GET | /api/v2/Languages | Get a list of the languages for which translations are supported. Returns a PagedResponse of Language objects. |
| POST | /api/v2/Languages | Add a Language to support for translations. Accepts a Language object. Returns the Id of the created object. |
| GET | /api/v2/Languages/{LocaleID} | Get a language by its id. Returns a Language object |
| PUT | /api/v2/Languages/{LocaleID} | Update a language’s description. Accepts a Language object. |
| DELETE | /api/v2/Languages/{LocaleID} | Remove a Language from those supported for translations. Marks language as deleted. |
| POST | /api/v2/LicenseActivations | Create a license activation. |
| PUT | /api/v2/LicenseActivations/{ID} | Update a license activiation. |
| PUT | /api/v2/LicenseActivations/{ID}/Confirm | Confirm that the client has applied the updated license. |
| POST | /api/v2/LicenseActivations/RegisterEDTLite | Register an EDT Lite with the Server |
| GET | /api/v2/Licenses | Gets a list of licenses with the specified criteria. |
| GET | /api/v2/Licenses/{ID} | Get a license. |
| GET | /api/v2/Logs | Get the API System logs, most recent first. |
| POST | /api/v2/Logs | Add a Log entry |
| GET | /api/v2/Logs/{ID} | Get a log by ID |
| POST | /api/v2/Notifications | Sends an email message. |
| PUT | /api/v2/Clients/{ClientID}/PackageReports/Batch | Submit a batch of package reports |
| GET | /api/v2/Clients/{ClientID}/PackageReports | Get the package reports for a client. |
| PUT | /api/v2/Clients/{ClientID}/PackageReports | Submit a package report |
| GET | /api/v2/Packages | List Packages. |
| POST | /api/v2/Packages | Add a Package to the Update System. |
| GET | /api/v2/Packages/{ID} | Find a Package. |
| PUT | /api/v2/Packages/{ID} | Modify a Packge to the Update System. |
| DELETE | /api/v2/Packages/{ID} | Delete a Package. |
| GET | /api/v2/PackageTypes | Get all of the Package Types. |
| POST | /api/v2/PackageTypes | Add a Package Type. |
| GET | /api/v2/PackageTypes/{ID} | Get a specific Package Type. |
| PUT | /api/v2/PackageTypes/{ID} | Modify a Package Type. |
| DELETE | /api/v2/PackageTypes/{ID} | Delete a Package Type. |
| POST | /api/v2/PackageTypes/{id}/Users/{userID} | Add a package type that a user can see. |
| DELETE | /api/v2/PackageTypes/{id}/Users/{userID} | Deletes a package type a user could see. |
| PUT | /api/v2/Bundles/{bundleID}/PackageTypetoBundles/Batch | Update multiple Package Type ID to Bundle Relationships. |
| POST | /api/v2/Bundles/{bundleID}/PackageTypetoBundles/Batch | No Documentation Found. |
| GET | /api/v2/PackageTypetoBundles | Get all of the Package Type to Bundle Relationships. |
| PUT | /api/v2/PackageTypetoBundles | Update a Package Type ID to Bundle Relationship. |
| POST | /api/v2/PackageTypetoBundles | Add a new Package Type ID to Bundle Relationship. |
| DELETE | /api/v2/PackageTypetoBundles | Delete a Package Type to Bundle Relationship. |
| GET | /api/v2/Permissions | List Permissions |
| POST | /api/v2/Permissions | Adds a Permission |
| GET | /api/v2/Permissions/{id} | Gets a Permission |
| PUT | /api/v2/Permissions/{id} | Updates a Permission |
| DELETE | /api/v2/Permissions/{id} | Deletes a Permission |
| GET | /api/v2/PriorityPackages | Get a list of Priority Packages by Client. |
| POST | /api/v2/PriorityPackages | Add a Priority Package for a Client. |
| GET | /api/v2/PriorityPackages/{ID} | Get a Priority Packages for a Client. |
| DELETE | /api/v2/PriorityPackages/{ID} | Delete a Priority Package for a Client. |
| GET | /api/v2/Releases | Get Release |
| POST | /api/v2/Releases | Create a Release |
| GET | /api/v2/Releases/{ReleaseId} | Get a  Release by ID |
| PUT | /api/v2/Releases/{releaseId} | Update a Release |
| POST | /api/v2/Releases/{ReleaseId}/Bundle/{BundleId} | Associates the release with a bundle. |
| DELETE | /api/v2/Releases/{ReleaseId}/Bundle/{BundleId} | Deletes the association between a release and a bundle. |
| GET | /api/v2/Reporting/GetClient | Get a Client in the Update System. |
| GET | /api/v2/Reporting/ClientInfo | Get Client Information |
| GET | /api/v2/Reporting/GetSubscriptions | Get a list of current Client Subscriptions. |
| GET | /api/v2/Reporting/RegisteredClients | Get a list of subscribed clients |
| GET | /api/v2/Reporting/UpdateGroups | Get a list of Update Groups.  Update Groups are used by the client to register for a specific type of update. |
| GET | /api/v2/Reporting/PackageStatusSummary | Get a summary report for a Specific Package |
| GET | /api/v2/Reporting/BundleStatusSummary | Get a summary of all Packages in a Bundle |
| GET | /api/v2/Reporting/BundlesInUpdateGroup | Get a list of bundles for UpdateGroup. |
| GET | /api/v2/Reporting/CurrentPackagesInUpdateGroup | Get the current packages for an update group. |
| GET | /api/v2/Reporting/UpdateMetrics | Get data for pie charts in UpdateMetrics. |
| GET | /api/v2/Roles | List Roles |
| POST | /api/v2/Roles | Adds a User Role |
| GET | /api/v2/Roles/{id} | Gets a User Role |
| PUT | /api/v2/Roles/{id} | Updates a User Role |
| DELETE | /api/v2/Roles/{id} | Deletes a User Role |
| GET | /api/v2/Roles/{id}/Permissions | Get the Permissions for a Role |
| PUT | /api/v2/Roles/{id}/Permissions | Manage the Permissions for a Role |
| GET | /api/v2/steps | Get Steps |
| POST | /api/v2/steps | Create a Step |
| GET | /api/v2/steps/{stepID} | Get a Step by ID |
| PUT | /api/v2/steps/{stepID} | Update a Step |
| GET | /api/v2/StringDefinitions | Get a paged response of Global String Definitions. |
| GET | /api/v2/StringDefinitions/{ID} | Get a paged response of Global String Definitions. |
| PUT | /api/v2/StringDefinitions/Batch | Update StringDefinition objects. Accepts an array of StringDefinition objects. This endpoint will add StringDefinitionChange objects to the database. The DescriptionForTranslator may not be modified after a String is submitted for translation. |
| POST | /api/v2/StringDefinitions/Batch | Create StringDefinition object. The originating translation must be provided. Accepts an array of StringDefinition objects. Returns nothing. |
| GET | /api/v2/StringTranslations | Get a paged response of Global String Translations. |
| GET | /api/v2/StringTranslations/{stringId}/{languageId} | Get a single translation based upon stringId and languageId |
| PUT | /api/v2/StringTranslations/{stringId}/{languageId} | Update a string value or a state for a string translation. |
| PUT | /api/v2/StringTranslations/Batch | Update corrections to string translations |
| GET | /api/v2/TranslationKeys | Get a paged response of TranslationKeys. |
| POST | /api/v2/TranslationKeys | Create a translationKey object. |
| GET | /api/v2/TranslationKeys/{ID} | Get TranslationKey by ID |
| PUT | /api/v2/TranslationKeys/{ID} | Update the StringID of the translationKey object. |
| GET | /api/v2/TranslationRequests | Get all TranslationRequest objects. Returns a PagedResponse of TranslationRequest objects with their language ids and string ids. |
| POST | /api/v2/TranslationRequests | Create a translation request. Accepts a TranslationRequest object. Returns the Id of the created object. The state of the TranslationRequest must be ‘NotSubmitted’. |
| GET | /api/v2/TranslationRequests/{Id} | Get a TranslationRequest object by id. Returns TranslationRequest object with its language ids and string ids. |
| PUT | /api/v2/TranslationRequests/{Id} | Update a TranslationRequest object by id. Accepts a TranslationRequest object. |
| PUT | /api/v2/TranslationRequests/{Id}/Strings | No Documentation Found. |
| GET | /api/v2/TranslationSets | Get a PagedResponse of TranslationSet objects. Related TranslationSetStrings are NOT returned |
| GET | /api/v2/TranslationSets/{ID} | Get a TranslationSet object by its id. Related TranslationSetStrings are NOT returned. |
| PUT | /api/v2/TranslationSets/{ID} | Update a Translation Set. Accepts a TranslationSet object. Only the state property may be updated. |
| GET | /api/v2/TranslationSets/{ID}/Strings | Get a PagedResponse of TranslationSetString objects |
| PUT | /api/v2/TranslationSets/{ID}/Strings | No Documentation Found. |
| GET | /api/v2/TranslationSets/{ID}/SourceStrings | Gets the information needed to translate a string in a translation set |
| GET | /api/v2/TranslationSets/{ID}/Statistics | Gets the statistics for translation sets such as the language ids and count of string definitions. |
| GET | /api/v2/TranslationSets/{ID}/Attributes | Get a PagedResponse of TranslationSetAttribute objects |
| POST | /api/v2/TranslationSets/{ID}/Attributes | Create a TranslationSetAttribute object |
| PUT | /api/v2/TranslationSetAttributes/{ID} | Update a TranslationSetAttribute object |
| DELETE | /api/v2/TranslationSetAttributes/{ID} | Delete a set of TranslationSetAttribute object |
| PUT | /api/v2/TranslationSetAttributes/Batch | No Documentation Found. |
| POST | /api/v2/TranslationSets/{ID}/Attributes/Batch | No Documentation Found. |
| GET | /api/v2/UpdateGroupClientRelationships | Get a list of current Client Subscriptions. |
| PUT | /api/v2/UpdateGroupClientRelationships | DEPRECATED. Set client subscription status for an update group. |
| POST | /api/v2/UpdateGroupClientRelationships | Add a subscription |
| GET | /api/v2/UpdateGroupClientRelationships/{RelationshipID} | Get a subscription by RelationshipID |
| PUT | /api/v2/UpdateGroupClientRelationships/{RelationshipID} | Updates a Subscription |
| GET | /api/v2/UpdateGroups | Get a list of Update Groups.  Update Groups are used by the client to register for a specific type of update. |
| POST | /api/v2/UpdateGroups | Add a new Update Group.  The report field is a string that has a dot based request for a specific piece of submitted data. |
| GET | /api/v2/UpdateGroups/{ID} | Get a specific Update Group by ID. |
| PUT | /api/v2/UpdateGroups/{ID} | Modify an Update Group. |
| DELETE | /api/v2/UpdateGroups/{ID} | Delete an Update Group. |
| GET | /api/v2/UpdateGroups/{ID}/Bundles | Get a list of bundles for UpdateGroup. |
| POST | /api/v2/UpdateGroups/{id}/Users/{userID} | Add an updateGroup that a user can see. |
| DELETE | /api/v2/UpdateGroups/{id}/Users/{userID} | Deletes an update group a user could see. |
| GET | /api/v2/UpdateGroupSubscriptions | Get Update Group Subscriptions |
| POST | /api/v2/UpdateGroupSubscriptions | Add an Update Group Subscription |
| GET | /api/v2/UpdateGroupSubscriptions/{UpdateGroupSubscriptionID} | Get an Update Group Subscription |
| PUT | /api/v2/UpdateGroupSubscriptions/{UpdateGroupSubscriptionID} | Update an Update Group Subscription |
| DELETE | /api/v2/UpdateGroupSubscriptions/{UpdateGroupSubscriptionID} | Delete an Update Group Subscription |
| PUT | /api/v2/UpdateGroupSubscriptions/Batch | No Documentation Found. |
| POST | /api/v2/UpdateGroupSubscriptions/Batch | No Documentation Found. |
| GET | /api/v2/UpdateSystem | Checks the Client ID into the Update System. |
| GET | /api/v2/Clients/{ClientID}/CachedFiles | Get a list of Cached Files installed on the client Machine. |
| GET | /api/v2/UserContentDefinitions | Get UserContentDefinitions |
| POST | /api/v2/UserContentDefinitions | Create a UserContentDefinition |
| GET | /api/v2/UserContentDefinitions/{userContentDefinitionID} | Get a UserContentDefinition by ID |
| DELETE | /api/v2/UserContentDefinitions/{userContentDefinitionID} | Delete a UserContentDefinition |
| GET | /api/v2/Users/{id}/Permissions | Get a user's permissions |
| GET | /api/v2/Users/Current/Permissions | Get a user's permissions |
| GET | /api/v2/Users/{id}/Roles | Get a user's roles |
| PUT | /api/v2/Users/{id}/Roles | Update a user's roles |
| GET | /api/v2/Roles/{id}/Users | Get all user's in a role |
| PUT | /api/v2/Roles/{id}/Users | Update a Role's users |
| GET | /api/v2/Users/Current/Roles | Gets the current user's roles |
| GET | /api/v2/Users | Get users |
| POST | /api/v2/Users | Create a user |
| GET | /api/v2/Users/{id} | Get a specific user |
| PUT | /api/v2/Users/{id} | Update a user |
| DELETE | /api/v2/Users/{id} | Delete a user |
| GET | /api/v2/Users/Current | Gets the current user |
| PUT | /api/v2/Users/Current | Update a user |
| GET | /api/v2/VoucherHistory | Gets voucher history data |
| GET | /api/v2/Vouchers | Gets a list of vouchers |
| POST | /api/v2/Vouchers | Create a voucher |
| GET | /api/v2/Vouchers/{VoucherCode} | Get a voucher |
| PUT | /api/v2/Vouchers/{VoucherCode} | Update a voucher |
| DELETE | /api/v2/Vouchers/{VoucherCode} | Delete a voucher |
| GET | /api/v2/Vouchers/{VoucherCode}/VoucherHistory | Get a voucher's history. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all activities?" -> GET /api/v2/activities
- "Create a activity?" -> POST /api/v2/activities
- "Get activity details?" -> GET /api/v2/activities/{activityID}
- "Update a activity?" -> PUT /api/v2/activities/{activityID}
- "Delete a activity?" -> DELETE /api/v2/activities/{activityID}
- "List all activityRuns?" -> GET /api/v2/activityRuns
- "Get activityRun details?" -> GET /api/v2/activityRuns/{activityRunID}
- "Update a activityRun?" -> PUT /api/v2/activityRuns/{activityRunID}
- "List all status?" -> GET /api/v2/activityRuns/{activityRunID}/status
- "List all Certificates?" -> GET /api/v2/AftermarketServices/Certificates
- "Update a ECU?" -> PUT /api/v2/AftermarketServices/ECUs/{serialNumber}
- "List all ProductionData?" -> GET /api/v2/AftermarketServices/Engines/{serialNumber}/ProductionData
- "List all IQACodes?" -> GET /api/v2/AftermarketServices/Engines/{serialNumber}/IQACodes
- "List all UserStatuses?" -> GET /api/v2/AftermarketServices/UserStatuses
- "List all Hello?" -> GET /api/v2/AftermarketServices/Hello
- "List all agents?" -> GET /api/v2/agents
- "Create a agent?" -> POST /api/v2/agents
- "Get agent details?" -> GET /api/v2/agents/{agentID}
- "Update a agent?" -> PUT /api/v2/agents/{agentID}
- "Delete a agent?" -> DELETE /api/v2/agents/{agentID}
- "List all Current?" -> GET /api/v2/agents/Current
- "List all ActivityRun?" -> GET /api/v2/agents/{agentID}/ActivityRun
- "List all ActivityRun?" -> GET /api/v2/agents/Current/ActivityRun
- "Create a Authentication?" -> POST /api/v2/Authentication
- "List all IsAlive?" -> GET /api/v2/Authentication/IsAlive
- "Create a RequestPasswordReset?" -> POST /api/v2/Authentication/RequestPasswordReset
- "Create a ResetPasword?" -> POST /api/v2/Authentication/ResetPasword
- "List all OAuthRedirect?" -> GET /api/v2/Authentication/OAuthRedirect
- "List all OAuthCallback?" -> GET /api/v2/Authentication/OAuthCallback
- "Create a OAuthUser?" -> POST /api/v2/Authentication/OAuthUser
- "List all OAuthCertificate?" -> GET /api/v2/Authentication/OAuthCertificate
- "List all AuthorizationCategories?" -> GET /api/v2/AuthorizationCategories
- "Create a AuthorizationCategory?" -> POST /api/v2/AuthorizationCategories
- "Update a AuthorizationCategory?" -> PUT /api/v2/AuthorizationCategories/{id}
- "Delete a AuthorizationCategory?" -> DELETE /api/v2/AuthorizationCategories/{id}
- "Delete a User?" -> DELETE /api/v2/AuthorizationCategories/{id}/Users/{userID}
- "List all Users?" -> GET /api/v2/AuthorizationCategories/Users
- "List all AuthorizationCodeDefinitions?" -> GET /api/v2/AuthorizationCodeDefinitions
- "Create a AuthorizationCodeDefinition?" -> POST /api/v2/AuthorizationCodeDefinitions
- "Get AuthorizationCodeDefinition details?" -> GET /api/v2/AuthorizationCodeDefinitions/{id}
- "Update a AuthorizationCodeDefinition?" -> PUT /api/v2/AuthorizationCodeDefinitions/{id}
- "Delete a AuthorizationCodeDefinition?" -> DELETE /api/v2/AuthorizationCodeDefinitions/{id}
- "Delete a Category?" -> DELETE /api/v2/AuthorizationCodeDefinitions/{ID}/Categories/{categoryID}
- "List all AuthorizationCodes?" -> GET /api/v2/AuthorizationCodes
- "Create a AuthorizationCode?" -> POST /api/v2/AuthorizationCodes
- "Get AuthorizationCode details?" -> GET /api/v2/AuthorizationCodes/{id}
- "Update a AuthorizationCode?" -> PUT /api/v2/AuthorizationCodes/{id}
- "Delete a AuthorizationCode?" -> DELETE /api/v2/AuthorizationCodes/{id}
- "List all Validate?" -> GET /api/v2/AuthorizationCodes/{id}/Validate
- "List all ContactInformation?" -> GET /api/v2/AuthorizationCodes/{id}/ContactInformation
- "List all AuthorizationContactInformation?" -> GET /api/v2/AuthorizationContactInformation
- "Create a AuthorizationContactInformation?" -> POST /api/v2/AuthorizationContactInformation
- "List all Brands?" -> GET /api/v2/Brands
- "List all Bundles?" -> GET /api/v2/Bundles
- "Create a Bundle?" -> POST /api/v2/Bundles
- "Get Bundle details?" -> GET /api/v2/Bundles/{ID}
- "Update a Bundle?" -> PUT /api/v2/Bundles/{ID}
- "Delete a Bundle?" -> DELETE /api/v2/Bundles/{ID}
- "List all Clients?" -> GET /api/v2/Clients
- "Get Client details?" -> GET /api/v2/Clients/{ID}
- "Update a Client?" -> PUT /api/v2/Clients/{ID}
- "List all UpdateGroupSubscriptions?" -> GET /api/v2/Clients/{ID}/UpdateGroupSubscriptions
- "List all AvailableUpdateGroupSubscriptions?" -> GET /api/v2/Clients/{ID}/AvailableUpdateGroupSubscriptions
- "List all ContentDefinitions?" -> GET /api/v2/ContentDefinitions
- "Create a ContentDefinition?" -> POST /api/v2/ContentDefinitions
- "Get ContentDefinition details?" -> GET /api/v2/ContentDefinitions/{contentDefinitionID}
- "Update a ContentDefinition?" -> PUT /api/v2/ContentDefinitions/{contentDefinitionID}
- "Delete a ContentDefinition?" -> DELETE /api/v2/ContentDefinitions/{contentDefinitionID}
- "List all Attributes?" -> GET /api/v2/ContentDefinitions/{contentDefinitionID}/Attributes
- "Create a Attribute?" -> POST /api/v2/ContentDefinitions/{contentDefinitionID}/Attributes
- "Create a Batch?" -> POST /api/v2/ContentDefinitions/{contentDefinitionID}/Attributes/Batch
- "Update a ContentDefinitionAttribute?" -> PUT /api/v2/ContentDefinitionAttributes/{contentDefinitionAttributeID}
- "Delete a ContentDefinitionAttribute?" -> DELETE /api/v2/ContentDefinitionAttributes/{contentDefinitionAttributeID}
- "List all ContentReleases?" -> GET /api/v2/ContentReleases
- "Create a ContentRelease?" -> POST /api/v2/ContentReleases
- "Get ContentRelease details?" -> GET /api/v2/ContentReleases/{ContentReleaseId}
- "Update a ContentRelease?" -> PUT /api/v2/ContentReleases/{ContentReleaseId}
- "Delete a ContentRelease?" -> DELETE /api/v2/ContentReleases/{ContentReleaseId}
- "List all ContentSubmissions?" -> GET /api/v2/ContentSubmissions
- "Create a ContentSubmission?" -> POST /api/v2/ContentSubmissions
- "Get ContentSubmission details?" -> GET /api/v2/ContentSubmissions/{contentSubmissionID}
- "Update a ContentSubmission?" -> PUT /api/v2/ContentSubmissions/{contentSubmissionID}
- "Delete a ContentSubmission?" -> DELETE /api/v2/ContentSubmissions/{contentSubmissionID}
- "List all Status?" -> GET /api/v2/ContentSubmissions/{contentSubmissionID}/Status
- "List all Attributes?" -> GET /api/v2/ContentSubmissions/{contentSubmissionID}/Attributes
- "Create a Attribute?" -> POST /api/v2/ContentSubmissions/{contentSubmissionID}/Attributes
- "Create a Batch?" -> POST /api/v2/ContentSubmissions/{contentSubmissionID}/Attributes/Batch
- "Update a ContentSubmissionAttribute?" -> PUT /api/v2/ContentSubmissionAttributes/{contentSubmissionAttributeID}
- "Delete a ContentSubmissionAttribute?" -> DELETE /api/v2/ContentSubmissionAttributes/{contentSubmissionAttributeID}
- "List all ContentSubmissionTypes?" -> GET /api/v2/ContentSubmissionTypes
- "Create a ContentSubmissionType?" -> POST /api/v2/ContentSubmissionTypes
- "Get ContentSubmissionType details?" -> GET /api/v2/ContentSubmissionTypes/{id}
- "Update a ContentSubmissionType?" -> PUT /api/v2/ContentSubmissionTypes/{id}
- "Delete a ContentSubmissionType?" -> DELETE /api/v2/ContentSubmissionTypes/{id}
- "List all DealerByCountry?" -> GET /api/v2/DealerByCountry
- "Get Dealer details?" -> GET /api/v2/Dealers/{DealerCode}
- "List all Dealers?" -> GET /api/v2/Dealers
- "List all Files?" -> GET /api/v2/Files
- "Create a File?" -> POST /api/v2/Files
- "Get File details?" -> GET /api/v2/Files/{ID}
- "Update a File?" -> PUT /api/v2/Files/{ID}
- "Delete a File?" -> DELETE /api/v2/Files/{ID}
- "List all FileContents?" -> GET /api/v2/Files/{ID}/FileContents
- "List all FileUploadIndexFields?" -> GET /api/v2/FileUploadIndexFields
- "Create a Report?" -> POST /api/v2/FileUploads/Report
- "List all FileUploadTypes?" -> GET /api/v2/FileUploadTypes
- "List all GlobalImageCategories?" -> GET /api/v2/GlobalImageCategories
- "Create a GlobalImageCategory?" -> POST /api/v2/GlobalImageCategories
- "Get GlobalImageCategory details?" -> GET /api/v2/GlobalImageCategories/{ID}
- "Search GlobalImages?" -> GET /api/v2/GlobalImages
- "Create a GlobalImage?" -> POST /api/v2/GlobalImages
- "Get GlobalImage details?" -> GET /api/v2/GlobalImages/{ID}
- "Update a GlobalImage?" -> PUT /api/v2/GlobalImages/{ID}
- "Delete a GlobalImage?" -> DELETE /api/v2/GlobalImages/{ID}
- "List all ImageContents?" -> GET /api/v2/GlobalImages/{ID}/ImageContents
- "List all jobRuns?" -> GET /api/v2/jobRuns
- "Create a jobRun?" -> POST /api/v2/jobRuns
- "Get jobRun details?" -> GET /api/v2/jobRuns/{jobRunID}
- "Update a jobRun?" -> PUT /api/v2/jobRuns/{jobRunID}
- "Delete a jobRun?" -> DELETE /api/v2/jobRuns/{jobRunID}
- "List all jobs?" -> GET /api/v2/jobs
- "Create a job?" -> POST /api/v2/jobs
- "Get job details?" -> GET /api/v2/jobs/{jobID}
- "Update a job?" -> PUT /api/v2/jobs/{jobID}
- "Delete a job?" -> DELETE /api/v2/jobs/{jobID}
- "List all Languages?" -> GET /api/v2/Languages
- "Create a Language?" -> POST /api/v2/Languages
- "Get Language details?" -> GET /api/v2/Languages/{LocaleID}
- "Update a Language?" -> PUT /api/v2/Languages/{LocaleID}
- "Delete a Language?" -> DELETE /api/v2/Languages/{LocaleID}
- "Create a LicenseActivation?" -> POST /api/v2/LicenseActivations
- "Update a LicenseActivation?" -> PUT /api/v2/LicenseActivations/{ID}
- "Create a RegisterEDTLite?" -> POST /api/v2/LicenseActivations/RegisterEDTLite
- "List all Licenses?" -> GET /api/v2/Licenses
- "Get Licens details?" -> GET /api/v2/Licenses/{ID}
- "List all Logs?" -> GET /api/v2/Logs
- "Create a Log?" -> POST /api/v2/Logs
- "Get Log details?" -> GET /api/v2/Logs/{ID}
- "Create a Notification?" -> POST /api/v2/Notifications
- "List all PackageReports?" -> GET /api/v2/Clients/{ClientID}/PackageReports
- "List all Packages?" -> GET /api/v2/Packages
- "Create a Package?" -> POST /api/v2/Packages
- "Get Package details?" -> GET /api/v2/Packages/{ID}
- "Update a Package?" -> PUT /api/v2/Packages/{ID}
- "Delete a Package?" -> DELETE /api/v2/Packages/{ID}
- "List all PackageTypes?" -> GET /api/v2/PackageTypes
- "Create a PackageType?" -> POST /api/v2/PackageTypes
- "Get PackageType details?" -> GET /api/v2/PackageTypes/{ID}
- "Update a PackageType?" -> PUT /api/v2/PackageTypes/{ID}
- "Delete a PackageType?" -> DELETE /api/v2/PackageTypes/{ID}
- "Delete a User?" -> DELETE /api/v2/PackageTypes/{id}/Users/{userID}
- "Create a Batch?" -> POST /api/v2/Bundles/{bundleID}/PackageTypetoBundles/Batch
- "List all PackageTypetoBundles?" -> GET /api/v2/PackageTypetoBundles
- "Create a PackageTypetoBundle?" -> POST /api/v2/PackageTypetoBundles
- "List all Permissions?" -> GET /api/v2/Permissions
- "Create a Permission?" -> POST /api/v2/Permissions
- "Get Permission details?" -> GET /api/v2/Permissions/{id}
- "Update a Permission?" -> PUT /api/v2/Permissions/{id}
- "Delete a Permission?" -> DELETE /api/v2/Permissions/{id}
- "List all PriorityPackages?" -> GET /api/v2/PriorityPackages
- "Create a PriorityPackage?" -> POST /api/v2/PriorityPackages
- "Get PriorityPackage details?" -> GET /api/v2/PriorityPackages/{ID}
- "Delete a PriorityPackage?" -> DELETE /api/v2/PriorityPackages/{ID}
- "List all Releases?" -> GET /api/v2/Releases
- "Create a Release?" -> POST /api/v2/Releases
- "Get Release details?" -> GET /api/v2/Releases/{ReleaseId}
- "Update a Release?" -> PUT /api/v2/Releases/{releaseId}
- "Delete a Bundle?" -> DELETE /api/v2/Releases/{ReleaseId}/Bundle/{BundleId}
- "List all GetClient?" -> GET /api/v2/Reporting/GetClient
- "List all ClientInfo?" -> GET /api/v2/Reporting/ClientInfo
- "List all GetSubscriptions?" -> GET /api/v2/Reporting/GetSubscriptions
- "List all RegisteredClients?" -> GET /api/v2/Reporting/RegisteredClients
- "List all UpdateGroups?" -> GET /api/v2/Reporting/UpdateGroups
- "List all PackageStatusSummary?" -> GET /api/v2/Reporting/PackageStatusSummary
- "List all BundleStatusSummary?" -> GET /api/v2/Reporting/BundleStatusSummary
- "List all BundlesInUpdateGroup?" -> GET /api/v2/Reporting/BundlesInUpdateGroup
- "List all CurrentPackagesInUpdateGroup?" -> GET /api/v2/Reporting/CurrentPackagesInUpdateGroup
- "List all UpdateMetrics?" -> GET /api/v2/Reporting/UpdateMetrics
- "List all Roles?" -> GET /api/v2/Roles
- "Create a Role?" -> POST /api/v2/Roles
- "Get Role details?" -> GET /api/v2/Roles/{id}
- "Update a Role?" -> PUT /api/v2/Roles/{id}
- "Delete a Role?" -> DELETE /api/v2/Roles/{id}
- "List all Permissions?" -> GET /api/v2/Roles/{id}/Permissions
- "List all steps?" -> GET /api/v2/steps
- "Create a step?" -> POST /api/v2/steps
- "Get step details?" -> GET /api/v2/steps/{stepID}
- "Update a step?" -> PUT /api/v2/steps/{stepID}
- "List all StringDefinitions?" -> GET /api/v2/StringDefinitions
- "Get StringDefinition details?" -> GET /api/v2/StringDefinitions/{ID}
- "Create a Batch?" -> POST /api/v2/StringDefinitions/Batch
- "List all StringTranslations?" -> GET /api/v2/StringTranslations
- "Get StringTranslation details?" -> GET /api/v2/StringTranslations/{stringId}/{languageId}
- "Update a StringTranslation?" -> PUT /api/v2/StringTranslations/{stringId}/{languageId}
- "List all TranslationKeys?" -> GET /api/v2/TranslationKeys
- "Create a TranslationKey?" -> POST /api/v2/TranslationKeys
- "Get TranslationKey details?" -> GET /api/v2/TranslationKeys/{ID}
- "Update a TranslationKey?" -> PUT /api/v2/TranslationKeys/{ID}
- "List all TranslationRequests?" -> GET /api/v2/TranslationRequests
- "Create a TranslationRequest?" -> POST /api/v2/TranslationRequests
- "Get TranslationRequest details?" -> GET /api/v2/TranslationRequests/{Id}
- "Update a TranslationRequest?" -> PUT /api/v2/TranslationRequests/{Id}
- "List all TranslationSets?" -> GET /api/v2/TranslationSets
- "Get TranslationSet details?" -> GET /api/v2/TranslationSets/{ID}
- "Update a TranslationSet?" -> PUT /api/v2/TranslationSets/{ID}
- "List all Strings?" -> GET /api/v2/TranslationSets/{ID}/Strings
- "List all SourceStrings?" -> GET /api/v2/TranslationSets/{ID}/SourceStrings
- "List all Statistics?" -> GET /api/v2/TranslationSets/{ID}/Statistics
- "List all Attributes?" -> GET /api/v2/TranslationSets/{ID}/Attributes
- "Create a Attribute?" -> POST /api/v2/TranslationSets/{ID}/Attributes
- "Update a TranslationSetAttribute?" -> PUT /api/v2/TranslationSetAttributes/{ID}
- "Delete a TranslationSetAttribute?" -> DELETE /api/v2/TranslationSetAttributes/{ID}
- "Create a Batch?" -> POST /api/v2/TranslationSets/{ID}/Attributes/Batch
- "List all UpdateGroupClientRelationships?" -> GET /api/v2/UpdateGroupClientRelationships
- "Create a UpdateGroupClientRelationship?" -> POST /api/v2/UpdateGroupClientRelationships
- "Get UpdateGroupClientRelationship details?" -> GET /api/v2/UpdateGroupClientRelationships/{RelationshipID}
- "Update a UpdateGroupClientRelationship?" -> PUT /api/v2/UpdateGroupClientRelationships/{RelationshipID}
- "List all UpdateGroups?" -> GET /api/v2/UpdateGroups
- "Create a UpdateGroup?" -> POST /api/v2/UpdateGroups
- "Get UpdateGroup details?" -> GET /api/v2/UpdateGroups/{ID}
- "Update a UpdateGroup?" -> PUT /api/v2/UpdateGroups/{ID}
- "Delete a UpdateGroup?" -> DELETE /api/v2/UpdateGroups/{ID}
- "List all Bundles?" -> GET /api/v2/UpdateGroups/{ID}/Bundles
- "Delete a User?" -> DELETE /api/v2/UpdateGroups/{id}/Users/{userID}
- "List all UpdateGroupSubscriptions?" -> GET /api/v2/UpdateGroupSubscriptions
- "Create a UpdateGroupSubscription?" -> POST /api/v2/UpdateGroupSubscriptions
- "Get UpdateGroupSubscription details?" -> GET /api/v2/UpdateGroupSubscriptions/{UpdateGroupSubscriptionID}
- "Update a UpdateGroupSubscription?" -> PUT /api/v2/UpdateGroupSubscriptions/{UpdateGroupSubscriptionID}
- "Delete a UpdateGroupSubscription?" -> DELETE /api/v2/UpdateGroupSubscriptions/{UpdateGroupSubscriptionID}
- "Create a Batch?" -> POST /api/v2/UpdateGroupSubscriptions/Batch
- "List all UpdateSystem?" -> GET /api/v2/UpdateSystem
- "List all CachedFiles?" -> GET /api/v2/Clients/{ClientID}/CachedFiles
- "List all UserContentDefinitions?" -> GET /api/v2/UserContentDefinitions
- "Create a UserContentDefinition?" -> POST /api/v2/UserContentDefinitions
- "Get UserContentDefinition details?" -> GET /api/v2/UserContentDefinitions/{userContentDefinitionID}
- "Delete a UserContentDefinition?" -> DELETE /api/v2/UserContentDefinitions/{userContentDefinitionID}
- "List all Permissions?" -> GET /api/v2/Users/{id}/Permissions
- "List all Permissions?" -> GET /api/v2/Users/Current/Permissions
- "List all Roles?" -> GET /api/v2/Users/{id}/Roles
- "List all Users?" -> GET /api/v2/Roles/{id}/Users
- "List all Roles?" -> GET /api/v2/Users/Current/Roles
- "List all Users?" -> GET /api/v2/Users
- "Create a User?" -> POST /api/v2/Users
- "Get User details?" -> GET /api/v2/Users/{id}
- "Update a User?" -> PUT /api/v2/Users/{id}
- "Delete a User?" -> DELETE /api/v2/Users/{id}
- "List all Current?" -> GET /api/v2/Users/Current
- "List all VoucherHistory?" -> GET /api/v2/VoucherHistory
- "List all Vouchers?" -> GET /api/v2/Vouchers
- "Create a Voucher?" -> POST /api/v2/Vouchers
- "Get Voucher details?" -> GET /api/v2/Vouchers/{VoucherCode}
- "Update a Voucher?" -> PUT /api/v2/Vouchers/{VoucherCode}
- "Delete a Voucher?" -> DELETE /api/v2/Vouchers/{VoucherCode}
- "List all VoucherHistory?" -> GET /api/v2/Vouchers/{VoucherCode}/VoucherHistory
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
