---
name: aws-codestar-notifications
description: "AWS CodeStar Notifications API skill. Use when working with AWS CodeStar Notifications for createNotificationRule, deleteNotificationRule, deleteTarget. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS CodeStar Notifications
API version: 2019-10-15

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST /createNotificationRule -- create first createNotificationRule

## Endpoints

13 endpoints across 13 groups. See references/api-spec.lap for full details.

### createNotificationRule
| Method | Path | Description |
|--------|------|-------------|
| POST | /createNotificationRule | Creates a notification rule for a resource. The rule specifies the events you want notifications about and the targets (such as Chatbot topics or Chatbot clients configured for Slack) where you want to receive them. |

### deleteNotificationRule
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteNotificationRule | Deletes a notification rule for a resource. |

### deleteTarget
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteTarget | Deletes a specified target for notifications. |

### describeNotificationRule
| Method | Path | Description |
|--------|------|-------------|
| POST | /describeNotificationRule | Returns information about a specified notification rule. |

### listEventTypes
| Method | Path | Description |
|--------|------|-------------|
| POST | /listEventTypes | Returns information about the event types available for configuring notifications. |

### listNotificationRules
| Method | Path | Description |
|--------|------|-------------|
| POST | /listNotificationRules | Returns a list of the notification rules for an Amazon Web Services account. |

### listTagsForResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /listTagsForResource | Returns a list of the tags associated with a notification rule. |

### listTargets
| Method | Path | Description |
|--------|------|-------------|
| POST | /listTargets | Returns a list of the notification rule targets for an Amazon Web Services account. |

### subscribe
| Method | Path | Description |
|--------|------|-------------|
| POST | /subscribe | Creates an association between a notification rule and an Chatbot topic or Chatbot client so that the associated target can receive notifications when the events described in the rule are triggered. |

### tagResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /tagResource | Associates a set of provided tags with a notification rule. |

### unsubscribe
| Method | Path | Description |
|--------|------|-------------|
| POST | /unsubscribe | Removes an association between a notification rule and an Chatbot topic so that subscribers to that topic stop receiving notifications when the events described in the rule are triggered. |

### untagResource
| Method | Path | Description |
|--------|------|-------------|
| POST | /untagResource/{resourceArn} | Removes the association between one or more provided tags and a notification rule. |

### updateNotificationRule
| Method | Path | Description |
|--------|------|-------------|
| POST | /updateNotificationRule | Updates a notification rule for a resource. You can change the events that trigger the notification rule, the status of the rule, and the targets that receive the notifications.  To add or remove tags for a notification rule, you must use TagResource and UntagResource. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a createNotificationRule?" -> POST /createNotificationRule
- "Create a deleteNotificationRule?" -> POST /deleteNotificationRule
- "Create a deleteTarget?" -> POST /deleteTarget
- "Create a describeNotificationRule?" -> POST /describeNotificationRule
- "Create a listEventType?" -> POST /listEventTypes
- "Create a listNotificationRule?" -> POST /listNotificationRules
- "Create a listTagsForResource?" -> POST /listTagsForResource
- "Create a listTarget?" -> POST /listTargets
- "Create a subscribe?" -> POST /subscribe
- "Create a tagResource?" -> POST /tagResource
- "Create a unsubscribe?" -> POST /unsubscribe
- "Create a updateNotificationRule?" -> POST /updateNotificationRule
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
