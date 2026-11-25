---
name: vimeo-api
description: "Vimeo API skill. Use when working with Vimeo for root, categories, channels. Covers 328 endpoints."
version: 1.0.0
generator: lapsh
---

# Vimeo API
API version: 3.4

## Auth
Bearer bearer | OAuth2

## Base URL
https://api.vimeo.com

## Setup
1. Set Authorization header with your Bearer token
2. GET / -- verify access
3. POST /channels -- create first channels

## Endpoints

328 endpoints across 15 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Get an API specification |

### categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /categories | Get all categories |
| GET | /categories/{category} | Get a specific category |
| GET | /categories/{category}/channels | Get all the channels in a category |
| GET | /categories/{category}/groups | Get all the groups in a category |
| GET | /categories/{category}/videos | Get all the videos in a category |
| GET | /categories/{category}/videos/{video_id} | Check for a video in a category |

### channels
| Method | Path | Description |
|--------|------|-------------|
| GET | /channels | Get all channels |
| POST | /channels | Create a channel |
| DELETE | /channels/{channel_id} | Delete a channel |
| GET | /channels/{channel_id} | Get a specific channel |
| PATCH | /channels/{channel_id} | Edit a channel |
| GET | /channels/{channel_id}/categories | Get all the categories in a channel |
| PUT | /channels/{channel_id}/categories | Add a list of categories to a channel |
| DELETE | /channels/{channel_id}/categories/{category} | Remove a category from a channel |
| PUT | /channels/{channel_id}/categories/{category} | Categorize a channel |
| DELETE | /channels/{channel_id}/moderators | Remove a list of channel moderators |
| GET | /channels/{channel_id}/moderators | Get all the moderators in a channel |
| PATCH | /channels/{channel_id}/moderators | Replace the moderators of a channel |
| PUT | /channels/{channel_id}/moderators | Add a list of channel moderators |
| GET | /channels/{channel_id}/moderators/{user_id} | Get a specific channel moderator |
| DELETE | /channels/{channel_id}/moderators/{user_id} | Remove a specific channel moderator |
| PUT | /channels/{channel_id}/moderators/{user_id} | Add a specific channel moderator |
| GET | /channels/{channel_id}/privacy/users | Get all the users who can view a private channel |
| PUT | /channels/{channel_id}/privacy/users | Permit a list of users to view a private channel |
| DELETE | /channels/{channel_id}/privacy/users/{user_id} | Restrict a user from viewing a private channel |
| PUT | /channels/{channel_id}/privacy/users/{user_id} | Permit a specific user to view a private channel |
| GET | /channels/{channel_id}/tags | Get all the tags that have been added to a channel |
| PUT | /channels/{channel_id}/tags | Add a list of tags to a channel |
| DELETE | /channels/{channel_id}/tags/{word} | Remove a tag from a channel |
| GET | /channels/{channel_id}/tags/{word} | Check if a tag has been added to a channel |
| PUT | /channels/{channel_id}/tags/{word} | Add a specific tag to a channel |
| GET | /channels/{channel_id}/users | Get all the followers of a channel |
| DELETE | /channels/{channel_id}/videos | Remove a list of videos from a channel |
| GET | /channels/{channel_id}/videos | Get all the videos in a channel |
| PUT | /channels/{channel_id}/videos | Add a list of videos to a channel |
| DELETE | /channels/{channel_id}/videos/{video_id} | Remove a specific video from a channel |
| GET | /channels/{channel_id}/videos/{video_id} | Get a specific video in a channel |
| PUT | /channels/{channel_id}/videos/{video_id} | Add a specific video to a channel |
| GET | /channels/{channel_id}/videos/{video_id}/comments | Get all the comments on a video |
| POST | /channels/{channel_id}/videos/{video_id}/comments | Add a comment to a video |
| GET | /channels/{channel_id}/videos/{video_id}/credits | Get all the credited users in a video |
| POST | /channels/{channel_id}/videos/{video_id}/credits | Credit a user in a video |
| GET | /channels/{channel_id}/videos/{video_id}/likes | Get all the users who have liked a video |
| GET | /channels/{channel_id}/videos/{video_id}/pictures | Get all the thumbnails of a video |
| POST | /channels/{channel_id}/videos/{video_id}/pictures | Add a video thumbnail |
| GET | /channels/{channel_id}/videos/{video_id}/privacy/users | Get all the users who can view a private video |
| PUT | /channels/{channel_id}/videos/{video_id}/privacy/users | Permit a list of users to view a private video |
| GET | /channels/{channel_id}/videos/{video_id}/texttracks | Get all the text tracks of a video |
| POST | /channels/{channel_id}/videos/{video_id}/texttracks | Add a text track to a video |

### contentratings
| Method | Path | Description |
|--------|------|-------------|
| GET | /contentratings | Get all content ratings |

### creativecommons
| Method | Path | Description |
|--------|------|-------------|
| GET | /creativecommons | Get all Creative Commons licenses |

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups | Get all groups |
| POST | /groups | Create a group |
| DELETE | /groups/{group_id} | Delete a group |
| GET | /groups/{group_id} | Get a specific group |
| GET | /groups/{group_id}/users | Get all the members of a group |
| GET | /groups/{group_id}/videos | Get all the videos in a group |
| DELETE | /groups/{group_id}/videos/{video_id} | Remove a video from a group |
| GET | /groups/{group_id}/videos/{video_id} | Get a specific video in a group |
| PUT | /groups/{group_id}/videos/{video_id} | Add a video to a group |

### languages
| Method | Path | Description |
|--------|------|-------------|
| GET | /languages | Get all languages |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /me | Get a user |
| PATCH | /me | Edit a user |
| GET | /me/albums | Get all the albums that belong to a user |
| POST | /me/albums | Create an album |
| DELETE | /me/albums/{album_id} | Delete an album |
| GET | /me/albums/{album_id} | Get a specific album |
| PATCH | /me/albums/{album_id} | Edit an album |
| GET | /me/albums/{album_id}/videos | Get all the videos in an album |
| PUT | /me/albums/{album_id}/videos | Replace all the videos in an album |
| DELETE | /me/albums/{album_id}/videos/{video_id} | Remove a video from an album |
| GET | /me/albums/{album_id}/videos/{video_id} | Get a specific video in an album |
| PUT | /me/albums/{album_id}/videos/{video_id} | Add a specific video to an album |
| POST | /me/albums/{album_id}/videos/{video_id}/set_album_thumbnail | Set a video as the album thumbnail |
| GET | /me/appearances | Get all the videos in which a user appears |
| GET | /me/categories | Get all the categories that a user follows |
| DELETE | /me/categories/{category} | Unsubscribe a user from a category |
| GET | /me/categories/{category} | Check if a user follows a category |
| PUT | /me/categories/{category} | Subscribe a user to a single category |
| GET | /me/channels | Get all the channels to which a user subscribes |
| DELETE | /me/channels/{channel_id} | Unsubscribe a user from a specific channel |
| GET | /me/channels/{channel_id} | Check if a user follows a channel |
| PUT | /me/channels/{channel_id} | Subscribe a user to a specific channel |
| GET | /me/customlogos | Get all the custom logos that belong to a user |
| POST | /me/customlogos | Add a custom logo |
| GET | /me/customlogos/{logo_id} | Get a specific custom logo |
| GET | /me/feed | Get all the videos in a user's feed |
| GET | /me/followers | Get all the followers of a user |
| GET | /me/following | Get all the users that a user is following |
| POST | /me/following | Follow a list of users |
| DELETE | /me/following/{follow_user_id} | Unfollow a user |
| GET | /me/following/{follow_user_id} | Check if a user is following another user |
| PUT | /me/following/{follow_user_id} | Follow a specific user |
| GET | /me/groups | Get all the groups that a user has joined |
| DELETE | /me/groups/{group_id} | Remove a user from a group |
| PUT | /me/groups/{group_id} | Add a user to a group |
| GET | /me/groups/{group_id} | Check if a user has joined a group |
| GET | /me/likes | Get all the videos that a user has liked |
| DELETE | /me/likes/{video_id} | Cause a user to unlike a video |
| GET | /me/likes/{video_id} | Check if a user has liked a video |
| PUT | /me/likes/{video_id} | Cause a user to like a video |
| GET | /me/ondemand/pages | Get all the On Demand pages of a user |
| POST | /me/ondemand/pages | Create an On Demand page |
| GET | /me/ondemand/purchases | Get all the On Demand purchases and rentals that a user has made |
| GET | /me/ondemand/purchases/{ondemand_id} | Check if a user has made a purchase or rental from an On Demand page |
| GET | /me/pictures | Get all the pictures that belong to a user |
| POST | /me/pictures | Add a user picture |
| DELETE | /me/pictures/{portraitset_id} | Delete a user picture |
| GET | /me/pictures/{portraitset_id} | Get a specific user picture |
| PATCH | /me/pictures/{portraitset_id} | Edit a user picture |
| GET | /me/portfolios | Get all the portfolios that belong to a user |
| GET | /me/portfolios/{portfolio_id} | Get a specific portfolio |
| GET | /me/portfolios/{portfolio_id}/videos | Get all the videos in a portfolio |
| DELETE | /me/portfolios/{portfolio_id}/videos/{video_id} | Remove a video from a portfolio |
| GET | /me/portfolios/{portfolio_id}/videos/{video_id} | Get a specific video in a portfolio |
| PUT | /me/portfolios/{portfolio_id}/videos/{video_id} | Add a video to a portfolio |
| GET | /me/presets | Get all the embed presets that a user has created |
| GET | /me/presets/{preset_id} | Get a specific embed preset |
| PATCH | /me/presets/{preset_id} | Edit an embed preset |
| GET | /me/presets/{preset_id}/videos | Get all the videos that have been added to an embed preset |
| GET | /me/projects | Get all the projects that belong to a user |
| POST | /me/projects | Create a project |
| DELETE | /me/projects/{project_id} | Delete a project |
| GET | /me/projects/{project_id} | Get a specific project |
| PATCH | /me/projects/{project_id} | Edit a project |
| DELETE | /me/projects/{project_id}/videos | Remove a list of videos from a project |
| GET | /me/projects/{project_id}/videos | Get all the videos in a project |
| PUT | /me/projects/{project_id}/videos | Add a list of videos to a project |
| DELETE | /me/projects/{project_id}/videos/{video_id} | Remove a specific video from a project |
| PUT | /me/projects/{project_id}/videos/{video_id} | Add a specific video to a project |
| GET | /me/videos | Get all the videos that a user has uploaded |
| POST | /me/videos | Upload a video |
| GET | /me/videos/{video_id} | Check if a user owns a video |
| DELETE | /me/watched/videos | Delete a user's watch history |
| GET | /me/watched/videos | Get all the videos that a user has watched |
| DELETE | /me/watched/videos/{video_id} | Delete a specific video from a user's watch history |
| GET | /me/watchlater | Get all the videos in a user's Watch Later queue |
| DELETE | /me/watchlater/{video_id} | Remove a video from a user's Watch Later queue |
| GET | /me/watchlater/{video_id} | Check if a user has added a specific video to their Watch Later queue |
| PUT | /me/watchlater/{video_id} | Add a video to a user's Watch Later queue |

### oauth
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth/access_token | Exchange an authorization code for an access token |
| POST | /oauth/authorize/client | Authorize a client with OAuth |
| POST | /oauth/authorize/vimeo_oauth1 | Convert OAuth 1 access tokens to OAuth 2 access tokens |
| GET | /oauth/verify | Verify an OAuth 2 token |

### ondemand
| Method | Path | Description |
|--------|------|-------------|
| GET | /ondemand/genres | Get all On Demand genres |
| GET | /ondemand/genres/{genre_id} | Get a specific On Demand genre |
| GET | /ondemand/genres/{genre_id}/pages | Get all the On Demand pages in a genre |
| GET | /ondemand/genres/{genre_id}/pages/{ondemand_id} | Get a specific On Demand page in a genre |
| DELETE | /ondemand/pages/{ondemand_id} | Delete a draft of an On Demand page |
| GET | /ondemand/pages/{ondemand_id} | Get a specific On Demand page |
| PATCH | /ondemand/pages/{ondemand_id} | Edit an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/backgrounds | Get all the backgrounds of an On Demand page |
| POST | /ondemand/pages/{ondemand_id}/backgrounds | Add a background to an On Demand page |
| DELETE | /ondemand/pages/{ondemand_id}/backgrounds/{background_id} | Remove a background from an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/backgrounds/{background_id} | Get a specific background of an On Demand page |
| PATCH | /ondemand/pages/{ondemand_id}/backgrounds/{background_id} | Edit a background of an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/genres | Get all the genres of an On Demand page |
| DELETE | /ondemand/pages/{ondemand_id}/genres/{genre_id} | Remove a genre from an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/genres/{genre_id} | Check whether an On Demand page belongs to a genre |
| PUT | /ondemand/pages/{ondemand_id}/genres/{genre_id} | Add a genre to an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/likes | Get all the users who have liked a video on an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/pictures | Get all the posters of an On Demand page |
| POST | /ondemand/pages/{ondemand_id}/pictures | Add a poster to an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/pictures/{poster_id} | Get a specific poster of an On Demand page |
| PATCH | /ondemand/pages/{ondemand_id}/pictures/{poster_id} | Edit a poster of an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/promotions | Get all the promotions on an On Demand page |
| POST | /ondemand/pages/{ondemand_id}/promotions | Add a promotion to an On Demand page |
| DELETE | /ondemand/pages/{ondemand_id}/promotions/{promotion_id} | Remove a promotion from an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/promotions/{promotion_id} | Get a specific promotion on an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/promotions/{promotion_id}/codes | Get all the codes of a promotion on an On Demand page |
| DELETE | /ondemand/pages/{ondemand_id}/regions | Remove a list of regions from an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/regions | Get all the regions of an On Demand page |
| PUT | /ondemand/pages/{ondemand_id}/regions | Add a list of regions to an On Demand page |
| DELETE | /ondemand/pages/{ondemand_id}/regions/{country} | Remove a specific region from an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/regions/{country} | Get a specific region of an On Demand page |
| PUT | /ondemand/pages/{ondemand_id}/regions/{country} | Add a specific region to an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/seasons | Get all the seasons on an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/seasons/{season_id} | Get a specific season on an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/seasons/{season_id}/videos | Get all the videos in a season on an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/videos | Get all the videos on an On Demand page |
| DELETE | /ondemand/pages/{ondemand_id}/videos/{video_id} | Remove a video from an On Demand page |
| GET | /ondemand/pages/{ondemand_id}/videos/{video_id} | Get a specific video on an On Demand page |
| PUT | /ondemand/pages/{ondemand_id}/videos/{video_id} | Add a video to an On Demand page |
| GET | /ondemand/regions | Get all the On Demand regions |
| GET | /ondemand/regions/{country} | Get a specific On Demand region |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{word} | Get a specific tag |
| GET | /tags/{word}/videos | Get all the videos with a specific tag |

### tokens
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /tokens | Revoke the current access token |

### tutorial
| Method | Path | Description |
|--------|------|-------------|
| GET | /tutorial | Get started with the Vimeo API |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | Search for users |
| GET | /users/{user_id} | Get a user |
| PATCH | /users/{user_id} | Edit a user |
| GET | /users/{user_id}/albums | Get all the albums that belong to a user |
| POST | /users/{user_id}/albums | Create an album |
| DELETE | /users/{user_id}/albums/{album_id} | Delete an album |
| GET | /users/{user_id}/albums/{album_id} | Get a specific album |
| PATCH | /users/{user_id}/albums/{album_id} | Edit an album |
| GET | /users/{user_id}/albums/{album_id}/custom_thumbnails | Get all the custom upload thumbnails of an album |
| POST | /users/{user_id}/albums/{album_id}/custom_thumbnails | Add a custom uploaded thumbnail |
| DELETE | /users/{user_id}/albums/{album_id}/custom_thumbnails/{thumbnail_id} | Remove a custom uploaded album thumbnail |
| GET | /users/{user_id}/albums/{album_id}/custom_thumbnails/{thumbnail_id} | Get a specific custom uploaded album thumbnail |
| PATCH | /users/{user_id}/albums/{album_id}/custom_thumbnails/{thumbnail_id} | Replace a custom uploaded album thumbnail |
| GET | /users/{user_id}/albums/{album_id}/logos | Get all the custom logos of an album |
| POST | /users/{user_id}/albums/{album_id}/logos | Add a custom album logo |
| DELETE | /users/{user_id}/albums/{album_id}/logos/{logo_id} | Remove a custom album logo |
| GET | /users/{user_id}/albums/{album_id}/logos/{logo_id} | Get a specific custom album logo |
| PATCH | /users/{user_id}/albums/{album_id}/logos/{logo_id} | Replace a custom album logo |
| GET | /users/{user_id}/albums/{album_id}/videos | Get all the videos in an album |
| PUT | /users/{user_id}/albums/{album_id}/videos | Replace all the videos in an album |
| DELETE | /users/{user_id}/albums/{album_id}/videos/{video_id} | Remove a video from an album |
| GET | /users/{user_id}/albums/{album_id}/videos/{video_id} | Get a specific video in an album |
| PUT | /users/{user_id}/albums/{album_id}/videos/{video_id} | Add a specific video to an album |
| POST | /users/{user_id}/albums/{album_id}/videos/{video_id}/set_album_thumbnail | Set a video as the album thumbnail |
| GET | /users/{user_id}/appearances | Get all the videos in which a user appears |
| GET | /users/{user_id}/categories | Get all the categories that a user follows |
| DELETE | /users/{user_id}/categories/{category} | Unsubscribe a user from a category |
| GET | /users/{user_id}/categories/{category} | Check if a user follows a category |
| PUT | /users/{user_id}/categories/{category} | Subscribe a user to a single category |
| GET | /users/{user_id}/channels | Get all the channels to which a user subscribes |
| DELETE | /users/{user_id}/channels/{channel_id} | Unsubscribe a user from a specific channel |
| GET | /users/{user_id}/channels/{channel_id} | Check if a user follows a channel |
| PUT | /users/{user_id}/channels/{channel_id} | Subscribe a user to a specific channel |
| GET | /users/{user_id}/customlogos | Get all the custom logos that belong to a user |
| POST | /users/{user_id}/customlogos | Add a custom logo |
| GET | /users/{user_id}/customlogos/{logo_id} | Get a specific custom logo |
| GET | /users/{user_id}/feed | Get all the videos in a user's feed |
| GET | /users/{user_id}/followers | Get all the followers of a user |
| GET | /users/{user_id}/following | Get all the users that a user is following |
| POST | /users/{user_id}/following | Follow a list of users |
| DELETE | /users/{user_id}/following/{follow_user_id} | Unfollow a user |
| GET | /users/{user_id}/following/{follow_user_id} | Check if a user is following another user |
| PUT | /users/{user_id}/following/{follow_user_id} | Follow a specific user |
| GET | /users/{user_id}/groups | Get all the groups that a user has joined |
| DELETE | /users/{user_id}/groups/{group_id} | Remove a user from a group |
| PUT | /users/{user_id}/groups/{group_id} | Add a user to a group |
| GET | /users/{user_id}/groups/{group_id} | Check if a user has joined a group |
| GET | /users/{user_id}/likes | Get all the videos that a user has liked |
| DELETE | /users/{user_id}/likes/{video_id} | Cause a user to unlike a video |
| GET | /users/{user_id}/likes/{video_id} | Check if a user has liked a video |
| PUT | /users/{user_id}/likes/{video_id} | Cause a user to like a video |
| GET | /users/{user_id}/ondemand/pages | Get all the On Demand pages of a user |
| POST | /users/{user_id}/ondemand/pages | Create an On Demand page |
| GET | /users/{user_id}/ondemand/purchases | Check if a user has made a purchase or rental from an On Demand page |
| GET | /users/{user_id}/pictures | Get all the pictures that belong to a user |
| POST | /users/{user_id}/pictures | Add a user picture |
| DELETE | /users/{user_id}/pictures/{portraitset_id} | Delete a user picture |
| GET | /users/{user_id}/pictures/{portraitset_id} | Get a specific user picture |
| PATCH | /users/{user_id}/pictures/{portraitset_id} | Edit a user picture |
| GET | /users/{user_id}/portfolios | Get all the portfolios that belong to a user |
| GET | /users/{user_id}/portfolios/{portfolio_id} | Get a specific portfolio |
| GET | /users/{user_id}/portfolios/{portfolio_id}/videos | Get all the videos in a portfolio |
| DELETE | /users/{user_id}/portfolios/{portfolio_id}/videos/{video_id} | Remove a video from a portfolio |
| GET | /users/{user_id}/portfolios/{portfolio_id}/videos/{video_id} | Get a specific video in a portfolio |
| PUT | /users/{user_id}/portfolios/{portfolio_id}/videos/{video_id} | Add a video to a portfolio |
| GET | /users/{user_id}/presets | Get all the embed presets that a user has created |
| GET | /users/{user_id}/presets/{preset_id} | Get a specific embed preset |
| PATCH | /users/{user_id}/presets/{preset_id} | Edit an embed preset |
| GET | /users/{user_id}/presets/{preset_id}/videos | Get all the videos that have been added to an embed preset |
| GET | /users/{user_id}/projects | Get all the projects that belong to a user |
| POST | /users/{user_id}/projects | Create a project |
| DELETE | /users/{user_id}/projects/{project_id} | Delete a project |
| GET | /users/{user_id}/projects/{project_id} | Get a specific project |
| PATCH | /users/{user_id}/projects/{project_id} | Edit a project |
| DELETE | /users/{user_id}/projects/{project_id}/videos | Remove a list of videos from a project |
| GET | /users/{user_id}/projects/{project_id}/videos | Get all the videos in a project |
| PUT | /users/{user_id}/projects/{project_id}/videos | Add a list of videos to a project |
| DELETE | /users/{user_id}/projects/{project_id}/videos/{video_id} | Remove a specific video from a project |
| PUT | /users/{user_id}/projects/{project_id}/videos/{video_id} | Add a specific video to a project |
| DELETE | /users/{user_id}/uploads/{upload_id} | Complete a user's streaming upload |
| GET | /users/{user_id}/uploads/{upload_id} | Get a user's upload attempt |
| GET | /users/{user_id}/videos | Get all the videos that a user has uploaded |
| POST | /users/{user_id}/videos | Upload a video |
| GET | /users/{user_id}/videos/{video_id} | Check if a user owns a video |
| GET | /users/{user_id}/watchlater | Get all the videos in a user's Watch Later queue |
| DELETE | /users/{user_id}/watchlater/{video_id} | Remove a video from a user's Watch Later queue |
| GET | /users/{user_id}/watchlater/{video_id} | Check if a user has added a specific video to their Watch Later queue |
| PUT | /users/{user_id}/watchlater/{video_id} | Add a video to a user's Watch Later queue |

### videos
| Method | Path | Description |
|--------|------|-------------|
| GET | /videos | Search for videos |
| DELETE | /videos/{video_id} | Delete a video |
| GET | /videos/{video_id} | Get a specific video |
| PATCH | /videos/{video_id} | Edit a video |
| GET | /videos/{video_id}/available_albums | Get all the albums to which a user can add or remove a specific video |
| GET | /videos/{video_id}/available_channels | Get all the channels to which a user can add or remove a specific video |
| GET | /videos/{video_id}/categories | Get all the categories to which a video belongs |
| PUT | /videos/{video_id}/categories | Suggest categories for a video |
| GET | /videos/{video_id}/comments | Get all the comments on a video |
| POST | /videos/{video_id}/comments | Add a comment to a video |
| DELETE | /videos/{video_id}/comments/{comment_id} | Delete a video comment |
| GET | /videos/{video_id}/comments/{comment_id} | Get a specific video comment |
| PATCH | /videos/{video_id}/comments/{comment_id} | Edit a video comment |
| GET | /videos/{video_id}/comments/{comment_id}/replies | Get all the replies to a video comment |
| POST | /videos/{video_id}/comments/{comment_id}/replies | Add a reply to a video comment |
| GET | /videos/{video_id}/credits | Get all the credited users in a video |
| POST | /videos/{video_id}/credits | Credit a user in a video |
| DELETE | /videos/{video_id}/credits/{credit_id} | Delete the credit for a user in a video |
| GET | /videos/{video_id}/credits/{credit_id} | Get a specific credited user in a video |
| PATCH | /videos/{video_id}/credits/{credit_id} | Edit the credit for a user in a video |
| GET | /videos/{video_id}/likes | Get all the users who have liked a video |
| GET | /videos/{video_id}/pictures | Get all the thumbnails of a video |
| POST | /videos/{video_id}/pictures | Add a video thumbnail |
| DELETE | /videos/{video_id}/pictures/{picture_id} | Delete a video thumbnail |
| GET | /videos/{video_id}/pictures/{picture_id} | Get a specific video thumbnail |
| PATCH | /videos/{video_id}/pictures/{picture_id} | Edit a video thumbnail |
| DELETE | /videos/{video_id}/presets/{preset_id} | Remove an embed preset from a video |
| GET | /videos/{video_id}/presets/{preset_id} | Check if an embed preset has been added to a video |
| PUT | /videos/{video_id}/presets/{preset_id} | Add an embed preset to a video |
| GET | /videos/{video_id}/privacy/domains | Get all the domains on a video's whitelist |
| DELETE | /videos/{video_id}/privacy/domains/{domain} | Remove a domain from a video's whitelist |
| PUT | /videos/{video_id}/privacy/domains/{domain} | Add a domain to a video's whitelist |
| GET | /videos/{video_id}/privacy/users | Get all the users who can view a private video |
| PUT | /videos/{video_id}/privacy/users | Permit a list of users to view a private video |
| DELETE | /videos/{video_id}/privacy/users/{user_id} | Restrict a user from viewing a private video |
| PUT | /videos/{video_id}/privacy/users/{user_id} | Permit a specific user to view a private video |
| GET | /videos/{video_id}/tags | Get all the tags of a video |
| PUT | /videos/{video_id}/tags | Add a list of tags to a video |
| DELETE | /videos/{video_id}/tags/{word} | Remove a tag from a video |
| GET | /videos/{video_id}/tags/{word} | Check if a tag has been added to a video |
| PUT | /videos/{video_id}/tags/{word} | Add a specific tag to a video |
| GET | /videos/{video_id}/texttracks | Get all the text tracks of a video |
| POST | /videos/{video_id}/texttracks | Add a text track to a video |
| DELETE | /videos/{video_id}/texttracks/{texttrack_id} | Delete a text track |
| GET | /videos/{video_id}/texttracks/{texttrack_id} | Get a specific text track |
| PATCH | /videos/{video_id}/texttracks/{texttrack_id} | Edit a text track |
| POST | /videos/{video_id}/timelinethumbnails | Add a new timeline event thumbnail to a video |
| GET | /videos/{video_id}/timelinethumbnails/{thumbnail_id} | Get a timeline event thumbnail |
| POST | /videos/{video_id}/versions | Add a version to a video |
| GET | /videos/{video_id}/videos | Get all the related videos of a video |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all categories?" -> GET /categories
- "Get category details?" -> GET /categories/{category}
- "Search channels?" -> GET /categories/{category}/channels
- "Search groups?" -> GET /categories/{category}/groups
- "Search videos?" -> GET /categories/{category}/videos
- "Get video details?" -> GET /categories/{category}/videos/{video_id}
- "Search channels?" -> GET /channels
- "Create a channel?" -> POST /channels
- "Delete a channel?" -> DELETE /channels/{channel_id}
- "Get channel details?" -> GET /channels/{channel_id}
- "Partially update a channel?" -> PATCH /channels/{channel_id}
- "List all categories?" -> GET /channels/{channel_id}/categories
- "Delete a category?" -> DELETE /channels/{channel_id}/categories/{category}
- "Update a category?" -> PUT /channels/{channel_id}/categories/{category}
- "Search moderators?" -> GET /channels/{channel_id}/moderators
- "Get moderator details?" -> GET /channels/{channel_id}/moderators/{user_id}
- "Delete a moderator?" -> DELETE /channels/{channel_id}/moderators/{user_id}
- "Update a moderator?" -> PUT /channels/{channel_id}/moderators/{user_id}
- "List all users?" -> GET /channels/{channel_id}/privacy/users
- "Delete a user?" -> DELETE /channels/{channel_id}/privacy/users/{user_id}
- "Update a user?" -> PUT /channels/{channel_id}/privacy/users/{user_id}
- "List all tags?" -> GET /channels/{channel_id}/tags
- "Delete a tag?" -> DELETE /channels/{channel_id}/tags/{word}
- "Get tag details?" -> GET /channels/{channel_id}/tags/{word}
- "Update a tag?" -> PUT /channels/{channel_id}/tags/{word}
- "Search users?" -> GET /channels/{channel_id}/users
- "Search videos?" -> GET /channels/{channel_id}/videos
- "Delete a video?" -> DELETE /channels/{channel_id}/videos/{video_id}
- "Get video details?" -> GET /channels/{channel_id}/videos/{video_id}
- "Update a video?" -> PUT /channels/{channel_id}/videos/{video_id}
- "List all comments?" -> GET /channels/{channel_id}/videos/{video_id}/comments
- "Create a comment?" -> POST /channels/{channel_id}/videos/{video_id}/comments
- "Search credits?" -> GET /channels/{channel_id}/videos/{video_id}/credits
- "Create a credit?" -> POST /channels/{channel_id}/videos/{video_id}/credits
- "List all likes?" -> GET /channels/{channel_id}/videos/{video_id}/likes
- "List all pictures?" -> GET /channels/{channel_id}/videos/{video_id}/pictures
- "Create a picture?" -> POST /channels/{channel_id}/videos/{video_id}/pictures
- "List all users?" -> GET /channels/{channel_id}/videos/{video_id}/privacy/users
- "List all texttracks?" -> GET /channels/{channel_id}/videos/{video_id}/texttracks
- "Create a texttrack?" -> POST /channels/{channel_id}/videos/{video_id}/texttracks
- "List all contentratings?" -> GET /contentratings
- "List all creativecommons?" -> GET /creativecommons
- "Search groups?" -> GET /groups
- "Create a group?" -> POST /groups
- "Delete a group?" -> DELETE /groups/{group_id}
- "Get group details?" -> GET /groups/{group_id}
- "Search users?" -> GET /groups/{group_id}/users
- "Search videos?" -> GET /groups/{group_id}/videos
- "Delete a video?" -> DELETE /groups/{group_id}/videos/{video_id}
- "Get video details?" -> GET /groups/{group_id}/videos/{video_id}
- "Update a video?" -> PUT /groups/{group_id}/videos/{video_id}
- "List all languages?" -> GET /languages
- "List all me?" -> GET /me
- "Search albums?" -> GET /me/albums
- "Create a album?" -> POST /me/albums
- "Delete a album?" -> DELETE /me/albums/{album_id}
- "Get album details?" -> GET /me/albums/{album_id}
- "Partially update a album?" -> PATCH /me/albums/{album_id}
- "Search videos?" -> GET /me/albums/{album_id}/videos
- "Delete a video?" -> DELETE /me/albums/{album_id}/videos/{video_id}
- "Get video details?" -> GET /me/albums/{album_id}/videos/{video_id}
- "Update a video?" -> PUT /me/albums/{album_id}/videos/{video_id}
- "Create a set_album_thumbnail?" -> POST /me/albums/{album_id}/videos/{video_id}/set_album_thumbnail
- "Search appearances?" -> GET /me/appearances
- "List all categories?" -> GET /me/categories
- "Delete a category?" -> DELETE /me/categories/{category}
- "Get category details?" -> GET /me/categories/{category}
- "Update a category?" -> PUT /me/categories/{category}
- "Search channels?" -> GET /me/channels
- "Delete a channel?" -> DELETE /me/channels/{channel_id}
- "Get channel details?" -> GET /me/channels/{channel_id}
- "Update a channel?" -> PUT /me/channels/{channel_id}
- "List all customlogos?" -> GET /me/customlogos
- "Create a customlogo?" -> POST /me/customlogos
- "Get customlogo details?" -> GET /me/customlogos/{logo_id}
- "List all feed?" -> GET /me/feed
- "Search followers?" -> GET /me/followers
- "Search following?" -> GET /me/following
- "Create a following?" -> POST /me/following
- "Delete a following?" -> DELETE /me/following/{follow_user_id}
- "Get following details?" -> GET /me/following/{follow_user_id}
- "Update a following?" -> PUT /me/following/{follow_user_id}
- "Search groups?" -> GET /me/groups
- "Delete a group?" -> DELETE /me/groups/{group_id}
- "Update a group?" -> PUT /me/groups/{group_id}
- "Get group details?" -> GET /me/groups/{group_id}
- "Search likes?" -> GET /me/likes
- "Delete a like?" -> DELETE /me/likes/{video_id}
- "Get like details?" -> GET /me/likes/{video_id}
- "Update a like?" -> PUT /me/likes/{video_id}
- "List all pages?" -> GET /me/ondemand/pages
- "Create a page?" -> POST /me/ondemand/pages
- "List all purchases?" -> GET /me/ondemand/purchases
- "Get purchase details?" -> GET /me/ondemand/purchases/{ondemand_id}
- "List all pictures?" -> GET /me/pictures
- "Create a picture?" -> POST /me/pictures
- "Delete a picture?" -> DELETE /me/pictures/{portraitset_id}
- "Get picture details?" -> GET /me/pictures/{portraitset_id}
- "Partially update a picture?" -> PATCH /me/pictures/{portraitset_id}
- "Search portfolios?" -> GET /me/portfolios
- "Get portfolio details?" -> GET /me/portfolios/{portfolio_id}
- "List all videos?" -> GET /me/portfolios/{portfolio_id}/videos
- "Delete a video?" -> DELETE /me/portfolios/{portfolio_id}/videos/{video_id}
- "Get video details?" -> GET /me/portfolios/{portfolio_id}/videos/{video_id}
- "Update a video?" -> PUT /me/portfolios/{portfolio_id}/videos/{video_id}
- "List all presets?" -> GET /me/presets
- "Get preset details?" -> GET /me/presets/{preset_id}
- "Partially update a preset?" -> PATCH /me/presets/{preset_id}
- "List all videos?" -> GET /me/presets/{preset_id}/videos
- "List all projects?" -> GET /me/projects
- "Create a project?" -> POST /me/projects
- "Delete a project?" -> DELETE /me/projects/{project_id}
- "Get project details?" -> GET /me/projects/{project_id}
- "Partially update a project?" -> PATCH /me/projects/{project_id}
- "List all videos?" -> GET /me/projects/{project_id}/videos
- "Delete a video?" -> DELETE /me/projects/{project_id}/videos/{video_id}
- "Update a video?" -> PUT /me/projects/{project_id}/videos/{video_id}
- "Search videos?" -> GET /me/videos
- "Create a video?" -> POST /me/videos
- "Get video details?" -> GET /me/videos/{video_id}
- "List all videos?" -> GET /me/watched/videos
- "Delete a video?" -> DELETE /me/watched/videos/{video_id}
- "Search watchlater?" -> GET /me/watchlater
- "Delete a watchlater?" -> DELETE /me/watchlater/{video_id}
- "Get watchlater details?" -> GET /me/watchlater/{video_id}
- "Update a watchlater?" -> PUT /me/watchlater/{video_id}
- "Create a access_token?" -> POST /oauth/access_token
- "Create a client?" -> POST /oauth/authorize/client
- "Create a vimeo_oauth1?" -> POST /oauth/authorize/vimeo_oauth1
- "List all verify?" -> GET /oauth/verify
- "List all genres?" -> GET /ondemand/genres
- "Get genre details?" -> GET /ondemand/genres/{genre_id}
- "Search pages?" -> GET /ondemand/genres/{genre_id}/pages
- "Get page details?" -> GET /ondemand/genres/{genre_id}/pages/{ondemand_id}
- "Delete a page?" -> DELETE /ondemand/pages/{ondemand_id}
- "Get page details?" -> GET /ondemand/pages/{ondemand_id}
- "Partially update a page?" -> PATCH /ondemand/pages/{ondemand_id}
- "List all backgrounds?" -> GET /ondemand/pages/{ondemand_id}/backgrounds
- "Create a background?" -> POST /ondemand/pages/{ondemand_id}/backgrounds
- "Delete a background?" -> DELETE /ondemand/pages/{ondemand_id}/backgrounds/{background_id}
- "Get background details?" -> GET /ondemand/pages/{ondemand_id}/backgrounds/{background_id}
- "Partially update a background?" -> PATCH /ondemand/pages/{ondemand_id}/backgrounds/{background_id}
- "List all genres?" -> GET /ondemand/pages/{ondemand_id}/genres
- "Delete a genre?" -> DELETE /ondemand/pages/{ondemand_id}/genres/{genre_id}
- "Get genre details?" -> GET /ondemand/pages/{ondemand_id}/genres/{genre_id}
- "Update a genre?" -> PUT /ondemand/pages/{ondemand_id}/genres/{genre_id}
- "List all likes?" -> GET /ondemand/pages/{ondemand_id}/likes
- "List all pictures?" -> GET /ondemand/pages/{ondemand_id}/pictures
- "Create a picture?" -> POST /ondemand/pages/{ondemand_id}/pictures
- "Get picture details?" -> GET /ondemand/pages/{ondemand_id}/pictures/{poster_id}
- "Partially update a picture?" -> PATCH /ondemand/pages/{ondemand_id}/pictures/{poster_id}
- "List all promotions?" -> GET /ondemand/pages/{ondemand_id}/promotions
- "Create a promotion?" -> POST /ondemand/pages/{ondemand_id}/promotions
- "Delete a promotion?" -> DELETE /ondemand/pages/{ondemand_id}/promotions/{promotion_id}
- "Get promotion details?" -> GET /ondemand/pages/{ondemand_id}/promotions/{promotion_id}
- "List all codes?" -> GET /ondemand/pages/{ondemand_id}/promotions/{promotion_id}/codes
- "List all regions?" -> GET /ondemand/pages/{ondemand_id}/regions
- "Delete a region?" -> DELETE /ondemand/pages/{ondemand_id}/regions/{country}
- "Get region details?" -> GET /ondemand/pages/{ondemand_id}/regions/{country}
- "Update a region?" -> PUT /ondemand/pages/{ondemand_id}/regions/{country}
- "List all seasons?" -> GET /ondemand/pages/{ondemand_id}/seasons
- "Get season details?" -> GET /ondemand/pages/{ondemand_id}/seasons/{season_id}
- "List all videos?" -> GET /ondemand/pages/{ondemand_id}/seasons/{season_id}/videos
- "List all videos?" -> GET /ondemand/pages/{ondemand_id}/videos
- "Delete a video?" -> DELETE /ondemand/pages/{ondemand_id}/videos/{video_id}
- "Get video details?" -> GET /ondemand/pages/{ondemand_id}/videos/{video_id}
- "Update a video?" -> PUT /ondemand/pages/{ondemand_id}/videos/{video_id}
- "List all regions?" -> GET /ondemand/regions
- "Get region details?" -> GET /ondemand/regions/{country}
- "Get tag details?" -> GET /tags/{word}
- "List all videos?" -> GET /tags/{word}/videos
- "List all tutorial?" -> GET /tutorial
- "Search users?" -> GET /users
- "Get user details?" -> GET /users/{user_id}
- "Partially update a user?" -> PATCH /users/{user_id}
- "Search albums?" -> GET /users/{user_id}/albums
- "Create a album?" -> POST /users/{user_id}/albums
- "Delete a album?" -> DELETE /users/{user_id}/albums/{album_id}
- "Get album details?" -> GET /users/{user_id}/albums/{album_id}
- "Partially update a album?" -> PATCH /users/{user_id}/albums/{album_id}
- "List all custom_thumbnails?" -> GET /users/{user_id}/albums/{album_id}/custom_thumbnails
- "Create a custom_thumbnail?" -> POST /users/{user_id}/albums/{album_id}/custom_thumbnails
- "Delete a custom_thumbnail?" -> DELETE /users/{user_id}/albums/{album_id}/custom_thumbnails/{thumbnail_id}
- "Get custom_thumbnail details?" -> GET /users/{user_id}/albums/{album_id}/custom_thumbnails/{thumbnail_id}
- "Partially update a custom_thumbnail?" -> PATCH /users/{user_id}/albums/{album_id}/custom_thumbnails/{thumbnail_id}
- "List all logos?" -> GET /users/{user_id}/albums/{album_id}/logos
- "Create a logo?" -> POST /users/{user_id}/albums/{album_id}/logos
- "Delete a logo?" -> DELETE /users/{user_id}/albums/{album_id}/logos/{logo_id}
- "Get logo details?" -> GET /users/{user_id}/albums/{album_id}/logos/{logo_id}
- "Partially update a logo?" -> PATCH /users/{user_id}/albums/{album_id}/logos/{logo_id}
- "Search videos?" -> GET /users/{user_id}/albums/{album_id}/videos
- "Delete a video?" -> DELETE /users/{user_id}/albums/{album_id}/videos/{video_id}
- "Get video details?" -> GET /users/{user_id}/albums/{album_id}/videos/{video_id}
- "Update a video?" -> PUT /users/{user_id}/albums/{album_id}/videos/{video_id}
- "Create a set_album_thumbnail?" -> POST /users/{user_id}/albums/{album_id}/videos/{video_id}/set_album_thumbnail
- "Search appearances?" -> GET /users/{user_id}/appearances
- "List all categories?" -> GET /users/{user_id}/categories
- "Delete a category?" -> DELETE /users/{user_id}/categories/{category}
- "Get category details?" -> GET /users/{user_id}/categories/{category}
- "Update a category?" -> PUT /users/{user_id}/categories/{category}
- "Search channels?" -> GET /users/{user_id}/channels
- "Delete a channel?" -> DELETE /users/{user_id}/channels/{channel_id}
- "Get channel details?" -> GET /users/{user_id}/channels/{channel_id}
- "Update a channel?" -> PUT /users/{user_id}/channels/{channel_id}
- "List all customlogos?" -> GET /users/{user_id}/customlogos
- "Create a customlogo?" -> POST /users/{user_id}/customlogos
- "Get customlogo details?" -> GET /users/{user_id}/customlogos/{logo_id}
- "List all feed?" -> GET /users/{user_id}/feed
- "Search followers?" -> GET /users/{user_id}/followers
- "Search following?" -> GET /users/{user_id}/following
- "Create a following?" -> POST /users/{user_id}/following
- "Delete a following?" -> DELETE /users/{user_id}/following/{follow_user_id}
- "Get following details?" -> GET /users/{user_id}/following/{follow_user_id}
- "Update a following?" -> PUT /users/{user_id}/following/{follow_user_id}
- "Search groups?" -> GET /users/{user_id}/groups
- "Delete a group?" -> DELETE /users/{user_id}/groups/{group_id}
- "Update a group?" -> PUT /users/{user_id}/groups/{group_id}
- "Get group details?" -> GET /users/{user_id}/groups/{group_id}
- "Search likes?" -> GET /users/{user_id}/likes
- "Delete a like?" -> DELETE /users/{user_id}/likes/{video_id}
- "Get like details?" -> GET /users/{user_id}/likes/{video_id}
- "Update a like?" -> PUT /users/{user_id}/likes/{video_id}
- "List all pages?" -> GET /users/{user_id}/ondemand/pages
- "Create a page?" -> POST /users/{user_id}/ondemand/pages
- "List all purchases?" -> GET /users/{user_id}/ondemand/purchases
- "List all pictures?" -> GET /users/{user_id}/pictures
- "Create a picture?" -> POST /users/{user_id}/pictures
- "Delete a picture?" -> DELETE /users/{user_id}/pictures/{portraitset_id}
- "Get picture details?" -> GET /users/{user_id}/pictures/{portraitset_id}
- "Partially update a picture?" -> PATCH /users/{user_id}/pictures/{portraitset_id}
- "Search portfolios?" -> GET /users/{user_id}/portfolios
- "Get portfolio details?" -> GET /users/{user_id}/portfolios/{portfolio_id}
- "List all videos?" -> GET /users/{user_id}/portfolios/{portfolio_id}/videos
- "Delete a video?" -> DELETE /users/{user_id}/portfolios/{portfolio_id}/videos/{video_id}
- "Get video details?" -> GET /users/{user_id}/portfolios/{portfolio_id}/videos/{video_id}
- "Update a video?" -> PUT /users/{user_id}/portfolios/{portfolio_id}/videos/{video_id}
- "List all presets?" -> GET /users/{user_id}/presets
- "Get preset details?" -> GET /users/{user_id}/presets/{preset_id}
- "Partially update a preset?" -> PATCH /users/{user_id}/presets/{preset_id}
- "List all videos?" -> GET /users/{user_id}/presets/{preset_id}/videos
- "List all projects?" -> GET /users/{user_id}/projects
- "Create a project?" -> POST /users/{user_id}/projects
- "Delete a project?" -> DELETE /users/{user_id}/projects/{project_id}
- "Get project details?" -> GET /users/{user_id}/projects/{project_id}
- "Partially update a project?" -> PATCH /users/{user_id}/projects/{project_id}
- "List all videos?" -> GET /users/{user_id}/projects/{project_id}/videos
- "Delete a video?" -> DELETE /users/{user_id}/projects/{project_id}/videos/{video_id}
- "Update a video?" -> PUT /users/{user_id}/projects/{project_id}/videos/{video_id}
- "Delete a upload?" -> DELETE /users/{user_id}/uploads/{upload_id}
- "Get upload details?" -> GET /users/{user_id}/uploads/{upload_id}
- "Search videos?" -> GET /users/{user_id}/videos
- "Create a video?" -> POST /users/{user_id}/videos
- "Get video details?" -> GET /users/{user_id}/videos/{video_id}
- "Search watchlater?" -> GET /users/{user_id}/watchlater
- "Delete a watchlater?" -> DELETE /users/{user_id}/watchlater/{video_id}
- "Get watchlater details?" -> GET /users/{user_id}/watchlater/{video_id}
- "Update a watchlater?" -> PUT /users/{user_id}/watchlater/{video_id}
- "Search videos?" -> GET /videos
- "Delete a video?" -> DELETE /videos/{video_id}
- "Get video details?" -> GET /videos/{video_id}
- "Partially update a video?" -> PATCH /videos/{video_id}
- "List all available_albums?" -> GET /videos/{video_id}/available_albums
- "List all available_channels?" -> GET /videos/{video_id}/available_channels
- "List all categories?" -> GET /videos/{video_id}/categories
- "List all comments?" -> GET /videos/{video_id}/comments
- "Create a comment?" -> POST /videos/{video_id}/comments
- "Delete a comment?" -> DELETE /videos/{video_id}/comments/{comment_id}
- "Get comment details?" -> GET /videos/{video_id}/comments/{comment_id}
- "Partially update a comment?" -> PATCH /videos/{video_id}/comments/{comment_id}
- "List all replies?" -> GET /videos/{video_id}/comments/{comment_id}/replies
- "Create a reply?" -> POST /videos/{video_id}/comments/{comment_id}/replies
- "Search credits?" -> GET /videos/{video_id}/credits
- "Create a credit?" -> POST /videos/{video_id}/credits
- "Delete a credit?" -> DELETE /videos/{video_id}/credits/{credit_id}
- "Get credit details?" -> GET /videos/{video_id}/credits/{credit_id}
- "Partially update a credit?" -> PATCH /videos/{video_id}/credits/{credit_id}
- "List all likes?" -> GET /videos/{video_id}/likes
- "List all pictures?" -> GET /videos/{video_id}/pictures
- "Create a picture?" -> POST /videos/{video_id}/pictures
- "Delete a picture?" -> DELETE /videos/{video_id}/pictures/{picture_id}
- "Get picture details?" -> GET /videos/{video_id}/pictures/{picture_id}
- "Partially update a picture?" -> PATCH /videos/{video_id}/pictures/{picture_id}
- "Delete a preset?" -> DELETE /videos/{video_id}/presets/{preset_id}
- "Get preset details?" -> GET /videos/{video_id}/presets/{preset_id}
- "Update a preset?" -> PUT /videos/{video_id}/presets/{preset_id}
- "List all domains?" -> GET /videos/{video_id}/privacy/domains
- "Delete a domain?" -> DELETE /videos/{video_id}/privacy/domains/{domain}
- "Update a domain?" -> PUT /videos/{video_id}/privacy/domains/{domain}
- "List all users?" -> GET /videos/{video_id}/privacy/users
- "Delete a user?" -> DELETE /videos/{video_id}/privacy/users/{user_id}
- "Update a user?" -> PUT /videos/{video_id}/privacy/users/{user_id}
- "List all tags?" -> GET /videos/{video_id}/tags
- "Delete a tag?" -> DELETE /videos/{video_id}/tags/{word}
- "Get tag details?" -> GET /videos/{video_id}/tags/{word}
- "Update a tag?" -> PUT /videos/{video_id}/tags/{word}
- "List all texttracks?" -> GET /videos/{video_id}/texttracks
- "Create a texttrack?" -> POST /videos/{video_id}/texttracks
- "Delete a texttrack?" -> DELETE /videos/{video_id}/texttracks/{texttrack_id}
- "Get texttrack details?" -> GET /videos/{video_id}/texttracks/{texttrack_id}
- "Partially update a texttrack?" -> PATCH /videos/{video_id}/texttracks/{texttrack_id}
- "Create a timelinethumbnail?" -> POST /videos/{video_id}/timelinethumbnails
- "Get timelinethumbnail details?" -> GET /videos/{video_id}/timelinethumbnails/{thumbnail_id}
- "Create a version?" -> POST /videos/{video_id}/versions
- "List all videos?" -> GET /videos/{video_id}/videos
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
