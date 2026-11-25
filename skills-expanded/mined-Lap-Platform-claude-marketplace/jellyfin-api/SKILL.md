---
name: jellyfin-api
description: "Jellyfin API skill. Use when working with Jellyfin for System, Auth, Artists. Covers 408 endpoints."
version: 1.0.0
generator: lapsh
---

# Jellyfin API
API version: v1

## Auth
ApiKey X-Emby-Authorization in header

## Base URL
http://localhost

## Setup
1. Set your API key in the appropriate header
2. GET /System/ActivityLog/Entries -- verify access
3. POST /Auth/Keys -- create first Keys

## Endpoints

408 endpoints across 46 groups. See references/api-spec.lap for full details.

### System
| Method | Path | Description |
|--------|------|-------------|
| GET | /System/ActivityLog/Entries | Gets activity log entries. |
| GET | /System/Configuration | Gets application configuration. |
| POST | /System/Configuration | Updates application configuration. |
| GET | /System/Configuration/{key} | Gets a named configuration. |
| POST | /System/Configuration/{key} | Updates named configuration. |
| GET | /System/Configuration/MetadataOptions/Default | Gets a default MetadataOptions object. |
| POST | /System/MediaEncoder/Path | Updates the path to the media encoder. |
| GET | /System/Endpoint | Gets information about the request endpoint. |
| GET | /System/Info | Gets information about the server. |
| GET | /System/Info/Public | Gets public information about the server. |
| GET | /System/Logs | Gets a list of available server log files. |
| GET | /System/Logs/Log | Gets a log file. |
| GET | /System/Ping | Pings the system. |
| POST | /System/Ping | Pings the system. |
| POST | /System/Restart | Restarts the application. |
| POST | /System/Shutdown | Shuts down the application. |
| GET | /System/WakeOnLanInfo | Gets wake on lan information. |

### Auth
| Method | Path | Description |
|--------|------|-------------|
| GET | /Auth/Keys | Get all keys. |
| POST | /Auth/Keys | Create a new api key. |
| DELETE | /Auth/Keys/{key} | Remove an api key. |
| GET | /Auth/PasswordResetProviders | Get all password reset providers. |
| GET | /Auth/Providers | Get all auth providers. |

### Artists
| Method | Path | Description |
|--------|------|-------------|
| GET | /Artists | Gets all artists from a given item, folder, or the entire library. |
| GET | /Artists/{name} | Gets an artist by name. |
| GET | /Artists/AlbumArtists | Gets all album artists from a given item, folder, or the entire library. |
| GET | /Artists/{name}/Images/{imageType}/{imageIndex} | Get artist image by name. |
| HEAD | /Artists/{name}/Images/{imageType}/{imageIndex} | Get artist image by name. |
| GET | /Artists/{id}/InstantMix | Creates an instant playlist based on a given song. |
| GET | /Artists/{itemId}/Similar | Gets similar items. |

### Audio
| Method | Path | Description |
|--------|------|-------------|
| GET | /Audio/{itemId}/stream | Gets an audio stream. |
| HEAD | /Audio/{itemId}/stream | Gets an audio stream. |
| GET | /Audio/{itemId}/stream.{container} | Gets an audio stream. |
| HEAD | /Audio/{itemId}/stream.{container} | Gets an audio stream. |
| GET | /Audio/{itemId}/hls1/{playlistId}/{segmentId}.{container} | Gets a video stream using HTTP live streaming. |
| GET | /Audio/{itemId}/main.m3u8 | Gets an audio stream using HTTP live streaming. |
| GET | /Audio/{itemId}/master.m3u8 | Gets an audio hls playlist stream. |
| HEAD | /Audio/{itemId}/master.m3u8 | Gets an audio hls playlist stream. |
| GET | /Audio/{itemId}/hls/{segmentId}/stream.aac | Gets the specified audio segment for an audio item. |
| GET | /Audio/{itemId}/hls/{segmentId}/stream.mp3 | Gets the specified audio segment for an audio item. |
| GET | /Audio/{itemId}/universal | Gets an audio stream. |
| HEAD | /Audio/{itemId}/universal | Gets an audio stream. |

### Branding
| Method | Path | Description |
|--------|------|-------------|
| GET | /Branding/Configuration | Gets branding configuration. |
| GET | /Branding/Css | Gets branding css. |
| GET | /Branding/Css.css | Gets branding css. |

### Channels
| Method | Path | Description |
|--------|------|-------------|
| GET | /Channels | Gets available channels. |
| GET | /Channels/{channelId}/Features | Get channel features. |
| GET | /Channels/{channelId}/Items | Get channel items. |
| GET | /Channels/Features | Get all channel features. |
| GET | /Channels/Items/Latest | Gets latest channel items. |

### Collections
| Method | Path | Description |
|--------|------|-------------|
| POST | /Collections | Creates a new collection. |
| POST | /Collections/{collectionId}/Items | Adds items to a collection. |
| DELETE | /Collections/{collectionId}/Items | Removes items from a collection. |

### web
| Method | Path | Description |
|--------|------|-------------|
| GET | /web/ConfigurationPage | Gets a dashboard configuration page. |
| GET | /web/ConfigurationPages | Gets the configuration pages. |

### Devices
| Method | Path | Description |
|--------|------|-------------|
| GET | /Devices | Get Devices. |
| DELETE | /Devices | Deletes a device. |
| GET | /Devices/Info | Get info for a device. |
| GET | /Devices/Options | Get options for a device. |
| POST | /Devices/Options | Update device options. |

### DisplayPreferences
| Method | Path | Description |
|--------|------|-------------|
| GET | /DisplayPreferences/{displayPreferencesId} | Get Display Preferences. |
| POST | /DisplayPreferences/{displayPreferencesId} | Update Display Preferences. |

### Dlna
| Method | Path | Description |
|--------|------|-------------|
| GET | /Dlna/ProfileInfos | Get profile infos. |
| POST | /Dlna/Profiles | Creates a profile. |
| GET | /Dlna/Profiles/{profileId} | Gets a single profile. |
| DELETE | /Dlna/Profiles/{profileId} | Deletes a profile. |
| POST | /Dlna/Profiles/{profileId} | Updates a profile. |
| GET | /Dlna/Profiles/Default | Gets the default profile. |
| GET | /Dlna/{serverId}/ConnectionManager | Gets Dlna media receiver registrar xml. |
| GET | /Dlna/{serverId}/ConnectionManager/ConnectionManager | Gets Dlna media receiver registrar xml. |
| GET | /Dlna/{serverId}/ConnectionManager/ConnectionManager.xml | Gets Dlna media receiver registrar xml. |
| POST | /Dlna/{serverId}/ConnectionManager/Control | Process a connection manager control request. |
| GET | /Dlna/{serverId}/ContentDirectory | Gets Dlna content directory xml. |
| GET | /Dlna/{serverId}/ContentDirectory/ContentDirectory | Gets Dlna content directory xml. |
| GET | /Dlna/{serverId}/ContentDirectory/ContentDirectory.xml | Gets Dlna content directory xml. |
| POST | /Dlna/{serverId}/ContentDirectory/Control | Process a content directory control request. |
| GET | /Dlna/{serverId}/description | Get Description Xml. |
| GET | /Dlna/{serverId}/description.xml | Get Description Xml. |
| GET | /Dlna/{serverId}/icons/{fileName} | Gets a server icon. |
| GET | /Dlna/{serverId}/MediaReceiverRegistrar | Gets Dlna media receiver registrar xml. |
| POST | /Dlna/{serverId}/MediaReceiverRegistrar/Control | Process a media receiver registrar control request. |
| GET | /Dlna/{serverId}/MediaReceiverRegistrar/MediaReceiverRegistrar | Gets Dlna media receiver registrar xml. |
| GET | /Dlna/{serverId}/MediaReceiverRegistrar/MediaReceiverRegistrar.xml | Gets Dlna media receiver registrar xml. |
| GET | /Dlna/icons/{fileName} | Gets a server icon. |

### Videos
| Method | Path | Description |
|--------|------|-------------|
| GET | /Videos/{itemId}/hls1/{playlistId}/{segmentId}.{container} | Gets a video stream using HTTP live streaming. |
| GET | /Videos/{itemId}/main.m3u8 | Gets a video stream using HTTP live streaming. |
| GET | /Videos/{itemId}/master.m3u8 | Gets a video hls playlist stream. |
| HEAD | /Videos/{itemId}/master.m3u8 | Gets a video hls playlist stream. |
| GET | /Videos/{itemId}/hls/{playlistId}/{segmentId}.{segmentContainer} | Gets a hls video segment. |
| GET | /Videos/{itemId}/hls/{playlistId}/stream.m3u8 | Gets a hls video playlist. |
| DELETE | /Videos/ActiveEncodings | Stops an active encoding. |
| GET | /Videos/{itemId}/{mediaSourceId}/Subtitles/{index}/{startPositionTicks}/Stream.{format} | Gets subtitles in a specified format. |
| GET | /Videos/{itemId}/{mediaSourceId}/Subtitles/{index}/Stream.{format} | Gets subtitles in a specified format. |
| GET | /Videos/{itemId}/{mediaSourceId}/Subtitles/{index}/subtitles.m3u8 | Gets an HLS subtitle playlist. |
| POST | /Videos/{itemId}/Subtitles | Upload an external subtitle file. |
| DELETE | /Videos/{itemId}/Subtitles/{index} | Deletes an external subtitle file. |
| GET | /Videos/{videoId}/{mediaSourceId}/Attachments/{index} | Get video attachment. |
| GET | /Videos/{itemId}/live.m3u8 | Gets a hls live stream. |
| GET | /Videos/{itemId}/{stream}.{container} | Gets a video stream. |
| HEAD | /Videos/{itemId}/{stream}.{container} | Gets a video stream. |
| GET | /Videos/{itemId}/AdditionalParts | Gets additional parts for a video. |
| DELETE | /Videos/{itemId}/AlternateSources | Removes alternate video sources. |
| GET | /Videos/{itemId}/stream | Gets a video stream. |
| HEAD | /Videos/{itemId}/stream | Gets a video stream. |
| POST | /Videos/MergeVersions | Merges videos into a single record. |

### Environment
| Method | Path | Description |
|--------|------|-------------|
| GET | /Environment/DefaultDirectoryBrowser | Get Default directory browser. |
| GET | /Environment/DirectoryContents | Gets the contents of a given directory in the file system. |
| GET | /Environment/Drives | Gets available drives from the server's file system. |
| GET | /Environment/NetworkShares | Gets network paths. |
| GET | /Environment/ParentPath | Gets the parent path of a given path. |
| POST | /Environment/ValidatePath | Validates path. |

### Items
| Method | Path | Description |
|--------|------|-------------|
| GET | /Items/Filters | Gets legacy query filters. |
| GET | /Items/Filters2 | Gets query filters. |
| GET | /Items/{itemId}/Images | Get item image infos. |
| DELETE | /Items/{itemId}/Images/{imageType} | Delete an item's image. |
| POST | /Items/{itemId}/Images/{imageType} | Set item image. |
| GET | /Items/{itemId}/Images/{imageType} | Gets the item's image. |
| HEAD | /Items/{itemId}/Images/{imageType} | Gets the item's image. |
| DELETE | /Items/{itemId}/Images/{imageType}/{imageIndex} | Delete an item's image. |
| POST | /Items/{itemId}/Images/{imageType}/{imageIndex} | Set item image. |
| GET | /Items/{itemId}/Images/{imageType}/{imageIndex} | Gets the item's image. |
| HEAD | /Items/{itemId}/Images/{imageType}/{imageIndex} | Gets the item's image. |
| GET | /Items/{itemId}/Images/{imageType}/{imageIndex}/{tag}/{format}/{maxWidth}/{maxHeight}/{percentPlayed}/{unplayedCount} | Gets the item's image. |
| HEAD | /Items/{itemId}/Images/{imageType}/{imageIndex}/{tag}/{format}/{maxWidth}/{maxHeight}/{percentPlayed}/{unplayedCount} | Gets the item's image. |
| POST | /Items/{itemId}/Images/{imageType}/{imageIndex}/Index | Updates the index for an item image. |
| GET | /Items/{id}/InstantMix | Creates an instant playlist based on a given song. |
| GET | /Items/{itemId}/ExternalIdInfos | Get the item's external id info. |
| POST | /Items/RemoteSearch/Apply/{itemId} | Applies search criteria to an item and refreshes metadata. |
| POST | /Items/RemoteSearch/Book | Get book remote search. |
| POST | /Items/RemoteSearch/BoxSet | Get box set remote search. |
| GET | /Items/RemoteSearch/Image | Gets a remote image. |
| POST | /Items/RemoteSearch/Movie | Get movie remote search. |
| POST | /Items/RemoteSearch/MusicAlbum | Get music album remote search. |
| POST | /Items/RemoteSearch/MusicArtist | Get music artist remote search. |
| POST | /Items/RemoteSearch/MusicVideo | Get music video remote search. |
| POST | /Items/RemoteSearch/Person | Get person remote search. |
| POST | /Items/RemoteSearch/Series | Get series remote search. |
| POST | /Items/RemoteSearch/Trailer | Get trailer remote search. |
| POST | /Items/{itemId}/Refresh | Refreshes metadata for an item. |
| GET | /Items | Gets items based on a query. |
| DELETE | /Items | Deletes items from the library and filesystem. |
| POST | /Items/{itemId} | Updates an item. |
| DELETE | /Items/{itemId} | Deletes an item from the library and filesystem. |
| POST | /Items/{itemId}/ContentType | Updates an item's content type. |
| GET | /Items/{itemId}/MetadataEditor | Gets metadata editor info for an item. |
| GET | /Items/{itemId}/Ancestors | Gets all parents of an item. |
| GET | /Items/{itemId}/CriticReviews | Gets critic review for an item. |
| GET | /Items/{itemId}/Download | Downloads item media. |
| GET | /Items/{itemId}/File | Get the original file of an item. |
| GET | /Items/{itemId}/Similar | Gets similar items. |
| GET | /Items/{itemId}/ThemeMedia | Get theme songs and videos for an item. |
| GET | /Items/{itemId}/ThemeSongs | Get theme songs for an item. |
| GET | /Items/{itemId}/ThemeVideos | Get theme videos for an item. |
| GET | /Items/Counts | Get item counts. |
| GET | /Items/{itemId}/PlaybackInfo | Gets live playback media info for an item. |
| POST | /Items/{itemId}/PlaybackInfo | Gets live playback media info for an item. |
| GET | /Items/{itemId}/RemoteImages | Gets available remote images for an item. |
| POST | /Items/{itemId}/RemoteImages/Download | Downloads a remote image for an item. |
| GET | /Items/{itemId}/RemoteImages/Providers | Gets available remote image providers for an item. |
| GET | /Items/{itemId}/RemoteSearch/Subtitles/{language} | Search remote subtitles. |
| POST | /Items/{itemId}/RemoteSearch/Subtitles/{subtitleId} | Downloads a remote subtitle. |

### Genres
| Method | Path | Description |
|--------|------|-------------|
| GET | /Genres | Gets all genres from a given item, folder, or the entire library. |
| GET | /Genres/{genreName} | Gets a genre, by name. |
| GET | /Genres/{name}/Images/{imageType} | Get genre image by name. |
| HEAD | /Genres/{name}/Images/{imageType} | Get genre image by name. |
| GET | /Genres/{name}/Images/{imageType}/{imageIndex} | Get genre image by name. |
| HEAD | /Genres/{name}/Images/{imageType}/{imageIndex} | Get genre image by name. |

### MusicGenres
| Method | Path | Description |
|--------|------|-------------|
| GET | /MusicGenres/{name}/Images/{imageType} | Get music genre image by name. |
| HEAD | /MusicGenres/{name}/Images/{imageType} | Get music genre image by name. |
| GET | /MusicGenres/{name}/Images/{imageType}/{imageIndex} | Get music genre image by name. |
| HEAD | /MusicGenres/{name}/Images/{imageType}/{imageIndex} | Get music genre image by name. |
| GET | /MusicGenres/{id}/InstantMix | Creates an instant playlist based on a given song. |
| GET | /MusicGenres/{name}/InstantMix | Creates an instant playlist based on a given song. |
| GET | /MusicGenres | Gets all music genres from a given item, folder, or the entire library. |
| GET | /MusicGenres/{genreName} | Gets a music genre, by name. |

### Persons
| Method | Path | Description |
|--------|------|-------------|
| GET | /Persons/{name}/Images/{imageType} | Get person image by name. |
| HEAD | /Persons/{name}/Images/{imageType} | Get person image by name. |
| GET | /Persons/{name}/Images/{imageType}/{imageIndex} | Get person image by name. |
| HEAD | /Persons/{name}/Images/{imageType}/{imageIndex} | Get person image by name. |
| GET | /Persons | Gets all persons. |
| GET | /Persons/{name} | Get person by name. |

### Studios
| Method | Path | Description |
|--------|------|-------------|
| GET | /Studios/{name}/Images/{imageType} | Get studio image by name. |
| HEAD | /Studios/{name}/Images/{imageType} | Get studio image by name. |
| GET | /Studios/{name}/Images/{imageType}/{imageIndex} | Get studio image by name. |
| HEAD | /Studios/{name}/Images/{imageType}/{imageIndex} | Get studio image by name. |
| GET | /Studios | Gets all studios from a given item, folder, or the entire library. |
| GET | /Studios/{name} | Gets a studio by name. |

### Users
| Method | Path | Description |
|--------|------|-------------|
| POST | /Users/{userId}/Images/{imageType} | Sets the user image. |
| DELETE | /Users/{userId}/Images/{imageType} | Delete the user's image. |
| GET | /Users/{userId}/Images/{imageType} | Get user profile image. |
| HEAD | /Users/{userId}/Images/{imageType} | Get user profile image. |
| GET | /Users/{userId}/Images/{imageType}/{imageIndex} | Get user profile image. |
| HEAD | /Users/{userId}/Images/{imageType}/{imageIndex} | Get user profile image. |
| POST | /Users/{userId}/Images/{imageType}/{index} | Sets the user image. |
| DELETE | /Users/{userId}/Images/{imageType}/{index} | Delete the user's image. |
| GET | /Users/{userId}/Items | Gets items based on a query. |
| GET | /Users/{userId}/Items/Resume | Gets items based on a query. |
| POST | /Users/{userId}/PlayedItems/{itemId} | Marks an item as played for user. |
| DELETE | /Users/{userId}/PlayedItems/{itemId} | Marks an item as unplayed for user. |
| POST | /Users/{userId}/PlayingItems/{itemId} | Reports that a user has begun playing an item. |
| DELETE | /Users/{userId}/PlayingItems/{itemId} | Reports that a user has stopped playing an item. |
| POST | /Users/{userId}/PlayingItems/{itemId}/Progress | Reports a user's playback progress. |
| GET | /Users/{userId}/Suggestions | Gets suggestions. |
| GET | /Users | Gets a list of users. |
| GET | /Users/{userId} | Gets a user by Id. |
| DELETE | /Users/{userId} | Deletes a user. |
| POST | /Users/{userId} | Updates a user. |
| POST | /Users/{userId}/Authenticate | Authenticates a user. |
| POST | /Users/{userId}/Configuration | Updates a user configuration. |
| POST | /Users/{userId}/EasyPassword | Updates a user's easy password. |
| POST | /Users/{userId}/Password | Updates a user's password. |
| POST | /Users/{userId}/Policy | Updates a user policy. |
| POST | /Users/AuthenticateByName | Authenticates a user by name. |
| POST | /Users/AuthenticateWithQuickConnect | Authenticates a user with quick connect. |
| POST | /Users/ForgotPassword | Initiates the forgot password process for a local user. |
| POST | /Users/ForgotPassword/Pin | Redeems a forgot password pin. |
| GET | /Users/Me | Gets the user based on auth token. |
| POST | /Users/New | Creates a user. |
| GET | /Users/Public | Gets a list of publicly visible users for display on a login screen. |
| POST | /Users/{userId}/FavoriteItems/{itemId} | Marks an item as a favorite. |
| DELETE | /Users/{userId}/FavoriteItems/{itemId} | Unmarks item as a favorite. |
| GET | /Users/{userId}/Items/{itemId} | Gets an item from a user's library. |
| GET | /Users/{userId}/Items/{itemId}/Intros | Gets intros to play before the main media item plays. |
| GET | /Users/{userId}/Items/{itemId}/LocalTrailers | Gets local trailers for an item. |
| DELETE | /Users/{userId}/Items/{itemId}/Rating | Deletes a user's saved personal rating for an item. |
| POST | /Users/{userId}/Items/{itemId}/Rating | Updates a user's rating for an item. |
| GET | /Users/{userId}/Items/{itemId}/SpecialFeatures | Gets special features for an item. |
| GET | /Users/{userId}/Items/Latest | Gets latest media. |
| GET | /Users/{userId}/Items/Root | Gets the root folder from a user's library. |
| GET | /Users/{userId}/GroupingOptions | Get user view grouping options. |
| GET | /Users/{userId}/Views | Get user views. |

### Images
| Method | Path | Description |
|--------|------|-------------|
| GET | /Images/General | Get all general images. |
| GET | /Images/General/{name}/{type} | Get General Image. |
| GET | /Images/MediaInfo | Get all media info images. |
| GET | /Images/MediaInfo/{theme}/{name} | Get media info image. |
| GET | /Images/Ratings | Get all general images. |
| GET | /Images/Ratings/{theme}/{name} | Get rating image. |
| GET | /Images/Remote | Gets a remote image. |

### Albums
| Method | Path | Description |
|--------|------|-------------|
| GET | /Albums/{id}/InstantMix | Creates an instant playlist based on a given song. |
| GET | /Albums/{itemId}/Similar | Gets similar items. |

### Playlists
| Method | Path | Description |
|--------|------|-------------|
| GET | /Playlists/{id}/InstantMix | Creates an instant playlist based on a given song. |
| POST | /Playlists | Creates a new playlist. |
| POST | /Playlists/{playlistId}/Items | Adds items to a playlist. |
| DELETE | /Playlists/{playlistId}/Items | Removes items from a playlist. |
| GET | /Playlists/{playlistId}/Items | Gets the original items of a playlist. |
| POST | /Playlists/{playlistId}/Items/{itemId}/Move/{newIndex} | Moves a playlist item. |

### Songs
| Method | Path | Description |
|--------|------|-------------|
| GET | /Songs/{id}/InstantMix | Creates an instant playlist based on a given song. |

### Libraries
| Method | Path | Description |
|--------|------|-------------|
| GET | /Libraries/AvailableOptions | Gets the library options info. |

### Library
| Method | Path | Description |
|--------|------|-------------|
| POST | /Library/Media/Updated | Reports that new movies have been added by an external source. |
| GET | /Library/MediaFolders | Gets all user media folders. |
| POST | /Library/Movies/Added | Reports that new movies have been added by an external source. |
| POST | /Library/Movies/Updated | Reports that new movies have been added by an external source. |
| GET | /Library/PhysicalPaths | Gets a list of physical paths from virtual folders. |
| GET | /Library/Refresh | Starts a library scan. |
| POST | /Library/Series/Added | Reports that new episodes of a series have been added by an external source. |
| POST | /Library/Series/Updated | Reports that new episodes of a series have been added by an external source. |
| GET | /Library/VirtualFolders | Gets all virtual folders. |
| POST | /Library/VirtualFolders | Adds a virtual folder. |
| DELETE | /Library/VirtualFolders | Removes a virtual folder. |
| POST | /Library/VirtualFolders/LibraryOptions | Update library options. |
| POST | /Library/VirtualFolders/Name | Renames a virtual folder. |
| POST | /Library/VirtualFolders/Paths | Add a media path to a library. |
| DELETE | /Library/VirtualFolders/Paths | Remove a media path. |
| POST | /Library/VirtualFolders/Paths/Update | Updates a media path. |

### Movies
| Method | Path | Description |
|--------|------|-------------|
| GET | /Movies/{itemId}/Similar | Gets similar items. |
| GET | /Movies/Recommendations | Gets movie recommendations. |

### Shows
| Method | Path | Description |
|--------|------|-------------|
| GET | /Shows/{itemId}/Similar | Gets similar items. |
| GET | /Shows/{seriesId}/Episodes | Gets episodes for a tv season. |
| GET | /Shows/{seriesId}/Seasons | Gets seasons for a tv series. |
| GET | /Shows/NextUp | Gets a list of next up episodes. |
| GET | /Shows/Upcoming | Gets a list of upcoming episodes. |

### Trailers
| Method | Path | Description |
|--------|------|-------------|
| GET | /Trailers/{itemId}/Similar | Gets similar items. |
| GET | /Trailers | Finds movies and trailers similar to a given trailer. |

### LiveTv
| Method | Path | Description |
|--------|------|-------------|
| GET | /LiveTv/ChannelMappingOptions | Get channel mapping options. |
| POST | /LiveTv/ChannelMappings | Set channel mappings. |
| GET | /LiveTv/Channels | Gets available live tv channels. |
| GET | /LiveTv/Channels/{channelId} | Gets a live tv channel. |
| GET | /LiveTv/GuideInfo | Get guid info. |
| GET | /LiveTv/Info | Gets available live tv services. |
| POST | /LiveTv/ListingProviders | Adds a listings provider. |
| DELETE | /LiveTv/ListingProviders | Delete listing provider. |
| GET | /LiveTv/ListingProviders/Default | Gets default listings provider info. |
| GET | /LiveTv/ListingProviders/Lineups | Gets available lineups. |
| GET | /LiveTv/ListingProviders/SchedulesDirect/Countries | Gets available countries. |
| GET | /LiveTv/LiveRecordings/{recordingId}/stream | Gets a live tv recording stream. |
| GET | /LiveTv/LiveStreamFiles/{streamId}/stream.{container} | Gets a live tv channel stream. |
| GET | /LiveTv/Programs | Gets available live tv epgs. |
| POST | /LiveTv/Programs | Gets available live tv epgs. |
| GET | /LiveTv/Programs/{programId} | Gets a live tv program. |
| GET | /LiveTv/Programs/Recommended | Gets recommended live tv epgs. |
| GET | /LiveTv/Recordings | Gets live tv recordings. |
| GET | /LiveTv/Recordings/{recordingId} | Gets a live tv recording. |
| DELETE | /LiveTv/Recordings/{recordingId} | Deletes a live tv recording. |
| GET | /LiveTv/Recordings/Folders | Gets recording folders. |
| GET | /LiveTv/Recordings/Groups | Gets live tv recording groups. |
| GET | /LiveTv/Recordings/Groups/{groupId} | Get recording group. |
| GET | /LiveTv/Recordings/Series | Gets live tv recording series. |
| GET | /LiveTv/SeriesTimers | Gets live tv series timers. |
| POST | /LiveTv/SeriesTimers | Creates a live tv series timer. |
| GET | /LiveTv/SeriesTimers/{timerId} | Gets a live tv series timer. |
| DELETE | /LiveTv/SeriesTimers/{timerId} | Cancels a live tv series timer. |
| POST | /LiveTv/SeriesTimers/{timerId} | Updates a live tv series timer. |
| GET | /LiveTv/Timers | Gets the live tv timers. |
| POST | /LiveTv/Timers | Creates a live tv timer. |
| GET | /LiveTv/Timers/{timerId} | Gets a timer. |
| DELETE | /LiveTv/Timers/{timerId} | Cancels a live tv timer. |
| POST | /LiveTv/Timers/{timerId} | Updates a live tv timer. |
| GET | /LiveTv/Timers/Defaults | Gets the default values for a new timer. |
| POST | /LiveTv/TunerHosts | Adds a tuner host. |
| DELETE | /LiveTv/TunerHosts | Deletes a tuner host. |
| GET | /LiveTv/TunerHosts/Types | Get tuner host types. |
| POST | /LiveTv/Tuners/{tunerId}/Reset | Resets a tv tuner. |
| GET | /LiveTv/Tuners/Discover | Discover tuners. |
| GET | /LiveTv/Tuners/Discvover | Discover tuners. |

### Localization
| Method | Path | Description |
|--------|------|-------------|
| GET | /Localization/Countries | Gets known countries. |
| GET | /Localization/Cultures | Gets known cultures. |
| GET | /Localization/Options | Gets localization options. |
| GET | /Localization/ParentalRatings | Gets known parental ratings. |

### LiveStreams
| Method | Path | Description |
|--------|------|-------------|
| POST | /LiveStreams/Close | Closes a media source. |
| POST | /LiveStreams/Open | Opens a media source. |

### Playback
| Method | Path | Description |
|--------|------|-------------|
| GET | /Playback/BitrateTest | Tests the network with a request with the size of the bitrate. |

### Notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /Notifications/{userId} | Gets a user's notifications. |
| POST | /Notifications/{userId}/Read | Sets notifications as read. |
| GET | /Notifications/{userId}/Summary | Gets a user's notification summary. |
| POST | /Notifications/{userId}/Unread | Sets notifications as unread. |
| POST | /Notifications/Admin | Sends a notification to all admins. |
| GET | /Notifications/Services | Gets notification services. |
| GET | /Notifications/Types | Gets notification types. |

### Packages
| Method | Path | Description |
|--------|------|-------------|
| GET | /Packages | Gets available packages. |
| GET | /Packages/{name} | Gets a package by name or assembly GUID. |
| POST | /Packages/Installed/{name} | Installs a package. |
| DELETE | /Packages/Installing/{packageId} | Cancels a package installation. |

### Repositories
| Method | Path | Description |
|--------|------|-------------|
| GET | /Repositories | Gets all package repositories. |
| POST | /Repositories | Sets the enabled and existing package repositories. |

### Sessions
| Method | Path | Description |
|--------|------|-------------|
| POST | /Sessions/Playing | Reports playback has started within a session. |
| POST | /Sessions/Playing/Ping | Pings a playback session. |
| POST | /Sessions/Playing/Progress | Reports playback progress within a session. |
| POST | /Sessions/Playing/Stopped | Reports playback has stopped within a session. |
| GET | /Sessions | Gets a list of sessions. |
| POST | /Sessions/{sessionId}/Command | Issues a full general command to a client. |
| POST | /Sessions/{sessionId}/Command/{command} | Issues a general command to a client. |
| POST | /Sessions/{sessionId}/Message | Issues a command to a client to display a message to the user. |
| POST | /Sessions/{sessionId}/Playing | Instructs a session to play an item. |
| POST | /Sessions/{sessionId}/Playing/{command} | Issues a playstate command to a client. |
| POST | /Sessions/{sessionId}/System/{command} | Issues a system command to a client. |
| POST | /Sessions/{sessionId}/User/{userId} | Adds an additional user to a session. |
| DELETE | /Sessions/{sessionId}/User/{userId} | Removes an additional user from a session. |
| POST | /Sessions/{sessionId}/Viewing | Instructs a session to browse to an item or view. |
| POST | /Sessions/Capabilities | Updates capabilities for a device. |
| POST | /Sessions/Capabilities/Full | Updates capabilities for a device. |
| POST | /Sessions/Logout | Reports that a session has ended. |
| POST | /Sessions/Viewing | Reports that a session is viewing an item. |

### Plugins
| Method | Path | Description |
|--------|------|-------------|
| GET | /Plugins | Gets a list of currently installed plugins. |
| DELETE | /Plugins/{pluginId} | Uninstalls a plugin. |
| DELETE | /Plugins/{pluginId}/{version} | Uninstalls a plugin by version. |
| POST | /Plugins/{pluginId}/{version}/Disable | Disable a plugin. |
| POST | /Plugins/{pluginId}/{version}/Enable | Enables a disabled plugin. |
| GET | /Plugins/{pluginId}/{version}/Image | Gets a plugin's image. |
| GET | /Plugins/{pluginId}/Configuration | Gets plugin configuration. |
| POST | /Plugins/{pluginId}/Configuration | Updates plugin configuration. |
| POST | /Plugins/{pluginId}/Manifest | Gets a plugin's manifest. |
| POST | /Plugins/SecurityInfo | Updates plugin security info. |

### QuickConnect
| Method | Path | Description |
|--------|------|-------------|
| POST | /QuickConnect/Activate | Temporarily activates quick connect for five minutes. |
| POST | /QuickConnect/Authorize | Authorizes a pending quick connect request. |
| POST | /QuickConnect/Available | Enables or disables quick connect. |
| GET | /QuickConnect/Connect | Attempts to retrieve authentication information. |
| POST | /QuickConnect/Deauthorize | Deauthorize all quick connect devices for the current user. |
| GET | /QuickConnect/Initiate | Initiate a new quick connect request. |
| GET | /QuickConnect/Status | Gets the current quick connect state. |

### ScheduledTasks
| Method | Path | Description |
|--------|------|-------------|
| GET | /ScheduledTasks | Get tasks. |
| GET | /ScheduledTasks/{taskId} | Get task by id. |
| POST | /ScheduledTasks/{taskId}/Triggers | Update specified task triggers. |
| POST | /ScheduledTasks/Running/{taskId} | Start specified task. |
| DELETE | /ScheduledTasks/Running/{taskId} | Stop specified task. |

### Search
| Method | Path | Description |
|--------|------|-------------|
| GET | /Search/Hints | Gets the search hint result. |

### Startup
| Method | Path | Description |
|--------|------|-------------|
| POST | /Startup/Complete | Completes the startup wizard. |
| GET | /Startup/Configuration | Gets the initial startup wizard configuration. |
| POST | /Startup/Configuration | Sets the initial startup wizard configuration. |
| GET | /Startup/FirstUser | Gets the first user. |
| POST | /Startup/RemoteAccess | Sets remote access and UPnP. |
| GET | /Startup/User | Gets the first user. |
| POST | /Startup/User | Sets the user name and password. |

### FallbackFont
| Method | Path | Description |
|--------|------|-------------|
| GET | /FallbackFont/Fonts | Gets a list of available fallback font files. |
| GET | /FallbackFont/Fonts/{name} | Gets a fallback font file. |

### Providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /Providers/Subtitles/Subtitles/{id} | Gets the remote subtitles. |

### SyncPlay
| Method | Path | Description |
|--------|------|-------------|
| POST | /SyncPlay/Buffering | Notify SyncPlay group that member is buffering. |
| POST | /SyncPlay/Join | Join an existing SyncPlay group. |
| POST | /SyncPlay/Leave | Leave the joined SyncPlay group. |
| GET | /SyncPlay/List | Gets all SyncPlay groups. |
| POST | /SyncPlay/MovePlaylistItem | Request to move an item in the playlist in SyncPlay group. |
| POST | /SyncPlay/New | Create a new SyncPlay group. |
| POST | /SyncPlay/NextItem | Request next item in SyncPlay group. |
| POST | /SyncPlay/Pause | Request pause in SyncPlay group. |
| POST | /SyncPlay/Ping | Update session ping. |
| POST | /SyncPlay/PreviousItem | Request previous item in SyncPlay group. |
| POST | /SyncPlay/Queue | Request to queue items to the playlist of a SyncPlay group. |
| POST | /SyncPlay/Ready | Notify SyncPlay group that member is ready for playback. |
| POST | /SyncPlay/RemoveFromPlaylist | Request to remove items from the playlist in SyncPlay group. |
| POST | /SyncPlay/Seek | Request seek in SyncPlay group. |
| POST | /SyncPlay/SetIgnoreWait | Request SyncPlay group to ignore member during group-wait. |
| POST | /SyncPlay/SetNewQueue | Request to set new playlist in SyncPlay group. |
| POST | /SyncPlay/SetPlaylistItem | Request to change playlist item in SyncPlay group. |
| POST | /SyncPlay/SetRepeatMode | Request to set repeat mode in SyncPlay group. |
| POST | /SyncPlay/SetShuffleMode | Request to set shuffle mode in SyncPlay group. |
| POST | /SyncPlay/Stop | Request stop in SyncPlay group. |
| POST | /SyncPlay/Unpause | Request unpause in SyncPlay group. |

### GetUtcTime
| Method | Path | Description |
|--------|------|-------------|
| GET | /GetUtcTime | Gets the current UTC time. |

### Years
| Method | Path | Description |
|--------|------|-------------|
| GET | /Years | Get years. |
| GET | /Years/{year} | Gets a year. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Entries?" -> GET /System/ActivityLog/Entries
- "List all Keys?" -> GET /Auth/Keys
- "Create a Key?" -> POST /Auth/Keys
- "Delete a Key?" -> DELETE /Auth/Keys/{key}
- "List all Artists?" -> GET /Artists
- "Get Artist details?" -> GET /Artists/{name}
- "List all AlbumArtists?" -> GET /Artists/AlbumArtists
- "List all stream?" -> GET /Audio/{itemId}/stream
- "Get stream.{container} details?" -> GET /Audio/{itemId}/stream.{container}
- "List all Configuration?" -> GET /Branding/Configuration
- "List all Css?" -> GET /Branding/Css
- "List all Css.css?" -> GET /Branding/Css.css
- "List all Channels?" -> GET /Channels
- "List all Features?" -> GET /Channels/{channelId}/Features
- "List all Items?" -> GET /Channels/{channelId}/Items
- "List all Features?" -> GET /Channels/Features
- "List all Latest?" -> GET /Channels/Items/Latest
- "Create a Collection?" -> POST /Collections
- "Create a Item?" -> POST /Collections/{collectionId}/Items
- "List all Configuration?" -> GET /System/Configuration
- "Create a Configuration?" -> POST /System/Configuration
- "Get Configuration details?" -> GET /System/Configuration/{key}
- "List all Default?" -> GET /System/Configuration/MetadataOptions/Default
- "Create a Path?" -> POST /System/MediaEncoder/Path
- "List all ConfigurationPage?" -> GET /web/ConfigurationPage
- "List all ConfigurationPages?" -> GET /web/ConfigurationPages
- "List all Devices?" -> GET /Devices
- "List all Info?" -> GET /Devices/Info
- "List all Options?" -> GET /Devices/Options
- "Create a Option?" -> POST /Devices/Options
- "Get DisplayPreference details?" -> GET /DisplayPreferences/{displayPreferencesId}
- "List all ProfileInfos?" -> GET /Dlna/ProfileInfos
- "Create a Profile?" -> POST /Dlna/Profiles
- "Get Profile details?" -> GET /Dlna/Profiles/{profileId}
- "Delete a Profile?" -> DELETE /Dlna/Profiles/{profileId}
- "List all Default?" -> GET /Dlna/Profiles/Default
- "List all ConnectionManager?" -> GET /Dlna/{serverId}/ConnectionManager
- "List all ConnectionManager?" -> GET /Dlna/{serverId}/ConnectionManager/ConnectionManager
- "List all ConnectionManager.xml?" -> GET /Dlna/{serverId}/ConnectionManager/ConnectionManager.xml
- "Create a Control?" -> POST /Dlna/{serverId}/ConnectionManager/Control
- "List all ContentDirectory?" -> GET /Dlna/{serverId}/ContentDirectory
- "List all ContentDirectory?" -> GET /Dlna/{serverId}/ContentDirectory/ContentDirectory
- "List all ContentDirectory.xml?" -> GET /Dlna/{serverId}/ContentDirectory/ContentDirectory.xml
- "Create a Control?" -> POST /Dlna/{serverId}/ContentDirectory/Control
- "List all description?" -> GET /Dlna/{serverId}/description
- "List all description.xml?" -> GET /Dlna/{serverId}/description.xml
- "Get icon details?" -> GET /Dlna/{serverId}/icons/{fileName}
- "List all MediaReceiverRegistrar?" -> GET /Dlna/{serverId}/MediaReceiverRegistrar
- "Create a Control?" -> POST /Dlna/{serverId}/MediaReceiverRegistrar/Control
- "List all MediaReceiverRegistrar?" -> GET /Dlna/{serverId}/MediaReceiverRegistrar/MediaReceiverRegistrar
- "List all MediaReceiverRegistrar.xml?" -> GET /Dlna/{serverId}/MediaReceiverRegistrar/MediaReceiverRegistrar.xml
- "Get icon details?" -> GET /Dlna/icons/{fileName}
- "Get hls1 details?" -> GET /Audio/{itemId}/hls1/{playlistId}/{segmentId}.{container}
- "List all main.m3u8?" -> GET /Audio/{itemId}/main.m3u8
- "List all master.m3u8?" -> GET /Audio/{itemId}/master.m3u8
- "Get hls1 details?" -> GET /Videos/{itemId}/hls1/{playlistId}/{segmentId}.{container}
- "List all main.m3u8?" -> GET /Videos/{itemId}/main.m3u8
- "List all master.m3u8?" -> GET /Videos/{itemId}/master.m3u8
- "List all DefaultDirectoryBrowser?" -> GET /Environment/DefaultDirectoryBrowser
- "List all DirectoryContents?" -> GET /Environment/DirectoryContents
- "List all Drives?" -> GET /Environment/Drives
- "List all NetworkShares?" -> GET /Environment/NetworkShares
- "List all ParentPath?" -> GET /Environment/ParentPath
- "Create a ValidatePath?" -> POST /Environment/ValidatePath
- "List all Filters?" -> GET /Items/Filters
- "List all Filters2?" -> GET /Items/Filters2
- "List all Genres?" -> GET /Genres
- "Get Genre details?" -> GET /Genres/{genreName}
- "List all stream.aac?" -> GET /Audio/{itemId}/hls/{segmentId}/stream.aac
- "List all stream.mp3?" -> GET /Audio/{itemId}/hls/{segmentId}/stream.mp3
- "Get hl details?" -> GET /Videos/{itemId}/hls/{playlistId}/{segmentId}.{segmentContainer}
- "List all stream.m3u8?" -> GET /Videos/{itemId}/hls/{playlistId}/stream.m3u8
- "Get Image details?" -> GET /Artists/{name}/Images/{imageType}/{imageIndex}
- "Get Image details?" -> GET /Genres/{name}/Images/{imageType}
- "Get Image details?" -> GET /Genres/{name}/Images/{imageType}/{imageIndex}
- "List all Images?" -> GET /Items/{itemId}/Images
- "Delete a Image?" -> DELETE /Items/{itemId}/Images/{imageType}
- "Get Image details?" -> GET /Items/{itemId}/Images/{imageType}
- "Delete a Image?" -> DELETE /Items/{itemId}/Images/{imageType}/{imageIndex}
- "Get Image details?" -> GET /Items/{itemId}/Images/{imageType}/{imageIndex}
- "Get Image details?" -> GET /Items/{itemId}/Images/{imageType}/{imageIndex}/{tag}/{format}/{maxWidth}/{maxHeight}/{percentPlayed}/{unplayedCount}
- "Create a Index?" -> POST /Items/{itemId}/Images/{imageType}/{imageIndex}/Index
- "Get Image details?" -> GET /MusicGenres/{name}/Images/{imageType}
- "Get Image details?" -> GET /MusicGenres/{name}/Images/{imageType}/{imageIndex}
- "Get Image details?" -> GET /Persons/{name}/Images/{imageType}
- "Get Image details?" -> GET /Persons/{name}/Images/{imageType}/{imageIndex}
- "Get Image details?" -> GET /Studios/{name}/Images/{imageType}
- "Get Image details?" -> GET /Studios/{name}/Images/{imageType}/{imageIndex}
- "Delete a Image?" -> DELETE /Users/{userId}/Images/{imageType}
- "Get Image details?" -> GET /Users/{userId}/Images/{imageType}
- "Get Image details?" -> GET /Users/{userId}/Images/{imageType}/{imageIndex}
- "Delete a Image?" -> DELETE /Users/{userId}/Images/{imageType}/{index}
- "List all General?" -> GET /Images/General
- "Get General details?" -> GET /Images/General/{name}/{type}
- "List all MediaInfo?" -> GET /Images/MediaInfo
- "Get MediaInfo details?" -> GET /Images/MediaInfo/{theme}/{name}
- "List all Ratings?" -> GET /Images/Ratings
- "Get Rating details?" -> GET /Images/Ratings/{theme}/{name}
- "List all InstantMix?" -> GET /Albums/{id}/InstantMix
- "List all InstantMix?" -> GET /Artists/{id}/InstantMix
- "List all InstantMix?" -> GET /Items/{id}/InstantMix
- "List all InstantMix?" -> GET /MusicGenres/{id}/InstantMix
- "List all InstantMix?" -> GET /MusicGenres/{name}/InstantMix
- "List all InstantMix?" -> GET /Playlists/{id}/InstantMix
- "List all InstantMix?" -> GET /Songs/{id}/InstantMix
- "List all ExternalIdInfos?" -> GET /Items/{itemId}/ExternalIdInfos
- "Create a Book?" -> POST /Items/RemoteSearch/Book
- "Create a BoxSet?" -> POST /Items/RemoteSearch/BoxSet
- "List all Image?" -> GET /Items/RemoteSearch/Image
- "Create a Movie?" -> POST /Items/RemoteSearch/Movie
- "Create a MusicAlbum?" -> POST /Items/RemoteSearch/MusicAlbum
- "Create a MusicArtist?" -> POST /Items/RemoteSearch/MusicArtist
- "Create a MusicVideo?" -> POST /Items/RemoteSearch/MusicVideo
- "Create a Person?" -> POST /Items/RemoteSearch/Person
- "Create a Sery?" -> POST /Items/RemoteSearch/Series
- "Create a Trailer?" -> POST /Items/RemoteSearch/Trailer
- "Create a Refresh?" -> POST /Items/{itemId}/Refresh
- "List all Items?" -> GET /Items
- "List all Items?" -> GET /Users/{userId}/Items
- "List all Resume?" -> GET /Users/{userId}/Items/Resume
- "Delete a Item?" -> DELETE /Items/{itemId}
- "Create a ContentType?" -> POST /Items/{itemId}/ContentType
- "List all MetadataEditor?" -> GET /Items/{itemId}/MetadataEditor
- "List all Similar?" -> GET /Albums/{itemId}/Similar
- "List all Similar?" -> GET /Artists/{itemId}/Similar
- "List all Ancestors?" -> GET /Items/{itemId}/Ancestors
- "List all CriticReviews?" -> GET /Items/{itemId}/CriticReviews
- "List all Download?" -> GET /Items/{itemId}/Download
- "List all File?" -> GET /Items/{itemId}/File
- "List all Similar?" -> GET /Items/{itemId}/Similar
- "List all ThemeMedia?" -> GET /Items/{itemId}/ThemeMedia
- "List all ThemeSongs?" -> GET /Items/{itemId}/ThemeSongs
- "List all ThemeVideos?" -> GET /Items/{itemId}/ThemeVideos
- "List all Counts?" -> GET /Items/Counts
- "List all AvailableOptions?" -> GET /Libraries/AvailableOptions
- "Create a Updated?" -> POST /Library/Media/Updated
- "List all MediaFolders?" -> GET /Library/MediaFolders
- "Create a Added?" -> POST /Library/Movies/Added
- "Create a Updated?" -> POST /Library/Movies/Updated
- "List all PhysicalPaths?" -> GET /Library/PhysicalPaths
- "List all Refresh?" -> GET /Library/Refresh
- "Create a Added?" -> POST /Library/Series/Added
- "Create a Updated?" -> POST /Library/Series/Updated
- "List all Similar?" -> GET /Movies/{itemId}/Similar
- "List all Similar?" -> GET /Shows/{itemId}/Similar
- "List all Similar?" -> GET /Trailers/{itemId}/Similar
- "List all VirtualFolders?" -> GET /Library/VirtualFolders
- "Create a VirtualFolder?" -> POST /Library/VirtualFolders
- "Create a LibraryOption?" -> POST /Library/VirtualFolders/LibraryOptions
- "Create a Name?" -> POST /Library/VirtualFolders/Name
- "Create a Path?" -> POST /Library/VirtualFolders/Paths
- "Create a Update?" -> POST /Library/VirtualFolders/Paths/Update
- "List all ChannelMappingOptions?" -> GET /LiveTv/ChannelMappingOptions
- "Create a ChannelMapping?" -> POST /LiveTv/ChannelMappings
- "List all Channels?" -> GET /LiveTv/Channels
- "Get Channel details?" -> GET /LiveTv/Channels/{channelId}
- "List all GuideInfo?" -> GET /LiveTv/GuideInfo
- "List all Info?" -> GET /LiveTv/Info
- "Create a ListingProvider?" -> POST /LiveTv/ListingProviders
- "List all Default?" -> GET /LiveTv/ListingProviders/Default
- "List all Lineups?" -> GET /LiveTv/ListingProviders/Lineups
- "List all Countries?" -> GET /LiveTv/ListingProviders/SchedulesDirect/Countries
- "List all stream?" -> GET /LiveTv/LiveRecordings/{recordingId}/stream
- "Get stream.{container} details?" -> GET /LiveTv/LiveStreamFiles/{streamId}/stream.{container}
- "List all Programs?" -> GET /LiveTv/Programs
- "Create a Program?" -> POST /LiveTv/Programs
- "Get Program details?" -> GET /LiveTv/Programs/{programId}
- "List all Recommended?" -> GET /LiveTv/Programs/Recommended
- "List all Recordings?" -> GET /LiveTv/Recordings
- "Get Recording details?" -> GET /LiveTv/Recordings/{recordingId}
- "Delete a Recording?" -> DELETE /LiveTv/Recordings/{recordingId}
- "List all Folders?" -> GET /LiveTv/Recordings/Folders
- "List all Groups?" -> GET /LiveTv/Recordings/Groups
- "Get Group details?" -> GET /LiveTv/Recordings/Groups/{groupId}
- "List all Series?" -> GET /LiveTv/Recordings/Series
- "List all SeriesTimers?" -> GET /LiveTv/SeriesTimers
- "Create a SeriesTimer?" -> POST /LiveTv/SeriesTimers
- "Get SeriesTimer details?" -> GET /LiveTv/SeriesTimers/{timerId}
- "Delete a SeriesTimer?" -> DELETE /LiveTv/SeriesTimers/{timerId}
- "List all Timers?" -> GET /LiveTv/Timers
- "Create a Timer?" -> POST /LiveTv/Timers
- "Get Timer details?" -> GET /LiveTv/Timers/{timerId}
- "Delete a Timer?" -> DELETE /LiveTv/Timers/{timerId}
- "List all Defaults?" -> GET /LiveTv/Timers/Defaults
- "Create a TunerHost?" -> POST /LiveTv/TunerHosts
- "List all Types?" -> GET /LiveTv/TunerHosts/Types
- "Create a Reset?" -> POST /LiveTv/Tuners/{tunerId}/Reset
- "List all Discover?" -> GET /LiveTv/Tuners/Discover
- "List all Discvover?" -> GET /LiveTv/Tuners/Discvover
- "List all Countries?" -> GET /Localization/Countries
- "List all Cultures?" -> GET /Localization/Cultures
- "List all Options?" -> GET /Localization/Options
- "List all ParentalRatings?" -> GET /Localization/ParentalRatings
- "List all PlaybackInfo?" -> GET /Items/{itemId}/PlaybackInfo
- "Create a PlaybackInfo?" -> POST /Items/{itemId}/PlaybackInfo
- "Create a Close?" -> POST /LiveStreams/Close
- "Create a Open?" -> POST /LiveStreams/Open
- "List all BitrateTest?" -> GET /Playback/BitrateTest
- "List all Recommendations?" -> GET /Movies/Recommendations
- "List all MusicGenres?" -> GET /MusicGenres
- "Get MusicGenre details?" -> GET /MusicGenres/{genreName}
- "Get Notification details?" -> GET /Notifications/{userId}
- "Create a Read?" -> POST /Notifications/{userId}/Read
- "List all Summary?" -> GET /Notifications/{userId}/Summary
- "Create a Unread?" -> POST /Notifications/{userId}/Unread
- "Create a Admin?" -> POST /Notifications/Admin
- "List all Services?" -> GET /Notifications/Services
- "List all Types?" -> GET /Notifications/Types
- "List all Packages?" -> GET /Packages
- "Get Package details?" -> GET /Packages/{name}
- "Delete a Installing?" -> DELETE /Packages/Installing/{packageId}
- "List all Repositories?" -> GET /Repositories
- "Create a Repository?" -> POST /Repositories
- "List all Persons?" -> GET /Persons
- "Get Person details?" -> GET /Persons/{name}
- "Create a Playlist?" -> POST /Playlists
- "Create a Item?" -> POST /Playlists/{playlistId}/Items
- "List all Items?" -> GET /Playlists/{playlistId}/Items
- "Create a Playing?" -> POST /Sessions/Playing
- "Create a Ping?" -> POST /Sessions/Playing/Ping
- "Create a Progress?" -> POST /Sessions/Playing/Progress
- "Create a Stopped?" -> POST /Sessions/Playing/Stopped
- "Delete a PlayedItem?" -> DELETE /Users/{userId}/PlayedItems/{itemId}
- "Delete a PlayingItem?" -> DELETE /Users/{userId}/PlayingItems/{itemId}
- "Create a Progress?" -> POST /Users/{userId}/PlayingItems/{itemId}/Progress
- "List all Plugins?" -> GET /Plugins
- "Delete a Plugin?" -> DELETE /Plugins/{pluginId}
- "Delete a Plugin?" -> DELETE /Plugins/{pluginId}/{version}
- "Create a Disable?" -> POST /Plugins/{pluginId}/{version}/Disable
- "Create a Enable?" -> POST /Plugins/{pluginId}/{version}/Enable
- "List all Image?" -> GET /Plugins/{pluginId}/{version}/Image
- "List all Configuration?" -> GET /Plugins/{pluginId}/Configuration
- "Create a Configuration?" -> POST /Plugins/{pluginId}/Configuration
- "Create a Manifest?" -> POST /Plugins/{pluginId}/Manifest
- "Create a SecurityInfo?" -> POST /Plugins/SecurityInfo
- "Create a Activate?" -> POST /QuickConnect/Activate
- "Create a Authorize?" -> POST /QuickConnect/Authorize
- "Create a Available?" -> POST /QuickConnect/Available
- "List all Connect?" -> GET /QuickConnect/Connect
- "Create a Deauthorize?" -> POST /QuickConnect/Deauthorize
- "List all Initiate?" -> GET /QuickConnect/Initiate
- "List all Status?" -> GET /QuickConnect/Status
- "List all Remote?" -> GET /Images/Remote
- "List all RemoteImages?" -> GET /Items/{itemId}/RemoteImages
- "Create a Download?" -> POST /Items/{itemId}/RemoteImages/Download
- "List all Providers?" -> GET /Items/{itemId}/RemoteImages/Providers
- "List all ScheduledTasks?" -> GET /ScheduledTasks
- "Get ScheduledTask details?" -> GET /ScheduledTasks/{taskId}
- "Create a Trigger?" -> POST /ScheduledTasks/{taskId}/Triggers
- "Delete a Running?" -> DELETE /ScheduledTasks/Running/{taskId}
- "List all Hints?" -> GET /Search/Hints
- "List all PasswordResetProviders?" -> GET /Auth/PasswordResetProviders
- "List all Providers?" -> GET /Auth/Providers
- "List all Sessions?" -> GET /Sessions
- "Create a Command?" -> POST /Sessions/{sessionId}/Command
- "Create a Message?" -> POST /Sessions/{sessionId}/Message
- "Create a Playing?" -> POST /Sessions/{sessionId}/Playing
- "Delete a User?" -> DELETE /Sessions/{sessionId}/User/{userId}
- "Create a Viewing?" -> POST /Sessions/{sessionId}/Viewing
- "Create a Capability?" -> POST /Sessions/Capabilities
- "Create a Full?" -> POST /Sessions/Capabilities/Full
- "Create a Logout?" -> POST /Sessions/Logout
- "Create a Viewing?" -> POST /Sessions/Viewing
- "Create a Complete?" -> POST /Startup/Complete
- "List all Configuration?" -> GET /Startup/Configuration
- "Create a Configuration?" -> POST /Startup/Configuration
- "List all FirstUser?" -> GET /Startup/FirstUser
- "Create a RemoteAccess?" -> POST /Startup/RemoteAccess
- "List all User?" -> GET /Startup/User
- "Create a User?" -> POST /Startup/User
- "List all Studios?" -> GET /Studios
- "Get Studio details?" -> GET /Studios/{name}
- "List all Fonts?" -> GET /FallbackFont/Fonts
- "Get Font details?" -> GET /FallbackFont/Fonts/{name}
- "Get Subtitle details?" -> GET /Items/{itemId}/RemoteSearch/Subtitles/{language}
- "Get Subtitle details?" -> GET /Providers/Subtitles/Subtitles/{id}
- "Get Stream.{format} details?" -> GET /Videos/{itemId}/{mediaSourceId}/Subtitles/{index}/{startPositionTicks}/Stream.{format}
- "Get Stream.{format} details?" -> GET /Videos/{itemId}/{mediaSourceId}/Subtitles/{index}/Stream.{format}
- "List all subtitles.m3u8?" -> GET /Videos/{itemId}/{mediaSourceId}/Subtitles/{index}/subtitles.m3u8
- "Create a Subtitle?" -> POST /Videos/{itemId}/Subtitles
- "Delete a Subtitle?" -> DELETE /Videos/{itemId}/Subtitles/{index}
- "List all Suggestions?" -> GET /Users/{userId}/Suggestions
- "Create a Buffering?" -> POST /SyncPlay/Buffering
- "Create a Join?" -> POST /SyncPlay/Join
- "Create a Leave?" -> POST /SyncPlay/Leave
- "List all List?" -> GET /SyncPlay/List
- "Create a MovePlaylistItem?" -> POST /SyncPlay/MovePlaylistItem
- "Create a New?" -> POST /SyncPlay/New
- "Create a NextItem?" -> POST /SyncPlay/NextItem
- "Create a Pause?" -> POST /SyncPlay/Pause
- "Create a Ping?" -> POST /SyncPlay/Ping
- "Create a PreviousItem?" -> POST /SyncPlay/PreviousItem
- "Create a Queue?" -> POST /SyncPlay/Queue
- "Create a Ready?" -> POST /SyncPlay/Ready
- "Create a RemoveFromPlaylist?" -> POST /SyncPlay/RemoveFromPlaylist
- "Create a Seek?" -> POST /SyncPlay/Seek
- "Create a SetIgnoreWait?" -> POST /SyncPlay/SetIgnoreWait
- "Create a SetNewQueue?" -> POST /SyncPlay/SetNewQueue
- "Create a SetPlaylistItem?" -> POST /SyncPlay/SetPlaylistItem
- "Create a SetRepeatMode?" -> POST /SyncPlay/SetRepeatMode
- "Create a SetShuffleMode?" -> POST /SyncPlay/SetShuffleMode
- "Create a Stop?" -> POST /SyncPlay/Stop
- "Create a Unpause?" -> POST /SyncPlay/Unpause
- "List all Endpoint?" -> GET /System/Endpoint
- "List all Info?" -> GET /System/Info
- "List all Public?" -> GET /System/Info/Public
- "List all Logs?" -> GET /System/Logs
- "List all Log?" -> GET /System/Logs/Log
- "List all Ping?" -> GET /System/Ping
- "Create a Ping?" -> POST /System/Ping
- "Create a Restart?" -> POST /System/Restart
- "Create a Shutdown?" -> POST /System/Shutdown
- "List all WakeOnLanInfo?" -> GET /System/WakeOnLanInfo
- "List all GetUtcTime?" -> GET /GetUtcTime
- "List all Trailers?" -> GET /Trailers
- "List all Episodes?" -> GET /Shows/{seriesId}/Episodes
- "List all Seasons?" -> GET /Shows/{seriesId}/Seasons
- "List all NextUp?" -> GET /Shows/NextUp
- "List all Upcoming?" -> GET /Shows/Upcoming
- "List all universal?" -> GET /Audio/{itemId}/universal
- "List all Users?" -> GET /Users
- "Get User details?" -> GET /Users/{userId}
- "Delete a User?" -> DELETE /Users/{userId}
- "Create a Authenticate?" -> POST /Users/{userId}/Authenticate
- "Create a Configuration?" -> POST /Users/{userId}/Configuration
- "Create a EasyPassword?" -> POST /Users/{userId}/EasyPassword
- "Create a Password?" -> POST /Users/{userId}/Password
- "Create a Policy?" -> POST /Users/{userId}/Policy
- "Create a AuthenticateByName?" -> POST /Users/AuthenticateByName
- "Create a AuthenticateWithQuickConnect?" -> POST /Users/AuthenticateWithQuickConnect
- "Create a ForgotPassword?" -> POST /Users/ForgotPassword
- "Create a Pin?" -> POST /Users/ForgotPassword/Pin
- "List all Me?" -> GET /Users/Me
- "Create a New?" -> POST /Users/New
- "List all Public?" -> GET /Users/Public
- "Delete a FavoriteItem?" -> DELETE /Users/{userId}/FavoriteItems/{itemId}
- "Get Item details?" -> GET /Users/{userId}/Items/{itemId}
- "List all Intros?" -> GET /Users/{userId}/Items/{itemId}/Intros
- "List all LocalTrailers?" -> GET /Users/{userId}/Items/{itemId}/LocalTrailers
- "Create a Rating?" -> POST /Users/{userId}/Items/{itemId}/Rating
- "List all SpecialFeatures?" -> GET /Users/{userId}/Items/{itemId}/SpecialFeatures
- "List all Latest?" -> GET /Users/{userId}/Items/Latest
- "List all Root?" -> GET /Users/{userId}/Items/Root
- "List all GroupingOptions?" -> GET /Users/{userId}/GroupingOptions
- "List all Views?" -> GET /Users/{userId}/Views
- "Get Attachment details?" -> GET /Videos/{videoId}/{mediaSourceId}/Attachments/{index}
- "List all live.m3u8?" -> GET /Videos/{itemId}/live.m3u8
- "Get Video details?" -> GET /Videos/{itemId}/{stream}.{container}
- "List all AdditionalParts?" -> GET /Videos/{itemId}/AdditionalParts
- "List all stream?" -> GET /Videos/{itemId}/stream
- "Create a MergeVersion?" -> POST /Videos/MergeVersions
- "List all Years?" -> GET /Years
- "Get Year details?" -> GET /Years/{year}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
