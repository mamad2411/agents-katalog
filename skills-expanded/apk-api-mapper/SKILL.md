---
name: apk-api-mapper
description: >-
  Reverse-engineer and document the network APIs used by an Android APK or JADX project. Trace
  endpoints, clients, authentication, serialization, signing, and multi-step flows from the app's
  primary implementation: use hermes-dec for React Native Hermes bundles, direct source analysis
  for plain JavaScript bundles, dnSpy CLI on Windows or ILSpy CLI on macOS/Linux for .NET MAUI
  assemblies, and JADX for Android-native code and native bridges. Use apktool for resources or
  smali other tools cannot expose. Produce API docs and standalone replay scripts
  suitable for building a client or SDK. Use for requests to map, inspect, or document an APK's
  backend API. Do not use for website-only API mapping.
---

# APK API Mapper

Map the API surface reachable from the target APK closely enough that another agent can implement
a client without reopening the analysis tools. Treat decompiled source as a lead, not ground truth:
confirm ambiguous control flow with callers, cross-references, resources, smali, or managed IL.

Keep the APK and JADX project read-only. Do not rename symbols, edit code, attach the debugger,
rebuild the APK, or install it unless the user asks.

## Choose the primary artifact

Identify the intended APK from its manifest or package tree, then classify the implementation as
Android-native, WebView, React Native, .NET MAUI, Flutter, another embedded runtime, or a mixture.
Follow the layer that owns request construction:

- For React Native, locate its JavaScript bundle (commonly `assets/index.android.bundle`) and
  analyze that first. If it is Hermes bytecode, read [references/hermes.md](references/hermes.md)
  and use hermes-dec as the primary analysis path. If it is plain JavaScript, trace the source
  directly. Use JADX only for Android configuration, app-owned native modules and bridges, JNI, or
  request behavior delegated out of the bundle.
- For .NET MAUI, locate the managed assemblies or assembly store and read
  [references/dotnet-maui.md](references/dotnet-maui.md). Decompile the assemblies with dnSpy CLI
  on Windows and ILSpy CLI (`ilspycmd`) on macOS/Linux, selected by the analysis host OS. Use JADX
  for Android configuration and Java/native bridges, not the managed request implementation.
- For Android-native code, start in JADX.
- For a mixed app, trace each request in its owning layer and follow only the bridges it crosses.
- For other embedded runtimes, inspect their primary artifact when supported; do not infer behavior
  from Java wrappers.

Do not require a full JADX survey before starting bundle or managed assembly analysis. Ask for the
APK path when the primary artifact must be extracted and is not otherwise accessible.

## Use JADX for Android code

JADX MCP implementations expose different tool names. Inspect the available tools and use their
equivalents for:

- manifest, package tree, main application classes, and main activity
- class, method, and field listing/source
- keyword search with package filters and pagination
- cross-references to classes, methods, and fields
- resources, strings, and smali

Do not reload or switch an open project. If native analysis is required and JADX MCP is unavailable
or points at the wrong APK, ask the user to open the APK and enable its MCP integration. If the user
also supplied the APK path, analysis may continue with local tools while the MCP issue remains
documented.

## Build the coverage map

1. Record the application ID, version when available, launcher/application classes, manifest
   components, app-owned packages, and major bundled libraries.
2. Record which implementation layer owns each API area and any bridge into another layer.
3. Inventory shared network clients and configuration before documenting individual endpoints.
   Look for base URLs, build/environment selection, interceptors, authenticators, serializers,
   cookie jars, certificate pinning, retry logic, and token storage/refresh.
4. Search app code and resources for URL schemes/hosts, path fragments, header names, MIME types,
   WebSocket URLs, GraphQL operations, protobuf service names, and common client markers such as
   Retrofit annotations, OkHttp, Volley, Cronet, Apollo, `HttpURLConnection`, `WebView`, `fetch`,
   and `XMLHttpRequest`.
5. Paginate search/list results to exhaustion. Search dependency packages too, but label
   first-party, platform, and third-party telemetry/payment/identity APIs separately.

Use string hits as entry points. Follow cross-references and callers until each request's complete
construction is understood; a URL literal alone is not an endpoint definition.

## Trace every request

For each endpoint, recover:

- resolved base URL, method, path, path/query parameters, body or multipart layout, and content type
- all direct and interceptor-added headers, cookies, auth state, and token refresh behavior
- request and response serializers/models, nullable/default fields, error mapping, and status cases
- pagination, retries, redirects, caching, uploads/downloads, WebSocket or streaming behavior
- where the request is invoked and any ordering or state shared with adjacent calls
- every timestamp, nonce, signature, encryption, compression, or custom encoding step, including
  constants, input order, output encoding, and the exact source method

Prefer app-owned request interfaces and shared client builders over isolated call sites. If JADX
produces incomplete or suspicious source, compare the method's smali. When logic crosses JNI or a
bundled runtime, trace up to that boundary and inspect the relevant artifact instead of guessing.

## Local artifacts

Extract only the artifact needed for the chosen analysis path. Ask for the APK path if it is not
already known.

- An APK is a ZIP archive. Use ordinary ZIP extraction for a raw asset such as a React Native
  bundle.
- Use `apktool d <apk> -o <new-output-dir>` for decoded resources or broad smali searches. Write to
  a new `artifacts/apk/{timestamp}/apktool/` directory; do not use force-overwrite or rebuild.

Check that a required tool exists before invoking it. Do not install missing software without the
user's approval.

## Evidence and confidence

Attach every material claim to an APK source such as `class#method`, a manifest/resource path, a
smali method, a managed assembly/type/method, or a Hermes function/string. Mark endpoints as:

- **confirmed-static**: request construction and reachable call site were traced
- **inferred**: some behavior comes from models, naming, or incomplete control flow
- **candidate**: a string or library surface was found without a reachable request path

Static analysis does not prove that a backend is live or that a response model is current. State
that limitation rather than inventing runtime examples. Never write user credentials or captured
tokens into docs or scripts.

## Deliverables

Write results into the user's target project, not this skill directory. Read
[references/deliverables.md](references/deliverables.md) before creating them.

```text
docs/apis/README.md
docs/apis/{area}.md
scripts/flows/{flow}.py       # only for non-trivial reproducible flows
artifacts/apk/{timestamp}/    # only when local extraction was necessary
```

Update docs as areas become understood. Before finishing, reconcile every discovered endpoint and
candidate with the index, syntax-check replay scripts, and run their offline/self-check path. Do not
send live, mutating, credentialed, or account-affecting requests unless the user authorized that
runtime validation.

## Walls

Write current findings and then ask for help when the remaining behavior depends on unavailable
credentials or device state, an inaccessible APK path/artifact, unsupported native or Flutter AOT
code, anti-tamper behavior, or decompilation too damaged to support a defensible conclusion. Name
the exact missing evidence and the API areas it blocks.
