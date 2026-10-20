---
name: aws-authentication
description: This skill provides instructions for authenticating with aws using aws cli
---

# AWS Authentication Skill

This skill ensures that you are authenticated correctly into the correct AWS environment using the aws CLI 

### Environment Profiles
Use the below profile names for each respective environment:
- aws-sandbox-field-eng_databricks-sandbox-admin, AWS Sandbox Environment. This is the profile to use when you require AWS resources as part of a Databricks demo or Databricks workspace deployment, or just for spinning up any arbitrary AWS resource

### Authentication Process and Running Commands While Authenticated
Before executing any commands, ensure you are authenticated following these steps:
1) Identify the appropriate environment profile name for the task at hand. If none is specified or can't be inferred, default to `aws-sandbox-field-eng_databricks-sandbox-admin`
2) Run `aws sts get-caller-identity --profile=<profile>` and validate whether the profile exists and if it is valid. If valid, use the profile in subsequent commands with `--profile=<profile>`
3) If the profile could not be found, the AWS config likely needs to be updated. **CRITICAL: Do NOT overwrite or clobber the user's existing `~/.aws/config` file.** The user may have custom profiles, SSO sessions, proxy settings, or other configuration that must be preserved. Follow these sub-steps:
   a) Download the full config to a temp file: `curl "https://aws-config.sec.databricks.us/full-config" --output /tmp/aws_config_full`
   b) If `~/.aws/config` does not exist, move the downloaded file into place: `mkdir -p ~/.aws && mv /tmp/aws_config_full ~/.aws/config`
   c) If `~/.aws/config` already exists, extract only the missing profile section from `/tmp/aws_config_full` and append it to the existing `~/.aws/config`. Use grep/awk or read the files to find the `[profile <name>]` block (including all lines until the next `[` section header) that is not already present, then append it with a newline separator.
   d) Clean up: `rm -f /tmp/aws_config_full`
   e) Retry step 2.
4) If the profile exists but the SSO session is expired or not authenticated, run `aws sso login --profile=<profile>` and ensure the user logs in with SSO.
5) If you are unable to login, attempt to run `configure-vibe`