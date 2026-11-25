---
name: aws-transfer-family
description: "AWS Transfer Family API skill. Use when working with AWS Transfer Family for root. Covers 60 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Transfer Family
API version: 2018-11-05

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

60 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Used by administrators to choose which groups in the directory should have access to upload and download files over the enabled protocols using Transfer Family. For example, a Microsoft Active Directory might contain 50,000 users, but only a small fraction might need the ability to transfer files to the server. An administrator can use CreateAccess to limit the access to the correct set of users who need this ability. |
| POST | / | Creates an agreement. An agreement is a bilateral trading partner agreement, or partnership, between an Transfer Family server and an AS2 process. The agreement defines the file and message transfer relationship between the server and the AS2 process. To define an agreement, Transfer Family combines a server, local profile, partner profile, certificate, and other attributes. The partner is identified with the PartnerProfileId, and the AS2 process is identified with the LocalProfileId. |
| POST | / | Creates the connector, which captures the parameters for a connection for the AS2 or SFTP protocol. For AS2, the connector is required for sending files to an externally hosted AS2 server. For SFTP, the connector is required when sending files to an SFTP server or receiving files from an SFTP server. For more details about connectors, see Configure AS2 connectors and Create SFTP connectors.  You must specify exactly one configuration object: either for AS2 (As2Config) or SFTP (SftpConfig). |
| POST | / | Creates the local or partner profile to use for AS2 transfers. |
| POST | / | Instantiates an auto-scaling virtual server based on the selected file transfer protocol in Amazon Web Services. When you make updates to your file transfer protocol-enabled server or when you work with users, use the service-generated ServerId property that is assigned to the newly created server. |
| POST | / | Creates a user and associates them with an existing file transfer protocol-enabled server. You can only create and associate users with servers that have the IdentityProviderType set to SERVICE_MANAGED. Using parameters for CreateUser, you can specify the user name, set the home directory, store the user's public key, and assign the user's Identity and Access Management (IAM) role. You can also optionally add a session policy, and assign metadata with tags that can be used to group and search for users. |
| POST | / | Allows you to create a workflow with specified steps and step details the workflow invokes after file transfer completes. After creating a workflow, you can associate the workflow created with any transfer servers by specifying the workflow-details field in CreateServer and UpdateServer operations. |
| POST | / | Allows you to delete the access specified in the ServerID and ExternalID parameters. |
| POST | / | Delete the agreement that's specified in the provided AgreementId. |
| POST | / | Deletes the certificate that's specified in the CertificateId parameter. |
| POST | / | Deletes the connector that's specified in the provided ConnectorId. |
| POST | / | Deletes the host key that's specified in the HostKeyId parameter. |
| POST | / | Deletes the profile that's specified in the ProfileId parameter. |
| POST | / | Deletes the file transfer protocol-enabled server that you specify. No response returns from this operation. |
| POST | / | Deletes a user's Secure Shell (SSH) public key. |
| POST | / | Deletes the user belonging to a file transfer protocol-enabled server you specify. No response returns from this operation.  When you delete a user from a server, the user's information is lost. |
| POST | / | Deletes the specified workflow. |
| POST | / | Describes the access that is assigned to the specific file transfer protocol-enabled server, as identified by its ServerId property and its ExternalId. The response from this call returns the properties of the access that is associated with the ServerId value that was specified. |
| POST | / | Describes the agreement that's identified by the AgreementId. |
| POST | / | Describes the certificate that's identified by the CertificateId. |
| POST | / | Describes the connector that's identified by the ConnectorId. |
| POST | / | You can use DescribeExecution to check the details of the execution of the specified workflow.  This API call only returns details for in-progress workflows.  If you provide an ID for an execution that is not in progress, or if the execution doesn't match the specified workflow ID, you receive a ResourceNotFound exception. |
| POST | / | Returns the details of the host key that's specified by the HostKeyId and ServerId. |
| POST | / | Returns the details of the profile that's specified by the ProfileId. |
| POST | / | Describes the security policy that is attached to your server or SFTP connector. The response contains a description of the security policy's properties. For more information about security policies, see Working with security policies for servers or Working with security policies for SFTP connectors. |
| POST | / | Describes a file transfer protocol-enabled server that you specify by passing the ServerId parameter. The response contains a description of a server's properties. When you set EndpointType to VPC, the response will contain the EndpointDetails. |
| POST | / | Describes the user assigned to the specific file transfer protocol-enabled server, as identified by its ServerId property. The response from this call returns the properties of the user associated with the ServerId value that was specified. |
| POST | / | Describes the specified workflow. |
| POST | / | Imports the signing and encryption certificates that you need to create local (AS2) profiles and partner profiles. |
| POST | / | Adds a host key to the server that's specified by the ServerId parameter. |
| POST | / | Adds a Secure Shell (SSH) public key to a Transfer Family user identified by a UserName value assigned to the specific file transfer protocol-enabled server, identified by ServerId. The response returns the UserName value, the ServerId value, and the name of the SshPublicKeyId. |
| POST | / | Lists the details for all the accesses you have on your server. |
| POST | / | Returns a list of the agreements for the server that's identified by the ServerId that you supply. If you want to limit the results to a certain number, supply a value for the MaxResults parameter. If you ran the command previously and received a value for NextToken, you can supply that value to continue listing agreements from where you left off. |
| POST | / | Returns a list of the current certificates that have been imported into Transfer Family. If you want to limit the results to a certain number, supply a value for the MaxResults parameter. If you ran the command previously and received a value for the NextToken parameter, you can supply that value to continue listing certificates from where you left off. |
| POST | / | Lists the connectors for the specified Region. |
| POST | / | Lists all in-progress executions for the specified workflow.  If the specified workflow ID cannot be found, ListExecutions returns a ResourceNotFound exception. |
| POST | / | Returns a list of host keys for the server that's specified by the ServerId parameter. |
| POST | / | Returns a list of the profiles for your system. If you want to limit the results to a certain number, supply a value for the MaxResults parameter. If you ran the command previously and received a value for NextToken, you can supply that value to continue listing profiles from where you left off. |
| POST | / | Lists the security policies that are attached to your servers and SFTP connectors. For more information about security policies, see Working with security policies for servers or Working with security policies for SFTP connectors. |
| POST | / | Lists the file transfer protocol-enabled servers that are associated with your Amazon Web Services account. |
| POST | / | Lists all of the tags associated with the Amazon Resource Name (ARN) that you specify. The resource can be a user, server, or role. |
| POST | / | Lists the users for a file transfer protocol-enabled server that you specify by passing the ServerId parameter. |
| POST | / | Lists all workflows associated with your Amazon Web Services account for your current region. |
| POST | / | Sends a callback for asynchronous custom steps.  The ExecutionId, WorkflowId, and Token are passed to the target resource during execution of a custom step of a workflow. You must include those with their callback as well as providing a status. |
| POST | / | Retrieves a list of the contents of a directory from a remote SFTP server. You specify the connector ID, the output path, and the remote directory path. You can also specify the optional MaxItems value to control the maximum number of items that are listed from the remote directory. This API returns a list of all files and directories in the remote directory (up to the maximum value), but does not return files or folders in sub-directories. That is, it only returns a list of files and directories one-level deep. After you receive the listing file, you can provide the files that you want to transfer to the RetrieveFilePaths parameter of the StartFileTransfer API call. The naming convention for the output file is  connector-ID-listing-ID.json. The output file contains the following information:    filePath: the complete path of a remote file, relative to the directory of the listing request for your SFTP connector on the remote server.    modifiedTimestamp: the last time the file was modified, in UTC time format. This field is optional. If the remote file attributes don't contain a timestamp, it is omitted from the file listing.    size: the size of the file, in bytes. This field is optional. If the remote file attributes don't contain a file size, it is omitted from the file listing.    path: the complete path of a remote directory, relative to the directory of the listing request for your SFTP connector on the remote server.    truncated: a flag indicating whether the list output contains all of the items contained in the remote directory or not. If your Truncated output value is true, you can increase the value provided in the optional max-items input attribute to be able to list more items (up to the maximum allowed list size of 10,000 items). |
| POST | / | Begins a file transfer between local Amazon Web Services storage and a remote AS2 or SFTP server.   For an AS2 connector, you specify the ConnectorId and one or more SendFilePaths to identify the files you want to transfer.   For an SFTP connector, the file transfer can be either outbound or inbound. In both cases, you specify the ConnectorId. Depending on the direction of the transfer, you also specify the following items:   If you are transferring file from a partner's SFTP server to Amazon Web Services storage, you specify one or more RetrieveFilePaths to identify the files you want to transfer, and a LocalDirectoryPath to specify the destination folder.   If you are transferring file to a partner's SFTP server from Amazon Web Services storage, you specify one or more SendFilePaths to identify the files you want to transfer, and a RemoteDirectoryPath to specify the destination folder. |
| POST | / | Changes the state of a file transfer protocol-enabled server from OFFLINE to ONLINE. It has no impact on a server that is already ONLINE. An ONLINE server can accept and process file transfer jobs. The state of STARTING indicates that the server is in an intermediate state, either not fully able to respond, or not fully online. The values of START_FAILED can indicate an error condition. No response is returned from this call. |
| POST | / | Changes the state of a file transfer protocol-enabled server from ONLINE to OFFLINE. An OFFLINE server cannot accept and process file transfer jobs. Information tied to your server, such as server and user properties, are not affected by stopping your server.  Stopping the server does not reduce or impact your file transfer protocol endpoint billing; you must delete the server to stop being billed.  The state of STOPPING indicates that the server is in an intermediate state, either not fully able to respond, or not fully offline. The values of STOP_FAILED can indicate an error condition. No response is returned from this call. |
| POST | / | Attaches a key-value pair to a resource, as identified by its Amazon Resource Name (ARN). Resources are users, servers, roles, and other entities. There is no response returned from this call. |
| POST | / | Tests whether your SFTP connector is set up successfully. We highly recommend that you call this operation to test your ability to transfer files between local Amazon Web Services storage and a trading partner's SFTP server. |
| POST | / | If the IdentityProviderType of a file transfer protocol-enabled server is AWS_DIRECTORY_SERVICE or API_Gateway, tests whether your identity provider is set up successfully. We highly recommend that you call this operation to test your authentication method as soon as you create your server. By doing so, you can troubleshoot issues with the identity provider integration to ensure that your users can successfully use the service.  The ServerId and UserName parameters are required. The ServerProtocol, SourceIp, and UserPassword are all optional.  Note the following:    You cannot use TestIdentityProvider if the IdentityProviderType of your server is SERVICE_MANAGED.    TestIdentityProvider does not work with keys: it only accepts passwords.    TestIdentityProvider can test the password operation for a custom Identity Provider that handles keys and passwords.    If you provide any incorrect values for any parameters, the Response field is empty.     If you provide a server ID for a server that uses service-managed users, you get an error:    An error occurred (InvalidRequestException) when calling the TestIdentityProvider operation: s-server-ID not configured for external auth      If you enter a Server ID for the --server-id parameter that does not identify an actual Transfer server, you receive the following error:   An error occurred (ResourceNotFoundException) when calling the TestIdentityProvider operation: Unknown server.  It is possible your sever is in a different region. You can specify a region by adding the following: --region region-code, such as --region us-east-2 to specify a server in US East (Ohio). |
| POST | / | Detaches a key-value pair from a resource, as identified by its Amazon Resource Name (ARN). Resources are users, servers, roles, and other entities. No response is returned from this call. |
| POST | / | Allows you to update parameters for the access specified in the ServerID and ExternalID parameters. |
| POST | / | Updates some of the parameters for an existing agreement. Provide the AgreementId and the ServerId for the agreement that you want to update, along with the new values for the parameters to update. |
| POST | / | Updates the active and inactive dates for a certificate. |
| POST | / | Updates some of the parameters for an existing connector. Provide the ConnectorId for the connector that you want to update, along with the new values for the parameters to update. |
| POST | / | Updates the description for the host key that's specified by the ServerId and HostKeyId parameters. |
| POST | / | Updates some of the parameters for an existing profile. Provide the ProfileId for the profile that you want to update, along with the new values for the parameters to update. |
| POST | / | Updates the file transfer protocol-enabled server's properties after that server has been created. The UpdateServer call returns the ServerId of the server you updated. |
| POST | / | Assigns new properties to a user. Parameters you pass modify any or all of the following: the home directory, role, and policy for the UserName and ServerId you specify. The response returns the ServerId and the UserName for the updated user. In the console, you can select Restricted when you create or update a user. This ensures that the user can't access anything outside of their home directory. The programmatic way to configure this behavior is to update the user. Set their HomeDirectoryType to LOGICAL, and specify HomeDirectoryMappings with Entry as root (/) and Target as their home directory. For example, if the user's home directory is /test/admin-user, the following command updates the user so that their configuration in the console shows the Restricted flag as selected.   aws transfer update-user --server-id &lt;server-id&gt; --user-name admin-user --home-directory-type LOGICAL --home-directory-mappings "[{\"Entry\":\"/\", \"Target\":\"/test/admin-user\"}]" |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
