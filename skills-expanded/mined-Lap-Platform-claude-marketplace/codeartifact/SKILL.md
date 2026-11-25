---
name: codeartifact
description: "CodeArtifact API skill. Use when working with CodeArtifact for repository, package, domain. Covers 48 endpoints."
version: 1.0.0
generator: lapsh
---

# CodeArtifact
API version: 2018-09-22

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /v1/domain -- verify access
3. POST /v1/repository/external-connection -- create first external-connection

## Endpoints

48 endpoints across 16 groups. See references/api-spec.lap for full details.

### repository
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/repository/external-connection | Adds an existing external connection to a repository. One external connection is allowed per repository.  A repository can have one or more upstream repositories, or an external connection. |
| POST | /v1/repository | Creates a repository. |
| DELETE | /v1/repository | Deletes a repository. |
| DELETE | /v1/repository/permissions/policies | Deletes the resource policy that is set on a repository. After a resource policy is deleted, the permissions allowed and denied by the deleted policy are removed. The effect of deleting a resource policy might not be immediate.    Use DeleteRepositoryPermissionsPolicy with caution. After a policy is deleted, Amazon Web Services users, roles, and accounts lose permissions to perform the repository actions granted by the deleted policy. |
| GET | /v1/repository | Returns a RepositoryDescription object that contains detailed information about the requested repository. |
| DELETE | /v1/repository/external-connection | Removes an existing external connection from a repository. |
| GET | /v1/repository/endpoint | Returns the endpoint of a repository for a specific package format. A repository has one endpoint for each package format:     cargo     generic     maven     npm     nuget     pypi     ruby     swift |
| GET | /v1/repository/permissions/policy | Returns the resource policy that is set on a repository. |
| PUT | /v1/repository/permissions/policy | Sets the resource policy on a repository that specifies permissions to access it.   When you call PutRepositoryPermissionsPolicy, the resource policy on the repository is ignored when evaluting permissions. This ensures that the owner of a repository cannot lock themselves out of the repository, which would prevent them from being able to update the resource policy. |
| PUT | /v1/repository | Update the properties of a repository. |

### package
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/package/versions/copy | Copies package versions from one repository to another repository in the same domain.    You must specify versions or versionRevisions. You cannot specify both. |
| DELETE | /v1/package | Deletes a package and all associated package versions. A deleted package cannot be restored. To delete one or more package versions, use the DeletePackageVersions API. |
| POST | /v1/package/versions/delete | Deletes one or more versions of a package. A deleted package version cannot be restored in your repository. If you want to remove a package version from your repository and be able to restore it later, set its status to Archived. Archived packages cannot be downloaded from a repository and don't show up with list package APIs (for example, ListPackageVersions), but you can restore them using UpdatePackageVersionsStatus. |
| GET | /v1/package | Returns a PackageDescription object that contains information about the requested package. |
| GET | /v1/package/version | Returns a PackageVersionDescription object that contains information about the requested package version. |
| POST | /v1/package/versions/dispose | Deletes the assets in package versions and sets the package versions' status to Disposed. A disposed package version cannot be restored in your repository because its assets are deleted.   To view all disposed package versions in a repository, use ListPackageVersions and set the status parameter to Disposed.   To view information about a disposed package version, use DescribePackageVersion. |
| GET | /v1/package/version/asset | Returns an asset (or file) that is in a package. For example, for a Maven package version, use GetPackageVersionAsset to download a JAR file, a POM file, or any other assets in the package version. |
| GET | /v1/package/version/readme | Gets the readme file or descriptive text for a package version.   The returned text might contain formatting. For example, it might contain formatting for Markdown or reStructuredText. |
| POST | /v1/package/version/assets | Returns a list of AssetSummary objects for assets in a package version. |
| POST | /v1/package/version/dependencies | Returns the direct dependencies for a package version. The dependencies are returned as PackageDependency objects. CodeArtifact extracts the dependencies for a package version from the metadata file for the package format (for example, the package.json file for npm packages and the pom.xml file for Maven). Any package version dependencies that are not listed in the configuration file are not returned. |
| POST | /v1/package/versions | Returns a list of PackageVersionSummary objects for package versions in a repository that match the request parameters. Package versions of all statuses will be returned by default when calling list-package-versions with no --status parameter. |
| POST | /v1/package/version/publish | Creates a new package version containing one or more assets (or files). The unfinished flag can be used to keep the package version in the Unfinished state until all of its assets have been uploaded (see Package version status in the CodeArtifact user guide). To set the package version’s status to Published, omit the unfinished flag when uploading the final asset, or set the status using UpdatePackageVersionStatus. Once a package version’s status is set to Published, it cannot change back to Unfinished.  Only generic packages can be published using this API. For more information, see Using generic packages in the CodeArtifact User Guide. |
| POST | /v1/package | Sets the package origin configuration for a package. The package origin configuration determines how new versions of a package can be added to a repository. You can allow or block direct publishing of new package versions, or ingestion and retaining of new package versions from an external connection or upstream source. For more information about package origin controls and configuration, see Editing package origin controls in the CodeArtifact User Guide.  PutPackageOriginConfiguration can be called on a package that doesn't yet exist in the repository. When called on a package that does not exist, a package is created in the repository with no versions and the requested restrictions are set on the package. This can be used to preemptively block ingesting or retaining any versions from external connections or upstream repositories, or to block publishing any versions of the package into the repository before connecting any package managers or publishers to the repository. |
| POST | /v1/package/versions/update_status | Updates the status of one or more versions of a package. Using UpdatePackageVersionsStatus, you can update the status of package versions to Archived, Published, or Unlisted. To set the status of a package version to Disposed, use DisposePackageVersions. |

### domain
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/domain | Creates a domain. CodeArtifact domains make it easier to manage multiple repositories across an organization. You can use a domain to apply permissions across many repositories owned by different Amazon Web Services accounts. An asset is stored only once in a domain, even if it's in multiple repositories.  Although you can have multiple domains, we recommend a single production domain that contains all published artifacts so that your development teams can find and share packages. You can use a second pre-production domain to test changes to the production domain configuration. |
| DELETE | /v1/domain | Deletes a domain. You cannot delete a domain that contains repositories. If you want to delete a domain with repositories, first delete its repositories. |
| DELETE | /v1/domain/permissions/policy | Deletes the resource policy set on a domain. |
| GET | /v1/domain | Returns a DomainDescription object that contains information about the requested domain. |
| GET | /v1/domain/permissions/policy | Returns the resource policy attached to the specified domain.    The policy is a resource-based policy, not an identity-based policy. For more information, see Identity-based policies and resource-based policies  in the IAM User Guide. |
| POST | /v1/domain/repositories | Returns a list of RepositorySummary objects. Each RepositorySummary contains information about a repository in the specified domain and that matches the input parameters. |
| PUT | /v1/domain/permissions/policy | Sets a resource policy on a domain that specifies permissions to access it.   When you call PutDomainPermissionsPolicy, the resource policy on the domain is ignored when evaluting permissions. This ensures that the owner of a domain cannot lock themselves out of the domain, which would prevent them from being able to update the resource policy. |

### package-group
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/package-group | Creates a package group. For more information about creating package groups, including example CLI commands, see Create a package group in the CodeArtifact User Guide. |
| DELETE | /v1/package-group | Deletes a package group. Deleting a package group does not delete packages or package versions associated with the package group. When a package group is deleted, the direct child package groups will become children of the package group's direct parent package group. Therefore, if any of the child groups are inheriting any settings from the parent, those settings could change. |
| GET | /v1/package-group | Returns a PackageGroupDescription object that contains information about the requested package group. |
| PUT | /v1/package-group | Updates a package group. This API cannot be used to update a package group's origin configuration or pattern. To update a package group's origin configuration, use UpdatePackageGroupOriginConfiguration. |

### get-associated-package-group
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/get-associated-package-group | Returns the most closely associated package group to the specified package. This API does not require that the package exist in any repository in the domain. As such, GetAssociatedPackageGroup can be used to see which package group's origin configuration applies to a package before that package is in a repository. This can be helpful to check if public packages are blocked without ingesting them. For information package group association and matching, see Package group definition syntax and matching behavior in the CodeArtifact User Guide. |

### authorization-token
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/authorization-token | Generates a temporary authorization token for accessing repositories in the domain. This API requires the codeartifact:GetAuthorizationToken and sts:GetServiceBearerToken permissions. For more information about authorization tokens, see CodeArtifact authentication and tokens.   CodeArtifact authorization tokens are valid for a period of 12 hours when created with the login command. You can call login periodically to refresh the token. When you create an authorization token with the GetAuthorizationToken API, you can set a custom authorization period, up to a maximum of 12 hours, with the durationSeconds parameter. The authorization period begins after login or GetAuthorizationToken is called. If login or GetAuthorizationToken is called while assuming a role, the token lifetime is independent of the maximum session duration of the role. For example, if you call sts assume-role and specify a session duration of 15 minutes, then generate a CodeArtifact authorization token, the token will be valid for the full authorization period even though this is longer than the 15-minute session duration. See Using IAM Roles for more information on controlling session duration. |

### package-group-allowed-repositories
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/package-group-allowed-repositories | Lists the repositories in the added repositories list of the specified restriction type for a package group. For more information about restriction types and added repository lists, see Package group origin controls in the CodeArtifact User Guide. |

### list-associated-packages
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/list-associated-packages | Returns a list of packages associated with the requested package group. For information package group association and matching, see Package group definition syntax and matching behavior in the CodeArtifact User Guide. |

### domains
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/domains | Returns a list of DomainSummary objects for all domains owned by the Amazon Web Services account that makes this call. Each returned DomainSummary object contains information about a domain. |

### package-groups
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/package-groups | Returns a list of package groups in the requested domain. |
| POST | /v1/package-groups/sub-groups | Returns a list of direct children of the specified package group. For information package group hierarchy, see Package group definition syntax and matching behavior in the CodeArtifact User Guide. |

### packages
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/packages | Returns a list of PackageSummary objects for packages in a repository that match the request parameters. |

### repositories
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/repositories | Returns a list of RepositorySummary objects. Each RepositorySummary contains information about a repository in the specified Amazon Web Services account and that matches the input parameters. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/tags | Gets information about Amazon Web Services tags for a specified Amazon Resource Name (ARN) in CodeArtifact. |

### tag
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/tag | Adds or updates tags for a resource in CodeArtifact. |

### untag
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/untag | Removes tags from a resource in CodeArtifact. |

### package-group-origin-configuration
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v1/package-group-origin-configuration | Updates the package origin configuration for a package group. The package origin configuration determines how new versions of a package can be added to a repository. You can allow or block direct publishing of new package versions, or ingestion and retaining of new package versions from an external connection or upstream source. For more information about package group origin controls and configuration, see Package group origin controls in the CodeArtifact User Guide. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a external-connection?" -> POST /v1/repository/external-connection
- "Create a copy?" -> POST /v1/package/versions/copy
- "Create a domain?" -> POST /v1/domain
- "Create a package-group?" -> POST /v1/package-group
- "Create a repository?" -> POST /v1/repository
- "Create a delete?" -> POST /v1/package/versions/delete
- "List all domain?" -> GET /v1/domain
- "List all package?" -> GET /v1/package
- "List all package-group?" -> GET /v1/package-group
- "List all version?" -> GET /v1/package/version
- "List all repository?" -> GET /v1/repository
- "Create a dispose?" -> POST /v1/package/versions/dispose
- "List all get-associated-package-group?" -> GET /v1/get-associated-package-group
- "Create a authorization-token?" -> POST /v1/authorization-token
- "List all policy?" -> GET /v1/domain/permissions/policy
- "List all asset?" -> GET /v1/package/version/asset
- "List all readme?" -> GET /v1/package/version/readme
- "List all endpoint?" -> GET /v1/repository/endpoint
- "List all policy?" -> GET /v1/repository/permissions/policy
- "List all package-group-allowed-repositories?" -> GET /v1/package-group-allowed-repositories
- "List all list-associated-packages?" -> GET /v1/list-associated-packages
- "Create a domain?" -> POST /v1/domains
- "Create a package-group?" -> POST /v1/package-groups
- "Create a asset?" -> POST /v1/package/version/assets
- "Create a dependency?" -> POST /v1/package/version/dependencies
- "Create a version?" -> POST /v1/package/versions
- "Create a package?" -> POST /v1/packages
- "Create a repository?" -> POST /v1/repositories
- "Create a repository?" -> POST /v1/domain/repositories
- "Create a sub-group?" -> POST /v1/package-groups/sub-groups
- "Create a tag?" -> POST /v1/tags
- "Create a publish?" -> POST /v1/package/version/publish
- "Create a package?" -> POST /v1/package
- "Create a tag?" -> POST /v1/tag
- "Create a untag?" -> POST /v1/untag
- "Create a update_status?" -> POST /v1/package/versions/update_status
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
