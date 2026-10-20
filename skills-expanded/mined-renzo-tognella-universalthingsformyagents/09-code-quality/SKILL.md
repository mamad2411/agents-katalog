# Code Quality — PerfectJob

> Clean code, SOLID, naming conventions, linting, code review checklist.

## Description

Padroes de qualidade de codigo para o PerfectJob. Aplica SOLID, DRY, KISS, YAGNI em todo o projeto. Define naming conventions, tamanho maximo de classes, cobertura de testes, e checklist de code review.

## Checklist

1. Cada classe tem no maximo 300 linhas — se passar, divida por responsabilidade
2. Cada metodo tem no maximo 30 linhas — se passar, extraia metodos privados
3. Max 5 parametros por metodo — se precisar mais, use um objeto (record ou DTO)
4. Nenhum nivel de indentacao > 4 — se passar, extraia metodo ou use early return
5. Nao duplique codigo — se copiar mais de 3 linhas, extraia para metodo compartilhado
6. Nomes de classes: PascalCase (`JobService`, `MatchingEngine`)
7. Nomes de metodos: camelCase, verbos (`findActiveJobs`, `calculateMatchScore`)
8. Nomes de variaveis: camelCase, substantivos descritivos (`activeJobs`, not `list`)
9. Nomes de constantes: UPPER_SNAKE_CASE (`MAX_RETRY_ATTEMPTS`)
10. Nomes de packages: lowercase, singular (`job` not `jobs`, `auth` not `authentication`)
11. Booleanos: prefixos `is`, `has`, `should` (`isActive`, `hasPermission`)
12. DTOs: sufixo `Request` ou `Response` (`JobSearchRequest`, `MatchResponse`)
13. Exceptions: sufixo `Exception` (`JobNotFoundException`)
14. Interfaces: sem prefixo `I` (`JobRepository`, not `IJobRepository`)
15. Testes: padrao `shouldX_whenY_givenZ`

## Key Rules

- **NEVER** deixe codigo morto (comentado) — delete, git guarda o historico
- **NEVER** use numeros magicos — extraia constantes com nomes descritivos
- **NEVER** retorne null — use Optional (backend) ou undefined com nullish coalescing (frontend)
- **NEVER** swollow exceptions — log e propague ou trate explicitamente
- **NEVER** use System.out.println — use SLF4J logger
- **NEVER** faça catch de Exception generica — catch especifico
- **ALWAYS** use Optional no retorno de queries que podem nao existir
- **ALWAYS** valide input na borda (controller) — nunca deixe chegar invalido no service
- **ALWAYS** use early return para reduzir indentacao
- **ALWAYS** faca PRs pequenos (<400 linhas) — mais faceis de revisar
- **ALWAYS** rode testes antes de commitar

## SOLID aplicado

### Single Responsibility (SRP)
```java
// ERRADO: JobService faz busca + scraping + matching
class JobService { ... }

// CERTO: uma classe, uma responsabilidade
class JobSearchService { ... }
class ScrapingOrchestrator { ... }
class MatchingService { ... }
```

### Open/Closed (OCP)
```java
// Use Strategy para extensao sem modificacao
public interface JobScraper {
    List<RawJob> scrape(ScrapeConfig config);
}

class LinkedInScraper implements JobScraper { ... }
class IndeedScraper implements JobScraper { ... }
// Adicionar novo scraper = nova classe, sem mudar nada existente
```

### Liskov Substitution (LSP)
```java
// Subtipos devem ser substituiveis pelo tipo base
// Todos JobScraper implementations devem funcionar com ScrapingOrchestrator
// sem comportamento especial por tipo
```

### Interface Segregation (ISP)
```java
// ERRADO: interface gordona
interface JobRepository {
    Job findById(UUID id);
    Page<Job> search(JobSearchCriteria criteria);
    void updateEmbedding(UUID id, float[] embedding);
    long countActive();
    void deleteExpired();
}

// CERTO: interfaces pequenas e especificas
interface JobReader {
    Job findById(UUID id);
    Page<Job> search(JobSearchCriteria criteria);
}

interface JobWriter {
    Job save(Job job);
    void updateEmbedding(UUID id, float[] embedding);
}
```

### Dependency Inversion (DIP)
```java
// Services dependem de interfaces (ports), nao implementacoes
@Service
class MatchingService {
    private final EmbeddingProvider embeddingProvider; // interface
    private final JobRepository jobRepository;          // interface
    
    // Injecao via construtor
    public MatchingService(EmbeddingProvider embeddingProvider, JobRepository jobRepository) {
        this.embeddingProvider = embeddingProvider;
        this.jobRepository = jobRepository;
    }
}
```

## Code Review Checklist

Antes de aprovar um PR, verificar:

- [ ] Nao ha codigo morto ou comentarios desnecessarios
- [ ] Classes < 300 linhas, metodos < 30 linhas
- [ ] Nao ha logica de negocio em controllers
- [ ] Input validado com Jakarta Validation
- [ ] Excecoes tratadas com GlobalExceptionHandler
- [ ] DTOs usados na borda (controller), nunca entidades JPA
- [ ] MapStruct para conversao entity <-> DTO
- [ ] Testes escritos (unit + integration se aplicavel)
- [ ] Nomes descritivos (sem abreviacoes obscuras)
- [ ] PII criptografado, sem secrets no codigo
- [ ] Migration Flyway criada se mudou schema

## Linting

### Backend
- Checkstyle com Google Java Style (modificado: 120 char line limit)
- SpotBugs para static analysis
- `./gradlew checkstyleMain spotbugsMain`

### Frontend
- ESLint com @typescript-eslint/recommended
- Prettier com config: singleQuote, trailingComma, printWidth 100
- `npm run lint && npm run typecheck`

## References
- Clean Code — Robert C. Martin
- Effective Java — Joshua Bloch (3rd Edition)
- Spring Boot Best Practices — https://docs.spring.io/spring-boot/reference/
