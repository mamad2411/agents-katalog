---
name: scraperapi-php-sdk
description: >
  Best-practices reference for the ScraperAPI PHP SDK (scraperapi/sdk Composer package).
  Consult whenever the user is writing, debugging, or reviewing PHP code that calls ScraperAPI.
  Use when user asks: "scrape a website with PHP and ScraperAPI", "ScraperAPI PHP example",
  "how do I use the ScraperAPI PHP SDK", "PHP ScraperAPI render", "ScraperAPI PHP premium proxy",
  "ScraperAPI PHP Composer install", "ScraperAPI PHP error handling". Covers Composer setup,
  all request parameters, the escalation ladder, POST requests, error handling, and credit costs.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "🐘"
    homepage: https://docs.scraperapi.com/php
---

# ScraperAPI — PHP SDK Best Practices

**Requires:** PHP 7.0+, Composer, `composer require scraperapi/sdk`, `SCRAPERAPI_API_KEY` environment variable.

## Setup

```php
<?php
require __DIR__ . '/vendor/autoload.php';
use ScraperAPI\Client;

$client = new Client(getenv('SCRAPERAPI_API_KEY'));
```

Never hardcode the API key. Read it from the environment every time.

## Basic Usage

```php
// Simple GET — returns HTML string via ->raw_body
$html = $client->get("https://example.com/")->raw_body;
echo $html;

// With a single parameter
$html = $client->get("https://example.com/", ["render" => true])->raw_body;

// With multiple parameters
$html = $client->get(
    "https://example.com/",
    [
        "render"       => true,
        "country_code" => "us",
    ]
)->raw_body;
```

Parameters are passed as an associative array. `->raw_body` extracts the HTML string from the response object.

## Decision Guide

| Situation | Approach |
|-----------|---------|
| Single URL, synchronous | `$client->get($url, $params)->raw_body` |
| Page loads content via JavaScript | Add `"render" => true` |
| Site blocks datacenter proxies | Add `"premium" => true` |
| Toughest anti-bot protection | Add `"ultra_premium" => true` |
| Multi-step / paginated flow on same domain | Use `"session_number"` |
| POST a form or JSON body to target | `$client->post($url, $options)->raw_body` |
| 20+ URLs or batch jobs | Use async endpoint via cURL or Guzzle |
| Supported platform (Amazon, Google, etc.) | Use structured data endpoint directly |

## Parameter Reference

### Rendering

```php
// Render JavaScript before returning HTML
// Use when: page is a React/Vue/Angular SPA, or scrape returns empty/partial content
// Cost: +10 credits
$html = $client->get("https://spa-site.com/", ["render" => true])->raw_body;

// Wait for a specific DOM element (requires render: true)
$html = $client->get("https://spa-site.com/", [
    "render"            => true,
    "wait_for_selector" => ".product-list",
])->raw_body;

// Screenshot (auto-enables rendering)
$html = $client->get("https://example.com/", ["screenshot" => true])->raw_body;
```

Start without `render`. Add it only when the response is missing expected content — it increases cost and latency.

### Proxies and Geotargeting

```php
// Route through a country-specific proxy — no extra credit cost
$html = $client->get("https://example.com/", ["country_code" => "de"])->raw_body;

// Premium residential/mobile IPs — for sites that block datacenter proxies
// Cost: 10 credits (25 with render)
$html = $client->get("https://hard-site.com/", ["premium" => true])->raw_body;

// Ultra-premium — for the toughest anti-bot protections
// Cost: 30 credits (75 with render)
// Note: incompatible with custom headers — keep_headers is ignored
$html = $client->get("https://hardest-site.com/", ["ultra_premium" => true])->raw_body;
```

`premium` and `ultra_premium` are mutually exclusive — never set both.
Escalation order: standard (1 cr) → render (10 cr) → premium (10 cr) → ultra_premium (30 cr).

### Sessions (Sticky Proxy)

```php
// Reuse the same proxy IP across requests — useful for pagination and multi-step flows
// Sessions expire 15 minutes after last use; any integer is a valid session ID
$html1 = $client->get("https://example.com/page1", ["session_number" => 42])->raw_body;
$html2 = $client->get("https://example.com/page2", ["session_number" => 42])->raw_body;
```

### Headers and Device Type

```php
// Forward custom headers to the target site
// Note: keep_headers is ignored when ultra_premium is true
$html = $client->get("https://example.com/", [
    "keep_headers" => true,
])->raw_body;
// Pass headers in the request options array alongside ScraperAPI params

// Emulate a mobile or desktop browser user-agent
$html = $client->get("https://example.com/", ["device_type" => "mobile"])->raw_body;
```

### Autoparse and Response Format

```php
// Return structured JSON instead of HTML for supported sites (Amazon, Google, etc.)
$json = $client->get("https://amazon.com/dp/B09V3KXJPB", ["autoparse" => true])->raw_body;
$data = json_decode($json, true);

// Markdown output — useful for text pipelines
$md = $client->get("https://docs.example.com/", ["output_format" => "markdown"])->raw_body;
```

## POST Requests

```php
// POST a JSON body to the target site through ScraperAPI's proxy
$options = [
    "body"    => json_encode(["key" => "value"]),
    "headers" => ["Content-Type" => "application/json"],
];
$result = $client->post("https://example.com/api", $options)->raw_body;
```

## Escalation Ladder

Always start with the cheapest option and escalate only when blocked.

```php
function scrapeWithEscalation(Client $client, string $url): ?string
{
    $tiers = [
        [],
        ["render"       => true],
        ["premium"      => true],
        ["premium"      => true, "render" => true],
        ["ultra_premium" => true],
    ];

    foreach ($tiers as $params) {
        $html = $client->get($url, $params)->raw_body;
        if ($html && stripos($html, '<html') !== false) {
            return $html;
        }
    }
    return null;
}
```

## Async Jobs (for Batches)

The SDK is synchronous — each `->get()` call blocks until the response (up to 70 seconds). For 20+ URLs, use the async REST endpoint.

```php
$apiKey = getenv('SCRAPERAPI_API_KEY');

function submitJob(string $url, array $apiParams = []): array
{
    global $apiKey;
    $ch = curl_init('https://async.scraperapi.com/jobs');
    curl_setopt_array($ch, [
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => json_encode(['apiKey' => $apiKey, 'url' => $url, 'apiParams' => $apiParams]),
        CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
        CURLOPT_RETURNTRANSFER => true,
    ]);
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true); // ["id" => "...", "statusUrl" => "..."]
}

function pollJob(array $job, int $maxWait = 120, int $interval = 5): string
{
    $deadline = time() + $maxWait;
    while (time() < $deadline) {
        $data = json_decode(file_get_contents($job['statusUrl']), true);
        if ($data['status'] === 'finished') return $data['response']['body'];
        if ($data['status'] === 'failed')   throw new \RuntimeException("Job {$job['id']} failed");
        sleep($interval);
    }
    throw new \RuntimeException("Job {$job['id']} timed out");
}

// Submit and collect
$urls = ['https://example.com/p1', 'https://example.com/p2'];
$jobs = array_map('submitJob', $urls);
$results = array_map('pollJob', $jobs);
```

## Structured Data Endpoints

For supported platforms, use structured endpoints instead of raw HTML — they return clean JSON without parsing logic.

```php
function structuredGet(string $vertical, array $params = []): array
{
    global $apiKey;
    $query = http_build_query(array_merge(['api_key' => $apiKey], $params));
    $url   = "https://api.scraperapi.com/structured/{$vertical}?{$query}";
    $body  = file_get_contents($url);
    if ($body === false) throw new \RuntimeException("Request failed for {$vertical}");
    return json_decode($body, true);
}

// Google SERP
$results = structuredGet('google/search', ['query' => 'PHP web scraping']);

// Amazon product details
$product = structuredGet('amazon/product', ['asin' => 'B09V3KXJPB']);

// Walmart search
$items = structuredGet('walmart/search', ['query' => 'standing desk', 'tld' => 'com']);
```

See [structured data docs](https://docs.scraperapi.com/php) for all verticals and required fields.

## Error Handling

```php
function safeScrape(Client $client, string $url, array $params = []): ?string
{
    try {
        return $client->get($url, $params)->raw_body;
    } catch (\Exception $e) {
        $status = method_exists($e, 'getCode') ? (int) $e->getCode() : 0;
        switch ($status) {
            case 401: throw new \RuntimeException('Invalid API key — check SCRAPERAPI_API_KEY');
            case 403: throw new \RuntimeException('Blocked or out of credits — try premium or ultra_premium');
            case 429: throw new \RuntimeException('Rate limit — reduce concurrency or switch to async');
            case 500:
            case 503: throw new \RuntimeException('Transient error — retry with exponential backoff');
            default:  throw $e;
        }
    }
}
```

Status code reference: 200 success, 401 bad key, 403 blocked/no credits, 404 target not found,
429 rate limit, 500/503 transient (not charged — safe to retry).

Also see [retry docs](https://docs.scraperapi.com/php/handle-and-process-responses-via-scraperapi-in-php/use-api-status-codes-to-retry-failed-requests-in-php).

## Credit Cost Reference

| Request type | Credits |
|---|---|
| Standard | 1 |
| `"render" => true` | 10 |
| `"premium" => true` | 10 |
| `"premium" => true, "render" => true` | 25 |
| `"ultra_premium" => true` | 30 |
| `"ultra_premium" => true, "render" => true` | 75 |

Add `"max_cost" => N` to any request to cap credit spend — returns 403 if the request would cost more than N credits.

## Documentation

- [PHP SDK getting started](https://docs.scraperapi.com/php)
- [SDK method reference](https://docs.scraperapi.com/php/making-requests/sdk-method)
- [Retry failed requests](https://docs.scraperapi.com/php/handle-and-process-responses-via-scraperapi-in-php/use-api-status-codes-to-retry-failed-requests-in-php)
- [API status codes](https://docs.scraperapi.com/php/handling-and-processing-responses/api-status-codes)
- [Dashboard & credits](https://dashboard.scraperapi.com/)
