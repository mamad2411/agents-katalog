---
name: amazon-ec2-container-registry
description: "Amazon EC2 Container Registry API skill. Use when working with Amazon EC2 Container Registry for root. Covers 49 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon EC2 Container Registry
API version: 2015-09-21

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

49 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Checks the availability of one or more image layers in a repository. When an image is pushed to a repository, each image layer is checked to verify if it has been uploaded before. If it has been uploaded, then the image layer is skipped.  This operation is used by the Amazon ECR proxy and is not generally used by customers for pulling and pushing images. In most cases, you should use the docker CLI to pull, tag, and push images. |
| POST | / | Deletes a list of specified images within a repository. Images are specified with either an imageTag or imageDigest. You can remove a tag from an image by specifying the image's tag in your request. When you remove the last tag from an image, the image is deleted from your repository. You can completely delete an image (and all of its tags) by specifying the image's digest in your request. |
| POST | / | Gets detailed information for an image. Images are specified with either an imageTag or imageDigest. When an image is pulled, the BatchGetImage API is called once to retrieve the image manifest. |
| POST | / | Gets the scanning configuration for one or more repositories. |
| POST | / | Informs Amazon ECR that the image layer upload has completed for a specified registry, repository name, and upload ID. You can optionally provide a sha256 digest of the image layer for data validation purposes. When an image is pushed, the CompleteLayerUpload API is called once per each new image layer to verify that the upload has completed.  This operation is used by the Amazon ECR proxy and is not generally used by customers for pulling and pushing images. In most cases, you should use the docker CLI to pull, tag, and push images. |
| POST | / | Creates a pull through cache rule. A pull through cache rule provides a way to cache images from an upstream registry source in your Amazon ECR private registry. For more information, see Using pull through cache rules in the Amazon Elastic Container Registry User Guide. |
| POST | / | Creates a repository. For more information, see Amazon ECR repositories in the Amazon Elastic Container Registry User Guide. |
| POST | / | Creates a repository creation template. This template is used to define the settings for repositories created by Amazon ECR on your behalf. For example, repositories created through pull through cache actions. For more information, see Private repository creation templates in the Amazon Elastic Container Registry User Guide. |
| POST | / | Deletes the lifecycle policy associated with the specified repository. |
| POST | / | Deletes a pull through cache rule. |
| POST | / | Deletes the registry permissions policy. |
| POST | / | Deletes a repository. If the repository isn't empty, you must either delete the contents of the repository or use the force option to delete the repository and have Amazon ECR delete all of its contents on your behalf. |
| POST | / | Deletes a repository creation template. |
| POST | / | Deletes the repository policy associated with the specified repository. |
| POST | / | Returns the replication status for a specified image. |
| POST | / | Returns the scan findings for the specified image. |
| POST | / | Returns metadata about the images in a repository.  Beginning with Docker version 1.9, the Docker client compresses image layers before pushing them to a V2 Docker registry. The output of the docker images command shows the uncompressed image size, so it may return a larger image size than the image sizes returned by DescribeImages. |
| POST | / | Returns the pull through cache rules for a registry. |
| POST | / | Describes the settings for a registry. The replication configuration for a repository can be created or updated with the PutReplicationConfiguration API action. |
| POST | / | Describes image repositories in a registry. |
| POST | / | Returns details about the repository creation templates in a registry. The prefixes request parameter can be used to return the details for a specific repository creation template. |
| POST | / | Retrieves the basic scan type version name. |
| POST | / | Retrieves an authorization token. An authorization token represents your IAM authentication credentials and can be used to access any Amazon ECR registry that your IAM principal has access to. The authorization token is valid for 12 hours. The authorizationToken returned is a base64 encoded string that can be decoded and used in a docker login command to authenticate to a registry. The CLI offers an get-login-password command that simplifies the login process. For more information, see Registry authentication in the Amazon Elastic Container Registry User Guide. |
| POST | / | Retrieves the pre-signed Amazon S3 download URL corresponding to an image layer. You can only get URLs for image layers that are referenced in an image. When an image is pulled, the GetDownloadUrlForLayer API is called once per image layer that is not already cached.  This operation is used by the Amazon ECR proxy and is not generally used by customers for pulling and pushing images. In most cases, you should use the docker CLI to pull, tag, and push images. |
| POST | / | Retrieves the lifecycle policy for the specified repository. |
| POST | / | Retrieves the results of the lifecycle policy preview request for the specified repository. |
| POST | / | Retrieves the permissions policy for a registry. |
| POST | / | Retrieves the scanning configuration for a registry. |
| POST | / | Retrieves the repository policy for the specified repository. |
| POST | / | Notifies Amazon ECR that you intend to upload an image layer. When an image is pushed, the InitiateLayerUpload API is called once per image layer that has not already been uploaded. Whether or not an image layer has been uploaded is determined by the BatchCheckLayerAvailability API action.  This operation is used by the Amazon ECR proxy and is not generally used by customers for pulling and pushing images. In most cases, you should use the docker CLI to pull, tag, and push images. |
| POST | / | Lists all the image IDs for the specified repository. You can filter images based on whether or not they are tagged by using the tagStatus filter and specifying either TAGGED, UNTAGGED or ANY. For example, you can filter your results to return only UNTAGGED images and then pipe that result to a BatchDeleteImage operation to delete them. Or, you can filter your results to return only TAGGED images to list all of the tags in your repository. |
| POST | / | List the tags for an Amazon ECR resource. |
| POST | / | Allows you to change the basic scan type version by setting the name parameter to either CLAIR to AWS_NATIVE. |
| POST | / | Creates or updates the image manifest and tags associated with an image. When an image is pushed and all new image layers have been uploaded, the PutImage API is called once to create or update the image manifest and the tags associated with the image.  This operation is used by the Amazon ECR proxy and is not generally used by customers for pulling and pushing images. In most cases, you should use the docker CLI to pull, tag, and push images. |
| POST | / | The PutImageScanningConfiguration API is being deprecated, in favor of specifying the image scanning configuration at the registry level. For more information, see PutRegistryScanningConfiguration.  Updates the image scanning configuration for the specified repository. |
| POST | / | Updates the image tag mutability settings for the specified repository. For more information, see Image tag mutability in the Amazon Elastic Container Registry User Guide. |
| POST | / | Creates or updates the lifecycle policy for the specified repository. For more information, see Lifecycle policy template. |
| POST | / | Creates or updates the permissions policy for your registry. A registry policy is used to specify permissions for another Amazon Web Services account and is used when configuring cross-account replication. For more information, see Registry permissions in the Amazon Elastic Container Registry User Guide. |
| POST | / | Creates or updates the scanning configuration for your private registry. |
| POST | / | Creates or updates the replication configuration for a registry. The existing replication configuration for a repository can be retrieved with the DescribeRegistry API action. The first time the PutReplicationConfiguration API is called, a service-linked IAM role is created in your account for the replication process. For more information, see Using service-linked roles for Amazon ECR in the Amazon Elastic Container Registry User Guide. For more information on the custom role for replication, see Creating an IAM role for replication.  When configuring cross-account replication, the destination account must grant the source account permission to replicate. This permission is controlled using a registry permissions policy. For more information, see PutRegistryPolicy. |
| POST | / | Applies a repository policy to the specified repository to control access permissions. For more information, see Amazon ECR Repository policies in the Amazon Elastic Container Registry User Guide. |
| POST | / | Starts an image vulnerability scan. An image scan can only be started once per 24 hours on an individual image. This limit includes if an image was scanned on initial push. For more information, see Image scanning in the Amazon Elastic Container Registry User Guide. |
| POST | / | Starts a preview of a lifecycle policy for the specified repository. This allows you to see the results before associating the lifecycle policy with the repository. |
| POST | / | Adds specified tags to a resource with the specified ARN. Existing tags on a resource are not changed if they are not specified in the request parameters. |
| POST | / | Deletes specified tags from a resource. |
| POST | / | Updates an existing pull through cache rule. |
| POST | / | Updates an existing repository creation template. |
| POST | / | Uploads an image layer part to Amazon ECR. When an image is pushed, each new image layer is uploaded in parts. The maximum size of each image layer part can be 20971520 bytes (or about 20MB). The UploadLayerPart API is called once per each new image layer part.  This operation is used by the Amazon ECR proxy and is not generally used by customers for pulling and pushing images. In most cases, you should use the docker CLI to pull, tag, and push images. |
| POST | / | Validates an existing pull through cache rule for an upstream registry that requires authentication. This will retrieve the contents of the Amazon Web Services Secrets Manager secret, verify the syntax, and then validate that authentication to the upstream registry is successful. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
