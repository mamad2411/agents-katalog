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

**Version:** 1.0.0 | **Terms of Service:**
<https://developer.spotify.com/terms/>

**Generated with:**

```sh
openapi2skill tests/assets/spotify.yaml --output-dir examples/api-spotify --force
```

**Servers:**

- <https://api.spotify.com/v1>

## API Description

You can use Spotify's Web API to discover music and podcasts, manage your
Spotify library, control audio playback, and much more. Browse our available Web
API endpoints using the sidebar at left, or via the navigation bar on top of
this page on smaller screens.

In order to make successful Web API requests your app will need a valid access
token. One can be obtained through [OAuth
2.0](https://developer.spotify.com/documentation/general/guides/authorization-guide/).

The base URI for all Web API requests is `https://api.spotify.com/v1`.

Need help? See our [Web API
guides](https://developer.spotify.com/documentation/web-api/guides/) for more
information, or visit the [Spotify for Developers community
forum](https://community.spotify.com/t5/Spotify-for-Developers/bd-p/Spotify_Developer)
to ask questions and connect with other developers.

## Navigation

Given your goal, read the relevant index.md file links bellow and subsequent
file to the endpoints required to achieve your task. Avoid using `ls` and
`grep`, use them only when after the indexes if they did not provide the
information required, or if you have to search for a specific pattern. Only
follow markdown links references required to achieve your goal. The less files
you read, the better.

Some endpoints are marked as deprecated. Prefer non-deprecated alternatives when
available.

Read the following files depending on your current needs:

- [authentication/index.md](./authentication/index.md): Authentication workflows
- [endpoints/index.md](./endpoints/index.md): API endpoints
- [schemas/index.md](./schemas/index.md): Data schemas, only if you need them
  alone. They are already included in endpoints.

## OpenAPI Manifest

The raw OpenAPI manifest is available at [`openapi.yml`](./openapi.yml). It is
provided only for tools that require the raw spec — e.g. generating an SDK, a
Swagger/OpenAPI client, or a fuzzer. Do **not** read it to navigate this API:
the indexed markdown files above contain the same information organized for far
fewer tokens.
