---
name: aws-budgets
description: "AWS Budgets API skill. Use when working with AWS Budgets for root. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Budgets
API version: 2016-10-20

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

26 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates a budget and, if included, notifications and subscribers.   Only one of BudgetLimit or PlannedBudgetLimits can be present in the syntax at one time. Use the syntax that matches your case. The Request Syntax section shows the BudgetLimit syntax. For PlannedBudgetLimits, see the Examples section. |
| POST | / | Creates a budget action. |
| POST | / | Creates a notification. You must create the budget before you create the associated notification. |
| POST | / | Creates a subscriber. You must create the associated budget and notification before you create the subscriber. |
| POST | / | Deletes a budget. You can delete your budget at any time.  Deleting a budget also deletes the notifications and subscribers that are associated with that budget. |
| POST | / | Deletes a budget action. |
| POST | / | Deletes a notification.  Deleting a notification also deletes the subscribers that are associated with the notification. |
| POST | / | Deletes a subscriber.  Deleting the last subscriber to a notification also deletes the notification. |
| POST | / | Describes a budget.  The Request Syntax section shows the BudgetLimit syntax. For PlannedBudgetLimits, see the Examples section. |
| POST | / | Describes a budget action detail. |
| POST | / | Describes a budget action history detail. |
| POST | / | Describes all of the budget actions for an account. |
| POST | / | Describes all of the budget actions for a budget. |
| POST | / | Lists the budget names and notifications that are associated with an account. |
| POST | / | Describes the history for DAILY, MONTHLY, and QUARTERLY budgets. Budget history isn't available for ANNUAL budgets. |
| POST | / | Lists the budgets that are associated with an account.  The Request Syntax section shows the BudgetLimit syntax. For PlannedBudgetLimits, see the Examples section. |
| POST | / | Lists the notifications that are associated with a budget. |
| POST | / | Lists the subscribers that are associated with a notification. |
| POST | / | Executes a budget action. |
| POST | / | Lists tags associated with a budget or budget action resource. |
| POST | / | Creates tags for a budget or budget action resource. |
| POST | / | Deletes tags associated with a budget or budget action resource. |
| POST | / | Updates a budget. You can change every part of a budget except for the budgetName and the calculatedSpend. When you modify a budget, the calculatedSpend drops to zero until Amazon Web Services has new usage data to use for forecasting.  Only one of BudgetLimit or PlannedBudgetLimits can be present in the syntax at one time. Use the syntax that matches your case. The Request Syntax section shows the BudgetLimit syntax. For PlannedBudgetLimits, see the Examples section. |
| POST | / | Updates a budget action. |
| POST | / | Updates a notification. |
| POST | / | Updates a subscriber. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
