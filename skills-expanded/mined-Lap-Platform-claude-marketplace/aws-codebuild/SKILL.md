---
name: aws-codebuild
description: "AWS CodeBuild API skill. Use when working with AWS CodeBuild for root. Covers 50 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS CodeBuild
API version: 2016-10-06

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

50 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Deletes one or more builds. |
| POST | / | Retrieves information about one or more batch builds. |
| POST | / | Gets information about one or more builds. |
| POST | / | Gets information about one or more compute fleets. |
| POST | / | Gets information about one or more build projects. |
| POST | / | Returns an array of report groups. |
| POST | / | Returns an array of reports. |
| POST | / | Creates a compute fleet. |
| POST | / | Creates a build project. |
| POST | / | Creates a report group. A report group contains a collection of reports. |
| POST | / | For an existing CodeBuild build project that has its source code stored in a GitHub or Bitbucket repository, enables CodeBuild to start rebuilding the source code every time a code change is pushed to the repository.  If you enable webhooks for an CodeBuild project, and the project is used as a build step in CodePipeline, then two identical builds are created for each commit. One build is triggered through webhooks, and one through CodePipeline. Because billing is on a per-build basis, you are billed for both builds. Therefore, if you are using CodePipeline, we recommend that you disable webhooks in CodeBuild. In the CodeBuild console, clear the Webhook box. For more information, see step 5 in Change a Build Project's Settings. |
| POST | / | Deletes a batch build. |
| POST | / | Deletes a compute fleet. When you delete a compute fleet, its builds are not deleted. |
| POST | / | Deletes a build project. When you delete a project, its builds are not deleted. |
| POST | / | Deletes a report. |
| POST | / | Deletes a report group. Before you delete a report group, you must delete its reports. |
| POST | / | Deletes a resource policy that is identified by its resource ARN. |
| POST | / | Deletes a set of GitHub, GitHub Enterprise, or Bitbucket source credentials. |
| POST | / | For an existing CodeBuild build project that has its source code stored in a GitHub or Bitbucket repository, stops CodeBuild from rebuilding the source code every time a code change is pushed to the repository. |
| POST | / | Retrieves one or more code coverage reports. |
| POST | / | Returns a list of details about test cases for a report. |
| POST | / | Analyzes and accumulates test report values for the specified test reports. |
| POST | / | Gets a resource policy that is identified by its resource ARN. |
| POST | / | Imports the source repository credentials for an CodeBuild project that has its source code stored in a GitHub, GitHub Enterprise, GitLab, GitLab Self Managed, or Bitbucket repository. |
| POST | / | Resets the cache for a project. |
| POST | / | Retrieves the identifiers of your build batches in the current region. |
| POST | / | Retrieves the identifiers of the build batches for a specific project. |
| POST | / | Gets a list of build IDs, with each build ID representing a single build. |
| POST | / | Gets a list of build identifiers for the specified build project, with each build identifier representing a single build. |
| POST | / | Gets information about Docker images that are managed by CodeBuild. |
| POST | / | Gets a list of compute fleet names with each compute fleet name representing a single compute fleet. |
| POST | / | Gets a list of build project names, with each build project name representing a single build project. |
| POST | / | Gets a list ARNs for the report groups in the current Amazon Web Services account. |
| POST | / | Returns a list of ARNs for the reports in the current Amazon Web Services account. |
| POST | / | Returns a list of ARNs for the reports that belong to a ReportGroup. |
| POST | / | Gets a list of projects that are shared with other Amazon Web Services accounts or users. |
| POST | / | Gets a list of report groups that are shared with other Amazon Web Services accounts or users. |
| POST | / | Returns a list of SourceCredentialsInfo objects. |
| POST | / | Stores a resource policy for the ARN of a Project or ReportGroup object. |
| POST | / | Restarts a build. |
| POST | / | Restarts a failed batch build. Only batch builds that have failed can be retried. |
| POST | / | Starts running a build with the settings defined in the project. These setting include: how to run a build, where to get the source code, which build environment to use, which build commands to run, and where to store the build output. You can also start a build run by overriding some of the build settings in the project. The overrides only apply for that specific start build request. The settings in the project are unaltered. |
| POST | / | Starts a batch build for a project. |
| POST | / | Attempts to stop running a build. |
| POST | / | Stops a running batch build. |
| POST | / | Updates a compute fleet. |
| POST | / | Changes the settings of a build project. |
| POST | / | Changes the public visibility for a project. The project's build results, logs, and artifacts are available to the general public. For more information, see Public build projects in the CodeBuild User Guide.  The following should be kept in mind when making your projects public:   All of a project's build results, logs, and artifacts, including builds that were run when the project was private, are available to the general public.   All build logs and artifacts are available to the public. Environment variables, source code, and other sensitive information may have been output to the build logs and artifacts. You must be careful about what information is output to the build logs. Some best practice are:   Do not store sensitive values in environment variables. We recommend that you use an Amazon EC2 Systems Manager Parameter Store or Secrets Manager to store sensitive values.   Follow Best practices for using webhooks in the CodeBuild User Guide to limit which entities can trigger a build, and do not store the buildspec in the project itself, to ensure that your webhooks are as secure as possible.     A malicious user can use public builds to distribute malicious artifacts. We recommend that you review all pull requests to verify that the pull request is a legitimate change. We also recommend that you validate any artifacts with their checksums to make sure that the correct artifacts are being downloaded. |
| POST | / | Updates a report group. |
| POST | / | Updates the webhook associated with an CodeBuild build project.    If you use Bitbucket for your repository, rotateSecret is ignored. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
