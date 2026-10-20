# CLAUDE.md

## Commands

```bash
./mvnw spring-boot:run                                          # requer PostgreSQL
./mvnw test                                                     # H2 in-memory, sem PostgreSQL
./mvnw test -Dtest=AtributoConfiguracaoServiceIntegrationTest   # classe específica
./mvnw test -Dtest=AtributoConfiguracaoServiceIntegrationTest#deveCriarConfiguracaoComSucesso
./mvnw package -DskipTests
docker compose up -d                                            # PostgreSQL via Docker
```

## Project

Spring Boot 4 / Java 25 REST API para fichas de RPG de mesa. Princípio central: **tudo configurável pelo Mestre, nada hardcoded**. Detalhes completos em `docs/backend/`.

### Stack

- Java 25, Spring Boot 4.0.2, PostgreSQL, H2 (testes)
- MapStruct 1.5.5 (mapeamento compile-time)
- OAuth2 Google + sessão (não JWT)
- exp4j para avaliação de fórmulas matemáticas

### Package structure

```
model/                        — entidades JPA
repository/                   — Spring Data JPA
service/configuracao/         — lógica de negócio (abstract base + 13 concretos)
controller/configuracao/      — controllers REST (thin layer)
dto/request/configuracao/     — DTOs de entrada (records)
dto/response/configuracao/    — DTOs de saída (records)
dto/defaults/                 — DTOs para inicialização de configs padrão
mapper/configuracao/          — MapStruct (request ↔ entity ↔ response)
config/                       — Security, OpenAPI, RateLimit, Audit
service/FormulaEvaluatorService — avalia fórmulas via exp4j
service/GameConfigInitializerService — popula configs padrão ao criar Jogo
```

## Core Abstractions

**`BaseEntity`** — todas as entidades estendem: soft delete (`deleted_at`), audit fields (`created_at`, `updated_at`, `created_by`, `updated_by`), `@SQLRestriction("deleted_at IS NULL")` (registros deletados invisíveis por padrão). Use `.delete()` / `.restore()`.

**`ConfiguracaoEntity`** — interface marker para entidades de configuração; exige `getId()` e `getJogo()`. Toda entidade de configuração deve implementar.

**`AbstractConfiguracaoService<T, R>`** — CRUD genérico para configurações. Subclasses sobrescrevem:
- `atualizarCampos(existente, atualizado)` — **obrigatório**
- `validarAntesCriar(configuracao)` — validação de nome duplicado etc.
- `validarAntesAtualizar(existente, atualizado)` — cheques de conflito

**`BaseConfiguracaoServiceIntegrationTest<T, S, R>`** — base abstrata para todos os testes de configuração. Implementar: `getService()`, `getRepository()`, `criarConfiguracaoValida()`, `criarConfiguracaoComNomeDuplicado()` (null = não valida), `atualizarCamposParaTeste()`, `verificarCamposAtualizados()`. Fornece ~10 testes automaticamente.

## Request Flow

```
HTTP → Controller (@Valid, mapper.toEntity) → Service (lógica, validações) → Repository → DB
                                             ← mapper.toResponse ←
```

- Controllers: thin (coordenação apenas), sem lógica de negócio
- Mappers: sempre na controller, nunca no service
- Services: trabalham com entities, lançam exceptions específicas
- `@Transactional(readOnly = true)` na classe, `@Transactional` em métodos de escrita

## Configuration Entities (13)

Todas estendem `BaseEntity` + implementam `ConfiguracaoEntity`, têm unique constraint `(jogo_id, nome)` e campo `ordemExibicao`.

| Entidade | Campos específicos |
|---|---|
| `AtributoConfig` | `abreviacao` (2-5), `formulaImpeto`, `valorMinimo/Maximo` |
| `AptidaoConfig` | `tipoAptidao` (FK → TipoAptidao) |
| `BonusConfig` | `formulaBase` (max 200) |
| `ClassePersonagem` | — |
| `DadoProspeccaoConfig` | `numeroFaces` (1-100) |
| `GeneroConfig` | — |
| `IndoleConfig` | — |
| `MembroCorpoConfig` | `porcentagemVida` (BigDecimal, 0.01-1.00) |
| `NivelConfig` | `nivel`, `xpNecessaria`, `pontosAtributo`, `pontosAptidao`, `limitadorAtributo` |
| `PresencaConfig` | — |
| `Raca` | → `List<RacaBonusAtributo>` |
| `TipoAptidao` | — |
| `VantagemConfig` | `nivelMaximo`, `formulaCusto`, `descricaoEfeito` |

**Entidades auxiliares sem controller ainda:**
- `RacaBonusAtributo` — bônus de atributo por raça (campo `bonus` pode ser negativo)
- `PontosVantagemConfig` — pontos de vantagem ganhos por nível

## Security

- `@PreAuthorize("hasRole('MESTRE')")` em writes (POST, PUT, DELETE)
- `@PreAuthorize("hasAnyRole('MESTRE', 'JOGADOR')")` em reads
- CORS via `app.cors.allowed-origins`
- Rate limit: 100 req/min geral, 10 req/min auth

## Testing

- `@ActiveProfiles("test")`, H2 in-memory, `ddl-auto=create-drop` — sem Flyway
- `@Transactional` nos testes (rollback automático) + limpeza manual no `@BeforeEach`
- **Preferir testes de integração** (80%) sobre unitários
- Usar `@DisplayName` descritivo e padrão Arrange-Act-Assert

## Adding a new configuration entity

1. Model: `extends BaseEntity implements ConfiguracaoEntity`, unique constraint `(jogo_id, nome)`
2. Repository: `extends JpaRepository`, método `findByJogoIdOrderByOrdemExibicao`
3. Service: `extends AbstractConfiguracaoService`, implementar `atualizarCampos()` e `validarAntesCriar()` (se valida nome)
4. DTOs: Create/Update records + Response record com `dataCriacao`, `dataUltimaAtualizacao`
5. Mapper: MapStruct com `@Mapping(target="jogoId", source="jogo.id")` e `NullValuePropertyMappingStrategy.IGNORE` no update
6. Controller: seguir padrão de `AtributoController`
7. Teste: `extends BaseConfiguracaoServiceIntegrationTest`

## Lombok Pattern (entidades)

```java
@Data @EqualsAndHashCode(callSuper = true) @Builder @NoArgsConstructor @AllArgsConstructor
```

## FormulaEvaluatorService

Avalia expressões matemáticas via exp4j. Variáveis disponíveis: `total`, `nivel`, `base`, abreviações de atributos (`FOR`, `AGI`, `VIG`, `SAB`, `INT`, `INTU`, `AST`). Métodos: `calcularImpeto()`, `calcularDerivado()`, `calcularCustoVantagem()`, `isValid()`.

**⚠️ REGRA CRÍTICA**: Toda sigla/abreviação deve ser **ÚNICA por jogo, cross-entity**. Se `FOR` existe como abreviação de atributo, nenhuma vantagem, bônus ou outra configuração do mesmo jogo pode usar `FOR`. Validar unicidade no escopo do jogo inteiro ao criar/editar.

## Key properties

| Property | Default |
|---|---|
| DB | `jdbc:postgresql://localhost:5432/rpg_fichas` |
| Port | `8080` |
| Swagger | `/swagger-ui.html` |
| CORS | `http://localhost:4200,http://localhost:80` |

## Docs

- `docs/GLOSSARIO.md` — **LEIA PRIMEIRO**: resumo e índice do glossário do domínio Klayrah RPG
- `docs/glossario/` — glossário completo dividido em módulos:
  - `01-contexto-geral.md` — o que é Klayrah, quem usa, conceitos estruturais
  - `02-configuracoes-jogo.md` — as 13+1 configurações detalhadas
  - `03-termos-dominio.md` — glossário de termos por sistema (Atributos, Vida, Vantagens, etc.)
  - `04-siglas-formulas.md` — sistema de siglas, unicidade por jogo, motor de fórmulas
  - `05-termos-tecnicos-fluxo.md` — termos técnicos, fluxo configuração→ficha, status

Padrões detalhados em `docs/backend/`:
- `01-architecture.md` — camadas, DI, fluxo completo
- `02-entities-dtos.md` — Lombok, records, validações, Java 25 features
- `03-exceptions.md` — hierarquia de exceptions, GlobalExceptionHandler
- `04-repositories.md` — query methods, Optional
- `05-services.md` — transações, padrões de update
- `06-mappers.md` — MapStruct patterns
- `07-controllers.md` — REST patterns, Swagger, HTTP status codes
- `08-security.md` — OAuth2, sessão, CORS
- `09-testing.md` — integração vs unitário, templates
- `10-database.md` — naming conventions
- `11-owasp-security.md` — OWASP Top 10
