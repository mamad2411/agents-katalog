---
name: salesforce-authentication
description: This skill provides instructions for authenticating with salesforce before using sf cli or any salesforce work.
---


# Salesforce Authentication Skill

This skill ensures that you are authenticated correctly into Salesforce 


## Instructions
1) Run `sf org display` and check to see if `Connected Status` shows `Connected`. If so, we are authenticated already. Skip to step 5.
2) If that fails with a `NoDefaultEnvError` or `NamedOrgNotFoundError`, run `sf org list` to check if any orgs are authenticated. If an org is listed as `Connected`, set it as the default with `sf config set target-org <username> --global` using the username from the list.
3) If no orgs are authenticated, run `sf org login web --instance-url=https://databricks.my.salesforce.com/ --set-default` and ensure the user does SSO flow.
4) If the sf command is failing, run the `configure-vibe` skill to ensure the environment is setup correctly.
5) **Always ensure the Databricks org is set as the global default.** After authentication succeeds, run:
   ```bash
   sf config set target-org $(sf org display --json | jq -r '.result.username') --global
   ```
   This prevents `NoDefaultEnvError` in subsequent `sf` CLI commands across all skills.