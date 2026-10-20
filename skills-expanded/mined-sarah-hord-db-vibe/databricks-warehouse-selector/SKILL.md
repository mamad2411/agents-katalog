---
name: databricks-warehouse-selector
description: Select a warehouse to execute a Databricks SQL Query on
---


# Databricks Warehouse Selector Skill

Select the best warehouse to execute Databricks SQL Query on

### Instructions
1) If not previously done, use databricks-authentication to authenticate and use correct profile in commands
2) Identify the best warehouse by running `databricks warehouses list --profile=<profile> --output=json` and passing that output to the `select_warehouses.py` script to choose the best. 
3) If no warehouses, create one to use with the command `databricks warehouses create --name "warehouse$RANDOM" --enable-serverless-compute --cluster-size="Small" --profile=<profile>` 

### Scripts
- `/resources/select_warehouses.py` - Takes as input the stdin output of a databricks warehouses list command and returns a sorted list of best warehouse candidates. 
