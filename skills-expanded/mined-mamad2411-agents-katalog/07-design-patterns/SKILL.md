# Design Patterns — PerfectJob

> Strategy, Factory, Builder, Observer, Chain of Responsibility, Repository, Adapter. Applied to PerfectJob domain.

## Description

PerfectJob applies well-established design patterns to keep the codebase maintainable, testable, and extensible. Each pattern is chosen to solve a specific problem in the domain: multi-source scraping (Strategy), multi-format parsing (Factory), complex search criteria (Builder), job alerts (Observer), resume processing (Chain of Responsibility), data access (Repository), and job board integration (Adapter).

## Checklist

1. Use **Strategy** for any multi-implementation scenario (scrapers per source, embedding providers)
2. Use **Factory** for creating objects with complex construction logic (resume parsers per file type)
3. Use **Builder** for objects with many optional parameters (JobSearchCriteria, MatchRequest)
4. Use **Observer** for event-driven decoupling (job alerts, match notifications)
5. Use **Chain of Responsibility** for sequential processing pipelines (resume processing)
6. Use **Repository** for data access abstraction (domain port + JPA adapter)
7. Use **Adapter** for integrating external systems (job boards, embedding APIs, LLMs)
8. Review every class > 300 lines for God class anti-pattern — split by responsibility
9. Keep controllers thin — only HTTP ↔ domain translation
10. Keep domain models rich — business logic stays in the entity or domain service

## Key Rules

- **NEVER** create God classes — max 300 lines, single responsibility
- **NEVER** put business logic in controllers — only parameter extraction and response formatting
- **NEVER** create anemic domain models — entities should encapsulate their invariants
- **NEVER** use `instanceof` chains — use polymorphism via interfaces/sealed types
- **NEVER** hardcode strategy selection — use Spring injection + Map<String, Interface>
- **ALWAYS** depend on abstractions (interfaces), not concrete implementations
- **ALWAYS** keep domain logic in the domain layer — no framework annotations except `@Entity`
- **ALWAYS** make domain port interfaces framework-agnostic
- **ALWAYS** use sealed interfaces when the set of implementations is closed and known

## Patterns Applied

### 1. Strategy — Job Scrapers

**Problem**: Each job board requires different scraping logic (Playwright vs Jsoup vs API).

**Solution**: Common `JobScraper` interface, one implementation per source. `ScrapingOrchestrator` doesn't know which scraper it's using.

```
JobScraper (interface)
├── LinkedInScraper    (Playwright)
├── IndeedScraper      (Playwright)
├── CathoScraper       (Playwright)
├── GlassdoorScraper   (Jsoup)
├── InfoJobsScraper    (Jsoup)
└── GupyScraper        (GraphQL API)
```

```java
public interface JobScraper {
    String getSourceName();
    ScrapingResult scrape(String query, String location, int maxPages);
}

@Component
public class ScrapingOrchestrator {
    private final Map<String, JobScraper> scrapers;

    public ScrapingOrchestrator(List<JobScraper> scraperList) {
        this.scrapers = scraperList.stream()
            .collect(Collectors.toMap(JobScraper::getSourceName, Function.identity()));
    }

    public void scrapeAll(String query, String location) {
        scrapers.forEach((name, scraper) -> {
            Thread.ofVirtual().name("scrape-" + name).start(() -> {
                scraper.scrape(query, location, 10);
            });
        });
    }
}
```

### 2. Factory — Resume Parsers

**Problem**: Resume files come in PDF, DOCX, and plain text formats. Parsing logic differs per format.

**Solution**: `ResumeParserFactory` returns the correct `ResumeParser` implementation based on file extension.

```java
public interface ResumeParser {
    boolean supports(String fileExtension);
    ParsedResume parse(InputStream fileContent);
}

@Component
public class PdfResumeParser implements ResumeParser {
    @Override
    public boolean supports(String ext) { return "pdf".equalsIgnoreCase(ext); }

    @Override
    public ParsedResume parse(InputStream content) {
        // Apache PDFBox extraction logic
    }
}

@Component
public class DocxResumeParser implements ResumeParser {
    @Override
    public boolean supports(String ext) { return "docx".equalsIgnoreCase(ext); }

    @Override
    public ParsedResume parse(InputStream content) {
        // Apache POI extraction logic
    }
}

@Component
@RequiredArgsConstructor
public class ResumeParserFactory {
    private final List<ResumeParser> parsers;

    public ResumeParser getParser(String filename) {
        String ext = FilenameUtils.getExtension(filename).toLowerCase();
        return parsers.stream()
            .filter(p -> p.supports(ext))
            .findFirst()
            .orElseThrow(() -> new UnsupportedOperationException(
                "Unsupported resume format: " + ext));
    }
}
```

### 3. Builder — JobSearchCriteria

**Problem**: Search requests have 10+ optional parameters. Constructor telescoping is unmanageable.

**Solution**: Builder pattern with Java 21 record + `@Builder` (Lombok) or manual builder.

```java
public record JobSearchCriteria(
    String query,
    String city,
    String state,
    String jobType,
    String experienceLevel,
    BigDecimal salaryMin,
    BigDecimal salaryMax,
    boolean remoteOnly,
    List<String> sources,
    int page,
    int size
) {
    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private String query;
        private String city;
        private String state;
        private String jobType;
        private String experienceLevel;
        private BigDecimal salaryMin;
        private BigDecimal salaryMax;
        private boolean remoteOnly = false;
        private List<String> sources = List.of();
        private int page = 0;
        private int size = 20;

        public Builder query(String query) { this.query = query; return this; }
        public Builder city(String city) { this.city = city; return this; }
        public Builder state(String state) { this.state = state; return this; }
        public Builder jobType(String jobType) { this.jobType = jobType; return this; }
        public Builder experienceLevel(String level) { this.experienceLevel = level; return this; }
        public Builder salaryMin(BigDecimal min) { this.salaryMin = min; return this; }
        public Builder salaryMax(BigDecimal max) { this.salaryMax = max; return this; }
        public Builder remoteOnly(boolean remote) { this.remoteOnly = remote; return this; }
        public Builder sources(List<String> sources) { this.sources = sources; return this; }
        public Builder page(int page) { this.page = Math.max(0, page); return this; }
        public Builder size(int size) { this.size = Math.clamp(size, 1, 50); return this; }

        public JobSearchCriteria build() {
            return new JobSearchCriteria(query, city, state, jobType,
                experienceLevel, salaryMin, salaryMax, remoteOnly, sources, page, size);
        }
    }
}
```

### 4. Observer — Job Alerts

**Problem**: When new matching jobs are found, notify users via email, push notification, and in-app alert — without coupling matching logic to notification logic.

**Solution**: Spring Application EventPublication. Matching engine publishes `NewMatchEvent`, listeners handle delivery.

```java
public record NewMatchEvent(
    Long userId,
    Long jobId,
    double score,
    String jobTitle,
    String companyName
) {}

@Component
@RequiredArgsConstructor
@Slf4j
public class MatchingEngine {
    private final ApplicationEventPublisher eventPublisher;

    public void processMatches(Long userId) {
        var matches = findMatches(userId);
        matches.stream()
            .filter(m -> m.score() >= 80.0)
            .forEach(m -> eventPublisher.publishEvent(
                new NewMatchEvent(userId, m.jobId(), m.score(),
                                  m.jobTitle(), m.companyName())
            ));
    }
}

@Component
@RequiredArgsConstructor
@Slf4j
public class EmailNotificationListener {

    @Async
    @EventListener
    public void onNewMatch(NewMatchEvent event) {
        log.info("Sending email for match: user={}, job={}, score={}",
            event.userId(), event.jobId(), event.score());
        // Send email via SMTP or SendGrid
    }
}

@Component
@RequiredArgsConstructor
@Slf4j
public class PushNotificationListener {

    @Async
    @EventListener
    public void onNewMatch(NewMatchEvent event) {
        log.info("Sending push notification for match: user={}", event.userId());
        // Send push via expo-notifications push API
    }
}
```

### 5. Chain of Responsibility — Resume Processing

**Problem**: Resume upload requires sequential processing steps: virus scan → format detection → text extraction → skill extraction → experience calculation → embedding generation.

**Solution**: Chain of handlers, each performing one step and passing to the next.

```java
public abstract class ResumeProcessor {
    protected ResumeProcessor next;

    public ResumeProcessor linkWith(ResumeProcessor next) {
        this.next = next;
        return next;
    }

    public abstract ResumeContext process(ResumeContext context);

    protected ResumeContext processNext(ResumeContext context) {
        return next != null ? next.process(context) : context;
    }
}

@Component
@Order(1)
public class VirusScanProcessor extends ResumeProcessor {
    @Override
    public ResumeContext process(ResumeContext context) {
        // Scan file for viruses using ClamAV
        boolean clean = scanForViruses(context.getFileBytes());
        if (!clean) {
            throw new SecurityException("File failed virus scan");
        }
        context.setVirusScanned(true);
        return processNext(context);
    }
}

@Component
@Order(2)
public class FormatDetectionProcessor extends ResumeProcessor {
    @Override
    public ResumeContext process(ResumeContext context) {
        String format = detectFormat(context.getFileBytes(), context.getFilename());
        context.setFormat(format);
        return processNext(context);
    }
}

@Component
@Order(3)
public class TextExtractionProcessor extends ResumeProcessor {
    private final ResumeParserFactory parserFactory;

    @Override
    public ResumeContext process(ResumeContext context) {
        ResumeParser parser = parserFactory.getParser(context.getFilename());
        ParsedResume parsed = parser.parse(new ByteArrayInputStream(context.getFileBytes()));
        context.setParsedResume(parsed);
        return processNext(context);
    }
}

@Component
@Order(4)
public class SkillExtractionProcessor extends ResumeProcessor {
    private final LlmService llmService;

    @Override
    public ResumeContext process(ResumeContext context) {
        List<ExtractedSkill> skills = llmService.extractSkills(context.getParsedResume());
        context.setExtractedSkills(skills);
        return processNext(context);
    }
}

@Component
@Order(5)
public class ExperienceCalculationProcessor extends ResumeProcessor {
    @Override
    public ResumeContext process(ResumeContext context) {
        int totalYears = calculateExperience(context.getParsedResume().getExperience());
        context.setTotalExperienceYears(totalYears);
        return processNext(context);
    }
}

@Component
@Order(6)
public class EmbeddingGenerationProcessor extends ResumeProcessor {
    private final EmbeddingService embeddingService;

    @Override
    public ResumeContext process(ResumeContext context) {
        var embeddings = embeddingService.generateEmbeddings(
            List.of(context.getParsedResume().getFullText()), "search_query"
        );
        context.setEmbedding(embeddings.get(0));
        return processNext(context);
    }
}

@Component
@RequiredArgsConstructor
public class ResumeProcessingChain {
    private final List<ResumeProcessor> processors;

    @PostConstruct
    public void initChain() {
        for (int i = 0; i < processors.size() - 1; i++) {
            processors.get(i).linkWith(processors.get(i + 1));
        }
    }

    public ResumeContext execute(ResumeContext context) {
        return processors.get(0).process(context);
    }
}
```

### 6. Repository — Domain Port Separation

**Problem**: Domain logic shouldn't depend on Spring Data JPA interfaces.

**Solution**: Define domain port interfaces in `domain/port/`, implement with JPA in `adapter/out/`.

```java
// domain/port/JobRepository.java (no Spring dependency)
public interface JobRepository {
    Optional<Job> findById(Long id);
    Page<Job> search(JobSearchCriteria criteria);
    boolean existsByUrlHash(String urlHash);
    Job save(Job job);
    List<Job> findSimilarJobs(float[] embedding, int limit);
}

// adapter/out/JobRepositoryImpl.java
@Component
@RequiredArgsConstructor
public class JobRepositoryImpl implements JobRepository {
    private final JobJpaRepository jpaRepository;

    @Override
    public Optional<Job> findById(Long id) {
        return jpaRepository.findById(id);
    }

    @Override
    public Page<Job> search(JobSearchCriteria criteria) {
        // Delegate to JPA repository with Specification
        return jpaRepository.findAll(buildSpecification(criteria),
            PageRequest.of(criteria.page(), criteria.size()));
    }

    @Override
    public Job save(Job job) {
        return jpaRepository.save(job);
    }
}
```

### 7. Adapter — Job Board Integrations

**Problem**: External job boards (LinkedIn, GUPY, Indeed) have different APIs and data formats.

**Solution**: Adapter pattern normalizes external data into PerfectJob's internal model.

```java
public interface JobBoardAdapter {
    String getBoardName();
    List<RawJobData> fetchJobs(String query, String location);
    NormalizedJob normalize(RawJobData rawData);
}

@Component
public class LinkedInAdapter implements JobBoardAdapter {
    @Override
    public NormalizedJob normalize(RawJobData raw) {
        return NormalizedJob.builder()
            .source("linkedin")
            .sourceId(raw.getExternalId())
            .sourceUrl(raw.getUrl())
            .title(raw.getTitle())
            .companyName(raw.getCompany())
            .description(cleanHtml(raw.getDescription()))
            .location(parseBrazilianLocation(raw.getLocation()))
            .isRemote(raw.getTitle().toLowerCase().contains("remoto"))
            .jobType(mapJobType(raw.getEmploymentType()))
            .salaryMin(parseSalaryRange(raw.getSalary()).getMin())
            .salaryMax(parseSalaryRange(raw.getSalary()).getMax())
            .postedDate(parseLinkedInDate(raw.getPostedDate()))
            .build();
    }
}
```

### Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|---|---|---|
| God class > 300 lines | Too many responsibilities | Split by SRP |
| Fat controller | Business logic in HTTP layer | Move to service/domain |
| Anemic domain model | Entity with only getters/setters | Add domain methods |
| Hardcoded strategy selection | `if (source.equals("linkedin"))` | Use Spring Map injection |
| `instanceof` chains | Brittle type checking | Polymorphism via interface |
| Utility classes with state | Hidden global state | Make stateless or use proper class |
| Callback hell | Nested async operations | Use CompletableFuture chains |
| Singleton misuse | Hidden dependencies | Use Spring `@Component` instead |

## References

- Design Patterns (GoF): https://en.wikipedia.org/wiki/Design_Patterns
- SOLID Principles: https://en.wikipedia.org/wiki/SOLID
- Hexagonal Architecture: https://alistair.cockburn.us/hexagonal-architecture/
- Spring Events: https://docs.spring.io/spring-framework/reference/core/beans/context-introduction.html#context-functionality-events
