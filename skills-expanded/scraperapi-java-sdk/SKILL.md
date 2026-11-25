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

**Requires:** Java 8+, Maven or Gradle, `SCRAPERAPI_API_KEY` environment variable.

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

## Basic Usage

The Java SDK uses a **fluent builder** pattern. Chain parameter methods onto the result of `.get()`, then call `.result()` to block and retrieve the HTML.

```java
// Simple GET — returns HTML as a String
String html = client.get("https://example.com/").result();

// With parameters — chain before .result()
String html = client.get("https://example.com/")
    .render(true)
    .result();

// Multiple parameters
String html = client.get("https://example.com/")
    .render(true)
    .countryCode("us")
    .result();
```

## Decision Guide

| Situation | Approach |
|-----------|---------|
| Single URL, synchronous | `.get(url).<params>.result()` |
| Page loads content via JavaScript | Chain `.render(true)` |
| Site blocks datacenter proxies | Chain `.premium(true)` |
| Toughest anti-bot protection | Chain `.ultraPremium(true)` |
| Multi-step / paginated flow on same domain | Chain `.sessionNumber(n)` |
| Transient failures expected | Chain `.retry(n)` |
| 20+ URLs or batch jobs | Async endpoint via `HttpClient` |
| Supported platform (Amazon, Google, etc.) | Structured data endpoint |

## Parameter Reference

### Rendering

```java
// Render JavaScript before returning HTML
// Use when: page is a React/Vue/Angular SPA, or initial scrape returns empty content
// Cost: +10 credits
String html = client.get("https://spa-site.com/").render(true).result();

// Wait for a DOM element before capturing (requires render)
String html = client.get("https://spa-site.com/")
    .render(true)
    .waitForSelector(".product-list")
    .result();
```

Don't call `.render(true)` by default — try without it first. It adds cost and latency.

### Proxies and Geotargeting

```java
// Route through a country-specific proxy — no extra credit cost
String html = client.get("https://example.com/").countryCode("gb").result();

// Premium residential/mobile IPs — for sites that block datacenter proxies
// Cost: 10 credits (25 with render)
String html = client.get("https://hard-site.com/").premium(true).result();

// Ultra-premium — for the toughest anti-bot protections
// Cost: 30 credits (75 with render)
// Note: incompatible with custom headers
String html = client.get("https://hardest-site.com/").ultraPremium(true).result();
```

`premium` and `ultraPremium` are mutually exclusive — never chain both.
Escalation order: standard (1 cr) → render (10 cr) → premium (10 cr) → ultraPremium (30 cr).

### Sessions (Sticky Proxy)

```java
// Reuse the same proxy IP across requests — useful for pagination and multi-step flows
// Sessions expire 15 minutes after last use; any integer is a valid ID
String page1 = client.get("https://example.com/page1").sessionNumber(42).result();
String page2 = client.get("https://example.com/page2").sessionNumber(42).result();
```

### Device Type and Autoparse

```java
// Emulate a mobile browser user-agent
String html = client.get("https://example.com/").deviceType("mobile").result();

// Return structured JSON for supported sites (Amazon, Google, etc.)
String json = client.get("https://amazon.com/dp/B09V3KXJPB").autoparse(true).result();
```

### Retry

```java
// Override the default retry count (default: 3)
// ScraperAPI retries failed requests for up to 70 seconds internally;
// .retry() controls how many times the SDK retries after a non-200 response
String html = client.get("https://flaky-site.com/").retry(5).result();
```

Do not set very low timeouts — the SDK defaults are calibrated to allow ScraperAPI's internal retry
window (up to 70 seconds). Setting a 5-second client timeout will cause false failures.

## Escalation Ladder

Always start cheapest. Escalate only when the site blocks the previous tier.

```java
public static String scrapeWithEscalation(ScraperApiClient client, String url) throws Exception {
    // Try each tier in order — stop at the first success
    String[][] tiers = {
        {},                                  // 1 credit — standard
        {"render:true"},                     // 10 credits
        {"premium:true"},                    // 10 credits
        {"premium:true", "render:true"},     // 25 credits
        {"ultraPremium:true"},               // 30 credits
    };

    // Practical implementation — explicit tier cascade
    String[] attempts = { "standard", "render", "premium", "premiumRender", "ultraPremium" };
    for (String tier : attempts) {
        try {
            var req = client.get(url);
            switch (tier) {
                case "render":       req = req.render(true); break;
                case "premium":      req = req.premium(true); break;
                case "premiumRender": req = req.premium(true).render(true); break;
                case "ultraPremium": req = req.ultraPremium(true); break;
            }
            String html = req.result();
            if (html != null && html.toLowerCase().contains("<html")) return html;
        } catch (Exception e) {
            // Log and try next tier
        }
    }
    return null;
}
```

## Async Jobs (for Batches)

`.result()` blocks the calling thread. For 20+ URLs, submit async jobs via the REST endpoint and
collect results concurrently.

```java
import java.net.http.*;
import java.net.URI;
import com.fasterxml.jackson.databind.ObjectMapper;

private static final String API_KEY = System.getenv("SCRAPERAPI_API_KEY");
private static final HttpClient HTTP = HttpClient.newHttpClient();
private static final ObjectMapper JSON = new ObjectMapper();

public static Map<String, Object> submitJob(String url) throws Exception {
    String body = JSON.writeValueAsString(Map.of("apiKey", API_KEY, "url", url));
    HttpRequest req = HttpRequest.newBuilder()
        .uri(URI.create("https://async.scraperapi.com/jobs"))
        .POST(HttpRequest.BodyPublishers.ofString(body))
        .header("Content-Type", "application/json")
        .build();
    HttpResponse<String> resp = HTTP.send(req, HttpResponse.BodyHandlers.ofString());
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
    StringBuilder query = new StringBuilder("api_key=" + API_KEY);
    params.forEach((k, v) -> query.append("&").append(k).append("=").append(v));
    URI uri = URI.create("https://api.scraperapi.com/structured/" + vertical + "?" + query);
    HttpRequest req = HttpRequest.newBuilder().uri(uri).GET().build();
    HttpResponse<String> resp = HTTP.send(req, HttpResponse.BodyHandlers.ofString());
    if (resp.statusCode() != 200)
        throw new RuntimeException("Error " + resp.statusCode());
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

```java
public static String safeScrape(ScraperApiClient client, String url) {
    try {
        return client.get(url).retry(3).result();
    } catch (Exception e) {
        String msg = e.getMessage() != null ? e.getMessage() : "";
        if (msg.contains("401")) throw new RuntimeException("Invalid API key — check SCRAPERAPI_API_KEY", e);
        if (msg.contains("403")) throw new RuntimeException("Blocked or out of credits — try premium/ultraPremium", e);
        if (msg.contains("429")) throw new RuntimeException("Rate limit — reduce concurrency or use async", e);
        if (msg.contains("500") || msg.contains("503"))
            throw new RuntimeException("Transient error — retry with backoff", e);
        throw new RuntimeException("Scrape failed: " + url, e);
    }
}
```

Status codes: 200 success, 401 bad key, 403 blocked/no credits, 404 target not found,
429 rate limit, 500/503 transient (not charged — safe to retry with backoff).

## Credit Cost Reference

| Request type | Credits |
|---|---|
| Standard `.result()` | 1 |
| `.render(true)` | 10 |
| `.premium(true)` | 10 |
| `.premium(true).render(true)` | 25 |
| `.ultraPremium(true)` | 30 |
| `.ultraPremium(true).render(true)` | 75 |

## Documentation

- [Java SDK getting started](https://docs.scraperapi.com/java)
- [SDK method reference](https://docs.scraperapi.com/java/making-requests/sdk-method)
- [JavaScript rendering](https://docs.scraperapi.com/java/making-requests/customizing-requests/rendering-javascript)
- [Premium proxy pools](https://docs.scraperapi.com/java/making-requests/customizing-requests/premium-residential-mobile-proxy-pools)
- [Autoparse / JSON response](https://docs.scraperapi.com/java/handling-and-processing-responses/output-formats/json-response-autoparse)
- [Callbacks (async)](https://docs.scraperapi.com/java/making-requests/async-requests-method/callbacks)
- [Dashboard & credits](https://dashboard.scraperapi.com/)
