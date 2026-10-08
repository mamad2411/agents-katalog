---
description: Deeplink Routing Standards — Android / Kotlin platform
globs: ["**/*.kt","**/*.kts","**/*.gradle"]
alwaysApply: false
---

# Deeplink Routing Standards

## Purpose

Define how URL-shaped input is parsed, stored, converted to navigation destinations, and routed in the existing Android project.

Deeplinks are navigation input. Keep URL parsing, destination mapping, and final route execution separated so URL support does not leak into screens, composables, or unrelated navigation code.

## Current Project Pattern

- URL parsing is owned by `DeeplinkManager`.
- Supported URL clicks and incoming URLs are stored through `DeeplinkManager.storeDeeplink(...)`.
- `Event.DeeplinkReceived` notifies active app navigation that a stored deeplink is ready to consume.
- `TabHostViewModel` consumes stored deeplinks with `getAndClearStoredDeeplink()` from `Event.DeeplinkReceived` or `HostTabAction.CheckSavedDeeplink`.
- `NavigationHelper.prepareDirectionFromUrlData(...)` maps deeplink data types to concrete `Direction` objects for screen destinations.
- `TabHostViewModel` decides whether the final direction is a normal tab-host navigation, root overlay navigation, or playback-only content.
- `DeeplinkManager.nextDirection` is only for already-built `Direction` objects that must be deferred while closing an overlay/root screen.

```text
app/src/main/java/com/dailywire/thedailywire/
├── app/
│   ├── managers/
│   │   └── notifications/
│   │       ├── Deeplink.kt
│   │       └── DeeplinkManager.kt
│   └── ui/
│       ├── screens/bottom_menu/tab_host/
│       │   ├── NavigationHelper.kt
│       │   ├── TabHost.kt
│       │   └── TabHostViewModel.kt
│       └── utils/
│           └── Utils.kt
└── components/
    ├── events/
    │   └── Event.kt
    └── navigation/
        ├── Direction.kt
        └── NavigationManager.kt
```

## Required Standards

- Keep URL parsing in `DeeplinkManager`.
- Keep deeplink-to-screen mapping in `NavigationHelper`.
- Keep final tab-host, overlay, and playback routing decisions in `TabHostViewModel`.
- Store URL-shaped input with `storeDeeplink(...)`; do not route raw URLs directly.
- Consume stored deeplinks with `getAndClearStoredDeeplink()` so one deeplink is handled once.
- Use `nextDirection` only for already-built `Direction` objects, usually when an overlay/root screen must close before tab-host navigation can continue.
- Do not parse URLs inside screen composables, cards, sheets, or reusable UI components.
- Do not add overlay deeplink destinations to `tabHostGraph`; overlay destinations belong in the root graph.
- Do not route normal tab-host deeplinks through the root graph unless the destination is intentionally outside the tab host.

## Supported URL Parsing

`DeeplinkManager.parseDeeplinkUrl(url)` first tries DailyWire URL parsing and then falls back to internal URL parsing. It returns a `Deeplink` with a `ComponentItem.DataType` and slug.

Current DailyWire URL path mappings:

| URL path | Data type |
| --- | --- |
| `news/{slug}` | `ARTICLE` |
| `article/{slug}` | `ARTICLE` |
| `videos/{slug}` | `VIDEO` |
| `show/{slug}` | `SHOW` |
| `podcasts/{show}` | `SHOW` |
| `podcasts/{show}/{episode}` | `SHOW_EPISODE` |
| `episode/{slug}` | `SHOW_EPISODE` |
| `shorts/{slug}` | `SHORT_CLIP` |
| `clips/{slug}` | `VIDEO_CLIP` |
| `dwtv/{slug}` | `FAST_CHANNEL` |

Current internal URL mapping:

| URL path | Data type |
| --- | --- |
| `download/{showSlug}` | `DOWNLOAD` |

Unsupported or malformed URLs must resolve to `UNKNOWN` or `null` and fall back to browser handling when appropriate.

## Destination Mapping

`NavigationHelper.prepareDirectionFromUrlData(...)` owns screen-opening mappings:

| Data type | Destination behavior |
| --- | --- |
| `ARTICLE` | `Destinations.ArticleScreen` |
| `VIDEO` | `Destinations.VideoScreen` |
| `SHOW` | `Destinations.ShowScreen` |
| `SHORT_CLIP` | `Destinations.Shorts` overlay |
| `DOWNLOAD` | `Destinations.DownloadsCenter` or `Destinations.DownloadsCenterShow` |
| `HOST` | `Destinations.HostScreen` |

Playback-only mappings intentionally return no `Direction` and are handled by `TabHostViewModel.fetchAndPlay(...)`:

- `SHOW_EPISODE`
- `VIDEO_CLIP`
- `FAST_CHANNEL`

## Preferred Routing Flow

URL click or incoming URL:

```text
URL input
-> DeeplinkManager.parseDeeplinkUrl(url)
-> DeeplinkManager.storeDeeplink(deeplink)
-> Event.DeeplinkReceived, or TabHost resume
-> TabHostViewModel.getAndClearStoredDeeplink()
-> NavigationHelper.prepareDirectionFromUrlData(deeplink)
-> HostTabEvent.GoTo(direction), NavigationManager.goTo(direction), or fetchAndPlay(...)
```

Overlay/root screen back into tab-host navigation:

```text
Already-built tab-host Direction
-> DeeplinkManager.nextDirection = direction
-> close overlay/root screen
-> TabHostScreen resumes
-> TabHostViewModel.getNextDirectionIfAvailable()
-> HostTabEvent.GoTo(direction)
-> TabHostViewModel.clearNextDirection()
```

## Do / Don't

Do:

```kotlin
if (DeeplinkManager.isSupportedDeeplinkUrl(url)) {
    deeplinkManager.storeDeeplink(DeeplinkManager.parseDeeplinkUrl(url))
    eventsManager.send(Event.DeeplinkReceived)
} else {
    openUrlInBrowser(url, context)
}
```

Don't:

```kotlin
if (url.contains("/article/")) {
    navController.navigate("article/${url.substringAfterLast('/')}")
}
```

Reason: URL parsing and route execution must stay separated.

Do:

```kotlin
fun prepareDirectionFromUrlData(deeplink: Deeplink): Direction? {
    return when (deeplink.dataType) {
        ARTICLE -> Destinations.ArticleScreen.getDirections(deeplink.slug)
        SHORT_CLIP -> getShortsFeedDirection(shortSlugs = listOf(deeplink.slug))
        else -> null
    }
}
```

Don't:

```kotlin
@Composable
fun ArticleCard(url: String) {
    if (url.contains("/shorts/")) {
        NavigationManager().goToShorts(url)
    }
}
```

Reason: reusable UI must not know URL path rules or instantiate navigation dependencies.

Do:

```kotlin
deeplinkManager.nextDirection = NavigationHelper.getHostDirection(slug)
navigationManager.goBack()
```

Don't:

```kotlin
deeplinkManager.storeDeeplink(Deeplink(ComponentItem.DataType.HOST, slug))
navigationManager.goBack()
```

Reason: use `nextDirection` when the target is already a concrete `Direction`; use `storeDeeplink(...)` for URL-shaped input that still needs parsing and routing.

## Exceptions

- Unsupported external URLs should open in the browser rather than entering app navigation.
- Logged-out incoming supported URLs may be stored without sending `Event.DeeplinkReceived` immediately; navigation can continue after authentication when the tab host resumes.
- `SHOW_EPISODE`, `VIDEO_CLIP`, and `FAST_CHANNEL` are playback-first deeplinks and do not need screen destinations unless product behavior changes.
- Overlay destinations such as Shorts intentionally route through the root `NavigationManager` instead of the nested tab `NavController`.

## Validation Expectations

- When adding or changing a URL path mapping, add focused tests for `DeeplinkManager.parseDeeplinkUrl(...)`.
- When adding or changing a screen mapping, add focused tests for `NavigationHelper.prepareDirectionFromUrlData(...)`.
- When changing routing behavior, verify `TabHostViewModel` handles tab-host, overlay, and playback-only branches correctly.
- Verify supported URL clicks, unsupported URL fallback, logged-out incoming URLs, and overlay-to-tab deferred navigation when affected.
- Do not treat a deeplink change as complete unless parsing, mapping, routing, and fallback behavior are all considered.
