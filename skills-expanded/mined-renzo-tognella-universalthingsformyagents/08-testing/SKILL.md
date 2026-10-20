# Testing — PerfectJob

> JUnit 5 + Mockito + Testcontainers. Test pyramid: 70% unit / 20% integration / 10% E2E. Given-When-Then naming.

## Description

PerfectJob follows a strict test pyramid strategy: 70% unit tests (domain logic, no Spring context), 20% integration tests (repositories, services with Testcontainers PostgreSQL), and 10% E2E tests (full API via MockMvc or Detox for mobile). All tests use Given-When-Then naming convention and test data factories with the Builder pattern.

**Stack**: JUnit 5.11.x, Mockito 5.x, Spring Boot Test 3.4.x, Testcontainers 1.20.x, MockMvc, AssertJ 3.x, React Native Testing Library, Jest, Detox.

## Checklist

1. Write unit tests FIRST for domain logic — no Spring context, pure Java tests
2. Use `@DataJpaTest` for repository integration tests — Testcontainers PostgreSQL
3. Use `@WebMvcTest` for controller tests — MockMvc + `@MockBean` services
4. Use `@SpringBootTest` + Testcontainers only for full integration tests
5. Name test methods using Given-When-Then: `shouldReturnJobs_whenSearchByTitle_givenActiveJobs`
6. Create test data factories using Builder pattern — never inline test data construction
7. Use `@TestConfiguration` for test-specific beans — never modify production config for tests
8. Mock external APIs (Cohere, OpenRouter, Playwright) in all tests — never call real services
9. Use Testcontainers for PostgreSQL + pgvector in integration tests
10. Write mobile tests with Jest + React Native Testing Library for components
11. Write mobile E2E tests with Detox for critical flows (login, job search, resume upload)
12. Verify test coverage ≥ 80% for domain and service layers

## Key Rules

- **NEVER** use `@SpringBootTest` for unit tests — it starts the entire context (slow)
- **NEVER** call external APIs in tests — always mock Cohere, OpenRouter, job boards
- **NEVER** use H2 in-memory database for tests — always use Testcontainers PostgreSQL
- **NEVER** share mutable test state between test methods — each test must be independent
- **NEVER** use `@DirtiesContext` — it recreates the entire Spring context (very slow)
- **NEVER** write tests without assertions — a test that doesn't assert is useless
- **ALWAYS** use Given-When-Then naming convention for test methods
- **ALWAYS** use AssertJ fluent assertions — never JUnit's `assertEquals`
- **ALWAYS** use test data factories — never construct test data inline
- **ALWAYS** test the unhappy path — error cases, validation failures, edge cases
- **ALWAYS** keep unit tests fast (< 1 second each) — no I/O, no framework startup
- **ALWAYS** tag tests: `@Tag("unit")`, `@Tag("integration")`, `@Tag("e2e")`

## Test Pyramid

```
          ╱╲
         ╱  ╲          E2E (10%)
        ╱    ╲         @SpringBootTest + MockMvc / Detox
       ╱──────╲
      ╱        ╲       Integration (20%)
     ╱          ╲      @DataJpaTest, Testcontainers
    ╱────────────╲
   ╱              ╲    Unit (70%)
  ╱                ╲   Plain JUnit + Mockito
 ╱──────────────────╲
```

## Code Examples

### Test Configuration (Testcontainers)

```java
package com.perfectjob.common.test;

import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.utility.DockerImageName;

@TestConfiguration(proxyBeanMethods = false)
public class TestcontainersConfig {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>(
        DockerImageName.parse("pgvector/pgvector:pg17")
    )
        .withDatabaseName("perfectjob_test")
        .withUsername("test")
        .withPassword("test");

    static {
        postgres.start();
    }
}
```

### Unit Test — Domain Logic (No Spring)

```java
package com.perfectjob.matching.service;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.within;

@Tag("unit")
class ScoreCalculatorTest {

    private final ScoreCalculator calculator = new ScoreCalculator(
        new MatchingProperties()
    );

    @Nested
    @DisplayName("computeHybridScore")
    class ComputeHybridScore {

        @Test
        @DisplayName("should return 100 when both scores are maximum")
        void shouldReturn100_whenBothScoresMaximum() {
            double result = calculator.computeHybridScore(1.0, 1.0);
            assertThat(result).isCloseTo(100.0, within(0.1));
        }

        @Test
        @DisplayName("should return ~50 when both scores are 0.5")
        void shouldReturn50_whenBothScoresMedium() {
            double result = calculator.computeHybridScore(0.5, 0.5);
            assertThat(result).isCloseTo(50.0, within(1.0));
        }

        @Test
        @DisplayName("should return near 0 when both scores are 0")
        void shouldReturnNearZero_whenBothScoresZero() {
            double result = calculator.computeHybridScore(0.0, 0.0);
            assertThat(result).isLessThan(1.0);
        }

        @ParameterizedTest(name = "embedding={0}, structured={1} → score≈{2}")
        @CsvSource({
            "0.8, 0.7, 92.0",
            "0.6, 0.5, 62.0",
            "0.3, 0.2, 18.0",
            "0.9, 0.3, 70.0"
        })
        void shouldProduceExpectedScores(double embedding, double structured, double expected) {
            double result = calculator.computeHybridScore(embedding, structured);
            assertThat(result).isCloseTo(expected, within(5.0));
        }
    }

    @Nested
    @DisplayName("computeStructuredScore")
    class ComputeStructuredScore {

        @Test
        @DisplayName("should weight skills match at 50%")
        void shouldWeightSkillsMatchAt50Percent() {
            double result = calculator.computeStructuredScore(1.0, 0.0, 0.0, 0.0);
            assertThat(result).isCloseTo(0.50, within(0.01));
        }

        @Test
        @DisplayName("should weight all components correctly")
        void shouldWeightAllComponents() {
            double result = calculator.computeStructuredScore(1.0, 1.0, 1.0, 1.0);
            assertThat(result).isCloseTo(1.0, within(0.01));
        }
    }
}
```

### Unit Test — Service with Mocks

```java
package com.perfectjob.scraping.service;

import com.perfectjob.scraping.domain.model.ScrapingResult;
import com.perfectjob.scraping.domain.port.JobScraper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.*;

@Tag("unit")
@ExtendWith(MockitoExtension.class)
class ScrapingOrchestratorTest {

    @Mock private JobScraper linkedInScraper;
    @Mock private JobScraper indeedScraper;
    @Mock private DeduplicationServiceImpl deduplicationService;

    private ScrapingOrchestrator orchestrator;

    @BeforeEach
    void setUp() {
        when(linkedInScraper.getSourceName()).thenReturn("linkedin");
        when(indeedScraper.getSourceName()).thenReturn("indeed");

        var properties = new ScrapingProperties();
        properties.setEnabled(true);
        properties.setSources(Map.of("linkedin", true, "indeed", true));

        orchestrator = new ScrapingOrchestrator(
            properties,
            deduplicationService,
            List.of(linkedInScraper, indeedScraper)
        );
    }

    @Test
    @DisplayName("should scrape all enabled sources")
    void shouldScrapeAllEnabledSources() {
        var result = new ScrapingResult(List.of(), 10, 0);
        when(linkedInScraper.scrape(anyString(), anyString(), anyInt())).thenReturn(result);
        when(indeedScraper.scrape(anyString(), anyString(), anyInt())).thenReturn(result);

        orchestrator.scrapeAllSources("java developer", "Sao Paulo");

        verify(linkedInScraper).scrape("java developer", "Sao Paulo", 10);
        verify(indeedScraper).scrape("java developer", "Sao Paulo", 10);
    }

    @Test
    @DisplayName("should skip disabled sources")
    void shouldSkipDisabledSources() {
        var properties = new ScrapingProperties();
        properties.setEnabled(true);
        properties.setSources(Map.of("linkedin", false, "indeed", true));

        orchestrator = new ScrapingOrchestrator(
            properties, deduplicationService, List.of(linkedInScraper, indeedScraper)
        );

        orchestrator.scrapeAllSources("java developer", "Sao Paulo");

        verify(linkedInScraper, never()).scrape(anyString(), anyString(), anyInt());
        verify(indeedScraper).scrape(anyString(), anyString(), anyInt());
    }

    @Test
    @DisplayName("should continue on single source failure")
    void shouldContinueOnSingleSourceFailure() {
        when(linkedInScraper.scrape(anyString(), anyString(), anyInt()))
            .thenThrow(new RuntimeException("Connection refused"));
        when(indeedScraper.scrape(anyString(), anyString(), anyInt()))
            .thenReturn(new ScrapingResult(List.of(), 10, 0));

        orchestrator.scrapeAllSources("java developer", "Sao Paulo");

        verify(indeedScraper).scrape("java developer", "Sao Paulo", 10);
    }
}
```

### Integration Test — Repository with Testcontainers

```java
package com.perfectjob.job.adapter.out;

import com.perfectjob.common.test.TestcontainersConfig;
import com.perfectjob.job.domain.model.Job;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.test.context.jdbc.Sql;

import java.math.BigDecimal;

import static org.assertj.core.api.Assertions.assertThat;

@Tag("integration")
@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Import(TestcontainersConfig.class)
@Sql(scripts = "/test-data/jobs.sql")
class JobJpaRepositoryIntegrationTest {

    @Autowired
    private JobJpaRepository repository;

    @Test
    @DisplayName("should find job by URL hash")
    void shouldFindJobByUrlHash() {
        var job = repository.findByUrlHash("abc123hash");

        assertThat(job).isPresent();
        assertThat(job.get().getTitle()).isEqualTo("Desenvolvedor Java Senior");
    }

    @Test
    @DisplayName("should search active jobs with filters")
    void shouldSearchActiveJobsWithFilters() {
        Page<Job> results = repository.searchActive(
            "java", "Sao Paulo", "SP", "CLT",
            PageRequest.of(0, 20)
        );

        assertThat(results.getContent()).isNotEmpty();
        assertThat(results.getContent())
            .allSatisfy(job -> {
                assertThat(job.getIsActive()).isTrue();
            });
    }

    @Test
    @DisplayName("should return empty when no jobs match")
    void shouldReturnEmptyWhenNoMatch() {
        Page<Job> results = repository.searchActive(
            "quantum physics", null, null, null,
            PageRequest.of(0, 20)
        );

        assertThat(results.getContent()).isEmpty();
    }
}
```

### Controller Test — MockMvc

```java
package com.perfectjob.job.adapter.in;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.perfectjob.job.dto.JobSearchRequest;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.bean.MockBean;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@Tag("integration")
@WebMvcTest(JobController.class)
class JobControllerTest {

    @Autowired private MockMvc mockMvc;
    @Autowired private ObjectMapper objectMapper;
    @MockBean private JobService jobService;

    @Test
    @WithMockUser
    @DisplayName("should return 200 with job results on valid search")
    void shouldReturn200OnValidSearch() throws Exception {
        var response = new JobResponse(1L, "Dev Java", "Tech Corp",
            "Sao Paulo", "CLT", 95.0, null);
        when(jobService.search(eq(1L), any(JobSearchRequest.class)))
            .thenReturn(new PageImpl<>(List.of(response), PageRequest.of(0, 20), 1));

        mockMvc.perform(post("/api/v1/jobs/search")
                .with(csrf())
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(
                    new JobSearchRequest("java", "Sao Paulo", null, null, null, null, null, 0, 20)
                )))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.content[0].title").value("Dev Java"))
            .andExpect(jsonPath("$.content[0].companyName").value("Tech Corp"));
    }

    @Test
    @DisplayName("should return 401 when not authenticated")
    void shouldReturn401WhenNotAuthenticated() throws Exception {
        mockMvc.perform(post("/api/v1/jobs/search")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{}"))
            .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser
    @DisplayName("should return 400 when query is blank")
    void shouldReturn400WhenQueryBlank() throws Exception {
        mockMvc.perform(post("/api/v1/jobs/search")
                .with(csrf())
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"query\":\"\"}"))
            .andExpect(status().isBadRequest());
    }
}
```

### Test Data Factory

```java
package com.perfectjob.common.test;

import com.perfectjob.job.domain.model.Job;
import java.math.BigDecimal;
import java.time.LocalDateTime;

public final class JobTestData {

    private JobTestData() {}

    public static Job.JobBuilder aJob() {
        return Job.builder()
            .source("indeed")
            .sourceId("indeed-12345")
            .sourceUrl("https://br.indeed.com/viewjob?jk=abc123")
            .urlHash("abc123hash456def")
            .title("Desenvolvedor Java Senior")
            .companyName("Tech Corp Brasil")
            .description("Vaga para desenvolvedor Java com experiencia em Spring Boot.")
            .location("Sao Paulo, SP")
            .city("Sao Paulo")
            .state("SP")
            .isRemote(false)
            .jobType("CLT")
            .experienceLevel("senior")
            .salaryMin(new BigDecimal("8000"))
            .salaryMax(new BigDecimal("15000"))
            .salaryCurrency("BRL")
            .tags(new String[]{"java", "spring", "postgresql"})
            .isActive(true)
            .postedDate(LocalDateTime.now().minusDays(2))
            .scrapedAt(LocalDateTime.now());
    }

    public static Job.JobBuilder aRemoteJob() {
        return aJob()
            .title("Desenvolvedor React Pleno - Remoto")
            .isRemote(true)
            .location("Remoto")
            .city(null)
            .state(null);
    }
}
```

### Mobile Test — React Native Testing Library

```typescript
// src/components/job/__tests__/JobCard.test.tsx
import { render, fireEvent } from '@testing-library/react-native';
import { JobCard } from '../JobCard';
import { aJob } from '../../../test/factories/jobFactory';

describe('JobCard', () => {
  const mockOnPress = jest.fn();

  it('should render job title and company name', () => {
    const job = aJob();
    const { getByText } = render(<JobCard job={job} onPress={mockOnPress} />);

    expect(getByText(job.title)).toBeTruthy();
    expect(getByText(job.companyName)).toBeTruthy();
  });

  it('should display salary range formatted in BRL', () => {
    const job = aJob({ salaryMin: 8000, salaryMax: 15000 });
    const { getByText } = render(<JobCard job={job} onPress={mockOnPress} />);

    expect(getByText(/R\$ 8.000/)).toBeTruthy();
  });

  it('should call onPress when pressed', () => {
    const job = aJob();
    const { getByTestId } = render(<JobCard job={job} onPress={mockOnPress} />);

    fireEvent.press(getByTestId('job-card'));
    expect(mockOnPress).toHaveBeenCalledTimes(1);
  });

  it('should display remote badge for remote jobs', () => {
    const job = aJob({ isRemote: true });
    const { getByText } = render(<JobCard job={job} onPress={mockOnPress} />);

    expect(getByText('Remoto')).toBeTruthy();
  });

  it('should display "A combinar" when no salary is provided', () => {
    const job = aJob({ salaryMin: null, salaryMax: null });
    const { getByText } = render(<JobCard job={job} onPress={mockOnPress} />);

    expect(getByText('A combinar')).toBeTruthy();
  });
});
```

### Mobile Test Data Factory

```typescript
// test/factories/jobFactory.ts
import type { Job } from '../../src/types/job';

interface JobOverrides extends Partial<Job> {}

export function aJob(overrides: JobOverrides = {}): Job {
  return {
    id: '1',
    title: 'Desenvolvedor Java Senior',
    companyName: 'Tech Corp Brasil',
    companyLogoUrl: null,
    description: 'Vaga para desenvolvedor Java com experiencia em Spring Boot.',
    location: 'Sao Paulo, SP',
    city: 'Sao Paulo',
    state: 'SP',
    country: 'BRA',
    isRemote: false,
    jobType: 'CLT',
    experienceLevel: 'senior',
    salaryMin: 8000,
    salaryMax: 15000,
    salaryCurrency: 'BRL',
    tags: ['java', 'spring', 'postgresql'],
    postedDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    sourceUrl: 'https://br.indeed.com/viewjob?jk=abc123',
    ...overrides,
  };
}
```

### Detox E2E Test (Mobile)

```typescript
// e2e/login.test.ts
describe('Login Flow', () => {
  beforeAll(async () => {
    await device.launchApp({ newInstance: true });
  });

  it('should show login screen on first launch', async () => {
    await expect(element(by.text('Entrar'))).toBeVisible();
    await expect(element(by.id('email-input'))).toBeVisible();
    await expect(element(by.id('password-input'))).toBeVisible();
  });

  it('should navigate to home after successful login', async () => {
    await element(by.id('email-input')).typeText('test@perfectjob.com.br');
    await element(by.id('password-input')).typeText('Test1234!\n');
    await element(by.id('login-button')).tap();

    await waitFor(element(by.id('home-screen')))
      .toBeVisible()
      .withTimeout(5000);
  });

  it('should display job feed on home screen', async () => {
    await waitFor(element(by.id('job-list')))
      .toBeVisible()
      .withTimeout(5000);

    await expect(element(by.id('job-card')).atIndex(0)).toBeVisible();
  });
});
```

## References

- JUnit 5: https://junit.org/junit5/docs/current/user-guide/
- Mockito 5: https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html
- Testcontainers: https://java.testcontainers.org/
- AssertJ: https://assertj.github.io/doc/
- Spring Boot Test: https://docs.spring.io/spring-boot/docs/3.4.x/reference/html/testing.html
- React Native Testing Library: https://callstack.github.io/react-native-testing-library/
- Detox: https://wix.github.io/Detox/
- Jest: https://jestjs.io/
