---
name: extension-http-outcalls
description: HTTP outcalls performed by the backend canister (not in the frontend), including mandatory local verification of external REST API requests.
version: 0.1.9
compatibility:
  mops:
    caffeineai-http-outcalls: "~0.1.4"
caffeineai-subscription: [none]
---

# HTTP Outcalls
HTTP outcalls extension for [Caffeine AI](https://caffeine.ai?utm_source=caffeine-skill&utm_medium=referral).

## Overview

This skill covers the requirements for HTTP requests from the backend canister,
including GET, HEAD, POST, PUT, DELETE, and PATCH. Use it whenever integrating
with an external API or service.

## Critical requirements

Follow these rules:
- **MUST use a provider-enforced bounded API request.** The request must limit
  the response by identifier, pagination, time range, geographic area, result
  count, or another server-side bound appropriate to the feature.
  Limit each response to both at most 10_000 entries and at most 1 MB, then
  paginate if needed.
- **MUST pick the bound that matches the feature.** The five bounds are not
  interchangeable. When the feature looks up one entity by something the user
  supplies — a flight number, an order id, a ticker, a postcode — the
  identifier bound is the only correct choice. Paginating a collection to find
  that entity is the anti-pattern, not an alternative: the work still scales
  with the whole collection no matter how small each page is. Pagination is for
  a list the user deliberately pages through, not for searching.
- **MUST put every bound in the actual Motoko http request.** A bound used only by a
  local test does not protect the canister.
- **NEVER fetch an unbounded collection and filter it in the canister.**
  Expected response size, typical traffic, or a currently small dataset is not
  a bound.
- **MUST reject the API or narrow the feature if the provider cannot enforce a
  response bound and supply the required data.** Do not implement a knowingly
  unsafe fallback.
- **Test locally against curl implementation.** Ensure the 1:1 curl call succeeds
  and returns every field the app consumes. When Motoko code changes, redo the
  local curl test.
- **Check the bounds with `check_canister_api_compliance`.** It probes the
  endpoint and measures the response against those limits, and it runs behind
  the deploy gate, so an endpoint it refuses cannot ship.

The 1 MB and 10_000-entry limits above are the module's own ceilings —
`defaultMaxResponseBytes` is 1 MB — and `check_canister_api_compliance` measures
against exactly those two numbers. It refuses earlier than they do: when the URL
carries no server-side bound, it blocks as soon as the probed response is
already past a quarter of the byte ceiling or past 1_000 entries. That band is
the dangerous one, because it passes a one-off curl and then grows until the
canister exceeds its per-message instruction budget parsing the payload. Design
to the stricter bound: bound the request server-side.

## Choosing the wrong bound

A flight lookup takes a flight number and must return one aircraft. Fetching
`https://opensky-network.org/api/states/all` — every aircraft airborne
worldwide, roughly 10-13k rows — and scanning the parsed result in Motoko for
the one callsign is wrong. The canister downloads and parses every record in
the world to answer a single lookup, and the message is rejected:
`IC0522: Canister exceeded the limit of 40000000000 instructions for single
message execution`. Nothing about the code looks wrong — the URL is valid, the
parse compiles, and a one-off curl returns 200.

That is an instruction limit, not a byte limit. Reaching for a smaller page
size does not help: the canister still walks the whole collection to find one
row.

The provider already offered the right bound. `?icao24=<hex>` on the same
endpoint is the identifier bound: kilobytes, one aircraft, one record to parse.

# Backend

For HTTP outcalls that must be performed in the backend:

The existing module `mo:caffeineai-http-outcalls/outcall.mo` provides a generic
bounded request function for every HTTP method supported by the IC, plus
backward-compatible GET and POST helpers.

```mo:caffeineai-http-outcalls/outcall
module {
  public type TransformationInput = {
    context : Blob;
    response : IC.HttpRequestResult;
  };
  public type TransformationOutput = IC.HttpRequestResult;
  public type Transform = query TransformationInput -> async TransformationOutput;
  public type Header = {
    name: Text;
    value: Text;
  };
  public type Method = {
    #get;
    #head;
    #post;
    #put;
    #delete;
    #patch;
  };
  public type Request = {
    url : Text;
    method : Method;
    headers : [Header];
    body : ?Blob;
    maxResponseBytes : Nat64;
    transform : Transform;
  };
  public type Response = IC.HttpRequestResult;
  public let defaultMaxResponseBytes : Nat64;

  // Helper function for the transform callback used by the IC on HTTP outcalls.
  public func transform(input : TransformationInput) : TransformationOutput;

  // Generic bounded request supporting GET, HEAD, POST, PUT, DELETE, and PATCH.
  public func httpRequest(request : Request) : async Response;

  // HTTP GET request with a transform callback function.
  public func httpGetRequest(url : Text, extraHeaders: [Header], transform : Transform) : async Text;

  // HTTP POST request, specifying a transform callback.
  public func httpPostRequest(url : Text, extraHeaders: [Header], body : Text, transform : Transform) : async Text;
};
```

Use `httpRequest` when the status, headers, a custom response limit, or a method
other than GET or POST is needed. `maxResponseBytes` may set a lower limit; the
module caps every request at `defaultMaxResponseBytes` (1 MB). The module
executes every HTTP outcall with `is_replicated = ?false`; callers cannot enable
replicated execution. The backward-compatible helper stays the shortest path for
a simple GET:

```motoko filepath=src/backend/main.mo
import Text "mo:core/Text";
import OutCall "mo:caffeineai-http-outcalls/outcall";

actor {
  public query func transform(input: OutCall.TransformationInput) : async OutCall.TransformationOutput {
    OutCall.transform(input);
  };

  func setItemActive() : async OutCall.Response {
    await OutCall.httpRequest({
      url = "https://api.example.com/items/123";
      method = #patch;
      headers = [{ name = "Content-Type"; value = "application/json" }];
      body = ?("{\"active\":true}".encodeUtf8());
      maxResponseBytes = 100_000;
      transform;
    });
  };

  func makeGetOutcall(url: Text) : async Text {
    await OutCall.httpGetRequest(url, [], transform);
  };
};
```

POST usage through `httpPostRequest` is analogous.

## Verify every external API request

Before considering an HTTP outcall complete, execute the equivalent request
locally with `curl`. Do not rely only on remembered API documentation or on the
Motoko code compiling. Every check below is required. If any check fails, the
HTTP outcall is incomplete and MUST NOT proceed to deployment.

1. **MUST test the exact request implemented in Motoko:** the same HTTP method,
   API version, endpoint path, query parameters, headers, and body. Testing a
   related endpoint or adding parameters that the implementation does not use
   is not valid verification.
2. **MUST trace one representative user input end to end** through every
   conversion into the API request, then test the exact resulting request. For
   example, if the user enters one identifier but the provider expects another
   identifier format, verify that mapping end to end. Calling only the
   provider's base or listing endpoint is insufficient.
3. **MUST validate the consumed response contract.** Run the request with
   `curl --fail-with-body --silent --show-error`. Verify
   the successful status plus every response field and type consumed by the
   app. A response that is merely valid JSON is not sufficient.
4. **MUST run `check_canister_api_compliance` on the exact URL and method the
   implementation uses.** It measures the response against the outcall byte
   ceiling and entry bound and reports whether the URL is bounded server-side,
   mechanically and behind the deploy gate, so an outcall to a host it never
   cleared cannot ship. When it refuses an endpoint, choose a compatible public
   API or narrow the feature honestly; do not implement an unbounded fetch-all
   request and filter it in the canister.

Response bounds are that check's job, not curl's. The checks above are the ones
it cannot do for you: it probes the endpoint, not the app, so it never learns
which response fields the app reads or what the user typed to produce the URL.

If the request fails or any check above is unmet, inspect the status and
response body. Check the provider's current official API documentation and
release or migration notes with web search. Confirm the current API version,
endpoint, parameter names and formats, required headers, and request body. Do
not guess around failures. Fix the Motoko request to match the working REST
request and rerun `curl`; repeat until all checks pass, then rerun the backend
checks. Never report completion while any required check is missing or failed.

Typical failure clues: `400` indicates invalid parameters or body shape;
`404`/`410` often indicates an obsolete endpoint or API version; `405`
indicates the wrong method; and `415` indicates the wrong content type. Treat
`429` and `5xx` responses as quota or provider availability issues only after
confirming the request against current official documentation.
