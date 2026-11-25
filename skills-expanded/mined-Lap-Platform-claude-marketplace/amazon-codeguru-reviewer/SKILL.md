---
name: amazon-codeguru-reviewer
description: "Amazon CodeGuru Reviewer API skill. Use when working with Amazon CodeGuru Reviewer for associations, codereviews, feedback. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon CodeGuru Reviewer
API version: 2019-09-19

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /codereviews -- verify access
3. POST /associations -- create first associations

## Endpoints

14 endpoints across 4 groups. See references/api-spec.lap for full details.

### associations
| Method | Path | Description |
|--------|------|-------------|
| POST | /associations | Use to associate an Amazon Web Services CodeCommit repository or a repository managed by Amazon Web Services CodeStar Connections with Amazon CodeGuru Reviewer. When you associate a repository, CodeGuru Reviewer reviews source code changes in the repository's pull requests and provides automatic recommendations. You can view recommendations using the CodeGuru Reviewer console. For more information, see Recommendations in Amazon CodeGuru Reviewer in the Amazon CodeGuru Reviewer User Guide.  If you associate a CodeCommit or S3 repository, it must be in the same Amazon Web Services Region and Amazon Web Services account where its CodeGuru Reviewer code reviews are configured. Bitbucket and GitHub Enterprise Server repositories are managed by Amazon Web Services CodeStar Connections to connect to CodeGuru Reviewer. For more information, see Associate a repository in the Amazon CodeGuru Reviewer User Guide.   You cannot use the CodeGuru Reviewer SDK or the Amazon Web Services CLI to associate a GitHub repository with Amazon CodeGuru Reviewer. To associate a GitHub repository, use the console. For more information, see Getting started with CodeGuru Reviewer in the CodeGuru Reviewer User Guide. |
| GET | /associations/{AssociationArn} | Returns a RepositoryAssociation object that contains information about the requested repository association. |
| DELETE | /associations/{AssociationArn} | Removes the association between Amazon CodeGuru Reviewer and a repository. |
| GET | /associations | Returns a list of RepositoryAssociationSummary objects that contain summary information about a repository association. You can filter the returned list by ProviderType, Name, State, and Owner. |

### codereviews
| Method | Path | Description |
|--------|------|-------------|
| POST | /codereviews | Use to create a code review with a CodeReviewType of RepositoryAnalysis. This type of code review analyzes all code under a specified branch in an associated repository. PullRequest code reviews are automatically triggered by a pull request. |
| GET | /codereviews/{CodeReviewArn} | Returns the metadata associated with the code review along with its status. |
| GET | /codereviews | Lists all the code reviews that the customer has created in the past 90 days. |
| GET | /codereviews/{CodeReviewArn}/Recommendations | Returns the list of all recommendations for a completed code review. |

### feedback
| Method | Path | Description |
|--------|------|-------------|
| GET | /feedback/{CodeReviewArn} | Describes the customer feedback for a CodeGuru Reviewer recommendation. |
| GET | /feedback/{CodeReviewArn}/RecommendationFeedback | Returns a list of RecommendationFeedbackSummary objects that contain customer recommendation feedback for all CodeGuru Reviewer users. |
| PUT | /feedback | Stores customer feedback for a CodeGuru Reviewer recommendation. When this API is called again with different reactions the previous feedback is overwritten. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Returns the list of tags associated with an associated repository resource. |
| POST | /tags/{resourceArn} | Adds one or more tags to an associated repository. |
| DELETE | /tags/{resourceArn} | Removes a tag from an associated repository. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a association?" -> POST /associations
- "Create a codereview?" -> POST /codereviews
- "Get codereview details?" -> GET /codereviews/{CodeReviewArn}
- "Get feedback details?" -> GET /feedback/{CodeReviewArn}
- "Get association details?" -> GET /associations/{AssociationArn}
- "Delete a association?" -> DELETE /associations/{AssociationArn}
- "List all codereviews?" -> GET /codereviews
- "List all RecommendationFeedback?" -> GET /feedback/{CodeReviewArn}/RecommendationFeedback
- "List all Recommendations?" -> GET /codereviews/{CodeReviewArn}/Recommendations
- "List all associations?" -> GET /associations
- "Get tag details?" -> GET /tags/{resourceArn}
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
