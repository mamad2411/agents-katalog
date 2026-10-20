# Matching Engine — PerfectJob

> Cohere embed-multilingual-v3.0, hybrid scoring, per-section embeddings, user weight system, MiniMax2.7 explainability.

## Description

PerfectJob's matching engine computes job-resume compatibility using a hybrid approach: semantic similarity via embeddings (55%) combined with structured field matching (45%). The system uses Cohere's multilingual embedding model optimized for Portuguese-BR text, per-section embedding with configurable weights, and a user-driven skill weight system. MiniMax2.7 via OpenRouter provides skill extraction and match explainability in natural PT-BR language.

**Stack**: Cohere embed-multilingual-v3.0 (1024 dims), pgvector (HNSW cosine), MiniMax2.7 via OpenRouter, Spring Boot 3.4.

## Checklist

1. Generate embeddings using Cohere `embed-multilingual-v3.0` with `search_document` input type for jobs and `search_query` for resumes
2. Chunk resume into sections: skills (0.40), experience (0.35), education (0.15), summary (0.10)
3. Chunk job listing into the same sections for per-section comparison
4. Apply user weight system (1-5) to skill matching — weights come from repetition frequency
5. Run two-phase pipeline: Phase 1 — ANN top-200 via pgvector cosine; Phase 2 — re-rank top-20 with per-section + structured scoring
6. Compute hybrid score: 55% embedding similarity + 45% structured field match
7. Normalize final score with sigmoid function to 0-100% range
8. Call MiniMax2.7 for skill extraction from resumes and match explanation generation
9. Store match results with individual scores (embedding_score, structured_score, skill_match breakdown)
10. Cache embeddings for jobs — regenerate only when job is updated
11. Batch embedding requests (max 96 texts per Cohere API call)
12. Handle Cohere rate limits with exponential backoff (429 → wait → retry)

## Key Rules

- **NEVER** use symmetric encoding — always use `search_document` for jobs, `search_query` for resumes
- **NEVER** skip per-section weighting — overall embedding alone is insufficient for quality matches
- **NEVER** use embedding dimensions other than 1024 — that's what pgvector indexes are configured for
- **NEVER** call the LLM for scoring — only for extraction and explanation
- **NEVER** return matches below 30% score — filter them out as noise
- **ALWAYS** use Cohere's batch API — never send one text at a time
- **ALWAYS** store individual section scores for transparency and debugging
- **ALWAYS** normalize scores to 0-100% using sigmoid before returning to the user
- **ALWAYS** include the explanation from MiniMax2.7 with every top-20 match
- **ALWAYS** pre-compute job embeddings at scrape time — never compute at query time

## Architecture

```
com.perfectjob.matching/
├── domain/
│   ├── model/
│   │   ├── MatchResult.java          # sealed interface: Success, Skipped, Failed
│   │   ├── SectionScore.java         # record: section, weight, rawScore, weightedScore
│   │   ├── MatchExplanation.java     # record: summary, matchedSkills, missingSkills
│   │   └── UserWeight.java           # record: skillName, weight(1-5)
│   └── port/
│       ├── EmbeddingService.java     # port for embedding generation
│       ├── LlmService.java           # port for skill extraction + explanation
│       └── MatchingRepository.java   # port for match persistence
├── adapter/in/
│   └── MatchingController.java       # REST API for triggering matches
├── adapter/out/
│   ├── CohereEmbeddingAdapter.java   # implements EmbeddingService
│   └── OpenRouterLlmAdapter.java     # implements LlmService (MiniMax2.7)
├── service/
│   ├── MatchingEngine.java           # Core two-phase pipeline
│   ├── EmbeddingService.java         # Embedding orchestration + caching
│   ├── SectionChunker.java           # Resume/Job section splitting
│   ├── ScoreCalculator.java          # Hybrid score computation
│   └── WeightSystem.java             # User skill weight calculation
└── config/
    └── MatchingProperties.java       # Weights, thresholds, model config
```

## Scoring Formula

### Section Weights

| Section | Resume Weight | Rationale |
|---------|--------------|-----------|
| Skills | 0.40 | Most important signal for job matching |
| Experience | 0.35 | Work history relevance |
| Education | 0.15 | Academic background |
| Summary | 0.10 | Professional objective alignment |

### Hybrid Score

```
embedding_score = Σ (section_cosine_similarity * section_weight)   [0.0 - 1.0]
structured_score = f(skills_match, salary_match, location_match, level_match)   [0.0 - 1.0]
raw_score = 0.55 * embedding_score + 0.45 * structured_score
final_score = sigmoid((raw_score - 0.5) * 10) * 100               [0 - 100]
```

### Structured Score Breakdown (45%)

| Component | Weight | Method |
|-----------|--------|--------|
| Skills match | 50% | Jaccard similarity with user weights |
| Salary match | 20% | Range overlap ratio |
| Location match | 20% | City=1.0, State=0.7, Remote=0.5 |
| Experience level | 10% | Exact match=1.0, adjacent=0.5 |

### User Weight System

```
weight = clamp(round(log2(occurrence_count + 1)), 1, 5)
```

Skills mentioned multiple times in a resume get higher weights (1-5). A skill appearing 1 time = weight 1, 2 times = weight 2, 4+ times = weight 3, 8+ times = weight 4, 16+ times = weight 5.

## Code Examples

### MatchingProperties

```java
package com.perfectjob.matching.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

import java.util.Map;

@Data
@Component
@ConfigurationProperties(prefix = "perfectjob.matching")
public class MatchingProperties {

    private int annTopK = 200;
    private int rerankTopK = 20;
    private double minScorePercent = 30.0;

    private Weights weights = new Weights();
    private Cohere cohere = new Cohere();
    private OpenRouter openRouter = new OpenRouter();

    @Data
    public static class Weights {
        private Map<String, Double> sections = Map.of(
            "skills", 0.40,
            "experience", 0.35,
            "education", 0.15,
            "summary", 0.10
        );
        private double embeddingWeight = 0.55;
        private double structuredWeight = 0.45;
        private Map<String, Double> structured = Map.of(
            "skills", 0.50,
            "salary", 0.20,
            "location", 0.20,
            "level", 0.10
        );
    }

    @Data
    public static class Cohere {
        private String model = "embed-multilingual-v3.0";
        private String inputTypeJobs = "search_document";
        private String inputTypeResumes = "search_query";
        private int batchSize = 96;
        private int maxRetries = 3;
    }

    @Data
    public static class OpenRouter {
        private String model = "minimax/max-2.7";
        private String baseUrl = "https://openrouter.ai/api/v1";
        private int maxTokens = 2000;
        private double temperature = 0.3;
    }
}
```

### Section Chunker

```java
package com.perfectjob.matching.service;

import com.perfectjob.matching.config.MatchingProperties;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.LinkedHashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class SectionChunker {

    private final MatchingProperties properties;

    public Map<String, String> chunkResume(String skills, String experience,
                                            String education, String summary) {
        Map<String, String> sections = new LinkedHashMap<>();
        sections.put("skills", nullSafe(skills));
        sections.put("experience", nullSafe(experience));
        sections.put("education", nullSafe(education));
        sections.put("summary", nullSafe(summary));
        return sections;
    }

    public Map<String, String> chunkJob(String title, String description,
                                         String requirements, String tags) {
        Map<String, String> sections = new LinkedHashMap<>();
        sections.put("skills", nullSafe(tags) + " " + nullSafe(requirements));
        sections.put("experience", nullSafe(description));
        sections.put("education", nullSafe(requirements));
        sections.put("summary", nullSafe(title) + " " + nullSafe(description));
        return sections;
    }

    private String nullSafe(String s) {
        return s != null ? s : "";
    }
}
```

### Cohere Embedding Adapter

```java
package com.perfectjob.matching.adapter.out;

import com.perfectjob.matching.config.MatchingProperties;
import com.perfectjob.matching.domain.port.EmbeddingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.net.URI;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class CohereEmbeddingAdapter implements EmbeddingService {

    private final MatchingProperties properties;
    private final RestTemplate restTemplate;

    @Override
    public List<float[]> generateEmbeddings(List<String> texts, String inputType) {
        int batchSize = properties.getCohere().getBatchSize();
        var allEmbeddings = new java.util.ArrayList<float[]>();

        for (int i = 0; i < texts.size(); i += batchSize) {
            List<String> batch = texts.subList(i, Math.min(i + batchSize, texts.size()));
            var request = new CohereEmbedRequest(
                batch,
                properties.getCohere().getModel(),
                inputType
            );

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.setBearerAuth(System.getenv("COHERE_API_KEY"));

            ResponseEntity<CohereEmbedResponse> response = restTemplate.exchange(
                URI.create("https://api.cohere.ai/v2/embed"),
                HttpMethod.POST,
                new HttpEntity<>(request, headers),
                CohereEmbedResponse.class
            );

            if (response.getBody() != null) {
                allEmbeddings.addAll(response.getBody().embeddings());
            }
        }

        return allEmbeddings;
    }

    public record CohereEmbedRequest(List<String> texts, String model, String input_type) {}
    public record CohereEmbedResponse(List<float[]> embeddings) {}
}
```

### Score Calculator

```java
package com.perfectjob.matching.service;

import com.perfectjob.matching.config.MatchingProperties;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ScoreCalculator {

    private final MatchingProperties properties;

    public double computeEmbeddingScore(Map<String, Double> sectionScores) {
        Map<String, Double> sectionWeights = properties.getWeights().getSections();
        return sectionScores.entrySet().stream()
            .mapToDouble(e -> e.getValue() * sectionWeights.getOrDefault(e.getKey(), 0.0))
            .sum();
    }

    public double computeStructuredScore(double skillMatch, double salaryMatch,
                                          double locationMatch, double levelMatch) {
        Map<String, Double> sw = properties.getWeights().getStructured();
        return sw.get("skills") * skillMatch
             + sw.get("salary") * salaryMatch
             + sw.get("location") * locationMatch
             + sw.get("level") * levelMatch;
    }

    public double computeHybridScore(double embeddingScore, double structuredScore) {
        double raw = properties.getWeights().getEmbeddingWeight() * embeddingScore
                   + properties.getWeights().getStructuredWeight() * structuredScore;
        return sigmoidNormalize(raw);
    }

    private double sigmoidNormalize(double raw) {
        return 100.0 / (1.0 + Math.exp(-10.0 * (raw - 0.5)));
    }
}
```

### Matching Engine (Two-Phase Pipeline)

```java
package com.perfectjob.matching.service;

import com.perfectjob.matching.config.MatchingProperties;
import com.perfectjob.matching.domain.model.MatchResult;
import com.perfectjob.matching.domain.port.EmbeddingService;
import com.perfectjob.matching.domain.port.LlmService;
import com.perfectjob.matching.domain.port.MatchingRepository;
import com.perfectjob.job.domain.port.JobRepository;
import com.perfectjob.resume.domain.port.ResumeRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.*;

@Slf4j
@Service
@RequiredArgsConstructor
public class MatchingEngine {

    private final MatchingProperties properties;
    private final EmbeddingService embeddingService;
    private final LlmService llmService;
    private final SectionChunker sectionChunker;
    private final ScoreCalculator scoreCalculator;
    private final WeightSystem weightSystem;
    private final JobRepository jobRepository;
    private final ResumeRepository resumeRepository;
    private final MatchingRepository matchingRepository;

    public List<MatchResult.Success> findMatches(Long userId) {
        var resume = resumeRepository.findActiveByUserId(userId)
            .orElseThrow(() -> new NoSuchElementException("No active resume for user: " + userId));

        Map<String, String> resumeSections = sectionChunker.chunkResume(
            String.join(", ", resume.getSkills()),
            resume.getExperience().toString(),
            resume.getEducation().toString(),
            resume.getSummary()
        );

        Map<String, float[]> resumeEmbeddings = new LinkedHashMap<>();
        for (var entry : resumeSections.entrySet()) {
            if (!entry.getValue().isBlank()) {
                var embeddings = embeddingService.generateEmbeddings(
                    List.of(entry.getValue()), "search_query"
                );
                resumeEmbeddings.put(entry.getKey(), embeddings.get(0));
            }
        }

        float[] combinedResumeEmbedding = combineSectionEmbeddings(
            resumeEmbeddings, properties.getWeights().getSections()
        );

        List<Job> topJobs = jobRepository.findSimilarJobs(
            new PGvector(combinedResumeEmbedding),
            properties.getAnnTopK()
        );

        List<MatchResult.Success> results = new ArrayList<>();

        for (Job job : topJobs) {
            Map<String, String> jobSections = sectionChunker.chunkJob(
                job.getTitle(), job.getDescription(),
                job.getRequirements(), String.join(",", job.getTags())
            );

            Map<String, Double> sectionScores = computeSectionScores(resumeEmbeddings, job);

            double embeddingScore = scoreCalculator.computeEmbeddingScore(sectionScores);

            Map<String, Integer> userWeights = weightSystem.getWeights(resume.getId());
            double skillMatch = computeWeightedSkillMatch(resume.getSkills(), job.getTags(), userWeights);
            double salaryMatch = computeSalaryMatch(resume, job);
            double locationMatch = computeLocationMatch(resume, job);
            double levelMatch = computeLevelMatch(resume, job);

            double structuredScore = scoreCalculator.computeStructuredScore(
                skillMatch, salaryMatch, locationMatch, levelMatch
            );

            double finalScore = scoreCalculator.computeHybridScore(embeddingScore, structuredScore);

            if (finalScore < properties.getMinScorePercent()) continue;

            String explanation = llmService.generateExplanation(resume, job, finalScore, sectionScores);

            results.add(new MatchResult.Success(job.getId(), finalScore, explanation));

            if (results.size() >= properties.getRerankTopK()) break;
        }

        results.sort(java.util.Comparator.comparingDouble(MatchResult.Success::score).reversed());
        matchingRepository.saveMatches(userId, results);

        return results;
    }

    private float[] combineSectionEmbeddings(Map<String, float[]> embeddings,
                                              Map<String, Double> weights) {
        float[] combined = new float[1024];
        for (var entry : embeddings.entrySet()) {
            double weight = weights.getOrDefault(entry.getKey(), 0.25);
            float[] vec = entry.getValue();
            for (int i = 0; i < 1024; i++) {
                combined[i] += (float) (vec[i] * weight);
            }
        }
        return normalize(combined);
    }

    private float[] normalize(float[] vec) {
        double norm = 0;
        for (float v : vec) norm += v * v;
        norm = Math.sqrt(norm);
        float[] result = new float[vec.length];
        for (int i = 0; i < vec.length; i++) result[i] = (float) (vec[i] / norm);
        return result;
    }
}
```

### Weight System

```java
package com.perfectjob.matching.service;

import com.perfectjob.resume.domain.port.WeightedSkillRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class WeightSystem {

    private final WeightedSkillRepository weightedSkillRepository;

    public Map<String, Integer> getWeights(Long resumeId) {
        return weightedSkillRepository.findByResumeId(resumeId).stream()
            .collect(Collectors.toMap(
                ws -> ws.getSkillName().toLowerCase(),
                ws -> ws.getWeight(),
                (a, b) -> Math.max(a, b)
            ));
    }

    public int calculateWeight(int occurrenceCount) {
        return Math.max(1, Math.min(5, (int) Math.round(Math.log2(occurrenceCount + 1))));
    }
}
```

## References

- Cohere Embed v3: https://docs.cohere.com/reference/embed
- pgvector cosine: https://github.com/pgvector/pgvector#querying
- OpenRouter API: https://openrouter.ai/docs
- MiniMax2.7: https://openrouter.ai/models/minimax/max-2.7
- Sigmoid normalization: https://en.wikipedia.org/wiki/Sigmoid_function
