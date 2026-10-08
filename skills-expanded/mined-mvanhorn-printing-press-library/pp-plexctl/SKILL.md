---
name: pp-plexctl
description: "Printing Press CLI for Plexctl. ## Content Types The API supports responses in both XML and JSON"
author: "keithah"
license: "Apache-2.0"
argument-hint: "<command> [args] | install cli|mcp"
allowed-tools: "Read Bash"
metadata:
  openclaw:
    requires:
      bins:
        - plexctl-pp-cli
    install:
      - kind: go
        bins: [plexctl-pp-cli]
        module: github.com/mvanhorn/printing-press-library/library/media-and-entertainment/plexctl/cmd/plexctl-pp-cli
---

# Plexctl — Printing Press CLI

## Prerequisites: Install the CLI

This skill drives the `plexctl-pp-cli` binary. **You must verify the CLI is installed before invoking any command from this skill.** If it is missing, install it first:

1. Install via the Printing Press installer. It defaults binaries to `$HOME/.local/bin` on macOS/Linux and `%LOCALAPPDATA%\Programs\PrintingPress\bin` on Windows:
   ```bash
   npx -y @mvanhorn/printing-press-library install plexctl --cli-only
   ```
2. Verify: `plexctl-pp-cli --version`
3. Ensure the reported install directory is on `$PATH` for the agent/runtime that will invoke this skill.

If the `npx` install fails (no Node, offline, etc.), fall back to a direct Go install (requires Go 1.26.6 or newer). This installs into `$GOPATH/bin` (default `$HOME/go/bin`), so add that directory to `$PATH` instead:

```bash
go install github.com/mvanhorn/printing-press-library/library/media-and-entertainment/plexctl/cmd/plexctl-pp-cli@latest
```

If `--version` reports "command not found" after install, the runtime cannot see the binary directory on `$PATH`. Do not proceed with skill commands until verification succeeds.

# API Info
## Content Types
The API supports responses in both XML and JSON, and clients can request one or the other using the standard `Accept` HTTP header. The default is XML, so JSON will only be returned if it's explicitly requested (`Accept: application/json`).  New applications should use JSON.

Throughout the docs, it's common for a examples to be given in JSON only since the JSON response would be preferred for new applications.

## Headers

PMS accept a variety of custom headers that follow the pattern `X-Plex-{name}`. The full set of headers isn't enumerated here since some may only apply to certain endpoints, but common headers that can be included on all requests include:

| Header | Description | Sample |
| --- | --- | --- |
| X-Plex-Client-Identifier | An opaque identifier unique to the client | abc123 |
| X-Plex-Token | An authentication token, obtained from plex.tv | XXXXXXXXXXXX |
| X-Plex-Product | The name of the client product | Plex for Roku |
| X-Plex-Version | The version of the client application | 2.4.1 |
| X-Plex-Platform | The platform of the client | Roku |
| X-Plex-Platform-Version | The version of the platform | 4.3 build 1057 |
| X-Plex-Device | A relatively friendly name for the client device | Roku 3 |
| X-Plex-Model | A potentially less friendly identifier for the device model | 4200X |
| X-Plex-Device-Vendor | The device vendor | Roku |
| X-Plex-Device-Name | A friendly name for the client | Living Room TV |
| X-Plex-Marketplace | The marketplace on which the client application is distributed  | googlePlay |

`X-Plex-Client-Identifier` is typically required, as is `X-Plex-Token` for authentication.

There's no standard way to send non-ASCII values as HTTP headers. We attempt to recognize and parse UTF-8 and ISO-8859-1. If you're sending something that may include non-ASCII characters (often `X-Plex-Device-Name`), use UTF-8 if possible.

These are referred to as headers throughout documentation, but all `X-Plex-` headers can also be sent as query string arguments.

## Auth

Most endpoints require token based authentication, and the token is expected to be sent in the `X-Plex-Token` header. Tokens are obtained from plex.tv.  See the <a href="#section/API-Info/Authenticating-with-Plex">Authenticating with Plex</a> section.

## Paths and Keys

Many parts of the API reference things that can be fetched by their `key`. These keys follow a sort of relative URL resolution pattern. Some examples will help clarify.

- For a request to `/library/sections` that includes an item with a `key` of `home` in the response, that item can be fetched at `/library/sections/home`.
- For a request to `/library/sections/home` that includes an item with a `key` of `/library/metadata/deadbeef` in the response, that item can be fetched at `/library/metadata/deadbeef`.

We say this follows a "sort of" relative URL resolution pattern because all requests are treated as though they have a trailing slash.

```
/library/sections/ + home => /library/sections/home
/library/sections + home => /library/sections/home
/library/sections + /library/sections/home => /library/sections/home
```

Just like URL resolution, keys may contain absolute URLs as well, especially absolute `https://...` URLs or custom `view://...` URLs. In these cases the key resolved by simply using it, the parent is irrelevant.

Also note that the features described in this API can generally be present at a different paths. The `/media/providers` path defines where all features can be found.  Note that a PMS can contain multiple providers which will be enumerated here.  For simplicity, these docs use the most common, default paths. But when we say that `/library/sections/{id}` is part of the API, what we really mean is that a endpoint exists which is composed of the key for the `content` feature and the key for the library section.

Finally, it's worth noting that many paths can potentially be discovered by walking API responses and fetching `key`s, but paths that aren't documented here aren't part of the API contract, they just happen to exist for a particular provider. For example, a particular content directory might include a directory with `key={baseLibraryPath}/genre`. That's not an official part of the API that's guaranteed to exist for every content directory, it's just a `key` that happened to exist within that content directory.

## Types

Many elements throughout the API have a `type` attribute. These types are meant to give helpful information, such as whether something is a movie library or a TV show library.  Some API elements rely on a type number so both are provided below

### List of Metadata Types

| Type Name | Type Number |
| -- | -- |
| `movie` | 1 |
| `show` | 2 |
| `season` | 3 |
| `episode` | 4 |
| `trailer` | 5 |
| `person` | 7 |
| `artist` | 8 |
| `album` | 9 |
| `track` | 10 |
| `clip` | 12 |
| `photo` | 13 |
| `photoalbum` | 14 |
| `playlist` | 15 |
| `playlistfolder` | 16 |
| `collection` | 18 |

When an element has both `type` and `key` attributes, the type describes what will be returned when fetching that key. Some types will return a list of other elements. That list may have a `Meta` element describing the specific types within the list. Consider the following examples:

```json
[
  {
    "key": "/foo",
    "type": "movie",
    "title": "A Movie"
  },
  {
    "key": "/bar",
    "type": "collection",
    "title": "My Favorite Movies"
  },
  {
    "key": "/baz",
    "type": "show",
    "title": "A Show"
  }
]
```

In each case, the `type` describes what will be returned when fetching the key. One exception is the `/children` key for parents like shows and seasons. It will return a list of children even though the `type` describes the parent.

Some elements may also include an optional `subtype` attribute. The subtype is meant to be a refinement of the type, not a completely different type. One test is trying to explain the type in natural language. `type="clip" subtype="news"` passes the test that "This is a clip, a news clip specifically." Another test is considering the client UI. A client should be functional if it ignores the subtype, and optimized if it respects it. If `type="track" subtype="podcast"`, a client can successfully play the podcast in an audio player based purely on the type, but it may tweak the display or which advanced playback controls are visible based on the subtype.

### List of Metadata Subtypes

- `podcast`
- `webshow`
- `news`
- `photo`

#### Collection Subtypes

- `movie`
- `show`
- `artist`
- `album`

#### Extras Subtypes

- `trailer`
- `deletedScene`
- `interview`
- `musicVideo`
- `behindTheScenes`
- `sceneOrSample`
- `liveMusicVideo`
- `lyricMusicVideo`
- `concert`
- `featurette`
- `short`
- `other`

## Sources

Source URIs and attributes make it possible to uniquely reference content outside the local server context without requiring a fixed url. This might be desirable when showing related albums from a friend's shared media server, building a universal play queue, or returning aggregated hubs that span multiple providers. Source components are immutable and act as pointers to a single item or directory in the Plex ecosystem.

A source URI from a media server uses the `server` scheme while a cloud provider uses the `provider` scheme.

```
server://{SERVER_ID}/{PROVIDER_ID}/{PATH}
provider://{PROVIDER_ID}/{PATH}
```

As a single regular expression, that's:

```
/^(server|provider):\/\/([a-fA-F0-9-]+)?\/?([^/]+)([^\?]+)\??(.*)?/
```

The server id is the server's `machineIdentifier`. The provider id is the provider's `identifier`. The rest of the path represents the path of the content at the provider and may include additional query parameters like `X-Plex-` headers or media query syntax for sorts and filters.

Some examples may be helpful:

```
server://546684a3d18ac5c39037360ec9ce900b7af9cc36/com.plexapp.plugins.library/library/metadata/2814936
provider://tv.plex.provider.podcasts/library/sections/audio/all
```

The `source` attribute has the same structure as the source URI, but omits the path.

```
{SOURCE_TYPE}://{SOURCE_ID}/{PROVIDER_ID?}
```
```
/^(server|provider):\/\/([a-fA-F0-9-]+)?\/?([^/]+)$/
```

```
source="server://546684a3d18ac5c39037360ec9ce900b7af9cc36/com.plexapp.plugins.library"
source="provider://tv.plex.provider.podcasts"
```

Source attributes can be used as a base and combined with `key` or other root-relative path components to construct unique source URIs.

## Pagination

Many endpoints that return a list of items support pagination.  Additionally some endpoints will force pagination and limit number of elements returned if the client attempts to request all items. To request a specific subset of data, add two headers to specify the starting offset and the number of desired items.

- **X-Plex-Container-Start** - The desired starting offset
- **X-Plex-Container-Size** - The desired number of items

Both headers should be sent in order to request paginated content. Note that it's possible to request a size of 0 on supported endpoints in order to learn the total size without actually getting any content.

The response **must** be checked to see if the response is in fact paginated. The response might not be paginated at all, or it might include a different number of items than what was requested. A paginated response will include the headers:

- **X-Plex-Container-Start** - The offset of the first returned item
- **X-Plex-Container-Total-Size** - The **total** size of the collection (optional but typically present)

The response body will also typically include pagination info. If the response is a `MediaContainer`, then it will have `offset` and `size` attributes representing the start index and the number of items in the current response along with an optional `totalSize` attribute for the total number of elements in the collection.

```
HTTP/1.1 200 OK
X-Plex-Container-Start: 2
X-Plex-Container-Total-Size: 5
Content-Type: application/xml

{
  "MediaContainer": {
    "size": 3,
    "totalSize": 5,
    "offset": 2,
    "Metadata" : [
      …
    ]
  }
}
```

Rather than requesting a page starting at an index, it is also possible in some lists to request a page centered on a specific item in the list.

- **X-Plex-Container-Focus-Key** - The key of an item to center on
- **X-Plex-Container-Size** - The desired number of items

The requested size is respected regardless of the position of the focus item in the list. If the item is at the start of the list and 10 items are requested, 9 items in the response will be after the item. If the item is in the middle of the list and 10 items are requested, 4 items will be before the item and 5 items will be after.

Endpoints that support rich media queries also have a `limit` parameter that interacts with pagination. Sending `limit` in a query string limits the desired number of items, much like the `X-Plex-Container-Size` header. There are two major differences:

1. When using `limit`, the total size of the collection is not returned. The minimum of the limit and the actual total size will be returned as the total size.
2. The request may be more efficient when using `limit`, since the total size doesn't have to be known.

If the total size of the collection isn't needed, use `limit`, since the request may be more efficient.

Note that `limit` and `X-Plex-Container-Size` aren't mutually exclusive. You can page within the results that are bounded by the limit. If you want a total of 1000 items from a collection of many thousands of items, but you want to page through them 20 at a time, you'd use `limit=1000&X-Plex-Container-Size=20&X-Plex-Container-Start=0`.

## API Versioning

PMS has never used API versioning before the creation of this document.  The first published API is considered `1.0` with the API prior to publication considered `0.0`.  A client species its version via the `X-Plex-Pms-Api-Version` header on requests.  If no header is provided, the version `0.0` is assumed.

### API Changes
 - 1.0.0 (Supported in PMS >= 1.41.9)
  - Added `/downloadQueue` endpoints.
  - Public release of API.
  - The `includeFields` parameter has been renamed to `includeOptionalFields`.  The `includeFields` parameter now means "include only these fields" where in the past it meant "please add these fields you wouldn't normally include."  This was changed to be consistent with the cloud provider API.


- 1.1.0 (Supported in PMS >= 1.42.0)
  - Added ability to filter '/media/providers/metadata' endpoint by metadata types (PM-3702)
  - Changed `types` in `/playlists/{playlistId}/items` to array of integers.
  - Document the `/photo/:/transcode` endpoints
  - Fixed serialization of MetadataType objects for '/media/providers/metadata' calls.


- 1.1.1 (Supported in PMS >= 1.42.2)
  - Added 'metadataAgentProviderGroupId' query param to create and edit library section (PM-3577)
  - Fixed Add library section method type.


- 1.2.0 (Supported in PMS >= 1.43.0)
  - Added 'squareArt' as additional element type for image assets (PM-2959)
  - Added `/media/providers/metadata` endpoints (PM-1012)
  - Added delete method for /library/metadata/{id}/{element} (PM-4094)
  - Added documentation for Metadata-type Media Providers (PM-3051)


- 1.2.1 (Supported in PMS >= 1.43.1)
  - Added `/tv.plex.providers.epg.{identifier}:{deviceId}` endpoints (PM-4017)
  - Added new state to itemsGeneratorItems endpoint (PM-3475)


- 1.2.2 (Supported in PMS >= 1.43.2)
  - Added `audioLayout` endpoint (PM-5118)
  - Added `videoCodec`, `audioCodec`, and `subtitleCodec` endpoints (PM-5117)

## Response Customization

Many endpoints allow the data that is included in the response to be tailored to exactly what the client wants. This is possible by either specifying things that should be excluded or the set of things that should be included.  PMS's ability to include/exclude elements and fields is currently limited but expanding so this should be used with care.

Attributes can be customized by using a query string arg of either `excludeFields` or `includeFields`. This single parameter should be a comma-separated list of attribute names. For example, a request with `excludeFields=summary,tagline` is asking for the summary and title attributes to be left off any metadata items while the `includeFields` parameter indicated that only the specified fields should be included.

Child elements can be customized by using a query string arg of either `excludeElements` or `includeElements`. This single parameter should be a comma-separated list of element names. For example, a request with `excludeElements=Media` is asking for the `Media` elements to be omitted while the `includeElements` parameter indicated that only the specified elements should be included.

In addition to the above are the parameters `includeOptionalFields` and `includeOptionalElements`.  These indicate that the fields/elements which are not normally included should be included in this request.  One example is `includeOptionalElements=musicAnalysis` on metadata will include the `musicAnalysis` parameter which can be large and typically not needed by a client.

Trimming the response to only include what a client will actually use can result in much better performance, especially in large collections.  Increasingly these are being used to select which data is fetched from the database.  So if a client knows it will only ever use a few parameters from a request, it should specify those with `includeFields`.

Note that these inclusions/exclusions are treated as requests, not guarantees. Some endpoints will disregard them completely, and others may ignore them for specific items and insist on returning data that the client didn't necessarily ask for.

## Media Providers

Media providers are general purpose entities which supply media to Plex clients. Their API describes the Plex Media Server API, via a set of features on the "root" endpoint of the provider. Media provider can be hosted by a media server or in the cloud, linked to a specific Plex account. This section explains media providers generally, and then provides the specific server-hosted APIs around media providers.

### Client Guide to Media Providers

The philosophy behind media providers in general is to allow a common API between cloud servers and PMS, since the APIs are nearly identical to a normal PMS. The general guidelines are:
- Consume `/media/providers` instead of `/library/sections`

  The new providers endpoint give you a list of all providers exported by a server and their features. Remember that the library itself is considered a (very rich) provider! This change will also require changing the client to not hardwire paths on the server, but rather read them from the feature keys directly (e.g. scrobble and rating endpoints).

- Gate management functionality on the `manage` feature

  Server libraries allow management (e.g. media deletion). The correct way to gate this functionality is via the manage feature.

- Make sure key construction is correct for things like genre lists

  For example, `/library/sections/x/genre` returns a relative key for each genre, but there's nothing which says that the `key` can't be an absolute URL. This is why servers pass back `fastKey` separately so as to not break clients which don't do key construction correctly. Media providers do not pass back `fastKey`, but assume clients will be doing correct key construction.

- Don't call `/library/sections/X/filters|sorts`

  You can get all that information (and more) in a single call by hitting `/library/sections/X?includeDetails=1`. Media providers include the extra information by default.

- Respect the Type keys in `/library/sections/x`

  The top-level type pivots have their own keys, which should be used over the old "just append `/all` to the path and add the type" approach. Not only is this more flexible, it also allows for "virtual" pivots, like music videos inside a music library.

- Look for the `skipChildren`/`skipParent` attributes for shows

  Because of things like Podcasts, single-season shows can now be made to skip seasons. This is indicated by a `skipChildren` attribute on the show, or a `skipParent` attribute on an episode. If this is set on a show, the client should use `/grandchildren` instead of `/children` in the show's key.

### Features

The list of supported features, along with the API endpoints each feature represents is shown in the following list. Note that each feature can define a custom endpoint URL, so it doesn't have to match the server API exactly.

- **search**: This feature implies that it supports search via the provided key.

- **metadata**: This feature implies that it supports metadata endpoint.  For example, if the `key` were `/library/metadata` then the endpoints `/library/metadata/X`, `/library/metadata/X/children` and `/library/metadata/X/grandchildren` would be supported. This endpoint family allows browsing a hierarchical tree of media (e.g. show to episodes, or artist to tracks).

- **content**: This feature implies that the provider exposes a content catalog, in the form of libraries to browse (grid of content), or discover (via hubs). Each entry in the content feature can contain:

  - `hubKey`: This implies it supports a discovery endpoint with hubs.
  - `key`: This implies it supports a content catalog.
  - `icon`: Optional, specifies the icon used for a content directory.

  Each content feature can contain one or both of these keys, depending on the structure. More details on the various combinations are provided below.

- **match**: The match feature is used to match a piece of media to the provider's content catalog via a set of hints. As a specific example, you might pass in a title hint of "Attack of the 50 Foot Woman" and a year hint of 1958 for the movie type. The provider would then use all the hints to attempt to match to entries in its catalog.

- **manage**: The manage feature implies a whole host of endpoints around _changing_ data inside a library (e.g. editing fields, customizing artwork, etc.). This feature is generally only available on an actual server and generally only to the admin.

- **timeline**: The timeline feature implies that the provider wants to receive timeline (playback notifications) requests from a client at the endpoint defined by `key`. The feature may additionally specify the `scrobbleKey` and `unscrobbleKey` attributes, which represent the endpoints which allow marking a piece of media played or unplayed.

- **rate**: This feature implies the provider supports the endpoint which allows rating content.

- **playqueue**: This feature implies the provider supports the play queue family of endpoints. The `flavor` attribute further specifies the subset; the only supported flavor is currently `full`.

- **playlist**: This feature implies the provider supports the playlist family of endpoints. If `readonly` is set, that means that the provider only allows listing and playing playlists (via play queue API), not actually creating or editing them.

- **subscribe**: This provider allows media subscriptions to be created.  If the flavor is `record` then media can be recorded from this library (such as DVR).  If the flavor is `download` then the user is allowed to download from this library.

- **promoted**: This feature allows the provider to supply an endpoint that will return a collection of "promoted" hubs that many clients show on a user's home screen.

- **continuewatching**: This feature allows the provider to supply an endpoint that will return a hub for merging into a global Continue Watching hub.

- **collection**: This feature implies the provider supports the collection family of endpoints.

- **actions**
  - **removeFromContinueWatching** - Action to remove an item from continue watching

- **imagetranscoder** - This feature implies the provider supports the image transcoder endpoints used to scale images for clients where memory and processor is at a premium

- **queryParser** - This feature implies the provider supports the media queries language below

- **grid** - This feature implies the provider supports displaying metadata in a grid over time (such as live TV)

##### Home discovery and browsable libraries

Shown in the example in [/media/providers](#tag/Provider/operation/getMediaProviders), in this media provider the first content directory is an item with only `hubKey`, meaning it only providers discovery hubs. This is the set of hubs covering the whole library which contains continue watching, recently added, recommendations, etc. It's essentially "landing page" for the provider.

The subsequent directories also have a browse `key`, which means they provide a list view of the content with options for filtering and sorting.  EPG providers may have only the `key` and no `hubKey`.

##### Minimal provider

There's no requirement to provide the content feature, given that there are two other ways to access content within a provider: search and match. The former can contribute to global search, whereas the latter is used for things like the DVR engine; once media subscriptions are set up, they look for matching content using the match feature, and examined using the metadata feature.

##### Deeper Hierarchies

If you examine an app like Spotify, you'll see many of the concepts here apply to their content hierarchy. Their content screens are either grids or hubs. But one notable difference is that the content hierarchy runs a bit deeper than the examples we've examined thus far. For example, one of the top-level selections is "Genres & Moods". Diving into one of the genres leads to a discovery area with different hubs for popular playlists, artists, and albums from the genre. Selecting a mood leads to a grid with popular playlists for the mood. In order to support this sort of hierarchy, we need an extension to the regular library, which is a *content directory*. This allows us to nest content, without losing any of the power and features—for example, the grid with popular playlists could list filters and sorts specific for that grid. This is power you simply don't have with the old channel architecture.

##### Extensions to regular libraries

This section examines extensions to plain libraries which content providers can use, and which clients need to be aware of.

- **Nested content directories**: In regular libraries, there are fixed types of directories (e.g. shows, or music albums). In content providers, we want to have the ability to display other types of things (e.g. stations, or moods, or genres) as first-class things in a grid or discovery layout. Here's an example of what a nested content directory looks like. Given the `type` of content, the client knows that this directory should be treated like a content directory feature entry.

  ```json
  {
    "Directory":[
      {
        "key":"foo",
        "hubKey":"foo2",
        "type":"content",
        "aspectRatio":"1:1",
        "title":"Genres and Moods"
      }
    ]
  }
  ```

- **Aspect ratio hint**: Because the entities listed in content directories can be arbitrary, it's important to tell the client some information about how they should be displayed. The `thumb` attribute contains no information about aspect ratio, so clients make assumptions based upon known types (e.g. movies are 2:3, episode thumbs are 16:9, etc.). This attributes allows the provider to specify exactly the aspect ratio of the thing being displayed.

## Metadata Providers

This section describes the specific Media Providers which supply the `metadata` feature. These providers can be created and used in Plex Media Server to supply metadata to items inside Movie and TV Show libraries (music libraries are currently not supported).

### Common Request Headers

There are a few headers which are common to both the Metadata and Match features. These can be passed as either headers or query parameters.

| Header | Support Required? | Description |
|--------|-------------------|-------------|
| X-Plex-Language | No | IETF language tag including the region subtag (e.g. 'en-US', 'de-DE'). Used for localization.
| X-Plex-Country | No | ISO 3166 two-letter country code. Used primarily to define the country for certification data, or can be used to determine release dates for the specific country.
| X-Plex-Container-Size | Yes | For paged requests. This determines what the maximum container size should be of a single response.
| X-Plex-Container-Start | Yes | For paged requests. This determines the starting index for the paged request.

### Response Paging

Certain responses may contain a large number of objects. The consumer may want to limit the size of the MediaContainer by paging through them using the `X-Plex-Container-Size` and `X-Plex-Container-Start` headers/params. Responses should them limit the object count inside the MediaContainer to `X-Plex-Container-Size` and start at the index provided by `X-Plex-Container-Start`.

See the [Pagination](#pagination) section for more details on how paging works.

The only two endpoints that require mandatory paging are the Metadata `/children` and `/grandchildren` endpoints as these will potentially contain many items. Passing no paging headers here should only return the first 20 Metadata objects.

### Common return codes

It is important to return the correct HTTP return codes.

| Code | Common Name | Description |
|------|-------------|-------------|
| 200 | OK | An response for an item or match is successfully returned |
| 404 | Not Found | If an item with the requested ratingKey is not found (Metadata feature only) |
| 400 | Bad Request | A request was made which cannot be fulfilled because the request is malformed |
| 500 | Internal Server Error | A request was made which cannot be fulfilled because the server encountered an internal error |

### Response Customization (Optional)

There may be cases where a reduced response is wanted, i.e. we only want to return specific attributes or exclude specific attributes. These are handled with `includeFields`, `excludeFields`, `includeElements` and `excludeElements`.

Information on its use can be found in the [Response Customization](#response-customization).

You may wish to add support for this to keep response sizes down, however it is not required and you can safely ignore when these parameters are passed.

### Metadata Feature

This is a path to retrieve metadata for a specific piece of content by its id.

It is called by making a `GET` request to the path defined by the `Metadata` feature inside the root of your provider with the `ratingKey` of the metadata item.

For example, the request may be something like `GET http://localhost/library/metadata/tmdb-movie-123` which should return a [Metadata Object](#metadata-object) for the item with the `ratingKey` of "tmdb-movie-123".

See some [Example Responses](#example-responses)

#### Supported Query Parameters

There are some query parameters available to media provider to augment the responses. Not all of these are required to be supported by all providers, support requirement is detailed in the below table.

| Param | Type | Support Required? | Description |
|-------|------|-------------------|-------------|
| `includeChildren` | integer (1/0) | Yes (TV Shows/Seasons only) | Returns a [Children Object](#children-object) when the metadata type has direct child objects (e.g. a TV Show should return Season Children)
| `episodeOrder` | string | No | When making a request that returns seasons in the response, pass back the appropriate season items for the requested [SeasonType id](#seasontype-array-optional). It is expected that if no seasons exist for the requested episodeOrder, that no season data should be returned.

#### Image endpoint (Recommended)

The Metadata feature should also provide a `/images` path for calls to specific items, e.g. `/library/metadata/tmdb-movie-123/images`. This endpoint should return a [MediaContainer](#mediacontainer) object containing and [Image Array](#image-array-highly-recommended) of all the available image assets for that item.

Example:

```json
{
  "MediaContainer": {
    "offset": 0,
    "totalSize": 3,
    "identifier": "tv.plex.provider.metadata",
    "size": 3,
    "Image": [
      {
        "type": "coverPoster",
        "url": "https://image.tmdb.org/t/p/original/qk3eQ8jW4opJ48gFWYUXWaMT4l.jpg",
      },
      {
        "type": "background",
        "url": "https://image.tmdb.org/t/p/original/3uE9SUywNbj1qSAuYCGgbTTYku5.jpg",
      },
      {
        "type": "clearLogo",
        "url": "https://image.tmdb.org/t/p/original/rIi0lY2UftYuKDJ4OlIefDdijve.png",
      }
    ]
  }
}
```

### Children and Grandchildren Requests

For items which contain child items, like TV Shows and Seasons, these types should also respond to requests for `/children` and `/grandchildren`, e.g. `/library/metadata/tmdb-show-123/children`.

For TV Shows and Seasons this should return a [MediaContainer](#mediacontainer) object with an array of [Metadata Objects](#metadata-object) for their Seasons and Episodes respectively.

It is required that these two endpoints support paged requests via the `X-Plex-Container-Size` and `X-Plex-Container-Start` headers/params.

### Match Feature

This is a path to retrieve potential matches to metadata items based on contextual hints passed in your request body. This should return a [MediaContainer Object](#mediacontainer) possibly containing multiple Metadata objects (by default should only return the best result only).

It is called by making a `POST` request to the path defined by the `Match` feature inside the root of your provider.

This may be where it is useful supporting [Response Customization](#response-customization-optional) as match responses don't always need to contain the full Metadata object responses.

A request body is required which can contain the attributes listed below.

| Attribute | Type | Support Required? | Optional | Description |
|-----------|------|-------------------|----------|-------------|
| `type` | integer | Yes | No | The numeric metadata type for the requested match. See [Metadata Types Table](#metadata-types-table) |
| `title` | string | Yes | No* | A title for the item. *Movies and TV Shows only. |
| `parentTitle` | string | Yes | No* | A title for the TV Show. *Seasons only. |
| `grandparentTitle` | string | Yes | No* | A title for the TV Show. *Episodes only. |
| `includeChildren` | integer (1/0) | Yes (TV Shows/Seasons only) | Yes* | Returns a [Children Object](#children-object) when the metadata type has direct child objects (e.g. a TV Show should return Season Children). *Is only optional for Movie and Episode types.
| `episodeOrder` | string | No | Yes | When making a request that returns seasons in the response, pass back the appropriate season items for the requested [SeasonType id](#seasontype-array-optional). It is expected that if no seasons exist for the requested episodeOrder, that no season data should be returned. |
| `year` | integer | Yes | Yes | The release year for the requested match. |
| `guid` | string | Yes | Yes | An external id which can help matching precisely (e.g. `tvdb://12345) |
| `index` | integer | Yes | Yes* | For Seasons, the season number. For Episodes, the episode number. |
| `parentIndex` | integer | Yes | Yes* | For Episodes, the season number. |
| `filename` | string | No | Yes | The relative path for the underlying media file. For TV Shows and Seasons this will return the first file found. e.g. `/Movies/Back to the Future (1985).mp4` |
| `date` | string | Yes | Yes* | When matching an TV Episode, if `index` and `parentIndex` are not available, a date must be passed representing the air date of the episode.
| `manual` | integer (1/0) | Yes | Yes | When a value of `1` is passed, the response should contain an array of the best matches for the request ordered by highest to lowest confidence. When this value is not passed or is `0`, only the best match should be returned. |
| `includeAdult` | integer (1/0) | No | Yes | If your provider supports explicit/adult content this value should be taken into consideration when returning responses and any explicit results should be filtered out unless a value of `1` is passed. |

#### Match Example

##### JSON Body

```json
{
  "parentTitle": "Adventure Time",
  "type": 3,
  "index": 8,
  "filename": "TV Shows/Adventure Time/Adventure Time S08E01.mp4",
  "includeElements": "Metadata,Children",
  "includeFields": "guid,parentGuid,title,parentTitle,thumb,parentThumb,index,originallyAvailableAt,year,type",
  "includeChildren": 1
}
```

##### CURL Command

```
curl  -X POST \
  'http://localhost/library/metadata/matches?X-Plex-Country=US&X-Plex-Language=en-US' \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "parentTitle": "Adventure Time",
  "type": 3,
  "index": 8,
  "filename": "TV Shows/Adventure Time/Adventure Time S08E01.mp4",
  "includeElements": "Metadata,Children",
  "includeFields": "guid,parentGuid,title,parentTitle,thumb,parentThumb,index,originallyAvailableAt,year,type",
  "includeChildren": 1
}'
```

##### Response

```json
{
  "MediaContainer": {
    "offset": 0,
    "totalSize": 1,
    "identifier": "tv.plex.provider.metadata",
    "size": 1,
    "Metadata": [
      {
        "guid": "plex://season/5d9c0939e9d5a1001f4def89",
        "type": "season",
        "thumb": "https://image.tmdb.org/t/p/original/zIDoU6YZXE3oz9MNBjE2Ld94Xuu.jpg",
        "title": "Season 8",
        "parentTitle": "Adventure Time",
        "parentThumb": "https://image.tmdb.org/t/p/original/qk3eQ8jW4opJ48gFWYUXWaMT4l.jpg",
        "parentGuid": "plex://show/5d9c07f72df347001e3a70b4",
        "index": 8,
        "originallyAvailableAt": "2016-03-26",
        "year": 2016,
        "Children": {
          "size": 2,
          "Metadata": [
            {
              "guid": "plex://episode/5eeb4fc1d39938003f7753c0",
              "type": "episode",
              "thumb": "https://image.tmdb.org/t/p/original/3WXclCno2MYKhdnUidQVsPSpolk.jpg",
              "title": "Broke His Crown",
              "parentTitle": "Season 8",
              "parentThumb": "https://image.tmdb.org/t/p/original/zIDoU6YZXE3oz9MNBjE2Ld94Xuu.jpg",
              "parentGuid": "plex://season/5d9c0939e9d5a1001f4def89",
              "index": 1,
              "originallyAvailableAt": "2016-03-26",
              "year": 2016
            },
            {
              "guid": "plex://episode/5eeb4fc1d39938003f7753be",
              "type": "episode",
              "thumb": "https://image.tmdb.org/t/p/original/mhhq4BXNmnZZfzfqsBvZwMvcngt.jpg",
              "title": "Don't Look",
              "parentTitle": "Season 8",
              "parentThumb": "https://image.tmdb.org/t/p/original/zIDoU6YZXE3oz9MNBjE2Ld94Xuu.jpg",
              "parentGuid": "plex://season/5d9c0939e9d5a1001f4def89",
              "index": 2,
              "originallyAvailableAt": "2016-04-02",
              "year": 2016
            }
          ]
        }
      }
    ]
  }
}
```

## MediaProvider Response

This document describes the JSON response schema for Plex-compatible metadata-specific Media Providers.

The root of the Media Provider must return some necessary attributes which define a metadata provider.

### MediaProvider

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `identifier` | string | Yes | Unique identifier for this media provider |
| `title` | string | Yes | A human readable title for the media provider |
| `version` | string | No | The version of the API being called |
| `Feature` | array | Yes | Array containing the features provided by the media provider |

### `Types` Array (Required)

This defines what metadata types are supported by the provider.

Please note that is recommended to support one specific metadata parent type per provider as this will make it easier for consumers to combine this provider with others inside Plex Media Server. This is because in order to combine providers, each provider in a combine group must support the types the other supports as well. Limiting the scope of types will make it more widely compatible.

If you wish to support both movie and TV Shows, consider creating two separate providers. This isn't a hard requirement but is recommended.

When supporting TV Shows, it is necessary to add a type for TV Shows, Seasons and Episodes (i.e. types 2, 3 and 4).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | integer | Yes | The metadata type represented by its numeric value (see mapping table below) |
| `Scheme` | array | Yes | Array defining the GUID-scheme (the prefix) for items returned by this provider  |

### `Scheme` Array (Required)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `scheme` | string | Yes | The GUID-scheme. Should be identical to the provider identifier. |

#### Metadata Types Table

Custom metadata provider currently support a subset of the full metadata types outline in the [Metadata Types](#metadata-types) section.

| Type Name | Type Number |
|-----------|-------------|
| `movie` | 1 |
| `show` | 2 |
| `season` | 3 |
| `episode` | 4 |

### `Feature` Array (Required)

A feature, as its name implies, defines a feature available to the specific provider.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Feature type (see feature table below) |
| `key` | string | Yes | API endpoint path to call this feature |

#### Available Features

| Type | Required | Description |
|------|----------|-------------|
| metadata | Yes | Path to retrieve metadata for a specific piece of content by its id. See Metadata Feature section. |
| match | Yes | Path to return a potential match for a specific piece of content using contextual hints. See Match Feature section. |

### Example Response

```json
{
  "MediaProvider": {
    "identifier": "tv.plex.agents.custom.johnz.tmdb",
    "title": "John Z's TV Show Provider",
    "version": "1.0.0",
    "Types": [
      {
        "type": 2,
        "Scheme": [
          {
            "scheme": "tv.plex.agents.custom.johnz.tmdb"
          }
        ]
      },
      {
        "type": 3,
        "Scheme": [
          {
            "scheme": "tv.plex.agents.custom.johnz.tmdb"
          }
        ]
      },
      {
        "type": 4,
        "Scheme": [
          {
            "scheme": "tv.plex.agents.custom.johnz.tmdb"
          }
        ]
      }
    ],
    "Feature": [
      {
        "type": "metadata",
        "key": "/library/metadata"
      },
      {
        "type": "match",
        "key": "/library/metadata/matches"
      }
    ]
  }
}
```

### Defining an identifier

Custom metadata providers need to provide an identifier using a scheme with the `tv.plex.agents.custom.` prefix. A custom provider can choose its own scheme as long as it is prefixed with this value, for example a provider for a custom TheMovieDB implementation might use a scheme like:

`tv.plex.agents.custom.johnz.tmdb`

It is important to note that you should try and keep the identifier unique as there is no guarantee that it will be the only provider added to a Plex user's server and could conflict with a another existing provider already in use. So avoid using very generic suffixes like `tmdb`, `tvdb`, etc.

The characters allowed for your suffix is very strict and can only contain ASCII letters, numbers and periods (`regex [a-zA-Z0-9.]`).

This identifier must be used as the scheme for the Metadata items the provider returns. See [GUID Construction](#guid-construction).

## Metadata Response

This section describes the JSON response schema for Plex-compatible metadata responses from Media Providers. This does not describe the Metadata response in its entirety only what is required for Media Provider responses.

The response consists of a `MediaContainer` object that wraps `Metadata` objects representing the movie, TV show, season or episode data.

The different metadata types may have specific attributes only returned by that type. e.g. Season and episode types will have some attributes specific to their parent like `parentTitle` which would not be serialized by a movie or TV show type.

### MediaContainer

The root object that contains metadata and pagination information.

| Field | Type | Description |
|-------|------|-------------|
| `offset` | integer | The starting position in the result set (always 0 for single items) |
| `totalSize` | integer | Total number of items in the response (always 1 for single items) |
| `identifier` | string | The provider identifier (e.g., "tv.plex.provider.metadata") |
| `size` | integer | Number of items in the current response (always 1 for single items) |
| `Metadata` | array | Array containing a single movie metadata object |

### Metadata Object

The main object containing all the item information.

#### Core Attributes (applicable to all metadata types)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ratingKey` | string | Yes | Unique identifier for this metadata item in Plex |
| `key` | string | Yes | API endpoint path to retrieve this metadata |
| `guid` | string | Yes | Global unique identifier in Plex-compatible format. See the 'Guid construction' section. |
| `type` | string | Yes | Content type (`movie`, `show`, `season` or `episode`) |
| `title` | string | Yes | The metadata title, e.g. "Back to the Future" |
| `originallyAvailableAt` | string | Yes | Original release date in ISO 8601 format (YYYY-MM-DD) |
| `thumb` | string | No | A publicly accessible URL to the default poster/thumbnail for the item |
| `art` | string | No | A publicly accessible URL to the default background artwork for the item |
| `contentRating` | string | No | Age rating/certification (e.g., "PG", "R", "PG-13"). For non-US ratings please prepend 2-letter country code followed by a forward slash (e.g. za/15) |
| `originalTitle` | string | No | If the request is made for language that is different to the original language of the release, return the title in its original language. |
| `titleSort` | string | No | Returned if the content should be sorted by a different value, e.g. "Quiet Place, A". This will be added automatically by the media server, so its inclusion is only necessary if you require a specific sorting value which the media server does not accommodate. |
| `year` | integer | No | Release year |
| `summary` | string | No | Full plot synopsis |
| `isAdult` | bool | No | Return `true` for explicit/adult content. |

#### Movie, TV Show and Episode Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `duration` | integer | No | Runtime in milliseconds |

#### Movie and TV Show Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tagline` | string | No | Movie tagline or promotional text |
| `studio` | string | No | Primary production studio |
| `theme` | string | No | A publicly accessible URL to an audio snippet of the item's theme music (MP3 only, preferably keep max length to around 30 seconds) |

#### Season and Episode Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `parentRatingKey` | string | Yes | Unique identifier for parent (the TV show for a season and the season for an episode) metadata item in Plex |
| `parentKey` | string | Yes | API endpoint path to retrieve the parent metadata |
| `parentGuid` | string | Yes | Global unique identifier in Plex-compatible format for the parent. See the 'Guid construction' section. |
| `parentType` | string | Yes | the content type of the parent (i.e. `show` for a season, `season` for an episode) |
| `parentTitle` | string | Yes | The metadata title of the parent. |
| `parentThumb` | string | No | A publicly accessible URL to the default poster/thubnail for the parent |
| `index` | integer | Yes | The item index. For a season this is the season number, for an episode it's the episode number |

#### Episode Attributes

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `grandparentRatingKey` | string | Yes | Unique identifier for grandparent (the TV Show item) metadata item in Plex |
| `grandparentKey` | string | Yes | API endpoint path to retrieve the grandparent metadata |
| `grandparentGuid` | string | Yes | Global unique identifier in Plex-compatible format for the grandparent. See the 'Guid construction' section. |
| `grandparentType` | string | Yes | `show` - the content type of the grandparent |
| `grandparentTitle` | string | Yes | The metadata title of the grandparent e.g. `Adventure Time` |
| `grandparentThumb` | string | No | A publicly accessible URL to the default poster/thubnail for the grandparent |
| `parentIndex` | integer | Yes | The season index, e.g. `8` |

#### `Image` Array (Highly Recommended)

Array of all available image assets in various dimensions.

Not all types are required but it is recommended to supply at least "coverPoster" (or "snapshot" for episode items) and "background". "clearLogo" and "backgroundSquare" are also utilized inside Plex client applications for movies and TV shows and should be supplied to provide the best experience for these types.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Image type: "background", "backgroundSquare", "clearLogo", "coverPoster", "snapshot" |
| `url` | string | Yes | Full URL to the image asset |
| `alt` | string | No | Alt text for accessibility (typically movie title) |

#### `OriginalImage` Array (Recommended)

The same attributes as `Image` but provides images in the original language of the content if the requested language doesn't match the original language.

#### `Genre` Array (Recommended)

Array of genres associated with the content.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | string | Yes | Display name of the genre (e.g. "Action") |
| `originalTag` | string | No | Original language of genre name if request is made in a language different from the original |

#### `Guid` Array (Optional)

Array of external identifier mappings. This is very useful to provide exact mappings to other metadata providers which can improve matching accuracy and speed when combining multiple metadata providers.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | External ID in format "provider://id" (e.g., "imdb://tt0088763", "tmdb://105") |

Internally supported providers include:
- `imdb` - IMDb
- `tmdb` - TheMovieDB
- `tvdb` - TVDB

#### `Country` Array (Optional)

Array of production countries.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | string | Yes | Full country name |

#### People

There are common attributes among `Role`, `Producer`, `Director` and `Writer` arrays.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | string | Yes | Person's full name |
| `thumb` | string | No | URL to person's photo |
| `role` | string | No | Character name or role description |
| `order` | integer | No | Display order in cast list |

#### `Role` Array (Recommended)

Array of cast members and their characters.

See "People" section for attributes.

#### `Director` Array (Recommended)

Array of directors.

See "People" section for attributes.

#### `Producer` Array (Recommended)

Array of producers.

See "People" section for attributes.

#### `Writer` Array (Recommended)

Array of writers/screenwriters.

See "People" section for attributes.

#### `Similar` Array (Optional)

Array of similar titles.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `guid` | string | Yes | GUID for the similar movie |
| `tag` | string | No | Title of the similar movie |

#### `Studio` Array (Optional)

Array of production studios and companies.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | string | Yes | Studio/company name |

#### `Rating` Array (Optional)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | string | Yes | Image identifier for critic rating badge (see supported identifiers below) |
| `type` | string | Yes | `audience` or `critic` - always `audience` for user-generated ratings |
| `value` | float | Yes | The rating represented by a floating point value between 0 and 10 |

#### Rating image identifiers

These are built-in mappings to display the appropriate badge inside the Plex client. Adding new types is not currently supported.

| Identifier | Source |
|------------|--------|
| `imdb://image.rating` | IMDb ratings |
| `themoviedb://image.rating` | TheMovieDb ratings |
| `rottentomatoes://image.rating.ripe` | Rotten Tomatoes for critic ratings |
| `rottentomatoes://image.rating.upright` | Rotten Tomatoes for audience ratings |

#### `Network` Array (Optional)

TV Shows only.

Array of television networks that the TV Show originally aired on.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag` | string | Yes | Network name |

#### `SeasonType` Array (Optional)

TV Shows only.

The provider must support the `episodeOrdering` query parameter to use this.

Array of available episode orderings for a specific TV Show e.g. ("DVD Order", "Airing Order", etc.).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier for the SeasonType, used as query parameter when making requests for TV Shows. ASCII characters only (e.g. "blurayOrder") |
| `source` | string | Yes | The source of the data, e.g. "tmdb" |
| `tag` | string | Yes | A human readable descriptor for the SeasonType, e.g. "Bluray" or "Airing" |
| `title` | string | Yes | A full description for the SeasonType as shown in the Plex UI (e.g. "TheMovieDB (Netflix Order)") |

#### `Children` Object

This is required to be supported for TV Shows and Seasons and should only be returned when a request with `includeChildren=1` is passed.

This is a simplified `MediaContainer` object inside a `Metadata` object which provides an array of child items for the parent object (i.e. when requesting a TV Show, `Children` will contain the list of Seasons of that TV Show).

Note: it is expected that all the child objects be returned in this array. In some edge cases this may result in very large arrays. Please see fit to ensure your provider can handle this and simplify the child objects with only the required attributes if necessary.

| Field | Type | Description |
|-------|------|-------------|
| `size` | integer | Number of items in the `Metadata` array |
| `Metadata` | array | Array containing all child `Metadata` objects |

### GUID construction

Plex-compatible GUIDs are constructed out of the following components:

`{scheme}://{metadataType}/{ratingKey}`

For an item from the Plex metadata provider this will look something like this:

`plex://movie/5d7768244de0ee001fcc7fed`

#### `Scheme` component

Custom metadata providers need to provide a GUID in this same format using a scheme with the `tv.plex.agents.custom.` prefix. The scheme should match the metadata provider's `identifier` (see [Defining an identifier](#defining-an-identifier)), for example a provider for a custom TheMovieDB implementation might use a scheme like:

`tv.plex.agents.custom.johnz.tmdb`

#### `metadataType` component

This should just be the string representation of the metadata type being returned, i.e. `movie`, `show`, `season` or `episode`.

#### `ratingKey` component

This value should match the `ratingKey` attribute on the metadata item and is what is used when making a metadata request to the provider (e.g. `http://localhost/library/metadata/{ratingKey}`).

The `ratingKey` can constist of ASCII letters, numbers, dashes and underscores (`regex [a-zA-Z0-9_-]`).

#### Custom GUID examples

Some valid GUIDs could look like this:

- `tv.plex.agents.custom.johnz.tmdb://movie/tmdb-movie-19934`
- `tv.plex.agents.custom.barkley.tvdb://show/78874`
- `tv.plex.agents.custom.finn.imdb://movie/tt0379786`

### Example Responses

#### Movie Type
```json
{
  "MediaContainer": {
    "offset": 0,
    "totalSize": 1,
    "identifier": "tv.plex.provider.metadata",
    "size": 1,
    "Metadata": [
      {
        "art": "https://metadata-static.plex.tv/d/gracenote/dc6be8ceb098b8e14a708786ea071c6e.jpg",
        "guid": "plex://movie/5d7768244de0ee001fcc7fed",
        "key": "/library/metadata/5d7768244de0ee001fcc7fed",
        "ratingKey": "5d7768244de0ee001fcc7fed",
        "studio": "Universal Pictures",
        "summary": "Marty McFly, a typical American teenager of the Eighties, is accidentally sent back to 1955 in a plutonium-powered DeLorean \"time machine\" invented by a slightly mad scientist. During his often hysterical, always amazing trip back in time, Marty must make sure his teenage parents-to-be meet and fall in love to get back to the future.",
        "tagline": "He was never in time for his classes... He wasn't in time for his dinner... Then one day... he wasn't in his time at all.",
        "type": "movie",
        "thumb": "https://metadata-static.plex.tv/9/gracenote/9cf50a3c04a44ff7d53e1134222e3929.jpg",
        "duration": 6960000,
        "title": "Back to the Future",
        "contentRating": "PG",
        "originallyAvailableAt": "1985-07-03",
        "year": 1985,
        "Image": [
          {
            "alt": "Back to the Future",
            "type": "background",
            "url": "https://metadata-static.plex.tv/d/gracenote/dc6be8ceb098b8e14a708786ea071c6e.jpg"
          },
          {
            "alt": "Back to the Future",
            "type": "backgroundSquare",
            "url": "https://metadata-static.plex.tv/a/gracenote/ab63d5222db8e9b9c319b478f81bf1b6.jpg"
          },
          {
            "alt": "Back to the Future",
            "type": "clearLogo",
            "url": "https://metadata-static.plex.tv/f/683a142553/f44fe9b4a2cb1a6eb3eadbd22eb09add.png"
          },
          {
            "alt": "Back to the Future",
            "type": "coverPoster",
            "url": "https://metadata-static.plex.tv/9/gracenote/9cf50a3c04a44ff7d53e1134222e3929.jpg"
          }
        ],
        "Genre": [
          {
            "tag": "Adventure",
          },
          {
            "tag": "Comedy",
          },
          {
            "tag": "Science Fiction",
          }
        ],
        "Guid": [
          {
            "id": "imdb://tt0088763"
          },
          {
            "id": "tmdb://105"
          },
          {
            "id": "tvdb://299"
          }
        ],
        "Rating": [
          {
            "image": "imdb://image.rating",
            "type": "audience",
            "value": 8.5
          },
          {
            "image": "rottentomatoes://image.rating.ripe",
            "type": "critic",
            "value": 9.3
          },
          {
            "image": "rottentomatoes://image.rating.upright",
            "type": "audience",
            "value": 9.5
          },
          {
            "image": "themoviedb://image.rating",
            "type": "audience",
            "value": 8.321
          }
        ],
        "Country": [
          {
            "tag": "United States of America"
          }
        ],
        "Role": [
          {
            "order": 1,
            "tag": "Michael J. Fox",
            "thumb": "https://metadata-static.plex.tv/8/people/835031cfa837a2bee58d4c0c345f617b.jpg",
            "role": "Marty McFly"
          },
          {
            "order": 2,
            "tag": "Christopher Lloyd",
            "thumb": "https://metadata-static.plex.tv/2/people/21ab248996f621004036e057a1bad43e.jpg",
            "role": "Emmett Brown"
          },
          {
            "order": 3,
            "tag": "Crispin Glover",
            "thumb": "https://metadata-static.plex.tv/4/people/490bb62cd498add695195a06dd0ca87e.jpg",
            "role": "George McFly"
          },
          {
            "order": 4,
            "tag": "Lea Thompson",
            "thumb": "https://metadata-static.plex.tv/1/people/170afcdfe5b74c88f5ea5f74a31d107d.jpg",
            "role": "Lorraine Baines"
          }
        ],
        "Director": [
          {
            "tag": "Robert Zemeckis",
            "thumb": "https://metadata-static.plex.tv/b/people/b6a7e4d5e61c2c4613be3ece75dace8e.jpg",
            "role": "Director"
          }
        ],
        "Producer": [
          {
            "tag": "Neil Canton",
            "thumb": "https://metadata-static.plex.tv/4/people/481b0c2f5f012c3a532e2bf48fef1d80.jpg",
            "role": "Producer"
          },
          {
            "tag": "Bob Gale",
            "thumb": "https://metadata-static.plex.tv/people/5d7768244de0ee001fcc80b8.jpg",
            "role": "Producer"
          }
        ],
        "Writer": [
          {
            "tag": "Robert Zemeckis",
            "thumb": "https://metadata-static.plex.tv/b/people/b6a7e4d5e61c2c4613be3ece75dace8e.jpg",
            "role": "Writer"
          },
          {
            "tag": "Bob Gale",
            "thumb": "https://metadata-static.plex.tv/people/5d7768244de0ee001fcc80b8.jpg",
            "role": "Writer"
          }
        ],
        "Similar": [
          {
            "guid": "plex://movie/5d776d1023d5a3001f52001d",
            "tag": "Back to the Future Part II"
          },
          {
            "guid": "plex://movie/5d776d1723d5a3001f520400",
            "tag": "The Karate Kid"
          },
          {
            "guid": "plex://movie/5d776d10fb0d55001f596237",
            "tag": "Back to the Future Part III"
          },
          {
            "guid": "plex://movie/5d77682a6f4521001ea99e2c",
            "tag": "The Breakfast Club"
          }
        ],
        "Studio": [
          {
            "tag": "Universal Pictures"
          },
          {
            "tag": "Amblin Entertainment"
          }
        ]
      }
    ]
  }
}
```

#### Show Type

```json
{
  "MediaContainer": {
    "offset": 0,
    "totalSize": 1,
    "identifier": "tv.plex.provider.metadata",
    "size": 1,
    "Metadata": [
      {
        "art": "https://image.tmdb.org/t/p/original/3uE9SUywNbj1qSAuYCGgbTTYku5.jpg",
        "guid": "plex://show/5d9c07f72df347001e3a70b4",
        "key": "/library/metadata/5d9c07f72df347001e3a70b4/children",
        "ratingKey": "5d9c07f72df347001e3a70b4",
        "studio": "Frederator Studios",
        "summary": "Unlikely heroes Finn and Jake are buddies who traverse the mystical Land of Ooo. The best of friends, our heroes always find themselves in the middle of escapades. Finn and Jake depend on each other through thick and thin.",
        "type": "show",
        "theme": "https://tvthemes.plexapp.com/152831.mp3",
        "thumb": "https://image.tmdb.org/t/p/original/qk3eQ8jW4opJ48gFWYUXWaMT4l.jpg",
        "duration": 660000,
        "title": "Adventure Time",
        "contentRating": "TV-PG",
        "originallyAvailableAt": "2010-04-05",
        "year": 2010,
        "Image": [
          {
            "alt": "Adventure Time",
            "type": "background",
            "url": "https://image.tmdb.org/t/p/original/3uE9SUywNbj1qSAuYCGgbTTYku5.jpg"
          },
          {
            "alt": "Adventure Time",
            "type": "backgroundSquare",
            "url": "https://metadata-static.plex.tv/1/gracenote/1c09b028e1b15c0325917c51966a47d7.jpg"
          },
          {
            "alt": "Adventure Time",
            "type": "clearLogo",
            "url": "https://metadata-static.plex.tv/9/683a142553/9bf0c95f0dede66fce0e507fbfedc653.png"
          },
          {
            "alt": "Adventure Time",
            "type": "coverPoster",
            "url": "https://image.tmdb.org/t/p/original/qk3eQ8jW4opJ48gFWYUXWaMT4l.jpg"
          }
        ],
        "Genre": [
          {
            "tag": "Animation"
          },
          {
            "tag": "Comedy"
          },
          {
            "tag": "Action"
          },
          {
            "tag": "Adventure"
          },
          {
            "tag": "Family"
          },
          {
            "tag": "Fantasy"
          },
          {
            "tag": "Science Fiction"
          },
          {
            "tag": "Sci-Fi & Fantasy"
          },
          {
            "tag": "Children"
          }
        ],
        "Guid": [
          {
            "id": "imdb://tt1305826"
          },
          {
            "id": "tmdb://15260"
          },
          {
            "id": "tvdb://152831"
          }
        ],
        "Rating": [
          {
            "image": "imdb://image.rating",
            "type": "audience",
            "value": 8.6
          },
          {
            "image": "rottentomatoes://image.rating.ripe",
            "type": "critic",
            "value": 10
          },
          {
            "image": "rottentomatoes://image.rating.upright",
            "type": "audience",
            "value": 9.4
          },
          {
            "image": "themoviedb://image.rating",
            "type": "audience",
            "value": 8.504
          }
        ],
        "Country": [
          {
            "tag": "United States of America"
          }
        ],
        "Role": [
          {
            "order": 1,
            "tag": "Jeremy Shada",
            "thumb": "https://metadata-static.plex.tv/b/people/ba6413846e4fc49884ec7694d012b198.jpg",
            "role": "Finn the Human (voice)"
          },
          {
            "order": 2,
            "tag": "John DiMaggio",
            "thumb": "https://metadata-static.plex.tv/0/people/0a945543418d442fea7ae4948b2a2fda.jpg",
            "role": "Jake the Dog (voice)"
          },
          {
            "order": 3,
            "tag": "Tom Kenny",
            "thumb": "https://metadata-static.plex.tv/7/people/7a7654471f4b87c2f8ce757357e860b5.jpg",
            "role": "Ice King (voice)"
          },
          {
            "order": 4,
            "tag": "Hynden Walch",
            "thumb": "https://metadata-static.plex.tv/b/people/b2588be9b38393facd27de7fc4081720.jpg",
            "role": "Princess Bubblegum (voice)"
          },
          {
            "order": 5,
            "tag": "Olivia Olson",
            "thumb": "https://metadata-static.plex.tv/4/people/4eec0b6c6d36f6c4cd0574af354d74aa.jpg",
            "role": "Marceline the Vampire Queen (voice)"
          }
        ],
        "Director": [
          {
            "tag": "Larry Leichliter",
            "role": "Director"
          },
          {
            "tag": "Adam Muto",
            "thumb": "https://metadata-static.plex.tv/e/people/e385c2d25614f10d505701e5f590372a.jpg",
            "role": "Director"
          }
        ],
        "Producer": [
          {
            "tag": "Derek Drymon",
            "thumb": "https://metadata-static.plex.tv/c/people/cb057ffd3860076eb0f0c1fb55c8fef1.jpg",
            "role": "Producer"
          },
          {
            "tag": "Kelly Crews",
            "role": "Producer"
          }
        ],
        "Writer": [
          {
            "tag": "Tim McKeon",
            "role": "Writer"
          },
          {
            "tag": "Sean Jimenez",
            "role": "Writer"
          }
        ],
        "Network": [
          {
            "tag": "Cartoon Network"
          }
        ],
        "SeasonType": [
          {
            "id": "tmdbAiring",
            "source": "tmdb",
            "tag": "Aired",
            "title": "The Movie Database (Aired)"
          },
          {
            "id": "tvdbAiring",
            "source": "tvdb",
            "tag": "Aired",
            "title": "TheTVDB (Aired)"
          },
          {
            "id": "tvdbDvd",
            "source": "tvdb",
            "tag": "DVD",
            "title": "TheTVDB (DVD)"
          },
          {
            "id": "tvdbAbsolute",
            "source": "tvdb",
            "tag": "Absolute",
            "title": "TheTVDB (Absolute)"
          }
        ],
        "Similar": [
          {
            "guid": "plex://show/611cdc357032b6002cb92e97",
            "tag": "Adventure Time: Fionna & Cake"
          },
          {
            "guid": "plex://show/5d9c0875ba6eb9001fba4e43",
            "tag": "Johnny Bravo"
          },
          {
            "guid": "plex://show/5d9c084de264b7001fc4088c",
            "tag": "Regular Show"
          }
        ],
        "Studio": [
          {
            "tag": "Frederator Studios"
          },
          {
            "tag": "Cartoon Network Studios"
          }
        ]
      }
    ]
  }
}
```

#### Season Type (with `Children`)

```json
{
  "MediaContainer": {
    "offset": 0,
    "totalSize": 1,
    "identifier": "tv.plex.provider.metadata",
    "size": 1,
    "Metadata": [
      {
        "guid": "plex://season/602e59ccfdd281002cddb790",
        "key": "/library/metadata/602e59ccfdd281002cddb790/children",
        "ratingKey": "602e59ccfdd281002cddb790",
        "type": "season",
        "thumb": "http://assets.fanart.tv/fanart/tv/152831/seasonposter/adventure-time-with-finn-and-jake-5c8d180f9b002.jpg",
        "title": "Season 10",
        "parentTitle": "Adventure Time",
        "parentType": "show",
        "parentArt": "https://image.tmdb.org/t/p/original/3uE9SUywNbj1qSAuYCGgbTTYku5.jpg",
        "parentThumb": "https://image.tmdb.org/t/p/original/qk3eQ8jW4opJ48gFWYUXWaMT4l.jpg",
        "parentRatingKey": "5d9c07f72df347001e3a70b4",
        "parentGuid": "plex://show/5d9c07f72df347001e3a70b4",
        "parentKey": "/library/metadata/5d9c07f72df347001e3a70b4",
        "index": 10,
        "contentRating": "TV-PG",
        "originallyAvailableAt": "2017-09-17",
        "year": 2017,
        "Image": [
          {
            "alt": "Season 10",
            "type": "background",
            "url": "https://image.tmdb.org/t/p/original/3uE9SUywNbj1qSAuYCGgbTTYku5.jpg"
          },
          {
            "alt": "Season 10",
            "type": "backgroundSquare",
            "url": "https://metadata-static.plex.tv/1/gracenote/1c09b028e1b15c0325917c51966a47d7.jpg"
          },
          {
            "alt": "Season 10",
            "type": "coverPoster",
            "url": "http://assets.fanart.tv/fanart/tv/152831/seasonposter/adventure-time-with-finn-and-jake-5c8d180f9b002.jpg"
          }
        ],
        "Guid": [
          {
            "id": "tvdb://1823714"
          }
        ],
        "Children": {
          "size": 2,
          "Metadata": [
            {
              "guid": "plex://episode/5d9c0b7ee98e47001eb2e3a0",
              "key": "/library/metadata/5d9c0b7ee98e47001eb2e3a0",
              "ratingKey": "5d9c0b7ee98e47001eb2e3a0",
              "summary": "A fierce creature is terrorizing the Candy Kingdom but before Finn can slay the beast, he must first overcome a guilty conscience.",
              "type": "episode",
              "thumb": "https://image.tmdb.org/t/p/original/qgKsxcwvkDbAIjUceuDrv2AgtOF.jpg",
              "duration": 660000,
              "title": "The Wild Hunt",
              "grandparentTitle": "Adventure Time",
              "grandparentType": "show",
              "grandparentArt": "https://image.tmdb.org/t/p/original/3uE9SUywNbj1qSAuYCGgbTTYku5.jpg",
              "grandparentThumb": "https://image.tmdb.org/t/p/original/qk3eQ8jW4opJ48gFWYUXWaMT4l.jpg",
              "grandparentRatingKey": "5d9c07f72df347001e3a70b4",
              "grandparentGuid": "plex://show/5d9c07f72df347001e3a70b4",
              "grandparentKey": "/library/metadata/5d9c07f72df347001e3a70b4",
              "parentTitle": "Season 10",
              "parentType": "season",
              "parentArt": "https://metadata-static.plex.tv/9/gracenote/9e06ae7ff36bd8d62fa1600287f80794.jpg",
              "parentThumb": "https://image.tmdb.org/t/p/original/w8mYplN3ysIJ5DIYYgmfGTvuNzd.jpg",
              "parentRatingKey": "5d9c0939e9d5a1001f4def80",
              "parentGuid": "plex://season/5d9c0939e9d5a1001f4def80",
              "parentKey": "/library/metadata/5d9c0939e9d5a1001f4def80",
              "index": 1,
              "parentIndex": 10,
              "contentRating": "TV-PG",
              "originallyAvailableAt": "2017-09-17",
              "year": 2017,
              "Image": [
                {
                  "alt": "The Wild Hunt",
                  "type": "snapshot",
                  "url": "https://image.tmdb.org/t/p/original/qgKsxcwvkDbAIjUceuDrv2AgtOF.jpg"
                }
              ],
              "Guid": [
                {
                  "id": "imdb://tt7308394"
                },
                {
                  "id": "tmdb://1418023"
                },
                {
                  "id": "tvdb://6179251"
                }
              ],
              "Rating": [
                {
                  "image": "imdb://image.rating",
                  "type": "audience",
                  "value": 8.3
                },
                {
                  "image": "themoviedb://image.rating",
                  "type": "audience",
                  "value": 7.9
                }
              ],
              "Role": [
                {
                  "order": 1,
                  "tag": "Jeremy Shada",
                  "thumb": "https://metadata-static.plex.tv/b/people/ba6413846e4fc49884ec7694d012b198.jpg",
                  "role": "Finn the Human (voice)"
                },
                {
                  "order": 2,
                  "tag": "John DiMaggio",
                  "thumb": "https://metadata-static.plex.tv/0/people/0a945543418d442fea7ae4948b2a2fda.jpg",
                  "role": "Jake the Dog (voice)"
                }
              ],
              "Producer": [
                {
                  "tag": "Adam Muto",
                  "thumb": "https://metadata-static.plex.tv/e/people/e385c2d25614f10d505701e5f590372a.jpg",
                  "role": "Producer"
                }
              ],
              "Writer": [
                {
                  "tag": "Pendleton Ward",
                  "thumb": "https://metadata-static.plex.tv/8/people/83eb3402f017498e3a0fd5e44af8d1ae.jpg",
                  "role": "Creator"
                }
              ]
            },
            {
              "guid": "plex://episode/5d9c0b7ee98e47001eb2e38b",
              "key": "/library/metadata/5d9c0b7ee98e47001eb2e38b",
              "ratingKey": "5d9c0b7ee98e47001eb2e38b",
              "summary": "BMO and Ice King hit the road as door to door salesmen and stumble upon an irresistible opportunity.",
              "type": "episode",
              "thumb": "https://image.tmdb.org/t/p/original/fvREJ2bNoXM2WAGVPCGa3ryQtJs.jpg",
              "duration": 660000,
              "title": "Always BMO Closing",
              "grandparentTitle": "Adventure Time",
              "grandparentType": "show",
              "grandparentArt": "https://image.tmdb.org/t/p/original/3uE9SUywNbj1qSAuYCGgbTTYku5.jpg",
              "grandparentThumb": "https://image.tmdb.org/t/p/original/qk3eQ8jW4opJ48gFWYUXWaMT4l.jpg",
              "grandparentRatingKey": "5d9c07f72df347001e3a70b4",
              "grandparentGuid": "plex://show/5d9c07f72df347001e3a70b4",
              "grandparentKey": "/library/metadata/5d9c07f72df347001e3a70b4",
              "parentTitle": "Season 10",
              "parentType": "season",
              "parentArt": "https://metadata-static.plex.tv/9/gracenote/9e06ae7ff36bd8d62fa1600287f80794.jpg",
              "parentThumb": "https://image.tmdb.org/t/p/original/w8mYplN3ysIJ5DIYYgmfGTvuNzd.jpg",
              "parentRatingKey": "5d9c0939e9d5a1001f4def80",
              "parentGuid": "plex://season/5d9c0939e9d5a1001f4def80",
              "parentKey": "/library/metadata/5d9c0939e9d5a1001f4def80",
              "index": 2,
              "parentIndex": 10,
              "contentRating": "TV-PG",
              "originallyAvailableAt": "2017-09-17",
              "year": 2017,
              "Image": [
                {
                  "alt": "Always BMO Closing",
                  "type": "snapshot",
                  "url": "https://image.tmdb.org/t/p/original/fvREJ2bNoXM2WAGVPCGa3ryQtJs.jpg"
                }
              ],
              "Guid": [
                {
                  "id": "imdb://tt7308402"
                },
                {
                  "id": "tmdb://1418024"
                },
                {
                  "id": "tvdb://6305580"
                }
              ],
              "Rating": [
                {
                  "image": "imdb://image.rating",
                  "type": "audience",
                  "value": 7.6
                },
                {
                  "image": "themoviedb://image.rating",
                  "type": "audience",
                  "value": 6.7
                }
              ],
              "Role": [
                {
                  "order": 1,
                  "tag": "Jeremy Shada",
                  "thumb": "https://metadata-static.plex.tv/b/people/ba6413846e4fc49884ec7694d012b198.jpg",
                  "role": "Finn the Human (voice)"
                },
                {
                  "order": 2,
                  "tag": "John DiMaggio",
                  "thumb": "https://metadata-static.plex.tv/0/people/0a945543418d442fea7ae4948b2a2fda.jpg",
                  "role": "Jake the Dog (voice)"
                }
              ],
              "Producer": [
                {
                  "tag": "Adam Muto",
                  "thumb": "https://metadata-static.plex.tv/e/people/e385c2d25614f10d505701e5f590372a.jpg",
                  "role": "Producer"
                }
              ],
              "Writer": [
                {
                  "tag": "Pendleton Ward",
                  "thumb": "https://metadata-static.plex.tv/8/people/83eb3402f017498e3a0fd5e44af8d1ae.jpg",
                  "role": "Creator"
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```

#### Episode Type

```json
{
  "MediaContainer": {
    "offset": 0,
    "totalSize": 1,
    "identifier": "tv.plex.provider.metadata",
    "size": 1,
    "Metadata": [
      {
        "guid": "plex://episode/5d9c0b7ee98e47001eb2e3a0",
        "key": "/library/metadata/5d9c0b7ee98e47001eb2e3a0",
        "ratingKey": "5d9c0b7ee98e47001eb2e3a0",
        "summary": "A fierce creature is terrorizing the Candy Kingdom but before Finn can slay the beast, he must first overcome a guilty conscience.",
        "type": "episode",
        "thumb": "https://image.tmdb.org/t/p/original/qgKsxcwvkDbAIjUceuDrv2AgtOF.jpg",
        "duration": 660000,
        "title": "The Wild Hunt",
        "grandparentTitle": "Adventure Time",
        "grandparentType": "show",
        "grandparentArt": "https://image.tmdb.org/t/p/original/3uE9SUywNbj1qSAuYCGgbTTYku5.jpg",
        "grandparentThumb": "https://image.tmdb.org/t/p/original/qk3eQ8jW4opJ48gFWYUXWaMT4l.jpg",
        "grandparentRatingKey": "5d9c07f72df347001e3a70b4",
        "grandparentGuid": "plex://show/5d9c07f72df347001e3a70b4",
        "grandparentKey": "/library/metadata/5d9c07f72df347001e3a70b4",
        "parentTitle": "Season 10",
        "parentType": "season",
        "parentArt": "https://metadata-static.plex.tv/9/gracenote/9e06ae7ff36bd8d62fa1600287f80794.jpg",
        "parentThumb": "https://image.tmdb.org/t/p/original/w8mYplN3ysIJ5DIYYgmfGTvuNzd.jpg",
        "parentRatingKey": "5d9c0939e9d5a1001f4def80",
        "parentGuid": "plex://season/5d9c0939e9d5a1001f4def80",
        "parentKey": "/library/metadata/5d9c0939e9d5a1001f4def80",
        "index": 1,
        "parentIndex": 10,
        "contentRating": "TV-PG",
        "originallyAvailableAt": "2017-09-17",
        "year": 2017,
        "Image": [
          {
            "alt": "The Wild Hunt",
            "type": "snapshot",
            "url": "https://image.tmdb.org/t/p/original/qgKsxcwvkDbAIjUceuDrv2AgtOF.jpg"
          }
        ],
        "Guid": [
          {
            "id": "imdb://tt7308394"
          },
          {
            "id": "tmdb://1418023"
          },
          {
            "id": "tvdb://6179251"
          }
        ],
        "Rating": [
          {
            "image": "imdb://image.rating",
            "type": "audience",
            "value": 8.3
          },
          {
            "image": "themoviedb://image.rating",
            "type": "audience",
            "value": 7.9
          }
        ],
        "Role": [
          {
            "order": 1,
            "tag": "Jeremy Shada",
            "thumb": "https://metadata-static.plex.tv/b/people/ba6413846e4fc49884ec7694d012b198.jpg",
            "role": "Finn the Human (voice)"
          },
          {
            "order": 2,
            "tag": "John DiMaggio",
            "thumb": "https://metadata-static.plex.tv/0/people/0a945543418d442fea7ae4948b2a2fda.jpg",
            "role": "Jake the Dog (voice)"
          }
        ],
        "Producer": [
          {
            "tag": "Adam Muto",
            "thumb": "https://metadata-static.plex.tv/e/people/e385c2d25614f10d505701e5f590372a.jpg",
            "role": "Producer"
          }
        ],
        "Writer": [
          {
            "tag": "Pendleton Ward",
            "thumb": "https://metadata-static.plex.tv/8/people/83eb3402f017498e3a0fd5e44af8d1ae.jpg",
            "role": "Creator"
          }
        ]
      }
    ]
  }
}

```

## Media Queries

Media queries are a querystring-based filtering language used to select subsets of media. The language is rich, and can express complex expressions for media selection, as well as sorting and grouping.

### Fields

Queries reference fields, which can be of a few types:

  - *integer*: numbers
  - *boolean*: true/false
  - *tag*: integers representing tag IDs.
  - *string*: strings
  - *date*: epoch seconds
  - *language*: string in ISO639-2b format.

These fields are detailed in `Field` elements in the section description endpoint (e.g. `/library/sections/X?includeDetails=1`).

### Operators

Given that media queries are expressible using querystrings, the operator syntax might look a bit quirky, because a) they have to include the `=` character, and b) characters to the left of the equal sign usually have to be URI encoded.

Operators are defined per type:

  - *integer*: `=` (equals), `!=` (not equals), `>>=` (greater than), `<<=` (less than), `<=` (less than or equals), `>=` (greater than or equals)
  - *boolean*: `=0` (false) and `=1` (true)
  - *tag*: `=` (is) and `!=` (is not)
  - *string*: `=` (contains), `!=` (does not contain), `==` (equals), `!==` (does not equal), `<=` (begins with), `>=` (ends with)
  - *date*:  `=` (equals), `!=` (not equals), `>>=` (after), `<<=` (before)
  - *language*:  `=` (equals), `!=` (not equals)

### Relative Values and Units

For some types, values can be specified as relative. For dates, epoch seconds can be specified as relative to “now” as follows: `+N` (in N seconds from now and `-N` (N seconds ago).

In addition, the following unit suffixes can be used on date values:

  - *m*: minutes
  - *h*: hours
  - *d*: days
  - *w*: weeks
  - *mon*: months
  - *y*: years

For example, `>>=-3y` means “within the last 3 years”.

### Field Scoping

Some media is organized hierarchically (e.g. shows), and in those cases, many fields are common to different elements in the hierarchy (e.g. show title vs episode title). The following rules are used to resolve field references.

  - A `type` parameter must be included to specify the result type.
  - Any non-qualified field is defaulted to refer to the result type.
  - In order to refer to other levels of the hierarchy, use the scoping operator, e.g. `show.title` or `episode.year`. A query may be comprised of multiple fields from different levels of the hierarchy.
  - the `sourceType` parameter may be used to change the default level to which fields refer. For example, `type=4&sourceType=2&title==24` means “all episodes where the show title is 24”.

### Sorting

The `sort` parameter is used to indicate an ordering on results. Typically, the sort value is a field (including optional scoping). The `:` character is used to indicate additional features of the sort, and the `,` character is used to include multiple fields to the sort.

For example, `sort=title,index` means “sort first by title ascending, then by index”.  Sort features are:

  - *desc*: indicates a descending sort.
  - *nullsLast*: indicates that null values are sorted last.

Sort features may be mixed and matched, e.g. `sort=title,index:desc`.

### Grouping

The `group` parameter is used to group results by a field, similar to the SQL feature `group by`. For example, when listing popular tracks, we use the query `type=10&sort=ratingCount:desc&group=title`, because we don't want multiple tracks with the same name (e.g. same track on different albums) showing up.

### Limits

The `limit` parameter is used to limit the number of results returned. Because it's implemented on top of the SQL `limit` operator, it currently only operates at the level of the type returned. In other words, `type=10&limit=100` will return at most 100 tracks, but you can't select tracks from a limit of 10 _albums_.

### Boolean Operators

Given the nature of querystrings, it makes a lot of sense to interpret the `&` character as a boolean AND operator. For example `rating=10&index=5` means “rating is 10 AND index is 5”.

We leverage the `,` operator to signify the boolean OR operator. SO `rating=1,2,3` means “rating is 1 OR 2 OR 3. Given standard precedence rules, `rating=1,2,3&index=5` is parsed as `(rating = 1 or rating = 2 or rating = 3) and index = 5)`.

### Complex Expressions

There's only so many expressions you can form using vanilla querystring-to-boolean mapping (essentially, “ANDs of ORs”). In order to fully represent complex boolean expressions, there are a few synthetic additions:

  - *push=1* and *pop=1*:  These are the equivalent of opening and closing parenthesis.
  - *or=1*: These is an explicit OR operator.

As an example: `push=1&index=1&or=1&rating=2&pop=1&duration=10` parses into `(index = 1 OR rating = 2) AND duration = 10`. This could not be expressed by the simplified syntax above.

Happy query building!

## Profile Augmentations

The universal transcode endpoint supports the following header or query string parameter: ```X-Plex-Client-Profile-Extra```.

The value of this parameter is url-encoded.  When url-decoded, it consists of a string expressed in the following (poor man's) BNF grammar:

```
<ProfileExtension> ::= <Directive> "+" <Directive>*
<Directive> :: = <Verb> <Arguments>
<Verb> ::= "add-direct-play-profile" | "add-limitation" | "add-transcode-target-codec" | "append-transcode-target-codec" | "add-transcode-target" | "add-settings"
<Arguments> ::= "(" (<Name> "=" <Value>) "&")*
<Name> ::= <Text>
<Value> ::= <Text>
```

### add-direct-play-profile
This directive augments the set of Direct Play profiles in the client profile. The following parameters are required:

- `type` = "videoProfile" | "musicProfile" | "photoProfile" | "subtitleProfile"
- `container` = * or a comma-separated list of containers
- `videoCodec` = * or a comma-separated list of video codecs
- `audioCodec` = * or a comma-separated list of audio codecs
- `subtitleCodec` = * or a comma-separated list of subtitle formats

`*` means to use all existing matching values in the profile. At least one of the `videoCodec`, `audioCodec` and `subtitleCodec` parameters must not be `*`.


#### add-direct-play-profile example
To add `ac3` as a video audio codec for mp4 and mov containers:

```
add-direct-play-profile(type=videoProfile&container=mp4,mov&videoCodec=*&audioCodec=ac3&subtitleCodec=*)
```

### add-limitation
This directive adds a scoped limitation to the profile. The following parameters are required:

- `scope` = "videoContainer" | "musicContainer" | "photoContainer" | "videoCodec" | "videoAudioCodec" | "musicCodec" | "subtitleCodec" | "transcodeTarget"
- `scopeName` = the name of the relevant container or codec
- `type` = "match" | "notMatch" | "upperBound" | "lowerBound"
- `name` = the name of the limitation

The following parameters are optional:
- `isRequired` = true|false (default is false)
- `allStreams` = true|false (default is false)
- `replace` = true|false (default is false)

If the `replace` parameter is true, the limitation will replace any similarly scoped limitations (i.e. identical `scope` and `scopeName`. If false, the new limitation will simply add itself to the list of limitations.

Exactly one of the following three parameters is required:
- `value` = the value of the limitation
- `substring` = the substring of the limitation
- `regex` = the regex of the limitation

The `transcodeTarget` scope exists to attach a limitation to a transcode target.  This allows clients to  tell the MDE to select a specific transcode target for a context/protocol pair, based on specific information about the media itself.  When multiple transcode targets match, the first one in the profile will be selected.


#### add-limitation examples
To add a limitation on ac3 audio tracks in video media specifying a maximum of 6 channels:
```
add-limitation(scope=videoAudioCodec&scopeName=ac3&type=upperBound&name=audio.channels&value=6)
```

To add a limitation on ac3 audio tracks in video media specifying a maximum bitrate:
```
add-limitation(scope=videoAudioCodec&scopeName=ac3&type=upperBound&name=audio.bitrate&value=160)
```

To add a limitation on h264 video specifying a maximum level:
```
add-limitation(scope=videoCodec&scopeName=h264&type=upperBound&name=video.level&value=40&isRequired=true)
```

To add a limitation to a transcode target:
```
add-limitation(scope=transcodeTarget&scopeName=MyTranscodeProfile&type=upperBound&name=audio.channels&value=2)
```

### add-transcode-target-codec
This directive adds additional codecs to the beginning of the audioCodec and/or subtitleCodec lists for the specified transcode target. The following parameters are required:

- `type` = "videoProfile" | "musicProfile" | "photoProfile" | "subtitleProfile"

Either `id` or `context` and `protocol` are required:

- `id` = a transcode target identifier
- `context` = a transcode context ("streaming" | "static")
- `protocol` = a protocol ("hls" | "http" | "slss" ... )

At least one of the following parameters are also required:

- `videoCodec` = a comma-separated list of videoCodecs, which are added to the set of video codecs on the target.
- `audioCodec` = a comma-separated list of audioCodecs, which are added to the set of audio codecs on the target.
- `subtitleCodec` = a comma-separated list of audioCodecs, which are added to the set of subtitle codecs on the target.

#### add-transcode-target-codec example
To add `ac3` as an additional transcode target option to a HTTP Live Streaming target:

```
add-transcode-target-codec(type=videoProfile&context=streaming&protocol=hls&audioCodec=ac3)
```

### append-transcode-target-codec
This directive appends additional codecs to the end of the audioCodec and/or subtitleCodec lists for the specified transcode target.  The parameters are the same as for `add-transcode-target-codec`.

```
append-transcode-target-codec(type=videoProfile&context=streaming&protocol=hls&audioCodec=dca)
```

### add-transcode-target
This directive adds a new transcode target.  If a transcode target matching the type/context/profile already exists in the profile, then this directive is ignored.  The following parameters are required:

- `type` = "videoProfile" | "musicProfile" | "photoProfile" | "subtitleProfile"
- `context` = a transcode context ("streaming" | "static")
- `protocol` = a protocol ("hls" | "http" | "slss" ... )
- `container` = a container

The following parameters are optional:

- `id` = a transcode target identifier
- `replace` = true|false (default is false)

If the `replace` parameter is true, the transcode target will replace any similarly scoped transcode target (i.e. identical `type`, `context` and `protocol`. If false, the augmentation will fail if there is an existing transcode target.

The following parameters are required, depending on the type:

- `videoCodec` = a video codec (required for video) or a comma-separated list of video codecs
- `audioCodec` = an audio codec (required for music and video) or a comma-separated list of audio codecs
- `subtitleCodec` = an subtitle codec (required for subtitles and optional for video) or a comma-separated list of subtitle codecs

#### add-transcode-target examples

```
add-transcode-target(type=videoProfile&context=streaming&protocol=http&container=mkv&videoCodec=h264&audioCodec=aac,ac3&subtitleCodec=srt)
```

```
add-transcode-target(type=musicProfile&context=streaming&protocol=http&container=flac&audioCodec=flac)
```

```
add-transcode-target(type=subtitleProfile&context=all&protocol=http&container=webvtt&subtitleCodec=webvtt)
```

### add-settings
This directive overrides global settings for the profile.  The parameters are name/value pairs matching existing client profile settings.

```
add-settings(DirectPlayStreamSelection=false&RandomAccessDataModel=limited)
```

## Authenticating with Plex

Plex supports two authentication methods:

### JWT Authentication (Recommended)

Plex now supports JSON Web Token (JWT) authentication that provides better security, shorter token lifespans, and improved protection against potential security breaches.

#### Why JWT Authentication?

The new JWT system addresses security concerns by:
- **Short-lived tokens**: Tokens expire after 7 days
- **Public-key cryptography**: Uses modern cryptographic standards (ED25519) for enhanced security
- **Better clock synchronization**: Built-in timestamp validation helps devices stay in sync

#### How JWT Authentication Works

**1. Register your public key**

The new system uses a public-key authentication model where each device uploads a public key (JWK) and then requests short-lived JWT tokens. There are two ways to get started with JWT authentication:

**Option 1: PIN Authentication Flow (Recommended for New Apps)**

This method allows you to get JWT tokens without needing any existing tokens first. It's the preferred approach for new applications.

**Step 1: Generate a PIN with JWK**

```bash
POST https://clients.plex.tv/api/v2/pins
Headers:
  X-Plex-Client-Identifier: your-device-identifier

Body:
{
  "jwk": {
    "kty": "OKP",
    "crv": "Ed25519",
    "x": "your-public-key-data",
    "kid": "your-key-id",
    "alg": "EdDSA"
  },
  "strong": true
}
```

**Step 2: User Authentication**

Construct the Auth App URL and have the user authenticate:
```
https://app.plex.tv/auth#?clientID=<clientIdentifier>&code=<pinCode>&context%5Bdevice%5D%5Bproduct%5D=My%20Cool%20Plex%20App&forwardUrl=https%3A%2F%2Fmy-cool-plex-app.com
```

For 4-digit pins, you need to use the link page: `https://plex.tv/link/?pin=<code>`

**Step 3: Exchange PIN for JWT Token**

```bash
GET https://clients.plex.tv/api/v2/pins/<pinID>?deviceJWT=<signedJWT>
```

The signed JWT must include:
- `"aud": "plex.tv"`
- `"iss": "<clientIdentifier>"`
- `"kid"` and `"alg"` in the header

You will get the Plex JWT token in the `authToken` field of the response.

**Option 2: Register your public key with existing tokens (For Existing Apps)**

If you already have a legacy token, you can use it to register your device for JWT authentication:

```bash
POST https://clients.plex.tv/api/v2/auth/jwk
Headers:
  X-Plex-Client-Identifier: your-device-identifier
  X-Plex-Token: your-existing-token

Body:
{
  "jwk": {
    "kty": "OKP",
    "crv": "Ed25519",
    "x": "your-public-key-data",
    "kid": "your-key-id",
    "use": "sig",
    "alg": "EdDSA"
  }
}
```

After registering your public key, you should follow the same steps described below to refresh your token to get your first JWT.

**2. Token Refresh Process**

Once registered, your device must refresh its token every 7 days using this three-step process:

**Step 1: Get a Nonce**

```bash
GET https://clients.plex.tv/api/v2/auth/nonce
Headers:
  X-Plex-Client-Identifier: your-device-identifier
```

This returns a unique nonce valid for 5 minutes:
```json
{
  "nonce": "7c415b56-8f48-488a-98ab-847ef4460442"
}
```

**Step 2: Create a Device JWT**

Your device creates a JWT containing:
- The nonce from step 1
- Required scope permissions (see Scope Details below)
- Audience set to `plex.tv`
- Issuer set to your `client_identifier`
- Signed with your device's private key

**Important JWT Header Requirements:**

Your JWT must include these header fields:
- `"kid"`: The key identifier from your JWK registration
- `"alg"`: Must be `"EdDSA"` for ED25519 signatures, or `"RS256"` for RSA signatures

**Scope Details:**

The scope field in your device JWT should contain comma-separated values for the user data you need included in the JWT:
- `username` - Access to the user's username
- `email` - Access to the user's email address
- `friendly_name` - Access to the user's friendly name
- `restricted` - Access to the user's restricted status
- `anonymous` - Access to the user's anonymous status
- `joinedAt` - Access to the user's account creation timestamp

**Example Device JWT Header:**

```json
{
  "kid": "your-key-id",
  "alg": "EdDSA",
  "typ": "JWT"
}
```

**Example Device JWT Payload:**

```json
{
  "nonce": "7c415b56-8f48-488a-98ab-847ef4460442",
  "scope": "username,email,friendly_name",
  "aud": "plex.tv",
  "iss": "your-client-identifier",
  "iat": 1705785603,
  "exp": 1705789203
}
```

**Step 3: Exchange for Plex Token**

```bash
POST https://clients.plex.tv/api/v2/auth/token
Headers:
  X-Plex-Client-Identifier: your-device-identifier

Body:
{
  "jwt": "your-device-signed-jwt"
}
```

This returns a new Plex.tv JWT valid for 7 days:

```json
{
  "auth_token": "eyJraWQiOiJYeVRRN21seXFtVmhJcEo0U1pDZGltdXo3ZjdEYXU1Ym9MLXU2MG5JeEdJIiwidHlwIjoiSldUIiwiYWxnIjoiRWREU0EifQ..."
}
```

**Using Your JWT Token**

Once you have a JWT token, use it exactly like the old tokens in the `X-Plex-Token` header. Note it can be used to access any Plex.tv endpoint or your Plex Media Server instance:

```bash
GET http://your-plex-server:32400/library/sections
Headers:
  X-Plex-Token: your-jwt-token
```

#### JWT Authentication Benefits

**Security Features:**

- **Token Rotation**: Automatic expiration every 7 days
- **Individual Revocation**: Each device can be individually disabled
- **Cryptographic Verification**: Uses industry-standard ED25519 signatures
- **Nonce Protection**: Prevents replay attacks

**Developer Experience:**

- **Familiar Interface**: Same `X-Plex-Token` header usage
- **Automatic Clock Sync**: Built-in timestamp validation
- **Clear Error Codes**: Specific error responses for different failure modes
- **Rate Limiting**: Built-in protection against abuse

#### Error Handling

The JWT system provides clear error responses with specific HTTP status codes:

**Common Error Responses:**

- **498 Token Expired**: Your JWT has expired and needs refresh
- **422 Signature Verification Failed**: Invalid device signature or JWT structure
- **422 Thumbprint Already Taken**: JWK already registered by another device
- **400 Bad Request**: Invalid request format or missing required fields
- **429 Too Many Requests**: Rate limit exceeded (nonce requests are rate-limited)

**Troubleshooting Tips:**

- **Missing `kid` field**: Ensure your JWT header includes the `kid` field matching your registered JWK
- **Invalid signature**: Verify your private key matches the public key you registered
- **Clock synchronization**: Ensure your device's clock is accurate (JWT includes timestamp validation)
- **Nonce expiration**: Nonces are only valid for 5 minutes - request a new one if yours has expired
- **Rate limiting**: Nonce requests are rate-limited to prevent abuse

#### Migration Guide

**For New Applications or new users:**

1. Generate an ED25519 key pair for your device
2. Use the PIN authentication flow (Option 1 above) to register your device and get JWT tokens
3. Implement the token refresh flow for ongoing authentication
4. Use the returned JWT in your `X-Plex-Token` header

**To replace legacy tokens of existing applications:**

1. Continue using your current token for now
2. Register your public key with your existing tokens (Option 2 above)
3. Generate your first JWT token using the token refresh process (Your legacy token will expire after this process)
4. Implement the token refresh flow for ongoing authentication
5. Use the returned JWT in your `X-Plex-Token` header


**Token Refresh:**

JWT tokens expire after 7 days but can be refreshed at any time, including after expiration. Use the token refresh process described above.

### Traditional Token Authentication (Legacy)

You're developing an app that needs access to a user's Plex account. To do this, you'll need to get access to the user's Access Token. This document details how to check whether an Access Token is valid, and how to obtain a new one.

#### High-level Steps

1. Choose a unique app name, like "My Cool App"
2. Check storage for your app's Client Identifier; generate and store one if none is present.
3. Check storage for the user's Access Token; if present, verify its validity and carry on.
4. If an Access Token is missing or invalid, generate a PIN, and store its `id`.
5. Construct an Auth App url and send the user's browser there to authenticate.
6. After authentication, check the PIN's `id` to obtain and store the user's Access Token.

#### Detailed Steps

1. Choose a unique app name

    The app name you choose will be visible in the user's Authorized Devices view. The name you choose should be different from any existing Plex products.

1. Generate a Client Identifier

    The Client Identifier identifies the specific instance of your app. A random string or UUID is sufficient here. There are no hard requirements for Client Identifier length or format, but once one is generated the client should store and re-use this identifier for subsequent requests.

1. Verify stored Access Token validity

    You can check whether a user's stored Access Token is valid by requesting user info from the plex.tv API and examining the HTTP status code of the response.

    ```
    $ curl -X GET https://plex.tv/api/v2/user \
      -H 'Accept: application/json' \
      -H 'X-Plex-Product: My Cool App' \
      -H 'X-Plex-Client-Identifier: <clientIdentifier>' \
      -H 'X-Plex-Token: <userToken>'
    ```

    | HTTP Status Code | |
    |-|-|
    | `200` | Access Token is valid |
    | `401` | Access Token is invalid |

    If an Access Token is invalid, it should be discarded, and new one should be obtained through the authentication process.

    If plex.tv cannot be reached, or if you receive any other status code it indicates an error state, but does not indicate an invalid Access Token.


1. Generate a PIN

    To sign a user in, the app must create a time-limited PIN. The user is then led through a process to "claim" the PIN, associating it with their account and granting the app access to the user's plex.tv account.

    ```
    $ curl -X POST https://plex.tv/api/v2/pins?strong=true \
      -H 'Accept: application/json' \
      -H 'X-Plex-Product: My Cool App' \
      -H 'X-Plex-Client-Identifier: <clientIdentifier>'
    ```

    Note: the `strong=true` header provides a longer length pin which will have a longer lifetime.  This is useful in cases where the user is not expected to type in the pin themselves.  If not specified, a shorter pin is created but will have a much shorter lifetime.

    The response will be a JSON payload; the two important properties are `id` and `code`. Store the `id` locally, and use the `code` to construct the Auth App url.

    ```
    {
      "id": 564964751,
      "code": "8lzjqnq8lye02n52jq3fqxf8e",
      …
    }
    ```

1. Checking the PIN

    There are two primary ways apps interact with the Auth App and the PIN-claiming process; **Forwarding** and **Polling**.

    **Forwarding** is used by web-based apps. A user visits your app in their web browser, leaves your app to authenticate with Plex, and returns to your app via a `forwardUrl` your app provides.

    **Polling** is used by native apps running outside of a web browser. A user indicates their intention to sign-in from within your app, and your app opens a web browser pointing to the Auth App where the user completes sign-in. Your app will periodically poll on the generated PIN until it is claimed, or it expires.

1. Construct the Auth App url

    The user will authenticate with the plex.tv Auth App through their web browser.

    If you're using the **Forwarding** flow, the user will be returned to your app after authenticating where you'll be able to check the created PIN to determine the user's Access Token. The `forwardUrl` to which the user will be returned can carry the PIN `id` which needs to be checked on their return to the app.

    Auth App urls are encoded as parameters to the url fragment. Practically, this means that your Auth App url will be prefixed with `https://app.plex.tv/auth#?`; the `#?` at the end indicates the beginning of the url fragment, and that the content of the fragment afterwards is encoded as url parameter key-values pairs.

    Append these parameters to construct the final URL.

    | Parameter                        |                                                                 |
    |----------------------------------|-----------------------------------------------------------------|
    | `clientID`                         | Your client identifier                                          |
    | `code`                             | The `code` from the generated PIN                               |
    | `forwardUrl`                       | The url to which the user will be returned after authenticating. |
    | `context%5Bdevice%5D%5Bproduct%5D` | The name of your App; ex "My Cool App"                     |

    *Example*

    ```
    https://app.plex.tv/auth#?clientID=<clientIdentifier>&code=<pinCode>&context%5Bdevice%5D%5Bproduct%5D=My%20Cool%20Plex%20App&forwardUrl=https%3A%2F%2Fmy-cool-plex-app.com
    ```

    You can use the [`qs`](https://www.npmjs.com/package/qs) module to encode all necessary parameters, including the nested `context` parameter.


    ```js
    const authAppUrl =
      'https://app.plex.tv/auth#?' +
      require('qs').stringify({
        clientID: '<clientIdentifier>',
        code: '<pinCode>',
        forwardUrl: 'https://my-cool-plex-app.com',
        context: {
          device: {
            product: 'My Cool App',
          },
        },
      });
    ```

1. Send user's browser to constructed Auth App url

    Once the Auth App URL has been constructed, send the user's browser there to authenticate.

1. Check PIN

    If you're using the **Polling** flow, your app should periodically (once per second) check the PIN `id` to determine when the user has signed-in.

    If you're using the **Forwarding** flow, check the stored PIN `id` from the PIN creation step. If the PIN has been claimed, the `authToken` field in the response will contain the user's Access Token you need to make API calls on behalf of the user. If authentication failed, the `authToken` field will remain `null`.

    ```
    $ curl -X GET 'https://plex.tv/api/v2/pins/<pinID>' \
      -H 'Accept: application/json' \
      -H 'X-Plex-Client-Identifier: <clientIdentifier>'
    ```
### Talking to PMS

Once you have a token to talk to plex.tv, you will need to obtain a different set of tokens used to talk to PMS instances.

```
$ curl https://clients.plex.tv/api/v2/resources?includeHttps=1&includeRelay=1&includeIPv6=1 \
  -H 'Accept: application/json' \
  -H 'X-Plex-Product: My Cool App' \
  -H 'X-Plex-Client-Identifier: <clientIdentifier>' \
  -H 'X-Plex-Token: <userToken>'
```

The response will be a JSON document which will contain available PMS instances, the `accessToken` used in communication with this PMS, and the list of connection URLs where the PMS may be contacted.  Connections labeled as `local` should be preferred over those that are not, and `relay` should only be used as a last resort as bandwidth on relay connections is limited.

## Unique Capabilities

These capabilities aren't available in any other tool for this API.
- **`serve`** — Serve the preserved /plex/<account>/<server> health contract for Uptime Kuma.
- **`serve`** — Refresh Plex.tv resources per health request and match servers by stable clientIdentifier.
- **`serve`** — Verify library metadata and read a bounded byte range from a playable media part.

## Command Reference

**activities** — Activities provide a way to monitor and control asynchronous operations on the server. In order to receive real-time updates for activities, a client would normally subscribe via either EventSource or Websocket endpoints.

Activities are associated with HTTP replies via a special `X-Plex-Activity` header which contains the UUID of the activity.

Activities are optional cancellable. If cancellable, they may be cancelled via the `DELETE` endpoint.

- `plexctl-pp-cli activities delete-activity` — Cancel a running activity. Admins can cancel all activities but other users can only cancel their own
- `plexctl-pp-cli activities get-slash` — List all activities on the server. Admins can see all activities but other users can only see their own

**butler** — The butler is responsible for running periodic tasks.  Some tasks run daily, others every few days, and some weekly.  These includes database maintenance, metadata updating, thumbnail generation, media analysis, and other tasks.

- `plexctl-pp-cli butler delete-slash` — This endpoint will stop all currently running tasks and remove any scheduled tasks from the queue.
- `plexctl-pp-cli butler delete-task` — This endpoint will stop a currently running task by name, or remove it from the list of scheduled tasks if it exists
- `plexctl-pp-cli butler get-slash` — Get the list of butler tasks and their scheduling
- `plexctl-pp-cli butler post-slash` — This endpoint will attempt to start all Butler tasks that are enabled in the settings.
- `plexctl-pp-cli butler post-task` — This endpoint will attempt to start a specific Butler task by name.

**download-queue** — Manage download queue

- `plexctl-pp-cli download-queue get-queue` — Available: 0.2.0 Get a download queue by its id
- `plexctl-pp-cli download-queue post` — Available: 0.2.

**hubs** — The hubs within a media provider

- `plexctl-pp-cli hubs get-continue-watching` — Get the global continue watching hub
- `plexctl-pp-cli hubs get-items` — Get the items within a single hub specified by identifier
- `plexctl-pp-cli hubs get-metadata-metadata` — Get the hubs for a section by metadata item. Currently only for music sections
- `plexctl-pp-cli hubs get-metadata-metadata-postplay` — Get the hubs for a metadata to be displayed in post play
- `plexctl-pp-cli hubs get-metadata-metadata-related` — Get the hubs for a metadata related to the provided metadata item
- `plexctl-pp-cli hubs get-promoted` — Get the global hubs which are promoted (should be displayed on the home screen)
- `plexctl-pp-cli hubs get-search` — Perform a search and get the result as hubs This endpoint performs a search across all library sections
- `plexctl-pp-cli hubs get-section` — Get the hubs for a single section
- `plexctl-pp-cli hubs get-slash` — Get the global hubs in this PMS
- `plexctl-pp-cli hubs search-get-voice` — Perform a search tailored to voice input and get the result as hubs This endpoint performs a search specifically
- `plexctl-pp-cli hubs sections-section-manage-delete-identifier` — Delete a custom hub from the server
- `plexctl-pp-cli hubs sections-section-manage-delete-slash` — Reset hubs for this section to defaults and delete custom hubs
- `plexctl-pp-cli hubs sections-section-manage-get-slash` — Get the list of hubs including both built-in and custom
- `plexctl-pp-cli hubs sections-section-manage-post-slash` — Create a custom hub based on a metadata item
- `plexctl-pp-cli hubs sections-section-manage-put-identifier` — Changed the visibility of a hub for both the admin and shared users
- `plexctl-pp-cli hubs sections-section-manage-put-move` — Changed the ordering of a hub among others hubs

**identity** — Manage identity

- `plexctl-pp-cli identity` — Get details about this PMS's identity

**library** — Library endpoints which are outside of the Media Provider API.  Typically this is manipulation of the library (adding/removing sections, modifying preferences, etc).

- `plexctl-pp-cli library collection-collection-get-composite` — Get an image for the collection based on the items within
- `plexctl-pp-cli library collection-collection-get-items` — Get items in a collection. Note if this collection contains more than 100 items, paging must be used.
- `plexctl-pp-cli library collection-collection-put-items` — Add items to a collection by uri
- `plexctl-pp-cli library collection-collection-put-items-item` — Delete an item from a collection
- `plexctl-pp-cli library collection-collection-put-items-item-move` — Reorder items in a collection with one item after another
- `plexctl-pp-cli library collection-post-slash` — Create a collection in the library
- `plexctl-pp-cli library delete-caches` — Delete the hub caches so they are recomputed on next request
- `plexctl-pp-cli library delete-section` — Delete a library section by id
- `plexctl-pp-cli library delete-sections-all-refresh` — Stop all refreshes across all sections
- `plexctl-pp-cli library delete-streams-stream` — Delete a stream. Only applies to downloaded subtitle streams or a sidecar subtitle when media deletion is enabled.
- `plexctl-pp-cli library get-all` — Request all metadata items according to a query.
- `plexctl-pp-cli library get-matches` — The matches endpoint is used to match content external to the library with content inside the library.
- `plexctl-pp-cli library get-media-media-chapter-images-chapter` — Get a single chapter image for a piece of media
- `plexctl-pp-cli library get-metadata-augmentations-augmentation` — Get augmentation status and potentially wait for completion
- `plexctl-pp-cli library get-parts-part-changestamp-filename` — Get a media part for streaming or download. - streaming: This is the default scenario.
- `plexctl-pp-cli library get-parts-part-indexes-index` — Get BIF index for a part by index type
- `plexctl-pp-cli library get-parts-part-indexes-index-offset` — Extract an image from the BIF for a part at a particular offset
- `plexctl-pp-cli library get-people-person` — Get details for a single actor.
- `plexctl-pp-cli library get-people-person-media` — Get all the media for a single actor.
- `plexctl-pp-cli library get-random-artwork` — Get random artwork across sections. This is commonly used for a screensaver.
- `plexctl-pp-cli library get-sections` — A library section (commonly referred to as just a library) is a collection of media.
- `plexctl-pp-cli library get-sections-prefs` — Get a section's preferences for a metadata type
- `plexctl-pp-cli library get-streams-stream` — Get a stream (such a a sidecar subtitle stream)
- `plexctl-pp-cli library get-streams-stream-levels` — The the loudness of a stream in db, one entry per 100ms
- `plexctl-pp-cli library get-streams-stream-loudness` — The the loudness of a stream in db, one number per line, one entry per 100ms
- `plexctl-pp-cli library get-tags` — Get all library tags of a type
- `plexctl-pp-cli library metadata-delete-element` — Delete the artwork, thumb, element for a metadata item This operation will also lock the field.
- `plexctl-pp-cli library metadata-delete-marker-marker` — Delete a marker for this user on the metadata item
- `plexctl-pp-cli library metadata-delete-media-media-item` — Delete a single media from a metadata item in the library
- `plexctl-pp-cli library metadata-delete-slash` — Delete a single metadata item from the library, deleting media as well
- `plexctl-pp-cli library metadata-get-all-leaves` — Get the leaves for a metadata item such as the episodes in a show
- `plexctl-pp-cli library metadata-get-element` — Get the artwork, thumb, element for a metadata item
- `plexctl-pp-cli library metadata-get-extras` — Get the extras for a metadata item
- `plexctl-pp-cli library metadata-get-file` — Get a bundle file for a metadata or media item. This is either an image or a mp3 (for a show's theme)
- `plexctl-pp-cli library metadata-get-matches` — Get the list of metadata matches for a metadata item
- `plexctl-pp-cli library metadata-get-nearest` — Get the nearest tracks, sonically, to the provided track
- `plexctl-pp-cli library metadata-get-related` — Get a hub of related items to a metadata item
- `plexctl-pp-cli library metadata-get-similar` — Get a list of similar items to a metadata item
- `plexctl-pp-cli library metadata-get-slash` — Get one or more metadata items.
- `plexctl-pp-cli library metadata-get-tree` — Get a tree of metadata items, such as the seasons/episodes of a show
- `plexctl-pp-cli library metadata-get-users-top` — Get the list of users which have played this item starting with the most
- `plexctl-pp-cli library metadata-post-element` — Set the artwork, thumb, element for a metadata item Generally only the admin can perform this action.
- `plexctl-pp-cli library metadata-post-extras` — Add an extra to a metadata item
- `plexctl-pp-cli library metadata-post-marker` — Create a marker for this user on the metadata item
- `plexctl-pp-cli library metadata-post-subtitles` — Add a subtitle to a metadata item
- `plexctl-pp-cli library metadata-put-addetect` — Start the detection of ads in a metadata item
- `plexctl-pp-cli library metadata-put-analyze` — Start the analysis of a metadata item
- `plexctl-pp-cli library metadata-put-chapter-thumbs` — Start the chapter thumb generation for an item
- `plexctl-pp-cli library metadata-put-credits` — Start credit detection on a metadata item
- `plexctl-pp-cli library metadata-put-element` — Set the artwork, thumb, element for a metadata item Generally only the admin can perform this action.
- `plexctl-pp-cli library metadata-put-index` — Start the indexing (BIF generation) of an item
- `plexctl-pp-cli library metadata-put-intro` — Start the detection of intros in a metadata item
- `plexctl-pp-cli library metadata-put-marker-marker` — Edit a marker for this user on the metadata item
- `plexctl-pp-cli library metadata-put-match` — Match a metadata item to a guid
- `plexctl-pp-cli library metadata-put-merge` — Merge a metadata item with other items
- `plexctl-pp-cli library metadata-put-prefs` — Set the preferences on a metadata item
- `plexctl-pp-cli library metadata-put-refresh` — Refresh a metadata item from the agent
- `plexctl-pp-cli library metadata-put-slash` — Edit metadata items setting fields
- `plexctl-pp-cli library metadata-put-split` — Split a metadata item into multiple items
- `plexctl-pp-cli library metadata-put-unmatch` — Unmatch a metadata item to info fetched from the agent
- `plexctl-pp-cli library metadata-put-voice-activity` — Start the detection of voice in a metadata item
- `plexctl-pp-cli library post-file` — This endpoint takes a file path specified in the `url` parameter, matches it using the scanner's match mechanism
- `plexctl-pp-cli library post-section` — Add a new library section to the server
- `plexctl-pp-cli library post-sections-refresh` — Tell PMS to refresh all section metadata
- `plexctl-pp-cli library put-clean-bundles` — Clean out any now unused bundles. Bundles can become unused when media is deleted
- `plexctl-pp-cli library put-optimize` — Initiate optimize on the database.
- `plexctl-pp-cli library put-parts-part` — Set which streams (audio/subtitle) are selected by this user
- `plexctl-pp-cli library put-streams-stream` — Set a stream offset in ms. This may not be respected by all clients
- `plexctl-pp-cli library section-delete-collection-collection` — Delete a library collection from the PMS
- `plexctl-pp-cli library section-delete-indexes` — Delete all the indexes in a section
- `plexctl-pp-cli library section-delete-intros` — Delete all the intro markers in a section
- `plexctl-pp-cli library section-delete-refresh` — Cancel the refresh of a section
- `plexctl-pp-cli library section-get-albums` — Get all albums in a music section
- `plexctl-pp-cli library section-get-all` — Get the items in a section, potentially filtering them
- `plexctl-pp-cli library section-get-all-leaves` — Get all leaves in a section (such as episodes in a show section)
- `plexctl-pp-cli library section-get-arts` — Get artwork for a library section
- `plexctl-pp-cli library section-get-audio-codecs` — Get list of distinct audio codecs found in this library section
- `plexctl-pp-cli library section-get-audio-layouts` — Get list of distinct audio layouts (e.g. stereo, 5.1, 7.1) found in this library section
- `plexctl-pp-cli library section-get-autocomplete` — The field to autocomplete on is specified by the {field}.query parameter. For example `genre.query` or `title.query`.
- `plexctl-pp-cli library section-get-categories` — Get categories in a library section
- `plexctl-pp-cli library section-get-cluster` — Get clusters in a library section (typically for photos)
- `plexctl-pp-cli library section-get-collections` — Get all collections in a section
- `plexctl-pp-cli library section-get-common` — Represents a 'Common' item.
- `plexctl-pp-cli library section-get-composite` — Get a composite image of images in this section
- `plexctl-pp-cli library section-get-compute-path` — Get a list of audio tracks starting at one and ending at another which are similar across the path
- `plexctl-pp-cli library section-get-filters` — Get common filters on a section
- `plexctl-pp-cli library section-get-first-charaters` — Get list of first characters in this section
- `plexctl-pp-cli library section-get-locations` — Get all folder locations of the media in a section
- `plexctl-pp-cli library section-get-moment` — Get moments in a library section (typically for photos)
- `plexctl-pp-cli library section-get-nearest` — Get the nearest audio tracks to a particular analysis
- `plexctl-pp-cli library section-get-prefs` — Get the prefs for a section by id and potentially overriding the agent
- `plexctl-pp-cli library section-get-section` — Returns details for the library.
- `plexctl-pp-cli library section-get-sorts` — Get the sort mechanisms available in a section
- `plexctl-pp-cli library section-get-subtitle-codecs` — Get list of distinct subtitle codecs found in this library section
- `plexctl-pp-cli library section-get-video-codecs` — Get list of distinct video codecs found in this library section
- `plexctl-pp-cli library section-post-refresh` — Start a refresh of this section
- `plexctl-pp-cli library section-put-all` — This endpoint takes an large possible set of values. Here are some examples.
- `plexctl-pp-cli library section-put-analyze` — Start analysis of all items in a section. If BIF generation is enabled, this will also be started on this section
- `plexctl-pp-cli library section-put-empty-trash` — Empty trash in the section, permanently deleting media/metadata for missing media
- `plexctl-pp-cli library section-put-prefs` — Set the prefs for a section by id
- `plexctl-pp-cli library section-put-section` — Edit a library section by id setting parameters

**livetv** — Manage livetv

- `plexctl-pp-cli livetv dvr-delete-dvr` — Delete a single DVR by its id (key)
- `plexctl-pp-cli livetv dvr-delete-dvr-device` — Remove a device from an existing DVR
- `plexctl-pp-cli livetv dvr-delete-lineup` — Deletes a DVR device's lineup.
- `plexctl-pp-cli livetv dvr-delete-reload-guide` — Tell a DVR to stop reloading program guide
- `plexctl-pp-cli livetv dvr-get-dvr` — Get a single DVR by its id (key)
- `plexctl-pp-cli livetv dvr-get-slash` — Get the list of all available DVRs
- `plexctl-pp-cli livetv dvr-post-channels-channel-tune` — Tune a channel on a DVR to the provided channel
- `plexctl-pp-cli livetv dvr-post-reload-guide` — Tell a DVR to reload program guide
- `plexctl-pp-cli livetv dvr-post-slash` — Creation of a DVR, after creation of a devcie and a lineup is selected
- `plexctl-pp-cli livetv dvr-put-dvr-device` — Add a device to an existing DVR
- `plexctl-pp-cli livetv dvr-put-lineup` — Add a lineup to a DVR device's set of lineups.
- `plexctl-pp-cli livetv dvr-put-prefs` — Set DVR preferences by name avd value
- `plexctl-pp-cli livetv epg-get-channelmap` — Compute the best channel map, given device and lineup
- `plexctl-pp-cli livetv epg-get-channels` — Get channels for a lineup within an EPG provider
- `plexctl-pp-cli livetv epg-get-countries` — This endpoint returns a list of countries which EPG data is available for.
- `plexctl-pp-cli livetv epg-get-countries-country-lineups` — Returns a list of lineups for a given country, EPG provider and postal code
- `plexctl-pp-cli livetv epg-get-countries-country-regions` — Get regions for a country within an EPG provider
- `plexctl-pp-cli livetv epg-get-countries-country-regions-region-lineups` — Get lineups for a region within an EPG provider
- `plexctl-pp-cli livetv epg-get-languages` — Returns a list of all possible languages for EPG data.
- `plexctl-pp-cli livetv epg-get-lineup` — Compute the best lineup, given lineup group and device
- `plexctl-pp-cli livetv epg-get-lineupchannels` — Get the channels across multiple lineups
- `plexctl-pp-cli livetv sessions-get-session` — Get a single livetv session and metadata
- `plexctl-pp-cli livetv sessions-get-session-consumer-index` — Get a playlist index for playing this session
- `plexctl-pp-cli livetv sessions-get-session-consumer-segment` — Get a single livetv session segment
- `plexctl-pp-cli livetv sessions-get-slash` — Get all livetv sessions and metadata

**log** — Logging mechanism to allow clients to log to the server

- `plexctl-pp-cli log post-papertrail` — This endpoint will enable all Plex Media Serverlogs to be sent to the Papertrail networked logging site for a period of
- `plexctl-pp-cli log post-slash` — This endpoint will write multiple lines to the main Plex Media Server log in a single request.
- `plexctl-pp-cli log put-slash` — This endpoint will write a single-line log message, including a level and source to the main Plex Media Server log.

**media** — Manage media

- `plexctl-pp-cli media delete-metadata-agent-provider` — Deletes a metadata agent provider with the given id.
- `plexctl-pp-cli media delete-metadata-agent-provider-group` — Deletes a metadata agent provider group with the given id.
- `plexctl-pp-cli media delete-metadata-agent-provider-group-item` — Deletes a metadata agent provider group item with the given id.
- `plexctl-pp-cli media delete-provider` — Deletes a media provider with the given id
- `plexctl-pp-cli media get-metadata-agent-provider` — Get the metadata agent provider with the given id.
- `plexctl-pp-cli media get-metadata-agent-provider-group` — Get the metadata agent provider group with the given id.
- `plexctl-pp-cli media get-metadata-agent-provider-groups` — Get the list of all available metadata agent provider groups for this PMS.
- `plexctl-pp-cli media get-metadata-agent-providers` — Get the list of all available metadata agent providers for this PMS.
- `plexctl-pp-cli media get-providers` — Get the list of all available media providers for this PMS.
- `plexctl-pp-cli media grabber-delete-devices-device-scan` — Tell a device to stop scanning for channels
- `plexctl-pp-cli media grabber-delete-operations-operation` — Cancels an existing media grab (recording).
- `plexctl-pp-cli media grabber-devices-device-delete-slash` — Remove a devices by its id along with its channel mappings
- `plexctl-pp-cli media grabber-devices-device-get-channels` — Get a device's channels by its id
- `plexctl-pp-cli media grabber-devices-device-get-slash` — Get a device's details by its id
- `plexctl-pp-cli media grabber-devices-device-get-thumb-version` — Get a device's thumb for display to the user
- `plexctl-pp-cli media grabber-devices-device-post-scan` — Tell a device to scan for channels
- `plexctl-pp-cli media grabber-devices-device-put-channelmap` — Set a device's channel mapping
- `plexctl-pp-cli media grabber-devices-device-put-prefs` — Set device preferences by its id
- `plexctl-pp-cli media grabber-devices-device-put-slash` — Enable or disable a device by its id
- `plexctl-pp-cli media grabber-get-devices` — Get the list of all devices present
- `plexctl-pp-cli media grabber-get-slash` — Get available grabbers visible to the server
- `plexctl-pp-cli media grabber-post-device-discover` — Tell grabbers to discover devices
- `plexctl-pp-cli media grabber-post-devices` — This endpoint adds a device to an existing grabber. The device is identified, and added to the correct grabber.
- `plexctl-pp-cli media post-metadata-agent-provider-groups` — This endpoint registers a new metadata agent provider group and creates a new MetadataAgentGroupItem for the
- `plexctl-pp-cli media post-metadata-agent-providers` — This endpoint registers a metadata agent provider with the server.
- `plexctl-pp-cli media post-providers` — This endpoint registers a media provider with the server.
- `plexctl-pp-cli media post-providers-refresh` — Refresh all known media providers. This is useful in case a provider has updated features.
- `plexctl-pp-cli media put-metadata-agent-provider` — Modify the metadata agent provider with the given id.
- `plexctl-pp-cli media put-metadata-agent-provider-group` — Modify the metadata agent group with the given id. Only the title can be changed.
- `plexctl-pp-cli media put-metadata-agent-provider-group-item` — Modify a metadata agent provider group's items.
- `plexctl-pp-cli media subscriptions-delete-subscription` — Delete a subscription, cancelling all of its grabs as well
- `plexctl-pp-cli media subscriptions-get-scheduled` — Get all scheduled recordings across all subscriptions
- `plexctl-pp-cli media subscriptions-get-slash` — Get all subscriptions and potentially the grabs too
- `plexctl-pp-cli media subscriptions-get-subscription` — Get a single subscription and potentially the grabs too
- `plexctl-pp-cli media subscriptions-get-template` — Get the templates for a piece of media which could include fetching one airing, season, the whole show, etc.
- `plexctl-pp-cli media subscriptions-post-process` — Process all subscriptions asynchronously
- `plexctl-pp-cli media subscriptions-post-slash` — Create a subscription.
- `plexctl-pp-cli media subscriptions-put-subscription` — Edit a subscription's preferences
- `plexctl-pp-cli media subscriptions-put-subscription-move` — Re-order a subscription to change its priority

**photo** — Manage photo

- `plexctl-pp-cli photo` — Transcode an image, possibly changing format or size

**play-queues** — The playqueue feature within a media provider
A play queue represents the current list of media for playback. Although queues are persisted by the server, they should be regarded by the user as a fairly lightweight, an ephemeral list of items queued up for playback in a session.  There is generally one active queue for each type of media (music, video, photos) that can be added to or destroyed and replaced with a fresh queue.
Play Queues has a region, which we refer to in this doc (partially for historical reasons) as "Up Next". This region is defined by `playQueueLastAddedItemID` existing on the media container. This follows iTunes' terminology. It is a special region after the currently playing item but before the originally-played items. This enables "Party Mode" listening/viewing, where items can be added on-the-fly, and normal queue playback resumed when completed. 
You can visualize the play queue as a sliding window in the complete list of media queued for playback. This model is important when scaling to larger play queues (e.g. shuffling 40,000 audio tracks). The client only needs visibility into small areas of the queue at any given time, and the server can optimize access in this fashion.
All created play queues will have an empty "Up Next" area - unless the item is an album and no `key` is provided. In this case the "Up Next" area will be populated by the contents of the album. This is to allow queueing of multiple albums - since the 'Add to Up Next' will insert after all the tracks. This means that If you're creating a PQ from an album, you can only shuffle it if you set `key`. This is due to the above implicit queueing of albums when no `key` is provided as well as the current limitation that you cannot shuffle a PQ with an "Up Next" area.
The play queue window advances as the server receives timeline requests. The client needs to retrieve the play queue as the “now playing” item changes. There is no play queue API to update the playing item.

- `plexctl-pp-cli play-queues post-slash` — Makes a new play queue for a device. The source of the playqueue can either be a URI, or a playlist.
- `plexctl-pp-cli play-queues queue-get-slash` — Retrieves the play queue, centered at current item.
- `plexctl-pp-cli play-queues queue-put-slash` — Adds an item to a play queue (e.g. party mode). Increments the version of the play queue.

**playlists** — The playlist feature within a media provider
Playlists are ordered collections of media. They can be dumb (just a list of media) or smart (based on a media query, such as "all albums from 2017"). They can be organized in (optionally nesting) folders.
Retrieving a playlist, or its items, will trigger a refresh of its metadata. This may cause the duration and number of items to change.

- `plexctl-pp-cli playlists delete` — Deletes a playlist by provided id
- `plexctl-pp-cli playlists get` — Gets detailed metadata for a playlist.
- `plexctl-pp-cli playlists get-slash` — Gets a list of playlists and playlist folders for a user.
- `plexctl-pp-cli playlists post-slash` — Create a new playlist. By default the playlist is blank.
- `plexctl-pp-cli playlists post-upload` — Imports m3u playlists by passing a path on the server to scan for m3u-formatted playlist files
- `plexctl-pp-cli playlists put` — Edits a playlist in the same manner as [editing metadata](#tag/Provider/operation/metadataPutItem)

**security** — Manage security

- `plexctl-pp-cli security get-resources` — If a caller requires connection details and a transient token for a source that is known to the server
- `plexctl-pp-cli security post-token` — This endpoint provides the caller with a temporary token with the same access level as the caller's token.

**services** — Manage services

- `plexctl-pp-cli services ultra-blur-get-colors` — Retrieves the four colors extracted from an image for clients to use to generate an ultrablur image.
- `plexctl-pp-cli services ultra-blur-get-image` — Retrieves a server-side generated UltraBlur image based on the provided color inputs.

**status** — The status endpoints give you information about current playbacks, play history, and even terminating sessions.

- `plexctl-pp-cli status delete-history` — Delete a single history item by id
- `plexctl-pp-cli status get-background` — Get the list of all background tasks
- `plexctl-pp-cli status get-history` — Get a single history item by id
- `plexctl-pp-cli status get-history-all` — List all playback history (Admin can see all users, others can only see their own).
- `plexctl-pp-cli status get-slash` — List all current playbacks on this server
- `plexctl-pp-cli status post-terminate` — Terminate a playback session kicking off the user

**tv-plex-providers-epg-identifier-device-id** — Manage tv plex providers epg identifier device id

- `plexctl-pp-cli tv-plex-providers-epg-identifier-device-id media-provider-epg-channels` — Get channels for a lineup within an EPG provider
- `plexctl-pp-cli tv-plex-providers-epg-identifier-device-id media-provider-epg-grid` — Get the airing information for a given channel on a given day
- `plexctl-pp-cli tv-plex-providers-epg-identifier-device-id media-provider-epg-watchnow` — Get the watchnow hubs for the specified provider
- `plexctl-pp-cli tv-plex-providers-epg-identifier-device-id media-provider-epg-watchnow-all` — Get the information for all currently airing shows on the specified provider

**updater** — This describes the API for searching and applying updates to the Plex Media Server.
Updates to the status can be observed via the Event API.

- `plexctl-pp-cli updater get-status` — Get the status of updating the server
- `plexctl-pp-cli updater put-apply` — Apply any downloaded updates. Note that the two parameters `tonight` and `skip` are effectively mutually exclusive.
- `plexctl-pp-cli updater put-check` — Perform an update check and potentially download


### Finding the right command

When you know what you want to do but not which command does it, ask the CLI directly:

```bash
plexctl-pp-cli which "<capability in your own words>"
```

`which` resolves a natural-language capability query to the best matching command from this CLI's curated feature index. Exit code `0` means at least one match; exit code `2` means no confident match — fall back to `--help` or use a narrower query.

## Auth Setup
Run `plexctl-pp-cli auth setup` to print the URL and steps for getting a key (add `--launch` to open the URL). Then set:

```bash
export PLEXCTL_USER_TOKEN="<your-key>"
```
To persist credentials, use `echo "$TOKEN" | plexctl-pp-cli auth set-token`. Stored secrets live in `credentials.toml` under the data dir, not in `config.toml`.

Run `plexctl-pp-cli doctor` to verify setup.

## Agent Mode

Add `--agent` to any command. Expands to: `--json --compact --no-input --no-color`.

- **Pipeable** — JSON on stdout, errors on stderr
- **Filterable** — `--select` keeps a subset of fields. Dotted paths descend into nested structures; arrays traverse element-wise. Critical for keeping context small on verbose APIs:

  ```bash
  plexctl-pp-cli identity --agent --select MediaContainer
  ```
- **Previewable** — `--dry-run` shows the request without sending
- **Offline-friendly** — sync/search commands can use the local SQLite store when available
- **Non-interactive** — never prompts, every input is a flag
- **Explicit confirmation** — `--agent` does not imply `--yes`; pass `--yes` separately only after the target, arguments, and side effects are clear
- **Explicit retries** — use `--idempotent` only when an already-existing create should count as success, and use `--ignore-missing` only when a missing delete target should count as success

### Response envelope

Commands that read from the local store or the API wrap output in a provenance envelope:

```json
{
  "meta": {"source": "live" | "local", "synced_at": "...", "reason": "..."},
  "results": <data>
}
```

Parse `.results` for data and `.meta.source` to know whether it's live or local. A human-readable `N results (live)` summary is printed to stderr only when stdout is a terminal AND no machine-format flag (`--json`, `--csv`, `--compact`, `--quiet`, `--plain`, `--select`) is set — piped/agent consumers and explicit-format runs get pure JSON on stdout.

## Paths and state

Agents should treat the CLI's path resolver as part of the runtime contract:

- Use `--home <dir>` for one invocation, or set `PLEXCTL_HOME=<dir>` to relocate all four path kinds under one root.
- Use per-kind env vars only when a specific kind must diverge: `PLEXCTL_CONFIG_DIR`, `PLEXCTL_DATA_DIR`, `PLEXCTL_STATE_DIR`, `PLEXCTL_CACHE_DIR`.
- Resolution order is per-kind env var, `--home`, `PLEXCTL_HOME`, XDG (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, `XDG_CACHE_HOME`), then platform defaults.
- `config` contains settings like `config.toml` and profiles. `data` contains `credentials.toml`, `data.db`, cookies, and auth sidecars. `state` contains persisted queries, jobs, and `teach.log`. `cache` contains regenerable HTTP/cache files.
- Stored secrets live in `credentials.toml` under the data dir. Existing legacy `config.toml` secrets are read for compatibility and leave `config.toml` on the first auth write.
- Run `plexctl-pp-cli doctor --fail-on warn` to surface path and credential-location warnings. `agent-context` exposes a schema v4 `paths` block for agents that need the resolved dirs.
- For MCP, pass relocation through the MCP host config. The MCP binary does not inherit CLI flags:

  ```json
  {
    "mcpServers": {
      "plexctl": {
        "command": "plexctl-pp-mcp",
        "env": {
          "PLEXCTL_HOME": "/srv/plexctl"
        }
      }
    }
  }
  ```

Fleet precedence: an inherited per-kind env var overrides an explicit `--home` for that kind. Use `PLEXCTL_HOME` or per-kind vars as durable fleet levers, and use `--home` only for a single invocation. Relocation is not reversible by unsetting env vars; move files manually before clearing `PLEXCTL_HOME`, or `doctor` will not find credentials left under the former root.

## Automatic learning

This CLI ships a self-capturing learning loop. The CLI does its own bookkeeping: every invocation is journaled locally, a failed flag followed by a corrected retry auto-derives a `flag_alias` candidate, and a `teach` on a query family without a playbook auto-synthesizes a `playbook_candidate` from the session's journal. Your job is judgment only: `recall` first, act on surfaced candidates, `teach` the final answer, `playbook amend` when you observe a correction. You never record failures by hand.

### Step 1: `recall` before any discovery

Before list/search/drill commands on a new user question, run:

```bash
plexctl-pp-cli recall "<user's question>" --agent
```

The response envelope:

```json
{
  "query": "...",
  "normalized": "<normalized form>",
  "query_entities": ["..."],
  "found": true | false,
  "match_score": 0.0,
  "results": [
    { "resource_id": "...", "resource_type": "...", "venue": "...",
      "confidence": 2, "entity_match": "exact|partial|unknown",
      "source": "taught|preseed|pattern", "warnings": ["..."] }
  ],
  "mismatches": [ /* only when --debug-mismatches */ ],
  "warnings": [ /* top-level */ ],
  "candidates": [
    { "id": 12, "class": "flag_alias | playbook_candidate",
      "summary": "...", "sightings": 3, "last_seen": "...",
      "rationale": "...",
      "next_action": ["<trial command>", "plexctl-pp-cli learnings confirm 12"] }
  ],
  "playbook": {
    "query_family": "...",
    "playbook": {
      "steps": [ { "cmd": "<command with {slot} substitution>", "purpose": "..." } ],
      "entity_slots": ["$ENTITY"],
      "expected_tool_calls": 3
    },
    "slots_resolved": { "$ENTITY": { "token": "<live token>", "canonical": "<canonical>" } },
    "notes": "<workarounds + gotchas for this query family>"
  },
  "notes": "<duplicate surface for non-playbook callers>"
}
```

Empty-store short-circuit: if the store has no learnings, playbooks, or candidates yet (recall finds nothing and `learnings list` and `learnings candidates` are both empty), skip recall for the rest of this session instead of taxing every query; resume recall-first once something has been taught.

### Step 2: decision tree

Read `candidates`, `playbook`, `notes`, `results[0]`, and warnings in that order:

```
if Candidates present (warnings include "candidates_present"):
    -> candidates are try-then-confirm, never facts. Follow each candidate's
       two-step next_action verbatim: run the trial command first, then run
       `learnings confirm <id>` only after the trial verified the behavior.
       Reject a wrong candidate with `learnings reject <id>`.
    -> NEVER re-teach something recall surfaced as a candidate; confirm or
       reject that candidate instead of teaching a duplicate.
    -> candidates ride alongside playbooks and resource hits, not instead of
       them; continue with the branches below after acting on them.

if Playbook present:
    -> READ Playbook.notes verbatim FIRST (workarounds + gotchas the CLI surface doesn't expose)
    -> replay Playbook.steps in order, substituting Playbook.slots_resolved entries
       for the entity slot tokens. If a step's slot is unresolved, fall back to
       discovery for that step only.
    -> the Playbook's expected_tool_calls is a budget; if you find yourself running
       materially more, record the divergence via `plexctl-pp-cli playbook amend`
       at end-of-session.

elif Notes present (no Playbook):
    -> read Notes verbatim before any discovery step; they carry known gotchas
       for this query family even when no structured choreography exists yet.

elif Found AND Results[0].EntityMatch == "exact" AND Results[0].Confidence >= 2:
    -> skip discovery; fetch live data for Results[*].ResourceID in parallel

elif Found AND Results[0].EntityMatch == "partial":
    -> candidate hint, NOT a hit; read the resource title to validate before trusting

elif (any row in Mismatches[] when --debug-mismatches was passed):
    -> treat as cold start; the stored learning is for a different entity
       (different canonical resolved from query_entities)

else:  // Found == false, no playbook, no notes
    -> cold start; run discovery normally; teach the answer afterward (Step 4).
       If the family has no playbook yet, that teach auto-synthesizes a
       playbook candidate from this session's journal - you do not need to
       record one by hand.
```

Playbook and Notes are orthogonal to the per-resource path. A recall response can carry both a Playbook AND a `Results[]` hit - use both: the Playbook tells you which choreography to run; the resource hits short-circuit specific steps. Default to skipping `mismatches`; pass `--debug-mismatches` only when investigating cold-start surprises.

Candidate judgment details: `learnings confirm <id>` prints the candidate's full payload before materializing it - check that the printed payload matches the behavior you verified. `learnings reject <id>` tombstones the derivation signature so the same candidate does not resurface. The envelope carries only the few candidates worth acting on now; `plexctl-pp-cli learnings candidates` lists the full open set.

Graceful degradation: if `learnings confirm` is an unknown command, you are driving an older binary - ignore the candidates guidance and follow the rest of the protocol.

### Step 3: always read `warnings`

- `low_confidence`: row exists at `confidence<2`. Treat as a hint, not a skip-discovery hit.
- `resource_not_in_store`: the local store doesn't have the resource the learning points at. The match validator couldn't classify entities — direct-fetch and re-evaluate.
- `cross_alias_match` (per-result): the row was taught under a different alias and matched the live query's canonical via `entity_lookups` (e.g., a "USA" teach satisfying a "United States" recall). Trust the resource_id.
- `similar_shape_different_entity:<canonical>` (top-level): a structurally matching row exists but its canonical entity differs from the live query's. Treated as cold start; the warning carries the conflicting canonical as a hint, but the row is NOT promoted into Results.
- `ambiguous_alias` (top-level): a single query entity resolved to multiple canonicals (e.g., "Cards" → Arizona Cardinals + St. Louis Cardinals). Surface the ambiguity from context before committing to a resource.
- `candidates_present` (top-level): the envelope carries a `candidates` section. Handle it via the candidates branch in Step 2 before anything else.
- `lookup_refresh_available` (top-level): an entity in the query has no lookup row yet, but synced data could provide one. Run `plexctl-pp-cli sync` to refresh entity lookups.
- Top-level `no_learnings_for_query_family`: the table had no rows above the Jaccard floor. Pure cold start.

### Step 4: `teach &` after finalizing your response - always

Teaching is unconditional. After resolving a query the store could not answer, background-teach the final resource mapping - no call-count threshold, no judging whether it was "worth" learning. The teach is the anchor of the loop: it triggers playbook synthesis for a family without a playbook, and same-referent phrasings fold into one family so near-duplicate teaches do not fragment the store. Fire it after assembling your user-facing response but BEFORE emitting it, with a shell `&` so the call returns immediately:

```bash
plexctl-pp-cli teach --query "<user's question>" --resource-type <type> --resource <id1> --resource <id2>
# (append shell `&` to background it)
```

Silent on success. Errors only land in `teach.log` under the resolved state dir. Teach the **most specific** resource - if the user asked a broad question and you walked through parent records to find the specific answer, teach the leaf id, not the parent. The CLI uses seeded `entity_lookups` for cross-alias resolution at recall time, so a teach under one alias (e.g., "Niners") satisfies future queries under another alias (e.g., "49ers", "San Francisco") automatically.

PII rule: teach the structural question with identifiers stripped - never include names, emails, phone numbers, account ids, or other personal identifiers in taught queries or notes. The CLI scans teach queries for obvious email/phone shapes and warns, but does not block; strip before teaching rather than relying on the warning.

### Step 5: playbooks - optional flags, automatic synthesis

You do not need to decide whether a session "deserves" a playbook: a teach on a family without one auto-synthesizes a `playbook_candidate` from the session's journal, and the next session judges it via confirm/reject. Attach explicit playbook flags only when you already hold choreography worth recording verbatim - workarounds the CLI didn't surface (silently-dropped flags, undocumented params, pagination tricks, payload gotchas). Prefer the **integrated one-call form** - record the resource learning and the playbook in the same `teach` invocation:

```bash
# Common case: record both the resource learning AND the playbook in one call.
plexctl-pp-cli teach \
  --query "<user's question>" \
  --resource <id> \
  --playbook-file ~/playbooks/<shape>.json \
  --playbook-notes-file ~/playbooks/<shape>-notes.md
# (append shell `&` to background it)

# Alternate: playbook-only (no resource to record alongside).
plexctl-pp-cli teach-playbook \
  --query "<user's question>" \
  --playbook-file ~/playbooks/<shape>.json \
  --notes-file ~/playbooks/<shape>-notes.md
```

Playbook files are JSON with `steps`, `entity_slots`, `expected_tool_calls`. Notes files are markdown carrying the gotchas verbatim. File-free callers (MCP-only agents) pass the same content inline: `--playbook-json` and `--playbook-notes` on the integrated `teach` form, `--playbook-json` and `--notes` on `teach-playbook`. On the integrated `teach` form, the playbook flags are optional - omit them entirely for a resource-only teach. On the standalone `teach-playbook` form, at least one of the playbook and notes flags must be set; both empty is rejected. Playbooks are keyed on the structural query family (entities stripped) so a recipe taught from one entity-shaped query applies to every other query of the same shape, with `slots_resolved` binding the live query's canonical at recall time.

When you DO find a playbook on a future recall, treat it as ground truth: replay the steps with `slots_resolved` substitutions, skip the discovery that the choreography already documents, and read `notes` before any step.

### Step 6: `playbook amend &` when your debug response identifies a correction

If your debug-protocol response identifies a concrete correction the notes or playbook should know — a workaround, an undocumented endpoint shape, a stale field name, observed schema drift, an empty-payload fallback — fire `playbook amend` BEFORE emitting your user-facing response. Same fire-and-forget posture as `teach`.

```bash
plexctl-pp-cli playbook amend \
  --query "<exact recall query string>" \
  --add-note "<your concrete correction>"
# (append shell `&` to background it)
```

What counts as worth amending: a behavior you OBSERVED this session that future-you would benefit from knowing. Examples worth amending:

- A workaround for a CLI surface that silently drops or misorders a flag.
- An undocumented endpoint shape (response wrapped in `{meta, results}`, payload nested two levels deeper than the docs claim).
- Observed schema drift (a field renamed, an index that shifted between seasons, a category label that the API now returns lower-cased).

What does NOT belong in notes:

- The year-specific or entity-specific answer to the user's question. That's the response, not a learning.
- Per-team / per-athlete / per-row data the playbook already retrieves at runtime.
- Statements that paraphrase what the existing notes already say.

The amend command appends to the family's existing notes with a timestamped marker (`[amend YYYY-MM-DDTHH:MMZ]: <text>`). Multiple amends accumulate; the audit trail is visible. If no playbook exists yet for the family, amend creates a notes-only one (so cold-start corrections still land).

#### PII discipline for amend notes

`playbook amend` notes are designed to potentially flow upstream as shared knowledge in future versions of the Printing Press. Keep them clean of user-identifying content so the upstream-contribution path stays open without retroactive scrubbing:

- **Do NOT embed** paths to user filesystems, personal API keys or tokens, user email addresses, user GitHub handles, or specific query histories tied to a single user.
- **Acceptable**: endpoint shapes, undocumented field names, API gotchas, observed schema drift, workarounds for CLI surfaces, generalizable pagination or retry tactics.

If a correction is only meaningful with user-specific context, it belongs in a personal note, not in the playbook amend.

### Measuring the loop

`plexctl-pp-cli learnings stats` reports recall hit rate, teach-to-reuse, playbook resolution rate, and candidate confirm/reject counts from the local `learn_events` table. Rates are null until they have a denominator; everything stays on this machine. Use it to check whether the loop is earning its keep for this CLI.

### Disabling learning

- `--no-learn` on a single command short-circuits both `recall` and the `teach` write path. Use for deterministic agent flows or tests that must not be affected by accumulated learnings.
- `PLEXCTL_NO_LEARN=true` in the environment globally disables the pipeline.

## Agent Feedback

When you (or the agent) notice something off about this CLI, record it:

```
plexctl-pp-cli feedback "the --since flag is inclusive but docs say exclusive"
plexctl-pp-cli feedback --stdin < notes.txt
plexctl-pp-cli feedback list --json --limit 10
```

Entries are stored locally as `feedback.jsonl` under the resolved data dir. They are never POSTed unless `PLEXCTL_FEEDBACK_ENDPOINT` is set AND either `--send` is passed or `PLEXCTL_FEEDBACK_AUTO_SEND=true`. Default behavior is local-only.

Write what *surprised* you, not a bug report. Short, specific, one line: that is the part that compounds.

## Output Delivery

Every command accepts `--deliver <sink>`. The output goes to the named sink in addition to (or instead of) stdout, so agents can route command results without hand-piping. Three sinks are supported:

| Sink | Effect |
|------|--------|
| `stdout` | Default; write to stdout only |
| `file:<path>` | Atomically write output to `<path>` (tmp + rename) |
| `webhook:<url>` | POST the output body to the URL (`application/json` or `application/x-ndjson` when `--compact`) |

Unknown schemes are refused with a structured error naming the supported set. Webhook failures return non-zero and log the URL + HTTP status on stderr.

## Named Profiles

A profile is a saved set of flag values, reused across invocations. Use it when a scheduled or recurring agent reuses the same saved flags while providing different input each run.

```
plexctl-pp-cli profile save briefing --json
plexctl-pp-cli --profile briefing identity
plexctl-pp-cli profile list --json
plexctl-pp-cli profile show briefing
plexctl-pp-cli profile delete briefing --yes
```

Explicit flags always win over profile values; profile values win over defaults. `agent-context` lists all available profiles under `available_profiles` so introspecting agents discover them at runtime.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Usage error (wrong arguments) |
| 3 | Resource not found |
| 4 | Authentication required |
| 5 | API error (upstream issue) |
| 7 | Rate limited (wait and retry) |
| 10 | Config error |

## Argument Parsing

Parse `$ARGUMENTS`:

1. **Empty, `help`, or `--help`** → show `plexctl-pp-cli --help` output
2. **Starts with `install`** → ends with `mcp` → MCP installation; otherwise → see Prerequisites above
3. **Anything else** → Direct Use (execute as CLI command with `--agent`)

## MCP Server Installation

1. Install the MCP server:
   ```bash
   go install github.com/mvanhorn/printing-press-library/library/media-and-entertainment/plexctl/cmd/plexctl-pp-mcp@latest
   ```
2. Register with Claude Code:
   ```bash
   claude mcp add plexctl-pp-mcp -- plexctl-pp-mcp
   ```
3. Verify: `claude mcp list`

## Direct Use

1. Check if installed: `which plexctl-pp-cli`
   If not found, offer to install (see Prerequisites at the top of this skill).
2. Match the user query to the best command from the Unique Capabilities and Command Reference above.
3. Execute with the `--agent` flag:
   ```bash
   plexctl-pp-cli <command> [subcommand] [args] --agent
   ```
4. If ambiguous, drill into subcommand help: `plexctl-pp-cli <command> --help`.
