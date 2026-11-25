# Web Scraping — PerfectJob

> Playwright Java + Jsoup + GraphQL. Strategy pattern per job board. Ethical scraping with anti-bot evasion.

## Description

PerfectJob scrapes job listings from Brazilian and international job boards to build a comprehensive job database. The scraping system uses a Strategy pattern with a common `JobScraper` interface and one implementation per source. Playwright handles JavaScript-heavy sites (LinkedIn, Indeed, Catho), while Jsoup handles static HTML (Glassdoor, InfoJobs). GUPY is integrated via GraphQL API. A centralized `ScrapingOrchestrator` manages scheduling, deduplication, and circuit breaking.

**Stack**: Playwright Java 1.49.x, Jsoup 1.18.x, Spring Boot 3.4, virtual threads, Bucket4j 8.10.x for rate limiting.

**Sources**: LinkedIn, Indeed Brasil, Catho, Glassdoor, InfoJobs, GUPY.

## Checklist

1. Check `robots.txt` of target site before implementing any scraper — respect crawl-delay and disallow rules
2. Create one class per source implementing `JobScraper` interface
3. Use Playwright for JS-heavy sites (LinkedIn, Indeed, Catho) — Jsoup for static sites (Glassdoor, InfoJobs)
4. Implement rate limiting per domain using Bucket4j — never exceed 1 request per 3-8 seconds (randomized)
5. Rotate User-Agent strings from a curated list of real browser UAs
6. Generate URL hash (SHA-256) for deduplication before inserting
7. Compare embeddings for fuzzy deduplication (similarity > 90%) before inserting new jobs
8. Wrap each scraper call in a circuit breaker — open after 5 failures, half-open after 60s
9. Always set `source` and `sourceUrl` on scraped jobs — users must be able to navigate to original listing
10. Use `@Scheduled` with virtual threads for orchestration — never block the scheduler thread
11. Store scraping metadata (task status, jobs found, errors) in `scraping_tasks` table
12. Handle pagination: max 10 pages per source per query unless configured otherwise

## Key Rules

- **NEVER** scrape without checking robots.txt first
- **NEVER** store personal data from profiles (email, phone) — only public job listing data
- **NEVER** exceed rate limits — use Bucket4j with randomized delays between 3-8 seconds
- **NEVER** run scrapers in the main request thread — always use `@Scheduled` or `@Async`
- **NEVER** hardcode credentials in scraper code — use Spring Environment or Vault
- **NEVER** ignore HTTP 429 (Too Many Requests) — back off exponentially
- **NEVER** scrape more than 10 pages per query per source in a single run
- **ALWAYS** attribute data to the original source (source field + sourceUrl)
- **ALWAYS** have a cease-and-desist plan — ability to disable any scraper via feature flag
- **ALWAYS** use headless browser with stealth options — never visible browser windows
- **ALWAYS** randomize delays between requests — never fixed intervals
- **ALWAYS** persist scraping task status for observability and debugging
- **ALWAYS** validate scraped data before persisting (non-null title, description, URL)

## Architecture

```
com.perfectjob.scraping/
├── domain/
│   ├── model/
│   │   ├── ScrapingTask.java
│   │   └── ScrapingResult.java          # record(List<RawJobData>, int totalPages, ...)
│   └── port/
│       ├── JobScraper.java              # interface: strategy contract
│       ├── ScrapingTaskRepository.java  # port for persistence
│       └── DeduplicationService.java    # port for dedup
├── adapter/in/
│   └── ScrapingScheduler.java          # @Scheduled entry point
├── adapter/out/
│   ├── linkedin/
│   │   └── LinkedInScraper.java        # Playwright-based
│   ├── indeed/
│   │   └── IndeedScraper.java          # Playwright-based
│   ├── catho/
│   │   └── CathoScraper.java           # Playwright-based
│   ├── glassdoor/
│   │   └── GlassdoorScraper.java       # Jsoup-based
│   ├── infojobs/
│   │   └── InfoJobsScraper.java        # Jsoup-based
│   └── gupy/
│       └── GupyScraper.java            # GraphQL-based
├── service/
│   ├── ScrapingOrchestrator.java       # Coordinates all scrapers
│   ├── DeduplicationServiceImpl.java   # URL hash + embedding similarity
│   └── RateLimiterFactory.java         # Bucket4j per-domain buckets
├── config/
│   ├── PlaywrightConfig.java           # Browser pool management
│   └── ScrapingProperties.java         # @ConfigurationProperties
└── exception/
    ├── ScrapingException.java
    ├── RateLimitExceededException.java
    └── SourceBlockedException.java      # Circuit breaker open
```

## Code Examples

### JobScraper Interface (Strategy Contract)

```java
package com.perfectjob.scraping.domain.port;

import com.perfectjob.scraping.domain.model.ScrapingResult;

import java.util.Optional;

public interface JobScraper {

    String getSourceName();

    ScrapingResult scrape(String query, String location, int maxPages);

    default Optional<String> normalizeJobUrl(String rawUrl) {
        return Optional.ofNullable(rawUrl)
            .map(url -> url.split("\\?")[0]);
    }
}
```

### ScrapingProperties

```java
package com.perfectjob.scraping.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

import java.util.Map;

@Data
@Component
@ConfigurationProperties(prefix = "perfectjob.scraping")
public class ScrapingProperties {

    private boolean enabled = true;
    private int maxPagesPerQuery = 10;
    private int delayMinSeconds = 3;
    private int delayMaxSeconds = 8;
    private int circuitBreakerFailureThreshold = 5;
    private int circuitBreakerResetSeconds = 60;
    private Map<String, Boolean> sources = Map.of(
        "linkedin", true,
        "indeed", true,
        "catho", true,
        "glassdoor", true,
        "infojobs", true,
        "gupy", true
    );
}
```

### Playwright-based Scraper (LinkedIn)

```java
package com.perfectjob.scraping.adapter.out.linkedin;

import com.microsoft.playwright.*;
import com.perfectjob.scraping.adapter.out.linkedin.parser.LinkedinJobParser;
import com.perfectjob.scraping.domain.model.ScrapingResult;
import com.perfectjob.scraping.domain.port.JobScraper;
import com.perfectjob.scraping.config.ScrapingProperties;
import com.perfectjob.scraping.service.RateLimiterFactory;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;

@Slf4j
@Component
@RequiredArgsConstructor
public class LinkedInScraper implements JobScraper {

    private final ScrapingProperties properties;
    private final RateLimiterFactory rateLimiterFactory;
    private final LinkedinJobParser parser;

    @Override
    public String getSourceName() {
        return "linkedin";
    }

    @Override
    public ScrapingResult scrape(String query, String location, int maxPages) {
        rateLimiterFactory.getBucket("linkedin").consume(1);

        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().launch(new BrowserType.LaunchOptions()
                .setHeadless(true));

            BrowserContext context = browser.newContext(new Browser.NewContextOptions()
                .setUserAgent(getRandomUserAgent())
                .setViewportSize(1920, 1080)
                .setLocale("pt-BR"));

            Page page = context.newPage();
            var rawJobs = new ArrayList<RawJobData>();

            for (int pageNum = 0; pageNum < maxPages; pageNum++) {
                String url = buildSearchUrl(query, location, pageNum);
                log.info("Scraping LinkedIn page {}: {}", pageNum + 1, url);

                page.navigate(url);
                page.waitForSelector(".jobs-search__results-list", new Page.WaitForSelectorOptions()
                    .setTimeout(15_000));

                var pageJobs = parser.parsePage(page);
                if (pageJobs.isEmpty()) break;
                rawJobs.addAll(pageJobs);

                randomDelay();
            }

            return new ScrapingResult(rawJobs, maxPages, rawJobs.size());
        }
    }

    private String buildSearchUrl(String query, String location, int page) {
        return String.format(
            "https://www.linkedin.com/jobs/search/?keywords=%s&location=%s&start=%d",
            URLEncoder.encode(query, StandardCharsets.UTF_8),
            URLEncoder.encode(location, StandardCharsets.UTF_8),
            page * 25
        );
    }

    private void randomDelay() {
        int delay = ThreadLocalRandom.current()
            .nextInt(properties.getDelayMinSeconds(), properties.getDelayMaxSeconds() + 1);
        try {
            Thread.sleep(Duration.ofSeconds(delay));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private String getRandomUserAgent() {
        return USER_AGENTS[ThreadLocalRandom.current().nextInt(USER_AGENTS.length)];
    }

    private static final String[] USER_AGENTS = {
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0"
    };
}
```

### Jsoup-based Scraper (Glassdoor)

```java
package com.perfectjob.scraping.adapter.out.glassdoor;

import com.perfectjob.scraping.domain.model.ScrapingResult;
import com.perfectjob.scraping.domain.port.JobScraper;
import com.perfectjob.scraping.config.ScrapingProperties;
import com.perfectjob.scraping.service.RateLimiterFactory;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;

@Slf4j
@Component
@RequiredArgsConstructor
public class GlassdoorScraper implements JobScraper {

    private final ScrapingProperties properties;
    private final RateLimiterFactory rateLimiterFactory;
    private final GlassdoorJobParser parser;

    @Override
    public String getSourceName() {
        return "glassdoor";
    }

    @Override
    public ScrapingResult scrape(String query, String location, int maxPages) {
        rateLimiterFactory.getBucket("glassdoor").consume(1);

        var rawJobs = new ArrayList<RawJobData>();

        for (int pageNum = 1; pageNum <= maxPages; pageNum++) {
            try {
                String url = buildSearchUrl(query, location, pageNum);
                log.info("Scraping Glassdoor page {}: {}", pageNum, url);

                Document doc = Jsoup.connect(url)
                    .userAgent(getRandomUserAgent())
                    .referrer("https://www.google.com/")
                    .timeout(15_000)
                    .followRedirects(true)
                    .get();

                var pageJobs = parser.parseDocument(doc);
                if (pageJobs.isEmpty()) break;
                rawJobs.addAll(pageJobs);

                randomDelay();
            } catch (IOException e) {
                log.error("Glassdoor scraping error on page {}", pageNum, e);
                break;
            }
        }

        return new ScrapingResult(rawJobs, maxPages, rawJobs.size());
    }
}
```

### Rate Limiter Factory (Bucket4j)

```java
package com.perfectjob.scraping.service;

import io.github.bucket4j.Bandwidth;
import io.github.bucket4j.Bucket;
import io.github.bucket4j.Refill;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class RateLimiterFactory {

    private final ConcurrentHashMap<String, Bucket> buckets = new ConcurrentHashMap<>();

    public Bucket getBucket(String domain) {
        return buckets.computeIfAbsent(domain, this::createBucket);
    }

    private Bucket createBucket(String domain) {
        Bandwidth bandwidth = Bandwidth.classic(
            10,
            Refill.greedy(1, Duration.ofSeconds(5))
        );
        return Bucket.builder()
            .addLimit(bandwidth)
            .build();
    }
}
```

### ScrapingOrchestrator

```java
package com.perfectjob.scraping.service;

import com.perfectjob.scraping.config.ScrapingProperties;
import com.perfectjob.scraping.domain.port.JobScraper;
import com.perfectjob.scraping.domain.model.ScrapingResult;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class ScrapingOrchestrator {

    private final ScrapingProperties properties;
    private final DeduplicationServiceImpl deduplicationService;
    private final Map<String, JobScraper> scrapers;

    public ScrapingOrchestrator(
            ScrapingProperties properties,
            DeduplicationServiceImpl deduplicationService,
            List<JobScraper> scraperList) {
        this.properties = properties;
        this.deduplicationService = deduplicationService;
        this.scrapers = scraperList.stream()
            .collect(Collectors.toMap(JobScraper::getSourceName, Function.identity()));
    }

    @Scheduled(fixedDelayString = "PT30M")
    public void runScheduledScraping() {
        if (!properties.isEnabled()) {
            log.info("Scraping is disabled");
            return;
        }

        List<String> queries = List.of(
            "desenvolvedor java",
            "desenvolvedor python",
            "engenheiro de dados",
            "product manager",
            "devops",
            "frontend react"
        );
        String location = "Brasil";

        for (String query : queries) {
            Thread.ofVirtual().name("scrape-" + query.replaceAll("\\s", "-")).start(() -> {
                scrapeAllSources(query, location);
            });
        }
    }

    private void scrapeAllSources(String query, String location) {
        for (var entry : scrapers.entrySet()) {
            String sourceName = entry.getKey();
            if (!properties.getSources().getOrDefault(sourceName, false)) continue;

            try {
                log.info("Starting scrape: source={}, query={}", sourceName, query);
                ScrapingResult result = entry.getValue().scrape(
                    query, location, properties.getMaxPagesPerQuery()
                );
                deduplicationService.processAndDeduplicate(result);
                log.info("Completed scrape: source={}, jobs={}", sourceName, result.rawJobs().size());
            } catch (Exception e) {
                log.error("Scraping failed: source={}, query={}", sourceName, query, e);
            }
        }
    }
}
```

### Deduplication Service

```java
package com.perfectjob.scraping.service;

import com.perfectjob.job.domain.port.JobRepository;
import com.perfectjob.scraping.domain.model.RawJobData;
import com.perfectjob.scraping.domain.model.ScrapingResult;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.HexFormat;

@Slf4j
@Service
@RequiredArgsConstructor
public class DeduplicationServiceImpl {

    private final JobRepository jobRepository;
    private static final double SIMILARITY_THRESHOLD = 0.90;

    public void processAndDeduplicate(ScrapingResult result) {
        for (RawJobData raw : result.rawJobs()) {
            String urlHash = hashUrl(raw.sourceUrl());

            if (jobRepository.existsByUrlHash(urlHash)) {
                log.debug("Skipping duplicate job (URL hash): {}", raw.sourceUrl());
                continue;
            }

            jobRepository.save(raw.toJob(urlHash));
        }
    }

    private String hashUrl(String url) {
        try {
            var digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(url.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hash);
        } catch (Exception e) {
            throw new RuntimeException("Failed to hash URL", e);
        }
    }
}
```

## References

- Playwright Java: https://playwright.dev/java/
- Jsoup: https://jsoup.org/
- Bucket4j: https://bucket4j.com/
- robots.txt parser: https://github.com/crawler-commons/crawler-commons
- GUPY GraphQL API: https://docs.gupy.io/
