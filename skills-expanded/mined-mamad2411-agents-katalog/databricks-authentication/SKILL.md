---
name: databricks-authentication
description: This skill provides instructions for authenticating with databricks. Do this before any databricks operations.
---


# Databricks Authentication Skill

This skill ensures that you are authenticated correctly into the correct Databricks environment using the Databricks CLI. 

###Workspace Environments
*IMPORTANT* For any use case/demo/etc that requires a Databricks App or Lakebase, you should use an fevm workspace. If someone talks about a workspace they created earlier, they likely mean this kind of workspace. Use the databricks-fe-vm-workspace to use or identify it*IMPORTANT*

These are the available Databricks workspace environments and their purpose:
- https://e2-demo-field-eng.cloud.databricks.com/ - This is the primary demo Workspace environment for Field Engineering. Typically when you are doing basic troubleshooting mostly scoped to Databricks, or building a quick Databricks-specific demo, this is the environment you should use. 
- https://adb-2548836972759138.18.azuredatabricks.net/ - This is the logfood environment, which you will ONLY use to run analytics queries on internal Databricks data.
- http://go/fevm - This is the FE Vending Machine, which is used to create net-new demo environments that can live for as long as 30 days. Create and/or use an already existing resource that you created previously by leveraging the databricks-fe-vm-workspace skill. 

###Account Environments
These are the available Databricks demo accounts. Generally you will use these to deploy new use cases for more advanced demos that require more control in both AWS and Azure. The url is always https://accounts.cloud.databricks.com. Below are the account IDs:
- 0d26daa6-5e44-4c97-a497-ef015f91254a - This is the AWS One Env Databricks Account for deploying serverless and classic workspaces in AWS. *ONLY USE THIS IF NONE OF THE OTHER WORKSPACE ENVIRONMENTS ARE SUITABLE FOR THE USE CASE OR DEMO* 

### Environment Profiles
Use the below profile names for each respective environment:
- e2-demo-west, https://e2-demo-field-eng.cloud.databricks.com/
- logfood, https://adb-2548836972759138.18.azuredatabricks.net/
- one-env-admin-aws, https://accounts.cloud.databricks.com, account ID = 0d26daa6-5e44-4c97-a497-ef015f91254a
- fe-vm-<name>, for a workspace created with FEVM. For example, if the name is vdm-serverless-6wo423, the profile name should be fe-vm-vdm-serverless-6wo423. 

### Authentication Process and Running Commands While Authenticated
Before executing any commands, ensure you are authenticated following these steps:
1) Identify the appropriate environment profile name for the task at hand. If none is specified or can't be inferred, default to `logfood` for queries on internal data, otherwise e2-demo-west for everything else
2) Run `databricks auth profiles | grep <profile>` and validate whether the profile exists and if it is valid (indicated by YES or NO). If valid, use the profile in subsequent commands with --profile=<profile>
3) If no valid profile for intended use case exists, for a WORKSPACE environment run `databricks auth login <host> --profile=<profile>` and ensure the user logs in with SSO.  
4) If the use case calls for leveraging an account and not a workspace, run `databricks auth login https://accounts.cloud.databricks.com --account-id=<account_id> --profile=<profile>`

### After Authentication
Typically you need to do something after authenticating. If creating a databricks demo, use the databricks-demo skill. If deploying databricks resources but possibly not as part of a demo, use the databricks-resource-deployment skill. To issue a query in logfood, use the logfood-querier skill.  
