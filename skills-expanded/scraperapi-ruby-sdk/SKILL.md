---
name: scraperapi-ruby-sdk
description: >
  Best-practices reference for the ScraperAPI Ruby SDK (scraperapi gem).
  Consult whenever the user is writing, debugging, or reviewing Ruby code that calls ScraperAPI.
  Use when user asks: "scrape a website with Ruby and ScraperAPI", "ScraperAPI Ruby example",
  "how do I use the ScraperAPI gem", "Ruby ScraperAPI render", "ScraperAPI Ruby premium proxy",
  "ScraperAPI gem sessions", "ScraperAPI Ruby error handling". Covers gem setup, all request
  parameters, the escalation ladder, error handling by status code, and credit costs.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "💎"
    homepage: https://docs.scraperapi.com/ruby
---

# ScraperAPI — Ruby SDK Best Practices

**Requires:** Ruby >= 2.0, `gem install scraperapi` (or `gem 'scraperapi'` in Gemfile), `SCRAPERAPI_API_KEY` environment variable.

## Setup

```ruby
require "scraper_api"

client = ScraperAPI::Client.new(ENV["SCRAPERAPI_API_KEY"])
```

Never hardcode the API key. Read it from the environment every time.

## Basic Usage

```ruby
# Simple GET — returns raw HTML string via .raw_body
html = client.get("https://example.com/").raw_body
puts html

# With a single parameter
html = client.get("https://example.com/", render: true).raw_body

# With multiple parameters
html = client.get(
  "https://example.com/",
  render: true,
  country_code: "us"
).raw_body
```

Parameters are passed as keyword arguments after the URL. `.raw_body` extracts the HTML string from the response object.

## Decision Guide

| Situation | Approach |
|-----------|---------|
| Single URL, synchronous | `client.get(url, **params).raw_body` |
| Page loads content via JavaScript | Pass `render: true` |
| Site blocks datacenter proxies | Pass `premium: true` |
| Toughest anti-bot protection | Pass `ultra_premium: true` |
| Multi-step / paginated flow on same domain | Use `session_number:` |
| 20+ URLs or batch jobs | Use async endpoint via `Net::HTTP` or `Faraday` |
| Supported platform (Amazon, Google, etc.) | Use structured data endpoint directly |

## Parameter Reference

### Rendering

```ruby
# Render JavaScript before returning HTML
# Use when: page is a React/Vue/Angular SPA, or initial scrape returns empty/partial content
# Cost: +10 credits
html = client.get("https://spa-site.com/", render: true).raw_body

# Wait for a specific DOM element (requires render: true)
html = client.get(
  "https://spa-site.com/",
  render: true,
  wait_for_selector: ".product-list"
).raw_body
```

Don't add `render: true` by default — try without it first. It increases cost and latency.

### Proxies and Geotargeting

```ruby
# Route through a country-specific proxy — no extra credit cost
html = client.get("https://example.com/", country_code: "gb").raw_body

# Premium residential/mobile IPs — for sites that block datacenter proxies
# Cost: 10 credits (25 with render: true)
html = client.get("https://hard-site.com/", premium: true).raw_body

# Ultra-premium — for the toughest anti-bot protections
# Cost: 30 credits (75 with render: true)
# Note: incompatible with keep_headers — custom headers are discarded
html = client.get("https://hardest-site.com/", ultra_premium: true).raw_body
```

`premium` and `ultra_premium` are mutually exclusive — never pass both.
Escalation order: standard (1 cr) → render (10 cr) → premium (10 cr) → ultra_premium (30 cr).

### Sessions (Sticky Proxy)

```ruby
# Reuse the same proxy IP across requests — useful for pagination and multi-step flows
# Sessions expire 15 minutes after last use; any integer is a valid session ID
html1 = client.get("https://example.com/page1", session_number: 42).raw_body
html2 = client.get("https://example.com/page2", session_number: 42).raw_body
```

### Headers and Device Type

```ruby
# Forward custom headers to the target site
# Note: keep_headers is ignored when ultra_premium: true
html = client.get(
  "https://example.com/",
  keep_headers: true
  # Pass additional headers via the underlying request object as needed
).raw_body

# Emulate a mobile or desktop browser user-agent
html = client.get("https://example.com/", device_type: "mobile").raw_body
```

### Autoparse

```ruby
# Return structured JSON instead of HTML for supported sites
# Use for Amazon, Google, and other supported platforms when you want clean data
json_result = client.get("https://amazon.com/dp/B09V3KXJPB", autoparse: true).raw_body
```

## Escalation Ladder

Always start with the cheapest option and escalate only when blocked.

```ruby
def scrape_with_escalation(client, url)
  tiers = [
    {},
    { render: true },
    { premium: true },
    { premium: true, render: true },
    { ultra_premium: true },
  ]

  tiers.each do |params|
    result = client.get(url, **params).raw_body
    return result if result&.include?("<html")
  end

  nil
end
```

## Async Jobs (for Batches)

The SDK is synchronous — each `client.get` blocks until the response arrives (up to 70 seconds).
For 20+ URLs, submit async jobs via the REST endpoint.

```ruby
require "net/http"
require "json"

API_KEY = ENV["SCRAPERAPI_API_KEY"]

def submit_job(url, api_params = {})
  uri = URI("https://async.scraperapi.com/jobs")
  payload = { apiKey: API_KEY, url: url, apiParams: api_params }
  response = Net::HTTP.post(uri, payload.to_json, "Content-Type" => "application/json")
  JSON.parse(response.body) # { "id" => "...", "statusUrl" => "..." }
end

def poll_job(job, max_wait: 120, interval: 5)
  deadline = Time.now + max_wait
  while Time.now < deadline
    uri = URI(job["statusUrl"])
    data = JSON.parse(Net::HTTP.get(uri))
    return data.dig("response", "body") if data["status"] == "finished"
    raise "Job #{job['id']} failed" if data["status"] == "failed"
    sleep interval
  end
  raise "Job #{job['id']} timed out"
end

# Submit all URLs, then collect results
urls = ["https://example.com/page1", "https://example.com/page2"]
jobs = urls.map { |u| submit_job(u) }
results = jobs.map { |j| poll_job(j) }
```

## Structured Data Endpoints

For supported platforms, use structured endpoints to get clean JSON without parsing HTML.

```ruby
require "net/http"
require "json"

def structured_get(vertical, params = {})
  query = URI.encode_www_form({ api_key: API_KEY }.merge(params))
  uri = URI("https://api.scraperapi.com/structured/#{vertical}?#{query}")
  response = Net::HTTP.get_response(uri)
  raise "Error #{response.code}" unless response.is_a?(Net::HTTPSuccess)
  JSON.parse(response.body)
end

# Google SERP
results = structured_get("google/search", { query: "ruby web scraping" })

# Amazon product details
product = structured_get("amazon/product", { asin: "B09V3KXJPB" })

# eBay search
listings = structured_get("ebay/search", { query: "mechanical keyboard" })
```

## Error Handling

The SDK raises exceptions on HTTP errors. Check the status code to determine the right action.

```ruby
def safe_scrape(client, url, params = {})
  client.get(url, **params).raw_body
rescue => e
  status = e.respond_to?(:response) ? e.response&.code&.to_i : nil
  case status
  when 401 then raise "Invalid API key — check SCRAPERAPI_API_KEY"
  when 403 then raise "Blocked or out of credits — try premium: true or ultra_premium: true"
  when 429 then raise "Rate limit hit — reduce concurrency or switch to async"
  when 500, 503 then raise "Transient error — retry with exponential backoff"
  else raise
  end
end
```

Status code reference: 200 success, 401 bad key, 403 blocked/no credits, 404 target not found,
429 rate limit, 500/503 transient (not charged — safe to retry).

## Credit Cost Reference

| Request type | Credits |
|---|---|
| Standard | 1 |
| `render: true` | 10 |
| `premium: true` | 10 |
| `premium: true, render: true` | 25 |
| `ultra_premium: true` | 30 |
| `ultra_premium: true, render: true` | 75 |

## Documentation

- [Ruby SDK getting started](https://docs.scraperapi.com/ruby)
- [SDK method reference](https://docs.scraperapi.com/ruby/making-requests/sdk-method)
- [JavaScript rendering](https://docs.scraperapi.com/ruby/making-requests-or-ruby/customizing-requests-or-ruby/rendering-javascript-or-ruby)
- [Sessions](https://docs.scraperapi.com/ruby/making-requests/customizing-requests/sessions)
- [API status codes](https://docs.scraperapi.com/ruby/handling-and-processing-responses/api-status-codes)
- [Dashboard & credits](https://dashboard.scraperapi.com/)
