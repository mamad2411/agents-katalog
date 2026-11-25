---
name: cdn-optimization
version: 1.0.0
min_mindforge_version: 10.1.1
status: stable
triggers: cdn optimization, cache hierarchy, cache purge strategy, edge-side includes, origin shielding, cache key design, cdn invalidation, cdn prewarming, stale-while-revalidate cdn, cdn hit ratio, cdn failover, multi-cdn strategy
compose: caching-strategies
---

# Skill — CDN Optimization

## When this skill activates
Any task involving CDN configuration, cache strategy design, cache invalidation,
origin shielding, cache key optimization, or multi-CDN architecture
for high-traffic web applications.

## Mandatory actions when this skill is active

### Before writing any code
1. Identify content types and their cacheability (static, dynamic, personalized).
2. Define cache hierarchy (Edge POP → Regional Shield → Origin).
3. Design cache keys (URL + Vary headers — don't over-key).
4. Plan purge/invalidation strategy before enabling caching.

### During implementation
- Set explicit Cache-Control headers on every response.
- Enable origin shielding to collapse edge requests.
- Use stale-while-revalidate for graceful cache refresh.
- Design cache keys to maximize hit ratio without serving wrong content.
- Implement tag-based purge for granular invalidation.
- Never cache responses with `Set-Cookie` headers.

### After implementation
- Measure cache hit ratio (target: >95% static, >80% dynamic).
- Verify purge propagates within acceptable time.
- Test cache behavior with different user contexts (logged in vs anonymous).
- Monitor origin load (should decrease significantly with CDN).
- Confirm no stale content is served after deploys.

## Cache Hierarchy

### Three-Tier Architecture
```
User → Edge POP (closest) → Regional Shield → Origin Server
        ↓ cache hit?         ↓ cache hit?      ↓ always fresh
        serve immediately    serve to edge      generate response
```

### Benefits
- **Edge POP**: Sub-10ms latency for cached content.
- **Regional Shield**: Collapses many edge misses into single origin request.
- **Origin**: Only handles truly unique/expired requests.

### Origin Shielding (Critical)
Without shielding: 100 edge POPs × cache miss = 100 origin requests.
With shielding: 100 edge POPs → 1 shield request → 1 origin request.

## Cache Key Design

### Principles
- Cache key = what makes a response unique.
- Over-keying (too many variants) = low hit ratio.
- Under-keying (too few variants) = serving wrong content.

### Common Cache Key Components
```
Default: scheme + host + path + query string
Add when needed: Accept-Encoding, Accept-Language, device type
NEVER include: session cookies, random headers, full cookie jar
```

### Examples
| Content Type | Cache Key | Vary Header |
|-------------|-----------|-------------|
| Static assets | URL (path + hash) | None |
| API (public) | URL + query params | Accept-Encoding |
| Localized page | URL + language | Accept-Language |
| Responsive image | URL + device class | (custom header) |

### Anti-Patterns
- Including session cookie in cache key (unique per user = 0% hit ratio).
- Including `Authorization` header for public content.
- Using full `User-Agent` as variant (thousands of variants).

## Cache-Control Headers

### Static Assets (Hashed Filenames)
```
Cache-Control: public, max-age=31536000, immutable
```
- One year cache, never revalidate.
- Safe because filename changes on content change.

### Dynamic Content (Cacheable)
```
Cache-Control: public, max-age=60, stale-while-revalidate=300
```
- Fresh for 60s, serve stale for 300s while fetching fresh in background.
- User always gets fast response, content refreshes async.

### Personalized/Private
```
Cache-Control: private, no-store
```
- Never cache in shared caches (CDN).
- Only browser can cache.

### API Responses
```
Cache-Control: public, max-age=10, stale-while-revalidate=60, stale-if-error=300
```
- Short freshness, graceful degradation on origin failure.

## Purge Strategy

### Methods (Ranked by Preference)
1. **Tag-based purge**: Assign cache tags, purge by tag. Most granular.
2. **URL-based purge**: Purge specific URL. Precise but doesn't scale to many URLs.
3. **Prefix purge**: Purge all URLs matching path prefix. Broad but useful for deploys.
4. **Full purge**: Nuclear option. Purge everything. Avoid in production.

### Purge Triggers
- Deploy: purge changed assets (tag-based or prefix).
- Content update: purge specific URLs or tags.
- Emergency: full purge if stale content is harmful.

### Propagation Time
- Instant purge at edge: <1 second (Fastly, Cloudflare).
- Some CDNs: 5-15 minutes propagation.
- Always verify purge completed before relying on fresh content.

## Stale-While-Revalidate

### How It Works
1. Request arrives for expired content.
2. CDN serves stale response immediately (fast!).
3. CDN fetches fresh content from origin in background.
4. Next request gets fresh content.

### Benefits
- User never waits for origin response.
- Origin gets time to respond without blocking users.
- Graceful handling of origin slowness or errors.

### Configuration
```
Cache-Control: public, max-age=60, stale-while-revalidate=600, stale-if-error=86400
```
- Fresh for 60s.
- Serve stale for up to 600s while revalidating.
- Serve stale for up to 24h if origin is erroring.

## Hit Ratio Targets

| Content Type | Target Hit Ratio | If Below |
|-------------|-----------------|----------|
| Static assets (JS/CSS/images) | >99% | Check cache key, immutable headers |
| HTML pages (anonymous) | >95% | Check Vary headers, cookie leakage |
| API responses (public) | >80% | Check TTL, query param diversity |
| Personalized content | N/A | Should not be cached at CDN |

### Diagnosing Low Hit Ratio
1. Check `Vary` header — is it over-specifying?
2. Check cache key — are cookies leaking in?
3. Check TTL — is content expiring too quickly?
4. Check query parameters — are tracking params included?
5. Check purge frequency — are you purging too often?

## Multi-CDN Strategy

### Use Cases
- Failover (CDN A down → traffic to CDN B).
- Cost arbitrage (cheaper CDN for bulk, premium for critical).
- Geographic optimization (CDN A better in region X, CDN B in region Y).
- Vendor independence (avoid lock-in).

### Implementation
- DNS-based switching (GeoDNS or failover).
- Unified purge API across CDN providers.
- Normalized configuration (cache rules consistent across providers).
- Monitoring per-CDN performance independently.

## Edge-Side Includes (ESI)

### Pattern
Compose pages from independently cached fragments:
```html
<esi:include src="/header" />
<main>Page-specific content</main>
<esi:include src="/footer" />
```

### Benefits
- Header/footer cached separately (long TTL).
- Page content has its own TTL.
- Reduces full-page cache misses.

### When to Use
- Pages share common components (header, nav, footer).
- Components have different cache lifetimes.
- Personalization is limited to specific fragments.

## Self-check
- [ ] Cache-Control headers set on every response type.
- [ ] Origin shielding enabled.
- [ ] Cache keys designed (not over-keyed or under-keyed).
- [ ] Purge strategy implemented and tested.
- [ ] Stale-while-revalidate configured for dynamic content.
- [ ] Hit ratio >95% for static, >80% for dynamic.
- [ ] No `Set-Cookie` responses being cached.
- [ ] Deploy purge automated in CI/CD pipeline.
- [ ] Origin load reduced significantly vs direct traffic.
