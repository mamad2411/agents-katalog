---
name: aws-device-farm
description: "AWS Device Farm API skill. Use when working with AWS Device Farm for root. Covers 77 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Device Farm
API version: 2015-06-23

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

77 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates a device pool. |
| POST | / | Creates a profile that can be applied to one or more private fleet device instances. |
| POST | / | Creates a network profile. |
| POST | / | Creates a project. |
| POST | / | Specifies and starts a remote access session. |
| POST | / | Creates a Selenium testing project. Projects are used to track TestGridSession instances. |
| POST | / | Creates a signed, short-term URL that can be passed to a Selenium RemoteWebDriver constructor. |
| POST | / | Uploads an app or test scripts. |
| POST | / | Creates a configuration record in Device Farm for your Amazon Virtual Private Cloud (VPC) endpoint. |
| POST | / | Deletes a device pool given the pool ARN. Does not allow deletion of curated pools owned by the system. |
| POST | / | Deletes a profile that can be applied to one or more private device instances. |
| POST | / | Deletes a network profile. |
| POST | / | Deletes an AWS Device Farm project, given the project ARN.  Deleting this resource does not stop an in-progress run. |
| POST | / | Deletes a completed remote access session and its results. |
| POST | / | Deletes the run, given the run ARN.  Deleting this resource does not stop an in-progress run. |
| POST | / | Deletes a Selenium testing project and all content generated under it.   You cannot undo this operation.   You cannot delete a project if it has active sessions. |
| POST | / | Deletes an upload given the upload ARN. |
| POST | / | Deletes a configuration for your Amazon Virtual Private Cloud (VPC) endpoint. |
| POST | / | Returns the number of unmetered iOS or unmetered Android devices that have been purchased by the account. |
| POST | / | Gets information about a unique device type. |
| POST | / | Returns information about a device instance that belongs to a private device fleet. |
| POST | / | Gets information about a device pool. |
| POST | / | Gets information about compatibility with a device pool. |
| POST | / | Returns information about the specified instance profile. |
| POST | / | Gets information about a job. |
| POST | / | Returns information about a network profile. |
| POST | / | Gets the current status and future status of all offerings purchased by an AWS account. The response indicates how many offerings are currently available and the offerings that will be available in the next period. The API returns a NotEligible error if the user is not permitted to invoke the operation. If you must be able to invoke this operation, contact aws-devicefarm-support@amazon.com. |
| POST | / | Gets information about a project. |
| POST | / | Returns a link to a currently running remote access session. |
| POST | / | Gets information about a run. |
| POST | / | Gets information about a suite. |
| POST | / | Gets information about a test. |
| POST | / | Retrieves information about a Selenium testing project. |
| POST | / | A session is an instance of a browser created through a RemoteWebDriver with the URL from CreateTestGridUrlResult$url. You can use the following to look up sessions:   The session ARN (GetTestGridSessionRequest$sessionArn).   The project ARN and a session ID (GetTestGridSessionRequest$projectArn and GetTestGridSessionRequest$sessionId). |
| POST | / | Gets information about an upload. |
| POST | / | Returns information about the configuration settings for your Amazon Virtual Private Cloud (VPC) endpoint. |
| POST | / | Installs an application to the device in a remote access session. For Android applications, the file must be in .apk format. For iOS applications, the file must be in .ipa format. |
| POST | / | Gets information about artifacts. |
| POST | / | Returns information about the private device instances associated with one or more AWS accounts. |
| POST | / | Gets information about device pools. |
| POST | / | Gets information about unique device types. |
| POST | / | Returns information about all the instance profiles in an AWS account. |
| POST | / | Gets information about jobs for a given test run. |
| POST | / | Returns the list of available network profiles. |
| POST | / | Returns a list of offering promotions. Each offering promotion record contains the ID and description of the promotion. The API returns a NotEligible error if the caller is not permitted to invoke the operation. Contact aws-devicefarm-support@amazon.com if you must be able to invoke this operation. |
| POST | / | Returns a list of all historical purchases, renewals, and system renewal transactions for an AWS account. The list is paginated and ordered by a descending timestamp (most recent transactions are first). The API returns a NotEligible error if the user is not permitted to invoke the operation. If you must be able to invoke this operation, contact aws-devicefarm-support@amazon.com. |
| POST | / | Returns a list of products or offerings that the user can manage through the API. Each offering record indicates the recurring price per unit and the frequency for that offering. The API returns a NotEligible error if the user is not permitted to invoke the operation. If you must be able to invoke this operation, contact aws-devicefarm-support@amazon.com. |
| POST | / | Gets information about projects. |
| POST | / | Returns a list of all currently running remote access sessions. |
| POST | / | Gets information about runs, given an AWS Device Farm project ARN. |
| POST | / | Gets information about samples, given an AWS Device Farm job ARN. |
| POST | / | Gets information about test suites for a given job. |
| POST | / | List the tags for an AWS Device Farm resource. |
| POST | / | Gets a list of all Selenium testing projects in your account. |
| POST | / | Returns a list of the actions taken in a TestGridSession. |
| POST | / | Retrieves a list of artifacts created during the session. |
| POST | / | Retrieves a list of sessions for a TestGridProject. |
| POST | / | Gets information about tests in a given test suite. |
| POST | / | Gets information about unique problems, such as exceptions or crashes. Unique problems are defined as a single instance of an error across a run, job, or suite. For example, if a call in your application consistently raises an exception (OutOfBoundsException in MyActivity.java:386), ListUniqueProblems returns a single entry instead of many individual entries for that exception. |
| POST | / | Gets information about uploads, given an AWS Device Farm project ARN. |
| POST | / | Returns information about all Amazon Virtual Private Cloud (VPC) endpoint configurations in the AWS account. |
| POST | / | Immediately purchases offerings for an AWS account. Offerings renew with the latest total purchased quantity for an offering, unless the renewal was overridden. The API returns a NotEligible error if the user is not permitted to invoke the operation. If you must be able to invoke this operation, contact aws-devicefarm-support@amazon.com. |
| POST | / | Explicitly sets the quantity of devices to renew for an offering, starting from the effectiveDate of the next period. The API returns a NotEligible error if the user is not permitted to invoke the operation. If you must be able to invoke this operation, contact aws-devicefarm-support@amazon.com. |
| POST | / | Schedules a run. |
| POST | / | Initiates a stop request for the current job. AWS Device Farm immediately stops the job on the device where tests have not started. You are not billed for this device. On the device where tests have started, setup suite and teardown suite tests run to completion on the device. You are billed for setup, teardown, and any tests that were in progress or already completed. |
| POST | / | Ends a specified remote access session. |
| POST | / | Initiates a stop request for the current test run. AWS Device Farm immediately stops the run on devices where tests have not started. You are not billed for these devices. On devices where tests have started executing, setup suite and teardown suite tests run to completion on those devices. You are billed for setup, teardown, and any tests that were in progress or already completed. |
| POST | / | Associates the specified tags to a resource with the specified resourceArn. If existing tags on a resource are not specified in the request parameters, they are not changed. When a resource is deleted, the tags associated with that resource are also deleted. |
| POST | / | Deletes the specified tags from a resource. |
| POST | / | Updates information about a private device instance. |
| POST | / | Modifies the name, description, and rules in a device pool given the attributes and the pool ARN. Rule updates are all-or-nothing, meaning they can only be updated as a whole (or not at all). |
| POST | / | Updates information about an existing private device instance profile. |
| POST | / | Updates the network profile. |
| POST | / | Modifies the specified project name, given the project ARN and a new name. |
| POST | / | Change details of a project. |
| POST | / | Updates an uploaded test spec. |
| POST | / | Updates information about an Amazon Virtual Private Cloud (VPC) endpoint configuration. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
