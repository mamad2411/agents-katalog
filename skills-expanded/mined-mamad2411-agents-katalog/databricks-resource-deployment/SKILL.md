---
name: databricks-resource-deployment
description: Deploys resources (notebooks, jobs, clusters, warehouses, apps, databases/lakebase instances, catalogs, schemas) into an existing databricks workspace.  
---

# Databricks Resource Deployment Skill

Creates configuration files for databricks clusters, notebooks, jobs, apps, databases/lakebase instances, catalogs, schemas, and more. 

## Instructions
**IMPORTANT** Always PREFER deploying serverless resource when possible unless specifically instructed not to or the use case wouldn't work with serverless. Look at resources/SERVERLESS.md for instructions. **IMPORTANT**
**IMPORTANT** Always use the databricks-fe-vm-workspace-deployment skill for a workspace unless you can do the demo with e2-demo mentioned in the databricks-authentication skill.

1) If required, deploy a new databricks workspace using the databricks-fe-vm-workspace-deployment skill. If you need to deploy apps and/or databases/lakebase instances, you'll need to deploy a serverless workspace. If you need to demo specific workspace configurations or integrations with specific cloud resources, you'll need to use a deploy a classic workspace. Otherwise, you should try using the existing demo environments mentioned in the databricks-authentication skill. 
2) If not previously done, use databricks-authentication to authenticate to the relevant Databricks workspace and use correct profile in commands. 
3) If in a project directory with no other files, assume this is a new project. Otherwise, assume this is an existing project that is being changed - so read in the existing files to see what needs to be done. 

## Specific Resource
- For any demo relating to setting up a Snowflake integration, vended credentials, etc, use the fe-snowflake skill.

## Guidelines
1) To upload files, use the `databricks sync` command, as opposed to using import/export cli commands.
2) Always PREFER deploying serverless resource when possible unless specifically instructed not to or the use case wouldn't work with serverless. Look at resources/SERVERLESS.md for instructions.
3) You can use the web-devloop-tester subagent to navigate to the Databricks workspace in order to run any validation that you can't figure out how to do with the Databricks CLI
4) Never use DBFS to store things. Use Unity Catalog volumes (preferred) or S3. Don't use external locations for tables unless you absolutely have to.
5) Always use Unity Catalog. Never use Hive Metastore unless explicitly specified. Always use 3-layer namespaces.
6) In FE-VM environment, use the already created catalog instead of a new catalog if possible in order to avoid certain errors.
