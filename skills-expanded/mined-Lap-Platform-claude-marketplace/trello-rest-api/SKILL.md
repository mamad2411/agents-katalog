---
name: trello-rest-api
description: "Trello REST API skill. Use when working with Trello REST for actions, applications, batch. Covers 256 endpoints."
version: 1.0.0
generator: lapsh
---

# Trello REST API
API version: 0.0.1

## Auth
ApiKey key in query | ApiKey token in query

## Base URL
https://api.trello.com/1

## Setup
1. Set your API key in the appropriate header
2. GET /batch -- verify access
3. POST /actions/{idAction}/reactions -- create first reactions

## Endpoints

256 endpoints across 18 groups. See references/api-spec.lap for full details.

### actions
| Method | Path | Description |
|--------|------|-------------|
| GET | /actions/{id} | Get an Action |
| PUT | /actions/{id} | Update an Action |
| DELETE | /actions/{id} | Delete an Action |
| GET | /actions/{id}/{field} | Get a specific field on an Action |
| GET | /actions/{id}/board | Get the Board for an Action |
| GET | /actions/{id}/card | Get the Card for an Action |
| GET | /actions/{id}/list | Get the List for an Action |
| GET | /actions/{id}/member | Get the Member of an Action |
| GET | /actions/{id}/memberCreator | Get the Member Creator of an Action |
| GET | /actions/{id}/organization | Get the Organization of an Action |
| PUT | /actions/{id}/text | Update a Comment Action |
| GET | /actions/{idAction}/reactions | Get Action's Reactions |
| POST | /actions/{idAction}/reactions | Create Reaction for Action |
| GET | /actions/{idAction}/reactions/{id} | Get Action's Reaction |
| DELETE | /actions/{idAction}/reactions/{id} | Delete Action's Reaction |
| GET | /actions/{idAction}/reactionsSummary | List Action's summary of Reactions |

### applications
| Method | Path | Description |
|--------|------|-------------|
| GET | /applications/{key}/compliance | Get Application's compliance data |

### batch
| Method | Path | Description |
|--------|------|-------------|
| GET | /batch | Batch Requests |

### boards
| Method | Path | Description |
|--------|------|-------------|
| GET | /boards/{id}/memberships | Get Memberships of a Board |
| GET | /boards/{id} | Get a Board |
| PUT | /boards/{id} | Update a Board |
| DELETE | /boards/{id} | Delete a Board |
| GET | /boards/{id}/{field} | Get a field on a Board |
| GET | /boards/{boardId}/actions | Get Actions of a Board |
| GET | /boards/{boardId}/boardStars | Get boardStars on a Board |
| GET | /boards/{id}/checklists | Get Checklists on a Board |
| GET | /boards/{id}/cards | Get Cards on a Board |
| GET | /boards/{id}/cards/{filter} | Get filtered Cards on a Board |
| GET | /boards/{id}/customFields | Get Custom Fields for Board |
| GET | /boards/{id}/labels | Get Labels on a Board |
| POST | /boards/{id}/labels | Create a Label on a Board |
| GET | /boards/{id}/lists | Get Lists on a Board |
| POST | /boards/{id}/lists | Create a List on a Board |
| GET | /boards/{id}/lists/{filter} | Get filtered Lists on a Board |
| GET | /boards/{id}/members | Get the Members of a Board |
| PUT | /boards/{id}/members | Invite Member to Board via email |
| PUT | /boards/{id}/members/{idMember} | Add a Member to a Board |
| DELETE | /boards/{id}/members/{idMember} | Remove Member from Board |
| PUT | /boards/{id}/memberships/{idMembership} | Update Membership of Member on a Board |
| PUT | /boards/{id}/myPrefs/emailPosition | Update emailPosition Pref on a Board |
| PUT | /boards/{id}/myPrefs/idEmailList | Update idEmailList Pref on a Board |
| PUT | /boards/{id}/myPrefs/showSidebar | Update showSidebar Pref on a Board |
| PUT | /boards/{id}/myPrefs/showSidebarActivity | Update showSidebarActivity Pref on a Board |
| PUT | /boards/{id}/myPrefs/showSidebarBoardActions | Update showSidebarBoardActions Pref on a Board |
| PUT | /boards/{id}/myPrefs/showSidebarMembers | Update showSidebarMembers Pref on a Board |
| POST | /boards/ | Create a Board |
| POST | /boards/{id}/calendarKey/generate | Create a calendarKey for a Board |
| POST | /boards/{id}/emailKey/generate | Create a emailKey for a Board |
| POST | /boards/{id}/idTags | Create a Tag for a Board |
| POST | /boards/{id}/markedAsViewed | Mark Board as viewed |
| GET | /boards/{id}/boardPlugins | Get Enabled Power-Ups on Board |
| POST | /boards/{id}/boardPlugins | Enable a Power-Up on a Board |
| DELETE | /boards/{id}/boardPlugins/{idPlugin} | Disable a Power-Up on a Board |
| GET | /boards/{id}/plugins | Get Power-Ups on a Board |

### cards
| Method | Path | Description |
|--------|------|-------------|
| POST | /cards | Create a new Card |
| GET | /cards/{id} | Get a Card |
| PUT | /cards/{id} | Update a Card |
| DELETE | /cards/{id} | Delete a Card |
| GET | /cards/{id}/{field} | Get a field on a Card |
| GET | /cards/{id}/actions | Get Actions on a Card |
| GET | /cards/{id}/attachments | Get Attachments on a Card |
| POST | /cards/{id}/attachments | Create Attachment On Card |
| GET | /cards/{id}/attachments/{idAttachment} | Get an Attachment on a Card |
| DELETE | /cards/{id}/attachments/{idAttachment} | Delete an Attachment on a Card |
| GET | /cards/{id}/board | Get the Board the Card is on |
| GET | /cards/{id}/checkItemStates | Get checkItems on a Card |
| GET | /cards/{id}/checklists | Get Checklists on a Card |
| POST | /cards/{id}/checklists | Create Checklist on a Card |
| GET | /cards/{id}/checkItem/{idCheckItem} | Get checkItem on a Card |
| PUT | /cards/{id}/checkItem/{idCheckItem} | Update a checkItem on a Card |
| DELETE | /cards/{id}/checkItem/{idCheckItem} | Delete checkItem on a Card |
| GET | /cards/{id}/list | Get the List of a Card |
| GET | /cards/{id}/members | Get the Members of a Card |
| GET | /cards/{id}/membersVoted | Get Members who have voted on a Card |
| POST | /cards/{id}/membersVoted | Add Member vote to Card |
| GET | /cards/{id}/pluginData | Get pluginData on a Card |
| GET | /cards/{id}/stickers | Get Stickers on a Card |
| POST | /cards/{id}/stickers | Add a Sticker to a Card |
| GET | /cards/{id}/stickers/{idSticker} | Get a Sticker on a Card |
| DELETE | /cards/{id}/stickers/{idSticker} | Delete a Sticker on a Card |
| PUT | /cards/{id}/stickers/{idSticker} | Update a Sticker on a Card |
| PUT | /cards/{id}/actions/{idAction}/comments | Update Comment Action on a Card |
| DELETE | /cards/{id}/actions/{idAction}/comments | Delete a comment on a Card |
| PUT | /cards/{idCard}/customField/{idCustomField}/item | Update Custom Field item on Card |
| PUT | /cards/{idCard}/customFields | Update Multiple Custom Field items on Card |
| GET | /cards/{id}/customFieldItems | Get Custom Field Items for a Card |
| POST | /cards/{id}/actions/comments | Add a new comment to a Card |
| POST | /cards/{id}/idLabels | Add a Label to a Card |
| POST | /cards/{id}/idMembers | Add a Member to a Card |
| POST | /cards/{id}/labels | Create a new Label on a Card |
| POST | /cards/{id}/markAssociatedNotificationsRead | Mark a Card's Notifications as read |
| DELETE | /cards/{id}/idLabels/{idLabel} | Remove a Label from a Card |
| DELETE | /cards/{id}/idMembers/{idMember} | Remove a Member from a Card |
| DELETE | /cards/{id}/membersVoted/{idMember} | Remove a Member's Vote on a Card |
| PUT | /cards/{idCard}/checklist/{idChecklist}/checkItem/{idCheckItem} | Update Checkitem on Checklist on Card |
| DELETE | /cards/{id}/checklists/{idChecklist} | Delete a Checklist on a Card |

### checklists
| Method | Path | Description |
|--------|------|-------------|
| POST | /checklists | Create a Checklist |
| GET | /checklists/{id} | Get a Checklist |
| PUT | /checklists/{id} | Update a Checklist |
| DELETE | /checklists/{id} | Delete a Checklist |
| GET | /checklists/{id}/{field} | Get field on a Checklist |
| PUT | /checklists/{id}/{field} | Update field on a Checklist |
| GET | /checklists/{id}/board | Get the Board the Checklist is on |
| GET | /checklists/{id}/cards | Get the Card a Checklist is on |
| GET | /checklists/{id}/checkItems | Get Checkitems on a Checklist |
| POST | /checklists/{id}/checkItems | Create Checkitem on Checklist |
| GET | /checklists/{id}/checkItems/{idCheckItem} | Get a Checkitem on a Checklist |
| DELETE | /checklists/{id}/checkItems/{idCheckItem} | Delete Checkitem from Checklist |

### customFields
| Method | Path | Description |
|--------|------|-------------|
| POST | /customFields | Create a new Custom Field on a Board |
| GET | /customFields/{id} | Get a Custom Field |
| PUT | /customFields/{id} | Update a Custom Field definition |
| DELETE | /customFields/{id} | Delete a Custom Field definition |
| POST | /customFields/{id}/options | Add Option to Custom Field dropdown |
| GET | /customFields/{id}/options | Get Options of Custom Field drop down |
| GET | /customFields/{id}/options/{idCustomFieldOption} | Get Option of Custom Field dropdown |
| DELETE | /customFields/{id}/options/{idCustomFieldOption} | Delete Option of Custom Field dropdown |

### emoji
| Method | Path | Description |
|--------|------|-------------|
| GET | /emoji | List available Emoji |

### enterprises
| Method | Path | Description |
|--------|------|-------------|
| GET | /enterprises/{id} | Get an Enterprise |
| GET | /enterprises/{id}/auditlog | Get auditlog data for an Enterprise |
| GET | /enterprises/{id}/admins | Get Enterprise admin Members |
| GET | /enterprises/{id}/signupUrl | Get signupUrl for Enterprise |
| GET | /enterprises/{id}/members/query | Get Users of an Enterprise |
| GET | /enterprises/{id}/members | Get Members of Enterprise |
| GET | /enterprises/{id}/members/{idMember} | Get a Member of Enterprise |
| GET | /enterprises/{id}/transferrable/organization/{idOrganization} | Get whether an organization can be transferred to an enterprise. |
| GET | /enterprises/{id}/transferrable/bulk/{idOrganizations} | Get a bulk list of organizations that can be transferred to an enterprise. |
| PUT | /enterprises/${id}/enterpriseJoinRequest/bulk | Decline enterpriseJoinRequests from one organization or a bulk list of organizations. |
| GET | /enterprises/{id}/claimableOrganizations | Get ClaimableOrganizations of an Enterprise |
| GET | /enterprises/{id}/pendingOrganizations | Get PendingOrganizations of an Enterprise |
| POST | /enterprises/{id}/tokens | Create an auth Token for an Enterprise. |
| GET | /enterprises/{id}/organizations | Get Organizations of an Enterprise |
| PUT | /enterprises/{id}/organizations | Transfer an Organization to an Enterprise. |
| PUT | /enterprises/{id}/members/{idMember}/licensed | Update a Member's licensed status |
| PUT | /enterprises/{id}/members/{idMember}/deactivated | Deactivate a Member of an Enterprise. |
| PUT | /enterprises/{id}/admins/{idMember} | Update Member to be admin of Enterprise |
| DELETE | /enterprises/{id}/admins/{idMember} | Remove a Member as admin from Enterprise. |
| DELETE | /enterprises/{id}/organizations/{idOrg} | Delete an Organization from an Enterprise. |
| GET | /enterprises/{id}/organizations/bulk/{idOrganizations} | Bulk accept a set of organizations to an Enterprise. |

### labels
| Method | Path | Description |
|--------|------|-------------|
| GET | /labels/{id} | Get a Label |
| PUT | /labels/{id} | Update a Label |
| DELETE | /labels/{id} | Delete a Label |
| PUT | /labels/{id}/{field} | Update a field on a label |
| POST | /labels | Create a Label |

### lists
| Method | Path | Description |
|--------|------|-------------|
| GET | /lists/{id} | Get a List |
| PUT | /lists/{id} | Update a List |
| POST | /lists | Create a new List |
| POST | /lists/{id}/archiveAllCards | Archive all Cards in List |
| POST | /lists/{id}/moveAllCards | Move all Cards in List |
| PUT | /lists/{id}/closed | Archive or unarchive a list |
| PUT | /lists/{id}/idBoard | Move List to Board |
| PUT | /lists/{id}/{field} | Update a field on a List |
| GET | /lists/{id}/actions | Get Actions for a List |
| GET | /lists/{id}/board | Get the Board a List is on |
| GET | /lists/{id}/cards | Get Cards in a List |

### members
| Method | Path | Description |
|--------|------|-------------|
| GET | /members/{id} | Get a Member |
| PUT | /members/{id} | Update a Member |
| GET | /members/{id}/{field} | Get a field on a Member |
| GET | /members/{id}/actions | Get a Member's Actions |
| GET | /members/{id}/boardBackgrounds | Get Member's custom Board backgrounds |
| POST | /members/{id}/boardBackgrounds | Upload new boardBackground for Member |
| GET | /members/{id}/boardBackgrounds/{idBackground} | Get a boardBackground of a Member |
| PUT | /members/{id}/boardBackgrounds/{idBackground} | Update a Member's custom Board background |
| DELETE | /members/{id}/boardBackgrounds/{idBackground} | Delete a Member's custom Board background |
| GET | /members/{id}/boardStars | Get a Member's boardStars |
| POST | /members/{id}/boardStars | Create Star for Board |
| GET | /members/{id}/boardStars/{idStar} | Get a boardStar of Member |
| PUT | /members/{id}/boardStars/{idStar} | Update the position of a boardStar of Member |
| DELETE | /members/{id}/boardStars/{idStar} | Delete Star for Board |
| GET | /members/{id}/boards | Get Boards that Member belongs to |
| GET | /members/{id}/boardsInvited | Get Boards the Member has been invited to |
| GET | /members/{id}/cards | Get Cards the Member is on |
| GET | /members/{id}/customBoardBackgrounds | Get a Member's custom Board Backgrounds |
| POST | /members/{id}/customBoardBackgrounds | Create a new custom Board Background |
| GET | /members/{id}/customBoardBackgrounds/{idBackground} | Get custom Board Background of Member |
| PUT | /members/{id}/customBoardBackgrounds/{idBackground} | Update custom Board Background of Member |
| DELETE | /members/{id}/customBoardBackgrounds/{idBackground} | Delete custom Board Background of Member |
| GET | /members/{id}/customEmoji | Get a Member's customEmojis |
| POST | /members/{id}/customEmoji | Create custom Emoji for Member |
| GET | /members/{id}/customEmoji/{idEmoji} | Get a Member's custom Emoji |
| GET | /members/{id}/customStickers | Get Member's custom Stickers |
| POST | /members/{id}/customStickers | Create custom Sticker for Member |
| GET | /members/{id}/customStickers/{idSticker} | Get a Member's custom Sticker |
| DELETE | /members/{id}/customStickers/{idSticker} | Delete a Member's custom Sticker |
| GET | /members/{id}/notifications | Get Member's Notifications |
| GET | /members/{id}/organizations | Get Member's Organizations |
| GET | /members/{id}/organizationsInvited | Get Organizations a Member has been invited to |
| GET | /members/{id}/savedSearches | Get Member's saved searched |
| POST | /members/{id}/savedSearches | Create saved Search for Member |
| GET | /members/{id}/savedSearches/{idSearch} | Get a saved search |
| PUT | /members/{id}/savedSearches/{idSearch} | Update a saved search |
| DELETE | /members/{id}/savedSearches/{idSearch} | Delete a saved search |
| GET | /members/{id}/tokens | Get Member's Tokens |
| POST | /members/{id}/avatar | Create Avatar for Member |
| POST | /members/{id}/oneTimeMessagesDismissed | Dismiss a message for Member |
| GET | /members/{id}/notificationsChannelSettings | Get a Member's notification channel settings |
| PUT | /members/{id}/notificationsChannelSettings | Update blocked notification keys of Member on a channel |
| GET | /members/{id}/notificationsChannelSettings/{channel} | Get blocked notification keys of Member on this channel |
| PUT | /members/{id}/notificationsChannelSettings/{channel} | Update blocked notification keys of Member on a channel |
| PUT | /members/{id}/notificationsChannelSettings/{channel}/{blockedKeys} | Update blocked notification keys of Member on a channel |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /notifications/{id} | Get a Notification |
| PUT | /notifications/{id} | Update a Notification's read status |
| GET | /notifications/{id}/{field} | Get a field of a Notification |
| POST | /notifications/all/read | Mark all Notifications as read |
| PUT | /notifications/{id}/unread | Update Notification's read status |
| GET | /notifications/{id}/board | Get the Board a Notification is on |
| GET | /notifications/{id}/card | Get the Card a Notification is on |
| GET | /notifications/{id}/list | Get the List a Notification is on |
| GET | /notifications/{id}/member | Get the Member a Notification is about (not the creator) |
| GET | /notifications/{id}/memberCreator | Get the Member who created the Notification |
| GET | /notifications/{id}/organization | Get a Notification's associated Organization |

### organizations
| Method | Path | Description |
|--------|------|-------------|
| POST | /organizations | Create a new Organization |
| GET | /organizations/{id} | Get an Organization |
| PUT | /organizations/{id} | Update an Organization |
| DELETE | /organizations/{id} | Delete an Organization |
| GET | /organizations/{id}/{field} | Get field on Organization |
| GET | /organizations/{id}/actions | Get Actions for Organization |
| GET | /organizations/{id}/boards | Get Boards in an Organization |
| POST | /organizations/{id}/exports | Create Export for Organizations |
| GET | /organizations/{id}/exports | Retrieve Organization's Exports |
| GET | /organizations/{id}/members | Get the Members of an Organization |
| PUT | /organizations/{id}/members | Update an Organization's Members |
| GET | /organizations/{id}/memberships | Get Memberships of an Organization |
| GET | /organizations/{id}/memberships/{idMembership} | Get a Membership of an Organization |
| GET | /organizations/{id}/pluginData | Get the pluginData Scoped to Organization |
| GET | /organizations/{id}/tags | Get Tags of an Organization |
| POST | /organizations/{id}/tags | Create a Tag in Organization |
| PUT | /organizations/{id}/members/{idMember} | Update a Member of an Organization |
| DELETE | /organizations/{id}/members/{idMember} | Remove a Member from an Organization |
| PUT | /organizations/{id}/members/{idMember}/deactivated | Deactivate or reactivate a member of an Organization |
| POST | /organizations/{id}/logo | Update logo for an Organization |
| DELETE | /organizations/{id}/logo | Delete Logo for Organization |
| DELETE | /organizations/{id}/members/{idMember}/all | Remove a Member from an Organization and all Organization Boards |
| DELETE | /organizations/{id}/prefs/associatedDomain | Remove the associated Google Apps domain from a Workspace |
| DELETE | /organizations/{id}/prefs/orgInviteRestrict | Delete the email domain restriction on who can be invited to the Workspace |
| DELETE | /organizations/{id}/tags/{idTag} | Delete an Organization's Tag |
| GET | /organizations/{id}/newBillableGuests/{idBoard} | Get Organizations new billable guests |

### plugins
| Method | Path | Description |
|--------|------|-------------|
| GET | /plugins/{id}/ | Get a Plugin |
| PUT | /plugins/{id}/ | Update a Plugin |
| POST | /plugins/{idPlugin}/listing | Create a Listing for Plugin |
| GET | /plugins/{id}/compliance/memberPrivacy | Get Plugin's Member privacy compliance |
| PUT | /plugins/{idPlugin}/listings/{idListing} | Updating Plugin's Listing |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | Search Trello |
| GET | /search/members/ | Search for Members |

### tokens
| Method | Path | Description |
|--------|------|-------------|
| GET | /tokens/{token} | Get a Token |
| GET | /tokens/{token}/member | Get Token's Member |
| GET | /tokens/{token}/webhooks | Get Webhooks for Token |
| POST | /tokens/{token}/webhooks | Create Webhooks for Token |
| GET | /tokens/{token}/webhooks/{idWebhook} | Get a Webhook belonging to a Token |
| DELETE | /tokens/{token}/webhooks/{idWebhook} | Delete a Webhook created by Token |
| PUT | /tokens/{token}/webhooks/{idWebhook} | Update a Webhook created by Token |
| DELETE | /tokens/{token}/ | Delete a Token |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| POST | /webhooks/ | Create a Webhook |
| GET | /webhooks/{id} | Get a Webhook |
| PUT | /webhooks/{id} | Update a Webhook |
| DELETE | /webhooks/{id} | Delete a Webhook |
| GET | /webhooks/{id}/{field} | Get a field on a Webhook |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get action details?" -> GET /actions/{id}
- "Update a action?" -> PUT /actions/{id}
- "Delete a action?" -> DELETE /actions/{id}
- "Get action details?" -> GET /actions/{id}/{field}
- "List all board?" -> GET /actions/{id}/board
- "List all card?" -> GET /actions/{id}/card
- "List all list?" -> GET /actions/{id}/list
- "List all member?" -> GET /actions/{id}/member
- "List all memberCreator?" -> GET /actions/{id}/memberCreator
- "List all organization?" -> GET /actions/{id}/organization
- "List all reactions?" -> GET /actions/{idAction}/reactions
- "Create a reaction?" -> POST /actions/{idAction}/reactions
- "Get reaction details?" -> GET /actions/{idAction}/reactions/{id}
- "Delete a reaction?" -> DELETE /actions/{idAction}/reactions/{id}
- "List all reactionsSummary?" -> GET /actions/{idAction}/reactionsSummary
- "List all compliance?" -> GET /applications/{key}/compliance
- "List all batch?" -> GET /batch
- "List all memberships?" -> GET /boards/{id}/memberships
- "Get board details?" -> GET /boards/{id}
- "Update a board?" -> PUT /boards/{id}
- "Delete a board?" -> DELETE /boards/{id}
- "Get board details?" -> GET /boards/{id}/{field}
- "List all actions?" -> GET /boards/{boardId}/actions
- "List all boardStars?" -> GET /boards/{boardId}/boardStars
- "List all checklists?" -> GET /boards/{id}/checklists
- "List all cards?" -> GET /boards/{id}/cards
- "Get card details?" -> GET /boards/{id}/cards/{filter}
- "List all customFields?" -> GET /boards/{id}/customFields
- "List all labels?" -> GET /boards/{id}/labels
- "Create a label?" -> POST /boards/{id}/labels
- "List all lists?" -> GET /boards/{id}/lists
- "Create a list?" -> POST /boards/{id}/lists
- "Get list details?" -> GET /boards/{id}/lists/{filter}
- "List all members?" -> GET /boards/{id}/members
- "Update a member?" -> PUT /boards/{id}/members/{idMember}
- "Delete a member?" -> DELETE /boards/{id}/members/{idMember}
- "Update a membership?" -> PUT /boards/{id}/memberships/{idMembership}
- "Create a board?" -> POST /boards/
- "Create a generate?" -> POST /boards/{id}/calendarKey/generate
- "Create a generate?" -> POST /boards/{id}/emailKey/generate
- "Create a idTag?" -> POST /boards/{id}/idTags
- "Create a markedAsViewed?" -> POST /boards/{id}/markedAsViewed
- "List all boardPlugins?" -> GET /boards/{id}/boardPlugins
- "Create a boardPlugin?" -> POST /boards/{id}/boardPlugins
- "Delete a boardPlugin?" -> DELETE /boards/{id}/boardPlugins/{idPlugin}
- "List all plugins?" -> GET /boards/{id}/plugins
- "Create a card?" -> POST /cards
- "Get card details?" -> GET /cards/{id}
- "Update a card?" -> PUT /cards/{id}
- "Delete a card?" -> DELETE /cards/{id}
- "Get card details?" -> GET /cards/{id}/{field}
- "List all actions?" -> GET /cards/{id}/actions
- "List all attachments?" -> GET /cards/{id}/attachments
- "Create a attachment?" -> POST /cards/{id}/attachments
- "Get attachment details?" -> GET /cards/{id}/attachments/{idAttachment}
- "Delete a attachment?" -> DELETE /cards/{id}/attachments/{idAttachment}
- "List all board?" -> GET /cards/{id}/board
- "List all checkItemStates?" -> GET /cards/{id}/checkItemStates
- "List all checklists?" -> GET /cards/{id}/checklists
- "Create a checklist?" -> POST /cards/{id}/checklists
- "Get checkItem details?" -> GET /cards/{id}/checkItem/{idCheckItem}
- "Update a checkItem?" -> PUT /cards/{id}/checkItem/{idCheckItem}
- "Delete a checkItem?" -> DELETE /cards/{id}/checkItem/{idCheckItem}
- "List all list?" -> GET /cards/{id}/list
- "List all members?" -> GET /cards/{id}/members
- "List all membersVoted?" -> GET /cards/{id}/membersVoted
- "Create a membersVoted?" -> POST /cards/{id}/membersVoted
- "List all pluginData?" -> GET /cards/{id}/pluginData
- "List all stickers?" -> GET /cards/{id}/stickers
- "Create a sticker?" -> POST /cards/{id}/stickers
- "Get sticker details?" -> GET /cards/{id}/stickers/{idSticker}
- "Delete a sticker?" -> DELETE /cards/{id}/stickers/{idSticker}
- "Update a sticker?" -> PUT /cards/{id}/stickers/{idSticker}
- "List all customFieldItems?" -> GET /cards/{id}/customFieldItems
- "Create a comment?" -> POST /cards/{id}/actions/comments
- "Create a idLabel?" -> POST /cards/{id}/idLabels
- "Create a idMember?" -> POST /cards/{id}/idMembers
- "Create a label?" -> POST /cards/{id}/labels
- "Create a markAssociatedNotificationsRead?" -> POST /cards/{id}/markAssociatedNotificationsRead
- "Delete a idLabel?" -> DELETE /cards/{id}/idLabels/{idLabel}
- "Delete a idMember?" -> DELETE /cards/{id}/idMembers/{idMember}
- "Delete a membersVoted?" -> DELETE /cards/{id}/membersVoted/{idMember}
- "Update a checkItem?" -> PUT /cards/{idCard}/checklist/{idChecklist}/checkItem/{idCheckItem}
- "Delete a checklist?" -> DELETE /cards/{id}/checklists/{idChecklist}
- "Create a checklist?" -> POST /checklists
- "Get checklist details?" -> GET /checklists/{id}
- "Update a checklist?" -> PUT /checklists/{id}
- "Delete a checklist?" -> DELETE /checklists/{id}
- "Get checklist details?" -> GET /checklists/{id}/{field}
- "Update a checklist?" -> PUT /checklists/{id}/{field}
- "List all board?" -> GET /checklists/{id}/board
- "List all cards?" -> GET /checklists/{id}/cards
- "List all checkItems?" -> GET /checklists/{id}/checkItems
- "Create a checkItem?" -> POST /checklists/{id}/checkItems
- "Get checkItem details?" -> GET /checklists/{id}/checkItems/{idCheckItem}
- "Delete a checkItem?" -> DELETE /checklists/{id}/checkItems/{idCheckItem}
- "Create a customField?" -> POST /customFields
- "Get customField details?" -> GET /customFields/{id}
- "Update a customField?" -> PUT /customFields/{id}
- "Delete a customField?" -> DELETE /customFields/{id}
- "Create a option?" -> POST /customFields/{id}/options
- "List all options?" -> GET /customFields/{id}/options
- "Get option details?" -> GET /customFields/{id}/options/{idCustomFieldOption}
- "Delete a option?" -> DELETE /customFields/{id}/options/{idCustomFieldOption}
- "List all emoji?" -> GET /emoji
- "Get enterprise details?" -> GET /enterprises/{id}
- "List all auditlog?" -> GET /enterprises/{id}/auditlog
- "List all admins?" -> GET /enterprises/{id}/admins
- "List all signupUrl?" -> GET /enterprises/{id}/signupUrl
- "Search query?" -> GET /enterprises/{id}/members/query
- "List all members?" -> GET /enterprises/{id}/members
- "Get member details?" -> GET /enterprises/{id}/members/{idMember}
- "Get organization details?" -> GET /enterprises/{id}/transferrable/organization/{idOrganization}
- "Get bulk details?" -> GET /enterprises/{id}/transferrable/bulk/{idOrganizations}
- "List all claimableOrganizations?" -> GET /enterprises/{id}/claimableOrganizations
- "List all pendingOrganizations?" -> GET /enterprises/{id}/pendingOrganizations
- "Create a token?" -> POST /enterprises/{id}/tokens
- "List all organizations?" -> GET /enterprises/{id}/organizations
- "Update a admin?" -> PUT /enterprises/{id}/admins/{idMember}
- "Delete a admin?" -> DELETE /enterprises/{id}/admins/{idMember}
- "Delete a organization?" -> DELETE /enterprises/{id}/organizations/{idOrg}
- "Get bulk details?" -> GET /enterprises/{id}/organizations/bulk/{idOrganizations}
- "Get label details?" -> GET /labels/{id}
- "Update a label?" -> PUT /labels/{id}
- "Delete a label?" -> DELETE /labels/{id}
- "Update a label?" -> PUT /labels/{id}/{field}
- "Create a label?" -> POST /labels
- "Get list details?" -> GET /lists/{id}
- "Update a list?" -> PUT /lists/{id}
- "Create a list?" -> POST /lists
- "Create a archiveAllCard?" -> POST /lists/{id}/archiveAllCards
- "Create a moveAllCard?" -> POST /lists/{id}/moveAllCards
- "Update a list?" -> PUT /lists/{id}/{field}
- "List all actions?" -> GET /lists/{id}/actions
- "List all board?" -> GET /lists/{id}/board
- "List all cards?" -> GET /lists/{id}/cards
- "Get member details?" -> GET /members/{id}
- "Update a member?" -> PUT /members/{id}
- "Get member details?" -> GET /members/{id}/{field}
- "List all actions?" -> GET /members/{id}/actions
- "List all boardBackgrounds?" -> GET /members/{id}/boardBackgrounds
- "Create a boardBackground?" -> POST /members/{id}/boardBackgrounds
- "Get boardBackground details?" -> GET /members/{id}/boardBackgrounds/{idBackground}
- "Update a boardBackground?" -> PUT /members/{id}/boardBackgrounds/{idBackground}
- "Delete a boardBackground?" -> DELETE /members/{id}/boardBackgrounds/{idBackground}
- "List all boardStars?" -> GET /members/{id}/boardStars
- "Create a boardStar?" -> POST /members/{id}/boardStars
- "Get boardStar details?" -> GET /members/{id}/boardStars/{idStar}
- "Update a boardStar?" -> PUT /members/{id}/boardStars/{idStar}
- "Delete a boardStar?" -> DELETE /members/{id}/boardStars/{idStar}
- "List all boards?" -> GET /members/{id}/boards
- "List all boardsInvited?" -> GET /members/{id}/boardsInvited
- "List all cards?" -> GET /members/{id}/cards
- "List all customBoardBackgrounds?" -> GET /members/{id}/customBoardBackgrounds
- "Create a customBoardBackground?" -> POST /members/{id}/customBoardBackgrounds
- "Get customBoardBackground details?" -> GET /members/{id}/customBoardBackgrounds/{idBackground}
- "Update a customBoardBackground?" -> PUT /members/{id}/customBoardBackgrounds/{idBackground}
- "Delete a customBoardBackground?" -> DELETE /members/{id}/customBoardBackgrounds/{idBackground}
- "List all customEmoji?" -> GET /members/{id}/customEmoji
- "Create a customEmoji?" -> POST /members/{id}/customEmoji
- "Get customEmoji details?" -> GET /members/{id}/customEmoji/{idEmoji}
- "List all customStickers?" -> GET /members/{id}/customStickers
- "Create a customSticker?" -> POST /members/{id}/customStickers
- "Get customSticker details?" -> GET /members/{id}/customStickers/{idSticker}
- "Delete a customSticker?" -> DELETE /members/{id}/customStickers/{idSticker}
- "List all notifications?" -> GET /members/{id}/notifications
- "List all organizations?" -> GET /members/{id}/organizations
- "List all organizationsInvited?" -> GET /members/{id}/organizationsInvited
- "List all savedSearches?" -> GET /members/{id}/savedSearches
- "Create a savedSearche?" -> POST /members/{id}/savedSearches
- "Get savedSearche details?" -> GET /members/{id}/savedSearches/{idSearch}
- "Update a savedSearche?" -> PUT /members/{id}/savedSearches/{idSearch}
- "Delete a savedSearche?" -> DELETE /members/{id}/savedSearches/{idSearch}
- "List all tokens?" -> GET /members/{id}/tokens
- "Create a avatar?" -> POST /members/{id}/avatar
- "Create a oneTimeMessagesDismissed?" -> POST /members/{id}/oneTimeMessagesDismissed
- "List all notificationsChannelSettings?" -> GET /members/{id}/notificationsChannelSettings
- "Get notificationsChannelSetting details?" -> GET /members/{id}/notificationsChannelSettings/{channel}
- "Update a notificationsChannelSetting?" -> PUT /members/{id}/notificationsChannelSettings/{channel}
- "Update a notificationsChannelSetting?" -> PUT /members/{id}/notificationsChannelSettings/{channel}/{blockedKeys}
- "Get notification details?" -> GET /notifications/{id}
- "Update a notification?" -> PUT /notifications/{id}
- "Get notification details?" -> GET /notifications/{id}/{field}
- "Create a read?" -> POST /notifications/all/read
- "List all board?" -> GET /notifications/{id}/board
- "List all card?" -> GET /notifications/{id}/card
- "List all list?" -> GET /notifications/{id}/list
- "List all member?" -> GET /notifications/{id}/member
- "List all memberCreator?" -> GET /notifications/{id}/memberCreator
- "List all organization?" -> GET /notifications/{id}/organization
- "Create a organization?" -> POST /organizations
- "Get organization details?" -> GET /organizations/{id}
- "Update a organization?" -> PUT /organizations/{id}
- "Delete a organization?" -> DELETE /organizations/{id}
- "Get organization details?" -> GET /organizations/{id}/{field}
- "List all actions?" -> GET /organizations/{id}/actions
- "List all boards?" -> GET /organizations/{id}/boards
- "Create a export?" -> POST /organizations/{id}/exports
- "List all exports?" -> GET /organizations/{id}/exports
- "List all members?" -> GET /organizations/{id}/members
- "List all memberships?" -> GET /organizations/{id}/memberships
- "Get membership details?" -> GET /organizations/{id}/memberships/{idMembership}
- "List all pluginData?" -> GET /organizations/{id}/pluginData
- "List all tags?" -> GET /organizations/{id}/tags
- "Create a tag?" -> POST /organizations/{id}/tags
- "Update a member?" -> PUT /organizations/{id}/members/{idMember}
- "Delete a member?" -> DELETE /organizations/{id}/members/{idMember}
- "Create a logo?" -> POST /organizations/{id}/logo
- "Delete a tag?" -> DELETE /organizations/{id}/tags/{idTag}
- "Get newBillableGuest details?" -> GET /organizations/{id}/newBillableGuests/{idBoard}
- "Get plugin details?" -> GET /plugins/{id}/
- "Update a plugin?" -> PUT /plugins/{id}/
- "Create a listing?" -> POST /plugins/{idPlugin}/listing
- "List all memberPrivacy?" -> GET /plugins/{id}/compliance/memberPrivacy
- "Update a listing?" -> PUT /plugins/{idPlugin}/listings/{idListing}
- "Search search?" -> GET /search
- "Search members?" -> GET /search/members/
- "Get token details?" -> GET /tokens/{token}
- "List all member?" -> GET /tokens/{token}/member
- "List all webhooks?" -> GET /tokens/{token}/webhooks
- "Create a webhook?" -> POST /tokens/{token}/webhooks
- "Get webhook details?" -> GET /tokens/{token}/webhooks/{idWebhook}
- "Delete a webhook?" -> DELETE /tokens/{token}/webhooks/{idWebhook}
- "Update a webhook?" -> PUT /tokens/{token}/webhooks/{idWebhook}
- "Delete a token?" -> DELETE /tokens/{token}/
- "Create a webhook?" -> POST /webhooks/
- "Get webhook details?" -> GET /webhooks/{id}
- "Update a webhook?" -> PUT /webhooks/{id}
- "Delete a webhook?" -> DELETE /webhooks/{id}
- "Get webhook details?" -> GET /webhooks/{id}/{field}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
