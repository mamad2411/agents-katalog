---
name: api-spotify
description: The API documentation and specifications of Spotify Web API
allowed-tools:
  - Read
  - Bash(ls *)
  - Bash(grep *)
  - Bash(find *)
---

# Spotify Web API Documentation

**Version:** 1.0.0 | **Terms of Service:** https://developer.spotify.com/terms/

**Servers:**
- https://api.spotify.com/v1

## API Description

You can use Spotify's Web API to discover music and podcasts, manage your Spotify library, control audio playback, and much more. Browse our available Web API endpoints using the sidebar at left, or via the navigation bar on top of this page on smaller screens.

In order to make successful Web API requests your app will need a valid access token. One can be obtained through <a href="https://developer.spotify.com/documentation/general/guides/authorization-guide/">OAuth 2.0</a>.

The base URI for all Web API requests is `https://api.spotify.com/v1`.

Need help? See our <a href="https://developer.spotify.com/documentation/web-api/guides/">Web API guides</a> for more information, or visit the <a href="https://community.spotify.com/t5/Spotify-for-Developers/bd-p/Spotify_Developer">Spotify for Developers community forum</a> to ask questions and connect with other developers.


## Navigation

Given your goal, read the relevant index.md file links bellow and subsequent file to the endpoints required to achieve your task.
Avoid using `ls` and `grep`, use them only when after the indexes if they did not provide the information required, or if you have to search for a specific pattern.
Only follow markdown links references required to achieve your goal. The less files you read, the better.

Some endpoints are marked as deprecated. Prefer non-deprecated alternatives when available.

Read the following files depending on your current needs:

- [authentication/index.md](./authentication/index.md): Authentication workflows
- [endpoints/index.md](./endpoints/index.md): API endpoints
- [schemas/index.md](./schemas/index.md): Data schemas, only if you need them alone. They are already included in endpoints.
