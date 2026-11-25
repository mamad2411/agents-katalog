---
name: databricks-demo
description: Create, deploy and run demos relating to or integrating with Databricks. 
---

# Databricks Demo Skill

Create, deploy and run demos relating to or integrating with Databricks.

## Instructions
A good demo will be use case and business relevant, exercise as many relevant features as possible.

**IMPORTANT** For deploying ANY DATABRICKS assets/resources that are not the workspace itself, use the databricks-resource-deployment skill. **IMPORTANT**

**IMPORTANT** Always use the databricks-fe-vm-workspace-deployment skill for a demo that requires any kind of integration or uses databricks apps. Otherwise, use the e2-demo workspace mentioned in the databricks-authentication skill. **IMPORTANT**

**IMPORTANT** Demos showing any kind of application will require Databricks Apps. Demos that require any low-latency state (e.g. not analytics use cases) will require Lakebase. Review resources/DATABRICKS_APPS.md before continuing if you will need a Databricks App **IMPORTANT**

**IMPORTANT** Use the databricks-apps-developer subagent to develop databricks apps. Use the web-devloop-tester subagent to perform the Databricks Apps devloop for UI validation **IMPORTANT**

1) Load any relevant skills before performing anything else as their instructions will be important for planning tasks. 
2) First check the current directory and see if it appears to be that of an existing demo with both a DEMO.md and TASKS.md file. If those files exist, read them in for brand guidelines and the desired demo state. If they exist and has all the details you need, you can skip upfront research as it's already been done. If they are missing and other code files exist, do the research required to create a DEMO.md and TASKS.md file as detailed in the next step, taking into account the code files that already exist. 
3) When given ambiguous instructions to create a demo relating to Databricks, you should first research the use case or customer mentioned (if a specific use case or customer) to determine the kind of data to use/generate and what kind of demo to build. Write out a DEMO.md file which should detail brand guidelines, use case(s) that are going to be built into the demo, an architecture for the demo and high-level components. Write out a TASKS.md file which contains the steps that need to be completed and their status. 
4) For any customer-facing demo or anything that will deploy lakebase or databricks apps, you need to use an fe-vm workspace. For quick prototyping, testing, or troubleshooting, use the e2-demo-west workspace mentioned in the databricks-authentication skill. Otherwise, attempt to deploy relevant base infrastructure if required using the databricks-fe-vm-workspace-deployment skill. 
5) Generate relevant data using referencing resources/DATA_GENERATION_SERVERLESS.md for instructions.
6) Always write and attempt to run the code locally first to make sure that it works BEFORE deploying it. Refer to resources/DATABRICKS_APPS.md for very important guidelines for the Databricks apps devloop.  
7) Deploy the actual code, schedule/start jobs, write to the database/tables etc - just generally deploy the actual demo and get it into a running state. Use the databricks-resource-deployment skill to understand configuring databricks apps and using databricks bundles.
8) As you complete tasks and/or add new ones, update TASKS.md.

## Guidelines
*ALWAYS* Follow the below guidelines when building demos and deploying resources:
1) If building for a specific customer, try to find their style guidelines and color schemes and use those in visuals
2) For python code, ALWAYS use `uv` to run local, build wheels, etc. Build wheels and copy them to the workspace if required/when referencing in bundles. Generate requirements.txt from pyproject.toml. *NEVER* use `pip` or `python` standalone without `uv`. 
3) See resources/DATA_GENERATION_SERVERLESS.md for data generation instructions
4) If the demo is showing some kind of application UI, you will need to create a Databricks App. See resources/DATABRICKS_APPS.md for critical guidelines. 
5) For llm/chatbot use cases, you need to use a Databricks-hosted model in your databricks workspace. You need to use one of the API querying options specified here: https://docs.databricks.com/aws/en/machine-learning/model-serving/score-foundation-models#-query-options. Use one of databricks-claude-sonnet-4-5, databricks-claude-sonnet-4 as the model.
6) Always use serverless resources unless specifically told not to. Use serverless client version 4 or greater. Never specify pyspark in serverless environment dependencies since it's already installed.
7) If the demo requires an integration with Snowflake, use the fe-snowflake skill.
8) Never use DBFS to store things. Use Unity Catalog volumes (preferred) or S3. Don't use external locations for tables unless you absolutely have to.
9) Always use Unity Catalog. Never use Hive Metastore unless explicitly specified. Always use 3-layer namespaces.
10) In FE-VM environment, use the already created catalog instead of a new catalog if possible in order to avoid certain errors.

