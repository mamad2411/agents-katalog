---
name: amazon-quicksight
description: "Amazon QuickSight API skill. Use when working with Amazon QuickSight for accounts, account, resources. Covers 177 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon QuickSight
API version: 2018-04-01

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /accounts/{AwsAccountId}/customizations -- verify access
3. POST /accounts/{AwsAccountId}/topics/{TopicId}/batch-create-reviewed-answers -- create first batch-create-reviewed-answers

## Endpoints

177 endpoints across 3 groups. See references/api-spec.lap for full details.

### accounts
| Method | Path | Description |
|--------|------|-------------|
| POST | /accounts/{AwsAccountId}/topics/{TopicId}/batch-create-reviewed-answers | Creates new reviewed answers for a Q Topic. |
| POST | /accounts/{AwsAccountId}/topics/{TopicId}/batch-delete-reviewed-answers | Deletes reviewed answers for Q Topic. |
| DELETE | /accounts/{AwsAccountId}/data-sets/{DataSetId}/ingestions/{IngestionId} | Cancels an ongoing ingestion of data into SPICE. |
| POST | /accounts/{AwsAccountId}/customizations | Creates Amazon QuickSight customizations for the current Amazon Web Services Region. Currently, you can add a custom default theme by using the CreateAccountCustomization or UpdateAccountCustomization API operation. To further customize Amazon QuickSight by removing Amazon QuickSight sample assets and videos for all new users, see Customizing Amazon QuickSight in the Amazon QuickSight User Guide.  You can create customizations for your Amazon Web Services account or, if you specify a namespace, for a QuickSight namespace instead. Customizations that apply to a namespace always override customizations that apply to an Amazon Web Services account. To find out which customizations apply, use the DescribeAccountCustomization API operation. Before you use the CreateAccountCustomization API operation to add a theme as the namespace default, make sure that you first share the theme with the namespace. If you don't share it with the namespace, the theme isn't visible to your users even if you make it the default theme. To check if the theme is shared, view the current permissions by using the  DescribeThemePermissions  API operation. To share the theme, grant permissions by using the  UpdateThemePermissions  API operation. |
| POST | /accounts/{AwsAccountId}/analyses/{AnalysisId} | Creates an analysis in Amazon QuickSight. Analyses can be created either from a template or from an AnalysisDefinition. |
| POST | /accounts/{AwsAccountId}/dashboards/{DashboardId} | Creates a dashboard from either a template or directly with a DashboardDefinition. To first create a template, see the  CreateTemplate  API operation. A dashboard is an entity in Amazon QuickSight that identifies Amazon QuickSight reports, created from analyses. You can share Amazon QuickSight dashboards. With the right permissions, you can create scheduled email reports from them. If you have the correct permissions, you can create a dashboard from a template that exists in a different Amazon Web Services account. |
| POST | /accounts/{AwsAccountId}/data-sets | Creates a dataset. This operation doesn't support datasets that include uploaded files as a source. |
| POST | /accounts/{AwsAccountId}/data-sources | Creates a data source. |
| POST | /accounts/{AwsAccountId}/folders/{FolderId} | Creates an empty shared folder. |
| PUT | /accounts/{AwsAccountId}/folders/{FolderId}/members/{MemberType}/{MemberId} | Adds an asset, such as a dashboard, analysis, or dataset into a folder. |
| POST | /accounts/{AwsAccountId}/namespaces/{Namespace}/groups | Use the CreateGroup operation to create a group in Amazon QuickSight. You can create up to 10,000 groups in a namespace. If you want to create more than 10,000 groups in a namespace, contact Amazon Web Services Support. The permissions resource is arn:aws:quicksight:&lt;your-region&gt;:&lt;relevant-aws-account-id&gt;:group/default/&lt;group-name&gt; . The response is a group object. |
| PUT | /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName}/members/{MemberName} | Adds an Amazon QuickSight user to an Amazon QuickSight group. |
| POST | /accounts/{AwsAccountId}/namespaces/{Namespace}/iam-policy-assignments/ | Creates an assignment with one specified IAM policy, identified by its Amazon Resource Name (ARN). This policy assignment is attached to the specified groups or users of Amazon QuickSight. Assignment names are unique per Amazon Web Services account. To avoid overwriting rules in other namespaces, use assignment names that are unique. |
| PUT | /accounts/{AwsAccountId}/data-sets/{DataSetId}/ingestions/{IngestionId} | Creates and starts a new SPICE ingestion for a dataset. You can manually refresh datasets in an Enterprise edition account 32 times in a 24-hour period. You can manually refresh datasets in a Standard edition account 8 times in a 24-hour period. Each 24-hour period is measured starting 24 hours before the current date and time. Any ingestions operating on tagged datasets inherit the same tags automatically for use in access control. For an example, see How do I create an IAM policy to control access to Amazon EC2 resources using tags? in the Amazon Web Services Knowledge Center. Tags are visible on the tagged dataset, but not on the ingestion resource. |
| POST | /accounts/{AwsAccountId} | (Enterprise edition only) Creates a new namespace for you to use with Amazon QuickSight. A namespace allows you to isolate the Amazon QuickSight users and groups that are registered for that namespace. Users that access the namespace can share assets only with other users or groups in the same namespace. They can't see users and groups in other namespaces. You can create a namespace after your Amazon Web Services account is subscribed to Amazon QuickSight. The namespace must be unique within the Amazon Web Services account. By default, there is a limit of 100 namespaces per Amazon Web Services account. To increase your limit, create a ticket with Amazon Web Services Support. |
| POST | /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-schedules | Creates a refresh schedule for a dataset. You can create up to 5 different schedules for a single dataset. |
| POST | /accounts/{AwsAccountId}/namespaces/{Namespace}/roles/{Role}/members/{MemberName} | Use CreateRoleMembership to add an existing Amazon QuickSight group to an existing role. |
| POST | /accounts/{AwsAccountId}/templates/{TemplateId} | Creates a template either from a TemplateDefinition or from an existing Amazon QuickSight analysis or template. You can use the resulting template to create additional dashboards, templates, or analyses. A template is an entity in Amazon QuickSight that encapsulates the metadata required to create an analysis and that you can use to create s dashboard. A template adds a layer of abstraction by using placeholders to replace the dataset associated with the analysis. You can use templates to create dashboards by replacing dataset placeholders with datasets that follow the same schema that was used to create the source analysis and template. |
| POST | /accounts/{AwsAccountId}/templates/{TemplateId}/aliases/{AliasName} | Creates a template alias for a template. |
| POST | /accounts/{AwsAccountId}/themes/{ThemeId} | Creates a theme. A theme is set of configuration options for color and layout. Themes apply to analyses and dashboards. For more information, see Using Themes in Amazon QuickSight in the Amazon QuickSight User Guide. |
| POST | /accounts/{AwsAccountId}/themes/{ThemeId}/aliases/{AliasName} | Creates a theme alias for a theme. |
| POST | /accounts/{AwsAccountId}/topics | Creates a new Q topic. |
| POST | /accounts/{AwsAccountId}/topics/{TopicId}/schedules | Creates a topic refresh schedule. |
| POST | /accounts/{AwsAccountId}/vpc-connections | Creates a new VPC connection. |
| DELETE | /accounts/{AwsAccountId}/customizations | Deletes all Amazon QuickSight customizations in this Amazon Web Services Region for the specified Amazon Web Services account and Amazon QuickSight namespace. |
| DELETE | /accounts/{AwsAccountId}/analyses/{AnalysisId} | Deletes an analysis from Amazon QuickSight. You can optionally include a recovery window during which you can restore the analysis. If you don't specify a recovery window value, the operation defaults to 30 days. Amazon QuickSight attaches a DeletionTime stamp to the response that specifies the end of the recovery window. At the end of the recovery window, Amazon QuickSight deletes the analysis permanently. At any time before recovery window ends, you can use the RestoreAnalysis API operation to remove the DeletionTime stamp and cancel the deletion of the analysis. The analysis remains visible in the API until it's deleted, so you can describe it but you can't make a template from it. An analysis that's scheduled for deletion isn't accessible in the Amazon QuickSight console. To access it in the console, restore it. Deleting an analysis doesn't delete the dashboards that you publish from it. |
| DELETE | /accounts/{AwsAccountId}/dashboards/{DashboardId} | Deletes a dashboard. |
| DELETE | /accounts/{AwsAccountId}/data-sets/{DataSetId} | Deletes a dataset. |
| DELETE | /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-properties | Deletes the dataset refresh properties of the dataset. |
| DELETE | /accounts/{AwsAccountId}/data-sources/{DataSourceId} | Deletes the data source permanently. This operation breaks all the datasets that reference the deleted data source. |
| DELETE | /accounts/{AwsAccountId}/folders/{FolderId} | Deletes an empty folder. |
| DELETE | /accounts/{AwsAccountId}/folders/{FolderId}/members/{MemberType}/{MemberId} | Removes an asset, such as a dashboard, analysis, or dataset, from a folder. |
| DELETE | /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName} | Removes a user group from Amazon QuickSight. |
| DELETE | /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName}/members/{MemberName} | Removes a user from a group so that the user is no longer a member of the group. |
| DELETE | /accounts/{AwsAccountId}/namespace/{Namespace}/iam-policy-assignments/{AssignmentName} | Deletes an existing IAM policy assignment. |
| DELETE | /accounts/{AwsAccountId}/identity-propagation-config/{Service} | Deletes all access scopes and authorized targets that are associated with a service from the Amazon QuickSight IAM Identity Center application. This operation is only supported for Amazon QuickSight accounts that use IAM Identity Center. |
| DELETE | /accounts/{AwsAccountId}/namespaces/{Namespace} | Deletes a namespace and the users and groups that are associated with the namespace. This is an asynchronous process. Assets including dashboards, analyses, datasets and data sources are not deleted. To delete these assets, you use the API operations for the relevant asset. |
| DELETE | /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-schedules/{ScheduleId} | Deletes a refresh schedule from a dataset. |
| DELETE | /accounts/{AwsAccountId}/namespaces/{Namespace}/roles/{Role}/custom-permission | Removes custom permissions from the role. |
| DELETE | /accounts/{AwsAccountId}/namespaces/{Namespace}/roles/{Role}/members/{MemberName} | Removes a group from a role. |
| DELETE | /accounts/{AwsAccountId}/templates/{TemplateId} | Deletes a template. |
| DELETE | /accounts/{AwsAccountId}/templates/{TemplateId}/aliases/{AliasName} | Deletes the item that the specified template alias points to. If you provide a specific alias, you delete the version of the template that the alias points to. |
| DELETE | /accounts/{AwsAccountId}/themes/{ThemeId} | Deletes a theme. |
| DELETE | /accounts/{AwsAccountId}/themes/{ThemeId}/aliases/{AliasName} | Deletes the version of the theme that the specified theme alias points to. If you provide a specific alias, you delete the version of the theme that the alias points to. |
| DELETE | /accounts/{AwsAccountId}/topics/{TopicId} | Deletes a topic. |
| DELETE | /accounts/{AwsAccountId}/topics/{TopicId}/schedules/{DatasetId} | Deletes a topic refresh schedule. |
| DELETE | /accounts/{AwsAccountId}/namespaces/{Namespace}/users/{UserName} | Deletes the Amazon QuickSight user that is associated with the identity of the IAM user or role that's making the call. The IAM user isn't deleted as a result of this call. |
| DELETE | /accounts/{AwsAccountId}/namespaces/{Namespace}/user-principals/{PrincipalId} | Deletes a user identified by its principal ID. |
| DELETE | /accounts/{AwsAccountId}/vpc-connections/{VPCConnectionId} | Deletes a VPC connection. |
| GET | /accounts/{AwsAccountId}/customizations | Describes the customizations associated with the provided Amazon Web Services account and Amazon Amazon QuickSight namespace in an Amazon Web Services Region. The Amazon QuickSight console evaluates which customizations to apply by running this API operation with the Resolved flag included.  To determine what customizations display when you run this command, it can help to visualize the relationship of the entities involved.     Amazon Web Services account - The Amazon Web Services account exists at the top of the hierarchy. It has the potential to use all of the Amazon Web Services Regions and Amazon Web Services Services. When you subscribe to Amazon QuickSight, you choose one Amazon Web Services Region to use as your home Region. That's where your free SPICE capacity is located. You can use Amazon QuickSight in any supported Amazon Web Services Region.     Amazon Web Services Region - In each Amazon Web Services Region where you sign in to Amazon QuickSight at least once, Amazon QuickSight acts as a separate instance of the same service. If you have a user directory, it resides in us-east-1, which is the US East (N. Virginia). Generally speaking, these users have access to Amazon QuickSight in any Amazon Web Services Region, unless they are constrained to a namespace.  To run the command in a different Amazon Web Services Region, you change your Region settings. If you're using the CLI, you can use one of the following options:   Use command line options.    Use named profiles.    Run aws configure to change your default Amazon Web Services Region. Use Enter to key the same settings for your keys. For more information, see Configuring the CLI.      Namespace - A QuickSight namespace is a partition that contains users and assets (data sources, datasets, dashboards, and so on). To access assets that are in a specific namespace, users and groups must also be part of the same namespace. People who share a namespace are completely isolated from users and assets in other namespaces, even if they are in the same Amazon Web Services account and Amazon Web Services Region.    Applied customizations - Within an Amazon Web Services Region, a set of Amazon QuickSight customizations can apply to an Amazon Web Services account or to a namespace. Settings that you apply to a namespace override settings that you apply to an Amazon Web Services account. All settings are isolated to a single Amazon Web Services Region. To apply them in other Amazon Web Services Regions, run the CreateAccountCustomization command in each Amazon Web Services Region where you want to apply the same customizations. |
| GET | /accounts/{AwsAccountId}/settings | Describes the settings that were used when your Amazon QuickSight subscription was first created in this Amazon Web Services account. |
| GET | /accounts/{AwsAccountId}/analyses/{AnalysisId} | Provides a summary of the metadata for an analysis. |
| GET | /accounts/{AwsAccountId}/analyses/{AnalysisId}/definition | Provides a detailed description of the definition of an analysis.  If you do not need to know details about the content of an Analysis, for instance if you are trying to check the status of a recently created or updated Analysis, use the  DescribeAnalysis  instead. |
| GET | /accounts/{AwsAccountId}/analyses/{AnalysisId}/permissions | Provides the read and write permissions for an analysis. |
| GET | /accounts/{AwsAccountId}/asset-bundle-export-jobs/{AssetBundleExportJobId} | Describes an existing export job. Poll job descriptions after a job starts to know the status of the job. When a job succeeds, a URL is provided to download the exported assets' data from. Download URLs are valid for five minutes after they are generated. You can call the DescribeAssetBundleExportJob API for a new download URL as needed. Job descriptions are available for 14 days after the job starts. |
| GET | /accounts/{AwsAccountId}/asset-bundle-import-jobs/{AssetBundleImportJobId} | Describes an existing import job. Poll job descriptions after starting a job to know when it has succeeded or failed. Job descriptions are available for 14 days after job starts. |
| GET | /accounts/{AwsAccountId}/dashboards/{DashboardId} | Provides a summary for a dashboard. |
| GET | /accounts/{AwsAccountId}/dashboards/{DashboardId}/definition | Provides a detailed description of the definition of a dashboard.  If you do not need to know details about the content of a dashboard, for instance if you are trying to check the status of a recently created or updated dashboard, use the  DescribeDashboard  instead. |
| GET | /accounts/{AwsAccountId}/dashboards/{DashboardId}/permissions | Describes read and write permissions for a dashboard. |
| GET | /accounts/{AwsAccountId}/dashboards/{DashboardId}/snapshot-jobs/{SnapshotJobId} | Describes an existing snapshot job. Poll job descriptions after a job starts to know the status of the job. For information on available status codes, see JobStatus. |
| GET | /accounts/{AwsAccountId}/dashboards/{DashboardId}/snapshot-jobs/{SnapshotJobId}/result | Describes the result of an existing snapshot job that has finished running. A finished snapshot job will return a COMPLETED or FAILED status when you poll the job with a DescribeDashboardSnapshotJob API call. If the job has not finished running, this operation returns a message that says Dashboard Snapshot Job with id &lt;SnapshotjobId&gt; has not reached a terminal state.. |
| GET | /accounts/{AwsAccountId}/data-sets/{DataSetId} | Describes a dataset. This operation doesn't support datasets that include uploaded files as a source. |
| GET | /accounts/{AwsAccountId}/data-sets/{DataSetId}/permissions | Describes the permissions on a dataset. The permissions resource is arn:aws:quicksight:region:aws-account-id:dataset/data-set-id. |
| GET | /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-properties | Describes the refresh properties of a dataset. |
| GET | /accounts/{AwsAccountId}/data-sources/{DataSourceId} | Describes a data source. |
| GET | /accounts/{AwsAccountId}/data-sources/{DataSourceId}/permissions | Describes the resource permissions for a data source. |
| GET | /accounts/{AwsAccountId}/folders/{FolderId} | Describes a folder. |
| GET | /accounts/{AwsAccountId}/folders/{FolderId}/permissions | Describes permissions for a folder. |
| GET | /accounts/{AwsAccountId}/folders/{FolderId}/resolved-permissions | Describes the folder resolved permissions. Permissions consists of both folder direct permissions and the inherited permissions from the ancestor folders. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName} | Returns an Amazon QuickSight group's description and Amazon Resource Name (ARN). |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName}/members/{MemberName} | Use the DescribeGroupMembership operation to determine if a user is a member of the specified group. If the user exists and is a member of the specified group, an associated GroupMember object is returned. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/iam-policy-assignments/{AssignmentName} | Describes an existing IAM policy assignment, as specified by the assignment name. |
| GET | /accounts/{AwsAccountId}/data-sets/{DataSetId}/ingestions/{IngestionId} | Describes a SPICE ingestion. |
| GET | /accounts/{AwsAccountId}/ip-restriction | Provides a summary and status of IP rules. |
| GET | /accounts/{AwsAccountId}/key-registration | Describes all customer managed key registrations in a Amazon QuickSight account. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace} | Describes the current namespace. |
| GET | /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-schedules/{ScheduleId} | Provides a summary of a refresh schedule. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/roles/{Role}/custom-permission | Describes all custom permissions that are mapped to a role. |
| GET | /accounts/{AwsAccountId}/templates/{TemplateId} | Describes a template's metadata. |
| GET | /accounts/{AwsAccountId}/templates/{TemplateId}/aliases/{AliasName} | Describes the template alias for a template. |
| GET | /accounts/{AwsAccountId}/templates/{TemplateId}/definition | Provides a detailed description of the definition of a template.  If you do not need to know details about the content of a template, for instance if you are trying to check the status of a recently created or updated template, use the  DescribeTemplate  instead. |
| GET | /accounts/{AwsAccountId}/templates/{TemplateId}/permissions | Describes read and write permissions on a template. |
| GET | /accounts/{AwsAccountId}/themes/{ThemeId} | Describes a theme. |
| GET | /accounts/{AwsAccountId}/themes/{ThemeId}/aliases/{AliasName} | Describes the alias for a theme. |
| GET | /accounts/{AwsAccountId}/themes/{ThemeId}/permissions | Describes the read and write permissions for a theme. |
| GET | /accounts/{AwsAccountId}/topics/{TopicId} | Describes a topic. |
| GET | /accounts/{AwsAccountId}/topics/{TopicId}/permissions | Describes the permissions of a topic. |
| GET | /accounts/{AwsAccountId}/topics/{TopicId}/refresh/{RefreshId} | Describes the status of a topic refresh. |
| GET | /accounts/{AwsAccountId}/topics/{TopicId}/schedules/{DatasetId} | Deletes a topic refresh schedule. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/users/{UserName} | Returns information about a user, given the user name. |
| GET | /accounts/{AwsAccountId}/vpc-connections/{VPCConnectionId} | Describes a VPC connection. |
| POST | /accounts/{AwsAccountId}/embed-url/anonymous-user | Generates an embed URL that you can use to embed an Amazon QuickSight dashboard or visual in your website, without having to register any reader users. Before you use this action, make sure that you have configured the dashboards and permissions. The following rules apply to the generated URL:   It contains a temporary bearer token. It is valid for 5 minutes after it is generated. Once redeemed within this period, it cannot be re-used again.   The URL validity period should not be confused with the actual session lifetime that can be customized using the  SessionLifetimeInMinutes  parameter. The resulting user session is valid for 15 minutes (minimum) to 10 hours (maximum). The default session duration is 10 hours.   You are charged only when the URL is used or there is interaction with Amazon QuickSight.   For more information, see Embedded Analytics in the Amazon QuickSight User Guide. For more information about the high-level steps for embedding and for an interactive demo of the ways you can customize embedding, visit the Amazon QuickSight Developer Portal. |
| POST | /accounts/{AwsAccountId}/embed-url/registered-user | Generates an embed URL that you can use to embed an Amazon QuickSight experience in your website. This action can be used for any type of user registered in an Amazon QuickSight account. Before you use this action, make sure that you have configured the relevant Amazon QuickSight resource and permissions. The following rules apply to the generated URL:   It contains a temporary bearer token. It is valid for 5 minutes after it is generated. Once redeemed within this period, it cannot be re-used again.   The URL validity period should not be confused with the actual session lifetime that can be customized using the  SessionLifetimeInMinutes  parameter. The resulting user session is valid for 15 minutes (minimum) to 10 hours (maximum). The default session duration is 10 hours.   You are charged only when the URL is used or there is interaction with Amazon QuickSight.   For more information, see Embedded Analytics in the Amazon QuickSight User Guide. For more information about the high-level steps for embedding and for an interactive demo of the ways you can customize embedding, visit the Amazon QuickSight Developer Portal. |
| GET | /accounts/{AwsAccountId}/dashboards/{DashboardId}/embed-url | Generates a temporary session URL and authorization code(bearer token) that you can use to embed an Amazon QuickSight read-only dashboard in your website or application. Before you use this command, make sure that you have configured the dashboards and permissions.  Currently, you can use GetDashboardEmbedURL only from the server, not from the user's browser. The following rules apply to the generated URL:   They must be used together.   They can be used one time only.   They are valid for 5 minutes after you run this command.   You are charged only when the URL is used or there is interaction with Amazon QuickSight.   The resulting user session is valid for 15 minutes (default) up to 10 hours (maximum). You can use the optional SessionLifetimeInMinutes parameter to customize session duration.   For more information, see Embedding Analytics Using GetDashboardEmbedUrl in the Amazon QuickSight User Guide. For more information about the high-level steps for embedding and for an interactive demo of the ways you can customize embedding, visit the Amazon QuickSight Developer Portal. |
| GET | /accounts/{AwsAccountId}/session-embed-url | Generates a session URL and authorization code that you can use to embed the Amazon Amazon QuickSight console in your web server code. Use GetSessionEmbedUrl where you want to provide an authoring portal that allows users to create data sources, datasets, analyses, and dashboards. The users who access an embedded Amazon QuickSight console need belong to the author or admin security cohort. If you want to restrict permissions to some of these features, add a custom permissions profile to the user with the  UpdateUser  API operation. Use  RegisterUser  API operation to add a new user with a custom permission profile attached. For more information, see the following sections in the Amazon QuickSight User Guide:    Embedding Analytics     Customizing Access to the Amazon QuickSight Console |
| GET | /accounts/{AwsAccountId}/analyses | Lists Amazon QuickSight analyses that exist in the specified Amazon Web Services account. |
| GET | /accounts/{AwsAccountId}/asset-bundle-export-jobs | Lists all asset bundle export jobs that have been taken place in the last 14 days. Jobs created more than 14 days ago are deleted forever and are not returned. If you are using the same job ID for multiple jobs, ListAssetBundleExportJobs only returns the most recent job that uses the repeated job ID. |
| GET | /accounts/{AwsAccountId}/asset-bundle-import-jobs | Lists all asset bundle import jobs that have taken place in the last 14 days. Jobs created more than 14 days ago are deleted forever and are not returned. If you are using the same job ID for multiple jobs, ListAssetBundleImportJobs only returns the most recent job that uses the repeated job ID. |
| GET | /accounts/{AwsAccountId}/dashboards/{DashboardId}/versions | Lists all the versions of the dashboards in the Amazon QuickSight subscription. |
| GET | /accounts/{AwsAccountId}/dashboards | Lists dashboards in an Amazon Web Services account. |
| GET | /accounts/{AwsAccountId}/data-sets | Lists all of the datasets belonging to the current Amazon Web Services account in an Amazon Web Services Region. The permissions resource is arn:aws:quicksight:region:aws-account-id:dataset/*. |
| GET | /accounts/{AwsAccountId}/data-sources | Lists data sources in current Amazon Web Services Region that belong to this Amazon Web Services account. |
| GET | /accounts/{AwsAccountId}/folders/{FolderId}/members | List all assets (DASHBOARD, ANALYSIS, and DATASET) in a folder. |
| GET | /accounts/{AwsAccountId}/folders | Lists all folders in an account. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName}/members | Lists member users in a group. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/groups | Lists all user groups in Amazon QuickSight. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/v2/iam-policy-assignments | Lists the IAM policy assignments in the current Amazon QuickSight account. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/users/{UserName}/iam-policy-assignments | Lists all of the IAM policy assignments, including the Amazon Resource Names (ARNs), for the IAM policies assigned to the specified user and group, or groups that the user belongs to. |
| GET | /accounts/{AwsAccountId}/identity-propagation-config | Lists all services and authorized targets that the Amazon QuickSight IAM Identity Center application can access. This operation is only supported for Amazon QuickSight accounts that use IAM Identity Center. |
| GET | /accounts/{AwsAccountId}/data-sets/{DataSetId}/ingestions | Lists the history of SPICE ingestions for a dataset. |
| GET | /accounts/{AwsAccountId}/namespaces | Lists the namespaces for the specified Amazon Web Services account. This operation doesn't list deleted namespaces. |
| GET | /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-schedules | Lists the refresh schedules of a dataset. Each dataset can have up to 5 schedules. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/roles/{Role}/members | Lists all groups that are associated with a role. |
| GET | /accounts/{AwsAccountId}/templates/{TemplateId}/aliases | Lists all the aliases of a template. |
| GET | /accounts/{AwsAccountId}/templates/{TemplateId}/versions | Lists all the versions of the templates in the current Amazon QuickSight account. |
| GET | /accounts/{AwsAccountId}/templates | Lists all the templates in the current Amazon QuickSight account. |
| GET | /accounts/{AwsAccountId}/themes/{ThemeId}/aliases | Lists all the aliases of a theme. |
| GET | /accounts/{AwsAccountId}/themes/{ThemeId}/versions | Lists all the versions of the themes in the current Amazon Web Services account. |
| GET | /accounts/{AwsAccountId}/themes | Lists all the themes in the current Amazon Web Services account. |
| GET | /accounts/{AwsAccountId}/topics/{TopicId}/schedules | Lists all of the refresh schedules for a topic. |
| GET | /accounts/{AwsAccountId}/topics/{TopicId}/reviewed-answers | Lists all reviewed answers for a Q Topic. |
| GET | /accounts/{AwsAccountId}/topics | Lists all of the topics within an account. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/users/{UserName}/groups | Lists the Amazon QuickSight groups that an Amazon QuickSight user is a member of. |
| GET | /accounts/{AwsAccountId}/namespaces/{Namespace}/users | Returns a list of all of the Amazon QuickSight users belonging to this account. |
| GET | /accounts/{AwsAccountId}/vpc-connections | Lists all of the VPC connections in the current set Amazon Web Services Region of an Amazon Web Services account. |
| PUT | /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-properties | Creates or updates the dataset refresh properties for the dataset. |
| POST | /accounts/{AwsAccountId}/namespaces/{Namespace}/users | Creates an Amazon QuickSight user whose identity is associated with the Identity and Access Management (IAM) identity or role specified in the request. When you register a new user from the Amazon QuickSight API, Amazon QuickSight generates a registration URL. The user accesses this registration URL to create their account. Amazon QuickSight doesn't send a registration email to users who are registered from the Amazon QuickSight API. If you want new users to receive a registration email, then add those users in the Amazon QuickSight console. For more information on registering a new user in the Amazon QuickSight console, see  Inviting users to access Amazon QuickSight. |
| POST | /accounts/{AwsAccountId}/restore/analyses/{AnalysisId} | Restores an analysis. |
| POST | /accounts/{AwsAccountId}/search/analyses | Searches for analyses that belong to the user specified in the filter.  This operation is eventually consistent. The results are best effort and may not reflect very recent updates and changes. |
| POST | /accounts/{AwsAccountId}/search/dashboards | Searches for dashboards that belong to a user.   This operation is eventually consistent. The results are best effort and may not reflect very recent updates and changes. |
| POST | /accounts/{AwsAccountId}/search/data-sets | Use the SearchDataSets operation to search for datasets that belong to an account. |
| POST | /accounts/{AwsAccountId}/search/data-sources | Use the SearchDataSources operation to search for data sources that belong to an account. |
| POST | /accounts/{AwsAccountId}/search/folders | Searches the subfolders in a folder. |
| POST | /accounts/{AwsAccountId}/namespaces/{Namespace}/groups-search | Use the SearchGroups operation to search groups in a specified Amazon QuickSight namespace using the supplied filters. |
| POST | /accounts/{AwsAccountId}/asset-bundle-export-jobs/export | Starts an Asset Bundle export job. An Asset Bundle export job exports specified Amazon QuickSight assets. You can also choose to export any asset dependencies in the same job. Export jobs run asynchronously and can be polled with a DescribeAssetBundleExportJob API call. When a job is successfully completed, a download URL that contains the exported assets is returned. The URL is valid for 5 minutes and can be refreshed with a DescribeAssetBundleExportJob API call. Each Amazon QuickSight account can run up to 5 export jobs concurrently. The API caller must have the necessary permissions in their IAM role to access each resource before the resources can be exported. |
| POST | /accounts/{AwsAccountId}/asset-bundle-import-jobs/import | Starts an Asset Bundle import job. An Asset Bundle import job imports specified Amazon QuickSight assets into an Amazon QuickSight account. You can also choose to import a naming prefix and specified configuration overrides. The assets that are contained in the bundle file that you provide are used to create or update a new or existing asset in your Amazon QuickSight account. Each Amazon QuickSight account can run up to 5 import jobs concurrently. The API caller must have the necessary "create", "describe", and "update" permissions in their IAM role to access each resource type that is contained in the bundle file before the resources can be imported. |
| POST | /accounts/{AwsAccountId}/dashboards/{DashboardId}/snapshot-jobs | Starts an asynchronous job that generates a snapshot of a dashboard's output. You can request one or several of the following format configurations in each API call.   1 Paginated PDF   1 Excel workbook that includes up to 5 table or pivot table visuals   5 CSVs from table or pivot table visuals   The status of a submitted job can be polled with the DescribeDashboardSnapshotJob API. When you call the DescribeDashboardSnapshotJob API, check the JobStatus field in the response. Once the job reaches a COMPLETED or FAILED status, use the DescribeDashboardSnapshotJobResult API to obtain the URLs for the generated files. If the job fails, the DescribeDashboardSnapshotJobResult API returns detailed information about the error that occurred.  StartDashboardSnapshotJob API throttling  Amazon QuickSight utilizes API throttling to create a more consistent user experience within a time span for customers when they call the StartDashboardSnapshotJob. By default, 12 jobs can run simlutaneously in one Amazon Web Services account and users can submit up 10 API requests per second before an account is throttled. If an overwhelming number of API requests are made by the same user in a short period of time, Amazon QuickSight throttles the API calls to maintin an optimal experience and reliability for all Amazon QuickSight users.  Common throttling scenarios  The following list provides information about the most commin throttling scenarios that can occur.    A large number of SnapshotExport API jobs are running simultaneously on an Amazon Web Services account. When a new StartDashboardSnapshotJob is created and there are already 12 jobs with the RUNNING status, the new job request fails and returns a LimitExceededException error. Wait for a current job to comlpete before you resubmit the new job.    A large number of API requests are submitted on an Amazon Web Services account. When a user makes more than 10 API calls to the Amazon QuickSight API in one second, a ThrottlingException is returned.   If your use case requires a higher throttling limit, contact your account admin or Amazon Web ServicesSupport to explore options to tailor a more optimal expereince for your account.  Best practices to handle throttling  If your use case projects high levels of API traffic, try to reduce the degree of frequency and parallelism of API calls as much as you can to avoid throttling. You can also perform a timing test to calculate an estimate for the total processing time of your projected load that stays within the throttling limits of the Amazon QuickSight APIs. For example, if your projected traffic is 100 snapshot jobs before 12:00 PM per day, start 12 jobs in parallel and measure the amount of time it takes to proccess all 12 jobs. Once you obtain the result, multiply the duration by 9, for example (12 minutes * 9 = 108 minutes). Use the new result to determine the latest time at which the jobs need to be started to meet your target deadline. The time that it takes to process a job can be impacted by the following factors:   The dataset type (Direct Query or SPICE).   The size of the dataset.   The complexity of the calculated fields that are used in the dashboard.   The number of visuals that are on a sheet.   The types of visuals that are on the sheet.   The number of formats and snapshots that are requested in the job configuration.   The size of the generated snapshots. |
| PUT | /accounts/{AwsAccountId}/customizations | Updates Amazon QuickSight customizations for the current Amazon Web Services Region. Currently, the only customization that you can use is a theme. You can use customizations for your Amazon Web Services account or, if you specify a namespace, for a Amazon QuickSight namespace instead. Customizations that apply to a namespace override customizations that apply to an Amazon Web Services account. To find out which customizations apply, use the DescribeAccountCustomization API operation. |
| PUT | /accounts/{AwsAccountId}/settings | Updates the Amazon QuickSight settings in your Amazon Web Services account. |
| PUT | /accounts/{AwsAccountId}/analyses/{AnalysisId} | Updates an analysis in Amazon QuickSight |
| PUT | /accounts/{AwsAccountId}/analyses/{AnalysisId}/permissions | Updates the read and write permissions for an analysis. |
| PUT | /accounts/{AwsAccountId}/dashboards/{DashboardId} | Updates a dashboard in an Amazon Web Services account.  Updating a Dashboard creates a new dashboard version but does not immediately publish the new version. You can update the published version of a dashboard by using the  UpdateDashboardPublishedVersion  API operation. |
| PUT | /accounts/{AwsAccountId}/dashboards/{DashboardId}/linked-entities | Updates the linked analyses on a dashboard. |
| PUT | /accounts/{AwsAccountId}/dashboards/{DashboardId}/permissions | Updates read and write permissions on a dashboard. |
| PUT | /accounts/{AwsAccountId}/dashboards/{DashboardId}/versions/{VersionNumber} | Updates the published version of a dashboard. |
| PUT | /accounts/{AwsAccountId}/data-sets/{DataSetId} | Updates a dataset. This operation doesn't support datasets that include uploaded files as a source. Partial updates are not supported by this operation. |
| POST | /accounts/{AwsAccountId}/data-sets/{DataSetId}/permissions | Updates the permissions on a dataset. The permissions resource is arn:aws:quicksight:region:aws-account-id:dataset/data-set-id. |
| PUT | /accounts/{AwsAccountId}/data-sources/{DataSourceId} | Updates a data source. |
| POST | /accounts/{AwsAccountId}/data-sources/{DataSourceId}/permissions | Updates the permissions to a data source. |
| PUT | /accounts/{AwsAccountId}/folders/{FolderId} | Updates the name of a folder. |
| PUT | /accounts/{AwsAccountId}/folders/{FolderId}/permissions | Updates permissions of a folder. |
| PUT | /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName} | Changes a group description. |
| PUT | /accounts/{AwsAccountId}/namespaces/{Namespace}/iam-policy-assignments/{AssignmentName} | Updates an existing IAM policy assignment. This operation updates only the optional parameter or parameters that are specified in the request. This overwrites all of the users included in Identities. |
| POST | /accounts/{AwsAccountId}/identity-propagation-config/{Service} | Adds or updates services and authorized targets to configure what the Amazon QuickSight IAM Identity Center application can access. This operation is only supported for Amazon QuickSight accounts using IAM Identity Center |
| POST | /accounts/{AwsAccountId}/ip-restriction | Updates the content and status of IP rules. Traffic from a source is allowed when the source satisfies either the IpRestrictionRule, VpcIdRestrictionRule, or VpcEndpointIdRestrictionRule. To use this operation, you must provide the entire map of rules. You can use the DescribeIpRestriction operation to get the current rule map. |
| POST | /accounts/{AwsAccountId}/key-registration | Updates a customer managed key in a Amazon QuickSight account. |
| PUT | /accounts/{AwsAccountId}/public-sharing-settings | Use the UpdatePublicSharingSettings operation to turn on or turn off the public sharing settings of an Amazon QuickSight dashboard. To use this operation, turn on session capacity pricing for your Amazon QuickSight account. Before you can turn on public sharing on your account, make sure to give public sharing permissions to an administrative user in the Identity and Access Management (IAM) console. For more information on using IAM with Amazon QuickSight, see Using Amazon QuickSight with IAM in the Amazon QuickSight User Guide. |
| PUT | /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-schedules | Updates a refresh schedule for a dataset. |
| PUT | /accounts/{AwsAccountId}/namespaces/{Namespace}/roles/{Role}/custom-permission | Updates the custom permissions that are associated with a role. |
| POST | /accounts/{AwsAccountId}/spice-capacity-configuration | Updates the SPICE capacity configuration for a Amazon QuickSight account. |
| PUT | /accounts/{AwsAccountId}/templates/{TemplateId} | Updates a template from an existing Amazon QuickSight analysis or another template. |
| PUT | /accounts/{AwsAccountId}/templates/{TemplateId}/aliases/{AliasName} | Updates the template alias of a template. |
| PUT | /accounts/{AwsAccountId}/templates/{TemplateId}/permissions | Updates the resource permissions for a template. |
| PUT | /accounts/{AwsAccountId}/themes/{ThemeId} | Updates a theme. |
| PUT | /accounts/{AwsAccountId}/themes/{ThemeId}/aliases/{AliasName} | Updates an alias of a theme. |
| PUT | /accounts/{AwsAccountId}/themes/{ThemeId}/permissions | Updates the resource permissions for a theme. Permissions apply to the action to grant or revoke permissions on, for example "quicksight:DescribeTheme". Theme permissions apply in groupings. Valid groupings include the following for the three levels of permissions, which are user, owner, or no permissions:    User    "quicksight:DescribeTheme"     "quicksight:DescribeThemeAlias"     "quicksight:ListThemeAliases"     "quicksight:ListThemeVersions"      Owner    "quicksight:DescribeTheme"     "quicksight:DescribeThemeAlias"     "quicksight:ListThemeAliases"     "quicksight:ListThemeVersions"     "quicksight:DeleteTheme"     "quicksight:UpdateTheme"     "quicksight:CreateThemeAlias"     "quicksight:DeleteThemeAlias"     "quicksight:UpdateThemeAlias"     "quicksight:UpdateThemePermissions"     "quicksight:DescribeThemePermissions"      To specify no permissions, omit the permissions list. |
| PUT | /accounts/{AwsAccountId}/topics/{TopicId} | Updates a topic. |
| PUT | /accounts/{AwsAccountId}/topics/{TopicId}/permissions | Updates the permissions of a topic. |
| PUT | /accounts/{AwsAccountId}/topics/{TopicId}/schedules/{DatasetId} | Updates a topic refresh schedule. |
| PUT | /accounts/{AwsAccountId}/namespaces/{Namespace}/users/{UserName} | Updates an Amazon QuickSight user. |
| PUT | /accounts/{AwsAccountId}/vpc-connections/{VPCConnectionId} | Updates a VPC connection. |

### account
| Method | Path | Description |
|--------|------|-------------|
| POST | /account/{AwsAccountId} | Creates an Amazon QuickSight account, or subscribes to Amazon QuickSight Q. The Amazon Web Services Region for the account is derived from what is configured in the CLI or SDK. Before you use this operation, make sure that you can connect to an existing Amazon Web Services account. If you don't have an Amazon Web Services account, see Sign up for Amazon Web Services in the Amazon QuickSight User Guide. The person who signs up for Amazon QuickSight needs to have the correct Identity and Access Management (IAM) permissions. For more information, see IAM Policy Examples for Amazon QuickSight in the Amazon QuickSight User Guide. If your IAM policy includes both the Subscribe and CreateAccountSubscription actions, make sure that both actions are set to Allow. If either action is set to Deny, the Deny action prevails and your API call fails. You can't pass an existing IAM role to access other Amazon Web Services services using this API operation. To pass your existing IAM role to Amazon QuickSight, see Passing IAM roles to Amazon QuickSight in the Amazon QuickSight User Guide. You can't set default resource access on the new account from the Amazon QuickSight API. Instead, add default resource access from the Amazon QuickSight console. For more information about setting default resource access to Amazon Web Services services, see Setting default resource access to Amazon Web Services services in the Amazon QuickSight User Guide. |
| DELETE | /account/{AwsAccountId} | Use the DeleteAccountSubscription operation to delete an Amazon QuickSight account. This operation will result in an error message if you have configured your account termination protection settings to True. To change this setting and delete your account, call the UpdateAccountSettings API and set the value of the TerminationProtectionEnabled parameter to False, then make another call to the DeleteAccountSubscription API. |
| GET | /account/{AwsAccountId} | Use the DescribeAccountSubscription operation to receive a description of an Amazon QuickSight account's subscription. A successful API call returns an AccountInfo object that includes an account's name, subscription status, authentication type, edition, and notification email address. |

### resources
| Method | Path | Description |
|--------|------|-------------|
| GET | /resources/{ResourceArn}/tags | Lists the tags assigned to a resource. |
| POST | /resources/{ResourceArn}/tags | Assigns one or more tags (key-value pairs) to the specified Amazon QuickSight resource.  Tags can help you organize and categorize your resources. You can also use them to scope user permissions, by granting a user permission to access or change only resources with certain tag values. You can use the TagResource operation with a resource that already has tags. If you specify a new tag key for the resource, this tag is appended to the list of tags associated with the resource. If you specify a tag key that is already associated with the resource, the new tag value that you specify replaces the previous value for that tag. You can associate as many as 50 tags with a resource. Amazon QuickSight supports tagging on data set, data source, dashboard, template, topic, and user.  Tagging for Amazon QuickSight works in a similar way to tagging for other Amazon Web Services services, except for the following:   Tags are used to track costs for users in Amazon QuickSight. You can't tag other resources that Amazon QuickSight costs are based on, such as storage capacoty (SPICE), session usage, alert consumption, or reporting units.   Amazon QuickSight doesn't currently support the tag editor for Resource Groups. |
| DELETE | /resources/{ResourceArn}/tags | Removes a tag or tags from a resource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a batch-create-reviewed-answer?" -> POST /accounts/{AwsAccountId}/topics/{TopicId}/batch-create-reviewed-answers
- "Create a batch-delete-reviewed-answer?" -> POST /accounts/{AwsAccountId}/topics/{TopicId}/batch-delete-reviewed-answers
- "Delete a ingestion?" -> DELETE /accounts/{AwsAccountId}/data-sets/{DataSetId}/ingestions/{IngestionId}
- "Create a customization?" -> POST /accounts/{AwsAccountId}/customizations
- "Create a data-set?" -> POST /accounts/{AwsAccountId}/data-sets
- "Create a data-source?" -> POST /accounts/{AwsAccountId}/data-sources
- "Update a member?" -> PUT /accounts/{AwsAccountId}/folders/{FolderId}/members/{MemberType}/{MemberId}
- "Create a group?" -> POST /accounts/{AwsAccountId}/namespaces/{Namespace}/groups
- "Update a member?" -> PUT /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName}/members/{MemberName}
- "Create a iam-policy-assignment?" -> POST /accounts/{AwsAccountId}/namespaces/{Namespace}/iam-policy-assignments/
- "Update a ingestion?" -> PUT /accounts/{AwsAccountId}/data-sets/{DataSetId}/ingestions/{IngestionId}
- "Create a refresh-schedule?" -> POST /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-schedules
- "Create a topic?" -> POST /accounts/{AwsAccountId}/topics
- "Create a schedule?" -> POST /accounts/{AwsAccountId}/topics/{TopicId}/schedules
- "Create a vpc-connection?" -> POST /accounts/{AwsAccountId}/vpc-connections
- "Delete a account?" -> DELETE /account/{AwsAccountId}
- "Delete a analysis?" -> DELETE /accounts/{AwsAccountId}/analyses/{AnalysisId}
- "Delete a dashboard?" -> DELETE /accounts/{AwsAccountId}/dashboards/{DashboardId}
- "Delete a data-set?" -> DELETE /accounts/{AwsAccountId}/data-sets/{DataSetId}
- "Delete a data-source?" -> DELETE /accounts/{AwsAccountId}/data-sources/{DataSourceId}
- "Delete a folder?" -> DELETE /accounts/{AwsAccountId}/folders/{FolderId}
- "Delete a member?" -> DELETE /accounts/{AwsAccountId}/folders/{FolderId}/members/{MemberType}/{MemberId}
- "Delete a group?" -> DELETE /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName}
- "Delete a member?" -> DELETE /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName}/members/{MemberName}
- "Delete a iam-policy-assignment?" -> DELETE /accounts/{AwsAccountId}/namespace/{Namespace}/iam-policy-assignments/{AssignmentName}
- "Delete a identity-propagation-config?" -> DELETE /accounts/{AwsAccountId}/identity-propagation-config/{Service}
- "Delete a namespace?" -> DELETE /accounts/{AwsAccountId}/namespaces/{Namespace}
- "Delete a refresh-schedule?" -> DELETE /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-schedules/{ScheduleId}
- "Delete a member?" -> DELETE /accounts/{AwsAccountId}/namespaces/{Namespace}/roles/{Role}/members/{MemberName}
- "Delete a template?" -> DELETE /accounts/{AwsAccountId}/templates/{TemplateId}
- "Delete a aliase?" -> DELETE /accounts/{AwsAccountId}/templates/{TemplateId}/aliases/{AliasName}
- "Delete a theme?" -> DELETE /accounts/{AwsAccountId}/themes/{ThemeId}
- "Delete a aliase?" -> DELETE /accounts/{AwsAccountId}/themes/{ThemeId}/aliases/{AliasName}
- "Delete a topic?" -> DELETE /accounts/{AwsAccountId}/topics/{TopicId}
- "Delete a schedule?" -> DELETE /accounts/{AwsAccountId}/topics/{TopicId}/schedules/{DatasetId}
- "Delete a user?" -> DELETE /accounts/{AwsAccountId}/namespaces/{Namespace}/users/{UserName}
- "Delete a user-principal?" -> DELETE /accounts/{AwsAccountId}/namespaces/{Namespace}/user-principals/{PrincipalId}
- "Delete a vpc-connection?" -> DELETE /accounts/{AwsAccountId}/vpc-connections/{VPCConnectionId}
- "List all customizations?" -> GET /accounts/{AwsAccountId}/customizations
- "List all settings?" -> GET /accounts/{AwsAccountId}/settings
- "Get account details?" -> GET /account/{AwsAccountId}
- "Get analysis details?" -> GET /accounts/{AwsAccountId}/analyses/{AnalysisId}
- "List all definition?" -> GET /accounts/{AwsAccountId}/analyses/{AnalysisId}/definition
- "List all permissions?" -> GET /accounts/{AwsAccountId}/analyses/{AnalysisId}/permissions
- "Get asset-bundle-export-job details?" -> GET /accounts/{AwsAccountId}/asset-bundle-export-jobs/{AssetBundleExportJobId}
- "Get asset-bundle-import-job details?" -> GET /accounts/{AwsAccountId}/asset-bundle-import-jobs/{AssetBundleImportJobId}
- "Get dashboard details?" -> GET /accounts/{AwsAccountId}/dashboards/{DashboardId}
- "List all definition?" -> GET /accounts/{AwsAccountId}/dashboards/{DashboardId}/definition
- "List all permissions?" -> GET /accounts/{AwsAccountId}/dashboards/{DashboardId}/permissions
- "Get snapshot-job details?" -> GET /accounts/{AwsAccountId}/dashboards/{DashboardId}/snapshot-jobs/{SnapshotJobId}
- "List all result?" -> GET /accounts/{AwsAccountId}/dashboards/{DashboardId}/snapshot-jobs/{SnapshotJobId}/result
- "Get data-set details?" -> GET /accounts/{AwsAccountId}/data-sets/{DataSetId}
- "List all permissions?" -> GET /accounts/{AwsAccountId}/data-sets/{DataSetId}/permissions
- "List all refresh-properties?" -> GET /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-properties
- "Get data-source details?" -> GET /accounts/{AwsAccountId}/data-sources/{DataSourceId}
- "List all permissions?" -> GET /accounts/{AwsAccountId}/data-sources/{DataSourceId}/permissions
- "Get folder details?" -> GET /accounts/{AwsAccountId}/folders/{FolderId}
- "List all permissions?" -> GET /accounts/{AwsAccountId}/folders/{FolderId}/permissions
- "List all resolved-permissions?" -> GET /accounts/{AwsAccountId}/folders/{FolderId}/resolved-permissions
- "Get group details?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName}
- "Get member details?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName}/members/{MemberName}
- "Get iam-policy-assignment details?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/iam-policy-assignments/{AssignmentName}
- "Get ingestion details?" -> GET /accounts/{AwsAccountId}/data-sets/{DataSetId}/ingestions/{IngestionId}
- "List all ip-restriction?" -> GET /accounts/{AwsAccountId}/ip-restriction
- "List all key-registration?" -> GET /accounts/{AwsAccountId}/key-registration
- "Get namespace details?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}
- "Get refresh-schedule details?" -> GET /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-schedules/{ScheduleId}
- "List all custom-permission?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/roles/{Role}/custom-permission
- "Get template details?" -> GET /accounts/{AwsAccountId}/templates/{TemplateId}
- "Get aliase details?" -> GET /accounts/{AwsAccountId}/templates/{TemplateId}/aliases/{AliasName}
- "List all definition?" -> GET /accounts/{AwsAccountId}/templates/{TemplateId}/definition
- "List all permissions?" -> GET /accounts/{AwsAccountId}/templates/{TemplateId}/permissions
- "Get theme details?" -> GET /accounts/{AwsAccountId}/themes/{ThemeId}
- "Get aliase details?" -> GET /accounts/{AwsAccountId}/themes/{ThemeId}/aliases/{AliasName}
- "List all permissions?" -> GET /accounts/{AwsAccountId}/themes/{ThemeId}/permissions
- "Get topic details?" -> GET /accounts/{AwsAccountId}/topics/{TopicId}
- "List all permissions?" -> GET /accounts/{AwsAccountId}/topics/{TopicId}/permissions
- "Get refresh details?" -> GET /accounts/{AwsAccountId}/topics/{TopicId}/refresh/{RefreshId}
- "Get schedule details?" -> GET /accounts/{AwsAccountId}/topics/{TopicId}/schedules/{DatasetId}
- "Get user details?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/users/{UserName}
- "Get vpc-connection details?" -> GET /accounts/{AwsAccountId}/vpc-connections/{VPCConnectionId}
- "Create a anonymous-user?" -> POST /accounts/{AwsAccountId}/embed-url/anonymous-user
- "Create a registered-user?" -> POST /accounts/{AwsAccountId}/embed-url/registered-user
- "List all embed-url?" -> GET /accounts/{AwsAccountId}/dashboards/{DashboardId}/embed-url
- "List all session-embed-url?" -> GET /accounts/{AwsAccountId}/session-embed-url
- "List all analyses?" -> GET /accounts/{AwsAccountId}/analyses
- "List all asset-bundle-export-jobs?" -> GET /accounts/{AwsAccountId}/asset-bundle-export-jobs
- "List all asset-bundle-import-jobs?" -> GET /accounts/{AwsAccountId}/asset-bundle-import-jobs
- "List all versions?" -> GET /accounts/{AwsAccountId}/dashboards/{DashboardId}/versions
- "List all dashboards?" -> GET /accounts/{AwsAccountId}/dashboards
- "List all data-sets?" -> GET /accounts/{AwsAccountId}/data-sets
- "List all data-sources?" -> GET /accounts/{AwsAccountId}/data-sources
- "List all members?" -> GET /accounts/{AwsAccountId}/folders/{FolderId}/members
- "List all folders?" -> GET /accounts/{AwsAccountId}/folders
- "List all members?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName}/members
- "List all groups?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/groups
- "List all iam-policy-assignments?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/v2/iam-policy-assignments
- "List all iam-policy-assignments?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/users/{UserName}/iam-policy-assignments
- "List all identity-propagation-config?" -> GET /accounts/{AwsAccountId}/identity-propagation-config
- "List all ingestions?" -> GET /accounts/{AwsAccountId}/data-sets/{DataSetId}/ingestions
- "List all namespaces?" -> GET /accounts/{AwsAccountId}/namespaces
- "List all refresh-schedules?" -> GET /accounts/{AwsAccountId}/data-sets/{DataSetId}/refresh-schedules
- "List all members?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/roles/{Role}/members
- "List all tags?" -> GET /resources/{ResourceArn}/tags
- "List all aliases?" -> GET /accounts/{AwsAccountId}/templates/{TemplateId}/aliases
- "List all versions?" -> GET /accounts/{AwsAccountId}/templates/{TemplateId}/versions
- "List all templates?" -> GET /accounts/{AwsAccountId}/templates
- "List all aliases?" -> GET /accounts/{AwsAccountId}/themes/{ThemeId}/aliases
- "List all versions?" -> GET /accounts/{AwsAccountId}/themes/{ThemeId}/versions
- "List all themes?" -> GET /accounts/{AwsAccountId}/themes
- "List all schedules?" -> GET /accounts/{AwsAccountId}/topics/{TopicId}/schedules
- "List all reviewed-answers?" -> GET /accounts/{AwsAccountId}/topics/{TopicId}/reviewed-answers
- "List all topics?" -> GET /accounts/{AwsAccountId}/topics
- "List all groups?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/users/{UserName}/groups
- "List all users?" -> GET /accounts/{AwsAccountId}/namespaces/{Namespace}/users
- "List all vpc-connections?" -> GET /accounts/{AwsAccountId}/vpc-connections
- "Create a user?" -> POST /accounts/{AwsAccountId}/namespaces/{Namespace}/users
- "Create a analysis?" -> POST /accounts/{AwsAccountId}/search/analyses
- "Create a dashboard?" -> POST /accounts/{AwsAccountId}/search/dashboards
- "Create a data-set?" -> POST /accounts/{AwsAccountId}/search/data-sets
- "Create a data-source?" -> POST /accounts/{AwsAccountId}/search/data-sources
- "Create a folder?" -> POST /accounts/{AwsAccountId}/search/folders
- "Create a groups-search?" -> POST /accounts/{AwsAccountId}/namespaces/{Namespace}/groups-search
- "Create a export?" -> POST /accounts/{AwsAccountId}/asset-bundle-export-jobs/export
- "Create a import?" -> POST /accounts/{AwsAccountId}/asset-bundle-import-jobs/import
- "Create a snapshot-job?" -> POST /accounts/{AwsAccountId}/dashboards/{DashboardId}/snapshot-jobs
- "Create a tag?" -> POST /resources/{ResourceArn}/tags
- "Update a analysis?" -> PUT /accounts/{AwsAccountId}/analyses/{AnalysisId}
- "Update a dashboard?" -> PUT /accounts/{AwsAccountId}/dashboards/{DashboardId}
- "Update a version?" -> PUT /accounts/{AwsAccountId}/dashboards/{DashboardId}/versions/{VersionNumber}
- "Update a data-set?" -> PUT /accounts/{AwsAccountId}/data-sets/{DataSetId}
- "Create a permission?" -> POST /accounts/{AwsAccountId}/data-sets/{DataSetId}/permissions
- "Update a data-source?" -> PUT /accounts/{AwsAccountId}/data-sources/{DataSourceId}
- "Create a permission?" -> POST /accounts/{AwsAccountId}/data-sources/{DataSourceId}/permissions
- "Update a folder?" -> PUT /accounts/{AwsAccountId}/folders/{FolderId}
- "Update a group?" -> PUT /accounts/{AwsAccountId}/namespaces/{Namespace}/groups/{GroupName}
- "Update a iam-policy-assignment?" -> PUT /accounts/{AwsAccountId}/namespaces/{Namespace}/iam-policy-assignments/{AssignmentName}
- "Create a ip-restriction?" -> POST /accounts/{AwsAccountId}/ip-restriction
- "Create a key-registration?" -> POST /accounts/{AwsAccountId}/key-registration
- "Create a spice-capacity-configuration?" -> POST /accounts/{AwsAccountId}/spice-capacity-configuration
- "Update a template?" -> PUT /accounts/{AwsAccountId}/templates/{TemplateId}
- "Update a aliase?" -> PUT /accounts/{AwsAccountId}/templates/{TemplateId}/aliases/{AliasName}
- "Update a theme?" -> PUT /accounts/{AwsAccountId}/themes/{ThemeId}
- "Update a aliase?" -> PUT /accounts/{AwsAccountId}/themes/{ThemeId}/aliases/{AliasName}
- "Update a topic?" -> PUT /accounts/{AwsAccountId}/topics/{TopicId}
- "Update a schedule?" -> PUT /accounts/{AwsAccountId}/topics/{TopicId}/schedules/{DatasetId}
- "Update a user?" -> PUT /accounts/{AwsAccountId}/namespaces/{Namespace}/users/{UserName}
- "Update a vpc-connection?" -> PUT /accounts/{AwsAccountId}/vpc-connections/{VPCConnectionId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
