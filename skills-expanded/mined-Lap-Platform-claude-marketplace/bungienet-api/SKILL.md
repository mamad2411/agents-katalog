---
name: bungienet-api
description: "Bungie.Net API skill. Use when working with Bungie.Net for App, User, Content. Covers 135 endpoints."
version: 1.0.0
generator: lapsh
---

# Bungie.Net API
API version: 2.21.9

## Auth
ApiKey X-API-Key in header | OAuth2

## Base URL
https://www.bungie.net/Platform

## Setup
1. Set your API key in the appropriate header
2. GET /App/FirstParty/ -- verify access
3. POST /User/Search/GlobalName/{page}/ -- create first GlobalName

## Endpoints

135 endpoints across 15 groups. See references/api-spec.lap for full details.

### App
| Method | Path | Description |
|--------|------|-------------|
| GET | /App/ApiUsage/{applicationId}/ | Get API usage by application for time frame specified. You can go as far back as 30 days ago, and can ask for up to a 48 hour window of time in a single request. You must be authenticated with at least the ReadUserData permission to access this endpoint. |
| GET | /App/FirstParty/ | Get list of applications created by Bungie. |

### User
| Method | Path | Description |
|--------|------|-------------|
| GET | /User/GetBungieNetUserById/{id}/ | Loads a bungienet user by membership id. |
| GET | /User/GetSanitizedPlatformDisplayNames/{membershipId}/ | Gets a list of all display names linked to this membership id but sanitized (profanity filtered). Obeys all visibility rules of calling user and is heavily cached. |
| GET | /User/GetCredentialTypesForTargetAccount/{membershipId}/ | Returns a list of credential types attached to the requested account |
| GET | /User/GetAvailableThemes/ | Returns a list of all available user themes. |
| GET | /User/GetMembershipsById/{membershipId}/{membershipType}/ | Returns a list of accounts associated with the supplied membership ID and membership type. This will include all linked accounts (even when hidden) if supplied credentials permit it. |
| GET | /User/GetMembershipsForCurrentUser/ | Returns a list of accounts associated with signed in user. This is useful for OAuth implementations that do not give you access to the token response. |
| GET | /User/GetMembershipFromHardLinkedCredential/{crType}/{credential}/ | Gets any hard linked membership given a credential. Only works for credentials that are public (just SteamID64 right now). Cross Save aware. |
| GET | /User/Search/Prefix/{displayNamePrefix}/{page}/ | [OBSOLETE] Do not use this to search users, use SearchByGlobalNamePost instead. |
| POST | /User/Search/GlobalName/{page}/ | Given the prefix of a global display name, returns all users who share that name. |

### Content
| Method | Path | Description |
|--------|------|-------------|
| GET | /Content/GetContentType/{type}/ | Gets an object describing a particular variant of content. |
| GET | /Content/GetContentById/{id}/{locale}/ | Returns a content item referenced by id |
| GET | /Content/GetContentByTagAndType/{tag}/{type}/{locale}/ | Returns the newest item that matches a given tag and Content Type. |
| GET | /Content/Search/{locale}/ | Gets content based on querystring information passed in. Provides basic search and text search capabilities. |
| GET | /Content/SearchContentByTagAndType/{tag}/{type}/{locale}/ | Searches for Content Items that match the given Tag and Content Type. |
| GET | /Content/SearchHelpArticles/{searchtext}/{size}/ | Search for Help Articles. |
| GET | /Content/Rss/NewsArticles/{pageToken}/ | Returns a JSON string response that is the RSS feed for news articles. |

### Forum
| Method | Path | Description |
|--------|------|-------------|
| GET | /Forum/GetTopicsPaged/{page}/{pageSize}/{group}/{sort}/{quickDate}/{categoryFilter}/ | Get topics from any forum. |
| GET | /Forum/GetCoreTopicsPaged/{page}/{sort}/{quickDate}/{categoryFilter}/ | Gets a listing of all topics marked as part of the core group. |
| GET | /Forum/GetPostsThreadedPaged/{parentPostId}/{page}/{pageSize}/{replySize}/{getParentPost}/{rootThreadMode}/{sortMode}/ | Returns a thread of posts at the given parent, optionally returning replies to those posts as well as the original parent. |
| GET | /Forum/GetPostsThreadedPagedFromChild/{childPostId}/{page}/{pageSize}/{replySize}/{rootThreadMode}/{sortMode}/ | Returns a thread of posts starting at the topicId of the input childPostId, optionally returning replies to those posts as well as the original parent. |
| GET | /Forum/GetPostAndParent/{childPostId}/ | Returns the post specified and its immediate parent. |
| GET | /Forum/GetPostAndParentAwaitingApproval/{childPostId}/ | Returns the post specified and its immediate parent of posts that are awaiting approval. |
| GET | /Forum/GetTopicForContent/{contentId}/ | Gets the post Id for the given content item's comments, if it exists. |
| GET | /Forum/GetForumTagSuggestions/ | Gets tag suggestions based on partial text entry, matching them with other tags previously used in the forums. |
| GET | /Forum/Poll/{topicId}/ | Gets the specified forum poll. |
| POST | /Forum/Recruit/Summaries/ | Allows the caller to get a list of to 25 recruitment thread summary information objects. |

### GroupV2
| Method | Path | Description |
|--------|------|-------------|
| GET | /GroupV2/GetAvailableAvatars/ | Returns a list of all available group avatars for the signed-in user. |
| GET | /GroupV2/GetAvailableThemes/ | Returns a list of all available group themes. |
| GET | /GroupV2/GetUserClanInviteSetting/{mType}/ | Gets the state of the user's clan invite preferences for a particular membership type - true if they wish to be invited to clans, false otherwise. |
| POST | /GroupV2/Recommended/{groupType}/{createDateRange}/ | Gets groups recommended for you based on the groups to whom those you follow belong. |
| POST | /GroupV2/Search/ | Search for Groups. |
| GET | /GroupV2/{groupId}/ | Get information about a specific group of the given ID. |
| GET | /GroupV2/Name/{groupName}/{groupType}/ | Get information about a specific group with the given name and type. |
| POST | /GroupV2/NameV2/ | Get information about a specific group with the given name and type. The POST version. |
| GET | /GroupV2/{groupId}/OptionalConversations/ | Gets a list of available optional conversation channels and their settings. |
| POST | /GroupV2/{groupId}/Edit/ | Edit an existing group. You must have suitable permissions in the group to perform this operation. This latest revision will only edit the fields you pass in - pass null for properties you want to leave unaltered. |
| POST | /GroupV2/{groupId}/EditClanBanner/ | Edit an existing group's clan banner. You must have suitable permissions in the group to perform this operation. All fields are required. |
| POST | /GroupV2/{groupId}/EditFounderOptions/ | Edit group options only available to a founder. You must have suitable permissions in the group to perform this operation. |
| POST | /GroupV2/{groupId}/OptionalConversations/Add/ | Add a new optional conversation/chat channel. Requires admin permissions to the group. |
| POST | /GroupV2/{groupId}/OptionalConversations/Edit/{conversationId}/ | Edit the settings of an optional conversation/chat channel. Requires admin permissions to the group. |
| GET | /GroupV2/{groupId}/Members/ | Get the list of members in a given group. |
| GET | /GroupV2/{groupId}/AdminsAndFounder/ | Get the list of members in a given group who are of admin level or higher. |
| POST | /GroupV2/{groupId}/Members/{membershipType}/{membershipId}/SetMembershipType/{memberType}/ | Edit the membership type of a given member. You must have suitable permissions in the group to perform this operation. |
| POST | /GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Kick/ | Kick a member from the given group, forcing them to reapply if they wish to re-join the group. You must have suitable permissions in the group to perform this operation. |
| POST | /GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Ban/ | Bans the requested member from the requested group for the specified period of time. |
| POST | /GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Unban/ | Unbans the requested member, allowing them to re-apply for membership. |
| GET | /GroupV2/{groupId}/Banned/ | Get the list of banned members in a given group. Only accessible to group Admins and above. Not applicable to all groups. Check group features. |
| GET | /GroupV2/{groupId}/EditHistory/ | Get the list of edits made to a given group. Only accessible to group Admins and above. |
| POST | /GroupV2/{groupId}/Admin/AbdicateFoundership/{membershipType}/{founderIdNew}/ | An administrative method to allow the founder of a group or clan to give up their position to another admin permanently. |
| GET | /GroupV2/{groupId}/Members/Pending/ | Get the list of users who are awaiting a decision on their application to join a given group. Modified to include application info. |
| GET | /GroupV2/{groupId}/Members/InvitedIndividuals/ | Get the list of users who have been invited into the group. |
| POST | /GroupV2/{groupId}/Members/ApproveAll/ | Approve all of the pending users for the given group. |
| POST | /GroupV2/{groupId}/Members/DenyAll/ | Deny all of the pending users for the given group. |
| POST | /GroupV2/{groupId}/Members/ApproveList/ | Approve all of the pending users for the given group. |
| POST | /GroupV2/{groupId}/Members/Approve/{membershipType}/{membershipId}/ | Approve the given membershipId to join the group/clan as long as they have applied. |
| POST | /GroupV2/{groupId}/Members/DenyList/ | Deny all of the pending users for the given group that match the passed-in . |
| GET | /GroupV2/User/{membershipType}/{membershipId}/{filter}/{groupType}/ | Get information about the groups that a given member has joined. |
| GET | /GroupV2/Recover/{membershipType}/{membershipId}/{groupType}/ | Allows a founder to manually recover a group they can see in game but not on bungie.net |
| GET | /GroupV2/User/Potential/{membershipType}/{membershipId}/{filter}/{groupType}/ | Get information about the groups that a given member has applied to or been invited to. |
| POST | /GroupV2/{groupId}/Members/IndividualInvite/{membershipType}/{membershipId}/ | Invite a user to join this group. |
| POST | /GroupV2/{groupId}/Members/IndividualInviteCancel/{membershipType}/{membershipId}/ | Cancels a pending invitation to join a group. |

### Tokens
| Method | Path | Description |
|--------|------|-------------|
| POST | /Tokens/Partner/ForceDropsRepair/ | Twitch Drops self-repair function - scans twitch for drops not marked as fulfilled and resyncs them. |
| POST | /Tokens/Partner/ClaimOffer/ | Claim a partner offer as the authenticated user. |
| POST | /Tokens/Partner/ApplyMissingOffers/{partnerApplicationId}/{targetBnetMembershipId}/ | Apply a partner offer to the targeted user. This endpoint does not claim a new offer, but any already claimed offers will be applied to the game if not already. |
| GET | /Tokens/Partner/History/{partnerApplicationId}/{targetBnetMembershipId}/ | Returns the partner sku and offer history of the targeted user. Elevated permissions are required to see users that are not yourself. |
| GET | /Tokens/Partner/History/{targetBnetMembershipId}/Application/{partnerApplicationId}/ | Returns the partner rewards history of the targeted user, both partner offers and Twitch drops. |
| GET | /Tokens/Rewards/GetRewardsForUser/{membershipId}/ | Returns the bungie rewards for the targeted user. |
| GET | /Tokens/Rewards/GetRewardsForPlatformUser/{membershipId}/{membershipType}/ | Returns the bungie rewards for the targeted user when a platform membership Id and Type are used. |
| GET | /Tokens/Rewards/BungieRewards/ | Returns a list of the current bungie rewards |

### Destiny2
| Method | Path | Description |
|--------|------|-------------|
| GET | /Destiny2/Manifest/ | Returns the current version of the manifest as a json object. |
| GET | /Destiny2/Manifest/{entityType}/{hashIdentifier}/ | Returns the static definition of an entity of the given Type and hash identifier. Examine the API Documentation for the Type Names of entities that have their own definitions. Note that the return type will always *inherit from* DestinyDefinition, but the specific type returned will be the requested entity type if it can be found. Please don't use this as a chatty alternative to the Manifest database if you require large sets of data, but for simple and one-off accesses this should be handy. |
| POST | /Destiny2/SearchDestinyPlayerByBungieName/{membershipType}/ | Returns a list of Destiny memberships given a global Bungie Display Name. This method will hide overridden memberships due to cross save. |
| GET | /Destiny2/{membershipType}/Profile/{membershipId}/LinkedProfiles/ | Returns a summary information about all profiles linked to the requesting membership type/membership ID that have valid Destiny information. The passed-in Membership Type/Membership ID may be a Bungie.Net membership or a Destiny membership. It only returns the minimal amount of data to begin making more substantive requests, but will hopefully serve as a useful alternative to UserServices for people who just care about Destiny data. Note that it will only return linked accounts whose linkages you are allowed to view. |
| GET | /Destiny2/{membershipType}/Profile/{destinyMembershipId}/ | Returns Destiny Profile information for the supplied membership. |
| GET | /Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/ | Returns character information for the supplied character. |
| GET | /Destiny2/Clan/{groupId}/WeeklyRewardState/ | Returns information on the weekly clan rewards and if the clan has earned them or not. Note that this will always report rewards as not redeemed. |
| GET | /Destiny2/Clan/ClanBannerDictionary/ | Returns the dictionary of values for the Clan Banner |
| GET | /Destiny2/{membershipType}/Profile/{destinyMembershipId}/Item/{itemInstanceId}/ | Retrieve the details of an instanced Destiny Item. An instanced Destiny item is one with an ItemInstanceId. Non-instanced items, such as materials, have no useful instance-specific details and thus are not queryable here. |
| GET | /Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/ | Get currently available vendors from the list of vendors that can possibly have rotating inventory. Note that this does not include things like preview vendors and vendors-as-kiosks, neither of whom have rotating/dynamic inventories. Use their definitions as-is for those. |
| GET | /Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/{vendorHash}/ | Get the details of a specific Vendor. |
| GET | /Destiny2/Vendors/ | Get items available from vendors where the vendors have items for sale that are common for everyone. If any portion of the Vendor's available inventory is character or account specific, we will be unable to return their data from this endpoint due to the way that available inventory is computed. As I am often guilty of saying: 'It's a long story...' |
| GET | /Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Collectibles/{collectiblePresentationNodeHash}/ | Given a Presentation Node that has Collectibles as direct descendants, this will return item details about those descendants in the context of the requesting character. |
| POST | /Destiny2/Actions/Items/TransferItem/ | Transfer an item to/from your vault. You must have a valid Destiny account. You must also pass BOTH a reference AND an instance ID if it's an instanced item. itshappening.gif |
| POST | /Destiny2/Actions/Items/PullFromPostmaster/ | Extract an item from the Postmaster, with whatever implications that may entail. You must have a valid Destiny account. You must also pass BOTH a reference AND an instance ID if it's an instanced item. |
| POST | /Destiny2/Actions/Items/EquipItem/ | Equip an item. You must have a valid Destiny Account, and either be in a social space, in orbit, or offline. |
| POST | /Destiny2/Actions/Items/EquipItems/ | Equip a list of items by itemInstanceIds. You must have a valid Destiny Account, and either be in a social space, in orbit, or offline. Any items not found on your character will be ignored. |
| POST | /Destiny2/Actions/Loadouts/EquipLoadout/ | Equip a loadout. You must have a valid Destiny Account, and either be in a social space, in orbit, or offline. |
| POST | /Destiny2/Actions/Loadouts/SnapshotLoadout/ | Snapshot a loadout with the currently equipped items. |
| POST | /Destiny2/Actions/Loadouts/UpdateLoadoutIdentifiers/ | Update the color, icon, and name of a loadout. |
| POST | /Destiny2/Actions/Loadouts/ClearLoadout/ | Clear the identifiers and items of a loadout. |
| POST | /Destiny2/Actions/Items/SetLockState/ | Set the Lock State for an instanced item. You must have a valid Destiny Account. |
| POST | /Destiny2/Actions/Items/SetTrackedState/ | Set the Tracking State for an instanced item, if that item is a Quest or Bounty. You must have a valid Destiny Account. Yeah, it's an item. |
| POST | /Destiny2/Actions/Items/InsertSocketPlug/ | Insert a plug into a socketed item. I know how it sounds, but I assure you it's much more G-rated than you might be guessing. We haven't decided yet whether this will be able to insert plugs that have side effects, but if we do it will require special scope permission for an application attempting to do so. You must have a valid Destiny Account, and either be in a social space, in orbit, or offline. Request must include proof of permission for 'InsertPlugs' from the account owner. |
| POST | /Destiny2/Actions/Items/InsertSocketPlugFree/ | Insert a 'free' plug into an item's socket. This does not require 'Advanced Write Action' authorization and is available to 3rd-party apps, but will only work on 'free and reversible' socket actions (Perks, Armor Mods, Shaders, Ornaments, etc.). You must have a valid Destiny Account, and the character must either be in a social space, in orbit, or offline. |
| GET | /Destiny2/Stats/PostGameCarnageReport/{activityId}/ | Gets the available post game carnage report for the activity ID. |
| POST | /Destiny2/Stats/PostGameCarnageReport/{activityId}/Report/ | Report a player that you met in an activity that was engaging in ToS-violating activities. Both you and the offending player must have played in the activityId passed in. Please use this judiciously and only when you have strong suspicions of violation, pretty please. |
| GET | /Destiny2/Stats/Definition/ | Gets historical stats definitions. |
| GET | /Destiny2/Stats/Leaderboards/Clans/{groupId}/ | Gets leaderboards with the signed in user's friends and the supplied destinyMembershipId as the focus. PREVIEW: This endpoint is still in beta, and may experience rough edges. The schema is in final form, but there may be bugs that prevent desirable operation. |
| GET | /Destiny2/Stats/AggregateClanStats/{groupId}/ | Gets aggregated stats for a clan using the same categories as the clan leaderboards. PREVIEW: This endpoint is still in beta, and may experience rough edges. The schema is in final form, but there may be bugs that prevent desirable operation. |
| GET | /Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats/Leaderboards/ | Gets leaderboards with the signed in user's friends and the supplied destinyMembershipId as the focus. PREVIEW: This endpoint has not yet been implemented. It is being returned for a preview of future functionality, and for public comment/suggestion/preparation. |
| GET | /Destiny2/Stats/Leaderboards/{membershipType}/{destinyMembershipId}/{characterId}/ | Gets leaderboards with the signed in user's friends and the supplied destinyMembershipId as the focus. PREVIEW: This endpoint is still in beta, and may experience rough edges. The schema is in final form, but there may be bugs that prevent desirable operation. |
| GET | /Destiny2/Armory/Search/{type}/{searchTerm}/ | Gets a page list of Destiny items. |
| GET | /Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/ | Gets historical stats for indicated character. |
| GET | /Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats/ | Gets aggregate historical stats organized around each character for a given account. |
| GET | /Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/ | Gets activity history stats for indicated character. |
| GET | /Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/UniqueWeapons/ | Gets details about unique weapon usage, including all exotic weapons. |
| GET | /Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/AggregateActivityStats/ | Gets all activities the character has participated in together with aggregate statistics for those activities. |
| GET | /Destiny2/Milestones/{milestoneHash}/Content/ | Gets custom localized content for the milestone of the given hash, if it exists. |
| GET | /Destiny2/Milestones/ | Gets public information about currently available Milestones. |
| POST | /Destiny2/Awa/Initialize/ | Initialize a request to perform an advanced write action. |
| POST | /Destiny2/Awa/AwaProvideAuthorizationResult/ | Provide the result of the user interaction. Called by the Bungie Destiny App to approve or reject a request. |
| GET | /Destiny2/Awa/GetActionToken/{correlationId}/ | Returns the action token if user approves the request. |

### CommunityContent
| Method | Path | Description |
|--------|------|-------------|
| GET | /CommunityContent/Get/{sort}/{mediaFilter}/{page}/ | Returns community content. |

### Trending
| Method | Path | Description |
|--------|------|-------------|
| GET | /Trending/Categories/ | Returns trending items for Bungie.net, collapsed into the first page of items per category. For pagination within a category, call GetTrendingCategory. |
| GET | /Trending/Categories/{categoryId}/{pageNumber}/ | Returns paginated lists of trending items for a category. |
| GET | /Trending/Details/{trendingEntryType}/{identifier}/ | Returns the detailed results for a specific trending entry. Note that trending entries are uniquely identified by a combination of *both* the TrendingEntryType *and* the identifier: the identifier alone is not guaranteed to be globally unique. |

### Fireteam
| Method | Path | Description |
|--------|------|-------------|
| GET | /Fireteam/Clan/{groupId}/ActiveCount/ | Gets a count of all active non-public fireteams for the specified clan. Maximum value returned is 25. |
| GET | /Fireteam/Clan/{groupId}/Available/{platform}/{activityType}/{dateRange}/{slotFilter}/{publicOnly}/{page}/ | Gets a listing of all of this clan's fireteams that are have available slots. Caller is not checked for join criteria so caching is maximized. |
| GET | /Fireteam/Search/Available/{platform}/{activityType}/{dateRange}/{slotFilter}/{page}/ | Gets a listing of all public fireteams starting now with open slots. Caller is not checked for join criteria so caching is maximized. |
| GET | /Fireteam/Clan/{groupId}/My/{platform}/{includeClosed}/{page}/ | Gets a listing of all fireteams that caller is an applicant, a member, or an alternate of. |
| GET | /Fireteam/Clan/{groupId}/Summary/{fireteamId}/ | Gets a specific fireteam. |

### Social
| Method | Path | Description |
|--------|------|-------------|
| GET | /Social/Friends/ | Returns your Bungie Friend list |
| GET | /Social/Friends/Requests/ | Returns your friend request queue. |
| POST | /Social/Friends/Add/{membershipId}/ | Requests a friend relationship with the target user. Any of the target user's linked membership ids are valid inputs. |
| POST | /Social/Friends/Requests/Accept/{membershipId}/ | Accepts a friend relationship with the target user. The user must be on your incoming friend request list, though no error will occur if they are not. |
| POST | /Social/Friends/Requests/Decline/{membershipId}/ | Declines a friend relationship with the target user. The user must be on your incoming friend request list, though no error will occur if they are not. |
| POST | /Social/Friends/Remove/{membershipId}/ | Remove a friend relationship with the target user. The user must be on your friend list, though no error will occur if they are not. |
| POST | /Social/Friends/Requests/Remove/{membershipId}/ | Remove a friend relationship with the target user. The user must be on your outgoing request friend list, though no error will occur if they are not. |
| GET | /Social/PlatformFriends/{friendPlatform}/{page}/ | Gets the platform friend of the requested type, with additional information if they have Bungie accounts. Must have a recent login session with said platform. |

### GetAvailableLocales
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetAvailableLocales/ | List of available localization cultures |

### Settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /Settings/ | Get the common settings used by the Bungie.Net environment. |

### UserSystemOverrides
| Method | Path | Description |
|--------|------|-------------|
| GET | /UserSystemOverrides/ | Get the user-specific system overrides that should be respected alongside common systems. |

### GlobalAlerts
| Method | Path | Description |
|--------|------|-------------|
| GET | /GlobalAlerts/ | Gets any active global alert for display in the forum banners, help pages, etc. Usually used for DOC alerts. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get ApiUsage details?" -> GET /App/ApiUsage/{applicationId}/
- "List all FirstParty?" -> GET /App/FirstParty/
- "Get GetBungieNetUserById details?" -> GET /User/GetBungieNetUserById/{id}/
- "Get GetSanitizedPlatformDisplayName details?" -> GET /User/GetSanitizedPlatformDisplayNames/{membershipId}/
- "Get GetCredentialTypesForTargetAccount details?" -> GET /User/GetCredentialTypesForTargetAccount/{membershipId}/
- "List all GetAvailableThemes?" -> GET /User/GetAvailableThemes/
- "Get GetMembershipsById details?" -> GET /User/GetMembershipsById/{membershipId}/{membershipType}/
- "List all GetMembershipsForCurrentUser?" -> GET /User/GetMembershipsForCurrentUser/
- "Get GetMembershipFromHardLinkedCredential details?" -> GET /User/GetMembershipFromHardLinkedCredential/{crType}/{credential}/
- "Get Prefix details?" -> GET /User/Search/Prefix/{displayNamePrefix}/{page}/
- "Get GetContentType details?" -> GET /Content/GetContentType/{type}/
- "Get GetContentById details?" -> GET /Content/GetContentById/{id}/{locale}/
- "Get GetContentByTagAndType details?" -> GET /Content/GetContentByTagAndType/{tag}/{type}/{locale}/
- "Get Search details?" -> GET /Content/Search/{locale}/
- "Get SearchContentByTagAndType details?" -> GET /Content/SearchContentByTagAndType/{tag}/{type}/{locale}/
- "Get SearchHelpArticle details?" -> GET /Content/SearchHelpArticles/{searchtext}/{size}/
- "Get NewsArticle details?" -> GET /Content/Rss/NewsArticles/{pageToken}/
- "Get GetTopicsPaged details?" -> GET /Forum/GetTopicsPaged/{page}/{pageSize}/{group}/{sort}/{quickDate}/{categoryFilter}/
- "Get GetCoreTopicsPaged details?" -> GET /Forum/GetCoreTopicsPaged/{page}/{sort}/{quickDate}/{categoryFilter}/
- "Get GetPostsThreadedPaged details?" -> GET /Forum/GetPostsThreadedPaged/{parentPostId}/{page}/{pageSize}/{replySize}/{getParentPost}/{rootThreadMode}/{sortMode}/
- "Get GetPostsThreadedPagedFromChild details?" -> GET /Forum/GetPostsThreadedPagedFromChild/{childPostId}/{page}/{pageSize}/{replySize}/{rootThreadMode}/{sortMode}/
- "Get GetPostAndParent details?" -> GET /Forum/GetPostAndParent/{childPostId}/
- "Get GetPostAndParentAwaitingApproval details?" -> GET /Forum/GetPostAndParentAwaitingApproval/{childPostId}/
- "Get GetTopicForContent details?" -> GET /Forum/GetTopicForContent/{contentId}/
- "List all GetForumTagSuggestions?" -> GET /Forum/GetForumTagSuggestions/
- "Get Poll details?" -> GET /Forum/Poll/{topicId}/
- "Create a Summary?" -> POST /Forum/Recruit/Summaries/
- "List all GetAvailableAvatars?" -> GET /GroupV2/GetAvailableAvatars/
- "List all GetAvailableThemes?" -> GET /GroupV2/GetAvailableThemes/
- "Get GetUserClanInviteSetting details?" -> GET /GroupV2/GetUserClanInviteSetting/{mType}/
- "Create a Search?" -> POST /GroupV2/Search/
- "Get GroupV2 details?" -> GET /GroupV2/{groupId}/
- "Get Name details?" -> GET /GroupV2/Name/{groupName}/{groupType}/
- "Create a NameV2?" -> POST /GroupV2/NameV2/
- "List all OptionalConversations?" -> GET /GroupV2/{groupId}/OptionalConversations/
- "Create a Edit?" -> POST /GroupV2/{groupId}/Edit/
- "Create a EditClanBanner?" -> POST /GroupV2/{groupId}/EditClanBanner/
- "Create a EditFounderOption?" -> POST /GroupV2/{groupId}/EditFounderOptions/
- "Create a Add?" -> POST /GroupV2/{groupId}/OptionalConversations/Add/
- "List all Members?" -> GET /GroupV2/{groupId}/Members/
- "List all AdminsAndFounder?" -> GET /GroupV2/{groupId}/AdminsAndFounder/
- "Create a Kick?" -> POST /GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Kick/
- "Create a Ban?" -> POST /GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Ban/
- "Create a Unban?" -> POST /GroupV2/{groupId}/Members/{membershipType}/{membershipId}/Unban/
- "List all Banned?" -> GET /GroupV2/{groupId}/Banned/
- "List all EditHistory?" -> GET /GroupV2/{groupId}/EditHistory/
- "List all Pending?" -> GET /GroupV2/{groupId}/Members/Pending/
- "List all InvitedIndividuals?" -> GET /GroupV2/{groupId}/Members/InvitedIndividuals/
- "Create a ApproveAll?" -> POST /GroupV2/{groupId}/Members/ApproveAll/
- "Create a DenyAll?" -> POST /GroupV2/{groupId}/Members/DenyAll/
- "Create a ApproveList?" -> POST /GroupV2/{groupId}/Members/ApproveList/
- "Create a DenyList?" -> POST /GroupV2/{groupId}/Members/DenyList/
- "Get User details?" -> GET /GroupV2/User/{membershipType}/{membershipId}/{filter}/{groupType}/
- "Get Recover details?" -> GET /GroupV2/Recover/{membershipType}/{membershipId}/{groupType}/
- "Get Potential details?" -> GET /GroupV2/User/Potential/{membershipType}/{membershipId}/{filter}/{groupType}/
- "Create a ForceDropsRepair?" -> POST /Tokens/Partner/ForceDropsRepair/
- "Create a ClaimOffer?" -> POST /Tokens/Partner/ClaimOffer/
- "Get History details?" -> GET /Tokens/Partner/History/{partnerApplicationId}/{targetBnetMembershipId}/
- "Get Application details?" -> GET /Tokens/Partner/History/{targetBnetMembershipId}/Application/{partnerApplicationId}/
- "Get GetRewardsForUser details?" -> GET /Tokens/Rewards/GetRewardsForUser/{membershipId}/
- "Get GetRewardsForPlatformUser details?" -> GET /Tokens/Rewards/GetRewardsForPlatformUser/{membershipId}/{membershipType}/
- "List all BungieRewards?" -> GET /Tokens/Rewards/BungieRewards/
- "List all Manifest?" -> GET /Destiny2/Manifest/
- "Get Manifest details?" -> GET /Destiny2/Manifest/{entityType}/{hashIdentifier}/
- "List all LinkedProfiles?" -> GET /Destiny2/{membershipType}/Profile/{membershipId}/LinkedProfiles/
- "Get Profile details?" -> GET /Destiny2/{membershipType}/Profile/{destinyMembershipId}/
- "Get Character details?" -> GET /Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/
- "List all WeeklyRewardState?" -> GET /Destiny2/Clan/{groupId}/WeeklyRewardState/
- "List all ClanBannerDictionary?" -> GET /Destiny2/Clan/ClanBannerDictionary/
- "Get Item details?" -> GET /Destiny2/{membershipType}/Profile/{destinyMembershipId}/Item/{itemInstanceId}/
- "List all Vendors?" -> GET /Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/
- "Get Vendor details?" -> GET /Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Vendors/{vendorHash}/
- "List all Vendors?" -> GET /Destiny2/Vendors/
- "Get Collectible details?" -> GET /Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}/Collectibles/{collectiblePresentationNodeHash}/
- "Create a TransferItem?" -> POST /Destiny2/Actions/Items/TransferItem/
- "Create a PullFromPostmaster?" -> POST /Destiny2/Actions/Items/PullFromPostmaster/
- "Create a EquipItem?" -> POST /Destiny2/Actions/Items/EquipItem/
- "Create a EquipItem?" -> POST /Destiny2/Actions/Items/EquipItems/
- "Create a EquipLoadout?" -> POST /Destiny2/Actions/Loadouts/EquipLoadout/
- "Create a SnapshotLoadout?" -> POST /Destiny2/Actions/Loadouts/SnapshotLoadout/
- "Create a UpdateLoadoutIdentifier?" -> POST /Destiny2/Actions/Loadouts/UpdateLoadoutIdentifiers/
- "Create a ClearLoadout?" -> POST /Destiny2/Actions/Loadouts/ClearLoadout/
- "Create a SetLockState?" -> POST /Destiny2/Actions/Items/SetLockState/
- "Create a SetTrackedState?" -> POST /Destiny2/Actions/Items/SetTrackedState/
- "Create a InsertSocketPlug?" -> POST /Destiny2/Actions/Items/InsertSocketPlug/
- "Create a InsertSocketPlugFree?" -> POST /Destiny2/Actions/Items/InsertSocketPlugFree/
- "Get PostGameCarnageReport details?" -> GET /Destiny2/Stats/PostGameCarnageReport/{activityId}/
- "Create a Report?" -> POST /Destiny2/Stats/PostGameCarnageReport/{activityId}/Report/
- "List all Definition?" -> GET /Destiny2/Stats/Definition/
- "Get Clan details?" -> GET /Destiny2/Stats/Leaderboards/Clans/{groupId}/
- "Get AggregateClanStat details?" -> GET /Destiny2/Stats/AggregateClanStats/{groupId}/
- "List all Leaderboards?" -> GET /Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats/Leaderboards/
- "Get Leaderboard details?" -> GET /Destiny2/Stats/Leaderboards/{membershipType}/{destinyMembershipId}/{characterId}/
- "Get Search details?" -> GET /Destiny2/Armory/Search/{type}/{searchTerm}/
- "List all Stats?" -> GET /Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/
- "List all Stats?" -> GET /Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats/
- "List all Activities?" -> GET /Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/
- "List all UniqueWeapons?" -> GET /Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/UniqueWeapons/
- "List all AggregateActivityStats?" -> GET /Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/AggregateActivityStats/
- "List all Content?" -> GET /Destiny2/Milestones/{milestoneHash}/Content/
- "List all Milestones?" -> GET /Destiny2/Milestones/
- "Create a Initialize?" -> POST /Destiny2/Awa/Initialize/
- "Create a AwaProvideAuthorizationResult?" -> POST /Destiny2/Awa/AwaProvideAuthorizationResult/
- "Get GetActionToken details?" -> GET /Destiny2/Awa/GetActionToken/{correlationId}/
- "Get Get details?" -> GET /CommunityContent/Get/{sort}/{mediaFilter}/{page}/
- "List all Categories?" -> GET /Trending/Categories/
- "Get Category details?" -> GET /Trending/Categories/{categoryId}/{pageNumber}/
- "Get Detail details?" -> GET /Trending/Details/{trendingEntryType}/{identifier}/
- "List all ActiveCount?" -> GET /Fireteam/Clan/{groupId}/ActiveCount/
- "Get Available details?" -> GET /Fireteam/Clan/{groupId}/Available/{platform}/{activityType}/{dateRange}/{slotFilter}/{publicOnly}/{page}/
- "Get Available details?" -> GET /Fireteam/Search/Available/{platform}/{activityType}/{dateRange}/{slotFilter}/{page}/
- "Get My details?" -> GET /Fireteam/Clan/{groupId}/My/{platform}/{includeClosed}/{page}/
- "Get Summary details?" -> GET /Fireteam/Clan/{groupId}/Summary/{fireteamId}/
- "List all Friends?" -> GET /Social/Friends/
- "List all Requests?" -> GET /Social/Friends/Requests/
- "Get PlatformFriend details?" -> GET /Social/PlatformFriends/{friendPlatform}/{page}/
- "List all GetAvailableLocales?" -> GET /GetAvailableLocales/
- "List all Settings?" -> GET /Settings/
- "List all UserSystemOverrides?" -> GET /UserSystemOverrides/
- "List all GlobalAlerts?" -> GET /GlobalAlerts/
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
