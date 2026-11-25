---
name: amazon-personalize-runtime
description: "Amazon Personalize Runtime API skill. Use when working with Amazon Personalize Runtime for action-recommendations, personalize-ranking, recommendations. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Amazon Personalize Runtime
API version: 2018-05-22

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /action-recommendations -- create first action-recommendations

## Endpoints

3 endpoints across 3 groups. See references/api-spec.lap for full details.

### action-recommendations
| Method | Path | Description |
|--------|------|-------------|
| POST | /action-recommendations | Returns a list of recommended actions in sorted in descending order by prediction score. Use the GetActionRecommendations API if you have a custom campaign that deploys a solution version trained with a PERSONALIZED_ACTIONS recipe.  For more information about PERSONALIZED_ACTIONS recipes, see PERSONALIZED_ACTIONS recipes. For more information about getting action recommendations, see Getting action recommendations. |

### personalize-ranking
| Method | Path | Description |
|--------|------|-------------|
| POST | /personalize-ranking | Re-ranks a list of recommended items for the given user. The first item in the list is deemed the most likely item to be of interest to the user.  The solution backing the campaign must have been created using a recipe of type PERSONALIZED_RANKING. |

### recommendations
| Method | Path | Description |
|--------|------|-------------|
| POST | /recommendations | Returns a list of recommended items. For campaigns, the campaign's Amazon Resource Name (ARN) is required and the required user and item input depends on the recipe type used to create the solution backing the campaign as follows:   USER_PERSONALIZATION - userId required, itemId not used   RELATED_ITEMS - itemId required, userId not used    Campaigns that are backed by a solution created using a recipe of type PERSONALIZED_RANKING use the API.   For recommenders, the recommender's ARN is required and the required item and user input depends on the use case (domain-based recipe) backing the recommender. For information on use case requirements see Choosing recommender use cases. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a action-recommendation?" -> POST /action-recommendations
- "Create a personalize-ranking?" -> POST /personalize-ranking
- "Create a recommendation?" -> POST /recommendations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
