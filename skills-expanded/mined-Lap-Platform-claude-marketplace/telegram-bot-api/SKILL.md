---
name: telegram-bot-api
description: "Telegram Bot API skill. Use when working with Telegram Bot for getUpdates, setWebhook, deleteWebhook. Covers 74 endpoints."
version: 1.0.0
generator: lapsh
---

# Telegram Bot API
API version: 5.0.0

## Auth
No authentication required.

## Base URL
https://api.telegram.org/bot{token}

## Setup
1. No auth setup needed
3. POST /getUpdates -- create first getUpdates

## Endpoints

74 endpoints across 74 groups. See references/api-spec.lap for full details.

### getUpdates
| Method | Path | Description |
|--------|------|-------------|
| POST | /getUpdates | Use this method to receive incoming updates using long polling ([wiki](https://en.wikipedia.org/wiki/Push_technology#Long_polling)). An Array of [Update](https://core.telegram.org/bots/api/#update) objects is returned. |

### setWebhook
| Method | Path | Description |
|--------|------|-------------|
| POST | /setWebhook | Use this method to specify a url and receive incoming updates via an outgoing webhook. Whenever there is an update for the bot, we will send an HTTPS POST request to the specified url, containing a JSON-serialized [Update](https://core.telegram.org/bots/api/#update). In case of an unsuccessful request, we will give up after a reasonable amount of attempts. Returns *True* on success. |

### deleteWebhook
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteWebhook | Use this method to remove webhook integration if you decide to switch back to [getUpdates](https://core.telegram.org/bots/api/#getupdates). Returns *True* on success. |

### getWebhookInfo
| Method | Path | Description |
|--------|------|-------------|
| POST | /getWebhookInfo | Use this method to get current webhook status. Requires no parameters. On success, returns a [WebhookInfo](https://core.telegram.org/bots/api/#webhookinfo) object. If the bot is using [getUpdates](https://core.telegram.org/bots/api/#getupdates), will return an object with the *url* field empty. |

### getMe
| Method | Path | Description |
|--------|------|-------------|
| POST | /getMe | A simple method for testing your bot's auth token. Requires no parameters. Returns basic information about the bot in form of a [User](https://core.telegram.org/bots/api/#user) object. |

### logOut
| Method | Path | Description |
|--------|------|-------------|
| POST | /logOut | Use this method to log out from the cloud Bot API server before launching the bot locally. You **must** log out the bot before running it locally, otherwise there is no guarantee that the bot will receive updates. After a successful call, you can immediately log in on a local server, but will not be able to log in back to the cloud Bot API server for 10 minutes. Returns *True* on success. Requires no parameters. |

### close
| Method | Path | Description |
|--------|------|-------------|
| POST | /close | Use this method to close the bot instance before moving it from one local server to another. You need to delete the webhook before calling this method to ensure that the bot isn't launched again after server restart. The method will return error 429 in the first 10 minutes after the bot is launched. Returns *True* on success. Requires no parameters. |

### sendMessage
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendMessage | Use this method to send text messages. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### forwardMessage
| Method | Path | Description |
|--------|------|-------------|
| POST | /forwardMessage | Use this method to forward messages of any kind. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### copyMessage
| Method | Path | Description |
|--------|------|-------------|
| POST | /copyMessage | Use this method to copy messages of any kind. The method is analogous to the method [forwardMessages](https://core.telegram.org/bots/api/#forwardmessages), but the copied message doesn't have a link to the original message. Returns the [MessageId](https://core.telegram.org/bots/api/#messageid) of the sent message on success. |

### sendPhoto
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendPhoto | Use this method to send photos. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### sendAudio
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendAudio | Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .MP3 or .M4A format. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. Bots can currently send audio files of up to 50 MB in size, this limit may be changed in the future. |

### sendDocument
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendDocument | Use this method to send general files. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future. |

### sendVideo
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendVideo | Use this method to send video files, Telegram clients support mp4 videos (other formats may be sent as [Document](https://core.telegram.org/bots/api/#document)). On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. Bots can currently send video files of up to 50 MB in size, this limit may be changed in the future. |

### sendAnimation
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendAnimation | Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future. |

### sendVoice
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendVoice | Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message. For this to work, your audio must be in an .OGG file encoded with OPUS (other formats may be sent as [Audio](https://core.telegram.org/bots/api/#audio) or [Document](https://core.telegram.org/bots/api/#document)). On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. Bots can currently send voice messages of up to 50 MB in size, this limit may be changed in the future. |

### sendVideoNote
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendVideoNote | As of [v.4.0](https://telegram.org/blog/video-messages-and-telescope), Telegram clients support rounded square mp4 videos of up to 1 minute long. Use this method to send video messages. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### sendMediaGroup
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendMediaGroup | Use this method to send a group of photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an array of [Messages](https://core.telegram.org/bots/api/#message) that were sent is returned. |

### sendLocation
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendLocation | Use this method to send point on the map. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### editMessageLiveLocation
| Method | Path | Description |
|--------|------|-------------|
| POST | /editMessageLiveLocation | Use this method to edit live location messages. A location can be edited until its *live\_period* expires or editing is explicitly disabled by a call to [stopMessageLiveLocation](https://core.telegram.org/bots/api/#stopmessagelivelocation). On success, if the edited message is not an inline message, the edited [Message](https://core.telegram.org/bots/api/#message) is returned, otherwise *True* is returned. |

### stopMessageLiveLocation
| Method | Path | Description |
|--------|------|-------------|
| POST | /stopMessageLiveLocation | Use this method to stop updating a live location message before *live\_period* expires. On success, if the message was sent by the bot, the sent [Message](https://core.telegram.org/bots/api/#message) is returned, otherwise *True* is returned. |

### sendVenue
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendVenue | Use this method to send information about a venue. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### sendContact
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendContact | Use this method to send phone contacts. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### sendPoll
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendPoll | Use this method to send a native poll. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### sendDice
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendDice | Use this method to send an animated emoji that will display a random value. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### sendChatAction
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendChatAction | Use this method when you need to tell the user that something is happening on the bot's side. The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status). Returns *True* on success. |

### getUserProfilePhotos
| Method | Path | Description |
|--------|------|-------------|
| POST | /getUserProfilePhotos | Use this method to get a list of profile pictures for a user. Returns a [UserProfilePhotos](https://core.telegram.org/bots/api/#userprofilephotos) object. |

### getFile
| Method | Path | Description |
|--------|------|-------------|
| POST | /getFile | Use this method to get basic info about a file and prepare it for downloading. For the moment, bots can download files of up to 20MB in size. On success, a [File](https://core.telegram.org/bots/api/#file) object is returned. The file can then be downloaded via the link `https://api.telegram.org/file/bot<token>/<file_path>`, where `<file_path>` is taken from the response. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling [getFile](https://core.telegram.org/bots/api/#getfile) again. |

### kickChatMember
| Method | Path | Description |
|--------|------|-------------|
| POST | /kickChatMember | Use this method to kick a user from a group, a supergroup or a channel. In the case of supergroups and channels, the user will not be able to return to the group on their own using invite links, etc., unless [unbanned](https://core.telegram.org/bots/api/#unbanchatmember) first. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns *True* on success. |

### unbanChatMember
| Method | Path | Description |
|--------|------|-------------|
| POST | /unbanChatMember | Use this method to unban a previously kicked user in a supergroup or channel. The user will **not** return to the group or channel automatically, but will be able to join via link, etc. The bot must be an administrator for this to work. By default, this method guarantees that after the call the user is not a member of the chat, but will be able to join it. So if the user is a member of the chat they will also be **removed** from the chat. If you don't want this, use the parameter *only\_if\_banned*. Returns *True* on success. |

### restrictChatMember
| Method | Path | Description |
|--------|------|-------------|
| POST | /restrictChatMember | Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate admin rights. Pass *True* for all permissions to lift restrictions from a user. Returns *True* on success. |

### promoteChatMember
| Method | Path | Description |
|--------|------|-------------|
| POST | /promoteChatMember | Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Pass *False* for all boolean parameters to demote a user. Returns *True* on success. |

### setChatAdministratorCustomTitle
| Method | Path | Description |
|--------|------|-------------|
| POST | /setChatAdministratorCustomTitle | Use this method to set a custom title for an administrator in a supergroup promoted by the bot. Returns *True* on success. |

### setChatPermissions
| Method | Path | Description |
|--------|------|-------------|
| POST | /setChatPermissions | Use this method to set default chat permissions for all members. The bot must be an administrator in the group or a supergroup for this to work and must have the *can\_restrict\_members* admin rights. Returns *True* on success. |

### exportChatInviteLink
| Method | Path | Description |
|--------|------|-------------|
| POST | /exportChatInviteLink | Use this method to generate a new invite link for a chat; any previously generated link is revoked. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns the new invite link as *String* on success. |

### setChatPhoto
| Method | Path | Description |
|--------|------|-------------|
| POST | /setChatPhoto | Use this method to set a new profile photo for the chat. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns *True* on success. |

### deleteChatPhoto
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteChatPhoto | Use this method to delete a chat photo. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns *True* on success. |

### setChatTitle
| Method | Path | Description |
|--------|------|-------------|
| POST | /setChatTitle | Use this method to change the title of a chat. Titles can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns *True* on success. |

### setChatDescription
| Method | Path | Description |
|--------|------|-------------|
| POST | /setChatDescription | Use this method to change the description of a group, a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Returns *True* on success. |

### pinChatMessage
| Method | Path | Description |
|--------|------|-------------|
| POST | /pinChatMessage | Use this method to add a message to the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can\_pin\_messages' admin right in a supergroup or 'can\_edit\_messages' admin right in a channel. Returns *True* on success. |

### unpinChatMessage
| Method | Path | Description |
|--------|------|-------------|
| POST | /unpinChatMessage | Use this method to remove a message from the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can\_pin\_messages' admin right in a supergroup or 'can\_edit\_messages' admin right in a channel. Returns *True* on success. |

### unpinAllChatMessages
| Method | Path | Description |
|--------|------|-------------|
| POST | /unpinAllChatMessages | Use this method to clear the list of pinned messages in a chat. If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have the 'can\_pin\_messages' admin right in a supergroup or 'can\_edit\_messages' admin right in a channel. Returns *True* on success. |

### leaveChat
| Method | Path | Description |
|--------|------|-------------|
| POST | /leaveChat | Use this method for your bot to leave a group, supergroup or channel. Returns *True* on success. |

### getChat
| Method | Path | Description |
|--------|------|-------------|
| POST | /getChat | Use this method to get up to date information about the chat (current name of the user for one-on-one conversations, current username of a user, group or channel, etc.). Returns a [Chat](https://core.telegram.org/bots/api/#chat) object on success. |

### getChatAdministrators
| Method | Path | Description |
|--------|------|-------------|
| POST | /getChatAdministrators | Use this method to get a list of administrators in a chat. On success, returns an Array of [ChatMember](https://core.telegram.org/bots/api/#chatmember) objects that contains information about all chat administrators except other bots. If the chat is a group or a supergroup and no administrators were appointed, only the creator will be returned. |

### getChatMembersCount
| Method | Path | Description |
|--------|------|-------------|
| POST | /getChatMembersCount | Use this method to get the number of members in a chat. Returns *Int* on success. |

### getChatMember
| Method | Path | Description |
|--------|------|-------------|
| POST | /getChatMember | Use this method to get information about a member of a chat. Returns a [ChatMember](https://core.telegram.org/bots/api/#chatmember) object on success. |

### setChatStickerSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /setChatStickerSet | Use this method to set a new group sticker set for a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Use the field *can\_set\_sticker\_set* optionally returned in [getChat](https://core.telegram.org/bots/api/#getchat) requests to check if the bot can use this method. Returns *True* on success. |

### deleteChatStickerSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteChatStickerSet | Use this method to delete a group sticker set from a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate admin rights. Use the field *can\_set\_sticker\_set* optionally returned in [getChat](https://core.telegram.org/bots/api/#getchat) requests to check if the bot can use this method. Returns *True* on success. |

### answerCallbackQuery
| Method | Path | Description |
|--------|------|-------------|
| POST | /answerCallbackQuery | Use this method to send answers to callback queries sent from [inline keyboards](/bots#inline-keyboards-and-on-the-fly-updating). The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. On success, *True* is returned. |

### setMyCommands
| Method | Path | Description |
|--------|------|-------------|
| POST | /setMyCommands | Use this method to change the list of the bot's commands. Returns *True* on success. |

### getMyCommands
| Method | Path | Description |
|--------|------|-------------|
| POST | /getMyCommands | Use this method to get the current list of the bot's commands. Requires no parameters. Returns Array of [BotCommand](https://core.telegram.org/bots/api/#botcommand) on success. |

### editMessageText
| Method | Path | Description |
|--------|------|-------------|
| POST | /editMessageText | Use this method to edit text and [game](https://core.telegram.org/bots/api/#games) messages. On success, if the edited message is not an inline message, the edited [Message](https://core.telegram.org/bots/api/#message) is returned, otherwise *True* is returned. |

### editMessageCaption
| Method | Path | Description |
|--------|------|-------------|
| POST | /editMessageCaption | Use this method to edit captions of messages. On success, if the edited message is not an inline message, the edited [Message](https://core.telegram.org/bots/api/#message) is returned, otherwise *True* is returned. |

### editMessageMedia
| Method | Path | Description |
|--------|------|-------------|
| POST | /editMessageMedia | Use this method to edit animation, audio, document, photo, or video messages. If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo or a video otherwise. When an inline message is edited, a new file can't be uploaded. Use a previously uploaded file via its file\_id or specify a URL. On success, if the edited message was sent by the bot, the edited [Message](https://core.telegram.org/bots/api/#message) is returned, otherwise *True* is returned. |

### editMessageReplyMarkup
| Method | Path | Description |
|--------|------|-------------|
| POST | /editMessageReplyMarkup | Use this method to edit only the reply markup of messages. On success, if the edited message is not an inline message, the edited [Message](https://core.telegram.org/bots/api/#message) is returned, otherwise *True* is returned. |

### stopPoll
| Method | Path | Description |
|--------|------|-------------|
| POST | /stopPoll | Use this method to stop a poll which was sent by the bot. On success, the stopped [Poll](https://core.telegram.org/bots/api/#poll) with the final results is returned. |

### deleteMessage
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteMessage | Use this method to delete a message, including service messages, with the following limitations: |

### sendSticker
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendSticker | Use this method to send static .WEBP or [animated](https://telegram.org/blog/animated-stickers) .TGS stickers. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### getStickerSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /getStickerSet | Use this method to get a sticker set. On success, a [StickerSet](https://core.telegram.org/bots/api/#stickerset) object is returned. |

### uploadStickerFile
| Method | Path | Description |
|--------|------|-------------|
| POST | /uploadStickerFile | Use this method to upload a .PNG file with a sticker for later use in *createNewStickerSet* and *addStickerToSet* methods (can be used multiple times). Returns the uploaded [File](https://core.telegram.org/bots/api/#file) on success. |

### createNewStickerSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /createNewStickerSet | Use this method to create a new sticker set owned by a user. The bot will be able to edit the sticker set thus created. You **must** use exactly one of the fields *png\_sticker* or *tgs\_sticker*. Returns *True* on success. |

### addStickerToSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /addStickerToSet | Use this method to add a new sticker to a set created by the bot. You **must** use exactly one of the fields *png\_sticker* or *tgs\_sticker*. Animated stickers can be added to animated sticker sets and only to them. Animated sticker sets can have up to 50 stickers. Static sticker sets can have up to 120 stickers. Returns *True* on success. |

### setStickerPositionInSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /setStickerPositionInSet | Use this method to move a sticker in a set created by the bot to a specific position. Returns *True* on success. |

### deleteStickerFromSet
| Method | Path | Description |
|--------|------|-------------|
| POST | /deleteStickerFromSet | Use this method to delete a sticker from a set created by the bot. Returns *True* on success. |

### setStickerSetThumb
| Method | Path | Description |
|--------|------|-------------|
| POST | /setStickerSetThumb | Use this method to set the thumbnail of a sticker set. Animated thumbnails can be set for animated sticker sets only. Returns *True* on success. |

### answerInlineQuery
| Method | Path | Description |
|--------|------|-------------|
| POST | /answerInlineQuery | Use this method to send answers to an inline query. On success, *True* is returned. |

### sendInvoice
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendInvoice | Use this method to send invoices. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### answerShippingQuery
| Method | Path | Description |
|--------|------|-------------|
| POST | /answerShippingQuery | If you sent an invoice requesting a shipping address and the parameter *is\_flexible* was specified, the Bot API will send an [Update](https://core.telegram.org/bots/api/#update) with a *shipping\_query* field to the bot. Use this method to reply to shipping queries. On success, True is returned. |

### answerPreCheckoutQuery
| Method | Path | Description |
|--------|------|-------------|
| POST | /answerPreCheckoutQuery | Once the user has confirmed their payment and shipping details, the Bot API sends the final confirmation in the form of an [Update](https://core.telegram.org/bots/api/#update) with the field *pre\_checkout\_query*. Use this method to respond to such pre-checkout queries. On success, True is returned. **Note:** The Bot API must receive an answer within 10 seconds after the pre-checkout query was sent. |

### setPassportDataErrors
| Method | Path | Description |
|--------|------|-------------|
| POST | /setPassportDataErrors | Informs a user that some of the Telegram Passport elements they provided contains errors. The user will not be able to re-submit their Passport to you until the errors are fixed (the contents of the field for which you returned the error must change). Returns *True* on success. |

### sendGame
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendGame | Use this method to send a game. On success, the sent [Message](https://core.telegram.org/bots/api/#message) is returned. |

### setGameScore
| Method | Path | Description |
|--------|------|-------------|
| POST | /setGameScore | Use this method to set the score of the specified user in a game. On success, if the message was sent by the bot, returns the edited [Message](https://core.telegram.org/bots/api/#message), otherwise returns *True*. Returns an error, if the new score is not greater than the user's current score in the chat and *force* is *False*. |

### getGameHighScores
| Method | Path | Description |
|--------|------|-------------|
| POST | /getGameHighScores | Use this method to get data for high score tables. Will return the score of the specified user and several of their neighbors in a game. On success, returns an *Array* of [GameHighScore](https://core.telegram.org/bots/api/#gamehighscore) objects. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a getUpdate?" -> POST /getUpdates
- "Create a setWebhook?" -> POST /setWebhook
- "Create a deleteWebhook?" -> POST /deleteWebhook
- "Create a getWebhookInfo?" -> POST /getWebhookInfo
- "Create a getMe?" -> POST /getMe
- "Create a logOut?" -> POST /logOut
- "Create a close?" -> POST /close
- "Create a sendMessage?" -> POST /sendMessage
- "Create a forwardMessage?" -> POST /forwardMessage
- "Create a copyMessage?" -> POST /copyMessage
- "Create a sendPhoto?" -> POST /sendPhoto
- "Create a sendAudio?" -> POST /sendAudio
- "Create a sendDocument?" -> POST /sendDocument
- "Create a sendVideo?" -> POST /sendVideo
- "Create a sendAnimation?" -> POST /sendAnimation
- "Create a sendVoice?" -> POST /sendVoice
- "Create a sendVideoNote?" -> POST /sendVideoNote
- "Create a sendMediaGroup?" -> POST /sendMediaGroup
- "Create a sendLocation?" -> POST /sendLocation
- "Create a editMessageLiveLocation?" -> POST /editMessageLiveLocation
- "Create a stopMessageLiveLocation?" -> POST /stopMessageLiveLocation
- "Create a sendVenue?" -> POST /sendVenue
- "Create a sendContact?" -> POST /sendContact
- "Create a sendPoll?" -> POST /sendPoll
- "Create a sendDice?" -> POST /sendDice
- "Create a sendChatAction?" -> POST /sendChatAction
- "Create a getUserProfilePhoto?" -> POST /getUserProfilePhotos
- "Create a getFile?" -> POST /getFile
- "Create a kickChatMember?" -> POST /kickChatMember
- "Create a unbanChatMember?" -> POST /unbanChatMember
- "Create a restrictChatMember?" -> POST /restrictChatMember
- "Create a promoteChatMember?" -> POST /promoteChatMember
- "Create a setChatAdministratorCustomTitle?" -> POST /setChatAdministratorCustomTitle
- "Create a setChatPermission?" -> POST /setChatPermissions
- "Create a exportChatInviteLink?" -> POST /exportChatInviteLink
- "Create a setChatPhoto?" -> POST /setChatPhoto
- "Create a deleteChatPhoto?" -> POST /deleteChatPhoto
- "Create a setChatTitle?" -> POST /setChatTitle
- "Create a setChatDescription?" -> POST /setChatDescription
- "Create a pinChatMessage?" -> POST /pinChatMessage
- "Create a unpinChatMessage?" -> POST /unpinChatMessage
- "Create a unpinAllChatMessage?" -> POST /unpinAllChatMessages
- "Create a leaveChat?" -> POST /leaveChat
- "Create a getChat?" -> POST /getChat
- "Create a getChatAdministrator?" -> POST /getChatAdministrators
- "Create a getChatMembersCount?" -> POST /getChatMembersCount
- "Create a getChatMember?" -> POST /getChatMember
- "Create a setChatStickerSet?" -> POST /setChatStickerSet
- "Create a deleteChatStickerSet?" -> POST /deleteChatStickerSet
- "Create a answerCallbackQuery?" -> POST /answerCallbackQuery
- "Create a setMyCommand?" -> POST /setMyCommands
- "Create a getMyCommand?" -> POST /getMyCommands
- "Create a editMessageText?" -> POST /editMessageText
- "Create a editMessageCaption?" -> POST /editMessageCaption
- "Create a editMessageMedia?" -> POST /editMessageMedia
- "Create a editMessageReplyMarkup?" -> POST /editMessageReplyMarkup
- "Create a stopPoll?" -> POST /stopPoll
- "Create a deleteMessage?" -> POST /deleteMessage
- "Create a sendSticker?" -> POST /sendSticker
- "Create a getStickerSet?" -> POST /getStickerSet
- "Create a uploadStickerFile?" -> POST /uploadStickerFile
- "Create a createNewStickerSet?" -> POST /createNewStickerSet
- "Create a addStickerToSet?" -> POST /addStickerToSet
- "Create a setStickerPositionInSet?" -> POST /setStickerPositionInSet
- "Create a deleteStickerFromSet?" -> POST /deleteStickerFromSet
- "Create a setStickerSetThumb?" -> POST /setStickerSetThumb
- "Create a answerInlineQuery?" -> POST /answerInlineQuery
- "Create a sendInvoice?" -> POST /sendInvoice
- "Create a answerShippingQuery?" -> POST /answerShippingQuery
- "Create a answerPreCheckoutQuery?" -> POST /answerPreCheckoutQuery
- "Create a setPassportDataError?" -> POST /setPassportDataErrors
- "Create a sendGame?" -> POST /sendGame
- "Create a setGameScore?" -> POST /setGameScore
- "Create a getGameHighScore?" -> POST /getGameHighScores

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
