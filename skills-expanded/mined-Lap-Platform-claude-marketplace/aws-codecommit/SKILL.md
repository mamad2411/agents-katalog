---
name: aws-codecommit
description: "AWS CodeCommit API skill. Use when working with AWS CodeCommit for root. Covers 79 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS CodeCommit
API version: 2015-04-13

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

79 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates an association between an approval rule template and a specified repository. Then, the next time a pull request is created in the repository where the destination reference (if specified) matches the destination reference (branch) for the pull request, an approval rule that matches the template conditions is automatically created for that pull request. If no destination references are specified in the template, an approval rule that matches the template contents is created for all pull requests in that repository. |
| POST | / | Creates an association between an approval rule template and one or more specified repositories. |
| POST | / | Returns information about one or more merge conflicts in the attempted merge of two commit specifiers using the squash or three-way merge strategy. |
| POST | / | Removes the association between an approval rule template and one or more specified repositories. |
| POST | / | Returns information about the contents of one or more commits in a repository. |
| POST | / | Returns information about one or more repositories.  The description field for a repository accepts all HTML characters and all valid Unicode characters. Applications that do not HTML-encode the description and display it in a webpage can expose users to potentially malicious code. Make sure that you HTML-encode the description field in any application that uses this API to display the repository description on a webpage. |
| POST | / | Creates a template for approval rules that can then be associated with one or more repositories in your Amazon Web Services account. When you associate a template with a repository, CodeCommit creates an approval rule that matches the conditions of the template for all pull requests that meet the conditions of the template. For more information, see AssociateApprovalRuleTemplateWithRepository. |
| POST | / | Creates a branch in a repository and points the branch to a commit.  Calling the create branch operation does not set a repository's default branch. To do this, call the update default branch operation. |
| POST | / | Creates a commit for a repository on the tip of a specified branch. |
| POST | / | Creates a pull request in the specified repository. |
| POST | / | Creates an approval rule for a pull request. |
| POST | / | Creates a new, empty repository. |
| POST | / | Creates an unreferenced commit that represents the result of merging two branches using a specified merge strategy. This can help you determine the outcome of a potential merge. This API cannot be used with the fast-forward merge strategy because that strategy does not create a merge commit.  This unreferenced merge commit can only be accessed using the GetCommit API or through git commands such as git fetch. To retrieve this commit, you must specify its commit ID or otherwise reference it. |
| POST | / | Deletes a specified approval rule template. Deleting a template does not remove approval rules on pull requests already created with the template. |
| POST | / | Deletes a branch from a repository, unless that branch is the default branch for the repository. |
| POST | / | Deletes the content of a comment made on a change, file, or commit in a repository. |
| POST | / | Deletes a specified file from a specified branch. A commit is created on the branch that contains the revision. The file still exists in the commits earlier to the commit that contains the deletion. |
| POST | / | Deletes an approval rule from a specified pull request. Approval rules can be deleted from a pull request only if the pull request is open, and if the approval rule was created specifically for a pull request and not generated from an approval rule template associated with the repository where the pull request was created. You cannot delete an approval rule from a merged or closed pull request. |
| POST | / | Deletes a repository. If a specified repository was already deleted, a null repository ID is returned.  Deleting a repository also deletes all associated objects and metadata. After a repository is deleted, all future push calls to the deleted repository fail. |
| POST | / | Returns information about one or more merge conflicts in the attempted merge of two commit specifiers using the squash or three-way merge strategy. If the merge option for the attempted merge is specified as FAST_FORWARD_MERGE, an exception is thrown. |
| POST | / | Returns information about one or more pull request events. |
| POST | / | Removes the association between a template and a repository so that approval rules based on the template are not automatically created when pull requests are created in the specified repository. This does not delete any approval rules previously created for pull requests through the template association. |
| POST | / | Evaluates whether a pull request has met all the conditions specified in its associated approval rules. |
| POST | / | Returns information about a specified approval rule template. |
| POST | / | Returns the base-64 encoded content of an individual blob in a repository. |
| POST | / | Returns information about a repository branch, including its name and the last commit ID. |
| POST | / | Returns the content of a comment made on a change, file, or commit in a repository.   Reaction counts might include numbers from user identities who were deleted after the reaction was made. For a count of reactions from active identities, use GetCommentReactions. |
| POST | / | Returns information about reactions to a specified comment ID. Reactions from users who have been deleted will not be included in the count. |
| POST | / | Returns information about comments made on the comparison between two commits.  Reaction counts might include numbers from user identities who were deleted after the reaction was made. For a count of reactions from active identities, use GetCommentReactions. |
| POST | / | Returns comments made on a pull request.  Reaction counts might include numbers from user identities who were deleted after the reaction was made. For a count of reactions from active identities, use GetCommentReactions. |
| POST | / | Returns information about a commit, including commit message and committer information. |
| POST | / | Returns information about the differences in a valid commit specifier (such as a branch, tag, HEAD, commit ID, or other fully qualified reference). Results can be limited to a specified path. |
| POST | / | Returns the base-64 encoded contents of a specified file and its metadata. |
| POST | / | Returns the contents of a specified folder in a repository. |
| POST | / | Returns information about a specified merge commit. |
| POST | / | Returns information about merge conflicts between the before and after commit IDs for a pull request in a repository. |
| POST | / | Returns information about the merge options available for merging two specified branches. For details about why a merge option is not available, use GetMergeConflicts or DescribeMergeConflicts. |
| POST | / | Gets information about a pull request in a specified repository. |
| POST | / | Gets information about the approval states for a specified pull request. Approval states only apply to pull requests that have one or more approval rules applied to them. |
| POST | / | Returns information about whether approval rules have been set aside (overridden) for a pull request, and if so, the Amazon Resource Name (ARN) of the user or identity that overrode the rules and their requirements for the pull request. |
| POST | / | Returns information about a repository.  The description field for a repository accepts all HTML characters and all valid Unicode characters. Applications that do not HTML-encode the description and display it in a webpage can expose users to potentially malicious code. Make sure that you HTML-encode the description field in any application that uses this API to display the repository description on a webpage. |
| POST | / | Gets information about triggers configured for a repository. |
| POST | / | Lists all approval rule templates in the specified Amazon Web Services Region in your Amazon Web Services account. If an Amazon Web Services Region is not specified, the Amazon Web Services Region where you are signed in is used. |
| POST | / | Lists all approval rule templates that are associated with a specified repository. |
| POST | / | Gets information about one or more branches in a repository. |
| POST | / | Retrieves a list of commits and changes to a specified file. |
| POST | / | Returns a list of pull requests for a specified repository. The return list can be refined by pull request status or pull request author ARN. |
| POST | / | Gets information about one or more repositories. |
| POST | / | Lists all repositories associated with the specified approval rule template. |
| POST | / | Gets information about Amazon Web Servicestags for a specified Amazon Resource Name (ARN) in CodeCommit. For a list of valid resources in CodeCommit, see CodeCommit Resources and Operations in the CodeCommit User Guide. |
| POST | / | Merges two branches using the fast-forward merge strategy. |
| POST | / | Merges two branches using the squash merge strategy. |
| POST | / | Merges two specified branches using the three-way merge strategy. |
| POST | / | Attempts to merge the source commit of a pull request into the specified destination branch for that pull request at the specified commit using the fast-forward merge strategy. If the merge is successful, it closes the pull request. |
| POST | / | Attempts to merge the source commit of a pull request into the specified destination branch for that pull request at the specified commit using the squash merge strategy. If the merge is successful, it closes the pull request. |
| POST | / | Attempts to merge the source commit of a pull request into the specified destination branch for that pull request at the specified commit using the three-way merge strategy. If the merge is successful, it closes the pull request. |
| POST | / | Sets aside (overrides) all approval rule requirements for a specified pull request. |
| POST | / | Posts a comment on the comparison between two commits. |
| POST | / | Posts a comment on a pull request. |
| POST | / | Posts a comment in reply to an existing comment on a comparison between commits or a pull request. |
| POST | / | Adds or updates a reaction to a specified comment for the user whose identity is used to make the request. You can only add or update a reaction for yourself. You cannot add, modify, or delete a reaction for another user. |
| POST | / | Adds or updates a file in a branch in an CodeCommit repository, and generates a commit for the addition in the specified branch. |
| POST | / | Replaces all triggers for a repository. Used to create or delete triggers. |
| POST | / | Adds or updates tags for a resource in CodeCommit. For a list of valid resources in CodeCommit, see CodeCommit Resources and Operations in the CodeCommit User Guide. |
| POST | / | Tests the functionality of repository triggers by sending information to the trigger target. If real data is available in the repository, the test sends data from the last commit. If no data is available, sample data is generated. |
| POST | / | Removes tags for a resource in CodeCommit. For a list of valid resources in CodeCommit, see CodeCommit Resources and Operations in the CodeCommit User Guide. |
| POST | / | Updates the content of an approval rule template. You can change the number of required approvals, the membership of the approval rule, and whether an approval pool is defined. |
| POST | / | Updates the description for a specified approval rule template. |
| POST | / | Updates the name of a specified approval rule template. |
| POST | / | Replaces the contents of a comment. |
| POST | / | Sets or changes the default branch name for the specified repository.  If you use this operation to change the default branch name to the current default branch name, a success message is returned even though the default branch did not change. |
| POST | / | Updates the structure of an approval rule created specifically for a pull request. For example, you can change the number of required approvers and the approval pool for approvers. |
| POST | / | Updates the state of a user's approval on a pull request. The user is derived from the signed-in account when the request is made. |
| POST | / | Replaces the contents of the description of a pull request. |
| POST | / | Updates the status of a pull request. |
| POST | / | Replaces the title of a pull request. |
| POST | / | Sets or changes the comment or description for a repository.  The description field for a repository accepts all HTML characters and all valid Unicode characters. Applications that do not HTML-encode the description and display it in a webpage can expose users to potentially malicious code. Make sure that you HTML-encode the description field in any application that uses this API to display the repository description on a webpage. |
| POST | / | Updates the Key Management Service encryption key used to encrypt and decrypt a CodeCommit repository. |
| POST | / | Renames a repository. The repository name must be unique across the calling Amazon Web Services account. Repository names are limited to 100 alphanumeric, dash, and underscore characters, and cannot include certain characters. The suffix .git is prohibited. For more information about the limits on repository names, see Quotas in the CodeCommit User Guide. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
