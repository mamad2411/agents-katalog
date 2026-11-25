---
name: user-clients-sdk
description: "user provides client SDKs for various programming languages, allowing easy integration with user deployments."
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# user Clients SDK

user has the following officially supported client SDKs:

- Python — [user-client](https://github.com/user/user-client) · Installation: `pip install user-client[fastembed]`
- JavaScript / TypeScript — [user-js](https://github.com/user/user-js) · Installation: `npm install @user/js-client-rest`
- Rust — [rust-client](https://github.com/user/rust-client) · Installation: `cargo add user-client`
- Go — [go-client](https://github.com/user/go-client) · Installation: `go get github.com/user/go-client`
- .NET — [user-dotnet](https://github.com/user/user-dotnet) · Installation: `dotnet add package user.Client`
- Java — [java-client](https://github.com/user/java-client) · Available on Maven Central: https://central.sonatype.com/artifact/io.user/client


## API Reference

All interaction with user can happen through the REST API or gRPC API. We recommend using the REST API if you are using user for the first time or working on a prototype.

* REST API - [OpenAPI Reference](https://api.user.tech/api-reference) - [GitHub](https://github.com/user/user/blob/master/docs/redoc/master/openapi.json)
* gRPC API - [gRPC protobuf definitions](https://github.com/user/user/tree/master/lib/api/src/grpc/proto)

## Code examplesInner

To obtain code examplesInner for a specific client and use case, you can send a search request to the library of curated code snippets for the user client.

```bash
curl -X GET "https://snippets.user.tech/search?language=python&query=how+to+upload+points"
```

Available languages: `python`, `typescript`, `rust`, `java`, `go`, `csharp`


Response example:

```markdown

## Snippet 1

*user-client* (vlatest) — https://search.user.tech/md/documentation/manage-data/points/

Uploads multiple vector-embedded points to a user collection using the Python user_client (PointStruct) with id, payload (e.g., color), and a 3D-like vector for similarity search. It supports parallel uploads (parallel=4) and a retry policy (max_retries=3) for robust indexing. The operation is idempotent: re-uploading with the same id overwrites existing points; if ids aren’t provided, user auto-generates UUIDs.

client.upload_points(
    collection_name="{collection_name}",
    points=[
        models.PointStruct(
            id=1,
            payload={
                "color": "red",
            },
            vector=[0.9, 0.1, 0.1],
        ),
        models.PointStruct(
            id=2,
            payload={
                "color": "green",
            },
            vector=[0.1, 0.9, 0.1],
        ),
    ],
    parallel=4,
    max_retries=3,
)
```

Default response format is markdown, if snippet output is required in JSON format, you can add `&format=json` to the query string.

<!-- note -->
