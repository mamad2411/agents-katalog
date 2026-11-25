---
name: sky-spring
description: >-
  Java/Kotlin ile Spring Boot 3: alan bazlı paket yapısı, REST controller, DTO olarak record'lar,
  Bean Validation, servis katmanı ve transaction sınırları, Spring Data JPA tuzakları (N+1,
  lazy loading, open-in-view), Flyway migration, Spring Security (JWT, metot güvenliği), global
  hata yönetimi (ProblemDetail), Testcontainers ile testler, Actuator, virtual thread'ler ve
  dağıtım. Spring Boot projesinde kullan.
disable-model-invocation: true
---

# Sky · Spring Boot

## Yapı (alan bazlı paketler)

```
com.acme.app
  booking/  BookingController, BookingService, BookingRepository, Booking (entity), BookingDtos (records)
  client/
  common/   error/, security/, config/
```
Katman paketleri yerine alan paketleri; `package-private` ile kapsülleme.

## Controller + DTO

```java
public record CreateBookingRequest(@NotNull UUID serviceId, @NotNull @Future OffsetDateTime startsAt,
                                   @Pattern(regexp = "^\\+905\\d{9}$") String phone) {}

public record BookingResponse(UUID id, OffsetDateTime startsAt, BookingStatus status) {
    static BookingResponse from(Booking b) { return new BookingResponse(b.getId(), b.getStartsAt(), b.getStatus()); }
}

@RestController
@RequestMapping("/api/bookings")
class BookingController {
    private final BookingService service;
    BookingController(BookingService service) { this.service = service; }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    BookingResponse create(@Valid @RequestBody CreateBookingRequest req, @AuthenticationPrincipal Jwt jwt) {
        return BookingResponse.from(service.create(jwt.getSubject(), req));
    }
}
```
Entity'yi asla doğrudan döndürme. Constructor injection.

## Transaction ve JPA

- `@Transactional` servis metotlarında; okumalar `@Transactional(readOnly = true)`.
- `spring.jpa.open-in-view=false` — view katmanında gizli lazy sorgu olmasın.
- N+1: `@EntityGraph(attributePaths = {"client", "service"})` veya `join fetch`; ilişkiler `@ManyToOne(fetch = FetchType.LAZY)`.
- Sayfalama `Pageable`; büyük tablolarda keyset.
- Sorgu sayısını görmek için `logging.level.org.hibernate.SQL=debug`.
- Eşzamanlılık: `@Version` (optimistic) veya `@Lock(LockModeType.PESSIMISTIC_WRITE)`.
- Şema: `spring.jpa.hibernate.ddl-auto=validate` + **Flyway** (`db/migration/V3__add_bookings.sql`); `update` asla prod'da.

## Hata yönetimi

```java
@RestControllerAdvice
class ApiErrors {
    @ExceptionHandler(NotFoundException.class)
    ProblemDetail notFound(NotFoundException e) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
    }
}
```
`spring.mvc.problemdetails.enabled=true` → RFC 9457 biçimi.

## Güvenlik

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .csrf(c -> c.disable())   // yalnızca saf token API'de; çerez oturumunda CSRF açık kalsın
        .authorizeHttpRequests(a -> a.requestMatchers("/actuator/health").permitAll().anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .build();
}
```
- `@EnableMethodSecurity` + `@PreAuthorize`; sahiplik kontrolü serviste.
- Parola: `PasswordEncoderFactories.createDelegatingPasswordEncoder()`.

## Test

```java
@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers
class BookingApiTest {
    @Container @ServiceConnection
    static PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16");
    @Autowired MockMvc mvc;

    @Test @WithMockUser
    void otherOrgBookingIsNotFound() throws Exception {
        mvc.perform(get("/api/bookings/{id}", UUID.randomUUID())).andExpect(status().isNotFound());
    }
}
```
Dilim testleri: `@WebMvcTest`, `@DataJpaTest`.

## Çalışma zamanı ve dağıtım

- `spring.threads.virtual.enabled=true` (Java 21+).
- **Actuator**: health, info, metrics, prometheus; hassas uç noktaları kapat/koru.
- `@ConfigurationProperties` record'ları + doğrulama; sırlar env.
- `./mvnw spring-boot:build-image` veya katmanlı jar Dockerfile; GraalVM native image hızlı açılış için.
- Kotlin: aynı kalıplar; `kotlin-spring` ve `kotlin-jpa` eklentileri.
