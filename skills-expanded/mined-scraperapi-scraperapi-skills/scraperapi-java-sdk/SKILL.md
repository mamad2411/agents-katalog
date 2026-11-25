---
name: scraperapi-java-sdk
description: >
  Best-practices reference for the ScraperAPI Java SDK (com.scraperapi:sdk Maven artifact).
  Consult whenever the user is writing, debugging, or reviewing Java code that calls ScraperAPI.
  Use when user asks: "scrape a website with Java and ScraperAPI", "ScraperAPI Java example",
  "how do I add ScraperAPI to my Maven project", "Java ScraperAPI render", "ScraperAPI Java fluent API",
  "ScraperAPI Java premium proxy", "ScraperAPI Java error handling", "ScraperAPI Java retry".
  Covers Maven/Gradle setup, the fluent builder API, all request parameters, the escalation ladder,
  async jobs, structured data calls, error handling, and credit costs.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "☕"
    homepage: https://docs.scraperapi.com/java
---

# ScraperAPI — Java SDK Best Practices

**Requires:** Java 8+ for the SDK, Maven or Gradle, `SCRAPERAPI_API_KEY` environment variable. The samples that call the API directly use `java.net.http` (Java 11+).

## Setup

### Maven

```xml
<dependency>
  <groupId>com.scraperapi</groupId>
  <artifactId>sdk</artifactId>
  <version>1.2</version>
</dependency>
```

### Gradle

```groovy
implementation 'com.scraperapi:sdk:1.2'
```

### Client instantiation

```java
import com.scraperapi.ScraperApiClient;

ScraperApiClient client = new ScraperApiClient(System.getenv("SCRAPERAPI_API_KEY"));
```

Never hardcode the API key. Read it from the environment every time.

## How the SDK Behaves

- **Method names are snake_case**, like the API parameters: `country_code`, `device_type`, `session_number`. There is no `countryCode()` or `sessionNumber()`.
- **`.result()` returns the response body as a `String`, whatever the status code.** It doesn't throw on 401, 403, 429 or 500, and you can't read the status code. It only throws (`kong.unirest.UnirestException`) on timeouts and connection errors.
- **Only six API parameters exist:** `render`, `premium`, `autoparse`, `country_code`, `device_type`, `session_number`. For anything else (`ultra_premium`, `wait_for_selector`, `output_format`, `max_cost`, `screenshot`…), call the API directly. See [Parameters the SDK Doesn't Have](#parameters-the-sdk-doesnt-have).
- **The timeout is 60 seconds by default**, but ScraperAPI can retry for up to 70 seconds, and requests you cancel before then are still charged. Set `.timeout(75_000)` (milliseconds) on every request.
- **`.retry(n)` doesn't retry n times.** Any value above 0 only turns on retries of dropped connections; non-200 responses are never retried. `.retry(0)` turns it off.
- **Each `.result()` call resets Unirest's global configuration.** If your app also uses Unirest, its settings get wiped.

## Basic Usage

The SDK uses a **fluent builder**: `client.get(url)` returns a request, you chain parameters onto it, and `.result()` sends it and blocks until the body comes back.

```java
// Simple GET, returns the body as a String
String html = client.get("https://example.com/").timeout(75_000).result();

// Multiple parameters
String html = client.get("https://example.com/")
    .render(true)
    .country_code("us")
    .timeout(75_000)
    .result();
```

## Decision Guide

| Situation | Approach |
|-----------|---------|
| Single URL, synchronous | `client.get(url).<params>.timeout(75_000).result()` |
| Page loads content via JavaScript | Chain `.render(true)` |
| Site blocks datacenter proxies | Chain `.premium(true)` |
| Toughest anti-bot protection | `apiGet` with `ultra_premium=true` (not in the SDK) |
| Wait for an element, Markdown output, cost cap | `apiGet` with `wait_for_selector`, `output_format`, `max_cost` (not in the SDK) |
| You need the status code | `apiGet` |
| Multi-step / paginated flow on same domain | Chain `.session_number("42")` |
| 20+ URLs or batch jobs | Async endpoint via `HttpClient` |
| Supported platform (Amazon, Google, etc.) | Structured data endpoint |

## Parameter Reference

### Rendering

```java
// Render JavaScript before returning HTML
// Use when: page is a React/Vue/Angular SPA, or initial scrape returns empty content
// Cost: 10 credits per request (instead of 1)
String html = client.get("https://spa-site.com/").render(true).timeout(75_000).result();
```

Don't call `.render(true)` by default — try without it first. It adds cost and latency.
To wait for a DOM element, use `apiGet` with `render=true` and `wait_for_selector`.

### Proxies and Geotargeting

```java
// Route through a country-specific proxy — no extra credit cost
String html = client.get("https://example.com/").country_code("gb").timeout(75_000).result();

// Premium residential/mobile IPs — for sites that block datacenter proxies
// Cost: 10 credits (25 with render)
String html = client.get("https://hard-site.com/").premium(true).timeout(75_000).result();
```

For the toughest anti-bot protections, use `ultra_premium=true` through `apiGet` (30 credits, 75 with render).
`premium` and `ultra_premium` are mutually exclusive — never set both. `ultra_premium` ignores custom headers.
Escalation order: standard (1 cr) → render (10 cr) → premium (10 cr) → ultra_premium (30 cr).

### Sessions (Sticky Proxy)

```java
// Reuse the same proxy IP across requests — useful for pagination and multi-step flows
// Sessions expire 15 minutes after last use. The SDK takes the session ID as a String.
String page1 = client.get("https://example.com/page1").session_number("42").timeout(75_000).result();
String page2 = client.get("https://example.com/page2").session_number("42").timeout(75_000).result();
```

### Headers, Device Type and Autoparse

```java
// Forward a custom header to the target site (the SDK sets keep_headers=true for you)
String html = client.get("https://example.com/").header("Accept-Language", "de-DE").timeout(75_000).result();

// Emulate a mobile browser user-agent
String html = client.get("https://example.com/").device_type("mobile").timeout(75_000).result();

// Return structured JSON for supported sites (Amazon, Google, etc.)
String json = client.get("https://amazon.com/dp/B09V3KXJPB").autoparse(true).timeout(75_000).result();
```

## POST and PUT Requests

```java
// POST a JSON body to the target site through ScraperAPI
String result = client.post("https://example.com/api")
    .header("Content-Type", "application/json")
    .body("{\"key\":\"value\"}")
    .timeout(75_000)
    .result();
```

`client.put(url)` works the same way.

## Parameters the SDK Doesn't Have

Call the API directly with `java.net.http`. This helper URL-encodes every value and returns the whole response, so you can check the status code. The structured, error-handling and escalation samples below reuse it.

```java
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.*;
import java.util.stream.Collectors;

private static final String API_KEY = System.getenv("SCRAPERAPI_API_KEY");
private static final HttpClient HTTP = HttpClient.newHttpClient();

// GET https://api.scraperapi.com/<path>?api_key=...&<params>
public static HttpResponse<String> apiGet(String path, Map<String, String> params) throws Exception {
    Map<String, String> all = new LinkedHashMap<>(params);
    all.put("api_key", API_KEY);
    String query = all.entrySet().stream()
        .map(e -> e.getKey() + "=" + URLEncoder.encode(e.getValue(), StandardCharsets.UTF_8))
        .collect(Collectors.joining("&"));
    HttpRequest req = HttpRequest.newBuilder(URI.create("https://api.scraperapi.com/" + path + "?" + query))
        .timeout(Duration.ofSeconds(75))
        .GET()
        .build();
    return HTTP.send(req, HttpResponse.BodyHandlers.ofString());
}

// Ultra-premium
HttpResponse<String> resp = apiGet("", Map.of("url", "https://hardest-site.com/", "ultra_premium", "true"));

// Render and wait for an element, then return Markdown, never spending more than 10 credits
HttpResponse<String> resp = apiGet("", Map.of(
    "url", "https://spa-site.com/",
    "render", "true",
    "wait_for_selector", ".product-list",
    "output_format", "markdown",
    "max_cost", "10"));
```

## Escalation Ladder

Always start cheapest. Escalate only when the site blocks the previous tier. The SDK hides the status code, so check the body; the last tier goes through `apiGet` because the SDK has no `ultra_premium`.

```java
import com.scraperapi.ScraperApiClient;
import com.scraperapi.ScraperApiRequest;
import kong.unirest.UnirestException;
import java.util.function.Supplier;

public static String scrapeWithEscalation(ScraperApiClient client, String url) throws Exception {
    List<Supplier<ScraperApiRequest>> tiers = Arrays.asList(
        () -> client.get(url),                              // 1 credit
        () -> client.get(url).render(true),                 // 10 credits
        () -> client.get(url).premium(true),                // 10 credits
        () -> client.get(url).premium(true).render(true));  // 25 credits
    for (Supplier<ScraperApiRequest> tier : tiers) {
        try {
            String html = tier.get().timeout(75_000).result();
            if (html != null && html.toLowerCase().contains("<html")) return html;
        } catch (UnirestException e) {
            // Timeout or connection error: try the next tier
        }
    }
    HttpResponse<String> resp = apiGet("", Map.of("url", url, "ultra_premium", "true")); // 30 credits
    return resp.statusCode() == 200 ? resp.body() : null;
}
```

## Async Jobs (for Batches)

`.result()` blocks the calling thread. For 20+ URLs, submit async jobs via the REST endpoint and
collect results concurrently. These use `API_KEY` and `HTTP` from `apiGet` above, plus Jackson
(`com.fasterxml.jackson.core:jackson-databind`).

```java
import com.fasterxml.jackson.databind.ObjectMapper;

private static final ObjectMapper JSON = new ObjectMapper();

public static Map<String, Object> submitJob(String url) throws Exception {
    // without expectUnsuccessReport, a job that fails never reaches "failed"
    String body = JSON.writeValueAsString(Map.of("apiKey", API_KEY, "url", url, "expectUnsuccessReport", true));
    HttpRequest req = HttpRequest.newBuilder()
        .uri(URI.create("https://async.scraperapi.com/jobs"))
        .POST(HttpRequest.BodyPublishers.ofString(body))
        .header("Content-Type", "application/json")
        .build();
    HttpResponse<String> resp = HTTP.send(req, HttpResponse.BodyHandlers.ofString());
    if (resp.statusCode() / 100 != 2)
        throw new RuntimeException("Job submit failed: HTTP " + resp.statusCode() + " " + resp.body());
    return JSON.readValue(resp.body(), Map.class); // {id, statusUrl}
}

public static String pollJob(Map<String, Object> job, int maxWaitSec) throws Exception {
    long deadline = System.currentTimeMillis() + maxWaitSec * 1000L;
    while (System.currentTimeMillis() < deadline) {
        HttpRequest req = HttpRequest.newBuilder()
            .uri(URI.create((String) job.get("statusUrl")))
            .GET().build();
        Map<String, Object> data = JSON.readValue(
            HTTP.send(req, HttpResponse.BodyHandlers.ofString()).body(), Map.class);
        if ("finished".equals(data.get("status")))
            return ((Map<?, ?>) data.get("response")).get("body").toString();
        if ("failed".equals(data.get("status")))
            throw new RuntimeException("Job " + job.get("id") + " failed");
        Thread.sleep(5_000);
    }
    throw new RuntimeException("Job " + job.get("id") + " timed out");
}
```

## Structured Data Endpoints

For supported platforms, use structured endpoints instead of raw HTML scraping.

```java
public static String structuredGet(String vertical, Map<String, String> params) throws Exception {
    HttpResponse<String> resp = apiGet("structured/" + vertical, params);
    if (resp.statusCode() != 200)
        throw new RuntimeException("Error " + resp.statusCode() + ": " + resp.body());
    return resp.body();
}

// Google SERP
String serp = structuredGet("google/search", Map.of("query", "java web scraping"));

// Amazon product
String product = structuredGet("amazon/product", Map.of("asin", "B09V3KXJPB"));

// Walmart search
String items = structuredGet("walmart/search", Map.of("query", "standing desk", "tld", "com"));
```

## Error Handling

`.result()` never tells you the status code, so an invalid key or exhausted credits come back as
an ordinary `String`. When you need to react to errors, use `apiGet` and switch on the status:

```java
public static String safeScrape(String url) throws Exception {
    HttpResponse<String> resp = apiGet("", Map.of("url", url));
    switch (resp.statusCode()) {
        case 200: return resp.body();
        case 401: throw new IllegalStateException("Invalid API key — check SCRAPERAPI_API_KEY");
        case 403: throw new IllegalStateException("Out of API credits for this billing cycle — upgrade or enable overages at https://dashboard.scraperapi.com/billing (don't retry)");
        case 429: throw new RuntimeException("Rate limit — reduce concurrency or use async");
        case 500: case 503:
            throw new RuntimeException("Failed after ScraperAPI retried for 70s (not charged) — retry; on protected sites add premium/ultra_premium");
        default: throw new RuntimeException("Scrape failed with HTTP " + resp.statusCode() + ": " + url);
    }
}
```

`HTTP.send` throws `java.net.http.HttpTimeoutException` if no response arrives within 75 seconds.

Status codes: 200 success, 401 bad key, 403 credits exhausted (don't retry), 404 target not found (charged),
429 concurrency limit, 500 failed after 70s of retries (not charged — retry, then escalate to premium/ultra_premium on protected sites).

## Credit Cost Reference

| Request type | Credits |
|---|---|
| Standard `.result()` | 1 |
| `.render(true)` | 10 |
| `.premium(true)` | 10 |
| `.premium(true).render(true)` | 25 |
| `ultra_premium=true` (`apiGet`) | 30 |
| `ultra_premium=true&render=true` (`apiGet`) | 75 |

Those are the costs on a normal site. Some sites cost more per request, before any parameters:

| Site | Credits |
|---|---|
| Amazon, Walmart, eBay | 5 |
| Google, Bing (all subdomains) | 25 |
| LinkedIn | 30 |
| Sites behind Cloudflare, DataDome, PerimeterX or Akamai | 10 |

You're charged for `200` and `404` responses, and for requests you cancel before ScraperAPI's 70s
of retries finish. Each response's `sa-credit-cost` header shows what it cost; preview a cost
without spending credits with `GET https://api.scraperapi.com/account/urlcost?api_key=...&url=...`
(it accepts the same parameters). Source: https://docs.scraperapi.com/getting-started/quick-start/credits-and-requests-costs

## Documentation

- [Java SDK getting started](https://docs.scraperapi.com/java)
- [SDK method reference](https://docs.scraperapi.com/java/making-requests/sdk-method)
- [JavaScript rendering](https://docs.scraperapi.com/java/making-requests/customizing-requests/rendering-javascript)
- [Premium proxy pools](https://docs.scraperapi.com/java/making-requests/customizing-requests/premium-residential-mobile-proxy-pools)
- [Autoparse / JSON response](https://docs.scraperapi.com/java/handling-and-processing-responses/output-formats/json-response-autoparse)
- [Callbacks (async)](https://docs.scraperapi.com/java/making-requests/async-requests-method/callbacks)
- [Dashboard & credits](https://dashboard.scraperapi.com/)
